import hx
import datetime
from math import prod
from algorithms import rate_constants as constants 
from algorithms.rate_utilities import look_up, look_up_with_bounds, factor_validation

def calc_schedule_rating_factor(hxd, state_info, results):
    asr = hxd.cds.layers[0].fid.admitted_schedule_rating
    
    if state_info["state_code"] == "GA":
        total_flex = (
            results.get("factor_selection_sponsor")
            + results.get("admitted_benefit")
            + results.get("admitted_litigation")
            + results.get("admitted_other")
            + results.get("admitted_expense")
        )
    else:
        total_flex = (
            results.get("factor_selection_sponsor")
            + results.get("admitted_benefit")
            + results.get("admitted_litigation")
            + results.get("admitted_other")
        )

    df_res = look_up(state_info["state_code"], "State", ["Basic Limits Min Before", "Basic Limits Min After", "Schedule Rating Min", "Schedule Rating Max"], hx.params.table_fid_admitted_applicabilities)

    max_credit = df_res["Schedule Rating Min"]
    max_debit = df_res["Schedule Rating Max"]
    asr.min.total_schedule_rating_modifier = max_credit
    asr.max.total_schedule_rating_modifier = max_debit

    schedule_rating_factor = (
        1 if total_flex == 0 
        else (max(1 + max_credit, min(1 + total_flex, 1 + max_debit)))
    )

    asr.factor_selection.total_schedule_rating_modifier = schedule_rating_factor - 1

    results["schedule_rating_factor"] = schedule_rating_factor

    # The below is only used for the unused section in the gmap calculations
    # results["min_premium_before"] = df_res["Basic Limits Min Before"]
    # results["min_premium_after"] = df_res["Basic Limits Min After"]