import hx
import algorithms.rate_utilities as utils
from algorithms.rate_risk_information import rate_risk_information
from algorithms.rate_pricing import rate_pricing
from algorithms.rate_rate_change import rate_rate_change
from algorithms.rate_risk_details import rate_risk_details

from algorithms.rate_rating_summary import rate_rating_summary
from algorithms.rate_validation import rate_validations
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from algorithms.model_state import model_state, allow_policy_doc_download
from algorithms.policy_document import create_dict_for_excel, store_policy_data


@hx.rating
def rating_algorithm(hxd):
    model_state(hxd)
    rate_risk_information(hxd)
    rate_pricing(hxd)
    rate_risk_details(hxd)
    rate_rating_summary(hxd)
    # rate_experience_rating(hxd)
    if hxd.cds.standard_fields.is_renewal:
        rate_rate_change(hxd)
    rate_validations(hxd)

    sync_hx_core(hxd) # NOTE:Do not remove for either main or inputs only model
    
    # Policy doc (only run if it's the live rating algo, the transient hxd causes error)
    if "transient_hxd" not in str(type(hxd)):
        store_policy_data(hxd)    
        allow_policy_doc_download(hxd)