import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter


def rate_risk_information(hxd):
    # Extracts database id for the risk information tab
    hxd.cds.database_id = hx.meta.policy_option_id
    
    # Benchmark Class
    hxd.cds.standard_fields.benchmark_class = "M&A"

    # Policy Period
    hxd.cds.term = utils.year_diff(start_date=hxd.hx_core.inception_date, end_date=hxd.hx_core.expiry_date, for_term=True)

    pass