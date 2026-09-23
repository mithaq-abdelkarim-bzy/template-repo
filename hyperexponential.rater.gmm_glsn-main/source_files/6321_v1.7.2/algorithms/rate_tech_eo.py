import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
from operator import itemgetter
from datetime import date
from algorithms.rate_constants import max_layers


def eec_limit_calc(hxd, eec_limit_table, techeo_ilf_factors_params, revenue_ratio, limit_minimum):

    techeo_eec_limit_lower = []
    techeo_eec_limit_upper = []

    # SA: never loop through dataframes! You can use merge_asof to merge on a higher than
    # https://pandas.pydata.org/docs/reference/api/pandas.merge_asof.html
    eec_limit_table = eec_limit_table.reset_index().sort_values("eec_limit")
    eec_limit_table = pd.merge_asof(eec_limit_table, techeo_ilf_factors_params[["per_occurence_limit", "next_per_occurence_limit"]], left_on="eec_limit", right_on="per_occurence_limit").fillna(0)
    eec_limit_table = eec_limit_table.rename(columns={"per_occurence_limit": "limit_lower", "next_per_occurence_limit": "limit_upper"})
    eec_limit_table = eec_limit_table.sort_values("index").drop("index", axis=1)

    eec_limit_table["limit_ratio"] = [(x-y)/(z-y)  if z > 0 and z > y else 0 for (x, y, z) in zip(eec_limit_table["eec_limit"], eec_limit_table["limit_lower"], eec_limit_table["limit_upper"])]
    

    techeo = techeo_ilf_factors_params[["per_occurence_limit", "lower_ilf", "upper_ilf"]]
    eec_limit_table = eec_limit_table.merge(techeo, how='left', left_on="limit_lower", right_on="per_occurence_limit", suffixes=('', '_0'))

    eec_limit_table = eec_limit_table.merge(techeo, how='left', left_on="limit_upper", right_on="per_occurence_limit", suffixes=('', '_1'))


    eec_limit_table = eec_limit_table.drop(columns = [
        "per_occurence_limit", "per_occurence_limit_1", 
        ])
    eec_limit_table = eec_limit_table.rename(columns = {
        "lower_ilf": "limit_lower_ilf_lower", 
        "upper_ilf": "limit_upper_ilf_lower", 
        "lower_ilf_1": "limit_lower_ilf_upper", 
        "upper_ilf_1": "limit_upper_ilf_upper"
        })


    # SA: just do the fillna in one go
    eec_limit_table = eec_limit_table.fillna(1.0)


    # get the final relativity (and the weights)
    eec_limit_table["eec_limit_final_relativity"] = \
        eec_limit_table["limit_lower_ilf_lower"] * (1 - eec_limit_table["limit_ratio"]) * (1 - revenue_ratio) \
        + eec_limit_table["limit_lower_ilf_upper"] * (eec_limit_table["limit_ratio"]) * (1 - revenue_ratio) \
        + eec_limit_table["limit_upper_ilf_lower"] * (1 - eec_limit_table["limit_ratio"]) * (revenue_ratio) \
        + eec_limit_table["limit_upper_ilf_upper"] * (eec_limit_table["limit_ratio"]) * (revenue_ratio) 


    return eec_limit_table


def agg_limit_calc(hxd, agg_eec_limit_table,techeo_agg_limit_params):
    agg_eec_limit_table["agg_eec_ratio"] = np.where(agg_eec_limit_table["eec_limit"]> 0,agg_eec_limit_table["agg_limit"]/agg_eec_limit_table["eec_limit"], 0)
    agg_eec_limit_table["agg_eec_ratio_max"] = 5
    agg_eec_limit_table["agg_eec_ratio_after_max"] = agg_eec_limit_table[["agg_eec_ratio","agg_eec_ratio_max"]].min(axis = 1)
    agg_eec_limit_table["agg_eec_ratio_after_max"] = np.where(agg_eec_limit_table["agg_eec_ratio_after_max"]< 1, 1.0,agg_eec_limit_table["agg_eec_ratio_after_max"] )
    agg_eec_limit_table["agg_limit_relativity"] = np.interp(agg_eec_limit_table["agg_eec_ratio_after_max"], techeo_agg_limit_params["limit_ratio"], techeo_agg_limit_params["value_at_start"])

    return agg_eec_limit_table

