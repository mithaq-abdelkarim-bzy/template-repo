import hx
from algorithms import rate_constants as constants 
from algorithms.rate_utilities import look_up, look_up_with_bounds, factor_validation, input_validation, rgetattr


def calc_limit_factor(option, results):
    # Limit of Liability Factor
    # Calculates the limit factor based on the aggregate limit
    aggregate_lim = option.aggregate_limit

    if aggregate_lim is None:
        limit_factor_epl = 0
    else:
        table = hx.params.table_epl_ilf
        df_res = look_up_with_bounds(aggregate_lim, "Limit Low", "Limit High", ["Limit Low", "Limit High", "Factor"], table)
        
        limit_low = df_res["Limit Low"]
        limit_high = df_res["Limit High"]

        numerator = aggregate_lim - limit_low
        denominator = limit_high - limit_low
        ratio_in_band = numerator / denominator if denominator != 0 else 1

        factor_low = df_res["Factor"]
        factor_high = look_up(limit_high, "Limit Low", "Factor", table)
        
        limit_factor_epl = (
            ratio_in_band * factor_high + (1 - ratio_in_band) * factor_low
        )

    results.setdefault("limit_factor_epl", []).append(limit_factor_epl)

def validate_option_epl(option, hxd, idx):
    
    validation_passed = True

    # Total employees check
    total_employees = hxd.cds.us_states.Total.fte + hxd.cds.us_states.Total.pte
    if total_employees == 0:
        hx.errors.validation(
            f"There must be at least one employee in one state in either full time or part time"
        )
        validation_passed = False  

    return validation_passed

def calc_deductible_factor(option, results):
    # Calculates the guideline deductible based on the number of employees and aggregate limit
    num_employees = results.get("total_state_factor_epl")
    aggregate_limit = option.aggregate_limit
    pct = look_up_with_bounds(num_employees, "Employees Low", "Employees High", "Percentage", hx.params.table_epl_guideline_deductible)
    
    guideline_deductible = pct * (aggregate_limit or 0)

    deductible = option.retention or 0

    if guideline_deductible != 0:
        ratio_to_guideline = min(3, deductible / guideline_deductible)
    else:
        ratio_to_guideline = 3

    # Ratio Low and Ratio High 
    table = hx.params.table_epl_deductible_modifier
    row_to_use = table[
        (table["Ratio Low"] <= ratio_to_guideline)
        & (table["Ratio High"] >= ratio_to_guideline)
    ].iloc[-1]  # Don't use look_up helper because of iloc[-1]
    ratio_low = row_to_use["Ratio Low"] or 0
    ratio_high = row_to_use["Ratio High"] or 0

    # Ratio in Band 
    if ratio_low == 3:
        ratio_in_band = 1
    else:
        denominator = ratio_high - ratio_low
        if denominator != 0:
            ratio_in_band = (ratio_to_guideline - ratio_low) / denominator
        else:
            ratio_in_band = 0    
    
    if ratio_to_guideline < 0.1:
        deductible_factor = 1.4
    else:
        factor_low = look_up(ratio_low, "Ratio Low", "Modifier", table)
        factor_high = look_up(ratio_high, "Ratio Low", "Modifier", table)
        deductible_factor = ratio_in_band * factor_high + (1 - ratio_in_band) * factor_low

    results.setdefault("deductible_factor_epl", []).append(deductible_factor)
    results.setdefault("deductible_list_epl", []).append(deductible)   


def calc_employment_event_loss_factor(option, results):
    # Employment Event Loss
    # Calculate the employent event loss limit
    aggregate_limit = option.aggregate_limit
    event_loss_limit_input = option.event_loss_limit

    limit_multiplier = 0.005
    limit_default = limit_multiplier * (aggregate_limit or 0)
    event_loss_limit = (event_loss_limit_input or 0) + limit_default
    limit_above_default = max(event_loss_limit - limit_default, 0)
    ap = 0.05 * limit_above_default / 5000
    employment_event_loss_limit_output = ap + 1

    results.setdefault("employement_event_loss_factor_epl", []).append(employment_event_loss_limit_output)



