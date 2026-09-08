### to activate timer find and replace " timer" with " timer" and then fix line 41

##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################

##############################################################################################################################

import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_constants as const
import datetime
from dateutil.relativedelta import relativedelta
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, write_pd_to_hxd_no_overrides
from operator import itemgetter
from scipy.interpolate import interp1d

# from algorithms.timer import timer




def rate_rating_summary(hxd):
    # timer.start("prep")  # SA: This function takes up the majority of the total rating run time so have broken it down
                         # with timers. Will need to be removed before release but leaving here in case you want to use them
    cds = hxd.cds
    profit_comm = cds.profit_commission.scenarios[0]
    rating_info = cds.layers[0]
    standard_fields = cds.standard_fields
    att = hxd.cds.rating_summary.summary_ratios.attritional
    lrg = hxd.cds.rating_summary.summary_ratios.large
    cat = hxd.cds.rating_summary.summary_ratios.catastrophe
    tot = hxd.cds.rating_summary.summary_ratios.total
    tech= hxd.cds.rating_summary.technical
    kpi = hxd.cds.rating_summary.kpi
    summary = hxd.cds.rating_summary
    risk_info = hxd.cds.risk_info

    prem = cds.layers[0].quoted_premium_100pct

    min_conditions = (pd.notnull(cds.standard_fields.benchmark_class)
                       & pd.notnull(cds.layers[0].quoted_premium_100pct)) 

    if min_conditions:
        # timer.end("prep")
        # timer.start("step 1")
        ####################################################################################
        ### 1) Setting Stage - error trapping etc                                        ###
        ####################################################################################
        # import df

        # timer.start("step 1c")

        policy_df                = pd_df_from_hx_list(cds.bi_data.facility_detail)
        policy_df                = policy_df.sort_values('written_or_estimated_premium', ascending=False) ###where there are multiple policies within the year we prioritise highest premium
        claim_df                 = pd_df_from_hx_list(cds.bi_data.claims_listing)
        claim_mvmt_df            = pd_df_from_hx_list(cds.bi_data.claims_movements)
        rating_df                = pd_df_from_hx_list(cds.rating_summary.detail_by_year)

        perc_ult_df              = pd_df_from_hx_list(cds.triangle_projection.percents_ultimate)

        benchmark_parameters_df  = hx.params.table_benchmarkclassparameters  
        
        # timer.end("step 1c")
        # timer.start("step 1b")
        # atomic values
        department      = cds.risk_info.department  
        renew_incept    = hxd.hx_core.inception_date
        renew_expiry    = hxd.hx_core.expiry_date
        cy_yoa          = hxd.hx_core.inception_date.year 
        cy_mth          = hxd.hx_core.inception_date.month
        cy_day          = hxd.hx_core.inception_date.day
        leap_day       = True if (hxd.hx_core.inception_date.month == 2 and hxd.hx_core.inception_date.day == 29) else False
        specialty_lines = (department=="Specialty Lines")

        # get fx for translating threshold
        currency_rates_df   = hx.params.table_currencyrates
        fx_rate_usd_row     = currency_rates_df[ (currency_rates_df['Currency'] == "USD") ]
        fx_rate_sett_row    = currency_rates_df[ (currency_rates_df['Currency'] == cds.currencies.source_currency) ]
        condition_fx        = (fx_rate_usd_row.empty) or (fx_rate_sett_row.empty)   
        fx_rate             = 1 if condition_fx else fx_rate_sett_row.Rate.iat[0] / fx_rate_usd_row.Rate.iat[0]

        # get large loss threshold
        large_threshold_row_df   = benchmark_parameters_df[(benchmark_parameters_df['Item'] == "Large Loss Threshold") 
                                                            & (benchmark_parameters_df['Benchmark Class'] == cds.standard_fields.benchmark_class)]
        large_threshold_usd      = const.dum_large_int   if large_threshold_row_df.empty   else large_threshold_row_df['Value'].iat[0]
        large_threshold_sett_fx  = large_threshold_usd * fx_rate



        # ####################################################################################
        # ### xxx) Example Data Fillers                                                    ###
        # ####################################################################################
        # print('Drop example data fillers: prior_selected_perc_ult')

        rating_df['prior_selected_perc_ult']        = [None]*16
        rating_df['incurred_att_selected_prior']    = [None]*16


        # timer.end("step 1b")
        # timer.end("step 1")
        # timer.start("step 2")

        ####################################################################################
        ### 2) Get Basic Information by year of account                                  ### 
        ####################################################################################
        
        rating_df['yoa']                    = [(cy_yoa - const.default_num_years + x) for x in range(const.default_num_years +1 )] # including current year

        # this is supplemented by an include_weight calculation in section 7 which also draws on premium
        rating_df['include_suggested']           = [ 'Yes'for x in rating_df.yoa]  
        rating_df['include_selected']            = np.where( pd.isnull(rating_df.include_override ),   rating_df.include_suggested,   rating_df.include_override)    


        rating_df['incept_date_empty']      = [ (policy_df[(policy_df.yoa == x) & (policy_df.include)]['inception_date'].empty)    for x in rating_df.yoa]

        rating_df['incept_date']            = [ ( pd.to_datetime(rating_df.yoa[index]*10000 + cy_mth*100 + cy_day - (1 if leap_day else 0), format='%Y%m%d') 
                                                    if rating_df.incept_date_empty[index] 
                                                    else policy_df[(policy_df.yoa == x) & (policy_df.include)]['inception_date'].iat[0])  
                                                    for index,x in enumerate(rating_df.yoa)]

        rating_df['expiry_date']            = [ ( rating_df['incept_date'][index]  +   relativedelta(years = 1, days = -1) 
                                                    if rating_df.incept_date_empty[index] 
                                                    else policy_df[(policy_df.yoa == x) & (policy_df.include)]['expiry_date'   ].iat[0])  
                                                    for index,x in enumerate(rating_df.yoa)]


        # forcing renewal year (last value in array) dates to be per those entered in the main section of the model 
        rating_df['incept_date'].iat[-1]        = renew_incept
        rating_df['expiry_date'].iat[-1]        = renew_expiry

        # converting to pd datetime to facilitate some of the later manipulation e.g. .dt.days needs it
        rating_df['incept_date']            = pd.to_datetime(  rating_df.incept_date  )
        rating_df['expiry_date']            = pd.to_datetime(  rating_df.expiry_date  )

        # remove 1 day and then add one year to imply expiry date if annual policy was assumed
        rating_df['expiry_date_annual_est'] = rating_df.incept_date + pd.offsets.DateOffset(years=1) - pd.offsets.DateOffset(days=1)
       
        # policy length including override
        rating_df['policy_length_calc']     = ( (rating_df.expiry_date              - rating_df.incept_date).dt.days
                                                /(rating_df.expiry_date_annual_est  - rating_df.incept_date).dt.days)
        
        rating_df['policy_length_calc']     = np.where(  pd.isnull(rating_df['policy_length_calc']) ,   1,   rating_df['policy_length_calc']) # forcing a default assumption of 1 if uw want to infill back years

        rating_df['policy_length_selected'] = np.where(  pd.isnull(rating_df.policy_length_override) 
                                                        , rating_df.policy_length_calc
                                                        , np.where( (rating_df.policy_length_override <= 0)
                                                                    ,   rating_df.policy_length_calc
                                                                    ,   rating_df.policy_length_override))

        cy_policy_length                    = rating_df.policy_length_selected.iat[-1]
        rating_df['policy_length_scalant']  = np.where(  (rating_df.policy_length_selected == 0)
                                                        , 0
                                                        , np.where((rating_df.policy_length_selected.isnull())
                                                                    , 0
                                                                    , cy_policy_length /  rating_df.policy_length_selected.astype(float)))


        #policy maturity - note the second line of maturity code tweaks for non-annual policies
        data_eval_date                      = pd.to_datetime( cds.risk_info.final_data_asat )

        rating_df['maturity']               = ( (data_eval_date - rating_df.incept_date).dt.days  / 365      - (rating_df.policy_length_selected - 1) * 0.5) 
                                                
        cds.rating_summary.message_excluded_years = "Please provide rationale in Comments box below for excluding a year." if (rating_df.include_selected == "Yes").count()>0 else ""



        # timer.end("step 2")
        # timer.start("step 3")
        ####################################################################################
        ### 3) Get Portfolio Change Statistics by year of account                        ###
        ####################################################################################
        #benchmark - load, filter and check available
        port_chg_df         = hx.params.table_portfoliochange
        port_chg_rows_df    = port_chg_df[ port_chg_df['Benchmark Class'] ==  cds.standard_fields.benchmark_class]
        port_chg_check      = port_chg_rows_df.empty
        
        # calculate incremental change
        rating_df['port_chg_suggested']           = [ (1 if port_chg_check else     ( port_chg_rows_df[(port_chg_rows_df['Year'] == x) ]['Value'].iat[0]))       for x in rating_df.yoa]
        rating_df['port_chg_selected']            = np.where( pd.isnull(rating_df.port_chg_override )  
                                                                , rating_df.port_chg_suggested   
                                                                , np.where((rating_df.port_chg_override <= 0)
                                                                            , rating_df.port_chg_suggested   
                                                                            , rating_df.port_chg_override))

        # calculate cumulative change
        rating_df['port_chg_cumul_prior']         = rating_df.port_chg_prior[::-1].fillna(1).cumprod()[::-1]       / rating_df.port_chg_prior.fillna(1)      # [::-1] reverses the series order - notice we do it at start and end
        rating_df['port_chg_cumul_suggested']     = rating_df.port_chg_suggested[::-1].fillna(1).cumprod()[::-1]   / rating_df.port_chg_suggested.fillna(1)  # [::-1] reverses the series order - notice we do it at start and end 
        rating_df['port_chg_cumul_selected']      = rating_df.port_chg_selected[::-1].fillna(1).cumprod()[::-1]    / rating_df.port_chg_selected.fillna(1)   # [::-1] reverses the series order - notice we do it at start and end            
       


        # timer.end("step 3")
        # timer.start("step 4")
        ####################################################################################
        ### 4) Get Rate Change Change Statistics by year of account                      ###
        ####################################################################################
        #benchmark - load, filter and check available
        rate_chg_df         = hx.params.table_ratechange
        rate_chg_rows_df    = rate_chg_df[ rate_chg_df['Benchmark Class'] ==  cds.standard_fields.benchmark_class]
        rate_chg_check      = rate_chg_rows_df.empty
        
        # calculate incremental change
        rating_df['rate_chg_premium']        = [ ( policy_df[(policy_df.yoa == x) & (policy_df.include) ]['net_100pct_premium_sett_fx'       ].sum())     for x in rating_df.yoa]
        rating_df['rate_chg_premium_expadj'] = [ ( policy_df[(policy_df.yoa == x) & (policy_df.include) ]['net_100pct_premium_adjexp_sett_fx'].sum())     for x in rating_df.yoa]
        rating_df['rate_chg_portfolio']      = [ (1 if rate_chg_check else     ( rate_chg_rows_df[(rate_chg_rows_df['Year'] == x) ]['Value'].iat[0]))       for x in rating_df.yoa]
        rating_df['rate_chg_account']        = np.where( rating_df.rate_chg_premium_expadj==0  ,   1                              ,  (rating_df.rate_chg_premium / rating_df.rate_chg_premium_expadj))
        rating_df['rate_chg_suggested']      = np.where( rating_df.rate_chg_premium_expadj==0  ,   rating_df['rate_chg_portfolio'],  rating_df.rate_chg_account )
        rating_df['rate_chg_selected']       = np.where( pd.isnull(rating_df.rate_chg_override)
                                                        ,  rating_df.rate_chg_suggested  
                                                        ,  np.where( rating_df.rate_chg_override  <= 0
                                                                    ,  rating_df.rate_chg_suggested   
                                                                    ,  rating_df.rate_chg_override))

        # calculate cumulative change
        rating_df['rate_chg_cumul_prior']    = rating_df.rate_chg_prior[::-1].fillna(1).cumprod()[::-1]     / rating_df.rate_chg_prior.fillna(1)        # [::-1] reverses the series order - notice we do it at start and end
        rating_df['rate_chg_cumul_suggested']= rating_df.rate_chg_suggested[::-1].fillna(1).cumprod()[::-1] / rating_df.rate_chg_suggested.fillna(1)    # [::-1] reverses the series order - notice we do it at start and end 
        rating_df['rate_chg_cumul_selected'] = rating_df.rate_chg_selected[::-1].fillna(1).cumprod()[::-1]  / rating_df.rate_chg_selected.fillna(1)     # [::-1] reverses the series order - notice we do it at start and end 



        # timer.end("step 4")
        # timer.start("step 5")
        ####################################################################################
        ### 5) Get Inflation Statistics by year of account                               ###
        ####################################################################################
        #benchmark - load, filter and check available
        infl_chg_df         = hx.params.table_inflationchange
        infl_chg_rows_df    = infl_chg_df[ infl_chg_df['Benchmark Class'] ==  cds.standard_fields.benchmark_class]
        infl_chg_check      = infl_chg_rows_df.empty
        
        # calculate incremental change
        rating_df['infl_chg_suggested']           = [ (1 if infl_chg_check else     ( infl_chg_rows_df[(infl_chg_rows_df['Year'] == x) ]['Value'].iat[0]))       for x in rating_df.yoa]
        rating_df['infl_chg_selected']            = np.where( pd.isnull(rating_df.infl_chg_override )
                                                                , rating_df.infl_chg_suggested   
                                                                , np.where((rating_df.infl_chg_override < 0)
                                                                            , rating_df.infl_chg_suggested   
                                                                            , rating_df.infl_chg_override))

        # calculate cumulative change
        rating_df['infl_chg_cumul_prior']         = rating_df.infl_chg_prior[::-1].fillna(0).add(1).cumprod()[::-1]       / rating_df.infl_chg_prior.fillna(0).add(1)      # [::-1] reverses the series order - notice we do it at start and end
        rating_df['infl_chg_cumul_suggested']     = rating_df.infl_chg_suggested[::-1].fillna(0).add(1).cumprod()[::-1]   / rating_df.infl_chg_suggested.fillna(0).add(1)  # [::-1] reverses the series order - notice we do it at start and end 
        rating_df['infl_chg_cumul_selected']      = rating_df.infl_chg_selected[::-1].fillna(0).add(1).cumprod()[::-1]    / rating_df.infl_chg_selected.fillna(0).add(1)   # [::-1] reverses the series order - notice we do it at start and end            
 
     

        # timer.end("step 5")
        # timer.start("step 6")
        ####################################################################################
        ### 6) Get Development Statistics by Year of Account                             ###
        ####################################################################################

        # load triangles are being used:
        if cds.risk_info.tri_modelling_required == "Yes":
    
            # load modelling from triangle
            rating_df['experience_default_perc_ult']    = perc_ult_df.experience_default_perc_ult[::-1].reset_index(drop=True) 
            rating_df['experience_selected_perc_ult']   = perc_ult_df.experience_selected_perc_ult[::-1].reset_index(drop=True)
            rating_df['benchmark_default_perc_ult']     = perc_ult_df.benchmark_default_perc_ult[::-1].reset_index(drop=True)
            rating_df['benchmark_selected_perc_ult']    = perc_ult_df.benchmark_selected_perc_ult[::-1].reset_index(drop=True)
            rating_df['blended_default_perc_ult']       = perc_ult_df.blended_default_perc_ult[::-1].reset_index(drop=True)
            rating_df['blended_selected_perc_ult']      = perc_ult_df.blended_selected_perc_ult[::-1].reset_index(drop=True)
            rating_df['initial_qtr_perc_ult']           = perc_ult_df.development_qtr[::-1].reset_index(drop=True)

            # interpolate from annual triangles for any differences in as at position
            f                                            = interp1d(rating_df.initial_qtr_perc_ult, rating_df.blended_selected_perc_ult, fill_value="extrapolate")
            rating_df['interp_blended_selected_perc_ult']= f(rating_df.maturity.astype(float)  *4 )
            rating_df['interp_blended_selected_perc_ult']= np.where(rating_df['interp_blended_selected_perc_ult']<0,  0,  rating_df['interp_blended_selected_perc_ult'])
            rating_df['interp_blended_selected_perc_ult']= rating_df['interp_blended_selected_perc_ult'].fillna(1)

        else:
             # load benchmark factors directly where no triangle modelling being utilised
            bench_all_class_idf_df      = hx.params.table_afbdevelopmentpatternsoc if cds.triangle_projection.benchmark_use_occurrence else hx.params.table_afbdevelopmentpatterns
            idf_df                      = bench_all_class_idf_df[  (bench_all_class_idf_df['Benchmark Class'] == cds.standard_fields.benchmark_class)  ].copy()
            if idf_df.empty == False:
                f                                                = interp1d(idf_df.qtr, idf_df.value, fill_value="extrapolate")
                rating_df['interp_blended_selected_perc_ult']    = f(rating_df.maturity.astype(float)  *4)
                rating_df['interp_blended_selected_perc_ult']    = np.where(rating_df['interp_blended_selected_perc_ult']<0,  0,  rating_df['interp_blended_selected_perc_ult'])
            else:
                rating_df['interp_blended_selected_perc_ult']    = 1







        # timer.end("step 6")
        # timer.start("step 7")
        ####################################################################################
        ### 7) Get Premium Statistics by Year of Account & include status                ###
        ####################################################################################
        rating_df['premium_suggested']           = [ ( policy_df[(policy_df.yoa == x) & (policy_df.include)  ]['gross_100pct_premium_sett_fx'].sum())     for x in rating_df.yoa]
        rating_df['premium_selected']            = np.where( pd.isnull(rating_df.premium_override )  
                                                            , rating_df.premium_suggested
                                                            , np.where((rating_df.premium_override < 0) 
                                                                        ,   rating_df.premium_suggested
                                                                        ,   rating_df.premium_override))
        
        ## calculating premium: suggested, selected, onleveled (ol), scaled
        rating_df['premium_selected_ol']        = rating_df.premium_selected     *   rating_df.rate_chg_cumul_selected
        rating_df['premium_selected_ol_scaled'] = rating_df.premium_selected_ol  *   rating_df.policy_length_scalant


        ## this follows on from the include calculation shown in section 2 - show here due to premium dependency
        rating_df['include_selected_weight']     = np.where( (      (rating_df.include_selected == "Yes") 
                                                                    & (rating_df.premium_selected !=0   ) 
                                                                    & (rating_df.index != 15            ))   #exclude current year
                                                            , 1
                                                            , 0)   



        # timer.end("step 7")
        # timer.start("step 8")

        ############################################################################################
        ### 8) Get Incurred Statistics by Year of Account - including initial manipulation       ###
        ############################################################################################

        # filtering out loss funds and any anomalies
        options = ['ATT', 'LARGE', 'CAT'] 
        claim_df = claim_df.loc[  claim_df['loss_category'].isin(options)  ]

        # building the amount columns we want populating
        amt_columns = ['paid_listing'
                        ,'incurred_listing'  
                        ,'incurred_pp_blend'
                        ,'incurred_pp_most_likely'  
                        
                        ,'paid_large_listing'  
                        ,'incurred_large_listing'  
                        ,'incurred_large_pp_blend'  
                        ,'incurred_large_pp_most_likely'  
                        
                        ,'paid_cat_listing'  
                        ,'incurred_cat_listing'  
                        ,'incurred_cat_pp_blend'  
                        ,'incurred_cat_pp_most_likely'

                        ,'paid_att_listing'  
                        ,'incurred_att_listing'  
                        ,'incurred_att_pp_blend'  
                        ,'incurred_att_pp_most_likely'  
                        ]

        # setting amt_columns to nil initially
        claim_df.loc[:,amt_columns]         = 0
        
        # populating total columns
        if 'bi_paid' in claim_df.columns:                       claim_df['paid_listing']            = claim_df['bi_paid']
        if 'bi_incurred' in claim_df.columns:                   claim_df['incurred_listing']        = claim_df['bi_incurred']
        if 'pre_peer_blend_incurred' in claim_df.columns:       claim_df['incurred_pp_blend']       = claim_df['pre_peer_blend_incurred']
        if 'pre_peer_most_likely_incurred' in claim_df.columns: claim_df['incurred_pp_most_likely'] = claim_df['pre_peer_most_likely_incurred']

        # populating LARGE columns
        claim_df.loc[claim_df['loss_category']=="LARGE", ['paid_large_listing']]            = claim_df['bi_paid']
        claim_df.loc[claim_df['loss_category']=="LARGE", ['incurred_large_listing']]        = claim_df['bi_incurred']
        claim_df.loc[claim_df['loss_category']=="LARGE", ['incurred_large_pp_blend']]       = claim_df['pre_peer_blend_incurred']
        claim_df.loc[claim_df['loss_category']=="LARGE", ['incurred_large_pp_most_likely']] = claim_df['pre_peer_most_likely_incurred']

        # populating CAT columns
        claim_df.loc[claim_df['loss_category']=="CAT",   ['paid_cat_listing']]              = claim_df['bi_paid']
        claim_df.loc[claim_df['loss_category']=="CAT",   ['incurred_cat_listing']]          = claim_df['bi_incurred']
        claim_df.loc[claim_df['loss_category']=="CAT",   ['incurred_cat_pp_blend']]         = claim_df['pre_peer_blend_incurred']
        claim_df.loc[claim_df['loss_category']=="CAT",   ['incurred_cat_pp_most_likely']]   = claim_df['pre_peer_most_likely_incurred']

        # populating ATT columns
        claim_df.loc[claim_df['loss_category']=="ATT",   ['paid_att_listing']]              = claim_df['bi_paid']
        claim_df.loc[claim_df['loss_category']=="ATT",   ['incurred_att_listing']]          = claim_df['bi_incurred']
        claim_df.loc[claim_df['loss_category']=="ATT",   ['incurred_att_pp_blend']]         = claim_df['pre_peer_blend_incurred']
        claim_df.loc[claim_df['loss_category']=="ATT",   ['incurred_att_pp_most_likely']]   = claim_df['pre_peer_most_likely_incurred']

        # claim_df forcing yoa to be int64 consistent with rating_df
        claim_df['yoa']                 = claim_df['yoa'].astype('Int64') 

        # claim_df grouping on yoa and dropping extra columns
        claim_df.loc[:,amt_columns]     = claim_df.loc[:,amt_columns].astype(float)                 # needed as if an amount is not assigned above they are object type which gets dropped in the sum
        claim_df                        = claim_df.groupby(['yoa'], as_index=False)[amt_columns].sum()  

        # dropping amt_columns from rating_df
        rating_df = rating_df.drop(amt_columns, axis=1)
        
        # adding amt_columns to rating_df from claim_df using a left join 
        rating_df = rating_df.merge(claim_df, on='yoa', how='left')
        
        # defaulting amt columns to zero if na
        rating_df.loc[:,amt_columns] = rating_df.loc[:,amt_columns].fillna(0)

        # loading incurred triangle data from claim_mvmt_df
        rating_df['incurred_triangle']       = [ ( claim_mvmt_df[ (claim_mvmt_df.yoa == x) ]['incurredmvmt_100_sett_fx'     ].sum())   for x in rating_df.yoa]

        # Jess C email 24072024: For Specialty: [BeazleyShareTotalIncurred] to be used in attritional calcs; [BeazleySharePrePeerBlend] – to be used in large and cat calcs  {note we use these at 100pct}
        # since this means we will be blending two sources here at the total level we do the individual calculation -large/cat/att and then aggregate

        # large loss statistics
        large_m = (claim_mvmt_df.loss_category=="LARGE")
        rating_df['incurred_large_triangle']       = [ ( claim_mvmt_df[ large_m & (claim_mvmt_df.yoa == x) ]['incurredmvmt_100_sett_fx' ].sum())   for x in rating_df.yoa]
        rating_df['incurred_large_suggested']= np.where( specialty_lines  , rating_df.incurred_large_pp_blend
                                                                          , rating_df.incurred_large_triangle if cds.bi_data.triangles_loaded else rating_df.incurred_large_listing)

        # cat loss statistics
        cat_m = (claim_mvmt_df.loss_category=="CAT")
        rating_df['incurred_cat_triangle']       = [ ( claim_mvmt_df[ cat_m & (claim_mvmt_df.yoa == x) ]['incurredmvmt_100_sett_fx' ].sum())   for x in rating_df.yoa]
        rating_df['incurred_cat_suggested']  = np.where(specialty_lines , rating_df.incurred_cat_pp_blend
                                                                        , rating_df.incurred_cat_triangle  if cds.bi_data.triangles_loaded else rating_df.incurred_cat_listing)

        # att loss statistics
        att_m = (claim_mvmt_df.loss_category=="ATT")
        rating_df['incurred_att_triangle']       = [ ( claim_mvmt_df[ att_m & (claim_mvmt_df.yoa == x) ]['incurredmvmt_100_sett_fx' ].sum())   for x in rating_df.yoa]
        rating_df['incurred_att_suggested']  = rating_df.incurred_att_triangle  if cds.bi_data.triangles_loaded else rating_df.incurred_att_listing

        # total loss statistics
        rating_df['incurred_suggested']      = rating_df['incurred_att_suggested'] + rating_df['incurred_large_suggested'] + rating_df['incurred_cat_suggested']
        rating_df['incurred_selected']       = np.where( pd.isnull(rating_df.incurred_override )  
                                                            , rating_df.incurred_suggested
                                                            , np.where((rating_df.incurred_override < 0)
                                                                        ,   rating_df.incurred_suggested
                                                                        ,   rating_df.incurred_override)      )

        # timer.end("step 8")
        # timer.start("step 9")
        ####################################################################################
        ### 9) Get Large Loss Statistics by year of account                             ###
        ####################################################################################

        # thresholds
        rating_df['large_threshold_usd']            = large_threshold_usd      / rating_df.infl_chg_cumul_selected
        rating_df['large_threshold_sett_fx']        = large_threshold_sett_fx  / rating_df.infl_chg_cumul_selected

        rating_df['incurred_large_selected']       = np.where( pd.isnull(rating_df.incurred_large_override )  
                                                                , rating_df.incurred_large_suggested
                                                                , np.where(  (rating_df.incurred_large_override < 0)
                                                                            ,   rating_df.incurred_large_suggested
                                                                            ,   rating_df.incurred_large_override))

        # .astype(float) was needed here to convert from object so we dont get a div 0 error
        rating_df['incurred_large_selected_lr']    = np.where( (rating_df.premium_selected == 0), 0,  rating_df.incurred_large_selected.astype(float)  /  rating_df.premium_selected.astype(float))   

        rating_df['incurred_large_selected_inflated'] = rating_df.incurred_large_selected   *   rating_df.infl_chg_cumul_selected *  rating_df.port_chg_cumul_selected



        # timer.end("step 9")
        # timer.start("step 10")
        ####################################################################################
        ### 10) Get Cat Loss Statistics by year of account                               ###
        ####################################################################################
                                                                                         
        rating_df['incurred_cat_selected']       = np.where(  pd.isnull(rating_df.incurred_cat_override )  
                                                                , rating_df.incurred_cat_suggested
                                                                , np.where((rating_df.incurred_cat_override < 0)
                                                                            ,   rating_df.incurred_cat_suggested
                                                                            ,   rating_df.incurred_cat_override  ))

        # .astype(float) was needed here to convert from object so we dont get a div 0 error
        rating_df['incurred_cat_selected_lr']    = np.where( (rating_df.premium_selected == 0), 0,  rating_df.incurred_cat_selected.astype(float)  /  rating_df.premium_selected.astype(float))   

        rating_df['incurred_cat_selected_inflated'] = rating_df.incurred_cat_selected   *   rating_df.infl_chg_cumul_selected



        # timer.end("step 10")
        # timer.start("step 11")
        ####################################################################################
        ### 11) Get Attitional Loss Statistics by year of account                        ###
        ####################################################################################

        rating_df['incurred_att_selected']       = rating_df['incurred_selected']  -  rating_df['incurred_large_selected']  -  rating_df['incurred_cat_selected']

        rating_df['incurred_att_override']       = rating_df['incurred_att_selected'] 

        # .astype(float) was needed here to convert from object so we dont get a div 0 error
        rating_df['incurred_att_selected_lr']    = np.where( (rating_df.premium_selected == 0),  0,  rating_df.incurred_att_selected.astype(float)  /  rating_df.premium_selected.astype(float))   

        rating_df['incurred_att_selected_inflated'] = rating_df.incurred_att_selected   *   rating_df.infl_chg_cumul_selected



        # timer.end("step 11")
        # timer.start("step 12")
        ########################################################################################
        ### 12) Calculate Attritional Loss Ultimates   - stage 1 - get Chainladder ultimates ###
        ########################################################################################

        ## shortforms: on-level (ol); prior year (py); chainladder (cl)


        ## calculating attritional losses in nominal terms - starting from everything on this years basis and stripping back to prior year (py) - by dev, then data
        rating_df['ultimate_att_cl_selected']                 = np.where( (rating_df.interp_blended_selected_perc_ult == 0), 0,  rating_df.incurred_att_selected.astype(float)       /  rating_df.interp_blended_selected_perc_ult.astype(float))

        rating_df['ultimate_att_cl_selected_py_factors']      = np.where( (rating_df.prior_selected_perc_ult == 0), 0,    rating_df.incurred_att_selected.astype(float)       /  rating_df.prior_selected_perc_ult.astype(float))   # notice the formula doesnt try to adjust for the different maturity - question???    

        rating_df['ultimate_att_cl_selected_py_factors_data'] = np.where( (rating_df.prior_selected_perc_ult == 0), 0,    rating_df.incurred_att_selected_prior.astype(float) /  rating_df.prior_selected_perc_ult.astype(float))
        

        ## calculating attritional losses on-leveled (ol) - starting from everything on this years basis and stripping back to prior year (py) - by onlevel, then dev, then data
        ## selected     
        rating_df['ultimate_att_cl_selected_ol']                 = (rating_df.ultimate_att_cl_selected            * rating_df.policy_length_scalant     * rating_df.port_chg_cumul_selected  * rating_df.infl_chg_cumul_selected)

        ## selected - no scalant - separate calc needed, but not main approach
        rating_df['ultimate_att_cl_selected_ol_exc_scalant']     = (rating_df.ultimate_att_cl_selected                                                  * rating_df.port_chg_cumul_selected  * rating_df.infl_chg_cumul_selected)

        ## selected on last times on-levelling
        rating_df['ultimate_att_cl_selected_ol_py_ol_assump']    = (rating_df.ultimate_att_cl_selected            * rating_df.policy_length_scalant     * rating_df.port_chg_cumul_prior     * rating_df.infl_chg_cumul_prior)

        ## selected on last times on-levelling & development
        rating_df['ultimate_att_cl_selected_ol_py_factors']      = (rating_df.ultimate_att_cl_selected_py_factors * rating_df.policy_length_scalant     * rating_df.port_chg_cumul_prior     * rating_df.infl_chg_cumul_prior)

        ## selected on last times on-levelling, development & data
        rating_df['ultimate_att_cl_selected_ol_py_factors_data'] = (rating_df.ultimate_att_cl_selected_py_factors_data * rating_df.policy_length_scalant* rating_df.port_chg_cumul_prior     * rating_df.infl_chg_cumul_prior)

 

       
        # timer.end("step 12")
        # timer.start("step 13")
        ##############################################################################################
        ### 13) Calculate Attritional Loss Ultimates   - stage 2 - get Reserving Method & aprioris ###
        ##############################################################################################

        ## get reserving method to apply
        all_class_method_att_cred_df                = hx.params.table_attritionalcredibility
        benchmark_method_att_cred_df                = all_class_method_att_cred_df[   (all_class_method_att_cred_df['Benchmark Class'] == cds.standard_fields.benchmark_class)   ]
        rating_df['reserving_method_attritional']   = [ ("IELR" if pd.isnull(x) else benchmark_method_att_cred_df[benchmark_method_att_cred_df['Percent Ultimate'] <= x]['Value'].iloc[-1] )
                                                            for x in rating_df.interp_blended_selected_perc_ult]


        ## getting experience weight
        single_value_df = hx.params.table_singlevalues
        max_premium_usd = single_value_df[single_value_df['Field'] == "Maximum premium credibility"]['Value'].iat[0]   /1000
        min_premium_usd = single_value_df[single_value_df['Field'] == "Min premium credibility"]['Value'].iat[0]       /1000
        min_year_cred   = 1
        max_year_cred   = single_value_df[single_value_df['Field'] == "Max years credibility"]['Value'].iat[0]       /1000

        max_exper_weight= single_value_df[single_value_df['Field'] == "Maximum Experience Weight"]['Value'].iat[0] 
        min_attr_GG_LR = single_value_df[single_value_df['Field'] == "Min Attr GG ULR"]['Value'].iat[0] 
        min_large_GG_LR = single_value_df[single_value_df['Field'] == "Min Large GG ULR"]['Value'].iat[0] 
        min_cat_GG_LR = single_value_df[single_value_df['Field'] == "Min Cat GG ULR"]['Value'].iat[0] 

        gg_premium_sett             = rating_df.premium_selected.sum() /1000
        gg_premium_usd              = gg_premium_sett   /  fx_rate
        gg_premium_constrained_usd  = min(max_premium_usd,    max(min_premium_usd,  gg_premium_usd))

        num_years_include           = max(1,   rating_df.include_selected_weight.sum() )
        num_years_constrained       = min(max_year_cred,    max(min_year_cred,  num_years_include))

        large_credibility_df = hx.params.table_largecredibility                                                    #notice we use experience_weight from "LARGE_credibility_df" for both attritional (here) and large (further down)

        conditions =( (large_credibility_df['Benchmark Class']  ==  cds.standard_fields.benchmark_class )
                     & (large_credibility_df['written_premium'] <=  gg_premium_constrained_usd)
                     & (large_credibility_df['num_yr_data']     <=  num_years_include))
       
        experience_weight = large_credibility_df[conditions]['Value'].iat[-1]
        experience_weight = min(  experience_weight,  max_exper_weight)


        ## getting experience apriori
        experience_loss_cost = np.where( (rating_df.reserving_method_attritional == "CL"),   rating_df.include_selected_weight *  rating_df.ultimate_att_cl_selected_ol,   0).sum() 
        chain_Ladder_count = np.where( (rating_df.reserving_method_attritional == "CL"),   rating_df.include_selected_weight,   0).sum() 
        experience_loss_cost = 0 if np.isnan(experience_loss_cost) else experience_loss_cost
        experience_premium   = np.where( (rating_df.reserving_method_attritional == "CL"),   rating_df.include_selected_weight *  rating_df.premium_selected_ol_scaled,  0).sum()
        experience_apriori   = 0   if (experience_premium ==0)    else experience_loss_cost / experience_premium


        ## getting benchmark apriori
        benchmark_row_df     = benchmark_parameters_df[(benchmark_parameters_df['Item'] == "Att LR") 
                                                            & (benchmark_parameters_df['Benchmark Class'] == cds.standard_fields.benchmark_class)]
        
        benchmark_apriori    = 0  if benchmark_row_df.empty   else benchmark_row_df['Value'].iat[0]             #gross net LR
        total_deductions     = (cds.layers[0].total_deductions or 0)
        benchmark_apriori    = benchmark_apriori * (1 -     total_deductions )                            #gross gross LR

        ## blended apriori
        experience_weight = 0 if  chain_Ladder_count ==0 else experience_weight
        
        selected_apriori     = experience_apriori * experience_weight   +   benchmark_apriori * (1 - experience_weight)
        
        ## passing to hxd
        att.gg_pre_uw_adj.ulr_initial_benchmark             = benchmark_apriori
        att.gg_pre_uw_adj.ulr_initial_experience            = experience_apriori
        att.gg_pre_uw_adj.ulr_initial_experience_weighting  = experience_weight
        att.gg_pre_uw_adj.ulr_initial_selected              = selected_apriori

        att.gn_pre_uw_adj.ulr_initial_benchmark             = benchmark_apriori     /  (1 -     total_deductions )
        att.gn_pre_uw_adj.ulr_initial_experience            = experience_apriori    /  (1 -     total_deductions )
        att.gn_pre_uw_adj.ulr_initial_experience_weighting  = experience_weight
        att.gn_pre_uw_adj.ulr_initial_selected              = selected_apriori      /  (1 -     total_deductions )



        # timer.end("step 13")
        # timer.start("step 14")
        #############################################################################################
        ### 14) Calculate Attritional Loss Ultimates   - stage 3 - apply Reserving Method         ###
        #############################################################################################

        ## selected     
        rating_df['ultimate_att_meth_selected_ol']                                                          = (  rating_df.ultimate_att_cl_selected_ol)
        rating_df.loc[rating_df['reserving_method_attritional'] == "IELR", 'ultimate_att_meth_selected_ol'] = (  rating_df.premium_selected_ol_scaled  *  selected_apriori)
        rating_df.loc[rating_df['reserving_method_attritional'] == "BF",   'ultimate_att_meth_selected_ol'] = (  rating_df.premium_selected_ol_scaled  *  selected_apriori * (1 - rating_df.interp_blended_selected_perc_ult)
                                                                                                               + rating_df.ultimate_att_cl_selected_ol                     * (rating_df.interp_blended_selected_perc_ult))


        ## selected - no scalant
        rating_df['ultimate_att_meth_selected_ol_exc_scalant']                                                          = (  rating_df.ultimate_att_cl_selected_ol_exc_scalant)
        rating_df.loc[rating_df['reserving_method_attritional'] == "IELR", 'ultimate_att_meth_selected_ol_exc_scalant'] = (  rating_df.premium_selected_ol_scaled  *  selected_apriori)
        rating_df.loc[rating_df['reserving_method_attritional'] == "BF",   'ultimate_att_meth_selected_ol_exc_scalant'] = (  rating_df.premium_selected_ol_scaled  *  selected_apriori  * (1 - rating_df.interp_blended_selected_perc_ult)
                                                                                                                           + rating_df.ultimate_att_cl_selected_ol_exc_scalant          * (rating_df.interp_blended_selected_perc_ult))


        ## selected on last times on-levelling
        rating_df['ultimate_att_meth_selected_ol_py_ol_assump']                                                          = (  rating_df.ultimate_att_cl_selected_ol_py_ol_assump)
        rating_df.loc[rating_df['reserving_method_attritional'] == "IELR", 'ultimate_att_meth_selected_ol_py_ol_assump'] = (  rating_df.premium_selected_ol_scaled  *  selected_apriori)
        rating_df.loc[rating_df['reserving_method_attritional'] == "BF",   'ultimate_att_meth_selected_ol_py_ol_assump'] = (  rating_df.premium_selected_ol_scaled  *  selected_apriori * (1 - rating_df.interp_blended_selected_perc_ult)
                                                                                                                            + rating_df.ultimate_att_cl_selected_ol_py_ol_assump        * (rating_df.interp_blended_selected_perc_ult))


        ## selected on last times on-levelling & development
        rating_df['ultimate_att_meth_selected_ol_py_factors']                                                          = (  rating_df.ultimate_att_cl_selected_ol_py_factors)
        rating_df.loc[rating_df['reserving_method_attritional'] == "IELR", 'ultimate_att_meth_selected_ol_py_factors'] = (  rating_df.premium_selected_ol_scaled  *  selected_apriori)
        rating_df.loc[rating_df['reserving_method_attritional'] == "BF",   'ultimate_att_meth_selected_ol_py_factors'] = (  rating_df.premium_selected_ol_scaled  *  selected_apriori * (1 - rating_df.interp_blended_selected_perc_ult)
                                                                                                                            + rating_df.ultimate_att_cl_selected_ol_py_factors        * (rating_df.interp_blended_selected_perc_ult))


        ## selected on last times on-levelling, development & data
        rating_df['ultimate_att_meth_selected_ol_py_factors_data']                                                          = (  rating_df.ultimate_att_cl_selected_ol_py_factors_data)
        rating_df.loc[rating_df['reserving_method_attritional'] == "IELR", 'ultimate_att_meth_selected_ol_py_factors_data'] = (  rating_df.premium_selected_ol_scaled  *  selected_apriori)
        rating_df.loc[rating_df['reserving_method_attritional'] == "BF",   'ultimate_att_meth_selected_ol_py_factors_data'] = (  rating_df.premium_selected_ol_scaled  *  selected_apriori * (1 - rating_df.interp_blended_selected_perc_ult)
                                                                                                                               + rating_df.ultimate_att_cl_selected_ol_py_factors_data     * (rating_df.interp_blended_selected_perc_ult))


        ## weightings

        ##exposure weight
        cy_written_premium                  = cds.layers[0].quoted_premium_100pct #rating_df.premium_selected.iat[-1] 
        rating_df['weighting_exposure']     = 1 if cy_written_premium ==0 else np.where(  rating_df.premium_selected_ol_scaled /cy_written_premium > 1,  1, rating_df.premium_selected_ol_scaled / cy_written_premium)

        ##decay weight
        decay_row_df                        = benchmark_parameters_df[(benchmark_parameters_df['Item'] == "Decay Factor") 
                                                                     & (benchmark_parameters_df['Benchmark Class'] == cds.standard_fields.benchmark_class)]
        decay_factor                        = 1   if decay_row_df.empty   else decay_row_df['Value'].iat[0] 
        rating_df['weighting_decay']        = [ ((decay_factor ** (cy_yoa -1 - x))      if x != cy_yoa else 0)     for x in rating_df.yoa]

        ##development weight
        rating_df['weighting_development']  = rating_df.interp_blended_selected_perc_ult

        ##combined weight
        rating_df['weighting_combined']     = (     rating_df.weighting_exposure       *   rating_df.weighting_decay    
                                                *   rating_df.weighting_development    *   rating_df.include_selected_weight)

        ##final weight after rebalancing
        total_weighting_combined            = rating_df.weighting_combined.sum()
        rating_df['weighting_final']        = 1 if total_weighting_combined ==0 else rating_df.weighting_combined  /  total_weighting_combined



        # timer.end("step 14")
        # timer.start("step 15")
        ####################################################################################
        ### 15) Calculate Attritional Loss Load Metrics including Scenarios   - pre UW ADJ       ###
        ####################################################################################

        ## take ulr_previous_override where populated othewise look at ulr_uw_override and if that is not filled in use ulr_previous
        att.gg_pre_uw_adj.ulr_previous_selected_inferred  = (att.gg_pre_uw_adj.ulr_previous_override   or   att.gg_pre_uw_adj.ulr_uw_override   or   att.gg_pre_uw_adj.ulr_previous)

        ## calc total weighted premium
        py_premium_total                                    =  (rating_df.weighting_final   *   rating_df.include_selected_weight  *   rating_df.premium_selected_ol_scaled).sum()

        ## ulr on last times on-levelling, development & data
        att.gg_pre_uw_adj.ulr_selected_ol_py_factors_data   = ( 0 if py_premium_total == 0   else  
                                                                    (rating_df.weighting_final   *   rating_df.include_selected_weight  *   rating_df.ultimate_att_meth_selected_ol_py_factors_data).sum()  / py_premium_total)

        ## ulr on last times on-levelling & development
        att.gg_pre_uw_adj.ulr_selected_ol_py_factors        = ( 0 if py_premium_total == 0   else  
                                                                    (rating_df.weighting_final   *   rating_df.include_selected_weight  *   rating_df.ultimate_att_meth_selected_ol_py_factors).sum()       / py_premium_total)
        
        ## selected on last times on-levelling
        att.gg_pre_uw_adj.ulr_selected_ol_py_ol_assump      = ( 0 if py_premium_total == 0   else  
                                                                     (rating_df.weighting_final   *   rating_df.include_selected_weight  *   rating_df.ultimate_att_meth_selected_ol_py_ol_assump).sum()    / py_premium_total)
        
        ## selected - no scalant or if not available use initial selected_apriori
        att.gg_pre_uw_adj.ulr_selected_ol_exc_scalant       =( selected_apriori if py_premium_total == 0   else  
                                                                    ( rating_df.weighting_final   *   rating_df.include_selected_weight  *   rating_df.ultimate_att_meth_selected_ol_exc_scalant).sum()     / py_premium_total)
                                                              

        ## selected or if not available use initial selected_apriori
        att.gg_pre_uw_adj.ulr_selected_ol                   =( selected_apriori if py_premium_total == 0   else  
                                                                    (rating_df.weighting_final   *   rating_df.include_selected_weight  *   rating_df.ultimate_att_meth_selected_ol).sum()                  / py_premium_total)

        
         
      
        # there is no override during the experince rating anymore as the override are post any blend.

        # assigning to the actuarial output lr where an input exists - always conditioning on gg_pre_uw_adj
        #if pd.isnull(att.gg_pre_uw_adj.ulr_actuarial_override) == False:   att.gg_pre_uw_adj.ulr_actuarial_override_output  = att.gg_pre_uw_adj.ulr_actuarial_override

        ## determining final loss ratio
        #att.gg_pre_uw_adj.ulr_final                         = (att.gg_pre_uw_adj.ulr_final_uw    if pd.isnull(att.gg_pre_uw_adj.ulr_actuarial_override) 
        #                                                                                        else att.gg_pre_uw_adj.ulr_actuarial_override) 


        att.gg_pre_uw_adj.ulr_final = max(att.gg_pre_uw_adj.ulr_selected_ol,min_attr_GG_LR)


        ## assigning to equivalent gross net, pre uw adjustments elements of hxd
        att.gn_pre_uw_adj.ulr_previous                      =(att.gg_pre_uw_adj.ulr_previous or 0)                       /  (1 -    total_deductions )
        att.gn_pre_uw_adj.ulr_previous_override             =(att.gg_pre_uw_adj.ulr_previous_override or 0)              /  (1 -    total_deductions )
        att.gn_pre_uw_adj.ulr_previous_suggested            =(att.gg_pre_uw_adj.ulr_previous_suggested or 0)             /  (1 -    total_deductions )
        att.gn_pre_uw_adj.ulr_previous_selected_inferred    =(att.gg_pre_uw_adj.ulr_previous_selected_inferred or 0)     /  (1 -    total_deductions )
        att.gn_pre_uw_adj.ulr_selected_ol_py_factors_data   = att.gg_pre_uw_adj.ulr_selected_ol_py_factors_data          /  (1 -    total_deductions )
        att.gn_pre_uw_adj.ulr_selected_ol_py_factors        = att.gg_pre_uw_adj.ulr_selected_ol_py_factors               /  (1 -    total_deductions )
        att.gn_pre_uw_adj.ulr_selected_ol_py_ol_assump      = att.gg_pre_uw_adj.ulr_selected_ol_py_ol_assump             /  (1 -    total_deductions )
        att.gn_pre_uw_adj.ulr_selected_ol_exc_scalant       = att.gg_pre_uw_adj.ulr_selected_ol_exc_scalant              /  (1 -    total_deductions )
        att.gn_pre_uw_adj.ulr_selected_ol                   = att.gg_pre_uw_adj.ulr_selected_ol                          /  (1 -    total_deductions )
        att.gn_pre_uw_adj.ulr_uw_override                   = (att.gg_pre_uw_adj.ulr_uw_override or 0)                   /  (1 -    total_deductions )
        att.gn_pre_uw_adj.ulr_actuarial_override            = (att.gg_pre_uw_adj.ulr_actuarial_override or 0)            /  (1 -    total_deductions )
        att.gn_pre_uw_adj.ulr_final                         = att.gg_pre_uw_adj.ulr_final                                /  (1 -    total_deductions )



        

       






        # timer.end("step 15")
        # timer.start("step 16")
        ####################################################################################
        ### 16) Calculate Large Loss Load Metrics       - pre UW ADJ                      ###
        ####################################################################################

        ## getting benchmark apriori
        benchmark_row_df     = benchmark_parameters_df[(benchmark_parameters_df['Item'] == "Large LR") 
                                                     & (benchmark_parameters_df['Benchmark Class'] == cds.standard_fields.benchmark_class)]
        
        ## GROSS NET - benchmark ULR
        lrg.gn_pre_uw_adj.ulr_benchmark             = 0  if benchmark_row_df.empty   else benchmark_row_df['Value'].iat[0]             #gross net LR

        ## GROSS GROSS - benchmark ULR
        lrg.gg_pre_uw_adj.ulr_benchmark             = lrg.gn_pre_uw_adj.ulr_benchmark    *    (1 -     total_deductions)

        ## GROSS GROSS - experience ULR - notice no ibnr - flagged for day 2 fix
        lrg.gg_pre_uw_adj.ulr_experience            = (0 if (   (rating_df.include_selected_weight  *   rating_df.premium_selected_ol).sum() == 0   ) else
                                                                    (  (rating_df.include_selected_weight  *   rating_df.incurred_large_selected_inflated).sum()
                                                                    / (rating_df.include_selected_weight  *   rating_df.premium_selected_ol).sum()))             

        ## GROSS GROSS - experience weighting is same as that used for attritional
        lrg.gg_pre_uw_adj.ulr_experience_weighting  = att.gg_pre_uw_adj.ulr_initial_experience_weighting 

        ## GROSS GROSS - selected ULR (blended)
        lrg.gg_pre_uw_adj.ulr_selected_ol           = (    lrg.gg_pre_uw_adj.ulr_experience  *      lrg.gg_pre_uw_adj.ulr_experience_weighting   
                                                        +  lrg.gg_pre_uw_adj.ulr_benchmark   * (1 - lrg.gg_pre_uw_adj.ulr_experience_weighting  ))

        ## GROSS GROSS - override ULR   - THERE ARE NO OVERRIDES AT THIS POINT ANYMORE - AC
        #if lrg.uw_override: 
        #    lrg.gg_pre_uw_adj.ulr_uw_override          = 0 

        ## final uw ulr allowing for overrides - notice that the test point is always the INPUT field lrg.gg_pst_uw_adj.ulr_uw_override
        #lrg.gg_pre_uw_adj.ulr_final_uw                 = lrg.gg_pre_uw_adj.ulr_uw_override   if lrg.uw_override else   lrg.gg_pre_uw_adj.ulr_selected_ol 
        
        #lrg.gg_pre_uw_adj.ulr_final                    = (lrg.gg_pre_uw_adj.ulr_final_uw    if pd.isnull(lrg.gg_pre_uw_adj.ulr_actuarial_override) 
        #                                                                                   else lrg.gg_pre_uw_adj.ulr_actuarial_override )

        lrg.gg_pre_uw_adj.ulr_final =  max(lrg.gg_pre_uw_adj.ulr_selected_ol,min_large_GG_LR)

        # assigning to the actuarial output lr where an input exists - always conditioning on gg_pre_uw_adj - THERE ARE NO OVERRIDES AT THIS POINT ANYMORE - AC 
        # if pd.isnull(lrg.gg_pre_uw_adj.ulr_actuarial_override) == False:   lrg.gg_pre_uw_adj.ulr_actuarial_override_output  = lrg.gg_pre_uw_adj.ulr_actuarial_override



        ## assigning to equivalent gross net, pre uw adjustments elements of hxd
        lrg.gn_pre_uw_adj.ulr_previous              =(lrg.gg_pre_uw_adj.ulr_previous or 0)          /  (1 -    total_deductions)
        lrg.gn_pre_uw_adj.ulr_experience            = lrg.gg_pre_uw_adj.ulr_experience              /  (1 -    total_deductions)
        lrg.gn_pre_uw_adj.ulr_experience_weighting  = lrg.gg_pre_uw_adj.ulr_experience_weighting    
        lrg.gn_pre_uw_adj.ulr_selected_ol           = lrg.gg_pre_uw_adj.ulr_selected_ol             /  (1 -    total_deductions)
        #if lrg.uw_override: 
        #    lrg.gn_pre_uw_adj.ulr_uw_override       = 0 
        #lrg.gn_pre_uw_adj.ulr_final_uw              = lrg.gg_pre_uw_adj.ulr_final_uw                /  (1 -    total_deductions)
        #lrg.gn_pre_uw_adj.ulr_actuarial_override    = (lrg.gg_pre_uw_adj.ulr_actuarial_override or 0)/ (1 -    total_deductions)
        lrg.gn_pre_uw_adj.ulr_final                 = lrg.gg_pre_uw_adj.ulr_final                   /  (1 -    total_deductions)

        # assigning to the actuarial output lr where an input exists - always conditioning on gg_pre_uw_adj
        #if pd.isnull(lrg.gg_pre_uw_adj.ulr_actuarial_override) == False:   lrg.gn_pre_uw_adj.ulr_actuarial_override_output  = lrg.gn_pre_uw_adj.ulr_actuarial_override



       


        # timer.end("step 16")
        # timer.start("step 17")
        ####################################################################################
        ### 17) Calculate Cat Loss Load Metrics    - pre UW ADJ                                      ###
        ####################################################################################

        ## getting experience weight
        cat_credibility_df = hx.params.table_catcredibility

        conditions =( (cat_credibility_df['Benchmark Class']  ==  cds.standard_fields.benchmark_class )
                     & (cat_credibility_df['written_premium'] <=  gg_premium_constrained_usd)               # gg_premium_constrained_usd was already calculated under attritional loss calc - identical here
                     & (cat_credibility_df['num_yr_data']     <=  num_years_include))                       # num_years_include was already calculated under attritional loss calc - identical here
       
        cat_experience_weight = 0 if (py_premium_total == 0) else cat_credibility_df[conditions]['Value'].iat[-1]
        cat_experience_weight = min(  cat_experience_weight,  max_exper_weight)                             # max_exper_weight was already calculated under attritional loss calc - identical here


        ## GROSS NET - benchmark ULR for CAT - MODELLED LOSSES
        benchmark_row_df     = benchmark_parameters_df[(benchmark_parameters_df['Item'] == "Cat LR") 
                                                     & (benchmark_parameters_df['Benchmark Class'] == cds.standard_fields.benchmark_class)]
        gnlr_cat_natural     = 0  if benchmark_row_df.empty   else benchmark_row_df['Value'].iat[0]             #gross net LR

        ## GROSS NET - benchmark ULR for CAT - NON MODELLED LOSSES (NML)
        benchmark_row_df     = benchmark_parameters_df[(benchmark_parameters_df['Item'] == "NML") 
                                                     & (benchmark_parameters_df['Benchmark Class'] == cds.standard_fields.benchmark_class)]
        gnlr_cat_non_modelled= 0  if benchmark_row_df.empty   else benchmark_row_df['Value'].iat[0]             #gross net LR
        gnlr_cat_non_modelled = 0 #TS - overriding based on JM guidance Dec 25, no NMP uplift

        ## GROSS NET - benchmark ***LOAD*** for CAT - Climate Change
        benchmark_row_df     = benchmark_parameters_df[(benchmark_parameters_df['Item'] == "Climate Load") 
                                                     & (benchmark_parameters_df['Benchmark Class'] == cds.standard_fields.benchmark_class)]
        load_cat_climate     = 0  if benchmark_row_df.empty   else benchmark_row_df['Value'].iat[0]             #this is a load not a loss ratio


        ## GROSS GROSS - benchmark ULR
        cat.gg_pre_uw_adj.ulr_benchmark             = gnlr_cat_natural    *    (1 -     total_deductions)

        ## GROSS GROSS - experience ULR - notice no ibnr - flagged for day 2 fix
        cat.gg_pre_uw_adj.ulr_experience            = ( 0 if (   (rating_df.include_selected_weight  *   rating_df.premium_selected_ol).sum() == 0  ) else 
                                                             (  (rating_df.include_selected_weight  *   rating_df.incurred_cat_selected_inflated).sum()
                                                             / (rating_df.include_selected_weight  *   rating_df.premium_selected_ol).sum()))

        ## GROSS GROSS - experience weighting is NOT the same as that used for attritional/large
        cat.gg_pre_uw_adj.ulr_experience_weighting  = cat_experience_weight

        ## GROSS GROSS - RMS loss ratio
        cat.gg_pre_uw_adj.ulr_rms                   = cds.rms.edm_summary.all_peril_selected_at_acc_fx.gross_lr

        ## GROSS GROSS - selected ULR excluding non-modelled losses - take RMS if available, otherwise blend experience and benchmark
        cat.gg_pre_uw_adj.ulr_selected_ol_exc_nml   = (cat.gg_pre_uw_adj.ulr_rms or
                                                          (    cat.gg_pre_uw_adj.ulr_experience  *      cat.gg_pre_uw_adj.ulr_experience_weighting   
                                                            +  cat.gg_pre_uw_adj.ulr_benchmark   * (1 - cat.gg_pre_uw_adj.ulr_experience_weighting  )))

        ## GROSS GROSS - selected ULR non-modelled losses & climate (climate load only applies to natcat not nml)
        cat.gg_pre_uw_adj.ulr_selected_ol_nml       = (   gnlr_cat_non_modelled  *    (1 -     total_deductions)
                                                        + cat.gg_pre_uw_adj.ulr_selected_ol_exc_nml  *  load_cat_climate)

        ## GROSS GROSS - selected ULR
        cat.gg_pre_uw_adj.ulr_selected_ol           = cat.gg_pre_uw_adj.ulr_selected_ol_exc_nml +  cat.gg_pre_uw_adj.ulr_selected_ol_nml

        ## GROSS GROSS - override ULR  - NO OVERRIDE AT THIS POINT ANYMRE AC
        #if cat.uw_override: 
        #    cat.gg_pre_uw_adj.ulr_uw_override          = 0  

        ## final uw ulr allowing for overrides - notice that the test point is always the INPUT field cat.gg_pst_uw_adj.ulr_uw_override
        #cat.gg_pre_uw_adj.ulr_final_uw                 = cat.gg_pre_uw_adj.ulr_uw_override   if cat.uw_override else   cat.gg_pre_uw_adj.ulr_selected_ol 
        #cat.gg_pre_uw_adj.ulr_final                    =(cat.gg_pre_uw_adj.ulr_final_uw      if pd.isnull(cat.gg_pre_uw_adj.ulr_actuarial_override) 
        #                                                                                     else cat.gg_pre_uw_adj.ulr_actuarial_override )

        # assigning to the actuarial output lr where an input exists - always conditioning on gg_pre_uw_adj
        #if pd.isnull(cat.gg_pre_uw_adj.ulr_actuarial_override) == False:   cat.gg_pre_uw_adj.ulr_actuarial_override_output  = cat.gg_pre_uw_adj.ulr_actuarial_override

        cat.gg_pre_uw_adj.ulr_final = max(cat.gg_pre_uw_adj.ulr_selected_ol,min_cat_GG_LR)


        ## assigning to equivalent gross net, pre uw adjustments elements of hxd
        cat.gn_pre_uw_adj.ulr_benchmark             = cat.gg_pre_uw_adj.ulr_benchmark               /  (1 -    total_deductions)  
        cat.gn_pre_uw_adj.ulr_previous_exc_nml      =(cat.gg_pre_uw_adj.ulr_previous_exc_nml or 0)  /  (1 -    total_deductions)
        cat.gn_pre_uw_adj.ulr_previous              =(cat.gg_pre_uw_adj.ulr_previous or 0)          /  (1 -    total_deductions)
        cat.gn_pre_uw_adj.ulr_rms                   = cat.gg_pre_uw_adj.ulr_rms                     /  (1 -    total_deductions)
        cat.gn_pre_uw_adj.ulr_experience            = cat.gg_pre_uw_adj.ulr_experience              /  (1 -    total_deductions)
        cat.gn_pre_uw_adj.ulr_experience_weighting  = cat.gg_pre_uw_adj.ulr_experience_weighting    
        cat.gn_pre_uw_adj.ulr_selected_ol_exc_nml   = cat.gg_pre_uw_adj.ulr_selected_ol_exc_nml     /  (1 -    total_deductions)
        cat.gn_pre_uw_adj.ulr_selected_ol_nml       = cat.gg_pre_uw_adj.ulr_selected_ol_nml         /  (1 -    total_deductions)
        cat.gn_pre_uw_adj.ulr_selected_ol           = cat.gg_pre_uw_adj.ulr_selected_ol             /  (1 -    total_deductions)
        #if cat.uw_override: 
        #    cat.gn_pre_uw_adj.ulr_uw_override          = 0  
        #cat.gn_pre_uw_adj.ulr_final_uw              = cat.gg_pre_uw_adj.ulr_final_uw                /  (1 -    total_deductions)
        #cat.gn_pre_uw_adj.ulr_actuarial_override    = (cat.gg_pre_uw_adj.ulr_actuarial_override or 0)/  (1 -    total_deductions)
        cat.gn_pre_uw_adj.ulr_final                 = cat.gg_pre_uw_adj.ulr_final                   /  (1 -    total_deductions)
        # assigning to the actuarial output lr where an input exists - always conditioning on gg_pre_uw_adj
        #if pd.isnull(cat.gg_pre_uw_adj.ulr_actuarial_override) == False:   cat.gn_pre_uw_adj.ulr_actuarial_override_output  = cat.gn_pre_uw_adj.ulr_actuarial_override



        


         ##################################################################################
        ####################### Experience / Exposure section ############################
        ##################################################################################   

        if risk_info.case_priced == "Yes": cds.rating_summary.kpi.case_priced.show_case_pricing_input_section = True 

        cds = hxd.cds.exposure_experience_weights

        # this is the final total epxerience rated projection of the ULR GN

        cds.experience_rating.pre_uw_adj_gn_ulr = att.gn_pre_uw_adj.ulr_final + lrg.gn_pre_uw_adj.ulr_final + cat.gn_pre_uw_adj.ulr_final 


        
        # Gets adjusted ULR for Att and Cat losses
        for peril in ("att_and_large", "cat"):
            adjustment_peril = getattr(hxd.cds.exposure_adj, peril)
            if adjustment_peril.pre_uw_adj_gn_ulr is not None:
                adjustment_peril.post_uw_adj_gn_ulr = adjustment_peril.pre_uw_adj_gn_ulr * (1 + adjustment_peril.ulr_adjustment) if adjustment_peril.ulr_adjustment is not None else adjustment_peril.pre_uw_adj_gn_ulr

        

        # calculates exposure rating ulr, adjustment to ulr, and the new adjusted ulr 
        if (hxd.cds.exposure_adj.att_and_large.pre_uw_adj_gn_ulr is not None and hxd.cds.exposure_adj.cat.pre_uw_adj_gn_ulr is not None): 
             cds.exposure_rating.pre_uw_adj_gn_ulr =  hxd.cds.exposure_adj.att_and_large.pre_uw_adj_gn_ulr + hxd.cds.exposure_adj.cat.pre_uw_adj_gn_ulr
             cds.exposure_rating.post_uw_adj_gn_ulr = hxd.cds.exposure_adj.att_and_large.post_uw_adj_gn_ulr + hxd.cds.exposure_adj.cat.post_uw_adj_gn_ulr
             cds.exposure_rating.ulr_adjustment = cds.exposure_rating.post_uw_adj_gn_ulr / cds.exposure_rating.pre_uw_adj_gn_ulr - 1
        
        # calculates experience rating ulr, adjustment to ulr, and the new adjusted ulr 
        #cds.experience_rating.pre_uw_adj_gn_ulr =  tot.gn_pre_uw_adj.ulr_priced_final_exc_pc
        #cds.experience_rating.post_uw_adj_gn_ulr = tot.gn_pst_uw_adj.ulr_priced_final_exc_pc
        #cds.experience_rating.ulr_adjustment = (tot.gn_pst_uw_adj.ulr_priced_final_exc_pc / tot.gn_pre_uw_adj.ulr_priced_final_exc_pc) - 1

        # assigns suggested weights
        historical_prem_df = rating_df[["premium_selected_ol_scaled"]]
        historical_prem_df = historical_prem_df[historical_prem_df["premium_selected_ol_scaled"] > 0]
        avg_prem = historical_prem_df["premium_selected_ol_scaled"].mean()
        num_years = historical_prem_df["premium_selected_ol_scaled"].count()

        value_vars = hx.params.table_experience_exposure_weights.columns[1:]
        melted_experience_weights = hx.params.table_experience_exposure_weights.melt(id_vars="Years", value_vars=value_vars, var_name="prem_band", value_name="weights")
        melted_experience_weights["prem_band"] = melted_experience_weights["prem_band"].astype(float)

        if num_years > 25:
             num_years = 25

        melted_experience_weights = melted_experience_weights[melted_experience_weights["Years"] == num_years]
        melted_experience_weights = melted_experience_weights[melted_experience_weights["prem_band"] <= avg_prem].sort_values(by="prem_band", ascending=False).head(1)

        cds.experience_rating.sugg_weight = melted_experience_weights["weights"].iloc[0] if not melted_experience_weights["weights"].empty else 0 
        cds.exposure_rating.sugg_weight = 1 - cds.experience_rating.sugg_weight

        if cds.exposure_rating.sel_weight is not None:
             cds.experience_rating.sel_weight = 1 - cds.exposure_rating.sel_weight
        else:
             cds.experience_rating.sel_weight = None   
        
        #cds.experience_rating.sel_weight = 1 - cds.exposure_rating.sel_weight if cds.exposure_rating.sel_weight else None

        if cds.exposure_rating.sel_weight is not None:
             exposure_weight = cds.exposure_rating.sel_weight
             experience_weight = cds.experience_rating.sel_weight
        else:
             exposure_weight = cds.exposure_rating.sugg_weight
             experience_weight = cds.experience_rating.sugg_weight

        cds.exposure_rating.final_weight = exposure_weight
        cds.experience_rating.final_weight = experience_weight
        
        # Calculates final ulr based on selected and suggested weights
        
        
        
        cds.gn_final_ulr = (att.gn_pre_uw_adj.ulr_final + lrg.gn_pre_uw_adj.ulr_final + cat.gn_pre_uw_adj.ulr_final)   # if there is no exposure rating

        if risk_info.sov_available == "Yes":

            if (hxd.cds.exposure_adj.att_and_large.pre_uw_adj_gn_ulr is not None and hxd.cds.exposure_adj.cat.pre_uw_adj_gn_ulr is not None): 
               
               cds.gn_final_ulr = experience_weight * (att.gn_pre_uw_adj.ulr_final + lrg.gn_pre_uw_adj.ulr_final + cat.gn_pre_uw_adj.ulr_final)  + exposure_weight * (cds.exposure_rating.pre_uw_adj_gn_ulr)
       


        ##############################  step 18 ) Allocation back out to Attr Large  ###################################
        ################################################################################################################
        
        # this is where the allocation back out from the blended attritional exposure experience view into attritional , large and cat occurs. 
        # this all occurs pre UW adjustments 

        #  if there is exposure rating then itll have RMS and it should match cat experience as that should default to RMS
                
        if hxd.cds.exposure_adj.cat.pre_uw_adj_gn_ulr is not None and risk_info.sov_available == "Yes": 
            cat.gn_pre_uw_adj.blended_LR = exposure_weight * hxd.cds.exposure_adj.cat.pre_uw_adj_gn_ulr + experience_weight * cat.gn_pre_uw_adj.ulr_final  
        else :  
            cat.gn_pre_uw_adj.blended_LR = cat.gn_pre_uw_adj.ulr_final 

        # the blending should only occur between the attr and large as the cat should be the same or defualt to experience view if not available 

        
        
        def ZeroDivideError(expression, fallback):
            try:
                return expression()
            except ZeroDivisionError:
                return fallback

        
        if hxd.cds.exposure_adj.att_and_large.pre_uw_adj_gn_ulr is not None and risk_info.sov_available == "Yes": 
            att.gn_pre_uw_adj.blended_LR = ZeroDivideError(lambda: (cds.gn_final_ulr - cat.gn_pre_uw_adj.blended_LR) * att.gn_pre_uw_adj.ulr_selected_ol / (att.gn_pre_uw_adj.ulr_selected_ol + lrg.gn_pre_uw_adj.ulr_selected_ol),0)
        
        else :  
            att.gn_pre_uw_adj.blended_LR = att.gn_pre_uw_adj.ulr_final
        
        if hxd.cds.exposure_adj.att_and_large.pre_uw_adj_gn_ulr is not None and risk_info.sov_available == "Yes": 
            lrg.gn_pre_uw_adj.blended_LR = ZeroDivideError(lambda: (cds.gn_final_ulr - cat.gn_pre_uw_adj.blended_LR)* lrg.gn_pre_uw_adj.ulr_selected_ol / (att.gn_pre_uw_adj.ulr_selected_ol + lrg.gn_pre_uw_adj.ulr_selected_ol ),0)
        
        else :  
            lrg.gn_pre_uw_adj.blended_LR = lrg.gn_pre_uw_adj.ulr_final
        
        att.gg_pre_uw_adj.blended_LR = att.gn_pre_uw_adj.blended_LR *  (1 -    total_deductions )
        lrg.gg_pre_uw_adj.blended_LR = lrg.gn_pre_uw_adj.blended_LR *  (1 -    total_deductions )
        cat.gg_pre_uw_adj.blended_LR = cat.gn_pre_uw_adj.blended_LR *  (1 -    total_deductions )
        

        # need to reassin due to how the data schema was set up 

        att.gn_pst_uw_adj.blended_LR  = att.gn_pre_uw_adj.blended_LR 
        lrg.gn_pst_uw_adj.blended_LR  = lrg.gn_pre_uw_adj.blended_LR 
        cat.gn_pst_uw_adj.blended_LR  = cat.gn_pre_uw_adj.blended_LR 

        att.gg_pst_uw_adj.blended_LR  = att.gg_pre_uw_adj.blended_LR 
        lrg.gg_pst_uw_adj.blended_LR  = lrg.gg_pre_uw_adj.blended_LR 
        cat.gg_pst_uw_adj.blended_LR  = cat.gg_pre_uw_adj.blended_LR 


        
        ####################################################################################
        ### 19) Attr post UW adj                                                         ###
        ####################################################################################

    
        ## assigning to equivalent gross gross, post uw adjustments elements of hxd
        
        #att.gg_pst_uw_adj.ulr_selected_ol_exc_scalant       = att.gg_pre_uw_adj.ulr_selected_ol_exc_scalant             *   (1 +    (att.uw_adjustment or 0))
        
        att.gg_pst_uw_adj.ulr_final_uw                     = att.gg_pre_uw_adj.blended_LR                        *   (1 +    (att.uw_adjustment or 0))
        
        # att.gg_pst_uw_adj.ulr_uw_override                   = (att.gg_pre_uw_adj.ulr_uw_override or 0)   
        
        if   pd.isnull(att.gg_pre_uw_adj.ulr_uw_override): att.gg_pst_uw_adj.ulr_final_uw   = (att.gg_pst_uw_adj.ulr_final_uw)
        else                                             : att.gg_pst_uw_adj.ulr_final_uw   = (att.gg_pst_uw_adj.ulr_uw_override)

        att.gg_pst_uw_adj.ulr_actuarial_override            = (att.gg_pre_uw_adj.ulr_actuarial_override or 0)      
        
        att.gg_pst_uw_adj.ulr_final                         = (att.gg_pst_uw_adj.ulr_final_uw     if pd.isnull(att.gg_pre_uw_adj.ulr_actuarial_override) 
                                                                                                  else   att.gg_pst_uw_adj.ulr_actuarial_override) ##notice condition on gg_pre_uw_adj deliberately
        # assigning to the actuarial output lr where an input exists - always conditioning on gg_pre_uw_adj
        if pd.isnull(att.gg_pre_uw_adj.ulr_actuarial_override) == False:   att.gg_pst_uw_adj.ulr_actuarial_override_output  = att.gg_pst_uw_adj.ulr_actuarial_override

        if att.gg_pst_uw_adj.ulr_uw_override is not None:   
            att.gg_pst_uw_adj.ulr_final  = att.gg_pst_uw_adj.ulr_uw_override

        ## assigning to equivalent gross net, post uw adjustments elements of hxd
        #att.gn_pst_uw_adj.ulr_selected_ol_exc_scalant       = att.gg_pst_uw_adj.ulr_selected_ol_exc_scalant              /  (1 -    total_deductions)
        #att.gn_pst_uw_adj.ulr_selected_ol                   = att.gg_pst_uw_adj.ulr_selected_ol                          /  (1 -    total_deductions)
        
        if att.gg_pst_uw_adj.ulr_uw_override == None:
        
            att.gn_pst_uw_adj.ulr_uw_override = None
        else:

            att.gn_pst_uw_adj.ulr_uw_override                   = (att.gg_pst_uw_adj.ulr_uw_override or 0)                /  (1 -    total_deductions)
        
        att.gn_pst_uw_adj.ulr_final_uw                      = att.gg_pst_uw_adj.ulr_final_uw                             /  (1 -    total_deductions)
        att.gn_pst_uw_adj.ulr_actuarial_override            = att.gg_pst_uw_adj.ulr_actuarial_override                   /  (1 -    total_deductions)
        att.gn_pst_uw_adj.ulr_final                         = att.gg_pst_uw_adj.ulr_final                                /  (1 -    total_deductions)

        # assigning to the actuarial output lr where an input exists - always conditioning on gg_pre_uw_adj
        if pd.isnull(att.gg_pre_uw_adj.ulr_actuarial_override) == False:   att.gn_pst_uw_adj.ulr_actuarial_override_output  = att.gn_pst_uw_adj.ulr_actuarial_override


        ####################################################################################
        ### 20) Large post UW adj                                                        ###
        ####################################################################################

        
         ## assigning to equivalent gross gross, post uw adjustments elements of hxd
        lrg.gg_pst_uw_adj.ulr_final_uw            = lrg.gg_pre_uw_adj.blended_LR             *   (1 +    (lrg.uw_adjustment or 0))
        
        #if lrg.uw_override: 
        #    lrg.gg_pst_uw_adj.ulr_uw_override       = 0  
        
        #lrg.gg_pst_uw_adj.ulr_final_uw              = lrg.gg_pst_uw_adj.ulr_uw_override   if lrg.uw_override else   lrg.gg_pst_uw_adj.ulr_selected_ol 
        #
        
        lrg.gg_pst_uw_adj.ulr_actuarial_override    = (lrg.gg_pst_uw_adj.ulr_actuarial_override or 0)    
        lrg.gg_pst_uw_adj.ulr_final                 = (lrg.gg_pst_uw_adj.ulr_final_uw   if pd.isnull(lrg.gg_pre_uw_adj.ulr_actuarial_override) 
                                                                                        else   lrg.gg_pst_uw_adj.ulr_actuarial_override) ##notice condition on gg_pre_uw_adj deliberately
        

        if lrg.uw_override == True : 
            lrg.gg_pst_uw_adj.ulr_final = 0 
            lrg.gg_pst_uw_adj.blended_LR = 0  


        # assigning to the actuarial output lr where an input exists - always conditioning on gg_pre_uw_adj
        if pd.isnull(lrg.gg_pre_uw_adj.ulr_actuarial_override) == False:   lrg.gg_pst_uw_adj.ulr_actuarial_override_output  = lrg.gg_pst_uw_adj.ulr_actuarial_override

        if lrg.gg_pst_uw_adj.ulr_uw_override is not None:   
            lrg.gg_pst_uw_adj.ulr_final  = lrg.gg_pst_uw_adj.ulr_uw_override

        if lrg.gg_pst_uw_adj.ulr_uw_override == None:
        
            lrg.gn_pst_uw_adj.ulr_uw_override = None
        else:

            lrg.gn_pst_uw_adj.ulr_uw_override                   = (lrg.gg_pst_uw_adj.ulr_uw_override or 0)                /  (1 -    total_deductions)

        ## assigning to equivalent gross net, post uw adjustments elements of hxd
        # lrg.gn_pst_uw_adj.ulr_selected_ol           = lrg.gg_pst_uw_adj.ulr_selected_ol             /  (1 -    total_deductions)
        # if lrg.uw_override: 
        #     lrg.gn_pst_uw_adj.ulr_uw_override       = 0 
        
        lrg.gn_pst_uw_adj.ulr_final_uw              = lrg.gg_pst_uw_adj.ulr_final_uw                 /  (1 -    total_deductions)
        lrg.gn_pst_uw_adj.ulr_actuarial_override    =(lrg.gg_pst_uw_adj.ulr_actuarial_override or 0) /  (1 -    total_deductions)
        lrg.gn_pst_uw_adj.ulr_final                 = lrg.gg_pst_uw_adj.ulr_final                    /  (1 -    total_deductions)

        # assigning to the actuarial output lr where an input exists - always conditioning on gg_pre_uw_adj
        if pd.isnull(lrg.gg_pre_uw_adj.ulr_actuarial_override) == False:   lrg.gn_pst_uw_adj.ulr_actuarial_override_output  = lrg.gn_pst_uw_adj.ulr_actuarial_override

        if lrg.uw_override == True : 
            lrg.gn_pst_uw_adj.ulr_final = 0 
            lrg.gn_pst_uw_adj.blended_LR = 0   

        ####################################################################################
        ### 21) Cat post UW adj                                                        ###
        ####################################################################################


         ## assigning to equivalent gross gross, post uw adjustments elements of hxd
        #cat.gg_pst_uw_adj.ulr_selected_ol_exc_nml   = cat.gg_pre_uw_adj.ulr_selected_ol_exc_nml     *  (1 +    (cat.uw_adjustment or 0))
        #cat.gg_pst_uw_adj.ulr_selected_ol_nml       = cat.gg_pre_uw_adj.ulr_selected_ol_nml         *  (1 +    (cat.uw_adjustment or 0))
        
        cat.gg_pst_uw_adj.ulr_final_uw            = cat.gg_pre_uw_adj.blended_LR             *  (1 +    (cat.uw_adjustment or 0))
        
        #if cat.uw_override: 
        #    cat.gg_pst_uw_adj.ulr_uw_override          = 0  
        #cat.gg_pst_uw_adj.ulr_final_uw              = cat.gg_pst_uw_adj.ulr_uw_override   if cat.uw_override else   cat.gg_pst_uw_adj.ulr_selected_ol 
        
        cat.gg_pst_uw_adj.ulr_actuarial_override    = (cat.gg_pst_uw_adj.ulr_actuarial_override or 0)  
        cat.gg_pst_uw_adj.ulr_final                 = (cat.gg_pst_uw_adj.ulr_final_uw   if pd.isnull(cat.gg_pre_uw_adj.ulr_actuarial_override) 
                                                                                        else   cat.gg_pst_uw_adj.ulr_actuarial_override) ##notice condition on gg_pre_uw_adj deliberately
        # assigning to the actuarial output lr where an input exists - always conditioning on gg_pre_uw_adj
        if pd.isnull(cat.gg_pre_uw_adj.ulr_actuarial_override) == False:   cat.gg_pst_uw_adj.ulr_actuarial_override_output  = cat.gg_pst_uw_adj.ulr_actuarial_override


        if cat.gg_pst_uw_adj.ulr_uw_override is not None:   
            cat.gg_pst_uw_adj.ulr_final  = cat.gg_pst_uw_adj.ulr_uw_override

        if cat.gg_pst_uw_adj.ulr_uw_override == None:
        
            cat.gn_pst_uw_adj.ulr_uw_override = None
        else:

            cat.gn_pst_uw_adj.ulr_uw_override                   = (cat.gg_pst_uw_adj.ulr_uw_override or 0)                /  (1 -    total_deductions)

        if cat.uw_override == True : 
            cat.gg_pst_uw_adj.ulr_final = 0 
            cat.gg_pst_uw_adj.blended_LR = 0 

        

        
        cat.gn_pst_uw_adj.ulr_final_uw              = cat.gg_pst_uw_adj.ulr_final_uw                /  (1 -    total_deductions)
        cat.gn_pst_uw_adj.ulr_actuarial_override    = cat.gg_pst_uw_adj.ulr_actuarial_override      /  (1 -    total_deductions)
        cat.gn_pst_uw_adj.ulr_final                 = cat.gg_pst_uw_adj.ulr_final                   /  (1 -    total_deductions)
        
        # assigning to the actuarial output lr where an input exists - always conditioning on gg_pre_uw_adj
        if pd.isnull(cat.gg_pre_uw_adj.ulr_actuarial_override) == False:   cat.gn_pst_uw_adj.ulr_actuarial_override_output  = cat.gn_pst_uw_adj.ulr_actuarial_override

        if cat.uw_override == True : 
            cat.gn_pst_uw_adj.ulr_final = 0 
            cat.gn_pst_uw_adj.blended_LR = 0 


        # timer.end("step 17")
        ####################################################################################
        ### 18) Calculate Pre & Post PC Premium Metrics                                  ###
        ####################################################################################

        
        tech.amount_pc_100         = ( profit_comm.result_exp_pc_payable_override 
                                        or profit_comm.result_exp_pc_payable
                                        or 0 )                                                              #necessary to calculate here and not use selected due to order of calculations

        if rating_info.status == "Bound" and rating_info.signed_line != 0:
            line_use = rating_info.signed_line
        else:
            line_use = rating_info.written_line

        tech.amount_pc_afb         = tech.amount_pc_100 * (line_use or 0)

        gg_prem                    = ( rating_info.quoted_premium_100pct or 0 )
        tech.percent_pc            = 0 if ( gg_prem == 0 ) else tech.amount_pc_100 / gg_prem 
        percent_pc                 = tech.percent_pc                                                         # profit commision as a % of gross prem


        tech.amts_pre_uw_adj.aqn_pc_afb = tech.amount_pc_afb 
        tech.amts_pst_uw_adj.aqn_pc_afb = tech.amount_pc_afb 

        # timer.start("step 19")
        ####################################################################################
        ### 19) Source KPI Summary Metrics and premiums                                  ###
        ####################################################################################

        # Calculating EPI - Gross & Net at 100 percent and beazley share (afb)
        tech.gg_premium_quoted_100_pct        = (rating_info.quoted_premium_100pct or 0)
        tech.gn_premium_quoted_exc_pc_100_pct = tech.gg_premium_quoted_100_pct * (1 - total_deductions)
        tech.gn_premium_quoted_inc_pc_100_pct = tech.gg_premium_quoted_100_pct * (1 - total_deductions - percent_pc)

        tech.gg_premium_quoted_afb           = tech.gg_premium_quoted_100_pct * (line_use or 0)
        tech.gn_premium_quoted_exc_pc_afb    = tech.gg_premium_quoted_afb    * (1 - total_deductions)
        tech.gn_premium_quoted_inc_pc_afb    = tech.gg_premium_quoted_afb    * (1 - total_deductions - percent_pc)


        # calculate benchmark insurance ratios
        bench_df   = benchmark_parameters_df[(benchmark_parameters_df['Benchmark Class'] == standard_fields.benchmark_class)]

        percent_bench_lr    = bench_df[(bench_df['Item'] == "Target NLR") ]['Value']
        percent_bench_lr    = 0 if pd.isnull(percent_bench_lr.iat[0]) else percent_bench_lr.iat[0]

        percent_plan_lr     = bench_df[(bench_df['Item'] == "Total ULR") ]['Value']
        percent_plan_lr     = 0 if pd.isnull(percent_plan_lr.iat[0]) else percent_plan_lr.iat[0]

        percent_ri_premium  = bench_df[(bench_df['Item'] == "RI Premium/GN Premium") ]['Value']
        percent_ri_premium  = 0 if pd.isnull(percent_ri_premium.iat[0]) else percent_ri_premium.iat[0]

        percent_ri_recovery = bench_df[(bench_df['Item'] == "RI Recoveries/ GN Premium") ]   ['Value']     
        percent_ri_recovery = 0 if pd.isnull(percent_ri_recovery.iat[0]) else percent_ri_recovery.iat[0]

            # the original model had an extra condition bespoke to covers international - which is not included here as not intended to be used by that team
        percent_capital_req = bench_df[(bench_df['Item'] == "Capital Required / GN Premium") ]['Value']
        percent_capital_req = 0 if pd.isnull(percent_capital_req.iat[0]) else percent_capital_req.iat[0]

        percent_roc         = bench_df[(bench_df['Item'] == "RoC") ]['Value']
        percent_roc         = 0 if pd.isnull(percent_roc.iat[0]) else percent_roc.iat[0]

        percent_expense     = bench_df[(bench_df['Item'] == "Net Expense/ GN Premium") ]['Value']
        percent_expense     = 0 if pd.isnull(percent_expense.iat[0]) else percent_expense.iat[0]

        percent_invest_inc  = bench_df[(bench_df['Item'] == "Investment Income /GN Premium") ]['Value']
        percent_invest_inc  = 0 if pd.isnull(percent_invest_inc.iat[0]) else percent_invest_inc.iat[0]

        percent_lae         = bench_df[(bench_df['Item'] == "LAE") ]['Value']
        percent_lae         = 0 if pd.isnull(percent_lae.iat[0]) else percent_lae.iat[0]



        # calculate total GROSS GROSS loss ratios - priced / benchmark / plan / prior - BEFORE UW ADJ
        tot.gg_pre_uw_adj.ulr_priced_final        = att.gg_pre_uw_adj.blended_LR +   lrg.gg_pre_uw_adj.blended_LR   +   cat.gg_pre_uw_adj.blended_LR


        # calculate total GROSS NET loss ratios - priced / benchmark / plan / prior - BEFORE UW ADJ
        tot.gn_pre_uw_adj.ulr_priced_final_exc_pc = att.gn_pre_uw_adj.blended_LR  +   lrg.gn_pre_uw_adj.blended_LR    +   cat.gn_pre_uw_adj.blended_LR 
        tot.gn_pre_uw_adj.ulr_priced_final_inc_pc = tot.gg_pre_uw_adj.ulr_priced_final / (1 - percent_pc - total_deductions)
        tot.gn_pre_uw_adj.ulr_bench               = percent_bench_lr
        tot.gn_pre_uw_adj.ulr_plan                = percent_plan_lr
        #tot.gn_pre_uw_adj.ulr_prior               
  

        # calculate total GROSS GROSS loss ratios - priced / benchmark / plan / prior - AFTER UW ADJ
        tot.gg_pst_uw_adj.ulr_priced_final          = att.gg_pst_uw_adj.ulr_final  +   lrg.gg_pst_uw_adj.ulr_final   +   cat.gg_pst_uw_adj.ulr_final 


        # calculate total GROSS NET loss ratios - priced / benchmark / plan / prior  - AFTER UW ADJ
        tot.gn_pst_uw_adj.ulr_priced_final_exc_pc = att.gn_pst_uw_adj.ulr_final  +   lrg.gn_pst_uw_adj.ulr_final   +   cat.gn_pst_uw_adj.ulr_final
        tot.gn_pst_uw_adj.ulr_priced_final_inc_pc = tot.gg_pst_uw_adj.ulr_priced_final / (1 - percent_pc - total_deductions)
        tot.gn_pst_uw_adj.ulr_bench               = percent_bench_lr
        tot.gn_pst_uw_adj.ulr_plan                = percent_plan_lr
        #tot.gn_pst_uw_adj.ulr_prior               
  


        tot.uw_adjustment  = 0 if tot.gg_pre_uw_adj.ulr_priced_final == 0 else (
                                  tot.gg_pst_uw_adj.ulr_priced_final / tot.gg_pre_uw_adj.ulr_priced_final )


        # timer.end("step 19")
        # timer.start("step 20")
        ####################################################################################
        ### 20) Calculate benchmark, technical amounts and KPIs - before UW adjustment   ###
        ####################################################################################

        # calculate amounts associated to gross insurance losses for beazley (afb)
        tech.amts_pre_uw_adj.losses_att_afb  = tech.gg_premium_quoted_afb    *   att.gg_pre_uw_adj.blended_LR
        tech.amts_pre_uw_adj.losses_lrg_afb  = tech.gg_premium_quoted_afb    *   lrg.gg_pre_uw_adj.blended_LR
        tech.amts_pre_uw_adj.losses_cat_afb  = tech.gg_premium_quoted_afb    *   cat.gg_pre_uw_adj.blended_LR
        tech.amts_pre_uw_adj.losses_tot_afb  = (tech.amts_pre_uw_adj.losses_att_afb +   tech.amts_pre_uw_adj.losses_lrg_afb +   tech.amts_pre_uw_adj.losses_cat_afb)


        # calculate amounts associated to income statement items OTHER THAN ACQUISITION
        tech.amts_pre_uw_adj.reinsurance_afb  = 0 if tot.gn_pre_uw_adj.ulr_priced_final_inc_pc==0 else (
                                                         tech.amts_pre_uw_adj.losses_tot_afb
                                                            *   (percent_ri_premium - percent_ri_recovery) 
                                                            /    tot.gn_pre_uw_adj.ulr_priced_final_exc_pc)

        tech.amts_pre_uw_adj.profit_req_afb   = 0 if tot.gn_pre_uw_adj.ulr_priced_final_inc_pc==0 else (
                                                         tech.amts_pre_uw_adj.losses_tot_afb  
                                                            *   percent_roc 
                                                            *   percent_capital_req
                                                            /   tot.gn_pre_uw_adj.ulr_priced_final_exc_pc )

        tech.amts_pre_uw_adj.expense_afb      = (tech.amts_pre_uw_adj.losses_tot_afb  *   percent_expense
                                                                                      /   tot.gn_pre_uw_adj.ulr_priced_final_exc_pc )  
        tech.amts_pre_uw_adj.investment_afb   = (tech.amts_pre_uw_adj.losses_tot_afb  *   percent_invest_inc
                                                                                      /   tot.gn_pre_uw_adj.ulr_priced_final_exc_pc )    
        tech.amts_pre_uw_adj.lae_afb          = tech.amts_pre_uw_adj.losses_cat_afb  *   percent_lae            #applies to cat only per old model


        # calculate technical premium PART 1 - Gross NET inc PC
        tech.amts_pre_uw_adj.gn_premium_tech_inc_pc_afb     = ( tech.amts_pre_uw_adj.losses_tot_afb 
                                                                     + tech.amts_pre_uw_adj.reinsurance_afb
                                                                     + tech.amts_pre_uw_adj.profit_req_afb
                                                                     + tech.amts_pre_uw_adj.expense_afb
                                                                     + tech.amts_pre_uw_adj.lae_afb 
                                                                     - tech.amts_pre_uw_adj.investment_afb) #subtracting investment


        # calculate amounts associated to acquisition costs PART 1 - 
        tech.amts_pre_uw_adj.aqn_comm_afb          = rating_info.quoted_premium_100pct * line_use* hxd.cds.layers[0].commission

        tech.amts_pre_uw_adj.aqn_brok_afb          = rating_info.quoted_premium_100pct * line_use * hxd.cds.layers[0].brokerage

        tech.amts_pre_uw_adj.aqn_iptax_afb         = rating_info.quoted_premium_100pct * line_use * hxd.cds.layers[0].ipt

        tech.amts_pre_uw_adj.aqn_total  = (tech.amts_pre_uw_adj.aqn_comm_afb
                                                                +   tech.amts_pre_uw_adj.aqn_brok_afb  
                                                                +   tech.amts_pre_uw_adj.aqn_iptax_afb)
        
                # note there is a slight inconsistency in the formula below - the PC is treated as multiplicative not additive to the other deductions.
                # however this is the way it is coded in the prior model - flagging it for review at day 2 - this logic has been carried through into the benchmark premium calc
        
        #tech.amts_pre_uw_adj.aqn_pc_afb        = (  (tech.amts_pre_uw_adj.gn_premium_tech_inc_pc_afb
        #                                                      +   tech.amts_pre_uw_adj.aqn_total_exc_pc_afb)
        #                                                 * (1 / ( 1  - percent_pc )    -   1 ))    

        #tech.amts_pre_uw_adj.aqn_total_inc_pc_afb  = tech.amts_pre_uw_adj.aqn_total_exc_pc_afb   +   tech.amts_pre_uw_adj.aqn_pc_afb


        # calculate technical premium PART 2
        tech.amts_pre_uw_adj.gn_premium_tech_exc_pc_afb    =  tech.amts_pre_uw_adj.gn_premium_tech_inc_pc_afb 
                                                                    


        tech.amts_pre_uw_adj.gg_premium_tech_afb           = (tech.amts_pre_uw_adj.gn_premium_tech_exc_pc_afb 
                                                                     + tech.amts_pre_uw_adj.aqn_total)

        tech.amts_pre_uw_adj.gn_premium_tech_inc_pc_100_pct= ( tech.amts_pre_uw_adj.gn_premium_tech_inc_pc_afb
                                                                     / (line_use or 1 ))

        tech.amts_pre_uw_adj.gn_premium_tech_exc_pc_100_pct= ( tech.amts_pre_uw_adj.gn_premium_tech_exc_pc_afb
                                                                     / (line_use or 1 ))

        tech.amts_pre_uw_adj.gg_premium_tech_100_pct       =  ( tech.amts_pre_uw_adj.gg_premium_tech_afb
                                                                      / (line_use or 1 ))



        # calculate benchmark premium
        tech.amts_pre_uw_adj.gn_premium_bench_inc_pc_afb       = 0 if pd.isna(percent_bench_lr) else (tech.amts_pre_uw_adj.losses_tot_afb
                                                                                                            / percent_bench_lr)
        tech.amts_pre_uw_adj.gn_premium_bench_exc_pc_afb       = tech.amts_pre_uw_adj.gn_premium_bench_inc_pc_afb  / (1 - percent_pc)
        tech.amts_pre_uw_adj.gg_premium_bench_afb              = tech.amts_pre_uw_adj.gn_premium_bench_exc_pc_afb  / (1 - total_deductions)

        tech.amts_pre_uw_adj.gn_premium_bench_inc_pc_100_pct   = ( tech.amts_pre_uw_adj.gn_premium_bench_inc_pc_afb
                                                                        / (line_use or 1 ))
        tech.amts_pre_uw_adj.gn_premium_bench_exc_pc_100_pct   = ( tech.amts_pre_uw_adj.gn_premium_bench_exc_pc_afb
                                                                        / (line_use or 1 ))
        tech.amts_pre_uw_adj.gg_premium_bench_100_pct          = ( tech.amts_pre_uw_adj.gg_premium_bench_afb 
                                                                        / (line_use or 1 ))

        # calcualte KPI Metrics

        kpi.pre_uw_adj.expected_profit  = ( tech.gn_premium_quoted_inc_pc_afb 
                                                - tech.amts_pre_uw_adj.losses_tot_afb  
                                                - tech.amts_pre_uw_adj.reinsurance_afb
                                                - tech.amts_pre_uw_adj.expense_afb
                                                - tech.amts_pre_uw_adj.lae_afb
                                                + tech.amts_pre_uw_adj.investment_afb )         
        kpi.pre_uw_adj.allocated_capital= ( percent_capital_req * tech.gn_premium_quoted_inc_pc_afb )        
        #kpi.pre_uw_adj.bpi_prior        = 
        kpi.pre_uw_adj.bpi              =  0 if tech.amts_pre_uw_adj.gn_premium_bench_inc_pc_afb == 0 else (
                                                tech.gn_premium_quoted_inc_pc_afb / tech.amts_pre_uw_adj.gn_premium_bench_inc_pc_afb )
        kpi.pre_uw_adj.tpi              =  0 if tech.amts_pre_uw_adj.gn_premium_tech_inc_pc_afb  == 0 else (
                                                tech.gn_premium_quoted_inc_pc_afb / tech.amts_pre_uw_adj.gn_premium_tech_inc_pc_afb )
        kpi.pre_uw_adj.roc              =  0 if kpi.pre_uw_adj.allocated_capital == 0 else ( 
                                                kpi.pre_uw_adj.expected_profit / kpi.pre_uw_adj.allocated_capital )


        # timer.end("step 20")
        # timer.start("step 21")
        ####################################################################################
        ### 21) Calculate benchmark, technical amounts and KPIs  - after UW adjustment   ###
        ####################################################################################

        # calculate amounts associated to gross insurance losses for beazley (afb)
        tech.amts_pst_uw_adj.losses_att_afb  = tech.gg_premium_quoted_afb    *   att.gg_pst_uw_adj.ulr_final
        tech.amts_pst_uw_adj.losses_lrg_afb  = tech.gg_premium_quoted_afb    *   lrg.gg_pst_uw_adj.ulr_final
        tech.amts_pst_uw_adj.losses_cat_afb  = tech.gg_premium_quoted_afb    *   cat.gg_pst_uw_adj.ulr_final
        tech.amts_pst_uw_adj.losses_tot_afb  = (tech.amts_pst_uw_adj.losses_att_afb
                                                   +   tech.amts_pst_uw_adj.losses_lrg_afb
                                                   +   tech.amts_pst_uw_adj.losses_cat_afb)


        # calculate amounts associated to income statement items OTHER THAN ACQUISITION
        tech.amts_pst_uw_adj.reinsurance_afb  = 0 if tot.gn_pst_uw_adj.ulr_priced_final_inc_pc==0 else (
                                                         tech.amts_pst_uw_adj.losses_tot_afb
                                                            *   (percent_ri_premium - percent_ri_recovery) 
                                                            /    tot.gn_pst_uw_adj.ulr_priced_final_exc_pc)

        tech.amts_pst_uw_adj.profit_req_afb   = 0 if tot.gn_pst_uw_adj.ulr_priced_final_exc_pc==0 else (
                                                         tech.amts_pst_uw_adj.losses_tot_afb  
                                                            *   percent_roc 
                                                            *   percent_capital_req
                                                            /   tot.gn_pst_uw_adj.ulr_priced_final_exc_pc )

        tech.amts_pst_uw_adj.expense_afb = 0 if tech.amts_pst_uw_adj.losses_tot_afb == 0 else (
            (tech.amts_pst_uw_adj.losses_tot_afb * percent_expense / tot.gn_pst_uw_adj.ulr_priced_final_exc_pc ) or 0
        )

        tech.amts_pst_uw_adj.investment_afb = 0 if tech.amts_pst_uw_adj.losses_tot_afb == 0 else (
            (tech.amts_pst_uw_adj.losses_tot_afb * percent_invest_inc / tot.gn_pst_uw_adj.ulr_priced_final_exc_pc ) or 0
        )
        
        tech.amts_pst_uw_adj.lae_afb          = tech.amts_pst_uw_adj.losses_cat_afb  *   percent_lae    #applies to cat only per old model


        # calculate technical premium PART 1 - Gross NET inc PC
        tech.amts_pst_uw_adj.gn_premium_tech_inc_pc_afb     = ( tech.amts_pst_uw_adj.losses_tot_afb 
                                                                     + tech.amts_pst_uw_adj.reinsurance_afb
                                                                     + tech.amts_pst_uw_adj.profit_req_afb
                                                                     + tech.amts_pst_uw_adj.expense_afb
                                                                     + tech.amts_pst_uw_adj.lae_afb 
                                                                     - tech.amts_pst_uw_adj.investment_afb) #subtracting investment


        # calculate amounts associated to acquisition costs PART 1 - 
        tech.amts_pst_uw_adj.aqn_comm_afb          = rating_info.quoted_premium_100pct * line_use* hxd.cds.layers[0].commission

        tech.amts_pst_uw_adj.aqn_brok_afb          = rating_info.quoted_premium_100pct * line_use * hxd.cds.layers[0].brokerage

        tech.amts_pst_uw_adj.aqn_iptax_afb         = rating_info.quoted_premium_100pct * line_use * hxd.cds.layers[0].ipt
        
        tech.amts_pst_uw_adj.aqn_total = tech.amts_pre_uw_adj.aqn_comm_afb +  tech.amts_pre_uw_adj.aqn_brok_afb + tech.amts_pre_uw_adj.aqn_iptax_afb 

        # calculate technical premium PART 2
        tech.amts_pst_uw_adj.gn_premium_tech_exc_pc_afb    = tech.amts_pst_uw_adj.gn_premium_tech_inc_pc_afb 
                                                                   


        tech.amts_pst_uw_adj.gg_premium_tech_afb           = (tech.amts_pst_uw_adj.gn_premium_tech_exc_pc_afb 
                                                                     + tech.amts_pst_uw_adj.aqn_total)

        tech.amts_pst_uw_adj.gn_premium_tech_inc_pc_100_pct = ( tech.amts_pst_uw_adj.gn_premium_tech_inc_pc_afb
                                                                     / (line_use or 1 ))

        tech.amts_pst_uw_adj.gn_premium_tech_exc_pc_100_pct= ( tech.amts_pst_uw_adj.gn_premium_tech_exc_pc_afb
                                                                     / (line_use or 1 ))

        tech.amts_pst_uw_adj.gg_premium_tech_100_pct       =  ( tech.amts_pst_uw_adj.gg_premium_tech_afb
                                                                      / (line_use or 1 ))



        # calculate benchmark premium
        tech.amts_pst_uw_adj.gn_premium_bench_inc_pc_afb       = 0 if pd.isna(percent_bench_lr) else (tech.amts_pst_uw_adj.losses_tot_afb
                                                                                                        / percent_bench_lr)
        tech.amts_pst_uw_adj.gn_premium_bench_exc_pc_afb       = tech.amts_pst_uw_adj.gn_premium_bench_inc_pc_afb  / (1 - percent_pc)
        tech.amts_pst_uw_adj.gg_premium_bench_afb              = tech.amts_pst_uw_adj.gn_premium_bench_exc_pc_afb  / (1 - total_deductions)

        tech.amts_pst_uw_adj.gn_premium_bench_inc_pc_100_pct   = ( tech.amts_pst_uw_adj.gn_premium_bench_inc_pc_afb
                                                                        / (line_use or 1))
        tech.amts_pst_uw_adj.gn_premium_bench_exc_pc_100_pct   = ( tech.amts_pst_uw_adj.gn_premium_bench_exc_pc_afb
                                                                        / (line_use or 1))
        tech.amts_pst_uw_adj.gg_premium_bench_100_pct          = ( tech.amts_pst_uw_adj.gg_premium_bench_afb 
                                                                        / (line_use or 1 ))




        # calcualte KPI Metrics
        kpi.pst_uw_adj.expected_profit  = ( tech.gn_premium_quoted_inc_pc_afb 
                                                - tech.amts_pst_uw_adj.losses_tot_afb  
                                                - tech.amts_pst_uw_adj.reinsurance_afb
                                                - tech.amts_pst_uw_adj.expense_afb
                                                - tech.amts_pst_uw_adj.lae_afb
                                                + tech.amts_pst_uw_adj.investment_afb )         
        kpi.pst_uw_adj.allocated_capital= ( percent_capital_req * tech.gn_premium_quoted_inc_pc_afb )        
        #kpi.pst_uw_adj.bpi_prior        = 
        kpi.pst_uw_adj.bpi              =  0 if tech.amts_pst_uw_adj.gn_premium_bench_inc_pc_afb == 0 else (
                                                    tech.gn_premium_quoted_inc_pc_afb / tech.amts_pst_uw_adj.gn_premium_bench_inc_pc_afb )
        kpi.pst_uw_adj.tpi              =  0 if tech.amts_pst_uw_adj.gn_premium_tech_inc_pc_afb  == 0 else (
                                                    tech.gn_premium_quoted_inc_pc_afb / tech.amts_pst_uw_adj.gn_premium_tech_inc_pc_afb )
        kpi.pst_uw_adj.roc              =  0 if kpi.pst_uw_adj.allocated_capital == 0 else (
                                                    kpi.pst_uw_adj.expected_profit / kpi.pst_uw_adj.allocated_capital)

        #########################


        # calculate combined loss ratios
        
        comb_ratio_pre_uw_adj_inc_pc = (
        0 if (tech.gg_premium_quoted_afb - tech.amount_pc_afb) == 0 else
        (
            tech.amts_pre_uw_adj.losses_tot_afb + 
            tech.amts_pre_uw_adj.expense_afb +
            tech.amts_pre_uw_adj.lae_afb +
            tech.amts_pre_uw_adj.reinsurance_afb +
            tech.amts_pre_uw_adj.aqn_total ) / (
            tech.gg_premium_quoted_afb-tech.amount_pc_afb )
            )

        comb_ratio_pre_uw_adj_exc_pc = (
        0 if (tech.gg_premium_quoted_afb - tech.amount_pc_afb) == 0 else
        (
            tech.amts_pre_uw_adj.losses_tot_afb + 
            tech.amts_pre_uw_adj.expense_afb +
            tech.amts_pre_uw_adj.lae_afb +
            tech.amts_pre_uw_adj.reinsurance_afb +
            tech.amts_pre_uw_adj.aqn_total) / (
            tech.gg_premium_quoted_afb)
        )
    
        comb_ratio_pst_uw_adj_inc_pc = (
        0 if (tech.gg_premium_quoted_afb - tech.amount_pc_afb) == 0 else
        (
            tech.amts_pst_uw_adj.losses_tot_afb + 
            tech.amts_pst_uw_adj.expense_afb +
            tech.amts_pst_uw_adj.lae_afb +
            tech.amts_pst_uw_adj.reinsurance_afb +
            tech.amts_pst_uw_adj.aqn_total) / (
            tech.gg_premium_quoted_afb-tech.amount_pc_afb)
        )

        comb_ratio_pst_uw_adj_exc_pc = (
        0 if (tech.gg_premium_quoted_afb - tech.amount_pc_afb) == 0 else
        (
            tech.amts_pst_uw_adj.losses_tot_afb + 
            tech.amts_pst_uw_adj.expense_afb +
            tech.amts_pst_uw_adj.lae_afb +
            tech.amts_pre_uw_adj.reinsurance_afb +
            tech.amts_pst_uw_adj.aqn_total) / (
            tech.gg_premium_quoted_afb)
        )

        # hxd.cds.rationale.comb_ratio_pre.inc_pc = gn_comb_ratio_pre_uw_adj_inc_pc
        # hxd.cds.rationale.comb_ratio_pst = gn_comb_ratio_pst_uw_adj_inc_pc

        # hxd.cds.rationale.comb_ratio_pre = gn_comb_ratio_pre_uw_adj_inc_pc
        # hxd.cds.rationale.comb_ratio_pst = gn_comb_ratio_pst_uw_adj_inc_pc

        hxd.cds.rating_summary.summary_ratios.total.pre_uw_adj.comb_ratio_exc_pc = comb_ratio_pre_uw_adj_exc_pc
        hxd.cds.rating_summary.summary_ratios.total.pre_uw_adj.comb_ratio_inc_pc = comb_ratio_pre_uw_adj_inc_pc
        hxd.cds.rating_summary.summary_ratios.total.pst_uw_adj.comb_ratio_exc_pc = comb_ratio_pst_uw_adj_exc_pc
        hxd.cds.rating_summary.summary_ratios.total.pst_uw_adj.comb_ratio_inc_pc = comb_ratio_pst_uw_adj_inc_pc


        tot = hxd.cds.rating_summary.summary_ratios.total

        # timer.end("step 21")
        # timer.start("step 26")
        ####################################################################################
        ### 22) Calculate CHART - Incurred LR by Year                                    ###
        ####################################################################################




        rating_df['display_yoa']                        = rating_df.yoa.astype(str)
        rating_df['display_premium_ol']                 = rating_df.premium_selected_ol_scaled.astype(float)
        rating_df['display_attritional_weight']         = rating_df.weighting_final


        rating_df['display_attritional_incurred_lr']    = np.where( (rating_df.display_premium_ol == 0),   0,   rating_df.incurred_att_selected_inflated.astype(float)   /  rating_df.display_premium_ol)
        rating_df['display_attritional_chainladder_lr'] = np.where( (rating_df.display_premium_ol == 0),   0,   rating_df.ultimate_att_cl_selected_ol.astype(float)      /  rating_df.display_premium_ol)
        rating_df['display_attritional_approach']       = rating_df.reserving_method_attritional
        rating_df['display_attritional_selected_lr']    = np.where( (rating_df.display_premium_ol == 0),   0,   rating_df.ultimate_att_meth_selected_ol.astype(float)    /  rating_df.display_premium_ol)
        
        rating_df['display_large_incurred_lr']          = np.where( (rating_df.display_premium_ol == 0),   0,   rating_df.incurred_large_selected_inflated.astype(float) /  rating_df.display_premium_ol)
        rating_df['display_large_chainladder_lr']       = 0
        rating_df['display_large_approach']             = "Incurred"
        rating_df['display_large_selected_lr']          = rating_df.display_large_incurred_lr

        rating_df['display_cat_incurred_lr']            = np.where( (rating_df.display_premium_ol == 0),   0,   rating_df.incurred_cat_selected_inflated.astype(float)   /  rating_df.display_premium_ol)
        rating_df['display_cat_chainladder_lr']         = 0
        rating_df['display_cat_approach']               = "Incurred"
        rating_df['display_cat_selected_lr']            = rating_df.display_cat_incurred_lr


        rating_df['display_show_row_inputs']            = np.where(rating_df.yoa == cy_yoa, False, True)
        rating_df['display_show_row_rating']            = np.where(rating_df.include_selected != "Yes" , False, True)


        ####################################################################################
        ### 23) Calculate Standard Deviation for PC                                      ###
        ####################################################################################

        #note we deliberately exclude Nils as this is the defualt for Null - however there could be genuine Nils that get excluded also - not used for now but coudl be improved
        sd_att  = rating_df[   (rating_df['ultimate_att_meth_selected_ol']   >0) & (rating_df.index.values<15) ]['ultimate_att_meth_selected_ol'   ].std(skipna = True)
        sd_lrg  = rating_df[   (rating_df['incurred_large_selected_inflated']>0) & (rating_df.index.values<15) ]['incurred_large_selected_inflated'].std(skipna = True) 
        sd_cat  = rating_df[   (rating_df['incurred_cat_selected_inflated']  >0) & (rating_df.index.values<15) ]['incurred_cat_selected_inflated'  ].std(skipna = True)

        summary.standard_deviation.attritional   = 0 if np.isnan(sd_att) else   sd_att
        summary.standard_deviation.large         = 0 if np.isnan(sd_lrg) else   sd_lrg
        summary.standard_deviation.catastrophe   = 0 if np.isnan(sd_cat) else   sd_cat

        ####################################################################################
        ### 24) Chart Data - loss ratios                                                 ###
        ####################################################################################

        summary.chart_show_basis_gg = True if summary.chart_basis == "Gross Gross" else False
        summary.chart_show_basis_gn = not summary.chart_show_basis_gg

        rating_df["chart_att_ilr_gg"] = rating_df["incurred_att_selected_lr"]
        rating_df["chart_large_ilr_gg"] = rating_df["incurred_large_selected_lr"]
        rating_df["chart_cat_ilr_gg"] = rating_df["incurred_cat_selected_lr"]

        rating_df["chart_att_ilr_gn"] = rating_df["incurred_att_selected_lr"] / (1-total_deductions)
        rating_df["chart_large_ilr_gn"] = rating_df["incurred_large_selected_lr"] / (1-total_deductions)
        rating_df["chart_cat_ilr_gn"] = rating_df["incurred_cat_selected_lr"] / (1-total_deductions)

        rating_df["chart_att_ilr_ol_gg"] = rating_df["display_attritional_incurred_lr"] * ( rating_df["policy_length_scalant"])
        rating_df["chart_large_ilr_ol_gg"] = rating_df["display_large_incurred_lr"] * ( rating_df["policy_length_scalant"])
        rating_df["chart_cat_ilr_ol_gg"] = rating_df["display_cat_incurred_lr"] * ( rating_df["policy_length_scalant"])

        rating_df["chart_att_ilr_ol_gn"] = rating_df["display_attritional_incurred_lr"] * ( rating_df["policy_length_scalant"]) / (1-total_deductions)
        rating_df["chart_large_ilr_ol_gn"] = rating_df["display_large_incurred_lr"] * ( rating_df["policy_length_scalant"]) / (1-total_deductions)
        rating_df["chart_cat_ilr_ol_gn"] = rating_df["display_cat_incurred_lr"] * ( rating_df["policy_length_scalant"]) / (1-total_deductions)


        rating_df["chart_att_ilr_proposed_gg"] = att.gg_pst_uw_adj.ulr_final
        rating_df["chart_large_ilr_proposed_gg"] = lrg.gg_pst_uw_adj.ulr_final  
        rating_df["chart_cat_ilr_proposed_gg"] = cat.gg_pst_uw_adj.ulr_final  

        rating_df["chart_att_ilr_proposed_gn"] = att.gn_pst_uw_adj.ulr_final
        rating_df["chart_large_ilr_proposed_gn"] = lrg.gn_pst_uw_adj.ulr_final  
        rating_df["chart_cat_ilr_proposed_gn"] = cat.gn_pst_uw_adj.ulr_final  

        ####################################################################################
        ### 25) Chart Data - Premium Breakdown                                           ###
        ####################################################################################
        chart_path = summary.chart_premium_breakdown

        uw_adj_basis = "pst" if chart_path.uw_adj_basis == "Post" else "pre"
        
        chart_path.technical.losses = getattr(tech,f"amts_{uw_adj_basis}_uw_adj").losses_tot_afb
        chart_path.technical.reinsurance = getattr(tech,f"amts_{uw_adj_basis}_uw_adj").reinsurance_afb
        chart_path.technical.cost_of_capital = getattr(tech,f"amts_{uw_adj_basis}_uw_adj").profit_req_afb
        chart_path.technical.expense = ( getattr(tech,f"amts_{uw_adj_basis}_uw_adj").expense_afb
                                            + getattr(tech,f"amts_{uw_adj_basis}_uw_adj").lae_afb
                                            - getattr(tech,f"amts_{uw_adj_basis}_uw_adj").investment_afb
        )

        chart_path.benchmark.losses = getattr(tech,f"amts_{uw_adj_basis}_uw_adj").losses_tot_afb
        chart_path.benchmark.bp_loading = chart_path.benchmark.losses * (1/0.7 - 1)
        

        if chart_path.premium_basis == "Gross Gross":
            chart_path.technical.brokerage = (getattr(tech,f"amts_{uw_adj_basis}_uw_adj").gg_premium_tech_afb
                                                - chart_path.technical.losses
                                                - chart_path.technical.reinsurance
                                                - chart_path.technical.cost_of_capital
                                                - chart_path.technical.expense
            )
            
            chart_path.benchmark.brokerage = (getattr(tech,f"amts_{uw_adj_basis}_uw_adj").gg_premium_bench_afb
                                                - (chart_path.benchmark.losses / 0.7)
            )

            chart_path.client.client_premium = tech.gg_premium_quoted_afb
            
        else:
            chart_path.technical.brokerage = 0
            chart_path.benchmark.brokerage = 0
            chart_path.client.client_premium = tech.gg_premium_quoted_afb * (1 - total_deductions)

        ####################################################################################
        ### 26) Chart Data - ILR by claim type and yoa                                   ###
        ####################################################################################

        rating_df["chart_att_ilr"]      = rating_df['incurred_att_selected_lr'] 
        rating_df["chart_large_ilr"]    = rating_df['incurred_large_selected_lr'] 
        rating_df["chart_cat_ilr"]      = rating_df['incurred_cat_selected_lr'] 

        if chart_path.premium_basis == "Gross Net":
            rating_df["chart_att_ilr"]  = rating_df["chart_att_ilr"] / (1 - total_deductions)
            rating_df["chart_large_ilr"] = rating_df["chart_large_ilr"] / (1 - total_deductions)
            rating_df["chart_cat_ilr"] = rating_df["chart_cat_ilr"] / (1 - total_deductions)

        if chart_path.uw_adj_basis == "Post":
            rating_df["chart_att_ilr"] = rating_df["chart_att_ilr"] * (1 + (att.uw_adjustment or 0))
            rating_df["chart_large_ilr"] = rating_df["chart_large_ilr"] * (1 + (lrg.uw_adjustment or 0))
            rating_df["chart_cat_ilr"] = rating_df["chart_cat_ilr"] * (1 + (cat.uw_adjustment or 0))    


        ####################################################################################
        ### 27) Chart Data - Total LR summary by YOA                                     ###
        ####################################################################################

        rating_df["chart_premium"] = rating_df['premium_selected']
        rating_df["chart_pricing_lr"] = tot.gg_pst_uw_adj.ulr_priced_final if chart_path.uw_adj_basis == "Post" else tot.gg_pre_uw_adj.ulr_priced_final
        rating_df["chart_experience_lr"] = rating_df["chart_att_ilr"] + rating_df["chart_large_ilr"] + rating_df["chart_cat_ilr"] 

        if chart_path.premium_basis == "Gross Net":
            rating_df["chart_premium"] = rating_df["chart_premium"] / (1 - total_deductions)
            rating_df["chart_pricing_lr"] = rating_df["chart_pricing_lr"] / (1 - total_deductions)
            rating_df["chart_experience_lr"] = rating_df["chart_experience_lr"] / (1 - total_deductions)
     



        ####################################################################################
        ### 28) Write to HXD                                                             ###
        ####################################################################################

        output_columns_str      =["include_suggested"
                                    ,"include_selected"
                                    ,"reserving_method_attritional"
                                    ,"display_yoa"
                                    ,"display_attritional_approach"
                                    ,"display_large_approach"
                                    ,"display_cat_approach"
                                    ]
        output_columns_date     = ["incept_date"
                                    ,"expiry_date"
                                    ,"expiry_date_annual_est"
                                    ]

        output_columns_bool     = ["display_show_row_inputs"
                                    ,"display_show_row_rating"
                                    ]


        output_columns_flt      = ["yoa"
                                    ,"include_selected_weight"
                                    ,"policy_length_calc"
                                    ,"policy_length_selected"
                                    ,"policy_length_scalant"
                                    ,"maturity"
                                    ,"port_chg_suggested"
                                    ,"port_chg_selected"
                                    ,"port_chg_cumul_prior"
                                    ,"port_chg_cumul_suggested"
                                    ,"port_chg_cumul_selected"
                                    ,"rate_chg_account"
                                    ,"rate_chg_portfolio"
                                    ,"rate_chg_suggested"
                                    ,"rate_chg_selected"
                                    ,"rate_chg_cumul_prior"
                                    ,"rate_chg_cumul_suggested"
                                    ,"rate_chg_cumul_selected"
                                    ,"infl_chg_suggested"
                                    ,"infl_chg_selected"
                                    ,"infl_chg_cumul_prior"
                                    ,"infl_chg_cumul_suggested"
                                    ,"infl_chg_cumul_selected"
                                    ,"experience_default_perc_ult"
                                    ,"experience_selected_perc_ult"
                                    ,"benchmark_default_perc_ult"
                                    ,"benchmark_selected_perc_ult"
                                    ,"blended_default_perc_ult"
                                    ,"blended_selected_perc_ult"
                                    ,"interp_blended_selected_perc_ult"
                                    ,"premium_prior"
                                    ,"premium_suggested"
                                    ,"premium_selected"
                                    ,"premium_selected_ol"
                                    ,"premium_selected_ol_scaled"
                                    ,"incurred_prior"
                                    ,"paid_listing"
                                    ,"incurred_listing"
                                    ,"incurred_pp_blend"
                                    ,"incurred_pp_most_likely"
                                    ,"incurred_triangle"
                                    ,"incurred_suggested"
                                    ,"incurred_selected"
                                    ,"large_threshold_usd"
                                    ,"large_threshold_sett_fx"
                                    ,"incurred_large_prior"
                                    ,"paid_large_listing"
                                    ,"incurred_large_listing"
                                    ,"incurred_large_pp_blend"
                                    ,"incurred_large_pp_most_likely"
                                    ,"incurred_large_triangle"
                                    ,"incurred_large_suggested"
                                    ,"incurred_large_selected"
                                    ,"incurred_large_selected_lr"
                                    ,"incurred_large_selected_inflated"
                                    ,"incurred_cat_prior"
                                    ,"paid_cat_listing"
                                    ,"incurred_cat_listing"
                                    ,"incurred_cat_pp_blend"
                                    ,"incurred_cat_pp_most_likely"
                                    ,"incurred_cat_triangle"
                                    ,"incurred_cat_suggested"
                                    ,"incurred_cat_selected"
                                    ,"incurred_cat_selected_lr"
                                    ,"incurred_cat_selected_inflated"
                                    ,"paid_att_listing"
                                    ,"incurred_att_listing"
                                    ,"incurred_att_pp_blend"
                                    ,"incurred_att_pp_most_likely"
                                    ,"incurred_att_triangle"
                                    ,"incurred_att_suggested"
                                    ,"incurred_att_override"
                                    ,"incurred_att_selected"
                                    ,"incurred_att_selected_lr"
                                    ,"incurred_att_selected_inflated"
                                    ,"ultimate_att_cl_selected"
                                    ,"ultimate_att_cl_selected_py_factors"
                                    ,"ultimate_att_cl_selected_py_factors_data"
                                    ,"ultimate_att_cl_selected_ol"
                                    ,"ultimate_att_cl_selected_ol_exc_scalant"
                                    ,"ultimate_att_cl_selected_ol_py_ol_assump"
                                    ,"ultimate_att_cl_selected_ol_py_factors"
                                    ,"ultimate_att_cl_selected_ol_py_factors_data"
                                    ,"ultimate_att_meth_selected_ol"
                                    ,"ultimate_att_meth_selected_ol_exc_scalant"
                                    ,"ultimate_att_meth_selected_ol_py_ol_assump"
                                    ,"ultimate_att_meth_selected_ol_py_factors"
                                    ,"ultimate_att_meth_selected_ol_py_factors_data"
                                    ,"weighting_exposure"
                                    ,"weighting_decay"
                                    ,"weighting_development"
                                    ,"weighting_combined"
                                    ,"weighting_final"
                                
                                    ,"display_premium_ol"
                                    ,"display_attritional_weight"

                                    ,"display_attritional_incurred_lr"
                                    ,"display_attritional_chainladder_lr"
                                    ,"display_attritional_selected_lr"
                                    
                                    ,"display_large_incurred_lr"
    #                                ,"display_large_chainladder_lr"#not passing so it remains null/blank
                                    ,"display_large_selected_lr"

                                    ,"display_cat_incurred_lr"
    #                                ,"display_cat_chainladder_lr"  #not passing so it remains null/blank
                                    ,"display_cat_selected_lr"

                                    ,"chart_att_ilr_gg"
                                    ,"chart_large_ilr_gg"
                                    ,"chart_cat_ilr_gg"
                                    ,"chart_att_ilr_gn"
                                    ,"chart_large_ilr_gn"
                                    ,"chart_cat_ilr_gn"
                                    ,"chart_att_ilr_ol_gg"
                                    ,"chart_large_ilr_ol_gg"
                                    ,"chart_cat_ilr_ol_gg"
                                    ,"chart_att_ilr_ol_gn"
                                    ,"chart_large_ilr_ol_gn"
                                    ,"chart_cat_ilr_ol_gn"
                                    ,"chart_att_ilr_proposed_gg"
                                    ,"chart_large_ilr_proposed_gg"
                                    ,"chart_cat_ilr_proposed_gg"
                                    ,"chart_att_ilr_proposed_gn"
                                    ,"chart_large_ilr_proposed_gn"
                                    ,"chart_cat_ilr_proposed_gn"

                                    ,"chart_att_ilr"
                                    ,"chart_large_ilr"
                                    ,"chart_cat_ilr"

                                    ,"chart_premium"
                                    ,"chart_pricing_lr"
                                    ,"chart_experience_lr"

                                ]

        dummy_date = pd.to_datetime(const.dum_old_date, format='%Y%m%d')
        rating_df[output_columns_str ] = rating_df[output_columns_str ].fillna('')
        rating_df[output_columns_date] = rating_df[output_columns_date].fillna(dummy_date)
        rating_df[output_columns_flt ] = rating_df[output_columns_flt ].fillna(0)

        write_pd_to_hxd(rating_df,  summary.detail_by_year,  output_columns_str + output_columns_date + output_columns_flt + output_columns_bool)


        # timer.end("step 26")

        
        ####################################################################################
        ### 29) Write to Standard CDS fields                                             ###
        ####################################################################################

        # map to standard  cds fields
        
        rating_info.benchmark_premium            = tech.amts_pst_uw_adj.gg_premium_tech_afb 
        rating_info.bpi                          = kpi.pst_uw_adj.bpi
        rating_info.bpi_pre_uw_adj               = kpi.pre_uw_adj.bpi 
        rating_info.technical_premium            = tech.amts_pst_uw_adj.gg_premium_tech_afb
        rating_info.technical_premium_pre_uw_adj = tech.amts_pre_uw_adj.gg_premium_tech_afb
        rating_info.technical_premium_net        = tech.amts_pst_uw_adj.gn_premium_tech_inc_pc_afb   # this is gross net, where we also net off PC
        rating_info.tpi                          = kpi.pst_uw_adj.tpi
        rating_info.tpi_pre_uw_adj               = kpi.pre_uw_adj.tpi 
        rating_info.pflr_att                     = (att.gg_pst_uw_adj.ulr_final + lrg.gg_pst_uw_adj.ulr_final)    / (1 - percent_pc - total_deductions)
        rating_info.pflr_cat                     = (cat.gg_pst_uw_adj.ulr_final)                                  / (1 - percent_pc - total_deductions)
        rating_info.pflr                         = rating_info.pflr_att + rating_info.pflr_cat 
        rating_info.roc                          = kpi.pst_uw_adj.roc
        rating_info.uw_adj_impact                = 0 if tech.amts_pst_uw_adj.losses_tot_afb == 0 else (tech.amts_pre_uw_adj.losses_tot_afb  /  tech.amts_pst_uw_adj.losses_tot_afb) -1
        rating_info.expected_loss_cost           = tech.amts_pst_uw_adj.losses_tot_afb
        rating_info.expected_loss_cost_pre_uw_adj= tech.amts_pre_uw_adj.losses_tot_afb
       
        
        #Calculates weighted Expected loss (I dont think this includes nmp. is it part of the bbt and should be be added here?)
        #if ((cds.att_and_large.exp_loss is not None) and (cds.cat.exp_loss is not None)):
        pre_uw_adj_weighted_expected_loss =  prem * (1-total_deductions) * tot.gn_pre_uw_adj.ulr_priced_final_exc_pc
        post_uw_adj_weighted_expected_loss = prem * (1-total_deductions) * tot.gn_pst_uw_adj.ulr_priced_final_exc_pc




        ########### assign UW adjustments for TP and BP components ##############

            ############### TPI and BPI Calcs ####################

        gg_beazley_share_prem_inc_pc = rating_info.quoted_premium_100pct * line_use
        gg_beazley_share_prem_exc_pc = gg_beazley_share_prem_inc_pc * (1 - percent_pc)
        gn_beazley_share_prem_inc_pc = rating_info.quoted_premium_100pct * line_use  * (1 - total_deductions)
        gn_beazley_share_prem_exc_pc = gn_beazley_share_prem_inc_pc * (1 - percent_pc)

        # this doesnt appear to be used anywhere
    #    post_uw_adj_weighted_exposure_gn_bpi_inc_pc =  gn_beazley_share_prem_inc_pc / (( post_uw_adj_weighted_expected_loss / const.benchmark_lr) * (1 - total_deductions))

    

            
        #check all the async tasks are up to date 

    if hxd.cds.layers[0].status == "Bound" and hxd.cds.layers[0].signed_line != 0:
        line_use = hxd.cds.layers[0].signed_line
    else:
        line_use = hxd.cds.layers[0].written_line

    data_consistent_test_exposure = False
    data_consistent_test_experience = False
    data_consistent_test_pc = False

    a = hxd.cds.layers[0].quoted_premium_100pct
          
    if hxd.cds.sch_check_async.experience_premium is not None: 

        data_consistent_test_experience  = ((round(hxd.cds.layers[0].quoted_premium_100pct, 4)  ==  round(hxd.cds.sch_check_async.experience_premium, 4))
                                                 & (round(hxd.cds.layers[0].total_deductions,4)  ==  round(hxd.cds.sch_check_async.experience_deductions , 4))
                                                    & (round(line_use, 4)  ==  round(hxd.cds.sch_check_async.experience_signed_line , 4)))
                               
    if hxd.cds.sch_check_async.exposure_premium is not None: 

        data_consistent_test_exposure  = ((round(hxd.cds.layers[0].quoted_premium_100pct,4)   ==  round(hxd.cds.sch_check_async.exposure_premium,  4))
                                                 & (round(hxd.cds.layers[0].total_deductions,4)  ==  round(hxd.cds.sch_check_async.exposure_deductions, 4))
                                                    & (round(line_use, 4)  ==  round(hxd.cds.sch_check_async.exposure_signed_line ,  4)))


    if hxd.cds.sch_check_async.pc_premium is not None: 

            data_consistent_test_pc  =           ((round(hxd.cds.layers[0].quoted_premium_100pct, 4)   ==  round(hxd.cds.sch_check_async.pc_premium  , 4))
                                                 & (round(hxd.cds.layers[0].total_deductions  , 4)  ==  round(hxd.cds.sch_check_async.pc_deductions  ,  4))
                                                 & (round(line_use ,  4)  ==  round(hxd.cds.sch_check_async.pc_signed_line , 4)))
                                                 


    if (data_consistent_test_experience) :
            pass

    else:
        if hxd.cds.sch_check_async.experience_premium is not None:
                hx.errors.validation(f"Experience needs rerunning")

    if (data_consistent_test_exposure) :
            pass
            

    else:
        if hxd.cds.sch_check_async.exposure_premium is not None :
                hx.errors.validation(f"Exposure needs rerunning")
                
    if(data_consistent_test_pc):
            pass
            

    else: 
        if hxd.cds.sch_check_async.pc_premium  is not None :
                hx.errors.validation(f"PC needs rerunning")
               
            

