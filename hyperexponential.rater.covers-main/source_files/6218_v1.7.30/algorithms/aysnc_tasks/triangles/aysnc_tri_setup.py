################################## TO DO ##############################################################
### 
#######################################################################################################

import hx
import pandas as pd
import numpy as np
import math as math
import datetime
import algorithms.rate_constants as const
from   algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, write_pd_to_hxd_no_overrides
from   dateutil.relativedelta    import relativedelta

#######################################################################################################
### BEGIN - build exclusions triangle of the correct size/shape                                     ###
#######################################################################################################

def tri_exclusions_setup(hxd,progress):

    cds       = hxd.cds
    tri       = hxd.cds.triangle_projection
    tri_2     = hxd.cds.triangle_projection.tri_2_manual_input
    tri_excl  = hxd.cds.triangle_projection.tri_3a_exclusions

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
        movement_df = pd_df_from_hx_list(cds.bi_data.claims_movements)
        if movement_df.empty or (movement_df.shape[0]==1 and movement_df.date_extracted.iat[0] is None):
            tri.tri_exclusions_setup_task_status = "Please load some data to proceed." 
            return

        last_origin_year            = int(np.max(movement_df.yoa))
        first_origin_year           = int(np.min(movement_df.yoa))
        first_origin_month          = hxd.hx_core.inception_date.month
        first_origin_day            = hxd.hx_core.inception_date.day
        first_origin_date           = datetime.date(first_origin_year,first_origin_month,first_origin_day)

        incept_date                 = hxd.hx_core.inception_date                        # deliberately not netting off the day here (unlike the associated sql code so when it bites below we get 12mth returned not 11)
        extracted_date              = cds.risk_info.bic_data_asat
        last_mvmt_date              = min(incept_date,extracted_date)
        delta_date                  = relativedelta(last_mvmt_date, first_origin_date)
        mths_total                  = delta_date.years * 12 + delta_date.months
        mths_first_dev_period       = mths_total % 12                                   # modulo or remainder
        mths_first_dev_period      += 12 if ( (delta_date.months == 0) & (delta_date.days == 0) ) else 0

        # triangle > single value settings 
        tri_excl.origin_period_count     = last_origin_year-first_origin_year +1   -1   # netting of 1 for exclusions triangle
        tri_excl.dev_period_increment    = 12
        tri_excl.dev_period_count        = mths_total // 12  + ( 0  if ( (delta_date.months == 0) & (delta_date.days == 0) ) else 1 ) -1   # netting of 1 for exclusions triangle
        tri_excl.first_dev_period        = mths_first_dev_period
    
        # triangle > list array for origin periods > Used below as couldnt pass a list:  tri_1.origin_periods = [first_origin_date + relativedelta(years=k) for k in range(last_origin_year-first_origin_year+1)]
        for k in range(tri_excl.origin_period_count):
            tri_excl.origin_periods[k] = first_origin_date + relativedelta(years=k) 

        hxd.cds.triangle_projection.tri_exclusions_setup_task_status = "Exclusion triangle built for Default BI triangle, Enter a 1 in the relevant cell below to exclude."

    pass

#######################################################################################################
### END - build exclusions triangle of the correct size/shape                                       ###
#######################################################################################################




#######################################################################################################
### BEGIN - build override triangle of the correct size/shape                                     ###
#######################################################################################################

def tri_override_setup(hxd,progress):

    # setting up initial values
    tri_ovd             = hxd.cds.triangle_projection.tri_2_manual_input
    tri_date            = hxd.cds.triangle_projection.override_triangle_date
    tri_years           = min(15, max(1, hxd.cds.triangle_projection.override_triangle_years)) #ensuring the value lies between 1 and 15
    tri_date_available  = (tri_date is None) == False
    incept_date         = hxd.hx_core.inception_date

    # assigning a triangle date where none is given
    if tri_date_available == False:         tri_date   = incept_date

    # calculating necessary day/mth/yr
    incept_day  = incept_date.day
    incept_mth  = incept_date.month
    incept_yr   = incept_date.year
    tri_yr      = tri_date.year
    
    # determining inception date prior to triangle date
    if datetime.date(tri_yr, incept_mth, incept_day) >= tri_date:  
        last_yr = tri_yr - 1
    else: 
        last_yr = tri_yr
    
    first_yr          = int(last_yr  - tri_years  + 1)
    first_origin_date = datetime.date(first_yr,  incept_mth, incept_day)
    last_origin_date  = datetime.date(last_yr,   incept_mth, incept_day)

    # assigning values to the override triangle node
    tri_ovd.origin_period_count      = tri_years
    tri_ovd.dev_period_count         = tri_years
    tri_ovd.dev_period_increment     = 12                                                               # 12 months always
    tri_ovd.first_dev_period         = (12  if relativedelta(tri_date, last_origin_date).years == 1 
                                            else relativedelta(tri_date, last_origin_date).months   )   # determining number of months between prior incept_date and triangle date

    # assigning origin period labels
    for k in range(tri_ovd.origin_period_count):
        tri_ovd.origin_periods[k]     = first_origin_date + relativedelta(years=k)

    # assign status
    hxd.cds.triangle_projection.async_override_triangle_status = "Triangle built"
    if tri_date_available == False: 
        hxd.cds.triangle_projection.async_override_triangle_status += ", date assumed as inception"
    if tri_years != hxd.cds.triangle_projection.override_triangle_years:
        hxd.cds.triangle_projection.async_override_triangle_status += ", number of years constrained to be between 1 & 15"

    hxd.cds.triangle_projection.override_triangle_date_used = tri_date
    pass

#######################################################################################################
### END - build override triangle of the correct size/shape                                       ###
#######################################################################################################