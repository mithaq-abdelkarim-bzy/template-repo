import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter, attrgetter
from algorithms.rate_constants import max_curves
from algorithms.timer import timer
from algorithms.udf import generate_ymlt, list_to_numpy

def rate_pml(hxd, common_data_dict):

    ## set dataframe variables for cleaner code
    cds = hxd.cds
    layers = cds.layers
    pml_select = cds.modelling_account_level

    curve_segments = ["rms_curves", "air_curves", "nmp_curves", "other_curves"]
    rp_list = [f"rp_{x}" for x in [2, 5, 10, 25, 50, 100, 200, 250, 500, 1000, 5000, 10000]]

    for seg in curve_segments:
        pml_curves = getattr(cds.pml_curves, seg)

        ## RMS Curve Selection Validation
        is_rms = seg == "rms_curves"

        if is_rms:
            if cds.show_us_fields:
                selections = [pml_select.rms_eq_curve_selection, pml_select.rms_ws_curve_selection, pml_select.rms_scs_curve_selection]                
            else:
                selections = [pml_select.rms_eu_ws_curve_selection, pml_select.rms_jp_eq_curve_selection, pml_select.rms_jp_ws_curve_selection, pml_select.rms_can_eq_curve_selection, pml_select.rms_caribbean_ws_curve_selection]

            selections = [x for x in selections if x is not None]
            if len(selections) > 0:
                selections = list_to_numpy(selections, int)
                selections = selections - 1 ## to get in python indexing level

                if len(selections[selections > len(pml_curves)]) > 0:
                    hx.errors.validation(f"RMS Peril PML Selection greater than number of RMS curves.")

        for index, curves in enumerate(pml_curves):
            rp_loss_ty = [getattr(curves.rp_loss, x) for x in rp_list]
            rp_loss_ly = [getattr(curves.rp_loss_prev, x) for x in rp_list]

            rp_loss_ty = list_to_numpy(rp_loss_ty, float)
            rp_loss_ly = list_to_numpy(rp_loss_ly, float)

            rp_loss_change = utils.ratio(rp_loss_ty - rp_loss_ly, rp_loss_ly)

            to_write = dict(zip(rp_list, rp_loss_change))

            curves.rp_loss_change = to_write

            ## RMS Curve Selection Validation
            if is_rms and (len(selections) > 0) and (index in selections):
                if rp_loss_ty.sum() == 0:
                    hx.errors.validation(f"Ensure all RMS curves, where they are a selected peril pml index, are populated.")

        ## curve agg and burn curve

        for curve_type in ["curve_aggregator", "burn_curve"]:
            pml_curves = getattr(cds.pml_curves, curve_type)

            rp_loss_ty = [getattr(pml_curves.rp_loss, x) for x in rp_list]
            rp_loss_ly = [getattr(pml_curves.rp_loss_prev, x) for x in rp_list]

            rp_loss_ty = list_to_numpy(rp_loss_ty, float)
            rp_loss_ly = list_to_numpy(rp_loss_ly, float)

            rp_loss_change = utils.ratio(rp_loss_ty - rp_loss_ly, rp_loss_ly)

            to_write = dict(zip(rp_list, rp_loss_change))

            pml_curves.rp_loss_change = to_write



                    


