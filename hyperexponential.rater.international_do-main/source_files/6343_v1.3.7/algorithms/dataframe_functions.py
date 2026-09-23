import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
import algorithms.dataframe_functions as df_func
import algorithms.freq_sev_functions as freq_sev_func
import algorithms.rate_side_abc_expected_loss as side_abc
import algorithms.rate_side_a_expected_loss as side_a
import algorithms.rate_constants as const
from operator import itemgetter
from scipy.stats import gamma, poisson, lognorm, norm
import re as re
import datetime as date
import calendar as ca

###########################################
########## Dataframe Functions ############
######## for Expected Loss Calcs ##########
###########################################

# Need to first calculate various factors used in setting up the average loss dataframe

# Monitoring Cost Modifiers
at_cost = utils.look_up("AtCost", "ParameterName", "Value", hx.params.tbl_monitoring_cost_mod)

mc_dismiss_rate = utils.look_up("MCDismissalRate", "ParameterName", "Value", hx.params.tbl_monitoring_cost_mod)

mc_dismiss_min = utils.look_up("MCDismissalMin", "ParameterName", "Value", hx.params.tbl_monitoring_cost_mod)

mc_dismiss_max = utils.look_up("MCDismissalMax", "ParameterName", "Value", hx.params.tbl_monitoring_cost_mod)

# SCA Claim Loads
s_load = 1

sd_load = utils.look_up("SDLoad", "ParameterName", "Value", hx.params.tbl_interaction_mod)

# Other Dismissal Modifiers
dismiss_deriv = utils.look_up("Derivatives", "ParameterName", "Value", hx.params.tbl_other_dismissal_mod)

dismiss_ma = utils.look_up("M&A", "ParameterName", "Value", hx.params.tbl_other_dismissal_mod)

# Derivative Dismissal Rate
deriv_rate = utils.look_up("DerivativeDismissalRate", "ParameterName", "Value", hx.params.tbl_deriv_freq_mod)

# Calcultes the average loss for each claim type across all layers
def calc_layer_avg_loss(variables, layer_df):
    # Creating the average loss dataframes needed for premium calcs
    # Note that Model and Unity premium calcs use the same average loss dataframe (model_avg_loss)
    cols = [str(i) for i in range(layer_df.shape[1])]
    model_avg_loss = pd.DataFrame(columns=cols)
    primary_avg_loss = pd.DataFrame(columns=cols)

    # Precompute common logs to avoid recalculating
    log_defense_factor = np.log(1 + variables["defense_sca_factor"])
    log_s_load = np.log(s_load)
    log_sd_load = np.log(sd_load)

    for layer_type, df in (("model", model_avg_loss), ("primary", primary_avg_loss)):

        if layer_type == "model":
            # Retrieve values for "model" layers
            layer_limit = layer_df.loc["limit"]
            layer_excess = layer_df.loc["excess"] + layer_df.loc["deductible"]
            ma_layer_excess = layer_df.loc["excess"]
        else:
            # Retrieve values for "primary" layers
            layer_limit = layer_df.loc["excess_limit"]
            layer_excess = layer_df.loc["deductible"]
            ma_layer_excess = layer_df.loc["ma_retention"]

        # Defense SCA Dismissed
        df.loc["DefenseSCADismissed"] = utils.truncated_lognormal(
            layer_limit, layer_excess,
            variables["defense_sca_mu"], variables["defense_sca_sigma"], 1
        )

        # SCA Monitoring Costs
        df.loc["SCAMonitoringCosts"] = (
            (1 - variables["dismissal_rate"]) * at_cost *
            utils.truncated_lognormal(
                layer_limit, layer_excess,
                variables["mu"] + log_defense_factor,
                variables["sigma_sca"], 1
            )
            + variables["dismissal_rate"] *
            utils.fixed_clt(
                mc_dismiss_rate * df.loc["DefenseSCADismissed"],
                mc_dismiss_min, mc_dismiss_max, True
            )
        )

        # Claim Type S
        df.loc["S_AvCost"] = (
            (1 - variables["dismissal_rate"]) *
            utils.truncated_lognormal(
                layer_limit, layer_excess,
                variables["mu"] + log_defense_factor + log_s_load,
                variables["sigma_sca"], 1
            )
        )

        # Claim Type SD
        df.loc["SD_AvCost"] = (
            (1 - variables["dismissal_rate"]) *
            utils.truncated_lognormal(
                layer_limit, layer_excess,
                variables["mu"] + log_defense_factor + log_sd_load,
                variables["sigma_sca"], 1
            )
        )

        # Claim Type D
        df.loc["D_AvCost"] = (
            (1 - dismiss_deriv) *
            utils.truncated_lognormal(
                layer_limit, layer_excess,
                variables["mu_der"] + log_defense_factor,
                variables["sigma_der"], 1
            )
        )

        # Claim Type M&A
        df.loc["M_AvCost"] = (
            (1 - dismiss_ma) *
            utils.truncated_lognormal(
                layer_limit, ma_layer_excess,
                variables["mu_ma"] + log_defense_factor,
                variables["sigma_ma"], 1
            )
        )

        # Derivative Monitoring Costs
        df.loc["DerivMonitoringCosts"] = (
            (1 - deriv_rate) * at_cost *
            utils.truncated_lognormal(
                layer_limit, layer_excess,
                variables["mu_der"] + log_defense_factor,
                variables["sigma_der"], 1
            )
            + deriv_rate *
            utils.fixed_clt(
                mc_dismiss_rate * df.loc["DefenseSCADismissed"],
                mc_dismiss_min, mc_dismiss_max, True
            )
        )

    return model_avg_loss, primary_avg_loss

