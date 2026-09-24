import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
import algorithms.rate_constants as const
from algorithms import parameter_tables_schema as params
from operator import itemgetter


# Helper functions for rate_adjustments.py ------------------------H--------------------------

def set_exp_factor_nodes(hxd, row):
    '''
    Fill in min/max for experience factor.
    '''   
    cds = hxd.cds

    node = getattr(cds.modifiers, "experience_factor")
    # Set the min and max in the UI
    setattr(node, "min", row["min"]) 
    setattr(node, "max", row["max"])
    # Get selected value from UI 
    row["selected"] = getattr(node, "selected")
    return row


def schedule_mod_calculations(hxd, option):
    '''
    Fill in the schedule rating table.
    '''   
    cds = hxd.cds

    schedule_rating_params = getattr(hx.params, f"table_{option}_schedule_mods")
    # mod_name = schedule_rating_params["description_name"]
    # mod_label = schedule_rating_params["description"]
    
    def set_schedule_rating_params_nodes(row):
        node = getattr(getattr(cds.modifiers, option), row["description_name"])
        # Set the min and max in the UI
        setattr(node, "min", row["min"]) 
        setattr(node, "max", row["max"])
        # Get schedule mod selected value from UI 
        row["schedule_mod_selected"] = getattr(node, "selected")
        return row 

    schedule_rating_params = schedule_rating_params.apply(set_schedule_rating_params_nodes, axis=1) 

    # Calculate total schedule mod
    total_schedule_mod = schedule_rating_params["schedule_mod_selected"].sum() + 1

    # Check schedule mods are within the bounds
    schedule_mod_validation =  schedule_rating_params
    schedule_mod_validation["min"]  = pd.to_numeric(schedule_mod_validation["min"]) / 100
    schedule_mod_validation["max"]  = schedule_mod_validation["max"].replace("Unlimited", 10000)
    schedule_mod_validation["max"]  = pd.to_numeric(schedule_mod_validation["max"]) / 100
    schedule_rating_params["validation"] = np.where((schedule_rating_params["schedule_mod_selected"] < schedule_rating_params["min"]) | (schedule_rating_params["schedule_mod_selected"] > schedule_rating_params["max"]) ,True,False)

    if schedule_rating_params["validation"].sum() > 0 :
        hx.errors.validation("Schedule Rating value outside allowable range. [Adjustments]")

    return total_schedule_mod

def validate_min_max(df: pd.DataFrame) -> bool:
    """
    Validate that all 'selected' values in the table fall within their 
    corresponding 'min' and 'max' bounds.

    Parameters
    ----------
    df : pd.DataFrame
        A DataFrame containing at least the columns:
        - 'selected' : numeric value chosen by user or calculated
        - 'min'      : minimum allowed value (inclusive)
        - 'max'      : maximum allowed value (inclusive)

    Returns
    -------
    bool
        True if all rows pass validation (each selected value lies within [min, max]).
        False if any value is outside the range.

    Notes
    -----
    - The function does **not** modify the input DataFrame.
    - Non-numeric values are coerced to NaN, which automatically fail validation.
    - Expected value format: decimals (e.g., 0.65 for 65%, not 65).
    - Use this for logical range checking of model inputs, e.g. experience factors, optional coverages, etc.
    """
    df = df.copy() # Do not mutate original dataframe
    df[["min", "max", "selected"]] = df[["min", "max", "selected"]].apply(pd.to_numeric, errors="coerce") # Coerce your columns to numeric
    invalid = (df["selected"] < df["min"]) | (df["selected"] > df["max"])
    return not invalid.any()

# def validate_min_max(table):
#     ''' 
#     Check selections are within bounds.
#     Note: ensure table values are in decimal form. e.g. 65% is 0.65, not 65.
#     '''
#     table["min"] = pd.to_numeric(table["min"]) 
#     table["max"] = pd.to_numeric(table["max"]) 
#     table["validation"] = np.where((table["selected"] < table["min"]) | (table["selected"] > table["max"]) , True, False) #if (table["selected"] is not None and table["min"] is not None and table["max"] is not None) else False

