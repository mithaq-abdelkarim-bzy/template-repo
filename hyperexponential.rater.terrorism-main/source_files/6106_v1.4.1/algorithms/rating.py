import hx
from algorithms.rate_risk_information                       import rate_risk_information
from algorithms.rate_countries                              import rate_countries
from algorithms.rate_exposure                               import rate_exposure, rate_cover_details, rate_construction
from algorithms.rate_rating_summary                         import rate_rating_summary
from algorithms.rate_rate_change                            import rate_rate_change, save_lists_for_rate_change

from algorithms.rate_validations                            import rate_validations
from algorithms.rate_show_hide                              import rate_show_hide
from algorithms.model_state                                 import model_state, allow_policy_doc_download
from algorithms.policy_document                             import create_dict_for_excel, store_policy_data
from libraries.common_data_schema.algorithms.sync_hx_core   import sync_hx_core



@hx.rating
def rating_algorithm(hxd: hx.Hxd):

    ### --- Set up --- ###
    model_state(hxd)
    sync_hx_core(hxd)
    rate_risk_information(hxd)
    rate_show_hide(hxd)    
    hxd.live_hxd = False if "transient_hxd" in str(type(hxd)) else True    # determine if using transient hxd and store a flag accoridngly for use elsewhere in the model
    hxd.cds.rationale.help_file = ( "User Guide, Quick Starts, Training Videos are stored [here](https://beazley.sharepoint.com/sites/ActuarialPricing).")

    ### --- Rating --- ###
    rate_cover_details(hxd)
    roe_df, curves_df = rate_countries(hxd)
    rate_exposure(hxd, roe_df)
    rate_construction(hxd, roe_df)
    term_factor = rate_rating_summary(hxd, curves_df)
    rate_rate_change(hxd, term_factor)

    ### --- Quote Summary Doc --- ###

    # Policy doc (only run if it's the live rating algo, the transient hxd causes error)
    if hxd.live_hxd:
        store_policy_data(hxd)    
        allow_policy_doc_download(hxd)

    ### --- Additional validations --- ###
    rate_validations(hxd)

    ### --- Rate Change Data --- ###
    save_lists_for_rate_change(hxd)






 



    

