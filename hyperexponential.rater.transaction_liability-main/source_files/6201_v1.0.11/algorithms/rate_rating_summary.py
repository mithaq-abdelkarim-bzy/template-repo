import hx
import pandas as pd
import numpy as np
import math as math
import scipy
from scipy.stats import norm
from algorithms import rate_utilities as utils
from algorithms import rate_constants as constants
from operator import itemgetter

def mbbefd_mu(g, b):
    g = np.asarray(g, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)

    gb = g * b
    log_g = np.log(g)
    log_b = np.log(b)
    log_gb = np.log(gb)

    conditions = [
        g == 1,
        (g > 1) & (b == 1),
        (g > 1) & np.isclose(gb, 1),
        (b > 0) & (b != 1) & (~np.isclose(gb, 1)) & (g > 1)
    ]

    choices = [
        1.0,
        log_g / (g - 1),
        (g - 1) / (g * log_g),
        log_gb * (1 - b) / ((1 - gb) * log_b)
    ]

    mu = np.select(conditions, choices, default=-1.0)
    return mu

def mbbefd_fx(curve_param_x, g, b):
    curve_param_x = np.asarray(curve_param_x, dtype=np.float64)
    g = np.asarray(g, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)

    gb = g * b
    log_g = np.log(g)
    log_gb = np.log(gb)

    conditions = [
        g == 1,
        (g > 1) & (b == 1),
        (g > 1) & np.isclose(gb, 1),
        (b > 0) & (b != 1) & (~np.isclose(gb, 1)) & (g > 1)
    ]

    choices = [
        curve_param_x,
        np.log(1 + (g - 1) * curve_param_x) / log_g,
        (1 - b ** curve_param_x) / (1 - b),
        np.log(((g - 1) * b + (1 - gb) * (b ** curve_param_x)) / (1 - b)) / log_gb
    ]

    return np.select(conditions, choices, default=0.0)


def simulation(transaction_value, volatility):
    # generate 999 percentiles from 0.0001 to 0.9999
    percentiles = np.linspace(0.0001, 0.9999, 9999)
    # Calculate simulated values from the normal distribution 
    simulated_values = norm.ppf(percentiles, loc=transaction_value, scale=transaction_value * volatility)
    # Compute simulated losses
    simulated_losses = np.median(np.vstack([np.zeros_like(simulated_values), np.full_like(simulated_values, transaction_value), transaction_value - simulated_values]), axis=0)
    # Thresholds condition based on div_threshold
    threshold_trigger = simulated_losses < (transaction_value * constants.div_threshold)
    # Adjust losses only f they meet the threshold condition 
    simulated_loss_adjusted = np.where(threshold_trigger, 0, simulated_losses)

    return simulated_loss_adjusted

def weighted_calcs(weights, elements):
    return sum([weight * element for weight, element in zip(filter(None, weights), filter(None, elements))])