# Calcultes the expected loss for each claim type across all layers
def calc_layer_net_exp_loss(avg_loss_df, variables, layer_df):
    # Creating the expected loss dataframes
    cols = [str(i) for i in range(layer_df.shape[1])]
    model_net_exp_loss = pd.DataFrame(columns=cols)
    primary_net_exp_loss = pd.DataFrame(columns=cols)
    primary_unity_net_exp_loss = pd.DataFrame(columns=cols)
    unity_net_exp_loss = pd.DataFrame(columns=cols)

    # Precompute common logs
    log_defense_factor = np.log(1 + variables["defense_sca_factor"])
    log_sd_load = np.log(sd_load)

    for layer_type, df, freq_str in (
        ("model", model_net_exp_loss, ""),
        ("primary", primary_net_exp_loss, ""),
        ("unity", unity_net_exp_loss, "_unity"),
        ("primary_unity", primary_unity_net_exp_loss, "_unity")
    ):
        if layer_type in ("model", "unity"):
            # Retrieve values for "model"/"unity" layers, with replacing of zeros with a very small positive value to avoid log(0)
            layer_excess = np.array(layer_df.loc["excess"] + layer_df.loc["deductible"], dtype=np.float64)
            ma_layer_excess = np.array(layer_df.loc["excess"], dtype=np.float64)
        else:
            # Retrieve values for "primary"/"primary_unity" layers, with replacing of zeros with a very small positive value to avoid log(0)
            layer_excess = np.array(layer_df.loc["deductible"], dtype=np.float64)
            ma_layer_excess = np.array(layer_df.loc["ma_retention"], dtype=np.float64)

        # Replace zeros with epsilon
        eps = np.finfo(float).eps
        layer_excess = np.where(layer_excess == 0, eps, layer_excess)
        ma_layer_excess = np.where(ma_layer_excess == 0, eps, ma_layer_excess)

        # Claim Type S
        df.loc["S_Exp"] = (
            1 - norm.cdf((np.log(layer_excess) - (variables["mu"] + log_defense_factor)) / variables["sigma_sca"], 0, 1)
        ) * avg_loss_df.loc["S_AvCost"] * variables[f"freq{freq_str}_s"]

        # Claim Type SD
        df.loc["SD_Exp"] = (
            1 - norm.cdf((np.log(layer_excess) - (variables["mu"] + log_defense_factor + log_sd_load)) / variables["sigma_sca"], 0, 1)
        ) * avg_loss_df.loc["SD_AvCost"] * variables[f"freq{freq_str}_sd"]

        # Claim Type D
        df.loc["D_Exp"] = (
            1 - norm.cdf((np.log(layer_excess) - (variables["mu_der"] + log_defense_factor)) / variables["sigma_der"], 0, 1)
        ) * avg_loss_df.loc["D_AvCost"] * variables[f"freq{freq_str}_d"]

        # Claim Type M&A
        df.loc["M_Exp"] = (
            1 - norm.cdf((np.log(ma_layer_excess) - (variables["mu_ma"] + log_defense_factor)) / variables["sigma_ma"], 0, 1)
        ) * avg_loss_df.loc["M_AvCost"] * variables[f"freq{freq_str}_ma"]

        # Claim Type SCA 1
        df.loc["SCA_Exp"] = (
            1 - norm.cdf((np.log(layer_excess) - (variables["defense_sca_mu"] + log_defense_factor)) / variables["defense_sca_sigma"], 0, 1)
        ) * variables["dismissal_rate"] * avg_loss_df.loc["DefenseSCADismissed"] * variables[f"freq{freq_str}_sca"]

        # Claim Type SCA 2
        df.loc["SCA_Exp_2"] = (
            avg_loss_df.loc["SCAMonitoringCosts"] * variables[f"freq{freq_str}_sca"]
            + avg_loss_df.loc["DerivMonitoringCosts"] * variables[f"freq{freq_str}_d"]
        )

        # Total Side ABC Net Expected Loss
        df.loc["Net Expected Loss"] = df.sum()

    return model_net_exp_loss, primary_net_exp_loss, unity_net_exp_loss, primary_unity_net_exp_loss

# NK: Long lines in this function & most the comments dont add anything so can be removed
# Calculates the Power ILF for use in the Intl Standalone expected loss calc. This is also used for MMP coverages
def calc_layer_power_ilf(limit, excess, deductible, alpha):

    # Some constants used in the calculation:
    l = 1350000

    r = 100000

    t = 1.5

    # Creating the Power ILF dataframe
    df_power_ilf = pd.DataFrame(columns = list(range(len(limit))), index = ["deductible + excess", "limit", "k", "k0", "k1", "power ilf"])

    # Sum the 'deductible' and 'excess' rows 
    sum_deductible_excess = np.nan_to_num(np.array(deductible, dtype=float), nan = 0) + np.nan_to_num(np.array(excess, dtype=float), nan = 0)

    # Apply condition to replace 0 with 0.01 
    sum_deductible_excess = np.where(sum_deductible_excess == 0, np.finfo(float).eps, sum_deductible_excess)

    df_power_ilf.loc["deductible + excess"] = sum_deductible_excess

    # Limit row
    df_power_ilf.loc["limit"] = limit

    # K row
    df_power_ilf.loc["k"] = (df_power_ilf.loc["limit"] / df_power_ilf.loc["deductible + excess"]) * t

    # K0 row
    df_power_ilf.loc["k0"] = l / r

    # K1 row
    df_power_ilf.loc["k1"] = df_power_ilf.loc["deductible + excess"] / r

    # Power ILF row
    df_power_ilf.loc["power ilf"] = (df_power_ilf.loc["k1"] ** alpha) * utils.ratio((-1 + (1 + df_power_ilf.loc["k"]) ** alpha), (-1 + (1 + df_power_ilf.loc["k0"]) ** alpha), 0)

    return df_power_ilf.loc["power ilf"]

