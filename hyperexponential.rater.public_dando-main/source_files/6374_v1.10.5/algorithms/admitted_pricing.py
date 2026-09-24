import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
import algorithms.rate_constants as const
from datetime import datetime, date

def admitted_pricing(hxd):
    # Saving locations as a variables for readability 
    agg = hxd.cds.exposure.aggregate
    adm = hxd.cds.admitted
    bici = hxd.cds.admitted.bici
    baic = hxd.cds.admitted.baic
    stn = hxd.cds.standard_fields

    # Steps depend on whether the state is California
    is_california = hxd.cds.admitted.baic.is_california
    baic_other_steps, baic_other_steps_nums, baic_other_steps_labels = const.get_baic_other(is_california)
    baic_all_steps = const.get_baic_all_steps(is_california)
    baic_calc_steps = const.get_baic_calc_steps(is_california)
    baic_steps = const.get_baic_steps(is_california)

    # Info displayed from main rater
    adm.company = hxd.cds.company_name
    adm.state = hxd.cds.company_state
    adm.inception_date = hxd.hx_core.inception_date
    assets = adm.total_assets = agg.total_assets

    insurer = adm.insurer

    # Setting field that unhides admitted information when conditions for admitted rating to apply are met
    adm.conditions_met = False
    if (
        (hxd.cds.company_state is not None) & 
        (hxd.cds.company_state in list(hx.params.bici_states_detail["State"])) &
        (hxd.cds.uw_location == "US")
    ):
       adm.conditions_met = True

    # Updating standard field for reporting
    stn.is_admitted_or_surplus.calculated = "Admitted" if adm.conditions_met else "Surplus"

    # Final admitted check
    # US business can be surplus so there is an additional manual update
    adm.is_admitted = True if (
        (stn.is_admitted_or_surplus.selected == "Admitted") and 
        (adm.conditions_met) and 
        (hxd.model_state.show_after_landing_page) and 
        (hxd.cds.admitted_excess.is_primary_excess == "Primary") 
    ) else False
    # Ignoring blank BICI states
    if adm.is_admitted:
        adm.is_admitted = False if (insurer == "BICI") and (hx.params.bici_states_detail[(hx.params.bici_states_detail["State"] == hxd.cds.company_state)].iloc[0]["PlanType"] == "No Value") else True

    # Setting boolean for when US surplus
    # Used to unhide the dropdown for surplus entity
    adm.is_not_admitted = not adm.is_admitted

    if insurer is not None:
        # Validates whether the rating plan has been approved for BAIC
        if (insurer == "BAIC") & (adm.is_admitted):
            df_approved = hx.params.baic_approved_states

            if isinstance(hxd.hx_core.inception_date, datetime):
                inception_date = hxd.hx_core.inception_date.date()
            else: inception_date = hxd.hx_core.inception_date

            if utils.look_up(hxd.cds.company_state,"State","Approved?",df_approved) != "Approved":
                hx.errors.validation("This state is not approved under the current BAIC rating plan")
            if inception_date < date(2025, 1, 1):
                hx.errors.validation("BAIC is effective 01-Jan 2025")

        # Updating the insurer field so that the BAIC rating plan is used for NYFTZ despite BICI being selected
        insurer = 'BAIC' if hxd.cds.company_state == 'New York (FTZ)' else insurer
        
        # Admitted calculated for selected option only
        selected_option = adm.selected_option - 1 if adm.selected_option else const.max_layers + 1

        if (adm.is_admitted) & (selected_option <= len(hxd.cds.layers) - 1):
            # Setup factors depending on rating plan (insurer)
            if insurer == "BICI":
                # Field for hiding or showing the admitted rating plan
                adm.is_bici = True
                adm.is_baic = False

                # Pointing the hxd to the correct insurer
                adm_insurer = bici

                df_state_detail = hx.params.bici_states_detail
                df_version = hx.params.bici_version
            elif insurer == "BAIC":
                adm.is_bici = False
                adm.is_baic = True

                adm_insurer = baic

                df_state_detail = hx.params.baic_states_detail
                df_version = hx.params.baic_version

            # Sets the plan factors for the given state
            df_row = df_state_detail[(df_state_detail["State"] == hxd.cds.company_state)].iloc[0]
            plan_type = df_row["PlanType"]
            list_type = df_row["ExtendedText"]
            rounding = df_row["RoundingPermitted?"]

            plan_version = utils.look_up(hxd.cds.company_state, "State", "PlanVersion", df_version)
        
            # Calculates base premium
            if assets is not None:
                calc_admitted_base_premium(hxd, insurer)

            # Sets up reason, min and max for industry factor
            # Reason is calculated not selected like for other steps
            setup_admitted_industry_factor(hxd, insurer, plan_type)

            # All other factors
            # Those that aren't calculated or have any other unique features
            if insurer == "BICI":
                # Pulling the steps and their numbers from the rate_constants file
                step_names = const.bici_other_steps
                step_numbers = const.bici_other_steps_nums
            elif insurer == "BAIC":
                step_names = baic_other_steps
                step_numbers = baic_other_steps_nums

            # Function to set the dropdowns for the listed states
            # Then sets the min and max based on the selected reason
            setup_all_other_admitted_steps(
                hxd,
                insurer,
                plan_type,
                list_type,
                step_names,
                step_numbers
            )

            # Calculates retention factor
            # Carrying out a bilinear interpolation on assets and retention
            cov = "side_a" if hxd.cds.is_side_a else "abc"

            deductible = getattr(getattr(getattr(hxd.cds.layers[selected_option], "coverages"), cov), "deductible")
            excess = getattr(getattr(getattr(hxd.cds.layers[selected_option], "coverages"), cov), "excess")
            limit = getattr(getattr(getattr(hxd.cds.layers[selected_option], "coverages"), cov), "limit")
            quoted_premium = getattr(getattr(getattr(hxd.cds.layers[selected_option], "coverages"), cov), "premium")

            # Adding the tower to the side A excess. This is only for display, not the calculations
            tower = getattr(getattr(getattr(hxd.cds.layers[selected_option], "coverages"), cov), "tower") if hxd.cds.is_side_a else 0
            excess = excess + tower if (tower is not None) & (excess is not None) else excess

            # Info displayed from main rater
            adm.deductible = deductible
            adm.excess = excess
            adm.limit = limit
            adm.quoted_premium = quoted_premium

            # BICI interpolates between deductible and assets
            # BAIC between deductible and limit
            if (deductible is not None):
                if (insurer == "BICI") and (assets is not None):
                    calc_admitted_retention_factor(hxd, insurer, deductible, assets, limit, plan_version)
                elif (insurer == "BAIC") and (limit is not None):
                    calc_admitted_retention_factor(hxd, insurer, deductible, assets, limit, plan_version)

            # Calculates limit factor
            # Only a factor for BICI    
            if (limit is not None) & (insurer == "BICI"):
                bici.step_18_llm.selected = calc_admitted_limit_factor(hxd, limit)

            # Final calculated premium factor
            # Only applies if the state is Nebraska
            if hxd.cds.company_state == "Nebraska":
                setup_final_calc_premium_factor(hxd, insurer)

            # Final premium
            if insurer == "BICI":
                # Need all steps except the additional factor
                steps = const.bici_all_steps
                # Passing the hxd path to the function
                steps = [getattr(bici, step) for step in steps]
            elif insurer == "BAIC":
                steps = baic_calc_steps
                steps = [getattr(baic, step) for step in steps]

            # Calculates the final premium from all the other steps
            calc_final_premium(hxd, insurer, steps)
        
            # Rounding
            if (adm_insurer.final_premium is not None):
                setup_admitted_rounding(hxd, insurer, rounding)


