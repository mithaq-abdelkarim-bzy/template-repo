import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter, attrgetter
from algorithms.rate_constants import max_curves
from algorithms.timer import timer
from hx import params as hx_params
from algorithms.udf import generate_ymlt, list_to_numpy, ccy_conversion

table_europe = hx_params.table_area_code_europe
table_us_aus = hx_params.table_area_code_us_aus
table_can_car = hx_params.table_area_code_can_car
table_far_east_amei = hx_params.table_area_code_far_east_amei

us_rds_regions = hx_params.table_rds_regions_all

ccy_table = hx_params.table_currency
uwa_table = hx_params.table_underwriter_authority

uwa_as_at_table = hx_params.table_authority_as_at


def rate_additional_pages(hxd, common_data_dict):

    ## set dataframe variables for cleaner code
    cds = hxd.cds
    layers = cds.layers
    area_codes = cds.area_codes_select

    # add epsilon in to deal with rounding errors in floating point arithmetic
    EPS = 1e-9

    ## 1) Area Codes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 1.1) Auto fill US regions
    rds_regions = us_rds_regions["region"]

    rms_regional_entries = [[getattr(layer.rms_regional,f"{event}") for event in rds_regions] for layer in layers]
    rms_regional_entries = pd.DataFrame(rms_regional_entries, columns=rds_regions)
    rms_regional_entries = rms_regional_entries.fillna(0)
    rms_regional_entries["layer_index"] = rms_regional_entries.index
    rms_regional_entries = rms_regional_entries.melt(id_vars="layer_index", var_name = "region", value_name = "rds_lol")
    rms_regional_entries = pd.merge(rms_regional_entries, us_rds_regions, on = "region", how = "left")
    rms_regional_entries["area_code_select"] = np.where(rms_regional_entries["rds_lol"] >= 0.1, "Yes", "")
    rms_regional_entries["column_path"] = "area_codes_select." + rms_regional_entries["area_code"]
    rms_regional_entries = rms_regional_entries.pivot(index = "layer_index", columns = "column_path", values = "area_code_select")

    utils.write_pd_to_hxd(rms_regional_entries, cds.layers, rms_regional_entries.columns.values)

    # 1.2) Calculate Summary
    area_code_total_error_count = 0

    if cds.show_intl_fields:
        europe_df = utils.pd_df_from_hx_list(layers, list("area_codes_perc." + table_europe["field"])).fillna(0)
        us_aus_df = utils.pd_df_from_hx_list(layers, list("area_codes_perc." + table_us_aus["field"])).fillna(0)
        can_car_df = utils.pd_df_from_hx_list(layers, list("area_codes_perc." + table_can_car["field"])).fillna(0)
        far_east_amei_df = utils.pd_df_from_hx_list(layers, list("area_codes_perc." + table_far_east_amei["field"])).fillna(0)

        euorpe_summ = europe_df.sum(axis=1)
        us_aus_summ = us_aus_df.sum(axis=1)
        can_car_summ = can_car_df.sum(axis=1)
        far_east_amei_summ = far_east_amei_df.sum(axis=1)
        total = euorpe_summ + us_aus_summ + can_car_summ + far_east_amei_summ

        for index, layer in enumerate(layers):
            layer.area_codes_summary.europe = euorpe_summ[index]
            layer.area_codes_summary.us_aus = us_aus_summ[index]
            layer.area_codes_summary.can_car = can_car_summ[index]
            layer.area_codes_summary.far_east_amei = far_east_amei_summ[index]
            layer.area_codes_summary.total = total[index]

            if total[index] > 1 + EPS:
                area_code_total_error_count += 1

    else: 
        ## Trim down to speed up for US
        us_aus_df = utils.pd_df_from_hx_list(layers, list("area_codes_perc." + table_us_aus["field"])).fillna(0)

        us_aus_summ = us_aus_df.sum(axis=1)

        for index, layer in enumerate(layers):
            layer.area_codes_summary.us_aus = us_aus_summ[index]
            layer.area_codes_summary.total = us_aus_summ[index]
    
            if us_aus_summ[index] > 1 + EPS:
                area_code_total_error_count += 1

    # 1.3) Total Validation
    if area_code_total_error_count > 0:
        hx.errors.validation(f"All totals (Area Codes Tab) must be less than 100%.")

    ## 2) Send rate change ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    total_error_count = cds.send_rate_change.total_error_count

    if (total_error_count == 0):
        cds.send_rate_change.show_send_rate_change = True

    ## 3) ESO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    is_renewal = cds.standard_fields.is_renewal
    summary_ccy = cds.currency_policy_financials

    eso = cds.eso_template
    cob = eso.cob_code
    authorising_uw = eso.authorising_uw

    table_eso_authority = hx_params.table_eso_authority
    table_eso_authority["fx_factor"] = ccy_conversion(table_eso_authority["Letter Currency"].str[:3], summary_ccy, ccy_table)

    uw_eso_authority = table_eso_authority[(table_eso_authority["Underwriter"].str[:3] == cds.standard_fields.underwriter) & (table_eso_authority["Cob"] == cob)]
    authorising_uw_eso_authority = table_eso_authority[(table_eso_authority["Underwriter"].str[:3] == authorising_uw) & (table_eso_authority["Cob"] == cob)]
    

    if is_renewal & (uw_eso_authority.shape[0] > 0):
        uw_loa_premium = uw_eso_authority["Treaty Risks (Renewal) Premium Authority "].iloc[0] * uw_eso_authority["fx_factor"].iloc[0]
        uw_loa_exposure = uw_eso_authority["Exposure Limit (Renewal Risks)"].iloc[0] * uw_eso_authority["fx_factor"].iloc[0]
        uw_loa_term = uw_eso_authority["Policy Period (Renewal)"].iloc[0] * uw_eso_authority["fx_factor"].iloc[0]
    elif uw_eso_authority.shape[0] > 0:
        uw_loa_premium = uw_eso_authority["Treaty Risks (New Business) Premium Authority"].iloc[0] * uw_eso_authority["fx_factor"].iloc[0]
        uw_loa_exposure = uw_eso_authority["Exposure Limit (New Business Risks)"].iloc[0] * uw_eso_authority["fx_factor"].iloc[0]
        uw_loa_term = uw_eso_authority["Policy Period (New Business)"].iloc[0] * uw_eso_authority["fx_factor"].iloc[0]
    else:
        uw_loa_premium = 0
        uw_loa_exposure = 0
        uw_loa_term = 0

    eso.uw_authority.loa_premium = uw_loa_premium
    eso.uw_authority.loa_exposure = uw_loa_exposure
    eso.uw_authority.loa_term = uw_loa_term

    eso.uw_authority.loa_exposure_stacking = uw_loa_exposure


    if is_renewal & (authorising_uw_eso_authority.shape[0] > 0):
        authorising_loa_premium = authorising_uw_eso_authority["Treaty Risks (Renewal) Premium Authority "].iloc[0] * authorising_uw_eso_authority["fx_factor"].iloc[0]
        authorising_loa_exposure = authorising_uw_eso_authority["Exposure Limit (Renewal Risks)"].iloc[0] * authorising_uw_eso_authority["fx_factor"].iloc[0] 
        authorising_loa_term = authorising_uw_eso_authority["Policy Period (Renewal)"].iloc[0] * authorising_uw_eso_authority["fx_factor"].iloc[0]
    elif authorising_uw_eso_authority.shape[0] > 0:
        authorising_loa_premium = authorising_uw_eso_authority["Treaty Risks (New Business) Premium Authority"].iloc[0] * authorising_uw_eso_authority["fx_factor"].iloc[0]
        authorising_loa_exposure = authorising_uw_eso_authority["Exposure Limit (New Business Risks)"].iloc[0] * authorising_uw_eso_authority["fx_factor"].iloc[0] 
        authorising_loa_term = authorising_uw_eso_authority["Policy Period (New Business)"].iloc[0] * authorising_uw_eso_authority["fx_factor"].iloc[0]
    else:
        authorising_loa_premium = 0
        authorising_loa_exposure = 0
        authorising_loa_term = 0

    eso.authorising_uw_authority.loa_premium = authorising_loa_premium
    eso.authorising_uw_authority.loa_exposure = authorising_loa_exposure
    eso.authorising_uw_authority.loa_term = authorising_loa_term

    eso.authorising_uw_authority.loa_exposure_stacking = authorising_loa_exposure

    eso.requested.request_note = "NB: UW to include 10% buffer in request."
    eso.authorising_uw_authority.authority_as_at = uwa_as_at_table["as_at"].iloc[0]