import hx
import algorithms.rate_utilities as utils
from algorithms.rate_risk_information                       import rate_risk_information
from algorithms.rate_rate_change                            import rate_rate_change
from algorithms.rate_rating_summary                         import rate_rating_summary
from algorithms.rate_validation                             import rate_validations
from algorithms.rate_exposure_details                       import rate_exposure_details
from libraries.common_data_schema.algorithms.sync_hx_core   import sync_hx_core
from algorithms.model_state                                 import model_state, allow_policy_doc_download
from algorithms.policy_document                             import create_dict_for_excel, store_policy_data
from algorithms.rate_show_hide                              import rate_show_hide


@hx.rating
def rating_algorithm(hxd):
    # determine if using transient hxd and store a flag accoridngly for use elsewhere in the model
    hxd.live_hxd = False if "transient_hxd" in str(type(hxd)) else True

    model_state(hxd)
    rate_risk_information(hxd)
    rate_exposure_details(hxd)
    rate_rating_summary(hxd)

    # only run rate change if renewal and they have entered a premium rate
    if hxd.cds.standard_fields.is_renewal and hxd.cds.layers[0].quoted_premium is not None: rate_rate_change(hxd)
    
    rate_validations(hxd)
    rate_show_hide(hxd)
    sync_hx_core(hxd)
    hxd.cds.rationale.help_file = ( "User Guide, Quick Starts, Training Videos are stored [here](https://beazley.sharepoint.com/sites/ActuarialPricing).")
                                   

    # Policy doc (only run if it's the live rating algo, the transient hxd causes error)
    if hxd.live_hxd:
        store_policy_data(hxd)    
        allow_policy_doc_download(hxd)