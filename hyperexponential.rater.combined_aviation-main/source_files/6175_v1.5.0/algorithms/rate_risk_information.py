import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import year_diff, one_layer, policy_term


def rate_risk_information(hxd):
    cds = hxd.cds
    sf = cds.standard_fields
    layer, cvg = one_layer(hxd)
    hull = cvg.hull
    liab = cvg.liability
    pol = cds.policy_info

    # Assign section ref
    layer.section_reference = cvg.hull.section_reference

    # Set rating methodology
    sf.is_case_priced = hxd.cds.standard_fields.rating_methodology == "Case Priced"
    sf.is_rater_priced = hxd.cds.standard_fields.rating_methodology == "Rater"


    # Calculate term
    pol.term_calculated = policy_term(hxd.hx_core.inception_date, hxd.hx_core.expiry_date)
    pol.is_term_valid = round(pol.term_calculated, 2) == round(pol.term, 2)
    pol.is_term_invalid = not pol.is_term_valid

    message_temp = "Start General Aviation" if hxd.cds.is_ga else "Start Airlines" 

    if pol.is_term_invalid:
        hx.errors.validation(f"Policy term is changed to {round(pol.term_calculated, 2)}, based on the inception and expiry date. Please click the button '{message_temp}' on 'Risk Information' tab to update the term")

    # Check inception date
    product = "General Aviation" if hxd.cds.is_ga else "Airlines"
    if (pol.inception_date_temp is not None) and (pol.inception_date_temp.year != hxd.hx_core.inception_date.year):
        hx.errors.validation(f"Inception date has changed. Please click on 'Start {product}' in Risk Information again.")

    # Validate policy reference and other fields
    finalizable_status = ["Bound", "Post Bind Complete"] 
    if layer.status in finalizable_status:
        if not sf.insured_name:
            hx.errors.validation("Insured Name in Risk Information cannot be empty.")
        if not sf.underwriter:
            hx.errors.validation("Underwriter in Risk Information cannot be empty.")
        if (not hull.section_reference) and (not liab.section_reference):
            hx.errors.validation("Section Reference in Risk Information cannot be empty for both Hull and Liability.")
        if (hull.section_reference is not None) and (len(hull.section_reference) != 12):
            hx.errors.validation(f"Hull Section Reference in Risk Information must have 12 characters. Current input has {len(hull.section_reference)} characters.")
        if (liab.section_reference is not None) and (len(liab.section_reference) != 12):
            hx.errors.validation(f"Liability Section Reference in Risk Information must have 12 characters. Current input has {len(liab.section_reference)} characters.")
        if hxd.cds.exposure.granular.show_check_cols:
            hx.errors.validation("Please untick 'Validate Data' in the Details page before setting the policy to Final.")

    if hull.section_reference:
        sf.policy_reference = hull.section_reference[:8]
    elif liab.section_reference:
        sf.policy_reference = liab.section_reference[:8]

    # Determine BM class
    hxd.cds.standard_fields.benchmark_class = "Aviation PD" # NOTE: not actually used when calculating TP

    # Labels
    yoa = hxd.hx_core.inception_date.year
    cvg.hull.rate_change_label = cvg.liability.rate_change_label = f"{yoa} Rate Change"

    # Calculate net premiums
    cvg.hull.quoted_premium_net = cvg.hull.quoted_premium * (1 - cvg.hull.brokerage)
    cvg.liability.quoted_premium_net = cvg.liability.quoted_premium * (1 - cvg.liability.brokerage)

    # Assign policy currency to cover currency
    cvg.hull.currency.calculated = cvg.liability.currency.calculated = cds.currencies.source_currency

    




    
    