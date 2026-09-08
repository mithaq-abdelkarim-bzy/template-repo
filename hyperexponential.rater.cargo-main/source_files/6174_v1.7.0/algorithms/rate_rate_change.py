import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter
from algorithms.rate_constants import max_layers
from algorithms.rate_utilities import ratio

def rate_change_buckets(hxd):

    buckets_cargo = {
        "model": [], # Start from expiry data priced with current model
        "exposure": [
            "cds/term",
            "cds/layers/coverages/cargo_transit/trans_vals",
            "cds/layers/coverages/cargo_storage/stock_vals"
            ],
        "risk_characteristics": [
            "cds/layers/coverages/cargo_transit/transit_flag",
            "cds/layers/coverages/cargo_transit/wh_to_port_flag",
            "cds/layers/coverages/cargo_transit/loading_flag",
            "cds/layers/coverages/cargo_transit/voyage_flag",
            "cds/layers/coverages/cargo_transit/unloading_flag",
            "cds/layers/coverages/cargo_transit/port_to_wh_flag",
            "cds/layers/coverages/cargo_transit/commodity",
            "cds/layers/coverages/cargo_transit/packaging",
            "cds/layers/coverages/cargo_transit/conv_air_factor",
            "cds/layers/coverages/cargo_transit/conv_land_factor",
            "cds/layers/coverages/cargo_transit/conv_sea_factor",
            "cds/layers/coverages/cargo_transit/voyage",
            "cds/layers/coverages/cargo_transit/surveyor",
            "cds/layers/coverages/cargo_transit/vessel",
            "cds/layers/coverages/cargo_transit/uw_discretion",
            "cds/layers/coverages/cargo_transit/uw_discretion_factor",
            "cds/layers/coverages/cargo_storage/storage_flag",
            "cds/layers/coverages/cargo_storage/survey",
            "cds/layers/coverages/cargo_storage/risk_mgmt",
            "cds/layers/coverages/cargo_storage/risk_mgmt_factor",
            "cds/layers/coverages/cargo_storage/uw_discretion",
            "cds/layers/coverages/cargo_storage/uw_discretion_factor",
            "cds/layers/coverages/cargo_storage/avg_val_pcm",
            "cds/layers/coverages/cargo_storage/cat_expo",
            "cds/layers/coverages/cargo_storage/countries/country",
            "cds/layers/coverages/cargo_storage/countries/cat_expo",
            "cds/layers/coverages/cargo_storage/retail_expo",
            "cds/layers/coverages/cargo_storage/all_else_expo" # Override
        ],
        "deductible": [
            "cds/layers/coverages/cargo_transit/deductible_level",
            "cds/layers/coverages/cargo_transit/deductible_level_factor", # Override
            "cds/layers/coverages/cargo_transit/excess",
            "cds/layers/coverages/cargo_transit/excess_factor", # Override
            "cds/layers/coverages/cargo_storage/deductible_level",
            "cds/layers/coverages/cargo_storage/deductible_level_factor", # Override
            "cds/layers/coverages/cargo_storage/excess",
            "cds/layers/coverages/cargo_storage/excess_factor" # Override
        ],
        "limit": [],
        "terms_conditions": [
            "cds/layers/coverages/cargo_transit/type_of_cover",
            "cds/layers/coverages/cargo_storage/type_of_cover"
        ],
        "brokerage": [
            "cds/layers/brokerage"
        ],
        "other": []
    }
    buckets_cargo_cyber = {
        "model": [], # Start from expiry data priced with current model
        "exposure": [
            "cds/term",
            "cds/layers/coverages/cargo_cyber_transit/trans_vals",
            "cds/layers/coverages/cargo_storage/stock_vals"
            ],
        "risk_characteristics": [
            "cds/layers/coverages/cargo_cyber_transit/transit_flag",
            "cds/layers/coverages/cargo_cyber_transit/wh_to_port_flag",
            "cds/layers/coverages/cargo_cyber_transit/loading_flag",
            "cds/layers/coverages/cargo_cyber_transit/voyage_flag",
            "cds/layers/coverages/cargo_cyber_transit/unloading_flag",
            "cds/layers/coverages/cargo_cyber_transit/port_to_wh_flag",
            "cds/layers/coverages/cargo_cyber_transit/commodity",
            "cds/layers/coverages/cargo_cyber_transit/packaging",
            "cds/layers/coverages/cargo_cyber_transit/conv_air_factor",
            "cds/layers/coverages/cargo_cyber_transit/conv_land_factor",
            "cds/layers/coverages/cargo_cyber_transit/conv_sea_factor",
            "cds/layers/coverages/cargo_cyber_transit/voyage",
            "cds/layers/coverages/cargo_cyber_transit/surveyor",
            "cds/layers/coverages/cargo_cyber_transit/vessel",
            "cds/layers/coverages/cargo_cyber_transit/uw_discretion",
            "cds/layers/coverages/cargo_cyber_transit/uw_discretion_factor",
            "cds/layers/coverages/cargo_cyber_storage/storage_flag",
            "cds/layers/coverages/cargo_cyber_storage/survey",
            "cds/layers/coverages/cargo_cyber_storage/risk_mgmt",
            "cds/layers/coverages/cargo_cyber_storage/risk_mgmt_factor",
            "cds/layers/coverages/cargo_cyber_storage/uw_discretion",
            "cds/layers/coverages/cargo_cyber_storage/uw_discretion_factor",
            "cds/layers/coverages/cargo_cyber_storage/avg_val_pcm",
            "cds/layers/coverages/cargo_cyber_storage/cat_expo",
            "cds/layers/coverages/cargo_cyber_storage/countries/country",
            "cds/layers/coverages/cargo_cyber_storage/countries/cat_expo",
            "cds/layers/coverages/cargo_cyber_storage/retail_expo",
            "cds/layers/coverages/cargo_cyber_storage/all_else_expo" # Override
        ],
        "deductible": [
            "cds/layers/coverages/cargo_cyber_transit/deductible_level",
            "cds/layers/coverages/cargo_cyber_transit/deductible_level_factor", # Override
            "cds/layers/coverages/cargo_cyber_transit/excess",
            "cds/layers/coverages/cargo_cyber_transit/excess_factor", # Override
            "cds/layers/coverages/cargo_cyber_storage/deductible_level",
            "cds/layers/coverages/cargo_cyber_storage/deductible_level_factor", # Override
            "cds/layers/coverages/cargo_cyber_storage/excess",
            "cds/layers/coverages/cargo_cyber_storage/excess_factor" # Override
        ],
        "limit": [],
        "terms_conditions": [
            "cds/layers/coverages/cargo_cyber_transit/type_of_cover",
            "cds/layers/coverages/cargo_cyber_storage/type_of_cover"
        ],
        "brokerage": [
            "cds/layers/brokerage"
        ],
        "other": []
    }


    buckets_specie = {
        "model": [], # Start from expiry data priced with current model
        "exposure": [
            "cds/term",
            "cds/layers/coverages/specie_transit/trans_vals",
            "cds/layers/coverages/specie_storage/stock_vals",
            "cds/layers/coverages/specie_storage/non_cat_expo"
            ],
        "risk_characteristics": [
            "cds/layers/coverages/specie_transit/transit_flag",
            "cds/layers/coverages/specie_transit/commodity",
            "cds/layers/coverages/specie_transit/uw_discretion",
            "cds/layers/coverages/specie_transit/uw_discretion_factor",
            "cds/layers/coverages/specie_storage/storage_flag",
            "cds/layers/coverages/specie_storage/commodity",
            "cds/layers/coverages/specie_storage/survey",
            "cds/layers/coverages/specie_storage/risk_mgmt",
            "cds/layers/coverages/specie_storage/risk_mgmt_factor",
            "cds/layers/coverages/specie_storage/uw_discretion",
            "cds/layers/coverages/specie_storage/uw_discretion_factor",
            "cds/layers/coverages/specie_storage/avg_val_pcm",
            "cds/layers/coverages/specie_storage/cat_expo",
            "cds/layers/coverages/specie_storage/countries/country",
            "cds/layers/coverages/specie_storage/countries/cat_expo"
        ],
        "deductible": [
            "cds/layers/coverages/specie_transit/deductible_level",
            "cds/layers/coverages/specie_transit/excess",
            "cds/layers/coverages/specie_transit/excess_factor", # Override
            "cds/layers/coverages/specie_storage/deductible_level",
            "cds/layers/coverages/specie_storage/excess",
            "cds/layers/coverages/specie_storage/excess_factor" # Override
        ],
        "limit": [],
        "terms_conditions": [
            "cds/layers/coverages/specie_transit/type_of_cover",
            "cds/layers/coverages/specie_storage/type_of_cover"
        ],
        "brokerage": [
            "cds/layers/brokerage"
        ],
        "other": []
    }

    buckets_conloss = {
        "model": [], # Start from expiry data priced with current model
        "exposure": [
            "cds/layers/coverages/conloss_transit/trans_vals"
            ],
        "risk_characteristics": [
            "cds/layers/coverages/conloss_transit/transit_flag",
            "cds/layers/coverages/conloss_transit/packaging_1",
            "cds/layers/coverages/conloss_transit/packaging_2",
            "cds/layers/coverages/conloss_transit/packaging_1_factor",
            "cds/layers/coverages/conloss_transit/packaging_2_factor",
            "cds/layers/coverages/conloss_transit/conv_air_factor",
            "cds/layers/coverages/conloss_transit/conv_land_factor",
            "cds/layers/coverages/conloss_transit/conv_sea_factor",
            "cds/layers/coverages/conloss_transit/voyage",
            "cds/layers/coverages/conloss_transit/surveyor",
            "cds/layers/coverages/conloss_transit/vessel",
            "cds/layers/coverages/conloss_transit/uw_discretion",
            "cds/layers/coverages/conloss_transit/uw_discretion_factor",
            "cds/layers/coverages/conloss/conloss_flag",
            "cds/layers/coverages/conloss/exposure",
            "cds/layers/coverages/conloss/uw_discretion",
            "cds/layers/coverages/conloss/uw_discretion_factor"
        ],
        "deductible": [
            "cds/layers/coverages/conloss_transit/deductible_level",
            "cds/layers/coverages/conloss/deductible_level"
        ],
        "limit": [
            "cds/layers/coverages/conloss/limit"
        ],
        "terms_conditions": [
            "cds/layers/coverages/conloss_transit/type_of_cover",
            "cds/layers/coverages/conloss/indemnity_period"
        ],
        "brokerage": [
            "cds/layers/brokerage"
        ],
        "other": []
    }

    # Return correct buckets depending on coverage
    if hxd.cds.cover_selection.is_cargo:
        return buckets_cargo
    elif hxd.cds.cover_selection.is_specie:
        return buckets_specie
    elif hxd.cds.cover_selection.is_conloss:
        return buckets_conloss
    elif hxd.cds.cover_selection.is_cargo_cyber_combined:
        return buckets_cargo_cyber
    

