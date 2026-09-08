##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################

###  1) 
###  2) 
###  3) 
###  4) 
###  5) 
###  6) 
###  7) 
###  8) 
###  9) 
### 10)
##############################################################################################################################





import hx
import pandas as pd
import numpy as np
import math as math
import json
from algorithms.rate_utilities import title_rc, ratio
from operator import itemgetter
from algorithms.rate_constants import max_layers

def rate_change_buckets(hxd):

    # -----------------------------------------------------------------------------
    # NOTE
    # As we need the rate change buckets to align with the PMD we have grouped
    # brokerage and other into 'other incl. brokerage' and allocated other node below. 
    # Brokerage will be calculated seperately in the rarc_task but not displayed standalone.
    # -----------------------------------------------------------------------------


    buckets_political = {
        "model": [], # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": [
            "cds/exposure/granular/political/country_exposure/country"
            , "cds/exposure/granular/political/country_exposure/sum_insured"
            , "cds/exposure/granular/political/country_exposure/excess"
            , "cds/exposure/granular/political/country_exposure/limit"

            , "cds/exposure/granular/political/coverage_matrix/mobile_assets/gov_action"
            , "cds/exposure/granular/political/coverage_matrix/mobile_assets/pol_violence"
            , "cds/exposure/granular/political/coverage_matrix/mobile_assets/cur_inconvertibility"
            , "cds/exposure/granular/political/coverage_matrix/mobile_assets/cont_relation_govt"
            , "cds/exposure/granular/political/coverage_matrix/fixed_assets/gov_action"
            , "cds/exposure/granular/political/coverage_matrix/fixed_assets/pol_violence"
            , "cds/exposure/granular/political/coverage_matrix/fixed_assets/cur_inconvertibility"
            , "cds/exposure/granular/political/coverage_matrix/fixed_assets/cont_relation_govt"
            , "cds/exposure/granular/political/coverage_matrix/lenders_interest/gov_action"
            , "cds/exposure/granular/political/coverage_matrix/lenders_interest/pol_violence"
            , "cds/exposure/granular/political/coverage_matrix/lenders_interest/cur_inconvertibility"
            , "cds/exposure/granular/political/coverage_matrix/lenders_interest/cont_relation_govt"           

            , "cds/exposure/granular/political/exposure_curve"
        ],
        "risk_characteristics": [
            "hx_core/inception_date"
            , "hx_core/expiry_date"

            , "cds/modifiers/political/override/industry"
            , "cds/modifiers/political/override/insured_quality"
            , "cds/modifiers/political/override/asset_composition"            
        ],
        "deductible": [
            "cds/layers/excess"
            , "cds/layers/deductible"
            , "cds/exposure/granular/political/coverage_matrix/deductible/pol_violence"
        ],
        "limit": [
            "cds/layers/limit"
            , "cds/exposure/granular/political/coverage_matrix/sublimit/pol_violence"
            , "cds/exposure/granular/political/coverage_matrix/sublimit/cur_inconvertibility"
        ],
        "terms_conditions": [],
        "other": [
            "cds/layers/brokerage"
        ]
    }


    buckets_crcf = {
        "model": [], # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": [
            "cds/risk_info/crcf_country"
            , "cds/exposure/granular/crcf/exposure_profile/month_1"
            , "cds/exposure/granular/crcf/exposure_profile/month_2"
            , "cds/exposure/granular/crcf/exposure_profile/month_3"
            , "cds/exposure/granular/crcf/exposure_profile/month_4"
            , "cds/exposure/granular/crcf/exposure_profile/month_5"
            , "cds/exposure/granular/crcf/exposure_profile/month_6"
            , "cds/exposure/granular/crcf/exposure_profile/month_7"
            , "cds/exposure/granular/crcf/exposure_profile/month_8"
            , "cds/exposure/granular/crcf/exposure_profile/month_9"
            , "cds/exposure/granular/crcf/exposure_profile/month_10"
            , "cds/exposure/granular/crcf/exposure_profile/month_11"
            , "cds/exposure/granular/crcf/exposure_profile/month_12"
        ],
        "risk_characteristics": [
            "hx_core/inception_date"
            , "hx_core/expiry_date"

            , "cds/exposure/granular/crcf/pre_shipment_risk"
            , "cds/exposure/granular/crcf/pre_shipment_amt"

            , "cds/modifiers/crcf/rating_source"
            , "cds/modifiers/crcf/rating_corporate"            
            , "cds/modifiers/crcf/override/grade"
            , "cds/modifiers/crcf/override/lgd"
            , "cds/modifiers/crcf/override/uw_adj"
        ],
        "deductible": [
            "cds/layers/excess"
            , "cds/layers/deductible"
        ],
        "limit": [
            "cds/layers/limit"
        ],
        "terms_conditions": [],
        "other": [
            "cds/layers/brokerage"
        ]
    }

    buckets = buckets_crcf if hxd.cds.product in {'Contract Frustration','Credit Risk'} else buckets_political

    return buckets

