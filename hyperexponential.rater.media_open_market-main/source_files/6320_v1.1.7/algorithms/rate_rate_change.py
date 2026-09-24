# v0.3.0
import hx
import pandas as pd
import numpy as np
import math as math
import json
from algorithms.rate_utilities import title_rc, ratio, usd, to_ccy, look_up
from operator import itemgetter
from algorithms.rate_constants import max_layers, exposure_change_list, risk_char_change_list, deductible_change_list, limit_change_list, t_and_cs_change_list, other_change_list
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import COVERAGES_LIST
from algorithms import parameter_tables_schema as params

# -----------------------------------------------------------------------------
# NOTE
# As we need the rate change buckets to align with the PMD we have grouped
# brokerage and other into 'other incl. brokerage' and allocated other node below. 
# Brokerage will be calculated seperately in the rarc_task but not displayed standalone.
# -----------------------------------------------------------------------------
# NOTE: Provide the bucket information. 
RATE_CHANGE_BUCKETS = {
    "model": [], # NOTE: leave this empty - starts from expiry data priced with current model
    "exposure": exposure_change_list() + [],
    "risk_characteristics": risk_char_change_list() + [],
    "deductible": deductible_change_list() + [],
    "limit": limit_change_list() + [],
    "terms_conditions": t_and_cs_change_list() + [],
    "other": other_change_list() + []

} if not RARC_COVERAGE_USE else {
    "example_coverage_1" : {
        "model": [], # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": [],
        "risk_characteristics": [],
        "deductible": [
            "cds/layers/coverages/example_coverage_1/excess",
            "cds/layers/coverages/example_coverage_1/deductible"
        ],
        "limit": [
            "cds/layers/coverages/example_coverage_1/limit"
        ],
        "terms_conditions": [],
        "other": [
            "cds/layers/coverages/example_coverage_1/brokerage"
        ]
    },
    "example_coverage_2" : {
        "model": [], # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": [],
        "risk_characteristics": [],
        "deductible": [
            "cds/layers/coverages/example_coverage_2/excess",
            "cds/layers/coverages/example_coverage_2/deductible"
        ],
        "limit": [
            "cds/layers/coverages/example_coverage_2/limit"
        ],
        "terms_conditions": [],
        "other": [
            "cds/layers/coverages/example_coverage_2/brokerage"
        ]
    }
}        

# NOTE: Provide the input subject to currency change.
EXP_INPUTS_IN_CCY = {
    "layers":[
        # (input_node_path,input_currency_node_path)

        ("cds/layers/limit","cds/currencies/source_currency"),
        ("cds/layers/excess","cds/currencies/source_currency"),
        ("cds/layers/deductible","cds/currencies/source_currency"),
        # ("cds/layers/aggregate_limit","cds/currencies/source_currency"),
        ("cds/layers/aggregate_limit_view","cds/currencies/source_currency"),
        # ("cds/layers/aggregate_excess","cds/currencies/source_currency"),
        # ("cds/layers/aggregate_deductible","cds/currencies/source_currency"),
        ("cds/layers/attachment","cds/currencies/source_currency"),
        ("cds/layers/quoted_premium_100","cds/currencies/source_currency"),

        ("cds/options/retention","cds/currencies/source_currency"),
        ("cds/options/eec_limit","cds/currencies/source_currency"),
        ("cds/options/aggregate_limit","cds/currencies/source_currency"),
        ("cds/options/eec_excess","cds/currencies/source_currency"),
        ("cds/options/aggregate_excess","cds/currencies/source_currency"),

        ("cds/primary/attachment","cds/currencies/source_currency"),
        # ("cds/primary/aggregate_limit","cds/currencies/source_currency"),

        ("cds/exposure/aggregate/total_revenue","cds/currencies/source_currency"),
        ("cds/exposure/aggregate/rateable/revenue","cds/currencies/source_currency"),

        ("cds/annual_tv/turnover","cds/currencies/source_currency"),
        ("cds/annual_tv/annual_budget","cds/currencies/source_currency"),
        ("cds/individual_tv/modifiers/genre","cds/currencies/source_currency"), # base premium
        ("cds/individual_film/modifiers/exhibition","cds/currencies/source_currency"), # base premium
    ]
} if not RARC_COVERAGE_USE else {
    "example_coverage_1" : [
        # (input_node_path,input_currency_node_path)
        ("cds/layers/coverages/example_coverage_1/limit","cds/layers/coverages/example_coverage_1/currency"),
        ("cds/layers/coverages/example_coverage_1/excess","cds/layers/coverages/example_coverage_1/currency"),
        ("cds/layers/coverages/example_coverage_1/deductible","cds/layers/coverages/example_coverage_1/currency"),
        ("cds/layers/coverages/example_coverage_1/quoted_premium_100","cds/layers/coverages/example_coverage_1/currency"),
    ],
    "example_coverage_2" : [
        # (input_node_path,input_currency_node_path)
        ("cds/layers/coverages/example_coverage_2/limit","cds/layers/coverages/example_coverage_2/currency"),
        ("cds/layers/coverages/example_coverage_2/excess","cds/layers/coverages/example_coverage_2/currency"),
        ("cds/layers/coverages/example_coverage_2/deductible","cds/layers/coverages/example_coverage_2/currency"),
        ("cds/layers/coverages/example_coverage_2/quoted_premium_100","cds/layers/coverages/example_coverage_2/currency"),
    ]       
}

