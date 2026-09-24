import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_pricing import interp_table_row
import algorithms.rate_utilities as utils

def admitted_excess_pricing(hxd):
    if shownby_conditions(hxd):
        admitted_premium_calculations(hxd)



def shownby_conditions(hxd):
    base_path = hxd.cds.admitted_excess
    # set out the conditional statements for the shownby tables in the view
    if (
        (hxd.cds.company_state is not None) and 
        (hxd.cds.uw_location == "US") and
        (hxd.cds.standard_fields.is_admitted_or_surplus.selected == "Admitted") and
        (base_path.is_primary_excess == "Excess") and
        (hxd.cds.admitted.conditions_met) and
        (hxd.model_state.show_after_landing_page)
    ):
        if hxd.cds.admitted.insurer == "BICI":  
            if (hx.params.bici_states_detail[(hx.params.bici_states_detail["State"] == hxd.cds.company_state)].iloc[0]["PlanType"] != "No Value"):
                base_path.conditions_met = True
                return True
        else:
            hx.errors.validation("Excess rating plan only approved for BICI")
    else: 
        base_path.conditions_met = False
        return False

def admitted_premium_calculations(hxd):
    base_path = hxd.cds.admitted_excess

    # Defining parameter tables
    df_type = hx.params.excess_state_type
    df_ilf = hx.params.excess_2_ilf
    df_singlelimit = hx.params.excess_4_single_limit
    df_rounding = hx.params.excess_5_rounding

    # Setting values from hxd
    primary_premium = 1 if base_path.exc_prim_premium.value is None else base_path.exc_prim_premium.value
    corrective_factor = 0 if base_path.exc_prim_rate_ade.value is None else base_path.exc_prim_rate_ade.value
    exc_ind_sec_factor = 0 if base_path.exc_ind_sec_factor.value is None else base_path.exc_ind_sec_factor.value
    exc_comp_spe_factor = 0 if base_path.exc_comp_spe_factor.value is None else base_path.exc_comp_spe_factor.value
    exc_liti_potential_factor = 0 if base_path.exc_liti_potential_factor.value is None else base_path.exc_liti_potential_factor.value
    product_three_sev_factors = exc_ind_sec_factor * exc_comp_spe_factor * exc_liti_potential_factor
    schedule_rating_factor = 0 if base_path.exc_fl_schedule_rating_factor.value is None else base_path.exc_fl_schedule_rating_factor.value

    # Pulling types
    type_row = df_type[df_type["State"]==hxd.cds.company_state].iloc[0]

    # Calling limit functions functions
    excess_attach_factor = excess_attach_factor_calculations(base_path, df_ilf, type_row["ILF Type"])
    basic_limit_factor = base_limit_factor_calculation(base_path, df_ilf, type_row["ILF Type"])

    exc_no_policies = base_path.exc_no_policies.value
    single_limit_factor = utils.look_up(exc_no_policies,"Number of", "Single Limit Factor", df_singlelimit, 1) if exc_no_policies is not None else 0

    # Calculates model premium
    model_premium = primary_premium * corrective_factor * (excess_attach_factor/basic_limit_factor) * product_three_sev_factors * schedule_rating_factor * single_limit_factor
    base_path.adm_exc_model_prem.value = model_premium

    # Pulls max rounding values
    rounding_rows = df_rounding[
        (df_rounding["Rated Premium Lower"] <= model_premium)
        & (df_rounding["Rated Premium Upper"] > model_premium)
    ]

    if rounding_rows.empty:
        # below minimum → pick first row
        if model_premium < df_rounding["Rated Premium Lower"].min():
            rounding_row = df_rounding.iloc[0]
        # above maximum → pick last row
        else:
            rounding_row = df_rounding.iloc[-1]
    else:
        rounding_row = rounding_rows.iloc[0]


    base_path.adm_exc_max_round_down.value = rounding_row["Round Down"]
    base_path.adm_exc_max_round_up.value = rounding_row["Round Up"]

    # Sets the minimum and maximum for all steps
    setup_steps(hxd, type_row["Primary Type"], type_row["Severity Type"], type_row["Schedule Rating"])

    # Rounded premium validation
    base_path.adm_exc_round_prem.value.calculated = base_path.adm_exc_model_prem.value
    hx.errors.validation("Insufficient information to calculate the Admitted Premium")  if base_path.adm_exc_round_prem.value.calculated == 0 else None

    if base_path.adm_exc_round_prem.value.selected is not None:
        rounding_upper = round(base_path.adm_exc_model_prem.value + rounding_row["Round Up"], 0)
        rounding_lower = round(base_path.adm_exc_model_prem.value - rounding_row["Round Down"],0)
        rounded_selected = round(base_path.adm_exc_round_prem.value.selected, 0)
        if (rounded_selected < rounding_lower) or (rounded_selected > rounding_upper):
            hx.errors.validation("Rounded premium is outside the rounding range")
    else:
        hx.errors.validation("Please enter an excess admitted rounded premium") 

    
