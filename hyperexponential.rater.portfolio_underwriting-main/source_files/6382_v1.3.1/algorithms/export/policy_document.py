import hx
import pandas as pd
import numpy as np
import json
from datetime import datetime
from algorithms.rate_utilities              import pd_df_from_hx_list, ratio, drop_and_merge
from algorithms.export.analysis_column_list import own_detail_cols, own_summary_cols, lloyds_detail_cols, lloyds_summary_cols, beazley_detail_cols, beazley_summary_cols
from libraries.model_profiler.algorithms.profiling_hxd_functions import time_me


# calculates weighted average for all specified numeric columns based on a supplied weightings df
def weighted_avgs(df, num_cols, weights_df, key_col, weights_col, fill_mtx):
    """
    Weighted averages for each column in `num_cols`, using weights from
    `weights_df` keyed by `key_col`. Missing values treated as zero.
    This uses map so is only appropriate for lower record count df e.g. 1k.
    """
    w_ss        = weights_df.set_index(key_col)[weights_col]                            # series of weights indexed by key_col
    num_mtx     = df[num_cols].apply(pd.to_numeric, errors="coerce").to_numpy(float)    # numpy 2D array for applying weights to
    num_mtx     = np.nan_to_num(num_mtx, nan=fill_mtx)                                  # errortrapping nans
    wt_1d       = df[key_col].map(w_ss).fillna(0.0).to_numpy(float)                     # numpy 1D array of weight, same order as df
    wt_2d       = wt_1d[:, None]                                                        # numpy 2D array n x 1 to allow subsequent multiplication
    numer       = (num_mtx * wt_2d).sum(axis=0)                                         # numpy 1D array 1 x num_cols
    denom       = wt_1d.sum()                                                           # scalar value of total weight
    out_ss      = pd.Series(np.nan if denom == 0 else numer / denom, index=num_cols)    # calculating weighted avg, errortrapping nil
    return out_ss



# Convert hx_list to a dictionary of lists
def list_converter(hx_list, col_order = []):
    df = pd_df_from_hx_list(hx_list)
    if col_order:
        df = df[col_order]

    dict_of_lists = df.to_dict(orient='records')

    return dict_of_lists


# Convert hx_list to a dictionary of lists
def df_converter(df, col_order = []):
    if col_order:
        df = df[col_order]
    dict_of_lists = df.to_dict(orient='records')
    return dict_of_lists




def _format_value(val: float):
    if val < 1_000_000:
        return f"{val/1_000:,.2f}k"
    else:
        return f"{val/1_000_000:,.2f}m"


def build_deduction_strings(hxd, rater):
    # load df
    deductions_df = rater["deductions_df"]
    # prem_limit_df = rater["prem_limit_data"][["selected_lob", "bst_share_ultimate_gross_premium"]]
    prem_limit_df = rater['prem_limit_data'].groupby("selected_lob", as_index=False)["bst_share_ultimate_gross_premium"].sum() # 22-april fix to handle non-unique lobs in df


    # detail columns needed
    cols = [
        {"field": "market_deductions",              "label": "Market Deductions"},
        {"field": "mga_fee",                        "label": "Consortium Managers fee / MGA fee"},
        {"field": "facility_brokerage",             "label": "Facility Brokerage"},
        {"field": "leaders_fee",                    "label": "Learders Fee"},
        {"field": "service_fee",                    "label": "Service Fee"},
        {"field": "other",                          "label": "Other"},
        {"field": "selected_effective_deductions",  "label": "Total Deductions"}
    ]

    all_cols    = ["selected_lob"] + [c["field"] for c in cols]
    combined_df = prem_limit_df.merge(  deductions_df[all_cols],   on="selected_lob",   how="left")
    deductions  = {}

    for index, col in enumerate(cols, start=1): 
        numer                          = (combined_df[col["field"]] * combined_df["bst_share_ultimate_gross_premium"]).sum()
        denom                          = combined_df["bst_share_ultimate_gross_premium"].sum()
        deductions[col["field"]]       = ratio(numer, denom)
        deductions[f"ded_str_{index}"] = f"{deductions[col['field']] * 100:.2f}% - {col['label']}"

    return deductions


def build_key_lob_str(hxd, rater):
    df      = rater["prem_limit_data"]
    lobs    = df["selected_lob"].dropna()
    value   = ", ".join(lobs.astype(str))
    return value


def build_trifocus_string(hxd, rater):
    df                           = rater["prem_limit_data"]
    df['portfolio_composition']  = pd.to_numeric(df['portfolio_composition'], errors='coerce')
    idx                          = df['portfolio_composition'].idxmax()
    value                        = df.loc[idx, 'assigned_trifocus']
    return value


