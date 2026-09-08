import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import one_layer, ratio, pd_df_from_hx_list, look_up, tp_components, year_diff, policy_term
from algorithms.rate_constants import benchmark_lr, liab_min_rate
from algorithms import parameter_tables_schema as params


def calculate_technical_premium(
    hxd, 
    expected_loss_cost, 
    total_expected_loss_cost=None,
    written_line=None, 
    brokerage=None, 
    bp_class=None
):
    layer, cvg = one_layer(hxd)
    tp = tp_components(hxd, bp_class)

    # Set key TP params
    che = tp["che"]
    fixed_exp = tp["fixed_exp"]
    technical_lr = tp["technical_lr"]

    if total_expected_loss_cost:  # Allow for allocation of fixed expenses to different coverages based on EL
        fixed_exp = fixed_exp * ratio(expected_loss_cost, total_expected_loss_cost)

    if written_line is None:
        written_line = layer.written_line or 0

    if brokerage is None:
        brokerage = layer.brokerage or 0
    
    # Calculate premium
    share_expected_loss = expected_loss_cost * written_line
    technical_premium_net = ratio(
        ratio((share_expected_loss * (1 + che) + fixed_exp), technical_lr),
        written_line
    )
    technical_premium = ratio(technical_premium_net, (1 - brokerage))

    return technical_premium

