# v0.5.0
import hx
import algorithms.rate_utilities as utils
import algorithms.rate_startup
from algorithms.rate_risk_information               import rate_risk_information
from algorithms.rate_exposure_event_cancellation    import rate_exposure_event_cancellation
from algorithms.rate_exposure_non_appearance        import rate_exposure_non_appearance
from algorithms.rate_experience_rating              import rate_experience_rating
from algorithms.rate_rate_change                    import rate_rate_change, rate_rate_change_coverages,rate_rate_change_coverages, save_insured_asset_list_for_rate_change
from algorithms.rate_rating_summary                 import rate_rating_summary
from algorithms.rate_validation                     import rate_validations
from algorithms.model_state                         import model_state, model_state_after, allow_policy_doc_download
from algorithms.policy_document                     import create_dict_for_excel, store_policy_data
from algorithms.data_schema.sch_rater_defined       import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
from algorithms.rate_rater                          import rater_load, rater_save



from libraries.common_data_schema.algorithms.sync_hx_core        import sync_hx_core
from libraries.email_notification.algorithms.bug_report          import provision_bug_report_inputs_outputs
from libraries.schema_viewer.algorithms.schema_view              import schema_view_rating
from libraries.model_profiler.algorithms.profiling_hxd_functions import time_me, timer

@time_me
@hx.rating
def rating_algorithm(hxd):

    model_state(hxd)
    
    rater = {}
    rater_load(                         hxd, rater)
    rate_risk_information(              hxd, rater)
    rate_exposure_event_cancellation(   hxd, rater)

    if hxd.cds.risk_info.product_bool:
        rate_exposure_non_appearance(   hxd, rater)

    rate_experience_rating(             hxd, rater)
    rate_rating_summary(                hxd, rater)
    rater_save(                         hxd, rater)

    if hxd.cds.standard_fields.is_renewal:
        rate_rate_change(hxd) # NOTE: calculation at a layer level. Can be removed if not used
    
    model_state_after(hxd)

    hxd.cds.rationale.help_file = ( "User Guide, Quick Starts, Training Videos are stored [here](https://beazley.sharepoint.com/sites/ActuarialPricing).")

    sync_hx_core(hxd) # NOTE:Do not remove for either main or inputs only model
    
    # Policy doc (only run if it's the live rating algo, the transient hxd causes error)
    if "transient_hxd" not in str(type(hxd)):
        store_policy_data(hxd)
        allow_policy_doc_download(hxd)

    # run validation checks as long as not disabled.
    if hxd.model_state.disable_validation == False:
        rate_validations(                   hxd, rater)

    # Log new bug functioality
    provision_bug_report_inputs_outputs(hxd)

    schema_view_rating(hxd=hxd)
    