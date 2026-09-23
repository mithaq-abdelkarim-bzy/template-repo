import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
import algorithms.dataframe_functions as df_func
import algorithms.freq_sev_functions as freq_sev_func
from algorithms import parameter_tables_schema as params
from operator import itemgetter
from scipy.stats import gamma, poisson, lognorm, norm
import re as re
import datetime as date
import calendar as ca


###########################################
########## Step 1: ADR Standalone #########
###########################################


def adr_standalone_expected_loss(hxd, layer_df, prelim_inputs):

    # ADR Expected Loss Ratio
    adr_elr = 0.6

    # Process Frequency Variables
    adr_variables = freq_sev_func.process_freq(hxd, "ADR Standalone", prelim_inputs)

    # Process Severity Variables
    adr_variables = freq_sev_func.process_sev(adr_variables)
    
    # Calculate Model and Primary Expected Average Losses (Unity and Model have the same average loss dataframes)
    adr_model_avg_loss, adr_primary_avg_loss = df_func.calc_layer_avg_loss(adr_variables, layer_df)

    # Calcualte Model, Primary and Unity Net Expected Losses
    adr_model_net_exp_loss, _, adr_unity_net_exp_loss, _ = df_func.calc_layer_net_exp_loss(adr_model_avg_loss, adr_variables, layer_df)

    _, adr_primary_net_exp_loss, _, adr_primary_unity_net_exp_loss = df_func.calc_layer_net_exp_loss(adr_primary_avg_loss, adr_variables, layer_df)

    # Total ADR Model Expected Loss
    adr_model_exp_loss = np.array(adr_model_net_exp_loss.loc["Net Expected Loss"] / (1 - np.float64(layer_df.loc["brokerage"])) / adr_elr)

    # Total ADR Primary Expected Loss
    adr_primary_exp_loss = np.array(adr_primary_net_exp_loss.loc["Net Expected Loss"] / (1 - np.float64(layer_df.loc["brokerage"])) / adr_elr)
    adr_primary_unity_exp_loss = np.array(adr_primary_unity_net_exp_loss.loc["Net Expected Loss"] / (1 - np.float64(layer_df.loc["brokerage"])) / adr_elr)

    # Total ADR Unity Expected Loss
    adr_unity_exp_loss = np.array(adr_unity_net_exp_loss.loc["Net Expected Loss"] / (1 - np.float64(layer_df.loc["brokerage"])) / adr_elr)

    # Market Price Factor
    market_price_factor = np.array((prelim_inputs["interpolated_ilf"] ** ((layer_df.loc["limit"] + layer_df.loc["excess"]) / layer_df.loc["excess_limit"]) - prelim_inputs["interpolated_ilf"] ** (layer_df.loc["excess"] / layer_df.loc["excess_limit"])) / (prelim_inputs["interpolated_ilf"] - 1))

    # Creating two dataframes for the model and unity ADR Standalone expected loss calcs
    adr_model_expected_loss = pd.DataFrame(columns=[str(i) for i in range(layer_df.shape[1])])
    adr_unity_expected_loss = pd.DataFrame(columns=[str(i) for i in range(layer_df.shape[1])])

    for i in ("model", "unity"):

        if i == "model":
            df = adr_model_expected_loss
            string = ""
        else:
            df = adr_unity_expected_loss
            string = "_unity"

        # Intermediary Result
        adr_result = np.maximum(eval(f"adr_primary{string}_exp_loss") * market_price_factor, eval(f"adr_{i}_exp_loss"))

        # Adjusted Expected Loss Ratio
        adr_adj_elr = np.array(adr_elr * utils.ratio(eval(f"adr_{i}_exp_loss"), adr_result, 1), dtype = np.float64)

        # Additional Catch for Intermediary Result
        adr_result_with_catch = np.where(prelim_inputs["adr_share"] * prelim_inputs["market_cap_adjusted_usd"] < 1.5e6, 0, adr_result)

        # ADR Standalone Total Expected Loss
        df.loc["adr_expected_loss"] = adr_result_with_catch * (1 - np.float64(layer_df.loc["brokerage"])) * adr_adj_elr

        # Need to calculate expected LRs, this is used to calculate the model premium
        min_elr = np.full_like(adr_adj_elr, utils.look_up("MinELR_International", "ParameterName", "Value", hx.params.tbl_intl_mod))

        max_elr = np.full_like(adr_adj_elr, utils.look_up("MaxELR_ABC", "ParameterName", "Value", hx.params.tbl_pricing_mod))

        # ADR Expected Loss Ratio
        df.loc["adr_expected_lr"] = np.median(np.vstack([min_elr, adr_adj_elr, max_elr]), axis = 0)

    return adr_model_expected_loss, adr_unity_expected_loss


