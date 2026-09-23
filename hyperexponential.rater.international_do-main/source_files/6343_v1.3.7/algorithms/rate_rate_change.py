import hx
import pandas as pd
import numpy as np
import math as math
import json
import algorithms.rate_utilities as utils
from algorithms.rate_utilities import title_rc, ratio, usd, to_ccy, look_up
from operator import itemgetter
from algorithms.rate_constants import max_layers
from algorithms import parameter_tables_schema as params
from datetime import timedelta, datetime
from algorithms.year_frac import basis1

def rate_change_buckets(hxd):
    # -----------------------------------------------------------------------------
    # NOTE
    # As we need the rate change buckets to align with the PMD we have grouped
    # brokerage and other into 'other incl. brokerage' and allocated other node below. 
    # Brokerage will be calculated seperately in the rarc_task but not displayed standalone.
    # -----------------------------------------------------------------------------
    
    buckets = {
        "model": [], # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": [
            "cds/exposure/aggregate/market_cap_2_year_high",
            "cds/exposure/aggregate/current_market_cap",
            "cds/exposure/aggregate/insider_shareholder_share",
            "cds/rating_factors/risk_information/country_of_domicile",
            "cds/rating_factors/risk_information/main_operating_country",
            "cds/rating_factors/risk_information/primary_listing_location",
            "cds/rating_factors/risk_information/ownership_type",
            "cds/exposure/aggregate/ignore_ipo",
            "cds/exposure/aggregate/ipo_date",
            "cds/rating_factors/risk_information/industry_class_sic_code",
            "cds/exposure/aggregate/us_listing_share",
            "cds/exposure/aggregate/credit_score",
            "cds/exposure/aggregate/total_assets",
            "cds/exposure/aggregate/ebit",
            "cds/exposure/aggregate/net_sales",
            "cds/exposure/aggregate/total_liabilities",
            "cds/exposure/aggregate/current_assets",
            "cds/exposure/aggregate/current_liabilities",
            "cds/exposure/aggregate/retained_earnings",
            "cds/exposure/aggregate/total_liabilities",
            "cds/exposure/aggregate/minimum_trading_volume",
            "cds/exposure/aggregate/volatility_trading_volume",
            "cds/exposure/aggregate/execs_under_fifty",
            "cds/exposure/aggregate/us_ftes",
            "cds/exposure/aggregate/row_ftes",
        ],
        "risk_characteristics": [          
            "cds/rating_factors/risk_information/us_adr_exposure",
            "cds/exposure/aggregate/period_data",
            "cds/exposure/aggregate/adr_level",
            "cds/large_cap/layers/uw_side_ab_discount_override",
            "cds/modifiers/sca_freq_adj_factor",
            "cds/modifiers/management_corp_gov_factors/value",
            "cds/modifiers/business_financial_model_factors/value",
            "cds/modifiers/significant_event_factors/value",
            "cds/modifiers/stock_market_factors/value",
            "cds/modifiers/regulatory_factors/value",
            "cds/modifiers/mergers_and_acquisitions_factors/value",
            "cds/modifiers/territory_of_operation_factors/value",
            "cds/modifiers/esg_factors/value",
            "cds/modifiers/management_corp_gov_factors_side_a/value",
            "cds/modifiers/business_financial_model_factors_side_a/value",
            "cds/modifiers/significant_event_factors_side_a/value",
            "cds/modifiers/stock_market_factors_side_a/value",
            "cds/modifiers/financial_stability_side_a_factors/value",
            "cds/modifiers/indemnification_side_a_factors/value",
            "cds/modifiers/esg_factors_side_a/value",
        ],
        "deductible": [
            "cds/large_cap/layers/excess",
            "cds/large_cap/layers/deductible",
            "cds/mmp/dno/excess",
            "cds/mmp/dno/deductible",
            "cds/mmp/epl/excess",
            "cds/mmp/epl/deductible",
            "cds/mmp/cll/excess",
            "cds/mmp/cll/deductible",
        ],
        "limit": [
            "cds/large_cap/layers/limit",
            "cds/mmp/dno/limit",
            "cds/mmp/epl/limit",
            "cds/mmp/cll/limit",
        ],
        "terms_conditions": [
            # "cds/currencies/source_currency", 
            "cds/large_cap/layers/side_selection",
            "cds/risk_information/mmp_flag",
            "cds/mmp/dno/coverage",
        ],
        "other": [
            "cds/large_cap/layers/brokerage",
            "cds/mmp/dno/brokerage",
            "cds/mmp/epl/brokerage",
            "cds/mmp/cll/brokerage",
            # "cds/mmp/dno/written_line",
            # "cds/mmp/epl/written_line",
            # "cds/mmp/cll/written_line",
        ]
    }

    return buckets

