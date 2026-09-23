######################################################################################
# This is the pricing code for GL
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




def rate_pricing_gl(hxd):

    revenue_params = hx.params.table_gl_product_revenue
    tier_params = hx.params.table_gl_product_tier
    exposure_type_params = hx.params.table_gl_product_exposure_type
    product_limit_params = hx.params.table_gl_product_limit
    product_dol_params = hx.params.table_gl_product_defence_limit
    product_excess_params = hx.params.table_gl_product_excess
    loss_experience_params = hx.params.table_gl_product_loss_experience
    product_dedutible_params = hx.params.table_gl_product_deductible
    excess_params = hx.params.table_gl_product_excess
    dol_params = hx.params.table_gl_product_defence_limit
    min_premium_tier_9_params = hx.params.table_gl_product_minimum_premium_tier9
    min_premium_params = hx.params.table_gl_product_minimum_premium
    constants_params = hx.params.table_constants
    tp_params = hx.params.table_tp_parameters
    nmp_load = tp_params[tp_params["business_plan_class"] =="International Specialty Programmes" ]["nmp_load"].iloc[0]
    # nmp_load = 0


    gl_model_brokerage = constants_params[constants_params["name"] == "model_brokerage_gl"]["factor"].iloc[0]
    hxd.cds.exposure.granular.gl_product = "Products"


    #get the exchange rate
    xe_table = hx.params.table_fx_rates
    ccy_usd_conversion =xe_table[xe_table["ccy"] == hxd.cds.currencies.source_currency]["fx_rate"].iloc[0]/ xe_table[xe_table["ccy"] == "USD"]["fx_rate"].iloc[0]

    ########################################################################
    #  Step 1: Revenue
    ########################################################################
    gl_revenue = hxd.cds.exposure.granular.gl_revenue

    [setattr(revenue_row, "revenue_input_usd", getattr(revenue_row, "revenue_input")/ccy_usd_conversion) for revenue_row in gl_revenue]

    total_revenue = sum([revenue_row.revenue_input for revenue_row in gl_revenue])   
    total_revenue_usd = total_revenue /ccy_usd_conversion
    #example
    # total_revenue_usd = 3316672.581

    total_revenue_relativity = np.interp(total_revenue_usd,revenue_params["revenue_band"], revenue_params["factor"])
    setattr(hxd.cds.exposure.aggregate, "gl_revenue",total_revenue)
    # total revenue base rate
    revenue_base_rate = total_revenue_usd*total_revenue_relativity/1000

    # tier and type of revenue
    tier_input = []
    revenue_input = []
    exposure_type_input = []
    for item in gl_revenue:
        tier_input.append(item.tier_input)
        revenue_input.append(item.revenue_input)
        exposure_type_input.append(item.exposure_type)
    
    for index_num in range(0,len(gl_revenue)):
        if revenue_input[index_num] > 0 :
            if (tier_input[index_num] is None) | (exposure_type_input is None):
                hx.errors.validation("GL Exposure: Tier and Exposure Type cannot be left empty!")

    #example
    # tier_input = ["Tier 2", "Tier 3", None]
    # revenue_input = [2000000/ccy_usd_conversion, 1000000/ccy_usd_conversion, 0]
    #exposure_type_input = ["Manufacturer", "Both", None]
    revenue_input_usd = [0 if x is None else x/ccy_usd_conversion for x in revenue_input]
    #set a default value for tier_input otherwise rate change won't working.
    tier_input = ["Tier 1" if x is None else x for x in tier_input]
    
    revenue_df = pd.DataFrame({"tier": tier_input,  "exposure_type": exposure_type_input, "revenue_amount_usd": revenue_input_usd})
    revenue_df = revenue_df.merge(tier_params[["tier_description", "factor"]], how = "left", left_on= "tier", right_on="tier_description")
    revenue_df  = revenue_df.rename({"factor": "tier_relativity"}, axis = 1)
    revenue_df  = revenue_df.drop(["tier_description"], axis = 1)
    # if not mapping then give 1
    revenue_df["tier_relativity"] = revenue_df["tier_relativity"].fillna(1)

    revenue_df = revenue_df.merge(exposure_type_params[["exposure_type_description", "factor"]], how = "left", left_on = "exposure_type", right_on = "exposure_type_description")
    revenue_df = revenue_df.rename({"factor": "exposure_type_relativity"}, axis = 1)
    revenue_df  = revenue_df.drop(["exposure_type_description"], axis = 1)
    revenue_df["exposure_type_relativity"] = revenue_df["exposure_type_relativity"].fillna(1)

    if total_revenue_usd == 0:
        revenue_df["revenue_pct"] = 0
    else: 
        revenue_df["revenue_pct"] = revenue_df["revenue_amount_usd"].divide(total_revenue_usd )

    revenue_df["revenue_type_tier_relativity"] = revenue_df["tier_relativity"].multiply(revenue_df["exposure_type_relativity"]).multiply(revenue_df["revenue_pct"])
    # Tier and Type final relativity
    revenue_type_tier_relativity = revenue_df["revenue_type_tier_relativity"].sum()

    revenue_df["tier_9_flag"] = [1 if x == "Tier 9" else 0 for x in revenue_df["tier"]]
    tier_9_flag = revenue_df["tier_9_flag"].sum()



    ########################################################################
    #  Step 2: Loss Experience
    ########################################################################

    loss_experience = hxd.cds.rating_factors.gl_loss.input_value
    #example 
    # loss_experience = "No Claims in 3-5 years"

    if loss_experience == None:
        loss_experience_relativity = 1
    else:
        loss_experience_relativity = loss_experience_params[loss_experience_params["loss_experience"] == loss_experience]["factor"].iloc[0]
    
    setattr(hxd.cds.rating_factors.gl_loss, "relativity", loss_experience_relativity)
    
    if (total_revenue_usd != 0) & (total_revenue_usd is not None):
        if loss_experience is None:
            hx.errors.validation("GL Exposure: Loss Experience cannot be left empty!")


    ########################################################################
    #  Step 3: Primary Deductible
    ########################################################################
    primary_deductible_org = []
    for item in hxd.cds.layers:
        primary_deductible_org.append(item.coverages.gl.deductible)
    primary_deductible = []
    primary_deductible = [0 if x is None else x for x in primary_deductible_org]
    #example
    # primary_deductible = [2500,1000000,0,0]

    primary_deductible_df = pd.DataFrame({"primary_deductible": primary_deductible})
    primary_deductible_df["primary_deductible_relativity"] = np.interp(primary_deductible_df["primary_deductible"], product_dedutible_params["deductible"], product_dedutible_params["factor"] )






    ########################################################################
    #  Step 4: Limit 
    ########################################################################

    product_eec_limit_org = []    
    product_agg_limit = []
    gl_agg_limit = []
    
    for item in hxd.cds.layers:
        eec_limit_temp = item.coverages.gl.limit
        product_eec_limit_org.append(eec_limit_temp )
        setattr(item.coverages.gl, "aggregate_limit",eec_limit_temp)
        product_agg_limit.append(item.coverages.gl.aggregate_limit)
        setattr(item.coverages.gl, "gl_limit_agg", eec_limit_temp)
        gl_agg_limit.append(item.coverages.gl.gl_limit_agg)
        setattr(item.coverages.gl, "personal_advertise_limit_agg", eec_limit_temp)
    
    product_eec_limit = []
    product_eec_limit = [0 if x is None else x for x in product_eec_limit_org]
    product_agg_limit = [0 if x is None else x for x in product_agg_limit]
    gl_agg_limit = [0 if x is None else x for x in gl_agg_limit]

    #example
    # product_eec_limit = [1000000, 2000000, 0, 0]
    # product_agg_limit = [1000000, 2000000, 0, 0]
    # gl_agg_limit = [1000000, 2000000, 0, 0]

    product_eec_limit_relativity = np.interp(product_eec_limit,  product_limit_params["liability_limits"], product_limit_params["factor"])
    product_eec_limit_relativity = [0 if x == 0 else y for (x,y) in zip(product_eec_limit ,product_eec_limit_relativity )]
    product_agg_limit_relativity = np.interp(product_agg_limit,  product_limit_params["liability_limits"], product_limit_params["factor"])
    product_agg_limit_relativity = [0 if x == 0 else y for (x,y) in zip(product_agg_limit ,product_agg_limit_relativity )]
    gl_agg_limit_relativity = np.interp(gl_agg_limit,  product_limit_params["liability_limits"], product_limit_params["factor"])
    gl_agg_limit_relativity = [0 if x == 0 else y for (x,y) in zip(gl_agg_limit,gl_agg_limit_relativity)]
    product_reinstatement_relativity = [0.7*(y-x)+x for (x,y) in zip(product_eec_limit_relativity,product_agg_limit_relativity )]
    gl_reinstatement_relativity = [0.9*(y-x)+x for (x,y) in zip(product_eec_limit_relativity,gl_agg_limit_relativity )]

    limit_eec_agg_relativity = [(x+y)/2 for (x,y) in zip(product_reinstatement_relativity,gl_reinstatement_relativity )]



    ########################################################################
    #  Step 5: Excess
    ########################################################################

    excess_input_org = []
    for item in hxd.cds.layers:
        excess_input_org.append(item.coverages.gl.excess_of)

    excess_input = []
    excess_input = [0 if x is None else x for x in excess_input_org]

    excess_option = hxd.cds.rating_factors.gl_excess_primary.input_value

    if excess_option == "Excess":
        hxd.cds.rating_factors.gl_excess_show = True
    else:
        hxd.cds.rating_factors.gl_excess_show = False

    #example
    # excess_input = [1000000,0,0,0]
    # excess_option = "Excess"

    excess_relativity = [1 if ((excess_option != "Excess") | (x ==0)) else 1 - np.interp(x, product_excess_params["excess"],product_excess_params["factor"]) for x in excess_input ]

    if (total_revenue_usd != 0) & (total_revenue_usd is not None):
        if excess_option is None:
            if hxd.cds.gl_coverage_selection:
                hx.errors.validation("GL Exposure: Excess/Primary option cannot be left empty!")
    if excess_option == "Excess":
        for item in excess_input_org:
            if item is not None:
                if(item < 1000000) | (item > 30000000):
                    if hxd.cds.gl_coverage_selection:
                        hx.errors.validation("GL Pricing: Excess Of must be between $1m USD and $30m USD!")




    

    ########################################################################
    #  Step 6: Defence Over Limit
    ########################################################################    

    dol_input_org = []
    for item in hxd.cds.layers:
        dol_input_org.append(item.coverages.gl.defence_outside_limit)

    dol_input = []
    dol_input = ["None" if x is None else x for x in dol_input_org]

    # example
    # dol_input = ["500000", "None", "None", "None"]
    
    dol_df = pd.DataFrame({"dol_input": dol_input})
    dol_df = dol_df.merge(dol_params, how = "left", left_on="dol_input", right_on="defence_over_limits")

   # Premium to calculat here for DOL 
    gl_premium_dol_input = [revenue_base_rate*revenue_type_tier_relativity*loss_experience_relativity*x for x in primary_deductible_df["primary_deductible_relativity"]]
    gl_premium_dol_input = [0 if y == 0 else x for (x,y) in zip(gl_premium_dol_input,product_eec_limit) ]

    # Premium before DOL factor
    gl_premium_before_dol = [x*y*z for (x,y,z) in zip(gl_premium_dol_input, limit_eec_agg_relativity ,excess_relativity )]
    dol_default_limit = constants_params[constants_params["name"] == "gl_dol_default_limit"]["factor"].iloc[0]

    dol_limit_factor = product_limit_params[product_limit_params["liability_limits"] == dol_default_limit]["factor"].iloc[0]

    # Premium after DOL factor
    gl_premium_after_dol = [x*dol_limit_factor*z+y for (x,y,z) in zip(gl_premium_dol_input,gl_premium_before_dol, dol_df["factor"] )]
    #load nmp
    gl_premium_after_dol = [x*(1+nmp_load) for x in gl_premium_after_dol]

    ###################################################################################
    #  Additional step to convert all inputs of limits and deductible to local currency
    ##################################################################################
    product_eec_limit_local_currency = [x*ccy_usd_conversion if x is not None else None for x in product_eec_limit_org]
    excess_input_local_currency = [x*ccy_usd_conversion if x is not None else None for x in excess_input_org]
    dol_input_local_currency = [None if ((x == "None") | (x is None)) else float(x.replace(',',''))*ccy_usd_conversion for x in dol_input_org]
    primary_deductible_local_currency = [x*ccy_usd_conversion if x is not None else None for x in primary_deductible_org]

    for index_num, item in enumerate(hxd.cds.layers):
        temp_var = item.coverages.gl
        setattr(temp_var, "limit_local_currency", product_eec_limit_local_currency[index_num])
        setattr(temp_var, "aggregate_limit_local_currency", product_eec_limit_local_currency[index_num])
        setattr(temp_var, "gl_limit_agg_local_currency", product_eec_limit_local_currency[index_num])
        setattr(temp_var, "personal_advertise_limit_agg_local_currency", product_eec_limit_local_currency[index_num])
        setattr(temp_var, "defence_outside_limit_local_currency", dol_input_local_currency[index_num])
        setattr(temp_var, "excess_of_local_currency", excess_input_local_currency[index_num])
        setattr(temp_var, "deductible_local_currency", primary_deductible_local_currency[index_num])
        





    ########################################################################
    #  Step 7: UW judgement
    ########################################################################    

 
    uw_adjustment = hxd.cds.modifiers.gl_uw_adjustment.input_value
    uw_adjustment_org = uw_adjustment
    min_uw_value =  constants_params[constants_params["name"] == "gl_uw_adjustment_min"]["factor"].iloc[0]
    max_uw_value = constants_params[constants_params["name"] == "gl_uw_adjustment_max"]["factor"].iloc[0]
    setattr(hxd.cds.modifiers.gl_uw_adjustment, "min_value", min_uw_value)
    setattr(hxd.cds.modifiers.gl_uw_adjustment, "max_value",max_uw_value )
    setattr(hxd.cds.modifiers.gl_uw_adjustment, "applied_value",min(max(min_uw_value,uw_adjustment),max_uw_value))

    uw_adjustment = getattr(hxd.cds.modifiers.gl_uw_adjustment,"applied_value")

    if uw_adjustment_org is not None:
        if (uw_adjustment_org < min_uw_value) or (uw_adjustment_org  > max_uw_value):
            if hxd.cds.gl_coverage_selection:
                hx.errors.validation("GL Exposure: The Input of UW Judgement is Outside the Range!")



    

    ########################################################################
    #  Step 8: Expected cost
    ########################################################################
    
    # Expected cost before UW adjustment
    gl_expected_cost_before_uw_adjustment = [x*(1-gl_model_brokerage) for x in gl_premium_after_dol]

    # Expected cost after UW adjustment
    gl_expected_cost_after_uw_adjustment = [x*(1+uw_adjustment)*(1-gl_model_brokerage) for x in gl_premium_after_dol]


    ########################################################################
    #  Step 9: Gross Premium
    ########################################################################
    
    gl_brokerage = []
    for item in hxd.cds.layers:
        gl_brokerage.append(item.coverages.gl.brokerage)
    
    gl_brokerage = [0
     if x is None else x for x in gl_brokerage]

    #example
    # gl_brokerage = [0.265, 0.265, 0.265, 0.265]

    # Gross premium before UW adjustment
    gl_gross_premium_before_uw_adjustment = [x/(1-y) for (x,y) in zip(gl_expected_cost_before_uw_adjustment, gl_brokerage)]
    # Gross premium after UW adjustment
    gl_gross_premium_after_uw_adjustment = [x/(1-y) for (x,y) in zip(gl_expected_cost_after_uw_adjustment, gl_brokerage)]


    ########################################################################
    #  Step 10: Minimum Premium
    ########################################################################

    min_premium_df = pd.DataFrame({"product_eec_limit": product_eec_limit})
    # map the tier 9 minimum premium
    min_premium_df= min_premium_df.merge(min_premium_tier_9_params[["liability_limits_eec", "min_premium"]], how = "left", left_on="product_eec_limit", right_on= "liability_limits_eec")
    min_premium_df = min_premium_df.rename({"min_premium": "min_premium_tier_9"}, axis = 1)
    min_premium_df = min_premium_df.drop(["liability_limits_eec"], axis = 1)
    min_premium_df["min_premium_tier_9"] = min_premium_df["min_premium_tier_9"].fillna(0)
    # map the other tiers minimum premium
    # min_premium_df= min_premium_df.merge(min_premium_params, how = "left", left_on="product_eec_limit", right_on= "liability_limit_eec")
    # min_premium_df = min_premium_df.drop(["liability_limit_eec"], axis = 1)

    tier_list = ["tier_"+str(x) for x in range(1,14)]
    for item in tier_list:
        min_premium_df[item] = np.interp(min_premium_df["product_eec_limit"], min_premium_params["liability_limit_eec"], min_premium_params[item])


    # minimum premium from max tiers
    tier_input = ["0" if x is None else x for x in tier_input]
    tier_max = max(tier_input)
    if tier_max != "0":
        tier_max = tier_params[tier_params["tier_description"] ==  tier_max]["tier"].iloc[0]
        min_premium_all_tiers = list(min_premium_df[tier_max])
        min_premium_all_tiers = [0 if x == 0 else y for (x,y) in zip(product_eec_limit, min_premium_all_tiers)]
    else: 
        min_premium_all_tiers = [0 for x in product_eec_limit]

    # minimum premium if tier 9 exists
    min_premium_tier_9 = list(min_premium_df["min_premium_tier_9"])
    
    if tier_9_flag > 0:
        min_premium_final = np.maximum(min_premium_all_tiers, min_premium_tier_9)
    else:
        min_premium_final = min_premium_all_tiers
    
    max_product_eec_limit = min_premium_df["product_eec_limit"].max()
    if (tier_9_flag > 0) & (max_product_eec_limit > 5000000):
        if hxd.cds.gl_coverage_selection:
            hx.errors.validation("Liability Limits EEC Cannot Exceed $5m USD with Tier 9 Exposure!")
    
    for item in min_premium_df["product_eec_limit"]:
        if (tier_9_flag > 0) & (item == 300000):
            if hxd.cds.gl_coverage_selection:
                hx.errors.validation("Liability Limits EEC Cannot be $300k USD with Tier 9 Exposure!")


    ########################################################################
    #  Step 11: Expected claims cost post minimum premium
    ########################################################################

    # Gross Premium before UW adjustment and Post Minimum Premium
    gl_gross_premium_before_uw_adjustment_post_minimum_prem = np.maximum(gl_gross_premium_before_uw_adjustment, min_premium_final)
    # Gross Premium after UW adjustment and Post Minimum Premium
    gl_gross_premium_after_uw_adjustment_post_minimum_prem = np.maximum(gl_gross_premium_after_uw_adjustment, min_premium_final)
    # Gross Premium after UW adjustment and BEFORE Minimum Premium
    gl_gross_premium_after_uw_adjustment_before_minimum_prem = np.array(gl_gross_premium_after_uw_adjustment)

    priced_to_lr = constants_params[constants_params["name"] == "priced_to_lr"]["factor"].iloc[0]

    # Gross Expected claims cost before UW adjustment and Post Minimum Premium
    gl_expected_cost_before_uw_adjustment_post_minimum = [x*(1-y)*priced_to_lr for (x,y) in zip(gl_gross_premium_before_uw_adjustment_post_minimum_prem, gl_brokerage)]
    # Gross Expected claims cost after UW adjustment and Post Minimum Premium
    gl_expected_cost_after_uw_adjustment_post_minimum = [x*(1-y)*priced_to_lr for (x,y) in zip(gl_gross_premium_after_uw_adjustment_post_minimum_prem, gl_brokerage)]
    # Gross Expected claims cost after UW adjustment and BEFORE Minimum Premium
    gl_expected_cost_after_uw_adjustment_before_minimum = [x*(1-y)*priced_to_lr for (x,y) in zip(gl_gross_premium_after_uw_adjustment_before_minimum_prem, gl_brokerage)]

    # output the expected cost
    for item, index_num in zip(hxd.cds.layers, range(0, len(hxd.cds.layers))):
        setattr(getattr(getattr(item, "coverages"), "gl"), "expected_loss_cost_pre_uw_adj_usd", gl_expected_cost_before_uw_adjustment_post_minimum[index_num])
        setattr(getattr(getattr(item, "coverages"), "gl"), "expected_loss_cost_usd", gl_expected_cost_after_uw_adjustment_post_minimum[index_num])
        setattr(getattr(getattr(item, "coverages"), "gl"), "expected_loss_cost_before_minimum_premium_usd", gl_expected_cost_after_uw_adjustment_before_minimum[index_num])
        setattr(getattr(getattr(item, "coverages"), "gl"), "expected_loss_cost_pre_uw_adj", gl_expected_cost_before_uw_adjustment_post_minimum[index_num]*ccy_usd_conversion)
        setattr(getattr(getattr(item, "coverages"), "gl"), "expected_loss_cost", gl_expected_cost_after_uw_adjustment_post_minimum[index_num]*ccy_usd_conversion)
        setattr(getattr(getattr(item, "coverages"), "gl"), "expected_loss_cost_before_minimum_premium", gl_expected_cost_after_uw_adjustment_before_minimum[index_num]*ccy_usd_conversion)   
        setattr(item, "option_selected", item.coverages.gl.option_selected)       

    
    ########################################################################
    #  Step 12: Set up uw notes
    ########################################################################

    hxd.cds.gl_tier_notes.text_box = """
        Products Tier 1
        Electronics NOC/light auto parts/metal goods (load 25%)
        
        Products Tier 2
        Non Comp, Herbal prod except herbal teas and nat. fruit drinks.  
        2 yrs ins history 5 yr clean loss history, unless in business for only 2 yrs.

        Products Tier 3
        Cosmetic skin creams, animal products etc

        Products Tier 4
        CBD Beauty/Cosmetic Creams, Shampoos, and Lotions, Hemp for textiles, Topicals for pain and Salves

        Products Tier 5
        New Ventures ,Non Comp Herbal prod expect herbal teas and nat. fruit drinks.  
        NO 2 yrs ins history, one loss in past 3 yrs under $10K

        Products Tier 6
        Light Machinery and equipment/Pumps/light bio materials,

        Products Tier 7
        Compounded Vitamins, herbal supplements and energy drinks

        Products Tier 8
        Valves/Welding/autoparts

        Products Tier 9
        E Cigs

        Products Tier 10
        CBD Products for pets including treats, Oils/Tinctures, Extracted Oils, Capsules/Tablets, Edibles & drinks

        Products Tier 11
        Construction Equip/Stoves/Heating/Ovens/Mobile equip/guns and sporting goods/Micromobility

        Products Tier 12
        Cutting/heavy machinery/equipment/Railroad/Grinding/Sanding (load 15%)

        Products Tier 13
        Tramps and other extreme entertainment venues, Football and Motorcycle helmets"""

    hxd.cds.gl_tier_notes.stretch_box = False


    #----------------------------------------------------------------------------------------------#
    # Step 13: Validation on status
    #----------------------------------------------------------------------------------------------#

    temp_sum = 0
    temp_sum_option = 0

    for item in hxd.cds.layers:
        section_status = item.coverages.gl.status
        section_reference = item.coverages.gl.section_reference
        section_quoted_prem = item.coverages.gl.quoted_premium
        section_option_selected = item.coverages.gl.option_selected
        if section_status == "Bound":
            temp_sum += 1
            if section_reference is None:
                if hxd.cds.gl_coverage_selection: 
                    hx.errors.validation("GL Pricing Summary: Need to input 'Section Reference' to Bound option! ")
            else:
                if len(section_reference) > 20:
                    if hxd.cds.gl_coverage_selection:
                        hx.errors.validation("GL Pricing Summary: 'Section Reference' cannot exceed 20 characters! ")
            if section_quoted_prem is None:
                if hxd.cds.gl_coverage_selection:
                    hx.errors.validation("GL Pricing Summary: Need to enter Quoted Premium for Bound option! ")
            if section_option_selected == "No":
                if hxd.cds.gl_coverage_selection:
                    hx.errors.validation("GL Pricing Summary: Select 'Yes' for Bound option!")
        if section_status == "Quoted":
            if section_quoted_prem is None:
                if hxd.cds.gl_coverage_selection: 
                    hx.errors.validation("GL Pricing Summary: Need to enter Quoted Premium for Quoted option! ")     
        if section_option_selected == "Yes":
            temp_sum_option += 1        

    
    if temp_sum > 1:
        if hxd.cds.gl_coverage_selection:
            hx.errors.validation("GL Coverage: Can Only Bound 1 Option!")
    if temp_sum_option > 1:
        if hxd.cds.gl_coverage_selection:
            hx.errors.validation("GL Coverage: Can Only Select 1 Option!")
        
    if hxd.cds.gl_coverage_selection == True:
        if total_revenue == 0:
            hx.errors.validation("GL Coverage: Need to Input revenue in the 'Reveneue Tiers' section!")








  








    pass