def build_risk_codes_str(hxd, rater):
    df                  = rater["risk_composition_final"]
    df['composition']   = pd.to_numeric(df['composition'], errors='coerce')
    df                  = df[["risk_code", "composition"]].dropna()
    grp_df              =(df.groupby('risk_code', sort=False).agg({'composition':'sum'})
                            .sort_values("composition", ascending=False, kind="mergesort")
                            .reset_index(drop=False))
    grp_df              = grp_df.head(5)
    grp_df['comp_str']  = (grp_df["composition"].astype(float)* 100).round(2).astype(str) + '%'
    grp_df['desc']      = grp_df['risk_code'] + " (" + grp_df['comp_str'] + ")"
    value               = ", ".join(grp_df['desc'].astype(str))
    return value


def build_prem_average_limit_str(hxd):
    currency             = hxd.cds.currencies.source_currency
    max_limit_at_100_per = hxd.cds.prem_limit_profile.summary.max_limit_at_100_per or 0
    avg_limit_at_100_per = hxd.cds.prem_limit_profile.summary.avg_limit_at_100_per or 0
    value                = f"{currency} {_format_value(max_limit_at_100_per)} / {currency} {_format_value(avg_limit_at_100_per)}"
    return value


def build_gn_prem(hxd):
    def format_value(val: float, suffix: str) -> str:
        if val < 1_000_000: return f"{val/1_000    :,.2f}k {suffix}"
        else:               return f"{val/1_000_000:,.2f}m {suffix}"
    currency                         = hxd.cds.currencies.source_currency
    bst_net_premium                  = hxd.cds.prem_limit_profile.summary.bst_net_premium or 0
    bst_share_ultimate_gross_premium = hxd.cds.prem_limit_profile.summary.bst_share_ultimate_gross_premium or 0 
    value                            =( f"{currency} {format_value(bst_share_ultimate_gross_premium, 'GROSS')} / "
                                       +f"{currency} {format_value(bst_net_premium,                  'NET')}"       )                               
    return value


def build_pc_description(hxd, rater):
    pc_structure_df = rater['pc_structure']

    profit_commission_description = ""

    if hxd.cds.risk_information.is_profit_comission:
        pc_structure_df     = pc_structure_df[pc_structure_df["selected_lob"].notna()]
        standard_bool       = (pc_structure_df["pc_type"] == "Standard").any()
        sliding_scale_bool  = (pc_structure_df["pc_type"] == "Sliding Scale").any()
        if standard_bool and sliding_scale_bool:
            profit_commission_description = "PC varies by class of business, refer to profit commission section below"
        else:
            uw_expense      = pc_structure_df["uw_expense"].values[0]
            expense_basis   = pc_structure_df["expense_basis"].values[0]
            if standard_bool:
                pc_percent  = pc_structure_df["std_pc_percent"].values[0]
                profit_commission_description = f"{pc_percent * 100:.5f}% after {uw_expense * 100}% Underwriting expenses on {expense_basis}"
            else:
                profit_commission_description = f"Sliding Scale PC after {uw_expense * 100}% Underwriting expenses on {expense_basis}"
    else:
        profit_commission_description = "Not Applicable"

    return profit_commission_description


def build_anti_sel_uncert_str(hxd):
    # paths
    al_path         = hxd.cds.rating_summary.additional_loadings.summary
    fp_path         = hxd.cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary
    
    # conditions
    is_bbt          = hxd.cds.risk_information.follow_main_syndicate
    
    # values
    anti_selection  = f"{(al_path.anti_selection_charge  or 0) * 100:.2f}"
    uncertainty     = f"{(al_path.uncertainty_charge     or 0) * 100:.2f}"
    
    add_charge_bbt  = f"{(al_path.additional_charge_bbt  or 0) * 100:.2f}"
    add_charge_xbbt = f"{(al_path.additional_charge      or 0) * 100:.2f}"
    add_charge      = (add_charge_bbt if is_bbt else add_charge_xbbt) or 0
    
    uw_adj_bbt      = f"{(fp_path.uw_adj_bbt             or 0) * 100:.2f}"
    uw_adj          = f"{(fp_path.uw_adj                 or 0) * 100:.2f}"
    uw_adj          = (uw_adj_bbt if is_bbt else uw_adj) or 0

    value           = f"{anti_selection}% / {uncertainty}% / {add_charge}% / {uw_adj}%"
    return value


