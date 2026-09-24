import hx

def set_dropdowns(hxd, state_info):
    fid = hxd.cds.fid

    # Employee Exposure
    if state_info["requires_employee_exposure_definition"] == "TRUE":
        exposure_table = hx.params.table_employee_exposure_def
    else:
        exposure_table = hx.params.table_employee_exposure

    exposure_dropdown = exposure_table["Response"].values

    for plan in fid.base_premium.bp_plans:
        plan.reactive_employee_exposure.reactive_employee_exposure_dropdown = exposure_dropdown

    # Financial conditions
    if state_info["allows_declining_financial_condition_characteristic"] == "TRUE":
        response_vals = hx.params.table_financial_conditions_cw["Response"].values
        fid.plan_sponsor.reactive_financial_condition.reactive_financial_condition_dropdown = response_vals
        fid.benefit_plans.reactive_financial_condition_bp.reactive_financial_condition_bp_dropdown = response_vals
    else:
        response_vals = hx.params.table_financial_conditions_excep["Response"].values
        fid.plan_sponsor.reactive_financial_condition.reactive_financial_condition_dropdown = response_vals
        fid.benefit_plans.reactive_financial_condition_bp.reactive_financial_condition_bp_dropdown = response_vals

    # Layoff Downsizing Table
    if state_info["state_code"] == "AK":
        response_vals = hx.params.table_layoffs_downsizing_ak["Response"].values
        fid.plan_sponsor.reactive_layoffs_downsizing_spinoffs.reactive_layoffs_downsizing_spinoffs_dropdown = response_vals
    else:
        response_vals = hx.params.table_layoffs_downsizing_cw["Response"].values
        fid.plan_sponsor.reactive_layoffs_downsizing_spinoffs.reactive_layoffs_downsizing_spinoffs_dropdown = response_vals

    # Litigation
    if state_info["allows_plan_litigation_debit"] == "TRUE":
        response_vals = hx.params.table_litigation_cw["Response"].values
        fid.reactive_litigation.reactive_litigation_dropdown = response_vals
    else:
        response_vals = hx.params.table_litigation_excep["Response"].values
        fid.reactive_litigation.reactive_litigation_dropdown = response_vals


def shownby_conditions_fid(hxd, state_info):
    state_code = state_info["state_code"]
    # set out the conditional statements for the shownby tables in the view
    hxd.non_cds.is_state_ga = True if state_code == "GA" else False
    hxd.non_cds.is_state_ne = True if state_code == "NE" else False
    hxd.non_cds.is_state_oh = True if state_code == "OH" else False
    hxd.non_cds.is_surplus = True if state_code == "Surplus" else False
    is_per_occurrence_limit = False
    hxd.non_cds.is_fid_finished_rating = not(hxd.cds.package_information.finished_rating)

    #set the premium label
    if hxd.cds.standard_fields.is_admitted_or_surplus == "Surplus":
        hxd.non_cds.fid_premium_label = "Surplus Premium"
    else:
        hxd.non_cds.fid_premium_label = "Admitted Premium"
