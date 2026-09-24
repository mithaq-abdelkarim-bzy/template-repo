import hx
import numpy as np
import algorithms.rate_utilities as utils
import pandas as pd
from scipy.stats import lognorm
import algorithms.rate_constants as constants


def calculate_lognorm_inv(probability):
    # Set lognormal distribution parameters
    mu = 12
    sigma = 2
    # Compute inverse CDF (quantile) for given probability
    quantile = lognorm.ppf(1 - probability, s=sigma, scale=np.exp(mu))
    # Scale down result
    return quantile / 3

# NK: As this is used a few times is it better to load a dict map once?
def get_to_usd_factor(currency_df, currency_code):
    # Find row for given currency
    row = currency_df.loc[currency_df["ccy"] == currency_code, "fx_rate"]
    # Return conversion factor, default to 1 if missing
    return row.iloc[0] if not row.empty else 1


def set_return_period_and_critical_prob(cat_path):
    # Define standard catastrophe return periods
    return_periods = [
        "one_in_10000", "one_in_5000", "one_in_1000", "one_in_500",
        "one_in_250", "one_in_200", "one_in_100", "one_in_50",
        "one_in_30", "one_in_10", "one_in_5", "one_in_2"
    ]
    # Loop through return periods and compute critical probabilities
    for field in return_periods:              
        rp_field = getattr(cat_path, field)
        return_period = getattr(rp_field, "return_period")
        return_period = return_period if return_period is not None else 0
        critical_prob = 1 / return_period if return_period != 0 else 0
        setattr(rp_field, "critical_prob", critical_prob)
    return return_periods


def calculate_and_save_cov(aal, standard_deviation, cat_path, curve):
    # Only compute if both values exist and aal is non-zero (to avoid division by zero)
    if aal is not None and standard_deviation is not None and aal != 0:
        # Coefficient of variation = std dev / mean
        cov = standard_deviation / aal
        # Save COV under curve node
        setattr(cat_path.cov, curve, cov)
        return cov
    return None


def calculate_and_save_unadjusted_ulr(cat_path, aal, curve, rater):
    # Get premium for given curve
    gn_in_force_premium = getattr(cat_path.gn_in_force_premium, curve)
    # Only compute if both values exist and gn_in_force_premium is non-zero (to avoid division by zero)
    if aal is not None and gn_in_force_premium is not None and gn_in_force_premium != 0:
        # Unadjusted ULR = AAL / Premium
        unadjusted_gn_cat_ulr = aal / gn_in_force_premium
        # Save result under curve node
        setattr(cat_path.unadjusted_gn_cat_ulr, curve, unadjusted_gn_cat_ulr)
        return unadjusted_gn_cat_ulr
    return None


def get_rate_change_factor(cat_path, hxd, curve, selected_lob, is_roll_forward, rater):
    # If not roll-forward, default factor is 1
    if not is_roll_forward:
        rate_change_factor = 1
    else:
        # Convert to DataFrame
        rate_change_df = rater.get("rate_change_data", pd.DataFrame())       
        # Check if data exists and LOB is selected
        if (not rate_change_df.empty) and selected_lob:
            # Filter for LOB row
            filtered_df = rate_change_df.loc[rate_change_df["selected_lob"] == selected_lob, 'year_0/selected']
            # Extract factor or set 0 if missing
            rate_change_factor = filtered_df.iat[0] if not filtered_df.empty else 0
        else:
            rate_change_factor = 0
    # Save factor under curve node
    rate_change_node = getattr(cat_path.rate_change_factor, curve)
    setattr(rate_change_node, "calculated", rate_change_factor)
    return rate_change_node.override if rate_change_node.is_overridden else rate_change_factor 


