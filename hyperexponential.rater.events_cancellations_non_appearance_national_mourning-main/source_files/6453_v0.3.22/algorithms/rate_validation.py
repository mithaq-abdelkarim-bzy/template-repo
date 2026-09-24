# v0.5.0
import hx
import pandas as pd
import numpy as np
import re


ec_coverages_dict = {"all_risks"                :"All Risks",
                     "adverse_weather"          :"Adverse Weather",
                     "earthquake"               :"Earthquake",
                     "windstorm"                :"Windstorm",
                     "wildfire"                 :"Wildfire",
                     "terrorism"                :"Terrorism",
                     "cyber"                    :"Cyber",
                     "national_mourning"        :"National Mourning",
                     "riots_and_civil_commotion":"Riots and Civil Commotion",
                     "strike"                   :"Strike",
                     "war"                      :"War",
                     "catastrophic_non_app"     :"Catastrophic Non-App",
                     "ec_total"                 :"Event Cancellation Total" }


######################################################################################
### F) Experience Rating
######################################################################################
def validate_experience_rating(hxd, rater):
    
    # paths
    exp         = hxd.cds.experience_rating

    # Loss Cost Override
    if (exp.el_final_ovd is not None)         and        (exp.el_final_ovd < 0):
        hx.errors.validation(f"Experience Rating > Final Loss Cost Override greater than or equal to 0 must be entered")

    # Weight Override
    if (exp.el_weight_ovd is not None)         and       ((exp.el_weight_ovd < 0) or (exp.el_weight_ovd > 1)):
        hx.errors.validation(f"Experience Rating > Weight Override between 0 and 1 must be entered")

    ## testing df
    df = rater.get("exper_df")

    # tiv override
    if ((df['tiv_ovd'].fillna(0) <0).any()):                                # fillna so NONE does not cause an issue
        hx.errors.validation(f"Experience Rating > Exposure TIV Override cannot be negative")

    ## FINANCIALS
    # Gross Net Premium Override
    if ((df['gnwp_nominal_ovd'].fillna(0) <0).any()):                       # fillna so NONE does not cause an issue
        hx.errors.validation(f"Experience Rating > Gross Net Premium Override cannot be negative")

    # Attritional override
    if ((df['attr_incurred_ovd'].fillna(0) <0).any()):                      # fillna so NONE does not cause an issue
        hx.errors.validation(f"Experience Rating > Attritional Incurred Override cannot be negative")

    # Large override
    if ((df['large_incurred_ovd'].fillna(0) <0).any()):                     # fillna so NONE does not cause an issue
        hx.errors.validation(f"Experience Rating > Large Incurred Override cannot be negative")

    # Cat override
    if ((df['cat_incurred_ovd'].fillna(0) <0).any()):                       # fillna so NONE does not cause an issue
        hx.errors.validation(f"Experience Rating > Cat Incurred Override cannot be negative")


    ## RATE & INFLATION
    # Rate Change override
    if ((df['rate_inc_ovd'].fillna(0) <0).any()):                           # fillna so NONE does not cause an issue
        hx.errors.validation(f"Experience Rating > Rate Change Override cannot be negative")

    # Inflation override
    if ((df['inf_inc_ovd'].fillna(0) <0).any()):                            # fillna so NONE does not cause an issue
        hx.errors.validation(f"Experience Rating > Rate Change Override cannot be negative")


    ## % ULT & IELRs
    # Attritional Percent override
    if ((df['attr_pct_ultimate_ovd'].fillna(0) <0).any()):                                # fillna so NONE does not cause an issue
        hx.errors.validation(f"Experience Rating > Attritional Percent Override cannot be negative")

    # Attritional IELR override
    if ((df['attr_ielr_ovd'].fillna(0) <0).any()):                                # fillna so NONE does not cause an issue
        hx.errors.validation(f"Experience Rating > Attritional IELR Override cannot be negative")

    # Large Percent override
    if ((df['large_pct_ultimate_ovd'].fillna(0) <0).any()):                                # fillna so NONE does not cause an issue
        hx.errors.validation(f"Experience Rating > Large Percent Override cannot be negative")

    # Large IELR override
    if ((df['large_ielr_ovd'].fillna(0) <0).any()):                                # fillna so NONE does not cause an issue
        hx.errors.validation(f"Experience Rating > Large IELR Override cannot be negative")

    # Cat Percent override
    if ((df['cat_pct_ultimate_ovd'].fillna(0) <0).any()):                                # fillna so NONE does not cause an issue
        hx.errors.validation(f"Experience Rating > Cat Percent Override cannot be negative")

    # Cat IELR override
    if ((df['cat_ielr_ovd'].fillna(0) <0).any()):                                # fillna so NONE does not cause an issue
        hx.errors.validation(f"Experience Rating > Cat IELR Override cannot be negative")

    return




