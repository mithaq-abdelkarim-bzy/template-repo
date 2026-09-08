##############################################################################################################################
################                             NOTES                                                            ################ 
##############################################################################################################################

### Below is orgnanised into 3 Validation Functions:
###     a) rate_validations_crcf        - anything specific to crcf
###     b) rate_validations_political   - anything specific to political
###     c) rate_validations             - anything generic and then conditions on whether political or crcf and does that



##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################

### 1) 
### 2)
### 3) 
### 4) 
### 5) 

##############################################################################################################################


import hx
import pandas as pd
import numpy as np
import re
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd


def rate_validations_crcf(hxd):

    cds         = hxd.cds 
    layer       = cds.layers[0]
    crcf_expos  = cds.exposure.granular.crcf
    crcf_mod    = cds.modifiers.crcf

    ###########################################
    ### 1) Risk Information   
    ###########################################

    ## 1d) Risk Information - CRCF additional fields
    ###########################################

    # obligor
    if (cds.risk_info.crcf_obligor  is None) and not (cds.product == "Political Risk") :
        hx.errors.validation(f"Risk Information > Obligor must be entered")

    # country
    if (cds.risk_info.crcf_country  is None) and not (cds.product == "Political Risk") :
        hx.errors.validation(f"Risk Information > Country must be entered")

    # industry group
    if (cds.risk_info.crcf_industry_group  is None) and not (cds.product == "Political Risk") :
        hx.errors.validation(f"Risk Information > Industry Group must be entered")

    # industry
    if (cds.risk_info.crcf_industry  is None) and not (cds.product == "Political Risk") :
        hx.errors.validation(f"Risk Information > Industry must be entered")

    # ihs data
    if (cds.ihs.check_run_consistent  != 'IHS extract remain valid') and not (cds.product == "Political Risk") :
        hx.errors.validation(f"Risk Information > IHS Data must be rerun")


    ###########################################
    ### 2) Exposure Details
    ###########################################

    ## 2a) Exposure Details - CRCF
    ###########################################
    
    # indemnity percent
    if ((crcf_expos.indemnity is None)      or   (crcf_expos.indemnity < 0)   or   (crcf_expos.indemnity > 1)):
        hx.errors.validation(f"Exposure Details > Indemnity Percent between 0 and 1 must be entered")

    # waiting period
    if ((crcf_expos.waiting_period is None)      or   (crcf_expos.waiting_period < 0)):
        hx.errors.validation(f"Exposure Details > Waiting Period greater than or equal to 0 must be entered")

    # pre-shipment percent
    if  (crcf_expos.pre_shipment_risk == "Yes"):
        if ((crcf_expos.pre_shipment_amt is None)    or   (crcf_expos.pre_shipment_amt < 0)   or   (crcf_expos.pre_shipment_amt > 1)):
            hx.errors.validation(f"Exposure Details > Pre-Shipment Percent between 0 and 1 must be entered")

    # Amount at Risk - Flat (note it is optional to use so we dont test on blank only negative)
    if  (crcf_expos.load_amt_basis == "Flat"):
        if (not (crcf_expos.load_amt_flat is None)) and (crcf_expos.load_amt_flat < 0):
            hx.errors.validation(f"Exposure Details > Amount at Risk - Flat - Sum Insured greater than or equal to 0 must be entered")


    # Amount at Risk - Step (note it is optional to use so we dont test on blank only negative)
    if  (crcf_expos.load_amt_basis == "Step"):
        
        # opening sum insured
        if (not (crcf_expos.load_amt_step_opening_si is None)) and (crcf_expos.load_amt_step_opening_si < 0):
            hx.errors.validation(f"Exposure Details > Amount at Risk - Step - Sum Insured greater than or equal to 0 must be entered")

        # grace period
        if (not (crcf_expos.load_amt_step_grace_period is None)) and (crcf_expos.load_amt_step_grace_period < 0):
            hx.errors.validation(f"Exposure Details > Amount at Risk - Step - Grace Period greater than or equal to 0 must be entered")

        # instalment amount
        if (not (crcf_expos.load_amt_step_instal_amt is None)) and (crcf_expos.load_amt_step_instal_amt < 0):
            hx.errors.validation(f"Exposure Details > Exposure Details > Amount at Risk - Step - Instalment Amount greater than or equal to 0 must be entered")

        # Period between instalments
        if (not (crcf_expos.load_amt_step_instal_freq is None)) and (crcf_expos.load_amt_step_instal_freq < 0):
            hx.errors.validation(f"Exposure Details > Amount at Risk - Step - Period between instalments greater than or equal to 0 must be entered")

        # term
        if (not (crcf_expos.load_amt_step_term is None)) and (crcf_expos.load_amt_step_term < 0):
            hx.errors.validation(f"Exposure Details > Amount at Risk - Step - Term greater than or equal to 0 must be entered")

    # exposure profile - check negatives - could test for monotonic decreasing without intermediate blanks but that is potentially too strict
    test = False
    for yr in crcf_expos.exposure_profile:
        for mth in range(1,13):
            value = getattr(yr, f'month_{mth}')
            if ((value is None) == False) and (value <0):       test = True
    if test == True: hx.errors.validation(f"Exposure Details > CRCF Exposure Profile has 1 or more negative values")      


    ## 2b) Exposure Details - Credit Rating - CRCF
    ###########################################

    # Grade Override no description
    if (not (crcf_mod.override.grade is None)) and ((crcf_mod.obligor_commentary is None) or (crcf_mod.obligor_commentary == '')):
        hx.errors.validation(f"Exposure Details > Grade Override - Please provide detail in obligor risk drivers commentary")

    # LGD Override no description
    if (not (crcf_mod.override.lgd is None)) and ((crcf_mod.lgd_commentary is None) or (crcf_mod.lgd_commentary == '')):
        hx.errors.validation(f"Exposure Details > LGD Override - Please provide detail in the Security & its Impact on Average LGD commentary")

    # Grade Override no description
    if (not (crcf_mod.override.uw_adj is None)) and ((crcf_mod.uw_adj_commentary is None) or (crcf_mod.uw_adj_commentary == '')):
        hx.errors.validation(f"Exposure Details > Grade Override - Please provide detail in the Underwriter Adjustments commentary")


    # Grade Override outside boundary
    if (not (crcf_mod.override.grade is None)) and (crcf_mod.override.grade != crcf_mod.selected.grade):
        hx.errors.validation(f"Exposure Details > Grade Override - Please select a grade within the given range")

    # LGD Override outside boundary
    if (not (crcf_mod.override.lgd is None)) and (crcf_mod.override.lgd != crcf_mod.selected.lgd):
        hx.errors.validation(f"Exposure Details > LGD Override - Please select a LGD within the given range")

    # Grade Override outside boundary
    if (not (crcf_mod.override.uw_adj is None)) and (crcf_mod.override.uw_adj != crcf_mod.selected.uw_adj):
        hx.errors.validation(f"Exposure Details > Grade Override - Please select a underwriter adjustment within the given range")


    ###########################################
    ### 3) Rating Summary
    ###########################################

    # rate on exposure offered
    if not (layer.crcf.metrics_summary_pst_uwadj_annual.roe_offered is None):
        if (layer.crcf.metrics_summary_pst_uwadj_annual.roe_offered <=0) or (layer.crcf.metrics_summary_pst_uwadj_annual.roe_offered >1):
            hx.errors.validation(f"Rating Summary > Rate-on-Exposure - Offered - an amount between 0 and 1 must be entered")







