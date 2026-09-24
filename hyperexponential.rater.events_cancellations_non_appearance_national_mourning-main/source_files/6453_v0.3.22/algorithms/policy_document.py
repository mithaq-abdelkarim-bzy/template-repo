import hx
import pandas as pd
import json
from datetime import datetime
from algorithms.rate_utilities import pd_df_from_hx_list, rgetattr



CVG_LST = ["all_risks" 
            , "adverse_weather" 
            , "earthquake" 
            , "windstorm" 
            , "wildfire" 
            , "terrorism" 
            , "cyber" 
            , "national_mourning" 
            , "riots_and_civil_commotion" 
            , "strike" 
            , "war" 
            , "catastrophic_non_app" ]


def dict_sclr_risk_info(hxd):
    cds  = hxd.cds
    data = {
             "ri.expiry_date":                                                      hxd.hx_core.expiry_date
            ,"ri.inception_date":                                                   hxd.hx_core.inception_date
            ,"ri.underwriter":                                                      cds.standard_fields.underwriter
            ,"ri.product_bool":                                                     cds.risk_info.product_bool
            ,"ri.currency":                                                         cds.currencies.source_currency
            ,"ri.is_renewal":                                                       cds.standard_fields.is_renewal
            ,"ri.section_ref_ec":                                                   cds.layers[0].coverages.ec_total.section_reference
            ,"ri.section_ref_na":                                                   cds.layers[0].coverages.na_total.section_reference.selected
            ,"ri.insured_name":                                                     cds.standard_fields.insured_name

            ,"ri.event_name":                                                       cds.risk_info.event_name
            ,"ri.written_line":                                                     cds.layers[0].written_line
            ,"ri.brokerage":                                                        cds.layers[0].brokerage
            ,"ri.status":                                                           cds.layers[0].status

            ,"ri.broker_name":                                                      cds.standard_fields.broker
            ,"ri.broker_contact":                                                   cds.broker_contact

            ,"ri.actuary_view":                                                     hxd.model_state.show_actuarial
            ,"ri.rater_priced":                                                     cds.standard_fields.rating_methodology
            ,"ri.schema_view":                                                      hxd.schema_view.force_show_view
            ,"ri.old_nm_approach":                                                  hxd.model_state.use_nm_app_old_model
            ,"ri.det_agg_approach":                                                 hxd.model_state.use_determ_agg_calc
            ,"ri.is_migrated":                                                      hxd.model_state.is_migrated
            ,"ri.disable_validation":                                               hxd.model_state.disable_validation
            }
    return data   


def dict_sclr_exposure(hxd): 
    cds  = hxd.cds
    data = {
             "expo.event_type":                                                     cds.exposure.granular.event_cancel.event_type
            ,"expo.limit":                                                          cds.layers[0].coverages.ec_total.limit
            ,"expo.agg_limit":                                                      cds.layers[0].coverages.ec_total.aggregate_limit
            ,"expo.use_excess":                                                     cds.layers[0].coverages.ec_total.excess_use
            ,"expo.excess":                                                         cds.layers[0].coverages.ec_total.excess
            ,"expo.deductible":                                                     cds.layers[0].coverages.ec_total.deductible
            ,"expo.agg_deductible":                                                 cds.layers[0].coverages.ec_total.aggregate_deductible

            ,"expo.terror_td":                                                      cds.exposure.granular.event_cancel.terrorism_terms.time_distance
            ,"expo.terror_profile":                                                 cds.exposure.granular.event_cancel.terrorism_terms.event_profile
            ,"expo.terror_cityload":                                                cds.exposure.granular.event_cancel.terrorism_terms.city_load

            ,"expo.exposure_curve":                                                 cds.exposure.granular.event_cancel.exposure_curve
            ,"expo.curve_comments":                                                 cds.exposure.granular.event_cancel.exposure_curve_comments
            ,"expo.exposure_curve_warning":                                         cds.exposure.granular.event_cancel.exposure_curve_warning

            ,"expo.experience_use":                                                 cds.exposure.granular.event_cancel.experience
            ,"expo.experience_ilr":                                                 cds.exposure.granular.event_cancel.experience_ratio
            ,"expo.experience_factor":                                              cds.exposure.granular.event_cancel.experience_factor
            ,"expo.ncb_use":                                                        cds.exposure.granular.event_cancel.ncb
            ,"expo.ncb_pct":                                                        cds.exposure.granular.event_cancel.ncb_offered
            ,"expo.ncb_factor":                                                     cds.exposure.granular.event_cancel.ncb_factor

            ,"expo.ihs_last_run_status":                                            cds.ihs.last_run_status
            ,"expo.ihs_rerun_status":                                               cds.ihs.check_run_consistent
            ,"expo.ihs_value":                                                      cds.ihs.calc_run_value
            ,"expo.sim_last_run_status":                                            cds.exposure.granular.event_cancel.simulation.last_run_status
            ,"expo.sim_rerun_status":                                               cds.exposure.granular.event_cancel.simulation.check_run_consistent
            ,"expo.sim_value":                                                      cds.exposure.granular.event_cancel.simulation.calc_run_value

            ,"expo.agg_tiv_calc":                                                   cds.exposure.granular.event_cancel.agg_tiv_calc
            ,"expo.agg_tiv_sel":                                                    cds.exposure.granular.event_cancel.agg_tiv_uw
            ,"expo.agg_tiv_warning":                                                cds.exposure.granular.event_cancel.agg_tiv_warning
            }
    return data   


