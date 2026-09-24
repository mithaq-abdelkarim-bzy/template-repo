import hx
import algorithms.rate_utilities as utils
from algorithms.rate_risk_information import rate_risk_information
from algorithms.rate_pricing import rate_pricing
from algorithms.rate_pricing_runoff import rate_pricing_runoff
from algorithms.rate_rate_change import rate_rate_change, constant_private_rate_change
from algorithms.admitted_pricing import admitted_pricing
from algorithms.admitted_excess_pricing import admitted_excess_pricing
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from algorithms.model_state import model_state
from algorithms.historical_freq import historical_freq
from algorithms.rate_private_priced import private_priced

from libraries.email_notification.algorithms.bug_report import provision_bug_report_inputs_outputs


@hx.rating
def rating_algorithm(hxd):
    model_state(hxd)
    rate_risk_information(hxd)
    
    if hxd.cds.review_type.rater_priced:
        admitted_pricing(hxd)
        admitted_excess_pricing(hxd)
        rate_pricing(hxd)
        rate_pricing_runoff(hxd)
        historical_freq(hxd)
    else:
        private_priced(hxd)
        historical_freq(hxd)
        constant_private_rate_change(hxd)

    if hxd.cds.standard_fields.is_renewal:
        rate_rate_change(hxd)
    sync_hx_core(hxd)

    bug_report_node = getattr(hxd, "bug_report", None)
    if bug_report_node is not None:
        provision_bug_report_inputs_outputs(hxd)

    pass