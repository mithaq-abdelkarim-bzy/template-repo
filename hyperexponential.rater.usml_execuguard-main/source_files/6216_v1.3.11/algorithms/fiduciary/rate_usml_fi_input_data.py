import hx
import datetime
from math import prod
from algorithms import rate_constants as constants 
from algorithms.rate_utilities import look_up, look_up_with_bounds, factor_validation

def fetch_state_info(hxd):
    # set the state code. 
    if hxd.cds.standard_fields.is_admitted_or_surplus == "Surplus":
        state_code = "Surplus"
    else: 
        state_code = look_up(hxd.cds.state, "State Name", "Abbreviation", hx.params.table_reference_state)

    # read all basic inputs once from the state table
    state_code_row = hx.params.table_admitted_applicabilities.loc[
        hx.params.table_admitted_applicabilities["State"] == state_code
    ].iloc[0]

    state_info = {
        "state_code": state_code,
        "foreign_charge_override": state_code_row["Foreign Territory Override?"],
        "requires_employee_exposure_definition": state_code_row["Employee Exposure Def Required?"],
        "allows_declining_financial_condition_characteristic": state_code_row["Allows Declining Financial Performance (Financial Condition)?"],
        "allows_plan_litigation_debit": state_code_row["Allows Plan Litigation Debit?"],
        "allows_expense_rating": state_code_row["Allows Expense Rating?"],
        "allows_adl": state_code_row["Allows ADL?"],
    }

    return state_info


def fetch_from_modifier_tables(hxd, state_info, results):
    # LITIGATION
    value_for_litigation = state_info["allows_plan_litigation_debit"]
    litigation_table = hx.params.table_litigation_cw if value_for_litigation == "TRUE" else hx.params.table_litigation_excep
 
    litigation_input = hxd.cds.fid.reactive_litigation.litigation.selection
    results["litigation_output"] = look_up(litigation_input, "Response", "Factor", litigation_table)    

    # PLAN SPONSOR
    declining_fin = state_info["allows_declining_financial_condition_characteristic"]
    financial_conditions_table = hx.params.table_financial_conditions_cw if declining_fin == "TRUE" else hx.params.table_financial_conditions_excep
    
    state_code = state_info["state_code"]
    layoffs_table = hx.params.table_layoffs_downsizing_ak if state_code == "AK" else hx.params.table_layoffs_downsizing_cw           

    plan_sponsor = hxd.cds.fid.plan_sponsor
    val_layoffs_downsizing_spinoffs=look_up(plan_sponsor.reactive_layoffs_downsizing_spinoffs.layoffs_downsizing_spinoffs.selection, "Response", "Factor", layoffs_table,"not found")
    if val_layoffs_downsizing_spinoffs == "not found":
        hx.errors.validation('In Fiduciary Inputs: Please reselect the Layoffs, Downsizing, or Spin-Offs')

    plan_sponsor_data = {
        "Industry Quality": look_up(plan_sponsor.industry_quality.selection, "Response", "Factor", hx.params.table_industry),  
        "Financial Condition": look_up(plan_sponsor.reactive_financial_condition.financial_condition.selection, "Response", "Factor", financial_conditions_table),
        "Merger Acquisition Activity": look_up(plan_sponsor.merger_acquisition_activity.selection, "Response", "Factor", hx.params.table_merger_acquisition),        
        "Layoffs, Downsiizng, or Spin-Offs": look_up(plan_sponsor.reactive_layoffs_downsizing_spinoffs.layoffs_downsizing_spinoffs.selection, "Response", "Factor", layoffs_table) ,
        "Type of Union": look_up(plan_sponsor.type_of_union.selection, "Response", "Factor", hx.params.table_type_of_union), 
    }
    results["plan_sponsor_product"] = prod([float(v or 1) for k, v in plan_sponsor_data.items()])

    # BENEFIT PLANS
    benefit_plans = hxd.cds.fid.benefit_plans
    benefit_plan_data = {
        "Funding Level": look_up(benefit_plans.funding_level.selection, "Response", "Factor", hx.params.table_funding_level),  
        "Investments/Expenses": look_up(benefit_plans.investments_expenses.selection, "Response", "Factor", hx.params.table_investment_expenses),
        "Asset Performance": look_up(benefit_plans.asset_performance.selection, "Response", "Factor", hx.params.table_asset_performance),
        "Benefits": look_up(benefit_plans.benefits.selection, "Response", "Factor", hx.params.table_benefits),
        "Outside Professionals": look_up(benefit_plans.outside_professionals.selection, "Response", "Factor", hx.params.table_outside_professionals),
    }
    results["benefit_plan_product"] = prod([float(v or 1) for k, v in benefit_plan_data.items()])
    
    # EMPLOYEE EXPOSURE
    employee_exp = state_info["requires_employee_exposure_definition"]
    employee_exposure_table = hx.params.table_fid_employee_exposure_def if employee_exp == "TRUE" else hx.params.table_fid_employee_exposure

    if hxd.cds.fid.base_premium.bp_plans[0].reactive_employee_exposure.employee_exposure is None:
        employee_exposure_to_use = employee_exposure_table["Response"][1]
    else:
        employee_exposure_to_use = hxd.cds.fid.base_premium.bp_plans[0].reactive_employee_exposure.employee_exposure

    employee_exposure_input = look_up(employee_exposure_to_use, "Response", "Global", employee_exposure_table)
    results["employee_exposure_factor"] = look_up(employee_exposure_input, "Response", "Value", hx.params.table_fid_employee_exposure_ib)


    # CLASS OF BUSINESS
    results["cob"] = look_up(hxd.cds.industry.class_of_business, "Occupation", "Rate", hx.params.table_fid_industry_factors)

    # AGG LIMIT
    table_fid_admitted_applicabilities = hx.params.table_fid_admitted_applicabilities
    results["minimum_admitted_agg_limit"] = look_up(state_info["state_code"], "State", "Minimum Limit?", table_fid_admitted_applicabilities)