def dict_sclr_national_mourning(hxd):
    cds  = hxd.cds
    data = {
             "nm.cover":                                                            cds.exposure.granular.event_cancel.national_mourning.cover_level
            ,"nm.mourning_period":                                                  cds.exposure.granular.event_cancel.national_mourning.mourning_period

            ,"nm.u75_include":                                                      cds.exposure.granular.event_cancel.national_mourning.under_75.include
            ,"nm.u75_country":                                                      cds.exposure.granular.event_cancel.national_mourning.under_75.country
            ,"nm.u75_age":                                                          cds.exposure.granular.event_cancel.national_mourning.under_75.age
            ,"nm.u75_pod":                                                          cds.exposure.granular.event_cancel.national_mourning.under_75.prob_die
            ,"nm.u75_pos":                                                          cds.exposure.granular.event_cancel.national_mourning.under_75.prob_live
            ,"nm.u75_adj_affl":                                                     cds.exposure.granular.event_cancel.national_mourning.under_75.mod_affluence
            ,"nm.u75_adj_health":                                                   cds.exposure.granular.event_cancel.national_mourning.under_75.mod_health
            ,"nm.u75_pod_adj":                                                      cds.exposure.granular.event_cancel.national_mourning.under_75.prob_die_mod
            ,"nm.u75_pos_adj":                                                      cds.exposure.granular.event_cancel.national_mourning.under_75.prob_live_mod
            ,"nm.u75_check":                                                        cds.exposure.granular.event_cancel.national_mourning.under_75.check

            ,"nm.o75_b1_include":                                                   cds.exposure.granular.event_cancel.national_mourning.bespoke_1.include
            ,"nm.o75_b1_name":                                                      cds.exposure.granular.event_cancel.national_mourning.bespoke_1.name
            ,"nm.o75_b1_country":                                                   cds.exposure.granular.event_cancel.national_mourning.bespoke_1.country
            ,"nm.o75_b1_gender":                                                    cds.exposure.granular.event_cancel.national_mourning.bespoke_1.gender
            ,"nm.o75_b1_dob":                                                       cds.exposure.granular.event_cancel.national_mourning.bespoke_1.date_of_birth
            ,"nm.o75_b1_age":                                                       cds.exposure.granular.event_cancel.national_mourning.bespoke_1.age
            ,"nm.o75_b1_pod":                                                       cds.exposure.granular.event_cancel.national_mourning.bespoke_1.prob_die
            ,"nm.o75_b1_pos":                                                       cds.exposure.granular.event_cancel.national_mourning.bespoke_1.prob_live
            ,"nm.o75_b1_adj_affl":                                                  cds.exposure.granular.event_cancel.national_mourning.bespoke_1.mod_affluence
            ,"nm.o75_b1_adj_health":                                                cds.exposure.granular.event_cancel.national_mourning.bespoke_1.mod_health
            ,"nm.o75_b1_pod_adj":                                                   cds.exposure.granular.event_cancel.national_mourning.bespoke_1.prob_die_mod
            ,"nm.o75_b1_pos_adj":                                                   cds.exposure.granular.event_cancel.national_mourning.bespoke_1.prob_live_mod
            ,"nm.o75_b1_check":                                                     cds.exposure.granular.event_cancel.national_mourning.bespoke_1.check

            ,"nm.o75_b2_include":                                                   cds.exposure.granular.event_cancel.national_mourning.bespoke_2.include
            ,"nm.o75_b2_name":                                                      cds.exposure.granular.event_cancel.national_mourning.bespoke_2.name
            ,"nm.o75_b2_country":                                                   cds.exposure.granular.event_cancel.national_mourning.bespoke_2.country
            ,"nm.o75_b2_gender":                                                    cds.exposure.granular.event_cancel.national_mourning.bespoke_2.gender
            ,"nm.o75_b2_dob":                                                       cds.exposure.granular.event_cancel.national_mourning.bespoke_2.date_of_birth
            ,"nm.o75_b2_age":                                                       cds.exposure.granular.event_cancel.national_mourning.bespoke_2.age
            ,"nm.o75_b2_pod":                                                       cds.exposure.granular.event_cancel.national_mourning.bespoke_2.prob_die
            ,"nm.o75_b2_pos":                                                       cds.exposure.granular.event_cancel.national_mourning.bespoke_2.prob_live
            ,"nm.o75_b2_adj_affl":                                                  cds.exposure.granular.event_cancel.national_mourning.bespoke_2.mod_affluence
            ,"nm.o75_b2_adj_health":                                                cds.exposure.granular.event_cancel.national_mourning.bespoke_2.mod_health
            ,"nm.o75_b2_pod_adj":                                                   cds.exposure.granular.event_cancel.national_mourning.bespoke_2.prob_die_mod
            ,"nm.o75_b2_pos_adj":                                                   cds.exposure.granular.event_cancel.national_mourning.bespoke_2.prob_live_mod
            ,"nm.o75_b2_check":                                                     cds.exposure.granular.event_cancel.national_mourning.bespoke_2.check
            }
    return data   


def dict_sclr_non_appearance(hxd):
    cds  = hxd.cds
    data = {
             "na.genre":                                                            cds.exposure.granular.non_appearance.genre
            ,"na.base_rate":                                                        cds.exposure.granular.non_appearance.base_rate
            ,"na.num_shows":                                                        cds.exposure.granular.non_appearance.num_shows
            ,"na.avg_value":                                                        cds.exposure.granular.non_appearance.avg_show_value
            ,"na.tiv":                                                              cds.exposure.granular.non_appearance.agg_show_value
            ,"na.el_fgu":                                                           cds.exposure.granular.non_appearance.el_fgu
            
            ,"na.num_members":                                                      cds.exposure.granular.non_appearance.num_band_members
            ,"na.mod_num_members":                                                  cds.exposure.granular.non_appearance.num_band_members_mod
            ,"na.claim_experience":                                                 cds.exposure.granular.non_appearance.claim_experience
            ,"na.mod_claim_experience":                                             cds.exposure.granular.non_appearance.claim_experience_mod
            ,"na.mod_nmp":                                                          cds.exposure.granular.non_appearance.nmp_mod
            ,"na.el_fgu_mod":                                                       cds.exposure.granular.non_appearance.el_fgu_mod
            ,"na.mod_total":                                                        cds.exposure.granular.non_appearance.total_mod

            ,"na.curve":                                                            cds.exposure.granular.non_appearance.fl_curve

            ,"na.uw_adj_min":                                                       cds.exposure.granular.non_appearance.uw_adj_min
            ,"na.uw_adj_selected":                                                  cds.exposure.granular.non_appearance.uw_adj_sel
            ,"na.uw_adj_max":                                                       cds.exposure.granular.non_appearance.uw_adj_max
            ,"na.uw_adj_final":                                                     cds.exposure.granular.non_appearance.uw_adj_fin

            ,"na.comment":                                                          cds.exposure.granular.non_appearance.uw_comment
            }
    return data   


