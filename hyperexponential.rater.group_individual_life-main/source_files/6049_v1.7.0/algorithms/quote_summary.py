import hx
import json
from datetime import datetime
import pandas as pd
import numpy as np
import math as math
from dateutil.relativedelta import relativedelta
from algorithms.rate_utilities import year_diff, one_layer, pd_df_from_hx_list, rgetattr
from algorithms.data_schema.sch_rater_defined import coverages_dict


def quote_summary(hxd):
    layer, cvg = one_layer(hxd)
    db = cvg.death

    inception_date = hxd.hx_core.inception_date
    expiry_date = hxd.hx_core.expiry_date
    sf = hxd.cds.standard_fields
    q = hxd.cds.quote

    expo = hxd.cds.exposure.granular
    expe = hxd.cds.experience_rating

    # Get DataFrame with exposures
    lives = expo.lives
    lives_df = pd_df_from_hx_list(lives)

    if lives_df.empty or not hxd.cds.cover_selection.are_db_fields_full:
        return
    
    # Policy details
    q.insured_name = sf.insured_name
    cover_type = db.cover_type if db.cover_type == "Any Cause" else "Natural Causes"
    q.cover = "Death by " + cover_type
    q.term = 12 * year_diff(start_date=inception_date, end_date=expiry_date, for_term=True)

    # Risk details
    q.max_age_attained.calculated = max(lives_df["age_attained"])
    q.no_lives = sum(lives_df["no_lives"])
    q.max_aol_sum_insured.calculated = max(lives_df["salary"] * lives_df["salary_multiple"])
    q.total_sum_insured = sum(lives_df["sum_insured"])

    # Financial details
    q.adjustable_rate = layer.totals.total.quoted_rate
    q.commission = layer.brokerage

    q.valid_until_date = hxd.cds.policy_info.application_date + relativedelta(days=30)


def format_date(date):
    date_str = str(date)
    formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")

    return formatted_date

# Create data dictionary to write to Excel file
def create_dict_for_excel(hxd):
    layer, cvg = one_layer(hxd)

    adb = cvg.additional_death
    ti = cvg.terminal_illness
    ci = cvg.critical_illness
    re = cvg.repat_exp

    q = hxd.cds.quote

    # Get selected exclusions and conditions
    exclusions = ""
    conditions = ""

    for excl in q.exclusions:
        if excl.is_excluded:
            exclusions += f"- {excl.exclusion} \n"

    for cond in q.conditions:
        if cond.is_included:
            conditions += f"- {cond.condition} \n"

    # Add notes for additional benefits
    add_cvg_dict = coverages_dict.copy()
    add_cvg_dict.pop("death")
    add_cvg_bools = [rgetattr(cvg, f"{cover}/is_covered") for cover in add_cvg_dict.keys()]

    if any(add_cvg_bools):
        cvg_notes = "Additional benefits covered:\n"
        
        for cover, view in add_cvg_dict.items():
            if rgetattr(cvg, f"{cover}/is_covered"):
                label = view.get("label").replace("\n", " ")
                cvg_notes += f"- {label}\n"

        clean_uw_notes = q.uw_notes or ""
        uw_notes = f"{cvg_notes}\n{clean_uw_notes}"
    else:
        uw_notes = q.uw_notes

    term = q.term or 0 # Avoid None error
    data = {
        "reinsured_name": q.reinsured_name,
        "insured_name": q.insured_name,
        "cover": q.cover,
        "term": str(int(term)) + " months",
        "max_age_attained": q.max_age_attained.selected,
        "no_lives": q.no_lives,
        "sum_insured_basis": q.sum_insured_basis,
        "max_aol_sum_insured": q.max_aol_sum_insured.selected,
        "free_cover_limit": q.free_cover_limit,
        "total_sum_insured": q.total_sum_insured,
        "event_limit": q.event_limit or "N/A",
        "deposit_premium": q.deposit_premium,
        "adjustable_rate": q.adjustable_rate,
        "commission": q.commission,
        "exclusions": exclusions,
        "conditions": conditions,
        "valid_until_date": format_date(q.valid_until_date),
        "uw_notes": uw_notes,
        "currency": hxd.cds.currencies.source_currency
    }

    json_data = json.dumps(data)

    return json_data

# Push dictionary to hxd for storage
def store_policy_data(hxd):
    # Only run when Group selected
    if hxd.cds.is_individual:
        return
        
    layer = hxd.cds.layers[0]

    # Don't run if premium has not been calculated
    if layer.quoted_premium is None:
        return

    data = create_dict_for_excel(hxd)
    hxd.policy_doc.data_dict = data

    # Compare task data with live data to unhide download button
    task_data = hxd.policy_doc.task_data_dict
    hxd.policy_doc.show_download = True if data == task_data else False