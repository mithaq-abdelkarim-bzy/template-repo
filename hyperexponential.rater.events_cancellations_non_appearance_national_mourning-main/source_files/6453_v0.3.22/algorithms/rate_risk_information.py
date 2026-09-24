# v0.5.0
import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_constants as const
from algorithms.rate_utilities import policy_term
from operator import itemgetter


def rate_risk_information(hxd, rater):

    cds = hxd.cds
    ri  = hxd.cds.risk_info
    cvg = hxd.cds.layers[0].coverages

    # Extracts database id for the risk information tab
    hxd.cds.policy_option_id = hx.meta.policy_option_id


    # calculating term
    hxd.cds.rating_factors.policy_term = policy_term(hxd.hx_core.inception_date, hxd.hx_core.expiry_date)


    # calculating profuct and na policy section ref
    if ri.product_bool:
        ri.product = "Event Cancellation with Non Appearance" 
        cvg.na_total.section_reference.calculated = cvg.ec_total.section_reference
    else:
        ri.product = "Event Cancellation" 


    # assigning sf to cds
    cds.standard_fields.policy_reference    = '' if cvg.ec_total.section_reference is None else cvg.ec_total.section_reference[:8]
    cds.standard_fields.benchmark_class     = const.BP_CLASS
    cds.standard_fields.trifocus            = const.BP_CLASS
    cds.layers[0].trifocus                  = const.BP_CLASS
    cds.layers[0].section_reference         = "Refer EC & NA coverages"


    # copying these from model state as they affect pricing so can be seen in snowflake
    hxd.cds.rating_factors.use_nm_app_old_model = hxd.model_state.use_nm_app_old_model  
    hxd.cds.rating_factors.use_determ_agg_calc  = hxd.model_state.use_determ_agg_calc   
    hxd.cds.rating_factors.is_migrated          = hxd.model_state.is_migrated   
    hxd.cds.rating_factors.disable_validation   = hxd.model_state.disable_validation   


    pass