import hx
import pandas as pd
import numpy as np
import algorithms.rate_constants as const
from algorithms import parameter_tables_schema as params
from algorithms.rate_utilities import ratio, look_up
from algorithms.rate_constants import benchmark_lr


def rate_rating_summary(hxd):

    rf = hxd.cds.rating_factors
    
    # Set rating methodology
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == 'Case Priced'
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == 'Rater'

    # Pull in technical premium parameters and fx rates from user library 
    tp_params_df = params.tp_parameters.df()
    fx_rates_df = params.fx_rates.df()
    yoa = hxd.hx_core.inception_date.year
    # To stop the model erroring if the inception year defaults to an old year not in the TP data
    if yoa in list(tp_params_df['year']):
        tp_year = yoa
    else:
        tp_year = tp_params_df['year'].max()
    
    # Placeholder variables: update with correct benchmark class and modelled expected loss, this might need to 
    # be linked if a rater can write to more than one class. May link to benchmark class in risk information.
    # bp_class = hxd.cds.standard_fields.benchmark_class
    bp_class = 'Fidelity and Crime' #PLACEHOLDER

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

    # Convert fixed expenses to model currency (default to USD if error)
    ccy = hxd.cds.currencies.source_currency
    fixed_exp = fixed_exp_usd * look_up(ccy, 'ccy', 'fx_rate', fx_rates_df, if_not_found=1)

    # Calculate technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc*capital_req

    '''
    If there is only ever one layer, use the following code to work with the first element of the layer list without having to loop
    '''
    # layer = hxd.cds.layers[0]
    # layer.expected_loss_cost = 10000 # EXAMPLE

    option_to_bind = hxd.cds.option_to_bind
    for layer_no, layer in enumerate(hxd.cds.layers):
        
        # Set status & section reference
        layer.section_reference = hxd.cds.standard_fields.policy_reference
        
        # Set written line to 100%
        layer.written_line = 1

        # Set Brokerage
        layer.brokerage = hxd.cds.brokerage.selected

        # Set technical premium
        layer.technical_premium = layer.kpis.total.technical_premium.premium

        # Set TPIs
        layer.tpi_pre_uw_adj = layer.kpis.total.tpi_pre_uw_adj
        layer.tpi = layer.kpis.total.tpi

        # If rater priced
        if hxd.cds.standard_fields.is_rater_priced:
            # Set quoted premium
            layer.quoted_premium = layer.kpis.total.commercial_premium.premium

            if  layer.quoted_premium:
                # Calculate PFLR
                net_benchmark_premium = layer.expected_loss_cost / benchmark_lr
                commission = layer.brokerage 
                gross_benchmark_premium = ratio(net_benchmark_premium, (1-commission))
                layer.benchmark_premium = gross_benchmark_premium

                actual_premium = layer.quoted_premium if layer.quoted_premium else 0 
                layer.bpi = actual_premium / gross_benchmark_premium if gross_benchmark_premium else 0
                layer.pflr = ratio(layer.expected_loss_cost, actual_premium)
                layer.kpis.total.pflr = layer.pflr
                commercial_prem_pre_adj = layer.kpis.total.commercial_premium_pre_uw_adj.premium if layer.kpis.total.commercial_premium_pre_uw_adj.premium else 0
                layer.pflr_pre_uw_adj = ratio(layer.expected_loss_cost, commercial_prem_pre_adj)
                layer.kpis.total.pflr_pre_uw_adj = layer.pflr_pre_uw_adj
                layer.pflr_cat = layer.pflr * (layer.kpis.pflr_split.ws_perc + layer.kpis.pflr_split.eq_perc)
                layer.pflr_att = layer.pflr - layer.pflr_cat

                layer.roc = ratio(
                    1 - layer.pflr - var_exp + inv_inc - (cost_of_ri-ri_rec) - ratio(fixed_exp + layer.expected_loss_cost*che, layer.quoted_premium * (1-commission)),
                    capital_req
                )

        # For case pricing only
        if hxd.cds.standard_fields.is_case_priced and layer.quoted_premium_case_priced and layer.bpi_case_priced:
            commission = layer.brokerage 
            layer.quoted_premium = layer.quoted_premium_case_priced
            layer.bpi = layer.bpi_case_priced
            layer.benchmark_premium = ratio(layer.quoted_premium, layer.bpi)
            layer.pflr = ratio(benchmark_lr, layer.bpi)

            layer.roc = ratio(
                1 - layer.pflr - var_exp + inv_inc - (cost_of_ri-ri_rec) - ratio(fixed_exp + layer.expected_loss_cost*che, layer.quoted_premium * (1-commission)),
                capital_req
            )

        # Store annualised premiums for use in rate change calcs
        layer.quoted_premium_annualised = (layer.quoted_premium or 0) / (rf.policy_term or 1)
        layer.benchmark_premium_annualised = (layer.benchmark_premium or 0) / (rf.policy_term or 1)