def dict_sclr_summary(hxd, rater, bbt_priced, case_priced, prem_avail):
    
    # pathways
    cds  = hxd.cds
    sf   = cds.standard_fields
    ri   = cds.risk_information
    fp   = cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary       # final (uw) pricing
    ap   = cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_actuarial_basis.summary     # actuarial  pricing
    rp   = cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_pre_adj.summary             # raw        pricing
    po   = cds.rating_summary.pricing_outputs
    cp   = cds.rating_summary.case_pricing
    layer= cds.layers[0]  

    not_main = bbt_priced or case_priced

    #helper calcs by bbt, case price, standard
    if case_priced:
        brk  = cp.brokerage or 0
        line = cp.written_line or 0 
        ggwp = cp.quoted_premium_100 or 0
        lob  = cp.tracker_class or ""
        deductions              = {}
        deductions["ded_str_1"] = f"{brk * 100:.2f}% - Total Deductions"
        key_lob                 = lob
        trifocus                = lob
        risk_codes              = ""
        max_avg_limit           = ""
        gn_prem                 = ggwp * (1 - brk) * line
        pc_descrption           = ""

    elif bbt_priced:
        brk                     = po.deductions_5623 or 0
        deductions              = {}
        deductions["ded_str_1"] = f"{brk * 100:.2f}% - Total Deductions"
        key_lob                 = f'BBT Class - {po.tracker_class or ""}'
        trifocus                =  po.tracker_class or ""   
        risk_codes              = ""
        max_avg_limit           = ""
        gn_prem                 = po.afb_api
        pc_descrption           = ""

    else:    
        deductions      = build_deduction_strings(      hxd, rater)
        key_lob         = build_key_lob_str(            hxd, rater)
        trifocus        = build_trifocus_string(        hxd, rater)
        risk_codes      = build_risk_codes_str(         hxd, rater)
        max_avg_limit   = build_prem_average_limit_str( hxd)
        gn_prem         = build_gn_prem(                hxd)
        pc_descrption   = build_pc_description(         hxd, rater)
    
    # loadings needs no modifications
    final_loadings  = build_anti_sel_uncert_str(    hxd)

    data = {
            "summary_insured_name":             sf.insured_name
            ,"summary_policy_reference":        sf.policy_reference
            ,"summary_underwriter":             sf.underwriter
            ,"summary_facility_type":           ri.facility_type
            ,"summary_deal_status":             ri.deal_status
            ,"summary_key_lob":                 key_lob
            ,"summary_trifocus":                trifocus
            ,"summary_risk_codes":              risk_codes
            ,"summary_renewal":                 sf.is_renewal              

            ,"summary_inception_date":          hxd.hx_core.inception_date
            ,"summary_expiry_date":             hxd.hx_core.expiry_date
            ,"summary_line_size":               cds.prem_limit_profile.summary.bst_share_line_size
            ,"summary_max_avg_limit":           max_avg_limit
            ,"summary_gn_prem":                 gn_prem

            ,"summary_ded_str_1":               deductions["ded_str_1"]
            ,"summary_ded_str_2":               "" if not_main else deductions["ded_str_2"]
            ,"summary_ded_str_3":               "" if not_main else deductions["ded_str_3"]
            ,"summary_ded_str_4":               "" if not_main else deductions["ded_str_4"]
            ,"summary_ded_str_5":               "" if not_main else deductions["ded_str_5"]
            ,"summary_ded_str_6":               "" if not_main else deductions["ded_str_6"]
            ,"summary_ded_str_7":               "" if not_main else deductions["ded_str_7"]

            ,"summary_pc":                      pc_descrption
            ,"summary_key_uncertainty":         hxd.cds.rationale.key_uncertainties
            ,"summary_actuary":                 ri.actuary_reviewed if ri.priced_by == "Actuarial" else "N/A (Priced by Underwriting)"
            # ,"summary_export_date":                                       NEEDS TO BE SET IN TASK - CANT GET TIME NOW IN ALGO
            # ,"summary_hx_model_ref":                                      NEEDS TO BE SET IN TASK - CANT GET environment IN ALGO

            ,"summary_analysis":                hxd.cds.rating_summary.case_pricing.case_pricing_analysis_location
            ,"summary_final_loadings":          final_loadings
            ,"summary_final_pc":                "" if case_priced else ap.pc_impact
            ,"summary_final_gn_ulr":            layer.pflr #if case_priced else fp.best_estimate_gn
            ,"summary_final_bpi":               layer.bpi  #if case_priced else fp.bpi
            ,"summary_final_tpi":               layer.tpi  #if case_priced else fp.tpi
            ,"summary_final_roc":               layer.roc  #if case_priced else fp.roc

            ,"summary_raw_pc":                  "" if case_priced else rp.pc_impact
            ,"summary_raw_gn_ulr":              "" if case_priced else rp.best_estimate
            ,"summary_raw_bpi":                 "" if case_priced else rp.bpi
            ,"summary_raw_tpi":                 "" if case_priced else rp.tpi
            ,"summary_raw_roc":                 "" if case_priced else rp.roc

            ,"is_bbt":                          bbt_priced
            ,"is_case_priced":                  case_priced
            ,"is_prem_avail":                   prem_avail

            }
    return data   



