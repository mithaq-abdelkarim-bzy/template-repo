import hx
import time
import algorithms.rate_utilities as utils
from algorithms.rate_risk_information import rate_risk_information
from algorithms.rate_risk_assessment import rate_risk_assessment
from algorithms.rate_pricing import rate_pricing
from algorithms.rate_rate_change import rate_rate_change
from algorithms.rate_rating_summary import rate_rating_summary
from algorithms.rate_exposure_details import rate_exposure_details
from algorithms.rate_rating_summary_mmp import rate_rating_summary_mmp
from algorithms.rate_change_layers import rate_change_layers
# from algorithms.rate_experience_rating import rate_experience_rating
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from algorithms.model_state import model_state
from algorithms.dropdown_validations import run_validation
from algorithms.rate_dashboard import rate_dashboard
from libraries.email_notification.algorithms.bug_report import provision_bug_report_inputs_outputs


@hx.rating
def rating_algorithm(hxd):
    model_state(hxd)
    rate_risk_information(hxd)
    rate_risk_assessment(hxd)
    rate_exposure_details(hxd)
    rate_dashboard(hxd)
    rate_pricing(hxd)
    rate_rating_summary_mmp(hxd)
    rate_rating_summary(hxd)
    rate_change_layers(hxd)
    # rate_experience_rating(hxd)
    # tpi_summary(hxd)
    if hxd.cds.standard_fields.is_renewal:
        rate_rate_change(hxd)
    sync_hx_core(hxd)

    run_validation(hxd)
    provision_bug_report_inputs_outputs(hxd)
    
    pass