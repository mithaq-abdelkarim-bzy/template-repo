# v0.5.0
import hx
import algorithms.rate_utilities as utils
from algorithms.rate_risk_information import rate_risk_information
from algorithms.rate_claims import rate_claims_tailored
from algorithms.rate_exposure_details import rate_exposure_details
from algorithms.rate_territory import rate_territory
from algorithms.rate_pricing import rate_pricing
from algorithms.rate_experience_rating_2 import rate_experience_rating_2
from algorithms.rate_rate_change import (
    rate_rate_change,
    rate_rate_change_coverages,
    rate_rate_change_coverages,
    save_insured_asset_list_for_rate_change,
)
from algorithms.rate_rating_summary import rate_rating_summary
from algorithms.rate_validation import rate_validations
from algorithms.rate_client_details import rate_client_details
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from algorithms.model_state import model_state, allow_policy_doc_download
from algorithms.policy_document import create_dict_for_excel, store_policy_data
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
from libraries.email_notification.algorithms.bug_report import provision_bug_report_inputs_outputs
from algorithms.rate_simulation_inputs import get_current_simulation_snapshot_json

# move this somewhere else
def _validate_simulation_inputs_are_current(hxd):
    simulation_state = getattr(hxd.model_state, "simulation_state", None)
    if simulation_state is None:
        return
    stored_snapshot = simulation_state.last_input_snapshot
    if not stored_snapshot:
        return
    try:
        current_snapshot = get_current_simulation_snapshot_json(hxd)
    except Exception:
        return
    if current_snapshot != stored_snapshot:
        error_msg = (
        "**!!  Please rerun the simulation  !!**\n"
        "Simulation inputs have changed since the last run."
        )
        hx.errors.validation("Simulation inputs have changed since the last run. Please rerun the simulation.")
        hxd.cds.run_simulation_notes = error_msg
        hxd.cds.run_simulation_notes_bool = True
    else:
        hxd.cds.run_simulation_notes = ""
        hxd.cds.run_simulation_notes_bool = False

@hx.rating
def rating_algorithm(hxd):
    model_state(hxd)
    rate_validations(hxd)
    rate_risk_information(hxd)
    rate_exposure_details(hxd)
    rate_territory(hxd)
    rate_client_details(hxd)
    rate_rating_summary(hxd)
    rate_claims_tailored(hxd)
    rate_experience_rating_2(hxd)
    rate_pricing(hxd)
    _validate_simulation_inputs_are_current(hxd)
    # rate_experience_rating(hxd)
    if hxd.cds.standard_fields.is_renewal:
        if RARC_INSURED_ASSET_USE:
            save_insured_asset_list_for_rate_change(hxd)  # save the renewing insured asset list in the Data Schema
        if not RARC_COVERAGE_USE:
            rate_rate_change(hxd)  # NOTE: calculation at a layer level. Can be removed if not used
        else:
            rate_rate_change_coverages(hxd)  # NOTE: calculation at a coverage level. Can be removed if not used

    sync_hx_core(hxd)  # NOTE:Do not remove for either main or inputs only model

    # Policy doc (only run if it's the live rating algo, the transient hxd causes error)
    # if "transient_hxd" not in str(type(hxd)):
    #     store_policy_data(hxd)
    #     allow_policy_doc_download(hxd)

    # Log new bug functioality
    provision_bug_report_inputs_outputs(hxd)