def calc_additional_defense_loss_factor(option, results):
    additional_defense_limit = option.adl_limit
    aggregate_limit = option.aggregate_limit

    # % of Aggregate 
    if additional_defense_limit and aggregate_limit:
        pct_of_aggregate = additional_defense_limit / aggregate_limit
    else:
        pct_of_aggregate = 0

    table = hx.params.table_epl_adl
    row_to_use = look_up_with_bounds(pct_of_aggregate, "Low", "High", ["Low", "High"], table)
    
    add_per_low = row_to_use["Low"]
    add_per_high = 1 if pct_of_aggregate == 1 else row_to_use["High"]
 
    # Ratio 
    numerator = pct_of_aggregate - add_per_low
    denominator = add_per_high - add_per_low
    add_def_ratio = numerator / denominator if denominator else 1
  
    # Debits 
    add_def_debit_low = look_up(add_per_low, "Low", "Debit", table, if_not_found=0)
    add_def_debit_high = look_up(add_per_high, "Low", "Debit", table, if_not_found=0)
    
    additional_defence_limit_output = (
        add_def_ratio * add_def_debit_high + (1 - add_def_ratio) * add_def_debit_low
    ) + 1

    results.setdefault("additional_defence_loss_factor_epl", []).append(additional_defence_limit_output)


