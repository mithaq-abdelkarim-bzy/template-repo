import hx
import math as math
import algorithms.rate_utilities as utils
import numpy as np
import pandas as pd
import algorithms.rate_constants as constants
from datetime import datetime
from libraries.model_profiler.algorithms.profiling_hxd_functions import time_me



# @time_me
def cols_exclude_fillna():
    return[ ]


# @time_me
def load_summary_detail_from_hxd(path, projection_data, rater):
    def clean_columns(df):
        df.columns = (
            df.columns
            .str.replace(".", "/", regex=False)
            .str.replace("/selected", "", regex=False)
        )
        return df

    # setup initial dataframes fixing the labelling issue from pd_df_from_hx_list_v2
    summary_df  = rater.get(f"proj_{projection_data}_summary", pd.DataFrame())
    detail_df   = rater.get(f"proj_{projection_data}_detail",  pd.DataFrame())
    
    summary_df  = clean_columns(summary_df)
    detail_df   = clean_columns(detail_df)                    
    
    summary_df['projection_data'] = projection_data
    detail_df[ 'projection_data'] = projection_data

    return summary_df, detail_df



# @time_me
def summary_initialise(summary_df, final_composition_df, lookup_lob_1, lookup_lob_2, lookup_lob_3, projection_data):

    # filter summary_df
    num_summ_rows                = summary_df.shape[0]
    num_comp_rows                = final_composition_df.shape[0]
    num_lobs                     = min(num_summ_rows, num_comp_rows)
    num_start                    = 1 if projection_data == 'lloyds' else 1001  #lob numbers for lloyds start at 1 and beazley 1001 

    # assign values from composition data
    comp_cols   = ['risk_code', 'selected_lob', 'selected_bp_class', 'selected_trifocus', 'composition']
    sum_cols    = ['risk_code', 'selected_lob', 'bp_class',          'tracker_class',     'composition']
    summary_df.loc[:num_lobs-1, sum_cols]         = final_composition_df.loc[:num_lobs-1, comp_cols].values           

    summary_df["lob_number"]     = range(num_start, num_start + num_summ_rows)
    summary_df['yoa']            = "Total"   
    summary_df['lookup_lob']     = summary_df['selected_lob'] + ' - ' + summary_df['risk_code']
    
    summary_df["is_row_visible"] = summary_df["risk_code"].notna()
    summary_df["lob_visible_1"]  = np.where(summary_df["lookup_lob"] == lookup_lob_1, True, False)
    summary_df["lob_visible_2"]  = np.where(summary_df["lookup_lob"] == lookup_lob_2, True, False)
    summary_df["lob_visible_3"]  = np.where(summary_df["lookup_lob"] == lookup_lob_3, True, False)
    summary_df["lob_visible_4"]  = np.where(summary_df["lookup_lob"] == lookup_lob_3, True, False)
    summary_df["lob_visible_5"]  = np.where(summary_df["lookup_lob"] == lookup_lob_3, True, False)    
    summary_df                   = summary_df[summary_df["risk_code"].notna()]    

    return summary_df

# @time_me
def summary_add_aqn(summary_df, deductions_df):
    
    # faster than merge operation where single column with clear relationship and values always on both side.
    # would not work if possibility values were missing in acquisition table
    summary_df['model_acc_aqn'] = summary_df['selected_lob'].map(
                                                  dict(zip(deductions_df['selected_lob']
                                                , deductions_df['selected_effective_deductions'])))
    summary_df['selected_acc_aqn'] = summary_df['model_acc_aqn']
    return summary_df


# @time_me
def summary_add_bp_cat_load(summary_df, bp_details_df):

    # Build mapping dictionary
    risk_to_cat_load                     = dict(  zip(  bp_details_df["risk_code"]
                                                      , bp_details_df["selected_cat_gn_ulr"]           ))

    # Apply mapping conditionally
    mask_bp_cat = (summary_df["bp_cat"]) | (summary_df["cat_lr_source"] == 'Business Plan')
    summary_df["bp_cat_load/calculated"] = np.where(    mask_bp_cat
                                                      , summary_df["risk_code"].map(risk_to_cat_load)
                                                      , np.nan                                          )

    # Resolve overridden vs calculated Cat GN ULR
    summary_df["bp_cat_load"]            = np.where(    summary_df["bp_cat_load/is_overridden"]
                                                      , summary_df["bp_cat_load"]
                                                      , summary_df["bp_cat_load/calculated"]            )

    return summary_df



# @time_me
def detail_initialise(detail_df, inception_year, num_yrs, projection_data):
    num_rows    = detail_df.shape[0]
    num_lobs    = num_rows // num_yrs
    num_start   = 1 if projection_data == 'lloyds' else 1001  #lob numbers for lloyds start at 1 and beazley 1001 
    start_year  = inception_year - (num_yrs - 1)
    
    detail_df["lob_number"] = np.repeat(    np.arange(num_start,  num_start + num_lobs),  num_yrs )    # implicitly will ignore any partial groups as intended, not that this should occur
    detail_df["yoa"]        = np.tile(      np.arange(start_year, inception_year   + 1),  num_lobs)    # Build yoa column from inception_year backwards
    detail_df['is_row_visible'] = True

    if num_rows % num_yrs != 0:
        print("Warning: Some rows may not be assigned a lob_number due to incomplete group.")

    return utils.safe_fillna_except(detail_df,cols_exclude_fillna())



# @time_me
def detail_add_summary_info_and_filter(detail_df, summary_df):
    cols_sum        = [   'selected_lob'               , 'risk_code',       'lookup_lob'
                        , 'projection_type'            , 'ielr_approach'    
                        , 'ielr_source'                , 'cat_lr_source'
                        , 'selected_ielr/is_overridden', 'selected_ielr' 
                        , "lob_visible_1"              , "lob_visible_2",   "lob_visible_3" , "lob_visible_4",   "lob_visible_5"  ]
    
    detail_df       = utils.drop_and_merge(     detail_df,   summary_df[cols_sum+["lob_number"]],    on="lob_number")
    not_na_mask     = detail_df['risk_code'].notna()
    detail_df       = detail_df[ not_na_mask ]
    return  utils.safe_fillna_except(detail_df,cols_exclude_fillna())



