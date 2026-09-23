import hx
import pandas as pd
import numpy as np
import algorithms.utils_global_lists as lst
from algorithms.utils_functions import create_title


def validations(hxd):
    layer = hxd.cds.layers[0]
    exp_agg = hxd.cds.exposure.aggregate
    cov = layer.coverages
    rc = layer.rate_change
    hxd_rc = hxd.rate_change
    std_fields = hxd.cds.standard_fields

    # Add validation for insured name

    if not std_fields.insured_name:
        hx.errors.validation("Enter the insured name in Risk Information")

    # Add validation for Deal Status field

    if layer.status is None:
        hx.errors.validation("Select Deal Status in Risk Information")

    # Add validation for policy reference when bound

    if layer.status == "Bound" and not std_fields.policy_reference:
        hx.errors.validation("Enter the policy reference in Risk Information")

    # Add validation for quota share when matching lead insurer

    if layer.is_follow and not (layer.lead_premium and layer.beazley_share):
        hx.errors.validation("Enter the leader's premium and Beazley's share in Risk Information")

    # Add validation for Exposure Details tab

    if (exp_agg.assets_june == 0 or exp_agg.assets_december == 0):
        hx.errors.validation("Enter both financial statement assets in Exposure Details")
    
    if not std_fields.insured_state_or_province:
        hx.errors.validation("State is missing in Exposure Details")

    if (exp_agg.number_of_employees == 0):
        hx.errors.validation("Enter the number of employees in Exposure Details")

    # Validations for min and max coverage

    for cv, name in zip(lst.cover_hxd_vbl(hxd), lst.cover_names):
        if cv.final_include == True:
            if cv.min_coverage is not None:
                if cv.coverage < cv.min_coverage:
                    hx.errors.validation(f"{name} min coverage not met in Pricing")
            if cv.max_coverage is not None:
                if cv.coverage > cv.max_coverage:
                    hx.errors.validation(f"{name} max coverage exceeded in Pricing")
            if cv.min_deductible is not None:
                if cv.deductible < cv.min_deductible:
                    hx.errors.validation(f"{name} min deductible not met in Pricing")
            if cv.max_deductible is not None:
                if cv.deductible > cv.max_deductible:
                    hx.errors.validation(f"{name} max deductible exceeded in Pricing")
    
    
    # Validations for ensuring comments are added to rate change overrides

    for item in lst.rate_change_list_static:
        rc_vbl = getattr(rc, item)
        if rc_vbl.uw_selected.is_overridden and not rc_vbl.comments :
            hx.errors.validation(f" {create_title(item)} has been overridden and no comment provided in Rate Change!")


    # Add validation for LRE eligibility

    if std_fields.is_admitted_or_surplus == "Admitted - LRE" and std_fields.insured_state_or_province not in lst.lre_states:
        hx.errors.validation("This state is not eligible for LRE")

    # Add validation for Rate Change
    if std_fields.is_renewal:
        if not rc.expiring_premium:
            hx.errors.validation(f"Expiring premium is missing in Rate Change")
        if not rc.expiring_policy_option_id.selected:
            hx.errors.validation(f"Expiring Policy Option is missing in Rate Change")

        if not hxd_rc.cover_1_basic_bond.coverage:
            hx.errors.validation(f"Expiring limit is missing in Rate Change") 
        if not hxd_rc.cover_1_basic_bond.deductible:
            hx.errors.validation(f"Expiring deductible is missing in Rate Change")
        if not (hxd_rc.financial_assets_june_rc or hxd_rc.financial_assets_dec_rc):
            hx.errors.validation(f"Expiring financial assets is missing in Rate Change")
        if not hxd_rc.number_of_employees_rc:
            hx.errors.validation(f"Expiring number of employees is missing in Rate Change")


    pass