def calc_admitted_unrounded_premium(hxd, option, results, option_index):
    # find extract the factors
    #set a value for the limit factor index as this could be one bigger than the option index
    #This is becaue the limit factor index could be called twice on a different index
    if len(results["limit_factor_epl"]) > 0:
        limit_factor_index = option_index + 1    
    else:
        limit_factor_index = option_index 

    base_premium = results.get("base_rate_epl")
    limit_factor = results.get("limit_factor_epl")[limit_factor_index]    
    total_modifier = results.get("total_modifier_epl")
    group_abc_modifier = results.get("group_abc_modifier")
    group_d123_modifier = results.get("group_d123_modifier")
    ahern_insurance = results.get("ahern_insurance")
    wage_hour_minimum_premium = results.get("wage_hour_minimum_premium")
    partnership_agreement_defense_costs = results.get("partnership_agreement_defense_costs_factor_epl")
    group_efgh_modifier = results.get("group_efgh_modifier")
    client_coverage = results.get("client_coverage_factor_epl")
    state_grouping = results.get("total_weighted_risk_factor_epl")
    deductible_factor = results.get("deductible_factor_epl")[option_index]    
    coinsurance = results.get("coinsurance_factor_epl")
    employement_event_loss = results.get("employement_event_loss_factor_epl")[option_index]
    additional_defence_loss = results.get("additional_defence_loss_factor_epl")[option_index]    
    schedule_rating = results.get("schedule_rating_factor_epl")
    premium_before_eligibility = results.get("premium_before_eligibility")
    premium_after_eligibility = results.get("premium_after_eligibility")
    prior_knowledge = results.get("prior_knowledge_factor_epl")
    ne_deviation = results.get("ne_deviation_factor_epl")
    surplus_deviation = results.get("surplus_deviation_factor_epl")

    # adjust the premiums based on the factors
    limit_adj_premium = base_premium * limit_factor
    total_modifier_adjusted_premium = (
        (
            max(
                limit_adj_premium * group_abc_modifier * group_d123_modifier,
                wage_hour_minimum_premium,
            )
            * client_coverage
            + ahern_insurance
        )
        * partnership_agreement_defense_costs
        * group_efgh_modifier
    )

    state_adjusted_premium = total_modifier_adjusted_premium * state_grouping
    deductible_adjusted_premium = state_adjusted_premium * deductible_factor
    coinsurance_adjusted_premium = deductible_adjusted_premium * coinsurance
    employement_event_loss_adjusted_premium = coinsurance_adjusted_premium * employement_event_loss
    additional_defence_loss_adjusted_premium = employement_event_loss_adjusted_premium * additional_defence_loss

    if (additional_defence_loss_adjusted_premium < premium_before_eligibility
        or additional_defence_loss_adjusted_premium * schedule_rating < premium_after_eligibility):
        schedule_rating_factor = 1
    else:
        schedule_rating_factor = schedule_rating
 
    schedule_rating_adjusted_premium = additional_defence_loss_adjusted_premium * schedule_rating_factor
    prior_knowledge_adjusted_premium = schedule_rating_adjusted_premium * prior_knowledge
    ne_deviation_adjusted_premium = prior_knowledge_adjusted_premium * ne_deviation
    admitted_unrounded_premium_epl = ne_deviation_adjusted_premium * surplus_deviation

    option.admitted_premium = admitted_unrounded_premium_epl    

    results.setdefault("admitted_unrounded_premium_epl", []).append(admitted_unrounded_premium_epl)

    
    # set values back to the cds for running prem totals
    prem_sum = hxd.cds.layers[0].coverages.epl.running_prem_sum
    if hxd.cds.layers[0].coverages.epl.quote_grid.qg_options[option_index].option_selected == True:
        prem_sum.base_rate.prem = base_premium
        prem_sum.lim_adj.modifier = limit_factor
        prem_sum.lim_adj.prem = limit_factor * prem_sum.base_rate.prem
        prem_sum.modifier_adj.modifier = total_modifier_adjusted_premium / limit_adj_premium
        prem_sum.modifier_adj.prem = total_modifier_adjusted_premium
        prem_sum.state_adj.modifier = state_grouping
        prem_sum.state_adj.prem = state_adjusted_premium
        prem_sum.ded_adj.modifier = deductible_factor
        prem_sum.ded_adj.prem = deductible_adjusted_premium
        prem_sum.coinsurance_adj.modifier = coinsurance
        prem_sum.coinsurance_adj.prem = coinsurance_adjusted_premium
        prem_sum.employment_event_adj.modifier = employement_event_loss
        prem_sum.employment_event_adj.prem = employement_event_loss_adjusted_premium
        prem_sum.adl_adj.modifier = additional_defence_loss
        prem_sum.adl_adj.prem = additional_defence_loss_adjusted_premium
        prem_sum.sch_rating_adj.modifier = schedule_rating_factor
        prem_sum.sch_rating_adj.prem = schedule_rating_adjusted_premium
        prem_sum.prior_acts_adj.modifier = prior_knowledge
        prem_sum.prior_acts_adj.prem = prior_knowledge_adjusted_premium
        prem_sum.ne_deviation_adj.modifier = ne_deviation
        prem_sum.ne_deviation_adj.prem = ne_deviation_adjusted_premium
        prem_sum.surp_dev_adj.modifier = surplus_deviation
        prem_sum.surp_dev_adj.prem = admitted_unrounded_premium_epl

