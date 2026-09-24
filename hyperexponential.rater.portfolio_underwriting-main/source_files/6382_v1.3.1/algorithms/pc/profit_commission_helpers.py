import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
import algorithms.rate_constants as constants


def build_profit_commission_summary(hxd, profit_commission_df, sim_loss_df):
    # Paths to profit commission summary and calculation summary
    summary_path = hxd.cds.pc.profit_commission.summary
    pc_calc_summary = hxd.cds.pc.pc_calculations.summary

    # Fields to aggregate across LOBs
    fields_to_sum = [
        'gwp_5623', 
        'deductions', 
        'nwp_5623', 
        'total_losses',
        'uw_expense', 
        'dcf', 
        'expected_pl', 
        'pc_on_binders',
        'pc_on_contract', 
        'nwp_after_pc',
        'total_gn_ulr_pre', 
        'total_gn_ulr_post'
    ]

    # Initialize summary dict
    summary = {}
    df = profit_commission_df.fillna(0)

    # Sum over all required fields
    for field in fields_to_sum:
        summary[field] = df[field].sum()

    # Sum expected loss components (attritional, large, catastrophe)
    sum_el = 0
    for field in ["attr_el", "large_el", "cat_non_weather_el", "cat_weather_el"]:
        sum_el += getattr(pc_calc_summary, field) 

    # Calculate gross/net ULR pre-PC
    if summary["nwp_5623"] == 0:
        summary["total_gn_ulr_pre"] = 0
    else:
        summary["total_gn_ulr_pre"] = sum_el / summary["nwp_5623"]

    # Calculate gross/net ULR post-PC
    if summary["nwp_after_pc"] == 0:
        summary["total_gn_ulr_post"] = 0 
    else:
        summary["total_gn_ulr_post"] = sum_el / summary["nwp_after_pc"]

    # Capture total PC impact from simulation output
    summary["pc_impact"] = sim_loss_df["pc_impact_tot_interlock"].iloc[0]

    # Write results back to HXD summary path
    for col in fields_to_sum + ["pc_impact"]:
        setattr(summary_path, col, summary[col])


def build_profit_commission_df(hxd, pc_calc_df, pc_structure_df, sim_loss_df, dcf_df):
    # Path to profit commission output
    profit_commission_path = hxd.cds.pc.profit_commission

    # Drop rows without selected LOB in each input DataFrame
    pc_calc_df = pc_calc_df[pc_calc_df["selected_lob"].notna()]
    pc_structure_df = pc_structure_df[pc_structure_df["selected_lob"].notna()]
    sim_loss_df = sim_loss_df[sim_loss_df["selected_lob"].notna()]
    sim_loss_df = sim_loss_df[[
        "selected_lob", 
        "avg_contract_total", 
        "avg_contract_p_l", 
        "avg_binder_pc", 
        "avg_total_pc_scaled", 
        "pc_impact_scaled"
    ]]
    dcf_df = dcf_df[dcf_df["selected_lob"].notna()]

    # Initialize profit commission DataFrame with required LOB rows
    profit_commission_df = pc_calc_df[['selected_lob']].copy()

    # Flag rows as visible if LOB is set
    profit_commission_df['is_row_visible'] = profit_commission_df['selected_lob'].notna()

    # Keep only visible rows
    profit_commission_df = profit_commission_df[profit_commission_df["selected_lob"].notna()]

    # Merge simulation losses onto PC DataFrame
    profit_commission_df = profit_commission_df.merge(sim_loss_df, on='selected_lob', how='left')

    # Add best estimate before PC adjustment
    profit_commission_df['best_estimate_pre_pc_adj'] = pc_calc_df['best_estimate_pre_pc_adj']

    # Gross written premium
    profit_commission_df['gwp_5623'] = pc_calc_df['gwp_5623']

    # Deductions = gross premium × deductions factor
    profit_commission_df['deductions'] = pc_calc_df['gwp_5623'] * pc_calc_df['deductions']

    # Net written premium = gross − deductions
    profit_commission_df['nwp_5623'] = (
        profit_commission_df['gwp_5623'] 
        - profit_commission_df['deductions']
    )

    # Total simulated losses
    profit_commission_df['total_losses'] = profit_commission_df['avg_contract_total'].fillna(0)
    
    # Underwriting expense based on expense basis
    profit_commission_df['uw_expense'] = np.where(
        pc_structure_df["expense_basis"] == "Gross Premium",
        pc_structure_df["uw_expense"] * profit_commission_df["gwp_5623"],
        pc_structure_df["uw_expense"] * profit_commission_df["nwp_5623"]
    )
    profit_commission_df['uw_expense'] = profit_commission_df['uw_expense'].fillna(0)

    # Deficit carry forward from prior results
    profit_commission_df['dcf'] = dcf_df["dcf"]

    # Expected profit/loss
    profit_commission_df['expected_pl'] = profit_commission_df['avg_contract_p_l'].fillna(0)

    # Profit commission on binders
    profit_commission_df['pc_on_binders'] = profit_commission_df['avg_binder_pc'].fillna(0)

    # Profit commission on contracts
    profit_commission_df['pc_on_contract'] = profit_commission_df['avg_total_pc_scaled'].fillna(0)

    # Net written premium after deducting profit commission
    profit_commission_df['nwp_after_pc'] = (
        profit_commission_df['nwp_5623'] 
        - profit_commission_df['pc_on_contract']
    )

    # Calculate sum of expected losses for ULR
    pc_calc_df['sum_el'] = ( 
        pc_calc_df['attr_el'] 
        + pc_calc_df['large_el']
        + pc_calc_df['cat_non_weather_el']
        + pc_calc_df['cat_weather_el']
    )

    # Total gross/net ULR before PC
    profit_commission_df['total_gn_ulr_pre'] = np.where(
        profit_commission_df["nwp_5623"] == 0,
        0,
        pc_calc_df['sum_el'] / profit_commission_df["nwp_5623"]
    )

    # Profit commission impact per LOB
    profit_commission_df['pc_impact'] = profit_commission_df["pc_impact_scaled"].fillna(0)

    # Total gross/net ULR after PC
    profit_commission_df['total_gn_ulr_post'] = (
        profit_commission_df['pc_impact'] 
        + profit_commission_df['total_gn_ulr_pre']
    )

    # Columns required for final output
    req_cols = [
        'selected_lob', 
        'gwp_5623', 
        'deductions', 
        'nwp_5623', 
        'total_losses',
        'uw_expense', 
        'dcf', 
        'expected_pl', 
        'pc_on_binders',
        'pc_on_contract', 
        'nwp_after_pc', 
        'total_gn_ulr_pre', 
        'total_gn_ulr_post',
        'pc_impact', 
        'best_estimate_pre_pc_adj',
        'is_row_visible'
    ]

    # Filter DataFrame to required columns
    filtered_profit_commission_df = profit_commission_df[req_cols]

    # Save detailed PC results back to HXD
    hxd.cds.pc.profit_commission.details = filtered_profit_commission_df.to_dict(orient='records')

    return profit_commission_df