def dict_sclr_experience_rating(hxd):
    cds  = hxd.cds
    data = {
             "exper.eval_date_est":                                                 cds.experience_rating.evaluation_date_calc
            ,"exper.eval_date_ovd":                                                 cds.experience_rating.evaluation_date_ovd
            
            ,"exper.el_calc":                                                       cds.experience_rating.el_final_calc
            ,"exper.el_ovd":                                                        cds.experience_rating.el_final_ovd
            ,"exper.el_sel":                                                        cds.experience_rating.el_final
            ,"exper.wgt_calc":                                                      cds.experience_rating.el_weight_calc
            ,"exper.wgt_ovd":                                                       cds.experience_rating.el_weight_ovd
            ,"exper.wgt_sel":                                                       cds.experience_rating.el_weight

            ,"exper.bi_status_last":                                                cds.bi.last_run_status
            ,"exper.bi_date_last":                                                  cds.bi.last_run_date
            ,"exper.bi_val_last":                                                   cds.bi.last_run_value
            ,"exper.bi_val_calc":                                                   cds.bi.calc_run_value
            ,"exper.bi_rerun":                                                      cds.bi.check_run_consistent

            ,"exper.trend_backfill":                                                cds.experience_rating.exposure_trend_backfill

            ,"exper.tbl_overall_total_year":                                        cds.experience_rating.analysis_table_total_included.yoa_label
            ,"exper.tbl_overall_total_tiv_calc":                                    cds.experience_rating.analysis_table_total_included.tiv_calc
            ,"exper.tbl_overall_total_tiv_ovd":                                     cds.experience_rating.analysis_table_total_included.tiv_ovd
            ,"exper.tbl_overall_total_gnol_p":                                      cds.experience_rating.analysis_table_total_included.gnwp_ol_dup
            ,"exper.tbl_overall_total_gnol_el":                                     cds.experience_rating.analysis_table_total_included.total_ol_selected_ultimate_dup
            ,"exper.tbl_overall_total_gnol_lr":                                     cds.experience_rating.analysis_table_total_included.total_ol_selected_ulr_dup
            # ,"exper.tbl_overall_total_gnol_el_to_tiv":                              cds.experience_rating.analysis_table_total_included.total_ol_selected_ult_to_tiv


            ,"exper.tbl_project_total_year":                                        cds.experience_rating.analysis_table_total.yoa_label
            ,"exper.tbl_project_total_gnol_p":                                      cds.experience_rating.analysis_table_total.gnwp_ol
            ,"exper.tbl_project_total_gnol_el_attr":                                cds.experience_rating.analysis_table_total.attr_ol_incurred
            ,"exper.tbl_project_total_gnol_el_large":                               cds.experience_rating.analysis_table_total.large_ol_incurred
            ,"exper.tbl_project_total_gnol_el_cat":                                 cds.experience_rating.analysis_table_total.cat_ol_incurred
                                             
            ,"exper.tbl_project_total_attr_cl_lr":                                  cds.experience_rating.analysis_table_total.attr_ol_cl_lr
            ,"exper.tbl_project_total_attr_bf_lr":                                  cds.experience_rating.analysis_table_total.attr_ol_bf_lr
            ,"exper.tbl_project_total_attr_ielr":                                   cds.experience_rating.analysis_table_total.attr_ol_ielr
            ,"exper.tbl_project_total_attr_ultimate":                               cds.experience_rating.analysis_table_total.attr_ol_selected_ultimate
            ,"exper.tbl_project_total_attr_ulr":                                    cds.experience_rating.analysis_table_total.attr_ol_selected_ulr

            ,"exper.tbl_project_total_large_cl_lr":                                 cds.experience_rating.analysis_table_total.large_ol_cl_lr
            ,"exper.tbl_project_total_large_ielr":                                  cds.experience_rating.analysis_table_total.large_ol_ielr
            ,"exper.tbl_project_total_large_ultimate":                              cds.experience_rating.analysis_table_total.large_ol_selected_ultimate
            ,"exper.tbl_project_total_large_ulr":                                   cds.experience_rating.analysis_table_total.large_ol_selected_ulr

            ,"exper.tbl_project_total_cat_cl_lr":                                   cds.experience_rating.analysis_table_total.cat_ol_cl_lr
            ,"exper.tbl_project_total_cat_ielr":                                    cds.experience_rating.analysis_table_total.cat_ol_ielr
            ,"exper.tbl_project_total_cat_ultimate":                                cds.experience_rating.analysis_table_total.cat_ol_selected_ultimate
            ,"exper.tbl_project_total_cat_ulr":                                     cds.experience_rating.analysis_table_total.cat_ol_selected_ulr

            ,"exper.tbl_project_total_total_ultimate":                              cds.experience_rating.analysis_table_total.total_ol_selected_ultimate
            ,"exper.tbl_project_total_total_ulr":                                   cds.experience_rating.analysis_table_total.total_ol_selected_ulr


            ,"exper.tbl_actuarial_total_year":                                      cds.experience_rating.analysis_table_total.yoa_label
            ,"exper.tbl_actuarial_total_gnol_p":                                    cds.experience_rating.analysis_table_total.gnwp_ol
            ,"exper.tbl_actuarial_total_gnol_el_attr":                              cds.experience_rating.analysis_table_total.attr_ol_incurred
            ,"exper.tbl_actuarial_total_gnol_el_large":                             cds.experience_rating.analysis_table_total.large_ol_incurred
            ,"exper.tbl_actuarial_total_gnol_el_cat":                               cds.experience_rating.analysis_table_total.cat_ol_incurred
            ,"exper.tbl_actuarial_total_gnol_el_total":                             cds.experience_rating.analysis_table_total.total_ol_incurred
                                                              
            ,"exper.tbl_actuarial_total_attr_cl_ultimate":                          cds.experience_rating.analysis_table_total.attr_ol_cl_ultimate
            ,"exper.tbl_actuarial_total_attr_bf_ultimate":                          cds.experience_rating.analysis_table_total.attr_ol_bf_ultimate
            ,"exper.tbl_actuarial_total_attr_ie_ultimate":                          cds.experience_rating.analysis_table_total.attr_ol_ielr_ultimate
            ,"exper.tbl_actuarial_total_attr_cl_lr":                                cds.experience_rating.analysis_table_total.attr_ol_cl_lr
            ,"exper.tbl_actuarial_total_attr_bf_lr":                                cds.experience_rating.analysis_table_total.attr_ol_bf_lr
            ,"exper.tbl_actuarial_total_attr_ielr":                                 cds.experience_rating.analysis_table_total.attr_ol_ielr
            ,"exper.tbl_actuarial_total_attr_ultimate":                             cds.experience_rating.analysis_table_total.attr_ol_selected_ultimate
            ,"exper.tbl_actuarial_total_attr_ulr":                                  cds.experience_rating.analysis_table_total.attr_ol_selected_ulr
                                                              
            ,"exper.tbl_actuarial_total_large_cl_ultimate":                         cds.experience_rating.analysis_table_total.large_ol_cl_ultimate
            ,"exper.tbl_actuarial_total_large_bf_ultimate":                         cds.experience_rating.analysis_table_total.large_ol_bf_ultimate
            ,"exper.tbl_actuarial_total_large_ie_ultimate":                         cds.experience_rating.analysis_table_total.large_ol_ielr_ultimate
            ,"exper.tbl_actuarial_total_large_cl_lr":                               cds.experience_rating.analysis_table_total.large_ol_cl_lr
            ,"exper.tbl_actuarial_total_large_bf_lr":                               cds.experience_rating.analysis_table_total.large_ol_bf_lr
            ,"exper.tbl_actuarial_total_large_ielr":                                cds.experience_rating.analysis_table_total.large_ol_ielr
            ,"exper.tbl_actuarial_total_large_ultimate":                            cds.experience_rating.analysis_table_total.large_ol_selected_ultimate
            ,"exper.tbl_actuarial_total_large_ulr":                                 cds.experience_rating.analysis_table_total.large_ol_selected_ulr
                                              
            ,"exper.tbl_actuarial_total_cat_cl_ultimate":                           cds.experience_rating.analysis_table_total.cat_ol_cl_ultimate
            ,"exper.tbl_actuarial_total_cat_bf_ultimate":                           cds.experience_rating.analysis_table_total.cat_ol_bf_ultimate
            ,"exper.tbl_actuarial_total_cat_ie_ultimate":                           cds.experience_rating.analysis_table_total.cat_ol_ielr_ultimate
            ,"exper.tbl_actuarial_total_cat_cl_lr":                                 cds.experience_rating.analysis_table_total.cat_ol_cl_lr
            ,"exper.tbl_actuarial_total_cat_bf_lr":                                 cds.experience_rating.analysis_table_total.cat_ol_bf_lr
            ,"exper.tbl_actuarial_total_cat_ielr":                                  cds.experience_rating.analysis_table_total.cat_ol_ielr
            ,"exper.tbl_actuarial_total_cat_ultimate":                              cds.experience_rating.analysis_table_total.cat_ol_selected_ultimate
            ,"exper.tbl_actuarial_total_cat_ulr":                                   cds.experience_rating.analysis_table_total.cat_ol_selected_ulr
                                              
            ,"exper.tbl_actuarial_total_total_cl_ultimate":                         cds.experience_rating.analysis_table_total.total_ol_cl_ultimate
            ,"exper.tbl_actuarial_total_total_bf_ultimate":                         cds.experience_rating.analysis_table_total.total_ol_bf_ultimate
            ,"exper.tbl_actuarial_total_total_ie_ultimate":                         cds.experience_rating.analysis_table_total.total_ol_ielr_ultimate
            ,"exper.tbl_actuarial_total_total_ultimate":                            cds.experience_rating.analysis_table_total.total_ol_selected_ultimate
            ,"exper.tbl_actuarial_total_total_cl_lr":                               cds.experience_rating.analysis_table_total.total_ol_cl_lr
            ,"exper.tbl_actuarial_total_total_bf_lr":                               cds.experience_rating.analysis_table_total.total_ol_bf_lr
            ,"exper.tbl_actuarial_total_total_ielr":                                cds.experience_rating.analysis_table_total.total_ol_ielr
            ,"exper.tbl_actuarial_total_total_ulr":                                 cds.experience_rating.analysis_table_total.total_ol_selected_ulr
            }
    return data   


