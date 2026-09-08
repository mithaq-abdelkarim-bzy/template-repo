##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################
### WARNING - 
### Below code for bi_clm_and_mvmt_fetch takes 2 paths: (i) where we load triangles & listing; (ii) just load listing
### There is some repeat code to handle identification of attritional/large/cat/lf accordingly
### [BlockIndicator] when taken from [ClaimMovementSectionCombinedView] table is a "Yes" / "No" field
### [BlockIndicator] when taken from [ClaimExposureSectionCombinedView] table is a True / False field

##############################################################################################################################
##############################################################################################################################

import hx, pyodbc
import pandas as pd
import numpy as np
import datetime     #use to build date - datetime.date(1990,1,1)
import algorithms.rate_constants as const
from dateutil.relativedelta import relativedelta
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, write_pd_to_hxd_no_overrides



#######################################################################################################
### BEGIN SELECT/DESELECT ALL FACILITIES                                                            ###
#######################################################################################################

### Used to select all facilities in the bi facility fetch - toggle all values based on the first selected value
def bi_facility_include_all(hxd,progress):
    cds = hxd.cds
    value_to_assign = True
    for index, i in enumerate(cds.bi_data.facility_detail):
        i.include = value_to_assign

### Used to deselect all facilities in the bi facility fetch - toggle all values based on the first selected value
def bi_facility_exclude_all(hxd,progress):
    cds = hxd.cds
    value_to_assign = False
    for index, i in enumerate(cds.bi_data.facility_detail):
        i.include = value_to_assign


#######################################################################################################
### END SELECT/DESELECT ALL FACILITIES                                                                ###
#######################################################################################################







#######################################################################################################
### BEGIN FACILITY FETCH - Pulling all relevant BI facility data and loading into relevant nodes        ###
#######################################################################################################

