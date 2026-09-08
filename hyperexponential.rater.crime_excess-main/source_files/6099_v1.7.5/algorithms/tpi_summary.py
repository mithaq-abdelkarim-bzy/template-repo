import hx
import pandas as pd
import numpy as np
import algorithms.utils_functions as fx
from algorithms.rate_constants import *
from algorithms import parameter_tables_schema as params
from algorithms.rate_utilities import ratio


def tpi_summary(hxd):
    cds = hxd.cds
    layer = cds.layers[0]
    param_gbl = fx.df_to_dict(hx.params.global_params, "Variable", "Value")

    layer.status_view = layer.status

    # Updated Final unity premium
    cds.conditions_met = True
    layer.unity_premium = cds.admitted_excess.rounded_premium.value.calculated * cds.beazley_share if cds.admitted_excess.rounded_premium.value.calculated else 0
    layer.unity_premium_annual = layer.unity_premium / cds.term_adjustment
    
    #Calculate the premiums (run code only if inputs for the quoted layer and the one right under it are valid)
    if cds.underlying_rate_per_m and cds.beazley_limit and cds.beazley_share:

        # Calc. deviation from unity 
        layer.deviation_from_unity = layer.final_premium / layer.unity_premium if layer.unity_premium else 0

        #library.algorithms.  can delete (current) rows 23 32
        # Benchmark premiums (Remove section when switching to new benchmark calcs)
        # Calc. basic excess portion
        basic_excess_premium = (1-cds.social_engineering_allocation) * layer.unity_premium
        # Calc. social engineering portion (assumed excess factor of 60% from xs se rater)
        if cds.social_engineering_sublimit > 0:
            se_premium = cds.social_engineering_allocation * cds.beazley_share * cds.underlying_premium*0.6 * cds.social_engineering_limit/cds.social_engineering_sublimit
        else: 
            se_premium = cds.social_engineering_allocation * layer.unity_premium
        # Calc. combined benchmark premiums
        expected_loss = (basic_excess_premium + se_premium) * (1 - layer.brokerage) * 0.51
        layer.net_benchmark_premium = expected_loss / 0.7
        layer.benchmark_premium = layer.net_benchmark_premium / (1 - layer.brokerage)

        
        #Can be deleted
        # # Benchmark premiums (Uncomment to replace section above when switching to new benchmark calcs)
        # ###layer.unity_premium path_model_prem
        hxd.cds.conditions_met = True
        # expected_loss = layer.unity_premium * priced_to_lr
        # layer.net_benchmark_premium = expected_loss / benchmark_lr
        # layer.benchmark_premium = layer.net_benchmark_premium / (1 - layer.brokerage)        

        # Technical loss ratio parameters
        # Pull in technical premium parameters and fx rates from user library 
        tp_params_df = params.tp_parameters.df()
        fx_rates_df = params.fx_rates.df()
        yoa = hxd.hx_core.inception_date.year
        # To stop the model erroring if the inception year defaults to an old year not in the TP data
        if yoa in list(tp_params_df["year"]):
            tp_year = yoa
        else:
            tp_year = tp_params_df["year"].max()

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
        if expected_loss == 0:
            layer.net_technical_premium = 0
            layer.technical_premium = 0
            layer.bpi = None
            layer.tpi = None
            layer.tpi_pre_uw_adj = None
            layer.bpi_pre_uw_adj = None
        else:
            layer.net_technical_premium = (expected_loss * (1+che) + fixed_exp) / technical_lr
            layer.technical_premium = layer.net_technical_premium / (1-layer.brokerage)
            layer.tpi =  layer.final_premium / layer.technical_premium
            layer.bpi =  layer.final_premium / layer.benchmark_premium
            layer.tpi_pre_uw_adj = layer.tpi
            layer.bpi_pre_uw_adj = layer.bpi

        
        # Calc. ULR
        ulr = benchmark_lr/layer.bpi if layer.bpi else 0

            
        # Calc. core data
        hxd.hx_core.ulr = ulr
        hxd.hx_core.model_premium = layer.benchmark_premium
        hxd.hx_core.charged_premium = layer.final_premium

        if hxd.cds.standard_fields.is_rater_priced:
           layer.written_line_view = 1  
           layer.pflr = ratio(benchmark_lr, layer.bpi) if layer.bpi else 0
           layer.pflr_pre_uw_adj = layer.pflr
           
        layer.uw_adj_impact = 0


        pass
