#########################################################
###  Outstanding Items                                ###
# 1) 
# 2) 
# 3) 
# 4) 
# 5) 
# 6) 
# 7) 
# 8) 
# 9) 
#10) 
#########################################################

import pandas                    as pd
import algorithms.rate_constants as constants
from libraries.model_profiler.algorithms.profiling_hxd_functions import time_me
from algorithms.rate_utilities                                   import(  pd_df_from_hx_list 
                                                                        , pd_df_from_hx_list_v2
                                                                        , pd_to_pl_df
                                                                        , write_pd_to_hxd_v2    
                                                                        , write_pd_to_hxd)


# Uses set Intersection to return a list of all the specified columns that exist in the df
def i_t(df,lst,ovd_calc=False):
    if ovd_calc:
        lst  = [f'{x}/calculated' for x in lst]
        cols = [c for c in lst if c in df.columns]
        cols = [c.removesuffix('/calculated') for c in cols]
    else:
        cols = [c for c in lst if c in df.columns]
    return cols


@time_me
def rater_load(hxd,rater):
    # need to specify columns and eliminate duplication and add paths to rater for easy saving
    # not contemplating feather or the unstructured data
    rater_load_policy_data(         hxd,rater)
    rater_load_claim_data(          hxd,rater)
    rater_load_assumed_deductions(  hxd,rater)
    rater_load_risk_composition(    hxd,rater)
    rater_load_inflation(           hxd,rater)
    rater_load_rate_change(         hxd,rater)
    rater_load_uncertainty(         hxd,rater)
    rater_load_anti_selection(      hxd,rater)
    rater_load_proj_lloyds_bzly(    hxd,rater)
    rater_load_prem_limit(          hxd,rater)
    rater_load_bp(                  hxd,rater)
    rater_load_proj_own_experience( hxd,rater)
    rater_load_rating_summary(      hxd,rater)
    rater_load_portfolio_profile(   hxd,rater)
    rater_load_pc(                  hxd,rater)

    return



@time_me
def rater_save(hxd,rater):

    is_bbt = hxd.cds.risk_information.follow_main_syndicate

    rater_save_risk_composition(    hxd,rater)  # make sure risk code composition happens early/first as some of the later saves condition on it
    rater_save_policy_data(         hxd,rater)
    rater_save_claim_data(          hxd,rater)
    rater_save_assumed_deductions(  hxd,rater)
    rater_save_inflation(           hxd,rater)
    rater_save_rate_change(         hxd,rater)
    rater_save_uncertainty(         hxd,rater)
    rater_save_anti_selection(      hxd,rater)
    rater_save_bp(                  hxd,rater)
    if rater.get('risk_composition_final', pd.DataFrame()).shape[0] != 0:
        rater_save_proj_lloyds_bzly(    hxd,rater)
        rater_save_proj_own_experience( hxd,rater)
    
    rater_save_prem_limit(          hxd,rater)
    rater_save_risk_code_library(    hxd,rater)
    rater_save_rating_summary(      hxd,rater)
    rater_save_pc(        hxd,rater)

    return




@time_me
def rater_load_policy_data(hxd,rater):
    if hxd.cds.policy_level_data_table.use_policy_level_data_grouped:
        path_data = hxd.cds.policy_level_data_table.policy_level_data_grouped
    else:
        path_data = hxd.cds.policy_level_data_table.policy_level_data
    cols                    = constants.policy_data_used_inputs
    rater["policy_data"]    = pd_df_from_hx_list_v2( path_data, cols )
    return 


@time_me
def rater_load_claim_data(hxd,rater):
    if hxd.cds.claim_level_data_table.use_claim_level_data_grouped:
        path_data = hxd.cds.claim_level_data_table.claim_level_data_grouped
    else:
        path_data              = hxd.cds.claim_level_data_table.claim_level_data
    cols                   = constants.claim_data_used_inputs
    rater['claim_data']    = pd_df_from_hx_list_v2( path_data, cols )
    return 


@time_me
def rater_load_assumed_deductions(hxd,rater):

    path_deductions_manual              = hxd.cds.assumed_deductions.deductions_manually_entered.table
    rater['deduct_manual']              = pd_df_from_hx_list_v2( path_deductions_manual )

    path_deductions_data                = hxd.cds.assumed_deductions.data_driven_deductions.deductions.table
    rater['deduct_data']                = pd_df_from_hx_list_v2( path_deductions_data )

    path_deductions_data_yr_sel_lob     = hxd.cds.assumed_deductions.data_driven_deductions.market_deductions.deductions_derived_from_data
    rater['deduct_data_yr_sel_lob']     = pd_df_from_hx_list_v2( path_deductions_data_yr_sel_lob )
    return 


@time_me
def rater_load_risk_composition(hxd,rater):
    path                                = hxd.cds.risk_code_composition.composition_manual.table
    rater['risk_comp_manual']           = pd_df_from_hx_list_v2( path )

    path                                = hxd.cds.risk_code_composition.data_driven_composition.composition_selection.table
    rater['risk_comp_data']             = pd_df_from_hx_list_v2( path )
        
    path                                = hxd.non_cds.risk_code_composition.final_composition 
    rater['risk_composition_final']     = pd_df_from_hx_list_v2(path)
    return 


@time_me
def rater_load_inflation(hxd,rater):
    path                    = hxd.cds.inflation.details
    cols                    = []
    rater['inflation_data'] = pd_df_from_hx_list_v2( path, cols )

    path                        = hxd.cds.inflation.summary_by_lob
    cols                        = []
    rater['inflation_by_lob']   = pd_df_from_hx_list_v2( path, cols )
    return



@time_me
def rater_load_rate_change(hxd,rater):
    path_data                 = hxd.cds.rate_change
    cols                      = [f'year_{x}.facility' for x in range(0,16)] + ['year_0.source']
    rater['rate_change_data'] = pd_df_from_hx_list_v2( path_data, cols )
    return 


@time_me
def rater_load_uncertainty(hxd,rater):
    path                                = hxd.cds.uncertainty.applied_charge.table
    rater['uncertainty_applied_charge'] = pd_df_from_hx_list_v2(path)
    return


