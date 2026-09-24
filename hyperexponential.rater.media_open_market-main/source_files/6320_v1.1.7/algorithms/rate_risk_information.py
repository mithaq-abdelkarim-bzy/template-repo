import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import policy_term
from operator import itemgetter


def rate_risk_information(hxd):
    cds = hxd.cds

    # Validation: Expiry date must be after Inception date
    if not hxd.hx_core.inception_date < hxd.hx_core.expiry_date:
        hx.errors.validation("Expiry date must be after Inception date. [Risk Information]")

    # Extracts database id for the risk information tab
    cds.policy_option_id = hx.meta.policy_option_id
    cds.rating_factors.policy_term = policy_term(hxd.hx_core.inception_date, hxd.hx_core.expiry_date)

    # Validation: Policy period must be <= 18 months (except for multi-year coverages)
    multiyear = (cds.coverage_name == "Individual Film") or (cds.coverage_name == "Individual TV")
    if not multiyear and (hxd.cds.rating_factors.policy_term > 1.5):
        hx.errors.validation("Policy period greater than 18 months is not permitted.")

    pass