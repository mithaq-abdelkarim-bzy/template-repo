import hx
import pandas as pd
import numpy as np
import algorithms.utils_global_lists as lst


def validations(hxd):
    cds = hxd.cds
    layer = cds.layers[0]
    rc = layer.rate_change
    std = hxd.cds.standard_fields
    exp_agg = cds.exposure.aggregate

    # Add validation for insured name
    if not std.insured_name:
        hx.errors.validation("Insured name is missing in Risk Information")

    # Add validation for Deal Status field

    if layer.status is None:
        hx.errors.validation("Select Deal Status in Risk Information")

    if layer.status == "Bound" and not std.policy_reference:
        hx.errors.validation("Policy reference number is missing in Risk Information")

    if not std.insured_state_or_province:
        hx.errors.validation("State is missing in Exposure Details")
        
    # # Uncomment when switching to new benchmark calcs
    # if not exp_agg.revenue:
    #     hx.errors.validation("Revenue is missing in Exposure Details")
        
    # if not exp_agg.assets:
    #     hx.errors.validation("Assets is missing in Exposure Details")
        
    # if not exp_agg.employees:
    #     hx.errors.validation("Number of employees is missing in Exposure Details")
        
    # if not exp_agg.locations:
    #     hx.errors.validation("Number of locations is missing in Exposure Details")

    # Validate that a selection has been made for the Beazley layer
    if cds.beazley_layer is None:
        hx.errors.validation(f"Beazley's layer is missing in Exposure Details")
    if cds.beazley_share == 0:
        hx.errors.validation(f"Beazley's share is missing in Exposure Details")

    # Validations for min and max coverage

    lst_modifier_vbl = [cds.classification_peculiarities, cds.management, cds.personnel, cds.location, cds.response_to_losses, cds.endorsements, cds.expense_modification]
    lst_modifier_str = ["Classification Peculiarities", "Management", "Personnel", "Location", "Response to Losses","Endorsements", "Expense Modification"]

    for loop_vbl, loop_str in zip(lst_modifier_vbl, lst_modifier_str):
        if loop_vbl.selected != 0 and std.insured_state_or_province:
            if loop_vbl.selected < loop_vbl.minimum_state:
                hx.errors.validation(f"{loop_str} max credit exceeded")
            if loop_vbl.selected > loop_vbl.maximum_state:
                hx.errors.validation(f"{loop_str} max debit exceeded")
            if loop_vbl.comment=="":
                hx.errors.validation(f"{loop_str} modifier note is missing")

    if layer.unity_premium:
        if layer.unity_premium<cds.eligibility_min_before or layer.unity_premium*cds.mod_factor<cds.eligibility_min_after:
            hx.errors.validation(f"Individual risk rating not allowed for this risk as premiums do not meet minimum requirements")      
    
    # Add validation for LRE eligibility
    if cds.standard_fields.insured_state_or_province not in lst.lre_states and cds.standard_fields.is_admitted_or_surplus == "Admitted - LRE":
        hx.errors.validation(f"LRE rating not allowed in this insured state")

    # Add validation for Rate Change
    if cds.standard_fields.is_renewal:
        if not rc.expiring_premium:
            hx.errors.validation(f"Expiring premium is missing in Rate Change")

        ## Uncomment when switching to new benchmark calcs
        # if not rc.expiring_revenue:
        #     hx.errors.validation(f"Expiring revenue is missing in Rate Change") 
        # if not rc.expiring_assets:
        #     hx.errors.validation(f"Expiring assets is missing in Rate Change")
        # if not rc.expiring_employees:
        #     hx.errors.validation(f"Expiring employees is missing in Rate Change") 
        # if not rc.expiring_locations:
        #     hx.errors.validation(f"Expiring locations is missing in Rate Change") 
        # if not rc.expiring_excess:
        #     hx.errors.validation(f"Expiring attachment point is missing in Rate Change") 

        if not rc.expiring_limit:
            hx.errors.validation(f"Expiring limit is missing in Rate Change") 

        


    