@time_me
def rater_load_anti_selection(hxd,rater):
    # anti-selection
    path                                = hxd.cds.anti_selection.applied_charge.table
    rater['anti_sel_applied_charge']    = pd_df_from_hx_list_v2(path)

    return


@time_me
def rater_load_rating_summary(hxd,rater):
    path                            = hxd.cds.rating_summary.model_gn_ulr.projected_gn_ulr.table
    rater['rat_sum_proj_gnulr']     = pd_df_from_hx_list_v2(path)

    path                            = hxd.cds.rating_summary.model_gn_ulr.model_weights.table
    rater['rat_sum_mod_wgt']        = pd_df_from_hx_list_v2(path)

    path                            = hxd.cds.rating_summary.cat_loadings.cat_allocation
    rater['rat_sum_cat_alloc']      = pd_df_from_hx_list_v2(path)

    path                            = hxd.cds.rating_summary.additional_loadings.additional_pricing_loads
    rater['rat_sum_add_load']       = pd_df_from_hx_list_v2(path)

    # needed??? - whilst all outputs generated from pc task
    path                            = hxd.cds.pc.profit_commission.details
    rater['pc_details']             = pd_df_from_hx_list_v2(path)

    path                            = hxd.cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_final_pricing.table
    rater['rat_sum_adeq_final']     = pd_df_from_hx_list_v2(path)

    return 


@time_me
def rater_load_proj_lloyds_bzly(hxd,rater):
    # specify only input & override columns needed for quick retrieval
    cols_detail_ipt = []
    cols_detail_ovd = [  'dev_patterns_gnpi',   'dev_patterns_paid', 'dev_patterns_incurred',   'rate_change_selected'
                       , 'weighting_ielr',      'method_paid',       'method_incurred',         'weighting_selected'  ]
    cols_detail     = (  cols_detail_ipt 
                        + [f'{x}.selected' for x in cols_detail_ovd]
                        + [f'{x}.is_overridden' for x in cols_detail_ovd])

    cols_summary_ipt = [ 'projection_type', 'ielr_approach',   'bp_cat', 'ielr_source', 'cat_lr_source', 'actuarial_notes', 'comments', 'checked']
    cols_summary_ovd = [ 'selected_ielr',   'bp_cat_load'              ]
    cols_summary     = (  cols_summary_ipt 
                        + [f'{x}.selected' for x in cols_summary_ovd]
                        + [f'{x}.is_overridden' for x in cols_summary_ovd])
   
    lloyds_path         = hxd.cds.projections_lloyds
    bzly_path           = hxd.cds.projections_beazley

    path                            = bzly_path.summary_table
    rater['proj_beazley_summary']   = pd_df_from_hx_list_v2(path, cols_summary)

    path                            = bzly_path.detail_table
    rater['proj_beazley_detail' ]   = pd_df_from_hx_list_v2(path, cols_detail)

    path                            = lloyds_path.summary_table
    rater['proj_lloyds_summary']    = pd_df_from_hx_list_v2(path, cols_summary)

    path                            = lloyds_path.detail_table
    rater['proj_lloyds_detail' ]    = pd_df_from_hx_list_v2(path, cols_detail)
    return 


@time_me
def rater_load_prem_limit(hxd,rater):
    path                     = hxd.cds.prem_limit_profile.table
    rater['prem_limit_data'] = pd_df_from_hx_list_v2(path)
    return


@time_me
def rater_load_bp(hxd,rater):
    path                      = hxd.cds.bp_projections.bp_details
    rater['bp_details']       = pd_df_from_hx_list_v2(path)
    return


@time_me
def rater_load_proj_own_experience(hxd,rater):
    # Load summary columns
    cols_summary_ipt = [ "claim_source", "claim_basis", "claim_to_develop_to_ultimate", "cat_basis", 'ielr_approach', 'actuarial_notes']

    cols_summary_ovd = [ "ielr_attr",           "ielr_large",           "ielr_cat",         "ielr_total"
                        ,"selected_attr",       "selected_large",       "selected_cat"
                        ,"model_default_attr",  "model_default_large",  "model_default_cat"             ]
    cols_summary     = (  cols_summary_ipt 
                        + [f'{x}.selected' for x in cols_summary_ovd]
                        + [f'{x}.is_overridden' for x in cols_summary_ovd])
   
    # load summary data including polars
    path                                = hxd.cds.projections_own_experience.summary_table
    proj_own_exper_summary_df           = pd_df_from_hx_list_v2(path, cols_summary)
    rater['proj_own_exper_summary']     = proj_own_exper_summary_df                 
    rater['proj_own_exper_summary_pl']  = pd_to_pl_df(proj_own_exper_summary_df)     


    cols_detail_ipt = [  "additional_ibnr_attr"        ,"additional_ibnr_large"         ,"additional_ibnr_cat"
                        ,"last_year_position_attr"     ,"last_year_position_large"      ,"last_year_position_cat"
                        ,"last_year_position_total"    
                        ,"ultimate_premium_selected_gnpi_override" 
                        ,"development_pattern_premium_override"            ,"development_pattern_incurred_override"]
    
    # Load detail columns                
    cols_detail_ovd = [  "ielr_weighting_cl_attr",          "ielr_weighting_cl_large"
                        ,"ielr_weighting_cl_cat",           "ielr_weighting_cl_total"
                        ,"ultimate_incurred_selected_attr", "ultimate_incurred_selected_large"
                        ,"ultimate_incurred_selected_cat",  "ultimate_incurred_selected_total"
                        ,"ielr_weighting_sel_attr",         "ielr_weighting_sel_large"
                        ,"ielr_weighting_sel_cat",          "ielr_weighting_sel_total"
                        ,"method_incurred", "applied_rate_change",  "applied_inflation"         ]

    # load detail data including polars
    cols_detail     = (  cols_detail_ipt 
                        + [f'{x}.selected' for x in cols_detail_ovd]
                        + [f'{x}.is_overridden' for x in cols_detail_ovd])

    path                                = hxd.cds.projections_own_experience.detail_table
    rater['proj_own_exper_detail']      = pd_df_from_hx_list_v2(path, cols_detail)
    return


