# v0.5.0
import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import policy_term
from operator import itemgetter


def rate_risk_information(hxd):
        
    # Extracts database id for the risk information tab
    hxd.cds.policy_option_id = hx.meta.policy_option_id
    hxd.cds.rating_factors.policy_term = policy_term(hxd.hx_core.inception_date, hxd.hx_core.expiry_date)
    
    hxd.cds.profession_lawyers_bool = False
    hxd.cds.profession_lawyers_bool_not = False     # profession could be None
    hxd.cds.profession_AE_bool = False
    hxd.cds.profession_contractors_bool = False

    if hxd.cds.profession == "Lawyers":
        hxd.cds.profession_lawyers_bool = True
        hxd.cds.profession_lawyers_bool_not = False
    elif hxd.cds.profession == "Architects and Engineers":
        hxd.cds.profession_AE_bool = True
        hxd.cds.profession_lawyers_bool_not = True
    elif hxd.cds.profession == "Contractors":
        hxd.cds.profession_contractors_bool = True
        hxd.cds.profession_lawyers_bool_not = True