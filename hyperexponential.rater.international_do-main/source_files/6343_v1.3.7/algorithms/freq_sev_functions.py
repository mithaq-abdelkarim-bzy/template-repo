import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
from operator import itemgetter
from scipy.stats import gamma, poisson, lognorm, norm
import re as re
import datetime as date
import calendar as ca


###########################################
########## UW Adjustment Function #########
############### Side A/ABC ################
###########################################


def process_uw_mods(hxd, prelim_inputs, is_side_a):

    mod = hxd.cds.modifiers
    if is_side_a is False:
        # SCA Modifier
        prelim_inputs["mod_sca"] = mod.sca_adj_factors.value or 0

        # Regulatory Modifier
        prelim_inputs["mod_reg"] = mod.regulatory_factors.value or 0

        # Mergers and Acquisitions Modifier
        prelim_inputs["mod_ma"] = mod.mergers_and_acquisitions_factors.value or 0

        # ESG Modifier
        prelim_inputs["mod_esg"] = mod.esg_factors.value or 0

        # Territory of Operation Modifier
        prelim_inputs["mod_territory"] = mod.territory_of_operation_factors.value or 0

        # SCA Override Modifier
        prelim_inputs["mod_sca_override"] = mod.sca_freq_adj_factor or 0
    else:
        # SCA Modifier
        prelim_inputs["mod_sca"] = mod.sca_adj_factors_side_a.value or 0

        # Regulatory Modifier
        prelim_inputs["mod_reg"] = mod.financial_stability_side_a_factors.value or 0

        # Mergers and Acquisitions Modifier
        prelim_inputs["mod_ma"] = mod.indemnification_side_a_factors.value or 0

        # ESG Modifier
        prelim_inputs["mod_esg"] = mod.esg_factors_side_a.value or 0

        # Territory of Operation Modifier
        prelim_inputs["mod_territory"] = 0

        # SCA Override Modifier
        prelim_inputs["mod_sca_override"] = mod.sca_freq_adj_factor or 0

    return prelim_inputs


###########################################
######## Frequency Function Inputs ########
###########################################        


