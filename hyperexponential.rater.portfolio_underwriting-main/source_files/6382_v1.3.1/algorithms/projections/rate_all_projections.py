##################################################################################################################################
###### Outstanding
##################################################################################################################################
###### 1) 
###### 2) 
###### 3) 
###### 4) 
###### 5) 
###### 6) 

##################################################################################################################################

import hx
import pandas   as pd
import numpy    as np
from datetime   import datetime
from io         import StringIO
from libraries.model_profiler.algorithms.profiling_hxd_functions        import time_me


import algorithms.rate_utilities                                    as utils
import algorithms.rate_constants                                    as constants
import algorithms.projections.own_experience_helpers                as oeh
import algorithms.projections.l_b_projections_helpers               as lbph



def rate_all_projections(hxd, rater):
    
    # Get policy inception date from HXD
    inception_date = hxd.cds.standard_fields.inception_date
    inception_year = inception_date.year

    # load dataframes
    lloyds_risk_code_data       = hx.params.table_lloyds_risk_code_data                                         # Lloyd’s risk code reference table (static params)
    beazley_data_df             = hx.params.table_beazley_data                                                  # Beazley benchmark data (static params)

    policy_level_df             = rater.get("policy_data",                  pd.DataFrame())                                      # Import policy-level datasets
    claim_level_df              = rater.get("claim_data",                   pd.DataFrame())                                      # Import claim-level datasets
    
    bp_details_df               = rater.get("bp_details",                   pd.DataFrame())                                      # BP projection details
    inflation_df                = rater.get("inflation_data",               pd.DataFrame())                                      # Inflation details
    prem_limit_df               = rater.get("prem_limit_data",              pd.DataFrame())                                      # Premium limit and profile
    
    final_composition_df        = rater.get("risk_composition_final",       pd.DataFrame())
    portfolio_profile_df        = rater.get("portfolio_profile",            pd.DataFrame())
    deductions_df               = rater.get("deductions_df",                pd.DataFrame())
    portfolio_profile_summary_df= rater.get("portfolio_profile_summary",    pd.DataFrame())
    inflation_summary_df        = rater.get("inflation_by_lob",             pd.DataFrame())

    # -------------------------------
    # Run different projections
    # -------------------------------

    # Lloyd’s benchmark projections
    l_b_summary = rate_lloyds_beazley_projections(  hxd,    rater,          inception_year,        final_composition_df, 
                                                    policy_level_df,         lloyds_risk_code_data, deductions_df, 
                                                    portfolio_profile_df,   inflation_df,           bp_details_df,
                                                    beazley_data_df) 

    # Own-experience projections
    rate_own_experience(    hxd,     rater,         inception_year,                 final_composition_df, 
                            policy_level_df,         claim_level_df,                  deductions_df,
                            portfolio_profile_df,   portfolio_profile_summary_df,   inflation_summary_df,
                            prem_limit_df)        
    
    lbph.set_is_tab_shown(hxd)

    return



