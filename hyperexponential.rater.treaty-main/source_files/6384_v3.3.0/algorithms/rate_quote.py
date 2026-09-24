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
from algorithms.timer import timer

from algorithms.udf import agg_std_dev, reins_approx, ccy_conversion, list_to_numpy, net_el_func

ccy_table = hx_params.table_currency
tp_params_table = hx_params.table_tp_params
tp_params_table = tp_params_table.set_index("item")
ri_cede_table = hx_params.table_ri_cede
ri_cede_table_ly = hx_params.table_ri_cede_ly
rds_ri_region_table = hx_params.table_rds_regions_us_ri
reins_cov_table = hx_params.table_reins_cov
reins_cov_table = reins_cov_table.set_index("parameter")

tp_params_table_ly = hx_params.table_tp_params_ly
tp_params_table_ly = tp_params_table_ly.set_index("item")

roc_load = tp_params_table.at["roc", "load"]
direct_expenses_load = tp_params_table.at["direct_expenses", "load"]
lae_load = tp_params_table.at["lae", "load"]
gross_group_cat_risk = tp_params_table.at["gross_group_cat_risk", "load"]
held_capital = tp_params_table.at["held_capital", "load"]
add_group_cat_risk = tp_params_table.at["add_group_cat_risk", "load"]
add_cap_req = tp_params_table.at["add_cap_req", "load"]
attr_cap_load = tp_params_table.at["attr_cap", "load"]
inv_income_load = tp_params_table.at["inv_income", "load"]
sd_factor_us = tp_params_table.at["sd_factor_us", "load"]
sd_factor_intl = tp_params_table.at["sd_factor_intl", "load"]
maxlr = tp_params_table.at["maxlr", "load"]
comb_ratio = tp_params_table.at["comb_ratio", "load"]
bs_load = tp_params_table.at["black_swan", "load"]
default_line = tp_params_table.at["default_line", "load"]
risk_xl_capital_load = tp_params_table.at["risk_xl_capital_load", "load"]
risk_xl_sd_load = tp_params_table.at["risk_xl_sd_load", "load"]


direct_expenses_load_ly = tp_params_table_ly.at["direct_expenses", "load"]
lae_load_ly = tp_params_table_ly.at["lae", "load"]
inv_income_load_ly = tp_params_table_ly.at["inv_income", "load"]
sd_factor_us_ly = tp_params_table_ly.at["sd_factor_us", "load"]
sd_factor_intl_ly = tp_params_table_ly.at["sd_factor_intl", "load"]

## ty ri cede
ty_ri_cede_dict = {}

ty_ri_cede_dict["north_east_ratio"] = ri_cede_table.loc[ri_cede_table["region"] == "north_east", "ceded_per_aal"].iloc[0]
ty_ri_cede_dict["mid_atlantic_ratio"] = ri_cede_table.loc[ri_cede_table["region"] == "mid_atlantic", "ceded_per_aal"].iloc[0]
ty_ri_cede_dict["carolinas_ratio"] = ri_cede_table.loc[ri_cede_table["region"] == "carolinas", "ceded_per_aal"].iloc[0]
ty_ri_cede_dict["fl_se_ratio"] = ri_cede_table.loc[ri_cede_table["region"] == "fl_se", "ceded_per_aal"].iloc[0]
ty_ri_cede_dict["fl_non_se_ratio"] = ri_cede_table.loc[ri_cede_table["region"] == "fl_non_se", "ceded_per_aal"].iloc[0]
ty_ri_cede_dict["al_miss_ratio"] = ri_cede_table.loc[ri_cede_table["region"] == "al_miss", "ceded_per_aal"].iloc[0]
ty_ri_cede_dict["louisiana_ratio"] = ri_cede_table.loc[ri_cede_table["region"] == "louisiana", "ceded_per_aal"].iloc[0]
ty_ri_cede_dict["tx_east_ratio"] = ri_cede_table.loc[ri_cede_table["region"] == "tx_east", "ceded_per_aal"].iloc[0]
ty_ri_cede_dict["tx_west_ratio"] = ri_cede_table.loc[ri_cede_table["region"] == "tx_west", "ceded_per_aal"].iloc[0]
ty_ri_cede_dict["cal_south_ratio"] = ri_cede_table.loc[ri_cede_table["region"] == "cal_south", "ceded_per_aal"].iloc[0]
ty_ri_cede_dict["cal_north_ratio"] = ri_cede_table.loc[ri_cede_table["region"] == "cal_north", "ceded_per_aal"].iloc[0]
ty_ri_cede_dict["pnw_ratio"] = ri_cede_table.loc[ri_cede_table["region"] == "pnw", "ceded_per_aal"].iloc[0]
ty_ri_cede_dict["new_madrid_ratio"] = ri_cede_table.loc[ri_cede_table["region"] == "new_madrid", "ceded_per_aal"].iloc[0]
ty_ri_cede_dict["hawaii_ratio"] = ri_cede_table.loc[ri_cede_table["region"] == "hawaii", "ceded_per_aal"].iloc[0]

eu_ws_ratio = ri_cede_table.loc[ri_cede_table["region"] == "eu_ws", "ceded_per_aal"].iloc[0]
jp_eq_ratio = ri_cede_table.loc[ri_cede_table["region"] == "jp_eq", "ceded_per_aal"].iloc[0]
jp_ws_ratio = ri_cede_table.loc[ri_cede_table["region"] == "jp_ws", "ceded_per_aal"].iloc[0]
can_eq_ratio = ri_cede_table.loc[ri_cede_table["region"] == "can_eq", "ceded_per_aal"].iloc[0]
caribbean_ws_ratio = ri_cede_table.loc[ri_cede_table["region"] == "caribbean_ws", "ceded_per_aal"].iloc[0]

us_wf_ratio = ri_cede_table.loc[ri_cede_table["region"] == "us_wf", "ceded_per_aal"].iloc[0]

ty_ri_cede_dict["eu_ws_ratio"] = eu_ws_ratio
ty_ri_cede_dict["jp_eq_ratio"] = jp_eq_ratio
ty_ri_cede_dict["jp_ws_ratio"] = jp_ws_ratio
ty_ri_cede_dict["can_eq_ratio"] = can_eq_ratio
ty_ri_cede_dict["caribbean_ws_ratio"] = caribbean_ws_ratio
ty_ri_cede_dict["us_wf_ratio"] = us_wf_ratio

## ly ri cede
ly_ri_cede_dict = {}

