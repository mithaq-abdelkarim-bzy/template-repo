import hx
import os
import pandas as pd

from libraries.rate_change.algorithms.rate_change import RateChange as RateChangeLib

from algorithms.rate_change.task_rarc_expiry_policy_fetch import task_expiring_policy_fetch
from algorithms.rate_rate_change import RATE_CHANGE_BUCKETS, EXP_INPUTS_IN_CCY
from algorithms import parameter_tables_schema as params
from algorithms.rate_change.simulation_reprice import (
    recalculate_exposure_rates_for_rate_change,
    reset_rarc_simulation_validation_state,
)


def task_rarc_layer_with_simulation(hxd, progress):
    """
    Layer-level RARC using the rate change library with transient exposure-rate
    simulation repricing enabled for each bucket.
    """
    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    reset_rarc_simulation_validation_state()

    # Get Expiring Data with any data transformation from task_expiring_policy_fetch
    expiring_data = task_expiring_policy_fetch(hxd, progress)

    # Get expiring data but remove bloating from dynamic dropdown data
    expiring_data = {
        "cds": expiring_data["cds"],
        "hx_core": expiring_data["hx_core"],
    }

    # Get data Schema static copy path
    data_schema_static_filename = "data_schema/data_schema_static_copy.py"
    current_dir = os.path.dirname(__file__)
    data_schema_static_path = os.path.join(os.path.dirname(current_dir), data_schema_static_filename)

    # Get the fx table
    fx_rates_df = params.fx_rates.df()

    # Get buckets
    buckets = RATE_CHANGE_BUCKETS

    # Get the expiring_inputs_in_ccy information to revalue in case of change in currency at renewal
    expiring_inputs_in_ccy = EXP_INPUTS_IN_CCY["layers"]

    # Prepare arguments for calculate_repriced_values() function
    kw_args = {
        "expiring_inputs_in_ccy": expiring_inputs_in_ccy,
        "fx_table": fx_rates_df,
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
        async_tasks=[recalculate_exposure_rates_for_rate_change],
        data_schema_static_path=data_schema_static_path,
    )

    rc.calculate_repriced_values(
        expiring_data=expiring_data,
        **kw_args,
    )

    # Use the repriced values to calculate the changes for each bucket
    rarc_df, rarc_list = rc.calculate_rarc_by_layer()

    # remove the nan by none
    rarc_df = rarc_df.where(pd.notnull(rarc_df), None)

    # Push to hxd
    for rarc_layer, hxd_layer in zip(rarc_list, hxd.cds.layers):
        # Store data in the temp_storage structure, this includes, quoted_premium_100, benchmark_100 and currency
        hxd_layer.rate_change.temp_storage = rarc_layer["temp_storage"]
        rarc_layer.pop("temp_storage")

        # Only populate bucket change for Renewing Layer. No calculation for New Layer.
        if hxd_layer.rate_change.renewing_layer == True:
            # populate bucket change for Renewing Layer. No data stored for new layer.
            for key, value in rarc_layer.items():
                setattr(hxd_layer.rate_change, key, value)

            # Calculate brokerage change for storage but not display
            expiring_brokerage = hxd_layer.rate_change.expiring_policy_info.expiring_brokerage or 0
            renewal_brokerage = hxd_layer.brokerage or 0
            hxd_layer.rate_change.brokerage_change.model_calculated = (1 - expiring_brokerage) / (1 - renewal_brokerage)

            for item in [
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
            ]:
                rc_vbl = getattr(hxd_layer.rate_change, item)
                # NOTE: ONLY for legacy model. Not necessary for a first build.
                # Assignment in tasks instead of rating (rate_rate_change(hxd)) to clear out the overrides at the creation of the renewal
                # rc_vbl.uw_selected.calculated = rc_vbl.model_calculated

    # Confirm task has been run
    hxd.cds.rate_change.has_rarc_run = True
    hxd.cds.rate_change.has_rarc_not_run = False