# Calcultes the average loss for each claim type across all layers
def calc_layer_avg_loss_side_a(variables, layer_df):

    # Creating the average loss dataframes needed for premium calcs
    cols = [str(i) for i in range(layer_df.shape[1])]
    model_avg_loss = pd.DataFrame(columns=cols)
    model_unity_avg_loss = pd.DataFrame(columns=cols)

    # Retrieve values for "model" layers
    layer_limit = np.array(layer_df.loc["limit"], dtype=np.float64)
    layer_limit = np.where(layer_limit == 0, np.finfo(float).eps, layer_limit)
    layer_excess = np.array(layer_df.loc["excess"] + layer_df.loc["deductible"], dtype=np.float64)
    layer_excess = np.where(layer_excess == 0, np.finfo(float).eps, layer_excess)
    
    for i in ("model", "unity"):

        if i == "model":
            df = model_avg_loss
            string = ""
        else:
            df = model_unity_avg_loss
            string = "_unity"

        # Defense Side A Dismissed
        df.loc["DefenseSideADismiss"] = utils.truncated_lognormal(
            layer_limit, layer_excess,
            variables["defense_sca_mu"], variables["defense_sca_sigma"], 1
        ) * (1 - norm.cdf((np.log(layer_excess) - (variables["defense_sca_mu"])), 0, 1)) 

        # Claim Type DIC
        df.loc["S_AvCost_DIC"] = (1 - variables["dismissal_rate"]) * utils.truncated_lognormal(
            layer_limit, layer_df.loc["excess"],
            variables["mu"] + np.log(1 + variables["defense_sca_factor"] + np.log(s_load)),
            variables["sigma_sca"], 1
        )

        # Claim Type Tag Along
        intermediary_calc = utils.truncated_lognormal(
            np.array(layer_df.loc["deductible"], dtype=np.float64), 0,
            variables["mu"] + np.log(1 + variables["defense_sca_factor"]),
            variables["sigma_sca"], 1
        )
        df.loc["S_AvCost_TagAlong"] = (1 - variables["dismissal_rate"]) * utils.truncated_lognormal(
            layer_limit, layer_excess - intermediary_calc,
            variables["mu_der"] + np.log(1 + variables["defense_sca_factor"]),
            variables["sigma_der"], 1
        )
        
        # Claim Type Non-Shock
        df.loc["S_AvCost_NonShock"] = (1 - variables[f"side_a{string}_dismissal"]) * utils.truncated_lognormal(
            layer_limit, layer_excess,
            variables["mu_der"] + np.log(1 + variables["defense_sca_factor"]),
            variables["sigma_der"], 1
        )

        # Claim Type Shock
        df.loc["S_AvCost_Shock"] = (1 - variables[f"side_a{string}_dismissal"]) * utils.truncated_lognormal(
            layer_limit, layer_excess,
            variables["mu"] + np.log(1 + variables["defense_sca_factor"]),
            variables["sigma_sca"], 1
        )

        # Defense SCA Dismissed
        smc_limit = [10e6] * layer_df.shape[1]
        smc_excess = [0] * layer_df.shape[1]

        df.loc["DefenseSCADismissed"] = utils.truncated_lognormal(
            smc_limit, smc_excess,
            variables["defense_sca_mu"], variables["defense_sca_sigma"], 1
        )
        
        # SCA Monitoring Costs 
        df.loc["SCAMonitoringCosts"] = (
            (1 - variables["dismissal_rate"]) * at_cost *
            utils.truncated_lognormal(
                smc_limit, smc_excess,
                variables["mu"] + np.log(1 + variables["defense_sca_factor"]),
                variables["sigma_sca"], 1
            )
            + variables["dismissal_rate"] * utils.fixed_clt(
                mc_dismiss_rate * df.loc["DefenseSCADismissed"], mc_dismiss_min, mc_dismiss_max, True
            )
        )
                
        # Derivative Monitoring Costs
        df.loc["DerivMonitoringCosts"] = (
            (1 - deriv_rate) * at_cost *
            utils.truncated_lognormal(
                smc_limit, smc_excess,
                variables["mu_der"] + np.log(1 + variables["defense_sca_factor"]),
                variables["sigma_der"], 1
            )
            + deriv_rate * utils.fixed_clt(
                mc_dismiss_rate * df.loc["DefenseSCADismissed"], mc_dismiss_min, mc_dismiss_max, True
            )
        )
            
    return model_avg_loss, model_unity_avg_loss