# @time_me
def detail_add_lloyds_data(detail_df, lloyds_df):

    # specify columns to join on
    cols_on             = ["risk_code",  "yoa"]
    
    # specify risk code, financial & development columns names - lloyds (orig) and detail (new)
    rc_cols_new        = ["risk_code"]
    rc_cols_orig       = ["lloyds_risk_code"]

    fin_cols_new        = ["latest_gpi", "latest_gnpi", "latest_paid",          "latest_incurred"]
    fin_cols_orig       = ["gpi",        "gnpi",        "latest_paid_position", "latest_incurred_position"]
    
    dev_cols            = ["dev_patterns_gnpi",  "dev_patterns_paid",  "dev_patterns_incurred" ]
    dev_cols_new        = [col + "/calculated" for col in dev_cols]
    dev_cols_orig       = ["premium_development",           "paid_development",              "incurred_development"             ]

    # force data for 2004 & prior with nil premium to be 100 percent developed
    dev_100_year            = constants.LLOYDS_YEAR_ASSUME_FULLY_DEV             
    mask_dev                = (lloyds_df['yoa'] <= dev_100_year) & (lloyds_df['gpi'] == 0)
    lloyds_df.loc[mask_dev, dev_cols_orig] = 1

    # rename columns in lloyds data and change yoa to string consistent with detail_df
    cols_dict           = dict(zip(  rc_cols_orig + fin_cols_orig + dev_cols_orig,  rc_cols_new + fin_cols_new + dev_cols_new   ))
    lloyds_df           = lloyds_df.rename( columns = cols_dict )

    # join detail_df and lloyds_df dropping the columns to be added from detail_df 
    detail_df           = utils.drop_and_merge(    detail_df,    lloyds_df[  fin_cols_new + dev_cols_new + cols_on  ],    on=cols_on)

    # Development - use override where assigned
    for col in dev_cols:
        detail_df[col] = np.where(  detail_df[f"{col}/is_overridden"],    detail_df[col],    detail_df[f"{col}/calculated"])

    # for Beazley we want to keep the development factors but not the lloyds financials
    mask_bzly = detail_df['projection_data'] == 'beazley'
    detail_df.loc[mask_bzly, fin_cols_new] = None

    # Calculate Acquisition cost ratio & Incurred loss ratio
    detail_df['acquisition_ratio']   = utils.ratio(   detail_df['latest_gpi'] - detail_df['latest_gnpi'],  detail_df['latest_gpi']) 
    detail_df['incurred_loss_ratio'] = utils.ratio(   detail_df['latest_incurred'],  detail_df['latest_gnpi']  )
    
    return  utils.safe_fillna_except(detail_df,cols_exclude_fillna())



# @time_me
def detail_add_bzly_data(detail_df, beazley_data_df):

    # calc gpi as gnpi + aqn
    beazley_data_df["gpi"] = beazley_data_df["gn_written_premium"] + beazley_data_df["acquisition_costs"]

    # specify columns to join on
    cols_on             = ["risk_code",  "yoa"]
    
    # specify risk code, financial & development columns names - lloyds (orig) and detail (new)
    rc_cols_new        = ["risk_code"]
    rc_cols_orig       = ["risk_code"]

    prem_cols_new        = ["bzly_gpi",   "bzly_gnpi"         ]
    prem_cols_orig       = ["gpi",        "gn_written_premium"  ]
    
    loss_cols_new        = ["bzly_tot_paid", "bzly_tot_inc",   "bzly_tot_paid_x_cat",  "bzly_tot_inc_x_cat"  ]
    loss_cols_orig       = ["paid_total",    "incurred_total", "paid_total_ex_cat",    "incurred_total_ex_cat"]

    # rename columns in lloyds data and change yoa to string consistent with detail_df
    cols_dict           = dict(zip(    rc_cols_orig + prem_cols_orig + loss_cols_orig
                                    ,  rc_cols_new  + prem_cols_new  + loss_cols_new  ))
    beazley_data_df     = beazley_data_df.rename( columns = cols_dict )

    # join detail_df and lloyds_df dropping the columns to be added from detail_df 
    detail_df = utils.drop_and_merge( detail_df,  beazley_data_df[ prem_cols_new + loss_cols_new + cols_on ],  on=cols_on)

    # assign beazley data - premium and claims to detail_df considering if all or x-cat and drop unused columns
    mask_bzly   = detail_df['projection_data'] == 'beazley'
    mask_x_cat  = detail_df["cat_lr_source"]   == 'Business Plan'
    mask_i_cat  = mask_x_cat == False 
    
    detail_df.loc[ mask_bzly             , "latest_gpi"  ]    = detail_df["bzly_gpi"]
    detail_df.loc[ mask_bzly             , "latest_gnpi" ]    = detail_df["bzly_gnpi"]

    detail_df.loc[ mask_bzly & mask_x_cat, "latest_paid" ]    = detail_df["bzly_tot_paid_x_cat"]
    detail_df.loc[ mask_bzly & mask_i_cat, "latest_paid" ]    = detail_df["bzly_tot_paid"]

    detail_df.loc[ mask_bzly & mask_x_cat, "latest_incurred"] = detail_df["bzly_tot_inc_x_cat"]
    detail_df.loc[ mask_bzly & mask_i_cat, "latest_incurred"] = detail_df["bzly_tot_inc"]

    detail_df   = detail_df.drop(  prem_cols_new + loss_cols_new,  axis=1 )

    # Calculate Acquisition cost ratio & Incurred loss ratio
    detail_df['acquisition_ratio']   = utils.ratio(   detail_df['latest_gpi'] - detail_df['latest_gnpi'],  detail_df['latest_gpi']) 
    detail_df['incurred_loss_ratio'] = utils.ratio(   detail_df['latest_incurred'],  detail_df['latest_gnpi']  )
    
    return  utils.safe_fillna_except(detail_df,cols_exclude_fillna())



