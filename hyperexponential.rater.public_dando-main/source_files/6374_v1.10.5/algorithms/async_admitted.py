import hx, pyodbc
import pandas as pd
import numpy as np
import math
import algorithms.rate_utilities as utils
import algorithms.global_parameters as gparams
import algorithms.rate_constants as const

# def set_admitted_to_min(hxd, progress):
#     """
#     Loops through all the admitted steps with selected inputs and sets it to the minimum in the range
#     """
#     adm = hxd.cds.admitted 
#     set_admitted("min", adm, progress)
#     pass

# def set_admitted_to_max(hxd, progress):
#     """
#     Loops through all the admitted steps with selected inputs and sets it to the maximum in the range
#     """
#     adm = hxd.cds.admitted 
#     set_admitted("max", adm, progress)
#     pass

# def set_admitted_to_midpoint(hxd, progress):
#     """
#     Loops through all the admitted steps with selected inputs and sets it to the midpoint of the range
#     """
#     adm = hxd.cds.admitted 
#     set_admitted("midpoint", adm, progress)
#     pass

def set_admitted(hxd, target, adm, nyftz, progress):
    """
    Loops through all the admitted steps with selected inputs and sets it to the specified target in the range
    Accepts as an input whether the state is New York (FTZ). Since the BAIC rating plan is used for NYFTZ despite BICI being selected 

    """
    is_california = hxd.cds.admitted.baic.is_california
    baic_steps = const.get_baic_steps(is_california)
    if adm.insurer is not None:
        if (adm.insurer == "BICI") and (not nyftz):
            adm_insurer = adm.bici
            steps = const.bici_steps
        elif (adm.insurer == "BAIC") or (nyftz): 
            adm_insurer = adm.baic
            steps = baic_steps

        for step in (steps):
            step_path = getattr(adm_insurer, step)
            if target == "midpoint":
                range_min = getattr(step_path, "min") 
                range_max = getattr(step_path, "max") 

                if (range_min is not None) and (range_max is not None):
                    midpoint = round(range_min + (range_max - range_min) / 2, 4)

                    setattr(step_path,"selected", midpoint)
            else:
                range_target = getattr(step_path, target) 

                if range_target is not None:
                    setattr(step_path,"selected", range_target)



def reset_admitted_reasons(hxd, progress):
    """
    Sets the reason to the first element of the dropdown
    Useful when the state changes and so do the updates
    """
    is_california = hxd.cds.admitted.baic.is_california
    baic_other_steps, baic_other_steps_nums, baic_other_steps_labels = const.get_baic_other(is_california)
    adm = hxd.cds.admitted 
    
    if adm.insurer is not None:
        # Updating the insurer field so that the BAIC rating plan is used for NYFTZ despite BICI being selected
        insurer = 'BAIC' if hxd.cds.company_state == 'New York (FTZ)' else adm.insurer 
        if insurer == "BICI":
            adm_insurer = hxd.cds.admitted.bici
            
            df_state_detail = hx.params.bici_states_detail
            df_all_other_steps = hx.params.bici_all_other_steps
            
            dropdown_string = "_bici_dropdown"
            
            # List of steps in the rate_constants file
            steps = const.bici_other_steps
            step_numbers = const.bici_other_steps_nums
        elif insurer == "BAIC": 
            adm_insurer = hxd.cds.admitted.baic

            df_state_detail = hx.params.baic_states_detail
            df_all_other_steps = hx.params.baic_all_other_steps

            dropdown_string = "_baic_dropdown"
            steps = baic_other_steps
            step_numbers = baic_other_steps_nums

        df_row = df_state_detail[(df_state_detail["State"] == hxd.cds.company_state)].iloc[0]
        plan_type = df_row["PlanType"]
        list_type = df_row["ExtendedText"]

        df_all_other_steps = df_all_other_steps[
            (df_all_other_steps["PlanType"] == plan_type) &
            (df_all_other_steps["ListType"] == list_type)
        ]

        df_steps = pd.DataFrame({
            "step": step_numbers,
            "step_name" : steps
        })

        step_list = zip(step_numbers, steps)

        # Loops through the steps in the dataframe
        for step, step_name in step_list:

            # Creating reason dropdown
            filtered_df = df_all_other_steps[df_all_other_steps["Step"] == step]
            first_option = filtered_df["Activity"].iloc[0]
            #dropdown_path = step_path + dropdown_string
            #setattr(hxd.cds, dropdown_path, filtered_dropdown.to_dict("records"))

            step_path = getattr(adm_insurer, step_name)

            setattr(step_path,"reason", first_option) if getattr(step_path, "reason", "dummy value") != "dummy value" else None