def freq_function_variables(coverage, prelim_inputs, is_side_a = False):
    
    # Creating empty data dictionary to be populated
    variables = {}

    # Market Cap Lower Limit
    if is_side_a == False or coverage == "Large Company":
        mcap_lower_limit = 1500000
    else:
        mcap_lower_limit = 10000


    # Upper Cap
    upper_cap = 375000000

    # Intl Market Cap (Used for Contagion Frequency Function)
    if prelim_inputs["adr_share"] == 0:
        imcap_1 = prelim_inputs["market_cap_adjusted_usd"]
    else:
        imcap_1 = prelim_inputs["market_cap_adjusted_usd"] * 0.5 * (0.5 ** prelim_inputs["adr_share"])

    imcap_2 = max(prelim_inputs["market_cap_adjusted_usd"] * (1 - prelim_inputs["adr_share"]) / 100, mcap_lower_limit)

    # Large Company Factors
    large_company_power_factor = utils.look_up("LargeCompanyRecognitionPower", "ParameterName", "Value", hx.params.tbl_intl_mod, if_not_found = "Not Found")

    large_company_size_factor = utils.look_up("LargeComanySize", "ParameterName", "Value", hx.params.tbl_intl_mod, if_not_found = "Not Found")

    x_a = (large_company_power_factor - 1) / (large_company_power_factor * (large_company_size_factor ** large_company_power_factor))

    # Intl Market Cap Calc
    if prelim_inputs["adr_level"] in ("Level 2", "Level 3", "Full Listing"):
        imcap = imcap_2
    else:
        imcap = imcap_1 * (1 - np.exp(-x_a * (imcap_1 ** large_company_power_factor)))

    # Market Cap
    if coverage in ("ADR Standalone", "Contagion"):
        variables["mcap"] = max(prelim_inputs["revised_adr_market_cap"], mcap_lower_limit)
    else:
        variables["mcap"] = imcap

        
    # f5adj Factor
    if prelim_inputs["sic"] is not None:
        f5adj = utils.look_up(int(prelim_inputs["sic"].lstrip("0")), "SIC", "f5Adj", hx.params.tbl_sic_freq, if_not_found = "Not Found")
    else:
        f5adj = 0

    # Frequency Group
    if prelim_inputs["sector"] is not None:
        freq_group = utils.look_up(prelim_inputs["sector"], "Sector", "FrequencyGroup", hx.params.tbl_sca_freq_group, if_not_found = "Not Found")
    else:
        freq_group = None

    # Capped Market Cap
    if freq_group is not None:
        freq_group_mcap = utils.look_up(f"MCapMin{freq_group}", "ParameterName", "Value", hx.params.tbl_sca_freq_mod, if_not_found = 0)
        capped_mcap = min(variables["mcap"], freq_group_mcap)
    else:
        capped_mcap = variables["mcap"]

    # Frequency A
    if freq_group is not None:
        freq_a = utils.look_up(f"Freq{freq_group}a", "ParameterName", "Value", hx.params.tbl_sca_freq_mod, if_not_found = "Not Found")
    else:
        freq_a = None

    # Frequency B
    if freq_group is not None:
        freq_b = utils.look_up(f"Freq{freq_group}b", "ParameterName", "Value", hx.params.tbl_sca_freq_mod, if_not_found = "Not Found")
    else:
        freq_b = None

    # Minimum Band 5 Trigger
    min_band_5_trigger = utils.look_up("MinBand5Trigger", "ParameterName", "Value", hx.params.tbl_sca_freq_mod, if_not_found = "Not Found")

    # Frequency Min
    if f5adj < min_band_5_trigger:
        f_min = f5adj
    else:
        f_min = min_band_5_trigger

    # Jobs Act
    jobs_act = utils.look_up("JobsAct", "ParameterName", "Value", hx.params.tbl_sca_freq_mod, if_not_found = "Not Found")

    # Jobs Act 1 
    jobs_act_1 = utils.look_up("JobsAct_Sector1", "ParameterName", "Value", hx.params.tbl_sca_freq_mod, if_not_found = "Not Found")

    # SCA Sector Frequency A
    if freq_a and freq_b and capped_mcap and upper_cap is not None:
        sca_sector_freq = max(f5adj * ((1 - math.exp(-freq_a * (math.log(capped_mcap) - freq_b) ** 2)) / (1 - math.exp(-freq_a * (math.log(upper_cap) - freq_b) ** 2))), f_min)
    else:
        sca_sector_freq = 0

    # SCA Sector Frequency Factor Calcs
    # IPO Lag
    if prelim_inputs["ipo_ignore"] == 1:
        lag = 5
    else:
        lag = max(0, min(prelim_inputs["ipo_lag"], 5))

    # Factor A
    if prelim_inputs["sector"] == 1:
        factor_a = utils.look_up(lag, "Lag", "Factor", hx.params.tbl_sca_lag_factor_1)
    else:
        factor_a = utils.look_up(lag, "Lag", "Factor", hx.params.tbl_sca_lag_factor_0)

    if prelim_inputs["mod_sca_override"] == 0:
        variables["sca_sector_freq_factor"] = sca_sector_freq * factor_a
    else:
        variables["sca_sector_freq_factor"] = sca_sector_freq * factor_a * (prelim_inputs["mod_sca_override"] + 1)

    # Interaction Modifiers
    variables["reg_deriv_interaction_mod"] = utils.look_up("RegDerivative", "ParameterName", "Value", hx.params.tbl_interaction_mod)

    variables["sca_deriv_interaction_mod"] = utils.look_up("SCADerivative", "ParameterName", "Value", hx.params.tbl_interaction_mod)

    variables["reg_sca_interaction_mod"] = utils.look_up("RegSCA", "ParameterName", "Value", hx.params.tbl_interaction_mod)

    # SCA Absolute Minimum Rate
    sca_min_rate = utils.look_up("SCAMinAbsoluteRate", "ParameterName", "Value", hx.params.tbl_sca_freq_mod)


    # z and subsequent n calculation, this is used in a few places and is a fairly large formula so will split up the calc with dummy variables a, b, and c
    a = utils.look_up_with_bounds(variables["mcap"], "Mcap_Lo", "MCap_Hi", "index_Hi", hx.params.tbl_mcap_band)

    b = utils.look_up_with_bounds(variables["mcap"], "Mcap_Lo", "MCap_Hi", "Mcap_Lo", hx.params.tbl_mcap_band)

    c = utils.look_up_with_bounds(variables["mcap"], "Mcap_Lo", "MCap_Hi", "MCap_Hi", hx.params.tbl_mcap_band)

    if all(value != 0 for value in [variables["mcap"], a, b, c]):
        z = max(a - 1 + utils.ratio(math.log(variables["mcap"] / b), math.log(c / b), 1), 1)
    else:
        z = 0

    n = math.floor(z)

    # Derivative Factors/Relativities
    deriv_freq_band_relativity_low = utils.look_up(n, "Band_Lo", "Relativity_Lo", hx.params.tbl_deriv_freq_band)

    deriv_freq_band_relativity_high = utils.look_up(n, "Band_Lo", "Relativity_Hi",  hx.params.tbl_deriv_freq_band)

    deriv_scale_factor = utils.look_up("DerivativeScaleFactor", "ParameterName", "Value", hx.params.tbl_deriv_freq_mod)

    # Regulatory Factors/Relativities
    reg_freq_band_relativity_low = utils.look_up(n, "Band", "Relativity_Lo", hx.params.tbl_reg_freq_band)

    reg_freq_band_relativity_high = utils.look_up(n, "Band", "Relativity_Hi",  hx.params.tbl_reg_freq_band)

    reg_scale_factor = utils.look_up("RegScaleFactor", "ParameterName", "Value", hx.params.tbl_reg_freq_mod)

    reg_freq_unit = utils.look_up("RegFreqUnit", "ParameterName", "Value", hx.params.tbl_reg_freq_mod)

    # MA Factors/Relativities
    ma_freq_band_relativity_low = utils.look_up(n, "Band", "Relativity_Lo", hx.params.tbl_ma_freq_band)

    ma_freq_band_relativity_high = utils.look_up(n, "Band", "Relativity_Hi",  hx.params.tbl_ma_freq_band)

    ma_scale_factor = utils.look_up("MAScaleFactor", "ParameterName", "Value", hx.params.tbl_ma_freq_mod)


    # CapIQ Factors
    # Interpolates each of the values against the corresponding tables
    if prelim_inputs["min_trading_volume"] is not None:
        min_trading_volume_factor = utils.interp_table_row(hx.params.tbl_min_trading_volume, prelim_inputs["min_trading_volume"], "Lower", "Upper", "SelectedRelativityLower", "SelectedRelativityUpper", 1)
    else:
        min_trading_volume_factor = 1

    if prelim_inputs["volatility_trading_volume"] is not None:
        volatility_trading_volume_factor = utils.interp_table_row(hx.params.tbl_volatility_trading, prelim_inputs["volatility_trading_volume"], "Lower", "Upper", "SelectedRelativityLower", "SelectedRelativityUpper", 1)
    else:
        volatility_trading_volume_factor = 1

    if prelim_inputs["execs_under_fifty"] is not None:
        execs_under_fifty_factor = utils.interp_table_row(hx.params.tbl_exec_under_50, prelim_inputs["execs_under_fifty"], "Lower", "Upper", "SelectedRelativityLower", "SelectedRelativityUpper", 1)
    else:
        execs_under_fifty_factor = 1

    # Dismissal Rate
    if prelim_inputs["sector"] is not None:
        variables["dismissal_rate"] = utils.look_up(prelim_inputs["sector"], "Sector", "DismissalRate", hx.params.tbl_sca_freq_dismissal)
    else:
        variables["dismissal_rate"] = 0
    

    # Intermediate Calculations for Frequency Adjustment Factors
    # Derivative IR
    deriv_ir = deriv_freq_band_relativity_low + (z - n) * (deriv_freq_band_relativity_high - deriv_freq_band_relativity_low)

    # Derivative Frequency (Intermediate step - Used for unity frequency)
    variables["deriv_freq_base"] = f5adj * deriv_ir * deriv_scale_factor
    
    # Regulatory IR
    reg_ir = reg_freq_band_relativity_low + (z - n) * (reg_freq_band_relativity_high - reg_freq_band_relativity_low)

    # Regulatory Sector Band 5 Freq
    reg_band_5_freq = utils.look_up(prelim_inputs["sector"], "Sector", "Relativity", hx.params.tbl_reg_freq_sector)
    
    # Regulatory Frequency (Intermediate step - Used for unity frequency)
    variables["reg_freq_base"] = reg_band_5_freq * reg_ir * reg_scale_factor * reg_freq_unit

    # MA IR
    ma_ir = ma_freq_band_relativity_low + (z - n) * (ma_freq_band_relativity_high - ma_freq_band_relativity_low)

    # MA Sector Band 5 Freq
    ma_band_5_freq = utils.look_up(prelim_inputs["sector"], "Sector", "Relativity", hx.params.tbl_ma_freq_sector)

    # MA Frequency (Intermediate step - Used for unity frequency)
    variables["ma_freq_base"] = ma_ir * ma_band_5_freq * ma_scale_factor

    # SCA Frequency Cap
    sca_freq_cap = utils.look_up("SCAFrequencyCap", "ParameterName", "Value", hx.params.tbl_sca_freq_mod)

    # Reg Modifier Scalar (Reg frequencies have been backed out of the algorithm to align with US D&O, UW have requested the Reg UW modifier still impacts pricing, therefore this is a work around)
    reg_mod_scalar = utils.look_up("RegModScalar", "Name", "Value", hx.params.tbl_reg_mod_scalar)

    reg_mod_factor = 1 + max(0.7, (1 + prelim_inputs["mod_reg"]) * (1 + prelim_inputs["mod_esg"])) * reg_mod_scalar

    # Frequency Adjustment Factors
    if coverage in ("ADR Standalone", "Contagion"):
        variables["sca_freq"] = min(max(variables["sca_sector_freq_factor"], sca_min_rate) * (1 + (np.median([min_trading_volume_factor * volatility_trading_volume_factor * execs_under_fifty_factor, 0.5, 1.5]) - 1) / 5) * (1 + max(prelim_inputs["mod_sca"], -0.3)) * reg_mod_factor, sca_freq_cap)
    else:
        variables["sca_freq"] = max(variables["sca_sector_freq_factor"] * (1 + prelim_inputs["mod_sca"]) * reg_mod_factor, sca_min_rate)

    variables["deriv_freq"] = variables["deriv_freq_base"] * (1 + prelim_inputs["mod_territory"])

    variables["reg_freq"] = variables["reg_freq_base"] * (1 + prelim_inputs["mod_reg"]) * (1 + prelim_inputs["mod_esg"])

    variables["ma_freq"] = variables["ma_freq_base"] * (1 + prelim_inputs["mod_ma"])

    # Coverage
    variables["coverage"] = coverage

    # Passing through some of the Preliminary Inputs for Contagion Adjustment Calculation
    variables["sector"] = prelim_inputs["sector"]
    variables["adr_share"] = prelim_inputs["adr_share"]
    variables["market_cap_adjusted_usd"] = prelim_inputs["market_cap_adjusted_usd"]
    variables["mod_sca_override"] = prelim_inputs["mod_sca_override"]
    variables["fx_rate"] = prelim_inputs["fx_rate"]

    return variables

    
