import hx
import pandas as pd
import polars as pl
import pyarrow as pa
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import rate_constants as constants
from libraries.model_profiler.algorithms.profiling_hxd_functions         import time_me

# helper function to handle missing columns in polars df
def ensure(df: pl.DataFrame, name: str, default):
    return (pl.col(name).fill_null(default) if name in df.columns else pl.lit(default)).alias(name)

# @time_me
def set_is_tab_shown(hxd):
    # Extract required flags from risk_information
    show_refs = hxd.cds.risk_information.show_refs
    priced_by = hxd.cds.risk_information.priced_by
    follow_main_syndicate = hxd.cds.risk_information.follow_main_syndicate

    # Show portfolio profile tab only when actuarial pricing is active, refs are shown, and not following main syndicate
    if (priced_by == "Actuarial") and show_refs and not follow_main_syndicate:
        hxd.non_cds.portfolio_profile.is_shown = True


# @time_me
def generate_years_dict(inception_date_year):
    # Map each year offset from inception_date_year to a label like 'year_0', 'year_1', ...
    return {
        str(inception_date_year - i): f"year_{i}"
        for i in range(constants.YEARS_TO_CONSIDER_IN_PORTFOLIO_PROFILE)
    }


# @time_me
def set_column_headers(tables, years_dict, hxd):
    # For each group/table, set dynamic year-based column headers in portfolio profile
    for group in tables:
        for year_attr, year_value in years_dict.items():
            setattr(     getattr(hxd.non_cds.portfolio_profile, group),     year_value,     year_attr)


# @time_me
def get_year_start(data_driven_rcc, inception_year):
    # Use input year_start if provided, else default to inception_year - 9
    selected_year = data_driven_rcc.year_start.selected
    return int(selected_year) if selected_year is not None else int(inception_year - 9)

# @time_me
def get_year_end(data_driven_rcc, inception_year):
    # Use input year_end if provided, else default to inception_year - 1
    selected_year = data_driven_rcc.year_end.selected
    return int(selected_year) if selected_year is not None else int(inception_year - 1)


# @time_me
def calculate_premium_and_weighting(portfolio_profile_df, policy_level_df, inception_date_year, hxd, final_code_composition_df):
    # Extract premium settings from Hx config
    data_driven_rcc = hxd.cds.risk_code_composition.data_driven_composition

    # Determine applicable year window
    year_start  = get_year_start(data_driven_rcc, inception_date_year)
    year_end    = get_year_end(data_driven_rcc, inception_date_year)

    # Pick premium column depending on Gross/Net basis
    premium_basis   = data_driven_rcc.premium_basis
    premium_col     = "gross_premium" if premium_basis == "Gross" else "net_premium"

    # Filter policies by year range and modelled flag
    filtered_policy_data = policy_level_df.filter(     (pl.col("yoa") >= year_start)
                                                    & (pl.col("yoa") <= year_end  )
                                                    & (pl.col("modelled") == "Yes")    )

    if filtered_policy_data.is_empty():
        # No data: set premiums to 0
        portfolio_profile_df = portfolio_profile_df.with_columns(     pl.lit(0).alias("selected_premium")       )
    else:
        # Group premiums by risk_code and LOB
        grouped_premiums = (    filtered_policy_data.group_by(["risk_code", "selected_lob"])
                                                    .agg(pl.col(premium_col).sum().alias("selected_premium"))   )

        # Merge premiums into portfolio profile
        portfolio_profile_df = portfolio_profile_df.join(  grouped_premiums, on=["risk_code", "selected_lob"], how="left"  )

        # Replace nulls with 0
        portfolio_profile_df = portfolio_profile_df.with_columns(   pl.col("selected_premium").fill_null(0)      )

    # Merge final composition to pull weighting (composition %) per risk code
    portfolio_profile_df = portfolio_profile_df.join(
        final_code_composition_df["composition", "risk_code", "selected_bp_class", "selected_lob"],
        how="left",
        right_on=["risk_code", "selected_bp_class", "selected_lob"],
        left_on=["risk_code", "bp_class", "selected_lob"]
    )

    # Assign weighting based on composition (default 0 if null)
    portfolio_profile_df = portfolio_profile_df.with_columns(   pl.col("composition").fill_null(0).fill_nan(0).alias("weighting")  )

    # Sort rows by descending premium
    portfolio_profile_df = portfolio_profile_df.sort(      by="selected_premium", descending=True    )

    return portfolio_profile_df



