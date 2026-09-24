import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter, attrgetter
from algorithms.rate_constants import max_curves, sims
from algorithms.timer import timer

from algorithms.udf import generate_ymlt, generate_oep, layer_loss, kpi_calc, list_to_numpy, ccy_conversion


def nmp_calc(hxd, progress):
    ## set dataframe variables for cleaner code  
    cds = hxd.cds        
    non_modelled_perils = cds.non_modelled_perils
    layers = cds.layers
    params = hx.params

    # 1) Load input values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    application_ccy = cds.currency

    limit = [layer.limit for layer in layers]
    excess = [layer.excess for layer in layers]
    layer_ccy = [layer.currency for layer in layers]
    layer_ccy = [x if x is not None else application_ccy for x in layer_ccy]

    limit = list_to_numpy(limit, float)
    excess = list_to_numpy(excess, float)

    curve_list = [None] * cds.non_modelled_perils_visual.curve_number
    include_in_summary_list = [None] * cds.non_modelled_perils_visual.curve_number
    peril_list = [None] * cds.non_modelled_perils_visual.curve_number
    currency_list = [None] * cds.non_modelled_perils_visual.curve_number

    # 2) Loop through each nmp curve ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for index, element in enumerate(range(cds.non_modelled_perils_visual.curve_number), start = 0):
        
        rebase_rp = non_modelled_perils[index].curve_selections.rp
        rebase_loss = non_modelled_perils[index].curve_selections.loss
        include_in_summary = non_modelled_perils[index].curve_selections.include_in_summary
        peril = non_modelled_perils[index].curve_selections.peril
        currency = non_modelled_perils[index].curve_selections.currency

        if non_modelled_perils[index].curve_selections.broker_pml:
            rp_values = [getattr(non_modelled_perils[index].pml_broker, f"rp_{i}") for i in hx.params.table_return_periods["return_period"]]
        else:
            rp_values = [getattr(non_modelled_perils[index].pml_market ,f"rp_{i}") for i in hx.params.table_return_periods["return_period"]]

        rp_values = pd.Series(rp_values)
        pml_temp = pd.DataFrame({"rp": hx.params.table_return_periods["return_period"], "cedant_loss": rp_values})

        # 3) Extrapolate for low and high RPs to fill out curve ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        ## extrapolate for RP 5 and 2 where blank (rare)
        if pd.isnull(pml_temp.loc[pml_temp["rp"] == 5, "cedant_loss"].iloc[0]):
            gradient = (pml_temp.loc[pml_temp["rp"] == 25, "cedant_loss"].iloc[0] - pml_temp.loc[pml_temp["rp"] == 10, "cedant_loss"].iloc[0]) / (25 - 10)
            intercept = pml_temp.loc[pml_temp["rp"] == 10, "cedant_loss"].iloc[0] - 10 * gradient
            pml_temp["cedant_loss"] = np.where(pml_temp["rp"].isin([2, 5]), np.maximum(pml_temp["rp"] * gradient + intercept, 0), pml_temp["cedant_loss"])

        ## extrapolate for RP 2 where necassary
        pml_temp["cedant_loss_extrap_below"] = (pml_temp["cedant_loss"].shift(-1) / pml_temp["cedant_loss"].shift(-2)) * pml_temp["cedant_loss"].shift(-1)
        if non_modelled_perils[index].curve_selections.broker_pml:
            pml_temp["cedant_loss"] = np.where(pd.isnull(pml_temp["cedant_loss"]), pml_temp["cedant_loss_extrap_below"], pml_temp["cedant_loss"])
        else:
            pml_temp["cedant_loss"] = np.where(pml_temp["cedant_loss"] == 0, pml_temp["cedant_loss_extrap_below"], pml_temp["cedant_loss"])

        ## extrapolate for high RPs
        ## repeat twice to fill in RP 10000 and 5000 
        for x in range(2):
            pml_temp["cedant_loss_extrap_above"] =  (
                                                        (
                                                            (
                                                            ((pml_temp["cedant_loss"].shift(1) / pml_temp["cedant_loss"].shift(2) - 1) / (pml_temp["rp"].shift(1) - pml_temp["rp"].shift(2)))
                                                            / ((pml_temp["cedant_loss"].shift(2) / pml_temp["cedant_loss"].shift(3) - 1) / (pml_temp["rp"].shift(2) - pml_temp["rp"].shift(3)))
                                                            ) 
                                                            * ((pml_temp["cedant_loss"].shift(1) / pml_temp["cedant_loss"].shift(2) - 1) / (pml_temp["rp"].shift(1) - pml_temp["rp"].shift(2)))
                                                            * (pml_temp["rp"] - pml_temp["rp"].shift(1))
                                                            + 1
                                                        )
                                                    * pml_temp["cedant_loss"].shift(1)
                                                    )

            pml_temp["cedant_loss"] = np.where(pd.isnull(pml_temp["cedant_loss"]) | ((pml_temp["cedant_loss"] == 0) & (pml_temp["rp"] >= 5000)), pml_temp["cedant_loss_extrap_above"], pml_temp["cedant_loss"])

        pml_temp = pml_temp.drop(columns=["cedant_loss_extrap_below", "cedant_loss_extrap_above"])

        # 4) Generalte YMLT and rebase ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ymlt = generate_ymlt(pml_temp, sims)

        if rebase_rp is not None and rebase_loss is not None:
            temp_rp_loss = np.quantile(ymlt["cedant_loss"], 1 - 1 / rebase_rp)
            rebase_factor = rebase_loss / temp_rp_loss
            ymlt["cedant_loss"] = ymlt["cedant_loss"] * rebase_factor

        ## write back scaled pml (or not) to pml final
        rp_array = np.array(hx.params.table_return_periods["return_period"])
        rp_array = np.sort(rp_array)[::-1]
        oep_curve = generate_oep(ymlt, "cedant_loss", sims, rp_array)

        for i in np.sort(hx.params.table_return_periods["return_period"])[::-1]:
            loss = oep_curve.loc[oep_curve["rp"] == i, "loss"].iloc[0]
            setattr(non_modelled_perils[index].pml_final, f"rp_{i}", loss)

        # 5) Calculate el, lol and sd for each layer under curve ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for i, layer in enumerate(layers, start = 1):
            ## currency conversion factor, if blank default curve to application currency
            if currency is not None:
                curve_to_layer_fx_mult = ccy_conversion(currency, layer_ccy[i - 1], params.table_currency)
            else:
                curve_to_layer_fx_mult = ccy_conversion(application_ccy, layer_ccy[i - 1], params.table_currency)

            ymlt["cedant_loss_cnv"] = ymlt["cedant_loss"] * curve_to_layer_fx_mult

            ymlt[f"gross_loss_{i}"] = layer_loss(ymlt.loc[:, ["year", "cedant_loss_cnv"]],
                                                 limit[i - 1],
                                                 excess[i - 1],
                                                 0)                                                 
            kpi = kpi_calc(ymlt, f"gross_loss_{i}", sims)

            setattr(getattr(layer.nmp,f"non_modelled_perils_{index + 1}"), "gross_el", kpi["el"])
            setattr(getattr(layer.nmp,f"non_modelled_perils_{index + 1}"), "loss_on_line", utils.ratio(kpi["el"], limit[i - 1]))
            setattr(getattr(layer.nmp,f"non_modelled_perils_{index + 1}"), "gross_sd", kpi["sd"])

        oep_curve = oep_curve.sort_values("rp",ascending = False).reset_index(drop = True)
        oep_curve = oep_curve.set_index("rp")
        curve_list[index] = oep_curve
        include_in_summary_list[index] = "Yes" if include_in_summary else "No"
        peril_list[index] = peril
        currency_list[index] = currency

    all_curves = pd.concat(curve_list, axis = 1)
    all_curves.columns = range(all_curves.shape[1])

    # 6) read ly curve to write back otherwise it gets wiped ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    rp_list = [f"rp_{x}" for x in [2, 5, 10, 25, 50, 100, 200, 250, 500, 1000, 5000, 10000]]

    rp_loss_prev = [None] * len(cds.pml_curves.nmp_curves)

    for index, curves in enumerate(cds.pml_curves.nmp_curves):
        rp_loss_prev[index] = [getattr(curves.rp_loss_prev, x) for x in rp_list]

    rp_loss_prev = pd.DataFrame(rp_loss_prev).T
    rp_loss_prev = rp_loss_prev.fillna(0)
    rp_loss_prev.index = [2, 5, 10, 25, 50, 100, 200, 250, 500, 1000, 5000, 10000]

    ## expand list if differing number of columns
    ### nmp_calc_columns
    ty_cols = all_curves.shape[1]
    ly_cols = rp_loss_prev.shape[1]
    no_cols = max(ty_cols, ly_cols)

    include_in_summary_list_to_write = [None] * no_cols
    peril_list_to_write = [None] * no_cols
    currency_list_to_write = [None] * no_cols

    include_in_summary_list_to_write = [include_in_summary_list[index] if index < ty_cols else "" for index in range(no_cols)]
    peril_list_to_write = [peril_list[index] if index < ty_cols else "" for index in range(no_cols)]
    currency_list_to_write = [currency_list[index] if index < ty_cols else "" for index in range(no_cols)]

    if ty_cols < no_cols:
        diff = no_cols - ty_cols
        blank_col = np.zeros(len(rp_list))

        for i in range(ty_cols, ty_cols + diff):
            all_curves["temp"] = blank_col
            all_curves = all_curves.rename(columns = {"temp": i})
    elif ly_cols < no_cols:
        diff = no_cols - ly_cols
        blank_col = np.zeros(len(rp_list))

        for i in range(ly_cols, ly_cols + diff):
            rp_loss_prev["temp"] = blank_col
            rp_loss_prev = rp_loss_prev.rename(columns = {"temp": i})


    # 7) write back to hxd ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    to_write = [{
        "include_in_peril_alloc": include_in_summary_list_to_write[i],
        "peril": peril_list_to_write[i],
        "currency": currency_list_to_write[i],
        "rp_loss": {
            "rp_2": all_curves.at[2, i],
            "rp_5": all_curves.at[5, i],
            "rp_10": all_curves.at[10, i],
            "rp_25": all_curves.at[25, i],
            "rp_50": all_curves.at[50, i],
            "rp_100": all_curves.at[100, i],
            "rp_200": all_curves.at[200, i],
            "rp_250": all_curves.at[250, i],
            "rp_500": all_curves.at[500, i],
            "rp_1000": all_curves.at[1000, i],
            "rp_5000": all_curves.at[5000, i],
            "rp_10000": all_curves.at[10000, i]
            },
        "rp_loss_prev": {
            "rp_2": rp_loss_prev.at[2, i],
            "rp_5": rp_loss_prev.at[5, i],
            "rp_10": rp_loss_prev.at[10, i],
            "rp_25": rp_loss_prev.at[25, i],
            "rp_50": rp_loss_prev.at[50, i],
            "rp_100": rp_loss_prev.at[100, i],
            "rp_200": rp_loss_prev.at[200, i],
            "rp_250": rp_loss_prev.at[250, i],
            "rp_500": rp_loss_prev.at[500, i],
            "rp_1000": rp_loss_prev.at[1000, i],
            "rp_5000": rp_loss_prev.at[5000, i],
            "rp_10000": rp_loss_prev.at[10000, i]
            }
    } for i in range(all_curves.shape[1])
    ]

    cds.pml_curves.nmp_curves = to_write
