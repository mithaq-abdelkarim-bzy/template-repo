import hx
import algorithms.rate_utilities as utils
from algorithms.rate_risk_information import rate_risk_information
from algorithms.rate_exposure import rate_exposure
from algorithms.rate_rating_summary import rate_rating_summary
from algorithms.rate_rate_change import rate_rate_change
from algorithms.validations.validation_exposure import validate_exposure
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from algorithms.model_state import model_state


@hx.rating
def rating_algorithm(hxd):
    model_state(hxd)
    rate_risk_information(hxd)
    rate_exposure(hxd)
    validate_exposure(hxd)
    rate_rating_summary(hxd)
    if hxd.cds.standard_fields.is_renewal:
        rate_rate_change(hxd)
    sync_hx_core(hxd)

    pass