def blend_option(cds):
    option = cds.blend_option
    layers = cds.layers
    blend_options = ["option_1", "option_2", "option_3"]

    # Instruction box
    option.instruction = "Select options to blend and copy the Blended Quote output to the table above."

    # Blend Inputs
    option.option_names_list = [layer.option_name for index, layer in enumerate(layers)]

    # this code is to allow for an istnace where the blended optionsa re filled out but a layer column is deleted 
    in_blend = True # Start with True and set to False if any option is not found
    for option_number in [1, 2, 3]:
        option_name = getattr(option, f"option_{option_number}").option_name
        if option_name is not None:
            match_found = any(layer.option_name is not None and option_name in layer.option_name for layer in layers)
        else:
            match_found = True
        if not match_found:
            in_blend = False
            break

    if option.option_1.option_name and option.option_1.weight and in_blend == True:
        # Get blend options and weights input in a list
        option_names = [getattr(getattr(option, item), "option_name") for item in blend_options]
        weights = [getattr(getattr(option, item), "weight") for item in blend_options]

        # option.option_name = option_names

        # Lookup individual option metrics
        lookup_indices = []

        for idx, item in enumerate(blend_options):
            if option_names[idx]:
                lookup_index = [index for index, layer in enumerate(layers) if layer.option_name == option_names[idx]][0]
                lookup_indices.append(lookup_index)
                element = getattr(option, item)
                setattr(element, "weight_excess", layers[lookup_index].excess.selected)
                setattr(element, "model_rol", layers[lookup_index].model_rol)


        # Blend quote calculations #######################################################

        # Lookup all option values for weight calculations
        blend_limits = [layers[lookup_index].limit for lookup_index in lookup_indices]       
        blend_limit_pcts = [layers[lookup_index].limit_pct for lookup_index in lookup_indices]       
        blend_excesses = [layers[lookup_index].excess.selected for lookup_index in lookup_indices]       
        blend_excess_pcts = [layers[lookup_index].excess_pct.selected for lookup_index in lookup_indices]

        # Set blend values       
        option.option_name = 'Blend of ' + ' and '.join(filter(None, [name for name in option_names]))

        # Calculated values
        option.limit = weighted_calcs(weights, blend_limits)
        option.limit_pct = weighted_calcs(weights, blend_limit_pcts)
        option.excess = weighted_calcs(weights, blend_excesses)
        option.excess_pct = weighted_calcs(weights, blend_excess_pcts)

        # Non-calculated values
        option.indicated = layers[lookup_indices[0]].indicated

    pass



