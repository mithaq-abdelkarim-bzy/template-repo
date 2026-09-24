import hx
import os
import pandas as pd
import algorithms.rate_utilities as utils


def get_to_usd_factor(currency_df, currency_code):
    # Select the "to_usd" conversion factor for the given currency_code
    row = currency_df.loc[currency_df["ccy"] == currency_code, "fx_rate"]

    # Return the factor if found, otherwise default to 1 (no conversion)
    return row.iloc[0] if not row.empty else 1


def calculate_base_to_account_fx_con(currencies_df, hxd):
    # Assume the base currency used in tables is USD
    table_base_currency = "USD"

    # Get the account currency from hxd configuration
    account_currency = hxd.cds.currencies.source_currency

    # Conversion factor: base currency (USD) → USD
    table_base_currency_to_usd = get_to_usd_factor(
        currencies_df, table_base_currency
    )

    # Conversion factor: account currency → USD
    account_currency_to_usd = get_to_usd_factor(
        currencies_df, account_currency
    )

    # Ratio gives conversion from table base currency → account currency
    base_to_account_fx_conv = account_currency_to_usd / table_base_currency_to_usd

    return base_to_account_fx_conv


def import_policy_level_data(hxd, rater, req_fields=None):
    if req_fields is None: 
        req_fields = []

    # Ensure 'facility_lob' is always included in required fields
    if "facility_lob" not in req_fields:
        req_fields += ["facility_lob"]
      
    policy_level_df = rater["policy_data"]

    # Filter out rows with missing 'facility_lob'
    policy_level_df_filtered = policy_level_df[policy_level_df['facility_lob'].notna()]

    # Reset index after filtering
    policy_level_df_filtered = policy_level_df_filtered.reset_index(drop=True)

    return policy_level_df_filtered


def show_hide_tab(hxd):
    # Determine if the policy-level tab should be shown
    is_shown = (
        hxd.cds.risk_information.prem_data_available 
        and not hxd.cds.risk_information.follow_main_syndicate
    )

    # Set visibility flag in hxd.non_cds
    hxd.non_cds.policy_level_data.is_shown = is_shown