def calc_admitted_base_premium(hxd, insurer):
    bici = hxd.cds.admitted.bici
    baic = hxd.cds.admitted.baic
    assets = hxd.cds.exposure.aggregate.total_assets
    baic_steps = const.get_baic_steps(hxd)

    if insurer == "BICI":
        df_base_premium = hx.params.bici_1_base_premium
        if assets >= max(df_base_premium["Asset Range 1 Lower"]):
            bici.step_1_bpm.message = "Total Assets are above $100B. Submit to Home Office"
        elif assets >= 0:
            base_premium = utils.look_up_with_bounds(
                assets, 
                "Asset Range 1 Lower", 
                "Asset Range 1 Upper", 
                "Annual Premium", 
                df_base_premium,
                0
            )
            bici.step_1_bpm.selected = base_premium
            bici.step_1_bpm.message = "If Total Assets are above $100B, please submit to Home Office"
    elif insurer == "BAIC":
        df_base_premium = hx.params.baic_1_base_premium
        if assets > 0:
            asset_match = utils.look_up_with_bounds( 
                assets, 
                "Asset Range 1", 
                "Asset Range 2", 
                "Asset Range 1", 
                df_base_premium,
                0
            )
            asset_match = max(asset_match, const.baic_max_assets)

            df_row = df_base_premium[(df_base_premium["Total Assets"] == asset_match)].iloc[0]

            initial_rate = df_row["Annual Premium"]
            marginal_asset = max(assets - asset_match, 0)
            marginal_rate = df_row["Marginal Rate"]
            marginal_per = df_row["Marginal Rate Per $"]

            base_premium = initial_rate + marginal_rate * utils.ratio(marginal_asset, marginal_per)
            baic.step_1_bpm.selected = base_premium

            df_baic_comments = hx.params.baic_all_other_steps

            # Populate infoBy labels (message)
            for step in baic_steps:
                #determine rate
                selected_rate = getattr(getattr(hxd.cds.admitted.baic,step), "selected")
                rate = selected_rate if selected_rate is not None else getattr(getattr(hxd.cds.admitted.baic,step), "min")
                if rate is None:
                    rate = 1.0

                selected_reason = getattr(getattr(hxd.cds.admitted.baic,step), "reason", None)
                
                df_filtered = df_baic_comments[df_baic_comments["ModifierName"] == step]
                if df_filtered.empty:
                    #setattr(getattr(hxd.cds.admitted.baic, step), "message", "No Description")
                    1 == 1
                else:
                    # df_comment = df_filtered[(df_filtered["Min"] <= rate) & (df_filtered["Max"] >= rate)]
                    # if df_comment.empty:
                    #     setattr(getattr(hxd.cds.admitted.baic, step), "message", "Rate out of Range")
                    # else:
                    df_comment = df_filtered[df_baic_comments["Activity"] == selected_reason]
                    if not df_comment.empty:
                        state_col = "WAState" if hxd.cds.admitted.state == "Washington" else "AllStates"
                        comment = df_comment[state_col].iloc[0] 
                        setattr(getattr(hxd.cds.admitted.baic, step), "message", comment)
            
            # California modifiers
            # TODO: Move this to a better function that isn't the base premium
            sum_ca_rate = 0
            bounds_flag = False
            for step in const.baic_ca_input_steps:
                selected_rate = getattr(getattr(hxd.cds.admitted.baic,step), "selected")
                if selected_rate is None:
                    rate = 0
                    bounds_flag = True
                else:
                    rate = selected_rate
                    df_range_test = df_filtered[(df_filtered["Min"] <= rate) & (df_filtered["Max"] >= rate)]
                    if df_range_test.empty:
                        bouncds_flag = True

                sum_ca_rate += rate
            
            if bounds_flag == True:
                hxd.cds.admitted.baic.step_20_srf.selected = 0
            else:
                hxd.cds.admitted.baic.step_20_srf.selected = max(min(1 + sum_ca_rate, 1.25), 0.75)

