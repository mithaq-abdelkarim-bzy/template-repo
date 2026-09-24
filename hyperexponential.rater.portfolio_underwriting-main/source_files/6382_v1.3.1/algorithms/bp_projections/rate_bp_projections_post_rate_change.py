import math as math
import algorithms.rate_utilities as utils
import pandas as pd
from algorithms.bp_projections.bp_projections_helpers import (
    build_bp_details,
    build_bp_summary_by_lob
)
from libraries.model_profiler.algorithms.profiling_hxd_functions         import time_me

@time_me
def rate_bp_projections_post_rate_change(hxd, rater):
    # Exit early if no final composition data is available
    if not hxd.non_cds.risk_code_composition.final_composition or hxd.non_cds.risk_code_composition.final_composition == [{}]:
        return

    # Build Table 3 (BP details) after applying rate change calculations
    bp_details = build_bp_details(hxd, rater["bp_details"], rater["rate_change_data"])
    
    # Build Table 2 (BP summary aggregated by line of business)
    bp_summary_by_lob = build_bp_summary_by_lob(hxd, bp_details, rater["bp_summary_by_lob"])
    
    # Table 1 is currently disabled but could be added back if needed
    # build_table_1(hxd, bp_details)

    # Update rater with new details and summary results
    rater["bp_details"] = bp_details
    rater["bp_summary_by_lob"] = bp_summary_by_lob