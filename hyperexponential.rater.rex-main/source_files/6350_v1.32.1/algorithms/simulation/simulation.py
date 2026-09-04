import hx, os, json, math, gc, io
import pandas as pd
import polars as pl
import numpy as np
from typing import Dict
from algorithms.exposure_management_task import pull_exchange_rate_data
from algorithms.schedule_clean_state_county import clean_state_county, schedule_table_hxd_assignment_state_county
from algorithms.simulation.deductible_logic import apply_deductibles, loss_to_layer, add_deductible_info, map_tier_columns, gather_peril_deductibles, apply_sublimits, apply_per_occurrence_deductible
from algorithms.simulation.stats_functions import calc_stddev, exceedence_prob_curves, marginal_impacts, agg_losses, calc_aal
from algorithms.simulation.data_imports import load_from_em_database, FeatherLoader, LoadFromSQL
from algorithms.simulation.utils import SimulationProgress, is_df_empty, has_intl_or_us_tiv, conv_col_lowercase, has_intl_or_us_elt
from algorithms.utilities import TimerTracker, pd_df_from_hx_list
from algorithms.schedule import get_currency_exchange


def run_simulation(hxd, progress):

    if not hxd.policy_information.accgrpid:
        hx.errors.fatal("Simulation Fail. Please import account from Exposure Management Database.")

    # Validation Output
    validation_output = dict()
    for index, layer in enumerate(hxd.layers, start=1):
        validation_output[f"simulation_excess{index}"] = layer.excess
        validation_output[f"simulation_limit{index}"] = layer.limit
    hxd.temp.simulation_validation_json = json.dumps(validation_output)

    # Pull exchange rate data from EM database
    pull_exchange_rate_data(hxd, progress)
    exchange_rate = hxd.policy_information.exchange_rate or 1

    # Initialise loader which will load a polars df and save in cache
    loader = FeatherLoader()
    sql_loader = LoadFromSQL()

    # Check whether the data frame has US or INTL exposure
    has_us, has_intl = has_intl_or_us_elt(hxd, sql_loader)
    status = SimulationProgress(hxd, progress, len(hxd.layers), has_us, has_intl)

    # Set variables which don't vary by layer
    sims = 1_000_000
    EP = np.array([10000, 5000, 1000, 500, 250, 200, 150, 100, 50, 30, 10, 2])
   
    ws_num_options = hxd.non_layer_perils.named_windstorm.num_options or 0
    eq_num_options = hxd.non_layer_perils.quake.num_options or 0

    per_occ_sublimits = {
        "WS": (hxd.sublimit.ws_sublimit or 0) / exchange_rate,
        "EQ": (hxd.sublimit.eq_sublimit or 0) / exchange_rate
    } 

    df = extract_schedule_df(hxd, progress)

    eym = yelt = event_pt3 = pt_max = pt_sum = None # initialise dfs that will be deleted after the US loop - catches instances where there are no ws/eq perils selected
    
    # ---------------------------------------------------
    # US Locations
    # ---------------------------------------------------

    if has_us:
        us_df = prepare_schedule(df)

        for index, layer in enumerate(hxd.layers):

            elt_basis = layer.elt_for_sim

            # Set seeed as Random State object for reproductable beta
            rng = np.random.RandomState(seed=3)

            ws_include = layer.perils.named_windstorm.include
            eq_include = layer.perils.quake.include
            cal_eq_include = layer.perils.quake.ca_quake_include

            if not any([ws_include, eq_include]):
                status.skip_us()
                continue

            limit = layer.limit / exchange_rate
            excess = layer.excess / exchange_rate
            
            per_occ_ded = {
                "WS": (layer.perils.named_windstorm.per_occurrence_ded or 0) / exchange_rate,
                "EQ": (layer.perils.quake.per_occurrence_ded or 0) / exchange_rate
            }

            # ---------------------------------------------------
            # US Deductibles    
            
            ws_opts = gather_peril_deductibles(layer, exchange_rate, "named_windstorm", ws_num_options)
            eq_opts = gather_peril_deductibles(layer, exchange_rate, "quake",           eq_num_options)
        
            tier_list_df = produce_tier_list(ws_opts, eq_opts)
            loc_file_df = join_tiers_to_schedule(us_df, tier_list_df)

            event_dfs = []       
            eventdata_eq = pl.DataFrame() # Avoids assignment error below
            if ws_include:
                toplocs_ws = determine_toplocs_ws(loc_file_df)
                eventdata_ws = us_ws_event_county_mapping(loader, toplocs_ws)
                event_dfs.append(eventdata_ws)
            if eq_include:
                toplocs_eq = determine_toplocs_eq(loc_file_df)
                eventdata_eq = us_eq_event_county_mapping(loader, toplocs_eq)
                event_dfs.append(eventdata_eq)

            eventdata_all = pl.concat(event_dfs).drop(["Statecode", "County"])

            loc_file_df = loc_file_df.merge(eventdata_all.to_pandas(), on='StateCountyKey', how='left')
            
            loc_file_df['WS_Ded_Type'] = 'No deductible'
            loc_file_df['EQ_Ded_Type'] = 'No deductible'

            for i in range(3):
                if ws_include:
                    add_deductible_info(loc_file_df, 'WS_Ded',      ws_opts[i]["region"], ws_opts[i]["state"], ws_opts[i]["amt"],  f"Tier_{i+1}_WS")
                    add_deductible_info(loc_file_df, 'WS_Ded_Perc', ws_opts[i]["region"], ws_opts[i]["state"], ws_opts[i]["perc"], f"Tier_{i+1}_WS")
                    add_deductible_info(loc_file_df, 'WS_Ded_Type', ws_opts[i]["region"], ws_opts[i]["state"], ws_opts[i]["type"], f"Tier_{i+1}_WS")
                    add_deductible_info(loc_file_df, 'WS_Ded_Sub',  ws_opts[i]["region"], ws_opts[i]["state"], ws_opts[i]["sub"],  f"Tier_{i+1}_WS")
                if eq_include:
                    add_deductible_info(loc_file_df, 'EQ_Ded',      eq_opts[i]["region"], eq_opts[i]["state"], eq_opts[i]["amt"],  f"Tier_{i+1}_EQ")
                    add_deductible_info(loc_file_df, 'EQ_Ded_Perc', eq_opts[i]["region"], eq_opts[i]["state"], eq_opts[i]["perc"], f"Tier_{i+1}_EQ")
                    add_deductible_info(loc_file_df, 'EQ_Ded_Type', eq_opts[i]["region"], eq_opts[i]["state"], eq_opts[i]["type"], f"Tier_{i+1}_EQ")
                    add_deductible_info(loc_file_df, 'EQ_Ded_Sub',  eq_opts[i]["region"], eq_opts[i]["state"], eq_opts[i]["sub"],  f"Tier_{i+1}_EQ")
            
            if ws_include:
                apply_deductibles(loc_file_df, 'WS', 'TIV', 'WS_Ded', 'WS_Ded_Perc', 'WS_Ded_Type', 'Deductible')
                apply_sublimits(loc_file_df, 'WS', 'WS_Ded_Sub')
            if eq_include:
                apply_deductibles(loc_file_df, 'EQ', 'TIV', 'EQ_Ded', 'EQ_Ded_Perc', 'EQ_Ded_Type', 'Deductible')
                apply_sublimits(loc_file_df, 'EQ', 'EQ_Ded_Sub')

            us_ded_by_event = sum_final_loc_file(loc_file_df)
            us_ded_by_event = pl.from_pandas(us_ded_by_event)

            status.update()
            
            # ---------------------------------------------------
            # Simulate ELT

            elt = sql_loader.get_elt(accgrpid=hxd.policy_information.accgrpid, perspcode=elt_basis)
            elt = format_elt(elt, meanloss_threshold=10)

            eym = loader.load_feather("EYM.feather")
            yelt = elt.join(eym, on='EventID')
            yelt = simulate_losses(yelt, rng=rng, loss_threshold=500)
        
            yelt = filter_yelt(yelt, ws_include, eq_include, cal_eq_include, eventdata_eq)

            status.update()

            # ---------------------------------------------------
            # Apply deductibles, limits and calc AALs

            # Apply deductibles to loss data
            yelt = yelt.join(us_ded_by_event, on='EventID', how='left').fill_null(0)
            yelt = apply_per_occurrence_deductible(yelt, per_occ_ded)

            # Loss to layer
            yelt = loss_to_layer(yelt, excess, limit, per_occ_sublimits, elt_basis)

            # YLT
            us_ylt = create_ylt(yelt)

            # Calc metrics and write to hxd                
            us_aal_ws = calc_aal(us_ylt, "WS", sims)
            us_aal_eq = calc_aal(us_ylt, "EQ", sims)
            us_aal_all = us_aal_ws + us_aal_eq

            layer.simulated_result.us_wind_aal = us_aal_ws * exchange_rate
            layer.simulated_result.us_quake_aal = us_aal_eq * exchange_rate
            layer.simulated_result.us_all_perils_aal = us_aal_all * exchange_rate

            layer.simulated_result.us_wind_sd = calc_stddev(us_ylt, 'WS', us_aal_ws,  sims) * exchange_rate
            layer.simulated_result.us_quake_sd = calc_stddev(us_ylt, 'EQ', us_aal_eq,  sims) * exchange_rate
            layer.simulated_result.us_all_perils_sd = calc_stddev(us_ylt, None, us_aal_all, sims) * exchange_rate

            status.update()

            # ---------------------------------------------------
            # RDS
            rds_elt = sql_loader.get_rds_elt(accgrpid=hxd.policy_information.accgrpid, perspcode=layer.elt_for_sim)
            rds_elt = format_elt(rds_elt)
            rds_sim = rds_event_losses(rds_elt, us_ded_by_event, rng=rng)
            rds_sim = apply_per_occurrence_deductible(rds_sim, per_occ_ded)
            rds_sim = loss_to_layer(rds_sim, excess, limit, per_occ_sublimits, elt_basis)
            rds_events = pl.from_pandas(hx.params.rds_eventids)
            rds_events = rds_events.join(rds_sim, on='EventID', how='left').fill_null(0)
            rds_events = rds_events.select(['EventID', 'EventName', 'LayerLoss'])

            # Write to hxd
            rds_events = rds_events.to_pandas()
            for idx, row in rds_events.iterrows():
                setattr(layer.simulation_output.rds_events, row["EventName"], row["LayerLoss"] * exchange_rate)
            
            # ---------------------------------------------------
            # RI Cost by Gate
            # Merge Ceded Ratios by Event and multiply to AAL to get RI Cost
            ri_ceded = loader.load_feather('RI Ceded Ratios by Event.feather')        
            ri_cost = ri_cost_by_peril(yelt, ri_ceded, hxd.policy_information.team, sims)

            # Write to hxd
            layer.ri_cost.quake_us_ri_cost = ri_cost.get("EQ", 0)
            layer.ri_cost.wind_us_ri_cost = ri_cost.get("WS", 0)

            # ---------------------------------------------------
            # Marginal Impacts
            # Property + Treaty

            status.update()
            line = (layer.written_line_perc if layer.status in {'Bound', 'MTA', 'Cancellation'} else layer.quoted_line_perc) or 1

            # Read in Event_PT3 from feather file
            event_pt3 = loader.load_feather('Event_PT3.feather')
            
            # AFB share loss
            yelt = yelt.with_columns([(pl.col("LayerLoss") * line).alias("LimitLoss")])

            # Merge on account losses then add account loss to property+treaty loss
            event_pt3 = join_account_pt3_losses(event_pt3, yelt) # Note US only

            pt_comb_max = agg_losses(event_pt3, "Year", ["Loss", "CombLoss"], "max")
            pt_comb_sum = agg_losses(event_pt3, "Year", ["Loss", "CombLoss"], "sum")
        
            pt_oep_marg_impts_df = marginal_impacts(pt_comb_max, 'Loss', 'CombLoss', EP, sims)
            pt_aep_marg_impts_df = marginal_impacts(pt_comb_sum, 'Loss', 'CombLoss', EP, sims)
            
            aep_impact_1_in_10 = pt_aep_marg_impts_df.loc[pt_aep_marg_impts_df['EP'] == 10, 'MarginalImpact'].iloc[0]
            oep_impact_1_in_250 = pt_oep_marg_impts_df.loc[pt_oep_marg_impts_df['EP'] == 250, 'MarginalImpact'].iloc[0]

            # Write to hxd
            layer.simulated_result.aep_impact_1_in_10 = (aep_impact_1_in_10 / line) * exchange_rate
            layer.simulated_result.oep_impact_1_in_250 = (oep_impact_1_in_250 / line) * exchange_rate

            layer.simulated_result.aep_impact_1_in_10_wrt_line = aep_impact_1_in_10 * exchange_rate
            layer.simulated_result.oep_impact_1_in_250_wrt_line = oep_impact_1_in_250 * exchange_rate

            for idx, row in pt_oep_marg_impts_df.iterrows():
                setattr(layer.simulation_output.pt_oep_loss, f"one_in_{int(row['EP'])}", row['CombLoss'] * exchange_rate)

            for idx, row in pt_aep_marg_impts_df.iterrows():
                setattr(layer.simulation_output.pt_aep_loss, f"one_in_{int(row['EP'])}", row['CombLoss'] * exchange_rate)

            # Account OEP
            acc_oep = exceedence_prob_curves(yelt, 'Yr', 'LayerLoss', "max", EP, sims)
            acc_oep = acc_oep.to_pandas()
            for idx, row in acc_oep.iterrows():
                setattr(layer.simulation_output.acc_oep_gu_loss, f"one_in_{int(row['EP'])}", row["LayerLoss"] * exchange_rate)

        # Memory
        del eym, yelt, event_pt3, pt_max, pt_sum
        loader.clear_cache()
        gc.collect()


        
    # ---------------------------------------------------
    # International Locations
    # ---------------------------------------------------

    if has_intl:
        # Intl deductibles (not by layer)
        intl_df = prepare_intl_schedule(df)
        intl_ded = extract_intl_deductibles(hxd, exchange_rate)
        intl_ded = calculate_intl_deductibles(intl_df, intl_ded)
        intl_ded_by_event = intl_deductibles_by_event(loader, intl_ded)
                
        for index, layer in enumerate(hxd.layers):
            
            rng = np.random.RandomState(seed=4)
            elt_basis = layer.elt_for_sim
                    
            ws_include = layer.perils.named_windstorm.include
            eq_include = layer.perils.quake.include
            if not any([ws_include, eq_include]):
                status.skip_intl()
                continue
    
            limit = layer.limit / exchange_rate
            excess = layer.excess / exchange_rate            

            per_occ_ded = {
                "WS": (layer.perils.named_windstorm.per_occurrence_ded or 0) / exchange_rate,
                "EQ": (layer.perils.quake.per_occurrence_ded or 0) / exchange_rate
            }

            elt = sql_loader.get_elt(accgrpid=hxd.policy_information.accgrpid, perspcode=layer.elt_for_sim)
            elt = format_elt(elt, meanloss_threshold=10)
                    
            intl_ylt = []
            intl_aals = []
            for i in range(10):
                status.update()
                
                eym = loader.load_parquet(f"EYM_INTL_split_{int(i+1)}.parquet", cache_flag=False)
                yelt = elt.join(eym, on='EventID')
                yelt = simulate_losses(yelt, rng=rng, loss_threshold=500)
                yelt = filter_yelt(yelt, ws_include, eq_include, True)

                # Apply deductibles and limits
                yelt = yelt.join(intl_ded_by_event, on='EventID', how='left').fill_null(0)
                yelt = apply_per_occurrence_deductible(yelt, per_occ_ded)

                # Loss to layer
                yelt = loss_to_layer(yelt, excess, limit, per_occ_sublimits, elt_basis)
                yelt = yelt.filter(pl.col('LayerLoss') > 0)

                # Join on country and produce MI by country
                event_country_mapping = loader.load_feather("intl_event_country_mapping.feather")
                yelt = join_event_country_mapping(yelt, event_country_mapping)
                yelt = remove_non_rms_modelled_events(yelt)

                ylt = create_ylt(yelt)

                intl_ylt.append(ylt)
            
                country_aals = aals_by_country(yelt, sims)
                intl_aals.append(country_aals)

                del eym, yelt
                gc.collect()


            intl_ylt = pl.concat(intl_ylt, how='vertical')

            # Calc metrics and write to hxd
            intl_aal_ws = calc_aal(intl_ylt, "WS", sims)
            intl_aal_eq = calc_aal(intl_ylt, "EQ", sims)
            intl_aal_all = intl_aal_ws + intl_aal_eq

            # Write to hxd      
            layer.simulated_result.intl_wind_aal = intl_aal_ws * exchange_rate
            layer.simulated_result.intl_quake_aal = intl_aal_eq * exchange_rate
            layer.simulated_result.intl_all_perils_aal = intl_aal_all * exchange_rate

            layer.simulated_result.intl_wind_sd = calc_stddev(intl_ylt, 'WS', intl_aal_ws,  sims) * exchange_rate
            layer.simulated_result.intl_quake_sd = calc_stddev(intl_ylt, 'EQ', intl_aal_eq,  sims) * exchange_rate
            layer.simulated_result.intl_all_perils_sd = calc_stddev(intl_ylt, None, intl_aal_all, sims) * exchange_rate        

            # International AALs by country 
            intl_aals = pl.concat(intl_aals, how='vertical')
            intl_aals = prep_aals_for_hxd(intl_aals, exchange_rate) # converts fx
            layer.simulated_result_intl_country = intl_aals.to_pandas().to_dict("records") # write to hxd
       
        

    hxd.schedule.large_schedule_workflow.simulation_updated = True
    hxd.schedule.small_schedule_workflow.simulation_updated = True

    schedule_table_hxd_assignment_state_county(hxd, df, not hxd.policy_information.small_schedule_model)
    status.finish()




