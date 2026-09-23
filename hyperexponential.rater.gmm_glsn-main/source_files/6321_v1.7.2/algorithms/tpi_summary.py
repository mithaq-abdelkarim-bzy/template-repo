import hx
import pandas as pd
import numpy as np
from algorithms import parameter_tables_schema as params
from algorithms.rate_utilities import ratio, look_up, _perform_lookup
from algorithms.rate_constants import benchmark_lr

def tpi_summary(hxd):

    # Set rating methodology
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == "Case Priced"
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == "Rater"

    # Pull in technical premium parameters and fx rates from user library 

    # Placeholder variables: update with correct benchmark class and modelled expected loss, this might need to 
    # be linked if a rater can write to more than one class. May link to benchmark class in risk information.
    # bp_class = hxd.cds.standard_fields.benchmark_class
    bp_class = 'Fidelity and Crime' #PLACEHOLDER

    ###################
    # IR edit 22/12 ---

    # Pull in technical premium parameters from user library 
    tp_params = params.tp_parameters.df()

    # To stop the model erroring if the inception year defaults to a year not in the TP data
    yoa = hxd.hx_core.inception_date.year
    tp_year = yoa if yoa in tp_params["year"].values else tp_params["year"].max()

    tp_lookup_bool = (tp_params['business_plan_class'] == bp_class) & (tp_params['year'] == tp_year)
    tp_params_df = tp_params[tp_lookup_bool]

    # end of IR edit 22/12 ---
    #############
        
    # Set up tp params
    che = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['che'].iloc[0]
    var_exp = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['var_exp'].iloc[0]
    inv_inc = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['inv_inc'].iloc[0]
    cost_of_ri = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['cost_of_ri'].iloc[0]
    ri_rec = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['ri_rec'].iloc[0]
    roc = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['roc'].iloc[0]
    fixed_exp_usd = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['fixed_exp'].iloc[0]
    capital_req = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['capital_req'].iloc[0]

    # Convert fixed expenses to model currency (default to USD if error)
    ccy = hxd.cds.currencies.source_currency
    fixed_exp = fixed_exp_usd * look_up(ccy, 'ccy', 'fx_rate', fx_rates_df, if_not_found=1)

    # Calculate technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc*capital_req

    for layer in hxd.cds.layers:
        # If rater priced
        if hxd.cds.standard_fields.is_rater_priced and layer.quoted_premium:
            
            # NOTE if currency varies by layer you must convert fixed expenses fx within 
            # the loop here

            # Note this is Beazley share
            expected_loss = layer.expected_loss_cost
            
            layer.technical_premium_net = ratio((expected_loss*(1+che) + fixed_exp), technical_lr)
            layer.technical_premium = ratio(layer.technical_premium_net, (1-layer.brokerage))

            layer.technical_premium_pre_uw_adj = ratio(
                ratio((expected_loss*(1+che) + fixed_exp), technical_lr), 
                (1-layer.brokerage)
            )
            layer.benchmark_premium = ratio(
                ratio(expected_loss, benchmark_lr), 
                (1-layer.brokerage)
            )

            layer.bpi = ratio(layer.quoted_premium, layer.benchmark_premium)
            layer.tpi = ratio(layer.quoted_premium, layer.technical_premium)
            layer.tpi_pre_uw_adj = ratio(layer.quoted_premium, layer.technical_premium_pre_uw_adj)
            
            quoted_premium_net = layer.quoted_premium * (1-layer.brokerage)
            layer.pflr = ratio(expected_loss, (quoted_premium_net or 1))

            # TODO: add Att and Cat expected loss to common data schema?
            # layer.pflr_att = ratio(layer.expected_loss_cost_att, (quoted_premium_net or 1))
            # layer.pflr_cat = ratio(layer.expected_loss_cost_cat, (quoted_premium_net or 1))

            layer.roc = ratio(
                1 - layer.pflr - var_exp + inv_inc - (cost_of_ri-ri_rec) - ratio(fixed_exp + expected_loss*che, quoted_premium_net),
                capital_req
            )

        # For case pricing only
        if hxd.cds.standard_fields.is_case_priced and layer.quoted_premium and layer.bpi_case_priced:
            layer.bpi = layer.bpi_case_priced
            layer.benchmark_premium = ratio(layer.quoted_premium, layer.bpi)
            layer.expected_loss_cost = layer.benchmark_premium * benchmark_lr * (1-layer.brokerage)
            
            layer.technical_premium_net = ratio((layer.expected_loss_cost*(1+che) + fixed_exp), technical_lr)
            layer.technical_premium = ratio(layer.technical_premium_net, (1-layer.brokerage))
                        
            layer.tpi = ratio(layer.quoted_premium, layer.technical_premium)

            layer.pflr = ratio(benchmark_lr, layer.bpi)
            layer.tpi_pre_uw_adj = layer.tpi
            layer.technical_premium_pre_uw_adj = layer.technical_premium
            
            quoted_premium_net = layer.quoted_premium * (1-layer.brokerage)

            layer.roc = ratio(
                1 - layer.pflr - var_exp + inv_inc - (cost_of_ri-ri_rec) - ratio(fixed_exp + layer.expected_loss_cost*che, quoted_premium_net),
                capital_req
            )
