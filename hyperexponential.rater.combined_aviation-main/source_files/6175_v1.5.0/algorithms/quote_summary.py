import hx
import json
from datetime import datetime
import pandas as pd
import numpy as np
import math as math
from dateutil.relativedelta import relativedelta
from algorithms.rate_utilities import year_diff, one_layer, pd_df_from_hx_list


def quote_summary(hxd):
    layer, cvg = one_layer(hxd)
    
    pass


def format_date(date):
    date_str = str(date)
    formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")

    return formatted_date

# Create data dictionary to write to Excel file
def create_dict_for_excel(hxd):
    cds = hxd.cds
    sf = cds.standard_fields
    
    layer, cvg = one_layer(hxd)
    hull = cvg.hull
    liab = cvg.liability
    tot = layer.totals

    p_id = hx.meta.policy_id
    po_id = hx.meta.policy_option_id
    insured_name = sf.insured_name or "Unnamed Insured"

    data = {
        "name": f"Combined Aviation Rater - {insured_name}",
        "policy_reference": sf.policy_reference,
        "source_currency": cds.currencies.source_currency,
        "policy_url": f"https://www.beazley.hxrenew.com/policies/{p_id}/options/{po_id}",
        # Cover
        "hull_benchmark_premium_pre_exp": hull.benchmark_premium_pre_exp,
        "pax_benchmark_premium_pre_exp": liab.pax.benchmark_premium_pre_exp,
        "tpl_benchmark_premium_pre_exp": liab.tpl.benchmark_premium_pre_exp,
        "hull_benchmark_rate_pre_exp": hull.benchmark_rate_pre_exp,
        "pax_benchmark_rate_pre_exp": liab.pax.benchmark_rate_pre_exp,
        "tpl_benchmark_rate_pre_exp": liab.tpl.benchmark_rate_pre_exp,
        # Experience Rating
        "hull_benchmark_premium_exp": hull.benchmark_premium_exp,
        "hull_exp_credibility": hull.exp_credibility,
        "hull_benchmark_premium_pre_uw_adj": hull.benchmark_premium_pre_uw_adj,
        "liab_benchmark_premium_exp": liab.benchmark_premium_exp,
        "liab_exp_credibility": liab.exp_credibility,
        "liab_benchmark_premium_pre_uw_adj": liab.benchmark_premium_pre_uw_adj,
        "liab_min_rate_info": liab.min_rate_info or "",
        # UW Adjustment
        "pilot_uw_adj": layer.pilot_uw_adj,
        "hull_uw_adj": hull.uw_adj,
        "liab_uw_adj": liab.uw_adj,
        "uw_rationale": sf.uw_rationale,
        "hull_benchmark_premium_post_uw_adj": hull.benchmark_premium_post_uw_adj,
        "hull_uw_adj_impact": hull.uw_adj_impact,
        "liab_benchmark_premium_post_uw_adj": liab.benchmark_premium_post_uw_adj,
        "liab_uw_adj_impact": liab.uw_adj_impact,
        # BPI
        "hull_benchmark_premium": hull.benchmark_premium,
        "hull_quoted_premium": hull.quoted_premium,
        "hull_pflr": hull.pflr,
        "hull_pflr_net": hull.pflr_net,
        "hull_bpi": hull.bpi,
        "hull_business_plan_bpi": hull.business_plan_bpi,
        "hull_roc_bpi": hull.roc_bpi,
        "liab_benchmark_premium": liab.benchmark_premium,
        "liab_quoted_premium": liab.quoted_premium,
        "liab_pflr": liab.pflr,
        "liab_pflr_net": liab.pflr_net,
        "liab_bpi": liab.bpi,
        "liab_business_plan_bpi": liab.business_plan_bpi,
        "liab_roc_bpi": liab.roc_bpi,
        "tot_benchmark_premium": tot.benchmark_premium,
        "tot_quoted_premium": tot.quoted_premium,
        "tot_pflr": tot.pflr,
        "tot_pflr_net": tot.pflr_net,
        "tot_bpi": tot.bpi,
        # TPI
        "hull_technical_premium": hull.technical_premium,
        "hull_technical_premium_pre_uw_adj": hull.technical_premium_pre_uw_adj,
        "hull_tpi": hull.tpi,
        "hull_tpi_pre_uw_adj": hull.tpi_pre_uw_adj,
        "liab_technical_premium": liab.technical_premium,
        "liab_technical_premium_pre_uw_adj": liab.technical_premium_pre_uw_adj,
        "liab_tpi": liab.tpi,
        "liab_tpi_pre_uw_adj": liab.tpi_pre_uw_adj,
        "tot_technical_premium": tot.technical_premium,
        "tot_technical_premium_pre_uw_adj": tot.technical_premium_pre_uw_adj,
        "tot_tpi": tot.tpi,
        "tot_tpi_pre_uw_adj": tot.tpi_pre_uw_adj
    }

    json_data = json.dumps(data)

    return json_data

# Push dictionary to hxd for storage
def store_policy_data(hxd):
    layer = hxd.cds.layers[0]

    # Don't run if premium has not been calculated
    if layer.quoted_premium is None:
        return

    data = create_dict_for_excel(hxd)
    hxd.policy_doc.data_dict = data

    # Compare task data with live data to unhide download button
    task_data = hxd.policy_doc.task_data_dict
    hxd.policy_doc.show_download = True if data == task_data else False