def extract_schedule_df(hxd, progress):
    """
    Return the orginal df for assignment back to the schedule table 
    and a dataframe summed by county for the simulation calculations. 
    Added country column for intl ded. 

    """
    if hxd.policy_information.large_schedule_model:
        # Large schedule: read file or EM database
        if hxd.schedule.large_schedule_workflow.load_from_schedule_file:
            src = hxd.schedule.large_schedule_workflow.schedule_file
        elif hxd.schedule.large_schedule_workflow.load_from_em_database:
            src = hxd.schedule.large_schedule_workflow.large_schedule_em_file
        else:
            hx.errors.fatal("Error: Please upload/import schedule file")

        with src.open("b") as f:
            df = pd.read_csv(f)

        # Ensure mandatory columns exist
        # for col in ("zip", "address_dropdown/country", "currency", "tiv_total"):
        #     df.setdefault(col, None)
        
        for col in ("zip", "address_dropdown/country", "currency", "tiv_total"):
            if col not in df.columns:
                df[col] = None

        # Standardise names
        df.rename(
            columns={
                "address_dropdown/country": "country",
                "tiv_total": "TIV"
            },
            inplace=True,
        )

        # Ensure consistent initial ordering
        df = df[["zip", "country", "currency", "TIV"]]

    else:
        # Small schedule: build from objects already in memory
        sched = hxd.schedule.schedule_table
        df = pd.DataFrame({
            "zip":     [row.zip for row in sched],
            "country": [row.address_dropdown.country for row in sched],
            "currency": [row.currency for row in sched],
            "TIV": [
                (row.tiv_buildings or 0)
                + (row.tiv_contents or 0)
                + (row.tiv_other or 0)
                + (row.tiv_bi or 0)
                for row in sched
            ]
        })

    df = clean_state_county(hxd, df)
    # convert location ccy to USD
    df = get_currency_exchange(hxd, pl.from_pandas(df), progress).to_pandas()
    df["TIV"] = (df["TIV"] / df["exchange_rate"]).round(2)

    df = df[["country", "county", "state", "TIV"]]
    df["loc_count"] = 1

    return df



