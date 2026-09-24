# v0.5.0
import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import policy_term, yearfrac, write_pd_to_hxd
from operator import itemgetter
from algorithms.rate_constants import exposure_details_notes, get_inflation_tables
import datetime

def get_year_nodes():
    """construct year nodes"""
    years = [f"year_{20 - i}" for i in range(21)]
    return years

def get_fields():
    fields = [
        "professional_services_fee",
        "epc_design_construct_values",
        "hard_fm_revenue",
        "construct_pass_soft_fm_revenue"
    ]
    return fields

def populate_exposure_details_notes(hxd):
    hxd.cds.exposure.granular.exposure_details_notes = exposure_details_notes

def generate_rows(hxd):
    #20 years
    years = range(21)
    incept_date = hxd.hx_core.inception_date
    incept_year = incept_date.year

    # Set the Expected Exposure Label here 
    hxd.cds.exposure.granular.exposure_expected_current_year_label = f'Expected Exposure - {incept_year}'

    # Set the labels for each row in the grid
    for year in years:
        setattr(hxd.cds.exposure.granular.exposure_details_year_labels, f"year_{year}",incept_year - year)


def populate_output_weights(hxd):
    def excel_logic(ad_year, start_date, retro_date):
        # Construct the Excel-style date
        constructed = datetime.date(ad_year, start_date.month, start_date.day)
        if retro_date is None:
            return 1
        else:
            if constructed >= retro_date:
                return 1
            frac = yearfrac(constructed, retro_date)
            if frac <= 1:
                return 1 - frac
            else:
                return 0

    df_weightings = hx.params.ref_exposure_weightings
    years = [f"year_{i}" for i in range(21)]
    profession = hxd.cds.profession
    if profession is None:
        hx.errors.validation("Profession field must be completed")
        return None

    start_date = hxd.hx_core.inception_date
    retro_date = hxd.cds.retro_date
    
    ad_year = start_date.year
    counter = 5
    for year in years:
        #yearfrac logic
        frac = excel_logic(ad_year, start_date, retro_date)
        if counter < 0:
            weight = 0
        else:
            weight = df_weightings[profession].iloc[counter]
        setattr(getattr(hxd.cds.exposure.granular.exposure_details, year), "weighting", weight * frac)
        counter -= 1
        ad_year -= 1