# @time_me
def detail_add_bzly_dev(detail_df):

    ## for beazley development we currently have lloyds unadjusted development factors loaded
    ## we need to interpolate these to reflect the different as at date on the beazley data

    
    # Get Beazley & Lloyds as at dates & convert to datetime objects & calculate difference (offset) using year_frac
    # use calculated offset to infer the floor & ceil to offset the data
    date_lloyds     = datetime.strptime(constants.LLOYDS_DATA_CUTOFF_DATE, '%Y-%m-%d')
    date_beazley    = datetime.strptime(constants.BEAZLEY_DATA_CUTOFF_DATE, '%Y-%m-%d')
    offset          = utils.year_frac(date_lloyds, date_beazley)
    offset_floor    = math.floor(offset)
    offset_ceil     = offset_floor + 1

    # calculate percent weighting to floor & ceiling arrays
    pct_floor       = offset_ceil - offset   
    pct_ceil        = 1 - pct_floor          

    # calc value to fill misaligned cells
    # positive number shifts array down so na at top on oldest year hence 100% dev, v-a-v negative use 0%
    filler          = 1 if offset>=0 else 0  

    # specify column names
    dev_cols            = ["dev_patterns_gnpi",  "dev_patterns_paid",  "dev_patterns_incurred" ]
    dev_cols_calc       = [col + "/calculated" for col in dev_cols]
    dev_cols_is_ovd     = [col + "/is_overridden" for col in dev_cols]
    dev_cols_floor      = [col + "/floor"      for col in dev_cols]
    dev_cols_ceil       = [col + "/ceil"       for col in dev_cols] 
    
    all_cols_orig       = [col + "/calculated" for col in dev_cols] + ["lob_number"]
    all_cols_floor      = [col + "/floor" for col in dev_cols]  + ["lob_number_floor"]
    all_cols_ceil       = [col + "/ceil" for col in dev_cols]  + ["lob_number_ceil"]
    
    detail_df[all_cols_floor] = detail_df[all_cols_orig].shift(  offset_floor  ).fillna(  filler  )
    detail_df[all_cols_ceil ] = detail_df[all_cols_orig].shift(  offset_ceil   ).fillna(  filler  )

    mask_filler_floor   = (detail_df["lob_number"] != detail_df["lob_number_floor"])
    mask_filler_ceil    = (detail_df["lob_number"] != detail_df["lob_number_ceil" ])

    detail_df.loc[mask_filler_floor, dev_cols_floor] = filler
    detail_df.loc[mask_filler_ceil,  dev_cols_ceil ] = filler

    # only want to apply this logic to beazley data
    mask_bzly                   = detail_df['projection_data'] == 'beazley'
    slice_bzly                  = detail_df.loc[mask_bzly]
    detail_df.loc[mask_bzly,dev_cols_calc]  = (   slice_bzly[ dev_cols_floor].to_numpy() * pct_floor        #to_numpy used here to handle a potential index misalignment
                                                + slice_bzly[ dev_cols_ceil ].to_numpy() * pct_ceil  )
    
    # calculating the selected value allowing for overrides
    detail_df[dev_cols]  = np.where(  detail_df[dev_cols_is_ovd],    detail_df[dev_cols],    detail_df[dev_cols_calc])

    return  utils.safe_fillna_except(detail_df,cols_exclude_fillna())


# EXISTING CODE /spreadsheet only uses risk_code but looking at cfc we can see duplicate risk codes
# Selected_lob is what is available to improve the join and now implemented
# facility lob would be optimal (via backtracking through the spreadsheet) but not in inflation details
# hence logic keep first row
# @time_me
def detail_add_rate_change(detail_df, pp_df, inception_year):

    # flick pp_df to long form
    pp_l_df = pp_df.melt( id_vars=['risk_code', 'selected_lob'],   var_name='metric_year',   value_name='value')

    # Split metric and year
    pp_l_df[['metric', 'year']] = pp_l_df['metric_year'].str.extract(r'(.*)/year_(\d+)')
    pp_l_df['yoa']              = inception_year - pp_l_df['year'].fillna(0).astype(int)

    pp_metrics  = ['rate_change_no_override','rate_change_with_selection_override']
    pp_mask     = pp_l_df['metric'].isin(pp_metrics)
    pp_l_df     = pp_l_df[pp_mask]

    # flick pp_l_df to wide form with metrics on columns
    # notice we force it to only keep the first row 
    pp_w_df         = pp_l_df.pivot_table(  index= ['risk_code', 'selected_lob', 'yoa']
                                          , columns='metric'
                                          , values='value'
                                          , aggfunc='first'  ).reset_index()


    # determine the column names that will need to be dropped following the merge
    cols_detail = detail_df.columns
    cols_pp     = pp_w_df.columns
    cols_extra  = [col for col in cols_pp if col not in cols_detail]
    cols_on     =  ['risk_code', 'selected_lob', 'yoa']

    # merge portfolio profile on selected lob
    detail_df   = utils.drop_and_merge(  detail_df,    pp_w_df,    on = cols_on )

    # assign values
    detail_df['rate_change_model']               = detail_df['rate_change_no_override']               
    detail_df['rate_change_selected/calculated'] = detail_df['rate_change_with_selection_override']               
    detail_df['rate_change_selected']            = np.where(  detail_df['rate_change_selected/is_overridden']
                                                            , detail_df['rate_change_selected']
                                                            , detail_df['rate_change_selected/calculated']    )

    # drop any columns not needed
    detail_df   = detail_df.drop(columns = cols_extra)
    
    return  utils.safe_fillna_except(detail_df,cols_exclude_fillna())


# EXISTING CODE /spreadsheet only uses risk_code but looking at cfc we can see duplicate risk codes
# Selected_lob is what is available to improve the join and now implemented
# facility lob would be optimal (via backtracking through the spreadsheet) but not in inflation details
# hence logic keep first row
# @time_me
def detail_add_inflation(detail_df, inf_df, inception_year):
    # flick pp_df to long form 
    # notice we force it to only keep the first row 
    inf_l_df            = inf_df.melt( id_vars=['risk_code','selected_lob'],   var_name='metric_year',  value_name='value')
    inf_l_df            = inf_l_df[inf_l_df['metric_year'].str.startswith('year_')]
    inf_l_df            = inf_l_df[ ~inf_l_df['metric_year'].str.contains('/')]   # we dont need all the additional just main selected
    inf_l_df            = inf_l_df.drop_duplicates(subset=['risk_code','selected_lob', 'metric_year'],    keep='first')
    inf_l_df['year']    = inf_l_df['metric_year'].str.extract(r'year_(\d+)')   # different pattern vs rate change
    inf_l_df['yoa']     = inception_year - inf_l_df['year'].fillna(0).astype(int)        
    
    # determine the column names that will need to be dropped following the merge
    cols_detail = detail_df.columns
    cols_inf    = inf_l_df.columns
    cols_extra  = [col for col in cols_inf if col not in cols_detail]
    cols_on     = ['risk_code', 'selected_lob', 'yoa']

    # merge portfolio profile on selected lob
    detail_df   = utils.drop_and_merge(  detail_df,    inf_l_df,    on = cols_on )

    # assign values
    detail_df['inflation_model']  = detail_df['value']               

    # drop any columns not needed
    detail_df   = detail_df.drop(columns = cols_extra)
    
    return  utils.safe_fillna_except(detail_df,cols_exclude_fillna())