# Calcultes the expected loss for each claim type across all layers for Side A
def calc_layer_net_exp_loss_side_a(avg_loss_df, variables, layer_df):
    # Helper to replace zeros with a very small positive value
    def safe_array(series):
        arr = np.array(series, dtype=np.float64)
        return np.where(arr == 0, np.finfo(float).eps, arr)

    # Precompute safe arrays
    layer_excess = safe_array(layer_df.loc["excess"] + layer_df.loc["deductible"])
    ma_layer_excess = safe_array(layer_df.loc["excess"])
    excess_safe = safe_array(layer_df.loc["excess"])  # used in DIC and DismissalExpense

    # Create the expected loss DataFrames
    model_net_exp_loss = pd.DataFrame(columns=[str(i) for i in range(layer_df.shape[1])])
    unity_net_exp_loss = pd.DataFrame(columns=[str(i) for i in range(layer_df.shape[1])])

    for mode, df in (("model", model_net_exp_loss), ("unity", unity_net_exp_loss)):
        freq_str = "" if mode == "model" else "_unity"

        # Claim Type DIC
        df.loc["DIC_Exp"] = (
            1 - norm.cdf(
                (np.log(excess_safe) - (variables["mu"] + np.log(1 + variables["defense_sca_factor"])))
                / variables["sigma_sca"], 0, 1
            )
        ) * avg_loss_df.loc["S_AvCost_DIC"] * variables[f"freq{freq_str}_dic"]

        # Claim Type Tag Along
        df.loc["TagAlong_Exp"] = (
            1 - norm.cdf(
                (np.log(layer_excess) - (variables["mu_der"] + np.log(1 + variables["defense_sca_factor"])))
                / variables["sigma_der"], 0, 1
            )
        ) * avg_loss_df.loc["S_AvCost_TagAlong"] * variables[f"freq{freq_str}_tag_along_side_a"]

        # Claim Type Non-Shock
        df.loc["NonShock_Exp"] = (
            1 - norm.cdf(
                (np.log(layer_excess) - (variables["mu_der"] + np.log(1 + variables["defense_sca_factor"])))
                / variables["sigma_der"], 0, 1
            )
        ) * avg_loss_df.loc["S_AvCost_NonShock"] * variables[f"freq{freq_str}_sector_side_a"] * (1 - variables["shock_load_freq"])

        # Claim Type Shock
        df.loc["Shock_Exp"] = (
            1 - norm.cdf(
                (np.log(layer_excess) - (variables["mu"] + np.log(1 + variables["defense_sca_factor"])))
                / variables["sigma_sca"], 0, 1
            )
        ) * avg_loss_df.loc["S_AvCost_Shock"] * variables[f"freq{freq_str}_sector_side_a"] * variables["shock_load_freq"]

        # Additional inputs
        prob_plaintiff = utils.look_up("ProbPlaintiff", "ParameterName", "Value", hx.params.tbl_side_a_mod)
        fees_cost_low, fees_cost_high = hx.params.tbl_plaintiff_fees["Cost"].iloc[:2]
        fees_mcap_low, fees_mcap_high = hx.params.tbl_plaintiff_fees["MarketCap"].iloc[:2]

        # Plaintiff Fees Side A
        df.loc["PlaintiffFees"] = (
            prob_plaintiff
            * (variables[f"freq{freq_str}_sector_side_a"] + variables[f"freq{freq_str}_tag_along_side_a"] + variables[f"freq{freq_str}_dic"])
            * (min(1, variables["mcap"] / fees_mcap_high) * (fees_cost_high - fees_cost_low) + fees_cost_low)
        )

        # Dismissal Expense
        df.loc["DismissalExpense"] = (
            avg_loss_df.loc["SCAMonitoringCosts"]
            * (variables[f"freq{freq_str}_tag_along_side_a"] + variables[f"freq{freq_str}_dic"])
            * variables["dismissal_rate"]
            + avg_loss_df.loc["DerivMonitoringCosts"]
            * variables[f"freq{freq_str}_sector_side_a"]
            * variables[f"side_a{freq_str}_dismissal"]
            + avg_loss_df.loc["DefenseSideADismiss"]
            * (
                (variables[f"freq{freq_str}_tag_along_side_a"] + variables[f"freq{freq_str}_dic"])
                * variables["dismissal_rate"]
                + variables[f"freq{freq_str}_sector_side_a"] * variables[f"side_a{freq_str}_dismissal"]
            )
            * (
                1 - norm.cdf(
                    (np.log(excess_safe) - (variables["mu"] + np.log(1 + variables["defense_sca_factor"])))
                    / variables["sigma_sca"], 0, 1
                )
            )
        )

        # Total Side A Net Expected Loss
        df.loc["Net Expected Loss"] = df.sum()

    return model_net_exp_loss, unity_net_exp_loss