###########################################
############ Step 2: Contagion ############
########################################### 


def contagion_expected_loss(hxd, layer_df, adr_model_expected_loss, adr_unity_expected_loss, prelim_inputs):

    # Contagion Expected Loss Ratio
    cont_elr = 0.6

    # Process Frequency Variables
    cont_variables = freq_sev_func.process_freq(hxd, "Contagion", prelim_inputs)

    # Process Severity Variables
    cont_variables = freq_sev_func.process_sev(cont_variables)
    
    # Calculate Model and Primary Expected Average Losses (Unity and Model have the same average loss dataframes)
    cont_model_avg_loss, cont_primary_avg_loss = df_func.calc_layer_avg_loss(cont_variables, layer_df)

    # Calcualte Model, Primary and Unity Net Expected Losses
    cont_model_net_exp_loss, _, cont_unity_net_exp_loss, _ = df_func.calc_layer_net_exp_loss(cont_model_avg_loss, cont_variables, layer_df)

    _, cont_primary_net_exp_loss, _, cont_primary_unity_net_exp_loss = df_func.calc_layer_net_exp_loss(cont_primary_avg_loss, cont_variables, layer_df)

    # Total Contagion Model Expected Loss
    cont_model_exp_loss = np.array(cont_model_net_exp_loss.loc["Net Expected Loss"] / (1 - np.float64(layer_df.loc["brokerage"])) / cont_elr)

    # Total Contagion Primary Expected Loss
    cont_primary_exp_loss = np.array(cont_primary_net_exp_loss.loc["Net Expected Loss"] / (1 - np.float64(layer_df.loc["brokerage"])) / cont_elr)
    cont_primary_unity_exp_loss = np.array(cont_primary_unity_net_exp_loss.loc["Net Expected Loss"] / (1 - np.float64(layer_df.loc["brokerage"])) / cont_elr)

    # Total Contagion Unity Expected Loss
    cont_unity_exp_loss = np.array(cont_unity_net_exp_loss.loc["Net Expected Loss"] / (1 - np.float64(layer_df.loc["brokerage"])) / cont_elr)

    # Market Price Factor
    market_price_factor = np.array((prelim_inputs["interpolated_ilf"] ** ((layer_df.loc["limit"] + layer_df.loc["excess"]) / layer_df.loc["excess_limit"]) - prelim_inputs["interpolated_ilf"] ** (layer_df.loc["excess"] / layer_df.loc["excess_limit"])) / (prelim_inputs["interpolated_ilf"] - 1))

    # Creating two dataframes for the model and unity ADR Standalone expected loss calcs
    cont_model_expected_loss = pd.DataFrame(columns=[str(i) for i in range(layer_df.shape[1])])
    cont_unity_expected_loss = pd.DataFrame(columns=[str(i) for i in range(layer_df.shape[1])])

    for i in ("model", "unity"):

        if i == "model":
            df = cont_model_expected_loss
            string = ""
        else:
            df = cont_unity_expected_loss
            string = "_unity"

        # Intermediary Result
        cont_result = np.maximum(eval(f"cont_primary{string}_exp_loss") * market_price_factor, eval(f"cont_{i}_exp_loss"))

        # Adjusted Expected Loss Ratio
        cont_adj_elr = np.array(cont_elr * utils.ratio(eval(f"cont_{i}_exp_loss"), cont_result, 1), dtype=np.float64)

        # Additional Catch for Intermediary Result
        cont_result_with_catch = np.where(prelim_inputs["adr_share"] * prelim_inputs["market_cap_adjusted_usd"] < 1.5e6, 0, cont_result)

        # Contagion Total Expected Loss
        cont_freq = utils.look_up("ContagionFrequency", "ParameterName", "Value", hx.params.tbl_intl_mod)
        df.loc["cont_expected_loss"] = np.maximum(0, np.array(cont_result_with_catch, dtype = np.float64) * (1 - np.float64(layer_df.loc["brokerage"])) * cont_adj_elr - eval(f"adr_{i}_expected_loss.loc['adr_expected_loss']")) * cont_freq

        # Need to calculate expected LRs, this is used to calculate the model premium
        min_elr = utils.look_up("MinELR_International", "ParameterName", "Value", hx.params.tbl_intl_mod)

        max_elr = utils.look_up("MaxELR_ABC", "ParameterName", "Value", hx.params.tbl_pricing_mod)

        cont_median_array = cont_result_with_catch * (1 - np.float64(layer_df.loc["brokerage"])) - eval(f"adr_{i}_expected_loss.loc['adr_expected_loss']") / eval(f"adr_{i}_expected_loss.loc['adr_expected_lr']")
        cont_median_array = np.where(cont_median_array == 0, np.finfo(float).eps, cont_median_array)
        
        median_values = np.median(np.vstack((cont_adj_elr, min_elr * np.ones(cont_adj_elr.shape), df.loc["cont_expected_loss"] / cont_median_array)), axis=0)
        
        df.loc["cont_expected_lr"] = np.where(df.loc["cont_expected_loss"] == 0, cont_adj_elr, 
        np.where(prelim_inputs["adr_share"] * prelim_inputs["market_cap_adjusted_usd"] < 1.5e6, max_elr,
        np.where(median_values == 0, cont_adj_elr, median_values)))

    return cont_model_expected_loss, cont_unity_expected_loss


