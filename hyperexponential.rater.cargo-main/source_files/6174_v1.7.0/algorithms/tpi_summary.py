import hx
import pandas as pd
import numpy as np
from algorithms import parameter_tables_schema as params
from algorithms.rate_utilities import one_layer, ratio, look_up, tp_lookup
from algorithms.rate_constants import benchmark_lr

def tpi_summary(hxd):

    layer, cvg = one_layer(hxd)

    # Set rating methodology
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == "Case Priced"
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == "Rater"

    # Pull in technical premium parameters from user library 
    tp_params_df = params.tp_parameters.df()
    fx_rates_df = params.fx_rates.df()

    # Get YOA
    yoa = hxd.hx_core.inception_date.year
    tp_year = yoa if yoa in list(tp_params_df["year"]) else tp_params_df["year"].max()

    # Placeholder variables: update with correct benchmark class and modelled expected loss, this might need to 
    # be linked if a rater can write to more than one class. May link to benchmark class in risk information.
    bp_class = hxd.cds.standard_fields.benchmark_class

    # Set up tp params
    che = tp_lookup("che", bp_class, tp_year)
    var_exp = tp_lookup("var_exp", bp_class, tp_year)
    inv_inc = tp_lookup("inv_inc", bp_class, tp_year)
    cost_of_ri = tp_lookup("cost_of_ri", bp_class, tp_year)
    ri_rec = tp_lookup("ri_rec", bp_class, tp_year)
    roc = tp_lookup("roc", bp_class, tp_year)
    fixed_exp_usd = tp_lookup("fixed_exp", bp_class, tp_year)
    capital_req = tp_lookup("capital_req", bp_class, tp_year)
    nmp_load = tp_lookup("nmp_load", bp_class, tp_year)
    
    # Convert fixed expenses to model currency (default to USD if error)
    ccy = hxd.cds.currencies.source_currency
    fixed_exp = fixed_exp_usd * look_up(ccy, "ccy", "fx_rate", fx_rates_df, if_not_found=1)

    # Calculate technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri-ri_rec) - roc * capital_req

    # NOTE: uncomment for testing in development - set specific values to technical factors to match results
    # che = 0.0095593864822655
    # fixed_exp = 877.940747122909
    # technical_lr = 0.863326359905082

    # If rater priced
    if hxd.cds.standard_fields.is_rater_priced and layer.quoted_premium:

        share_expected_loss = layer.expected_loss_cost * layer.written_line
        layer.technical_premium_net = ratio(
            ratio((share_expected_loss*(1+che) + fixed_exp), technical_lr),
            layer.written_line
        )
        layer.technical_premium = ratio(layer.technical_premium_net, (1-layer.brokerage))
        
        share_expected_loss_pre_uw_adj = layer.expected_loss_cost_pre_uw_adj * layer.written_line
        technical_premium_pre_uw_adj_net = ratio(
            ratio((share_expected_loss_pre_uw_adj*(1+che) + fixed_exp), technical_lr), 
            layer.written_line
        )
        layer.technical_premium_pre_uw_adj = ratio(technical_premium_pre_uw_adj_net, (1-layer.brokerage))
        
        layer.benchmark_premium = ratio(
            ratio(layer.expected_loss_cost, benchmark_lr), 
            (1-layer.brokerage)
        )

        bencmark_premium_pre_uw_adj = ratio(
            ratio(layer.expected_loss_cost_pre_uw_adj, benchmark_lr),
            (1-layer.brokerage)
        )

        layer.bpi = ratio(layer.quoted_premium, layer.benchmark_premium)
        layer.bpi_pre_uw_adj = ratio(layer.quoted_premium,bencmark_premium_pre_uw_adj )
        layer.tpi = ratio(layer.quoted_premium, layer.technical_premium)
        layer.tpi_pre_uw_adj = ratio(layer.quoted_premium, layer.technical_premium_pre_uw_adj)
        
        quoted_premium_net = layer.quoted_premium * (1-layer.brokerage)
        layer.pflr = ratio(layer.expected_loss_cost, (quoted_premium_net or 1))
        layer.pflr_att = ratio(layer.expected_loss_cost_att, (quoted_premium_net or 1))
        layer.pflr_cat = ratio(layer.expected_loss_cost_cat, (quoted_premium_net or 1))
        layer.pflr_pre_uw_adj  =  ratio(layer.expected_loss_cost_pre_uw_adj, (quoted_premium_net or 1))

        layer.roc = ratio(
            1 - layer.pflr - var_exp + inv_inc - (cost_of_ri-ri_rec) - ratio(fixed_exp + layer.expected_loss_cost*che, quoted_premium_net),
            capital_req
        )

        layer.uw_adj_impact = ratio(layer.expected_loss_cost, layer.expected_loss_cost_pre_uw_adj) - 1
    
    # For add on Cargo Cyber
    layer_cyber = layer.coverages.cargo_cyber_addon
    is_cargo_cyber_addon = hxd.cds.cover_selection.is_cargo_cyber
    if hxd.cds.standard_fields.is_rater_priced and layer_cyber.quoted_premium and is_cargo_cyber_addon:
        
        share_expected_loss = layer_cyber.expected_loss_cost * layer_cyber.written_line
        layer_cyber.technical_premium_net = ratio(
            ratio((share_expected_loss*(1+che) + fixed_exp), technical_lr),
            layer_cyber.written_line
        )
        layer_cyber.technical_premium = ratio(layer_cyber.technical_premium_net, (1-layer_cyber.brokerage))
        
        share_expected_loss_pre_uw_adj = layer_cyber.expected_loss_cost_pre_uw_adj * layer_cyber.written_line
        technical_premium_pre_uw_adj_net = ratio(
            ratio((share_expected_loss_pre_uw_adj*(1+che) + fixed_exp), technical_lr), 
            layer_cyber.written_line
        )
        layer_cyber.technical_premium_pre_uw_adj = ratio(technical_premium_pre_uw_adj_net, (1-layer_cyber.brokerage))
        
        layer_cyber.benchmark_premium = ratio(
            ratio(layer_cyber.expected_loss_cost, benchmark_lr), 
            (1-layer_cyber.brokerage)
        )

        bencmark_premium_pre_uw_adj = ratio(
            ratio(layer_cyber.expected_loss_cost_pre_uw_adj, benchmark_lr),
            (1-layer_cyber.brokerage)
        )

        layer_cyber.bpi = ratio(layer_cyber.quoted_premium, layer_cyber.benchmark_premium)
        layer_cyber.bpi_pre_uw_adj = ratio(layer_cyber.quoted_premium,bencmark_premium_pre_uw_adj )
        layer_cyber.tpi = ratio(layer_cyber.quoted_premium, layer_cyber.technical_premium)
        layer_cyber.tpi_pre_uw_adj = ratio(layer_cyber.quoted_premium, layer_cyber.technical_premium_pre_uw_adj)
        
        quoted_premium_net = layer_cyber.quoted_premium * (1-layer_cyber.brokerage)
        layer_cyber.pflr = ratio(layer_cyber.expected_loss_cost, (quoted_premium_net or 1))
        layer_cyber.pflr_att = ratio(layer_cyber.expected_loss_cost_att, (quoted_premium_net or 1))
        layer_cyber.pflr_cat = ratio(layer_cyber.expected_loss_cost_cat, (quoted_premium_net or 1))
        layer_cyber.pflr_pre_uw_adj  =  ratio(layer_cyber.expected_loss_cost_pre_uw_adj, (quoted_premium_net or 1))

        layer_cyber.roc = ratio(
            1 - layer_cyber.pflr - var_exp + inv_inc - (cost_of_ri-ri_rec) - ratio(fixed_exp + layer_cyber.expected_loss_cost*che, quoted_premium_net),
            capital_req
        )

        layer_cyber.uw_adj_impact = ratio(layer_cyber.expected_loss_cost, layer_cyber.expected_loss_cost_pre_uw_adj) - 1


    # For case pricing only
    if hxd.cds.standard_fields.is_case_priced and layer.quoted_premium:                
        layer.bpi = layer.bpi_case_priced
        layer.benchmark_premium = ratio(layer.quoted_premium, layer.bpi)
        layer.expected_loss_cost = layer.benchmark_premium * benchmark_lr * (1-layer.brokerage)
        
        share_expected_loss = layer.expected_loss_cost * layer.written_line
        layer.technical_premium_net = ratio(
            ratio((share_expected_loss*(1+che) + fixed_exp), technical_lr),
            layer.written_line
        )
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

        layer.uw_adj_impact = ratio(layer.expected_loss_cost, layer.expected_loss_cost_pre_uw_adj) - 1
        
