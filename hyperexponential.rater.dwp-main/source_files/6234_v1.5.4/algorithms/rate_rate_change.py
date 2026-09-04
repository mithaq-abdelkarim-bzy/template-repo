import hx, os, json, requests, math
import pandas as pd
import numpy as np
from operator import itemgetter
from copy import deepcopy
from algorithms.rate_utilities import title_rc, ratio, pd_df_from_hx_list, df_to_nested_list, transient_list_from_hx_list
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from algorithms.transient_hxd import init_transient_hxd


          

@hx.task
def rate_rate_change(hxd):
    layers = hxd.cds.layers
    rc = hxd.cds.rate_change
    rc.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id
    layer = hxd.cds.layers[0]
        
    # Write actual premiums back to hxd in rate_change node    
    layer.rate_change.premium_annualized_100pct.renewal = layer.quoted_premium_annualised
    layer.rate_change.premium_annualized_beazley_share.renewal = (layer.quoted_premium_annualised or 0) * (layer.written_line or 0)
    layer.rate_change.premium_policy_term_100pct.renewal = layer.quoted_premium
    layer.rate_change.premium_policy_term_beazley_share.renewal = (layer.quoted_premium or 0) * (layer.written_line or 0)
    
    # Calculate change for each bucket
    rebased_premium_model = rebased_premium_uw = layer.rate_change.premium_annualized_100pct.expiring or 0

    # Initialise list to check all changes are filled in
    rate_changes = []
    ms = hxd.model_state
    # Cumulatively apply rate changes, must be in same order as in rate change task 
    for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "brokerage_change", "other_change"]:
        # Calculate rebased premium based on % changes
        rc_vbl = getattr(layer.rate_change, item)
        rebased_premium_model *= rc_vbl.model_calculated or 1
        rebased_premium_uw *= rc_vbl.uw_selected.selected or 1

        # Add selected change to list
        rate_changes.append(rc_vbl.uw_selected.selected)
        
        # Validate overrides if unexplained
        if rc_vbl.uw_selected.is_overridden is True and rc_vbl.comments is None:
            hx.errors.validation(f"Rate Change: {(title_rc(item))} has been overridden and no comment provided")

    # Calculate final rate change with and without overrides
    renewal_premium = layer.quoted_premium_annualised
    model_rarc = ratio(renewal_premium, rebased_premium_model, 1)
    final_rarc = ratio(renewal_premium, rebased_premium_uw, 1)

    layer.rate_change.rate_change.model_calculated = model_rarc
    layer.rate_change.risk_adjusted_rate_change.uw_selected = layer.rate_change.rate_change.uw_selected = final_rarc

    # Suggestion for case pricing
    if hxd.cds.standard_fields.is_case_priced:
        layer.rate_change.risk_adjusted_rate_change_case_priced.uw_selected.calculated = ratio(
            layer.bpi_case_priced, 
            layer.rate_change.expiring_policy_info.expiring_bpi,
            if_undefined=1
        ) if layer.rate_change.expiring_policy_info.expiring_bpi else None


    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # VALIDATION
    
    # Valildation to ensure rate change is completed for bound layers (updated as only 1 layer)
    if hxd.cds.standard_fields.is_rater_priced:
        if any(change is None for change in rate_changes) and layer.status in ["Bound", "Post Bind Complete"]:
            hx.errors.validation(f"Rate change must be completed.")
            pass
    if hxd.cds.standard_fields.is_case_priced:
        if layer.rate_change.risk_adjusted_rate_change_case_priced.uw_selected.selected is None and layer.status in ["Bound", "Post Bind Complete"]:
            hx.errors.validation(f"Rate change must be completed")

    # Validate premiums
    if not rc.has_rarc_run:
        return
    
    if hxd.cds.standard_fields.is_rater_priced:
        is_bm_different = (layer.benchmark_premium != layer.rate_change.temp_storage.benchmark_premium)
        is_quoted_different = (layer.quoted_premium != layer.rate_change.temp_storage.quoted_premium)

        if is_bm_different and is_quoted_different:
            rc.rarc_run_again_message = "❗ Benchmark and quoted premiums have changed. Run the rate change calculation again ❗"
            rc.rarc_message_show = True
        elif is_bm_different:
            rc.rarc_run_again_message = f"❗ Benchmark premium has changed. Run the rate change calculation again ❗"
            rc.rarc_message_show = True
        elif is_quoted_different:
            rc.rarc_run_again_message = f"❗ Quoted premium has changed. Run the rate change calculation again ❗"
            rc.rarc_message_show = True

        if is_bm_different or is_quoted_different:
            hx.errors.validation("'Calculate Rate Change' in the Rate Change page must be run again.")
        



def expiring_policy_fetch_task(hxd, progress):

    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id = hxd.cds.rate_change.expiring_policy_option_id.selected #or 85244 # NOTE: use hardcoded ID for debugging if needed
    expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False)

    if expiring_response.status_code != 200:
        raise Exception(expiring_response.json())

    expiring_data = expiring_response.json()["data"]  

    return expiring_data



