import json
import numpy as np
import pandas as pd
import polars as pl
import hx

from algorithms.rate_constants import max_layers, states_list, weight_epl, weight_fid, weight_pcl
from algorithms.rate_utilities import ratio, title_rc, year_diff, calc_pro_rata

# Start of a possible defaulting value for rate change if one of the raters is turned off
# Not the most logical thing to do

# def rate_change_buckets(hxd):
#      buckets = {
#         "model": [],  # NOTE: leave this empty - starts from expiry data priced with current model
#         "exposure": [
#             "cds/exposure/granular/pcl/base_rate/asset_size",
#             "cds/split/seasonal/head_count",
#             "cds/split/independent_contractors/head_count",
#             "cds/split/temporary/head_count",
#             "cds/split/foreign/head_count",
#             "cds/exposure/granular/pcl/base_rate/revenue",
#             "cds/fid/base_premium/bp_plans/percent_of_active_participants",
#             "cds/fid/base_premium/bp_plans/additional_designated_fiduciaries",
#             "cds/fid/base_premium/bp_plans/assets_contributions",
#             "cds/fid/base_premium/bp_plans/reactive_employee_exposure/employee_exposure",
#             "cds/fid/base_premium/bp_plans/total_employees_or_members",
#             "cds/fid/employer_type",
#             "cds/fid/base_premium/bp_plans/plan_type",
#         ],
#         "risk_characteristics": [],
#         "deductible": [
#             "cds/layers/coverages/epl/quote_grid/qg_options/retention",
#             "cds/layers/coverages/fid/quote_grid/qg_options/retention",
#             "cds/layers/coverages/pcl/quote_grid/qg_options/retention",
#         ],
#         "limit": [
#             "cds/layers/coverages/epl/quote_grid/qg_options/aggregate_limit",
#             "cds/layers/coverages/fid/quote_grid/qg_options/aggregate_limit",
#             "cds/layers/coverages/pcl/quote_grid/qg_options/aggregate_limit",
#             "cds/layers/coverages/epl/quote_grid/qg_options/adl_limit",
#             "cds/layers/coverages/fid/quote_grid/qg_options/adl_limit",          
#         ],
#         "terms_conditions": [
#             "cds/standard_fields/inception_date",
#             "cds/standard_fields/expiry_date",
#             "cds/state_requirements/retroactive_date",         
#             "cds/coverage_elections/epl",
#             "cds/coverage_elections/fid",
#             "cds/coverage_elections/pcl"
#         ],
        
#         "brokerage": ["cds/layers/brokerage"],
#         "other": [],
#     }


# RC helper functions 
def get_matching_row(table, low_col, value):
    """Filter table for a row where value is between low_col and high_col"""
    matched = table.filter((pl.col(low_col) <= value) )#& (pl.col(high_col) >= value)
    return matched [-1]

def get_ratios(table, ratio):
    """Get modifier for a given ratio"""
    row = get_matching_row(table, "Ratio Low", ratio)
    return row["Ratio Low"].item(), row["Ratio High"].item()

def interpolate_modifier(ratio, low, high, coverage):
    """Interpolate modifier based on ratio within band"""
    if coverage == 'epl' and low == 3:
        return 1
    elif coverage == 'fid' and low == high:
        return 0
    return (ratio - low) / (high - low)

def calculate_ded_factor(ratio, in_band, low_factor, high_factor):
    """Calculate deductible factor based on ratio and interpolation"""
    if ratio <= 0.1:
        return 1.4
    return in_band * high_factor + (1 - in_band) * low_factor

def capped_ratio(value, guideline, state):
    """Cap ratio at 3 for Florida, otherwise return raw ratio."""
    ratio = value / guideline
    return min(ratio, 3) if state == "FL" else ratio

def get_retention_high(table, retention_value, fallback_value):
    # Step 1: Find the matching row
    matching_rows = table.filter(pl.col("Retention - Low") <= retention_value)
    if matching_rows.is_empty():
        return fallback_value  # fallback if no match
    else:
        matched_row = matching_rows[-1]
        return matched_row["Retention - High"].item()

