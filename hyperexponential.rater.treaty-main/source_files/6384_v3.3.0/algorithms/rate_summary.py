import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import policy_term
from operator import itemgetter
from algorithms.udf import ccy_conversion, list_to_numpy
from hx import params as hx_params
import algorithms.rate_utilities as utils

ccy_table = hx_params.table_currency
uwa_table = hx_params.table_underwriter_authority

def rate_summary(hxd, common_data_dict):

    # set dataframe variables for cleaner code 
    cds = hxd.cds
    layers = cds.layers

    # 2) Load input values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    programme = cds.programme
    underwriter = cds.standard_fields.underwriter
    is_renewal = cds.standard_fields.is_renewal

    application_ccy = common_data_dict["application_ccy"]
    summary_ccy = cds.currency_policy_financials
    
    multi_year_period = [layer.summary.ty.multi_year_period for layer in layers]
    pol_ref = [layer.section_reference for layer in layers]

    ## ly
    ly_current_year_section_reference = [layer.summary.ly.current_year_section_reference for layer in layers]
    ly_current_year_share = [layer.summary.ly.current_year_share for layer in layers]
    ly_current_year_share = [1 if x is None else x for x in ly_current_year_share]
    ly_mi_250 = [layer.summary.ly.mi_250 for layer in layers]
    ly_mi_10 = [layer.summary.ly.mi_10 for layer in layers]
    ly_limit_cnv = [layer.limit_cnv_ly for layer in layers]

    ly_written_line = [layer.quote.rol_ly.written_line for layer in layers]
    ly_estimated_signing = [layer.quote.rol_ly.estimated_signing for layer in layers]
    ly_signed_line = [layer.quote.rol_ly.signed_line for layer in layers]

    ly_epi_written = [layer.quote.rol_ly.epi_written for layer in layers]
    ly_epi_estimated = [layer.quote.rol_ly.epi_estimated for layer in layers]
    ly_epi_signed = [layer.quote.rol_ly.epi_signed for layer in layers]

    # convert to arrays
    ly_current_year_section_reference = list_to_numpy(ly_current_year_section_reference, str)
    ly_current_year_share = list_to_numpy(ly_current_year_share, float)
    ly_mi_250 = list_to_numpy(ly_mi_250, float)
    ly_mi_10 = list_to_numpy(ly_mi_10, float)

    ly_limit_cnv = list_to_numpy(ly_limit_cnv, float)

    ly_written_line = list_to_numpy(ly_written_line, float)
    ly_estimated_signing = list_to_numpy(ly_estimated_signing, float)
    ly_signed_line = list_to_numpy(ly_signed_line, float)

    ly_epi_written = list_to_numpy(ly_epi_written, float)
    ly_epi_estimated = list_to_numpy(ly_epi_estimated, float)
    ly_epi_signed = list_to_numpy(ly_epi_signed, float)

    ## year_before_last
    ybl_current_year_section_reference = [layer.summary.year_before_last.current_year_section_reference for layer in layers]
    ybl_current_year_share = [layer.summary.year_before_last.current_year_share for layer in layers]
    ybl_current_year_share = [1 if x is None else x for x in ybl_current_year_share]
    ybl_mi_250 = [layer.summary.year_before_last.mi_250 for layer in layers]
    ybl_mi_10 = [layer.summary.year_before_last.mi_10 for layer in layers]

    ybl_limit_cnv = [layer.summary.year_before_last.limit_cnv for layer in layers]

    ybl_written_line = [layer.summary.year_before_last.written_line for layer in layers]
    ybl_estimated_signing = [layer.summary.year_before_last.estimated_signing for layer in layers]
    ybl_signed_line = [layer.summary.year_before_last.signed_line for layer in layers]

    ybl_epi_written = [layer.summary.year_before_last.epi_written for layer in layers]
    ybl_epi_estimated = [layer.summary.year_before_last.epi_estimated for layer in layers]
    ybl_epi_signed = [layer.summary.year_before_last.epi_signed for layer in layers]

    # convert to arrays
    ybl_current_year_section_reference = list_to_numpy(ybl_current_year_section_reference, str)
    ybl_current_year_share = list_to_numpy(ybl_current_year_share, float)
    ybl_mi_250 = list_to_numpy(ybl_mi_250, float)
    ybl_mi_10 = list_to_numpy(ybl_mi_10, float)

    ybl_limit_cnv = list_to_numpy(ybl_limit_cnv, float)

    ybl_written_line = list_to_numpy(ybl_written_line, float)
    ybl_estimated_signing = list_to_numpy(ybl_estimated_signing, float)
    ybl_signed_line = list_to_numpy(ybl_signed_line, float)

    ybl_epi_written = list_to_numpy(ybl_epi_written, float)
    ybl_epi_estimated = list_to_numpy(ybl_epi_estimated, float)
    ybl_epi_signed = list_to_numpy(ybl_epi_signed, float)

    ## expiring year
    expiring_mi_250 = [layer.summary.expiring_year.mi_250 for layer in layers]
    expiring_mi_10 = [layer.summary.expiring_year.mi_10 for layer in layers]

    expiring_limit_cnv = [layer.summary.expiring_year.limit_cnv for layer in layers]

    expiring_written_line = [layer.summary.expiring_year.written_line for layer in layers]
    expiring_estimated_signing = [layer.summary.expiring_year.estimated_signing for layer in layers]
    expiring_signed_line = [layer.summary.expiring_year.signed_line for layer in layers]

    expiring_epi_written = [layer.summary.expiring_year.epi_written for layer in layers]
    expiring_epi_estimated = [layer.summary.expiring_year.epi_estimated for layer in layers]
    expiring_epi_signed = [layer.summary.expiring_year.epi_signed for layer in layers]

    # convert to arrays
    expiring_mi_250 = list_to_numpy(expiring_mi_250, float)
    expiring_mi_10 = list_to_numpy(expiring_mi_10, float)

    expiring_limit_cnv = list_to_numpy(expiring_limit_cnv, float)

    expiring_written_line = list_to_numpy(expiring_written_line, float)
    expiring_estimated_signing = list_to_numpy(expiring_estimated_signing, float)
    expiring_signed_line = list_to_numpy(expiring_signed_line, float)

    expiring_epi_written = list_to_numpy(expiring_epi_written, float)
    expiring_epi_estimated = list_to_numpy(expiring_epi_estimated, float)
    expiring_epi_signed = list_to_numpy(expiring_epi_signed, float)

    ## Validation
    pol_ref_for_validation = [x for x in pol_ref if x is not None and x != ""]
    ly_current_year_section_reference_for_val = [x for x in ly_current_year_section_reference if x != "None" and x != ""]
    ybl_current_year_section_reference_for_val = [x for x in ybl_current_year_section_reference if x != "None" and x != ""]

    duplicate_references = set(pol_ref_for_validation) & (set(ly_current_year_section_reference_for_val) | set(ybl_current_year_section_reference_for_val))

    if len(duplicate_references) > 0:
        hx.errors.validation(f"A section reference (Risk Information Tab) is equal to this year's reference of a previous multi-year policy.")

    # 3) Calculations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ## UWA
    summary_fx_factor = ccy_conversion(pd.Series(application_ccy), summary_ccy, ccy_table)[0]

    uwa_table["fx_factor"] = ccy_conversion(uwa_table["currency"], summary_ccy, ccy_table)
    uwa_table_filtered = uwa_table.loc[(uwa_table["underwriter"] == underwriter) & (uwa_table["programme"] == programme)]

    if is_renewal & uwa_table_filtered.shape[0] > 0:
        uwa_limit = uwa_table_filtered["exposure_limit_renewal"].iloc[0] * uwa_table_filtered["fx_factor"].iloc[0] 
        uwa_premium = uwa_table_filtered["premium_renewal"].iloc[0] * uwa_table_filtered["fx_factor"].iloc[0] 
    elif uwa_table_filtered.shape[0] > 0:
        uwa_limit = uwa_table_filtered["exposure_limit_new"].iloc[0] * uwa_table_filtered["fx_factor"].iloc[0] 
        uwa_premium = uwa_table_filtered["premium_new"].iloc[0] * uwa_table_filtered["fx_factor"].iloc[0]
    else:
        uwa_limit = 0
        uwa_premium = 0

    ## multi year policy references

    if cds.multi_year == "Yes":
        year = [int(x[6:8]) if x and len(x) >= 8 and x[6:8].isdigit() else "" for x in pol_ref]

        pol_ref_next_year = [x[:6] + str(year[i] + 1) + x[8:] if (x != None and year[i] != "" and multi_year_period[i] > 1) else "" for i, x in enumerate(pol_ref)]
        pol_ref_year_after_next = [x[:6] + str(year[i] + 2) + x[8:] if (x != None and year[i] != "" and multi_year_period[i] > 2) else "" for i, x in enumerate(pol_ref)]

        show_row_next_year = [x >= 2 for x in multi_year_period]
        show_row_year_after_next = [x == 3 for x in multi_year_period]
    else:
        pol_ref_next_year = ["" for x in pol_ref]
        pol_ref_year_after_next = ["" for x in pol_ref]

        show_row_next_year = [False for x in pol_ref]
        show_row_year_after_next = [False for x in pol_ref]

    ## labels
    cds.fx_conversion_label = f"FX rate to convert from {application_ccy} to {summary_ccy}"

    cds.uwa_limit_label = f"UWA Exposure Limit in {summary_ccy}"
    cds.uwa_premium_label = f"UWA Premium Limit in {summary_ccy}"

    ##NOTE premium 100% in application currency
    cds.prem_100_label = f"Premium 100% in {application_ccy}"

    cds.written_line_label = f"Written Line in {summary_ccy}"
    cds.estimated_line_label = f"Estimated Line in {summary_ccy}"
    cds.signed_line_label = f"Signed Line in {summary_ccy}"

    cds.written_epi_label = f"Written EPI in {summary_ccy}"
    cds.estimated_epi_label = f"Estimated EPI in {summary_ccy}"
    cds.signed_epi_label = f"Signed EPI in {summary_ccy}"

    # 4) converting ly and year before last policy financials ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ## ly
    ly_line_written_summary_fx = ly_written_line * ly_limit_cnv * summary_fx_factor
    ly_line_estimated_summary_fx = ly_estimated_signing * ly_limit_cnv * summary_fx_factor
    ly_line_signed_summary_fx = ly_signed_line * ly_limit_cnv * summary_fx_factor

    ly_epi_written_summary_fx = ly_epi_written * summary_fx_factor
    ly_epi_estimated_summary_fx = ly_epi_estimated * summary_fx_factor
    ly_epi_signed_summary_fx = ly_epi_signed * summary_fx_factor

    ## year before last
    ybl_line_written_summary_fx = ybl_written_line * ybl_limit_cnv * summary_fx_factor
    ybl_line_estimated_summary_fx = ybl_estimated_signing * ybl_limit_cnv * summary_fx_factor
    ybl_line_signed_summary_fx = ybl_signed_line * ybl_limit_cnv * summary_fx_factor

    ybl_epi_written_summary_fx = ybl_epi_written * summary_fx_factor
    ybl_epi_estimated_summary_fx = ybl_epi_estimated * summary_fx_factor
    ybl_epi_signed_summary_fx = ybl_epi_signed * summary_fx_factor

    ## expiring year
    expiring_line_written_summary_fx = expiring_written_line * expiring_limit_cnv * summary_fx_factor
    expiring_line_estimated_summary_fx = expiring_estimated_signing * expiring_limit_cnv * summary_fx_factor
    expiring_line_signed_summary_fx = expiring_signed_line * expiring_limit_cnv * summary_fx_factor

    expiring_epi_written_summary_fx = expiring_epi_written * summary_fx_factor
    expiring_epi_estimated_summary_fx = expiring_epi_estimated * summary_fx_factor
    expiring_epi_signed_summary_fx = expiring_epi_signed * summary_fx_factor

    # 7) Totals ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## weightings for mi 250 and mi 10
    ### ly
    conditions_ly = [ly_signed_line > 0, ly_estimated_signing > 0, ly_written_line > 0]
    choices_ly = [ly_signed_line, ly_estimated_signing, ly_written_line]
    afb_line_for_totals_ly = np.select(conditions_ly, choices_ly, default = 0)
    ### ybl
    conditions_ybl = [ybl_signed_line > 0, ybl_estimated_signing > 0, ybl_written_line > 0]
    choices_ybl = [ybl_signed_line, ybl_estimated_signing, ybl_written_line]
    afb_line_for_totals_ybl = np.select(conditions_ybl, choices_ybl, default = 0)
    ### expiring_year
    conditions_expiring = [expiring_signed_line > 0, expiring_estimated_signing > 0, expiring_written_line > 0]
    choices_expiring = [expiring_signed_line, expiring_estimated_signing, expiring_written_line]
    afb_line_for_totals_expiring = np.select(conditions_expiring, choices_expiring, default = 0)


    ## ly
    cds.summary.ly.line_written_summary_fx = ly_line_written_summary_fx.sum()
    cds.summary.ly.line_estimated_summary_fx = ly_line_estimated_summary_fx.sum()
    cds.summary.ly.line_signed_summary_fx = ly_line_signed_summary_fx.sum()

    cds.summary.ly.epi_written_summary_fx = ly_epi_written_summary_fx.sum()
    cds.summary.ly.epi_estimated_summary_fx = ly_epi_estimated_summary_fx.sum()
    cds.summary.ly.epi_signed_summary_fx = ly_epi_signed_summary_fx.sum()

    cds.summary.ly.mi_250 = (ly_mi_250 * ly_limit_cnv * summary_fx_factor * afb_line_for_totals_ly).sum()
    cds.summary.ly.mi_10 = (ly_mi_10 * ly_limit_cnv * summary_fx_factor * afb_line_for_totals_ly).sum()

    ## year before last
    cds.summary.year_before_last.line_written_summary_fx = ybl_line_written_summary_fx.sum()
    cds.summary.year_before_last.line_estimated_summary_fx = ybl_line_estimated_summary_fx.sum()
    cds.summary.year_before_last.line_signed_summary_fx = ybl_line_signed_summary_fx.sum()

    cds.summary.year_before_last.epi_written_summary_fx = ybl_epi_written_summary_fx.sum()
    cds.summary.year_before_last.epi_estimated_summary_fx = ybl_epi_estimated_summary_fx.sum()
    cds.summary.year_before_last.epi_signed_summary_fx = ybl_epi_signed_summary_fx.sum()

    cds.summary.year_before_last.mi_250 = (ybl_mi_250 * ybl_limit_cnv * summary_fx_factor * afb_line_for_totals_ybl).sum()
    cds.summary.year_before_last.mi_10 = (ybl_mi_10 * ybl_limit_cnv * summary_fx_factor * afb_line_for_totals_ybl).sum()

    ## expiring year
    cds.summary.expiring_year.line_written_summary_fx = expiring_line_written_summary_fx.sum()
    cds.summary.expiring_year.line_estimated_summary_fx = expiring_line_estimated_summary_fx.sum()
    cds.summary.expiring_year.line_signed_summary_fx = expiring_line_signed_summary_fx.sum()

    cds.summary.expiring_year.epi_written_summary_fx = expiring_epi_written_summary_fx.sum()
    cds.summary.expiring_year.epi_estimated_summary_fx = expiring_epi_estimated_summary_fx.sum()
    cds.summary.expiring_year.epi_signed_summary_fx = expiring_epi_signed_summary_fx.sum()

    cds.summary.expiring_year.mi_250 = (expiring_mi_250 * expiring_limit_cnv * summary_fx_factor * afb_line_for_totals_expiring).sum()
    cds.summary.expiring_year.mi_10 = (expiring_mi_10 * expiring_limit_cnv * summary_fx_factor * afb_line_for_totals_expiring).sum()


    # multi year total (this year)
    cds.summary.multi_year_summary_ty.line_written_summary_fx = (
        cds.summary.ty.line_written_summary_fx
        + (ly_line_written_summary_fx * ly_current_year_share * np.where(np.char.str_len(ly_current_year_section_reference) == 12, 1, 0)).sum()
        + (ybl_line_written_summary_fx * ybl_current_year_share * np.where(np.char.str_len(ybl_current_year_section_reference) == 12, 1, 0)).sum()
    )

    cds.summary.multi_year_summary_ty.line_estimated_summary_fx = (
        cds.summary.ty.line_estimated_summary_fx
        + (ly_line_estimated_summary_fx * ly_current_year_share * np.where(np.char.str_len(ly_current_year_section_reference) == 12, 1, 0)).sum()
        + (ybl_line_estimated_summary_fx * ybl_current_year_share * np.where(np.char.str_len(ybl_current_year_section_reference) == 12, 1, 0)).sum()
    )

    cds.summary.multi_year_summary_ty.line_signed_summary_fx = (
        cds.summary.ty.line_signed_summary_fx
        + (ly_line_signed_summary_fx * ly_current_year_share * np.where(np.char.str_len(ly_current_year_section_reference) == 12, 1, 0)).sum()
        + (ybl_line_signed_summary_fx * ybl_current_year_share * np.where(np.char.str_len(ybl_current_year_section_reference) == 12, 1, 0)).sum()
    )

    cds.summary.multi_year_summary_ty.epi_written_summary_fx = (
        cds.summary.ty.epi_written_summary_fx
        + (ly_epi_written_summary_fx * ly_current_year_share * np.where(np.char.str_len(ly_current_year_section_reference) == 12, 1, 0)).sum()
        + (ybl_epi_written_summary_fx * ybl_current_year_share * np.where(np.char.str_len(ybl_current_year_section_reference) == 12, 1, 0)).sum()
    )

    cds.summary.multi_year_summary_ty.epi_estimated_summary_fx = (
        cds.summary.ty.epi_estimated_summary_fx
        + (ly_epi_estimated_summary_fx * ly_current_year_share * np.where(np.char.str_len(ly_current_year_section_reference) == 12, 1, 0)).sum()
        + (ybl_epi_estimated_summary_fx * ybl_current_year_share * np.where(np.char.str_len(ybl_current_year_section_reference) == 12, 1, 0)).sum()
    )

    cds.summary.multi_year_summary_ty.epi_signed_summary_fx = (
        cds.summary.ty.epi_signed_summary_fx
        + (ly_epi_signed_summary_fx * ly_current_year_share * np.where(np.char.str_len(ly_current_year_section_reference) == 12, 1, 0)).sum()
        + (ybl_epi_signed_summary_fx * ybl_current_year_share * np.where(np.char.str_len(ybl_current_year_section_reference) == 12, 1, 0)).sum()
    )

    cds.summary.multi_year_summary_ty.mi_250 = (
        cds.summary.ty.mi_250 
        + (ly_mi_250 * ly_limit_cnv * summary_fx_factor * afb_line_for_totals_ly * ly_current_year_share * np.where(np.char.str_len(ly_current_year_section_reference) == 12, 1, 0)).sum()
        + (ybl_mi_250 * ybl_limit_cnv * summary_fx_factor * afb_line_for_totals_ybl * ybl_current_year_share * np.where(np.char.str_len(ybl_current_year_section_reference) == 12, 1, 0)).sum()
    )

    cds.summary.multi_year_summary_ty.mi_250_prem_ratio = utils.ratio(cds.summary.multi_year_summary_ty.mi_250, cds.summary.multi_year_summary_ty.epi_signed_summary_fx)
    cds.summary.multi_year_summary_ty.mi_250_estimate_prem_ratio = utils.ratio(cds.summary.multi_year_summary_ty.mi_250, cds.summary.multi_year_summary_ty.epi_estimated_summary_fx)
    

    # 8) Write back to hxd ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    cds.summary_comments = cds.tp_comments

    cds.summary_fx_conversion = summary_fx_factor
    cds.summary_uwa_exposure = uwa_limit
    cds.summary_uwa_premium = uwa_premium

    if (cds.summary.ty.line_written_summary_fx > uwa_limit) & (cds.summary.ty.epi_written_summary_fx > uwa_premium):
        cds.summary_uwa_warning = "Warning: UW exposure authority limits and premium authority limits have been breached."
        cds.summary_show_eso_obtained = True
    elif (cds.summary.ty.line_written_summary_fx > uwa_limit):
        cds.summary_uwa_warning = "Warning: UW exposure authority limits have been breached."
        cds.summary_show_eso_obtained = True
    elif (cds.summary.ty.epi_written_summary_fx > uwa_premium):
        cds.summary_uwa_warning = "Warning: UW premium authority limits have been breached."
        cds.summary_show_eso_obtained = True
    else:
        cds.summary_uwa_warning = "Exposure and premium within authority limits."

    if cds.summary_show_eso_obtained:
        if not cds.summary_eso_obtained:
            hx.errors.validation(f"UW authority limits have been breached but ESO has not been obtained.")

    for index, layer in enumerate(layers):
        ## year after next
        layer.summary.year_after_next.section_reference = pol_ref_year_after_next[index]
        layer.summary.year_after_next.risk_adjusted_rate_change = 1
        layer.summary.year_after_next.show_row = show_row_year_after_next[index]

        ## next year
        layer.summary.next_year.section_reference = pol_ref_next_year[index]
        layer.summary.next_year.risk_adjusted_rate_change = 1
        layer.summary.next_year.show_row = show_row_next_year[index]

        ## ly
        layer.summary.ly.line_written_summary_fx = ly_line_written_summary_fx[index]
        layer.summary.ly.line_estimated_summary_fx = ly_line_estimated_summary_fx[index]
        layer.summary.ly.line_signed_summary_fx = ly_line_signed_summary_fx[index]

        layer.summary.ly.epi_written_summary_fx = ly_epi_written_summary_fx[index]
        layer.summary.ly.epi_estimated_summary_fx = ly_epi_estimated_summary_fx[index]
        layer.summary.ly.epi_signed_summary_fx = ly_epi_signed_summary_fx[index]

        ## year before last
        layer.summary.year_before_last.line_written_summary_fx = ybl_line_written_summary_fx[index]
        layer.summary.year_before_last.line_estimated_summary_fx = ybl_line_estimated_summary_fx[index]
        layer.summary.year_before_last.line_signed_summary_fx = ybl_line_signed_summary_fx[index]

        layer.summary.year_before_last.epi_written_summary_fx = ybl_epi_written_summary_fx[index]
        layer.summary.year_before_last.epi_estimated_summary_fx = ybl_epi_estimated_summary_fx[index]
        layer.summary.year_before_last.epi_signed_summary_fx = ybl_epi_signed_summary_fx[index]

        ## expiring year
        layer.summary.expiring_year.line_written_summary_fx = ybl_line_written_summary_fx[index]
        layer.summary.expiring_year.line_estimated_summary_fx = ybl_line_estimated_summary_fx[index]
        layer.summary.expiring_year.line_signed_summary_fx = ybl_line_signed_summary_fx[index]

        layer.summary.expiring_year.epi_written_summary_fx = ybl_epi_written_summary_fx[index]
        layer.summary.expiring_year.epi_estimated_summary_fx = ybl_epi_estimated_summary_fx[index]
        layer.summary.expiring_year.epi_signed_summary_fx = ybl_epi_signed_summary_fx[index]

