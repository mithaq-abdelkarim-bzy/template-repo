import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import policy_term
from operator import itemgetter
from algorithms.rate_constants import max_curves
import algorithms.rate_utilities as utils
from algorithms.timer import timer
from hx import params as hx_params

from algorithms.udf import agg_std_dev, list_to_numpy

## paramter values
table_peril_name = hx_params.table_peril_name
table_peril_name = table_peril_name.set_index("peril_label")
peril_reference =  hx_params.table_peril_name["peril_reference"]
peril_reference = [x for x in peril_reference if x != "ap"]

table_nmp_curves = hx_params.table_nmp_curves
rp_list = hx_params.table_return_periods["return_period"]

def rate_non_modelled_perils(hxd, common_data_dict):

    # set dataframe variables for cleaner code  
    cds = hxd.cds        
    non_modelled_perils = cds.non_modelled_perils
    nmp_visual = cds.non_modelled_perils_visual
    layers = cds.layers  

    # 1) Load input values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    limit = common_data_dict["limit"]

    gross_el_uw = [layer.nmp.non_modelled_perils_total.gross_el_uw for layer in layers]
    gross_sd_uw = [layer.nmp.non_modelled_perils_total.gross_sd_uw for layer in layers]

    gross_el_uw = list_to_numpy(gross_el_uw, float)
    gross_sd_uw = list_to_numpy(gross_sd_uw, float)

    non_modelled_perils_df = utils.pd_df_from_hx_list(non_modelled_perils, columns = ["curve_selections.broker_pml", "curve_selections.curve", "curve_selections.include_in_summary", "curve_selections.peril"] + [f"pml_market.rp_{item}" for item in rp_list])

    curve_count = nmp_visual.curve_number
    layer_columns_to_read = [f"nmp.non_modelled_perils_{i}.{field}" for i in range(1, curve_count + 1) for field in ["gross_el", "gross_sd", "include_curve"]]
    layer_nmp = utils.pd_df_from_hx_list(layers, columns = layer_columns_to_read)

    # 2) show/hide number of curves ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for i in range(1, curve_count + 1):
        setattr(nmp_visual, f"show_curve_{i}", True)

    # 3) Column labeling and market pml selection (non_modelled_perils) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    non_modelled_perils_df = non_modelled_perils_df.head(curve_count)
    non_modelled_perils_df.columns = [col.replace("curve_selections.", "").replace("pml_market.", "") for col in non_modelled_perils_df.columns]

    ## create market_curve_table, each row gives return period loss for curve
    rp_columns = [f"rp_{item}" for item in rp_list]
    market_curve_table = non_modelled_perils_df[[*rp_columns, "curve"]].copy()
    market_curve_table = (
        market_curve_table
        .reset_index()
        .melt(id_vars = ["index", "curve"], var_name = "rp")
        .drop(columns = "value")
    )
    market_curve_table = pd.merge(market_curve_table, table_nmp_curves, how = "left", on=["curve", "rp"])
    market_curve_table = (market_curve_table
        .pivot(index = "index", columns = "rp", values = "loss")
        .fillna(0)
    )
    market_curve_table.columns = [f"pml_market.{x}" for x in market_curve_table.columns.values]

    ## set values for "show_market_pml", "pml_market_label", "pml_broker_label"
    non_modelled_perils_df = non_modelled_perils_df.drop(columns=rp_columns)
    non_modelled_perils_df["show_market_pml"] = ~non_modelled_perils_df["broker_pml"]
    non_modelled_perils_df["pml_market_label"] = np.where(non_modelled_perils_df["broker_pml"], "Not Used", "PML - Market")
    non_modelled_perils_df["pml_broker_label"] = np.where(non_modelled_perils_df["broker_pml"], "PML - Broker", "Not Used")
    non_modelled_perils_df_to_write = non_modelled_perils_df[["show_market_pml", "pml_market_label", "pml_broker_label"]].copy()
    non_modelled_perils_df_to_write.columns = ["curve_selections." + name for name in non_modelled_perils_df_to_write.columns.values]

    ## join non_modelled_perils_df_to_write and market_curve_table
    non_modelled_perils_to_write = pd.concat([non_modelled_perils_df_to_write, market_curve_table], axis = 1)

    ## non_modelled_perils_df columns to merge later
    curve_level_df_to_merge = non_modelled_perils_df[["peril", "include_in_summary"]].copy()
    curve_level_df_to_merge["include_in_summary"] += 0
    curve_level_df_to_merge.index = range(1, curve_level_df_to_merge.shape[0] + 1)

    # 4) Aggregate NMP losses (layers) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    layer_nmp.columns = [col.replace("nmp.non_modelled_perils_", "") for col in layer_nmp.columns]
    layer_nmp = layer_nmp.reset_index()

    layer_nmp = layer_nmp.melt(id_vars = "index")
    layer_nmp["curve_index"] = layer_nmp["variable"].str.split('.').str[0]
    layer_nmp["variable"] = layer_nmp["variable"].str.split('.').str[1]
    layer_nmp = (
        layer_nmp
        .pivot(index = ["index", "curve_index"], columns = "variable", values = "value")
        .reset_index()
    )
    layer_nmp["curve_index"] = layer_nmp["curve_index"].astype("int64")
    layer_nmp["include_curve"] = layer_nmp["include_curve"].fillna(0).astype("float64")
    layer_nmp = layer_nmp.fillna(0)
    layer_nmp = pd.merge(layer_nmp, curve_level_df_to_merge, how = "left", left_on = "curve_index", right_index=True)
    layer_nmp["gross_el"] *= layer_nmp["include_curve"] * layer_nmp["include_in_summary"]
    layer_nmp["gross_sd"] *= layer_nmp["include_curve"] * layer_nmp["include_in_summary"]

    ## store peril el's to use in peril allocation
    df_peril = (layer_nmp
                .groupby(["index", "peril"], as_index=False)
                .agg({"gross_el": "sum"})
                )

    df_peril = pd.merge(df_peril, table_peril_name, how = "left", left_on = "peril", right_index=True)
    df_peril = df_peril[df_peril["peril"] != "AP"].drop(columns = ["peril"])
    df_peril["peril_reference"] = "el_" + df_peril["peril_reference"]
    df_peril = df_peril.pivot(index = "index", columns = "peril_reference", values = "gross_el")
    df_peril.columns = "nmp.non_modelled_perils_total.peril_el." + df_peril.columns.values

    ## calc el by layer for nmp
    layer_nmp = (layer_nmp
                .groupby("index")
                .agg({"gross_el": "sum", "gross_sd": agg_std_dev})
                )
    layer_nmp["limit"] = limit
    
    layer_nmp["gross_el_selected"] = np.where(gross_el_uw > 0, gross_el_uw, layer_nmp["gross_el"])
    layer_nmp["gross_sd_selected"] = np.where(gross_sd_uw > 0, gross_sd_uw, layer_nmp["gross_sd"])
    layer_nmp["loss_on_line"] = utils.ratio(layer_nmp["gross_el_selected"], layer_nmp["limit"])

    ## write to common data dict
    common_data_dict["model_nmp_gross_el"] = layer_nmp["gross_el_selected"]
    common_data_dict["model_nmp_gross_sd"] = layer_nmp["gross_sd_selected"]

    ## create dict to write to modelling tab
    model_to_write = layer_nmp[["gross_el_selected", "gross_sd_selected"]].to_dict()
    layer_nmp = layer_nmp[["gross_el", "loss_on_line", "gross_sd"]]
    layer_nmp.columns = [f"nmp.non_modelled_perils_total.{x}" for x in layer_nmp.columns.values]

    # 5) Write back to hxd ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    utils.write_pd_to_hxd(non_modelled_perils_to_write, non_modelled_perils, non_modelled_perils_to_write.columns.values)
    utils.write_pd_to_hxd(layer_nmp, layers, layer_nmp.columns.values)

    if df_peril.shape[0] > 0:
        utils.write_pd_to_hxd(df_peril, layers, df_peril.columns.values)

    for index, layer in enumerate(layers):
        layer.model.nmp.gross_el = model_to_write["gross_el_selected"][index]
        layer.model.nmp.gross_sd = model_to_write["gross_sd_selected"][index]  

    return common_data_dict
