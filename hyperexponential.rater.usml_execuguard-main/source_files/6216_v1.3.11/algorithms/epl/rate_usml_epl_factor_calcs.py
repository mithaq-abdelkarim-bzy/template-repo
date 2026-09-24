import hx
import datetime
from math import prod
import numpy as np
from operator import itemgetter
from algorithms import rate_constants as constants 
from algorithms.rate_utilities import look_up, look_up_with_bounds, factor_validation, pd_df_from_hx_structure


def calc_schedule_rating_factor(hxd, state_info, results):
    adm = hxd.cds.modifiers.epl.admitted_schedule_rating

    other_list = ["prior_claim_activity", "turnover_rate", "financial_strength", "hr_policies", "demographic_metro"]
    both_list = ["management", "internal_controls", "cooperation", "experience", "staffing_turnover", "salary_structure"]

    df_res = look_up(state_info["state_code"], "State", ["Min Schedule Rating Modifier", "Max Schedule Rating Modifier", "Min Before Schedule Rating", "Min After Schedule Rating"], hx.params.table_epl_admitted_applicabilities)

    sch_rating_state_min = df_res["Min Schedule Rating Modifier"]
    sch_rating_state_max = df_res["Max Schedule Rating Modifier"]

    premium_before_eligibility = df_res["Min Before Schedule Rating"]
    premium_after_eligibility = df_res["Min After Schedule Rating"]

    # add up all the flex values
    other_total_flex = sum([getattr(adm.factor_selection, item) or 0 for item in other_list])
    both_total_flex = sum([getattr(adm.factor_selection, item) or 0 for item in both_list])

    # set the total based on the state
    if state_info["state_code"] == "CA":
        ca_factor_selection_value = (adm.factor_selection.stability or 0) + (adm.factor_selection.hr_policies or 0) + (adm.factor_selection.demographic_metro or 0)
        total_flex = both_total_flex + ca_factor_selection_value
    elif state_info["state_code"] == "IN":
        in_factor_selection_value = adm.factor_selection.demographic_metro or 0
        total_flex = both_total_flex + in_factor_selection_value
    else:
        total_flex = other_total_flex

    schedule_rating_output = 1 if total_flex == 0 else ( max(
        1 + sch_rating_state_min, min(total_flex + 1, sch_rating_state_max + 1)
    ))
    
    # subtract 1 from the values of the output to keep the factor selected consistent with the min and max
    adm.factor_selection.tot_sch_rat = schedule_rating_output - 1
    adm.min.tot_sch_rat = sch_rating_state_min
    adm.max.tot_sch_rat = sch_rating_state_max
    results["schedule_rating_factor_epl"] = schedule_rating_output
    results["premium_before_eligibility"] = premium_before_eligibility
    results["premium_after_eligibility"] = premium_after_eligibility
    for item in other_list:
        results[item] = 1 + (getattr(adm.factor_selection, item) or 0)
    for item in both_list:
        results[item] = 1 + (getattr(adm.factor_selection, item) or 0)



def calc_employee_split_totals(hxd, results):
    """
    This function calculates totals for different employee types: seasonal, independent contractors,
    temporary, and foreign.
    """
    # SA: Totally static lookup that could be a constant
    table_epl_empfact = hx.params.table_epl_empfact

    total_seasonal_employees = look_up("SE", "Emp Fact", "Part-Time", table_epl_empfact) * (hxd.cds.split.seasonal.head_count or 0)
    total_indep_contractor = look_up("IC", "Emp Fact", "Part-Time", table_epl_empfact) * (hxd.cds.split.independent_contractors.head_count or 0)
    total_temp_employees = look_up("TE", "Emp Fact", "Part-Time", table_epl_empfact) * (hxd.cds.split.temporary.head_count or 0)
    
    total_foreign_employees = (hxd.cds.split.foreign.head_count or 0) * 0.25

    employee_total = (
        total_seasonal_employees
        + total_indep_contractor
        + total_temp_employees
        + total_foreign_employees
    )

    results["employee_split_total_epl"] = employee_total