def validate_inputs_plan_sponsor_benefit_plans(hxd, state_info, results):
    """
    Validate the factor selection inputs for plan sponsor and benefit plans, and 
    display min and max values on the front end 
    """
    plan_sponsor = hxd.cds.fid.plan_sponsor
    benefit_plans = hxd.cds.fid.benefit_plans

    declining_fin = state_info["allows_declining_financial_condition_characteristic"]
    financial_conditions_table = hx.params.table_financial_conditions_cw if declining_fin == "TRUE" else hx.params.table_financial_conditions_excep

    # FINANCIAL CONDITION
    financial_condition_factor_selection = (plan_sponsor.reactive_financial_condition.financial_condition.factor_selection or 0) + 1
    
    column = "Global" if declining_fin == "TRUE" else "Response"
    fc_sponsor = look_up(plan_sponsor.reactive_financial_condition.financial_condition.selection, "Response", column, financial_conditions_table)
    fc_limits = look_up(fc_sponsor, "Response", ["Min", "Max"], hx.params.table_fid_financial_conditions)
    factor_validation(fc_limits["Min"],fc_limits["Max"],financial_condition_factor_selection,"In Fid Inputs Sheet: Finacial Condition")

    plan_sponsor.reactive_financial_condition.financial_condition.min = fc_limits["Min"] - 1
    plan_sponsor.reactive_financial_condition.financial_condition.max = fc_limits["Max"] - 1
    results["financial_condition_sponsor"] = financial_condition_factor_selection

    # MERGERS AND AQUISITIONS
    merger_acquisition_activity_factor_selection = (plan_sponsor.merger_acquisition_activity.factor_selection or 0) + 1
    
    ma_activity = look_up(plan_sponsor.merger_acquisition_activity.selection, "Response", "Global", hx.params.table_merger_acquisition)
    ma_limits = look_up(ma_activity, "Response", ["Min", "Max"], hx.params.table_fid_merger_acquisitions)
    factor_validation(ma_limits["Min"],ma_limits["Max"],merger_acquisition_activity_factor_selection,"In Fid Inputs Sheet: Merger Acquisition")
    
    plan_sponsor.merger_acquisition_activity.min = ma_limits["Min"] - 1
    plan_sponsor.merger_acquisition_activity.max = ma_limits["Max"] - 1
    results["merger_acquisition_activity"] = merger_acquisition_activity_factor_selection

    # FINANCIAL CONDITION BENEFIT PLAN
    financial_condition_bp_factor_selection = (benefit_plans.reactive_financial_condition_bp.financial_condition_bp.factor_selection or 0) + 1
    
    column = "Global" if declining_fin == "TRUE" else "Response"
    fc_plan = look_up(benefit_plans.reactive_financial_condition_bp.financial_condition_bp.selection, "Response", column, financial_conditions_table)
    bp_limits = look_up(fc_plan, "Response", ["Min", "Max"], hx.params.table_fid_financial_conditions)
    factor_validation(bp_limits["Min"],bp_limits["Max"],financial_condition_bp_factor_selection,"In Fid Inputs Sheet: Benefit Plan Financial Condition")

    benefit_plans.reactive_financial_condition_bp.financial_condition_bp.min = bp_limits["Min"] - 1
    benefit_plans.reactive_financial_condition_bp.financial_condition_bp.max = bp_limits["Max"] - 1
    results["financial_condition_plan"] = financial_condition_bp_factor_selection

    # OUTSIDE PROFESSIONALS
    outside_professionals_factor_selection = (benefit_plans.outside_professionals.factor_selection or 0) + 1
    
    op_limits = look_up(benefit_plans.outside_professionals.selection, "Response", ["Min", "Max"], hx.params.table_fid_outside_professionals)
    factor_validation(round(op_limits["Min"], 4),round(op_limits["Max"], 4),outside_professionals_factor_selection,"In Fid Inputs Sheet: Outside Professionals",)
    benefit_plans.outside_professionals.min = op_limits["Min"] - 1
    benefit_plans.outside_professionals.max = op_limits["Max"] - 1
    results["outside_professionals"] = outside_professionals_factor_selection

    