def calc_ib_limit_factor(option, hxd, results):
    per_occ_limit = option.aggregate_limit
    agg_lim = option.aggregate_limit
    is_primary_excess = hxd.cds.layers[0].is_primary_excess
    table_epl_ilf_mega = hx.params.table_epl_ilf_mega
    table_epl_limit_lookup = hx.params.table_epl_limit_lookup

    agg_ecc_ratio = 1

    row_to_use_mega = look_up_with_bounds(per_occ_limit, "EELimitFrom", "EELimitTo", ["EELimitFrom", "EELimitTo"], table_epl_ilf_mega)
    eec_low = row_to_use_mega["EELimitFrom"]
    eec_upper = row_to_use_mega["EELimitTo"]

    eec_upper = 30000000 if eec_upper == 35000000  else eec_upper

    L33_F1 = agg_ecc_ratio
    L34_F1 = int(eec_low)
    lookup_value = int(str(L34_F1) + str(L33_F1))
    lim_liab_f1 = look_up(lookup_value, "Lookup", "EPLFactor", table_epl_ilf_mega)

    L33_F2 = agg_ecc_ratio + 1
    L34_F2 = int(eec_low)
    lookup_value_f2 = int(str(L34_F2) + str(L33_F2))
    lim_liab_f2 = look_up(lookup_value_f2, "Lookup", "EPLFactor", table_epl_ilf_mega)

    L33_F3 = agg_ecc_ratio
    L35_F3 = int(eec_upper)
    lookup_value_f3 = int(str(L35_F3) + str(L33_F3))
    lim_liab_f3 = look_up(lookup_value_f3, "Lookup", "EPLFactor", table_epl_ilf_mega)

    L33_F4 = agg_ecc_ratio + 1
    L35_F4 = int(eec_upper)
    lookup_value_f4 = int(str(L35_F4) + str(L33_F4))
    lim_liab_f4 = look_up(lookup_value_f4, "Lookup", "EPLFactor", table_epl_ilf_mega)

    row_to_use_lookup = look_up_with_bounds(per_occ_limit, "Lower", "Upper", ["Lower", "Upper"], table_epl_limit_lookup)
    lim_liab_x0 = row_to_use_lookup["Lower"]
    lim_liab_x1 = row_to_use_lookup["Upper"]
    lim_liab_alpha = (per_occ_limit - lim_liab_x0) / (lim_liab_x1 - lim_liab_x0)

    # NOTE: This is identical to alpha but this matches Excel (agg_lim and per_occ_limit are equal)
    lim_liab_beta = (agg_lim - lim_liab_x0) / (lim_liab_x1 - lim_liab_x0)

    if is_primary_excess == "Primary":
        lim_liab_limit_factor = (
            lim_liab_f1
            + lim_liab_alpha * (lim_liab_f3 - lim_liab_f1)
            + lim_liab_beta * (lim_liab_f2 - lim_liab_f1)
            + lim_liab_alpha
            * lim_liab_beta
            * (lim_liab_f4 + lim_liab_f1 == lim_liab_f2 - lim_liab_f3)
        )
    else:
        lim_liab_limit_factor = 1

    results.setdefault("ib_limit_factor_epl", []).append(lim_liab_limit_factor)


