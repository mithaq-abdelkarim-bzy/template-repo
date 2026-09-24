import hx
import pandas as pd
import numpy as np
import math as math
import json
from algorithms.rate_utilities import title_rc, ratio
from operator import itemgetter
from algorithms.rate_constants import max_layers
import algorithms.rate_utilities as utils
from algorithms.udf import list_to_numpy, net_el_func


def rate_rate_change(hxd, common_data_dict):
    # set dataframe variables for cleaner code  
    cds = hxd.cds        
    layers = cds.layers
    exp_change = cds.exposure.aggregate.perc_change

    # 1) Load input values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    epi_weight = common_data_dict["epi_weight"]
    rol_prem_selection = common_data_dict["rol_prem_selection"]

    expiring_layer_to_use = [layer.rate_change.expiring_layer_to_use - 1 for layer in layers]
    renewal_layer = [layer.renewal_layer for layer in layers]

    is_risk_xl = cds.programme == "Risk XL"

    roev = [layer.quote.rol_ty.roev for layer in layers]
    roev_ly = [layer.quote.rol_ly.roev for layer in layers]

    roev = list_to_numpy(roev, float)
    roev_ly = list_to_numpy(roev_ly, float)

    ## validation
    expiring_layer_to_use_for_validation = list_to_numpy(expiring_layer_to_use, int)

    if max(expiring_layer_to_use_for_validation) + 1 > len(layers):
        cds.rate_change.rate_change_validation = False
        hx.errors.validation(f"All entered 'Expiring layer to use' must be within range of layers to run rate change.")
    else:
        cds.rate_change.rate_change_validation = True

        exposure_selection = [layer.rate_change.exposure_selection for layer in layers]
        exp_total_change = exp_change.exposure_total
        exp_bespoke_total = exp_change.bespoke_total
        exp_key_zone_total = exp_change.key_zone_total
        exp_prem_change = cds.exposure.aggregate.perc_change.prem_change

        exposure_model_factor = [layer.rate_change.exposure_change_fixed.model_calculated for layer in layers]
        exposure_uw_factor = [layer.rate_change.exposure_change_fixed.uw_selected for layer in layers]

        limit_model_factor = [layer.rate_change.limit_change_fixed.model_calculated for layer in layers]
        limit_uw_factor = [layer.rate_change.limit_change_fixed.uw_selected for layer in layers]

        other_uw_factor = [layer.rate_change.other_change_fixed.uw_selected for layer in layers]
        tc_uw_factor = [layer.rate_change.terms_conditions_change_fixed.uw_selected for layer in layers]
        
        rol_fot_ly = [layer.quote.rol_ly.rol_fot for layer in layers]

        gross_lol_ty = [layer.quote.rol_ty.gross_lol_weighted for layer in layers]
        gross_lol_ly = [layer.quote.rol_ly.gross_lol_weighted for layer in layers]

        ## convert to arrays and turn NAN to 0 
        exposure_selection = list_to_numpy(exposure_selection, str)

        exposure_model_factor = list_to_numpy(exposure_model_factor, float)
        exposure_uw_factor = list_to_numpy(exposure_uw_factor, float)

        limit_model_factor = list_to_numpy(limit_model_factor, float)
        limit_uw_factor = list_to_numpy(limit_uw_factor, float)

        other_uw_factor = list_to_numpy(other_uw_factor, float)
        tc_uw_factor = list_to_numpy(tc_uw_factor, float)

        rol_fot_ly = list_to_numpy(rol_fot_ly, float)

        gross_lol_ty = list_to_numpy(gross_lol_ty, float)
        gross_lol_ly = list_to_numpy(gross_lol_ly, float)

        ## re-order all ly data
        rol_fot_ly = rol_fot_ly[expiring_layer_to_use]
        gross_lol_ly = gross_lol_ly[expiring_layer_to_use]

        # 2) Calcs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        exposure_increase = np.where(exposure_selection == "Total", 1 + exp_total_change,
                                np.where(exposure_selection == "Bespoke", 1 + exp_bespoke_total,
                                    np.where(exposure_selection == "Premium", exp_prem_change, # prem change already relative
                                            1 + exp_key_zone_total)))

        exposure_selected_factor = np.where(exposure_uw_factor == 0, exposure_model_factor, exposure_uw_factor)
        exposure_selected_factor = np.where(exposure_selected_factor == 0, 1, exposure_selected_factor)

        limit_selected_factor = np.where(limit_uw_factor == 0, limit_model_factor, limit_uw_factor)
        limit_selected_factor = np.where(limit_selected_factor == 0, 1, limit_selected_factor)
        
        other_selected_factor = np.where(other_uw_factor == 0, 1, other_uw_factor)
        tc_selected_factor = np.where(tc_uw_factor == 0, 1, tc_uw_factor)

        rebase_factor = exposure_selected_factor * limit_selected_factor * other_selected_factor * tc_selected_factor

        if (is_risk_xl) & (cds.rate_change.risk_xl_exposure_selection == "ROEV"):
            rol_rebased = rol_fot_ly
            risk_adjusted_rate_change = np.array(utils.ratio(roev, roev_ly * other_selected_factor * tc_selected_factor))
        else:
            rol_rebased = rol_fot_ly * rebase_factor
            risk_adjusted_rate_change = np.array(utils.ratio(rol_prem_selection, rol_rebased))

        ## comments
        exposure_comment = np.where(exposure_selected_factor == exposure_model_factor, exposure_selection, "UW Override")
        limit_comment = np.where(limit_selected_factor == limit_model_factor, "Curve Aggregator Estimate", "UW Override")

        # populate total fields
        total_rc = utils.ratio(epi_weight[(risk_adjusted_rate_change > 0) & renewal_layer].sum(), utils.ratio(epi_weight[renewal_layer], risk_adjusted_rate_change[renewal_layer]).sum())
        cds.summary.ty.risk_adjusted_rate_change = total_rc
        cds.rate_change.risk_adjusted_rate_change = total_rc

        # 3) Lloyd's buckets ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        other_factors_change = exposure_selected_factor * other_selected_factor * tc_selected_factor

        # 3) Write back to hxd ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        for index in range(1, len(layers) + 1):
            setattr(hxd.cds.rate_change, f"show_layer_{index}", True)

        for index, layer in enumerate(layers):
            if renewal_layer[index]:
                layer.rate_change.exposure_increase = exposure_increase[index]
                layer.rate_change.rebase_factor = rebase_factor[index]
                layer.rate_change.rol_rebased = rol_rebased[index]
                layer.rate_change.risk_adjusted_rate_change = risk_adjusted_rate_change[index]
                layer.rate_change.rol_ly_to_use = rol_fot_ly[index]

                # for synergy tab
                layer.rate_change.exposure_change_fixed.final = exposure_selected_factor[index]
                layer.rate_change.risk_characteristics_change_fixed.final = 1
                layer.rate_change.deductible_change_fixed.final = 1
                layer.rate_change.limit_change_fixed.final = limit_selected_factor[index]
                layer.rate_change.terms_conditions_change_fixed.final = tc_selected_factor[index]
                layer.rate_change.other_change_fixed.final = other_selected_factor[index]
                
                layer.rate_change.rate_change.uw_selected = risk_adjusted_rate_change[index]
                layer.rate_change.rate_change.lloyds_limit_attachment_point_change = limit_selected_factor[index]
                layer.rate_change.rate_change.lloyds_breadth_of_cover_change = 1
                layer.rate_change.rate_change.other_factors_change = other_factors_change[index]

                layer.rate_change.exposure_change_fixed.comment = exposure_comment[index]
                layer.rate_change.limit_change_fixed.comment = limit_comment[index]

                ## summary
                layer.summary.ty.risk_adjusted_rate_change = risk_adjusted_rate_change[index]
