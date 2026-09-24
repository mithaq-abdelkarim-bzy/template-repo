import hx
import numpy as np
import pandas as pd
import algorithms.rate_utilities as utils
import algorithms.validations.premium_and_limit_profile_validations as validations


def calculate_bst_share_ultimate_gross_premium(prem_limit_profile_df):
    # Multiply future ultimate gross premium by BST share line size, unless either input is null
    prem_limit_profile_df['bst_share_ultimate_gross_premium'] = np.where(
        prem_limit_profile_df[['future_ultimate_gross_prem', 'bst_share_line_size']].isnull().any(axis=1),
        np.nan, 
        prem_limit_profile_df['future_ultimate_gross_prem'] * prem_limit_profile_df['bst_share_line_size']
    )
    return prem_limit_profile_df


def init_prem_limit_profile_df(prem_limit_profile_path, rater):
    # Load existing profile table into DataFrame
    rcc_final_composition_df = rater.get("risk_composition_final", pd.DataFrame())
    prem_limit_profile_df    = rater.get("prem_limit_data",      pd.DataFrame())

    # Remove duplicates at facility level
    rcc_final_composition_df = rcc_final_composition_df.drop_duplicates(subset=['facility_lob']) 
    no_of_rows = rcc_final_composition_df.shape[0]

    # Map composition attributes into profile table
    prem_limit_profile_df.loc[:no_of_rows - 1, ['lob/calculated', 'selected_lob/calculated', 'assigned_trifocus/calculated']] = \
        rcc_final_composition_df[['facility_lob', 'selected_lob', 'selected_trifocus']].values

    # Apply overrides if present, otherwise keep calculated values
    for base in ["lob", "selected_lob", "assigned_trifocus"]:
        prem_limit_profile_df[base] = np.where(
            prem_limit_profile_df[f"{base}/is_overridden"],
            prem_limit_profile_df[base],
            prem_limit_profile_df[f"{base}/calculated"]
        )

    # Mark visible rows only where selected LOB exists
    prem_limit_profile_df["is_row_visible"] = prem_limit_profile_df["selected_lob"].notna()

    # Run validation checks on critical fields
    apply_validations(prem_limit_profile_df)

    return prem_limit_profile_df


def apply_validations(prem_limit_profile_df):
    # Drop rows with missing LOB
    prem_limit_profile_df = prem_limit_profile_df[prem_limit_profile_df["lob"].notna()]

    max_limit_at_100_per        = prem_limit_profile_df["max_limit_at_100_per"]
    max_limit_at_bst_share      = prem_limit_profile_df["max_limit_at_bst_share"]    
    future_ultimate_gross_prem  = prem_limit_profile_df["future_ultimate_gross_prem"]
    bst_share_line_size         = prem_limit_profile_df["bst_share_line_size"]

    # Ensure key limit and premium fields pass validation checks
    validations.check_max_limit_at_100_per_value(       max_limit_at_100_per,       bst_share_line_size)
    validations.check_max_limit_at_bst_share_value(     max_limit_at_bst_share,     bst_share_line_size)
    validations.check_future_ultimate_gross_prem_value( future_ultimate_gross_prem, bst_share_line_size)


def calculate_bst_share_line_size(prem_limit_profile_df):
    # Ratio of limit at BST share to limit at 100%
    prem_limit_profile_df['bst_share_line_size/calculated'] = np.where(
        prem_limit_profile_df[['max_limit_at_bst_share', 'max_limit_at_100_per']].isnull().any(axis=1),
        np.nan,
        prem_limit_profile_df['max_limit_at_bst_share'] / prem_limit_profile_df['max_limit_at_100_per']        
    )

    # Use override if available
    prem_limit_profile_df['bst_share_line_size'] = np.where(
        prem_limit_profile_df['bst_share_line_size/is_overridden'],
        prem_limit_profile_df['bst_share_line_size'],
        prem_limit_profile_df['bst_share_line_size/calculated']
    )

    # Replace NaN values with 0
    prem_limit_profile_df['bst_share_line_size'] = prem_limit_profile_df['bst_share_line_size'].fillna(0)

    return prem_limit_profile_df


def calculate_bst_deductions(prem_limit_profile_df, deductions_df):
    # Map selected LOBs to effective deductions
    lob_deduction_map = dict(zip(deductions_df['selected_lob'], deductions_df['selected_effective_deductions']))

    # Assign mapped deductions, default to 0 if no mapping
    prem_limit_profile_df['bst_deductions'] = prem_limit_profile_df['selected_lob'].replace(lob_deduction_map).fillna(0)

    return prem_limit_profile_df