def calc_total_state_factor(hxd, results):
    employee_split_total = results.get("employee_split_total_epl")

    # Employee Count Weights distribution - FTEs
    
    states_df = pd_df_from_hx_structure(hxd.cds.us_states).fillna(0).drop("Total")

    state_risk_df = hx.params.table_epl_state_risk_level
    state_risk_df.index = state_risk_df["State"].str.replace(" - ", "_").str.replace(" ", "_").str.replace("-", "_")

    states_df = states_df.join(state_risk_df[["Risk Group"]])

    employee_factors_df = hx.params.table_epl_empfact
    ef_transposed_df = employee_factors_df[employee_factors_df["Emp Fact"].isin(["FT", "PT"])].set_index("Emp Fact")[["Part-Time"]].T

    states_df = states_df.reset_index()
    states_df = states_df.join(ef_transposed_df, how="cross")
    states_df = states_df.set_index("index")

    states_df["fte"] = states_df["fte"]*states_df["FT"] + states_df["pte"]*states_df["PT"]

    risk_totals_df = states_df.groupby("Risk Group").sum()

    risk_totals_df.loc["Average", "fte"] += employee_split_total

    # set the front end values
    ftes = risk_totals_df["fte"].to_dict()
    hxd.cds.weights.high.ftes = ftes["High"]
    hxd.cds.weights.above_average.ftes = ftes["Above Average"]
    hxd.cds.weights.moderate.ftes = ftes["Moderate"]
    hxd.cds.weights.average.ftes = ftes["Average"]
    hxd.cds.weights.below_average.ftes = ftes["Below Average"]

    total_state_factor_epl = sum([factor for key, factor in ftes.items()])
    hxd.cds.total_ftes = total_state_factor_epl
    results["total_state_factor_epl"] = total_state_factor_epl
    risk_totals_df["total_state_factor_epl"] = total_state_factor_epl

    state_groupings_df = hx.params.table_epl_state_groupings.set_index("Risk Profile")
    risk_totals_df = risk_totals_df.join(state_groupings_df) 

    # Calculate weighted risk amounts
    risk_totals_df["weighted_risk"] = (risk_totals_df["fte"]/risk_totals_df["total_state_factor_epl"]) * risk_totals_df["Risk Factor"]
    risk_totals_df["weighted_risk"] = risk_totals_df["weighted_risk"].replace([np.inf, -np.inf], np.nan).fillna(0)

    weighted_risks = risk_totals_df["weighted_risk"].to_dict()

    # Sum the weighted risk amounts
    total_weighted_risk = max(1, sum([factor for key, factor in weighted_risks.items()]))
    # set the front end
    hxd.cds.total_state_factor = total_weighted_risk
    hxd.cds.weights.high.weighted_risk = weighted_risks["High"]
    hxd.cds.weights.above_average.weighted_risk = weighted_risks["Above Average"]
    hxd.cds.weights.moderate.weighted_risk = weighted_risks["Moderate"]
    hxd.cds.weights.average.weighted_risk = weighted_risks["Average"]
    hxd.cds.weights.below_average.weighted_risk = weighted_risks["Below Average"]

    results["total_weighted_risk_factor_epl"] = total_weighted_risk
    results["states_df"] = states_df  # Store this to save processing later


def calc_base_rate_epl(hxd, results):
    # Calculates the base rate based on the number of employees
    num_employees = hxd.cds.total_ftes
    if num_employees is not None:
        table = hx.params.table_epl_base_premium
        row_to_use = table[(table["Min"] <= num_employees) & (table["Max"] > num_employees)].iloc[0]
        
        underlying_rate = row_to_use["Rate Running Total"]
        employee_in_band = num_employees - row_to_use["Min"]
        rate_in_band = row_to_use["Rate per Employee in Band"]
        add_rate_in_band = employee_in_band * rate_in_band
        base_rate_epl = add_rate_in_band + underlying_rate
    else:
        underlying_rate = 0
        employee_in_band = 0
        rate_in_band = 0
        add_rate_in_band = 0
        base_rate_epl = 0

    results["base_rate_epl"] = base_rate_epl