# converts to dictionary from df
def dict_table_model_gn_ulr(hxd, rater):
    # get the df
    wgt_df  = rater['rat_sum_mod_wgt']
    ulr_df  = rater['rat_sum_proj_gnulr']
    df      = drop_and_merge(ulr_df, wgt_df, 'selected_lob' )
    
    # required columns
    cols    = [  "selected_lob"         ,"gn_premium"           ,"portfolio_percent"
                ,"own_exp_gn_ulr"       ,"lloyds_gn_ulr"        ,"bp_gn_ulr"
                ,"own_experience"       ,"lloyds_proj"          ,"bp_proj"
                ,"case_pricing", "beazley_proj"
                ,"model_estimate"                                                       ]

    return df_converter(df, col_order=cols)   


# converts to dictionary from scalar values
def dict_sclr_table_model_gn_ulr_total(hxd, rater):
    # pathways
    cds  = hxd.cds
    ulr  = cds.rating_summary.model_gn_ulr.projected_gn_ulr.summary       
    wgt  = cds.rating_summary.model_gn_ulr.model_weights.summary     

    data = {
             "table_model_gn_ulr_total_gn_premium" 	         : ulr.gn_premium
            ,"table_model_gn_ulr_total_portfolio_pct"        : ulr.portfolio_percent
            ,"table_model_gn_ulr_total_ulr_own_experience"   : ulr.own_exp_gn_ulr
            ,"table_model_gn_ulr_total_ulr_lloyds"           : ulr.lloyds_gn_ulr
            ,"table_model_gn_ulr_total_ulr_business_plan"    : ulr.bp_gn_ulr
            ,"table_model_gn_ulr_total_wgt_own_experience"   : wgt.own_experience
            ,"table_model_gn_ulr_total_wgt_lloyds"           : wgt.lloyds_proj
            ,"table_model_gn_ulr_total_wgt_business_plan"    : wgt.bp_proj
            ,"table_model_gn_ulr_total_wgt_case_pricing"     : wgt.case_pricing
            ,"table_model_gn_ulr_total_wgt_beazley"          : wgt.beazley_proj
            ,"table_model_gn_ulr_total_ulr"                  : wgt.model_estimate
        }
    return data



# converts to dictionary from df
def dict_table_selected_ulr(hxd, rater):

    # sourcing the df
    ini_ulr_df  = rater['rat_sum_mod_wgt']
    cat_df      = rater['rat_sum_cat_alloc' ]
    load_df     = rater['rat_sum_add_load'  ]
    act_ulr_df  = rater['rat_sum_adeq_act'  ]
    fin_ulr_df  = rater['rat_sum_adeq_final']

    # merging the df
    df1     = drop_and_merge(ini_ulr_df, cat_df,     'selected_lob' )
    df2     = drop_and_merge(df1,        load_df,    'selected_lob' )
    df3     = drop_and_merge(df2,        act_ulr_df, 'selected_lob' )
    df4     = drop_and_merge(df3,        fin_ulr_df, 'selected_lob' )
    
    # calc additional columns
    df4['init_ulr'] = df4['model_estimate']
    df4['nmp']      = df4['nmp_load_general'] + df4['nmp_load_weather'] 
    df4['climate']  = df4['model_estimate'] * df4['cat'] * df4['climate_change_load']
    df4['base_ulr'] = df4['init_ulr'] + df4['nmp'] + df4['climate']

    # required columns
    cols    = [  "selected_lob"         ,"init_ulr"             
                ,"nmp"                  ,"climate"              ,"base_ulr"        
                ,"anti_selection_charge","uncertainty_charge"   ,"additional_charge"          
                ,"pc_impact"            ,"uw_adj"               ,"best_estimate_gn"     ]

    return df_converter(df4, col_order=cols)   


def dict_sclr_table_selected_ulr_total(hxd, rater):
    # pathways
    cds  = hxd.cds
    wgt  = cds.rating_summary.model_gn_ulr.model_weights.summary     
    cat  = cds.rating_summary.cat_loadings.summary   
    load = cds.rating_summary.additional_loadings.summary   
    abase= cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_actuarial_basis.summary   
    fbase= cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary   

    # calcs
    nmp     = cat.nmp_load_general + cat.nmp_load_weather
    climate = wgt.model_estimate * cat.cat * cat.climate_change_load
    base_ulr= wgt.model_estimate + nmp + climate

    # assignment
    data = {
             "table_selected_ulr_total_model_gn_ulr" 	    : wgt.model_estimate
            ,"table_selected_ulr_total_nmp"                 : nmp
            ,"table_selected_ulr_total_climate"             : climate
            ,"table_selected_ulr_total_selected_gn_ulr"     : base_ulr
            ,"table_selected_ulr_total_anti_selection"      : load.anti_selection_charge
            ,"table_selected_ulr_total_uncertainty"         : load.uncertainty_charge
            ,"table_selected_ulr_total_additional_charge"   : load.additional_charge
            ,"table_selected_ulr_total_pc"                  : abase.pc_impact
            ,"table_selected_ulr_total_uw_adjustment"       : fbase.uw_adj
            ,"table_selected_ulr_total_final_gn_ulr"        : fbase.best_estimate_gn
        }
    return data


