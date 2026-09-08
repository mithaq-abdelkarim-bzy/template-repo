import hx, datetime
import pandas as pd
import numpy as np
import algorithms.utils_global_lists as lst
import algorithms.utils_functions as fx
from dateutil.relativedelta import relativedelta

def set_global_params(hxd):
    cds = hxd.cds
    layer = cds.layers[0]
    
    # ~~~~~~~~~~~~~~ GLOBAL ~~~~~~~~~~~~~~~~~~~
    
    # Set global variables

    hxd.hx_core.premium_currency = "USD"
    hxd.cds.standard_fields.insured_country = "USA"

    cds.database_id = hx.meta.policy_option_id
    cds.yoa = hxd.hx_core.inception_date.year

    # ~~~~~~~~~~~~~~ GENERAL PARAMETERS ~~~~~~~~~~~~~~~~~~~
    
   # Set primary/excess
    layer.is_primary_excess = "Excess"

    # Set bound status
    layer.is_bound = layer.status=="Bound"

    # Set flag to show rate change page
    if hxd.model_state.show_landing_page: 
        hxd.show_rate_change = False
    else:
        hxd.show_rate_change = hxd.cds.standard_fields.is_renewal 
    
    # Calculate term adjustment factor. The excess layer will be assumed to have the same policy length as the underlying layer, unless
    # overridden.
    
    hxd.info_date = "Override date if the quoted and underlying layers have different policy lengths"
    
    cds.underlying_inception_date.calculated = hxd.hx_core.inception_date
    cds.underlying_expiry_date.calculated = hxd.hx_core.expiry_date

    days_in_year = ((hxd.hx_core.inception_date + relativedelta(years=+1))- hxd.hx_core.inception_date).days
    selected_term = (hxd.hx_core.expiry_date - hxd.hx_core.inception_date).days
    
    cds.term_adjustment_underlying = (cds.underlying_expiry_date.selected - cds.underlying_inception_date.selected).days/(days_in_year)
    cds.term_adjustment = ((hxd.hx_core.expiry_date - hxd.hx_core.inception_date).days)/(days_in_year)

    # Set rating methodology
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == "Rater"
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == "Case Priced"