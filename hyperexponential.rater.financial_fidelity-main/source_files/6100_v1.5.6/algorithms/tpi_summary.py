import hx
import pandas as pd
import numpy as np
from algorithms import parameter_tables_schema as params
from algorithms.utils_functions import ratio


def tpi_summary(hxd):
    layer = hxd.cds.layers[0]
    exp_agg = hxd.cds.exposure.aggregate
    cov = layer.coverages
    
    beazley_share = layer.beazley_share if layer.quota_share_flag else 1

    # Add any endorsements to unity and final premium 
    if layer.is_follow and layer.quota_share_flag:
        layer.final_premium = layer.lead_premium * beazley_share
    else:
        layer.final_premium = (layer.final_premium + layer.premium_bearing_endorsements_total.premium) * beazley_share
    layer.final_premium_annual = layer.final_premium / layer.term_adjustment
    layer.unity_premium = (layer.unity_premium + layer.premium_bearing_endorsements_total.benchmark_premium) * beazley_share
    
    # Assign value to quoted premium to align with other raters
    layer.quoted_premium = layer.final_premium        

    # Calc. deviation from unity 
    layer.bound_deviation_from_unity = layer.final_premium / layer.unity_premium if layer.unity_premium else None
    
    # EL excludes brokerage and schedule rating 
 
    layer.net_benchmark_premium = layer.unity_premium * (1 - layer.assumed_brokerage) * layer.priced_to_lr / layer.benchmark_lr if layer.benchmark_lr else 0
    expected_loss = layer.net_benchmark_premium * layer.benchmark_lr

    # Calculate gross and net benchmark premium and dollar value of modifiers
    layer.benchmark_premium = layer.net_benchmark_premium/(1 - layer.brokerage) if layer.brokerage != 1 else 0
    layer.modifiers_dollar_value = layer.final_premium*layer.total_modifiers.uw_selected
    
    # Pull in technical premium parameters and fx rates from user library 
    tp_params_df = params.tp_parameters.df()
    fx_rates_df = params.fx_rates.df()
    yoa = hxd.hx_core.inception_date.year
    # To stop the model erroring if the inception year defaults to an old year not in the TP data
    if yoa in list(tp_params_df["year"]):
        tp_year = yoa
    else:
        tp_year = tp_params_df["year"].max()
    
    # Placeholder variables: update with correct benchmark class and modelled expected loss, this might need to 
    # be linked if a rater can write to more than one class. May link to benchmark class in risk information.
    # bp_class = hxd.cds.standard_fields.benchmark_class
    bp_class = 'Fidelity and Crime'

    # Define function to look up bp class
    def tp_lookup(vbl, bp_class):
        out = tp_params_df[
            (tp_params_df['business_plan_class'] == bp_class)
            & (tp_params_df['year'] == tp_year)
        ][vbl].iloc[0]
        return out

    # Set up tp params
    che = tp_lookup("che", bp_class)
    var_exp = tp_lookup("var_exp", bp_class)
    inv_inc = tp_lookup("inv_inc", bp_class)
    cost_of_ri = tp_lookup("cost_of_ri", bp_class)
    ri_rec = tp_lookup("ri_rec", bp_class)
    roc = tp_lookup("roc", bp_class)
    fixed_exp = tp_lookup("fixed_exp", bp_class)
    capital_req = tp_lookup("capital_req", bp_class)
    nmp_load = tp_lookup("nmp_load", bp_class)

    # Calculate technical loss ratio
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc*capital_req

    # TPI / BPI / technical premium calc
    if hxd.cds.standard_fields.is_rater_priced:
        if expected_loss == 0:
            layer.technical_premium_net = 0
            layer.technical_premium = 0
            layer.bpi = None
            layer.tpi = None
            layer.tpi_pre_uw_adj = None
            layer.bpi_pre_uw_adj = None
        else:
            layer.technical_premium_net = (expected_loss*(1+che) + fixed_exp)/technical_lr if technical_lr else 0
            layer.technical_premium = layer.technical_premium_net / (1 - layer.brokerage) if layer.brokerage != 1 else 0
            layer.tpi = layer.final_premium/layer.technical_premium if layer.technical_premium else 0
            layer.bpi = layer.final_premium/layer.benchmark_premium if layer.benchmark_premium else 0
            layer.tpi_pre_uw_adj = layer.tpi
            layer.bpi_pre_uw_adj = layer.bpi
            layer.pflr = ratio(layer.benchmark_lr, layer.bpi)  
            layer.pflr_pre_uw_adj = layer.pflr
           
        layer.uw_adj_impact = 0   
        layer.written_line_view = 1
     
    else:
        if hxd.cds.standard_fields.is_case_priced and layer.quoted_premium_case_priced and layer.bpi_case_priced:
            layer.benchmark_premium_case_priced = ratio(layer.quoted_premium_case_priced, layer.bpi_case_priced)
            layer.expected_loss_cost = layer.benchmark_premium_case_priced * layer.benchmark_lr * (1-layer.brokerage)
            
            layer.technical_premium_net = ratio((layer.expected_loss_cost*(1+che) + fixed_exp), technical_lr)
            layer.technical_premium_case_priced = ratio(layer.technical_premium_net, (1-layer.brokerage))
                        
            layer.tpi_case_priced = ratio(layer.quoted_premium_case_priced, layer.technical_premium_case_priced)

            layer.pflr = ratio(layer.benchmark_lr, layer.bpi_case_priced)
            layer.tpi_pre_uw_adj = layer.tpi_case_priced
          
            quoted_premium_net = layer.quoted_premium_case_priced * (1-layer.brokerage)

            layer.roc = ratio(
                1 - layer.pflr - var_exp + inv_inc - (cost_of_ri-ri_rec) - ratio(fixed_exp + layer.expected_loss_cost*che, quoted_premium_net),
                capital_req
            )
        layer.written_line_view = layer.written_line


    
    # Calc. ULR
    ulr = layer.benchmark_lr/layer.bpi if layer.bpi else 0

          
    # Calc. core data
    hxd.hx_core.ulr = ulr
    hxd.hx_core.model_premium = layer.benchmark_premium
    hxd.hx_core.charged_premium = layer.final_premium


    
    pass
