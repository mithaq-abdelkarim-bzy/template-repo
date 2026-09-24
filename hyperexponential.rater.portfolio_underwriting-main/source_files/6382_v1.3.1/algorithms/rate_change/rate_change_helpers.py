import pandas as pd
import numpy as np
import algorithms.rate_utilities as utils
from algorithms import rate_constants as constants
from algorithms.risk_information.risk_information_helpers import import_inception_date


def calculate_past_years_rate_change(hxd, rater, rate_change_df, years_dict):
 
    portfolio_profile_summary_df = rater.get("portfolio_profile_summary", pd.DataFrame())
    
    # Iterate over all years except the most recent
    for year in list(years_dict.values())[1:]:
        # Map achieved rate change from portfolio profile summary
        rate_change_df[f'{year}/beazley_group_achieved'] = rate_change_df['selected_lob'].map(
            dict(zip(
                portfolio_profile_summary_df['selected_lob'],
                portfolio_profile_summary_df[f'rate_change_no_override/{year}']
            ))
        )

        # Replace NaN values with None       
        rate_change_df[f'{year}/beazley_group_achieved'] = np.where(
            np.isnan(rate_change_df[f'{year}/beazley_group_achieved']),
            None,
            rate_change_df[f'{year}/beazley_group_achieved']
        )

        # Select final rate change: use facility if available, else achieved
        rate_change_df[f'{year}/selected'] = np.where(
            rate_change_df[f'{year}/facility'].isnull(),
            rate_change_df[f'{year}/beazley_group_achieved'],
            rate_change_df[f'{year}/facility']
        )

    # Calculate years to process
    years_to_process = list(years_dict.values())[1:]

    # Build the list of column names explicitly
    columns_to_write = []
    for year in years_to_process:
        columns_to_write.append(f'{year}/beazley_group_achieved')
        columns_to_write.append(f'{year}/selected')
    
    # Pass to rater (not hxd)
    rater['rate_change_data'] = rate_change_df

    # Calculate summary
    for year in list(years_dict.values())[1:]:
        rate_change_df[f'{year}/selected_implied_expiry'] = utils.ratio(rate_change_df["bst_net_premium"], rate_change_df[f'{year}/selected'].fillna(1))
        rate_change_df[f'{year}/facility_implied_expiry'] = utils.ratio(rate_change_df["bst_net_premium"], rate_change_df[f'{year}/facility'].fillna(1))
        rate_change_df[f'{year}/beazley_implied_expiry'] = utils.ratio(rate_change_df["bst_net_premium"], rate_change_df[f'{year}/beazley_group_achieved'].fillna(1))
    
    summary_df = calculate_rate_change_past_years_summary(rate_change_df, years_dict)
    summary_cols = ["selected", "facility", "beazley_group_achieved"]

    for col in summary_cols:
        for year in list(years_dict.values())[1:]:
            setattr(
                getattr(hxd.cds.rate_change_summary, str(year)),
                col,
                summary_df[f'{year}/{col}'].iloc[0]
            )

    return rate_change_df


def set_facility_columns_headers(hxd, years_dict):
    # Assign readable facility labels for each year
    for year, column_name in years_dict.items():
        setattr(
            getattr(hxd.non_cds.rate_change, str(column_name)),
            "facility",
            f"{year} Facility"
        )


def calculate_current_year_rate_change(hxd, rater, rate_change_df):
    
    bp_projections_bp_summary_by_lob_df = rater.get("bp_summary_by_lob", pd.DataFrame())
    
    # Create mappings for rate change and margin by lob
    rate_change_mapping = dict(zip(
        bp_projections_bp_summary_by_lob_df['selected_lob'],
        bp_projections_bp_summary_by_lob_df['attr_rate_change']
    ))
    rarc_margin_mapping = dict(zip(
        bp_projections_bp_summary_by_lob_df['selected_lob'],
        bp_projections_bp_summary_by_lob_df['attr_rarc_margin']
    ))

    # Calculate bp_rate_change and bp_rarc_margin for current year
    rate_change_df['year_0/bp_rate_change'] = rate_change_df['selected_lob'].map(
        rate_change_mapping
    ).fillna(0) + 1
    rate_change_df['year_0/bp_rarc_margin'] = rate_change_df['selected_lob'].map(
        rarc_margin_mapping
    ).fillna(0)

    # Calculate blended effective rate change
    rate_change_df['year_0/blend_effective_rate_change'] = (
        0.5 * rate_change_df['year_0/facility'].fillna(0) +
        0.5 * rate_change_df['year_0/bp_rate_change'].fillna(0) / (
            1 + rate_change_df['year_0/bp_rarc_margin'].replace(-1, np.nan).fillna(0))
    )

    # Fill NaNs in key columns with 0
    cols_to_fill = [
        'year_0/blend_effective_rate_change',
        'year_0/bp_rate_change',
        'year_0/bp_rarc_margin'
    ]
  
    rate_change_df[cols_to_fill] = rate_change_df[cols_to_fill].fillna(0)

    # Define mapping logic for selected source
    conditions = [
        rate_change_df['year_0/source'] == 'Blend',
        rate_change_df['year_0/source'] == 'Business Plan',
        rate_change_df['year_0/source'] == 'Facility'
    ]
    choices = [
        rate_change_df['year_0/blend_effective_rate_change'],
        rate_change_df['year_0/bp_rate_change'] / (1 + rate_change_df['year_0/bp_rarc_margin']),
        np.where(rate_change_df['year_0/facility'].isna(), 1, rate_change_df['year_0/facility'])
    ]

    # Select final value for year_0
    rate_change_df['year_0/selected'] = np.select(conditions, choices, default=1)

    # Pass to rater (not hxd)
    rater['rate_change_data'] = rate_change_df

    # Calculate summary
    rate_change_df["selected_implied_expiry"] = utils.ratio(rate_change_df["bst_net_premium"], rate_change_df['year_0/selected'].fillna(1))
    rate_change_df["facility_implied_expiry"] = utils.ratio(rate_change_df["bst_net_premium"], rate_change_df['year_0/facility'].fillna(1))
    rate_change_df["bp_implied_expiry"] = utils.ratio(rate_change_df["bst_net_premium"], rate_change_df['year_0/bp_rate_change'].fillna(1))
    rate_change_df["bp_rarc_margin_implied_expiry"] = utils.ratio(
        rate_change_df["bst_net_premium"] * (1 + rate_change_df['year_0/bp_rarc_margin'].fillna(0)), 
        rate_change_df['year_0/bp_rate_change'].fillna(1) 
    )

    summary_df = rate_change_current_year_summary(rate_change_df)
    summary_cols = ["selected", "facility", "bp_rate_change", "bp_rarc_margin"]

    for col in summary_cols:
        setattr(
        hxd.cds.rate_change_summary.year_0,
        col,
        summary_df[col].iloc[0]
            )

    hxd.cds.rate_change_summary.year_0.bp_rarc_margin_info = "Total calculated after applying the RARC margin to the Plan Rate Change"

    return rate_change_df