# @time_me
def init_hxd_output_nodes(portfolio_profile_df, summary_by_lob_df, hxd):
    # Initialize empty dict placeholders for CDS outputs
    hxd.cds.portfolio_profile.selected_lob_and_risk_code_combination = [{}] * portfolio_profile_df.height
    hxd.cds.portfolio_profile.summary_by_lob                         = [{}] * summary_by_lob_df.height


# @time_me
def calculate_rate_change_no_override(portfolio_profile_df, beazley_data_df, years_dict):
    """Calculate rate change (no override) for all years at once (vectorized)."""
    
    # Select only required columns
    beazley_data_subset = beazley_data_df.select(["yoa", "risk_code", "rate_change"])
    
    # Create year-to-column mapping
    year_to_col         = {int(year): col for year, col in years_dict.items()}
    
    # Map each year to its target column name
    beazley_with_cols = beazley_data_subset.with_columns( pl.col("yoa")
                                                            .map_elements(   lambda y: year_to_col.get(int(y))
                                                                           , return_dtype=pl.Utf8)
                                                            .alias("column_name")    )
    
    # Pivot once: reshape from long to wide (one column per year)
    beazley_pivoted = beazley_with_cols.pivot(  on="column_name",
                                                values="rate_change",
                                                index="risk_code",
                                                aggregate_function="sum"    )
    
    # Rename columns with prefix
    rename_map = {  col: f"rate_change_no_override/{col}"    for col in beazley_pivoted.columns    if col != "risk_code"}
    beazley_pivoted = beazley_pivoted.rename(rename_map)
    
    # Single join (not per-year)
    result_df = portfolio_profile_df.join(  beazley_pivoted,    on="risk_code",    how="left"   )
    
    # Fill all missing values with 0 in one expression
    fill_exprs = [  pl.col(f"rate_change_no_override/{col}").fill_null(1)     for year, col in years_dict.items()    ]              # JB updated filler to be 1 26/2/2026
    result_df = result_df.with_columns(fill_exprs)
    
    return result_df



# @time_me
def get_lloyds_data(portfolio_profile_df, years_dict, hxd):
    # Load Lloyds risk code data from hx.params (pre-loaded table)
    lloyds_risk_code_data = hx.params.table_lloyds_risk_code_data

    # Convert Pandas DataFrame to Arrow table, then to Polars DataFrame
    arrow_table = pa.Table.from_pandas(lloyds_risk_code_data, preserve_index=False)
    lloyds_risk_code_data_pl = pl.from_arrow(arrow_table)

    # Extract unique years of account (yoa) & Convert years to integers and sort ascending
    unique_years = lloyds_risk_code_data_pl.select("yoa").unique().to_series().to_list()
    unique_years = sorted(map(int, unique_years))

    # Build dictionary mapping reversed years to year_n style keys
    adjusted_dict = {     f"year_{i+1}": str(year) for i, year in enumerate(reversed(unique_years))     }

    # Determine list of columns to create in portfolio_profile_df
    columns_to_update = []
    for column_name in years_dict.values():
        columns_to_update.extend(   [   f"lloyds_incurred_development/{column_name}",
                                        f"lloyds_paid_development/{column_name}",
                                        f"lloyds_premium_development/{column_name}"    ]  )

    # Add placeholder columns initialized to 0
    for col in columns_to_update:
        portfolio_profile_df = portfolio_profile_df.with_columns(    pl.lit(0).alias(col)   )

    # Collect unique risk codes from portfolio_profile_df
    unique_risk_codes = (    portfolio_profile_df.select("risk_code").unique().to_series().to_list()            )

    # Loop over each metric type
    for metric in ["incurred_development", "paid_development", "premium_development"]:
        # Add base column year_0 for each metric initialized to 0
        portfolio_profile_df = portfolio_profile_df.with_columns(   pl.lit(0).alias(f"lloyds_{metric}/year_0")  )

        # Extract relevant columns and filter by unique risk codes
        filtered_df = ( lloyds_risk_code_data_pl.select(["yoa", "lloyds_risk_code", metric])
                                                .rename({metric: "value"})
                                                .filter(pl.col("lloyds_risk_code").is_in(unique_risk_codes))    )

        # Build mapping from yoa → year_key
        yoa_to_year_key = {v: k for k, v in adjusted_dict.items()}
        mapping_df      = pl.DataFrame(   {   "yoa":      list(yoa_to_year_key.keys())
                                            , "year_key": list(yoa_to_year_key.values())  })

        # Build new column containing future column names in the form "lloyds_metric/year_x"
        filtered_df = filtered_df.with_columns(pl.col("yoa").cast(str))         # Ensure yoa is string for consistent joining
        filtered_df = filtered_df.join(mapping_df, on="yoa", how="left")        # Add year_key column using yoa
        filtered_df = filtered_df.filter(pl.col("year_key").is_not_null())      # Drop nulls
        filtered_df = filtered_df.with_columns(   (pl.lit(f"lloyds_{metric}/") + pl.col("year_key")).alias("column_name")   )

        # Pivot table to wide format with risk_code as index
        pivot_df = (     filtered_df.pivot(   values="value"
                                            , index="lloyds_risk_code"
                                            , columns="column_name"
                                            , aggregate_function="sum"  )
                                    .rename({"lloyds_risk_code": "risk_code"})
                                    .fill_null(0)                               )

        # Remove any existing overlapping columns from portfolio_profile_df
        columns_to_drop      = [col for col in pivot_df.columns if col != "risk_code"]
        portfolio_profile_df = portfolio_profile_df.drop(columns_to_drop)

        # Join pivoted Lloyds data back into portfolio_profile_df and replace nulls with 0
        portfolio_profile_df = portfolio_profile_df.join(  pivot_df, on="risk_code", how="left"   )
        portfolio_profile_df = portfolio_profile_df.fill_null(0)

    return portfolio_profile_df


