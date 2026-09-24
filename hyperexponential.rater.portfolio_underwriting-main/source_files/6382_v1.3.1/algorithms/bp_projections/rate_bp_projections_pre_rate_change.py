import hx
import pandas as pd
import math as math
import algorithms.rate_utilities as utils
from algorithms.bp_projections.bp_projections_helpers import (
    set_is_tab_shown,
    init_bp_details,
    init_bp_summary_by_lob
)
from libraries.model_profiler.algorithms.profiling_hxd_functions         import time_me

@time_me
def rate_bp_projections_pre_rate_change(hxd, rater):
    # Ensure tab visibility conditions are checked
    set_is_tab_shown(hxd)

    # Exit early if no final composition data is present
    if not hxd.non_cds.risk_code_composition.final_composition or hxd.non_cds.risk_code_composition.final_composition == [{}]:
        bp_details = pd.DataFrame({})
        bp_summary_by_lob = pd.DataFrame({})
    else:
        # Build Table 3 (details) and Table 2 (summary by LOB)
        bp_details = init_bp_details(hxd, rater)
        bp_summary_by_lob = init_bp_summary_by_lob(hxd, bp_details,rater)

    # Store results back into rater dictionary
    rater["bp_details"] = bp_details
    rater["bp_summary_by_lob"] = bp_summary_by_lob