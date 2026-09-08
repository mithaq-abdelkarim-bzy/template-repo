#########################################################################################################
########################################### Outstanding Items ###########################################
#########################################################################################################
### 1) 
### 2) 
### 3) 
### 4) 
### 5) 
#########################################################################################################





import hx
import requests
import json
import pandas as pd
from datetime import datetime

@hx.task
def api_ihs_data(hxd, progress):

    cds = hxd.cds

    # Available endpoints - NOTE: using "violentrisk" for Terrorism; "strategicrisk" for political and CRCF
    endpoints = [
        "https://api.connect.ihsmarkit.com/risk/v3/country-risk/scores/comprehensiverisk", 
        "https://api.connect.ihsmarkit.com/risk/v3/country-risk/scores/politicalrisk", 
        "https://api.connect.ihsmarkit.com/risk/v3/country-risk/scores/strategicrisk", 
        "https://api.connect.ihsmarkit.com/risk/v3/country-risk/scores/securityrisk", 
        "https://api.connect.ihsmarkit.com/risk/v3/country-risk/scores/violentrisk"
    ]
    
    country_codes = cds.ihs.calc_run_value

    # checking if no digit country code(s) have been returned 
    if country_codes == '':
        # do nothing
        cds.ihs.last_run_status = "No IHS data returned - no countries entered"
        return


    # API Request Setup
    user = hx.secrets.ihs_pat_username
    password = hx.secrets.ihs_pat_password
    base_url = "https://api.connect.ihsmarkit.com/risk/v3/country-risk/scores/strategicrisk"
    params = {"countries": country_codes}

    # Send GET request with basic authentication, expecting JSON response
    response = requests.get(base_url, params=params, auth=(user, password))
    #response = requests.get(base_url, auth=(user, password))

    # Check response status
    if response.status_code != 200:
        hx.errors.fatal(f"API request failed with status code {response.status_code}: {response.text}")
        return
    
    # Proceed with data processing
    json_string = response.text
    
    # Decode JSON string and assign to hxd
    data = json.loads(json_string)


    # convert json to dataframe extracting first level
    # df has columns: 'Country' (2 char name) & 'Risks' (multilevel list)
    df  = pd.json_normalize(data, max_level =0)


    # extract next level of 'risks' list and use melt to flick from columns to rows without resetting index to facilitate the join in the next row
    # df1 has columns:  'RiskName' (basic description);     'RiskValue' (multilevel list)
    df1 = pd.json_normalize(df['Risks'], max_level=0).melt(var_name='RiskName', value_name='RiskValue', ignore_index = False)


    # join 'Country' from df back to the transformed data in df1 using the existing index, which then gets reset and the original index dropped
    # df2 has columns:  'Country' (2 char name);     'RiskName' (basic description);     'RiskValue' (multilevel list)
    df2 = df.join(    df1).reset_index().drop(['Risks','index'],axis=1)


    # extract next level of list from 'RiskValue' and append 'Country' &  'RiskName' from df2 dropping extra columns and renaming others for clarity
    # df3 has columns:  'Country' (2 char name);     'RiskName' (basic description);    'RiskName2' (basic description);  'Outlook' (1 word indicator);     'OutlookDescription' (more detail on outlook)
    #                   'latest_update_on' (date of last update);     'latest_value' (latest value);    'History' (single level list)   
    df3 = df2.join(   pd.json_normalize(df2['RiskValue'], max_level=0)).drop(['RiskValue'],axis=1).rename(columns={'UpdatedOn': 'latest_update_on','Value':'latest_value','Name':'RiskName2', 'Description':'OutlookDescription'})
    

    # fillna on text columns
    cols_to_fillna = [item for item in df3.columns.values.tolist() if item not in ['latest_update_on','latest_value'] ]
    df3[cols_to_fillna] = df3[cols_to_fillna].fillna(value='')


    # expand out history so each historic value goes on its own row retaining all other columns and resetting index
    df4 = df3.explode('History').dropna().reset_index()
    

    # expand out history so we have each historic value and associated date adopting agreed column names
    df_column_names  = {  'Country'              : 'country'
                        , 'RiskName'             : 'risk_name'
                        , 'RiskName2'            : 'risk_name_other'
                        , 'Outlook'              : 'outlook'
                        , 'OutlookDescription'   : 'outlook_description'
                        , 'latest_update_on'     : 'last_updated_date'
                        , 'latest_value'         : 'last_updated_value'
                        , 'UpdatedOn'            : 'historic_updated_date'
                        , 'Value'                : 'historic_updated_value'
                        }
    ihs_df = df4.join(   pd.json_normalize(df4['History'], max_level=0)).drop(['History','index'],axis=1).rename(columns = df_column_names).dropna()


    # determine if data has been returned
    if ihs_df.empty:
        # do nothing
        cds.ihs.last_run_status     = "No IHS data returned for entered references"
        return

    # split dataframe into 2 parts - the outlook (small # rows) and the detail (large # rows)
    outlook_df  = ihs_df[['country', 'risk_name', 'last_updated_date', 'last_updated_value',  'outlook','outlook_description' ]].drop_duplicates()
    detail_df   = ihs_df[['country', 'risk_name', 'historic_updated_date', 'historic_updated_value']].drop_duplicates()

    # assign to hxd including statuses
    setattr(cds.ihs,    "ihs_outlook",  outlook_df.to_dict("records") )
    setattr(cds.ihs,    "ihs_detail",   detail_df.to_dict("records")  )
    cds.ihs.last_run_date           = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cds.ihs.last_run_status         = f"IHS data load successful at {cds.ihs.last_run_date}"
    cds.ihs.last_run_value          = country_codes

    return