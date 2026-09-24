import hx
from algorithms import rate_constants as constants
from algorithms.rate_utilities import look_up, look_up_with_bounds, agg_lim_calc, factor_validation


def fetch_state_info(hxd):
    if hxd.cds.standard_fields.is_admitted_or_surplus == "Surplus":
        state_code = "Surplus"
    else:
        state_code = look_up(hxd.cds.state, "State Name", "Abbreviation", hx.params.table_reference_state)

    # Fetch the row corresponding to the state_code
    cols = [
        "Rounding", 
        "Allows Removal of Punitive Damages?",
        "Allows Ranges?",
        "Schedule Rating Table",
        "Risk Characteristic Change",
        "Minimum Premium",
        "Minimum Aggregate Limit",
        "Min Before Schedule Rating",
        "Max Aggregate Schedule Rating Debit",
        "Max Aggregate Schedule Rating Credit"
    ]
    df_res = look_up(state_code, "State", cols, hx.params.table_pcl_admitted_applicabilities)

    # Determine rounding value
    rounding_value = "Standard" if df_res["Rounding"] == "Standard" else "Nearest Dollar"

    # Determine punitive damages policy
    punitive_damages_mapping = {
        "Deleted": "No",
        "Yes": "Yes"
    }
    punitive_damages = punitive_damages_mapping.get(df_res["Allows Removal of Punitive Damages?"], "Apply to all")

    # #set the shownby condition
    # if punitive_damages == "Yes":
    #     hxd.non_cds.is_punitive_damages = True

    # Prepare data dictionary
    state_info = {
        "state": hxd.cds.state,
        "surplus_lines": hxd.cds.standard_fields.is_admitted_or_surplus,
        "state_code": state_code,
        "allows_ranges": df_res["Allows Ranges?"],
        "rounding": rounding_value,
        "schedule_rating_table": df_res["Schedule Rating Table"],
        "risk_characteristic_change": df_res["Risk Characteristic Change"],
        "allows_removal_of_punitive_damages": punitive_damages,
        "minimum_premium": df_res["Minimum Premium"],
        "minimum_limit": df_res["Minimum Aggregate Limit"],
        "basic_limit_premium_eligibility": df_res["Min Before Schedule Rating"],
        "schedule_rating_min": df_res["Max Aggregate Schedule Rating Debit"],
        "schedule_rating_max": df_res["Max Aggregate Schedule Rating Credit"],
    }

    return state_info

def set_retention_value(option, results):

    retention = option.retention
    results.setdefault("selected_retention_pcl", []).append(retention)


def fetch_asset_and_retention_categories(hxd, state_info, results, new_idx):
    input_value = hxd.cds.exposure.granular.pcl.base_rate.asset_size
    retention_input = results.get('selected_retention_pcl')[new_idx]
    input_to_use = input_value if input_value else constants.assets_base_rate_pcl_default
    retention_to_use = retention_input if retention_input else constants.retention_pcl_default

    #We can not use the standard method for lookup here as the table is structured differently
    table = hx.params.table_pcl_base_rate_ranges_cw

    row_to_use = table[
        (table["Min"] <= input_to_use) & (table["Max"] >= input_to_use)
    ].iloc[0]
    # extract the values we need
    assets_base_rate_pcl = row_to_use["Base Premium"]
    asset_size_category_pcl = row_to_use["Asset Size Category"]

    # set them to the results dictionary to be used later
    results["assets_input_pcl"] = input_to_use
    results["asset_size_category_pcl"] = asset_size_category_pcl
    results["assets_base_rate_pcl"] = assets_base_rate_pcl

    # set the retention factor based on the asset size
    if state_info["state_code"] == "FL":
        table = hx.params.table_pcl_retention_factors_fl
    else:
        table = hx.params.table_pcl_retention_factors_cw

    asset_size_category_pcl = results.get("asset_size_category_pcl") + 1
    col = table.columns[asset_size_category_pcl]

    df_res = look_up_with_bounds(retention_to_use, "Retention - Low", "Retention - High", ["Retention - Low", "Retention - High"], table)
    retention_low = df_res["Retention - Low"]
    retention_high = df_res["Retention - High"]
    results["asset_size_retention_low"] = retention_low
    results["asset_size_retention_high"] = retention_high

    factor_low = look_up(retention_low, "Retention - Low", col, table)
    factor_high = look_up(retention_high, "Retention - Low", col, table)
    results["retention_factor_low"] = df_res["Retention - Low"]
    results["retention_factor_high"] = df_res["Retention - High"]




