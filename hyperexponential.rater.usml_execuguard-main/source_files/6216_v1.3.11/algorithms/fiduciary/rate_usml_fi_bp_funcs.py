import hx
from algorithms import rate_constants as constants
from algorithms.rate_utilities import input_validation, look_up, look_up_with_bounds

def validate_bp_inputs(plan, idx):
    validation_passed = True

    percent_of_active_participants_to_use = plan.percent_of_active_participants or 0

    if not input_validation(
        constants.active_particpants_factor_min,
        constants.active_particpants_factor_max,
        percent_of_active_participants_to_use,
        "% of Active Participants",
    ):
        validation_passed = False

    if not input_validation(
        constants.base_employee_min,
        constants.base_employee_max,
        plan.total_employees_or_members,
        "Total Employees or Members",
    ):
        validation_passed = False       

    # Add 1 to the idx because python indexes from 0
    if plan.assets_contributions is None:
        hx.errors.validation(
           f"The asset contribution in plan {idx + 1} has no value in Fiduciary Inputs"
        )
        validation_passed = False

    if plan.total_employees_or_members is None:
        hx.errors.validation(
            f"The total employees or members in plan {idx + 1} has no value in Fiduciary Inputs"
        )
        validation_passed = False

    return validation_passed


def calc_base_premium_assets(plan, results):
    # Calculate Base Premium
    assets_contribution = plan.assets_contributions or constants.assets_contributions_default
    df_vals = look_up_with_bounds(assets_contribution, "Min", "Max", ["Rate Running Total", "Min", "Rate per Employee in Band"], hx.params.table_fid_base_premium_assets)

    asset_underlying_premium = 0 if assets_contribution == 0 else df_vals["Rate Running Total"]
    assets_in_band = assets_contribution - df_vals["Min"]
    rate_in_band = df_vals["Rate per Employee in Band"]
    additional_rate_in_band = (assets_in_band / constants.base_premium_assets_division) * rate_in_band
    asset_contribution_base_premium = 0 if assets_contribution == 0 else asset_underlying_premium + additional_rate_in_band

    results.setdefault("assets_contributions", []).append(assets_contribution)
    results.setdefault("asset_contribution_base_premium", []).append(asset_contribution_base_premium)


def calc_employee_charges(plan, results, state_info):
    # Calculate Base Premium
    employee = plan.total_employees_or_members or constants.employees_default
    df_vals = look_up_with_bounds(employee, "Min", "Max", ["Rate Running Total", "Min", "Rate per Employee in Band"], hx.params.table_fid_base_premium_employees)

    employee_underlying_premium = 0 if employee == 0 else df_vals["Rate Running Total"]
    assets_in_band = employee - df_vals["Min"]
    rate_in_band = df_vals["Rate per Employee in Band"]
    additional_rate_in_band = assets_in_band * rate_in_band
    employee_charge_base_premium = 0 if employee == 0 else employee_underlying_premium + additional_rate_in_band

    # Calculate Charges
    if state_info["requires_employee_exposure_definition"] == "TRUE":
        exposure_table = hx.params.table_employee_exposure_def  
    else:
        exposure_table = hx.params.table_employee_exposure

    reactive_emp_exp = plan.reactive_employee_exposure.employee_exposure or ""
    exposure_emp_output = look_up(reactive_emp_exp, "Response", "Value", exposure_table, if_not_found=0)

    results.setdefault("total_employee_charge", []).append(employee)
    results.setdefault("employee_charge", []).append(employee_charge_base_premium * exposure_emp_output)


def fetch_particpants_factor(plan, results):
    input_to_use = plan.percent_of_active_participants or constants.active_particpants_factor_default

    active_particpants_factor = float(look_up_with_bounds(input_to_use, "Min", "Max", "Factor", hx.params.table_fid_active_participants))

    results.setdefault("active_particpants_factor", []).append(active_particpants_factor)



def calc_assets_base_rate(plan, results):
    # Determine the base rate for the assets
    input_to_use = plan.assets_contributions or constants.base_assets_default

    df_res = look_up_with_bounds(input_to_use, "Min", "Max", ["Rate Running", "Rate in Band per 1000", "Min"], hx.params.table_fid_base_assets)

    assets_underlying_premium = float(df_res["Rate Running"])
    assets_rate_in_band = float(df_res["Rate in Band per 1000"])
    assets_asset_in_band = float(df_res["Min"])

    assets_in_band = input_to_use - assets_asset_in_band
    additional_rate_in_band = (assets_in_band / constants.assets_base_rate_divider) * assets_rate_in_band
    assets_base_rate = 0 if input_to_use == 0 else assets_underlying_premium + additional_rate_in_band

    results.setdefault("assets_base_rate", []).append(assets_base_rate)


def calc_employee_base_rate(plan, results):
    # Determine the base rate for the assets
    input_to_use = plan.total_employees_or_members or constants.base_employee_default

    table = hx.params.table_fid_base_employee

    df_res = look_up_with_bounds(input_to_use, "Min", "Max", ["Rate Running", "Rate in Band per Employee", "Min"], hx.params.table_fid_base_employee)

    employee_underlying_premium = float(df_res["Rate Running"])
    employee_rate_in_band = float(df_res["Rate in Band per Employee"])
    employee_asset_in_band = float(df_res["Min"])

    assets_in_band = input_to_use - employee_asset_in_band
    additional_rate_in_band = assets_in_band * employee_rate_in_band
    employee_base_rate = 0 if input_to_use == 0 else employee_underlying_premium + additional_rate_in_band

    results.setdefault("employee_base_rate", []).append(employee_base_rate)


def calc_ib_base_premium(plan, hxd, results, plan_index):
    # this function brings together the values from several other functions to calculate the base premium for the internal benchmark
    active_particpants_factor = results.get("active_particpants_factor")[plan_index]
    assets_base_rate = results.get("assets_base_rate")[plan_index]
    employee_base_rate = results.get("employee_base_rate")[plan_index]

    employee_exposure_factor = results["employee_exposure_factor"]  # Not plan dependant

    plan_factor = look_up(plan.plan_type, "Response", "Value", hx.params.table_fid_plan_type)

    plan_base_premium = (
        (assets_base_rate + (employee_base_rate * employee_exposure_factor))
        * plan_factor
        * active_particpants_factor
    )

    results.setdefault("plan_base_premium_ib", []).append(plan_base_premium)


def other_plan_variables(plan, results):
    
    fiduciary_charge = (
        constants.fiduciary_charge_default if plan.additional_designated_fiduciaries is None 
        else plan.additional_designated_fiduciaries*constants.fiduciary_charge_multiplier 
    )
    results.setdefault("fiduciary_charge", []).append(fiduciary_charge)  # SA: looks like only the first one of these is used?
    results.setdefault("plan_type", []).append(plan.plan_type)