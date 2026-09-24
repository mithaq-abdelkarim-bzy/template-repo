# v0.5.0
import hx
import pandas as pd
import numpy as np
import math as math
import json
from algorithms.rate_utilities import title_rc, ratio, usd, to_ccy, look_up
from operator import itemgetter

from algorithms.rate_constants import max_layers
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import COVERAGES_LIST

from algorithms import parameter_tables_schema as params

def assign_rc_nodes(rc_source_data, rc_data):
    """
    This function can be used a layer-level or a coverage-level.

    It assigns values to the rate change nodes:
     - the renewing, expiring, expiring revalued rate change nodes
     - 100 premium, Beazley premium, policy term, and annualised. 
    It also populates table nodes with policy details including limit, deductible, excess, and brokerage.

    Args:
    - rc_source_data: the path of the source data
    - rc_data: the path where the rate change data is stored

    Requirements:
    - annualisese premium and insurer's share premium MUST be calculated in the rating beforehand
    """
    fx_rates_df = params.fx_rates.df() # Using fx from library
    # fx_rates_df = hx.params.table_currency # Using fx from params

    # Assign rate change renewal data
    rc_data.premium.line_100pct.policy_term.renewal = (rc_source_data.quoted_premium_100 or 0) 
    rc_data.premium.line_100pct.annualised.renewal = (rc_source_data.quoted_premium_annual_100 or 0)
    rc_data.premium.beazley_line.annualised.renewal = (rc_source_data.quoted_premium_annual or 0)
    rc_data.premium.beazley_line.policy_term.renewal = (rc_source_data.quoted_premium or 0)
    if not RARC_INSURED_ASSET_USE:
        # Node only aplicable to premium calculated at a layer or coverage level
        rc_data.limit.renewal = rc_source_data.limit
        rc_data.deductible.renewal = rc_source_data.deductible
        rc_data.excess.renewal = rc_source_data.excess

    rc_data.brokerage.renewal = rc_source_data.brokerage
    rc_data.currency.renewal = rc_source_data.currency
    
    # Assign rate change expiring data
    rc_data.premium.line_100pct.policy_term.expiring = rc_data.expiring_policy_info.expiring_quoted_premium_100 or 0
    rc_data.premium.line_100pct.annualised.expiring = rc_data.expiring_policy_info.expiring_quoted_premium_annual_100 or 0 
    rc_data.premium.beazley_line.annualised.expiring = rc_data.expiring_policy_info.expiring_quoted_premium_annual or 0 
    rc_data.premium.beazley_line.policy_term.expiring = rc_data.expiring_policy_info.expiring_quoted_premium or 0 

    if not RARC_INSURED_ASSET_USE:
    # Node only aplicable to premium calculated at a layer or coverage level
        rc_data.limit.expiring = (rc_data.expiring_policy_info.expiring_limit or 0)
        rc_data.deductible.expiring = (rc_data.expiring_policy_info.expiring_deductible or 0)
        rc_data.excess.expiring = (rc_data.expiring_policy_info.expiring_excess or 0)

    rc_data.brokerage.expiring = (rc_data.expiring_policy_info.expiring_brokerage or 0)
    rc_data.currency.expiring = (rc_data.expiring_policy_info.expiring_currency or "USD")

    # get expiring and renewing fx
    expiring_fx_to_usd = look_up(lookup_value=rc_data.currency.expiring, lookup_col="ccy", return_col="fx_rate", df=fx_rates_df, if_not_found=1)
    renewing_fx_to_usd = look_up(lookup_value=rc_data.currency.renewal, lookup_col="ccy", return_col="fx_rate", df=fx_rates_df, if_not_found=1)
    
    # assign value to show_expiring   
    rc_data.show_expiring_revalued = (rc_data.currency.expiring != rc_data.currency.renewal)
    # calculate revaluing factor
    revaluing_factor = ratio(renewing_fx_to_usd,expiring_fx_to_usd) if rc_data.show_expiring_revalued else 1
     
    rc_data.premium.line_100pct.annualised.expiring_revalued = rc_data.premium.line_100pct.annualised.expiring * revaluing_factor
    rc_data.premium.beazley_line.annualised.expiring_revalued = rc_data.premium.beazley_line.annualised.expiring * revaluing_factor
    rc_data.premium.line_100pct.policy_term.expiring_revalued = rc_data.premium.line_100pct.policy_term.expiring * revaluing_factor
    rc_data.premium.beazley_line.policy_term.expiring_revalued = rc_data.premium.beazley_line.policy_term.expiring * revaluing_factor

    if not RARC_INSURED_ASSET_USE:
    # Node only aplicable to premium calculated at a layer or coverage level
        rc_data.limit.expiring_revalued = rc_data.limit.expiring * revaluing_factor
        rc_data.deductible.expiring_revalued = rc_data.deductible.expiring * revaluing_factor
        rc_data.excess.expiring_revalued = rc_data.excess.expiring * revaluing_factor

    rc_data.brokerage.expiring_revalued = rc_data.brokerage.expiring # same as expiring
    rc_data.currency.expiring_revalued = rc_data.currency.renewal # same as renewing

    # Calculate rebased premium for each bucket
    rebased_premium_model = rebased_premium_uw = rc_data.premium.line_100pct.annualised.expiring or 0
    renewal_premium = rc_data.premium.line_100pct.annualised.renewal
    return rebased_premium_model, rebased_premium_uw, renewal_premium
