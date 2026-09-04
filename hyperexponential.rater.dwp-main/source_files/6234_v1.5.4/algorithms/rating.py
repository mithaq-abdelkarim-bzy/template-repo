import hx
from algorithms.rate_utilities import rates_display
from algorithms.rate_risk_information import rate_risk_information
from algorithms.rate_pricing_education import rate_pricing_education
from algorithms.rate_pricing_non_education import rate_pricing_non_education
from algorithms.rate_rate_change import rate_rate_change
from algorithms.rate_rating_summary import rate_rating_summary
from algorithms.rate_experience_rating import rate_experience_rating
from algorithms.rate_validations import rate_validations
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from algorithms.model_state import model_state, allow_policy_doc_download
from algorithms.rate_layer_calcs import rate_layer_calcs
from algorithms.policy_document import create_dict_for_excel, store_policy_data
from libraries.email_notification.algorithms.bug_report import provision_bug_report_inputs_outputs



@hx.rating
def rating_algorithm(hxd):
    model_state(hxd)
    rate_risk_information(hxd)
    rate_pricing_education(hxd)
    rate_pricing_non_education(hxd)
    rate_layer_calcs(hxd)
    rate_experience_rating(hxd)
    rate_rating_summary(hxd)
    
    if hxd.cds.standard_fields.is_renewal:
        rate_rate_change(hxd)

    rate_validations(hxd)
    # rates_display(hxd) # removed for now to make hxd smaller for debugging rc 
    sync_hx_core(hxd)
    
    # Policy doc (only run if it's the live rating algo, the transient hxd causes error)
    if "transient_hxd" not in str(type(hxd)):
        store_policy_data(hxd)    
        allow_policy_doc_download(hxd)

    provision_bug_report_inputs_outputs(hxd)
    