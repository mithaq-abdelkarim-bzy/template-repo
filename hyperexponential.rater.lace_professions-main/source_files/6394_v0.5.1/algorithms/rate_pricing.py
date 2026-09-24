# v0.5.0
import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms.rate_utilities import ratio, policy_term, write_pd_to_hxd
from algorithms.rate_constants import (retention_split_notes,get_territory_groups,get_fx_rate,get_fx_rate_base,get_base_params,get_tech_params,get_nmp_load,get_inflation_tables,
                                        get_quotes_params,get_quotes_params_addl, get_credibility_params,units_to_convert,attritional_cap,
                                        layer_order,policy_structure_to_dataframe,policy_addl_structure_to_dataframe,retention_to_dataframe,territory_to_dataframe,
                                        client_details_lawyers_to_dataframe,client_details_aec_to_dataframe, hover_info, policy_notes
                                        )
from algorithms.year_frac import diffdays
from algorithms import parameter_tables_schema as params
from operator import itemgetter
from dataclasses import dataclass
from datetime import date
from collections import defaultdict
from scipy.stats import norm
from algorithms.rate_simulation_inputs import get_model_params

def read_inception_expiry_date(hxd):
    hxd.cds.standard_fields.inception_date = hxd.hx_core.inception_date
    hxd.cds.standard_fields.expiry_date = hxd.hx_core.expiry_date

def tower_excess_calc(hxd):
    eec_running_total = 0
    agg_running_total = 0
    for idx, layer in enumerate(hxd.cds.layers):
        layer.excess_eec = eec_running_total
        layer.excess_agg = agg_running_total
        eec_running_total = (layer.limit_eec or 0) + layer.excess_eec
        agg_running_total = (layer.limit_agg or 0) + layer.excess_agg


def get_simulation_inputs(hxd):
    profession = "lpl" if hxd.cds.profession == "Lawyers" else "aec"
    df_quote_params = get_quotes_params(hxd)
    df_ded_params = get_ded_params(hxd)
    df_ModelParamsFinal, df_ModelParamsUnadjustedFinal = get_model_params(hxd, profession)

def layer_names(hxd):
    names = ["Primary", "1XS","2XS","3XS","4XS","5XS","6XS", "7XS", "8XS", "9XS", "10XS"]
    for idx, layer in enumerate(hxd.cds.layers):
        if idx > len(names):
            layer.name =f'Additional {idx - len(names)}'
        else:
            layer.name = names[idx]

def layer_addl_names(hxd):
    names = ["Addl 1", "Addl 2", "Addl 3", "Addl 4", "Addl 5"]
    for idx, layer in enumerate(hxd.cds.layers_addl):
        if idx > len(names):
            layer.name=f'Additional {idx - len(names)}'
        else:
            layer.name=names[idx]


def claims_recoveries_dropdown_calc(hxd, layers, bool_is_addl: bool) -> pd.DataFrame:
    """
    This calculation is based on the Claim Dropdown Calc in the Excel LACE Rater
    layers is either hxd.cds.layers or hxd.cds.layers_addl
    Claims are processed in policy_year_estimated order so the aggregate limits
    erode within each policy year; all working arrays stay keyed by the claim's
    original node index, so the returned frame aligns with the claims list as before.
    returns year | layer | recovery
    """
    fx_rate = (get_fx_rate(hxd.cds.currencies.source_currency) or 1)
    claims_path = hxd.cds.experience_rating.claims
    claims = list(claims_path)
    # Snapshot the fields we need once instead of re-reading the nodes per layer
    claim_info = [
        (c.policy_year_estimated, c.total_usd_inflated, c.RDC_True.final_total_incurred)
        for c in claims
    ]
    # Policy-year ordering: sort claim node *indices* by policy_year_estimated,
    # then chronologically within the year by claim_made_date
    # (yearless/dateless claims last, original row order as a stable tie-break)
    order = sorted(
        range(len(claims)),
        key=lambda i: (claims[i].policy_year_estimated is None,
                       claims[i].policy_year_estimated or 0,
                       claims[i].claim_made_date is None,
                       claims[i].claim_made_date or date.min,
                       i),
    )
    # Tower
    result = {}
    rec_across_tower_sum = defaultdict(int)  # recoveries up to and including the prior claim (keyed by original claim index)
    retention_rdc_yes_no = hxd.cds.retention_split[0].defence_cost_bool
    for layer in layers:
        if not layer.include:
            continue
        is_rtc_bool = bool(layer.rtc or layer.rtc_agg)
        layer_name = layer.name
        # Addl layer specific
        if bool_is_addl:
            primary_eec_limit = (layer.excess_eec or 0) / fx_rate
            agg_lim = (layer.excess_eec or 0) / fx_rate if is_rtc_bool else (layer.excess_agg or 0) / fx_rate
            primary_agg_limit = np.inf if not agg_lim else agg_lim
        layer_eec_limit = (layer.limit_eec or 0) / fx_rate
        agg_lim = (layer.limit_eec or 0) / fx_rate if is_rtc_bool else (layer.limit_agg or 0) / fx_rate
        layer_agg_limit = np.inf if not agg_lim else agg_lim   # adjust for fx_rate here
        # working arrays  (reset per layer — carry-over between layers was a bug)
        layer_rec_arr = defaultdict(int)                 # automatically zero
        prev_policy_year = None
        prev_recovery = 0
        prev_recovery_primary = 0
        recovery = 0
        recovery_primary = 0
        # Running recovery totals keyed by policy_year_estimated. Appending a row
        # to df_running_total_recovery and then grouping by policy year and summing
        # is exactly a running sum, so accumulate it directly.
        run_tot_rec = defaultdict(float)
        run_tot_rec_primary = defaultdict(float)         # Addl layer specific
        for idx in order:                    # policy-year pass; idx stays the original node index
            policy_year, final_total_incurred, rdc_final_total_incurred = claim_info[idx]   # pri = post retention incurred
            pri = rdc_final_total_incurred if retention_rdc_yes_no == "Yes" else final_total_incurred
            if policy_year is not None and pri is not None:
                same_year_as_prev = (prev_policy_year is not None
                                     and policy_year == prev_policy_year)
                if bool_is_addl:
                    # Update the working totals
                    if same_year_as_prev:
                        run_tot_rec_primary[policy_year] += prev_recovery_primary
                        run_tot_rec[policy_year] += prev_recovery
                    # calculate recovery
                    recovery_primary = min(
                        pri,
                        primary_eec_limit,
                        primary_agg_limit - run_tot_rec.get(policy_year, 0) * 0 - run_tot_rec_primary.get(policy_year, 0),
                    )
                    recovery = min(
                        pri - recovery_primary,
                        layer_eec_limit,
                        layer_agg_limit - run_tot_rec.get(policy_year, 0),
                    )
                else:
                    # Update the working totals
                    if same_year_as_prev:
                        run_tot_rec[policy_year] += prev_recovery
                    # calculate recovery
                    recovery = min(
                        pri - rec_across_tower_sum.get(idx, 0),
                        layer_eec_limit,
                        layer_agg_limit - run_tot_rec.get(policy_year, 0),
                    )
                    rec_across_tower_sum[idx] += recovery
            else:
                recovery = 0
                recovery_primary = 0
            layer_rec_arr[idx] = recovery
            prev_policy_year = policy_year
            prev_recovery = recovery
            prev_recovery_primary = recovery_primary
        result[layer_name] = layer_rec_arr
    df = pd.DataFrame(result)
    # Keys were inserted in policy-year order; restore original claim/node order so
    # the rows line up with claims_path before attaching the year column
    df = df.sort_index()
    # Add the year column
    df["year"] = [py for py, _, _ in claim_info]
    # Convert to flat file format
    flat = df.melt(
        id_vars="year",
        var_name="layer",
        value_name="recovery"
    )
    return flat[flat["year"].notna()]

