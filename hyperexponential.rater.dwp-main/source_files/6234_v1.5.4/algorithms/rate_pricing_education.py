import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import pd_df_from_hx_list, df_to_dict, write_pd_to_hxd, look_up, ratio, interp2d_agg_factors, extract_subkey_values
from algorithms import parameter_tables_schema as params
from operator import itemgetter

def rate_pricing_education(hxd):

    # Shortcuts
    rf = hxd.cds.rating_factors
    fx_rates = params.fx_rates.df()

    # Main exposure table
    df = pd_df_from_hx_list(hxd.cds.exposure.granular.education).fillna(0)
    fx = look_up(hxd.cds.currencies.source_currency, "ccy", "fx_rate", fx_rates, if_not_found=1)

    # Create dictionaries from parameter tables
    state_code_name_dict = df_to_dict(hx.params.lst_state_lookup, "State Code", "State Name")
    country_rates_dict = df_to_dict(hx.params.country_rates, "Country", "Rate")
    state_rates_dict = df_to_dict(hx.params.state_rates, "State", "Rate")
    city_risk_dict = df_to_dict(hx.params.city_risk_factor, "City Risk", "Rate")
    school_grade_dict = df_to_dict(hx.params.school_grade_factor, "Field", "Relativity")
    school_type_dict = df_to_dict(hx.params.school_type_factor, "Field", "Relativity")
    boarding_day_dict = df_to_dict(hx.params.boarding_day_factor, "Field", "Relativity")
    location_dict = df_to_dict(hx.params.location_factor, "Field", "Relativity")
    school_sex_dict = df_to_dict(hx.params.school_sex_factor, "Field", "Relativity")
  
    scalars = df_to_dict(hx.params.scalar_parameters, "Field", "Parameter")
    
    # Map state name from code and write back to hxd
    df["state_name"] = np.where(
        df["country"] == "US", 
        df["state_code"].map(state_code_name_dict).fillna(value=""),
        None
    )
    
    # Number requiring councelling
    df["num_req_counselling"] = np.where(
        df["num_students"] + df["num_employees"] > 0, 
        (df["num_students"] + df["num_employees"]) * scalars["Counselling Std"],
        None
    )


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # LOADS / DISCOUNTS
    
    # Calculate factors
    df["factor_state_country"] = np.where(
        df["country"] == "US", 
        df["state_code"].map(state_rates_dict), 
        df["country"].map(country_rates_dict)
    )
    df["factor_city_risk"] = df["city_risk"].map(city_risk_dict).fillna(0)
    df["factor_school_grade"] = df["school_grade"].map(school_grade_dict)
    df["factor_type"] = df["school_type"].map(school_type_dict)
    df["factor_boarding_day"] = df["boarding_day"].map(boarding_day_dict)
    df["factor_student_teacher_ratio"] = np.minimum(
        scalars["STRateCap"],
        (scalars["STCParameter"] * np.exp(
            scalars["STBParameter"] * (df["num_students"] / df["num_employees"])
        ))
    )
    df["factor_location"] = df["location"].map(location_dict)
    df["factor_school_sex"] = df["sex_of_school"].map(school_sex_dict)
    
    # Multiply together for main factor
    df["rate_multiplier"] = np.where(
        df["num_schools"] == 0, 
        0, 
        (
            df["factor_state_country"]
            *df["factor_city_risk"]
            *df["factor_school_grade"]
            *df["factor_type"]
            *df["factor_boarding_day"]
            *df["factor_student_teacher_ratio"]
            *df["factor_location"]
            *df["factor_school_sex"]
        )
    )

    df["base_d_i_per_student"] = df["rate_multiplier"] * scalars["Ed Base Rate"]

    # Spread multliplier    
    total_schools = sum(df["num_schools"])
    avg_events_per_school = (df["num_students"] * df["base_d_i_per_student"]).sum() / (scalars["D&I Per Event"] * total_schools) if total_schools > 0 else 0
    
    spread_tbl = hx.params.spread_discount_events
    spread_discount_group = spread_tbl[spread_tbl["Num events per school"] <= avg_events_per_school]["Spread Multiplier Group"].iloc[-1]
    spread_multiplior = np.interp(
        total_schools, 
        hx.params.spread_discount_factors["Num Est"], 
        hx.params.spread_discount_factors[spread_discount_group]
    )

    # Number of events
    df["num_d_i"] = np.where(df["num_schools"] > 0, df["num_students"] * df["base_d_i_per_student"] * spread_multiplior, 0)
    df["num_deaths"] = df["num_d_i"] * scalars["Death Proportion"]
    df["num_injuries"] = df["num_d_i"] * scalars["Injury Proportion"]
    df["num_ppd_injuries"] = df["num_d_i"] * scalars["PPD Proportion"]
    df["events_per_student"] = df["base_d_i_per_student"] * (
        scalars["Event Freq Factor"] / df["factor_student_teacher_ratio"]
        ) * df["num_schools"] * spread_multiplior
    df["num_events"] = df["events_per_student"] * df["num_students"] / df["num_schools"]


    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # INFLATION ADJUSTED ECONOMIC COST

    # Note on inflation: Economic damages are intended to restore a person to their original position (Wage Inflation). 
    # Non-economic damages compensation to account for pain and suffering (Social Inflation)

    ed_court_award = hx.params.ed_court_award
    ed_court_award["Economic Inf"] = ed_court_award["Economic"] * hxd.cds.rating_factors.base_inflation
    ed_court_award["Non-economic Inf"] = ed_court_award["Non-economic"] * hxd.cds.rating_factors.social_inflation
    ed_court_award["Total Inf"] = ed_court_award["Economic Inf"] + ed_court_award["Non-economic Inf"]


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

    econ_award_typical = look_up("Cost of typical event", "Type", "Economic Inf", ed_court_award)
    non_econ_award_typical = look_up("Cost of typical event", "Type", "Non-economic Inf", ed_court_award)

    econ_award_6yr = look_up("Cost of 1 in 6.5 yr event", "Type", "Economic Inf", ed_court_award)
    non_econ_award_6yr = look_up("Cost of 1 in 6.5 yr event", "Type", "Non-economic Inf", ed_court_award)

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
    df["loss_cost_legal"] = df["num_d_i"] * severity_dict["Legal Costs"] * hxd.cds.rating_factors.base_inflation

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
    ) + df["num_d_i"]

    df["loss_cost_counselling_total_cost_per_event_capped"] =  np.minimum(
        df["loss_cost_counselling_est_observers_per_event"] * severity_dict["Counselling"] * hxd.cds.rating_factors.base_inflation,
        sub_limit_dict["Counselling"]["Incident"]
    )

    df["loss_cost_counselling_exp_cost"] = df["loss_cost_counselling_total_cost_per_event_capped"] * df["num_events"]

    # Death & PPD benefit
    df["loss_cost_deaths"] = df["num_deaths"] * severity_dict["Death"]
    df["loss_cost_ppd"] = df["num_ppd_injuries"] * severity_dict["PPD"] * hxd.cds.rating_factors.base_inflation

    # Medical expenses
    df["loss_cost_medical"] = df["num_injuries"] * severity_dict["Medical Expenses"] * hxd.cds.rating_factors.base_inflation

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
        df["num_schools"] > 0,
        (
            df["loss_cost_total_excl_death"] 
            + df["loss_cost_deaths"] 
            + df["loss_cost_crisis_mgt"] 
            + df["loss_cost_court_settlements"]
        ),
        0
    )

    df["loss_cost_total_pol_term"] = df["loss_cost_total"] * rf.policy_term

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # WRITE TO HXD

    # Rating factors can be applied to total loss cost now
    hxd.cds.ground_up_expected_loss.education = df["loss_cost_total_pol_term"].sum()
    hxd.cds.ground_up_expected_loss.education_annualised = df["loss_cost_total"].sum()
    hxd.cds.exposure.aggregate.total_schools = total_schools or 0    
    
    
    # Set min premium (in policy currenty)
    # Minimum Premium is for $1m limit with no deductible. Scaled using ILF in layer calcs.
    hxd.cds.min_premium_base.education = scalars["Ed Min Premium"] * fx if total_schools > 0 else 0
    
    # Update all NaN values to None before writing back to hxd
    df["num_req_counselling"] = np.where(df["num_req_counselling"].isna(), None, df["num_req_counselling"])
    df["rate_multiplier"] = np.where(df["rate_multiplier"].isna(), None, df["rate_multiplier"])

    # Write df to hxd
    write_pd_to_hxd(df, hxd.cds.exposure.granular.education, [
        "state_name", 
        "factor_city_risk", 
        "num_req_counselling",
        "rate_multiplier"
    ])


    


