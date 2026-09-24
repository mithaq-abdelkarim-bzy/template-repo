# v0.5.0
import hx
import pandas as pd
import numpy as np
# import math as math
import algorithms.rate_utilities as utils
from algorithms.rate_constants  import (NON_APP_UW_ADJ_MIN, NON_APP_UW_ADJ_MAX, NON_APP_DEFAULT_RATE)
# from algorithms                 import parameter_tables_schema as lib_params
# from operator                   import itemgetter
from libraries.model_profiler.algorithms.profiling_hxd_functions import time_me


def get_non_app_base_rate(hxd, df):
    path        = hxd.cds.exposure.granular.non_appearance
    genre       = path.genre
    row         = df[df['genre'] == genre]
    if row.empty:
        return NON_APP_DEFAULT_RATE
    return row['base_rate'].iat[0]

def get_non_app_num_band_members_mod(hxd, df):
    path            = hxd.cds.exposure.granular.non_appearance
    num_band_members= path.num_band_members
    row             = df[df['num_band_members'] == num_band_members]
    if row.empty:
        return 0
    return row['factor'].iat[0]


def get_non_app_claim_experience_mod(hxd, df):
    path            = hxd.cds.exposure.granular.non_appearance
    claim_experience= path.claim_experience
    row             = df[df['claim_experience'] == claim_experience]
    if row.empty:
        return 0
    return row['factor'].iat[0]


def get_first_loss_curve(df, limit, excess, deductible, excess_use, tiv, curve):

    def _na0(x):
        x = 0.0 if x is None else x
        return x.fillna(0.0) if isinstance(x, pd.Series) else np.nan_to_num(x, nan=0.0) # preserves series type if provided

    # error trap nans and nones
    deductible  = _na0(deductible)
    excess      = _na0(excess)
    limit       = _na0(limit)
    tiv         = _na0(tiv)

    # Use either excess or deductible, never both
    if isinstance(excess_use, pd.Series):
        excess_use  = excess_use.fillna(False)
        excess      = excess.where(      excess_use, 0.0)
        deductible  = deductible.where( ~excess_use, 0.0)
    else:
        excess      = excess if excess_use else 0.0
        deductible  = 0.0    if excess_use else deductible

    # determine attachment, exhaustion and curve
    attach      = utils.ratio(excess + deductible,  tiv) * 100  # note either excess or limit used not both
    exhaust     = utils.ratio(excess + limit,       tiv) * 100
    col_curve   = "salzman_b_primary" if curve == "Large" else "salzman_a_primary"

    # prepare index aligned series's from original exposure curve
    curve_x          = df["attachment"].to_numpy()
    curve_y          = df[col_curve   ].to_numpy()
    
    curve_attach_pct = np.interp(attach,  curve_x,  curve_y)
    curve_exhaust_pct= np.interp(exhaust, curve_x,  curve_y)
    curve_pct        = _na0(utils.ratio(curve_exhaust_pct - curve_attach_pct, 100))

    if isinstance(attach, pd.Series):
        curve_pct = pd.Series(curve_pct, index=attach.index).clip(0.0, 1.0)
    else:
        curve_pct = np.clip(curve_pct, 0.0, 1.0)

    return curve_pct