def rate_rate_change(hxd):
    """
    Use when the rate change is calculated at a layer level. In case of use of coverages, use rate_rate_change_coverages instead.
    Assign rate change renewing and expiring premium, calculate the rarc and set some validation on layer and premium 
    """
    layers = hxd.cds.layers
    rc = hxd.cds.rate_change
    if RARC_COVERAGE_USE:
        cvgs = hxd.cds.layers[0].coverages
        rc.rarc_coverage_use = RARC_COVERAGE_USE
        rc.rarc_insured_asset_use = RARC_INSURED_ASSET_USE
    # rc.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id # Edit v0.3.0 commented and reassigned in start_renewal_task to allow Override to clear when creating a renewal options
    sf = hxd.cds.standard_fields
    agg = hxd.cds.exposure.aggregate

    # get FX table from the library
    fx_rates_df = params.fx_rates.df() # Using fx from library
    # fx_rates_df = hx.params.table_currency # Using fx from params

    # The rate change is hidden for layers not used in the pricing summary
    num_layers = len(layers)
    for index in range(1,max_layers+1):
        setattr(hxd.cds.rate_change, f"show_layer_{index}", True) if index <= num_layers else False
        
    annualise_renewal = 12 / (hxd.cds.rating_factors.policy_term * 12) if hxd.cds.rating_factors.policy_term else 0

    for idx, layer in enumerate(layers): 
        # Set the shownby of the expiring revalued 
        layer.rate_change.new_layer = False if isinstance(layer.rate_change.expiring_layer,int) else True
        layer.rate_change.renewing_layer = not layer.rate_change.new_layer
        rebased_premium_model , rebased_premium_uw , renewal_premium = assign_rc_nodes(layer, layer.rate_change,annualise_renewal) # Edit v0.3.0 - using generic function

        # Initialise list to check all changes are filled in
        rate_changes = []
        rarc_changes_titles = {
        "exposure_change": "Exposure Change",
        "risk_characteristics_change": "Risk Characteristics Change",
        "limit_change":"Limit Change",
        "deductible_change": "Deductible Change",
        "terms_conditions_change":  "Terms & Conditions Change",
        "other_change":"Other Change(incl. Brokerage)"
        }

        rate_change_ow_values = ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]
        for item in rate_change_ow_values:
            # Calculate rebased premium based on % changes
            rc_vbl = getattr(layer.rate_change, item)
            # rc_vbl.uw_selected.calculated = rc_vbl.model_calculated # Edit v0.3.0 Move to task to Clear at the creation of a renewal
            rc_vbl.final = rc_vbl.uw_override or rc_vbl.model_calculated # Edit v0.3.0
            rebased_premium_model *= rc_vbl.model_calculated or 0
            # rebased_premium_uw *= rc_vbl.uw_selected.selected or 0 # Edit v0.3.0 - Commented out since the introduction of uw_override and final nodes. DO NOT USE IN NEW MODEL
            rebased_premium_uw *= rc_vbl.final or 0 # Edit v0.3.0

            # Add selected change to list
            # rate_changes.append(rc_vbl.uw_selected.selected) # Edit v0.3.0 DO NOT USE IN NEW MODEL
            rate_changes.append(rc_vbl.final) # Edit v0.3.0
            
            # Validate overrides if unexplained
            # if rc_vbl.uw_selected.is_overridden is True and rc_vbl.comments is None: # Edit v0.3.0
            if rc_vbl.uw_override is not None and (rc_vbl.comments is None or rc_vbl.comments =="") and hxd.cds.standard_fields.is_renewal == True:
                # hx.errors.validation(f"Rate Change: {(title_rc(item))} has been overridden and no comment provided")
                hx.errors.validation(f"Rate Change: Comment required for {(rarc_changes_titles[item])} override")

        # Calculate final rate change with overrides
        layer.rate_change.premium.line_100pct.annualised.rebased_expiring = rebased_premium_uw
        if renewal_premium is not None:
            model_rarc = ratio(renewal_premium, rebased_premium_model, 1)
            final_rarc = ratio(renewal_premium, rebased_premium_uw, 1)
        else:
            model_rarc = 1
            final_rarc = 1   

        layer.rate_change.rate_change.model_calculated = model_rarc
        # layer.rate_change.risk_adjusted_rate_change = layer.rate_change.rate_change.uw_selected = layer.rate_change.rate_change.final = final_rarc # Edit v0.3.0 Commented out since the introduction of uw_override and final nodes.
        layer.rate_change.risk_adjusted_rate_change = layer.rate_change.rate_change.final = final_rarc 

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
    current_mapping = {str(idx + 1): layer.rate_change.expiring_layer for idx, layer in enumerate(layers)}

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
        # get FX rates
        current_fx_to_usd = look_up(lookup_value=layer.currency, lookup_col="ccy", return_col="fx_rate", df=fx_rates_df, if_not_found=1)
        temp_fx_to_usd = look_up(lookup_value=layer.rate_change.temp_storage.currency, lookup_col="ccy", return_col="fx_rate", df=fx_rates_df, if_not_found=1)

        # Here we compare the annualised benchmark and quoted premiums, the temp storage premiums are already annualised
        is_bm_different = (layer.benchmark_premium_annual_100 * current_fx_to_usd != layer.rate_change.temp_storage.benchmark_premium * temp_fx_to_usd) # from the library benchmark_premium is in line with the value assigned to expiring_technical_prem
        is_quoted_different = (layer.quoted_premium_annual_100 * current_fx_to_usd != layer.rate_change.temp_storage.quoted_premium * temp_fx_to_usd) # from the library quoted_premium is in line with the value assigned to expiring_actual_prem

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
    # Edit v0.3.0 - Comment be below to have a stronger condition on error message
    # if is_bm_different or is_quoted_different:
    #     hx.errors.validation("'Calculate Rate Change' in the Rate Change page must be run again.")
    if rc.rarc_run_again_message is not None:
        hx.errors.validation("Rate Change: 'Calculate Rate Change' must be run again")

