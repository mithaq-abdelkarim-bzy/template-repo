import math as math
import algorithms.rate_utilities as utils
from algorithms.inflation.inflation_helpers import (
    set_year_columns_headers,
    generate_years_dict,
    init_inflation_details_df,
    process_year_inflation_details,
    init_summary_by_lob_df,
    process_year_inflation_details_sum,
    set_is_tab_shown
)
from algorithms import rate_constants as constants
from libraries.model_profiler.algorithms.profiling_hxd_functions import time_me

@time_me
def rate_inflation(hxd, rater):
    # Show inflation tab
    set_is_tab_shown(hxd)

    # Get paths to data
    final_composition_path = hxd.non_cds.risk_code_composition.final_composition
    inflation_details_path = hxd.cds.inflation.details
    inflation_summary_path = hxd.cds.inflation.summary_by_lob

    # Build year mapping and headers
    years_dict = generate_years_dict(hxd)
    set_year_columns_headers(hxd, years_dict)

    # Exit if no composition data
    if not final_composition_path or final_composition_path == [{}]:
        return

    # Load DataFrames from rater
    final_composition_df = rater["risk_composition_final"]
    final_composition_df['selected_lob'] = final_composition_df['selected_lob'].fillna('0')
    base_inf_df = rater["base_inf_df"]
    excess_inf_df = rater["excess_inf_df"]

    # Initialize inflation details
    inflation_details_df = init_inflation_details_df(rater, final_composition_df)

    # Process first 6 years
    inflation_details_df = process_year_inflation_details(
        inflation_details_df, base_inf_df, excess_inf_df, inflation_details_path,
        list(years_dict.values())[:6], True
    )

    # Process remaining years
    inflation_details_df = process_year_inflation_details(
        inflation_details_df, base_inf_df, excess_inf_df, inflation_details_path,
        list(years_dict.values())[6:], False
    )

    # Build summary by line of business
    summary_by_lob_df = init_summary_by_lob_df(inflation_details_df)

    # Aggregate inflation impact
    summary_by_lob_df = process_year_inflation_details_sum(summary_by_lob_df, inflation_details_df, years_dict)

    # Reset hxd summary container
    hxd.cds.inflation.summary_by_lob = [{}] * summary_by_lob_df.shape[0]

    # Write inflation details back
    base_cols = ['bp_class', 'composition', 'is_row_visible', 'risk_code', 'selected_lob']
    year_cols = [f'year_{i}' for i in range(26)]
    cols_to_keep = base_cols + year_cols
    rater['inflation_data'] = inflation_details_df #[cols_to_keep] this was removed as part of moving all the saves to end - we need calculated

    # Write summary back
    rater['inflation_by_lob'] = summary_by_lob_df

    # Save summary as CSV string
    hxd.non_cds.inflation.inflation_summary_str = summary_by_lob_df.to_csv(index=False)