def excess_attach_factor_calculations(hxd_path, df, ilf_type):
    excess_excess_limit = 0 if hxd_path.exc_excess_limit.value is None else hxd_path.exc_excess_limit.value
    excess_excess_attachment_point = 0 if hxd_path.exc_excess_attach.value is None else hxd_path.exc_excess_attach.value
    excess_primary_retention = 0 if hxd_path.exc_prim_retention.value is None else hxd_path.exc_prim_retention.value

    if ilf_type == "Limited":
        large_loss_potential_column = "Limited"
    else:
        large_loss_potential_column = "Average" if hxd_path.exc_large_loss.value is None else hxd_path.exc_large_loss.value

    f_lower = f"{large_loss_potential_column} Lower"
    f_upper = f"{large_loss_potential_column} Upper"

    beazley_limit_attach_point_retention = excess_excess_limit + excess_excess_attachment_point + excess_primary_retention

    # Validation
    if beazley_limit_attach_point_retention > 600e6:
        hx.errors.validation("Aggregate Limit + Attachment Point + Retention must be less than $600m")    
        excess_attachment_factor = 0
    else:
        beazley_attach_retention_interpolated_factor = interp_table_row(
            df, 
            beazley_limit_attach_point_retention, 
            "Attachment Point Lower", 
            "Attachment Point Upper", 
            f_lower, 
            f_upper, 
            0
        )

        attach_point_retention = excess_excess_attachment_point + excess_primary_retention
        attach_point_retention_interpolated_factor = interp_table_row(
            df, 
            attach_point_retention, 
            "Attachment Point Lower", 
            "Attachment Point Upper", 
            f_lower, 
            f_upper, 
            0
        )

        excess_attachment_factor = beazley_attach_retention_interpolated_factor - attach_point_retention_interpolated_factor

    return excess_attachment_factor

def base_limit_factor_calculation(hxd_path, df, ilf_type):

    primary_limit = 0 if hxd_path.exc_prim_limit.value is None else hxd_path.exc_prim_limit.value
    excss_primary_retention = 0 if hxd_path.exc_prim_retention.value is None else hxd_path.exc_prim_retention.value
    primary_limit_plus_retention = primary_limit + excss_primary_retention

    # Input validation
    if primary_limit < 10e3:
        hx.errors.validation("Primary Limit must be at least $10,000")

    if ilf_type == "Limited":
        large_loss_potential_column = "Limited"
    else:
        large_loss_potential_column = "Average" if hxd_path.exc_large_loss.value is None else hxd_path.exc_large_loss.value

    f_lower = f"{large_loss_potential_column} Lower"
    f_upper = f"{large_loss_potential_column} Upper"

    prim_limit_inter_factor = interp_table_row(
        df, 
        primary_limit_plus_retention, 
        "Attachment Point Lower", 
        "Attachment Point Upper", 
        f_lower, 
        f_upper, 
        0
    )

    prim_retention = 0 if hxd_path.exc_prim_retention.value is None else hxd_path.exc_prim_retention.value
    prim_ret_inter_factor = interp_table_row(
        df, 
        prim_retention, 
        "Attachment Point Lower", 
        "Attachment Point Upper", 
        f_lower, 
        f_upper, 
        0
    )

    base_limit_factor =  prim_limit_inter_factor - prim_ret_inter_factor

    base_limit_factor_output = 1 if base_limit_factor == 0 else base_limit_factor

    return base_limit_factor_output