######################################################################################
### E) Validate Layer
######################################################################################
def validate_layer(layer, product):
    # Policy Section reference
    ec_path = layer.coverages.ec_total
    na_path = layer.coverages.na_total
    reference_format = "......\d\d...."
    format_description = "6 char of any type, 2 digits and 4 chars of any type"

    if (ec_path.section_reference is None)  or  (not re.fullmatch(reference_format, ec_path.section_reference)):
        hx.errors.validation(f"Rating Summary > Policy Section Reference > EC must be in the format of {format_description}")

    if product == "Event Cancellation with Non Appearance":
        if (na_path.section_reference.selected is None)  or  (not re.fullmatch(reference_format, na_path.section_reference.selected)):
            hx.errors.validation(f"Rating Summary > Policy Section Reference > NA must be in the format of {format_description}")

    # policy line
    if (layer.written_line is None)       or        ((layer.written_line < 0) or (layer.written_line > 1)):
        hx.errors.validation(f"Rating Summary > Written Line between 0 and 1 must be entered")

    # policy brokerage
    if ((layer.brokerage is None)==False) and       ((layer.brokerage < 0) or (layer.brokerage >= 1)):
        hx.errors.validation(f"Rating Summary > Brokerage between 0 and 1 must be entered")

    # policy limit
    if (layer.limit is None)              or        ((layer.limit <= 0)):
        hx.errors.validation(f"Rating Summary > Policy Limit greater than 0 must be entered")

    # policy excess
    if (layer.excess is not None)         and       ((layer.excess < 0)):
        hx.errors.validation(f"Rating Summary > Policy Excess greater than or equal to 0 must be entered")

    # policy deductible
    if (layer.deductible is not None)     and        ((layer.deductible < 0)):
        hx.errors.validation(f"Rating Summary > Deductible greater than or equal to 0 must be entered")

    # policy aggregate limit
    if (layer.aggregate_limit is not None)      and       ((layer.aggregate_limit < 0)):
        hx.errors.validation(f"Rating Summary > Aggregate Limit greater than or equal to 0 must be entered")

    # policy aggregate_deductible
    if (layer.aggregate_deductible is not None) and       ((layer.aggregate_deductible < 0)):
        hx.errors.validation(f"Rating Summary > Aggregate Deductible greater than or equal to 0 must be entered")

    # Quoted Premium EC
    if product == "Event Cancellation":
        if (layer.coverages.ec_total.quoted_premium_100 is None) or  ((layer.coverages.ec_total.quoted_premium_100 <= 0)):
            hx.errors.validation(f"Rating Summary > Quoted Premium (Event Cancellation) greater than 0 must be entered")

    # Quoted Premium NA    
    if product == "Event Cancellation with Non Appearance":
        if (layer.coverages.na_total.quoted_premium_100 is None) or  ((layer.coverages.na_total.quoted_premium_100 <= 0)):
            hx.errors.validation(f"Rating Summary > Quoted Premium (Non Appearance) greater than 0 must be entered")

    if product == "Case Priced":
        # Quoted Premium Case Priced
        if (layer.quoted_premium_100_case_priced is None) or  ((layer.quoted_premium_100_case_priced <= 0)):
            hx.errors.validation(f"Rating Summary > Quoted Premium greater than 0 must be entered")

        if (layer.bpi_case_priced is None)                or  ((layer.bpi_case_priced <= 0)):
            hx.errors.validation(f"Rating Summary > BPI greater than 0 must be entered")




######################################################################################
### D) Main Non- Appearance Script for Exposure
######################################################################################
def validate_non_appearance(hxd, rater):
    
    # paths
    na_path     = hxd.cds.exposure.granular.non_appearance

    # Genre 
    if (na_path.genre is None)         or        (na_path.genre == ""):
        hx.errors.validation(f"Exposure Details - Non-Appearance > Genre must be selected")

    # Number of Shows
    if (na_path.num_shows is None)         or        ((na_path.num_shows <= 0)):
        hx.errors.validation(f"Exposure Details - Non-Appearance > Number of Shows greater than 0 must be entered")    

    # Aggregate Insured Value
    if (na_path.agg_show_value is None)    or        ((na_path.agg_show_value <= 0)):
        hx.errors.validation(f"Exposure Details - Non-Appearance > Aggregate Insured Value greater than 0 must be entered")    

    # Number of Band Memebers
    if (na_path.num_band_members is None)         or        (na_path.num_band_members == ""):
        hx.errors.validation(f"Exposure Details - Non-Appearance > Number of Band Members must be selected")    

    # Claims Experience - assume ok
    # if (na_path.claim_experience is None)         or        (na_path.claim_experience == ""):
    #     hx.errors.validation(f"Exposure Details - Non-Appearance > Number of Band Members must be selected")    

    # UW Adjustment 
    if (na_path.uw_adj_sel != na_path.uw_adj_fin):
        hx.errors.validation(f"Exposure Details - Non-Appearance > Enter a UW Adjustment in the given range")

    if (na_path.uw_adj_sel != 0) and (na_path.uw_comment is None):
        hx.errors.validation(f"Exposure Details - Non-Appearance > Enter a UW Adjustment Comment")

    return