def prepare_schedule(df):
    # Sum by county 
    df = df.groupby(['county', 'state'], as_index=False).sum()
    df = df.rename(columns={"county": "County", "state": "Statecode"})

    df['County'] = df['County'].astype("string").str.upper()
    df['Statecode'] = df['Statecode'].astype("string")
    df['StateCountyKey'] = df['Statecode'] + df['County']
    df = df[["Statecode", "County", "StateCountyKey", "TIV", "loc_count"]]

    return df


def prepare_intl_schedule(df):
    df_ws = df.loc[df['TIV'] > 0, ['country', 'TIV']].copy()
    df_ws['peril'] = 'WS'
    df_eq = df.loc[df['TIV'] > 0, ['country', 'TIV']].copy()
    df_eq['peril'] = 'EQ'

    df_out = pd.concat([df_ws, df_eq])
    
    df_out['country'] = df_out['country'].astype(str).str.lower()
    df_out = df_out[df_out["country"] != "united states"]
    return df_out



def produce_tier_list(ws_opts, eq_opts):
    tier_df = hx.params.tier_list_for_simulation
    tier_df['County'] = tier_df['County'].str.upper()
    tier_df['StateCountyKey'] = tier_df['Statecode'] + tier_df['County']

    # Set tiers based on input paramters for WS and EQ
    for i in range(3):
        map_tier_columns(tier_df, f"Tier_{i+1}_WS", ws_opts[i]["region"], ws_opts[i]["tier"], "ws")
        map_tier_columns(tier_df, f"Tier_{i+1}_EQ", eq_opts[i]["region"], eq_opts[i]["tier"], "eq")

    tier_df = tier_df[["StateCountyKey", "Tier_1_WS", "Tier_2_WS", "Tier_3_WS", "Tier_1_EQ", "Tier_2_EQ", "Tier_3_EQ"]]

    return tier_df


