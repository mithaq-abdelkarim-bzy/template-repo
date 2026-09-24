# v0.5.0
import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import policy_term
from operator import itemgetter
from algorithms.model_profiler.profiling_hxd_functions import time_me

@time_me
def rate_risk_information(hxd):
    
    ##############################
    ## Assign value to cds.meta and cds.rating_factors
    ##############################
    hxd.cds.metadata.policy_option_id = hx.meta.policy_option_id
    hxd.cds.rating_factors.policy_term = policy_term(hxd.hx_core.inception_date, hxd.hx_core.expiry_date)
    hxd.cds.metadata.model_version_id = hx.meta.model_version_id
    ##############################
    ## upfront premium assignment
    ##############################
    layers = hxd.cds.layers
    for layer in layers:
        if layer.epi_100 is not None and layer.rate is not None:
            layer.upfront_premium_gross_100 = layer.epi_100 * layer.rate
        else:
            layer.upfront_premium_gross_100 = None
        
        layer.loss_cap_used = True if layer.cap_gross_pct is not None else False
        layer.currency = hxd.cds.currencies.source_currency

        layer.line_size = 0
        layer.line_size = (layer.written_line * layer.limit) if layer.written_line and layer.limit else 0

    ##############################
    # Steer COB reference assignment
    ##############################
    selected_cob = hxd.cds.technical_price_assumptions.select_class
    cob_df = hx.params.table_cob_code_assumptions

    # Search for the selected class in the DataFrame
    matching_rows = cob_df[cob_df["Class of Business"] == selected_cob]

    # Assign the COB reference if a match is found
    if not matching_rows.empty:
        # hxd.cds.steer.risk_information.cob_reference = matching_rows["Class of Business Code"].values[0]
        hxd.cds.technical_price_assumptions.cob_reference = matching_rows["Class of Business Code"].values[0]
    
    else:
        # Log a warning or raise an exception if no match is found
        print(f"Warning: No matching 'Class of Business Code' found for '{selected_cob}'.")



