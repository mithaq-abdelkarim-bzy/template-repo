##############################################################################################################################
################                             NOTES                                                            ################ 
##############################################################################################################################

### Below is organised into 3 expoure rating functions:
###     a) rate_exposure_details_crcf        - anything specific to crcf
###     b) rate_exposure_details_political   - anything specific to political
###     c) rate_exposure_details             - anything generic and then conditions on whether political or crcf and does that
###
### Additionally there are 2 helper functions to calculate the MBBEFD exposure curve - https://www.casact.org/sites/default/files/2021-03/8_Bernegger.pdf
###     a) exposure_curve           - determine a single point on the exposure curve
###     b) exposure_curve_series    - determine a series of points on the exposure curve
###


##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################

###  1) 
###  2) 
###  3)
###  4) 
###  5) line 1007             # JB day2 consider if the adjustments below would be better forming part of the simulations 
###  6) 
###  7) 
###  8) 
###  9) 
### 10)
##############################################################################################################################



import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_constants as const
from algorithms import parameter_tables_schema as params
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd
from dateutil.relativedelta import relativedelta
from datetime import datetime
from operator import itemgetter


# 'The distribution function for the G-curve (limit expectation) for mbbedf = exposure curve
def exposure_curve(b, g, x):
    if g == 1:                                      result = x
    elif b == 1 and g > 1:                          result = math.log(1 + (g - 1) * x) / math.log(g)
    elif b * g == 1 and g > 1:                      result = (1 - b ** x) / (1 - b)
    elif b > 0 and b != 1 and b * g != 1 and g > 1: result = math.log(((g - 1) * b + (1 - g * b) * (b ** x)) / (1 - b)) / math.log(g * b)
    else:                                           result = -1 #error
    return result


def exposure_curve_series(b, g, x_series):
    x_series    =   x_series.astype(float)                        
    if g == 1:                                      result = x_series
    elif b == 1 and g > 1:                          result = np.log(1 + (g - 1) * x_series) / math.log(g)
    elif b * g == 1 and g > 1:                      result = (1 - b ** x_series) / (1 - b)
    elif b > 0 and b != 1 and b * g != 1 and g > 1: result = np.log(((g - 1) * b + (1 - g * b) * (b ** x_series)) / (1 - b)) / math.log(g * b)
    else:                                           result = -1 #error
    return result