# @time_me
def detail_add_onlevel_ratios(detail_df):
    # convert inflation to an incremental index
    detail_df['inflation_model_plus_1'] = 1 + detail_df['inflation_model'] 

    # get cumulative amount by year ascending, get overall product, product/cumul gives the index needed.
    for col in ['rate_change_model', 'rate_change_selected', 'inflation_model_plus_1']:
        detail_df[col           ] = pd.to_numeric(detail_df[col], errors='coerce')
        ss_col                    = detail_df.groupby("lob_number")[col]
        detail_df[f'{col}_cumul'] = ss_col.cumprod()
        detail_df[f'{col}_prod' ] = ss_col.transform('prod')
        detail_df[f'{col}_index'] = utils.ratio(    detail_df[f'{col}_prod' ],     detail_df[f'{col}_cumul']   )

    # fix resulting name on inflation to be consistent to schema
    detail_df['inflation_model_index'] = detail_df['inflation_model_plus_1_index']

    detail_df['loss_ratio_model_index']     = utils.ratio(   detail_df['inflation_model_index']
                                                           , detail_df['rate_change_model_index']
                                                           , 1 )
    detail_df['loss_ratio_selected_index']  = utils.ratio(   detail_df['inflation_model_index']
                                                           , detail_df['rate_change_selected_index']
                                                           , 1 )

    return utils.safe_fillna_except(detail_df,cols_exclude_fillna())


# @time_me
def detail_add_ultimate_premiums(detail_df):
    # calculate ultimate premiums including on-levelled
    detail_df['ultimate_gnpi']              = utils.ratio(   detail_df['latest_gnpi'], detail_df['dev_patterns_gnpi']  )
    detail_df['ultimate_gnpi_ol_model']     = detail_df['ultimate_gnpi']  *  detail_df['rate_change_model_index']
    detail_df['ultimate_gnpi_ol_selected']  = detail_df['ultimate_gnpi']  *  detail_df['rate_change_selected_index']

    return utils.safe_fillna_except(detail_df,cols_exclude_fillna())


# @time_me
def detail_add_cl_ultimate_losses(detail_df):
    
    # calculate ultimate paid & ulr associated
    detail_df['ultimate_cl_paid']           = utils.ratio(   detail_df['latest_paid'],       detail_df['dev_patterns_paid']  )
    detail_df['ultimate_cl_paid_ulr']       = utils.ratio(   detail_df['ultimate_cl_paid'],  detail_df['ultimate_gnpi']      )
    
    # calculate ultimate incurred & ulr associated
    detail_df['ultimate_cl_incurred']       = utils.ratio(   detail_df['latest_incurred'],      detail_df['dev_patterns_incurred'] )
    detail_df['ultimate_cl_incurred_ulr']   = utils.ratio(   detail_df['ultimate_cl_incurred'], detail_df['ultimate_gnpi']         )

    return utils.safe_fillna_except(detail_df,cols_exclude_fillna())


# @time_me
def detail_add_weighting_1_exposure(detail_df):
    # Max on-level GNPI & GNPI by selected LOB
    lob_max_gnpi_df = (detail_df[['lob_number','ultimate_gnpi_ol_selected', 'ultimate_gnpi']]
                            .groupby('lob_number')
                            .max()   
                            .reset_index()              
                            .rename(columns={   "ultimate_gnpi_ol_selected": "max_gnpi_ol"
                                              , "ultimate_gnpi":             "max_gnpi"     }))

    # Add Max on-level back to detail_df
    detail_df       = utils.drop_and_merge(detail_df, lob_max_gnpi_df, on = ["lob_number"])

    # test if max_gnpi_ol = 0 then 0 else min (1, gnpi/max_gnpi_ol)
    detail_df['weighting_1_exposure_onlevel']   = utils.ratio(    detail_df['ultimate_gnpi_ol_selected'],   detail_df['max_gnpi_ol'])
    detail_df['weighting_1_exposure_onlevel']   = np.minimum( 1,  detail_df['weighting_1_exposure_onlevel']                         )

    # test if max_gnpi = 0 then 0 else min (1, gnpi/max_gnpi)
    detail_df['weighting_1_exposure_nominal']   = utils.ratio(    detail_df['ultimate_gnpi'],               detail_df['max_gnpi'])
    detail_df['weighting_1_exposure_nominal']   = np.minimum( 1,  detail_df['weighting_1_exposure_nominal']                              )

    return detail_df



def detail_add_weighting_2_decay_ratio(detail_df, inception_year):
    decay       = constants.DECAY_RATIO
    detail_df["weighting_2_decay_ratio"] = decay **   ( inception_year - detail_df["yoa"] ) # yoa is a int64 at this point hence can subtract
    return detail_df


# @time_me
def detail_add_weighting_3_development(detail_df):
    # Developed weighting = incurred pattern
    detail_df["weighting_3_developed"] = detail_df["dev_patterns_incurred"].fillna(0)
    return detail_df


