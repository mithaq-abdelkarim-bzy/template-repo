import hx
import pandas as pd
import numpy as np
import math as math
import scipy
from scipy.stats import norm
from algorithms.rate_utilities import *
from algorithms.rate_constants import *
from algorithms import parameter_tables_schema as params
from operator import itemgetter

def validations(hxd):
    cds = hxd.cds
    sev = cds.rating_factors.sev

    # Validation to ensure the severity adjustment selections are not out of bounds
    sev_cov_vbl = [sev.due_diligence, sev.disclosure, sev.general_warranties, sev.tax_warranties]

    for loop_vbl, loop_str in zip(sev_cov_vbl, sev_cov_label):
        if not (sev_adj_min <= loop_vbl.adjustment <= sev_adj_max):
            hx.errors.validation(f"{loop_str} adjustment must be between {sev_adj_min * 100}% and {sev_adj_max * 100}%")
        if loop_vbl.adjustment and not loop_vbl.comment:
            hx.errors.validation(f"Comment must accompany the adjustment selection for {loop_str}")
        

    # Validation to check how many layers are set as bound
    bound_count = 0
    for layer in cds.layers:
        if layer.status in ["Bound", "Post Bind Complete", "Bound - Old Rater"]:
            bound_count += 1

            # if cds.standard_fields.policy_reference is None:
            #     hx.errors.validation(f"Policy reference must be entered when the policy is bound")
            if layer.section_reference is None:
                hx.errors.validation(f"Policy reference must be entered when the policy is bound")

            if layer.section_reference is not None and len(layer.section_reference) not in (8, 12):
                hx.errors.validation(f"Valid Policy reference must be of length 8 or 12")

    
    if bound_count == 0:
        hx.errors.validation("Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final")
    # elif bound_count > 1:
    #     hx.errors.validation("There must be only one bound policy")

    # validation to make sure brokerage is between 0 and 1 
    # for layer in cds.layers:
    #     if (layer.brokerage > 1 or layer.brokerage < 0):
    #         hx.errors.validation(f"Please ensure that Brokerage is between 0% and 100%")
    
    # validation to ensure that limit and excess % are filled out 

    #Validation to make sure transaction value is not blank
    if cds.policy_info.transaction_value in [None, 0]:
        hx.errors.validation(f"Please fill in Transaction Value")
    
    for index, layer in enumerate(cds.layers, start=1):
        if layer.excess_pct.selected is None:
            hx.errors.validation(f"Please fill out Excess or Excess % for option {index}")
        if layer.limit_pct is None:
            hx.errors.validation(f"Please fill out Limit")

        # Validation to ensure that excess and excess percentage are valid
        if ((layer.excess.selected is not None and layer.excess_pct.selected is not None and cds.policy_info.transaction_value is not None) and (layer.excess.selected != (layer.excess_pct.selected * cds.policy_info.transaction_value))):
            hx.errors.validation(f"Please reset the override for Excess or Excess % for option {index}")
    
    if (cds.rating_factors.freq.buyer.jurisdiction is None or cds.rating_factors.freq.target.jurisdiction is None):
         hx.errors.validation(f"Please fill out Jurisdiction")

    if (cds.rating_factors.freq.buyer.industry is None or cds.rating_factors.freq.target.industry is None):
         hx.errors.validation(f"Please fill out Industry")

    # validation for blended weights to be 100%
    blend_options = ["option_1", "option_2", "option_3"]
    option_names = [getattr(getattr(cds.blend_option, item), "option_name") for item in blend_options]
    weights = [getattr(getattr(cds.blend_option, item), "weight") for item in blend_options]

    if (any(option_names) & (sum(filter(None, weights)) != 1)):
        hx.errors.validation("Option weights in blend quote must sum to 100%.")

    pass

 

 




