import hx
import pandas    as pd
import numpy     as np
import math      as math
import algorithms.rate_utilities as utils
from algorithms.rate_constants  import (NCB_FREQUENCY, ADVERSE_WEATHER_NMP, IHS_EXP_BASE, CAT_NON_APP_LOAD, 
                                        EVENTS_MIN_UW_ADJ, EVENTS_MAX_UW_ADJ, WEIGHT_TO_SIMS, benchmark_lr,
                                        NM_MIN_ADJ, NM_MAX_ADJ, EVENT_DEFAULT_LENGTH)
# from algorithms                 import parameter_tables_schema as lib_params
# from operator                   import itemgetter
# from datetime                   import date, timedelta
from libraries.model_profiler.algorithms.profiling_hxd_functions import time_me





# taken from cpr model
def exposure_curve_series(b, g, x_series):
    x_series    =   x_series.astype(float)                        
    if g == 1:                                      result = x_series
    elif b == 1 and g > 1:                          result = np.log(1 + (g - 1) * x_series) / math.log(g)
    elif b * g == 1 and g > 1:                      result = (1 - b ** x_series) / (1 - b)
    elif b > 0 and b != 1 and b * g != 1 and g > 1: result = np.log(((g - 1) * b + (1 - g * b) * (b ** x_series)) / (1 - b)) / math.log(g * b)
    else:                                           result = -1 #error
    return result


def get_pat_rate(events_df, df, enabled, rate_col, pat_col):
    if not enabled:
        events_df[rate_col] = 0
        events_df[pat_col]  = ''
        return events_df

    df['country'] = df['country'].fillna('')
    df['state']   = df['state'].fillna('')
    cols_on       = ['country', 'state']
    df            = df.rename(columns={'rate': rate_col, 'pattern': pat_col})

    events_df           = utils.drop_and_merge(events_df, df, on=list(cols_on))
    events_df[rate_col] = events_df[rate_col].fillna(0)
    events_df[pat_col]  = events_df[pat_col].fillna('')

    return events_df



def get_seasonality_mth(main_df, ref_df, value_col, lhs_pattern_col, lhs_month_col, rhs_pattern_col='pattern', rhs_month_col='month'):
    return (main_df.merge( ref_df[ [rhs_pattern_col, rhs_month_col, value_col]],
                           left_on=[lhs_pattern_col, lhs_month_col],
                           right_on=[rhs_pattern_col, rhs_month_col],
                           how='left',
                           suffixes=('', '_rhs'))                                                           # these 2 lines eliminate duplicate join keys, but technically not needed as get_seasonality only return the final calculated column
                    .drop(columns=[f'{rhs_pattern_col}_rhs', f'{rhs_month_col}_rhs'], errors='ignore'))     # these 2 lines eliminate duplicate join keys, but technically not needed as get_seasonality only return the final calculated column


def get_seasonality(main_df, ref_df, main_pattern_col):
    ref_df                 = ref_df.sort_values(['pattern', 'month'])
    ref_df['rate_cumul']   = ref_df.groupby('pattern')['rate'].cumsum()
    ref_df['rate_start']   = ref_df['rate_cumul'] -  ref_df['rate']               # since we want to include the opening amount
    ref_df['rate_end']     = ref_df['rate_cumul']
    ref_df['rate_mth_12']  = ref_df['rate_cumul']

    main_df = get_seasonality_mth(main_df, ref_df, 'rate_start',  main_pattern_col, 'mth_start')
    main_df = get_seasonality_mth(main_df, ref_df, 'rate_end',    main_pattern_col, 'mth_end')
    main_df = get_seasonality_mth(main_df, ref_df, 'rate_mth_12', main_pattern_col, 'mth_12')

    test                         = main_df['mth_end'] < main_df['mth_start']  
    main_df['season_mths']       = main_df['mth_end' ] - main_df['mth_start' ] + 1 + np.where(test, main_df['mth_12'],      0) # notice the +1 to handle the starting month
    main_df['season_rate_sum']   = main_df['rate_end'] - main_df['rate_start']     + np.where(test, main_df['rate_mth_12'], 0)

    return utils.ratio(main_df['season_rate_sum'], main_df['season_mths'] )



def get_ihs_m_c(main_df, ref_df, coverage, ihs_col):

    left_df   = main_df[[ihs_col]].fillna(0).astype("float64").reset_index()
    left_df   = left_df.rename(columns={'index': 'old_index'}).sort_values(ihs_col)

    right_df  = ref_df[ ref_df['coverage'] == coverage ]
    right_df  = right_df[['ihs_score', 'm', 'c']].sort_values(['ihs_score'])
    
    joined_df = pd.merge_asof(left_df, right_df, left_on=ihs_col, right_on='ihs_score', direction='backward')
    joined_df = joined_df.sort_values('old_index').set_index('old_index').reindex(main_df.index)

    return joined_df['m'].fillna(0), joined_df['c'].fillna(0)


def get_ncb_factor(hxd, ncb_frequency):
    path        = hxd.cds.exposure.granular.event_cancel
    ncb_offered = path.ncb_offered
    enabled     = path.ncb
    if (enabled is False) or (ncb_offered is None):
        return 1
    return utils.ratio(1, (  (1 - ncb_frequency)    +    (ncb_frequency * (1 - ncb_offered))))


def get_experience_factor(hxd, df):
    path        = hxd.cds.exposure.granular.event_cancel
    exper_ilr   = path.experience_ratio                 # string banding
    enabled     = path.experience
    row         = df[df['loss_ratio'] == exper_ilr]['multiplier']
    if (enabled is False) or row.empty:
        return 1
    return row.iat[0]


def get_event_rates(hxd, df):
    path        = hxd.cds.exposure.granular.event_cancel
    event_type  = path.event_type
    row         = df[df['event_type'] == event_type]
    if row.empty:
        return 0, 0
    return (  row['base_rate'].iat[0],    row['adverse_weather_relativity'].iat[0]    )


def get_cyber_factor(hxd, df):
    path    = hxd.cds.exposure.granular.event_cancel.base_coverages
    trigger = path.cyber.trigger    
    enabled = path.cyber.covered                            
    row     = df[df['option'] == trigger]['factor']
    if (enabled is False) or row.empty:
        return 0
    return row.iat[0]


def get_national_mourning_rate(hxd, df):
    path       = hxd.cds.exposure.granular.event_cancel.base_coverages
    trigger    = path.national_mourning.trigger  
    enabled    = path.national_mourning.covered                                    
    row        = df[df['trigger'] == trigger]['rate']
    if (enabled is False) or row.empty:
        return 0
    return row.iat[0]


def get_terrorism_city_load(hxd, df):
    path       = hxd.cds.exposure.granular.event_cancel
    city_load  = path.terrorism_terms.city_load  
    enabled    = path.base_coverages.terrorism.covered                                    
    row        = df[df['city_load'] == city_load]['multiplier']
    if (enabled is False) or row.empty:
        return 1
    return row.iat[0]


