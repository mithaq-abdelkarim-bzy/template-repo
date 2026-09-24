import hx
import algorithms.rate_utilities as utils
import pandas as pd
from algorithms import rate_constants as constants
from algorithms.risk_information.risk_information_helpers import import_inception_date
from algorithms.risk_code_composition.risk_code_composition_helpers import (
    set_rater_type,
    set_dropdown_values,
    set_years_headers,
    get_year_start,
    get_year_end,
    get_selected_years_array,
    set_emojis_for_selected_years,
    set_premiums_from_policy_level_data,
    merge_with_lloyds_data_and_calculate_composition,
    calculate_and_set_total_summations,
    save_premiums_table,
    build_data_cs_table,
    build_manual_cs_table,
    build_non_cds_final_selected_composition
)
from libraries.model_profiler.algorithms.profiling_hxd_functions         import time_me

@time_me
def rate_risk_code_composition(hxd, rater):
    # Determine if user selected "Data" or "Manual" mode for risk code composition
    selected_type = set_rater_type(hxd)

    # Check if premium data is available (switch for whether Data-driven mode can work)
    is_prem_data_available = hxd.cds.risk_information.prem_data_available

    # Handle references to risk code composition table (rcc shorthand)
    rcc = hxd.cds.risk_code_composition
    
    # Load risk code library reference data
    risk_code_library = rater["risk_code_library_df"]

    # Extract inception date/year for this account
    inception_date = import_inception_date(hxd)
    inception_year = inception_date.year

    # Build dictionary mapping: { "2017": "year_1", "2016": "year_2", ... }
    years_dict = {
        str(inception_year - i): f"year_{i}"
        for i in range(constants.YEARS_TO_CONSIDER_IN_RISK_CODE_COMPOSITION)
    }

    # Sync headers and dropdown values in the UI with available years
    set_years_headers(hxd, years_dict)
    set_dropdown_values(rcc, years_dict)

    # Get start/end year selection from user
    year_start = get_year_start(rcc, years_dict)
    year_end = get_year_end(rcc, years_dict)

    # Convert year_start/year_end into list of selected years
    selected_years_array = get_selected_years_array(year_start, year_end, years_dict)

    # Add ✅ emojis to selected years in the UI (UX nicety)
    set_emojis_for_selected_years(hxd, selected_years_array)

    # Initialize outputs
    rcc_cs_df = None
    rcc_manual_cs_df = None

    # If user selects "Manual", build manual composition table
    if selected_type == "Manual":
        rcc_manual_cs_df = build_manual_cs_table(rcc, risk_code_library, hxd, rater)

    # Pull in policy-level data (already processed in rate_policy_level earlier)
    policy_level_df = rater["policy_data"] 

    # Find unique risk codes present
    unique_risk_codes = policy_level_df['risk_code'].fillna('[blank]').unique()
    no_of_rows = len(unique_risk_codes)

    # write available plan classes to hxd
    bp_df   = hx.params.table_business_plan.rename(columns={'business_plan_class': 'desc'})
    bp_yr   = pd.Series([ min(bp_df['year']),  max(bp_df['year']),  inception_year]).median()
    mask_yr = bp_df['year']==bp_yr
    hxd.cds.risk_code_composition.bp_class_desc = bp_df.loc[mask_yr,['desc']].to_dict(orient="records")


    # If premium data exists and there are risk codes, run Data-driven flow
    if is_prem_data_available and no_of_rows:
        # Input: which premium basis to use (gross, net, etc.)
        premium_base = rcc.data_driven_composition.premium_basis

        # Initialize premiums table
        premiums_df = pd.DataFrame()

        # Force risk_code column to align with unique values found
        premiums_df["risk_code"] = unique_risk_codes

        # Step 1: Calculate premiums from policy-level data
        unique_fob_x_risk_code_df, premiums_df = set_premiums_from_policy_level_data(
            policy_level_df, premiums_df, premium_base, years_dict
        )

        # Step 2: Merge with Lloyd’s data & compute final composition %
        unique_fob_x_risk_code_df, premiums_df = merge_with_lloyds_data_and_calculate_composition(
            premiums_df, unique_fob_x_risk_code_df, risk_code_library, selected_years_array
        )

        # STEP 3: drop nils - added 15/1/2026
        mask_nil_composition = unique_fob_x_risk_code_df['composition'] !=  0
        unique_fob_x_risk_code_df = unique_fob_x_risk_code_df[mask_nil_composition]

        years_dict_vals = list(years_dict.values())

        # Save updated premiums table to rcc
        save_premiums_table(premiums_df, rcc, years_dict_vals)

        # Compute totals/summations and persist them
        rcc_sum_df = calculate_and_set_total_summations( premiums_df, years_dict_vals, hxd     )

        # Build Data-driven composition summary (cross-section table)
        rcc_cs_df = build_data_cs_table( rcc, unique_fob_x_risk_code_df, risk_code_library, hxd, rater)

    # Merge manual vs. data-driven outputs into a final composition DataFrame
    build_non_cds_final_selected_composition(
        hxd,
        rater,
        manual_df=rcc_manual_cs_df,
        data_df=rcc_cs_df
    )