# Calculates the Various Required Summary Dataframes from the Expected Losses
def calc_summary_dataframe(hxd, adr_standalone_expected_loss, contagion_expected_loss, intl_standalone_expected_loss, intl_large_company_expected_loss, layer_df, prelim_inputs, is_side_a = False):

    # Defining Row Names (These need to match the exact data schema naming conventions to write back to hxd)
    row_names = ["adr_standalone", "contagion", "intl_standalone", "intl_large_company"]

    # Attritional Expected Loss in USD for All Four Coverages
    df_att_expected_loss_usd = pd.DataFrame([adr_standalone_expected_loss.loc["adr_expected_loss"], contagion_expected_loss.loc["cont_expected_loss"], intl_standalone_expected_loss.loc["intl_expected_loss"], intl_large_company_expected_loss.loc["lc_expected_loss"]], index = row_names)

    if is_side_a == False:
        # Applying Side AB Discount
        mask_ab = layer_df.loc["side_selection"] == "AB"

        side_ab_discount = np.where(layer_df.loc["uw_side_ab_discount_override"] == 0, layer_df.loc["side_ab_discount"], layer_df.loc["uw_side_ab_discount_override"])

        df_att_expected_loss_usd = df_att_expected_loss_usd * np.array(1 - side_ab_discount * mask_ab.astype(float))

    # Assigning values to zero for those layers with no limit inputted
    df_att_expected_loss_usd[df_att_expected_loss_usd.columns[layer_df.loc["limit"] == 0]] = 0

    # Creating the Expected LR Dataframe
    df_expected_lr = pd.DataFrame([adr_standalone_expected_loss.loc["adr_expected_lr"], contagion_expected_loss.loc["cont_expected_lr"], intl_standalone_expected_loss.loc["intl_expected_lr"], intl_large_company_expected_loss.loc["lc_expected_lr"]], index = row_names)

    # Explicit CAT Loading in USD
    us_cat_load = utils.look_up("US Exposed", "Explicit Cat Load", "Value", hx.params.tbl_cat_load)
    non_us_cat_load = utils.look_up("Non-US Exposed", "Explicit Cat Load", "Value", hx.params.tbl_cat_load)

    df_cat_loading = pd.DataFrame(columns = range(layer_df.shape[1]), index = row_names)

    df_cat_loading.loc["adr_standalone"] = np.array((df_expected_lr.loc["adr_standalone"] + us_cat_load) / df_expected_lr.loc["adr_standalone"])

    df_cat_loading.loc["contagion"] = np.array((df_expected_lr.loc["contagion"] + us_cat_load) / df_expected_lr.loc["contagion"])

    df_cat_loading.loc["intl_standalone"] = (1 + non_us_cat_load)

    df_cat_loading.loc["intl_large_company"] = (1 + non_us_cat_load)

    # Total Expected Loss in USD
    df_total_expected_loss_usd = df_att_expected_loss_usd * np.float64(df_cat_loading)

    # Converting this to Source Currency and Applying Term Adjustment
    # CAT Expected Loss
    df_cat_expected_loss = pd.DataFrame(columns = range(layer_df.shape[1]), index = row_names)
    
    df_cat_expected_loss = df_att_expected_loss_usd * np.float64(df_cat_loading - 1) * prelim_inputs["fx_rate"] * prelim_inputs["term_adj_factor"]

    df_cat_expected_loss.loc["total"] = df_cat_expected_loss.sum()

    # Total Expected Loss
    df_total_expected_loss = df_total_expected_loss_usd * prelim_inputs["fx_rate"] * prelim_inputs["term_adj_factor"]

    df_total_expected_loss.loc["total"] = df_total_expected_loss.sum()
 
    return df_total_expected_loss, df_cat_expected_loss, df_expected_lr





# Calculates the Various Required Summary Dataframes for MMP from the Expected Losses
def calc_summary_dataframe_mmp(hxd, adr_standalone_expected_loss, contagion_expected_loss, intl_standalone_expected_loss, intl_large_company_expected_loss, layer_df, prelim_inputs):

    # Defining Row Names (These need to match the exact data schema naming conventions to write back to hxd)
    row_names = ["adr_standalone", "contagion", "intl_standalone", "intl_large_company"]

    # Attritional Expected Loss in USD for All Four Coverages
    df_att_expected_loss_usd = pd.DataFrame([adr_standalone_expected_loss.loc["adr_expected_loss"], contagion_expected_loss.loc["cont_expected_loss"], intl_standalone_expected_loss.loc["intl_expected_loss"], intl_large_company_expected_loss.loc["lc_expected_loss"]], index = row_names)

    # Assigning values to zero for those layers with no limit inputted
    df_att_expected_loss_usd[df_att_expected_loss_usd.columns[layer_df.loc["limit"] == 0]] = 0

    # Creating the Expected LR Dataframe
    df_expected_lr = pd.DataFrame([adr_standalone_expected_loss.loc["adr_expected_lr"], contagion_expected_loss.loc["cont_expected_lr"], intl_standalone_expected_loss.loc["intl_expected_lr"], intl_large_company_expected_loss.loc["lc_expected_lr"]], index = row_names)

    # Explicit CAT Loading in USD
    us_cat_load = utils.look_up("US Exposed", "Explicit Cat Load", "Value", hx.params.tbl_cat_load)
    non_us_cat_load = utils.look_up("Non-US Exposed", "Explicit Cat Load", "Value", hx.params.tbl_cat_load)

    df_cat_loading = pd.DataFrame(columns = range(layer_df.shape[1]), index = row_names)

    df_cat_loading.loc["adr_standalone"] = np.array((df_expected_lr.loc["adr_standalone"] + us_cat_load) / df_expected_lr.loc["adr_standalone"])

    df_cat_loading.loc["contagion"] = np.array((df_expected_lr.loc["contagion"] + us_cat_load) / df_expected_lr.loc["contagion"])

    df_cat_loading.loc["intl_standalone"] = (1 + non_us_cat_load)

    df_cat_loading.loc["intl_large_company"] = (1 + non_us_cat_load)

    # Total Expected Loss in USD
    df_total_expected_loss_usd = df_att_expected_loss_usd * np.float64(df_cat_loading)

    # Converting this to Source Currency and Applying Term Adjustment
    # CAT Expected Loss
    df_cat_expected_loss = pd.DataFrame(columns = range(layer_df.shape[1]), index = row_names)
    
    df_cat_expected_loss = df_att_expected_loss_usd * np.float64(df_cat_loading - 1) * prelim_inputs["fx_rate"] * prelim_inputs["term_adj_factor"]

    df_cat_expected_loss.loc["total"] = df_cat_expected_loss.sum()

    # Total Expected Loss
    df_total_expected_loss = df_total_expected_loss_usd * prelim_inputs["fx_rate"] * prelim_inputs["term_adj_factor"]

    df_total_expected_loss.loc["total"] = df_total_expected_loss.sum()
 
    return df_total_expected_loss, df_cat_expected_loss, df_expected_lr


