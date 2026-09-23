######################################################################################
# This is the pricing code for Media Tech
######################################################################################
import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
#from algorithms.rate_constants import eo_reinstatement_factor, eo_fees_scale, eo_territory_scale
from operator import itemgetter
import datetime




def rate_pricing_mediatech(hxd):

    # get the conversion rate from ccy to usd
    #xe_table = params.fx_rates.df()
    xe_table = hx.params.table_fx_rates
    ccy_usd_conversion =xe_table[xe_table["ccy"] == hxd.cds.currencies.source_currency]["fx_rate"].iloc[0]/ xe_table[xe_table["ccy"] == "USD"]["fx_rate"].iloc[0]


    # get the paramter tables
    territory_params = hx.params.table_eo_territory 
    industry_list = hx.params.table_mediatech_industry["industry_name"] 
    industry_params = hx.params.table_mediatech_industry 
    minimum_premium_params = hx.params.table_mediatech_minimum_premium
    base_rate_params = hx.params.table_mediatech_base_rate
    bipd_params = hx.params.table_mediatech_bi_pd_cover
    retroactive_params = hx.params.table_mediatech_prior_acts_years
    longevity_params = hx.params.table_mediatech_longevity
    claim_experience_params = hx.params.table_mediatech_claim_experience
    cost_included_params = hx.params.table_mediatech_cost_included
    schedule_params = hx.params.table_mediatech_schedule
    ilf_rows_params = hx.params.table_mediatech_ilf_rows
    eec_limit_params = hx.params.table_mediatech_eec_limit
    agg_limit_params = hx.params.table_mediatech_agg_limit
    guideline_deductible_params = hx.params.table_mediatech_guidline_deductible
    deductible_params = hx.params.table_mediatech_deductible
    additional_defense_params = hx.params.table_mediatech_additional_defense
    constants_params = hx.params.table_constants
    tp_params = hx.params.table_tp_parameters
    nmp_load = tp_params[tp_params["business_plan_class"] =="International Specialty Programmes" ]["nmp_load"].iloc[0]






    #################################################################################
    # Step 1: Get territory factor
    #################################################################################
    if hxd.cds.rating_factors.mediatech_territory.input_value == None:
        mediatech_territory_relativity = 1
    else:
        mediatech_territory_relativity = territory_params[territory_params["territory"] == hxd.cds.rating_factors.mediatech_territory.input_value]["factor"].iloc[0]
    
    hxd.cds.rating_factors.mediatech_territory.relativity = mediatech_territory_relativity



    #################################################################################
    # Step 2: Get the revenue and the splits by classes
    #################################################################################
    mediatech_total_revenue = hxd.cds.exposure.aggregate.mediatech_revenue
    #example data to delete:
    # mediatech_total_revenue = 900000
    # ccy_usd_conversion = 0.904521

    #converted to USD
    mediatech_total_revenue_usd = mediatech_total_revenue/ccy_usd_conversion
    mediatech_revenue_max = constants_params[constants_params["name"] == "mediatech_revenue_max"]["factor"].iloc[0]

    if mediatech_total_revenue_usd > mediatech_revenue_max :
        mediatech_total_revenue_usd = mediatech_revenue_max - 1
        hx.errors.validation("Media Tech Exposure: The total revenue is above the limit of " + str(mediatech_revenue_max)  + " (USD)")

    #get the revenue percentage from input
    input_revenue_pct = [getattr(getattr(hxd.cds.exposure.granular, item), "input_pct") for item in industry_list]
    revenue_df = pd.DataFrame({"industry": industry_list, "input_revenue_pct": input_revenue_pct})
    # # #example here
    # revenue_df.at[5, "input_revenue_pct"] = 1
    # revenue_df.at[12, "input_revenue_pct"] = 0.25
    # revenue_df.at[38, "input_revenue_pct"] = 0.25
    revenue_df["revenue_amount_usd"] = revenue_df["input_revenue_pct"].multiply(mediatech_total_revenue_usd)
    # map the class
    revenue_df = revenue_df.merge( industry_params[["industry_name", "class_name"]], how = "left", left_on = "industry", right_on = "industry_name")
    total_revenue_pct = revenue_df["input_revenue_pct"].sum()

    hxd.cds.exposure.granular.mediatech_total_revenue_pct = total_revenue_pct

    if (mediatech_total_revenue != 0) & (abs(total_revenue_pct - 1.00) > 0.00001) :
        hx.errors.validation("Media Tech Exposure: The total exposure percentage of Media Tech is not 100%")    

    # Export the result into data schema
    for item in industry_list:
        filtered_table = revenue_df[revenue_df["industry_name"] == item]
        setattr(getattr(hxd.cds.exposure.granular , item ), "revenue_amount",filtered_table["revenue_amount_usd"].iloc[0]*ccy_usd_conversion)
        setattr(getattr(hxd.cds.exposure.granular , item ), "class_name",filtered_table["class_name"].iloc[0] )
    
    #get the minimum premium from the highest risk class 
    if total_revenue_pct == 0 :
        max_class = 0
    else:
        max_class = max(revenue_df[revenue_df["input_revenue_pct"] > 0]["class_name"])
    
    if max_class == 0:
        mediatech_min_prem_usd = 0
    else:
        mediatech_min_prem_usd = minimum_premium_params[minimum_premium_params["class"] == max_class]["minimum_premium"].iloc[0] 
    
    hxd.cds.exposure.granular.mediatech_max_class = max_class


    # summarised by 6 classes
    revenue_df_class = revenue_df[["class_name", "input_revenue_pct", "revenue_amount_usd"]]
    revenue_df_class = revenue_df_class.groupby(by = ["class_name"]).sum()

    base_rate_params_filtered = base_rate_params[(base_rate_params["revenue"] <= mediatech_total_revenue_usd) & (base_rate_params["next"] > mediatech_total_revenue_usd)]
    
    if (base_rate_params_filtered["next"].iloc[0] - base_rate_params_filtered["revenue"].iloc[0]) == 0:
        base_rate_weight = 0
    else:
        base_rate_weight = (mediatech_total_revenue_usd - base_rate_params_filtered["revenue"].iloc[0]) / (base_rate_params_filtered["next"].iloc[0] - base_rate_params_filtered["revenue"].iloc[0])

    lower_base_rate_bound = []
    upper_base_rate_bound = []

    for index_num in range(0, revenue_df_class.shape[0]):
        lower_base_rate_bound.append(base_rate_params_filtered[f"lower_{index_num+1}"].iloc[0])
        upper_base_rate_bound.append(base_rate_params_filtered[f"upper_{index_num+1}"].iloc[0])
    
    revenue_df_class["lower_base_rate_bound"] = lower_base_rate_bound
    revenue_df_class["upper_base_rate_bound"] = upper_base_rate_bound
    revenue_df_class["base_rate"] = revenue_df_class["lower_base_rate_bound"].multiply(1-base_rate_weight) + revenue_df_class["upper_base_rate_bound"].multiply(base_rate_weight)

    revenue_df_class["base_rate_weighted"] = revenue_df_class["base_rate"].multiply(revenue_df_class["input_revenue_pct"])
    total_base_rate_usd = revenue_df_class["base_rate_weighted"].sum()

    hxd.cds.exposure.granular.mediatech_total_base_rate_relativity = total_base_rate_usd

    #################################################################################################
    # Step 3: Contingent BI/PD
    #################################################################################################

    bipd_input = hxd.cds.modifiers.mediatech_bipd.input_value
    #example:
    # bipd_input = "No"

    if bipd_input == None:
        bipd_relativity = 0
        hxd.cds.modifiers.mediatech_bipd.min_rel = 0
        hxd.cds.modifiers.mediatech_bipd.max_rel = 0
        hxd.cds.modifiers.mediatech_bipd.default_rel = 0
    else:
        bi_pd_params_filtered = bipd_params[bipd_params["contingent_bi_pd"] == bipd_input ]
        hxd.cds.modifiers.mediatech_bipd.min_rel = bi_pd_params_filtered["min"].iloc[0]
        hxd.cds.modifiers.mediatech_bipd.max_rel = bi_pd_params_filtered["max"].iloc[0]
        hxd.cds.modifiers.mediatech_bipd.default_rel = bi_pd_params_filtered["default"].iloc[0]
        if hxd.cds.modifiers.mediatech_bipd.input_relativity == None:
            bipd_relativity = hxd.cds.modifiers.mediatech_bipd.default_rel
        else:
            bipd_relativity = min(max(hxd.cds.modifiers.mediatech_bipd.input_relativity,hxd.cds.modifiers.mediatech_bipd.min_rel),hxd.cds.modifiers.mediatech_bipd.max_rel)
        
    hxd.cds.modifiers.mediatech_bipd.applied_rel = bipd_relativity

    #validation
    if (mediatech_total_revenue_usd!= 0) & (bipd_input  == None):
        hx.errors.validation("Media Tech Exposure: Contingent Bodily Injury / Property Damage coverage cannot be left empty!")
   
    input_relativity_org = hxd.cds.modifiers.mediatech_bipd.input_relativity
    if (mediatech_total_revenue_usd!= 0) & (bipd_input  is not None):
        if input_relativity_org is not None: 
            if (input_relativity_org < bi_pd_params_filtered["min"].iloc[0]) | (input_relativity_org>  bi_pd_params_filtered["max"].iloc[0]):
                hx.errors.validation("Media Tech Exposure: 'Input Relativity' for Contingent Bodily Injury / Property Damage is out of bound!")

    if (mediatech_total_revenue_usd!= 0) & (hxd.cds.rating_factors.mediatech_territory.input_value  == None):
        hx.errors.validation("Media Tech Exposure: Territory cannot be left empty!")
    
    
    #################################################################################################
    # Step 4: Prior Acts Factor
    #################################################################################################
    
    prior_acts_coverage = hxd.cds.rating_factors.mediatech_prior_acts.coverage
    # #example:
    # prior_acts_coverage  = "No Prior Acts"
    inception_date = hxd.hx_core.inception_date 
    if (prior_acts_coverage is None) or (prior_acts_coverage == "Unlimited"):
        retroactive_relativity = 1
        hxd.cds.rating_factors.mediatech_prior_acts.shown_by = False
    else:   
        retroactive_date = hxd.cds.rating_factors.mediatech_prior_acts.retroactive_date
        hxd.cds.rating_factors.mediatech_prior_acts.shown_by = True
        if (retroactive_date is None):
            retroactive_relativity = 1
        else:
            if (retroactive_date <= inception_date):
                month_difference = (inception_date.year - retroactive_date.year)*12 + (inception_date.month - retroactive_date.month )
                year_diff = int(month_difference // 12)
                if (month_difference - 12*year_diff) >= 6:
                    year_diff = year_diff + 1        
                year_diff = min (4, year_diff) # cap the retro years to be 4
                retroactive_relativity = retroactive_params[retroactive_params["years_of_prior_acts_coverage"] == year_diff]["factor"].iloc[0]
            else:
                retroactive_relativity = 1
                # hx.errors.validation("Media Tech Exposure: The Retroactive Date shoule be earlier than Inception Date")  

    
    hxd.cds.rating_factors.mediatech_prior_acts.relativity = retroactive_relativity

    #validation
    if prior_acts_coverage == "Specific Date":
        if retroactive_date is None:
            if hxd.cds.mediatech_coverage_selection: 
                hx.errors.validation("Media Tech Exposure: Retroactive Date cannot be left empty!")
        else:    
            if retroactive_date > hxd.hx_core.inception_date:
                if hxd.cds.mediatech_coverage_selection:
                    hx.errors.validation("Media Tech Exposure: Retroactive Date needs to be earlier than policy Inception Date!")

    #################################################################################################
    # Step 5: Business Longevity
    #################################################################################################

    business_years = hxd.cds.rating_factors.mediatech_longevity.business_years
    if business_years == None:
        longevity_relativity = 1.1
    else:
        longevity_relativity = longevity_params[longevity_params["year_in_business_name"] == business_years]["factor"].iloc[0]

            
    hxd.cds.rating_factors.mediatech_longevity.relativity = longevity_relativity

    

    #################################################################################################
    # Step 6: Experience Factor and Cost Included factor
    #################################################################################################

    experience_value = hxd.cds.modifiers.mediatech_claim_experience.input_value
    # # #example
    # experience_value = "Severe claim activity"
   
    experience_relativity_input = hxd.cds.modifiers.mediatech_claim_experience.input_relativity
    if experience_value == None:
        experience_relativity = 1
        hxd.cds.modifiers.mediatech_claim_experience.min_rel = 1
        hxd.cds.modifiers.mediatech_claim_experience.max_rel = 1
        hxd.cds.modifiers.mediatech_claim_experience.default_rel = 1
    else:
        claim_experience_params_filtered = claim_experience_params[claim_experience_params["experience"] == experience_value]
        hxd.cds.modifiers.mediatech_claim_experience.min_rel = claim_experience_params_filtered["min"].iloc[0]
        hxd.cds.modifiers.mediatech_claim_experience.max_rel = claim_experience_params_filtered["max"].iloc[0]
        hxd.cds.modifiers.mediatech_claim_experience.default_rel = claim_experience_params_filtered["default"].iloc[0]
        if experience_relativity_input == None:
            experience_relativity = hxd.cds.modifiers.mediatech_claim_experience.default_rel
        else:
            experience_relativity = min(max(experience_relativity_input,hxd.cds.modifiers.mediatech_claim_experience.min_rel),hxd.cds.modifiers.mediatech_claim_experience.max_rel)
    
    hxd.cds.modifiers.mediatech_claim_experience.applied_rel = experience_relativity 

    if experience_relativity_input is not None:
        if (experience_relativity_input < hxd.cds.modifiers.mediatech_claim_experience.min_rel) | (experience_relativity_input > hxd.cds.modifiers.mediatech_claim_experience.max_rel):
            if hxd.cds.mediatech_coverage_selection:
                hx.errors.validation("Media Tech Exposure: Claim Experience relativity is out of bound")


    cost_included = hxd.cds.rating_factors.mediatech_cost_included.cost_included
    # #example
    # cost_included = "Yes"
    if cost_included == None:
        cost_included_rel = 1
    else:
        cost_included_rel = cost_included_params[cost_included_params["response"] == cost_included]["factor"].iloc[0]
    
    hxd.cds.rating_factors.mediatech_cost_included.relativity = cost_included_rel

    if (mediatech_total_revenue != 0 ) & (cost_included is None):
        if hxd.cds.mediatech_coverage_selection:
            hx.errors.validation("Media Tech Exposure: Cost Included cannot be left empty")

    
    #################################################################################################
    # Step 7: Schedule factors
    #################################################################################################  

    schedule_input_rel = [getattr(getattr(hxd.cds.modifiers, item), "input_value") for item in schedule_params["schedule_name"]]

    schedule_df = pd.DataFrame({"schedule_name":schedule_params["schedule_name"],"schedule_description":schedule_params["schedule_factor"] ,"input_relativity": schedule_input_rel })
    schedule_df = schedule_df.merge(schedule_params[["schedule_name","min", "max"]], how = "left", left_on="schedule_name", right_on="schedule_name")
    schedule_df["applied"] = schedule_df[["input_relativity", "min"]].max(axis = 1)
    schedule_df["applied"] = schedule_df[["applied", "max"]].min(axis = 1)

    total_schedule_relativity = 1+ schedule_df["applied"].sum()

    #export schedule relativities
    for item in schedule_params["schedule_name"]:
        filtered_table = schedule_df[schedule_df["schedule_name"] == item]
        setattr(getattr(hxd.cds.modifiers, item), "min_val",filtered_table["min"].iloc[0] )
        setattr(getattr(hxd.cds.modifiers, item), "max_val",filtered_table["max"].iloc[0] )
        setattr(getattr(hxd.cds.modifiers, item), "applied_val",filtered_table["applied"].iloc[0] )
    
    hxd.cds.modifiers.mediatech_total_schedule.input_value = total_schedule_relativity -1
    hxd.cds.modifiers.mediatech_total_schedule.min_val = constants_params[constants_params["name"] == "mediatech_total_schedule_min"]["factor"].iloc[0]
    hxd.cds.modifiers.mediatech_total_schedule.max_val = constants_params[constants_params["name"] == "mediatech_total_schedule_max"]["factor"].iloc[0]
    hxd.cds.modifiers.mediatech_total_schedule.applied_val = min(max(hxd.cds.modifiers.mediatech_total_schedule.input_value, hxd.cds.modifiers.mediatech_total_schedule.min_val), hxd.cds.modifiers.mediatech_total_schedule.max_val)

    total_schedule_relativity_final = hxd.cds.modifiers.mediatech_total_schedule.applied_val 

    for index_num in range(0, schedule_df.shape[0]):
        if (schedule_df["input_relativity"].iloc[index_num] < schedule_df["min"].iloc[index_num]) | (schedule_df["input_relativity"].iloc[index_num] > schedule_df["max"].iloc[index_num]):
            if hxd.cds.mediatech_coverage_selection: 
                hx.errors.validation("Media Tech Exposure: Schedule modifier of " + schedule_df["schedule_description"].iloc[index_num] + " is out of bound")

    # #example:
    # total_schedule_relativity_final = 0.25
    #################################################################################################
    # Step 8: Limit factors
    #################################################################################################  


    mediatech_limit = [getattr(getattr(getattr(item, "coverages"), "mediatech") , "limit") for item in hxd.cds.layers]
    #mediatech_agg_limit = [getattr(getattr(getattr(item, "coverages"), "mediatech"), "aggregate_limit") for item in hxd.cds.layers]
    #set the aggregate limit to the the default of EEC
    [setattr(getattr(getattr(getattr(item, "coverages"), "mediatech"), "aggregate_limit"),"calculated", eec_limit) for (item, eec_limit) in zip(hxd.cds.layers, mediatech_limit)]
    mediatech_agg_limit = [getattr(getattr(getattr(getattr(item, "coverages"), "mediatech"), "aggregate_limit"), "selected") for item in hxd.cds.layers]
    #mediatech_deductible = [getattr(getattr(getattr(item, "coverages"), "mediatech") , "deductible") for item in hxd.cds.layers ]
    # update the none

    # # example
    # mediatech_limit = [1000000, 1500000, 2000000, 2500000]
    # mediatech_agg_limit = [1000000, 1500000, 2000000, 2500000]
    # convert to USD

    #set up default limit to $1m if no limit (relativity = 1)
    #cap at $15m
    limit_cap = constants_params[constants_params["name"] == "mediatech_eeclimit_cap"]["factor"].iloc[0]
    limit_floor = constants_params[constants_params["name"] == "mediatech_eeclimit_floor"]["factor"].iloc[0]
    mediatech_limit_usd = [limit_floor if x is None else max(min(x/ccy_usd_conversion,limit_cap), limit_floor) for x in mediatech_limit]
    #set aggregate limit to be the same as EEC limit if None (Realtivity = 1)
    mediatech_agg_limit_usd = [y if x is None else min(x/ccy_usd_conversion,limit_cap) if x/ccy_usd_conversion >= y else y for (x,y) in zip(mediatech_agg_limit, mediatech_limit_usd)]
    #cap at 5 and default to be 1
    aggregate_cap = constants_params[constants_params["name"] == "mediatech_agg_to_eec_ratio_cap"]["factor"].iloc[0]
    mediatech_agg_eec_ratio = [min(x/y,aggregate_cap) if y > 0 else 1 for (x,y) in zip(mediatech_agg_limit_usd, mediatech_limit_usd)]

    # revenue column
    ilf_rows_params_filtered = ilf_rows_params[ilf_rows_params["revenue_lower"] <= mediatech_total_revenue_usd].iloc[-1]
    revenue_lower = ilf_rows_params_filtered["revenue_lower"]
    revenue_upper = ilf_rows_params_filtered["revenue_upper"]
    column_lower = ilf_rows_params_filtered["column_lower"]
    column_upper = ilf_rows_params_filtered["column_upper"]
    #revenue ratio in band
    revenue_ratio = (mediatech_total_revenue_usd - revenue_lower)/(revenue_upper -  revenue_lower)

    #EEC limit bound
    eec_limit_lower_bound = []
    eec_limit_upper_bound = []
    for index_num in range(0, len(mediatech_limit_usd)):
        temp_table_filtered = eec_limit_params[(eec_limit_params["limit_lower"] <= mediatech_limit_usd[index_num]) & (eec_limit_params["limit_upper"] > mediatech_limit_usd[index_num])]
        eec_limit_lower_bound.append(temp_table_filtered["limit_lower"].iloc[0])
        eec_limit_upper_bound.append(temp_table_filtered["limit_upper"].iloc[0])
    #limit ratio in band
    eec_limit_ratio = [(z-x)/(y-x) if (y-x) > 0 else 0 for (x, y, z) in zip(eec_limit_lower_bound, eec_limit_upper_bound, mediatech_limit_usd)]

    #get pandas dataframe
    ilf_factor_df = pd.DataFrame({"agg_limit": mediatech_agg_limit_usd , "eec_limit": mediatech_limit_usd, "agg_eec_ratio": mediatech_agg_eec_ratio, 
    "eec_limit_lower_bound": eec_limit_lower_bound, "eec_limit_upper_bound": eec_limit_upper_bound , "eec_limit_ratio": eec_limit_ratio })
    # lower revenue lower and upper limit
    ilf_factor_df["lower_limit_weight_lower_revenue"] = (1-ilf_factor_df["eec_limit_ratio"]).multiply(1-revenue_ratio)
    ilf_factor_df["upper_limit_weight_lower_revenue"] = (ilf_factor_df["eec_limit_ratio"]).multiply(1-revenue_ratio)
    # upper revenue lower and upper limit
    ilf_factor_df["lower_limit_weight_upper_revenue"] = (1-ilf_factor_df["eec_limit_ratio"]).multiply(revenue_ratio)
    ilf_factor_df["upper_limit_weight_upper_revenue"] = (ilf_factor_df["eec_limit_ratio"]).multiply(revenue_ratio)
    # merge the limit factor
    #lower revenue
    ilf_factor_df = ilf_factor_df.merge(eec_limit_params.iloc[:,[0,column_lower-1]], how = "left", left_on = "eec_limit_lower_bound", right_on="limit_lower")
    ilf_factor_df = ilf_factor_df.rename({"factor_small_revenue": "lower_limit_lower_revenue"}, axis = 1)
    ilf_factor_df = ilf_factor_df.drop(["limit_lower"], axis = 1)
    ilf_factor_df = ilf_factor_df.merge(eec_limit_params.iloc[:,[0,column_lower-1]], how = "left", left_on = "eec_limit_upper_bound", right_on="limit_lower")
    ilf_factor_df = ilf_factor_df.rename({"factor_small_revenue": "upper_limit_lower_revenue"}, axis = 1)
    ilf_factor_df = ilf_factor_df.drop(["limit_lower"], axis = 1)
    #upper revene
    ilf_factor_df = ilf_factor_df.merge(eec_limit_params.iloc[:,[0,column_upper-1]], how = "left", left_on = "eec_limit_lower_bound", right_on="limit_lower")
    # ilf_factor_df = ilf_factor_df.rename({"factor_small_revenue": "lower_limit_upper_revenue"}, axis = 1)
    ilf_factor_df = ilf_factor_df.set_axis([*ilf_factor_df.columns[:-1], 'lower_limit_upper_revenue'], axis=1, inplace=False)
    ilf_factor_df = ilf_factor_df.drop(["limit_lower"], axis = 1)
    ilf_factor_df = ilf_factor_df.merge(eec_limit_params.iloc[:,[0,column_upper-1]], how = "left", left_on = "eec_limit_upper_bound", right_on="limit_lower")
    # ilf_factor_df = ilf_factor_df.rename({"factor_small_revenue": "upper_limit_upper_revenue"}, axis = 1)
    ilf_factor_df = ilf_factor_df.set_axis([*ilf_factor_df.columns[:-1], 'upper_limit_upper_revenue'], axis=1, inplace=False)
    ilf_factor_df = ilf_factor_df.drop(["limit_lower"], axis = 1)
    
    #EEC increased limit factor
    ilf_factor_df["eec_limit_relativity"] = ilf_factor_df["lower_limit_weight_lower_revenue"].multiply(ilf_factor_df["lower_limit_lower_revenue"]) + ilf_factor_df["upper_limit_weight_lower_revenue"].multiply(ilf_factor_df["upper_limit_lower_revenue"]) + ilf_factor_df["lower_limit_weight_upper_revenue"].multiply(ilf_factor_df["lower_limit_upper_revenue"]) +ilf_factor_df["upper_limit_weight_upper_revenue"].multiply(ilf_factor_df["upper_limit_upper_revenue"]) 

    # Aggregate Limit factor
    agg_lower_bound = []
    agg_upper_bound = []
    agg_factor_lower = []
    agg_factor_upper = []
    for index_num in range(0, len(mediatech_agg_eec_ratio)):
        temp_table = agg_limit_params[agg_limit_params["agg_limit_ratio_lower"] <= mediatech_agg_eec_ratio[index_num]]
        agg_lower_bound.append(temp_table["agg_limit_ratio_lower"].iloc[0])
        agg_upper_bound.append(temp_table["agg_limit_ratio_upper"].iloc[0])
        agg_factor_lower.append(temp_table["factor_lower"].iloc[0])
        agg_factor_upper.append(temp_table["factor_upper"].iloc[0])
    
    ilf_factor_df["agg_lower_bound"] = agg_lower_bound
    ilf_factor_df["agg_upper_bound"] = agg_upper_bound
    ilf_factor_df["agg_factor_lower"] = agg_factor_lower
    ilf_factor_df["agg_factor_upper"] = agg_factor_upper

    ilf_factor_df["agg_ratio_weight"] = np.where((ilf_factor_df["agg_upper_bound"] - ilf_factor_df["agg_lower_bound"]) == 0, 0, (ilf_factor_df["agg_eec_ratio"] - ilf_factor_df["agg_lower_bound"])/ (ilf_factor_df["agg_upper_bound"] - ilf_factor_df["agg_lower_bound"]) )
    ilf_factor_df["agg_limit_relativity"] = ilf_factor_df["agg_ratio_weight"].multiply(ilf_factor_df["agg_factor_upper"] ) + (1-ilf_factor_df["agg_ratio_weight"]).multiply(ilf_factor_df["agg_factor_lower"])

    # multiply EEC and AGG limit factors
    ilf_factor_df["limit_final_relativity"] = ilf_factor_df["agg_limit_relativity"].multiply(ilf_factor_df["eec_limit_relativity"] )

    

    #################################################################################################
    # Step 9: Deductible factors
    #################################################################################################  

    guideline_deductible_filtered = guideline_deductible_params[guideline_deductible_params["revenue_low"] <= mediatech_total_revenue_usd].iloc[-1]
    guideline_deductible = guideline_deductible_filtered["intercept"] + guideline_deductible_filtered["slope"]*mediatech_total_revenue_usd
    guideline_deductible_local_ccy = guideline_deductible * ccy_usd_conversion

    #export guideline deductible
    for item, index_num in zip(hxd.cds.layers, range(len(hxd.cds.layers))):
        if item.coverages.mediatech.limit  == None:
            item.coverages.mediatech.guideline_deductible = None
        else:
            item.coverages.mediatech.guideline_deductible = guideline_deductible_local_ccy
    
    #mediatech_deductible = [getattr(getattr(getattr(item, "coverages"), "mediatech") , "deductible") for item in hxd.cds.layers]
    # #example
    # mediatech_deductible = [5000,3000,4000,5000]
    [setattr(getattr(getattr(getattr(item, "coverages"), "mediatech") , "deductible"), "calculated",item.coverages.mediatech.guideline_deductible) for item in hxd.cds.layers]
    mediatech_deductible = [getattr(getattr(getattr(getattr(item, "coverages"), "mediatech") , "deductible"), "selected") for item in hxd.cds.layers]
    mediatech_deductible = [0 if x is None else x for x in mediatech_deductible]
    mediatech_deductible_usd = [x/ccy_usd_conversion for x in mediatech_deductible]


    # deductible interpolate factor
    deductible_interpolate = [ min(x/guideline_deductible,5) if guideline_deductible!= 0 else 0 for x in mediatech_deductible_usd]
    deductible_interpolate = [0 if x < 0 else x for x in deductible_interpolate]
    # deductuble lower bound
    deductible_lower = []
    deductible_upper = []
    for index_num in range(0, len(deductible_interpolate)):
        temp_table = deductible_params[deductible_params["lower"] <= deductible_interpolate[index_num]].iloc[-1]
        deductible_lower.append(temp_table["lower"])
        deductible_upper.append(temp_table["higher"])
    
    deductible_factor_df = pd.DataFrame({"deductible_interpolate":deductible_interpolate, "deductible_lower": deductible_lower, "deductible_upper": deductible_upper })
    deductible_factor_df = deductible_factor_df.merge(deductible_params[["lower", "factor"]], how = "left", left_on="deductible_lower", right_on="lower")
    deductible_factor_df = deductible_factor_df.rename({"factor": "lower_factor"}, axis = 1)
    deductible_factor_df = deductible_factor_df.drop(["lower"], axis = 1)
    deductible_factor_df = deductible_factor_df.merge(deductible_params[["lower", "factor"]], how = "left", left_on="deductible_upper", right_on="lower")
    deductible_factor_df = deductible_factor_df.rename({"factor": "upper_factor"}, axis = 1)
    deductible_factor_df = deductible_factor_df.drop(["lower"], axis = 1)  
    # get the final deductible relativity
    deductible_factor_df["weight"] = np.where((deductible_factor_df["deductible_upper"] - deductible_factor_df["deductible_lower"]) == 0, 0, (deductible_factor_df["deductible_interpolate"] - deductible_factor_df["deductible_lower"] ) / (deductible_factor_df["deductible_upper"] - deductible_factor_df["deductible_lower"]) )
    deductible_factor_df["deductible_relativity"] = np.where(deductible_factor_df["deductible_interpolate"] < 0.1, 1.4, (deductible_factor_df["upper_factor"] - deductible_factor_df["lower_factor"])*deductible_factor_df["weight"] +deductible_factor_df["lower_factor"])

    for index_num, item in zip(range(0, len(hxd.cds.layers)), hxd.cds.layers):
        item.coverages.mediatech.deductible_relativity = deductible_factor_df["deductible_relativity"].iloc[index_num] 
    
    for item in mediatech_deductible:
        if item < 0 :
            if hxd.cds.mediatech_coverage_selection:
                hx.errors.validation("Media Tech Pricing: Retention Cannot be Negative!")  
        
    #################################################################################################
    # Step 10: Additional Defense Factor
    #################################################################################################      
    mediatech_add_defense = [getattr(getattr(getattr(item, "coverages"), "mediatech") , "additional_defense_limit") for item in hxd.cds.layers]
    mediatech_add_defense = [0 if x is None else x for x in mediatech_add_defense]
    # #example
    # mediatech_add_defense = [500000,500000,500000,500000]
    mediatech_add_defense_usd = [x / ccy_usd_conversion for x in mediatech_add_defense]
    mediatech_add_defense_usd = [0 if x < 0 else x for x in mediatech_add_defense_usd]
    mediatech_add_defense_usd = [50000000 if x > 50000000 else x for x in mediatech_add_defense_usd]

    add_defense_lower = []
    add_defense_upper = []
    for index_num in range(0, len(mediatech_add_defense_usd)):
        temp_table = additional_defense_params[additional_defense_params["additional_defense_lower"] <= mediatech_add_defense_usd[index_num]].iloc[-1]
        add_defense_lower.append(temp_table["additional_defense_lower"])
        add_defense_upper.append(temp_table["additional_defense_upper"])
    
    additional_defense_factor_df = pd.DataFrame({"add_defense_limit":mediatech_add_defense_usd, "add_defense_lower": add_defense_lower, "add_defense_upper": add_defense_upper })
    additional_defense_factor_df = additional_defense_factor_df.merge(additional_defense_params[["additional_defense_lower", "debit"]], how = "left", left_on = "add_defense_lower", right_on = "additional_defense_lower")
    additional_defense_factor_df = additional_defense_factor_df.rename({"debit": "defense_lower_factor"}, axis = 1)
    additional_defense_factor_df = additional_defense_factor_df.drop(["additional_defense_lower"], axis = 1)
    additional_defense_factor_df = additional_defense_factor_df.merge(additional_defense_params[["additional_defense_lower", "debit"]], how = "left", left_on = "add_defense_upper", right_on = "additional_defense_lower")
    additional_defense_factor_df = additional_defense_factor_df.rename({"debit": "defense_upper_factor"}, axis = 1)
    additional_defense_factor_df = additional_defense_factor_df.drop(["additional_defense_lower"], axis = 1)
    # additional defense relativity
    additional_defense_factor_df["weight"] = np.where((additional_defense_factor_df["add_defense_upper"] - additional_defense_factor_df["add_defense_lower"]) == 0 , 0, (additional_defense_factor_df["add_defense_limit"] - additional_defense_factor_df["add_defense_lower"]) / (additional_defense_factor_df["add_defense_upper"] - additional_defense_factor_df["add_defense_lower"]) )
    additional_defense_factor_df["additional_defense_relativity"] = 1+(additional_defense_factor_df["defense_lower_factor"] + additional_defense_factor_df["weight"]*(additional_defense_factor_df["defense_upper_factor"] - additional_defense_factor_df["defense_lower_factor"]))

    for index_num, item in zip(range(0, len(hxd.cds.layers)), hxd.cds.layers):
        item.coverages.mediatech.limit_relativity = ilf_factor_df["limit_final_relativity"].iloc[index_num] * additional_defense_factor_df["additional_defense_relativity"].iloc[index_num] 
    
    # Add the model validation here   
    for item in hxd.cds.layers:
        eec_limit = item.coverages.mediatech.limit
        agg_limit = item.coverages.mediatech.aggregate_limit.selected
        dol_limit = item.coverages.mediatech.additional_defense_limit
        if (eec_limit is not None):
            if (eec_limit/ccy_usd_conversion > limit_cap):
                if hxd.cds.mediatech_coverage_selection:
                    hx.errors.validation("Media Tech Pricing: Each and every limit cannot be more than $15m USD!")
            if (eec_limit/ccy_usd_conversion < limit_floor):
                if hxd.cds.mediatech_coverage_selection:
                    hx.errors.validation("Media Tech Pricing: Each and every limit cannot be less than $100k USD!")   
        if (eec_limit is not None) & (agg_limit is None):
            if hxd.cds.mediatech_coverage_selection:
                hx.errors.validation("Media Tech Pricing: Aggregate limit cannot be left empty!")
        if (eec_limit is not None) & (agg_limit is not None):
            if (agg_limit/ccy_usd_conversion > limit_cap):
                if hxd.cds.mediatech_coverage_selection:
                    hx.errors.validation("Media Tech Pricing: Aggregate limit cannot be more than $15m USD!")
        if (eec_limit is not None) & (agg_limit is not None):
            if (agg_limit < eec_limit):
                if hxd.cds.mediatech_coverage_selection:
                    hx.errors.validation("Media Tech Pricing: Aggregate limit cannot be less than Each and Every Limit!")
        if (eec_limit is not None) & (agg_limit is not None):
            if eec_limit > 0:
                if (agg_limit/eec_limit > aggregate_cap):
                    if hxd.cds.mediatech_coverage_selection:
                        hx.errors.validation("Media Tech Pricing: Aggregate limit cannot be more than 5 times of Each and Every Limit!")    
        if(agg_limit is not None) & (dol_limit is not None):
            if dol_limit > agg_limit:
                if hxd.cds.mediatech_coverage_selection:
                    hx.errors.validation("Media Tech Pricing: Additional Defence Limit cannot be more than Aggregate Limit!")    
        if(dol_limit is not None):
            if(dol_limit < 0):
                if hxd.cds.mediatech_coverage_selection:
                    hx.errors.validation("Media Tech Pricing: Additional Defence Limit cannot be Negative!")   



    #################################################################################################
    # Step 11: Pro rata factor - multi year
    #################################################################################################  

    mediatech_prorata_relativity = 1


    #################################################################################################
    # Step 12.1: Premium Calculation BEFORE Minimum Premium
    ################################################################################################# 
    # Gross Premium BEFORE UW adjustment and BEFORE minimum premium 
    mediatech_prem_before_uwadj_before_miniprem_usd = [total_base_rate_usd for i in hxd.cds.layers]
    mediatech_prem_before_uwadj_before_miniprem_usd = pd.Series(mediatech_prem_before_uwadj_before_miniprem_usd)
    mediatech_prem_before_uwadj_before_miniprem_usd = mediatech_prem_before_uwadj_before_miniprem_usd.multiply(retroactive_relativity)
    mediatech_prem_before_uwadj_before_miniprem_usd = mediatech_prem_before_uwadj_before_miniprem_usd.multiply(mediatech_territory_relativity)
    mediatech_prem_before_uwadj_before_miniprem_usd = mediatech_prem_before_uwadj_before_miniprem_usd.multiply(longevity_relativity)
    mediatech_prem_before_uwadj_before_miniprem_usd = mediatech_prem_before_uwadj_before_miniprem_usd.multiply(cost_included_rel)
    mediatech_prem_before_uwadj_before_miniprem_usd = mediatech_prem_before_uwadj_before_miniprem_usd.multiply(deductible_factor_df["deductible_relativity"])
    mediatech_prem_before_uwadj_before_miniprem_usd_incl_nmp = mediatech_prem_before_uwadj_before_miniprem_usd.multiply(1+nmp_load)

    # Gross Premium POST UW adjustment and BEFORE minimum premium 
    mediatech_prem_post_uwadj_before_miniprem_usd = [total_base_rate_usd for i in hxd.cds.layers]
    mediatech_prem_post_uwadj_before_miniprem_usd = pd.Series(mediatech_prem_post_uwadj_before_miniprem_usd)
    #subjective factor BI/PD 
    mediatech_prem_post_uwadj_before_miniprem_usd = mediatech_prem_post_uwadj_before_miniprem_usd.multiply(1+bipd_relativity)
    #objective factors:
    mediatech_prem_post_uwadj_before_miniprem_usd = mediatech_prem_post_uwadj_before_miniprem_usd.multiply(retroactive_relativity)
    mediatech_prem_post_uwadj_before_miniprem_usd = mediatech_prem_post_uwadj_before_miniprem_usd.multiply(mediatech_territory_relativity)
    mediatech_prem_post_uwadj_before_miniprem_usd = mediatech_prem_post_uwadj_before_miniprem_usd.multiply(longevity_relativity)
    mediatech_prem_post_uwadj_before_miniprem_usd = mediatech_prem_post_uwadj_before_miniprem_usd.multiply(cost_included_rel)
    mediatech_prem_post_uwadj_before_miniprem_usd = mediatech_prem_post_uwadj_before_miniprem_usd.multiply(deductible_factor_df["deductible_relativity"])
    #Subjective factor: experience rating and schedule factor
    mediatech_prem_post_uwadj_before_miniprem_usd = mediatech_prem_post_uwadj_before_miniprem_usd.multiply(experience_relativity)
    mediatech_prem_post_uwadj_before_miniprem_usd = mediatech_prem_post_uwadj_before_miniprem_usd.multiply(1+total_schedule_relativity_final)
    mediatech_prem_post_uwadj_before_miniprem_usd_incl_nmp = mediatech_prem_post_uwadj_before_miniprem_usd.multiply(1+nmp_load)

    #################################################################################################
    # Step 12.2: Premium Calculation POST Minimum Premium
    #################################################################################################  
       
    # Gross Premium BEFORE UW adjustment and AFTER minimum premium 
    mediatech_prem_before_uwadj_usd_org= np.maximum(mediatech_prem_before_uwadj_before_miniprem_usd_incl_nmp , mediatech_min_prem_usd)
    # Gross Premium AFTER UW adjustment and AFTER minimum premium 
    mediatech_prem_post_uwadj_usd_org = np.maximum(mediatech_prem_post_uwadj_before_miniprem_usd_incl_nmp , mediatech_min_prem_usd)
    # UW adjustment
    mediatech_prem_uw_adjustment = mediatech_prem_post_uwadj_usd_org.div(mediatech_prem_before_uwadj_usd_org)


    #################################################################################################
    # Step 12.3: Premium Calculation Post Limit Factor
    #################################################################################################
    # Gross premium before UW adjustment
    mediatech_prem_before_uwadj_usd =  mediatech_prem_before_uwadj_usd_org.multiply(ilf_factor_df["limit_final_relativity"])
    mediatech_prem_before_uwadj_usd =  mediatech_prem_before_uwadj_usd + mediatech_prem_before_uwadj_usd_org.multiply(additional_defense_factor_df["additional_defense_relativity"]-1)
    mediatech_prem_before_uwadj_usd =  mediatech_prem_before_uwadj_usd.multiply(mediatech_prorata_relativity)

    # Gross premium after UW adjustment
    mediatech_prem_post_uwadj_usd =  mediatech_prem_post_uwadj_usd_org.multiply(ilf_factor_df["limit_final_relativity"])
    mediatech_prem_post_uwadj_usd =  mediatech_prem_post_uwadj_usd + mediatech_prem_post_uwadj_usd_org.multiply(additional_defense_factor_df["additional_defense_relativity"]-1)
    mediatech_prem_post_uwadj_usd =  mediatech_prem_post_uwadj_usd.multiply(mediatech_prorata_relativity)

    #Gross premium after UW adjustment BEFORE minimum premium
    mediatech_prem_post_uwadj_before_miniprem_usd_org = mediatech_prem_post_uwadj_before_miniprem_usd_incl_nmp
    mediatech_prem_post_uwadj_before_miniprem_usd = mediatech_prem_post_uwadj_before_miniprem_usd_org.multiply(ilf_factor_df["limit_final_relativity"])
    mediatech_prem_post_uwadj_before_miniprem_usd = mediatech_prem_post_uwadj_before_miniprem_usd + mediatech_prem_post_uwadj_before_miniprem_usd_org.multiply(additional_defense_factor_df["additional_defense_relativity"]-1)
    mediatech_prem_post_uwadj_before_miniprem_usd = mediatech_prem_post_uwadj_before_miniprem_usd.multiply(mediatech_prorata_relativity) 


    #################################################################################################
    # Step 13:  Expected claims costs
    #################################################################################################
    model_brokerage = constants_params[constants_params["name"] == "model_brokerage"]["factor"].iloc[0]
    priced_to_lr = constants_params[constants_params["name"] == "priced_to_lr"]["factor"].iloc[0]

    mediatech_claims_cost_before_uwadj_usd = mediatech_prem_before_uwadj_usd*(1-model_brokerage)*priced_to_lr
    mediatech_claims_cost_after_uwadj_usd = mediatech_prem_post_uwadj_usd*(1-model_brokerage)*priced_to_lr
    #claims cost BEFORE minimum premium 
    mediatech_claims_cost_after_uwadj_usd_before_minimum_premium = mediatech_prem_post_uwadj_before_miniprem_usd*(1-model_brokerage)*priced_to_lr

    for item, index_num in zip(hxd.cds.layers, range(0, len(hxd.cds.layers))):
        setattr(getattr(getattr(item, "coverages"), "mediatech"), "expected_loss_cost_pre_uw_adj_usd", mediatech_claims_cost_before_uwadj_usd[index_num])
        setattr(getattr(getattr(item, "coverages"), "mediatech"), "expected_loss_cost_usd", mediatech_claims_cost_after_uwadj_usd[index_num])
        setattr(getattr(getattr(item, "coverages"), "mediatech"), "expected_loss_cost_before_minimum_premium_usd", mediatech_claims_cost_after_uwadj_usd_before_minimum_premium[index_num])
        setattr(getattr(getattr(item, "coverages"), "mediatech"), "expected_loss_cost_pre_uw_adj", mediatech_claims_cost_before_uwadj_usd[index_num]*ccy_usd_conversion)
        setattr(getattr(getattr(item, "coverages"), "mediatech"), "expected_loss_cost", mediatech_claims_cost_after_uwadj_usd[index_num]*ccy_usd_conversion)
        setattr(getattr(getattr(item, "coverages"), "mediatech"), "expected_loss_cost_before_minimum_premium", mediatech_claims_cost_after_uwadj_usd_before_minimum_premium[index_num]*ccy_usd_conversion) 
        setattr(item, "option_selected", item.coverages.mediatech.option_selected)       


    #----------------------------------------------------------------------------------------------#
    # Step 14: Validation on status
    #----------------------------------------------------------------------------------------------#

    temp_sum = 0
    temp_sum_option = 0

    for item in hxd.cds.layers:
        section_status = item.coverages.mediatech.status
        section_reference = item.coverages.mediatech.section_reference
        section_quoted_prem = item.coverages.mediatech.quoted_premium
        section_option_selected = item.coverages.mediatech.option_selected
        if section_status == "Bound":
            temp_sum += 1
            if section_reference is None:
                if hxd.cds.mediatech_coverage_selection:
                    hx.errors.validation("Media Tech Pricing Summary: Need to input 'Section Reference' to Bound option! ")
            else:
                if len(section_reference) > 20:
                    if hxd.cds.mediatech_coverage_selection:
                        hx.errors.validation("Media Tech Pricing Summary: 'Policy Section Reference' cannot exceed 20 characters! ")
            if section_quoted_prem is None:
                if hxd.cds.mediatech_coverage_selection:
                    hx.errors.validation("Media Tech Pricing Summary: Need to enter Quoted Premium for Bound option! ")
            if section_option_selected == "No":
                if hxd.cds.mediatech_coverage_selection:
                    hx.errors.validation("Media Tech Pricing Summary: Select 'Yes' for Bound option!")
        if section_status == "Quoted":
            if section_quoted_prem is None:
                if hxd.cds.mediatech_coverage_selection:
                    hx.errors.validation("Media Tech Pricing Summary: Need to enter Quoted Premium for Quoted option! ")
        if section_option_selected == "Yes":
            temp_sum_option += 1           
    
    if temp_sum > 1:
        if hxd.cds.mediatech_coverage_selection:
            hx.errors.validation("Media Tech Coverage: Can Only Bound 1 Option!")
    if temp_sum_option > 1:
        if hxd.cds.mediatech_coverage_selection:
            hx.errors.validation("Media Tech Coverage: Can Only Select 1 Option!")

    if hxd.cds.mediatech_coverage_selection == True:
        if mediatech_total_revenue == 0:
            if hxd.cds.mediatech_coverage_selection:
                hx.errors.validation("Media Tech Coverage: Need to Input the 'Total Revenue!' in the 'Exposure Information' section! ")


    

    



    

    








    


    

        
        



    

    




  


    
    













    


    pass