def setup_admitted_industry_factor(hxd, insurer, plan_type):
    if insurer == "BICI":
        df_industry_reason = hx.params.bici_2a_industry
        df_industry = hx.params.bici_2b_industry
        adm = hxd.cds.admitted.bici
    elif insurer == "BAIC":
        df_industry_reason = hx.params.baic_2a_industry
        df_industry = hx.params.baic_2b_industry
        adm = hxd.cds.admitted.baic       
    
    if hxd.cds.key_industry.code is not None:
        im_reason = utils.look_up(int(hxd.cds.key_industry.code), "SICCode", "Admitted", df_industry_reason, "Not Found")
        adm.step_2_im.reason = im_reason

        if im_reason != "Not Found":
            df_row = df_industry[(df_industry["Industry Modifier"] == im_reason)].iloc[0]
            if plan_type == "Range":
                im_range_min = df_row["min"]
                im_range_max = df_row["max"]
            else:
                im_range_min = df_row["No Range"]
                im_range_max = df_row["No Range"]
            
            im_range = df_row["Modifier Range"]
            
            adm.step_2_im.min = im_range_min
            adm.step_2_im.max = im_range_max

            # Setting validation for if selected is outside min and max
            selected = adm.step_2_im.selected
            if selected is not None:
                if (selected < im_range_min) or (selected > im_range_max):
                    hx.errors.validation("Value selected for step 2 is outside of the allowed range")
        