def claims_recoveries_calc(hxd, layers) -> pd.DataFrame:
    """
    Claims recoveries calculations for each layer
    returns year | layer | recovery
    """
    fx_rate = (get_fx_rate(hxd.cds.currencies.source_currency) or 1)   
    claims_path = hxd.cds.experience_rating.claims
    result = {}
    for index, layer in enumerate(layers):
        if layer.include:
            # Get layer limits
            layer_name = layer.name
            layer_eec_limit = (layer.limit_eec or 0) / fx_rate
            layer_eec_xs = (layer.excess_eec or 0) / fx_rate

            # working arrays
            layer_rec_arr = defaultdict(int)   #automatically zero
            for idx, claim in enumerate(claims_path):
                # Post retention incurred
                loss = claim.total_usd_inflated  # always picks Retention not applied on Defence Cost

                if claim.policy_year_estimated is not None:
                    # calculate recovery
                    recovery = min(layer_eec_limit, max(loss - layer_eec_xs, 0))
                else:
                    recovery = 0

                layer_rec_arr[idx] = recovery

            result[layer_name] = layer_rec_arr

    df = pd.DataFrame(result)
    # Add the year column
    df["year"] = [claim.policy_year_estimated for claim in claims_path]
    # Convert to flat file format
    flat = df.melt(
        id_vars="year",
        var_name="layer",
        value_name="recovery"
    )
    return flat[flat["year"].notna()]

def claims_recoveries_att_layer(hxd) -> pd.DataFrame:
    """
    Claims recoveries calculations for Attritional Layer
    returns year | layer | recovery
    """
    layer_name = "att_layer"
    limit = attritional_cap
    claims_path = hxd.cds.experience_rating.claims
    
    result = {}
    layer_rec_arr = defaultdict(int)
    for idx, claim in enumerate(claims_path):
        # Developed Attritional Layer
        loss = claim.total_usd_inflated
        if claim.policy_year_estimated is not None:
            recovery = min(max(loss, 0), limit)
        else:
            recovery = 0       
        layer_rec_arr[idx] = recovery
    result[layer_name] = layer_rec_arr      

    df = pd.DataFrame(result)
    # Add the year column
    df["year"] = [claim.policy_year_estimated for claim in claims_path]

    # Convert to flat file format
    flat = df.melt(
        id_vars="year",
        var_name="layer",
        value_name="recovery"
    )
    return flat[flat["year"].notna()]


def get_agg_limits(layers) -> pd.DataFrame:
    # Get Aggregate Limits
    rows = []
    rows.append({
        "layer": "att_layer",
        "agg_lim": 0
    })

    for index, layer in enumerate(layers):
        # Get layer limits
        layer_name = layer.name
        layer_agg_limit = np.inf if layer.limit_agg == 0 else layer.limit_agg

        if layer.include:
            rows.append({
                "layer": layer_name,
                "agg_lim": layer_agg_limit
            })

    return pd.DataFrame(rows)

def get_eec_excess(layers) -> pd.DataFrame:
    # Get Aggregate Limits
    rows = []
    rows.append({
                "layer": "att_layer",
                "eec_excess": 0
            })
    for index, layer in enumerate(layers):
        # Get layer limits
        layer_name = layer.name
        layer_eec_excess = layer.excess_eec

        if layer.include:
            rows.append({
                "layer": layer_name,
                "eec_excess": layer_eec_excess
            })

    return pd.DataFrame(rows)

def get_eec_limit(layers) -> pd.DataFrame:
    rows = []
    for index, layer in enumerate(layers):
        if layer.include:
            rows.append({
                "layer": layer.name,
                "eec_limit": layer.limit_eec,
                "brokerage": layer.brokerage
            })
    return pd.DataFrame(rows)

def get_dev_pattern(hxd) -> pd.DataFrame:
    '''
    Return development patterns for Incurred and Claims by Policy year
    year | dev_factor
    '''
    df_claims_dev = hx.params.ref_tbl_claims_development
    lookup_col = "Lawyers Claims Development" if hxd.cds.profession_lawyers_bool else "A&E Claims Development"
    claims_asatdate = hxd.cds.experience_rating.claims_asatdate
    incept_date = hxd.hx_core.inception_date
    incept_year = incept_date.year
    years = range(16)
    
    rows = []
    for year in years:
        actual_year = incept_year - year
        if claims_asatdate is None:
            claim_dev_month = 3
        else:
            claim_dev_month = 3 if claims_asatdate.year < actual_year else 12 + (claims_asatdate.year - actual_year) * 12
        
        count_dev_month = claim_dev_month + 6
        df_claims_dev_filtered = df_claims_dev[df_claims_dev["Development Month"] == claim_dev_month]
        df_count_dev_filtered = df_claims_dev[df_claims_dev["Development Month"] == count_dev_month]

        if df_claims_dev_filtered is None or len(df_claims_dev_filtered) == 0:
            incurred_dev_factor = 0
        else:
            incurred_dev_factor = df_claims_dev_filtered[lookup_col].iloc[0]

        if df_count_dev_filtered is None or len(df_count_dev_filtered) == 0:
            claims_dev_factor = 0
        else:
            claims_dev_factor = df_count_dev_filtered[lookup_col].iloc[0]

        rows.append({
            "year": actual_year,
            "incurred_dev_factor": incurred_dev_factor,
            "claims_dev_factor": claims_dev_factor
        })

    return pd.DataFrame(rows)

def get_actual_years(hxd) -> pd.DataFrame:
    incept_date = hxd.hx_core.inception_date
    incept_year = incept_date.year
    years = range(21)
    actual_years = {"year_2": [incept_year - y for y in years]}
    df_actual_years = pd.DataFrame(actual_years)
    return df_actual_years

def get_onlevelled_rev(hxd) -> pd.DataFrame:
    incept_date = hxd.hx_core.inception_date
    incept_year = incept_date.year
    years = range(21)
    rows=[]
    for year in years:
        value = (getattr(getattr(hxd.cds.experience_rating.claims_summary,f"year_{year}"),"revalued_notional_revenue_weighted") or 0)
        rows.append({
            "year": incept_year - year,
            "revalued_notional_revenue_weighted": value
        })
    return pd.DataFrame(rows)

def is_cape_cod_pricing_method(hxd) -> bool:
    # df_method = hx.params.ref_list_experience_method
    # dev_pattern = get_dev_pattern(hxd)
    return True