def assign_rc_nodes(rc_source_data, rc_data, annualise_factor):
    """
    This function assigns values to rate change nodes:
     - the renewing, expiring, expiring revalued rate change nodes
     - 100 premium, Beazley premium, policy term, and annualised. 
    It also populates table nodes with policy details including limit, deductible, excess, and brokerage.
    """
    fx_rates_df = params.fx_rates.df() # Using fx from library
    # fx_rates_df = hx.params.table_currency # Using fx from params

    # Assign rate change renewal data
    quoted_premium_100 = rc_source_data.quoted_premium_100 or 0
    rc_data.premium.line_100pct.annualised.renewal = quoted_premium_100 * annualise_factor
    rc_data.premium.beazley_line.annualised.renewal = quoted_premium_100 * annualise_factor * (rc_source_data.written_line or 1)
    rc_data.premium.line_100pct.policy_term.renewal = quoted_premium_100 
    rc_data.premium.beazley_line.policy_term.renewal = quoted_premium_100 *  (rc_source_data.written_line or 1)

    # rc_data.total_revenue.renewal = # IR: how to add? doesn't exist for nonstandard coverages
    # rc_data.rateable_revenue.renewal =  # IR: how to add? doesn't exist for nonstandard coverages
    rc_data.aggregate_limit.renewal = rc_source_data.aggregate_limit
    # rc_data.eec_limit.renewal = ??? # IR: how to add?
    rc_data.attachment.renewal = rc_source_data.attachment # deductible
    # rc_data.excess.renewal = rc_source_data.excess 
    rc_data.brokerage.renewal = rc_source_data.brokerage
    rc_data.currency.renewal = rc_source_data.currency
    
    # Assign rate change expiring data
    # rc_data.premium.line_100pct.annualised.expiring = expiring_premium_annual = (rc_data.expiring_policy_info.expiring_quoted_premium_100 or 0)* (annualise_factor) 
    rc_data.premium.line_100pct.annualised.expiring = expiring_premium_annual_100 = rc_data.expiring_policy_info.expiring_quoted_premium_annual_100 or 0
    rc_data.premium.beazley_line.annualised.expiring = expiring_premium_annual_100 * (rc_data.expiring_policy_info.expiring_written_line or 0)
    rc_data.premium.line_100pct.policy_term.expiring = expiring_premium_policy_term_100 = rc_data.expiring_policy_info.expiring_quoted_premium_annual_100 or 0
    rc_data.premium.beazley_line.policy_term.expiring = expiring_premium_policy_term_100 * (rc_data.expiring_policy_info.expiring_written_line or 0)

    # rc_data.total_revenue.expiring = # IR: how to add? doesn't exist for nonstandard coverages
    # rc_data.rateable_revenue.expiring = # IR: how to add? doesn't exist for nonstandard coverages
    rc_data.aggregate_limit.expiring = (rc_data.expiring_policy_info.expiring_aggregate_limit or 0)
    # rc_data.eec_limit.expiring = ??? # IR: how to add?
    rc_data.attachment.expiring = (rc_data.expiring_policy_info.expiring_attachment or 0) # deductible
    # rc_data.excess.expiring = (rc_data.expiring_policy_info.expiring_excess or 0)
    rc_data.brokerage.expiring = (rc_data.expiring_policy_info.expiring_brokerage or 0)
    rc_data.currency.expiring = (rc_data.expiring_policy_info.expiring_currency or "USD")

    # get expiring and renewing fx
    expiring_fx_to_usd = look_up(lookup_value=rc_data.currency.expiring, lookup_col="ccy", return_col="fx_rate", df=fx_rates_df, if_not_found=1)
    renewing_fx_to_usd = look_up(lookup_value=rc_data.currency.renewal, lookup_col="ccy", return_col="fx_rate", df=fx_rates_df, if_not_found=1)
    
    # assign value to show_expiring
    rc_data.show_expiring_revalued = (rc_data.currency.expiring != rc_data.currency.renewal)
    
    revaluing_factor = ratio(renewing_fx_to_usd,expiring_fx_to_usd) if rc_data.show_expiring_revalued else 1
    
    # rc_data.premium.line_100pct.annualised.expiring = expiring_premium_annual = (rc_data.expiring_policy_info.expiring_quoted_premium_100 or 0)* (annualise_factor) 
    rc_data.premium.line_100pct.annualised.expiring_revalued = rc_data.premium.line_100pct.annualised.expiring * revaluing_factor
    rc_data.premium.beazley_line.annualised.expiring_revalued = rc_data.premium.beazley_line.annualised.expiring * revaluing_factor
    rc_data.premium.line_100pct.policy_term.expiring_revalued = rc_data.premium.line_100pct.policy_term.expiring * revaluing_factor
    rc_data.premium.beazley_line.policy_term.expiring_revalued = rc_data.premium.beazley_line.policy_term.expiring * revaluing_factor

    # rc_data.total_revenue.expiring_revalued = rc_data.total_revenue.expiring * revaluing_factor
    # rc_data.rateable_revenue.expiring_revalued = rc_data.rateable_revenue.expiring * revaluing_factor
    rc_data.aggregate_limit.expiring_revalued = rc_data.aggregate_limit.expiring * revaluing_factor
    # rc_data.eec_limit.expiring_revalued = rc_data.eec_limit.expiring * revaluing_factor
    rc_data.attachment.expiring_revalued = rc_data.attachment.expiring * revaluing_factor
    # rc_data.excess.expiring_revalued = rc_data.excess.expiring * revaluing_factor
    rc_data.brokerage.expiring_revalued = rc_data.brokerage.expiring # same as expiring
    rc_data.currency.expiring_revalued = rc_data.currency.renewal # same as renewing

    # Calculate rebased premium for each bucket
    rebased_premium_model = rebased_premium_uw = rc_data.premium.line_100pct.annualised.expiring or 0
    renewal_premium = rc_data.premium.line_100pct.annualised.renewal
    return rebased_premium_model, rebased_premium_uw, renewal_premium

