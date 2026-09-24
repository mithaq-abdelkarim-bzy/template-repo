import hx
from hx import params as hx_params
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter, attrgetter
from algorithms.rate_constants import max_curves, sims
from algorithms.timer import timer
from scipy.stats import percentileofscore

from algorithms.udf import generate_ymlt, layer_loss, kpi_calc, list_to_numpy

def peril_allocation(hxd, progress):
    ## set dataframe variables for cleaner code
    cds = hxd.cds
    layers = cds.layers
    pml_curves = cds.curve_aggregator.pml_selections

    ## paramter values
    peril_label_all =  hx_params.table_peril_name["peril_label"]
    peril_label = [x for x in peril_label_all if x != "AP"]
    peril_reference_all =  hx_params.table_peril_name["peril_reference"]
    peril_reference = [x for x in peril_reference_all if x != "ap"]

    field_names = [f"el_{x}" for x in peril_reference]

    rp_attach_field_names = ["rms_ap", "rms_eq", "rms_ws", "rms_scs", "air_ap", "air_eq", "air_ws", "air_scs", "air_winter", "air_wf"]

    # 1) Load input values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    include_ivor = cds.peril_allocation_account_level.include_ivor
    allocation_methodology = cds.peril_allocation_account_level.allocation_methodology

    nmp_layer_el = utils.pd_df_from_hx_list(layers, [f"nmp.non_modelled_perils_total.peril_el.{el_name}" for el_name in field_names])
    layer_peril_df = utils.pd_df_from_hx_list(layers, [f"peril_allocation.{model}.{el_name}" for model in ["rms_aal", "air_aal", "ivor_aal"]  for el_name in field_names])

    ## rms modelling ws/eq/scs el
    model_pml_eq_el = [layer.model.rms.eq_el for layer in layers]
    model_pml_ws_el = [layer.model.rms.ws_el for layer in layers]
    model_pml_scs_el = [layer.model.rms.scs_el for layer in layers]

    ## weightings
    weighting_rms = [layer.quote.rol_ty.weighting_rms for layer in layers]
    weighting_ivor = [layer.quote.rol_ty.weighting_ivor for layer in layers]
    weighting_air = [layer.quote.rol_ty.weighting_air for layer in layers]
    weighting_burn = [layer.quote.rol_ty.weighting_burn for layer in layers]

    ## layer info
    limit_cnv = [layer.limit_cnv for layer in layers]
    excess_cnv = [layer.excess_cnv for layer in layers]


    model_pml_eq_el = list_to_numpy(model_pml_eq_el, float)
    model_pml_ws_el = list_to_numpy(model_pml_ws_el, float)
    model_pml_scs_el = list_to_numpy(model_pml_scs_el, float)

    weighting_rms = list_to_numpy(weighting_rms, data_type = float)
    weighting_ivor = list_to_numpy(weighting_ivor, data_type = float)
    weighting_air = list_to_numpy(weighting_air, data_type = float)
    weighting_burn = list_to_numpy(weighting_burn, data_type = float)

    limit_cnv = list_to_numpy(limit_cnv, data_type = float)
    excess_cnv = list_to_numpy(excess_cnv, data_type = float)

    # 2) Pull and filter PML curves ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    curve_df = utils.pd_df_from_hx_list(pml_curves)
    ## filter out NMP as already importing el from NMP tab
    curve_df = curve_df[~curve_df["name"].str.contains("NMP", case = False)]
    ## pull curve names
    curve_names = list(curve_df["name"])
    curve_names = [f"{name}_{index}" for index, name in enumerate(curve_names)]
    ## transform df into columns of the OEP curves
    curve_df = curve_df.filter(regex = "rp_loss/")
    curve_df.columns = [int(col.replace("rp_loss/rp_", "")) for col in curve_df.columns]
    curve_df = (
        curve_df
        .T
        .reset_index()
        .rename(columns = {"index": "rp"})
        .sort_values("rp", ascending = False)
        .reset_index(drop = True)
        .fillna(0)
    )
    curve_df.columns = ["rp"] + curve_names

    # 3) Cycle though each curve and calculate EL for each layer and attach / exit points ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    pml_model = [None] * len(curve_names)
    pml_peril = [None] * len(curve_names)
    pml_layer_el = [None] * len(curve_names)
    rp_attach = [None] * len(curve_names)
    rp_exit = [None] * len(curve_names)

    for index, name in enumerate(curve_names):
        ## The peril sits between the first two white spaces, add a trailing white space to ensure
        ## NOTE: dont think trailing white space needed
        model_temp = (name + " ").split(" ")[0]
        peril_temp = (name + " ").split(" ")[1]

        curve_temp = curve_df[["rp", name]].copy()
        curve_temp.columns = ["rp", "cedant_loss"]
        ymlt = generate_ymlt(curve_temp, sims)

        el = [None] * len(layers)

        ## attach / exit point
        percentile_attach = percentileofscore(ymlt["cedant_loss"], excess_cnv) / 100
        percentile_exit = percentileofscore(ymlt["cedant_loss"], excess_cnv + limit_cnv) / 100

        rp_attach_temp = np.where(percentile_attach > 0, 1 / (1 - percentile_attach), 0)
        rp_attach_temp[rp_attach_temp == np.inf] = 10000
        rp_exit_temp = np.where(percentile_attach > 0, 1 / (1 - percentile_exit), 0)
        rp_exit_temp[rp_exit_temp == np.inf] = 10000

        rp_attach[index] = rp_attach_temp
        rp_exit[index] = rp_exit_temp

        ## el
        for j, _ in enumerate(layers):
            ymlt[f"gross_loss_{j}"] = layer_loss(ymlt.loc[:, ["year", "cedant_loss"]],
                                                 limit_cnv[j],
                                                 excess_cnv[j],
                                                 0)                                                 
            kpi = kpi_calc(ymlt, f"gross_loss_{j}", sims)

            el[j] = kpi["el"]

        pml_model[index] = model_temp
        pml_peril[index] = peril_temp
        pml_layer_el[index] = el

    pml_layer_el = pd.DataFrame(pml_layer_el)
    pml_layer_el["model"] = pml_model
    pml_layer_el["peril"] = pml_peril
    # outer join on all model_peril combos to ensure nothing missed
    expected_combos = pd.DataFrame({
        "model": ["RMS"] * len(peril_label_all) + ["AIR"] * len(peril_label_all),
        "peril": np.tile(peril_label_all,2),
        })
    pml_layer_el = expected_combos.merge(pml_layer_el, on =["model", "peril"], how = "left")
    pml_layer_el = pml_layer_el.melt(id_vars = ["model", "peril"], var_name = "layer", value_name = "el")

    # 4) Populate attach and exit points ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## RMS
    rms_pml_peril = [x for x, y in zip(pml_peril, pml_model) if y == "RMS"]
    rms_attach = [x for x, y in zip(rp_attach, pml_model) if y == "RMS"]
    rms_exit = [x for x, y in zip(rp_exit, pml_model) if y == "RMS"]

    rms_ap_valid = len([x for x in rms_pml_peril if x == "AP"])
    rms_eq_valid = len([x for x in rms_pml_peril if x == "EQ"])
    rms_ws_valid = len([x for x in rms_pml_peril if x == "WS"])
    rms_scs_valid = len([x for x in rms_pml_peril if x == "SCS"])

    if len(rms_pml_peril) > 0:
        for i, layer in enumerate(layers):
            if rms_ap_valid > 0:
                layer.quote.rol_ty.rms_ap_attach = rms_attach[rms_pml_peril.index("AP")][i]
                layer.quote.rol_ty.rms_ap_exit = rms_exit[rms_pml_peril.index("AP")][i]
            if rms_eq_valid > 0:
                layer.quote.rol_ty.rms_eq_attach = rms_attach[rms_pml_peril.index("EQ")][i]
                layer.quote.rol_ty.rms_eq_exit = rms_exit[rms_pml_peril.index("EQ")][i]
            if rms_ws_valid > 0:
                layer.quote.rol_ty.rms_ws_attach = rms_attach[rms_pml_peril.index("WS")][i]
                layer.quote.rol_ty.rms_ws_exit = rms_exit[rms_pml_peril.index("WS")][i]
            if rms_scs_valid > 0:
                layer.quote.rol_ty.rms_scs_attach = rms_attach[rms_pml_peril.index("SCS")][i]
                layer.quote.rol_ty.rms_scs_exit = rms_exit[rms_pml_peril.index("SCS")][i]

    ## AIR
    air_pml_peril = [x for x, y in zip(pml_peril, pml_model) if y == "AIR"]
    air_attach = [x for x, y in zip(rp_attach, pml_model) if y == "AIR"]
    air_exit = [x for x, y in zip(rp_exit, pml_model) if y == "AIR"]

    air_ap_valid = len([x for x in air_pml_peril if x == "AP"])
    air_eq_valid = len([x for x in air_pml_peril if x == "EQ"])
    air_ws_valid = len([x for x in air_pml_peril if x == "WS"])
    air_scs_valid = len([x for x in air_pml_peril if x == "SCS"])
    air_winter_valid = len([x for x in air_pml_peril if x == "Winter"])
    air_wf_valid = len([x for x in air_pml_peril if x == "WF"])

    if len(air_pml_peril) > 0:
        for i, layer in enumerate(layers):
            if air_ap_valid > 0:
                layer.quote.rol_ty.air_ap_attach = air_attach[air_pml_peril.index("AP")][i]
                layer.quote.rol_ty.air_ap_exit = air_exit[air_pml_peril.index("AP")][i]
            if air_eq_valid > 0:
                layer.quote.rol_ty.air_eq_attach = air_attach[air_pml_peril.index("EQ")][i]
                layer.quote.rol_ty.air_eq_exit = air_exit[air_pml_peril.index("EQ")][i]
            if air_ws_valid > 0:
                layer.quote.rol_ty.air_ws_attach = air_attach[air_pml_peril.index("WS")][i]
                layer.quote.rol_ty.air_ws_exit = air_exit[air_pml_peril.index("WS")][i]
            if air_scs_valid > 0:
                layer.quote.rol_ty.air_scs_attach = air_attach[air_pml_peril.index("SCS")][i]
                layer.quote.rol_ty.air_scs_exit = air_exit[air_pml_peril.index("SCS")][i]
            if air_winter_valid > 0:
                layer.quote.rol_ty.air_winter_attach = air_attach[air_pml_peril.index("Winter")][i]
                layer.quote.rol_ty.air_winter_exit = air_exit[air_pml_peril.index("Winter")][i]
            if air_wf_valid > 0:
                layer.quote.rol_ty.air_wf_attach = air_attach[air_pml_peril.index("WF")][i]
                layer.quote.rol_ty.air_wf_exit = air_exit[air_pml_peril.index("WF")][i]

    # 5) Peril allocation calculations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    nmp_layer_el.columns = [col.replace("nmp.non_modelled_perils_total.peril_el.", "nmp.") for col in nmp_layer_el.columns]
    layer_peril_df.columns = [col.replace("peril_allocation.", "") for col in layer_peril_df.columns]

    layer_peril_df = pd.concat([layer_peril_df, nmp_layer_el], axis=1)
    layer_peril_df = layer_peril_df.reset_index()
    layer_peril_df = layer_peril_df.melt(id_vars = "index", var_name = "peril", value_name = "el")
    layer_peril_df["model"] = layer_peril_df["peril"].str.split('.').str[0]
    layer_peril_df["peril"] = layer_peril_df["peril"].str.split('.').str[1]
    layer_peril_df = layer_peril_df.rename(columns = {"index": "layer"})

    ## filter out AP from pml approx calcs
    pml_layer_el = pml_layer_el[pml_layer_el["peril"] != "AP"]
    pml_layer_el["peril"] = "el_" + pml_layer_el["peril"].str.lower()
    pml_layer_el["model"] = pml_layer_el["model"].str.lower() + "_pml"

    ## replace approx rms eq,ws,scs el with el derived from rms_el_allocation task for consistency
    if model_pml_eq_el.sum() > 0:
        pml_layer_el.loc[(pml_layer_el["model"] == "rms_pml") & (pml_layer_el["peril"] == "el_eq"), "el"] = model_pml_eq_el
    if model_pml_ws_el.sum() > 0:
        pml_layer_el.loc[(pml_layer_el["model"] == "rms_pml") & (pml_layer_el["peril"] == "el_ws"), "el"] = model_pml_ws_el
    if model_pml_scs_el.sum() > 0:
        pml_layer_el.loc[(pml_layer_el["model"] == "rms_pml") & (pml_layer_el["peril"] == "el_scs"), "el"] = model_pml_scs_el

    layer_peril_df = pd.concat([layer_peril_df, pml_layer_el], axis = 0, ignore_index=True)
    layer_peril_df = layer_peril_df.fillna(0)

    layer_peril_df = layer_peril_df.groupby(["model", "layer", "peril"], as_index = False).agg(
        el = ("el", "sum")
    )
    ## create rms/air el_approx to populate hxd later (ensure consistency with rms_el_allocation)
    rms_el_approx = (
        layer_peril_df[layer_peril_df["model"] == "rms_pml"]
        .pivot(index = "layer", columns = "peril", values ="el")
        .to_dict(orient = "records")
        )
    air_el_approx = (
        layer_peril_df[layer_peril_df["model"] == "air_pml"]
        .pivot(index = "layer", columns = "peril", values ="el")
        .to_dict(orient = "records")
        )
                
    # 6) Calculate peril weighting ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if allocation_methodology == "PML":
        layer_peril_df = layer_peril_df[~layer_peril_df["model"].isin(["rms_aal", "air_aal"])]
    else:
        layer_peril_df = layer_peril_df[~layer_peril_df["model"].isin(["rms_pml", "air_pml"])]

    if include_ivor == "No":
        weighting_ivor[:] = 0

    total_weight = weighting_rms + weighting_air + weighting_ivor
    weighting_rms = utils.ratio(weighting_rms, total_weight)
    weighting_air = utils.ratio(weighting_air, total_weight)
    weighting_ivor = utils.ratio(weighting_ivor, total_weight)

    ## if no weighting applied, set to rms to 100%
    weighting_rms = np.where(total_weight == 0, 1, weighting_rms)

    ## create weighting df
    weighting_df = pd.DataFrame({
        "layer": range(len(layers)),
        "rms_pml": weighting_rms,
        "rms_aal": weighting_rms,
        "air_pml": weighting_air,
        "air_aal": weighting_air,
        "ivor_aal": weighting_ivor,
        "nmp": 1
    })

    weighting_df = weighting_df.melt(id_vars = ["layer"], var_name = "model", value_name = "weight")
    layer_peril_df = pd.merge(layer_peril_df, weighting_df, on = ["layer", "model"], how = "left")
    layer_peril_df["weighted_el"] = layer_peril_df["el"] * layer_peril_df["weight"]

    layer_peril_df = layer_peril_df.groupby(["layer", "peril"], as_index = False).agg(
        el = ("weighted_el", "sum")
    )
    layer_peril_df["layer_el"] = layer_peril_df.groupby(["layer"], as_index = False)["el"].transform("sum")
    layer_peril_df["final_proportions"] = utils.ratio(layer_peril_df["el"], layer_peril_df["layer_el"])

    final_proportions = (
        layer_peril_df
        .pivot(index = "layer", columns = "peril", values ="final_proportions")
        .to_dict(orient = "records")
        )

    # 7) write back to hxd ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for index, layer in enumerate(layers):
        layer.peril_allocation.rms_el_approx = rms_el_approx[index]
        layer.peril_allocation.air_el_approx = air_el_approx[index]
        layer.peril_allocation.final_proportions = final_proportions[index]

    cds.send_rate_change.peril_allocation_run = True