###########################################
######### Step 3: Intl Standalone #########
###########################################


def intl_standalone_expected_loss(hxd, layer_df, prelim_inputs):

    # Parameter and assumptions set up for Intl Standalone specific variables

    # International Market Cap variables
    intl_mcap_min = 10000

    intl_mcap_1 = max(intl_mcap_min, prelim_inputs["market_cap_adjusted_usd"] * (1 - prelim_inputs["adr_share"]))

    if prelim_inputs["adr_share"] == 1:
        intl_mcap = prelim_inputs["total_assets"] / prelim_inputs["fx_rate"]
    else:
        intl_mcap = intl_mcap_1

    # Country Factor
    if prelim_inputs["country"] is not None:
        country_factor = utils.look_up(prelim_inputs["country"], "Country", "Factor", hx.params.tbl_intl_countries)
    else:
        country_factor = 1

    # Industry
    if prelim_inputs["sic"] is not None:
        industry = utils.look_up(int(prelim_inputs["sic"].lstrip("0")), "SIC", "InternationalIndustry", hx.params.tbl_sic_freq)
    else:
        industry = None

    # Occupation Factor
    occupation_factor = utils.look_up(industry, "Industry", "Factor", hx.params.tbl_intl_industry, if_not_found = 1)

    # ILF Band
    ilf_band = utils.look_up(prelim_inputs["country"], "Country", "ILFBand", hx.params.tbl_intl_countries)

    # Additional Germany and UK Calcs for power factor
    germany_ilf_band = utils.look_up("GERMANY", "Country", "ILFBand", hx.params.tbl_intl_countries)

    uk_ilf_band = utils.look_up("UNITED KINGDOM", "Country", "ILFBand", hx.params.tbl_intl_countries)

    germany_ilf = utils.look_up(germany_ilf_band, "ILFBand", "PowerFactor", hx.params.tbl_intl_ilf)

    uk_ilf = utils.look_up(uk_ilf_band, "ILFBand", "PowerFactor", hx.params.tbl_intl_ilf)

    ilf_scaling_factor = min(intl_mcap/20e9, 1)

    weighted_power_factor = germany_ilf * ilf_scaling_factor + uk_ilf * (1 - ilf_scaling_factor)

    # Power Factor
    if prelim_inputs["country"] == "GERMANY":
        if prelim_inputs["ownership"] == "Public":
            power_factor = weighted_power_factor
        else:
            power_factor = uk_ilf
    else:
        power_factor = utils.look_up(ilf_band, "ILFBand", "PowerFactor", hx.params.tbl_intl_ilf, if_not_found = 1)

    # IPO Lag Factor
    if prelim_inputs["sic"] is not None:
        sector = utils.look_up(int(prelim_inputs["sic"].lstrip("0")), "SIC", "Sector", hx.params.tbl_sic_freq, if_not_found = "Not Found")
        if sector == 1:
            lag_factor = utils.look_up(prelim_inputs["ipo_lag"], "Lag", "Factor", hx.params.tbl_sca_lag_factor_1, if_not_found = "Not Found")
        else:
            lag_factor = utils.look_up(prelim_inputs["ipo_lag"], "Lag", "Factor", hx.params.tbl_sca_lag_factor_0, if_not_found = "Not Found")
    else:
        lag_factor = 1
        
    # More Additional Factors
    if prelim_inputs["adr_share"] == 1 or prelim_inputs["ownership"] == "Private":
        private_company_factor = utils.look_up("PrivateCompanyFactor", "ParameterName", "Value", hx.params.tbl_intl_mod, if_not_found = "Not Found")
    else:
        private_company_factor = 1

    uw_min_adj = utils.look_up("UWAdjMin", "ParameterName", "Value", hx.params.tbl_intl_mod, if_not_found = "Not Found")

    max_elr_intl = utils.look_up("MaxELR_International", "ParameterName", "Value", hx.params.tbl_intl_mod, if_not_found = "Not Found")

    # Base Premium Table Lookups

    df_intl_base_prems = pd.DataFrame(hx.params.tbl_intl_base_premium)

    # Market Cap Bounds
    if intl_mcap > 0:
        mcap_bounds = df_intl_base_prems[(df_intl_base_prems["Mcap_Lo"] <= intl_mcap) & (df_intl_base_prems["Mcap_Hi"] > intl_mcap)]

        mcap_lo = mcap_bounds["Mcap_Lo"].values[0]
        mcap_hi = mcap_bounds["Mcap_Hi"].values[0]

        # Costs Bounds
        cost_bounds = df_intl_base_prems[(df_intl_base_prems["Cost_Lo"] <= intl_mcap) & (df_intl_base_prems["Cost_Hi"] > intl_mcap)]

        cost_lo = mcap_bounds["Cost_Lo"].values[0]
        cost_hi = mcap_bounds["Cost_Hi"].values[0]
    else: 
        mcap_lo = df_intl_base_prems["Mcap_Lo"].iloc[0]
        mcap_hi = df_intl_base_prems["Mcap_Hi"].iloc[0]

        cost_lo = df_intl_base_prems["Cost_Lo"].iloc[0]
        cost_hi = df_intl_base_prems["Cost_Hi"].iloc[0]

    # Even more preliminary factors
    if power_factor is not None:
        alpha = math.log(float(power_factor))/math.log(2)
    else:
        alpha = 0

    df_sca_defense_cost = pd.DataFrame(hx.params.tbl_sca_defense_cost_dismissal)
        
    mcap_row_for_match_value = df_sca_defense_cost[df_sca_defense_cost["MarketCap_Lo"] < prelim_inputs["market_cap_adjusted_usd"]]["Index"].max()

    z = mcap_row_for_match_value + utils.ratio(math.log(utils.ratio(intl_mcap + np.finfo(float).eps, mcap_lo, 1)), math.log(utils.ratio(mcap_hi, mcap_lo, 1)), 0)

    n = np.floor(z)

    # Creating two dataframes for the model and unity Intl Standalone expected loss calcs
    intl_model_expected_loss = pd.DataFrame(columns=[str(i) for i in range(layer_df.shape[1])])
    intl_unity_expected_loss = pd.DataFrame(columns=[str(i) for i in range(layer_df.shape[1])])

    for i in ("model", "unity"):

        if i == "model":
            df = intl_model_expected_loss
        else:
            df = intl_unity_expected_loss

        # Coverage Factor
        cover_factor = utils.look_up("ABC", "CoverageType", "Factor", hx.params.tbl_intl_cover_type)
        
        # Base expected loss row
        base_expected_loss = cost_lo + (z - n) * (cost_hi - cost_lo)

        # SCA adjustment row
        if i == "model":
            if hxd.cds.modifiers.sca_adj_factors.value is not None:
                sca_adjustment = max(uw_min_adj, 1 + hxd.cds.modifiers.sca_adj_factors.value)
            else:
                sca_adjustment = max(uw_min_adj, 1)
        else:
            sca_adjustment = 1

        # Calculating the Power ILF
        power_ilf = np.array(df_func.calc_layer_power_ilf(layer_df.loc["limit"], layer_df.loc["excess"], layer_df.loc["deductible"], alpha))

        # Net expected loss row 
        net_expected_loss = (
            base_expected_loss * 
            power_ilf * 
            np.float64(sca_adjustment) *
            np.float64(country_factor) * 
            np.float64(cover_factor) * 
            np.float64(occupation_factor) * 
            np.float64(private_company_factor) * 
            np.float64(lag_factor)
            )

        if ((intl_mcap*(1 - prelim_inputs["adr_share"]) < intl_mcap_min and prelim_inputs["adr_share"] < 1) or 
        (prelim_inputs["total_assets"] / prelim_inputs["fx_rate"] < intl_mcap_min and prelim_inputs["adr_share"] == 1)):
            df.loc["intl_expected_loss"] = 0
        else:
            df.loc["intl_expected_loss"] = net_expected_loss * np.float64(prelim_inputs["high_risk_segment_loading"])

        # Intl Standalone Expected LR
        df.loc["intl_expected_lr"] = intl_expected_lr = np.full(layer_df.shape[1], utils.look_up("MaxELR_International", "ParameterName", "Value", hx.params.tbl_intl_mod))

    return intl_model_expected_loss, intl_unity_expected_loss, alpha