######################################################################################
### C) National Mourning Script for Exposure
######################################################################################
def validate_national_mourning(hxd, rater):
    
    # paths
    nm          = hxd.cds.exposure.granular.event_cancel.national_mourning
    nm_u75      = hxd.cds.exposure.granular.event_cancel.national_mourning.under_75
    nm_b1       = hxd.cds.exposure.granular.event_cancel.national_mourning.bespoke_1
    nm_b2       = hxd.cds.exposure.granular.event_cancel.national_mourning.bespoke_2

    # Type of Event 
    if (nm.cover_level is None)         or        (nm.cover_level == ""):
        hx.errors.validation(f"Exposure Details - National Mourning > Level of Cover must be selected")

    # Mourning Period
    if (nm.mourning_period is None) or       ((nm.mourning_period < 0) or (nm.mourning_period >= 25)):
        hx.errors.validation(f"Exposure Details - National Mourning > Mourning between 0 and 25 must be entered")

    # Check Column
    df = rater.get("nm_indiv_df")
    table_check = ((df['check'] != "OK").sum()   != 0)
    if (nm_u75.check != "OK") or (nm_b1.check != "OK") or (nm_b2.check != "OK") or table_check:
        hx.errors.validation(f"Exposure Details - National Mourning > Review Check Column please")

    return


######################################################################################
### B) Main Event Cancellation Script for Exposure
######################################################################################
def validate_event_cancellation(hxd, rater):
    
    ec_path = hxd.cds.exposure.granular.event_cancel
    cvg_path= hxd.cds.exposure.granular.event_cancel.base_coverages
    ms_path = hxd.model_state
    # Type of Event 
    if (ec_path.event_type is None)         or        (ec_path.event_type == ""):
        hx.errors.validation(f"Exposure Details - Event Cancellation > Type of Event must be selected")
    
    # UW Adjustment & Sub-limit   
    for key, value in ec_coverages_dict.items():
        if key == "ec_total":
            continue
        
        path = getattr(cvg_path, key)
        
        if key == "all_risks" or path.covered:
            if (path.uw_adj_sel != path.uw_adj_fin):
                hx.errors.validation(f"Exposure Details - Event Cancellation > {value} enter a UW Adjustment in the given range")

            if (path.uw_adj_sel != 0) and (path.uw_comment is None):
                hx.errors.validation(f"Exposure Details - Event Cancellation > {value} enter a UW Adjustment Comment") 

            if key != "all_risks":
                if (path.sublimit is not None) and ((path.sublimit <= 0)):
                    hx.errors.validation(f"Exposure Details - Event Cancellation > {value} Sublimit greater than 0 must be entered")

    # Cyber Trigger    
    path = cvg_path.cyber
    if path.covered:
        if path.trigger is None:
            hx.errors.validation(f"Exposure Details - Event Cancellation > Cyber Trigger must be entered")

    # National Mourning Trigger
    path = cvg_path.national_mourning
    if path.covered:
        if hxd.model_state.use_nm_app_old_model:
            if path.trigger is None:
                hx.errors.validation(f"Exposure Details - Event Cancellation > National Mourning Trigger must be entered")
        else:
            validate_national_mourning(hxd, rater)

    # Cat Non-App Trigger & delegates %
    path = cvg_path.catastrophic_non_app
    if path.covered:
        if path.trigger is None:
            hx.errors.validation(f"Exposure Details - Event Cancellation > Catastrophic Non-App Trigger must be entered")
        if (path.delegates is None) or       ((path.delegates < 0) or (path.delegates >= 1)):
            hx.errors.validation(f"Exposure Details - Event Cancellation > Catastrophic Non-App Delegates% between 0 and 1 must be entered")

    # Terrorism Modifiers
    path        = cvg_path.terrorism
    mods_path   = ec_path.terrorism_terms
    if path.covered:
        if mods_path.time_distance is None:
            hx.errors.validation(f"Exposure Details - Event Cancellation > Terrorism Time/Distance must be entered")
        if mods_path.event_profile is None:
            hx.errors.validation(f"Exposure Details - Event Cancellation > Terrorism Event Profile must be entered")
        if mods_path.city_load is None:
            hx.errors.validation(f"Exposure Details - Event Cancellation > Terrorism City Load must be entered")

    # Exposure Curve
    if  (ec_path.exposure_curve != "Standard")   and   (ec_path.exposure_curve_comments is None):
        hx.errors.validation(f"Exposure Details - Event Cancellation > Exposure Curve non-Standard, please add a comment")          

    # Experience Ratio
    if (ec_path.experience)    and       ((ec_path.experience_ratio is None)  or  (ec_path.experience_ratio == "") ):
        hx.errors.validation(f"Exposure Details - Event Cancellation > Experience Adjustment, please select a loss ratio range")    

    # NCB Ratio
    if (ec_path.ncb) and (ec_path.ncb_offered is not None) and ((ec_path.ncb_offered < 0) or (ec_path.ncb_offered >= 1)):
        hx.errors.validation(f"Exposure Details - Event Cancellation > NCB% between 0 and 1 must be entered")                       

    # Simulation
    if (ms_path.run_simulation):
        hx.errors.validation(f"Exposure Details - Event Cancellation > Simulation needs to be run")

    # IHS
    if (ms_path.run_ihs):
        hx.errors.validation(f"Exposure Details - Event Cancellation > IHS needs to be run")



    # event cancellation entries - YZ requested removed 3-August 2026 - possibility of splitting into hard and soft checks and only doing hard checks but day 2 probably
    # df = rater.get("ec_events_df")
    # if ((df['check'] != "OK").sum()   != 0):
    #     hx.errors.validation(f"Exposure Details - Event Cancellation > Events Table - please review issues flagged in Check column")

    return



