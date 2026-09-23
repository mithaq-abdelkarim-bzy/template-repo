import hx, pyodbc
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
import algorithms.rate_constants as const
from algorithms import parameter_tables_schema as params


def capiq_fetch(hxd,progress): 
    hxd.cds.capiq_search_complete = False
    
    name = hxd.cds.company_search
    ticker = hxd.cds.key_industry.ticker


    if name is None and ticker is None:
        hxd.cds.capiq_results = "Please enter a ticker or company name"
    elif ticker:
         query = f"""
            select [companyId]
                , [companyName]
                , [tickerSymbol]
                , [exchangeName]
                , cast([TwoYearMarketCapHighOrigCCY] as float)*1e6 TwoYearMarketCapHighOrigCCY
                , [AsOfDate]
                , [SIC_Code]
                , [IPODate]
                , cast([TotalAssets] as float)*1e6 TotalAssets
                , [min_trading_volume_adr]
                , [volatility_trading_volume_downturn_adr]
                , [percentage_execs_under_fifty]
                , cast([EBIT] as float)*1e6 EBIT
                , cast([CurrentAssets] as float)*1e6 CurrentAssets
                , cast([TotalLiabilities] as float)*1e6 TotalLiabilities
                , cast([CurrentLiabilities] as float)*1e6 CurrentLiabilities
                , cast([RetainedEarnings] as float)*1e6 RetainedEarnings
                , cast([Revenues] as float)*1e6 NetSales
                , cast([mCapUSD] as float)*1e6 mCapUSD 
                , cast(getdate() as date)
                , [BusinessDescription]
                , [MarketCapCurrency]
                , [periodEndDate]
                , cast([Low52Week] as float)*1e6  Low52Week
                , cast([High52Week] as float)*1e6  High52Week
                , cast([InstitutionalOwnershipPercent] as float) / 100 InstitutionalOwnershipPercent
                , cast([InsiderOwnershipPercent] as float) / 100 InsiderOwnershipPercent
                , cast([TotalEquity] as float)*1e6 TotalEquity
            from 
            [dbo].[vwCAPIQ_PubDO_leadership_features]
            where tickerSymbol like '%{ticker}%'
            order by TwoYearMarketCapHigh desc
            """
    elif name:
        query = f"""
            select [companyId]
                , [companyName]
                , [tickerSymbol]
                , [exchangeName]
                , cast([TwoYearMarketCapHighOrigCCY] as float)*1e6 TwoYearMarketCapHighOrigCCY
                , [AsOfDate]
                , [SIC_Code]
                , [IPODate]
                , cast([TotalAssets] as float)*1e6 TotalAssets
                , [min_trading_volume_adr]
                , [volatility_trading_volume_downturn_adr]
                , [percentage_execs_under_fifty]
                , cast([EBIT] as float)*1e6 EBIT
                , cast([CurrentAssets] as float)*1e6 CurrentAssets
                , cast([TotalLiabilities] as float)*1e6 TotalLiabilities
                , cast([CurrentLiabilities] as float)*1e6 CurrentLiabilities
                , cast([RetainedEarnings] as float)*1e6 RetainedEarnings
                , cast([Revenues] as float)*1e6 NetSales
                , cast([mCapUSD] as float)*1e6 mCapUSD 
                , cast(getdate() as date)
                , [BusinessDescription]
                , [MarketCapCurrency]
                , [periodEndDate]
                , cast([Low52Week] as float)*1e6  Low52Week
                , cast([High52Week] as float)*1e6  High52Week
                , cast([InstitutionalOwnershipPercent] as float) / 100 InstitutionalOwnershipPercent
                , cast([InsiderOwnershipPercent] as float) / 100 InsiderOwnershipPercent
                , cast([TotalEquity] as float)*1e6 TotalEquity
            from 
            [dbo].[vwCAPIQ_PubDO_leadership_features]
            where companyName like '%{name}%'
            order by TwoYearMarketCapHigh desc
            """

    columns = [
        'id',
        'insured_name',
        'ticker',
        'exchange',
        'market_cap_2_year_high',
        'date_updated',
        'sic_code',
        'ipo_date',
        'total_assets',
        'minimum_trading_volume',
        'volatility_trading_volume',
        'execs_under_fifty',
        'ebit',
        'current_assets',
        'total_liabilities',
        'current_liabilities',
        'retained_earnings',
        'net_sales',
        'current_market_cap',
        'source',
        'company_description',
        'currency',
        'period_ended',
        'fifty_two_week_low',
        'fifty_two_week_high',
        'institutional_ownership_share',
        'insider_shareholder_share',
        "equity"
    ]

    if query:
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
def populate_capiq_data(hxd,process):
    capiq = hxd.cds.capiq

    # read in capiq data table
    capiq_data = utils.pd_df_from_hx_list(capiq)

    # Update capiq data table in UI to only show the selected row
    capiq_output = capiq_data.copy(deep=True)
    capiq_output = capiq_output.replace({np.nan: None})
    capiq_output = capiq_output[capiq_output["selection"]]
    capiq_output = capiq_output[["selection", "insured_name", "exchange", "market_cap_2_year_high", "currency", "date_updated"]]
    setattr(hxd.cds,"capiq",capiq_output.to_dict("records"))
    hxd.cds.capiq_results = "Results for " + str(capiq_output["insured_name"].iloc[0]) + " populated"

    # Search for true values in boolean column
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

            # Converting NaNs to None
            capiq_data = capiq_data.replace({np.nan: None})

            # Populating rater fields with CapIQ data
            hxd.cds.standard_fields.insured_name = capiq_data.insured_name 
            hxd.cds.key_industry.ticker = capiq_data.ticker
            hxd.cds.risk_information.company_description = capiq_data.company_description
            hxd.cds.exposure.aggregate.main_exchange = capiq_data.exchange
            hxd.cds.exposure.aggregate.period_ended = capiq_data.period_ended



            # FX Rates
            fx_rates = params.fx_rates.df()

            source_ccy = capiq_data.currency if capiq_data.currency else "USD"
            target_ccy = hxd.cds.currencies.source_currency

            fx_rate = utils.ratio(fx_rates[fx_rates["ccy"]==target_ccy]["fx_rate"].iloc[0], fx_rates[fx_rates["ccy"]==source_ccy]["fx_rate"].iloc[0])

            
            hxd.cds.exposure.aggregate.ipo_date = capiq_data.ipo_date
            hxd.cds.exposure.aggregate.market_cap_2_year_high = capiq_data.market_cap_2_year_high * fx_rate if capiq_data.market_cap_2_year_high else None
            hxd.cds.exposure.aggregate.minimum_trading_volume = capiq_data.minimum_trading_volume * fx_rate if capiq_data.minimum_trading_volume else None
            hxd.cds.exposure.aggregate.volatility_trading_volume = capiq_data.volatility_trading_volume
            hxd.cds.exposure.aggregate.execs_under_fifty = capiq_data.execs_under_fifty
            hxd.cds.exposure.aggregate.total_assets = capiq_data.total_assets * fx_rate if capiq_data.total_assets else None
            hxd.cds.exposure.aggregate.ebit = capiq_data.ebit * fx_rate if capiq_data.ebit else None
            hxd.cds.exposure.aggregate.current_assets = capiq_data.current_assets * fx_rate if capiq_data.current_assets else None
            hxd.cds.exposure.aggregate.total_liabilities = capiq_data.total_liabilities * fx_rate if capiq_data.total_liabilities else None
            hxd.cds.exposure.aggregate.current_liabilities = capiq_data.current_liabilities * fx_rate if capiq_data.current_liabilities else None
            hxd.cds.exposure.aggregate.retained_earnings = capiq_data.retained_earnings * fx_rate if capiq_data.retained_earnings else None
            hxd.cds.exposure.aggregate.net_sales = capiq_data.net_sales * fx_rate if capiq_data.net_sales else None
            hxd.cds.exposure.aggregate.equity = capiq_data.equity * fx_rate if capiq_data.equity else None
            hxd.cds.exposure.aggregate.current_market_cap = capiq_data.current_market_cap * fx_rate if capiq_data.current_market_cap else None
            hxd.cds.exposure.aggregate.fifty_two_week_high = capiq_data.fifty_two_week_high * fx_rate if capiq_data.fifty_two_week_high else None
            hxd.cds.exposure.aggregate.fifty_two_week_low = capiq_data.fifty_two_week_low * fx_rate if capiq_data.fifty_two_week_low else None
            hxd.cds.exposure.aggregate.insider_shareholder_share = capiq_data.insider_shareholder_share if capiq_data.insider_shareholder_share else None
            hxd.cds.exposure.aggregate.institutional_ownership_share = capiq_data.institutional_ownership_share if capiq_data.institutional_ownership_share else None

            df_sic = hx.params.tbl_sic
            if capiq_data.sic_code is not None:
                sic = int(capiq_data.sic_code)
            else:
                sic = None

            if sic:
                if hxd.cds.rating_factors.risk_information.search_sic == "Class":
                    hxd.cds.rating_factors.risk_information.industry_class_sic_code = df_sic["Sic Code"][df_sic["Sic Code"].str.contains(str(sic), na=False)].iloc[0]
                else:
                    hxd.cds.rating_factors.risk_information.industry_class_sic_code = df_sic["Sic Code2 (SIC first)"][df_sic["Sic Code2 (SIC first)"].str.contains(str(sic), na=False)].iloc[0]


            hxd.cds.capiq_populate = "Populate Rater succeeded"


    return