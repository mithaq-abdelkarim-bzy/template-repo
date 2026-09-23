import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import year_diff


def rate_risk_information(hxd):
    cds = hxd.cds
    sf = cds.standard_fields
    layer = hxd.cds.layers[0]

    # Validate policy reference and other fields
    if (sf.policy_reference is not None) and (len(sf.policy_reference) != 12):
        hx.errors.validation(f"Policy Reference in Risk Information must have 12 characters. Current input has {len(sf.policy_reference)} characters.")

    finalizable_status = ["Bound", "Post Bind Complete"] 
    if layer.status in finalizable_status:
        if not sf.insured_name:
            hx.errors.validation("Insured Name in Risk Information cannot be empty.")
        if not sf.underwriter:
            hx.errors.validation("Underwriter in Risk Information cannot be empty.")
        if not sf.policy_reference:
            hx.errors.validation("Policy Reference in Risk Information cannot be empty.")
        if hxd.cds.exposure.granular.show_check_cols:
            hx.errors.validation("Please untick 'Validate Data' in Premium before setting the policy to Final.")

    # Determine BM class
    hxd.cds.standard_fields.benchmark_class = "Life " + (hxd.cds.policy_info.direct_ri or "Direct")
    layer.written_line = layer.written_line_input
    
    # Set labels
    if cds.is_group:
        layer.brokerage_label = "Brokerage"
        return

    # Only make following changes if it's Individual
    hxd.cds.standard_fields.benchmark_class = "Life Direct"
    layer.brokerage_label = "Brokerage (Direct)"
    layer.written_line = 1 # Always 100% when Individual
    




    
    