# @time_me
def detail_add_weighting_overall(detail_df):

    # on-level weighting
    detail_df['weighting_onlevel'] = (     detail_df['weighting_1_exposure_onlevel'] 
                                        *  detail_df['weighting_2_decay_ratio'] 
                                        *  detail_df['weighting_3_developed']        ).fillna(0)

    # nominal weighting
    detail_df['weighting_nominal'] = (     detail_df['weighting_1_exposure_nominal'] 
                                        *  detail_df['weighting_2_decay_ratio'] 
                                        *  detail_df['weighting_3_developed']        ).fillna(0)

    # Sum weight by selected LOB
    lob_sum_wgt_df  = (detail_df[['lob_number','weighting_onlevel','weighting_nominal']]
                            .groupby("lob_number")
                            .sum()   
                            .reset_index()              
                            .rename(columns={   'weighting_onlevel':    'sum_wgt_ol'
                                              , 'weighting_nominal':    'sum_wgt_nom'     }))

    # Add sum_cl_wgt back to detail_df
    detail_df       = utils.drop_and_merge(detail_df, lob_sum_wgt_df, on = ["lob_number"])

    # Normalize
    detail_df['weighting_onlevel'] = utils.ratio(  detail_df['weighting_onlevel'],  detail_df["sum_wgt_ol"]  ).fillna(0)
    detail_df['weighting_nominal'] = utils.ratio(  detail_df['weighting_nominal'],  detail_df["sum_wgt_nom"] ).fillna(0)
    
    # assign model default weights
    mask_nominal                 = detail_df['ielr_approach'] == 'Nominal'
    detail_df['weighting_model'] = np.where(mask_nominal,   detail_df['weighting_nominal'],   detail_df['weighting_onlevel'])
    
    # assign selected weights including override
    detail_df['weighting_ielr/calculated']     = detail_df['weighting_model']
    detail_df['weighting_ielr']                = np.where(    detail_df['weighting_ielr/is_overridden']
                                                            , detail_df['weighting_ielr']
                                                            , detail_df['weighting_ielr/calculated']    )
   
    # assign selected weights including override
    detail_df['weighting_selected/calculated'] = detail_df['weighting_model']
    detail_df['weighting_selected']            = np.where(    detail_df['weighting_selected/is_overridden']
                                                            , detail_df['weighting_selected']
                                                            , detail_df['weighting_selected/calculated']    )
    return detail_df


# @time_me
def detail_add_reserving_method(detail_df):
   ############################################################################################################################################
    # load constant thresholds
    bf_threshold = constants.THRESHOLD_FOR_BF
    cl_threshold = constants.THRESHOLD_FOR_CL
    cols_method  = ['method_paid','method_incurred']
    cols_devt    = ['dev_patterns_paid','dev_patterns_incurred']

    for method, devt in zip(cols_method, cols_devt):
        # choose method based on development pattern: < 0.4 → IELR, 0.4–0.75 → BF, ≥ 0.75 → CL
        detail_df[f'{method}/calculated']   = np.where(       detail_df[  devt  ] < bf_threshold,  "IELR",
                                                  np.where(   detail_df[  devt  ] < cl_threshold,  "BF"  ,   "CL"    ))

        # use override if present, else keep calculated
        detail_df[  method  ]               = np.where(   detail_df[f'{method}/is_overridden']
                                                        , detail_df[method]
                                                        , detail_df[f'{method}/calculated']    )

    return detail_df


# @time_me
def detail_add_helpers_summary_ielr(detail_df):

    # intermediate columns used in the helpers...
    weight_cl       = np.where(detail_df['method_incurred']=="CL",          1,  0)
    weight_nil_lr   = np.where(detail_df['ultimate_cl_incurred_ulr'] > 0,   1,  0)
    mask_nominal    = detail_df['ielr_approach'] == 'Nominal'
    adj_if_onlevel  = np.where(mask_nominal,1, detail_df['loss_ratio_selected_index'])


    # helper columns for derivation of ielr's numerators
    detail_df['model_ielr_nominal_numerator'] = (  detail_df['ultimate_cl_incurred_ulr']  
                                                 * detail_df['weighting_nominal'] 
                                                 * weight_cl                             )

    detail_df['model_ielr_onlevel_numerator'] = (  detail_df['ultimate_cl_incurred_ulr']  
                                                 * detail_df['weighting_onlevel'] 
                                                 * detail_df['loss_ratio_model_index'] 
                                                 * weight_cl                             )

    detail_df['model_ielr_ol_allyr_numerator']= (  detail_df['ultimate_cl_incurred_ulr']  
                                                 * detail_df['weighting_onlevel'] 
                                                 * detail_df['loss_ratio_model_index']   )
    
    detail_df['selected_ielr_numerator']      = (  detail_df['ultimate_cl_incurred_ulr']  
                                                 * detail_df['weighting_ielr'] 
                                                 * adj_if_onlevel
                                                 * weight_cl                             )

    # helper columns for derivation of ielr's denominators
    detail_df['model_ielr_nominal_denominator'] = (  detail_df['weighting_nominal'] 
                                                   * weight_nil_lr
                                                   * weight_cl                           )

    detail_df['model_ielr_onlevel_denominator'] = (  detail_df['weighting_onlevel'] 
                                                   * weight_cl                           )

    detail_df['model_ielr_ol_allyr_denominator']= (  detail_df['weighting_onlevel']                     )
    
    detail_df['selected_ielr_denominator']      = (  detail_df['weighting_ielr'] 
                                                   * np.where(mask_nominal, weight_nil_lr, 1)
                                                   * weight_cl                                )

    return utils.safe_fillna_except(detail_df,cols_exclude_fillna())


