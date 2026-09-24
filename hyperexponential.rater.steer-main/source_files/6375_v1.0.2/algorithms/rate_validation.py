# v0.5.0
import hx
import pandas as pd
import numpy as np
import math
import ast
import hashlib
import json
from algorithms.model_profiler.profiling_hxd_functions import time_me

from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, write_pd_to_hxd_no_overrides, pd_df_from_hx_list_columns_task, get_nested_attr

import algorithms.rate_constants as const 

@time_me
def missing_attribute_list(hxd, attribute: str):
    """
    Check if a specified compulsory field (e.g., 'rate' or 'epi_100') is missing or zero for each layer.

    Args:
        hxd: The input object containing layers.
        attribute (str): The attribute to check (e.g., "rate" or "epi_100").

    Returns:
        list: A list of layer suffixes (e.g., ["01", "02"]) where the attribute is missing or zero.
    """
    layers = hxd.cds.layers
    missing_list = []

    for index, layer in enumerate(layers):
        suffix = f"{index + 1:02d}"
        if layer.limit > 1:
            # Dynamically check the attribute (e.g., layer.rate or layer.epi_100)
            attr_value = getattr(layer, attribute, None)
            if attr_value == 0 or attr_value is None:
                missing_list.append(suffix)

    return missing_list
            
