# v0.5.0
import hx
import pandas as pd
import numpy as np

def rate_validations(hxd):


    # Pricing Page
    # Retention Table
    rs_neg_check = False
    for item in hxd.cds.retention_split:
        if (item.eec or 0) < 0: rs_neg_check = True
        if (item.aggregate or 0) < 0: rs_neg_check = True
        if (item.retention_underlying or 0) < 0: rs_neg_check = True
        if (item.retention_residual or 0) < 0: rs_neg_check = True

    if rs_neg_check:
        hx.errors.validation("There are negative values in the Retention table")

    # Policy Structures
    ps_neg_check = False
    node_list = ""
    for item in hxd.cds.layers:
        for node in ["limit_eec", "limit_agg", "excess_eec", "excess_agg", "rtc", "rtc_agg", "brokerage" ]:
            if (getattr(item, node) or 0) < 0: 
                ps_neg_check = True
                node_list += f"{node}, "

    if ps_neg_check:
        hx.errors.validation(f"There are negative values in columns in the Policy Structures Table that are not allowed negative values: {node_list}")

    # Policy Structures
    ps_neg_check = False
    node_list = ""
    for item in hxd.cds.layers_addl:
        for node in ["limit_eec", "limit_agg", "excess_eec", "excess_agg", "rtc", "rtc_agg", "brokerage"]:
            if (getattr(item, node) or 0) < 0: 
                ps_neg_check = True
                node_list += f"{node}, "

    if ps_neg_check:
        hx.errors.validation(f"There are negative values in columns in the Additinoal Policy Structures Table that are not allowed negative values: {node_list}")

    # RISK INFORMATION
    # Insured name must be completed, this is needed to ensure landing page works correctly
    if not hxd.cds.standard_fields.insured_name:
        hx.errors.validation("Insured name field must be completed.")
    
    if not hxd.cds.standard_fields.underwriter:
        hx.errors.validation("Underwriter field must be completed")
    
    # if not hxd.cds.profession:
    #     hx.errors.validation("Profession field must be completed")

    if not hxd.cds.currencies.source_currency:
        hx.errors.validation("Source Currency field must be completed")       


    # Claims
    bool_claims_error = False
    if not hxd.cds.experience_rating.claims_asatdate:
        for item in hxd.cds.experience_rating.claims:
            if item.claim_name:
                bool_claims_error = True
        
        if bool_claims_error:
            hx.errors.validation("Claims As At Date must be completed")
    # TERRITORY

   # Validation to check how many layers are set as bound, also updates premium label for bound policies
    bound_count = 0
    include_count = 0
    layers_all = [hxd.cds.layers, hxd.cds.layers_addl]

    for layer_set in layers_all:
        for layer in layer_set:
            if layer.status in ["Bound", "Post Bind Complete"]:
                bound_count += 1
                layer.premium_label = "Gross Bound Premium"
            else:
                layer.premium_label = "Gross Quoted Premium"

            if layer.include:
                include_count +=1

    if include_count == 0:
        hx.errors.validation("At least one layer must be included")
    
    # if bound_count == 0:
    #     hx.errors.validation("Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final")
    # elif bound_count > 1:
    #     hx.errors.validation("There must be only one bound policy")

    # agg_ret is unique
    regions = [item.region for item in hxd.cds.retention_split if item.region is not None]
    if len(regions) != len(set(regions)):
        hx.errors.validation("There are duplicate regions in the Retention table")


    