def validate_inputs_admitted_schedule(hxd, state_info, results):
    # setting the value based on the state for the admitted schedule Rating table
    # set the conditions
    table_fid_schedule_rating = hx.params.table_fid_schedule_rating
    table_fid_schedule_rating_2 = hx.params.table_fid_schedule_rating_2
    state_code = state_info["state_code"]

    asr = hxd.cds.layers[0].fid.admitted_schedule_rating

    cn_dict = {
        "sponsor": ("Sponsor", "factor_selection_sponsor"),
        "benefit_plan": ("Benefit Plans", "admitted_benefit"),
        "litigation": ("Litigation", "admitted_litigation"),
        "other": ("Other", "admitted_other"),
        "expense_factor": ("Expense Factor", "admitted_expense")
    }

    valid_states = {"CA","HI","NE","NY","NYFTZ","LA", "GA"}

    if state_code not in valid_states:
        state_code = "Other"

    error_trigger = False

    #Set Expense Factor to None if not GA

    for cn in cn_dict:
        key_lookup, key_results = cn_dict[cn]
        factor_selection = getattr(asr.factor_selection, cn) or 0
        admitted_range = -1 * look_up(key_lookup, "Characteristic", state_code, table_fid_schedule_rating_2)
        factor_validation(admitted_range, -admitted_range, factor_selection, "In Fid Inputs Sheet: Admitted Schedule - " + key_lookup)
        setattr(asr.min, cn, admitted_range)
        setattr(asr.max, cn, -admitted_range)
        results[key_results] = factor_selection

        if factor_selection and getattr(asr.rationale, cn) is None:
            if cn == "expense_factor" and state_code != "GA":   # expense factor only applicable for GA
                pass
            else:
                error_trigger = True

    if error_trigger:
        hx.errors.validation("Please provide the rationale for each corresponding factor selection made within the Admitted Schedule Rating Table on the FID sheet.")