def weighted_sum_with_none_handling(values, weights):
    # Filter out None values
    valid_items = {k: v for k, v in values.items() if v is not None}
    if not valid_items:
        return None  

    # Total weight of valid items
    total_weight = sum(weights[k] for k in valid_items)

    # Normalize weights and compute weighted sum
    return sum((weights[k] / total_weight) * valid_items[k] for k in valid_items)



def rate_change_exposure(hxd, execuguard_package, coverages, expiring_data):
    rc = hxd.cds.rate_change
    qg_summary = hxd.cds.quote_grid_summary
        # expsoure RC calcs 
    if "epl" in coverages:
        expiring_emplyee_count = expiring_data["cds"]["total_ftes"]
        renewal_employee_count = hxd.cds.total_ftes
        rc.exposure_change.epl.model = (renewal_employee_count / expiring_emplyee_count)**.7 if (expiring_emplyee_count and renewal_employee_count) else 1
        rc.exposure_change.epl.selected.calculated = (renewal_employee_count / expiring_emplyee_count)**.7 if (expiring_emplyee_count and renewal_employee_count) else 1

        # indvidual coverage details 
        rc.fte.epl.expiry = expiring_data["cds"]["total_ftes"]
        rc.fte.epl.renewal = hxd.cds.total_ftes
        rc.fte.epl.rate_change = rc.exposure_change.epl.model

    if "fid" in coverages:
        expiring_asstes_contribution = 0 
        expiring_participants = 0 

        for item in expiring_data["cds"]["fid"]["base_premium"]["bp_plans"]:
            expiring_asstes_contribution += item["assets_contributions"] if item["assets_contributions"] else 0
            expiring_participants += item["total_employees_or_members"] if item["total_employees_or_members"] else 0

        renewal_asstes_contribution = 0
        renewal_participants = 0 

        for item in hxd.cds.fid.base_premium.bp_plans:
            renewal_asstes_contribution += item.assets_contributions if item.assets_contributions else 0
            renewal_participants += item.total_employees_or_members if item.total_employees_or_members else 0
        ################################ I'll need to add this to the view############################
        rc.assets.fid.rate_change = (renewal_asstes_contribution / expiring_asstes_contribution)**.2 if expiring_asstes_contribution != 0 else 1
        rc.participants.fid.rate_change = (renewal_participants / expiring_participants)**.5 if expiring_participants != 0 else 1

        rc.exposure_change.fid.model = (rc.assets.fid.rate_change + rc.participants.fid.rate_change) / 2 
        rc.exposure_change.fid.selected.calculated = (rc.assets.fid.rate_change + rc.participants.fid.rate_change) / 2 

        # indvidual coverage details 
        rc.assets.fid.expiry = expiring_asstes_contribution
        rc.assets.fid.renewal = renewal_asstes_contribution
        rc.participants.fid.expiry = expiring_participants
        rc.participants.fid.renewal = renewal_participants
      
    
    if "pcl" in coverages:
        if execuguard_package: 
            rc.assets.pcl.expiry  = expiring_data["cds"]["exposure"]["granular"]["pcl"]["base_rate"]["asset_size"]
            rc.assets.pcl.renewal = hxd.cds.exposure.granular.pcl.base_rate.asset_size

            rc.exposure_change.pcl.model = (rc.assets.pcl.renewal / rc.assets.pcl.expiry )**.2 if (rc.assets.pcl.renewal and rc.assets.pcl.expiry ) else 1
            rc.exposure_change.pcl.selected.calculated = (rc.assets.pcl.renewal / rc.assets.pcl.expiry )**.2 if (rc.assets.pcl.renewal and rc.assets.pcl.expiry ) else 1

            # indvidual coverage details
            rc.assets.pcl.rate_change = rc.exposure_change.pcl.model

        else:
            rc.assets.pcl.expiry = expiring_data["cds"]["exposure"]["granular"]["pcl"]["base_rate"]["asset_size"]
            rc.assets.pcl.renewal = hxd.cds.exposure.granular.pcl.base_rate.asset_size

            rc.assets.pcl.rate_change = (rc.assets.pcl.renewal / rc.assets.pcl.expiry)**.2 if (rc.assets.pcl.renewal and rc.assets.pcl.expiry) else 1

            rc.fte.pcl.expiry = expiring_data["cds"]["us_states"]["Total"]["fte"] + expiring_data["cds"]["us_states"]["Total"]["pte"]
            rc.fte.pcl.renewal = hxd.cds.us_states.Total.fte + hxd.cds.us_states.Total.pte

            rc.fte.pcl.rate_change = (rc.fte.pcl.renewal / rc.fte.pcl.expiry)**.7 if (rc.fte.pcl.expiry and rc.fte.pcl.renewal) else 1

            rc.exposure_change.pcl.model = (rc.assets.pcl.rate_change + rc.fte.pcl.rate_change) / 2
            rc.exposure_change.pcl.selected.calculated  = (rc.assets.pcl.rate_change + rc.fte.pcl.rate_change) / 2

    # if execuguard_package: 
    # Original weights
    weights = {
        'epl': 0.55,
        'fid_assets': 0.05,
        'fid_participants': 0.05,
        'pcl': 0.35
    }

    # Model values
    variables_model = {
        'epl': rc.exposure_change.epl.model,
        'fid_assets': rc.assets.fid.rate_change,
        'fid_participants': rc.participants.fid.rate_change,
        'pcl': rc.exposure_change.pcl.model
    }

    variables_selected = {
        'epl': rc.exposure_change.epl.selected.selected,
        'fid_assets': rc.assets.fid.rate_change,
        'fid_participants': rc.participants.fid.rate_change,
        'pcl': rc.exposure_change.pcl.selected.selected
    }

    # Assign results
    rc.exposure_change.execuguard.model = weighted_sum_with_none_handling(variables_model, weights)
    rc.exposure_change.execuguard.selected.calculated = weighted_sum_with_none_handling(variables_selected, weights)


        # rc.exposure_change.execuguard.model = rc.exposure_change.epl.model * .55 + rc.assets.fid.rate_change * .05 + rc.participants.fid.rate_change * .05 + rc.exposure_change.pcl.model * .35
        # rc.exposure_change.execuguard.selected.calculated = rc.exposure_change.execuguard.model
    # else:
    #     rc.exposure_change.execuguard.model = 1
    #     rc.exposure_change.execuguard.selected.calculated = 1

