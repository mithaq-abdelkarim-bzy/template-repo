# v0.5.0
import hx, os, json, requests, openpyxl, copy
import pandas as pd
import numpy as np
import datetime

from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from libraries.rate_change.algorithms.rate_change import RateChange as RateChangeLib

from algorithms.year_frac import basis1 # Edit v0.3.0 Import from year_frac to replicate yearfrac function, basis 1
from algorithms.rate_utilities import policy_term

from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import COVERAGES_LIST
from algorithms.rate_rate_change import RATE_CHANGE_BUCKETS, EXP_INPUTS_IN_CCY, define_insured_asset_list_variable # Edit v0.3.0
from algorithms import parameter_tables_schema as params

from algorithms.rate_change.task_rarc_expiry_policy_fetch import task_expiring_policy_fetch, task_expiring_policy_fetch_coverage

def task_rarc_layer(hxd, progress):
    """
    This rate change process uses the rate change library to perform calculations and stores the results for each bucket in the rate change Data Schema at the layer-level.
    Steps for Each Bucket:
    - A temporary data schema (transient HXD) is created using the expiring data.
    - Only the inputs relevant to the bucket scope are aligned with the renewing policy.
    - The library applies the rating calculation to compute the rebased value.
    Notes:
    - Some temporary results are stored in the data schema for validation purposes.
    - For insured asset use, use the rate_change_insured_asset library version 2.x instead of version 1.x.
    """
    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Get Expiring Data with any data transformation from task_expiring_policy_fetch
    expiring_data = task_expiring_policy_fetch(hxd, progress)

    # Get expiring data but remove bloating from dynamic dropdown data
    expiring_data = {
        "cds": expiring_data["cds"],
        "hx_core": expiring_data["hx_core"],
    }

    # NOTE: Align Expiring Data Schema to Current Data Schema to use the rate change feature without issues.
    # Add new node and assign their value
    # Reassign existing node if there was a change in definition
    # Delete Node that are not present in the current data schema

    # Get data Schema static copy path
    data_schema_static_filename = "data_schema/data_schema_static_copy.py"
    # data_schema_static_path = os.path.join(os.path.dirname(__file__), data_schema_static_filename) # v0.5.0 Use when this file location is within editing/algorithms
    current_dir = os.path.dirname(__file__)
    data_schema_static_path = os.path.join(os.path.dirname(current_dir), data_schema_static_filename)

    # Get the fx table
    fx_rates_df = params.fx_rates.df() # Using fx from library
    # fx_rates_df = hx.params.table_currency # Using fx from params

    # Get buckets 
    buckets = RATE_CHANGE_BUCKETS
    # Get the expiring_inputs_in_ccy information to revalue in case of change in currency at renewal
    # NOTE: Provide the path of the input value node and the corresponding currency. DO NOT Provide output Node
    expiring_inputs_in_ccy = EXP_INPUTS_IN_CCY["layers"]

    # Prepare arguments for calculate_repriced_values() function
    kw_args = {
        "expiring_inputs_in_ccy": expiring_inputs_in_ccy, # list of tuples
        "fx_table": fx_rates_df 
    }
    # Rate Change with transient_hxd
    rc = RateChangeLib(
        hxd=hxd,
        progress=progress,
        buckets=buckets,
        layers_path="cds/layers",
        expiring_actual_prem="quoted_premium_annual_100",
        expiring_technical_prem="benchmark_premium_annual_100", 
        expiring_currency="currency",
        async_tasks=[],  # Pass the actual tasks name as a variable, not a string
        data_schema_static_path=data_schema_static_path
    )

    rc.calculate_repriced_values(
        expiring_data = expiring_data, # NOTE: this allows to use the expiry data with aligned Data Schema
        **kw_args
    )
    # Use the repriced values to calculate the changes for each bucket
    rarc_df, rarc_list = rc.calculate_rarc_by_layer()

    # remove the nan by none
    rarc_df = rarc_df.where(pd.notnull(rarc_df), None)
    
    # # NOTE: for debugging if needed
    # pd.set_option('display.max_columns', None)
    # print(rarc_df)
    # print(rarc_list)

    # Push to hxd
    for rarc_layer, hxd_layer in zip(rarc_list, hxd.cds.layers):
        # Store data in the temp_storage structure, this includes, quoted_premium_100, benchmark_100 and currency
        hxd_layer.rate_change.temp_storage = rarc_layer["temp_storage"]
        rarc_layer.pop("temp_storage")

        # Only populate bucket change for Renewing Layer. No calculation for New Layer.
        if hxd_layer.rate_change.renewing_layer==True: # EDIT v0.3.0
            # populate bucket change for Renewing Layer. No data stored for new layer.
            for key, value in rarc_layer.items():
                setattr(hxd_layer.rate_change, key, value)
            # Calculate brokerage change for storage but not display
            expiring_brokerage = hxd_layer.rate_change.expiring_policy_info.expiring_brokerage or 0
            renewal_brokerage = hxd_layer.brokerage or 0
            hxd_layer.rate_change.brokerage_change.model_calculated = (1 - expiring_brokerage) / (1 - renewal_brokerage)

            for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
                rc_vbl = getattr(hxd_layer.rate_change, item)
                # NOTE: ONLY for legacy model. NOt necessary for a first build. 
                # Assignment in tasks instead of rating (rate_rate_change(hxd)) to clear out the overrides at the creation of the renewal
                # rc_vbl.uw_selected.calculated = rc_vbl.model_calculated # Edit v0.5.0 Legacy model only.
            
    # Confirm task has been run
    hxd.cds.rate_change.has_rarc_run = True
    hxd.cds.rate_change.has_rarc_not_run = False

