import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import pd_df_from_hx_list, df_to_dict, write_pd_to_hxd, look_up, ratio, interp2d_agg_factors, extract_subkey_values
from algorithms import parameter_tables_schema as params
from operator import itemgetter

def rate_pricing_non_education(hxd):

    # Shortcuts
    rf = hxd.cds.rating_factors
    fx_rates = params.fx_rates.df()

    # Main exposure table
    df = pd_df_from_hx_list(hxd.cds.exposure.granular.non_education).fillna(0)
    fx = look_up(hxd.cds.currencies.source_currency, "ccy", "fx_rate", fx_rates, if_not_found=1)
    
    # Create dictionaries from parameter tables
    state_code_name_dict = df_to_dict(hx.params.lst_state_lookup, "State Code", "State Name")
    city_risk_dict = df_to_dict(hx.params.city_risk_factor, "City Risk", "Rate")
    sector_rates_dict = df_to_dict(hx.params.sector_rates, "Sector", "Rate")
    country_rates_dict = df_to_dict(hx.params.country_rates, "Country", "Rate")
    state_rates_dict = df_to_dict(hx.params.state_rates, "State", "Rate")
    location_dict = df_to_dict(hx.params.location_factor, "Field", "Relativity")
    ease_of_access_dict = df_to_dict(hx.params.ease_of_access, "Ease of Access", "Rate")
    footfall_dict = df_to_dict(hx.params.footfall_factor, "Footfall", "Rate")
    enclosed_space_dict = df_to_dict(hx.params.enclosed_space_factor, "Enclosed Space", "Rate")
    events_min_el_dict = df_to_dict(hx.params.events_min_el, "Events Footfall", "Events Min EL")
    events_avg_days_dict = df_to_dict(hx.params.events_avg_days, "Event", "Average Days")
    

    # Sector sub sector dictionary
    subsector_rates_df = hx.params.sector_subsector_rates
    subsector_rates_df["Lookup"] = subsector_rates_df["Sector"] + subsector_rates_df["SubSector"] 
    subsector_dict = df_to_dict(
        subsector_rates_df, 
        "Lookup", 
        [
            "Low",
            "Medium",
            "High",
            "Counselling Est Measure",
            "TP Per Employee",
            "TP Per Unit",
            "Measure",
            "Minimum Premium",
            "Relativity",
            "Spread Discount Group"
        ]
    )
  
    scalars = df_to_dict(hx.params.scalar_parameters, "Field", "Parameter")
    
    # Map state name from code and write back to hxd
    df["state_name"] = np.where(
        df["country"] == "US", 
        df["state_code"].map(state_code_name_dict).fillna(value=""),
        None
    )

    # Map football band to calc num requiring councelling
    df["sector_lookup"] = df["sector/sector"].astype(str) + df["sector/sub_sector"].astype(str)
    df["footfall_measure"] = df["sector_lookup"].map(extract_subkey_values(subsector_dict, "Measure"))
    df["selected_footfall"] = np.where(df["footfall_measure"] == "Staff", df["num_of_staff_per_est"], df["footfall_measure_per_est"])
    df["footfall_band"] = np.where(
        df["selected_footfall"] >= df["sector_lookup"].map(extract_subkey_values(subsector_dict, "High")),
        "High",
        np.where(
            df["selected_footfall"] >= df["sector_lookup"].map(extract_subkey_values(subsector_dict, "Medium")),
            "Medium",
            np.where(
                df["selected_footfall"] >= df["sector_lookup"].map(extract_subkey_values(subsector_dict, "Low")),
                "Low",
                None
            )
        )
    )


    # # Number requiring councelling
    df["num_req_counselling"] = np.where(
        df["sector_lookup"].map(extract_subkey_values(subsector_dict, "Counselling Est Measure")) == "Use Footfall", 
        df["num_of_staff_per_est"] + df["footfall_measure_per_est"],
        np.where(
            df["sector_lookup"].map(extract_subkey_values(subsector_dict, "Counselling Est Measure")) == "Per Unit",
            df["num_of_staff_per_est"] + df["footfall_measure_per_est"] * df["sector_lookup"].map(extract_subkey_values(subsector_dict, "TP Per Unit")),
            df["num_of_staff_per_est"] * (1 + df["sector_lookup"].map(extract_subkey_values(subsector_dict, "TP Per Employee")))
        )
    ) * np.where(df["sector/sector"] == "Residences", scalars["Counselling Res"], scalars["Counselling Std"])
    
    
    # # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # # LOADS / DISCOUNTS
    
    # Base frequency per establishment
    df["base_freq_per_est"] = df["sector/sector"].map(sector_rates_dict)


    
    
    # Calculate factors
    df["factor_state_country"] = np.where(
        df["country"] == "US", 
        df["state_code"].map(state_rates_dict), 
        df["country"].map(country_rates_dict)
    )

    df["factor_city_risk"] = df["city_risk"].map(city_risk_dict).fillna(0)
    df["factor_location"] = df["location"].map(location_dict)

    df["factor_subsector_loading"] = df["sector_lookup"].map(extract_subkey_values(subsector_dict, "Relativity"))
    df["factor_ease_of_access"] = df["east_of_access"].map(ease_of_access_dict)
    df["factor_enclosed_space"] = df["enclosed_space"].map(enclosed_space_dict)

    #SB Added 10/05/25    
    # Extract all values for High, Medium, and Low footfall
    footfall_High = df["sector_lookup"].map(extract_subkey_values(subsector_dict, "High")).values
    footfall_Medium = df["sector_lookup"].map(extract_subkey_values(subsector_dict, "Medium")).values
    footfall_Low = df["sector_lookup"].map(extract_subkey_values(subsector_dict, "Low")).values

    # Select footfall measure based on condition
    selected_footfall = np.where(df["footfall_measure"] == "Staff", df["num_of_staff_per_est"], df["footfall_measure_per_est"])

    # Create arrays for interpolation
    footfall_x = np.array([footfall_Low, footfall_Medium, footfall_High])
    footfall_y = np.tile(np.array(hx.params.footfall_factor["Rate"]), (len(df["sector_lookup"]), 1))

    # Interpolate values for each row
    df["factor_footfall"] = np.array([np.interp(footfall, footfall_x[:, i], footfall_y[i]) for i, footfall in enumerate(selected_footfall)])

        
    # Total Event Freq per Est.
    df["rate_multiplier"] = np.where(
        df["num_of_est"] == 0, 
        0, 
        (
            df["base_freq_per_est"]
            *df["factor_subsector_loading"]
            *df["factor_state_country"]
            *df["factor_city_risk"]
            *df["factor_location"]
            *df["factor_footfall"]
            *df["factor_ease_of_access"]
            *df["factor_enclosed_space"]
        )
    )

    # Total number of establishments
    total_est = sum(df["num_of_est"])

    # Sum over by sector
    num_est_by_subsector = df.groupby("sector/sub_sector")["num_of_est"].sum().reset_index()
    num_est_by_subsector["num_of_est"] = np.maximum(num_est_by_subsector["num_of_est"], 1) # Ensure 1 is min or else the apply falls down below
    num_est_by_subsector_dict = df_to_dict(num_est_by_subsector, "sector/sub_sector", "num_of_est")

    # Spread multliplier
    df["spread_multiplier_category"] = df["sector_lookup"].map(extract_subkey_values(subsector_dict, "Spread Discount Group"))
    spread_discount_factors_df = hx.params.spread_discount_factors
    
        
    df["spread_multiplier"] = df.apply(
        # The rater does not interpolate here, unlike in education
        lambda row: spread_discount_factors_df[
            spread_discount_factors_df["Num Est"] <= num_est_by_subsector_dict[row["sector/sub_sector"]]
        ][row["spread_multiplier_category"]].iloc[-1] if pd.notna(row["spread_multiplier_category"]) else None,
        axis=1
    )

    # Number of events
    df["num_events"] = df["rate_multiplier"] * df["num_of_est"] * df["spread_multiplier"]
    df["num_d_i"] = df["num_events"] * scalars["D&I Per Event"]
    df["num_deaths"] = df["num_d_i"] * scalars["Death Proportion"]
    df["num_injuries"] = df["num_d_i"] - df["num_deaths"]
    df["num_ppd_injuries"] = df["num_d_i"] * scalars["PPD Proportion"]
    
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # INFLATION ADJUSTED ECONOMIC COST

    # Note on inflation: Economic damages are intended to restore a person to their original position (Wage Inflation). 
    # Non-economic damages compensation to account for pain and suffering (Social Inflation)

    non_ed_court_award = hx.params.non_ed_court_award
    non_ed_court_award["Economic Inf"] = non_ed_court_award["Economic"] * rf.base_inflation
    non_ed_court_award["Non-economic Inf"] = non_ed_court_award["Non-economic"] * rf.social_inflation
    non_ed_court_award["Total Inf"] = non_ed_court_award["Economic Inf"] + non_ed_court_award["Non-economic Inf"]


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # COURT SETTLEMENTS PER CLAIMANT FOR LOSS COST

    # Cap per claimant
    # AC Note: Aggregate cap not included as very unlikely to trigger based on expected loss.
    total_cap = hx.params.state_liability_total_cap
    total_claimant_cap_dict = df_to_dict(total_cap, "state_code", "claimant_cap")
    
    non_econ_cap = hx.params.state_liability_non_econ_cap
    non_econ_claimant_cap_dict = df_to_dict(non_econ_cap, "state_code", "claimant_cap")

    # States which are not included in the table are uncapped so set the value as 1e20 for the np.min below
    df["cap_per_claimant_overall"] = df["state_code"].map(total_claimant_cap_dict).fillna(value=1e20)
    df["cap_per_claimant_non_economic"] = df["state_code"].map(non_econ_claimant_cap_dict).fillna(value=1e20)

    econ_award_typical = look_up("Cost of typical event", "Type", "Economic Inf", non_ed_court_award)
    non_econ_award_typical = look_up("Cost of typical event", "Type", "Non-economic Inf", non_ed_court_award)

    econ_award_6yr = look_up("Cost of 1 in 6.5 yr event", "Type", "Economic Inf", non_ed_court_award)
    non_econ_award_6yr = look_up("Cost of 1 in 6.5 yr event", "Type", "Non-economic Inf", non_ed_court_award)

    # Court settlement per claimant (post cap) - Typical
    df["court_settlement_typical_total"] = np.minimum(
        df["cap_per_claimant_overall"],
        np.minimum(df["cap_per_claimant_non_economic"], non_econ_award_typical) + econ_award_typical
    )

    # Court settlement per claimant (post cap) - 1 in 6.5 Yr
    # Total
    df["court_settlement_6yr_total"] = np.minimum(
        df["cap_per_claimant_overall"],
        np.minimum(df["cap_per_claimant_non_economic"], non_econ_award_6yr) + econ_award_6yr
    )

    # Court settlement per claimant - Final
    df["court_settlement_total"] = df["court_settlement_typical_total"] + (df["court_settlement_6yr_total"] - df["court_settlement_typical_total"])/6.5

    # Total Court settlement loss cost
    df["loss_cost_court_settlements"] = df["court_settlement_total"] * df["num_d_i"]


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # OTHER LOSS COST CALCS

    severity_dict = df_to_dict(hx.params.severity, "Component", "Cost of typical event")
    sub_limit_dict = df_to_dict(hx.params.sub_limit, "Endorsement", ["Incident", "Aggregate"])

    # Legal
    df["loss_cost_legal"] = df["num_d_i"] * severity_dict["Legal Costs"] * rf.base_inflation

    # Funeral
    df["loss_cost_funeral"] = np.minimum(
        df["num_deaths"] * severity_dict["Funeral"],
         sub_limit_dict["Funeral"]["Aggregate"]
    )

    # Counselling

    # This takes the # which require counselling and defaults to 100 if this is blank, then 
    # adds on the total # D&I
    df["loss_cost_counselling_est_observers_per_event"] = np.where(
        df["num_req_counselling"] == None,
        100,
        df["num_req_counselling"]
    ) + scalars["D&I Per Event"]

    df["loss_cost_counselling_total_cost_per_event_capped"] =  np.minimum(
        df["loss_cost_counselling_est_observers_per_event"] * severity_dict["Counselling"] * rf.base_inflation,
        sub_limit_dict["Counselling"]["Aggregate"]
    )

    df["loss_cost_counselling_exp_cost"] = df["loss_cost_counselling_total_cost_per_event_capped"] * df["num_events"]

    # Death & PPD benefit
    df["loss_cost_deaths"] = df["num_deaths"] * severity_dict["Death"]
    df["loss_cost_ppd"] = df["num_ppd_injuries"] * severity_dict["PPD"] * rf.base_inflation

    # Medical expenses
    df["loss_cost_medical"] = df["num_injuries"] * severity_dict["Medical Expenses"] * rf.base_inflation

    # Totals (excl. death)

    df["loss_cost_total_excl_death"] = (
        df["loss_cost_legal"]
        + df["loss_cost_funeral"]
        + df["loss_cost_counselling_exp_cost"]
        + df["loss_cost_ppd"]
        + df["loss_cost_medical"]
    )

     # Crisis Management
    df["loss_cost_crisis_mgt"] = df["num_events"] * severity_dict["Crisis Management"]

   
    df["loss_cost_total"] = np.where(
        df["num_of_est"] > 0,
        (
            df["loss_cost_total_excl_death"] 
            + df["loss_cost_deaths"] 
            + df["loss_cost_crisis_mgt"] 
            + df["loss_cost_court_settlements"]
        ),
        0
    )

    df["pol_term_multiplier"] = np.where(
        df["sector/sector"] == "Events",
        df["num_of_days"] / df["sector/sub_sector"].map(events_avg_days_dict),
        rf.policy_term
    )
        
    df["loss_cost_total_pol_term"] = np.where(
        (df["sector/sector"] == "Events") & (df["num_of_est"] > 0),
        np.maximum(
            df["footfall_band"].map(events_min_el_dict),
            df["loss_cost_total"] 
        ),
        df["loss_cost_total"]
    ) * df["pol_term_multiplier"]

    
    # Calculate minimum premiums ~~~~~
    # Minimum Premium is for $1m limit with no deductible. Scaled using ILF in layer calcs.
    df["min_premium"] = np.where(
        df["num_of_est"] > 0,
        df["sector_lookup"].map(extract_subkey_values(subsector_dict, "Minimum Premium")).fillna(0),
        0
    )

    # Conv to policy currency
    hxd.cds.min_premium_base.non_education = (np.max(df["min_premium"])) * fx


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # WRITE TO HXD

    # ILFs applied to total ground up loss
    hxd.cds.ground_up_expected_loss.non_education = df["loss_cost_total_pol_term"].sum()
    hxd.cds.ground_up_expected_loss.non_education_annualised = df["loss_cost_total"].sum()
    hxd.cds.exposure.aggregate.total_non_ed_est = total_est or 0
  
    
    # Update all NaN values to None before writing back to hxd
    df["num_req_counselling"] = np.where(df["num_req_counselling"].isna(), None, df["num_req_counselling"])
    df["footfall_measure"] = np.where(df["footfall_measure"].isna(), None, df["footfall_measure"])
    df["rate_multiplier"] = np.where(df["rate_multiplier"].isna(), None, df["rate_multiplier"])
    df["factor_footfall"] = np.where(df["factor_footfall"].isna(), None, df["factor_footfall"])

    # Write to hxd
    hxd_non_ed = hxd.cds.exposure.granular.non_education
    write_pd_to_hxd(df, hxd_non_ed, [
        "state_name",
        "factor_city_risk",
        "num_req_counselling",
        "footfall_measure",
        "footfall_band",
        "rate_multiplier"
    ])