ly_ri_cede_dict["north_east_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "north_east", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["mid_atlantic_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "mid_atlantic", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["carolinas_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "carolinas", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["fl_se_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "fl_se", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["fl_non_se_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "fl_non_se", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["al_miss_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "al_miss", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["louisiana_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "louisiana", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["tx_east_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "tx_east", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["tx_west_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "tx_west", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["cal_south_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "cal_south", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["cal_north_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "cal_north", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["pnw_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "pnw", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["new_madrid_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "new_madrid", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["hawaii_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "hawaii", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["us_wf_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "us_wf", "ceded_per_aal"].iloc[0]

ly_ri_cede_dict["eu_ws_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "eu_ws", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["jp_eq_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "jp_eq", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["jp_ws_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "jp_ws", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["can_eq_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "can_eq", "ceded_per_aal"].iloc[0]
ly_ri_cede_dict["caribbean_ws_ratio"] = ri_cede_table_ly.loc[ri_cede_table_ly["region"] == "caribbean_ws", "ceded_per_aal"].iloc[0]


def rate_quote(hxd, common_data_dict):

    # set dataframe variables for cleaner code  
    cds = hxd.cds        
    layers = cds.layers

    # 1) Load parameter table values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # convert indirect expenses from USD to application currency
    application_ccy = common_data_dict["application_ccy"]
    ccy_from_usd = ccy_conversion(pd.Series("USD"), application_ccy, hx_params.table_currency)[0]

    indirect_expenses = tp_params_table.at["indirect_expenses", "load"] * ccy_from_usd

    indirect_expenses_ly = tp_params_table_ly.at["indirect_expenses", "load"] * ccy_from_usd

    # 2) Load input values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    summary_ccy = cds.currency_policy_financials
    layer_to_app_fx_mult = common_data_dict["layer_to_app_fx_mult"]

    brokerage = common_data_dict["effective_brokerage"]
    tax = cds.tax if cds.tax else 0
    ceding_commission = cds.ceding_commission if cds.ceding_commission else 0
    other_acq_costs = cds.other_acq_costs if cds.other_acq_costs else 0

    up_front_deductions = brokerage + tax + ceding_commission + other_acq_costs

    if np.any(up_front_deductions > 1):        
        hx.errors.validation(f"The sum of brokerage, tax and ceding commission is ({up_front_deductions}), it must be less than (1).")
        up_front_deductions = 1

    limit_cnv = common_data_dict["limit_cnv"]
    aad_cnv = common_data_dict["aad_cnv"]
    number_reins = common_data_dict["number_reins"]
    perc_reins_1 = common_data_dict["perc_reins_1"]
    perc_reins_2 = common_data_dict["perc_reins_2"]
    perc_reins_3 = common_data_dict["perc_reins_3"]

    eu_ws_el = [layer.model.rms.eu_ws_el for layer in layers]
    jp_eq_el = [layer.model.rms.jp_eq_el for layer in layers]
    jp_ws_el = [layer.model.rms.jp_ws_el for layer in layers]
    can_eq_el = [layer.model.rms.can_eq_el for layer in layers]
    caribbean_ws_el = [layer.model.rms.caribbean_ws_el for layer in layers]

    wf_gross_el = [layer.nmp.non_modelled_perils_total.peril_el.el_wf for layer in layers]
    rms_gross_el_for_ri_us = common_data_dict["rms_gross_el_for_ri_us"]
    rms_gross_el = common_data_dict["rms_gross_el"]
    rms_gross_sd = common_data_dict["rms_gross_sd"]
    ivor_gross_el = common_data_dict["ivor_gross_el"]
    ivor_gross_sd = common_data_dict["ivor_gross_sd"]
    air_gross_el = common_data_dict["air_gross_el"]
    air_gross_sd = common_data_dict["air_gross_sd"]

    burn_gross_el = common_data_dict["burn_gross_el"]
    burn_gross_sd = common_data_dict["burn_gross_sd"]

    mi_250 = [layer.marginal_impacts.treaty_group.mi_250 for layer in layers]
    mi_10 = [layer.marginal_impacts.treaty_group.mi_10 for layer in layers] 
    override_limit_factor = [layer.quote.rms_tp_calc.override_limit_factor for layer in layers]

    rol_quote = [layer.quote.rol_ty.rol_quote for layer in layers]
    rol_fot = [layer.quote.rol_ty.rol_fot for layer in layers]

    written_line = [layer.quote.rol_ty.written_line for layer in layers]
    estimated_signing = [layer.quote.rol_ty.estimated_signing for layer in layers]
    signed_line = [layer.quote.rol_ty.signed_line for layer in layers]

    weighting_rms = [layer.quote.rol_ty.weighting_rms for layer in layers]
    weighting_ivor = [layer.quote.rol_ty.weighting_ivor for layer in layers]
    weighting_air = [layer.quote.rol_ty.weighting_air for layer in layers]
    weighting_burn = [layer.quote.rol_ty.weighting_burn for layer in layers]
    rol_burn_override = [layer.quote.rol_ty.rol_burn_override for layer in layers]


    ## attach and exit rp
    curve_agg_rp_attach = [layer.quote.rol_ty.curve_agg_rp_attach for layer in layers]
    curve_agg_rp_exit = [layer.quote.rol_ty.curve_agg_rp_exit for layer in layers]
    ## rms ap
    rms_ap_attach = [layer.quote.rol_ty.rms_ap_attach for layer in layers]
    rms_ap_exit = [layer.quote.rol_ty.rms_ap_exit for layer in layers]
    ## rms eq
    rms_eq_attach = [layer.quote.rol_ty.rms_eq_attach for layer in layers]
    rms_eq_exit = [layer.quote.rol_ty.rms_eq_exit for layer in layers]
    ## rms ws
    rms_ws_attach = [layer.quote.rol_ty.rms_ws_attach for layer in layers]
    rms_ws_exit = [layer.quote.rol_ty.rms_ws_exit for layer in layers]
    ## rms scs
    rms_scs_attach = [layer.quote.rol_ty.rms_scs_attach for layer in layers]
    rms_scs_exit = [layer.quote.rol_ty.rms_scs_exit for layer in layers]
    ## air ap
    air_ap_attach = [layer.quote.rol_ty.air_ap_attach for layer in layers]
    air_ap_exit = [layer.quote.rol_ty.air_ap_exit for layer in layers]
    ## air eq
    air_eq_attach = [layer.quote.rol_ty.air_eq_attach for layer in layers]
    air_eq_exit = [layer.quote.rol_ty.air_eq_exit for layer in layers]
    ## air ws
    air_ws_attach = [layer.quote.rol_ty.air_ws_attach for layer in layers]
    air_ws_exit = [layer.quote.rol_ty.air_ws_exit for layer in layers]
    ## air scs
    air_scs_attach = [layer.quote.rol_ty.air_scs_attach for layer in layers]
    air_scs_exit = [layer.quote.rol_ty.air_scs_exit for layer in layers]
    ## air winter
    air_winter_attach = [layer.quote.rol_ty.air_winter_attach for layer in layers]
    air_winter_exit = [layer.quote.rol_ty.air_winter_exit for layer in layers]
    ## air wf
    air_wf_attach = [layer.quote.rol_ty.air_wf_attach for layer in layers]
    air_wf_exit = [layer.quote.rol_ty.air_wf_exit for layer in layers]

    rp_pml_selection = [layer.quote.rol_ty.rp_pml_selection for layer in layers]
    rp_pml_selection_peak = [layer.quote.rol_ty.rp_pml_selection_peak for layer in layers]

    ## convert to arrays and turn NAN to 0    
    reins_perc = [[perc_reins_1[i], perc_reins_2[i], perc_reins_3[i]] for i in range(len(layers))]

    eu_ws_el = list_to_numpy(eu_ws_el, float)
    jp_eq_el = list_to_numpy(jp_eq_el, float)
    jp_ws_el = list_to_numpy(jp_ws_el, float)
    can_eq_el = list_to_numpy(can_eq_el, float)
    caribbean_ws_el = list_to_numpy(caribbean_ws_el, float)

    wf_gross_el = list_to_numpy(wf_gross_el, float)

    mi_250 = list_to_numpy(mi_250, float)
    mi_10 = list_to_numpy(mi_10, float)
    override_limit_factor = list_to_numpy(override_limit_factor, float)

    rol_quote = list_to_numpy(rol_quote, float)
    rol_fot = list_to_numpy(rol_fot, float)

    written_line = list_to_numpy(written_line, float)
    estimated_signing = list_to_numpy(estimated_signing, float)
    signed_line = list_to_numpy(signed_line, float)

    weighting_rms = list_to_numpy(weighting_rms, float)
    weighting_ivor = list_to_numpy(weighting_ivor, float)
    weighting_air = list_to_numpy(weighting_air, float)
    weighting_burn = list_to_numpy(weighting_burn, float)
    rol_burn_override = list_to_numpy(rol_burn_override, float)


    ## curve agg
    curve_agg_rp_attach = list_to_numpy(curve_agg_rp_attach, float)
    curve_agg_rp_exit = list_to_numpy(curve_agg_rp_exit, float)
    ## rms ap
    rms_ap_attach = list_to_numpy(rms_ap_attach, float)
    rms_ap_exit = list_to_numpy(rms_ap_exit, float)
    ## rms eq
    rms_eq_attach = list_to_numpy(rms_eq_attach, float)
    rms_eq_exit = list_to_numpy(rms_eq_exit, float)
    ## rms ws
    rms_ws_attach = list_to_numpy(rms_ws_attach, float)
    rms_ws_exit = list_to_numpy(rms_ws_exit, float)
    ## rms scs
    rms_scs_attach = list_to_numpy(rms_scs_attach, float)
    rms_scs_exit = list_to_numpy(rms_scs_exit, float)
    ## air ap
    air_ap_attach = list_to_numpy(air_ap_attach, float)
    air_ap_exit = list_to_numpy(air_ap_exit, float)
    ## air eq
    air_eq_attach = list_to_numpy(air_eq_attach, float)
    air_eq_exit = list_to_numpy(air_eq_exit, float)
    ## air ws
    air_ws_attach = list_to_numpy(air_ws_attach, float)
    air_ws_exit = list_to_numpy(air_ws_exit, float)
    ## air scs
    air_scs_attach = list_to_numpy(air_scs_attach, float)
    air_scs_exit = list_to_numpy(air_scs_exit, float)
    ## air winter
    air_winter_attach = list_to_numpy(air_winter_attach, float)
    air_winter_exit = list_to_numpy(air_winter_exit, float)
    ## air wf
    air_wf_attach = list_to_numpy(air_wf_attach, float)
    air_wf_exit = list_to_numpy(air_wf_exit, float)

    rp_pml_selection = np.array(rp_pml_selection, dtype = str)
    rp_pml_selection_peak = np.array(rp_pml_selection_peak, dtype = str)

    # 3) ROL and Premium ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if rol_fot.sum() > 0:
        rol_prem_selection = rol_fot
    else:
        rol_prem_selection = rol_quote

    common_data_dict["rol_prem_selection"] = rol_prem_selection

    quote_fot_ratio = utils.ratio(rol_fot, rol_quote)

    conditions = [signed_line > 0, estimated_signing > 0, written_line > 0]
    choices = [signed_line, estimated_signing, written_line]
    afb_line = np.select(conditions, choices, default = default_line)
    afb_line_for_totals = np.select(conditions, choices, default = 0)

    prem_full_line = limit_cnv * rol_prem_selection

    epi_written = prem_full_line * written_line * (1 - up_front_deductions)
    epi_estimated = prem_full_line * estimated_signing * (1 - up_front_deductions)
    epi_signed = prem_full_line * signed_line * (1 - up_front_deductions)

    est_sign_written_ratio = utils.ratio(epi_estimated, epi_written, 1)
    est_sign_written_ratio = np.where(est_sign_written_ratio == 0, 1, est_sign_written_ratio)

    #NOTE start risk / cat calc split
    is_risk_xl = cds.programme == "Risk XL"

    if is_risk_xl:

        ## risk xl fields
        risk_burn_gross_non_cat = common_data_dict["risk_burn_gross_non_cat"]
        risk_burn_gross_total = common_data_dict["risk_burn_gross_total"]
        burn_net_el = common_data_dict["burn_net_el"]

        afb_burn_net_el = burn_net_el * afb_line
        afb_burn_net_cat_el = afb_burn_net_el * utils.ratio(risk_burn_gross_total - risk_burn_gross_non_cat, risk_burn_gross_total)

        risk_exposure_gross_non_cat = common_data_dict["risk_exposure_gross_non_cat"]
        risk_exposure_gross_total = common_data_dict["risk_exposure_gross_total"]
        risk_exposure_net_el = common_data_dict["risk_exposure_net_el"]

        risk_exposure_gross_non_cat = list_to_numpy(risk_exposure_gross_non_cat, float)
        risk_exposure_gross_total = list_to_numpy(risk_exposure_gross_total, float)
        risk_exposure_net_el = list_to_numpy(risk_exposure_net_el, float)

        afb_risk_exposure_net_el = risk_exposure_net_el * afb_line
        afb_risk_exposure_net_cat_el = afb_risk_exposure_net_el * utils.ratio(risk_exposure_gross_total - risk_exposure_gross_non_cat, risk_exposure_gross_total)

        risk_xl_weighting_exposure = [layer.quote.rol_ty.risk_xl_weighting_exposure for layer in layers]
        risk_xl_weighting_exposure = list_to_numpy(risk_xl_weighting_exposure, float)

        ## bermuda brokerage adjustment
        second_loss_probability_results = [layer.risk_xl_exposure_rating.no_expected_reins for layer in layers]
        second_loss_probability_results = list_to_numpy(second_loss_probability_results, float)

        if cds.show_bermuda:
            second_loss_brokerage = cds.second_loss_brokerage
            second_loss_probability_results = np.where(number_reins > 0, second_loss_probability_results, 0)

            expected_second_loss_brokerage = second_loss_brokerage * perc_reins_1 * second_loss_probability_results

            rol_calc_deductions = brokerage + expected_second_loss_brokerage + tax + ceding_commission + other_acq_costs
        else:
            rol_calc_deductions = up_front_deductions        
    
        
        ## burn
        total_coc = afb_burn_net_el * risk_xl_capital_load * roc_load
        ri_cost = 0
        sd_selection = risk_xl_sd_load

        tp_calc_1_burn = np.where(afb_burn_net_el > 0, utils.ratio(afb_burn_net_el + (afb_burn_net_cat_el * lae_load) + total_coc + ri_cost + indirect_expenses, 1 - direct_expenses_load + inv_income_load), 0)
        tp_calc_2_burn = np.where(afb_burn_net_el > 0, utils.ratio(afb_burn_net_el + (afb_burn_net_cat_el * lae_load) + indirect_expenses + (rms_gross_sd * afb_line * sd_selection), 1 - direct_expenses_load), 0)
        tp_calc_3_burn = np.where(afb_burn_net_el > 0, utils.ratio(afb_burn_net_el + (afb_burn_net_cat_el * lae_load), maxlr), 0)

        tp_max_burn = np.maximum(tp_calc_1_burn, tp_calc_2_burn)
        tp_max_burn = np.maximum(tp_max_burn, tp_calc_3_burn)

        rol_burn = utils.ratio(utils.ratio(tp_max_burn, 1 - rol_calc_deductions), limit_cnv * afb_line)

        ## exposure
        total_coc = afb_risk_exposure_net_el * risk_xl_capital_load * roc_load
        ri_cost = 0
        sd_selection = risk_xl_sd_load

        tp_calc_1_exposure = np.where(afb_risk_exposure_net_el > 0, utils.ratio(afb_risk_exposure_net_el + (afb_risk_exposure_net_cat_el * lae_load) + total_coc + ri_cost + indirect_expenses, 1 - direct_expenses_load + inv_income_load), 0)
        tp_calc_2_exposure = np.where(afb_risk_exposure_net_el > 0, utils.ratio(afb_risk_exposure_net_el + (afb_risk_exposure_net_cat_el * lae_load) + indirect_expenses + (rms_gross_sd * afb_line * sd_selection), 1 - direct_expenses_load), 0)
        tp_calc_3_exposure = np.where(afb_risk_exposure_net_el > 0, utils.ratio(afb_risk_exposure_net_el + (afb_risk_exposure_net_cat_el * lae_load), maxlr), 0)

        tp_max_exposure = np.maximum(tp_calc_1_exposure, tp_calc_2_exposure)
        tp_max_exposure = np.maximum(tp_max_exposure, tp_calc_3_exposure)

        rol_exposure = utils.ratio(utils.ratio(tp_max_exposure, 1 - rol_calc_deductions), limit_cnv * afb_line)

        ## lol gross
        gross_lol_exposure = utils.ratio(risk_exposure_gross_total, limit_cnv)
        gross_lol_burn = utils.ratio(risk_burn_gross_total, limit_cnv)
        gross_lol_burn_override = rol_burn_override * utils.ratio(gross_lol_exposure, rol_exposure)
        gross_lol_burn = np.where(gross_lol_burn_override > 0, gross_lol_burn_override, gross_lol_burn)

        ## lol net
        lol_exposure = utils.ratio(afb_risk_exposure_net_el, limit_cnv * afb_line)
        lol_burn = utils.ratio(afb_burn_net_el, limit_cnv * afb_line)
        lol_burn_override = rol_burn_override * utils.ratio(lol_exposure, rol_exposure)
        lol_burn = np.where(lol_burn_override > 0, lol_burn_override, lol_burn)


        # 10) Weighted Results ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        rol_arrays = [rol_exposure, np.where(rol_burn_override > 0, rol_burn_override, rol_burn)]
        gross_lol_arrays = [gross_lol_exposure, gross_lol_burn]
        net_lol_arrays = [lol_exposure, lol_burn]
        net_el_arrays = [afb_risk_exposure_net_el, afb_burn_net_el]
        tp_arrays = [tp_max_exposure, tp_max_burn]
        weighting_arrays = [risk_xl_weighting_exposure, weighting_burn]

        ## metrics
        rol_afb_tech = utils.ratio(
                                    np.sum(np.multiply(rol_arrays, weighting_arrays), axis = 0),
                                    np.sum(weighting_arrays, axis = 0)
        )

        gross_lol_weighted = utils.ratio(
                                        np.sum(np.multiply(gross_lol_arrays, weighting_arrays), axis = 0),
                                        np.sum(weighting_arrays, axis = 0)
        )

        lol_weighted = utils.ratio(
                                    np.sum(np.multiply(net_lol_arrays, weighting_arrays), axis = 0),
                                    np.sum(weighting_arrays, axis = 0)
        )

        weighted_el = utils.ratio(
                                    np.sum(np.multiply(net_el_arrays, weighting_arrays), axis = 0),
                                    np.sum(weighting_arrays, axis = 0)
        )

        weighted_tp = utils.ratio(
                                    np.sum(np.multiply(tp_arrays, weighting_arrays), axis = 0),
                                    np.sum(weighting_arrays, axis = 0)
        )

        ### indirect expenses done upon load and currency conversion as done at top
        inv_income = weighted_tp * inv_income_load
        direct_expenses = direct_expenses_load * weighted_tp
        lae = afb_risk_exposure_net_cat_el * lae_load
        total_expenses = indirect_expenses + direct_expenses + lae

        expenses_less_inv_income = total_expenses - inv_income

        sd_load = (rms_gross_sd * afb_line * sd_selection)
        calc_3_lr_load = np.maximum(tp_calc_3_exposure - afb_risk_exposure_net_el, 0)

        total_capital = weighted_el * 1.1


        rol_rms = rol_afb_tech

    else:
        
        # 4) Expected Loss Calculations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        rms_afb_net_results = net_el_func(True, [rms_gross_el], [rms_gross_sd], limit_cnv, aad_cnv, number_reins, reins_perc, reins_cov_table, override_limit_factor, bs_load, afb_line, cds.show_cat_work_comp_input)

        gross_lol_rms = rms_afb_net_results[0][0]
        model_limit_factor = rms_afb_net_results[1][0]
        net_el_excl_reins_prem = rms_afb_net_results[2][0]
        exp_reins_cost = rms_afb_net_results[3][0]
        net_el = rms_afb_net_results[4][0]
        net_sd = rms_afb_net_results[5][0]
        net_el_incl_bs = rms_afb_net_results[6][0]
        net_sd_incl_bs = rms_afb_net_results[7][0]
        afb_net_el = rms_afb_net_results[8][0]
        afb_net_sd = rms_afb_net_results[9][0]

        second_loss_probability_results = rms_afb_net_results[10][0]

        ## bermuda brokerage adjustment
        if cds.show_bermuda:
            second_loss_brokerage = cds.second_loss_brokerage
            second_loss_probability_results = np.where(number_reins > 0, second_loss_probability_results, 0)

            expected_second_loss_brokerage = second_loss_brokerage * perc_reins_1 * second_loss_probability_results

            rol_calc_deductions = brokerage + expected_second_loss_brokerage + tax + ceding_commission + other_acq_costs
        else:
            rol_calc_deductions = up_front_deductions

        # 5) Capital Costs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        marginal_impact = limit_cnv * mi_250 * afb_line
        capital_us = marginal_impact * utils.ratio(held_capital, gross_group_cat_risk) * add_cap_req * add_group_cat_risk * 100
        ## TODO: intl capital calculation, review parameters
        cov_intl = np.where(cds.show_intl_fields, np.minimum(np.maximum(utils.ratio(afb_net_sd * sd_factor_intl, afb_net_el), 2.5), 20), 0)
        capital_intl = afb_net_el * cov_intl * 0.25
        attritional_capital = afb_net_el * attr_cap_load  
        total_capital = capital_us + capital_intl + attritional_capital
        total_coc = total_capital * roc_load

        # 6) RI Costs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        rds_regions = rds_ri_region_table["region"]

        rms_regional_entries = [[getattr(layer.rms_regional,f"{event}") for event in rds_regions] for layer in layers]
        rms_regional_entries = pd.DataFrame(rms_regional_entries, columns=rds_regions)
        rms_regional_entries = rms_regional_entries.fillna(0)
        rms_regional_entries["layer_index"] = rms_regional_entries.index
        rms_regional_entries = rms_regional_entries.melt(id_vars="layer_index", var_name = "rds_region", value_name = "rds_lol")
        rms_regional_entries["total_rds_lol"] = rms_regional_entries.groupby("layer_index")["rds_lol"].transform("sum")
        rms_regional_entries = pd.merge(rms_regional_entries, ri_cede_table, left_on="rds_region", right_on="region", how = "left")
        rms_regional_entries["ri_cost"] = utils.ratio(rms_regional_entries["rds_lol"], rms_regional_entries["total_rds_lol"]) * rms_regional_entries["ceded_per_aal"]

        rms_net_ratio = utils.ratio(afb_net_el, rms_gross_el)

        rms_net_el_for_ri_us = rms_gross_el_for_ri_us * rms_net_ratio

        ri_cost = rms_regional_entries.groupby("layer_index")["ri_cost"].sum()
        ri_cost = ri_cost * rms_net_el_for_ri_us

        # add in wf_el
        if cds.show_us_fields:
            us_wf_el = wf_gross_el * rms_net_ratio
            us_wf_ri_cost = us_wf_el * us_wf_ratio
            ri_cost += us_wf_ri_cost

        ## intl reinsurance cost, els need converting to app currency
        eu_ws_el = eu_ws_el * rms_net_ratio * layer_to_app_fx_mult
        jp_eq_el = jp_eq_el * rms_net_ratio * layer_to_app_fx_mult
        jp_ws_el = jp_ws_el * rms_net_ratio * layer_to_app_fx_mult
        can_eq_el = can_eq_el * rms_net_ratio * layer_to_app_fx_mult
        caribbean_ws_el = caribbean_ws_el * rms_net_ratio * layer_to_app_fx_mult

        intl_ri_cost = (
            eu_ws_el * eu_ws_ratio
            + jp_eq_el * jp_eq_ratio
            + jp_ws_el * jp_ws_ratio 
            + can_eq_el * can_eq_ratio
            + caribbean_ws_el * caribbean_ws_ratio
        )

        ## final sum up of ri cost
        ri_cost += intl_ri_cost

        # 7) TP Calculations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if cds.show_intl_fields:
            sd_selection = sd_factor_intl

            # create el and sd adjustment factor for japan eq (rms viewed as too penal so don't want to rely on for non-loss costs)
            japan_eq_perc = utils.ratio(jp_eq_el, afb_net_el)

            air_rms_el_factor = utils.ratio(air_gross_el - rms_gross_el, rms_gross_el)
            air_rms_sd_factor = utils.ratio(air_gross_sd - rms_gross_sd, rms_gross_sd)

            air_rms_el_factor *= japan_eq_perc
            air_rms_sd_factor *= japan_eq_perc

            tp_calc_1_jp_eq_adj = np.where(afb_net_el > 0,  utils.ratio((afb_net_el * (1 + air_rms_el_factor)) * (1 + lae_load) + total_coc + ri_cost + indirect_expenses, 1 - direct_expenses_load + inv_income_load), 0)
            tp_calc_2_jp_eq_adj = np.where(afb_net_el > 0, utils.ratio((afb_net_el * (1 + air_rms_el_factor) * (1 + lae_load)) + indirect_expenses + (afb_net_sd * (1 + air_rms_sd_factor) * sd_selection), 1 - direct_expenses_load), 0)
            tp_calc_3_jp_eq_adj = np.where(afb_net_el > 0, utils.ratio(afb_net_el * (1 + air_rms_el_factor) * (1 + lae_load), maxlr), 0)

            tp_jp_eq_adj_max = np.maximum(tp_calc_1_jp_eq_adj, tp_calc_2_jp_eq_adj)
            tp_jp_eq_adj_max = np.maximum(tp_jp_eq_adj_max, tp_calc_3_jp_eq_adj)

            non_loss_1 = tp_calc_1_jp_eq_adj - (afb_net_el * (1 + air_rms_el_factor))
            non_loss_2 = tp_calc_2_jp_eq_adj - (afb_net_el * (1 + air_rms_el_factor))
            non_loss_3 = tp_calc_3_jp_eq_adj - (afb_net_el * (1 + air_rms_el_factor))

            tp_calc_1 = afb_net_el + non_loss_1
            tp_calc_2 = afb_net_el + non_loss_2
            tp_calc_3 = afb_net_el + non_loss_3

            tp_max = np.maximum(tp_calc_1, tp_calc_2)
            tp_max = np.maximum(tp_max, tp_calc_3)

            conditions = [(tp_calc_1 == tp_max) & (tp_max > 0), (tp_calc_2 == tp_max)  & (tp_max > 0), (tp_calc_3 == tp_max)  & (tp_max > 0)]
            choices = ["Calculation 1", "Calculation 2", "Calculation 3"]
            tp_max_calculation = np.select(conditions, choices, default = "")
            tp_non_loss_cost = tp_max - afb_net_el
            rol_rms = utils.ratio(utils.ratio(tp_max, 1 - rol_calc_deductions), limit_cnv * afb_line)

            # 8) Expenses and non-loss cost loads ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            ### indirect expenses done upon load and currency conversion as done at top
            ## for intl, we need to use tp_calc_3_jp_eq_adj for tp components
            inv_income = np.where(tp_max_calculation == "Calculation 1", tp_jp_eq_adj_max * inv_income_load, 0)
            direct_expenses = np.where(tp_max_calculation == "Calculation 3", (comb_ratio - maxlr) * tp_jp_eq_adj_max, direct_expenses_load * tp_jp_eq_adj_max)
            lae = afb_net_el * (1 + air_rms_el_factor) * lae_load
            total_expenses = indirect_expenses + direct_expenses + lae

            expenses_less_inv_income = total_expenses - inv_income

            sd_load = np.maximum(tp_calc_2 - afb_net_el - total_expenses, 0)
            calc_3_lr_load = np.maximum(tp_calc_3 - afb_net_el, 0)

        else: 
            sd_selection = sd_factor_us

            tp_calc_1 = np.where(afb_net_el > 0,  utils.ratio((afb_net_el * (1 + lae_load)) + total_coc + ri_cost + indirect_expenses, 1 - direct_expenses_load + inv_income_load), 0)
            tp_calc_2 = np.where(afb_net_el > 0, utils.ratio((afb_net_el * (1 + lae_load)) + indirect_expenses + (afb_net_sd * sd_selection), 1 - direct_expenses_load), 0)
            tp_calc_3 = np.where(afb_net_el > 0, utils.ratio(afb_net_el * (1 + lae_load), maxlr), 0)

            tp_max = np.maximum(tp_calc_1, tp_calc_2)
            tp_max = np.maximum(tp_max, tp_calc_3)

            conditions = [(tp_calc_1 == tp_max) & (tp_max > 0), (tp_calc_2 == tp_max)  & (tp_max > 0), (tp_calc_3 == tp_max)  & (tp_max > 0)]
            choices = ["Calculation 1", "Calculation 2", "Calculation 3"]
            tp_max_calculation = np.select(conditions, choices, default = "")
            tp_non_loss_cost = tp_max - afb_net_el
            rol_rms = utils.ratio(utils.ratio(tp_max, 1 - rol_calc_deductions), limit_cnv * afb_line)

            # 8) Expenses and non-loss cost loads ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            ### indirect expenses done upon load and currency conversion as done at top
            inv_income = np.where(tp_max_calculation == "Calculation 1", tp_max * inv_income_load, 0)
            direct_expenses = np.where(tp_max_calculation == "Calculation 3", (comb_ratio - maxlr) * tp_max, direct_expenses_load * tp_max)
            lae = afb_net_el * lae_load
            total_expenses = indirect_expenses + direct_expenses + lae

            expenses_less_inv_income = total_expenses - inv_income

            sd_load = np.maximum(tp_calc_2 - afb_net_el - total_expenses, 0)
            calc_3_lr_load = np.maximum(tp_calc_3 - afb_net_el, 0)

        # 9) Calc EL, TP, ROL and LOL for remaining 3 methods ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        method_el = [ivor_gross_el, air_gross_el, burn_gross_el]
        method_sd = [ivor_gross_sd, air_gross_sd, burn_gross_sd]

        afb_net_results = net_el_func(False, method_el, method_sd, limit_cnv, aad_cnv, number_reins, reins_perc, reins_cov_table, override_limit_factor, bs_load, afb_line, cds.show_cat_work_comp_input)
        afb_net_el_results = afb_net_results[0]
        afb_net_sd_results = afb_net_results[1]

        ## ivor
        ivor_afb_net_el = afb_net_el_results[0]
        ivor_afb_net_sd = afb_net_sd_results[0]
        ivor_tp_final = np.where(ivor_afb_net_el > 0, ivor_afb_net_el + tp_non_loss_cost, 0)
        ## calc 3 method agnostic add in
        ivor_tp_final = np.maximum(ivor_tp_final, utils.ratio(ivor_afb_net_el * (1 + lae_load), maxlr))
        rol_ivor = utils.ratio(utils.ratio(ivor_tp_final, 1 - rol_calc_deductions), limit_cnv * afb_line)

        ## air
        air_afb_net_el = afb_net_el_results[1]
        air_afb_net_sd = afb_net_sd_results[1]
        air_tp_final = np.where(air_afb_net_el > 0, air_afb_net_el + tp_non_loss_cost, 0)
        ## calc 3 method agnostic add in
        air_tp_final = np.maximum(air_tp_final, utils.ratio(air_afb_net_el * (1 + lae_load), maxlr))
        rol_air = utils.ratio(utils.ratio(air_tp_final, 1 - rol_calc_deductions), limit_cnv * afb_line)

        ## burn
        if cds.experience_rating.claims_other.show_gross_fields:
            burn_afb_net_el = afb_net_el_results[2]
            burn_afb_net_sd = afb_net_sd_results[2]
        else:
            burn_net_el = common_data_dict["burn_net_el"]
            burn_net_sd = common_data_dict["burn_net_sd"]

            burn_afb_net_el = burn_net_el * (1 + bs_load) * afb_line
            burn_afb_net_sd = burn_net_sd * (1 + bs_load) * afb_line

        burn_tp_final = np.where(burn_afb_net_el > 0, burn_afb_net_el + tp_non_loss_cost, 0)
        ## calc 3 method agnostic add in
        burn_tp_final = np.maximum(burn_tp_final, utils.ratio(burn_afb_net_el * (1 + lae_load), maxlr))
        rol_burn = utils.ratio(utils.ratio(burn_tp_final, 1 - rol_calc_deductions), limit_cnv * afb_line)

        ## lol gross
        gross_lol_ivor = utils.ratio(ivor_gross_el, limit_cnv)
        gross_lol_air = utils.ratio(air_gross_el, limit_cnv)
        gross_lol_burn = utils.ratio(burn_gross_el, limit_cnv)
        gross_lol_burn_override = rol_burn_override * utils.ratio(gross_lol_rms, rol_rms)
        gross_lol_burn = np.where(gross_lol_burn_override > 0, gross_lol_burn_override, gross_lol_burn)

        ## lol net
        lol_rms = utils.ratio(afb_net_el, limit_cnv * afb_line)
        lol_ivor = utils.ratio(ivor_afb_net_el, limit_cnv * afb_line)
        lol_air = utils.ratio(air_afb_net_el, limit_cnv * afb_line)
        lol_burn = utils.ratio(burn_afb_net_el, limit_cnv * afb_line)
        lol_burn_override = rol_burn_override * utils.ratio(lol_rms, rol_rms)
        lol_burn = np.where(lol_burn_override > 0, lol_burn_override, lol_burn)

        # 10) Weighted Results ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        rol_arrays = [rol_rms, rol_ivor, rol_air, np.where(rol_burn_override > 0, rol_burn_override, rol_burn)]
        gross_lol_arrays = [gross_lol_rms, gross_lol_ivor, gross_lol_air, gross_lol_burn]
        net_lol_arrays = [lol_rms, lol_ivor, lol_air, lol_burn]
        net_el_arrays = [afb_net_el, ivor_afb_net_el, air_afb_net_el, burn_afb_net_el]
        weighting_arrays = [weighting_rms, weighting_ivor, weighting_air, weighting_burn]


        ## metrics
        rol_afb_tech = utils.ratio(
                                    np.sum(np.multiply(rol_arrays, weighting_arrays), axis = 0),
                                    np.sum(weighting_arrays, axis = 0)
        )

        gross_lol_weighted = utils.ratio(
                                        np.sum(np.multiply(gross_lol_arrays, weighting_arrays), axis = 0),
                                        np.sum(weighting_arrays, axis = 0)
        )

        lol_weighted = utils.ratio(
                                    np.sum(np.multiply(net_lol_arrays, weighting_arrays), axis = 0),
                                    np.sum(weighting_arrays, axis = 0)
        )

        weighted_el = utils.ratio(
                                    np.sum(np.multiply(net_el_arrays, weighting_arrays), axis = 0),
                                    np.sum(weighting_arrays, axis = 0)
        )
        ## since we use weighted_el for graphs, default to rms if no weighting applied
        weighted_el = np.where(weighted_el != 0, weighted_el, afb_net_el)

    #NOTE end risk / cat calc split




    ulr = utils.ratio(lol_weighted, (rol_prem_selection * (1 - rol_calc_deductions)))
    quote_adequacy = utils.ratio(rol_quote, rol_afb_tech)
    fot_adequacy = utils.ratio(rol_fot, rol_afb_tech)
    rms_adequacy = utils.ratio(rol_prem_selection, rol_rms)
    tpi = utils.ratio(rol_prem_selection, rol_afb_tech)
    roc = utils.ratio((rol_prem_selection * limit_cnv * afb_line * (1 - rol_calc_deductions)) - (lol_weighted * limit_cnv * afb_line) - total_expenses - ri_cost, total_capital)
    roc = np.where((lol_weighted == 0) | (rol_prem_selection == 0), 0, roc)
    bpi = utils.ratio(0.7, ulr)

    # 11) Break Even ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    rp_quote_break_even = utils.ratio(1, (0.7 * rol_quote * (1 - up_front_deductions)))
    rp_quote_break_even = np.nan_to_num(rp_quote_break_even, posinf = 0, neginf = 0)

    rp_fot_break_even = utils.ratio(1, (0.7 * rol_prem_selection * (1 - up_front_deductions)))
    rp_fot_break_even = np.nan_to_num(rp_fot_break_even, posinf = 0, neginf = 0)

    # 12) Attach / Exit points ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ap_selection_df = pd.DataFrame({
        "layer": range(len(rp_pml_selection)),
        "pml_selection": rp_pml_selection
    })

    peak_selection_df = pd.DataFrame({
        "layer": range(len(rp_pml_selection_peak)),
        "pml_selection": rp_pml_selection_peak
    })

    attach_df = pd.DataFrame({
        "Curve Agg": curve_agg_rp_attach,
        "RMS AP": rms_ap_attach,
        "RMS EQ": rms_eq_attach,
        "RMS WS": rms_ws_attach,
        "RMS SCS": rms_scs_attach,
        "AIR AP": air_ap_attach,
        "AIR EQ": air_eq_attach,
        "AIR WS": air_ws_attach,
        "AIR SCS": air_scs_attach,
        "AIR WF": air_wf_attach,
        "AIR Winter": air_winter_attach
    })

    exit_df = pd.DataFrame({
        "Curve Agg": curve_agg_rp_exit,
        "RMS AP": rms_ap_exit,
        "RMS EQ": rms_eq_exit,
        "RMS WS": rms_ws_exit,
        "RMS SCS": rms_scs_exit,
        "AIR AP": air_ap_exit,
        "AIR EQ": air_eq_exit,
        "AIR WS": air_ws_exit,
        "AIR SCS": air_scs_exit,
        "AIR WF": air_wf_exit,
        "AIR Winter": air_winter_exit
    })

    attach_df["layer"] = attach_df.index
    attach_df = pd.melt(attach_df, id_vars = ["layer"], var_name = "pml_selection", value_name = "attach_rp")

    exit_df["layer"] = exit_df.index
    exit_df = pd.melt(exit_df, id_vars = ["layer"], var_name = "pml_selection", value_name = "exit_rp")

    ap_selection_df = pd.merge(ap_selection_df, attach_df, how = "left", on = ["layer", "pml_selection"])
    ap_selection_df = pd.merge(ap_selection_df, exit_df, how = "left", on = ["layer", "pml_selection"])

    peak_selection_df = pd.merge(peak_selection_df, attach_df, how = "left", on = ["layer", "pml_selection"])
    peak_selection_df = pd.merge(peak_selection_df, exit_df, how = "left", on = ["layer", "pml_selection"])

    rp_attach = np.where(rp_pml_selection == "Curve Agg", curve_agg_rp_attach, 0)
    rp_exit = np.where(rp_pml_selection == "Curve Agg", curve_agg_rp_exit, 0)

    # 13) Calculations for Summary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    summary_fx_factor = ccy_conversion(pd.Series(application_ccy), summary_ccy, ccy_table)[0]

    line_written_dollar = written_line * limit_cnv
    line_estimated_dollar = estimated_signing * limit_cnv
    line_signed_dollar = signed_line * limit_cnv

    line_written_summary_fx = line_written_dollar * summary_fx_factor
    line_estimated_summary_fx = line_estimated_dollar * summary_fx_factor
    line_signed_summary_fx = line_signed_dollar * summary_fx_factor

    epi_written_summary_fx = epi_written * summary_fx_factor
    epi_estimated_summary_fx = epi_estimated * summary_fx_factor
    epi_signed_summary_fx = epi_signed * summary_fx_factor

    reinstatement_description = [
        str(x) + "@" + str(round(y * 100)) + "%/" + str(round(z * 100)) + "%/" + str(round(w * 100)) + "%"     
        for x, y, z, w in zip(number_reins, perc_reins_1, perc_reins_2, perc_reins_3) 
        ]

    mi_250_prem_ratio = utils.ratio(mi_250, rol_prem_selection * (1 - up_front_deductions))
    mi_10_prem_ratio = utils.ratio(mi_10, rol_prem_selection * (1 - up_front_deductions))

    epi_yoa = cds.epi_yoa or 0
    epi_rate = utils.ratio(prem_full_line, epi_yoa)

    # 14) Calculations for mandatory fields - Standard KPIs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    gross_quoted_premium = limit_cnv * rol_prem_selection * afb_line
    net_quoted_premium = limit_cnv * rol_prem_selection * afb_line * (1 - up_front_deductions)
    
    ## rol_afb_tech is on gross basis
    gross_technical_premium = limit_cnv * rol_afb_tech * afb_line 
    net_technical_premium = limit_cnv * rol_afb_tech * (1 - up_front_deductions) * afb_line

    gross_benchmark_premium = utils.ratio(limit_cnv * utils.ratio(lol_weighted, 0.7) * afb_line, 1 - up_front_deductions)
    net_benchmark_premium = limit_cnv * utils.ratio(lol_weighted, 0.7) * afb_line

    # 15) BI Data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    profit = cds.bi_data.profit
    
    if profit is not None:
        if profit > 0:
            cds.bi_data.break_even = "In Profit"
        else:
            prem = net_quoted_premium.sum()
            cds.bi_data.break_even = str(math.ceil(utils.ratio(abs(profit), prem))) + " Years"

    # 16) Day 2 Nodes (LY) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    limit_cnv_ly = [layer.limit_cnv_ly for layer in layers]

    rol_quote_ly = [layer.quote.rol_ly.rol_quote for layer in layers]
    rol_fot_ly = [layer.quote.rol_ly.rol_fot for layer in layers]
    prem_full_line_ly = [layer.quote.rol_ly.prem_full_line for layer in layers]

    written_line_ly = [layer.quote.rol_ly.written_line for layer in layers]
    estimated_signing_ly = [layer.quote.rol_ly.estimated_signing for layer in layers]
    signed_line_ly = [layer.quote.rol_ly.signed_line for layer in layers]

    epi_written_ly = [layer.quote.rol_ly.epi_written for layer in layers]
    epi_estimated_ly = [layer.quote.rol_ly.epi_estimated for layer in layers]
    epi_signed_ly = [layer.quote.rol_ly.epi_signed for layer in layers]
    #

    limit_cnv_ly = list_to_numpy(limit_cnv_ly, float)

    rol_quote_ly = list_to_numpy(rol_quote_ly, float)
    rol_fot_ly = list_to_numpy(rol_fot_ly, float)
    prem_full_line_ly = list_to_numpy(prem_full_line_ly, float)

    written_line_ly = list_to_numpy(written_line_ly, float)
    estimated_signing_ly = list_to_numpy(estimated_signing_ly, float)
    signed_line_ly = list_to_numpy(signed_line_ly, float)

    epi_written_ly = list_to_numpy(epi_written_ly, float)
    epi_estimated_ly = list_to_numpy(epi_estimated_ly, float)
    epi_signed_ly = list_to_numpy(epi_signed_ly, float)
    #

    line_written_dollar_ly = written_line_ly * limit_cnv_ly
    line_estimated_dollar_ly = estimated_signing_ly * limit_cnv_ly
    line_signed_dollar_ly = signed_line_ly * limit_cnv_ly
    #

    ## total
    cds.quote.rol_ly.rol_quote = (limit_cnv_ly * rol_quote_ly).sum()
    cds.quote.rol_ly.rol_fot = (limit_cnv_ly * rol_fot_ly).sum()

    cds.quote.rol_ly.prem_full_line = prem_full_line_ly.sum()

    cds.quote.rol_ly.written_line_dollar = line_written_dollar_ly.sum()
    cds.quote.rol_ly.estimated_signing_dollar = line_estimated_dollar_ly.sum()
    cds.quote.rol_ly.signed_line_dollar = line_signed_dollar_ly.sum()

    cds.quote.rol_ly.epi_written = epi_written_ly.sum()
    cds.quote.rol_ly.epi_estimated = epi_estimated_ly.sum()
    cds.quote.rol_ly.epi_signed = epi_signed_ly.sum()

    ## total usd
    cds.quote_total_usd.quote.rol_ly.rol_quote = (limit_cnv_ly * rol_quote_ly).sum() / ccy_from_usd
    cds.quote_total_usd.quote.rol_ly.rol_fot = (limit_cnv_ly * rol_fot_ly).sum() / ccy_from_usd

    cds.quote_total_usd.quote.rol_ly.prem_full_line = prem_full_line_ly.sum() / ccy_from_usd

    cds.quote_total_usd.quote.rol_ly.written_line_dollar = line_written_dollar_ly.sum() / ccy_from_usd
    cds.quote_total_usd.quote.rol_ly.estimated_signing_dollar = line_estimated_dollar_ly.sum() / ccy_from_usd
    cds.quote_total_usd.quote.rol_ly.signed_line_dollar = line_signed_dollar_ly.sum() / ccy_from_usd

    cds.quote_total_usd.quote.rol_ly.epi_written = epi_written_ly.sum() / ccy_from_usd
    cds.quote_total_usd.quote.rol_ly.epi_estimated = epi_estimated_ly.sum() / ccy_from_usd
    cds.quote_total_usd.quote.rol_ly.epi_signed = epi_signed_ly.sum() / ccy_from_usd
    #
    for index, layer in enumerate(layers):

        ## premium and line
        layer.quote.rol_ly.written_line_dollar = line_written_dollar_ly[index]
        layer.quote.rol_ly.estimated_signing_dollar = line_estimated_dollar_ly[index]
        layer.quote.rol_ly.signed_line_dollar = line_signed_dollar_ly[index]
    

    # 17) Write back to hxd ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    line_weight = limit_cnv * afb_line_for_totals * summary_fx_factor
    epi_weight = limit_cnv * afb_line_for_totals * rol_prem_selection * (1 - up_front_deductions) * summary_fx_factor

    common_data_dict["epi_weight"] = epi_weight

    ## quote totals
    cds.quote.rol_ty.ulr = utils.ratio((epi_weight * ulr).sum(), epi_weight[ulr > 0].sum())
    cds.quote.rol_ty.tpi = utils.ratio(epi_weight[tpi > 0].sum(), utils.ratio(epi_weight, tpi).sum())
    cds.quote.rol_ty.bpi = utils.ratio(epi_weight[bpi > 0].sum(), utils.ratio(epi_weight, bpi).sum())
    cds.quote.rol_ty.roc = utils.ratio((total_capital[epi_weight > 0] * roc[epi_weight > 0]).sum(), total_capital[(roc > 0) & (epi_weight > 0)].sum())

    cds.quote.rol_ty.quote_adequacy = utils.ratio(epi_weight[quote_adequacy > 0].sum(), utils.ratio(epi_weight, quote_adequacy).sum())
    cds.quote.rol_ty.fot_adequacy = utils.ratio(epi_weight[fot_adequacy > 0].sum(), utils.ratio(epi_weight, fot_adequacy).sum())

    cds.quote.rol_ty.rol_quote = (limit_cnv * rol_quote).sum()
    cds.quote.rol_ty.rol_fot = (limit_cnv * rol_fot).sum()

    cds.quote.rol_ty.prem_full_line = prem_full_line.sum()

    cds.quote.rol_ty.written_line_dollar = line_written_dollar.sum()
    cds.quote.rol_ty.estimated_signing_dollar = line_estimated_dollar.sum()
    cds.quote.rol_ty.signed_line_dollar = line_signed_dollar.sum()

    cds.quote.rol_ty.epi_written = epi_written.sum()
    cds.quote.rol_ty.epi_estimated = epi_estimated.sum()
    cds.quote.rol_ty.epi_signed = epi_signed.sum()

    ### usd totals
    cds.quote_total_usd.quote.rol_ty.rol_quote = (limit_cnv * rol_quote).sum() / ccy_from_usd
    cds.quote_total_usd.quote.rol_ty.rol_fot = (limit_cnv * rol_fot).sum() / ccy_from_usd

    cds.quote_total_usd.quote.rol_ty.prem_full_line = prem_full_line.sum() / ccy_from_usd

    cds.quote_total_usd.quote.rol_ty.written_line_dollar = line_written_dollar.sum() / ccy_from_usd
    cds.quote_total_usd.quote.rol_ty.estimated_signing_dollar = line_estimated_dollar.sum() / ccy_from_usd
    cds.quote_total_usd.quote.rol_ty.signed_line_dollar = line_signed_dollar.sum() / ccy_from_usd

    cds.quote_total_usd.quote.rol_ty.epi_written = epi_written.sum() / ccy_from_usd
    cds.quote_total_usd.quote.rol_ty.epi_estimated = epi_estimated.sum() / ccy_from_usd
    cds.quote_total_usd.quote.rol_ty.epi_signed = epi_signed.sum() / ccy_from_usd

    ## summary totals
    cds.summary.ty.rol_quote = cds.quote.rol_ty.rol_quote
    cds.summary.ty.rol_fot = cds.quote.rol_ty.rol_fot

    cds.summary.ty.bpi = utils.ratio(epi_weight[bpi > 0].sum(), utils.ratio(epi_weight, bpi).sum())
    cds.summary.ty.fot_adequacy = utils.ratio(epi_weight[fot_adequacy > 0].sum(), utils.ratio(epi_weight, fot_adequacy).sum())
    cds.summary.ty.rms_adequacy = utils.ratio(epi_weight[rms_adequacy > 0].sum(), utils.ratio(epi_weight, rms_adequacy).sum())
    cds.summary.ty.ulr = utils.ratio((epi_weight * ulr).sum(), epi_weight[ulr > 0].sum())
    cds.summary.ty.epi_adj_rate = utils.ratio(prem_full_line.sum(), epi_yoa)
    cds.summary.ty.prem_full_line = prem_full_line.sum()
    
    cds.summary.ty.line_written_summary_fx = line_written_summary_fx.sum()
    cds.summary.ty.line_estimated_summary_fx = line_estimated_summary_fx.sum()
    cds.summary.ty.line_signed_summary_fx = line_signed_summary_fx.sum()

    cds.summary.ty.epi_written_summary_fx = epi_written_summary_fx.sum()
    cds.summary.ty.epi_estimated_summary_fx = epi_estimated_summary_fx.sum()
    cds.summary.ty.epi_signed_summary_fx = epi_signed_summary_fx.sum()

    cds.summary.ty.mi_250 = (mi_250 * line_weight).sum()
    cds.summary.ty.mi_250_prem_ratio = utils.ratio((mi_250 * line_weight).sum(), epi_weight[mi_250 > 0].sum())

    cds.summary.ty.mi_10 = (mi_10 * line_weight).sum()
    cds.summary.ty.mi_10_prem_ratio = utils.ratio((mi_10 * line_weight).sum(), epi_weight[mi_10 > 0].sum())

    ## layer fields
    for index, layer in enumerate(layers):

        ## premium and line
        layer.quote.rol_ty.written_line_dollar = line_written_dollar[index]
        layer.quote.rol_ty.estimated_signing_dollar = line_estimated_dollar[index]
        layer.quote.rol_ty.signed_line_dollar = line_signed_dollar[index]

        layer.quote.rol_ty.quote_fot_ratio = quote_fot_ratio[index]
        layer.quote.rol_ty.prem_full_line = prem_full_line[index]
        layer.quote.rol_ty.epi_written = epi_written[index]
        layer.quote.rol_ty.epi_estimated = epi_estimated[index]
        layer.quote.rol_ty.epi_signed = epi_signed[index]

        layer.quote.rol_ty.est_sign_written_ratio = est_sign_written_ratio[index]

        ## expected loss
        if not is_risk_xl:
            layer.quote.rms_tp_calc.gross_lol = gross_lol_rms[index]
            layer.quote.rms_tp_calc.gross_el = rms_gross_el[index]
            layer.quote.rms_tp_calc.gross_sd = rms_gross_sd[index]
            layer.quote.rms_tp_calc.model_limit_factor = model_limit_factor[index]
            layer.quote.rms_tp_calc.net_el_excl_reins_prem = net_el_excl_reins_prem[index]
            layer.quote.rms_tp_calc.no_expected_reins = exp_reins_cost[index]
            layer.quote.rms_tp_calc.net_el = net_el[index]
            layer.quote.rms_tp_calc.net_sd = net_sd[index]
            layer.quote.rms_tp_calc.net_el_incl_bs = net_el_incl_bs[index]
            layer.quote.rms_tp_calc.net_sd_incl_bs = net_sd_incl_bs[index]
            layer.quote.rms_tp_calc.afb_net_el = afb_net_el[index]
            layer.quote.rms_tp_calc.afb_net_sd = afb_net_sd[index]

            ## expenses
            layer.quote.rms_tp_calc.indirect_expenses = indirect_expenses
            layer.quote.rms_tp_calc.direct_expenses = direct_expenses[index]
            layer.quote.rms_tp_calc.lae = lae[index]
            layer.quote.rms_tp_calc.total_expenses = total_expenses[index]

            ## capital
            layer.quote.rms_tp_calc.mi_250 = mi_250[index]
            layer.quote.rms_tp_calc.marginal_impact = marginal_impact[index]
            layer.quote.rms_tp_calc.capital_us = capital_us[index]
            layer.quote.rms_tp_calc.capital_intl = capital_intl[index]
            layer.quote.rms_tp_calc.attritional_capital = attritional_capital[index]
            layer.quote.rms_tp_calc.total_capital = total_capital[index]
            layer.quote.rms_tp_calc.total_coc = total_coc[index]

            ## ri cost
            layer.quote.rms_tp_calc.ri_cost = ri_cost[index]

            ## rms tp calcs
            layer.quote.rms_tp_calc.tp_calc_1 = tp_calc_1[index]
            layer.quote.rms_tp_calc.tp_calc_2 = tp_calc_2[index]
            layer.quote.rms_tp_calc.tp_calc_3 = tp_calc_3[index]
            layer.quote.rms_tp_calc.tp_max_calculation = tp_max_calculation[index]
            layer.quote.rms_tp_calc.tp_non_loss_cost = tp_non_loss_cost[index]
            layer.quote.rms_tp_calc.tp_final = tp_max[index]

            ## non loss costs
            layer.quote.rms_tp_calc.sd_load = sd_load[index]
            layer.quote.rms_tp_calc.calc_3_lr_load = calc_3_lr_load[index]
            layer.quote.rms_tp_calc.expenses_less_inv_income = expenses_less_inv_income[index]        

            ## other tp calcs
            layer.quote.ivor_tp_calc.afb_net_el = ivor_afb_net_el[index]
            layer.quote.ivor_tp_calc.afb_net_sd = ivor_afb_net_sd[index]
            layer.quote.ivor_tp_calc.tp_final = ivor_tp_final[index]

            layer.quote.air_tp_calc.afb_net_el = air_afb_net_el[index]
            layer.quote.air_tp_calc.afb_net_sd = air_afb_net_sd[index]
            layer.quote.air_tp_calc.tp_final = air_tp_final[index]

            layer.quote.burn_tp_calc.afb_net_el = burn_afb_net_el[index]
            layer.quote.burn_tp_calc.afb_net_sd = burn_afb_net_sd[index]
            layer.quote.burn_tp_calc.tp_final = burn_tp_final[index]

            ## rol and lol
            layer.quote.rol_ty.rol_rms = rol_rms[index]
            layer.quote.rol_ty.rol_ivor = rol_ivor[index]
            layer.quote.rol_ty.rol_air = rol_air[index]        
            layer.quote.rol_ty.rol_burn = rol_burn[index]

            layer.quote.rol_ty.lol_rms = lol_rms[index]
            layer.quote.rol_ty.lol_ivor = lol_ivor[index]
            layer.quote.rol_ty.lol_air = lol_air[index]        
            layer.quote.rol_ty.lol_burn = lol_burn[index]
        else:
            layer.quote.rol_ty.risk_xl_rol_exposure = rol_exposure[index]
            layer.quote.rol_ty.rol_burn = rol_burn[index]

            layer.quote.rol_ty.risk_xl_lol_exposure = lol_exposure[index]
            layer.quote.rol_ty.lol_burn = lol_burn[index]

            layer.quote.rol_ty.tp_calc_1_burn = tp_calc_1_burn[index]
            layer.quote.rol_ty.tp_calc_2_burn = tp_calc_2_burn[index]
            layer.quote.rol_ty.tp_calc_3_burn = tp_calc_3_burn[index]
            layer.quote.rol_ty.tp_final_burn = tp_max_burn[index]

            layer.quote.rol_ty.tp_calc_1_exposure = tp_calc_1_exposure[index]
            layer.quote.rol_ty.tp_calc_2_exposure = tp_calc_2_exposure[index]
            layer.quote.rol_ty.tp_calc_3_exposure = tp_calc_3_exposure[index]
            layer.quote.rol_ty.tp_final_exposure = tp_max_exposure[index]

            layer.quote.rol_ty.roev = utils.ratio(prem_full_line[index], layer.quote.rol_ty.layer_exposure)


        ## weighted results
        layer.quote.rol_ty.rol_afb_tech = rol_afb_tech[index]
        layer.quote.rol_ty.tpi = tpi[index]
        layer.quote.rol_ty.roc = roc[index]
        layer.quote.rol_ty.ulr = ulr[index]
        layer.quote.rol_ty.bpi = bpi[index]
        layer.quote.rol_ty.quote_adequacy = quote_adequacy[index]
        layer.quote.rol_ty.fot_adequacy = fot_adequacy[index]
        layer.quote.rol_ty.rms_adequacy = rms_adequacy[index]
        layer.quote.rol_ty.lol_weighted = lol_weighted[index]
        layer.quote.rol_ty.weighted_el = weighted_el[index]
        layer.quote.rol_ty.gross_lol_weighted = gross_lol_weighted[index]

        ## break even and attach/exit points
        layer.quote.rol_ty.rp_quote_break_even = rp_quote_break_even[index]
        layer.quote.rol_ty.rp_fot_break_even = rp_fot_break_even[index]

        layer.quote.rol_ty.rp_attach = ap_selection_df["attach_rp"][index]
        layer.quote.rol_ty.rp_exit = ap_selection_df["exit_rp"][index]

        layer.quote.rol_ty.rp_attach_peak = peak_selection_df["attach_rp"][index]
        layer.quote.rol_ty.rp_exit_peak = peak_selection_df["exit_rp"][index]
        
        ## summary
        layer.summary.ty.reinstatement_description = reinstatement_description[index]

        layer.summary.ty.rol_quote = rol_quote[index]
        layer.summary.ty.rol_fot = rol_fot[index]

        layer.summary.ty.bpi = bpi[index]
        layer.summary.ty.fot_adequacy = fot_adequacy[index]
        layer.summary.ty.rms_adequacy = rms_adequacy[index]
        layer.summary.ty.ulr = ulr[index]
        layer.summary.ty.epi_adj_rate = epi_rate[index]
        layer.summary.ty.prem_full_line = prem_full_line[index]

        layer.summary.ty.line_written_summary_fx = line_written_summary_fx[index]
        layer.summary.ty.line_estimated_summary_fx = line_estimated_summary_fx[index]
        layer.summary.ty.line_signed_summary_fx = line_signed_summary_fx[index]

        layer.summary.ty.epi_written_summary_fx = epi_written_summary_fx[index]
        layer.summary.ty.epi_estimated_summary_fx = epi_estimated_summary_fx[index]
        layer.summary.ty.epi_signed_summary_fx = epi_signed_summary_fx[index]

        layer.summary.ty.mi_250 = mi_250[index]
        layer.summary.ty.mi_10 = mi_10[index]

        layer.summary.ty.mi_250_prem_ratio = mi_250_prem_ratio[index]
        layer.summary.ty.mi_10_prem_ratio = mi_10_prem_ratio[index]
        

        ## mandatory fields - Standard KPIs, going in order of data schema static
        layer.brokerage = brokerage[index]
        layer.written_line = afb_line[index]

        layer.benchmark_premium = gross_benchmark_premium[index]
        layer.bpi = bpi[index]
        layer.bpi_pre_uw_adj = bpi[index]
        ## model_premium NA
        ## unity_premium NA
        layer.quoted_premium = gross_quoted_premium[index]
        layer.technical_premium = gross_technical_premium[index]
        layer.technical_premium_pre_uw_adj = gross_technical_premium[index]
        layer.technical_premium_net = net_technical_premium[index]
        layer.tpi = tpi[index]
        layer.tpi_pre_uw_adj = tpi[index]    
        ## pflr_att NA
        ## pflr_cat NA  
        layer.pflr = ulr[index]
        layer.roc = roc[index]
        layer.uw_adj_impact = 0
        ## trifocus NA
        layer.expected_loss_cost = weighted_el[index]
        layer.expected_loss_cost_pre_uw_adj = weighted_el[index]
        ## expected_loss_cost_100 NA
        layer.quoted_premium_net = net_quoted_premium[index]
        ## quoted_premium_net_100 NA
        ## quoted_premium_100 NA
        ## quoted_premium_annual NA
        ## quoted_premium_annual_100 NA
        layer.benchmark_premium_net = net_benchmark_premium[index]
        ## benchmark_premium_net_100 NA
        ## benchmark_premium_100 NA
        ## benchmark_premium_annual NA
        ## benchmark_premium_annual_100 NA
        layer.benchmark_premium_pre_uw_adj = gross_benchmark_premium[index]
        ## technical_premium_100 NA
        ## technical_premium_net_100 NA
        layer.pflr_pre_uw_adj = ulr[index]



    ## TP notes
    cds.quote.tp_calc_info.description.general_notes = """Technical Premium = EL + Non-Loss Costs (varies by calc). EL component weighted between methods. Non-Loss component solely uses RMS as the EL base."""
    cds.quote.tp_calc_info.description.default_line = """If no written, estimated, or signed line is entered, a default line of 5% will be used for the TP calc."""

    cds.quote.tp_calc_info.description.tp_calc_1 = """Capital intensive:  EL + Expenses (Fixed, Variable and LAE) + Capital Cost + RI Cost - Inv. Income."""
    cds.quote.tp_calc_info.description.tp_calc_2 = """Volatile but low capital:  EL + Expenses (Fixed, Variable and LAE) + SD Load (12% US, 7.5% Intl.)."""
    cds.quote.tp_calc_info.description.tp_calc_3 = """Max LR acceptable:  (EL + LAE) / Max LR (0.8)."""

    cds.quote.tp_calc_info.description.lae = """Loss adjustment expenses applied to RMS EL for all 3 TP calcs."""
    cds.quote.tp_calc_info.description.indirect_expenses = """Fixed cost applied to TP calcs 1 & 2."""
    cds.quote.tp_calc_info.description.direct_expenses = """Variable cost applied to TP calcs 1 & 2."""
    cds.quote.tp_calc_info.description.inv_income = """Investment income applies for TP calc 1 only, reducing the price."""

    cds.quote.tp_calc_info.description.ri_cost = """Reinsurance loads are applied to RMS WS/EQ EL in peak cat regions (see table below). US has an additional load applied to NMP WF EL."""
    cds.quote.tp_calc_info.description.capital_alloc = """Capital is allocated to layers either using 1 in 250 MI (US) or RMS SD (Intl.). Therefore (for US), capital will vary depending on the correlation with the overall P+T portfolio."""
    cds.quote.tp_calc_info.description.roc = """TP calc 1 is calibrated such that achieving a 100% TPI (adequacy) yields a 15% return on allocated capital."""
    cds.quote.tp_calc_info.description.sd_load = """TP calc 2 SD factor applied to RMS SD."""

    cds.quote.tp_calc_info.value.lae = f"{lae_load:.2%} of RMS EL."
    cds.quote.tp_calc_info.value.indirect_expenses = f"{indirect_expenses:.0f} {application_ccy}."
    cds.quote.tp_calc_info.value.direct_expenses = f"{direct_expenses_load:.2%} of RMS TP."   
    cds.quote.tp_calc_info.value.inv_income = f"{inv_income_load:.2%} of RMS TP."
    cds.quote.tp_calc_info.value.roc = """15% of allocated capital."""
    cds.quote.tp_calc_info.value.sd_load = f"{sd_factor_us:.1%} (US) or {sd_factor_intl:.1%} (Intl.) of RMS SD."

    cds.quote.tp_calc_info.value_ly.lae = f"{lae_load_ly:.2%} of RMS EL."
    cds.quote.tp_calc_info.value_ly.indirect_expenses = f"{indirect_expenses_ly:.0f} {application_ccy}."
    cds.quote.tp_calc_info.value_ly.direct_expenses = f"{direct_expenses_load_ly:.2%} of RMS TP."   
    cds.quote.tp_calc_info.value_ly.inv_income = f"{inv_income_load_ly:.2%} of RMS TP."
    cds.quote.tp_calc_info.value_ly.roc = """15% of allocated capital."""
    cds.quote.tp_calc_info.value_ly.sd_load = f"{sd_factor_us_ly:.1%} (US) or {sd_factor_intl_ly:.1%} (Intl.) of RMS SD."

    ## RI Loads
    for region in ri_cede_table["region"]:
        setattr(cds.quote.tp_calc_info.ri_cost_ty, f"{region}", ty_ri_cede_dict[f"{region}_ratio"])
        setattr(cds.quote.tp_calc_info.ri_cost_ly, f"{region}", ly_ri_cede_dict[f"{region}_ratio"])

        setattr(cds.quote.tp_calc_info.mvt, f"{region}", utils.ratio(ty_ri_cede_dict[f"{region}_ratio"] - ly_ri_cede_dict[f"{region}_ratio"], ly_ri_cede_dict[f"{region}_ratio"]))


    return common_data_dict
        
