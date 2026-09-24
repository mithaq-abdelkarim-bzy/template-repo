import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter, attrgetter
from algorithms.rate_constants import max_curves, return_periods, sims
from algorithms.timer import timer

from algorithms.udf import generate_ymlt, generate_oep, layer_loss, kpi_calc, list_to_numpy

def rms_el_allocation(hxd, progress):
    ## set dataframe variables for cleaner code
    cds = hxd.cds 
    pml_curves = cds.pml_curves.rms_curves
    act_lvl = cds.modelling_account_level
    layers = cds.layers    

    # 1) Load input values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if cds.show_us_fields:
        index_eq = getattr(act_lvl,"rms_eq_curve_selection") or "NA"
        index_ws = getattr(act_lvl,"rms_ws_curve_selection") or "NA"        
        index_scs = getattr(act_lvl,"rms_scs_curve_selection") or "NA"

        index_list = [index_eq, index_ws,  index_scs]
    else:
        index_eu_ws = getattr(act_lvl,"rms_eu_ws_curve_selection") or "NA"
        index_jp_eq = getattr(act_lvl,"rms_jp_eq_curve_selection") or "NA"
        index_jp_ws = getattr(act_lvl,"rms_jp_ws_curve_selection") or "NA"
        index_can_eq_el = getattr(act_lvl,"rms_can_eq_curve_selection") or "NA"
        index_caribbean_el = getattr(act_lvl,"rms_caribbean_ws_curve_selection") or "NA"

        index_list = [index_eu_ws, index_jp_eq, index_jp_ws, index_can_eq_el, index_caribbean_el]

    columns_to_read = [f"rp_loss.rp_{x}" for x in return_periods]
    curve_df = utils.pd_df_from_hx_list(pml_curves, columns_to_read)

    limit = [layer.limit for layer in layers]
    excess = [layer.excess for layer in layers]
    gross_el = [layer.model.rms.gross_el for layer in layers]

    limit = list_to_numpy(limit, float)
    excess = list_to_numpy(excess, float)
    gross_el = list_to_numpy(gross_el, float)

    gross_el_df = pd.DataFrame({"layer": range(len(gross_el)), "gross_el": gross_el})

    # 2) Filter for curves ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    curve_df = curve_df.filter(regex = "rp_loss.")
    curve_df.columns = [int(col.replace("rp_loss.rp_", "")) for col in curve_df.columns]
    curve_df = (
        curve_df
        .T
        .reset_index()
        .rename(columns = {"index": "rp"})
        .sort_values("rp", ascending = False)
        .reset_index(drop = True)
    )

    curve_list = [
        pd.DataFrame(columns = ["rp", "cedant_loss"])
        if index == "NA"
        else curve_df[["rp", index - 1]]
        for index in index_list
    ]

    for curve in curve_list:
        curve.columns = ["rp", "cedant_loss"]

    # 3) calc approx el for each curve ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    result_list = [[None] * len(layers) for _ in range(len(curve_list))]

    for df, result in zip(curve_list, result_list):
        if df.shape[0] == 0:
            result = [0 for x in result]
        else: 
            ymlt = generate_ymlt(df, sims)
            for index, _ in enumerate(layers):
                ymlt[f"gross_loss_{index}"] = layer_loss(ymlt.loc[:, ["year", "cedant_loss"]],
                                                         limit[index],
                                                         excess[index],
                                                         0)                                                 
                kpi = kpi_calc(ymlt, f"gross_loss_{index}", sims)
                result[index] = kpi["el"]


    result_df = pd.DataFrame(result_list)
    result_df = result_df.fillna(0)
    # turn to long format, join on gross_el, create layer_curve_el as well for comparison
    result_df = pd.melt(result_df, value_vars=result_df.columns.tolist(), var_name = "layer", value_name="curve_el")
    result_df = pd.merge(result_df, gross_el_df, how = "left", on = "layer")
    result_df["layer_curve_el"] = result_df.groupby("layer")["curve_el"].transform("sum")

    if cds.show_us_fields:
        # scale curve_el to sum to layer el
        result_df["curve_el"] = result_df["gross_el"] * utils.ratio(result_df["curve_el"], result_df["layer_curve_el"])
    else: 
        # if sum of curve_el > layer_el scale, otherwise keep same (this is because intl. may have other perils in layer el so don't always to to allocate all el to curves)
        result_df["curve_el"] = np.where(
            result_df["layer_curve_el"] < result_df["gross_el"],
            result_df["curve_el"],
            result_df["gross_el"] * utils.ratio(result_df["curve_el"], result_df["layer_curve_el"])
        )

    result_df = result_df[["layer", "curve_el"]]

    result_df["curve"] = list(range(len(result_list))) * len(gross_el)
    result_df = result_df.pivot(index = "layer", columns = "curve", values = "curve_el")

    # 4) Write back to hxd ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if cds.show_us_fields: 
        for index, layer in enumerate(layers):
            ## order: [eq_el, ws_el, scs_el]
            layer.model.rms.eq_el = result_df[0][index]
            layer.model.rms.ws_el = result_df[1][index]
            layer.model.rms.scs_el = result_df[2][index]
    else:
        for index, layer in enumerate(layers):
            ## order: [eu_ws_el, jp_eq_el, jp_ws_el, can_eq_el, caribbean_ws_el]
            layer.model.rms.eu_ws_el = result_df[0][index]
            layer.model.rms.jp_eq_el = result_df[1][index]
            layer.model.rms.jp_ws_el = result_df[2][index]
            layer.model.rms.can_eq_el = result_df[3][index]
            layer.model.rms.caribbean_ws_el = result_df[4][index]
             