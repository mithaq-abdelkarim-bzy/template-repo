# v0.5.0
import hx
import pandas as pd
import numpy as np
import algorithms.rate_constants as const
from algorithms import parameter_tables_schema as params
from algorithms.rate_utilities import ratio, look_up, pd_df_from_hx_list, policy_term
from algorithms.rate_constants import benchmark_lr
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import coverages_dict
from algorithms.model_profiler.profiling_hxd_functions import time_me

from algorithms.parameter_tables_schema import tp_parameters



@time_me
def rate_rating_summary(hxd):
    """ Assign vairable in page Rating Summary and assign Benchmark and Technical variables"""
    ##############################
    ## Initialise variables
    ##############################

    cds = hxd.cds
    cds_layers = cds.layers
    rf = hxd.cds.rating_factors  
    tp_params_df = params.tp_parameters.df()
    # fx_rates_df = params.fx_rates.df() # Using fx from library
    fx_rates_df = hx.params.table_currency
    cob_reference = cds.technical_price_assumptions.cob_reference
    include_aad = cds.risk_information.include_aad
    include_loss_corridor = cds.risk_information.include_loss_corridor

    # Assign technical price assumptions
    yoa = hxd.hx_core.inception_date.year

    if yoa in list(set(tp_params_df[(tp_params_df["business_plan_class"]=="Specialty Reinsurance") | (tp_params_df["business_plan_class"]=="Specialty (PT)") | (tp_params_df["business_plan_class"]=="Specialty Surety")]['year'])):
        tp_year = yoa
    else:
        tp_year = tp_params_df['year'].max()

    if cob_reference == "TQ":
        hxd.cds.standard_fields.benchmark_class = business_plan_class = "Specialty Surety"
    elif tp_year < 2026:
        hxd.cds.standard_fields.benchmark_class = business_plan_class = "Specialty (PT)"
    else:
        hxd.cds.standard_fields.benchmark_class = business_plan_class =  "Specialty Reinsurance"

    tpa_df = tp_params_df[(tp_params_df["year"]==tp_year) & (tp_params_df["business_plan_class"]==business_plan_class) ]
    
    cds_tpa = hxd.cds.technical_price_assumptions
    cds_tpa.benchmark_loss_ratio = const.benchmark_lr

    cds_tpa.claims_handling_expenses = che = tpa_df["che"].item()
    fixed_exp_usd = tpa_df["fixed_exp"].item()
    cds_tpa.variable_expenses = var_exp = tpa_df["var_exp"].item()
    cds_tpa.investment_income = inv_inc = tpa_df["inv_inc"].item()
    cds_tpa.cost_of_ri = cost_of_ri = tpa_df["cost_of_ri"].item()
    cds_tpa.return_on_capital = roc = tpa_df["roc"].item()
    cds_tpa.capital_cost = capital_req = tpa_df["capital_req"].item()
    cds_tpa.non_modelled_perils_nmp = nmp_load =  tpa_df["nmp_load"].item()
    cds_tpa.ri_rec = ri_rec =  tpa_df["ri_rec"].item()

    # Convert fixed expenses to model currency (default to USD if error)
    ccy = hxd.cds.currencies.source_currency
    cds_tpa.fixed_expenses = fixed_exp = fixed_exp_usd * look_up(ccy, 'ccy', 'fx_rate', fx_rates_df, if_not_found=1)
    
    # Calculate technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc * capital_req

    ##############################
    ## Assign variables: 
    ############################## 
    for layer in cds_layers:
        # initialise variables
        layer.pure_rate = layer.pricing_selection.final_selection.pure_rate or 0
        brokerage = layer.brokerage_inc_swing or 0
        ceding_commission = layer.ceding_commission or 0
        expected_losses_after_loss_sensitive_features = layer.expected_losses_after_loss_sensitive_features or 0

        # define brokerage netting down factor
        if layer.bkg_gross_or_net == "Gross":
            bkg_netting_down_factor = 1 - brokerage - ceding_commission
        else:
            bkg_netting_down_factor = (1 - brokerage) * (1 - ceding_commission)

        # If rater priced - specific calculation for benchmark_premium_100 and technical_premium_100 with Advanced Features 
        # to maintain Variable Expenses and Brokerage amounts the same than before Advance Feature
        if hxd.cds.standard_fields.is_rater_priced and layer.quoted_premium_net_100:
            
            expected_loss_inc_nmp_100 = expected_losses_after_loss_sensitive_features * (1 + nmp_load)
            layer.expected_loss_inc_nmp = expected_loss_inc_nmp_100
            layer.expected_loss_cost_100 = expected_loss_inc_nmp_100

            if not expected_loss_inc_nmp_100:
                continue
            # initialise benchmark premiums 100 gross and net
            layer.benchmark_premium_net_100 = 0
            layer.benchmark_premium_100 = 0
            # assign benchmark premiums 100 gross and net
            benchmark_premium_net_100 = ratio(expected_loss_inc_nmp_100, const.benchmark_lr)
            layer.benchmark_premium_net_100 = benchmark_premium_net_100
            layer.benchmark_premium_100 = ratio(benchmark_premium_net_100, bkg_netting_down_factor)

            # benchmark premiums
            expected_losses_pre_ad = layer.pricing_selection.final_selection.pure_premium or 0
            expected_losses_pre_ad_inc_npm = expected_losses_pre_ad * (1 + nmp_load)
            net_prem_tech_100_pre_ad = (expected_losses_pre_ad_inc_npm * (1 + che) + fixed_exp )/(1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc * capital_req)
            variable_expense_pre_ad = net_prem_tech_100_pre_ad * var_exp

            net_prem_tech_100_post_ad_pre_var_exp_adj = (expected_loss_inc_nmp_100 * ( 1 + che ) + fixed_exp)/(1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc * capital_req)
            
            
            # variable_expense_post_ad = net_prem_tech_100_pre_ad * var_exp
            variable_expense_post_ad = net_prem_tech_100_post_ad_pre_var_exp_adj * var_exp
            # adjustment to maintain variable expense at the same level than pre Advanced features
            net_prem_tech_100_post_ad = net_prem_tech_100_post_ad_pre_var_exp_adj - variable_expense_post_ad + variable_expense_pre_ad

            gross_prem_tech_100_pre_ad = ratio(net_prem_tech_100_pre_ad, bkg_netting_down_factor)

            brokerage_amount = brokerage * gross_prem_tech_100_pre_ad
            if layer.bkg_gross_or_net == "Gross":
                ceding_commission_amount = gross_prem_tech_100_pre_ad * ceding_commission
            else:
                ceding_commission_amount = (gross_prem_tech_100_pre_ad - brokerage_amount) * ceding_commission
            # adjustment to maintain brokerage at the same level than pre Advanced features
            gross_prem_tech_100_post_ad = net_prem_tech_100_post_ad + brokerage_amount + ceding_commission_amount

            if include_aad == True or include_loss_corridor == True:
                technical_premium_100 = gross_prem_tech_100_post_ad
                technical_premium_net_100 = net_prem_tech_100_post_ad
            else:
                technical_premium_100 = gross_prem_tech_100_pre_ad
                technical_premium_net_100 = net_prem_tech_100_pre_ad
        
            layer.technical_premium_100 = technical_premium_100
            layer.technical_premium_net_100 = technical_premium_net_100

            # set gross quoted premium 100 in line with Upfront premium. Confirm by JC and JM. 
            # layer.quoted_premium_100 = layer.upfront_premium_gross_100
            # set to 
            # layer.quoted_premium_100 = layer.expected_premium_paid_gross_100

        
        # generic calculation including annualisation of the premium
        calculate_premiums(layer, hxd, nmp_load, che, fixed_exp, technical_lr, benchmark_lr, var_exp, inv_inc, cost_of_ri, ri_rec, capital_req, rf, bkg_netting_down_factor) # Edit v0.3.0
        
    cds_layers_df = pd_df_from_hx_list(cds.layers)
    
    cds.programme_all.expected_loss = cds_layers_df["expected_loss"].sum()
    cds.programme_all.expected_losses_after_loss_sensitive_features = total_el_after_loss_sensitive_features = cds_layers_df["expected_losses_after_loss_sensitive_features"].sum()
    cds.programme_all.expected_loss_inc_nmp = total_expected_loss_inc_nmp_programme_all = cds_layers_df["expected_loss_inc_nmp"].sum()

    cds.programme_all.upfront_premium_gross_100 = cds_layers_df["upfront_premium_gross_100"].sum()
    cds.programme_all.upfront_premium_net_100 = cds_layers_df["upfront_premium_net_100"].sum()
    cds.programme_all.expected_premium_paid_gross_100 = cds_layers_df["expected_premium_paid_gross_100"].sum()
    cds.programme_all.expected_premium_paid_net_100 = cds_layers_df["expected_premium_paid_net_100"].sum()

    cds.programme_all.quoted_premium_100 = total_quoted_premium_gross_100_programme_all = cds_layers_df["quoted_premium_100"].sum()
    cds.programme_all.benchmark_premium_100 = cds_layers_df["benchmark_premium_100"].sum()
    cds.programme_all.technical_premium_100 =  cds_layers_df["technical_premium_100"].sum()
    cds.programme_all.quoted_premium_net_100 = total_quoted_premium_net_100_programme_all = cds_layers_df["quoted_premium_net_100"].sum()
    cds.programme_all.benchmark_premium_net_100 = benchmark_prem_net_100_sum  = cds_layers_df["benchmark_premium_net_100"].sum()
    cds.programme_all.technical_premium_net_100 = technical_prem_net_100_sum = cds_layers_df["technical_premium_net_100"].sum()
    
    cds.programme_all.quoted_premium = cds_layers_df["quoted_premium"].sum()
    cds.programme_all.line_size = cds_layers_df["line_size"].sum()
    cds.programme_all.bpi = ratio(total_quoted_premium_net_100_programme_all,benchmark_prem_net_100_sum)
    cds.programme_all.tpi = ratio(total_quoted_premium_net_100_programme_all,technical_prem_net_100_sum)
    cds.programme_all.pflr = total_pflr_programme_all =  ratio(total_expected_loss_inc_nmp_programme_all,total_quoted_premium_net_100_programme_all)
    # cds.programme_all.roc = ratio(1 - total_pflr_programme_all - var_exp + inv_inc - (cost_of_ri - ri_rec) - ratio(fixed_exp * len(cds_layers_df) + total_expected_loss_inc_nmp_programme_all * che, total_quoted_premium_net_100_programme_all), capital_req)
    cds.programme_all.glr = total_gflr_programme_all =  ratio(total_expected_loss_inc_nmp_programme_all,total_quoted_premium_gross_100_programme_all)
    
    cds.programme_all.roc = ratio((total_expected_loss_inc_nmp_programme_all * ( 1 + che ) + fixed_exp* len(cds_layers_df)) - total_quoted_premium_net_100_programme_all * (1 - var_exp + inv_inc - (cost_of_ri - ri_rec)) , (-total_quoted_premium_net_100_programme_all * capital_req) )
    

    
    cds_layers_selected_df = cds_layers_df[cds_layers_df["include_layer"]==True]
    cds.programme_selected.expected_loss = cds_layers_selected_df["expected_loss"].sum()
    cds.programme_selected.expected_losses_after_loss_sensitive_features = total_el_after_loss_sensitive_features_selected = cds_layers_selected_df["expected_losses_after_loss_sensitive_features"].sum()
    cds.programme_selected.expected_loss_inc_nmp = total_expected_loss_inc_nmp_programme_selected = cds_layers_selected_df["expected_loss_inc_nmp"].sum()
    
    cds.programme_selected.upfront_premium_gross_100 = cds_layers_selected_df["upfront_premium_gross_100"].sum()
    cds.programme_selected.upfront_premium_net_100 = cds_layers_selected_df["upfront_premium_net_100"].sum()
    cds.programme_selected.expected_premium_paid_gross_100 = cds_layers_selected_df["expected_premium_paid_gross_100"].sum()
    cds.programme_selected.expected_premium_paid_net_100 = cds_layers_selected_df["expected_premium_paid_net_100"].sum()

    cds.programme_selected.quoted_premium_100 = total_quoted_premium_gross_100_programme_selected = cds_layers_selected_df["quoted_premium_100"].sum()
    cds.programme_selected.benchmark_premium_100 = cds_layers_selected_df["benchmark_premium_100"].sum()
    cds.programme_selected.technical_premium_100 =  cds_layers_selected_df["technical_premium_100"].sum()
    cds.programme_selected.quoted_premium_net_100 = total_quoted_premium_net_100_programme_selected = cds_layers_selected_df["quoted_premium_net_100"].sum()
    cds.programme_selected.benchmark_premium_net_100 = benchmark_prem_net_100_sum_selected  = cds_layers_selected_df["benchmark_premium_net_100"].sum()
    cds.programme_selected.technical_premium_net_100 = technical_prem_net_100_sum_selected = cds_layers_selected_df["technical_premium_net_100"].sum()
    
    cds.programme_selected.quoted_premium = cds_layers_selected_df["quoted_premium"].sum()
    cds.programme_selected.line_size = cds_layers_selected_df["line_size"].sum()
    cds.programme_selected.bpi = ratio(total_quoted_premium_net_100_programme_selected,benchmark_prem_net_100_sum_selected)
    cds.programme_selected.tpi = ratio(total_quoted_premium_net_100_programme_selected,technical_prem_net_100_sum_selected)
     
    cds.programme_selected.pflr = total_pflr_programme_selected =  ratio(total_expected_loss_inc_nmp_programme_selected,total_quoted_premium_net_100_programme_selected)
    # cds.programme_selected.roc = ratio(1 - total_pflr_programme_selected - var_exp + inv_inc - (cost_of_ri - ri_rec) - ratio(fixed_exp * len(cds_layers_df) + total_expected_loss_inc_nmp_programme_selected * che, total_quoted_premium_net_100_programme_selected), capital_req)
    cds.programme_selected.glr = total_glr_programme_selected =  ratio(total_expected_loss_inc_nmp_programme_selected,total_quoted_premium_gross_100_programme_selected)
    
    cds.programme_selected.roc = ratio((total_expected_loss_inc_nmp_programme_selected * ( 1 + che ) + fixed_exp* len(cds_layers_df)) - total_quoted_premium_net_100_programme_selected * (1 - var_exp + inv_inc - (cost_of_ri - ri_rec)) , (-total_quoted_premium_net_100_programme_selected * capital_req) )
    
    return