def validate_inputs_risk_characteristics(hxd, results, state_info):
    mod_table = hxd.cds.modifiers.pcl.modifiers_table
    risk_char_table = hx.params.table_pcl_risk_characteristics_cw

    risk_condition = state_info.get("risk_characteristic_change")
    allows_range_condition = state_info.get("allows_ranges")

    column_lookup_min = "Low" if allows_range_condition == "TRUE" else "No Range"
    column_lookup_max = "High" if allows_range_condition == "TRUE" else "No Range"


    # FINANCIAL CONDITIONS
    factor_selection = mod_table.financial_condition.factor_selection
    
    financial_conditions_string = "Financial Condition&" + str(mod_table.financial_condition.description)
    if risk_condition == "Deleted":
        min_val = 0
        max_val = 0
    else:
        df_res = look_up(financial_conditions_string, "Risk", [column_lookup_min, column_lookup_max, "No Range"], risk_char_table)
        min_val = round(df_res[column_lookup_min] - 1, 6)
        max_val = round(df_res[column_lookup_max] - 1, 6)
        factor_selection.calculated = round(df_res["No Range"] - 1, 6)

    if factor_selection.selected is not None:
        factor_validation(min_val, max_val, factor_selection.selected, "In PCL Inputs Sheet:  Financial Conditions Modifier",)

    mod_table.financial_condition.min = min_val
    mod_table.financial_condition.max = max_val
    results["financial_condition_to_use"] = (factor_selection.selected or 0) + 1

    # PROFITABILITY
    factor_selection = mod_table.profitability.factor_selection

    profitability_string = "Profitability&" + str(mod_table.profitability.description)
    if risk_condition == "Deleted":
        min_val = 0
        max_val = 0
    else:
        df_res = look_up(profitability_string, "Risk", [column_lookup_min, column_lookup_max, "No Range"], risk_char_table)
        min_val = round(df_res[column_lookup_min] - 1, 6)
        max_val = round(df_res[column_lookup_max] - 1, 6)
        factor_selection.calculated = round(df_res["No Range"] - 1, 6)

    if factor_selection.selected is not None:
        factor_validation(min_val, max_val, factor_selection.selected, "In PCL Inputs Sheet: Profitability Modifier")

    mod_table.profitability.min = min_val
    mod_table.profitability.max = max_val
    results["profitability_to_use"] = (factor_selection.selected or 0) + 1

    # MERGERS AND ACQUISITIONS
    factor_selection = mod_table.mergers_and_acquisition_activity.factor_selection

    merger_acquisition_string = "Merger Acquisition Activity&" + str(mod_table.mergers_and_acquisition_activity.description)
    if risk_condition == "Deleted":
        min_val = 0
        max_val = 0
    else:
        df_res = look_up(merger_acquisition_string, "Risk", [column_lookup_min, column_lookup_max, "No Range"], risk_char_table)
        min_val = round(df_res[column_lookup_min] - 1, 6)
        max_val = round(df_res[column_lookup_max] - 1, 6)
        factor_selection.calculated = round(df_res["No Range"] - 1, 6)

    if factor_selection.selected is not None:
        factor_validation(min_val, max_val, factor_selection.selected, "In PCL Inputs Sheet: Mergers and Acquisitions Modifier")

    mod_table.mergers_and_acquisition_activity.min = min_val
    mod_table.mergers_and_acquisition_activity.max = max_val
    results["merger_acquisition_to_use"] = (factor_selection.selected or 0) + 1

    # LAYOFFS, DOWNSIZING, OR SPINOFFS
    factor_selection = mod_table.layoffs_downsizing_or_spinoffs.factor_selection

    layoffs_string = "Layoffs, Downsizing, or spin-offs&" + str(mod_table.layoffs_downsizing_or_spinoffs.description)
    if risk_condition == "Deleted":
        min_val = 0
        max_val = 0
    else:
        df_res = look_up(layoffs_string, "Risk", [column_lookup_min, column_lookup_max, "No Range"], risk_char_table)
        min_val = round(df_res[column_lookup_min] - 1, 6)
        max_val = round(df_res[column_lookup_max] - 1, 6)
        factor_selection.calculated = round(df_res["No Range"] - 1, 6)

    if factor_selection.selected is not None:
        factor_validation(min_val, max_val, factor_selection.selected, "In PCL Inputs Sheet: Layoffs, Downsizing or Spinoffs Modifier")

    mod_table.layoffs_downsizing_or_spinoffs.min = min_val
    mod_table.layoffs_downsizing_or_spinoffs.max = max_val
    results["layoffs_to_use"] = (factor_selection.selected or 0) + 1

    # LITIGATION
    factor_selection = mod_table.litigation.factor_selection

    litigation_string = "Litigation&" + str(mod_table.litigation.description)
    if risk_condition == "Deleted":
        min_val = 0
        max_val = 0
    else:
        df_res = look_up(litigation_string, "Risk", [column_lookup_min, column_lookup_max, "No Range"], risk_char_table)
        min_val = round(df_res[column_lookup_min] - 1, 6)
        max_val = round(df_res[column_lookup_max] - 1, 6)
        factor_selection.calculated = round(df_res["No Range"] - 1, 6)        

    if factor_selection.selected is not None:
        factor_validation(min_val, max_val, factor_selection.selected, "In PCL Inputs Sheet: Litigation Modifier")

    mod_table.litigation.min = min_val
    mod_table.litigation.max = max_val
    results["litigation_to_use"] = (factor_selection.selected or 0) + 1

    # OWNERSHIP
    factor_selection = mod_table.ownership.factor_selection

    ownership_string = "Ownership&" + str(mod_table.ownership.description)
    if risk_condition == "Deleted":
        min_val = 0
        max_val = 0
    else:
        df_res = look_up(ownership_string, "Risk", [column_lookup_min, column_lookup_max, "No Range"], risk_char_table)
        min_val = round(df_res[column_lookup_min] - 1, 6)
        max_val = round(df_res[column_lookup_max] - 1, 6)
        factor_selection.calculated = round(df_res["No Range"] - 1, 6)

    if factor_selection.selected is not None:
        factor_validation(min_val, max_val, factor_selection.selected, "In PCL Inputs Sheet: Ownership Modifier")

    mod_table.ownership.min = min_val
    mod_table.ownership.max = max_val
    results["ownership_to_use"] = (factor_selection.selected or 0) + 1

    # LENGTH OF TIME IN BUSINESS
    factor_selection = mod_table.length_of_time_in_business.factor_selection

    time_in_business_string = "Length of time in business&" + str(mod_table.length_of_time_in_business.description)
    if risk_condition == "Deleted":
        min_val = 0
        max_val = 0
        factor_selection.calculated = 0
    else:
        df_res = look_up(time_in_business_string, "Risk", [column_lookup_min, column_lookup_max, "No Range"], risk_char_table)
        min_val = round(df_res[column_lookup_min] - 1, 6)
        max_val = round(df_res[column_lookup_max] - 1, 6)
        factor_selection.calculated = round(df_res["No Range"] - 1, 6)

    if factor_selection.selected is not None:
        factor_validation(min_val, max_val, factor_selection.selected, "In PCL Inputs Sheet: Length of Time in Business Modifier")

    mod_table.length_of_time_in_business.min = min_val
    mod_table.length_of_time_in_business.max = max_val
    results["time_in_business_to_use"] = (factor_selection.selected or 0) + 1

    # QUALITY OF MANAGEMENT
    factor_selection = mod_table.quality_of_management.factor_selection

    management_quality_string = "Quality of Management&" + str(mod_table.quality_of_management.description)
    if risk_condition == "Deleted":
        min_val = 0
        max_val = 0
        factor_selection.calculated = 0
    else:
        df_res = look_up(management_quality_string, "Risk", [column_lookup_min, column_lookup_max, "No Range"], risk_char_table)
        min_val = round(df_res[column_lookup_min] - 1, 6)
        max_val = round(df_res[column_lookup_max] - 1, 6)
        factor_selection.calculated = round(df_res["No Range"] - 1, 6)

    if factor_selection.selected is not None:
        factor_validation(min_val, max_val, factor_selection.selected, "In PCL Inputs Sheet: Quality of Management Modifier")

    mod_table.quality_of_management.min = min_val
    mod_table.quality_of_management.max = max_val
    results["management_quality_to_use"] = (factor_selection.selected or 0) + 1