# Calculates the Cost Percentiles for given Dismissal Rate, Log-Mu and Log-Sigma

def calc_cost_percentiles(dismissal_rate, log_mu, log_sigma):

    # Converting inputs to arrays to avoid errors
    dismissal_rate = np.array(dismissal_rate)
    log_mu = np.array(log_mu)
    log_sigma = np.array(log_sigma)

    df_cost_percentile = pd.DataFrame(columns = range(len(dismissal_rate)))

    perc_50_after_dismiss = np.maximum(0, utils.ratio(0.5 - dismissal_rate, 1 - dismissal_rate))

    perc_75_after_dismiss = np.maximum(0, utils.ratio(0.75 - dismissal_rate, 1 - dismissal_rate))

    df_cost_percentile.loc["perc_50_after_dismiss"] = lognorm.ppf(perc_50_after_dismiss, log_sigma, scale = np.exp(log_mu))

    df_cost_percentile.loc["perc_50_cost_only"] = lognorm.ppf(0.5, log_sigma, scale = np.exp(log_mu))

    df_cost_percentile.loc["perc_75_after_dismiss"] = lognorm.ppf(perc_75_after_dismiss, log_sigma, scale = np.exp(log_mu))

    df_cost_percentile.loc["perc_75_cost_only"] = lognorm.ppf(0.75, log_sigma, scale = np.exp(log_mu))

    return df_cost_percentile

# Gets the Required Inputs for the Cost Percentile Function    
def get_cost_percentile_inputs(hxd, prelim_inputs, is_side_a = False):

    adr_vars = freq_sev_func.process_freq(hxd, "ADR Standalone", prelim_inputs, is_side_a)

    adr_vars = freq_sev_func.process_sev(adr_vars)

    lc_vars = freq_sev_func.process_freq(hxd, "Large Company", prelim_inputs, is_side_a)

    lc_vars = freq_sev_func.process_sev(lc_vars)

    # Dismissal Rate
    dismissal_rate = [adr_vars["dismissal_rate"]] * 3

    # Log Mu
    ilf_band = utils.look_up(prelim_inputs["country"], "Country", "ILFBand", hx.params.tbl_intl_countries)
    log_mu_intl = utils.look_up("mu_standalone_" + str(ilf_band), "ParameterName", "Value", hx.params.tbl_intl_mod)
    log_mu_us = adr_vars["mu"] + math.log(1 + adr_vars["defense_sca_factor"])
    log_mu_large = lc_vars["mu"] + math.log(1 + lc_vars["defense_sca_factor"])

    log_mu = [log_mu_intl, log_mu_us, log_mu_large]

    # Log Sigma
    log_sigma_intl = utils.look_up("si_standalone", "ParameterName", "Value", hx.params.tbl_intl_mod)
    log_sigma_us = adr_vars["sigma_sca"]
    log_sigma_large = lc_vars["sigma_sca"]

    log_sigma = [log_sigma_intl, log_sigma_us, log_sigma_large]


    # Running Side A/ABC with 10m Limit
    coverage_str = "ABC" if is_side_a is False else "A"
    data = [coverage_str, 0, 0, 10e6 / prelim_inputs["fx_rate"], 0, 0, 0, 5e6 / prelim_inputs["fx_rate"], 0]

    row_names = ["side_selection",
        "side_ab_discount",
        "uw_side_ab_discount_override", 
        "limit",
        "excess",
        "deductible",
        "brokerage",
        "excess_limit",
        "ma_retention"]

    df = pd.DataFrame(data, index = row_names)

    if is_side_a is True:

        adr, adr_unity = side_a.adr_standalone_expected_loss_side_a(hxd, df, prelim_inputs)
        cont, cont_unity = side_a.contagion_expected_loss_side_a(hxd, df, adr, adr_unity, prelim_inputs)
        intl, intl_unity = side_a.intl_standalone_expected_loss_side_a(hxd, df, prelim_inputs)
        lc, lc_unity = side_a.intl_large_company_expected_loss_side_a(hxd, df, prelim_inputs)
        exp_loss, _, exp_lr = calc_summary_dataframe(hxd, adr, cont, intl, lc, df, prelim_inputs, is_side_a)
    else:

        adr, adr_unity = side_abc.adr_standalone_expected_loss(hxd, df, prelim_inputs)
        cont, cont_unity = side_abc.contagion_expected_loss(hxd, df, adr, adr_unity, prelim_inputs)
        intl, intl_unity, _ = side_abc.intl_standalone_expected_loss(hxd, df, prelim_inputs)
        lc, lc_unity = side_abc.intl_large_company_expected_loss(hxd, df, prelim_inputs)
        exp_loss, _, exp_lr = calc_summary_dataframe(hxd, adr, cont, intl, lc, df, prelim_inputs, is_side_a)




    return dismissal_rate, log_mu, log_sigma, exp_loss, exp_lr

