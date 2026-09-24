# v0.5.0
import hx, numpy as np, pandas as pd
from dateutil.relativedelta import relativedelta

from algorithms.rate_constants  import EXPER_RATING_LOGIC_DICT, EXPER_RATING_DECAY, EXPER_RATING_LL_THRESHOLD, EXPER_RATING_MAX_NUM_YRS, EVALUATION_DATE_LAG
from algorithms.rate_utilities  import ratio, yearfrac_basis0, drop_and_merge, get_tp_dict, look_up_with_bounds, get_fx_rate



def pick_override(ovd, calc):
    return calc if ovd is None or pd.isna(ovd) else ovd


def rate_experience_rating(hxd, rater):

    ### Preparing the data
    # paths
    cds= hxd.cds
    er = hxd.cds.experience_rating
    tt = hxd.cds.experience_rating.analysis_table_total
    tti= hxd.cds.experience_rating.analysis_table_total_included
    cy = hxd.cds.experience_rating.analysis_table_cy

    # loading df
    exper_df      = rater.get('exper_df')
    policy_df     = rater.get('policy_df')
    claim_df      = rater.get('claim_df')
    fx_df         = rater.get('fx_df')
    tp_dict       = rater.get('tp_dict')
    yoa_assump_df = hx.params.tbl_experience_yoa_assump
    yoa_assump_df = yoa_assump_df.set_index("yoa").reindex(range(yoa_assump_df["yoa"].min(), 2031)).ffill().reset_index()
    dev_df        = hx.params.tbl_experience_dev_factors.sort_values('month')
    yr_exp_wgt_df = hx.params.tbl_experience_year_exposure_weight
    lrg_cred_df   = hx.params.tbl_experience_large_year_credibility

    # simple scalar
    date_incept   = pd.to_datetime(hxd.hx_core.inception_date)
    yoa_incept    = date_incept.year
    ccy           = cds.currencies.source_currency
    cy_tiv        = cds.exposure.aggregate.exposure or 0
    cy_tiv_trend  = er.exposure_trend_backfill or 0 
    filt_pol_bool = er.use_policy_ref_filter
    fx_scc        = get_fx_rate(fx_df, ccy ) 

    # setting evaluation date
    er.evaluation_date_calc = date_incept + relativedelta(months=EVALUATION_DATE_LAG)
    er.evaluation_date      = pick_override(er.evaluation_date_ovd, er.evaluation_date_calc)
    date_claim              = pd.to_datetime(er.evaluation_date)

    # getting complex scalar/dict
    # fx_rate         = get_fx_rate( fx_df, ccy  )
    fx_usd          = get_fx_rate( fx_df, "USD")                                                                                # calculating fx factor
    mth_eval_incept = yearfrac_basis0(date_claim, date_incept)  *  12                                                           # months between claim evaluation and incept
    section_ref     = cds.layers[0].coverages.ec_total.section_reference
    section_ref6    = section_ref[:6] if section_ref else ''
    exper_rows      = exper_df.shape[0]
    # cy_tiv_usd      = ratio(cy_tiv, fx_rate)
    nmp_load        = tp_dict['nmp_load'   ]
    cy_inf          = yoa_assump_df[yoa_assump_df['yoa']==yoa_incept]['port_clm_inflation'].iat[0]

    # checking if bi needs to be rerun
    cds.bi.calc_run_value = section_ref
    cds.bi.check_run_consistent = "OK" if cds.bi.calc_run_value == cds.bi.last_run_value else "❌❌❌Please reload data❌❌❌"

    ### policy table manipulation
    # fx
    policy_df['fx_rate_to_scc']     = ratio(fx_scc,  get_fx_rate(fx_df, policy_df['settlement_fx'] ),  1) 

    # ensuring datatypes and convert to account fx (source currency code)
    for col in ['gnwp_100', 'incurred_100', 'gnwp_bzly', 'incurred_bzly']:
        policy_df[col]          = policy_df[col].astype(np.float64).fillna(0)
        policy_df[f'{col}_scc'] = policy_df[col] * policy_df['fx_rate_to_scc']

    # rate change
    policy_df['rate_chg']             = policy_df['rate_chg'].astype(np.float64)
    policy_df['gnwp_100_exp_adj_scc'] = ratio(policy_df['gnwp_100_scc'], policy_df['rate_chg'])                               # noticing we are using the adjusted rate(not raw) and the expiring adjusted

    # filtering and grouping
    cols_policy_grp = ['yoa']
    cols_policy_sum = ['gnwp_100_scc', 'incurred_100_scc', 'gnwp_100_exp_adj_scc']
    rows_policy_mask=(policy_df['policy_ref'].str[:6] == section_ref6)   if   filt_pol_bool   else True                         # implies use of broadcasting in False Test
    rows_policy_mask= rows_policy_mask &  policy_df['bool_ec']
    policy_grp_df   = policy_df.loc[  rows_policy_mask  ].groupby(  cols_policy_grp, as_index=False   )[  cols_policy_sum  ].sum()


    ### claim table manipulation
     # fx
    claim_df['fx_rate_to_scc']          = ratio(fx_scc,  get_fx_rate(fx_df, claim_df['settlement_fx'] ),  1)  # notice premium was initially translated into USD at an unknown currency, claims is using the built in library - so slight inconsistency here.

    # ensuring datatypes and convert to account fx (source currency code)
    for col in ['incurred_100', 'incurred_bzly', 'os_bzly']:
        claim_df[col]          = claim_df[col].astype(np.float64).fillna(0)
        claim_df[f'{col}_scc'] = claim_df[col] * claim_df['fx_rate_to_scc']

    # attritional large cat split
    claim_df['incurred_100_scc_cat']    = claim_df['incurred_100_scc'].where(  claim_df['cat_bzly_bool'],  0)
    claim_df['incurred_100_scc_a_l']    = claim_df['incurred_100_scc']  - claim_df['incurred_100_scc_cat'] 
    claim_df['large_loss_threshold']    = EXPER_RATING_LL_THRESHOLD * ratio(fx_scc, fx_usd)                                                            # arguably could be detrended
    claim_df['incurred_100_scc_large']  = claim_df['incurred_100_scc_a_l'].where(  claim_df['incurred_100_scc_a_l'] > claim_df['large_loss_threshold'] ,  0)
    claim_df['incurred_100_scc_attr']   = claim_df['incurred_100_scc_a_l']  -  claim_df['incurred_100_scc_large']
    claim_df['bool_large']              = np.where(claim_df['incurred_100_scc_large'] != 0, True, False)

    # filtering and grouping
    cols_claim_grp  = ['yoa']
    cols_claim_sum  = ['incurred_100_scc_attr', 'incurred_100_scc_large', 'incurred_100_scc_cat', 'incurred_100_scc']
    rows_claim_mask =(claim_df['policy_ref'].str[:6] == section_ref6)   if   filt_pol_bool   else True                          # implies use of broadcasting in False Test
    rows_claim_mask = rows_claim_mask &  claim_df['bool_ec'] & (claim_df['bool_covid'] == False)
    claim_grp_df    = claim_df.loc[  rows_claim_mask  ].groupby(  cols_claim_grp, as_index=False   )[  cols_claim_sum  ].sum()


    ### Experience Analysis manipulation > getting assumptions
    # adding yoa column
    exper_df['yoa']             = [i for i in range(yoa_incept - exper_rows, yoa_incept)]
    exper_df['yoa_label']       = exper_df['yoa'].astype(str)

    # enriching/supplementing the data
    exper_df                    = drop_and_merge(exper_df, policy_grp_df, on='yoa')
    exper_df                    = drop_and_merge(exper_df, claim_grp_df,  on='yoa')
    exper_df                    = drop_and_merge(exper_df, yoa_assump_df, on='yoa')

    # rate change
    exper_df['rate_inc_calc']   = ratio(exper_df['gnwp_100_scc'], exper_df['gnwp_100_exp_adj_scc'])
    exper_df['rate_inc_calc']   = exper_df['rate_inc_calc'].where(exper_df['rate_inc_calc'] != 0, exper_df['port_rate'])
    exper_df['rate_inc']        = exper_df['rate_inc_ovd'].fillna(exper_df['rate_inc_calc'] )
    exper_df['rate_cum']        = exper_df['rate_inc'].shift(-1).fillna(1)                                                  # adding 1 and shifting back a year
    exper_df['rate_cum']        = exper_df['rate_cum'].iloc[::-1].cumprod().iloc[::-1]

    # inflation
    exper_df['inf_inc_calc']    = exper_df['port_clm_inflation'].fillna(0)
    exper_df['inf_inc']         = exper_df['inf_inc_ovd'].fillna(exper_df['inf_inc_calc'] )                                 
    exper_df['inf_cum']         =(1 + exper_df['inf_inc']).shift(-1).fillna(1)                                              # adding 1 and shifting back a year
    exper_df['inf_cum']         = exper_df['inf_cum'].iloc[::-1].cumprod().iloc[::-1]                                       # reversing, calculating a forward product and reversing again
    exper_df['inf_cum']        *= (1 + cy_inf)                                                                              # loading for current year inflation so we inflate to the right point, notice also this is not an overridable field per YZ

    # development
    exper_df['maturity_mths']           = (12 * (yoa_incept - exper_df['yoa']) - mth_eval_incept).clip(0,98)                
    exper_df['pct_ultimate']            = np.interp( exper_df['maturity_mths'],   dev_df['month'],   dev_df['factor']   )
    exper_df['attr_pct_ultimate_calc']  = exper_df['pct_ultimate']
    exper_df['large_pct_ultimate_calc'] = 1.0                                                                                 # AC request to assume fully mature Teams 2/3 June 2026
    exper_df['cat_pct_ultimate_calc']   = 1.0                                                                                 # AC request to assume fully mature Teams 2/3 June 2026
    exper_df['attr_pct_ultimate']       = exper_df['attr_pct_ultimate_ovd' ].fillna(exper_df['attr_pct_ultimate_calc'] )
    exper_df['large_pct_ultimate']      = exper_df['large_pct_ultimate_ovd'].fillna(exper_df['large_pct_ultimate_calc'] )
    exper_df['cat_pct_ultimate']        = exper_df['cat_pct_ultimate_ovd'  ].fillna(exper_df['cat_pct_ultimate_calc'] )

    # ielrs
    exper_df['attr_ielr_calc']  = exper_df['ielr_attr']
    exper_df['large_ielr_calc'] = exper_df['ielr_large']
    exper_df['cat_ielr_calc']   = exper_df['ielr_cat']
    exper_df['attr_ielr']       = exper_df['attr_ielr_ovd'].fillna(exper_df['attr_ielr_calc'] )
    exper_df['large_ielr']      = exper_df['large_ielr_ovd'].fillna(exper_df['large_ielr_calc'] )
    exper_df['cat_ielr']        = exper_df['cat_ielr_ovd'].fillna(exper_df['cat_ielr_calc'] )

    ### Experience Analysis manipulation > getting financial values
    # premium
    exper_df['gnwp_nominal_calc'] = exper_df['gnwp_100_scc']
    exper_df['gnwp_nominal']      = exper_df['gnwp_nominal_ovd'].fillna(exper_df['gnwp_nominal_calc'] ).fillna(0.0)
    exper_df['gnwp_ol']           = exper_df['gnwp_nominal'] * exper_df['rate_cum']     

    # calculating helper values for next stage
    md_dict = EXPER_RATING_LOGIC_DICT
    gnwp_ol = exper_df['gnwp_ol']
    gnwp_tot= exper_df["gnwp_ol"].sum()
    inf     = exper_df["inf_cum"]
    rate    = exper_df["rate_cum"]
    yoa     = exper_df["yoa"]    
    min_yr  = lrg_cred_df["num_year"].min()
    max_yr  = lrg_cred_df["num_year"].max()
    first_yr= exper_df.loc[ exper_df["gnwp_nominal"] != 0,    "yoa" ].min()
    num_yrs = ((exper_df["gnwp_nominal"] != 0) & exper_df["include"]).sum()
    num_yrs = np.clip(num_yrs, min_yr, max_yr)
    lrg_cred= lrg_cred_df[  lrg_cred_df['num_year']==num_yrs  ]['credibility'].iat[0]

    # calculating ulrs in ["attr", "large", "cat"]
    p_list  = ["attr", "large", "cat"]   
    for p in p_list:
        # deriving
        pct           = exper_df[f"{p}_pct_ultimate"]
        incurred_calc = exper_df[f"incurred_100_scc_{p}"].fillna(0)                             # handle when no data is loaded
        incurred      = exper_df[f"{p}_incurred_ovd"].fillna(  incurred_calc  )
        ol_incurred   = incurred * inf
        ielr          = exper_df[f"{p}_ielr"]
        cl_ult        = ratio(ol_incurred, pct)
        bf_ult        = ol_incurred   +   (1 - pct) * gnwp_ol * ielr
        ielr_ult      = gnwp_ol * ielr
        cl_lr         = ratio(cl_ult, gnwp_ol)
        bf_lr         = ratio(bf_ult, gnwp_ol)
        max_lr        = np.maximum(cl_lr, ielr)
        nil_lr        = pd.Series(0, index=pct.index)
        lrg_lr        = ielr * lrg_cred + (1 - lrg_cred) * cl_lr
        if p == 'attr':
            method   = np.where(    pct < md_dict["IELR"], "IELR",   np.where(pct < md_dict["BF"], "BF",    "CL" ))
            ulr      = np.where(    pct < md_dict["IELR"],  ielr,    np.where(pct < md_dict["BF"],  bf_lr,  cl_lr))
        elif p == 'large':
            method   = np.where(    yoa < first_yr, "Nil LR",  "Lrg Credibility" )
            ulr      = np.where(    yoa < first_yr,  nil_lr,    lrg_lr )
        elif p == 'cat':
            method   = np.where(    yoa < first_yr, "Nil LR",  "Max LR" )
            ulr      = np.where(    yoa < first_yr,  nil_lr,    max_lr )
                        
        ult = ulr * gnwp_ol

        # assigning
        exper_df[f"{p}_incurred_calc"]       = incurred_calc
        exper_df[f"{p}_incurred"]            = incurred
        exper_df[f"{p}_ol_incurred"]         = ol_incurred
        exper_df[f"{p}_method"]              = method
        exper_df[f"{p}_ol_cl_ultimate"]      = cl_ult
        exper_df[f"{p}_ol_bf_ultimate"]      = bf_ult
        exper_df[f"{p}_ol_ielr_ultimate"]    = ielr_ult
        exper_df[f"{p}_ol_selected_ultimate"]= ult
        exper_df[f"{p}_ol_cl_lr"]            = cl_lr
        exper_df[f"{p}_ol_bf_lr"]            = bf_lr
        exper_df[f"{p}_ol_ielr"]             = ielr
        exper_df[f"{p}_ol_selected_ulr"]     = ulr

    
    # assigning large credibility
    exper_df['large_credibility']     = lrg_cred

    # calculating total ulrs
    exper_df["total_incurred"]            = sum(exper_df[f"{p}_incurred"]             for p in p_list)
    exper_df["total_ol_incurred"]         = sum(exper_df[f"{p}_ol_incurred"]          for p in p_list)
    exper_df["total_ol_cl_ultimate"]      = sum(exper_df[f"{p}_ol_cl_ultimate"]       for p in p_list)
    exper_df["total_ol_bf_ultimate"]      = sum(exper_df[f"{p}_ol_bf_ultimate"]       for p in p_list)
    exper_df["total_ol_ielr_ultimate"]    = sum(exper_df[f"{p}_ol_ielr_ultimate"]     for p in p_list)
    exper_df["total_ol_selected_ultimate"]= sum(exper_df[f"{p}_ol_selected_ultimate"] for p in p_list)    
    exper_df["total_ol_cl_lr"]            = sum(exper_df[f"{p}_ol_cl_lr"]             for p in p_list)
    exper_df["total_ol_ielr"]             = sum(exper_df[f"{p}_ol_ielr"]              for p in p_list)
    exper_df["total_ol_bf_lr"]            = sum(exper_df[f"{p}_ol_bf_lr"]             for p in p_list)
    exper_df["total_ol_selected_ulr"]     = sum(exper_df[f"{p}_ol_selected_ulr"]      for p in p_list)
    exper_df["total_pct_ultimate"]        = exper_df['pct_ultimate']   # YZ request change here for the weighting from Development pattern exper_df["total_pct_ultimate"]        = ratio(exper_df["total_ol_incurred"], exper_df["total_ol_cl_ultimate"]) # could be slightly distortive if get high/low claims

    # adding tiv
    exper_df['tiv_calc']        = cy_tiv   *   ((1.0 + cy_tiv_trend)  **  (exper_df['yoa'] - yoa_incept))
    exper_df['tiv_calc']        = np.where(exper_df["yoa"]  < first_yr, 0, exper_df['tiv_calc'] )           # not loading tiv past earliest GNWP year
    exper_df['tiv']             = exper_df['tiv_ovd'].fillna(exper_df['tiv_calc'] )
    exper_df['tiv']             = np.where(exper_df['yoa'] < first_yr, 0, exper_df['tiv'])                  # not loading tiv past earliest GNWP year

    # weights
    exper_df['wgt_include']       = np.where(exper_df['include'], 1, 0)
    exper_df['wgt_decay']         = EXPER_RATING_DECAY
    exper_df['wgt_decay']         = exper_df['wgt_decay'].shift(-1).fillna(1)                                 
    exper_df['wgt_decay']         = exper_df['wgt_decay'].iloc[::-1].cumprod().iloc[::-1]   
    exper_df['wgt_exposure']      = ratio(exper_df['tiv'], cy_tiv)
    exper_df['wgt_pct_ult']       =exper_df['total_pct_ultimate']
    exper_df['wgt_overall_initial']=(exper_df['wgt_include'] * exper_df['wgt_decay'] * exper_df['wgt_exposure'] * exper_df['wgt_pct_ult'])
    exper_df['wgt_overall_final'] = ratio( exper_df['wgt_overall_initial'], exper_df['wgt_overall_initial'].sum())

    # duplicate cols & ratio to tiv
    exper_df['total_ol_selected_ult_to_tiv']   = ratio(exper_df['total_ol_selected_ultimate'], exper_df['tiv']) * 1000
    exper_df['total_ol_selected_ultimate_dup'] = exper_df['total_ol_selected_ultimate']
    exper_df['total_ol_selected_ulr_dup']      = exper_df['total_ol_selected_ulr']
    exper_df['gnwp_ol_dup']                    = exper_df['gnwp_ol']

    ### Experience Analysis > Assigning Totals
    # strings
    setattr(tt, 'yoa_label', f"Total")

    # sums
    sum_lst = ['attr_ol_incurred',  'attr_ol_cl_ultimate',  'attr_ol_bf_ultimate',  'attr_ol_ielr_ultimate',  'attr_ol_selected_ultimate',
               'large_ol_incurred', 'large_ol_cl_ultimate', 'large_ol_bf_ultimate', 'large_ol_ielr_ultimate', 'large_ol_selected_ultimate',
               'cat_ol_incurred',   'cat_ol_cl_ultimate',   'cat_ol_bf_ultimate',   'cat_ol_ielr_ultimate',   'cat_ol_selected_ultimate',
               'total_ol_incurred', 'total_ol_cl_ultimate', 'total_ol_bf_ultimate', 'total_ol_ielr_ultimate', 'total_ol_selected_ultimate',
               'gnwp_ol' ]
    for k in sum_lst:
        setattr(tt,    k,    exper_df[k].sum())

    # loss ratios
    wgt_lst = ['attr_ol_cl_lr',  'attr_ol_ielr',  'attr_ol_bf_lr',  'attr_ol_selected_ulr'
            , 'large_ol_cl_lr', 'large_ol_ielr', 'large_ol_bf_lr', 'large_ol_selected_ulr'
            , 'cat_ol_cl_lr',   'cat_ol_ielr',   'cat_ol_bf_lr',   'cat_ol_selected_ulr'
            , 'total_ol_cl_lr', 'total_ol_ielr', 'total_ol_bf_lr', 'total_ol_selected_ulr'] 
    for k in wgt_lst:
        setattr(tt,    k,    ratio( (exper_df[k] * gnwp_ol).sum(),    gnwp_tot)  )


    ### Experience Analysis > Assigning Totals on "INCLUDED"
    # strings
    setattr(tti, 'yoa_label', f"Total excl {yoa_incept}")

    # sums
    sum_lst = ['tiv_calc', 'tiv_ovd', 'tiv', 'gnwp_ol_dup', 'total_ol_selected_ultimate_dup']
    for k in sum_lst:
        setattr(tti,    k,    (exper_df[k] * exper_df['include']).sum() )
    
    # loss ratios
    wgt_lst = ['total_ol_selected_ulr_dup']
    for k in wgt_lst:
        setattr(tti,    k,    ratio( (exper_df[k] * exper_df['include'] * gnwp_ol).sum(), gnwp_tot)  )


    ### Experience Analysis > Assigning Current Year
    cy.yoa_label     = f'{yoa_incept}'
    cy.tiv_calc      = cy_tiv
    cy.rate_inc_calc = 1
    cy.rate_inc      = 1
    cy.rate_cum      = 1
    cy.inf_inc_calc  = cy_inf
    cy.inf_inc       = cy_inf
    cy.inf_cum       = 1

    ### Experience Analysis > Final Financials
    yr_exp_wgt_df['exposure_shift1'] = yr_exp_wgt_df['exposure'].shift(-1).fillna(1e12)   
    er.el_cy_tiv            = cy_tiv
    er.el_final_calc        =(exper_df['total_ol_selected_ulr'] * exper_df['gnwp_ol'] * exper_df['wgt_overall_final'] ).sum() * (1 + nmp_load)
    er.el_final_rate        = ratio(er.el_final_calc * 1000, cy_tiv)    # multiplying by 1000 to convert to per 1000
    er.el_final             = pick_override(er.el_final_ovd,   er.el_final_calc)

    er.el_avg_exposure     = (exper_df['tiv']   *   exper_df['wgt_overall_final'] ).sum()
    er.el_years            = int(0 if pd.isna(first_yr) else num_yrs)
    avg_exp_usd            = er.el_avg_exposure * ratio(fx_usd, fx_scc)   
    er.el_avg_exposure_band= look_up_with_bounds(avg_exp_usd, 'exposure', 'exposure_shift1', 'exposure', yr_exp_wgt_df, if_not_found=0)
    er.el_weight_calc      = look_up_with_bounds(avg_exp_usd, 'exposure', 'exposure_shift1', f'{er.el_years}yr', yr_exp_wgt_df, if_not_found=0)
    er.el_weight           = pick_override(er.el_weight_ovd,   er.el_weight_calc)

    # store df back to rater
    rater['exper_df']  = exper_df
    rater['policy_df'] = policy_df
    rater['claim_df']  = claim_df
