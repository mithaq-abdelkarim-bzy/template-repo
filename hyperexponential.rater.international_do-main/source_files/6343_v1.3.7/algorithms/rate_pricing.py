import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
import algorithms.dataframe_functions as df_func
import algorithms.freq_sev_functions as freq_sev_func
import algorithms.rate_side_abc_expected_loss as side_abc
import algorithms.rate_side_a_expected_loss as side_a
from algorithms import parameter_tables_schema as params
from operator import itemgetter
from scipy.stats import gamma, poisson, lognorm, norm
import re as re
import datetime as date
import calendar as ca
import time


def rate_pricing(hxd):

    ###########################################
    ##########  Preliminary Inputs ############
    ###########################################

    # Define node shortcuts

    exp_agg = hxd.cds.exposure.aggregate
    rf_risk_info = hxd.cds.rating_factors.risk_information
    risk_info = hxd.cds.risk_information
    mod = hxd.cds.modifiers

    fx_rates = params.fx_rates.df()

    # First need to define input variables to be used in algorithm

    # Market Cap
    mcap_2year = exp_agg.market_cap_2_year_high or 0

    current_mcap = exp_agg.current_market_cap or 0

    insider_share = exp_agg.insider_shareholder_share or 0

    max_mcap = max(mcap_2year, current_mcap)

    total_mcap = max(max_mcap - (max_mcap * insider_share * 0.60), 0) if insider_share >= 0.20 else max_mcap

    # Ownership
    ownership = rf_risk_info.ownership_type

    # ADR Percentage
    if risk_info.public_flag is False or rf_risk_info.us_adr_exposure == "No" or exp_agg.us_listing_share is None:
        adr_share = 0
    else:
        adr_share = exp_agg.us_listing_share
    
    # Country
    if adr_share == 1:
        country = rf_risk_info.main_operating_country
    elif risk_info.public_flag is True:
        country = rf_risk_info.primary_listing_location
    else:
        country = rf_risk_info.main_operating_country

    # Ignore IPO Flag
    ipo_ignore = 1 if not risk_info.public_flag or exp_agg.ignore_ipo == "Yes" else 0

    # IPO Lag
    if exp_agg.ipo_date is not None:
        inception_date = hxd.hx_core.inception_date
        ipo_date = exp_agg.ipo_date
        ipo_lag = round(utils.year_diff(ipo_date, inception_date, False))
        if ipo_ignore == 1:
            ipo_lag = 5
        else:
            ipo_lag = max(0, min(ipo_lag, 5))
    else:
        ipo_lag = 5

    # Extract SIC Code 
    sic = utils.extract_sic(rf_risk_info.industry_class_sic_code) if rf_risk_info.industry_class_sic_code else None
    
    # Sector from SIC Code
    sector = utils.look_up(int(sic.lstrip("0")), "SIC", "Sector", hx.params.tbl_sic_freq, if_not_found = "Not Found") if sic else None

    # FX Rates
    ccy = hxd.cds.currencies.source_currency
    fx_rate = fx_rates[fx_rates["ccy"]==ccy]["fx_rate"].iloc[0]

    # Exposure currency for private companies, defaults to source currency if exposure currency is left blank
    exp_ccy = hxd.cds.exposure.aggregate.exposure_currency or hxd.cds.currencies.source_currency

    exp_fx_rate = fx_rates[fx_rates["ccy"]==exp_ccy]["fx_rate"].iloc[0]

    # Total Assets
    total_assets = exp_agg.total_assets or 0

    # Total Assets (USD)
    if risk_info.private_flag is False:
        total_assets_usd = total_assets/fx_rate
    else:
        total_assets_usd = total_assets/exp_fx_rate

    # Credit Score
    credit_score = exp_agg.credit_score or "NA"

    # EBIT
    ebit = exp_agg.ebit or 0

    # Net Sales
    net_sales = exp_agg.net_sales or 0

    # Total Liabilities
    total_liabs = exp_agg.total_liabilities or 0

    # Current Assets
    current_assets = exp_agg.current_assets or 0

    # Current Liabilities
    current_liabs = exp_agg.current_liabilities or 0

    # Retained Earnings
    retained_earnings = exp_agg.retained_earnings or 0

    # Period Data
    period_data = exp_agg.period_data or 0

    # US ADR Exposure Flag
    adr_flag = "Yes" if rf_risk_info.us_adr_exposure == "Yes" else "NA"

    # ADR Level
    adr_level = exp_agg.adr_level or "NA"

    # Minimum Trading Volume
    min_trading_volume = None if exp_agg.minimum_trading_volume in (None, -999) else exp_agg.minimum_trading_volume

    # Volatility Trading Volume
    volatility_trading_volume = None if exp_agg.volatility_trading_volume in (None, -999) else exp_agg.volatility_trading_volume

    # Percentage of Executives Under 50
    execs_under_fifty = None if exp_agg.execs_under_fifty in (None, -999) else exp_agg.execs_under_fifty

    # Total Market Cap (Unadjusted for Insider Shareholding)
    market_cap = exp_agg.market_cap_2_year_high or 0

    current_market_cap = exp_agg.current_market_cap or 0

    total_mcap_unadj = max(market_cap, current_market_cap)

    # Term Adjustment Factor 
    term_adj_factor = round(utils.year_diff(hxd.hx_core.inception_date, hxd.hx_core.expiry_date, False), 2)

    # Assinging Side AB Discount in Rating Summary

    for layer in hxd.cds.large_cap.layers:
        if layer.side_selection is None:
            layer.side_ab_discount = None
        elif layer.side_selection == "AB":
            layer.side_ab_discount = utils.look_up(country, "Country", "SideBSelectedDiscount", hx.params.tbl_intl_countries, 0)
        else:
            layer.side_ab_discount = 0
     
    # ILF Calculations 
    # Converting Adjusted Market Cap to USD
    if ownership == "Private":
        market_cap_adjusted_usd = total_assets/exp_fx_rate
    else:
        market_cap_adjusted_usd = total_mcap/fx_rate

    # Create the dataframe of the bounds and relativities
    df_market_ilf = pd.DataFrame(hx.params.tbl_market_ilf)

    # Perform linear interpolation
    interpolated_ilf = utils.interp_table_row(df_market_ilf, market_cap_adjusted_usd, "MarketCap_Lo", "MarketCap_Hi", "ILF_Lo", "ILF_Hi", 1)

    # High Risk Sector Loading
    # Market Cap Banding
    if total_mcap_unadj == 0:
        mcap_band = "Unknown"
    elif total_mcap_unadj < 10e9:
        mcap_band = "a) Less than $10bn"
    elif total_mcap_unadj < 50e9:
        mcap_band = "b) $10bn - $50bn" 
    else:
        mcap_band = "c) Greater than $50bn"

    # ADR Group
    if adr_level is not None:
        if adr_level == "Level 2" or adr_level == "Level 3" or adr_level == "Full Listing":
            adr_group = "Level 2 and above"
        elif country == "AUSTRALIA":
            adr_group = "Listed in AUS"
        else:
            adr_group = "Level 1, No-AUS Listing and No-US Listing"
    else:
        adr_group = "No ADR Exposure"

    # Create dataframe of bounds and relativities
    df_high_risk_segments = pd.DataFrame(hx.params.tbl_high_risk_segment)

    concat_string = mcap_band + adr_group

    matching_rows = df_high_risk_segments[df_high_risk_segments["Concat"] == concat_string]

    if matching_rows.empty is False:
        if ownership =="Public":
            high_risk_segment_loading = 1 + utils.interp_table_row(matching_rows, total_mcap_unadj, "Lower Band", "Upper Band", "Lower Loading", "Upper Loading", 1)
        else:
            high_risk_segment_loading = 1
    else: high_risk_segment_loading = 1

    # US Market Cap Curve Adjustment
    adr_market_cap = adr_share * market_cap_adjusted_usd 

    # Define constants for calculation
    k0 = 241.7
    k1 = -0.15

    if adr_market_cap == 0:
        us_mcap_curve_factor = 1
    else:
        us_mcap_curve_factor = k0 * (adr_market_cap ** k1)

    revised_adr_market_cap = adr_market_cap * us_mcap_curve_factor
    
    # Adding Required Premliminary Inputs to an Array as they're Needed as Inputs for Freq/Sev and Expected Loss Functions
    prelim_inputs = {}

    prelim_inputs["adr_share"] = adr_share
    prelim_inputs["market_cap_adjusted_usd"] = market_cap_adjusted_usd
    prelim_inputs["adr_level"] = adr_level
    prelim_inputs["revised_adr_market_cap"] = revised_adr_market_cap
    prelim_inputs["sic"] = sic
    prelim_inputs["sector"] = sector
    prelim_inputs["ipo_ignore"] = ipo_ignore
    prelim_inputs["ipo_lag"] = ipo_lag
    prelim_inputs["min_trading_volume"] = min_trading_volume
    prelim_inputs["volatility_trading_volume"] = volatility_trading_volume
    prelim_inputs["execs_under_fifty"] = execs_under_fifty
    prelim_inputs["interpolated_ilf"] = interpolated_ilf
    prelim_inputs["total_assets"] = total_assets
    prelim_inputs["country"] = country
    prelim_inputs["ownership"] = ownership
    prelim_inputs["fx_rate"] = fx_rate
    prelim_inputs["term_adj_factor"] = term_adj_factor
    prelim_inputs["high_risk_segment_loading"] = high_risk_segment_loading
    prelim_inputs["adr_flag"] = adr_flag
 

    ###########################################
    ######### Creating Layer DataFrame ########
    ###########################################

    # Setting up dataframe with layer parameters

    layers = utils.pd_df_from_hx_list(hxd.cds.large_cap.layers).T

    # Filtering this dataframe to just the required rows

    rows_to_keep = [
        "side_selection",
        "side_ab_discount",
        "uw_side_ab_discount_override", 
        "limit",
        "excess",
        "deductible",
        "brokerage"
    ]

    layers = layers.loc[rows_to_keep]

    # Appending on two rows 

    excess_limit = [5000000] * layers.shape[1]

    ma_retention = [0] * layers.shape[1]

    layers = pd.concat([layers, pd.DataFrame([excess_limit, ma_retention], index=["excess_limit", "ma_retention"])])
    
    # Converting this to USD and omitting the rows which aren't needed to be converted

    layer_usd = layers.copy()

    layer_usd = layer_usd.apply(lambda x: x / fx_rate if x.name not in ("brokerage", "side_selection", "side_ab_discount", "uw_side_ab_discount_override") else x, axis = 1)

    # Removing NAs for ease of further calculations
    layer_usd = layer_usd.fillna(0)
    

    ###########################################
    ########## Step 1: ADR Standalone #########
    ###########################################


    adr_model_expected_loss_side_abc, adr_unity_expected_loss_side_abc = side_abc.adr_standalone_expected_loss(hxd, layer_usd, prelim_inputs)

    adr_model_expected_loss_side_a, adr_unity_expected_loss_side_a = side_a.adr_standalone_expected_loss_side_a(hxd, layer_usd, prelim_inputs)


    ###########################################
    ############ Step 2: Contagion ############
    ###########################################


    cont_model_expected_loss_side_abc, cont_unity_expected_loss_side_abc = side_abc.contagion_expected_loss(hxd, layer_usd, adr_model_expected_loss_side_abc, adr_unity_expected_loss_side_abc, prelim_inputs)
        
    cont_model_expected_loss_side_a, cont_unity_expected_loss_side_a = side_a.contagion_expected_loss_side_a(hxd, layer_usd, adr_model_expected_loss_side_a, adr_unity_expected_loss_side_a, prelim_inputs)
    

    ###########################################
    ######### Step 3: Intl Standalone #########
    ###########################################

    intl_model_expected_loss_side_abc, intl_unity_expected_loss_side_abc, _ = side_abc.intl_standalone_expected_loss(hxd, layer_usd, prelim_inputs)

    intl_model_expected_loss_side_a, intl_unity_expected_loss_side_a = side_a.intl_standalone_expected_loss_side_a(hxd, layer_usd, prelim_inputs)


    ###########################################
    ########## Step 4: Large Company ##########
    ###########################################


    lc_model_expected_loss_side_abc, lc_unity_expected_loss_side_abc = side_abc.intl_large_company_expected_loss(hxd, layer_usd, prelim_inputs)

    lc_model_expected_loss_side_a, lc_unity_expected_loss_side_a = side_a.intl_large_company_expected_loss_side_a(hxd, layer_usd, prelim_inputs)


    ###########################################
    ######## Step 5: Summary Dataframes #######
    ###########################################

    # Model and CAT Expected Losses
    df_total_expected_loss_side_abc, df_cat_expected_loss_side_abc, _ = df_func.calc_summary_dataframe(hxd, adr_model_expected_loss_side_abc, cont_model_expected_loss_side_abc, intl_model_expected_loss_side_abc, lc_model_expected_loss_side_abc, layer_usd, prelim_inputs)

    df_total_expected_loss_side_a, df_cat_expected_loss_side_a, _ = df_func.calc_summary_dataframe(hxd, adr_model_expected_loss_side_a, cont_model_expected_loss_side_a, intl_model_expected_loss_side_a, lc_model_expected_loss_side_a, layer_usd, prelim_inputs, is_side_a = True)

    df_total_expected_loss = pd.DataFrame(columns=[str(i) for i in range(layer_usd.shape[1])], index = ["adr_standalone", "contagion", "intl_standalone", "intl_large_company", "total"])
    df_cat_expected_loss = pd.DataFrame(columns=[str(i) for i in range(layer_usd.shape[1])], index = ["adr_standalone", "contagion", "intl_standalone", "intl_large_company", "total"])

    for index, layer in enumerate(hxd.cds.large_cap.layers):
        if layer.side_selection in ["ABC", "AB"] and layer.limit is not None:
            # Assign values from the Side ABC DataFrame
            df_total_expected_loss.iloc[:, index] = df_total_expected_loss_side_abc.iloc[:, index]
            df_cat_expected_loss.iloc[:, index] = df_cat_expected_loss_side_abc.iloc[:, index]
        elif layer.side_selection in ["A-side", "A-side DIC"] and layer.limit is not None:
            # Assign values from the Side A DataFrame
            df_total_expected_loss.iloc[:, index] = df_total_expected_loss_side_a.iloc[:, index]
            df_cat_expected_loss.iloc[:, index] = df_cat_expected_loss_side_a.iloc[:, index]
        else:
            # Assign a column of zeros
            df_total_expected_loss.iloc[:, index] = [0] * len(df_total_expected_loss)
            df_cat_expected_loss.iloc[:, index] = [0] * len(df_cat_expected_loss)

    # Creating a dataframe with all the expected losses needed to be written to the view, i.e. taking the side selection by coverage (A, AB, ABC)
    df_rating_summary_values = pd.DataFrame(columns = range(layers.shape[1]))

    df_rating_summary_values.loc["adr_standalone"] = df_total_expected_loss.loc["adr_standalone"].values

    df_rating_summary_values.loc["contagion"] = df_total_expected_loss.loc["contagion"].values

    df_rating_summary_values.loc["intl_standalone"] = df_total_expected_loss.loc["intl_standalone"].values

    df_rating_summary_values.loc["intl_large_company"] = df_total_expected_loss.loc["intl_large_company"].values

    df_rating_summary_values.loc["expected_loss_cost_att"] = df_total_expected_loss.loc["total"].values - df_cat_expected_loss.loc["total"].values

    df_rating_summary_values.loc["expected_loss_cost_cat"] = df_cat_expected_loss.loc["total"].values

    df_rating_summary_values.loc["expected_loss_cost"] = df_total_expected_loss.loc["total"].values

    df_rating_summary_values = df_rating_summary_values.fillna(0).T

    for i in df_rating_summary_values.columns:
        utils.write_pd_to_hxd(df_rating_summary_values, hxd.cds.large_cap.layers, [f"{i}"])

    # Unity Expected Losses (Unity denotes the exclusion of UW adjustments)
    df_total_unity_expected_loss_side_abc, df_cat_unity_expected_loss_side_abc, _ = df_func.calc_summary_dataframe(hxd, adr_unity_expected_loss_side_abc, cont_unity_expected_loss_side_abc, intl_unity_expected_loss_side_abc, lc_unity_expected_loss_side_abc, layer_usd, prelim_inputs)

    df_total_unity_expected_loss_side_a, df_cat_unity_expected_loss_side_a, _ = df_func.calc_summary_dataframe(hxd, adr_unity_expected_loss_side_a, cont_unity_expected_loss_side_a, intl_unity_expected_loss_side_a, lc_unity_expected_loss_side_a, layer_usd, prelim_inputs, is_side_a = True)

    df_total_unity_expected_loss = pd.DataFrame(columns=[str(i) for i in range(layer_usd.shape[1])], index = ["adr_standalone", "contagion", "intl_standalone", "intl_large_company", "total"])
    df_cat_unity_expected_loss = pd.DataFrame(columns=[str(i) for i in range(layer_usd.shape[1])], index = ["adr_standalone", "contagion", "intl_standalone", "intl_large_company", "total"])

    for index, layer in enumerate(hxd.cds.large_cap.layers):
        if layer.side_selection in ["ABC", "AB"] and layer.limit is not None:
            # Assign values from the Side ABC DataFrame
            df_total_unity_expected_loss.iloc[:, index] = df_total_unity_expected_loss_side_abc.iloc[:, index]
            df_cat_unity_expected_loss.iloc[:, index] = df_cat_unity_expected_loss_side_abc.iloc[:, index]
        elif layer.side_selection in ["A-side", "A-side DIC"] and layer.limit is not None:
            # Assign values from the Side A DataFrame
            df_total_unity_expected_loss.iloc[:, index] = df_total_unity_expected_loss_side_a.iloc[:, index]
            df_cat_unity_expected_loss.iloc[:, index] = df_cat_unity_expected_loss_side_a.iloc[:, index]
        else:
            # Assign a column of zeros otherwise
            df_total_unity_expected_loss.iloc[:, index] = [0] * len(df_total_unity_expected_loss)
            df_cat_unity_expected_loss.iloc[:, index] = [0] * len(df_cat_unity_expected_loss)

    expected_loss_cost_pre_uw_adj = pd.DataFrame({"expected_loss_cost_pre_uw_adj" : df_total_unity_expected_loss.loc["total"].values})

    utils.write_pd_to_hxd(expected_loss_cost_pre_uw_adj, hxd.cds.large_cap.layers, ["expected_loss_cost_pre_uw_adj"]) 

    # Calcualting Impact of UW adjustments (Adding small positive value to avoid divide by 0 errors)
    uw_adj_impact = ((df_total_expected_loss.loc["total"] + 0.000001) / (df_total_unity_expected_loss.loc["total"] + 0.000001) - 1).values

    uw_adj_impact = pd.DataFrame({"uw_adj_impact" : uw_adj_impact}) 
  
    utils.write_pd_to_hxd(uw_adj_impact, hxd.cds.large_cap.layers, ["uw_adj_impact"])

    # Calculating Net Technical Premiums    

    # First need to get written line from cds/layers
    written_line = np.array(utils.pd_df_from_hx_list(hxd.cds.large_cap.layers)["written_line"])
    written_line = np.where(written_line == None, 0, written_line)

    net_tech_prem = pd.DataFrame(utils.calc_net_tech_premium(df_rating_summary_values["expected_loss_cost"] * np.where(written_line != 0, written_line, 1), hxd)).where(df_rating_summary_values["expected_loss_cost"] != 0, 0)
    
    net_unity_tech_prem = np.where(df_total_unity_expected_loss.loc["total"] != 0, utils.calc_net_tech_premium(df_total_unity_expected_loss.loc["total"] * np.where(written_line != 0, written_line, 1), hxd), 0)
    
    # Grossing this up and Assinging to the hxd
    technical_premium = pd.DataFrame(np.array(net_tech_prem).flatten() / (1 - layer_usd.loc["brokerage"].values.flatten()) , columns=["technical_premium"])

    technical_premium = technical_premium.fillna(0)

    unity_technical_premium = pd.DataFrame(np.array(net_unity_tech_prem).flatten() / (1 - layer_usd.loc["brokerage"].values.flatten()) , columns=["technical_premium_pre_uw_adj"])

    unity_technical_premium = unity_technical_premium.fillna(0)

    # Use the function to write the DataFrame to hxd
    utils.write_pd_to_hxd(technical_premium, hxd.cds.large_cap.layers, ["technical_premium"])

    utils.write_pd_to_hxd(unity_technical_premium, hxd.cds.large_cap.layers, ["technical_premium_pre_uw_adj"])


    ###########################################
    ############ Cost Percentiles #############
    ###########################################

    # Side ABC

    # Gather all Required Variables (Dismissal, Log Mu, Log Sigma) for 3 Coverages (Intl Standalone, US, Large Company)
    side_abc_dismiss, side_abc_log_mu, side_abc_log_sigma, side_abc_exp_loss, side_abc_exp_lr = df_func.get_cost_percentile_inputs(hxd, prelim_inputs)

    # Calculates 50% and 75% Cost Percentiles
    side_abc_percentiles = df_func.calc_cost_percentiles(side_abc_dismiss, side_abc_log_mu, side_abc_log_sigma)

    # Calculating Frequency for Each Coverage
    side_abc_model_premium = (side_abc_exp_loss / side_abc_exp_lr).sum()

    intl_freq = (side_abc_model_premium / utils.truncated_lognormal(10e6 / fx_rate, np.finfo(float).eps, side_abc_log_mu[0], side_abc_log_sigma[0], 1)).iloc[0]

    adr_sector_freq = freq_sev_func.freq_function_variables("ADR Standalone", prelim_inputs)["sca_sector_freq_factor"]

    lc_mcap = freq_sev_func.freq_function_variables("Large Company", prelim_inputs)["mcap"]

    lc_sector_freq = freq_sev_func.freq_function_variables("Large Company", prelim_inputs)["sca_sector_freq_factor"]

    if adr_share * total_mcap / fx_rate > 0:
        us_freq = adr_sector_freq
    else:
        us_freq = 0

    if lc_mcap >= 1.5e6:
        lc_freq = lc_sector_freq
    else:
        lc_freq = 0

    # Calculating Weights for Weighted Averages
    intl_wgt = utils.ratio(side_abc_exp_loss.loc["intl_standalone"],  side_abc_exp_loss.loc["total"], np.finfo(float).eps)

    us_wgt = utils.ratio(side_abc_exp_loss.loc["adr_standalone"] + side_abc_exp_loss.loc["contagion"], side_abc_exp_loss.loc["total"], np.finfo(float).eps)

    lc_wgt = utils.ratio(side_abc_exp_loss.loc["intl_large_company"], side_abc_exp_loss.loc["total"], np.finfo(float).eps)

    freqs = np.array([intl_freq, us_freq, lc_freq], dtype = np.float64)

    weights = np.array([intl_wgt, us_wgt, lc_wgt], dtype = np.float64).reshape(-1) 

    perc_50_after_dismiss = np.array(side_abc_percentiles.loc["perc_50_after_dismiss"].values, dtype = np.float64)
    perc_75_after_dismiss = np.array(side_abc_percentiles.loc["perc_75_after_dismiss"].values, dtype = np.float64)
    perc_50_cost_only = np.array(side_abc_percentiles.loc["perc_50_cost_only"].values, dtype = np.float64)
    perc_75_cost_only = np.array(side_abc_percentiles.loc["perc_75_cost_only"].values, dtype = np.float64)

    # Compute weighted average to show in view (Side ABC)
    hxd.cds.rating_summary.side_abc_fifty_percentile.inclusive_dismissals = np.average(perc_50_after_dismiss, weights=weights) if sum(perc_50_after_dismiss) > 0 else 0
    hxd.cds.rating_summary.side_abc_seventyfive_percentile.inclusive_dismissals = np.average(perc_75_after_dismiss, weights=weights) if sum(perc_75_after_dismiss) > 0 else 0
    hxd.cds.rating_summary.side_abc_fifty_percentile.at_cost_only = np.average(perc_50_cost_only, weights=weights) if sum(perc_50_cost_only) > 0 else 0
    hxd.cds.rating_summary.side_abc_seventyfive_percentile.at_cost_only = np.average(perc_75_cost_only, weights=weights) if sum(perc_75_cost_only) > 0 else 0
    hxd.cds.rating_summary.side_abc_sca_freq = np.average(freqs, weights=weights) if sum(freqs) > 0 else 0


    # Side A

    # Gather all Required Variables (Dismissal, Log Mu, Log Sigma) for 3 Coverages (Intl Standalone, US, Large Company)
    side_a_dismiss, side_a_log_mu, side_a_log_sigma, side_a_exp_loss, side_a_exp_lr = df_func.get_cost_percentile_inputs(hxd, prelim_inputs, is_side_a = True)

    # Calculates 50% and 75% Cost Percentiles
    side_a_percentiles = df_func.calc_cost_percentiles(side_a_dismiss, side_a_log_mu, side_a_log_sigma)

    # Calculating Frequency for Each Coverage
    side_a_model_premium = (side_a_exp_loss / side_a_exp_lr).sum()

    side_a_intl_freq = (side_a_model_premium / utils.truncated_lognormal(10e6 / fx_rate, np.finfo(float).eps, side_a_log_mu[0], side_a_log_sigma[0], 1)).iloc[0]

    side_a_adr_sector_freq = freq_sev_func.freq_function_variables("ADR Standalone", prelim_inputs, is_side_a = True)["sca_sector_freq_factor"]

    side_a_lc_mcap = freq_sev_func.freq_function_variables("Large Company", prelim_inputs, is_side_a = True)["mcap"]

    side_a_lc_sector_freq = freq_sev_func.freq_function_variables("Large Company", prelim_inputs, is_side_a = True)["sca_sector_freq_factor"]

    if adr_share * total_mcap / fx_rate > 0:
        side_a_us_freq = side_a_adr_sector_freq
    else:
        side_a_us_freq = 0

    if side_a_lc_mcap >= 1.5e6:
        side_a_lc_freq = side_a_lc_sector_freq
    else:
        side_a_lc_freq = 0

    # Calculating Weights for Weighted Averages
    side_a_intl_wgt = utils.ratio(side_a_exp_loss.loc["intl_standalone"],  side_a_exp_loss.loc["total"], np.finfo(float).eps)

    side_a_us_wgt = utils.ratio(side_a_exp_loss.loc["adr_standalone"] + side_a_exp_loss.loc["contagion"], side_a_exp_loss.loc["total"], np.finfo(float).eps)

    side_a_lc_wgt = utils.ratio(side_a_exp_loss.loc["intl_large_company"], side_a_exp_loss.loc["total"], np.finfo(float).eps)

    side_a_freqs = np.array([side_a_intl_freq, side_a_us_freq, side_a_lc_freq], dtype = np.float64)

    side_a_weights = np.array([side_a_intl_wgt, side_a_us_wgt, side_a_lc_wgt], dtype = np.float64).reshape(-1) 

    side_a_perc_50_after_dismiss = np.array(side_a_percentiles.loc["perc_50_after_dismiss"].values, dtype = np.float64)
    side_a_perc_75_after_dismiss = np.array(side_a_percentiles.loc["perc_75_after_dismiss"].values, dtype = np.float64)
    side_a_perc_50_cost_only = np.array(side_a_percentiles.loc["perc_50_cost_only"].values, dtype = np.float64)
    side_a_perc_75_cost_only = np.array(side_a_percentiles.loc["perc_75_cost_only"].values, dtype = np.float64)

    # Compute weighted average to show in view (Side A)
    hxd.cds.rating_summary.side_a_fifty_percentile.inclusive_dismissals = np.average(side_a_perc_50_after_dismiss, weights=side_a_weights) if sum(side_a_perc_50_after_dismiss) > 0 else 0
    hxd.cds.rating_summary.side_a_seventyfive_percentile.inclusive_dismissals = np.average(side_a_perc_75_after_dismiss, weights=side_a_weights) if sum(side_a_perc_75_after_dismiss) > 0 else 0
    hxd.cds.rating_summary.side_a_fifty_percentile.at_cost_only = np.average(side_a_perc_50_cost_only, weights=side_a_weights) if sum(side_a_perc_50_cost_only) > 0 else 0
    hxd.cds.rating_summary.side_a_seventyfive_percentile.at_cost_only = np.average(side_a_perc_75_cost_only, weights=side_a_weights) if sum(side_a_perc_75_cost_only) > 0 else 0
    hxd.cds.rating_summary.side_a_sca_freq = np.average(side_a_freqs, weights=side_a_weights) if sum(side_a_freqs) > 0 else 0


    ###########################################
    ########### Return on Capital #############
    ###########################################
       

    layer_roc = pd.DataFrame(df_func.calc_roc(hxd), columns=["roc"])

    utils.write_pd_to_hxd(layer_roc, hxd.cds.large_cap.layers, ["roc"])


    ###########################################
    ########### Graph Calculations#############
    ###########################################


    df_func.calc_graph_prem_build_up(hxd)


    ###########################################
    ############ MMP Calculations #############
    ###########################################

    # Function that creates Dataframe with MMP Option Limits, Excesses, Deductibles, and Brokerages this function takes an abbreviation of the coverage as an input from (dno, epl, cll)
    # The resulting dataframe comprises of 1 selected choice, and 4 options each row as an array [Selected, Option 1, ..., Option 4]

    mmp = hxd.cds.mmp

    def get_mmp_layers(coverage_abrv, hxd):

        mmp = hxd.cds.mmp
        cov = getattr(mmp, coverage_abrv)

        # Metrics (rows)
        metrics = ["limit", "excess", "deductible", "brokerage"]

        # Selected column (col 0)
        selected_column = pd.DataFrame(
            [cov.limit, cov.excess, cov.deductible, cov.brokerage],
            index=metrics
        )

        # Option columns (cols 1–4) from option_1..option_4
        option_cols = []
        for i in range(1, 5):
            opt = getattr(cov, f"option_{i}")
            option_cols.append([
                getattr(opt, "aggregate_limit"),
                getattr(opt, "aggregate_excess"),
                getattr(opt, "aggregate_deductible"),
                cov.brokerage  # brokerage same across options
            ])

        options_df = pd.DataFrame(option_cols, columns=metrics).T

        # Assemble final df (rows = metrics; cols = 0..n with 0 = selected)
        layer_mmp = pd.concat([selected_column, options_df], axis=1)
        layer_mmp.columns = range(layer_mmp.shape[1])

        # Appending on two rows
        excess_limit = [5000000] * layer_mmp.shape[1]
        ma_retention = [0] * layer_mmp.shape[1]
        layer_mmp = pd.concat([layer_mmp, pd.DataFrame([excess_limit, ma_retention], index=["excess_limit", "ma_retention"])])

        # Converting this to USD and omitting the rows which aren't needed to be converted
        layer_mmp_usd = layer_mmp.copy()
        layer_mmp_usd = layer_mmp_usd.apply(lambda x: x / fx_rate if x.name not in ("brokerage") else x, axis=1)

        # Removing NAs for ease of further calculations
        layer_mmp_usd = layer_mmp_usd.fillna(0)

        return layer_mmp_usd


    # 1. D&O: This is calculated via gross expected losses for side ABC using the MMP D&O limits, excesses, deductibles and brokerages

    # Getting D&O Layer Information
    layer_mmp_dno = get_mmp_layers("dno", hxd)

    # Side AB Discount
    if mmp.dno.coverage == "AB":
        mmp_side_ab_discount = utils.look_up(country, "Country", "SideBSelectedDiscount", hx.params.tbl_intl_countries, if_not_found = 0)
    else:
        mmp_side_ab_discount = 0

    # Getting expected losses
    
    adr_mmp_model_expected_loss, adr_mmp_unity_expected_loss = side_abc.adr_standalone_expected_loss(hxd, layer_mmp_dno, prelim_inputs)

    cont_mmp_model_expected_loss, cont_mmp_unity_expected_loss = side_abc.contagion_expected_loss(hxd, layer_mmp_dno, adr_mmp_model_expected_loss, adr_mmp_unity_expected_loss, prelim_inputs)

    intl_mmp_model_expected_loss, intl_mmp_unity_expected_loss, alpha = side_abc.intl_standalone_expected_loss(hxd, layer_mmp_dno, prelim_inputs)

    lc_mmp_model_expected_loss, lc_mmp_unity_expected_loss = side_abc.intl_large_company_expected_loss(hxd, layer_mmp_dno, prelim_inputs)

    # Getting the summary dataframes
    df_mmp_total_expected_loss, _, df_mmp_expected_lr = df_func.calc_summary_dataframe_mmp(hxd, adr_mmp_model_expected_loss, cont_mmp_model_expected_loss, intl_mmp_model_expected_loss, lc_mmp_model_expected_loss, layer_mmp_dno, prelim_inputs)

    df_mmp_total_expected_loss = df_mmp_total_expected_loss * (1 - mmp_side_ab_discount)

    # Converting this to Gross Technical Premium and assigning to the view (The selected choice is subject to written line whereas options are given as 100%)
    if mmp.dno.brokerage is None:
        dno_brokerage = 0
    else:
        dno_brokerage = mmp.dno.brokerage

    mmp_dno_written_line = 1 if mmp.dno.written_line is None else mmp.dno.written_line

    mmp.dno.technical_premium = utils.ratio(utils.calc_net_tech_premium(df_mmp_total_expected_loss.loc["total"].iloc[0] * mmp_dno_written_line, hxd) , (1 - dno_brokerage), 0) if hxd.cds.mmp.dno.limit else 0

    # Loop over option_1 .. option_4 for the given coverage
    for i in range(1, layer_mmp_dno.shape[1]):
        mmp_dno_obj = getattr(hxd.cds.mmp.dno, f"option_{i}")

        if getattr(mmp_dno_obj, "aggregate_limit"):
            value = utils.ratio(
                utils.calc_net_tech_premium(
                    df_mmp_total_expected_loss.loc["total"].iloc[i], 
                    hxd
                ),
                (1 - dno_brokerage),
                0
            )
        else:
            value = 0

        setattr(mmp_dno_obj, "technical_premium", value)

    # Gross Benchmark Premium (Subject to written line)
    mmp.dno.benchmark_premium = utils.ratio((df_mmp_total_expected_loss.loc["total"].iloc[0] * mmp_dno_written_line) / 0.7, (1 - dno_brokerage), 0) if hxd.cds.mmp.dno.limit else 0


    # 2. EPL:

    # Getting EPL Layer Information
    layer_mmp_epl = get_mmp_layers("epl", hxd)

    # Full Time Employees
    if exp_agg.us_ftes is not None:
        us_ftes = exp_agg.us_ftes
    else:
        us_ftes = 0

    if exp_agg.row_ftes is not None:
        row_ftes = exp_agg.row_ftes
    else:
        row_ftes = 0

    ftes = us_ftes + row_ftes

    # Assumed LR (This uses the modelled LR from Side ABC for the selected option)
    mmp_total_model_premium = (df_mmp_total_expected_loss[:-1] / (df_mmp_expected_lr * (1 - dno_brokerage))).sum()
    
    mmp_epl_assumed_lr = df_mmp_total_expected_loss.loc["total"].iloc[0] / (mmp_total_model_premium.iloc[0] * (1 - dno_brokerage))

    # Base Rate Calculation

    # Underlying Rate
    df_mmp_epl_base = pd.DataFrame(hx.params.tbl_mmp_epl_base)

    underlying_rate = utils.look_up_with_bounds(ftes, "Min", "Max", "Rate Running Total", df_mmp_epl_base)

    # Employees in Band
    employees_in_band = ftes - utils.look_up_with_bounds(ftes, "Min", "Max", "Min", df_mmp_epl_base)

    # Rate in Band
    rate_in_band = utils.look_up_with_bounds(ftes, "Min", "Max", "Rate per Employee in Band", df_mmp_epl_base)

    # Additional Rate in Band
    additional_rate = employees_in_band * rate_in_band

    # Base Rate
    mmp_epl_base_rate = underlying_rate + additional_rate

    # EPL Country Factor
    if country is not None:
        mmp_epl_country_factor = utils.look_up(country, "Country", "EPL Factor", hx.params.tbl_intl_countries)
    else:
        mmp_epl_country_factor = 0

    # Industry Factor
    if sic is not None:
        mmp_epl_industry_factor = utils.look_up(int(sic), "SIC", "EPL_COBFactor", hx.params.tbl_sic_freq)
    else:
        mmp_epl_industry_factor = 0

    # Limit Factor Calcs
    
    # Create the dataframe of the bounds and relativities
    df_mmp_epl_ilf = pd.DataFrame(hx.params.tbl_mmp_epl_ilf)

    def epl_limit_find_bounds(layer_df, bounds_df): 
        lower_bounds = [] 
        upper_bounds = [] 
        lower_factors = []
        upper_factors = []
        
        for i in range(layer_df.shape[1]): 
            lower_bound = utils.look_up_with_bounds(layer_df.loc["limit"].iloc[i], "Limit Low", "Limit High", "Limit Low", bounds_df)
            lower_factor = utils.look_up(lower_bound, "Limit Low", "Factor", bounds_df)
            upper_bound = utils.look_up_with_bounds(layer_df.loc["limit"].iloc[i], "Limit Low", "Limit High", "Limit High", bounds_df)
            upper_factor = utils.look_up(upper_bound, "Limit Low", "Factor", bounds_df)
            lower_bounds.append(lower_bound) 
            upper_bounds.append(upper_bound)
            lower_factors.append(lower_factor)
            upper_factors.append(upper_factor) 

        return pd.DataFrame(lower_bounds).T, pd.DataFrame(upper_bounds).T, pd.DataFrame(lower_factors).T, pd.DataFrame(upper_factors).T

    limit_low , limit_high, factor_low, factor_high = epl_limit_find_bounds(layer_mmp_epl, df_mmp_epl_ilf)

    # Ratio in Band
    limit_ratio_in_band = (layer_mmp_epl.loc["limit"] - limit_low)/(limit_high - limit_low)

    # Limit Factor
    mmp_epl_limit_factor = limit_ratio_in_band * factor_high + (1 - limit_ratio_in_band) * factor_low

    # Subjective Modifiers
    risk_chars = 1

    financial_stability = 1.03

    loss_prevention = 1

    employment_policies = 1

    # Objective Modifiers
    stock_option_exp = 1

    # Total Modifier
    mmp_epl_total_mod = risk_chars * financial_stability * loss_prevention * employment_policies * stock_option_exp

    # Deductible Factor Calcs

    # Create the dataframe of the bounds and relativities
    df_mmp_epl_guide_deduc = pd.DataFrame(hx.params.tbl_mmp_epl_guide_deductible)
    df_mmp_epl_deduc_mod = pd.DataFrame(hx.params.tbl_mmp_epl_deductible_mod)

    # Guideline Deductible
    guide_deduc_factor = utils.look_up_with_bounds(ftes, "# of Employees Low", "# of Employees High", "Percentage", df_mmp_epl_guide_deduc)

    mmp_epl_guideline_deduc = guide_deduc_factor * layer_mmp_epl.loc["limit"]

    # Minimum Deductible
    mmp_epl_min_deduc = utils.look_up_with_bounds(ftes, "# of Employees Low", "# of Employees High", "Min", df_mmp_epl_guide_deduc)

    # Ratio to Guideline
    ratio_to_guideline = np.minimum(3, layer_mmp_epl.loc["deductible"] / mmp_epl_guideline_deduc)

    # Deductible Factors at Bounds
     
    mmp_epl_deductible_factors = []

    for i in range(layer_mmp_epl.shape[1]):
        if ratio_to_guideline.iloc[i] != 3:
            ratio_low = utils.look_up_with_bounds(ratio_to_guideline.iloc[i], "Ratio Low", "Ratio High", "Ratio Low", df_mmp_epl_deduc_mod)
            ratio_high = utils.look_up_with_bounds(ratio_to_guideline.iloc[i], "Ratio Low", "Ratio High", "Ratio High", df_mmp_epl_deduc_mod)
        else:
            ratio_low = 3
            ratio_high = 3
        
        factor_low = utils.look_up(ratio_low, "Ratio Low", "Modifier", df_mmp_epl_deduc_mod)
        factor_high = utils.look_up(ratio_high, "Ratio Low", "Modifier", df_mmp_epl_deduc_mod)

        if ratio_low == 3:
            deduc_ratio_in_band = 1
        else:
            deduc_ratio_in_band = (ratio_to_guideline.iloc[i] - ratio_low) / (ratio_high - ratio_low)

        # Deductible Factor
        if ratio_to_guideline.iloc[i] < 0.1:
            mmp_epl_deduc_factor = 1.4
        else:
            mmp_epl_deduc_factor = deduc_ratio_in_band * factor_high + (1 - deduc_ratio_in_band) * factor_low

        mmp_epl_deductible_factors.append(mmp_epl_deduc_factor)
        
    # Gross Expected Loss in USD
    mmp_epl_gross_el_usd = mmp_epl_assumed_lr * mmp_epl_base_rate * mmp_epl_country_factor * mmp_epl_industry_factor * mmp_epl_limit_factor * mmp_epl_total_mod * mmp_epl_deductible_factors

    # Gross Expected Loss in Source Currency and Term Adjustment
    mmp_epl_gross_el = mmp_epl_gross_el_usd * fx_rate * term_adj_factor

    mmp_epl_gross_el = mmp_epl_gross_el.fillna(0)

    # Converting this to Gross Technical Premium and assigning to the view (The selected choice is subject to written line whereas options are given as 100%)
    epl_brokerage = mmp.epl.brokerage or 0

    mmp_epl_written_line = 1 if mmp.epl.written_line is None else mmp.epl.written_line

    mmp.epl.technical_premium = utils.ratio(utils.calc_net_tech_premium(mmp_epl_gross_el.iloc[0, 0] * mmp_epl_written_line, hxd) , (1 - epl_brokerage), 0) if hxd.cds.mmp.epl.limit else 0

    for i in range(1, layer_mmp_epl.shape[1]):
        mmp_epl_obj = getattr(hxd.cds.mmp.epl, f"option_{i}")

        if getattr(mmp_epl_obj, "aggregate_limit"):
            value = utils.ratio(
                utils.calc_net_tech_premium(
                    mmp_epl_gross_el.iloc[0, i],
                    hxd
                ),
                (1 - epl_brokerage),
                0
            )
        else:
            value = 0

        setattr(mmp_epl_obj, "technical_premium", value)

    # Gross Benchmark Premium (Subject to written line)
    mmp.epl.benchmark_premium = utils.ratio((mmp_epl_gross_el.iloc[0, 0] * mmp_epl_written_line) / 0.7, (1 - epl_brokerage), 0) if hxd.cds.mmp.epl.limit else 0


    # 3. CLL: This also uses a similar methodology to MMP D&O with some slight differences 

    # Getting CLL Layer Information
    layer_mmp_cll = get_mmp_layers("cll", hxd)

    # The ratio of the power ILF between D&O and CLL coverages is required for expected loss calcs
    mmp_cll_power_ilf = df_func.calc_layer_power_ilf(layer_mmp_cll.loc["limit"], layer_mmp_cll.loc["excess"], layer_mmp_cll.loc["deductible"], alpha)

    mmp_dno_power_ilf = df_func.calc_layer_power_ilf(layer_mmp_dno.loc["limit"], layer_mmp_dno.loc["excess"], layer_mmp_dno.loc["deductible"], alpha)

    # Percentage of D&O
    perc_dno = 0.1

    # Gross Expected Loss (Source currency and term adjustment) (The np.where() statement used to work but now doesn't for some reason, so adding an infinitesimal positive float)
    if sic is not None:
        mmp_cll_gross_el = np.array(df_mmp_total_expected_loss.loc["total"]) * np.where(mmp_dno_power_ilf != 0, (mmp_cll_power_ilf + np.finfo(float).eps) / (mmp_dno_power_ilf + np.finfo(float).eps), 1) * np.float64(perc_dno)
    else:
        mmp_cll_gross_el = np.zeros(layer_mmp_cll.shape[1])

    # CLL Minimum Premium
    mmp_cll_min_premium = utils.look_up_with_bounds(mmp.cll.limit, "Sublimit Lower Bound", "Sublimit Higher Bound", "Min Premium", hx.params.tbl_mmp_cll_min_prem) if hxd.cds.mmp.cll.limit else 0

    # Converting Gross Expected Loss to Technical Premium Subject to Minimum Premium and written line
    cll_brokerage = mmp.cll.brokerage or 0

    mmp_cll_written_line = 1 if mmp.cll.written_line is None else mmp.cll.written_line

    mmp.cll.technical_premium = np.maximum(utils.ratio(utils.calc_net_tech_premium(mmp_cll_gross_el[0] * mmp_cll_written_line, hxd), (1 - cll_brokerage), 0), mmp_cll_min_premium * term_adj_factor) if hxd.cds.mmp.cll.limit else 0

    for i in range(1, layer_mmp_cll.shape[1]):
        mmp_cll_obj = getattr(hxd.cds.mmp.cll, f"option_{i}")

        if getattr(mmp_cll_obj, "aggregate_limit"):
            value = np.maximum(
                utils.ratio(
                    utils.calc_net_tech_premium(mmp_cll_gross_el[i], hxd),
                    (1 - cll_brokerage),
                    0
                ),
                mmp_cll_min_premium * term_adj_factor
            )
        else:
            value = 0

        setattr(mmp_cll_obj, "technical_premium", value)

    # Gross Benchmark Premium (Subject to written line)
    mmp.cll.benchmark_premium = np.maximum(utils.ratio((mmp_cll_gross_el[0] * mmp_cll_written_line) / 0.7, (1 - cll_brokerage), 0), mmp_cll_min_premium * term_adj_factor) if hxd.cds.mmp.cll.limit else 0

    # MMP Total Expected Loss
    mmp.total.expected_loss_cost = df_mmp_total_expected_loss.loc["total"].iloc[0] + mmp_epl_gross_el.iloc[0, 0] + mmp_cll_gross_el[0]
