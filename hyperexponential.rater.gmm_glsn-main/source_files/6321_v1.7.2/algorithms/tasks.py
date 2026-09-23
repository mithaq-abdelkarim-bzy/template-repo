import hx
import os
import pandas as pd
import numpy as np
import requests
import json
import math
import copy
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
from algorithms.rate_rate_change import rate_change_buckets
from algorithms.rationale_proposal_templates.primary_proposal import primary_email_generation
from algorithms.rationale_proposal_templates.excess_proposal import excess_email_generation
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from algorithms.rate_change import RateChange as RateChangeLib
from datetime import datetime
### --- EMAIL EXAMPLE --- ###
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import policy
from email.generator import BytesGenerator
import time
from libraries.email_notification.algorithms.bug_report import send_bug_report, new_bug_report, cancel_bug_report, generate_bug_report, add_additional_file
import re
from html.parser import HTMLParser

# Update example task below 
@hx.task
def venue_factors_select_all(hxd, progress):
    cds = hxd.cds
    
    venue_us_list = hx.params.table_venue_us["venue_name"]
    venue_international_list = hx.params.table_venue_international["venue_name"]
    
    if cds.international_masking == True:
        venue_international_params = hx.params.table_venue_international
        venue_international_list = hx.params.table_venue_international["venue_name"]
        venue_international_selection = []

        for item in  venue_international_list:
            setattr(getattr(hxd.cds.exposure.granular , item ), "selection", True)
            venue_international_selection.append(True)
        
        venue_international_df = pd.DataFrame({"venue_international": venue_international_list,"selection": venue_international_selection})
        venue_international_df["percentage"] = 1 / (venue_international_df["selection"].sum())

        venue_international_df = venue_international_df.merge( venue_international_params, how = "left", left_on = "venue_international", right_on = "venue_name")

        total_venue_international_factor = (venue_international_df["percentage"] * venue_international_df["factor"] * venue_international_df["selection"]).sum()
 
            

    if cds.us_masking == True:
        venue_us_params = hx.params.table_venue_us
        venue_us_list = hx.params.table_venue_us["venue_name"]
        venue_us_selection = []

        for item in  venue_us_list:
            if item == "international":
                setattr(getattr(hxd.cds.exposure.granular , item ), "selection", False)
                venue_us_selection.append(False)
            else:
                setattr(getattr(hxd.cds.exposure.granular , item ), "selection", True)
                venue_us_selection.append(True)
            
        
        venue_us_df = pd.DataFrame({"venue_us": venue_us_list,"selection": venue_us_selection})
        venue_us_df["percentage"] = 1 / (venue_us_df["selection"].sum())

        venue_us_df = venue_us_df.merge( venue_us_params, how = "left", left_on = "venue_us", right_on = "venue_name")

        total_venue_us_factor = (venue_us_df["percentage"] * venue_us_df["factor"] * venue_us_df["selection"]).sum()
        
        for item in  venue_us_list:
            if item == "international":
                setattr(getattr(hxd.cds.exposure.granular , item ),"percentage",0)
            else:
                setattr(getattr(hxd.cds.exposure.granular , item ),"percentage", venue_us_df[venue_us_df["venue_us"] == item]["percentage"].iloc[0])  


    for index, item in  enumerate(venue_us_list):
        setattr(getattr(hxd.cds.exposure.granular , item ), "override_flag", False )   
        temp_value = getattr(getattr(hxd.cds.exposure.granular , item), "percentage" )
        setattr(getattr(hxd.cds.exposure.granular , item ), "percentage_async_copy",temp_value  )      
    for index, item in  enumerate(venue_international_list):
        setattr(getattr(hxd.cds.exposure.granular , item ), "override_flag",False ) 
        temp_value = getattr(getattr(hxd.cds.exposure.granular , item), "percentage" )
        setattr(getattr(hxd.cds.exposure.granular , item ), "percentage_async_copy",temp_value  )                             
              
    pass

@hx.task
def venue_factors_clear_all(hxd, progress):
    cds = hxd.cds
    
    venue_international_list = hx.params.table_venue_international["venue_name"]
    venue_us_list = hx.params.table_venue_us["venue_name"]

    if cds.international_masking == True:
            for item in  venue_international_list:
                setattr(getattr(hxd.cds.exposure.granular , item ), "selection", False)
                setattr(getattr(hxd.cds.exposure.granular , item ), "percentage", 0)

    if cds.us_masking == True:
            for item in  venue_us_list:
                setattr(getattr(hxd.cds.exposure.granular , item ), "selection", False) 
                setattr(getattr(hxd.cds.exposure.granular , item ), "percentage", 0)  
    #set up override to default false
    for index, item in  enumerate(venue_us_list):
        setattr(getattr(hxd.cds.exposure.granular , item ), "override_flag",False )
    for index, item in  enumerate(venue_international_list):
        setattr(getattr(hxd.cds.exposure.granular , item ), "override_flag", False )             
                
    pass

@hx.task
def venue_factors_override_flag(hxd, progress):
    cds = hxd.cds
    venue_us_list = hx.params.table_venue_us["venue_name"]
    venue_international_list = hx.params.table_venue_international["venue_name"]
        # default the override flag to be false
    if (cds.exposure.aggregate.total_percentage_selected  == 0.0) :
        for index, item in  enumerate(venue_us_list):
            setattr(getattr(hxd.cds.exposure.granular , item ), "override_flag", False)
        for index, item in  enumerate(venue_international_list):
            setattr(getattr(hxd.cds.exposure.granular , item ), "override_flag", False)

    if  (cds.exposure.granular.alaska.percentage_async_copy is None) & (cds.exposure.aggregate.total_percentage_selected  != 0.0):
        for index, item in  enumerate(venue_us_list):
            temp_value_1 = getattr(getattr(hxd.cds.exposure.granular , item ), "percentage_output_copy") 
            if temp_value_1 > 0.0:
                setattr(getattr(hxd.cds.exposure.granular , item ), "override_flag", True)
            else:
                setattr(getattr(hxd.cds.exposure.granular , item ), "override_flag", False)
        for index, item in  enumerate(venue_international_list):
            temp_value_1 = getattr(getattr(hxd.cds.exposure.granular , item ), "percentage_output_copy")  
            if temp_value_1 > 0.0:
                setattr(getattr(hxd.cds.exposure.granular , item ), "override_flag", True)
            else:
                setattr(getattr(hxd.cds.exposure.granular , item ), "override_flag", False)


            

    override_flag_international = []   
    override_flag_us = []  
    percentage_output_us = []
    percentage_output_international = []
    for index, item in  enumerate(venue_us_list):
        temp_value = getattr(getattr(hxd.cds.exposure.granular , item ), "override_flag")
        temp_value_1 = getattr(getattr(hxd.cds.exposure.granular , item ), "percentage_output_copy")    
        override_flag_us.append(temp_value)
        percentage_output_us.append(temp_value_1)
    for index, item in  enumerate(venue_international_list):
        temp_value = getattr(getattr(hxd.cds.exposure.granular , item ), "override_flag")
        temp_value_1 = getattr(getattr(hxd.cds.exposure.granular , item ), "percentage_output_copy")    
        override_flag_international.append(temp_value)
        percentage_output_international.append(temp_value_1)


    #get the async oput of venue percentage
    venue_us_pct_async = []
    venue_international_pct_async = []

    for index,item in  enumerate(venue_international_list):
        temp_value = getattr(getattr(hxd.cds.exposure.granular , item), "percentage_async_copy")
        venue_international_pct_async.append(temp_value)
    for index,item in  enumerate(venue_us_list):
        temp_value = getattr(getattr(hxd.cds.exposure.granular , item), "percentage_async_copy")
        venue_us_pct_async.append(temp_value)
    
    override_flag_us_new = []
    override_flag_international_new = []
    if venue_us_pct_async[0] is not None:
        override_flag_us_new = [True if ((percentage_output_us[i] != venue_us_pct_async[i]))  else override_flag_us[i] for i in range(0,len(venue_us_list))]
        override_flag_international_new = [True if ((percentage_output_international[i] != venue_international_pct_async[i]) & (override_flag_international[i] == False)) else override_flag_international[i]  for i in range(0,len(venue_international_list))]
        for index, item in  enumerate(venue_us_list):
            setattr(getattr(hxd.cds.exposure.granular , item ), "override_flag",override_flag_us_new[index] )
        for index, item in  enumerate(venue_international_list):
            setattr(getattr(hxd.cds.exposure.granular , item ), "override_flag", override_flag_international_new[index] )   

@hx.task
def venue_factors_calculate_selected(hxd, progress):

    cds = hxd.cds
    venue_us_list = hx.params.table_venue_us["venue_name"]
    venue_international_list = hx.params.table_venue_international["venue_name"]

    
    # if cds.us_masking == True:
    #     venue_us_params = hx.params.table_venue_us
    #     venue_us_list = hx.params.table_venue_us["venue_name"]
    #     venue_us_selection = []
    #     venue_us_ptc = []

    #     for item in  venue_us_list:
    #         venue_us_ptc.append(getattr(getattr(hxd.cds.exposure.granular , item ),"percentage"))
    #         venue_us_selection.append(getattr(getattr(hxd.cds.exposure.granular , item ), "selection"))

    #     venue_us_df = pd.DataFrame({"venue_us": venue_us_list, "percentage" : venue_us_ptc, "selection" : venue_us_selection})
    #     venue_us_df["selection_with_no_percentage"] = np.where((venue_us_df["selection"] == True) & (venue_us_df["percentage"] == 0), True, False )

    #     if cds.exposure.granular.include_international_venues : 
    #         venue_international_params = hx.params.table_venue_international
    #         venue_international_list = hx.params.table_venue_international["venue_name"]
    #         venue_international_selection = []
    #         venue_international_ptc = []

    #         for item in  venue_international_list:
    #             venue_international_ptc.append(getattr(getattr(hxd.cds.exposure.granular , item ),"percentage"))
    #             venue_international_selection.append(getattr(getattr(hxd.cds.exposure.granular , item ), "selection"))

    #         venue_international_df = pd.DataFrame({"venue_international": venue_international_list, "percentage" : venue_international_ptc, "selection" : venue_international_selection})
    #         venue_international_df["selection_with_no_percentage"] = np.where((venue_international_df["selection"] == True) & (venue_international_df["percentage"] == 0), True, False )

    #         denominator = venue_us_df["selection_with_no_percentage"].sum() + venue_international_df["selection_with_no_percentage"].sum()
    #         percent_entered_manually = venue_us_df["percentage"].sum() + venue_international_df["percentage"].sum()

    #         remianing_percent_to_spread = max(1 - percent_entered_manually, 0)

    #         venue_us_df["calculated_percentage"] = np.where(venue_us_df["selection_with_no_percentage"] == True, remianing_percent_to_spread / denominator, 0 )
    #         venue_international_df["calculated_percentage"] = np.where(venue_international_df["selection_with_no_percentage"] == True, remianing_percent_to_spread / denominator, 0 )

    #         venue_us_df["percentage_to_use"] = np.where(venue_us_df["selection_with_no_percentage"] == True, venue_us_df["calculated_percentage"], venue_us_df["percentage"])
    #         venue_international_df["percentage_to_use"] = np.where(venue_international_df["selection_with_no_percentage"] == True, venue_international_df["calculated_percentage"], venue_international_df["percentage"])

    #         for item in  venue_us_list:
    #             setattr(getattr(hxd.cds.exposure.granular , item ),"percentage", venue_us_df[venue_us_df["venue_us"] == item]["percentage_to_use"].iloc[0]) 

    #         for item in  venue_international_list:
    #             setattr(getattr(hxd.cds.exposure.granular , item ),"percentage", venue_international_df[venue_international_df["venue_international"] == item]["percentage_to_use"].iloc[0])    

    #     else:
    #         denominator = venue_us_df["selection_with_no_percentage"].sum()
    #         percent_entered_manually = venue_us_df["percentage"].sum()

    #         remianing_percent_to_spread = max(1 - percent_entered_manually, 0)

    #         venue_us_df["calculated_percentage"] = np.where(venue_us_df["selection_with_no_percentage"] == True, remianing_percent_to_spread / denominator, 0 )

    #         venue_us_df["percentage_to_use"] = np.where(venue_us_df["selection_with_no_percentage"] == True, venue_us_df["calculated_percentage"], venue_us_df["percentage"])
            
    #         for item in  venue_us_list:
    #             setattr(getattr(hxd.cds.exposure.granular , item ),"percentage", venue_us_df[venue_us_df["venue_us"] == item]["percentage_to_use"].iloc[0]) 
    
    # if cds.international_masking == True:
    #     venue_international_params = hx.params.table_venue_international
    #     venue_international_list = hx.params.table_venue_international["venue_name"]
    #     venue_international_selection = []
    #     venue_international_ptc = []

    #     for item in  venue_international_list:
    #         venue_international_ptc.append(getattr(getattr(hxd.cds.exposure.granular , item ),"percentage"))
    #         venue_international_selection.append(getattr(getattr(hxd.cds.exposure.granular , item ), "selection"))

        
    #     venue_international_df = pd.DataFrame({"venue_international": venue_international_list, "percentage" : venue_international_ptc, "selection" : venue_international_selection})

    #     venue_international_df["selection_with_no_percentage"] = np.where((venue_international_df["selection"] == True) & (venue_international_df["percentage"] == 0), True, False )
       
         
    #     if cds.exposure.granular.include_us_venues : 
    #         venue_us_params = hx.params.table_venue_us
    #         venue_us_list = hx.params.table_venue_us["venue_name"]
    #         venue_us_selection = []
    #         venue_us_ptc = []

    #         for item in  venue_us_list:
    #             venue_us_ptc.append(getattr(getattr(hxd.cds.exposure.granular , item ),"percentage"))
    #             venue_us_selection.append(getattr(getattr(hxd.cds.exposure.granular , item ), "selection"))

    #         venue_us_df = pd.DataFrame({"venue_us": venue_us_list, "percentage" : venue_us_ptc, "selection" : venue_us_selection})
    #         venue_us_df["selection_with_no_percentage"] = np.where((venue_us_df["selection"] == True) & (venue_us_df["percentage"] == 0), True, False )

    #         denominator = venue_us_df["selection_with_no_percentage"].sum() + venue_international_df["selection_with_no_percentage"].sum()
    #         percent_entered_manually = venue_us_df["percentage"].sum() + venue_international_df["percentage"].sum()

    #         remianing_percent_to_spread = max(1 - percent_entered_manually, 0)

    #         venue_us_df["calculated_percentage"] = np.where(venue_us_df["selection_with_no_percentage"] == True, remianing_percent_to_spread / denominator, 0 )
    #         venue_international_df["calculated_percentage"] = np.where(venue_international_df["selection_with_no_percentage"] == True, remianing_percent_to_spread / denominator, 0 )

    #         venue_us_df["percentage_to_use"] = np.where(venue_us_df["selection_with_no_percentage"] == True, venue_us_df["calculated_percentage"], venue_us_df["percentage"])
    #         venue_international_df["percentage_to_use"] = np.where(venue_international_df["selection_with_no_percentage"] == True, venue_international_df["calculated_percentage"], venue_international_df["percentage"])

    #         for item in  venue_us_list:
    #             setattr(getattr(hxd.cds.exposure.granular , item ),"percentage", venue_us_df[venue_us_df["venue_us"] == item]["percentage_to_use"].iloc[0]) 

    #         for item in  venue_international_list:
    #             setattr(getattr(hxd.cds.exposure.granular , item ),"percentage", venue_international_df[venue_international_df["venue_international"] == item]["percentage_to_use"].iloc[0])  

    #     else:
    #         denominator = venue_international_df["selection_with_no_percentage"].sum()
    #         percent_entered_manually = venue_international_df["percentage"].sum()

    #         remianing_percent_to_spread = max(1 - percent_entered_manually, 0)

    #         venue_international_df["calculated_percentage"] = np.where(venue_international_df["selection_with_no_percentage"] == True, remianing_percent_to_spread / denominator, 0 )

    #         venue_international_df["percentage_to_use"] = np.where(venue_international_df["selection_with_no_percentage"] == True, venue_international_df["calculated_percentage"], venue_international_df["percentage"])
            
    #         for item in  venue_international_list:
    #             setattr(getattr(hxd.cds.exposure.granular , item ),"percentage", venue_international_df[venue_international_df["venue_international"] == item]["percentage_to_use"].iloc[0]) 

    venue_us_selection = []
    venue_us_override = []
    venue_us_ptc = []

    for item in  venue_us_list:
        venue_us_ptc.append(getattr(getattr(hxd.cds.exposure.granular , item ),"percentage"))
        venue_us_selection.append(getattr(getattr(hxd.cds.exposure.granular , item ), "selection"))
        venue_us_override.append(getattr(getattr(hxd.cds.exposure.granular , item ), "override_flag"))

    venue_us_df = pd.DataFrame({"venue_us": venue_us_list, "percentage" : venue_us_ptc, "selection" : venue_us_selection, "override_flag": venue_us_override})
    venue_us_df["selection_with_no_override"] = np.where((venue_us_df["selection"] == True) & (venue_us_df["override_flag"] == False), True, False )    

    venue_international_selection = []
    venue_international_override = []
    venue_international_ptc = []

    for item in  venue_international_list:
        venue_international_ptc.append(getattr(getattr(hxd.cds.exposure.granular , item ),"percentage"))
        venue_international_selection.append(getattr(getattr(hxd.cds.exposure.granular , item ), "selection"))
        venue_international_override.append(getattr(getattr(hxd.cds.exposure.granular , item ), "override_flag"))

    venue_international_df = pd.DataFrame({"venue_international": venue_international_list, "percentage" : venue_international_ptc, "selection" : venue_international_selection, "override_flag": venue_international_override})
    venue_international_df["selection_with_no_override"] = np.where((venue_international_df["selection"] == True) & (venue_international_df["override_flag"] == False), True, False )    

    us_total_overried_pct = venue_us_df[(venue_us_df["override_flag"] == True)&(venue_us_df["selection"] == True)]["percentage"].sum()
    international_total_overried_pct = venue_international_df[(venue_international_df["override_flag"] == True)&(venue_international_df["selection"] == True)]["percentage"].sum()
    denominator = venue_us_df["selection_with_no_override"].sum() + venue_international_df["selection_with_no_override"].sum()
    update_value = (1- us_total_overried_pct - international_total_overried_pct)/ denominator

    for index,item in enumerate(venue_us_list):
        if venue_us_df["selection_with_no_override"].iloc[index] == True:
            setattr(getattr(hxd.cds.exposure.granular , item ),"percentage",update_value)
        if venue_us_df["selection"].iloc[index] == False:
            setattr(getattr(hxd.cds.exposure.granular , item ),"percentage",0.0)

    for index,item in enumerate(venue_international_list):
        if venue_international_df["selection_with_no_override"].iloc[index] == True:
            setattr(getattr(hxd.cds.exposure.granular , item ),"percentage",update_value)
        if venue_international_df["selection"].iloc[index] == False:
            setattr(getattr(hxd.cds.exposure.granular , item ),"percentage",0.0)




    for item in venue_us_list:
        temp_value = getattr(getattr(hxd.cds.exposure.granular , item ),"percentage")
        setattr(getattr(hxd.cds.exposure.granular , item ),"percentage_async_copy", temp_value)
    for item in venue_international_list:
        temp_value = getattr(getattr(hxd.cds.exposure.granular , item ),"percentage")
        setattr(getattr(hxd.cds.exposure.granular , item ),"percentage_async_copy", temp_value)    

    pass

@hx.task
def venue_calculation_with_override(hxd,progress):
    venue_factors_override_flag(hxd,progress)
    venue_factors_calculate_selected(hxd,progress)