def calculate_bst_net_premium(prem_limit_profile_df):
    # Multiply BST gross premium by (1 - deductions), unless inputs are null
    prem_limit_profile_df['bst_net_premium/calculated'] = np.where(
        prem_limit_profile_df[['future_ultimate_gross_prem', 'bst_share_line_size']].isnull().any(axis=1),
        np.nan,
        prem_limit_profile_df['bst_share_ultimate_gross_premium'] * (1 - prem_limit_profile_df['bst_deductions'])
    )

    # Apply overrides if available
    prem_limit_profile_df['bst_net_premium'] = np.where(
        prem_limit_profile_df['bst_net_premium/is_overridden'],
        prem_limit_profile_df['bst_net_premium'],
        prem_limit_profile_df['bst_net_premium/calculated'],
    )

    return prem_limit_profile_df


def calculate_limit_profile_summary(prem_limit_profile_df, prem_limit_profile_path):
    # Metrics to aggregate by mean, max, or sum
    columns_to_mean = ["avg_attachment_point", "primary"]
    columns_to_max = ["max_limit_at_100_per", "avg_limit_at_100_per", "max_limit_at_bst_share"]
    columns_to_sum = ["future_ultimate_gross_prem", "bst_share_ultimate_gross_premium", "bst_net_premium"]
    all_cols = columns_to_mean + columns_to_max + columns_to_sum + ['bst_share_line_size', 'bst_deductions']

    limit_profile_sum_dict = {}
    prem_limit_profile_df = prem_limit_profile_df[prem_limit_profile_df['selected_lob'].notna()]

    # Aggregate sums
    for column in columns_to_sum:
        limit_profile_sum_dict[column] = prem_limit_profile_df[column].fillna(0).sum(skipna=True)

    # Aggregate max
    for column in columns_to_max:
        limit_profile_sum_dict[column] = prem_limit_profile_df[column].fillna(0).max(skipna=True)

    # Aggregate mean
    for column in columns_to_mean:
        limit_profile_sum_dict[column] = prem_limit_profile_df[column].fillna(0).mean(skipna=True)

    # Compute weighted BST line size
    limit_profile_sum_dict['bst_share_line_size'] = (
        limit_profile_sum_dict['bst_share_ultimate_gross_premium'] 
        / limit_profile_sum_dict['future_ultimate_gross_prem'] 
        if limit_profile_sum_dict['future_ultimate_gross_prem'] != 0 
        else 0
    )

    # Weighted average of BST deductions
    numerator = (prem_limit_profile_df["bst_deductions"] * prem_limit_profile_df["bst_share_ultimate_gross_premium"]).sum(skipna=True)
    denominator = prem_limit_profile_df["bst_share_ultimate_gross_premium"].sum(skipna=True)
    limit_profile_sum_dict["bst_deductions"] = numerator / denominator if denominator else None

    # Save back into summary structure    
    prem_limit_profile_path.summary = limit_profile_sum_dict

    return limit_profile_sum_dict


def calculate_portfolio_composition(prem_limit_profile_df, limit_profile_sum_dict):
    # Compute relative share of each row's net premium in the portfolio
    sum_bst_net_premium = limit_profile_sum_dict['bst_net_premium']

    if sum_bst_net_premium is None or sum_bst_net_premium == 0 or np.isnan(sum_bst_net_premium):
        prem_limit_profile_df['portfolio_composition/calculated'] = 0
    else:
        prem_limit_profile_df['portfolio_composition/calculated'] = (
            prem_limit_profile_df['bst_net_premium'] 
            / sum_bst_net_premium
        ).fillna(0)

    # Apply overrides if available
    prem_limit_profile_df['portfolio_composition'] = np.where(
        prem_limit_profile_df['portfolio_composition/is_overridden'],
        prem_limit_profile_df['portfolio_composition'],
        prem_limit_profile_df['portfolio_composition/calculated']
    )

    return prem_limit_profile_df


def calculate_portfolio_composition_sum(prem_limit_profile_df, prem_limit_profile_path):
    # Total sum of all portfolio composition values
    sum_portfolio_composition = prem_limit_profile_df['portfolio_composition'].sum(skipna=True)
    setattr(prem_limit_profile_path.summary, "portfolio_composition", sum_portfolio_composition)