# v0.5.0
import hx
import algorithms.rate_utilities as utils
from algorithms.rate_risk_information import rate_risk_information
from algorithms.rate_pricing_selection import  rate_pricing_selection, steer_rate_pricing_selection, healthcare_rate_pricing_selection, clash_rate_pricing_selection
from algorithms.rate_advanced_features import  rate_advanced_features

from algorithms.rate_rate_change import rate_rate_change
from algorithms.rate_rating_summary import rate_rating_summary 
from algorithms.rate_validation import rate_validations, missing_attribute_list
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from algorithms.model_state import model_state, allow_policy_doc_download
from algorithms.model_state_all_inputs import model_state_all_inputs
from algorithms.rate_policy_document import create_dict_for_excel, store_policy_data
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
from algorithms.rate_steer_experience_rating import rate_steer_experience_rating
from algorithms.rate_steer_exposure_rating import rate_steer_exposure_curve_descriptions, rate_steer_exposure_rating_risk_profil_bdx, rate_steer_exposure_rating_las_bdx

from libraries.email_notification.algorithms.bug_report import provision_bug_report_inputs_outputs
# from libraries.model_profiler.algorithms.profiling_hxd_functions import time_me # commented as adjusted in a specific module in the model
from algorithms.model_profiler.profiling_hxd_functions import time_me
from algorithms.schema_view.rating import schema_view_rating

from algorithms.rate_healthcare_cat_exposure_rating import rate_healthcare_cat_exposure_rating


@hx.rating
@time_me
def rating_algorithm(hxd: hx.Hxd):

    # model_state_all_inputs(hxd) # only for input only model

    model_state(hxd)
    
    rate_risk_information(hxd)
    
    if not missing_attribute_list(hxd,"limit"):
        if hxd.model_state.is_steer:
            if hxd.model_state.is_steer_experience_rating:
                rate_steer_experience_rating(hxd)
                
            if hxd.model_state.is_steer_exposure_rating_risk_profil_bdx:
                rate_steer_exposure_curve_descriptions(hxd)
                rate_steer_exposure_rating_risk_profil_bdx(hxd)

            if hxd.model_state.is_steer_exposure_rating_limit_average_severity:
                rate_steer_exposure_rating_las_bdx(hxd)
            
            steer_rate_pricing_selection(hxd)
        elif hxd.model_state.is_healthcare_cat:
            rate_healthcare_cat_exposure_rating(hxd)
            healthcare_rate_pricing_selection(hxd)
        elif hxd.model_state.is_clash:
            clash_rate_pricing_selection(hxd)

        rate_pricing_selection(hxd)

        rate_advanced_features(hxd)
        
        rate_rating_summary(hxd)
        
        if hxd.cds.standard_fields.is_renewal:        
            rate_rate_change(hxd) 

        rate_validations(hxd)

    sync_hx_core(hxd) # NOTE:Do not remove for either main or inputs only model
    
    # Policy doc (only run if it's the live rating algo, the transient hxd causes error)
    if "transient_hxd" not in str(type(hxd)):
        store_policy_data(hxd)    
        allow_policy_doc_download(hxd)

    # Log new bug functioality
    provision_bug_report_inputs_outputs(hxd)

    schema_view_rating(hxd=hxd)
    