import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_z_utilities as utils
from operator import itemgetter
import datetime
from mailmerge import MailMerge
import os

def rate_rationale(hxd, df):
    cds = hxd.cds
    layer = cds.layers[0]
    cov = layer.coverages
    rc = layer.rate_change
    
    # INSURED DETAILS ----------------------------
    cds.rationale.insured_name = cds.risk_info.insured_name_final
    cds.rationale.inception_date = hxd.hx_core.inception_date
    cds.rationale.policy_ref = cds.standard_fields.policy_reference
    
    # RISK OVERVIEW ----------------------------
    cds.rationale.signed_line = cds.final_premium_summary_table.signed_line if cds.final_premium_summary_table.signed_line is not None else 0
    cds.rationale.limit = layer.limit if layer.limit is not None else 0
    cds.rationale.deductions = cds.final_premium_summary_table.acq_cost if cds.final_premium_summary_table.acq_cost is not None else 0

    # Assign value to written line to align with other raters
    cds.rationale.written_line = cds.final_premium_summary_table.signed_line

    tsi_final = cds.final_claims_summary_table.tsi if cds.final_claims_summary_table.tsi is not None else 0 

    if tsi_final == 0:
        cds.rationale.avg_model_rate = 0.0
    else:
        cds.rationale.avg_model_rate = (cds.final_prem_summary_tp_postuwadj_table.tech_prem / cds.final_claims_summary_table.tsi)

    cds.rationale.avg_uw_rate = cds.final_premium_summary_table.gg_achieved_rate if cds.final_premium_summary_table.gg_achieved_rate is not None else 0
    cds.rationale.epi = layer.quoted_premium if layer.quoted_premium is not None else 0
    cds.rationale.rate_change = rc.rate_change.uw_selected if rc.rate_change.uw_selected is not None else 0
    cds.rationale.cat_load = cds.final_claims_summary_table.perc_cat_sel if cds.final_claims_summary_table.perc_cat_sel is not None else 0

    final_lost_cost = cds.final_claims_summary_table.final_loss_cost if cds.final_claims_summary_table.final_loss_cost is not None else 0
    cds.rationale.attr_lr = (final_lost_cost * (1 - cds.rationale.cat_load)) / cds.rationale.epi if cds.rationale.epi > 0 else 0

    cds.rationale.bpi = layer.bpi if layer.bpi is not None else 0
    cds.rationale.tpi = layer.tpi if layer.tpi is not None else 0
    cds.rationale.roc = layer.roc if layer.roc is not None else 0

    pass

def generate_rationale_doc(hxd, progress):
    cds = hxd.cds

    insured_name = cds.rationale.insured_name
    inception_date = cds.rationale.inception_date.strftime("%d %b %Y")
    reference = cds.rationale.policy_ref
    risk_background = cds.rationale.coverholder_background
    risk_type = cds.rationale.risk_type
    construction = cds.rationale.construction
    signed_line = f"{cds.rationale.signed_line * 100:,.2f}%" if cds.rationale.signed_line is not None else ""
    writen_line = signed_line
    limit = f"${cds.rationale.limit:,.0f}" if cds.rationale.limit is not None else ""
    deductions = f"{cds.rationale.deductions * 100:,.2f}%" if cds.rationale.deductions is not None else ""
    average_limit = f"${cds.rationale.avg_limit:,.0f}" if cds.rationale.avg_limit is not None else ""
    top_country = cds.rationale.top_country
    avg_tech_rate = f"{cds.rationale.avg_model_rate * 100:,.2f}%" if cds.rationale.avg_model_rate is not None else ""
    avg_achieved_rate = f"{cds.rationale.avg_uw_rate * 100:,.2f}%" if cds.rationale.avg_uw_rate is not None else ""
    epi = f"${cds.rationale.epi:,.0f}" if cds.rationale.epi is not None else ""
    rate_change = f"{cds.rationale.rate_change * 100:,.0f}%" if cds.rationale.rate_change is not None else ""
    attr_loss_ratio = f"{cds.rationale.attr_lr * 100:,.0f}%" if cds.rationale.attr_lr is not None else ""
    cat_load = f"{cds.rationale.cat_load * 100:,.0f}%" if cds.rationale.cat_load is not None else ""
    bpi = f"{cds.rationale.bpi * 100:,.0f}%" if cds.rationale.bpi is not None else ""
    tpi = f"{cds.rationale.tpi * 100:,.0f}%" if cds.rationale.tpi is not None else ""
    roc = f"{cds.rationale.roc * 100:,.0f}%" if cds.rationale.roc is not None else ""
    underwriter_commentary = cds.rationale.uw_comments
    rate_change_rationale = cds.rationale.rate_change_rationale
    terms_and_conditions_change = cds.rationale.tnc_change
    risk_profile = cds.rationale.risk_profile
    territory_profile = cds.rationale.territory_and_agg_dist
    exposure_change = cds.rationale.exposure_change
    large_losses = cds.rationale.large_losses

    path = "uwr_template.docx"
    template = os.path.join(os.path.dirname(__file__), path)
    document = MailMerge(template)

    document.merge(
        insured_name = insured_name,
        inception_date = inception_date,
        reference = reference,
        risk_background = risk_background,
        risk_type = risk_type,
        construction = construction,
        signed_line = signed_line,
        limit = limit,
        deductions = deductions,
        average_limit = average_limit,
        top_country = top_country,
        avg_tech_rate = avg_tech_rate,
        avg_achieved_rate = avg_achieved_rate,
        epi = epi,
        rate_change = rate_change,
        attr_loss_ratio = attr_loss_ratio,
        cat_load = cat_load,
        bpi = bpi,
        tpi = tpi,
        roc = roc,
        underwriter_commentary = underwriter_commentary,
        rate_change_rationale = rate_change_rationale,
        terms_and_conditions_change = terms_and_conditions_change,
        risk_profile = risk_profile,
        territory_profile = territory_profile,
        exposure_change = exposure_change,
        large_losses = large_losses,
    )

    with hxd.rationale_file.open("b") as f:
        document.write(f)