def dict_sclr_rat_sum(hxd):
    cds  = hxd.cds
    data = {
             "rs.rater_priced":                                                     cds.standard_fields.rating_methodology

            ,"rs.clmnum_calc":                                                      cds.exposure.granular.event_cancel.simulation.total_sim_claim_number_calc
            ,"rs.clmnum_ovd":                                                       cds.exposure.granular.event_cancel.simulation.total_sim_claim_number_override
            ,"rs.clmnum_sim":                                                       cds.exposure.granular.event_cancel.simulation.total_sim_claim_number
            ,"rs.sim_last_status":                                                  cds.exposure.granular.event_cancel.simulation.last_run_status
            ,"rs.sim_check_calc":                                                   cds.exposure.granular.event_cancel.simulation.calc_run_value
            ,"rs.sim_check_last":                                                   cds.exposure.granular.event_cancel.simulation.last_run_value
            ,"rs.sim_rerun":                                                        cds.exposure.granular.event_cancel.simulation.check_run_consistent
            ,"rs.sim_el_uncap":                                                     cds.exposure.granular.event_cancel.simulation.total_sim_loss_before_agg
            ,"rs.sim_el_cap":                                                       cds.exposure.granular.event_cancel.simulation.total_sim_loss_after_agg
            ,"rs.sim_el_adj":                                                       cds.exposure.granular.event_cancel.simulation.total_sim_loss_after_agg_adj
            ,"rs.sim_el_scaled":                                                    cds.exposure.granular.event_cancel.simulation.total_sim_loss_after_agg_adj_scaled
            ,"rs.det_el_uncap":                                                     cds.exposure.granular.event_cancel.simulation.total_det_loss_before_agg
            ,"rs.det_el_cap":                                                       cds.exposure.granular.event_cancel.simulation.total_det_loss_after_agg
            ,"rs.det_el_adj":                                                       cds.exposure.granular.event_cancel.simulation.total_det_loss_after_agg_adj
            ,"rs.sim_error":                                                        cds.exposure.granular.event_cancel.simulation.sim_error
            ,"rs.num_sims":                                                         cds.exposure.granular.event_cancel.simulation.num_sims
            ,"rs.agg_adj":                                                          cds.exposure.granular.event_cancel.simulation.sim_agg_adj

            ,"rs.status":                                                           cds.layers[0].status
            ,"rs.currency":                                                         cds.currencies.source_currency
            ,"rs.brokerage":                                                        cds.layers[0].brokerage
            ,"rs.written_line":                                                     cds.layers[0].written_line
            ,"rs.limit":                                                            cds.layers[0].coverages.ec_total.limit
            ,"rs.agg_limit":                                                        cds.layers[0].coverages.ec_total.aggregate_limit
            ,"rs.use_excess":                                                       cds.layers[0].coverages.ec_total.excess_use
            ,"rs.excess":                                                           cds.layers[0].coverages.ec_total.excess                 
            ,"rs.deductible":                                                       cds.layers[0].coverages.ec_total.deductible
            ,"rs.deductible_agg":                                                   cds.layers[0].coverages.ec_total.aggregate_deductible

            ,"rs.quoted_premium_100":                                               cds.layers[0].quoted_premium_100
            ,"rs.quoted_premium_afb":                                               cds.layers[0].quoted_premium
            ,"rs.quoted_rol":                                                       cds.layers[0].quoted_rol
            ,"rs.bench_premium_100":                                                cds.layers[0].benchmark_premium_100
            ,"rs.bench_premium_afb":                                                cds.layers[0].benchmark_premium
            ,"rs.quoted_roe":                                                       cds.layers[0].quoted_roe
            ,"rs.tech_premium_100":                                                 cds.layers[0].technical_premium_100
            ,"rs.tech_premium_afb":                                                 cds.layers[0].technical_premium

            ,"rs.bpi":                                                              cds.layers[0].bpi
            ,"rs.pflr":                                                             cds.layers[0].pflr
            ,"rs.uw_adj":                                                           cds.layers[0].uw_adj_impact
            ,"rs.tpi":                                                              cds.layers[0].tpi
            ,"rs.tpi_pre":                                                          cds.layers[0].tpi_pre_uw_adj
            ,"rs.roc":                                                              cds.layers[0].roc
            }
    return data   


def dict_sclr_other(hxd):
    cds  = hxd.cds
    data = {
             "rc.uw_rationale":                                                     cds.standard_fields.uw_rationale
            ,"rc.expiring_id":                                                      cds.rate_change.expiring_policy_option_id.selected
            ,"rc.actuarial_reviewed":                                               cds.rationale.actuarial_review
            ,"rc.actuarial_rationale":                                              cds.rationale.actuarial_notes
            }
    return data   


