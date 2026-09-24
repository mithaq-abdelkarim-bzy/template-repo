import hx
import numpy as np
from algorithms import parameter_tables_schema as params
from algorithms.policy_level_data.input_policy_level import (
    sov_column_mapping_similarity_score_policy_level, 
    check_duplicates_for_renew_columns
)
from algorithms.policy_level_data.policy_level_helpers import (
    calculate_base_to_account_fx_con, 
    import_policy_level_data,
    show_hide_tab,
)
import algorithms.rate_constants as constants
from libraries.model_profiler.algorithms.profiling_hxd_functions         import time_me


@time_me
def rate_policy_level(hxd, rater):
    # Run helper to check similarity scores on SoV (schedule of values) policy-level data
    sov_column_mapping_similarity_score_policy_level(hxd)

    # Run helper to check for duplicate values in renew columns
    check_duplicates_for_renew_columns(hxd)

    # Load currency conversion table
    fx_rates_df = params.fx_rates.df()

    # Compute conversion factor: table base currency → account currency
    base_to_account_fx_con = calculate_base_to_account_fx_con(
        fx_rates_df, hxd
    )

    # Decide whether to show/hide the policy-level tab
    show_hide_tab(hxd)

    # Store a user-facing string that lists required fields
    hxd.cds.policy_level_data_table.req_fields = (
        "Please ensure the following fields are completed before submitting, "
        "at a minimum: Account Name, Facility LoB, Year of Account, Currency, "
        "Gross Premium, Net Premium, Total Incurred"
    )
    hxd.cds.rationale.polcy_claim_data_msg = (
        "Write Policy/Claim Level Data to HXD for Renewal"
    )

    # Define expected fields to load for policy-level data  
    # Import the policy-level data from hxd
    policy_level_df = import_policy_level_data(hxd, rater, constants.policy_data_fields)   


    # Ensure numeric fields are floats, fill missing with 0 for calculations
    fields_to_convert                   = constants.policy_fields_to_convert
    policy_level_df[fields_to_convert]  = (policy_level_df[fields_to_convert].astype(float).fillna(0))

    # Build a dictionary mapping currency → conversion factor to USD
    currency_map = dict(zip(fx_rates_df['ccy'], fx_rates_df['fx_rate']))

    # Create a column with the USD conversion factor for each row
    policy_level_df['data_to_usd'] = (  policy_level_df['currency'].map(currency_map).fillna(1)  )

    # Compute conversion factor to account currency: base_to_account / row_to_usd
    policy_level_df['data_to_cnv'] = (  base_to_account_fx_con / policy_level_df['data_to_usd']  )

    # Apply conversion to each numeric field, creating "_cnv" columns
    for field in fields_to_convert:
        policy_level_df[field + "_cnv"] = policy_level_df[field].fillna(0) * policy_level_df['data_to_cnv']

    # Calculate incurred total as sum of converted components
    policy_level_df["total_from_sum_cnv"] = policy_level_df[
        ["incurred_large_cnv", "incurred_cat_cnv", "incurred_attritional_cnv"]
    ].sum(axis=1)

    # If total_from_sum_cnv is nonzero, overwrite incurred_total_cnv with it
    policy_level_df["incurred_total_cnv"] = np.where(
        policy_level_df["total_from_sum_cnv"] == 0,
        policy_level_df["incurred_total_cnv"],
        policy_level_df["total_from_sum_cnv"],
    )

    # Store final DataFrame into rater dict
    rater["policy_data"] = policy_level_df