@time_me
def rate_validations(hxd):
    er = hxd.cds.steer.experience_rating
    ol = hxd.cds.steer.experience_rating.on_levelling
    cds = hxd.cds
    ms = hxd.model_state
    cds_hc = hxd.cds.healthcare_cat

    include_aad = cds.risk_information.include_aad
    include_loss_corridor = cds.risk_information.include_loss_corridor
    include_swing_rates = cds.risk_information.include_swing_rates
    include_profit_commission = cds.risk_information.include_profit_commission

    cy_yoa = hxd.cds.risk_information.inception_year

    
    # Insured name must be completed, this is needed to ensure landing page works correctly
    if not hxd.cds.standard_fields.insured_name:
        hx.errors.validation("Risk information - Insured name field must be completed.")
    
    if not hxd.cds.standard_fields.underwriter:
        hx.errors.validation("Risk information - Underwriter name must be entered")

    if hxd.cds.standard_fields.policy_reference is None or (hxd.cds.standard_fields.policy_reference is not None and len(hxd.cds.standard_fields.policy_reference) != 12):
        hx.errors.validation("Risk information - Policy reference must exist and contain 12 characters: letters and numbers")
        
    if include_swing_rates == True and include_profit_commission == True:
        hx.errors.validation("Risk Information - Must only select one of Swing Rates and Profit Commission")

    missing_limit_list = missing_attribute_list(hxd,"limit")
    if missing_limit_list:
        hx.errors.validation(f"Pricing Assumptions - Limit must be provided and be a value > 0 for layer {', '.join(map(str,missing_limit_list))}.")
    
    missing_epi_list = missing_attribute_list(hxd,"epi_100")
    if missing_epi_list:
        hx.errors.validation(f"Pricing Assumptions - EPI must be provided and be a value > 0 for layer {', '.join(map(str,missing_epi_list))}.")

    missing_rate_list = missing_attribute_list(hxd,"rate")
    if missing_rate_list:
        hx.errors.validation(f"Pricing Assumptions - Rate must be provided and be a value > 0 for layer {', '.join(map(str,missing_rate_list))}.")
    
    missing_rate_list = missing_attribute_list(hxd,"bkg_gross_or_net")
    if missing_rate_list:
        hx.errors.validation(f"Pricing Assumptions - Bkg Gross Or Net must be provided for layer {', '.join(map(str,missing_rate_list))}.")
     
    missing_rate_list = missing_attribute_list(hxd,"brokerage")
    if missing_rate_list:
        hx.errors.validation(f"Pricing Assumptions - Brokerage must be provided and be a value > 0 for layer {', '.join(map(str,missing_rate_list))}.")
     

    if ms.is_steer and hxd.cds.standard_fields.is_rater_priced:
    # Validation for Steer Experience Rating exposure input
        missing_expo_layer_list = []
        if ms.is_steer_experience_rating:

            expo_assump_df = pd_df_from_hx_list(ol.exposure_assumptions)
            sum_expo = expo_assump_df["exposure"].fillna(0).sum()
            if sum_expo == 0:
                hx.errors.validation("On-Levelling - Column exposure can't be empty")
            
            # no need the below since the FGU is the default value
            # for index, layer in enumerate(hxd.cds.layers) :
            #     suffix = f"{index+1:02d}"
            #     if layer.limit>1:
            #         if expo_assump_df[f"exposure_adjusted_layer_{suffix}"].fillna(0).sum() == 0:
            #             missing_expo_layer_list.append(suffix)
                
        if missing_expo_layer_list:
            hx.errors.validation(f"On-Levelling - Column Adjusted Exposure can't be empty for layer {', '.join(map(str,missing_expo_layer_list))}.")

        # # check that inputs are the same since Format Data has been run
        # if ms.has_run_steer_format_data:
        #     # get the task inputs list
        #     task_data_dict, task_layer_data_list, task_raw_data_list, task_expo_assumptions_list = get_inputs_steer_format_data_task(hxd)
        #     # compare the inputs list to the one used when the task has been run
        #     are_inputs_same = (
        #       ms.data_used_in_steer_format_data_task == str(task_data_dict)) 
        #       and (ms.layer_data_used_in_steer_format_data_task == str(task_layer_data_list)) 
        #       and (ms.raw_data_used_in_steer_format_data_task == str(task_raw_data_list)) 
        #       and (ms.expo_assumptions_data_used_in_steer_format_data_task == str(task_expo_assumptions_list))

        #     if not are_inputs_same:
        #         hx.errors.validation("Data Format - Inputs have changed. Data Format must be recalculated")

        # check that inputs are the same since Format Data has been run
        if ms.has_run_steer_format_data:
            # get fingerprints of the task inputs
            task_data_hash, task_layer_data_hash, task_raw_data_hash, task_expo_assumptions_hash = get_inputs_steer_format_data_task(hxd)
 
            # compare the current input fingerprints to the ones stored when the task was run
            are_inputs_same = (
                ms.data_used_in_steer_format_data_task == task_data_hash
                and ms.layer_data_used_in_steer_format_data_task == task_layer_data_hash
                and ms.raw_data_used_in_steer_format_data_task == task_raw_data_hash
                and ms.expo_assumptions_data_used_in_steer_format_data_task == task_expo_assumptions_hash
            )
 
            if not are_inputs_same:
                hx.errors.validation("Data Format - Inputs have changed. Data Format must be recalculated")


        if (er.is_not_experience_selected_updated):
            hx.errors.validation("Burning Cost - Burning Cost Pattern must be updated")

    if ms.is_healthcare_cat and hxd.cds.standard_fields.is_rater_priced:
        if cds_hc.trial_history.uw_view.from_year < cy_yoa - const.hc_max_trial_history_years + 1:

            hx.errors.validation(f"Trial History - From Year must be between {cy_yoa - const.hc_max_trial_history_years + 1:0.0f} and {cy_yoa:0.0f}")

        if cds_hc.trial_history.uw_view.to_year > cy_yoa:
            hx.errors.validation(f"Trial History - To Year must be between {cy_yoa - const.hc_max_trial_history_years + 1:0.0f} and {cy_yoa:0.0f}")

        if cds_hc.trial_history.total.taken_to_trial == 0 :
            hx.errors.validation(f"Trial History - Taken To Trials per year must be provided")
        
        trial_df = pd_df_from_hx_list(cds_hc.trial_history.trial)
        # Identify rows where taken_to_trial != wins + losses + mistrials
        error_rows = trial_df[trial_df["taken_to_trial"] != trial_df["wins"] + trial_df["losses"] + trial_df["mistrials"]]

        # If there are any error rows, log the error and display the 'display_yoa' column
        if not error_rows.empty:
            hx.errors.validation(
                f"Trial History - Taken To Trials per year must be equal to the sum of wins, losses, and mistrials per year. "
                f"Error in rows: {error_rows['display_yoa'].tolist()}"
            )

        exposure_spit_by_state_df = pd_df_from_hx_list(cds_hc.exposure_territory.exposure_spit_by_state)
        if exposure_spit_by_state_df["split"].sum() == 0:
            hx.errors.validation("Exposure Territory - Exposure per State must be provided")

    if hxd.cds.standard_fields.is_rater_priced:
        # Pricing Selection
        total_overweight_list = []

        for index, layer in enumerate(cds.layers):
            suffix = f"{index + 1:02d}"
            if layer.limit > 1 and layer.pricing_selection.final_selection.total_weighting  != 1:
                total_overweight_list.append(suffix)

        if total_overweight_list:
            hx.errors.validation(f"Pricing Selection - Total Weight must be 100% for layers {', '.join(map(str,total_overweight_list))}.")

        zero_pure_rate_list = []

        for index, layer in enumerate(cds.layers):
            suffix = f"{index + 1:02d}"
            if layer.limit > 1 and layer.pure_rate ==0:
                zero_pure_rate_list.append(suffix)

        if zero_pure_rate_list:
                hx.errors.validation(f"Pricing Selection - Final Selection Pure rate can't be 0 for layers {', '.join(map(str,zero_pure_rate_list))}.")


        method_list = [
            "risk_profile_bdx",
            "burning_cost",
            "limit_average_severity",
            "clash",
            "healthcare_cat",
            "other_method",
        ]

        methods_to_remove = set()

        if ms.is_steer:
            methods_to_remove = {
                "clash",
                "healthcare_cat",
            }

        elif ms.is_clash:
            methods_to_remove = {
                "risk_profile_bdx",
                "limit_average_severity",
                "burning_cost",
                "healthcare_cat",
            }

        elif ms.is_healthcare_cat:
            methods_to_remove = {
                "risk_profile_bdx",
                "limit_average_severity",
                "burning_cost",
                "clash",
            }

        method_list = [
            method
            for method in method_list
            if method not in methods_to_remove
        ]

        # out_of_range_weight_list = []

        # for method in method_list:
        #     for index, layer in enumerate(cds.layers):
        #         suffix = f"{index + 1:02d}"
            
        #         if layer.limit > 1 and (getattr(layer.pricing_selection.method).weighting <0 or getattr(layer.pricing_selection.method).weighting > 1): 
        #             out_of_range_weight_list.append(f"suffix")

        #     if out_of_range_weight_list:
        #         method_display = method.replace("_"," ").capitalize
        #         hx.errors.validation(f"Pricing Selection - {method_display} Weighting has to be between 0 and 100% for layers {', '.join(map(str,out_of_range_weight_list))}.")

        for method in method_list:
            out_of_range_weight_list = []

            for index, layer in enumerate(cds.layers):
                suffix = f"{index + 1:02d}"

                if layer.limit > 1:
                    weighting = getattr(
                        getattr(layer.pricing_selection, method),
                        "weighting",
                        0,
                    ) or 0

                    if not 0 <= weighting <= 1:
                        out_of_range_weight_list.append(suffix)

            if out_of_range_weight_list:
                method_display = method.replace("_", " ").capitalize()

                hx.errors.validation(
                    f"Pricing Selection - {method_display} weighting has to be "
                    f"between 0 and 100% for layers "
                    f"{', '.join(out_of_range_weight_list)}."
                )



        # is_profit_commission = any((layer.profit_commission_rate or 0 ) > 0 for layer in cds.layers)

        # Check Advanced Features button has been used
        # is_advanced_features = include_aad or include_loss_corridor or include_swing_rates or is_profit_commission
        is_advanced_features = include_aad or include_loss_corridor or include_swing_rates or include_profit_commission
        if is_advanced_features:
            if ms.has_run_advanced_features != True:
                hx.errors.validation("Advanced Features - Advanced Features must be calculated")
            else:
                # build data_dict, inputs at a policy level, used in advanced features
                alpha = cds.pricing_selection.pareto_parameters.selected
                odf_parameter = cds.pricing_selection.odf_parameters.selected
                sliding_scale_ind = cds.risk_information.include_swing_rates
                loss_corridor_ind = cds.risk_information.include_loss_corridor
                aad_ind = cds.risk_information.include_aad
                
                data_dict = {}
                data_dict["alpha"] = alpha
                data_dict["odf_parameter"] = odf_parameter
                data_dict["sliding_scale_ind"] = sliding_scale_ind
                data_dict["loss_corridor_ind"] = loss_corridor_ind
                data_dict["aad_ind"] = aad_ind 

                # build layer_data_list, inputs at a layer level, used in advanced features

                async_input_nodes = [
                    "epi_100",
                    "excess",
                    "limit",
                    "upfront_premium_gross_100",
                    "pricing_selection/final_selection/pure_premium",
                    "brokerage",
                    "ceding_commission",
                    "brokerage_inc_swing",
                    "advanced_features_input/aad",
                    "ncb",
                    "profit_commission_rate",
                    "expense_allowance",
                    "loss_corridor/insured_participation",
                    "loss_corridor/max_rate",
                    "loss_corridor/min_rate",
                    "loss_cap_used",
                    "cap_gross_pct",
                    "no_reinstatement",
                    'reinstatement_pct_1', 
                    'reinstatement_pct_2', 
                    'reinstatement_pct_3', 
                    'reinstatement_pct_4', 
                    'reinstatement_pct_5',
                    'reinstatement_pct_6', 
                    'reinstatement_pct_7', 
                    'reinstatement_pct_8', 
                    'reinstatement_pct_9', 
                    'reinstatement_pct_10',
                    "number_of_rips",


                    "swing_rates/deposit_rate",
                    "swing_rates/min_rate",
                    "swing_rates/max_rate",
                    "swing_rates/margin",
                    "swing_rates/loading_factor",
                    "expected_loss" # this is 100 before AD
                ]

                layers_df = pd_df_from_hx_list_columns_task(hxd.cds.layers, async_input_nodes)
                layers_df["unlimited_rips"] = layers_df["no_reinstatement"]=="Unlimited"
                layers_df["num_rips"] = np.where(layers_df['unlimited_rips'], 999, layers_df['number_of_rips'])
                layers_df["brokerage_ad"] = layers_df["brokerage_inc_swing"] + layers_df["ceding_commission"]

                layers_df = layers_df[async_input_nodes]
                layer_data_list = layers_df.to_dict(orient='records')
                layer_data_list = str(layer_data_list).replace('nan','None')

                task_layer_data_list = ms.layer_data_used_in_advanced_features_task.replace('nan','None')
                task_layer_data_list = ast.literal_eval(task_layer_data_list)

                if not(str(layer_data_list) == str(task_layer_data_list) and str(data_dict) == ms.data_used_in_advanced_features_task):
                    hx.errors.validation("Advanced Features - Advanced Features must be recalculated")

        
    # Validation to check how many layers are set as bound, also updates premium label for bound policies
    bound_count = 0
    for layer in hxd.cds.layers:
        # assign labels
        if layer.status in ["Bound", "Post Bind Complete"]:
            bound_count += 1
            layer.premium_label = "Gross Bound Premium"
        else:
            layer.premium_label = "Gross Quoted Premium"
        # Written Premium validations
        if layer.written_line ==0 and layer.status in ["Bound", "Post Bind Complete","Quoted"]:
            hx.errors.validation("Rating Summary - Written Line can't be 0 for When status for Bound or Quoted layers")
        
        

    
    if bound_count == 0:
        hx.errors.validation("Rating Summary - Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final")
    # elif bound_count > 1:
    #     hx.errors.validation("Rating Summary - There must be only one bound policy")
    
    if hxd.cds.standard_fields.is_case_priced:
        if any(layer.bpi_case_priced == 0 and layer.include_layer for layer in hxd.cds.layers):
            hx.errors.validation("Rating Summary - Enter BPI Case Priced for all included layers.")
        
