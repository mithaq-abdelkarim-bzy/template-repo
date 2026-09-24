import hx
from algorithms.epl.rate_usml_epl_input_data import (
    fetch_admitted_mod,
    fetch_state_info,
    calc_sug_class_of_business,
    fetch_wage_and_hour_selection,
    fetch_client_coverage_selection,
    fetch_ahern_factors,
    fetch_partnership_factors,
    fetch_coinsurance_credit,
    fetch_prior_knowledge_factor,
    fetch_admitted_ne_deviation_factor,
    fetch_surplus_deviation,
    fetch_client_coverage_factor,
    validate_inputs_admitted_mod,
    validate_inputs_risk_characteristic,
    validate_inputs_third_party_liability,
    validate_inputs_punitive_damage_factor,
    validate_inputs_schedule_rating_factors,
    validate_inputs_subjective_motifiers
)
from algorithms.epl.rate_usml_epl_options_funcs import (
    validate_option_epl,
    calc_min_retention_and_validate,    
    calc_limit_factor,
    calc_deductible_factor,
    calc_employment_event_loss_factor,
    calc_additional_defense_loss_factor,
    calc_admitted_unrounded_premium,
    calc_ib_limit_factor,
    calc_guideline_retentions,
    calc_guideline_minimium_premium,
    calc_split_retention_factor,
    calc_ib_prem_and_bpi_pct
)
from algorithms.epl.rate_usml_epl_model_state import (
    set_dropdowns,
    shownby_conditions_epl
)
from algorithms.epl.rate_usml_epl_factor_calcs import (
    calc_schedule_rating_factor,
    calc_employee_split_totals,
    calc_total_state_factor,
    calc_base_rate_epl,
    calc_total_modifier,
    calc_base_rate_base_prem,
    calc_objective_modifier_ib,
    calc_subjective_modifer_ib
)
from algorithms.rate_utilities import look_up, set_labels_multiple_selections, rgetattr, validate_selected_coverage_options

from algorithms import rate_constants as constants
from algorithms.rate_utilities import validate_aggregate_retention


