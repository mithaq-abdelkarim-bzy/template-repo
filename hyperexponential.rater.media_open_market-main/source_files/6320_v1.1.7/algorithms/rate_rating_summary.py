import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_constants as const
from algorithms import parameter_tables_schema as params
import algorithms.rate_utilities as utils
import algorithms.rate_pricing_functions as pricing_funcs
from operator import itemgetter
from datetime import datetime
from dateutil.relativedelta import relativedelta
from functools import reduce
# Import helper functions:
from algorithms.rate_helpers import eec_ilf_calcs, agg_ilf_calcs, idf_calcs, benchmark_prem_calcs, technical_prem_calcs, nonstandard_idf_calcs


def rate_rating_summary(hxd):
    cds = hxd.cds
    hx_core = hxd.hx_core
    rf = cds.rating_factors
    
    # Labels ------------------------------------------
    # Set option labels
    for index, option in enumerate(cds.options):        
        #Set the label for each option:
        option.option_label = f"Option {index+1}"


    # Set layer labels
    for index, layer in enumerate(hxd.cds.layers):        

        #Set the label for each layer:
        if index == 0:
            layer.layer_label = "Primary Layer"
        else:
            layer.layer_label = f"Excess {index}"

        # Set up the view page
        if index == 0 :
            layer.excess_flag = False
        else:
            layer.excess_flag = True
            
    cds.primary.layer_label = "Primary Layer"

    # Set rating methodology ------------------------
    cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == 'Case Priced'
    cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == 'Rater'

    # Set show/hide masking ---
    cds.rater_priced_standard = cds.standard_fields.is_rater_priced and cds.standard_rater_masking
    cds.rater_priced_nonstandard = cds.standard_fields.is_rater_priced and cds.nonstandard_rater_masking
    cds.rater_priced_excess = cds.standard_fields.is_rater_priced and cds.price_excess_flag
    cds.coverage_selected_flag = cds.standard_rater_masking or cds.nonstandard_rater_masking # True when one of the coverages has been selected in Risk Info tab 
    
    # FX rate for currency conversion ---------------
    fx_rates_df = params.fx_rates.df()
    ccy = hxd.cds.currencies.source_currency
    fx_rate = utils.look_up(ccy, 'ccy', 'fx_rate', fx_rates_df, if_not_found=1) # default to USD if error

    # Technical Premium parameters ------------------
    # Pull in technical premium parameters and fx rates from user library 
    tp_params_df = params.tp_parameters.df()

    # To stop the model erroring if the inception year defaults to an old year not in the TP data
    yoa = hxd.hx_core.inception_date.year
    tp_year = yoa if yoa in tp_params_df["year"].values else tp_params_df["year"].max()
    
    # Business Plan class
    bp_class = const.bp_class

    tp_lookup_bool = (tp_params_df['business_plan_class'] == bp_class) & (tp_params_df['year'] == tp_year)
    tp_params = tp_params_df[tp_lookup_bool]

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

    # Convert fixed expenses to model currency
    fixed_exp = fixed_exp_usd * fx_rate

    # Calculate technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc*capital_req

    # Pro Rata Factor -------------------------
    inception = hx_core.inception_date
    expiry = hx_core.expiry_date
    pro_rata_factor = utils.policy_term(inception, expiry)


    # If rater priced ----------------------------------------------------------------------------------------
    if hxd.cds.standard_fields.is_rater_priced:

        # STANDARD RATER CALCULATIONS [Media Liability, Music Liabilty, TV & Film E&O] -----------------------
        if cds.standard_rater_masking:
            pricing_funcs.pricing_standard_rater_calcs(hxd, tp_params, fx_rate, pro_rata_factor)


        # NON-STANDARD RATER CALCULATIONS [Individual TV, Individual Film, Annual TV] --------------------
        if cds.nonstandard_rater_masking:
            pricing_funcs.pricing_nonstandard_rater_calcs(hxd, tp_params, fx_rate)

        # EXCESS PRICING CALCULATIONS ------------------------------------------------------------------------------
        layers = cds.layers

        if cds.price_excess_flag:
            pricing_funcs.pricing_excess_calcs(hxd, tp_params, fx_rate, pro_rata_factor)


        if cds.price_excess_flag == False:
            layers[0].status = cds.primary.status
            layers[0].section_reference = cds.primary.section_reference
            layers[0].aggregate_limit = cds.primary.aggregate_limit_view
            layers[0].attachment = cds.primary.attachment
            layers[0].quoted_premium = cds.primary.quoted_premium_view
            layers[0].quoted_premium_net = (cds.primary.quoted_premium_view or 0) * (1 - (cds.primary.brokerage or 0)) if cds.primary.quoted_premium_view else None
            layers[0].benchmark_premium = cds.primary.benchmark_premium
            layers[0].benchmark_premium_net = cds.primary.benchmark_premium_net
            layers[0].technical_premium = cds.primary.technical_premium
            layers[0].technical_premium_net = cds.primary.technical_premium_net
            layers[0].bpi = cds.primary.bpi
            layers[0].tpi = cds.primary.tpi
            layers[0].bpi_pre_uw_adj = cds.primary.bpi_pre_uw_adj
            layers[0].tpi_pre_uw_adj = cds.primary.tpi_pre_uw_adj
            layers[0].brokerage = cds.primary.brokerage
            layers[0].written_line = 1 # For Standard KPIs tab

            # UW Adj Impact calcs
            uw_adj_impact = utils.ratio(cds.primary.expected_loss_cost, cds.primary.expected_loss_cost_pre_uw_adj) - 1 if cds.primary.expected_loss_cost_pre_uw_adj else None
            pflr = utils.ratio(const.benchmark_lr, cds.primary.bpi) if cds.primary.bpi else None
            pflr_pre_uw_adj = utils.ratio(const.benchmark_lr, cds.primary.bpi_pre_uw_adj) if cds.primary.bpi_pre_uw_adj else None
            # Assign to layer 0 nodes
            layers[0].uw_adj_impact = uw_adj_impact
            layers[0].pflr = pflr
            layers[0].pflr_pre_uw_adj = pflr_pre_uw_adj


    layers = cds.layers
    # For case pricing only -------------------------------
    if cds.standard_fields.is_case_priced:
        for layer in cds.layers:
            # Set outputs for Standard KPIs page
            layer.status = layer.status_view
            layer.section_reference = layer.section_reference_view
            layer.brokerage = layer.brokerage_input or 0
            layer.written_line = layer.written_line_input
            layer.quoted_premium = layer.quoted_premium_view
            layer.bpi = layer.bpi_case_priced

            # Premium calculations
            if layer.bpi and layer.quoted_premium: # Only calculate when bpi and quoted premium have been entered.
                layer.benchmark_premium = utils.ratio(layer.quoted_premium, layer.bpi)
                layer.expected_loss_cost = layer.benchmark_premium * const.benchmark_lr * (1-layer.brokerage)

                layer.technical_premium_net = utils.ratio((layer.expected_loss_cost*(1+che) + fixed_exp), technical_lr)
                layer.technical_premium = utils.ratio(layer.technical_premium_net, (1-layer.brokerage))
  
                layer.tpi = utils.ratio(layer.quoted_premium, layer.technical_premium)

                layer.pflr = utils.ratio(const.benchmark_lr, layer.bpi)
                layer.tpi_pre_uw_adj = layer.tpi
                layer.technical_premium_pre_uw_adj = layer.technical_premium
            
                layer.quoted_premium_net = layer.quoted_premium * (1-layer.brokerage) if layer.quoted_premium else None

                layer.roc = utils.ratio(
                    1 - layer.pflr - var_exp + inv_inc - (cost_of_ri-ri_rec) - utils.ratio(fixed_exp + layer.expected_loss_cost*che, layer.quoted_premium_net),
                    capital_req
                )


    # For rate change calcs ----------------------
    for index, layer in enumerate(layers):

        # Store annualised premiums
        layer.quoted_premium_annualised = (layer.quoted_premium or 0) / (rf.policy_term or 1)
        layer.benchmark_premium_annualised = (layer.benchmark_premium or 0) / (rf.policy_term or 1)
        layer.quoted_premium_annual = (layer.quoted_premium or 0) / (rf.policy_term or 1)
        layer.benchmark_premium_annual = (layer.benchmark_premium or 0) / (rf.policy_term or 1)

        # All calcs are already made on 100% written line basis.
        layer.expected_loss_cost_100 = layer.expected_loss_cost or 0
        
        # Pick up bound premium if it is entered, otherwise pick up quoted premium 
        if (index==0) and cds.primary.bound_premium: # necessary because layer.0.bound_premium is always empty, due to view setup
            premium = cds.primary.bound_premium
            premium_net = cds.primary.bound_premium * (1 - (layer.brokerage or 0))
            premium_annual = (cds.primary.bound_premium or 0) / (rf.policy_term or 1)
        elif layer.bound_premium:
            premium = layer.bound_premium
            premium_net = layer.bound_premium * (1 - (layer.brokerage or 0)) 
            premium_annual = (layer.bound_premium or 0) / (rf.policy_term or 1)
        else:
            premium = layer.quoted_premium or 0
            premium_net = layer.quoted_premium_net or 0
            premium_annual = layer.quoted_premium_annual or 0
        
        # Always assume written line is 100% in this model
        layer.quoted_premium_100 = premium
        layer.quoted_premium_net_100 = premium_net
        layer.quoted_premium_annual_100 = premium_annual

        layer.benchmark_premium_100 = layer.benchmark_premium or 0
        layer.benchmark_premium_net_100 = layer.benchmark_premium_net or 0
        layer.benchmark_premium_annual_100 = layer.benchmark_premium_annual or 0
        layer.technical_premium_100 = layer.technical_premium or 0
        layer.technical_premium_net_100 = layer.technical_premium_net or 0

        layer.currency = cds.currencies.source_currency or "USD"
    
