import hx
import pandas as pd
import numpy as np
import re

def rate_validations(hxd):

    # set dataframe variables for cleaner code 
    cds = hxd.cds
    layers = cds.layers

    total_error_count = 0

    # Insured name must be completed, this is needed to ensure landing page works correctly
    if not cds.standard_fields.insured_name:
        hx.errors.validation("Insured name field must be completed.")
        total_error_count += 1

    if not cds.standard_fields.underwriter:
        hx.errors.validation(f"An Underwriter (Risk Information Tab) must be entered.")
        total_error_count += 1

    if not cds.hours_clause:
        hx.errors.validation(f"Hours clause (Risk Information Tab) must be entered.")
        total_error_count += 1

    if not cds.sanctions_clause:
        hx.errors.validation(f"Sanctions clause (Risk Information Tab) must be entered.")
        total_error_count += 1

    if not cds.terrorism_code:
        hx.errors.validation(f"Terrorism code (Risk Information Tab) must be entered.")
        total_error_count += 1

    if not cds.cyber_code:
        hx.errors.validation(f"Cyber code (Risk Information Tab) must be entered.")
        total_error_count += 1

    if not cds.com_disease:
        hx.errors.validation(f"Com disease (Risk Information Tab) must be entered.")
        total_error_count += 1

    if cds.risk_carrier == "Bermuda" and not cds.discussed_london :
        hx.errors.validation(f"Must be discussed with London office (Risk Information Tab).")
        total_error_count += 1

    if not cds.send_rate_change.confirm_area_codes:
        hx.errors.validation(f"Area codes (Area Codes Tab) must be confirmed.")
        total_error_count += 1

    if not cds.generate_tags_run:
        hx.errors.validation(f"Generate Tags task must be run (Risk Information Tab).")
        total_error_count += 1


    if cds.programme != "Risk XL":

        if not cds.peril_allocation_account_level.skip_peril_allocation:
            if (not cds.send_rate_change.peril_allocation_run):
                hx.errors.validation(f"Peril allocation task (Peril Allocation Tab) must be run.")
                total_error_count += 1

        if not cds.send_rate_change.confirm_rms_el_allocation:
            hx.errors.validation(f"RMS EL allocation (Modelling Tab) must be confirmed.")
            total_error_count += 1


    # Matches reference
    reference_format = "......\d\d...."
    format_description = "6 char of any type, 2 digits and 4 chars of any type"

    pol_error_count = 0

    for layer in layers:
        if (layer.section_reference is not None) and (layer.section_reference != "") and (not re.fullmatch(reference_format, layer.section_reference)):
            pol_error_count += 1
            
    if pol_error_count > 0:
        hx.errors.validation(f"All entered section reference's (Risk Information Tab) must be in the format of {format_description}")
    

    total_error_count += pol_error_count

    cds.send_rate_change.total_error_count = total_error_count