# @time_me
def save_selected_lob_and_risk_code_combination(portfolio_profile_df, output_columns, hxd):
    # Write subset of portfolio_profile_df to HxD node
    try:
        utils.write_pl_to_hxd(
            portfolio_profile_df,
            hxd.cds.portfolio_profile.selected_lob_and_risk_code_combination,
            output_columns,
        )

    except:
        utils.write_pl_to_hxd(
            portfolio_profile_df,
            hxd.cds.portfolio_profile.selected_lob_and_risk_code_combination,
            output_columns,
        )


# @time_me
def generate_summary_by_lob_df(summary_by_lob_df, portfolio_profile_df, years_dict, tables):
    weighted_col_data = {}   # Store weighted column computations
    final_result_data = {}   # Store final weighted averages

    # Compute weighted columns for each group and year
    for group in tables:
        for column_name in years_dict.values():
            metric_col = f"{group}/{column_name}"  # e.g., 'rate_change/year_0'
            weighted_col = f"{metric_col}_weighted"

            # Multiply metric by weighting to prep for weighted avg calc
            weighted_col_data[weighted_col] = portfolio_profile_df.select(  (pl.col(metric_col) * pl.col("weighting")).alias(weighted_col) )[weighted_col]

    # Add all weighted columns to portfolio_profile_df
    portfolio_profile_df = portfolio_profile_df.hstack(pl.DataFrame(weighted_col_data))

    # Compute weighted averages grouped by selected_lob
    for group in tables:
        for column_name in years_dict.values():
            metric_col = f"{group}/{column_name}"
            weighted_col = f"{metric_col}_weighted"
            filler = 1 if group in ['rate_change_no_override','rate_change_with_selection_override'] else 0                     # JB updated filler to be variable 26/2/2026

            # Weighted sum of metric for each lob
            weighted_sum    = ( portfolio_profile_df.group_by("selected_lob")
                                                    .agg(   pl.col(weighted_col).sum()
                                                              .alias("weighted_sum")       ))
            # Total weights for each lob
            weight_sum      = ( portfolio_profile_df.group_by("selected_lob")
                                                    .agg(   pl.col("weighting").sum()
                                                              .alias("weight_sum")         ))

            # Weighted average = weighted_sum / weight_sum
            weighted_avg    = (weighted_sum.join(weight_sum, on="selected_lob")
                                           .with_columns(   (pl.col("weighted_sum") / pl.col("weight_sum"))
                                                            .fill_nan(  filler  )
                                                            .alias("weighted_avg")         ))

            # Map back to summary_by_lob_df
            final_result_data[metric_col] = summary_by_lob_df.join( weighted_avg.select(["selected_lob", "weighted_avg"])
                                                                    , on="selected_lob"
                                                                    , how="left"      )["weighted_avg"].fill_null(  filler  )

    # Convert collected results into a Polars DataFrame
    final_result_df = pl.DataFrame(final_result_data)

    # Update existing columns
    for col in final_result_df.columns:
        if col in summary_by_lob_df.columns:
            summary_by_lob_df = summary_by_lob_df.with_columns(       final_result_df[col].alias(col)        )

    # Add any new columns not already in summary_by_lob_df
    new_columns = [col for col in final_result_df.columns if col not in summary_by_lob_df.columns]
    if new_columns:
        summary_by_lob_df = summary_by_lob_df.hstack(final_result_df.select(new_columns))

    # Drop temporary weighted columns from portfolio_profile_df
    portfolio_profile_df = portfolio_profile_df.drop(list(weighted_col_data.keys()))

    # Sort summary_by_lob_df by weighting, descending
    summary_by_lob_df = summary_by_lob_df.sort("weighting", descending=True)

    return summary_by_lob_df



