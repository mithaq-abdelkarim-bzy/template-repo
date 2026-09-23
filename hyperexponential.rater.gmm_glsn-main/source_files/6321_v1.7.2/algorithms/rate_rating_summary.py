import hx
import pandas as pd
import numpy as np
import math as math
import re
from algorithms.rate_utilities import ratio
import algorithms.rate_utilities as utils
from operator import itemgetter
from algorithms import parameter_tables_schema as params

def rate_rating_summary(hxd):
    cds = hxd.cds

    ########################################################
    # Global inputs
    ########################################################

    # Rater or case priced flag
    if hxd.cds.standard_fields.rating_methodology == "Rater":
        hxd.cds.standard_fields.is_rater_priced = True
        hxd.cds.standard_fields.is_case_priced = False
    else:
        hxd.cds.standard_fields.is_rater_priced = False
        hxd.cds.standard_fields.is_case_priced = True

    # Currency factor
    
    # FX rate for currency conversion - from user library
    fx_rates = params.fx_rates.df()
    ccy = cds.currencies.source_currency
    fx_rate = utils.look_up(ccy, 'ccy', 'fx_rate', fx_rates, if_not_found=1) # default to USD if error
    currency_factor = 1 / fx_rate

    #  US/International Risk
    us_international = cds.rating_factors.us_international_choice_of_law.us_international

    # Selected option
    selected_option = int(cds.option_selected[-1])

    # Set layer labels
    for index, layer in enumerate(hxd.cds.layers):        

        #Set the label for each layer:
        if index == 0:
            layer.layer_label = "Retention"
        elif index == 1:
            layer.layer_label = "Primary Layer"
        else:
            layer.layer_label = f"Excess {index-1}"
    
    ########################################################
    # GMM
    ########################################################
    if cds.gmm_masking == True:        

        # Calculating benchmark premium and BPIs    
        priced_to_net_loss_ratio = hx.params.table_gmm_priced_to_net_lr.loc[:,"loss_ratio"].iloc[0]
        benchmark_loss_ratio = hx.params.table_benchmark_lr.loc[:,"loss_ratio"].iloc[0]


        ###################
        # IR edit 22/12 ---

        # Pull in technical premium parameters from user library 
        tp_params = params.tp_parameters.df()

        # To stop the model erroring if the inception year defaults to a year not in the TP data
        yoa = hxd.hx_core.inception_date.year
        tp_year = yoa if yoa in tp_params["year"].values else tp_params["year"].max()

        # ML edit 07/09/26 ---
        # Business parameters --------       
        # Pull the right business class parameters
        if (us_international == "International"):
            if (tp_year <= 2025):
                bp_class = "Intl Misc Med (London)"
            else:
                bp_class = "Intl Misc Med & Life Sciences"
        else:
            bp_class = "US Misc Med"  
        # End of ML edit --- 

        tp_lookup_bool = (tp_params['business_plan_class'] == bp_class) & (tp_params['year'] == tp_year)
        tp_params_df = tp_params[tp_lookup_bool]

        # end of IR edit 22/12 ---
        #############   

        che = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['che'].iloc[0]
        var_exp = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['var_exp'].iloc[0]
        inv_inc = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['inv_inc'].iloc[0]
        cost_of_ri = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['cost_of_ri'].iloc[0]
        ri_rec = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['ri_rec'].iloc[0]
        roc = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['roc'].iloc[0]
        fixed_exp_usd = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['fixed_exp'].iloc[0]
        capital_req = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['capital_req'].iloc[0]
        nmp_load = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['nmp_load'].iloc[0]               
        cyber_brokerage = cds.cyber_options[selected_option - 1].brokerage if cds.cyber_options[selected_option - 1].brokerage is not None else 0

        # Inputs to each layer ----------------
        bound_validation = []
        for index, layer in enumerate(hxd.cds.layers):                    
            if index == 0:
                # limit
                if (cds.rating_factors.pricing.professional_liability.include_primary == True):
                    layer.limit = cds.options[selected_option - 1].coverages.professional_liability.retention
                else:
                    layer.limit = cds.options[selected_option - 1].coverages.tech_eo_products_media.retention
                                         
                # aggregate limit
                layer.aggregate_limit = None
                # brokerage, model premium, benchmark premium
                layer.brokerage = None
                layer.model_premium = None
                layer.benchmark_premium = None 
                layer.show_row = False              
            elif index == 1:
                # limit
                if (cds.rating_factors.pricing.professional_liability.include_primary == True):
                    layer.limit = cds.options[selected_option - 1].coverages.professional_liability.per_claim_limit
                # aggregate limit
                    layer.aggregate_limit = cds.options[selected_option - 1].coverages.professional_liability.aggregate_limit
                else:
                    layer.limit = cds.options[selected_option - 1].coverages.tech_eo_products_media.per_claim_limit
                    layer.aggregate_limit = cds.options[selected_option - 1].coverages.tech_eo_products_media.aggregate_limit

                # brokerage, model premium, benchmark premium
                layer.brokerage = cds.options[selected_option - 1].brokerage_primary
                if cds.options[selected_option - 1].model_premium_primary < cds.options[selected_option - 1].minimum_premium_primary:
                    # Apportioning out the non-cyber and cyber parts of the loss cost where minimum bites
                    cyber_premium_pre_min = cds.options[selected_option - 1].cyber_premium_primary * (1 + nmp_load) if cds.options[selected_option - 1].cyber_premium_primary is not None else 0   
                    min_premium_primary = cds.options[selected_option - 1].minimum_premium_primary
                    model_premium_exc_cyber_pre_min = cds.options[selected_option - 1].model_premium_primary - cyber_premium_pre_min  

                    # Now express the model premium and cyber premium based on their proportion of the minimum premium
                    if cds.options[selected_option - 1].model_premium_primary is not None and cds.options[selected_option - 1].model_premium_primary != 0 : 
                        model_premium_exc_cyber = min_premium_primary * model_premium_exc_cyber_pre_min / cds.options[selected_option - 1].model_premium_primary 
                        cyber_premium = min_premium_primary * cyber_premium_pre_min / cds.options[selected_option - 1].model_premium_primary 
                    else: 
                        model_premium_exc_cyber = 0
                        cyber_premium = 0
                    layer.model_premium = cds.options[selected_option - 1].minimum_premium_primary

                else:
                    layer.model_premium = cds.options[selected_option - 1].model_premium_primary
                    cyber_premium = cds.options[selected_option - 1].cyber_premium_primary * (1 + nmp_load) if cds.options[selected_option - 1].cyber_premium_primary is not None else 0   
                    model_premium_exc_cyber = layer.model_premium - cyber_premium 

                layer.quoted_premium = cds.options[selected_option - 1].quoted_premium_primary
                layer.show_row = True
     
            else:
                # limit
                layer.limit = getattr(cds.options[selected_option - 1], f"per_claim_limit_{index - 1}_excess")
                # aggregate limit
                layer.aggregate_limit = getattr(cds.options[selected_option - 1], f"aggregate_limit_{index-1}_excess")
                # brokerage, model premium, benchmark premium
                layer.brokerage = getattr(cds.options[selected_option - 1], f"brokerage_{index-1}_excess")
                if getattr(cds.options[selected_option - 1], f"model_premium_{index-1}_excess") < getattr(cds.options[selected_option - 1], f"minimum_premium_{index-1}_excess"):
                    # Apportioning out the non-cyber and cyber parts of the loss cost where minimum bites
                    cyber_premium_pre_min = cds.rating_factors.cyber.include_excess * getattr(cds.cyber_options[selected_option - 1],f"model_premium_third_party_{index-1}_excess") * (1 + nmp_load) if getattr(cds.cyber_options[selected_option - 1],f"model_premium_third_party_{index-1}_excess") is not None else 0 
                    min_premium = getattr(cds.options[selected_option - 1], f"minimum_premium_{index-1}_excess")
                    model_premium_exc_cyber_pre_min = max(getattr(cds.options[selected_option - 1], f"model_premium_{index-1}_excess") - cyber_premium_pre_min, 0)

                    # Now express the model premium and cyber premium based on their proportion of the minimum premium
                    if getattr(cds.options[selected_option - 1], f"model_premium_{index-1}_excess") > 0 : 
                        model_premium_exc_cyber = min_premium * model_premium_exc_cyber_pre_min / getattr(cds.options[selected_option - 1], f"model_premium_{index-1}_excess")
                        cyber_premium = min_premium * cyber_premium_pre_min / getattr(cds.options[selected_option - 1], f"model_premium_{index-1}_excess") 
                    else: 
                        model_premium_exc_cyber = 0
                        cyber_premium = 0

                    layer.model_premium = getattr(cds.options[selected_option - 1], f"minimum_premium_{index-1}_excess")
                else:
                    layer.model_premium = getattr(cds.options[selected_option - 1], f"model_premium_{index-1}_excess")
                    cyber_premium = getattr(cds.cyber_options[selected_option - 1],f"model_premium_third_party_{index-1}_excess") * (1 + nmp_load) if getattr(cds.cyber_options[selected_option - 1],f"model_premium_third_party_{index-1}_excess") is not None else 0   
                    model_premium_exc_cyber = max(layer.model_premium - cyber_premium, 0)

                if getattr(cds,f"add_excess_{index-1}") : 
                    layer.show_row = True
                else: 
                    layer.show_row = False    

                layer.quoted_premium = getattr(cds.options[selected_option - 1], f"quoted_premium_{index-1}_excess")

            # Calculations --------------------
            # Retention layer
            if index == 0:
                layer.brokerage = None     
                layer.quoted_rate = None
                layer.bound_rate = None
                layer.benchmark_premium = None
                layer.technical_premium_net = None
                layer.technical_premium = None
                layer.tpi = None
                layer.net_written_premium = None
            # Primary and Excess layers
            else:
                # brokerage - if none, set to zero
                if layer.brokerage == None:
                    layer.brokerage = 0
                    
                # Quoted rate
                layer.quoted_rate = (layer.quoted_premium / (cds.exposure.aggregate.revenue / 1000)) if cds.exposure.aggregate.revenue and layer.quoted_premium else 0            

                # Bound rate
                layer.bound_rate = (layer.bound_premium / (cds.exposure.aggregate.revenue / 1000)) if cds.exposure.aggregate.revenue and layer.bound_premium else 0  

                # Benchmark premium
                if ((hxd.cds.standard_fields.is_case_priced == True) and (layer.bpi_case_priced > 0) and (layer.bound_premium is not None)):
                    layer.benchmark_premium = ratio(layer.bound_premium, layer.bpi_case_priced) # IR edit
                else:
                    layer.benchmark_premium = layer.model_premium * (priced_to_net_loss_ratio / benchmark_loss_ratio) if benchmark_loss_ratio else 0

                # BPI
                if layer.benchmark_premium == 0:
                    layer.bpi = None
                elif layer.bound_premium != None:
                    layer.bpi = layer.bound_premium / layer.benchmark_premium
                elif layer.quoted_premium != None:
                    layer.bpi = layer.quoted_premium / layer.benchmark_premium
                else:
                    layer.bpi = 0                
                    
                # Net written premium
                if ((hxd.cds.standard_fields.is_case_priced == True) and (layer.bound_premium and layer.brokerage_case_priced != None)):
                    layer.net_written_premium = layer.bound_premium * (1 - layer.brokerage_case_priced) # IR edit
                elif layer.bound_premium != None:                 
                    layer.net_written_premium = layer.bound_premium * (1 - layer.brokerage)                    
                elif layer.quoted_premium != None:
                    layer.net_written_premium = layer.quoted_premium * (1 - layer.brokerage)
                else:
                    layer.net_written_premium = 0

                # Net technical premium
                # note expected losses already loads up for nmp
                denominator = (1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc * capital_req)
                if (hxd.cds.standard_fields.is_case_priced == True) and (denominator != 0): #and (layer.benchmark_premium and layer.brokerage_case_priced is not None): # IR edit
                    if layer.brokerage_case_priced is None:
                        brokerage_case_priced = 0
                    else:
                        brokerage_case_priced = layer.brokerage_case_priced
                    layer.technical_premium_net = ratio(((layer.benchmark_premium * benchmark_loss_ratio * (1-brokerage_case_priced)) * (1+che) + fixed_exp_usd), denominator)
                    layer.technical_premium = ratio(layer.technical_premium_net, (1-brokerage_case_priced))
                    layer.tpi = ratio(layer.bound_premium, layer.technical_premium) if layer.bound_premium is not None else 0
                else:
                    # denominator = (1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc * capital_req)
                    if denominator and layer.benchmark_premium != 0:
                        expect_loss_cost_non_cyber = model_premium_exc_cyber * priced_to_net_loss_ratio * ( 1 - layer.brokerage)
                        expect_loss_cost_cyber = cyber_premium  * priced_to_net_loss_ratio * ( 1 - cyber_brokerage)
                        tech_prem_net = ((expect_loss_cost_non_cyber + expect_loss_cost_cyber)* (1 + che) + fixed_exp_usd / currency_factor) / denominator
                        weighted_cyber_and_pricing_brokerage = (expect_loss_cost_non_cyber * layer.brokerage + expect_loss_cost_cyber * cyber_brokerage) / (expect_loss_cost_non_cyber + expect_loss_cost_cyber) if (expect_loss_cost_non_cyber + expect_loss_cost_cyber) > 0 else 0
                        # Old Method
                        layer.technical_premium_net = (layer.benchmark_premium * (1- layer.brokerage) * 0.7 * (1 + che) + fixed_exp_usd / currency_factor) / denominator
                    else:
                        layer.technical_premium_net = 0
                        weighted_cyber_and_pricing_brokerage = 0
                        tech_prem_net = 0
                    # Gross technical premium
                    # layer.technical_premium = layer.technical_premium_net / (1- layer.brokerage) if (1- layer.brokerage) else 0
                    layer.technical_premium = tech_prem_net / (1- weighted_cyber_and_pricing_brokerage) if (1- weighted_cyber_and_pricing_brokerage) else 0

                    # TPI
                    if layer.bound_premium != None and layer.technical_premium != 0:
                        layer.tpi = layer.bound_premium / layer.technical_premium
                    elif layer.quoted_premium != None and layer.technical_premium != 0:
                        layer.tpi = layer.quoted_premium / layer.technical_premium
                    else:
                        layer.tpi = None  

            # Section reference valdations 
            if layer.section_reference is not None and re.search(r'[£$%&,@!*.<>\?/\|~#}{\[\]]', layer.section_reference) :
                hx.errors.validation("Invalid characters entered in layer Policy Reference")
            if layer.section_reference is not None and layer.status != "Bound" :    
                hx.errors.validation("Only Bound risks should have a Policy Reference")
            if layer.section_reference is not None :
                if len(layer.section_reference) > 20:    
                    hx.errors.validation("Policy Reference cannot exceed 20 characters")
            if layer.section_reference is not None and layer.section_reference == layer.rate_change.expiring_policy_info.expiring_section_reference:
                hx.errors.validation("Current Policy Reference is equal to Expiring Policy Reference. Please update Policy Reference.")

            if layer.status == "Bound" :
                bound_validation.append(True)
            else: 
                bound_validation.append(False)

            if layer.section_reference is None and layer.status == "Bound" :
                hx.errors.validation("Please enter a Policy Reference for Bound Risks")
                
        # This is just for the view - setting the retention (which is in a different structure) equal to the 0 layer in the layers node 
        cds.rating_factors.retention.limit = cds.layers[0].limit
        
        # bound_validation_check = sum(bound_validation)
        # if bound_validation_check < 1 :
        #     hx.errors.validation("To finalise a risk, at least one layer must be bound")

    ########################################################
    # GLSN
    ########################################################
    if cds.glsn_masking == True:        

        # Calculating benchmark premium and BPIs    
        priced_to_net_loss_ratio = hx.params.table_glsn_priced_to_net_lr.loc[:,"loss_ratio"].iloc[0]
        benchmark_loss_ratio = hx.params.table_benchmark_lr.loc[:,"loss_ratio"].iloc[0]

        #####
        # ##############
        # IR edit 22/12 ---

        # Pull in technical premium parameters from user library 
        tp_params = params.tp_parameters.df()

        # To stop the model erroring if the inception year defaults to a year not in the TP data
        yoa = hxd.hx_core.inception_date.year
        tp_year = yoa if yoa in tp_params["year"].values else tp_params["year"].max()

        # ML edit 07/09/26 ---
        # Business parameters --------       
        # Pull the right business class parameters
        if (us_international == "International"):
            if (tp_year <= 2025):
                bp_class = "Intl Misc Med (London)"
            else:
                bp_class = "Intl Misc Med & Life Sciences"
        else:
            bp_class = "US Misc Med"  
        # End of ML edit --- 

        tp_lookup_bool = (tp_params['business_plan_class'] == bp_class) & (tp_params['year'] == tp_year)
        tp_params_df = tp_params[tp_lookup_bool]

        # end of IR edit 22/12 ---
        #############

        che = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['che'].iloc[0]
        var_exp = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['var_exp'].iloc[0]
        inv_inc = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['inv_inc'].iloc[0]
        cost_of_ri = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['cost_of_ri'].iloc[0]
        ri_rec = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['ri_rec'].iloc[0]
        roc = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['roc'].iloc[0]
        fixed_exp_usd = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['fixed_exp'].iloc[0]
        capital_req = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['capital_req'].iloc[0]
        nmp_load = tp_params_df[tp_params_df['business_plan_class'] == bp_class]['nmp_load'].iloc[0]  
        cyber_brokerage = cds.cyber_options[selected_option - 1].brokerage if cds.cyber_options[selected_option - 1].brokerage is not None else 0             

        # Inputs to each layer ----------------
        override_label = cds.override_terms_to_display
        override_terms_to_display = hx.params.table_glsn_override_terms[hx.params.table_glsn_override_terms["override_label"] == override_label]["override_name"].iloc[0]

        
        bound_validation = []
        for index, layer in enumerate(hxd.cds.layers):                    
            if index == 0:
                # limit
                if override_terms_to_display == "all":
                    if (cds.rating_factors.pricing.product_liability.significant_coverage == "Significant"):
                        layer.limit = cds.options[selected_option - 1].coverages.product_liability.retention
                    elif (cds.rating_factors.pricing.eo.significant_coverage == "Significant"):
                        layer.limit = cds.options[selected_option - 1].coverages.eo.retention
                    elif (cds.rating_factors.pricing.healthcare_professional_liability.significant_coverage == "Significant"):
                        layer.limit = cds.options[selected_option - 1].coverages.healthcare_professional_liability.retention
                    else:
                        layer.limit = 0
                else:  
                    layer.limit = getattr(cds.options[selected_option - 1].coverages,override_terms_to_display).retention          

                # aggregate_limit
                layer.aggregate_limit = None
                # brokerage, model premium, quoted premium
                layer.brokerage = None
                layer.model_premium = None
                layer.benchmark_premium = None   
                layer.show_row = False              
            elif index == 1:
                # limit
                if override_terms_to_display == "all":
                    if (cds.rating_factors.pricing.product_liability.significant_coverage == "Significant"):
                        layer.limit = cds.options[selected_option - 1].coverages.product_liability.per_claim_limit
                    elif (cds.rating_factors.pricing.eo.significant_coverage == "Significant"):
                        layer.limit = cds.options[selected_option - 1].coverages.eo.per_claim_limit
                    elif (cds.rating_factors.pricing.healthcare_professional_liability.significant_coverage == "Significant"):
                        layer.limit = cds.options[selected_option - 1].coverages.healthcare_professional_liability.per_claim_limit
                    else:
                        layer.limit = 0
                else:
                    layer.limit = getattr(cds.options[selected_option - 1].coverages,override_terms_to_display).per_claim_limit
                                                                       
                # aggregate limit
                if override_terms_to_display == "all":
                    if (cds.rating_factors.pricing.product_liability.significant_coverage == "Significant"):
                        layer.aggregate_limit = cds.options[selected_option - 1].coverages.product_liability.aggregate_limit
                    elif (cds.rating_factors.pricing.eo.significant_coverage == "Significant"):
                        layer.aggregate_limit = cds.options[selected_option - 1].coverages.eo.aggregate_limit
                    elif (cds.rating_factors.pricing.healthcare_professional_liability.significant_coverage == "Significant"):
                        layer.aggregate_limit = cds.options[selected_option - 1].coverages.healthcare_professional_liability.aggregate_limit
                    else:
                        layer.aggregate_limit = 0    
                else:
                    layer.aggregate_limit = getattr(cds.options[selected_option - 1].coverages,override_terms_to_display).aggregate_limit
                                                  
                # brokerage, model premium, quoted premium
                layer.brokerage = cds.options[selected_option - 1].brokerage_primary
                if cds.options[selected_option - 1].model_premium_primary < cds.options[selected_option - 1].minimum_premium_primary:
                    # Apportioning out the non-cyber and cyber parts of the loss cost where minimum bites
                    cyber_premium_pre_min = cds.options[selected_option - 1].cyber_premium_primary * (1 + nmp_load) if cds.options[selected_option - 1].cyber_premium_primary is not None else 0   
                    min_premium_primary = cds.options[selected_option - 1].minimum_premium_primary
                    model_premium_exc_cyber_pre_min = cds.options[selected_option - 1].model_premium_primary - cyber_premium_pre_min  

                    # Now express the model premium and cyber premium based on their proportion of the minimum premium
                    if cds.options[selected_option - 1].model_premium_primary is not None and cds.options[selected_option - 1].model_premium_primary != 0 : 
                        model_premium_exc_cyber = min_premium_primary * model_premium_exc_cyber_pre_min / cds.options[selected_option - 1].model_premium_primary 
                        cyber_premium = min_premium_primary * cyber_premium_pre_min / cds.options[selected_option - 1].model_premium_primary 
                    else: 
                        model_premium_exc_cyber = 0
                        cyber_premium = 0

                    layer.model_premium = cds.options[selected_option - 1].minimum_premium_primary
                
                else:
                    layer.model_premium = cds.options[selected_option - 1].model_premium_primary
                    cyber_premium = cds.options[selected_option - 1].cyber_premium_primary * (1 + nmp_load) if cds.options[selected_option - 1].cyber_premium_primary is not None else 0   
                    model_premium_exc_cyber = layer.model_premium - cyber_premium 

                layer.quoted_premium = cds.options[selected_option - 1].quoted_premium_primary  
                layer.show_row = True

                               
            else:
                # limit                
                layer.limit = getattr(cds.options[selected_option - 1], f"per_claim_limit_{index - 1}_excess")
                # aggregate limit
                layer.aggregate_limit = getattr(cds.options[selected_option - 1], f"aggregate_limit_{index-1}_excess")
                # brokerage, model premium, quoted premium
                layer.brokerage = getattr(cds.options[selected_option - 1], f"brokerage_{index-1}_excess")
                if getattr(cds.options[selected_option - 1], f"model_premium_{index-1}_excess") < getattr(cds.options[selected_option - 1], f"minimum_premium_{index-1}_excess"):
                    # Apportioning out the non-cyber and cyber parts of the loss cost where minimum bites
                    cyber_premium_pre_min = cds.rating_factors.cyber.include_excess * getattr(cds.cyber_options[selected_option - 1],f"model_premium_third_party_{index-1}_excess") * (1 + nmp_load) if getattr(cds.cyber_options[selected_option - 1],f"model_premium_third_party_{index-1}_excess") is not None else 0 
                    min_premium = getattr(cds.options[selected_option - 1], f"minimum_premium_{index-1}_excess")
                    model_premium_exc_cyber_pre_min = max(getattr(cds.options[selected_option - 1], f"model_premium_{index-1}_excess") - cyber_premium_pre_min, 0)

                    # Now express the model premium and cyber premium based on their proportion of the minimum premium
                    if getattr(cds.options[selected_option - 1], f"model_premium_{index-1}_excess") > 0 : 
                        model_premium_exc_cyber = min_premium * model_premium_exc_cyber_pre_min / getattr(cds.options[selected_option - 1], f"model_premium_{index-1}_excess")
                        cyber_premium = min_premium * cyber_premium_pre_min / getattr(cds.options[selected_option - 1], f"model_premium_{index-1}_excess") 
                    else: 
                        model_premium_exc_cyber = 0
                        cyber_premium = 0

                    layer.model_premium = getattr(cds.options[selected_option - 1], f"minimum_premium_{index-1}_excess")
                else:
                    layer.model_premium = getattr(cds.options[selected_option - 1], f"model_premium_{index-1}_excess")
                    cyber_premium = getattr(cds.cyber_options[selected_option - 1],f"model_premium_third_party_{index-1}_excess") * (1 + nmp_load) if getattr(cds.cyber_options[selected_option - 1],f"model_premium_third_party_{index-1}_excess") is not None else 0   
                    model_premium_exc_cyber = max(layer.model_premium - cyber_premium, 0)

                    
                layer.quoted_premium = getattr(cds.options[selected_option - 1], f"quoted_premium_{index-1}_excess")
                
                if getattr(cds,f"add_excess_{index-1}") : 
                    layer.show_row = True
                else: 
                    layer.show_row = False 
                
    

            # Calculations -----------
            # Retention layer
            if index == 0:
                layer.brokerage = None     
                layer.quoted_rate = None
                layer.bound_rate = None
                layer.benchmark_premium = None
                layer.technical_premium_net = None
                layer.technical_premium = None
                layer.tpi = None
                layer.net_written_premium = None
            # Primary and Excess layers
            else:
                # brokerage - if none, set to zero
                if layer.brokerage == None:
                    layer.brokerage = 0
                    
                # Quoted rate
                layer.quoted_rate = (layer.quoted_premium / (cds.exposure.aggregate.revenue / 1000)) if cds.exposure.aggregate.revenue and layer.quoted_premium else 0

                # Bound rate
                layer.bound_rate = (layer.bound_premium / (cds.exposure.aggregate.revenue / 1000)) if cds.exposure.aggregate.revenue and layer.bound_premium else 0          

                # Benchmark premium
                layer.benchmark_premium = layer.model_premium * (priced_to_net_loss_ratio / benchmark_loss_ratio) if benchmark_loss_ratio else 0

                # BPI
                if layer.benchmark_premium == 0 :
                    layer.bpi = None 
                elif layer.bound_premium != None:
                    layer.bpi = layer.bound_premium / layer.benchmark_premium
                elif layer.quoted_premium != None:
                    layer.bpi = layer.quoted_premium / layer.benchmark_premium
                else:
                    layer.bpi = None                
                    
                # Net written premium
                if layer.bound_premium != None:                 
                        layer.net_written_premium = layer.bound_premium * (1 - layer.brokerage)                    
                elif layer.quoted_premium != None:
                        layer.net_written_premium = layer.quoted_premium * (1 - layer.brokerage)
                else:
                        layer.net_written_premium = 0

                # Net technical premium
                # note expected losses already loads up for nmp
                denominator = (1 - var_exp + inv_inc - (cost_of_ri -ri_rec) - roc * capital_req)
                if denominator and layer.benchmark_premium != 0 : 
                    expect_loss_cost_non_cyber = model_premium_exc_cyber * priced_to_net_loss_ratio * ( 1 - layer.brokerage)
                    expect_loss_cost_cyber = cyber_premium  * priced_to_net_loss_ratio * ( 1 - cyber_brokerage)
                    tech_prem_net = ((expect_loss_cost_non_cyber + expect_loss_cost_cyber)* (1 + che) + fixed_exp_usd / currency_factor) / denominator
                    weighted_cyber_and_pricing_brokerage = (expect_loss_cost_non_cyber * layer.brokerage + expect_loss_cost_cyber * cyber_brokerage) / (expect_loss_cost_non_cyber + expect_loss_cost_cyber) if (expect_loss_cost_non_cyber + expect_loss_cost_cyber) > 0 else 0
                    # Old Method
                    layer.technical_premium_net = (layer.benchmark_premium * (1- layer.brokerage) * 0.7 * (1 + che) + fixed_exp_usd / currency_factor) / denominator
                else:
                    layer.technical_premium_net = 0
                    weighted_cyber_and_pricing_brokerage = 0
                    tech_prem_net = 0
                
                # Gross technical premium
                # layer.technical_premium = layer.technical_premium_net / (1 - layer.brokerage) if (1 - layer.brokerage) else 0
                layer.technical_premium = tech_prem_net / (1- weighted_cyber_and_pricing_brokerage) if (1- weighted_cyber_and_pricing_brokerage) else 0

                # TPI
                if layer.bound_premium != None and layer.technical_premium != 0:
                    layer.tpi = layer.bound_premium / layer.technical_premium
                elif layer.quoted_premium != None and layer.technical_premium != 0:
                    layer.tpi = layer.quoted_premium / layer.technical_premium
                else:
                    layer.tpi = None                               

            # Section reference valdations 
            if layer.section_reference is not None and re.search(r'[£$%&,@!*.<>\?/\|~#}{\[\]]', layer.section_reference) :
                hx.errors.validation("Invalid characters entered in layer Policy Reference")
            if layer.section_reference is not None and layer.status != "Bound" :    
                hx.errors.validation("Only Bound risks should have a Policy Reference")
            if layer.section_reference is not None :
                if len(layer.section_reference) > 20:    
                    hx.errors.validation("Policy Reference cannot exceed 20 characters")
            if layer.section_reference is not None and layer.section_reference == layer.rate_change.expiring_policy_info.expiring_section_reference:
                hx.errors.validation("Current Policy Reference is equal to Expiring Policy Reference. Please update Policy Reference.")
            
            if layer.status == "Bound" :
                bound_validation.append(True)
            else: 
                bound_validation.append(False)

            if layer.section_reference is None and layer.status == "Bound" :
                hx.errors.validation("Please enter a Policy Reference for Bound Risks")

        # This is just for the view - setting the retention (which is in a different structure) equal to the 0 layer in the layers node 
        cds.rating_factors.retention.limit = cds.layers[0].limit

        # bound_validation_check = sum(bound_validation)
        # if bound_validation_check < 1 :
        #     hx.errors.validation("To finalise a risk, at least one layer must be bound")
