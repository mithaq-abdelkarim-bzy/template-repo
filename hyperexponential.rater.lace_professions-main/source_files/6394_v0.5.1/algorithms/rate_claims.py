# v0.5.1
import hx
import pandas as pd
import numpy as np
import math as math
from datetime import date
from algorithms.rate_utilities import policy_term, ratio, write_pd_to_hxd
from algorithms.rate_constants import (get_inflation_tables, claims_notes, get_fx_rate,
    get_quotes_params, get_quotes_params_addl, get_credibility_params)
from collections import defaultdict
from calendar import monthrange


def populate_notes(hxd):
    hxd.cds.experience_rating.claims_instructions = claims_notes


def get_index(df, year):
    index_value = 0
    if year is not None:
        df_filter = df[df["Year"]==year]
        if not df_filter.empty:
            index_value = df_filter["Index"].iloc[0]
        else:
            index_value = 0
    else:
        index_value = 0
    return index_value


def claims_retention_calc(hxd, item, item_prev, df_I_cd, eec_cum_true, eec_cum_false):
    # item / item_prev are claim nodes in DateMade (claim_made_date) order —
    # item_prev is the chronologically previous claim, NOT the previous node in the list.
    # eec_cum_true / eec_cum_false are shared across the whole ordered pass so
    # the cumulative EEC genuinely accumulates by policy year.
    fx_rate = (get_fx_rate(hxd.cds.currencies.source_currency) or 1)
    vbl_EEC = (hxd.cds.retention_split[0].eec or 0) / fx_rate        #convert to usd for this process
    vbl_Agg = (hxd.cds.retention_split[0].aggregate or 0) / fx_rate
    vbl_NonRanking = (hxd.cds.retention_split[0].retention_underlying or 0) / fx_rate
    vbl_Maintenance = (hxd.cds.retention_split[0].retention_residual or 0) / fx_rate

    def RDC_non_ranking_or_maintenance_ded(base_prev):
        if item_prev is None:
            return vbl_NonRanking
        if item.policy_year_estimated != item_prev.policy_year_estimated:
            return vbl_NonRanking
        if (base_prev.agg_retention == vbl_Agg and vbl_Agg > 0):
            return vbl_Maintenance
        return vbl_NonRanking

    def update_eec_cum(eec, year, _dict):
        if year is not None:
            if year not in _dict:
                _dict[year] = 0
            _dict[year] += eec
            return _dict[year]
        else:
            return 0

    def RDC_final_retention(base, base_prev):
        if item_prev is None:
            return base.agg_retention
        if item.policy_year_estimated != item_prev.policy_year_estimated:
            return base.agg_retention
        return base.agg_retention - base_prev.agg_retention

    ### RDC TRUE ####
    rdct = item.RDC_True
    rdct_prev = item_prev.RDC_True if item_prev is not None else None
    rdct.non_ranking_or_maintenance_ded = RDC_non_ranking_or_maintenance_ded(rdct_prev)
    rdct.post_ded_claims = max(0, item.incurred_total_usd_inflated - rdct.non_ranking_or_maintenance_ded)
    rdct.eec = min(rdct.post_ded_claims, vbl_EEC)
    rdct.eec_cumulative = update_eec_cum(rdct.eec, item.policy_year_estimated, eec_cum_true)
    rdct.agg_retention = min(rdct.eec_cumulative, 9999999999 if vbl_Agg==0 else vbl_Agg)
    rdct.final_retention = RDC_final_retention(rdct, rdct_prev)
    rdct.final_total_incurred = max(rdct.post_ded_claims - rdct.final_retention, 0)

    ### RDC FALSE ###
    rdcf = item.RDC_False
    rdcf_prev = item_prev.RDC_False if item_prev is not None else None
    rdcf.incurred_defense_inflated = item.defense_incurred_usd * get_index(df_I_cd, item.policy_year_estimated)
    rdcf.incurred_indemnity_inflated = item.incurred_total_usd_inflated - rdcf.incurred_defense_inflated
    rdcf.non_ranking_or_maintenance_ded = RDC_non_ranking_or_maintenance_ded(rdcf_prev)
    rdcf.post_ded_claims = max(0, rdcf.incurred_indemnity_inflated - rdcf.non_ranking_or_maintenance_ded)
    rdcf.eec = min(rdcf.post_ded_claims, vbl_EEC)
    rdcf.eec_cumulative = update_eec_cum(rdcf.eec, item.policy_year_estimated, eec_cum_false)
    rdcf.agg_retention = min(rdcf.eec_cumulative, 9999999999 if vbl_Agg==0 else vbl_Agg)
    rdcf.final_retention = RDC_final_retention(rdcf, rdcf_prev)
    rdcf.final_total_incurred = max(rdcf.post_ded_claims - rdcf.final_retention, 0) + rdcf.incurred_defense_inflated

    ####### Retention not applied on defense cost ####
    # Non Ranking or Maintenance Deductible
    # Post Deductible Claims
    # EEC
    # Cumulative EEC Calculation
    # Aggregate Retention
    # Final Retention Applied
    # Final Total Incurred _ Defense cost retention No


