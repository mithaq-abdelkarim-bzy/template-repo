import hx
import pandas as pd
import numpy as np
import algorithms.utils_global_lists as lst
from algorithms.utils_debug import fn_debug
from algorithms.modifiers import modifiers
from algorithms.tpi_summary import tpi_summary
from algorithms.min_max_coverage import min_max_coverage
from algorithms.validations import validations
from algorithms.experience_rating import experience_rating
from algorithms.set_global_params import set_global_params
from algorithms.calc_totals import calc_totals
from algorithms.set_coverage_premium import set_coverage_premium
from algorithms.rate_change import rate_change
from algorithms.model_state import model_state
from algorithms.rate_rating_summary import rate_rating_summary
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from libraries.email_notification.algorithms.bug_report import provision_bug_report_inputs_outputs


@hx.rating
def rating_algorithm(hxd):

    # Called at the start so that the rest of the code can modify some of the variables here
    # but still initializing expiry_date and inception_date which is the intention
    # Details in: https://beazley.atlassian.net/browse/RRG-13193
    sync_hx_core(hxd)
    
    set_global_params(hxd)
    
    set_coverage_premium(hxd)

    rate_rating_summary(hxd)

    min_max_coverage(hxd)

    experience_rating(hxd)
    
    modifiers(hxd)

    calc_totals(hxd)
   
    tpi_summary(hxd)
    
    if hxd.cds.standard_fields.is_renewal is True:
        rate_change(hxd)

    model_state(hxd)

    fn_debug(hxd)
 
    provision_bug_report_inputs_outputs(hxd)

    validations(hxd)
    
    pass