def task_rarc_coverage(hxd, progress):
    """
    This rate change process uses the rate change library to perform calculations and stores the results for each bucket in the rate change Data Schema at the coverage_level.
    Steps for Each Bucket:
    - A temporary data schema (transient HXD) is created using the expiring data.
    - Only the inputs relevant to the bucket scope are aligned with the renewing policy.
    - The library applies the rating calculation to compute the rebased value.
    Notes:
    - Some temporary results are stored in the data schema for validation purposes.
    - For insured asset use, use the rate_change_insured_asset library version 2.x instead of version 1.x.
    """
    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Get Expiring Data with any data transformation from task_expiring_policy_fetch
    expiring_data = task_expiring_policy_fetch_coverage(hxd, progress)

    # Get expiring data but remove bloating from dynamic dropdown data
    expiring_data = {
        "cds": expiring_data["cds"],        
        "hx_core": expiring_data["hx_core"],       
    }

    # NOTE: Align legacy Data Schema to current Data Schema to proceed to the import without issues.
    # Add new node and assign their value
    # Reassign existing node if there was a change in definition
    # Delete Node that are not present in the current data schema

    # Get data Schema static copy path
    data_schema_static_filename = "data_schema/data_schema_static_copy.py"
    # data_schema_static_path = os.path.join(os.path.dirname(__file__), data_schema_static_filename) # v0.5.0 Use when this file location is within editing/algorithms
    current_dir = os.path.dirname(__file__)
    data_schema_static_path = os.path.join(os.path.dirname(current_dir), data_schema_static_filename)

    # Get the fx table
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
        kw_args = {
            "expiring_inputs_in_ccy": expiring_inputs_in_ccy_cvg, # list of tuples
            "fx_table": fx_rates_df 
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

        rc.calculate_repriced_values(
            expiring_data = expiring_data, # NOTE: this allows to use the expiry data with aligned Data Schema
            **kw_args
        )
        # Use the repriced values to calculate the changes for each bucket
        rc_result[f'{coverage}_rarc_df'], rc_result[f'{coverage}_rarc_list'] = rc.calculate_rarc_by_layer()
        
        # # remove the nan by none
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

            # Only populate bucket change for Renewing Layer. No calculation for New Layer.
            if hxd_layer.rate_change.renewing_layer==True:
                # populate bucket change for Renewing Layer. No calculation for New Layer.
                for key, value in rarc_layer.items():
                    setattr(getattr(hxd_layer.rate_change, coverage), key, value)
                # Calculate brokerage change for storage but not display
                expiring_brokerage = getattr(hxd_layer.rate_change, coverage).expiring_policy_info.expiring_brokerage or 0
                renewal_brokerage = getattr(getattr(hxd_layer, "coverages"), coverage).brokerage or 0
                brokerage_change = (1 - expiring_brokerage) / (1 - renewal_brokerage)
                getattr(hxd_layer.rate_change, coverage).brokerage_change.model_calculated = brokerage_change

            for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
                rc_vbl = getattr(getattr(hxd_layer.rate_change, coverage), item)
                # NOTE: ONLY for legacy model. Not necessary for a first build. 
                # Assignment in tasks instead of rating (rate_rate_change(hxd)) to clear out the overrides at the creation of the renewa
                # rc_vbl.uw_selected.calculated = rc_vbl.model_calculated # Edit v0.5.0 Legacy model only.

    # Confirm task has been run
    hxd.cds.rate_change.has_rarc_run = True
    hxd.cds.rate_change.has_rarc_not_run = False