# @time_me
def calculate_rate_change_with_selection_override(hxd, portfolio_profile_df, beazley_data_df, years_dict, rater):
    # Convert raw rate change data from hx list into Polars DataFrame
    rate_change_df = rater.get('rate_change_data', pd.DataFrame())
    rate_change_df = utils.pd_to_pl_df(rate_change_df)
    years_items = list(years_dict.items())
    result_df = portfolio_profile_df

    for idx, (year, column_name) in enumerate(years_items):
        year = int(year)

        # Get Beazley fallback rate change data for the given year
        beazley_fallback = ( beazley_data_df.filter(pl.col('yoa') == year)
                                            .select(['risk_code', 'rate_change'])      )

        # Join fallback into portfolio profile
        fallback_map = ( result_df.join( beazley_fallback, on='risk_code', how='left'        )
                                  .with_columns([pl.col('rate_change').fill_null(1).alias('fallback')])['fallback'])    # JB updated to filler of 1 26/2/2026

        if idx == 0:
            # First year: pull from selected rate change
            selected_map = ( rate_change_df.select([  pl.col(f'{column_name}/selected').alias("rate_change")
                                                    , pl.col('selected_lob')])       )

            final        = (result_df.join(  selected_map, on='selected_lob', how='left')
                                     .with_columns([ pl.col('rate_change').fill_null(1)                                 # JB updated to filler of 1 26/2/2026
                                                       .alias(f'rate_change_with_selection_override/{column_name}') ]))

        elif idx < constants.YEARS_TO_CONSIDER_IN_RATE_CHANGE:
            # Mid-years: combine selected & facility rate changes, fall back if facility = 0
            selected_map = ( rate_change_df.select([   pl.col(f'{column_name}/selected').alias("selected_rate_change")
                                                     , pl.col('selected_lob')]))
            facility_map = ( rate_change_df.select([   pl.col(f'{column_name}/facility').alias("facility_rate_change")
                                                     , pl.col('selected_lob')]))

            temp = ( result_df.join(selected_map, on='selected_lob', how='left') 
                              .join(facility_map, on='selected_lob', how='left') 
                              .with_columns([   pl.col('selected_rate_change').fill_null(1)                             # JB updated to filler of 1 26/2/2026
                                              , pl.col('facility_rate_change').fill_null(0)  ]))                        # deliberately left as nil to facilitate test below

            # Use fallback when facility rate change = 0
            selected_or_fallback = ( temp.with_columns([ pl.when(pl.col('facility_rate_change') == 0)
                                                           .then(fallback_map)
                                                           .otherwise(pl.col('selected_rate_change'))
                                                           .alias(f'rate_change_with_selection_override/{column_name}')]))
            final = selected_or_fallback

        else:
            # Later years: only fallback values are used
            final = result_df.with_columns([ fallback_map.alias(f'rate_change_with_selection_override/{column_name}') ])

        # Update the result_df with calculated rate change for this year
        result_df = result_df.with_columns([ final[f'rate_change_with_selection_override/{column_name}']  ])

    return result_df



# @time_me
def save_summary_by_lob_df(summary_by_lob_df, output_columns, hxd):
    # Write subset of summary_by_lob_df to HxD node
    utils.write_pl_to_hxd( summary_by_lob_df, hxd.cds.portfolio_profile.summary_by_lob, output_columns   )





