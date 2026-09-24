import hx
from algorithms import rate_constants as constants 
from algorithms.rate_utilities import look_up, look_up_with_bounds, factor_validation, input_validation, greater_than_validation, ratio_validation, agg_lim_calc
from math import prod

def validate_quote_inputs_all(options, results):
    """
    Pre-validates all quote inputs before the main loop.

    Returns:
        A tuple containing:
            - A list of indices of options that passed validation.
            - A boolean indicating if at least one option passed validation.
    """
    valid_option_indices = []
    overall_passed = False
    for i, option in enumerate(options):
        if validate_quote_inputs_single(option, results, i):
            valid_option_indices.append(i)
            overall_passed = True
    return valid_option_indices, overall_passed

def validate_quote_inputs_single(option, results, option_index):
    validation_passed = True  # Flag to track validation status     

    additional_defense_limit_to_use = option.adl_limit or constants.additional_defence_limit_value_default
    aggregate_to_use = option.aggregate_limit or constants.aggregate_limit_default

    if not greater_than_validation(
        additional_defense_limit_to_use,
        aggregate_to_use,
        "Aggregate limit",
        "Additional Defence Limit",
    ):
        validation_passed = False

    asset_contribution_to_use = constants.assets_contributions_default if results.get("assets_contributions") is None else results.get("assets_contributions")[0]
    retention_to_use = option.retention or constants.retention_fi_default
    if not ratio_validation(
        constants.retention_ratio_max,
        retention_to_use,
        asset_contribution_to_use,
        "Retention",
        "Asset Contribution"
    ):
        validation_passed = False

    voluntary_compliance_fees_and_defense_to_use = option.voluntary_compliance_fees_and_defense or constants.vcfdc_default

    if not input_validation(
        constants.vcfdc_min,
        constants.vcfdc_max,
        voluntary_compliance_fees_and_defense_to_use,
        "Voluntary Compliance Fees and Defense Costs",
    ):
        validation_passed = False
   
    if results.get("plan_type") is not None:
        one_esop_plan = "ESOP" in results.get("plan_type")
        esop_value = constants.esop_input if one_esop_plan else 0
        guidleine_retention = max(
            min(
                max(
                    (sum(results.get("assets_contributions")) / len(results.get("assets_contributions")))
                    / constants.retention_ib_divider,
                    constants.retention_ib_default_lower,
                ),
                constants.retention_ib_default_upper,
            ),
            esop_value,
        )
        if option.retention is not None:
            if not ratio_validation(
                999,
                option.retention,
                guidleine_retention,
                "FID Quoted Retention",
                "Guideline Retention",
                ):
                validation_passed = False    

    return validation_passed


def calc_limit_factor(option, hxd, results):
    # set the plan table
    if hxd.cds.fid.employer_type == "Single Employer":  
        plan_table = hx.params.table_fid_single_ilf
    else:
        plan_table = hx.params.table_fid_multi_ilf

    # Find the appropriate row based on the range
    if option.aggregate_limit == constants.aggregate_limit_max:
        aggregate_limit_row = look_up(option.aggregate_limit, "Limit Low", ["Limit Low", "Limit High", "Factor"], plan_table)
    else:
        aggregate_limit_row = look_up_with_bounds(option.aggregate_limit, "Limit Low", "Limit High", ["Limit Low", "Limit High", "Factor"], plan_table)

    # If validation passes, proceed with calculations
    low_limit = aggregate_limit_row["Limit Low"]
    high_limit = aggregate_limit_row["Limit High"]

    low_factor = aggregate_limit_row["Factor"]  # We find the low factor with the filters above
    high_factor = look_up(high_limit, "Limit Low", "Factor", plan_table)  # Get the next line up

    if option.aggregate_limit == constants.aggregate_limit_max:
        ratio_in_band = 1
    else:
        ratio_in_band = (option.aggregate_limit - low_limit) / (high_limit - low_limit)

    # this is the output of the limit function to be used later
    limit_factor = ratio_in_band * high_factor + (1 - ratio_in_band) * low_factor

    # Initialize the 'limit_factor' list within 'results' if it doesn't exist
    results.setdefault("limit_factor", []).append(limit_factor)