def calc_override_gross_fee_nodes(hxd):
    path = hxd.cds.exposure.granular.exposure_details
    # Calculate Annual Growth Rate for Notional Reveneue
    gf_year_15 = getattr(getattr(path, "year_15"), "gross_fee") or 0
    gf_year_11 = getattr(getattr(path, "year_11"), "gross_fee") or 0

    psf_year_15 = getattr(getattr(path, "year_15"), "professional_services_fee") or 0
    psf_year_11 = getattr(getattr(path, "year_11"), "professional_services_fee") or 0

    epc_year_15 = getattr(getattr(path, "year_15"), "epc_design_construct_values") or 0   
    epc_year_11 = getattr(getattr(path, "year_11"), "epc_design_construct_values") or 0    

    hfm_year_15 = getattr(getattr(path, "year_15"), "hard_fm_revenue") or 0
    hfm_year_11 = getattr(getattr(path, "year_11"), "hard_fm_revenue") or 0
    
    cps_year_15 = getattr(getattr(path, "year_15"), "construct_pass_soft_fm_revenue") or 0
    cps_year_11 = getattr(getattr(path, "year_11"), "construct_pass_soft_fm_revenue") or 0

    gross_fee_agr = 0 if gf_year_15 == 0 or gf_year_11 == 0 else pow(gf_year_11 / gf_year_15, 1/4) - 1 
    psf_fee_agr = 0 if psf_year_15 == 0 or psf_year_11 == 0 else pow(psf_year_11 / psf_year_15, 1/4) - 1
    epc_fee_agr = 0 if epc_year_15 == 0 or epc_year_11 == 0 else pow(epc_year_11 / epc_year_15, 1/4) - 1
    hfm_fee_agr = 0 if hfm_year_15 == 0 or hfm_year_11 == 0 else pow(hfm_year_11 / hfm_year_15, 1/4) - 1
    cps_fee_agr = 0 if cps_year_15 == 0 or cps_year_11 == 0 else pow(cps_year_11 / cps_year_15, 1/4) - 1

    for year in range(16, 21):
        year_string = f"year_{year}"
        last_year_string = f"year_{year-1}"   #label wise this would be 2011 if current year 2010  (last year really means the next year in real terms)
        if year == 16:
            gf_last_year = getattr(getattr(path, last_year_string), "gross_fee") or 0
            psf_last_year = getattr(getattr(path, last_year_string), "professional_services_fee") or 0
            epc_last_year = getattr(getattr(path, last_year_string), "epc_design_construct_values") or 0
            hfm_last_year = getattr(getattr(path, last_year_string), "hard_fm_revenue") or 0
            cps_last_year = getattr(getattr(path, last_year_string), "construct_pass_soft_fm_revenue") or 0
        else:
            gf_last_year = getattr(getattr(getattr(path, last_year_string), "gross_fee"), "selected") or 0    
            psf_last_year = getattr(getattr(getattr(path, last_year_string), "professional_services_fee"), "selected") or 0    
            epc_last_year = getattr(getattr(getattr(path, last_year_string), "epc_design_construct_values"), "selected") or 0    
            hfm_last_year = getattr(getattr(getattr(path, last_year_string), "hard_fm_revenue"), "selected") or 0    
            cps_last_year = getattr(getattr(getattr(path, last_year_string), "construct_pass_soft_fm_revenue"), "selected") or 0    

        gross_fee = gf_last_year / (1 + gross_fee_agr)
        psf_fee = psf_last_year / (1 + psf_fee_agr)
        epc_fee = epc_last_year / (1 + epc_fee_agr)
        hfm_fee = hfm_last_year / (1 + hfm_fee_agr)       
        cps_fee = cps_last_year / (1 + cps_fee_agr)

        setattr(getattr(getattr(path, year_string), "gross_fee"), "calculated", gross_fee)
        setattr(getattr(getattr(path, year_string), "professional_services_fee"), "calculated", psf_fee)
        setattr(getattr(getattr(path, year_string), "epc_design_construct_values"), "calculated", epc_fee)
        setattr(getattr(getattr(path, year_string), "hard_fm_revenue"), "calculated", hfm_fee)
        setattr(getattr(getattr(path, year_string), "construct_pass_soft_fm_revenue"), "calculated", cps_fee)

def calc_revenues(hxd):
    df_rev_wt = hx.params.ref_ae_revenue_weight
    fields = get_fields()
    years = get_year_nodes()

    # inflation factor for 
    df_ref_inflation = hx.params.ref_inflation
    inflation_factor_exposure = df_ref_inflation[df_ref_inflation["Year"]=="Future"]["Revenue"].iloc[0]

    negative_value_check = False
    for year in years:
        year_num = int(year[5:])
        total_100 = 0
        total_notional = 0
        for field in fields:
            #revenue_100_pcnt
            if year in {f"year_{i}" for i in range(16, 21)}:
                value = getattr(getattr(getattr(hxd.cds.exposure.granular.exposure_details, year), field), "selected") or 0   
            else:
                value = getattr(getattr(hxd.cds.exposure.granular.exposure_details, year), field) or 0

            if value < 0:
                negative_value_check = True

            total_100 += value

            #notional_revenue
            factor = df_rev_wt[df_rev_wt["Revenue Type"]==field]["Weighting"].iloc[0]
            total_notional += value * factor

            #revalued notional revenues
            total_notional_revalued = total_notional * pow((1 + inflation_factor_exposure),year_num)

            #revalued fees
            if year in {f"year_{i}" for i in range(16, 21)}:
                gross_fee = getattr(getattr(getattr(hxd.cds.exposure.granular.exposure_details, year), "gross_fee"), "selected") or 0             
            else:
                gross_fee = getattr(getattr(hxd.cds.exposure.granular.exposure_details, year), "gross_fee") or 0
            
            total_fee_revalued = gross_fee * pow((1 + inflation_factor_exposure),year_num)
        
        setattr(getattr(hxd.cds.exposure.granular.exposure_details, year), "revenue_100_pcnt", total_100)
        setattr(getattr(hxd.cds.exposure.granular.exposure_details, year), "notional_revenue", total_notional)
        setattr(getattr(hxd.cds.exposure.granular.exposure_details, year), "revalued_notional_revenue", total_notional_revalued)
        setattr(getattr(hxd.cds.exposure.granular.exposure_details, year), "revalued_fee", total_fee_revalued)

    if negative_value_check:
        hx.errors.validation("There are negative values in the Exposure Details table in the Exposure Details page")       