def rate_rate_change(hxd):
    layers = hxd.cds.layers
    rc = hxd.cds.rate_change
    rc.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id
    sf = hxd.cds.standard_fields
    agg = hxd.cds.exposure.aggregate

    # get FX table from the library
    fx_rates_df = params.fx_rates.df() # Using fx from library
    # fx_rates_df = hx.params.table_currency # Using fx from params
    
    # For layers not used in the pricing summary, the rate change is hidden
    if hxd.cds.risk_information.mmp_flag is False:
        num_layers = len(hxd.cds.large_cap.layers)
    else: 
        num_layers = 1

    for index in range(1,max_layers+1):
        setattr(hxd.cds.rate_change, f"show_layer_{index}", True) if index <= num_layers else False

    if hxd.cds.risk_information.mmp_flag:
        for index in range(1,max_layers+1):
            setattr(hxd.cds.rate_change, f"show_layer_{index}", False)

    # Annualising factors for renewal and expiry
    annualise_renewal = 12 / (hxd.cds.rating_factors.risk_information.policy_term * 12) or 0
    
    expiring_incept = hxd.cds.rate_change.expiring_inception_date
    expiring_expiry = hxd.cds.rate_change.expiring_expiry_date

    if expiring_incept: 
        expiring_policy_term = utils.policy_term(expiring_incept, expiring_expiry)
        annualise_expiry = 12 / (expiring_policy_term * 12) or 0
    else:
        annualise_expiry = 1

    
    for idx, layer in enumerate(layers):

        # rc_prem = layer.rate_change.premium
        # # Add renewal premium to table - NOTE: this assumes 'quoted_premium' is annualised
        # rc_prem.line_100pct.annualised.renewal = layer.quoted_premium
        # if hxd.cds.risk_information.mmp_flag is not True: 
        #     rc_prem.beazley_line.annualised.renewal = layer.quoted_premium * (layer.written_line or 0)
        # else:
        #     rc_prem.beazley_line.annualised.renewal = layer.quoted_premium * (hxd.cds.mmp.total.written_line or 0)

      
        # Calculate change for each bucket
        rebased_premium_model , rebased_premium_uw , renewal_premium = assign_rc_renewal_nodes(layer, layer.rate_change, annualise_renewal, annualise_expiry) # Edit v0.2.4.1-Dev - using generic function

        # Initialise list to check all changes are filled in
        rate_changes = []

        for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
            # Calculate rebased premium based on % changes
            rc_vbl = getattr(layer.rate_change, item)
            # rc_vbl.uw_selected.calculated = rc_vbl.model_calculated # Edit v0.2.4.2-Dev Move to task to Clear at the creation of a renewal
            rc_vbl.final = rc_vbl.uw_override or rc_vbl.model_calculated # Edit v0.2.4.2-Dev
            rebased_premium_model *= rc_vbl.model_calculated or 0
            # rebased_premium_uw *= rc_vbl.uw_selected.selected or 0 # Edit v0.2.4.2-Dev - Commented out since the introduction of uw_override and final nodes
            rebased_premium_uw *= rc_vbl.final or 0 # Edit v0.2.4.2-Dev

            # Add selected change to list
            # rate_changes.append(rc_vbl.uw_selected.selected) # Edit v0.2.4.2-Dev
            rate_changes.append(rc_vbl.final) # Edit v0.2.4.2-Dev
            
            # Validate overrides if unexplained
            # if rc_vbl.uw_selected.is_overridden is True and rc_vbl.comments is None: # Edit v0.2.4.2-Dev
            if rc_vbl.uw_override is True and rc_vbl.comments is None:
                hx.errors.validation(f"Rate Change: {(title_rc(item))} has been overridden and no comment provided")
        
        # Handling Change in Coverage currency with Insured interest
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
        # layer.rate_change.risk_adjusted_rate_change = layer.rate_change.rate_change.uw_selected = layer.rate_change.rate_change.final = final_rarc # Edit v0.2.4.2-Dev
        layer.rate_change.risk_adjusted_rate_change = layer.rate_change.rate_change.final = final_rarc 

        # For PMD reporting
        brokerage_change = layer.rate_change.brokerage_change.model_calculated or 1
        layer.rate_change.risk_adjusted_rate_change_gross_for_reporting = final_rarc * brokerage_change

    # Validation of New Layer at the end of the list
    # if len(layers)>1 and sf.is_renewal == True:
    #     for i in range(len(layers)-1):
    #         if layers[i] and layers[i+1]:
    #             current_layer = layers[i]
    #             next_layer = layers[i+1]
    #             if current_layer.rate_change.new_layer and not next_layer.rate_change.new_layer:
    #                 hx.errors.validation(f"Ensure that New Layers (with no Expiry layer) are placed at the end of the list. Move Layer {idx+1}")

    # Valildation to ensure rate change is completed for bound layers
    if hxd.cds.standard_fields.is_rater_priced:
        if any(change is None for change in rate_changes) and layer.status in ["Bound", "Post Bind Complete"]:
            hx.errors.validation(f"Rate change must be completed for bound layer {idx+1}")
    if hxd.cds.standard_fields.is_case_priced:
        if layer.rate_change.risk_adjusted_rate_change_case_priced is None and layer.status in ["Bound", "Post Bind Complete"]:
            hx.errors.validation(f"Rate change must be completed for bound layer {idx+1}")

    # Validate layer mapping
    current_mapping = {}
    if hxd.cds.risk_information.mmp_flag is not True:
        for idx, layer in enumerate(layers):
            current_mapping[str(idx+1)] = layer.rate_change.expiring_layer
    else:
        current_mapping[str(idx+1)] = 1

    previous_mapping = json.loads(rc.layer_mapping) if rc.layer_mapping else current_mapping
    if current_mapping != previous_mapping and hxd.cds.risk_information.mmp_flag is False:
        hx.errors.validation("Mapping of Expiring Layers to Renewal Layers is inconsistent with numbers shown in Rate Change")

        task = "'Calculate Rate Change'" if rc.has_rarc_run else "'Fetch Expiring Data'"
        rc.rarc_run_again_message = f"❗ Mapping of Expiring Layers to Renewal Layers has changed. Run {task} again ❗"
        rc.rarc_message_show = True
        
        return # Do not validate any further until the task is run again

    # Validate premiums
    if not rc.has_rarc_run:
        return

    fx_rates_df = params.fx_rates.df() # Using fx from library

    for idx, layer in enumerate(layers):
        # get FX rates
        current_fx_to_usd = look_up(lookup_value=layer.currency, lookup_col="ccy", return_col="fx_rate", df=fx_rates_df, if_not_found=1)
        temp_fx_to_usd = look_up(lookup_value=layer.rate_change.temp_storage.currency, lookup_col="ccy", return_col="fx_rate", df=fx_rates_df, if_not_found=1)

        # Here we compare the annualised benchmark and quoted premiums, the temp storage premiums are already annualised
        is_bm_different = ((layer.benchmark_premium_annual_100 or 0) * current_fx_to_usd != (layer.rate_change.temp_storage.benchmark_premium  or 0)* temp_fx_to_usd) # from the library benchmark_premium is in line with the value assigned to expiring_technical_prem
        is_quoted_different = ((layer.quoted_premium_annual_100 or 0) * current_fx_to_usd != (layer.rate_change.temp_storage.quoted_premium or 0) * temp_fx_to_usd) # from the library quoted_premium is in line with the value assigned to expiring_actual_prem

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
    # Edit v0.2.4.1-Dev - Comment be below to have a stronger condition on error message
    # if is_bm_different or is_quoted_different:
    #     hx.errors.validation("'Calculate Rate Change' in the Rate Change page must be run again.")
    if rc.rarc_run_again_message is not None:
        hx.errors.validation("Rate Change: 'Calculate Rate Change' must be run again")