def calc_retention_factor(option, state_info, results):
    if state_info["state_code"] == "FL":
        retention_table = hx.params.table_fid_deductible_modifier_fl
        retention_ratio_max = 3  
    elif state_info["state_code"] == "ME":
        retention_table = hx.params.table_fid_deductible_modifier_me
        retention_ratio_max = 3
    else:
        retention_table = hx.params.table_fid_deductible_modifier_cw
        retention_ratio_max = 4

    # Get the corresponding asset contribution based on option_index
    # perform a validation check also as this value is a required field
    guidleine_retention = (
        constants.retention_multiplier
        * results.get("assets_contributions")[0]
        / constants.retention_divider
    )

    guideline_to_use = min(
        max(constants.default_retention, guidleine_retention), 
        constants.maximum_retention
    )

    if state_info["state_code"] == "FL" and option.retention / guideline_to_use > constants.florida_ratio:
        quoted_to_guideline_ratio = constants.florida_ratio
    else:
        quoted_to_guideline_ratio = option.retention / guideline_to_use

    if quoted_to_guideline_ratio >= retention_ratio_max:
        ratio_row = look_up(retention_ratio_max, "Ratio Low", ["Ratio Low", "Ratio High", "Factor"], retention_table)
    else:
        ratio_row = look_up_with_bounds(quoted_to_guideline_ratio, "Ratio Low", "Ratio High", ["Ratio Low", "Ratio High", "Factor"], retention_table)

    ratio_low = ratio_row["Ratio Low"]
    ratio_high = ratio_row["Ratio High"]
    ratio_band = (
        0
        if ratio_low == ratio_high
        else (quoted_to_guideline_ratio - ratio_low) / (ratio_high - ratio_low)
    )

    factor_low = ratio_row["Factor"]
    factor_high = look_up(ratio_high, "Ratio Low", "Factor", retention_table)
    retention_factor = ratio_band * factor_high + (1 - ratio_band) * factor_low

    results.setdefault("retention_factor", []).append(retention_factor)


def calc_limit_compression_factor(option, results):
    # Limit is greater than or equal to $5m and the limit is greater than or equal to the total plan assets
    criteria_1 = (
        option.aggregate_limit >= results.get("assets_contributions")[0]
        and option.aggregate_limit >= constants.limit_compression_value
    )
    # Limit is less than 5% of the total plan assets and the limit is less than or equal to $5m
    criteria_2 = (
        option.aggregate_limit
        < results.get("assets_contributions")[0] * constants.limit_compression_multiplier
        and option.aggregate_limit <= constants.limit_compression_value
    )
    limit_compression_factor = (
        constants.criteria_list_compression_factor if criteria_1 or criteria_2 else 1
    )

    results.setdefault("limit_compression_factor", []).append(limit_compression_factor)


def calc_additional_defence_limit_factor(option, results):
    adl = option.adl_limit or constants.additional_defence_limit_value_default

    per_of_aggregate = adl / option.aggregate_limit

    adl_table = hx.params.table_fid_adl

    if per_of_aggregate == 1:
        df_res = look_up(per_of_aggregate, "% of Aggregate Min", ["% of Aggregate Min", "% of Aggregate Max"], adl_table)
    else:
        df_res = look_up_with_bounds(per_of_aggregate, "% of Aggregate Min", "% of Aggregate Max", ["% of Aggregate Min", "% of Aggregate Max"], adl_table)

    per_low = df_res["% of Aggregate Min"]
    per_high = df_res["% of Aggregate Max"]
    ratio_band = (
        1
        if per_of_aggregate == 1
        else (per_of_aggregate - per_low) / (per_high - per_low)
    )

    factor_low = look_up(per_low, "% of Aggregate Min", "Factor", adl_table)
    factor_high = look_up(per_high, "% of Aggregate Min", "Factor", adl_table)

    additional_defence_limit_factor = (
        constants.additional_defence_limit_factor_default
        if adl == 0 or adl == None
        else (ratio_band * factor_high + (1 - ratio_band) * factor_low)
    )

    results.setdefault("additional_defence_limit_factor", []).append(additional_defence_limit_factor)

    # calculate the value for the modifier
    adl_modifier = option.adl_limit or 0
    adl_modifier_table = hx.params.table_fid_adl_modifier

    adl_ratio = adl_modifier / option.aggregate_limit
    
    adl_modifier_output = 1 + look_up_with_bounds(per_of_aggregate, "Lower", "Upper", "Factor", adl_modifier_table)

    results.setdefault("adl_modifier_output", []).append(adl_modifier_output)