# @time_me
def get_proj_risk_code_result(hxd, portfolio_profile_df: pl.DataFrame, rater) -> pl.DataFrame:
    # Load Lloyd's projections summary as a Polars DataFrame
    lloyds_proj_summary = rater.get('proj_lloyds_summary', pd.DataFrame())
    lloyds_proj_summary = utils.pd_to_pl_df( lloyds_proj_summary )
    # Load Beazley projections summary as a Polars DataFrame
    beazley_proj_summary = rater.get('proj_beazley_summary', pd.DataFrame())
    beazley_proj_summary = utils.pd_to_pl_df( beazley_proj_summary )

    # Trim Lloyd's summary to match portfolio profile row count
    lloyds_proj_summary = lloyds_proj_summary.slice(0, portfolio_profile_df.height)
    # Trim Beazley summary to match portfolio profile row count
    beazley_proj_summary = beazley_proj_summary.slice(0, portfolio_profile_df.height)

    # Select required columns from Lloyd's summary and fill missing values
    lloyds_proj_summary = (lloyds_proj_summary
                            .with_columns([ ensure(lloyds_proj_summary, "selected_final_gn_ulr", 0.0),
                                            ensure(lloyds_proj_summary, "selected_ielr",         0.0),
                                            ensure(lloyds_proj_summary, "model_ielr",            0.0),
                                            ensure(lloyds_proj_summary, "risk_code",             "TEMP"),
                                            ensure(lloyds_proj_summary, "bp_class",              "TEMP"),
                                            ensure(lloyds_proj_summary, "selected_lob",          "TEMP"), ])
                            .select(["selected_lob", "risk_code", "bp_class", "selected_final_gn_ulr", "selected_ielr", "model_ielr"]))

    # Select required columns from Beazley summary and fill missing values
    beazley_proj_summary = (beazley_proj_summary
                            .with_columns([
                                ensure(beazley_proj_summary, "selected_final_gn_ulr", 0.0).alias("beazley_risk_code_results/final_gn_ulr"),
                                ensure(beazley_proj_summary, "risk_code",  "TEMP"),
                                ensure(beazley_proj_summary, "bp_class",   "TEMP"),
                                ensure(beazley_proj_summary, "selected_lob", "TEMP"),])
                            .select(["selected_lob", "risk_code", "bp_class", "beazley_risk_code_results/final_gn_ulr"]))



    # Join Lloyd's summary data with portfolio profile on lob, risk code, and class
    portfolio_profile_df = portfolio_profile_df.join( lloyds_proj_summary,  on=["selected_lob", "risk_code", "bp_class"],  how='left'  )

    # Join Beazley summary data with portfolio profile on lob, risk code, and class
    portfolio_profile_df = portfolio_profile_df.join( beazley_proj_summary, on=["selected_lob", "risk_code", "bp_class"],  how='left'  )

    # Add renamed columns with filled defaults for Lloyd's and Beazley results
    portfolio_profile_df = portfolio_profile_df.with_columns([
        pl.col("selected_final_gn_ulr").fill_null(0).alias("lloyds_risk_code_results/final_gn_ulr"),
        pl.col("selected_ielr").fill_null(0).alias("lloyds_risk_code_results/selected_ielr"),
        pl.col("model_ielr").fill_null(0).alias("lloyds_risk_code_results/model_ielr"),
        pl.col("beazley_risk_code_results/final_gn_ulr").fill_null(0)
    ])

    # Return updated portfolio profile with projection results
    return portfolio_profile_df

# @time_me
def get_proj_lob_summary_result(hxd, summary_by_lob_df: pl.DataFrame, own_exp_summary: pl.DataFrame) -> pl.DataFrame:
    # Select required columns from own experience summary and fill missing values

    own_exp_summary = ( own_exp_summary
                        .with_columns([ ensure(own_exp_summary, "lloyds_final_gn_ulr",  0.0),
                                        ensure(own_exp_summary, "lloyds_selected_ielr", 0.0),
                                        ensure(own_exp_summary, "lloyds_model_ielr",    0.0),
                                        ensure(own_exp_summary, "beazley_final_gn_ulr", 0.0),
                                        ensure(own_exp_summary, "selected_lob",         "TEMP")])
                        .select(["selected_lob",        "lloyds_final_gn_ulr",  "lloyds_selected_ielr",
                                "lloyds_model_ielr",    "beazley_final_gn_ulr"                          ]))


    # Join own experience summary with summary by LOB on selected LOB
    summary_by_lob_df = summary_by_lob_df.join(
        own_exp_summary,
        on=["selected_lob"],
        how='left'
    )

    # Add renamed columns for Lloyd's and Beazley results to summary
    summary_by_lob_df = summary_by_lob_df.with_columns([
        pl.col("lloyds_final_gn_ulr").alias("lloyds_risk_code_results/final_gn_ulr"),
        pl.col("lloyds_selected_ielr").alias("lloyds_risk_code_results/selected_ielr"),
        pl.col("lloyds_model_ielr").alias("lloyds_risk_code_results/model_ielr"),
        pl.col("beazley_final_gn_ulr").alias("beazley_risk_code_results/final_gn_ulr"),
    ])

    # Return updated summary with projection results
    return summary_by_lob_df

