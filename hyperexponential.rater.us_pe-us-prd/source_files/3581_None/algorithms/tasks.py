import hx
import os
import pandas as pd
import json
from algorithms.rate_rate_change import rate_change_buckets
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from libraries.rate_change.algorithms.rate_change import RateChange as RateChangeLib


# Update example task below
@hx.task
def example_empty_task(hxd, progress):
    pass


# Importing expiring policy for rate change
"""
Async task to import data from an expiring policy option for rate change calculation and analysis of movement.
Developers will need to update the task in two places, first for which variables from the expiring policy to import,
second to assign these to the current model variables.
"""


@hx.task
def generate_email(hxd, progress):
    # Not sure exactly what to do here yet
    raise ValueError("Hi, generate email is not implemented yet")


@hx.task
def bind_option(hxd, progress):
    # Not sure exactly what to do here yet
    raise ValueError("Hi, bind_option is not implemented yet")


# Importing expiring policy for rate change
"""
Async task to import data from an expiring policy option for rate change calculation and analysis of movement.
Developers will need to update the task in two places, first for which variables from the expiring policy to import,
second to assign these to the current model variables.
"""


@hx.task
def expiring_policy_fetch_task(hxd, progress):

    expiring_policy_option_id = None
    if hxd.cds.rate_change.expiring_policy_option_id.selected:
        expiring_policy_option_id = (
            hxd.cds.rate_change.expiring_policy_option_id.selected
        )
    elif hxd.cds.rate_change.expiring_policy_option_id.calculated:
        expiring_policy_option_id = (
            hxd.cds.rate_change.expiring_policy_option_id.calculated
        )

    if not expiring_policy_option_id:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id = expiring_policy_option_id  # or 85244 # NOTE: use hardcoded ID for debugging if needed
    expiring_response = hx_renew.snapshots.get_snapshot(
        policy_option_id=expiring_policy_option_id, stream=False
    )

    if expiring_response.status_code != 200:
        raise Exception(expiring_response.json())

    expiring_data = expiring_response.json()["data"]

    # Get fields from json response and push to hxd
    expiring_layers_len = len(expiring_data["cds"]["layers"])
    layer_mapping = {}

    for idx, layer in enumerate(hxd.cds.layers):
        # Throw error if expiring layer doesn't exist
        if layer.rate_change.expiring_layer > expiring_layers_len:
            hx.errors.fatal(
                f"Expiring Layer {layer.rate_change.expiring_layer}, mapped to Renewal Layer {idx+1}, does not exist. Number of expiring layers is {expiring_layers_len}."
            )

        mapped_expiring_layer_idx = layer.rate_change.expiring_layer - 1
        layer.rate_change.premium_annualized_100pct.expiring = expiring_data["cds"][
            "layers"
        ][mapped_expiring_layer_idx]["quoted_premium"]
        expiring_written_line = expiring_data["cds"]["layers"][
            mapped_expiring_layer_idx
        ]["written_line"]
        layer.rate_change.premium_annualized_beazley_share.expiring = (
            layer.rate_change.premium_annualized_100pct.expiring
            * (expiring_written_line or 0)
        )
        # NOTE: ... Add expiring fields as required here

        # Save layer mapping
        layer_mapping[str(idx + 1)] = layer.rate_change.expiring_layer

    hxd.cds.rate_change.layer_mapping = json.dumps(layer_mapping)

    # Confirm task has been run
    hxd.cds.rate_change.has_fetch_run = True
    hxd.cds.rate_change.has_fetch_not_run = False


@hx.task
def rarc_task(hxd, progress):

    # Make sure expiring data is up to date
    expiring_policy_fetch_task(hxd, progress)

    # Get correct buckets based on coverage
    buckets = rate_change_buckets(hxd)

    data_schema_static_filename = "data_schema/data_schema_static.py"
    data_schema_static_path = os.path.join(
        os.path.dirname(__file__), data_schema_static_filename
    )

    # Rate Change with offline_hxd
    rc = RateChangeLib(
        hxd=hxd,
        progress=progress,
        buckets=buckets,
        layers_path="cds/layers",
        expiring_actual_prem="quoted_premium",
        expiring_technical_prem="benchmark_premium",
        async_tasks=[],  # Pass the actual tasks, not strings
        data_schema_static_path=data_schema_static_path,
    )

    rc.calculate_repriced_values(
        # expiring_policy_option_id=139529, #policy_option_id=139529 # NOTE: for debugging if needed
    )

    # Use the repriced values to calculate the changes for each bucket
    rarc_df, rarc_list = rc.calculate_rarc_by_layer()

    # NOTE: for debugging if needed
    # pd.set_option('display.max_columns', None)
    # print(rarc_df)
    # print(rarc_list)

    # Push to hxd
    for rarc_layer, hxd_layer in zip(rarc_list, hxd.cds.layers):
        hxd_layer.rate_change.temp_storage = rarc_layer["temp_storage"]
        rarc_layer.pop("temp_storage")

        for key, value in rarc_layer.items():
            setattr(hxd_layer.rate_change, key, value)

    # Confirm task has been run
    hxd.cds.rate_change.has_rarc_run = True
    hxd.cds.rate_change.has_rarc_not_run = False


@hx.task
def start_renewal_task(hxd, progress):

    # The following statement checks that the expiring information has been imported for renewals. Some teams might want to start
    # from a blank rater each time, in which case update the below
    if not hxd.cds.standard_fields.insured_name:
        hxd.model_state.landing_page_info = "❗❗ FAILED: Click 'Undo' then 'Import Expiring Policy Data' in the top right corner ❗❗"
    else:
        hxd.model_state.pressed_start_renewal_task = True

        # Add tasks which must be done before starting a policy here >>

        # expiring_policy_fetch_task(hxd, progress)
