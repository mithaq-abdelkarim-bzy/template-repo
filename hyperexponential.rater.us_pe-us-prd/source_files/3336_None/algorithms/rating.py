import hx
import algorithms.rate_utilities as utils
from algorithms.rate_risk_information import rate_risk_information
from algorithms.rate_exposure import rate_exposure
from algorithms.rate_rating_summary import rate_rating_summary
from algorithms.validations.validation_exposure import validate_exposure
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core


@hx.rating
def rating_algorithm(hxd):

    rate_risk_information(hxd)
    rate_exposure(hxd)
    validate_exposure(hxd)
    rate_rating_summary(hxd)
    sync_hx_core(hxd)

    pass