@time_me
def rate_lloyds_beazley_projections( hxd,                    rater,                  inception_year,         
                                     final_composition_df,   policy_level_df,         lloyds_risk_code_data,  
                                     deductions_df,          portfolio_profile_df,   
                                     inflation_df,           bp_details_df,          beazley_data_df):

    # Exit early if no risk codes in final composition
    if final_composition_df.shape[0] == 0:
        return

    # Retrieve relevant LLOYDS data from the HxData structure
    lloyds_path         = hxd.cds.projections_lloyds
    lloyds_show_all_yrs = lloyds_path.show_all_yrs
    lloyds_lob_1        = lloyds_path.lookup_lob_1
    lloyds_lob_2        = lloyds_path.lookup_lob_2
    lloyds_lob_3        = lloyds_path.lookup_lob_3

    # Retrieve relevant BEAZLEY data from the HxData structure
    bzly_path           = hxd.cds.projections_beazley
    bzly_show_all_yrs   = bzly_path.show_all_yrs
    bzly_lob_1          = bzly_path.lookup_lob_1
    bzly_lob_2          = bzly_path.lookup_lob_2
    bzly_lob_3          = bzly_path.lookup_lob_3

   
    # Create a mapping of historical years to labels like "year_0", "year_1", etc.
    num_yrs     = constants.YEARS_TO_CONSIDER_IN_LLOYDS_PROJECTIONS
    years_dict  = {str(inception_year - i): f"year_{i}" for i in range(0, num_yrs)}

    # prepare dataframes   
    mask_not_nil         = ~np.isclose(final_composition_df["composition"], 0.0, atol=1e-12)
    final_composition_df = final_composition_df[mask_not_nil]   # Filter out risk codes with near-zero composition

    # load data from hxd
    sum_lloyds_df, det_lloyds_df = lbph.load_summary_detail_from_hxd(lloyds_path,'lloyds',rater)
    sum_bzly_df,   det_bzly_df   = lbph.load_summary_detail_from_hxd(bzly_path,'beazley',rater)

    # summary_df - initialise
    sum_lloyds_df= lbph.summary_initialise(      sum_lloyds_df, final_composition_df, lloyds_lob_1, lloyds_lob_2, lloyds_lob_3, 'lloyds' )
    sum_bzly_df  = lbph.summary_initialise(      sum_bzly_df,   final_composition_df,   bzly_lob_1,   bzly_lob_2,   bzly_lob_3, 'beazley')
    summary_df   = pd.concat([sum_lloyds_df, sum_bzly_df], axis=0, ignore_index=True)

    # summary_df - set basic values
    summary_df  = lbph.summary_add_aqn(                      summary_df, deductions_df            )
    summary_df  = lbph.summary_add_bp_cat_load(              summary_df, bp_details_df            )

    # detail_df - initialise
    det_lloyds_df= lbph.detail_initialise(                   det_lloyds_df, inception_year,     num_yrs, 'lloyds' )
    det_bzly_df  = lbph.detail_initialise(                   det_bzly_df  , inception_year,     num_yrs, 'beazley')
    detail_df    = pd.concat([det_lloyds_df, det_bzly_df], axis=0, ignore_index=True    )    
    detail_df    = lbph.detail_add_summary_info_and_filter(  detail_df, summary_df       )

    # detail_df - add loss data & development - notice we add lloyds to everything eliminating the financials on bzly
    detail_df    = lbph.detail_add_lloyds_data(              detail_df,   lloyds_risk_code_data)
    detail_df    = lbph.detail_add_bzly_data(                detail_df,   beazley_data_df      )
    detail_df    = lbph.detail_add_bzly_dev(                 detail_df                         )

    # Determine on-levelling - rate change & inflation
    detail_df   = lbph.detail_add_rate_change(               detail_df, portfolio_profile_df, inception_year  )
    detail_df   = lbph.detail_add_inflation(                 detail_df, inflation_df,         inception_year  )
    detail_df   = lbph.detail_add_onlevel_ratios(            detail_df           )

    # Determine Ultimate Premiums and chainladder (CL) losses
    detail_df   = lbph.detail_add_ultimate_premiums(         detail_df)
    detail_df   = lbph.detail_add_cl_ultimate_losses(        detail_df)

    # Determine Weightings and Reserving methods
    detail_df   = lbph.detail_add_weighting_1_exposure(      detail_df                )
    detail_df   = lbph.detail_add_weighting_2_decay_ratio(   detail_df, inception_year)
    detail_df   = lbph.detail_add_weighting_3_development(   detail_df                )
    detail_df   = lbph.detail_add_weighting_overall(         detail_df                )
    detail_df   = lbph.detail_add_reserving_method(          detail_df                )

    # Determine IELRs
    detail_df   = lbph.detail_add_helpers_summary_ielr(      detail_df                )   
    detail_df, summary_df  = lbph.det_sum_add_ielr(          detail_df, summary_df    )   

    # Determine remaining methods and on-levelling
    detail_df   = lbph.detail_add_ielr_ultimate_losses(      detail_df)
    detail_df   = lbph.detail_add_bf_ultimate_losses(        detail_df)
    detail_df   = lbph.detail_add_blend_ultimate_losses(     detail_df)
    detail_df   = lbph.detail_add_onlevel_ulr(               detail_df)

    # Determine helpers for any complex totals needed, visible rows
    detail_df   = lbph.detail_add_total_helpers(             detail_df)
    detail_df   = lbph.detail_add_visible_rows(              detail_df, lloyds_show_all_yrs, bzly_show_all_yrs )     

    # Determine Summary from details and add additional columns
    summary_df  = lbph.summary_grp_details(                  summary_df, detail_df   )
    summary_df  = lbph.summary_add_final_lr_calcs(           summary_df              )

    # write to hxd
    # lbph.save_df_to_hxd(                                     detail_df, summary_df, lloyds_path, bzly_path)
    lbph.save_unique_lobs_to_hxd(                                       summary_df, lloyds_path, bzly_path)
    lbph.save_selected_lob_to_hxd(                           detail_df, summary_df, lloyds_path, bzly_path)

    rater['proj_lloyds_summary']  = summary_df[(summary_df['projection_data'] == 'lloyds' )].reset_index()
    rater['proj_beazley_summary'] = summary_df[(summary_df['projection_data'] == 'beazley')].reset_index()
    
    rater['proj_lloyds_detail']   = detail_df[(detail_df['projection_data'] == 'lloyds' )].reset_index()
    rater['proj_beazley_detail']  = detail_df[(detail_df['projection_data'] == 'beazley')].reset_index()


    return summary_df




