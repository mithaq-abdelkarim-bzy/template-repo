import hx
import numpy as np
import algorithms.rate_utilities as utils
import algorithms.rate_constants as constants
from algorithms import parameter_tables_schema as params
from algorithms.cat.cat_helpers import (
    set_return_period_and_critical_prob,
    calculate_and_save_cov,
    calculate_and_save_unadjusted_ulr,
    get_rate_change_factor,
    get_inflation_factor,
    set_selected_class_dropdowns,
    calculate_selected_gn_cat_ulr,
    get_modelling_fX_conv,
    copy_values_to_cnv
)
from libraries.model_profiler.algorithms.profiling_hxd_functions         import time_me

def build_cnv_curve(cat_path, hxd, modelling_fx_conv, curve, return_period_fields, rater):
    cnv_curve = f"{curve}_cnv"  # Name for the converted version of the curve

    # Copy and convert numeric fields like return periods, AAL, and standard deviation
    for field in return_period_fields + ['aal', 'standard_deviation']:
        copy_values_to_cnv(cat_path, field, curve, modelling_fx_conv)

    # Access converted AAL and standard deviation objects
    aal = getattr(getattr(cat_path, "aal"), cnv_curve)
    standard_deviation = getattr(getattr(cat_path, "standard_deviation"), cnv_curve)
    
    # Compute and save Coefficient of Variation (CoV)
    calculate_and_save_cov(aal, standard_deviation, cat_path, cnv_curve)

    # Copy metadata fields to the converted curve
    for field in ['curve_label', 'model', 'selected_class', 'gn_in_force_premium']:
        copy_values_to_cnv(cat_path, field, curve)
    
    # Copy overrideable factors for inflation and rate change
    inflation_factor = copy_values_to_cnv(cat_path, 'inflation_factor', curve, is_override=True)
    rate_change_factor = copy_values_to_cnv(cat_path, 'rate_change_factor', curve, is_override=True)

    # Calculate unadjusted Ultimate Loss Ratio for the converted curve
    calculate_and_save_unadjusted_ulr(cat_path, aal, cnv_curve,rater)

    # Apply inflation and rate adjustments if inflation data exists
    if hxd.cds.inflation.summary_by_lob:
        calculate_selected_gn_cat_ulr(cat_path, cnv_curve, inflation_factor, rate_change_factor)

@time_me
def rate_cat(hxd, rater):
    cat_path = hxd.cds.cat  # Catastrophe data source
    inflation_path = hxd.cds.inflation  # Inflation data source   
    fx_rates_df = params.fx_rates.df() # Currency conversion table    
    
    # Determine modeling FX conversion factor for monetary calculations
    modelling_fx_conv = get_modelling_fX_conv(cat_path, hxd, fx_rates_df)
    
    # Determine return period fields for each curve
    return_period_fields = set_return_period_and_critical_prob(cat_path)

    # Prepare list of curve names based on configured number of curves
    curves = [f"curve_{i+1}" for i in range(constants.NUM_CURVES_IN_CAT)]

    for curve in curves:
        # Fetch curve-specific AAL and standard deviation
        aal = getattr(getattr(cat_path, "aal"), curve)
        standard_deviation = getattr(getattr(cat_path, "standard_deviation"), curve)
        
        # Compute and store Coefficient of Variation
        calculate_and_save_cov(aal, standard_deviation, cat_path, curve)
        
        # Calculate unadjusted Ultimate Loss Ratio
        calculate_and_save_unadjusted_ulr(cat_path, aal, curve, rater)
        
        # Determine the selected line of business for the curve
        selected_lob = getattr(cat_path.selected_class, curve)

        # Update dropdown selections for the UI based on LOB
        set_selected_class_dropdowns(hxd, rater["prem_limit_data"])
        
        # Check if curve is being rolled forward from previous period
        is_roll_forward = getattr(cat_path.roll_forward, curve)

        # Fetch inflation and rate change factors for adjustments
        inflation_factor = get_inflation_factor(cat_path, hxd, curve, selected_lob, is_roll_forward, rater)
        rate_change_factor = get_rate_change_factor(cat_path, hxd, curve, selected_lob, is_roll_forward, rater)

        # Calculate adjusted Ultimate Loss Ratio with factors applied
        calculate_selected_gn_cat_ulr(cat_path, curve, inflation_factor, rate_change_factor, True)
        
        # Build the converted catastrophe risk curve
        build_cnv_curve(cat_path, hxd, modelling_fx_conv, curve, return_period_fields, rater)