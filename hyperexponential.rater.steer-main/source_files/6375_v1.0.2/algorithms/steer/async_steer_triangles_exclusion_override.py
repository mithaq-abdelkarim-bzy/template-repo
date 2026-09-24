import hx
import pandas as pd
import numpy as np
import math as math
import datetime
import algorithms.rate_constants as const
from   algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, write_pd_to_hxd_no_overrides
from   dateutil.relativedelta    import relativedelta
import algorithms.rate_constants as const


# #######################################################################################################
# ### BEGIN - build exclusions triangle of the correct size/shape                                     ###
# #######################################################################################################

# def steer_tri_exclusions_setup(hxd,progress):

#     cds       = hxd.cds
#     tri       = hxd.cds.steer.experience_rating.layers.fgu.triangle_projection
#     # tri = getattr(hxd.cds.steer.experience_rating.layers, layer_name).triangle_projection
    
#     tri_1a       = tri.tri_1a_raw_data_incurred
#     tri_1b       = tri.tri_1b_raw_data_paid
    
#     tri_1_basis = tri.tri_1_basis

#     tri_2     = tri.tri_2_manual_input
#     tri_excl  = tri.tri_3a_exclusions

#     # where override triangle has been selected draw parameter from the override triangle
#     if tri.override_triangle:

#         if ( (tri_2.origin_period_count==0) or (tri_2.dev_period_increment==0) or (tri_2.dev_period_count==0) ) :# or (tri_2.first_dev_period):
#             tri.tri_exclusions_setup_task_status = "Please complete override triangle to proceed." 
#             return

#         tri_excl.origin_period_count   = tri_2.origin_period_count      -1   # netting of 1 for exclusions triangle
#         tri_excl.dev_period_increment  = tri_2.dev_period_increment
#         tri_excl.dev_period_count      = tri_2.dev_period_count         -1   # netting of 1 for exclusions triangle
#         tri_excl.first_dev_period      = tri_2.first_dev_period  
        
#         for k in range(tri_excl.origin_period_count):
#             tri_excl.origin_periods[k] = tri_2.origin_periods[k]
        
#         tri.tri_exclusions_setup_task_status = "Exclusion triangle built for override triangle. Enter a 1 in the relevant cell below to exclude." 
    
#     # where override triangle has NOT been selected draw parameter from the default BI triangle
#     else:

#         processed_claims = hxd.cds.steer.experience_rating.processed_claims

#         if len(processed_claims)==0:
#             tri.tri_exclusions_setup_task_status = "Please load some data to proceed."

#             return
#         processed_claims_df = pd_df_from_hx_list(processed_claims)

#         tri_1_ab = tri_1a  if tri_1_basis == "Incurred" else tri_1b

#         tri_excl.origin_period_count   = tri_1_ab.origin_period_count      -1   # netting of 1 for exclusions triangle
#         tri_excl.dev_period_increment  = tri_1_ab.dev_period_increment
#         tri_excl.dev_period_count      = tri_1_ab.dev_period_count         -1   # netting of 1 for exclusions triangle
#         tri_excl.first_dev_period      = tri_1_ab.first_dev_period  
        
#         for k in range(tri_excl.origin_period_count):
#             tri_excl.origin_periods[k] = tri_1_ab.origin_periods[k] 

#         hxd.cds.steer.experience_rating.layers.fgu.triangle_projection.tri_exclusions_setup_task_status = "Exclusion triangle built for Raw Data, Enter a 1 in the relevant cell below to exclude."

#     pass

# #######################################################################################################
# ### END - build exclusions triangle of the correct size/shape                                       ###
# #######################################################################################################


#######################################################################################################
### BEGIN - build exclusions triangle of the correct size/shape                                     ###
#######################################################################################################