def bi_facility_fetch(hxd,progress):
    
    
    cds = hxd.cds
    
  
    if  (cds.standard_fields.facility_reference is None):
        cds.bi_data.fetch_facility_detail_task_status = "Please enter a master binder reference"
        return

    cy_facility_ref = cds.standard_fields.facility_reference #'B7268C23ANVE' #
    cy_facility_ref = cy_facility_ref.upper()

    # Building the field index_ref to use in the sql IN statement
    index_ref = "'" + cy_facility_ref[:6] + "'"
    if cds.bi_data.include_all_facility_references:
        ref2 = "" if (cds.risk_info.facility_reference2 is None) else (",'" + cds.risk_info.facility_reference2[:6] + "'") 
        ref3 = "" if (cds.risk_info.facility_reference3 is None) else (",'" + cds.risk_info.facility_reference3[:6] + "'") 
        ref4 = "" if (cds.risk_info.facility_reference4 is None) else (",'" + cds.risk_info.facility_reference4[:6] + "'") 
        ref5 = "" if (cds.risk_info.facility_reference5 is None) else (",'" + cds.risk_info.facility_reference5[:6] + "'") 
        ref6 = "" if (cds.risk_info.facility_reference6 is None) else (",'" + cds.risk_info.facility_reference6[:6] + "'") 
        ref7 = "" if (cds.risk_info.facility_reference7 is None) else (",'" + cds.risk_info.facility_reference7[:6] + "'") 
        index_ref = index_ref + ref2 + ref3 + ref4 + ref5 + ref6 + ref7

   
     
    # Query
    query1 = f"""
                    SELECT      
                        GETDATE() as date_extracted
                        ,[SectionReference]
                        ,[InsuredParty]
                        ,[InceptionDate]
                        ,[ExpiryDate]
                        ,[UnderwriterName]
                        ,[SettlementCurrency]
                        ,[SectionIsRenewal]  
                        ,[Division]  
                        ,[TotalWrittenIfNotSignedMultiplier]  
                        ,[TriFocusName]
                        ,[ExternalAcquisitionCostMultiplier]
                        ,[ProfitCommissionMultiplier]
                        ,[PlacingBrokerName]
                        ,[RiskClassCode]
                        ,[YOA]
                        ,[WrittenOrEstimatedPremium]
                        ,[RateChangeDivisor]
    
                    FROM [BeazleyIntelligenceDataSets].[Report].[SectionCombinedView]
                    WHERE Left(SectionReference,6) IN ({index_ref})
                    Order by [YOA] Desc
            """

    columns1 =  ['date_extracted'
                    , 'section_reference'
                    , 'insured_party'
                    , 'inception_date'
                    , 'expiry_date'
                    , 'underwriter_name'
                    , 'settlement_currency'
                    , 'section_is_renewal'
                    , 'division'
                    , 'written_or_estimated_signed_line'
                    , 'trifocus_name'
                    , 'external_acquisition_cost_multiplier'
                    , 'profit_commission_multiplier'
                    , 'placing_brokername'
                    , 'risk_class_code'
                    , 'yoa'
                    , 'written_or_estimated_premium'
                    , 'rate_change_divisor'
                ]



    # pull facility detail for all facilities from sql based on query 1
    facility_detail_df  = query_bi_database(query1, columns1) 


    # determine if data has been returned
    if facility_detail_df.empty:
        # do nothing
        cds.bi_data.fetch_facility_detail_task_status = "Facility Information not found for entered references"
        return

    # assign false here so it resets the include status on load - it could be enhanced by looking up values associated with facility ids from last load if there was one
    facility_detail_df['include'] = False
    facility_detail_df = facility_detail_df.fillna(const.dum_large_neg)
    setattr(cds.bi_data,"facility_detail",facility_detail_df.to_dict("records"))
    

    # filtering the dataframe to just main facility and assigning status
    main_facility_df = facility_detail_df.loc[ facility_detail_df.section_reference == cy_facility_ref ]
    cy_facility_success = main_facility_df.empty == False
    cds.bi_data.fetch_facility_detail_task_status = "" if main_facility_df.empty else "BI Binder Information successfully retrieved. Core fields populated from main binder reference." 


    # filtering the dataframe to just expiring main facility and assigning status where expiring main facility found
    if main_facility_df.empty and cy_facility_ref[6:8].isdigit():
        py_year_num  = int(cy_facility_ref[6:8]) -1
        py_year_text = "00" + str(py_year_num) 
        py_year_text = py_year_text[-2:]
        py_facility_ref = cy_facility_ref[:6] + py_year_text + cy_facility_ref[8:]                
        main_facility_df = facility_detail_df.loc[ facility_detail_df.section_reference == py_facility_ref ]
        cds.bi_data.fetch_facility_detail_task_status = "" if  main_facility_df.empty else "BI Binder Information successfully retrieved. Core fields populated from expiring binder reference  - update as necessary."


    # assigning status where cant identify suitable facility for core fields
    if main_facility_df.empty:
        cds.bi_data.fetch_facility_detail_task_status = "BI Binder Information successfully retrieved. Core fields not populated (no current/expiring) - please fill manually." 
    else:
            
       # where succesful we need to push data to the following fields
        #cds.standard_fields.insured_name        = main_facility_df['insured_party'].iat[0]
        #cds.standard_fields.underwriter         = main_facility_df['underwriter_name'].iat[0]
        #cds.currencies.source_currency          = main_facility_df['settlement_currency'].iat[0]
        #cds.layers[0].written_line              = main_facility_df['written_or_estimated_signed_line'].iat[0]
        #cds.standard_fields.trifocus            = main_facility_df['trifocus_name'].iat[0]
        #cds.layers[0].commission                = main_facility_df['external_acquisition_cost_multiplier'].iat[0]                     
        #cds.profit_commission.scenarios[0].share= main_facility_df['profit_commission_multiplier'].iat[0]
        #cds.standard_fields.broker              = main_facility_df['placing_brokername'].iat[0]

        #hxd.hx_core.inception_date              = main_facility_df['inception_date'].iat[0] if cy_facility_success else (main_facility_df['inception_date'].iat[0]  +  relativedelta(years=+1))
        #hxd.hx_core.expiry_date                 = main_facility_df['expiry_date'].iat[0] if cy_facility_success else (hxd.hx_core.inception_date  +  relativedelta(years=+1, days = -1) )
        #cds.standard_fields.is_renewal          = facility_detail_df['section_is_renewal'].iat[0]

        assigned_trifocus                       = main_facility_df['trifocus_name'].iat[0]
        tfg_df                                  = hx.params.table_tfgmappings
        trifocus_valid                          = (tfg_df[tfg_df["Trifocus"] == assigned_trifocus].empty == False)
        if trifocus_valid == False:
           cds.bi_data.fetch_facility_detail_task_status += "\r\n" + " TRIFOCUS NOT RECOGNISED. PLEASE UPDATE OR USE PROXY OVERRIDE TO PROCEED"


        #cds.layers[0].quoted_premium_100pct        =  (main_facility_df['written_or_estimated_premium'].iat[0]/(1-main_facility_df['external_acquisition_cost_multiplier'].iat[0]))/main_facility_df['written_or_estimated_signed_line'].iat[0]

#######################################################################################################
### END FACILITY FETCH - Pulling all relevant BI facility data and loading into relevant nodes      ###
#######################################################################################################