def develop_claims(hxd):
    claims_policy_year = hxd.cds.experience_rating.claims_policy_year or 0
    incept_year = hxd.hx_core.inception_date.year
    utc = units_to_convert(hxd)
    #utc = 1
    is_cape_cod = is_cape_cod_pricing_method(hxd)
    # needs the names to be labelled
    layer_names(hxd)
    layer_addl_names(hxd)

    # Recoveries from standard calc and claims dropdown calc
    df_layers_att_layer = claims_recoveries_att_layer(hxd)
    df_layers_rec = claims_recoveries_calc(hxd, hxd.cds.layers)
    df_layers_rec_addl = claims_recoveries_calc(hxd, hxd.cds.layers_addl)   
    df_layers_rec = pd.concat([df_layers_att_layer, df_layers_rec, df_layers_rec_addl], ignore_index=True)

    df_layers_rec_dropdown = claims_recoveries_dropdown_calc(hxd, hxd.cds.layers, False)
    df_layers_rec_addl_dropdown = claims_recoveries_dropdown_calc(hxd, hxd.cds.layers_addl, True) 
    df_layers_rec_dropdown = pd.concat([df_layers_rec_dropdown, df_layers_rec_addl_dropdown], ignore_index=True)

    # Filter for claims_policy_year here
    df_layers_rec = df_layers_rec[df_layers_rec["year"] >= claims_policy_year]
    df_layers_rec_dropdown = df_layers_rec_dropdown[df_layers_rec_dropdown["year"] >= claims_policy_year]

    # get number of experience years here for later
    #num_years_experience = df_layers_rec["year"].nunique()
    num_years_experience = incept_year - (claims_policy_year or 0)  # + 1    exclude incept year

    # For the purpose of future calcs have all necesary years present in df_layers_rec and df_layer_rec_dropdown 
    df_years = get_actual_years(hxd)
    full_grid = (
    df_years["year_2"]
    .drop_duplicates()
    .to_frame(name="year")
    .assign(key=1)
    .merge(
        df_layers_rec[["layer"]].drop_duplicates().assign(key=1),
        on="key"
    )
    .drop(columns="key")
    )

    # Step 3: join df_layers_rec onto the full grid
    df_layers_rec = (
        full_grid
        .merge(df_layers_rec, on=["year", "layer"], how="left")
        .fillna(0)
    )

    # Step 4: same for dropdown
    df_layers_rec_dropdown = (
        full_grid
        .merge(df_layers_rec_dropdown, on=["year", "layer"], how="left")
        .fillna(0)
    )

    # get aggregate Limits
    df_agg_lim = get_agg_limits(hxd.cds.layers)
    df_agg_lim_addl = get_agg_limits(hxd.cds.layers_addl)
    df_agg_lim = pd.concat([df_agg_lim, df_agg_lim_addl], ignore_index=True)

    #get excess layers
    df_layers_xs = get_eec_excess(hxd.cds.layers)
    df_layers_xs_addl = get_eec_excess(hxd.cds.layers_addl)
    df_layers_xs = pd.concat([df_layers_xs, df_layers_xs_addl], ignore_index=True)

    # Uncapped Trended Claims (After Maintenance Retention only)
    df_uncapped_trended_claims = (df_layers_rec.groupby(["year", "layer"], as_index=False).agg({"recovery": "sum"}))

    # get development percentages
    df_dev_factors = get_dev_pattern(hxd)

    # Uncapped Trended Capped Claims for Aggregate Limits
    df_capped = df_uncapped_trended_claims.merge(df_agg_lim, on="layer", how="left")
    df_capped["recovery_capped"] = np.where(df_capped["agg_lim"]==0, df_capped["recovery"], df_capped[["recovery", "agg_lim"]].min(axis=1))
    df_capped = df_capped.merge(df_dev_factors, on="year", how="left")

    # Developed (BF) Claims for Aggregate Limits - this uses claims dropdown calc
    # - first group the dropdown calcs
    df_layers_rec_dropdown_grouped = df_layers_rec_dropdown.groupby(["year", "layer"], as_index=False).agg({"recovery": "sum"})

    decay_factor = 0.98
    cutoff_10yr = incept_year - 11
    cutoff_15yr = incept_year - 16
    cutoff_20yr = incept_year - 21
    df_onlevelled_rev = get_onlevelled_rev(hxd)
    df_actual_years = get_actual_years(hxd)                             # returns column year_2

    # need to deal with attritional layer separately 
    df_exp_bc_att = df_uncapped_trended_claims[df_uncapped_trended_claims["layer"]=="att_layer"]
    df_exp_bc_att = df_exp_bc_att.merge(df_dev_factors, on="year", how="left")
    df_exp_bc_att = df_exp_bc_att.merge(df_onlevelled_rev, on="year", how="left")  
    df_exp_bc_att_15yr = df_exp_bc_att[(df_exp_bc_att["year"] > cutoff_15yr) & (df_exp_bc_att["year"] != incept_year)]
    df_exp_bc_att_15yr = df_exp_bc_att_15yr.merge(df_actual_years, how="cross")
    df_exp_bc_att_15yr["cape_cod_factor"] = decay_factor ** abs(df_exp_bc_att_15yr["year"] - df_exp_bc_att_15yr["year_2"])
    df_exp_bc_att_15yr["top_ebc"] = df_exp_bc_att_15yr["cape_cod_factor"] * df_exp_bc_att_15yr["recovery"]   
    df_exp_bc_att_15yr["bottom_ebc"] = df_exp_bc_att_15yr["cape_cod_factor"] * df_exp_bc_att_15yr["revalued_notional_revenue_weighted"] * df_exp_bc_att_15yr["incurred_dev_factor"]
    df_exp_bc_att_15yr = df_exp_bc_att_15yr.groupby(["layer","year_2"], as_index=False).agg(
        top_ebc=("top_ebc", "sum"),
        bottom_ebc=("bottom_ebc", "sum")
    )
    df_exp_bc_att_15yr["ExpectedBC"] = ratio(df_exp_bc_att_15yr["top_ebc"], df_exp_bc_att_15yr["bottom_ebc"] / utc)
    df_exp_bc_att_15yr.rename(
        columns={"year_2":"year"},
        inplace=True
    )  

    df_att_bf_1 = df_exp_bc_att_15yr.merge(df_dev_factors, on="year", how="left")
    df_att_bf_1 = df_att_bf_1.merge(df_onlevelled_rev, on="year", how="left")
    df_att_bf_1 = df_att_bf_1.merge(df_layers_att_layer, on="year", how="left")
    df_att_bf_1["recovery"] = df_att_bf_1["recovery"].fillna(0)
    df_att_bf_1["bf_prep"] = np.where(df_att_bf_1["incurred_dev_factor"] > 0.7, ratio(df_att_bf_1["recovery"], df_att_bf_1["incurred_dev_factor"]), 
                df_att_bf_1["recovery"] + (1 - df_att_bf_1["incurred_dev_factor"]) * df_att_bf_1["revalued_notional_revenue_weighted"] * df_att_bf_1["ExpectedBC"] / utc)
    df_att_bf_1["bf"] = df_att_bf_1["bf_prep"] #does not ned the agg lim if statement as agg lim always zero

    df_dev_bf = df_layers_rec_dropdown_grouped.merge(df_dev_factors, on="year", how="left")
    df_dev_bf = df_dev_bf.merge(df_agg_lim, on="layer", how="left")

    # Expected BC per unit of exposure - 10 years
    # requires
    #   Onlevelled Revenue - get onleveled Revenue and merge in
    #   Incurred DF Pattern - already included above
    #   Cape Cod Dev Factors - cross product years and calculate
    df_exp_bc_10 = df_dev_bf.copy()
    df_exp_bc_10 = df_exp_bc_10[(df_exp_bc_10["year"] > cutoff_10yr) & (df_exp_bc_10["year"] != incept_year)]
    df_exp_bc_10 = df_exp_bc_10.merge(df_onlevelled_rev, on="year", how="left")

    df_exp_bc_10 = df_exp_bc_10.merge(df_actual_years, how="cross")
    df_exp_bc_10["cape_cod_factor"] = decay_factor ** abs(df_exp_bc_10["year"] - df_exp_bc_10["year_2"])
    df_exp_bc_10["top_ebc"] = df_exp_bc_10["cape_cod_factor"] * df_exp_bc_10["recovery"]   
    df_exp_bc_10["bottom_ebc"] = df_exp_bc_10["cape_cod_factor"] * df_exp_bc_10["revalued_notional_revenue_weighted"] * df_exp_bc_10["incurred_dev_factor"]
    df_exp_bc_10 = df_exp_bc_10.groupby(["layer","year_2"], as_index=False).agg(
        top_ebc=("top_ebc", "sum"),
        bottom_ebc=("bottom_ebc", "sum")
    )
    df_exp_bc_10["ExpectedBC"] = ratio(df_exp_bc_10["top_ebc"], df_exp_bc_10["bottom_ebc"] / utc)
    df_exp_bc_10.rename(
        columns={"year_2":"year"},
        inplace=True
    )

    # Expected BC per unit of exposure - 15 years
    # requires
    #   Onlevelled Revenue - get onleveled Revenue and merge in
    #   Incurred DF Pattern - already included above
    #   Cape Cod Dev Factors - cross product years and calculate
    df_exp_bc_15 = df_dev_bf.copy()
    df_exp_bc_15 = df_exp_bc_15[(df_exp_bc_15["year"] > cutoff_15yr) & (df_exp_bc_15["year"] != incept_year)]
    df_exp_bc_15 = df_exp_bc_15.merge(df_onlevelled_rev, on="year", how="left")
    
    df_exp_bc_15 = df_exp_bc_15.merge(df_actual_years, how="cross")
    df_exp_bc_15["cape_cod_factor"] = decay_factor ** abs(df_exp_bc_15["year"] - df_exp_bc_15["year_2"])
    df_exp_bc_15["top_ebc"] = df_exp_bc_15["cape_cod_factor"] * df_exp_bc_15["recovery"] 
    df_exp_bc_15["bottom_ebc"] = df_exp_bc_15["cape_cod_factor"] * df_exp_bc_15["revalued_notional_revenue_weighted"] * df_exp_bc_15["incurred_dev_factor"]
    df_exp_bc_15 = df_exp_bc_15.groupby(["layer","year_2"], as_index=False).agg(
        top_ebc=("top_ebc", "sum"),
        bottom_ebc=("bottom_ebc", "sum")
    )
    df_exp_bc_15["ExpectedBC"] = ratio(df_exp_bc_15["top_ebc"], df_exp_bc_15["bottom_ebc"] / utc)
    df_exp_bc_15.rename(
        columns={"year_2":"year"},
        inplace=True
    )

    # Expected BC per unit of exposure - 20 years
    # requires
    #   Onlevelled Revenue - get onleveled Revenue and merge in
    #   Incurred DF Pattern - already included above
    #   Cape Cod Dev Factors - cross product years and calculate
    df_exp_bc_20 = df_dev_bf.copy()
    df_exp_bc_20 = df_exp_bc_20[(df_exp_bc_20["year"] > cutoff_20yr) & (df_exp_bc_20["year"] != incept_year)]
    df_exp_bc_20 = df_exp_bc_20.merge(df_onlevelled_rev, on="year", how="left")
    
    df_exp_bc_20 = df_exp_bc_20.merge(df_actual_years, how="cross")
    df_exp_bc_20["cape_cod_factor"] = decay_factor ** abs(df_exp_bc_20["year"] - df_exp_bc_20["year_2"])
    
    # for gcc rebased calc
    # print(df_exp_bc_20.to_string())
    df_cape_cod_factor = df_exp_bc_20[df_exp_bc_20["year_2"] == incept_year - 1]
    df_cape_cod_factor = (df_cape_cod_factor[
                                [  
                                    "cape_cod_factor", 
                                    "incurred_dev_factor", 
                                    "revalued_notional_revenue_weighted", 
                                    "year"
                                ]
                            ]
                            .groupby(
                                [
                                    "cape_cod_factor", 
                                    "incurred_dev_factor", 
                                    "revalued_notional_revenue_weighted", 
                                    "year"                                    
                                ],
                                as_index=False
                            )
                            .size()
                        )


    df_exp_bc_20["top_ebc"] = df_exp_bc_20["cape_cod_factor"] * df_exp_bc_20["recovery"] 
    df_exp_bc_20["bottom_ebc"] = df_exp_bc_20["cape_cod_factor"] * df_exp_bc_20["revalued_notional_revenue_weighted"] * df_exp_bc_20["incurred_dev_factor"]
    df_exp_bc_20 = df_exp_bc_20.groupby(["layer","year_2"], as_index=False).agg(
        top_ebc=("top_ebc", "sum"),
        bottom_ebc=("bottom_ebc", "sum")
    )
    df_exp_bc_20["ExpectedBC"] = ratio(df_exp_bc_20["top_ebc"], df_exp_bc_20["bottom_ebc"] / utc)
    df_exp_bc_20.rename(
        columns={"year_2":"year"},
        inplace=True
    )

    # resume with Deveoped BF Claims for Aggregate Limits
    df_dev_bf = df_dev_bf.merge(df_onlevelled_rev, on="year", how="left")
    df_dev_bf = df_dev_bf.merge(df_exp_bc_15, on=["year","layer"], how="left")
    df_dev_bf["bf_prep"] = np.where(df_dev_bf["incurred_dev_factor"] > 0.7, ratio(df_dev_bf["recovery"], df_dev_bf["incurred_dev_factor"]), 
                df_dev_bf["recovery"] + (1 - df_dev_bf["incurred_dev_factor"]) * df_dev_bf["revalued_notional_revenue_weighted"] * df_dev_bf["ExpectedBC"] / utc)
    df_dev_bf["bf"] = np.where(df_dev_bf["agg_lim"] == 0, df_dev_bf["bf_prep"], np.minimum(df_dev_bf["agg_lim"], df_dev_bf["bf_prep"]))

    # Uncapped Developed Count (After Maintenance Retention only)
    # Needs to account for include - does the ogirinal df_layers_rec exclude those that are not included?
    df_unc_dev_count = (
        (df_layers_rec["recovery"] > 0)
        .groupby([df_layers_rec["year"], df_layers_rec["layer"]])
        .sum()
        .reset_index(name="count_recovery")
    )

    # Get claims_dev_pattern
    df_unc_dev_count = df_unc_dev_count.merge(df_dev_factors, on="year", how="left")

    # Chain ladder developed Count (After Maintenance Retention only)
    df_unc_dev_count["chain_ladder_dev_count"] = ratio(df_unc_dev_count["count_recovery"], df_unc_dev_count["claims_dev_factor"])

    # Calculate Expected Frequency per unit of exposure
    # top sumproduct(uncappaed dev count, capecod factor)
    # bottom sumprodcut(onlevelled revenue, capecod factor, incurred df pattern)
    # merge on onlevelled revenue and incurred df pattern
    # also need to cross product for year_2
    df_exp_freq_unit = df_unc_dev_count.copy()
    df_exp_freq_unit = df_exp_freq_unit.merge(df_onlevelled_rev, on="year", how="left")
    #df_exp_freq_unit = df_exp_freq_unit.merge(df_dev_factors, on="year", how="left")
    df_exp_freq_unit = df_exp_freq_unit.merge(df_actual_years, how="cross")
    df_exp_freq_unit["cape_cod_factor"] = decay_factor ** abs(df_exp_freq_unit["year"] - df_exp_freq_unit["year_2"])
    df_exp_freq_unit["top"] = df_exp_freq_unit["count_recovery"] * df_exp_freq_unit["cape_cod_factor"]
    df_exp_freq_unit["bottom"] = df_exp_freq_unit["cape_cod_factor"] * df_exp_freq_unit["revalued_notional_revenue_weighted"] * df_exp_freq_unit["incurred_dev_factor"]
    df_exp_freq_unit = df_exp_freq_unit.groupby(["layer","year_2"], as_index=False).agg({"top":"sum", "bottom":"sum"})
    df_exp_freq_unit["EFreq"] = ratio(df_exp_freq_unit["top"], df_exp_freq_unit["bottom"] / utc)     # layer, year, Efreq
    df_exp_freq_unit.rename(
        columns={"year_2":"year"},
        inplace=True
    )

    # BF developed Count (After Maintenance Retention only)
    # requires Expected Frequency per unit of exposure
    # requires weighted revalued ntional revenue
    df_unc_dev_count = df_unc_dev_count.merge(df_exp_freq_unit, on=["year", "layer"], how="left")
    df_unc_dev_count = df_unc_dev_count.merge(df_onlevelled_rev, on="year", how="left")
    df_unc_dev_count["bf_dev_count"] = np.where(
        df_unc_dev_count["claims_dev_factor"] > 0.7, 
        df_unc_dev_count["chain_ladder_dev_count"],
        df_unc_dev_count["count_recovery"] + df_unc_dev_count["EFreq"] * df_unc_dev_count["revalued_notional_revenue_weighted"] / utc * (1 - df_unc_dev_count["claims_dev_factor"])
        )

    # Accumulated Inurred capped with aggregate dropdown
    # this is basically df_layers_rec_dropdown
    # get selected layer
    selected_layer = hxd.cds.experience_rating.layer_to_view
    df_accum_inc_capped_layer = df_layers_rec_dropdown_grouped[df_layers_rec_dropdown_grouped["layer"]==selected_layer]

    years_claims_summary = range(21)     #16
    for year in years_claims_summary:
        df_filter = df_accum_inc_capped_layer[df_accum_inc_capped_layer["year"]==incept_year-year]
        if df_filter.empty:
            value = 0
        else:
            value = df_filter["recovery"].iloc[0]
        setattr(getattr(hxd.cds.experience_rating.claims_summary,f"year_{year}"),"ql_inflated_incurred", value)

    # GCC Rebased
    # Just reuse df_accum_inc_capped_layer
    df_accum_inc_capped_layer = df_accum_inc_capped_layer.merge(df_cape_cod_factor, on="year", how="left")
    df_accum_inc_capped_layer = df_accum_inc_capped_layer.rename(columns={"cape_cod_factor":"decay_factor",
                                                                          "incurred_dev_factor": "incurred_df",
                                                                          "revalued_notional_revenue_weighted":"revenue"}
                                                                )
    df_accum_inc_capped_layer["revenue"] = df_accum_inc_capped_layer["revenue"] / utc
    df_accum_inc_capped_layer["product"] = df_accum_inc_capped_layer["decay_factor"] * df_accum_inc_capped_layer["incurred_df"] * df_accum_inc_capped_layer["revenue"] 
    product_total = df_accum_inc_capped_layer["product"].sum() or 0
    df_accum_inc_capped_layer["step_1"] = df_accum_inc_capped_layer["decay_factor"] * df_accum_inc_capped_layer["recovery"]
    df_accum_inc_capped_layer["step_2"] = df_accum_inc_capped_layer["step_1"] / product_total
    step_2_sum = df_accum_inc_capped_layer["step_2"].sum()
    df_accum_inc_capped_layer["weighting_applied_gcc"] = df_accum_inc_capped_layer["decay_factor"].fillna(0) / product_total if product_total > 0 else 0
    weighting_applied_gcc_sum = df_accum_inc_capped_layer["weighting_applied_gcc"].sum() or 0
    df_accum_inc_capped_layer["gcc_rebased"] = df_accum_inc_capped_layer["weighting_applied_gcc"] / weighting_applied_gcc_sum if weighting_applied_gcc_sum > 0 else 0

    years_claims_summary = range(21)
    for year in years_claims_summary:
        df_filter = df_accum_inc_capped_layer[df_accum_inc_capped_layer["year"]==incept_year-year]
        if df_filter.empty:
            value = 0
        else:
            raw_value = df_filter["gcc_rebased"].iloc[0]
            value = None if pd.isna(raw_value) else raw_value 

        setattr(getattr(hxd.cds.experience_rating.claims_summary,f"year_{year}"),"weighting_applied_year", value)


    # Summary
    sum_notional_revenue = df_onlevelled_rev["revalued_notional_revenue_weighted"].sum()
    incept_year = hxd.hx_core.inception_date.year
    cp = get_credibility_params(num_years_experience)
    df_exp_bc_10_iy = df_exp_bc_10[df_exp_bc_10["year"] == incept_year][["layer", "ExpectedBC"]]
    df_exp_bc_15_iy = df_exp_bc_15[df_exp_bc_15["year"] == incept_year][["layer", "ExpectedBC"]]
    df_exp_bc_20_iy = df_exp_bc_20[df_exp_bc_20["year"] == incept_year][["layer", "ExpectedBC"]]    
    df_unc_dev_count_group_layer = df_unc_dev_count.groupby("layer").agg({"count_recovery": "sum"})

    df_summary = df_dev_bf.groupby("layer", as_index=False).agg({"bf": "sum"}).rename(columns={"bf": "total_claims_to_layer"})
    df_summary["experience_rate"] = ratio(df_summary["total_claims_to_layer"], sum_notional_revenue / utc) #* 1e6 / utc

    df_summary = df_summary.merge(df_exp_bc_20_iy, on="layer", how="left")
    df_summary.rename(
        columns={"ExpectedBC":"experience_rate_20yr"},
        inplace=True
    )

    df_summary = df_summary.merge(df_exp_bc_15_iy, on="layer", how="left")
    df_summary.rename(
        columns={"ExpectedBC":"experience_rate_15yr"},
        inplace=True
    )

    df_summary = df_summary.merge(df_exp_bc_10_iy, on="layer", how="left")
    df_summary.rename(
        columns={"ExpectedBC":"experience_rate_10yr"},
        inplace=True
    )

    df_summary = df_summary.merge(df_unc_dev_count_group_layer, on="layer", how="left")
    df_summary["claim_count_credibility"] = np.minimum(np.maximum((ratio(df_summary["count_recovery"], cp.num_claims_full_cred)) ** 0.5, ratio(cp.cred_based_on_years_experience_nil_claims, cp.cred_based_on_years_experience)), 1)
    df_summary["exposure_credibility"] = cp.cred_based_on_years_experience

    df_summary = df_summary.merge(df_layers_xs, on="layer", how="left")
    df_summary["decay_factor"] = np.power(cp.dampening_factor, np.maximum(0, (df_summary["eec_excess"] - cp.decay_treshold)/ 1e6))

    ############# LEV and ILF #####################
    profession = "lpl" if hxd.cds.profession == "Lawyers" else "aec"
    bp = get_base_params(profession)
    df_layer_limit = pd.concat(
        [
            get_eec_limit(hxd.cds.layers),
            get_eec_limit(hxd.cds.layers_addl)
        ],
        ignore_index=True
    )

    df_summary = df_summary.merge(df_layer_limit, on="layer", how="left")

    # --- Helpers -------------------------------------------------------------
    def log_safe(x):
        """Vectorised log that returns NaN for non-positive values."""
        x = np.asarray(x, dtype=float)   # <— ensures float dtype
        return np.where(x > 0, np.log(x), np.nan)

    def lognorm_cdf(x, mu, sigma):
        """Standard lognormal CDF."""
        return norm.cdf((log_safe(x) - mu) / sigma)

    def adj_cdf(x, mu, sigma):
        """Adjusted CDF used in the Excel formula."""
        return norm.cdf((log_safe(x) - mu) / sigma - sigma)

    mu = bp.mu_base
    sigma = bp.sigma
    #mu = 13.48
    #sigma = 2.1
    lim_base = attritional_cap
    xs_base = 0
    LX = lim_base + xs_base
    incept_year_rnrw = getattr(getattr(hxd.cds.experience_rating.claims_summary, f'year_0'),"revalued_notional_revenue_weighted") or 0

    # ---------- LEV Base -------------------
    cdf_LX_adj = adj_cdf(LX, mu, sigma)
    cdf_X_adj = 0.0 if xs_base == 0 else adj_cdf(xs_base, mu, sigma)

    cdf_LX = lognorm_cdf(LX, mu, sigma)
    cdf_X  = 0.0 if xs_base == 0 else lognorm_cdf(xs_base,  mu, sigma)

    lev_base = (
        np.exp(mu + 0.5 * sigma**2) * (cdf_LX_adj - cdf_X_adj)
        + LX * (1 - cdf_LX)
        - xs_base  * (1 - cdf_X)
    )

    # --- Precompute columns --------------------------------------------------
    L = df_summary["eec_limit"]
    X = df_summary["eec_excess"]
    LX = L + X
 
    # Mask zeros to avoid unnecessary branching
    cdf_LX_adj = adj_cdf(LX, mu, sigma)
    cdf_LX = lognorm_cdf(LX, mu, sigma)

    # For X == 0, force CDF = 0 (the correct mathematical limit)
    cdf_X_adj = np.where(X <= 0, 0.0, adj_cdf(X, mu, sigma))
    cdf_X     = np.where(X <= 0, 0.0, lognorm_cdf(X, mu, sigma))

    # --- Main expression -----------------------------------------------------
    df_summary["lev"] = (
        np.exp(mu + 0.5 * sigma**2) * (cdf_LX_adj - cdf_X_adj)
        + LX * (1 - cdf_LX)
        - X  * (1 - cdf_X)
    )

    # requires attritional cap 
    #att_layer_15yr = 814024529 
    df_exp_bc_att_15yr_filtered = df_exp_bc_att_15yr.loc[df_exp_bc_att_15yr["year"] == (incept_year - 1),"ExpectedBC"]
    att_layer_15yr = 0 if df_exp_bc_att_15yr_filtered.empty else df_exp_bc_att_15yr_filtered.iloc[0]

    att_layer_total_claims_to_layer = df_att_bf_1[df_att_bf_1["year"] < incept_year]["bf"].sum()
    wrnr_not_incept_year = df_onlevelled_rev[df_onlevelled_rev["year"] < incept_year]["revalued_notional_revenue_weighted"].sum()

    att_layer_experience_rate = att_layer_total_claims_to_layer / (wrnr_not_incept_year / utc)
    #att_layer_experience_rate = 827705078
    df_summary["ilf"] = ratio(df_summary["lev"], lev_base)
    df_summary["ilf"] = df_summary["ilf"] * (att_layer_15yr if is_cape_cod else att_layer_experience_rate) * incept_year_rnrw / utc / 0.7 / (1 - df_summary["brokerage"].fillna(0))

    # Credibility weighting
    # Sort df_summary by layer order
    df_layer_order = layer_order()
    df_summary = df_summary.merge(df_layer_order, on="layer", how="left")
    df_summary.sort_values("order", ascending=True, inplace=True)

    # 1st row
    if df_summary.empty:
        pass
    else:
        #1st row
        df_summary.loc[df_summary.index[0], "credibility_weighting"] = np.minimum(
            1, 
            df_summary["claim_count_credibility"].iloc[0] 
            * df_summary["exposure_credibility"].iloc[0] 
            * cp.cred_based_on_years_experience
            )     
        # Recursive rows
        for i in range(1, len(df_summary)):
            prev = df_summary.loc[df_summary.index[i-1], "credibility_weighting"]

            if (df_summary["experience_rate"].iloc[i] > 0) and (df_summary["claim_count_credibility"].iloc[i] == 0):
                if 0 < df_summary["decay_factor"].iloc[i-1] < 1:
                    value = prev * df_summary["decay_factor"].iloc[i-1]
                else:
                    value = prev * cp.dampening_factor
            else:
                value = np.minimum(
                    1,
                    df_summary["claim_count_credibility"].iloc[i]
                    * df_summary["decay_factor"].iloc[i]
                    * cp.cred_based_on_years_experience
                )

            df_summary.loc[df_summary.index[i], "credibility_weighting"] = value

        df_summary = df_summary.fillna(0)
        # write to layers
        for layers in [hxd.cds.layers, hxd.cds.layers_addl]:
            for layer in layers:
                if layer.include:
                    ers = layer.experience_rating_summary
                    name = layer.name
                    layer.experience_rate = (df_summary[df_summary["layer"]==name]["experience_rate_15yr"].iloc[0] if is_cape_cod else df_summary[df_summary["layer"]==name]["experience_rate"].iloc[0]) * 1e6 / utc
                    layer.experience_weighting_2.calculated = df_summary[df_summary["layer"]==name]["credibility_weighting"].iloc[0]
                    layer.experience_rate_20yr_avg = df_summary[df_summary["layer"]==name]["experience_rate_20yr"].iloc[0]   # change this experience_rate_20yr
                    layer.experience_rate_15yr_avg = df_summary[df_summary["layer"]==name]["experience_rate_15yr"].iloc[0]
                    layer.experience_rate_10yr_avg = df_summary[df_summary["layer"]==name]["experience_rate_10yr"].iloc[0]
                    ers.ilf_gross_benchmark_premium = df_summary[df_summary["layer"]==name]["ilf"].iloc[0]
              