def steer_tri_exclusions_setup(hxd,progress):
    
    cds = hxd.cds

    layer_list = ["fgu"]
    for layer_index in range(len(cds.layers)):
        layer_name = f"layer_{layer_index+1:02d}"
        layer_list.append(layer_name)
    
    for layer_name in layer_list:

        tri       = getattr(hxd.cds.steer.experience_rating.layers,layer_name).triangle_projection
        
        tri_1a       = tri.tri_1a_raw_data_incurred
        tri_1b       = tri.tri_1b_raw_data_paid
        
        tri_1_basis = tri.tri_1_basis

        tri_2     = tri.tri_2_manual_input
        tri_excl  = tri.tri_3a_exclusions

        # where override triangle has been selected draw parameter from the override triangle
        if tri.override_triangle:

            if ( (tri_2.origin_period_count==0) or (tri_2.dev_period_increment==0) or (tri_2.dev_period_count==0) ) :# or (tri_2.first_dev_period):
                tri.tri_exclusions_setup_task_status = "Please complete override triangle to proceed." 
                return

            tri_excl.origin_period_count   = tri_2.origin_period_count      -1   # netting of 1 for exclusions triangle
            tri_excl.dev_period_increment  = tri_2.dev_period_increment
            tri_excl.dev_period_count      = tri_2.dev_period_count         -1   # netting of 1 for exclusions triangle
            tri_excl.first_dev_period      = tri_2.first_dev_period  
            
            for k in range(tri_excl.origin_period_count):
                tri_excl.origin_periods[k] = tri_2.origin_periods[k]
            
            tri.tri_exclusions_setup_task_status = "Exclusion triangle built for override triangle. Enter a 1 in the relevant cell below to exclude." 
        
        # where override triangle has NOT been selected draw parameter from the default BI triangle
        else:

            processed_claims = hxd.cds.steer.experience_rating.processed_claims

            if len(processed_claims)==0:
                tri.tri_exclusions_setup_task_status = "Please load some data to proceed."

                return
            processed_claims_df = pd_df_from_hx_list(processed_claims)

            tri_1_ab = tri_1a  if tri_1_basis == "Incurred" else tri_1b

            tri_excl.origin_period_count   = tri_1_ab.origin_period_count      -1   # netting of 1 for exclusions triangle
            tri_excl.dev_period_increment  = tri_1_ab.dev_period_increment
            tri_excl.dev_period_count      = tri_1_ab.dev_period_count         -1   # netting of 1 for exclusions triangle
            tri_excl.first_dev_period      = tri_1_ab.first_dev_period  
            
            for k in range(tri_excl.origin_period_count):
                tri_excl.origin_periods[k] = tri_1_ab.origin_periods[k] 

            hxd.cds.steer.experience_rating.layers.fgu.triangle_projection.tri_exclusions_setup_task_status = "Exclusion triangle built for Raw Data, Enter a 1 in the relevant cell below to exclude."

        pass

#######################################################################################################
### END - build exclusions triangle of the correct size/shape                                       ###
#######################################################################################################




#######################################################################################################
### BEGIN - build override triangle of the correct size/shape                                     ###
#######################################################################################################