###########################################
###### Frequency Function Definition ######
###########################################

# Calculates derivative frequency
# 1) Unity: Derivative base frequency adjusted for market cap and scale factor. Interacts with SCA unity freq 
# 2) Used (or just "freq"): model freq interacted with SCA used freq
def calc_freq_der(variables):

    # Initialising to stop errors with default values
    variables["freq_unity_d"] = 0
    variables["freq_d"] = 0

    if variables["sector"] is not None:
        variables["freq_unity_d"] = max(variables["deriv_freq_base"] - variables["sca_deriv_interaction_mod"] * variables["sca_sector_freq_factor"] / (1 + variables["mod_sca_override"]), 0) 

        if variables["coverage"] == "Large Company":
            variables["freq_d"] = max(variables["deriv_freq"] - variables["sca_deriv_interaction_mod"] * variables["sca_freq"], 0)
        else:
            variables["freq_d"] = max(min(variables["deriv_freq"] - variables["sca_deriv_interaction_mod"] * variables["sca_freq"], utils.look_up("DerivFrequencyCap", "ParameterName", "Value", hx.params.tbl_sca_freq_mod)), 0)
    
    return variables

# Calculates M&A frequency
# 1) Unity: MA base frequency adjusted for market cap and scale factor
# 2) Used (or just "freq"): model freq interacted with MA used freq
def calc_freq_ma(variables):

    # Initialising to stop errors with default values
    variables["freq_unity_ma"] = 0
    variables["freq_ma"] = 0

    if variables["sector"] is not None:
        variables["freq_unity_ma"] = variables["ma_freq_base"]
        variables["freq_ma"] = max(variables["ma_freq"], 0)
        
    return variables