def structure_and_pricing(hxd):
    def calc_layer_structure(layers):
        for idx, layer in enumerate(layers):
            if layer.include:
                brokerage = min(0.9999, (layer.brokerage or 0)) #cannot be 1 or greater - user will receive validation error also
                experience_rate = layer.experience_rate or 0
                experience_weighting_calculated = layer.experience_weighting_2.calculated or 0
                experience_weighting_selected = layer.experience_weighting_2.selected or 0
                layer.exposure_rate_incl_adj = (layer.exposure_rate or 0) * (1 + (layer.wordings_adj or 0 )) * (1 + (layer.uw_adj or 0))
                layer.experience_rate_incl_adj = experience_rate * (1 + (layer.wordings_adj or 0 )) * (1 + (layer.uw_adj or 0))
                # Experience rating comes from rate_claims.py

                layer.blended_model_net_rate_pre = (experience_rate * experience_weighting_calculated + (layer.exposure_rate or 0) * (1 - experience_weighting_calculated)) * (1 + cat_load) 
                layer.expected_loss_cost_net_pre = (layer.blended_model_net_rate_pre or 0) * (hxd.cds.exposure.granular.exposure_expected_current_year or 0) / 1e6

                layer.blended_model_net_rate = (layer.experience_rate_incl_adj * experience_weighting_selected + layer.exposure_rate_incl_adj * (1 - experience_weighting_selected)) * (1 + cat_load)  # no nmp_load
                layer.expected_loss_cost_net = (layer.blended_model_net_rate or 0) * (hxd.cds.exposure.granular.exposure_expected_current_year or 0) / 1e6

                if layer.limit_eec is not None:
                    layer.uw_experience_weighting = 0.2 if (layer.exposure_rate or 0) > experience_rate else 1
                else:
                    layer.uw_experience_weighting = 0
                layer.blended_uw_net_rate = ((1 - layer.uw_experience_weighting) * layer.exposure_rate_incl_adj + layer.uw_experience_weighting * experience_rate) * (1 + cat_load)    # no nmp_load
                layer.benchmark_premium_uw_view = ((layer.blended_uw_net_rate or 0) * (hxd.cds.exposure.granular.exposure_expected_current_year or 0) / 1e6) / 0.7 / (1 - brokerage)
                
                layer.technical_premium_100 = ((layer.expected_loss_cost_net_pre * (1 + tp.che) + tp.fixed_expense) / (1 - tp.variable_expense + tp.investment_income - tp.ri_cost - tp.roc * tp.capital_cost)) / (1 - brokerage) if layer.include else 0
                layer.benchmark_premium_100 = ((layer.expected_loss_cost_net_pre or 0) / 0.7) / (1 - brokerage)
                layer.technical_premium_100_incl_adj = ((layer.expected_loss_cost_net * (1 + tp.che) + tp.fixed_expense) / (1 - tp.variable_expense + tp.investment_income - tp.ri_cost - tp.roc * tp.capital_cost)) / (1 - brokerage) if layer.include else 0
                layer.benchmark_premium_100_incl_adj = ((layer.expected_loss_cost_net or 0) / 0.7) / (1 - brokerage)

                layer.benchmark_premium_exposure_100 = layer.benchmark_premium_100 * (1 - layer.uw_experience_weighting)       #layer.uw_experience_weighting ?
                layer.benchmark_premium_experience_100 = layer.benchmark_premium_100 * layer.uw_experience_weighting       
                # layer.quoted_premium_100 = 1          Inputs
                # layer.bound_premium_100 = 1           Inputs
                if profession == "lawyers":
                    layer.gross_rate_per_mill = ratio(layer.bound_premium_100 or 0, hxd.cds.lawyers_num_attorneys_full or 1)
                else:
                    layer.gross_rate_per_mill = ratio(layer.bound_premium_100 or 0, hxd.cds.exposure.granular.exposure_expected_current_year or 1) / 1e6
            
                layer.bpi_quoted_100 = ratio(layer.quoted_premium_100 or 0, layer.benchmark_premium_100 or 1)
                layer.bpi_bound_100 = ratio(layer.bound_premium_100 or 0, layer.benchmark_premium_100 or 1)
                layer.tpi_quoted_100 = ratio(layer.quoted_premium_100 or 0, layer.technical_premium_100 or 1)
                layer.tpi_bound_100 = ratio(layer.bound_premium_100 or 0, layer.technical_premium_100 or 1)

                layer.bpi_quoted_100_incl_adj = ratio(layer.quoted_premium_100 or 0, layer.benchmark_premium_100_incl_adj or 1)
                layer.bpi_bound_100_incl_adj = ratio(layer.bound_premium_100 or 0, layer.benchmark_premium_100_incl_adj or 1)
                layer.tpi_quoted_100_incl_adj = ratio(layer.quoted_premium_100 or 0, layer.technical_premium_100_incl_adj or 1)
                layer.tpi_bound_100_incl_adj = ratio(layer.bound_premium_100 or 0, layer.technical_premium_100_incl_adj or 1)

                # layer.status                      Inputs
                # layer.policyRefernce              Inputs   
                # layer.written_line                Inputs
                layer.bound_premium_share = (layer.written_line or 1) * (layer.bound_premium_100 or 0)
                elevated_risk_year_load = hxd.cds.rating_factors.elevated_risk_year_load
                layer.gross_premium_uw_view = (layer.blended_uw_net_rate * (1 + elevated_risk_year_load) * (hxd.cds.exposure.granular.exposure_expected_current_year or 0) / 1e6) / 0.7 / (1-brokerage)
                layer.technical_premium_ryv = ((layer.expected_loss_cost_net * (1 + elevated_risk_year_load) * (1 + tp.che) + tp.fixed_expense) / (1 - tp.variable_expense + tp.investment_income - tp.ri_cost - tp.roc * tp.capital_cost)) / (1-brokerage) if layer.include else 0
                layer.benchmark_premium_ryv = (layer.expected_loss_cost_net * (1 + elevated_risk_year_load) / 0.7) / (1-brokerage)

                #loss ratios
                premium = (layer.quoted_premium_100 or 0) if layer.status != "Bound" else (layer.bound_premium_100 or 0)
                layer.pflr = ratio(layer.expected_loss_cost_net, premium)
                layer.pflr_pre_uw_adj = ratio((layer.expected_loss_cost_net_pre or 0), premium)
                layer.uw_adj_impact = ratio((layer.expected_loss_cost_net or 0), (layer.expected_loss_cost_net_pre or 0)) - 1

                layer.bpi_quoted_ryv = ratio(layer.quoted_premium_100, layer.benchmark_premium_ryv)
                layer.bpi_bound_ryv = 0 if (layer.benchmark_premium_ryv or 0) == 0 else (layer.bound_premium_100 or 0) / layer.benchmark_premium_ryv
                layer.tpi_quoted_ryv = ratio(layer.quoted_premium_100, layer.technical_premium_ryv)
                layer.tpi_bound_ryv = 0 if (layer.technical_premium_ryv or 0) == 0 else (layer.bound_premium_100 or 0) / layer.technical_premium_ryv

    profession = hxd.cds.profession
    tp = get_tech_params(hxd.hx_core.inception_date.year)
    df_cat_load = hx.params.ref_lst_cat_load
    df_cat_load_filter = df_cat_load[df_cat_load["Professions"]==profession]
    if df_cat_load_filter.empty:
        cat_load = 0
    else:
        cat_load = df_cat_load_filter["CatLoad"].iloc[0]

    # populate cat_load field
    hxd.cds.rating_factors.cat_load = cat_load

    nmp_load = get_nmp_load()

    calc_layer_structure(hxd.cds.layers)
    calc_layer_structure(hxd.cds.layers_addl)