# converts to dictionary from df
def dict_table_tech_adequacy_metrics(hxd, rater):

    # sourcing the df
    ulr_df      = rater['rat_sum_proj_gnulr']
    pre_ulr_df  = rater['rat_sum_adeq_pre'  ]
    fin_ulr_df  = rater['rat_sum_adeq_final']

    # columns rename
    cols_act_orig   = ['best_estimate',     'bpi',     'tpi',     'roc'    ] 
    cols_act_new    = ['act_gnulr',         'act_bpi', 'act_tpi', 'act_roc']
    cols_fin_orig   = ['best_estimate_gn',  'bpi',     'tpi',     'roc'    ] 
    cols_fin_new    = ['fin_gnulr',         'fin_bpi', 'fin_tpi', 'fin_roc']
    pre_ulr_df      = pre_ulr_df.rename(  columns=dict(zip(cols_act_orig,  cols_act_new))  )
    fin_ulr_df      = fin_ulr_df.rename(  columns=dict(zip(cols_fin_orig,  cols_fin_new))  )

    # merging the df
    df1     = drop_and_merge(ulr_df, pre_ulr_df,    'selected_lob' )
    df2     = drop_and_merge(df1,    fin_ulr_df,    'selected_lob' )

    # required columns
    cols    = [  "selected_lob"         ,"gn_premium"             
                ,"fin_gnulr"            ,"fin_bpi"      ,"fin_tpi"  ,"fin_roc"  
                ,"act_gnulr"            ,"act_bpi"      ,"act_tpi"  ,"act_roc"  ]

    return df_converter(df2, col_order=cols)  



def dict_sclr_table_tech_adequacy_metrics_total(hxd, rater):
    # pathways
    cds  = hxd.cds
    ulr  = cds.rating_summary.model_gn_ulr.projected_gn_ulr.summary  
    pbase= cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_pre_adj.summary   
    fbase= cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary   

    # assignment
    data = {
             "table_tech_adequacy_metrics_total_gn_premium" 	: ulr.gn_premium
            ,"table_tech_adequacy_metrics_total_loaded_gn_ulr"  : fbase.best_estimate_gn
            ,"table_tech_adequacy_metrics_total_loaded_bpi"     : fbase.bpi
            ,"table_tech_adequacy_metrics_total_loaded_tpi"     : fbase.tpi
            ,"table_tech_adequacy_metrics_total_loaded_roc"     : fbase.roc
            ,"table_tech_adequacy_metrics_total_raw_gn_ulr"     : pbase.best_estimate
            ,"table_tech_adequacy_metrics_total_raw_bpi"        : pbase.bpi
            ,"table_tech_adequacy_metrics_total_raw_tpi"        : pbase.tpi
            ,"table_tech_adequacy_metrics_total_raw_roc"        : pbase.roc

        }
    return data



# converts to dictionary from df
def dict_table_premium_limit_profile_old(hxd, rater):
    # sourcing the df
    df      = rater['prem_limit_data']

    # required columns
    cols    = [  "selected_lob"                     ,"future_ultimate_gross_prem"       ,"bst_share_line_size"  
                ,"bst_share_ultimate_gross_premium" ,"bst_deductions"                   ,"bst_net_premium"  
                ,"max_limit_at_100_per"             ,"avg_limit_at_100_per"             ,"max_limit_at_bst_share" ]

    return df_converter(df, col_order=cols)  