def rate_rate_change_coverages(hxd): 
    """
    Use when the rate change is calculated at a coverages level.
    Assign rate change renewing and expiring premium, calculate the rarc and set some validation on layer and premium.
    """
    layers = hxd.cds.layers
    rc = hxd.cds.rate_change
    if RARC_COVERAGE_USE:
        cvgs = hxd.cds.layers[0].coverages
        rc.rarc_coverage_use = RARC_COVERAGE_USE
        rc.rarc_insured_asset_use = RARC_INSURED_ASSET_USE
    sf = hxd.cds.standard_fields
    agg = hxd.cds.exposure.aggregate

    # get FX table 
    fx_rates_df = params.fx_rates.df() # Using fx from library
    # fx_rates_df = hx.params.table_currency # Using fx from params

    # For layers not used in the pricing summary, the rate change is hidden
    num_layers = len(layers)
    for index in range(1, max_layers + 1):
        setattr(hxd.cds.rate_change, f"show_layer_{index}", True) if index <= num_layers else False

    annualise_renewal = 12 / (hxd.cds.rating_factors.policy_term * 12) or 0

    for idx, layer in enumerate(layers):
        # Set the shownby of the expiring revalued 
        layer.rate_change.new_layer = False if isinstance(layer.rate_change.expiring_layer,int) else True
        layer.rate_change.renewing_layer = not layer.rate_change.new_layer

        for coverage in COVERAGES_LIST:
            # Initialise variables for each coverage
            rebased_premium_model, rebased_premium_uw, renewal_premium = assign_rc_nodes(
                rc_source_data = getattr(layer.coverages, coverage),
                rc_data = getattr(layer.rate_change, coverage),
                annualise_factor = annualise_renewal
            )

            # Initialise list to check all changes are filled in
            rate_changes = []
            for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
                # Calculate rebased premium based on % changes
                rc_vbl = getattr(getattr(layer.rate_change, coverage), item)
                
                rc_vbl.final = rc_vbl.uw_override or rc_vbl.model_calculated
                rebased_premium_model *= rc_vbl.model_calculated or 0
                
                rebased_premium_uw *= rc_vbl.final or 0
                
                # Add selected change to list
                rate_changes.append(rc_vbl.final)
                
                # Validate overrides if unexplained
                if rc_vbl.uw_override is True and rc_vbl.comments is None:
                    hx.errors.validation(f"Rate Change: {title_rc(item)} has been overridden and no comment provided")

            # Calculate final rate change with overrides
            getattr(layer.rate_change, coverage).premium.line_100pct.annualised.rebased_expiring = rebased_premium_uw
            if renewal_premium is not None:
                model_rarc = ratio(renewal_premium, rebased_premium_model, 1)
                final_rarc = ratio(renewal_premium, rebased_premium_uw, 1)
            else:
                model_rarc = 1
                final_rarc = 1

            getattr(layer.rate_change, coverage).rate_change.model_calculated = model_rarc
            # getattr(layer.rate_change, coverage).risk_adjusted_rate_change = getattr(layer.rate_change, coverage).rate_change.uw_selected = final_rarc
            getattr(layer.rate_change, coverage).risk_adjusted_rate_change = getattr(layer.rate_change, coverage).rate_change.final = final_rarc
            
            # For PMD reporting
            brokerage_change = getattr(getattr(layer.rate_change, coverage), "brokerage_change").model_calculated or 1
            getattr(layer.rate_change, coverage).risk_adjusted_rate_change_gross_for_reporting = final_rarc * brokerage_change


            # Validation to ensure rate change is completed for bound layers
            if hxd.cds.standard_fields.is_rater_priced and any(change is None for change in rate_changes) and getattr(layer.coverages, coverage).status in ["Bound", "Post Bind Complete"]:
                hx.errors.validation(f"Rate change must be completed for bound layer {idx+1}")

            if hxd.cds.standard_fields.is_case_priced and getattr(getattr(layer.rate_change, coverage), "risk_adjusted_rate_change_case_priced") is None and getattr(layer.coverages, coverage).status in ["Bound", "Post Bind Complete"]:
                hx.errors.validation(f"Rate change must be completed for bound layer {idx+1}")

    
    # Validate layer mapping
    current_mapping = {str(idx + 1): layer.rate_change.expiring_layer for idx, layer in enumerate(layers)}
    
    previous_mapping = json.loads(rc.layer_mapping) if rc.layer_mapping else current_mapping

    if current_mapping != previous_mapping:
        hx.errors.validation("Mapping of Expiring Layers to Renewal Layers is inconsistent with numbers shown in Rate Change")
        task = "'Calculate Rate Change'" if rc.has_rarc_run else "'Fetch Expiring Data'"
        rc.rarc_run_again_message = f"❗ Mapping of Expiring Layers to Renewal Layers has changed. Run {task} again ❗"
        rc.rarc_message_show = True
        return

    # Validate rate change calculation run by comparing calculated premiums vs temp
    if not rc.has_rarc_run:
        return

    for idx, layer in enumerate(layers):
        # get FX rates
        current_fx_to_usd = look_up(lookup_value=layer.currency, lookup_col="ccy", return_col="fx_rate", df=fx_rates_df, if_not_found=1)
        temp_fx_to_usd = look_up(lookup_value=layer.rate_change.temp_storage.currency, lookup_col="ccy", return_col="fx_rate", df=fx_rates_df, if_not_found=1)

        is_bm_different = False
        is_quoted_different = False
        for coverage in COVERAGES_LIST:
            is_bm_different |= ((getattr(layer.coverages, coverage).benchmark_premium_annual_100 * current_fx_to_usd) != (getattr(getattr(layer.rate_change, coverage), "temp_storage").benchmark_premium) * temp_fx_to_usd)
            is_quoted_different |= ((getattr(layer.coverages, coverage).quoted_premium_annual_100 * current_fx_to_usd) != (getattr(getattr(layer.rate_change, coverage), "temp_storage").quoted_premium) * temp_fx_to_usd)

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

    if rc.rarc_run_again_message is not None:
        hx.errors.validation("Rate Change: 'Calculate Rate Change' must be run again")