def calc_guideline_retentions(option, hxd, results):
    class_of_business = hxd.cds.industry.class_of_business
    total_state = results.get("total_state")
    state = hxd.cds.state

    #adj_employee_count = results.get("total_state_factor_epl") + results.get("employee_split_total_epl")
    adj_employee_count = results.get("total_state_factor_epl") 

    db_version_id = 117  # Assuming this is a constant. If not, fetch it appropriately.
    ee_threshold_check = (adj_employee_count >= 500) and (class_of_business == "Staffing (excluding PEOs)")

    if class_of_business == "Professional Employer Organisation":
        state_group = look_up_with_bounds(total_state, "LowerState", "UpperState", "RetGroup", hx.params.table_epl_state_groups)
        adj_emp_band = look_up_with_bounds(adj_employee_count or 1, "Lower", "Upper", "Lower", hx.params.table_min_ret_peo)
        min_ret = look_up_with_bounds(adj_emp_band, "Lower", "Upper", state_group, hx.params.table_min_ret_peo_all)

    elif class_of_business == "Law Firm":
        state_group = look_up_with_bounds(total_state, "LowerState", "UpperState", "RetGroup", hx.params.table_epl_state_group_lawfirm)
        adj_emp_band = look_up_with_bounds(adj_employee_count or 1, "Lower", "Upper", "Lower", hx.params.table_min_ret_law)
        min_ret = look_up_with_bounds(adj_emp_band, "Lower", "Upper", state_group, hx.params.table_min_ret_law_all)

    elif class_of_business == "Staffing (excluding PEOs)": # and ee_threshold_check:
        if  not ee_threshold_check:
            min_ret = 0
        else:
            state_group = look_up_with_bounds(total_state, "LowerState", "UpperState", "RetGroup", hx.params.table_epl_state_groups)
            table = hx.params.table_min_ret_peo if db_version_id > 46 else hx.params.table_min_ret_staffing  # If statement but this is static
            adj_emp_band = look_up_with_bounds(adj_employee_count or 1, "Lower", "Upper", "Lower", table)
            min_ret = look_up_with_bounds(adj_emp_band, "Lower", "Upper", state_group, hx.params.table_min_ret_staffing_all)

    else:
        state_group = look_up_with_bounds(total_state, "LowerState", "UpperState", "RetGroup", hx.params.table_epl_state_groups)
        adj_emp_band = look_up_with_bounds(adj_employee_count or 1, "Lower", "Upper", "Lower", hx.params.table_min_ret_all_other_band)
        min_ret = look_up_with_bounds(adj_emp_band, "Lower", "Upper", state_group, hx.params.table_min_ret_all_other)

    group1_guide_retention = min_ret or 0

    cal_col = "CAMinRet" if hxd.cds.state == "California" else "NonCAMinRet"
    df_res = look_up(class_of_business, "BeazleyOcc", [cal_col, "LevelUp"], hx.params.table_epl_industry_factors, if_not_found=None)

    group2_guide_retention = df_res[cal_col]
    ret_level_check = df_res["LevelUp"]


    # Liberal/Non-Liberal Group
    #we need to first look up the underscore name as insured_state_is_liberal uses the underscore name
    state_underscore = look_up(hxd.cds.state,"State Name","Underscore", hx.params.table_state_underscore)
    liberal = results["states_df"]["insured_state_is_liberal"][state_underscore]
    if ret_level_check == 1:
        col = "StateGroupLiberal" if liberal == "TRUE" else "StateGroupNonLiberal"
        lib_group = look_up(hxd.cds.state, "State", "StateGroup", "StateGroupLiberal", hx.params.table_epl_state_factor)
        group3_guide_retention = look_up(adj_employee_count, "Lower", lib_group, hx.params.table_epl_min_ret_all_other)
    else:
        group3_guide_retention = 0


    guideline_retention = max(group1_guide_retention, group2_guide_retention, group3_guide_retention)

    option.guideline_retention = guideline_retention

    results.setdefault("guideline_retention_epl", []).append(guideline_retention)


def calc_guideline_minimium_premium(option,hxd, results):
    lower_eec = look_up_with_bounds(option.aggregate_limit, "EE Limit From", "EE Limit To", "EE Limit From", hx.params.table_epl_min_prem_limit_ee, if_not_found=500000)
    lower_agg = look_up_with_bounds(option.aggregate_limit, "Agg Limit From", "Agg Limit To", "Agg Limit From", hx.params.table_epl_min_prem_limit_agg, if_not_found=0) 
    state_group = look_up_with_bounds(results.get("total_state"), "LowerState", "UpperState", "RetGroup", hx.params.table_epl_state_groups)

    option.guideline_minimum_premium = look_up(f"{lower_eec}&{lower_agg}", "Lookup Value", state_group, hx.params.table_epl_min_prem_limit)


def calc_min_retention_and_validate(option, hxd, idx):
    ded_df = hx.params.table_epl_guideline_deductible
    num_employees = hxd.cds.total_ftes
    min_retention = ded_df[ded_df["Employees Low"]<=num_employees]["Min"].iloc[-1]    #-1 takes last record
    option.miniumum_retention = min_retention    

        # Check the retention is bigger than the min retention
    if (option.retention or 0) < (option.miniumum_retention or 0):
        hx.errors.validation(
            f"EPL: The retention is less than the minimum retention for option {idx + 1}"
        )