# converts to dictionary from structure
def dict_tbl_ec_coverage(hxd):
    path_root        = hxd.cds.exposure.granular.event_cancel.base_coverages
    data             = []
    for structure in CVG_LST:
        path = getattr(path_root,structure)
        data.append({
            "covered":              path.covered        if structure not in ["all_risks"                                         ] else ""
            ,"sublimit":            path.sublimit       if structure not in ["all_risks"                                         ] else ""
            ,"trigger":             path.trigger        if structure     in ["cyber", "national_mourning", "catastrophic_non_app"] else ""
            ,"delegates":           path.delegates      if structure     in [                              "catastrophic_non_app"] else ""
            ,"uw_adj_min":          path.uw_adj_min
            ,"uw_adj_sel":          path.uw_adj_sel
            ,"uw_adj_max":          path.uw_adj_max
            ,"uw_adj_fin":          path.uw_adj_fin
            ,"uw_comment":          path.uw_comment
            ,"blank1":              None
            ,"net_el_usd":          path.net_el_usd
            ,"net_el":              path.net_el
            ,"net_el_mod":          path.net_el_mod
        })
    return data   


# converts to dictionary from list
def dict_tbl_ec_event_table(hxd):
    intended_cols    = ["event_name"       ,"country"                          ,"state"    
                        ,"date_start"       ,"date_end"                         ,"tiv"          ,"venue"        ,"check"
                        ,"blank"
                        ,"ihs_terrorism"    ,"ihs_riots_and_civil_commotion"    ,"ihs_strike"    ,"ihs_war"                 ]
    intended_lst     = hxd.cds.exposure.granular.event_cancel.events
    return list_converter(intended_lst, col_order=intended_cols)


# converts to dictionary from list
def dict_tbl_nm_o75_table(hxd):
    intended_cols    = [  "include"     , "name"         , "country"      , "gender"     , "date_of_birth", "age"
                        , "prob_die"    , "prob_live"    , "mod_affluence", "mod_health"
                        , "prob_die_mod", "prob_live_mod", "check"]
    intended_lst     = hxd.cds.exposure.granular.event_cancel.national_mourning.over_75
    return list_converter(intended_lst, col_order=intended_cols)


# converts to dictionary from list
def dict_tbl_exper_overall(hxd):
    # prior year data
    intended_lst     = hxd.cds.experience_rating.analysis_table
    intended_cols    = [  "yoa_label"   ,"include"   ,"tiv_calc"    ,"tiv_ovd"      ,"gnwp_ol_dup"
                        , "total_ol_selected_ultimate_dup"  ,"total_ol_selected_ulr_dup"    ,"total_ol_selected_ult_to_tiv"]
    py_data          = list_converter(intended_lst, col_order=intended_cols)

    # current year data
    cy_cols = [ "yoa_label", "tiv_calc"]
    cy_path = hxd.cds.experience_rating.analysis_table_cy
    cy_data = { col: getattr(cy_path, col) if col in cy_cols else ""
                    for col in intended_cols    }

    return py_data + [cy_data]


# converts to dictionary from list
def dict_tbl_exper_assump(hxd):
    # prior year data
    intended_lst     = hxd.cds.experience_rating.analysis_table
    intended_cols    = [ "yoa_label"
                        ,"gnwp_nominal_calc"        ,"gnwp_nominal_ovd"
                        ,"attr_incurred_calc"       ,"attr_incurred_ovd"
                        ,"large_incurred_calc"      ,"large_incurred_ovd"
                        ,"cat_incurred_calc"        ,"cat_incurred_ovd"
                        ,"rate_inc_calc"            ,"rate_inc_ovd"             ,"rate_inc"         ,"rate_cum"
                        ,"inf_inc_calc"             ,"inf_inc_ovd"              ,"inf_inc"          ,"inf_cum"
                        ,"attr_pct_ultimate_calc"   ,"attr_pct_ultimate_ovd"    ,"attr_ielr_calc"   ,"attr_ielr_ovd" 
                        ,"large_pct_ultimate_calc"  ,"large_pct_ultimate_ovd"   ,"large_ielr_calc"  ,"large_ielr_ovd"
                        ,"cat_pct_ultimate_calc"    ,"cat_pct_ultimate_ovd"     ,"cat_ielr_calc"    ,"cat_ielr_ovd" ]

    py_data          = list_converter(intended_lst, col_order=intended_cols)

    # current year data
    cy_cols = [ "yoa_label", "rate_inc_calc"    ,"rate_inc" ,"rate_cum" ,"inf_inc_calc" ,"inf_inc"  ,"inf_cum"]
    cy_path = hxd.cds.experience_rating.analysis_table_cy
    cy_data = { col: getattr(cy_path, col) if col in cy_cols else ""
                    for col in intended_cols    }

    return py_data + [cy_data]


# converts to dictionary from list
def dict_tbl_exper_project(hxd):
    # prior year data
    intended_lst     = hxd.cds.experience_rating.analysis_table
    intended_cols    = [ "yoa_label"
                        ,"gnwp_ol"   ,"attr_ol_incurred" ,"large_ol_incurred"    ,"cat_ol_incurred"
                        ,"attr_pct_ultimate"            ,"attr_ol_cl_lr"        ,"attr_ol_bf_lr"    ,"attr_ol_ielr" ,"attr_method"
                        ,"attr_ol_selected_ultimate"    ,"attr_ol_selected_ulr"
                        ,"large_ol_cl_lr"               ,"large_ol_ielr"        ,"large_method"
                        ,"large_ol_selected_ultimate"   ,"large_ol_selected_ulr"
                        ,"cat_ol_cl_lr"                 ,"cat_ol_ielr"          ,"cat_method"
                        ,"cat_ol_selected_ultimate"     ,"cat_ol_selected_ulr"
                        ,"total_ol_selected_ultimate"   ,"total_ol_selected_ulr"    ]

    data             = list_converter(intended_lst, col_order=intended_cols)
    return data


# converts to dictionary from list
def dict_tbl_exper_actuarial_project(hxd):
    # prior year data
    intended_lst     = hxd.cds.experience_rating.analysis_table
    intended_cols    = [ "yoa_label"
                        ,"gnwp_ol"           ,"attr_ol_incurred"     ,"large_ol_incurred"    ,"cat_ol_incurred"          ,"total_ol_incurred"
                        ,"attr_pct_ultimate" ,"attr_ol_cl_ultimate"  ,"attr_ol_bf_ultimate"  ,"attr_ol_ielr_ultimate"    ,"attr_ol_cl_lr"
                        ,"attr_ol_bf_lr"     ,"attr_ol_ielr"         ,"attr_method"          ,"attr_ol_selected_ultimate","attr_ol_selected_ulr"
                        ,"large_pct_ultimate","large_ol_cl_ultimate" ,"large_ol_bf_ultimate" ,"large_ol_ielr_ultimate"   ,"large_ol_cl_lr"
                        ,"large_ol_bf_lr"    ,"large_ol_ielr"        ,"large_method"         ,"large_credibility"        ,"large_ol_selected_ultimate"   ,"large_ol_selected_ulr"
                        ,"cat_pct_ultimate"  ,"cat_ol_cl_ultimate"   ,"cat_ol_bf_ultimate"   ,"cat_ol_ielr_ultimate"     ,"cat_ol_cl_lr"
                        ,"cat_ol_bf_lr"      ,"cat_ol_ielr"          ,"cat_method"           ,"cat_ol_selected_ultimate" ,"cat_ol_selected_ulr"
                        ,"total_pct_ultimate","total_ol_cl_ultimate" ,"total_ol_bf_ultimate" ,"total_ol_ielr_ultimate"   ,"total_ol_selected_ultimate"
                        ,"total_ol_cl_lr"    ,"total_ol_bf_lr"       ,"total_ol_ielr"        ,"total_ol_selected_ulr"
                        ,"wgt_include","wgt_decay","wgt_exposure","wgt_pct_ult","wgt_overall_initial","wgt_overall_final" ]
    data             = list_converter(intended_lst, col_order=intended_cols)
    return data


