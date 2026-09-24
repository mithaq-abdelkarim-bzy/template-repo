import pandas                    as pd
import algorithms.rate_constants as constants
from libraries.model_profiler.algorithms.profiling_hxd_functions import time_me
from algorithms.rate_utilities                                   import(  pd_df_from_hx_list 
                                                                        , pd_df_from_hx_list_v2
                                                                        , write_pd_to_hxd_v2    
                                                                        , write_pd_to_hxd
                                                                        , get_tp_dict
                                                                        , get_fx_rate)
from algorithms                 import parameter_tables_schema as lib_params


# Returns requested columns that exist in df, preserving input order.
# If ovd_calc=True, checks for "<col>/calculated" in df.columns and returns base names.
def cols_intersect(df,lst,ovd_calc=False):
    if ovd_calc:
        lst  = [f'{x}/calculated' for x in lst]
        cols = [c for c in lst if c in df.columns]
        cols = [c.removesuffix('/calculated') for c in cols]
    else:
        cols = [c for c in lst if c in df.columns]
    return cols


@time_me
def rater_load(hxd,rater):
    rater_load_ec_events(           hxd,rater)
    rater_load_nm_individuals(      hxd,rater)
    rater_load_layers(              hxd,rater)
    rater_load_experience_analysis( hxd,rater)
    rater_load_experience_policy(   hxd,rater)
    rater_load_experience_claim(    hxd,rater)   
    rater_load_tp_and_fx(           hxd,rater)
    return



@time_me
def rater_save(hxd,rater):
    rater_save_ec_events(           hxd,rater)
    rater_save_nm_individuals(      hxd,rater)
    rater_save_experience_analysis( hxd,rater)
    rater_save_experience_policy(   hxd,rater)
    rater_save_experience_claim(    hxd,rater)
    # rater_save_layers(              hxd,rater) # done manually as part of rating summary
    return



#########################
### Load Scripts
#########################

def rater_load_ec_events(hxd,rater):
    path_data = hxd.cds.exposure.granular.event_cancel.events
    cols                    = ['event_name','country','state','date_start','date_end','tiv','venue'
                                ,"ihs_terrorism", "ihs_riots_and_civil_commotion", "ihs_strike", "ihs_war"]
    rater["ec_events_df"]   = pd_df_from_hx_list_v2( path_data, cols )
    return 


def rater_load_nm_individuals(hxd,rater):
    path_data = hxd.cds.exposure.granular.event_cancel.national_mourning.over_75
    cols                    = ['include','name','country','gender','date_of_birth','mod_affluence','mod_health']
    rater["nm_indiv_df"]    = pd_df_from_hx_list_v2( path_data, cols )
    return 


def rater_load_layers(hxd, rater):
    path_data = hxd.cds.layers
    cols                    = [ 'coverages.ec_total.limit',           'coverages.ec_total.excess'
                               ,'coverages.ec_total.deductible',      'coverages.ec_total.excess_use'           # deliberately using ec_total as this is where the limit etc is set
                               ,'currency',  'premium', 'status',     'brokerage',        'written_line',      'section_reference'
                               , 'trifocus', 'is_primary_excess',     'quoted_premium_100',                    'bpi_case_priced']
    rater["layers_df"]      = pd_df_from_hx_list_v2( path_data, cols )
    return 

def rater_load_experience_analysis(hxd, rater):
    path_data = hxd.cds.experience_rating.analysis_table
    cols                    = [ "tiv_ovd",                 "include",     "rate_inc_ovd", "inf_inc_ovd",
                                "attr_pct_ultimate_ovd",   "large_pct_ultimate_ovd",      "cat_pct_ultimate_ovd",
                                "attr_ielr_ovd",           "large_ielr_ovd",              "cat_ielr_ovd",
                                "attr_incurred_ovd",       "large_incurred_ovd",          "cat_incurred_ovd",
                                "gnwp_nominal_ovd"                                                                  ]
    rater["exper_df"]      = pd_df_from_hx_list_v2( path_data, cols )
    return 


def rater_load_experience_policy(hxd, rater):
    path_data = hxd.cds.experience_rating.policy_table
    cols                    = ["policy_ref",   "section_ref",   "yoa",        "coverage_name",  "trifocus_name",
                              "division",      "settlement_fx", "index_bzly", "class_code",     "bool_ec",  "bool_na",
                              "gnwp_bzly_usd", "incurred_bzly_usd",   "gnwp_100_usd",   "incurred_100_usd",
                              "share_bzly",    "rate_chg_init",       "rate_chg",       "fx_rate_usd_sett",
                              "gnwp_bzly",     "incurred_bzly",       "gnwp_100",       "incurred_100"                  ]
    rater["policy_df"]      = pd_df_from_hx_list_v2( path_data, cols )
    return     

def rater_load_experience_claim(hxd, rater):
    path_data = hxd.cds.experience_rating.claim_table
    cols                    = [ "policy_ref", "section_ref", "claim_ref",     "trifocus_name",
                                "division",   "yoa",         "settlement_fx",
                                "cat_code_bzly", "cat_desc_bzly", "cat_code_mkt", "cat_desc_mkt", "cat_bzly_bool",
                                "cause_of_loss", "bool_covid",    "index_bzly",
                                "class_code",    "bool_ec",       "bool_na",       "bool_large",
                                "incurred_bzly", "os_bzly",       "incurred_100",  "share_bzly" ]
    rater["claim_df"]      = pd_df_from_hx_list_v2( path_data, cols )
    return

