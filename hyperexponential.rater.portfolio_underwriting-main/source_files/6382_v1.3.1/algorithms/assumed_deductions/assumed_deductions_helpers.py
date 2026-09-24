import pandas as pd
import numpy as np
import algorithms.rate_utilities as utils
from algorithms import rate_constants as constants
from algorithms.risk_information.risk_information_helpers import import_inception_date


def set_years_headers(hxd, years_dict):
    # For each year, set the attribute name (year_value) to the year key (year_attr)
    for year_attr, year_value in years_dict.items():
        setattr(hxd.non_cds.assumed_deductions, year_value, year_attr)


def set_dropdown_values(ad, years_dict):
    # Populate dropdown values with available years sorted in ascending order
    prior_years = [year for year in years_dict.keys()]
    ad.data_driven_deductions.year_dropdown = sorted(prior_years)


def get_year_start(ad, years_dict):
    # Use selected year start if provided, otherwise fallback to 3rd key in years_dict
    selected_year_start = ad.data_driven_deductions.year_start.selected
    default_year = list(years_dict.keys())[2]
    year_start = (
        selected_year_start
        if selected_year_start is not None 
        else default_year
    )
    # Always set the calculated value to the default year
    ad.data_driven_deductions.year_start.calculated = default_year

    return year_start


def get_year_end(ad, years_dict):
    # Use selected year end if provided, otherwise fallback to 2nd key in years_dict
    selected_year_end = ad.data_driven_deductions.year_end.selected
    default_year = list(years_dict.keys())[1]
    year_end = (
        selected_year_end
        if selected_year_end is not None 
        else default_year
    )
    # Always set the calculated value to the default year
    ad.data_driven_deductions.year_end.calculated = default_year

    return year_end


def set_model_type(hxd):
    # Get both CDS and non-CDS assumed deductions
    non_cds_ad = hxd.non_cds.assumed_deductions
    ad = hxd.cds.assumed_deductions

    # Check whether premium data is available
    prem_data_available = hxd.cds.risk_information.prem_data_available

    # Default model type is 'Data' if premium data exists, otherwise 'Manual'
    calculated_model_type = 'Data' if prem_data_available else 'Manual'
    ad.model_type.calculated = calculated_model_type
    selected_model_type = ad.model_type.selected

    # Update non-CDS is_manual flag based on selection
    non_cds_ad.is_manual = (selected_model_type == 'Manual')

    return selected_model_type


def build_years_dict(hxd):
    # Number of years to consider from system constants
    years_to_consider = constants.YEARS_TO_CONSIDER_IN_ASSUMED_DEDUCTIONS
    # Get inception year from core data
    inception_date = import_inception_date(hxd)
    inception_year = inception_date.year

    # Build mapping of year string → year attribute name
    years_dict = {
        str(inception_year - i): f"year_{i}" 
        for i in range(0, years_to_consider)
    }

    return years_dict


def set_premiums_from_policy_level_data(hxd, rater, df, premium_basis, years_dict):
    # Choose net or gross premium column
    premium_column = 'net_premium_cnv' if premium_basis == "Net" else 'gross_premium_cnv'

    # import policy level data and final risk code composition
    policy_level_df = rater["policy_data"]

    # Aggregate premiums by selected_lob and year_of_account
    grouped_df = policy_level_df.groupby(
        ['selected_lob', 'yoa'], as_index=False)[premium_column].sum()

    # Pivot table with selected_lob as index and YOAs as columns
    pivot_df = grouped_df.pivot(
        index='selected_lob', columns='yoa', values=premium_column).fillna(0)
    pivot_df.columns = pivot_df.columns.astype(int).astype(str)

    # Keep only years that exist in years_dict
    existing_years = [col for col in pivot_df.columns if col in years_dict]
    filtered_pivot_df = pivot_df[existing_years].rename(columns=years_dict)

    # Ensure all years are present, fill missing with 0
    filtered_pivot_df = filtered_pivot_df.reindex(
        columns=years_dict.values(), fill_value=0)

    # Drop old year columns in df to avoid duplicates
    df = df.drop(columns=years_dict.values(), errors='ignore')

    # Reset index for merging
    filtered_pivot_df.reset_index(inplace=True)

    # Merge transformed premiums into df
    result_df = pd.merge(df, filtered_pivot_df,
                         on='selected_lob', how='left').fillna(0)
    return result_df