def rate_rate_change(hxd):

    layer = hxd.cds.layers[0]
    rc = layer.rate_change
    exp = layer.rate_change.expiring_policy_info
    hxd.cds.rate_change.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id

    # Define conditions for function to run
    has_expiring_data = hxd.cds.rate_change.has_expiring_data = (exp.expiring_premium is not None) and (exp.expiring_written_line is not None)

    # Exit if condition is not satisfied
    if not has_expiring_data:
        return
    
    # --- Continue with the rate change calculation - populate expiring vs. renewal data
    rc.premium_policy_term_100pct.renewal = layer.quoted_premium
    rc.premium_policy_term_beazley_share.renewal = layer.quoted_premium * layer.written_line

    rc.premium_policy_term_100pct.expiring = exp.expiring_premium
    rc.premium_policy_term_beazley_share.expiring = exp.expiring_premium * exp.expiring_written_line

    rc.written_line.expiring = exp.expiring_written_line
    rc.written_line.renewal = layer.written_line

    rc.benchmark_premium.expiring = exp.expiring_benchmark_premium
    rc.benchmark_premium.renewal = layer.benchmark_premium
    rc.bpi.expiring = exp.expiring_bpi
    rc.bpi.renewal = layer.bpi

    rc.technical_premium.expiring = exp.expiring_technical_premium
    rc.technical_premium.renewal = layer.technical_premium
    rc.tpi.expiring = exp.expiring_tpi
    rc.tpi.renewal = layer.tpi

    # For layers not used in the pricing summary, the rate change is hidden
    num_layers = len(hxd.cds.layers)
    for index in range(1, max_layers+1):
        setattr(hxd.cds.rate_change, f"show_layer_{index}", True) if index <= num_layers else False

    rebased_premium_model = rebased_premium_uw = exp.expiring_premium or 0

    for layer in hxd.cds.layers:
        # Initialise list to check all changes are filled in
        rate_changes = []

        for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "brokerage_change", "other_change"]:
            # Calculate rebased premium based on % changes
            rc_vbl = getattr(layer.rate_change, item)
            rc_vbl.uw_selected.calculated = rc_vbl.model_calculated
            rebased_premium_model *= rc_vbl.model_calculated or 0
            rebased_premium_uw *= rc_vbl.uw_selected.selected or 0

            # Add selected change to list
            rate_changes.append(rc_vbl.uw_selected.selected)
            
            # Validate overrides if unexplained
            if rc_vbl.uw_selected.is_overridden is True and rc_vbl.comments is None:
                hx.errors.validation(f"Rate Change: {(title_rc(item))} has been overridden and no comment provided")

        # Calculate final rate change with overrides
        renewal_premium = layer.quoted_premium

        model_rarc = ratio(renewal_premium, rebased_premium_model, 1)
        final_rarc = ratio(renewal_premium, rebased_premium_uw, 1)

        layer.rate_change.rate_change.model_calculated = model_rarc
        layer.rate_change.risk_adjusted_rate_change.uw_selected = layer.rate_change.rate_change.uw_selected = final_rarc

        # Prompt user to run calcs again if premium changes
        is_bm_different = layer.rate_change.temp_storage.benchmark_premium and (layer.benchmark_premium != layer.rate_change.temp_storage.benchmark_premium)
        is_quoted_different = layer.rate_change.temp_storage.quoted_premium and (layer.quoted_premium != layer.rate_change.temp_storage.quoted_premium)
        rarc_message = ""
        rarc_message_show = False
        previous_bm_prem = "{:,.0f}".format(layer.rate_change.temp_storage.benchmark_premium or 0)
        previous_quoted_prem = "{:,.0f}".format(layer.rate_change.temp_storage.quoted_premium or 0)
        current_bm_prem = "{:,.0f}".format(layer.benchmark_premium or 0)
        current_quoted_prem = "{:,.0f}".format(layer.quoted_premium)

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
        

        



    