def get_terrorism_event_profile(hxd, df):
    path          = hxd.cds.exposure.granular.event_cancel
    event_profile = path.terrorism_terms.event_profile  
    enabled       = path.base_coverages.terrorism.covered                                    
    row           = df[df['event_profile'] == event_profile]['multiplier']
    if (enabled is False) or row.empty:
        return 1
    return row.iat[0]


def get_terrorism_time_distance(hxd, df):
    path          = hxd.cds.exposure.granular.event_cancel
    time_distance = path.terrorism_terms.time_distance  
    enabled       = path.base_coverages.terrorism.covered                                    
    row           = df[df['time_distance'] == time_distance]['multiplier']
    if (enabled is False) or row.empty:
        return 1
    return row.iat[0]


def get_exposure_curve_b_g(curve, df):
    row         = df[df['curve'] == curve]
    if row.empty:
        return 0, 0
    return (  row['b'].iat[0],    row['g'].iat[0]    )




@time_me
def get_nm_u75_probs(df, age_group, gender, mod_affluence, mod_health, include):
    mask   = (df['age_group'] == age_group) & (df['gender'] == gender)
    row    = df[mask]
    age    = row['age_assumed'].iat[0]
    qx     = row['qx_assumed'].iat[0]
    qx_mod = max(0.0,  min(1.0, qx * mod_affluence * mod_health))
    sx     = 1.0 - (qx     if include else 0.0)
    sx_mod = 1.0 - (qx_mod if include else 0.0)
    return age, sx, sx_mod


@time_me
def get_nm_probs(df, date_incept, date_of_birth, mod_affluence, mod_health, include, gender=None, col=None ):

    is_v= isinstance(date_of_birth, (pd.Series, pd.Index, np.ndarray, list, tuple))                         # np.is_scalar fails on dates hence used this
    dob = pd.Series(pd.to_datetime(date_of_birth))              if is_v else pd.Timestamp(date_of_birth)
    doi = pd.Series(pd.Timestamp(date_incept), index=dob.index) if is_v else pd.Timestamp(date_incept)
    age = utils.yearfrac_basis0(dob, doi)                                                                   

    # ensure index aligned series if that was the input otherwise scalar
    if isinstance(age, pd.Series):
        qx_m = np.interp(age, df["age"].to_numpy(), df['qx_male'   ].to_numpy())
        qx_f = np.interp(age, df["age"].to_numpy(), df['qx_female' ].to_numpy())
        qx_u = np.interp(age, df["age"].to_numpy(), df['qx_unknown'].to_numpy())
        qx   = np.where(gender == "Male", qx_m,     np.where(gender == "Female", qx_f, qx_u))
        qx   = pd.Series(qx, index=age.index).clip(0.0, 1.0)
    else:
        qx = np.interp(age, df["age"].to_numpy(), df[col].to_numpy())                                       # notice the scalar solution uses col and not gender
        qx = np.clip(qx, 0.0, 1.0)

    qx_mod  = np.clip(qx * mod_affluence * mod_health, 0.0, 1.0)
    sx      = np.where(include, 1.0 - qx, 1.0)
    sx_mod  = np.where(include, 1.0 - qx_mod, 1.0)

    if isinstance(age, pd.Series):
        sx     = pd.Series(sx, index=age.index)
        sx_mod = pd.Series(sx_mod, index=age.index)

    return age, sx, sx_mod



def set_nm_u75_group_probs(nm_obj, country, age, sx, sx_mod):
    model = nm_obj.include
    nm_obj.country       = country    if model else ''
    nm_obj.age           = age        if model else 0
    nm_obj.prob_die      = 1 - sx     if model else 0
    nm_obj.prob_live     = sx         if model else 1
    nm_obj.prob_die_mod  = 1 - sx_mod if model else 0
    nm_obj.prob_live_mod = sx_mod     if model else 1


def set_nm_bespoke_probs(nm_obj, age, sx, sx_mod):
    model = nm_obj.include
    nm_obj.age           = age        if model else 0
    nm_obj.prob_die      = 1 - sx     if model else 0
    nm_obj.prob_live     = sx         if model else 1
    nm_obj.prob_die_mod  = 1 - sx_mod if model else 0
    nm_obj.prob_live_mod = sx_mod     if model else 1




@time_me
def set_nm_event_base_rate(df, date_incept, date_expiry, cover_level, mourning_period, use_mods):

    # establishing a suffix to identify if the UW modifiers are in play and working out which qx column to use
    sfx             = "_mod"            if use_mods else ""
    col_qx          = "nm_qx_daily_mod" if use_mods else "nm_qx_daily"
    mourning_period = mourning_period or 0

    # this exhibit explains the concept of when pay W:\Finance\Actuarial\Pricing\01 - Property\JB\Contingency\National Mourning Payouts - Visual.xlsx
    date_start_ss       = pd.to_datetime(df['date_start'],      errors="coerce").clip(lower=date_incept)        
    date_end_ss         = pd.to_datetime(df['date_end_filled'], errors="coerce").clip(lower=date_incept)        
    qx_ss               = df[col_qx]

    # death rate calc - (summing diagonal in exhibit)
    days_start_incept_ss= (date_start_ss - date_incept).dt.days.clip(lower=0)                                   # period (a): days from incept to event start
    days_end_incept_ss  = (date_end_ss   - date_incept).dt.days.clip(lower=0)                                   # period (b): days from incept to event end
    days_end_start_ss   = (days_end_incept_ss - days_start_incept_ss + 1).clip(lower=0)                         # period (c): days from event start to end (b-a) allowing for any interaction with policy incept/expiry

    prob_live_start_ss          = (1- qx_ss ) ** days_start_incept_ss                                           # probability alive at start of event
    df[f'nm_death_rate{sfx}']   = (prob_live_start_ss * ( 1 - ((1 - qx_ss) ** days_end_start_ss))).fillna(0)    # probability die during period (c) contemplating survive to start

    # funeral rate calc                                                                                         # ASSUMES funeral happens on last day of national mourning - WHICH BEGINS THE DAY AFTER DEATH
    days_start_incept_ss  = ((date_start_ss - date_incept).dt.days - mourning_period).clip(lower=0)             # period (a): days from incept + nm days    to event start
    days_end_incept_ss    = ((date_end_ss   - date_incept).dt.days - mourning_period).clip(lower=0)             # period (b): days from incept + nm days    to event end
    days_end_start_ss     = (days_end_incept_ss - days_start_incept_ss + 1).clip(lower=0)                       # period (c): days from event start to end (b-a+1) allowing for any interaction with policy incept/expiry

    prob_live_start_ss          = (1- qx_ss ) ** days_start_incept_ss                                           # probability alive 10 days before start of event if national mourning is 10 days
    df[f'nm_funeral_rate{sfx}'] = (prob_live_start_ss * ( 1 - ((1 - qx_ss) ** days_end_start_ss))).fillna(0)    # probability die during period (c) contemplating survive to start

    # mourning rate calc - (think of this as summing the diagonal in exhibit repeatedly)
    df[f'nm_mourning_rate{sfx}']     = 0
    for mourning_day in range(mourning_period):                                                                 # ASSUMES n days NATIONAL MOURNING
        days_start_incept_ss   = ((date_start_ss - date_incept).dt.days - mourning_day).clip(lower=0)           # period (a): days from incept + nm DAY    to event start
        days_end_incept_ss     = ((date_end_ss   - date_incept).dt.days - mourning_day).clip(lower=0)           # period (b): days from incept + nm DAY    to event end
        days_end_start_ss      = (days_end_incept_ss - days_start_incept_ss + 1).clip(lower=0)                  # period (c): days from event start to end (b-a+1) allowing for any interaction with policy incept/expiry

        prob_live_start_ss              = (1- qx_ss ) ** days_start_incept_ss                                    # probability alive 10 days before start of event if national mourning is 10 days
        df[f'nm_mourning_rate{sfx}']+= (prob_live_start_ss * ( 1 - ((1 - qx_ss) ** days_end_start_ss))).fillna(0)# probability die during period (c) contemplating survive to start

    # mapping to the main rate for downstream use
    if   cover_level == "Death Day Only":       df[f'nm_rate{sfx}']  = df[f'nm_death_rate{sfx}']
    elif cover_level == "Funeral Day Only":     df[f'nm_rate{sfx}']  = df[f'nm_funeral_rate{sfx}']
    elif cover_level == "Death and Funeral Day":df[f'nm_rate{sfx}']  = df[f'nm_funeral_rate{sfx}']   + df[f'nm_death_rate{sfx}']
    elif cover_level == "Mourning Period":      df[f'nm_rate{sfx}']  = df[f'nm_mourning_rate{sfx}']
    else:                                       df[f'nm_rate{sfx}']  = 0    

    return df


