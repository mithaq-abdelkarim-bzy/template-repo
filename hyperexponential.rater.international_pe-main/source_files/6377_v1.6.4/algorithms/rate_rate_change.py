import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter
from algorithms.rate_constants import max_layers,discipline_list, ae_operation_list, mediatech_industry_list, mediatech_schedule_list
import json



def rate_change_buckets(hxd):
    buckets_eo = {
        "model": [], # start from expiry data priced with current model
        "exposure": discipline_list() + ae_operation_list() + [
            "cds/exposure/aggregate/eo_total_fees",
            "cds/rating_factors/eo_territory/input_value"],
        "risk_characteristics": [
            "cds/modifiers/eo_insurance_history/input_value",
            "cds/modifiers/eo_insurance_history/input_rel",
            "cds/modifiers/eo_claim_history/input_value",
            "cds/modifiers/eo_claim_history/input_rel",
            "cds/rating_factors/eo_prior_knowledge/input_value",
            "cds/rating_factors/eo_cost_included/input_value",
            "cds/modifiers/eo_schedule_modifier/input_value"
        ],
        "deductible": [
            "cds/layers/coverages/eo/deductible"
        ],
        "limit": [
            "cds/layers/coverages/eo/limit",
            "cds/layers/coverages/eo/aggregate_limit"
        ],
        "terms_conditions":[],
        "brokerage":[
            "cds/layers/coverages/eo/brokerage"
        ],
        "other": []        

    }


    buckets_mediatech = {
        "model": [], # start from expiry data priced with current model
        "exposure": mediatech_industry_list() + [
            "cds/exposure/aggregate/mediatech_revenue",
            "cds/rating_factors/mediatech_territory/input_value"],
        "risk_characteristics": [
            "cds/rating_factors/mediatech_prior_acts/coverage",
            "cds/rating_factors/mediatech_prior_acts/retroactive_date",
            "cds/rating_factors/mediatech_longevity/business_years",
            "cds/modifiers/mediatech_claim_experience/input_value",
            "cds/modifiers/mediatech_claim_experience/input_relativity",
            "cds/rating_factors/mediatech_cost_included/cost_included"
        ] + mediatech_schedule_list(),
        "deductible": [
            "cds/layers/coverages/mediatech/deductible"
        ],
        "limit": [
            "cds/layers/coverages/mediatech/limit",
            "cds/layers/coverages/mediatech/aggregate_limit"
        ],
        "terms_conditions":[
            "cds/modifiers/mediatech_bipd/input_value",
            "cds/modifiers/mediatech_bipd/input_relativity",
            "cds/layers/coverages/mediatech/additional_defense_limit"
        ],
        "brokerage":[
            "cds/layers/coverages/mediatech/brokerage"
        ],
        "other": []        
    }

    buckets_gl = {
        "model": [], # start from expiry data priced with current model
        "exposure": [
            "cds/exposure/granular/gl_exposure_info/occupation",
            "cds/exposure/granular/gl_revenue/tier_input",
            "cds/exposure/granular/gl_revenue/revenue_input",
            "cds/exposure/granular/gl_revenue/exposure_type"
            ],

        "risk_characteristics": [
            "cds/rating_factors/gl_loss/input_value",
            "cds/modifiers/gl_uw_adjustment/input_value",
        ],
        "deductible": [
            "cds/layers/coverages/gl/deductible"
        ],
        "limit": [
            "cds/layers/coverages/gl/limit"
        ],
        "terms_conditions":[
            "cds/rating_factors/gl_excess_primary/input_value",
            "cds/layers/coverages/gl/excess_of",
            "cds/layers/coverages/gl/defence_outside_limit"
        ],
        "brokerage":[
            "cds/layers/coverages/gl/brokerage"
        ],
        "other": []        
    }
    if hxd.cds.eo_coverage_selection:
        return buckets_eo
    elif hxd.cds.mediatech_coverage_selection:
        return buckets_mediatech
    elif hxd.cds.gl_coverage_selection:
        return buckets_gl