# Calculates the interaction claims types:
# 1) Standalone SCA (s) 
# 2) SCAs that become Derivatives (sd)
def calc_freq_inter(variables):

    # Initialising to stop errors with default values
    variables["freq_unity_s"] = 0
    variables["freq_s"] = 0
    variables["freq_unity_sd"] = 0
    variables["freq_sd"] = 0
    variables["freq_unity_sca"] = 0
    variables["freq_sca"] = 0

    if variables["sector"] is not None:
        variables["freq_unity_s"] = (1 - variables["sca_deriv_interaction_mod"]) * variables["sca_sector_freq_factor"] / (1 + variables["mod_sca_override"])
        variables["freq_s"] = max((1 - variables["sca_deriv_interaction_mod"]) * variables["sca_freq"], 0)

        variables["freq_unity_sd"] = variables["sca_deriv_interaction_mod"] * variables["sca_sector_freq_factor"] / (1 + variables["mod_sca_override"])
        variables["freq_sd"] = max(variables["sca_deriv_interaction_mod"] * variables["sca_freq"], 0)

        # Need to normalise the non-unity frequencies and apply frequency adjustment factors
        variables["freq_s"] = variables["freq_s"] * variables["sca_freq"] / (variables["freq_s"] + variables["freq_sd"])
        variables["freq_sd"] = variables["freq_sd"] * variables["sca_freq"] / (variables["freq_s"] + variables["freq_sd"])

        # Total SCA Sector Frequency
        variables["freq_unity_sca"] = variables["freq_unity_s"] + variables["freq_unity_sd"]
        variables["freq_sca"] = variables["freq_s"] + variables["freq_sd"]

    return variables


