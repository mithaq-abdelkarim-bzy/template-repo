import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import policy_term
import algorithms.rate_utilities as utils
from operator import itemgetter
from algorithms.udf import ccy_conversion, list_to_numpy


def rate_risk_information(hxd):
        
    # set dataframe variables for cleaner code 
    cds = hxd.cds
    layers = cds.layers
    params = hx.params

    # Extracts database id for the risk information tab
    cds.policy_option_id = hx.meta.policy_option_id
    # cds.rating_factors.policy_term = policy_term(hxd.hx_core.inception_date, hxd.hx_core.expiry_date)

    # Set rating methodology
    cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == 'Case Priced'
    cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == 'Rater'

    # 1) Load input values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    application_ccy = cds.currency

    limit = [layer.limit for layer in layers]
    excess = [layer.excess for layer in layers]
    aggregate_deductible = [layer.aggregate_deductible for layer in layers]
    risk_xl_occurrence_limit = [layer.risk_xl_occurrence_limit for layer in layers]
    layer_ccy = [layer.currency for layer in layers]

    number_reins = [layer.number_reins for layer in layers]
    perc_reins_1 = [layer.perc_reins_1 for layer in layers]
    perc_reins_2 = [layer.perc_reins_2 for layer in layers]
    perc_reins_3 = [layer.perc_reins_3 for layer in layers]

    is_facility = [layer.is_facility for layer in layers]

    limit = list_to_numpy(limit, float)
    excess = list_to_numpy(excess, float)
    aggregate_deductible = list_to_numpy(aggregate_deductible, float)
    risk_xl_occurrence_limit = list_to_numpy(risk_xl_occurrence_limit, float)
    layer_ccy = list_to_numpy(layer_ccy, str)

    number_reins = list_to_numpy(number_reins, int)
    perc_reins_1 = list_to_numpy(perc_reins_1, float)
    perc_reins_2 = list_to_numpy(perc_reins_2, float)
    perc_reins_3 = list_to_numpy(perc_reins_3, float)

    is_facility = list_to_numpy(is_facility, int)

    # 2) Show / Hides ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    cds.show_intl_fields = False if cds.calc_type == "US" else True
    cds.show_us_fields = not cds.show_intl_fields
    cds.show_us_exposure_fields = True if (cds.show_us_fields or cds.includes_us_exposure) else False
    cds.show_perc_us_el = True if (cds.show_intl_fields and cds.includes_us_exposure) else False

    cds.show_multi_year = True if cds.multi_year == "Yes" else False
    cds.show_declined_reasons = True if cds.deal_status == "Declined" else False
    cds.show_cat_work_comp_input = True if cds.programme in ["Cat XL", "Workers Comp", "Risk XL"] else False
    cds.show_agg_qs_input = not cds.show_cat_work_comp_input

    cds.show_ceding_commission = True if cds.programme == "QS" else False

    show_risk_xl = True if cds.programme == "Risk XL" else False
    show_non_risk_xl = not show_risk_xl

    cds.show_risk_xl = show_risk_xl and hxd.model_state.show_after_landing_page
    cds.show_non_risk_xl = show_non_risk_xl and hxd.model_state.show_after_landing_page
    
    ## Rate change show hide
    cds.show_cat_rate_change = True if cds.programme == "Cat XL" else False
    ## below also used when cat XL but also model change
    use_cat_approx_rate_change = True if (cds.programme == "Cat XL") else False # this means using curve agg methodology
    cds.show_other_programme_rate_change = not use_cat_approx_rate_change # this means using change in ULR

    cds.show_case_priced = hxd.cds.standard_fields.rating_methodology == 'Case Priced'
    cds.show_aad_cnv_field = cds.show_intl_fields * cds.show_cat_work_comp_input

    cds.show_bermuda = True if cds.risk_carrier == "Bermuda" else False

    # 3) Currency Conversion ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    cds.limit_application_ccy_label = f"Limit in {cds.currency}"
    cds.excess_application_ccy_label = f"Excess in {cds.currency}"
    cds.aggregate_deductible_application_ccy_label = f"AAD in {cds.currency}"

    layer_to_app_fx_mult = ccy_conversion(layer_ccy, application_ccy, params.table_currency)

    limit_cnv = limit * layer_to_app_fx_mult
    excess_cnv = excess * layer_to_app_fx_mult
    aggregate_deductible_cnv = aggregate_deductible * layer_to_app_fx_mult

    risk_xl_occurrence_limit_cnv = risk_xl_occurrence_limit * layer_to_app_fx_mult

    layer_structure = [str(round(x/1e6, 1)) + "m xs " + str(round(y/1e6, 1)) + "m" if x > 0 else "" for x, y in zip(limit_cnv, excess_cnv)]

    # 4) Brokerage ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    effective_brokerage = np.where(is_facility, (cds.brokerage or 0) + 0.025, cds.brokerage or 0)


    # 5) Write back to hxd ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    cds.layer_totals.limit = limit.sum()

    for index, layer in enumerate(layers):
        layer.limit_cnv = limit_cnv[index]
        layer.excess_cnv = excess_cnv[index]
        layer.aggregate_deductible_cnv = aggregate_deductible_cnv[index]
        layer.risk_xl_occurrence_limit_cnv = risk_xl_occurrence_limit_cnv[index]
        layer.layer_structure = layer_structure[index]

        layer.layer_index = index + 1

        layer.effective_brokerage = effective_brokerage[index]

    # 6) Create input dictionary to carry throughout model ~~~~~~~~~~~~~~~~~~
    common_data_dict = {
        "limit": limit,
        "excess": excess,
        "limit_cnv": limit_cnv,
        "excess_cnv": excess_cnv,
        "aad_cnv": aggregate_deductible_cnv,
        "risk_xl_occurrence_limit_cnv": risk_xl_occurrence_limit_cnv,
        "number_reins": number_reins,
        "perc_reins_1": perc_reins_1,
        "perc_reins_2": perc_reins_2,
        "perc_reins_3": perc_reins_3,
        "application_ccy": application_ccy,
        "layer_ccy": layer_ccy,
        "layer_to_app_fx_mult": layer_to_app_fx_mult,
        "effective_brokerage": effective_brokerage
    }

    return common_data_dict