#############################################################################################################################
### BEGIN CLAIMS & MOVEMENTS - Pulling all relevant BI Claims and Movements and loading into relevant nodes               ###
#############################################################################################################################
def bi_clm_and_mvmt_fetch(hxd,progress,include_triangles):
    
    # these are for the async task check 
    
    #hxd.cds.sch_check_async.experience_premium = hxd.cds.layers[0].quoted_premium_100pct
    #hxd.cds.sch_check_async.experience_deductions = hxd.cds.layers[0].total_deductions

    #if hxd.cds.layers[0].status == "Bound" and hxd.cds.layers[0].signed_line != 0:
     #   hxd.cds.sch_check_async.experience_signed_line = hxd.cds.layers[0].signed_line
    #else:
     #   hxd.cds.sch_check_async.experience_signed_line = hxd.cds.layers[0].written_line
           
    cds = hxd.cds
    
    ################################################    
    ## 1) Error Trapping and Prepping for Import
    ################################################

    # Load facility detail and test if empty - in which case update task status and exit
    facility_detail_df = pd_df_from_hx_list(cds.bi_data.facility_detail)
    if facility_detail_df.empty:
        cds.bi_data.fetch_clm_and_mvmt_detail_task_status = "Please load and select binders to proceed."
        return
   
    # concatenate all rows of facility references, where included, with appropriate syntax for SQL IN statements and return a single value.
    facility_detail_df.loc[facility_detail_df.include,        'included_facility_reference'] = (",'" + facility_detail_df.section_reference + "'")
    facility_detail_df.loc[facility_detail_df.include==False, 'included_facility_reference'] = ""
    index_ref = ''.join(facility_detail_df.included_facility_reference)
    index_ref = index_ref[1:]


    # Test if index_ref is empty - in which case update task status and exit
    if index_ref =='' and cds.standard_fields.benchmark_class is None:
        cds.bi_data.fetch_clm_and_mvmt_detail_task_status = "Please select some binders to proceed and enter a TriFocus."
        return

    if cds.standard_fields.benchmark_class is None:
        cds.bi_data.fetch_clm_and_mvmt_detail_task_status = "Please enter a TriFocus."
        return

    if index_ref =='':
        cds.bi_data.fetch_clm_and_mvmt_detail_task_status = "Please select some binders to proceed."
        return

    if cds.currencies.source_currency =='':
        cds.bi_data.fetch_clm_and_mvmt_detail_task_status = "Please enter a settlement currency to proceed."
        return

    # Determine whether to use EuroBase table or Combined
    lst_benchgroup_using_eurobase = hx.params.lst_benchgroup_using_eurobase
    test_view = lst_benchgroup_using_eurobase[ lst_benchgroup_using_eurobase['BenchmarkGroup'] == cds.standard_fields.benchmark_class].empty
    exposure_table = "ClaimExposureSectionCombinedView" if test_view else "ClaimExposureSectionEurobaseView"
    movement_table = "ClaimMovementSectionCombinedView" if test_view else "ClaimMovementSectionEurobaseView"


    incept_date_less_1_day = (hxd.hx_core.inception_date + relativedelta(days = -1)).strftime('%Y-%m-%d') 
    if hxd.hx_core.inception_date.month == 3 and hxd.hx_core.inception_date.day == 1:                           #handling leap year
       incept_date_less_1_day = (hxd.hx_core.inception_date +  relativedelta(days = -2)).strftime('%Y-%m-%d')

    ################################################    
    ## 2a) Policy Premium Load - call procedure to fx convert premium and load current year premium where available
    ################################################
    update_premium_table(hxd,progress)



    ################################################    
    ## 2b) Claims Query
    ################################################
    query1 = f"""
                        SELECT
                            GETDATE() as date_extracted
                            ,[SectionReference]
                            ,[ClaimReference]
                            ,[ExposureReference]
                            ,isnull([PolicyYOA],1990)  as 'YoA'
                            ,isnull([BeazleyCatCode],'') as 'BeazleyCatCode'
                            ,isnull([MarketCatCode],'') as 'MarketCatCode'
                            ,isnull([TriFocusName],'') as 'TriFocusName'
                            ,isnull([SettlementCurrency],'') as 'SettlementCurrency'
                            ,isnull([BlockIndicator],'') as 'BlockIndicator'
                            ,isnull([DateOfLoss],'1990-01-01') as 'DateOfLoss'
                            ,isnull([ClaimMadeDate],'1990-01-01') as 'ClaimMadeDate'
                            ,isnull([ClaimOrCircumstance],'') as 'ClaimOrCircumstance'
                            ,isnull([BeazleyShareTotalIncurred],0) as 'BeazleyShareTotalIncurred'
                            ,isnull([SlipOrderTotalIncurred],0) as 'SlipOrderTotalIncurred'
                            ,isnull([SlipOrderTotalPaid],0) as 'SlipOrderTotalPaid'
							,isnull([BeazleySharePrePeerBlend],0)	as 'BeazleySharePrePeerBlend'
							,isnull([BeazleySharePrePeerMostLikely],0) as 'BeazleySharePrePeerMostLikely'

                        FROM [BeazleyIntelligenceDataSets].[Report].[{exposure_table}]
                        WHERE   [SectionReference] IN ({index_ref})
                """

    columns1 =  ['date_extracted'
                    , 'section_reference'
                    , 'claim_reference'
                    , 'exposure_reference'
                    , 'yoa'
                    , 'beazley_catcode'
                    , 'market_catcode'
                    , 'trifocus_name'
                    , 'settlement_currency'
                    , 'block_indicator'
                    , 'date_of_loss'
                    , 'claim_made_date'
                    , 'claim_or_circumstance'
                    , 'beazley_share_total_incurred'
                    , 'slip_order_total_incurred'
                    , 'slip_order_total_paid'
                    , 'beazley_share_pre_peer_blend'
                    , 'beazley_share_pre_peer_most_likely'
                ]


    ################################################
    ## 3) Claims Movements Query
    ################################################
    if include_triangles == True:
        query2 = f"""
                                DECLARE @NewInceptDate_less1 AS DATE	
                                SELECT @NewInceptDate_less1 = '{incept_date_less_1_day}'	

                                DECLARE @LastMovementDate AS DATE																						
                                SELECT @LastMovementDate = IIF(GETDATE()<@NewInceptDate_less1, GETDATE(),@NewInceptDate_less1)
                                    
                                SELECT                     	
                                    GETDATE() as date_extracted                      	
                                    , [ExposureReference]                       	
                                    , isnull([Division],'') as 'Division'                     	
                                    , isnull([BlockIndicator],'') as 'BlockIndicator'                       	
                                    , isnull([BeazleyCatCode],'') as 'BeazleyCatCode'                       	
                                    , isnull(year([InceptionDate]),1990) as 'YoA'                           	
                                    , sum([BeazleyShareMovementIncurredDefence] * [ExchangeRate]                           	
                                            +  [BeazleyShareMovementIncurredFees] * [ExchangeRate]                        	
                                            +  [BeazleyShareMovementIncurredIndemnity] * [ExchangeRate]) as 'incurred_mvmt'                           	
                                    , AVG([TotalWrittenIfNotSignedMultiplier]) AS signed_line                      	     	
                                    , (   isnull(YEAR([movementdate]) ,1990) 																					
                                        - isnull(YEAR([InceptionDate]),1990)																					
                                        + iif(DATEFROMPARTS(YEAR(@LastMovementDate),MONTH([InceptionDate]),	 DAY([InceptionDate]))     < @LastMovementDate,   1, 0)																
                                        - iif(DATEFROMPARTS(YEAR([movementdate]),   MONTH(@LastMovementDate),DAY(  @LastMovementDate)) > [movementdate]   ,   1, 0)
                                        +1) as dev_yr	

                                FROM [BeazleyIntelligenceDataSets].[Report].[{movement_table}]                        	
                                WHERE   [SectionReference] IN (
                                    SELECT DISTINCT [SectionReference]
								    FROM [BeazleyIntelligenceDataSets].[Report].[ClaimMovementSectionCombinedView]
								    WHERE   [SectionReference] IN ({index_ref})
                                    )
                                            AND [movementdate] <= @NewInceptDate_less1	
                                GROUP BY                          	
                                    [ExposureReference]                         	
                                    , isnull([Division],'')                     	
                                    , isnull([BlockIndicator],'')                      	
                                    , isnull([BeazleyCatCode],'')                      	
                                    , isnull(year([InceptionDate]),1990)                      	     	
                                    , case when ([movementdate] > DATEFROMPARTS(year([movementdate])	
                                                                                ,month(IIF(GETDATE()<@NewInceptDate_less1, GETDATE(),@NewInceptDate_less1))	
                                                                                ,day(IIF(GETDATE()<@NewInceptDate_less1, GETDATE(),@NewInceptDate_less1)))) 	
                                                    then (Year([movementdate]) - isnull(year([InceptionDate]),1990) +1) 	
                                                    else (Year([movementdate]) - isnull(year([InceptionDate]),1990) )	
                                                    end
                                    , (   isnull(YEAR([movementdate]) ,1990) 																					
                                        - isnull(YEAR([InceptionDate]),1990)																					
                                        + iif(DATEFROMPARTS(YEAR(@LastMovementDate),MONTH([InceptionDate]),	 DAY([InceptionDate]))     < @LastMovementDate,   1, 0)																
                                        - iif(DATEFROMPARTS(YEAR([movementdate]),   MONTH(@LastMovementDate),DAY(  @LastMovementDate)) > [movementdate]   ,   1, 0)
                                        +1)                                             	
                    """

        columns2 =  ['date_extracted'
                        , 'exposure_reference'
                        , 'division'
                        , 'block_indicator'
                        , 'beazley_catcode'
                        , 'yoa'
                        , 'incurred_mvmt'
                        , 'signed_line'
                        , 'mvmt_yr'
                    ]

    ########################################################
    ## 4) Query databases - errortrapping no records returned
    ########################################################

    ## Pull Claims information, test empty
    claim_summary_detail_df  = query_bi_database(query1, columns1) 
 
    # determine if data has been returned and where not update status and exit
    if claim_summary_detail_df.empty:
        # do nothing
        cds.bi_data.fetch_clm_and_mvmt_detail_task_status = "Warning: no claim Information found for selected references"
        return


    ## Pull Claims Movement information, test empty
    if include_triangles == True:
        claim_mvmt_detail_df     = query_bi_database(query2, columns2)
        
        # determine if data has been returned and where not update status and exit
        if claim_mvmt_detail_df.empty:
            # do nothing
            cds.bi_data.fetch_clm_and_mvmt_detail_task_status = "Claim Movement Information not found for selected references"
            return






    ################################################################################################
    ## 5) Determine large loss threshold for Claims Movement Manipulation
    ################################################################################################

    cy_yoa              = hxd.hx_core.inception_date.year   

    # get fx for translating threshold
    currency_rates_bi_df= hx.params.table_currencyratebicurrent
    fx_rate_usd_row     = currency_rates_bi_df[ (currency_rates_bi_df['Currency'] == "USD") ]
    fx_rate_sett_row    = currency_rates_bi_df[ (currency_rates_bi_df['Currency'] == cds.currencies.source_currency) ]
    condition_fx        = (fx_rate_usd_row.empty) or (fx_rate_sett_row.empty)   
    fx_rate             = 1 if condition_fx else fx_rate_sett_row.ExchangeRate.iat[0] / fx_rate_usd_row.ExchangeRate.iat[0]


    # determine loss threshold
    benchmark_parameters_df  = hx.params.table_benchmarkclassparameters
    large_threshold_row_df   = benchmark_parameters_df[(benchmark_parameters_df['Item'] == "Large Loss Threshold") 
                                                        & (benchmark_parameters_df['Benchmark Class'] == cds.standard_fields.benchmark_class)]
    large_threshold_usd      = const.dum_large_int    if large_threshold_row_df.empty   else large_threshold_row_df['Value'].iat[0]
    large_threshold_sett_fx  = large_threshold_usd * fx_rate


    # inflation - load, filter and check available
    infl_chg_df         = hx.params.table_inflationchange
    infl_chg_rows_df    = infl_chg_df[ infl_chg_df['Benchmark Class']  ==  cds.standard_fields.benchmark_class]
    infl_chg_check      = infl_chg_rows_df.empty


    # build thres_df to detail amounts by year - note it we have to work on suggested not selected given the time this takes place in the rating algorithm
    thres_df                            = pd.DataFrame()
    thres_df['yoa']                     = [(cy_yoa - const.default_num_years + x) for x in range(const.default_num_years +1 )] # including current year
    thres_df['infl_chg_suggested']      = [ (1 if infl_chg_check else     ( infl_chg_rows_df[(infl_chg_rows_df['Year'] == x) ]['Value'].iat[0]))       for x in thres_df.yoa]
    thres_df['infl_chg_cumul_suggested']= thres_df['infl_chg_suggested'][::-1].fillna(0).add(1).cumprod()[::-1]   / thres_df['infl_chg_suggested'].fillna(0).add(1)  # [::-1] reverses the series order - notice we do it at start and end 
    thres_df['large_threshold_sett_fx'] = large_threshold_sett_fx  / thres_df['infl_chg_cumul_suggested']



    ################################################
    ## 6) Claims Movement Manipulation
    ################################################

    if include_triangles == True:
        # force datatypes to numeric, set incurred amounts to nil for nan, and signed line to one for na, make sure a development period less than 1 can never occur
        claim_mvmt_detail_df.incurred_mvmt = pd.to_numeric(claim_mvmt_detail_df.incurred_mvmt,errors='coerce').fillna(0)
        claim_mvmt_detail_df.signed_line   = pd.to_numeric(claim_mvmt_detail_df.signed_line ,errors='coerce').fillna(1)
        claim_mvmt_detail_df.mvmt_yr       = np.where(claim_mvmt_detail_df.mvmt_yr <1, 1, claim_mvmt_detail_df.mvmt_yr)

        # calculate 100 percent incurred amount, handling Nils    
        claim_mvmt_detail_df['incurred_mvmt_100'] = np.where( ( claim_mvmt_detail_df.signed_line == 0)
                                                                , 0
                                                                , claim_mvmt_detail_df.incurred_mvmt / claim_mvmt_detail_df.signed_line )

        # calculate running total column in claim_mvmt_detail_df.mvmt_yr by claim_mvmt_detail_df.exposure_reference
        claim_mvmt_detail_df.sort_values(by=['exposure_reference', 'mvmt_yr'], inplace=True)
        claim_mvmt_detail_df['incurred_cum_100'] = claim_mvmt_detail_df[['exposure_reference', 'incurred_mvmt_100']].groupby('exposure_reference').cumsum()

    
        # calculate maximum of running total
        claim_mvmt_detail_df['incurred_cummax_100'] = claim_mvmt_detail_df[['exposure_reference', 'incurred_cum_100']].groupby('exposure_reference').transform('max')

        
        # append to claim_df the determined detrended threshold
        claim_mvmt_detail_df = claim_mvmt_detail_df.merge(thres_df, on='yoa', how='left')
        claim_mvmt_detail_df['large_threshold_sett_fx'] = claim_mvmt_detail_df['large_threshold_sett_fx'].fillna(large_threshold_sett_fx)


        # determine conditions for loss category
        condition_loss_fund = (claim_mvmt_detail_df.beazley_catcode.str[:2] == "LF") | (claim_mvmt_detail_df.beazley_catcode.str[-2:]  == "LF")
        condition_cat       = (claim_mvmt_detail_df.beazley_catcode != "B") & (claim_mvmt_detail_df.beazley_catcode.str[:3]  != "PCS") & (claim_mvmt_detail_df.beazley_catcode != "") 
        condition_block     = (claim_mvmt_detail_df.block_indicator == "Yes")                                                   # per warning at top this is yes/no field
        condition_large     = (claim_mvmt_detail_df.incurred_cummax_100 >= claim_mvmt_detail_df['large_threshold_sett_fx'] )
    
        # assign loss category
        claim_mvmt_detail_df['loss_category']   = np.where(condition_loss_fund, "LF"
                                                    ,np.where(condition_cat, "CAT"
                                                        ,np.where(condition_block, "ATT"
                                                            ,np.where(condition_large, "LARGE","ATT"))))

        # convert to settlement currency - #### JB NEED TO ADD WARNING MESSAGE IS FX NOT ENTERED - TEST BEHAVIOUR ON NO CURRENCY SELECTED IN MDOEL
        currency_rates_bi_df= hx.params.table_currencyratebicurrent
        fx_rate_usd_row     = currency_rates_bi_df[ (currency_rates_bi_df['Currency'] == "USD") ]
        fx_rate_sett_row    = currency_rates_bi_df[ (currency_rates_bi_df['Currency'] == cds.currencies.source_currency) ]
        
        condition_fx        = (fx_rate_usd_row.empty) or (fx_rate_sett_row.empty)   
        fx_rate             = 0 if condition_fx else fx_rate_sett_row.ExchangeRate.iat[0] / fx_rate_usd_row.ExchangeRate.iat[0]

        claim_mvmt_detail_df['incurredmvmt_sett_fx']     =  claim_mvmt_detail_df.incurred_mvmt     * fx_rate  
        claim_mvmt_detail_df['incurredmvmt_100_sett_fx'] =  claim_mvmt_detail_df.incurred_mvmt_100 * fx_rate
    



    ################################################
    ## 6) Claims Details Manipulation
    ################################################


    # a) get fx rate to convert  - 06082024 AX request to follow PROD logic not UAT (UAT contemplated PIMS unclear why)
    ####################################################################################
    # GET spot_rate_sett_to_usd
    spot_fx_df                          = hx.params.table_currencyratebicurrent
    claims_df                           = pd.merge(claim_summary_detail_df,spot_fx_df[['Currency','ExchangeRate']], left_on='settlement_currency', right_on='Currency', how='left')
    claims_df.rename(columns={'ExchangeRate': 'spot_rate_gbp_to_clmfx'}, inplace=True)

    fx_rate_polfx_row                   = spot_fx_df[ (spot_fx_df['Currency'] == cds.currencies.source_currency) ] 
    claims_df['spot_rate_gbp_to_polfx'] = 0 if fx_rate_polfx_row.empty else fx_rate_polfx_row.ExchangeRate.iat[0]
    claims_df['spot_rate_clmfx_to_polfx']=np.where((claims_df.spot_rate_gbp_to_polfx==0) | (claims_df.spot_rate_gbp_to_clmfx==0) | (claims_df.spot_rate_gbp_to_clmfx== None)
                                                           ,  0,  claims_df.spot_rate_gbp_to_polfx / claims_df.spot_rate_gbp_to_clmfx)
    claims_df['translation_fx']         = np.where(claims_df.spot_rate_clmfx_to_polfx ==0, 1, claims_df.spot_rate_clmfx_to_polfx)



    # b) calculate claims amounts on updated fx rate and at 100% ... getting line first as some of the data is at share
    ####################################################################################
    claims_df = pd.merge(claims_df, facility_detail_df[['section_reference','written_or_estimated_signed_line']], left_on='section_reference', right_on='section_reference', how='left')
    claims_df.written_or_estimated_signed_line  = np.where(claims_df.written_or_estimated_signed_line==0,  1,  claims_df.written_or_estimated_signed_line)

    claims_df['bi_paid']                        = claims_df.translation_fx    * claims_df.slip_order_total_paid
    claims_df['bi_incurred']                    = claims_df.translation_fx    * claims_df.slip_order_total_incurred
    claims_df['bi_os']                          = claims_df.bi_incurred       - claims_df.bi_paid
    claims_df['pre_peer_blend_incurred']        = claims_df.translation_fx    * claims_df.beazley_share_pre_peer_blend          / claims_df.written_or_estimated_signed_line
    claims_df['pre_peer_most_likely_incurred']  = claims_df.translation_fx    * claims_df.beazley_share_pre_peer_most_likely    / claims_df.written_or_estimated_signed_line


    # c) add loss category column to claims_df 
    ####################################################################################
    if include_triangles == True:
        loss_category_df            = claim_mvmt_detail_df[['exposure_reference','loss_category']].drop_duplicates()
        claims_df                   = claims_df.merge(right = loss_category_df, how="left")
        claims_df['loss_category']  = claims_df['loss_category'].fillna("ATT") # if a claim is in listing but not triangles default it to attritional

    else:
        # append to claims_df the determined detrended threshold
        claims_df = claims_df.merge(thres_df, on='yoa', how='left')
        claims_df['large_threshold_sett_fx'] = claims_df['large_threshold_sett_fx'].fillna(large_threshold_sett_fx)


        # determine conditions for loss category
        condition_loss_fund = (claims_df['beazley_catcode'].str[:2] == "LF") | (claims_df['beazley_catcode'].str[-2:]  == "LF")
        condition_cat       = (claims_df['beazley_catcode'] != "B") & (claims_df['beazley_catcode'].str[:3]  != "PCS") & (claims_df['beazley_catcode'] != "") 
        condition_block     = (claims_df['block_indicator'] == True)                                        # per warning at top this is true/false field
        condition_large     = (claims_df['bi_incurred'] >= claims_df['large_threshold_sett_fx'] )


        # assign loss category
        claims_df['loss_category']   = np.where(condition_loss_fund, "LF"
                                                    ,np.where(condition_cat, "CAT"
                                                        ,np.where(condition_block, "ATT"
                                                            ,np.where(condition_large, "LARGE", "ATT"))))


    # d) calculate ranks for cat and exc. cat/lf ...https://machinelearningtutorials.org/a-comprehensive-guide-to-pandas-rank-understanding-and-utilizing-data-ranking-in-python/
    #    in the grouping we exclude block claims from appearing in the ranks, in the old model similar but on xcat and test was on beazleycatcode == 'B'
    #    consequently it may show slightly different results on cat (block was included) and x-cat where it was coded as block but not in beazleycatcode - e.g. maybe it had a pcs code on it
    ####################################################################################

    claims_df['temp_group'] = np.where( ((claims_df.loss_category=="ATT") | (claims_df.loss_category=="LARGE")) & (claims_df.block_indicator != True)
                                        , "ATT_LARGE"
                                        , np.where( (claims_df.loss_category=="CAT")  & (claims_df.block_indicator != True)
                                                    ,"CAT", "OTHER"))

    claims_df['temp_rank']  = claims_df.groupby("temp_group")["bi_incurred"].rank(method="first", ascending=False)
    claims_df['class_rank'] = np.where(claims_df.temp_group=="OTHER", const.dum_large_neg,    np.where(claims_df.temp_rank>100, const.dum_large_neg,     claims_df.temp_rank))


    # e) determine if row should be visible on screen
    ####################################################################################
    claims_df['show_cat']   = np.where((claims_df.class_rank==const.dum_large_neg) | (claims_df.temp_group !="CAT"),          False,  True)
    claims_df['show_large'] = np.where((claims_df.class_rank==const.dum_large_neg) | (claims_df.temp_group !="ATT_LARGE"),    False,  True)


    # f) sort data by rank for subsequent displaying on screen.
    ####################################################################################
    claims_df.sort_values(by=['class_rank', 'exposure_reference'], inplace=True)

    ################################################
    ## 7) Summarise data and write to hxd
    ################################################

    # a) summarise triangle movements & write to hxd
    ################################################
    if include_triangles == True:
        output_mvmt_groupby_columns = ['date_extracted'
                                        ,'loss_category'
                                        ,'yoa'
                                        ,'mvmt_yr'
                                    ]  

        claim_mvmt_detail_output_df = claim_mvmt_detail_df[output_mvmt_groupby_columns + ['incurredmvmt_100_sett_fx']].groupby(output_mvmt_groupby_columns).sum().reset_index()
    
        output_columns= ['date_extracted','loss_category','yoa','mvmt_yr','incurredmvmt_100_sett_fx']
        setattr(cds.bi_data,"claims_movements",claim_mvmt_detail_output_df.to_dict("records"))


    # b) write claims details to hxd
    ################################################
    output_columns= ['date_extracted' 
                        , 'section_reference'
                        , 'claim_reference'
                        , 'exposure_reference'
                        , 'yoa' 
                        , 'beazley_catcode'
                        , 'market_catcode' 
                        , 'trifocus_name' 
                        , 'settlement_currency'
                        , 'block_indicator'
                        , 'date_of_loss' 
                        , 'claim_made_date'
                        , 'claim_or_circumstance'
                        , 'beazley_share_total_incurred'
                        , 'slip_order_total_incurred'
                        , 'slip_order_total_paid'
                        , 'beazley_share_pre_peer_blend'
                        , 'beazley_share_pre_peer_most_likely'
                        , 'loss_category' 
                        , 'bi_paid' 
                        , 'bi_os' 
                        , 'bi_incurred' 
                        , 'pre_peer_blend_incurred'
                        , 'pre_peer_most_likely_incurred'
                        , 'show_cat' 
                        , 'show_large'
                        , 'class_rank'
                    ]

    claims_df = claims_df[claims_df.columns.intersection(output_columns)]
    setattr(cds.bi_data,"claims_listing",claims_df.to_dict("records"))

    cds.bi_data.fetch_clm_and_mvmt_detail_task_status = ("Claim listing and triangles Information retrieved" if include_triangles else "Claim listing retrieved")


    ### write effective date of claims data to relevant node
    cds.risk_info.bic_data_asat = claims_df.date_extracted[0]

    ### write triangle status to hxd
    cds.bi_data.triangles_loaded = include_triangles

