import hx
import algorithms.rate_constants as constants
import numpy as np
from algorithms.claim_level_data.input_claim_level import sov_column_mapping_similarity_score_claim_level
from algorithms import parameter_tables_schema as params
from algorithms.claim_level_data.claim_level_helpers import (
    check_duplicates_for_renew_columns,
    show_hide_tab,
    import_claim_level_data,
    calculate_base_to_account_fx_con
)
from libraries.model_profiler.algorithms.profiling_hxd_functions         import time_me

@time_me
def rate_claims_level(hxd, rater):
    # Run similarity checks on column mappings for claim-level data
    sov_column_mapping_similarity_score_claim_level(hxd)

    # Check for duplicate entries in renew_column mapping
    check_duplicates_for_renew_columns(hxd)

    # Load currency conversion table and compute base→account FX rate
    fx_rates_df = params.fx_rates.df()
    
    base_to_account_fx_con = calculate_base_to_account_fx_con(fx_rates_df, hxd)

    # Show/hide claim-level tab depending on availability flags
    show_hide_tab(hxd)

    # Set required fields for claim-level data table (validation hint for users)
    hxd.cds.claim_level_data_table.req_fields = (
        "Please ensure the following fields are completed before submitting, "
        "at a minimum: Account Name, Facility LoB, Year of Account, Currency, "
        "Claim Type, Incurred; Where Claim Type must be one of "
        "'Attritional', 'Large', 'CAT"
    )

    # Columns expected in claim-level dataset
    claim_data_fields = constants.claim_data_fields

    # Import claim-level data into DataFrame
    claim_level_df = import_claim_level_data(hxd, rater, claim_data_fields)

    # Financial fields requiring numeric conversion
    fields_to_convert = ["paid", "outstanding", "incurred"]

    # Force numeric dtype for math operations (NaNs remain NaN)
    claim_level_df[fields_to_convert] = claim_level_df[fields_to_convert].astype(float)

    # Build dictionary: currency → USD conversion factor
    currency_map = dict(zip(fx_rates_df['ccy'], fx_rates_df['fx_rate']))

    # Add column for conversion from original currency to USD (default 1 if missing)   
    claim_level_df['data_to_usd'] = (
        claim_level_df['currency']
        .map(currency_map)
        .fillna(1)
    )

    # Calculate multiplier for converting into account’s reporting currency
    claim_level_df['data_to_cnv'] = base_to_account_fx_con / claim_level_df['data_to_usd']

    # For each financial field, create converted values (_cnv suffix)
    for field in fields_to_convert:
        claim_level_df[field + "_cnv"] = claim_level_df[field].fillna(0) * claim_level_df['data_to_cnv']

    # Store DataFrame in rater for downstream use
    rater["claim_data"] = claim_level_df