# Voluntary Compliance Fees and Defense Costs
def calc_vcfdc_factor(option, state_info, results):
    input_value = option.voluntary_compliance_fees_and_defense
    sub_limit_to_use = input_value if input_value else constants.vcfdc_default

    vcfdc_table = hx.params.table_fid_vcfdc

    if sub_limit_to_use == constants.vcfdc_max:
        df_res = look_up(sub_limit_to_use, "Min", ["Min", "Max"], vcfdc_table)
    else:
        df_res = look_up_with_bounds(sub_limit_to_use, "Min", "Max", ["Min", "Max"], vcfdc_table)

    limit_low = df_res["Min"]
    limit_high = df_res["Max"]
    ratio_band = (
        1
        if sub_limit_to_use == constants.sub_limit_to_use_default
        else (sub_limit_to_use - limit_low) / (limit_high - limit_low)
    )

    factor_low = look_up(limit_low, "Min", "Charge", vcfdc_table)
    factor_high = look_up(limit_high, "Max", "Charge", vcfdc_table)
    vcfdc_factor = (
        ratio_band * factor_high + (1 - ratio_band) * factor_low
        if state_info["state_code"] == "OH"
        else 1
    )

    results.setdefault("vcfdc_factor", []).append(vcfdc_factor)



def calc_expense_factor(results, option_index, state_info):
    basic_expense_factor = state_info["allows_expense_rating"]

    base_premium_factor = (
        results.get("assets_contributions")
        + results.get("total_employee_charge")
        + results.get("fiduciary_charge")
    )
    florida_factor = (
        results.get("limit_factor")[option_index]
        + results.get("retention_factor")[option_index]
        if state_info["state_code"] == "FL"
        else 1
    )
    other_categories_product = (
        results.get("limit_factor")[option_index]
        * results.get("retention_factor")[option_index]
        * results.get("litigation_output")
        * results.get("plan_sponsor_product")
        * results.get("benefit_plan_product")
        * results.get("limit_compression_factor")[option_index]
        * results.get("additional_defence_limit_factor")[option_index]
        * results.get("foreign_charge_factor")
        * results.get("vcfdc_factor")[option_index]
        * results.get("ne_deviation_factor")
        * results.get("schedule_rating_factor")
    )

    if (
       state_info["state_code"] in ("NY", "NYFTZ")
       and
       base_premium_factor[option_index]*other_categories_product < constants.fiduciary_ny_value 
    ):
        requirement_ny = "No"
    else:
        requirement_ny ="Yes"    
    # create an output to be used in calculations
    if (
        results.get("expense_rating_input") == 0
        or not basic_expense_factor
        or (state_info["state_code"] in ("NY", "NYFTZ") and requirement_ny == "No")
    ):
        expense_factor = 1
    else:
        expense_factor = results.get("expense_rating_input")

    results.setdefault("expense_factor", []).append(expense_factor)


def fetch_surplus_factor(hxd, results, option_index):

    basic_surplus_value = hxd.cds.standard_fields.is_admitted_or_surplus

    surplus_input = results.get("limit_factor")[option_index]

    surplus_factor = surplus_input + 1 if basic_surplus_value == "Surplus" else 1

    results.setdefault("surplus_factor", []).append(surplus_factor)



