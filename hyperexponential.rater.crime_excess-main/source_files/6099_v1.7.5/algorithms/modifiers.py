import hx
import pandas as pd
import numpy as np
import algorithms.utils_global_lists as lst
import algorithms.utils_functions as fx

# ~~~~~~~~~~~~~~~~~~~ MODIFIERS ~~~~~~~~~~~~~~~~~~~

def modifiers(hxd):
    cds = hxd.cds
    cds_industry = cds.key_industry
    std_fields = cds.standard_fields
    param_mod = fx.df_to_dict(hx.params.modifier_limits, "Risk Characteristic", ["Max Credit Rate Plan", "Max Debit Rate Plan"])
    param_state = fx.df_to_dict(hx.params.state_lookup, "State", ["Schedule Min", "Schedule Max", "Eligibility Requirement (Before)", "Eligibility Requirement (After)"])
    param_expense = fx.df_to_dict(hx.params.expense_mod_limits, "State", ["Expense Mod Min", "Expense Mod Max", "Include in Risk Mod"])
       
    #The minimum and maxiumum modifiers are stored as a parameter table, loop through and set each node in the data schema 
    lst_modifier_vbl = [cds.classification_peculiarities, cds.management, cds.personnel, cds.location, cds.response_to_losses, cds.endorsements]
    lst_modifier_str = ["Classification Peculiarities", "Management", "Personnel", "Location", "Response to Losses","Endorsements"]

    for loop_vbl, loop_str in zip(lst_modifier_vbl,lst_modifier_str):
        #Always include these characteristics in the parameter table 
        loop_vbl.available = True
        
        #Look up the min/max for each parameter 
        loop_vbl.minimum_plan = param_mod[loop_str]["Max Credit Rate Plan"]
        loop_vbl.maximum_plan = param_mod[loop_str]["Max Debit Rate Plan"]
       
       #Depending on the state, the max/min modifiers for each characteristic may be further restricted
        if (cds.standard_fields.insured_state_or_province in ["LA", "NY"]):
            loop_vbl.minimum_state = max(-0.1, loop_vbl.minimum_plan)
            loop_vbl.maximum_state = min(0.1, loop_vbl.maximum_plan)
        elif (cds.standard_fields.insured_state_or_province == "NYFTZ"):
            loop_vbl.minimum_state = max(-0.15, loop_vbl.minimum_plan)
            loop_vbl.maximum_state = min(0.15, loop_vbl.maximum_plan)
        else:
            loop_vbl.minimum_state = loop_vbl.minimum_plan
            loop_vbl.maximum_state = loop_vbl.maximum_plan


    if std_fields.insured_state_or_province:
        #Set parameters for expense modification and include in individual risk modification table based on state requirements
        cds.expense_modification.minimum_state = param_expense[std_fields.insured_state_or_province]["Expense Mod Min"]
        cds.expense_modification.maximum_state = param_expense[std_fields.insured_state_or_province]["Expense Mod Max"]
        cds.expense_modification.available = param_expense[std_fields.insured_state_or_province]["Include in Risk Mod"]
        
        #Calculate the final mod factor once state min/max are applied to the total mod
        cds.total_unbounded = sum(item.selected for item in lst_modifier_vbl) + (cds.expense_modification.selected if cds.expense_modification.available else 0)
        cds.total_modifiers.minimum_state = param_state[std_fields.insured_state_or_province]["Schedule Min"]
        cds.total_modifiers.maximum_state = param_state[std_fields.insured_state_or_province]["Schedule Max"]
        cds.total_modifiers.selected = max(
            min(cds.total_unbounded,cds.total_modifiers.maximum_state),
            cds.total_modifiers.minimum_state
            )
        cds.mod_factor = 1 + cds.total_modifiers.selected
        cds.eligibility_min_before = param_state[std_fields.insured_state_or_province]["Eligibility Requirement (Before)"]
        cds.eligibility_min_after = param_state[std_fields.insured_state_or_province]["Eligibility Requirement (After)"]

    else:
        cds.mod_factor = 1
        cds.eligibility_min_before = 0
        cds.eligibility_min_after = 0


    #Create flag for separate expense modification section on the rating summary page
    cds.expense_mod_flag = False if (cds.expense_modification.minimum_state == 0 and cds.expense_modification.minimum_state == 0) else not cds.expense_modification.available
    cds.expense_mod_factor = 1 + cds.expense_modification.selected if cds.expense_mod_flag else 1

    #Surplus deviation factor
    cds.is_surplus = cds.standard_fields.is_admitted_or_surplus in ("Admitted - LRE", "Surplus")
    
    
