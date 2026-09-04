import hx
import pandas as pd
import numpy as np
import algorithms.rate_constants as const
from algorithms import parameter_tables_schema as params
from algorithms.rate_utilities import ratio, look_up
from algorithms.rate_constants import benchmark_lr
#from algorithms.tasks import insert_hx_meta_policy_references_task

def rate_rating_summary(hxd):

    rf = hxd.cds.rating_factors
    
    # Set rating methodology
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == 'Case Priced'
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == 'Rater'

    # Pull in technical premium parameters and fx rates from user library 
    
    yoa = hxd.hx_core.inception_date.year
    if yoa <= 2023:

        tp_params_df = hx.params.tbl_tp_parameters_pre2024
        tp_params_df = pd.DataFrame(tp_params_df) # convert table to dataframe
        
    else :
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
    bp_class = 'Hull' 

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

    fx_rates = hx.params.tbl_fx
    fx_usd = look_up('USD', "Currency", "Exchange Rate", fx_rates)
    fx_gbp = look_up(ccy, "Currency", "Exchange Rate", fx_rates) 

    fixed_exp_gbp = fixed_exp_usd / fx_usd

    # Calculate technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc*capital_req

    '''
    If there is only ever one layer, use the following code to work with the first element of the layer list without having to loop
    '''
    layer = hxd.cds.layers[0]

    

    for layer in hxd.cds.layers:

                

        # PLACEHOLDER FORMULA
         # ~~~

        # Calculate the impact of UW adjustment by using Expected Loss Cost and Expected Loss Cost Pre UW Adjustment. 
        # rather than using TP and TP pre UW adjustment for the calc

        layer.section_reference = hxd.cds.standard_fields.policy_reference
        brokerage = layer.brokerage = hxd.cds.brokerage
        beazley_share = layer.written_line  = hxd.cds.beazley_share
        tsi = hxd.cds.exposure.granular.total_sum_insured.total      

        
        # If rater priced
        if hxd.cds.standard_fields.is_rater_priced :
            
            #and layer.quoted_premium


            
            quoted_premium_net = layer.net_kpi.achieved_premium
            
            #Expected Loss
            #NMP loading included in expected loss
            expected_loss_gbp = hxd.cds.exposure.granular.total_expected_loss_gbp
            expected_loss = layer.expected_loss_cost = hxd.cds.exposure.granular.total_expected_loss
            
            # Expected loss pre-UW adjustment
            underwriter_adjustment_factor = (1+hxd.cds.exposure.granular.uw_adjustment)
            exp_loss_pre_adj = layer.expected_loss_cost_pre_uw_adj =  expected_loss / underwriter_adjustment_factor
            layer.uw_adj_impact = ratio(expected_loss, exp_loss_pre_adj) - 1  
            
            # Benchmark Premium
            benchmark_premium_net = layer.net_kpi.benchmark_premium = expected_loss / benchmark_lr
            layer.benchmark_premium = layer.gross_kpi.benchmark_premium = benchmark_premium_net / (1 - brokerage )
            layer.net_kpi.benchmark_rate = ratio(benchmark_premium_net, tsi)
            layer.gross_kpi.benchmark_rate = ratio(layer.benchmark_premium, tsi)

            layer.net_kpi.benchmark_premium = expected_loss / benchmark_lr

            layer.bpi = layer.net_kpi.bpi_post_uw_adj = ratio(quoted_premium_net , benchmark_premium_net)
            layer.bpi_pre_uw_adj = layer.net_kpi.bpi_pre_uw_adj = layer.bpi * (1 + layer.uw_adj_impact)               
            layer.pflr  = layer.net_kpi.pflr = ratio( benchmark_lr , layer.bpi )
            layer.pflr_pre_uw_adj = ratio(layer.pflr ,  (1 + layer.uw_adj_impact)) 
            
            layer.quoted_premium = layer.gross_kpi.achieved_premium = quoted_premium_net / (1 - brokerage )
            layer.net_kpi.achieved_rate = ratio(quoted_premium_net,  tsi)
            layer.gross_kpi.achieved_rate = ratio(layer.quoted_premium ,  tsi)

            # Technical price calculated on 100% basis
            technical_premium_net = layer.net_kpi.technical_premium = (ratio((expected_loss_gbp*beazley_share*(1+che) + fixed_exp_gbp), technical_lr) / beazley_share) * fx_gbp
            layer.technical_premium = ratio(technical_premium_net, (1-brokerage))
             
            layer.tpi = layer.net_kpi.tpi_post_uw_adj = ratio(quoted_premium_net, technical_premium_net)
            
            expected_loss_pre_uw_adj_gbp = expected_loss_gbp/underwriter_adjustment_factor

            technical_premium_pre_uw_adj_net = (ratio((expected_loss_pre_uw_adj_gbp*beazley_share*(1+che) + fixed_exp_gbp), technical_lr) / beazley_share) * fx_gbp
            layer.tpi_pre_uw_adj = layer.net_kpi.tpi_pre_uw_adj = ratio(quoted_premium_net, technical_premium_pre_uw_adj_net)
            
            #Technical premium not calculated prior to 2022 YOA
            if yoa <= 2021 :
                layer.net_kpi.technical_premium = 0
                layer.technical_premium = 0
                layer.tpi = layer.net_kpi.tpi_post_uw_adj = 0
                layer.tpi_pre_uw_adj = 0
            

            #layer.technical_premium_pre_uw_adj = layer.technical_premium_pre_uw_adj_net/ (1-brokerage)
            
            
           

        # For case pricing only
        #if hxd.cds.standard_fields.is_case_priced and layer.quoted_premium and layer.bpi_case_priced:
        if hxd.cds.standard_fields.is_case_priced :    
            
            layer.quoted_premium_case_priced = ratio(layer.quoted_premium_net_case_priced, (1-brokerage))
            layer.quoted_premium = layer.quoted_premium_case_priced

            layer.bpi = layer.bpi_case_priced
            layer.benchmark_premium_net = layer.net_kpi.benchmark_premium = ratio(layer.quoted_premium_net_case_priced, layer.bpi)
            layer.benchmark_premium = ratio(layer.benchmark_premium_net , (1-brokerage))
            
            layer.expected_loss_cost = layer.benchmark_premium * benchmark_lr * (1-brokerage)
            expected_loss_gbp = layer.expected_loss_cost / fx_gbp

            layer.technical_premium_net = layer.net_kpi.technical_premium =  (ratio((expected_loss_gbp*beazley_share*(1+che) + fixed_exp_gbp), technical_lr) / beazley_share) * fx_gbp
            layer.technical_premium = ratio(layer.technical_premium_net, (1-brokerage))
                        
            #layer.tpi = ratio(layer.quoted_premium, layer.technical_premium)

            layer.pflr = ratio( benchmark_lr , layer.bpi )
            layer.tpi_pre_uw_adj = layer.tpi = ratio(layer.quoted_premium_net_case_priced, layer.technical_premium_net)
            layer.technical_premium_pre_uw_adj = layer.technical_premium
            
            #quoted_premium_net = layer.quoted_premium * (1-brokerage)

         #   layer.roc = ratio( 1 - layer.pflr - var_exp + inv_inc - (cost_of_ri-ri_rec) - ratio(fixed_exp + layer.expected_loss_cost*che, quoted_quoted_premium_net),
         #       capital_req            )

        # Store annualised premiums for use in rate change calcs
        layer.quoted_premium_annualised = (layer.quoted_premium or 0) / (rf.policy_term or 1)
        layer.benchmark_premium_annualised = (layer.benchmark_premium or 0) / (rf.policy_term or 1)