def assign_region(state_series):
    region_map = {
        "WA": "PNW", "OR": "PNW", "ID": "PNW",
        "AR": "NM", "IL": "NM", "IN": "NM", "KY": "NM", "MO": "NM", "MS": "NM", "TN": "NM",
        "VA": "VA"
    }
    return state_series.map(region_map).fillna(state_series)


def join_tiers_to_schedule(loc_df, tier_df):

    # Merge tier list to location file
    loc_df = loc_df.merge(tier_df, on='StateCountyKey', how='left')
    loc_df['Tier_1_WS'] = loc_df['Tier_1_WS'].fillna(0) * loc_df["loc_count"]
    loc_df['Tier_2_WS'] = loc_df['Tier_2_WS'].fillna(0) * loc_df["loc_count"]
    loc_df['Tier_3_WS'] = loc_df['Tier_3_WS'].fillna(0) * loc_df["loc_count"]
    loc_df['Tier_1_EQ'] = loc_df['Tier_1_EQ'].fillna(0) * loc_df["loc_count"]
    loc_df['Tier_2_EQ'] = loc_df['Tier_2_EQ'].fillna(0) * loc_df["loc_count"]
    loc_df['Tier_3_EQ'] = loc_df['Tier_3_EQ'].fillna(0) * loc_df["loc_count"]

    # Set region column
    loc_df['Region'] = assign_region(loc_df['Statecode'])

    return loc_df


