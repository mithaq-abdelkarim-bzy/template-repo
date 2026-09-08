import hx
import pandas as pd
import numpy as np
import algorithms.utils_functions as fx
from algorithms.rate_constants import *
from algorithms import parameter_tables_schema as params
from algorithms.rate_utilities import ratio

def rate_rating_summary(hxd):
    cds = hxd.cds
    param_gbl = fx.df_to_dict(hx.params.global_params, "Variable", "Value")

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

    if hxd.cds.standard_fields.is_case_priced:        
        options = hxd.cds.options
        num_options = len(options)
        for index in range(1,max_options+1):
            setattr(hxd.cds.rate_change, f"show_option_{index}", True) if index <= num_options else False     

        for option in hxd.cds.options:  
            option.status_view = option.status
                
            if option.quoted_premium and option.bpi:
                option.benchmark_premium = ratio(option.quoted_premium, option.bpi)
                expected_loss_cost = option.benchmark_premium * benchmark_lr * (1-option.brokerage)
                    
                technical_premium_net = ratio((expected_loss_cost*(1+che) + fixed_exp), technical_lr)
                option.technical_premium = ratio(technical_premium_net, (1-option.brokerage))
                                
                option.tpi = ratio(option.quoted_premium, option.technical_premium)
                option.pflr = ratio(benchmark_lr, option.bpi)
                    
                quoted_premium_net = option.quoted_premium * (1-option.brokerage)

                option.roc = ratio(
                    1 - option.pflr - var_exp + inv_inc - (cost_of_ri-ri_rec) - ratio(fixed_exp + expected_loss_cost*che, quoted_premium_net),
                    capital_req
                )     
        

    pass
