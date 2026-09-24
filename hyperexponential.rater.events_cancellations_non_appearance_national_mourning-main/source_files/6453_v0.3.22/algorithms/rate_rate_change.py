# v0.5.0
import hx
import pandas as pd
import numpy as np
import math as math
import json
from algorithms.rate_utilities import title_rc, ratio, look_up
from operator import itemgetter

from algorithms.rate_constants import max_layers
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import COVERAGES_LIST

from algorithms import parameter_tables_schema as params

from algorithms.rate_change.rate_rate_change_global_variables import RATE_CHANGE_BUCKETS, EXP_INPUTS_IN_CCY
from algorithms.rate_change.rate_rate_change_generic_functions import assign_rc_nodes
from algorithms.rate_change.rate_rate_change_insured_asset import define_insured_asset_list_variable, save_insured_asset_list_for_rate_change

def rate_rate_change(hxd):
    """
    Assign rate change renewing and expiring premium, calculate the rarc and set some validation on layer and premium
    Use for rate change at a layer-level only. For rate change at a coverage-level, use rate_rate_change_coverages instead.
    """
    layers = hxd.cds.layers
    rc = hxd.cds.rate_change
    if RARC_COVERAGE_USE:
        rc.rarc_coverage_use = RARC_COVERAGE_USE
        rc.rarc_insured_asset_use = RARC_INSURED_ASSET_USE
    sf = hxd.cds.standard_fields
    agg = hxd.cds.exposure.aggregate

    # get FX table from the library
    fx_rates_df = params.fx_rates.df() # Using fx from library
    # fx_rates_df = hx.params.table_currency # Using fx from params

    # The rate change is hidden for layers not used in the pricing summary
    num_layers = len(layers)
    for index in range(1,max_layers+1):
        if index <= num_layers: 
            setattr(hxd.cds.rate_change, f"show_layer_{index}", True)

    for idx, layer in enumerate(layers): 
        # Set the shownby of the expiring revalued 
        layer.rate_change.new_layer = False if isinstance(layer.rate_change.expiring_layer,int) else True
        layer.rate_change.renewing_layer = not layer.rate_change.new_layer
        # Assign rate change variables
        rebased_premium_model , rebased_premium_uw , renewal_premium = assign_rc_nodes(rc_source_data = layer, rc_data=layer.rate_change) # Edit v0.3.0 - using generic function

        # Initialise list to check all changes are filled in
        rate_changes = []
        for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
            # Calculate rebased premium based on % changes
            rc_vbl = getattr(layer.rate_change, item)
            # rc_vbl.uw_selected.calculated = rc_vbl.model_calculated # Edit v0.3.0 Legacy model only. Move to task to Clear at the creation of a renewal
            rc_vbl.final = rc_vbl.uw_override or rc_vbl.model_calculated # Edit v0.3.0
            rebased_premium_model *= rc_vbl.model_calculated or 0
            # rebased_premium_uw *= rc_vbl.uw_selected.selected or 0 # Edit v0.3.0 - Legacy model only. Commented out since the introduction of uw_override and final nodes. DO NOT USE IN NEW MODEL
            rebased_premium_uw *= rc_vbl.final or 0 # Edit v0.3.0

            # Add selected change to list
            # rate_changes.append(rc_vbl.uw_selected.selected) # Edit v0.3.0 Legacy model only. DO NOT USE IN NEW MODEL
            rate_changes.append(rc_vbl.final) # Edit v0.3.0
            
            # Validate overrides if unexplained
            # if rc_vbl.uw_selected.is_overridden is True and rc_vbl.comments is None: # Edit v0.3.0. Legacy model only. 
            if rc_vbl.uw_override and rc_vbl.comments is None:
                hx.errors.validation(f"Rate Change: {(title_rc(item))} has been overridden and no comment provided")

        # Handling Change in Coverage currency with Insured interest
        if RARC_INSURED_ASSET_USE:
            # get the currency
            current_currency = layer.currency
            previous_currency = layer.rate_change.expiring_policy_info.expiring_currency

            # revaluing expiry premium at a laver level in case of change in policy currency at renewal
            if not current_currency == previous_currency:
                # get the Current FX
                renewing_fx_to_usd = look_up(current_currency,"ccy","fx_rate",fx_rates_df,if_not_found=1)
                # get the Previous FX
                expiring_fx_to_usd = look_up(previous_currency,"ccy","fx_rate",fx_rates_df,if_not_found=1)
                # calculate revaluing factor
                revaluing_factor = ratio(renewing_fx_to_usd,expiring_fx_to_usd) or 1
                # revalue expiry premium rebased_premium_model and rebased_premium_uw in renewing currency
                rebased_premium_model = rebased_premium_model * revaluing_factor
                rebased_premium_uw = rebased_premium_uw * revaluing_factor

        # Calculate final rate change with overrides
        layer.rate_change.premium.line_100pct.annualised.rebased_expiring = rebased_premium_uw
        if renewal_premium is not None:
            model_rarc = ratio(renewal_premium, rebased_premium_model, 1)
            final_rarc = ratio(renewal_premium, rebased_premium_uw, 1)
        else:
            model_rarc = 1
            final_rarc = 1   

        layer.rate_change.rate_change.model_calculated = model_rarc
        # layer.rate_change.risk_adjusted_rate_change = layer.rate_change.rate_change.uw_selected = layer.rate_change.rate_change.final = final_rarc # Edit v0.3.0 Legacy model only. Commented out since the introduction of uw_override and final nodes.
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

        # Here we compare the annualised benchmark and quoted premiums to the temp premium (already annualised). If different, the calculation has to be run again.
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