###########################################
####### Severity Variables Set Up #########
###########################################


def contagion_adjustment(variables):
    # Contagion Adjustment Calculation
    max_cont_load = utils.look_up("MaxContagionLoad", "ParameterName", "Value", hx.params.tbl_intl_mod)

    intl_cont = utils.look_up("InternationalContagion", "ParameterName", "Value", hx.params.tbl_intl_mod)

    cont_scale_min = utils.look_up("ContagionScaleMin", "ParameterName", "Value", hx.params.tbl_intl_mod)

    cont_scale_max = utils.look_up("ContagionScaleMax", "ParameterName", "Value", hx.params.tbl_intl_mod)

    cont_scale_mc = utils.look_up("ContagionScaleMC", "ParameterName", "Value", hx.params.tbl_intl_mod)

    cont_freq = utils.look_up("ContagionFrequency", "ParameterName", "Value", hx.params.tbl_intl_mod)

    if variables["adr_share"] != 0:
        variables["contagion_adjustment"] = min(max_cont_load, intl_cont * ((1 - variables["adr_share"]) / variables["adr_share"])) * min(cont_scale_max, max(cont_scale_min, math.sqrt(variables["market_cap_adjusted_usd"] * variables["adr_share"] / cont_scale_mc)))
    else:
        variables["contagion_adjustment"] = 0

    return variables

# Calcultes the initial mu for each claim type
def calc_initial_mu(variables):
    sev_a = utils.look_up("a", "ParameterName", "Value", hx.params.tbl_sca_sev_mod, 0)
    sev_b = utils.look_up("b", "ParameterName","Value", hx.params.tbl_sca_sev_mod, 0)
    sev_c = utils.look_up("c", "ParameterName", "Value", hx.params.tbl_sca_sev_mod, 0)

    variables["mu"] = (
        sev_a * pow(np.log(variables["mcap"]), 2) + 
        sev_b * np.log(variables["mcap"]) + 
        sev_c
        )

    if variables["coverage"] == "Contagion":
        variables["mu"] = variables["mu"] + np.log(1 + variables["contagion_adjustment"])

    return variables

# Calcultes the sigma for SCA claims
def calc_sigma_sca(variables):

    mc_1 = utils.look_up("MC1", "ParameterName", "Value", hx.params.tbl_sca_sev_mod, 0)
    mc_2 = utils.look_up("MC2", "ParameterName", "Value", hx.params.tbl_sca_sev_mod, 0)

    if variables["mcap"] < mc_1:
        sd_lookup = "sd_1"
    elif variables["mcap"] < mc_2:
        sd_lookup = "sd_2"
    else: 
        sd_lookup = "sd_3"

    variables["sigma_sca"] = utils.look_up(sd_lookup, "ParameterName", "Value", hx.params.tbl_sca_sev_mod, 0)

    return variables

