##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################

###  1) DAY 2 - check 0.01 in implied_pod_capped below:
###     implied_pod_capped          = min(1,    max(0.01,   implied_pod))                                           # relected 0.01 per model but AAA pod is 0.0000001 - above code would be better
###  2) 
###  3) 
###  4) 
###  5) 

##############################################################################################################################


import hx
import pandas as pd
import numpy as np
import algorithms.rate_constants as const
from algorithms import parameter_tables_schema as params
from algorithms.rate_utilities import ratio, look_up,  pd_df_from_hx_list, write_pd_to_hxd
from algorithms.rate_constants import benchmark_lr, bp_class


def rate_rating_summary(hxd):

    rf = hxd.cds.rating_factors

    # Set rating methodology
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == 'Case Priced'
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == 'Rater'

    # Pull in technical premium parameters and fx rates from user library & append legacy parameters
    legacy_tp_df    = hx.params.tbl_legacy_tp_parameters
    tp_params_df    = params.tp_parameters.df()
    tp_params_df    = pd.concat([tp_params_df, legacy_tp_df], axis=0, ignore_index=True) # appending the legacy tp parameters
    fx_rates_df     = params.fx_rates.df()
    yoa             = hxd.hx_core.inception_date.year
    
    # To stop the model erroring if the inception year defaults to an old year not in the TP data
    if yoa in list(tp_params_df['year']):   tp_year = yoa
    else:                                   tp_year = tp_params_df['year'].max()
    

    tp_lookup_bool  = (tp_params_df['business_plan_class'] == bp_class) & (tp_params_df['year'] == tp_year)
    tp_params       = tp_params_df[tp_lookup_bool]

    # Set up tp params
    che             = tp_params['che'].iloc[0]
    var_exp         = tp_params['var_exp'].iloc[0]
    inv_inc         = tp_params['inv_inc'].iloc[0]
    cost_of_ri      = tp_params['cost_of_ri'].iloc[0]
    ri_rec          = tp_params['ri_rec'].iloc[0]
    roc             = tp_params['roc'].iloc[0]
    fixed_exp_usd   = tp_params['fixed_exp'].iloc[0]
    capital_req     = tp_params['capital_req'].iloc[0]
    nmp_load        = tp_params['nmp_load'].iloc[0]

    # Convert fixed expenses to model currency (default to USD if error)
    ccy       = hxd.cds.currencies.source_currency
    fixed_exp = fixed_exp_usd * look_up(ccy, 'ccy', 'fx_rate', fx_rates_df, if_not_found=1)

    # Calculate technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc*capital_req
 
    cds         = hxd.cds  
 




 
    ###########################################################################################################################################################################################
    ##################      CRCF            ##### > PATH TAKEN IF CRCF        (inappropriate to separate into crcf / political functions - due to co-dependency on all the factors above
    ###########################################################################################################################################################################################
    if (cds.product in {'Contract Frustration','Credit Risk'}):

        layer       = hxd.cds.layers[0].crcf

        ################################################
        # 1) load exposure profile values
        ################################################
        exposure_df             = pd_df_from_hx_list(cds.exposure.granular.crcf.exposure_profile)

        avg_exp_na              = exposure_df['average_exposure'].sum() ==0
        pre_avg_sev_na          = exposure_df['pre_uw_adj_average_severity'].sum() ==0
        pst_avg_sev_na          = exposure_df['pst_uw_adj_average_severity'].sum() ==0
        pre_avg_loss_na         = exposure_df['pre_uw_adj_average_loss'].sum() ==0
        pst_avg_loss_na         = exposure_df['pst_uw_adj_average_loss'].sum() ==0

        pre_uw_adj_tenor_load   = 1 if avg_exp_na       else ( (exposure_df['pre_uw_adj_tenor_load'] * exposure_df['average_exposure']).sum()   /   exposure_df['average_exposure'].sum())
        pre_uw_adj_recov_expect = 0 if pre_avg_sev_na   else ( (exposure_df['expected_recovery_pct'] * exposure_df['pre_uw_adj_average_severity']).sum()   /   exposure_df['pre_uw_adj_average_severity'].sum())
        pre_uw_adj_limit_discount=1 if pre_avg_loss_na  else ( exposure_df['pre_uw_adj_average_loss_adj_lim_xs'].sum() / exposure_df['pre_uw_adj_average_loss'].sum()  )
        pre_uw_adj_expect_loss  = ( exposure_df['pre_uw_adj_average_loss_adj_lim_xs'].sum()  )
        gross_premium_offer     = ( exposure_df['pre_uw_adj_premium_achieved_adj_pod'].sum()  )

        pst_uw_adj_tenor_load   = 1 if avg_exp_na       else ( (exposure_df['pst_uw_adj_tenor_load'] * exposure_df['average_exposure']).sum()   /   exposure_df['average_exposure'].sum())
        pst_uw_adj_recov_expect = 0 if pst_avg_sev_na   else ( (exposure_df['expected_recovery_pct'] * exposure_df['pst_uw_adj_average_severity']).sum()   /   exposure_df['pst_uw_adj_average_severity'].sum())
        pst_uw_limit_discount   = 1 if pst_avg_loss_na  else ( exposure_df['pst_uw_adj_average_loss_adj_lim_xs'].sum() / exposure_df['pst_uw_adj_average_loss'].sum()  )
        pst_uw_adj_expect_loss  = ( exposure_df['pst_uw_adj_average_loss_adj_lim_xs'].sum()  )

        implied_lgd             = 0 if avg_exp_na       else ( (exposure_df['implied_lgd'] * exposure_df['average_exposure']).sum()   /   exposure_df['average_exposure'].sum())
        implied_pod             = 1 if pst_avg_sev_na   else ( (exposure_df['implied_grade_pod_inc'] * exposure_df['pst_uw_adj_average_severity']).sum()   /   exposure_df['pst_uw_adj_average_severity'].sum())


        ################################################
        # 2) Calculate Expected Losses
        ################################################

        # load inflation & cat uplift
        plan_df     = hx.params.tbl_year_plan_assump
        plan_year   = yoa   if (yoa in list(plan_df['year']))  else plan_df['year'].max()
        plan_lr     = plan_df[(plan_df['year'] == plan_year)]['plan_gnlr_att_cat'].iat[0]
        inf_uplift  = plan_df[(plan_df['year'] == plan_year)]['inflation_uplift'].iat[0]
        cat_uplift  = plan_df[(plan_df['year'] == plan_year)]['cat_uplift'].iat[0]

        # load other assump - notice tenor_annual here reflects the true number of days of coverage expressed in years
        uw_adj      = cds.modifiers.crcf.selected.uw_adj
        tenor_annual= cds.rating_factors.policy_term / 12


        # expected loss calc
        layer.premium_composition_pre_uwadj_term.expected_loss      = pre_uw_adj_expect_loss                * (1 + nmp_load) * (1 + inf_uplift) * (1 + cat_uplift)
        layer.premium_composition_pst_uwadj_term.expected_loss      = pst_uw_adj_expect_loss * (1 + uw_adj) * (1 + nmp_load) * (1 + inf_uplift) * (1 + cat_uplift)
        layer.premium_composition_pre_uwadj_annual.expected_loss    = layer.premium_composition_pre_uwadj_term.expected_loss / tenor_annual
        layer.premium_composition_pst_uwadj_annual.expected_loss    = layer.premium_composition_pst_uwadj_term.expected_loss / tenor_annual



        ################################################
        # 3) Calculate Premium Composition
        ################################################
        #load additional assump
        bkg = 0 if hxd.cds.layers[0].brokerage == 1 else hxd.cds.layers[0].brokerage
        share = (hxd.cds.layers[0].written_line or 1)

        for basis_desc in {'pre_uwadj_term','pst_uwadj_term','pre_uwadj_annual','pst_uwadj_annual'}:
            basis                       = getattr(layer, f'premium_composition_{basis_desc}')
            basis.che                   = basis.expected_loss * che
            basis.fixed_expenses        = fixed_exp / share

            basis.premium_technical       = ( (basis.expected_loss + basis.che   +   basis.fixed_expenses) 
                                                    /(1 - (cost_of_ri - ri_rec) - var_exp - roc*capital_req + inv_inc)
                                                    /(1 - bkg) )
            basis.investment_income       = basis.premium_technical * (1 - bkg) * inv_inc * (-1)
            basis.variable_expenses       = basis.premium_technical * (1 - bkg) * var_exp
            basis.cost_of_reinsurance     = basis.premium_technical * (1 - bkg) * (cost_of_ri - ri_rec)
            basis.capital                 = basis.premium_technical * (1 - bkg) * capital_req * roc
            basis.brokerage               = basis.premium_technical * bkg

            basis.premium_benchmark     = basis.expected_loss / benchmark_lr / (1 - bkg)
            basis.loadings_benchmark    = basis.premium_benchmark - basis.expected_loss
            basis.premium_model         = 0 #not used
            basis.loadings_model        = 0 #not used
            basis.premium_plan          = basis.expected_loss / plan_lr / (1 - bkg) 
            basis.loadings_plan         = basis.premium_plan - basis.expected_loss
            basis.premium_bound         = gross_premium_offer / (1 if basis_desc in {'pre_uwadj_term','pst_uwadj_term'} else tenor_annual)
            basis.loadings_bound        = basis.premium_bound - basis.expected_loss



        ################################################
        # 4) Loss Composition
        ################################################
        loss_pre            = hxd.cds.layers[0].crcf.loss_composition_pre_uwadj_term
        loss_pst            = hxd.cds.layers[0].crcf.loss_composition_pst_uwadj_term

        loss_pre.exposure           = cds.exposure.granular.crcf.sum_insured
        loss_pst.exposure           = cds.exposure.granular.crcf.sum_insured

        loss_pre.credit_rating      = cds.modifiers.crcf.default.grade
        loss_pst.credit_rating      = cds.modifiers.crcf.selected.grade

        loss_pre.pod                = cds.modifiers.crcf.default.pod
        loss_pst.pod                = cds.modifiers.crcf.selected.pod

        loss_pre.lgd                = cds.modifiers.crcf.default.lgd
        loss_pst.lgd                = cds.modifiers.crcf.selected.lgd

        loss_pre.tenor_load         = pre_uw_adj_tenor_load
        loss_pst.tenor_load         = pst_uw_adj_tenor_load

        loss_pre.recovery_discounted= pre_uw_adj_recov_expect
        loss_pst.recovery_discounted= pst_uw_adj_recov_expect

        loss_pre.limit_discount     = pre_uw_adj_limit_discount
        loss_pst.limit_discount     = pst_uw_limit_discount

        loss_pre.term               = tenor_annual
        loss_pst.term               = tenor_annual

        loss_pre.expected_loss      = layer.premium_composition_pre_uwadj_term.expected_loss
        loss_pst.expected_loss      = layer.premium_composition_pst_uwadj_term.expected_loss

        loss_pre_other_helper       = (     loss_pre.exposure
                                        * loss_pre.pod
                                        * loss_pre.lgd 
                                        * loss_pre.tenor_load
                                        * (1 - loss_pre.recovery_discounted)
                                        * loss_pre.limit_discount
                                        * loss_pre.term )

        loss_pre.other              = 1 if np.isnan(loss_pre_other_helper) or (loss_pre_other_helper == 0) else loss_pre.expected_loss / loss_pre_other_helper

        loss_pst_other_helper       = (     loss_pst.exposure
                                        * loss_pst.pod
                                        * loss_pst.lgd 
                                        * loss_pst.tenor_load
                                        * (1 - loss_pst.recovery_discounted)
                                        * loss_pst.limit_discount
                                        * loss_pst.term )

        loss_pst.other              = 1 if np.isnan(loss_pst_other_helper) or (loss_pst_other_helper == 0) else loss_pst.expected_loss / loss_pst_other_helper




        ################################################
        # 5) Rate on Exposure & KPIs
        ################################################

        annual_roe_offered = layer.metrics_summary_pst_uwadj_annual.roe_offered

        if annual_roe_offered is not None:
            layer.metrics_summary_pre_uwadj_annual.roe_offered  = annual_roe_offered
            layer.metrics_summary_pre_uwadj_term.roe_offered    = annual_roe_offered * tenor_annual
            layer.metrics_summary_pst_uwadj_term.roe_offered    = annual_roe_offered * tenor_annual


            for basis_desc in {'pre_uwadj_term','pst_uwadj_term','pre_uwadj_annual','pst_uwadj_annual'}:
                basis                       = getattr(layer, f'metrics_summary_{basis_desc}')
                prem_basis                  = getattr(layer, f'premium_composition_{basis_desc}')


                expected_loss               = prem_basis.expected_loss
                gg_premium_offer            = prem_basis.premium_bound
                gg_premium_bench            = prem_basis.premium_benchmark
                gg_premium_tech             = prem_basis.premium_technical
                gg_premium_plan             = prem_basis.premium_plan

                basis.roe_plan       = 0 if (gg_premium_offer == 0) else basis.roe_offered * gg_premium_plan  / gg_premium_offer
                basis.roe_technical  = 0 if (gg_premium_offer == 0) else basis.roe_offered * gg_premium_tech  / gg_premium_offer
                basis.roe_benchmark  = 0 if (gg_premium_offer == 0) else basis.roe_offered * gg_premium_bench / gg_premium_offer

                if basis_desc in {'pre_uwadj_term','pst_uwadj_term'}:
                    basis.priced_gglr   = 0 if (gg_premium_offer == 0) else expected_loss     / gg_premium_offer
                    basis.priced_gnlr   = 0 if (bkg == 1)              else basis.priced_gglr / (1 - bkg)                       
                    basis.bpi           = 0 if (gg_premium_bench == 0) else gg_premium_offer  / gg_premium_bench
                    basis.tpi           = 0 if (gg_premium_tech == 0)  else gg_premium_offer  / gg_premium_tech
                    basis.priced_to_plan= 0 if (gg_premium_plan == 0)  else gg_premium_offer  / gg_premium_plan

                if basis_desc in {'pst_uwadj_term'}:
                    basis.lgd_bound             = implied_lgd
                    
                    grade_pod_df                = hx.params.tbl_grade_pod
                    grade_pod_df.sort_values(by=['Score'], inplace = True)
                    # pod_min_available           = grade_pod_df['Value'].min()
                    # pod_max_available           = grade_pod_df['Value'].max()
                    # implied_pod_capped          = min(pod_max_available,    max(pod_min_available,   implied_pod)) # better code
                    implied_pod_capped          = min(1,    max(0.01,   implied_pod))                                           # relected 0.01 per model but AAA pod is 0.0000001 - above code would be better
                    implied_pod_row             = grade_pod_df[ (grade_pod_df['Value'] <= implied_pod_capped) ]
                    basis.credit_rating_bound   = '' if implied_pod_row.empty     else implied_pod_row['Grade'].iat[0]
               



        ################################################
        # 6) Loading values into CDS standard fields incluiding layers etc
        ################################################

        for layer in hxd.cds.layers:

            share                               = (layer.written_line or 1)
            layer.quoted_premium                = layer.crcf.premium_composition_pst_uwadj_term.premium_bound    *   share
            layer.expected_loss_cost            = loss_pst.expected_loss    *   share
            layer.expected_loss_cost_pre_uw_adj = loss_pre.expected_loss    *   share

            # Calculate the impact of UW adjustment by using Expected Loss Cost and Expected Loss Cost Pre UW Adjustment, rather than using TP and TP pre UW adjustment for the calc
            layer.uw_adj_impact = ratio(layer.expected_loss_cost, layer.expected_loss_cost_pre_uw_adj) - 1
            
            # If rater priced
            if hxd.cds.standard_fields.is_rater_priced and layer.quoted_premium:

                expected_loss                       = layer.expected_loss_cost
                layer.technical_premium             = layer.crcf.premium_composition_pst_uwadj_term.premium_technical    *   share
                layer.technical_premium_net         = layer.technical_premium   *   (1- (layer.brokerage or 0))
                layer.technical_premium_pre_uw_adj  = layer.crcf.premium_composition_pre_uwadj_term.premium_technical    *   share
                layer.benchmark_premium             = layer.crcf.premium_composition_pst_uwadj_term.premium_benchmark    *   share
                layer.model_premium                 = layer.technical_premium 

                layer.bpi                           = ratio(layer.quoted_premium,   layer.benchmark_premium)
                layer.bpi_pre_uw_adj                = ratio(layer.quoted_premium,   layer.crcf.premium_composition_pre_uwadj_term.premium_benchmark    *   share )
                layer.tpi                           = ratio(layer.quoted_premium,   layer.technical_premium)
                layer.tpi_pre_uw_adj                = ratio(layer.quoted_premium,   layer.technical_premium_pre_uw_adj)

                
                quoted_premium_net = layer.quoted_premium *   (1- (layer.brokerage or 0))
                layer.pflr = ratio(expected_loss, (quoted_premium_net or 1))
                layer.pflr_pre_uw_adj   = ratio(layer.expected_loss_cost_pre_uw_adj,    (quoted_premium_net or 1))

                layer.roc = ratio(
                    1 - layer.pflr - var_exp + inv_inc - (cost_of_ri-ri_rec) - ratio(fixed_exp + expected_loss*che, quoted_premium_net),
                    capital_req
                )

                # Store annualised premiums for use in rate change calcs
                layer.quoted_premium_annualised     = (layer.quoted_premium or 0)    / ( (rf.policy_term or 12) /12 )
                layer.benchmark_premium_annualised  = (layer.benchmark_premium or 0) / ( (rf.policy_term or 12) /12 )

                # layer.pflr_att = ratio(layer.expected_loss_cost_att, (quoted_premium_net or 1))  # Guidance: AC/JC Discussion 10-March-25 do not map to and remove from views
                # layer.pflr_cat = ratio(layer.expected_loss_cost_cat, (quoted_premium_net or 1))  # Guidance: AC/JC Discussion 10-March-25 do not map to and remove from views
                # layer.premium               = 1 # Guidance: DO NOT USE UNTIL WORKBENCH INTEGRATION.
                # layer.unity_premium         = 1 # Guidance: This is an admitted measure. The premium before any scheduled modifiers. Gross of brokerage.








     
    ###########################################################################################################################################################################################
    ##################      Political       ##### > PATH TAKEN IF Political   (inappropriate to separate into crcf / political functions - due to co-dependency on all the factors above
    ###########################################################################################################################################################################################
    elif (cds.product in {'Political Risk'}):

        pol         = cds.exposure.granular.political
        pol_key     = cds.exposure.granular.political.key_summary_outputs
        pol_mod     = cds.modifiers.political
        layer       = hxd.cds.layers[0].political
        
        ################################################
        # 1) load exposure profile values
        ################################################
        exposure_df             = pd_df_from_hx_list(cds.exposure.granular.political.country_exposure)


        ################################################
        # 2) Calculate Expected Losses
        ################################################

        uw_adj                      = (pol_mod.selected.total or 0)
        term_to_annual              = 12 / (hxd.cds.rating_factors.policy_term or 12)
        term_to_annual              = 1 if (term_to_annual >= 364/365.25 and term_to_annual <=366/365.25) else term_to_annual # so slight variations in date entry dont drive a difference in values displayed
        annual_to_term              = ratio(1, term_to_annual)

        # set totals to nil prior to adding incrementally below
        layer.premium_composition_pre_uwadj.total.expected_loss = 0
        layer.premium_composition_pst_uwadj.total.expected_loss = 0

        for cover_desc in {'gov_action',  'pol_violence', 'cur_inconvertibility', 'cont_relation_govt'}:
            pre_adj_cover               = getattr(layer.premium_composition_pre_uwadj, cover_desc)
            pst_adj_cover               = getattr(layer.premium_composition_pst_uwadj, cover_desc)


            # assign expected losses before and after uw adjustments
            pre_adj_cover               = getattr(layer.premium_composition_pre_uwadj, cover_desc)
            pre_adj_cover.expected_loss = (getattr(pol_key.simulated_loss, cover_desc) or 0)
            pst_adj_cover.expected_loss = pre_adj_cover.expected_loss * (1 + uw_adj)

            # increment the totals with the amount of expected loss from basis
            layer.premium_composition_pre_uwadj.total.expected_loss   += pre_adj_cover.expected_loss
            layer.premium_composition_pst_uwadj.total.expected_loss   += pst_adj_cover.expected_loss


        ################################################
        # 3) Calculate Premium Composition
        ################################################
        #load additional assump
        bkg = 0 if hxd.cds.layers[0].brokerage == 1 else hxd.cds.layers[0].brokerage
        share = (hxd.cds.layers[0].written_line or 1)

        # load in the plan loss ratio
        plan_df     = hx.params.tbl_year_plan_assump
        plan_year   = yoa   if (yoa in list(plan_df['year']))  else plan_df['year'].max()
        plan_lr     = plan_df[(plan_df['year'] == plan_year)]['plan_gnlr_att_cat'].iat[0]

        # load in the 'model' loss ratio
        all_product_assump_df           = hx.params.tbl_product_assump
        product_assump_df               = all_product_assump_df[ (all_product_assump_df['Product']   == cds.product     )]
        lr_on_model_premium_row         = product_assump_df[    (product_assump_df['Assumption Group']  == "lr_on_model_premium"        ) ]
        lr_on_model_premium             = 1 if lr_on_model_premium_row.empty        else lr_on_model_premium_row['Value'].iat[0]   

        # calculate the bound premium
        bound_prem                      = (layer.metrics_summary_pst_uwadj.rol_offered or 0)     *     (hxd.cds.layers[0].limit or 0)


        for basis_desc in  {'pre_uwadj',  'pst_uwadj'}:
            for cover_desc in {'gov_action',  'pol_violence', 'cur_inconvertibility', 'cont_relation_govt', 'total'}:

                # setup the pointer to the basis and cover in question
                basis_cover                         = getattr(getattr(layer, f'premium_composition_{basis_desc}'),cover_desc)                       # needed to nest getattr as can only go one layer deep on attributes at a time it appears

                # calculate class contribution to total for expected losses - needed to allocate out fixed expenses
                total_exp_loss                      = getattr(getattr(getattr(layer, f'premium_composition_{basis_desc}'),'total'),'expected_loss') # needed to nest getattr as can only go one layer deep on attributes at a time it appears
                percent_cover                       = 0     if total_exp_loss==0    else basis_cover.expected_loss / total_exp_loss                 # needed to nest getattr as can only go one layer deep on attributes at a time it appears

                basis_cover.che                     = basis_cover.expected_loss * che
                basis_cover.fixed_expenses          = fixed_exp / share * percent_cover * term_to_annual

                basis_cover.premium_technical       = ( (basis_cover.expected_loss + basis_cover.che   +   basis_cover.fixed_expenses) 
                                                       /(1 - (cost_of_ri - ri_rec) - var_exp - roc*capital_req + inv_inc)
                                                       /(1 - bkg) )

                basis_cover.investment_income       = basis_cover.premium_technical * (1 - bkg) * inv_inc * (-1)
                basis_cover.variable_expenses       = basis_cover.premium_technical * (1 - bkg) * var_exp
                basis_cover.cost_of_reinsurance     = basis_cover.premium_technical * (1 - bkg) * (cost_of_ri - ri_rec)
                basis_cover.capital                 = basis_cover.premium_technical * (1 - bkg) * capital_req * roc
                basis_cover.brokerage               = basis_cover.premium_technical * bkg

                basis_cover.premium_benchmark       = basis_cover.expected_loss / benchmark_lr / (1 - bkg)
                basis_cover.loadings_benchmark      = basis_cover.premium_benchmark - basis_cover.expected_loss
                
                basis_cover.premium_model           = basis_cover.expected_loss / lr_on_model_premium / (1 - bkg)
                basis_cover.loadings_model          = basis_cover.premium_model - basis_cover.expected_loss
                
                basis_cover.premium_plan            = basis_cover.expected_loss / plan_lr / (1 - bkg) 
                basis_cover.loadings_plan           = basis_cover.premium_plan - basis_cover.expected_loss
                
                basis_cover.premium_bound           = bound_prem * percent_cover
                basis_cover.loadings_bound          = basis_cover.premium_bound - basis_cover.expected_loss


        ################################################
        # 5) Rate on Line & KPIs
        ################################################

        annual_rol_offered = layer.metrics_summary_pst_uwadj.rol_offered

        if annual_rol_offered is not None:
            layer.metrics_summary_pre_uwadj.rol_offered  = annual_rol_offered

            for basis_desc in {'pre_uwadj','pst_uwadj'}:

                basis                       = getattr(layer, f'metrics_summary_{basis_desc}')
                prem_basis                  = getattr(getattr(layer, f'premium_composition_{basis_desc}'),'total')

                expected_loss               = prem_basis.expected_loss
                gg_premium_offer            = prem_basis.premium_bound
                gg_premium_bench            = prem_basis.premium_benchmark
                gg_premium_tech             = prem_basis.premium_technical
                gg_premium_plan             = prem_basis.premium_plan
                gg_premium_model            = prem_basis.premium_model


                basis.rol_plan       = 0 if (gg_premium_offer == 0) else basis.rol_offered * gg_premium_plan  / gg_premium_offer
                basis.rol_model      = 0 if (gg_premium_offer == 0) else basis.rol_offered * gg_premium_model / gg_premium_offer
                basis.rol_technical  = 0 if (gg_premium_offer == 0) else basis.rol_offered * gg_premium_tech  / gg_premium_offer
                basis.rol_benchmark  = 0 if (gg_premium_offer == 0) else basis.rol_offered * gg_premium_bench / gg_premium_offer

                basis.priced_gglr   = 0 if (gg_premium_offer == 0) else expected_loss     / gg_premium_offer
                basis.priced_gnlr   = 0 if (bkg == 1)              else basis.priced_gglr / (1 - bkg)                       
                basis.bpi           = 0 if (gg_premium_bench == 0) else gg_premium_offer  / gg_premium_bench
                basis.tpi           = 0 if (gg_premium_tech == 0)  else gg_premium_offer  / gg_premium_tech
                basis.priced_to_plan= 0 if (gg_premium_plan == 0)  else gg_premium_offer  / gg_premium_plan


        ################################################
        # 6) Loading values into CDS standard fields incluiding layers etc
        ################################################

        for layer in hxd.cds.layers:

            share                               = (layer.written_line or 1)
            layer.quoted_premium                = layer.political.premium_composition_pst_uwadj.total.premium_bound    *   share   *   annual_to_term
            layer.expected_loss_cost            = layer.political.premium_composition_pst_uwadj.total.expected_loss    *   share   *   annual_to_term
            layer.expected_loss_cost_pre_uw_adj = layer.political.premium_composition_pre_uwadj.total.expected_loss    *   share   *   annual_to_term

            # Calculate the impact of UW adjustment by using Expected Loss Cost and Expected Loss Cost Pre UW Adjustment, rather than using TP and TP pre UW adjustment for the calc
            layer.uw_adj_impact = ratio(layer.expected_loss_cost, layer.expected_loss_cost_pre_uw_adj) - 1
            
            # If rater priced
            if hxd.cds.standard_fields.is_rater_priced and layer.quoted_premium:

                expected_loss                       = layer.expected_loss_cost
                layer.technical_premium             = layer.political.premium_composition_pst_uwadj.total.premium_technical    *   share   *   annual_to_term
                layer.technical_premium_net         = layer.technical_premium   *   (1- (layer.brokerage or 0))
                layer.technical_premium_pre_uw_adj  = layer.political.premium_composition_pre_uwadj.total.premium_technical    *   share   *   annual_to_term
                layer.benchmark_premium             = layer.political.premium_composition_pst_uwadj.total.premium_benchmark    *   share   *   annual_to_term
                layer.model_premium                 = layer.technical_premium 

                layer.bpi                           = ratio(layer.quoted_premium,   layer.benchmark_premium)
                layer.tpi                           = ratio(layer.quoted_premium,   layer.technical_premium)
                layer.tpi_pre_uw_adj                = ratio(layer.quoted_premium,   layer.technical_premium_pre_uw_adj)
                layer.bpi_pre_uw_adj                = ratio(layer.quoted_premium,   layer.political.premium_composition_pre_uwadj.total.premium_benchmark   *   share   *   annual_to_term)


                quoted_premium_net      = layer.quoted_premium  *   (1- (layer.brokerage or 0))
                layer.pflr              = ratio(expected_loss,                          (quoted_premium_net or 1))
                layer.pflr_pre_uw_adj   = ratio(layer.expected_loss_cost_pre_uw_adj,    (quoted_premium_net or 1))

                layer.roc = ratio(
                    1 - layer.pflr - var_exp + inv_inc - (cost_of_ri-ri_rec) - ratio(fixed_exp + expected_loss*che, quoted_premium_net),
                    capital_req
                )

                # Store annualised premiums for use in rate change calcs
                layer.quoted_premium_annualised     = (layer.quoted_premium or 0)    * term_to_annual
                layer.benchmark_premium_annualised  = (layer.benchmark_premium or 0) * term_to_annual


                # layer.pflr_att = ratio(layer.expected_loss_cost_att, (quoted_premium_net or 1))  # Guidance: AC/JC Discussion 10-March-25 do not map to and remove from views
                # layer.pflr_cat = ratio(layer.expected_loss_cost_cat, (quoted_premium_net or 1))  # Guidance: AC/JC Discussion 10-March-25 do not map to and remove from views
                # layer.premium               = 1 # Guidance: DO NOT USE UNTIL WORKBENCH INTEGRATION.
                # layer.unity_premium         = 1 # Guidance: This is an admitted measure. The premium before any scheduled modifiers. Gross of brokerage.




