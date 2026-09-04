import hx
import pandas as pd
import numpy as np
import math as math
from operator import itemgetter
import datetime
from mailmerge import MailMerge
import os


def generate_uw_doc(hxd, progress):
    cds     = hxd.cds
    tech    = cds.rating_summary.technical
    att     = cds.rating_summary.summary_ratios.attritional
    lrg     = cds.rating_summary.summary_ratios.large
    cat     = cds.rating_summary.summary_ratios.catastrophe
    tot     = cds.rating_summary.summary_ratios.total
    kpi     = cds.rating_summary.kpi

    status              = cds.layers[0].status
    insured_name        = cds.standard_fields.insured_name
    facility_reference  = cds.standard_fields.facility_reference
    inception_date      = hxd.hx_core.inception_date.strftime("%d %b %Y")
    expiry_date         = hxd.hx_core.expiry_date.strftime("%d %b %Y")
    underwriter         = cds.standard_fields.underwriter
    total_deductions    = f"{cds.layers[0].total_deductions * 100:,.2f}%"   if cds.layers[0].total_deductions is not None else ""
    share               = f"{cds.layers[0].written_line * 100:,.2f}%"       if cds.layers[0].written_line is not None else ""

    ggwp_100_q          = f"${tech.gg_premium_quoted_100_pct:,.0f}"         if tech.gg_premium_quoted_100_pct is not None else ""
    gnwp_100_q          = f"${tech.gn_premium_quoted_exc_pc_100_pct:,.0f}"  if tech.gn_premium_quoted_exc_pc_100_pct is not None else ""
    ggwp_afb_q          = f"${tech.gg_premium_quoted_afb:,.0f}"             if tech.gg_premium_quoted_afb is not None else ""
    gnwp_afb_q          = f"${tech.gn_premium_quoted_exc_pc_afb:,.0f}"      if tech.gn_premium_quoted_exc_pc_afb is not None else ""

    ggwp_100_t          = f"${tech.amts_pst_uw_adj.gg_premium_tech_100_pct:,.0f}"           if tech.amts_pst_uw_adj.gg_premium_tech_100_pct is not None else ""
    gnwp_100_t          = f"${tech.amts_pst_uw_adj.gn_premium_tech_exc_pc_100_pct:,.0f}"    if tech.amts_pst_uw_adj.gn_premium_tech_exc_pc_100_pct is not None else ""
    ggwp_afb_t          = f"${tech.amts_pst_uw_adj.gg_premium_tech_afb:,.0f}"               if tech.amts_pst_uw_adj.gg_premium_tech_afb is not None else ""
    gnwp_afb_t          = f"${tech.amts_pst_uw_adj.gn_premium_tech_exc_pc_afb:,.0f}"        if tech.amts_pst_uw_adj.gn_premium_tech_exc_pc_afb is not None else ""

    ggwp_100_b          = f"${tech.amts_pst_uw_adj.gg_premium_bench_100_pct:,.0f}"          if tech.amts_pst_uw_adj.gg_premium_bench_100_pct is not None else ""
    gnwp_100_b          = f"${tech.amts_pst_uw_adj.gn_premium_bench_exc_pc_100_pct:,.0f}"   if tech.amts_pst_uw_adj.gn_premium_bench_exc_pc_100_pct is not None else ""
    ggwp_afb_b          = f"${tech.amts_pst_uw_adj.gg_premium_bench_afb:,.0f}"              if tech.amts_pst_uw_adj.gg_premium_bench_afb is not None else ""
    gnwp_afb_b          = f"${tech.amts_pst_uw_adj.gn_premium_bench_exc_pc_afb:,.0f}"       if tech.amts_pst_uw_adj.gn_premium_bench_exc_pc_afb is not None else ""

    gglr_pre_att        = f"{att.gg_pre_uw_adj.ulr_final * 100:,.2f}%"      if att.gg_pre_uw_adj.ulr_final is not None else ""
    gnlr_pre_att        = f"{att.gn_pre_uw_adj.ulr_final * 100:,.2f}%"      if att.gn_pre_uw_adj.ulr_final is not None else ""
    gglr_pst_att        = f"{att.gg_pst_uw_adj.ulr_final * 100:,.2f}%"      if att.gg_pst_uw_adj.ulr_final is not None else ""
    gnlr_pst_att        = f"{att.gn_pst_uw_adj.ulr_final * 100:,.2f}%"      if att.gn_pst_uw_adj.ulr_final is not None else ""

    gglr_pre_lrg        = f"{lrg.gg_pre_uw_adj.ulr_final * 100:,.2f}%"      if lrg.gg_pre_uw_adj.ulr_final is not None else ""
    gnlr_pre_lrg        = f"{lrg.gn_pre_uw_adj.ulr_final * 100:,.2f}%"      if lrg.gn_pre_uw_adj.ulr_final is not None else ""
    gglr_pst_lrg        = f"{lrg.gg_pst_uw_adj.ulr_final * 100:,.2f}%"      if lrg.gg_pst_uw_adj.ulr_final is not None else ""
    gnlr_pst_lrg        = f"{lrg.gn_pst_uw_adj.ulr_final * 100:,.2f}%"      if lrg.gn_pst_uw_adj.ulr_final is not None else ""

    gglr_pre_cat        = f"{cat.gg_pre_uw_adj.ulr_final * 100:,.2f}%"      if cat.gg_pre_uw_adj.ulr_final is not None else ""
    gnlr_pre_cat        = f"{cat.gn_pre_uw_adj.ulr_final * 100:,.2f}%"      if cat.gn_pre_uw_adj.ulr_final is not None else ""
    gglr_pst_cat        = f"{cat.gg_pst_uw_adj.ulr_final * 100:,.2f}%"      if cat.gg_pst_uw_adj.ulr_final is not None else ""
    gnlr_pst_cat        = f"{cat.gn_pst_uw_adj.ulr_final * 100:,.2f}%"      if cat.gn_pst_uw_adj.ulr_final is not None else ""

    gglr_pre_tot        = f"{tot.gg_pre_uw_adj.ulr_priced_final * 100:,.2f}%"             if tot.gg_pre_uw_adj.ulr_priced_final is not None else ""
    gnlr_pre_tot        = f"{tot.gn_pre_uw_adj.ulr_priced_final_exc_pc * 100:,.2f}%"      if tot.gn_pre_uw_adj.ulr_priced_final_exc_pc is not None else ""
    gglr_pst_tot        = f"{tot.gg_pst_uw_adj.ulr_priced_final * 100:,.2f}%"             if tot.gg_pst_uw_adj.ulr_priced_final is not None else ""
    gnlr_pst_tot        = f"{tot.gn_pst_uw_adj.ulr_priced_final_exc_pc * 100:,.2f}%"      if tot.gn_pst_uw_adj.ulr_priced_final_exc_pc is not None else ""

    uwadj_att           = f"{att.uw_adjustment * 100:,.2f}%"                if att.uw_adjustment is not None else ""
    uwadj_lrg           = f"{lrg.uw_adjustment * 100:,.2f}%"                if lrg.uw_adjustment is not None else ""
    uwadj_cat           = f"{cat.uw_adjustment * 100:,.2f}%"                if cat.uw_adjustment is not None else ""

    profit_pre          = f"${kpi.pre_uw_adj.expected_profit:,.0f}"         if kpi.pre_uw_adj.expected_profit is not None else ""
    capital_pre         = f"${kpi.pre_uw_adj.allocated_capital:,.0f}"       if kpi.pre_uw_adj.allocated_capital is not None else ""
    roc_pre             = f"{kpi.pre_uw_adj.roc * 100:,.2f}%"               if kpi.pre_uw_adj.roc is not None else ""
    bpi_pre             = f"{kpi.pre_uw_adj.bpi * 100:,.2f}%"               if kpi.pre_uw_adj.bpi is not None else ""
    tpi_pre             = f"{kpi.pre_uw_adj.tpi * 100:,.2f}%"               if kpi.pre_uw_adj.tpi is not None else ""


    profit_pst          = f"${kpi.pst_uw_adj.expected_profit:,.0f}"         if kpi.pst_uw_adj.expected_profit is not None else ""
    capital_pst         = f"${kpi.pst_uw_adj.allocated_capital:,.0f}"       if kpi.pst_uw_adj.allocated_capital is not None else ""
    roc_pst             = f"{kpi.pst_uw_adj.roc * 100:,.2f}%"               if kpi.pst_uw_adj.roc is not None else ""
    bpi_pst             = f"{kpi.pst_uw_adj.bpi * 100:,.2f}%"               if kpi.pst_uw_adj.bpi is not None else ""
    tpi_pst             = f"{kpi.pst_uw_adj.tpi * 100:,.2f}%"               if kpi.pst_uw_adj.tpi is not None else ""

    pc_pct              = f"{tech.percent_pc * 100:,.2f}%"                  if tech.percent_pc is not None else ""
    pc_amt_100          = f"${tech.amount_pc_100:,.0f}"                     if tech.amount_pc_100 is not None else ""
    pc_amt_afb          = f"${tech.amount_pc_afb:,.0f}"                     if tech.amount_pc_afb is not None else ""
    rationale           = cds.standard_fields.uw_rationale
    actuary_review      = cds.rationale.actuarial_review
    
    rate_change         = f"{cds.layers[0].rate_change.rate_change.uw_selected * 100:,.2f}%" if cds.layers[0].rate_change.rate_change.uw_selected is not None else ""
    

    path = "uw_doc_template.docx"
    template = os.path.join(os.path.dirname(__file__), path)
    document = MailMerge(template)

    document.merge( status              = status
                   , insured_name       = insured_name
                   , facility_reference = facility_reference
                   , inception_date     = inception_date
                   , expiry_date        = expiry_date
                   , underwriter        = underwriter
                   , total_deductions   = total_deductions
                   , ggwp_100_q         = ggwp_100_q    #quote - name abbreviated as mailmerge resizes larger names 
                   , ggwp_100_t         = ggwp_100_t    #tech  - name abbreviated as mailmerge resizes larger names 
                   , ggwp_100_b         = ggwp_100_b    #bench - name abbreviated as mailmerge resizes larger names 
                   , gnwp_100_q         = gnwp_100_q    #quote - name abbreviated as mailmerge resizes larger names 
                   , gnwp_100_t         = gnwp_100_t    #tech  - name abbreviated as mailmerge resizes larger names 
                   , gnwp_100_b         = gnwp_100_b    #bench - name abbreviated as mailmerge resizes larger names 
                   , share              = share
                   , ggwp_afb_q         = ggwp_afb_q    #quote - name abbreviated as mailmerge resizes larger names 
                   , ggwp_afb_t         = ggwp_afb_t    #tech  - name abbreviated as mailmerge resizes larger names 
                   , ggwp_afb_b         = ggwp_afb_b    #bench - name abbreviated as mailmerge resizes larger names 
                   , gnwp_afb_q         = gnwp_afb_q    #quote - name abbreviated as mailmerge resizes larger names 
                   , gnwp_afb_t         = gnwp_afb_t    #tech  - name abbreviated as mailmerge resizes larger names 
                   , gnwp_afb_b         = gnwp_afb_b    #bench - name abbreviated as mailmerge resizes larger names 
                   , gglr_pre_att       = gglr_pre_att
                   , gglr_pre_lrg       = gglr_pre_lrg
                   , gglr_pre_cat       = gglr_pre_cat
                   , gglr_pre_tot       = gglr_pre_tot
                   , gnlr_pre_att       = gnlr_pre_att
                   , gnlr_pre_lrg       = gnlr_pre_lrg
                   , gnlr_pre_cat       = gnlr_pre_cat
                   , gnlr_pre_tot       = gnlr_pre_tot
                   , uwadj_att          = uwadj_att
                   , uwadj_lrg          = uwadj_lrg
                   , uwadj_cat          = uwadj_cat
                   , gglr_pst_att       = gglr_pst_att
                   , gglr_pst_lrg       = gglr_pst_lrg
                   , gglr_pst_cat       = gglr_pst_cat
                   , gglr_pst_tot       = gglr_pst_tot
                   , gnlr_pst_att       = gnlr_pst_att
                   , gnlr_pst_lrg       = gnlr_pst_lrg
                   , gnlr_pst_cat       = gnlr_pst_cat
                   , gnlr_pst_tot       = gnlr_pst_tot
                   , profit_pre         = profit_pre
                   , capital_pre        = capital_pre
                   , roc_pre            = roc_pre
                   , bpi_pre            = bpi_pre
                   , tpi_pre            = tpi_pre
                   , profit_pst         = profit_pst
                   , capital_pst        = capital_pst
                   , roc_pst            = roc_pst
                   , bpi_pst            = bpi_pst
                   , tpi_pst            = tpi_pst
                   , pc_pct             = pc_pct
                   , pc_amt_100         = pc_amt_100
                   , pc_amt_afb         = pc_amt_afb
                   , rationale          = rationale
                   , actuary_review     = actuary_review
                   , rate_change        = rate_change
    )

    with hxd.uw_doc_template.open("b") as f:
        document.write(f)