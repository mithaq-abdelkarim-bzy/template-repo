# v0.5.0
import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
from operator import itemgetter
from algorithms.model_profiler.profiling_hxd_functions import time_me

from algorithms.rate_constants import max_layers, experience_rating_max_years, reinstatement_max_number

@time_me
def rate_advanced_features(hxd):
    """Set section of page Advanced features"""
    ##############################
    ## initialise variables
    ##############################

    cds = hxd.cds
    cds_layers = cds.layers


    ##############################
    ## Assign variables: expected_losses, expected_losses_after_loss_sensitive_features, upfront_premium_gross_100_gross_100_gross_100
    ##############################

    for layer_index, layer in enumerate(cds_layers):
        layer.expected_loss = expected_loss = (layer.pricing_selection.final_selection.pure_premium or 0)
        layer.expected_losses_after_loss_sensitive_features = expected_loss - (layer.expected_aad or 0) - (layer.loss_corridor_loss_cost or 0)
        
        # Count the number of non-zero and non-None reinstatement percentages
        layer.number_of_rips = sum(
            1 for index in range(1, reinstatement_max_number + 1)
            if getattr(layer, f"reinstatement_pct_{index}", 0) not in { None}
        )

        upfront_premium_gross_100 = layer.upfront_premium_gross_100 or 0

        # Set brokerage including swing
        layer.brokerage_inc_swing = 0
        layer.brokerage_inc_swing = (
            layer.swing_rates.swing_brokerage
            if layer.swing_rates.use_swing_brokerage
            else layer.brokerage
        )

        brokerage_inc_swing = layer.brokerage_inc_swing or 0
        ceding_commission = layer.ceding_commission or 0

        if layer.bkg_gross_or_net == "Gross":
            netting_down_factor = (1 - brokerage_inc_swing - ceding_commission )
        else:
            netting_down_factor =  (1 - brokerage_inc_swing) * (1 - ceding_commission )

        reinstatement_factor = layer.expected_reinstatement_factor or 0
        ncb_percentage = layer.expected_ncb_pct or 0
        profit_commission = layer.profit_commission or 0
        swing_premium = layer.swing_premium or 0
        
        layer.quoted_premium_net_100 = 0

        if upfront_premium_gross_100 is not None:
            net_premium_after_commissions = upfront_premium_gross_100 * netting_down_factor
            reinstatement_and_ncb_adjustment = upfront_premium_gross_100 * (reinstatement_factor - ncb_percentage)
            additional_adjustments = swing_premium - profit_commission

            layer.expected_premium_paid_net_100 = expected_premium_paid_net_100 =  (
                net_premium_after_commissions +
                reinstatement_and_ncb_adjustment +
                additional_adjustments
            )

            layer.quoted_premium_net_100 = expected_premium_paid_net_100
            layer.expected_premium_paid_gross_100 = expected_premium_paid_gross_100 = utils.ratio(expected_premium_paid_net_100,netting_down_factor)
            layer.upfront_premium_net_100 = upfront_premium_gross_100 * netting_down_factor
            layer.quoted_premium_100 = expected_premium_paid_gross_100
    return