def rate_validations_political(hxd):

    cds         = hxd.cds 
    layer       = cds.layers[0]
    pol_expos   = cds.exposure.granular.political
    pol_mod     = cds.modifiers.political

    ###########################################
    ### 2) Exposure Details
    ###########################################

    ## 2c) Exposure Details - Political Settings
    ###########################################

    # ihs data
    if (cds.ihs.check_run_consistent        != 'IHS extract remain valid')  and (cds.product == "Political Risk") :
        hx.errors.validation(f"Exposure Details > IHS Data must be rerun")

    # simulation data
    if (pol_expos.simulation.check_run_consistent  != 'Simulation remains valid')  and (cds.product == "Political Risk") :
        hx.errors.validation(f"Exposure Details > Simulation must be rerun")


    ## 2d) Exposure Details - Political Risk
    ###########################################

    # Political Violence - Sublimit
    if (not (pol_expos.coverage_matrix.sublimit.pol_violence is None)) and (pol_expos.coverage_matrix.sublimit.pol_violence <0):
        hx.errors.validation(f"Exposure Details > Political Violence - Sublimit - an amount greater than or equal to 0 must be entered")

    # Political Violence - Deductible
    if (not (pol_expos.coverage_matrix.deductible.pol_violence is None)) and (pol_expos.coverage_matrix.deductible.pol_violence <0):
        hx.errors.validation(f"Exposure Details > Political Violence - Deductible - an amount greater than or equal to 0 must be entered")


    # Currency Inconvertibility - Sublimit
    if (not (pol_expos.coverage_matrix.sublimit.cur_inconvertibility is None)) and (pol_expos.coverage_matrix.sublimit.cur_inconvertibility <0):
        hx.errors.validation(f"Exposure Details > Currency Inconvertibility - Sublimit - an amount greater than or equal to 0 must be entered")


    # Underwriter Adjustment no description
    if (pol_mod.uw_adj_commentary is None) and ((pol_mod.override.industry != 0) or (pol_mod.override.insured_quality != 0) or (pol_mod.override.asset_composition != 0)):
        hx.errors.validation(f"Exposure Details > Overrides - Please provide detail in the Underwriter Adjustments commentary")



    # Industry Override outside boundary
    if (not (pol_mod.override.industry is None)) and (pol_mod.override.industry != pol_mod.selected.industry):
        hx.errors.validation(f"Exposure Details > Industry Override - Please Override select a within the given range")

    # Quality of Insured Override outside boundary
    if (not (pol_mod.override.insured_quality is None)) and (pol_mod.override.insured_quality != pol_mod.selected.insured_quality):
        hx.errors.validation(f"Exposure Details > Quality of Insured Override - Please select a Override within the given range")

    # Asset Composition Override outside boundary
    if (not (pol_mod.override.asset_composition is None)) and (pol_mod.override.asset_composition != pol_mod.selected.asset_composition):
        hx.errors.validation(f"Exposure Details > Asset Composition Override - Please select a Override within the given range")

    # country detail - check negatives - could test for monotonic decreasing without intermediate blanks but that is potentially too strict
    exposure_df     = pd_df_from_hx_list(pol_expos.country_exposure)
    test            = len(exposure_df) - exposure_df['check'].isin({'','ok'}).sum()
    if test == True: hx.errors.validation(f"Country Details table > Political has 1 or more anomalous values flagged for review")      



    ###########################################
    ### 3) Rating Summary
    ###########################################

    if not (layer.political.metrics_summary_pst_uwadj.rol_offered is None):
        if (layer.political.metrics_summary_pst_uwadj.rol_offered <=0) or (layer.political.metrics_summary_pst_uwadj.rol_offered >1):
            hx.errors.validation(f"Rating Summary > Rate-on-Line - Offered - an amount between 0 and 1 must be entered")