def rate_rating_summary(hxd):
    # Use a for loop if your model prices multiple layers 
    layers = hxd.cds.layers
    for index, layer in enumerate(layers):
        cds = hxd.cds
        freq = cds.rating_factors.freq
        policy_info = cds.policy_info
        params = hx.params        
        sev = cds.rating_factors.sev

        
        layer.limit_pct = layer.limit / policy_info.transaction_value if (layer.limit is not None and policy_info.transaction_value not in [None, 0]) else 0
      
        if layer.excess.selected is not None:
            layer.excess_pct.calculated = layer.excess.selected / policy_info.transaction_value if (policy_info.transaction_value not in [None, 0]) else 0
        elif layer.excess_pct.selected is not None:
            layer.excess.calculated = layer.excess_pct.selected * policy_info.transaction_value if (policy_info.transaction_value not in [None, 0]) else 0


        if freq.target.jurisdiction == "EU-27 countries (+ Switzerland)":
            cds.rating_factors.fun_top_up.base_rate = constants.eu_base_rate
        else:
            cds.rating_factors.fun_top_up.base_rate = constants.all_other_base_rate  


        if not layer.is_fun_top_up_coverage:

            sev_params = params.table_severity_parameters
            param_volatility = utils.df_to_dict(params.table_volatility, "volatility", "pct")

            # DOES NOT VARY BY OPTION
            # Set up cover parameters
            sev_cov_flags = [1 * getattr(getattr(sev, cov), "coverage_flag") for cov in constants.sev_cov]
            sev_cov_assessments = [getattr(getattr(sev, cov), "severity_assessment") for cov in constants.sev_cov]
            sev_adjustments = [getattr(getattr(sev, cov), "adjustment") for cov in constants.sev_cov]

            covers_parameters = pd.DataFrame({
                "coverage": constants.sev_cov,
                "include": sev_cov_flags,
                "severity": sev_cov_assessments,
                "sev_adjustment": sev_adjustments
                })

            covers_parameters = pd.merge(covers_parameters, sev_params, on="severity")

            covers_parameters['mu'] = mbbefd_mu(covers_parameters['g'].values, covers_parameters['b'].values)


            # VARIES BY OPTION
            # Set up curve parameters
            excess_pct = []
            limit_pct = []

            # Get the list of excess and limit inputs for each option
            for option in cds.layers:
                excess_pct.append(option.excess_pct.selected)
                limit_pct.append(option.limit_pct)
            
            excess_pct = [0 if i is None else i for i in excess_pct]
            limit_pct = [0 if i is None else i for i in limit_pct]

            # for i in range(len(excess_pct):
            #     if excess_pct[i] is None:
            #         excess_pct[i] = 0

            # for i in range(len(limit_pct):
            #     if limit_pct[i] is None:
            #         limit_pct[i] = 0
            
            # Derive the curve parameters based on the excess/input for each option
            curve_parameters = pd.DataFrame(
                {"ax": np.array(limit_pct) / constants.pml_factor, 
                "bx": np.array(excess_pct) / constants.pml_factor
                })
            # This returns a curve parameter 'x' for each option
            curve_parameters["x"] = curve_parameters["ax"] + curve_parameters["bx"]

            # Default values
            layer.model_premium = 0
            layer.expected_loss_cost = 0
            layer.expected_loss_cost_pre_uw_adj = 0


            # is_layer_fun_top_up_coverage = layer.is_fun_top_up_coverage
            # for index, layer in enumerate(cds.layers):
            #     if is_layer_fun_top_up_coverage == layer.is_fun_top_up_coverage:
                    
                    # If the limit is missing, skip calculations and check the next layer
            if not layer.limit:
                continue

            # Calculate the expected cost % to the layer for each coverage
            # Limit 
            option_limit =  mbbefd_fx(curve_parameters['x'].iloc[index], covers_parameters['g'].values, covers_parameters['b'].values)   

            # Excess
            option_excess = mbbefd_fx(curve_parameters['bx'].iloc[index], covers_parameters['g'].values, covers_parameters['b'].values)

            # Layer
            option_layer = option_limit - option_excess

            # Adjusted MBBEFD
            option_mbbefd_adj_pre_uw = np.array(option_layer) * covers_parameters["include"] * constants.sev_gen_param_weight * covers_parameters["mu"]
            option_mbbefd_adj = option_mbbefd_adj_pre_uw * (1 + covers_parameters["sev_adjustment"])
            
            #Sum coverages to get the expected Cost % to Layer
            expected_cost_pct_to_layer_pre_uw = sum(option_mbbefd_adj_pre_uw)
            expected_cost_pct_to_layer = sum(option_mbbefd_adj)

            # Core Cover Cost and Premium
            total_expected_cost = constants.pml_factor * policy_info.transaction_value * freq.freq_adjusted * (constants.sev_base_rate / constants.sev_gen_param_mu) if policy_info.transaction_value else 0
            
            core_cover_exp_cost = expected_cost_pct_to_layer * total_expected_cost
            core_cover_exp_cost_pre_uw = (expected_cost_pct_to_layer_pre_uw * total_expected_cost) / freq.freq_adjusted * freq.freq_adjusted_pre_uw if (freq.freq_adjusted != 0 and freq.freq_adjusted_pre_uw != 0) else 0
            
            gross_core_model_premium_excl_exp = core_cover_exp_cost / constants.priced_to_lr / (1 - layer.brokerage)
            gross_core_model_premium_excl_exp_pre_uw = gross_core_model_premium_excl_exp / core_cover_exp_cost * core_cover_exp_cost_pre_uw if core_cover_exp_cost != 0 else 0

            # DIV Cover Cost and Premium
            # Volatility for simulations
            volatility = param_volatility[sev.volatility]
            simulated_losses = simulation(policy_info.transaction_value, volatility) if policy_info.transaction_value else 0
            adjusted_losses = simulated_losses - layer.excess.selected if layer.excess.selected else simulated_losses
            stacked = np.stack([np.zeros_like(adjusted_losses), np.full_like(adjusted_losses, layer.limit), adjusted_losses])
            simulated_option_loss = np.median(stacked, axis=0)

            div_severity = np.mean(simulated_option_loss)
            div_frequency = freq.freq_adjusted * (constants.sev_base_rate / constants.sev_gen_param_mu) * constants.sev_gen_param_weight * (1 + sev.general_warranties.adjustment)
            div_cover_exp_cost = div_severity * div_frequency if sev.div_flag else 0

            gross_div_model_premium_excl_exp = div_cover_exp_cost / constants.priced_to_lr / (1 - layer.brokerage) if layer.brokerage is not 0 else 0 
            gross_div_model_premium_excl_exp_pre_uw = gross_div_model_premium_excl_exp / freq.freq_adjusted * freq.freq_adjusted_pre_uw if (freq.freq_adjusted != 0 and freq.freq_adjusted_pre_uw != 0) else 0 # UW adjustment was only applied to div_freq

            # Total Cost and Premium
            all_cover_exp_cost = core_cover_exp_cost + div_cover_exp_cost
            gross_total_model_premium_excl_exp = gross_core_model_premium_excl_exp + gross_div_model_premium_excl_exp + (policy_info.uw_expenses if (policy_info.uw_expenses_flag and (policy_info.uw_expenses is not None)) else 0) #model premium output
            gross_total_model_premium_excl_exp_pre_uw = gross_core_model_premium_excl_exp_pre_uw + gross_div_model_premium_excl_exp_pre_uw + (policy_info.uw_expenses if (policy_info.uw_expenses_flag and (policy_info.uw_expenses is not None)) else 0) #model premium output pre-uw adj
        

            # Expenses
            expenses = policy_info.uw_expenses if (policy_info.uw_expenses_flag and (policy_info.uw_expenses is not None)) else 0
            expected_loss_cost = (gross_total_model_premium_excl_exp - expenses) * (1 - layer.brokerage) * constants.priced_to_lr
            expected_loss_cost_pre_uw = (gross_total_model_premium_excl_exp_pre_uw - expenses) * (1 - layer.brokerage) * constants.priced_to_lr
        
        # These are the calculations for fundamental top up coverage
        else: 
            # No expenses for fundamental top up 
            expenses = 0
            if layer.limit is not None and layer.brokerage is not None:
                gross_total_model_premium_excl_exp = layer.limit * cds.rating_factors.fun_top_up.base_rate * (1 + cds.rating_factors.fun_top_up.adjustment)
                expected_loss_cost = (gross_total_model_premium_excl_exp - expenses) * (1 - layer.brokerage) * constants.priced_to_lr
                expected_loss_cost_pre_uw = (layer.limit * cds.rating_factors.fun_top_up.base_rate - expenses) * (1 - layer.brokerage) * constants.priced_to_lr
            else:
                gross_total_model_premium_excl_exp = 0 
                expected_loss_cost = 0
                expected_loss_cost_pre_uw = 0


        # Set output values
        layer.model_premium = gross_total_model_premium_excl_exp
        layer.expected_loss_cost = expected_loss_cost
        layer.expected_loss_cost_pre_uw_adj = expected_loss_cost_pre_uw
        layer.model_rol = layer.model_premium / layer.limit if layer.limit else None
    
        
            # Warning messages
        if layer.limit:
            if layer.model_rol < 0.004:
                layer.warnings = "ROL below 0.4%" 
            elif layer.model_premium < 40e3:
                layer.warnings = "Premium below $40k"
            else:
                layer.warnings = ""

        # Calculate the impact of UW adjustments
        layer.uw_adj_impact = utils.ratio(layer.expected_loss_cost, layer.expected_loss_cost_pre_uw_adj) - 1 if layer.expected_loss_cost_pre_uw_adj else 0

    # Blend option -- helps UW calculate the inputs necessary to add a weighted option between ones that have already been created
    blend_option(cds)

    num_layers = len(layers)
    for index in range(1, constants.max_layers+1):
        setattr(hxd.cds.rate_change, f"show_layer_{index}", True) if index <= num_layers else False