def calculate_ib_retention_factor(selected_retention, hxd, results, option_index):
    if hxd.cds.layers[0].is_primary_excess != "Primary":
        return 1

    guideline_retention = results.get("guideline_retention_epl")[option_index]

    # if the guideline retntion is less than 750000 (guideline_retention_min)
    if guideline_retention < constants.guideline_retention_min:
        df_res_lower = look_up_with_bounds(selected_retention, "Lower", "Upper", ["Lower", "Upper", str(guideline_retention)], hx.params.table_epl_deductible_factor_500k_lower)
        df_res_upper = look_up_with_bounds(selected_retention, "Lower", "Upper", ["Lower", "Upper", str(guideline_retention)], hx.params.table_epl_deductible_factor_500k_upper)

        lower_factor = df_res_lower[str(guideline_retention)]
        upper_factor = df_res_upper[str(guideline_retention)]
        band_lower = int(df_res_upper["Lower"])
        band_upper = int(df_res_upper["Upper"])
        #set a table to extract the upper and lower limits for validations
        table = hx.params.table_epl_deductible_factor_500k_upper
    else:
        ded_lower_factor = look_up_with_bounds(guideline_retention, "Lower Guideline", "Upper Guideline", "Lower Factor", hx.params.table_epl_deductible_table_to_use)

        if ded_lower_factor == "tblgEPL_DeductibleFactor500kLower":
            df_res_lower = look_up_with_bounds(selected_retention, "Lower", "Upper", ["Lower", "Upper", str(guideline_retention)], hx.params.table_epl_deductible_factor_500k_lower)
            df_res_upper = look_up_with_bounds(selected_retention, "Lower", "Upper", ["Lower", "Upper", str(guideline_retention)], hx.params.table_epl_deductible_factor_500k_upper)

            lower_factor = df_res_lower[str(guideline_retention)]
            upper_factor = df_res_upper[str(guideline_retention)]
            band_lower = int(df_res_upper["Lower"])
            band_upper = int(df_res_upper["Upper"])
        else:
            if ded_lower_factor == "tblgEPL_DeductibleFactor750k":
                table = hx.params.table_epl_deductible_factor_750k
            elif ded_lower_factor == "tblgEPL_DeductibleFactor1m":
                table = hx.params.table_epl_deductible_factor_1m
            elif ded_lower_factor == "tblgEPL_DeductibleFactor2m":
                table = hx.params.table_epl_deductible_factor_2m
            else:
                table = hx.params.table_epl_deductible_factor_5m

            df_res_lower = look_up_with_bounds(selected_retention, "Lower", "Upper", ["Lower", "Upper", "Factor Lower", "Factor Upper"], table)

            lower_factor = df_res_lower["Factor Lower"]
            upper_factor = df_res_lower["Factor Upper"]
            band_lower = df_res_lower["Lower"]
            band_upper = df_res_lower["Upper"]

    weight = (selected_retention - band_lower) / (band_upper - band_lower)
    
    #we need a dynamic validation for the retention split
    results.setdefault("minimum_split_retention", []).append(table['Lower'].min())
    results.setdefault("maximum_split_retention", []).append(table['Upper'].max())

    return weight * upper_factor + (1 - weight) * lower_factor