def rate_exposure_details_crcf(hxd):
    cds         = hxd.cds 

    ##############################################
    ### 1) key names / pre-shipment / ihs countries
    ##############################################
    crcf        = cds.exposure.granular.crcf   
    crcf_mod    = cds.modifiers.crcf   

    # setting pst_shipment_amt
    crcf.pst_shipment_amt       = 1 - (crcf.pre_shipment_amt or 0)


    # determine the ihs data request
    ihs_country_df              = hx.params.tbl_ihs_country
    cds.ihs.calc_run_value      = ihs_country_df[ (ihs_country_df['IHS Country'] == cds.risk_info.crcf_country) ]['Two Digit Codes'].iat[0]
    cds.ihs.check_run_consistent=("IHS extract remain valid" if cds.ihs.last_run_value == cds.ihs.calc_run_value 
                                                                    else "IHS needs to be rerun - values have changed")

    ##############################################
    ### 2) Load product assumptions
    ##############################################

    # load in assumptions dataframe and filter to product
    all_product_assump_df           = hx.params.tbl_product_assump
    product_assump_df               = all_product_assump_df[    (all_product_assump_df['Product']   == cds.product)]
    
    # filter assumptions dataframe to just relevant row
    lgd_row                         = product_assump_df[    (product_assump_df['Assumption Group']  == "lgd"                 ) ]
    lgd_min_row                     = product_assump_df[    (product_assump_df['Assumption Group']  == "lgd_min"             ) ]
    lgd_max_row                     = product_assump_df[    (product_assump_df['Assumption Group']  == "lgd_max"             ) ]

    uw_adj_min_row                  = product_assump_df[    (product_assump_df['Assumption Group']  == "uw_adj_min"          ) ]
    uw_adj_max_row                  = product_assump_df[    (product_assump_df['Assumption Group']  == "uw_adj_max"          ) ]

    pre_shipment_m_value_row        = product_assump_df[    (product_assump_df['Assumption Group']  == "pre_shipment_m_value") ]
    pre_shipment_c_value_row        = product_assump_df[    (product_assump_df['Assumption Group']  == "pre_shipment_c_value") ]
    pre_shipment_base_row           = product_assump_df[    (product_assump_df['Assumption Group']  == "pre_shipment_base"   ) ]

    recovery_rate_row               = product_assump_df[    (product_assump_df['Assumption Group']  == "recovery_rate"       ) ]
    time_to_recovery_row            = product_assump_df[    (product_assump_df['Assumption Group']  == "dol_to_recovery"     ) ]    
    risk_free_rate_row              = product_assump_df[    (product_assump_df['Assumption Group']  == "risk_free_rate"      ) ]  

    benchmark_lr_row                = product_assump_df[    (product_assump_df['Assumption Group']  == "benchmark_lr"        ) ]    
    exposure_curve_b_row            = product_assump_df[    (product_assump_df['Assumption Group']  == "exposure_curve_b"    ) ]   
    exposure_curve_g_row            = product_assump_df[    (product_assump_df['Assumption Group']  == "exposure_curve_g"    ) ]   

    # checking for empty push intended value to hxd or temporary variable as appropriate
    crcf_mod.default.lgd            = 0 if lgd_row.empty                    else lgd_row['Value'].iat[0]
    crcf_mod.override_min.lgd       = 0 if lgd_min_row.empty                else lgd_min_row['Value'].iat[0]
    crcf_mod.override_max.lgd       = 0 if lgd_max_row.empty                else lgd_max_row['Value'].iat[0]

    crcf_mod.override_min.uw_adj    = 0 if uw_adj_min_row.empty             else uw_adj_min_row['Value'].iat[0]
    crcf_mod.override_max.uw_adj    = 0 if uw_adj_max_row.empty             else uw_adj_max_row['Value'].iat[0]

    pre_shipment_m_value            = 0 if pre_shipment_m_value_row.empty   else pre_shipment_m_value_row['Value'].iat[0]   
    pre_shipment_c_value            = 0 if pre_shipment_c_value_row.empty   else pre_shipment_c_value_row['Value'].iat[0]   
    pre_shipment_base               = 0 if pre_shipment_base_row.empty      else pre_shipment_base_row['Value'].iat[0]   

    crcf.recovery_adj_pct           = 0 if recovery_rate_row.empty          else recovery_rate_row['Value'].iat[0]   
    time_to_recovery                = 0 if time_to_recovery_row.empty       else time_to_recovery_row['Value'].iat[0]  
    risk_free_rate                  = 0 if risk_free_rate_row.empty         else risk_free_rate_row['Value'].iat[0]  
                                                                                                        
    benchmark_lr                    = 1 if benchmark_lr_row.empty           else benchmark_lr_row['Value'].iat[0]  
    b                               = 0 if exposure_curve_b_row.empty       else exposure_curve_b_row['Value'].iat[0]  
    g                               = 0 if exposure_curve_g_row.empty       else exposure_curve_g_row['Value'].iat[0]  




    ##############################################
    ### 3) Get Default Ratings / Grades / LGD / POD / UW Adj
    ##############################################

    # determine country rating
    country_rating_df           = hx.params.tbl_country_rating
    std_country_rating_row      = country_rating_df[ (country_rating_df['Country']     == cds.risk_info.crcf_country) ]
    ihs_country_rating_row      = country_rating_df[ (country_rating_df['IHS Country'] == cds.risk_info.crcf_country) ]
    crcf_mod.rating_country     = ( std_country_rating_row['Rating'].iat[0]      
                                        if not std_country_rating_row.empty        
                                        else ihs_country_rating_row['Rating'].iat[0]     
                                            if not ihs_country_rating_row.empty       
                                            else const.default_country_rating)


    # determine corporate rating
    grade_pod_df                = hx.params.tbl_grade_pod
    pod_country_row             = grade_pod_df[ (grade_pod_df['Grade'] == crcf_mod.rating_country) ]
    pod_corporate_row           = grade_pod_df[ (grade_pod_df['Grade'] == crcf_mod.rating_corporate) ]
    crcf_mod.default.grade      = ( crcf_mod.rating_country   
                                        if (cds.product == "Contract Frustration"       or      crcf_mod.rating_corporate is None ) 
                                        else crcf_mod.rating_country  
                                            if (pod_corporate_row['Score'].iat[0] >= pod_country_row['Score'].iat[0]) 
                                            else crcf_mod.rating_corporate)


    # determine probability of default (pod)
    pod_default_row             = grade_pod_df[ (grade_pod_df['Grade'] == crcf_mod.default.grade) ]
    crcf_mod.default.pod        = pod_default_row['Value'].iat[0]

    # determine underwriter adjustment
    crcf_mod.default.uw_adj     = 0




    ##############################################
    ### 4) Get Min/Max/Selected of Grades / LGD / POD / UW Adj
    ##############################################

    # determine Min/Max  of   Grades & PODs
    pod_score_min_available     = grade_pod_df['Score'].min()
    pod_score_max_available     = grade_pod_df['Score'].max()

    pod_default_row             = grade_pod_df[ (grade_pod_df['Grade'] == crcf_mod.default.grade) ]
    score_default               = pod_default_row['Score'].iat[0]
    score_min                   = max(score_default - 2,    pod_score_min_available)
    score_max                   = min(score_default + 2,    pod_score_max_available)

    crcf_mod.override_min.grade = grade_pod_df[ (grade_pod_df['Score'] == score_min) ]['Grade'].iat[0]
    crcf_mod.override_max.grade = grade_pod_df[ (grade_pod_df['Score'] == score_max) ]['Grade'].iat[0]

    crcf_mod.override_min.pod   = grade_pod_df[ (grade_pod_df['Score'] == score_min) ]['Value'].iat[0]
    crcf_mod.override_max.pod   = grade_pod_df[ (grade_pod_df['Score'] == score_max) ]['Value'].iat[0]


    # determine Selected Grade
    override_grade_available    = crcf_mod.override.grade is not None 
    override_grade              = crcf_mod.override.grade     if override_grade_available      else crcf_mod.default.grade 

    pod_override_row            = grade_pod_df[ (grade_pod_df['Grade'] == override_grade) ]
    score_override              = pod_override_row['Score'].iat[0]
    crcf_mod.override.pod       = pod_override_row['Value'].iat[0]

    score_selected              = max(score_min,    min(score_max, score_override))
    crcf_mod.selected.grade     = grade_pod_df[ (grade_pod_df['Score'] == score_selected) ]['Grade'].iat[0]
    crcf_mod.selected.pod       = grade_pod_df[ (grade_pod_df['Score'] == score_selected) ]['Value'].iat[0]


    # determine Selected LGD (min/max done earlier section)
    override_lgd_available      = crcf_mod.override.lgd is not None 
    crcf_mod.selected.lgd       = ( max(crcf_mod.override_min.lgd ,    min(crcf_mod.override_max.lgd, crcf_mod.override.lgd))
                                        if override_lgd_available  else crcf_mod.default.lgd)


    # determine Selected UW Adjustments (min/max done earlier section)
    override_uw_adj_available   = crcf_mod.override.uw_adj is not None 
    crcf_mod.selected.uw_adj    = ( max(crcf_mod.override_min.uw_adj ,    min(crcf_mod.override_max.uw_adj, crcf_mod.override.uw_adj))
                                        if override_uw_adj_available  else crcf_mod.default.uw_adj)




    ##############################################
    ### 5a) Gather IHS information and determine pre_shipment_exponent & recession_score
    ##############################################

    # set ihs dataframe
    ihs_name_group_df           = hx.params.tbl_ihs_name_group
    ihs_country_df              = hx.params.tbl_ihs_country
    ihs_factors_df              = pd_df_from_hx_list(cds.ihs.ihs_detail)


    # handling for rarc & transient hxd - we dont want to have to keep querying the ihs api - (2-3seconds x 8 buckets) - repeated for crcf & political
    # similarly on migrated data we dont want it to not show any information until they have pressed refresh on ihs
    migrated_no_live_ihs = (hxd.model_state.is_migrated == True) and ihs_factors_df.empty
    if hxd.live_hxd == False or migrated_no_live_ihs:
        ihs_static_factors_df                           = hx.params.tbl_ihs_static_data
        ihs_static_factors_df['historic_updated_date']  = pd.to_datetime(ihs_static_factors_df['historic_updated_date']).dt.date # converts from datetime to date so drop duplicates below works
        columns                 = ['country','risk_name','historic_updated_date','historic_updated_value']
        ihs_factors_df          = ihs_factors_df.append(ihs_static_factors_df, ignore_index=True).drop_duplicates().sort_values(by = columns) 


    ihs_name_group_df.rename(columns={'crcf_group':'group'}, inplace=True)
    ihs_name_group_df.drop(['pr_group_2_weight','pr_group_2','pr_group_1'], axis = 1, inplace = True)

    #filter ihs by: (i) country code; (ii) updated before inception date; (iii) maximum of last updated date
    country_2digit              = ihs_country_df[ (ihs_country_df['IHS Country'] == cds.risk_info.crcf_country) ]['Two Digit Codes'].iat[0]     # cds.risk_info.crcf_country depends on this table so no need to error trap here
    incept_date                 = hxd.hx_core.inception_date.date() if isinstance(hxd.hx_core.inception_date,datetime) else hxd.hx_core.inception_date
    conditions                  =(   (ihs_factors_df['country']                   == country_2digit            )
                                   & (ihs_factors_df['historic_updated_date']     <= np.datetime64(incept_date))    )
    
    ihs_factors_df['historic_updated_date'] = pd.to_datetime(ihs_factors_df['historic_updated_date'])               # convert from object to date so idxmax works
    ihs_factors_by_name_df      = ihs_factors_df[ conditions]
    max_date_idx                = ihs_factors_by_name_df.groupby('risk_name')['historic_updated_date'].idxmax()
    ihs_factors_by_name_df      = ihs_factors_by_name_df.loc[max_date_idx]


    # calculate pre_shipment_exponent
    ihs_name_group_df                   = pd.merge(ihs_name_group_df,  ihs_factors_by_name_df,  how='left', left_on=['ihs_name'], right_on=['risk_name']).dropna()
    ihs_name_group_df['value_preship']  = ihs_name_group_df['historic_updated_value']  *  ihs_name_group_df['pre_shipment_weight']
    pre_shipment_exponent               = (1 if ihs_name_group_df.empty
                                                else ihs_name_group_df.groupby('group')[['group','value_preship']].mean().sum().iat[0]  )


    # get recession_score
    recession_score_row                 = ihs_name_group_df[(ihs_name_group_df['ihs_name'] == "Recession")]
    recession_score                     = 0 if recession_score_row.empty else recession_score_row['historic_updated_value'].iat[0]   




    ##############################################
    ### 5b) Calculate pre_shipment_pct & economic_outlook
    ##############################################
    # calculate pre_shipment_pct
    crcf.pre_shipment_adj_pct           = (0    if  pre_shipment_exponent < 1
                                                else 1  if pre_shipment_exponent > 4
                                                        else pre_shipment_m_value * (pre_shipment_base ** pre_shipment_exponent) + pre_shipment_c_value)
    
    # set economic outlook
    economic_banding                    = hx.params.tbl_economic_banding
    conditions                          =(   (economic_banding['lower_band']    <=  recession_score )
                                        & (economic_banding['upper_band']    >   recession_score ))
    economic_banding_row                = economic_banding[conditions]
    crcf_mod.economic_outlook           = 'Unknown' if economic_banding_row.empty else economic_banding_row['economic_band'].iat[0]




    ##############################################
    ### 6) Calculate single values needed for analysis in subsequent dataframe: (i) shipment_risk_pct; (ii) economic_outlook_pct
    ##############################################

    # (i) shipment_risk_pct; 
    crcf.shipment_risk_adj_pct = (crcf.pre_shipment_amt or 0) * (1 + crcf.pre_shipment_adj_pct)    +  crcf.pst_shipment_amt

    # (ii) economic_outlook_adj_pct_pre_adj; 
    economic_grade_band                     = hx.params.tbl_grade_economic_band
    conditions                              =( economic_grade_band['Rating']  == crcf_mod.default.grade)
    economic_grade_band_row                 = economic_grade_band[conditions]
    crcf.economic_outlook_adj_pct_pre_adj   = (1 if (economic_grade_band_row.empty or crcf_mod.economic_outlook == 'Unknown')
                                                else economic_grade_band_row[crcf_mod.economic_outlook].iat[0])

    # (iii) economic_outlook_adj_pct_pst_adj; 
    conditions                              =( economic_grade_band['Rating']  == crcf_mod.selected.grade)
    economic_grade_band_row                 = economic_grade_band[conditions]
    crcf.economic_outlook_adj_pct_pst_adj   = (1 if (economic_grade_band_row.empty or crcf_mod.economic_outlook == 'Unknown')
                                                else economic_grade_band_row[crcf_mod.economic_outlook].iat[0])


    ##############################################
    ### 7) Loading in exposure dataframe, setting sum insured value and appending year labels
    ##############################################

    exposure_df                 = pd_df_from_hx_list(cds.exposure.granular.crcf.exposure_profile)
    exposure_amt_columns        = [  'month_1',  'month_2',  'month_3',  'month_4',  'month_5',  'month_6'
                                    ,'month_7',  'month_8',  'month_9',  'month_10', 'month_11', 'month_12']

    # setting sum insured
    exposure_amt_df             = exposure_df.loc[:,exposure_amt_columns]
    crcf.sum_insured            = exposure_amt_df.fillna(0).max().max() #double max used below first max for each row, second max get max of the resulting column

    # year labels
    yoa                             = hxd.hx_core.inception_date.year
    exposure_df['year']             = exposure_df.index + 1                                                     # main model works on years starting at 1
    exposure_df['year_label']       = (exposure_df['year'] + yoa -1).astype(str)                                # uw requested hx model year labelling to detail year at outset
    exposure_df['year_show_hide']   = (exposure_df['year'] <=   math.ceil(cds.risk_info.crcf_term / 12)   )


    ##############################################
    ### 8) calculating dataframe columns which are basis agnostic
    ##############################################

    # calculate average default time
    month                                       = list(range(1, 13))                                            # series 1 to 12
    exposure_df['helper_exposure_x_month']      = exposure_amt_df.fillna(0).dot(month)  # use dot for matrix multiplication
    exposure_df['helper_sum_insured']           = exposure_amt_df.fillna(0).sum(axis=1)
    exposure_df['average_default_month']        = np.where( exposure_df['helper_sum_insured'] == 0 , 6
                                                            , exposure_df['helper_exposure_x_month'] / exposure_df['helper_sum_insured'] - 0.5)
    exposure_df['average_default_year_month']   = (exposure_df['year'] - 1) + exposure_df['average_default_month']/12

    # calculate average recovery time
    exposure_df['average_recovery_time']        = exposure_df['average_default_year_month'] + time_to_recovery

    # calculate average exposure
    exposure_df['average_exposure']             = exposure_amt_df.mean(axis=1,skipna=True)


    # calculate expected recovery percent discounted
    exposure_df['expected_recovery_pct']        = crcf.recovery_adj_pct / ((1 + risk_free_rate) ** exposure_df['average_recovery_time']) 

    # calculate the term adjustment in respect of the final year
    final_yr_test                               = int(math.ceil(cds.rating_factors.policy_term/12))
    final_yr_adj                                = (cds.rating_factors.policy_term % 12) / 12  
    final_yr_adj                                = 1 if final_yr_adj ==0 else final_yr_adj
    exposure_df['term_adj']                     = np.where(         exposure_df['year'] == final_yr_test,       (cds.rating_factors.policy_term % 12) / 12
                                                     ,np.where(     exposure_df['year'] >  final_yr_test,       0
                                                        ,                                                       1))

    ##############################################
    ### 9) calculating dataframe columns for pre uw adjustment
    ##############################################

    # loading in Tenor
    exposure_df.drop(['pre_uw_adj_tenor_load'], axis = 1, inplace = True) # this is the value we are trying to source from grade_tenor_load_df 
    grade_tenor_load_df                                 = hx.params.tbl_grade_tenor_load
    grade_tenor_load_df.rename(columns={'Tenor': 'year','Value': 'pre_uw_adj_tenor_load'}, inplace=True)
    grade_tenor_load_rows                               = grade_tenor_load_df.loc[ (grade_tenor_load_df['Grade']  == crcf_mod.default.grade),['year','pre_uw_adj_tenor_load'] ]
    exposure_df                                         = exposure_df.merge(grade_tenor_load_rows, on='year', how='left')
    
    
    # pre_uw_adj_pod_adj_inc = "Probability of Default (at n)" * "Tenor Load" * "Economic Outlook Load" * "Pre-shipment risk load"
    exposure_df['pre_uw_adj_pod_adj_inc']               = (crcf_mod.default.pod   *   exposure_df['pre_uw_adj_tenor_load']   *   crcf.economic_outlook_adj_pct_pre_adj   *  crcf.shipment_risk_adj_pct)
        
    # survival probability in year n
    exposure_df['helper_pre_uw_adj_prob_no_default_inc']= 1 - exposure_df['pre_uw_adj_pod_adj_inc']

    # probability of default in year n adjusted for probability a default may have already occurred
    exposure_df['pre_uw_adj_pod_adj_inc_allow_prior']   = ( exposure_df['helper_pre_uw_adj_prob_no_default_inc'].cumprod() 
                                                            /   exposure_df['helper_pre_uw_adj_prob_no_default_inc']
                                                            *   exposure_df['pre_uw_adj_pod_adj_inc']  ) 
    
    # average severity in year n, should a default occur = lgd * average exposure
    exposure_df['pre_uw_adj_average_severity']          =   exposure_df['average_exposure']   * crcf_mod.default.lgd
    
    # average loss in year n, allowing for probability of occurring, likely severity after netting off any recoveries and if only part of a year of coverage
    exposure_df['pre_uw_adj_average_loss']              = ( exposure_df['pre_uw_adj_average_severity'] 
                                                            *   (1 - exposure_df['expected_recovery_pct'] )
                                                            *   exposure_df['pre_uw_adj_pod_adj_inc_allow_prior']  
                                                            *   exposure_df['term_adj'] )

    # calculate the adjustment for excess and limit necessary using the custom formula and apply to pre_uw_adj_average_loss
    limit                                       = cds.layers[0].limit
    excess                                      = cds.layers[0].excess
    sum_insured                                 = cds.exposure.granular.crcf.sum_insured
    lim_xs_si_unavailable                       = ((sum_insured == 0    or  cds.layers[0].limit is None     or  cds.layers[0].excess is None))
    lim_xs_adj                                  = (0 if lim_xs_si_unavailable   else exposure_curve(b, g, (excess + limit)/sum_insured) - exposure_curve(b, g, (excess)/sum_insured)   )
    exposure_df['pre_uw_adj_average_loss_adj_lim_xs']   = exposure_df['pre_uw_adj_average_loss']  *  lim_xs_adj

    # calculate the benchmark GN premium by loading in benchmark lr and grossing up
    exposure_df['pre_uw_adj_premium_benchmark'] = exposure_df['pre_uw_adj_average_loss_adj_lim_xs'] / benchmark_lr
    
    # calculate the premium achieved
    return_on_exposure_annual_offered           = cds.layers[0].crcf.metrics_summary_pst_uwadj_annual.roe_offered or 0
    exposure_df['pre_uw_adj_premium_achieved']  = exposure_df['average_exposure'] * return_on_exposure_annual_offered * exposure_df['term_adj']
    
    # calculate the premium achieved allowing for defaults - EXCEL APPROACH before feedback 06/02/2025 - similarly 50 lines below
    # exposure_df['helper_pre_uw_adj_pod_adj_inc_allow_prior_previous']   =  [ ( 0    if index == 0
    #                                                                                 else exposure_df['pre_uw_adj_pod_adj_inc_allow_prior'][(index - 1)] )  
    #                                                                                 for index,x in enumerate(exposure_df['pre_uw_adj_pod_adj_inc_allow_prior'])]
    # exposure_df['pre_uw_adj_premium_achieved_adj_pod']  = exposure_df['pre_uw_adj_premium_achieved']  *  (1 - exposure_df['helper_pre_uw_adj_pod_adj_inc_allow_prior_previous'])

    # calculate the premium achieved allowing for defaults
    exposure_df['helper_pre_uw_adj_pod_adj_inc_allow_prior_previous']   =  (    exposure_df['helper_pre_uw_adj_prob_no_default_inc'].cumprod() 
                                                                                / exposure_df['helper_pre_uw_adj_prob_no_default_inc']            )
    exposure_df['pre_uw_adj_premium_achieved_adj_pod']  = exposure_df['pre_uw_adj_premium_achieved']  *  exposure_df['helper_pre_uw_adj_pod_adj_inc_allow_prior_previous']



    ##############################################
    ### 10) calculating dataframe columns for post uw adjustment
    ##############################################

    # loading in Tenor - loaded again as we change some of the column names above different to below
    grade_tenor_load_df                                 = hx.params.tbl_grade_tenor_load
    grade_tenor_load_df.rename(columns={'Tenor': 'year','Value': 'pst_uw_adj_tenor_load'}, inplace=True)
    grade_tenor_load_rows                               = grade_tenor_load_df.loc[ (grade_tenor_load_df['Grade']  == crcf_mod.selected.grade),['year','pst_uw_adj_tenor_load'] ]
    exposure_df.drop(['pst_uw_adj_tenor_load'], axis = 1, inplace = True)
    exposure_df                                         = exposure_df.merge(grade_tenor_load_rows, on='year', how='left')

    # pst_uw_adj_pod_adj_inc = "Probability of Default (at n)" * "Tenor Load" * "Economic Outlook Load" * "Pre-shipment risk load"
    exposure_df['pst_uw_adj_pod_adj_inc']               = (crcf_mod.selected.pod   *   exposure_df['pst_uw_adj_tenor_load']   *   crcf.economic_outlook_adj_pct_pst_adj   *  crcf.shipment_risk_adj_pct)
        
    # survival probability in year n
    exposure_df['helper_pst_uw_adj_prob_no_default_inc']= 1 - exposure_df['pst_uw_adj_pod_adj_inc']

    # probability of default in year n adjusted for probability a default may have already occurred
    exposure_df['pst_uw_adj_pod_adj_inc_allow_prior']   = ( exposure_df['helper_pst_uw_adj_prob_no_default_inc'].cumprod() 
                                                            /   exposure_df['helper_pst_uw_adj_prob_no_default_inc']
                                                            *   exposure_df['pst_uw_adj_pod_adj_inc']  ) 
    
    # average severity in year n, should a default occur = lgd * average exposure
    exposure_df['pst_uw_adj_average_severity']          =   exposure_df['average_exposure']   * crcf_mod.selected.lgd
    
    # average loss in year n, allowing for probability of occurring, likely severity after netting off any recoveries and if only part of a year of coverage
    exposure_df['pst_uw_adj_average_loss']              = ( exposure_df['pst_uw_adj_average_severity'] 
                                                            *   (1 - exposure_df['expected_recovery_pct'] )
                                                            *   exposure_df['pst_uw_adj_pod_adj_inc_allow_prior']  
                                                            *   exposure_df['term_adj'] )


    # apply the adjustment for excess and limit calculated earlier (pre_uw_adj)  and apply to pst_uw_adj_average_loss
    exposure_df['pst_uw_adj_average_loss_adj_lim_xs']   = exposure_df['pst_uw_adj_average_loss']  *  lim_xs_adj

    # calculate the benchmark GN premium by using benchmark lr loaded earlier and grossing up
    exposure_df['pst_uw_adj_premium_benchmark']         = exposure_df['pst_uw_adj_average_loss_adj_lim_xs'] / benchmark_lr
    
    # calculate the premium achieved
    exposure_df['pst_uw_adj_premium_achieved']          = exposure_df['average_exposure'] * return_on_exposure_annual_offered * exposure_df['term_adj']
    
    # calculate the premium achieved allowing for defaults
    exposure_df['helper_pst_uw_adj_pod_adj_inc_allow_prior_previous']   =  (   exposure_df['helper_pst_uw_adj_prob_no_default_inc'].cumprod() 
                                                                                / exposure_df['helper_pst_uw_adj_prob_no_default_inc']           )
    exposure_df['pst_uw_adj_premium_achieved_adj_pod']  = exposure_df['pst_uw_adj_premium_achieved']  * exposure_df['helper_pst_uw_adj_pod_adj_inc_allow_prior_previous']



    ##############################################
    ### 11) calculating dataframe columns for implied lgd
    ##############################################

    # implying expected loss in layer from achieved premium and benchmark lr
    exposure_df['implied_lgd_average_loss_adj_lim_xs']  = exposure_df['pst_uw_adj_premium_achieved']  *  benchmark_lr 

    # implying expected loss FGU & unlimitted from assocated loss to layer and exposure curve
    exposure_df['implied_lgd_average_loss']             = (0 if lim_xs_adj == 0 
                                                            else exposure_df['implied_lgd_average_loss_adj_lim_xs'] / lim_xs_adj)

    # implying average severity by grossing up above expected losses for recoveries and removing application of default probability
    exposure_df['implied_lgd_average_severity']         = (exposure_df['implied_lgd_average_loss']  
                                                                / ( 1  - exposure_df['expected_recovery_pct']  ) 
                                                                / exposure_df['pst_uw_adj_pod_adj_inc_allow_prior'] 
                                                                / exposure_df['term_adj'] )

    # implying average lgd by taking above severity and dividing by average exposure
    exposure_df['implied_lgd']                          = np.where( exposure_df['average_exposure']  == 0
                                                                    , 0 
                                                                    , exposure_df['implied_lgd_average_severity']  / exposure_df['average_exposure']  )


    ##############################################
    ### 12) calculating dataframe columns for implied grade
    ##############################################

    # implying expected loss in layer from achieved premium and benchmark lr
    exposure_df['implied_grade_average_loss_adj_lim_xs']= exposure_df['pst_uw_adj_premium_achieved']  *  benchmark_lr 

    # implying expected loss FGU & unlimitted from assocated loss to layer and exposure curve
    exposure_df['implied_grade_average_loss']           = (0 if lim_xs_adj == 0 
                                                            else exposure_df['implied_lgd_average_loss_adj_lim_xs'] / lim_xs_adj)

    # implying pod by grossing up above expected losses for recoveries and removing average severity
    exposure_df['implied_grade_pod_adj_inc_allow_prior']= np.where( exposure_df['pst_uw_adj_average_severity']  == 0
                                                                    , 0
                                                                    , exposure_df['implied_lgd_average_loss']  
                                                                        / ( 1  - exposure_df['expected_recovery_pct']  ) 
                                                                        /  exposure_df['pst_uw_adj_average_severity']  
                                                                        /  exposure_df['term_adj'] )                                                                        
    
    # implying pod in a year after removing impact of prior defaults
    cum_prob_survival = 1   #cumulative survival probability to start of year
    for index, row in exposure_df.iterrows():
        if      row['year'] == 1 :  temp_value = row['implied_grade_pod_adj_inc_allow_prior']
        else:                       temp_value = row['implied_grade_pod_adj_inc_allow_prior'] / cum_prob_survival
        exposure_df.at[index,'implied_grade_pod_adj_inc'] = temp_value
        cum_prob_survival *= ( 1 - temp_value )

    # implying raw pod in a year after removing impact of prior defaults
    exposure_df['implied_grade_pod_inc']                = np.where( (exposure_df['pst_uw_adj_tenor_load']  *  crcf.economic_outlook_adj_pct_pst_adj  *  crcf.shipment_risk_adj_pct ) == 0
                                                                    , 0
                                                                    , ( exposure_df['implied_grade_pod_adj_inc'] 
                                                                        / ( exposure_df['pst_uw_adj_tenor_load']  *  crcf.economic_outlook_adj_pct_pst_adj  *  crcf.shipment_risk_adj_pct )))


    ####################################################################################
    ### 13) Write to HXD                                                             ###
    ####################################################################################

    output_columns_str      = ['year_label']
    output_columns_date     = []
    output_columns_int      = ['year']
    output_columns_bool     = ['year_show_hide']
    output_columns_flt      = ['average_default_month'
                                ,'average_default_year_month'
                                ,'average_exposure'
                                ,'average_recovery_time'
                                ,'expected_recovery_pct'
                                ,'term_adj'
                                ,'pre_uw_adj_tenor_load'
                                ,'pre_uw_adj_pod_adj_inc'
                                ,'pre_uw_adj_pod_adj_inc_allow_prior'
                                ,'pre_uw_adj_average_severity'
                                ,'pre_uw_adj_average_loss'
                                ,'pre_uw_adj_average_loss_adj_lim_xs'
                                ,'pre_uw_adj_premium_benchmark'
                                ,'pre_uw_adj_premium_achieved'
                                ,'pre_uw_adj_premium_achieved_adj_pod'
                                ,'pst_uw_adj_tenor_load'
                                ,'pst_uw_adj_pod_adj_inc'
                                ,'pst_uw_adj_pod_adj_inc_allow_prior'
                                ,'pst_uw_adj_average_severity'
                                ,'pst_uw_adj_average_loss'
                                ,'pst_uw_adj_average_loss_adj_lim_xs'
                                ,'pst_uw_adj_premium_benchmark'
                                ,'pst_uw_adj_premium_achieved'
                                ,'pst_uw_adj_premium_achieved_adj_pod'
                                ,'implied_lgd_average_loss_adj_lim_xs'
                                ,'implied_lgd_average_loss'
                                ,'implied_lgd_average_severity'
                                ,'implied_lgd'
                                ,'implied_grade_average_loss_adj_lim_xs'
                                ,'implied_grade_average_loss'
                                ,'implied_grade_pod_adj_inc_allow_prior'
                                ,'implied_grade_pod_adj_inc'
                                ,'implied_grade_pod_inc'
                                ]

    dummy_date = pd.to_datetime(const.dum_old_date, format='%Y%m%d')
    exposure_df[output_columns_str ] = exposure_df[output_columns_str ].fillna('')
    exposure_df[output_columns_date] = exposure_df[output_columns_date].fillna(dummy_date)
    exposure_df[output_columns_int ] = exposure_df[output_columns_int ].fillna(0)
    exposure_df[output_columns_bool] = exposure_df[output_columns_bool].fillna(True)
    exposure_df[output_columns_flt ] = exposure_df[output_columns_flt ].fillna(0)

    write_pd_to_hxd(exposure_df
                    , cds.exposure.granular.crcf.exposure_profile
                    ,  output_columns_str + output_columns_date + output_columns_int + output_columns_bool + output_columns_flt)


    ####################################################################################
    ### 14) Adding month labels                                                      ###
    ####################################################################################

    # using incept_date from above which is date_time variable
    for mth in range(1,13):
        mth_desc = (incept_date + relativedelta(months=mth-1)).strftime("%B")
        setattr(cds.exposure.granular.crcf.exposure_profile_label_months,  f"month_{mth}",  mth_desc)

    

    









