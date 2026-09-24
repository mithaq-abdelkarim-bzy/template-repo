import hx
import os
import pandas as pd
import algorithms.rate_utilities as utils


def check_duplicates_for_renew_columns(hxd):
    # Convert the unformatted file column mapping into a DataFrame
    col_mapping_df = utils.pd_df_from_hx_list(
        hxd.cds.claim_level_data_table.unformatted_file_column_mapping
    )

    # Extract the 'renew_column' values, drop NaNs, reset index for alignment
    renew_col_non_na = col_mapping_df["renew_column"].dropna().reset_index(drop=True)

    # Create a mask where duplicate values exist (keep=False marks all occurrences)
    duplicate_mask = renew_col_non_na.duplicated(keep=False)

    # If duplicates exist, log a warning and flag in hxd
    if duplicate_mask.any():
        duplicates = renew_col_non_na[duplicate_mask].unique().tolist()
        hx.errors.validation(
            f"WARNING: Duplicate values found in 'renew_column' (Claim Level Data): {duplicates}"
        )
        hxd.non_cds.claim_level_data.duplicate_found = True
    else:
        # Otherwise, mark as no duplicates found
        hxd.non_cds.claim_level_data.duplicate_found = False 



def get_to_usd_factor(currency_df, currency_code):
    # Select the "to_usd" conversion factor for the given currency_code
    row = currency_df.loc[currency_df["ccy"] == currency_code, "fx_rate"]

    # Return the factor if found, otherwise default to 1 (no conversion)
    return row.iloc[0] if not row.empty else 1


def calculate_base_to_account_fx_con(currencies_df, hxd):
    # Assume the base currency in the tables is USD
    table_base_currency = "USD"

    # Get the account currency from hxd config
    account_currency = hxd.cds.currencies.source_currency

    # Conversion factor: base currency (USD) → USD
    table_base_currency_to_usd = get_to_usd_factor(currencies_df, table_base_currency)

    # Conversion factor: account currency → USD
    account_currency_to_usd = get_to_usd_factor(currencies_df, account_currency)

    # Ratio provides conversion factor: table base currency → account currency
    base_to_account_fx_conv = account_currency_to_usd / table_base_currency_to_usd

    return base_to_account_fx_conv


def show_hide_tab(hxd):
    # Determine whether the claim-level tab should be visible
    is_shown = (
        hxd.cds.risk_information.det_claims_data_available
        and not hxd.cds.risk_information.follow_main_syndicate
    )

    # Update hxd with visibility flag
    hxd.non_cds.claim_level_data.is_shown = is_shown


def import_claim_level_data(hxd, rater, req_fields=[]):
    # Always ensure 'facility_lob' is in required fields
    if "facility_lob" not in req_fields:
        req_fields += ["facility_lob"]


    # Convert hxd list into DataFrame with required fields
    claim_level_df = rater["claim_data"]

    # Filter out rows with missing facility_lob
    claim_level_df_filtered = claim_level_df[claim_level_df['facility_lob'].notna()]

    return claim_level_df_filtered