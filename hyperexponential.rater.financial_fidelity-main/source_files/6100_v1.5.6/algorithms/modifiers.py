import hx
import pandas as pd
import numpy as np
import algorithms.utils_global_lists as lst

# ~~~~~~~~~~~~~~~~~~~ MODIFIERS ~~~~~~~~~~~~~~~~~~~

def modifiers(hxd):
    layer = hxd.cds.layers[0]
    exp_agg = hxd.cds.exposure.aggregate
    cov = layer.coverages
    param_mod_limits = hx.params.modifier_limits
    param_state = hx.params.StateLookup
    std_fields = hxd.cds.standard_fields
    
    lst_modifier_vbl = [layer.audit_procedures, layer.internal_controls, layer.management_and_personnel, layer.classification_peculiarities]
    lst_modifier_str = ["Audit Procedures", "Internal Controls", "Management & Personnel", "Classification Peculiarities"]

    #The minimum and maxiumum modifiers are stored as a parameter table, loop through and set each node in the data schema

    for loop_vbl, loop_str in zip(lst_modifier_vbl, lst_modifier_str):
        loop_vbl.minimum = param_mod_limits[param_mod_limits["modifier"] == loop_str]["minimum"].iloc[0]
        loop_vbl.maximum = param_mod_limits[param_mod_limits["modifier"] == loop_str]["maximum"].iloc[0]
    
    if std_fields.insured_state_or_province:
    # Some states don't allow modifiers or have different total min / max. So the total modifier min/max is looked up from a different prameter table
        layer.total_modifiers.minimum = param_state[param_state["State"] == std_fields.insured_state_or_province]["Schedule Mod Minimum"].iloc[0]
        layer.total_modifiers.maximum = param_state[param_state["State"] == std_fields.insured_state_or_province]["Schedule Mod Maximum"].iloc[0]

        # Check the selected state against the parameter table to check if schedule rating (modifiers) are allowed 
        # This also sets a 'total_label' which is used in the rating summary sheet
        if param_state[param_state["State"] == std_fields.insured_state_or_province]["Allows Schedule Rating"].iloc[0] == "Yes":
            layer.modifier_label = f"{std_fields.insured_state_or_province} allows schedule rating"
            layer.modifier_flag = True
            layer.total_label = "Total Model Premium (Pre Schedule Rating)"
        else:
            layer.modifier_label = f"{std_fields.insured_state_or_province} does not allow schedule rating"
            layer.modifier_flag = False
            layer.total_label = "Total Model Premium"
    
    # Sum selected modifiers if modifiers are allowed, also sum prior for rate change
    layer.total_modifiers.uw_selected = sum(item.uw_selected for item in lst_modifier_vbl) if layer.modifier_flag else 0
    layer.total_modifiers.prior_modifier = sum(item.prior_modifier for item in lst_modifier_vbl) if layer.modifier_flag else 0
    
    # Append totals onto list for validation below 
    lst_modifier_vbl.append(layer.total_modifiers)
    lst_modifier_str.append("Total")

    # Loop through validations to check modifier thresholds not exceeded (only if modifiers allowed)
    if layer.modifier_flag is True:
        for loop_vbl, loop_str in zip(lst_modifier_vbl, lst_modifier_str):
            if (loop_vbl.uw_selected > loop_vbl.maximum) or (loop_vbl.uw_selected < loop_vbl.minimum):
                hx.errors.validation(f"{loop_str} modifier threshold exceeded")
            if loop_str!="Total" and loop_vbl.uw_selected !=0 and loop_vbl.comment=="":
                hx.errors.validation(f"{loop_str} modifier note is missing")
    

    # Calculte final premium post schedule rating and post deviation factor

    if std_fields.is_admitted_or_surplus in ("Surplus", "Admitted - LRE"):
        a_rating_dev_factor_selected = layer.a_rating_dev_factor
        hxd.cds.is_surplus = True  
    elif std_fields.insured_state_or_province:
        if layer.manual_premium * 3 > 100e3 and param_state[param_state["State"] == std_fields.insured_state_or_province]["Allows (a) Rating"].iloc[0] == "Yes":
            a_rating_dev_factor_selected = layer.a_rating_dev_factor
            hxd.cds.is_surplus = True
        else: 
            a_rating_dev_factor_selected = 1
            hxd.cds.is_surplus = False
    else:
        a_rating_dev_factor_selected = 1
        hxd.cds.is_surplus = False
    
    for loop_vbl in lst.cover_hxd_vbl(hxd):
        if loop_vbl.final_include is True:
            coverage_premium_prorated =                         loop_vbl.coverage_premium * layer.term_adjustment
            loop_vbl.coverage_premium_post_experience =         coverage_premium_prorated * hxd.cds.experience_rating.experience_modification
            loop_vbl.coverage_premium_post_schedule =           loop_vbl.coverage_premium_post_experience * (1 + layer.total_modifiers.uw_selected)
            loop_vbl.coverage_premium_post_a_rating =           loop_vbl.coverage_premium_post_schedule * a_rating_dev_factor_selected
            loop_vbl.coverage_premium_post_a_rating_annual =    loop_vbl.coverage_premium_post_a_rating / layer.term_adjustment