#############################################################################################################################
### END CLAIMS & MOVEMENTS - Pulling all relevant BI Claims and Movements and loading into relevant nodes                 ###
#############################################################################################################################











#############################################################################################################################
### START PREMIUM TABLE ADDITIONAL UPDATE - This does the fx conversion having given the underwriter an opportunity to enter fx if missing ###
#############################################################################################################################

def update_premium_table (hxd,progress):

    cds = hxd.cds
    #########################################################
    ### 1) import premium table
    #########################################################
    policy_df = pd_df_from_hx_list(cds.bi_data.facility_detail)


    #########################################################
    ### 2) GET spot_rate_usd_to_sett
    #########################################################
    spot_fx_df                          = hx.params.table_currencyratebicurrent

    selected_ccy = cds.currencies.source_currency

    policy_df["selected_ccy"] = selected_ccy

    policy_df                           = pd.merge(policy_df,spot_fx_df[['Currency','ExchangeRate']], left_on='selected_ccy', right_on='Currency', how='left')
    policy_df.rename(columns={'ExchangeRate': 'spot_rate_gbp_to_sett'}, inplace=True)

    fx_rate_usd_row                     = spot_fx_df[ (spot_fx_df['Currency'] == "USD") ] 
    policy_df['spot_rate_gbp_to_usd']   = 0 if fx_rate_usd_row.empty else fx_rate_usd_row.ExchangeRate.iat[0]
    policy_df['spot_rate_usd_to_sett']  = np.where((policy_df.spot_rate_gbp_to_usd==0) | (policy_df.spot_rate_gbp_to_sett==0) | (policy_df.spot_rate_gbp_to_sett== None)
                                                           ,  1,  policy_df.spot_rate_gbp_to_sett / policy_df.spot_rate_gbp_to_usd)

    #########################################################
    ### 3)  GET premium, gross to !00%, convert to settlement currency, assess before and after aqn and rate change 
    #########################################################
    policy_df['net_beazley_premium_sett_fx']  = policy_df.spot_rate_usd_to_sett    * policy_df.written_or_estimated_premium

    policy_df['net_100pct_premium_sett_fx']   = np.where((policy_df.written_or_estimated_signed_line==0) 
                                                            | (policy_df.written_or_estimated_signed_line== None)
                                                            | (policy_df.written_or_estimated_signed_line==const.dum_large_neg)
                                                         , policy_df.net_beazley_premium_sett_fx
                                                         , policy_df.net_beazley_premium_sett_fx / policy_df.written_or_estimated_signed_line)

    # grossing up for acquisition costs - brokerage and commission (agent fees)                                                          
    policy_df['gross_100pct_premium_sett_fx'] = np.where((policy_df.external_acquisition_cost_multiplier==0)
                                                            | (policy_df.external_acquisition_cost_multiplier== None) 
                                                            | (policy_df.external_acquisition_cost_multiplier==const.dum_large_neg)
                                                         , policy_df.net_100pct_premium_sett_fx
                                                         , policy_df.net_100pct_premium_sett_fx / (1-policy_df.external_acquisition_cost_multiplier))

    # adjusted expiring - implied from renewing after adjusting for intervening rate change                                                          
    policy_df['net_100pct_premium_adjexp_sett_fx']   = np.where((policy_df.rate_change_divisor==0) 
                                                                    | (policy_df.rate_change_divisor== None) 
                                                                    | (policy_df.rate_change_divisor==const.dum_large_neg)
                                                                , 0
                                                                , policy_df.net_100pct_premium_sett_fx / policy_df.rate_change_divisor)


    #########################################################
    ### 4) export premium table & write current year epi to node
    #########################################################
    for index, i in enumerate(cds.bi_data.facility_detail):
        i.spot_rate_usd_to_sett                 = policy_df['spot_rate_usd_to_sett'].iat[index]
        i.net_beazley_premium_sett_fx           = policy_df['net_beazley_premium_sett_fx'].iat[index]
        i.net_100pct_premium_sett_fx            = policy_df['net_100pct_premium_sett_fx'].iat[index]
        i.gross_100pct_premium_sett_fx          = policy_df['gross_100pct_premium_sett_fx'].iat[index]
        i.net_100pct_premium_adjexp_sett_fx     = policy_df['net_100pct_premium_adjexp_sett_fx'].iat[index]


    ### write epi out to relevant node
    current_inception_date      = hxd.hx_core.inception_date
    filter_condition            = (policy_df.inception_date == current_inception_date) & (policy_df.include == True) 
    current_year_premium        = policy_df[filter_condition]['gross_100pct_premium_sett_fx'].sum()
    
    # JK - I removed the quoted_premium_100pct data assigment ad I think this should be input by the UW 
    # if current_year_premium > 0:   cds.layers[0].quoted_premium_100pct  =  current_year_premium










