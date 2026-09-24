# v0.5.0
import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import policy_term, ratio
from algorithms.rate_constants import experience_notes, get_fx_rate
from collections import defaultdict

def populate_notes(hxd):
    hxd.cds.experience_rating.experience_instructions = experience_notes

def claims_summary(hxd):
    claims_policy_year = hxd.cds.experience_rating.claims_policy_year or 0
    ccy = hxd.cds.currencies.source_currency
    fx_rate_usd = get_fx_rate(ccy)
    claims_row_range = 21           # 15 years => 16
    
    years = range(claims_row_range)
    incept_date = hxd.hx_core.inception_date
    incept_year = incept_date.year

    for year in years:
        setattr(getattr(hxd.cds.experience_rating.claims_summary, f"year_{year}"),"policy_year",incept_year - year)

    #Revalued Notional Revenue
    profession = hxd.cds.profession
    col_name = "revalued_fee" if profession == "Lawyers" else "revalued_notional_revenue"
    for year in years:
        if incept_year - year >= claims_policy_year:
            value = getattr(getattr(hxd.cds.exposure.granular.exposure_details, f"year_{year}"), col_name)
            value = ratio(value, fx_rate_usd)
            setattr(getattr(hxd.cds.experience_rating.claims_summary, f"year_{year}"),"revalued_notional_revenue",value)

    # Weighted Revalued Notional Revenue
    # From Exposure
    if hxd.cds.profession_lawyers_bool:
        col_name = "gross_fee"
        col_name_revalued = "revalued_fee"
    else: 
        col_name = "notional_revenue"
        col_name_revalued = "revalued_notional_revenue"

    # Get weights from the 5 computed weight years as dict
    path = hxd.cds.exposure.granular.exposure_details
    years_6 = range(6)
    weight_dict = defaultdict(int)
    for year in years_6:
        #if year >= claims_policy_year:
        weight_dict[year] += (getattr(getattr(path, f"year_{year}"), "weighting") or 0)

    year_wee_total = defaultdict(int)
    year_wod_total = defaultdict(int)
    for year in years:
        if incept_year - year >= claims_policy_year:
            for row in years_6:     # perform sumproduct
                #if year + row < claims_row_range or col_name != "gross_fee":
                #year_wee_total[year] += weight_dict[row] * (getattr(getattr(path,f"year_{min(20, year + row)}"), col_name) or 0)
                if year + row < 16 or col_name != "gross_fee":
                    year_wee_total[year] += weight_dict[row] * (getattr(getattr(path,f"year_{min(20, year + row)}"), col_name) or 0)
                else:
                    year_wee_total[year] += weight_dict[row] * (getattr(getattr(getattr(path,f"year_{min(20, year + row)}"), col_name),"selected") or 0)

                year_wod_total[year] += weight_dict[row] * (getattr(getattr(path,f"year_{min(20, year + row)}"), col_name_revalued) or 0)

            value = ratio(year_wod_total[year], fx_rate_usd)
            setattr(getattr(hxd.cds.experience_rating.claims_summary,f"year_{year}"),"revalued_notional_revenue_weighted", value)

    # Percent Developed
    # calculate dev month

    df_claims_dev = hx.params.ref_tbl_claims_development
    lookup_col = "Lawyers Claims Development" if hxd.cds.profession_lawyers_bool else "A&E Claims Development"
    claims_asatdate = hxd.cds.experience_rating.claims_asatdate
    incept_date = hxd.hx_core.inception_date
    incept_year = incept_date.year
    
    for year in years:
        if incept_year - year >= claims_policy_year:
            actual_year = incept_year - year
            if claims_asatdate is None:
                claim_dev_month = 3
            else:
                claim_dev_month = 3 if claims_asatdate.year < actual_year else 12 + (claims_asatdate.year - actual_year) * 12
            df_claims_dev_filtered = df_claims_dev[df_claims_dev["Development Month"] == claim_dev_month]
            if df_claims_dev_filtered is None or len(df_claims_dev_filtered) == 0:
                dev_factor = 0
            else:
                dev_factor = df_claims_dev_filtered[lookup_col].iloc[0]

            setattr(getattr(hxd.cds.experience_rating.claims_summary,f"year_{year}"),"pcnt_developed", dev_factor)


    # Ground Up - Incurred USD
    # Ground Up - Inflated USD
    year_inc_totals = defaultdict(int)
    year_inf_totals = defaultdict(int)
    for item in hxd.cds.experience_rating.claims:
        if item.policy_year_estimated is not None and item.to_use:
            #year should be in range 0 - 14  (i.e. not actual year)
            year_index = int(incept_year - item.policy_year_estimated)
            if year_index > 0:
                year_inc_totals[year_index] += (item.incurred_total_usd or 0)
                year_inf_totals[year_index] += (item.incurred_total_usd_inflated or 0)

    for year, value in year_inc_totals.items():
        if incept_year - year >= claims_policy_year:
            setattr(getattr(hxd.cds.experience_rating.claims_summary, f"year_{year}"), "gu_incurred", value)

    for year, value in year_inf_totals.items():
        if incept_year - year >= claims_policy_year:
            setattr(getattr(hxd.cds.experience_rating.claims_summary, f"year_{year}"), "gu_inflated", value)

    # Inflated Incurred - comes from Simulation output
    # ql_inflated_incurred

def set_last_x_year_labels(hxd):
    incept_year = hxd.hx_core.inception_date.year
    path = hxd.cds.experience_rating.last_x_year_labels
    claims_date = hxd.cds.experience_rating.claims_policy_year or 0

    if claims_date == 0:
        last_10 = 10
        last_15 = 15
        last_20 = 20
    else:
        last_10 = min(10, incept_year - claims_date)
        last_15 = min(15, incept_year - claims_date)
        last_20 = min(20, incept_year - claims_date)

    path.last_10_years = f"Last {last_10}yrs"
    path.last_15_years = f"Last {last_15}yrs"
    path.last_20_years = f"Last {last_20}yrs"  

def rate_experience_rating_2(hxd):
    populate_notes(hxd)
    set_last_x_year_labels(hxd)
    claims_summary(hxd)