def populate_experience_rating_layer_summary(hxd):
    utc = units_to_convert(hxd)
    incept_year_rnrw = getattr(getattr(hxd.cds.experience_rating.claims_summary, f'year_0'),"revalued_notional_revenue_weighted") or 0
    is_cape_cod = is_cape_cod_pricing_method(hxd)
    for layers in [hxd.cds.layers, hxd.cds.layers_addl]:
        for layer in layers:
            if layer.include:
                brokerage = min(0.9999, (layer.brokerage or 0)) #cannot be 1 or greater - user will receive validation error also
                ers = layer.experience_rating_summary
                ers.aoc_limit = layer.limit_eec
                ers.agg_limit = layer.limit_eec if (layer.rtc or 0 > 0 ) or (layer.rtc_agg or 0 > 0) else layer.limit_agg
                ers.aoc_attachment = layer.excess_eec
                ers.agg_attachment = layer.excess_eec if (layer.rtc or 0 > 0 ) or (layer.rtc_agg or 0 > 0) else layer.excess_agg
                x = (layer.experience_rate or 0) * (incept_year_rnrw or 0) / 1e6
                ers.gross_benchmark_premium = x / 0.7 / (1 - brokerage)
                # ers.ilf_gross_benchmark_premium = 10
            
def populate_experience_rating_layer_to_view_summary(hxd):
    fx_rate = (get_fx_rate(hxd.cds.currencies.source_currency) or 1) #required or not?
    selected_layer = hxd.cds.experience_rating.layer_to_view
    ltv = hxd.cds.experience_rating.layer_to_view_summary
    for layers in [hxd.cds.layers, hxd.cds.layers_addl]:
        for layer in layers:
            if layer.name == selected_layer:
                ltv.aoc_limit_usd = layer.limit_eec
                ltv.agg_limit_usd = layer.limit_agg 
                ltv.aoc_attachment = layer.excess_eec
                ltv.agg_attachment = layer.excess_agg