def fetch_admitted_cob_factor(hxd, results):
    revenue = hxd.cds.exposure.granular.pcl.base_rate.revenue or 0

    granular_shortcut = hxd.cds.exposure.granular.pcl

    table_string = look_up(hxd.cds.industry.naics_code, "NAICS Code", "tblPCL_NAICSMap", hx.params.table_naics_master)

    cob_input = "Table A Class of Business" if revenue > constants.tableA_limit_pcl else table_string

    admitted_cob_factor = look_up(cob_input, "Description", "Modifier", hx.params.table_pcl_cob_code)

    #best direct way if output nodes
    granular_shortcut.class_of_business_table = {
        "option_1" : {"table_a": "Financial Institutions", "table_b": "Entertainment"},
        "option_2" : {"table_a": "High Tech/Bio-Tech Firms", "table_b": "Governmental Organizations"},
        "option_3" : {"table_a": "Health Care","table_b": "Utilities"},
        "option_4" : {"table_a": "Defense Contractors","table_b": "Industries in Consolidation"},
        "option_5" : {"table_a": "Revenues greater than $250M","table_b": ""},    
        }            
    
    granular_shortcut.class_of_business = cob_input                                  

    results["admitted_cob_factor"] = admitted_cob_factor


def fetch_admitted_punitive_damages_factor(hxd, results, state_info):
    mod_table = hxd.cds.modifiers.pcl.modifiers_table
    description = mod_table.reactive_removal_of_punitive_damages.removal_of_punitive_damages.description
    
    # Premim Credit if Punitive Dmages Coverage is completely removed from the policy by endorsement
    credit_decision = state_info.get("allows_removal_of_punitive_damages")
    #work through the logic with Apply to all taking precident over the drop down logic
    #this is a deliberate deviation from the excel file
    if credit_decision == "Apply to all":
        factor_min = constants.punitive_damages_default_pcl
        factor_max = constants.punitive_damages_default_pcl
        calculated_factor = constants.punitive_damages_default_pcl
        drop_down_descripton = ["Mandate"]
      
    elif credit_decision == "Yes":
        drop_down_descripton = ["Yes", "No"]
        if description == "Yes":
            factor_min = constants.punitive_damages_yes_min_pcl
            factor_max = constants.punitive_damages_yes_max_pcl
            calculated_factor = constants.punitive_damages_default_pcl
        else:
            factor_min = constants.punitive_damages_no_pcl
            factor_max = constants.punitive_damages_no_pcl
            calculated_factor = constants.punitive_damages_no_pcl

    else:
        factor_min = constants.punitive_damages_no_pcl
        factor_max = constants.punitive_damages_no_pcl
        calculated_factor = constants.punitive_damages_no_pcl
        drop_down_descripton = ["No"]

    #set the values for the drop downs
    reactive_removal_of_punitive_damages_dropdown = drop_down_descripton

    mod_table.reactive_removal_of_punitive_damages.reactive_removal_of_punitive_damages_dropdown = [
        {"dropdown_item": item} for item in reactive_removal_of_punitive_damages_dropdown
    ]
     #assign the front end
    mod_table.reactive_removal_of_punitive_damages.removal_of_punitive_damages.min = round(factor_min - 1,6)
    mod_table.reactive_removal_of_punitive_damages.removal_of_punitive_damages.max = round(factor_max - 1,6)
    mod_table.reactive_removal_of_punitive_damages.removal_of_punitive_damages.factor_selection.calculated = round(calculated_factor - 1, 6)      

    #validation message for selected factor    
    factor_validation(mod_table.reactive_removal_of_punitive_damages.removal_of_punitive_damages.min, 
    mod_table.reactive_removal_of_punitive_damages.removal_of_punitive_damages.max, 
    mod_table.reactive_removal_of_punitive_damages.removal_of_punitive_damages.factor_selection.selected, 
    "In PCL Inputs Sheet: Removal of Punitive Damages Modifier")

    #set up validation message on description dropdown as it is state dependent
    if description not in drop_down_descripton:
        hx.errors.validation("PCL Removal of Punitive damages descripton does not belong to the State Options")

    results["admitted_punitive_damages_factor"] = mod_table.reactive_removal_of_punitive_damages.removal_of_punitive_damages.factor_selection.selected + 1
    