def calc_total_modifier(hxd, state_info, results):
    base_premium = results.get("base_rate_epl")
    limit_factor = results.get("limit_factor_epl")[0]  # Use just first option
    risk_characteristics = results.get("risk_characteristic_factor_epl")
    financial_stability = results.get("financial_stability_factor_epl")
    loss_prevention = results.get("loss_prevention_factor_epl")
    employement_policy = results.get("employement_policy_factor_epl")
    class_of_business = results.get("class_of_business_factor_epl")
    unnionized_employees = results.get("unionized_employees_factor_epl")
    stock_option_exposure = results.get("stock_option_exposure_factor_epl")
    punitive_damages = results.get("punitive_damage_factor_epl")
    third_party_liability = results.get("third_party_liability_factor_epl")
    wage_hour = results.get("wage_hour_factor_epl")
    client_coverage = results.get("client_coverage_factor_epl")
    ahern_charge = results.get("ahern_charge_factor_epl")
    ahern_surcharge = results.get("ahern_surcharge_factor_epl")
    partnership_agreement_defense_costs = results.get("partnership_agreement_defense_costs_factor_epl")
    wage_hour_minimum_premium = results.get("wage_hour_minimum_premium") # Use just first option

    total_modifier = (
        risk_characteristics
        * financial_stability
        * loss_prevention
        * employement_policy
        * class_of_business
        * unnionized_employees
        * stock_option_exposure
        * punitive_damages
        * third_party_liability
        * wage_hour
        * client_coverage
    )
    hxd.cds.modifiers.epl.total_admitted_modifier = total_modifier

    limit_adjusted_premium = base_premium * limit_factor

    group_abc_modifier = risk_characteristics * class_of_business * unnionized_employees
    group_d123_modifier = punitive_damages * third_party_liability * wage_hour

    if state_info["state_code"] == "CA":
        ahern_insurance = (
            max(
                limit_adjusted_premium * group_abc_modifier * group_d123_modifier,
                wage_hour_minimum_premium,
            )
            * client_coverage
            * (ahern_surcharge - 1)
            + ahern_charge
        )
    else:
        ahern_insurance = 0

    group_efgh_modifier = (
        stock_option_exposure
        * financial_stability
        * loss_prevention
        * employement_policy
    )

    results["total_modifier_epl"] = total_modifier
    results["group_abc_modifier"] = group_abc_modifier
    results["group_d123_modifier"] = group_d123_modifier
    results["ahern_insurance"] = ahern_insurance
    results["group_efgh_modifier"] = group_efgh_modifier


def calc_base_rate_base_prem(hxd, results):
    states_df = results["states_df"]
    totals = states_df.sum().to_dict()

    state_groupings_df = hx.params.table_epl_state_groupings.set_index("Risk Profile")
    states_df = states_df.merge(state_groupings_df, left_on="Risk Group", right_index=True) 

    total_risk_factor = (
        sum(states_df["fte"]*states_df["Risk Factor"]) / totals["fte"] if totals["fte"] else 0
    )

    state_groupings_df = hx.params.table_epl_state_groupings.set_index("Risk Profile")
    states_df = states_df.merge(state_groupings_df, left_on="Risk Group", right_index=True) 

    # Equivalency state
    insured_state = hxd.cds.state
    county = hxd.cds.county
    liberal_search = str(insured_state) + str(county)
    liberal_state = look_up(liberal_search, "Lookup", "Liberal", hx.params.table_epl_liberal_county, if_not_found="FALSE")

    states_df["is_insured_state"] = states_df.index == insured_state
    states_df["insured_state_is_liberal"] = liberal_state == "TRUE"

    table_epl_state_factor = hx.params.table_epl_state_factor[["State", "Liberal", "NonLiberal"]]
    table_epl_state_factor["State"] = table_epl_state_factor["State"].str.replace(" - ", "_").str.replace(" ", "_").str.replace("-", "_")
    table_epl_state_factor = table_epl_state_factor.set_index("State")
    
    states_df = states_df.join(table_epl_state_factor)

    use_liberal_weight = (states_df['is_insured_state']) & (states_df["insured_state_is_liberal"])
    states_df['equivalency_state'] = np.where(use_liberal_weight, states_df["Liberal"], states_df["NonLiberal"])

    total_state = sum(states_df["fte"].fillna(0)*states_df["equivalency_state"].fillna(0)) / totals["fte"] if totals["fte"] else 0
    results["total_state"] = total_state

    total_ftes = hxd.cds.total_ftes
    states_df["proportion"] = states_df["fte"] / total_ftes if total_ftes else 0

    state_fte = hxd.cds.us_states.California.fte or 0
    state_pte = hxd.cds.us_states.California.pte or 0

    # states_df["FT"] and ["PT"] are static columns, so this can be reduced
    ca_fte = state_fte*states_df["FT"].iloc[0] + state_pte*states_df["PT"].iloc[0] 

    ca_ftes_weight = ca_fte / total_ftes if total_ftes else 0
    non_ca_ftes_weight = (total_ftes - ca_fte) / total_ftes if total_ftes else 0

    if hxd.cds.industry.naics_code is not None:
        df_res = look_up(hxd.cds.industry.class_of_business, "BeazleyOcc", ["CAFactor", "NonCAFactor"], hx.params.table_epl_industry_factors)
        ca_ftes_cob_factor = df_res["CAFactor"]
        non_ca_ftes_cob_factor = df_res["NonCAFactor"]
    else:
        ca_ftes_cob_factor = 1
        non_ca_ftes_cob_factor = 1

    cob_factor = ca_ftes_weight * ca_ftes_cob_factor + non_ca_ftes_weight * non_ca_ftes_cob_factor 

    table_epl_base_premium = hx.params.table_epl_ib_base_premium
    df_res = look_up_with_bounds(total_ftes, "Lower", "Upper", ["Premium (25.6% load)", "Lower", "Charge (25.6% load)"], table_epl_base_premium)
    
    base_rate_underlying_rate = df_res["Premium (25.6% load)"]
    base_rate_emp_in_band = total_ftes - df_res["Lower"]
    base_rate_rate_in_band = df_res["Charge (25.6% load)"]
    base_rate_add_rate_in_band = base_rate_emp_in_band * base_rate_rate_in_band

    base_rate_base_prem = (base_rate_underlying_rate + base_rate_add_rate_in_band) * (total_state or 1) * (cob_factor or 1)
    
    results["ib_base_rate_base_premium"] = base_rate_base_prem
    results["states_df"] = states_df  # Again save to avoid recalculating later