def input_paths_steer_format_raw_data_task():

    
    input_paths = [
        "hx_core/inception_date",
        "cds/currencies/source_currency",
        "cds/steer/experience_rating/misc_parameters/closed_indicator",
        "cds/steer/experience_rating/data_mapping/field_01/specify_column",
        "cds/steer/experience_rating/data_mapping/field_02/specify_column",
        "cds/steer/experience_rating/data_mapping/field_03/specify_column",
        "cds/steer/experience_rating/data_mapping/field_04/specify_column",
        "cds/steer/experience_rating/data_mapping/field_05/specify_column",
        "cds/steer/experience_rating/data_mapping/field_06/specify_column",
        "cds/steer/experience_rating/data_mapping/field_07/specify_column",
        "cds/steer/experience_rating/data_mapping/field_08/specify_column",
        "cds/steer/experience_rating/data_mapping/field_09/specify_column",
        "cds/steer/experience_rating/data_mapping/field_10/specify_column",
        "cds/steer/experience_rating/data_mapping/field_11/specify_column",
        "cds/steer/experience_rating/data_mapping/field_12/specify_column",
        "cds/steer/experience_rating/data_mapping/field_13/specify_column",
        "cds/steer/experience_rating/data_mapping/field_14/specify_column",
        "cds/steer/experience_rating/data_mapping/field_15/specify_column",
        "cds/steer/experience_rating/data_mapping/field_16/specify_column",
        "cds/steer/experience_rating/data_mapping/field_17/specify_column",
        "cds/steer/experience_rating/data_mapping/field_18/specify_column",
        "cds/steer/experience_rating/other_fields/fvy/value",
        "cds/steer/experience_rating/other_fields/coverage_basis/value",
        "cds/steer/experience_rating/other_fields/data_as_at_date/value",
    ]

    layer_input_paths = [
        "limit",
        "excess",
    ]
    
    expo_assumptions_input_paths = [
        # "cds/steer/experience_rating/on_levelling/exposure_assumptions",
        "exposure",
        "annual_rate_change",
        "claims_inflation",
        "exposure_adjusted_layer_01",
        "exposure_adjusted_layer_02",
        "exposure_adjusted_layer_03",
        "exposure_adjusted_layer_04",
        "exposure_adjusted_layer_05",
    ]

    raw_input_paths = [f"column_{index:02d}" for index in range(1,const.raw_data_max_column +1)]

    return input_paths, layer_input_paths, expo_assumptions_input_paths, raw_input_paths

