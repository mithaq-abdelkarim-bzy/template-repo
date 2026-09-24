import hx, pyodbc
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
import algorithms.global_parameters as gparams
import algorithms.rate_constants as const

def capiq_query(search_type, query_input, query_input_2=None):
        query = f"""
            select [companyId]
                , [companyName]
                , [tickerSymbol]
                , [HQState]
                , [IncorporationState]
                , [city]
                , [exchangeName]
                , cast([TwoYearMarketCapHigh] as float)*1e6 TwoYearMarketCapHigh
                , [AsOfDate]
                , [SIC_Code]
                , [IPODate]
                , cast([TotalAssets] as float)*1e6 TotalAssets
                , [min_trading_volume]
                , [volatility_trading_volume_downturn]
                , [percentage_execs_under_fifty]
                , [year_founded]
                , cast([EBIT] as float)*1e6 EBIT
                , cast([CurrentAssets] as float)*1e6 CurrentAssets
                , cast([TotalLiabilities] as float)*1e6 TotalLiabilities
                , cast([CurrentLiabilities] as float)*1e6 CurrentLiabilities
                , cast([RetainedEarnings] as float)*1e6 RetainedEarnings
                , cast([Revenues] as float)*1e6 NetSales
                , cast(coalesce([mCapUSD], [TwoYearMarketCapHigh]) as float)*1e6 mCapUSD 
                , cast(getdate() as date)
                , [BusinessDescription]
            from 
            [dbo].[vwCAPIQ_PubDO_leadership_features]

            """

        if search_type == "name":
            where_clause = f""" 
                where companyName like '%{query_input}%'
                order by TwoYearMarketCapHigh desc
                """
        elif search_type == "id":
            where_clause = f""" 
                where companyid ='{query_input}'
                order by TwoYearMarketCapHigh desc
                """
        elif search_type == "capiq":
            where_clause = f""" 
                where tickerSymbol = '{query_input}'
                order by TwoYearMarketCapHigh desc
                """
        elif search_type == "name_and_capiq":
            where_clause = f""" 
                where tickerSymbol = '{query_input_2}' and 
                companyName like '%{query_input}%'
                order by TwoYearMarketCapHigh desc
                """
        query += where_clause
        return query

def capiq_columns():
    columns = [
                'id',
                'company_name',
                'ticker',
                'hq_state',
                'incorporated_state',
                'hq_city',
                'exchange',
                'market_cap',
                'date_updated',
                'sic_code',
                'ipo_date',
                'total_assets',
                'minimum_trading_volume',
                'volatility_of_trading',
                'execs_under_age_50',
                'year_founded',
                'ebit',
                'current_assets',
                'total_liabilities',
                'current_liabilities',
                'retained_earnings',
                'net_sales',
                'market_value_of_equity',
                'source',
                'company_description'
            ]
    return columns

        

def capiq_fetch(hxd,progress): #JD?: What does this "progress" input do and is it needed (taken from All- BBT rater)
    hxd.cds.capiq_search_complete = False
    
    name = hxd.cds.company_search
    capiq = hxd.cds.capiq_search
    
    if name is None and capiq is None:
        hxd.cds.capiq_results = "Please enter a company name or CapIQ ticker"
    else:
        if name is not None and capiq is None:
            query = capiq_query("name", name)
        elif name is None and capiq is not None:
            query = capiq_query("capiq", capiq)
        elif name is not None and capiq is not None:
            query = capiq_query("name_and_capiq", name, capiq)

        columns = capiq_columns()
        #capiq_data = query_bi_database(query, columns)
        capiq_data = query_capiq_database(query, columns)
        # Converting NaNs to None
        capiq_data = capiq_data.replace({np.nan: None})

        if capiq_data.shape[0] < 1:
            # do nothing
            hxd.cds.capiq_results = "No results returned"
        else:
            setattr(hxd.cds,"capiq",capiq_data.to_dict("records"))
            hxd.cds.capiq_results = "Select from " + str(capiq_data.shape[0]) + " returned results"
            hxd.cds.capiq_search_complete = True

    pass