# Gross Modelled Annual Premium gathers all the results from the functions and perfoms the final calculations
def calc_gross_modelled_annual_premium(hxd, option, state_info, results, option_index):
    # Create a dictionary to store the results
    gmap_results = {}
    # Note: subtract 1 from the option index as it references from 0

    # Add values from the results dictionary that are static but come from the layers list so are not pre calculated
    static_keys = [
        "ne_deviation_factor",
        "schedule_rating_factor",
        "expense_factor",
        "prior_acts_factor",
        "surplus_factor",
    ]
    for key in static_keys:
        value = results.get(key)
        if isinstance(value, list):
            gmap_results[key] = value[0]  # Take the first element if it's a list
        else:
            gmap_results[key] = value  # Otherwise, take the value directly

    # Add values from the results dictionary that come from the plan loop
    # we are taking only the first index from the plan as this copies the excel sheet
    results['fiduciary_values'] = []
    for i in range(len(results['asset_contribution_base_premium'])):
        assets = results['asset_contribution_base_premium'][i]
        charge = results['employee_charge'][i]
        fiduciary = results['fiduciary_charge'][i]
        results['fiduciary_values'].append((assets + charge) * fiduciary)

    plan_keys = [
        "asset_contribution_base_premium",
        "employee_charge",
        "fiduciary_values",
    ]
    for key in plan_keys:        
        gmap_results[key] = sum(results.get(key)) 

    # Add values from the results dictionary that come from the options loop
    option_keys = [
        "limit_factor",
        "retention_factor",
        "limit_compression_factor",
        "additional_defence_limit_factor",
        "vcfdc_factor",
    ]
    for key in option_keys:
        gmap_results[key] = results.get(key)[option_index]

    # Add values that are calculated or passed in
    gmap_results["florida_factor"] = (
        gmap_results["limit_factor"] + gmap_results["retention_factor"]
        if state_info["state_code"] == "FL"
        else 1
    )
    gmap_results["total_risk_characteristic_charge"] = (
        results.get("litigation_output")
        * results.get("plan_sponsor_product")
        * results.get("benefit_plan_product")
    )
    gmap_results["fcf"] = results.get("foreign_charge_factor")

    # Sum the values from the specified keys
    gmap_results["total_plan_charges"] = sum(
        gmap_results[key]
        for key in [
            "asset_contribution_base_premium",
            "employee_charge",
            "fiduciary_values",
        ]
    )    

    # there is no florida factor in the keys to multiply intentionally
    keys_to_multiply = [
        "limit_factor",
        "retention_factor",
        "limit_compression_factor",
        "additional_defence_limit_factor",
        "vcfdc_factor",
        "total_risk_characteristic_charge",
        "fcf",
        "schedule_rating_factor",
        "expense_factor"
    ]
    fl_keys_to_multiply = [
        "limit_compression_factor",
        "additional_defence_limit_factor",
        "vcfdc_factor",
        "florida_factor",
        "total_risk_characteristic_charge",
        "fcf",
        "schedule_rating_factor",
        "expense_factor"
    ]

    product_of_values = 1  # Initialize the product to 1
    if state_info["state_code"] == "FL":
        for key in fl_keys_to_multiply:
            product_of_values *= gmap_results[key]
        gmap_results["product_keys_to_multiply"] = product_of_values
    else:
        for key in keys_to_multiply:
            val = gmap_results[key]
            if isinstance(val, list):
                val = val[option_index]
            product_of_values *= val
        gmap_results["product_keys_to_multiply"] = product_of_values

    gmap_results["Model Annual Premium"] = (
        gmap_results["total_plan_charges"] * gmap_results["product_keys_to_multiply"]
    )

    results.setdefault("Model Annual Premium", []).append(
        gmap_results["Model Annual Premium"]
    )

    # set the value in the data schema
    option.admitted_premium = gmap_results["Model Annual Premium"]

    # set values back to the cds for running prem totals
    prem_sum = hxd.cds.layers[0].coverages.fid.running_prem_sum
    if hxd.cds.layers[0].coverages.fid.quote_grid.qg_options[option_index].option_selected == True:        
        prem_sum.base_rate.prem = gmap_results["total_plan_charges"]
        prem_sum.lim_adj.modifier = gmap_results["limit_factor"]
        prem_sum.lim_adj.prem  = gmap_results["limit_factor"] * prem_sum.base_rate.prem
        prem_sum.retention_adj.modifier = gmap_results["retention_factor"]
        prem_sum.retention_adj.prem  = gmap_results["retention_factor"] * prem_sum.lim_adj.prem
        prem_sum.fl_adj.modifier = gmap_results["florida_factor"]
        prem_sum.fl_adj.prem  = gmap_results["florida_factor"] * prem_sum.retention_adj.prem
        prem_sum.risk_char_adj.modifier = gmap_results["total_risk_characteristic_charge"]
        prem_sum.risk_char_adj.prem  = gmap_results["total_risk_characteristic_charge"] * prem_sum.fl_adj.prem
        prem_sum.lim_compression_adj.modifier = gmap_results["limit_compression_factor"]
        prem_sum.lim_compression_adj.prem  = gmap_results["limit_compression_factor"] * prem_sum.risk_char_adj.prem 
        prem_sum.adl_adj.modifier = gmap_results["additional_defence_limit_factor"]
        prem_sum.adl_adj.prem  = gmap_results["additional_defence_limit_factor"] * prem_sum.lim_compression_adj.prem
        prem_sum.fcf_adj.modifier = gmap_results["fcf"]
        prem_sum.fcf_adj.prem  = gmap_results["fcf"] * prem_sum.adl_adj.prem
        prem_sum.vcfdc_adj.modifier = gmap_results["vcfdc_factor"]
        prem_sum.vcfdc_adj.prem  = gmap_results["vcfdc_factor"] * prem_sum.fcf_adj.prem
        prem_sum.exp_fac_adj.modifier = gmap_results["expense_factor"]
        prem_sum.exp_fac_adj.prem  = gmap_results["expense_factor"] * prem_sum.vcfdc_adj.prem
        prem_sum.prior_acts_adj.modifier = gmap_results["prior_acts_factor"]
        prem_sum.prior_acts_adj.prem  = gmap_results["prior_acts_factor"] * prem_sum.exp_fac_adj.prem
        prem_sum.sch_rating_adj.modifier = gmap_results["schedule_rating_factor"]
        prem_sum.sch_rating_adj.prem  = gmap_results["schedule_rating_factor"] * prem_sum.prior_acts_adj.prem





            


    ########################################################################
    # NOTE: The below calculations don't go anywhere or get displayed anywhere. They were built to replicate requested
    # functionality from the Excel that also didn't go anywhere. As a result they're commented out

    # # calculate the rolling adjusted premium
    # gmap_results["base_premium"] = gmap_results["total_plan_charges"]
    # gmap_results["limit_adjusted_premium"] = (
    #     gmap_results["base_premium"] * gmap_results["limit_factor"]
    # )
    # gmap_results["retention_adjusted_premium"] = (
    #     gmap_results["limit_adjusted_premium"] * gmap_results["retention_factor"]
    # )
    # gmap_results["florida_adjusted_premium"] = (
    #     gmap_results["base_premium"] * gmap_results["florida_factor"]
    # )
    # gmap_results["risk_characteristic_adjusted_premium"] = (
    #     gmap_results["florida_adjusted_premium"]
    #     * gmap_results["total_risk_characteristic_charge"]
    #     if state_info["state_code"] == "FL"
    #     else (
    #         gmap_results["retention_adjusted_premium"]
    #         * gmap_results["total_risk_characteristic_charge"]
    #     )
    # )
    # gmap_results["limit_compression_adjusted_premium"] = (
    #     gmap_results["risk_characteristic_adjusted_premium"]
    #     * gmap_results["limit_compression_factor"]
    # )
    # gmap_results["additional_defence_limit_adjusted_premium"] = (
    #     gmap_results["limit_compression_adjusted_premium"]
    #     * gmap_results["additional_defence_limit_factor"]
    # )
    # gmap_results["foreign_charge_adjusted_premium"] = (
    #     gmap_results["additional_defence_limit_adjusted_premium"] * gmap_results["fcf"]
    # )
    # gmap_results["vcfcd_adjusted_premium"] = (
    #     gmap_results["foreign_charge_adjusted_premium"] * gmap_results["vcfdc_factor"]
    #     if state_info["state_code"] == "OH"
    #     else gmap_results["foreign_charge_adjusted_premium"]
    # )
    # gmap_results["ne_deviation_adjusted_premium"] = (
    #     gmap_results["vcfcd_adjusted_premium"] * gmap_results["ne_deviation_factor"]
    #     if state_info["state_code"] == "NE"
    #     else gmap_results["vcfcd_adjusted_premium"]
    # )

    # # set the criteria for the schedule rating
    # schedule_rating_criteria = gmap_results[
    #     "ne_deviation_adjusted_premium"
    # ] > results.get("min_premium_before")[0] and (
    #     gmap_results["ne_deviation_adjusted_premium"]
    #     * gmap_results["schedule_rating_factor"]
    #     > results.get("min_premium_after")[0]
    # )
    # # carry on with the rolling adjusted premium
    # gmap_results["schedule_rating_adjusted_premium"] = (
    #     gmap_results["ne_deviation_adjusted_premium"]
    #     * gmap_results["schedule_rating_factor"]
    #     if schedule_rating_criteria
    #     else gmap_results["ne_deviation_adjusted_premium"]
    # )
    # gmap_results["expense_adjusted_premium"] = (
    #     gmap_results["schedule_rating_adjusted_premium"]
    #     * gmap_results["expense_factor"]
    #     if state_info["allows_expense_rating"]
    #     else gmap_results["schedule_rating_adjusted_premium"]
    # )
    # gmap_results["prior_acts_adjusted_premium"] = (
    #     gmap_results["expense_adjusted_premium"] * gmap_results["prior_acts_factor"]
    # )
    # gmap_results["surplus_deviation_adjusted_premium"] = (
    #     gmap_results["expense_adjusted_premium"] * gmap_results["surplus_factor"]
    # )