def calc_objective_modifier_ib(hxd, results):
    prior_act_mod = hxd.cds.state_requirements.retroactive_date
    if prior_act_mod is None or prior_act_mod == "TBD":
        lookup_to_use = "Policy Inception"
    else:
        lookup_to_use = prior_act_mod
    prior_acts_modifier = 1 - look_up(lookup_to_use, "RetroPeriod", "Credit", hx.params.table_retro_period)

    uni_empl_conc = hxd.cds.modifiers.epl.admitted_modifiers.unionized_employees.description
    unionized_employee_concentration = look_up(uni_empl_conc, "Response", "Modifier", hx.params.table_unionized_employee)
    
    coinsurance = max(1 - (hxd.cds.modifiers.epl.per_self_ins.selection or 0), 0.85)

    total_objective_modifier = prior_acts_modifier * unionized_employee_concentration * coinsurance

    results["ib_objective_modifiers_epl"] = total_objective_modifier

def calculate_subjective_modifiers(hxd, uw_category, min, max, string):

    target_object = getattr(hxd.cds.modifiers.epl.benchmark_uw_modifiers, uw_category)

    input_to_use = (
        0 if target_object.factor_selection is None else target_object.factor_selection
    )

    subjective_modifier_output = 1 + input_to_use

    # set the front end values
    target_object.min = min
    target_object.max = max

    #factor_validation(min, max, input_to_use, string)

    return subjective_modifier_output


def calc_subjective_modifer_ib(hxd, results):
    #min and max values set in constants file
    risk_characteristics = calculate_subjective_modifiers(
        hxd, "bnch_risk_characteristics", constants.bnch_risk_characteristics_min, constants.bnch_risk_characteristics_max, "UW Risk Characteristic"
    )
    prior_claims_activity = calculate_subjective_modifiers(
        hxd, "bnch_pro_claim_activity", constants.bnch_pro_claim_activity_min, constants.bnch_pro_claim_activity_max, "UW Prior Claim Activity"
    )
    hr_policy = calculate_subjective_modifiers(
        hxd, "bnch_hr_policies", constants.bnch_hr_policies_min, constants.bnch_hr_policies_max, "UW HR Policy"
    )
    turnover_ma = calculate_subjective_modifiers(
        hxd, "bnch_turnover_ma_layoffs", constants.bnch_turnover_ma_layoffs_min, constants.bnch_turnover_ma_layoffs_max, "UW Turnover, M&A Activity, Layoffs"
    )
    financial_strength = calculate_subjective_modifiers(
        hxd, "bnch_financial_strength", constants.bnch_financial_strength_min, constants.bnch_financial_strength_max, "UW Financial Strength"
    )
    demographic = calculate_subjective_modifiers(
        hxd, "bnch_demographic", constants.bnch_demographic_min, constants.bnch_demographic_max, "UW Demogrphic"
    )

    #the subjective modifiers for the benchmark premium are different to the ones
    #for the admitted premium
    total_subjective_modifier = (
        risk_characteristics
        * prior_claims_activity
        * hr_policy
        * turnover_ma
        * financial_strength
        * demographic
    )

    results["ib_subjective_modifiers_epl"] = total_subjective_modifier