@hx.task
def set_defaults_button(hxd, progress):
    cds = hxd.cds
    coverages = ["professional_liability","general_liability","product_liability","eo","sexual_abuse","employee_benefits_liability","employers_liability","tech_eo_products_media","healthcare_professional_liability","product_recall","well_tech_eo_media"]
    include_coverage = []
    retro_date = []
    for coverage in coverages :
        selection = getattr(getattr(cds.rating_factors.pricing, coverage), "include_primary")
        retro =  getattr(getattr(cds.rating_factors.pricing, coverage), "retroactive_date")

        include_coverage.append(selection)
        retro_date.append(retro)
    
    default_retros = pd.DataFrame({"coverage": coverages,"include": include_coverage,"retro_date": retro_date})
    first_retro = default_retros["retro_date"].dropna().iloc[0]
    default_retros["calculated_retro"] = np.where((default_retros["include"])&(default_retros["retro_date"].isna()),True, False)

    for coverage in coverages :
        set_retro_flag = default_retros[default_retros["coverage"]==coverage]["calculated_retro"].iloc[0]
        if set_retro_flag:
            setattr(getattr(cds.rating_factors.pricing, coverage), "retroactive_date", first_retro)

        set_coverages = default_retros[default_retros["coverage"]==coverage]["include"].iloc[0]
        if set_coverages and coverage != "sexual_abuse":
            setattr(getattr(cds.options[0].coverages, coverage), "retention", cds.default_retention)
            setattr(getattr(cds.options[0].coverages, coverage), "per_claim_limit", cds.default_per_claim_limit)
            setattr(getattr(cds.options[0].coverages, coverage), "aggregate_limit", cds.default_aggregate_limit)
        elif set_coverages and coverage == "sexual_abuse":
            setattr(getattr(cds.options[0].coverages, coverage), "retention", cds.default_retention)
            setattr(getattr(cds.options[0].coverages, coverage), "per_claim_limit", 1000000)
            setattr(getattr(cds.options[0].coverages, coverage), "aggregate_limit", 1000000)
                
    pass


# Importing expiring policy for rate change
'''
Async task to import data from an expiring policy option for rate change calculation and analysis of movement.
Developers will need to update the task in two places, first for which variables from the expiring policy to import,
second to assign these to the current model variables.
'''


@hx.task
def expiring_policy_fetch_task(hxd, progress):
    
    # if not hxd.cds.rate_change.expiring_policy_option_id.selected:
    #     hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id = hxd.cds.rate_change.expiring_policy_option_id.selected #or 85244 # NOTE: use hardcoded ID for debugging if needed
    # TODO comment above and uncomment below for dev
    # expiring_policy_option_id = 1116037 #or 85244 # NOTE: use hardcoded ID for debugging if needed
    expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False)


    
    if expiring_response.status_code != 200:
        raise Exception(expiring_response.json())
    
    expiring_data = expiring_response.json()["data"]

    # Need to copy the options across in the expiring data so that the rate change accounts for options
    selected_option = int(expiring_data["cds"]["option_selected"][-1]) -1 
    bucket_to_copy = expiring_data["cds"]["options"][selected_option]

    for i in range(len(expiring_data ["cds"]["options"])):
        if i != selected_option:
            expiring_data["cds"]["options"][i] = copy.deepcopy(bucket_to_copy)


    # Get fields from json response and push to hxd
    expiring_layers_len = len(expiring_data["cds"]["layers"])
    layer_mapping = {}

    for idx, layer in enumerate(hxd.cds.layers):
        # Throw error if expiring layer doesn't exist
        if layer.rate_change.expiring_layer > expiring_layers_len:
            hx.errors.fatal(f"Expiring Layer {layer.rate_change.expiring_layer}, mapped to Renewal Layer {idx+1}, does not exist. Number of expiring layers is {expiring_layers_len}.")

        mapped_expiring_layer_idx = layer.rate_change.expiring_layer - 1
        layer.rate_change.premium_annualized_100pct.expiring = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["bound_premium"]
        expiring_written_line = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["written_line"]
        #layer.rate_change.premium_annualized_beazley_share.expiring = layer.rate_change.premium_annualized_100pct.expiring * (expiring_written_line or 0)
        # NOTE: ... Add expiring fields as required here

        # Save layer mapping
        layer_mapping[str(idx+1)] = layer.rate_change.expiring_layer

        layer.rate_change.premium_annualized_100pct.renewal = layer.bound_premium

    hxd.cds.rate_change.layer_mapping = json.dumps(layer_mapping)

    # Confirm task has been run
    hxd.cds.rate_change.has_fetch_run = True
    hxd.cds.rate_change.has_fetch_not_run = False
    return (expiring_data)


@hx.task
def rarc_task(hxd, progress):

    # if not hxd.cds.rate_change.expiring_policy_option_id.selected:
    #     hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Make sure expiring data is up to date
    expiring_data = expiring_policy_fetch_task(hxd, progress)

    # Get correct buckets based on coverage
    buckets = rate_change_buckets(hxd)

    data_schema_static_filename = "data_schema/data_schema_static_copy.py"
    data_schema_static_path = os.path.join(os.path.dirname(__file__), data_schema_static_filename)


    # Rate Change with offline_hxd
    rc = RateChangeLib(
        hxd=hxd,
        progress=progress,
        buckets=buckets,
        layers_path="cds/layers",
        expiring_actual_prem="bound_premium",
        expiring_technical_prem="benchmark_premium",
        async_tasks=[],  # Pass the actual tasks, not strings
        data_schema_static_path=data_schema_static_path
    )

    rc.calculate_repriced_values(
        #expiring_policy_option_id=42837 # NOTE: for debugging if needed
        expiring_data = expiring_data
    )

    # Use the repriced values to calculate the changes for each bucket
    rarc_df, rarc_list = rc.calculate_rarc_by_layer()

    # Fill Nans in first row to avoid errors when assigning to hxd, and recreate list after this change
    # rarc_df = rarc_df.fillna(0)
    # rarc_list = rarc_df[[col for col in rarc_df if "_change" in col]].to_dict(orient="records")
    # The index [0] is for the retention layer. Set all these to 1 for RC figures and 0 for premiums to avoid errors when pushing to hxd
    # rarc_list[0]['brokerage_change']['model_calculated'] = 1
    # rarc_list[0]['deductible_change']['model_calculated'] = 1
    # rarc_list[0]['exposure_change']['model_calculated'] = 1
    # rarc_list[0]['limit_change']['model_calculated'] = 1
    # rarc_list[0]['other_change']['model_calculated'] = 1
    # rarc_list[0]['risk_characteristics_change']['model_calculated'] = 1
    # rarc_list[0]['terms_conditions_change']['model_calculated'] = 1
    # rarc_list[0]['temp_storage']['benchmark_premium'] = 0
    # rarc_list[0]['temp_storage']['quoted_premium'] = 0

    # First layer will always be null so replace nulls in rarc_list with 0 for hxd assigns
    # Use nested list and dict comprehensions to recreate the list with nans replaced with 0s
    rarc_list = [
        {
            key1: {
                key2: 0 if math.isnan(list_item[key1][key2] or np.nan) else list_item[key1][key2]  # Replace nans and Nones with 0
                for key2 in list_item[key1]  # Second layer of nested dicts
            } 
            for key1 in list_item  # First layer of nested dicts
        } 
        for list_item in rarc_list  # Items in rarc_list
    ]

    # NOTE: for debugging if needed
    # pd.set_option('display.max_columns', None)
    # print(rarc_df)
    # print(rarc_list)

    # Push to hxd
    for rarc_layer, hxd_layer in zip(rarc_list, hxd.cds.layers):
        hxd_layer.rate_change.temp_storage = rarc_layer["temp_storage"]
        rarc_layer.pop("temp_storage")

        for key, value in rarc_layer.items():
            setattr(hxd_layer.rate_change, key, value)

    # Confirm task has been run
    hxd.cds.rate_change.has_rarc_run = True
    hxd.cds.rate_change.has_rarc_not_run = False



# @hx.task
# def roll_exposure_fields_task(hxd, progress):
#     '''
#     Shift exposure data by one year.
#     Using exposure data section
#     '''

#     if hxd.cds.gmm_masking and hxd.cds.exposure.granular.gmm_product.product != "Triage":
#         primary_exposure_dict = [{
#             "current_year": item.current_year,
#             "one_years_ago": item.one_years_ago,
#             "two_years_ago": item.two_years_ago,
#             "three_years_ago": item.three_years_ago,
#             "four_years_ago": item.four_years_ago,
#             "five_years_ago": item.five_years_ago,
#         } for item in hxd.cds.exposure.granular.gmm_primary_exposure_details]
#         primary_exposure = pd.DataFrame(primary_exposure_dict)

#         primary_exposure_shifted = primary_exposure.shift(periods=1,axis="columns")
#         primary_exposure_shifted = primary_exposure_shifted.fillna(0)
#         primary_exposure_shifted["current_year"] = 0

#         utils.write_pd_to_hxd(primary_exposure_shifted, hxd.cds.exposure.granular.gmm_primary_exposure_details, ["current_year","one_years_ago","two_years_ago","three_years_ago","four_years_ago","five_years_ago"])

#         secondary_exposure_dict = [{
#             "current_year": item.current_year,
#             "one_years_ago": item.one_years_ago,
#             "two_years_ago": item.two_years_ago,
#             "three_years_ago": item.three_years_ago,
#             "four_years_ago": item.four_years_ago,
#             "five_years_ago": item.five_years_ago,
#         } for item in hxd.cds.exposure.granular.gmm_secondary_exposure_details]
#         secondary_exposure = pd.DataFrame(secondary_exposure_dict)

#         secondary_exposure_shifted = secondary_exposure.shift(periods=1,axis="columns")
#         secondary_exposure_shifted = secondary_exposure_shifted.fillna(0)
#         secondary_exposure_shifted["current_year"] = 0
#         utils.write_pd_to_hxd(secondary_exposure_shifted, hxd.cds.exposure.granular.gmm_secondary_exposure_details, ["current_year","one_years_ago","two_years_ago","three_years_ago","four_years_ago","five_years_ago"])

#     elif hxd.cds.gmm_masking :
#         docs_dict = [{
#             "doc_current_year": item.doc_current_year,
#             "doc_one_years_ago": item.doc_one_years_ago,
#             "doc_two_years_ago": item.doc_two_years_ago,
#             "doc_three_years_ago": item.doc_three_years_ago,
#             "doc_four_years_ago": item.doc_four_years_ago,
#         } for item in hxd.cds.exposure.granular.triage_doctors_residents]
#         doc_exposure = pd.DataFrame(docs_dict)

#         doc_shifted = doc_exposure.shift(periods=1,axis="columns")
#         doc_shifted = doc_shifted.fillna(0)
#         doc_shifted["doc_current_year"] = 0
        
#         res_dict = [{
#             "resident_current_year": item.resident_current_year,
#             "resident_one_years_ago": item.resident_one_years_ago,
#             "resident_two_years_ago": item.resident_two_years_ago,
#             "resident_three_years_ago": item.resident_three_years_ago,
#             "resident_four_years_ago": item.resident_four_years_ago,
#         } for item in hxd.cds.exposure.granular.triage_doctors_residents]
#         res_exposure = pd.DataFrame(res_dict)

#         res_shifted = res_exposure.shift(periods=1,axis="columns")
#         res_shifted = res_shifted.fillna(0)
#         res_shifted["resident_current_year"] = 0
        
#         doc_res_shifted = pd.concat([doc_shifted, res_shifted], axis=1)
#         utils.write_pd_to_hxd(doc_res_shifted, hxd.cds.exposure.granular.triage_doctors_residents, ["doc_current_year","doc_one_years_ago","doc_two_years_ago","doc_three_years_ago","doc_four_years_ago","resident_current_year","resident_one_years_ago","resident_two_years_ago","resident_three_years_ago","resident_four_years_ago"])

#         procedures_dict = [{
#             "current_year": item.current_year,
#             "one_years_ago": item.one_years_ago,
#             "two_years_ago": item.two_years_ago,
#             "three_years_ago": item.three_years_ago,
#             "four_years_ago": item.four_years_ago,
#         } for item in hxd.cds.exposure.granular.triage_procedures]
#         procedures = pd.DataFrame(procedures_dict)

#         procedures_shifted = procedures.shift(periods=1,axis="columns")
#         procedures_shifted = procedures_shifted.fillna(0)
#         procedures_shifted["current_year"] = 0
#         utils.write_pd_to_hxd(procedures_shifted, hxd.cds.exposure.granular.triage_procedures, ["current_year","one_years_ago","two_years_ago","three_years_ago","four_years_ago"])

#     elif hxd.cds.glsn_masking :
#         primary_exposure_dict = [{
#             "current_year": item.current_year,
#             "one_years_ago": item.one_years_ago,
#             "two_years_ago": item.two_years_ago,
#             "three_years_ago": item.three_years_ago,
#             "four_years_ago": item.four_years_ago,
#             "five_years_ago": item.five_years_ago,
#         } for item in hxd.cds.exposure.granular.glsn_primary_exposure_details]
#         primary_exposure = pd.DataFrame(primary_exposure_dict)

#         primary_exposure_shifted = primary_exposure.shift(periods=1,axis="columns")
#         primary_exposure_shifted = primary_exposure_shifted.fillna(0)
#         primary_exposure_shifted["current_year"] = 0
#         utils.write_pd_to_hxd(primary_exposure_shifted, hxd.cds.exposure.granular.glsn_primary_exposure_details, ["current_year","one_years_ago","two_years_ago","three_years_ago","four_years_ago","five_years_ago"])

#         secondary_exposure_dict = [{
#             "current_year": item.current_year,
#             "one_years_ago": item.one_years_ago,
#             "two_years_ago": item.two_years_ago,
#             "three_years_ago": item.three_years_ago,
#             "four_years_ago": item.four_years_ago,
#             "five_years_ago": item.five_years_ago,
#         } for item in hxd.cds.exposure.granular.glsn_secondary_exposure_details]
#         secondary_exposure = pd.DataFrame(secondary_exposure_dict)

#         secondary_exposure_shifted = secondary_exposure.shift(periods=1,axis="columns")
#         secondary_exposure_shifted = secondary_exposure_shifted.fillna(0)
#         secondary_exposure_shifted["current_year"] = 0
#         utils.write_pd_to_hxd(secondary_exposure_shifted, hxd.cds.exposure.granular.glsn_secondary_exposure_details, ["current_year","one_years_ago","two_years_ago","three_years_ago","four_years_ago","five_years_ago"])

#     if hxd.cds.uw_notes is not None: 
#         inception_date = hxd.hx_core.inception_date
#         year_stamp = inception_date.year - 1
#         if hxd.cds.historical_comments is None:
#             hxd.cds.historical_comments = str(year_stamp) + " Comments: \n" + hxd.cds.uw_notes
#         else: 
#             hist_comments_updated = hxd.cds.historical_comments + "\n" +"\n" + str(year_stamp) + " Comments:\n" + hxd.cds.uw_notes
#             hxd.cds.historical_comments = hist_comments_updated
#         hxd.cds.uw_notes = "Enter " + str(year_stamp +1 ) + " notes here:"
#     hxd.cds.exposure.aggregate.revenue = 0


@hx.task
def roll_exposure_fields_task(hxd, progress):
    '''
    Shift exposure data by the number of year between the current option and the expiry options
    Using staging expiry exposure input nodes for gmm and gsl primary and secondary
    Using current input nodes for triange doctor and residents and procedures
    '''
    # calculate the shift if years
    shift_period = hxd.hx_core.inception_date.year - hxd.cds.expiry_inception_date.year

    if hxd.cds.gmm_masking and hxd.cds.exposure.granular.gmm_product.product != "Triage":
        primary_exposure_dict = [{
            "current_year": item.stg_current_year,
            "one_years_ago": item.stg_one_years_ago,
            "two_years_ago": item.stg_two_years_ago,
            "three_years_ago": item.stg_three_years_ago,
            "four_years_ago": item.stg_four_years_ago,
            "five_years_ago": item.stg_five_years_ago,
        } for item in hxd.cds.exposure.granular.gmm_primary_exposure_details]
        primary_exposure = pd.DataFrame(primary_exposure_dict)

        primary_exposure_shifted = primary_exposure.shift(periods=shift_period,axis="columns")
        primary_exposure_shifted = primary_exposure_shifted.fillna(0)
        primary_exposure_shifted["current_year"] = 0

        utils.write_pd_to_hxd(primary_exposure_shifted, hxd.cds.exposure.granular.gmm_primary_exposure_details, ["current_year","one_years_ago","two_years_ago","three_years_ago","four_years_ago","five_years_ago"])

        secondary_exposure_dict = [{
            "current_year": item.stg_current_year,
            "one_years_ago": item.stg_one_years_ago,
            "two_years_ago": item.stg_two_years_ago,
            "three_years_ago": item.stg_three_years_ago,
            "four_years_ago": item.stg_four_years_ago,
            "five_years_ago": item.stg_five_years_ago,
        } for item in hxd.cds.exposure.granular.gmm_secondary_exposure_details]
        secondary_exposure = pd.DataFrame(secondary_exposure_dict)

        secondary_exposure_shifted = secondary_exposure.shift(periods=shift_period,axis="columns")
        secondary_exposure_shifted = secondary_exposure_shifted.fillna(0)
        secondary_exposure_shifted["current_year"] = 0
        utils.write_pd_to_hxd(secondary_exposure_shifted, hxd.cds.exposure.granular.gmm_secondary_exposure_details, ["current_year","one_years_ago","two_years_ago","three_years_ago","four_years_ago","five_years_ago"])

    elif hxd.cds.gmm_masking :
        docs_dict = [{
            "doc_current_year": item.doc_current_year,
            "doc_one_years_ago": item.doc_one_years_ago,
            "doc_two_years_ago": item.doc_two_years_ago,
            "doc_three_years_ago": item.doc_three_years_ago,
            "doc_four_years_ago": item.doc_four_years_ago,
        } for item in hxd.cds.exposure.granular.triage_doctors_residents]
        doc_exposure = pd.DataFrame(docs_dict)

        doc_shifted = doc_exposure.shift(periods=shift_period,axis="columns")
        doc_shifted = doc_shifted.fillna(0)
        doc_shifted["doc_current_year"] = 0
        
        res_dict = [{
            "resident_current_year": item.resident_current_year,
            "resident_one_years_ago": item.resident_one_years_ago,
            "resident_two_years_ago": item.resident_two_years_ago,
            "resident_three_years_ago": item.resident_three_years_ago,
            "resident_four_years_ago": item.resident_four_years_ago,
        } for item in hxd.cds.exposure.granular.triage_doctors_residents]
        res_exposure = pd.DataFrame(res_dict)

        res_shifted = res_exposure.shift(periods=shift_period,axis="columns")
        res_shifted = res_shifted.fillna(0)
        res_shifted["resident_current_year"] = 0
        
        doc_res_shifted = pd.concat([doc_shifted, res_shifted], axis=1)
        utils.write_pd_to_hxd(doc_res_shifted, hxd.cds.exposure.granular.triage_doctors_residents, ["doc_current_year","doc_one_years_ago","doc_two_years_ago","doc_three_years_ago","doc_four_years_ago","resident_current_year","resident_one_years_ago","resident_two_years_ago","resident_three_years_ago","resident_four_years_ago"])

        procedures_dict = [{
            "current_year": item.current_year,
            "one_years_ago": item.one_years_ago,
            "two_years_ago": item.two_years_ago,
            "three_years_ago": item.three_years_ago,
            "four_years_ago": item.four_years_ago,
        } for item in hxd.cds.exposure.granular.triage_procedures]
        procedures = pd.DataFrame(procedures_dict)

        procedures_shifted = procedures.shift(periods=1,axis="columns")
        procedures_shifted = procedures_shifted.fillna(0)
        procedures_shifted["current_year"] = 0
        utils.write_pd_to_hxd(procedures_shifted, hxd.cds.exposure.granular.triage_procedures, ["current_year","one_years_ago","two_years_ago","three_years_ago","four_years_ago"])

    elif hxd.cds.glsn_masking :
        primary_exposure_dict = [{
            "current_year": item.stg_current_year,
            "one_years_ago": item.stg_one_years_ago,
            "two_years_ago": item.stg_two_years_ago,
            "three_years_ago": item.stg_three_years_ago,
            "four_years_ago": item.stg_four_years_ago,
            "five_years_ago": item.stg_five_years_ago,
        } for item in hxd.cds.exposure.granular.glsn_primary_exposure_details]
        primary_exposure = pd.DataFrame(primary_exposure_dict)

        primary_exposure_shifted = primary_exposure.shift(periods=1,axis="columns")
        primary_exposure_shifted = primary_exposure_shifted.fillna(0)
        primary_exposure_shifted["current_year"] = 0
        utils.write_pd_to_hxd(primary_exposure_shifted, hxd.cds.exposure.granular.glsn_primary_exposure_details, ["current_year","one_years_ago","two_years_ago","three_years_ago","four_years_ago","five_years_ago"])

        secondary_exposure_dict = [{
            "current_year": item.stg_current_year,
            "one_years_ago": item.stg_one_years_ago,
            "two_years_ago": item.stg_two_years_ago,
            "three_years_ago": item.stg_three_years_ago,
            "four_years_ago": item.stg_four_years_ago,
            "five_years_ago": item.stg_five_years_ago,
        } for item in hxd.cds.exposure.granular.glsn_secondary_exposure_details]
        secondary_exposure = pd.DataFrame(secondary_exposure_dict)

        secondary_exposure_shifted = secondary_exposure.shift(periods=1,axis="columns")
        secondary_exposure_shifted = secondary_exposure_shifted.fillna(0)
        secondary_exposure_shifted["current_year"] = 0
        utils.write_pd_to_hxd(secondary_exposure_shifted, hxd.cds.exposure.granular.glsn_secondary_exposure_details, ["current_year","one_years_ago","two_years_ago","three_years_ago","four_years_ago","five_years_ago"])

    if hxd.cds.uw_notes is not None: 
        inception_date = hxd.hx_core.inception_date
        year_stamp = inception_date.year - 1
        if hxd.cds.historical_comments is None:
            hxd.cds.historical_comments = str(year_stamp) + " Comments: \n" + hxd.cds.uw_notes
        else: 
            hist_comments_updated = hxd.cds.historical_comments + "\n" +"\n" + str(year_stamp) + " Comments:\n" + hxd.cds.uw_notes
            hxd.cds.historical_comments = hist_comments_updated
        hxd.cds.uw_notes = "Enter " + str(year_stamp +1 ) + " notes here:"
    hxd.cds.exposure.aggregate.revenue = 0