# Calculates the initial mu for M&A claims
def calc_mu_ma(variables):

    mu_ma_a = utils.look_up("MASE.alpha", "ParameterName", "Value", hx.params.tbl_ma_sev_mod, 0) 
    mu_ma_b = utils.look_up("MASE.beta", "ParameterName", "Value", hx.params.tbl_ma_sev_mod, 0)

    variables["mu_ma"] = mu_ma_a + mu_ma_b  * np.log(variables["mcap"])

    if variables["coverage"] == "Contagion":
        variables["mu_ma"] = variables["mu_ma"] + np.log(1 + variables["contagion_adjustment"])

    return variables

# Calcultes the sigma for M&A claims
def calc_sigma_ma(variables):

    ma_mc = utils.look_up("MASE.MC", "ParameterName", "Value", hx.params.tbl_ma_sev_mod, 0) 
    ma_sd_a = utils.look_up("MASE.sd_a", "ParameterName", "Value", hx.params.tbl_ma_sev_mod, 0) 
    ma_sd_b1 = utils.look_up("MASE.sd_b1", "ParameterName", "Value", hx.params.tbl_ma_sev_mod, 0) 
    ma_sd_b2 = utils.look_up("MASE.sd_b2", "ParameterName", "Value", hx.params.tbl_ma_sev_mod, 0) 

    if variables["mcap"] < ma_mc:
        variables["sigma_ma"] = ma_sd_b1
    else:
        variables["sigma_ma"] = ma_sd_b2 + ma_sd_a * np.log(variables["mcap"])

    return variables

# Calculates the initial mu for Derivative claims
def calc_mu_der(variables):
    
    variables["mu_der"] = utils.look_up("mulog", "ParameterName", "Value", hx.params.tbl_deriv_sev_mod)

    if variables["coverage"] == "Contagion":
        variables["mu_der"] = variables["mu_der"] + np.log(1 + variables["contagion_adjustment"])

    return variables


# Calcultes the sigma for Derivative claims
def calc_sigma_der(variables):
    
    variables["sigma_der"] = utils.look_up("sdlog", "ParameterName", "Value", hx.params.tbl_deriv_sev_mod)

    return variables

# Calculates the defense SCA factor
def calc_defense_sca_factor(variables):

    dc_mean = math.exp(variables["mu"] + 0.5 * pow(variables["sigma_sca"] , 2))

    df_sca_dc = hx.params.tbl_sca_defense_cost

    dc_indemnity_lower = df_sca_dc[df_sca_dc["Indemnity"] < dc_mean]["Indemnity"].max()
    dc_factor = df_sca_dc[df_sca_dc["Indemnity"] < dc_mean]["Factor"].min()

    if dc_mean < 10000000:
        dc_cumf = 0
    else:
        dc_cumf = (df_sca_dc[df_sca_dc["Indemnity"] < dc_mean].iloc[1:, :])["CumF"].min()               

    variables["defense_sca_factor"] = dc_factor * (1 - dc_indemnity_lower / dc_mean) + dc_cumf * (dc_indemnity_lower / dc_mean)

    return variables

# Calculates the defense SCA mu
def calc_defense_sca_dismissed_mu(variables):

    variables["defense_sca_sigma"] = utils.look_up("DefenseDismissalSCA_si", "ParameterName", "Value", hx.params.tbl_sca_sev_mod)

    if variables["coverage"] == "Contagion":
            exp_lookup = variables["market_cap_adjusted_usd"]
    else:
            exp_lookup = variables["mcap"]
    
    if exp_lookup != 0:
        
        df_sca_dismiss = hx.params.tbl_sca_defense_cost_dismissal

        match_row = df_sca_dismiss[df_sca_dismiss["MarketCap_Lo"] < exp_lookup]["Index"].max() + 1

        mcap_low = df_sca_dismiss[df_sca_dismiss["MarketCap_Lo"] < exp_lookup]["MarketCap_Lo"].max()

        mcap_high = df_sca_dismiss[df_sca_dismiss["MarketCap_Lo"] < exp_lookup]["MarketCap_Hi"].max()

        cost_low = df_sca_dismiss[df_sca_dismiss["MarketCap_Lo"] < exp_lookup]["Cost_Lo"].max()

        cost_high = df_sca_dismiss[df_sca_dismiss["MarketCap_Lo"] < exp_lookup]["Cost_Hi"].max()

        z = match_row - 1 + np.log(exp_lookup / mcap_low) / np.log(mcap_high / mcap_low)

        if not np.isnan(z):
            n = np.floor(z)
        else:
            n = 0

        dc_dismiss_mean = cost_low + (z - n) * (cost_high - cost_low)

        variables["defense_sca_mu"] = np.log(dc_dismiss_mean) - 0.5 * (variables["defense_sca_sigma"] ** 2)
    else:
        variables["defense_sca_mu"] = 0

    return variables


