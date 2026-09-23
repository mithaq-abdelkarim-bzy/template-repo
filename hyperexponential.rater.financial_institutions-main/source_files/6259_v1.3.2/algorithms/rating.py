import hx
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core

from algorithms.model_state import model_state
from algorithms.rate_cover_details import rate_cover_details
from algorithms.rate_exposure_details import rate_exposure_details
from algorithms.rate_rate_change import rate_rate_change
from algorithms.rate_rating_summary import rate_rating_summary
from algorithms.rate_risk_assessment import rate_risk_assessment
from algorithms.rate_risk_information import rate_risk_information


@hx.rating
def rating_algorithm(hxd):
    model_state(hxd)
    rate_risk_information(hxd)
    rate_exposure_details(hxd)
    rate_cover_details(hxd)
    rate_risk_assessment(hxd)
    rate_rating_summary(hxd)
    if hxd.cds.standard_fields.is_renewal:
        rate_rate_change(hxd)
    sync_hx_core(hxd)