def determine_toplocs_ws(loc_df):
    """ Determines the number of counties to take from event set for WS """

    region_sum = loc_df.groupby(['Region'], as_index=False).agg({'TIV': "sum"})
    county_count = len(list(set(loc_df['County'])))
    locs_count = sum(loc_df["loc_count"])
    region_count = len(region_sum)

    region_list = region_sum['Region'].tolist()

    if locs_count == 1:
        return 10
    elif region_count == 1 and ('FL' in region_list or 'SC' in region_list):
        return 2
    elif region_count == 1 and 'VA' in region_list:
        return 10
    elif region_count <= 2 and 'HI' in region_list:
        return 1
    elif county_count <= 3:
        return 4
    else:
        return 2


def determine_toplocs_eq(loc_df):
    """ Determines the number of counties to take from event set for EQ """

    region_sum = loc_df.groupby(['Region'], as_index=False).agg({'TIV': "sum"})
    county_count = len(list(set(loc_df['County'])))
    locs_count = sum(loc_df["loc_count"])
    region_count = len(region_sum)

    region_list = region_sum['Region'].tolist()

    if locs_count == 1:
        return 10
    elif region_count == 1 and 'NW' in region_list:
        return 5
    elif region_count == 1 and 'CA' in region_list and county_count <= 3:
        return 2
    elif region_count <= 2 and 'HI' in region_list:
        return 1
    elif region_count == 1 and 'CA' not in region_list:
        return 3
    elif county_count >= 6:
        return 1
    else:
        return 2


