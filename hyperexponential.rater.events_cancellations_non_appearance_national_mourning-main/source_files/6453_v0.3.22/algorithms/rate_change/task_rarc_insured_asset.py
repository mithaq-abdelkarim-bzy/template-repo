# v0.5.0
import hx, os, json,copy
import pandas as pd
import numpy as np

from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from libraries.rate_change_insured_asset.algorithms.rate_change import RateChange as RateChangeLib # Edit v0.5.0 - Library for Rate change with insured asset

from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import COVERAGES_LIST
from algorithms.rate_rate_change import RATE_CHANGE_BUCKETS, EXP_INPUTS_IN_CCY, define_insured_asset_list_variable # Edit v0.3.0
from algorithms import parameter_tables_schema as params

from algorithms.rate_change.task_rarc_expiry_policy_fetch import task_expiring_policy_fetch, task_expiring_policy_fetch_coverage

from algorithms.rate_utilities import nan_to_none

def calculate_rate_change(rate_change_lib, kw_args):
    """
    Send the rate change library object and the kw arguments to the rate change library
    Return in rarc_df and the rarc_list. The latter include the model impact
    """
    rate_change_lib.calculate_repriced_values(**kw_args)
    rarc_df, rarc_list = rate_change_lib.calculate_rarc_by_layer()
    return rarc_df, rarc_list

def clean_expiring_data(hxd, expiring_data, insured_asset_list_name):
    """
    Sorts the expiring insured assets in the same order as the renewing insured assets using a unique_id.
    Renewal may have additional aircrafts which are not present in expiring; they will be added at the end of the list.
    If 'split' is set to True, returns two expiring_data dictionaries:
        - expiring_data_common: contains the sorted list of insured assets that are common between expiring and renewal;
        - expiring_data_others: contains the list of additional insured assets that are present in renewal but not in expiring.
    """
    # Get the expiring list of insured assets
    expiring_list = expiring_data["cds"]["exposure"]["granular"][insured_asset_list_name]
   
    # load insured assets list from rate change staging area
    renewal_list = json.loads(getattr(hxd.cds.rate_change.insured_asset_list,insured_asset_list_name))
    
    # Create a dictionary with key value pair set equal to unique Id, idx to capture the order of keys from the renewal list
    renewal_order = {insured_asset["unique_id"]: idx for idx, insured_asset in enumerate(renewal_list)}

    # Create a list of expiring insured assets that renewed
    common = [exp_insured_asset for exp_insured_asset in expiring_list if exp_insured_asset["unique_id"] in renewal_order]
    
    # Create a list of expiring insured asset that did not renew. Others contains New and Lapsed insured asset
    others = [exp_insured_asset for exp_insured_asset in expiring_list if exp_insured_asset["unique_id"] not in renewal_order]

    # Sort items present in the renewal_order
    common.sort(key=lambda insured_asset: renewal_order[insured_asset["unique_id"]])
    sorted_expiring_list = common + others

    expiring_data_sorted = copy.deepcopy(expiring_data)
    expiring_data_sorted["cds"]["exposure"]["granular"][insured_asset_list_name] = sorted_expiring_list

    # Build a set of keys from the expiring list and renewal list
    expiring_keys = {item["unique_id"] for item in sorted_expiring_list}
    renewal_keys = {item["unique_id"] for item in renewal_list}

    # Partition the renewal list based on renewal_keys and expiring_keys
    expiring_list_common = [item for item in sorted_expiring_list if item["unique_id"] in renewal_keys]
    renewal_list_others = [item for item in renewal_list if item["unique_id"] not in expiring_keys]
    expiring_list_dropped = [item for item in sorted_expiring_list if item["unique_id"] not in renewal_keys]

    # Creating independent copy of expiry_data for common, others and dropped. The insured assets list will be trimmed in the next step
    expiring_data_common = copy.deepcopy(expiring_data)
    expiring_data_others = copy.deepcopy(expiring_data)  # Calling this expiring_data even though the specified list will contain renewal elements
    expiring_data_dropped = copy.deepcopy(expiring_data)

    # Filter the insured assets of the expiry data for common, others and dropped
    expiring_data_common["cds"]["exposure"]["granular"][insured_asset_list_name] = expiring_list_common
    expiring_data_others["cds"]["exposure"]["granular"][insured_asset_list_name] = renewal_list_others
    expiring_data_dropped["cds"]["exposure"]["granular"][insured_asset_list_name] = expiring_list_dropped

    return (
        expiring_data_sorted,
        expiring_data_common,
        expiring_data_others,
        expiring_data_dropped,
    )

