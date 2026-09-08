import hx
import pandas as pd
import numpy as np
import algorithms.utils_global_lists as lst
import algorithms.utils_functions as fx
from algorithms.modifiers import modifiers
from algorithms.rate_constants import *
import math

def cdf(hxd, ded):
    # General parameters
    cds = hxd.cds
    param_ilf = fx.df_to_dict(hx.params.ilf_params, "Parameter", ["Commercial", "Financial"])

    ilf_alpha = param_ilf['alpha'][cds.entity_type]
    ilf_beta = param_ilf['beta'][cds.entity_type]
    ilf_lambda = param_ilf['lambda'][cds.entity_type]

    cdf = 1 - (1 + (ded / ilf_lambda) ** ilf_beta) ** (-ilf_alpha)
    return cdf

def exposure_factor(hxd, excess, limit, primary):
    return ((
        cdf(hxd, excess + limit) - cdf(hxd, excess)
        ).div(
            cdf(hxd, primary + base_lim) - cdf(hxd, primary), axis=0
        ))

def base_rate_calc(hxd, key, value):
    # General parameters
    param_size = hx.params.size_params

    size_lambda = param_size[param_size['Variable'] == key]['lambda']
    size_alpha = param_size[param_size['Variable'] == key]['alpha']
    size_theta = param_size[param_size['Variable'] == key]['theta']

    if key == "Revenue" and value < min_revenue:
        rate = min_revenue_rate 
    else:
        rate = sum(size_lambda * (value + size_theta) ** size_alpha)

    return rate

def admitted_calcs(hxd):
# ~~~~~~~~~~~~~~~~~~~ ADMITTED CALCS ~~~~~~~~~~~~~~~~~~~
# The admitted calcs consists of taking the rate on line of the layer right under Beazley's and applying an entity type factor and mods on it to get the admitted rate.

    cds = hxd.cds
    cds_cov_list = ['', '_social_engineering', '_other_cov']

    #Loop through excess layers
    for index, layer in enumerate(cds.layers):

        #Set the label for each layer:
        layer.layer_label = "Primary" if index==0 else f"Excess {index}"

        layer.layer_brokerage.calculated = cds.layers[0].brokerage

        # Define calculations for the primary layer
        if index == 0:
            if layer.limit and layer.limit > 0:
                for cov in cds_cov_list:
                    setattr(layer, 'excess' + cov, getattr(cds.retention, 'limit' + cov))
                layer.rate_per_m = layer.premium / (layer.limit / 1e6) if layer.premium else 0

        #Define calculations for all excess layers
        else:
            previous_layer = cds.layers[index -1]
            
            # These conditions are needed to prevent error output when layers are not inputed in order
            # The layer.limit and preious_layer.limit conditions prevent errors when the user enters then deletes a limit

            if layer.limit and layer.limit > 0:
                layer.rate_per_m = layer.premium / (layer.limit / 1e6) if layer.premium else None
                if previous_layer.limit and previous_layer.limit > 0 and previous_layer.excess is not None:
                    for cov in cds_cov_list:
                        setattr(layer, 'excess' + cov, getattr(previous_layer, 'excess' + cov) + getattr(previous_layer, 'limit' + cov))
                    layer.percent_underlying_rate = layer.rate_per_m/previous_layer.rate_per_m if (layer.rate_per_m and previous_layer.rate_per_m) else None

    # Create excess layers dropdown by removing the Primary layer
    cds.excess_layers = [layer.layer_label for index, layer in enumerate(cds.layers) if layer.layer_label != "Primary"]

    #Look up selected Beazley layer and underlying layer
    if cds.beazley_layer is None:
        hxd.beazley_layer_index = 1
    else: 
        layer_indices = [index for index, layer in enumerate(cds.layers) if layer.layer_label == cds.beazley_layer]
        hxd.beazley_layer_index = layer_indices[0] if layer_indices else 1

    beazley_pre_layer_index = hxd.beazley_layer_index -1
    cds.beazley_pre_layer = cds.layers[beazley_pre_layer_index].layer_label

    if hxd.beazley_layer_index < len(cds.layers):
        cds.total_layer_limit = cds.layers[hxd.beazley_layer_index].limit or 0
        cds.beazley_limit = cds.total_layer_limit * cds.beazley_share
        cds.lead_premium = cds.layers[hxd.beazley_layer_index].premium
        cds.underlying_layer_limit = cds.layers[beazley_pre_layer_index].limit or 0
        cds.underlying_premium = cds.layers[beazley_pre_layer_index].premium
        cds.underlying_rate_per_m = cds.layers[beazley_pre_layer_index].rate_per_m
        cds.underlying_brokerage.calculated = cds.layers[beazley_pre_layer_index].layer_brokerage.selected
    
    cds.beazley_layer_index = hxd.beazley_layer_index