def fetch_admitted_ne_deviation_factor(hxd, state_info, results):
    ne_shortcut = hxd.cds.modifiers.pcl.ne_deviation_factor
    ne_shortcut.min = constants.ne_deviation_min
    ne_shortcut.max = constants.ne_deviation_max
    ne_deviation_factor_credit_debit = ne_shortcut.credit_debit or 0

    # set the deviation factor to be used in the calculations
    if ne_deviation_factor_credit_debit == 0:
        ne_deviation_factor_pcl = 1
    else:    
        ne_deviation_factor_pcl = max(
            1 + constants.ne_deviation_min,  # min is -ve
            min(
                1 + constants.ne_deviation_max,
                1 + ne_deviation_factor_credit_debit or 0,
            ),
        )

    #a validation message for the rationale    
    if (ne_deviation_factor_credit_debit is not None and ne_deviation_factor_credit_debit !=0) and ne_shortcut.rationale is None:
        hx.errors.validation("Please provide a rationale for the NE Deviation in PCL Inputs" )

    #a min and max validation
    factor_validation(
        constants.ne_deviation_min,
        constants.ne_deviation_max,
        ne_deviation_factor_credit_debit,
        "In PCL Inputs Sheet: NE Deviation",
    )

    #a catch to return the ne_deviation_factor to 1 if the state changes from nebraska to something else
    if state_info["state_code"] != "NE":
        ne_deviation_factor_pcl = 1
        
    results["ne_deviation_factor_pcl"] = ne_deviation_factor_pcl


