import hx
import pandas as pd
import numpy as np
import algorithms.utils_global_lists as lst
from algorithms.utils_debug import fn_debug
from algorithms.modifiers import modifiers
from algorithms.layer_calcs import layer_calcs
from algorithms.tpi_summary import tpi_summary
from algorithms.validations import validations
from algorithms.set_global_params import set_global_params
from algorithms.rate_change import rate_change
from algorithms.model_state import model_state
from algorithms.rate_rating_summary import rate_rating_summary
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from libraries.email_notification.algorithms.bug_report import provision_bug_report_inputs_outputs
from libraries.admitted_excess_premium.algorithms.rate_admitted_excess import admitted_excess_pricing
from algorithms.rate_unity_premium import rate_unity_premium
 


@hx.rating
def rating_algorithm(hxd):

    # Called at the start so that the rest of the code can modify some of the variables here
    # but still initializing expiry_date and inception_date which is the intention
    # Details in: https://beazley.atlassian.net/browse/RRG-13193
    sync_hx_core(hxd)
    
    set_global_params(hxd)
    
    layer_calcs(hxd)
    
    rate_rating_summary(hxd)
    
    validations(hxd)

    model_state(hxd)

    rate_unity_premium(hxd)

    admitted_excess_pricing(hxd)

    tpi_summary(hxd)
    

    if hxd.cds.standard_fields.is_renewal is True:
        rate_change(hxd)
    
    fn_debug(hxd)

    provision_bug_report_inputs_outputs(hxd)
    
    pass