# converts to dictionary from structure
def dict_tbl_metrics_post(hxd):
    FIELDS_POST_UW_ADJ = [  "section_reference",
                            "quoted_premium_100",
                            "quoted_rol",
                            "quoted_roe",
                            "technical_premium_100",
                            "technical_rol",
                            "tpi",
                            "benchmark_premium_100",
                            "benchmark_rol",
                            "bpi",
                            "pflr"    ]

    data     = []
    path     = hxd.cds.layers[0]
    cvg_path = path.coverages

    for fld in FIELDS_POST_UW_ADJ:
        data_row             = {}                                       # reset data_row
        data_row['overall']  = getattr(path,                   fld)     # add totals
        na_fld               = getattr(cvg_path.na_total,      fld)
        if fld == "section_reference":
            na_fld           = na_fld.selected                          # handling the na section ref switching to an override field
        data_row['na_total'] = na_fld
        data_row['ec_total'] = getattr(cvg_path.ec_total,      fld)
        for cvg in CVG_LST:                                             # add standard ec coverages
            data_row[cvg]    = getattr(getattr(cvg_path, cvg), fld) 

        data.append(data_row)                                           # append row
    return data   


# converts to dictionary from structure
def dict_tbl_metrics_pre(hxd):
    FIELDS_PRE_UW_ADJ  = [  "technical_premium_pre_uw_adj_100",
                            "technical_rol_pre_uw_adj",
                            "tpi_pre_uw_adj",
                            "benchmark_premium_pre_uw_adj_100",
                            "benchmark_rol_pre_uw_adj",
                            "bpi_pre_uw_adj",
                            "pflr_pre_uw_adj"  ]

    data     = []
    path     = hxd.cds.layers[0]
    cvg_path = path.coverages

    for fld in FIELDS_PRE_UW_ADJ:
        data_row             = {}                                       # reset data_row
        data_row['overall']  = getattr(path,                   fld)     # add totals
        data_row['na_total'] = getattr(cvg_path.na_total,      fld)
        data_row['ec_total'] = getattr(cvg_path.ec_total,      fld)
        for cvg in CVG_LST:                                             # add standard ec coverages
            data_row[cvg]    = getattr(getattr(cvg_path, cvg), fld) 

        data.append(data_row)                                           # append row
    return data   


# converts to dictionary from structure
def dict_tbl_metrics_el(hxd):
    FIELDS_LOSS_COSTS  = [  "loss_cost_layer_adj",
                            "agg_adjustment", 
                            "loss_cost_layer_agg_adj",
                            "uw_adjustment",
                            "loss_cost_layer_agg_uw_adj",
                            "experience_weight",
                            "experience_loss_cost",
                            "blended_loss_cost_no_uw_adj",
                            "blended_loss_cost"             ]

    data     = []
    path     = hxd.cds.layers[0]
    cvg_path = path.coverages

    for fld in FIELDS_LOSS_COSTS:
        data_row             = {}                                       # reset data_row
        data_row['overall']  = getattr(path,                   fld)     # add totals
        data_row['na_total'] = getattr(cvg_path.na_total,      fld)
        data_row['ec_total'] = getattr(cvg_path.ec_total,      fld)
        for cvg in CVG_LST:                                             # add standard ec coverages
            data_row[cvg]    = getattr(getattr(cvg_path, cvg), fld) 

        data.append(data_row)                                           # append row
    return data   


# converts to dictionary from structure
def dict_tbl_rc_profile(hxd):
    FIELDS  = [ "currency",
                "premium.line_100pct.annualised",
                "premium.beazley_line.annualised",
                "limit",
                "deductible",
                "excess",
                "brokerage" ]

    data     = []

    for fld in FIELDS:
        data_row                     = {}                                                # reset data_row
        data_path                    = rgetattr(hxd.cds.layers[0].rate_change,  fld)     # determine path
        data_row['expiring']         = data_path.expiring                                # assign values
        data_row['expiring_revalued']= data_path.expiring_revalued
        data_row['renewal']          = data_path.renewal
        data.append(data_row)                                                            # append row

    return data   


