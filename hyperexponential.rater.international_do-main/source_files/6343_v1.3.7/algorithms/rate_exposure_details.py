import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter
from algorithms.rate_constants import RAG_STATUS


# Import RAG Definition

def set_fin_metric(base_path, rag_tbl, metric, value):
    rag_tbl=rag_tbl[rag_tbl["metric"]==metric]
    operator = rag_tbl["sign"].iloc[0]
    red = rag_tbl["red"].iloc[0]
    amber = rag_tbl["amber"].iloc[0]

    if operator == "<":
        if value < red:
            rag = "red"
        elif value < amber:
            rag = "amber"
        else:
            rag = "green"
    elif operator == ">":
        if value > red:
            rag = "red"
        elif value > amber:
            rag = "amber"
        else:
            rag = "green"

    path = getattr(base_path, metric)
    
    # set values
    setattr(path, "value", value)
    setattr(path, "rag_status", RAG_STATUS[rag])

def rate_exposure_details(hxd):
    exp = hxd.cds.exposure.aggregate
    rf_risk_info = hxd.cds.rating_factors.risk_information
    rag_tbl = getattr(hx.params, "tbl_financial_metrics_rag")

    # Assigning Calculated Financial Metrics
    if all(var is not None for var in (exp.current_assets, exp.current_liabilities)):
        set_fin_metric(exp, rag_tbl, "current_ratio", utils.ratio(exp.current_assets, exp.current_liabilities, 0))

    if all(var is not None for var in (exp.retained_earnings, exp.total_assets)):
        set_fin_metric(exp, rag_tbl, "accumulated_profitability", utils.ratio(exp.retained_earnings, exp.total_assets, 0))

    if all(var is not None for var in (exp.ebit, exp.total_assets)):
        set_fin_metric(exp, rag_tbl, "return_on_assets", utils.ratio(exp.ebit, exp.total_assets, 0))

    if all(var is not None for var in (exp.equity, exp.total_liabilities)):
        set_fin_metric(exp, rag_tbl, "book_value_liability_ratio", utils.ratio(exp.equity, exp.total_liabilities, 0))

    if all(var is not None for var in (exp.net_sales, exp.total_assets)):
        set_fin_metric(exp, rag_tbl, "asset_turnover", utils.ratio(exp.net_sales, exp.total_assets, 0))

    # Z score used hardcoded constants in the Excel rater without documentation as to their derivation, using the same calcualtion here
    if all(var is not None for var in (exp.total_assets, exp.current_assets, exp.current_liabilities, exp.accumulated_profitability.value, exp.return_on_assets.value, exp.book_value_liability_ratio.value, exp.asset_turnover.value)):
        result = (0.847 * exp.accumulated_profitability.value + 3.107 * exp.return_on_assets.value 
                + 0.42 * exp.book_value_liability_ratio.value + 0.998 * exp.asset_turnover.value 
                + 0.717 * utils.ratio(exp.current_assets - exp.current_liabilities, exp.total_assets, 0))
        set_fin_metric(exp, rag_tbl, "z_score", result)

    if all(var is not None for var in (exp.net_profit, exp.equity)):
        set_fin_metric(exp, rag_tbl, "roe", utils.ratio(exp.net_profit, exp.equity, 0))

    if all(var is not None for var in (exp.net_debt, exp.equity)):
        set_fin_metric(exp, rag_tbl, "net_debt_equity_ratio", utils.ratio(exp.net_debt, exp.equity, 0))
   
    if all(var is not None for var in (exp.operating_cashflow, exp.ebitda)):
        set_fin_metric(exp, rag_tbl, "cash_conversion", utils.ratio(exp.operating_cashflow, exp.ebitda, 0))


    # Note on Company Search
    hxd.cds.exposure.aggregate.company_search_info = 'Search results will be for Ticker if both Ticker and Company Search are populated'

    # Info for Credit Score
    hxd.cds.exposure.aggregate.credit_score_info = "This is no longer populated by the CapIQ search, would require manual entry if needed"

    # Exposure Details Validation

    if (exp.market_cap_2_year_high is None and rf_risk_info.ownership_type == "Public"):
        hx.errors.validation("Exposure Details: Enter Market Cap")


    if ((exp.total_assets is None and exp.us_listing_share == 1)
        or (exp.total_assets is None and rf_risk_info.ownership_type == "Private")):
        hx.errors.validation("Exposure Details: Enter Total Assets")



    if (rf_risk_info.us_adr_exposure == "Yes"
        and rf_risk_info.ownership_type == "Public"
        and exp.adr_level is None):
        hx.errors.validation("Exposure Details: Select ADR Level")


    if (rf_risk_info.us_adr_exposure == "Yes"
        and rf_risk_info.ownership_type == "Public"
        and (exp.us_listing_share is None or exp.us_listing_share == 0)
        and rf_risk_info.primary_listing_location == "USA"):
        hx.errors.validation("Exposure Details: Policy primarily listed in the US. Enter % traded on US Exchange")
    elif (rf_risk_info.us_adr_exposure == "Yes"
        and rf_risk_info.ownership_type == "Public"
        and (exp.us_listing_share is not None and exp.us_listing_share > 0)
        and exp.adr_level == "Level 1"
        and rf_risk_info.primary_listing_location != "USA"):
        hxd.cds.level_1_us_exp_flag = True
        hxd.cds.level_1_us_exp_msg = "Level 1 listed should not have a US Listing % share"
    elif (rf_risk_info.us_adr_exposure == "Yes"
        and rf_risk_info.ownership_type == "Public"
        and (exp.us_listing_share is None or exp.us_listing_share == 0)
        and (exp.adr_level != "Level 1" and exp.adr_level is not None)):
        hx.errors.validation("Exposure Details: Level 2 and Above must have a US Listing % share")

    
    if (rf_risk_info.ownership_type == "Private"
        and exp.exposure_currency is None):
        hx.errors.validation("Exposure Details: Select Exposure Currency")



    
    





    