def rate_exposure_details_political(hxd):

    cds         = hxd.cds 
    pol         = cds.exposure.granular.political
    pol_key     = cds.exposure.granular.political.key_summary_outputs
    pol_mod     = cds.modifiers.political

    ##############################################
    ### Pol_1) Calcuate Tenor
    ##############################################


    pol.simulation.num_sims = const.number_of_sims


    ##############################################
    ### Pol_2) Load product assumptions
    ##############################################

    # load in assumptions dataframe and filter to product
    all_product_assump_df           = hx.params.tbl_product_assump
    product_assump_df               = all_product_assump_df[    (all_product_assump_df['Product']   == cds.product)]


    # filter assumptions dataframe to just relevant row
    industry_adj_min_row            = product_assump_df[    (product_assump_df['Assumption Group']  == "industry_adj_min"           ) ]
    industry_adj_max_row            = product_assump_df[    (product_assump_df['Assumption Group']  == "industry_adj_max"           ) ]

    insured_quality_adj_min_row     = product_assump_df[    (product_assump_df['Assumption Group']  == "insured_quality_adj_min"    ) ]
    insured_quality_adj_max_row     = product_assump_df[    (product_assump_df['Assumption Group']  == "insured_quality_adj_max"    ) ]

    asset_composition_adj_min_row   = product_assump_df[    (product_assump_df['Assumption Group']  == "asset_composition_adj_min"  ) ]
    asset_composition_adj_max_row   = product_assump_df[    (product_assump_df['Assumption Group']  == "asset_composition_adj_max"  ) ]

    total_uw_adj_min_row            = product_assump_df[    (product_assump_df['Assumption Group']  == "total_uw_adj_min"           ) ]
    total_uw_adj_max_row            = product_assump_df[    (product_assump_df['Assumption Group']  == "total_uw_adj_max"           ) ]

    roe_base_gai_row                = product_assump_df[    (product_assump_df['Assumption Group']  == "roe_base_gai"               ) ]
    roe_base_pv_row                 = product_assump_df[    (product_assump_df['Assumption Group']  == "roe_base_pv"                ) ]
    roe_base_ci_row                 = product_assump_df[    (product_assump_df['Assumption Group']  == "roe_base_ci"                ) ]

    roe_m_gai_row                   = product_assump_df[    (product_assump_df['Assumption Group']  == "roe_m_gai"                  ) ]
    roe_m_pv_row                    = product_assump_df[    (product_assump_df['Assumption Group']  == "roe_m_pv"                   ) ]
    roe_m_ci_row                    = product_assump_df[    (product_assump_df['Assumption Group']  == "roe_m_ci"                   ) ]

    roe_c_gai_row                   = product_assump_df[    (product_assump_df['Assumption Group']  == "roe_c_gai"                  ) ]
    roe_c_pv_row                    = product_assump_df[    (product_assump_df['Assumption Group']  == "roe_c_pv"                   ) ]
    roe_c_ci_row                    = product_assump_df[    (product_assump_df['Assumption Group']  == "roe_c_ci"                   ) ]

    roe_load_fix_ass_row            = product_assump_df[    (product_assump_df['Assumption Group']  == "roe_load_fix_ass"           ) ]
    roe_load_mob_ass_row            = product_assump_df[    (product_assump_df['Assumption Group']  == "roe_load_mob_ass"           ) ]
    roe_load_len_int_row            = product_assump_df[    (product_assump_df['Assumption Group']  == "roe_load_len_int"           ) ]
    roe_load_gov_cont_row           = product_assump_df[    (product_assump_df['Assumption Group']  == "roe_load_gov_cont"          ) ]

    lr_on_model_premium_row         = product_assump_df[    (product_assump_df['Assumption Group']  == "lr_on_model_premium"        ) ]


    # checking for empty push intended value to hxd or temporary variable as appropriate
    pol_mod.override_min.industry          = 0 if industry_adj_min_row.empty           else industry_adj_min_row['Value'].iat[0]
    pol_mod.override_max.industry          = 0 if industry_adj_max_row.empty           else industry_adj_max_row['Value'].iat[0]

    pol_mod.override_min.insured_quality   = 0 if insured_quality_adj_min_row.empty    else insured_quality_adj_min_row['Value'].iat[0]
    pol_mod.override_max.insured_quality   = 0 if insured_quality_adj_max_row.empty    else insured_quality_adj_max_row['Value'].iat[0]

    pol_mod.override_min.asset_composition = 0 if asset_composition_adj_min_row.empty  else asset_composition_adj_min_row['Value'].iat[0]   
    pol_mod.override_max.asset_composition = 0 if asset_composition_adj_max_row.empty  else asset_composition_adj_max_row['Value'].iat[0]   

    pol_mod.override_min.total             = 0 if total_uw_adj_min_row.empty           else total_uw_adj_min_row['Value'].iat[0]   
    pol_mod.override_max.total             = 0 if total_uw_adj_max_row.empty           else total_uw_adj_max_row['Value'].iat[0]   

    roe_base_gai                           = 0 if roe_base_gai_row.empty               else roe_base_gai_row['Value'].iat[0]
    roe_base_pv                            = 0 if roe_base_pv_row.empty                else roe_base_pv_row['Value'].iat[0]   
    roe_base_ci                            = 0 if roe_base_ci_row.empty                else roe_base_ci_row['Value'].iat[0]   

    roe_m_gai                              = 0 if roe_m_gai_row.empty                  else roe_m_gai_row['Value'].iat[0]
    roe_m_pv                               = 0 if roe_m_pv_row.empty                   else roe_m_pv_row['Value'].iat[0]   
    roe_m_ci                               = 0 if roe_m_ci_row.empty                   else roe_m_ci_row['Value'].iat[0]   

    roe_c_gai                              = 0 if roe_c_gai_row.empty                  else roe_c_gai_row['Value'].iat[0]
    roe_c_pv                               = 0 if roe_c_pv_row.empty                   else roe_c_pv_row['Value'].iat[0]   
    roe_c_ci                               = 0 if roe_c_ci_row.empty                   else roe_c_ci_row['Value'].iat[0]   

    roe_load_fix_ass                       = 0 if roe_load_fix_ass_row.empty           else roe_load_fix_ass_row['Value'].iat[0]
    roe_load_mob_ass                       = 0 if roe_load_mob_ass_row.empty           else roe_load_mob_ass_row['Value'].iat[0]
    roe_load_len_int                       = 0 if roe_load_len_int_row.empty           else roe_load_len_int_row['Value'].iat[0]   
    roe_load_gov_cont                      = 0 if roe_load_gov_cont_row.empty          else roe_load_gov_cont_row['Value'].iat[0]   

    lr_on_model_premium                    = 1 if lr_on_model_premium_row.empty        else lr_on_model_premium_row['Value'].iat[0]   


    # get the b & g parameters for the exposure_curve function
    exposure_curves_df                  = hx.params.tbl_exposure_curves
    exposure_curves_row                 = exposure_curves_df[    (exposure_curves_df['Curve'] == pol.exposure_curve)    ]
    b                                   = 0 if exposure_curves_row.empty               else exposure_curves_row['b'].iat[0]   
    g                                   = 0 if exposure_curves_row.empty               else exposure_curves_row['g'].iat[0]           
    pol.ec_param_b                      = b
    pol.ec_param_g                      = g


    ##############################################
    ### Pol_3) Calculate Underwriter Adjustments
    ##############################################

    # calculating total override
    pol_mod.override.total              = pol_mod.override.industry    +   pol_mod.override.insured_quality  +   pol_mod.override.asset_composition 


    # calculating selected
    pol_mod.selected.industry           = max(pol_mod.override_min.industry,         min(pol_mod.override_max.industry,          pol_mod.override.industry))
    pol_mod.selected.insured_quality    = max(pol_mod.override_min.insured_quality,  min(pol_mod.override_max.insured_quality,   pol_mod.override.insured_quality))
    pol_mod.selected.asset_composition  = max(pol_mod.override_min.asset_composition,min(pol_mod.override_max.asset_composition, pol_mod.override.asset_composition))
    pol_mod.selected.total              = max(pol_mod.override_min.total,            min(pol_mod.override_max.total,             (pol_mod.override.total or 0)))

    
    ##############################################
    ### Pol_4) Gather IHS information and determine factors by country
    ##############################################

    # set ihs dataframe
    ihs_name_group_df           = hx.params.tbl_ihs_name_group
    ihs_country_df              = hx.params.tbl_ihs_country
    ihs_factors_df              = pd_df_from_hx_list(cds.ihs.ihs_detail)


    # handling for rarc & transient hxd - we dont want to have to keep querying the ihs api - (2-3seconds x 8 buckets) - repeated for crcf & political
    # similarly on migrated data we dont want it to not show any information until they have pressed refresh on ihs
    migrated_no_live_ihs = (hxd.model_state.is_migrated == True) and ihs_factors_df.empty
    if hxd.live_hxd == False or migrated_no_live_ihs:
        ihs_static_factors_df                           = hx.params.tbl_ihs_static_data
        ihs_static_factors_df['historic_updated_date']  = pd.to_datetime(ihs_static_factors_df['historic_updated_date']).dt.date # converts from datetime to date so drop duplicates below works
        columns                 = ['country','risk_name','historic_updated_date','historic_updated_value']
        ihs_factors_df          = ihs_factors_df.append(ihs_static_factors_df, ignore_index=True).drop_duplicates().sort_values(by = columns) 


    ihs_name_group_df.rename(columns={'pr_group_2':'group'}, inplace=True)
    ihs_name_group_df.drop(['crcf_group','pre_shipment_weight'], axis = 1, inplace = True)


    #filter ihs by: (i) country code; (ii) updated before inception date; (iii) maximum of last updated date
    ihs_factors_df['historic_updated_date'] = pd.to_datetime(ihs_factors_df['historic_updated_date'])               # convert from object to date so idxmax works
    conditions =(   (ihs_factors_df['historic_updated_date']     <= np.datetime64(hxd.hx_core.inception_date))    )
    
    ihs_factors_by_name_df      = ihs_factors_df[ conditions]
    max_date_idx                = ihs_factors_by_name_df.groupby(['risk_name','country'])['historic_updated_date'].idxmax()
    ihs_factors_by_name_df      = ihs_factors_by_name_df.loc[max_date_idx]


    # manipulate ihs data by country
    ihs_name_group_df                       = pd.merge(ihs_name_group_df,  ihs_factors_by_name_df,  how='left', left_on=['ihs_name'], right_on=['risk_name']).dropna()
    ihs_name_group_df['value_pr_group_2']   = ihs_name_group_df['historic_updated_value']  *  ihs_name_group_df['pr_group_2_weight']             

    if ihs_name_group_df.empty:
        ihs_output_df                           = pd.DataFrame()
    else:
        ihs_output_df                           = ihs_name_group_df.groupby(['country','group'])[['value_pr_group_2']].sum().reset_index()
        ihs_output_df                           = ihs_output_df.pivot(index='country', columns='group', values='value_pr_group_2').reset_index()
        ihs_output_df.drop(['excluded'], axis = 1, inplace = True)
        ihs_output_df.rename(columns={ 'Currency Inconvertability'  : 'ihs_ci'
                                        ,'Political'                : 'ihs_political'
                                        ,'Political Violence'       : 'ihs_violence'
                                        ,'country'                  : 'country_2dig'}, inplace=True)
        


    ##############################################
    ### Pol_5) Loading in exposure dataframe and appending 2 digit country codes and ihs scores
    ##############################################

    # load in exposure dataframe (exposure_df) from hxd
    exposure_df                 = pd_df_from_hx_list(pol.country_exposure)
    exposure_df.drop(['country_2dig'], axis = 1, inplace = True)

    # load ihs dataframe with 2 digit country code
    ihs_country_df              = hx.params.tbl_ihs_country
    ihs_country_df.rename(columns={'IHS Country':'country','Two Digit Codes':'country_2dig'}, inplace=True)

    # append 2 digit country code to exposure dataframe
    exposure_df                 = exposure_df.merge(ihs_country_df, on='country', how='left')

    # append ihs scores to exposure dataframe
    ihs_cols = ['ihs_ci','ihs_political','ihs_violence']   
    if ihs_name_group_df.empty:
        exposure_df.loc[:,ihs_cols] = 1
    else:
        exposure_df.drop(ihs_cols, axis = 1, inplace = True)
        exposure_df             = exposure_df.merge(ihs_output_df, on='country_2dig', how='left')
        missing_columns         = [col for col in ihs_cols if col not in exposure_df.columns]
        if missing_columns: exposure_df.loc[:,missing_columns] = 1


    # determine if 2 digit country entered exists in ihs data by referencing last run value which is a string concatenation of 2 digit countries loaded
    # exposure_df['is_in_ihs']    = [ test in (cds.ihs.last_run_value or '') for test in exposure_df['country_2dig'].fillna('Missing')]
    # formula above was replaced with below to accommodate the situation where we have the country in the ihs data. e.g. the RARC append of static table
    exposure_df['is_in_ihs']    = [ test in ihs_factors_by_name_df['country'].values for test in exposure_df['country_2dig'].fillna('Missing')]



    # add check on country added
    exposure_df['check']        = np.where(                             exposure_df['country'].isnull(),        ""
                                    ,np.where(                          exposure_df['country']=="",             ""
                                        ,np.where(                      exposure_df['sum_insured'].isnull(),    "Error - Please enter a sum insured >0"
                                            ,np.where(                  exposure_df['sum_insured']<=0,          "Error - Please enter a sum insured >0"
                                                ,np.where(              exposure_df['excess']     < 0,          "Error - Please enter an excess >=0"
                                                    ,np.where(          exposure_df['limit'].isnull(),          "Error - Please enter a limit >0"
                                                        ,np.where(      exposure_df['limit']      <=0,          "Error - Please enter a limit >0"
                                                            ,np.where(  exposure_df['is_in_ihs']==False,        "Error - Country not loaded - reload IHS"
                                                                ,                                               "ok"))))))))

    # calculating the total modelled sum insured - excluding things not ok
    sum_insured_modeled                       = np.where(exposure_df['check']!="ok",0,  exposure_df['sum_insured'] ).sum()

    if sum_insured_modeled >0: 

        ##############################################
        ### Pol_6) determining sublimits and impact of structuring
        ##############################################

        sublimit_pv_avail = pol.coverage_matrix.sublimit.pol_violence         is not None and pol.coverage_matrix.sublimit.pol_violence         !=0
        sublimit_ci_avail = pol.coverage_matrix.sublimit.cur_inconvertibility is not None and pol.coverage_matrix.sublimit.cur_inconvertibility !=0
        deduct_pv_avail   = pol.coverage_matrix.deductible.pol_violence       is not None
        
        exposure_df['sublimit_pv']   = np.where(sublimit_pv_avail, pol.coverage_matrix.sublimit.pol_violence,           exposure_df['limit'])
        exposure_df['sublimit_ci']   = np.where(sublimit_ci_avail, pol.coverage_matrix.sublimit.cur_inconvertibility,   exposure_df['limit'])
        exposure_df['deductible_pv'] = pol.coverage_matrix.deductible.pol_violence   if deduct_pv_avail    else 0


        # calculate the adjustment for excess and limit necessary using the custom formula and apply to pre_uw_adj_average_loss
        policy_limit                        = cds.layers[0].limit or 0
        

        # calculating some helper columns in advance of calculating the exposure curve impact
        # minimum can generate a warning message in the presence of nans but behaves as intended
        exposure_df['excess_or_zero']   = np.where(   exposure_df['excess'].isna(),    0,  exposure_df['excess'])

        exposure_df['struc_adj_ci_top'] = np.minimum(1, (np.minimum( exposure_df['sublimit_ci'], policy_limit)    + exposure_df['excess_or_zero']   )  / exposure_df['sum_insured'])
        exposure_df['struc_adj_ci_bot'] = np.minimum(1, (                                                           exposure_df['excess_or_zero']   )  / exposure_df['sum_insured'])

        exposure_df['struc_adj_pv_top'] = np.minimum(1, (np.minimum( exposure_df['sublimit_pv'], policy_limit)    + exposure_df['excess_or_zero']   )  / exposure_df['sum_insured'])
        exposure_df['struc_adj_pv_bot'] = np.minimum(1, (            exposure_df['deductible_pv']                 + exposure_df['excess_or_zero']   )  / exposure_df['sum_insured'])

        exposure_df['struc_adj_gai_top']= np.minimum(1, (np.minimum( exposure_df['limit'],       policy_limit)    + exposure_df['excess_or_zero']   )  / exposure_df['sum_insured'])
        exposure_df['struc_adj_gai_bot']= np.minimum(1, (                                                           exposure_df['excess_or_zero']   )  / exposure_df['sum_insured'])


        # calculating impact of structuring - vectorised
        exposure_df['struc_adj_ci']     = np.where(exposure_df['check'] != "ok", 0,     exposure_curve_series(b, g, exposure_df['struc_adj_ci_top']) 
                                                                                        - exposure_curve_series(b, g, exposure_df['struc_adj_ci_bot']))

        exposure_df['struc_adj_pv']     = np.where(exposure_df['check'] != "ok", 0,     exposure_curve_series(b, g, exposure_df['struc_adj_pv_top']) 
                                                                                        - exposure_curve_series(b, g, exposure_df['struc_adj_pv_bot']))

        exposure_df['struc_adj_gai']    = np.where(exposure_df['check'] != "ok", 0,     exposure_curve_series(b, g, exposure_df['struc_adj_gai_top']) 
                                                                                        - exposure_curve_series(b, g, exposure_df['struc_adj_gai_bot']))

        exposure_df['struc_adj_crg']    = exposure_df['struc_adj_gai']



        ##############################################
        ### Pol_7) Rate on Exposure - premium and loss
        ##############################################

        # determine whether cover applies for the respective heads of cover
        cover_apply_gai = (     pol.coverage_matrix.mobile_assets.gov_action               or pol.coverage_matrix.fixed_assets.gov_action                or pol.coverage_matrix.lenders_interest.gov_action             )

        cover_apply_pv  = (     pol.coverage_matrix.mobile_assets.pol_violence             or pol.coverage_matrix.fixed_assets.pol_violence              or pol.coverage_matrix.lenders_interest.pol_violence           )

        cover_apply_ci  = (     pol.coverage_matrix.mobile_assets.cur_inconvertibility     or pol.coverage_matrix.fixed_assets.cur_inconvertibility      or pol.coverage_matrix.lenders_interest.cur_inconvertibility   )

        cover_apply_crg = (     pol.coverage_matrix.mobile_assets.cont_relation_govt       or pol.coverage_matrix.fixed_assets.cont_relation_govt        or pol.coverage_matrix.lenders_interest.cont_relation_govt     )


        # assigning values above to hxd
        pol_key.on_cover.gov_action             = cover_apply_gai
        pol_key.on_cover.pol_violence           = cover_apply_pv
        pol_key.on_cover.cur_inconvertibility   = cover_apply_ci
        pol_key.on_cover.cont_relation_govt     = cover_apply_crg


        # determine a load to apply to the roe calculation in the next step
        helper_load_gai = ( roe_load_fix_ass    if pol.coverage_matrix.fixed_assets.gov_action                  else
                            roe_load_mob_ass    if pol.coverage_matrix.mobile_assets.gov_action                 else
                            roe_load_len_int    if pol.coverage_matrix.lenders_interest.gov_action              else 1 )

        helper_load_pv  = ( roe_load_fix_ass    if pol.coverage_matrix.fixed_assets.pol_violence                else
                            roe_load_mob_ass    if pol.coverage_matrix.mobile_assets.pol_violence               else
                            roe_load_len_int    if pol.coverage_matrix.lenders_interest.pol_violence            else 1 )

        helper_load_ci  = ( roe_load_fix_ass    if pol.coverage_matrix.fixed_assets.cur_inconvertibility        else
                            roe_load_mob_ass    if pol.coverage_matrix.mobile_assets.cur_inconvertibility       else
                            roe_load_len_int    if pol.coverage_matrix.lenders_interest.cur_inconvertibility    else 1 )

        helper_load_crg = ( roe_load_fix_ass    if pol.coverage_matrix.fixed_assets.cont_relation_govt          else
                            roe_load_mob_ass    if pol.coverage_matrix.mobile_assets.cont_relation_govt         else
                            roe_load_len_int    if pol.coverage_matrix.lenders_interest.cont_relation_govt      else 1 )


        # determine premium rate-on-exposure based on 35% loss ratio
        exposure_df['prem_roe_gai']         = (0 if cover_apply_gai == False     
                                                else np.where(exposure_df['check']!="ok", 0, roe_m_gai   *   (roe_base_gai ** exposure_df['ihs_political'])  +  roe_c_gai)   *  helper_load_gai)

        exposure_df['prem_roe_pv']          = (0 if cover_apply_pv == False     
                                                else np.where(exposure_df['check']!="ok", 0, roe_m_pv    *   (roe_base_pv ** exposure_df['ihs_violence']  )  +  roe_c_pv )   *  helper_load_pv)

        exposure_df['prem_roe_ci']          = (0 if cover_apply_ci == False     
                                                else np.where(exposure_df['check']!="ok", 0, roe_m_ci    *   (roe_base_ci ** exposure_df['ihs_ci']        )  +  roe_c_ci )   *  helper_load_ci)

        exposure_df['prem_roe_crg']         = (0 if cover_apply_crg == False 
                                                else np.where(exposure_df['check']!="ok", 0, exposure_df['prem_roe_gai']   *  roe_load_gov_cont)   *  helper_load_crg) ### NOTICE THE DIFFERENT FORMULA
        
        exposure_df['prem_roe_tot']         = exposure_df['prem_roe_gai']  +  exposure_df['prem_roe_pv']  +  exposure_df['prem_roe_ci']  +  exposure_df['prem_roe_crg']


        # determine equivalent loss rate-on-exposure based on 35% loss ratio
        exposure_df['loss_roe_gai']         = exposure_df['prem_roe_gai']         * lr_on_model_premium
        exposure_df['loss_roe_pv']          = exposure_df['prem_roe_pv']          * lr_on_model_premium
        exposure_df['loss_roe_ci']          = exposure_df['prem_roe_ci']          * lr_on_model_premium
        exposure_df['loss_roe_crg']         = exposure_df['prem_roe_crg']         * lr_on_model_premium
        exposure_df['loss_roe_tot']         = exposure_df['prem_roe_tot']         * lr_on_model_premium



        ##############################################
        ### Pol_8) Calculate tenor rate and tenor score - notice we only use 3 of 4 covers - reflects model - connected to us only having 3 sets of ihs factors
        ##############################################
        
        # determine sum-insured weighted averages by ihs class
        wgt_avg_ihs_political   = (   np.where(exposure_df['check']!="ok",0, exposure_df['sum_insured'] * exposure_df['ihs_political']).sum()
                                    / np.where(exposure_df['check']!="ok",0, exposure_df['sum_insured']                               ).sum() )
        wgt_avg_ihs_violence    = (   np.where(exposure_df['check']!="ok",0, exposure_df['sum_insured'] * exposure_df['ihs_violence'] ).sum()
                                    / np.where(exposure_df['check']!="ok",0, exposure_df['sum_insured']                               ).sum() )
        wgt_avg_ihs_ci          = (   np.where(exposure_df['check']!="ok",0, exposure_df['sum_insured'] * exposure_df['ihs_ci']       ).sum()
                                    / np.where(exposure_df['check']!="ok",0, exposure_df['sum_insured']                               ).sum() )

        # determine number of relevant of ihs covers 
        cover_count = (   (1 if pol_key.on_cover.gov_action           else 0) 
                        + (1 if pol_key.on_cover.pol_violence         else 0)
                        + (1 if pol_key.on_cover.cur_inconvertibility else 0) )
        
        # determine total amount of relevant of ihs covers
        cover_amount= (   (1 if pol_key.on_cover.gov_action           else 0) *  wgt_avg_ihs_political 
                        + (1 if pol_key.on_cover.pol_violence         else 0) *  wgt_avg_ihs_violence  
                        + (1 if pol_key.on_cover.cur_inconvertibility else 0) *  wgt_avg_ihs_ci        )

        # determine tenor score
        pol_key.tenor_score     = 0 if cover_count==0 else cover_amount / cover_count

        # determine tenor rate by looking up tenor score in associated table and uplifting
        ihsscore_rate_df        = hx.params.tbl_ihsscore_rate
        ihsscore_rate_row       = ihsscore_rate_df[    (ihsscore_rate_df['ihs_score']  <=  pol_key.tenor_score)    ]
        ihsscore_rate           = 0 if ihsscore_rate_row.empty      else ihsscore_rate_row['rate'].iat[-1] # -1 to take the last value in the list  
        tenor_annual            = cds.rating_factors.policy_term / 12
        pol_key.tenor_rate      = 1 if (tenor_annual <= 1) else (  ihsscore_rate ** tenor_annual  )



        ##############################################
        ### Pol_9) Rate on line - premium - allowing for structuring unless noted otherwise
        ##############################################
        #rate_limit                  = 0      if policy_limit==0       else   (pol_key.tenor_rate / policy_limit)       # JB old formula but presented double counting issue on tenor_rate as used here and further down in pol.simulation.total_det_loss_scaled
        rate_limit                  = 0      if policy_limit==0       else   (1 / policy_limit)
        exposure_df['net_rol_gai']  = np.where(exposure_df['check']!="ok",0, (exposure_df['sum_insured'] * exposure_df['prem_roe_gai'] * exposure_df['struc_adj_gai'] * rate_limit))
        exposure_df['net_rol_pv']   = np.where(exposure_df['check']!="ok",0, (exposure_df['sum_insured'] * exposure_df['prem_roe_pv']  * exposure_df['struc_adj_pv']  * rate_limit))
        exposure_df['net_rol_ci']   = np.where(exposure_df['check']!="ok",0, (exposure_df['sum_insured'] * exposure_df['prem_roe_ci']  * exposure_df['struc_adj_ci']  * rate_limit))
        exposure_df['net_rol_crg']  = np.where(exposure_df['check']!="ok",0, (exposure_df['sum_insured'] * exposure_df['prem_roe_crg'] * exposure_df['struc_adj_crg'] * rate_limit))
        exposure_df['net_rol_tot']  = exposure_df['net_rol_gai']  +  exposure_df['net_rol_pv']  +  exposure_df['net_rol_ci']  +  exposure_df['net_rol_crg']

        bkg = 0 if hxd.cds.layers[0].brokerage == 1 else hxd.cds.layers[0].brokerage
        exposure_df['gross_rol_tot']= exposure_df['net_rol_tot'] / (1  -  bkg)



        ##############################################
        ### Pol_10) determine, by cover, summary values: exposure_rol;   simulated_rol;   simulated_lol
        ##############################################
    
        # calculating the overall rate on line for each head of cover
        if sum_insured_modeled != 0:
            pol_key.exposure_rol.gov_action           = np.where(exposure_df['check']!="ok",0, (exposure_df['net_rol_gai'])).sum()
            pol_key.exposure_rol.pol_violence         = np.where(exposure_df['check']!="ok",0, (exposure_df['net_rol_pv'])).sum()
            pol_key.exposure_rol.cur_inconvertibility = np.where(exposure_df['check']!="ok",0, (exposure_df['net_rol_ci'])).sum()
            pol_key.exposure_rol.cont_relation_govt   = np.where(exposure_df['check']!="ok",0, (exposure_df['net_rol_crg'])).sum()
            pol_key.exposure_rol.total                = np.where(exposure_df['check']!="ok",0, (exposure_df['net_rol_tot'])).sum() 

            # code below is equivalent to old excel model but it doesnt make sense to multiply a rate-on-LINE by SUM INSURED like this
            # pol_key.exposure_rol.gov_action           = np.where(exposure_df['check']!="ok",0, (exposure_df['sum_insured'] * exposure_df['net_rol_gai'] )).sum()   /   sum_insured_modeled  
            # pol_key.exposure_rol.pol_violence         = np.where(exposure_df['check']!="ok",0, (exposure_df['sum_insured'] * exposure_df['net_rol_pv']  )).sum()   /   sum_insured_modeled
            # pol_key.exposure_rol.cur_inconvertibility = np.where(exposure_df['check']!="ok",0, (exposure_df['sum_insured'] * exposure_df['net_rol_ci']  )).sum()   /   sum_insured_modeled
            # pol_key.exposure_rol.cont_relation_govt   = np.where(exposure_df['check']!="ok",0, (exposure_df['sum_insured'] * exposure_df['net_rol_crg'] )).sum()   /   sum_insured_modeled
            # pol_key.exposure_rol.total                = np.where(exposure_df['check']!="ok",0, (exposure_df['sum_insured'] * exposure_df['net_rol_tot'] )).sum()   /   sum_insured_modeled




        else:
            pol_key.exposure_rol.gov_action           = 0
            pol_key.exposure_rol.pol_violence         = 0
            pol_key.exposure_rol.cur_inconvertibility = 0
            pol_key.exposure_rol.cont_relation_govt   = 0
            pol_key.exposure_rol.total                = 0


        # determining the load for non-modelled perils (nmp)
        legacy_tp_df    = hx.params.tbl_legacy_tp_parameters
        tp_params_df    = params.tp_parameters.df()
        tp_params_df    = pd.concat([tp_params_df, legacy_tp_df], axis=0, ignore_index=True) # appending the legacy tp parameters
        yoa             = hxd.hx_core.inception_date.year
        if yoa in list(tp_params_df['year']):   tp_year = yoa
        else:                                   tp_year = tp_params_df['year'].max()
        tp_lookup_bool  = (tp_params_df['business_plan_class'] == const.bp_class) & (tp_params_df['year'] == tp_year)
        tp_params       = tp_params_df[tp_lookup_bool]
        nmp_load        = tp_params['nmp_load'].iloc[0]
    
    
        # load inflation uplift - note cat uplift is only for crcf not political - Asa email 21/2/2025
        plan_df         = hx.params.tbl_year_plan_assump
        plan_year       = yoa   if (yoa in list(plan_df['year']))  else plan_df['year'].max()
        inf_uplift      = plan_df[(plan_df['year'] == plan_year)]['inflation_uplift'].iat[0]       

        
        # uplifting simulated loss for nmp and prorating through the covers
        pol.simulation.total_det_loss_uncapped      = np.where(exposure_df['check']!="ok",0, (exposure_df['net_rol_tot'])).sum() * policy_limit * lr_on_model_premium
        simul_uncapped_lc                           = (pol.simulation.total_sim_loss_uncapped or 0)
        simul_capped_lc                             = (pol.simulation.total_sim_loss_capped   or 0)
        simul_ratio_lc                              = 0 if simul_capped_lc == 0 else ( simul_capped_lc / pol.simulation.total_det_loss_uncapped if simul_uncapped_lc ==0 else simul_capped_lc / simul_uncapped_lc) # 2nd condition handling legacy case where we just used simulated capped loss cost directly

        pol.simulation.total_det_loss_capped        = pol.simulation.total_det_loss_uncapped * simul_ratio_lc
            # JB day2 consider if the adjustments below would be better forming part of the simulations 
        pol.simulation.total_det_loss_scaled        = pol.simulation.total_det_loss_capped * pol_key.tenor_rate * (1 + nmp_load) * (1 + inf_uplift) 

        pol_key.simulated_loss.total                = pol.simulation.total_det_loss_scaled
        pol_key.simulated_loss.gov_action           = 0 if pol_key.exposure_rol.total ==0 else pol_key.simulated_loss.total / pol_key.exposure_rol.total   *   pol_key.exposure_rol.gov_action 
        pol_key.simulated_loss.pol_violence         = 0 if pol_key.exposure_rol.total ==0 else pol_key.simulated_loss.total / pol_key.exposure_rol.total   *   pol_key.exposure_rol.pol_violence 
        pol_key.simulated_loss.cur_inconvertibility = 0 if pol_key.exposure_rol.total ==0 else pol_key.simulated_loss.total / pol_key.exposure_rol.total   *   pol_key.exposure_rol.cur_inconvertibility 
        pol_key.simulated_loss.cont_relation_govt   = 0 if pol_key.exposure_rol.total ==0 else pol_key.simulated_loss.total / pol_key.exposure_rol.total   *   pol_key.exposure_rol.cont_relation_govt 


        # determining the simulated gross net premium by head of cover
        pol_key.simulated_prem.total                = pol_key.simulated_loss.total                  / lr_on_model_premium
        pol_key.simulated_prem.gov_action           = pol_key.simulated_loss.gov_action             / lr_on_model_premium
        pol_key.simulated_prem.pol_violence         = pol_key.simulated_loss.pol_violence           / lr_on_model_premium
        pol_key.simulated_prem.cur_inconvertibility = pol_key.simulated_loss.cur_inconvertibility   / lr_on_model_premium
        pol_key.simulated_prem.cont_relation_govt   = pol_key.simulated_loss.cont_relation_govt     / lr_on_model_premium



    ####################################################################################
    ### Pol_11) Write to HXD                                                         ###
    ####################################################################################

    output_columns_str      = [ 'country_2dig'
                                ,'check'
                                ]
    output_columns_date     = []
    output_columns_int      = []
    output_columns_bool     = []
    output_columns_flt      = [ 'sublimit_pv'
                                ,'deductible_pv'
                                ,'sublimit_ci'
                                ,'ihs_political'
                                ,'ihs_violence'
                                ,'ihs_ci'
                                ,'prem_roe_gai'
                                ,'prem_roe_pv'
                                ,'prem_roe_ci'
                                ,'prem_roe_crg'
                                ,'prem_roe_tot'
                                ,'loss_roe_gai'
                                ,'loss_roe_pv'
                                ,'loss_roe_ci'
                                ,'loss_roe_crg'
                                ,'loss_roe_tot'
                                ,'struc_adj_gai'
                                ,'struc_adj_pv'
                                ,'struc_adj_ci'
                                ,'struc_adj_crg'
                                ,'net_rol_gai'
                                ,'net_rol_pv'
                                ,'net_rol_ci'
                                ,'net_rol_crg'
                                ,'net_rol_tot'
                                ,'gross_rol_tot'
                                ]

    dummy_date = pd.to_datetime(const.dum_old_date, format='%Y%m%d')
    exposure_df[output_columns_str ] = exposure_df[output_columns_str ].fillna('')
    exposure_df[output_columns_date] = exposure_df[output_columns_date].fillna(dummy_date)
    exposure_df[output_columns_int ] = exposure_df[output_columns_int ].fillna(0)
    exposure_df[output_columns_bool] = exposure_df[output_columns_bool].fillna(True)
    exposure_df[output_columns_flt ] = exposure_df[output_columns_flt ].fillna(0)

    write_pd_to_hxd(exposure_df
                    , cds.exposure.granular.political.country_exposure
                    ,  output_columns_str + output_columns_date + output_columns_int + output_columns_bool + output_columns_flt)



    # determine the ihs data request status
    country_code_lst            = sorted(list(set([c.country_2dig for c in cds.exposure.granular.political.country_exposure if c.country is not None]))) # wrapping list(set(..)) around deduplicates
    cds.ihs.calc_run_value      = '' if      country_code_lst == []    else   ','.join(country_code_lst)    
    cds.ihs.check_run_consistent=("IHS extract remain valid" if cds.ihs.last_run_value == cds.ihs.calc_run_value 
                                                                    else "IHS needs to be rerun - values have changed")


    # determine the simulation data request status
    cumul_rate  = np.where(exposure_df['check']!="ok",0,  exposure_df['loss_roe_gai'] + exposure_df['loss_roe_crg'] + exposure_df['loss_roe_pv'] +  exposure_df['loss_roe_ci'] ).sum()
    pol_sim     = cds.exposure.granular.political.simulation
    pol_sim.calc_run_value  = f"{ cumul_rate :.5f}"
    pol_sim.check_run_consistent=("Simulation remains valid" if pol_sim.last_run_value == pol_sim.calc_run_value 
                                                                    else "Simulation needs to be rerun - values have changed")




def rate_exposure_details(hxd):

    cds         = hxd.cds 

    if (cds.product in {'Contract Frustration','Credit Risk'}): rate_exposure_details_crcf(hxd)
    if (cds.product in {'Political Risk'}):                     rate_exposure_details_political(hxd)
