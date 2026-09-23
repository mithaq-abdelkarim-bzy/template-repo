import hx
import math, os, json
import numpy as np
import pandas as pd

from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from libraries.rate_change.algorithms.rate_change import RateChange as RateChangeLib

from algorithms.rate_utilities import get_layer_idx_from_label, ratio
from algorithms.rate_rate_change import rate_change_buckets

def rarc(hxd, progress):
    
    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Make sure expiring data is up to date
    expiring_data = expiring_policy_fetch(hxd, progress)

    expiring_data = handle_legacy_model_versions(hxd, expiring_data)

    # Get correct buckets based on coverage
    buckets = rate_change_buckets()

    root_dir = os.path.dirname(os.path.abspath(__file__))
    data_schema_static_path = os.path.join(root_dir, 'data_schema', 'data_schema_static_copy.py')

    # Rate Change with offline_hxd
    rc = RateChangeLib(
        hxd=hxd,
        progress=progress,
        buckets=buckets,
        layers_path="cds/layers",
        expiring_actual_prem="quoted_premium_annualised",
        expiring_technical_prem="benchmark_premium_annualised_100",
        async_tasks=[],  # Pass the actual tasks, not strings
        data_schema_static_path=data_schema_static_path,
        expiring_currency="currency"
    )

    rc.calculate_repriced_values(
        expiring_data=expiring_data
        # expiring_policy_option_id=496991 # NOTE: for debugging if needed
    )

    # Use the repriced values to calculate the changes for each bucket
    rarc_df, rarc_list = rc.calculate_rarc_by_layer()

    # NOTE: for debugging if needed
    # pd.set_option('display.max_columns', None)
    # print(rarc_df)
    # print(rarc_list)

    # Calculate brokerage change for storage but not display
    for layer in hxd.cds.layers:
        expiring_brokerage = layer.rate_change.expiring_policy_info.expiring_brokerage or 0
        renewal_brokerage = layer.brokerage or 0
        layer.rate_change.brokerage_change.model_calculated = (1 - expiring_brokerage) / (1 - renewal_brokerage)

    # Push to hxd
    for rarc_layer, hxd_layer in zip(rarc_list, hxd.cds.layers):
        hxd_layer.rate_change.temp_storage = {k: None if isinstance(v, (int, float, np.number)) and np.isnan(v) else v for k, v in rarc_layer["temp_storage"].items()}  # Handle NaN to allow empty layers
        rarc_layer.pop("temp_storage")

        for key, value in rarc_layer.items():
            nan_handled_values = {k: None if isinstance(v, (int, float, np.number)) and math.isnan(v) else v for k, v in value.items()}
            setattr(hxd_layer.rate_change, key, nan_handled_values)

    # Confirm task has been run
    hxd.cds.rate_change.has_rarc_run = True
    hxd.cds.rate_change.has_rarc_not_run = False


def expiring_policy_fetch(hxd, progress):
    """
    Async task to import data from an expiring policy option for rate change calculation and analysis of movement.
    Developers will need to update the task in two places, first for which variables from the expiring policy to import,
    second to assign these to the current model variables.
    """
    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id = hxd.cds.rate_change.expiring_policy_option_id.selected #or 85244 # NOTE: use hardcoded ID for debugging if needed
    expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False)

    if expiring_response.status_code != 200:
        raise Exception(expiring_response.json())

    expiring_data = expiring_response.json()["data"]
    #for testing rate change without having to create a new policy
    # expiring_data = None
    # input_path = "/workspace/editing/algorithms/testing_jsons/expiring_policy.json"
    # with open(input_path, "r") as file:
    #     expiring_data = json.load(file)

    # Get fields from json response and push to hxd
    expiring_layers_len = len(expiring_data["cds"]["layers"])
    layer_mapping = {}
    
    # Create a set of expiring layers (adjusted to zero-based index)
    expiring_layers = set()
    for layer in hxd.cds.layers:
        expiring_layers.add(get_layer_idx_from_label(layer.rate_change.expiring_layer_label))

    # Initialize the mapping and the new filtered list
    index_mapping = {}
    new_layers = []
    new_layers_set = set()

    # Iterate through the original list and keep only the expiring layers
    for original_index, layer in enumerate(expiring_data["cds"]["layers"]):
        if (original_index in expiring_layers) and (original_index not in new_layers_set):
            # Add the layer to the new list
            new_layers.append(layer)
            # Map the original index to the new index
            index_mapping[original_index] = len(new_layers)
            new_layers_set.add(original_index)

    while (len(new_layers) > 0) and (len(new_layers) < len(hxd.cds.layers)):
        new_row = new_layers[0]
        new_row = set_values_to_none(new_row)
        # Append the new row to new_layers
        new_layers.append(new_row)

    expiring_data["cds"]["layers"] = new_layers

    for idx, layer in enumerate(hxd.cds.layers):
        # Throw error if expiring layer doesn't exist
        expiring_layer_id = get_layer_idx_from_label(layer.rate_change.expiring_layer_label)
        if (expiring_layer_id + 1) > expiring_layers_len:
            hx.errors.fatal(f"Expiring Layer {layer.rate_change.expiring_layer}, mapped to Renewal Layer {idx+1}, does not exist. Number of expiring layers is {expiring_layers_len}.")

        layer.rate_change.expiring_layer = index_mapping[expiring_layer_id]
        mapped_expiring_layer_idx = layer.rate_change.expiring_layer - 1
        layer.rate_change.premium.line_100pct.annualised.expiring = expiring_premium = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["quoted_premium_annualised"]

        # Inputs only model doesn't have layer.written_line populated
        #expiring_written_line = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["written_line"] or 0
        # so we calculate it:
        afb_net_premium = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["afb_net_premium"] or 0
        net_premium = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["net_premium"] or 0
        expiring_written_line = ratio(afb_net_premium, net_premium)
        
        layer.rate_change.premium.beazley_line.annualised.expiring = (expiring_premium or 0) * expiring_written_line
        layer.rate_change.expiring_policy_info.expiring_brokerage = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["brokerage"] or 0
        # NOTE add other expiring fields as required here

        # Save layer mapping
        layer_mapping[str(idx+1)] = layer.rate_change.expiring_layer
    
    hxd.cds.rate_change.layer_mapping = json.dumps(layer_mapping)

    # Confirm task has been run
    hxd.cds.rate_change.has_fetch_run = True
    hxd.cds.rate_change.has_fetch_not_run = False

    return expiring_data


def handle_legacy_model_versions(hxd, expiring_data):
    # Old model versions don't have tower excesses as overrides, which causes data schema incompatibilities
    for layer in expiring_data["cds"]["layers"]:
        towers = [key for key in layer if "tower" in key]
        for tower in towers:
            if not isinstance(layer[tower]["excess"], dict):
                layer[tower]["excess"] = {
                    "calculated": layer[tower]["excess"],
                }

    return expiring_data  # This gets modified in place, but make explicit


# Recursive function to set all values to None
def set_values_to_none(data):
    if isinstance(data, dict):
        return {key: set_values_to_none(value) for key, value in data.items()}
    else:
        return None