def rate_rate_change(hxd):

    if hxd.cds.rate_change.expiring_policy_option_id.selected is None:
        hxd.cds.rate_change.fetch_rarc_show_hide = False
    else:
        hxd.cds.rate_change.fetch_rarc_show_hide = True
    
    if hxd.cds.rate_change.fetch_rarc_show_hide_renewal:
        hxd.cds.rate_change.fetch_rarc_show_hide = True


    hxd.cds.rate_change.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id

    #hxd.cds.rate_change.expiring_policy_option_id.calculated = 128275
    
    # For layers not used in the pricing summary, the rate change is hidden
    num_layers = len(hxd.cds.layers)
    for index in range(1,max_layers+1):
        setattr(hxd.cds.rate_change, f"show_layer_{index}", True) if index <= num_layers else False

    coverage_selection = "None"

    if hxd.cds.eo_coverage_selection:
        coverage_selection = "eo"
    elif hxd.cds.mediatech_coverage_selection:
        coverage_selection = "mediatech"
    elif hxd.cds.gl_coverage_selection:
        coverage_selection = "gl"  

    for idx, layer in enumerate(hxd.cds.layers):
        if coverage_selection != "None":
            setattr(layer, "deal_status_record",getattr(getattr(getattr(layer, "coverages"), coverage_selection), "status"))
        else:
            setattr(layer, "deal_status_record",getattr(layer, "status")) 

    for idx, layer in enumerate(hxd.cds.layers):
        rc = layer.rate_change
        exp = rc.expiring_policy_info

        # the expiring layer selected in the comparison
        temp_layer = rc.expiring_layer
        expiring_premium_temp = hxd.cds.layers[temp_layer-1].rate_change.expiring_policy_info.expiring_premium
        has_expiring_data = hxd.cds.rate_change.has_expiring_data = (expiring_premium_temp is not None) 
        # Define conditions for function to run
        # Exit if condition is not satisfied
        if (not has_expiring_data) | (layer.quoted_premium is None) | (layer.quoted_premium == 0):
            return
        if expiring_premium_temp is not None:
            if expiring_premium_temp == 0:
                hx.errors.validation("Rate Change Renewal Option " + str(idx+1) +": Selected Expring Option has Empty Premium! Please change the Expiring Option or Change the Renewal Status on the 'Risk Information' tab")
                return        
        # --- Continue with the rate change calculation - populate expiring vs. renewal data
        
        rc.premium_policy_term_100pct.renewal = layer.quoted_premium
        # rc.premium_policy_term_beazley_share.renewal = layer.quoted_premium * layer.written_line
        
        #rc.premium_policy_term_100pct.expiring = exp.expiring_premium
        rc.premium_policy_term_100pct.expiring = expiring_premium_temp 
        # rc.premium_policy_term_beazley_share.expiring = exp.expiring_premium * exp.expiring_written_line

        rarc_change_list = [
            "exposure_change",
            "risk_characteristics_change",
            "limit_change",
            "deductible_change",
            "terms_conditions_change",
            "other_change",
            "brokerage_change"
        ]

        if (rc.exposure_change.model_calculated is not None) & (rc.risk_characteristics_change.model_calculated is not None) & (rc.deductible_change.model_calculated is not None) & (rc.limit_change.model_calculated  is not None) & (rc.terms_conditions_change.model_calculated  is not None) & (rc.brokerage_change.model_calculated is not None) & ( rc.other_change.model_calculated is not None):
            rc.total_change.model_calculated = rc.exposure_change.model_calculated * rc.risk_characteristics_change.model_calculated * rc.deductible_change.model_calculated * rc.limit_change.model_calculated * rc.terms_conditions_change.model_calculated * rc.brokerage_change.model_calculated * rc.other_change.model_calculated
            for item in rarc_change_list:
                rc_temp = getattr(rc, item)
                setattr(getattr(rc_temp, "uw_selected"), "calculated", getattr(rc_temp, "model_calculated"))
            rc.total_change.uw_selected= rc.exposure_change.uw_selected.selected * rc.risk_characteristics_change.uw_selected.selected *  rc.deductible_change.uw_selected.selected  * rc.limit_change.uw_selected.selected * rc.terms_conditions_change.uw_selected.selected * rc.brokerage_change.uw_selected.selected * rc.other_change.uw_selected.selected
            rc.risk_adjusted_rate_change.expiry_onlevel_premium_uw_selected  = rc.premium_policy_term_100pct.expiring  * rc.total_change.uw_selected
            if(rc.risk_adjusted_rate_change.expiry_onlevel_premium_uw_selected != 0):
                rc.risk_adjusted_rate_change.uw_selected = layer.quoted_premium / rc.risk_adjusted_rate_change.expiry_onlevel_premium_uw_selected
        # Validation for adding comment if rate change has been overridden for each layer.
        for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
            rc_vbl = getattr(layer.rate_change, item)
            if rc_vbl.uw_selected.is_overridden is True and rc_vbl.comments is None:
                hx.errors.validation(f"Rate Change: {(utils.title_rc(item))} has been overridden and no comment provided")  


   
    pass

def rate_rate_change_validation(hxd):
    layers = hxd.cds.layers
    rc = hxd.cds.rate_change

    for count, layer in enumerate(layers):
        # Valildation to ensure rate change is completed for bound layers
        if hxd.cds.standard_fields.is_rater_priced is True:
            if layer.rate_change.risk_adjusted_rate_change.uw_selected is None and layer.deal_status_record in ["Bound"]:
                hx.errors.validation(f"Rate change must be completed for 'Bound' - Option {count+1}")    

    # Validate layer mapping
    current_mapping = {}
    for idx, layer in enumerate(layers):
        current_mapping[str(idx+1)] = layer.rate_change.expiring_layer

    previous_mapping = json.loads(rc.layer_mapping) if rc.layer_mapping else current_mapping
    if current_mapping != previous_mapping:
        hx.errors.validation("Expring Option Input has changed! Please run 'Calculate Rate Change' again!")
        # task = "'Calculate Rate Change'" if rc.has_rarc_run else "'Fetch Expiring Data'"
        # rc.rarc_run_again_message = f"❗ Mapping of Expiring Layers to Renewal Layers has changed. Run {task} again ❗"
        # rc.rarc_message_show = True    
        return # Do not validate any further until the task is run again

    # Validate premiums
    if not rc.has_rarc_run:
        return

    for idx, layer in enumerate(layers):
        is_bm_different = (layer.benchmark_premium != layer.rate_change.temp_storage.benchmark_premium)
        if is_bm_different:
            hx.errors.validation(" Benchmark premiums have changed. Run the 'Calculate Rate Change' again!")
            break


    pass
