import hx
import pandas as pd
from algorithms.rate_risk_information import rate_risk_information
from algorithms.rate_life import rate_life
from algorithms.rate_lives import calculate_sum_insured, aggregate_lives, rate_lives, rate_agg_limits
from algorithms.rate_experience_rating import rate_experience_rating
from algorithms.rate_rating_summary import rate_rating_summary
from algorithms.quote_summary import quote_summary, store_policy_data
from algorithms.rate_rate_change import rate_rate_change
from algorithms.rate_ux import show_and_hide_pages, show_and_hide_fields, validate_status, allow_policy_doc_download
from algorithms.model_state import model_state
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from libraries.email_notification.algorithms.bug_report import provision_bug_report_inputs_outputs


@hx.rating
def rating_algorithm(hxd):

    ### --- Set up --- ###
    model_state(hxd)
    validate_status(hxd)
    rate_risk_information(hxd)
    
    ### --- User experience --- ###
    show_and_hide_pages(hxd)
    show_and_hide_fields(hxd)

    ### --- Rating --- ###
    
    # Individual
    rate_life(hxd)

    # Group
    calculate_sum_insured(hxd)
    aggregate_lives(hxd)
    rate_lives(hxd)
    rate_agg_limits(hxd)
    rate_experience_rating(hxd)
    rate_rating_summary(hxd)
    quote_summary(hxd)

    if hxd.cds.standard_fields.is_renewal:
        rate_rate_change(hxd)

    ### --- Utilities and additional validation --- ###
    sync_hx_core(hxd)

    ### --- Quote Summary Doc --- ###
    store_policy_data(hxd)
    allow_policy_doc_download(hxd)

    provision_bug_report_inputs_outputs(hxd)



 



    

