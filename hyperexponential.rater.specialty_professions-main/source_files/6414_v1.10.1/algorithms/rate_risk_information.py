import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter
from algorithms.rate_constants import bp_class

def rate_risk_information(hxd):
    # Extracts database id for the risk information tab
    hxd.cds.database_id = hx.meta.policy_option_id

    # Currency label
    hxd.cds.currency_label = f"Amounts in {hxd.cds.ccy}"

    # Benchmark class
    hxd.cds.standard_fields.benchmark_class = bp_class    

    # State modification factor ####################################################################
    location = hxd.cds.rating_factors.location
    param_state = hx.params.tbl_state
    total_state_factor_selected = 0
    total_percentage = 0

    for index, state in enumerate(location.states):
        param_state_lookup = param_state[param_state['State'] == state.state]
        
        # Lookup risk group
        state.risk_group = param_state_lookup['Risk Group'].iloc[0]

        # Parameter table 
        # Lookup general state factor 
        state_factor = param_state_lookup['Selected Factor'].iloc[0]

        # Look up state factor adjustment - additional loading based on claims heat map
        state_factor_chm_adj = param_state_lookup['Claims Heat Map Factor'].iloc[0]    

        # Look up state factor adjustment - additional loading for residential, depending on state
        state_factor_resi_adj = param_state_lookup['Residential Factor'].iloc[0]

        # State factor adj (resi) only applies for residential project
        if (hxd.cds.rating_factors.resi.resi_proj == True): 
            state_factor_resi_adj2 = max(state_factor_resi_adj/state_factor_chm_adj,1)
        else:
            state_factor_resi_adj2 = 1
    
        # State factor adjustment to apply
        state.state_factor_selected = state_factor * state_factor_chm_adj * state_factor_resi_adj2
        
        total_percentage += state.percentage if state.percentage else 0
        total_state_factor_selected += state.state_factor_selected * state.percentage if (state.state_factor_selected and state.percentage) else 0

    location.state = "Total"
    location.percentage = total_percentage
    total_state_factor_selected = total_state_factor_selected / total_percentage if total_percentage != 0 else 1
    location.state_factor_selected = total_state_factor_selected 





