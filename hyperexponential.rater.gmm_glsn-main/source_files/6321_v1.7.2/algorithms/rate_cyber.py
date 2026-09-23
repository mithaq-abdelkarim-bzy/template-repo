import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter
from datetime import date
from dateutil.relativedelta import relativedelta
from algorithms.rate_constants import max_options, max_layers
from algorithms import parameter_tables_schema as params


def rate_cyber(hxd):
    cds = hxd.cds

    #----------------------------------------------------------------------------------------------#
    #step 1: Set the show/hide masking for BBR/InfoSec and Option labels
    #----------------------------------------------------------------------------------------------#

    cds.bbr_masking = True if cds.rating_factors.cyber.product == "BBR" else False
    cds.infosec_masking = True if cds.rating_factors.cyber.product == "InfoSec" else False
    cds.rating_factors.cyber.bbr_rater_info_by = "Enter total modelled Premium (First Party and Third Party Premium) from the BBR rater here"
    cds.rating_factors.cyber.third_party_only_info_by = "Third Party Premium only"

    #This is to set the option label
    for index, x in enumerate(cds.cyber_options):
        x.option_label = f"Option {index+1}"

    if cds.rating_factors.cyber.first_or_third_party == "First Party and Third Party":
        cds.rating_factors.cyber.first_or_third_party_note = 'For First AND Third Party, please use the BBR rater to rate the risk, and then enter the policy and premium information in the relevant Option.'
        cds.rating_factors.cyber.first_and_third_party_show = True 
        cds.rating_factors.cyber.third_party_only_show = False 
    else:
        cds.rating_factors.cyber.first_or_third_party_note = 'For Third Party only, please complete the rest of this page.'
        cds.rating_factors.cyber.first_and_third_party_show = False 
        cds.rating_factors.cyber.third_party_only_show = True 

    # Excess Cyber note
    if cds.rating_factors.cyber.include_excess == True:
        cds.rating_factors.cyber.excess_cyber_note = "Note: For excess layers, there may be differences in attachment points between cyber and non-cyber coverages."
    else:
        cds.rating_factors.cyber.excess_cyber_note = ""

    # Excess Cyber Calc note #IR edit
    selected_option = int(cds.option_selected[-1]) - 1
    if (cds.rating_factors.cyber.include_excess == True) and (cds.cyber_options[selected_option].policy_agg_limit is None):
        cds.rating_factors.cyber.excess_cyber_calc_note = "Please populate primary Policy Agg. Limit of Lia. for the selected option, in order for excess cyber coverage to be calculated."
    else:
        cds.rating_factors.cyber.excess_cyber_calc_note = ""

    # Validation error: require primary policy agg limit to be entered, if First and Third Party and excess coverage. #IR edit
    # selected_option = int(cds.option_selected[-1]) - 1
    # if (cds.rating_factors.cyber.first_or_third_party == "First Party and Third Party") and (cds.rating_factors.cyber.include_excess == True) and (cds.cyber_options[selected_option].policy_agg_limit is None): 
    #     # print("working") #for debugging
    #     hx.errors.validation("Please populate primary Policy Agg. Limit of Lia. [Cyber tab], in order for excess cyber coverage to be calculated.")


    #----------------------------------------------------------------------------------------------#
    #step X: Fill in the schedule rating table 
    #----------------------------------------------------------------------------------------------#   
    cyber_schedule_rating_params= hx.params.table_cyber_schedule_rating
    cyber_name = cyber_schedule_rating_params["description_name"]
    cyber_sched_value = []
   
    for y in cyber_name:
        setattr(getattr(cds.modifiers.cyber, y),"min", cyber_schedule_rating_params[cyber_schedule_rating_params["description_name"]== y]["min"].iloc[0])
        setattr(getattr(cds.modifiers.cyber, y),"max", cyber_schedule_rating_params[cyber_schedule_rating_params["description_name"]== y]["max"].iloc[0])
        cyber_sched_value.append(getattr(getattr(cds.modifiers.cyber, y),"value"))


    schedule_mod_validation =  cyber_schedule_rating_params
    schedule_mod_validation["min"]  = pd.to_numeric(schedule_mod_validation["min"]) 
    schedule_mod_validation["max"]  = pd.to_numeric(schedule_mod_validation["max"]) 
    schedule_mod_validation["schedule_mod_value"] = cyber_sched_value
    schedule_mod_validation["validation"] = np.where((schedule_mod_validation["schedule_mod_value"] < schedule_mod_validation["min"]) | (schedule_mod_validation["schedule_mod_value"] > schedule_mod_validation["max"]) ,True,False)

    if schedule_mod_validation["validation"].sum() > 0 :
        hx.errors.validation("Cyber Schedule Rating Value Outside Allowable Range")


    #----------------------------------------------------------------------------------------------#
    #Start Pricing from here
    #----------------------------------------------------------------------------------------------#    
    #Parameter tables

    # FX rate for currency conversion - from user library
    fx_rates = params.fx_rates.df()
    ccy = cds.currencies.source_currency
    fx_rate = utils.look_up(ccy, 'ccy', 'fx_rate', fx_rates, if_not_found=1) # default to USD if error
    ccy_usd_conversion = 1 / fx_rate

    bbr_base_premium_params = hx.params.table_cyber_base_premium_bbr
    bbr_base_rate_params = hx.params.table_cyber_base_rate_bbr
    infosec_base_premium_params = hx.params.table_cyber_base_premium_infosec
    infosec_base_rate_params = hx.params.table_cyber_base_rate_infosec
    cyber_constants_params = hx.params.table_cyber_constants
    cyber_agg_limit_ilf_params = hx.params.table_cyber_agg_limit_ilf
    cyber_notified_guideline_params = hx.params.table_cyber_notified_guideline
    cyber_notified_params = hx.params.table_cyber_notified_retention_ratio
    cyber_agg_retention_guideline_params = hx.params.table_cyber_aggregate_retention_guideline
    cyber_agg_retention_ratio_params = hx.params.table_cyber_agg_retention_ratio_modifier
    cyber_privacy_breach_params = hx.params.table_cyber_privacy_breach_response
    cyber_payment_card_limit_params = hx.params.table_cyber_payment_card_limit
    cyber_deleted_coverage_params = hx.params.table_cyber_additional_coverages_deleted
    cyber_bi_pd_params = hx.params.table_cyber_bi_pd
    cyber_reg_defence_params = hx.params.table_cyber_regulatory_defence
    
    #----------------------------------------------------------------------------------------------#
    # Pricing 01: Base Premium
    #----------------------------------------------------------------------------------------------#   
    total_revenue = cds.exposure.aggregate.revenue

    if total_revenue <= 0:
        total_revenue_usd = (-total_revenue) * ccy_usd_conversion
    else : 
        total_revenue_usd = total_revenue * ccy_usd_conversion

    cyber_product = hxd.cds.rating_factors.cyber.product


    if cyber_product is None:
        cyber_product = "BBR"
    

    filter_table_temp_bbr = bbr_base_premium_params[bbr_base_premium_params["revenue_start"] <= total_revenue_usd].iloc[-1]
    filter_table_temp_rate_bbr = bbr_base_rate_params[bbr_base_rate_params["revenue_start"] <= total_revenue_usd].iloc[-1]

    filter_table_temp_infosec =infosec_base_premium_params[infosec_base_premium_params["revenue_start"] <= total_revenue_usd].iloc[-1]
    filter_table_temp_rate_infosec = infosec_base_rate_params[infosec_base_rate_params["revenue_start"] <= total_revenue_usd].iloc[-1]
        
    base_prem_start_bbr = filter_table_temp_bbr["base_premium"]
    base_prem_revenue_start_bbr = filter_table_temp_bbr["revenue_start"]
    base_rate_bbr = filter_table_temp_rate_bbr["base_rate"]

    base_prem_start_infosec = filter_table_temp_infosec ["base_premium"]
    base_prem_revenue_start_infosec = filter_table_temp_infosec ["revenue_start"]   
    base_rate_infosec = filter_table_temp_rate_infosec["base_rate"]

    cyber_base_premium_bbr= base_prem_start_bbr + base_rate_bbr * (total_revenue_usd - base_prem_revenue_start_bbr )/1000
    cyber_base_premium_infosec= base_prem_start_infosec + base_rate_infosec * (total_revenue_usd - base_prem_revenue_start_infosec )/1000

    model_brokerage = cyber_constants_params[cyber_constants_params["factor_name"] == "Model Brokerage"]["factor"].iloc[0]
    net_prlr = cyber_constants_params[cyber_constants_params["factor_name"] == "Net Priced to LR"]["factor"].iloc[0]
    target_lr = cyber_constants_params[cyber_constants_params["factor_name"] == "Target LR"]["factor"].iloc[0]

    cyber_base_premium_final_bbr = cyber_base_premium_bbr*(1-model_brokerage)*(net_prlr/target_lr)
    cyber_base_premium_final_infosec = cyber_base_premium_infosec*(1-model_brokerage)*(net_prlr/target_lr)
    

    #----------------------------------------------------------------------------------------------#
    # Pricing 02: Policy Aggregate Limit
    #----------------------------------------------------------------------------------------------#    
    #cyber_options_df = utils.pd_df_from_hx_list(cds.cyber_options)

    cyber_options_dict = [{
        "policy_agg_limit": item.policy_agg_limit,
        "notified_individuals_limit": item.notified_individuals_limit,
        "policy_agg_retention": item.policy_agg_retention,
        "legal_forensic_limit": item.legal_forensic_limit,
        "defense_penalties_limit": item.defense_penalties_limit,
        "payment_card_limit": item.payment_card_limit,
        "brokerage": item.brokerage,
        "model_premium_bbr_rater": item.model_premium_bbr_rater
        } for item in cds.cyber_options]
        
    cyber_options_df = pd.DataFrame(cyber_options_dict)



    cyber_policy_agg_limit = cyber_options_df["policy_agg_limit"]
    cyber_policy_agg_limit = cyber_policy_agg_limit.fillna(0)
    cyber_policy_agg_limit_usd = cyber_policy_agg_limit * (ccy_usd_conversion)
    agg_limit_max = cyber_constants_params[cyber_constants_params["factor_name"] == "Aggregate Maximum Limit"]["factor"].iloc[0]
    agg_limit_min = cyber_constants_params[cyber_constants_params["factor_name"] == "Aggregate Minimum Limit"]["factor"].iloc[0]

    agg_limit_ilf = np.interp(cyber_policy_agg_limit_usd, cyber_agg_limit_ilf_params["limit"], cyber_agg_limit_ilf_params["low"])


    #----------------------------------------------------------------------------------------------#
    # Pricing 03: Individual Notification Limit
    #----------------------------------------------------------------------------------------------#   
    filter_table_temp = cyber_notified_guideline_params[cyber_notified_guideline_params["revenue_from"] <= total_revenue_usd].iloc[-1]
    retention_slope = filter_table_temp["slope"]
    retention_intercept = filter_table_temp["intercept"]
    retention_min = filter_table_temp["min"]
    retention_max = filter_table_temp["max"]
    guideline_retention_notification = retention_slope*total_revenue_usd + retention_intercept
    guideline_retention_notification = max(guideline_retention_notification, retention_min)
    guideline_retention_notification = min(guideline_retention_notification, retention_max)

    cyber_notified_retention = cyber_options_df["notified_individuals_limit"]
    cyber_notified_retention = cyber_notified_retention.fillna(0)
    cyber_notified_retention_usd = cyber_notified_retention * (ccy_usd_conversion)
    cyber_notified_retention_ratio = cyber_notified_retention_usd.divide(guideline_retention_notification)

    cyber_notified_retention_ratio_factor  = np.interp(cyber_notified_retention_ratio, cyber_notified_params["retention_ratio_lower"], cyber_notified_params["modifier_lower"])

    #----------------------------------------------------------------------------------------------#
    # Pricing 04: Policy Aggregate Retention
    #----------------------------------------------------------------------------------------------#   
    filter_table_temp = cyber_agg_retention_guideline_params[cyber_agg_retention_guideline_params["revenue_from"] <= total_revenue_usd].iloc[-1]
    retention_slope = filter_table_temp["slope"]
    retention_intercept = filter_table_temp["intercept"]
    retention_min = filter_table_temp["min"]
    retention_max = filter_table_temp["max"]   
    guideline_agg_retention= retention_slope*total_revenue_usd + retention_intercept
    guideline_agg_retention = max(guideline_agg_retention, retention_min)
    guideline_agg_retention = min(guideline_agg_retention,retention_max)

    cyber_agg_retention_df = cyber_options_df["policy_agg_retention"]
    cyber_agg_retention_df = cyber_agg_retention_df.fillna(0)
    cyber_agg_retention_usd = cyber_agg_retention_df * (ccy_usd_conversion)
    cyber_agg_retention_ratio = cyber_agg_retention_usd.divide(guideline_agg_retention)

    if cyber_product == "BBR":
        cyber_agg_retention_factor = np.interp(cyber_agg_retention_ratio, cyber_agg_retention_ratio_params["ratio_lower"],cyber_agg_retention_ratio_params["bbr_modifier_lower"] )
    else:
         cyber_agg_retention_factor = np.interp(cyber_agg_retention_ratio, cyber_agg_retention_ratio_params["ratio_lower"],cyber_agg_retention_ratio_params["infosec_modifier_lower"] )


    #----------------------------------------------------------------------------------------------#
    # Pricing 05: Loss Rating
    #----------------------------------------------------------------------------------------------#
    cyber_loss_ratio= utils.pd_df_from_hx_list(cds.modifiers.cyber.cyber_loss_rating)
    cyber_params= hx.params.table_cyber_loss_rating
    cyber_loss_ratio_merge = cyber_loss_ratio.merge(cyber_params,how= "left", left_on =["cyber_loss_ratio"],right_on = ["loss_ratio"])
    cyber_loss_ratio_asign = cyber_loss_ratio_merge.loc[:,["cyber_loss_ratio","default","lower_bound","upper_bound"]]
    cyber_loss_ratio_asign["floor"] = 1
    cyber_loss_ratio_asign["default_value"] = np.maximum(cyber_loss_ratio_asign["lower_bound"], cyber_loss_ratio_asign["floor"])
    cyber_loss_ratio_asign["default_value"] = np.minimum(cyber_loss_ratio_asign["default_value"], cyber_loss_ratio_asign["upper_bound"])
    cyber_loss_ratio_asign = cyber_loss_ratio_asign.rename(columns={"default_value":"cyber_loss_ratio_selected_calculated","lower_bound":"cyber_loss_ratio_min","upper_bound":"cyber_loss_ratio_max"})

    utils.write_pd_to_hxd(cyber_loss_ratio_asign,cds.modifiers.cyber.cyber_loss_rating,
    ["cyber_loss_ratio_min","cyber_loss_ratio_max"],override_cols_to_write = ["cyber_loss_ratio_selected"]) 

    cyber_loss_ratio_factor = getattr(getattr(cds.modifiers.cyber.cyber_loss_rating[0], "cyber_loss_ratio_selected"), "selected")

    
    #----------------------------------------------------------------------------------------------#
    # Pricing 05: Legal Forensic Limit
    #----------------------------------------------------------------------------------------------#
    cyber_forensic_limit = cyber_options_df["legal_forensic_limit"]
    cyber_forensic_limit = cyber_forensic_limit.fillna(0)
    cyber_forensic_limit_usd = cyber_forensic_limit * (ccy_usd_conversion)
    bbr_max_sublimit = cyber_constants_params[cyber_constants_params["factor_name"] == "BBR Max Sublimit"]["factor"].iloc[0]

    cyber_standard_limit = [min(x,bbr_max_sublimit ) for x in cyber_policy_agg_limit_usd]
    cyber_forensic_limit_ratio = [ 0 if y == 0 else x/y for (x,y) in zip(cyber_forensic_limit_usd,cyber_standard_limit)]
    
    cyber_forensic_limit_ratio_factor = np.interp(cyber_forensic_limit_ratio, cyber_privacy_breach_params["open_low"], cyber_privacy_breach_params["default"])

    # for item in cyber_forensic_limit_ratio:
    #     if item >= 1:
    #         hx.errors.validation("'Forensic Limit' Cannot Exceed or Equal to 'Policy Aggregate Limit of Liablity'!")    

 
    #----------------------------------------------------------------------------------------------#
    # Pricing 06: Legal Forensic Limit
    #----------------------------------------------------------------------------------------------#
    cyber_defense_limit = cyber_options_df["defense_penalties_limit"]
    cyber_defense_limit = cyber_defense_limit.fillna(0)
    cyber_defense_limit_usd = cyber_defense_limit * (ccy_usd_conversion)
    cyber_defense_limit_ratio = [0 if y==0 else (x/y) for (x,y) in zip(cyber_defense_limit_usd, cyber_policy_agg_limit_usd)]

    # for item in cyber_defense_limit_ratio:
    #     if item > 1:
    #         hx.errors.validation("'Regulatory Defense and Penalties Limit' Cannot Exceed 'Policy Aggregate Limit of Liablity'!")
    
    cyber_defence_limit_ratio_factor = np.interp(cyber_defense_limit_ratio, cyber_reg_defence_params["low"],cyber_reg_defence_params["default"] )
    #----------------------------------------------------------------------------------------------#
    # Pricing 07: Payment Card Limit
    #----------------------------------------------------------------------------------------------#
    cyber_payment_card_limit = cyber_options_df["payment_card_limit"]
    cyber_payment_card_limit = cyber_payment_card_limit.fillna(0)
    cyber_payment_card_limit_usd = cyber_payment_card_limit * (ccy_usd_conversion)

    cyber_payment_card_limit_ratio = [0 if y==0 else (x/y) for (x,y) in zip(cyber_payment_card_limit_usd, cyber_policy_agg_limit_usd)]
    cyber_payment_card_limit_factor = np.interp(cyber_payment_card_limit_ratio, cyber_payment_card_limit_params["answer_low"], cyber_payment_card_limit_params["credit"])
    
    # for item in cyber_payment_card_limit_ratio:
    #     if item > 1:
    #         hx.errors.validation("'Payment Card Liability and Cost Limit' Cannot Exceed 'Policy Aggregate Limit of Liablity'!")    

    #timer.end("payment_card_limit")
    #----------------------------------------------------------------------------------------------#
    # Pricing 08: Other Additional Coverage Load
    #----------------------------------------------------------------------------------------------#
    #timer.start("other_parts")
    cyber_electronic_load = cyber_deleted_coverage_params[cyber_deleted_coverage_params["delete_coverage_name"] == "Electronic Crime"]["factor"].iloc[0]
    cyber_tele_fraud_load = cyber_deleted_coverage_params[cyber_deleted_coverage_params["delete_coverage_name"] == "Telephone Fraud"]["factor"].iloc[0]
    cyber_fraud_instruct_load = cyber_deleted_coverage_params[cyber_deleted_coverage_params["delete_coverage_name"] == "Fraudlent Instruction"]["factor"].iloc[0]
    cyber_bi_pd_load = cyber_bi_pd_params[cyber_bi_pd_params["option"] == "Yes"]["debit"].iloc[0]

    #----------------------------------------------------------------------------------------------#
    # Pricing 08 - 02: Schedule Factors
    #----------------------------------------------------------------------------------------------#
    cyber_financial_condition_schedule = cds.modifiers.cyber.cyber_financial_condition.value
    cyber_maturity_of_business_schedule = cds.modifiers.cyber.cyber_maturity_of_business.value
    cyber_quality_of_management_schedule = cds.modifiers.cyber.cyber_quality_of_management.value
    cyber_volume_of_information_stored_schedule = cds.modifiers.cyber.cyber_volume_of_information_stored.value

    if cyber_financial_condition_schedule is None:
        cyber_financial_condition_schedule = 0.0
    if cyber_maturity_of_business_schedule is None:
        cyber_maturity_of_business_schedule = 0.0
    if cyber_quality_of_management_schedule is None:
        cyber_quality_of_management_schedule = 0.0
    if cyber_volume_of_information_stored_schedule is None:
        cyber_volume_of_information_stored_schedule = 0.0
    
    cyber_schedule_factor = cyber_financial_condition_schedule + cyber_maturity_of_business_schedule  + cyber_quality_of_management_schedule  + cyber_volume_of_information_stored_schedule
    schedule_total_min = cyber_constants_params[cyber_constants_params["factor_name"] == "Total Schedule Minimum"]["factor"].iloc[0]
    schedule_total_max = cyber_constants_params[cyber_constants_params["factor_name"] == "Total Schedule Maximum"]["factor"].iloc[0]
    cyber_schedule_factor = max(cyber_schedule_factor, schedule_total_min)
    cyber_schedule_factor = min(cyber_schedule_factor, schedule_total_max)

    #----------------------------------------------------------------------------------------------#
    # Pricing 09: Policy Term
    #----------------------------------------------------------------------------------------------#  
    inception_date = hxd.hx_core.inception_date
    expiry_date = hxd.hx_core.expiry_date
    year_on_expiry_date = date(inception_date.year + 1, inception_date.month, inception_date.day)
    term_factor = ((expiry_date-year_on_expiry_date).days+1)/365+1
    expiry_18_months = inception_date + relativedelta(months=18)

    if expiry_date < inception_date:
        hx.errors.validation("Expiry Date Cannot Before Inception Date!")
    if expiry_18_months < expiry_date:
        hx.errors.validation("Policy Length Cannot Exceed 18 Months!")
    
    #----------------------------------------------------------------------------------------------#
    # Pricing 10: Cyber Brokerage
    #----------------------------------------------------------------------------------------------#   

    cyber_brokerage = cyber_options_df["brokerage"]
    cyber_brokerage_new = cyber_brokerage.fillna(0.0)

    # for item in cyber_brokerage:
    #     if item is None:
    #         hx.errors.validation("Cyber: Brokerage Shoule be Entered!")
    
    #timer.end("other_parts")
    #----------------------------------------------------------------------------------------------#
    # Pricing 11: Excess Layers
    #----------------------------------------------------------------------------------------------# 
    #options_df = utils.pd_df_from_hx_list(cds.options)
    #timer.start("excess_inputs")
    options_dict = [{
    "per_claim_limit_1_excess": item.per_claim_limit_1_excess,
    "aggregate_limit_1_excess": item.aggregate_limit_1_excess,

    "per_claim_limit_2_excess": item.per_claim_limit_2_excess,
    "aggregate_limit_2_excess": item.aggregate_limit_2_excess,

    "per_claim_limit_3_excess": item.per_claim_limit_3_excess,
    "aggregate_limit_3_excess": item.aggregate_limit_3_excess,

    "per_claim_limit_4_excess": item.per_claim_limit_4_excess,
    "aggregate_limit_4_excess": item.aggregate_limit_4_excess,

    "per_claim_limit_5_excess": item.per_claim_limit_5_excess,
    "aggregate_limit_5_excess": item.aggregate_limit_5_excess,

    "per_claim_limit_6_excess": item.per_claim_limit_6_excess,
    "aggregate_limit_6_excess": item.aggregate_limit_6_excess,

    "per_claim_limit_7_excess": item.per_claim_limit_7_excess,
    "aggregate_limit_7_excess": item.aggregate_limit_7_excess,

    "per_claim_limit_8_excess": item.per_claim_limit_8_excess,
    "aggregate_limit_8_excess": item.aggregate_limit_8_excess,

    "per_claim_limit_9_excess": item.per_claim_limit_9_excess,
    "aggregate_limit_9_excess": item.aggregate_limit_9_excess,

    "per_claim_limit_10_excess": item.per_claim_limit_10_excess,
    "aggregate_limit_10_excess": item.aggregate_limit_10_excess,
    
    } for item in cds.options]
        
    layers_table = pd.DataFrame(options_dict)  
    # layers_table = options_df[["per_claim_limit_1_excess","aggregate_limit_1_excess",\
    # "per_claim_limit_2_excess","aggregate_limit_2_excess",\
    # "per_claim_limit_3_excess","aggregate_limit_3_excess",\
    # "per_claim_limit_4_excess","aggregate_limit_4_excess",\
    # "per_claim_limit_5_excess","aggregate_limit_5_excess",\
    # "per_claim_limit_6_excess","aggregate_limit_6_excess",\
    # "per_claim_limit_7_excess","aggregate_limit_7_excess",\
    # "per_claim_limit_8_excess","aggregate_limit_8_excess",\
    # "per_claim_limit_9_excess","aggregate_limit_9_excess",\
    # "per_claim_limit_10_excess","aggregate_limit_10_excess"]] 
    layers_table = layers_table.fillna(0) 
    #convert to USD
    layers_table_usd = layers_table * (ccy_usd_conversion)

    layers_agg_limit_df = pd.DataFrame()
    layers_detachment_df = pd.DataFrame({"agg_limit": cyber_policy_agg_limit_usd})
    layers_agg_limit_final = pd.DataFrame()
    #timer.end("excess_inputs")
    #timer.start("cyber_loop")
    #Loop the excess layers
    for index in range(1, max_layers+1):

        layers_df = layers_table_usd[[f"per_claim_limit_{index}_excess", f"aggregate_limit_{index}_excess"]]
        layers_df = layers_df.rename(columns = {f"per_claim_limit_{index}_excess": "eec_limit",f"aggregate_limit_{index}_excess": "agg_limit" })
        layers_detachment_temp = pd.DataFrame({"agg_limit": layers_df["agg_limit"]})
        layers_detachment_df["agg_limit"] = layers_detachment_df["agg_limit"] + layers_detachment_temp["agg_limit"] 

        layers_agg_limit_df[f"agg_limit_{index}_excess_detachment"] = np.interp(layers_detachment_df["agg_limit"], cyber_agg_limit_ilf_params["limit"], cyber_agg_limit_ilf_params["low"])
        if index == 1:
            layers_agg_limit_df[f"agg_limit_{index}_excess_final"] = layers_agg_limit_df[f"agg_limit_{index}_excess_detachment"] - agg_limit_ilf
        else:
            layers_agg_limit_df[f"agg_limit_{index}_excess_final"] = layers_agg_limit_df[f"agg_limit_{index}_excess_detachment"] - layers_agg_limit_df[f"agg_limit_{index-1}_excess_detachment"] 
        
        layers_agg_limit_final[f"agg_limit_{index}_excess_final"] = np.where(cyber_policy_agg_limit_usd > 0, layers_agg_limit_df[f"agg_limit_{index}_excess_final"], 0)
    
    #timer.end("cyber_loop")
    #----------------------------------------------------------------------------------------------#
    # Pricing 12: Final Premium - Primary Layer
    #----------------------------------------------------------------------------------------------# 
    #timer.start("final_prem_primary2")
    prem_list_temp = [cyber_base_premium_final_bbr, cyber_base_premium_final_infosec]
    
    # BBR Net Premium
    cyber_prem = np.array([prem_list_temp[0] for i in range(0,len(cyber_options_df))])
    cyber_prem = np.multiply(cyber_prem, cyber_notified_retention_ratio_factor)
    cyber_prem = np.multiply(cyber_prem, cyber_agg_retention_factor)
    #Sublimit factors
    cyber_sublimit_factor = cyber_forensic_limit_ratio_factor + cyber_payment_card_limit_factor + cyber_defence_limit_ratio_factor
    cyber_sublimit_factor = cyber_sublimit_factor + cyber_tele_fraud_load + cyber_electronic_load + cyber_fraud_instruct_load + cyber_bi_pd_load
    cyber_sublimit_prem = np.multiply(cyber_prem, cyber_sublimit_factor)
    #include the sublimit_factpr
    cyber_prem = cyber_prem + cyber_sublimit_prem
    cyber_prem = cyber_prem *(1+cyber_schedule_factor)
    cyber_prem = cyber_prem*(term_factor)
    cyber_premium_bbr_usd = cyber_prem

    #Infosec Net Premmium
    cyber_prem = np.array([prem_list_temp[1] for i in range(0,len(cyber_options_df))])
    cyber_prem = np.multiply(cyber_prem, cyber_agg_retention_factor)
    cyber_sublimit_factor = cyber_tele_fraud_load + cyber_electronic_load + cyber_fraud_instruct_load + cyber_bi_pd_load
    cyber_sublimit_prem = np.multiply(cyber_prem, cyber_sublimit_factor)
    #include the sublimit_factpr
    cyber_prem = cyber_prem + cyber_sublimit_prem
    cyber_prem = cyber_prem *(1+cyber_schedule_factor)
    cyber_prem = cyber_prem*(term_factor)
    cyber_premium_infosec_usd = cyber_prem

    # total final Net Premium
    if cyber_product == "BBR":
        cyber_net_prem_usd_term = cyber_premium_bbr_usd + cyber_premium_infosec_usd
    if cyber_product == "InfoSec":
        cyber_net_prem_usd_term = cyber_premium_infosec_usd
    
    cyber_min_prem_usd = cyber_constants_params[cyber_constants_params["factor_name"] == "Cyber Minimum Premium"]["factor"].iloc[0]
    
    cyber_min_prem_usd_list = np.array([cyber_min_prem_usd for i in range(0,len(cyber_options_df))])
    cyber_net_prem_usd_post_min = np.maximum(cyber_net_prem_usd_term, cyber_min_prem_usd_list)
    cyber_final_net_prem_usd = np.multiply(cyber_net_prem_usd_post_min , agg_limit_ilf)
    #Final Net Premium
    cyber_final_net_prem_usd = [round(x/100,1)*100 for x in cyber_final_net_prem_usd]        
    # cyber_brokerage_new = [0.25,0.25,0.25,0.25]

    # Cyber territory factor
    us_international = cds.rating_factors.us_international_choice_of_law.us_international
    cyber_territory_table = hx.params.table_cyber_territory_factor
    
    # Pull the territory factor  
    filtered_cyber_territory = cyber_territory_table[cyber_territory_table['Level'] == us_international]  
    if filtered_cyber_territory.shape[0]:
        cyber_territory_factor = filtered_cyber_territory['Factor'].iloc[0]
    else:
        cyber_territory_factor = 1

    # Final gross premium
    cyber_final_gross_prem_usd = [(x/(1-y)) * cyber_territory_factor for (x,y) in zip(cyber_final_net_prem_usd , cyber_brokerage_new)]
   

    cyber_final_gross_prem_1 = [x / ccy_usd_conversion for x in cyber_final_gross_prem_usd]
    cyber_final_gross_prem = [0 if y == 0 else x for (x,y) in zip(cyber_final_gross_prem_1, cyber_policy_agg_limit)]

    #timer.end("final_prem_primary2")

    #timer.start("export1")
    #export to hxd
    for index, item in enumerate(cds.cyber_options):
        setattr(item, "model_premium_third_party_usd", cyber_final_gross_prem_usd[index])
        setattr(item, "model_premium_third_party", cyber_final_gross_prem[index])
    #timer.end("export1")


    #----------------------------------------------------------------------------------------------#
    # Pricing 13: Final Premium - Excess Layers
    #----------------------------------------------------------------------------------------------# 

    # First and Third Party - sub calcs for excess cyber prem for First and Third Party (BBR entered) #IR edit.
    bbr_cyber_gross_prem = cyber_options_df["model_premium_bbr_rater"].fillna(0) 
    bbr_cyber_gross_prem = bbr_cyber_gross_prem / cyber_territory_factor
    bbr_cyber_net_prem = bbr_cyber_gross_prem * (1 - cyber_brokerage_new) 
    bbr_cyber_term_prem = bbr_cyber_net_prem / agg_limit_ilf 
    bbr_cyber_term_prem = np.array(bbr_cyber_term_prem, dtype=float)  # not sure what the best practice is for doing these calcssss
    bbr_cyber_net_prem_usd_post_min = np.maximum(bbr_cyber_term_prem, cyber_min_prem_usd_list)


    cyber_excess_net_prem_usd = pd.DataFrame()
    cyber_excess_gross_prem_usd = pd.DataFrame()
    cyber_excess_gross_prem = pd.DataFrame()
    brokerage_temp = np.array([1-x for x in cyber_brokerage_new])
    #timer.start("first_excess_loop")
    for index in range(1, max_layers+1):
        if cds.rating_factors.cyber.first_and_third_party_show == True: # IR edit
            cyber_net_prem_usd_post_min = bbr_cyber_net_prem_usd_post_min 
        cyber_excess_net_prem_usd[f"net_prem_{index}_excess_final"] = np.multiply(cyber_net_prem_usd_post_min, layers_agg_limit_final[f"agg_limit_{index}_excess_final"])
        cyber_excess_net_prem_usd[f"net_prem_{index}_excess_final"] = [round(x/100,1)*100 for x in cyber_excess_net_prem_usd[f"net_prem_{index}_excess_final"]]
        cyber_excess_gross_prem_usd[f"gross_prem_{index}_excess_final"] =  cyber_excess_net_prem_usd[f"net_prem_{index}_excess_final"].divide(brokerage_temp)
        cyber_excess_gross_prem[f"gross_prem_{index}_excess_final"] = (cyber_excess_gross_prem_usd[f"gross_prem_{index}_excess_final"] / ccy_usd_conversion) * cyber_territory_factor
    #timer.end("first_excess_loop")    
    #export to hxd 
    #timer.start("export_loop")   
    layers_list = ["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"]
    for index, layers in enumerate(layers_list):
        for index_2, item in enumerate(cds.cyber_options):
            setattr(item, f"model_premium_third_party_{layers}_usd",  cyber_excess_gross_prem_usd[f"gross_prem_{index+1}_excess_final"][index_2])
            setattr(item, f"model_premium_third_party_{layers}",  cyber_excess_gross_prem[f"gross_prem_{index+1}_excess_final"][index_2])
    #timer.end("export_loop")  
    #timer.start("second_export") 
    #export to hxd for limits
    for index,item in enumerate(cds.cyber_options):
        temp_val = cyber_agg_retention_df[index]
        if temp_val > 0:
            setattr(getattr(item,"data_network_retention" ), "calculated", temp_val)
            setattr(getattr(item,"defense_penalties_retention" ), "calculated", temp_val)
            setattr(getattr(item,"payment_card_retention" ), "calculated", temp_val)
    #timer.end("second_export")    
    #timer.start("bbr_prems") 
    # first part premium calc
    bbr_rater_prem = cyber_options_df["model_premium_bbr_rater"]
    # bbr_rater_prem = [15000, None, None, None]
    first_party_prem = []
    for index, item in enumerate(bbr_rater_prem):
        if item is not None:
            cyber_plfr_net = cyber_constants_params[cyber_constants_params["factor_name"] == "Cyber Priced To LR Net"]["factor"].iloc[0]
            cyber_first_party_proportion = cyber_constants_params[cyber_constants_params["factor_name"] == "BBR First Party Proportion"]["factor"].iloc[0]
            plfr_net = cyber_constants_params[cyber_constants_params["factor_name"] == "Priced to LR Net"]["factor"].iloc[0]
            first_party_prem.append(item * cyber_first_party_proportion * cyber_plfr_net / plfr_net)
    #timer.end("bbr_prems") 
    # fill nans with 0s
    #timer.start("next_larger_section")
    first_party_prem = pd.Series(first_party_prem, dtype=object).fillna(0).tolist()
    cyber_final_gross_prem = pd.Series(cyber_final_gross_prem, dtype=object).fillna(0).tolist()

    # if empty list - add numbers, otherwise errors out in the sum below
    if first_party_prem == []:
        first_party_prem = [0] * len(cds.options)
    
    if cyber_final_gross_prem == []:
        cyber_final_gross_prem = [0] * len(cds.options)
    #timer.end("next_larger_section")
    #timer.start("end_export")
    # save to CDS
    for index, item in enumerate(first_party_prem):
        if item > 0 :
            setattr(cds.cyber_options[index], "model_premium_first_party", item)
    
    # output the final premium - depends on whether first party and third party coverage is requested or just third party is required
    if cds.rating_factors.cyber.first_or_third_party == "First Party and Third Party":
        for index, item in enumerate(bbr_rater_prem):
            if item is not None and item > 0 :
                setattr(cds.cyber_options[index], "model_premium_final", bbr_rater_prem[index])
            else:
                setattr(cds.cyber_options[index], "model_premium_final", 0)
    else:
        for index, item in enumerate(cyber_final_gross_prem):
            if item is not None and item > 0:
                setattr(cds.cyber_options[index], "model_premium_final", cyber_final_gross_prem[index])
            else:
                setattr(cds.cyber_options[index], "model_premium_final", 0)


    for index, item in enumerate(cds.options):
        setattr(item, "cyber_premium_primary", getattr(cds.cyber_options[index],"model_premium_final"))

    #timer.end("end_export")
    pass