def populate_experience_rating_10_15_tables(hxd):
    utc = units_to_convert(hxd)
    path=hxd.cds.experience_rating

    # Weighted Revalued Notional Revenue
    # year 1 to 10, year 1 to 15
    incept_year_rnrw = getattr(getattr(path.claims_summary, f'year_0'),"revalued_notional_revenue_weighted") or 0
    
    total_10 = 0
    total_wt_10 = 0
    total_qlii_10 = 0
    for x in range(1, 11):
        rnrw = getattr(getattr(path.claims_summary, f'year_{x}'),"revalued_notional_revenue_weighted") or 0
        wt = getattr(getattr(path.claims_summary, f'year_{x}'),"pcnt_developed") or 0
        qlii = getattr(getattr(path.claims_summary, f'year_{x}'),"ql_inflated_incurred") or 0
        
        total_10 += rnrw
        total_wt_10 += rnrw * wt
        total_qlii_10 += qlii


    total_15 = 0
    total_wt_15 = 0
    total_qlii_15 = 0
    for x in range(1, 16):
        rnrw = getattr(getattr(path.claims_summary, f'year_{x}'),"revalued_notional_revenue_weighted") or 0
        wt = getattr(getattr(path.claims_summary, f'year_{x}'),"pcnt_developed") or 0
        qlii = getattr(getattr(path.claims_summary, f'year_{x}'),"ql_inflated_incurred") or 0
        
        total_15 += rnrw
        total_wt_15 += rnrw * wt
        total_qlii_15 += qlii


    total_20 = 0
    total_wt_20 = 0
    total_qlii_20 = 0
    for x in range(1, 21):
        rnrw = getattr(getattr(path.claims_summary, f'year_{x}'),"revalued_notional_revenue_weighted") or 0
        wt = getattr(getattr(path.claims_summary, f'year_{x}'),"pcnt_developed") or 0
        qlii = getattr(getattr(path.claims_summary, f'year_{x}'),"ql_inflated_incurred") or 0
        
        total_20 += rnrw
        total_wt_20 += rnrw * wt
        total_qlii_20 += qlii

    path.weighted_revalued_notional_revenue.last_10_years = total_10
    path.weighted_revalued_notional_revenue.last_15_years = total_15
    path.weighted_revalued_notional_revenue.last_20_years = total_20  


    # Developed Weighted Revalued Notional Revenue
    path.developed_weighted_revalued_notional_revenue.last_10_years = total_wt_10
    path.developed_weighted_revalued_notional_revenue.last_15_years = total_wt_15
    path.developed_weighted_revalued_notional_revenue.last_20_years = total_wt_20

    # Value of Claims Data
    path.value_of_claims_data.last_10_years = ratio(total_wt_10, incept_year_rnrw)
    path.value_of_claims_data.last_15_years = ratio(total_wt_15, incept_year_rnrw)
    path.value_of_claims_data.last_20_years = ratio(total_wt_20, incept_year_rnrw)

    # Inflated Incurred to Quoted Layer
    path.inflated_incurred_to_quoted_layer.last_10_years = total_qlii_10
    path.inflated_incurred_to_quoted_layer.last_15_years = total_qlii_15
    path.inflated_incurred_to_quoted_layer.last_20_years = total_qlii_20

    # Per Yr of Claims Data Value
    # Compute Loss Cost Per Billion Revenue         =INDEX('ROutput & Calcs'!$L$175:$L$190,MATCH(QuotedLayer,'ROutput & Calcs'!$I$175:$I$190,0))
    # Experience Rate 10yr * incept_year_rnrw / Unit to convert
    # Experience Rate 15yr * incept_year_rnrw / Unit to convert

    # Get Experience Rate 10yr
    exp_rate_10yr = 1
    exp_rate_15yr = 1    
    exp_rate_20yr = 1
    brokerage_selected_layer = 0
    for layers in [hxd.cds.layers, hxd.cds.layers_addl]:
        for layer in layers:
            if layer.include and layer.name == hxd.cds.experience_rating.layer_to_view:
                exp_rate_10yr = layer.experience_rate_10yr_avg
                exp_rate_15yr = layer.experience_rate_15yr_avg
                exp_rate_20yr = layer.experience_rate_20yr_avg
                brokerage_selected_layer = min(0.9999, (layer.brokerage or 0))


    path.per_yr_of_claims_data_value.last_10_years = (exp_rate_10yr or 0) * (incept_year_rnrw or 0)  / utc
    path.per_yr_of_claims_data_value.last_15_years = (exp_rate_15yr or 0) * (incept_year_rnrw or 0)  / utc
    path.per_yr_of_claims_data_value.last_20_years = (exp_rate_20yr or 0) * (incept_year_rnrw or 0)  / utc

    # Gross Benchmark Experience Rated Premium
    #per_yr_claims_data_value / 0.7 /(1 -  brokerage for quoted layer)
    path.gross_benchmark_experience_rated_premium.last_10_years = path.per_yr_of_claims_data_value.last_10_years / 0.7 / (1 - brokerage_selected_layer)
    path.gross_benchmark_experience_rated_premium.last_15_years = path.per_yr_of_claims_data_value.last_15_years / 0.7 / (1 - brokerage_selected_layer)
    path.gross_benchmark_experience_rated_premium.last_20_years = path.per_yr_of_claims_data_value.last_20_years / 0.7 / (1 - brokerage_selected_layer)