def calc_limit_factor_ib(option, hxd, results, option_index):

    agg_eec_ratio = option.aggregate_limit / option.aggregate_limit

    ilf_table = hx.params.table_fid_ilfs

    ilf_table["Lookup"] = ilf_table["Lookup"].astype(str)

    # the look up values in this table is actually a concatination of two other values as a string
    f1_lookup_value = str(results.get("limit_from")[option_index]) + str(int(round(agg_eec_ratio, 0)))
    f2_lookup_value = str(results.get("limit_from")[option_index]) + str(int(round(agg_eec_ratio + 1, 0)))
    f3_lookup_value = str(results.get("limit_to")[option_index]) + str(int(round(agg_eec_ratio, 0)))
    f4_lookup_value = str(results.get("limit_to")[option_index]) + str(int(round(agg_eec_ratio + 1, 0)))
    column_to_use = "FIDEEAggMedILFs" if hxd.cds.fid.employer_type == "Single Employer" else "FIDEEAggHighILFs"

    f1 = look_up(f1_lookup_value, "Lookup", column_to_use, ilf_table)
    f2 = look_up(f2_lookup_value, "Lookup", column_to_use, ilf_table) 
    f3 = look_up(f3_lookup_value, "Lookup", column_to_use, ilf_table) 
    f4 = look_up(f4_lookup_value, "Lookup", column_to_use, ilf_table)

    alpha = results.get("alpha")[option_index]
    beta = results.get("beta")[option_index]

    limit_factor_ib = (
        f1 + alpha * (f3 - f1) + beta * (f2 - f1) + alpha * beta * (f4 + f1 - f2 - f3)
    )
    limit_factor_ib_to_use = limit_factor_ib if hxd.cds.layers[0].is_primary_excess == "Primary" else 1
    results.setdefault("limit_factor_ib", []).append(limit_factor_ib_to_use)

    