def get_overall_frequency(events_df, exp_cve_attr_b, exp_cve_attr_g
                                   , exp_cve_eq_b,   exp_cve_eq_g
                                   , exp_cve_ws_b,   exp_cve_ws_g   ):

    # declaring constants
    freq                = 0
    ec_coverages_lst    = [  "all_risks",     "adverse_weather",   "earthquake",  "windstorm",  "wildfire",  "terrorism",  "cyber"
                           , "national_mourning",  "riots_and_civil_commotion",   "strike",     "war",       "catastrophic_non_app"]
    weather_lst         = [  "adverse_weather",   "windstorm",  "wildfire"]
    eq_lst              = [  "earthquake"]

    # checking ok    
    # check_ok = events_df['check'].fillna("").str.strip().str.lower().eq("ok")

    # iterating over coverages
    for c in ec_coverages_lst:
        # get exposure curve factors for coverage
        b       = exp_cve_ws_b if c in weather_lst else (exp_cve_eq_b if c in eq_lst else exp_cve_attr_b)
        g       = exp_cve_ws_g if c in weather_lst else (exp_cve_eq_g if c in eq_lst else exp_cve_attr_g)
        mean_b_g= utils.ratio(( np.log(b*g) * (1-b) ),    ( np.log(b) * (1-b*g) ))
        # rate_ss = np.where(check_ok, events_df[f'rate_{c}'], 0)
        rate_ss = events_df[f'rate_{c}']
        freq   += np.clip( utils.ratio(rate_ss, mean_b_g), 0.0, 1.0).sum()

    return freq
















