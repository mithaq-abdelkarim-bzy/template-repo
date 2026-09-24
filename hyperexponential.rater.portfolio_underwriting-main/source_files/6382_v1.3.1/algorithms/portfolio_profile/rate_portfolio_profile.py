import hx
import algorithms.rate_utilities as utils
import polars as pl
import pyarrow as pa
import pandas as pd
from algorithms.risk_information.risk_information_helpers import import_inception_date
from algorithms.portfolio_profile.portfolio_profile_helpers import (
    set_is_tab_shown,
    generate_years_dict,
    set_column_headers,
    calculate_rate_change_with_selection_override,
    calculate_rate_change_no_override,
    calculate_premium_and_weighting,

    generate_summary_by_lob_df,
    save_selected_lob_and_risk_code_combination,
    save_summary_by_lob_df,
    get_lloyds_data,
    init_hxd_output_nodes,

    get_proj_risk_code_result,
    get_proj_lob_summary_result
)
from algorithms import rate_constants as constants
from libraries.model_profiler.algorithms.profiling_hxd_functions import time_me

    
@time_me
def rate_portfolio_profile(hxd, rater, run_lloyds_data_only: bool):
    # Ensure the relevant tab is shown depending on syndicate/priced_by rules
    set_is_tab_shown(hxd)

    # Exit early if no final composition data exists
    if not len(hxd.non_cds.risk_code_composition.final_composition):
        rater["portfolio_profile"] = pd.DataFrame()
        rater["portfolio_profile_summary"] = pd.DataFrame()
        return

    # Convert input policy-level DataFrame to Polars format
    policy_level_df = rater["policy_data"]
    policy_level_df = utils.pd_to_pl_df(policy_level_df)

    # Convert final composition DataFrame to Polars format
    final_composition_df_pd = rater["risk_composition_final"]
    final_composition_df = utils.pd_to_pl_df(final_composition_df_pd)

    # Extract risk_code, selected LOB, and business plan class
    portfolio_profile_df = final_composition_df.select(
        [
            pl.col("risk_code"),
            pl.col("selected_lob"),
            pl.col("selected_bp_class").alias("bp_class"),
        ]
    )  

    # Rate change tables for override logic
    rate_change_tables = [
        'rate_change_with_selection_override',
    ]

    # Get inception year and build year mapping
    inception_date = import_inception_date(hxd)
    inception_year = inception_date.year
    years_dict = generate_years_dict(inception_year)

    if run_lloyds_data_only:
        # Setup headers for Lloyd’s and rate change tables
        set_column_headers(rate_change_tables + constants.lloyds_tables, years_dict, hxd)

        # Calculate premium and weighting by policy
        portfolio_profile_df = calculate_premium_and_weighting( portfolio_profile_df, policy_level_df, inception_year, hxd, final_composition_df)

        # Aggregate premium and weighting at LoB level
        summary_by_lob_df = portfolio_profile_df.group_by("selected_lob").agg(
            [
                pl.col("selected_premium").sum().alias("selected_premium"),
                pl.col("weighting").sum().alias("weighting"),
            ]
        )

        # Initialize output nodes in HXD for downstream usage
        init_hxd_output_nodes(portfolio_profile_df, summary_by_lob_df, hxd)

        # Load Beazley reference data
        beazley_data_arrow_table = pa.Table.from_pandas(hx.params.table_beazley_data, preserve_index=False)
        beazley_data_df = pl.from_arrow(beazley_data_arrow_table)

        # Apply rate change calculation without overrides
        portfolio_profile_df = calculate_rate_change_no_override( portfolio_profile_df, beazley_data_df, years_dict)

        # Append Lloyd’s-specific development and premium data
        portfolio_profile_df = get_lloyds_data(          portfolio_profile_df, years_dict, hxd)

        # Determine output columns based on available Lloyd’s tables
        output_columns = ['risk_code', 'bp_class', 'selected_lob', 'selected_premium', 'weighting'] + [
            f"{group}/{year}" for group in constants.lloyds_tables for year in years_dict.values()
            if f"{group}/{year}" in portfolio_profile_df.columns]
        
        # Save selected risk/LOB combinations with rate data
        save_selected_lob_and_risk_code_combination(    portfolio_profile_df, output_columns, hxd)
        
        # Build updated LoB summary including Lloyd’s metrics
        summary_by_lob_df = generate_summary_by_lob_df( summary_by_lob_df, portfolio_profile_df, years_dict, constants.lloyds_tables)

        # Define summary output columns for Lloyd’s data
        summary_output_columns = ['selected_lob', 'selected_premium', 'weighting'] + [
            f"{group}/{year}" for group in constants.lloyds_tables for year in years_dict.values()]

        # Save summarized LoB data
        save_summary_by_lob_df(summary_by_lob_df, summary_output_columns, hxd)

    else:
        # Exit if no composition data exists
        if len(hxd.non_cds.risk_code_composition.final_composition) == 0:
            return

        # Load portfolio profile and LoB summary data from HXD into Polars
        portfolio_profile_df = rater.get("portfolio_profile", pd.DataFrame())
        portfolio_profile_df = utils.pd_to_pl_df(portfolio_profile_df)
        summary_by_lob_df    = rater.get("portfolio_profile_summary", pd.DataFrame())
        summary_by_lob_df    = utils.pd_to_pl_df(summary_by_lob_df)


        # Load Beazley reference data
        beazley_data_pd_df = hx.params.table_beazley_data
        beazley_data_df = utils.pd_to_pl_df(beazley_data_pd_df)

        # Apply rate change logic with overrides 
        portfolio_profile_df = calculate_rate_change_with_selection_override(hxd, portfolio_profile_df, beazley_data_df, years_dict, rater)        

        # Append projection-level risk code results
        portfolio_profile_df = get_proj_risk_code_result(hxd, portfolio_profile_df, rater)

        # Projection columns to retain
        proj_cols = [
            "lloyds_risk_code_results/final_gn_ulr", 
            "lloyds_risk_code_results/selected_ielr", 
            "lloyds_risk_code_results/model_ielr",
            "beazley_risk_code_results/final_gn_ulr"
        ]

        # Build output columns for rate change tables
        output_columns = [
            f"{group}/{year}" 
            for group in rate_change_tables 
            for year in years_dict.values()
            if f"{group}/{year}" in portfolio_profile_df.columns
        ] + proj_cols

        # Save updated risk/LOB combinations with projections
        save_selected_lob_and_risk_code_combination(portfolio_profile_df, output_columns, hxd)

        # Build updated LoB summary including override tables
        summary_by_lob_df = generate_summary_by_lob_df(summary_by_lob_df, portfolio_profile_df, years_dict, rate_change_tables)

        # Load own experience summary data and align to LoB summary length
        own_exp_summary = rater.get("proj_own_exper_summary_pl", pd.DataFrame())
        own_exp_summary = own_exp_summary.slice(0, summary_by_lob_df.height)
        rater["proj_own_exper_summary_pl"] = own_exp_summary
        rater["proj_own_exper_summary"]    = own_exp_summary.to_pandas()

        # Append projection results at LoB level
        summary_by_lob_df = get_proj_lob_summary_result(hxd, summary_by_lob_df, own_exp_summary)

        # Build summary output columns for rate change tables
        summary_output_columns = [
            f"{group}/{year}" for group in rate_change_tables for year in years_dict.values()] + proj_cols

        # Save final summarized LoB data
        save_summary_by_lob_df(summary_by_lob_df, summary_output_columns, hxd)

    # Update rater with final portfolio profile and summary outputs
    rater["portfolio_profile"]         = portfolio_profile_df.to_pandas()
    rater["portfolio_profile_summary"] = summary_by_lob_df.to_pandas()