@time_me
def rate_own_experience( hxd,                    rater,                  inception_year,     
                         final_composition_df,   policy_level_df,         claim_level_df,     
                         deductions_df,          portfolio_profile_df,   portfolio_profile_summary_df,
                         inflation_summary_df,   prem_limit_df):

    # Exit if there is no composition or premium data to work with
    test1 = hxd.cds.risk_information.prem_data_available == False
    test2 = final_composition_df.shape[0] == 0
    test3 = policy_level_df.shape[0] == 0
    if test1 or test2 or test3:
        return

    # Retrieve relevant data from the HxData structure
    non_cds_rcc             = hxd.non_cds.risk_code_composition
    own_experience_path     = hxd.cds.projections_own_experience
    show_all_yrs            = own_experience_path.show_all_yrs
    selected_lob_1          = own_experience_path.selected_lob_1
    selected_lob_2          = own_experience_path.selected_lob_2
    selected_lob_3          = own_experience_path.selected_lob_3
    selected_lob_4          = own_experience_path.selected_lob_4
    selected_lob_5          = own_experience_path.selected_lob_5

    lloyds_summary_df       = rater.get('proj_lloyds_summary',  pd.DataFrame())
    beazley_summary_df      = rater.get('proj_beazley_summary', pd.DataFrame())
    bp_summary_df           = rater.get('bp_summary_by_lob', pd.DataFrame())

    # toggle show_detail based on show_compact
    own_experience_path.show_compact = own_experience_path.show_detail==False

    # Create a mapping of historical years to labels like "year_0", "year_1", etc.
    num_yrs     = constants.YEARS_TO_CONSIDER_IN_OWN_EXPERIENCE
    years_dict  = {str(inception_year - i): f"year_{i}" for i in range(0, num_yrs)}

    ###########################################
    # summarise policy & claims data
    ###########################################
    pol_sum_df      = oeh.build_policy_summary_df( policy_level_df)
    claim_sum_df    = oeh.build_claim_summary_df(  claim_level_df )

    ###########################################
    # Load and manipulate the summary data
    ###########################################
    # Extract unique selected LOBs and populate the summary table
    # add these to the summary    'lloyds_final_gn_ulr', 'lloyds_selected_ielr', 'lloyds_model_ielr', 'beazley_final_gn_ulr' 
    # force "claims to develop to ultimate" to be "Open + Closed" when claim source is policy level data and show an error message
    summary_df              = rater.get("proj_own_exper_summary", pd.DataFrame())
    summary_df              = oeh.set_sum_lob_number(                        prem_limit_df, summary_df, selected_lob_1,  selected_lob_2,   selected_lob_3, selected_lob_4, selected_lob_5)
    summary_df              = oeh.calculate_portfolio_profile_summary_by_lob(summary_df,    lloyds_summary_df, beazley_summary_df, portfolio_profile_df)
    summary_df              = oeh.check_policy_data_x_open_claim(            summary_df,    hxd)


    ###########################################
    # Load and manipulate the detail data
    ###########################################
    # Set YOA, lob number, append values in cols_sum to detail_df from summary_df dropping any in-situ columns, filter detail to just active lobs
    detail_df = rater.get("proj_own_exper_detail", pd.DataFrame())
    detail_df = oeh.add_yoa_lob_number(           detail_df,  inception_year,     num_yrs)
    detail_df = oeh.add_summary_info_and_filter(  detail_df, summary_df)

    # Calculate financial and claims data
    detail_df = oeh.add_policy_data(          detail_df, pol_sum_df   )
    detail_df = oeh.add_acquisition_cost(     detail_df, deductions_df    )
    detail_df = oeh.calc_gnpi(                detail_df                   )
    detail_df = oeh.add_claims_data(          detail_df, claim_sum_df     )
    detail_df = oeh.assign_claims(            detail_df                   )
    detail_df = oeh.calculate_movement(       detail_df                   )
    detail_df = oeh.calculate_gn_ilr(                         detail_df)


    # Calculate ldf, rate change, inflation and factors thereon
    detail_df = oeh.calculate_ldf_and_rate_change(            detail_df, portfolio_profile_summary_df, hxd)
    detail_df = oeh.calculate_applied_inflation(              detail_df, inflation_summary_df)
    detail_df = oeh.calculate_on_level_indices(               detail_df                 )

    # Calculate premiums and weightings
    detail_df = oeh.calculate_ultimate_premium_selected(      detail_df                 )
    detail_df = oeh.calculate_exposure_weighting_1(           detail_df                 )
    detail_df = oeh.calculate_decay_ratio_weighting_2(        detail_df, inception_year )
    detail_df = oeh.calculate_developed_weighting_3(          detail_df                 )
    detail_df = oeh.calculate_modelled_weighting(             detail_df                 )
    detail_df = oeh.calculate_ielr_weighting(                 detail_df                 )

    # Calculate ult method, ielrs and propogate back to detail_df
    detail_df = oeh.calculate_method_incurred(                detail_df)
    detail_df = oeh.calculate_ultimate_incurred_cl(           detail_df)
    summary_df= oeh.calculate_ielr_fields(                    detail_df, summary_df) ### NOTICE RETURNS SUMMARY DF
    detail_df = oeh.append_ielr(                              detail_df, summary_df)

    # Calculate various ultimate incurred and ULR values
    detail_df = oeh.calculate_ultimate_incurred_ielr(         detail_df)
    detail_df = oeh.calculate_ultimate_incurred_bf(           detail_df)
    detail_df = oeh.calculate_additional_ibnr(                detail_df)
    detail_df = oeh.calculate_ultimate_incurred_selected(     detail_df)
    detail_df = oeh.calculate_ultimate_ulr_selected(          detail_df)
    detail_df = oeh.calculate_on_levelled(                    detail_df)

    # set row visibility
    detail_df = oeh.calculate_visible_detail_rows(            detail_df, show_all_yrs)
    detail_df = oeh.calculate_where_detail_overrides(         detail_df              )

    # collapse data in detail_df to the totals needed in summary_df
    summary_df= oeh.calculate_summary_totals(                 detail_df, summary_df) ### NOTICE RETURNS SUMMARY DF
    summary_df= oeh.calculate_cat_gn_ulr_bp(                  summary_df, bp_summary_df)
    summary_df= oeh.calculate_cat_gn_ulr_rms(                 summary_df, hxd)
    summary_df= oeh.set_cat_gn_ulr_and_totals(                summary_df)
    summary_df= oeh.get_lloyds_bzy_lrs(           hxd, rater, summary_df)
    
    # Save the results to the data model
    # oeh.save_df_to_hxd(                                       detail_df, summary_df, own_experience_path)
    oeh.save_unique_lobs_to_hxd(                                         summary_df, own_experience_path)
    oeh.save_selected_lob_to_hxd(                             detail_df, summary_df, own_experience_path)
   
    rater["proj_own_exper_summary"] = summary_df
    rater["proj_own_exper_detail"]  = detail_df
 
    return