# def get_inputs_steer_format_data_task(hxd):
#     # Get list of input
#     input_paths, layer_input_paths, expo_assumptions_input_paths, raw_input_paths = input_paths_steer_format_raw_data_task()
    
#     # cds and other level not nested in a list
#     task_data_dict = {}
#     for path in input_paths:
#         task_data_dict[path] = str(get_nested_attr(hxd,path.split("/")))
#     # layer list children
#     layers_df = pd_df_from_hx_list_columns_task(hxd.cds.layers, layer_input_paths)
#     task_layer_data_list = layers_df.to_dict(orient='records')
#     # raw_data list children
#     raw_data_df = pd_df_from_hx_list_columns_task(hxd.cds.steer.experience_rating.raw_data, raw_input_paths )
#     task_raw_data_list = raw_data_df.to_dict(orient='records')
#     # exposure assumption list children
#     expo_assumptions_df = pd_df_from_hx_list_columns_task(hxd.cds.steer.experience_rating.on_levelling.exposure_assumptions, expo_assumptions_input_paths )
#     task_expo_assumptions_list = expo_assumptions_df.to_dict(orient='records')  
#     return task_data_dict, task_layer_data_list, task_raw_data_list, task_expo_assumptions_list

def _normalise_for_hash(value):
    """
    Convert values into a stable JSON-serialisable form for fingerprinting.
    This keeps comparisons consistent across rating/task runs, including pandas,
    numpy, dates and hx override-like objects.
    """
    if hasattr(value, "selected") and hasattr(value, "is_overridden"):
        return _normalise_for_hash(value.selected)
 
    if isinstance(value, dict):
        return {
            str(k): _normalise_for_hash(v)
            for k, v in value.items()
        }
 
    if isinstance(value, list):
        return [_normalise_for_hash(v) for v in value]
 
    if isinstance(value, tuple):
        return [_normalise_for_hash(v) for v in value]
 
    if pd.isna(value) if not isinstance(value, (list, tuple, dict, str)) else False:
        return None
 
    if isinstance(value, np.generic):
        return value.item()
 
    return str(value)
 
 