# @time_me
def det_sum_add_ielr(detail_df,summary_df):

    # specify the columns we want from detail_df
    cols_grp   = [  'lob_number'
                  , 'ielr_approach'
                  , 'projection_data'
                  , 'ielr_source'
                  , 'selected_ielr/is_overridden'
                  , 'selected_ielr'                  ]
    
    cols_agg   = [  'model_ielr_nominal_numerator'
                  , 'model_ielr_onlevel_numerator'
                  , 'model_ielr_ol_allyr_numerator'
                  , 'selected_ielr_numerator'
                  , 'model_ielr_nominal_denominator'
                  , 'model_ielr_onlevel_denominator'
                  , 'model_ielr_ol_allyr_denominator'
                  , 'selected_ielr_denominator'                  ]

    cols_all   = cols_grp + cols_agg

    # group by lob_number and sum the calculated numerators and denominators
    detail_grp_df = detail_df[  cols_all  ].groupby(  cols_grp  ).sum().reset_index().fillna(0)

    # determine ielrs
    cols_ielr = [  'model_ielr_nominal',   'model_ielr_onlevel', 'model_ielr_ol_allyr',  'selected_ielr' ]

    for col in cols_ielr:
        sfx = '/calculated' if col == 'selected_ielr' else ''
        detail_grp_df[f'{col}{sfx}']= utils.ratio(    detail_grp_df[f'{col}_numerator']
                                                   ,  detail_grp_df[f'{col}_denominator'])

    detail_grp_df['model_ielr']     = np.where(   detail_grp_df['ielr_approach'] == 'Nominal'
                                                , detail_grp_df['model_ielr_nominal']  
                                                , detail_grp_df['model_ielr_onlevel']  )

    detail_grp_df['selected_ielr']  = np.where(   detail_grp_df['selected_ielr/is_overridden']
                                                , detail_grp_df['selected_ielr']
                                                , detail_grp_df['selected_ielr/calculated']    )
    
    # add lloyds selected ielr to beazley
    mask_lloyds     = detail_grp_df['projection_data'] == 'lloyds'
    mask_beazley    = detail_grp_df['projection_data'] == 'beazley'
    
    detail_grp_df['temp_lob_number_ielr'] = detail_grp_df['lob_number'] + np.where(mask_lloyds, 100, 0)     #this reflects the lob_number we want to map the ielr to
    map_lloyds      = detail_grp_df.loc[mask_lloyds].set_index('temp_lob_number_ielr')['selected_ielr'].to_dict()
    
    detail_grp_df.loc[mask_beazley, 'lloyds_ielr'] = detail_grp_df.loc[mask_beazley, 'temp_lob_number_ielr'].map(map_lloyds)

    # assigning lloyds loss ratio to beazley analysis ielr when selected
    mask_ielr_lloyds =   detail_grp_df['ielr_source'] == 'Lloyds Data'
    col_dest = 'selected_ielr/calculated'
    col_srce = 'lloyds_ielr'
    detail_grp_df.loc[mask_beazley & mask_ielr_lloyds, col_dest] = detail_grp_df.loc[mask_beazley & mask_ielr_lloyds, col_srce] 

    # rerunning map to selected ielr having contemplated assigning lloyds loss ratio to beazley analysis ielr when selected
    detail_grp_df['selected_ielr']  = np.where(   detail_grp_df['selected_ielr/is_overridden']
                                                , detail_grp_df['selected_ielr']
                                                , detail_grp_df['selected_ielr/calculated']    )

    # add ielrs to summary_df
    cols_out = cols_ielr + ['selected_ielr/calculated'] + ['lloyds_ielr'] + ['model_ielr', 'lob_number'] 
    summary_df = utils.drop_and_merge(summary_df, detail_grp_df[cols_out],  on = ["lob_number"])
    detail_df  = utils.drop_and_merge(detail_df,  detail_grp_df[cols_out],  on = ["lob_number"])
    
    return detail_df, summary_df


# @time_me
def detail_add_ielr_ultimate_losses(detail_df):

    # intermediate helpers - assess mask for whether nominal ielr & associated on-levelling adjustment
    mask_nominal        = detail_df['ielr_approach'] == 'Nominal'
    adj_onlevel_model   = np.where(mask_nominal,  1,  detail_df['loss_ratio_model_index'   ])
    adj_onlevel_selected= np.where(mask_nominal,  1,  detail_df['loss_ratio_selected_index'])
    
    # assign ielr applying onlevelling where appropraite to put back in that times money (aka nominal)
    detail_df['ultimate_ielr_model_ulr']    = utils.ratio(   detail_df['model_ielr'],     adj_onlevel_model   )
    detail_df['ultimate_ielr_selected_ulr'] = utils.ratio(   detail_df['selected_ielr'],  adj_onlevel_selected)
    
    # determine model and selected ultimate
    detail_df['ultimate_ielr_model'   ]     = detail_df['ultimate_gnpi'] * detail_df['ultimate_ielr_model_ulr']
    detail_df['ultimate_ielr_selected']     = detail_df['ultimate_gnpi'] * detail_df['ultimate_ielr_selected_ulr']
   
    return detail_df


# @time_me
def detail_add_bf_ultimate_losses(detail_df):

    # intermediate helpers - get paid & incurred development
    dev_paid = detail_df['dev_patterns_paid'] 
    dev_inc  = detail_df['dev_patterns_incurred'] 

    # bf on model default
    detail_df['ultimate_bf_model_paid']    = (   detail_df['ultimate_cl_paid'   ] *      dev_paid  
                                               + detail_df['ultimate_ielr_model'] * (1 - dev_paid) )
    detail_df['ultimate_bf_model_incurred']= (   detail_df['ultimate_cl_incurred'] *      dev_inc  
                                               + detail_df['ultimate_ielr_model']  * (1 - dev_inc) )   
    
    # bf on model selected    
    detail_df['ultimate_bf_selected_paid']    = (   detail_df['ultimate_cl_paid'   ]     *      dev_paid  
                                                  + detail_df['ultimate_ielr_selected']  * (1 - dev_paid))
    detail_df['ultimate_bf_selected_incurred']= (   detail_df['ultimate_cl_incurred']    *      dev_inc  
                                                  + detail_df['ultimate_ielr_selected']  * (1 - dev_inc) ) 
       
    return detail_df


# @time_me
def detail_add_blend_ultimate_losses(detail_df):

    # determine masks for when which method applies
    mask_incurred_cl =  (detail_df['method_incurred'] == "CL") & (detail_df['projection_type'] == "Incurred")
    mask_incurred_bf =  (detail_df['method_incurred'] == "BF") & (detail_df['projection_type'] == "Incurred")
    mask_paid_cl     =  (detail_df['method_incurred'] == "CL") & (detail_df['projection_type'] == "Paid")
    mask_paid_bf     =  (detail_df['method_incurred'] == "BF") & (detail_df['projection_type'] == "Paid")
    mask_ielr        = ~(mask_incurred_cl | mask_incurred_bf | mask_paid_cl | mask_paid_bf )


    # determine the ultimate for model default in each permutation
    detail_df.loc[mask_incurred_cl, 'ultimate_model' ] = detail_df['ultimate_cl_incurred']
    detail_df.loc[mask_incurred_bf, 'ultimate_model' ] = detail_df['ultimate_bf_model_incurred']
    detail_df.loc[mask_paid_cl,     'ultimate_model' ] = detail_df['ultimate_cl_paid']
    detail_df.loc[mask_paid_bf,     'ultimate_model' ] = detail_df['ultimate_bf_model_paid']
    detail_df.loc[mask_ielr,        'ultimate_model' ] = detail_df['ultimate_ielr_model']


    # determine the ultimate for selected in each permutation
    detail_df.loc[mask_incurred_cl, 'ultimate_selected' ] = detail_df['ultimate_cl_incurred']
    detail_df.loc[mask_incurred_bf, 'ultimate_selected' ] = detail_df['ultimate_bf_selected_incurred']
    detail_df.loc[mask_paid_cl,     'ultimate_selected' ] = detail_df['ultimate_cl_paid']
    detail_df.loc[mask_paid_bf,     'ultimate_selected' ] = detail_df['ultimate_bf_selected_paid']
    detail_df.loc[mask_ielr,        'ultimate_selected' ] = detail_df['ultimate_ielr_selected']
       

    # determine the associated loss ratios
    detail_df['ultimate_model_ulr']    = utils.ratio( detail_df['ultimate_model'],      detail_df['ultimate_gnpi'] )
    detail_df['ultimate_selected_ulr'] = utils.ratio( detail_df['ultimate_selected'],   detail_df['ultimate_gnpi'] )

    return detail_df