def generate_years_dict(hxd):
    # Get inception year from hxd
    inception_date = import_inception_date(hxd)
    inception_year = inception_date.year

    # Map years to "year_i" style labels
    return {
        str(inception_year - i): f"year_{i}"
        for i in range(constants.YEARS_TO_CONSIDER_IN_RATE_CHANGE)
    }


def init_rate_change(hxd, rater, non_cds_rcc, years_dict):
   
    # Remove duplicates in final composition by line of business
    rcc_final_composition_df = rater["risk_composition_final"]
    rcc_final_composition_df = rcc_final_composition_df.drop_duplicates( subset=['selected_lob']  )
    rcc_final_no_of_rows = rcc_final_composition_df.shape[0]

    # Load existing rate change DataFrame
    rate_change_df = rater.get("rate_change_data", pd.DataFrame())

    # Fill key lob-related fields from final composition
    rate_change_df.loc[:rcc_final_no_of_rows - 1, ['selected_lob', 'dominant_risk_code', 'bp_class']] = (
            rcc_final_composition_df[    ['selected_lob', 'risk_code', 'selected_bp_class']   ].values    )

    # Add pricing year premiums to rate change table to calculate summary
    prem_limit_df = rater.get("prem_limit_data",   pd.DataFrame())

    prem_limit_agg = (
        prem_limit_df
        .groupby("selected_lob", as_index=False)
        ["bst_net_premium"]
        .sum()
    )

    rate_change_df = rate_change_df.merge(
        prem_limit_agg,
        on="selected_lob",
        how="left"
    )

    # Mark rows as visible if lob exists
    rate_change_df["is_row_visible"] = rate_change_df["selected_lob"].notna()

    # Add year values into yoa columns
    """ NK: Could pre-build a dict and do rate_change_df.assign(**dict) instead of looping.
    # Build dict of all new columns in one go
    yoa_cols = {f"{col}/yoa": year for year, col in years_dict.items()}

    # Assign them all at once
    rate_change_df = rate_change_df.assign(**yoa_cols)
    """
    #JF: I think this is easy enough to read
    for year, column_name in years_dict.items():
        rate_change_df[f'{column_name}/yoa'] = year

    # Pass to rater (not hxd)
    rater['rate_change_data'] = rate_change_df

    return rate_change_df


def rate_change_current_year_summary(rate_change_df):
    total_cols = ["selected_implied_expiry", "facility_implied_expiry", "bp_implied_expiry", "bp_rarc_margin_implied_expiry", "bst_net_premium"]

    out = pd.DataFrame([{
        c: rate_change_df[c].sum()
        for c in total_cols
    }])

    out["selected"] = utils.ratio(out["bst_net_premium"], out["selected_implied_expiry"])
    out["facility"] = utils.ratio(out["bst_net_premium"], out["facility_implied_expiry"])
    out["bp_rate_change"] = utils.ratio(out["bst_net_premium"], out["bp_implied_expiry"])
    out["bp_rarc_margin"] = utils.ratio(out["bst_net_premium"], out["bp_rarc_margin_implied_expiry"])

    return out


def calculate_rate_change_past_years_summary(rate_change_df, years_dict):
    total_cols = ["bst_net_premium"]    
    
    for year in list(years_dict.values())[1:]:
        total_cols += [f'{year}/selected_implied_expiry']
        total_cols += [f'{year}/facility_implied_expiry']
        total_cols += [f'{year}/beazley_implied_expiry']

    out = pd.DataFrame([{
        c: rate_change_df[c].sum()
        for c in total_cols
    }])

    for year in list(years_dict.values())[1:]:
        out[f'{year}/selected'] = utils.ratio(out["bst_net_premium"], out[f'{year}/selected_implied_expiry'])
        out[f'{year}/facility'] = utils.ratio(out["bst_net_premium"], out[f'{year}/facility_implied_expiry'])
        out[f'{year}/beazley_group_achieved'] = utils.ratio(out["bst_net_premium"], out[f'{year}/beazley_implied_expiry'])

    return out