#     # return False if any selected values outside bounds
#     return False if table["validation"].sum() > 0 else True 

def validate_comments(table):
    ''' 
    Check comments are given where selections have been made.
    '''
    table["comment_validation"] = np.where((table["selected"] != 0) & (table["included"] == "Yes") & (table["comment"].isnull()), True, False)

    # return False if any selected values are missing corresponding comments
    return False if table["comment_validation"].sum() > 0 else True

def set_optional_coverages_nodes(optional_coverages, row):
    ''' 
    Set min/max for optional coverages.
    '''
    node = getattr(optional_coverages, row["description_name"])
    # Set the min and max in the UI
    setattr(node, "min", row["min"]) 
    setattr(node, "max", row["max"])
    # Get schedule mod selected value, include flag and comments from UI 
    row["selected"] = getattr(node, "selected")
    row["included"] = getattr(node, "included")
    row["comment"] = getattr(node, "comment")
    return row 

def set_optional_coverages_outputs(optional_coverages, row):
    ''' 
    Set output node for optional coverages.
    '''
    node = getattr(optional_coverages, row["description_name"])
    setattr(node, "output", row["output"])


# Helper functions for rate_exposure_details.py --------------------------------------------------

def exposure_measure_calcs(hxd, option):
    '''
    Fill in exposure details table
    '''
    cds = hxd.cds

    exposure_params = getattr(hx.params, f"table_{option}_exposures")

    def get_base_rate(row):
        node = getattr(getattr(cds.exposure.granular, option), row["exposure_name"])
        # Get base rate selection from UI
        row["base_rate"] = getattr(node, "base_rate")
        # Validation error: base rate cannot be negative
        if (row["base_rate"] is not None) and (row["base_rate"] < 0):
            hx.errors.validation("Base rate allocations cannot be negative. [Exposure Details]")
        return row
    
    exposure_params = exposure_params.apply(get_base_rate, axis=1)

    # Calculate total of base rates, and check they add to 100% (validation)
    total_base_rate = exposure_params["base_rate"].sum()
    if np.round(total_base_rate, 10) != 1:
        hx.errors.validation("Base rate allocation must sum to 100% [Exposure Details]")

    return exposure_params


def class_base_rate_calculations(class_table, bands, string):
    '''
    Fill in exposure by class table, with base rate bounds for each class.
    'string' is for column naming purposes: "rateable" or "nonrateable"
    '''
    lower_values = bands[bands.index.str.contains("lower")] # Pull out lower bounds for each class
    upper_values = bands[bands.index.str.contains("upper")] # Pull out upper bounds for each class

    class_table[f"rate_lower_{string}"] = lower_values.reset_index(drop=True)
    class_table[f"rate_upper_{string}"] = upper_values.reset_index(drop=True)
    if string == "nonrateable":
        class_table["rate_lower_nonrateable"] = class_table["rate_lower_nonrateable"] * 0.1 # Non-rateable revenue base rate factor of 10%
        class_table["rate_upper_nonrateable"] = class_table["rate_upper_nonrateable"] * 0.1 # Non-rateable revenue base rate factor of 10%

    revenue_lower = bands["revenue"]
    revenue_upper = bands["next"]
    revenue_in_band = class_table[f"alloc_revenue_{string}_usd"].sum() - revenue_lower
    weight = np.where((revenue_upper - revenue_lower) != 0, revenue_in_band / (revenue_upper - revenue_lower), 0)

    class_table[f"interpolated_rate_{string}"] = weight*class_table[f"rate_upper_{string}"] + (1-weight)*class_table[f"rate_lower_{string}"]

    return class_table


