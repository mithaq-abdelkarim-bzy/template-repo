import math as math
import pandas as pd
from algorithms.rate_change.rate_change_helpers import (
    generate_years_dict,
    init_rate_change,
    set_facility_columns_headers,
    calculate_current_year_rate_change,
    calculate_past_years_rate_change
)
from libraries.model_profiler.algorithms.profiling_hxd_functions         import time_me


@time_me
def rate_rate_change(hxd, rater):
    
    # preparatory work
    non_cds_rcc = hxd.non_cds.risk_code_composition                                     # Extract non-CDS risk code composition data
    years_dict = generate_years_dict(hxd)                                               # Generate dictionary of year mappings for rate change
    set_facility_columns_headers(hxd, years_dict)                                       # Set up headers for facility columns based on years

    # Exit early if no final composition exists   
    if not non_cds_rcc.final_composition:
        rater["rate_change_data"] = pd.DataFrame()
        return

    # main calculation on rate change
    rate_change_df =    init_rate_change(                   hxd, rater, non_cds_rcc, years_dict   ) # Initialize rate change DataFrame with base structure
    rate_change_df =    calculate_current_year_rate_change( hxd, rater, rate_change_df            ) # Add current year's rate change calculations 
    rate_change_df =    calculate_past_years_rate_change(   hxd, rater, rate_change_df, years_dict) # Add historical rate change calculations

    # Store final DataFrame in rater dictionary
    rater["rate_change_data"] = rate_change_df[rate_change_df["selected_lob"].notna()]
