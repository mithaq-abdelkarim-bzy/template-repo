import hx
import numpy as np
import pandas as pd
import algorithms.rate_utilities as utils
from algorithms.premium_and_limit_profile.premium_and_limit_profile_helpers import (
    calculate_bst_share_ultimate_gross_premium,
    init_prem_limit_profile_df,
    calculate_bst_share_line_size,
    calculate_bst_deductions,
    calculate_bst_net_premium,
    calculate_portfolio_composition,
    calculate_portfolio_composition_sum,
    calculate_limit_profile_summary
)
from libraries.model_profiler.algorithms.profiling_hxd_functions         import time_me


# Processes and calculates various premium and limit profile metrics.
@time_me
def rate_premium_and_limit_profile(hxd, rater):    

    # Extract non-CDS (non-Credit Default Swap) risk code composition
    non_cds_rcc = hxd.non_cds.risk_code_composition
    prem_limit_profile_path = hxd.cds.prem_limit_profile

    # Exit early if there is no composition data to process
    if len(non_cds_rcc.final_composition) == 0:
        rater["prem_limit_data"] = pd.DataFrame({"selected_lob": []})
        return

    # Initialize profile DataFrame from existing composition data
    prem_limit_profile_df = init_prem_limit_profile_df(  prem_limit_profile_path, rater )

    # Calculate BST share line size (line size adjusted for BST assumptions)
    prem_limit_profile_df = calculate_bst_share_line_size(prem_limit_profile_df)

    # Compute BST share ultimate gross premium
    prem_limit_profile_df = calculate_bst_share_ultimate_gross_premium(prem_limit_profile_df)

    # Apply BST deductions (adjustments provided in deductions_df)
    prem_limit_profile_df = calculate_bst_deductions(
        prem_limit_profile_df, rater["deductions_df"]
    )

    # Compute net premium after BST deductions
    prem_limit_profile_df = calculate_bst_net_premium(prem_limit_profile_df)

    # Aggregate limit profile metrics into a summary dictionary
    limit_profile_sum_dict = calculate_limit_profile_summary(
        prem_limit_profile_df, prem_limit_profile_path
    )

    # Compute portfolio composition (relative share of each LOB in total portfolio)
    prem_limit_profile_df = calculate_portfolio_composition(
        prem_limit_profile_df, limit_profile_sum_dict
    )

    # Compute portfolio composition summary and update hxd
    calculate_portfolio_composition_sum(
        prem_limit_profile_df, prem_limit_profile_path
    )

    # Remove rows without a selected LOB
    # NK: Could this be filtered earlier (before calculations) to avoid unnecessary work on NaN rows.
    prem_limit_profile_df = prem_limit_profile_df[prem_limit_profile_df['selected_lob'].notna()]


    # Store result in rater dictionary for downstream use
    rater["prem_limit_data"] = prem_limit_profile_df