def rate_tech_eo(hxd):
    cds = hxd.cds

    #----------------------------------------------------------------------------------------------#
    # parameter tables
    #----------------------------------------------------------------------------------------------#
    # FX rate for currency conversion - from user library
    fx_rates = params.fx_rates.df()
    ccy = cds.currencies.source_currency
    fx_rate = utils.look_up(ccy, 'ccy', 'fx_rate', fx_rates, if_not_found=1) # default to USD if error
    ccy_usd_conversion = 1 / fx_rate
    
    techeo_base_prem_params = hx.params.table_tech_eo_base_rate
    techeo_constants_params = hx.params.table_tech_eo_constants
    techeo_bi_pd_params = hx.params.table_tech_eo_contingent_bi_pd
    techeo_retention_params = hx.params.table_tech_eo_guideline_retention
    techeo_retention_ratio_params = hx.params.table_tech_eo_retention_ratio
    techeo_ilf_revenue_params = hx.params.table_tech_eo_ilf_revenue
    techeo_ilf_factors_params = hx.params.table_tech_eo_ilf_factors
    techeo_agg_limit_params = hx.params.table_tech_eo_agg_limit


    #Setting the Contingent Bodily Injury / Property Damage factor
    if cds.glsn_masking == True:
        contingent_bi_pd_selection = cds.rating_factors.tech_eo.contingent_bi_pd
        contingent_bi_pd = hx.params.table_tech_eo_contingent_bi_pd
        contingent_bi_pd_filtered = contingent_bi_pd[contingent_bi_pd["contingent_bi_pd"] == contingent_bi_pd_selection]
        contingent_bi_pd_asign = contingent_bi_pd_filtered["factor"].iloc[0]
        cds.rating_factors.tech_eo.contingent_bi_pd_factor = contingent_bi_pd_asign

    #----------------------------------------------------------------------------------------------#
    #step X: Set up tech eo table
    #----------------------------------------------------------------------------------------------#    
    tech_eo_params= hx.params.table_tech_eo
    tech_eo_name = tech_eo_params["industry_class_name"]

    tech_eo_revenue_percentage = []
    for item in tech_eo_name:
        tech_eo_revenue_percentage.append(getattr(getattr(cds.exposure.granular , item ),"tech_eo_percent_rateble_revenue"))
    tech_eo_revenue_percentage = pd.Series(tech_eo_revenue_percentage)

    # Create a pandas table
    tech_eo_df = pd.DataFrame({"industry_class_name": tech_eo_name, "tech_eo_revenue_percentage": tech_eo_revenue_percentage}) 
    tech_eo_df = tech_eo_df.merge(tech_eo_params,how = "left", left_on = "industry_class_name", right_on = "industry_class_name")

    rateable_revenue_pct = cds.exposure.aggregate.tech_eo_rateble_revenue 
    
    total_revenue = cds.exposure.aggregate.revenue

    if total_revenue <= 0:
        total_revenue = (-total_revenue)

    tech_eo_df["tech_eo_revenue"] = tech_eo_df["tech_eo_revenue_percentage"] * rateable_revenue_pct * total_revenue
    total_revenue_percentage = np.sum(tech_eo_df["tech_eo_revenue_percentage"])

    include_tech_eo = cds.rating_factors.pricing.tech_eo_products_media.include_primary or cds.rating_factors.pricing.well_tech_eo_media.include_primary

   
    if include_tech_eo and total_revenue_percentage == 0 :
        hx.errors.validation("Please complete Tech E&O sheet")
    elif include_tech_eo and total_revenue_percentage != 1 :
        hx.errors.validation("Total Tech E&O revenue allocated does not equal 100%")

    for item in  tech_eo_name:
        setattr(getattr(hxd.cds.exposure.granular , item ), "tech_eo_revenue", tech_eo_df[tech_eo_df["industry_class_name"] == item]["tech_eo_revenue"].iloc[0])
        setattr(getattr(hxd.cds.exposure.granular , item ),"tech_eo_class", tech_eo_df[tech_eo_df["industry_class_name"] == item]["class_group"].iloc[0])

    cds.exposure.aggregate.tech_eo_total_revenue = total_revenue_percentage

    #----------------------------------------------------------------------------------------------#
    #Pricing: 01. Base Premium
    #----------------------------------------------------------------------------------------------#    

    total_revenue_usd = total_revenue * ccy_usd_conversion
    rateable_revenue_usd = total_revenue_usd * rateable_revenue_pct
    tech_eo_df["tech_eo_revenue_usd"] = tech_eo_df["tech_eo_revenue"] * (ccy_usd_conversion)

    class_weight_df = pd.DataFrame(tech_eo_df.groupby(["class_group"])["tech_eo_revenue_percentage"].sum())
    class_weight_df = class_weight_df.reset_index()

    class_group_list = list(class_weight_df.index)
    class_group_list = [str(x+1)+"_lower" for x in class_group_list]

    techeo_base_premium = []
    revenue_list = techeo_base_prem_params["revenue"]

    for index, item in enumerate(class_group_list):
        base_prem = techeo_base_prem_params[item]
        techeo_base_premium.append(np.interp(rateable_revenue_usd, revenue_list, base_prem))
    
    base_prem_total = np.dot(np.array(techeo_base_premium), class_weight_df["tech_eo_revenue_percentage"])
    #net model assumed brokerage
    model_brokerage = techeo_constants_params[techeo_constants_params["factor_name"] == "model_brokerage"]["factor"].iloc[0]
    base_net_prem_total = base_prem_total*(1-model_brokerage )
    #convert to target LR premium
    pflr = techeo_constants_params[techeo_constants_params["factor_name"] == "model_net_priced_to_lr"]["factor"].iloc[0]
    target_lr =  techeo_constants_params[techeo_constants_params["factor_name"] == "model_target_lr"]["factor"].iloc[0]
    base_net_prem_target_total = base_net_prem_total*pflr/target_lr
    
    #load the contingent BI/PD - always yes in GMM but can be selected in GLSN
    if cds.gmm_masking : 
        include_bi_pd = "Yes"
    elif cds.glsn_masking :     
        include_bi_pd = cds.rating_factors.tech_eo.contingent_bi_pd
    bi_pd_load = techeo_bi_pd_params[techeo_bi_pd_params["contingent_bi_pd"] == include_bi_pd]["factor"].iloc[0]
    base_net_prem_final = base_net_prem_target_total*(1+bi_pd_load)


    #----------------------------------------------------------------------------------------------#
    #Pricing: 02. Retention USD
    #----------------------------------------------------------------------------------------------# 
    # 
    #  Get the options information ready 
    options_dict = [{
    "coverages.tech_eo_products_media.retention": item.coverages.tech_eo_products_media.retention,
    "coverages.tech_eo_products_media.per_claim_limit": item.coverages.tech_eo_products_media.per_claim_limit, 
    "coverages.tech_eo_products_media.aggregate_limit": item.coverages.tech_eo_products_media.aggregate_limit,

    "coverages.well_tech_eo_media.retention": item.coverages.well_tech_eo_media.retention,
    "coverages.well_tech_eo_media.per_claim_limit": item.coverages.well_tech_eo_media.per_claim_limit, 
    "coverages.well_tech_eo_media.aggregate_limit": item.coverages.well_tech_eo_media.aggregate_limit,

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
        
    options_df = pd.DataFrame(options_dict)
    #options_df = utils.pd_df_from_hx_list(cds.options)
    #select the tech eo information
    if cds.gmm_masking == True:
        tech_eo_df = options_df[["coverages.tech_eo_products_media.retention", "coverages.tech_eo_products_media.per_claim_limit", "coverages.tech_eo_products_media.aggregate_limit"]]
        tech_eo_df = tech_eo_df.rename(columns = {"coverages.tech_eo_products_media.retention": "retention",
    "coverages.tech_eo_products_media.per_claim_limit": "eec_limit", 
    "coverages.tech_eo_products_media.aggregate_limit": "agg_limit"})
    else:
        tech_eo_df = options_df[["coverages.well_tech_eo_media.retention", "coverages.well_tech_eo_media.per_claim_limit", "coverages.well_tech_eo_media.aggregate_limit"]]
        tech_eo_df = tech_eo_df.rename(columns = {"coverages.well_tech_eo_media.retention": "retention",
    "coverages.well_tech_eo_media.per_claim_limit": "eec_limit", 
    "coverages.well_tech_eo_media.aggregate_limit": "agg_limit"})

    tech_eo_df["retention"] = tech_eo_df["retention"].fillna(0)
    tech_eo_df["eec_limit"] = tech_eo_df["eec_limit"].fillna(0)
    tech_eo_df["agg_limit"] = tech_eo_df["agg_limit"].fillna(0)

    #convert all the retention, eec_limit and agg_limit to USD
    tech_eo_df["retention"]  = tech_eo_df["retention"] * ccy_usd_conversion
    tech_eo_df["eec_limit"]  = tech_eo_df["eec_limit"] * ccy_usd_conversion
    tech_eo_df["agg_limit"]  = tech_eo_df["agg_limit"] * ccy_usd_conversion


    # guideline Retention
    retention_filter = techeo_retention_params[techeo_retention_params["revenue_low"] <= total_revenue_usd].iloc[-1]
    retention_guideline_slope = retention_filter["slope"]
    retention_guideline_intercept = retention_filter["intercept"]
    retention_guideline = retention_guideline_slope*total_revenue_usd + retention_guideline_intercept

    # ratio to guideline retention
    tech_eo_retention_df = pd.DataFrame({"retention": tech_eo_df["retention"]})
    tech_eo_retention_df["retention_ratio"] = tech_eo_df["retention"].divide(retention_guideline)
    tech_eo_retention_df["retention_ratio_max"] = 5
    tech_eo_retention_df["retention_ratio_final"] = tech_eo_retention_df[["retention_ratio","retention_ratio_max"]].min(axis = 1)
    tech_eo_retention_df["retention_ratio_factor"] = np.interp(tech_eo_retention_df["retention_ratio_final"], techeo_retention_ratio_params["lower"], techeo_retention_ratio_params["factor"])
    # if ratio < 0.1, then 1.4 factor
    tech_eo_retention_df["retention_ratio_factor_small"] = np.where(tech_eo_retention_df["retention_ratio_final"] < 0.1, 1.4,tech_eo_retention_df["retention_ratio_factor"] )
    # ! here is the final retention factors!
    tech_eo_retention_df["retention_ratio_factor_final"] = tech_eo_retention_df[["retention_ratio_factor", "retention_ratio_factor_small"]].max(axis = 1)


    #----------------------------------------------------------------------------------------------#
    #Pricing: 02. Primary layer: EEC  limit USD
    #----------------------------------------------------------------------------------------------# 
    
    # revenue ratio - look up for limit ILF table
    revenue_filtered_df = techeo_ilf_revenue_params[techeo_ilf_revenue_params["revenue_lower"] <= total_revenue_usd]
    revenue_lower = revenue_filtered_df["revenue_lower"].iloc[-1]
    revenue_upper = revenue_filtered_df["revenue_upper"].iloc[-1]
    revenue_ratio = (total_revenue_usd - revenue_lower)/(revenue_upper - revenue_lower)
    revenue_lower_column = int(revenue_filtered_df["column_lower"].iloc[-1])
    revenue_upper_column = int(revenue_filtered_df["column_upper"].iloc[-1])
    lower_col_name = techeo_ilf_factors_params.columns[revenue_lower_column-1]
    upper_col_name = techeo_ilf_factors_params.columns[revenue_upper_column-1]


    #create a EEC limit table
    tech_eo_eec_limit_df = pd.DataFrame(tech_eo_df["eec_limit"])

    techeo_ilf_factors_params_min = techeo_ilf_factors_params["per_occurence_limit"].min()
    techeo_ilf_factors = techeo_ilf_factors_params[["per_occurence_limit", "next_per_occurence_limit", lower_col_name, upper_col_name]]
    techeo_ilf_factors.columns = ["per_occurence_limit", "next_per_occurence_limit", "lower_ilf", "upper_ilf"]

    tech_eo_eec_limit_df_02 = pd.DataFrame()
    tech_eo_eec_limit_df_02 = eec_limit_calc(hxd,tech_eo_eec_limit_df,techeo_ilf_factors, revenue_ratio, techeo_ilf_factors_params_min)


    #----------------------------------------------------------------------------------------------#
    #Pricing: 03. Primary layer: Agg limit USD
    #----------------------------------------------------------------------------------------------# 
    tech_eo_agg_limit_df = pd.DataFrame({"eec_limit":tech_eo_df["eec_limit"], "agg_limit":tech_eo_df["agg_limit"]})
    tech_eo_agg_limit_df_02 = pd.DataFrame()
    tech_eo_agg_limit_df_02 = agg_limit_calc(hxd, tech_eo_agg_limit_df,techeo_agg_limit_params)

    tech_eo_agg_limit_df_02["tech_eo_agg_ilf_primary_factor"] = tech_eo_agg_limit_df_02["agg_limit_relativity"]
    utils.write_pd_to_hxd(tech_eo_agg_limit_df_02, cds.options, ["tech_eo_agg_ilf_primary_factor"])
    
    #----------------------------------------------------------------------------------------------#
    #Pricing: 04. Excess layer EEC and AGG limit
    #----------------------------------------------------------------------------------------------#  

    layers_table = options_df[["per_claim_limit_1_excess","aggregate_limit_1_excess",\
    "per_claim_limit_2_excess","aggregate_limit_2_excess",\
    "per_claim_limit_3_excess","aggregate_limit_3_excess",\
    "per_claim_limit_4_excess","aggregate_limit_4_excess",\
    "per_claim_limit_5_excess","aggregate_limit_5_excess",\
    "per_claim_limit_6_excess","aggregate_limit_6_excess",\
    "per_claim_limit_7_excess","aggregate_limit_7_excess",\
    "per_claim_limit_8_excess","aggregate_limit_8_excess",\
    "per_claim_limit_9_excess","aggregate_limit_9_excess",\
    "per_claim_limit_10_excess","aggregate_limit_10_excess"]] 
    layers_table = layers_table.fillna(0) 
    #convert to USD
    layers_table_usd = layers_table * (ccy_usd_conversion)

    # Loop for the 10 excess layer
    layer_eec_limit_final = pd.DataFrame()
    layer_agg_limit_final = pd.DataFrame()

    layer_detachment_df = pd.DataFrame({"eec_limit": tech_eo_df["eec_limit"]})

    for index in range(1,11):
        #eec limit
        layer_df = layers_table_usd[[f"per_claim_limit_{index}_excess",f"aggregate_limit_{index}_excess"]]
        layer_df = layer_df.rename(columns = {f"per_claim_limit_{index}_excess": "eec_limit", f"aggregate_limit_{index}_excess": "agg_limit" })
        layer_detachment_temp = pd.DataFrame({"eec_limit": layer_df["eec_limit"]})
        layer_detachment_df["eec_limit"] = layer_detachment_df["eec_limit"] + layer_detachment_temp["eec_limit"]

        layer_eec_limit_df = pd.DataFrame()
        layer_eec_limit_df = eec_limit_calc(hxd, layer_detachment_df, techeo_ilf_factors, revenue_ratio, techeo_ilf_factors_params_min)
        layer_eec_limit_final[f"eec_limit_{index}_excess_final"] = np.where(layer_df["eec_limit"]>0, (layer_eec_limit_df["eec_limit_final_relativity"]-tech_eo_eec_limit_df_02["eec_limit_final_relativity"]).divide(tech_eo_eec_limit_df_02["eec_limit_final_relativity"]),0)
        
        # aggregate limit
        layer_df_org = pd.DataFrame({"eec_limit": layer_df["eec_limit"], "agg_limit": layer_df["agg_limit"]})
        layer_agg_limit_df = pd.DataFrame()
        layer_agg_limit_df = agg_limit_calc(hxd, layer_df_org  ,techeo_agg_limit_params)
        layer_agg_limit_final[f"agg_limit_{index}_excess_final"] = layer_agg_limit_df["agg_limit_relativity"]
    

    #----------------------------------------------------------------------------------------------#
    #Pricing: 05. Net and Gross Tech E&O Premium before chedule Rating Factors and Retro factor and Term adjustment
    #----------------------------------------------------------------------------------------------#  

    #-------------------------------------------------------
    # Primary layer
    #-------------------------------------------------------
    # inception_date = hxd.hx_core.inception_date
    # expiry_date = hxd.hx_core.expiry_date
    # year_on_expiry_date = date(inception_date.year + 1, inception_date.month, inception_date.day)
    # term_factor = 1.083333333

    if cds.gmm_masking == True:
        techeo_net_base_prem_usd = [base_net_prem_final for x in range(0,tech_eo_df.shape[0])]
        techeo_net_base_prem_usd = [0 if y == 0 else x for (x,y) in  zip(techeo_net_base_prem_usd,tech_eo_df["eec_limit"]) ]
        techeo_net_prem_final_usd = np.multiply(techeo_net_base_prem_usd ,tech_eo_retention_df["retention_ratio_factor_final"])
        techeo_net_prem_final_usd = np.multiply(techeo_net_prem_final_usd,tech_eo_eec_limit_df_02["eec_limit_final_relativity"])
        techeo_net_prem_final_usd = np.multiply(techeo_net_prem_final_usd,tech_eo_agg_limit_df_02["agg_limit_relativity"])    
    else:
        techeo_net_base_prem_usd = [base_net_prem_final for x in range(0,tech_eo_df.shape[0])]
        techeo_net_base_prem_usd = [0 if y == 0 else x for (x,y) in  zip(techeo_net_base_prem_usd,tech_eo_df["eec_limit"]) ]
        # techeo_net_prem_final_usd = np.multiply(techeo_net_base_prem_usd ,tech_eo_retention_df["retention_ratio_factor_final"])
        techeo_net_prem_final_usd = np.multiply(techeo_net_base_prem_usd,tech_eo_eec_limit_df_02["eec_limit_final_relativity"])
        techeo_net_prem_final_usd = np.multiply(techeo_net_prem_final_usd,tech_eo_agg_limit_df_02["agg_limit_relativity"])    


    for index, item in enumerate(cds.options):
        setattr(item, "tech_eo_primary_net_premium_usd",techeo_net_prem_final_usd[index])
    
    cds.tech_eo_base_net_premium_usd = base_net_prem_final
    
    for index, item in enumerate(cds.options):
        setattr(item, "tech_eo_retention_ratio_factor", tech_eo_retention_df["retention_ratio_factor_final"].iloc[0]) 

    for index, item in enumerate(cds.options):
        setattr(item, "tech_eo_eec_ilf", tech_eo_eec_limit_df_02["eec_limit_final_relativity"].iloc[0]) 

    #for index, item in enumerate(cds.options):
    #    setattr(item, "tech_eo_agg_ilf", tech_eo_agg_limit_df_02["agg_limit_relativity"].iloc[0]) 

    #-------------------------------------------------------
    # Excess Layer
    #-------------------------------------------------------
    techeo_layer_ilf_final = pd.DataFrame()
    ilf_agg_temp = pd.DataFrame({"ilf_agg_temp": tech_eo_agg_limit_df_02["agg_limit_relativity"]})


    for index in range(1, max_layers+1):
        techeo_layer_ilf_final[f"unlimited_ilf_{index}_excess"] = layer_eec_limit_final[f"eec_limit_{index}_excess_final"]
        techeo_layer_ilf_final[f"agg_ilf_{index}_excess"] = layer_agg_limit_final[f"agg_limit_{index}_excess_final"].divide(ilf_agg_temp["ilf_agg_temp"] )
        techeo_layer_ilf_final[f"agg_ilf_{index}_excess"] = techeo_layer_ilf_final[f"agg_ilf_{index}_excess"].multiply(techeo_layer_ilf_final[f"unlimited_ilf_{index}_excess"] )
        ilf_agg_temp["ilf_agg_temp"] = ilf_agg_temp["ilf_agg_temp"].multiply(layer_agg_limit_final[f"agg_limit_{index}_excess_final"])

    techeo_layer_net_premium_final_usd = pd.DataFrame()

    for index in range(1, max_layers+1):
        techeo_layer_net_premium_final_usd[f"net_premium_{index}_excess_usd"] = np.multiply(np.array(techeo_net_base_prem_usd), techeo_layer_ilf_final[f"agg_ilf_{index}_excess"])

    layers_list = ["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"]
    for index, layers in enumerate(layers_list):
        for index_2, item in enumerate(cds.options):
            setattr(item, f"tech_eo_net_premium_usd_{layers}",  techeo_layer_net_premium_final_usd[f"net_premium_{index+1}_excess_usd"][index_2])

    pass



    


    














     






    