def query_bi_database(query, columns):
    # Set up connection details
    #print("starting " + str(datetime.datetime.now()))
    print(str(query))
    host = hx.secrets.beazleyintelligencedatasets_host_uat                                 ### UAT: hx.secrets.beazleyintelligencedatasets_host_uat;        Prod:   hx.secrets.beazleyintelligencedatasets_host_prd
    database_name = "BeazleyIntelligenceDataSets"
    user = hx.secrets.beazleyintelligencedataSets_login_uat                                ### UAT: hx.secrets.beazleyintelligencedataSets_login_uat;       Prod:   hx.secrets.beazleyintelligencedataSets_login_prd
    password = hx.secrets.beazleyintelligencedataSets_password_uat                           ### UAT: hx.secrets.beazleyintelligencedataSets_password_uat;    Prod:   hx.secrets.beazleyintelligencedataSets_password_prd

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER={' + host + '};DATABASE={' + database_name + '};UID={' + user + '};PWD={' + password + '}', timeout=30)

    # Setting up a cursor is the idiomatic way of maintaining the connection
    cursor = cnxn.cursor()

    # Fetch data
    cursor.execute(query)
    rows = cursor.fetchall()

    #print("ending " + str(datetime.datetime.now()))
    return pd.DataFrame.from_records(rows, columns=columns)
    # return rows

def query_capiq_database(query, columns):
    # Set up connection details
    #print("starting " + str(datetime.datetime.now()))
    print(str(query))

    if "dev" in hx.secrets.environment_name.lower():
        host = hx.secrets.capiq_host_dev
        user = hx.secrets.capiq_login_dev
        pwd = hx.secrets.capiq_password_dev
    elif "tst" in hx.secrets.environment_name.lower():
        host = hx.secrets.capiq_host_tst
        user = hx.secrets.capiq_login_tst
        pwd = hx.secrets.capiq_password_tst
    else:
        host = hx.secrets.capiq_host_prd
        user = hx.secrets.capiq_login_prd
        pwd = hx.secrets.capiq_password_prd

    database_name = 'Capiq'

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER={' + host + '};DATABASE={' + database_name + '};UID={' + user + '};PWD={' + pwd + '}', timeout=60)

    # Setting up a cursor is the idiomatic way of maintaining the connection
    cursor = cnxn.cursor()

    # Fetch data
    cursor.execute(query)
    rows = cursor.fetchall()

    #print("ending " + str(datetime.datetime.now()))
    return pd.DataFrame.from_records(rows, columns=columns)
    # return rows

# The user selects an entry from the CapIQ search using a boolean column
# This function populates the rater with the selection policy
def populate_capiq_data(hxd,progress):
    capiq = hxd.cds.capiq

    # Controls the landing page
    hxd.model_state.pressed_populate_capiq_task = True

    # Search for true values in boolean column
    capiq_data = utils.pd_df_from_hx_list(capiq)
    select_col = capiq_data.loc[:,"selection"]
    selection = [i for i, x in enumerate(select_col) if x]

    # End task and report error if:
    #   1) No rows was selected or;
    #   2) More than one row was selected
    if not selection:
        hxd.cds.capiq_populate = "Populate Rater failed: No option selected"
    else:
        if len(selection) > 1:
            hxd.cds.capiq_populate = "Populate Rater failed: Please select only one option"
        else:
            selection = selection[0]
            capiq_data = capiq_data.iloc[selection]

            populate_fields_from_capiq_df(hxd, progress, capiq_data)

            hxd.cds.capiq_populate = "Populate Rater succeeded"
    return