def benchmark_calcs(hxd):
    #Can be deledted until row 216
    #General parameters
    cds = hxd.cds
    exp_agg = cds.exposure.aggregate
    cds_industry = cds.key_industry
    rating = cds.rating_factors

    cds_cov_list = ['', '_social_engineering', '_other_cov']

    param_industry = fx.df_to_dict(hx.params.industry_lookup, "Industry", ["Manufacturing", "Wholesale Trade", "Retail Trade", "All"])
    param_claim = fx.df_to_dict(hx.params.claim_basis, "Claim Basis", "Factor")
    param_endt_ext = fx.df_to_dict(hx.params.endt_extensions, "Endorsements and Coverages Extensions", "Factor")
    param_other_perils = fx.df_to_dict(hx.params.other_perils, "Other Perils", ["On-Premises", "Off-Premises"])
    param_sublim = fx.df_to_dict(hx.params.sublimited_perils, "Sublimited Perils", "Factor")

    # ~~~~~~~~~~~~~~~~~~~ BENCHMARK CALCS ~~~~~~~~~~~~~~~~~~~
    
    rate_revenue = base_rate_calc(hxd, "Revenue", exp_agg.revenue)
    rate_assets = base_rate_calc(hxd, "Assets", exp_agg.assets)
    rate_employees = base_rate_calc(hxd, "Employees", exp_agg.employees)

    adj_fct_locations = max(0.8, min(1.25, (1.6 + math.log10( exp_agg.locations + 1 )) / 3))
    adj_fct_assets = 0.875 if exp_agg.assets < 100000 else (math.log10( exp_agg.assets) + 12.5 ) / 20
    adj_fct_max = max(adj_fct_locations, adj_fct_assets)

    industry_grp_lookup = cds_industry.industry_group if cds_industry.industry_group in ["Manufacturing", "Wholesale Trade", "Retail Trade"] else "All"
    industry_factor = param_industry[cds_industry.industry][industry_grp_lookup] if cds.entity_type != 'Financial' else 1 #TODO: update when JR provides factors

    #Base Prem calcs for all structures
    commercial_main = (rate_revenue + rate_employees) / 2 * adj_fct_locations * adj_fct_assets
    commercial_se = rate_revenue * adj_fct_assets

    hxd.total_adj_factor =  industry_factor * cds.term_adjustment * param_claim[rating.claim_basis] * (1 + param_endt_ext[rating.endt_extensions])
    std_struct_main = commercial_main * hxd.total_adj_factor
    std_struct_se = commercial_se * hxd.total_adj_factor  if cds.has_social_engineering else 0
    std_struct_other = (std_struct_main + std_struct_se) * max(0.025, param_other_perils[rating.other_on_premises]["On-Premises"] + param_other_perils[rating.other_off_premises]["Off-Premises"]) if cds.has_other_coverages else 0

    #ILF calcs
    base_ded = max(base_ded_lambda * exp_agg.revenue ** base_ded_alpha, base_ded_min) 
        
    exposure_fct_base_ded = cdf(hxd, base_ded + base_lim) - cdf(hxd, base_ded)
    exposure_fct_base_lim = cdf(hxd, base_ded + base_lim)

    # Initialise the dataframes to follow the same format
    calcs_dfs = {}
    for df in ['primary_struct', 'limit_df', 'excess_df', 'calc_df', 'weight_df', 'std_tower_df', 'allocated_pricing', 'implied_pricing_std_lim_ded_adj', 'expiring_df']:
        calcs_dfs[df] = pd.DataFrame(index = ["main", "se", "other"])

    # Calculating the primary structure for all coverages

    primary_struct = calcs_dfs['primary_struct']
    primary_struct['deductible'] = [getattr(cds.retention,'limit' + cov) for cov in cds_cov_list]

    primary_struct['limit'] = [getattr(cds.layers[0],'limit' + cov) for cov in cds_cov_list]

    primary_struct['ded_effect'] = [ cdf(hxd, ded + base_lim) - cdf(hxd, ded) for ded in primary_struct['deductible']]

    primary_struct['ded_effect_base'] = [0.25 + 0.75 * ((ded / base_ded) if ded < base_ded else 1) for ded in primary_struct['deductible']]

    primary_struct['ded_factor'] = primary_struct['ded_effect'] / (exposure_fct_base_ded * primary_struct['ded_effect_base'] ** 0.75)

    primary_struct['lim_factor'] = [(
        cdf(hxd, ded + lim) - cdf(hxd, ded)) / (
            cdf(hxd, ded + base_lim) - cdf(hxd, ded)
        ) for ded, lim in zip(primary_struct['deductible'], primary_struct['limit'])]
        
    primary_struct['structure'] =  primary_struct['ded_factor'] * primary_struct['lim_factor']

    primary_struct['std_struct'] = [std_struct_main, std_struct_se, std_struct_other]
    
    primary_struct['std_lim_ded_adj'] = primary_struct['std_struct'] * primary_struct['ded_factor']

    primary_struct['primary_struct'] = primary_struct['std_struct'] * primary_struct['structure']

    for layer in cds.layers:
        calcs_dfs['limit_df'][layer.layer_label] = [getattr(layer,'limit' + cov) for cov in cds_cov_list]
        calcs_dfs['excess_df'][layer.layer_label] = [getattr(layer,'excess' + cov) for cov in cds_cov_list]

    weight_df = [(0 if layer.layer_label == cds.beazley_layer else 15 * layer.layer_quality) for layer in cds.layers]
    weight_base =  20 + 5 * sum(1 for weight in weight_df if weight>0)
    weight_df.insert(0, weight_base)
    weight_df = [weight / sum(weight_df) for weight in weight_df]

    calcs_dfs['calc_df'] = exposure_factor(hxd, calcs_dfs['excess_df'], calcs_dfs['limit_df'], calcs_dfs['excess_df']['Primary'])

    sublim_prem = primary_struct['primary_struct'].sum(axis=0) * (
                    1 / (1 - param_sublim[rating.sublimited_perils])
                    - 1)

    calcs_dfs['std_tower_df'] = (calcs_dfs['calc_df'].multiply(primary_struct['std_lim_ded_adj'], axis=0)).astype(np.float64)
    std_tower_total = calcs_dfs['std_tower_df'].sum(axis=0)

    std_tower_total['Primary'] += sublim_prem

    gnwp_layers = [(getattr(layer, 'premium') if layer.premium else 0) * (1 - cds.layers[0].brokerage) for layer in cds.layers]
    calcs_dfs['allocated_pricing_df'] = gnwp_layers * calcs_dfs['std_tower_df'].div(std_tower_total, axis=1)
    calcs_dfs['implied_pricing_std_lim_ded_adj'] = calcs_dfs['allocated_pricing_df']/calcs_dfs['calc_df']
    calcs_dfs['implied_pricing_std_lim_ded_adj'].insert(0, "Base", primary_struct['std_lim_ded_adj'])

    std_lim_pol_ded_price = (calcs_dfs['implied_pricing_std_lim_ded_adj'] * weight_df).sum(axis=1)

    weighted_layer_price = ((calcs_dfs['calc_df'].multiply(std_lim_pol_ded_price, axis=0)).sum(axis=0)).astype(np.float64)
    weighted_layer_price['Primary'] += sublim_prem

    for index, layer in enumerate(cds.layers):
        setattr(layer, 'internal_weighted_premium', weighted_layer_price.iloc[index])

    return  (primary_struct['ded_factor'],
            weight_df, 
            calcs_dfs['implied_pricing_std_lim_ded_adj'], 
            calcs_dfs['excess_df'].iloc[:, hxd.beazley_layer_index], 
            calcs_dfs['limit_df'].iloc[:, hxd.beazley_layer_index],
            calcs_dfs['calc_df'].iloc[:, [hxd.beazley_layer_index]],
            calcs_dfs['excess_df']['Primary'])