def test_layer_selected(hxd):
    """
    returns true if a layers is selected
    """
    count = 0 
    for layers in [hxd.cds.layers, hxd.cds.layers_addl]:
        for layer in layers:
            if layer.include:
                count +=1
    
    return not count == 0

def set_hover_info(hxd):
    for path, text in hover_info.items():
        setattr(hxd.cds.hover_info, path, text)

def set_notes(hxd):
    hxd.cds.retention_split_notes = retention_split_notes
    hxd.cds.policy_notes = policy_notes


def experience_rating_oc(hxd):
    #fx_rate = (get_fx_rate(hxd.cds.currencies.source_currency) or 1)
    fx_rate = 1
    
    def oc_values(dct, path, fx):
        for key, value in dct.items():
            new_value = None if getattr(path, value) is None else getattr(path, value) * fx
            setattr(path, key, new_value)

    dct = {
        "aoc_limit_oc":"aoc_limit_usd",
        "agg_limit_oc":"agg_limit_usd",
        "aoc_attachment_oc":"aoc_attachment",
        "agg_attachment_oc":"agg_attachment"
    }
    path = hxd.cds.experience_rating.layer_to_view_summary
    oc_values(dct, path, fx_rate)    

    dct = {
        "revalued_notional_revenue_oc":"revalued_notional_revenue",
        "revalued_notional_revenue_weighted_oc":"revalued_notional_revenue_weighted",
        "gu_incurred_oc":"gu_incurred",
        "gu_inflated_oc":"gu_inflated",
        "ql_inflated_incurred_oc":"ql_inflated_incurred"
    }

    for key in range(20, -1,-1):
        path = getattr(hxd.cds.experience_rating.claims_summary, f"year_{key}")
        oc_values(dct, path, fx_rate)

    dct = {
        "last_10_years_oc":"last_10_years",
        "last_15_years_oc":"last_15_years",
        "last_20_years_oc":"last_20_years"
    }
    path = hxd.cds.experience_rating.weighted_revalued_notional_revenue
    oc_values(dct, path, fx_rate)    

    path = hxd.cds.experience_rating.developed_weighted_revalued_notional_revenue
    oc_values(dct, path, fx_rate)

    path = hxd.cds.experience_rating.value_of_claims_data
    oc_values(dct, path, 1)

    path = hxd.cds.experience_rating.inflated_incurred_to_quoted_layer
    oc_values(dct, path, fx_rate)

    path = hxd.cds.experience_rating.per_yr_of_claims_data_value
    oc_values(dct, path, fx_rate)

    path = hxd.cds.experience_rating.gross_benchmark_experience_rated_premium
    oc_values(dct, path, fx_rate)

    dct = {
        "aoc_limit_oc":"aoc_limit",
        "agg_limit_oc":"agg_limit",
        "aoc_attachment_oc":"aoc_attachment",
        "agg_attachment_oc":"agg_attachment",
        "gross_benchmark_premium_oc":"gross_benchmark_premium",
        "ilf_gross_benchmark_premium_oc":"ilf_gross_benchmark_premium"
    }

    layers_all = [hxd.cds.layers, hxd.cds.layers_addl]
    for layers in layers_all:
        for layer in layers:
            for key, value in dct.items():
                new_value = None if getattr(layer.experience_rating_summary, value) is None else getattr(layer.experience_rating_summary, value) * fx_rate
                setattr(layer.experience_rating_summary, key, new_value)