def assign_modifier_annualtv(hxd, cover_type):
    '''
    Calculate modifiers for Annual TV exposure table.
    '''
    
    cds = hxd.cds 

    params = getattr(hx.params, f"tbl_annualtv_{cover_type}")
    selected = getattr(cds.annual_tv.selections, cover_type)
    if selected is not None:
        modifier = params[params.iloc[:, 0] == selected]["modifier"].iloc[0] # pick out modifier for row corresponding to selection
    else:
        modifier = None
    setattr(cds.annual_tv.modifiers, cover_type, modifier) # assign modifier back to UI


def assign_modifier_individualtv(hxd, cover_type):
    '''
    Calculate modifiers for Individual TV exposure table.
    '''
    
    cds = hxd.cds 

    params = getattr(hx.params, f"tbl_indtv_{cover_type}")
    selected = getattr(cds.individual_tv.selections, cover_type)
    if selected is not None:
        modifier = params[params.iloc[:, 0] == selected]["modifier"].iloc[0] # pick out modifier for row corresponding to selection
    else:
        modifier = None
    setattr(cds.individual_tv.modifiers, cover_type, modifier) # assign modifier back to UI


def assign_modifier_individualfilm(hxd, cover_type):
    '''
    Calculate modifiers for Individual Film exposure table.
    '''
    
    cds = hxd.cds 

    params = getattr(hx.params, f"tbl_film_{cover_type}")
    selected = getattr(cds.individual_film.selections, cover_type)
    if selected is not None:
        modifier = params[params.iloc[:, 0] == selected]["modifier"].iloc[0] # pick out modifier for row corresponding to selection
    else:
        modifier = None
    setattr(cds.individual_film.modifiers, cover_type, modifier) # assign modifier back to UI


# Helper functions for rate_pricing.py --------------------------------------------------

def eec_ilf_calcs(hxd, row, fx_rate):
    '''
    Calculate EEC ILF using selected ILF curve and parameter table.
    '''
    cds = hxd.cds

    if cds.standard_rater_masking:
        params = hx.params.tbl_eec_limit

        # ILF curve
        selected_curve = cds.rating_factors.ilf_curve
        default_curve = cds.rating_factors.default_curve
        curve = selected_curve if selected_curve is not None else default_curve
        curve = curve.lower() # make lower case

    if cds.nonstandard_rater_masking:
        params = hx.params.tbl_eec_limit_nonstandard
        curve = "ilf_selected"

    limit = row["eec_limit"] / fx_rate # Convert to USD, for looking up in table.

    if limit >= 2000:
        # Select relevant row from params table
        params_row = params[params["per_occurrence_limit"] <= limit].iloc[-1]
        # Find upper and lower ILF bounds
        limit_lower = params_row["per_occurrence_limit"] if not params_row.empty else 0
        limit_upper = params_row["next"] if not params_row.empty else 0
        ilf_lower = params[curve][params["per_occurrence_limit"] == limit_lower].iloc[0] if limit_lower > 0 else 0
        ilf_upper = params[curve][params["per_occurrence_limit"] == limit_upper].iloc[0] if limit_upper > 0 else 0

        # Calculate ILF using weightings
        if (limit_upper - limit_lower) > 0:
            weight = (limit - limit_lower) / (limit_upper - limit_lower)
        else:
            weight = 0
        
        row["eec_ilf"] = ilf_lower + weight * (ilf_upper - ilf_lower)
    else:
        row["eec_ilf"] = 0

    return row


