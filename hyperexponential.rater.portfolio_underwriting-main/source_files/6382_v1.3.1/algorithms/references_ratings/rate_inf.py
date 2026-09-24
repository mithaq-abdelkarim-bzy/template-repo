import hx
import pandas as pd
import algorithms.rate_utilities as utils
import algorithms.rate_constants as const
from libraries.model_profiler.algorithms.profiling_hxd_functions         import time_me

def _process_inflation_table(df, hxd_attr, rater_key, rater, hxd):
    """Shared helper for rate_base_inf and rate_excess_inf."""
    
    df = df.rename(columns={'Business Plan Class': 'bp_class'})
    
    start_yr = hxd.hx_core.inception_date.year
    end_yr   = start_yr - const.YEARS_TO_CONSIDER_IN_Inflation
    years = list(range(start_yr, end_yr, -1))

    # --- fill missing years by using previous year ---
    for y in years:
        col = str(y)
        if col not in df:
            prev = y - 1
            while str(prev) not in df and prev >= years[-1]:
                prev -= 1
            df[col] = df[str(prev)] if str(prev) in df else pd.NA
    # -------------------------------------------------

    year_rename_map = {str(year): f'year_{i}' for i, year in enumerate(years)}
    df = df.rename(columns=year_rename_map)

    columns_to_keep = ['bp_class'] + list(year_rename_map.values())
    df = df[columns_to_keep]
    
    # Set attributes on the provided hxd object
    for i, year in enumerate(years):
        setattr(hxd_attr, f'year_{i}', year)
    
    rater[rater_key] = df

@time_me
def rate_base_inf(hxd, rater):
    _process_inflation_table(
        hx.params.table_base_inf, 
        hxd.non_cds.base_inf, 
        "base_inf_df", 
        rater, 
        hxd
    )

@time_me
def rate_excess_inf(hxd, rater):
    _process_inflation_table(
        hx.params.table_excess_inf, 
        hxd.non_cds.excess_inf, 
        "excess_inf_df", 
        rater, 
        hxd
    )