def populate_pbu_chart(hxd):
    # premium build up
    tp = get_tech_params(hxd.hx_core.inception_date.year)
    selected_layer = hxd.cds.technical_premium_buildup_layer
    for layers in [hxd.cds.layers, hxd.cds.layers_addl]:
        for layer in layers:
            if layer.name == selected_layer:
                net_tp = (layer.technical_premium_100 or 0) * (1 - (layer.brokerage or 0))
                nel_fixedcost = (layer.expected_loss_cost_net or 0) * (1 + tp.che) + tp.fixed_expense
                profit_load = tp.roc * tp.capital_cost - tp.investment_income

                # Technical premium
                path = hxd.cds.pbu_chart.data.technical_premium
                path.brokerage = net_tp / (1 - (layer.brokerage or 0)) - net_tp
                path.profit_load = profit_load * net_tp
                path.expenses = nel_fixedcost - (layer.expected_loss_cost_net or 0) + net_tp * tp.variable_expense
                path.ri_cost = tp.ri_cost * net_tp
                path.elc = layer.expected_loss_cost_net

                # Benchmark premium
                path = hxd.cds.pbu_chart.data.benchmark_premium
                path.elc = layer.expected_loss_cost_net
                path.expenses = (layer.expected_loss_cost_net or 0) / 0.7 - (layer.expected_loss_cost_net or 0)
                net_tp_eff = (path.elc or 0) + (path.expenses or 0)
                path.brokerage = 0 if (layer.brokerage or 0) == 0 else (layer.expected_loss_cost_net or 0) / (1 - (layer.brokerage or 0)) - (layer.expected_loss_cost_net or 0)                

                # Bound premium
                path = hxd.cds.pbu_chart.data.bound_premium
                path.elc = layer.bound_premium_100

def rate_pricing(hxd):
    set_hover_info(hxd)
    read_inception_expiry_date(hxd)
    set_notes(hxd)
    layer_names(hxd)
    layer_addl_names(hxd)

    if test_layer_selected(hxd):
        tower_excess_calc(hxd)
        develop_claims(hxd)
        structure_and_pricing(hxd)
        # Experience rating
        populate_experience_rating_layer_summary(hxd)
        populate_experience_rating_layer_to_view_summary(hxd)
        populate_experience_rating_10_15_tables(hxd)

        # Experience rating original CCY
        experience_rating_oc(hxd)

        profession = "lpl" if hxd.cds.profession == "Lawyers" else "aec"
        expected_exposure = (hxd.cds.exposure.granular.exposure_expected_current_year or 0)
        get_model_params(hxd, profession, expected_exposure)

        # Premium Build Up
        populate_pbu_chart(hxd)