def agg_ilf_calcs(hxd, row):
    '''
    Calculate Aggregate ILF using desired Agg/EEC ratio and parameter table.
    '''
    cds = hxd.cds

    if cds.standard_rater_masking:
        params = hx.params.tbl_agg_lim_adjust
    if cds.nonstandard_rater_masking:
        params = hx.params.tbl_agg_lim_adjust_nonstandard
    
    # Desired Agg/EEC Ratio
    if row["eec_limit"] > 0:
        ratio = row["aggregate_limit"] / row["eec_limit"]
    else:
        ratio = 0

    if ratio >= 1:
        # Select relevant row from params table
        params_row = params[params["limit_ratio"] <= ratio].iloc[-1]
        # Find upper and lower bounds
        limit_lower = params_row["limit_ratio"] if not params_row.empty else 0
        limit_upper = params_row["next"] if not params_row.empty else 0
        ilf_start = params_row["value_at_start"] if not params_row.empty else 0
        ilf_end = params_row["value_at_end"] if not params_row.empty else 0

        # Calculate ILF using weightings
        if (limit_upper - limit_lower) > 0:
            weight = (ratio - limit_lower) / (limit_upper - limit_lower)
        else:
            weight = 0
        
        row["agg_ilf"] = weight * ilf_end + (1-weight) * ilf_start
    else:
        row["agg_ilf"] = 0
        # IR: and add a validation error here!

    return row


def idf_calcs(hxd, row):
    '''
    Calculate Deductible Factor (IDF) using previously calculated guideline deductible and parameter table.
    '''
    cds = hxd.cds
    # Guideline Deductible (calculated in rate_exposure_details.py)
    guideline_deductible = cds.rating_factors.guideline_deductible
    # Retention factor parameter table
    params = hx.params.tbl_retention_factor

    # Interpolate ded factor
    retention = max(row["retention"],0) # Set to 0 if negative retention entered
    interp_factor = min(5, retention / guideline_deductible) if guideline_deductible else 0 # Max of 5
    # Note: no need to convert retention and guideline deductible to USD, since this is a ratio.

    # Find upper and lower bounds
    low_row = params[params["lower"] <= interp_factor].iloc[-1]
    low_ratio = low_row["lower"] if not low_row.empty else 0
    high_ratio = low_row["higher"] if not low_row.empty else 0
    low_factor = low_row["factor"] if not low_row.empty else 0

    high_row = params[params["lower"] <= high_ratio].iloc[-1]
    high_factor = high_row["factor"] if not high_row.empty else 0

    # Calculate weightings
    if (interp_factor == low_ratio) | (high_ratio - low_ratio == 0):
        weight = 0
    else:
        weight = (interp_factor - low_ratio) / (high_ratio - low_ratio)
    
    # Calculate IDF output
    if interp_factor < 0.1:
        row["idf"] = 1.4
    else:
        row["idf"] = weight*(high_factor - low_factor) + low_factor
    
    return row


def benchmark_prem_calcs(hxd, options_df, pro_rata_factor, nmp_load):
    # Note: all done in source currency
    cds = hxd.cds
    
    # Premium post factors
    options_df["premium_post_ded_factor"] = options_df["premium_post_op_covers"] * options_df["factor"]

    # Premium post minimum premium
    min_premium = cds.exposure.aggregate.minimum_premium
    options_df["premium_post_min"] = options_df["premium_post_ded_factor"].clip(lower = min_premium)

    # Premium post ILF
    options_df["premium_post_ilf"] = options_df["premium_post_min"] * options_df["ilf"]

    # Term premium: Apply pro-rata factor and extended reporting period. Then round to integer.
    erp = cds.modifiers.extended_reporting_period.factor # Note: ERP factor is currently set to 1 always.
    options_df["term_premium"] = (options_df["premium_post_ilf"] * pro_rata_factor * erp).round()

    # Final Net Premium
    brokerage = cds.primary.brokerage or 0
    options_df["final_net_premium"] = options_df["term_premium"] * (1-brokerage)

    # Expected Loss
    options_df["expected_loss_cost"] = options_df["final_net_premium"] * const.benchmark_lr
    # Apply NMP load
    options_df["expected_loss"] = options_df["expected_loss_cost"] * (1 + nmp_load)

    # Benchmark Premium
    options_df["net_benchmark_premium"] = options_df["expected_loss"] / const.benchmark_lr
    options_df["gross_benchmark_premium"] = options_df["net_benchmark_premium"] / (1 - brokerage)

    return options_df


