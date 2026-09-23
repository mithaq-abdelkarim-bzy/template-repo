import hx
import pandas as pd
import numpy as np
from algorithms import parameter_tables_schema as params
from algorithms.rate_utilities import ratio, look_up, _perform_lookup
from algorithms.rate_constants import benchmark_lr

def tpi_calculation(hxd, layer_coverage, calc_option,model_brokerage, tp_parameters ):
    che = tp_parameters["che"]
    fixed_exp_usd = tp_parameters["fixed_exp_usd"]
    technical_lr = tp_parameters["technical_lr"]
    xe_rate = tp_parameters["xe_rate"]
    var_exp = tp_parameters["var_exp"]
    inv_inc = tp_parameters["inv_inc"]
    cost_of_ri = tp_parameters["cost_of_ri"] 
    ri_rec = tp_parameters["ri_rec"]
    capital_req = tp_parameters["capital_req"]
    # nmp_load = tp_parameters["nmp_load"]

    layer_cover = layer_coverage

    expected_loss_preuwadj_usd = layer_cover.expected_loss_cost_pre_uw_adj_usd
    expected_loss_postuwadj_usd = layer_cover.expected_loss_cost_usd
    expected_loss_before_minimum_prem_usd = layer_cover.expected_loss_cost_before_minimum_premium_usd

    if layer_cover.brokerage == None: 
        brokerage = 0.0
    else:
        brokerage = layer_cover.brokerage

    # if layer_cover.brokerage is not None:
    #     if layer_cover.brokerage < 0 or layer_coverage.brokerage > 1:
    #         hx.errors.validation("Pricing: Brokerage Cannot be Negative or Excess 100%")

    #Gross and Net technical premium AFTER UW adj
    #USD currency
    if(calc_option == 1):
        layer_cover.technical_premium_usd = ratio((ratio(expected_loss_postuwadj_usd, (1-brokerage))*(1+che) + fixed_exp_usd), technical_lr)
        layer_cover.technical_premium_net_usd = layer_cover.technical_premium_usd * (1-brokerage)
    elif(calc_option == 2):
        layer_cover.technical_premium_net_usd = ratio(expected_loss_postuwadj_usd*(1+che)+fixed_exp_usd,technical_lr )
        layer_cover.technical_premium_usd = ratio(layer_cover.technical_premium_net_usd ,(1-brokerage) )
        layer_cover.technical_premium_net_before_minimum_prem_usd = ratio(expected_loss_before_minimum_prem_usd*(1+che)+fixed_exp_usd,technical_lr )
        layer_cover.technical_premium_before_minimum_prem_usd = ratio(layer_cover.technical_premium_net_before_minimum_prem_usd ,(1-brokerage) )
    elif(calc_option == 3):
        layer_cover.technical_premium_usd = ratio(ratio((ratio(expected_loss_postuwadj_usd*(1-model_brokerage), (1-brokerage))*(1+che) + fixed_exp_usd), technical_lr), (1-model_brokerage))
        layer_cover.technical_premium_net_usd = layer_cover.technical_premium_usd * (1-brokerage)
    #Local currency
    layer_cover.technical_premium = layer_cover.technical_premium_usd * xe_rate
    layer_cover.technical_premium_net = layer_cover.technical_premium_net_usd * xe_rate

    #Gross and Net technical premium BEFORE UW adj
    # USD currency
    if(calc_option == 1):
        layer_cover.technical_premium_pre_uw_adj_usd = ratio((ratio(expected_loss_preuwadj_usd, (1-brokerage))*(1+che) + fixed_exp_usd), technical_lr)
        layer_cover.technical_premium_net_pre_uw_adj_usd = layer_cover.technical_premium_pre_uw_adj_usd * (1-brokerage)
    elif(calc_option == 2):
        layer_cover.technical_premium_net_pre_uw_adj_usd = ratio(expected_loss_preuwadj_usd*(1+che)+fixed_exp_usd,technical_lr )
        layer_cover.technical_premium_pre_uw_adj_usd = ratio(layer_cover.technical_premium_net_pre_uw_adj_usd ,(1-brokerage) )
    elif(calc_option == 3):
        layer_cover.technical_premium_pre_uw_adj_usd= ratio(ratio((ratio(expected_loss_preuwadj_usd*(1-model_brokerage), (1-brokerage))*(1+che) + fixed_exp_usd), technical_lr), (1-model_brokerage))
        layer_cover.technical_premium_net_pre_uw_adj_usd = layer_cover.technical_premium_pre_uw_adj_usd * (1-brokerage)

    # Local currency
    layer_cover.technical_premium_pre_uw_adj = layer_cover.technical_premium_pre_uw_adj_usd * xe_rate
    layer_cover.technical_premium_net_pre_uw_adj = layer_cover.technical_premium_net_pre_uw_adj_usd * xe_rate
    #Before minimum premium
    layer_cover.technical_premium_before_minimum_prem = layer_coverage.technical_premium_before_minimum_prem_usd * xe_rate
    layer_cover.technical_premium_net_before_minimum_prem = layer_cover.technical_premium_net_before_minimum_prem_usd * xe_rate
    

    #Gross and Net benchmark premium AFTER UW adj
    #USD
    # Calc_option 1 is for E&O. Use Pre UW adjustment for Benchmark Premium Calc

    if(calc_option == 1):
        layer_cover.benchmark_premium_net_usd = ratio(expected_loss_preuwadj_usd, benchmark_lr)
    else:
        layer_cover.benchmark_premium_net_usd = ratio(expected_loss_postuwadj_usd, benchmark_lr)
    layer_cover.benchmark_premium_usd = ratio(layer_cover.benchmark_premium_net_usd, (1-brokerage))
    #Local currency
    layer_cover.benchmark_premium_net = layer_cover.benchmark_premium_net_usd * xe_rate
    layer_cover.benchmark_premium = layer_cover.benchmark_premium_usd * xe_rate

    #Gross and Net benchmark premium BEFORE UW adj
    #USD
    layer_cover.benchmark_premium_net_pre_uw_adj_usd = ratio(expected_loss_preuwadj_usd, benchmark_lr)    
    layer_cover.benchmark_premium_pre_uw_adj_usd = ratio(layer_cover.benchmark_premium_net_pre_uw_adj_usd, (1-brokerage)) 
    #Local currency
    layer_cover.benchmark_premium_net_pre_uw_adj = layer_cover.benchmark_premium_net_pre_uw_adj_usd * xe_rate
    layer_cover.benchmark_premium_pre_uw_adj = layer_cover.benchmark_premium_pre_uw_adj_usd * xe_rate
    
    if expected_loss_preuwadj_usd == 0:
        layer_cover.uw_adj_impact = 1
    else:
        layer_cover.uw_adj_impact = ratio(expected_loss_postuwadj_usd, expected_loss_preuwadj_usd)

    # #model premium -> assume to be the same as TP
    # layer_cover.model_premium = layer_cover.technical_premium 
    if  layer_cover.quoted_premium:
    #Price adequacy ratio
        layer_cover.bpi = ratio(layer_cover.quoted_premium, layer_cover.benchmark_premium)
        layer_cover.bpi_pre_uw_adj = ratio(layer_cover.quoted_premium,layer_cover.benchmark_premium_pre_uw_adj )
        layer_cover.tpi = ratio(layer_cover.quoted_premium, layer_cover.technical_premium )
        layer_cover.tpi_pre_uw_adj = ratio(layer_cover.quoted_premium, layer_cover.technical_premium_pre_uw_adj)

        #Price adequacy ratio
        layer_cover.bpi = ratio(layer_cover.quoted_premium, layer_cover.benchmark_premium)
        layer_cover.bpi_pre_uw_adj = ratio(layer_cover.quoted_premium,layer_cover.benchmark_premium_pre_uw_adj )
        layer_cover.tpi = ratio(layer_cover.quoted_premium, layer_cover.technical_premium )
        layer_cover.tpi_pre_uw_adj = ratio(layer_cover.quoted_premium, layer_cover.technical_premium_pre_uw_adj)
        # use usd currency to cacluate the ratio
        quoted_premium_net_usd = layer_cover.quoted_premium * (1-brokerage) / xe_rate
        layer_cover.pflr = ratio(expected_loss_postuwadj_usd, (quoted_premium_net_usd or 1))
        layer_cover.pflr_pre_uw_adj = ratio(expected_loss_preuwadj_usd, (quoted_premium_net_usd or 1))

        # TODO: add Att and Cat expected loss to common data schema?
        # layer.pflr_att = ratio(layer.expected_loss_cost_att, (quoted_premium_net or 1))
        # layer.pflr_cat = ratio(layer.expected_loss_cost_cat, (quoted_premium_net or 1))

        layer_cover.pflr_att = layer_cover.pflr
        layer_cover.pflr_cat = 0

        layer_cover.roc = ratio(
            1 - layer_cover.pflr - var_exp + inv_inc - (cost_of_ri-ri_rec) - ratio(fixed_exp_usd + expected_loss_postuwadj_usd*che, quoted_premium_net_usd),
            capital_req
        )