def validate_inputs_expense_rating(hxd, state_info, results):
    expense_rating = hxd.cds.layers[0].fid.expense_rating
    if state_info["state_code"] == "GA":   #only applicable for GA
        expense_rating_factor_selection = expense_rating.factor_selection or 0
    else:
        expense_rating_factor_selection = 0

    if state_info["state_code"] == "NY" or state_info["state_code"] == "NYFTZ":
        expense_min = constants.ny_expense_min
        expense_max = constants.ny_expense_max
    elif state_info["allows_expense_rating"]:
        expense_min = constants.basic_expense_min
        expense_max = constants.basic_expense_max
    else:
        expense_min = constants.alt_expense_min
        expense_max = constants.alt_expense_max
    factor_validation(expense_min, expense_max, expense_rating_factor_selection + 1, "In Fid Inputs Sheet: Expense Rating")

    expense_rating.min = expense_min - 1
    expense_rating.max = expense_max - 1
    results["expense_rating_input"] = expense_rating_factor_selection + 1


def validate_inputs_foreign_charge(hxd, state_info, results):
    plans_shortcut = hxd.cds.fid.number_of_plans_outside_us
    number_of_plans_outside_us_factor_selection = plans_shortcut.factor_selection or 0

    number_of_plans = plans_shortcut.number_of_plans_outside_us or 0

    if state_info["foreign_charge_override"] == "TRUE":
        calculated_value = (
            min(
            constants.foreign_charge_output_min,
                    constants.foreign_charge_output_multiplier * number_of_plans,
                ) + 1
        )

        foreign_charge_output = calculated_value
        plans_shortcut.min = calculated_value - 1
        plans_shortcut.max = calculated_value - 1
    else:
        foreign_charge_output = number_of_plans_outside_us_factor_selection + 1
        plans_shortcut.min = constants.foreign_charge_min - 1
        plans_shortcut.max = constants.foreign_charge_max - 1
        
    # set the out of validation for the factor input
    factor_validation(
        round(plans_shortcut.min, 6) + 1,
        round(plans_shortcut.max, 6) + 1,
        number_of_plans_outside_us_factor_selection + 1,
        "In Fid Inputs Sheet: Foreign Charge"
    )

    
    results["foreign_charge_factor"] = foreign_charge_output


def validate_inputs_benchmark_deviation(hxd, state_info, results):
    layer = hxd.cds.layers[0]
    bench_uw_mod = layer.fid.benchmark_uw_modifiers
    ne_deviation_factor_credit_debit = layer.fid.ne_deviation_factor.credit_debit or 0

    # NE DEVIATION
    
    if ne_deviation_factor_credit_debit == 0:
        ne_deviation_factor = 1
    else:
        ne_deviation_factor = max(
            1 + constants.ne_deviation_min,
            min(
                1 + constants.ne_deviation_max,
                1 + ne_deviation_factor_credit_debit,
            ),
        )

    factor_validation(
        constants.ne_deviation_min,
        constants.ne_deviation_max,
        ne_deviation_factor_credit_debit,
        "In Fid Inputs Sheet: NE Deviation",
    )
    #a validation message for the rationale    
    if (ne_deviation_factor_credit_debit is not None and ne_deviation_factor_credit_debit !=0) and layer.fid.ne_deviation_factor.rationale is None:
        hx.errors.validation("Please provide a rationale for the NE Deviation in FID Inputs" )
    
    layer.fid.ne_deviation_factor.min = constants.ne_deviation_min
    layer.fid.ne_deviation_factor.max = constants.ne_deviation_max

    #a catch to return the ne_deviation_factor to 1 if the state changes from nebraska to something else
    if state_info["state_code"] != "NE":
        ne_deviation_factor = 1    

    results["ne_deviation_factor"] = ne_deviation_factor

    # PRIOR CLAIM ACTIVITY
    prior_claim_activity_factor_selection = bench_uw_mod.prior_claim_activity.factor_selection or 0

    factor_validation(
        constants.prior_claim_activity_min - 1,
        constants.prior_claim_activity_max - 1,
        prior_claim_activity_factor_selection,
        "In Fid Inputs Sheet: Benchmark- PRIOR CLAIM ACTIVITY",
    )
    
    bench_uw_mod.prior_claim_activity.min = constants.prior_claim_activity_min - 1
    bench_uw_mod.prior_claim_activity.max = constants.prior_claim_activity_max - 1
    results["prior_claim_output"] = (prior_claim_activity_factor_selection or 0) + 1

    # ADDITIONAL RISK CHARACTERISTICS
    additional_risk_characteristics_factor_selection = bench_uw_mod.additional_risk_characteristics.factor_selection or 0

    factor_validation(
        constants.additional_risk_characteristics_min - 1,
        constants.additional_risk_characteristics_max - 1,
        additional_risk_characteristics_factor_selection,
        "In Fid Inputs Sheet: Benchmark- ADDITIONAL RISK CHARACTERISTICS",
    )

    bench_uw_mod.additional_risk_characteristics.min = constants.additional_risk_characteristics_min - 1
    bench_uw_mod.additional_risk_characteristics.max = constants.additional_risk_characteristics_max - 1
    results["additional_risk_output"] = (additional_risk_characteristics_factor_selection or 0) + 1