# @time_me
def detail_add_onlevel_ulr(detail_df):

    # determine the on-level loss ratios
    detail_df['on_levelled_model_ulr']    = detail_df['ultimate_model_ulr']    *  detail_df['loss_ratio_model_index'] 
    detail_df['on_levelled_selected_ulr'] = detail_df['ultimate_selected_ulr'] *  detail_df['loss_ratio_selected_index']

    return detail_df

# @time_me
def detail_add_total_helpers(detail_df):
    # calculating onlevel ulr total - calc DOES NOT vary with ielr approach
    detail_df['on_levelled_model_ulr_numerator']       = detail_df['ultimate_gnpi_ol_model'] * detail_df['on_levelled_model_ulr'] 
    detail_df['on_levelled_model_ulr_denominator']     = detail_df['ultimate_gnpi_ol_model']

    detail_df['on_levelled_selected_ulr_numerator']    = detail_df['ultimate_gnpi_ol_selected'] * detail_df['on_levelled_selected_ulr'] 
    detail_df['on_levelled_selected_ulr_denominator']  = detail_df['ultimate_gnpi_ol_selected']

    # calculating onlevel ulr total - calc DOES vary with ielr approach
    # this is the onlevel approach, nominal approach is this with an adjustment
    detail_df['model_gn_ulr_numerator']         = detail_df['weighting_model'] * detail_df['on_levelled_model_ulr'] 
    detail_df['model_gn_ulr_denominator']       = detail_df['weighting_model']

    detail_df['selected_gn_ulr_numerator']      = detail_df['weighting_selected'] * detail_df['on_levelled_selected_ulr'] 
    detail_df['selected_gn_ulr_denominator']    = detail_df['weighting_selected']

    detail_df['model_base_aqn_numerator']       = detail_df['weighting_model'] * detail_df['acquisition_ratio'] 
    detail_df['model_base_aqn_denominator']     = detail_df['weighting_model']

    detail_df['selected_base_aqn_numerator']    = detail_df['weighting_selected'] * detail_df['acquisition_ratio'] 
    detail_df['selected_base_aqn_denominator']  = detail_df['weighting_selected']

    # calculating onlevel ulr total - calc DOES vary with ielr approach 
    # this is the nominal approach, which is done by adjusting the onlevel approach
    mask_nominal        = detail_df['ielr_approach'] == 'Nominal'
    cols_adj_ult_gnpi   = [  'model_gn_ulr_numerator',      'model_gn_ulr_denominator'
                            ,'selected_gn_ulr_numerator',   'selected_gn_ulr_denominator']
    cols_adj_lat_gnpi   = [  'model_base_aqn_numerator',    'model_base_aqn_denominator'
                            ,'selected_base_aqn_numerator', 'selected_base_aqn_denominator']
    detail_df.loc[mask_nominal, cols_adj_ult_gnpi] *= detail_df.loc[mask_nominal,'ultimate_gnpi'].values[:, None]
    detail_df.loc[mask_nominal, cols_adj_lat_gnpi] *= detail_df.loc[mask_nominal,'latest_gnpi'].values[:, None]

    return detail_df



# @time_me
def detail_add_visible_rows(detail_df, lloyds_show_all_yrs, bzly_show_all_yrs ):
    for show_all_yrs, proj_data in    zip(  [lloyds_show_all_yrs, bzly_show_all_yrs],  ['lloyds','beazley']  ):
        if not show_all_yrs and not detail_df.empty:
            mask_proj_data          = (detail_df['projection_data']      == proj_data ) 
            mask_empty_incurred_yr  = (detail_df['latest_incurred']      ==0 )
            mask_empty_paid_yr      = (detail_df['latest_paid']          ==0 )
            mask_empty_premium_yr   = (detail_df['latest_gnpi']          ==0 )
            mask_not_latest_2_yr    = (detail_df['yoa']                  < max(detail_df['yoa']) - 1 ) # ie if 26 incept make sure 25 & 24 are always visible - PB req 4-feb-26
            mask_empty_yr           =( mask_empty_incurred_yr & mask_empty_paid_yr & mask_empty_premium_yr & mask_proj_data & mask_not_latest_2_yr)
            detail_df.loc[mask_empty_yr, ['lob_visible_1', 'lob_visible_2', 'lob_visible_3', "lob_visible_4",   "lob_visible_5"]] = False
    return detail_df



