import hx, pyodbc
import pandas as pd
from datetime                   import datetime
from algorithms.rate_utilities  import pd_df_from_hx_list, write_pd_to_hxd, get_fx_rate, ratio
from algorithms                 import parameter_tables_schema as lib_params



#############################################################################################################################
### POLICY TABLE QUERY & COLUMNS
#############################################################################################################################
query1 = """
                SELECT 
                    GETDATE() as date_extracted
                    ,[PolicyReference]
                    ,[SectionReference]
                    ,[YOA]
                    ,[CoverageName]
                    ,[TriFocusName]
                    ,[Division]
                    ,[RateChangeDivisor]
                    ,[SettlementCurrency]
                    ,ISNULL([WrittenOrEstimatedPremium],0)  AS 'gnwp_bzly_usd'
                    ,[TotalIncurred]                        AS 'incurred_bzly_usd'
                    ,(CASE WHEN [RateChangeDivisor] IS NULL THEN 1 
                        WHEN [RateChangeDivisor] < 10    THEN [RateChangeDivisor] 
                        ELSE 10 
                        END) as 'RateChangeReformat'
                    ,LEFT([PolicyReference],6) AS 'Index'
                    , [TotalWrittenIfNotSignedMultiplier]
                    ,([WrittenOrEstimatedPremium]/[TotalWrittenIfNotSignedMultiplier]) AS 'gnwp_100_usd'
                    ,([TotalIncurred]            /[TotalWrittenIfNotSignedMultiplier]) AS 'incurred_100_usd'
                    , [ClassOfBusinessCode]
                    ,IIF([ClassOfBusinessCode] NOT IN ('SN', 'SB', 'SQ', 'SJ', 'SK'), 1, 0) AS 'Event Cancellation'
                    ,IIF([ClassOfBusinessCode]     IN ('SN'), 1, 0)                         AS 'Non App'

                    FROM [BeazleyIntelligenceDataSets].[Report].[SectionCombinedView]
                    WHERE [PolicyReference] LIKE 'DUMMY_REFERENCE%'
                    ORDER BY [InceptionDate]
         """

columns1 =  ['date_extracted'
                ,'policy_ref'
                ,'section_ref'
                ,'yoa'
                ,'coverage_name'
                ,'trifocus_name'
                ,'division'
                ,'rate_chg_init'
                ,'settlement_fx'
                ,'gnwp_bzly_usd'
                ,'incurred_bzly_usd'
                ,'rate_chg'
                ,'index_bzly'
                ,'share_bzly'
                ,'gnwp_100_usd'
                ,'incurred_100_usd'
                ,'class_code'
                ,'bool_ec'
                ,'bool_na'
            ]



#############################################################################################################################
### CLAIMS TABLE QUERY & COLUMNS
#############################################################################################################################

query2 = """
            WITH claims AS (
                SELECT
                     [PolicyReference]
                    ,[SectionReference]
                    ,[ClaimReference]
                    ,[TriFocusName]
                    ,[Division]
                    ,[PolicyYOA]
                    ,[SettlementCurrency]
                    ,[BeazleyCatCode]
                    ,[BeazleyCat]
                    ,[MarketCatCode]
                    ,[MarketCat]
                    ,[HasBeazleyCatCode]
                    ,[CauseOfLoss]
                    ,LEFT([SectionReference], 6) AS [Index]
                    ,[BeazleyShareTotalIncurred]
                    ,[BeazleyShareTotalOutstanding]
                    ,[SignedLineMultiplier]
                    ,[BeazleyShareTotalIncurred] / [SignedLineMultiplier] AS [Incurred_100]
                    ,CASE
                         WHEN [SectionReference] IS NULL OR [SectionReference] = '' THEN ''
                         WHEN CHARINDEX('-', [SectionReference]) > 0 THEN RIGHT(LEFT([SectionReference], CHARINDEX('-', [SectionReference]) - 1), 2)
                         ELSE RIGHT([SectionReference], 2)
                     END AS [ClassOfBusinessCode]
                FROM [BeazleyIntelligenceDataSets].[Report].[ClaimExposureSectionCombinedView]
                WHERE [PolicyReference] LIKE 'DUMMY_REFERENCE%'
            )
            SELECT
                *
                , CASE WHEN [BeazleyCatCode] = 'CORO' THEN 1 ELSE 0 END AS [COVID Indicator]
                , IIF([ClassOfBusinessCode] NOT IN ('SN', 'SB', 'SQ', 'SJ', 'SK'), 1, 0) AS 'Event Cancellation'
                , IIF([ClassOfBusinessCode]     IN ('SN'),                         1, 0) AS 'Non App'
            FROM claims;

         """

