import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter
from algorithms.rate_constants import max_layers
from algorithms.rate_utilities import ratio

def rate_change_buckets():

    buckets = {
        "model": [], # Start from expiry data priced with current model
        "exposure": [
            # Coverage page
            "cds/layers/coverages/additional_death/is_covered",
            "cds/layers/coverages/terminal_illness/is_covered",
            "cds/layers/coverages/critical_illness/benefit",
            "cds/layers/coverages/critical_illness/benefit_amount_fixed",
            "cds/layers/coverages/critical_illness/benefit_amount_pct",
            "cds/layers/coverages/critical_illness/cap_amount",
            "cds/layers/coverages/critical_illness/cap_pct",
            # Premium page
            "cds/exposure/granular/lives/no_lives",
            "cds/exposure/granular/lives/salary",
            "cds/exposure/granular/lives/salary_multiple"

        ],
        "risk_characteristics": [
            # Coverage page
            "cds/layers/coverages/death/cover_type",
            "cds/layers/coverages/death/accidental_death_adj",
            "cds/layers/coverages/death/sick_affluence",
            "cds/layers/coverages/death/sick_weight_to_nationality",
            "cds/layers/coverages/death/accidental_death_rate",
            # Premium page
            "cds/exposure/granular/lives/sex",
            "cds/exposure/granular/lives/age_attained",
            "cds/exposure/granular/lives/nationality",
            "cds/exposure/granular/lives/location",
            "cds/exposure/granular/lives/region",
            "cds/exposure/granular/lives/occupation_code"
        ],
        "deductible": [
            "cds/layers/aggregate_deductible",
        ],
        "limit": [
            "cds/layers/aggregate_limit",
            "cds/layers/coverages/repat_exp/limit"
        ],
        "terms_conditions": [
            "cds/layers/coverages/critical_illness/is_covered",
            "cds/layers/coverages/repat_exp/is_covered"
        ],
        "brokerage": [
            "cds/layers/brokerage"
        ],
        "other": []
    }

    return buckets
    

def rate_rate_change(hxd):

    layer = hxd.cds.layers[0]
    rc = layer.rate_change
    exp = layer.rate_change.expiring_policy_info
    hxd.cds.rate_change.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id

    # Define conditions for function to run
    has_expiring_data = exp.expiring_premium is not None and exp.expiring_written_line is not None

    # Exit if condition is not satisfied
    if not has_expiring_data:
        return
    
    # --- Continue with the rate change calculation - calculate Beazley share premium
    rc.premium_policy_term_100pct.renewal = layer.quoted_premium or 0
    rc.premium_policy_term_beazley_share.renewal = rc.premium_policy_term_100pct.renewal * layer.written_line

    rc.premium_policy_term_100pct.expiring = exp.expiring_premium
    rc.premium_policy_term_beazley_share.expiring = exp.expiring_premium * exp.expiring_written_line

    rc.written_line.expiring = exp.expiring_written_line
    rc.written_line.renewal = layer.written_line

    # For layers not used in the pricing summary, the rate change is hidden
    num_layers = len(hxd.cds.layers)
    for index in range(1, max_layers+1):
        setattr(hxd.cds.rate_change, f"show_layer_{index}", True) if index <= num_layers else False
    
    # Calculate change for each bucket
    rebased_premium_model = rebased_premium_uw = exp.expiring_premium or 0

    for layer in hxd.cds.layers:
        # Allow for premium to exclude PC/NCB
        if layer.rate_change.is_from_inputs_only:
            quoted_premium = layer.totals.total_ex_pc_ncb.quoted_premium or 0
        else:
            quoted_premium = layer.quoted_premium or 0
        
        # Calculate UW overrides
        for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change", "brokerage_change"]:
            rc_vbl = getattr(layer.rate_change, item)
            rc_vbl.uw_selected.calculated = rc_vbl.model_calculated
            rebased_premium_model *= rc_vbl.model_calculated or 0
            rebased_premium_uw *= rc_vbl.uw_selected.selected or 0

            # Validate overrides if unexplained
            if rc_vbl.uw_selected.is_overridden is True and rc_vbl.comments is None:
                hx.errors.validation(f"Rate Change: {(utils.title_rc(item))} has been overridden and no comment provided")

        # Calculate final rate change with overrides
        renewal_premium = quoted_premium

        model_rarc = ratio(renewal_premium, rebased_premium_model, 1)
        final_rarc = ratio(renewal_premium, rebased_premium_uw, 1)

        layer.rate_change.rate_change.model_calculated = model_rarc
        layer.rate_change.risk_adjusted_rate_change.uw_selected = layer.rate_change.rate_change.uw_selected = final_rarc

        # Prompt user to run calcs again if premium changes
        if rc.is_from_inputs_only:
            is_bm_different = layer.rate_change.temp_storage.benchmark_premium and (layer.totals.total_ex_pc_ncb.benchmark_premium != layer.rate_change.temp_storage.benchmark_premium)
            is_quoted_different = layer.rate_change.temp_storage.quoted_premium and (layer.totals.total_ex_pc_ncb.quoted_premium != layer.rate_change.temp_storage.quoted_premium)
        else:
            is_bm_different = layer.rate_change.temp_storage.benchmark_premium and (layer.benchmark_premium != layer.rate_change.temp_storage.benchmark_premium)
            is_quoted_different = layer.rate_change.temp_storage.quoted_premium and (layer.quoted_premium != layer.rate_change.temp_storage.quoted_premium)
        
        rarc_message = ""
        rarc_message_show = False
        previous_bm_prem = "{:,.0f}".format(layer.rate_change.temp_storage.benchmark_premium or 0)
        previous_quoted_prem = "{:,.0f}".format(layer.rate_change.temp_storage.quoted_premium or 0)
        current_bm_prem = "{:,.0f}".format(layer.benchmark_premium or 0)
        current_quoted_prem = "{:,.0f}".format(quoted_premium)

        if is_bm_different and is_quoted_different:
            rarc_message = "Benchmark and quoted premiums have changed. Please run the rate change calculation again."
            rarc_message_show = True
        elif is_bm_different:
            rarc_message = f"Benchmark premium has changed from {previous_bm_prem} to {current_bm_prem}.\nPlease run the rate change calculation again."
            rarc_message_show = True
        elif is_quoted_different:
            rarc_message = f"Quoted premium has changed from {previous_quoted_prem} to {current_quoted_prem}.\nPlease run the rate change calculation again."
            rarc_message_show = True
        
        hxd.cds.rate_change.rarc_run_again_message = rarc_message
        hxd.cds.rate_change.rarc_message_show = rarc_message_show
        hxd.cds.rate_change.rarc_calcs_show = not rarc_message_show

        # Add validation error to prevent policy from being set to final
        if is_bm_different or is_quoted_different:
            hx.errors.validation("'Calculate Rate Change' in the Rate Change page must be run again.")
        

        



    