def rate_change_deductible(hxd, execuguard_package, coverages, expiring_data):
    rc = hxd.cds.rate_change
    qg_summary = hxd.cds.quote_grid_summary

    # constansts
    MAX_RATIO = 3

    if "epl" in coverages:
        # extract data
        exp_limit = expiring_data["cds"]["quote_grid_summary"]["epl"]["limit"]
        exp_ded = expiring_data["cds"]["quote_grid_summary"]["epl"]["retention"]
        ren_limit = hxd.cds.quote_grid_summary.epl.limit
        ren_ded = hxd.cds.quote_grid_summary.epl.retention
        ren_employee_count = hxd.cds.total_ftes

        # guidline ded
        guideline_table = pl.from_pandas(hx.params.table_epl_guideline_deductible)
        
        row = get_matching_row(guideline_table, "Employees Low", ren_employee_count)
        percentage = row["Percentage"].item()
        min_guideline = row["Min"].item()

        exp_guideline_ded = percentage * exp_limit
        ren_guideline_ded = percentage * ren_limit

        exp_ratio_to_guidline = min(MAX_RATIO, exp_ded / exp_guideline_ded)
        ren_ratio_to_guidline = min(MAX_RATIO, ren_ded / ren_guideline_ded)

        # deductible modifier
        ded_modifier_table = pl.from_pandas(hx.params.table_epl_deductible_modifier)

        exp_ratio_low, exp_ratio_high = get_ratios(ded_modifier_table, exp_ratio_to_guidline)
        ren_ratio_low, ren_ratio_high = get_ratios(ded_modifier_table, ren_ratio_to_guidline)
        
        exp_ratio_in_band = interpolate_modifier(exp_ratio_to_guidline, exp_ratio_low, exp_ratio_high, "epl")
        ren_ratio_in_band = interpolate_modifier(ren_ratio_to_guidline, ren_ratio_low, ren_ratio_high, "epl")

        
        # Get low/high factors for interpolation
        exp_low_factor = get_matching_row(ded_modifier_table, "Ratio Low", exp_ratio_low)["Modifier"].item()
        exp_high_factor = get_matching_row(ded_modifier_table, "Ratio Low", exp_ratio_high)["Modifier"].item()
        ren_low_factor = get_matching_row(ded_modifier_table, "Ratio Low", ren_ratio_low)["Modifier"].item()
        ren_high_factor = get_matching_row(ded_modifier_table, "Ratio Low", ren_ratio_high)["Modifier"].item()

        # Final deductible factors
        exp_ded_factor = calculate_ded_factor(exp_ratio_to_guidline, exp_ratio_in_band, exp_low_factor, exp_high_factor)
        ren_ded_factor = calculate_ded_factor(ren_ratio_to_guidline, ren_ratio_in_band, ren_low_factor, ren_high_factor)

        rc.deductible_change.epl.model = ren_ded_factor / exp_ded_factor
        rc.deductible_change.epl.selected.calculated = ren_ded_factor / exp_ded_factor

        # indvidual coverage details 
        rc.ded.epl.expiry = expiring_data["cds"]["quote_grid_summary"]["epl"]["retention"]
        rc.ded.epl.renewal = hxd.cds.quote_grid_summary.epl.retention
        rc.ded.epl.rate_change = rc.deductible_change.epl.model
 
    if "fid" in coverages:
        # extract data
        exp_retention = expiring_data["cds"]["quote_grid_summary"]["fid"]["retention"]
        ren_retention = hxd.cds.quote_grid_summary.fid.retention
        assets_contributions = hxd.cds.fid.base_premium.bp_plans[0].assets_contributions
        
        
        # Calculate guideline retention
        guideline_retention = 50 * (assets_contributions / 1000000)
        guidline_to_use = min(max(guideline_retention, 5000), 100000)

        # Determine state 
        state_ref_table = pl.from_pandas(hx.params.table_reference_state)

        if hxd.cds.standard_fields.is_admitted_or_surplus == "Surplus":
            state_decoded = "surplus"
        else:
            state_decoded = state_ref_table.filter(pl.col("State Name") == hxd.cds.state)["Abbreviation"].item()
        
        # Calculate quote to guidline ratio
        
        exp_quote_guidline_ratio = capped_ratio(exp_retention, guidline_to_use, state_decoded)
        ren_quote_guidline_ratio = capped_ratio(ren_retention, guidline_to_use, state_decoded)

        # get correct lookup table for deductibale modifier 
        if state_decoded == "FL":
            ded_modifier_table = pl.from_pandas(hx.params.table_fid_deductible_modifier_fl)
        elif state_decoded == "ME":
            ded_modifier_table = pl.from_pandas(hx.params.table_fid_deductible_modifier_me)
        else:
            ded_modifier_table = pl.from_pandas(hx.params.table_fid_deductible_modifier_cw)
        
        # Get ratio bands
        exp_ratio_low, exp_ratio_high = get_ratios(ded_modifier_table, exp_quote_guidline_ratio)
        ren_ratio_low, ren_ratio_high = get_ratios(ded_modifier_table, ren_quote_guidline_ratio)

        # calculate revune in band
        exp_ratio_in_band = interpolate_modifier(exp_quote_guidline_ratio, exp_ratio_low, exp_ratio_high, "fid")
        ren_ratio_in_band = interpolate_modifier(ren_quote_guidline_ratio, ren_ratio_low, ren_ratio_high, "fid")

        # calculate factors 
        exp_factor_low = get_matching_row(ded_modifier_table, "Ratio Low", exp_ratio_low)["Factor"].item()
        exp_factor_high = get_matching_row(ded_modifier_table, "Ratio Low", exp_ratio_high)["Factor"].item()
        ren_factor_low = get_matching_row(ded_modifier_table, "Ratio Low", ren_ratio_low)["Factor"].item()
        ren_factor_high = get_matching_row(ded_modifier_table, "Ratio Low", ren_ratio_high)["Factor"].item()


        exp_retention_output = exp_ratio_in_band * exp_factor_high + (1 - exp_ratio_in_band) * exp_factor_low
        ren_retention_output = ren_ratio_in_band * ren_factor_high + (1 - ren_ratio_in_band) * ren_factor_low

        # write to hxd
        rc.deductible_change.fid.model = ren_retention_output / exp_retention_output if exp_retention_output != 0 else 1.0
        rc.deductible_change.fid.selected.calculated = ren_retention_output / exp_retention_output if exp_retention_output != 0 else 1.0

        # indvidual coverage details 
        rc.ded.fid.expiry = expiring_data["cds"]["quote_grid_summary"]["fid"]["retention"]
        rc.ded.fid.renewal = hxd.cds.quote_grid_summary.fid.retention
        rc.ded.fid.rate_change = rc.deductible_change.fid.model
    
    if "pcl" in coverages:
        # extract data
        exp_retention = expiring_data["cds"]["quote_grid_summary"]["pcl"]["retention"]
        ren_retention = hxd.cds.quote_grid_summary.pcl.retention
        assets_size = hxd.cds.exposure.granular.pcl.base_rate.asset_size

        retention_factors = pl.from_pandas(hx.params.table_pcl_retention_factors_cw)

        exp_retention_low = get_matching_row(retention_factors, "Retention - Low", exp_retention)["Retention - Low"].item()
        exp_retention_high = get_retention_high(retention_factors, exp_retention, exp_retention_low)

        ren_retention_low = get_matching_row(retention_factors, "Retention - Low", ren_retention)["Retention - Low"].item()
        ren_retention_high = get_retention_high(retention_factors, ren_retention, ren_retention_low)

        # Determine state 
        state_ref_table = pl.from_pandas(hx.params.table_reference_state)

        if hxd.cds.standard_fields.is_admitted_or_surplus == "Surplus":
            state_decoded = "surplus"
        else:
            state_decoded = state_ref_table.filter(pl.col("State Name") == hxd.cds.state)["Abbreviation"].item()

        # dertermine retention lookup table 
        if state_decoded == "FL":
            retention_lookup_table = pl.from_pandas(hx.params.table_pcl_retention_factors_fl)
        else:
            retention_lookup_table = pl.from_pandas(hx.params.table_pcl_retention_factors_cw)

        pcl_base_rate_table = pl.from_pandas(hx.params.table_pcl_base_rate_ranges_cw)

        asset_size_category = pcl_base_rate_table.filter(pl.col("Min") <= assets_size)[-1]["Asset Size Category Description"].item()

        exp_factor_low = retention_lookup_table.filter(pl.col("Retention - Low") <= exp_retention_low)[-1][asset_size_category].item()
        ren_factor_low = retention_lookup_table.filter(pl.col("Retention - Low") <= ren_retention_low)[-1][asset_size_category].item()
        exp_factor_high = retention_lookup_table.filter(pl.col("Retention - Low") <= exp_retention_high)[-1][asset_size_category].item()
        ren_factor_high = retention_lookup_table.filter(pl.col("Retention - Low") <= ren_retention_high)[-1][asset_size_category].item()

        #calculate retention factors
        if exp_factor_low == exp_factor_high:
            exp_retention_factor = exp_factor_low
        else:
            exp_retention_factor = exp_factor_low + (((exp_retention - exp_retention_low) / (exp_retention_high - exp_retention_low)) * (exp_factor_high - exp_factor_low))
        
        if ren_factor_low == ren_factor_high:
            ren_retention_factor = ren_factor_low
        else:
            ren_retention_factor = ren_factor_low + (((ren_retention - ren_retention_low) / (ren_retention_high - ren_retention_low)) * (ren_factor_high - ren_factor_low))

        # write to hxd
        rc.deductible_change.pcl.model = ren_retention_factor / exp_retention_factor
        rc.deductible_change.pcl.selected.calculated = ren_retention_factor / exp_retention_factor

        # indvidual coverage details 
        rc.ded.pcl.expiry = expiring_data["cds"]["quote_grid_summary"]["pcl"]["retention"]
        rc.ded.pcl.renewal = hxd.cds.quote_grid_summary.pcl.retention
        rc.ded.pcl.rate_change = rc.deductible_change.pcl.model
    
    # write execuguard package data 
    weights = {
        'epl': 0.55,
        'fid': 0.1,
        'pcl': 0.35
    }

    # Model values
    variables_model = {
        'epl': rc.deductible_change.epl.model,
        'fid': rc.deductible_change.fid.model,
        'pcl': rc.deductible_change.pcl.model
    }
    variables_selected = {
        'epl': rc.deductible_change.epl.selected.selected,
        'fid': rc.deductible_change.fid.selected.selected,
        'pcl': rc.deductible_change.pcl.selected.selected
    }

    # Assign results
    rc.deductible_change.execuguard.model = weighted_sum_with_none_handling(variables_model, weights)
    rc.deductible_change.execuguard.selected.calculated = weighted_sum_with_none_handling(variables_selected, weights)