# converts to dictionary from structure
def dict_tbl_rc_drivers(hxd):
    FIELDS  = [ "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                "rate_change"]

    data     = []

    for fld in FIELDS:
        data_row                     = {}                                                # reset data_row
        data_path                    = rgetattr(hxd.cds.layers[0].rate_change,  fld)     # determine path
        data_row['model_calculated'] = data_path.model_calculated                        # assign values
        data_row['uw_override']      = data_path.uw_override
        data_row['final']            = data_path.final
        data_row['comments']         = data_path.comments
        data.append(data_row)                                                            # append row

    return data   


# converts to dictionary from list
def dict_tbl_actuarial_event(hxd):
    intended_cols    = [    "event_name",
                            "country",
                            "state",
                            "date_start",
                            "date_end",
                            "tiv",
                            "venue",
                            "ihs_terrorism",
                            "ihs_riots_and_civil_commotion",
                            "ihs_strike",
                            "ihs_war",
                            "check",
                            "country_code",
                            "date_cover_start",
                            "mths_diff",
                            "venue_multiplier",
                            "tiv_usd",
                            "cap_tiv_usd",
                            "m_terrorism",
                            "c_terrorism",
                            "m_riots_and_civil_commotion",
                            "c_riots_and_civil_commotion",
                            "m_strike",
                            "c_strike",
                            "m_war",
                            "c_war",
                            "base_rate_adverse_weather",
                            "pat_adverse_weather",
                            "base_rate_windstorm",
                            "pat_windstorm",
                            "base_rate_wildfire",
                            "pat_wildfire",
                            "base_rate_earthquake",
                            "pat_earthquake",
                            "season_adverse_weather",
                            "season_windstorm",
                            "season_wildfire",
                            "nm_o75_sx",
                            "nm_o75_sx_mod",
                            "nm_u75_sx",
                            "nm_sx",
                            "nm_qx",
                            "nm_qx_daily",
                            "nm_u75_sx_mod",
                            "nm_sx_mod",
                            "nm_qx_mod",
                            "nm_qx_daily_mod",
                            "nm_death_rate",
                            "nm_funeral_rate",
                            "nm_mourning_rate",
                            "nm_rate",
                            "nm_death_rate_mod",
                            "nm_funeral_rate_mod",
                            "nm_mourning_rate_mod",
                            "nm_rate_mod",
                            "rate_all_risks",
                            "rate_adverse_weather",
                            "rate_windstorm",
                            "rate_wildfire",
                            "rate_earthquake",
                            "rate_cyber",
                            "rate_national_mourning",
                            "rate_national_mourning_mod",
                            "rate_terrorism",
                            "rate_riots_and_civil_commotion",
                            "rate_strike",
                            "rate_war",
                            "rate_catastrophic_non_app",
                            "el_usd_total",
                            "net_el_usd_total",
                            "struct_pct_all_risks",
                            "el_usd_all_risks",
                            "net_el_usd_all_risks",
                            "struct_pct_terrorism",
                            "el_usd_terrorism",
                            "net_el_usd_terrorism",
                            "struct_pct_cyber",
                            "el_usd_cyber",
                            "net_el_usd_cyber",
                            "struct_pct_national_mourning",
                            "el_usd_national_mourning",
                            "net_el_usd_national_mourning",
                            "struct_pct_riots_and_civil_commotion",
                            "el_usd_riots_and_civil_commotion",
                            "net_el_usd_riots_and_civil_commotion",
                            "struct_pct_strike",
                            "el_usd_strike",
                            "net_el_usd_strike",
                            "struct_pct_war",
                            "el_usd_war",
                            "net_el_usd_war",
                            "struct_pct_catastrophic_non_app",
                            "el_usd_catastrophic_non_app",
                            "net_el_usd_catastrophic_non_app",
                            "struct_pct_adverse_weather",
                            "el_usd_adverse_weather",
                            "net_el_usd_adverse_weather",
                            "struct_pct_windstorm",
                            "el_usd_windstorm",
                            "net_el_usd_windstorm",
                            "struct_pct_wildfire",
                            "el_usd_wildfire",
                            "net_el_usd_wildfire",
                            "struct_pct_earthquake",
                            "el_usd_earthquake",
                            "net_el_usd_earthquake",
                            "el_usd_national_mourning_mod",
                            "net_el_usd_national_mourning_mod"    ]
    intended_lst     = hxd.cds.exposure.granular.event_cancel.events
    return list_converter(intended_lst, col_order=intended_cols)   


# converts to dictionary from list
def dict_tbl_actuarial_nm(hxd):
    intended_cols    = ["label",
                        "include",
                        "name",
                        "country",
                        "gender",
                        "date_of_birth",
                        "age",
                        "prob_die",
                        "prob_live",
                        "mod_affluence",
                        "mod_health",
                        "prob_die_mod",
                        "prob_live_mod",
                        "check"]
    intended_lst     = hxd.cds.exposure.granular.event_cancel.national_mourning.over_75
    return list_converter(intended_lst, col_order=intended_cols)   


# converts to dictionary from list
def dict_tbl_actuarial_experience_analysis(hxd):
    intended_cols    = ["yoa",
                        "yoa_label",
                        "include",
                        "tiv_calc",
                        "tiv_ovd",
                        "tiv",
                        "gnwp_ol_dup",
                        "total_ol_selected_ultimate_dup",
                        "total_ol_selected_ulr_dup",
                        "total_ol_selected_ult_to_tiv",
                        "gnwp_nominal_calc",
                        "gnwp_nominal_ovd",
                        "gnwp_nominal",
                        "attr_incurred_calc",
                        "attr_incurred_ovd",
                        "attr_incurred",
                        "large_incurred_calc",
                        "large_incurred_ovd",
                        "large_incurred",
                        "cat_incurred_calc",
                        "cat_incurred_ovd",
                        "cat_incurred",
                        "rate_inc_calc",
                        "rate_inc_ovd",
                        "rate_inc",
                        "rate_cum",
                        "inf_inc_calc",
                        "inf_inc_ovd",
                        "inf_inc",
                        "inf_cum",
                        "attr_pct_ultimate_calc",
                        "attr_pct_ultimate_ovd",
                        "large_pct_ultimate_calc",
                        "large_pct_ultimate_ovd",
                        "cat_pct_ultimate_calc",
                        "cat_pct_ultimate_ovd",
                        "attr_ielr_calc",
                        "attr_ielr_ovd",
                        "large_ielr_calc",
                        "large_ielr_ovd",
                        "cat_ielr_calc",
                        "cat_ielr_ovd",
                        "gnwp_ol",
                        "attr_ol_incurred",
                        "large_ol_incurred",
                        "cat_ol_incurred",
                        "total_ol_incurred",
                        "attr_pct_ultimate",
                        "attr_method",
                        "attr_ol_cl_ultimate",
                        "attr_ol_bf_ultimate",
                        "attr_ol_ielr_ultimate",
                        "attr_ol_selected_ultimate",
                        "attr_ol_cl_lr",
                        "attr_ol_bf_lr",
                        "attr_ol_ielr",
                        "attr_ol_selected_ulr",
                        "large_pct_ultimate",
                        "large_method",
                        "large_credibility",
                        "large_ol_cl_ultimate",
                        "large_ol_bf_ultimate",
                        "large_ol_ielr_ultimate",
                        "large_ol_selected_ultimate",
                        "large_ol_cl_lr",
                        "large_ol_bf_lr",
                        "large_ol_ielr",
                        "large_ol_selected_ulr",
                        "cat_pct_ultimate",
                        "cat_method",
                        "cat_ol_cl_ultimate",
                        "cat_ol_bf_ultimate",
                        "cat_ol_ielr_ultimate",
                        "cat_ol_selected_ultimate",
                        "cat_ol_cl_lr",
                        "cat_ol_bf_lr",
                        "cat_ol_ielr",
                        "cat_ol_selected_ulr",
                        "total_pct_ultimate",
                        "total_ol_cl_ultimate",
                        "total_ol_bf_ultimate",
                        "total_ol_ielr_ultimate",
                        "total_ol_selected_ultimate",
                        "total_ol_cl_lr",
                        "total_ol_bf_lr",
                        "total_ol_ielr",
                        "total_ol_selected_ulr",
                        "wgt_include",
                        "wgt_decay",
                        "wgt_exposure",
                        "wgt_pct_ult",
                        "wgt_overall_initial",
                        "wgt_overall_final"]
    intended_lst     = hxd.cds.experience_rating.analysis_table
    return list_converter(intended_lst, col_order=intended_cols)   


# converts to dictionary from list
def dict_tbl_actuarial_policy(hxd):
    intended_cols    = ["policy_ref",
                        "section_ref",
                        "yoa",
                        "coverage_name",
                        "trifocus_name",
                        "division",
                        "settlement_fx",
                        "index_bzly",
                        "class_code",
                        "bool_ec",
                        "bool_na",
                        "gnwp_bzly_usd",
                        "incurred_bzly_usd",
                        "gnwp_100_usd",
                        "incurred_100_usd",
                        "share_bzly",
                        "rate_chg_init",
                        "rate_chg",
                        "fx_rate_usd_sett",
                        "gnwp_bzly",
                        "incurred_bzly",
                        "gnwp_100",
                        "incurred_100",
                        "gnwp_bzly_scc",
                        "incurred_bzly_scc",
                        "gnwp_100_scc",
                        "incurred_100_scc"]
    intended_lst     = hxd.cds.experience_rating.policy_table
    return list_converter(intended_lst, col_order=intended_cols)   


# converts to dictionary from list
def dict_tbl_actuarial_claim(hxd):
    intended_cols    = ["policy_ref",
                        "section_ref",
                        "claim_ref",
                        "trifocus_name",
                        "division",
                        "yoa",
                        "settlement_fx",
                        "cat_code_bzly",
                        "cat_desc_bzly",
                        "cat_code_mkt",
                        "cat_desc_mkt",
                        "cat_bzly_bool",
                        "cause_of_loss",
                        "bool_covid",
                        "index_bzly",
                        "class_code",
                        "bool_ec",
                        "bool_na",
                        "bool_large",
                        "incurred_bzly",
                        "os_bzly",
                        "incurred_100",
                        "share_bzly",
                        "incurred_bzly_scc",
                        "os_bzly_scc",
                        "incurred_100_scc",
                        "incurred_100_scc_attr",
                        "incurred_100_scc_large",
                        "incurred_100_scc_cat"    ]
    intended_lst     = hxd.cds.experience_rating.claim_table
    return list_converter(intended_lst, col_order=intended_cols)   


###########################################################################################################
#### CODE TO FORMAT AND COMBINE
###########################################################################################################


# Format data in dictionary for Excel
def clean_data_for_policy_doc(data):
    dates_lst = ["ri.expiry_date"       ,"ri.inception_date"
                ,"nm.o75_b1_dob"        ,"nm.o75_b2_dob"        ,"date_of_birth"        # national mourning
                ,"exper.eval_date_est"  ,"exper.eval_date_ovd"                          # experience analysis
                ,"date_start"           ,"date_end"             ,"date_cover_start"     # events table
    ]   # allow more generic specification of dates
    for key, value in data.items():
        if isinstance(value, list):                             # non-standard added such that algo pushes into list being passed and allows steps below then to apply
            for lst_value in value:                             # as above
                clean_data_for_policy_doc(lst_value)            # as above
        elif value is None:
            data[key] = ""
        elif value is True:
            data[key] = "Yes"
        elif value is False:
            data[key] = "No"
        elif key in dates_lst:
            date_str = str(value)
            data[key] = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    return data


# Convert hx_list to a dictionary of lists
def list_converter(hx_list, col_order = []):
    df = pd_df_from_hx_list(hx_list)
    if col_order:
        df = df.reindex(columns=col_order)

    dict_of_lists = df.to_dict(orient='records')

    return dict_of_lists



# Create data dictionary to write to Excel file
def create_dict_for_excel(hxd):
   
    ##########################################################################################
    ### customised code to push merged dictionaries and additional tables expressed as nested dictionary
    ##########################################################################################

    # Add scalar fields below
    data    = (    dict_sclr_risk_info(hxd)  
                |  dict_sclr_exposure(hxd)  
                |  dict_sclr_national_mourning(hxd)  
                |  dict_sclr_non_appearance(hxd)
                |  dict_sclr_experience_rating(hxd)
                |  dict_sclr_rat_sum(hxd)
                |  dict_sclr_other(hxd)                 )


    # Add table fields below
    data["expo.tbl_coverage"]                   = dict_tbl_ec_coverage(hxd)
    data["expo.event_table"]                    = dict_tbl_ec_event_table(hxd)
    data["nm.o75_table"]                        = dict_tbl_nm_o75_table(hxd)
    data["exper.tbl_overall"]                   = dict_tbl_exper_overall(hxd)
    data["exper.tbl_assump"]                    = dict_tbl_exper_assump(hxd)
    data["exper.tbl_project"]                   = dict_tbl_exper_project(hxd)
    data["exper.tbl_actuarial"]                 = dict_tbl_exper_actuarial_project(hxd)
    data["tbl_metrics_post"]                    = dict_tbl_metrics_post(hxd)
    data["tbl_metrics_pre"]                     = dict_tbl_metrics_pre(hxd)
    data["tbl_metrics_el"]                      = dict_tbl_metrics_el(hxd)
    data["rc.tbl_rc_profile"]                   = dict_tbl_rc_profile(hxd)
    data["rc.tbl_rc_drivers"]                   = dict_tbl_rc_drivers(hxd)
    data["tbl_actuarial_event"]                 = dict_tbl_actuarial_event(hxd)
    data["tbl_actuarial_nm"]                    = dict_tbl_actuarial_nm(hxd)
    data["tbl_actuarial_experience_analysis"]   = dict_tbl_actuarial_experience_analysis(hxd)
    data["tbl_actuarial_policy"]                = dict_tbl_actuarial_policy(hxd)
    data["tbl_actuarial_claim"]                 = dict_tbl_actuarial_claim(hxd)



    ##########################################################################################
    ### standard skeleton model code below here
    ##########################################################################################
    
    # Add URL of hx policy
    p_id    = hx.meta.policy_id
    po_id   = hx.meta.policy_option_id
    
    
    data["tst_policy_url"]  = f"https://www.beazley-tst.hxrenew.com/policies/{p_id}/options/{po_id}"
    data["dev_policy_url"]  = f"https://www.beazley-dev.hxrenew.com/policies/{p_id}/options/{po_id}"
    data["prd_policy_url"]  = f"https://www.beazley.hxrenew.com/policies/{p_id}/options/{po_id}"
    
    # policy_url = f"https://www.beazley.hxrenew.com/policies/{p_id}/options/{po_id}"
    # data["policy_url"] = policy_url

    # Format data
    formatted_data = clean_data_for_policy_doc(data)
    json_data = json.dumps(formatted_data)

    return json_data


# exclude section references from a stringified json
def exc_sr(s: str) -> str:
    # if empty return, otherwise convert to a json (js)
    if not s:                               # handling null json
        return s
    js  = json.loads(s)                     # converting to string

    # drop basic section references
    js.pop('ri.section_ref_na', None)       # removing basic section refs
    js.pop('ri.section_ref_ec', None)
    js.pop('exper.bi_val_calc', None)

    # drop sr in metrics if exists
    metrics = js.get('tbl_metrics_post')
    if metrics:                             # removing section refs from metrics if it exists
        metrics[0].pop('na_total', None)
        metrics[0].pop('ec_total', None)

    # drop pol_ref and sec_ref in tbl_actuarial_policy if exists
    policy_rows = js.get("tbl_actuarial_policy")
    if policy_rows:
        for row in policy_rows:
            row.pop("policy_ref", None)
            row.pop("section_ref", None)

    return json.dumps(js)


# Push dictionary to hxd for storage
def store_policy_data(hxd):
    # If there are multiple layers you'll need to update
    layer = hxd.cds.layers[0]

    # Don't run if premium has not been input
    if not layer.quoted_premium:
        return

    data = create_dict_for_excel(hxd)
    hxd.policy_doc.data_dict = data

    # Compare task data with live data to unhide download button
    task_data = hxd.policy_doc.task_data_dict
    hxd.policy_doc.show_download = True if exc_sr(data) == exc_sr(task_data) else False
