##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################

##############################################################################################################################


import hx
import pandas as pd
import numpy as np
import math as math
import datetime
#import itertools
import algorithms.rate_constants as const
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, write_pd_to_hxd_no_overrides
#from operator import itemgetter
from dateutil.relativedelta import relativedelta
from scipy.interpolate import interp1d

from algorithms.timer import timer


def rate_triangle_projection(hxd):
    cds   = hxd.cds
    tri   = hxd.cds.triangle_projection
    tri_2 = tri.tri_2_manual_input

    movement_df = pd_df_from_hx_list(cds.bi_data.claims_movements)

    override_triangle_active = tri.override_triangle
    override_triangle_valid  = (    ((tri_2.origin_period_count or 0)                            == min(15, max(1,tri.override_triangle_years)))
                                and ((tri.override_triangle_date or hxd.hx_core.inception_date)  == tri.override_triangle_date_used))

    if (override_triangle_valid == False): tri.assign_override_triangle_status = "Please press Button (Setup Override Triangle) to activate"


    bi_triangle_status      = (     movement_df.empty 
                                or (movement_df.shape[0]==1 and movement_df.date_extracted.iat[0] is None)) == False

    tri_3_status            = False
    leap_day                = True if (hxd.hx_core.inception_date.month == 2 and hxd.hx_core.inception_date.day == 29) else False
    short_or_long_tailed    = cds.risk_info.st_or_lt

    #######################################################################################
    ### 1) BUILDING TRIANGLE WHERE we have a complete triangle either from bi
    #######################################################################################
    if (bi_triangle_status):

        ############################################
        ### 1a) BEGIN Build Tri_1 (Beazley Intelligence)
        ### triangles inputs are described here: https://www.beazley.hxrenew.com/customer-service/platform/developer/building-your-model/define-your-data/example-data
        ############################################

        # initial settings
        last_origin_year            = int(np.max(movement_df.yoa))
        first_origin_year           = int(np.min(movement_df.yoa))
        first_origin_month          = hxd.hx_core.inception_date.month
        first_origin_day            = hxd.hx_core.inception_date.day - (1 if leap_day else 0)
        first_origin_date           = datetime.date(first_origin_year,first_origin_month,first_origin_day)

        incept_date                 = hxd.hx_core.inception_date                        # deliberately not netting off the day here (unlike the associated sql code so when it bites below we get 12mth returned not 11)
        extracted_date              = cds.risk_info.bic_data_asat
        last_mvmt_date              = min(incept_date,extracted_date)
        delta_date                  = relativedelta(last_mvmt_date, first_origin_date)
        mths_total                  = delta_date.years * 12 + delta_date.months
        mths_first_dev_period       = mths_total % 12                                   # modulo or remainder
        mths_first_dev_period      += 12 if ( (delta_date.months == 0) & (delta_date.days == 0) ) else 0

        # triangle > single value settings 
        tri_1 = tri.tri_1_loaded_from_bi
        tri_1.origin_period_count     = last_origin_year-first_origin_year+1
        tri_1.dev_period_increment    = 12
        tri_1.dev_period_count        = int(np.max(movement_df.mvmt_yr)) #mths_total // 12  + ( 0  if ( (delta_date.months == 0) & (delta_date.days == 0) ) else 1 )
        tri_1.first_dev_period        = mths_first_dev_period
    
        # triangle > list array for origin periods > Used below as couldnt pass a list:  tri_1.origin_periods = [first_origin_date + relativedelta(years=k) for k in range(last_origin_year-first_origin_year+1)]
        for k in range(tri_1.origin_period_count):
            tri_1.origin_periods[k] = first_origin_date + relativedelta(years=k) 

        movement_attritional_df = movement_df[(movement_df.loss_category == "ATT") ]
    
        # load matrix of triangle data either cumulative or incremental - favoured incremental since no guarantee of a value everywhere - error trap?
        for row in movement_attritional_df.index:
            origin_period   = datetime.date(int(movement_attritional_df.yoa[row]),  first_origin_month,  first_origin_day)
            dev_period      = ( movement_attritional_df.mvmt_yr[row] -1 ) *12  + mths_first_dev_period                      #first year is 1 so net of 1 year convert to months and then add back on the starting number of months
            value           = movement_attritional_df.incurredmvmt_100_sett_fx[row]
            if value is not None and not math.isnan(value):
                # print(str(origin_period) + ":" + str(dev_period)+ " val:" + str(value))
                start_value = tri_1.incremental_data[ tri_1.origin_periods.index(origin_period), tri_1.dev_periods.index(dev_period)] or 0
                tri_1.incremental_data[ tri_1.origin_periods.index(origin_period), tri_1.dev_periods.index(dev_period)] = start_value + value



    ###################################
    ### 1b) BEGIN Build Tri_3 (selected)
    ###################################




    if (bi_triangle_status or      (override_triangle_active and override_triangle_valid) ):

        tri_3   = tri.tri_3_selected
        tri_exc = tri.tri_3a_exclusions
        
        ### Build Tri_3 (selected): if triangle override has been selected set tri_3 equal to override otherwise use BI
        if (override_triangle_active and override_triangle_valid):
   
            #############################################
            ## 1c) BEGIN Build Tri_3 (selected) from Override
            #############################################
            # path taken if overridden & valid
            
            # assigning individual values
            tri_3.origin_period_count   = tri_2.origin_period_count
            tri_3.dev_period_increment  = tri_2.dev_period_increment
            tri_3.dev_period_count      = tri_2.dev_period_count
            tri_3.first_dev_period      = tri_2.first_dev_period  

            # JB CHECK HANDLING OF NULLS IN BELOW 2 SECTIONS
            # assigning origin_periods array ... smarter way to assign to list & matrix but they dont feel like they are behaving as lists - cant map to df etc?
            for k in range(tri_2.origin_period_count):
                tri_3.origin_periods[k] = tri_2.origin_periods[k]

            # assigning incremental_data matrix ... smarter way to assign to list & matrix but they dont feel like they are behaving as lists - cant map to df etc?
            # AT catch for renewal (hx_core inception year + 1 on renewal causing list index out of range error)
            try:
                for k in range(tri_2.origin_period_count):
                    for j in range(tri_2.dev_period_count):
                        tri_3.incremental_data[k,j]  = tri_2.incremental_data[k,j] 
                        # = value if value is not None and not math.isnan(value) else None 
            except:
                for k in range(tri_2.origin_period_count):
                    for j in range(tri_2.dev_period_count - 1):
                        tri_3.incremental_data[k,j]  = tri_2.incremental_data[k,j] 
                        # = value if value is not None and not math.isnan(value) else None 
            tri.assign_override_triangle_status = "Override Triangle Active" 


        else:
            #############################################
            ## 1d) BEGIN Build Tri_3 (selected) from BI
            #############################################
            # assigning individual values
            tri_3.origin_period_count   = tri_1.origin_period_count
            tri_3.dev_period_increment  = tri_1.dev_period_increment
            tri_3.dev_period_count      = tri_1.dev_period_count
            tri_3.first_dev_period      = tri_1.first_dev_period  

            # JB CHECK HANDLING OF NULLS IN BELOW 2 SECTIONS
            # assigning origin_periods array ... smarter way to assign to list & matrix but they dont feel like they are behaving as lists - cant map to df etc?
            for k in range(tri_1.origin_period_count):
                tri_3.origin_periods[k] = tri_1.origin_periods[k]

            # assigning incremental_data matrix ... smarter way to assign to list & matrix but they dont feel like they are behaving as lists - cant map to df etc?
            # AT catch for renewal (hx_core inception year + 1 on renewal causing list index out of range error)
            try:
                for k in range(tri_1.origin_period_count):
                    for j in range(tri_1.dev_period_count):
                        tri_3.incremental_data[k,j]  = tri_1.incremental_data[k,j] 
            except:
                for k in range(tri_1.origin_period_count):
                    for j in range(tri_1.dev_period_count - 1):
                      tri_3.incremental_data[k,j]  = tri_1.incremental_data[k,j]


        ## set averaging option
        tri_3.selected_average_option = "vw_7" if short_or_long_tailed == "ST" else "vw_all" 


        #############################################
        ## 1e) assign exclusions triangle
        #############################################

        # AT catch for renewal (hx_core inception year + 1 on renewal causing list index out of range error)
        try:
            if (tri_3.origin_period_count == tri_exc.origin_period_count +1)   &   (tri_3.dev_period_count == tri_exc.dev_period_count +1):
                for k in range(tri_exc.origin_period_count):
                    for j in range(tri_exc.dev_period_count):
                        if tri_exc.incremental_data[k,j] == 1:
                            tri_3.idf_table_adjustments.exclusions.exclude(k, j)
                        else:
                            tri_3.idf_table_adjustments.exclusions.include(k, j)
                tri.tri_exclusions_dimensions_status = "Exclusions Active"
            else:
                tri.tri_exclusions_dimensions_status = "Exclusions Inactive - dimensions incorrect. Press Setup Exclusions Triangle to activate"
        except: 
            if (tri_3.origin_period_count == tri_exc.origin_period_count +1)   &   (tri_3.dev_period_count == tri_exc.dev_period_count +1):
                for k in range(tri_exc.origin_period_count):
                    for j in range(tri_exc.dev_period_count - 1):
                        if tri_exc.incremental_data[k,j] == 1:
                            tri_3.idf_table_adjustments.exclusions.exclude(k, j)
                        else:
                            tri_3.idf_table_adjustments.exclusions.include(k, j)
                tri.tri_exclusions_dimensions_status = "Exclusions Active"
            else:
                tri.tri_exclusions_dimensions_status = "Exclusions Inactive - dimensions incorrect. Press Setup Exclusions Triangle to activate"


        #############################################
        ## 1f) determine tri_3_selected status - nb cant project a triangle with only one development period
        #############################################
        tri_3_status = ( (tri_3.origin_period_count <= 1) or (tri_3.dev_period_increment==0) or (tri_3.dev_period_count <= 1) )  == False






    #######################################################################################
    ### 2) Triangles Available - BUILDING IN TAIL FACTORS AND BENCHMARKS
    #######################################################################################

    if (bi_triangle_status or (override_triangle_active and override_triangle_valid))   and tri_3_status:

        ###############################################################################
        ### 2a) Triangles Available - BEGIN TAIL FACTOR - Beazley specific approach
        ###############################################################################

        ## set tail factor
        # last_dev_period = last development period in selected triangle
        # noting list starts at zero we need to deduct 1, noting we are looking at ldfs there will be 1 less than the incurred triangle so we want last_dev_period-2
        last_dev_period = tri_3.dev_period_count
        last_dev_factor = max(1, tri_3.idfs_calculated[last_dev_period-2])

        # get tail factor table and filter
        tf_df = hx.params.tb_rule_tail_factor
        tf_rows_df = tf_df[ (tf_df.basis=="cumulative")  &  (tf_df.tail_code == short_or_long_tailed)  &  (tf_df.tail_df <= last_dev_factor) ].sort_values(by=['tail_df'])

        # return the last factor where it exists
        tri_3.tail_factor = 1 if tf_rows_df.empty else tf_rows_df.incurred_dev_factor.iat[-1]



        #############################################################################
        ## 2b) Triangles Available - BEGIN BENCHMARK OVERRIDE - key values
        #############################################################################

        # Set the benchmark override name
        tri.benchmark_name.default      = cds.standard_fields.benchmark_class
        tri.benchmark_name.selected     = tri.benchmark_name.override or tri.benchmark_name.default


        # Set the benchmark override weight     
        num_years_data                  = tri_3.origin_period_count                                                             # JB - could consider if some years are nil, but old algorithm didnt
        num_link_ratio_x_tail           = tri_3.origin_period_count -1 
        average_incurred                = np.average([i for i in tri_3.most_recent_cumulative_values if i != None])             # needed to condition on nones otherwise average dont work
        

        # get weight to experience
        weight_df                       = hx.params.tb_rule_pattern_weight
        weight_conditions               = (weight_df.num_yr_data<=num_years_data)  &  (weight_df.tail_code == short_or_long_tailed)  &  (weight_df.average_total_claims <= average_incurred)
        weight_rows_df                  = weight_df[ weight_conditions ].sort_values(by=['num_yr_data','average_total_claims'])
        tri.experience_weight.default   = 0 if weight_rows_df.empty else weight_rows_df.wgt_experience.iat[-1] 
        tri.experience_weight.selected  = tri.experience_weight.default if ( pd.isna(tri.experience_weight.override)
                                                                             or tri.experience_weight.override <0
                                                                             or tri.experience_weight.override >1  ) else  tri.experience_weight.override



        #############################################################################
        ### 2c) Triangles Available - BEGIN EXPERIENCE OVERRIDES - IDF & Tail
        #############################################################################
        # # Set the experience override incurred development factors table
        custom_idf_df                     = pd_df_from_hx_list( tri.incremental_dev_factor )
        custom_idf_df.development_mth     = [(tri_3.first_dev_period        +  12*x ) for x in range(const.default_num_rows)]                               #converting monthly       
        custom_idf_df.development_qtr     = [(tri_3.first_dev_period / 3    +   4*x ) for x in range(const.default_num_rows)]                               #converting to quarterly
        custom_idf_df.experience_default  = [tri_3.idfs_calculated[x] if x< len(tri_3.idfs_calculated) else None for x in range(const.default_num_rows)]

        # removing negative and nils from override for analysis purposes - note this field is not written back to hxd
        custom_idf_df.experience_override = np.where(custom_idf_df.experience_override is None
                                                        , np.nan
                                                        , np.where(custom_idf_df.experience_override <=0
                                                                    , np.nan
                                                                    , custom_idf_df.experience_override))
        custom_idf_df.experience_selected = np.where(custom_idf_df.experience_override.isnull()
                                                        , custom_idf_df.experience_default
                                                        , np.where(custom_idf_df.experience_override <=0
                                                                    , custom_idf_df.experience_default
                                                                    , custom_idf_df.experience_override))
        custom_idf_df.show_idf_row        = np.where(custom_idf_df.experience_default.isnull(),False,True)


        # Set the experience override tail factors
        tri.tail_factor.show_idf_row        = True
        tri.tail_factor.experience_default  = tri_3.tail_factor
        tri.tail_factor.experience_selected = tri.tail_factor.experience_default if ( pd.isna(tri.tail_factor.experience_override)
                                                                                            or tri.tail_factor.experience_override <= 0) else  tri.tail_factor.experience_override
        






    #######################################################################################
    ### 3) No Triangles - BUILDING IN TAIL FACTORS AND BENCHMARKS
    #######################################################################################

    else:

        #######################################################################################
        ### 3a) No Triangles - settings
        #######################################################################################
        

        first_origin_year           = hxd.hx_core.inception_date.year - 1 ### DIFFERENCE TO STAGE 2 - assumed 1 year prior
        first_origin_month          = hxd.hx_core.inception_date.month
        first_origin_day            = hxd.hx_core.inception_date.day - (1 if leap_day else 0)
        first_origin_date           = datetime.date(first_origin_year,first_origin_month,first_origin_day)

        incept_date                 = hxd.hx_core.inception_date                        # deliberately not netting off the day here (unlike the associated sql code so when it bites below we get 12mth returned not 11)
        extracted_date              = cds.risk_info.final_data_asat
        last_mvmt_date              = min(incept_date,extracted_date)
        delta_date                  = relativedelta(last_mvmt_date, first_origin_date)
        mths_total                  = delta_date.years * 12 + delta_date.months
        mths_first_dev_period       = mths_total % 12                                   # modulo or remainder
        mths_first_dev_period      += 12 if ( (delta_date.months == 0) & (delta_date.days == 0) ) else 0




        ###################################
        ## 3b) BEGIN BENCHMARK OVERRIDE - key values
        ###################################

        # Set the benchmark override name
        tri.benchmark_name.default      = cds.standard_fields.benchmark_class
        tri.benchmark_name.selected     = tri.benchmark_name.override or tri.benchmark_name.default

        # get weight to experience
        tri.experience_weight.default   = 0     ### DIFFERENCE TO STAGE 2 - defaulted to zero
        tri.experience_weight.selected  = tri.experience_weight.default if pd.isna(tri.experience_weight.override) else  tri.experience_weight.override


        ###################################
        ### 3c) BEGIN EXPERIENCE OVERRIDES - IDF & Tail
        ###################################
        # # Set the experience override incurred development factors table
        custom_idf_df                     = pd_df_from_hx_list( tri.incremental_dev_factor )
        custom_idf_df.development_mth     = [(mths_first_dev_period       +  12*x ) for x in range(const.default_num_rows)]         ### DIFFERENCE TO STAGE 2 -used mths_first_dev_period
        custom_idf_df.development_qtr     = [(mths_first_dev_period / 3    +   4*x ) for x in range(const.default_num_rows)]        ### DIFFERENCE TO STAGE 2 -used mths_first_dev_period
        custom_idf_df.experience_default  = [1 for x in range(const.default_num_rows)]                                              ### DIFFERENCE TO STAGE 2 -used 1

        # removing negative and nils from override for analysis purposes - note this field is not written back to hxd
        custom_idf_df.experience_override = np.where(custom_idf_df.experience_override is None
                                                        , np.nan
                                                        , np.where(custom_idf_df.experience_override <=0
                                                                    , np.nan
                                                                    , custom_idf_df.experience_override))
        custom_idf_df.experience_selected = np.where(custom_idf_df.experience_override.isnull()
                                                        , custom_idf_df.experience_default
                                                        , np.where(custom_idf_df.experience_override <=0
                                                                    , custom_idf_df.experience_default
                                                                    , custom_idf_df.experience_override))
        custom_idf_df.show_idf_row        = np.where(custom_idf_df.experience_default.isnull(),False,True)                          


        # Set the experience override tail factors
        tri.tail_factor.show_idf_row        = True  
        tri.tail_factor.experience_default  = 1                                                                                     ### DIFFERENCE TO STAGE 2 -used 1
        tri.tail_factor.experience_selected = tri.tail_factor.experience_default if ( pd.isna(tri.tail_factor.experience_override)
                                                                                            or tri.tail_factor.experience_override <= 0) else  tri.tail_factor.experience_override





    #########################################################################################################
    ## 4) BEGIN BENCHMARK OVERRIDE - IDF & Tail
    #########################################################################################################

    # build table to fill in the required percentage of ultimate
    bench_all_class_idf_df      = hx.params.tb_afbdevelopmentpatternsoc if tri.benchmark_use_occurrence else hx.params.tb_afbdevelopmentpatterns

    #DEFAULT calculation
    idf_df                      = bench_all_class_idf_df[  (bench_all_class_idf_df['Benchmark Class'] == tri.benchmark_name.default)  ].copy()
    custom_idf_df['dev_qtr_min'] = 1
    custom_idf_df['dev_qtr_max'] = 80 if idf_df.empty else idf_df['qtr'].max() 
    custom_idf_df['development_qtr'] = custom_idf_df[['development_qtr', 'dev_qtr_max']].min(axis = 1)
    custom_idf_df['development_qtr'] = custom_idf_df[['development_qtr', 'dev_qtr_min']].max(axis = 1)

    if idf_df.empty == False:
        f                                                   = interp1d(idf_df.qtr, idf_df.value)
        custom_idf_df['benchmark_default_perc_ult']         = f(custom_idf_df.development_qtr)
        custom_idf_df['benchmark_default_perc_ult_plus_4q'] = f(custom_idf_df.development_qtr+4)
        custom_idf_df.benchmark_default                     = np.where(  (custom_idf_df.development_qtr ==max(custom_idf_df.development_qtr)) 
                                                                        ,1/custom_idf_df.benchmark_default_perc_ult
                                                                        ,custom_idf_df.benchmark_default_perc_ult_plus_4q / custom_idf_df.benchmark_default_perc_ult  ) 
    else:
        custom_idf_df['benchmark_default_perc_ult']         = 1
        custom_idf_df.benchmark_default                     = 1

    #OVERRIDE calculation
    idf_df                       = bench_all_class_idf_df[  (bench_all_class_idf_df['Benchmark Class'] == tri.benchmark_name.override)  ].copy()
    if idf_df.empty == False:
        f                                                    = interp1d(idf_df.qtr, idf_df.value)
        custom_idf_df['benchmark_override_perc_ult']         = f(custom_idf_df.development_qtr)
        custom_idf_df['benchmark_override_perc_ult_plus_4q'] = f(custom_idf_df.development_qtr+4)
        custom_idf_df.benchmark_override                     = np.where(  (custom_idf_df.development_qtr ==max(custom_idf_df.development_qtr)) 
                                                                        ,1/custom_idf_df.benchmark_override_perc_ult
                                                                        ,custom_idf_df.benchmark_override_perc_ult_plus_4q / custom_idf_df.benchmark_override_perc_ult ) 
    else:
        custom_idf_df['benchmark_override_perc_ult']        = 1
        custom_idf_df.benchmark_override                    = 1


    custom_idf_df['benchmark_default']                      = custom_idf_df['benchmark_default'].fillna(1).replace([np.inf, -np.inf], 1)
    custom_idf_df['benchmark_override']                     = custom_idf_df['benchmark_override'].fillna(1).replace([np.inf, -np.inf], 1)

    custom_idf_df.benchmark_selected                         = custom_idf_df.benchmark_override if tri.benchmark_name.override else custom_idf_df.benchmark_default

    # filling in tail factors and clearing them out of the main df
    tri.tail_factor.benchmark_default   = custom_idf_df.benchmark_default.iat[-1]
    tri.tail_factor.benchmark_override  = custom_idf_df.benchmark_override.iat[-1]
    tri.tail_factor.benchmark_selected  = custom_idf_df.benchmark_selected.iat[-1]
    custom_idf_df.benchmark_default.iat[-1]   = 1
    custom_idf_df.benchmark_override.iat[-1]  = 1
    custom_idf_df.benchmark_selected.iat[-1]  = 1




    #########################################################################################################
    ## 5) BEGIN BLENDED CALCULATION
    #########################################################################################################

    empty_override    = (pd.isna(custom_idf_df.experience_override[0])   or pd.isna(tri.tail_factor.experience_override) or
                        pd.isna(custom_idf_df.benchmark_override[0])  or pd.isna(tri.tail_factor.benchmark_override) or
                        pd.isna(tri.experience_weight.override))



    custom_idf_df.blended_default  = (   custom_idf_df.experience_default  *  tri.experience_weight.default 
                                       + custom_idf_df.benchmark_default   *  (1- tri.experience_weight.default))

    if empty_override==False:
        custom_idf_df.blended_override = (   custom_idf_df.experience_override  *  tri.experience_weight.override 
                                           + custom_idf_df.benchmark_override   *  (1- tri.experience_weight.override))

    custom_idf_df.blended_selected = (   custom_idf_df.experience_selected  *  tri.experience_weight.selected 
                                       + custom_idf_df.benchmark_selected   *  (1- tri.experience_weight.selected))



    tri.tail_factor.blended_default  = (   tri.tail_factor.experience_default  *  tri.experience_weight.default 
                                         + tri.tail_factor.benchmark_default   *  (1- tri.experience_weight.default))

    if empty_override==False:
        tri.tail_factor.blended_override = (   tri.tail_factor.experience_override  *  tri.experience_weight.override 
                                             + tri.tail_factor.benchmark_override   *  (1- tri.experience_weight.override))

    tri.tail_factor.blended_selected = (   tri.tail_factor.experience_selected  *  tri.experience_weight.selected 
                                         + tri.tail_factor.benchmark_selected   *  (1- tri.experience_weight.selected))



    
    ### get percents of ultimate 
    custom_idf_df['percents_label']               = custom_idf_df.development_qtr.astype(str)

    custom_idf_df['show_ult_row']                 = custom_idf_df.show_idf_row
    
    if (bi_triangle_status or (override_triangle_active and override_triangle_valid))  and tri_3_status:
        custom_idf_df['show_ult_row'][len(tri_3.idfs_calculated)] = True                    # we want 1 extra row to show on percent ultimate = len(tri_3.idfs_calculated) +1 -1 


    custom_idf_df['experience_default_perc_ult']  = ( 1 / (tri.tail_factor.experience_default or 1) 
                                                        / (custom_idf_df.experience_default[::-1].fillna(1).cumprod()[::-1]))

    custom_idf_df['experience_override_perc_ult'] = ( 1 / (tri.tail_factor.experience_override or 1) 
                                                        / (custom_idf_df.experience_override[::-1].fillna(1).cumprod()[::-1])) 

    custom_idf_df['experience_selected_perc_ult'] = ( 1 / (tri.tail_factor.experience_selected or 1) 
                                                        / (custom_idf_df.experience_selected[::-1].fillna(1).cumprod()[::-1]))


    custom_idf_df.benchmark_default_perc_ult      = custom_idf_df.benchmark_default_perc_ult                                                                    # it already exists
    custom_idf_df['benchmark_override_perc_ult']  = custom_idf_df.benchmark_override_perc_ult if tri.benchmark_name.override else 1                             # it maybe already exists        
    custom_idf_df['benchmark_selected_perc_ult']  = custom_idf_df.benchmark_override_perc_ult if tri.benchmark_name.override else custom_idf_df.benchmark_default_perc_ult

    custom_idf_df['blended_default_perc_ult']  = ( 1 / (tri.tail_factor.blended_default or 1) 
                                                        / (custom_idf_df.blended_default[::-1].fillna(1).cumprod()[::-1]))

    custom_idf_df['blended_override_perc_ult'] = ( 1 / (tri.tail_factor.blended_override or 1) 
                                                        / (custom_idf_df.blended_override[::-1].fillna(1).cumprod()[::-1])) 

    custom_idf_df['blended_selected_perc_ult'] = ( 1 / (tri.tail_factor.blended_selected or 1) 
                                                        / (custom_idf_df.blended_selected[::-1].fillna(1).cumprod()[::-1]))


    ### adding labels
    custom_idf_df.development_label   = (custom_idf_df.development_mth).astype(str) + ":" + (custom_idf_df.development_mth + 12).astype(str)
    custom_idf_df['percents_label']   = custom_idf_df.development_mth.astype(str)

    # Replacing infinite with 1 (if say no data for first few dev periods )
    custom_idf_df.replace([np.inf, -np.inf], 0, inplace=True) 


    #########################################################################################################
    ### 6) Writing DF to HXD
    #########################################################################################################

    #writing incremental factors
    output_columns= [   "show_idf_row"
                        ,"development_qtr"
                        ,"development_mth"
                        ,"development_label"

                        ,"experience_default"
                        #,"experience_override" not needed as input
                        ,"experience_selected"

                        ,"benchmark_default"
                        ,"benchmark_override"
                        ,"benchmark_selected"

                        ,"blended_default"
                        ,"blended_override"
                        ,"blended_selected"
                        ]

    # writign to hxd - enhancement here would be to not fill show_row with 1???  
    write_pd_to_hxd(custom_idf_df.fillna(1), cds.triangle_projection.incremental_dev_factor, output_columns)



    #writing percents of ultimate
    output_columns= [   "show_ult_row"
                        ,"development_qtr"
                        ,"development_mth"                            
                        ,"percents_label"

                        ,"experience_default_perc_ult"
                        ,"experience_override_perc_ult"
                        ,"experience_selected_perc_ult"

                        ,"benchmark_default_perc_ult"
                        ,"benchmark_override_perc_ult"
                        ,"benchmark_selected_perc_ult"

                        ,"blended_default_perc_ult"
                        ,"blended_override_perc_ult"
                        ,"blended_selected_perc_ult"
                        ]

    # writign to hxd - enhancement here would be to not fill show_row with 1???  
    write_pd_to_hxd(custom_idf_df.fillna(1), cds.triangle_projection.percents_ultimate, output_columns)




    #########################################################################################################
    ### 7) Building result triangle - where triangle exists
    #########################################################################################################
    if (bi_triangle_status or (override_triangle_active and override_triangle_valid) ) and tri_3_status:

        tri_4 = tri.tri_4_result
        
        # assigning individual values
        tri_4.origin_period_count     = tri_3.origin_period_count
        tri_4.dev_period_increment    = tri_3.dev_period_increment
        tri_4.dev_period_count        = tri_3.dev_period_count
        tri_4.first_dev_period        = tri_3.first_dev_period  
        tri_4.tail_factor             = tri.tail_factor.blended_selected
        tri_4.selected_average_option = tri_3.selected_average_option


        # JB CHECK HANDLING OF NULLS IN BELOW 2 SECTIONS
        for k in range(tri_3.origin_period_count):
            tri_4.origin_periods[k] = tri_3.origin_periods[k]

        # AT catch for renewal (hx_core inception year + 1 on renewal causing list index out of range error)
        try:
            # assigning incremental_data matrix
            for k in range(tri_3.origin_period_count):
                for j in range(tri_3.dev_period_count):
                    value = tri_3.incremental_data[k,j] 
                    if value is not None and not math.isnan(value):
                        tri_4.incremental_data[k,j]  = tri_3.incremental_data[k,j] 

            # assigning incremental development factors
            for k in range(tri_4.dev_period_count-1):
                tri_4.idf_overrides[k] = tri.incremental_dev_factor[k].blended_selected 
        except:
            # assigning incremental_data matrix
            for k in range(tri_3.origin_period_count):
                for j in range(tri_3.dev_period_count - 1):
                    value = tri_3.incremental_data[k,j] 
                    if value is not None and not math.isnan(value):
                        tri_4.incremental_data[k,j]  = tri_3.incremental_data[k,j] 

            # assigning incremental development factors
            for k in range(tri_4.dev_period_count - 2):
                tri_4.idf_overrides[k] = (tri.incremental_dev_factor[k].blended_selected)  if (k<15)   else 1



    pass

               