def dict_table_premium_limit_profile(hxd, rater):
    # sourcing the df
    df = rater["prem_limit_data"]

    # aggregation groups
    sum_cols = [
        "future_ultimate_gross_prem",
        "bst_share_ultimate_gross_premium",
        "bst_net_premium",
    ]

    max_cols = [
        "max_limit_at_100_per",
        "max_limit_at_bst_share",
    ]

    avg_cols = [
        "avg_limit_at_100_per",
    ]

    agg_map = {col: "sum" for col in sum_cols}
    agg_map.update({col: "max" for col in max_cols})
    agg_map.update({col: "mean" for col in avg_cols})

    grouped = (
        df.groupby("selected_lob", as_index=False, sort=False)
        .agg(agg_map)
    )

    # weighted average bst_deductions
    deductions = (
        df.groupby("selected_lob", sort=False)
        .apply(
            lambda x: np.average(
                x["bst_deductions"],
                weights=x["bst_share_ultimate_gross_premium"],
            )
            if x["bst_share_ultimate_gross_premium"].sum() > 0
            else np.nan
        )
        .reset_index(name="bst_deductions")
    )

    grouped = grouped.merge(deductions, on="selected_lob", how="left")

    # derived metric
    grouped["bst_share_line_size"] = (
        grouped["bst_share_ultimate_gross_premium"]
        / grouped["future_ultimate_gross_prem"]
    )

    cols = [
        "selected_lob",
        "future_ultimate_gross_prem",
        "bst_share_line_size",
        "bst_share_ultimate_gross_premium",
        "bst_deductions",
        "bst_net_premium",
        "max_limit_at_100_per",
        "avg_limit_at_100_per",
        "max_limit_at_bst_share",
    ]

    return df_converter(grouped, col_order=cols)



# converts to dictionary from scalar values
def dict_sclr_table_premium_limit_profile_total(hxd, rater):
    # pathways
    cds  = hxd.cds
    path  = cds.prem_limit_profile.summary     

    data = {
             "table_premium_limit_profile_total_gg_premium_100" : path.future_ultimate_gross_prem
            ,"table_premium_limit_profile_total_line"           : path.bst_share_line_size
            ,"table_premium_limit_profile_total_gg_premium_bst" : path.bst_share_ultimate_gross_premium
            ,"table_premium_limit_profile_total_deductions"     : path.bst_deductions
            ,"table_premium_limit_profile_total_gn_premium_bst" : path.bst_net_premium
            ,"table_premium_limit_profile_total_max_limit_100"  : path.max_limit_at_100_per
            ,"table_premium_limit_profile_total_avg_limit_100"  : path.avg_limit_at_100_per
            ,"table_premium_limit_profile_total_max_limit_bst"  : path.max_limit_at_bst_share
        }
    return data



# converts to dictionary from df
def dict_table_deductions(hxd, rater):
    # sourcing the df
    df      = rater['deductions_df']

    # required columns
    cols    = [  "selected_lob"         ,"market_deductions"            ,"mga_fee"  
                ,"facility_brokerage"   ,"leaders_fee"                  ,"service_fee"  
                ,"other"                ,"selected_effective_deductions"                ]

    return df_converter(df, col_order=cols) 


# converts to dictionary from df
def dict_sclr_table_deductions_total(hxd, rater):

    # required columns
    num_cols    = [  "market_deductions"    ,"mga_fee"      ,"facility_brokerage"   
                    ,"leaders_fee"          ,"service_fee"  ,"other"                
                    ,"selected_effective_deductions"                                ]
    cols        = num_cols + ["selected_lob"]
    weights_col = "bst_share_ultimate_gross_premium"                                    # use "bst_net_premium" for net premium

    # sourcing the df
    df          = rater['deductions_df'  ][cols]
    weights_df  = rater['prem_limit_data'].groupby("selected_lob", as_index=False)[weights_col].sum() # 22-april fix to handle non-unique lobs in df

    # getting the weighted series
    ss      = weighted_avgs(df, num_cols, weights_df, "selected_lob", weights_col, 0)

    # assigning the values
    data = {
             "table_deductions_total_market"    : ss['market_deductions']
            ,"table_deductions_total_consortium": ss['mga_fee']
            ,"table_deductions_total_facility"  : ss['facility_brokerage']
            ,"table_deductions_total_leader_fee": ss['leaders_fee']
            ,"table_deductions_total_service_fee":ss['service_fee']
            ,"table_deductions_total_other"     : ss['other']
            ,"table_deductions_total_all"       : ss['selected_effective_deductions']
        }
    return data



# converts to dictionary from scalar values
def dict_sclr_table_deductions_basis(hxd, rater):
    # pathways
    cds         = hxd.cds
    manual      = cds.assumed_deductions.model_type.selected == "Manual"
    data_path   = cds.assumed_deductions.data_driven_deductions.deductions.basis
    manual_path = cds.assumed_deductions.deductions_manually_entered.basis
    path        = manual_path if manual else data_path

    data = { "table_deductions_basis_consortium"    : path.mga_fee
            ,"table_deductions_basis_facility"      : path.facility_brokerage
            ,"table_deductions_basis_leader_fee"    : path.leaders_fee
            ,"table_deductions_basis_service_fee"   : path.service_fee
            ,"table_deductions_basis_other"         : path.other
        }
    return data