def get_inflation_factor(cat_path, hxd, curve, selected_lob, is_roll_forward, rater):
    # If not roll-forward, default factor is 1
    if not is_roll_forward:
        inflation_factor = 1
    else:
        # Check if data exists and LOB is selected
        inf_summary_path = hxd.cds.inflation.summary_by_lob
        if inf_summary_path and selected_lob:
            # Convert to DataFrame
            inflation_summary_df = rater.get("inflation_by_lob", pd.DataFrame())
            # Filter for selected LOB
            lob_mask = inflation_summary_df["selected_lob"] == selected_lob
            filtered_df = inflation_summary_df.loc[lob_mask, 'year_0']
            # Extract value and add 1 (base adjustment)
            inflation_factor = filtered_df.iat[0] + 1 if not filtered_df.empty else 0
        else:
            inflation_factor = 0
    # Save factor under curve node
    inflation_node = getattr(cat_path.inflation_factor, curve)
    setattr(inflation_node, "calculated", inflation_factor)
    return inflation_node.override if inflation_node.is_overridden else inflation_factor 


def set_selected_class_dropdowns(hxd, prem_limit_profile_df):
    # Extract unique LOBs
    lobs = (
        prem_limit_profile_df
        .dropna(subset=["selected_lob"])
        .drop_duplicates(subset=["selected_lob"])
        ["selected_lob"]
        .unique()
    )
    # Assign dropdown values for each curve  
    for i in range(1, constants.NUM_CURVES_IN_CAT):
        setattr(hxd.cds.cat.selected_class, f"selected_class_drop_down_{i}", lobs)


def calculate_selected_gn_cat_ulr(cat_path, curve, inflation_factor, rate_change_factor, is_override=False):
    # Get unadjusted ULR for curve
    unadjusted_gn_cat_ulr = getattr(cat_path.unadjusted_gn_cat_ulr, curve, None)
    # If values exist, adjust for inflation and rate change
    if unadjusted_gn_cat_ulr is not None and all([inflation_factor, rate_change_factor]):
        selected_gn_cat_ulr = unadjusted_gn_cat_ulr * inflation_factor / rate_change_factor
    else:
        selected_gn_cat_ulr = 0
    # Save adjusted ULR, respecting override flag
    selected_gn_cat_ulr_node = cat_path.selected_gn_cat_ulr
    if is_override:
        selected_gn_cat_ulr_node = getattr(selected_gn_cat_ulr_node, curve)
        setattr(selected_gn_cat_ulr_node, "calculated", selected_gn_cat_ulr)
    else:
        setattr(selected_gn_cat_ulr_node, curve, selected_gn_cat_ulr)


def get_modelling_fX_conv(cat_path, hxd, currencies_df):
    # Define base currency for table
    table_base_currency = 'USD'
    # Conversion factor for base currency
    table_base_currency_to_usd = get_to_usd_factor(currencies_df, table_base_currency)
    # Get account and modelling currencies
    account_currency = hxd.cds.currencies.source_currency
    modelling_currency = cat_path.currency
    # Convert from base to account currency
    base_to_account_fx_conv = get_to_usd_factor(currencies_df, account_currency) / table_base_currency_to_usd
    # Convert from account to modelling currency
    modelling_fx_conv = base_to_account_fx_conv / get_to_usd_factor(currencies_df, modelling_currency)
    return modelling_fx_conv


def copy_values_to_cnv(cat_path, field, curve, modelling_fx_conv=None, is_override=False):
    # Construct converted curve name
    cnv_curve = f"{curve}_cnv"
    # Get value from parent field
    parent_node = getattr(cat_path, field)
    value = getattr(parent_node, curve)
    # Override with selected value if flag set
    if is_override:
        value = value.selected
    # If value exists, copy or convert
    if value is not None:
        if modelling_fx_conv is None:
            setattr(parent_node, cnv_curve, value)
        else:
            setattr(parent_node, cnv_curve, value * modelling_fx_conv)
    return value


def get_cat_param_by_lob(hxd, lob, col_name):
    # Access parent node for given parameter
    cat_path = hxd.cds.cat
    parent_node = getattr(cat_path, col_name)
    # Build list of curve names
    curves = [f"curve_{i+1}" for i in range(constants.NUM_CURVES_IN_CAT)]
    # Iterate through curves and return first match
    for curve in curves:
        selected_lob = getattr(cat_path.selected_class, curve)
        if selected_lob == lob:
            result = getattr(parent_node, curve)
            return result if result else 0
    # Default to 0 if no match found
    return 0
