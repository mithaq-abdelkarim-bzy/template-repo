##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
### 1) Consider add optional to grace period description
### 2) 

##############################################################################################################################
##############################################################################################################################
import hx
import numpy as np
import pandas as pd
import math as math
from algorithms.rate_utilities import pd_df_from_hx_list
from datetime import datetime



###############################################################################################################
### function to generate a vector of impacts for all countries and covers                                   ###
###############################################################################################################
def fill_exposure_profile(hxd,progress):

    
    #################################################################
    ### 1) Collect Values                                         ###
    #################################################################

    cds                 = hxd.cds
    exp_settings        = cds.exposure.granular.crcf

    term                = cds.risk_info.crcf_term
    basis               = exp_settings.load_amt_basis

    step_sum_insured    = exp_settings.load_amt_step_opening_si
    step_instal_amt     = exp_settings.load_amt_step_instal_amt
    
    step_instal_period  = exp_settings.load_amt_step_instal_freq
    step_grace_period   = exp_settings.load_amt_step_grace_period
    step_term           = exp_settings.load_amt_step_term

    flat_sum_insured    = exp_settings.load_amt_flat


    #################################################################
    ### 2) Error Trap Values                                      ###
    #################################################################

    status_init         = "Please resolve the following issues to proceed: "
    status              = status_init

    if term <= 0:                           status  += "Policy Term <= 0; "
    if basis == "":                         status  += "No Basis Entered; "

    if basis == "Step":
        if step_sum_insured is None:        status  += "Sum Insured is Missing; "
        elif step_sum_insured <=0:          status  += "Sum Insured <= 0; "
        
        if step_instal_period is None:      status  += "Instalment Period is Missing; "
        elif step_instal_period <=0:        status  += "Instalment Period <= 0; "
        
        if step_grace_period is None:       status  += "Grace Period is Missing; "
        elif step_grace_period <=0:         status  += "Grace Period <= 0; "
        
        if step_term is None:               step_term = term                                # assigning value where missing
        elif step_term <=0:                 status  += "Term <= 0; "                

        if (step_instal_amt is not None):
            if step_instal_amt<=0:          status  += "Instalment Amount <= 0; "
        elif (status == status_init):       step_instal_amt = step_sum_insured / ( (math.ceil(min(step_term,  term))  - step_grace_period)  / step_instal_period  +  1)   # assigning value where missing and no status warning


    if basis == "Flat":
        if flat_sum_insured is None:        status  += "Sum Insured is Missing; "
        elif flat_sum_insured <=0:          status  += "Sum Insured <= 0; "

    # check if any errors have been raised and if so write to hxd and exit function
    if status != status_init:
        exp_settings.last_run_status = status                                                                     
        return


    #################################################################
    ### 3) Calculate Values and write to hxd                      ###
    #################################################################


    last_mth = math.ceil(    min(step_term,  term)   if basis == "Step" else term    )
    for index, row in enumerate(exp_settings.exposure_profile):

        for inc_mth in range(1, 13):
            cum_mth = index * 12   +   inc_mth
            if cum_mth <= last_mth:
                if basis == "Step": 
                    amount = max(0,  step_sum_insured  - max(0,   step_instal_amt  * (1  + (cum_mth - step_grace_period - 1) // step_instal_period)))
                else:              
                    amount = flat_sum_insured
                setattr(row,f'month_{inc_mth}',amount)  

    exp_settings.last_run_date            = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    exp_settings.last_run_status          = f"{basis} Exposure Loaded at {exp_settings.last_run_date}."
    exp_settings.last_run_value           = (f"SI={step_sum_insured}; instal_pd={step_instal_period}; instal_amt={step_instal_amt}; grace_pd={step_grace_period}; term={last_mth}"
                                            if basis == "Step" 
                                            else f"SI={flat_sum_insured}; term={last_mth}")