def _stable_hash(value):
    """
    Create a deterministic SHA-256 fingerprint for a Python object.
    """
    normalised_value = _normalise_for_hash(value)
    payload = json.dumps(normalised_value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
 
 
def _hash_hx_list_columns(hx_list, input_paths):
    """
    Hash selected columns from an hx.List directly.
    This avoids building a large pandas DataFrame, converting it to records,
    and then stringifying the entire raw data object inside the rating algorithm.
    """
    hasher = hashlib.sha256()
 
    for row in hx_list:
        row_dict = {}
 
        for path in input_paths:
            value = get_nested_attr(row, path.split("/"))
            row_dict[path] = _normalise_for_hash(value)
 
        payload = json.dumps(row_dict, sort_keys=True, separators=(",", ":"), default=str)
        hasher.update(payload.encode("utf-8"))
        hasher.update(b"\n")
 
    return hasher.hexdigest()
 
 
def get_inputs_steer_format_data_task(hxd):
    # Get list of inputs
    input_paths, layer_input_paths, expo_assumptions_input_paths, raw_input_paths = input_paths_steer_format_raw_data_task()
    
    # cds and other level not nested in a list
    task_data_dict = {}
    for path in input_paths:
        task_data_dict[path] = str(get_nested_attr(hxd, path.split("/")))
 
    # layer list children
    layers_df = pd_df_from_hx_list_columns_task(hxd.cds.layers, layer_input_paths)
    task_layer_data_list = layers_df.to_dict(orient="records")
 
    # raw_data list children
    # Hash directly from hxd to avoid creating/stringifying a large list of dictionaries.
    task_raw_data_hash = _hash_hx_list_columns(
        hxd.cds.steer.experience_rating.raw_data,
        raw_input_paths,
    )
 
    # exposure assumption list children
    expo_assumptions_df = pd_df_from_hx_list_columns_task(
        hxd.cds.steer.experience_rating.on_levelling.exposure_assumptions,
        expo_assumptions_input_paths,
    )
    task_expo_assumptions_list = expo_assumptions_df.to_dict(orient="records")
 
    return (
        _stable_hash(task_data_dict),
        _stable_hash(task_layer_data_list),
        task_raw_data_hash,
        _stable_hash(task_expo_assumptions_list),
    )