@hx.task
def sync_expiring_ids(hxd, progress):
    # Note this task is to be run following each migrated policy to sync the expiring ids
    hxd.model_state.expiring_policy_option_id = hx.meta.expiring_policy_option_id
    # hxd.model_state.expiring_policy_option_id = 56654 # For debugging

@hx.task
def initialise_model(hxd, progress):
    '''
    Get policy options id updated from
    set the show initialised page
    '''
    # initialising API
    hx_renew = init_hx_renew_api()
    
    # TODO comment the below before going live
    # current_policy_option_id =  1067930 # expected expiry id 844560 no model updated from 844576 https://www.beazley-dev.hxrenew.com/risks/633071/policies/793746  
    # get current policy option id
    # current_policy_option_id = hx.meta.policy_option_id

    # # get the policy_option_updated_from
    # current_response = hx_renew.policies.get_policy_options(policy_option_id={current_policy_option_id})
    
    # # NOTE: This line above will cause a bug when running the model test on the async tasks 'initialise_model' due to different structure in the LIVE API and TEST API.
    # # WORK AROUND: please comment row 815, uncoment line 813 and provide an exisiting Poi to allow the Model test to work.
    # if current_response.status_code != 200:
    #     raise Exception(current_response.json())
    
    # current_data = current_response.json()[0]

    current_policy_option_id = hx.meta.policy_option_id or hxd.cds.database_id

    current_response = hx_renew.policies.get_policy_options(
        policy_option_id=[current_policy_option_id]
    )

    if current_response.status_code != 200:
        raise Exception(current_response.json())

    current_payload = current_response.json()

    if not isinstance(current_payload, list) or len(current_payload) == 0:
        hx.errors.fatal(
            f"Initialise model failed: no policy option was returned for "
            f"policy_option_id={current_policy_option_id}. "
            f"Status code: {current_response.status_code}. "
            f"Response body: {current_response.text}"
        )

    current_data = current_payload[0]

    policy_option_updated_from = current_data['policy_option_updated_from']
    
    hxd.model_state.policy_option_updated_from_id = policy_option_updated_from
    
    # TODO comment the below before go live
    # hxd.model_state.expiring_policy_option_id = None
    hxd.model_state.expiring_policy_option_id = hx.meta.expiring_policy_option_id
    # move assignement rate change here to allow clearance of the override
    hxd.cds.rate_change.expiring_policy_option_id.calculated = hxd.model_state.expiring_policy_option_id
    
    
    # hxd.model_state.pressed_initialise_model = True

    # No model version update
    if hxd.model_state.policy_option_updated_from_id == 0 or hxd.model_state.policy_option_updated_from_id == None: # not a model version update
        if (hxd.model_state.expiring_policy_option_id is None): # New Policy
            hxd.model_state.pressed_initialise_model = True
        else: # renewal
            hxd.model_state.pressed_start_renewal_task = False
            
            # # fetch expiry
            
            # with hx_renew.poi.session(policy_option_id = current_policy_option_id) as session_id:
            #     expiry_response = hx_renew.poi.import_from_expiring(policy_option_id = hxd.model_state.expiring_policy_option_id, session_id=session_id)

            # with hx_renew.poi.create_session(policy_option_id = current_policy_option_id) as session_id:
            #     expiry_response = hx_renew.poi.import_from_expiring(policy_option_id = hxd.model_state.expiring_policy_option_id, session_id=session_id)


            # time.sleep(5)
            # if expiry_response.status_code != 200:
            #     raise Exception(expiry_response.json())
            #     # issues with permission for session 403 error

            # hx_renew.poi.close_session(policy_option_id = current_policy_option_id, session_id= session_id)

            start_renewal_task(hxd, progress) # process pre population for Renewal
            
    else: # Model version update
        start_renewal_task(hxd, progress)
        hxd.model_state.pressed_initialise_model = True
    pass

@hx.task
def start_renewal_task(hxd, progress):
   
    hx_renew = init_hx_renew_api()

    # not a model version update
    if hxd.model_state.policy_option_updated_from_id == 0 or hxd.model_state.policy_option_updated_from_id == None: 
        # The following statement checks that the expiring information has been imported for renewals. Some teams might want to start
        # from a blank rater each time, in which case update the below

        #TODO Switch off check below for coding
        if not hxd.cds.standard_fields.insured_name:
            hxd.model_state.landing_page_info = "❗❗❗ FAILED: Click 'Undo' then 'Import Expiring Policy Data' in the top right corner ❗❗❗"
        else:
            hxd.model_state.pressed_start_renewal_task = True
            hxd.model_state.pressed_initialise_model = True

        # Default renewal flag to true upon renewal    
        # hxd.cds.standard_fields.is_renewal = True  

        # TODO uncomment the below for dev
        # hxd.model_state.expiring_policy_option_id = None #830774
        # expiring_policy_option_id = hxd.model_state.expiring_policy_option_id
        hxd.model_state.expiring_policy_option_id = expiring_policy_option_id = hx.meta.expiring_policy_option_id
        
        if hxd.model_state.expiring_policy_option_id !=None:
            hxd.cds.standard_fields.is_renewal = True  
            
            expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=hxd.model_state.expiring_policy_option_id, stream=False)

            if expiring_response.status_code != 200:
                raise Exception(expiring_response.json())
            
            expiring_data = expiring_response.json()["data"]

            # Get section reference fields from json response and push to hxd
            for idx, layer in enumerate(hxd.cds.layers):
                layer.rate_change.expiring_policy_info.expiring_section_reference = expiring_data["cds"]["layers"][idx]["section_reference"]

            clear_values(hxd, progress)

            # IH edit - set value to staging input nodes for prior exposure data
            for index, detail in enumerate(hxd.cds.exposure.granular.gmm_primary_exposure_details):
                detail.stg_current_year = expiring_data["cds"]["exposure"]["granular"]["gmm_primary_exposure_details"][index]["current_year"]
                detail.stg_one_years_ago = expiring_data["cds"]["exposure"]["granular"]["gmm_primary_exposure_details"][index]["one_years_ago"]
                detail.stg_two_years_ago = expiring_data["cds"]["exposure"]["granular"]["gmm_primary_exposure_details"][index]["two_years_ago"]
                detail.stg_three_years_ago = expiring_data["cds"]["exposure"]["granular"]["gmm_primary_exposure_details"][index]["three_years_ago"]
                detail.stg_four_years_ago = expiring_data["cds"]["exposure"]["granular"]["gmm_primary_exposure_details"][index]["four_years_ago"]
                detail.stg_five_years_ago = expiring_data["cds"]["exposure"]["granular"]["gmm_primary_exposure_details"][index]["five_years_ago"]

            for index, detail in enumerate(hxd.cds.exposure.granular.gmm_secondary_exposure_details):
                detail.stg_current_year = expiring_data["cds"]["exposure"]["granular"]["gmm_secondary_exposure_details"][index]["current_year"]
                detail.stg_one_years_ago = expiring_data["cds"]["exposure"]["granular"]["gmm_secondary_exposure_details"][index]["one_years_ago"]
                detail.stg_two_years_ago = expiring_data["cds"]["exposure"]["granular"]["gmm_secondary_exposure_details"][index]["two_years_ago"]
                detail.stg_three_years_ago = expiring_data["cds"]["exposure"]["granular"]["gmm_secondary_exposure_details"][index]["three_years_ago"]
                detail.stg_four_years_ago = expiring_data["cds"]["exposure"]["granular"]["gmm_secondary_exposure_details"][index]["four_years_ago"]
                detail.stg_five_years_ago = expiring_data["cds"]["exposure"]["granular"]["gmm_secondary_exposure_details"][index]["five_years_ago"]

            for index, detail in enumerate(hxd.cds.exposure.granular.glsn_primary_exposure_details):
                detail.stg_current_year = expiring_data["cds"]["exposure"]["granular"]["glsn_primary_exposure_details"][index]["current_year"]
                detail.stg_one_years_ago = expiring_data["cds"]["exposure"]["granular"]["glsn_primary_exposure_details"][index]["one_years_ago"]
                detail.stg_two_years_ago = expiring_data["cds"]["exposure"]["granular"]["glsn_primary_exposure_details"][index]["two_years_ago"]
                detail.stg_three_years_ago = expiring_data["cds"]["exposure"]["granular"]["glsn_primary_exposure_details"][index]["three_years_ago"]
                detail.stg_four_years_ago = expiring_data["cds"]["exposure"]["granular"]["glsn_primary_exposure_details"][index]["four_years_ago"]
                detail.stg_five_years_ago = expiring_data["cds"]["exposure"]["granular"]["glsn_primary_exposure_details"][index]["five_years_ago"]

            for index, detail in enumerate(hxd.cds.exposure.granular.glsn_secondary_exposure_details):
                detail.stg_current_year = expiring_data["cds"]["exposure"]["granular"]["glsn_secondary_exposure_details"][index]["current_year"]
                detail.stg_one_years_ago = expiring_data["cds"]["exposure"]["granular"]["glsn_secondary_exposure_details"][index]["one_years_ago"]
                detail.stg_two_years_ago = expiring_data["cds"]["exposure"]["granular"]["glsn_secondary_exposure_details"][index]["two_years_ago"]
                detail.stg_three_years_ago = expiring_data["cds"]["exposure"]["granular"]["glsn_secondary_exposure_details"][index]["three_years_ago"]
                detail.stg_four_years_ago = expiring_data["cds"]["exposure"]["granular"]["glsn_secondary_exposure_details"][index]["four_years_ago"]
                detail.stg_five_years_ago = expiring_data["cds"]["exposure"]["granular"]["glsn_secondary_exposure_details"][index]["five_years_ago"]
        

            # save Expiry inception date in the Data schema
            hxd.cds.expiry_inception_date = expiring_data["hx_core"]["inception_date"]
            # Add tasks which must be done before starting a policy here >>
            roll_exposure_fields_task(hxd, progress)

    # case where there is model update
    else:
        if hxd.model_state.expiring_policy_option_id != None:
            # Default renewal flag to true upon renewal    
            hxd.cds.standard_fields.is_renewal = True 
        
        
        print(f'hxd.model_state.policy_option_updated_from_id: {hxd.model_state.policy_option_updated_from_id}')
        # get data from beofre the model version update
        pre_update_response = hx_renew.snapshots.get_snapshot(policy_option_id=hxd.model_state.policy_option_updated_from_id, stream=False)

        if pre_update_response.status_code != 200:
            raise Exception(pre_update_response.json())
        
        rate_changes = [    
            "exposure_change",
            "risk_characteristics_change",
            "limit_change",
            "deductible_change",
            "terms_conditions_change",
            "other_change",
            "brokerage_change"
        ]

        pre_update_data = pre_update_response.json()["data"]
        for idx, layer in enumerate(hxd.cds.layers):
            # layer.status = pre_update_data["cds"]["layers"][idx]["status"]
            # layer.bound_premium = pre_update_data["cds"]["layers"][idx]["bound_premium"]
            # layer.section_reference = pre_update_data["cds"]["layers"][idx]["section_reference"]

            for change in rate_changes:
                attr = getattr(layer.rate_change, change)
                # attr.comments = pre_update_data["cds"]["layers"][idx]["rate_change"][change]["comments"]
                attr.uw_selected.calculated = pre_update_data["cds"]["layers"][idx]["rate_change"][change]["uw_selected"]["selected"]

        # IH edit - set value to the exposure nodes as per before the model update
        for index, detail in enumerate(hxd.cds.exposure.granular.gmm_primary_exposure_details):
            detail.current_year = pre_update_data["cds"]["exposure"]["granular"]["gmm_primary_exposure_details"][index]["current_year"]
            detail.one_years_ago = pre_update_data["cds"]["exposure"]["granular"]["gmm_primary_exposure_details"][index]["one_years_ago"]
            detail.two_years_ago = pre_update_data["cds"]["exposure"]["granular"]["gmm_primary_exposure_details"][index]["two_years_ago"]
            detail.three_years_ago = pre_update_data["cds"]["exposure"]["granular"]["gmm_primary_exposure_details"][index]["three_years_ago"]
            detail.four_years_ago = pre_update_data["cds"]["exposure"]["granular"]["gmm_primary_exposure_details"][index]["four_years_ago"]
            detail.five_years_ago = pre_update_data["cds"]["exposure"]["granular"]["gmm_primary_exposure_details"][index]["five_years_ago"]

        for index, detail in enumerate(hxd.cds.exposure.granular.gmm_secondary_exposure_details):
            detail.current_year = pre_update_data["cds"]["exposure"]["granular"]["gmm_secondary_exposure_details"][index]["current_year"]
            detail.one_years_ago = pre_update_data["cds"]["exposure"]["granular"]["gmm_secondary_exposure_details"][index]["one_years_ago"]
            detail.two_years_ago = pre_update_data["cds"]["exposure"]["granular"]["gmm_secondary_exposure_details"][index]["two_years_ago"]
            detail.three_years_ago = pre_update_data["cds"]["exposure"]["granular"]["gmm_secondary_exposure_details"][index]["three_years_ago"]
            detail.four_years_ago = pre_update_data["cds"]["exposure"]["granular"]["gmm_secondary_exposure_details"][index]["four_years_ago"]
            detail.five_years_ago = pre_update_data["cds"]["exposure"]["granular"]["gmm_secondary_exposure_details"][index]["five_years_ago"]

        for index, detail in enumerate(hxd.cds.exposure.granular.glsn_primary_exposure_details):
            detail.current_year = pre_update_data["cds"]["exposure"]["granular"]["glsn_primary_exposure_details"][index]["current_year"]
            detail.one_years_ago = pre_update_data["cds"]["exposure"]["granular"]["glsn_primary_exposure_details"][index]["one_years_ago"]
            detail.two_years_ago = pre_update_data["cds"]["exposure"]["granular"]["glsn_primary_exposure_details"][index]["two_years_ago"]
            detail.three_years_ago = pre_update_data["cds"]["exposure"]["granular"]["glsn_primary_exposure_details"][index]["three_years_ago"]
            detail.four_years_ago = pre_update_data["cds"]["exposure"]["granular"]["glsn_primary_exposure_details"][index]["four_years_ago"]
            detail.five_years_ago = pre_update_data["cds"]["exposure"]["granular"]["glsn_primary_exposure_details"][index]["five_years_ago"]

        for index, detail in enumerate(hxd.cds.exposure.granular.glsn_secondary_exposure_details):
            detail.current_year = pre_update_data["cds"]["exposure"]["granular"]["glsn_secondary_exposure_details"][index]["current_year"]
            detail.one_years_ago = pre_update_data["cds"]["exposure"]["granular"]["glsn_secondary_exposure_details"][index]["one_years_ago"]
            detail.two_years_ago = pre_update_data["cds"]["exposure"]["granular"]["glsn_secondary_exposure_details"][index]["two_years_ago"]
            detail.three_years_ago = pre_update_data["cds"]["exposure"]["granular"]["glsn_secondary_exposure_details"][index]["three_years_ago"]
            detail.four_years_ago = pre_update_data["cds"]["exposure"]["granular"]["glsn_secondary_exposure_details"][index]["four_years_ago"]
            detail.five_years_ago = pre_update_data["cds"]["exposure"]["granular"]["glsn_secondary_exposure_details"][index]["five_years_ago"]

        # set value of previous base premium in line with original expiry option. This allows accurate amount when the renewal uses a different COB        
        # Use the .get() method to safely access the key and provide a default value of 0 if the key is missing
        temp_gmm_total_base_premium = pre_update_data["cds"]["exposure"]["aggregate"].get("temp_gmm_total_base_premium_one_years_ago", 0)
        hxd.cds.exposure.aggregate.temp_gmm_total_base_premium_one_years_ago = temp_gmm_total_base_premium  

        temp_glsn_total_base_premium = pre_update_data["cds"]["exposure"]["aggregate"].get("temp_glsn_total_base_premium_one_years_ago", 0)
        hxd.cds.exposure.aggregate.temp_glsn_total_base_premium_one_years_ago = temp_glsn_total_base_premium


    # Set temp expiry base premiums from expiry options if it exist, if not set to zero. The final value will be calculated in the rating.
    if hxd.model_state.expiring_policy_option_id != None:
        # get expiry data from original option
        expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=hxd.model_state.expiring_policy_option_id, stream=False)

        if expiring_response.status_code != 200:
            raise Exception(expiring_response.json())
        
        expiring_data = expiring_response.json()["data"]

        # get expiry currency in the temp node
        if expiring_data["cds"]["currencies"]["source_currency"]: # checking currency node for model version all inputs exist 
            temp_expiry_currency = expiring_data["cds"]["currencies"]["source_currency"] # using all input model structure, input node
        else:
            temp_expiry_currency = expiring_data["cds"]["rating_factors"]["currency"]["selected"] # using latest model stucture, override node

        
        # get rate of exchange of current and expiry currency 
        fx_rates = params.fx_rates.df() # FX rate for currency conversion - from user library
        expiry_exchange_rate = utils.look_up(temp_expiry_currency, 'ccy', 'fx_rate', fx_rates, if_not_found=1) # default to USD if error
        expiry_fx_to_usd = 1 / expiry_exchange_rate
        current_exchange_rate = utils.look_up(hxd.cds.rating_factors.currency.selected, 'ccy', 'fx_rate', fx_rates, if_not_found=1) # default to USD if error
        current_fx_to_usd = 1 / current_exchange_rate

        # set value of previous base premium in line with original expiry option. This allows accurate amount when the renewal uses a different COB.
        hxd.cds.exposure.aggregate.temp_gmm_total_base_premium_one_years_ago = (expiring_data["cds"]["exposure"]["aggregate"]["gmm_total_base_premium_current_year"] or 0) * expiry_fx_to_usd / current_fx_to_usd 
        hxd.cds.exposure.aggregate.temp_glsn_total_base_premium_one_years_ago = (expiring_data["cds"]["exposure"]["aggregate"]["glsn_total_base_premium_current_year"]or 0 ) * expiry_fx_to_usd / current_fx_to_usd

    else:
        # if there is not expiry data in HX, set value of the temp previous base premium in line with original expiry option.
        hxd.cds.exposure.aggregate.temp_gmm_total_base_premium_one_years_ago =  0
        hxd.cds.exposure.aggregate.temp_glsn_total_base_premium_one_years_ago =  0


def clear_values(hxd, progress):
    rate_changes = [    
        "exposure_change",
        "risk_characteristics_change",
        "limit_change",
        "deductible_change",
        "terms_conditions_change",
        "other_change",
        "brokerage_change"
    ]

    # Push to hxd
    for idx, layer in enumerate(hxd.cds.layers):
        layer.status = None
        layer.bound_premium = None
        layer.section_reference = None

        for change in rate_changes:
            attr = getattr(layer.rate_change, change)
            setattr(attr, "comments", "")

    clear_overrides_task(hxd, progress)

    