def calculate_premiums(calculated_level, hxd, nmp_load, che, fixed_exp, technical_lr, benchmark_lr, var_exp, inv_inc, cost_of_ri, ri_rec, capital_req, rf, bkg_netting_down_factor): # Edit v0.3.0
    """
    Calculate the premium for the given level
    Args:
        calculated_level: this could be Layer, Coverage or Insured Asset
        pricing assumptions:
        rf = rating factor level that contains the policy_term
    """
    # assign quoted_premiums_100 assuming quoted_premium_net_100 is already calculated
    quoted_premium_net_100 = calculated_level.quoted_premium_net_100 or 0
    # calculated_level.quoted_premium_100 = quoted_premium_100 = ratio(quoted_premium_net_100, bkg_netting_down_factor)
    quoted_premium_100 = calculated_level.quoted_premium_100 or 0
    # If rater priced
    if hxd.cds.standard_fields.is_rater_priced and calculated_level.quoted_premium_100:
        # Previoulsy defined nodes from rate_rating_summary: 
        # benchmark_premium_100 
        # technical_premium_100 
        # expected_loss_cost_100
        # expected_loss_inc_nmp_100 
  
        # Assign expected losses
        benchmark_premium_100 = calculated_level.benchmark_premium_100 or 0
        technical_premium_100 = calculated_level.technical_premium_100 or 0
        benchmark_premium_net_100 = calculated_level.benchmark_premium_net_100 or 0
        technical_premium_net_100 = calculated_level.technical_premium_net_100 or 0
        expected_loss_cost_100 = calculated_level.expected_loss_cost_100 or 0
        
        # Assign expected losses
        calculated_level.expected_loss_cost_pre_uw_adj_100 = exp_loss_pre_adj_100 = expected_loss_cost_100 or 0
        calculated_level.expected_loss_cost = expected_loss = expected_loss_cost_100 * (calculated_level.written_line or 0)
        calculated_level.expected_loss_cost_pre_uw_adj = expected_loss
        
        # Calculate the impact of UW adjustment
        calculated_level.uw_adj_impact = ratio(expected_loss_cost_100, calculated_level.expected_loss_cost_pre_uw_adj_100) - 1

        benchmark_premium_pre_uw_adj_100 = benchmark_premium_100 * (calculated_level.uw_adj_impact + 1) # node does not exisit in the Data Schema
        calculated_level.technical_premium_pre_uw_adj_100 = technical_premium_pre_uw_adj_100 = exp_loss_pre_adj_100 = technical_premium_100 * (calculated_level.uw_adj_impact + 1)
        calculated_level.benchmark_premium_pre_uw_adj = benchmark_premium_pre_uw_adj_100 * calculated_level.written_line
        calculated_level.technical_premium_pre_uw_adj = calculated_level.technical_premium_pre_uw_adj_100 * calculated_level.written_line

        calculated_level.bpi = ratio(quoted_premium_net_100, benchmark_premium_net_100)
        calculated_level.tpi = ratio(quoted_premium_net_100, technical_premium_net_100) # NET BASIS ESSENTIAL to since Brokearge amount maintain for Advanced features
        calculated_level.tpi_pre_uw_adj = ratio(quoted_premium_100, technical_premium_pre_uw_adj_100)
        calculated_level.bpi_pre_uw_adj = ratio(quoted_premium_100, benchmark_premium_pre_uw_adj_100)
        # calculated_level.bpi_pre_uw_adj = calculated_level.bpi * (calculated_level.uw_adj_impact + 1)

    # For case pricing only
    if hxd.cds.standard_fields.is_case_priced and calculated_level.quoted_premium_100 and calculated_level.bpi_case_priced:
        calculated_level.bpi = calculated_level.bpi_case_priced

        calculated_level.benchmark_premium_100 = ratio(calculated_level.quoted_premium_100, calculated_level.bpi)
        calculated_level.benchmark_premium_net_100 = benchmark_premium_net_100 = calculated_level.benchmark_premium_100 * bkg_netting_down_factor
        calculated_level.expected_loss_cost_100 = calculated_level.expected_loss_inc_nmp = expected_loss_cost_100 = benchmark_premium_net_100 * benchmark_lr or 0

        calculated_level.technical_premium_net_100 = ratio((expected_loss_cost_100 * (1 + che) + fixed_exp), technical_lr)
        calculated_level.technical_premium_100 = ratio(calculated_level.technical_premium_net_100, bkg_netting_down_factor)

        calculated_level.tpi = ratio(calculated_level.quoted_premium_100, calculated_level.technical_premium_100)
        
        calculated_level.tpi_pre_uw_adj = calculated_level.tpi
        calculated_level.technical_premium_pre_uw_adj_100 = calculated_level.technical_premium_100

    expected_loss_cost_100 = calculated_level.expected_loss_cost_100 or 0
    benchmark_premium_net_100 = calculated_level.benchmark_premium_net_100 or 0
    # pflr is equal to net_loss_ratio in Excel
    calculated_level.pflr = ratio(expected_loss_cost_100, quoted_premium_net_100)
    # calculated_level.pflr = ratio(benchmark_lr, calculated_level.bpi)
    calculated_level.pflr_pre_uw_adj = ratio(expected_loss_cost_100, quoted_premium_net_100)
    # calculated_level.roc = ratio(1 - calculated_level.pflr - var_exp + inv_inc - (cost_of_ri - ri_rec) - ratio(fixed_exp + expected_loss_cost_100 * che, quoted_premium_net_100), capital_req)
    calculated_level.glr = ratio(expected_loss_cost_100, quoted_premium_100)
    # calculated_level.glr = ratio(expected_loss_cost_100, quoted_premium_gross_100)
    calculated_level.roc = ratio((expected_loss_cost_100 * ( 1 + che ) + fixed_exp) - quoted_premium_net_100 * (1 - var_exp + inv_inc - (cost_of_ri - ri_rec)) , (-quoted_premium_net_100 * capital_req) )

    # for completeness
    calculated_level.model_premium = 0
    calculated_level.unity_premium = 0

    ##############################
    ## Assign variables for ABZ share and Annualised quoted, technical, benchmark
    ##############################

    # NOTE - RARC requirement - Calculate annualised premium, insurer's share and net premium. These will be used for rate change and reporting
    calculated_level.quoted_premium_annual_100 = (calculated_level.quoted_premium_100 or 0) / (rf.policy_term or 1)
    calculated_level.quoted_premium_annual = (calculated_level.quoted_premium_annual_100 or 0) * (calculated_level.written_line or 0)
    # quoted_premium_net_100 = (calculated_level.quoted_premium_100 or 0) * (1-(calculated_level.brokerage or 0))
    calculated_level.quoted_premium = (calculated_level.quoted_premium_100 or 0) * (calculated_level.written_line or 0)
    calculated_level.quoted_premium_net = (quoted_premium_net_100 or 0) * (calculated_level.written_line or 0)

    calculated_level.benchmark_premium_annual_100 = (calculated_level.benchmark_premium_100 or 0) / (rf.policy_term or 1)
    calculated_level.benchmark_premium_annual = (calculated_level.benchmark_premium_annual_100 or 0) * (calculated_level.written_line or 0)
    # calculated_level.benchmark_premium_net_100 = (calculated_level.benchmark_premium_100 or 0) * (1-(calculated_level.brokerage or 0))
    calculated_level.benchmark_premium = (calculated_level.benchmark_premium_100 or 0) * (calculated_level.written_line or 0)
    calculated_level.benchmark_premium_net = (benchmark_premium_net_100 or 0) * (calculated_level.written_line or 0)
        
    calculated_level.technical_premium_annual_100 = (calculated_level.technical_premium_100 or 0) / (rf.policy_term or 1)
    calculated_level.technical_premium_annual = (calculated_level.technical_premium_annual_100 or 0) * (calculated_level.written_line or 0)
    # calculated_level.technical_premium_net_100 = (calculated_level.technical_premium_100 or 0) * (1-(calculated_level.brokerage or 0))
    calculated_level.technical_premium = (calculated_level.technical_premium_100 or 0) * (calculated_level.written_line or 0)
    calculated_level.technical_premium_net = (calculated_level.technical_premium_net_100 or 0) * (calculated_level.written_line or 0)