def task_rarc_layer_insured_asset(hxd, progress):
    """
    This rate change process uses the rate change library to perform calculations and stores the results for each bucket in the rate change Data Schema at the layer-level.
    Steps for Each Bucket:
    - A temporary data schema (transient HXD) is created using the expiring data.
    - Only the inputs relevant to the bucket scope are aligned with the renewing policy.
    - The library applies the rating calculation to compute the rebased premium.
    Notes:
    - Some temporary results are stored in the data schema for validation purposes.
    - This function uses the library rate_change_insured_asset versionned 2.X 
    For non-insured asset use, use the library rate_change library versionned 1.x
    """
    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Get Expiring Data with any data transformation from task_expiring_policy_fetch
    expiring_data = task_expiring_policy_fetch(hxd, progress)

    # Get expiring data but remove bloating from dynamic dropdown data and other section.
    expiring_data = {
        "cds": expiring_data["cds"],
        "hx_core": expiring_data["hx_core"],
    }

    # NOTE: Align Expiring Data Schema to Current Data Schema to use the rate change feature without issues.
    # - Add new node to the expiring data and assign their value
    # - Reassign existing node if there was a change in definition
    # - Delete node that are not present in the current data schema

    # Get data Schema static copy path
    data_schema_static_filename = "data_schema/data_schema_static_copy.py"
    # data_schema_static_path = os.path.join(os.path.dirname(__file__), data_schema_static_filename) # v0.5.0 Use when this file location is within editing/algorithms
    current_dir = os.path.dirname(__file__)
    data_schema_static_path = os.path.join(os.path.dirname(current_dir), data_schema_static_filename)

    # NOTE: Provide the path of the input value node and the corresponding currency
    fx_rates_df = params.fx_rates.df() # NOTE: if using fx from library
    # fx_rates_df = hx.params.table_currency # NOTE: if using fx from params

    rc_result={}

    # Get the rate change buckets 
    buckets = RATE_CHANGE_BUCKETS["layers"]
    # Get the expiring_inputs_in_ccy information to revalue in case of change in currency at renewal
    # NOTE: Provide the path of the input value node and the corresponding currency. DO NOT Provide output Node
    expiring_inputs_in_ccy_cvg = EXP_INPUTS_IN_CCY["layers"]
    # Prepare arguments for calculate_repriced_values() function
    (
        expiring_data_sorted,
        expiring_data_common,
        expiring_data_others,
        expiring_data_dropped,
    ) = clean_expiring_data(hxd, expiring_data, insured_asset_list_name = "layers" )
    
    kw_args = {
        "custom_expiring_data": [
            dict(expiring_data_sorted),
            dict(expiring_data_common),
            dict(expiring_data_others),
            dict(expiring_data_dropped),
        ],
        "split_list_path": f"cds/exposure/granular/layers",
        "matching_key": "unique_id",
        "additional_items_bucket": "exposure", 
    }

    # Rate Change with transient_hxd
    rc = RateChangeLib(
        hxd=hxd,
        progress=progress,
        buckets=buckets,
        layers_path=f"cds/layers",
        expiring_actual_prem="quoted_premium_annual_100",
        expiring_technical_prem="benchmark_premium_annual_100",
        expiring_currency="currency",
        async_tasks=[],
        data_schema_static_path=data_schema_static_path
    )

    # Store the results
    rc_result[f'layers_rarc_df'], rc_result['layers_rarc_list'] = calculate_rate_change(rc, kw_args)

    # remove the nan by none to prevent any future assignemnt issue
    # rc_result[f'layers_rarc_df'] = rc_result[f'layers_rarc_df'].where(pd.notnull(rc_result[f'layers_rarc_df']), None)
    
    rc_result[f'layers_rarc_df'] = nan_to_none(rc_result[f'layers_rarc_df'])
    # # NOTE: for debugging if needed
    # pd.set_option('display.max_columns', None)
    # print(rc_result['layers_rarc_df'])
    # print(rc_result['layers_rarc_list'])
    
    # Store result in hxd
    for rarc_layer, hxd_layer in zip(rc_result['layers_rarc_list'] , hxd.cds.layers):
        # Store data in the temp_storage structure, this include, quoted_premium_100, benchmark_100 and currency
        hxd_layer.rate_change.temp_storage = rarc_layer["temp_storage"]
        rarc_layer.pop("temp_storage")

        if hxd_layer.rate_change.renewing_layer==True:
            # populate bucket change for Renewing Layer. No calculation for New Layer.
            for key, value in rarc_layer.items():
                setattr(hxd_layer.rate_change,key, value)
            # Calculate brokerage change for storage but not display
            expiring_brokerage = hxd_layer.rate_change.expiring_policy_info.expiring_brokerage or 0
            renewal_brokerage = hxd_layer.brokerage or 0
            brokerage_change = (1 - expiring_brokerage) / (1 - renewal_brokerage)
            hxd_layer.rate_change.brokerage_change.model_calculated = brokerage_change
 
        # Store bucket impact in hxd
        for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
            rc_vbl = getattr(hxd_layer.rate_change, item)
            # NOTE: ONLY for legacy model. Not necessary for a first build.
            # Assignment in tasks instead of rating (rate_rate_change(hxd)) to clear out the overrides at the creation of the renewal
            # rc_vbl.uw_selected.calculated = rc_vbl.model_calculated # Edit v0.5.0 Legacy model only.

    # Confirm task has been run
    hxd.cds.rate_change.has_rarc_run = True
    hxd.cds.rate_change.has_rarc_not_run = False

