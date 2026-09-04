import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import year_diff, one_layer, policy_term

 
def rate_risk_information(hxd):
    cds = hxd.cds
    sf = cds.standard_fields
    layer, cvg = one_layer(hxd)

    # Extracts database id for the risk information tab
    hxd.cds.policy_option_id = hx.meta.policy_option_id

    # Set rating methodology
    sf.is_case_priced = hxd.cds.standard_fields.rating_methodology == "Case Priced"
    sf.is_rater_priced = hxd.cds.standard_fields.rating_methodology == "Rater"

    # Calculate term
    hxd.cds.policy_info.term = policy_term(hxd.hx_core.inception_date, hxd.hx_core.expiry_date)

    # Determine BM class
    hxd.cds.standard_fields.benchmark_class = "Terrorism" # NOTE: not actually used when calculating TP

    cds.standard_fields.policy_reference    = '' if layer.section_reference is None else layer.section_reference[:8]

    # [TriFocusName] in('Stand Alone Terrorism','BUSA Terrorism','BESI Terrorism') but this is the main one
    cds.standard_fields.trifocus            = "Stand Alone Terrorism"
    
    layer.currency = cds.currencies.source_currency  

    hxd.hx_core.premium_currency = layer.currency