def rate_rating_summary(hxd, max_liab_limit):
    layer, cvg = one_layer(hxd)
    term = hxd.cds.policy_info.term
    tp = tp_components(hxd)
    tp_hull = tp_components(hxd, bp_class="Aviation PD")
    tp_liab = tp_components(hxd, bp_class="Aviation Liab")
    hull = cvg.hull
    liab = cvg.liability
    tot = layer.totals

    expo = hxd.cds.exposure.granular
    expe = hxd.cds.experience_rating
    as_tot = expo.aircraft_summary_total

    BPItoMeetPlan = hx.params.al_BPItoMeetPlan
    BPItoMeetROC = hx.params.al_BPItoMeetROC
    
    # Set rating methodology
    product = hxd.cds.rater

    # Show aircraft summary
    expo.show_aircraft_summary = expo.show_al_pricing or expo.show_ga_pricing
    expo.hide_aircraft_summary = not expo.show_aircraft_summary

    # Cover section
    coverages = [hull, liab, tot]

    hull.benchmark_premium_pre_exp = as_tot.hull_benchmark
    liab.pax.benchmark_premium_pre_exp = as_tot.pax_liab_benchmark
    liab.tpl.benchmark_premium_pre_exp = as_tot.tpl_benchmark

    hull.benchmark_rate_pre_exp = as_tot.hull_benchmark_rate
    liab.pax.benchmark_rate_pre_exp = f"{round(as_tot.pax_liab_benchmark_per_seat or 0):,} per seat"
    liab.tpl.benchmark_rate_pre_exp = as_tot.tpl_benchmark

    # Experience Rating section
    hull_exp_claims = expe.hull.expected_claims or 0
    liab_exp_claims = expe.liability.expected_claims or 0
    hull.benchmark_premium_exp = ratio(ratio(hull_exp_claims, benchmark_lr), 1 - hull.brokerage)
    liab.benchmark_premium_exp = ratio(ratio(liab_exp_claims, benchmark_lr), 1 - liab.brokerage)

    hull.exp_credibility = expe.hull.credibility or 0
    liab.exp_credibility = expe.liability.credibility or 0

    hull.benchmark_premium_pre_uw_adj = hull.benchmark_premium_pre_exp * (1 - hull.exp_credibility) + hull.benchmark_premium_exp * hull.exp_credibility
    total_liab_premium = liab.pax.benchmark_premium_pre_exp + liab.tpl.benchmark_rate_pre_exp

    # Calculate minimum premium
    pol_liab_min_rate = liab_min_rate * term
    pol_liab_min_premium = ratio(max_liab_limit * pol_liab_min_rate, 1 - liab.brokerage)

    liab_premium = 0
    combined_liab_premium = (total_liab_premium) * (1 - liab.exp_credibility) + liab.benchmark_premium_exp * liab.exp_credibility

    if liab.coverage == "Combined":
        liab_premium = combined_liab_premium
    elif liab.coverage == "Third Party":
        liab_premium = liab.tpl.benchmark_rate_pre_exp * (1 - liab.exp_credibility) + liab.benchmark_premium_exp * liab.exp_credibility
    elif liab.coverage == "Passenger":
        liab_premium = liab.pax.benchmark_premium_pre_exp * (1 - liab.exp_credibility) + liab.benchmark_premium_exp * liab.exp_credibility

    liab.benchmark_premium_pre_uw_adj = max(pol_liab_min_premium, liab_premium) if product == "Airlines" else combined_liab_premium
    liab.min_rate_info = "Minimum Liability rate applied" if pol_liab_min_premium > liab_premium else None

    # UW Adjustments section
    hull.benchmark_premium_post_uw_adj = hull.benchmark_premium_pre_uw_adj * layer.pilot_uw_adj * hull.uw_adj
    liab.benchmark_premium_post_uw_adj = liab.benchmark_premium_pre_uw_adj * layer.pilot_uw_adj * liab.uw_adj

    hull.uw_adj_impact = layer.pilot_uw_adj * hull.uw_adj
    liab.uw_adj_impact = layer.pilot_uw_adj * liab.uw_adj
    
    # BPI
    hull.benchmark_premium = (1 + tp_hull["nmp_load"]) * hull.benchmark_premium_post_uw_adj
    liab.benchmark_premium = (1 + tp_liab["nmp_load"]) * liab.benchmark_premium_post_uw_adj
    
    tot.benchmark_premium = hull.benchmark_premium + liab.benchmark_premium
    tot.quoted_premium = hull.quoted_premium + liab.quoted_premium

    for cvg in coverages:
        brokerage = liab.brokerage if cvg == liab else hull.brokerage
        cvg.pflr = ratio(cvg.benchmark_premium * (1 - brokerage) * benchmark_lr, cvg.quoted_premium)
        cvg.pflr_net = ratio(cvg.benchmark_premium * (1 - brokerage) * benchmark_lr, cvg.quoted_premium * (1- brokerage))
        cvg.bpi = ratio(cvg.quoted_premium, cvg.benchmark_premium)

    # BPI to meet plan and ROC
    yoa = hxd.hx_core.inception_date.year
    bp_plan_year = yoa if yoa in list(BPItoMeetPlan["YOA"]) else BPItoMeetPlan["YOA"].max()
    bp_roc_year = yoa if yoa in list(BPItoMeetROC["YOA"]) else BPItoMeetROC["YOA"].max()
    
    hull.business_plan_bpi = look_up(bp_plan_year, "YOA", "Airlines Hull", BPItoMeetPlan, if_not_found=1, lookup_type="single")
    liab.business_plan_bpi = look_up(bp_plan_year, "YOA", "Airlines Liab", BPItoMeetPlan, if_not_found=1, lookup_type="single")
    hull.roc_bpi = look_up(bp_roc_year, "YOA", "Airlines Hull", BPItoMeetROC, if_not_found=1, lookup_type="single")
    liab.roc_bpi = look_up(bp_roc_year, "YOA", "Airlines Liab", BPItoMeetROC, if_not_found=1, lookup_type="single")

    # TPI
    hull_el_cost = hull.benchmark_premium * (1 - hull.brokerage) * benchmark_lr
    liab_el_cost = liab.benchmark_premium * (1 - liab.brokerage) * benchmark_lr
    layer.expected_loss_cost = hull_el_cost + liab_el_cost
    
    hull.technical_premium = calculate_technical_premium(hxd, hull_el_cost, written_line=hull.written_line, brokerage=hull.brokerage, bp_class="Aviation PD")
    liab.technical_premium = calculate_technical_premium(hxd, liab_el_cost, written_line=liab.written_line, brokerage=liab.brokerage, bp_class="Aviation Liab")
    tot.technical_premium = hull.technical_premium + liab.technical_premium

    hull.technical_premium_pre_uw_adj = ratio(hull.technical_premium, hull.uw_adj_impact)
    liab.technical_premium_pre_uw_adj = ratio(liab.technical_premium, liab.uw_adj_impact)
    tot.technical_premium_pre_uw_adj = hull.technical_premium_pre_uw_adj + liab.technical_premium_pre_uw_adj

    for cvg in coverages:
        cvg.tpi = ratio(cvg.quoted_premium, cvg.technical_premium)
        cvg.tpi_pre_uw_adj = ratio(cvg.quoted_premium, cvg.technical_premium_pre_uw_adj)

    # Overall Summary
    layer.written_line = ratio(
        hull.written_line * hull.quoted_premium + liab.written_line * liab.quoted_premium, 
        hull.quoted_premium + liab.quoted_premium
    )
    layer.brokerage = ratio(
        hull.brokerage * hull.quoted_premium + liab.brokerage * liab.quoted_premium, 
        hull.quoted_premium + liab.quoted_premium
    )

    # --- Rater priced
    if hxd.cds.standard_fields.is_rater_priced:
        layer.quoted_premium = tot.quoted_premium
        quoted_premium_net = layer.quoted_premium * (1 - layer.brokerage)
        
        layer.benchmark_premium = tot.benchmark_premium
        layer.bpi = tot.bpi
        layer.technical_premium = tot.technical_premium
        layer.technical_premium_pre_uw_adj = tot.technical_premium_pre_uw_adj
        layer.tpi = tot.tpi
        layer.tpi_pre_uw_adj = tot.tpi_pre_uw_adj

        layer.pflr = tot.pflr
        layer.uw_adj_impact = ratio(tot.technical_premium, tot.technical_premium_pre_uw_adj)
        layer.roc = ratio(
            1 - layer.pflr - tp["var_exp"] + tp["inv_inc"] - (tp["cost_of_ri"] - tp["ri_rec"]) - ratio(tp["fixed_exp"] + layer.expected_loss_cost * tp["che"], quoted_premium_net),
            tp["capital_req"]
        )

    # --- Case priced
    elif hxd.cds.standard_fields.is_case_priced and layer.quoted_premium_case_priced:
        layer.bpi = layer.bpi_case_priced
        layer.benchmark_premium = ratio(layer.quoted_premium_case_priced, layer.bpi)
        
        layer.expected_loss_cost = layer.benchmark_premium * benchmark_lr * (1 - layer.brokerage)
        
        layer.technical_premium = calculate_technical_premium(hxd, layer.expected_loss_cost)
        layer.technical_premium_net = layer.technical_premium * (1 - layer.brokerage)  
        layer.tpi = ratio(layer.quoted_premium_case_priced, layer.technical_premium)
        layer.tpi_pre_uw_adj = layer.tpi
        layer.technical_premium_pre_uw_adj = layer.technical_premium

        # Additional metrics for CDS
        layer.pflr = ratio(benchmark_lr, layer.bpi)
        quoted_premium_net = layer.quoted_premium_case_priced * (1 - layer.brokerage)
        layer.roc = ratio(
            1 - layer.pflr - tp["var_exp"] + tp["inv_inc"] - (tp["cost_of_ri"] - tp["ri_rec"]) - ratio(tp["fixed_exp"] + layer.expected_loss_cost * tp["che"], quoted_premium_net),
            tp["capital_req"]
        )

    # Store annualised premiums for use in rate change calcs
    levels = [layer, hull, liab]

    for level in levels:
        level.quoted_premium_annualised = ratio(level.quoted_premium or 0, term, if_undefined=level.quoted_premium)
        level.benchmark_premium_annualised = ratio(level.benchmark_premium or 0, term, if_undefined=level.benchmark_premium)


    
    
    