def setup_steps(hxd, prim_type, sev_type, schedule_type):
    base_path = hxd.cds.admitted_excess 

    # Defining parameter tables
    df_prim_adj = hx.params.excess_1_primary_adj
    df_sev = hx.params.excess_3_severity
    df_schedule = hx.params.excess_3a_schedule
    
    # Primary Rate Adequacy Correction 
    prim_adj_row = df_prim_adj[df_prim_adj["State"] == prim_type].iloc[0]
    min_value = prim_adj_row["min"]
    max_value = prim_adj_row["max"]
    base_path.exc_prim_rate_ade.min = prim_adj_row["min"]
    base_path.exc_prim_rate_ade.max = prim_adj_row["max"]

    input_validation(min_value, max_value, base_path.exc_prim_rate_ade.value, "Primary Rate Adequacy Correction Value")

    ## Severity Factors ##
    df_sev = df_sev[(df_sev["State"] == sev_type)]

    # Industry/ Sector Factor
    risk_level = base_path.exc_ind_risk_level.value
    if risk_level is not None:
        # Changes column based on risk level
        sev_lower_col = f"{risk_level} - LB"
        sev_upper_col = f"{risk_level} - UB"

        sev_row = df_sev[df_sev["Severity Component"] == "Industry/ Sector Factor"].iloc[0]
        ind_sec_min = sev_row[sev_lower_col]
        ind_sec_max = sev_row[sev_upper_col] 
        base_path.exc_ind_sec_factor.min = ind_sec_min
        base_path.exc_ind_sec_factor.max = ind_sec_max

        input_validation(ind_sec_min, ind_sec_max, base_path.exc_ind_sec_factor.value, "Industry/ Sector Factor Value")


    # Company Specific Factor
    risk_level = base_path.exc_comp_spe_risk_level.value
    if risk_level is not None:
        sev_lower_col = f"{risk_level} - LB"
        sev_upper_col = f"{risk_level} - UB"

        sev_row = df_sev[df_sev["Severity Component"] == "Company Specific Factor"].iloc[0]
        comp_spe_min = sev_row[sev_lower_col]
        comp_spe_max = sev_row[sev_upper_col] 
        base_path.exc_comp_spe_factor.min = comp_spe_min
        base_path.exc_comp_spe_factor.max = comp_spe_max

        input_validation(comp_spe_min, comp_spe_max, base_path.exc_comp_spe_factor.value, "Company Specific Factor")

    # Litigation Potential Factor
    risk_level = base_path.exc_liti_potential_risk_level.value
    if risk_level is not None:
        sev_lower_col = f"{risk_level} - LB"
        sev_upper_col = f"{risk_level} - UB"

        sev_row = df_sev[df_sev["Severity Component"] == "Litigation Potential Factor"].iloc[0]
        lit_pot_min = sev_row[sev_lower_col]
        lit_pot_max = sev_row[sev_upper_col]
        base_path.exc_liti_potential_factor.min = lit_pot_min
        base_path.exc_liti_potential_factor.max = lit_pot_max

        input_validation(lit_pot_min, lit_pot_max, base_path.exc_liti_potential_factor.value, "Litigation Potential Factor Value")

    ## FL Schedule Rating Factor ##
    sch_row = df_schedule[df_schedule["State"] == schedule_type].iloc[0]
    sch_rat_min = sch_row["LB"]
    sch_rat_max = sch_row["UB"]
    base_path.exc_fl_schedule_rating_factor.min = sch_rat_min
    base_path.exc_fl_schedule_rating_factor.max = sch_rat_max

    input_validation(sch_rat_min, sch_rat_max, base_path.exc_fl_schedule_rating_factor.value, "FL Schedule Rating Factor Factor Value")


def input_validation(min, max, value, string):
    value = 0 if value is None else value
    if value > max or value < min:
        hx.errors.validation(f"{string} is less than {min} or greater than {max}")
        return False  # Indicate validation failure
    return True  # Indicate validation success
