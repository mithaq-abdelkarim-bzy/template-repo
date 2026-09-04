import hx
import algorithms.rate_utilities                            as      utils
from algorithms.rate_risk_information                       import  rate_risk_information
from algorithms.rate_exposure_details                       import  rate_exposure_details
from algorithms.rate_rating_summary                         import  rate_rating_summary
from algorithms.tpi_summary                                 import  tpi_summary
from algorithms.eso_outputs                                 import  eso_outputs
from algorithms.validation_outputs                          import  validations
from libraries.common_data_schema.algorithms.sync_hx_core   import  sync_hx_core
from algorithms.model_state                                 import  model_state
from algorithms.generate_doc                                import allow_policy_doc_download
from libraries.email_notification.algorithms.bug_report     import provision_bug_report_inputs_outputs



@hx.rating
def rating_algorithm(hxd):
    model_state(hxd)
    rate_risk_information(hxd)
    rate_exposure_details(hxd)
    rate_rating_summary(hxd)
    eso_outputs(hxd)
    tpi_summary(hxd)
    validations(hxd)
    sync_hx_core(hxd)
    allow_policy_doc_download(hxd)
    provision_bug_report_inputs_outputs(hxd)

    
    pass