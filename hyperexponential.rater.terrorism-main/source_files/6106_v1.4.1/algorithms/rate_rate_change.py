##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################

###  1) check line 225 CPR commented out so could assign by task and thereby clear out overrides
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
import algorithms.rate_utilities as utils
from operator import itemgetter
from algorithms.rate_constants import max_layers
from algorithms.rate_utilities import ratio, one_layer
from algorithms.data_schema.sch_rater_defined import coverages_dict

def save_lists_for_rate_change(hxd):
    expo = hxd.cds.exposure.granular
    
    hxd.rate_change.countries = json.dumps(
        [{
            "country": c.country,
            "proxy_rating_country": c.proxy_rating_country,
            "rated_country": c.rated_country,
            "country_code_original": c.country_code_original,
            "country_code": c.country_code,
            "no_of_locations": c.no_of_locations,
            "pml": c.pml,
            "coverage": c.coverage,
            "limit": c.limit,
            "excess": c.excess,
            "subcoverage": c.subcoverage,
            "sublimit": c.sublimit,
            "deductible": c.deductible,
            "total_sum_insured": c.total_sum_insured,
            "bi_sum_insured": c.bi_sum_insured,
            "pd_sum_insured": c.pd_sum_insured,
            "liability_risk": c.liability_risk,
            "attritional_risk": c.attritional_risk,
            "geog_risk": c.geog_risk,
            "location_cat_risk": c.location_cat_risk,
            "political": c.political,
            "terrorism_raw": c.terrorism_raw,
            "labour_strikes": c.labour_strikes,
            "protests_riots": c.protests_riots,
            "interstate_war": c.interstate_war,
            "civil_war": c.civil_war,
            "civil_unrest": c.civil_unrest,
            "war": c.war,
            "terrorism": c.terrorism,
            "selected_sum_insured": c.selected_sum_insured,
            "warning": c.warning,
            "civil_unrest_roe_calculated": c.civil_unrest_roe_calculated,
            "civil_unrest_roe_selected": c.civil_unrest_roe_selected,
            "war_roe_calculated": c.war_roe_calculated,
            "war_roe_selected": c.war_roe_selected,
            "terrorism_roe_calculated": c.terrorism_roe_calculated,
            "terrorism_roe_selected": c.terrorism_roe_selected,
            "civil_unrest_uw_adj": c.civil_unrest_uw_adj,
            "war_uw_adj": c.war_uw_adj,
            "terrorism_uw_adj": c.terrorism_uw_adj,
            "override_civil_unrest": c.override_civil_unrest,
            "override_war": c.override_war,
            "override_terrorism": c.override_terrorism,
            "selected_civil_unrest": c.selected_civil_unrest,
            "selected_war": c.selected_war,
            "selected_terrorism": c.selected_terrorism,
            "has_civil_unrest": c.has_civil_unrest,
            "has_war": c.has_war,
            "has_terrorism": c.has_terrorism,
            "country_cvg_subcvg": c.country_cvg_subcvg,
        } for c in expo.countries]
    )
    pass