def steer_tri_override_setup(hxd,progress):

    # setting up initial values
    tri_ovd             =  hxd.cds.steer.experience_rating.layers.fgu.triangle_projection.tri_2_manual_input
    tri_date            = hxd.cds.steer.experience_rating.layers.fgu.triangle_projection.override_triangle_date
    tri_years           = min(const.experience_rating_max_years, max(1, hxd.cds.steer.experience_rating.layers.fgu.triangle_projection.override_triangle_years)) # ensuring the value lies between 1 and Max Experience years
    tri_date_available  = (tri_date is None) == False
    incept_date         = hxd.hx_core.inception_date

    # assigning a triangle date where none is given
    if tri_date_available == False:         tri_date   = incept_date

    # calculating necessary day/mth/yr
    incept_day  = incept_date.day
    incept_month  = incept_date.month
    incept_yr   = incept_date.year
    tri_yr      = tri_date.year

    as_at_day  = tri_date.day
    as_at_month  = tri_date.month
    
    # determining inception date prior to triangle date
    if datetime.date(tri_yr, incept_month, incept_day) >= tri_date:  
        last_yr = tri_yr - 1
    else: 
        last_yr = tri_yr
    
    first_yr          = int(last_yr  - tri_years  + 1)
    first_origin_date = datetime.date(first_yr,  as_at_month, as_at_day)
    last_origin_date  = datetime.date(last_yr,   as_at_month, as_at_day)

    # assigning values to the override triangle node
    tri_ovd.origin_period_count      = tri_years
    tri_ovd.dev_period_count         = tri_years
    # tri_ovd.dev_period_increment     = 1   
    tri_ovd.dev_period_increment     = 12                                                           # 1 year always
    # tri_ovd.first_dev_period         = (12  if relativedelta(tri_date, last_origin_date).years == 1 
                                            # else relativedelta(tri_date, last_origin_date).months   )   # determining number of year between prior incept_date and triangle date
    tri_ovd.first_dev_period         = 12
    
    # assigning origin period labels
    for k in range(tri_ovd.origin_period_count):
        tri_ovd.origin_periods[k]     = first_origin_date + relativedelta(years=k)

    # assign status
    hxd.cds.steer.experience_rating.layers.fgu.triangle_projection.async_override_triangle_status = "Triangle built"
    if tri_date_available == False: 
        hxd.cds.steer.experience_rating.layers.fgu.triangle_projection.async_override_triangle_status += ", date assumed as inception"
    if tri_years != hxd.cds.steer.experience_rating.layers.fgu.triangle_projection.override_triangle_years:
        hxd.cds.steer.experience_rating.layers.fgu.triangle_projection.async_override_triangle_status += f", number of years constrained to be between 1 & {const.experience_rating_max_years}"

    hxd.cds.steer.experience_rating.layers.fgu.triangle_projection.override_triangle_date_used = tri_date
    
    # set Count Override Triangle Date and number of years the same as the Claims Override Triangle
    hxd.cds.steer.experience_rating.layers.fgu.claim_count.override_triangle_date = hxd.cds.steer.experience_rating.layers.fgu.triangle_projection.override_triangle_date
    hxd.cds.steer.experience_rating.layers.fgu.claim_count.override_triangle_years = hxd.cds.steer.experience_rating.layers.fgu.triangle_projection.override_triangle_years 
    
    pass

#######################################################################################################
### END - build override triangle of the correct size/shape                                       ###
#######################################################################################################


#######################################################################################################
### BEGIN - build exclusions triangle count of the correct size/shape                                     ###
#######################################################################################################

def steer_tri_count_exclusions_setup(hxd,progress):

    cds       = hxd.cds
    tri       = cds.steer.experience_rating.layers.fgu.claim_count
    # tri_1       = tri.tri_1_raw_data

    tri_1_basis = tri.tri_1_basis
    tri_1a       = tri.tri_1a_raw_data_incurred
    tri_1b       = tri.tri_1b_raw_data_paid

    
    tri_2     = tri.tri_2_manual_input
    tri_excl  = tri.tri_3a_exclusions

    # where override triangle has been selected draw parameter from the override triangle
    if tri.override_triangle:

        if ( (tri_2.origin_period_count==0) or (tri_2.dev_period_increment==0) or (tri_2.dev_period_count==0) ) :# or (tri_2.first_dev_period):
            tri.tri_exclusions_setup_task_status = "Please complete override triangle to proceed." 
            return

        tri_excl.origin_period_count   = tri_2.origin_period_count      -1   # netting of 1 for exclusions triangle
        tri_excl.dev_period_increment  = tri_2.dev_period_increment
        tri_excl.dev_period_count      = tri_2.dev_period_count         -1   # netting of 1 for exclusions triangle
        tri_excl.first_dev_period      = tri_2.first_dev_period  
        
        for k in range(tri_excl.origin_period_count):
            tri_excl.origin_periods[k] = tri_2.origin_periods[k]
        
        tri.tri_exclusions_setup_task_status = "Exclusion triangle built for override triangle. Enter a 1 in the relevant cell below to exclude." 
    
    # where override triangle has NOT been selected draw parameter from the default BI triangle
    else:

        processed_claims = hxd.cds.steer.experience_rating.processed_claims

        if len(processed_claims)==0:
            tri.tri_exclusions_setup_task_status = "Please load some data to proceed."

            return
        processed_claims_df = pd_df_from_hx_list(processed_claims)

        tri_1_ab = tri_1a  if tri_1_basis == "Incurred" else tri_1b

        tri_excl.origin_period_count   = tri_1_ab.origin_period_count      -1   # netting of 1 for exclusions triangle
        tri_excl.dev_period_increment  = tri_1_ab.dev_period_increment
        tri_excl.dev_period_count      = tri_1_ab.dev_period_count         -1   # netting of 1 for exclusions triangle
        tri_excl.first_dev_period      = tri_1_ab.first_dev_period  
        
        for k in range(tri_excl.origin_period_count):
            tri_excl.origin_periods[k] = tri_1_ab.origin_periods[k] 

        hxd.cds.steer.experience_rating.layers.fgu.claim_count.tri_exclusions_setup_task_status = "Exclusion triangle built for Raw Data, Enter a 1 in the relevant cell below to exclude."

    pass