def calc_split_retention_factor(option, hxd, results, option_index):
    """Calculates the split retention factor adjustment for EPL coverage.

    Args:
        option: Current option being processed.
        hxd: Data object containing policy structure and exposures.
        results: Dictionary storing EPL calculation results.
        option_index: Index of the current option.

    Returns:
        None. Updates the 'results' dictionary with calculated values.
    """      

    # Extract relevant data
    states_df = results.get("states_df").reset_index()

    # Determine main retention
    main_retention_selected = results.get("deductible_list_epl")[option_index]
    main_retention_factor = calculate_ib_retention_factor(main_retention_selected, hxd, results, option_index)

    # Iterate through layers and calculate split retention factors
    layer = hxd.cds.layers[0]    

    # Define variables to hold cumulative sums
    weighted_factors = []
    proportions = []
    state_underscore_table = hx.params.table_state_underscore

    for i in range(1, 6):
        if not hxd.cds.modifiers.epl.bnch_split_retention_offered:
            weighted_factors.append(0)
            proportions.append(0)
            continue        

        state_to_use = getattr(layer.coverages.epl.state_split, f"state_split_{i}").state
        state = state_underscore_table.loc[state_underscore_table["State Name"] == state_to_use, "Underscore"].iloc[0] if state_to_use else None

        split_retention = getattr(layer.coverages.epl.state_split, f"state_split_{i}").retention
        split_retention_min = results.get("minimum_split_retention")[option_index] if results.get("minimum_split_retention") is not None else None
        split_retention_max = results.get("maximum_split_retention")[option_index] if results.get("maximum_split_retention") is not None else None

        #adding a validation error and stopping the rest of the function from running
        if (split_retention and split_retention_min and split_retention_max and (
            split_retention < split_retention_min or
            split_retention > split_retention_max
        )
        ):
            hx.errors.validation(f"Split Retention must be between {split_retention_min} and {split_retention_max}")                                    
            continue

        if split_retention and state:
            retention_factor = calculate_ib_retention_factor(split_retention, hxd, results, option_index)
            # Access and set the nested attribute
            setattr(getattr(layer.coverages.epl.state_split, f"state_split_{i}"), "retention_factor", retention_factor)

            proportion = look_up(state, "index", "proportion", states_df)
            setattr(getattr(layer.coverages.epl.state_split, f"state_split_{i}"), "proportion", proportion)

            weighted_factor = retention_factor * proportion
            setattr(getattr(layer.coverages.epl.state_split, f"state_split_{i}"), "weighted_factor", weighted_factor)

            weighted_factors.append(weighted_factor)
            proportions.append(proportion)
        else:
            # Set values to 0 if condition not met
            setattr(getattr(layer.coverages.epl.state_split, f"state_split_{i}"), "retention_factor", 0)
            setattr(getattr(layer.coverages.epl.state_split, f"state_split_{i}"), "proportion", 0)
            setattr(getattr(layer.coverages.epl.state_split, f"state_split_{i}"), "weighted_factor", 0)

            weighted_factors.append(0)
            proportions.append(0)


    # Calculate total state split factor
    propotion_sum = sum(proportions)
    weighted_sum = sum(weighted_factors)
    # sum_weighted_retention_factor = sum((getattr(layer.coverages.epl.state_split, f"state_split_{i}").retention_factor or 0) * weighted_factors[i - 1] for i in range(1, 6))
    sum_weighted_retention_factor = sum((getattr(layer.coverages.epl.state_split, f"state_split_{i}").retention_factor or 0)
                                    * (getattr(layer.coverages.epl.state_split, f"state_split_{i}").weighted_factor or 0) for i in range(1, 6))

    total_state_split_factor = 1 - weighted_sum + sum_weighted_retention_factor / main_retention_factor if propotion_sum > 0 else 1

    # Calculate other split factors
    other_split_1_shortcut = layer.coverages.epl.option_split.option_split_1
    other_split_2_shortcut = layer.coverages.epl.option_split.option_split_2
    other_split_1 = other_split_1_shortcut.retention_modifier
    other_split_2 = other_split_2_shortcut.retention_modifier
    other_split_factor_1 = 1 + (other_split_1 or 0)
    other_split_factor_2 = 1 + (other_split_2 or 0)
    total_other_split_factor = other_split_factor_1 * other_split_factor_2
    
    #other split detail
    other_split_1_shortcut.detail = "3 or more" if other_split_1_shortcut.basis_for_split == "Multi Plaintiff" else None
    other_split_2_shortcut.detail = "3 or more" if other_split_2_shortcut.basis_for_split == "Multi Plaintiff" else None

    # Calculate final split retention factor adjustment
    split_retention_factor_adjustment = total_state_split_factor * total_other_split_factor if hxd.cds.modifiers.epl.bnch_split_retention_offered else 1
    results.setdefault("split_retention_factor_adjustment_epl", []).append(split_retention_factor_adjustment)

