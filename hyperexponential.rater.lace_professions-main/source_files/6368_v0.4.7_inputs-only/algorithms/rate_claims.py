# v0.5.0
import hx
import pandas as pd
import numpy as np
import math as math
from datetime import date
from algorithms.rate_utilities import policy_term, ratio
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

def claims_retention_calc(hxd, index, item, df_I_cd):
    item_prev = hxd.cds.experience_rating.claims[index-1] if index > 0  else None
    vbl_EEC = 0
    vbl_Agg = 0
    vbl_NonRanking = 0
    vbl_Maintenance = 0

    eec_cum_true={}
    eec_cum_false={}

    def RDC_non_ranking_or_maintenance_ded(base_prev):
        if index == 0:
            return  vbl_NonRanking
        else:
            if item.policy_year_estimated != item_prev.policy_year_estimated:
                return vbl_NonRanking
            else:
                if (base_prev.agg_retention == vbl_Agg and vbl_Agg > 0):
                    return vbl_Maintenance
                else:
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
        if index == 0:
            return  base.agg_retention
        else:
            if item.policy_year_estimated != item_prev.policy_year_estimated:
                return base.agg_retention
            else:
                return base.agg_retention - base_prev.agg_retention

    ### RDC TRUE ####
    rdct = item.RDC_True
    rdct_prev = item_prev.RDC_True if index > 0  else None
    rdct.non_ranking_or_maintenance_ded = RDC_non_ranking_or_maintenance_ded(rdct_prev)
    rdct.post_ded_claims = max(0,item.incurred_total_usd_inflated - rdct.non_ranking_or_maintenance_ded)  
    rdct.eec = min(rdct.post_ded_claims, vbl_EEC)
    rdct.eec_cumulative = update_eec_cum(rdct.eec, item.policy_year_estimated, eec_cum_true)
    rdct.agg_retention = min(rdct.eec_cumulative, 9999999999 if vbl_Agg==0 else vbl_Agg)
    rdct.final_retention = RDC_final_retention(rdct, rdct_prev)
    rdct.final_total_incurred = max(rdct.post_ded_claims - rdct.final_retention, 0)

    ### RDC FALSE ###
    rdcf  = item.RDC_False
    rdcf_prev = item_prev.RDC_False if index > 0  else None
    rdcf.incurred_defense_inflated = item.defense_incurred_usd * get_index(df_I_cd, item.claim_made_year)
    rdcf.incurred_indemnity_inflated = item.incurred_total_usd_inflated - rdcf.incurred_defense_inflated
    rdcf.non_ranking_or_maintenance_ded = RDC_non_ranking_or_maintenance_ded(rdcf_prev)
    rdcf.post_ded_claims = max(0,rdcf.incurred_indemnity_inflated - rdcf.non_ranking_or_maintenance_ded)
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
    vbl_applies_defence_cost = True
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

    for index, item in enumerate(hxd.cds.experience_rating.claims):
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
        index_defense=get_index(df_I_aec, item.claim_made_year)
        indemnity_inflation_df = df_I_lc if hxd.cds.profession == "lawyers" else df_I_cd
        index_indemnity = get_index(indemnity_inflation_df, item.claim_made_year)
        item.incurred_total_usd_inflated = ((item.defense_incurred_usd or 0) * index_defense
                                        + (item.indemnity_incurred_usd or 0) * index_indemnity)
        ######################################

        ## Paid Total USD Inflated ###########
        defense_df = df_I_cd if hxd.cds.profession == "lawyers" else df_I_aec
        index_defense = get_index(defense_df, item.claim_made_year)
        #index_indemnity #already calculated
        item.paid_total_usd_inflated = ratio((item.defense_fgu_paid or 0) * index_defense + (item.indemnity_fgu_paid or 0) * index_indemnity, item.claims_fx_rate)
        #######################################

        ## Claims Retentions Calculationw #####
        claims_retention_calc(hxd, index, item, df_I_cd)
        item.total_usd_inflated = item.RDC_True.final_total_incurred if vbl_applies_defence_cost else item.RDC_False.final_total_incurred
        ########################################

def rate_claims_tailored(hxd):
    populate_notes(hxd)
    calculate_row_level_items(hxd)
