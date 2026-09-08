##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################



##############################################################################################################################
##############################################################################################################################

import hx, pyodbc
import pandas as pd
import numpy as np
from datetime import datetime
import algorithms.rate_constants as const
from dateutil.relativedelta import relativedelta
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd



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

    return pd.DataFrame.from_records(rows, columns=columns)
    # return rows



#######################################################################################################
### BEGIN SQL BI Data pull - Pulling all relevant BI data and loading into relevant nodes           ###
#######################################################################################################

def sql_bi_data(hxd,progress):

    cds = hxd.cds
      
    if  (cds.layers[0].section_reference is None):
        cds.bi.last_run_status = "Please enter a policy section reference"
        return

    section_ref = cds.layers[0].section_reference
    section_ref = section_ref.upper()

    # section_ref = 'JQD65C25APSE' #USE FOR TESTING
    
    # Query
    query1 = f"""
                    SELECT      
                        GETDATE() as date_extracted
                        ,PolicyReference
                        ,SectionReference
                        ,InceptionDate
                        ,ExpiryDate
                        ,UnderwriterName
                        ,Industry
                        ,IndustryCode
                        ,Area
                        ,AreaCode
                        ,OriginalCurrency
                        ,InsuredParty
                        ,OriginalInsured
                        ,RiskClass
                        ,RiskClassCode
                        ,'unknown' as obligor
                        ,[PlacingBrokerName]
                        ,[SectionIsRenewal]  
                        ,ExternalAcquisitionCostMultiplier
                        ,[TotalWrittenIfNotSignedMultiplier]  
  
                    FROM [BeazleyIntelligenceDataSets].[Report].[SectionCombinedView]
                    WHERE SectionReference IN ('{section_ref}')
                    Order by [YOA] Desc
            """

    columns1 =  ['date_extracted'
                    ,'policy_reference'
                    ,'section_reference'
                    ,'inception_date'
                    ,'expiry_date'
                    ,'underwriter_name' 
                    ,'industry'
                    ,'industry_code'
                    ,'area'
                    ,'area_code'
                    ,'original_currency'
                    ,'insured_party'
                    ,'original_insured'
                    ,'risk_class'
                    ,'risk_class_code'
                    ,'obligor'
                    ,'placing_brokername'
                    ,'section_is_renewal'
                    ,'external_acquisition_cost_multiplier'
                    ,'written_or_estimated_signed_line'  
                ]

    # pull facility detail for all facilities from sql based on query 1
    policy_detail_df  = query_bi_database(query1, columns1) 


    # assigning status where cant identify suitable facility for core fields
    if policy_detail_df.empty:
        cds.bi.last_run_status  = f"Policy Section: {section_ref} not found in Beazley Intelligence." 
    else:
        cds.bi.last_run_date            = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cds.bi.last_run_status          = f"Policy Section: {section_ref} retrieved from Beazley Intelligence at {cds.bi.last_run_date}."
        cds.bi.last_run_value           = section_ref

        # load basic retrieved fields to hxd
        hxd.hx_core.inception_date              = policy_detail_df['inception_date'].iat[0] 
        hxd.hx_core.expiry_date                 = policy_detail_df['expiry_date'].iat[0] 
        cds.standard_fields.underwriter         = policy_detail_df['underwriter_name'].iat[0]
        cds.currencies.source_currency          = policy_detail_df['original_currency'].iat[0]
        cds.standard_fields.insured_name        = policy_detail_df['insured_party'].iat[0]
        cds.standard_fields.broker              = policy_detail_df['placing_brokername'].iat[0]
        cds.standard_fields.is_renewal          = policy_detail_df['section_is_renewal'].iat[0]
        cds.layers[0].brokerage                 = policy_detail_df['external_acquisition_cost_multiplier'].iat[0]
        cds.layers[0].written_line              = policy_detail_df['written_or_estimated_signed_line'].iat[0]

        # obligor not available in current datasets - rumoured to be in ods - old path in RedCube was here ("{[Policy - Section].[Obligor].children}") via mdx on RedCubeServer   
        # cds.risk_info.crcf_obligor             = policy_detail_df['obligor'].iat[0]

        # load industry to hxd where not NULL
        industry = policy_detail_df['industry'].iat[0]
        if industry == "NULL":          cds.bi.last_run_status          += 'No industry info available.'
        elif industry is None:          cds.bi.last_run_status          += 'No industry info available.'
        else:                           cds.risk_info.crcf_industry      = industry

        # load industry to hxd where found after converting to lowercase - as cases dont match naturally
        ihs_country_df                  = hx.params.tbl_ihs_country
        ihs_country_df['ihs_lowercase'] = ihs_country_df['IHS Country'].str.lower()
        country_bi                      = policy_detail_df['area'].iat[0]
        country_bi_lower                = country_bi.lower()
        country_selected_proper_df      = ihs_country_df[ihs_country_df['ihs_lowercase'] == country_bi_lower]


        if len(country_selected_proper_df)!=0:
            cds.risk_info.crcf_country          = country_selected_proper_df['IHS Country'].iat[0]
        else:
            remap_country_df                    = hx.params.tbl_bi_country_remap
            remap_country_df['bi_lowercase']    = remap_country_df['bi_country'].str.lower()
            remap_country_selected_df           = remap_country_df[remap_country_df['bi_lowercase'] == country_bi_lower]
            if len(remap_country_selected_df)!=0:
                cds.risk_info.crcf_country      = remap_country_selected_df['ihs_country'].iat[0]
            else:
                cds.bi.last_run_status         += f'Country {country_bi} not a valid entry.'
