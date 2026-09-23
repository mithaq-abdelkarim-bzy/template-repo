import hx
import algorithms.rate_utilities as utils
from algorithms.rate_risk_information import rate_risk_information
from algorithms.rate_exposure_details import rate_exposure_details
from algorithms.rate_triage import rate_triage
from algorithms.rate_pricing import rate_pricing
from algorithms.rate_rate_change import rate_rate_change
from algorithms.rate_tech_eo import rate_tech_eo
from algorithms.rate_cyber import rate_cyber
from algorithms.rate_umbrella import rate_umbrella
from algorithms.rate_rating_summary import rate_rating_summary
from algorithms.model_state import model_state
#from algorithms.rate_experience_rating import rate_experience_rating
# from algorithms.tpi_summary import tpi_summary
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from libraries.email_notification.algorithms.bug_report import provision_bug_report_inputs_outputs

@hx.rating
def rating_algorithm(hxd):
    sync_hx_core(hxd)
    model_state(hxd)
    rate_risk_information(hxd)
    rate_exposure_details(hxd)
    if hxd.cds.triage_masking:
        rate_triage(hxd)    
    if hxd.cds.cyber_selection:
        rate_cyber(hxd)    
    # rate_tech_eo(hxd)  
    rate_pricing(hxd)
    # rate_umbrella(hxd)    
    rate_rating_summary(hxd)
   # rate_experience_rating(hxd)
    # tpi_summary(hxd)
    # if hxd.cds.standard_fields.is_renewal:
    if hxd.cds.is_real_renewal:
        rate_rate_change(hxd)
    
    provision_bug_report_inputs_outputs(hxd)
    
    pass