def calc_admitted_limit_factor(hxd, limit):
    # Only in the bici rating plan
    df_limit = hx.params.bici_15_limit

    if limit > max(df_limit["limit lower"]):
        limit_factor = max(df_limit["Modifier"])
    elif limit <= min(df_limit["limit lower"]):
        limit_factor = min(df_limit["Modifier"])
    else:
        df_row = df_limit[
            (df_limit["limit lower"] <= limit) & 
            (df_limit["limit upper"] > limit)
        ].iloc[0]
        initial_mod = df_row["Modifier"]
        limit_lower = df_row["limit lower"]
        limit_step = df_row["step"] 
        limit_change = df_row["change"]

        limit_factor = initial_mod + utils.ratio((limit - limit_lower), limit_step) * limit_change

    return limit_factor

def setup_all_other_admitted_steps(hxd, insurer, plan_type, list_type, step_names, step_numbers):
    if insurer == "BICI":
        adm = hxd.cds.admitted.bici
        df_all_other_steps = hx.params.bici_all_other_steps
        dropdown_string = "_bici_dropdown"
    elif insurer == "BAIC": 
        adm = hxd.cds.admitted.baic
        df_all_other_steps = hx.params.baic_all_other_steps
        dropdown_string = "_baic_dropdown"

    # Pre filters for state plan factors
    df_all_other_steps = df_all_other_steps[
        (df_all_other_steps["PlanType"] == plan_type) &
        (df_all_other_steps["ListType"] == list_type)
    ]

    step_list = zip(step_numbers, step_names)

    # Loops through the steps in the dataframe
    for step, step_path in step_list:
        # Creating reason dropdown
        filtered_df = df_all_other_steps[df_all_other_steps["Step"] == step]
        filtered_dropdown = filtered_df[["Activity"]]
        dropdown_path = step_path + dropdown_string
        setattr(adm, dropdown_path, filtered_dropdown.to_dict("records")) if getattr(adm, dropdown_path, None) is not None else None

        # Pulling the reason entered for the step
        step_path = getattr(adm, step_path)
        reason = getattr(step_path, "reason", "None")

        # For entered reasons, displaying their min and max values
        if reason is not None:
            # If a reason entered is not in the dropdown then the final premium won't calculate
            # This is needed when the dropdown updates with the state but a reason was previously selected
            if reason in list(filtered_dropdown["Activity"]):
                # Looking up min and max
                df_row = df_all_other_steps[(df_all_other_steps["Activity"] == reason) & (df_all_other_steps["Step"] == step)].iloc[0]
                if plan_type == "Range":
                    range_min = df_row["Min"]
                    range_max = df_row["Max"]
                else:
                    if df_row["Step"] in const.baic_ca_input_steps_numbers :   # exception for the CA specific steps which need to be a range as opposed to No Range which is default for CA
                        range_min = df_row["Min"]
                        range_max = df_row["Max"]
                    else:
                        range_min = df_row["Value"]
                        range_max = df_row["Value"]

                # Updating hxd
                setattr(step_path, "min", range_min)
                setattr(step_path, "max", range_max)

                selected = (getattr(step_path, "selected"))
                if selected is not None:
                    # Setting validation for if selected is outside min and max
                    if (selected < range_min) or (selected > range_max):
                        hx.errors.validation("Value selected for step " + str(step) + " is outside of the allowed range")          