#######################################################################################################
### END - build exclusions triangle of the correct size/shape                                       ###
#######################################################################################################



#######################################################################################################
### BEGIN - build override triangle Count of the correct size/shape                                     ###
#######################################################################################################

def steer_tri_count_override_setup(hxd,progress):

    # setting up initial values
    tri_ovd             = hxd.cds.steer.experience_rating.layers.fgu.claim_count.tri_2_manual_input
    tri_date            = hxd.cds.steer.experience_rating.layers.fgu.claim_count.override_triangle_date
    tri_years           = min(const.experience_rating_max_years, max(1, hxd.cds.steer.experience_rating.layers.fgu.claim_count.override_triangle_years)) # ensuring the value lies between 1 and Max Experience years
    tri_date_available  = (tri_date is None) == False
    incept_date         = hxd.hx_core.inception_date

    # assigning a triangle date where none is given
    if tri_date_available == False:         tri_date   = incept_date

    # calculating necessary day/mth/yr
    incept_day  = incept_date.day
    incept_month  = incept_date.month
    incept_yr   = incept_date.year
    tri_yr      = tri_date.year

    as_at_day  = tri_date.day
    as_at_month  = tri_date.month
    
    # determining inception date prior to triangle date
    if datetime.date(tri_yr, incept_month, incept_day) >= tri_date:  
        last_yr = tri_yr - 1
    else: 
        last_yr = tri_yr
    
    first_yr          = int(last_yr  - tri_years  + 1)
    first_origin_date = datetime.date(first_yr,  as_at_month, as_at_day)
    last_origin_date  = datetime.date(last_yr,   as_at_month, as_at_day)

    # assigning values to the override triangle node
    tri_ovd.origin_period_count      = tri_years
    tri_ovd.dev_period_count         = tri_years
    # tri_ovd.dev_period_increment     = 1   
    tri_ovd.dev_period_increment     = 12                                                           # 1 year always
    # tri_ovd.first_dev_period         = (12  if relativedelta(tri_date, last_origin_date).years == 1 
                                            # else relativedelta(tri_date, last_origin_date).months   )   # determining number of year between prior incept_date and triangle date
    tri_ovd.first_dev_period         = 12
    
    # assigning origin period labels
    for k in range(tri_ovd.origin_period_count):
        tri_ovd.origin_periods[k]     = first_origin_date + relativedelta(years=k)

    # assign status
    hxd.cds.steer.experience_rating.layers.fgu.claim_count.async_override_triangle_status = "Triangle built"
    if tri_date_available == False: 
        hxd.cds.steer.experience_rating.layers.fgu.claim_count.async_override_triangle_status += ", date assumed as inception"
    if tri_years != hxd.cds.steer.experience_rating.layers.fgu.claim_count.override_triangle_years:
        hxd.cds.steer.experience_rating.layers.fgu.claim_count.async_override_triangle_status += f", number of years constrained to be between 1 & {const.experience_rating_max_years}"

    hxd.cds.steer.experience_rating.layers.fgu.claim_count.override_triangle_date_used = tri_date
    

    pass

#######################################################################################################
### END - build override triangle of the correct size/shape                                       ###
#######################################################################################################