#############################################################################################################################
### BEGIN QUERY BI Database -
#############################################################################################################################
# similar query for EDM arguably could be combined but would require lots of parameters passed...

def query_bi_database(query, columns):
    # Set up connection details
    print("starting " + str(datetime.datetime.now()))
    print(str(query))
    
    if "dev" in hx.secrets.environment_name.lower() or "tst" in hx.secrets.environment_name.lower(): 
        host = hx.secrets.beazleyintelligencedatasets_host_uat
        user = hx.secrets.beazleyintelligencedataSets_login_uat
        password = hx.secrets.beazleyintelligencedataSets_password_uat
    else:
        host = hx.secrets.beazleyintelligencedatasets_host_prd
        user = hx.secrets.beazleyintelligencedataSets_login_prd
        password = hx.secrets.beazleyintelligencedataSets_password_prd
    
    database_name = "BeazleyIntelligenceDataSets"
    
    # host = hx.secrets.beazleyintelligencedatasets_host_uat                                   ### UAT: hx.secrets.beazleyintelligencedatasets_host_uat;        Prod:   hx.secrets.beazleyintelligencedatasets_host_prd
    # database_name = "BeazleyIntelligenceDataSets"
    # user = hx.secrets.beazleyintelligencedataSets_login_uat                                  ### UAT: hx.secrets.beazleyintelligencedataSets_login_uat;       Prod:   hx.secrets.beazleyintelligencedataSets_login_prd
    # password = hx.secrets.beazleyintelligencedataSets_password_uat                           ### UAT: hx.secrets.beazleyintelligencedataSets_password_uat;    Prod:   hx.secrets.beazleyintelligencedataSets_password_prd

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER={' + host + '};DATABASE={' + database_name + '};UID={' + user + '};PWD={' + password + '}', timeout=30)

    # Setting up a cursor is the idiomatic way of maintaining the connection
    cursor = cnxn.cursor()

    # Fetch data
    cursor.execute(query)
    rows = cursor.fetchall()

    print("ending " + str(datetime.datetime.now()))
    return pd.DataFrame.from_records(rows, columns=columns)
    # return rows

#############################################################################################################################
### END QUERY BI Database -
#############################################################################################################################