def calc_admitted_retention_factor(hxd, insurer, deductible, assets, limit, plan_version):
    if plan_version == 1:
        if insurer == "BICI":
            df_retention = hx.params.bici_15_retention_v1
        elif insurer == "BAIC":
            df_retention = hx.params.baic_15_combined_lr
    else:
        if insurer == "BICI":
            df_retention = hx.params.bici_15_retention_v2
        elif insurer == "BAIC":
            df_retention = hx.params.baic_15_combined_lr
    
    # The first column in the BICI table includes the asset band label.
    # Removing that here
    if insurer == "BICI": df_retention = df_retention.iloc[:, 1:] 

    # Defining the x values
    retention = list(df_retention.columns.values)
    retention = retention[1:]
    retention = [int(x) for x in retention]

    # Defining the different y values for BICI and BAIC
    if insurer == "BICI":
        asset_list = list(df_retention["Total Assets"])
    elif insurer == "BAIC":  
        limit_list = list(df_retention["Limit"])

    # Carrying out the bilinear interpolation
    if insurer == "BICI":
        hxd.cds.admitted.bici.step_15_rm.selected = bilinear_interpolation(df_retention, retention, asset_list, deductible, assets, insurer)
        if hxd.cds.admitted.bici.step_15_rm.selected == 0:
            hx.errors.validation("Invalid retention - please check sufficient for size of firm against Admitted Plan")
    elif insurer == "BAIC":
        hxd.cds.admitted.baic.step_15_clrm.selected = bilinear_interpolation(df_retention, retention, limit_list, deductible, limit, insurer)


def bilinear_interpolation(df, x_values, y_values, x, y, insurer):
    # Only calculates if x is within the x values
    if x < max(x_values) and x >= min(x_values):
        x1 = max([i for i in x_values if i <= x])                       
        x2 = min([i for i in x_values if i >= x])
        
        # If y is larger than the max then still calculates but using the max
        # This is unique to the admitted calcs this was built for
        # May need adjusting for other scenarios requiring bilinear interpolation
        if y < max(y_values):
            y1 = max([i for i in y_values if i <= y])                     
            y2 = min([i for i in y_values if i >= y]) if insurer == "BAIC" else y1
        else:  
            y1 = max(y_values)
            y2 = max(y_values)
        
        f_q11 = df.iloc[y_values.index(y1), x_values.index(x1) + 1]
        if f_q11 > 0:
            f_q21 = df.iloc[y_values.index(y1), x_values.index(x2) + 1]
            f_q12 = df.iloc[y_values.index(y2), x_values.index(x1) + 1]
            f_q22 = df.iloc[y_values.index(y2), x_values.index(x2) + 1] 

            f_x_y1 = np.interp(y, [y1,y2], [f_q11, f_q12]) 
            f_x_y2 = np.interp(y, [y1,y2], [f_q21, f_q22])   
            f_x_y =  np.interp(x, [x1,x2], [f_x_y1, f_x_y2]) 
        else:  
            f_x_y = 0
    else:  
        f_x_y = 0

    return f_x_y   