@time_me
def rate_exposure_event_cancellation(hxd, rater):


    ###############################################################################################
    ### 1) Setting paths and derivign initial scalar values
    ###############################################################################################

    # paths
    ms          = hxd.model_state
    cds         = hxd.cds 
    exposure    = hxd.cds.exposure.granular
    exposure_ec = hxd.cds.exposure.granular.event_cancel
    base_cov    = hxd.cds.exposure.granular.event_cancel.base_coverages
    nm          = hxd.cds.exposure.granular.event_cancel.national_mourning
    nm_u75      = hxd.cds.exposure.granular.event_cancel.national_mourning.under_75
    nm_b1       = hxd.cds.exposure.granular.event_cancel.national_mourning.bespoke_1
    nm_b2       = hxd.cds.exposure.granular.event_cancel.national_mourning.bespoke_2
    sim_path    = hxd.cds.exposure.granular.event_cancel.simulation
    ec_lay_path = cds.layers[0].coverages.ec_total
    params      = hx.params

    # loading parameter tables
    nm_indiv_df   = rater.get('nm_indiv_df',  pd.DataFrame())
    events_df     = rater.get('ec_events_df', pd.DataFrame())                 # notice dropping "ec_" from name
    fx_df         = rater.get('fx_df',        pd.DataFrame())                 

    # simple scalar
    date_incept         = pd.to_datetime(hxd.hx_core.inception_date)
    date_expiry         = pd.to_datetime(hxd.hx_core.expiry_date)
    event_type          = exposure_ec.event_type
    ccy                 = hxd.cds.currencies.source_currency

    # getting complex scalar
    base_rate, adverse_weather_rel  = get_event_rates(            hxd, params.tbl_event_rates)               # calculating base rate and adverse weather relativity
    exper_adj                       = get_experience_factor(      hxd, params.tbl_experience_adj_lr)         # calculating experience factor
    ncb_adj                         = get_ncb_factor(             hxd, NCB_FREQUENCY)                        # calculating ncb factor
    fx_rate                         = utils.get_fx_rate(               fx_df, ccy)                           # calculating fx factor
    cyber_rate                      = get_cyber_factor(           hxd, params.tbl_event_cyber)               # calculating cyber factor
    national_mourning_rate          = get_national_mourning_rate( hxd, params.tbl_event_national_mourning  ) # calculating national mourning rate
    terrorism_city_load             = get_terrorism_city_load   ( hxd, params.tbl_event_terror_cityload    )
    terrorism_event_profile         = get_terrorism_event_profile(hxd, params.tbl_event_terror_eventprofile)
    terrorism_time_distance         = get_terrorism_time_distance(hxd, params.tbl_event_terror_timedistance)

    # getting policy structure in usd
    limit_usd           = utils.ratio(ec_lay_path.limit,                  fx_rate)
    excess_usd          = utils.ratio(ec_lay_path.excess,                 fx_rate) if ec_lay_path.excess_use == True  else 0
    deductible_usd      = utils.ratio(ec_lay_path.deductible,             fx_rate) if ec_lay_path.excess_use == False else 0
    agg_limit_usd       = utils.ratio(ec_lay_path.aggregate_limit,        fx_rate)
    agg_deductible_usd  = utils.ratio(ec_lay_path.aggregate_deductible,   fx_rate) if ec_lay_path.excess_use == False else 0


    ###############################################################################################
    ### 2) loading df and basic df calculations involving dates
    ###############################################################################################

    # calculating dates/months/date cover start ("Policy Inception Day or Event End Date - 6 months. Choose the closer date")
    events_df['date_start']        = pd.to_datetime(events_df['date_start'], errors='coerce')                                       # since fakedate
    events_df['date_end']          = pd.to_datetime(events_df['date_end'],   errors='coerce')                                       # since fakedate
    events_df['date_start_plus_10']= events_df['date_start'] + pd.Timedelta(days=EVENT_DEFAULT_LENGTH)
    events_df['date_end_filled']   = events_df['date_end'].fillna(events_df['date_start_plus_10'])
    events_df['date_end_filled']   = events_df['date_end_filled'].where(events_df['date_start']<=events_df['date_end_filled'],  events_df['date_start_plus_10'])
    events_df['date_end_less_180'] = events_df['date_end_filled'] - pd.Timedelta(days=180)                                          # 180 days prior to event end
    events_df['date_start_calc']   = events_df['date_start'].clip(upper=date_incept)                                                # earliest of incept and event start
    events_df['date_cover_start']  = events_df[  ['date_start_calc', 'date_end_less_180']  ].max(axis=1)                            # get highest of 2 prior
    events_df['date_cover_start']  = np.where( events_df['date_start'] > date_expiry, events_df['date_start'], events_df['date_cover_start'])
    events_df['date_cover_start']  = events_df['date_cover_start'].fillna(date_incept)                                              # errortrap NaTs to a default date
    events_df['mths_diff']         = utils.yearfrac_basis0(events_df['date_cover_start'],     events_df['date_end_filled'] + pd.Timedelta(days=1)) * 12
    events_df['mths_diff']         = np.ceil(events_df['mths_diff']).fillna(0).clip(upper=12).astype(int)                           # mirrors excel
    events_df['mth_start']         = events_df['date_cover_start'].dt.month.fillna(0).astype('Int64')    
    events_df['mth_end']           = events_df['date_end_filled' ].dt.month.fillna(0).astype('Int64')    
    events_df['mth_12']            = 12  

    delay_days                     = np.maximum(0,       (events_df['date_start']      -             date_incept).dt.days).fillna(0) 
    duration_days                  = np.minimum(365, 1 + (events_df['date_end_filled'] - events_df['date_start']).dt.days).fillna(0) 

    ###############################################################################################
    ### 3) Calculating TIV & Discounts and other basic columns
    ###############################################################################################

    # calculating venue factor
    event_venue_df                = params.tbl_event_venue.rename(columns={'multiplier':'venue_multiplier'})
    events_df                     = utils.drop_and_merge(events_df, event_venue_df, on='venue')
    events_df['venue_multiplier'] = events_df['venue_multiplier'].fillna(1)

    # errortrapping blanks on country and state
    events_df['country']    = events_df['country'].fillna('')                   # handling Nones
    events_df['state']      = events_df['state'].fillna('')                     # handling Nones

    # base tiv calculations:
    events_df['tiv_usd']    = utils.ratio(events_df['tiv'], fx_rate ).clip(lower=0)
    events_df['cap_tiv_usd']= (events_df['tiv_usd'] - excess_usd - deductible_usd).clip(lower=0, upper=(limit_usd - deductible_usd))

    # tiv to aggregate percents
    cap_tiv_total_usd   = events_df['cap_tiv_usd'].sum()
    cap_tiv_to_agg_pct  = utils.ratio(cap_tiv_total_usd, agg_limit_usd     , if_undefined=1)
    cap_tiv_to_ded_pct  = utils.ratio(cap_tiv_total_usd, agg_deductible_usd, if_undefined=1)

    # aggregate discounts
    if ms.use_determ_agg_calc:
        agg_discount_df = params.tbl_event_aggregate_discount
        agg_discount_pct= np.interp(  cap_tiv_to_agg_pct,   agg_discount_df['exposure_limit'],   agg_discount_df['agg_limit_discount'     ]) 
        ded_discount_pct= np.interp(  cap_tiv_to_ded_pct,   agg_discount_df['exposure_limit'],   agg_discount_df['agg_deductible_discount'])
    else:
        agg_discount_pct= 1
        ded_discount_pct= 1


    # tiv totals
    tiv         = events_df['tiv'        ].fillna(0).sum()
    tiv_usd     = events_df['tiv_usd'    ].fillna(0).sum()
    tiv_cap_usd = events_df['cap_tiv_usd'].fillna(0).sum()

    ###############################################################################################
    ### 4) Deriving IHS Parameters & associated
    ###############################################################################################

    # assigning country_code
    ihs_country_df      = params.tbl_ihs_country_codes
    ihs_country_group_df= params.tbl_ihs_country_group

    country_code_ss           = utils.drop_and_merge(events_df[["country"]], ihs_country_df, 'country')['code'].fillna("")
    country_groups_set        = set(  ihs_country_group_df["group"].unique()  )
    group_ss                  = events_df["country"].isin( country_groups_set  )
    events_df["country_code"] = np.where(group_ss, events_df["country"], country_code_ss)

    # calculate ihs check value - used to monitor for changes - THINK CAREFULLY BEFORE CHANGING THIS AS THE ORDER AND REPETITION OF VALUES IS IMPORTANT CONSIDERING WE STORE THEM DIRECTLY TO THE EVENTS TABLE
    ihs_calc_run_value        = (     "Incept: "
                                    + date_incept.strftime("%Y-%m-%d")
                                    + "; Ctry: "
                                    + ",".join(events_df["country_code"].dropna().astype(str)))

    ## add check on Events Table
    # masks
    event_name_mask = events_df['event_name'].isnull() |  (events_df['event_name']=="")
    country_name_mask = events_df['country'].isnull() |  (events_df['country']=="")
                    
    state_missing    = (events_df['state'].isnull() |  (events_df['state']==""))
    state_name_mask  = (events_df['country']=="US")    &   (state_missing == True )
    state_name_mask |= (events_df['country']!="US")    &   (state_missing == False)   &   (country_name_mask== False) 

    date_start_mask  = events_df['date_start'].isnull()                #|  (events_df['date_start']=="")
    date_end_mask    = events_df['date_end'].isnull()                  |  (events_df['date_end'] < events_df['date_start'])
    tiv_mask         = events_df['tiv'].isnull()                       |  (events_df['tiv'] < 0)
    venue_mask       = events_df['venue'].isnull() |  (events_df['venue']=="")

    date_outside_mask  = ~(date_start_mask | date_end_mask)
    date_outside_mask &=  ((date_incept > events_df['date_start']) | (date_expiry < events_df['date_end']))

    # strings
    event_name_str   = pd.Series(np.where(event_name_mask,  "Event Name; ",                  "" ), index=events_df.index)
    country_name_str = pd.Series(np.where(country_name_mask,"Country; ",                     "" ), index=events_df.index)
    state_name_str   = pd.Series(np.where(state_name_mask,  "State; ",                       "" ), index=events_df.index)
    date_start_str   = pd.Series(np.where(date_start_mask,  "Date Start; ",                  "" ), index=events_df.index)
    date_end_str     = pd.Series(np.where(date_end_mask,    "Date End; ",                    "" ), index=events_df.index)
    tiv_str          = pd.Series(np.where(tiv_mask,         "Insured Value; ",               "" ), index=events_df.index)
    venue_str        = pd.Series(np.where(venue_mask,       "Venue; ",                       "" ), index=events_df.index)
    date_outside_str = pd.Series(np.where(date_outside_mask,"Dates outside policy period; ", "" ), index=events_df.index)


    # outputs
    all_missing_mask   = (event_name_mask & country_name_mask & state_missing   & date_start_mask & date_end_mask & tiv_mask & venue_mask)
    some_missing_mask  = (event_name_mask | country_name_mask | state_name_mask | date_start_mask | date_end_mask | tiv_mask | venue_mask | date_outside_str) 
    overall_str        = (event_name_str  + country_name_str  + state_name_str  + date_start_str  + date_end_str  + tiv_str  + venue_str  + date_outside_str)
    events_df['check'] = np.where(all_missing_mask, "OK",     np.where(some_missing_mask, "❌Check: " + overall_str,   "OK"))

    # calculate ihs factors - m & c
    for cvg in ['terrorism', 'riots_and_civil_commotion', 'strike', 'war']:
        m, c = get_ihs_m_c(events_df, params.tbl_event_ihs_parameters, cvg, f'ihs_{cvg}')
        events_df[f'm_{cvg}'] = m
        events_df[f'c_{cvg}'] = c



    ###############################################################################################
    ### 5) Loading base rates and parameters
    ###############################################################################################

    # loading rates & patterns - adverse_weather, earthquake, earthquake, wildfire
    events_df = get_pat_rate(events_df, params.tbl_event_adverse_weather, base_cov.adverse_weather.covered, 'base_rate_adverse_weather', 'pat_adverse_weather')  # adverse weather
    events_df = get_pat_rate(events_df, params.tbl_event_windstorm,       base_cov.windstorm.covered,       'base_rate_windstorm',       'pat_windstorm')        # windstorm
    events_df = get_pat_rate(events_df, params.tbl_event_wildfire,        base_cov.wildfire.covered,        'base_rate_wildfire',        'pat_wildfire')         # wildfire
    events_df = get_pat_rate(events_df, params.tbl_event_earthquake,      base_cov.earthquake.covered,      'base_rate_earthquake',      'pat_earthquake')       # earthquake

    
    # calculating seasonality factors
    events_df['season_adverse_weather'] = get_seasonality(  events_df,   params.tbl_event_seasonality_adverse_weather,       'pat_adverse_weather')
    events_df['season_windstorm']       = get_seasonality(  events_df,   params.tbl_event_seasonality_windstorm,             'pat_windstorm')
    events_df['season_wildfire']        = get_seasonality(  events_df,   params.tbl_event_seasonality_wildfire,              'pat_wildfire')



    ###############################################################################################
    ### 6) loading national mourning df and doing supporting calculations
    ###############################################################################################

    
    # loading parameter tables
    age_g_df = params.tbl_event_national_mourning_mortality_by_age_group
    age_df   = params.tbl_event_national_mourning_mortality_by_age
    
    # processing values
    nm_u75_age, nm_u75_sx, nm_u75_sx_mod = get_nm_u75_probs(age_g_df, "Under 75s",  "Male", nm_u75.mod_affluence, nm_u75.mod_health, nm_u75.include)
    nm_b1_age,  nm_b1_sx,  nm_b1_sx_mod  = get_nm_probs(    age_df, date_incept
                                                          , nm_b1.date_of_birth,            nm_b1.mod_affluence
                                                          , nm_b1.mod_health,               nm_b1.include
                                                          , col="qx_bespoke_1",)
    nm_b2_age,  nm_b2_sx,  nm_b2_sx_mod  = get_nm_probs(    age_df, date_incept
                                                          , nm_b2.date_of_birth,            nm_b2.mod_affluence
                                                          , nm_b2.mod_health,               nm_b2.include
                                                          , col="qx_bespoke_2",)
    nm_o75_age, nm_o75_sx, nm_o75_sx_mod = get_nm_probs(    age_df, date_incept
                                                          , nm_indiv_df['date_of_birth'],   nm_indiv_df['mod_affluence']
                                                          , nm_indiv_df['mod_health'],      nm_indiv_df['include']
                                                          , gender=nm_indiv_df['gender']          )

    # writing to df 
    nm_indiv_df['age']           = nm_o75_age
    nm_indiv_df['nm_o75_sx']     = nm_o75_sx
    nm_indiv_df['nm_o75_sx_mod'] = nm_o75_sx_mod
    nm_indiv_df['nm_o75_qx']     = 1 - nm_o75_sx
    nm_indiv_df['nm_o75_qx_mod'] = 1 - nm_o75_sx_mod
           

    # grouping df ready to join
    nm_indiv_filt_df = nm_indiv_df[nm_indiv_df['include']]
    bespoke_rows = pd.DataFrame({   'country':        [nm_b1.country,  nm_b2.country],
                                    'nm_o75_sx':      [nm_b1_sx,       nm_b2_sx     ],
                                    'nm_o75_sx_mod':  [nm_b1_sx_mod,   nm_b2_sx_mod ]  })
    nm_indiv_grp_df = pd.concat([bespoke_rows, nm_indiv_filt_df], ignore_index=True).groupby('country')[['nm_o75_sx','nm_o75_sx_mod']].prod()

    # merging df
    events_df                  = utils.drop_and_merge(events_df, nm_indiv_grp_df, on=['country'])
    events_df['nm_o75_sx']     = events_df['nm_o75_sx'    ].fillna(1)
    events_df['nm_o75_sx_mod'] = events_df['nm_o75_sx_mod'].fillna(1)

    # appending new national mourning columms - no modifiers
    events_df['nm_o75_sx']     = events_df['nm_o75_sx'    ].fillna(1)
    events_df['nm_u75_sx']     = nm_u75_sx
    events_df['nm_sx']         =(events_df['nm_o75_sx'] * events_df['nm_u75_sx']).fillna(1)
    events_df['nm_qx']         = 1 - events_df['nm_sx'] 
    events_df['nm_qx_daily']   = 1 -(events_df['nm_sx'] ** (1/365))
    
    # appending new national mourning columms - with modifiers
    events_df['nm_o75_sx_mod']  = events_df['nm_o75_sx_mod'].fillna(1)
    events_df['nm_u75_sx_mod']  = nm_u75_sx_mod
    events_df['nm_sx_mod']      =(events_df['nm_o75_sx_mod'] * events_df['nm_u75_sx_mod']).fillna(1)
    events_df['nm_qx_mod']      = 1 - events_df['nm_sx_mod'] 
    events_df['nm_qx_daily_mod']= 1 -(events_df['nm_sx_mod'] ** (1/365))

    # appending base rates - before and after modifiers
    events_df = set_nm_event_base_rate(events_df, date_incept, date_expiry, nm.cover_level, nm.mourning_period, False)
    events_df = set_nm_event_base_rate(events_df, date_incept, date_expiry, nm.cover_level, nm.mourning_period, True )

    # setting final df column names for export
    column_names = {    'nm_o75_sx':        'prob_live',
                        'nm_o75_sx_mod':    'prob_live_mod',
                        'nm_o75_qx':        'prob_die',
                        'nm_o75_qx_mod':    'prob_die_mod'    }
    nm_indiv_df = nm_indiv_df.rename(columns=column_names)

    # add check on National Mourning table entries
    min_adj = NM_MIN_ADJ
    max_adj = NM_MAX_ADJ

    name_mask         = nm_indiv_df['name'].isnull()    |  (nm_indiv_df['name']=="")
    country_name_mask = nm_indiv_df['country'].isnull() |  (nm_indiv_df['country']=="")
    gender_mask       = nm_indiv_df['gender'].isnull()  |  (nm_indiv_df['gender']=="")
    date_of_birth_mask= nm_indiv_df['date_of_birth'].isnull()
    affluence_mask    = (nm_indiv_df['mod_affluence']< min_adj) | (nm_indiv_df['mod_affluence']> max_adj) 
    health_mask       = (nm_indiv_df['mod_health']   < min_adj) | (nm_indiv_df['mod_health']   > max_adj) 

    name_str         = pd.Series(np.where(name_mask,         "Name; ",           "" ), index=nm_indiv_df.index)
    country_name_str = pd.Series(np.where(country_name_mask, "Country; ",        "" ), index=nm_indiv_df.index)
    gender_str       = pd.Series(np.where(gender_mask,       "Gender; ",         "" ), index=nm_indiv_df.index)
    date_of_birth_str= pd.Series(np.where(date_of_birth_mask,"Date of Birth; ",  "" ), index=nm_indiv_df.index)
    affluence_str    = pd.Series(np.where(affluence_mask,   f"Affluence <{min_adj} or >{max_adj}; ",  "" ), index=nm_indiv_df.index)
    health_str       = pd.Series(np.where(health_mask,      f"Health <{min_adj} or >{max_adj}; ",     "" ), index=nm_indiv_df.index)

    overall_mask        = (name_mask | country_name_mask | gender_mask | date_of_birth_mask | affluence_mask | health_mask)
    overall_str         = (name_str  + country_name_str  + gender_str  + date_of_birth_str  + affluence_str  + health_str )
    nm_indiv_df['check']= np.where(nm_indiv_df['include'] == False, "OK",   np.where(overall_mask, "Check: " + overall_str,   "OK"))


    # add check on National Mourning scalar entries    
    for path in [nm_u75, nm_b1, nm_b2]:
        if path.include == False:
            path.check = "OK"
        else:
            path.check = "Check: "
            if (path.mod_affluence < min_adj) or (path.mod_affluence > max_adj):
                path.check += f"Affluence <{min_adj} or >{max_adj}; "
            if (path.mod_health < min_adj)    or (path.mod_health > max_adj):
                path.check += f"Health <{min_adj} or >{max_adj}; "
            if path.check == "Check: ":
                path.check = "OK"


    ###############################################################################################
    ### 7) Calculating total rate by coverage
    ###############################################################################################

    # calculating total rate by coverage
    events_df['rate_all_risks']         = base_rate

    events_df['rate_adverse_weather']   = (  (1 if base_cov.adverse_weather.covered else 0)                     # bool that determines if cover is active
                                           * (  (events_df['base_rate_adverse_weather'].fillna(0))              # notice fillna 0  
                                              * (events_df['season_adverse_weather'   ].fillna(1))
                                              * (events_df['mths_diff'                ].fillna(0)) 
                                              * (events_df['venue_multiplier'         ].fillna(1))
                                              * (adverse_weather_rel or 1)
                                              + ADVERSE_WEATHER_NMP                                 ))

    events_df['rate_windstorm']         = ( (1 if base_cov.windstorm.covered else 0)                               # bool that determines if cover is active
                                           * (  (events_df['base_rate_windstorm'      ].fillna(0))              # notice fillna 0  
                                              * (events_df['season_windstorm'         ].fillna(1))
                                              * (events_df['mths_diff'                ].fillna(0))  ))
    
    events_df['rate_wildfire']          = ( (1 if base_cov.wildfire.covered else 0)                             # bool that determines if cover is active
                                           * (  (events_df['base_rate_wildfire'       ].fillna(0))              # notice fillna 0  
                                              * (events_df['season_wildfire'          ].fillna(1))
                                              * (events_df['mths_diff'                ].fillna(0))  ))

    events_df['rate_earthquake']        = ( (1 if base_cov.earthquake.covered else 0)                             # bool that determines if cover is active
                                             * (events_df['base_rate_earthquake'     ].fillna(0))  )

    events_df['rate_cyber']             = ( (1 if base_cov.cyber.covered else 0)     *  (cyber_rate or 0))



    # conditioning on whether to use the old national mourning approach
    if hxd.model_state.use_nm_app_old_model:
        events_df['rate_national_mourning']     = ( (1 if base_cov.national_mourning.covered else 0)                       # bool that determines if cover is active
                                                    * (  (national_mourning_rate/365)
                                                    * (duration_days)
                                                    * ((1 - national_mourning_rate/365) ** delay_days)  ))
        events_df['rate_national_mourning_mod'] = events_df['rate_national_mourning']

    else:
        events_df['rate_national_mourning']     = (  (1 if base_cov.national_mourning.covered else 0)                 # bool that determines if cover is active
                                                    *(utils.ratio((events_df['nm_rate'].fillna(0))  
                                                                        , duration_days  )))                          

        events_df['rate_national_mourning_mod'] = ( (1 if base_cov.national_mourning.covered else 0)                  # bool that determines if cover is active
                                                   *(utils.ratio((events_df['nm_rate_mod'].fillna(0))  
                                                                    , duration_days  )))



    events_df['rate_terrorism']         = (  (1 if base_cov.terrorism.covered else 0)                             # bool that determines if cover is active
                                           * (terrorism_city_load    )
                                           * (terrorism_event_profile)
                                           * (terrorism_time_distance)                                         
                                           * (  (events_df['m_terrorism'].fillna(0)               )
                                              * (IHS_EXP_BASE ** events_df['ihs_terrorism'].fillna(0) )
                                              + (events_df['c_terrorism'].fillna(0)                 )).fillna(0))

    events_df['rate_riots_and_civil_commotion']= (  (1 if base_cov.riots_and_civil_commotion.covered else 0)        # bool that determines if cover is active
                                                  * (  (events_df['m_riots_and_civil_commotion'].fillna(0)              )
                                                     * (IHS_EXP_BASE ** events_df['ihs_riots_and_civil_commotion'].fillna(0))
                                                     + (events_df['c_riots_and_civil_commotion'].fillna(0)                )))
    
    events_df['rate_strike']            = (  (   (1 if base_cov.strike.covered               else 0)
                                               * (1 if event_type == "Conference/Exhibition" else 0)
                                               * (events_df['ihs_strike'] > 3.1).astype(int)        )
                                           * ( events_df['m_strike']
                                               * (IHS_EXP_BASE ** events_df['ihs_strike'])
                                               + events_df['c_strike']                              )).fillna(0)

    events_df['rate_war']               = (  (1 if base_cov.war.covered else 0)                                 # bool that determines if cover is active
                                           * (  (events_df['m_war'].fillna(0)              )
                                              * (IHS_EXP_BASE ** events_df['ihs_war'].fillna(0))
                                              + (events_df['c_war'].fillna(0)                ))).fillna(0)


    events_df['rate_catastrophic_non_app'] = (  (1 if base_cov.catastrophic_non_app.covered else 0)             # bool that determines if cover is active
                                              * (CAT_NON_APP_LOAD or 0))


    ###############################################################################################
    ### 8) Getting Exposure Curves by line of business and overlaying on TIV
    ###############################################################################################

    # getting b & g parameters for mbbefdg in various coverages
    exp_cve_attr_b, exp_cve_attr_g =   get_exposure_curve_b_g(exposure_ec.exposure_curve,   params.tbl_exposure_curve_attr)
    exp_cve_eq_b,   exp_cve_eq_g   =   get_exposure_curve_b_g('Earthquake',                 params.tbl_exposure_curve_cat )
    exp_cve_ws_b,   exp_cve_ws_g   =   get_exposure_curve_b_g('Windstorm',                  params.tbl_exposure_curve_cat )    

    # specifiying coverage list
    std_lst          = ["all_risks", "terrorism", "cyber", "national_mourning",                          #"non_appearance",
                        "riots_and_civil_commotion",   "strike",    "war",   "catastrophic_non_app"  ]
    weather_lst      = ["adverse_weather", "windstorm", "wildfire"]
    eq_lst           = ["earthquake"]
    ec_coverages_lst = std_lst + weather_lst + eq_lst                                   # in the loop follwo
    
    # specifiying starting behaviour
    sublimit                      = None
    enabled                       = True
    events_df['el_usd_total']     = 0
    events_df['net_el_usd_total'] = 0
    net_el_mod_total              = 0

    # setting exposure curve warning
    if (event_type == "Music Festival") and (exposure_ec.exposure_curve == "Standard"):
        hxd.model_state.show_exposure_curve_warning = True
        exposure_ec.exposure_curve_warning          = "Please consider using Heavy exposure curve for Music Festivals."
    else:
        hxd.model_state.show_exposure_curve_warning = False


    # looping over coverage and assigning a structure_pct for each coverage
    for cvg in ec_coverages_lst:
        # specifying the coverage path
        cvg_path = getattr(base_cov,  cvg )
        
        # specifying the columns
        sp_col      = f"struct_pct_{cvg}"
        el_col      = f"el_usd_{cvg}"
        net_el_col  = f"net_el_usd_{cvg}"
        rate_col    = f"rate_{cvg}"
        
        # specify the parameters
        b = exp_cve_attr_b if cvg in std_lst else (exp_cve_eq_b if cvg in eq_lst else exp_cve_ws_b)
        g = exp_cve_attr_g if cvg in std_lst else (exp_cve_eq_g if cvg in eq_lst else exp_cve_ws_g)

        # getting sublimit and whether enabled if NOT all risks
        if cvg != "all_risks":
            sublimit     = cvg_path.sublimit
            sublimit_usd = utils.ratio(sublimit, fx_rate)
            enabled      = cvg_path.covered
        else:
            sublimit = None
            enabled  = True
        
        # if enabled calculating the mbbefdg else nil
        if enabled:
            sel_limit_usd     = limit_usd if sublimit is None else np.minimum( sublimit_usd, limit_usd)     # notice conditioning on sublimit to retain the None state
            upper_ss          = np.minimum(1, utils.ratio((sel_limit_usd  + excess_usd ),  events_df['tiv_usd']))
            lower_ss          = np.minimum(1, utils.ratio((deductible_usd + excess_usd ),  events_df['tiv_usd']))
            events_df[sp_col] = exposure_curve_series(b, g, upper_ss) - exposure_curve_series(b, g, lower_ss)
            events_df[sp_col] = events_df[sp_col].clip(lower=0)                                             # requested by AC Sep-1
        else:
            events_df[sp_col] = 0

        # calculating the expected loss
        events_df[el_col]     = (events_df['tiv_usd']  *  events_df[sp_col]  * events_df[rate_col]             ).fillna(0)
        events_df[net_el_col] = (events_df[el_col] * exper_adj * ncb_adj  * agg_discount_pct * ded_discount_pct).fillna(0)

        if cvg == "national_mourning":
            el_col_mod                = f'{el_col}_mod'
            net_el_col_mod            = f'{el_col_mod}_mod'
            events_df[el_col_mod]     = (events_df['tiv_usd']  *  events_df[sp_col]  * events_df[rate_col + "_mod"]    ).fillna(0)  # adding uw modifiers "mod"
            events_df[net_el_col_mod] = (events_df[el_col_mod] * exper_adj * ncb_adj  * agg_discount_pct * ded_discount_pct).fillna(0)
    
        ### WORKING WITH THE HXD
        # writing uw adj to hxd
        cvg_path.uw_adj_min = EVENTS_MIN_UW_ADJ
        cvg_path.uw_adj_max = EVENTS_MAX_UW_ADJ
        cvg_path.uw_adj_fin = float(np.clip(cvg_path.uw_adj_sel or 0.0, EVENTS_MIN_UW_ADJ, EVENTS_MAX_UW_ADJ))

        # calculating uw mod factor for national mourning        
        net_el_usd      = utils.safe_sum(events_df[net_el_col    ], default=0)
        net_el_mod_usd  = utils.safe_sum(events_df[net_el_col_mod], default=0) if cvg == "national_mourning" else  net_el_usd 
        uw_mod_factor   = utils.ratio(net_el_mod_usd, net_el_usd)
       
        # writing el & bm prem to hxd
        cvg_path.net_el_usd    = net_el_usd
        cvg_path.net_el        = net_el_usd * fx_rate
        cvg_path.net_el_mod    = cvg_path.net_el * (1 + cvg_path.uw_adj_fin) * uw_mod_factor
        cvg_path.net_prem_usd  = utils.ratio(cvg_path.net_el_usd, benchmark_lr)
        cvg_path.net_prem      = utils.ratio(cvg_path.net_el,     benchmark_lr)
        cvg_path.net_prem_mod  = utils.ratio(cvg_path.net_el_mod, benchmark_lr)

        # accumulating values
        events_df['el_usd_total'    ] += events_df[    el_col]
        events_df['net_el_usd_total'] += events_df[net_el_col]
        net_el_mod_total              += cvg_path.net_el_mod

    ###############################################################################################
    ### 9) getting frequency overall
    ###############################################################################################
    freq = get_overall_frequency(events_df, exp_cve_attr_b, exp_cve_attr_g
                                          , exp_cve_eq_b,   exp_cve_eq_g
                                          , exp_cve_ws_b,   exp_cve_ws_g   )

    freq_adj = utils.ratio(   sim_path.total_sim_claim_number_override, freq, 1)

    ###############################################################################################
    ### 10) Writing factors back to hxd and the events df to the rater
    ###############################################################################################

    # writing totals to hxd
    ec_total               = base_cov.ec_total
    ec_total.net_el_usd    = utils.safe_sum(events_df['net_el_usd_total'], default=0)
    ec_total.net_el        = ec_total.net_el_usd * fx_rate
    ec_total.net_el_mod    = net_el_mod_total

    ec_total.net_prem_usd  = utils.ratio(ec_total.net_el_usd, benchmark_lr)
    ec_total.net_prem      = utils.ratio(ec_total.net_el,     benchmark_lr)
    ec_total.net_prem_mod  = utils.ratio(ec_total.net_el_mod, benchmark_lr)

    # exposure and ncb
    exposure_ec.ncb_factor                       = ncb_adj
    exposure_ec.experience_factor                = exper_adj
    exposure_ec.factors.fx_rate                  = fx_rate      
    exposure_ec.factors.cyber_rate               = cyber_rate      
    exposure_ec.factors.national_mourning_rate   = national_mourning_rate      
    exposure_ec.factors.terrorism_city_load      = terrorism_city_load      
    exposure_ec.factors.terrorism_event_profile  = terrorism_event_profile      
    exposure_ec.factors.terrorism_time_distance  = terrorism_time_distance      
    exposure_ec.factors.cap_tiv_total_usd        = cap_tiv_total_usd      
    exposure_ec.factors.cap_tiv_to_agg_pct       = cap_tiv_to_agg_pct      
    exposure_ec.factors.cap_tiv_to_ded_pct       = cap_tiv_to_ded_pct      
    exposure_ec.factors.agg_discount_pct         = agg_discount_pct   
    exposure_ec.factors.ded_discount_pct         = ded_discount_pct      
    exposure_ec.factors.exp_cve_attr_b           = exp_cve_attr_b      
    exposure_ec.factors.exp_cve_attr_g           = exp_cve_attr_g      
    exposure_ec.factors.exp_cve_eq_b             = exp_cve_eq_b      
    exposure_ec.factors.exp_cve_eq_g             = exp_cve_eq_g      
    exposure_ec.factors.exp_cve_ws_b             = exp_cve_ws_b      
    exposure_ec.factors.exp_cve_ws_g             = exp_cve_ws_g
    exposure_ec.factors.freq_adj                 = freq_adj  

    # agg tiv to hxd
    cds.exposure.aggregate.exposure = tiv # notice not fx converted
    exposure_ec.agg_tiv_calc        = tiv
    hxd.model_state.show_tiv_warning= round(exposure_ec.agg_tiv_calc - (exposure_ec.agg_tiv_uw or 0),  0) != 0
    exposure_ec.agg_tiv_warning     = "Inconsistent Aggregate TIV - please review" if hxd.model_state.show_tiv_warning else "ok"

    # national mourning scalar to hxd
    set_nm_u75_group_probs(nm_u75, "Worldwide", nm_u75_age, nm_u75_sx, nm_u75_sx_mod)
    set_nm_bespoke_probs(  nm_b1,               nm_b1_age,  nm_b1_sx,  nm_b1_sx_mod )
    set_nm_bespoke_probs(  nm_b2,               nm_b2_age,  nm_b2_sx,  nm_b2_sx_mod )

    # ihs to hxd
    ihs_path = hxd.cds.ihs
    ihs_path.calc_run_value = ihs_calc_run_value
    ihs_path.check_run_consistent = "IHS Data Remains Valid" if (ihs_calc_run_value==ihs_path.last_run_value) else "Please reload IHS Scores"

    # deriving the equivalent simulated estimates
    if sim_path.total_sim_loss_before_agg:
        sim_path.total_det_loss_after_agg_adj = ec_total.net_el * freq_adj
        sim_path.total_det_loss_after_agg     = utils.ratio(ec_total.net_el,  exper_adj * ncb_adj)
        sim_path.total_det_loss_before_agg    = utils.ratio(ec_total.net_el,  exper_adj * ncb_adj  * agg_discount_pct * ded_discount_pct)

        if sim_path.total_sim_claim_number_override is None : 
            sim_path.sim_error = utils.ratio(sim_path.total_sim_loss_before_agg, sim_path.total_det_loss_before_agg, 1) - 1
        else :
            sim_path.sim_error = 0
        
        sim_path.total_sim_loss_after_agg_adj        =                sim_path.total_sim_loss_after_agg    * exper_adj * ncb_adj
        sim_path.total_sim_loss_after_agg_adj_scaled = utils.ratio(   sim_path.total_sim_loss_after_agg_adj, sim_path.sim_error + 1)
        sim_path.sim_agg_adj                         =((utils.ratio(  sim_path.total_sim_loss_after_agg_adj_scaled
                                                                     ,sim_path.total_det_loss_after_agg_adj, 1    ) - 1)
                                                            * WEIGHT_TO_SIMS)
    else:
        sim_path.sim_agg_adj  = 0                                                                

    sim_path.total_sim_claim_number_calc = freq
    
    # passing events_df to rater
    rater["ec_events_df"]   = events_df         # notice adding "ec_" to name
    rater["nm_indiv_df"]    = nm_indiv_df
    rater["nm_indiv_grp_df"]= nm_indiv_grp_df



    return rater

