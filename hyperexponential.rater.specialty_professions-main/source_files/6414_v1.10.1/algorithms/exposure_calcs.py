import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
from operator import itemgetter

def exposure_calcs(hxd):

    # RATEABLE EXPOSURE SECTION ##############################################################

    # Exposure parameter table
    param_exprates = hx.params.tbl_exposureprop

    # define where exposure variables live in data schema
    cons_with_in_house = hxd.cds.exposure.granular.construction_with_in_house_design
    cons_sub_con = hxd.cds.exposure.granular.construction_with_sub_contracted_design
    desi_no_cons = hxd.cds.exposure.granular.design_only_no_construction
    cons_no_desi = hxd.cds.exposure.granular.construction_only_no_design
    at_risk = hxd.cds.exposure.granular.at_risk_construction_management
    agency_con = hxd.cds.exposure.granular.agency_construction_management
    other_exposure = hxd.cds.exposure.granular.other
    total_exposure = hxd.cds.exposure.granular.total

    # List of exposure variables
    lst_exposure_vbl = [
        cons_with_in_house,
        cons_sub_con,
        desi_no_cons,
        cons_no_desi,
        at_risk,
        agency_con,
        other_exposure]
    # List of exposure strings - for matching to parameter levels
    lst_exposure_str = [
        'Construction with In House Design',
        'Construction with Sub Contracted Design',
        'Design Only – No Construction',
        'Construction Only – No Design', 
        'At Risk Construction Management',
        'Agency Construction Management',
        'Other (specify)']

    # Assign variable name, other variable cannot be referenced
    cv_factor = [0, 0, 0, 0, 0, 0, 0]
    pf_factor = [0, 0, 0, 0, 0, 0, 0]
 
    # Loop through each exposure variable
    for loop_cv, loop_pf, loop_vbl, loop_str in zip(cv_factor, pf_factor, lst_exposure_vbl, lst_exposure_str):
        
        # param lookup
        param_lookup = param_exprates[param_exprates['Proportion'] == loop_str]
        
        # Look up cv and pf factor for each exposure variable
        loop_cv = param_lookup['Construction Values'].iloc[0]
        loop_pf = param_lookup['Professional Fees'].iloc[0]
  
        # Max of cv_factor x cv or pf_factor x pf                
        if (loop_vbl in [other_exposure]):
            loop_vbl.current_yr_rateable_exposure = loop_pf * loop_vbl.current_yr_professional_fees
            loop_vbl.last_yr_rateable_exposure = loop_pf * loop_vbl.last_yr_professional_fees
            loop_vbl.two_yr_ago_rateable_exposure = loop_pf * loop_vbl.two_yr_ago_professional_fees    
        else:            
            loop_vbl.current_yr_rateable_exposure = max(loop_cv * loop_vbl.current_yr_construction_value, loop_pf * loop_vbl.current_yr_professional_fees)
            loop_vbl.last_yr_rateable_exposure = max(loop_cv * loop_vbl.last_yr_construction_value, loop_pf * loop_vbl.last_yr_professional_fees)
            loop_vbl.two_yr_ago_rateable_exposure = max(loop_cv * loop_vbl.two_yr_ago_construction_value, loop_pf * loop_vbl.two_yr_ago_professional_fees)
                                                   
    pass

    # Calculate total

    # create separate list for construction value as Other - CV does not exist
    lst_exposure_vbl_cv = [cons_with_in_house,cons_sub_con, desi_no_cons, cons_no_desi, at_risk, agency_con, other_exposure]

    # Set up bucket to store data
    total_exposure.current_yr_construction_value = 0
    total_exposure.current_yr_professional_fees = 0
    total_exposure.current_yr_rateable_exposure = 0
    total_exposure.last_yr_construction_value = 0
    total_exposure.last_yr_professional_fees = 0
    total_exposure.last_yr_rateable_exposure = 0
    total_exposure.two_yr_ago_construction_value = 0
    total_exposure.two_yr_ago_professional_fees = 0
    total_exposure.two_yr_ago_rateable_exposure = 0

    # Total professional fees and rateable exposure

    # Sum current year
    total_exposure.current_yr_professional_fees = sum([vbl.current_yr_professional_fees for vbl in lst_exposure_vbl])
    total_exposure.current_yr_rateable_exposure = sum([vbl.current_yr_rateable_exposure for vbl in lst_exposure_vbl])

    # Sum last year
    total_exposure.last_yr_professional_fees = sum([vbl.last_yr_professional_fees for vbl in lst_exposure_vbl])
    total_exposure.last_yr_rateable_exposure = sum([vbl.last_yr_rateable_exposure for vbl in lst_exposure_vbl])

    # Sum two years ago
    total_exposure.two_yr_ago_professional_fees = sum([vbl.two_yr_ago_professional_fees for vbl in lst_exposure_vbl])
    total_exposure.two_yr_ago_rateable_exposure = sum([vbl.two_yr_ago_rateable_exposure for vbl in lst_exposure_vbl])
    

    # Total construction value
    # Sum current year
    total_exposure.current_yr_construction_value = sum([vbl.current_yr_construction_value for vbl in lst_exposure_vbl_cv])
    
    # Sum last year
    total_exposure.last_yr_construction_value = sum([vbl.last_yr_construction_value for vbl in lst_exposure_vbl_cv])

    # Sum two years ago
    total_exposure.two_yr_ago_construction_value = sum([vbl.two_yr_ago_construction_value for vbl in lst_exposure_vbl_cv])      
        
    # AVERAGE RATEABLE EXPOSURE SECTION ##############################################################

    # Calculate average rateable exposure for each exposure metric
    for loop_vbl, loop_str in zip(lst_exposure_vbl, lst_exposure_str):
        
        # three year average calc
        if (loop_vbl.two_yr_ago_rateable_exposure == 0):
            loop_vbl.three_yr_avg_rateable_exposure = 0            
        else:
            loop_vbl.three_yr_avg_rateable_exposure = (loop_vbl.two_yr_ago_rateable_exposure + loop_vbl.last_yr_rateable_exposure + loop_vbl.current_yr_rateable_exposure)/3

        # two year average calc
        if (loop_vbl.two_yr_ago_rateable_exposure == 0) and (loop_vbl.last_yr_rateable_exposure == 0):
            loop_vbl.two_yr_avg_rateable_exposure = 0            
        else:
            loop_vbl.two_yr_avg_rateable_exposure = (loop_vbl.last_yr_rateable_exposure + loop_vbl.current_yr_rateable_exposure)/2

        # current year
        loop_vbl.current_yr_avg_rateable_exposure = loop_vbl.current_yr_rateable_exposure

        # Default selected avg rateable exposure to fiscal year
        loop_vbl.selected_avg_rateable_exposure.calculated = loop_vbl.current_yr_avg_rateable_exposure

    # Set up bucket to store data
    total_exposure.three_yr_avg_rateable_exposure = 0
    total_exposure.two_yr_avg_rateable_exposure = 0
    total_exposure.current_yr_avg_rateable_exposure = 0
    total_exposure.selected_avg_rateable_exposure = 0

    # Calculate total

    # total of three year average rateable exposure
    total_exposure.three_yr_avg_rateable_exposure = sum([vbl.three_yr_avg_rateable_exposure for vbl in lst_exposure_vbl])

    # total of two year average rateable exposure
    total_exposure.two_yr_avg_rateable_exposure = sum([vbl.two_yr_avg_rateable_exposure for vbl in lst_exposure_vbl])

    # total of current year average rateable exposure
    total_exposure.current_yr_avg_rateable_exposure = sum([vbl.current_yr_avg_rateable_exposure for vbl in lst_exposure_vbl])

    # total of UW selected average rateable exposure
    total_exposure.selected_avg_rateable_exposure = sum([vbl.selected_avg_rateable_exposure.selected for vbl in lst_exposure_vbl])    

    # Default override total to selected total
    total_exposure.override_avg_rateable_exposure.calculated = total_exposure.selected_avg_rateable_exposure
    
    # Save down total rateable exposure into aggregate node
    hxd.cds.exposure.aggregate.rateable_exposure = total_exposure.override_avg_rateable_exposure.selected

    # Respread override exposure
    for loop_vbl in lst_exposure_vbl:

        # total of three year avg
        if (total_exposure.override_avg_rateable_exposure.calculated == 0):
            loop_vbl.override_avg_rateable_exposure = 0
        else:
            loop_vbl.override_avg_rateable_exposure = (loop_vbl.selected_avg_rateable_exposure.selected / total_exposure.selected_avg_rateable_exposure) * total_exposure.override_avg_rateable_exposure.selected      
   
    