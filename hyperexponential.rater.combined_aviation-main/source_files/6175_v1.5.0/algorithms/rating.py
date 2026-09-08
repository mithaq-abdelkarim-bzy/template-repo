import hx
import pandas as pd
from algorithms.rate_risk_information import rate_risk_information
from algorithms.rate_experience_rating import rate_experience_rating
from algorithms.rate_airlines import rate_airlines
from algorithms.rate_ga import rate_ga
from algorithms.rate_rating_summary import rate_rating_summary
from algorithms.quote_summary import quote_summary, store_policy_data
from algorithms.rate_rate_change import rate_rate_change, save_lists_for_rate_change
from algorithms.rate_ux import show_and_hide_pages, show_and_hide_fields, validate_status, validate_custom_fields, allow_policy_doc_download
from algorithms.model_state import model_state
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from libraries.email_notification.algorithms.bug_report import provision_bug_report_inputs_outputs


@hx.rating
def rating_algorithm(hxd: hx.Hxd):

    ### --- Renewal flow --- ###
    ms = hxd.model_state
    #expiring_policy_option_id = hx.meta.expiring_policy_option_id # or 598824 # NOTE: For debugging in dev mode
    expiring_policy_option_id = hx.meta.expiring_policy_option_id

    ### --- Set up --- ###
    model_state(hxd, expiring_policy_option_id)
    sync_hx_core(hxd)
    rate_risk_information(hxd)
    
    ### --- User experience --- ###
    show_and_hide_pages(hxd)

    if hxd.cds.is_neither: # Early exit if no product selected
        return

    show_and_hide_fields(hxd)

    ### --- Rating --- ###
    rating_df, max_liab_limit = rate_ga(hxd) if hxd.cds.is_ga else rate_airlines(hxd)    
    rate_experience_rating(hxd, rating_df)
    rate_rating_summary(hxd, max_liab_limit)
        
    quote_summary(hxd)

    if hxd.cds.standard_fields.is_renewal:
        rate_rate_change(hxd)    

    ### --- Quote Summary Doc --- ###
    store_policy_data(hxd)
    allow_policy_doc_download(hxd)
    
    ### --- Additional validations --- ###
    validate_custom_fields(hxd)
    validate_status(hxd)

    ### --- Rate Change Data --- ###
    save_lists_for_rate_change(hxd)

    ### ---Something is broken --- ###
    provision_bug_report_inputs_outputs(hxd)





 



    

