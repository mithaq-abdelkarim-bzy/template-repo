# v0.5.0
import hx, os, json, requests, openpyxl, copy

from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api

import datetime

from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import COVERAGES_LIST

def assign_expiry_nodes_rate_change(rc_source_data, rc_data): # Edit v0.3.0
    """
    Assigns values to expiring rate change nodes necessary in the Rate Change Page.
    This function is applicable for both layer-level and coverage-level rate changes.

    """
    # Expiring info
    rc_data.expiring_policy_info.expiring_quoted_premium_100        = rc_source_data["quoted_premium_100"]    
    rc_data.expiring_policy_info.expiring_quoted_premium_annual_100 = rc_source_data["quoted_premium_annual_100"]
    rc_data.expiring_policy_info.expiring_quoted_premium            = rc_source_data["quoted_premium"]    
    rc_data.expiring_policy_info.expiring_quoted_premium_annual     = rc_source_data["quoted_premium_annual"]
    if not RARC_INSURED_ASSET_USE:
        rc_data.expiring_policy_info.expiring_limit         = rc_source_data["limit"]
        rc_data.expiring_policy_info.expiring_excess        = rc_source_data["excess"]    
        rc_data.expiring_policy_info.expiring_deductible    = rc_source_data["deductible"]
    rc_data.expiring_policy_info.expiring_brokerage         = rc_source_data["brokerage"] or 0
    rc_data.expiring_policy_info.expiring_currency          = rc_source_data["currency"]
    return

def task_expiring_policy_fetch(hxd, progress):
    '''
    Import expiring data used in the rate change page from an expiring policy option.
    This function is applicable for layer-level only. For coverage-level, use task_expiring_policy_fetch_coverage.
    NOTE:
    - Compulsory: ensure the expiring data is aligned with the current Data Schema. Data transformations may be required.
    - the resulting expiring data will be used in the rate change calculation.
    '''
    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id =  hxd.cds.rate_change.expiring_policy_option_id.selected # 395204 # NOTE: use hardcoded ID for debugging if needed
    expiring_response         = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False)

    if expiring_response.status_code != 200:
        raise Exception(expiring_response.json())

    expiring_data = expiring_response.json()["data"]

    # NOTE: Align Expiring Data Schema to Current Data Schema to use the rate change feature without issues.
    # - Add new node to the expiring data and assign their value
    # - Reassign existing node if there was a change in definition
    # - Delete node that are not present in the current data schema
    # NOTE: Deletion Example 
    # for layer in expiring_data["cds"]["layers"]:
    #     expiring_policy_info = layer["rate_change"]["expiring_policy_info"]
    #     expiring_policy_info.pop("expiring_benchmark_premium_annual_100", None)


    # Get fields from json response and push to hxd
    expiring_layers_len = len(expiring_data["cds"]["layers"])
    layer_mapping = {}

    for idx, layer in enumerate(hxd.cds.layers):
        # Throw error if expiring layer doesn't exist
        if isinstance(layer.rate_change.expiring_layer,int):
            if layer.rate_change.expiring_layer > expiring_layers_len:
                hx.errors.fatal(f"Expiring Layer {layer.rate_change.expiring_layer}, mapped to Renewal Layer {idx+1}, does not exist. Number of expiring layers is {expiring_layers_len}.")

        if layer.rate_change.renewing_layer == True:
            # populate the expiry layer only if the layer is a renewing layer
            mapped_expiring_layer_idx = layer.rate_change.expiring_layer - 1
            assign_expiry_nodes_rate_change(
                rc_source_data = expiring_data["cds"]["layers"][mapped_expiring_layer_idx], 
                rc_data=layer.rate_change
                )
                
        # Save layer mapping
        layer_mapping[str(idx+1)] = layer.rate_change.expiring_layer

    # save mapping before assigment
    hxd.cds.rate_change.layer_mapping = json.dumps(layer_mapping)
    
    # Confirm task has been run
    hxd.cds.rate_change.has_fetch_run = True
    hxd.cds.rate_change.has_fetch_not_run = False

    return (expiring_data)

def task_expiring_policy_fetch_coverage(hxd, progress):
    '''
    Import expiring data used in the rate change page from an expiring policy option.
    This function is applicable for coverage-level only. For layer-level, use task_expiring_policy_fetch.
    NOTE:
    - Compulsory: ensure the expiring data is aligned with the current Data Schema. Data transformations may be required.
    - The resulting expiring data will be used in the rate change calculation.
    '''
    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id =  hxd.cds.rate_change.expiring_policy_option_id.selected # 395204 # NOTE: use hardcoded ID for debugging if needed
    expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False)

    if expiring_response.status_code != 200:
        raise Exception(expiring_response.json())

    expiring_data = expiring_response.json()["data"]

    # NOTE: Align Expiring Data Schema to Current Data Schema to use the rate change feature without issues.
    # - Add new node to the expiring data and assign their value
    # - Reassign existing node if there was a change in definition
    # - Delete node that are not present in the current data schema
    # NOTE Deletion example
    # for layer in expiring_data["cds"]["layers"]:
    #     keys_to_remove = [
    #         "expiring_benchmark_premium_annual_100",
    #     ]
    #     for cvg in COVERAGES_LIST:
    #         expiring_policy_info = layer["rate_change"][cvg]["expiring_policy_info"]
    #         for key in keys_to_remove:
    #             expiring_policy_info.pop(key, None)


    # Get fields from json response and push to hxd
    expiring_layers_len = len(expiring_data["cds"]["layers"])
    layer_mapping = {}
    
    for idx, layer in enumerate(hxd.cds.layers):
        # Error message if expiring layer doesn't exist
        if isinstance(layer.rate_change.expiring_layer,int):
            if layer.rate_change.expiring_layer > expiring_layers_len:
                hx.errors.fatal(f"Expiring Layer {layer.rate_change.expiring_layer}, mapped to Renewal Layer {idx+1}, does not exist. Number of expiring layers is {expiring_layers_len}.")

        if layer.rate_change.renewing_layer == True:
            mapped_expiring_layer_idx = layer.rate_change.expiring_layer - 1

            for coverage in COVERAGES_LIST:
                assign_expiry_nodes_rate_change(\
                    rc_source_data = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["coverages"][coverage], \
                    rc_data = getattr(layer.rate_change,coverage)
                    )
        # Save layer mapping
        layer_mapping[str(idx+1)] = layer.rate_change.expiring_layer

    hxd.cds.rate_change.layer_mapping = json.dumps(layer_mapping)

    # Confirm task has been run
    hxd.cds.rate_change.has_fetch_run = True
    hxd.cds.rate_change.has_fetch_not_run = False
    return (expiring_data)