@hx.task
def pricing_copy_option(hxd, progress):
    cds = hxd.cds
    options_dict = [{
        "coverages.professional_liability.retention": item.coverages.professional_liability.retention,
        "coverages.professional_liability.per_claim_limit":item.coverages.professional_liability.per_claim_limit,
        "coverages.professional_liability.aggregate_limit": item.coverages.professional_liability.aggregate_limit,

        "coverages.general_liability.retention": item.coverages.general_liability.retention,
        "coverages.general_liability.per_claim_limit":item.coverages.general_liability.per_claim_limit,
        "coverages.general_liability.aggregate_limit": item.coverages.general_liability.aggregate_limit,

        "coverages.product_liability.retention": item.coverages.product_liability.retention,
        "coverages.product_liability.per_claim_limit":item.coverages.product_liability.per_claim_limit,
        "coverages.product_liability.aggregate_limit": item.coverages.product_liability.aggregate_limit,

        "coverages.eo.retention": item.coverages.eo.retention,
        "coverages.eo.per_claim_limit":item.coverages.eo.per_claim_limit,
        "coverages.eo.aggregate_limit": item.coverages.eo.aggregate_limit,

        "coverages.employers_liability.retention": item.coverages.employers_liability.retention,
        "coverages.employers_liability.per_claim_limit":item.coverages.employers_liability.per_claim_limit,
        "coverages.employers_liability.aggregate_limit": item.coverages.employers_liability.aggregate_limit,

        "coverages.sexual_abuse.retention": item.coverages.sexual_abuse.retention,
        "coverages.sexual_abuse.per_claim_limit":item.coverages.sexual_abuse.per_claim_limit,
        "coverages.sexual_abuse.aggregate_limit": item.coverages.sexual_abuse.aggregate_limit,            

        "coverages.employee_benefits_liability.retention": item.coverages.employee_benefits_liability.retention,
        "coverages.employee_benefits_liability.per_claim_limit":item.coverages.employee_benefits_liability.per_claim_limit,
        "coverages.employee_benefits_liability.aggregate_limit": item.coverages.employee_benefits_liability.aggregate_limit,

        "coverages.tech_eo_products_media.retention": item.coverages.tech_eo_products_media.retention,
        "coverages.tech_eo_products_media.per_claim_limit":item.coverages.tech_eo_products_media.per_claim_limit,
        "coverages.tech_eo_products_media.aggregate_limit": item.coverages.tech_eo_products_media.aggregate_limit,

        "coverages.healthcare_professional_liability.retention": item.coverages.healthcare_professional_liability.retention,
        "coverages.healthcare_professional_liability.per_claim_limit":item.coverages.healthcare_professional_liability.per_claim_limit,
        "coverages.healthcare_professional_liability.aggregate_limit": item.coverages.healthcare_professional_liability.aggregate_limit,

        "coverages.product_recall.retention": item.coverages.product_recall.retention,
        "coverages.product_recall.per_claim_limit":item.coverages.product_recall.per_claim_limit,
        "coverages.product_recall.aggregate_limit": item.coverages.product_recall.aggregate_limit,            

        "coverages.well_tech_eo_media.retention": item.coverages.well_tech_eo_media.retention,
        "coverages.well_tech_eo_media.per_claim_limit":item.coverages.well_tech_eo_media.per_claim_limit,
        "coverages.well_tech_eo_media.aggregate_limit": item.coverages.well_tech_eo_media.aggregate_limit, 

        "agg_limit": item.agg_limit,
        "agg_retention": item.agg_retention,
        "indemnity_only": item.indemnity_only,

        "include_auto_primary": item.include_auto_primary,
        "auto_measure": item.auto_measure,
        "auto_amount": item.auto_amount,

        "include_stop_gap_primary": item.include_stop_gap_primary,

        "include_tria_primary": item.include_tria_primary,

        "include_punitive_damages_primary": item.include_punitive_damages_primary,

        "costs_in_addition_selection": item.costs_in_addition_selection,
        "include_costs_in_addition_primary": item.include_costs_in_addition_primary,

        "brokerage_primary": item.brokerage_primary,
        "quoted_premium_primary": item.quoted_premium_primary,

        "per_claim_limit_1_excess": item.per_claim_limit_1_excess,
        "aggregate_limit_1_excess": item.aggregate_limit_1_excess,
        "brokerage_1_excess": item.brokerage_1_excess,
        "quoted_premium_1_excess": item.quoted_premium_1_excess,

        "per_claim_limit_2_excess": item.per_claim_limit_2_excess,
        "aggregate_limit_2_excess": item.aggregate_limit_2_excess,
        "brokerage_2_excess": item.brokerage_2_excess,
        "quoted_premium_2_excess": item.quoted_premium_2_excess,

        "per_claim_limit_3_excess": item.per_claim_limit_3_excess,
        "aggregate_limit_3_excess": item.aggregate_limit_3_excess,
        "brokerage_3_excess": item.brokerage_3_excess,
        "quoted_premium_3_excess": item.quoted_premium_3_excess,

        "per_claim_limit_4_excess": item.per_claim_limit_4_excess,
        "aggregate_limit_4_excess": item.aggregate_limit_4_excess,
        "brokerage_4_excess": item.brokerage_4_excess,
        "quoted_premium_4_excess": item.quoted_premium_4_excess,

        "per_claim_limit_5_excess": item.per_claim_limit_5_excess,
        "aggregate_limit_5_excess": item.aggregate_limit_5_excess,
        "brokerage_5_excess": item.brokerage_5_excess,
        "quoted_premium_5_excess": item.quoted_premium_5_excess,

        "per_claim_limit_6_excess": item.per_claim_limit_6_excess,
        "aggregate_limit_6_excess": item.aggregate_limit_6_excess,
        "brokerage_6_excess": item.brokerage_6_excess,
        "quoted_premium_6_excess": item.quoted_premium_6_excess,

        "per_claim_limit_7_excess": item.per_claim_limit_7_excess,
        "aggregate_limit_7_excess": item.aggregate_limit_7_excess,
        "brokerage_7_excess": item.brokerage_7_excess,
        "quoted_premium_7_excess": item.quoted_premium_7_excess,

        "per_claim_limit_8_excess": item.per_claim_limit_8_excess,
        "aggregate_limit_8_excess": item.aggregate_limit_8_excess,
        "brokerage_8_excess": item.brokerage_8_excess,
        "quoted_premium_8_excess": item.quoted_premium_8_excess,

        "per_claim_limit_9_excess": item.per_claim_limit_9_excess,
        "aggregate_limit_9_excess": item.aggregate_limit_9_excess,
        "brokerage_9_excess": item.brokerage_9_excess,
        "quoted_premium_9_excess": item.quoted_premium_9_excess,

        "per_claim_limit_10_excess": item.per_claim_limit_10_excess,
        "aggregate_limit_10_excess": item.aggregate_limit_10_excess,
        "brokerage_10_excess": item.brokerage_10_excess,
        "quoted_premium_10_excess": item.quoted_premium_10_excess,

        } for item in cds.options]
    options = pd.DataFrame(options_dict)
    copy_option_from = int(cds.copy_option_from[-1]) - 1
    copy_option_to = int(cds.copy_option_to[-1]) - 1

    options.iloc[copy_option_to] = options.iloc[copy_option_from]
    #options = options.fillna(0)

    if cds.gmm_masking:
        coverages = ["professional_liability","general_liability","product_liability","eo","sexual_abuse","employee_benefits_liability","employers_liability","tech_eo_products_media"]
    elif cds.glsn_masking:
        coverages = ["product_liability","eo","healthcare_professional_liability","general_liability","sexual_abuse","employee_benefits_liability","product_recall","well_tech_eo_media"]    
    
    values = ["retention", "per_claim_limit", "aggregate_limit"]

    for coverage in coverages:
        coverage_obj = getattr(cds.options[copy_option_to].coverages, coverage)
        for value in values:
            if pd.isna(options[f"coverages.{coverage}.{value}"].iloc[copy_option_to]):
                setattr(coverage_obj, value, None)
            else:
                setattr(coverage_obj, value, options[f"coverages.{coverage}.{value}"].iloc[copy_option_to])
    
    other_copy_values = ["agg_limit", "agg_retention", "indemnity_only", "include_auto_primary","auto_measure",\
         "auto_amount", "include_stop_gap_primary", "include_tria_primary", "include_punitive_damages_primary", "costs_in_addition_selection", "include_costs_in_addition_primary", "brokerage_primary", "quoted_premium_primary"]

    for item in other_copy_values:
        if pd.isna(options[f"{item}"].iloc[copy_option_to]):
            setattr(cds.options[copy_option_to], item, None)
        else:    
            setattr(cds.options[copy_option_to], item, options[f"{item}"].iloc[copy_option_to])
   
    excess_value = ["per_claim_limit_", "aggregate_limit_", "brokerage_", "quoted_premium_"]
    excess_layers = ["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"]

    for layer in excess_layers:
        if pd.isna(options[f"per_claim_limit_{layer}"].iloc[copy_option_to]):
            setattr(cds.options[copy_option_to], f"per_claim_limit_{layer}", None)
        else:
            setattr(cds.options[copy_option_to], f"per_claim_limit_{layer}", options[f"per_claim_limit_{layer}"].iloc[copy_option_to])

        if pd.isna(options[f"aggregate_limit_{layer}"].iloc[copy_option_to]):
            setattr(cds.options[copy_option_to], f"aggregate_limit_{layer}", None)
        else:
            setattr(cds.options[copy_option_to], f"aggregate_limit_{layer}", options[f"aggregate_limit_{layer}"].iloc[copy_option_to])

        if pd.isna(options[f"brokerage_{layer}"].iloc[copy_option_to]):
            setattr(cds.options[copy_option_to], f"brokerage_{layer}", None)
        else:
            setattr(cds.options[copy_option_to], f"brokerage_{layer}", options[f"brokerage_{layer}"].iloc[copy_option_to])

        if pd.isna(options[f"quoted_premium_{layer}"].iloc[copy_option_to]):
            setattr(cds.options[copy_option_to], f"quoted_premium_{layer}", None)
        else:
            setattr(cds.options[copy_option_to], f"quoted_premium_{layer}", options[f"quoted_premium_{layer}"].iloc[copy_option_to])


@hx.task
def cyber_copy_option(hxd, progress):
    cds = hxd.cds
    cyber_options_dict = [{
        "policy_agg_limit": item.policy_agg_limit,
        "notified_individuals_limit": item.notified_individuals_limit,
        "policy_agg_retention": item.policy_agg_retention,
        "legal_forensic_limit": item.legal_forensic_limit,
        "additional_breach_costs_limit": item.additional_breach_costs_limit,
        "infosec_breach_response_limit":item.infosec_breach_response_limit,
        "data_network_limit": item.data_network_limit,
        "legal_forensic_retention": item.legal_forensic_retention,
        "legal_forensic_subretention": item.legal_forensic_subretention,
        "policy_agg_retention": item.policy_agg_retention,
        "breach_response_retention": item.breach_response_retention,
        "defense_penalties_limit": item.defense_penalties_limit,
        "payment_card_limit": item.payment_card_limit,
        "brokerage": item.brokerage,
        "model_premium_bbr_rater": item.model_premium_bbr_rater
        } for item in cds.cyber_options]
        
    cyber_options_df = pd.DataFrame(cyber_options_dict)

    copy_option_from = int(cds.cyber_copy_option_from[-1]) - 1
    copy_option_to = int(cds.cyber_copy_option_to[-1]) - 1

    cyber_options_df.iloc[copy_option_to] = cyber_options_df.iloc[copy_option_from]
    #pd.isna(cyber_options_df) = None
    #cyber_options_df = cyber_options_df.fillna(0)

    if cds.bbr_masking:
        cyber_values = ["policy_agg_limit", "notified_individuals_limit", "policy_agg_retention", "legal_forensic_limit","additional_breach_costs_limit", "data_network_limit",\
            "legal_forensic_retention", "legal_forensic_subretention", "policy_agg_retention", "defense_penalties_limit", "payment_card_limit","brokerage","model_premium_bbr_rater"]
    elif cds.infosec_masking:
        cyber_values = ["policy_agg_limit", "infosec_breach_response_limit", "data_network_limit",\
            "policy_agg_retention", "breach_response_retention", "defense_penalties_limit", "payment_card_limit","brokerage","model_premium_bbr_rater"]  

    for item in cyber_values:
        if pd.isna(cyber_options_df[f"{item}"].iloc[copy_option_to]):
            setattr(cds.cyber_options[copy_option_to], item, None)
        else:
            setattr(cds.cyber_options[copy_option_to], item, cyber_options_df[f"{item}"].iloc[copy_option_to])
 
def format_note_field(value, key=None):
    if value is None:
        return ""
    if isinstance(value, dict):
        if key and key in value:
            content = value[key]
        elif len(value) > 0:
            content = next(iter(value.values()))
        else:
            content = ""
    else:
        content = value

    if not isinstance(content, str):
        return str(content)

    if re.search(r'<[A-Za-z]', content):
        content = _clean_html_preserve_tables(content)
    else:
        content = content.replace('\n', '<br>')

    return content

def _clean_html_preserve_tables(html_content):
    class TableCleaner(HTMLParser):
        def __init__(self):
            super().__init__()
            self.result = []
            self.in_table = False
            self.buffer = []

        def handle_starttag(self, tag, attrs):
            self._flush_buffer()
            if tag == "table":
                self.in_table = True
            self.result.append(self.get_starttag_text())

        def handle_endtag(self, tag):
            if tag == "table":
                self.in_table = False
            self._flush_buffer()
            self.result.append(f"</{tag}>")

        def handle_data(self, data):
            if self.in_table or data.strip():
                self.buffer.append(data)

        def _flush_buffer(self):
            if self.buffer:
                self.result.append("".join(self.buffer))
                self.buffer.clear()

        def get_clean_html(self):
            self._flush_buffer()
            return "".join(self.result)

    parser = TableCleaner()
    parser.feed(html_content)
    return parser.get_clean_html()

