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

from algorithms.udf import agg_std_dev, ccy_conversion, list_to_numpy

def rate_modelling(hxd, common_data_dict):

    # set dataframe variables for cleaner code  
    cds = hxd.cds        
    layers = cds.layers  
    rds = cds.modelling_account_level.rds_gross_loss

    rds_events = ["carolinas_ws", "miami_dade_ws", "gulf_ws", "ne_ws", "fl_pinnelas_ws", "la_eq", "nm_eq", "nm_stress_eq", "sf_eq"]

    # 1) Load input values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    limit = common_data_dict["limit"]
    application_ccy = common_data_dict["application_ccy"]
    layer_ccy  = common_data_dict["layer_ccy"]
    layer_to_app_fx_mult = common_data_dict["layer_to_app_fx_mult"]
    
    rms_ws_el = [layer.model.rms.ws_el for layer in layers]
    rms_eq_el = [layer.model.rms.eq_el for layer in layers]
    rms_scs_el = [layer.model.rms.scs_el for layer in layers]

    perc_us_el = [layer.model.rms.perc_us_el for layer in layers]

    rms_el_ty = [layer.model.rms.gross_el for layer in layers] 
    air_el_ty = [layer.model.air.gross_el for layer in layers] 
    ivor_el_ty = [layer.model.ivor.gross_el for layer in layers] 

    rms_el_ly = [layer.model_prev.rms.gross_el for layer in layers] 
    air_el_ly = [layer.model_prev.air.gross_el for layer in layers] 
    ivor_el_ly = [layer.model_prev.ivor.gross_el for layer in layers] 

    rms_nmp_el_ly = [layer.model_prev.total_rms_nmp.gross_el for layer in layers] 
    air_nmp_el_ly = [layer.model_prev.total_air_nmp.gross_el for layer in layers] 
    ivor_nmp_el_ly = [layer.model_prev.total_ivor_nmp.gross_el for layer in layers] 

    rms_sd = [layer.model.rms.gross_sd for layer in layers]
    air_sd = [layer.model.air.gross_sd for layer in layers] 
    ivor_sd = [layer.model.ivor.gross_sd for layer in layers] 

    nmp_el = common_data_dict["model_nmp_gross_el"]
    nmp_sd = common_data_dict["model_nmp_gross_sd"]
    add_rol = [layer.model.nmp.additional_rol for layer in layers]

    # convert to arrays and turn NAN to 0

    rms_ws_el = list_to_numpy(rms_ws_el, float)
    rms_eq_el = list_to_numpy(rms_eq_el, float)
    rms_scs_el = list_to_numpy(rms_scs_el, float)

    perc_us_el = list_to_numpy(perc_us_el, float)

    rms_el_ty = list_to_numpy(rms_el_ty, float)
    air_el_ty = list_to_numpy(air_el_ty, float)
    ivor_el_ty = list_to_numpy(ivor_el_ty, float)

    rms_el_ly = list_to_numpy(rms_el_ly, float)
    air_el_ly = list_to_numpy(air_el_ly, float)
    ivor_el_ly = list_to_numpy(ivor_el_ly, float)

    rms_nmp_el_ly = list_to_numpy(rms_nmp_el_ly, float)
    air_nmp_el_ly = list_to_numpy(air_nmp_el_ly, float)
    ivor_nmp_el_ly = list_to_numpy(ivor_nmp_el_ly, float)

    rms_sd = list_to_numpy(rms_sd, float)
    air_sd = list_to_numpy(air_sd, float)
    ivor_sd = list_to_numpy(ivor_sd, float)

    add_rol = list_to_numpy(add_rol, float)

    # 2) Calculations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if cds.calc_type == "US":
        perc_us_el[:] = 1
        
    gross_el_for_ri_us_application_ccy = (
        rms_el_ty 
        * utils.ratio(rms_ws_el + rms_eq_el, rms_ws_el + rms_eq_el + rms_scs_el, if_undefined = 1)
        * perc_us_el
    )

    nmp_el_incl_rol = nmp_el + (limit * add_rol)
    rol_increase = utils.ratio(nmp_el_incl_rol, nmp_el)
    nmp_sd_incl_rol = nmp_sd * rol_increase

    rms_delta = utils.ratio(rms_el_ty, rms_el_ly)
    air_delta = utils.ratio(air_el_ty, air_el_ly)

    for index, layer in enumerate(layers):
        layer.model.nmp.gross_el_incl_rol = nmp_el_incl_rol[index]
        layer.model.nmp.gross_sd_incl_rol = nmp_sd_incl_rol[index]

        layer.model.rms.change_el = rms_delta[index]
        layer.model.air.change_el = air_delta[index]

    if cds.show_intl_fields:
        ## in here convert to application currencies
        gross_el_for_ri_us_application_ccy = gross_el_for_ri_us_application_ccy * layer_to_app_fx_mult

        nmp_el_incl_rol = nmp_el_incl_rol * layer_to_app_fx_mult
        nmp_sd_incl_rol = nmp_sd_incl_rol * layer_to_app_fx_mult

        rms_el_ty = rms_el_ty * layer_to_app_fx_mult
        rms_sd = rms_sd * layer_to_app_fx_mult

        air_el_ty = air_el_ty * layer_to_app_fx_mult
        air_sd = air_sd * layer_to_app_fx_mult

        ivor_el_ty = ivor_el_ty * layer_to_app_fx_mult
        ivor_sd = ivor_sd * layer_to_app_fx_mult

    rms_nmp_el = rms_el_ty + nmp_el_incl_rol
    rms_nmp_sd = np.sqrt(rms_sd ** 2 + nmp_sd_incl_rol ** 2)
    rms_nmp_delta = utils.ratio(rms_nmp_el, rms_nmp_el_ly)

    air_nmp_el = air_el_ty + nmp_el_incl_rol
    air_nmp_sd = np.sqrt(air_sd ** 2 + nmp_sd_incl_rol ** 2)
    air_nmp_delta = utils.ratio(air_nmp_el, air_nmp_el_ly)

    if cds.modelling_account_level.ivor_nmp_selection == "Excludes NMP":
        ivor_nmp_el = ivor_el_ty + nmp_el_incl_rol
        ivor_nmp_sd = np.sqrt(ivor_sd ** 2 + nmp_sd_incl_rol ** 2)
    else:
        ivor_nmp_el = ivor_el_ty
        ivor_nmp_sd = ivor_el_ty

    ivor_nmp_delta = utils.ratio(ivor_nmp_el, ivor_nmp_el_ly)

    # 3) write back to hxd ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for index, layer in enumerate(layers):
        rms_df = {"gross_el": rms_nmp_el[index],
                  "gross_sd": rms_nmp_sd[index],
                  "change_el": rms_nmp_delta[index]}

        ivor_df = {"gross_el": ivor_nmp_el[index],
                   "gross_sd": ivor_nmp_sd[index],
                   "change_el": ivor_nmp_delta[index]}

        air_df = {"gross_el": air_nmp_el[index],
                  "gross_sd": air_nmp_sd[index],
                  "change_el": air_nmp_delta[index]}

        layer.model.total_rms_nmp = rms_df
        layer.model.total_air_nmp = air_df
        layer.model.total_ivor_nmp = ivor_df

        layer.model.rms.gross_el_for_ri_us_application_ccy = gross_el_for_ri_us_application_ccy[index]

    # 4) Write RDS Growth ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for i in rds_events:
        growth = utils.ratio( (getattr(rds.this_year, i) or 0) - (getattr(rds.previous_year, i) or 0),
                                                getattr(rds.previous_year, i) or 0)
        setattr(rds.yoy_growth, i, growth)

    # 4) Write to common_data_dict ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    common_data_dict["rms_gross_el_for_ri_us"] = gross_el_for_ri_us_application_ccy
    common_data_dict["rms_gross_el"] = rms_nmp_el
    common_data_dict["rms_gross_sd"] = rms_nmp_sd

    common_data_dict["ivor_gross_el"] = ivor_nmp_el
    common_data_dict["ivor_gross_sd"] = ivor_nmp_sd

    common_data_dict["air_gross_el"] = air_nmp_el
    common_data_dict["air_gross_sd"] = air_nmp_sd

    return common_data_dict