@time_me
def rater_load_portfolio_profile(hxd,rater):

    path                            = hxd.cds.portfolio_profile.selected_lob_and_risk_code_combination
    rater['portfolio_profile']      = pd_df_from_hx_list_v2(path) # was portfolio_profile_df - empty

    path                                = hxd.cds.portfolio_profile.summary_by_lob 
    rater['portfolio_profile_summary']  = pd_df_from_hx_list_v2(path) # was portfolio_profile_summary_df
    return


@time_me
def rater_load_pc(hxd,rater):
    path                      = hxd.cds.pc.pc_structure.table
    rater['pc_structure']     = pd_df_from_hx_list_v2(path)

    path                      = hxd.cds.pc.pc_calculations.details
    rater['pc_calc']          = pd_df_from_hx_list_v2(path)
    return

####################################################################################################
### SAVES BELOW HERE
####################################################################################################


@time_me
def rater_save_assumed_deductions(hxd,rater):

    # data prep work
    path_ad     = hxd.cds.assumed_deductions
    inception_year   = hxd.cds.standard_fields.inception_date.year
    num_years        = constants.YEARS_TO_CONSIDER_IN_ASSUMED_DEDUCTIONS
    years_dict       = {  str(inception_year - i): f"year_{i}"   for i in range(num_years)  }
    years_to_process = list(years_dict.values())


    # deduct_data
    df          = rater.get('deduct_data', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty & hxd.cds.risk_information.prem_data_available
    if condition:
        path        = path_ad.data_driven_deductions.deductions.table
        cols_out    = ['selected_lob', "selected_effective_deductions", "is_row_visible"]
        cols_ovd    = ['market_deductions', 'mga_fee', 'facility_brokerage', 'leaders_fee', 'service_fee', 'other']
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2


    # deduct_manual
    df          = rater.get('deduct_manual', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty & (path_ad.model_type.selected == 'Manual')
    if condition:
        path        = path_ad.deductions_manually_entered.table
        cols_out    = ['selected_lob', "selected_effective_deductions", "is_row_visible"]
        cols_ovd    = ['mga_fee', 'facility_brokerage', 'leaders_fee', 'service_fee', 'other']
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2


    # deduct_data_gp_ded
    df          = rater.get('deduct_data_gp_ded', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = path_ad.data_driven_deductions.gross_premium
        cols_out    = years_to_process + ['selected_lob']
        cols_ovd    = []
        path.deductions_derived_from_data = df[cols_out].to_dict(orient="records")      # passing as dictionary as all outputs 


    # deduct_data_np_ded
    df          = rater.get('deduct_data_np_ded', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty 
    if condition:
        path        = path_ad.data_driven_deductions.net_premium
        cols_out    = years_to_process + ['selected_lob']
        cols_ovd    = []
        path.deductions_derived_from_data = df[cols_out].to_dict(orient="records")      # passing as dictionary as all outputs 


    # deduct_data_mkt_ded
    df          = rater.get('deduct_data_mkt_ded', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = path_ad.data_driven_deductions.market_deductions
        cols_out    = years_to_process + ['selected_lob']
        cols_ovd    = []
        path.deductions_derived_from_data = df[cols_out].to_dict(orient="records")      # passing as dictionary as all outputs 

    return



@time_me
def rater_save_anti_selection(hxd,rater):
    df          = rater.get('anti_sel_applied_charge', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = hxd.cds.anti_selection.applied_charge.table
        cols_out    = ['selected_lob', 'is_row_visible', 'own_performance', 'lloyds_performance',
                       'beazley_performance', 'business_plan', 'case_pricing', 'pricing_2623_623']
        cols_ovd    = ['anti_selection_charge']
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd)                         # not use True here for ovd cols as using v1 of write_pd_to_hxd
        write_pd_to_hxd(df, path, cols_out, cols_ovd)           # using v1 as 'calculated' part of the override is in the root of the node
    return



@time_me
def rater_save_bp(hxd,rater):
    df          = rater.get('bp_summary_by_lob', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = hxd.cds.bp_projections.bp_summary_by_lob
        cols_out    =( ['tracker_class', 'selected_lob', 'is_row_visible', 'composition']
                      +['acc_aquisition_costs', 'attr_base_gn_ulr',     'attr_inflation_1_year',
                        'attr_rate_change',     'attr_rarc_margin',     'attr_portfolio_change',
                        'cat_base_gn_ulr',      'cat_inflation_1_year', 'cat_rate_change',
                        'cat_rarc_margin',      'cat_climate_change',   'cat_nmp_general',  'cat_nmp_all_other'   ]
                      +['selected_attr_gn_ulr', 'selected_cat_gn_ulr',  'total_gn_ulr',     'bp_acquisition_costs', 
                        'adj_attr_gn_ulr',      'adj_cat_gn_ulr',       'adj_total_gn_ulr', 'rate_change_override']) # kept as 3 lists for easy comparing to init_bp_summary_by_lob & build_bp_summary_by_lob
        cols_ovd    = []
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2


    df          = rater.get('bp_details', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = hxd.cds.bp_projections.bp_details
        cols_out    =  ['tracker_class',        'selected_lob',         'is_row_visible',       'composition',      'risk_code',     
                        'acc_aquisition_costs', 'attr_base_gn_ulr',     'attr_inflation_1_year','attr_rate_change', 'attr_rarc_margin',     'attr_portfolio_change',
                        'cat_base_gn_ulr',      'cat_inflation_1_year', 'cat_rate_change',      'cat_rarc_margin',  'cat_climate_change',   'cat_nmp_general',
                        'cat_nmp_all_other',    'selected_attr_gn_ulr', 'selected_cat_gn_ulr',  'total_gn_ulr',     'bp_acquisition_costs', 'adj_total_gn_ulr']
        cols_ovd    = ['bp_class', 'rate_change_override', 'adj_attr_gn_ulr', 'adj_cat_gn_ulr']
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2
    return



@time_me
def rater_save_claim_data(hxd,rater):
    df          = rater.get('claim_data', pd.DataFrame())
    df_not_empty= not df.empty
    path        = hxd.cds.claim_level_data_table.claim_level_data
    lm_mode     = hxd.cds.risk_information.is_large_model_mode
    len_match   = len(path) == len(df)                          # added to handle switching back from large model mode with data still cached
    condition   = df_not_empty and len_match and (not lm_mode)
    if condition:
        # path        = hxd.cds.claim_level_data_table.claim_level_data
        cols_out    = ['selected_lob', 'modelled', "paid_cnv", "outstanding_cnv", "incurred_cnv"]
        cols_ovd    = []
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2
    return



@time_me
def rater_save_policy_data(hxd,rater):
    df          = rater.get('policy_data', pd.DataFrame())
    df_not_empty= not df.empty
    path        = hxd.cds.policy_level_data_table.policy_level_data
    lm_mode     = hxd.cds.risk_information.is_large_model_mode
    len_match   = len(path) == len(df)                          # added to handle switching back from large model mode with data still cached
    condition   = df_not_empty and len_match and (not lm_mode)
    if condition:
        # path        = hxd.cds.policy_level_data_table.policy_level_data
        cols_out    = [f"{field}_cnv" for field in constants.policy_fields_to_convert] + ['selected_lob', 'modelled']
        cols_ovd    = []
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2
    return



@time_me
def rater_save_prem_limit(hxd,rater):
    df          = rater.get('prem_limit_data', pd.DataFrame())
    df          = df.astype(object).where(pd.notnull(df), None)                # substitute None for nan when writing to hxd
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = hxd.cds.prem_limit_profile.table
        cols_out    = ['is_row_visible', 'bst_share_ultimate_gross_premium', 'bst_deductions']
        cols_ovd    = ['lob', 'selected_lob', 'assigned_trifocus', 'bst_share_line_size', 'bst_net_premium', 'portfolio_composition']
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2
    return



@time_me
def rater_save_proj_lloyds_bzly(hxd,rater):

    lloyds_path  = hxd.cds.projections_lloyds
    beazley_path = hxd.cds.projections_beazley

    det_bzly_df  = rater.get('proj_beazley_detail', pd.DataFrame())
    sum_bzly_df  = rater.get('proj_beazley_summary', pd.DataFrame())

    det_lyds_df  = rater.get('proj_lloyds_detail', pd.DataFrame())
    sum_lyds_df  = rater.get('proj_lloyds_summary', pd.DataFrame())

    # columns needed in both summary & detail - not override (also implicitly none of these are inputs)
    core_std_lst =  [   'lob_number',
                        'risk_code',
                        'selected_lob',
                        'lookup_lob',

                        'latest_gpi',
                        'latest_gnpi',
                        'latest_paid',


                        'latest_incurred',
                        'acquisition_ratio',
                        'incurred_loss_ratio',
                        'ultimate_gnpi',
                        'ultimate_gnpi_ol_model',
                        'ultimate_gnpi_ol_selected',
                        'ultimate_cl_paid',
                        'ultimate_cl_paid_ulr',
                        'ultimate_cl_incurred',
                        'ultimate_cl_incurred_ulr',
                        'ultimate_ielr_model',
                        'ultimate_ielr_model_ulr',
                        'ultimate_ielr_selected',
                        'ultimate_ielr_selected_ulr',
                        'ultimate_bf_model_paid',
                        'ultimate_bf_model_incurred',
                        'ultimate_bf_selected_paid',
                        'ultimate_bf_selected_incurred',
                        'ultimate_model',
                        'ultimate_model_ulr',
                        'ultimate_selected',
                        'ultimate_selected_ulr',
                        'on_levelled_model_ulr',
                        'on_levelled_selected_ulr',

                        'is_row_visible', 
                        'lob_visible_1',
                        'lob_visible_2',
                        'lob_visible_3',
                        'lob_visible_4',
                        'lob_visible_5'                                     
                        ]

    # columns needed in just detail - not override (also implicitly none of these are inputs)
    detail_std_lst = [  'yoa',
                        'inflation_model',
                        'rate_change_model',

                        'inflation_model_index',
                        'rate_change_model_index',
                        'rate_change_selected_index',
                        'loss_ratio_model_index',
                        'loss_ratio_selected_index',
                        'weighting_model',

                        'weighting_1_exposure_onlevel',
                        'weighting_2_decay_ratio',
                        'weighting_3_developed',
                        'weighting_onlevel',
                        'weighting_1_exposure_nominal',
                        'weighting_nominal'
                        ]

    # columns needed in just detail - and override
    detail_ovd_lst = [  'dev_patterns_gnpi',
                        'dev_patterns_paid',
                        'dev_patterns_incurred',
                        'weighting_ielr',
                        'method_paid',
                        'method_incurred',
                        'rate_change_selected',
                        'weighting_selected']

    # columns needed in just summary - not override (implicitly these are summations of inputs by year)
    summary_std_lst = []

    # these are additional summary values that are outputs and present in just the summary table
    summary_adn_std_lst = [ 
                            'selected_lob',
                            'bp_class',
                            'tracker_class',
                            # 'projection_type',
                            # 'ielr_approach',
                            'lloyds_ielr',
                            'composition',
                            'model_ielr_nominal',
                            'model_ielr_onlevel',
                            'model_ielr_ol_allyr',
                            'model_ielr',
                            'model_gn_ulr',
                            'model_base_aqn',
                            'model_acc_aqn',
                            'model_final_gn_ulr',
                            'model_adj_gn_ulr',
                            'selected_gn_ulr',
                            'selected_base_aqn',
                            'selected_acc_aqn',
                            'selected_adj_gn_ulr',
                            'selected_final_gn_ulr'
                            ]

            
    # these are additional summary values that are outputs and present in just the summary table
    summary_adn_ovd_lst = [ 'selected_ielr','bp_cat_load' ]


    # build final lists of columns
    detail_output_lst   = [x for x in (core_std_lst + detail_std_lst)  if x in det_bzly_df.columns]                       # using bzly but could have used lloyds - same structure
    detail_override_lst = [x for x in (               detail_ovd_lst)  if x in det_bzly_df.columns]                       # using bzly but could have used lloyds - same structure
    summary_output_lst  = [x for x in (core_std_lst + summary_std_lst + summary_adn_std_lst) if x in sum_bzly_df.columns] # using bzly but could have used lloyds - same structure
    summary_override_lst= [x for x in (             summary_adn_ovd_lst                    ) if x in sum_bzly_df.columns] # using bzly but could have used lloyds - same structure


    detail_output_lst    = i_t(det_bzly_df, detail_output_lst)
    detail_override_lst  = i_t(det_bzly_df, detail_override_lst, True)    # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
    summary_output_lst   = i_t(sum_bzly_df, summary_output_lst)
    summary_override_lst = i_t(sum_bzly_df, summary_override_lst, True)    # use True here for ovd cols as using v2 of write_pd_to_hxd_v2

    # split df to just bzly and write to hxd
    det_bzly_df  = rater.get('proj_beazley_detail', pd.DataFrame())
    sum_bzly_df  = rater.get('proj_beazley_summary', pd.DataFrame())
    write_pd_to_hxd_v2(det_bzly_df, beazley_path.detail_table,  detail_output_lst,  detail_override_lst)
    write_pd_to_hxd_v2(sum_bzly_df, beazley_path.summary_table, summary_output_lst, summary_override_lst)

    # split df to anything but bzly and write to hxd
    det_lyds_df  = rater.get('proj_lloyds_detail', pd.DataFrame())
    sum_lyds_df  = rater.get('proj_lloyds_summary', pd.DataFrame())
    write_pd_to_hxd_v2(det_lyds_df, lloyds_path.detail_table,  detail_output_lst,  detail_override_lst)
    write_pd_to_hxd_v2(sum_lyds_df, lloyds_path.summary_table, summary_output_lst, summary_override_lst)
    return



@time_me
def rater_save_proj_own_experience(hxd, rater):
    """
    Saves detail and summary DataFrames to HxD using predefined column mappings.
    """

    # alct columns that are used in both detail_df & summary_df and not overrides
    def alct_core_std_lst(k):
        return [        f'latest_incurred_open_claims_{k}',
                        f'latest_incurred_closed_claims_{k}',
                        f'latest_incurred_total_claims_{k}',
                        f'movement_{k}',
                        f'gn_ilr_{k}',
                        f'ultimate_incurred_ielr_{k}',
                        f'ultimate_incurred_bf_{k}',
                        f'ultimate_incurred_cl_{k}',             
                        f'ultimate_ulr_selected_{k}'            ]

    # alct columns that are used in both detail_df & summary_df and are overrides 
    # *** NOTE HOWEVER THESE ARE NOT OVERRIDES AT THE SUMMARY LEVEL
    def alct_core_ovd_lst(k):
        return [        f'ultimate_incurred_selected_{k}'       ]


    # alct columns that are used in detail_df and are NOT overrides
    def alct_detail_std_lst(k):
        return [        f'ultimate_ulr_on_levelled_{k}',            # arguably we should calculate totals on this
                        f'ultimate_ulr_selected_{k}'            ]   # arguably we should calculate totals on this

    # alct columns that are used in detail_df and are overrides
    def alct_detail_ovd_lst(k):
        return [        f'ielr_weighting_cl_{k}',                   #override
                        f'ielr_weighting_sel_{k}'               ]   #override

    # alct columns that are used in just summary_df and are NOT overrides
    def alct_summary_std_lst(k):
        return [        f'additional_ibnr_{k}',                 ]


    detail_df           = rater['proj_own_exper_detail']
    summary_df          = rater['proj_own_exper_summary']
    own_experience_path = hxd.cds.projections_own_experience


    # columns needed in both summary & detail - not override (also implicitly none of these are inputs)
    core_std_lst =  [   'lob_number',
                        'selected_lob',
                        'yoa',

                        'latest_gpi',
                        'latest_gnpi',
                        'acquisition_costs',

                        'ultimate_premium_selected_gnpi_cl',
                        'ultimate_premium_selected_gnpi_selected',  
                        'ultimate_premium_selected_gnpi_selected_ol',

                        'ultimate_incurred_cl_ielr',
                        'additional_ibnr_total',
                        'ultimate_incurred_selected_total_x_cat',     
                        'ultimate_ulr_selected_total_x_cat',
                        'ultimate_ulr_on_levelled_total_x_cat',
                        
                        'is_row_visible',
                        'lob_visible_1',
                        'lob_visible_2',
                        'lob_visible_3',
                        'lob_visible_4',
                        'lob_visible_5'
                    ]

    # columns needed in just detail - not override (also implicitly none of these are inputs)
    detail_std_lst = [  'development_pattern_premium_lloyds_unadjusted',
                        'development_pattern_paid_lloyds_unadjusted',
                        'development_pattern_incurred_lloyds_unadjusted',
                        'development_pattern_premium_lloyds',
                        'development_pattern_paid_lloyds',
                        'development_pattern_incurred_lloyds',
                        'development_pattern_premium_selected',
                        'development_pattern_incurred_selected',
                        
                        'modelled_weighting',

                        'exposure_weighting_onlevel_1',
                        'exposure_weighting_nominal_1',
                        'decay_ratio_weighting_2',
                        'developed_weighting_3',
                        'overall_weighting_onlevel',
                        'overall_weighting_nominal',
                        'adjustments_actual',
                        'adjustments_lower',
                        'adjustments_upper',
                        'adjustments_prem_lloyds_lower',
                        'adjustments_prem_lloyds_upper',
                        'adjustments_prem_lloyds_actual',
                        'adjustments_incurred_lloyds_lower',
                        'adjustments_incurred_lloyds_upper',
                        'adjustments_incurred_lloyds_actual',

                        'applied_rate_change_cumulative',
                        'applied_inflation_cumulative',
                        'onlevel_factor_cumulative'             ]

                        # 'ultimate_ulr_selected_total_x_cat',        # arguably we should calculate totals on this
                        # 'ultimate_ulr_on_levelled_total_x_cat']      # arguably we should calculate totals on this
                        # # ultimate_incurred_cl_ielr              ]

    # columns needed in just detail - and override
    detail_ovd_lst = [  'method_incurred', 
                        'applied_rate_change',
                        'applied_inflation'                      ]

    # columns needed in just summary - not override (implicitly these are summations of inputs by year)
    summary_std_lst = ['ultimate_premium_selected_gnpi_override',
                        'additional_ibnr_attr',
                        'additional_ibnr_large',
                        'additional_ibnr_cat'                    ]

    # *** not needed - input with no totals 
    # 'development_pattern_premium_override',
    # 'development_pattern_incurred_override',


    # these are additional summary values that are outputs and present in just the summary table
    summary_adn_std_lst = [ 'ielr_total_excl_cat',

                            'ielr_nominal_attr',
                            'ielr_nominal_large',
                            'ielr_nominal_cat',
                            'ielr_nominal_total',
                            'ielr_nominal_total_excl_cat',

                            'ielr_ol_all_yr_attr',
                            'ielr_ol_all_yr_large',
                            'ielr_ol_all_yr_cat',
                            'ielr_ol_all_yr_total',
                            'ielr_ol_all_yr_total_excl_cat',

                            'ielr_ol_cl_yr_attr',
                            'ielr_ol_cl_yr_large',
                            'ielr_ol_cl_yr_cat',
                            'ielr_ol_cl_yr_total',
                            'ielr_ol_cl_yr_total_excl_cat',

                            'selected_total',
                            'selected_total_excl_cat',
                            'selected_cat_exp',
                            'selected_cat_bp',
                            'selected_cat_rms',
                            'selected_cat_basis',

                            'model_default_total',
                            'model_default_total_excl_cat',
                            'model_default_cat_exp',
                            'model_default_cat_bp',
                            'model_default_cat_rms',
                            'model_default_cat_basis',

                            'lloyds_model_ielr',
                            'lloyds_model_final_gn_ulr',
                            'lloyds_selected_ielr',
                            'lloyds_selected_final_gn_ulr',
                            'beazley_model_ielr',
                            'beazley_model_final_gn_ulr',
                            'beazley_selected_ielr',
                            'beazley_selected_final_gn_ulr',

                            'ovd_dev',
                            'ovd_index',
                            'ovd_premium',
                            'ovd_ielr_weights',
                            'ovd_ielr',
                            'ovd_ibnr',
                            'ovd_ultimate_method',
                            'ovd_ultimate',
                            'ovd_ulr_weights',
                            'ovd_ulr',
                            
                            'cov_attr',
                            'cov_large',
                            'cov_cat'

                            ]

            
    # these are additional summary values that are outputs and present in just the summary table
    summary_adn_ovd_lst = [ 'ielr_attr',
                            'ielr_large',
                            'ielr_cat',
                            'ielr_total',

                            'selected_attr',
                            'selected_large',
                            'selected_cat',

                            'model_default_attr',
                            'model_default_large',
                            'model_default_cat'
                            ]


    # build final lists of columns
    detail_output_lst   = (   core_std_lst
                            + detail_std_lst
                            + [item for k in ['attr', 'large', 'cat', 'total'] for item in alct_core_std_lst(k)]
                            + [item for k in ['attr', 'large', 'cat', 'total'] for item in alct_detail_std_lst(k)]  )
    
    detail_override_lst = (   detail_ovd_lst
                            + [item for k in ['attr', 'large', 'cat', 'total'] for item in alct_core_ovd_lst(k)]
                            + [item for k in ['attr', 'large', 'cat', 'total'] for item in alct_detail_ovd_lst(k)]  )        


    summary_output_lst  = (   core_std_lst
                            + summary_std_lst
                            + [item for k in ['attr', 'large', 'cat', 'total'] for item in alct_core_std_lst(k)]
                            + [item for k in ['attr', 'large', 'cat', 'total'] for item in alct_core_ovd_lst(k)]    #deliberately included here as not override at summary level
                            + [item for k in ['attr', 'large', 'cat', 'total'] for item in alct_summary_std_lst(k)]  
                            + summary_adn_std_lst                                                                   )
    
    summary_override_lst = summary_adn_ovd_lst


    detail_output_lst    = i_t(detail_df, detail_output_lst)
    detail_override_lst  = i_t(detail_df, detail_override_lst, True)    # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
    summary_output_lst   = i_t(summary_df, summary_output_lst)
    summary_override_lst = i_t(summary_df, summary_override_lst, True)    # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
    
    # write to hx
    
    write_pd_to_hxd_v2(detail_df,  own_experience_path.detail_table,  detail_output_lst,  detail_override_lst)
    write_pd_to_hxd_v2(summary_df, own_experience_path.summary_table, summary_output_lst, summary_override_lst)
    
    return



@time_me
def rater_save_inflation(hxd,rater):
    
    # prep steps to select right columns
    from algorithms.inflation.inflation_helpers import  generate_years_dict
    years_dict              = generate_years_dict(hxd)
    final_composition_path  = hxd.non_cds.risk_code_composition.final_composition
    fc_empty                = (not final_composition_path) or (final_composition_path == [{}])
    fc_not_empty            = not fc_empty

    # inflation_data
    df               = rater.get('inflation_data', pd.DataFrame())
    df_not_empty     = not df.empty
    condition        = df_not_empty & fc_not_empty
    numeric_cols     = df.select_dtypes(include='number').columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    if condition:
        path        = hxd.cds.inflation.details
        cols_out    = ['selected_lob', 'risk_code', 'composition', 'is_row_visible'] + list(years_dict.values())[6:26]
        cols_ovd    = ['bp_class'] + list(years_dict.values())[:constants.NUMBER_OF_INFLATION_YEARS]
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2

    # inflation_by_lob
    df          = rater.get('inflation_by_lob', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty & fc_not_empty
    if condition:
        path        = hxd.cds.inflation.summary_by_lob
        cols_out    = ['selected_lob', 'composition'] + list(years_dict.values())
        cols_ovd    = []
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2

    return



@time_me
def rater_save_rate_change(hxd,rater):

    df          = rater.get('rate_change_data', pd.DataFrame())
    df          = df.astype(object).where(pd.notnull(df), None)                # substitute None for nan when writing to hxd
    df_not_empty= not df.empty
    condition   = df_not_empty
 
    if condition:
        # Determine years of rate change to process
        inception_year   = hxd.cds.standard_fields.inception_date.year
        num_years        = constants.YEARS_TO_CONSIDER_IN_RATE_CHANGE
        years_dict       = {  str(inception_year - i): f"year_{i}"   for i in range(num_years)  }
        years_to_process = list(years_dict.values())[1:]

        # Build the list of output column names explicitly
        cols_out = ['year_0/bp_rate_change', 'year_0/bp_rarc_margin', 'year_0/selected']
        cols_out+=['dominant_risk_code', 'selected_lob', 'is_row_visible', 'bp_class']
        cols_out+= [f'{year}/yoa' for year in years_dict.values()]
        
        for year in years_to_process:
            cols_out.append(f'{year}/beazley_group_achieved')
            cols_out.append(f'{year}/selected')
        
        cols_ovd    = []
        path        = hxd.cds.rate_change
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2
    return



@time_me
def rater_save_rating_summary(hxd,rater):
    
    rating_summary_path = hxd.cds.rating_summary 
    
    # save projected GNULR to hxd
    df          = rater.get('rat_sum_proj_gnulr', pd.DataFrame())
    df          = df.astype(object).where(pd.notnull(df), None)                # substitute None for nan when writing to hxd
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = rating_summary_path.model_gn_ulr.projected_gn_ulr.table
        cols_out    = ['selected_lob',   'tracker_class', 'gn_premium',     'portfolio_percent', 'total_deductions',
                       'own_exp_gn_ulr', 'lloyds_gn_ulr', 'beazley_gn_ulr', 'bp_gn_ulr',         'is_row_visible']
        cols_ovd    = []
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2

    # save summary weights to hxd
    df          = rater.get('rat_sum_mod_wgt', pd.DataFrame())
    df          = df.astype(object).where(pd.notnull(df), None)                # substitute None for nan when writing to hxd
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = rating_summary_path.model_gn_ulr.model_weights.table
        cols_out    = ['weighting_check', 'model_estimate', 'selected_lob','is_row_visible']
        cols_ovd    = []
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2

    # save cat allocation to hxd
    df          = rater.get('rat_sum_cat_alloc', pd.DataFrame())
    df          = df.astype(object).where(pd.notnull(df), None)                # substitute None for nan when writing to hxd
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = rating_summary_path.cat_loadings.cat_allocation 
        cols_out    = [  'attr_and_lrg_exp',    'cat_exp',          'attr_and_lrg_bp', 'cat_bp',       'attr_and_lrg'
                       , 'climate_change_load', 'nmp_load_general', 'nmp_load_weather','selected_lob', 'is_row_visible']
        cols_ovd    = ['cat']
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd)                         # not use True here for ovd cols as using v1 of write_pd_to_hxd
        write_pd_to_hxd(df, path, cols_out, cols_ovd)           # using v1 as 'calculated' part of the override is in the root of the node

    # save additional loadings to hxd
    df          = rater.get('rat_sum_add_load', pd.DataFrame())
    df          = df.astype(object).where(pd.notnull(df), None)                # substitute None for nan when writing to hxd
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = rating_summary_path.additional_loadings.additional_pricing_loads
        cols_out    = ['selected_lob', 'is_row_visible', 'anti_selection_charge', 'uncertainty_charge']
        cols_ovd    = []
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2

    # save cat ulr to hxd
    df          = rater.get('rat_sum_cat_ulr', pd.DataFrame())
    df          = df.astype(object).where(pd.notnull(df), None)                # substitute None for nan when writing to hxd
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = rating_summary_path.cat_ulr_summary         # notice this does not include "details" as we need that when we pass the dictionary a few rows lower so as not to mutate the original path object 
        cols_out    = ["gn_cat_ulr_excl_loads", "gn_cat_ulr_inc_loads", "selected_lob", "is_row_visible"]
        cols_ovd    = []
        path.details= df[cols_out].to_dict(orient="records")      # passing as dictionary as all outputs 

    # save cat ulr to hxd
    df          = rater.get('rat_sum_cat_ulr', pd.DataFrame())
    df          = df.astype(object).where(pd.notnull(df), None)                # substitute None for nan when writing to hxd
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = rating_summary_path.cat_ulr_summary         # notice this does not include "details" as we need that when we pass the dictionary a few rows lower so as not to mutate the original path object 
        cols_out    = ["gn_cat_ulr_excl_loads", "gn_cat_ulr_inc_loads", "selected_lob", "is_row_visible"]
        cols_ovd    = []
        path.details= df[cols_out].to_dict(orient="records")      # passing as dictionary as all outputs 

    # save pricing adequacy actuarial basis to HXD
    df          = rater.get('rat_sum_adeq_act', pd.DataFrame())
    df          = df.astype(object).where(pd.notnull(df), None)                # substitute None for nan when writing to hxd
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = rating_summary_path.pricing_adequacy_metrics.pricing_adequacy_actuarial_basis    # notice this does not include "table" as we need that when we pass the dictionary a few rows lower so as not to mutate the original path object 
        cols_out    = [ 'selected_lob', 'best_estimate_pre_pc_adj', 'is_row_visible', 'pc_impact',
                        'best_estimate','bpi',                      'tpi',            'roc'    ]
        cols_ovd    = []
        path.table  = df[cols_out].to_dict(orient="records")      # passing as dictionary as all outputs 

    # save pricing adequacy pre uncertainty & anti-selection  to HXD
    df          = rater.get('rat_sum_adeq_pre', pd.DataFrame())
    df          = df.astype(object).where(pd.notnull(df), None)                # substitute None for nan when writing to hxd
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = rating_summary_path.pricing_adequacy_metrics.pricing_adequacy_pre_adj    # notice this does not include "table" as we need that when we pass the dictionary a few rows lower so as not to mutate the original path object 
        cols_out    = [ 'selected_lob', 'best_estimate_pre_pc_adj', 'is_row_visible', 'pc_impact',
                        'best_estimate','bpi',                      'tpi',            'roc'    ]
        cols_ovd    = []
        path.table  = df[cols_out].to_dict(orient="records")      # passing as dictionary as all outputs 

    # save pricing adequacy final selection to HXD
    df          = rater.get('rat_sum_adeq_final', pd.DataFrame())
    df          = df.astype(object).where(pd.notnull(df), None)                # substitute None for nan when writing to hxd
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = rating_summary_path.pricing_adequacy_metrics.pricing_adequacy_final_pricing.table
        cols_out    = ['selected_lob', 'is_row_visible', 'best_estimate_gn', 'best_estimate_gg', 'bpi', 'tpi', 'roc']
        cols_ovd    = []
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2

    # save technical premium   to HXD
    df          = rater.get('rat_sum_tech_prem', pd.DataFrame())
    df          = df.astype(object).where(pd.notnull(df), None)                # substitute None for nan when writing to hxd
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = rating_summary_path.technical_premium_build_up                        # notice this does not include "technical_premium" as we need that when we pass the dictionary a few rows lower so as not to mutate the original path object 
        cols_out    = ['selected_lob', 'el_pre_adj', 'el_actuarial',  'el_final',         'net_expense', 
                      'inv_income',   'ri_premium', 'ri_recoveries', 'capital_required', 'target_roc', 
                      'tp_pre_adj',   'tp_actuarial','tp_final',     'gg_tp_final',      'gg_bm_final', 'is_row_visible']
        cols_ovd    = []
        path.technical_premium  = df[cols_out].to_dict(orient="records")      # passing as dictionary as all outputs 
    return



@time_me 
def rater_save_risk_composition(hxd,rater):
    
    # risk_comp_data 
    df          = rater.get('risk_comp_data', pd.DataFrame())
    df          = df.dropna(subset=["cs_risk_code"])
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = hxd.cds.risk_code_composition.data_driven_composition.composition_selection.table
        cols_out    = ["cs_risk_code",    "cs_composition",   "exists_in_data_bool",  "composition_reweighted",
                       "cs_facility_line_of_business",        "is_row_visible",        "risk_code_description"    ]
        cols_ovd    = ["selected_bp_class", "tracker_class"]
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2


    # risk_comp_manual 
    df          = rater.get('risk_comp_manual', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = hxd.cds.risk_code_composition.composition_manual.table
        cols_out    = ["exists_in_data_bool", "composition_reweighted", "cs_facility_line_of_business", "risk_code_description","is_row_visible"]
        cols_ovd    = ["selected_bp_class", "tracker_class"]
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2

    return



@time_me 
def rater_save_risk_code_library(hxd,rater):
    
    # risk_code_library_df 
    df          = rater.get('risk_code_library_df', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = hxd.cds.risk_code_library
        cols_out    = df.columns
        cols_ovd    = []
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2

    return


@time_me 
def rater_save_uncertainty(hxd,rater):
    # uncertainty_applied_charge 
    df          = rater.get('uncertainty_applied_charge', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = hxd.cds.uncertainty.applied_charge.table
        cols_out    = ['selected_lob', 'is_row_visible', 'own_performance', 'lloyds_performance',
                       'beazley_performance', 'business_plan', 'case_pricing', 'pricing_2623_623']
        cols_ovd    = ['load']
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd)                         # not use True here for ovd cols as using v1 of write_pd_to_hxd
        write_pd_to_hxd(df, path, cols_out, cols_ovd)           # using v1 as 'calculated' part of the override is in the root of the node
    return

@time_me
def rater_save_pc(hxd,rater):
    df          = rater.get('pc_structure', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = hxd.cds.pc.pc_structure.table
        cols_out    = ['selected_lob', 'total_fees', 'market_deductions', 'is_row_visible']
        cols_ovd    = []
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2
   
    df          = rater.get('pc_calc', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = hxd.cds.pc.pc_calculations.details
        cols_out    = [ 'selected_lob',  'is_row_visible',  'bm_class_auto',       'bm_class_applied',
                        'gwp_5623',      'deductions',      'nwp_5623',            'best_estimate_pre_pc_adj',
                        'attr_gg_ulr',   'large_gg_ulr',    'cat_gg_ulr',          'total_gg_ulr',
                        'attr_cov',      'large_cov',       'cat_cov',             
                        'attr_el',       'large_el',        'cat_weather_el',      'cat_non_weather_el',
                        'attr_sd',       'large_sd',        'cat_non_weather_sd',  'cat_weather_sd'             ]
        cols_ovd    = []
        cols_out    = i_t(df, cols_out)
        cols_ovd    = i_t(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2
    return

# below function was great in theory but took 0.2 seconds to run once, with the heavy lifting being constructing the object tree
# HOW TO USE CODE
    # path_policy_data_str    = "hxd.cds.policy_level_data_table.policy_level_data"
    # nodes                   = ds_get_mode_type(  path_policy_data_str  )
    # cols                    = [node for node,mode,hxtype,label in nodes if mode == "input"]
    # cols                   += [node for node,mode,hxtype,label in nodes if mode == "override"]
    # rater['policy_data']    = pd_df_from_hx_list_v2( path_policy_data, cols )

# from algorithms.data_schema_static import hx_calculation_legacy_initial_premium 
# import hx

# @time_me
# def ds_get_mode_type(path):
    
#     def get_node_by_path(structure, path):
#         parts = path.split(".")
#         node = structure
#         for part in parts:
#             node = node.children.get(part)
#             if node is None:
#                 raise ValueError(f"Path '{path}' not found.")
#         return node
    
#     results     = []
#     root        = hx_calculation_legacy_initial_premium()
#     clean_path  = path[4:] if path.startswith("hxd.") else path
#     node_target = get_node_by_path(root, clean_path)

#     if hasattr(node_target, "children"):
#         for name, obj in node_target.children.items():
#             if not hasattr(obj, "children"):
#                 mode = getattr(obj, "mode", None)
#                 field_type = obj.__class__.__name__
#                 view_label = obj.view.get("label") if hasattr(obj, "view") else None
#                 results.append((name, mode, field_type, view_label))
#     return results