###########################################
########## Step 4: Large Company ##########
###########################################


def intl_large_company_expected_loss(hxd, layer_df, prelim_inputs):

    # Large Company Expected Loss Ratio
    lc_elr = 0.6

    # Process Frequency Variables
    lc_variables = freq_sev_func.process_freq(hxd, "Large Company", prelim_inputs)

    # Process Severity Variables
    lc_variables = freq_sev_func.process_sev(lc_variables)

    # Calculate Model Expected Average Losses (Unity and Model have the same average loss dataframes)
    lc_model_avg_loss, _ = df_func.calc_layer_avg_loss(lc_variables, layer_df)

    # Calcualte Model, and Unity Net Expected Losses
    lc_model_net_exp_loss, _, lc_unity_net_exp_loss, _ = df_func.calc_layer_net_exp_loss(lc_model_avg_loss, lc_variables, layer_df)

    # Total Large Company Model Expected Loss
    lc_model_exp_loss = np.array(lc_model_net_exp_loss.loc["Net Expected Loss"] / (1 - np.float64(layer_df.loc["brokerage"])) / lc_elr)

    # Creating two dataframes for the model and unity Intl Standalone expected loss calcs
    lc_model_expected_loss = pd.DataFrame(columns=[str(i) for i in range(layer_df.shape[1])])
    lc_unity_expected_loss = pd.DataFrame(columns=[str(i) for i in range(layer_df.shape[1])])

    uw_min_adj = utils.look_up("UWAdjMin", "ParameterName", "Value", hx.params.tbl_intl_mod, if_not_found = "Not Found")

    for i in ("model", "unity"):

        if i == "model":
            df = lc_model_expected_loss
        else:
            df = lc_unity_expected_loss

        # SCA Factor
        if i == "model":
            lc_sca_factor = max(1 - (prelim_inputs["mod_sca"] + uw_min_adj), 1)
        else:
            lc_sca_factor = 1

        # Private Company Loading
        if prelim_inputs["ownership"] == "Private":
            private_load = utils.look_up("PrivateLargeFactor", "ParameterName", "Value", hx.params.tbl_intl_mod)
        else:
            private_load = 1

        # ADR Level 1 Adjustment
        if prelim_inputs["ownership"] == "Private" or prelim_inputs["adr_flag"] == "NA" or prelim_inputs["adr_level"] == "Level 1":
            level_1_adj = 0.3
        else:
            level_1_adj = 0

        # Large Company Total Expected Loss
        df.loc["lc_expected_loss"] = np.where(lc_variables["mcap"] < 1.5e6, 0, eval(f"lc_{i}_net_exp_loss.loc['Net Expected Loss']") * np.float64(lc_sca_factor) * np.float64(private_load) * (1 - np.float64(level_1_adj)) * np.float64(prelim_inputs["high_risk_segment_loading"]))

        # International Large Company Loss Ratio
        df.loc["lc_expected_lr"] = np.full(layer_df.shape[1], utils.look_up("MaxELR_International", "ParameterName", "Value", hx.params.tbl_intl_mod))

    return lc_model_expected_loss, lc_unity_expected_loss