def setup_final_calc_premium_factor(hxd, insurer):
    if insurer == "BICI":
        adm = hxd.cds.admitted.bici
        adm_step = adm.step_18a_fcp
        step_num = "18a"
    elif insurer == "BAIC":
        adm = hxd.cds.admitted.baic
        adm_step = adm.step_19a_fcp
        step_num = "19a"

    # Setting the boolean to show the factor in the view
    adm.show_final_prem_factor = True

    adm_step.min = const.admitted_final_premium_factor_min
    adm_step.max = const.admitted_final_premium_factor_max 

    if adm_step.selected is not None:
        if (adm_step.selected < adm_step.min) or (adm_step.selected > adm_step.max):
            hx.errors.validation("Value selected for step " + step_num + " is outside of the allowed range")
    pass

def calc_final_premium(hxd, insurer, steps):
    if insurer == "BICI":
        adm = hxd.cds.admitted.bici
        final_calc = adm.step_18a_fcp
        remove_steps = [adm.step_1_bpm, adm.step_15_rm, adm.step_18_llm]
    elif insurer == "BAIC":
        adm = hxd.cds.admitted.baic   
        final_calc = adm.step_19a_fcp
        remove_steps = [adm.step_1_bpm, adm.step_15_clrm, adm.step_20_srf]
    
    # Removing calculated steps from the min check
    other_steps = [step for step in steps if step not in remove_steps]

    if (
        all(getattr(step, "selected") is not None for step in steps) and
        all(getattr(step, "min") is not None for step in other_steps)
    ):
        steps = [getattr(step, "selected") for step in steps]
        adm.final_premium = np.prod(steps)

        if (hxd.cds.company_state == "Nebraska") and (final_calc.selected is not None):
            adm.final_premium = adm.final_premium * final_calc.selected
        
        adm.final_premium = round(adm.final_premium, 0)
    else: 
        adm.final_premium is None

    # If a final premium hasn't been calculated then raise an error
    hx.errors.validation("Insufficient information to calculate the Admitted Premium") if adm.final_premium is None else None

def setup_admitted_rounding(hxd, insurer, rounding):
    # If the state doesn't allow rounding then just need to communicate this
    if insurer == "BICI":
        adm = hxd.cds.admitted.bici
    elif insurer == "BAIC":
        adm = hxd.cds.admitted.baic

    # Defaulting the rounded premium to the calculated premium
    adm.rounded_premium.calculated = round(adm.final_premium, 0)

    if (rounding == "True"):
        if insurer == "BICI":
            df_rounding = hx.params.bici_rounding
        elif insurer == "BAIC":
            df_rounding = hx.params.baic_rounding

        premium_lookup = round(adm.final_premium, 0)
        
        if premium_lookup >= max(df_rounding["Premium Lower"]):
            rounding_amount = max(df_rounding["Rounding amount"])
        else:
            rounding_amount = utils.look_up_with_bounds(premium_lookup, "Premium Lower", "Premium Upper", "Rounding amount", df_rounding)
        
        rounding_lower = premium_lookup - rounding_amount
        rounding_upper = premium_lookup + rounding_amount

        adm.rounding_message = (
            "This State allows rounding in range [" + 
            "{:,.0f}".format(rounding_lower) +
            " - " +
            "{:,.0f}".format(rounding_upper) +
            "]"
        )

        if adm.rounded_premium.selected is not None:
            if (adm.rounded_premium.selected < rounding_lower) or (adm.rounded_premium.selected > rounding_upper):
                hx.errors.validation("Rounded premium is outside the rounding range")
        else:
            hx.errors.validation("Please enter a rounded premium in the admitted section") 
    else:
        adm.rounding_message = "Rounding not permitted"

        if adm.rounded_premium.selected is not None:
            if abs(adm.rounded_premium.selected - adm.final_premium) >= 0.5:
                hx.errors.validation("Rounded premium is outside the rounding range")
        else:
            hx.errors.validation("Please enter a rounded premium in the admitted section") 