def calc_retention_factor_ib(option, results):

    quoted_retention = option.retention
    asset_contribution = results.get("assets_contributions")
    one_esop_plan = "ESOP" in results.get("plan_type")
    esop_value = constants.esop_input if one_esop_plan else 0
    guidleine_retention = max(
        min(
            max(
                (sum(asset_contribution) / len(asset_contribution))
                / constants.retention_ib_divider,
                constants.retention_ib_default_lower,
            ),
            constants.retention_ib_default_upper,
        ),
        esop_value,
    )
    ratio_of_quoted_to_guideline = quoted_retention / guidleine_retention

    input_to_use = ratio_of_quoted_to_guideline

    table = hx.params.table_fid_guideline_retention

    row_to_use = table[
        (table["Lower"] <= input_to_use) & (table["Upper"] > input_to_use)
    ].iloc[0]

    retention_ib = row_to_use["Factor"]
    results.setdefault("retention_ib", []).append(retention_ib)

        # set the guideline retention to the results
    results.setdefault("guidleine_retention", []).append(guidleine_retention)

    #also set the minimum retention output field.  This is always static and for user reference
    option.miniumum_retention = 0
    #option.miniumum_retention = constants.default_retention


def calc_total_modifier_ib(results, option_index):
    total_modifier_ib = (
        results.get("financial_condition_sponsor")
        * results.get("merger_acquisition_activity")
        * results.get("financial_condition_plan")
        * results.get("outside_professionals")
        * results.get("prior_claim_output")
        * results.get("additional_risk_output")
        * results.get("prior_acts_modifier_output")
        * results.get("adl_modifier_output")[option_index]
    )

    results.setdefault("total_modifier_ib", []).append(total_modifier_ib)