def rate_change_buckets():

    buckets = {
        "model": [], # Start from expiry data priced with current model
        "exposure": [
            # Allow for correct term calculation
            "hx_core/inception_date",
            "hx_core/expiry_date",
            # Countries
            "cds/exposure/granular/countries/country",
            "cds/exposure/granular/countries/proxy_rating_country",
            "cds/exposure/granular/countries/country_cvg_subcvg",
            "cds/exposure/granular/countries/no_of_locations",
            "cds/exposure/granular/countries/pml",
            "cds/exposure/granular/countries/total_sum_insured",
            "cds/exposure/granular/countries/bi_sum_insured",
            "cds/exposure/granular/countries/pd_sum_insured",
            # NOTE: including coverage here to make country_cvg_subcvg consistent
            "cds/exposure/granular/countries/coverage",
            "cds/exposure/granular/countries/subcoverage",
            # Policy details - allow for overrides
            "cds/exposure/aggregate/total_sum_insured",
            "cds/exposure/aggregate/bi_sum_insured",
            "cds/exposure/aggregate/pd_sum_insured",
            "cds/currencies/source_currency",
        ],
        "risk_characteristics": [
            # IHS Data
            "ihs_countries_retrieved",
            "cds/exposure/granular/countries/political",
            "cds/exposure/granular/countries/terrorism_raw",
            "cds/exposure/granular/countries/labour_strikes",
            "cds/exposure/granular/countries/protests_riots",
            "cds/exposure/granular/countries/interstate_war",
            "cds/exposure/granular/countries/civil_war",
            # Countries
            "cds/exposure/granular/countries/liability_risk",
            "cds/exposure/granular/countries/attritional_risk",
            "cds/exposure/granular/countries/geog_risk",
            "cds/exposure/granular/countries/location_cat_risk",
            # Risk adjustments
            "cds/layers/risk_adjustments/security/level",
            "cds/layers/risk_adjustments/security/override",
            "cds/layers/risk_adjustments/industry/level",
            "cds/layers/risk_adjustments/industry/override",
            "cds/layers/risk_adjustments/policy/level",
            "cds/layers/risk_adjustments/policy/override",
            # Construction
            "cds/layers/coverages/construction/years/build_up_override",
            # Old IHS Score adjustments - NOTE: including these as they'll have to be cleared when renewing a migrated policy
            "cds/layers/risk_adjustments/ihs_score/level",
            "cds/layers/risk_adjustments/ihs_score/override",
            "model_state/is_migrated",                       # this should allow the model to switch ihs approaches
            # New IHS Score adjustments
            "cds/exposure/granular/countries/override_civil_unrest",
            "cds/exposure/granular/countries/override_war",
            "cds/exposure/granular/countries/override_terrorism",
        ],
        "deductible": [
            "cds/exposure/granular/countries/excess",
            "cds/exposure/granular/countries/deductible",
            # Policy details - allow for overrides
            "cds/exposure/aggregate/policy_excess",
            "cds/exposure/aggregate/policy_deductible",
        ],
        "limit": [
            "cds/exposure/granular/countries/limit",
            "cds/exposure/granular/countries/sublimit",
            # Policy details - allow for overrides
            "cds/exposure/aggregate/policy_limit",
            "cds/exposure/aggregate/policy_sublimit",
        ],
        "terms_conditions": [
            # Construction
            "cds/layers/coverages/construction/is_covered",
            # Policy details
            "cds/exposure/aggregate/details/limit_type",
            "cds/exposure/aggregate/details/bi_wait_period",
            "cds/exposure/aggregate/details/bi_indemnity_period",
            "cds/exposure/aggregate/details/contingent_bi",
            "cds/exposure/aggregate/details/aggregate_usage",
        ],
        # "brokerage": [

        # ],

        "other": [
            "cds/layers/brokerage"
        ]
    }

    return buckets