def calc_weighted_exposure(hxd):
    years = get_year_nodes()
    profession = hxd.cds.profession
    exp_field = "revalued_fee" if profession == "Lawyers" else "revalued_notional_revenue"

    path = hxd.cds.exposure.granular.exposure_details
    total = 0
    for year in years:
        total += getattr(getattr(path, year), exp_field) * (getattr(getattr(path, year), "weighting") or 0)
    
    hxd.cds.exposure.granular.exposure_expected_current_year = total
    

def set_policy_year(hxd):
    years = range(21)
    incept_date = hxd.hx_core.inception_date
    incept_year = incept_date.year

    for year in years:
        setattr(getattr(hxd.cds.exposure.granular.exposure_details, f"year_{year}"),"policy_year", incept_year - year)

def populate_chart_nodes(hxd):
    label_lpl_uk = "UK Only Model Loss Cost - Lawyers"
    label_aec_uk = "UK Only Model Loss Cost - AEC"

    label_lpl_eu = "Europe Only Model Loss Cost - Lawyers"
    label_aec_eu = "Europe Only Model Loss Cost - AEC"

    col_lpl = "loss_cost_lpl"
    col_aec = "loss_cost_aec"

    df_uk = hx.params.ref_chart_data_p5m_ukonly
    df_uk = df_uk / 1e6

    df_eu = hx.params.ref_chart_data_p5m_euonly
    df_eu = df_eu / 1e6

    if hxd.cds.profession == "Lawyers":
        label_uk = label_lpl_uk
        label_eu = label_lpl_eu
        col = col_lpl
    else:
        label_uk = label_aec_uk
        label_eu = label_aec_eu
        col = col_aec

    df_uk = df_uk[["revenue", col]]
    df_uk = df_uk.rename(columns={col:"loss_cost"}) 

    df_eu = df_eu[["revenue", col]]
    df_eu = df_eu.rename(columns={col:"loss_cost"})   

    write_pd_to_hxd(
        df_uk, 
        hxd.cds.exposure.granular.chart_loss_cost_by_revenue.data.points_uk,
        ["revenue", "loss_cost"]
        )
    
    write_pd_to_hxd(
        df_eu,
        hxd.cds.exposure.granular.chart_loss_cost_by_revenue.data.points_eu,
        ["revenue", "loss_cost"]
    )

    hxd.cds.exposure.granular.chart_loss_cost_by_revenue.data.label_uk = label_uk
    hxd.cds.exposure.granular.chart_loss_cost_by_revenue.data.label_eu = label_eu

def client_details_inception_year_column(hxd):
    path = hxd.cds.exposure.granular

    if hxd.cds.profession == "Lawyers":
        pcnt_bool = True if path.bool_show_inception_year_client_details_input and path.client_details_lawyers.bool_is_pcnt else False
        value_bool = True if path.bool_show_inception_year_client_details_input and path.client_details_lawyers.bool_is_pcnt_not else False
    else:
        pcnt_bool = True if path.bool_show_inception_year_client_details_input and path.client_details_AEC.bool_aop_is_pcnt else False
        value_bool = True if path.bool_show_inception_year_client_details_input and path.client_details_AEC.bool_aop_is_pcnt_not else False

    path.bool_show_inception_year_client_details_output_pcnt = pcnt_bool
    path.bool_show_inception_year_client_details_output_value = value_bool   

def rate_exposure_details(hxd):
    populate_chart_nodes(hxd)
    populate_exposure_details_notes(hxd) 
    set_policy_year(hxd)
    generate_rows(hxd)
    populate_output_weights(hxd)
    calc_override_gross_fee_nodes(hxd)
    calc_revenues(hxd)
    calc_weighted_exposure(hxd)
    client_details_inception_year_column(hxd)