def us_ws_event_county_mapping(loader, toplocs_ws):
    eventdata_ws = loader.load_feather('00 Wind Eventid by County.feather')
    eventdata_ws = (
        eventdata_ws
        .sort(by=["EventID", "Perspvalue"], descending=[False, True])
        .groupby("EventID")
        .head(toplocs_ws)
    )
    return eventdata_ws


def us_eq_event_county_mapping(loader, toplocs_eq):
    eventdata_eq = loader.load_feather('00 Quake Eventid by County - Top 10.feather')
    eventdata_eq = (
        eventdata_eq
        .with_columns([
            pl.when(pl.col("Statecode").is_in(["WA", "OR", "ID"]))
            .then(3)
            .otherwise(toplocs_eq)
            .alias("toplocs_eq"),

            (-pl.col("Perspvalue"))
            .rank("dense")
            .over("EventID")
            .alias("idx")
        ])
        .filter(pl.col("idx") <= pl.col("toplocs_eq"))
        .drop(["toplocs_eq", "idx"])
    )
    return eventdata_eq


def sum_final_loc_file(df):
    df = df.copy()
    df.dropna(subset=["EventID"], inplace=True)

    df = df.groupby(['EventID'], as_index=False)[['Deductible', 'SubLimit', 'NoSubs']].sum()
    df['EventID'] = df['EventID'].astype('int64')

    df['SubLimit'] = np.where(
        df['SubLimit'] > 0,
        df['SubLimit'] / df['NoSubs'], 
        0
    )
    df = df[["EventID", "Deductible", "SubLimit"]]

    return df