def rate_rate_change(hxd):
    layers = hxd.cds.layers
    rc = hxd.cds.rate_change
    rc.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id
    
    # For layers not used in the pricing summary, the rate change is hidden
    num_layers = len(layers)
    for index in range(1,max_layers+1):
        setattr(hxd.cds.rate_change, f"show_layer_{index}", True) if index <= num_layers else False
    
    annualise_renewal = 12 / (hxd.cds.rating_factors.policy_term or 12)

    for idx, layer in enumerate(layers):        
        
        rc_prem = layer.rate_change.premium
        # Add renewal premium to table - NOTE: will have to be annualised if policy term is not one year
        rc_prem.line_100pct.annualised.renewal  = layer.quoted_premium * annualise_renewal /  (layer.written_line or 1) 
        rc_prem.beazley_line.annualised.renewal = layer.quoted_premium * annualise_renewal

       
        # Calculate change for each bucket
        rebased_premium_model = rebased_premium_uw = rc_prem.line_100pct.annualised.expiring or 0

        # Initialise list to check all changes are filled in
        rate_changes = []

        for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
            # Calculate rebased premium based on % changes
            rc_vbl = getattr(layer.rate_change, item)                     
            # rc_vbl.uw_selected.calculated = rc_vbl.model_calculated       ### THIS LINE IS NOW DONE THROUGH ASYNC RARC_TASK SO WE CAN CLEAR IT ON RENEWAL VIA ASYNC WITHOUT CONFLICTS
            rebased_premium_model *= rc_vbl.model_calculated or 0
            rebased_premium_uw *= rc_vbl.uw_selected.selected or 0

            # Add selected change to list
            rate_changes.append(rc_vbl.uw_selected.selected)
            
            # Validate overrides if unexplained
            if rc_vbl.uw_selected.is_overridden is True and rc_vbl.comments is None:
                hx.errors.validation(f"Rate Change: {(title_rc(item))} has been overridden and no comment provided")

        # Calculate final rate change with overrides
        renewal_premium = layer.quoted_premium * annualise_renewal /  (layer.written_line or 1) 

        model_rarc = ratio(renewal_premium, rebased_premium_model, 1)
        final_rarc = ratio(renewal_premium, rebased_premium_uw, 1)

        layer.rate_change.rate_change.model_calculated = model_rarc
        layer.rate_change.risk_adjusted_rate_change = layer.rate_change.rate_change.uw_selected = final_rarc

        # For PMD reporting
        brokerage_change = layer.rate_change.brokerage_change.model_calculated or 1
        layer.rate_change.risk_adjusted_rate_change_gross_for_reporting = final_rarc * brokerage_change

        # Valildation to ensure rate change is completed for bound layers
        if hxd.cds.standard_fields.is_rater_priced:
            if any(change is None for change in rate_changes) and layer.status in ["Bound", "Post Bind Complete"]:
                hx.errors.validation(f"Rate change must be completed for bound layer {idx+1}")
        if hxd.cds.standard_fields.is_case_priced:
            if layer.rate_change.risk_adjusted_rate_change_case_priced is None and layer.status in ["Bound", "Post Bind Complete"]:
                hx.errors.validation(f"Rate change must be completed for bound layer {idx+1}")

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
        is_bm_different     = (layer.benchmark_premium_annualised != layer.rate_change.temp_storage.benchmark_premium)
        is_quoted_different = (layer.quoted_premium_annualised    != layer.rate_change.temp_storage.quoted_premium)

        if is_bm_different and is_quoted_different:
            rc.rarc_run_again_message = "❗ Benchmark and quoted premiums have changed. Run the rate change calculation again ❗"
            rc.rarc_message_show = True
            break
        elif is_bm_different:
            rc.rarc_run_again_message = f"❗ Benchmark premium has changed on Layer {idx+1}. Run the rate change calculation again ❗"
            rc.rarc_message_show = True
            break
        elif is_quoted_different:
            rc.rarc_run_again_message = f"❗ Quoted premium has changed on Layer {idx+1}. Run the rate change calculation again ❗"
            rc.rarc_message_show = True
            break

    if is_bm_different or is_quoted_different:
        hx.errors.validation("'Calculate Rate Change' in the Rate Change page must be run again.")
        