def fetch_surplus_deviation(hxd, state_info, results):
    layer = hxd.cds.layers[0]

    # extract the value of surplus deviation from the layers and add it to the results list
    surplus_deviation = layer.fid.surplus_deviation or 0
    surplus_deviation_factor_fid = 1 + surplus_deviation if state_info["state_code"] == "Surplus" else 1

    results["surplus_deviation"] = surplus_deviation_factor_fid


def fetch_prior_acts_factor(hxd, state_info, results):
    retroactive_date = hxd.cds.state_requirements.retroactive_date
    
    if state_info["state_code"] == 'NY' and retroactive_date in ['TBD', "Policy Inception"]:
        if retroactive_date == "TBD":
            today = datetime.date.today()  
            retroactive_date_to_use = today
        else:
            retroactive_date_to_use = hxd.hx_core.inception_date 

        inception_date = hxd.hx_core.inception_date

        #find the retro calcs
        retro_year = retroactive_date_to_use.year    
        retro_start_date_of_year = datetime.date(retro_year, 1, 1)
        retro_date_day_in_the_year = (retroactive_date_to_use - retro_start_date_of_year).days + 1

        #find the inception calcs
        inception_year = inception_date.year
        inception_month = inception_date.month 
        inception_day =  inception_date.day   
        inception_start_date_of_year = datetime.date(inception_year, 1, 1)
        inception_date_day_in_the_year = (inception_date - inception_start_date_of_year).days + 1

        #retro date anniversary
        comparison = -1 if inception_date_day_in_the_year < retro_date_day_in_the_year else 0
        year_to_use = inception_year + comparison
        month_to_use = retroactive_date_to_use.month
        day_to_use = retroactive_date_to_use.day
        retro_date_anniversary = datetime.date(year_to_use, month_to_use, day_to_use)

        day_subtraction = 1 if day_to_use > inception_day else 0
        months_between_anniversary_and_inception = (inception_year*12+inception_month) - (year_to_use*12 + month_to_use) - day_subtraction
        month_iversary = datetime.date(year_to_use, month_to_use + months_between_anniversary_and_inception, day_to_use)
        remaining_days = inception_date - month_iversary
        inception_date_check = month_iversary + remaining_days

        years = year_to_use - retro_year
        months = months_between_anniversary_and_inception
        days = remaining_days
        final_comparison = 1 if months>=6 else 0
        rounded_for_lookup_max_4 = min(final_comparison + years, 4)
        
        prior_acts_factor = look_up_with_bounds(rounded_for_lookup_max_4, "Claims Made Year Min", "Claims Made Year Max", "Factor", hx.params.table_fid_prior_acts)
    else:
        if retroactive_date in [None, "TBD", "Policy Inception"]:
            prior_acts_factor = 0.75
        else:
            prior_acts_factor = look_up(retroactive_date, "NonDates", "Factor", hx.params.table_retro_mapping)

    
    # create the variables for the IB calculation   

    if retroactive_date in [None, "TBD", "Policy Inception"]:
        prior_acts_modifier_output = 0.75
    else:
        prior_acts_modifier_output = 1 - look_up(retroactive_date, "RetroPeriod", "Credit", hx.params.table_retro_period)

    results["prior_acts_factor"] = prior_acts_factor
    results["prior_acts_modifier_output"] = prior_acts_modifier_output