def calc_subjective_modifier_ib(results, option_index):
    subjective_modifier_ib = (
        results.get("financial_condition_sponsor")
        * results.get("financial_condition_plan")
        * results.get("outside_professionals")
        * results.get("prior_claim_output")
        * results.get("additional_risk_output")
    )

    results.setdefault("subjective_modifier_ib", []).append(subjective_modifier_ib)


def calc_adjusted_model_premium_ib(option, hxd, results, option_index):

    base_premium_input = results.get(
        "plan_base_premium_ib"
    )  # take the sum of the first three values from excel model
    base_premium = 0

    for value in base_premium_input:
        base_premium += value

    adjusted_base_premium = base_premium * results.get("cob")

    total_modifier_ib = results.get("total_modifier_ib")[option_index]
    subjective_modifier_ib = results.get("subjective_modifier_ib")[option_index]
    limit_factor_ib = results.get("limit_factor_ib")[option_index]
    if hxd.cds.layers[0].is_primary_excess == "Primary":
        retention_ib = results.get("retention_ib")[option_index]
    else:
        retention_ib = 1

    model_premium = (
        adjusted_base_premium * total_modifier_ib * limit_factor_ib * retention_ib
    )
    london_brokerage = 0
    us_brokerage = 0 if hxd.cds.layers[0].brokerage == None else hxd.cds.layers[0].brokerage

    adjusted_model_premium = model_premium * (1 - london_brokerage) / (1 - us_brokerage)

    option.internal_benchmark = adjusted_model_premium
    option.internal_benchmark_pre_uw_adj = 0 if subjective_modifier_ib == 0 else adjusted_model_premium / subjective_modifier_ib

    results.setdefault("ib_model_premium", []).append(adjusted_model_premium)


def calc_bpi_percent(option, results, option_index):
    admitted_unrounded_premium = results.get("Model Annual Premium")[option_index]
    ib_model_premium = results.get("ib_model_premium")[option_index]

    bpi_percent = 0 if ib_model_premium == 0 else admitted_unrounded_premium / ib_model_premium

    option.bpi = bpi_percent  # Write to hxd