# Calculates the Return on Capitel (RoC) for each layer in cds/layers
def calc_roc(hxd):

    import algorithms.rate_utilities as utils

    # Get Losses
    layer_metrics = utils.pd_df_from_hx_list(hxd.cds.large_cap.layers)[["expected_loss_cost", "written_line", "quoted_premium_100", "brokerage", "technical_premium"]].fillna(0)

    gross_losses = np.where(layer_metrics["written_line"] != 0, layer_metrics["expected_loss_cost"] * layer_metrics["written_line"], layer_metrics["expected_loss_cost"]) 

    net_tech = utils.calc_net_tech_premium(gross_losses, hxd)
    # layer_metrics["technical_premium"] * (1 - layer_metrics["brokerage"])

    # Get TP Parameters
    fx_rates = params.fx_rates.df()
    tp_params_df = params.tp_parameters.df()

    # FX Rates
    ccy = hxd.cds.currencies.source_currency
    fx_rate = fx_rates[fx_rates["ccy"]==ccy]["fx_rate"].iloc[0]

    bp_class = "International ML"

    year = utils.calc_tp_year(hxd)

    tp_IML = tp_params_df[(tp_params_df['business_plan_class'] == bp_class) & 
        (tp_params_df['year'] == year)]

    che = np.float64(tp_IML["che"].iloc[0])
    var_exp = np.float64(tp_IML["var_exp"].iloc[0])
    inv_inc = np.float64(tp_IML["inv_inc"].iloc[0])
    cost_of_ri = (np.float64(tp_IML["cost_of_ri"].iloc[0]) - np.float64(tp_IML["ri_rec"].iloc[0]))
    fixed_exp_usd = np.float64(tp_IML["fixed_exp"].iloc[0])
    fixed_exp = np.float64(fixed_exp_usd * fx_rate)

    total_exp = net_tech * var_exp + fixed_exp + gross_losses * che

    inv_returns = net_tech * inv_inc

    excess_load = np.float64(tp_IML["capital_req"].iloc[0])

    bound_premium = np.where(layer_metrics["written_line"] != 0, layer_metrics["quoted_premium_100"] * (1 - layer_metrics["brokerage"]) * layer_metrics["written_line"], layer_metrics["quoted_premium_100"] * (1 - layer_metrics["brokerage"]))

    profit = bound_premium - gross_losses - total_exp - cost_of_ri * layer_metrics["technical_premium"] * (1 - layer_metrics["brokerage"]) + inv_returns

    roc = np.where(layer_metrics["quoted_premium_100"] != 0, profit / (net_tech * excess_load), 0)

    return roc

