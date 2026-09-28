import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter
from algorithms.rate_constants import max_layers

def rate_rate_change(hxd):

    hxd.cds.rate_change.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id
    
    # For layers not used in the pricing summary, the rate change is hidden
    num_layers = len(hxd.cds.layers)
    for index in range(1,max_layers+1):
        setattr(hxd.cds.rate_change, f"show_layer_{index}", True) if index <= num_layers else False
    
    for layer in hxd.cds.layers:
        # Validation for adding comment if rate change has been overridden for each layer.
        for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
            rc_vbl = getattr(layer.rate_change, item)
            if rc_vbl.uw_selected.is_overridden is True and rc_vbl.comments is None:
                hx.errors.validation(f"Rate Change: {(utils.title_rc(item))} has been overridden and no comment provided")

        # Rate change calculations go here, per layer 
        # Replace with Calculation for the specific model

        #rc_vbl.model_calculated = 1
        #rc_vbl.uw_selected.calculated = rc_vbl.calculated

        #total_change = total_change * rc_vbl.model_calculated
        #total_change_uw = total_change_uw * rc_vbl.uw_selected.selected



   
    pass