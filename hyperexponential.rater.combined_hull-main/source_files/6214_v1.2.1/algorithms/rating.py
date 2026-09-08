import hx
import algorithms.rate_utilities as utils
from algorithms.rate_risk_information import rate_risk_information

# from algorithms.rate_rate_change import rate_rate_change
from algorithms.rate_rating_summary import rate_rating_summary

from algorithms.rate_experience_rating import rate_experience_rating
from algorithms.tpi_summary import tpi_summary
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from algorithms.model_state import model_state
from algorithms.rate_vessels import rate_vessels
from algorithms.rate_coverages import rate_coverages
from algorithms.rate_modelling import rate_modelling
from algorithms.rate_portfolio_analysis import rate_portfolio_analysis
from algorithms.rate_vessel_analysis import rate_vessel_analysis
from algorithms.validation.validate_inputs import validate_inputs
from algorithms.rate_rate_change import rate_rate_change, save_lists_for_rate_change


@hx.rating
def rating_algorithm(hxd):
    sync_hx_core(hxd)
    model_state(hxd)
    rate_risk_information(hxd)
    rate_modelling(hxd)
    rate_vessels(hxd)
    rate_coverages(hxd)
    rate_vessel_analysis(hxd)
    rate_portfolio_analysis(hxd)
    rate_experience_rating(hxd)
    rate_rating_summary(hxd)
    tpi_summary(hxd)
    validate_inputs(hxd)
    if hxd.cds.standard_fields.is_renewal:
        rate_rate_change(hxd)
        save_lists_for_rate_change(hxd)

    pass