# Runs calculations required for the premium build up graphs on the rating summary tab
def calc_graph_prem_build_up(hxd):

    import algorithms.rate_utilities as utils

    # Get Layer Metrics needed for graph calcs
    layer_metrics = utils.pd_df_from_hx_list(hxd.cds.large_cap.layers)[["expected_loss_cost", "written_line", "quoted_premium_100", "brokerage", "expected_loss_cost_att", "expected_loss_cost_cat", "technical_premium"]].fillna(0)

    layer_metrics["benchmark_premium"] = np.where(layer_metrics["written_line"] != 0, utils.ratio(layer_metrics["expected_loss_cost"] * layer_metrics["written_line"]/0.7, (1 - layer_metrics["brokerage"])), utils.ratio(layer_metrics["expected_loss_cost"] /0.7, (1 - layer_metrics["brokerage"])))

    gross_losses = np.where(layer_metrics["written_line"] != 0, layer_metrics["expected_loss_cost"] * layer_metrics["written_line"], layer_metrics["expected_loss_cost"])

    # Get TP Parameters
    fx_rates = params.fx_rates.df()
    tp_params_df = params.tp_parameters.df()

    # FX Rates
    ccy = hxd.cds.currencies.source_currency
    fx_rate = fx_rates[fx_rates["ccy"]==ccy]["fx_rate"].iloc[0]

    bp_class = "International ML"

    year = utils.calc_tp_year(hxd)

    tp_IML = tp_params_df[(tp_params_df['business_plan_class'] == bp_class) &
        (tp_params_df['year'] == year)]

    che = np.float64(tp_IML["che"].iloc[0]) * gross_losses
    fixed_exp_usd = np.float64(tp_IML["fixed_exp"].iloc[0])
    fixed_exp = np.float64(fixed_exp_usd * fx_rate)

    att_losses = pd.DataFrame(np.where(layer_metrics["written_line"] != 0, layer_metrics["expected_loss_cost_att"] * layer_metrics["written_line"], layer_metrics["expected_loss_cost_att"]), columns = ["gross_att_graph"])
      
    cat_losses = pd.DataFrame(np.where(layer_metrics["written_line"] != 0, layer_metrics["expected_loss_cost_cat"] * layer_metrics["written_line"], layer_metrics["expected_loss_cost_cat"]), columns = ["gross_cat_graph"])
    
    bound_premium = pd.DataFrame(np.where(layer_metrics["written_line"] != 0, layer_metrics["quoted_premium_100"] * (1 - layer_metrics["brokerage"]) * layer_metrics["written_line"], layer_metrics["quoted_premium_100"] * (1 - layer_metrics["brokerage"])), columns = ["bound_premium_graph"])


    nel_and_fe = gross_losses + fixed_exp + che

    cost_of_ri = pd.DataFrame(np.float64(tp_IML["cost_of_ri"].iloc[0] - np.float64(tp_IML["ri_rec"].iloc[0])) * nel_and_fe, columns = ["cost_ri_graph"])

    tech_expenses = pd.DataFrame(fixed_exp + np.float64(tp_IML["var_exp"].iloc[0]) * nel_and_fe, columns = ["expenses_graph"])

    bp_expenses = pd.DataFrame(np.array(layer_metrics["benchmark_premium"] * 0.3 * (1 - layer_metrics["brokerage"])), columns = ["expenses_graph"])

    excess_load = np.float64(tp_IML["capital_req"].iloc[0])

    profit_load = excess_load * 0.15

    profit = pd.DataFrame(profit_load * nel_and_fe, columns = ["profit_load_graph"])

    tech_brokerage =  pd.DataFrame(np.array(layer_metrics["technical_premium"] * layer_metrics["brokerage"]),  columns = ["brokerage_graph"])

    bp_brokerage = pd.DataFrame(np.array(layer_metrics["benchmark_premium"] * layer_metrics["brokerage"]), columns = ["brokerage_graph"])

    if hxd.cds.prem_build_up.selected_option is not None:
        selected = int(hxd.cds.prem_build_up.selected_option) - 1
    else:
        selected = 0
 

    if hxd.cds.large_cap.layers[selected].technical_premium == 0:
        hxd.cds.prem_build_up.technical_premium.gross_att_graph = 0
        hxd.cds.prem_build_up.benchmark_premium.gross_att_graph = 0
        hxd.cds.prem_build_up.bound_premium.gross_att_graph = 0

        hxd.cds.prem_build_up.technical_premium.gross_cat_graph = 0
        hxd.cds.prem_build_up.benchmark_premium.gross_cat_graph = 0
        hxd.cds.prem_build_up.bound_premium.gross_cat_graph = 0

        hxd.cds.prem_build_up.technical_premium.bound_premium_graph = 0
        hxd.cds.prem_build_up.benchmark_premium.bound_premium_graph = 0
        hxd.cds.prem_build_up.bound_premium.bound_premium_graph = 0

        hxd.cds.prem_build_up.technical_premium.cost_ri_graph = 0
        hxd.cds.prem_build_up.benchmark_premium.cost_ri_graph = 0
        hxd.cds.prem_build_up.bound_premium.cost_ri_graph = 0

        hxd.cds.prem_build_up.technical_premium.expenses_graph = 0
        hxd.cds.prem_build_up.benchmark_premium.expenses_graph = 0
        hxd.cds.prem_build_up.bound_premium.expenses_graph = 0

        hxd.cds.prem_build_up.technical_premium.profit_load_graph = 0        
        hxd.cds.prem_build_up.benchmark_premium.profit_load_graph = 0
        hxd.cds.prem_build_up.bound_premium.profit_load_graph = 0 

        hxd.cds.prem_build_up.technical_premium.brokerage_graph = 0
        hxd.cds.prem_build_up.benchmark_premium.brokerage_graph = 0
        hxd.cds.prem_build_up.bound_premium.brokerage_graph = 0
    else:
        hxd.cds.prem_build_up.technical_premium.gross_att_graph = att_losses.iloc[selected]["gross_att_graph"]
        hxd.cds.prem_build_up.benchmark_premium.gross_att_graph = att_losses.iloc[selected]["gross_att_graph"]
        hxd.cds.prem_build_up.bound_premium.gross_att_graph = 0

        hxd.cds.prem_build_up.technical_premium.gross_cat_graph = cat_losses.iloc[selected]["gross_cat_graph"]
        hxd.cds.prem_build_up.benchmark_premium.gross_cat_graph = cat_losses.iloc[selected]["gross_cat_graph"]
        hxd.cds.prem_build_up.bound_premium.gross_cat_graph = 0

        hxd.cds.prem_build_up.technical_premium.bound_premium_graph = 0
        hxd.cds.prem_build_up.benchmark_premium.bound_premium_graph = 0
        hxd.cds.prem_build_up.bound_premium.bound_premium_graph = bound_premium.iloc[selected]["bound_premium_graph"]

        hxd.cds.prem_build_up.technical_premium.cost_ri_graph = cost_of_ri.iloc[selected]["cost_ri_graph"]
        hxd.cds.prem_build_up.benchmark_premium.cost_ri_graph = 0
        hxd.cds.prem_build_up.bound_premium.cost_ri_graph = 0

        hxd.cds.prem_build_up.technical_premium.expenses_graph = tech_expenses.iloc[selected]["expenses_graph"]
        hxd.cds.prem_build_up.benchmark_premium.expenses_graph = bp_expenses.iloc[selected]["expenses_graph"]
        hxd.cds.prem_build_up.bound_premium.expenses_graph = 0

        hxd.cds.prem_build_up.technical_premium.profit_load_graph = profit.iloc[selected]["profit_load_graph"]        
        hxd.cds.prem_build_up.benchmark_premium.profit_load_graph = 0
        hxd.cds.prem_build_up.bound_premium.profit_load_graph = 0 

        hxd.cds.prem_build_up.technical_premium.brokerage_graph = tech_brokerage.iloc[selected]["brokerage_graph"]
        hxd.cds.prem_build_up.benchmark_premium.brokerage_graph = bp_brokerage.iloc[selected]["brokerage_graph"]
        hxd.cds.prem_build_up.bound_premium.brokerage_graph = 0
        
    return 