def populate_fields_from_capiq_df(hxd,progress,capiq_data):
    # Converting NaNs to None
    capiq_data = capiq_data.replace({np.nan: None})

    # Converting state codes to state names
    state_table = hx.params.dd_state
    state_code = state_table["Code"].values
    for field in ["hq_state", "incorporated_state"]:
        capiq_state = getattr(capiq_data, field) 
        if capiq_state in state_code:
            state = utils.look_up(capiq_state, "Code", "State", state_table, capiq_state)
            setattr(capiq_data, field, state)

    ## Populating rater fields with CapIQ data ##
    hxd.cds.company_name = capiq_data.company_name 
    hxd.cds.ticker = capiq_data.ticker
    
    # Adding new description to current
    # original_desc = hxd.cds.company_description if hxd.cds.company_description else ''
    # new_desc = capiq_data.company_description if capiq_data.company_description else ''
    # if len(original_desc) > 0:
    #     if (original_desc == capiq_data.company_description):
    #         hxd.cds.company_description = original_desc
    #     else:
    #         hxd.cds.company_description = f"""
    #         /******** CapIQ Company Description - {capiq_data.source} ********/
    #         {new_desc}        
    #         /***************************************************************/
    #         {original_desc} 
    #         """
    # else:
    #     hxd.cds.company_description = capiq_data.company_description

    # 16/03 - No longer adding new description to current. Just replacing. 
    hxd.cds.company_description = capiq_data.company_description

    # Checking that values are in the field dropdown
    if capiq_data.hq_state in state_table["State"].values:
        hxd.cds.company_state = capiq_data.hq_state
        hxd.cds.hq_state = capiq_data.hq_state

    if capiq_data.incorporated_state in hx.params.dd_incorporated_state["State"].values:    
        hxd.cds.incorporated_state = capiq_data.incorporated_state

    hxd.cds.hq_city = capiq_data.hq_city
    
    hxd.cds.exposure.aggregate.ipo_date = capiq_data.ipo_date
    hxd.cds.exposure.aggregate.market_cap = capiq_data.market_cap
    hxd.cds.exposure.aggregate.minimum_trading_volume = capiq_data.minimum_trading_volume
    hxd.cds.exposure.aggregate.volatility_of_trading = capiq_data.volatility_of_trading
    hxd.cds.exposure.aggregate.execs_under_age_50 = capiq_data.execs_under_age_50
    hxd.cds.exposure.aggregate.year_founded = capiq_data.year_founded
    hxd.cds.exposure.aggregate.total_assets = capiq_data.total_assets
    hxd.cds.exposure.aggregate.ebit = capiq_data.ebit
    hxd.cds.exposure.aggregate.current_assets = capiq_data.current_assets
    hxd.cds.exposure.aggregate.total_liabilities = capiq_data.total_liabilities
    hxd.cds.exposure.aggregate.current_liabilities = capiq_data.current_liabilities
    hxd.cds.exposure.aggregate.retained_earnings = capiq_data.retained_earnings
    hxd.cds.exposure.aggregate.net_sales = capiq_data.net_sales
    hxd.cds.exposure.aggregate.market_value_of_equity = capiq_data.market_value_of_equity
    hxd.cds.exposure.aggregate.source = hxd.cds.capiq_refresh_date = capiq_data.source

    df_sic = hx.params.ref_sic
    sic = int(capiq_data.sic_code) if capiq_data.sic_code else None

    if sic in df_sic['SICCode'].values:
        df_row = df_sic[df_sic['SICCode'] == sic].iloc[0]
        hxd.cds.key_industry.code_name = df_row['SICCombined']
        #hxd.cds.key_industry.sector_name = df_row['SectorName']    
    
    return

def populate_capiq_data_from_wb(hxd,progress):
    # Controls the landing page
    hxd.model_state.pressed_populate_capiq_task = True

    query = query = capiq_query("id", hxd.cds.capiq_wb_id)
    columns = capiq_columns()

    capiq_data = query_capiq_database(query, columns)

    # Do nothing if id cannot be found
    if capiq_data.shape[0] > 0:
        capiq_data = capiq_data.iloc[0]
        populate_fields_from_capiq_df(hxd, progress, capiq_data)

    return

def skip_capiq(hxd,progress):
    """
    Allows the user to skip the CapIQ pull by just updating the show/hide fields
    """
    hxd.model_state.pressed_populate_capiq_task = True
