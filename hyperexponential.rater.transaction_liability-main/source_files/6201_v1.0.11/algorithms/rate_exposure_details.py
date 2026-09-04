import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import *
from algorithms.rate_constants import *
from operator import itemgetter



def rate_exposure_details(hxd):
    #Set paths
    freq = hxd.cds.rating_factors.freq
    freq_target = freq.target
    freq_buyer = freq.buyer
    sev = hxd.cds.rating_factors.sev
    policy_info = hxd.cds.policy_info
    params = hx.params

    # Load parameter tables
    param_country_factor = df_to_dict(params.table_country_factor, "location", "factor")
    param_industry = df_to_dict(params.table_industry, "industry list", ["target hazard class", "target relativity", "buyer hazard class", "buyer relativity"])
    param_sev_mod = df_to_dict(params.table_modifiers, "coverage", ["min", "max", "default weights"])

    
    policy_info.total_limit_percentage = (policy_info.total_limit / policy_info.transaction_value) if policy_info.transaction_value not in [None, 0] else 0 

    # FREQ selections
    freq.default_score = param_country_factor[freq_target.jurisdiction] if freq_target.jurisdiction else 0

    industry_adjustment = max(param_industry[freq_target.industry]['target relativity'], param_industry[freq_buyer.industry]['buyer relativity']) if (freq_target.industry and freq_buyer.industry) else 1

    freq.freq_adjusted =  freq.default_score * (1 + freq.freq_adjustment) * industry_adjustment
    freq.freq_adjusted_pre_uw = freq.default_score * industry_adjustment

    #TODO: Check if IHS Contract Enforcement links anywhere

    # Severity selections
    sev.modified_score = freq.freq_adjusted * (
        sum(
            [param_sev_mod[sev_cov_dict[cov]['label']]['default weights'] *
            (1 + getattr(getattr(sev, cov), "adjustment")) *
            ((1 + getattr(getattr(sev, cov), "term_modifier")) if sev_cov_dict[cov]['incl_term_mod'] else 1)
            for cov in sev_cov]
    ))

    for layer in hxd.cds.layers: 
        layer.brokerage = hxd.cds.policy_info.brokerage


    sev.modified_score_pre_uw = sev.modified_score / freq.freq_adjusted * freq.freq_adjusted_pre_uw if freq.freq_adjusted else None

    pass