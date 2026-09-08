import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import year_diff


def rate_risk_information(hxd):
    layer = hxd.cds.layers[0]
    ref_characters = len(layer.non_eea_section_reference.ref) if layer.has_double_section_ref else len(layer.single_section_reference.ref)

    # Extracts database id for the risk information tab
    hxd.cds.database_id = hx.meta.policy_option_id

    # Determine if it's a renewal policy
    hxd.cds.standard_fields.is_renewal.calculated = True if hx.meta.expiring_policy_option_id else False
    
    # Calculate term
    hxd.cds.term.calculated = year_diff(start_date=hxd.hx_core.inception_date, end_date=hxd.hx_core.expiry_date, for_term=True)

    # Assign to section and policy reference
    if ref_characters == 12:
        layer.section_reference = layer.non_eea_section_reference.ref if layer.has_double_section_ref else layer.single_section_reference.ref # Take Non-EEA ref by default
        hxd.cds.standard_fields.policy_reference = layer.section_reference[:8] # First 8 characters of section ref is policy ref
    
    # Validate fields for section reference
    if layer.has_double_section_ref:
        if len(layer.eea_section_reference.ref) > 0 and len(layer.non_eea_section_reference.ref) == 0:
            hx.errors.validation(f"Non-EEA Section Reference in Risk Information must also be filled in.")
        elif len(layer.eea_section_reference.ref) == 0 and len(layer.non_eea_section_reference.ref) > 0:
            hx.errors.validation(f"EEA Section Reference in Risk Information must also be filled in.")
        elif len(layer.eea_section_reference.ref) > 0 and len(layer.non_eea_section_reference.ref) > 0:
            if len(layer.eea_section_reference.ref) != 12:
                hx.errors.validation(f"EEA Section Reference in Risk Information must have 12 characters. Current input has {len(layer.eea_section_reference.ref)} characters.")
            if len(layer.non_eea_section_reference.ref) != 12:
                hx.errors.validation(f"Non-EEA Section Reference in Risk Information must have 12 characters. Current input has {len(layer.non_eea_section_reference.ref)} characters.")
        elif not layer.section_reference:
            hx.errors.validation("Section Reference in Risk Information must be filled in.")
    
    elif ref_characters > 0 and ref_characters != 12:
        hx.errors.validation(f"Section Reference in Risk Information must have 12 characters. Current input has {ref_characters} characters.")
    
    elif not layer.section_reference:
        hx.errors.validation("Section Reference in Risk Information must be filled in.")
    
    #Decide whether to show the Cargo Cyber policy reference 
    hx_01 = hxd.cds
    coverages_01  = hxd.cds.cover_selection
    hx_01.main_polref_is_shown = True
    hx_01.cargo_cyber_is_shown = False
    if coverages_01.is_cargo_cyber:
        hx_01.cargo_cyber_is_shown  = True
    
    #Assign policy reference and validations to Cargo Cyber Add On
    if hxd.cds.cover_selection.is_cargo_cyber:
        layer_cyber = layer.coverages.cargo_cyber_addon
        ref_characters_cyber = len(layer_cyber.non_eea_section_reference.ref) if layer.has_double_section_ref else len(layer_cyber.single_section_reference.ref)
        layer_cyber_section_reference = None
        # Assign to section reference view for KPI
        if ref_characters_cyber == 12:
            layer_cyber_section_reference = layer_cyber.non_eea_section_reference.ref if layer.has_double_section_ref else layer_cyber.single_section_reference.ref # Take Non-EEA ref by default
            layer_cyber.section_reference_view = layer_cyber_section_reference[:8] # First 8 characters of section ref is policy ref

        # Validate fields for section reference
        if layer.has_double_section_ref:
            if len(layer_cyber.eea_section_reference.ref) > 0 and len(layer_cyber.non_eea_section_reference.ref) == 0:
                hx.errors.validation(f"Cargo Cyber: Non-EEA Section Reference in Risk Information must also be filled in.")
            elif len(layer_cyber.eea_section_reference.ref) == 0 and len(layer_cyber.non_eea_section_reference.ref) > 0:
                hx.errors.validation(f"Cargo Cyber:EEA Section Reference in Risk Information must also be filled in.")
            elif len(layer_cyber.eea_section_reference.ref) > 0 and len(layer_cyber.non_eea_section_reference.ref) > 0:
                if len(layer_cyber.eea_section_reference.ref) != 12:
                    hx.errors.validation(f"Cargo Cyber:EEA Section Reference in Risk Information must have 12 characters. Current input has {len(layer_cyber.eea_section_reference.ref)} characters.")
                if len(layer_cyber.non_eea_section_reference.ref) != 12:
                    hx.errors.validation(f"Cargo Cyber:Non-EEA Section Reference in Risk Information must have 12 characters. Current input has {len(layer_cyber.non_eea_section_reference.ref)} characters.")
            elif not layer_cyber_section_reference:
                hx.errors.validation("Cargo Cyber:Section Reference in Risk Information must be filled in.")
        
        elif ref_characters_cyber > 0 and ref_characters_cyber != 12:
            hx.errors.validation(f"Cargo Cyber:ection Reference in Risk Information must have 12 characters. Current input has {ref_characters_cyber} characters.")
    
        elif not layer_cyber_section_reference:
            hx.errors.validation("Cargo Cyber:Section Reference in Risk Information must be filled in.")


    
    