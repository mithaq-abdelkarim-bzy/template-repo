
import hx
import algorithms.rate_utilities as utils
from algorithms.rate_risk_information import rate_risk_information
from algorithms.rate_pricing import rate_pricing
from algorithms.rate_rate_change import rate_rate_change
from algorithms.rate_rating_summary import rate_rating_summary
from algorithms.rate_validation import rate_validations
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
# from algorithms.rate_experience_rating import rate_experience_rating
from algorithms.model_state import model_state
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE


@hx.rating
def rating_algorithm(hxd):
    model_state(hxd)
    rate_risk_information(hxd)
    rate_pricing(hxd)
    rate_rating_summary(hxd)
    # rate_experience_rating(hxd)
    if hxd.cds.standard_fields.is_renewal:
        if RARC_INSURED_ASSET_USE:      # False for Specialty Professions
            pass
        if not RARC_COVERAGE_USE:       # False - layer-level calc for Specialty Professions
            rate_rate_change(hxd)       # NOTE: calculation at a layer level.
        else:                           # False - layer-level calc for Specialty Professions
            pass

    rate_validations(hxd)
    
    sync_hx_core(hxd)
    