def rate_usml_epl_runner(hxd):
    results = {}
    layer = hxd.cds.layers[0] # One Layer Model
    options = layer.coverages.epl.quote_grid.qg_options
    admitted_mods = hxd.cds.modifiers.epl.admitted_modifiers

    state_info = fetch_state_info(hxd)

    # Set Class of Business
    naics_code = int(hxd.cds.industry.naics_code) or 0
    naics_industry_code = look_up(naics_code, "national_industry_code", "naics_industry_code", hx.params.table_naics_hierarchy, if_not_found=None)
    class_of_business = look_up(naics_industry_code, "NAICS Level III", "COB", hx.params.table_epl_cob_map, if_not_found=None)
    sug_class_of_business = calc_sug_class_of_business(hxd)
    admitted_mods.reactive_cob.class_of_business.description.calculated = class_of_business

    set_dropdowns(hxd, state_info)
    shownby_conditions_epl(hxd, state_info)

    validate_inputs_risk_characteristic(hxd, state_info, results)
    validate_inputs_admitted_mod(hxd, admitted_mods.financial_stability, "financial_stability_factor_epl", hx.params.table_financial_stability, "Financial Stability", results, "financial_stability",  allows_ranges=state_info["allows_ranges"], minus_one=True)
    validate_inputs_admitted_mod(hxd, admitted_mods.loss_prevention_and_mitigation, "loss_prevention_factor_epl", hx.params.table_loss_prevention, "Loss Prevention", results, "loss_prevention_and_mitigation", allows_ranges=state_info["allows_ranges"], minus_one=True)
    validate_inputs_admitted_mod(hxd, admitted_mods.employment_policies, "employement_policy_factor_epl", hx.params.table_employment_policies, "Employement Policy", results, "employment_policies", allows_ranges=state_info["allows_ranges"], minus_one=True)    
    validate_inputs_third_party_liability(hxd, state_info, results)
    validate_inputs_punitive_damage_factor(hxd, state_info, results)
    validate_inputs_schedule_rating_factors(hxd, state_info, results)
    
    validate_inputs_subjective_motifiers(hxd, "bnch_risk_characteristics", "UW Risk Characteristic", results, minus_one = True)
    validate_inputs_subjective_motifiers(hxd, "bnch_pro_claim_activity", "UW Prior Claim Activity", results, minus_one = True)
    validate_inputs_subjective_motifiers(hxd, "bnch_hr_policies", "UW HR Policy", results, minus_one = True)
    validate_inputs_subjective_motifiers(hxd, "bnch_turnover_ma_layoffs", "UW Turnover, M&A Activity, Layoffs", results, minus_one = True)
    validate_inputs_subjective_motifiers(hxd, "bnch_financial_strength", "UW Financial Strength", results, minus_one = True)
    validate_inputs_subjective_motifiers(hxd, "bnch_demographic", "UW Demogrphic", results, minus_one = True)

    fetch_admitted_mod(admitted_mods.reactive_cob.class_of_business, "class_of_business_factor_epl", hx.params.table_epl_cob, "Table", results)
    fetch_admitted_mod(admitted_mods.unionized_employees, "unionized_employees_factor_epl", hx.params.table_unionized_employee, "Response", results)
    fetch_admitted_mod(admitted_mods.stock_option_exposure, "stock_option_exposure_factor_epl", hx.params.table_stock_option_exp, "Response", results)
    fetch_wage_and_hour_selection(hxd, state_info, results)
    fetch_client_coverage_selection(hxd, state_info, results)
    fetch_ahern_factors(hxd, results)
    fetch_partnership_factors(hxd, state_info, results)
    fetch_coinsurance_credit(hxd, results)
    
    calc_schedule_rating_factor(hxd, state_info, results)
    calc_employee_split_totals(hxd, results)
    calc_total_state_factor(hxd, results)
    calc_base_rate_epl(hxd, results)
    
    # Calculate the first option's limit factor as it's used in the modifier below, will skip it in the first option
    # loop later to compensate
    calc_limit_factor(options[0], results)
    calc_total_modifier(hxd, state_info, results)

    # calculate the IB premium
    fetch_prior_knowledge_factor(hxd, state_info, results)
    fetch_admitted_ne_deviation_factor(hxd, state_info, results)
    fetch_surplus_deviation(hxd, state_info, results)
    fetch_client_coverage_factor(hxd, results)

    calc_base_rate_base_prem(hxd, results)
    calc_objective_modifier_ib(hxd, results)
    calc_subjective_modifer_ib(hxd, results)
    
    # Validate selected options
    validate_selected_coverage_options(hxd, options, "epl")

    #validate the aggregate limit and retention separately and outside of the loop
    ar_validation_passed, valid_option_indices = validate_aggregate_retention(
        options, 
        constants.aggregate_limit_epl_max,
        state_info.get("minimum_limit"),
        constants.retention_rate_epl_max,
        constants.retention_rate_epl_min,
        "EPL" )
        

    for new_idx, idx in enumerate(valid_option_indices):
        option = options[idx]


        validation_passed = validate_option_epl(option, hxd, idx)
        if not validation_passed or not ar_validation_passed:
            continue
       
        calc_limit_factor(option, results)
        calc_deductible_factor(option, results)
        calc_employment_event_loss_factor(option, results)
        calc_additional_defense_loss_factor(option, results)

        calc_admitted_unrounded_premium(hxd, option, results, new_idx)
        calc_ib_limit_factor(option, hxd, results)
        calc_guideline_retentions(option, hxd, results)
        calc_guideline_minimium_premium(option, hxd, results)
        calc_split_retention_factor(option, hxd, results, new_idx)

        # set min retention as used in validation
        calc_min_retention_and_validate(option, hxd, idx)


        if not option.option_selected:
            continue
     
        # calc_split_retention_factor(option, hxd, results, idx)
        calc_ib_prem_and_bpi_pct(option, hxd, results, new_idx)

        #set the retention to be displayed    
        layer = hxd.cds.layers[0]
        layer.coverages.epl.main_retention_selected = results.get("deductible_list_epl")[new_idx]       
        