def rater_load_tp_and_fx(hxd, rater):
    fx_df           = lib_params.fx_rates.df()
    tp_params_df    = lib_params.tp_parameters.df()
    yoa_incept      = hxd.hx_core.inception_date.year
    ccy             = hxd.cds.currencies.source_currency
    fx_rate         = get_fx_rate( fx_df, ccy)    
    tp_dict         = get_tp_dict(tp_params_df, yoa_incept, constants.BP_CLASS, fx_rate)
    rater['tp_dict']= tp_dict
    rater['fx_df']  = fx_df
    return







#########################
### Save Scripts
#########################

@time_me
def rater_save_layers(hxd,rater):
    df          = rater.get('layers_df', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = hxd.cds.layers
        cols_out    = ['fgu_pct', 'description', 'el_fgu_mod', 'el_fgu_mod_adj']
        cols_ovd    = []
        cols_out    = cols_intersect(df, cols_out)
        cols_ovd    = cols_intersect(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2
    return


def rater_save_nm_individuals(hxd,rater):
    df          = rater.get('nm_indiv_df', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = hxd.cds.exposure.granular.event_cancel.national_mourning.over_75
        cols_out    = ['age', 'prob_die', 'prob_live', 'prob_die_mod', 'prob_live_mod', "check"]
        cols_ovd    = []
        cols_out    = cols_intersect(df, cols_out)
        cols_ovd    = cols_intersect(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2
    return


def rater_save_ec_events(hxd,rater):
    df          = rater.get('ec_events_df', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = hxd.cds.exposure.granular.event_cancel.events
        cols_out    = [     "check",
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
                            "net_el_usd_national_mourning_mod"
                            ]
        cols_ovd    = []
        cols_out    = cols_intersect(df, cols_out)
        cols_ovd    = cols_intersect(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2
    return




def rater_save_experience_analysis(hxd,rater):
    df          = rater.get('exper_df', pd.DataFrame()).fillna(0)
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = hxd.cds.experience_rating.analysis_table
        cols_out    = [ "yoa",                    "yoa_label",                "tiv_calc",                   "tiv",

                        "total_ol_selected_ultimate_dup",      "total_ol_selected_ulr_dup",    "total_ol_selected_ult_to_tiv",
                        "gnwp_nominal_calc",      "gnwp_nominal",            "gnwp_ol_dup",                 "gnwp_ol",

                        "attr_incurred_calc",     "attr_incurred",           "attr_pct_ultimate_calc",      "attr_ielr_calc",                        
                        "large_incurred_calc",    "large_incurred",          "large_pct_ultimate_calc",     "large_ielr_calc",
                        "cat_incurred_calc",      "cat_incurred",            "cat_pct_ultimate_calc",       "cat_ielr_calc",

                        "rate_inc_calc",          "rate_inc",                "rate_cum",
                        "inf_inc_calc",           "inf_inc",                 "inf_cum",

                        "attr_ol_incurred",       "large_ol_incurred",       "cat_ol_incurred",             "total_ol_incurred",

                        "attr_pct_ultimate",      "attr_method",            
                        "attr_ol_cl_ultimate",    "attr_ol_bf_ultimate",      "attr_ol_ielr_ultimate",      "attr_ol_selected_ultimate",
                        "attr_ol_cl_lr",          "attr_ol_bf_lr",            "attr_ol_ielr",               "attr_ol_selected_ulr",

                        "large_pct_ultimate",     "large_method",             "large_credibility", 
                        "large_ol_cl_ultimate",   "large_ol_bf_ultimate",     "large_ol_ielr_ultimate",     "large_ol_selected_ultimate",
                        "large_ol_cl_lr",         "large_ol_bf_lr",           "large_ol_ielr",              "large_ol_selected_ulr",

                        "cat_pct_ultimate",       "cat_method",            
                        "cat_ol_cl_ultimate",     "cat_ol_bf_ultimate",       "cat_ol_ielr_ultimate",       "cat_ol_selected_ultimate",
                        "cat_ol_cl_lr",           "cat_ol_bf_lr",             "cat_ol_ielr",                "cat_ol_selected_ulr",

                        "total_pct_ultimate",                
                        "total_ol_cl_ultimate",   "total_ol_bf_ultimate",     "total_ol_ielr_ultimate",     "total_ol_selected_ultimate",
                        "total_ol_cl_lr",         "total_ol_bf_lr",           "total_ol_ielr",              "total_ol_selected_ulr",

                        "wgt_include",            "wgt_decay",                "wgt_exposure",        "wgt_pct_ult",
                        "wgt_overall_initial",    "wgt_overall_final"                                                           ]
        cols_ovd    = []
        cols_out    = cols_intersect(df, cols_out)
        cols_ovd    = cols_intersect(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2
    return


def rater_save_experience_claim(hxd,rater):
    df          = rater.get('claim_df', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = hxd.cds.experience_rating.claim_table
        cols_out    = [ "bool_large",  "incurred_bzly_scc",  "os_bzly_scc",  "incurred_100_scc", "incurred_100_scc_attr", "incurred_100_scc_large", "incurred_100_scc_cat"]
        cols_ovd    = []
        cols_out    = cols_intersect(df, cols_out)
        cols_ovd    = cols_intersect(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2
    return


def rater_save_experience_policy(hxd,rater):
    df          = rater.get('policy_df', pd.DataFrame())
    df_not_empty= not df.empty
    condition   = df_not_empty
    if condition:
        path        = hxd.cds.experience_rating.policy_table
        cols_out    = [ "gnwp_bzly_scc",  "incurred_bzly_scc",  "gnwp_100_scc",  "incurred_100_scc"]
        cols_ovd    = []
        cols_out    = cols_intersect(df, cols_out)
        cols_ovd    = cols_intersect(df, cols_ovd, True)                   # use True here for ovd cols as using v2 of write_pd_to_hxd_v2
        write_pd_to_hxd_v2(df, path, cols_out, cols_ovd)        # using v2
    return