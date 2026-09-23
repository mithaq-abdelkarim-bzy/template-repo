######################################################################################
# This is the pricing code for E&O Coverage
######################################################################################
import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
#from algorithms.rate_constants import eo_reinstatement_factor, eo_fees_scale, eo_territory_scale
from operator import itemgetter



def rate_pricing_eo(hxd):

    #get the rater constants
    eo_constants = hx.params.table_constants
    eo_reinstatement_factor = eo_constants[eo_constants["name"] == "eo_reinstatement"]["factor"].iloc[0]
    eo_fees_scale_1 = eo_constants[eo_constants["name"] == "eo_fees_scale_1"]["factor"].iloc[0]
    eo_fees_scale_2 = eo_constants[eo_constants["name"] == "eo_fees_scale_2"]["factor"].iloc[0]
    eo_fees_scale_benchmark = eo_constants[eo_constants["name"] == "eo_fees_scale_benchmark"]["factor"].iloc[0]
    eo_territory_scale = eo_constants[eo_constants["name"] == "eo_territory_scale"]["factor"].iloc[0]
    eo_priced_lr = eo_constants[eo_constants["name"] == "priced_to_lr"]["factor"].iloc[0]
    eo_model_brokerage = eo_constants[eo_constants["name"] == "model_brokerage"]["factor"].iloc[0]
    eo_total_fees = hxd.cds.exposure.aggregate.eo_total_fees
    # get all the parameters 
    discipline_list = hx.params.table_eo_discipline["discipline_name"]
    discpline_params = hx.params.table_eo_discipline
    ae_operation_list = hx.params.table_eo_ae_operation["ae_operations_name"]
    ae_operation_params = hx.params.table_eo_ae_operation
    territory_params = hx.params.table_eo_territory
    fee_size_params = hx.params.table_eo_fee_size
    limit_params = hx.params.table_eo_limit
    deductible_params = hx.params.table_eo_retention
    prior_knowlege_params = hx.params.table_eo_prior_knowledge
    insurance_history_params = hx.params.table_eo_insurance_history
    claim_history_params = hx.params.table_eo_claim_history
    cost_include_params = hx.params.table_eo_cost_included
    program_modifier_params = hx.params.table_eo_program_modifier
    eo_minimum_prem_params = hx.params.table_eo_minimum_premium
    profession_params = hx.params.table_eo_profession
    tp_params = hx.params.table_tp_parameters
    nmp_load = tp_params[tp_params["business_plan_class"] =="International Specialty Programmes" ]["nmp_load"].iloc[0]
    # nmp_load = 0



    # get the conversion rate from ccy to usd
    #xe_table = params.fx_rates.df()
    xe_table = hx.params.table_fx_rates
    ccy_usd_conversion =xe_table[xe_table["ccy"] == hxd.cds.currencies.source_currency]["fx_rate"].iloc[0]/ xe_table[xe_table["ccy"] == "USD"]["fx_rate"].iloc[0]


    #----------------------------------------------------------------------------------------------#
    #step 0: Get the profession number
    #----------------------------------------------------------------------------------------------#

    #get the profession number
    profession_text  = hxd.cds.exposure.granular.eo_profession

    # Default to empty
    if profession_text == None:
         profession_num = 999 
         hxd.cds.exposure.granular.eo_exposure_shownby = False
    else:
        profession_num = profession_params[profession_params["profession"] == profession_text]["mapping"].iloc[0]
        hxd.cds.exposure.granular.eo_exposure_shownby = True
    # output the shown by to the A&E operation table
    hxd.cds.exposure.granular.eo_ae_operaion_shownby = (profession_num == 2)
    
    #----------------------------------------------------------------------------------------------#
    #step 1: Base Rater: calculate the weigthed base rate of discipline
    #----------------------------------------------------------------------------------------------#

    #example here
    #eo_total_fees = 79800
    #ccy_usd_conversion = 0.90452
    eo_total_fees_usd = eo_total_fees/ccy_usd_conversion
    eo_fees_max = eo_constants[eo_constants["name"] == "eo_fees_max"]["factor"].iloc[0]

    # if eo_total_fees_usd > eo_fees_max :
    #     eo_total_fees_usd = eo_fees_max -1 
    #     hx.errors.validation("E&O Exposure: The total fees must be less than " + str(eo_fees_max) + "(USD)")

    # get the fees percentage input from the UI
    input_fees = [getattr(getattr(hxd.cds.exposure.granular, item), "input_pct") for item in discipline_list]
    # create a pandas table
    discipline_df = pd.DataFrame({"discipline": discipline_list, "input_pct": input_fees})
    #example here
    #discipline_df.at[33, "input_pct"] = 1

    # create a new column for weighted fees
    discipline_df["weighted_fee"] = discipline_df["input_pct"] * eo_total_fees_usd
    # map the relativity
    discipline_df = discipline_df.merge( discpline_params, how = "left", left_on = "discipline", right_on = "discipline_name")
    # calculate the base rate for each discipline and the total base rate
    discipline_df["base_rate"] =  discipline_df["weighted_fee"] * discipline_df["factor"] 
    eo_total_base_rate = discipline_df["base_rate"].sum()/100

    hxd.cds.exposure.granular.eo_total_base_rate_relativity = eo_total_base_rate

    discipline_df["profession_bool"] = discipline_df["profession"] == profession_num
    
    # export the relativity of the discipline
    for item in  discipline_list:
        filtered_discipline_df = discipline_df[discipline_df["discipline"] == item]
        setattr(getattr(hxd.cds.exposure.granular , item ), "relativity",filtered_discipline_df["factor"].iloc[0] ) 
        setattr(getattr(hxd.cds.exposure.granular , item ), "show_row", filtered_discipline_df["profession_bool"].iloc[0] )    

    hxd.cds.exposure.granular.eo_total_fees_pct = discipline_df["input_pct"].sum()   
    
    if (eo_total_fees != 0) & (abs(discipline_df["input_pct"].sum() - 1.00) > 0.00001) :
        hx.errors.validation("E&O Exposure: The total exposure percentage is not 100%")
    

    #----------------------------------------------------------------------------------------------#
    # Step 2: get the operation relativity - only for A&E
    #----------------------------------------------------------------------------------------------#

    input_fees = [getattr(getattr(hxd.cds.exposure.granular , item ), "input_pct") for item in ae_operation_list]
    # create a pandas table
    ae_operation_df = pd.DataFrame({"ae_operation": ae_operation_list, "input_pct": input_fees})
    # map the relativity
    ae_operation_df = ae_operation_df.merge(ae_operation_params, how = "left", left_on = "ae_operation", right_on = "ae_operations_name")
    #calculate the relativity
    ae_operation_df["weighted_relativity"] = ae_operation_df["input_pct"] * ae_operation_df["factor"]

    if profession_num ==2:
        ae_operate_relativity =  ae_operation_df["weighted_relativity"].sum()
    else:
        # for other professions the default is 1
        ae_operate_relativity = 1    

    #show and hide the rows
    ae_operation_df["profession_bool"] = ae_operation_df["profession"] == profession_num

    # export relativity of the A&E operations
    for item in ae_operation_list:
        filtered_ae_operation_df = ae_operation_df[ae_operation_df["ae_operation"] == item]
        setattr(getattr(hxd.cds.exposure.granular , item ), "relativity", filtered_ae_operation_df["factor"].iloc[0])
        setattr(getattr(hxd.cds.exposure.granular , item ), "show_row", filtered_ae_operation_df["profession_bool"].iloc[0] ) 

    hxd.cds.exposure.granular.eo_ae_operation_pct =  ae_operation_df["input_pct"].sum()
    # if((ae_operation_df["input_pct"].sum() != 0) & (ae_operation_df["input_pct"].sum() != 1) ):
    if((profession_num == 2) & (eo_total_fees != 0) & (abs(ae_operation_df["input_pct"].sum() - 1.00) > 0.00001)):
        hx.errors.validation("E&O Exposure: The total A&E operation percentage is not 100%")

    #----------------------------------------------------------------------------------------------#
    # Step 3: get the territory relativity
    #----------------------------------------------------------------------------------------------#    
    if hxd.cds.rating_factors.eo_territory.input_value == None:
        eo_territory_relativity = 1
    else:
        eo_territory_relativity = territory_params[territory_params["territory"] == hxd.cds.rating_factors.eo_territory.input_value]["factor"].iloc[0]
    
    hxd.cds.rating_factors.eo_territory.relativity = eo_territory_relativity

    if (eo_total_fees != 0) & (hxd.cds.rating_factors.eo_territory.input_value == None) :
        hx.errors.validation("E&O Exposure: Territory cannot be left empty!")

    #----------------------------------------------------------------------------------------------#
    # Step 4: get the fee size relativity
    #----------------------------------------------------------------------------------------------#
    
    #eo_total fees territory adjusted
    eo_total_fees_usd_adj = eo_total_fees_usd/eo_territory_relativity

    if eo_total_fees_usd_adj >= eo_fees_max:
        filtered_fee_size_df = fee_size_params[fee_size_params["x_lower"] == eo_fees_max]
        size_relativity = 1 - filtered_fee_size_df["y_lower"].iloc[0]/100
    else:
        filtered_fee_size_df = fee_size_params[(fee_size_params["x_lower"] <= eo_total_fees_usd_adj) & (fee_size_params["x_upper"] > eo_total_fees_usd_adj)]
        size_x_lower = filtered_fee_size_df["x_lower"].iloc[0]
        size_x_upper = filtered_fee_size_df["x_upper"].iloc[0]
        size_y_lower = filtered_fee_size_df["y_lower"].iloc[0]
        size_y_upper = filtered_fee_size_df["y_upper"].iloc[0]
        size_relativity = 1- np.interp(eo_total_fees_usd_adj, [size_x_lower, size_x_upper], [size_y_lower, size_y_upper])/100

    hxd.cds.rating_factors.eo_size_relativity = size_relativity

    #----------------------------------------------------------------------------------------------#
    # Step 5: Get the limit relativity
    #----------------------------------------------------------------------------------------------#
    layer_number = len(hxd.cds.layers)
    eo_limit = [getattr(getattr(getattr(item, "coverages"), "eo") , "limit") for item in hxd.cds.layers]
    #eo_agg_limit = [getattr(getattr(getattr(item, "coverages"), "eo"), "aggregate_limit") for item in hxd.cds.layers]
    # default aggregate limit to be the EEC limit 
    [setattr(getattr(getattr(getattr(item, "coverages"), "eo"), "aggregate_limit"), "calculated", eec_limit) for (item, eec_limit) in zip(hxd.cds.layers, eo_limit)]
    eo_agg_limit = [getattr(getattr(getattr(getattr(item, "coverages"), "eo"), "aggregate_limit"), "selected") for item in hxd.cds.layers]

    #example data- to delete
    #eo_limit = [1000000, 1500000, 2000000, 1000000]
    #eo_agg_limit = [1000000,3000000,6000000,1000000]
    #eo_deductible = [5000, 6000, 10000,5000]
    #eo_territory_relativity = 0.8
    #Each and Every Limit and Reinstatement relativity
    eo_limit = [item if item is not None else 0 for item in eo_limit]
    eo_limit_usd = eo_limit / ccy_usd_conversion
    eo_agg_limit = [item if item is not None else 0 for item in eo_agg_limit]
    eo_agg_limit_usd = eo_agg_limit/ ccy_usd_conversion



    # Find out the limit factors
    eo_limit_index = []
    limit_params_row = limit_params.shape[0]
    limit_params_last_row = limit_params.iloc[limit_params_row-1,]
    for item in range(0,len(eo_limit_usd)):
        if(eo_limit_usd[item] >= 10000000):
            eo_limit_index.append(limit_params_last_row["x_lower"])
        elif(eo_limit_usd[item] < 0 ):
            eo_limit_index.append(0)
        else:
            eo_limit_index.append(limit_params[(limit_params["x_lower"] <= eo_limit_usd[item]) & (limit_params["x_uppwer"] > eo_limit_usd[item])]["x_lower"].iloc[0])
    
    eo_limit_index = pd.DataFrame({"eo_limit_usd": eo_limit_usd, "eo_limit_index": eo_limit_index, "eo_agg_limit": eo_agg_limit_usd})
    # vlookup the relativities for lower and upper limit bounds
    eo_limit_rel = pd.merge(eo_limit_index, limit_params, how = "left", left_on = "eo_limit_index", right_on= "x_lower")
    #eo_limit_rel["eec_limit_factor"] = eo_limit_rel.apply(lambda row: np.interp(row.eo_limit_usd, [row.x_lower, row.x_uppwer], [row.y_lower, row.y_upper]), axis = 1)
    eo_limit_rel["eec_limit_factor"] = eo_limit_rel["y_lower"] + ((eo_limit_rel["eo_limit_usd"] - eo_limit_rel["x_lower"])/(eo_limit_rel["x_uppwer"]-eo_limit_rel["x_lower"]))*(eo_limit_rel["y_upper"] - eo_limit_rel["y_lower"])
    #reinstatement releativity: set up in constant value as a parameter
    eo_limit_rel["reinstatement_factor"] = np.where(((eo_agg_limit_usd == 0) | (eo_agg_limit_usd == None)), eo_reinstatement_factor, 1)

    for index_num, item in zip(range(0, len(hxd.cds.layers)), hxd.cds.layers):
        item.coverages.eo.limit_relativity = eo_limit_rel["eec_limit_factor"].iloc[index_num] * eo_limit_rel["reinstatement_factor"].iloc[index_num]

    for item in eo_limit_usd:
        if item < 0:
            hx.errors.validation("E&O Pricing: Each and Every Limit Cannot be Negative!")
        if item > 10000000:
            hx.errors.validation("E&O Pricing: Each and Every Limit Cannot Exceed $10m USD")

    for item in eo_agg_limit:
        if item < 0:
            hx.errors.validation("E&O Pricing: Aggregate Limit Cannot be Negative!")
    #----------------------------------------------------------------------------------------------#
    # Step 6: Get Retention/Deductible relativity
    #----------------------------------------------------------------------------------------------#
    if eo_total_fees_usd <= eo_fees_scale_benchmark:
        eo_fees_scale = eo_fees_scale_1
    else:
        eo_fees_scale = eo_fees_scale_2

    guideline_deductible_calc = max(eo_fees_scale * eo_total_fees_usd, eo_territory_relativity*eo_territory_scale)
    #guideline_deductible_calc is in USD
    guideline_deductible_calc_local_ccy = guideline_deductible_calc * ccy_usd_conversion

    for item, index_num in zip(hxd.cds.layers, range(len(hxd.cds.layers))):
        if item.coverages.eo.limit  == None:
            setattr(getattr(getattr(item, "coverages"), "eo") , "guideline_deductible", None)
        else:
            setattr(getattr(getattr(item, "coverages"), "eo"), "guideline_deductible", guideline_deductible_calc_local_ccy)

    #set deudctible t obe guideline deductible
    #eo_deductible = [getattr(getattr(getattr(item, "coverages"), "eo") , "deductible") for item in hxd.cds.layers ]
    [setattr(getattr(getattr(getattr(item, "coverages"), "eo") , "deductible"), "calculated", item.coverages.eo.guideline_deductible) for item in hxd.cds.layers ]
    eo_deductible = [getattr(getattr(getattr(getattr(item, "coverages"), "eo") , "deductible"), "selected") for item in hxd.cds.layers ]
    eo_deductible = [item if item is not None else 0 for item in eo_deductible]
    eo_deductible_usd = eo_deductible / ccy_usd_conversion

    eo_deductible_rel = pd.DataFrame({"eo_deductible": eo_deductible_usd})
    eo_deductible_rel["guideline_deductible"] = guideline_deductible_calc
    eo_deductible_rel["reinstatement"] = np.where(eo_deductible_rel["guideline_deductible"] > 0, eo_deductible_rel["eo_deductible"] / eo_deductible_rel["guideline_deductible"], 1.0)
    eo_deductible_rel["reinstatement"] = np.where(eo_deductible_rel["reinstatement"] >= 9999,9999,eo_deductible_rel["reinstatement"])
    # eo_deductible_rel["layer_label"] = np.arange(eo_deductible_rel.shape[0])
    # #vlook up the relativity for retention. No interpolation. Need to sort the left table deductible value
    # eo_deductible_rel = pd.merge_asof(eo_deductible_rel.sort_values("reinstatement"), deductible_params, left_on= "reinstatement", right_on= "x_upper", direction = "forward")
    # eo_deductible_rel = eo_deductible_rel.sort_values("layer_label")
    # eo_deductible_rel = eo_deductible_rel.set_index("layer_label")
    # eo_deductible_rel.rename(columns = {"factor": "deductible_index"}, inplace=True)


    eo_deductible_index = []
    for index, item in enumerate( eo_deductible_rel["reinstatement"]):
        filted_deductible_paramter = deductible_params[item >= deductible_params["x_lower"]].iloc[-1]
        eo_deductible_val = filted_deductible_paramter["factor"]
        eo_deductible_index.append(eo_deductible_val)
    
    eo_deductible_rel["deductible_index"] = eo_deductible_index


    
    for index_num, item in zip(range(0, len(hxd.cds.layers)), hxd.cds.layers):
        item.coverages.eo.deductible_relativity = eo_deductible_rel["deductible_index"].iloc[index_num]

    for item in eo_deductible_usd:
        if item < 0:
            hx.errors.validation("E&O Pricing: Retention Cannot be Negative!")

    #----------------------------------------------------------------------------------------------#
    # Step 7: Get other relativities
    #----------------------------------------------------------------------------------------------#
    # prior knowledge relativity
    eo_priorknowledge = hxd.cds.rating_factors.eo_prior_knowledge.input_value
    if eo_priorknowledge == None:
        eo_priorknowledge_rel = 1
    else:
        eo_priorknowledge_rel =  prior_knowlege_params[prior_knowlege_params["prior_knowledge"] == eo_priorknowledge]["factor"].iloc[0]
    hxd.cds.rating_factors.eo_prior_knowledge.relativity = eo_priorknowledge_rel


   # cost included relativity
    eo_costincluded = hxd.cds.rating_factors.eo_cost_included.input_value
    if eo_costincluded == None:
        eo_costincluded_rel = 1
    else:
        eo_costincluded_rel = cost_include_params[cost_include_params["cost_included"] == eo_costincluded]["factor"].iloc[0]
    hxd.cds.rating_factors.eo_cost_included.relativity = eo_costincluded_rel

    if (eo_total_fees != 0) &  (eo_costincluded is None):
        hx.errors.validation("E&O Exposure: Cost Included cannot be left empty!")
    
    # prorata relativity: the rater only write annual policies
    eo_prorata_rel  = 1


    #----------------------------------------------------------------------------------------------#
    # Step 8: Get all the subjective relativites
    #----------------------------------------------------------------------------------------------#

    #Insurance history relativity
    eo_insurancehistory =  hxd.cds.modifiers.eo_insurance_history.input_value
    if eo_insurancehistory == None:
        hxd.cds.modifiers.eo_insurance_history.min_rel = 1
        hxd.cds.modifiers.eo_insurance_history.max_rel = 1
        hxd.cds.modifiers.eo_insurance_history.default_rel = 1
    else:
        hxd.cds.modifiers.eo_insurance_history.min_rel = insurance_history_params[insurance_history_params["insurance_history_list"] == eo_insurancehistory]["lower_bound"].iloc[0]
        hxd.cds.modifiers.eo_insurance_history.max_rel = insurance_history_params[insurance_history_params["insurance_history_list"] == eo_insurancehistory]["upper_bound"].iloc[0]
        hxd.cds.modifiers.eo_insurance_history.default_rel = insurance_history_params[insurance_history_params["insurance_history_list"] == eo_insurancehistory]["default"].iloc[0]
        hxd.cds.modifiers.eo_insurance_history.output_class = insurance_history_params[insurance_history_params["insurance_history_list"] == eo_insurancehistory]["insurance_history_respond"].iloc[0]

    eo_insurancehistory_rel_input = hxd.cds.modifiers.eo_insurance_history.input_rel
    if eo_insurancehistory_rel_input == None:
        eo_insurancehistory_rel = hxd.cds.modifiers.eo_insurance_history.default_rel
    else:
        eo_insurancehistory_rel = min(max(hxd.cds.modifiers.eo_insurance_history.min_rel,eo_insurancehistory_rel_input ), hxd.cds.modifiers.eo_insurance_history.max_rel)
    
    hxd.cds.modifiers.eo_insurance_history.applied_rel = eo_insurancehistory_rel

    if eo_insurancehistory_rel_input is not None:
        if((eo_insurancehistory_rel_input < hxd.cds.modifiers.eo_insurance_history.min_rel) | (eo_insurancehistory_rel_input > hxd.cds.modifiers.eo_insurance_history.max_rel)):
            if hxd.cds.eo_coverage_selection:
                hx.errors.validation("E&O Exposure: The insurance history is outside the bound")
    if (eo_total_fees != 0) &  (eo_insurancehistory is  None):
        if hxd.cds.eo_coverage_selection:
            hx.errors.validation("E&O Exposure: Insurance History cannot be left empty!")

    #Claim history relativity
    eo_claimhistory =  hxd.cds.modifiers.eo_claim_history.input_value
    #eo_claimhistory = "None"
    if eo_claimhistory == None:
        hxd.cds.modifiers.eo_claim_history.min_rel = 1
        hxd.cds.modifiers.eo_claim_history.max_rel = 1
        hxd.cds.modifiers.eo_claim_history.default_rel = 1
    else:
        hxd.cds.modifiers.eo_claim_history.min_rel = claim_history_params[claim_history_params["claim_history"] == eo_claimhistory]["lower_bound"].iloc[0]
        hxd.cds.modifiers.eo_claim_history.max_rel = claim_history_params[claim_history_params["claim_history"] == eo_claimhistory]["upper_bound"].iloc[0]
        hxd.cds.modifiers.eo_claim_history.default_rel = claim_history_params[claim_history_params["claim_history"] == eo_claimhistory]["default"].iloc[0]
    
    eo_claimhistory_rel_input = hxd.cds.modifiers.eo_claim_history.input_rel
    if eo_claimhistory_rel_input == None:
        eo_claimhistory_rel = hxd.cds.modifiers.eo_claim_history.default_rel 
    else:
        eo_claimhistory_rel = min(max(eo_claimhistory_rel_input, hxd.cds.modifiers.eo_claim_history.min_rel),hxd.cds.modifiers.eo_claim_history.max_rel)

    hxd.cds.modifiers.eo_claim_history.applied_rel = eo_claimhistory_rel

    if eo_claimhistory_rel_input is not None:
        if((eo_claimhistory_rel_input < hxd.cds.modifiers.eo_claim_history.min_rel) | (eo_claimhistory_rel_input > hxd.cds.modifiers.eo_claim_history.max_rel) ):
            if hxd.cds.eo_coverage_selection:
                hx.errors.validation("E&O Exposure: The claim history is outside the bound")


    #program modifier
    hxd.cds.modifiers.eo_schedule_modifier.min_rel = program_modifier_params["lower_bound"].iloc[0]
    hxd.cds.modifiers.eo_schedule_modifier.max_rel = program_modifier_params["upper_bound"].iloc[0]
    eo_program_modifier_rel = min(max(hxd.cds.modifiers.eo_schedule_modifier.input_value, hxd.cds.modifiers.eo_schedule_modifier.min_rel),hxd.cds.modifiers.eo_schedule_modifier.max_rel)
    hxd.cds.modifiers.eo_schedule_modifier.applied_rel  =  eo_program_modifier_rel

    eo_program_modifier_rel_input = hxd.cds.modifiers.eo_schedule_modifier.input_value
    if eo_program_modifier_rel_input is not None: 
        if((eo_program_modifier_rel_input  < hxd.cds.modifiers.eo_schedule_modifier.min_rel) | (eo_program_modifier_rel_input > hxd.cds.modifiers.eo_schedule_modifier.max_rel)):
            if hxd.cds.eo_coverage_selection:
                hx.errors.validation("E&O Exposure: The program modifier is outside the bound")
    
    #combine all the subjective relativity
    eo_total_subjective_rel = eo_insurancehistory_rel*eo_claimhistory_rel*(1+eo_program_modifier_rel)



    #----------------------------------------------------------------------------------------------#
    # Step 9: Calculate the expected cost BEFORE UW adjustment
    #----------------------------------------------------------------------------------------------#
    eo_prem_before_uwadj = eo_limit_rel["eec_limit_factor"].multiply(eo_limit_rel["reinstatement_factor"], axis = 0)
    eo_prem_before_uwadj = eo_prem_before_uwadj.multiply(eo_deductible_rel["deductible_index"])
    eo_prem_before_uwadj = eo_prem_before_uwadj.multiply(eo_total_base_rate)
    # 1+ ae operation relativity
    eo_prem_before_uwadj = eo_prem_before_uwadj.multiply(ae_operate_relativity)
    eo_prem_before_uwadj = eo_prem_before_uwadj.multiply(size_relativity)
    eo_prem_before_uwadj = eo_prem_before_uwadj.multiply(eo_territory_relativity)
    eo_prem_before_uwadj = eo_prem_before_uwadj.multiply(eo_priorknowledge_rel)
    eo_prem_before_uwadj = eo_prem_before_uwadj.multiply(eo_costincluded_rel)
    #load the nmp
    eo_prem_before_uwadj_incl_nmp = eo_prem_before_uwadj.multiply(1+nmp_load)

    #minimum premium
    eo_minimum_prem = []
    last_row_min_prem = eo_minimum_prem_params.shape[0]
    eo_minimum_prem_last_row = eo_minimum_prem_params.iloc[last_row_min_prem-1,:]
    max_limit_temp = eo_minimum_prem_last_row["x_upper"]
    max_limit_min_prem_temp = eo_minimum_prem_last_row["minimum_prem"]
    min_limit_temp = eo_minimum_prem_params.iloc[0,0]
    min_limit_min_prem_temp = eo_minimum_prem_params.loc[0, "minimum_prem"]

    for index_num in range( len(eo_limit)):
        if (eo_limit_usd[index_num] < min_limit_temp ):
            eo_minimum_prem.append(min_limit_min_prem_temp)
        elif (eo_limit_usd[index_num] >= max_limit_temp):
            eo_minimum_prem.append(max_limit_min_prem_temp)
        else:
            eo_minimum_prem.append(eo_minimum_prem_params[(eo_minimum_prem_params["x_lower"] <= eo_limit_usd[index_num]) & (eo_minimum_prem_params["x_upper"] > eo_limit_usd[index_num])]["minimum_prem"].iloc[0] )
    eo_minimum_prem = pd.Series(eo_minimum_prem)
    eo_minimum_prem_usd = eo_minimum_prem/ccy_usd_conversion
    # eo_minimum_prem_usd = eo_minimum_prem
    #post minimum premium
    eo_prem_before_uwadj_post_minimum = np.maximum(eo_prem_before_uwadj_incl_nmp  , eo_minimum_prem_usd)

    #get the final claims expected cost 
    eo_claims_cost_before_uwadj = eo_prem_before_uwadj_post_minimum * (1- eo_model_brokerage) * eo_priced_lr


    for item, index_number in zip(hxd.cds.layers, range(layer_number)):
        setattr(item.coverages.eo, "expected_loss_cost_pre_uw_adj_usd", eo_claims_cost_before_uwadj[index_number])
        setattr(item.coverages.eo, "expected_loss_cost_pre_uw_adj", eo_claims_cost_before_uwadj[index_number]*ccy_usd_conversion)



    #----------------------------------------------------------------------------------------------#
    # Step 10: Calculate the expected cost After UW adjustment
    #----------------------------------------------------------------------------------------------#

    eo_prem_after_uwadj = eo_prem_before_uwadj.multiply(eo_total_subjective_rel)
    #load nmp
    eo_prem_after_uwadj_incl_nmp = eo_prem_after_uwadj.multiply(1+nmp_load)
    eo_prem_after_uwadj_post_minimum = np.maximum(eo_prem_after_uwadj_incl_nmp  , eo_minimum_prem_usd)
    #get the final claims expected cost
    eo_claims_cost_after_uwadj_before_minimum_premium = eo_prem_after_uwadj_incl_nmp* (1- eo_model_brokerage) * eo_priced_lr
    eo_claims_cost_after_uwadj = eo_prem_after_uwadj_post_minimum * (1- eo_model_brokerage) * eo_priced_lr    

    for item, index_number in zip(hxd.cds.layers, range(layer_number)):
        setattr(item.coverages.eo, "expected_loss_cost_usd", eo_claims_cost_after_uwadj[index_number])
        setattr(item.coverages.eo, "expected_loss_cost", eo_claims_cost_after_uwadj[index_number]*ccy_usd_conversion)
        setattr(item.coverages.eo, "expected_loss_cost_before_minimum_premium_usd", eo_claims_cost_after_uwadj_before_minimum_premium[index_number])
        setattr(item.coverages.eo, "expected_loss_cost_before_minimum_premium", eo_claims_cost_after_uwadj_before_minimum_premium[index_number]*ccy_usd_conversion)
        setattr(item, "option_selected", item.coverages.eo.option_selected)


    #----------------------------------------------------------------------------------------------#
    # Step 11: Validation on status
    #----------------------------------------------------------------------------------------------#

    temp_sum = 0
    temp_sum_option = 0

    for item in hxd.cds.layers:
        section_status = item.coverages.eo.status
        section_reference = item.coverages.eo.section_reference
        section_quoted_prem = item.coverages.eo.quoted_premium
        section_option_selected = item.coverages.eo.option_selected
        if section_status == "Bound":
            temp_sum += 1
            if section_reference is None:
                if hxd.cds.eo_coverage_selection:
                    hx.errors.validation("EO Pricing Summary: Need to input 'Section Reference' to Bound option! ")
            else:
                if len(section_reference) > 20:
                    if hxd.cds.eo_coverage_selection:
                        hx.errors.validation("EO Pricing Summary: 'Policy Section Reference' cannot exceed 20 characters! ")
            if section_quoted_prem is None:
                if hxd.cds.eo_coverage_selection:
                    hx.errors.validation("EO Pricing Summary: Need to enter Quoted Premium for Bound option! ")
            if section_option_selected == "No":
                if hxd.cds.eo_coverage_selection:
                    hx.errors.validation("EO Pricing Summary: Select 'Yes' for Bound option!")

        if section_status == "Quoted":
            if section_quoted_prem is None:
                if hxd.cds.eo_coverage_selection:
                    hx.errors.validation("EO Pricing Summary: Need to enter Quoted Premium for Quoted option! ")    
        if section_option_selected == "Yes":
            temp_sum_option += 1    
    
    if temp_sum > 1:
        if hxd.cds.eo_coverage_selection:
            hx.errors.validation("EO Coverage: Can Only Bound 1 Option!")
    
    if temp_sum_option > 1:
        if hxd.cds.eo_coverage_selection:
            hx.errors.validation("EO Coverage: Can Only Select 1 Option!")
    
    if hxd.cds.eo_coverage_selection == True:
        if eo_total_fees == 0:
            if hxd.cds.eo_coverage_selection:
                hx.errors.validation("EO Coverage: Need to Input the 'Total Fees' in the 'Exposure Information' section!")
    

    

        
        
    
    

    


    
    













    


    pass