def task_rarc_coverage_insured_asset(hxd, progress):
    """
    The rate change process uses the rate change library to perform calculations and stores the results for each bucket in the rate change Data Schema at the coverage level.
    Steps for Each Bucket:
    - A temporary data schema (transient HXD) is created using the expiring data.
    - Only the inputs relevant to the bucket scope are aligned with the renewing policy.
    - The library applies the rating calculation to compute the rebased value.
    Notes:
    - Some temporary results are stored in the data schema for validation purposes.
    - This function uses the library rate_change_insured_asset versionned 2.X 
    For non-insured asset use, use the library rate_change library versionned 1.x
    """
    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Get Expiring Data with any data transformation from task_expiring_policy_fetch_coverage
    expiring_data = task_expiring_policy_fetch_coverage(hxd, progress)

    # Get expiring data but remove bloating from dynamic dropdown data
    expiring_data = {
        "cds": expiring_data["cds"],
        "hx_core": expiring_data["hx_core"],
    }
    
    # NOTE: Align Expiring Data Schema to Current Data Schema to use the rate change feature without issues.
    # - Add new node to the expiring data and assign their value
    # - Reassign existing node if there was a change in definition
    # - Delete node that are not present in the current data schema

    # Get data Schema static copy path
    data_schema_static_filename = "data_schema/data_schema_static_copy.py"
    # data_schema_static_path = os.path.join(os.path.dirname(__file__), data_schema_static_filename) # v0.5.0 Use when this file location is within editing/algorithms
    current_dir = os.path.dirname(__file__)
    data_schema_static_path = os.path.join(os.path.dirname(current_dir), data_schema_static_filename)

    # NOTE: Provide the path of the input value node and the corresponding currency
    fx_rates_df = params.fx_rates.df() # NOTE: if using fx from library
    # fx_rates_df = hx.params.table_currency # NOTE: if using fx from params

    rc_result={}
    for coverage in COVERAGES_LIST:
        # Get the rate change buckets based on the coverage name
        buckets = RATE_CHANGE_BUCKETS[coverage]
        # Get the expiring_inputs_in_ccy information to revalue in case of change in currency at renewal
        # NOTE: Provide the path of the input value node and the corresponding currency. DO NOT Provide output Node
        expiring_inputs_in_ccy_cvg = EXP_INPUTS_IN_CCY[coverage]
        # Prepare arguments for calculate_repriced_values() function
        (
            expiring_data_sorted,
            expiring_data_common,
            expiring_data_others,
            expiring_data_dropped,
        ) = clean_expiring_data(hxd, expiring_data, coverage )
        
        kw_args = {
            "custom_expiring_data": [
                dict(expiring_data_sorted),
                dict(expiring_data_common),
                dict(expiring_data_others),
                dict(expiring_data_dropped),
            ],
            "split_list_path": f"cds/exposure/granular/{coverage}",
            "matching_key": "unique_id",
            "additional_items_bucket": "exposure", 
        }

        # Rate Change with transient_hxd
        rc = RateChangeLib(
            hxd=hxd,
            progress=progress,
            buckets=buckets,
            layers_path=f"cds/layers",
            expiring_actual_prem=f"coverages/{coverage}/quoted_premium_annual_100",
            expiring_technical_prem=f"coverages/{coverage}/benchmark_premium_annual_100",
            expiring_currency=f"coverages/{coverage}/currency",
            async_tasks=[],
            data_schema_static_path=data_schema_static_path
        )

        # Store the results
        rc_result[f'{coverage}_rarc_df'], rc_result[f'{coverage}_rarc_list'] = calculate_rate_change(rc, kw_args)
    
        # remove the nan by none
        rc_result[f'{coverage}_rarc_df'] = rc_result[f'{coverage}_rarc_df'].where(pd.notnull(rc_result[f'{coverage}_rarc_df']), None)
        
    # # # NOTE: for debugging if needed
    # pd.set_option('display.max_columns', None)
    # print(rc_result[f'{coverage}_rarc_df'])
    # print(rc_result[f'{coverage}_rarc_list'])
        
    # Push to hxd
    for coverage in COVERAGES_LIST:
        for rarc_layer, hxd_layer in zip(rc_result[f'{coverage}_rarc_list'] , hxd.cds.layers):
            # Store data in the temp_storage structure, this includes, quoted_premium_100, benchmark_100 and currency
            getattr(hxd_layer.rate_change, coverage).temp_storage = rarc_layer["temp_storage"]
            rarc_layer.pop("temp_storage")

            if hxd_layer.rate_change.renewing_layer==True:
                # populate bucket change for Renewing Layer. No data stored for new layer.
                for key, value in rarc_layer.items():
                    setattr(getattr(hxd_layer.rate_change, coverage), key, value)
                # Calculate brokerage change for storage but not display
                expiring_brokerage = getattr(hxd_layer.rate_change, coverage).expiring_policy_info.expiring_brokerage or 0
                renewal_brokerage = getattr(getattr(hxd_layer, "coverages"), coverage).brokerage or 0
                brokerage_change = (1 - expiring_brokerage) / (1 - renewal_brokerage)
                getattr(hxd_layer.rate_change, coverage).brokerage_change.model_calculated = brokerage_change
                
            # Store bucket impact in hxd
            for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
                rc_vbl = getattr(getattr(hxd_layer.rate_change, coverage), item)
                # NOTE: ONLY for legacy model. Not necessary for a first build. 
                # Assignment in tasks instead of rating (rate_rate_change(hxd)) to clear out the overrides at the creation of the renewal
                # rc_vbl.uw_selected.calculated = rc_vbl.model_calculated # Edit v0.5.0 Legacy model only.

    # Confirm task has been run
    hxd.cds.rate_change.has_rarc_run = True
    hxd.cds.rate_change.has_rarc_not_run = False