def tpi_summary(hxd):

    # Set rating methodology
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == "Case Priced"
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == "Rater"
    constants_params = hx.params.table_constants


    # Pull in technical premium parameters and fx rates from user library 
    #tp_params_df = params.tp_parameters.df()
    tp_params_df = hx.params.table_tp_parameters
    #fx_rates_df = params.fx_rates.df()
    fx_rates_df = hx.params.table_fx_rates
    model_brokerage = constants_params[constants_params["name"] == "model_brokerage"]["factor"].iloc[0]
    model_brokerage_gl = constants_params[constants_params["name"] == "model_brokerage_gl"]["factor"].iloc[0]

    # Placeholder variables: update with correct benchmark class and modelled expected loss, this might need to 
    # be linked if a rater can write to more than one class. May link to benchmark class in risk information.
    # bp_class = hxd.cds.standard_fields.benchmark_class
    bp_class = 'International Specialty Programmes' #PLACEHOLDER
        
    # Set up tp params
    filtered_tp_params = tp_params_df[tp_params_df['business_plan_class'] == bp_class]
    che = filtered_tp_params['che'].iloc[0]
    var_exp = filtered_tp_params['var_exp'].iloc[0]
    inv_inc = filtered_tp_params['inv_inc'].iloc[0]
    cost_of_ri = filtered_tp_params['cost_of_ri'].iloc[0]
    ri_rec = filtered_tp_params['ri_rec'].iloc[0]
    roc = filtered_tp_params['roc'].iloc[0]
    fixed_exp_usd = filtered_tp_params['fixed_exp'].iloc[0]
    capital_req = filtered_tp_params['capital_req'].iloc[0]
    nmp_load = filtered_tp_params['nmp_load'].iloc[0]

    # Convert fixed expenses to model currency (default to USD if error)
    ccy = hxd.cds.currencies.source_currency
    #ccy = "EUR"
    xe_rate = look_up(ccy, 'ccy', 'fx_rate', fx_rates_df, if_not_found=1)
    fixed_exp = fixed_exp_usd * look_up(ccy, 'ccy', 'fx_rate', fx_rates_df, if_not_found=1)
    #xe_rate = 0.904521

    # Calculate technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc*capital_req

    tp_parameters = {"che": che, "fixed_exp_usd": fixed_exp_usd,"technical_lr":technical_lr, "xe_rate" : xe_rate, "var_exp" : var_exp,
    "inv_inc" : inv_inc,"cost_of_ri" : cost_of_ri,"ri_rec" : ri_rec, "capital_req" : capital_req, "nmp_load": nmp_load}




    for layer in hxd.cds.layers:
        # If rater priced
        ######################################################################################
        #                   E&O Coverage
        ######################################################################################
        if hxd.cds.standard_fields.is_rater_priced and layer.coverages.eo.limit and hxd.cds.eo_coverage_selection:
            tpi_calculation(hxd, layer_coverage = layer.coverages.eo, calc_option = 2, model_brokerage = model_brokerage, tp_parameters = tp_parameters)
            
        ######################################################################################
        #                   Media Tech Coverage
        ######################################################################################  
        if hxd.cds.standard_fields.is_rater_priced and layer.coverages.mediatech.limit and hxd.cds.mediatech_coverage_selection:
            tpi_calculation(hxd, layer_coverage = layer.coverages.mediatech, calc_option = 2, model_brokerage = model_brokerage, tp_parameters = tp_parameters)              

        ######################################################################################
        #                   GL Coverage
        ######################################################################################  
        
        if hxd.cds.standard_fields.is_rater_priced and layer.coverages.gl.limit and hxd.cds.gl_coverage_selection:
            tpi_calculation(hxd, layer_coverage = layer.coverages.gl, calc_option = 2, model_brokerage = model_brokerage_gl, tp_parameters = tp_parameters)


        ######################################################################################
        #     Summarise the layer benchmark premium and quoted premium for None-Case pricing
        ######################################################################################      

        #summrise benchmark premium
        eo_benchmark_premium = 0
        mediatech_benchmark_premium = 0
        gl_benchmark_premium = 0
        layer_benchmark_premium = 0

        eo_benchmark_premium = getattr(layer.coverages.eo, "benchmark_premium")
        mediatech_benchmark_premium = getattr(layer.coverages.mediatech, "benchmark_premium")
        gl_benchmark_premium = getattr(layer.coverages.gl, "benchmark_premium")

        if eo_benchmark_premium == None:
            eo_benchmark_premium = 0
        if mediatech_benchmark_premium == None:
            mediatech_benchmark_premium = 0
        if gl_benchmark_premium == None:
            gl_benchmark_premium = 0
        
        layer_benchmark_premium = eo_benchmark_premium  + mediatech_benchmark_premium  +  gl_benchmark_premium
        setattr(layer, "benchmark_premium", layer_benchmark_premium)

        #summarise quoted premium
        eo_quoted_premium = 0
        mediatech_quoted_premium = 0
        gl_quoted_premium = 0
        layer_quoted_premium = 0

        eo_quoted_premium = getattr(layer.coverages.eo, "quoted_premium")
        mediatech_quoted_premium = getattr(layer.coverages.mediatech, "quoted_premium")
        gl_quoted_premium = getattr(layer.coverages.gl, "quoted_premium")

        if eo_quoted_premium == None:
            eo_quoted_premium = 0
        if mediatech_quoted_premium == None:
            mediatech_quoted_premium = 0
        if gl_quoted_premium == None:
            gl_quoted_premium = 0
        
        layer_quoted_premium = eo_quoted_premium  + mediatech_quoted_premium  +  gl_quoted_premium
        setattr(layer, "quoted_premium", layer_quoted_premium)
        
        # BPI Case priced is moved to be coverage based, instead of layer based
        bpi_case_priced = None
        if hxd.cds.eo_coverage_selection:
            bpi_case_priced = getattr(layer.coverages.eo, "bpi_case_priced")
        if hxd.cds.mediatech_coverage_selection:
            bpi_case_priced = getattr(layer.coverages.mediatech, "bpi_case_priced")
        if hxd.cds.gl_coverage_selection:
            bpi_case_priced = getattr(layer.coverages.gl, "bpi_case_priced")
        
        layer.bpi = bpi_case_priced
        
        ############################################################################################
        # For case pricing only
        ###########################################################################################
        if hxd.cds.standard_fields.is_case_priced and layer.quoted_premium and bpi_case_priced:
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

    pass