def get_wage_hour_coverage_values(
    wage_hour_coverage,
    state,
    table_epl_wh_admitted_mapping_cafl,
    table_epl_wh_admitted_mapping,
    table_epl_wh_defense_sublimit,
):
    if wage_hour_coverage == "Not Purchased":
        return 0
    else:
        if state in ("California", "Florida"):
            table = table_epl_wh_admitted_mapping_cafl
        else:
            table = table_epl_wh_admitted_mapping

        #we need a catch for the scenario where a wage and hour selection is made and then the state is changed
        if wage_hour_coverage in table["Reponse"].values:
            row_to_use =  table.loc[table["Reponse"] == wage_hour_coverage].iloc[0]
            class_action_co_insurance = row_to_use['Coinsurance']
            defense_only_sub_limit  = row_to_use['Sublimit']

            lookup_column = "CAFactor" if state == "California" else "NonCAFactor"        
            wh_factor_temp = table_epl_wh_defense_sublimit.loc[table_epl_wh_defense_sublimit['WHDefenseSubLimit'] == defense_only_sub_limit, lookup_column].iloc[0]+1

            return wh_factor_temp
        else:
            return 1    

def calculate_wh_coverage_factor(hxd):   
     
    wh_factor_temp = get_wage_hour_coverage_values(
        hxd.cds.modifiers.epl.endorsements.selection.reactive_wage_and_hour.wage_and_hour,
        hxd.cds.state,
        hx.params.table_epl_wh_admitted_mapping_cafl,
        hx.params.table_epl_wh_admitted_mapping,
        hx.params.table_epl_wh_defense_sublimit,
    )
    wh_coverage_factor = (
        wh_factor_temp
        if hxd.cds.modifiers.epl.endorsements.selection.reactive_wage_and_hour.wage_and_hour != "Not Purchased"
        else 1
    )

    return wh_coverage_factor


def calc_ib_prem_and_bpi_pct(option, hxd, results, option_index):
    # ToDo: make sure the option functions have an option index filter
    ib_base_rate_base_premium = results.get("ib_base_rate_base_premium")
    ib_limit_factor = results.get("ib_limit_factor_epl")[option_index]
    ib_objective_modifiers = results.get("ib_objective_modifiers_epl")
    ib_subjective_modifiers = results.get("ib_subjective_modifiers_epl")
    client_coverage_factor = results.get("ib_client_coverage_factor_epl")
    split_retentions_factor = results.get("split_retention_factor_adjustment_epl")[option_index]
    admitted_unrounded_premium = results.get("admitted_unrounded_premium_epl")[option_index]
    adl_factor = 1  # this is hardcoded to 1 in the excel sheet
    #we need to set the brokerage before we use it
    us_brokerage = hxd.cds.layers[0].brokerage or 0
    ib_brokerage_factor = (1 - constants.london_brokerage) / (1 - us_brokerage)
    ib_retention_factor = calculate_ib_retention_factor(option.retention, hxd, results, option_index)
    wh_coverage_factor = calculate_wh_coverage_factor(hxd)

    ib_premium_before_ap = (
        ib_base_rate_base_premium
        * ib_brokerage_factor
        * ib_limit_factor
        * ib_retention_factor
        * ib_objective_modifiers
        * ib_subjective_modifiers
    )

    wh_coverage_ap = (wh_coverage_factor - 1) * ib_premium_before_ap
    client_coverage_ap = (client_coverage_factor - 1) * ib_premium_before_ap
    adl_ap = (adl_factor - 1) * ib_premium_before_ap
    split_retentions_ap = (split_retentions_factor - 1) * ib_premium_before_ap

    ib_model_premium = (
        ib_premium_before_ap
        + wh_coverage_ap
        + client_coverage_ap
        + adl_ap
        + split_retentions_ap
    )

    option.internal_benchmark = ib_model_premium
    option.internal_benchmark_pre_uw_adj = ib_model_premium / ib_subjective_modifiers
    option.bpi = None if ib_model_premium == 0 else admitted_unrounded_premium / ib_model_premium

    

