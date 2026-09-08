import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, write_pd_to_hxd_no_overrides
from operator import itemgetter

def rate_exp_det(hxd):
    cds = hxd.cds
    hxd.cds.exposure_management_api.inputs.binder_name = cds.standard_fields.insured_name
    hxd.cds.exposure_management_api.inputs.binder_reference = cds.standard_fields.facility_reference

pass
    