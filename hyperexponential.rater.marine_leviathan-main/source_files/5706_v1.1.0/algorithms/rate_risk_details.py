import hx
import pandas as pd
import numpy as np
import math as math
import dateutil as dateutil
from algorithms.rate_utilities import policy_term, pd_df_from_hx_list, look_up, look_up_with_bounds, ratio, MBBEFDG3
from algorithms import parameter_tables_schema as params
from algorithms.rate_constants import benchmark_lr, bp_class, defaultusage
from operator import itemgetter
from datetime import datetime


def ratio(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return 0


def iferror(a, b, fallback):
    try:
        return a / b
    except ZeroDivisionError:
        return fallback

def rate_risk_details(hxd):

    exp = hxd.cds.exposure.granular 

    exp.total_sum_insured_label = "Total Sum Insured" + " (" + hxd.cds.currencies.source_currency + ")"
    exp.average_sum_insured_label = "Average Sum Insured per Unit" + " (" + hxd.cds.currencies.source_currency + ")"
    exp.benchmark_premium_label = "Benchmark Premium" + " (" + hxd.cds.currencies.source_currency + ")"
    exp.rov_hovertext = "Includes trenchers & ploughs"

   # Calculate total columns
    exp.number_of_units.total = exp.number_of_units.rov + exp.number_of_units.auv + exp.number_of_units.seismic_towed + exp.number_of_units.seismic_ocean_bottom + exp.number_of_units.diving_oceanographic + exp.number_of_units.submersibles + exp.number_of_units.other
    exp.total_sum_insured.total = exp.total_sum_insured.rov + exp.total_sum_insured.auv + exp.total_sum_insured.seismic_towed + exp.total_sum_insured.seismic_ocean_bottom + exp.total_sum_insured.diving_oceanographic +exp.total_sum_insured.submersibles + exp.total_sum_insured.other
    
    # Calculate average sum insured per vessel
    exp.average_sum_insured_per_unit.rov =  ratio(exp.total_sum_insured.rov, exp.number_of_units.rov)
    exp.average_sum_insured_per_unit.auv =  ratio(exp.total_sum_insured.auv, exp.number_of_units.auv)
    exp.average_sum_insured_per_unit.seismic_towed =  ratio(exp.total_sum_insured.seismic_towed, exp.number_of_units.seismic_towed)
    exp.average_sum_insured_per_unit.seismic_ocean_bottom =  ratio(exp.total_sum_insured.seismic_ocean_bottom, exp.number_of_units.seismic_ocean_bottom)
    exp.average_sum_insured_per_unit.diving_oceanographic =  ratio(exp.total_sum_insured.diving_oceanographic, exp.number_of_units.diving_oceanographic)
    exp.average_sum_insured_per_unit.submersibles =  ratio(exp.total_sum_insured.submersibles, exp.number_of_units.submersibles)
    exp.average_sum_insured_per_unit.other =  ratio(exp.total_sum_insured.other, exp.number_of_units.other)
        
    fx_rates = hx.params.tbl_fx
    fx_gbp = 1/look_up(hxd.cds.currencies.source_currency, "Currency", "Exchange Rate", fx_rates)
    claim_rate = hx.params.tbl_claim_rates 
    
    #Other adjustments
    policy_term_factor = hxd.cds.policy_term
    type_of_work_factor = look_up(exp.type_of_work, "Type of Work", "Factor", hx.params.tbl_type_of_work)
    ice_debris_other_traffic_factor = look_up(exp.ice_debris_other_traffic, "Ice, debris, other marine traffic?", "Factor", hx.params.tbl_ice_debris_traffic)
    experience_level_factor = look_up(exp.experience_level, "Experience Category", "Factor", hx.params.tbl_experience_category)
    usage_factor_scaled = exp.usage_factor / defaultusage
    
    expected_usage_adjustment = look_up_with_bounds(exp.usage_factor, "Lower", "Upper","Exp Usage", hx.params.tbl_exp_usage)
    expected_usage_adjustment_factor = look_up(expected_usage_adjustment, "Usage", "Rebased", hx.params.tbl_usage)
    underwriter_adjustment_factor = (1+exp.uw_adjustment)

    total_adjustment_factor = policy_term_factor * type_of_work_factor * ice_debris_other_traffic_factor * experience_level_factor * usage_factor_scaled * expected_usage_adjustment_factor * underwriter_adjustment_factor


    # Covert sum insured to gbp
    exposure_gbp_rov = exp.total_sum_insured.rov * fx_gbp
    exposure_gbp_aov = exp.total_sum_insured.auv * fx_gbp
    exposure_gbp_seismic_towed = exp.total_sum_insured.seismic_towed * fx_gbp
    exposure_gbp_seismic_ocean_bottom = exp.total_sum_insured.seismic_ocean_bottom * fx_gbp
    exposure_gbp_diving_oceanographic = exp.total_sum_insured.diving_oceanographic * fx_gbp
    exposure_gbp_submersibles = exp.total_sum_insured.submersibles * fx_gbp
    exposure_gbp_other = exp.total_sum_insured.other * fx_gbp

    # Assign claim rate based on vessel category
    claim_rate_rov = look_up("ROV", "Category", "Expected Cost (Rate of SI)", hx.params.tbl_claim_rates)
    claim_rate_auv = look_up("AUV", "Category", "Expected Cost (Rate of SI)", hx.params.tbl_claim_rates)
    claim_rate_seismic_towed = look_up("Seismic - Towed", "Category", "Expected Cost (Rate of SI)", hx.params.tbl_claim_rates)
    claim_rate_seismic_ocean_bottom = look_up("Seismic - Ocean Bottom", "Category", "Expected Cost (Rate of SI)", hx.params.tbl_claim_rates)
    claim_rate_diving_oceanographic = look_up("Diving & Oceanographic", "Category", "Expected Cost (Rate of SI)", hx.params.tbl_claim_rates)
    claim_rate_submersibles = look_up("Submersibles", "Category", "Expected Cost (Rate of SI)", hx.params.tbl_claim_rates)
    claim_rate_other = look_up("Other", "Category", "Expected Cost (Rate of SI)", hx.params.tbl_claim_rates)
    
    #Calculate expected claim cost in gbp
    expected_claim_cost_rov = exposure_gbp_rov * claim_rate_rov
    expected_claim_cost_auv = exposure_gbp_aov * claim_rate_auv
    expected_claim_cost_seismic_towed = exposure_gbp_seismic_towed * claim_rate_seismic_towed
    expected_claim_cost_sesimic_ocean_bottom = exposure_gbp_seismic_ocean_bottom * claim_rate_seismic_ocean_bottom
    expected_claim_cost_diving_oceanographic = exposure_gbp_diving_oceanographic * claim_rate_diving_oceanographic
    expected_claim_cost_submersibles = exposure_gbp_submersibles * claim_rate_submersibles
    expected_claim_cost_other = exposure_gbp_other * claim_rate_other

    # Assign size discount for each vessel category
    # No discount for AUV, Diving & Oceanographics and Submersibles
    # ROV discount based on number of units, all other vessel categories based on total sum insured in GBP
    size_discount_rov = look_up_with_bounds(exp.number_of_units.rov,  "Lower", "Upper","Discount", hx.params.tbl_size_discount_rov)
    size_discount_auv = 0
    size_discount_seismic_towed = look_up_with_bounds(exposure_gbp_seismic_towed,  "Lower (\u00a3m)", "Upper (\u00a3m)","Discount", hx.params.tbl_size_discount_seismic_towed)
    size_discount_seismic_bottom = look_up_with_bounds(exposure_gbp_seismic_ocean_bottom ,  "Lower (\u00a3m)", "Upper (\u00a3m)","Discount", hx.params.tbl_size_discount_seismic_ocean)
    size_discount_diving_oceanographic = 0
    size_discount_submersibles = 0
    size_discount_other = look_up_with_bounds(exposure_gbp_other,  "Lower (\u00a3m)", "Upper (\u00a3m)","Discount", hx.params.tbl_size_discount_other)

    # Apply size discount to expected claim cost
    expected_claim_cost_post_discount_rov = (1 - size_discount_rov) * expected_claim_cost_rov
    expected_claim_cost_post_discount_auv = (1 - size_discount_auv) * expected_claim_cost_auv
    expected_claim_cost_post_discount_seismic_towed = (1 - size_discount_seismic_towed) * expected_claim_cost_seismic_towed
    expected_claim_cost_post_discount_seismic_ocean_bottom = (1 - size_discount_seismic_bottom) * expected_claim_cost_sesimic_ocean_bottom
    expected_claim_cost_post_discount_diving_oceanographic = (1 - size_discount_diving_oceanographic) * expected_claim_cost_diving_oceanographic
    expected_claim_cost_post_discount_submersibles = (1 - size_discount_submersibles) * expected_claim_cost_submersibles
    expected_claim_cost_post_discount_other = (1 - size_discount_other) * expected_claim_cost_other

    # Excess adjustment calculation

    # We will assume the following default assumptions, and scale everything relative to that using the Hull exposure curve.
    mbbefdg_param_small = look_up("Hull Curve - small vessels", "Category", "MBBEFDG Param",hx.params.tbl_MBBEFDG)
    mbbefdg_param_large = look_up("Hull Curve - large vessels", "Category", "MBBEFDG Param",hx.params.tbl_MBBEFDG)

    # Excess adjustment function definition
    def excess_adjustment(vessel_category, average_sum_insured_per_unit, excess_per_loss):

        if vessel_category == "Diving":
            
            default_perc_si_diving_air = look_up("Diving - Air","Category", "Default XS", hx.params.tbl_diving)/look_up("Diving - Air","Category", "Default SI", hx.params.tbl_diving)
            default_perc_si_diving_saturation = look_up("Diving - Saturation","Category", "Default XS", hx.params.tbl_diving)/look_up("Diving - Saturation","Category", "Default SI", hx.params.tbl_diving)
            risk_split = look_up("Diving - Air","Category", "Risk Split", hx.params.tbl_diving)

            default_perc_si = risk_split * default_perc_si_diving_air + (1 - risk_split) * default_perc_si_diving_saturation        
        else:   
            default_perc_si = look_up(vessel_category, "Category", "% of SI", hx.params.tbl_default_perc_SI)

        selected_si_avg = average_sum_insured_per_unit
        
        if selected_si_avg > 15000000: 
            default_exposure_perc_above_XS = 1 - MBBEFDG3(mbbefdg_param_large,   default_perc_si)
        else:
            default_exposure_perc_above_XS = 1 - MBBEFDG3(mbbefdg_param_small,   default_perc_si)
        
        selected_perc_si = iferror(excess_per_loss , selected_si_avg,  0)
        
        if selected_si_avg > 15000000: 
            selected_exposure_perc_above_XS = 1 - MBBEFDG3(mbbefdg_param_large,   selected_perc_si)
        else:
            selected_exposure_perc_above_XS = 1 - MBBEFDG3(mbbefdg_param_small,   selected_perc_si)
        
        if selected_si_avg == 0 :
            excess_adjustment = 1
        else:
            excess_adjustment = iferror(selected_exposure_perc_above_XS, default_exposure_perc_above_XS, 1) 

        return excess_adjustment

        

    # Excess adjustment calculation for each vessel category
    # Excess adjustment for AUV calculated further below
    excess_adjustment_rov = excess_adjustment("ROV", exp.average_sum_insured_per_unit.rov, exp.excess_per_loss.rov)
    excess_adjustment_seismic_towed = excess_adjustment("Seismic - Towed",exp.average_sum_insured_per_unit.seismic_towed, exp.excess_per_loss.seismic_towed)
    excess_adjustment_seismic_ocean_bottom = excess_adjustment("Seismic - Ocean Bottom",exp.average_sum_insured_per_unit.seismic_ocean_bottom, exp.excess_per_loss.seismic_ocean_bottom)
    excess_adjustment_submersibles = excess_adjustment("Subs",exp.average_sum_insured_per_unit.submersibles, exp.excess_per_loss.submersibles)
    excess_adjustment_seismic_diving_oceanographic = excess_adjustment("Diving",exp.average_sum_insured_per_unit.diving_oceanographic, exp.excess_per_loss.diving_oceanographic)
    excess_adjustment_other = excess_adjustment("Other",exp.average_sum_insured_per_unit.other, exp.excess_per_loss.other)

    # Excess adjustment calculation AUV
    auv_risk_split_normal_operation = 0.1
    auv_risk_split_launch_recovery = 1 - auv_risk_split_normal_operation

    excess_adjustment_auv_normal_ops = excess_adjustment("AUV - Normal operation", exp.average_sum_insured_per_unit.auv, exp.excess_per_loss_auv.normal_ops)
    excess_adjustment_auv_launch_recovery = excess_adjustment("AUV - Launch & Recovery", exp.average_sum_insured_per_unit.auv, exp.excess_per_loss_auv.launch_recovery)
    excess_adjustment_auv = excess_adjustment_auv_normal_ops * auv_risk_split_normal_operation + excess_adjustment_auv_launch_recovery * auv_risk_split_launch_recovery

    expected_claim_cost_post_excess_rov =    excess_adjustment_rov * expected_claim_cost_post_discount_rov
    expected_claim_cost_post_excess_auv =    excess_adjustment_auv * expected_claim_cost_post_discount_auv
    expected_claim_cost_post_excess_seismic_towed =    excess_adjustment_seismic_towed * expected_claim_cost_post_discount_seismic_towed
    expected_claim_cost_post_excess_seismic_ocean_bottom =    excess_adjustment_seismic_ocean_bottom * expected_claim_cost_post_discount_seismic_ocean_bottom
    expected_claim_cost_post_excess_submersibles =    excess_adjustment_submersibles * expected_claim_cost_post_discount_submersibles
    expected_claim_cost_post_excess_diving_oceanographic =    excess_adjustment_seismic_diving_oceanographic * expected_claim_cost_post_discount_diving_oceanographic
    expected_claim_cost_post_excess_other =    excess_adjustment_other * expected_claim_cost_post_discount_other
    
     
    tp_params_df = params.tp_parameters.df()
    yoa = hxd.hx_core.inception_date.year

    # Define function to look up bp class
    def tp_lookup(vbl, bp_class):
        out = tp_params_df[
            (tp_params_df["business_plan_class"] == bp_class)
            & (tp_params_df["year"] == tp_year)
        ][vbl].iloc[0]
        return out
    
    # To stop the model erroring if the inception year defaults to an old year not in the TP data
    # For older policies (2023 YOA & prior) assume the NMP zero
    if yoa in list(tp_params_df['year']):   tp_year = yoa
    else:                                   tp_year = tp_params_df['year'].max()
    
    if yoa <= 2023:
        nmp_load = 0
    else :
        nmp_load = tp_lookup("nmp_load", bp_class)

    # Apply other adjustments and NMP loading
    expected_claim_cost_post_other_adj_rov = expected_claim_cost_post_excess_rov * total_adjustment_factor * (1+nmp_load)
    expected_claim_cost_post_other_adj_auv = expected_claim_cost_post_excess_auv * total_adjustment_factor * (1+nmp_load)
    expected_claim_cost_post_other_adj_seismic_towed = expected_claim_cost_post_excess_seismic_towed * total_adjustment_factor * (1+nmp_load)
    expected_claim_cost_post_other_adj_seismic_ocean_bottom = expected_claim_cost_post_excess_seismic_ocean_bottom * total_adjustment_factor * (1+nmp_load)
    expected_claim_cost_post_other_adj_submersibles = expected_claim_cost_post_excess_submersibles * total_adjustment_factor * (1+nmp_load)
    expected_claim_cost_post_other_adj_diving_oceanographic = expected_claim_cost_post_excess_diving_oceanographic * total_adjustment_factor * (1+nmp_load)
    expected_claim_cost_post_other_adj_other = expected_claim_cost_post_excess_other * total_adjustment_factor * (1+nmp_load)

    # Net benchmark premium calculation in gbp for each vessel category
    benchmark_premium_gbp_rov = expected_claim_cost_post_other_adj_rov / benchmark_lr
    benchmark_premium_gbp_auv = expected_claim_cost_post_other_adj_auv / benchmark_lr
    benchmark_premium_gbp_seismic_towed = expected_claim_cost_post_other_adj_seismic_towed / benchmark_lr
    benchmark_premium_gbp_seismic_ocean_bottom = expected_claim_cost_post_other_adj_seismic_ocean_bottom / benchmark_lr
    benchmark_premium_gbp_submersibles = expected_claim_cost_post_other_adj_submersibles / benchmark_lr
    benchmark_premium_gbp_diving_oceanographic = expected_claim_cost_post_other_adj_diving_oceanographic / benchmark_lr
    benchmark_premium_gbp_other = expected_claim_cost_post_other_adj_other / benchmark_lr
 
    #Convert back to underlying CCY
    exp.benchmark_premium.rov = benchmark_premium_gbp_rov / fx_gbp
    exp.benchmark_premium.auv = benchmark_premium_gbp_auv / fx_gbp
    exp.benchmark_premium.seismic_towed = benchmark_premium_gbp_seismic_towed / fx_gbp
    exp.benchmark_premium.seismic_ocean_bottom = benchmark_premium_gbp_seismic_ocean_bottom / fx_gbp
    exp.benchmark_premium.submersibles = benchmark_premium_gbp_submersibles / fx_gbp
    exp.benchmark_premium.diving_oceanographic = benchmark_premium_gbp_diving_oceanographic / fx_gbp
    exp.benchmark_premium.other = benchmark_premium_gbp_other / fx_gbp
    exp.benchmark_premium.total =  exp.benchmark_premium.rov + exp.benchmark_premium.auv + exp.benchmark_premium.seismic_towed + exp.benchmark_premium.seismic_ocean_bottom + exp.benchmark_premium.submersibles + exp.benchmark_premium.diving_oceanographic + exp.benchmark_premium.other

    #store expected in gbp and underlying CCY for rating summary
    exp.total_expected_loss_gbp = total_expected_loss_gbp = expected_claim_cost_post_other_adj_rov + expected_claim_cost_post_other_adj_auv + expected_claim_cost_post_other_adj_seismic_towed + expected_claim_cost_post_other_adj_seismic_ocean_bottom + expected_claim_cost_post_other_adj_submersibles + expected_claim_cost_post_other_adj_diving_oceanographic + expected_claim_cost_post_other_adj_other
    exp.total_expected_loss = total_expected_loss_gbp / fx_gbp 
      
    return
