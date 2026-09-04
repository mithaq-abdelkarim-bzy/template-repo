##############################################################################################################################
################                             NOTES                                                            ################ 
##############################################################################################################################

### 

##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################

### 1) check Rationale > Underwriter Rationale still works once limit has been filled in
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


    # ###########################################
    # ### 1) Risk Information   
    # ###########################################

    # ## 1a) Risk Information - Account Details
    # ###########################################

    # expiry date
    if hxd.hx_core.expiry_date <= hxd.hx_core.inception_date:
        hx.errors.validation("Risk Information > Expiry Date must be greater than the inception date.")


    # Underwriter name
    if (not cds.standard_fields.underwriter) or (cds.standard_fields.underwriter == ''):
        hx.errors.validation("Risk Information > Underwriter name must be completed.")

    # Source System
    if (not cds.policy_info.source_system) or (cds.policy_info.source_system == ''):
        hx.errors.validation("Risk Information > Source System must be completed.")

    # # insured name is done as standard

    # Policy Section reference
    reference_format = "......\d\d...."
    format_description = "6 char of any type, 2 digits and 4 chars of any type"
    if (layer.section_reference is None)  or  (not re.fullmatch(reference_format, layer.section_reference)):
        hx.errors.validation(f"Risk Information > Policy Section Reference must be in the format of {format_description}")

    # Currency
    if (not cds.currencies.source_currency) or (cds.currencies.source_currency == ''):
        hx.errors.validation("Risk Information > Source Currency must be completed.")



    # ## 1b) Risk Information - Policy Information
    # ###########################################

    # policy line
    if (layer.written_line is None)             or        ((layer.written_line < 0) or (layer.written_line > 1)):
        hx.errors.validation(f"Risk Information > Written Line between 0 and 1 must be entered")

    # order
    if (layer.order is None)                    or        ((layer.order < 0)        or (layer.order > 1)):
        hx.errors.validation(f"Risk Information > Order between 0 and 1 must be entered")

    # line
    if ((layer.line is None)==False)           and        ((layer.line < 0)):
        hx.errors.validation(f"Risk Information > Line (Currency) greater than or equal to 0 must be entered")

    # Terrorism Only
    if (cds.policy_info.terrorism_only is None) or        ((cds.policy_info.terrorism_only < 0)    or (cds.policy_info.terrorism_only > 1)):
        hx.errors.validation(f"Risk Information > TO (Terrorism Only) between 0 and 1 must be entered")

    # War on Land
    if (cds.policy_info.war_on_land is None)    or        ((cds.policy_info.war_on_land < 0)    or (cds.policy_info.war_on_land > 1)):
        hx.errors.validation(f"Risk Information > WL (War on Land) between 0 and 1 must be entered")

    # TO + WL
    if round(cds.policy_info.terrorism_only + cds.policy_info.war_on_land,  4) != 1:
        hx.errors.validation(f"Risk Information > TO (Terrorism Only) and WL (War on Land) must add to 1 in aggregate")

    # policy status is considered in section 0 above

    # policy brokerage
    if ((layer.brokerage is None)==False)           and   ((layer.brokerage < 0) or (layer.brokerage >= 1)):
        hx.errors.validation(f"Risk Information > Brokerage between 0 and 1 must be entered")


    # # policy limit
    # if (layer.limit is None)             or        ((layer.limit <= 0)):
    #     hx.errors.validation(f"Risk Information > Policy Limit greater than 0 must be entered")

    # # policy excess
    # if (layer.excess is None)             or        ((layer.excess < 0)):
    #     hx.errors.validation(f"Risk Information > Policy Excess greater than or equal to 0 must be entered")



    ######################################################################################
    ### 2) Exposure Details; 3) Rating Summary; and some additional on 1) Risk Info
    ######################################################################################
    
    
    ## countries validation 
    # 1) ON MAIN CODE PAGE: if any warning messages have been displayed as part of 
    #       a) check_multi_si   = checking we dont have both sum insured at a TOTAL level and BI/PD level
    #       b) loc_condition    = checking #loc, pml, selected si filled in & where  # loc =1 the pml=Selected SI and vis-a-vis if loc>1 then pml != Selected SI
    #       c) check_negatives  = checking no negative numeric values on row
    # 2) ON MAIN CODE PAGE: requiring ihs to be loaded/reloaded


    ## exposure validation
    # 1) ON MAIN CODE PAGE: Validating risk adjustment are between min & max.

    # ihs underwriting adjustments
    civil_unrest_uw_adj_test = False
    war_uw_adj_test          = False
    terrorism_uw_adj_test    = False

    for country in cds.exposure.granular.countries:
        if (country.civil_unrest_uw_adj < 0.5   or country.civil_unrest_uw_adj  > 2) :       civil_unrest_uw_adj_test   = True
        if (country.war_uw_adj < 0.5            or country.war_uw_adj           > 2) :       war_uw_adj_test            = True
        if (country.terrorism_uw_adj    < 0.5   or country.terrorism_uw_adj     > 2) :       terrorism_uw_adj_test      = True

    if civil_unrest_uw_adj_test == True: hx.errors.validation(f"Exposure Details > Civil Unrest - override - value must be between 50% and 200% of the value before override")
    if war_uw_adj_test          == True: hx.errors.validation(f"Exposure Details > War - override - value must be between 50% and 200% of the value before override")
    if terrorism_uw_adj_test    == True: hx.errors.validation(f"Exposure Details > Terrorism - override - value must be between 50% and 200% of the value before override")


    # risk adjustment overrides
    # REMOVE: the validation for individual category
    # path_root = layer.risk_adjustments
    # for name, structure in zip(["Security", "Industry", "Policy", "IHS Score"],["security", "industry", "policy", "ihs_score"]):
    #     path = getattr(path_root, structure)
    #     missing_rationale = (path.uw_rationale is None) or (path.uw_rationale == "")
    #     if path.override is not None and missing_rationale and (round(path.calculated,3) != round(path.override,3)):
    #         hx.errors.validation(f"Exposure Details > Risk Adjustments > {name} - override - please provide rationale where override is used.")
    # INCLUDE: the validation for the new Overall Comment
    

    # bi wait period
    value           = cds.exposure.aggregate.details.bi_wait_period
    BIWaitPeriod    = hx.params.BIWaitPeriod
    value_min       = BIWaitPeriod["BI Wait Period"].min()
    value_max       = BIWaitPeriod["BI Wait Period"].max()
    if ((value is None)==False)           and   ((value< value_min) or (value > value_max)):
        hx.errors.validation(f"Exposure Details > BI Wait Period (days) between {value_min} and {value_max} must be entered")
    
    # bi indemnity period
    value               = cds.exposure.aggregate.details.bi_indemnity_period 
    BIIndemnityPeriod   = hx.params.BIIndemnityPeriod
    value_min           = BIIndemnityPeriod["BI Indemnity Period"].min()
    value_max           = BIIndemnityPeriod["BI Indemnity Period"].max()
    if ((value is None)==False)           and   ((value< value_min) or (value > value_max)):
        hx.errors.validation(f"Exposure Details > BI Indemnity Period (months) between {value_min} and {value_max} must be entered")
    

    ## Construction
    test      = False
    value_cum = 0
    for year in cds.layers[0].coverages.construction.years:
        value       = year.build_up_override or 0
        # value_cum  += value 
        if (value < 0 or value > 1) :  test   = True
    # if (value_cum != 0 and value_cum != 1): hx.errors.validation(f"Construction > Build Up override, where used must sum to 1")
    if (test==True                       ): hx.errors.validation(f"Construction > Build Up override, all values must be between 0 and 1")


    
    ## rating summary

    # Quoted premium - policy period
    if (layer.quoted_premium_100_pct is None) and (layer.quoted_rol is None):
        hx.errors.validation("Rating Summary > Please enter a Gross Quoted Premium or Gross Quoted ROL")
    
    if (layer.quoted_premium_100_pct is not None) and (layer.quoted_rol is not None):
        hx.errors.validation("Rating Summary > Please only enter Gross Quoted Premium or Gross Quoted ROL - not both")
    
    if (layer.quoted_premium_100_pct is not None) and (layer.quoted_premium_100_pct < 0):
        hx.errors.validation("Rating Summary > Please enter Gross Quoted Premium greater than 0")    

    if (layer.quoted_rol is not None) and (layer.quoted_rol < 0 or layer.quoted_rol >= 1):
        hx.errors.validation("Rating Summary > Please enter Gross Quoted ROL between 0% and 100%")    


    ## Rationale
    # Chris Parker request 4-June-2025
    # IR edit 13-Jan-2025: Adapted for all currencies
    ccy = cds.currencies.source_currency
    fx_to_usd = cds.exposure.granular.fx_to_usd
    # Convert caps to source currency
    quoted_premium_cap = 1e5 * fx_to_usd # 100,000 USD
    limit_cap = 1e8 * fx_to_usd # 100m USD
    # Display warning in source currency
    if ccy != "USD":
        warning_prem = f"Rationale > Underwriter Rationale - Please add commentary for all risks where Premium to Beazley exceeds 100,000 USD ({quoted_premium_cap:,.0f} {ccy})"
        warning_limit =  f"Rationale > Underwriter Rationale - Please add commentary for all risks where Limit Deployed exceeds 100m USD ({limit_cap:,.0f} {ccy})"
    else:
        warning_prem = f"Rationale > Underwriter Rationale - Please add commentary for all risks where Premium to Beazley exceeds $100,000"
        warning_limit =  f"Rationale > Underwriter Rationale - Please add commentary for all risks where Limit Deployed exceeds $100m"
    # Trigger warning
    if (cds.standard_fields.uw_rationale is None) or (cds.standard_fields.uw_rationale == ""):
        if (layer.quoted_premium is not None)  and (layer.quoted_premium             > quoted_premium_cap): hx.errors.validation(warning_prem)
        if (layer.limit is not None)           and (layer.limit * layer.written_line > limit_cap): hx.errors.validation(warning_limit)


    ## Peril Sheet
    # main perils
    path_root        = hxd.cds.exposure.aggregate.perils
    for structure in [  "terrorism", "sabotage",    "rscc",         "damage",   "insurrection", "coup"
                      , "war",       "insurgency",  "liability",    "cyber",    "nrcb",         "looting"]:
        path = getattr(path_root,structure)
        if path.limit_override      is not None and path.limit_override         < 0 : 
            hx.errors.validation(f"Peril Sheet > Limit Override > {structure} - should not be negative") 

        if path.excess_override     is not None and path.excess_override        < 0 : 
            hx.errors.validation(f"Peril Sheet > Excess Override > {structure} - should not be negative") 

        if path.deductible_override is not None and path.deductible_override    < 0 : 
            hx.errors.validation(f"Peril Sheet > Deductible Override > {structure} - should not be negative") 

    # cbi perils        
    path_root        = hxd.cds.exposure.aggregate.cbi_perils
    for structure in ["unnamed", "named", "interruption", "denial", "ingress", "authority"]:
        path = getattr(path_root,structure)
        if path.limit_selected      is not None and path.limit_selected         < 0 : 
            hx.errors.validation(f"Peril Sheet > Limit > {structure} - should not be negative") 

        if path.excess_selected     is not None and path.excess_selected        < 0 : 
            hx.errors.validation(f"Peril Sheet > Excess > {structure} - should not be negative") 

        if path.deductible_selected is not None and path.deductible_selected    < 0 : 
            hx.errors.validation(f"Peril Sheet > Deductible > {structure} - should not be negative") 
        
        if path.distance_selected   is not None and path.distance_selected     < 0 : 
            hx.errors.validation(f"Peril Sheet > Distance > {structure} - should not be negative") 