###########################################
######### Overarching Functions ###########
###### Gets all Freq/Sev Variables ########
###########################################


def process_freq(hxd, coverage, prelim_inputs, is_side_a = False):

    # 0. Get UW Modifiers
    variables = process_uw_mods(hxd, prelim_inputs, is_side_a)

    # 1. Get Prerequisite Variables
    variables = freq_function_variables(coverage, prelim_inputs, is_side_a)

    # 2. Derivative Frequency
    variables = calc_freq_der(variables)

    # 3. M&A Frequency
    variables = calc_freq_ma(variables)

    # 4. SCA and Interaction Frequencies
    variables = calc_freq_inter(variables)

    # 5. Side A Preliminary Factors
    variables = calc_side_a_factors(hxd, variables)

    # 6. Side A Frequencies
    variables = calc_side_a_freq(variables)

    return variables

def process_sev(variables):

    # 1. Contagion Adjustment Factor
    variables = contagion_adjustment(variables)

    # 2. Initial SCA Mu
    variables = calc_initial_mu(variables)

    # 3. SCA Sigma
    variables = calc_sigma_sca(variables)

    # 4. M&A Mu
    variables = calc_mu_ma(variables)

    # 5. M&A Sigma
    variables = calc_sigma_ma(variables)

    # 6. Derivative Mu
    variables = calc_mu_der(variables)

    # 7. Derivative Sigma
    variables = calc_sigma_der(variables)

    # 8. SCA Defense Factor
    variables = calc_defense_sca_factor(variables)

    # 9. SCA Defense Dismissed Mu
    variables = calc_defense_sca_dismissed_mu(variables) 

    return variables


###########################################
############ Side A Functions #############
###########################################


# Calculates all the additional factors that only apply for Side A. Includes:
#   1) Extracts variables for Side A frequencies by layer
#   2) Calculates the average bankruptcy load using the Z-score and Credit Score
def calc_side_a_factors(hxd, variables):
    agg = hxd.cds.exposure.aggregate

    # Defining parameter tables
    df_side_a_mod = hx.params.tbl_side_a_mod
    df_bankruptcy = hx.params.tbl_side_a_bankruptcy

    # Extracts Side A Specific Constants
    variables["state_desc"] = utils.look_up("Canada", "State", "Value", hx.params.tbl_state_indemnification, 0)
    variables["b_no_case"] = utils.look_up("BNoCase", "ParameterName", "Value", df_side_a_mod)
    variables["prob_dic"] = utils.look_up("ProbDIC", "ParameterName", "Value", df_side_a_mod)
    variables["are_dismissed"] = utils.look_up("ArelDismissed", "ParameterName", "Value", df_side_a_mod)
    variables["b_dismissed"] = utils.look_up("BDismissed", "ParameterName", "Value", df_side_a_mod)
    variables["shock_load_freq"] = utils.look_up("ShockLoadFreq", "ParameterName", "Value", hx.params.tbl_deriv_freq_mod)
    

    # The following financials are required
    financials = {
        "ebit": agg.ebit or 0,
        "period": agg.period_data or 0,
        "current_assets": agg.current_assets or 0,
        "current_liabilities": agg.current_liabilities or 0,
        "total_assets": agg.total_assets or 0,
        "total_liabilities": agg.total_liabilities or 0,
        "retained_earnings": agg.retained_earnings or 0,
        "market_cap_adjusted_usd": variables["market_cap_adjusted_usd"] or 0,
        "net_sales": agg.net_sales or 0,
        "fx_rate": variables["fx_rate"]
    }

    variables["z_score"] = calc_z_score(df_side_a_mod, financials)

    # Z bankruptcy score
    variables["z_bankruptcy_score"] = calc_z_bankruptcy_score(df_side_a_mod, variables["z_score"])

    # Average bankruptcy score 
    # This is the average of z bankruptcy score and credit score
    variables["average_bankruptcy_score"] = calc_average_bankruptcy_score(df_bankruptcy, agg.credit_score, variables["z_bankruptcy_score"])

    return variables

