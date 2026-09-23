import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter



def rate_triage(hxd):
    cds = hxd.cds

    #----------------------------------------------------------------------------------------------#
    # Triage Pricing
    #----------------------------------------------------------------------------------------------#

    if cds.triage_masking == True:
        # Set UI 
        doctors_residents_params = hx.params.table_triage_doctors_residents
        utils.write_pd_to_hxd(doctors_residents_params,cds.exposure.granular.triage_doctors_residents,["specialty","iso_code","iso_class","obe_per_doctor","obe_per_resident"])

        obe_params = hx.params.table_triage_obe
        obe_params_filtered = obe_params[(obe_params["category"]=="Beds") | (obe_params["category"]=="Procedures")]

        utils.write_pd_to_hxd(obe_params_filtered,cds.exposure.granular.triage_procedures,["category","exposure_measure","obe_or_fte","formatted_obe_or_fte"])
        utils.write_pd_to_hxd(obe_params,cds.exposure.granular.triage_historical_obe,["category","exposure_measure","obe_or_fte","obe_equivalent","formatted_obe_or_fte"])

        # Sort OBE from UI
        doctors_residents = utils.pd_df_from_hx_list(cds.exposure.granular.triage_doctors_residents)
        doctors_residents = doctors_residents.groupby(['iso_class']).sum().reset_index()

        doctors = doctors_residents.loc[:,["iso_class","doc_current_year","doc_one_years_ago","doc_two_years_ago","doc_three_years_ago","doc_four_years_ago"]]
        doctors = doctors.rename(columns={"iso_class": "exposure_measure","doc_current_year": "current_year","doc_one_years_ago": "one_years_ago","doc_two_years_ago": "two_years_ago","doc_three_years_ago": "three_years_ago","doc_four_years_ago": "four_years_ago"})
        doctors["category"] = "Employed Doctors"
        residents = doctors_residents.loc[:,["iso_class","resident_current_year","resident_one_years_ago","resident_two_years_ago","resident_three_years_ago","resident_four_years_ago"]]
        residents = residents.rename(columns={"iso_class": "exposure_measure","resident_current_year": "current_year","resident_one_years_ago": "one_years_ago","resident_two_years_ago": "two_years_ago","resident_three_years_ago": "three_years_ago","resident_four_years_ago": "four_years_ago"})
        residents["category"] = "Residents"

        doctors_residents = doctors.append(residents)

        procedures = utils.pd_df_from_hx_list(cds.exposure.granular.triage_procedures)
        procedures = procedures.loc[:,["category","exposure_measure","current_year","one_years_ago","two_years_ago","three_years_ago","four_years_ago"]]
        
        obe = procedures.append(doctors_residents)
        
        # Carry out OBE calcs
        obe_table = utils.pd_df_from_hx_list(cds.exposure.granular.triage_historical_obe)
        obe_table["overall_obe"] = obe_table["obe_or_fte"] * obe_table["obe_equivalent"]
        obe_table = obe_table.loc[:,["category","exposure_measure","overall_obe"]]

        #Merge this with the obe table of inputs and then calcualte the OBEs. Note the merge isn't working due to the iso_class in the OBE table being a float and the obe_table iso_class being an int. Set both to strings then merge
        merged_obe_table = obe_table.merge(obe,how="left",left_on = ['category','exposure_measure'], right_on = ['category','exposure_measure'])
        overall_obe = merged_obe_table["overall_obe"]

        obe_output = merged_obe_table[['current_year','one_years_ago','two_years_ago','three_years_ago','four_years_ago']].mul(overall_obe,axis=0)

        utils.write_pd_to_hxd(obe_output,cds.exposure.granular.triage_historical_obe,['current_year','one_years_ago','two_years_ago','three_years_ago','four_years_ago'])
        utils.write_pd_to_hxd(merged_obe_table,cds.exposure.granular.triage_historical_obe,['overall_obe'])       

        running_total_obe = obe_output.sum().to_frame().T
        utils.write_pd_to_hxd(running_total_obe,cds.exposure.aggregate.triage_running_total_obe,['current_year','one_years_ago','two_years_ago','three_years_ago','four_years_ago'])






      

    
