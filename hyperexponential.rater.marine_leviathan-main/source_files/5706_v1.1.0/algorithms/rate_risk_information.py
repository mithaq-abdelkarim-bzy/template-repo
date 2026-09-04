import hx
import pandas as pd
import numpy as np
import math as math
import dateutil as dateutil
from algorithms.rate_utilities import policy_term
from operator import itemgetter
from datetime import datetime



def rate_risk_information(hxd):
        
    # Extracts database id for the risk information tab
    hxd.cds.policy_option_id = hx.meta.policy_option_id
    hxd.cds.rating_factors.policy_term = policy_term(hxd.hx_core.inception_date, hxd.hx_core.expiry_date)

    hxd.cds.yoa = hxd.hx_core.inception_date.year

    
    hxd.cds.policy_term = round((((hxd.hx_core.expiry_date    -    hxd.hx_core.inception_date).days +1) / 365.25),2)

    pass