# Calculates the Z score from the company financials
def calc_z_score(df, financials):

    z_a = utils.ratio((financials["current_assets"] - financials["current_liabilities"]), financials["total_assets"], 0)
    z_b = utils.ratio(financials["retained_earnings"], financials["total_assets"], 0)
    z_c = utils.ratio(utils.ratio(financials["ebit"], financials["total_assets"], 0) * 12, financials["period"], 0)
    z_d = utils.ratio(financials["market_cap_adjusted_usd"], financials["total_liabilities"] / financials["fx_rate"], 0)
    z_e = utils.ratio(utils.ratio(financials["net_sales"], financials["total_assets"], 0) * 12 ,financials["period"], 0)

    z_wgt_a = utils.look_up("Z_T1", "ParameterName", "Value", df, 0) 
    z_wgt_b = utils.look_up("Z_T2", "ParameterName", "Value", df, 0) 
    z_wgt_c = utils.look_up("Z_T3", "ParameterName", "Value", df, 0) 
    z_wgt_d = utils.look_up("Z_T4", "ParameterName", "Value", df, 0) 
    z_wgt_e = utils.look_up("Z_T5", "ParameterName", "Value", df, 0)

    z_score = (
        z_a * z_wgt_a +
        z_b * z_wgt_b +
        z_c * z_wgt_c +
        z_d * z_wgt_d +
        z_e * z_wgt_e
    )

    return z_score

# Accepts a z score and converts this into a bankruptcy score
def calc_z_bankruptcy_score(df, z_score):
    z_base = utils.look_up("Z_BaseConstant", "ParameterName", "Value", df, 0)
    z_lambda = utils.look_up("Z_BaseLambda", "ParameterName", "Value", df, 0)
    z_max = utils.look_up("Z_Max", "ParameterName", "Value", df, 0)

    if z_score != 0:
        try:
            z_bankruptcy_score = min(z_base * math.exp(z_lambda * z_score), z_max)
        except OverflowError:
            z_bankruptcy_score = 0
    else:
        z_bankruptcy_score = 0

    return z_bankruptcy_score

def calc_average_bankruptcy_score(df, credit_rating, z_bankruptcy_score):
    if credit_rating is not None:
        credit_score = utils.look_up(credit_rating, "Rating", "BankruptcyScore", df, 0)
        bankruptcy_score = (z_bankruptcy_score + credit_score) / 2
    else: bankruptcy_score = z_bankruptcy_score

    return bankruptcy_score

def calc_side_a_freq(variables):

    variables["freq_sector_side_a"] = (1 - variables["b_no_case"]) * variables["average_bankruptcy_score"] + variables["freq_d"] * (1 - variables["state_desc"])

    variables["freq_unity_sector_side_a"] = (1 - variables["b_no_case"]) * variables["average_bankruptcy_score"] + variables["freq_unity_d"] * (1 - variables["state_desc"])

    variables["freq_tag_along_side_a"] = variables["freq_sd"]

    variables["freq_unity_tag_along_side_a"] = variables["freq_unity_sd"]

    variables["freq_dic"] = (variables["freq_s"] + variables["freq_sd"]) * variables["prob_dic"]

    variables["freq_unity_dic"] = (variables["freq_unity_s"] + variables["freq_unity_sd"]) * variables["prob_dic"]

    variables["side_a_dismissal"] = utils.ratio((variables["freq_d"] * (1 - variables["state_desc"]) * 
    variables["are_dismissed"] + variables["average_bankruptcy_score"] * variables["b_dismissed"]), (variables["freq_d"] * 
    (1 - variables["state_desc"]) + variables["average_bankruptcy_score"]))

    variables["side_a_unity_dismissal"] = utils.ratio((variables["freq_unity_d"] * (1 - variables["state_desc"]) * 
    variables["are_dismissed"] + variables["average_bankruptcy_score"] * variables["b_dismissed"]), (variables["freq_unity_d"] * 
    (1 - variables["state_desc"]) + variables["average_bankruptcy_score"]))

    return variables