def technical_prem_calcs(hxd, df, tp_params, fx_rate):
    # Note: all done in source currency
    cds = hxd.cds

    # Set up tp params
    che = tp_params['che'].iloc[0]
    var_exp = tp_params['var_exp'].iloc[0]
    inv_inc = tp_params['inv_inc'].iloc[0]
    cost_of_ri = tp_params['cost_of_ri'].iloc[0]
    ri_rec = tp_params['ri_rec'].iloc[0]
    roc = tp_params['roc'].iloc[0]
    fixed_exp_usd = tp_params['fixed_exp'].iloc[0]
    capital_req = tp_params['capital_req'].iloc[0]
    nmp_load = tp_params['nmp_load'].iloc[0]

    # Convert fixed expenses to model currency (default to USD if error)
    fixed_exp = fixed_exp_usd * fx_rate

    # Calculate technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc*capital_req

    # Technical Premium
    df["net_technical_premium"] = (df["expected_loss"] * (1+che) + fixed_exp) / technical_lr
    df["gross_technical_premium"] = df["net_technical_premium"] / (1 - df["brokerage"])

    return df


def nonstandard_idf_calcs(hxd, row, fx_rate):
    '''
    Calculate IDF using Excess and Excess Ratio tables for nonstandard raters.
    '''
    cds = hxd.cds

    # EEC IDF -----
    eec_params = hx.params.tbl_excess_eec_nonstandard
    eec_excess_usd = (row["eec_excess"] or 0) / fx_rate # Convert to USD, for parameter table lookup

    if eec_excess_usd >= 2000:
        # Select relevant row from params table
        params_row = eec_params[eec_params["excess"] <= eec_excess_usd].iloc[-1]
        # Find upper and lower IDF bounds
        deductible_lower = params_row["excess"] if not params_row.empty else 0
        deductible_upper = params_row["next"] if not params_row.empty else 0
        idf_lower = eec_params["idf_selected"][eec_params["excess"] == deductible_lower].iloc[0] if deductible_lower > 0 else 0
        idf_upper = eec_params["idf_selected"][eec_params["excess"] == deductible_upper].iloc[0] if deductible_upper > 0 else 0

        # Calculate EEC IDF using weightings
        if (deductible_upper - deductible_lower) > 0:
            weight_eec = (eec_excess_usd - deductible_lower) / (deductible_upper - deductible_lower)
        else:
            weight_eec = 0
        eec_idf = idf_lower + weight_eec * (idf_upper - idf_lower)
    else:
        eec_idf = 0 

    # Aggregate IDF -----  # IR: temp fix - We should not have an agg excess, so using ratio=1
    agg_params = hx.params.tbl_excess_agg_nonstandard
    agg_excess_usd = 0 # (row["aggregate_excess"] or 0) / fx_rate 

    if eec_excess_usd > 0:
        ratio = 1 #agg_excess_usd / eec_excess_usd
    else:
        ratio = 0

    if ratio >= 1:
        # Select relevant row from params table
        params_row = agg_params[agg_params["excess_ratio"] <= ratio].iloc[-1]
        # Find upper and lower bounds
        agg_lower = params_row["excess_ratio"] if not params_row.empty else 0
        agg_upper = params_row["next"] if not params_row.empty else 0
        idf_start = params_row["value_at_start"] if not params_row.empty else 0
        idf_end = params_row["value_at_end"] if not params_row.empty else 0

        # Calculate IDF using weightings
        if (agg_upper - agg_lower) > 0:
            weight_agg = (ratio - agg_lower) / (agg_upper - agg_lower)
        else:
            weight_agg = 0
        agg_idf = idf_start + weight_agg * (idf_end - idf_start)
    else:
        agg_idf = 0

    # Combined IDF -----
    row["idf"] = eec_idf * agg_idf
   
    return row
    

