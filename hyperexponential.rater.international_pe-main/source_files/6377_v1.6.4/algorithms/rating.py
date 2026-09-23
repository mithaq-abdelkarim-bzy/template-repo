import hx
import algorithms.rate_utilities as utils
from algorithms.rate_risk_information import rate_risk_information
from algorithms.rate_pricing_eo import rate_pricing_eo
from algorithms.rate_pricing_mediatech import rate_pricing_mediatech
from algorithms.rate_pricing_gl import rate_pricing_gl
from algorithms.rate_rate_change import rate_rate_change
from algorithms.rate_rate_change import rate_rate_change_validation
from algorithms.rate_rating_summary import rate_rating_summary
from algorithms.rate_experience_rating import rate_experience_rating
from algorithms.tpi_summary import tpi_summary
from algorithms.model_state import model_state
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from libraries.email_notification.algorithms.bug_report import provision_bug_report_inputs_outputs

@hx.rating
def rating_algorithm(hxd):
    model_state(hxd)
    rate_risk_information(hxd)
    if hxd.cds.eo_coverage_selection:
        rate_pricing_eo(hxd)
    if hxd.cds.mediatech_coverage_selection:
        rate_pricing_mediatech(hxd)
    if hxd.cds.gl_coverage_selection:
        rate_pricing_gl(hxd)
    # rate_rating_summary(hxd)
    # # rate_experience_rating(hxd)
    tpi_summary(hxd)
    if hxd.cds.standard_fields.is_renewal:
        rate_rate_change(hxd)
        rate_rate_change_validation(hxd)
    # rate_rate_change(hxd)
    # rate_rate_change_validation(hxd)
    sync_hx_core(hxd)
    provision_bug_report_inputs_outputs(hxd)
    
    pass