def assign_rc_renewal_nodes(rc_source_data, rc_data, annualise_renewal_factor, annualise_expiry_factor):
    """
    This function assigns values to the renewing rate change nodes, including the renewal premium at 100 percent for Beazley, policy term, and annualised. 
    It also populates table nodes with details such as limit, deductible, excess, and brokerage.
    """
    
    fx_rates_df = params.fx_rates.df()

    # Assign rate change renewal data
    rc_data.premium.line_100pct.annualised.renewal = (rc_source_data.quoted_premium_100 or 0) * annualise_renewal_factor
    rc_data.premium.beazley_line.annualised.renewal = (rc_source_data.quoted_premium_100 or 0) * annualise_renewal_factor * (rc_source_data.written_line or 1)
    rc_data.premium.line_100pct.policy_term.renewal = (rc_source_data.quoted_premium_100 or 0)
    rc_data.premium.beazley_line.policy_term.renewal = (rc_source_data.quoted_premium_100 or 0) * (rc_source_data.written_line or 1)

    rc_data.limit.renewal = rc_source_data.limit
    rc_data.deductible.renewal = rc_source_data.deductible
    rc_data.excess.renewal = rc_source_data.excess
    rc_data.brokerage.renewal = rc_source_data.brokerage
    rc_data.currency.renewal = rc_source_data.currency
    rc_data.market_cap.renewal = rc_source_data.market_cap
    rc_data.total_assets.renewal = rc_source_data.total_assets
    rc_data.insider_share.renewal = rc_source_data.insider_share
    rc_data.number_employees.renewal = rc_source_data.number_employees
    rc_data.mmp_flag.renewal = rc_source_data.mmp_flag
    
    # Assign rate change expiring data
    expiring_premium_policy_term_100 = rc_data.expiring_policy_info.expiring_quoted_premium_100 or 0
    rc_data.premium.line_100pct.annualised.expiring = expiring_premium_policy_term_100 * annualise_expiry_factor
    rc_data.premium.beazley_line.annualised.expiring = expiring_premium_policy_term_100 * annualise_expiry_factor * (rc_data.expiring_policy_info.expiring_written_line or 0)
    rc_data.premium.line_100pct.policy_term.expiring = expiring_premium_policy_term_100
    rc_data.premium.beazley_line.policy_term.expiring = expiring_premium_policy_term_100 * (rc_data.expiring_policy_info.expiring_written_line or 0)

    rc_data.limit.expiring = (rc_data.expiring_policy_info.expiring_limit or 0)
    rc_data.deductible.expiring = (rc_data.expiring_policy_info.expiring_deductible or 0)
    rc_data.excess.expiring = (rc_data.expiring_policy_info.expiring_excess or 0)
    rc_data.brokerage.expiring = (rc_data.expiring_policy_info.expiring_brokerage or 0)
    rc_data.currency.expiring = (rc_data.expiring_policy_info.expiring_currency or "USD")
    rc_data.market_cap.expiring = (rc_data.expiring_policy_info.expiring_market_cap or 0)
    rc_data.total_assets.expiring = (rc_data.expiring_policy_info.expiring_total_assets or 0)
    rc_data.insider_share.expiring = (rc_data.expiring_policy_info.expiring_insider_share or 0)
    rc_data.number_employees.expiring = (rc_data.expiring_policy_info.expiring_employees or 0)
    rc_data.mmp_flag.expiring = rc_data.expiring_policy_info.expiring_mmp_flag

    # get expiring and renewing fx
    # expiring_fx_to_usd = usd(value=1, ccy=rc_data.currency.expiring, ccy_table=params.fx_rates.df(), lookup_type="single")
    # renewing_fx_to_usd = usd(value=1, ccy=rc_data.currency.renewal, ccy_table=params.fx_rates.df(), lookup_type="single")
    expiring_fx_to_usd = look_up(lookup_value=rc_data.currency.expiring, lookup_col="ccy", return_col="fx_rate", df=fx_rates_df, if_not_found=1)
    renewing_fx_to_usd = look_up(lookup_value=rc_data.currency.renewal, lookup_col="ccy", return_col="fx_rate", df=fx_rates_df, if_not_found=1)
    
    # assign value to show_expiring
    rc_data.show_expiring_revalued = (rc_data.currency.expiring != rc_data.currency.renewal)
    
    revaluing_factor = ratio(renewing_fx_to_usd,expiring_fx_to_usd) if rc_data.show_expiring_revalued else 1
    
    # rc_data.premium.line_100pct.annualised.expiring = expiring_premium_annual = (rc_data.expiring_policy_info.expiring_quoted_premium_100 or 0)* (annualise_renewal_factor) 
    rc_data.premium.line_100pct.annualised.expiring_revalued = rc_data.premium.line_100pct.annualised.expiring * revaluing_factor
    rc_data.premium.beazley_line.annualised.expiring_revalued = rc_data.premium.beazley_line.annualised.expiring * revaluing_factor
    rc_data.premium.line_100pct.policy_term.expiring_revalued = rc_data.premium.line_100pct.policy_term.expiring * revaluing_factor
    rc_data.premium.beazley_line.policy_term.expiring_revalued = rc_data.premium.beazley_line.policy_term.expiring * revaluing_factor

    rc_data.limit.expiring_revalued = rc_data.limit.expiring * revaluing_factor
    rc_data.deductible.expiring_revalued = rc_data.deductible.expiring * revaluing_factor
    rc_data.excess.expiring_revalued = rc_data.excess.expiring * revaluing_factor
    rc_data.brokerage.expiring_revalued = rc_data.brokerage.expiring # same as expiring
    rc_data.currency.expiring_revalued = rc_data.currency.renewal # same as renewing
    rc_data.market_cap.expiring_revalued = rc_data.market_cap.expiring * revaluing_factor
    rc_data.total_assets.expiring_revalued = rc_data.total_assets.expiring * revaluing_factor
    rc_data.insider_share.expiring_revalued = rc_data.insider_share.expiring # same as expiring
    rc_data.number_employees.expiring_revalued = rc_data.number_employees.expiring # same as expiring
    rc_data.mmp_flag.expiring_revalued = rc_data.mmp_flag.expiring # same as expiring

    # Calculate rebased premium for each bucket
    rebased_premium_model = rebased_premium_uw = rc_data.premium.line_100pct.annualised.expiring or 0
    renewal_premium = rc_data.premium.line_100pct.annualised.renewal

    return rebased_premium_model, rebased_premium_uw, renewal_premium


    

