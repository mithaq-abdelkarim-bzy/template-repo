import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter


def rate_risk_information(hxd):
    # Extracts database id for the risk information tab
    hxd.cds.database_id = hx.meta.policy_option_id

    fx_param_table = hx.params.table_fx_rates
    hxd.cds.currencies.source_currency = hx.params.table_fx_rates[hx.params.table_fx_rates["ccy_name"] == hxd.cds.source_currency_name]["ccy"].iloc[0]
    hxd.cds.local_currency_output = hxd.cds.currencies.source_currency

    hxd.cds.eo_fees_currency_label = "Total Fees in " + hxd.cds.local_currency_output
    hxd.cds.mediatech_revenue_currency_label= "Total Revenue in " + hxd.cds.local_currency_output
    hxd.cds.gl_revenue_currency_label= "Revenue in " + hxd.cds.local_currency_output
    hxd.cds.gl_revenue_total_currency_label= "Total Revenue in " + hxd.cds.local_currency_output
    hxd.cds.gl_local_currency_label = "Show Policy Limits and Retention in Source Currency: " + hxd.cds.local_currency_output


    coverage_selection = hxd.cds.coverage_selection


    #default to not show any coverage
    hxd.cds.eo_coverage_selection = False
    hxd.cds.mediatech_coverage_selection = False
    hxd.cds.gl_coverage_selection= False

    if coverage_selection == "E&O":
        hxd.cds.eo_coverage_selection = True
    elif coverage_selection == "Media Tech":
        hxd.cds.mediatech_coverage_selection = True
    elif coverage_selection == "GL":
        hxd.cds.gl_coverage_selection = True
    
    hxd.cds.gl_coverage_selection_opposite = not hxd.cds.gl_coverage_selection

        
    #Add validation for time difference. This model can only model for 1 year
    time_difference = hxd.hx_core.expiry_date - hxd.hx_core.inception_date
    time_difference_years = round((time_difference.days/365.25))
    if(time_difference_years > 1):
        hx.errors.validation("Risk Information: Policy Term must be 1 year!")

    #Add validation that only one cover can be priced in this rater
    if hxd.cds.eo_coverage_selection == True:
        if (hxd.cds.exposure.aggregate.mediatech_revenue is not None):
            if (hxd.cds.exposure.aggregate.mediatech_revenue > 0 ):
                hx.errors.validation("E&O Coverage is Selected! Please clean exposure input in 'Exposure Media Tech'!")
        if (hxd.cds.exposure.granular.gl_revenue[0].revenue_input is not None ):
            if (hxd.cds.exposure.granular.gl_revenue[0].revenue_input > 0):
                hx.errors.validation("E&O Coverage is Selected! Please clean exposure input in 'Exposure GL'!")

    if hxd.cds.mediatech_coverage_selection == True:
        if (hxd.cds.exposure.aggregate.eo_total_fees is not None):
            if (hxd.cds.exposure.aggregate.eo_total_fees > 0 ):
                hx.errors.validation("Media Tech Coverage is Selected! Please clean exposure input in 'Exposure E&O'!")
        if (hxd.cds.exposure.granular.gl_revenue[0].revenue_input is not None ):
            if (hxd.cds.exposure.granular.gl_revenue[0].revenue_input > 0):
                hx.errors.validation("Media Tech Coverage is Selected! Please clean exposure input in 'Exposure GL'!")

    if hxd.cds.gl_coverage_selection == True:
        if (hxd.cds.exposure.aggregate.eo_total_fees is not None):
            if (hxd.cds.exposure.aggregate.eo_total_fees > 0 ):
                hx.errors.validation("GL Coverage is Selected! Please clean exposure input in 'Exposure E&O'!")
        if (hxd.cds.exposure.aggregate.mediatech_revenue is not None):
            if (hxd.cds.exposure.aggregate.mediatech_revenue > 0 ):
                hx.errors.validation("GL Coverage is Selected! Please clean exposure input in 'Exposure Media Tech'!")

    # Add validation that insured name must input
    if coverage_selection is not None:
        if hxd.cds.standard_fields.insured_name is None:
            hx.errors.validation("Risk Information: Insured Name Cannot be Empty! Please either select an insured from the list or entered a new insured in the search box!")

    # Add validation that policy length cannot be more than 20 characters
    policy_reference = hxd.cds.standard_fields.policy_reference
    if policy_reference is not None:
        if len(policy_reference) > 20:
            hx.errors.validation("Risk Information: Policy Reference cannot exceed 20 characters!")
    





    pass