def get_selected_years_array(year_start, year_end, years_dict):
    # Extract keys (years) and values into lists
    keys = list(years_dict.keys())       # e.g. ["2023", "2022", "2021"]
    values = list(years_dict.values())   # corresponding values for each year

    # Define the first and last years based on dict key ordering
    # NOTE: This assumes keys are sorted in descending order (latest → earliest)
    first_year = int(keys[-1])  # the earliest year
    last_year = int(keys[0])    # the latest year

    # If both start and end years are completely outside the known range, return empty
    if ((int(year_start) < first_year and int(year_end) < first_year) or
        (int(year_start) > last_year and int(year_end) > last_year)):
        return []

    # --- Handle start year ---
    if int(year_start) < first_year:
        # Clamp start to earliest year (index after last element, corrected later by slicing)
        start_year_index = len(values)
    elif int(year_start) >= first_year and int(year_start) <= last_year:
        # Valid year inside range → find its index
        start_year_index = keys.index(str(year_start))
    else:
        return []  # fallback if somehow invalid

    # --- Handle end year ---
    if int(year_end) > last_year:
        # Clamp end to latest year (first index)
        end_year_index = 0
    elif int(year_end) >= first_year and int(year_end) <= last_year:
        # Valid year inside range → find its index
        end_year_index = keys.index(str(year_end))
    else:
        return []  # fallback if somehow invalid

    # Ensure indices are in ascending order so slicing works
    lo, hi = sorted([start_year_index, end_year_index])

    # Slice values inclusively between the start and end year
    years_array = values[lo: hi + 1]

    return years_array


def set_emojis_for_selected_years(hxd, selected_years_array):
    # Loop through each selected year attribute
    for year_attr in selected_years_array:
        # Add a checkmark emoji to the existing value for that year in assumed deductions
        setattr(
            hxd.non_cds.assumed_deductions, 
            year_attr,
            f"{getattr(hxd.non_cds.assumed_deductions, year_attr, None)} ✅")


def build_premium_table(hxd, rater, unique_selected_lob, years_dict, prem_basis, path):
    # import policy level data and final risk code composition
    policy_level_df = rater["policy_data"]  

    # Handle the case when no policy data exists
    if policy_level_df.empty:
        # Create DataFrame with required columns and a single row of zeros
        columns = ["selected_lob"] + list(years_dict.values())
        df = pd.DataFrame([[0] * len(columns)], columns=columns)
        return df

    # Initialize DataFrame for premiums
    df = pd.DataFrame()
    # Populate selected lines of business
    df["selected_lob"] = unique_selected_lob
    # Add premium values from policy data according to chosen basis and years
    df = set_premiums_from_policy_level_data(hxd, rater, df, prem_basis, years_dict)
    return df


def calculate_total_summations(df, years, path):
    # Only proceed if DataFrame has data
    if not df.empty:
        # For each year, calculate the column sum and store in summary path
        for year in years:
            node = getattr(path, "summary")
            setattr(node, year, df[year].sum())


def build_market_deductions_df(rater, gross_premium_df, net_prem_df, unique_selected_lob):
    # Load deductions data from hx list into DataFrame
    ad_md_df = rater.get("deduct_data_yr_sel_lob", pd.DataFrame())

    # Assign selected lines of business
    ad_md_df["selected_lob"] = unique_selected_lob

    # Keep numeric data by dropping 'selected_lob'
    gross_premium_df_numeric = gross_premium_df.drop(columns=['selected_lob'])
    net_prem_df_numeric = net_prem_df.drop(columns=['selected_lob'])
    # Compute deductions as (gross - net) / gross
    ad_md_df_numeric = (gross_premium_df_numeric - net_prem_df_numeric) / gross_premium_df_numeric
    # Copy numeric deductions to final DataFrame
    ad_md_df = ad_md_df_numeric.copy()
    # Re-attach selected_lob column
    ad_md_df['selected_lob'] = gross_premium_df['selected_lob']
    # Replace NaNs with zeros
    ad_md_df = ad_md_df.fillna(0)
    return ad_md_df


def get_prem_basis_input(basis_path, common_fields):
    # Create empty DataFrame with one row and given fields
    basis_df = pd.DataFrame(index=[0], columns=common_fields)
    # Fill each field with value from basis_path
    for col in common_fields:
        basis_df.at[0, col] = getattr(basis_path, col)
    return basis_df


def copy_amount_to_market_deductions(amount_path, common_fields, market_deductions_df):
    # For each field, copy calculated values and handle overrides
    for col in common_fields:
        # Save calculated value
        market_deductions_df[f"{col}/calculated"] = getattr(amount_path, col)
        # Use overridden value if present, otherwise calculated
        market_deductions_df[f"{col}"] = np.where(
            market_deductions_df[f"{col}/is_overridden"],
            market_deductions_df[col],
            market_deductions_df[f"{col}/calculated"]
        )
    # Replace nulls in deduction columns with zeros
    market_deductions_df[common_fields].fillna(0, inplace = True)
    return market_deductions_df