def rate_change_limit(hxd, execuguard_package, coverages, expiring_data):
    rc = hxd.cds.rate_change
    qg_summary = hxd.cds.quote_grid_summary
    # calcualte Limit RC component 
    if "epl" in coverages:
        # extract data
        exp_limit = expiring_data["cds"]["quote_grid_summary"]["epl"]["limit"]
        ren_limit = hxd.cds.quote_grid_summary.epl.limit

        epl_ilfs_table = pl.from_pandas(hx.params.table_epl_ilf)

        exp_limit_low = epl_ilfs_table.filter(pl.col("Limit Low") <= exp_limit)[-1]["Limit Low"].item()
        ren_limit_low = epl_ilfs_table.filter(pl.col("Limit Low") <= ren_limit)[-1]["Limit Low"].item()
        exp_limit_high = epl_ilfs_table.filter(pl.col("Limit Low") <= exp_limit)[-1]["Limit High"].item()
        ren_limit_high = epl_ilfs_table.filter(pl.col("Limit Low") <= ren_limit)[-1]["Limit High"].item()

        exp_ratio_in_band = (exp_limit - exp_limit_low) /(exp_limit_high - exp_limit_low) if (exp_limit_high - exp_limit_low) not in [0, None] else 1
        ren_ratio_in_band = (ren_limit - ren_limit_low) /(ren_limit_high - ren_limit_low) if (ren_limit_high - ren_limit_low) not in [0, None] else 1

        exp_factor_low = epl_ilfs_table.filter(pl.col("Limit Low") <= exp_limit_low)[-1]["Factor"].item()
        ren_factor_low = epl_ilfs_table.filter(pl.col("Limit Low") <= ren_limit_low)[-1]["Factor"].item()
        exp_factor_high = epl_ilfs_table.filter(pl.col("Limit Low") <= exp_limit_high)[-1]["Factor"].item()
        ren_factor_high = epl_ilfs_table.filter(pl.col("Limit Low") <= ren_limit_high)[-1]["Factor"].item()

        exp_lim_factor = exp_ratio_in_band * exp_factor_high + (1 - exp_ratio_in_band) * exp_factor_low
        ren_lim_factor = ren_ratio_in_band * ren_factor_high + (1 - ren_ratio_in_band) * ren_factor_low

        rc.limit_change.epl.model = ren_lim_factor / exp_lim_factor
        rc.limit_change.epl.selected.calculated = ren_lim_factor / exp_lim_factor

        # indvidual coverage details 
        rc.limit.epl.expiry = expiring_data["cds"]["quote_grid_summary"]["epl"]["limit"]
        rc.limit.epl.renewal = hxd.cds.quote_grid_summary.epl.limit
        rc.limit.epl.rate_change = rc.limit_change.epl.model

    if "fid" in coverages:
        exp_limit = expiring_data["cds"]["quote_grid_summary"]["fid"]["limit"]
        ren_limit = hxd.cds.quote_grid_summary.fid.limit

        # get correct lookup table 
        if hxd.cds.fid.employer_type == "Single Employer":
            ilf_table = pl.from_pandas(hx.params.table_fid_single_ilf)
        else:
            ilf_table = pl.from_pandas(hx.params.table_fid_multi_ilf)

        # get low and high limit 
        exp_limit_low = ilf_table.filter(pl.col("Limit Low") <= exp_limit)[-1]["Limit Low"].item()
        ren_limit_low = ilf_table.filter(pl.col("Limit Low") <= ren_limit)[-1]["Limit Low"].item()
        exp_limit_high = ilf_table.filter(pl.col("Limit Low") <= exp_limit)[-1]["Limit High"].item()
        ren_limit_high = ilf_table.filter(pl.col("Limit Low") <= ren_limit)[-1]["Limit High"].item()

        exp_ratio_in_band = (exp_limit - exp_limit_low) / (exp_limit_high - exp_limit_low) if (exp_limit_high - exp_limit_low) not in [0, None] else 1  
        ren_ratio_in_band = (ren_limit - ren_limit_low) / (ren_limit_high - ren_limit_low) if (ren_limit_high - ren_limit_low) not in [0, None] else 1

        exp_factor_low = ilf_table.filter(pl.col("Limit Low") <= exp_limit_low)[-1]["Factor"].item()
        ren_factor_low = ilf_table.filter(pl.col("Limit Low") <= ren_limit_low)[-1]["Factor"].item()
        exp_factor_high = ilf_table.filter(pl.col("Limit Low") <= exp_limit_high)[-1]["Factor"].item()
        ren_factor_high = ilf_table.filter(pl.col("Limit Low") <= ren_limit_high)[-1]["Factor"].item()

        exp_limit_factor = exp_ratio_in_band * exp_factor_high + (1 - exp_ratio_in_band) * exp_factor_low
        ren_limit_factor = ren_ratio_in_band * ren_factor_high + (1 - ren_ratio_in_band) * ren_factor_low

        rc.limit_change.fid.model = ren_limit_factor / exp_limit_factor
        rc.limit_change.fid.selected.calculated = ren_limit_factor / exp_limit_factor

        # indvidual coverage details 
        rc.limit.fid.expiry = expiring_data["cds"]["quote_grid_summary"]["fid"]["limit"]
        rc.limit.fid.renewal = hxd.cds.quote_grid_summary.fid.limit
        rc.limit.fid.rate_change = rc.limit_change.fid.model
 
    if "pcl" in coverages:
        exp_limit = expiring_data["cds"]["quote_grid_summary"]["pcl"]["limit"]
        ren_limit = hxd.cds.quote_grid_summary.pcl.limit

        pcl_limit_factor_table = pl.from_pandas(hx.params.table_pcl_limit_factors_cw)
        
        #get limits 
        exp_limit_low = pcl_limit_factor_table.filter(pl.col("Limit - low") <= exp_limit)[-1]["Limit - low"].item()
        ren_limit_low = pcl_limit_factor_table.filter(pl.col("Limit - low") <= ren_limit)[-1]["Limit - low"].item()
        exp_limit_high = pcl_limit_factor_table.filter(pl.col("Limit - low") <= exp_limit)[-1]["Limit - High"].item()
        ren_limit_high = pcl_limit_factor_table.filter(pl.col("Limit - low") <= ren_limit)[-1]["Limit - High"].item()

        # get factors
        exp_factor_low = pcl_limit_factor_table.filter(pl.col("Limit - low") <= exp_limit_low)[-1]["Factor"].item()
        ren_factor_low = pcl_limit_factor_table.filter(pl.col("Limit - low") <= ren_limit_low)[-1]["Factor"].item()
        exp_factor_high = pcl_limit_factor_table.filter(pl.col("Limit - low") <= exp_limit_high)[-1]["Factor"].item()
        ren_factor_high = pcl_limit_factor_table.filter(pl.col("Limit - low") <= ren_limit_high)[-1]["Factor"].item()
        
        #calcualte lim factors
        if exp_factor_low == exp_factor_high:
            exp_limit_factor = exp_factor_low
        else:
            exp_limit_factor = exp_factor_low + ((exp_limit - exp_limit_low) / (exp_limit_high - exp_limit_low)) * (exp_factor_high - exp_factor_low)
        
        if ren_factor_low == ren_factor_high:
            ren_limit_factor = ren_factor_low
        else:
            ren_limit_factor = ren_factor_low + ((ren_limit - ren_limit_low) / (ren_limit_high - ren_limit_low)) * (ren_factor_high - ren_factor_low)

        # write to hxd
        rc.limit_change.pcl.model = ren_limit_factor / exp_limit_factor
        rc.limit_change.pcl.selected.calculated = ren_limit_factor / exp_limit_factor

        # indvidual coverage details 
        rc.limit.pcl.expiry = expiring_data["cds"]["quote_grid_summary"]["pcl"]["limit"]
        rc.limit.pcl.renewal = hxd.cds.quote_grid_summary.pcl.limit
        rc.limit.pcl.rate_change = rc.limit_change.pcl.model

        rc.limit_change.pcl.model = ren_limit_factor / exp_limit_factor
        rc.limit_change.pcl.selected.calculated = ren_limit_factor / exp_limit_factor

    # calculate execuguard RC 
    weights = {
        'epl': 0.55,
        'fid': 0.1,
        'pcl': 0.35
    }

    # Model values
    variables_model = {
        'epl': rc.limit_change.epl.model,
        'fid': rc.limit_change.fid.model,
        'pcl': rc.limit_change.pcl.model
    }
    variables_selected = {
        'epl': rc.limit_change.epl.selected.selected,
        'fid': rc.limit_change.fid.selected.selected,
        'pcl': rc.limit_change.pcl.selected.selected
    }

    # Assign results
    rc.limit_change.execuguard.model = weighted_sum_with_none_handling(variables_model, weights)
    rc.limit_change.execuguard.selected.calculated = weighted_sum_with_none_handling(variables_selected, weights)