def format_elt(df, meanloss_threshold=0.0001) -> pl.DataFrame:
    """ Takes polars elt and formats for simulation """
    
    # Derived columns
    df = (
        df
        .with_columns([
            (pl.col("MeanLoss") / pl.col("ExpVal")).alias("MDR"),
            (pl.col("StdevI") + pl.col("StDevC")).alias("Stdev"),
        ])
        .with_columns((pl.col("Stdev") / pl.col("MeanLoss")).alias("COV"))
        .with_columns(
            (((1 - pl.col("MDR")) / (pl.col("COV") ** 2)) - pl.col("MDR"))
            .alias("alpha_raw")
        )
        .with_columns(
            pl.when(pl.col("alpha_raw").is_finite())
              .then(pl.col("alpha_raw"))
              .otherwise(0)
              .alias("alpha")
        )
        .with_columns(
            (pl.col("alpha") * (1 - pl.col("MDR")) / pl.col("MDR")).alias("beta")
        )
    )

    # Case to numeric value
    df = df.with_columns([
        pl.col("EventID").cast(pl.Int64),
        pl.col("ExpVal").cast(pl.Float64),
        pl.col("MeanLoss").cast(pl.Float64),
        pl.col("alpha").cast(pl.Float64),
        pl.col("beta").cast(pl.Float64),
        pl.col("Stdev").cast(pl.Float64),
    ])
    
    # Final filter
    df = (
        df
        .filter(
            (pl.col("ExpVal") > 0) &
            (pl.col("MeanLoss") > meanloss_threshold) &
            (pl.col("alpha") > 0) &
            (pl.col("beta") > 0) &
            (pl.col("Stdev") > 0)
        )
        .drop("alpha_raw")   # tidy up
    )

    df = df.select(["EventID", "Peril", "alpha", "beta", "ExpVal"])

    return df



def filter_yelt(df, ws_include: bool, eq_include: bool,cal_eq_include: bool, eventdata_eq = pl.DataFrame) -> pl.DataFrame:
    """ Takes polars yelt and filters for coverage included / excluded """
    
    # Peril filters
    if not ws_include:
        df = df.filter(pl.col("Peril") != "WS")
    if not eq_include:
        df = df.filter(pl.col("Peril") != "EQ")

    # Drop California EQ rows
    if eq_include and (not cal_eq_include):
        event_no_ca = (
            eventdata_eq
            .sort("Perspvalue", descending=True)           # biggest Perspvalue first
            .groupby("EventID")
            .agg(pl.col("Statecode").first())              # keep top row per group
        )

        df = (
            df
            .join(event_no_ca, on="EventID", how="left")
            .with_columns(pl.col("Statecode").fill_null("UN"))
            .filter(pl.col("Statecode") != "CA")
            .drop("Statecode")
        )

    return df


def simulate_losses(df: pl.DataFrame, rng: np.random.RandomState, loss_threshold = 0.01) -> pl.DataFrame:
    """ Simulate event losses for polars dataframe. Returns a polars DataFrame. """

    # RunNumPy simulation
    alpha = df["alpha"].to_numpy()
    beta = df["beta"].to_numpy()
    exp_val = df["ExpVal"].to_numpy()

    simulated_loss = rng.beta(alpha, beta) * exp_val

    # Attach simulated loss back to Polars df
    df_out = (
        df.with_columns(pl.Series("Loss", simulated_loss))
        .filter(pl.col("Loss") >= loss_threshold)
        .drop(['alpha', 'beta', 'ExpVal'])
    )

    return df_out



def rds_event_losses(elt, ded_df, rng):
    
    rds_events = pl.from_pandas(hx.params.rds_eventids)

    # Merge on loss data if event is in account
    rds_sim = rds_events.join(elt, on='EventID', how='left')

    # Simulate losses
    rds_sim = simulate_losses(rds_sim, rng=rng)
    rds_sim = rds_sim.join(ded_df, on='EventID', how='left').fill_null(0)

    return rds_sim



def ri_cost_by_peril(yelt, ri_ceded, team, sims):

    ri_col = "ES" if team == "NACP" else "OM"
    
    ri_cost = (
        yelt
        .filter(pl.col("LayerLoss") > 0)
        .join(
            ri_ceded.select(["EventID", ri_col]),
            on="EventID",
            how="inner"
        )
        .with_columns([
            ((pl.col("LayerLoss") * pl.col(ri_col)) / sims).alias("RICost")
        ])
        .groupby("Peril")
        .agg(pl.col("RICost").sum())
    )
    
    ri_cost_dict = ri_cost.to_pandas().set_index('Peril').to_dict()['RICost']

    return ri_cost_dict


def join_account_pt3_losses(event_pt3, yelt):
    '''Merge account property+treaty losses onto YELT''' 

    if 'Yr' in yelt.columns:
        yelt = yelt.rename({'Yr': 'Year'})

    event_pt3 = (
        event_pt3.join(
            yelt.select(['Year', 'EventID', 'LimitLoss']),
            on=['Year', 'EventID'],
            how='left'
        )
        .fill_null(0)
        .with_columns([(pl.col("Loss") + pl.col("LimitLoss")).alias("CombLoss")])
    )
    return event_pt3


