import numpy as np
import pandas as pd
import algorithms.rate_utilities as utils
from algorithms import rate_constants as constants
from algorithms.risk_information.risk_information_helpers import import_inception_date


def set_year_columns_headers(hxd, years_dict):
    # Set dynamic year headers in hxd using the mapping from years_dict
    for year_attr, year_value in years_dict.items():
        setattr(hxd.non_cds.inflation, year_value, year_attr)


def generate_years_dict(hxd):
    # Get inception date and year
    inception_date = import_inception_date(hxd)  
    inception_year = inception_date.year  
    # Build mapping: actual year -> relative label (year_0, year_1, ...)
    return {
        str(inception_year - i): f"year_{i}"
        for i in range(constants.YEARS_TO_CONSIDER_IN_Inflation)
    }


def set_is_tab_shown(hxd):
    # Get pricing method and syndicate flag
    priced_by = hxd.cds.risk_information.priced_by
    not_follow_main_syndicate = hxd.non_cds.risk_information.not_follow_main_syndicate
    # Show inflation tab if conditions are met
    if priced_by == "Actuarial" and not_follow_main_syndicate:
        hxd.non_cds.inflation.is_shown = True


def init_inflation_details_df(rater, final_composition_df):
    # Load inflation details from hxd as DataFrame, match size with composition
    inflation_details_df = rater.get("inflation_data", pd.DataFrame())
    inflation_details_df = inflation_details_df[:final_composition_df.shape[0]]

    fields_to_copy = ['risk_code', 'composition', 'selected_lob']

    # Copy risk_code, composition, and LOB from composition DataFrame
    inflation_details_df[fields_to_copy] = final_composition_df[fields_to_copy]

    # Copy business plan class for calculated values
    inflation_details_df['bp_class/calculated'] = final_composition_df['selected_bp_class']
    
    # Use overridden bp_class if set, otherwise fallback to calculated
    inflation_details_df['bp_class'] = np.where(
        inflation_details_df['bp_class/is_overridden'],
        inflation_details_df['bp_class'],
        inflation_details_df['bp_class/calculated'],
    )

    # Mark row as visible if LOB is not null
    inflation_details_df["is_row_visible"] = inflation_details_df["selected_lob"].notna()

    return inflation_details_df


def process_year_inflation_details(inflation_details_df, base_inf_df, excess_inf_df, inflation_details_path, years_list, is_override=False):
    # Create lookup dictionaries once (avoids repeated merges)
    base_inf_lookup   = {year: base_inf_df.set_index("bp_class")[year].to_dict()   for year in years_list}
    excess_inf_lookup = {year: excess_inf_df.set_index("bp_class")[year].to_dict() for year in years_list}
                         
    # Iterate through all years in years_list
    for col_name in years_list:
        # Map base inflation by business plan class
        inflation_details_df[f"{col_name}/base_inf"] = inflation_details_df["bp_class"].map(
            base_inf_lookup[col_name]
        ).fillna(0)

        # Map excess inflation by business plan class
        inflation_details_df[f"{col_name}/excess_inf"] = inflation_details_df["bp_class"].map(
            excess_inf_lookup[col_name]
        ).fillna(0)

        # Calculate total inflation = base + excess
        inflation_details_df[f"{col_name}/calculated"] = (
            inflation_details_df[f"{col_name}/base_inf"] 
            + inflation_details_df[f"{col_name}/excess_inf"]
        )

        if is_override:
            # If overridden, use overridden values, else use calculated
            inflation_details_df[col_name] = np.where(
                inflation_details_df[f"{col_name}/is_overridden"],
                inflation_details_df[col_name],
                inflation_details_df[f"{col_name}/calculated"]
            )
        else:
            # Default case: always use calculated values
            inflation_details_df[col_name] = inflation_details_df[f"{col_name}/calculated"]
            

    return inflation_details_df


def init_summary_by_lob_df(inflation_details_df):
    # Group by LOB and sum composition
    return (inflation_details_df.groupby("selected_lob", as_index=False)
            .agg(composition=("composition", "sum"))
            .sort_values(by="composition", ascending=False)
            .reset_index(drop=True))


def process_year_inflation_details_sum(summary_by_lob_df, inflation_details_df, years_dict):
    # Assuming 'selected_lob' is the grouping key
    # For each year column, calculate the weighted average
    for column_name in years_dict.values():
        # Calculate the numerator: sum(inflation * composition) for each LOB
        numerator = (inflation_details_df[column_name] * inflation_details_df['composition']).groupby(inflation_details_df['selected_lob']).sum()

        # Calculate the denominator: sum(composition) for each LOB
        denominator = inflation_details_df.groupby(inflation_details_df['selected_lob'])['composition'].sum()

        # Calculate the weighted average
        weighted_avg = (numerator / denominator).fillna(0) # Handle cases where denominator might be zero

        # Assign the results back to summary_by_lob_df
        # Ensure that the index of weighted_avg aligns with 'selected_lob' in summary_by_lob_df
        summary_by_lob_df[column_name] = summary_by_lob_df['selected_lob'].map(weighted_avg)

        # Fill any NaN values that might result if a 'selected_lob' in summary_by_lob_df
        # does not exist in inflation_details_df or has a zero denominator
        summary_by_lob_df[column_name] = summary_by_lob_df[column_name].fillna(0)

    return summary_by_lob_df