def calculate_data_driven_deductions(df, years_selected, gross_premium_df, net_prem_df):
    # Compute deductions as (gross - net) / gross across selected years
    df["market_deductions/calculated"] = (
        (gross_premium_df[years_selected].sum(axis=1) - net_prem_df[years_selected].sum(axis=1))
        / gross_premium_df[years_selected].sum(axis=1)
    )
    # Replace infinities and NaNs with zeros
    df["market_deductions/calculated"] = (
       df["market_deductions/calculated"]
       .replace([np.inf, -np.inf], 0)
       .fillna(0)
    )
    # Respect overrides, otherwise use calculated values
    df["market_deductions"] = np.where(
        df["market_deductions/is_overridden"],
        df["market_deductions"],
        df["market_deductions/calculated"]
    )
    return df


def init_deductions_df(rater, basis, unique_selected_lob):
    # Convert deductions table into DataFrame
    rater_source = 'deduct_manual' if basis == "manual" else 'deduct_data'
    market_deductions_df = rater.get(rater_source, pd.DataFrame())

    # Assign selected lines of business to each row (up to 20 rows)
    for i in range(min(len(unique_selected_lob), 20)):
        market_deductions_df.at[i, 'selected_lob'] = unique_selected_lob[i]
    # Set row visibility based on whether lob is assigned
    market_deductions_df["is_row_visible"] = market_deductions_df["selected_lob"].notna()
    return market_deductions_df


def build_deduction_summary_df(basis_path, common_fields, unique_selected_lob, market_deductions_df):
    # Define required columns for summary
    columns = ["premium", "market_brokerage", "net_premium",
               "total_deductions", "effective_deductions"] + common_fields
    # Load premium basis values
    basis_df = get_prem_basis_input(basis_path, common_fields)
    # Create empty summary DataFrame sized to number of lines of business
    summary_df = pd.DataFrame(index=range(len(unique_selected_lob)), columns=columns)
    # Set premium to 1 for all rows
    summary_df["premium"] = 1
    # Compute brokerage as premium * deductions
    summary_df["market_brokerage"] = summary_df["premium"] * market_deductions_df["market_deductions"]
    # Net premium = premium - brokerage
    summary_df["net_premium"] = summary_df["premium"] - summary_df["market_brokerage"]
    # For each deduction field, calculate value based on Gross or Net basis
    # Vectorized version: much faster for large DataFrames 
    gross_mask = pd.Series([basis_df.at[0, col] == 'Gross' for col in common_fields], index=common_fields)
 
    # Only use columns present in both mask and DataFrame
    gross_cols = [col for col in common_fields if gross_mask.get(col, False) and col in summary_df.columns and col in market_deductions_df.columns]
    net_cols = [col for col in common_fields if not gross_mask.get(col, False) and col in summary_df.columns and col in market_deductions_df.columns]

    # Vectorized assignment for gross basis columns
    if gross_cols:
        summary_df[gross_cols] = market_deductions_df[gross_cols].mul(summary_df["premium"], axis=0)

    # Vectorized assignment for net basis columns
    if net_cols:
        summary_df[net_cols] = market_deductions_df[net_cols].mul(summary_df["net_premium"], axis=0)
   
    # Total deductions = sum of all fields + brokerage
    summary_df["total_deductions"] = summary_df[common_fields + ["market_brokerage"]].sum(axis=1)
    # Effective deductions = total / premium
    summary_df["effective_deductions"] = summary_df["total_deductions"] / summary_df["premium"]
    return summary_df


def build_total_summations_tables(ad, years_dict):
    dd_path = ad.data_driven_deductions
    gp_path = dd_path.gross_premium.summary
    np_path = dd_path.net_premium.summary
    md_path = dd_path.market_deductions.summary

    # Loop through each year in the years dictionary
    for year in years_dict.values():
        # Get gross premium sum for the year
        gp_sum = getattr(gp_path, year) or 0
        # Get net premium sum for the year
        np_sum = getattr(np_path, year) or 0
        # Calculate market deductions as (gross - net) / gross, handle division by zero
        sum_value = (gp_sum - np_sum) / gp_sum if gp_sum != 0 else 0  
        # Store the calculated value in the market deductions summary
        setattr(md_path, year, sum_value)


