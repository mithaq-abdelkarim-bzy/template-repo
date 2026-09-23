import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter


def rate_risk_information(hxd):
    # Extracts database id for the risk information tab
    hxd.cds.database_id = hx.meta.policy_option_id

    if hxd.cds.standard_fields.insured_name is None:
        hx.errors.validation("Please Enter Insured Name")
    # set the value of is_real_renewal: renewal with no Bound layer are not real renewals
    is_bound=False
    for index , layer in enumerate(hxd.cds.layers):
        if layer.status == 'Bound' or layer.status == 'Post Bind Complete' or layer.status == 'Quoted':
            is_bound=True
    
    if hxd.cds.standard_fields.is_renewal == True:
        if is_bound == False or is_bound==None:
            hxd.cds.is_real_renewal = False
        else:
            hxd.cds.is_real_renewal = True
    else:
        hxd.cds.is_real_renewal = False

    if hxd.cds.exposure.aggregate.revenue is None or hxd.cds.exposure.aggregate.revenue == 0:
        hxd.cds.exposure.aggregate.revenue_empty = True
        hxd.cds.exposure.aggregate.revenue_filled = False
        hxd.cds.exposure.aggregate.revenue_info = "Please ensure the revenue field is completed before proceeding"
    else:
        hxd.cds.exposure.aggregate.revenue_filled = True
        hxd.cds.exposure.aggregate.revenue_empty = False

    pass