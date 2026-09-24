import hx
import math

def check_model_weightings_sum_value(model_weighting_sum):
    if not math.isclose(model_weighting_sum, 1.0):
        hx.errors.validation("Model Weightings must add to 100%. Please revise the weighting allocation (Rating Summary tab).")


def check_model_weightings_no_experience(warning_path, weights, ulrs):
    mask = (ulrs == 0) & (weights > 0)
    if mask.any():
        warning_path.is_oe_msg_shown = True
        warning_path.is_there_global_message = True
    else:
        warning_path.is_oe_msg_shown = False


def check_tpi_year_value(tpi_year):
    if tpi_year is None:
        hx.errors.validation("A TPI Year (Rating Summary Tab) must be entered.")


def check_best_estimate_pre_pc_adj_change(hxd, pricing_adequacy_act_basis_df):
    is_empty    = pricing_adequacy_act_basis_df.empty
    is_invalid  = True if is_empty else not (pricing_adequacy_act_basis_df["best_estimate_pre_pc_adj"] == pricing_adequacy_act_basis_df["best_estimate_pre_pc_adj_ref"]).all()
    if is_invalid:
        hx.errors.validation("Profit Commission Calculation is not up-to-date, please run the calculation.")
        hxd.non_cds.global_fields.is_pc_msg_shown = True
        hxd.non_cds.global_fields.is_there_global_message = True
    else :
        hxd.non_cds.global_fields.is_pc_msg_shown = False       


# not used pb /jb agreed to deactivate in bbt scenario 6-feb-26
def check_best_estimate_pre_pc_adj_change_bbt(hxd, best_estimate_pre_pc_adj, best_estimate_pre_pc_adj_ref):
    if not (best_estimate_pre_pc_adj == best_estimate_pre_pc_adj_ref):
        hx.errors.validation("Profit Commission Calculation is not up-to-date, please run the calculation.")
        hxd.non_cds.global_fields.is_pc_msg_shown = True
        hxd.non_cds.global_fields.is_there_global_message = True
    else :
        hxd.non_cds.global_fields.is_pc_msg_shown = False       


def check_uw_adj_limits(uw_adj_series):
    condition = (uw_adj_series > 0.1) | (uw_adj_series < -0.1)
    if condition.any():
        hx.errors.validation("UW Adjustment (Rating Summary) values must be between 10% to -10%, please update it.")


def check_excel_produced(hxd):
    condition = not hxd.non_cds.excel_analysis.show_download
    if condition:
        hx.errors.validation("Excel Analysis File (Rationale page) needs to be run")


def check_case_pricing(hxd):
    # brokerage
    val = hxd.cds.rating_summary.case_pricing.brokerage
    condition = (val is None) 
    condition = condition if condition else (val <= 0)
    if condition:
        hx.errors.validation("Case Pricing - Brokerage (Rating Summary) must be entered and > 0.")

    # written_line
    val = hxd.cds.rating_summary.case_pricing.written_line
    condition = (val is None) 
    condition = condition if condition else (val <= 0)
    if condition:
        hx.errors.validation("Case Pricing - Written Line (Rating Summary) must be entered and > 0.")

    # premium
    val = hxd.cds.rating_summary.case_pricing.quoted_premium_100
    condition = (val is None) 
    condition = condition if condition else (val <= 0)
    if condition:
        hx.errors.validation("Case Pricing - Quoted Premium (Rating Summary) must be entered and > 0.")

    # bpi
    val = hxd.cds.rating_summary.case_pricing.bpi
    condition = (val is None) 
    condition = condition if condition else (val <= 0)
    if condition:
        hx.errors.validation("Case Pricing - BPI (Rating Summary) must be entered and > 0.")

    # tracker class
    val = hxd.cds.rating_summary.case_pricing.tracker_class
    condition = (val is None) 
    if condition:
        hx.errors.validation("Case Pricing - Tracker Class (Rating Summary) must be entered.")