def fetch_surplus_deviation_factor(hxd, state_info, results):
    # extract the value of surplus deviation from the layers and add it to the results list
    surplus_deviation = hxd.cds.modifiers.pcl.surplus_deviation or 0
    surplus_deviation_factor_pcl = 1 + surplus_deviation if state_info["state_code"] == "Surplus" else 1
    results["surplus_deviation_factor_pcl"] = surplus_deviation_factor_pcl



def fetch_base_premium_ib(hxd, results):
    # we can switch the basis of the premium to be on assets or revenue.
    # there is no such switch on the calculations in admitted
    
    ib_assets_of_insured = hxd.cds.exposure.granular.pcl.base_rate.asset_size or 0
    ib_revenue_of_insured = hxd.cds.exposure.granular.pcl.base_rate.revenue or 0
    
    # SA: if statement on a constant condition?
    input_to_use = ib_assets_of_insured if constants.ib_basis == "Assets" else ib_revenue_of_insured
    df_res = look_up_with_bounds(input_to_use, "Lower", "Upper", ["BasePremium Assets", "BasePremium Revenue"], hx.params.table_pcl_base_rates_revenue)

    ib_base_premium_before_minimum = df_res["BasePremium Assets"] if constants.ib_basis == "Assets" else df_res["BasePremium Revenue"]

    results["ib_base_premium_before_minimum"] = ib_base_premium_before_minimum
    results["ib_base_premium_input_basis"] = input_to_use



def validate_inputs_generic_ib(hxd, table, string, root, results):
    mod_table = hxd.cds.modifiers.pcl.modifiers_table
    target_object = getattr(mod_table, root)
    input_selected = target_object.description
    input_value = target_object.factor_selection_nm

    input_to_use = input_value or constants.ib_non_admitted_default
    factor = (input_to_use or 0) + 1

    # set the min and max values outputs
    df_res = look_up(input_selected, "Admitted", ["Min", "Max"], table)
    min_val = round(df_res["Min"] - 1, 6)
    max_val = round(df_res["Max"] - 1, 6)

    # set out of range validation
    if input_value is not None:
        factor_validation(min_val, max_val, round(factor-1,8), "In PCL Inputs Sheet: " + string)

    setattr(target_object, "min_nm", min_val)
    setattr(target_object, "max_nm", max_val)
    results[f"{root}_factor"] = factor


def validate_inputs_subjective_modifiers_ib(hxd, results):
    mod_table = hxd.cds.modifiers.pcl.modifiers_table
    fin_con_table = hx.params.table_pcl_financial_conditions_non_admitted

    # FINANCIAL CONDITIONS
    #financial_conditions_factor = mod_table.financial_condition.factor_selection_nm or constants.ib_non_admitted_default or 1
    #adding input_value to have a condition that will only trigger the validation if it is not none
    input_value = mod_table.financial_condition.factor_selection_nm 
    financial_conditions_factor = mod_table.financial_condition.factor_selection_nm or constants.ib_non_admitted_default

    df_res = look_up(mod_table.financial_condition.description, "Admitted", ["Max", "Min"], fin_con_table)
    min_val = round(df_res["Min"] - 1, 6)
    max_val = round(df_res["Max"] - 1, 6)

    if input_value is not None:
        factor_validation(min_val, max_val, financial_conditions_factor, "In PCL Inputs Sheet: Non-Admitted Financial Conditions")

    mod_table.financial_condition.min_nm = min_val
    mod_table.financial_condition.max_nm = max_val
    results["financial_conditions_factor"] = financial_conditions_factor+1

    # PRIOR CLAIMS
    prior_claims_factor = 1 + (hxd.cds.modifiers.pcl.bnch_prior_claim_activity_selection.factor_selection or 0)

    min_val = constants.bnch_prior_min
    max_val = constants.bnch_prior_max

    factor_validation(min_val, max_val, prior_claims_factor-1, "In PCL Inputs Sheet: Prior Claim Activity")

    hxd.cds.modifiers.pcl.bnch_prior_claim_activity_selection.min = min_val
    hxd.cds.modifiers.pcl.bnch_prior_claim_activity_selection.max = max_val
    results["prior_claims_factor"] = prior_claims_factor