def layer_calcs(hxd):

    #General parameters
    cds = hxd.cds
    cds_industry = cds.key_industry
    layer = cds.layers[0]

    param_sic = fx.df_to_dict(hx.params.sic_lookup, "SIC Code 4ch", ["Industry Description 4ch", "Industry Group", "Industry"])
    param_entity = fx.df_to_dict(hx.params.institution_lookup, "Institution Type", "Factor")

    #Look up the sic code industries in the parameter table 
    if hasattr(cds_industry, "code") and cds_industry.code is not None:
        industry_code = cds_industry.code
    else:
        industry_code = "0111"
        
    cds_industry.code_name = param_sic[industry_code]["Industry Description 4ch"]
    cds_industry.industry_group = param_sic[industry_code]["Industry Group"]
    cds_industry.industry = param_sic[industry_code]["Industry"]
    cds.entity_type = "Financial" if cds_industry.industry_group == "Financial Services" else "Commercial"
    
    #Look up the entity type factor in the parameter table 
    cds.excess_factor = param_entity[cds.entity_type]

    #Run premium calculations
    admitted_calcs(hxd)
    modifiers(hxd)

    # Return unity premium for layer to price
    if cds.underlying_rate_per_m and cds.beazley_limit and cds.beazley_share:

        # # Uncomment when switching to new benchmark calcs
        # benchmark_calcs(hxd)

        # Final charged premium
        layer_rate = cds.underlying_rate_per_m * cds.excess_factor
        layer_premium = layer_rate * cds.total_layer_limit / 1e6
        adjusted_premium = layer_premium / cds.term_adjustment_underlying * cds.term_adjustment

        if cds.is_follow and cds.lead_premium and cds.beazley_share:
            layer.final_premium = cds.lead_premium * cds.beazley_share
        else:
            layer.final_premium = adjusted_premium * cds.beazley_share * cds.mod_factor * cds.expense_mod_factor * (cds.surplus_deviation_factor if cds.is_surplus else 1)

        layer.final_premium_annual = layer.final_premium / cds.term_adjustment

        # # Final unity premium
        # # Moved to tpi_summary.py and updated to round_premium
        # layer.unity_premium = adjusted_premium * cds.beazley_share
        # layer.unity_premium_annual = layer.unity_premium / cds.term_adjustment 

        
        
        # Assign value to quoted premium to align with other raters
        layer.quoted_premium = layer.final_premium        