@hx.task
def generate_email_task(hxd, progress):

    insured_name = hxd.cds.standard_fields.insured_name or "TEST TEST TEST" # NOTE: can remove the "or" condition, it's just to always have it populated
    underwriter = hxd.cds.standard_fields.underwriter
    formatted_underwriter = underwriter.replace(" ", ".").lower()
    underwriter_email = formatted_underwriter + "@beazley.com"
    hxd.cds.email.sender = underwriter_email
    hxd.cds.email.recipient = underwriter_email

    ### --- Define data for each table --- ###

    # This is a normal table that can be formed from separate fields or come from a Structure
    risk_information = {
        "Insured": insured_name, # NOTE: update all these fields like the one above so they come from the hxd
        "Brokerage Firm": hxd.cds.standard_fields.broker, 
        "Broker Contact": hxd.cds.broker_contact,
        "Inception Date": hxd.hx_core.inception_date,
        "Expiry Date": hxd.hx_core.expiry_date,
        "US/International": hxd.cds.rating_factors.us_international_choice_of_law.us_international,
        "Choice of Law": hxd.cds.rating_factors.us_international_choice_of_law.choice_of_law,
        "Currency": hxd.cds.currencies.source_currency,
        "Revenue": f"{int(hxd.cds.exposure.aggregate.revenue):,}",
        "Account Score": hxd.cds.rating_factors.account_score,
        "Profit Status": hxd.cds.rating_factors.profit_status,
        "":"",
        "Product": hxd.cds.exposure.granular.gmm_product.product if hxd.cds.gmm_masking else  hxd.cds.exposure.granular.glsn_product.product ,
        "COB Code": hxd.cds.exposure.granular.gmm_product.cob_code_description if hxd.cds.gmm_masking else  hxd.cds.exposure.granular.glsn_product.cob_code_description,
        "Class": hxd.cds.exposure.granular.gmm_product.cob_class if hxd.cds.gmm_masking else None ,
        "Form / Product Override": hxd.cds.rating_factors.gmm.product_override if hxd.cds.gmm_masking else hxd.cds.rating_factors.glsn.form
    }
    
    # For account scorings
    account_scoring_list = hx.params.table_account_scoring["account_scoring_name"]
    account_scoring = [
            {
                "Feature": utils.title_rc(item),
                "Score": getattr(getattr(hxd.cds.rating_factors.account_scoring , item ),"value"),
                "Comment": getattr(getattr(hxd.cds.rating_factors.account_scoring , item ),"comment"),
                #... Add your other fields
            } for item in account_scoring_list 
            ]

    # GMM Primary Exposure details
    if hxd.cds.gmm_masking: 
        if hxd.cds.exposure.granular.gmm_product.product != "Triage":
            p_expo = hxd.cds.exposure.granular.gmm_primary_exposure_details
            primary_exposure_details = [
                {
                    "Class": item.exposure_class,
                    "Exposure Measure": item.exposure_measure,
                    "Base Rate": item.formatted_base_rate,
                    "Current Year": f"{int(item.current_year):,}",
                    "Use For Calculation": item.selection,
                    "Base Premium": f"{int(item.base_premium):,}",
                    #... Add your other fields
                } for item in p_expo if item.selection is not False # Adding this condition as you have a fixed number of items - feel free to change as appropriate
            ]
            if not primary_exposure_details:
                primary_exposure_details = [
                    {
                        "Class": "No Primary Classes Selected",
                    } 
                ] 
            # GMM Secondary Exposure details
            secondary_exposure_details = [
                {
                    "Class": item.gmm_secondary_exposure.exposure_class,
                    "Exposure Measure": item.gmm_secondary_exposure.exposure_measure,
                    "Base Rate": item.formatted_base_rate,
                    "Current Year": f"{int(item.current_year):,}",
                    "Use For Calculation": item.selection,
                    "Base Premium": f"{int(item.base_premium):,}",
                    #... Add your other fields
                } for item in hxd.cds.exposure.granular.gmm_secondary_exposure_details if item.selection is not False # Adding this condition as you have a fixed number of items - feel free to change as appropriate
            ]
            if not secondary_exposure_details:
                secondary_exposure_details = [
                    {
                        "Class": "No Secondary Classes Selected",
                    } 
                ] 
        else:
            
            triage_doc_res = [
                {
                    "Specialty": (item.specialty), 
                    "Employed Doctors Current Year": item.doc_current_year, 
                    "OBE Per Doctor": item.obe_per_doctor, 
                    "Residents Current Year": item.resident_current_year, 
                    "OBE Per Resident": item.obe_per_resident, 
                } for item in hxd.cds.exposure.granular.triage_doctors_residents if item.doc_current_year != 0 or item.resident_current_year != 0
            ]
            if not triage_doc_res:
                triage_doc_res = [
                    {
                        "Doctors and Residents": "No Doctors and Residents Entered",
                    } 
                ] 
            triage_procedures = [
                {
                    "Category": (item.category), 
                    "Exposure Measure": item.exposure_measure, 
                    "OBE or FTE": item.obe_or_fte, 
                    "Procedures Current Year": item.current_year, 
                } for item in hxd.cds.exposure.granular.triage_procedures if item.current_year != 0 
            ]
            if not triage_procedures:
                triage_procedures = [
                    {
                        "Procedures": "No Procedures Entered",
                    } 
                ]
            triage_total_obe = [
                {
                    "Total OBE": item.current_year , 
                } for item in hxd.cds.exposure.aggregate.triage_running_total_obe
            ]
            if not triage_total_obe:
                triage_total_obe = [
                    {
                        "Total OBE": "Total OBE Not a",
                    } 
                ]

    else:
        p_expo = hxd.cds.exposure.granular.glsn_primary_exposure_details
        primary_exposure_details = [
            {
                "Class": item.cob,
                "Exposure Base": item.exposure_base,
                "Exposure Measure": item.exposure_measure,
                "Base Rate": item.formatted_base_rate,
                "Current Year": f"{int(item.current_year):,}",
                "Use For Calculation": item.selection,
                "Base Premium": f"{int(item.base_premium):,}",
                #... Add your other fields
            } for item in p_expo if item.selection is not False # Adding this condition as you have a fixed number of items - feel free to change as appropriate
        ]
        if not primary_exposure_details:
                primary_exposure_details = [
                    {
                        "Class": "No Primary Classes Selected",
                    } 
                ] 
        # Glsn Secondary Exposure details
        secondary_exposure_details = [
                {
                    "Class": item.glsn_secondary_exposure.cob,
                    "Exposure Base": item.glsn_secondary_exposure.exposure_base,
                    "Exposure Measure": item.glsn_secondary_exposure.exposure_measure,
                    "Base Rate": item.formatted_base_rate,
                    "Current Year": f"{int(item.current_year):,}",
                    "Use For Calculation": item.selection,
                    "Base Premium": f"{int(item.base_premium):,}",
                    #... Add your other fields
                } for item in hxd.cds.exposure.granular.glsn_secondary_exposure_details if item.selection is not False # Adding this condition as you have a fixed number of items - feel free to change as appropriate
            ]
        if not secondary_exposure_details:
                secondary_exposure_details = [
                    {
                        "Class": "No Secondary Classes Selected",
                    } 
                ]   
        
            
    # Venue Factors
    venue_factors = {
        "Total Venue Splits": f"{hxd.cds.exposure.aggregate.total_percentage_selected *100:.0f}%", 
        "Total Venue Factor": f"{hxd.cds.exposure.aggregate.total_venue_factor:.2f}", 
    }

    venue_us_list = hx.params.table_venue_us["venue_name"]
    venue_us_params =  hx.params.table_venue_us
    venue_us_splits = [
            {
                "US Venue": venue_us_params[venue_us_params["venue_name"] == item]["venue_label"].iloc[0],
                "Factor": getattr(getattr(hxd.cds.exposure.granular , item ),"factor"),
                "Split %": f"{getattr(getattr(hxd.cds.exposure.granular , item ),'percentage')*100:.1f}%",
                "Use For Calculation": getattr(getattr(hxd.cds.exposure.granular , item ),"selection"),
                #... Add your other fields
            } for item in venue_us_list if getattr(getattr(hxd.cds.exposure.granular , item ),"selection") is not False # Adding this condition as you have a fixed number of items - feel free to change as appropriate
            ]
    if len(venue_us_splits) == 0 :
        venue_us_output = [
            {
                "Venue": "No US Venues Entered"
            } 
            ]
    else:
        venue_us_output = venue_us_splits    

    venue_international_list = hx.params.table_venue_international["venue_name"]
    venue_international_params =  hx.params.table_venue_international
    venue_international_splits = [
            {
                "US Venue": venue_international_params[venue_international_params["venue_name"] == item]["venue_label"].iloc[0],
                "Factor": getattr(getattr(hxd.cds.exposure.granular , item ),"factor"),
                "Split %": f"{getattr(getattr(hxd.cds.exposure.granular , item ),'percentage')*100:.1f}%",
                "Use For Calculation": getattr(getattr(hxd.cds.exposure.granular , item ),"selection"),
                #... Add your other fields
            } for item in venue_international_list if getattr(getattr(hxd.cds.exposure.granular , item ),"selection") is not False # Adding this condition as you have a fixed number of items - feel free to change as appropriate
            ]
    if len(venue_international_splits) == 0 :
        venue_international_output = [
            {
                "Venue": "No International Venues Entered"
            } 
            ]
    else:
        venue_international_output = venue_international_splits   

    # Pricing Section
    coverages = ["professional_liability","general_liability","product_liability","eo","sexual_abuse","employee_benefits_liability","employers_liability","tech_eo_products_media","healthcare_professional_liability","product_recall","well_tech_eo_media"]
   
    coverage_details = [
            {
                "Coverage": utils.title_rc(item),
                "Include in Primary": getattr(getattr(hxd.cds.rating_factors.pricing , item ),"include_primary"),
                "Include in Excess": getattr(getattr(hxd.cds.rating_factors.pricing , item ),"include_excess"),
                "Claim Basis": getattr(getattr(hxd.cds.rating_factors.pricing , item ),"claims_basis"),
                "Retroactive Date": getattr(getattr(hxd.cds.rating_factors.pricing , item ),"retroactive_date"),
                **({"Significant Coverage": getattr(getattr(hxd.cds.rating_factors.pricing, item), "significant_coverage")} if not hxd.cds.gmm_masking else {})
                #... Add your other fields
            } for item in coverages if getattr(getattr(hxd.cds.rating_factors.pricing , item ),"include_primary") is not False # Adding this condition as you have a fixed number of items - feel free to change as appropriate
    ]

    coverage_limits = []
    selected_option = int(hxd.cds.option_selected[-1]) -1 

    option = hxd.cds.options[selected_option].coverages
    option_name = f"Option {selected_option + 1}"

    # Make three rows per coverage
    for cvg in coverages:
        retention_dict = {
            "Coverage": utils.title_rc(cvg),
            "Name": "Retention",
            option_name: f"{int(getattr(getattr(option,cvg),'retention')):,}" if getattr(getattr(option,cvg),'retention') is not None else None
        }
        per_claim_limit_dict = {
            "Coverage": utils.title_rc(cvg),
            "Name": "Per Claim Limit",
            option_name: f"{int(getattr(getattr(option,cvg),'per_claim_limit')):,}" if getattr(getattr(option,cvg),'per_claim_limit') is not None else None
        }
        agg_limit_dict = {
            "Coverage": utils.title_rc(cvg),
            "Name": "Aggregate Limit",
            option_name: f"{int(getattr(getattr(option,cvg),'aggregate_limit')):,}" if getattr(getattr(option,cvg),'aggregate_limit') is not None else None
        }

        # Append to list
        coverage_limits.append(retention_dict)
        coverage_limits.append(per_claim_limit_dict)
        coverage_limits.append(agg_limit_dict)

        coverage_limits = [data for data in coverage_limits if data[f"Option {selected_option + 1}"] is not None]

    # Coverage Enhancements
    enhancement_option = hxd.cds.options[selected_option]
    enhancements = []
    stop_gap_dict = {
                "Coverage": "Stop Gap",
                "Include Primary": hxd.cds.options[selected_option].include_stop_gap_primary,
                "Include Excess": hxd.cds.rating_factors.pricing.include_stop_gap_excess,
                "Type":"N/A",
                "Amount":"N/A",
            } 
    tria_dict = {
                "Coverage": "TRIA",
                "Include Primary": hxd.cds.options[selected_option].include_tria_primary,
                "Include Excess": hxd.cds.rating_factors.pricing.include_tria_excess,
                "Type":"N/A",
                "Amount":"N/A",
            }   
    punitive_damages_dict = {
                "Coverage": "Punitive Damages",
                "Include Primary": hxd.cds.options[selected_option].include_punitive_damages_primary,
                "Include Excess": hxd.cds.rating_factors.pricing.include_punitive_damages_excess,
                "Type":"N/A",
                "Amount":"N/A",
            }  
    costs_in_addition_dict = {
                "Coverage": "Costs In Addition",
                "Include Primary": hxd.cds.options[selected_option].include_costs_in_addition_primary,
                "Include Excess": hxd.cds.rating_factors.pricing.include_costs_in_addition_excess,
                "Type": hxd.cds.options[selected_option].costs_in_addition_selection,
                "Amount":"N/A",
            } 
    auto_dict = {
        "Coverage": "Auto HNOA",
        "Include Primary": hxd.cds.options[selected_option].include_auto_primary,
        "Include Excess": hxd.cds.rating_factors.pricing.include_auto_excess,
        "Type": hxd.cds.options[selected_option].auto_measure,
        "Amount":hxd.cds.options[selected_option].auto_amount,
    } 
    enhancements.append(stop_gap_dict)
    enhancements.append(tria_dict)
    enhancements.append(punitive_damages_dict)
    enhancements.append(costs_in_addition_dict)
    enhancements.append(auto_dict)
    enhancements = [data for data in enhancements if data["Include Primary"]]

    if len(enhancements) == 0 :
        enhancements = [
            {
                "Enhancements": "No Coverage Enhancements Selected"
            } 
            ]
    else:
        enhancements = enhancements

    # Layer outputs  
    layer_path =  hxd.cds.options[selected_option]  
    primary_layer = [{
        "Brokerage": f"{layer_path.brokerage_primary * 100:.1f}%" if layer_path.brokerage_primary is not None else None, 
        "Cyber Premium": f"{layer_path.cyber_premium_primary:,.0f}" if layer_path.cyber_premium_primary is not None else None, 
        "Model Premium": f"{layer_path.model_premium_primary:,.0f}" if layer_path.model_premium_primary is not None else None, 
        "Minimum Premium": f"{layer_path.minimum_premium_primary:,.0f}" if layer_path.minimum_premium_primary is not None else None, 
        "Gross Premium": f"{layer_path.gross_premium_primary:,.0f}" if layer_path.gross_premium_primary is not None else None, 
        # "Uplift for NMP": f"{layer_path.uplift_for_nmp_primary:,.2f}" if layer_path.uplift_for_nmp_primary is not None else None, 
        "Quoted Premium": f"{layer_path.quoted_premium_primary:,.0f}" if layer_path.quoted_premium_primary is not None else None, 
        "BPI": f"{layer_path.bpi_primary * 100:.0f}%" if layer_path.bpi_primary is not None else None, 
    }]
    layers = ["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"]
    excess_layers = []
    for layer in layers : 
        layer_number = layer.split('_')[0]
        excess_dict = {
            "Excess Layer": f"Excess Layer {layer_number}",
            "Per Claim Limit": f"{getattr(layer_path,f'per_claim_limit_{layer}'):,.0f}" if getattr(layer_path,f'per_claim_limit_{layer}') is not None else None,
            "Aggregate Limit": f"{getattr(layer_path,f'aggregate_limit_{layer}'):,.0f}" if getattr(layer_path,f'aggregate_limit_{layer}') is not None else None,
            "Brokerage": f"{getattr(layer_path,f'brokerage_{layer}') * 100 :.1f}%" if getattr(layer_path,f'brokerage_{layer}') is not None else None,
            "Supported Excess Premium": f"{getattr(layer_path,f'supported_excess_premium_{layer}'):,.0f}" if getattr(layer_path,f'supported_excess_premium_{layer}') is not None else None,
            "Cyber Premium": f"{getattr(hxd.cds.cyber_options[selected_option],f'model_premium_third_party_{layer}'):.0f}" if getattr(hxd.cds.cyber_options[selected_option],f'model_premium_third_party_{layer}') is not None else None,
            "Umbrella Premium": f"{getattr(layer_path,f'umbrella_premium_{layer}'):,.0f}" if getattr(layer_path,f'umbrella_premium_{layer}') is not None else None,
            # "Uplift for NMP": f"{getattr(layer_path,f'uplift_for_nmp_{layer}'):,.2f}" if getattr(layer_path,f'uplift_for_nmp_{layer}') is not None else None,
            "Minimum Premium": f"{getattr(layer_path,f'minimum_premium_{layer}'):,.0f}" if getattr(layer_path,f'minimum_premium_{layer}') is not None else None,
            "Gross Premium": f"{getattr(layer_path,f'gross_premium_{layer}'):,.0f}" if getattr(layer_path,f'gross_premium_{layer}') is not None else None,
            "Quoted Premium": f"{getattr(layer_path,f'quoted_premium_{layer}'):,.0f}" if getattr(layer_path,f'quoted_premium_{layer}') is not None else None,
            "BPI": f"{getattr(layer_path,f'bpi_{layer}') * 100 :.0f}%" if getattr(layer_path,f'bpi_{layer}') is not None else None,
            "Comment": getattr(layer_path,f"comment_{layer}"),
        }
        excess_layers.append(excess_dict)
    excess_layers = [data for data in excess_layers if data["Per Claim Limit"] is not None]
    if len(excess_layers) == 0 :
        excess_layers = [
            {
                "Excess Layers": "No Excess Layers Entered"
            } 
            ]
    else:
        excess_layers = excess_layers 

   # Tech EO Section
    if hxd.cds.rating_factors.pricing.tech_eo_products_media.include_primary or hxd.cds.rating_factors.pricing.well_tech_eo_media.include_primary:
        tech_eo_name = hx.params.table_tech_eo["industry_class_name"]
        
        tech_eo_coverage_details = [
                {
                    "Industry Class": utils.title_rc(item),
                    "% of Rateable Revenue": f"{(getattr(getattr(hxd.cds.exposure.granular , item ),'tech_eo_percent_rateble_revenue')) * 100:.0f}%" if (getattr(getattr(hxd.cds.exposure.granular , item ),'tech_eo_percent_rateble_revenue')) is not None else None,
                    "Class": getattr(getattr(hxd.cds.exposure.granular , item ),"tech_eo_class"),
                    "Revenue": f"{getattr(getattr(hxd.cds.exposure.granular , item ),'tech_eo_revenue'):,.0f}" if getattr(getattr(hxd.cds.exposure.granular , item ),'tech_eo_revenue') is not None else None,

                } for item in tech_eo_name if getattr(getattr(hxd.cds.exposure.granular , item ),"tech_eo_percent_rateble_revenue") > 0 
        ]
        
        if len(tech_eo_coverage_details) == 0 :
            tech_eo_coverage_details = [
                {
                    "Tech EO": "No Tech EO Coverage Entered"
                } 
                ]
            tech_rateable = { "Tech EO Rateable Revenue %": ""}
        else:
            if hxd.cds.gmm_masking:
                tech_rateable = { "Tech EO Rateable Revenue %": f"{hxd.cds.exposure.aggregate.tech_eo_rateble_revenue* 100: .0f}%"} 
            else:
                tech_rateable = { 
                    "Tech EO Rateable Revenue %": f"{hxd.cds.exposure.aggregate.tech_eo_rateble_revenue* 100: .0f}%",
                    "Contingent BI/PD Selection": hxd.cds.rating_factors.tech_eo.contingent_bi_pd
                }
            tech_eo_coverage_details = tech_eo_coverage_details  
  
    # Cyber details
    if hxd.cds.rating_factors.cyber.product is not None :
        cyber_details =  {
                    "Cyber Product": hxd.cds.rating_factors.cyber.product,
                    "Notified Individuals": f"{hxd.cds.cyber_options[selected_option].notified_individuals_limit:,.0f}" if hxd.cds.cyber_options[selected_option].notified_individuals_limit is not None else None,
                    "Legal, Forensic & PR Limit": f"{hxd.cds.cyber_options[selected_option].legal_forensic_limit:,.0f}" if hxd.cds.cyber_options[selected_option].legal_forensic_limit is not None else None,
                    "Additional Breach Resp. Costs":  f"{hxd.cds.cyber_options[selected_option].additional_breach_costs_limit:,.0f}" if hxd.cds.cyber_options[selected_option].additional_breach_costs_limit is not None else "Not Purchased",
                    "Policy Aggregate Limit of Lia": f"{hxd.cds.cyber_options[selected_option].policy_agg_limit:,.0f}" if hxd.cds.cyber_options[selected_option].policy_agg_limit is not None else None,
                    "InfoSec Breach Response Limit": f"{hxd.cds.cyber_options[selected_option].infosec_breach_response_limit:,.0f}" if hxd.cds.cyber_options[selected_option].infosec_breach_response_limit is not None else None,
                    "Data & Network Limit": f"{hxd.cds.cyber_options[selected_option].data_network_limit:,.0f}" if hxd.cds.cyber_options[selected_option].data_network_limit is not None else "Not Purchased",
                    "Reg. Defense & Penalties Limit": f"{hxd.cds.cyber_options[selected_option].defense_penalties_limit:,.0f}" if hxd.cds.cyber_options[selected_option].defense_penalties_limit is not None else "Not Purchased",
                    "Payment Card Lia. & Costs Limit": f"{hxd.cds.cyber_options[selected_option].payment_card_limit:,.0f}"if hxd.cds.cyber_options[selected_option].payment_card_limit is not None else "Not Purchased",
                    "Legal Forensic & PR Retention": f"{hxd.cds.cyber_options[selected_option].legal_forensic_retention:,.0f}" if hxd.cds.cyber_options[selected_option].legal_forensic_retention is not None else None,
                    "Legal Subretention": f"{hxd.cds.cyber_options[selected_option].legal_forensic_subretention:,.0f}" if hxd.cds.cyber_options[selected_option].legal_forensic_subretention is not None else None,
                    "Agg. Per Incident, Claim, or Loss Retention": f"{hxd.cds.cyber_options[selected_option].policy_agg_retention:,.0f}" if hxd.cds.cyber_options[selected_option].policy_agg_retention is not None else None,
                    "Data & Network Retention": f"{hxd.cds.cyber_options[selected_option].data_network_retention.selected:,.0f}" if hxd.cds.cyber_options[selected_option].data_network_retention.selected is not None else None,
                    "Reg.Defense Penalites Retention": f"{hxd.cds.cyber_options[selected_option].defense_penalties_retention.selected:,.0f}" if hxd.cds.cyber_options[selected_option].defense_penalties_retention.selected is not None else None,
                    "Payment Card Retention": f"{hxd.cds.cyber_options[selected_option].payment_card_retention.selected:,.0f}" if hxd.cds.cyber_options[selected_option].payment_card_retention.selected is not None else None,
                    "InfoSec Breach Response Retention": f"{hxd.cds.cyber_options[selected_option].breach_response_retention:,.0f}" if hxd.cds.cyber_options[selected_option].breach_response_retention is not None else None,
                }

        cyber_details_schedule_mods =  {
                "Cyber Schedule Rating: Financial Condition": f"{hxd.cds.modifiers.cyber.cyber_financial_condition.value * 100: .0f}%" if hxd.cds.modifiers.cyber.cyber_financial_condition.value is not None else None,
                "Cyber Schedule Rating: Financial Condition Comment": hxd.cds.modifiers.cyber.cyber_financial_condition.comment,
                "Cyber Schedule Rating: Maturity of Business": f"{hxd.cds.modifiers.cyber.cyber_maturity_of_business.value * 100: .0f}%" if hxd.cds.modifiers.cyber.cyber_maturity_of_business.value is not None else None,
                "Cyber Schedule Rating: Maturity of Business Comment": hxd.cds.modifiers.cyber.cyber_maturity_of_business.comment,
                "Cyber Schedule Rating: Quality of Management": f"{hxd.cds.modifiers.cyber.cyber_quality_of_management.value * 100: .0f}%" if hxd.cds.modifiers.cyber.cyber_quality_of_management.value is not None else None,
                "Cyber Schedule Rating: Quality of Management Comment": hxd.cds.modifiers.cyber.cyber_quality_of_management.comment,
                "Cyber Schedule Rating: Volume of Information Stored": f"{hxd.cds.modifiers.cyber.cyber_volume_of_information_stored.value * 100: .0f}%" if hxd.cds.modifiers.cyber.cyber_volume_of_information_stored.value is not None else None,
                "Cyber Schedule Rating: Volume of Information Stored Comment": hxd.cds.modifiers.cyber.cyber_volume_of_information_stored.comment,
                "Cyber Schedule Rating: Cyber Loss Rating": hxd.cds.modifiers.cyber.cyber_loss_rating[0].cyber_loss_ratio,
                "Cyber Schedule Rating: Cyber Loss Rating Comment": hxd.cds.modifiers.cyber.cyber_loss_rating[0].cyber_loss_ratio_selected,
            }
        
        if hxd.cds.cyber_options[selected_option].model_premium_bbr_rater is not None:
            cyber_totals =  {
                "Cyber First Party and Third Party Premium":  f"{hxd.cds.cyber_options[selected_option].model_premium_bbr_rater:,.0f}" if hxd.cds.cyber_options[selected_option].model_premium_bbr_rater is not None else None,
            }
        else:
            cyber_totals =  {
                "Cyber Brokerage": f"{hxd.cds.cyber_options[selected_option].brokerage * 100: .1f}%" if hxd.cds.cyber_options[selected_option].brokerage is not None else None,
                "Cyber Third Party Premium": f"{hxd.cds.cyber_options[selected_option].model_premium_third_party:,.0f}" if hxd.cds.cyber_options[selected_option].model_premium_third_party is not None else None,
            }

    



    # Umbrella Coverage
    if hxd.cds.gmm_masking:
        umbrella_name = hx.params.table_gmm_umbrella["umbrella_name"]
        umbrella_inputs = [
                {
                    "Description": utils.title_rc(item),
                    "Actual EE Underling": f"{getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'underlying_ee'):,.0f}" if getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'underlying_ee') is not None else None,
                    "Actual Agg Underling": f"{getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'underlying_agg'):,.0f}"if getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'underlying_agg') is not None else None,
                    "Underlying Premium": f"{getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'underlying_premium'):,.0f}"if getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'underlying_premium') is not None else None,
                    "Occurrence Cover?": getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'occurrence_cover') if getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'occurrence_cover') is not None else None,

                } for item in umbrella_name if getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'occurrence_cover') is not False
        ]
        umbrella_outputs = []
        umbrella_layers = ["premium_primary", "premium_1_excess", "premium_2_excess", "premium_3_excess", "premium_4_excess", "premium_5_excess", "premium_6_excess", "premium_7_excess", "premium_8_excess", "premium_9_excess", "premium_10_excess"]
        for item in umbrella_name: 
            umbrella_dict = {
                "Description": utils.title_rc(item),
            } 
            for node in umbrella_layers:
                premium = getattr(getattr(hxd.cds.options[selected_option], f"gmm_{item}"), node) 
                if premium != 0: 
                    umbrella_dict[utils.title_rc(node)] = f"{int(premium):,}"
            umbrella_outputs.append(umbrella_dict)
        umbrella_outputs = [entry for entry in umbrella_outputs if entry.get("Premium 1 Excess",0) != 0]
    else:
        umbrella_name = hx.params.table_glsn_umbrella["umbrella_name"]
        umbrella_inputs = [
                {
                    "Description": utils.title_rc(item),
                    "Actual EE Underling": f"{getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'underlying_ee'):,.0f}" if getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'underlying_ee') is not None else None,
                    "Actual Agg Underling": f"{getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'underlying_agg'):,.0f}"if getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'underlying_agg') is not None else None,
                    "Underlying Premium": f"{getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'underlying_premium'):,.0f}"if getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'underlying_premium') is not None else None,
                    "Occurrence Cover?": getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'occurrence_cover') if getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'occurrence_cover') is not None else None,

                } for item in umbrella_name if getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'occurrence_cover') is not False
        ]   
        umbrella_outputs = []
        umbrella_layers = ["premium_primary", "premium_1_excess", "premium_2_excess", "premium_3_excess", "premium_4_excess", "premium_5_excess", "premium_6_excess", "premium_7_excess", "premium_8_excess", "premium_9_excess", "premium_10_excess"]
        for item in umbrella_name: 
            umbrella_dict = {
                "Description": utils.title_rc(item),
            } 
            for node in umbrella_layers:
                premium = getattr(getattr(hxd.cds.options[selected_option], f"glsn_{item}"), node) 
                if premium != 0: 
                    umbrella_dict[utils.title_rc(node)] = f"{int(premium):,}"
            umbrella_outputs.append(umbrella_dict)
        umbrella_outputs = [entry for entry in umbrella_outputs if entry.get("Premium 1 Excess",0) != 0] 

    if len(umbrella_inputs) == 0  :
       umbrella_inputs = [
        {
        "Umbrella": "No Umbrella Coverages Entered"
       } 
       ]
    else:
        umbrella_inputs = umbrella_inputs
    if len(umbrella_outputs) == 0  :
       umbrella_outputs = [
        {
        "Umbrella": "No Umbrella Coverages Entered"
       } 
       ]
    else:
        umbrella_outputs = umbrella_outputs


    # Rating Summary
    
    rating_summary_table = [
                {
                    "Layer": "Retention" if layer ==0 else "Primary Layer" if layer == 1 else f"Excess Layer {layer-1}",
                    "Per Claim Limit": f"{hxd.cds.layers[layer].limit :,.0f}" if hxd.cds.layers[layer].limit is not None else "-",
                    "Aggregate Limit": f"{hxd.cds.layers[layer].aggregate_limit :,.0f}" if hxd.cds.layers[layer].aggregate_limit is not None else "-",
                    "Brokerage": f"{hxd.cds.layers[layer].brokerage * 100:.1f}%" if hxd.cds.layers[layer].brokerage is not None else "-",
                    "Model Premium": f"{hxd.cds.layers[layer].model_premium :,.0f}" if hxd.cds.layers[layer].model_premium is not None else "-",
                    "Quoted Premium": f"{hxd.cds.layers[layer].quoted_premium :,.0f}" if hxd.cds.layers[layer].quoted_premium is not None else "-",
                    "Bound Premium": f"{hxd.cds.layers[layer].bound_premium :,.0f}" if hxd.cds.layers[layer].bound_premium is not None else "-",
                    "Section Reference": hxd.cds.layers[layer].section_reference if hxd.cds.layers[layer].section_reference is not None else "-",
                    "Status": hxd.cds.layers[layer].status if hxd.cds.layers[layer].status is not None else "-",
                    "Benchmark Premium": f"{hxd.cds.layers[layer].benchmark_premium :,.0f}" if hxd.cds.layers[layer].benchmark_premium is not None else "-",
                    "BPI": f"{hxd.cds.layers[layer].bpi * 100:.0f}%" if hxd.cds.layers[layer].bpi is not None else "-",
                    "Net Written Premium": f"{hxd.cds.layers[layer].net_written_premium :,.0f}" if hxd.cds.layers[layer].net_written_premium is not None else "-",
                    "Technical Premium": f"{hxd.cds.layers[layer].technical_premium :,.0f}" if hxd.cds.layers[layer].technical_premium is not None else "-",
                    "TPI": f"{hxd.cds.layers[layer].tpi * 100:.0f}%" if hxd.cds.layers[layer].tpi is not None else "-",

                } for layer in range (0,10) if hxd.cds.layers[layer].limit is not None
        ]    

    # Umbrella Coverage
    if hxd.cds.gmm_masking:
        schedule_mods = hx.params.table_gmm_schedule_mods["description_name"]
        schedule_mods = [
                {
                    "Description": utils.title_rc(item),
                    "Min": f"{getattr(getattr(hxd.cds.modifiers.gmm,item),'min')}%",
                    "Max": f"{getattr(getattr(hxd.cds.modifiers.gmm,item),'max')}%",
                    "Value": f"{getattr(getattr(hxd.cds.modifiers.gmm,item),'value') * 100:.0f}%" if getattr(getattr(hxd.cds.modifiers.gmm,item),'value') is not None else None,
                    "Comment": getattr(getattr(hxd.cds.modifiers.gmm,item),"comment"),

                } for item in schedule_mods if getattr(getattr(hxd.cds.modifiers.gmm,item),"value") is not None
        ]
    else:
        schedule_mods = hx.params.table_glsn_schedule_mods["description_name"]
        schedule_mods = [
                {
                    "Description": utils.title_rc(item),
                    "Min": f"{getattr(getattr(hxd.cds.modifiers.glsn,item),'min')}%",
                    "Max": f"{getattr(getattr(hxd.cds.modifiers.glsn,item),'max')}%",
                    "Value": f"{getattr(getattr(hxd.cds.modifiers.glsn,item),'value') * 100:.0f}%" if getattr(getattr(hxd.cds.modifiers.glsn,item),'value') is not None else None,
                    "Comment": getattr(getattr(hxd.cds.modifiers.glsn,item),"comment"),

                } for item in schedule_mods if getattr(getattr(hxd.cds.modifiers.glsn,item),"value") is not None
        ] 

    #Rate change 
    if hxd.cds.standard_fields.is_renewal :
        rate_change_table = [
                    {
                        "Renewal Layer": "Primary Layer" if layer == 1 else f"Excess Layer {layer-1}",
                        "Expiring Layer": hxd.cds.layers[layer].rate_change.expiring_layer_dropdown,
                        "Exposure Change": f"{hxd.cds.layers[layer].rate_change.exposure_change.uw_selected.selected * 100:.1f}%" if hxd.cds.layers[layer].rate_change.exposure_change.uw_selected.selected is not None else None,
                        "Exposure Change Comments": hxd.cds.layers[layer].rate_change.exposure_change.comments,
                        "Risk Characteristics Change": f"{hxd.cds.layers[layer].rate_change.risk_characteristics_change.uw_selected.selected * 100:.1f}%" if hxd.cds.layers[layer].rate_change.risk_characteristics_change.uw_selected.selected is not None else None,
                        "Risk Characteristics Comments": hxd.cds.layers[layer].rate_change.risk_characteristics_change.comments,
                        "Limit Change": f"{hxd.cds.layers[layer].rate_change.limit_change.uw_selected.selected * 100:.1f}%" if hxd.cds.layers[layer].rate_change.limit_change.uw_selected.selected is not None else None,
                        "Limit Change Comments": hxd.cds.layers[layer].rate_change.limit_change.comments,
                        "Deductible Change": f"{hxd.cds.layers[layer].rate_change.deductible_change.uw_selected.selected * 100:.1f}%" if hxd.cds.layers[layer].rate_change.deductible_change.uw_selected.selected is not None else None,
                        "Deductible Change Comments": hxd.cds.layers[layer].rate_change.deductible_change.comments,
                        "T&Cs Change": f"{hxd.cds.layers[layer].rate_change.terms_conditions_change.uw_selected.selected * 100:.1f}%" if hxd.cds.layers[layer].rate_change.terms_conditions_change.uw_selected.selected is not None else None,
                        "T&Cs Change Comments": hxd.cds.layers[layer].rate_change.terms_conditions_change.comments,
                        "Brokerage Change": f"{hxd.cds.layers[layer].rate_change.brokerage_change.uw_selected.selected * 100:.1f}%" if hxd.cds.layers[layer].rate_change.brokerage_change.uw_selected.selected is not None else None,
                        "Brokerage Change Comments": hxd.cds.layers[layer].rate_change.brokerage_change.comments,
                        "Other Change": f"{hxd.cds.layers[layer].rate_change.other_change.uw_selected.selected * 100:.1f}%" if hxd.cds.layers[layer].rate_change.other_change.uw_selected.selected is not None else None,
                        "Other Change Comments": hxd.cds.layers[layer].rate_change.other_change.comments,
                        "Final Rate Change": f"{hxd.cds.layers[layer].rate_change.risk_adjusted_rate_change.uw_selected * 100:.1f}%" if hxd.cds.layers[layer].rate_change.risk_adjusted_rate_change.uw_selected is not None else None,
                    } for layer in range (1,11) if hxd.cds.layers[layer].rate_change.premium_annualized_100pct.renewal is not None and hxd.cds.layers[layer].rate_change.premium_annualized_100pct.renewal != 0
            ] 
    else:
        rate_change_table = [{
            "Rate Change": "Rate Change Not Calculated",
        }]
    
    # Underwriting Notes Section
    uw_notes = hxd.cds.uw_notes
    # Extract and format the uw notes
    if uw_notes is None:
        formatted_uw_notes = ""
    elif isinstance(uw_notes, dict) and 'UW Notes' in uw_notes:
        formatted_uw_notes = uw_notes['UW Notes'].replace('\n', '<br>')
    else:
        formatted_uw_notes = uw_notes.replace('\n', '<br>')   

    formatted_uw_notes = format_note_field(uw_notes, 'UW Notes')

    mta_comments = hxd.cds.mid_term_adjustments
    # Extract and format the mta notes
    if mta_comments is None:
        formatted_mta_comments = ""
    elif isinstance(mta_comments, dict) and 'Mid Term Adjustments' in mta_comments:
        formatted_mta_comments = mta_comments['Mid Term Adjustments'].replace('\n', '<br>')
    else:
        formatted_mta_comments = mta_comments.replace('\n', '<br>')  
    
    formatted_mta_comments = format_note_field(mta_comments, 'Mid Term Adjustments')

    # historical_comments = hxd.cds.historical_comments
    # # Extract and format the mta notes
    # if historical_comments is None:
    #     formatted_historical_comments = ""
    # elif isinstance(historical_comments, dict) and 'Historical Comments' in historical_comments:
    #     formatted_historical_comments = historical_comments['Historical Comments'].replace('\n', '<br>')
    # else:
    #     formatted_historical_comments = historical_comments.replace('\n', '<br>')        

    # NOTE: define all your tables here first as dictionaries (or list of dictionaries) with values coming from the hxd

    # Function to generate an HTML table
    def generate_html_table(data, title):
        html = f"<h2 class='section-title'>{title}</h2><table>"
        
        # Check if data is a list of dictionaries
        if isinstance(data, list) and all(isinstance(row, dict) for row in data):
            # Create table headers from the keys of the first dictionary
            headers = data[0].keys()
            html += "<tr>" + "".join(f"<th>{header}</th>" for header in headers) + "</tr>"
            
            # Create table rows
            for row in data:
                html += "<tr>" + "".join(f"<td>{row.get(header, '')}</td>" for header in headers) + "</tr>"
        # If data is a single dictionary (two-column table)
        elif isinstance(data, dict):
            for key, value in data.items():
                html += f"""
                <tr>
                    <td><strong>{key}</strong></td>
                    <td>{value}</td>
                </tr>"""
        
        html += "</table><br>"  # Add space after each table
        return html

    # Generate HTML content for each table by calling the function with a title
    # NOTE: this function lets you add the table to the HTML code (first argument), and set the title you want (second argument)
    # Add as many tables as you need
    title_html = f"<h1 style='color:#004A7C; font-family:Arial, sans-serif; font-weight: bold;'>{insured_name}</h1><br>"
    html_tables = ""
    html_tables += generate_html_table(risk_information, "Risk Information")
    html_tables += generate_html_table(account_scoring, "Account Scoring")
    if hxd.cds.exposure.granular.gmm_product.product != "Triage":
        html_tables += generate_html_table(primary_exposure_details, "Primary Exposure Details")
        html_tables += generate_html_table(secondary_exposure_details, "Secondary Exposure Details")
    else: 
        html_tables += generate_html_table(triage_doc_res, "Doctors and Residents")
        html_tables += generate_html_table(triage_procedures, "Procedures")
        html_tables += generate_html_table(triage_total_obe, "Total OBE")
        
    html_tables += generate_html_table(venue_factors, "Overall Venue Factors")
    html_tables += generate_html_table(venue_us_output, "US Venue Splits")
    html_tables += generate_html_table(venue_international_output, "International Venue Splits")
    html_tables += generate_html_table(coverage_details, "Coverage Details")
    html_tables += generate_html_table(coverage_limits, "Coverage Limits")
    html_tables += generate_html_table(enhancements, "Coverage Enhancements")
    html_tables += generate_html_table(primary_layer, "Primary Layer Pricing")
    html_tables += generate_html_table(excess_layers, "Excess Layer Pricing")

    if hxd.cds.rating_factors.pricing.tech_eo_products_media.include_primary or hxd.cds.rating_factors.pricing.well_tech_eo_media.include_primary:
        html_tables += generate_html_table(tech_rateable, "Tech EO")
        html_tables += generate_html_table(tech_eo_coverage_details, "Tech EO Coverage Details")

    if hxd.cds.rating_factors.cyber.product is not None :
        html_tables += generate_html_table(cyber_details, "Cyber")
        html_tables += generate_html_table(cyber_details_schedule_mods, "")
        html_tables += generate_html_table(cyber_totals, "")

    html_tables += generate_html_table(umbrella_inputs, "Umbrella Inputs")
    html_tables += generate_html_table(umbrella_outputs, "Umbrella Calculations")
    html_tables += generate_html_table(rating_summary_table, "Rating Summary")
    html_tables += generate_html_table(schedule_mods, "Schedule Modifiers")
    html_tables += generate_html_table(rate_change_table, "Rate Change")
    #... Add your tables here

    # Put all the tables together in HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; font-size: 12px; }}
            h1 {{ color: #004A7C; font-size: 16px; }}
            h2 {{ color: #CC007F; font-size: 14px; margin-top: 20px; }}
            table {{ width: 50%; border-collapse: collapse; font-size: 12px; margin: 0 auto; }}
            td, th {{ border: 1px solid #000; padding: 4px; text-align: left; }}
            th {{ background-color: #f2f2f2; font-weight: bold; }}
            .section-title {{ color: #CC007F; font-weight: bold; }}
        </style>
    </head>
    <body>
    <h1>{insured_name}</h1>
    {html_tables}
    
    <h2 class='section-title'>Underwriting Notes</h2><p>{formatted_uw_notes}</p>
    <h2 class='section-title'>Mid Term Adjustment Notes</h2><p>{formatted_mta_comments}</p>
    

    </body>
    </html>
    """

    # Create the email message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Rationale email - {insured_name}"
    msg["From"] = hxd.cds.email.sender # NOTE: can have address of the relevant UWs here so they can just reply and send after downloading the message
    msg["To"] = hxd.cds.email.recipient

    # Attach the HTML content to the email
    msg.attach(MIMEText(html_content, "html"))

    # Save the email as an .eml file
    with hxd.cds.email.rationale_file.open("b") as file:
        gen = BytesGenerator(file, policy=policy.default)
        gen.flatten(msg)



##############################


@hx.task
def generate_referral_email_task(hxd, progress):
    insured_name = hxd.cds.standard_fields.insured_name or "TEST TEST TEST" # NOTE: can remove the "or" condition, it's just to always have it populated
    underwriter = hxd.cds.standard_fields.underwriter
    formatted_underwriter = underwriter.replace(" ", ".").lower()
    underwriter_email = formatted_underwriter + "@beazley.com"
    hxd.cds.email.sender = underwriter_email
    hxd.cds.email.recipient = underwriter_email

    insured_name = hxd.cds.standard_fields.insured_name or "TEST TEST TEST" # NOTE: can remove the "or" condition, it's just to always have it populated
    # Load the existing referral .htm file with fallback encoding
    referral_filename = "referral_template.htm"
    referral_path = os.path.join(os.path.dirname(__file__), referral_filename)
    try:
        with open(referral_path, "r", encoding="utf-8") as file:
            html_referral_content = file.read()
    except UnicodeDecodeError:
        # Try ISO-8859-1 encoding if UTF-8 fails
        with open(referral_path, "r", encoding="ISO-8859-1") as file:
            html_referral_content = file.read()

    ### --- Define data for each table --- ###

    # This is a normal table that can be formed from separate fields or come from a Structure
    risk_information = {
        "Insured": insured_name, # NOTE: update all these fields like the one above so they come from the hxd
        "Brokerage Firm": hxd.cds.standard_fields.broker, 
        "Broker Contact": hxd.cds.broker_contact,
        "Inception Date": hxd.hx_core.inception_date,
        "Expiry Date": hxd.hx_core.expiry_date,
        "US/International": hxd.cds.rating_factors.us_international_choice_of_law.us_international,
        "Choice of Law": hxd.cds.rating_factors.us_international_choice_of_law.choice_of_law,
        "Currency": hxd.cds.currencies.source_currency,
        "Revenue": f"{int(hxd.cds.exposure.aggregate.revenue):,}",
        "Account Score": hxd.cds.rating_factors.account_score,
        "Profit Status": hxd.cds.rating_factors.profit_status,
        "":"",
        "Product": hxd.cds.exposure.granular.gmm_product.product if hxd.cds.gmm_masking else  hxd.cds.exposure.granular.glsn_product.product ,
        "COB Code": hxd.cds.exposure.granular.gmm_product.cob_code_description if hxd.cds.gmm_masking else  hxd.cds.exposure.granular.glsn_product.cob_code_description,
        "Class": hxd.cds.exposure.granular.gmm_product.cob_class if hxd.cds.gmm_masking else None ,
    }
    
    # For account scorings
    account_scoring_list = hx.params.table_account_scoring["account_scoring_name"]
    account_scoring = [
            {
                "Feature": utils.title_rc(item),
                "Score": getattr(getattr(hxd.cds.rating_factors.account_scoring , item ),"value"),
                "Comment": getattr(getattr(hxd.cds.rating_factors.account_scoring , item ),"comment"),
                #... Add your other fields
            } for item in account_scoring_list 
            ]

    # GMM Primary Exposure details
    if hxd.cds.gmm_masking: 
        if hxd.cds.exposure.granular.gmm_product.product != "Triage":
            p_expo = hxd.cds.exposure.granular.gmm_primary_exposure_details
            primary_exposure_details = [
                {
                    "Class": item.exposure_class,
                    "Exposure Measure": item.exposure_measure,
                    "Base Rate": item.formatted_base_rate,
                    "Current Year": f"{int(item.current_year):,}",
                    "Use For Calculation": item.selection,
                    "Base Premium": f"{int(item.base_premium):,}",
                    #... Add your other fields
                } for item in p_expo if item.selection is not False # Adding this condition as you have a fixed number of items - feel free to change as appropriate
            ]
            if not primary_exposure_details:
                primary_exposure_details = [
                    {
                        "Class": "No Primary Classes Selected",
                    } 
                ] 
            # GMM Secondary Exposure details
            secondary_exposure_details = [
                {
                    "Class": item.gmm_secondary_exposure.exposure_class,
                    "Exposure Measure": item.gmm_secondary_exposure.exposure_measure,
                    "Base Rate": item.formatted_base_rate,
                    "Current Year": f"{int(item.current_year):,}",
                    "Use For Calculation": item.selection,
                    "Base Premium": f"{int(item.base_premium):,}",
                    #... Add your other fields
                } for item in hxd.cds.exposure.granular.gmm_secondary_exposure_details if item.selection is not False # Adding this condition as you have a fixed number of items - feel free to change as appropriate
            ]
            if not secondary_exposure_details:
                secondary_exposure_details = [
                    {
                        "Class": "No Secondary Class data available",
                    } 
                ] 
        else:
            
            triage_doc_res = [
                {
                    "Specialty": (item.specialty), 
                    "Employed Doctors Current Year": item.doc_current_year, 
                    "OBE Per Doctor": item.obe_per_doctor, 
                    "Residents Current Year": item.resident_current_year, 
                    "OBE Per Resident": item.obe_per_resident, 
                } for item in hxd.cds.exposure.granular.triage_doctors_residents if item.doc_current_year != 0 or item.resident_current_year != 0
            ]
            if not triage_doc_res:
                triage_doc_res = [
                    {
                        "Doctors and Residents": "No Doctors and Residents Entered",
                    } 
                ] 
            triage_procedures = [
                {
                    "Category": (item.category), 
                    "Exposure Measure": item.exposure_measure, 
                    "OBE or FTE": item.obe_or_fte, 
                    "Procedures Current Year": item.current_year, 
                } for item in hxd.cds.exposure.granular.triage_procedures if item.current_year != 0 
            ]
            if not triage_procedures:
                triage_procedures = [
                    {
                        "Procedures": "No Procedures Entered",
                    } 
                ]
            triage_total_obe = [
                {
                    "Total OBE": item.current_year , 
                } for item in hxd.cds.exposure.aggregate.triage_running_total_obe
            ]
            if not triage_total_obe:
                triage_total_obe = [
                    {
                        "Total OBE": "Total OBE Not a",
                    } 
                ]

    else:
        p_expo = hxd.cds.exposure.granular.glsn_primary_exposure_details
        primary_exposure_details = [
            {
                "Class": item.cob,
                "Exposure Base": item.exposure_base,
                "Exposure Measure": item.exposure_measure,
                "Base Rate": item.formatted_base_rate,
                "Current Year": f"{int(item.current_year):,}",
                "Use For Calculation": item.selection,
                "Base Premium": f"{int(item.base_premium):,}",
                #... Add your other fields
            } for item in p_expo if item.selection is not False # Adding this condition as you have a fixed number of items - feel free to change as appropriate
        ]
        if not primary_exposure_details:
                primary_exposure_details = [
                    {
                        "Class": "No Primary Classes Selected",
                    } 
                ] 
        # Glsn Secondary Exposure details
        secondary_exposure_details = [
                {
                    "Class": item.glsn_secondary_exposure.cob,
                    "Exposure Base": item.glsn_secondary_exposure.exposure_base,
                    "Exposure Measure": item.glsn_secondary_exposure.exposure_measure,
                    "Base Rate": item.formatted_base_rate,
                    "Current Year": f"{int(item.current_year):,}",
                    "Use For Calculation": item.selection,
                    "Base Premium": f"{int(item.base_premium):,}",
                    #... Add your other fields
                } for item in hxd.cds.exposure.granular.glsn_secondary_exposure_details if item.selection is not False # Adding this condition as you have a fixed number of items - feel free to change as appropriate
            ]
        if not secondary_exposure_details:
                secondary_exposure_details = [
                    {
                        "Class": "No Secondary Classes Selected",
                    } 
                ] 
    # Venue Factors
    venue_factors = {
        "Total Venue Splits": f"{hxd.cds.exposure.aggregate.total_percentage_selected *100:.0f}%", 
        "Total Venue Factor": f"{hxd.cds.exposure.aggregate.total_venue_factor:.2f}", 
    }

    venue_us_list = hx.params.table_venue_us["venue_name"]
    venue_us_params =  hx.params.table_venue_us
    venue_us_splits = [
            {
                "US Venue": venue_us_params[venue_us_params["venue_name"] == item]["venue_label"].iloc[0],
                "Factor": getattr(getattr(hxd.cds.exposure.granular , item ),"factor"),
                "Split %": f"{getattr(getattr(hxd.cds.exposure.granular , item ),'percentage')*100:.1f}%",
                "Use For Calculation": getattr(getattr(hxd.cds.exposure.granular , item ),"selection"),
                #... Add your other fields
            } for item in venue_us_list if getattr(getattr(hxd.cds.exposure.granular , item ),"selection") is not False # Adding this condition as you have a fixed number of items - feel free to change as appropriate
            ]
    if len(venue_us_splits) == 0 :
        venue_us_output = [
            {
                "Venue": "No US Venues Entered"
            } 
            ]
    else:
        venue_us_output = venue_us_splits    

    venue_international_list = hx.params.table_venue_international["venue_name"]
    venue_international_params =  hx.params.table_venue_international
    venue_international_splits = [
            {
                "US Venue": venue_international_params[venue_international_params["venue_name"] == item]["venue_label"].iloc[0],
                "Factor": getattr(getattr(hxd.cds.exposure.granular , item ),"factor"),
                "Split %": f"{getattr(getattr(hxd.cds.exposure.granular , item ),'percentage')*100:.1f}%",
                "Use For Calculation": getattr(getattr(hxd.cds.exposure.granular , item ),"selection"),
                #... Add your other fields
            } for item in venue_international_list if getattr(getattr(hxd.cds.exposure.granular , item ),"selection") is not False # Adding this condition as you have a fixed number of items - feel free to change as appropriate
            ]
    if len(venue_international_splits) == 0 :
        venue_international_output = [
            {
                "Venue": "No International Venues Entered"
            } 
            ]
    else:
        venue_international_output = venue_international_splits   

    # Pricing Section
    coverages = ["professional_liability","general_liability","product_liability","eo","sexual_abuse","employee_benefits_liability","employers_liability","tech_eo_products_media","healthcare_professional_liability","product_recall","well_tech_eo_media"]
   
    coverage_details = [
            {
                "Coverage": utils.title_rc(item),
                "Include in Primary": getattr(getattr(hxd.cds.rating_factors.pricing , item ),"include_primary"),
                "Include in Excess": getattr(getattr(hxd.cds.rating_factors.pricing , item ),"include_excess"),
                "Claim Basis": getattr(getattr(hxd.cds.rating_factors.pricing , item ),"claims_basis"),
                "Retroactive Date": getattr(getattr(hxd.cds.rating_factors.pricing , item ),"retroactive_date"),
                **({"Significant Coverage": getattr(getattr(hxd.cds.rating_factors.pricing, item), "significant_coverage")} if not hxd.cds.gmm_masking else {})
                #... Add your other fields
            } for item in coverages if getattr(getattr(hxd.cds.rating_factors.pricing , item ),"include_primary") is not False # Adding this condition as you have a fixed number of items - feel free to change as appropriate
    ]

    coverage_limits = []
    selected_option = int(hxd.cds.option_selected[-1]) -1 

    option = hxd.cds.options[selected_option].coverages
    option_name = f"Option {selected_option + 1}"

    # Make three rows per coverage
    for cvg in coverages:
        retention_dict = {
            "Coverage": utils.title_rc(cvg),
            "Name": "Retention",
            option_name: f"{int(getattr(getattr(option,cvg),'retention')):,}" if getattr(getattr(option,cvg),'retention') is not None else None
        }
        per_claim_limit_dict = {
            "Coverage": utils.title_rc(cvg),
            "Name": "Per Claim Limit",
            option_name: f"{int(getattr(getattr(option,cvg),'per_claim_limit')):,}" if getattr(getattr(option,cvg),'per_claim_limit') is not None else None
        }
        agg_limit_dict = {
            "Coverage": utils.title_rc(cvg),
            "Name": "Aggregate Limit",
            option_name: f"{int(getattr(getattr(option,cvg),'aggregate_limit')):,}" if getattr(getattr(option,cvg),'aggregate_limit') is not None else None
        }

        # Append to list
        coverage_limits.append(retention_dict)
        coverage_limits.append(per_claim_limit_dict)
        coverage_limits.append(agg_limit_dict)

        coverage_limits = [data for data in coverage_limits if data[f"Option {selected_option + 1}"] is not None]

    # Coverage Enhancements
    enhancement_option = hxd.cds.options[selected_option]
    enhancements = []
    stop_gap_dict = {
                "Coverage": "Stop Gap",
                "Include Primary": hxd.cds.options[selected_option].include_stop_gap_primary,
                "Include Excess": hxd.cds.rating_factors.pricing.include_stop_gap_excess,
                "Type":"N/A",
                "Amount":"N/A",
            } 
    tria_dict = {
                "Coverage": "TRIA",
                "Include Primary": hxd.cds.options[selected_option].include_tria_primary,
                "Include Excess": hxd.cds.rating_factors.pricing.include_tria_excess,
                "Type":"N/A",
                "Amount":"N/A",
            }   
    punitive_damages_dict = {
                "Coverage": "Punitive Damages",
                "Include Primary": hxd.cds.options[selected_option].include_punitive_damages_primary,
                "Include Excess": hxd.cds.rating_factors.pricing.include_punitive_damages_excess,
                "Type":"N/A",
                "Amount":"N/A",
            }  
    costs_in_addition_dict = {
                "Coverage": "Costs In Addition",
                "Include Primary": hxd.cds.options[selected_option].include_costs_in_addition_primary,
                "Include Excess": hxd.cds.rating_factors.pricing.include_costs_in_addition_excess,
                "Type": hxd.cds.options[selected_option].costs_in_addition_selection,
                "Amount":"N/A",
            } 
    auto_dict = {
        "Coverage": "Auto HNOA",
        "Include Primary": hxd.cds.options[selected_option].include_auto_primary,
        "Include Excess": hxd.cds.rating_factors.pricing.include_auto_excess,
        "Type": hxd.cds.options[selected_option].auto_measure,
        "Amount":hxd.cds.options[selected_option].auto_amount,
    } 
    enhancements.append(stop_gap_dict)
    enhancements.append(tria_dict)
    enhancements.append(punitive_damages_dict)
    enhancements.append(costs_in_addition_dict)
    enhancements.append(auto_dict)
    enhancements = [data for data in enhancements if data["Include Primary"]]

    if len(enhancements) == 0 :
        enhancements = [
            {
                "Enhancements": "No Coverage Enhancements Selected"
            } 
            ]
    else:
        enhancements = enhancements

    # Layer outputs  
    layer_path =  hxd.cds.options[selected_option]  
    primary_layer = [{
        "Brokerage": f"{layer_path.brokerage_primary * 100:.1f}%" if layer_path.brokerage_primary is not None else None, 
        "Cyber Premium": f"{layer_path.cyber_premium_primary:,.0f}" if layer_path.cyber_premium_primary is not None else None, 
        "Model Premium": f"{layer_path.model_premium_primary:,.0f}" if layer_path.model_premium_primary is not None else None, 
        "Minimum Premium": f"{layer_path.minimum_premium_primary:,.0f}" if layer_path.minimum_premium_primary is not None else None, 
        "Gross Premium": f"{layer_path.gross_premium_primary:,.0f}" if layer_path.gross_premium_primary is not None else None, 
        # "Uplift for NMP": f"{layer_path.uplift_for_nmp_primary:,.2f}" if layer_path.uplift_for_nmp_primary is not None else None, 
        "Quoted Premium": f"{layer_path.quoted_premium_primary:,.0f}" if layer_path.quoted_premium_primary is not None else None, 
        "BPI": f"{layer_path.bpi_primary * 100:.0f}%" if layer_path.bpi_primary is not None else None, 
    }]
    layers = ["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"]
    excess_layers = []
    for layer in layers : 
        layer_number = layer.split('_')[0]
        excess_dict = {
            "Excess Layer": f"Excess Layer {layer_number}",
            "Per Claim Limit": f"{getattr(layer_path,f'per_claim_limit_{layer}'):,.0f}" if getattr(layer_path,f'per_claim_limit_{layer}') is not None else None,
            "Aggregate Limit": f"{getattr(layer_path,f'aggregate_limit_{layer}'):,.0f}" if getattr(layer_path,f'aggregate_limit_{layer}') is not None else None,
            "Brokerage": f"{getattr(layer_path,f'brokerage_{layer}') * 100 :.1f}%" if getattr(layer_path,f'brokerage_{layer}') is not None else None,
            "Supported Excess Premium": f"{getattr(layer_path,f'supported_excess_premium_{layer}'):,.0f}" if getattr(layer_path,f'supported_excess_premium_{layer}') is not None else None,
            "Cyber Premium": f"{getattr(hxd.cds.cyber_options[selected_option],f'model_premium_third_party_{layer}'):.0f}" if getattr(hxd.cds.cyber_options[selected_option],f'model_premium_third_party_{layer}') is not None else None,
            "Umbrella Premium": f"{getattr(layer_path,f'umbrella_premium_{layer}'):,.0f}" if getattr(layer_path,f'umbrella_premium_{layer}') is not None else None,
            # "Uplift for NMP": f"{getattr(layer_path,f'uplift_for_nmp_{layer}'):,.2f}" if getattr(layer_path,f'uplift_for_nmp_{layer}') is not None else None,
            "Minimum Premium": f"{getattr(layer_path,f'minimum_premium_{layer}'):,.0f}" if getattr(layer_path,f'minimum_premium_{layer}') is not None else None,
            "Gross Premium": f"{getattr(layer_path,f'gross_premium_{layer}'):,.0f}" if getattr(layer_path,f'gross_premium_{layer}') is not None else None,
            "Quoted Premium": f"{getattr(layer_path,f'quoted_premium_{layer}'):,.0f}" if getattr(layer_path,f'quoted_premium_{layer}') is not None else None,
            "BPI": f"{getattr(layer_path,f'bpi_{layer}') * 100 :.0f}%" if getattr(layer_path,f'bpi_{layer}') is not None else None,
            "Comment": getattr(layer_path,f"comment_{layer}"),
        }
        excess_layers.append(excess_dict)
    excess_layers = [data for data in excess_layers if data["Per Claim Limit"] is not None]
    if len(excess_layers) == 0 :
        excess_layers = [
            {
                "Excess Layers": "No Excess Layers Entered"
            } 
            ]
    else:
        excess_layers = excess_layers 

   # Tech EO Section
    if hxd.cds.rating_factors.pricing.tech_eo_products_media.include_primary or hxd.cds.rating_factors.pricing.well_tech_eo_media.include_primary:
        tech_eo_name = hx.params.table_tech_eo["industry_class_name"]
        
        tech_eo_coverage_details = [
                {
                    "Industry Class": utils.title_rc(item),
                    "% of Rateable Revenue": f"{(getattr(getattr(hxd.cds.exposure.granular , item ),'tech_eo_percent_rateble_revenue')) * 100:.0f}%" if (getattr(getattr(hxd.cds.exposure.granular , item ),'tech_eo_percent_rateble_revenue')) is not None else None,
                    "Class": getattr(getattr(hxd.cds.exposure.granular , item ),"tech_eo_class"),
                    "Revenue": f"{getattr(getattr(hxd.cds.exposure.granular , item ),'tech_eo_revenue'):,.0f}" if getattr(getattr(hxd.cds.exposure.granular , item ),'tech_eo_revenue') is not None else None,

                } for item in tech_eo_name if getattr(getattr(hxd.cds.exposure.granular , item ),"tech_eo_percent_rateble_revenue") > 0 
        ]
        
        if len(tech_eo_coverage_details) == 0 :
            tech_eo_coverage_details = [
                {
                    "Tech EO": "No Tech EO Coverage Entered"
                } 
                ]
            tech_rateable = { "Tech EO Rateable Revenue %": ""}
        else:
            if hxd.cds.gmm_masking:
                tech_rateable = { "Tech EO Rateable Revenue %": f"{hxd.cds.exposure.aggregate.tech_eo_rateble_revenue* 100: .0f}%"} 
            else:
                tech_rateable = { 
                    "Tech EO Rateable Revenue %": f"{hxd.cds.exposure.aggregate.tech_eo_rateble_revenue* 100: .0f}%",
                    "Contingent BI/PD Selection": hxd.cds.rating_factors.tech_eo.contingent_bi_pd
                }
            tech_eo_coverage_details = tech_eo_coverage_details  
  
    # Cyber details
    if hxd.cds.rating_factors.cyber.product is not None :
        cyber_details =  {
                    "Cyber Product": hxd.cds.rating_factors.cyber.product,
                    "Notified Individuals": f"{hxd.cds.cyber_options[selected_option].notified_individuals_limit:,.0f}" if hxd.cds.cyber_options[selected_option].notified_individuals_limit is not None else None,
                    "Legal, Forensic & PR Limit": f"{hxd.cds.cyber_options[selected_option].legal_forensic_limit:,.0f}" if hxd.cds.cyber_options[selected_option].legal_forensic_limit is not None else None,
                    "Additional Breach Resp. Costs":  f"{hxd.cds.cyber_options[selected_option].additional_breach_costs_limit:,.0f}" if hxd.cds.cyber_options[selected_option].additional_breach_costs_limit is not None else "Not Purchased",
                    "Policy Aggregate Limit of Lia": f"{hxd.cds.cyber_options[selected_option].policy_agg_limit:,.0f}" if hxd.cds.cyber_options[selected_option].policy_agg_limit is not None else None,
                    "InfoSec Breach Response Limit": f"{hxd.cds.cyber_options[selected_option].infosec_breach_response_limit:,.0f}" if hxd.cds.cyber_options[selected_option].infosec_breach_response_limit is not None else None,
                    "Data & Network Limit": f"{hxd.cds.cyber_options[selected_option].data_network_limit:,.0f}" if hxd.cds.cyber_options[selected_option].data_network_limit is not None else "Not Purchased",
                    "Reg. Defense & Penalties Limit": f"{hxd.cds.cyber_options[selected_option].defense_penalties_limit:,.0f}" if hxd.cds.cyber_options[selected_option].defense_penalties_limit is not None else "Not Purchased",
                    "Payment Card Lia. & Costs Limit": f"{hxd.cds.cyber_options[selected_option].payment_card_limit:,.0f}"if hxd.cds.cyber_options[selected_option].payment_card_limit is not None else "Not Purchased",
                    "Legal Forensic & PR Retention": f"{hxd.cds.cyber_options[selected_option].legal_forensic_retention:,.0f}" if hxd.cds.cyber_options[selected_option].legal_forensic_retention is not None else None,
                    "Legal Subretention": f"{hxd.cds.cyber_options[selected_option].legal_forensic_subretention:,.0f}" if hxd.cds.cyber_options[selected_option].legal_forensic_subretention is not None else None,
                    "Agg. Per Incident, Claim, or Loss Retention": f"{hxd.cds.cyber_options[selected_option].policy_agg_retention:,.0f}" if hxd.cds.cyber_options[selected_option].policy_agg_retention is not None else None,
                    "Data & Network Retention": f"{hxd.cds.cyber_options[selected_option].data_network_retention.selected:,.0f}" if hxd.cds.cyber_options[selected_option].data_network_retention.selected is not None else None,
                    "Reg.Defense Penalites Retention": f"{hxd.cds.cyber_options[selected_option].defense_penalties_retention.selected:,.0f}" if hxd.cds.cyber_options[selected_option].defense_penalties_retention.selected is not None else None,
                    "Payment Card Retention": f"{hxd.cds.cyber_options[selected_option].payment_card_retention.selected:,.0f}" if hxd.cds.cyber_options[selected_option].payment_card_retention.selected is not None else None,
                    "InfoSec Breach Response Retention": f"{hxd.cds.cyber_options[selected_option].breach_response_retention:,.0f}" if hxd.cds.cyber_options[selected_option].breach_response_retention is not None else None,
                }

        cyber_details_schedule_mods =  {
                "Cyber Schedule Rating: Financial Condition": f"{hxd.cds.modifiers.cyber.cyber_financial_condition.value * 100: .0f}%" if hxd.cds.modifiers.cyber.cyber_financial_condition.value is not None else None,
                "Cyber Schedule Rating: Financial Condition Comment": hxd.cds.modifiers.cyber.cyber_financial_condition.comment,
                "Cyber Schedule Rating: Maturity of Business": f"{hxd.cds.modifiers.cyber.cyber_maturity_of_business.value * 100: .0f}%" if hxd.cds.modifiers.cyber.cyber_maturity_of_business.value is not None else None,
                "Cyber Schedule Rating: Maturity of Business Comment": hxd.cds.modifiers.cyber.cyber_maturity_of_business.comment,
                "Cyber Schedule Rating: Quality of Management": f"{hxd.cds.modifiers.cyber.cyber_quality_of_management.value * 100: .0f}%" if hxd.cds.modifiers.cyber.cyber_quality_of_management.value is not None else None,
                "Cyber Schedule Rating: Quality of Management Comment": hxd.cds.modifiers.cyber.cyber_quality_of_management.comment,
                "Cyber Schedule Rating: Volume of Information Stored": f"{hxd.cds.modifiers.cyber.cyber_volume_of_information_stored.value * 100: .0f}%" if hxd.cds.modifiers.cyber.cyber_volume_of_information_stored.value is not None else None,
                "Cyber Schedule Rating: Volume of Information Stored Comment": hxd.cds.modifiers.cyber.cyber_volume_of_information_stored.comment,
                "Cyber Schedule Rating: Cyber Loss Rating": hxd.cds.modifiers.cyber.cyber_loss_rating[0].cyber_loss_ratio,
                "Cyber Schedule Rating: Cyber Loss Rating Comment": hxd.cds.modifiers.cyber.cyber_loss_rating[0].cyber_loss_ratio_selected,
            }
        
        if hxd.cds.cyber_options[selected_option].model_premium_bbr_rater is not None:
            cyber_totals =  {
                "Cyber First Party and Third Party Premium":  f"{hxd.cds.cyber_options[selected_option].model_premium_bbr_rater:,.0f}" if hxd.cds.cyber_options[selected_option].model_premium_bbr_rater is not None else None,
            }
        else:
            cyber_totals =  {
                "Cyber Brokerage": f"{hxd.cds.cyber_options[selected_option].brokerage * 100: .1f}%" if hxd.cds.cyber_options[selected_option].brokerage is not None else None,
                "Cyber Third Party Premium": f"{hxd.cds.cyber_options[selected_option].model_premium_third_party:,.0f}" if hxd.cds.cyber_options[selected_option].model_premium_third_party is not None else None,
            }

    



    # Umbrella Coverage
    if hxd.cds.gmm_masking:
        umbrella_name = hx.params.table_gmm_umbrella["umbrella_name"]
        umbrella_inputs = [
                {
                    "Description": utils.title_rc(item),
                    "Actual EE Underling": f"{getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'underlying_ee'):,.0f}" if getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'underlying_ee') is not None else None,
                    "Actual Agg Underling": f"{getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'underlying_agg'):,.0f}"if getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'underlying_agg') is not None else None,
                    "Underlying Premium": f"{getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'underlying_premium'):,.0f}"if getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'underlying_premium') is not None else None,
                    "Occurrence Cover?": getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'occurrence_cover') if getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'occurrence_cover') is not None else None,

                } for item in umbrella_name if getattr(getattr(hxd.cds.rating_factors.gmm.umbrella,item),'occurrence_cover') is not False
        ]
        umbrella_outputs = []
        umbrella_layers = ["premium_primary", "premium_1_excess", "premium_2_excess", "premium_3_excess", "premium_4_excess", "premium_5_excess", "premium_6_excess", "premium_7_excess", "premium_8_excess", "premium_9_excess", "premium_10_excess"]
        for item in umbrella_name: 
            umbrella_dict = {
                "Description": utils.title_rc(item),
            } 
            for node in umbrella_layers:
                premium = getattr(getattr(hxd.cds.options[selected_option], f"gmm_{item}"), node) 
                if premium != 0: 
                    umbrella_dict[utils.title_rc(node)] = f"{int(premium):,}"
            umbrella_outputs.append(umbrella_dict)
        umbrella_outputs = [entry for entry in umbrella_outputs if entry.get("Premium 1 Excess",0) != 0]
    else:
        umbrella_name = hx.params.table_glsn_umbrella["umbrella_name"]
        umbrella_inputs = [
                {
                    "Description": utils.title_rc(item),
                    "Actual EE Underling": f"{getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'underlying_ee'):,.0f}" if getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'underlying_ee') is not None else None,
                    "Actual Agg Underling": f"{getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'underlying_agg'):,.0f}"if getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'underlying_agg') is not None else None,
                    "Underlying Premium": f"{getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'underlying_premium'):,.0f}"if getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'underlying_premium') is not None else None,
                    "Occurrence Cover?": getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'occurrence_cover') if getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'occurrence_cover') is not None else None,

                } for item in umbrella_name if getattr(getattr(hxd.cds.rating_factors.glsn.umbrella,item),'occurrence_cover') is not False
        ]   
        umbrella_outputs = []
        umbrella_layers = ["premium_primary", "premium_1_excess", "premium_2_excess", "premium_3_excess", "premium_4_excess", "premium_5_excess", "premium_6_excess", "premium_7_excess", "premium_8_excess", "premium_9_excess", "premium_10_excess"]
        for item in umbrella_name: 
            umbrella_dict = {
                "Description": utils.title_rc(item),
            } 
            for node in umbrella_layers:
                premium = getattr(getattr(hxd.cds.options[selected_option], f"glsn_{item}"), node) 
                if premium != 0: 
                    umbrella_dict[utils.title_rc(node)] = f"{int(premium):,}"
            umbrella_outputs.append(umbrella_dict)
        umbrella_outputs = [entry for entry in umbrella_outputs if entry.get("Premium 1 Excess",0) != 0] 

    if len(umbrella_inputs) == 0  :
       umbrella_inputs = [
        {
        "Umbrella": "No Umbrella Coverages Entered"
       } 
       ]
    else:
        umbrella_inputs = umbrella_inputs
    if len(umbrella_outputs) == 0  :
       umbrella_outputs = [
        {
        "Umbrella": "No Umbrella Coverages Entered"
       } 
       ]
    else:
        umbrella_outputs = umbrella_outputs


    # Rating Summary
    
    rating_summary_table = [
                {
                    "Layer": "Retention" if layer ==0 else "Primary Layer" if layer == 1 else f"Excess Layer {layer-1}",
                    "Per Claim Limit": f"{hxd.cds.layers[layer].limit :,.0f}" if hxd.cds.layers[layer].limit is not None else "-",
                    "Aggregate Limit": f"{hxd.cds.layers[layer].aggregate_limit :,.0f}" if hxd.cds.layers[layer].aggregate_limit is not None else "-",
                    "Brokerage": f"{hxd.cds.layers[layer].brokerage * 100:.1f}%" if hxd.cds.layers[layer].brokerage is not None else "-",
                    "Model Premium": f"{hxd.cds.layers[layer].model_premium :,.0f}" if hxd.cds.layers[layer].model_premium is not None else "-",
                    "Quoted Premium": f"{hxd.cds.layers[layer].quoted_premium :,.0f}" if hxd.cds.layers[layer].quoted_premium is not None else "-",
                    "Bound Premium": f"{hxd.cds.layers[layer].bound_premium :,.0f}" if hxd.cds.layers[layer].bound_premium is not None else "-",
                    "Section Reference": hxd.cds.layers[layer].section_reference if hxd.cds.layers[layer].section_reference is not None else "-",
                    "Status": hxd.cds.layers[layer].status if hxd.cds.layers[layer].status is not None else "-",
                    "Benchmark Premium": f"{hxd.cds.layers[layer].benchmark_premium :,.0f}" if hxd.cds.layers[layer].benchmark_premium is not None else "-",
                    "BPI": f"{hxd.cds.layers[layer].bpi * 100:.0f}%" if hxd.cds.layers[layer].bpi is not None else "-",
                    "Net Written Premium": f"{hxd.cds.layers[layer].net_written_premium :,.0f}" if hxd.cds.layers[layer].net_written_premium is not None else "-",
                    "Technical Premium": f"{hxd.cds.layers[layer].technical_premium :,.0f}" if hxd.cds.layers[layer].technical_premium is not None else "-",
                    "TPI": f"{hxd.cds.layers[layer].tpi * 100:.0f}%" if hxd.cds.layers[layer].tpi is not None else "-",

                } for layer in range (0,10) if hxd.cds.layers[layer].limit is not None
        ]    

    # Umbrella Coverage
    if hxd.cds.gmm_masking:
        schedule_mods = hx.params.table_gmm_schedule_mods["description_name"]
        schedule_mods = [
                {
                    "Description": utils.title_rc(item),
                    "Min": f"{getattr(getattr(hxd.cds.modifiers.gmm,item),'min')}%",
                    "Max": f"{getattr(getattr(hxd.cds.modifiers.gmm,item),'max')}%",
                    "Value": f"{getattr(getattr(hxd.cds.modifiers.gmm,item),'value') * 100:.0f}%" if getattr(getattr(hxd.cds.modifiers.gmm,item),'value') is not None else None,
                    "Comment": getattr(getattr(hxd.cds.modifiers.gmm,item),"comment"),

                } for item in schedule_mods if getattr(getattr(hxd.cds.modifiers.gmm,item),"value") is not None
        ]
    else:
        schedule_mods = hx.params.table_glsn_schedule_mods["description_name"]
        schedule_mods = [
                {
                    "Description": utils.title_rc(item),
                    "Min": f"{getattr(getattr(hxd.cds.modifiers.glsn,item),'min')}%",
                    "Max": f"{getattr(getattr(hxd.cds.modifiers.glsn,item),'max')}%",
                    "Value": f"{getattr(getattr(hxd.cds.modifiers.glsn,item),'value') * 100:.0f}%" if getattr(getattr(hxd.cds.modifiers.glsn,item),'value') is not None else None,
                    "Comment": getattr(getattr(hxd.cds.modifiers.glsn,item),"comment"),

                } for item in schedule_mods if getattr(getattr(hxd.cds.modifiers.glsn,item),"value") is not None
        ] 

    #Rate change 
    if hxd.cds.standard_fields.is_renewal :
        rate_change_table = [
                    {
                        "Renewal Layer": "Primary Layer" if layer == 1 else f"Excess Layer {layer-1}",
                        "Expiring Layer": hxd.cds.layers[layer].rate_change.expiring_layer_dropdown,
                        "Exposure Change": f"{hxd.cds.layers[layer].rate_change.exposure_change.uw_selected.selected * 100:.1f}%" if hxd.cds.layers[layer].rate_change.exposure_change.uw_selected.selected is not None else None,
                        "Exposure Change Comments": hxd.cds.layers[layer].rate_change.exposure_change.comments,
                        "Risk Characteristics Change": f"{hxd.cds.layers[layer].rate_change.risk_characteristics_change.uw_selected.selected * 100:.1f}%" if hxd.cds.layers[layer].rate_change.risk_characteristics_change.uw_selected.selected is not None else None,
                        "Risk Characteristics Comments": hxd.cds.layers[layer].rate_change.risk_characteristics_change.comments,
                        "Limit Change": f"{hxd.cds.layers[layer].rate_change.limit_change.uw_selected.selected * 100:.1f}%" if hxd.cds.layers[layer].rate_change.limit_change.uw_selected.selected is not None else None,
                        "Limit Change Comments": hxd.cds.layers[layer].rate_change.limit_change.comments,
                        "Deductible Change": f"{hxd.cds.layers[layer].rate_change.deductible_change.uw_selected.selected * 100:.1f}%" if hxd.cds.layers[layer].rate_change.deductible_change.uw_selected.selected is not None else None,
                        "Deductible Change Comments": hxd.cds.layers[layer].rate_change.deductible_change.comments,
                        "T&Cs Change": f"{hxd.cds.layers[layer].rate_change.terms_conditions_change.uw_selected.selected * 100:.1f}%" if hxd.cds.layers[layer].rate_change.terms_conditions_change.uw_selected.selected is not None else None,
                        "T&Cs Change Comments": hxd.cds.layers[layer].rate_change.terms_conditions_change.comments,
                        "Brokerage Change": f"{hxd.cds.layers[layer].rate_change.brokerage_change.uw_selected.selected * 100:.1f}%" if hxd.cds.layers[layer].rate_change.brokerage_change.uw_selected.selected is not None else None,
                        "Brokerage Change Comments": hxd.cds.layers[layer].rate_change.brokerage_change.comments,
                        "Other Change": f"{hxd.cds.layers[layer].rate_change.other_change.uw_selected.selected * 100:.1f}%" if hxd.cds.layers[layer].rate_change.other_change.uw_selected.selected is not None else None,
                        "Other Change Comments": hxd.cds.layers[layer].rate_change.other_change.comments,
                        "Final Rate Change": f"{hxd.cds.layers[layer].rate_change.risk_adjusted_rate_change.uw_selected * 100:.1f}%" if hxd.cds.layers[layer].rate_change.risk_adjusted_rate_change.uw_selected is not None else None,
                    } for layer in range (1,11) if hxd.cds.layers[layer].rate_change.premium_annualized_100pct.renewal is not None and hxd.cds.layers[layer].rate_change.premium_annualized_100pct.renewal != 0
            ] 
    else:
        rate_change_table = [{
            "Rate Change": "Rate Change Not Calculated",
        }]
    
    # Underwriting Notes Section
    uw_notes = hxd.cds.uw_notes
    # Extract and format the uw notes
    if uw_notes is None:
        formatted_uw_notes = ""
    elif isinstance(uw_notes, dict) and 'UW Notes' in uw_notes:
        formatted_uw_notes = uw_notes['UW Notes'].replace('\n', '<br>')
    else:
        formatted_uw_notes = uw_notes.replace('\n', '<br>')   

    formatted_uw_notes = format_note_field(uw_notes, 'UW Notes')

    mta_comments = hxd.cds.mid_term_adjustments
    # Extract and format the mta notes
    if mta_comments is None:
        formatted_mta_comments = ""
    elif isinstance(mta_comments, dict) and 'Mid Term Adjustments' in mta_comments:
        formatted_mta_comments = mta_comments['Mid Term Adjustments'].replace('\n', '<br>')
    else:
        formatted_mta_comments = mta_comments.replace('\n', '<br>')

    formatted_mta_comments = format_note_field(mta_comments, 'Mid Term Adjustments')

    # historical_comments = hxd.cds.historical_comments
    # # Extract and format the mta notes
    # if historical_comments is None:
    #     formatted_historical_comments = ""
    # elif isinstance(historical_comments, dict) and 'Historical Comments' in historical_comments:
    #     formatted_historical_comments = historical_comments['Historical Comments'].replace('\n', '<br>')
    # else:
    #     formatted_historical_comments = historical_comments.replace('\n', '<br>')        

    # NOTE: define all your tables here first as dictionaries (or list of dictionaries) with values coming from the hxd

    # Function to generate an HTML table
    def generate_html_table(data, title):
        html = f"<h2 class='section-title'>{title}</h2><table>"
        
        # Check if data is a list of dictionaries
        if isinstance(data, list) and all(isinstance(row, dict) for row in data):
            # Create table headers from the keys of the first dictionary
            headers = data[0].keys()
            html += "<tr>" + "".join(f"<th>{header}</th>" for header in headers) + "</tr>"
            
            # Create table rows
            for row in data:
                html += "<tr>" + "".join(f"<td>{row.get(header, '')}</td>" for header in headers) + "</tr>"
        # If data is a single dictionary (two-column table)
        elif isinstance(data, dict):
            for key, value in data.items():
                html += f"""
                <tr>
                    <td><strong>{key}</strong></td>
                    <td>{value}</td>
                </tr>"""
        
        html += "</table><br>"  # Add space after each table
        return html

    # Generate HTML content for each table by calling the function with a title
    # NOTE: this function lets you add the table to the HTML code (first argument), and set the title you want (second argument)
    # Add as many tables as you need
    title_html = f"<h1 style='color:#004A7C; font-family:Arial, sans-serif; font-weight: bold;'>{insured_name}</h1><br>"
    html_tables = ""
    html_tables += generate_html_table(risk_information, "Risk Information")
    html_tables += generate_html_table(account_scoring, "Account Scoring")
    if hxd.cds.exposure.granular.gmm_product.product != "Triage":
        html_tables += generate_html_table(primary_exposure_details, "Primary Exposure Details")
        html_tables += generate_html_table(secondary_exposure_details, "Secondary Exposure Details")
    else: 
        html_tables += generate_html_table(triage_doc_res, "Doctors and Residents")
        html_tables += generate_html_table(triage_procedures, "Procedures")
        html_tables += generate_html_table(triage_total_obe, "Total OBE")
        
    html_tables += generate_html_table(venue_factors, "Overall Venue Factors")
    html_tables += generate_html_table(venue_us_output, "US Venue Splits")
    html_tables += generate_html_table(venue_international_output, "International Venue Splits")
    html_tables += generate_html_table(coverage_details, "Coverage Details")
    html_tables += generate_html_table(coverage_limits, "Coverage Limits")
    html_tables += generate_html_table(enhancements, "Coverage Enhancements")
    html_tables += generate_html_table(primary_layer, "Primary Layer Pricing")
    html_tables += generate_html_table(excess_layers, "Excess Layer Pricing")

    if hxd.cds.rating_factors.pricing.tech_eo_products_media.include_primary or hxd.cds.rating_factors.pricing.well_tech_eo_media.include_primary:
        html_tables += generate_html_table(tech_rateable, "Tech EO")
        html_tables += generate_html_table(tech_eo_coverage_details, "Tech EO Coverage Details")

    if hxd.cds.rating_factors.cyber.product is not None :
        html_tables += generate_html_table(cyber_details, "Cyber")
        html_tables += generate_html_table(cyber_details_schedule_mods, "")
        html_tables += generate_html_table(cyber_totals, "")

    html_tables += generate_html_table(umbrella_inputs, "Umbrella Inputs")
    html_tables += generate_html_table(umbrella_outputs, "Umbrella Calculations")
    html_tables += generate_html_table(rating_summary_table, "Rating Summary")
    html_tables += generate_html_table(schedule_mods, "Schedule Modifiers")
    html_tables += generate_html_table(rate_change_table, "Rate Change")
    #... Add your tables here

    # Put all the tables together in HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; font-size: 12px; }}
            h1 {{ color: #004A7C; font-size: 16px; }}
            h2 {{ color: #CC007F; font-size: 14px; margin-top: 20px; }}
            table {{ width: 50%; border-collapse: collapse; font-size: 12px; margin: 0 auto; }}
            td, th {{ border: 1px solid #000; padding: 4px; text-align: left; }}
            th {{ background-color: #f2f2f2; font-weight: bold; }}
            .section-title {{ color: #CC007F; font-weight: bold; }}
        </style>
    </head>
    <body>
    <h1>{insured_name}</h1>
    {html_tables}
    
    <h2 class='section-title'>Underwriting Notes</h2><p>{formatted_uw_notes}</p>
    <h2 class='section-title'>Mid Term Adjustment Notes</h2><p>{formatted_mta_comments}</p>

    </body>
    </html>
    """
    updated_html_content = title_html + html_referral_content + html_content
    # Create the email message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Referral email - {insured_name}"
    msg["From"] = hxd.cds.email.sender # NOTE: can have address of the relevant UWs here so they can just reply and send after downloading the message
    msg["To"] = hxd.cds.email.recipient

    # Attach the HTML content to the email
    msg.attach(MIMEText(updated_html_content, "html"))

    # Save the email as an .eml file
    with hxd.cds.email.referral_file.open("b") as file:
        gen = BytesGenerator(file, policy=policy.default)
        gen.flatten(msg)


@hx.task
def save_uw_to_pas_reference(hxd, progress):
    pas_reference = hxd.cds.standard_fields.underwriter
    hx.meta.pas_references.clear()
    hx.meta.pas_references.append(pas_reference)

##############################
# These empty tasks are necessary to clear override for specific nodes in the Data Schema.
@hx.task
def clear_uw_rationale_task(hxd, progress):
    pass

@hx.task
def clear_overrides_task(hxd, progress):
    pass

@hx.task
def clear_exposures_task(hxd, progress):
    # set exposure data current and prior years to zero
    pass

@hx.task
def new_bug_report_task(hxd, progress):
    model_name = "GMMLS"
    new_bug_report(hxd, progress, model_name)

@hx.task
def send_bug_report_task(hxd, progress):
    send_bug_report(hxd, progress)

@hx.task
def cancel_bug_report_task(hxd, progress):
    cancel_bug_report(hxd, progress)

@hx.task
def generate_bug_report_task(hxd, progress):
    generate_bug_report(hxd, progress)

@hx.task
def add_additional_file_task(hxd, progress):
    add_additional_file(hxd, progress)

@hx.task
def generate_primary_proposal_template_task(hxd, progress):
    primary_email_generation.generate_email_proposal(hxd)
    
@hx.task
def generate_excess_proposal_template_task(hxd, progress):
    excess_email_generation.generate_email_proposal(hxd)