# converts to dictionary from df
def dict_table_rate_change(hxd, rater):
    # sourcing the df
    df      = rater['rate_change_data']

    # required columns
    num_cols    = [  "year_0/selected"    ,"year_1/selected"    ,"year_2/selected"   
                    ,"year_3/selected"    ,"year_4/selected"    ,"year_5/selected"                
                    ,"year_6/selected"    ,"year_7/selected"    ,"year_8/selected"  ]
    cols        = ["selected_lob"] + num_cols

    return df_converter(df, col_order=cols) 



# converts to dictionary from df
def dict_sclr_table_rate_change_total(hxd, rater):

    # required columns
    num_cols    = [  "year_0/selected"    ,"year_1/selected"    ,"year_2/selected"   
                    ,"year_3/selected"    ,"year_4/selected"    ,"year_5/selected"                
                    ,"year_6/selected"    ,"year_7/selected"    ,"year_8/selected"  ]
    cols        = num_cols + ["selected_lob"]
    weights_col = "bst_net_premium"                                    # use "bst_share_ultimate_gross_premium" for gross premium

    # sourcing the df
    df          = rater['rate_change_data'][cols]
    weights_df  = rater['prem_limit_data'].groupby("selected_lob", as_index=False)[weights_col].sum() # 22-april fix to handle non-unique lobs in df
    
    # getting the weighted series
    ss      = weighted_avgs(df, num_cols, weights_df, "selected_lob", weights_col, 1)

    # assigning the values
    data = {
             "table_rate_change_total_cy" : ss['year_0/selected']
            ,"table_rate_change_total_py1": ss['year_1/selected']
            ,"table_rate_change_total_py2": ss['year_2/selected']
            ,"table_rate_change_total_py3": ss['year_3/selected']
            ,"table_rate_change_total_py4": ss['year_4/selected']
            ,"table_rate_change_total_py5": ss['year_5/selected']
            ,"table_rate_change_total_py6": ss['year_6/selected']
            ,"table_rate_change_total_py7": ss['year_7/selected']
            ,"table_rate_change_total_py8": ss['year_8/selected']
        }
    return data



# converts to dictionary from df
def dict_table_own_experience(hxd, rater):
    # sourcing the df
    df      = rater['proj_own_exper_summary']

    # required columns
    num_cols    = ["selected_attr", "selected_large", "selected_cat", "selected_total", "selected_total_excl_cat"]
    cols        = ["selected_lob"] + ['cat_basis'] + num_cols

    return df_converter(df, col_order=cols) 



# converts to dictionary from df
def dict_sclr_table_own_experience_total(hxd, rater):

    # required columns
    num_cols    = ["selected_attr", "selected_large", "selected_cat", "selected_total", "selected_total_excl_cat"]
    cols        = num_cols + ["selected_lob"]                           # notice no cat basis
    weights_col = "bst_net_premium"                                     # use "bst_share_ultimate_gross_premium" for gross premium

    # sourcing the df
    df          = rater['proj_own_exper_summary'][cols]
    weights_df  = rater['prem_limit_data'].groupby("selected_lob", as_index=False)[weights_col].sum() # 22-april fix to handle non-unique lobs in df
    
    # getting the weighted series
    ss      = weighted_avgs(df, num_cols, weights_df, "selected_lob", weights_col, 0)

    # assigning the values
    data = { "table_own_experience_total_attritional_gn_ulr": ss['selected_attr'          ]
            ,"table_own_experience_total_large_gn_ulr"      : ss['selected_large'         ]
            ,"table_own_experience_total_cat_gn_ulr"        : ss['selected_cat'           ]
            ,"table_own_experience_total_overall_gn_ulr"    : ss['selected_total'         ]
            ,"table_own_experience_total_xcat_gn_ulr"       : ss['selected_total_excl_cat']        }
    
    return data



# converts to dictionary from df
def dict_table_profit_commission(hxd, rater):
    # extra values needed
    is_pc_interlocking  = hxd.cds.pc.pc_control.is_pc_interlocking
    dcf_opt             = hxd.cds.pc.pc_control.dcf_opt
    ul_binders_pc       = hxd.cds.pc.pc_control.ul_binders_pc
    dcf_exper_num_yrs   = hxd.cds.pc.pc_control.dcf_exper_num_yrs
    dcf_amount          = hxd.cds.pc.pc_control.dcf_amount
    dcf_amount_basis    = hxd.cds.pc.pc_control.dcf_amount_basis

    # calculate deficit
    if dcf_opt == "Experience":
        deficit = f'{dcf_exper_num_yrs}yrs'
    elif dcf_opt == "$ Amount":
        deficit = f'{dcf_amount} amt'
    else:
        deficit = dcf_opt

    # sourcing the df
    df      = rater['pc_structure']

    # add columns
    df['is_pc_interlocking'] = is_pc_interlocking
    df['deficit']            = deficit
    df['ul_binders_pc']      = ul_binders_pc
    df["std_pc_percent_txt"] = df["std_pc_percent"].map(lambda brk: f"{brk * 100:.2f}%" if pd.notna(brk) else "")
    df['pc_pct']    = np.where(df["pc_type"]=="Standard", df['std_pc_percent_txt'], "Refer to binding agreement")

    # required columns
    cols        = ["selected_lob",  "is_pc_interlocking", "deficit",        "ul_binders_pc",
                   "pc_type",       "uw_expense",         "expense_basis",  "pc_pct"        ]

    return df_converter(df, col_order=cols) 





