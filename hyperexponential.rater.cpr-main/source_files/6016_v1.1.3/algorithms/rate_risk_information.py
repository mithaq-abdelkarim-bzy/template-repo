##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################

### 1) 
### 2) 
### 2) 
### 4) 
### 5) 

##############################################################################################################################



import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_constants as const
from algorithms.rate_utilities import policy_term
from dateutil.relativedelta import relativedelta
from datetime import datetime
from operator import itemgetter


def rate_risk_information(hxd):

    cds         = hxd.cds
    layer       = cds.layers[0]

    # Extracts database id for the risk information tab
    hxd.cds.policy_option_id = hx.meta.policy_option_id

    ###########################################
    ### 1) Map to cds - standard fields   
    ###########################################

    cds.standard_fields.policy_reference    = '' if layer.section_reference is None else layer.section_reference[:8]
    cds.standard_fields.benchmark_class     = const.bp_class
    cds.standard_fields.trifocus            = const.bp_class
    
    if cds.product in {'Contract Frustration','Credit Risk'}:     cds.standard_fields.insured_country     = cds.risk_info.crcf_country


    ###########################################
    ### 2) Map to cds - standard layer fields   
    ###########################################

    layer.currency              = cds.currencies.source_currency
    layer.trifocus              = cds.standard_fields.trifocus
    layer.aggregate_limit       = layer.limit
    layer.aggregate_excess      = layer.excess 


    ###########################################
    ### 3) Derive Policy Term
    ###########################################

    # notice policy_term here reflect the true number of days of coverage and will be use to calculate the actual rates rather than displayed 
    cds.rating_factors.policy_term = (hxd.hx_core.expiry_date    +    relativedelta(days=1)    -    hxd.hx_core.inception_date).days / 365.25 * 12

    # Calculate the difference in months after adding 1 day so see (1-jul-24 to 30-jun-25) as 1 complete year if entered that way
    # notice this differs from policy_term below which is used in the main rating algorithm where the focus is on the true days of coverage
    # here we are interested in the complete numnber of months plus the fraction of the month which is more intuitive to UW and in line with the CRCF exposure profile by month displayed
    incept                        = hxd.hx_core.inception_date
    expiry                        = hxd.hx_core.expiry_date 
    expiry_plus1                  = expiry   +  relativedelta(days=1)
    complete_months               = ( 12 * (      expiry_plus1.year  - incept.year        )
                                         + (      expiry_plus1.month - incept.month       )
                                         + (-1 if expiry_plus1.day   < incept.day   else 0) )
    complete_months_end_date      = incept + relativedelta(months=complete_months)
    complete_to_expiry_days       =(expiry                      -   complete_months_end_date).days
    additional_days               = max(0, complete_to_expiry_days)
    cds.risk_info.crcf_term                 = complete_months + additional_days / 365.25 * 12
    cds.exposure.granular.political.tenor   = complete_months + additional_days / 365.25 * 12


    ###########################################
    ### 4) Setup BI load info
    ###########################################

    cds.bi.calc_run_value         = cds.layers[0].section_reference
    cds.bi.check_run_consistent   =("BI extract remain valid" if cds.bi.last_run_value == cds.bi.calc_run_value 
                                                              else "BI needs to be rerun - values have changed")
    pass