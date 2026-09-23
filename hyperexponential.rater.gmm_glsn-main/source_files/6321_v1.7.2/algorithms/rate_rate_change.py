import hx
import pandas as pd
import numpy as np
import math as math
import json
from algorithms.rate_utilities import title_rc, ratio
from operator import itemgetter
from algorithms.rate_constants import max_layers, exposure_change_list, terms_and_conditions_change_list, deductible_change_list, limit_change_list , brokerage_change_list, risk_characteristics_change_list, model_change_list

def rate_change_buckets(hxd):

    buckets = {
        "model": model_change_list() + [], # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": exposure_change_list() + 
        [],
        "risk_characteristics": risk_characteristics_change_list() +
        [],
        "deductible": deductible_change_list() +
        [],
        "limit": limit_change_list() +
        [],
        "terms_conditions": terms_and_conditions_change_list() +           
        [],
        "brokerage": brokerage_change_list() +
        [],
        "other": []
    }

    return buckets

def rate_rate_change(hxd):
    layers = hxd.cds.layers
    rc = hxd.cds.rate_change
    # rc.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id
    #rc.expiring_policy_option_id.calculated = 42837
    
    # For layers not used in the pricing summary, the rate change is hidden
    num_layers = len(layers)
    rc.show_layer_1 = False
    for index in range(2,max_layers+1):
        setattr(hxd.cds.rate_change, f"show_layer_{index}", True) if index <= num_layers else False
    
    for idx, layer in enumerate(layers):        
        # Add renewal premium to table - NOTE: will have to be annualised if policy term is not one year
        # layer.rate_change.premium_annualized_100pct.renewal = layer.bound_premium
        #layer.rate_change.premium_annualized_beazley_share.renewal = layer.quoted_premium * (layer.written_line or 0)
        
        # Define expiring layers to compare to
        if (layer.rate_change.expiring_layer_dropdown == "Primary"):
            layer.rate_change.expiring_layer = 2
        elif (layer.rate_change.expiring_layer_dropdown == "Excess 1"):
            layer.rate_change.expiring_layer = 3
        elif (layer.rate_change.expiring_layer_dropdown == "Excess 2"):
            layer.rate_change.expiring_layer = 4
        elif (layer.rate_change.expiring_layer_dropdown == "Excess 3"):
            layer.rate_change.expiring_layer = 5
        elif (layer.rate_change.expiring_layer_dropdown == "Excess 4"):
            layer.rate_change.expiring_layer = 6
        elif (layer.rate_change.expiring_layer_dropdown == "Excess 5"):
            layer.rate_change.expiring_layer = 7
        elif (layer.rate_change.expiring_layer_dropdown == "Excess 6"):
            layer.rate_change.expiring_layer = 8
        elif (layer.rate_change.expiring_layer_dropdown == "Excess 7"):
            layer.rate_change.expiring_layer = 9
        elif (layer.rate_change.expiring_layer_dropdown == "Excess 8"):
            layer.rate_change.expiring_layer = 10
        elif (layer.rate_change.expiring_layer_dropdown == "Excess 9"):
            layer.rate_change.expiring_layer = 11   


        # Calculate change for each bucket
        rebased_premium_model = rebased_premium_uw = layer.rate_change.premium_annualized_100pct.expiring or 0

        # Initialise list to check all changes are filled in
        rate_changes = []

        for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "brokerage_change", "other_change"]:
            # Calculate rebased premium based on % changes
            rc_vbl = getattr(layer.rate_change, item)
            # rc_vbl.uw_selected.calculated = rc_vbl.model_calculated #IR note: now calculated in rate_change task instead.
            rebased_premium_model *= rc_vbl.model_calculated or 0
            rebased_premium_uw *= rc_vbl.uw_selected.selected or 0

            # Add selected change to list
            rate_changes.append(rc_vbl.uw_selected.selected)
            
            # Validate overrides if unexplained
            if idx != 0 and rc_vbl.uw_selected.is_overridden is True and (rc_vbl.comments is None or rc_vbl.comments == ""):
                hx.errors.validation(f"Rate Change: {(title_rc(item))} has been overridden and no comment provided")

        # Calculate final rate change with overrides
        renewal_premium = layer.rate_change.premium_annualized_100pct.renewal if layer.rate_change.premium_annualized_100pct.renewal is not None else layer.bound_premium
        layer.rate_change.premium_annualized_100pct.implied = rebased_premium_uw

        if renewal_premium is not None:
            model_rarc = ratio(renewal_premium, rebased_premium_model, 1)
            final_rarc = ratio(renewal_premium, rebased_premium_uw, 1)
        else:
            model_rarc = 1
            final_rarc = 1    
        
        layer.rate_change.rate_change.model_calculated = model_rarc
        layer.rate_change.risk_adjusted_rate_change.uw_selected = layer.rate_change.rate_change.uw_selected = final_rarc

        # Valildation to ensure rate change is completed for bound layers
        if hxd.cds.standard_fields.is_rater_priced:
            if any(change is None for change in rate_changes) and layer.status in ["Bound", "Post Bind Complete"]:
                hx.errors.validation(f"Rate change must be completed for bound layer {idx+1}")
        if hxd.cds.standard_fields.is_case_priced:
            if layer.rate_change.risk_adjusted_rate_change_case_priced.uw_selected.selected is None and layer.status in ["Bound", "Post Bind Complete"]:
                hx.errors.validation(f"Rate change must be completed for bound layer {idx+1}")
        
        
        if layer.bound_premium != layer.rate_change.premium_annualized_100pct.renewal:
            layer.rate_change.renewal_premium_warning = f"❗ Renewal Premium in Rate Change Sheet must equal Bound Premium in Rating Summary Sheet ❗"
            layer.rate_change.renewal_premium_warning_show = True
            

    # Validate layer mapping
    current_mapping = {}
    for idx, layer in enumerate(layers):
        current_mapping[str(idx+1)] = layer.rate_change.expiring_layer

    previous_mapping = json.loads(rc.layer_mapping) if rc.layer_mapping else current_mapping
    if current_mapping != previous_mapping:
        hx.errors.validation("Mapping of Expiring Layers to Renewal Layers is inconsistent with numbers shown in Rate Change")

        task = "'Calculate Rate Change'" if rc.has_rarc_run else "'Fetch Expiring Data'"
        rc.rarc_run_again_message = f"❗ Mapping of Expiring Layers to Renewal Layers has changed. Run {task} again ❗"
        rc.rarc_message_show = True
        
        return # Do not validate any further until the task is run again

    # Validate premiums
    if not rc.has_rarc_run:
        return

    for idx, layer in enumerate(layers):
        if idx != 0 and hxd.cds.layers[idx].show_row == True: 
            is_bm_different = (layer.benchmark_premium != layer.rate_change.temp_storage.benchmark_premium)
            is_bound_different = (layer.bound_premium != layer.rate_change.temp_storage.quoted_premium)
            is_bound_none = layer.bound_premium is None

            if is_bm_different and is_bound_different:
                rc.rarc_run_again_message = "❗ Benchmark and bound premiums have changed. Run the rate change calculation again ❗"
                rc.rarc_message_show = True
                break
            elif is_bm_different:
                if idx == 1:
                    rc.rarc_run_again_message = f"❗ Benchmark premium has changed on Primary Layer {idx-1}. Run the rate change calculation again ❗"
                    rc.rarc_message_show = True
                else:
                    rc.rarc_run_again_message = f"❗ Benchmark premium has changed on Excess Layer {idx-1}. Run the rate change calculation again ❗"
                    rc.rarc_message_show = True    
                break
            elif is_bound_none:
                if idx == 1:
                    rc.rarc_run_again_message = f"❗ No bound premium entered for Primary Layer. Enter a quote and run the rate change calculation again ❗"
                    rc.rarc_message_show = True
                else:
                    rc.rarc_run_again_message = f"❗ No bound premium entered for Excess Layer {idx-1}. Enter a quote and run the rate change calculation again ❗"
                    rc.rarc_message_show = True    
                break
            elif is_bound_different:
                if idx == 1:
                    rc.rarc_run_again_message = f"❗ Bound premium has changed on Primary Layer. Enter a quote and run the rate change calculation again ❗"
                    rc.rarc_message_show = True
                else:
                    rc.rarc_run_again_message = f"❗ Bound premium has changed on Excess Layer {idx-1}. Run the rate change calculation again ❗"
                    rc.rarc_message_show = True
                break
        
            if is_bm_different or is_bound_different:
                hx.errors.validation("'Calculate Rate Change' in the Rate Change page must be run again.")

    
        