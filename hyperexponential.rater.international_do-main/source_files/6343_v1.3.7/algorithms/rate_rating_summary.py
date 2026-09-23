import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import ratio
from algorithms import parameter_tables_schema as params
import algorithms.rate_utilities as utils
from operator import itemgetter

def rate_rating_summary(hxd):
    
    # define cds
    cds = hxd.cds
    
    # define labels
    cds.labels.uw_side_ab_discount_override_info = "Notes must be provided if overridden"
    cds.labels.beazley_market_share_info = "Beazley market share must be populated for each layer being priced"
    cds.labels.section_reference_info = "Any layers that have a Policy Reference value are considered bound and are sent through to downstream systems (BI). Do not use this field to add notes or put TBA.  If the Policy Reference is not known leave it blank until it is known."
    cds.labels.premium_and_costs_info = "1. If the Beazley Market Share is 0% for any layer, then all figures for that layer in the table below will be expressed in 100% terms. If Beazley Market Share is entered, then technical and benchmark premium figures are expressed as Beazley Share. \n 2. The Cat LR will vary by policy. Overall on a portfolio level, the Cat LR is 14%. \n 3. All losses shown are 100% share."

    benchmark_premium_pre_uw_adj = [0]*len(hxd.cds.large_cap.layers)

    # Use a for loop if your model prices multiple layers 
    for i, layer in enumerate(hxd.cds.large_cap.layers):

        layer.quoted_premium_annual_100 = ((layer.quoted_premium_100 or 0) / hxd.cds.rating_factors.risk_information.policy_term) or 0

        # Assign mmp totals if flag is true and skip the rest
        mmp = cds.mmp

        
        # Assigning calculated fields on the rating summary tab. Expected loss costs are calculted in rate_pricing.py
        # Benchmark Premium
        if layer.written_line == 0 or layer.written_line is None:
            layer.benchmark_premium = utils.ratio(layer.expected_loss_cost/0.7, (1 - layer.brokerage))
            layer.benchmark_premium_100 = (layer.benchmark_premium or 0)
            benchmark_premium_pre_uw_adj[i] = utils.ratio(layer.expected_loss_cost_pre_uw_adj/0.7, (1 - layer.brokerage))
        else:
            layer.benchmark_premium = utils.ratio(layer.expected_loss_cost/0.7, (1 - layer.brokerage)) * layer.written_line
            layer.benchmark_premium_100 = ((layer.benchmark_premium or 0) / layer.written_line) or 0
            benchmark_premium_pre_uw_adj[i] = utils.ratio(layer.expected_loss_cost_pre_uw_adj/0.7, (1 - layer.brokerage)) * layer.written_line

        layer.benchmark_premium_annual_100 = ((layer.benchmark_premium_100 or 0) / hxd.cds.rating_factors.risk_information.policy_term) or 0

        # TPI%
        if layer.quoted_premium_100 is not None:
            bound_premium = layer.quoted_premium_100 * (layer.written_line if layer.written_line and layer.written_line != 0 else 1)
            layer.tpi = utils.ratio(bound_premium, layer.technical_premium)
            layer.tpi_pre_uw_adj = utils.ratio(bound_premium, layer.technical_premium_pre_uw_adj)

        # BPI%
        if layer.quoted_premium_100 is not None:
            bound_premium = layer.quoted_premium_100 * (layer.written_line if layer.written_line and layer.written_line != 0 else 1)
            layer.bpi = utils.ratio(bound_premium, layer.benchmark_premium)
            layer.bpi_pre_uw_adj = utils.ratio(bound_premium, benchmark_premium_pre_uw_adj[i])


        # Achieved Loss Ratio
        if layer.quoted_premium_100 is not None:
            layer.pflr = utils.ratio(layer.expected_loss_cost, (layer.quoted_premium_100 * (1 - layer.brokerage)), 0)
            layer.pflr_pre_uw_adj = utils.ratio(layer.expected_loss_cost_pre_uw_adj, (layer.quoted_premium_100 * (1 - layer.brokerage)), 0)



    # Validation for Inputs
    for layer in hxd.cds.large_cap.layers:
        for attr in ("limit", "excess", "deductible", "quoted_premium_100", "brokerage", "written_line"):
            value = getattr(layer, attr, None)
            if value is not None and value < 0:
                hx.errors.fatal("Rating Summary: Entered value must be greater than zero.")

    # Validation to check how many layers are set as bound
    status_count = 0
    if cds.risk_information.mmp_flag is False:
        for layer in hxd.cds.large_cap.layers:
            if layer.status is not None:
                status_count += 1
    elif mmp.total.status is not None:
        status_count += 1


        
    if status_count == 0:
        hx.errors.validation("Rating Summary: Status must be set to mark a policy as final")
    # elif status_count > 1:
    #     hx.errors.validation("There must be only one bound policy")

    for layer in hxd.cds.large_cap.layers:
        if layer.status == "Bound" and layer.section_reference is None:
            hx.errors.validation("Rating Summary: Bound layer must have a Section Reference")

        if layer.side_selection == "AB" and layer.uw_side_ab_discount_override is not None and layer.notes is None:
            hx.errors.validation("Rating Summary: Notes must be provided for Side AB discount override")

        if layer.side_selection is not None and layer.written_line is None:
            hx.errors.validation("Rating Summary: Written Line must be provided for each layer being priced")

        if hxd.cds.risk_information.cips_policy == "No" and layer.section_reference is not None and len(layer.section_reference) != 12 and layer.limit is not None:
            hx.errors.validation("Rating Summary: Check Section Reference, must be 12 Characters")

        # Cips validation    
        elif hxd.cds.risk_information.cips_policy == "Yes" and layer.section_reference is not None and len(layer.section_reference) != 8 and layer.limit is not None:
            hx.errors.validation("Rating Summary: Check Section Reference, must be 8 Characters as CIPS Policy")


    cds.prem_build_up.options_list = calc_length_layers(hxd) 


    


# Setting length of layer selection for graphs
def calc_length_layers(hxd):

    length = list(range(1, len(hxd.cds.large_cap.layers) + 1))

    length_array = pd.DataFrame({"option": length}).to_dict("records")

    return length_array


