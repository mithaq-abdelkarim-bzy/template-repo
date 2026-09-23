import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
from operator import itemgetter
from datetime import datetime



def rate_exposure_details(hxd):
    cds = hxd.cds

    #----------------------------------------------------------------------------------------------#
    #step 1: Set the show/hide masking for GMM/GLSN rater as well as US/International 
    #----------------------------------------------------------------------------------------------#

    #Masking for GMM/GLSN rater as well as US/International locations are set below and triage
    cds.gmm_masking = cds.rater_selection == "Global Misc Med Rater"
    cds.glsn_masking = cds.rater_selection == "Global Life Sciences Rater"
    cds.us_masking = cds.rating_factors.us_international_choice_of_law.us_international == "US"
    cds.international_masking = cds.rating_factors.us_international_choice_of_law.us_international == "International"
    cds.us_and_international_masking = cds.exposure.granular.include_international_venues 
    cds.international_and_us_masking = cds.exposure.granular.include_us_venues
    if cds.gmm_masking:
        cds.triage_masking = cds.exposure.granular.gmm_product.product == "Triage"
        cds.exposure_masking = cds.exposure.granular.gmm_product.product != "Triage"
    else:
        cds.triage_masking = False
        cds.exposure_masking = True
    
    inception_date_for_label = hxd.hx_core.inception_date
    cds.rating_factors.current_year_label = inception_date_for_label.year
    cds.rating_factors.one_years_ago_label = inception_date_for_label.year - 1
    cds.rating_factors.two_years_ago_label = inception_date_for_label.year - 2
    cds.rating_factors.three_years_ago_label = inception_date_for_label.year - 3
    cds.rating_factors.four_years_ago_label = inception_date_for_label.year - 4
    cds.rating_factors.five_years_ago_label = inception_date_for_label.year - 5


    # Set the currency
        
    if cds.international_masking:
        cds.rating_factors.currency.calculated = hx.params.table_choice_of_law[hx.params.table_choice_of_law["choice_of_law"] == cds.rating_factors.us_international_choice_of_law.choice_of_law ]["default_currency"].iloc[0]
    else:
        cds.rating_factors.currency.calculated = "USD"

    cds.currencies.source_currency = cds.rating_factors.currency.selected
    #----------------------------------------------------------------------------------------------#
    #step 2: Calculate Total Net Score and Account Score 
    #----------------------------------------------------------------------------------------------#

    # Account scorings list
    account_scoring_list = hx.params.table_account_scoring["account_scoring_name"]

    # Get the individual scorings input from the UI
    account_scoring = []
    for item in account_scoring_list:
        account_scoring.append(getattr(getattr(hxd.cds.rating_factors.account_scoring , item ), "value"))
    total_net_score = sum(account_scoring)

    # Export value to UI
    cds.rating_factors.total_net_score.value = total_net_score

    #Calculate the account score and export it to the UI
    if total_net_score >=5 :
        account_score = "A"
    elif total_net_score >=3 :
        account_score = "B"
    elif total_net_score >=-2 :
        account_score = "C"
    elif total_net_score >=-4 :
        account_score = "D"
    else :
        account_score = "F"

    cds.rating_factors.account_score = account_score  


    #----------------------------------------------------------------------------------------------#
    #step 3: Calculate supply chain and clinical trial factors for glsn
    #----------------------------------------------------------------------------------------------#

    if cds.glsn_masking == True:
        supply_chain_selection = cds.rating_factors.glsn.supply_chain
        supply_chain = hx.params.table_glsn_supply_chain
        supply_chain_filtered = supply_chain[supply_chain["supply_chain_label"] == supply_chain_selection]
        supply_chain_asign = supply_chain_filtered["factor"].iloc[0]
        cds.rating_factors.glsn.supply_chain_factor = supply_chain_asign

    if cds.glsn_masking == True:    
        clinical_trial_selection = cds.rating_factors.glsn.clinical_trial
        clinical_trial = hx.params.table_glsn_clinical_trial
        clinical_trial_filtered = clinical_trial[clinical_trial["clinical_trial_label"] == clinical_trial_selection]
        clinical_trial_asign = clinical_trial_filtered["factor"].iloc[0]
        cds.rating_factors.glsn.clinical_trial_factor = clinical_trial_asign


    #----------------------------------------------------------------------------------------------#
    #step 4: Calculate venue factors 
    #----------------------------------------------------------------------------------------------#

    #step 4.A: Calculate venue factors if International is selected    

    # International venu factor list
    venue_international_list = hx.params.table_venue_international["venue_name"]
    venue_international_params = hx.params.table_venue_international

    # get the venue percentage input from the UI
    venue_international_ptc = []
    venue_international_selection = []
    for item in venue_international_list:
        venue_international_ptc.append(getattr(getattr(hxd.cds.exposure.granular , item ),"percentage"))
        venue_international_selection.append(getattr(getattr(hxd.cds.exposure.granular , item ), "selection"))


    # US venu factor list
    venue_us_list = hx.params.table_venue_us["venue_name"]
    venue_us_params = hx.params.table_venue_us

    venue_us_and_international = cds.exposure.granular.include_international_venues
    venue_international_and_us = cds.exposure.granular.include_us_venues

    # Get the venue percentage input from the UI and the selection of the relevant states
    venue_us_ptc = []
    venue_us_selection = []
    for item in venue_us_list:
        venue_us_ptc.append(getattr(getattr(hxd.cds.exposure.granular , item ),"percentage"))
        venue_us_selection.append(getattr(getattr(hxd.cds.exposure.granular , item ), "selection"))
    venue_us_ptc = pd.Series(venue_us_ptc)
    venue_us_selection = pd.Series(venue_us_selection)

    # Create a pandas table for each 
    venue_international_df = pd.DataFrame({"venue_international": venue_international_list, "venue_international_pct": venue_international_ptc,"selection": venue_international_selection})
    venue_us_df = pd.DataFrame({"venue_us": venue_us_list, "venue_us_pct": venue_us_ptc,"selection": venue_us_selection})
    
    # # Add flag for percentage input being completed
    # venue_international_df["percentage_complete"] = venue_international_df["venue_international_pct"] > 0  # IR edit
    # venue_us_df["percentage_complete"] = venue_us_df["venue_us_pct"] > 0 # IR edit

    # map the relativity
    venue_international_df = venue_international_df.merge( venue_international_params, how = "left", left_on = "venue_international", right_on = "venue_name")
    venue_us_df = venue_us_df.merge( venue_us_params, how = "left", left_on = "venue_us", right_on = "venue_name")


    # # Sum product to get the total factor   
    total_venue_international_factor = (venue_international_df["venue_international_pct"]*venue_international_df["factor"]*venue_international_df["selection"]).sum()
    total_venue_us_factor = (venue_us_df["venue_us_pct"] * venue_us_df["factor"] * venue_us_df["selection"]).sum()
    

   
    # Export back to UI
    for index,item in  enumerate(venue_international_list):
        setattr(getattr(hxd.cds.exposure.granular , item ), "factor", venue_international_df[venue_international_df["venue_international"] == item]["factor"].iloc[0])
        setattr(getattr(hxd.cds.exposure.granular , item ), "percentage_output_copy", venue_international_df["venue_international_pct"].iloc[index])
        # setattr(getattr(hxd.cds.exposure.granular , item ), "percentage_complete", venue_international_df[venue_international_df["venue_international"] == item]["percentage_complete"].iloc[0]) # IR edit
    cds.exposure.aggregate.total_venue_international_factor = total_venue_international_factor           
    
    for index, item in  enumerate(venue_us_list):
        setattr(getattr(hxd.cds.exposure.granular , item ), "factor", venue_us_df[venue_us_df["venue_us"] == item]["factor"].iloc[0])
        setattr(getattr(hxd.cds.exposure.granular , item ), "percentage_output_copy", venue_us_df["venue_us_pct"].iloc[index])
        # setattr(getattr(hxd.cds.exposure.granular , item ), "percentage_complete", venue_us_df[venue_us_df["venue_us"] == item]["percentage_complete"].iloc[0]) # IR edit
    cds.exposure.aggregate.total_venue_us_factor = total_venue_us_factor
    
    #Set the total venue factor 
    cds.exposure.aggregate.total_venue_factor = total_venue_us_factor + total_venue_international_factor
    cds.exposure.aggregate.total_percentage_selected = (venue_us_df["venue_us_pct"] * venue_us_df["selection"]).sum() + (venue_international_df["venue_international_pct"] * venue_international_df["selection"]).sum()


     




    if cds.exposure.aggregate.total_venue_factor == 0:
        hx.errors.validation("Venue Factor Missing")

    if round(cds.exposure.aggregate.total_percentage_selected, 3) != 1 :
        hx.errors.validation("Total Venue Split must equal 100%")  
    

   


    #----------------------------------------------------------------------------------------------#
    #step 5: Carry out primary and secondary exposure calcualtions and calculate base premium
    #----------------------------------------------------------------------------------------------#

    #5.A We need to determine currencies for exposure measures other than receipts. 

    # FX rate for currency conversion - from user library
    fx_rates = params.fx_rates.df()
    ccy = cds.currencies.source_currency
    fx_rate = utils.look_up(ccy, 'ccy', 'fx_rate', fx_rates, if_not_found=1) # default to USD if error
    currency_factor = 1 / fx_rate

    #5.B First calculate base premiums for GMM 
    if cds.gmm_masking == True:
        gmm_cob_class = cds.exposure.granular.gmm_product.cob_class
        gmm_exposure = hx.params.table_gmm_exposure_classes
        gmm_exposure_filtered = gmm_exposure[gmm_exposure["class"] == gmm_cob_class]
        gmm_exposure_asign = gmm_exposure_filtered.loc[:,["class","exposure_measure","base_rate","exposure_measure_agg_group","formatted_base_rate"]].reset_index(drop=True)
        gmm_exposure_asign = gmm_exposure_asign.rename(columns={"class": "exposure_class"})
        utils.write_pd_to_hxd(gmm_exposure_asign,cds.exposure.granular.gmm_primary_exposure_details,["exposure_class","exposure_measure","base_rate","formatted_base_rate"])
        #Bring through the inputs from the UI here and asign to a dataframe
        gmm_primary_exposure = utils.pd_df_from_hx_list(cds.exposure.granular.gmm_primary_exposure_details)
        gmm_primary_exposure = gmm_primary_exposure.loc[:,["exposure_class","exposure_measure","current_year","one_years_ago","selection","show_row"]]
        gmm_primary_exposure['show_row'] = np.where((gmm_primary_exposure['exposure_class'].isnull()),False,True)
        gmm_primary_base_premium = gmm_exposure_asign.merge(gmm_primary_exposure , how = "left", left_on = ['exposure_class','exposure_measure'], right_on = ['exposure_class','exposure_measure'])

        # try:
        gmm_primary_base_premium['base_premium'] = np.where(gmm_primary_base_premium['exposure_measure'].str.contains('Receipts', case = False), gmm_primary_base_premium['base_rate'] * gmm_primary_base_premium['current_year'] * currency_factor , gmm_primary_base_premium['base_rate'] * gmm_primary_base_premium['current_year']) / currency_factor
        gmm_primary_base_premium['base_premium_one_years_ago'] = np.where(gmm_primary_base_premium['exposure_measure'].str.contains('Receipts', case = False), gmm_primary_base_premium['base_rate'] * gmm_primary_base_premium['one_years_ago'] * currency_factor , gmm_primary_base_premium['base_rate'] * gmm_primary_base_premium['one_years_ago']) / currency_factor
        # except:
            # gmm_primary_base_premium['base_premium'] = 0 

        gmm_primary_base_premium = gmm_primary_base_premium.fillna(0)
        utils.write_pd_to_hxd(gmm_primary_base_premium,cds.exposure.granular.gmm_primary_exposure_details,["base_premium","show_row"])
        

        #Secondary class calculations for GMM- slightly different format here as the classes are inputs rather than outputs, but once the pd dataframe is set up we can use the same calcs
        gmm_secondary_exposure_dict = [{
            "exposure_class": item.gmm_secondary_exposure.exposure_class,
            "exposure_measure": item.gmm_secondary_exposure.exposure_measure,
            "base_rate": item.base_rate,
            "five_years_ago": item.five_years_ago,
            "four_years_ago": item.four_years_ago,
            "three_years_ago": item.three_years_ago,
            "two_years_ago": item.two_years_ago,
            "one_years_ago": item.one_years_ago,
            "current_year": item.current_year,
            "selection": item.selection,
            "base_premium": item.base_premium,
            "formatted_base_rate": item.base_premium
        } for item in cds.exposure.granular.gmm_secondary_exposure_details]
        gmm_secondary_exposure = pd.DataFrame(gmm_secondary_exposure_dict)
        
        gmm_secondary_exposure = gmm_secondary_exposure.loc[:,["exposure_class","exposure_measure","current_year","one_years_ago","selection"]]
        gmm_exposure = gmm_exposure.rename(columns={"class":"exposure_class"})
        gmm_secondary_base_premium = gmm_secondary_exposure.merge(gmm_exposure, how = "left", left_on = ['exposure_class','exposure_measure'], right_on = ['exposure_class','exposure_measure'])
        # try:
        gmm_secondary_base_premium['base_premium'] = np.where(gmm_secondary_base_premium['exposure_measure'].str.contains('Receipts', case = False) , gmm_secondary_base_premium['base_rate'] * gmm_secondary_base_premium['current_year'] * currency_factor , gmm_secondary_base_premium['base_rate'] * gmm_secondary_base_premium['current_year'] ) / currency_factor
        gmm_secondary_base_premium['base_premium_one_years_ago'] = np.where(gmm_secondary_base_premium['exposure_measure'].str.contains('Receipts', case = False) , gmm_secondary_base_premium['base_rate'] * gmm_secondary_base_premium['one_years_ago'] * currency_factor , gmm_secondary_base_premium['base_rate'] * gmm_secondary_base_premium['one_years_ago'] ) / currency_factor
        gmm_secondary_base_premium = gmm_secondary_base_premium.fillna(0)
        # except:
        #         gmm_secondary_base_premium['base_premium'] = 0 
 
                
        if sum(gmm_secondary_base_premium['base_premium'])>=0:
            utils.write_pd_to_hxd(gmm_secondary_base_premium,cds.exposure.granular.gmm_secondary_exposure_details,["base_rate","base_premium","formatted_base_rate"])  

        #Total GMM base premium 
        gmm_selected_base_premium = (gmm_primary_base_premium["base_premium"] * gmm_primary_base_premium["selection"]).sum() + (gmm_secondary_base_premium["base_premium"] * gmm_secondary_base_premium["selection"]).sum()
        gmm_selected_base_premium_one_years_ago = (gmm_primary_base_premium["base_premium_one_years_ago"] * gmm_primary_base_premium["selection"]).sum() + (gmm_secondary_base_premium["base_premium_one_years_ago"] * gmm_secondary_base_premium["selection"]).sum()
        cds.exposure.aggregate.gmm_total_base_premium_current_year = gmm_selected_base_premium
        cds.exposure.aggregate.gmm_total_base_premium_one_years_ago = (gmm_selected_base_premium_one_years_ago if cds.exposure.aggregate.temp_gmm_total_base_premium_one_years_ago == 0 else cds.exposure.aggregate.temp_gmm_total_base_premium_one_years_ago)

        # set info by
        cds.exposure.aggregate.gmm_total_base_premium_one_years_ago_info_by = "The Previous Year Base Premium is revalued in the renewal currency and is derived from the expiry option. However, it may not match the previous year displayed exposure if there has been a change in the Class of Business (COB)."

        # Validation checks 
        if gmm_selected_base_premium == 0 and cds.exposure.granular.gmm_product.product != "Triage":
            hx.errors.validation("Please complete Exposure Details sheet")

        receipts_table_primary =  gmm_primary_base_premium[gmm_primary_base_premium["exposure_measure_agg_group"] == "Receipts"] 
        receipts_table_secondary =  gmm_secondary_base_premium[gmm_secondary_base_premium["exposure_measure"] == "Receipts"] 
        receipts_used = (receipts_table_primary["current_year"] * receipts_table_primary["selection"]).sum() + (receipts_table_secondary["current_year"] * receipts_table_secondary["selection"]).sum()

        non_receipts_table_primary =  gmm_primary_base_premium[gmm_primary_base_premium["exposure_measure_agg_group"] != "Receipts"] 
        non_receipts_table_secondary =  gmm_secondary_base_premium[gmm_secondary_base_premium["exposure_measure"] != "Receipts"] 
        non_receipts_used = (non_receipts_table_primary["current_year"] * non_receipts_table_primary["selection"]).sum() + (non_receipts_table_secondary["current_year"] * non_receipts_table_secondary["selection"]).sum()

        if receipts_used > 0 and non_receipts_used > 0 :
            cds.rating_factors.mix_of_exposure_measures_message = "Receipts should not be used with any other exposure base"
            cds.rating_factors.exposure_measures_message_show = True

    #5.C Then the base premiums for GLSN  
    if cds.glsn_masking == True:
        glsn_cob_class = cds.exposure.granular.glsn_product.cob_code_description
        glsn_exposure = hx.params.table_glsn_exposure_classes
        glsn_base_rate_adjustment = hx.params.table_glsn_base_rate_commission.loc[0,"base_rate_standard_commission"]
        #Gross up the GLSN base rates based on standard brokerage
        glsn_exposure["base_rate"] = glsn_exposure["base_rate"] / (1-glsn_base_rate_adjustment)
        glsn_exposure_filtered = glsn_exposure[glsn_exposure["cob"] == glsn_cob_class]
        glsn_exposure_asign = glsn_exposure_filtered.loc[:,["cob","exposure_base","exposure_measure","base_rate","formatted_base_rate"]].reset_index(drop=True)
        utils.write_pd_to_hxd(glsn_exposure_asign,cds.exposure.granular.glsn_primary_exposure_details,["cob","exposure_base","exposure_measure","base_rate","formatted_base_rate"])

        #Bring through the inputs from the UI here and asign to a dataframe
        glsn_primary_exposure = utils.pd_df_from_hx_list(cds.exposure.granular.glsn_primary_exposure_details)
        glsn_primary_exposure = glsn_primary_exposure.loc[:,["exposure_base","exposure_measure","current_year","one_years_ago","selection","show_row"]]
        glsn_primary_exposure['show_row'] = np.where((glsn_primary_exposure['exposure_base'].isnull()),False,True)
        glsn_primary_base_premium = glsn_exposure_asign.merge(glsn_primary_exposure , how = "left", left_on = ['exposure_base','exposure_measure'], right_on = ['exposure_base','exposure_measure'])
        # try:
        glsn_primary_base_premium['base_premium'] = np.where(glsn_primary_base_premium['exposure_measure'].str.contains('Receipts', case = False), glsn_primary_base_premium['base_rate'] * glsn_primary_base_premium['current_year'] * currency_factor , glsn_primary_base_premium['base_rate'] * glsn_primary_base_premium['current_year'] ) / currency_factor
        glsn_primary_base_premium['base_premium_one_years_ago'] = np.where(glsn_primary_base_premium['exposure_measure'].str.contains('Receipts', case = False), glsn_primary_base_premium['base_rate'] * glsn_primary_base_premium['one_years_ago'] * currency_factor , glsn_primary_base_premium['base_rate'] * glsn_primary_base_premium['one_years_ago'] ) / currency_factor
            
        # except:
        #     glsn_primary_base_premium['base_premium'] = 0 
        glsn_primary_base_premium = glsn_primary_base_premium.fillna(0)
        utils.write_pd_to_hxd(glsn_primary_base_premium,cds.exposure.granular.glsn_primary_exposure_details,["base_premium","show_row"])
        

        #Secondary class calculations for GLSN - slightly different format here as the classes are inputs rather than outputs, but once the pd dataframe is set up we can use the same calcs
        #glsn_secondary_exposure = utils.pd_df_from_hx_list(cds.exposure.granular.glsn_secondary_exposure_details)
        #glsn_secondary_exposure = glsn_secondary_exposure.rename(columns={"glsn_secondary_exposure.exposure_base": "exposure_base","glsn_secondary_exposure.exposure_measure": "exposure_measure"})
        glsn_secondary_exposure_dict = [{
            "exposure_base": item.glsn_secondary_exposure.exposure_base,
            "exposure_measure": item.glsn_secondary_exposure.exposure_measure,
            "base_rate": item.base_rate,
            "five_years_ago": item.five_years_ago,
            "four_years_ago": item.four_years_ago,
            "three_years_ago": item.three_years_ago,
            "two_years_ago": item.two_years_ago,
            "one_years_ago": item.one_years_ago,
            "current_year": item.current_year,
            "selection": item.selection,
            "base_premium": item.base_premium,
            "formatted_base_rate": item.formatted_base_rate
        } for item in cds.exposure.granular.glsn_secondary_exposure_details]
        glsn_secondary_exposure = pd.DataFrame(glsn_secondary_exposure_dict)

        glsn_secondary_exposure = glsn_secondary_exposure.loc[:,["exposure_base","exposure_measure","current_year","one_years_ago","selection"]]
        glsn_secondary_base_premium = glsn_secondary_exposure.merge(glsn_exposure, how = "left", left_on = ['exposure_base','exposure_measure'], right_on = ['exposure_base','exposure_measure'])
        # try:
        glsn_secondary_base_premium['base_premium'] = np.where(glsn_secondary_base_premium['exposure_measure'].str.contains('Receipts', case = False), glsn_secondary_base_premium['base_rate'] * glsn_secondary_base_premium['current_year']  * currency_factor , glsn_secondary_base_premium['base_rate'] * glsn_secondary_base_premium['current_year']) / currency_factor
        glsn_secondary_base_premium['base_premium_one_years_ago'] = np.where(glsn_secondary_base_premium['exposure_measure'].str.contains('Receipts', case = False), glsn_secondary_base_premium['base_rate'] * glsn_secondary_base_premium['one_years_ago']  * currency_factor , glsn_secondary_base_premium['base_rate'] * glsn_secondary_base_premium['one_years_ago']) / currency_factor
        glsn_secondary_base_premium = glsn_secondary_base_premium.fillna(0)
        # except:
        #         glsn_secondary_base_premium['base_premium'] = 0 

        if sum(glsn_secondary_base_premium['base_premium'])>=0:
           utils.write_pd_to_hxd(glsn_secondary_base_premium,cds.exposure.granular.glsn_secondary_exposure_details,["base_rate","base_premium","formatted_base_rate"]) 
        

        #Total GLSN base premium 
        glsn_selected_base_premium = (glsn_primary_base_premium["base_premium"] * glsn_primary_base_premium["selection"]).sum() + (glsn_secondary_base_premium["base_premium"] * glsn_secondary_base_premium["selection"]).sum()
        glsn_selected_base_premium_one_years_ago = (glsn_primary_base_premium["base_premium_one_years_ago"] * glsn_primary_base_premium["selection"]).sum() + (glsn_secondary_base_premium["base_premium_one_years_ago"] * glsn_secondary_base_premium["selection"]).sum()
        cds.exposure.aggregate.glsn_total_base_premium_current_year = glsn_selected_base_premium
        cds.exposure.aggregate.glsn_total_base_premium_one_years_ago = (glsn_selected_base_premium_one_years_ago if cds.exposure.aggregate.temp_glsn_total_base_premium_one_years_ago == 0 else cds.exposure.aggregate.temp_glsn_total_base_premium_one_years_ago)

        # set info by
        cds.exposure.aggregate.glsn_total_base_premium_one_years_ago_info_by = "The Previous Year Base Premium is revalued in the renewal currency and is derived from the expiry option. However, it may not match the previous year displayed exposure if there has been a change in the Class of Business (COB)."  

        # Validation checks
        if cds.exposure.granular.glsn_product.cob_code_description == 'HI : Sponsored Clinical Trials':
            cds.rating_factors.glsn.size_discount_selection.calculated = "Participants"
        else:
            cds.rating_factors.glsn.size_discount_selection.calculated = "Revenue"
        
        if glsn_selected_base_premium == 0:
            hx.errors.validation("Please complete Exposure Details sheet")

        receipts_table_primary =  glsn_primary_base_premium[glsn_primary_base_premium["exposure_measure"] == "Receipts"] 
        receipts_table_secondary =  glsn_secondary_base_premium[glsn_secondary_base_premium["exposure_measure"] == "Receipts"] 
        receipts_used = (receipts_table_primary["current_year"] * receipts_table_primary["selection"]).sum() + (receipts_table_secondary["current_year"] * receipts_table_secondary["selection"]).sum()

        non_receipts_table_primary =  glsn_primary_base_premium[glsn_primary_base_premium["exposure_measure"] != "Receipts"] 
        non_receipts_table_secondary =  glsn_secondary_base_premium[glsn_secondary_base_premium["exposure_measure"] != "Receipts"] 
        non_receipts_used = (non_receipts_table_primary["current_year"] * non_receipts_table_primary["selection"]).sum() + (non_receipts_table_secondary["current_year"] * non_receipts_table_secondary["selection"]).sum()

        if receipts_used > 0 and non_receipts_used > 0 :
            cds.rating_factors.mix_of_exposure_measures_message = "Receipts should not be used with any other exposure base"
            cds.rating_factors.exposure_measures_message_show = True
            # hx.errors.validation("Receipts should not be used with any other exposure base")    
       
        participants_table_primary = glsn_primary_base_premium[glsn_primary_base_premium["exposure_measure"] == "Participants"]
        participants_table_secondary = glsn_secondary_base_premium[glsn_secondary_base_premium["exposure_measure"] == "Participants"]
        partcipants_used = (participants_table_primary["current_year"] * participants_table_primary["selection"]).sum() + (participants_table_secondary["current_year"] * participants_table_secondary["selection"]).sum()
        cds.rating_factors.glsn.number_of_participants = partcipants_used

        if cds.rating_factors.glsn.size_discount_selection.selected == "Participants" and partcipants_used <= 0 :
            hx.errors.validation("Participants is selected for Size Discount calculation. Please give Participant exposure")

    #----------------------------------------------------------------------------------------------#
    #step 6: Cyber Cover selection
    #----------------------------------------------------------------------------------------------#
    if cds.gmm_masking : 
        product_selection = cds.exposure.granular.gmm_product.product
        product_override_selection = cds.rating_factors.gmm.product_override
        if (product_selection == "Virtual Care") | (product_override_selection == "Virtual Care"):
            cyber_selection = True
        else:
            cyber_selection = False
    elif cds.glsn_masking:
        product_selection = cds.exposure.granular.glsn_product.product
        product_override_selection = cds.rating_factors.glsn.form.selected     
        if (product_selection == "Virtual Care") | (product_override_selection == "Virtual Care") | (product_selection == "WellTech") | (product_override_selection == "WellTech") :
            cyber_selection = True
        else:
            cyber_selection = False
    cds.cyber_selection = cyber_selection



      

    