def build_data_driven_deductions_df(hxd, years_selected,  rater, unique_selected_lobs, years_dict, 
                                    deductions_path, common_fields,   no_of_rows):
    # Build gross premium DataFrame from policy-level data
    gross_premium_df = build_premium_table(
        hxd,
        rater,
        unique_selected_lobs,
        years_dict,
        'Gross',
        deductions_path.data_driven_deductions.gross_premium.deductions_derived_from_data)

    # Save gross premium table to rater
    rater['deduct_data_gp_ded'] = gross_premium_df

    # Build net premium DataFrame from policy-level data
    net_prem_df = build_premium_table(
        hxd,
        rater,
        unique_selected_lobs,
        years_dict,
        'Net',
        deductions_path.data_driven_deductions.net_premium.deductions_derived_from_data)

    # Save net premium table to deductions path
    rater['deduct_data_np_ded'] = net_prem_df

    # Build market deductions DataFrame by comparing gross vs net premiums
    market_deductions_df = build_market_deductions_df(
        rater,
        gross_premium_df, 
        net_prem_df, 
        unique_selected_lobs)

    # Save market deductions table to deductions path
    rater['deduct_data_mkt_ded'] = market_deductions_df

    # Build total summations for market deductions and save them
    build_total_summations_tables(deductions_path, years_dict)

    # Initialize deductions DataFrame with unique lines of business
    data_driven_deductions_df = init_deductions_df(rater, "data", unique_selected_lobs)

    # Calculate market deductions for selected years
    data_driven_deductions_df = calculate_data_driven_deductions(
        data_driven_deductions_df, 
        years_selected, 
        gross_premium_df, 
        net_prem_df)

    # Copy calculated/overridden amounts into deductions DataFrame
    data_driven_deductions_df = copy_amount_to_market_deductions(
        deductions_path.data_driven_deductions.deductions.amount, 
        common_fields, 
        data_driven_deductions_df)

    # Build a summary DataFrame for deductions (basis: Gross or Net)
    summary_df = build_deduction_summary_df(
        deductions_path.data_driven_deductions.deductions.basis,
        common_fields,
        unique_selected_lobs,
        data_driven_deductions_df)

    # Add effective deductions from summary into the deductions DataFrame
    data_driven_deductions_df["selected_effective_deductions"] = summary_df["effective_deductions"]

    # Write truncated manual deductions DataFrame to rater
    rater['deduct_data'] = data_driven_deductions_df[:no_of_rows]

    # Return the truncated deductions DataFrame
    return data_driven_deductions_df[:no_of_rows]


def build_manual_deductions(common_fields, unique_selected_lobs, deductions_path, no_of_rows, rater):
    # Initialize manual deductions DataFrame with unique lines of business
    manually_entered_deductions_df = init_deductions_df(rater, "manual", unique_selected_lobs)

    # Copy entered amounts into manual deductions DataFrame
    copy_amount_to_market_deductions(
        deductions_path.deductions_manually_entered.amount, 
        common_fields, 
        manually_entered_deductions_df)

    # Build summary DataFrame for manual deductions
    manual_summary_df = build_deduction_summary_df(
        deductions_path.deductions_manually_entered.basis,
        common_fields,
        unique_selected_lobs,
        manually_entered_deductions_df)

    # Add effective deductions from summary into manual deductions DataFrame
    manually_entered_deductions_df["selected_effective_deductions"] = manual_summary_df["effective_deductions"]

    # Write truncated manual deductions DataFrame to rater
    rater['deduct_manual'] = manually_entered_deductions_df[:no_of_rows]

    # Return manual deductions DataFrame (limited rows)
    return manually_entered_deductions_df[:no_of_rows]


def build_non_cds_final_deductions(selected_type, hxd, data_driven_df=None, manual_df=None):
    # Pick the correct DataFrame based on whether the model type is Data or Manual
    selected_df = data_driven_df if selected_type == 'Data' else manual_df

    # Replace NaN values in market_deductions column with 0
    selected_df['market_deductions'] = selected_df['market_deductions'].fillna(0)

    # Calculate total fees as the sum of multiple fee columns
    selected_df['total_fees'] = (
        selected_df['mga_fee'].fillna(0)
        + selected_df['facility_brokerage'].fillna(0)
        + selected_df['leaders_fee'].fillna(0)
        + selected_df['service_fee'].fillna(0)
        + selected_df['other'].fillna(0)
    )

    # Keep only relevant columns for final deductions
    filtered_cols = [
        "market_deductions",
        "facility_brokerage",
        "service_fee",
        "other",
        "mga_fee",
        "leaders_fee",
        "is_row_visible",
        "selected_effective_deductions",
        "selected_lob",
        "total_fees"
    ]

    # Create a filtered DataFrame with only the needed columns
    filtered_df = selected_df[filtered_cols]

    # Convert DataFrame to a list of dictionaries and assign it to non-CDS final deductions
    hxd.non_cds.assumed_deductions.final_deductions = filtered_df.to_dict('records')

    # Return the filtered DataFrame
    return filtered_df