columns2 =  [    'policy_ref'
                ,'section_ref'
                ,'claim_ref'
                ,'trifocus_name'
                ,'division'
                ,'yoa'
                ,'settlement_fx'

                ,'cat_code_bzly'
                ,'cat_desc_bzly'
                ,'cat_code_mkt'
                ,'cat_desc_mkt'
                ,'cat_bzly_bool'

                ,'cause_of_loss'
                ,'index_bzly'

                ,'incurred_bzly'
                ,'os_bzly'
                ,'share_bzly'
                ,'incurred_100'

                ,'class_code'
                ,'bool_covid'
                ,'bool_ec'
                ,'bool_na'            ]





#############################################################################################################################
### BEGIN QUERY BI Database - function to actually extract from BI
#############################################################################################################################

def query_bi_database(query, columns):
    # Set up connection details
    is_dev = (hx.secrets.environment_name == 'beazley-dev' or hx.secrets.environment_name == 'beazley-tst')
 
    database_name   = "BeazleyIntelligenceDataSets"
    host            = hx.secrets.beazleyintelligencedatasets_host_uat       if is_dev   else hx.secrets.beazleyintelligencedatasets_host_prd       ### UAT: hx.secrets.beazleyintelligencedatasets_host_uat;        Prod:   hx.secrets.beazleyintelligencedatasets_host_prd
    user            = hx.secrets.beazleyintelligencedataSets_login_uat      if is_dev   else hx.secrets.beazleyintelligencedataSets_login_prd      ### UAT: hx.secrets.beazleyintelligencedataSets_login_uat;       Prod:   hx.secrets.beazleyintelligencedataSets_login_prd
    password        = hx.secrets.beazleyintelligencedataSets_password_uat   if is_dev   else hx.secrets.beazleyintelligencedataSets_password_prd   ### UAT: hx.secrets.beazleyintelligencedataSets_password_uat;    Prod:   hx.secrets.beazleyintelligencedataSets_password_prd

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER={' + host + '};DATABASE={' + database_name + '};UID={' + user + '};PWD={' + password + '}', timeout=30)

    # Setting up a cursor is the idiomatic way of maintaining the connection
    cursor = cnxn.cursor()

    # Fetch data
    cursor.execute(query)
    rows = cursor.fetchall()

    # close connection
    cursor.close()
    cnxn.close()

    return pd.DataFrame.from_records(rows, columns=columns)
    # return rows



#######################################################################################################
### BEGIN SQL BI Data pull - Pulling all relevant BI data and loading into relevant nodes           ###
#######################################################################################################

def tsk_sql_bi_data(hxd,progress):

    # paths
    cds     = hxd.cds
    er      = cds.experience_rating
    fx_df   = lib_params.fx_rates.df()    

    if  (cds.layers[0].coverages.ec_total.section_reference is None):
        cds.bi.last_run_status = "Please enter a policy section reference"
        return

    section_ref = cds.layers[0].coverages.ec_total.section_reference
    ref         = section_ref.upper()[:6]
   
    # pull policy detail based on query 1
    query      = query1.replace("DUMMY_REFERENCE", ref)
    policy_df  = query_bi_database(query, columns1) 

    # pull claims detail based on query 2
    query      = query2.replace("DUMMY_REFERENCE", ref)
    claim_df   = query_bi_database(query, columns2) 

    # add settlement fx to policy detail
    policy_df['fx_rate_usd_sett']= ratio(get_fx_rate(fx_df, policy_df['settlement_fx'] ),   get_fx_rate(fx_df, "USD" ),   1) 
    policy_df['gnwp_bzly']       = policy_df['gnwp_bzly_usd']        *   policy_df['fx_rate_usd_sett'] 
    policy_df['incurred_bzly']   = policy_df['incurred_bzly_usd']    *   policy_df['fx_rate_usd_sett'] 
    policy_df['gnwp_100']        = policy_df['gnwp_100_usd']         *   policy_df['fx_rate_usd_sett'] 
    policy_df['incurred_100']    = policy_df['incurred_100_usd']     *   policy_df['fx_rate_usd_sett'] 
    
    # assigning status where cant identify suitable facility for core fields
    if policy_df.empty:
        cds.bi.last_run_status  = f"Policy Section: {section_ref} not found in Beazley Intelligence." 
    else:
        cds.bi.last_run_date            = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cds.bi.last_run_status          = f"Policy Section: {section_ref} retrieved from Beazley Intelligence at {cds.bi.last_run_date}."
        cds.bi.last_run_value           = section_ref
 
        er.evaluation_date_ovd          = policy_df['date_extracted'].iat[0]
        
        # policy table
        cols        = policy_df.columns[policy_df.columns != "date_extracted"].tolist()
        policy_df   = policy_df.astype(object).where(pd.notna(policy_df),None)
        setattr(er, "policy_table", policy_df[cols].to_dict("records"))

        # claim table
        cols        = claim_df.columns.tolist()
        claim_df    = claim_df.astype(object).where(pd.notna(claim_df),None)
        setattr(er, "claim_table", claim_df[cols].to_dict("records"))
