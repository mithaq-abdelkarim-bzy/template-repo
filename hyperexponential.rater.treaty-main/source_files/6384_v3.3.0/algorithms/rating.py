import hx
import algorithms.rate_utilities as utils
import algorithms.rate_constants
from algorithms.rate_risk_information import rate_risk_information
from algorithms.rate_rate_change import rate_rate_change
from algorithms.rate_validation import rate_validations
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from algorithms.model_state import model_state, allow_policy_doc_download
from algorithms.policy_document import create_dict_for_excel, store_policy_data
from algorithms.timer import timer

import algorithms.udf

from algorithms.rate_pml import rate_pml
from algorithms.rate_non_modelled_perils import rate_non_modelled_perils
from algorithms.rate_burn import rate_burn
from algorithms.rate_modelling import rate_modelling
from algorithms.rate_quote import rate_quote
from algorithms.rate_aggregates import rate_aggregates
from algorithms.rate_summary import rate_summary
from algorithms.rate_calculator import rate_calculator
from algorithms.rate_simulation import rate_simulation
from algorithms.rate_additional_pages import rate_additional_pages

from algorithms.rate_risk_xl_exposure_rating import rate_risk_xl_exposure_rating

@hx.rating
def rating_algorithm(hxd):
    model_state(hxd)

    common_data_dict = rate_risk_information(hxd)

    rate_non_modelled_perils(hxd, common_data_dict)
    rate_pml(hxd, common_data_dict)
    rate_burn(hxd, common_data_dict)
    rate_modelling(hxd, common_data_dict)
    rate_risk_xl_exposure_rating(hxd, common_data_dict)
    rate_quote(hxd, common_data_dict)
    rate_aggregates(hxd, common_data_dict)
    rate_summary(hxd, common_data_dict)
    rate_calculator(hxd, common_data_dict)
    rate_simulation(hxd, common_data_dict)
    rate_rate_change(hxd, common_data_dict)
    rate_validations(hxd)
    rate_additional_pages(hxd, common_data_dict)
    sync_hx_core(hxd)
    
    # Policy doc (only run if it's the live rating algo, the transient hxd causes error)
    # if "transient_hxd" not in str(type(hxd)):
    #     store_policy_data(hxd)    
    #     allow_policy_doc_download(hxd)