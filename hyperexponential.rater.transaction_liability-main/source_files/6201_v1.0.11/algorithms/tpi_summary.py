import hx
import pandas as pd
import numpy as np
from algorithms import parameter_tables_schema as params
from algorithms.rate_utilities import *
from algorithms.rate_constants import benchmark_lr

def tpi_summary(hxd):
    # Set paths
    freq = hxd.cds.rating_factors.freq

    # Set rating methodology
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == "Case Priced"
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == "Rater"

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
    bp_class = 'M&A'

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
    fixed_exp_usd = tp_lookup("fixed_exp", bp_class)
    capital_req = tp_lookup("capital_req", bp_class)
    nmp_load = tp_lookup("nmp_load", bp_class)

    # Convert fixed expenses to model currency (default to USD if error)
    ccy = hxd.cds.currencies.source_currency
    fixed_exp = fixed_exp_usd * look_up(ccy, 'ccy', 'fx_rate', fx_rates_df, if_not_found=1)

    # Find scaling factors
    scaling_factors_df = hx.params.table_scaling_factors
    scaling_factors = scaling_factors_df.loc[scaling_factors_df["region"] == ("North America" if freq.target.jurisdiction == "North America" else "ROW")]


    for layer in hxd.cds.layers:
        
        # Set default values
        layer.benchmark_premium = 0

        # If rater priced
        if hxd.cds.standard_fields.is_rater_priced and layer.limit:

            # Calculate capital factor based on Excess/Primary
            scaling_factor = scaling_factors["Excess"].item() if layer.excess.selected not in [0, None] else 1
            capital_factor = capital_req * scaling_factor
            # Calculate technical loss ratio (excl. fixed costs)
            technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc*capital_factor

            # Note this is Beazley share for the calculation of TPI. 
            # To update to 100%, scale by line size at the end
            # Expected loss increased by the NMP load
            layer.expected_loss_cost *=  (1 + nmp_load) 
            layer.expected_loss_cost_pre_uw_adj *=  (1 + nmp_load)
            expected_loss = layer.expected_loss_cost
                        
            layer.technical_premium_net = ratio((expected_loss * (1+che) + fixed_exp), technical_lr)
            layer.technical_premium = ratio(layer.technical_premium_net, (1-layer.brokerage))

            layer.technical_premium_pre_uw_adj = ratio(
                ratio((layer.expected_loss_cost_pre_uw_adj * (1+che) + fixed_exp), technical_lr), 
                (1-layer.brokerage)
            )
            layer.benchmark_premium = ratio(
                ratio(expected_loss, benchmark_lr), 
                (1-layer.brokerage)
            )

            if layer.quoted_premium:
                layer.bpi = ratio(layer.quoted_premium, layer.benchmark_premium)
                layer.tpi = ratio(layer.quoted_premium, layer.technical_premium)
                layer.tpi_pre_uw_adj = ratio(layer.quoted_premium, layer.technical_premium_pre_uw_adj)
                
                quoted_premium_net = layer.quoted_premium * (1-layer.brokerage)
                layer.pflr = ratio(expected_loss, (quoted_premium_net or 1))

                #TODO: Revise assumptions
                layer.pflr_cat = nmp_load
                layer.pflr_att = layer.pflr - nmp_load if layer.pflr else 0

                layer.pflr_pre_uw_adj = ratio(layer.expected_loss_cost_pre_uw_adj, (quoted_premium_net or 1))

                layer.roc = ratio(
                    1 - layer.pflr - var_exp + inv_inc - (cost_of_ri-ri_rec) - ratio(fixed_exp + expected_loss*che, quoted_premium_net),
                    capital_req
                )