def extract_intl_deductibles(hxd, fx):
    
    peril_map = {
        "quake": "EQ",
        "named_windstorm": "WS"
    }

    ded_collect = []
    for peril in peril_map.keys():
        ded_df = pd_df_from_hx_list(getattr(hxd.non_layer_perils, peril).intl_ded)
        ded_df["peril"] = peril_map[peril] 
        ded_collect.append(ded_df)
    
    df = pd.concat(ded_collect).fillna(0)
    df = df[df["country"] != ""]
    df['country'] = df['country'].astype(str).str.lower()    

    # Convert ccy
    df['fixed_min'] = df['fixed_min'] / fx
    df['fixed_max'] = df['fixed_max'] / fx
    df['country_sublimit'] = df['country_sublimit'] / fx

    return df[['country', 'peril', 'perc_of_tiv', 'fixed_min', 'fixed_max', 'country_sublimit']]



def calculate_intl_deductibles(sch_df, intl_ded_df):

    df = sch_df.merge(intl_ded_df, on=['country', 'peril'], how='left').fillna(0)
    df['fixed_max_adj'] = np.where(df['fixed_max'] == 0, np.inf, df['fixed_max'])

    df['comb_deductible'] = np.maximum(
        np.minimum(df['TIV'] * df['perc_of_tiv'], df['fixed_max_adj']),
        df['fixed_min']
    )
    df['Deductible'] = np.minimum(df['comb_deductible'], df['TIV'])
    df['SubLimit'] = np.minimum(df['country_sublimit'], df['TIV'])
    df['loc_count'] = 1

    df = df.groupby(['country', 'peril'], as_index=False)[['TIV', 'loc_count', 'Deductible', 'SubLimit']].sum()
   
    return df


def join_event_country_mapping(yelt, event_country_mapping):
    yelt = yelt.join(event_country_mapping.drop("peril"), on='EventID', how='left')

    yelt = yelt.with_columns([
        pl.col('country').fill_null('United States').alias('country')
    ])

    return yelt


def remove_non_rms_modelled_events(yelt: pl.DataFrame):
    """Removes event IDs which aren't officially modelled by RMS to avoid double count with rating table method"""

    rms_pl = pl.DataFrame(hx.params.intl_cat_model_coverage)
    rms_pl = rms_pl.melt(id_vars=["Country"], value_vars=["WS", "EQ"], variable_name="Peril", value_name="modelled_flag")
    rms_pl = rms_pl.with_columns([
        pl.when(pl.col("Country") == 'United States')
        .then(1)
        .otherwise(pl.col('modelled_flag'))
        .alias("modelled_flag")
    ]).rename({'Country': 'country'})
    
    yelt = yelt.join(rms_pl, on=['country', 'Peril'], how='left')
    yelt = yelt.filter(pl.col('modelled_flag') > 0).drop('modelled_flag')
    return yelt



def create_ylt(yelt):
    ylt = (
        yelt.filter(pl.col('LayerLoss') > 0)
        .groupby(["Yr", "Peril"])
        .agg(pl.col("LayerLoss").sum())
    )
    return ylt



def aals_by_country(yelt, sims):
    
    df = yelt.groupby(['country','Peril']).agg([
        (pl.col('LayerLoss').sum() / sims).alias('aal')
    ])

    df = df.filter(pl.col('aal') > 50)

    return df
    


def prep_aals_for_hxd(df, fx):
    df =  df.groupby(['country', 'Peril']).agg(pl.col('aal').sum())

    peril_map = {"WS": "aal_ws", "EQ": "aal_eq"}    

    df = df.with_columns([
        pl.col("Peril").map_dict(peril_map).alias("peril_mapped"),
        (pl.col("aal") * fx).alias('aal')
    ])

    df = df.pivot(
        values="aal",
        index="country",
        columns="peril_mapped",
    ).fill_null(0).sort(pl.col("country"))

    return df



def intl_deductibles_by_event(loader, intl_ded: pd.DataFrame) -> pd.DataFrame:
    
    intl_ded_pl = pl.from_pandas(intl_ded)
    
    # Import event country mapping
    event_country_mapping = loader.load_feather("intl_event_country_mapping.feather")
    event_country_mapping = conv_col_lowercase(event_country_mapping, "country")
    
    intl_ded_by_event = event_country_mapping.join(intl_ded_pl, on=['country', 'peril'], how='left').fill_null(0)
    intl_ded_by_event = intl_ded_by_event.select(["EventID", "Deductible", "SubLimit"])
    
    return intl_ded_by_event

