import hx

from algorithms.rate_model_state import shownby_conditions_excess, set_dropdowns, validation_functions_rating, model_state
from algorithms.rate_employee_count import rate_employee_count
from algorithms.rate_rate_change import rate_rate_change
from algorithms.rate_rating_summary import rate_rating_summary
from algorithms.rate_risk_information import rate_risk_information
from algorithms.epl.rate_usml_epl_runner import rate_usml_epl_runner
from algorithms.fiduciary.rate_usml_fi_runner import rate_usml_fi_runner
from algorithms.pcl.rate_usml_pcl_runner import rate_usml_pcl_runner
from algorithms.excess.rate_usml_excess import excess_bp_tp_calculations, excess_rc_calcs
from algorithms.tpi_summary import tpi_summary
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from libraries.admitted_excess_premium.algorithms.rate_admitted_excess import admitted_excess_pricing
from algorithms.rate_validation import rate_validations
from libraries.email_notification.algorithms.bug_report import provision_bug_report_inputs_outputs
from algorithms import rate_constants as constants  


@hx.rating
def rating_algorithm(hxd):
    model_state(hxd)
    shownby_conditions_excess(hxd)
    set_dropdowns(hxd)  
    rate_risk_information(hxd) 

    if not validation_functions_rating(hxd):
        return  # Exit early if validations fail

    primary_excess = hxd.cds.layers[0].is_primary_excess or "Primary"
    
    rate_employee_count(hxd)   
    
    if hxd.cds.coverage_elections.fid and primary_excess == "Primary":
        rate_usml_fi_runner(hxd)
    if hxd.cds.coverage_elections.epl and primary_excess == "Primary":
        rate_usml_epl_runner(hxd)
    if hxd.cds.coverage_elections.pcl and primary_excess == "Primary":
        rate_usml_pcl_runner(hxd)      

    admitted_excess_pricing(hxd)
    rate_rating_summary(hxd)
    # CB - needs to go after rating_summary as pulls benchmark premium from there      
    if (primary_excess != "Primary"):
        excess_bp_tp_calculations(hxd)

    tpi_summary(hxd)
    
    if hxd.cds.standard_fields.is_renewal:
        rate_rate_change(hxd)
        if hxd.cds.conditions_met and hxd.cds.standard_fields.is_renewal:
            excess_rc_calcs(hxd)
    rate_validations(hxd)    
    sync_hx_core(hxd)
    # Log new bug functioality
    provision_bug_report_inputs_outputs(hxd)