# @time_me
def summary_grp_details(summary_df, detail_df):
    # Although all aggregations are currently sums, .agg() with a dictionary is used to allow future flexibility (e.g., max, mean).
    # initialising the dictionary of values to aggregate with operation to apply
    agg_dict = {    'latest_gpi':                          'sum'
                  , 'latest_gnpi':                         'sum'
                  , 'latest_paid':                         'sum'
                  , 'latest_incurred':                     'sum'
                  , 'ultimate_gnpi':                       'sum'
                  , 'ultimate_gnpi_ol_model':              'sum'
                  , 'ultimate_gnpi_ol_selected':           'sum'
                  , 'ultimate_cl_paid':                    'sum'
                  , 'ultimate_cl_incurred':                'sum'
                  , 'ultimate_ielr_model':                 'sum'
                  , 'ultimate_ielr_selected':              'sum'
                  , 'ultimate_bf_selected_paid':           'sum'
                  , 'ultimate_bf_selected_incurred':       'sum'
                  , 'ultimate_bf_model_paid':              'sum'
                  , 'ultimate_bf_model_incurred':          'sum'
                  , 'ultimate_model':                      'sum'
                  , 'ultimate_selected':                   'sum'
                  
                  , 'on_levelled_model_ulr_numerator':     'sum'
                  , 'on_levelled_model_ulr_denominator':   'sum'
                  , 'on_levelled_selected_ulr_numerator':  'sum'
                  , 'on_levelled_selected_ulr_denominator':'sum'
                  , 'model_gn_ulr_numerator':              'sum'
                  , 'model_gn_ulr_denominator':            'sum'
                  , 'selected_gn_ulr_numerator':           'sum'
                  , 'selected_gn_ulr_denominator':         'sum'
                  , 'model_base_aqn_numerator':            'sum'
                  , 'model_base_aqn_denominator':          'sum'
                  , 'selected_base_aqn_numerator':         'sum'
                  , 'selected_base_aqn_denominator':       'sum'       }

    # summarising data by lob_number and joining to summary_df
    detail_grouped_df = detail_df.groupby("lob_number").agg(   agg_dict  )
    summary_df = utils.drop_and_merge(summary_df, detail_grouped_df, on="lob_number").fillna(0)

    # complex columns for which we calculated a numerator and denominator
    cols_complex = [  'on_levelled_model_ulr', 'on_levelled_selected_ulr', 'model_gn_ulr'
                    , 'model_base_aqn'       , 'selected_gn_ulr'         , 'selected_base_aqn']
    for col in cols_complex:
        summary_df[col] = utils.ratio( summary_df[f'{col}_numerator'],    summary_df[f'{col}_denominator'])

    # simple columns 
    summary_df['acquisition_ratio']          = 1 - utils.ratio(summary_df['latest_gnpi'],           summary_df['latest_gpi'])
    summary_df['incurred_loss_ratio']        =     utils.ratio(summary_df['latest_incurred'],       summary_df['latest_gnpi'])
    summary_df['ultimate_cl_paid_ulr']       =     utils.ratio(summary_df['ultimate_cl_paid'],      summary_df['ultimate_gnpi'])
    summary_df['ultimate_cl_incurred_ulr']   =     utils.ratio(summary_df['ultimate_cl_incurred'],  summary_df['ultimate_gnpi'])
    summary_df['ultimate_ielr_model_ulr']    =     utils.ratio(summary_df['ultimate_ielr_model'],   summary_df['ultimate_gnpi'])
    summary_df['ultimate_ielr_selected_ulr'] =     utils.ratio(summary_df['ultimate_ielr_selected'],summary_df['ultimate_gnpi'])
    summary_df['ultimate_model_ulr']         =     utils.ratio(summary_df['ultimate_model'],        summary_df['ultimate_gnpi'])
    summary_df['ultimate_selected_ulr']      =     utils.ratio(summary_df['ultimate_selected'],     summary_df['ultimate_gnpi'])

    return summary_df



# @time_me
def summary_add_final_lr_calcs(summary_df):
    # calculate loss ratios after adjusting for acquisition
    summary_df['model_adj_gn_ulr']      = summary_df['model_gn_ulr'] * utils.ratio(      1 - summary_df['model_base_aqn']
                                                                                        ,1 - summary_df['model_acc_aqn' ] )
    summary_df['selected_adj_gn_ulr']   = summary_df['selected_gn_ulr'] * utils.ratio(   1 - summary_df['selected_base_aqn']
                                                                                        ,1 - summary_df['selected_acc_aqn' ] )

    # calculate loss ratios after adding any cat load for acquisition
    summary_df['model_final_gn_ulr']    = summary_df['model_adj_gn_ulr']    + summary_df['bp_cat_load']
    summary_df['selected_final_gn_ulr'] = summary_df['selected_adj_gn_ulr'] + summary_df['bp_cat_load']

    # store the index as a 'row' to use in the hx.With statement in view
    mask_beazley                = (summary_df['projection_data'] == 'beazley') 
    summary_df['row']           = summary_df['lob_number'] - np.where(mask_beazley,101,1)
  
    return summary_df


# @time_me
def save_unique_lobs_to_hxd(summary_df, lloyds_path, bzly_path):
    mask_beazley                = (summary_df['projection_data'] == 'beazley') 
    mask_lloyds                 = (mask_beazley == False)
    bzly_path.drop_down_lobs    = summary_df.loc[mask_beazley, ['lookup_lob']].to_dict(orient="records")
    lloyds_path.drop_down_lobs  = summary_df.loc[mask_lloyds,  ['lookup_lob']].to_dict(orient="records")
    return 


# @time_me
def save_selected_lob_to_hxd(detail_df, summary_df, lloyds_path, bzly_path):

    # columns needed in summary - not override (also implicitly none of these are inputs)
    core_std_lst =  [   'yoa',
                        'row',

                        'lob_number',
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
                        ]
    
    cols_chart_detail = ['yoa',  'incurred_loss_ratio', 'ultimate_selected_ulr',       'on_levelled_selected_ulr'   ]

    # build final lists of columns
    summary_totals_lst  = (   core_std_lst  )
 
    
    # write data to hxd
    paths           = [lloyds_path,bzly_path]
    values_for_mask = ['lloyds','beazley']

    for path, value in zip(paths,values_for_mask):

        mask_proj_sum_data  = (  summary_df['projection_data'] == value  )
        mask_proj_det_data  = (  detail_df['projection_data'] == value  )

        summary_proj_data_df= summary_df[  mask_proj_sum_data   ]
        detail_proj_data_df = detail_df[   mask_proj_det_data   ]

        for x in range(1,6):
            sum_lob_df = summary_proj_data_df.loc[    summary_proj_data_df[f'lob_visible_{x}']   ]
            
            # if there is a selected lob and it is found in the summary table write the necessary values to the hxd
            if sum_lob_df.shape[0] == 1:

                # write summary data to hxd
                sum_row = sum_lob_df.iloc[0] 
                lob_path = getattr(path, f'selected_lob_totals_{x}' )
                for node in summary_totals_lst:
                    setattr(   lob_path,   node,   sum_row[node]  )

                # write chart data to hxd
                det_lob_df                  = detail_proj_data_df.loc[   detail_proj_data_df[f'lob_visible_{x}'],    cols_chart_detail]     # isolate just the rows & columns we want 
                det_lob_df['pricing_basis'] = sum_row['selected_final_gn_ulr']
                setattr(   lob_path,   "chart_data",   det_lob_df.to_dict(orient="records")   )

    return


# @time_me
def set_is_tab_shown(hxd):
    # Show Lloyd’s projections tab if priced by Actuarial and not following main syndicate
    not_follow_main_syndicate = hxd.non_cds.risk_information.not_follow_main_syndicate
    priced_by = hxd.cds.risk_information.priced_by

    if priced_by == "Actuarial" and not_follow_main_syndicate:
        hxd.non_cds.lloyds_projections.is_shown = True