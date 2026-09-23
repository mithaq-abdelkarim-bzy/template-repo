import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
from algorithms.rate_constants import max_options
from operator import itemgetter

def rate_umbrella(hxd):
    cds = hxd.cds

    #----------------------------------------------------------------------------------------------#
    #step 1: Set show and hide for each umbrella option - based on the numnber of options added in the pricing sheet
    #----------------------------------------------------------------------------------------------#
    for umbrella_option in range(1,max_options+1):
        if len(cds.options) >= umbrella_option:
            setattr(cds,f"show_option_{umbrella_option}",True)

    #----------------------------------------------------------------------------------------------#
    #Import the parameter tables
    #----------------------------------------------------------------------------------------------#    

    gmm_umbrella_name = hx.params.table_gmm_umbrella["umbrella_name"]
    gmm_umbrella_curve = hx.params.table_umbrella_gmm_curves
    glsn_umbrella_name = hx.params.table_glsn_umbrella["umbrella_name"]
    glsn_umbrella_curve = hx.params.table_umbrella_glsn_curves

    # FX rate for currency conversion - from user library
    fx_rates = params.fx_rates.df()
    ccy = cds.currencies.source_currency
    fx_rate = utils.look_up(ccy, 'ccy', 'fx_rate', fx_rates, if_not_found=1) # default to USD if error
    ccy_usd_conversion = 1 / fx_rate


    # utils.lev(5000000,13.36, 1.04) -- 1019221.06
    # utils.layer_lev(5000000,2000000,13.36,1.04) -- 31792.25
    # utils.layer_lev(5000000,1000000,13.36,1.04) -- 19077.22

    #----------------------------------------------------------------------------------------------#
    # GMM Umbrella Calculation
    #----------------------------------------------------------------------------------------------#   

    #options_df = utils.pd_df_from_hx_list(cds.options)
    options_dict = [{
        "per_claim_limit_1_excess": item.per_claim_limit_1_excess,
        "per_claim_limit_2_excess": item.per_claim_limit_2_excess,
        "per_claim_limit_3_excess": item.per_claim_limit_3_excess,
        "per_claim_limit_4_excess": item.per_claim_limit_4_excess,
        "per_claim_limit_5_excess": item.per_claim_limit_5_excess,
        "per_claim_limit_6_excess": item.per_claim_limit_6_excess,
        "per_claim_limit_7_excess": item.per_claim_limit_7_excess,
        "per_claim_limit_8_excess": item.per_claim_limit_8_excess,
        "per_claim_limit_9_excess": item.per_claim_limit_9_excess,
        "per_claim_limit_10_excess": item.per_claim_limit_10_excess,

        "gmm_general_liability.premium_1_excess": item.gmm_general_liability.premium_1_excess,
        "gmm_general_liability.premium_2_excess": item.gmm_general_liability.premium_2_excess,
        "gmm_general_liability.premium_3_excess": item.gmm_general_liability.premium_3_excess,
        "gmm_general_liability.premium_4_excess": item.gmm_general_liability.premium_4_excess,
        "gmm_general_liability.premium_5_excess": item.gmm_general_liability.premium_5_excess,
        "gmm_general_liability.premium_6_excess": item.gmm_general_liability.premium_6_excess,
        "gmm_general_liability.premium_7_excess": item.gmm_general_liability.premium_7_excess,
        "gmm_general_liability.premium_8_excess": item.gmm_general_liability.premium_8_excess,
        "gmm_general_liability.premium_9_excess": item.gmm_general_liability.premium_9_excess,
        "gmm_general_liability.premium_10_excess": item.gmm_general_liability.premium_10_excess,

        "glsn_general_liability.premium_1_excess": item.glsn_general_liability.premium_1_excess,
        "glsn_general_liability.premium_2_excess": item.glsn_general_liability.premium_2_excess,
        "glsn_general_liability.premium_3_excess": item.glsn_general_liability.premium_3_excess,
        "glsn_general_liability.premium_4_excess": item.glsn_general_liability.premium_4_excess,
        "glsn_general_liability.premium_5_excess": item.glsn_general_liability.premium_5_excess,
        "glsn_general_liability.premium_6_excess": item.glsn_general_liability.premium_6_excess,
        "glsn_general_liability.premium_7_excess": item.glsn_general_liability.premium_7_excess,
        "glsn_general_liability.premium_8_excess": item.glsn_general_liability.premium_8_excess,
        "glsn_general_liability.premium_9_excess": item.glsn_general_liability.premium_9_excess,
        "glsn_general_liability.premium_10_excess": item.glsn_general_liability.premium_10_excess,
        
        } for item in cds.options]
        
    options_df = pd.DataFrame(options_dict) 


    gmm_cover_selection = cds.gmm_masking
    glsn_cover_selection = cds.glsn_masking

    

    #Each and Every Limit 
    umbrella_eel = pd.DataFrame()
    for layer in range(1,11):
        umbrella_eel[f"eel_{layer}_excess"] = options_df[f"per_claim_limit_{layer}_excess"].fillna(0) 

    # export to the main hxd
    for layer in range(1,11):
        for index, item in enumerate(cds.options):
            setattr(getattr(item, "umbrella_eel"), f"premium_{layer}_excess", (umbrella_eel.iloc[index, layer-1] * ccy_usd_conversion))
       

    #Import the structure
    if gmm_cover_selection:
        umbrella_df = pd.DataFrame({"umbrella_name": gmm_umbrella_name})
    if glsn_cover_selection:
        umbrella_df = pd.DataFrame({"umbrella_name": glsn_umbrella_name})

    underlying_ee_temp = []
    underlying_agg_temp = []
    underlying_prem_temp = []
    occurrence_temp = []

    if gmm_cover_selection:
        umbrella_name_list = gmm_umbrella_name
        rating_factors_umbrella = cds.rating_factors.gmm.umbrella
    if glsn_cover_selection:
        umbrella_name_list = glsn_umbrella_name
        rating_factors_umbrella = cds.rating_factors.glsn.umbrella

    for index, item in enumerate(umbrella_name_list):
        underlying_ee_temp.append(getattr(getattr(rating_factors_umbrella, item),"underlying_ee"))
        underlying_agg_temp.append(getattr(getattr(rating_factors_umbrella, item),"underlying_agg"))
        underlying_prem_temp.append(getattr(getattr(rating_factors_umbrella, item),"underlying_premium"))
        occurrence_temp.append(getattr(getattr(rating_factors_umbrella, item),"occurrence_cover"))
    
    umbrella_df["underlying_ee_limit"] = underlying_ee_temp
    umbrella_df["underlying_agg_limit"] = underlying_agg_temp
    umbrella_df["underlying_prem"] = underlying_prem_temp
    umbrella_df["underlying_occurence"] = occurrence_temp 

   
    umbrella_df["underlying_ee_limit"] = umbrella_df["underlying_ee_limit"].fillna(0)
    umbrella_df["underlying_agg_limit"]  = umbrella_df["underlying_agg_limit"].fillna(0)
    umbrella_df["underlying_prem"] = umbrella_df["underlying_prem"].fillna(0)

    umbrella_df["underlying_ee_limit_usd"] = umbrella_df["underlying_ee_limit"] * ccy_usd_conversion
    umbrella_df["underlying_agg_limit_usd"]  = umbrella_df["underlying_agg_limit"] * ccy_usd_conversion



    #merge the lognormal curves
    if gmm_cover_selection:
        umbrella_curve = gmm_umbrella_curve
    if glsn_cover_selection:
        umbrella_curve = glsn_umbrella_curve
    
    umbrella_df = umbrella_df.merge(umbrella_curve, how = "left", left_on = "umbrella_name", right_on = "umbrella_name" )
    
    umbrella_eel = umbrella_eel.fillna(0)
    umbrella_eel_usd = umbrella_eel * ccy_usd_conversion
    for layer in range(1,11):
        if layer == 1:
            umbrella_eel_usd[f"eel_{layer}_excess_cumulative"] = umbrella_eel_usd[f"eel_{layer}_excess"]
        else:
            umbrella_eel_usd[f"eel_{layer}_excess_cumulative"]  = umbrella_eel_usd[f"eel_{layer-1}_excess_cumulative"] + umbrella_eel_usd[f"eel_{layer}_excess"]

    
    # gmm_umbrella_df_factor = pd.DataFrame({"umbrella_name":gmm_umbrella_df["gmm_umbrella_name"] })
    umbrella_df["primary_premium"] = umbrella_df["underlying_prem"]  
    

    # filter table only with limit > 0  
    filtered_umbrella_df = umbrella_df[umbrella_df["underlying_ee_limit_usd"] > 0].copy()
    filtered_umbrella_df["primary_lev"] = utils.lev_col(filtered_umbrella_df["underlying_ee_limit_usd"],filtered_umbrella_df["mu"], filtered_umbrella_df["sigma"] )

    for option_index, option in enumerate(cds.options):
        for layer_index in range(1,11):
            if layer_index == 1:
                filtered_umbrella_df[f"lev_option_{option_index+1}_excess_{layer_index}"] = utils.layer_lev_col(
                    filtered_umbrella_df["underlying_ee_limit_usd"], 
                    umbrella_eel_usd.loc[option_index, f"eel_{layer_index}_excess"], 
                    filtered_umbrella_df["mu"], 
                    filtered_umbrella_df["sigma"]
                )
            else:
                filtered_umbrella_df[f"lev_option_{option_index+1}_excess_{layer_index}"] = utils.layer_lev_col(
                    filtered_umbrella_df["underlying_ee_limit_usd"] + umbrella_eel_usd.loc[option_index, f"eel_{layer_index-1}_excess_cumulative"], 
                    umbrella_eel_usd.loc[option_index, f"eel_{layer_index}_excess"], 
                    filtered_umbrella_df["mu"], 
                    filtered_umbrella_df["sigma"]
                )
            filtered_umbrella_df[f"premium_option_{option_index+1}_excess_{layer_index}"] = filtered_umbrella_df["primary_premium"] * filtered_umbrella_df[f"lev_option_{option_index+1}_excess_{layer_index}"]  / filtered_umbrella_df["primary_lev"] 


    # calculate unsupported net premium
    filter_col = [col for col in filtered_umbrella_df if col.startswith('premium_option')]
    unsupported_net_prem= filtered_umbrella_df[filtered_umbrella_df["umbrella_name"]!= "general_liability"][filter_col].sum()
    net_prem_occurence = filtered_umbrella_df[filtered_umbrella_df["underlying_occurence"] == True][filter_col].sum()
    
    gl_selection = cds.rating_factors.pricing.general_liability.include_primary
    gl_premium = []
    if gl_selection:
        if gmm_cover_selection:
            gl_cover_name = "gmm_general_liability"
        if glsn_cover_selection:
            gl_cover_name = "glsn_general_liability"
        for option_index in range(0, options_df.shape[0]):
            for layer_index in range(1,11):
                gl_premium.append(options_df[f"{gl_cover_name}.premium_{layer_index}_excess"][option_index])
        gl_premium = [0 if x is None else x for x in gl_premium]
    
    #!!Need to include the GL premium from Primary and Excess Layers
   
    if gl_selection:
        total_excess_net_prem = unsupported_net_prem + gl_premium
    else: 
        total_excess_net_prem = unsupported_net_prem.copy()

    gl_occurence_selection = umbrella_df[umbrella_df["umbrella_name"] == "general_liability"]["underlying_occurence"].iloc[0]

    occurence_num = filtered_umbrella_df["underlying_occurence"].sum() + gl_occurence_selection
    munich_cession_prem = pd.DataFrame({"unsupported_net_prem_occurrence": net_prem_occurence, "min_prem": 5000 / ccy_usd_conversion})

    if gl_selection:
        munich_cession_prem["general_liability_net_prem"] = gl_premium
    else:
        munich_cession_prem["general_liability_net_prem"] = 0

    # Need to add the GL premium in
    if occurence_num == 0:
        munich_cession_prem["munich_cession_net_prem"] = 0
    elif filtered_umbrella_df["underlying_occurence"].sum() == 0 and gl_occurence_selection is not False:
        munich_cession_prem["munich_cession_net_prem"] = np.maximum(munich_cession_prem["unsupported_net_prem_occurrence"]+ munich_cession_prem["general_liability_net_prem"], munich_cession_prem["min_prem"])
    elif gl_selection :
        munich_cession_prem["munich_cession_net_prem"] =np.where( munich_cession_prem["unsupported_net_prem_occurrence"] == 0, 0.0, np.maximum(munich_cession_prem["unsupported_net_prem_occurrence"]+ gl_premium, munich_cession_prem["min_prem"])) 
    else:
        munich_cession_prem["munich_cession_net_prem"] =np.where( munich_cession_prem["unsupported_net_prem_occurrence"] == 0, 0.0, np.maximum(munich_cession_prem["unsupported_net_prem_occurrence"],munich_cession_prem["min_prem"]))


    # !!Need to add in the GL

    brokerage_excess = []
    for option_index, option_item in enumerate(cds.options):
        for layer_index in range(1,11):
            brokerage_excess.append(getattr(option_item, f"brokerage_{layer_index}_excess"))
    
    #brokerage_excess = pd.Series(brokerage_excess).fillna(0)

    munich_cession_prem["brokerage"] = brokerage_excess
    munich_cession_prem["munich_cession_gross_prem"] = munich_cession_prem["munich_cession_net_prem"]  / (1 - munich_cession_prem["brokerage"])

    munich_cession_prem["general_liability_net_prem_pct"] = np.where(munich_cession_prem["munich_cession_net_prem"] == 0, 0, (munich_cession_prem["general_liability_net_prem"]*gl_occurence_selection)/(munich_cession_prem["unsupported_net_prem_occurrence"]+ munich_cession_prem["general_liability_net_prem"] )) 
    munich_cession_prem = munich_cession_prem.fillna(0)
    
    #output the unsupported net premium
    for option_index, option_item in enumerate(cds.options):
        for layer_index in range(1,11):
            setattr(getattr(option_item, "umbrella_unsupported_net_premium"), f"premium_{layer_index}_excess",unsupported_net_prem[f"premium_option_{option_index+1}_excess_{layer_index}"] )
            setattr(getattr(option_item, "umbrella_total_excess_net_premium"), f"premium_{layer_index}_excess",total_excess_net_prem[f"premium_option_{option_index+1}_excess_{layer_index}"] )
            setattr(getattr(option_item, "umbrella_munich_cession_net"), f"premium_{layer_index}_excess",munich_cession_prem["munich_cession_net_prem"][f"premium_option_{option_index+1}_excess_{layer_index}"] )
            setattr(getattr(option_item, "umbrella_munich_cession_gross"), f"premium_{layer_index}_excess",munich_cession_prem["munich_cession_gross_prem"][f"premium_option_{option_index+1}_excess_{layer_index}"]  )

    
    # output the individual coverage's option and layer premim

    umbrella_prem_df = pd.DataFrame({"umbrella_name": umbrella_df["umbrella_name"]})
    umbrella_prem_df = umbrella_df.merge(filtered_umbrella_df, how = "left", on = "umbrella_name")
    umbrella_prem_df = umbrella_prem_df.fillna(0)


    for option_index, option_item in enumerate(cds.options):
        for layer_index in range(1,11):
            temp_sum = munich_cession_prem["unsupported_net_prem_occurrence"][f"premium_option_{option_index+1}_excess_{layer_index}"] + munich_cession_prem["general_liability_net_prem"][f"premium_option_{option_index+1}_excess_{layer_index}"] 
            if temp_sum > 0:
                umbrella_prem_df[f"premium_pct_option_{option_index+1}_excess_{layer_index}"] = (umbrella_prem_df[f"premium_option_{option_index+1}_excess_{layer_index}"].multiply(umbrella_prem_df["underlying_occurence_x"]) )/ temp_sum
            else:
                umbrella_prem_df[f"premium_pct_option_{option_index+1}_excess_{layer_index}"] = 0


    #Output
    if gmm_cover_selection: 
        umbrella_name_new = ["gmm_"+ x for x in umbrella_df["umbrella_name"]]
    if glsn_cover_selection:
        umbrella_name_new = ["glsn_"+ x for x in umbrella_df["umbrella_name"]]
        
    for cover_index, cover_item in enumerate(umbrella_name_new):
        for option_index, option_item in enumerate(cds.options):
            for layer_index in range(1,11):  
                if (cover_item != "gmm_general_liability") and (cover_item != "glsn_general_liability"):
                    setattr(getattr(option_item, cover_item), f"premium_{layer_index}_excess",umbrella_prem_df[f"premium_option_{option_index+1}_excess_{layer_index}"].iloc[cover_index]  )
                    setattr(getattr(option_item, cover_item), f"cession_premium_split_{layer_index}_excess",umbrella_prem_df[f"premium_pct_option_{option_index+1}_excess_{layer_index}"].iloc[cover_index]  )
                elif (cover_item == "gmm_general_liability") | (cover_item == "glsn_general_liability"):
                    setattr(getattr(option_item, cover_item), f"cession_premium_split_{layer_index}_excess",munich_cession_prem["general_liability_net_prem_pct"][f"premium_option_{option_index+1}_excess_{layer_index}"] )
                
                    
    
    for cover_index, cover_item in enumerate(umbrella_name_new):
        if cover_item != "gmm_general_liability" and cover_item != "glsn_general_liability":
            for option_index, option_item in enumerate(cds.options):
                setattr(getattr(option_item, cover_item),f"premium_primary",umbrella_df["primary_premium"].iloc[cover_index])
        

   
    pass



