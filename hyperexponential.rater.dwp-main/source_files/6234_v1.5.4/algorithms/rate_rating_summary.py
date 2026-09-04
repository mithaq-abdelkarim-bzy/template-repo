import hx
import pandas as pd
import numpy as np
from algorithms import parameter_tables_schema as params
from algorithms.rate_utilities import ratio, look_up, df_to_dict, tp_lookup


def rate_rating_summary(hxd):

    scalars = df_to_dict(hx.params.scalar_parameters, "Field", "Parameter")
    benchmark_lr = scalars["Benchmark Net LR"]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # SET UP TECHNICAL PREMIUM PARAMETERS      
    
    # Set rating methodology for case priced vs 
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
    
    bp_class = hxd.cds.standard_fields.benchmark_class # DWP

    # Set up tp params
    che = tp_lookup("che", bp_class, tp_params_df, tp_year)
    var_exp = tp_lookup("var_exp", bp_class, tp_params_df, tp_year)
    inv_inc = tp_lookup("inv_inc", bp_class, tp_params_df, tp_year)
    cost_of_ri = tp_lookup("cost_of_ri", bp_class, tp_params_df, tp_year)
    ri_rec = tp_lookup("ri_rec", bp_class, tp_params_df, tp_year)
    roc = tp_lookup("roc", bp_class, tp_params_df, tp_year)
    fixed_exp_usd = tp_lookup("fixed_exp", bp_class, tp_params_df, tp_year)
    capital_req = tp_lookup("capital_req", bp_class, tp_params_df, tp_year)
    nmp_load = tp_lookup("nmp_load", bp_class, tp_params_df, tp_year)

    # Convert fixed expenses to model currency (default to USD if error)
    ccy = hxd.cds.currencies.source_currency
    fx_rate = look_up(ccy, 'ccy', 'fx_rate', fx_rates_df, if_not_found=1)
    fixed_exp = fixed_exp_usd * fx_rate

    # Calculate technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc*capital_req

    # MIN PREMIUM 
    # Minimum Premium is for $1m limit with no deductible. Scaled using ILF in layer calcs.
    # Many of the params are only defined in the first layer (as the others are for info only). 
    # So using the pol object to call these params
    pol = hxd.cds.layers[0]
    policy_term = hxd.cds.rating_factors.policy_term

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # CALCULATED WEIGHTED EXPECTED LOSS
    
    for count, layer in enumerate(hxd.cds.layers):
        
        # Sum education and non education loss cost
        # Note this is in the policy currency
        # Add non model perils load here 
        el = layer.expected_loss
        el.exposure_rated = (el.education + el.non_education) * (1 + nmp_load)
        
        # Experience rating
        # Note the buring cost includes non modelled perils load
        hxd_er = hxd.cds.experience_rating
        el.experience_weight = exp_weight = hxd_er.credibility_weight or 0
        el.experience_rated = hxd_er.final_burning_cost or 0
        
        # Combine exposure rated and experience weighted
        el.blended = exp_weight * el.experience_rated + (1 - exp_weight) * el.exposure_rated

        # Add NMP Load
        layer.expected_loss_cost_pre_uw_adj = el.blended

        # UW adjustment
        uw_adj = hxd.cds.modifiers.underwriter_adjustment or 0
        layer.expected_loss_cost = layer.expected_loss_cost_pre_uw_adj * (1 + uw_adj)
        layer.uw_adj_impact = uw_adj

        # Filter out main layer in alt scenarios
        layer.label = "Scenario "+str(count)
        layer.filter = True if count > 0 else False

        # Fill the standard kpi view fields
        layer.status_view = layer.status         
        layer.written_line_view = layer.written_line
        layer.section_reference_view = hxd.cds.standard_fields.policy_reference
        layer.brokerage_view = layer.brokerage
        layer.quoted_premium_view = layer.quoted_premium

        if  hxd.cds.standard_fields.is_case_priced:
            layer.bpi_case_priced_view = layer.bpi_case_priced

        # ~~~~~~~~~~~~~~~~~~~~~~~~~
        # CALC TECHNICAL & BENCHMARK PREMIUM

        # If rater priced
        if hxd.cds.standard_fields.is_rater_priced:
                       
            expected_loss = layer.expected_loss_cost
            expected_loss_pre_uw_adj = layer.expected_loss_cost_pre_uw_adj
            
            if expected_loss > 0:
                layer.technical_premium_net = ratio((expected_loss * (1 + che) + fixed_exp), technical_lr)
                layer.technical_premium = ratio(layer.technical_premium_net, (1 - pol.brokerage))

                layer.technical_premium_pre_uw_adj = ratio(
                    ratio((expected_loss_pre_uw_adj * (1 + che) + fixed_exp), technical_lr), 
                    (1 - pol.brokerage)
                )
                layer.benchmark_premium = ratio(
                    ratio(expected_loss, benchmark_lr), 
                    (1-layer.brokerage)
                )
                layer.benchmark_premium_view = layer.benchmark_premium

                layer.benchmark_premium_pre_uw_adj = ratio(
                    ratio(expected_loss_pre_uw_adj, benchmark_lr), 
                    (1-layer.brokerage)
                )
                layer.model_premium = max(
                    layer.technical_premium, 
                    layer.min_premium.education,
                    layer.min_premium.non_education
                )
                if layer.model_premium > layer.technical_premium:
                    layer.min_premium.flag = True
                else:
                    layer.min_premium.flag = False


                # Annualise premium
                layer.benchmark_premium_annualised = (layer.benchmark_premium or 0)/ policy_term
                layer.quoted_premium_annualised = (layer.quoted_premium or 0)/ policy_term

        pass # End loop
        
    # BPI / TPI is only calculated for the first (i.e. main) layer so taken these calcs out of the loop
    if pol.quoted_premium and hxd.cds.standard_fields.is_rater_priced:
        pol.bpi = pol.quoted_premium / pol.benchmark_premium if pol.benchmark_premium else None
        pol.tpi = pol.quoted_premium / pol.technical_premium if pol.technical_premium else None

        pol.bpi_pre_uw_adj = pol.quoted_premium / pol.benchmark_premium_pre_uw_adj if pol.benchmark_premium_pre_uw_adj else None
        pol.tpi_pre_uw_adj = pol.quoted_premium / pol.technical_premium_pre_uw_adj if pol.technical_premium_pre_uw_adj else None
    
        quoted_premium_net = pol.quoted_premium * (1-pol.brokerage)
        pol.pflr = ratio(pol.expected_loss_cost, (quoted_premium_net or 1))
        pol.pflr_pre_uw_adj = ratio(pol.expected_loss_cost_pre_uw_adj,(quoted_premium_net or 1) )

        pol.roc = ratio(
            1 - pol.pflr - var_exp + inv_inc - (cost_of_ri-ri_rec) - ratio(fixed_exp + expected_loss*che, quoted_premium_net),
            capital_req
        )


    # For case pricing only
    if hxd.cds.standard_fields.is_case_priced and pol.quoted_premium and pol.bpi_case_priced:
        pol.bpi = pol.bpi_case_priced
        pol.benchmark_premium = ratio(pol.quoted_premium, pol.bpi)
        pol.benchmark_premium_view = pol.benchmark_premium
        pol.expected_loss_cost = pol.benchmark_premium * benchmark_lr * (1-pol.brokerage)
        
        pol.technical_premium_net = ratio((pol.expected_loss_cost*(1+che) + fixed_exp), technical_lr)
        pol.technical_premium = ratio(pol.technical_premium_net, (1-pol.brokerage))
                    
        pol.tpi = ratio(pol.quoted_premium, pol.technical_premium)

        pol.pflr = ratio(benchmark_lr, pol.bpi)
        pol.tpi_pre_uw_adj = pol.tpi
        pol.technical_premium_pre_uw_adj = pol.technical_premium
        
        quoted_premium_net = pol.quoted_premium * (1-pol.brokerage)

        pol.roc = ratio(
            1 - pol.pflr - var_exp + inv_inc - (cost_of_ri-ri_rec) - ratio(fixed_exp + pol.expected_loss_cost*che, quoted_premium_net),
            capital_req
        )
        
        # Annualise premium
        pol.benchmark_premium_annualised = (pol.benchmark_premium or 0)/ policy_term
        pol.quoted_premium_annualised = (pol.quoted_premium or 0)/ policy_term


    # Flag to check if uw rationale should be required
    premium_beaz_share = (pol.quoted_premium or 0) * (pol.written_line or 0)
    rationale_threshold = scalars["UW Rationale Threshold"] * fx_rate
    if premium_beaz_share > rationale_threshold:
        hxd.cds.uw_rationale.is_rationale_required = True
     