def rate_validations(hxd):

    cds     = hxd.cds 
    layer   = cds.layers[0]

    ###########################################
    ### 0) Standard Validation from Skeleton Model
    ###########################################

    # Insured name must be completed, this is needed to ensure landing page works correctly
    if not hxd.cds.standard_fields.insured_name:
        hx.errors.validation("Risk Information > Insured name field must be completed.")
    
    # Validation to check how many layers are set as bound, also updates premium label for bound policies
    bound_count = 0
    for layer in hxd.cds.layers:
        if layer.status in ["Bound", "Post Bind Complete"]:
            bound_count += 1
            layer.premium_label = "Gross Bound Premium"
        else:
            layer.premium_label = "Gross Quoted Premium"
    
    if bound_count == 0:
        hx.errors.validation("Risk Information > Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final")
    elif bound_count > 1:
        hx.errors.validation("There must be only one bound policy")


    ###########################################
    ### 1) Risk Information   
    ###########################################

    ## 1a) Risk Information - Account Details
    ###########################################

    # insured name is done as standard

    # Underwriter name
    if (not cds.standard_fields.underwriter) or (cds.standard_fields.underwriter == ''):
        hx.errors.validation("Risk Information > Underwriter name must be completed.")

    # Product name
    if (not cds.product) or (cds.product == ''):
        hx.errors.validation("Risk Information > Product name must be completed.")

    # Policy Section reference
    reference_format = "......\d\d...."
    format_description = "6 char of any type, 2 digits and 4 chars of any type"
    if (layer.section_reference is None)  or  (not re.fullmatch(reference_format, layer.section_reference)):
        hx.errors.validation(f"Risk Information > Policy Section Reference must be in the format of {format_description}")

    # Currency
    if (not cds.currencies.source_currency) or (cds.currencies.source_currency == ''):
        hx.errors.validation("Risk Information > Source Currency must be completed.")

    # expiry date
    if hxd.hx_core.expiry_date <= hxd.hx_core.inception_date:
        hx.errors.validation("Risk Information > Expiry Date must be greater than the inception date.")


    ## 1b) Risk Information - Policy Information
    ###########################################

    # policy line
    if (layer.written_line is None)             or        ((layer.written_line < 0) or (layer.written_line > 1)):
        hx.errors.validation(f"Risk Information > Written Line between 0 and 1 must be entered")

    # policy brokerage
    if ((layer.brokerage is None)==False)           and   ((layer.brokerage < 0) or (layer.brokerage >= 1)):
        hx.errors.validation(f"Risk Information > Brokerage between 0 and 1 must be entered")

    # policy limit
    if (layer.limit is None)             or        ((layer.limit <= 0)):
        hx.errors.validation(f"Risk Information > Policy Limit greater than 0 must be entered")

    # policy excess
    if (layer.excess is None)             or        ((layer.excess < 0)):
        hx.errors.validation(f"Risk Information > Policy Excess greater than or equal to 0 must be entered")

    # policy status is considered in section 0 above


    ## 1c) Risk Information - Broker Details
    ###########################################

    # Broker name
    if (not cds.standard_fields.broker) or (cds.standard_fields.broker == ''):
        hx.errors.validation("Risk Information > Broker name must be completed.")


    ######################################################################################
    ### 2) Exposure Details; 3) Rating Summary; and some additional on 1) Risk Info
    ######################################################################################
    # notice it doesnt go down either path without a valid product
    if cds.product == "Political Risk":                         rate_validations_political(hxd)
    if cds.product in {'Contract Frustration','Credit Risk'}:   rate_validations_crcf(hxd)
    