def rate_rate_change(hxd, term_factor=1):
    layers = hxd.cds.layers
    rc = hxd.cds.rate_change
    sf = hxd.cds.standard_fields

    # layer, cvg = one_layer(hxd)
    # rc = layer.rate_change
    # exp = layer.rate_change.expiring_policy_info

    if not hxd.cds.standard_fields.is_renewal:
        return

    rc.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id

    # For layers not used in the pricing summary, the rate change is hidden
    num_layers = len(hxd.cds.layers)
    for index in range(1, max_layers+1):
        test = False if index > num_layers else hxd.cds.rate_change.has_fetch_run
        setattr(hxd.cds.rate_change, f"show_layer_{index}", test)
    

    # --- Continue with the rate change calculation - calculate Beazley share premium
    for idx, layer in enumerate(layers):        
        
        rc_lay  = layer.rate_change
        rc_prem = layer.rate_change.premium
        rc_exp = layer.rate_change.expiring_policy_info

        # add written line to table
        rc_lay.written_line.expiring            = rc_exp.expiring_written_line
        rc_lay.written_line.renewal             = layer.written_line

        # Add renewal premium to table
        rc_prem.line_100pct.annualised.renewal   = (layer.quoted_premium_annualised or 0)   /  (rc_lay.written_line.renewal or 1) 
        rc_prem.beazley_line.annualised.renewal  = rc_prem.line_100pct.annualised.renewal   *  (rc_lay.written_line.renewal or 0)

        rc_prem.line_100pct.policy_term.renewal  = (layer.quoted_premium or 0)              /  (rc_lay.written_line.renewal or 1) 
        rc_prem.beazley_line.policy_term.renewal = rc_prem.line_100pct.policy_term.renewal  *  (rc_lay.written_line.renewal or 0) 

        # handled within async task
        # rc_prem.line_100pct.annualised.expiring  = (rc_exp.expiring_premium_annualised or 0)/  (rc_lay.written_line.expiring or 1) 
        # rc_prem.beazley_line.annualised.expiring = rc_prem.line_100pct.annualised.expiring  *  (rc_lay.written_line.expiring or 0) 

        # rc_prem.line_100pct.policy_term.expiring = (rc_exp.expiring_premium or 0)           /  (rc_lay.written_line.expiring or 1) 
        # rc_prem.beazley_line.policy_term.expiring= rc_prem.line_100pct.policy_term.expiring *  (rc_lay.written_line.expiring or 0) 

        # Calculate change for each bucket
        rebased_premium_model = rebased_premium_uw  = rc_prem.line_100pct.annualised.expiring_override or rc_prem.line_100pct.annualised.expiring or 0 # CUSTOM ALLOW AN EXPIRING OVERRIDE PER AC request July-25 & EXPIRING MDOEL

        # Initialise list to check all changes are filled in
        rate_changes = []

        for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
            # Calculate rebased premium based on % changes
            rc_vbl = getattr(layer.rate_change, item)
            # Calculate rebased premium based on % changes
            # rc_vbl.uw_selected.calculated = rc_vbl.model_calculated       ### CUSTOM THIS LINE IS NOW DONE THROUGH ASYNC RARC_TASK SO WE CAN CLEAR IT ON RENEWAL VIA ASYNC WITHOUT CONFLICTS
            rebased_premium_model        *= rc_vbl.model_calculated or 0
            rebased_premium_uw           *= rc_vbl.uw_selected.selected or 0

            # Add selected change to list
            rate_changes.append(rc_vbl.uw_selected.selected)
            
            # Validate overrides if unexplained
            if rc_vbl.uw_selected.is_overridden is True and rc_vbl.comments is None:
                hx.errors.validation(f"Rate Change: {(utils.title_rc(item))} has been overridden and no comment provided")

        # Calculate final rate change with overrides
        renewal_premium = layer.quoted_premium_annualised /  (rc_lay.written_line.renewal or 1) 

        model_rarc_net = ratio(renewal_premium, rebased_premium_model, 1)
        final_rarc_net = ratio(renewal_premium, rebased_premium_uw, 1)

        layer.rate_change.risk_adjusted_rate_change_model_net   = layer.rate_change.rate_change.model_calculated    = model_rarc_net
        layer.rate_change.risk_adjusted_rate_change             = layer.rate_change.rate_change.uw_selected         = final_rarc_net
        layer.rate_change.risk_adjusted_rate_change_uw_net      = final_rarc_net

        # For PMD reporting
        brokerage_change = layer.rate_change.brokerage_change.model_calculated or 1
        layer.rate_change.risk_adjusted_rate_change_model_gross =                                                                   model_rarc_net * brokerage_change
        layer.rate_change.risk_adjusted_rate_change_uw_gross    = layer.rate_change.risk_adjusted_rate_change_gross_for_reporting = final_rarc_net * brokerage_change

        # Valildation to ensure rate change is completed for bound layers

        hx_rc_warning = False

        if hxd.cds.standard_fields.is_rater_priced:
            if any(change is None for change in rate_changes) and layer.status in ["Bound", "Post Bind Complete"]:
                hx.errors.validation(f"Rate change must be completed for bound layer {idx+1}")
                hx_rc_warning = True
        if hxd.cds.standard_fields.is_case_priced:
            if layer.rate_change.risk_adjusted_rate_change_case_priced is None and layer.status in ["Bound", "Post Bind Complete"]:
                hx.errors.validation(f"Rate change must be completed for bound layer {idx+1}")
                hx_rc_warning = True

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

    # # Validate premiums
    # if not rc.has_rarc_run:
    #     return

    for idx, layer in enumerate(layers):
        rc_prem = layer.rate_change.premium

        # Here we compare the annualised benchmark and quoted premiums, the temp storage premiums are already annualised
        is_bm_different =    (layer.benchmark_premium_annualised != layer.rate_change.temp_storage.benchmark_premium)
        is_quoted_different =(layer.quoted_premium_annualised    != layer.rate_change.temp_storage.quoted_premium)
        
        # assign default values
        rarc_message            = ""
        rarc_message_show       = False
        
        # format premiums for use in f strings
        previous_bm_prem        = "{:,.0f}".format((layer.rate_change.temp_storage.benchmark_premium or 0) * (term_factor or 0)) # Convert premium from annual to policy term
        previous_quoted_prem    = "{:,.0f}".format((layer.rate_change.temp_storage.quoted_premium or 0) * (term_factor or 0))
        current_bm_prem         = "{:,.0f}".format(layer.benchmark_premium or 0)
        current_quoted_prem     = "{:,.0f}".format(rc_prem.beazley_line.policy_term.renewal)

        if is_bm_different and is_quoted_different:
            rc.rarc_run_again_message = "❗ Benchmark and quoted premiums have changed. Run the rate change calculation again ❗"
            rc.rarc_message_show = True
            break
        elif is_bm_different:
            rc.rarc_run_again_message = f"Benchmark premium has changed from {previous_bm_prem} to {current_bm_prem}.\nPlease run the rate change calculation again."
            rc.rarc_message_show = True
            break
        elif is_quoted_different:
            rc.rarc_run_again_message = f"Quoted premium has changed from {previous_quoted_prem} to {current_quoted_prem}.\nPlease run the rate change calculation again."
            rc.rarc_message_show = True
            break

    hxd.cds.rate_change.rarc_calcs_show = not rc.rarc_message_show

    # Add validation error to prevent policy from being set to final
    if (is_bm_different or is_quoted_different) and not hx_rc_warning:
        hx.errors.validation("'Calculate Rate Change' in the Rate Change page must be run again.")
        