# Format data in dictionary for Excel
def clean_data_for_policy_doc(data):
    dates_lst = ["summary_inception_date", "summary_expiry_date"]   # allow more generic specification of dates
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






# Create data dictionary to write to Excel file
def create_dict_for_excel(hxd, rater):
    cds     = hxd.cds

    # special process flows
    bbt_priced = cds.risk_information.follow_main_syndicate
    case_priced= cds.standard_fields.rating_methodology != "Rater"
    prem_avail = (cds.risk_information.prem_data_available
                    and 'selected_lob' in rater['proj_own_exper_summary'].columns)
    
    ##########################################################################################
    ### customised code to push merged dictionaries and additional dataframes expressed as dictionary
    ##########################################################################################
    # Add basic scalar fields below in all cases
    data    = dict_sclr_summary(hxd, rater, bbt_priced, case_priced, prem_avail)

    # if not bbt and not case_priced then do below
    if not (bbt_priced or case_priced):
        # Add additional scalar fields below
        data    = (   data   
                    | dict_sclr_table_model_gn_ulr_total(           hxd, rater)
                    | dict_sclr_table_selected_ulr_total(           hxd, rater)  
                    | dict_sclr_table_tech_adequacy_metrics_total(  hxd, rater)
                    | dict_sclr_table_premium_limit_profile_total(  hxd, rater)
                    | dict_sclr_table_deductions_total(             hxd, rater)                
                    | dict_sclr_table_deductions_basis(             hxd, rater)     # notice this is basis and not total (above)
                    | dict_sclr_table_rate_change_total(            hxd, rater)
                    |(dict_sclr_table_own_experience_total(         hxd, rater) if prem_avail else {})
                    )

        # Add summary tables
        data["table_model_gn_ulr"]          = dict_table_model_gn_ulr(          hxd, rater)
        data['table_selected_ulr']          = dict_table_selected_ulr(          hxd, rater)
        data['table_tech_adequacy_metrics'] = dict_table_tech_adequacy_metrics( hxd, rater)
        data['table_premium_limit_profile'] = dict_table_premium_limit_profile( hxd, rater)    
        data['table_deductions']            = dict_table_deductions(            hxd, rater)
        data['table_rate_change']           = dict_table_rate_change(           hxd, rater)
        data['table_profit_commission']     = dict_table_profit_commission(     hxd, rater)
        data['table_own_experience']        = dict_table_own_experience(        hxd, rater) if prem_avail else None

        # add analysis tables
        data['table_own_experience_summary']= df_converter(rater['proj_own_exper_summary'][own_summary_cols],     own_summary_cols    )  if prem_avail else None
        data['table_own_experience_detail'] = df_converter(rater['proj_own_exper_detail' ][own_detail_cols],      own_detail_cols     )  if prem_avail else None
        data['table_lloyds_summary']        = df_converter(rater['proj_lloyds_summary'][   lloyds_summary_cols],  lloyds_summary_cols ) 
        data['table_lloyds_detail']         = df_converter(rater['proj_lloyds_detail'][    lloyds_detail_cols],   lloyds_detail_cols  )
        data['table_beazley_summary']       = df_converter(rater['proj_beazley_summary'][  beazley_summary_cols], beazley_summary_cols)
        data['table_beazley_detail']        = df_converter(rater['proj_beazley_detail'][   beazley_detail_cols],  beazley_detail_cols )

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



# Push dictionary to hxd for storage
@time_me
def store_policy_data(hxd, rater):

    # Don't run if premium has not been input
    marked_complete = hxd.non_cds.excel_analysis.projection_complete
    no_global_error = hxd.non_cds.global_fields.is_there_global_message == False
    
    if not (marked_complete and no_global_error):
        data=json.dumps({})
    else:
        data = create_dict_for_excel(hxd, rater)
    
    hxd.non_cds.excel_analysis.data_dict = data

    # Compare task data with live data to unhide download button
    task_data = hxd.non_cds.excel_analysis.task_data_dict
    hxd.non_cds.excel_analysis.show_download = True if data == task_data else False


