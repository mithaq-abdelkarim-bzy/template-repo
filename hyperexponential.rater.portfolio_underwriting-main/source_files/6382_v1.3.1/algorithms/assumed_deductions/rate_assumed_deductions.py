import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import rate_constants as constants
from algorithms.assumed_deductions.assumed_deductions_helpers import (
    build_deduction_summary_df,
    build_market_deductions_df,
    build_non_cds_final_deductions,
    build_years_dict,
    build_total_summations_tables,
    calculate_data_driven_deductions,
    set_years_headers,
    copy_amount_to_market_deductions,
    init_deductions_df,
    get_selected_years_array,
    set_dropdown_values,
    get_year_start,
    get_year_end,
    set_model_type,
    set_emojis_for_selected_years,
    calculate_total_summations,
    build_data_driven_deductions_df,
    build_manual_deductions
)
from libraries.model_profiler.algorithms.profiling_hxd_functions         import time_me

@time_me
def rate_assumed_deductions(hxd, rater):
    deductions_path = hxd.cds.assumed_deductions

    # Set the model type based premium data available in risk information
    selected_type = set_model_type(hxd)
    is_prem_data_available = hxd.cds.risk_information.prem_data_available

    # Build a dictionary mapping years to their respective labels e.g. {'2017': 'year_1', '2016': 'year_2', '2015': 'year_3',...}
    years_dict = build_years_dict(hxd)

    # Set years headers and dropdown values for the year end and year start
    set_years_headers(  hxd,             years_dict)
    set_dropdown_values(deductions_path, years_dict)

    # Get the start and end years inputs from the assumed deduction
    year_start      = get_year_start(deductions_path, years_dict)
    year_end        = get_year_end(  deductions_path, years_dict)

    # Get an array of selected years between the start and end years
    years_selected  = get_selected_years_array(year_start, year_end, years_dict)

    # Set ✅ emoji for selected years
    set_emojis_for_selected_years(hxd, years_selected)

    final_composition_df = rater["risk_composition_final"]

    # If there is no final composition in non_cds_rcc, exit the function   
    if final_composition_df.empty:
        rater['deduct_data']    = pd.DataFrame()
        rater['deduct_manual']  = pd.DataFrame()
        return pd.DataFrame()

    # Get unique selected lines of business from the final  risk code composition
    unique_selected_lobs = final_composition_df['selected_lob'].unique()

    # Get the number of unique selected lines of business
    no_of_rows = len(unique_selected_lobs)   

    manually_entered_deductions_df = None
    data_driven_deductions_df = None
    
    if selected_type == "Manual":
        manually_entered_deductions_df = build_manual_deductions(
            constants.common_fields, 
            unique_selected_lobs, 
            deductions_path,
            no_of_rows,
            rater            )

    if is_prem_data_available and no_of_rows:
        data_driven_deductions_df = build_data_driven_deductions_df(
            hxd,
            years_selected,
            rater, 
            unique_selected_lobs, 
            years_dict, 
            deductions_path, 
            constants.common_fields, 
            no_of_rows)

    deductions_df = build_non_cds_final_deductions(
        selected_type,
        hxd, 
        data_driven_deductions_df, 
        manually_entered_deductions_df)

    rater["deductions_df"] = deductions_df