######################################################################################
### A) Main Validation Script
######################################################################################
def rate_validations(hxd, rater):

    cds = hxd.cds

    ###########################################
    ### 1) Risk Information   
    ###########################################

    # Insured name must be completed, this is needed to ensure landing page works correctly
    if not cds.standard_fields.insured_name:
        hx.errors.validation("Risk Information > Insured name must be completed.")

    # Underwriter name
    if (not cds.standard_fields.underwriter) or (cds.standard_fields.underwriter == ''):
        hx.errors.validation("Risk Information > Underwriter name must be completed.")

    # Currency
    if (not cds.currencies.source_currency) or (cds.currencies.source_currency == ''):
        hx.errors.validation("Risk Information > Source Currency must be completed.")

    # expiry date
    if hxd.hx_core.expiry_date <= hxd.hx_core.inception_date:
        hx.errors.validation("Risk Information > Expiry Date must be greater than the inception date.")

    # Event name
    if (not cds.risk_info.event_name) or (cds.risk_info.event_name == ''):
        hx.errors.validation("Risk Information > Event name must be completed.")

    # Broker name
    if (not cds.standard_fields.broker) or (cds.standard_fields.broker == ''):
        hx.errors.validation("Risk Information > Broker name must be completed.")


    ###########################################
    ### 2) Rating Summary / Layer Information   
    ###########################################

    # Validation to check how many layers are set as bound, also updates premium label for bound policies
    bound_count = 0
    for layer in cds.layers:
        if layer.status in ["Bound", "Post Bind Complete"]:
            bound_count += 1
            layer.premium_label = "Gross Bound Premium"
        else:
            layer.premium_label = "Gross Quoted Premium"
    
    if bound_count == 0:
        hx.errors.validation("Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final")

    # all the layer validations other than status
    if cds.standard_fields.is_rater_priced:
        validate_layer(hxd.cds.layers[0], "Event Cancellation")        # for event canc. we can validate these fields irrespective  
        if cds.risk_info.product_bool:
            for layer in hxd.cds.layers: 
                if layer.status in ["Bound", "Post Bind Complete"]:     # for non-app practically we can only validate these fields if marked as bound where multi-layer
                    validate_layer(layer, "Event Cancellation with Non Appearance")      
   
    else:
        validate_layer(hxd.cds.layers[0], "Case Priced")
        if (cds.case_pricing_analysis_location is None) or (cds.case_pricing_analysis_location == ""):
            hx.errors.validation(f"Rating Summary > Case Pricing File Analysis Path nust be filled in")



    ######################################################################################
    ### 3) Exposure Details
    ######################################################################################
    if cds.standard_fields.is_rater_priced:    
        validate_event_cancellation(hxd, rater)
        if cds.risk_info.product_bool:
            validate_non_appearance(    hxd, rater)
    
    ######################################################################################
    ### 4) Experience Rating
    ######################################################################################
    if cds.standard_fields.is_rater_priced:  
        validate_experience_rating(hxd, rater)

    ######################################################################################
    ### 5) Policy Document
    ######################################################################################
    if hxd.policy_doc.show_download == False:  
        hx.errors.validation("Rationale > Policy Document must be generated prior to finalisation")