def rate_rate_change(hxd):
    rc = hxd.cds.rate_change
    excess_rc = hxd.cds.excess_rate_change
    # show hide RC and excess RC pages 
    if hxd.cds.standard_fields.is_renewal:
        if hxd.cds.layers[0].is_primary_excess == "Primary":
            rc.show_hide_rc = True
        else: 
            excess_rc.show_hide_excess_rc = True
    else:
        rc.show_hide_rc = False
        excess_rc.show_hide_excess_rc = False
    

    # Get the Renewed Premium Amount
    if hxd.cds.rate_change.expiring_policy_option_id.selected is None:
        rc.rarc_run_again_message = "❗Please enter a Expiring Policy Option and Run the Rate Change Calculations ❗"
        rc.rarc_message_show = True
    else:
        if hxd.cds.final_premium_summary.pre_rounding_admitted_premium +  hxd.cds.final_premium_summary.post_rounding_admitted_premium != rc.check_if_prem_changed:
            rc.rarc_run_again_message = "❗Premiums have changed. Run the rate change calculation again ❗"
            rc.rarc_message_show = True
        else:
            rc.rarc_message_show = False

    # if is_bm_different and is_quoted_different:
    #     rc.rarc_run_again_message = "❗ Benchmark and quoted premiums have changed. Run the rate change calculation again ❗"
    #     rc.rarc_message_show = True
    # elif is_bm_different:
    #     rc.rarc_run_again_message = f"❗ Benchmark premium has changed on Layer {idx+1}. Run the rate change calculation again ❗"
    #     rc.rarc_message_show = True
    # elif is_quoted_different:
    #     rc.rarc_run_again_message = f"❗ Quoted premium has changed on Layer {idx+1}. Run the rate change calculation again ❗"
    #     rc.rarc_message_show = True

    # if is_bm_different or is_quoted_different:
    #     hx.errors.validation("'Calculate Rate Change' in the Rate Change page must be run again.")