def calculate_row_level_items(hxd):
    vbl_applies_defence_cost = hxd.cds.retention_split[0].defence_cost_bool == "Yes"
    inflation_tables = get_inflation_tables(hxd)
    df_I_aec = inflation_tables["df_I_aec"]
    df_I_lc = inflation_tables["df_I_lc"]
    df_I_cd = inflation_tables["df_I_cd"]

    def policy_year_estimated(claim_made_date):
        date_start = hxd.hx_core.inception_date
        if claim_made_date is None or date_start is None:
            return None
        year_risk_start = date_start.year
        year_claim_start = claim_made_date.year
        month_claim_start = claim_made_date.month
        day_claim_start = claim_made_date.day
        # Adjust the day so it is valid for the inception year (handles 29 Feb claims)
        max_day = monthrange(year_risk_start, month_claim_start)[1]
        safe_day = min(day_claim_start, max_day)
        if date(year_risk_start, month_claim_start, safe_day) < date_start:
            return year_claim_start - 1
        else:
            return year_claim_start

    ###### Pass 1: order-independent row-level calcs (original node order) ######
    for item in hxd.cds.experience_rating.claims:
        item.claim_made_year = item.claim_made_date.year if item.claim_made_date else None
        item.defense_incurred = (item.defense_fgu_os or 0) + (item.defense_fgu_paid or 0)
        item.indemnity_incurred = (item.indemnity_fgu_os or 0) + (item.indemnity_fgu_paid or 0)
        item.claims_fx_rate = get_fx_rate(item.currency)
        item.policy_year_estimated = policy_year_estimated(item.claim_made_date)
        item.defense_incurred_usd = ratio(item.defense_incurred, item.claims_fx_rate)
        item.indemnity_incurred_usd = ratio(item.indemnity_incurred, item.claims_fx_rate)
        item.incurred_total_usd = item.defense_incurred_usd + item.indemnity_incurred_usd
        item.incurred_total_usd_inflated = item.defense_incurred_usd + item.indemnity_incurred_usd
        item.to_use = False if (item.policy_year_estimated or 0) < (hxd.hx_core.inception_date.year or 99999) - 15 else True # Excludes claims older than 15 years

        ## Incurred Total USD Inflated #######
        #index_defense=get_index(df_I_aec, item.claim_made_year)
        index_defense=get_index(df_I_cd, item.policy_year_estimated)
        indemnity_inflation_df = df_I_lc if hxd.cds.profession == "Lawyers" else df_I_aec    #df_I_cd
        index_indemnity = get_index(indemnity_inflation_df, item.policy_year_estimated)
        item.incurred_total_usd_inflated = ((item.defense_incurred_usd or 0) * index_defense
                                        + (item.indemnity_incurred_usd or 0) * index_indemnity)
        # if item.incurred_total_usd_inflated != 0:
        #     print("index_defense", index_defense)
        #     print("defense_incurred_usd", item.defense_incurred_usd)
        #     print("index_indemnity", index_indemnity)
        #     print("indemnity_incurred_usd", item.indemnity_incurred_usd)
        #     print("incurred_total_usd_inflated", item.incurred_total_usd_inflated)

        ######################################

        ## Paid Total USD Inflated ###########
        #defense_df = df_I_cd if hxd.cds.profession == "lawyers" else df_I_aec
        defense_df = df_I_cd
        index_defense = get_index(defense_df, item.policy_year_estimated)
        #index_indemnity #already calculated
        item.paid_total_usd_inflated = ratio((item.defense_fgu_paid or 0) * index_defense + (item.indemnity_fgu_paid or 0) * index_indemnity, item.claims_fx_rate)
        #######################################

    ###### Pass 2: retention calcs in DateMade (claim_made_date) order ######
    # Sort node *references*, not values: results are written straight back to
    # the correct claim node, so the on-screen HX Renew claim order is untouched
    # and no dataframe round-trip / write-back is needed.
    claims = list(hxd.cds.experience_rating.claims)
    order = sorted(
        range(len(claims)),
        key=lambda i: (claims[i].claim_made_date is None,      # dateless claims last
                       claims[i].claim_made_date or date.min,
                       i),                                     # stable tie-break: original row order
    )

    eec_cum_true = {}
    eec_cum_false = {}
    item_prev = None
    for i in order:
        item = claims[i]
        claims_retention_calc(hxd, item, item_prev, df_I_cd, eec_cum_true, eec_cum_false)
        item.total_usd_inflated = item.RDC_True.final_total_incurred if vbl_applies_defence_cost else item.RDC_False.final_total_incurred
        item_prev = item
        ########################################


def populate_ave_chart_experience(hxd):
    # simulation routine will populate for exposure
    rows = []
    for item in hxd.cds.experience_rating.claims:
        if item.to_use:
            loss = item.incurred_total_usd_inflated
            if (loss or 0) > 0:
                rows.append(loss)
    df = pd.DataFrame(rows, columns=["loss"])
    df = df.sort_values("loss", ascending=False).reset_index(drop=True)
    n = len(df)
    if n == 0:
        df["percentile"] = []
    elif n == 1:
        df["percentile"] = [1.0]
    else:
        df["percentile"] = np.linspace(1.0, 0.0, n)
    max_points = 5000
    if len(df) > max_points:
        idx = np.linspace(0, len(df) - 1, max_points, dtype=int)
        df_plot = df.iloc[idx].reset_index(drop=True)
    else:
        df_plot = df.copy()
    path = hxd.cds.ave_chart
    path.data.label_exposure = "Simulated Loss"
    path.data.label_experience = "Actual Loss"
    hxd.cds.ave_chart.data.points_experience = [{}] * len(df_plot)    # required hack to initialise the list to the correct length
    write_pd_to_hxd(
        df_plot,
        path.data.points_experience,
        ["percentile", "loss"]
    )


def rate_claims_tailored(hxd):
    populate_notes(hxd)
    calculate_row_level_items(hxd)
    populate_ave_chart_experience(hxd)