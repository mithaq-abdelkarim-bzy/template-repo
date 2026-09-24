import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter, attrgetter
from algorithms.rate_constants import max_curves, sims
from algorithms.timer import timer
from hx import params as hx_params
from scipy.stats import gmean
from algorithms.udf import generate_ymlt, generate_oep, layer_loss, kpi_calc, list_to_numpy, net_el_func, reins_approx

def rate_change(hxd, progress):
    ## set dataframe variables for cleaner code
    cds = hxd.cds 
    agg_output = cds.curve_aggregator.aggregator_output.rp_loss
    exp_change = cds.exposure.aggregate.perc_change
    layers = cds.layers    

    # 1) Load parameter table values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    reins_cov_table = hx_params.table_reins_cov
    reins_cov_table = reins_cov_table.set_index("parameter")
    tp_params_table = hx_params.table_tp_params
    tp_params_table = tp_params_table.set_index("item")
    bs_load = tp_params_table.at["black_swan", "load"]

    curve_rp = hx_params.table_return_periods["return_period"]

    # 2) Load input values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    programme = cds.programme
    expiring_layer_to_use = [layer.rate_change.expiring_layer_to_use - 1 for layer in layers]
    
    curve_losses = [getattr(agg_output,f"rp_{rp}") for rp in curve_rp]

    ## exposure info
    exposure_increase = [layer.rate_change.exposure_increase for layer in layers]

    ## ty layer information
    renewal_layer = [layer.renewal_layer for layer in layers]
    limit_cnv = [layer.limit_cnv for layer in layers]
    excess_cnv = [layer.excess_cnv for layer in layers]
    aggregate_deductible_cnv = [layer.aggregate_deductible_cnv for layer in layers]
    number_reins = [layer.number_reins for layer in layers]
    perc_reins_1 = [layer.perc_reins_1 or 0 for layer in layers]
    perc_reins_2 = [layer.perc_reins_2 or 0 for layer in layers]
    perc_reins_3 = [layer.perc_reins_3 or 0 for layer in layers]

    gross_lol_weighted = [layer.quote.rol_ty.gross_lol_weighted for layer in layers]

    roev = [layer.quote.rol_ty.roev for layer in layers]
    layer_exposure = [layer.quote.rol_ty.layer_exposure for layer in layers]
    bpi = [layer.quote.rol_ty.bpi for layer in layers]
    rol_fot = [layer.quote.rol_ly.rol_fot for layer in layers]

    ## ly layer information
    limit_cnv_ly = [layer.limit_cnv_ly for layer in layers]
    excess_cnv_ly = [layer.excess_cnv_ly for layer in layers]
    aggregate_deductible_cnv_ly = [layer.aggregate_deductible_cnv_ly for layer in layers]
    number_reins_ly = [layer.number_reins_ly for layer in layers]
    perc_reins_1_ly = [layer.perc_reins_1_ly or 0 for layer in layers]
    perc_reins_2_ly = [layer.perc_reins_2_ly or 0 for layer in layers]
    perc_reins_3_ly = [layer.perc_reins_3_ly or 0 for layer in layers]

    gross_lol_weighted_ly = [layer.quote.rol_ly.gross_lol_weighted for layer in layers]

    roev_ly = [layer.quote.rol_ly.roev for layer in layers]
    layer_exposure_ly = [layer.quote.rol_ly.layer_exposure for layer in layers]
    bpi_ly = [layer.quote.rol_ly.bpi for layer in layers]
    rol_fot_ly = [layer.quote.rol_ly.rol_fot for layer in layers]

    # convert to arrays and turn NAN to 0  
    curve_rp = list_to_numpy(curve_rp, int)
    curve_losses = list_to_numpy(curve_losses, float)

    exposure_increase = list_to_numpy(exposure_increase, float)

    ## ty
    limit_cnv = list_to_numpy(limit_cnv, float)
    excess_cnv = list_to_numpy(excess_cnv, float)
    aggregate_deductible_cnv = list_to_numpy(aggregate_deductible_cnv, float)
    number_reins = list_to_numpy(number_reins, int)
    perc_reins_1 = list_to_numpy(perc_reins_1, float)
    perc_reins_2 = list_to_numpy(perc_reins_2, float)
    perc_reins_3 = list_to_numpy(perc_reins_3, float)
    reins_perc = [[perc_reins_1[i], perc_reins_2[i], perc_reins_3[i]] for i in range(len(layers))]

    gross_lol_weighted = list_to_numpy(gross_lol_weighted, float)

    roev = list_to_numpy(roev, float)
    layer_exposure = list_to_numpy(layer_exposure, float)
    bpi = list_to_numpy(bpi, float)
    rol_fot = list_to_numpy(rol_fot, float)

    ## ly
    limit_cnv_ly = list_to_numpy(limit_cnv_ly, float)
    excess_cnv_ly = list_to_numpy(excess_cnv_ly, float)
    aggregate_deductible_cnv_ly = list_to_numpy(aggregate_deductible_cnv_ly, float)
    number_reins_ly = list_to_numpy(number_reins_ly, int)
    perc_reins_1_ly = list_to_numpy(perc_reins_1_ly, float)
    perc_reins_2_ly = list_to_numpy(perc_reins_2_ly, float)
    perc_reins_3_ly = list_to_numpy(perc_reins_3_ly, float)
    reins_perc_ly = [[perc_reins_1_ly[i], perc_reins_2_ly[i], perc_reins_3_ly[i]] for i in range(len(layers))]

    gross_lol_weighted_ly = list_to_numpy(gross_lol_weighted_ly, float)

    roev_ly = list_to_numpy(roev_ly, float)
    layer_exposure_ly = list_to_numpy(layer_exposure_ly, float)
    bpi_ly = list_to_numpy(bpi_ly, float)
    rol_fot_ly = list_to_numpy(rol_fot_ly, float)

    ## re-order all ly data
    limit_cnv_ly =  limit_cnv_ly[expiring_layer_to_use]
    excess_cnv_ly = excess_cnv_ly[expiring_layer_to_use]
    aggregate_deductible_cnv_ly = aggregate_deductible_cnv_ly[expiring_layer_to_use]
    number_reins_ly = number_reins_ly[expiring_layer_to_use]
    gross_lol_weighted_ly = gross_lol_weighted_ly[expiring_layer_to_use]

    reins_perc_ly = [reins_perc_ly[i] for i in expiring_layer_to_use]

    ## TODO: easy dugugging start
    # limit_cnv_ly = np.array([45e6, 75e6, 65e6, 115e6, 100e6, 175e6, 0, 351196698])
    # excess_cnv_ly = np.array([15e6, 60e6, 135e6, 200e6, 465e6, 565e6, 0, 178195245])
    # gross_lol_weighted_ly = gross_lol_weighted / 1.1
    # number_reins_ly = number_reins.copy()
    # reins_perc_ly = reins_perc.copy()

    ## TODO: easy debugging end

    if cds.programme == "Risk XL":

        if cds.rate_change.risk_xl_exposure_selection == "ROEV":
            exposure_factor = 1 + utils.ratio(layer_exposure - layer_exposure_ly, layer_exposure_ly)
        else:
            bp = utils.ratio(rol_fot, bpi)
            bp_ly = utils.ratio(rol_fot_ly, bpi_ly)

            exposure_factor = 1 + utils.ratio(bp - bp_ly, bp_ly)
        
        total_limit_factor = np.ones(len(roev))

    else:

        if cds.show_other_programme_rate_change:

            ## Limits and Retentions Factor - if excess is zero, use square root.
            geomean_ty = np.where(excess_cnv == 0, np.sqrt(limit_cnv), gmean([excess_cnv, excess_cnv + limit_cnv]))
            geomean_ly = np.where(excess_cnv_ly == 0, np.sqrt(limit_cnv_ly), gmean([excess_cnv_ly, excess_cnv_ly + limit_cnv_ly]))

            limit_excess_factor = utils.ratio(geomean_ly, geomean_ty) ## ly / ty, we're thinking in terms of rol not $ amount

            ## aad / reins
            if cds.programme == "Workers Comp":
                sd_list = [None] * len(gross_lol_weighted)
                sd_list = [0 for x in sd_list]

                net_results_ty = net_el_func(True, [gross_lol_weighted * limit_cnv], [sd_list], limit_cnv, aggregate_deductible_cnv, number_reins, reins_perc, reins_cov_table, 0, bs_load, 1, cds.show_cat_work_comp_input)
                afb_net_el_ty = net_results_ty[8][0]

                net_results_ly = net_el_func(True, [gross_lol_weighted * limit_cnv], [sd_list], limit_cnv, aggregate_deductible_cnv_ly, number_reins_ly, reins_perc_ly, reins_cov_table, 0, bs_load, 1, cds.show_cat_work_comp_input)
                afb_net_el_ly = net_results_ly[8][0]

                rc_aad_net_lol_ty = utils.ratio(afb_net_el_ty, limit_cnv)
                rc_aad_net_lol_ly = utils.ratio(afb_net_el_ly, limit_cnv)

                ## adjust for where ly not populate (using limit = 0)
                rc_aad_net_lol_ly = np.where(limit_cnv_ly == 0, rc_aad_net_lol_ty, 0)

                aad_reins_factor = utils.ratio(rc_aad_net_lol_ty - rc_aad_net_lol_ly, rc_aad_net_lol_ly)
            else:
                aad_reins_factor = 0

            ## total limit factor
            total_limit_factor = (limit_excess_factor) * (1 + aad_reins_factor)

            ## exposure
            exposure_factor = exposure_increase

        else:

            # 3) ymlt calcs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            curve_df = pd.DataFrame({"rp": curve_rp, "cedant_loss": curve_losses})
            ymlt = generate_ymlt(curve_df, sims)

            el_ty_limit_ty_exposure = [None] * len(layers)
            el_ly_limit_ty_exposure = [None] * len(layers)
            el_ly_limit_ly_exposure = [None] * len(layers)

            for index, layer in enumerate(layers):
                ymlt_ly_exposure = ymlt.copy()
                ymlt_ly_exposure["cedant_loss"] = utils.ratio(ymlt_ly_exposure["cedant_loss"], exposure_increase[index])

                ymlt[f"gross_loss_ty_limit_ty_exposure_{index}"] = layer_loss(ymlt.loc[:, ["year", "cedant_loss"]],
                                                                            limit_cnv[index],
                                                                            excess_cnv[index],
                                                                            0)  

                ymlt[f"gross_loss_ly_limit_ty_exposure_{index}"] = layer_loss(ymlt.loc[:, ["year", "cedant_loss"]],
                                                                            limit_cnv_ly[index],
                                                                            excess_cnv_ly[index],
                                                                            0)  

                ymlt[f"gross_loss_ly_limit_ly_exposure_{index}"] = layer_loss(ymlt_ly_exposure.loc[:, ["year", "cedant_loss"]],
                                                                            limit_cnv_ly[index],
                                                                            excess_cnv_ly[index],
                                                                            0) 

                kpi_ty_limit_ty_exposure = kpi_calc(ymlt, f"gross_loss_ty_limit_ty_exposure_{index}", sims)
                kpi_ly_limit_ty_exposure = kpi_calc(ymlt, f"gross_loss_ly_limit_ty_exposure_{index}", sims)
                kpi_ly_limit_ly_exposure = kpi_calc(ymlt, f"gross_loss_ly_limit_ly_exposure_{index}", sims)

                el_ty_limit_ty_exposure[index] = kpi_ty_limit_ty_exposure["el"]
                el_ly_limit_ty_exposure[index] = kpi_ly_limit_ty_exposure["el"]
                el_ly_limit_ly_exposure[index] = kpi_ly_limit_ly_exposure["el"]

            el_ty_limit_ty_exposure = list_to_numpy(el_ty_limit_ty_exposure, float)
            el_ly_limit_ty_exposure = list_to_numpy(el_ly_limit_ty_exposure, float)
            el_ly_limit_ly_exposure = list_to_numpy(el_ly_limit_ly_exposure, float)

            lol_ty_limit_ty_exposure = utils.ratio(el_ty_limit_ty_exposure, limit_cnv)
            lol_ly_limit_ty_exposure = utils.ratio(el_ly_limit_ty_exposure, limit_cnv_ly)
            lol_ly_limit_ly_exposure = utils.ratio(el_ly_limit_ly_exposure, limit_cnv_ly)

            ## Exposure Factor
            exposure_factor = utils.ratio(lol_ly_limit_ty_exposure - lol_ly_limit_ly_exposure, lol_ly_limit_ly_exposure)
            exposure_factor = np.where(exposure_increase == 0, 0, 1 + exposure_factor)

            ## Limits and Retentions Factor 
            lol_ty_limit_ty_exposure = utils.ratio(el_ty_limit_ty_exposure, limit_cnv)
            lol_ly_limit_ty_exposure = utils.ratio(el_ly_limit_ty_exposure, limit_cnv_ly)

            limit_excess_factor = utils.ratio(lol_ty_limit_ty_exposure - lol_ly_limit_ty_exposure, lol_ly_limit_ty_exposure)

            ## aad / reins
            sd_list = [None] * len(gross_lol_weighted)
            sd_list = [0 for x in sd_list]

            net_results_ty = net_el_func(True, [gross_lol_weighted * limit_cnv], [sd_list], limit_cnv, aggregate_deductible_cnv, number_reins, reins_perc, reins_cov_table, 0, bs_load, 1, cds.show_cat_work_comp_input)
            afb_net_el_ty = net_results_ty[8][0]

            net_results_ly = net_el_func(True, [gross_lol_weighted * limit_cnv], [sd_list], limit_cnv, aggregate_deductible_cnv_ly, number_reins_ly, reins_perc_ly, reins_cov_table, 0, bs_load, 1, cds.show_cat_work_comp_input)
            afb_net_el_ly = net_results_ly[8][0]

            rc_aad_net_lol_ty = utils.ratio(afb_net_el_ty, limit_cnv)
            rc_aad_net_lol_ly = utils.ratio(afb_net_el_ly, limit_cnv)

            ## adjust for where ly not populate (using limit = 0)
            rc_aad_net_lol_ly = np.where(limit_cnv_ly == 0, rc_aad_net_lol_ty, 0)

            aad_reins_factor = utils.ratio(rc_aad_net_lol_ty - rc_aad_net_lol_ly, rc_aad_net_lol_ly)

            ## total limit factor

            total_limit_factor = (1 + limit_excess_factor) * (1 + aad_reins_factor)


    # 4) Write back to hxd ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for index, layer in enumerate(layers):
        if renewal_layer[index]:
            layer.rate_change.exposure_change_fixed.model_calculated = exposure_factor[index]
            layer.rate_change.limit_change_fixed.model_calculated = total_limit_factor[index]

                