@time_me
def rate_exposure_non_appearance(hxd, rater):
    ###############################################################################################
    ### 1) Setting paths and derivign initial scalar values
    ###############################################################################################

    # paths
    cds         = hxd.cds 
    exposure    = hxd.cds.exposure.granular
    exposure_na = hxd.cds.exposure.granular.non_appearance
    layers      = hxd.cds.layers
    params      = hx.params

    # load layers
    layers_df   = rater.get('layers_df')
    tp_dict     = rater.get('tp_dict')

    # simple scalar
    tiv             = exposure_na.agg_show_value                # No fx conversion needed as dealing with ratios
    nmp_load        = tp_dict['nmp_load'   ]

    # getting complex scalar
    base_rate                   = get_non_app_base_rate(           hxd,  params.tbl_non_app_base_rates)
    num_band_members_mod        = get_non_app_num_band_members_mod(hxd,  params.tbl_non_app_num_band_members_mod)
    non_app_claim_experience_mod= get_non_app_claim_experience_mod(hxd,  params.tbl_non_app_claim_experience_mod)

    # uw adjustments
    sel_uw_adj = exposure_na.uw_adj_sel
    uw_adj_min = NON_APP_UW_ADJ_MIN
    uw_adj_max = NON_APP_UW_ADJ_MAX
    uw_adj_fin = float(np.clip(sel_uw_adj or 0.0, uw_adj_min, uw_adj_max))

    # basic rating
    avg_show_value  = utils.ratio(  exposure_na.agg_show_value,    exposure_na.num_shows)
    el_fgu          = (exposure_na.agg_show_value or 0) * (base_rate or 0)
    nmp_mod         = 1 + nmp_load
    total_mod       = (num_band_members_mod or 0) * (non_app_claim_experience_mod or 0) * (nmp_mod or 0)
    el_fgu_mod      = el_fgu     * total_mod
    el_fgu_mod_adj  = el_fgu_mod * (uw_adj_fin + 1)

    # layers
    num_rows = layers_df.shape[0]
    layers_df['fgu_pct'] = get_first_loss_curve(  params.tbl_non_app_loss_curves
                                                , layers_df['coverages/ec_total/limit']       # No fx conversion needed as dealing with ratios # deliberately using ec_total as this is where the limit etc is set
                                                , layers_df['coverages/ec_total/excess']      # No fx conversion needed as dealing with ratios # deliberately using ec_total as this is where the limit etc is set
                                                , layers_df['coverages/ec_total/deductible']  # No fx conversion needed as dealing with ratios # deliberately using ec_total as this is where the limit etc is set
                                                , layers_df['coverages/ec_total/excess_use']
                                                , tiv                      # No fx conversion needed as dealing with ratios
                                                , exposure_na.fl_curve)
    layers_df['description']    = [f"Layer {x}" for x in range(1, num_rows + 1)]
    layers_df['el_fgu_mod']     = (layers_df['fgu_pct'] * el_fgu_mod     ).fillna(0)
    layers_df['el_fgu_mod_adj'] = (layers_df['fgu_pct'] * el_fgu_mod_adj ).fillna(0)


    # simple processing and storing scalar to hxd
    exposure_na.fgu.description     = "FGU"
    exposure_na.fgu.el_fgu_mod      = el_fgu_mod
    exposure_na.fgu.el_fgu_mod_adj  = el_fgu_mod_adj

    exposure_na.total.description   = "Total"
    exposure_na.total.fgu_pct       = layers_df['fgu_pct'].sum()
    exposure_na.total.el_fgu_mod    = layers_df['el_fgu_mod'].sum()
    exposure_na.total.el_fgu_mod_adj= layers_df['el_fgu_mod_adj'].sum()

    exposure_na.base_rate            = base_rate
    exposure_na.avg_show_value       = avg_show_value
    exposure_na.el_fgu               = el_fgu
    exposure_na.num_band_members_mod = num_band_members_mod
    exposure_na.claim_experience_mod = non_app_claim_experience_mod
    exposure_na.nmp_mod              = nmp_mod
    exposure_na.total_mod            = total_mod
    exposure_na.el_fgu_mod           = el_fgu_mod

    exposure_na.uw_adj_min           = uw_adj_min
    exposure_na.uw_adj_max           = uw_adj_max
    exposure_na.uw_adj_fin           = uw_adj_fin        

    # agg tiv to hxd
    cds.exposure.aggregate.exposure  = cds.exposure.granular.non_appearance.agg_show_value
    
    # passing events_df to rater
    rater["layers_df"]   = layers_df        


    return rater