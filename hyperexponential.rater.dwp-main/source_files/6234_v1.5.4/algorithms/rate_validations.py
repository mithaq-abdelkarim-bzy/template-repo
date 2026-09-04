import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import ratio
from operator import itemgetter

def rate_validations(hxd):

    # Insured name must be completed, this is needed to ensure landing page works correctly
    if not hxd.cds.standard_fields.insured_name:
        hx.errors.validation("Insured name field must be completed.")

    # Must provide a comment if there is an uw adjustment provided
    if hxd.cds.modifiers.underwriter_adjustment:
        if hxd.cds.modifiers.underwriter_adjustment != 0 and (hxd.cds.uw_rationale.comments is None or hxd.cds.uw_rationale.comments == ''):
            hx.errors.validation("Underwriter adjustment applied. Please provide a comment.")
    
    # Validation to check how many layers are set as bound
    bound_count = 0
    for layer in hxd.cds.layers:
        if layer.status in ["Bound", "Post Bind Complete"]:
            bound_count += 1
    
    if bound_count == 0:
        hx.errors.validation("Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final")
    elif bound_count > 1:
        hx.errors.validation("There must be only one bound policy")

    
    # To flag min if min premium has been applied
    layer = hxd.cds.layers[0]

    if layer.model_premium and layer.technical_premium:
        if layer.min_premium.flag:
            hxd.messages.min_premium_note = "⚠️ Minimum premium applied."


    # To ensure comment is put in for the extensions covered selection
    if not hxd.cds.rating_factors.extensions_covered == 0:
        hxd.flags.extensions_comment_flag = True
        if not hxd.cds.uw_rationale.extensions_comment:
            hx.errors.validation("An extension is covered but no comment provided. Please enter in the 'Policy Level Information' tab.")
    
    # Validation to ensure all UW rationale is completed for risks above $100k
    if hxd.cds.uw_rationale.is_rationale_required:
        rationale_lst = ['knowledge_of_insured', 'portfolio_fit', 'basis_of_risk_selection', 'complex_considerations', 'facts_affecting_decision']
        for rationale in rationale_lst:
            rationale_obj = getattr(hxd.cds.uw_rationale, rationale)
            if not rationale_obj:
                hx.errors.validation(f"Premium above $100k. Rationale must be provided for {rationale}")
                hxd.flags.validation_count += 1



    # Combine uw rationale
    hxd.cds.standard_fields.uw_rationale = (
        "**Knowledge of the Insured** \n\n"
        + (hxd.cds.uw_rationale.knowledge_of_insured or "") + "\n\n"
        + "**Portfolio Fit**\n\n"
        + (hxd.cds.uw_rationale.portfolio_fit or "") + "\n\n"
        + "**Basis of Risk Selection**\n\n"
        + (hxd.cds.uw_rationale.basis_of_risk_selection or "") + "\n\n"
        + "**Any Unusual or Complex Considerations**\n\n"
        + (hxd.cds.uw_rationale.complex_considerations or "") + "\n\n"
        + "**Any facts which affect Underwriter's decision**\n\n"
        + (hxd.cds.uw_rationale.facts_affecting_decision or "") + "\n\n"
    ) if hxd.cds.uw_rationale.is_rationale_required else ""
    