def rate_rate_change_coverages(hxd): 
    """
    Assign rate change renewing and expiring premium, calculate the rarc and set some validation on layer and premium
    Use for rate change at a coverage-level  only. For rate change at a layer-level, use rate_rate_change instead.
    """
    layers = hxd.cds.layers
    rc = hxd.cds.rate_change
    if RARC_COVERAGE_USE:
        rc.rarc_coverage_use = RARC_COVERAGE_USE
        rc.rarc_insured_asset_use = RARC_INSURED_ASSET_USE
    sf = hxd.cds.standard_fields
    agg = hxd.cds.exposure.aggregate
    pol_ccy = hxd.cds.currencies.source_currency

    # get FX table 
    fx_rates_df = params.fx_rates.df() # Using fx from library
    # fx_rates_df = hx.params.table_currency # Using fx from params

    # The rate change is hidden for layers not used in the pricing summary
    num_layers = len(layers)
    for index in range(1, max_layers + 1):
        if index <= num_layers:
            setattr(hxd.cds.rate_change, f"show_layer_{index}", True) 

    for idx, layer in enumerate(layers):
        # Set the shownby of the expiring revalued 
        layer.rate_change.new_layer = False if isinstance(layer.rate_change.expiring_layer,int) else True
        layer.rate_change.renewing_layer = not layer.rate_change.new_layer

        for coverage in COVERAGES_LIST:
            if RARC_INSURED_ASSET_USE:
                # When using insured asset, the reporting currency by coverage is set equal to the policy reporting currency. 
                setattr(getattr(layer.coverages, coverage),"currency", pol_ccy)
            # Assign rate change variables
            rebased_premium_model, rebased_premium_uw, renewal_premium = assign_rc_nodes(
                rc_source_data = getattr(layer.coverages, coverage),
                rc_data = getattr(layer.rate_change, coverage)
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

            # Handling Change in Coverage currency with Insured interest
            if RARC_INSURED_ASSET_USE:
                # get the currency
                current_currency = getattr(getattr(layer.coverages, coverage),"currency")
                previous_currency = getattr(layer.rate_change, coverage).expiring_policy_info.expiring_currency

                 # check if the currency is the same
                if not current_currency == previous_currency:
                    # revalue expiry premium rebased_premium_model and rebased_premium_uw in renewing currency
                    # get the Current FX
                    renewing_fx_to_usd = look_up(current_currency,"ccy","fx_rate",fx_rates_df,if_not_found=1)
                    # get the Previous FX
                    expiring_fx_to_usd = look_up(previous_currency,"ccy","fx_rate",fx_rates_df,if_not_found=1)
                    revaluing_factor = ratio(renewing_fx_to_usd,expiring_fx_to_usd) or 1
                    # revalue expiry premium
                    rebased_premium_model = rebased_premium_model * revaluing_factor
                    rebased_premium_uw = rebased_premium_uw * revaluing_factor
                    
            # Calculate final rate change with overrides
            getattr(layer.rate_change, coverage).premium.line_100pct.annualised.rebased_expiring = rebased_premium_uw
            if renewal_premium is not None:
                model_rarc = ratio(renewal_premium, rebased_premium_model, 1)
                final_rarc = ratio(renewal_premium, rebased_premium_uw, 1)
            else:
                model_rarc = 1
                final_rarc = 1

            getattr(layer.rate_change, coverage).rate_change.model_calculated = model_rarc
            # getattr(layer.rate_change, coverage).risk_adjusted_rate_change = getattr(layer.rate_change, coverage).rate_change.uw_selected = final_rarc # Edit v0.3.0. Legacy model only. DO NOT USE uw_selected since uw_override and Final nodes have been introduced
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
        
        return # Do not validate any further until the task is run again

    # Validate rate change calculation run by comparing calculated premiums vs temp
    if not rc.has_rarc_run:
        return

    for idx, layer in enumerate(layers):

        is_bm_different = False
        is_quoted_different = False
        for coverage in COVERAGES_LIST:
            # get FX rates for coverages
            current_fx_to_usd = look_up(lookup_value=getattr(layer.coverages,coverage).currency, lookup_col="ccy", return_col="fx_rate", df=fx_rates_df, if_not_found=1)
            temp_fx_to_usd = look_up(lookup_value=getattr(layer.rate_change,coverage).temp_storage.currency, lookup_col="ccy", return_col="fx_rate", df=fx_rates_df, if_not_found=1)
            
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


