import hx

from algorithms.fiduciary.rate_usml_fi_input_data import (
    fetch_state_info, 
    fetch_from_modifier_tables, 
    validate_inputs_plan_sponsor_benefit_plans,
    validate_inputs_admitted_schedule,
    validate_inputs_foreign_charge, 
    validate_inputs_expense_rating,
    validate_inputs_benchmark_deviation,
    fetch_surplus_deviation,
    fetch_prior_acts_factor, 
)
from algorithms.fiduciary.rate_usml_fi_options_funcs import (
    agg_lim_calc,
    validate_quote_inputs_all, 
    #validate_quote_inputs,    
    calc_limit_factor, 
    calc_retention_factor, 
    calc_limit_compression_factor, 
    calc_additional_defence_limit_factor, 
    calc_vcfdc_factor, 
    calc_expense_factor, 
    fetch_surplus_factor,
    calc_limit_factor_ib, 
    calc_retention_factor_ib, 
    calc_total_modifier_ib,
    calc_subjective_modifier_ib,
    calc_adjusted_model_premium_ib, 
    calc_gross_modelled_annual_premium,
    calc_bpi_percent
)
from algorithms.fiduciary.rate_usml_fi_bp_funcs import (
    validate_bp_inputs,
    calc_base_premium_assets,
    calc_employee_charges,
    fetch_particpants_factor,
    calc_assets_base_rate,
    calc_employee_base_rate,
    calc_ib_base_premium,
    other_plan_variables
)
from algorithms.fiduciary.rate_usml_fi_model_state import (
    set_dropdowns,
    shownby_conditions_fid
)
from algorithms.fiduciary.rate_usml_fi_factor_calcs import (
    calc_schedule_rating_factor
)
from algorithms.rate_utilities import validate_aggregate_retention, validate_selected_coverage_options
from algorithms import rate_constants as constants


def rate_usml_fi_runner(hxd):
    # this is going to hold all the results from the functions so we can call it later
    results = {}

    # Fetch state info once as this will be referred back to often
    state_info = fetch_state_info(hxd)

    # Set Model State
    set_dropdowns(hxd, state_info)
    shownby_conditions_fid(hxd, state_info)

    #### Fetch several values before loops begin
    # These also validate the factor selection inputs and sets the min/max values to the front-end
    validate_inputs_plan_sponsor_benefit_plans(hxd, state_info, results)
    validate_inputs_admitted_schedule(hxd, state_info, results)
    validate_inputs_expense_rating(hxd, state_info, results)
    validate_inputs_foreign_charge(hxd, state_info, results)  
    validate_inputs_benchmark_deviation(hxd, state_info, results)   

    # No validation on these but still fetch now to avoid fetching in loops
    fetch_surplus_deviation(hxd, state_info, results)
    fetch_prior_acts_factor(hxd, state_info, results)
    
    # Extract values from litigation, plan sponsor, benefit plans, employee exposure, class of business and agg limit tables
    fetch_from_modifier_tables(hxd, state_info, results)

    calc_schedule_rating_factor(hxd, state_info, results)

    
    # Looping through bp plans as the number is expected to never be large
    bp_plans_list = hxd.cds.fid.base_premium.bp_plans
    all_validations_passed = True
    # First pass: Perform all validations and aggregate results
    for idx, plan in enumerate(bp_plans_list):
        validation_passed = validate_bp_inputs(plan, idx)
        all_validations_passed = all_validations_passed and validation_passed
    # Second pass: Proceed only if all validations passed in the first pass
    if all_validations_passed:
        for idx, plan in enumerate(bp_plans_list):     
            # if not validation_passed:
            #     continue  # Skip iteration
       
            calc_base_premium_assets(plan, results)
            calc_employee_charges(plan, results, state_info)
            fetch_particpants_factor(plan, results)
            calc_assets_base_rate(plan, results)
            calc_employee_base_rate(plan, results)
            
            calc_ib_base_premium(plan, hxd, results, idx)

            other_plan_variables(plan, results)

    layer = hxd.cds.layers[0] # One Layer Model
    
    # set the minimum aggreate limit
    layer.coverages.fid.minimum_admitted_agg_limit = results["minimum_admitted_agg_limit"]
    options = layer.coverages.fid.quote_grid.qg_options
    
    ar_validation_passed, aggregate_valid_indices = validate_aggregate_retention(
        options, 
        constants.aggregate_limit_max,
        constants.aggregate_limit_min,
        constants.maximum_retention,
        constants.retention_fid_min,
        "FID" )

    # Get valid indices from both validation functions:
    quote_valid_indices, _ = validate_quote_inputs_all(options, results)
    
    # Find the intersection of the valid indices:
    final_valid_indices = list(set(quote_valid_indices) & set(aggregate_valid_indices))
    
    if not final_valid_indices:
        hx.errors.validation("No FID option contains valid entries")
    else:

    
        for new_idx, idx in enumerate(final_valid_indices):
            option = options[idx]
            # validation_passed = validate_quote_inputs(option, results, idx)
            # if not validation_passed or not ar_validation_passed:
            #     continue   

            calc_limit_factor(option, hxd, results)
            calc_retention_factor(option, state_info, results)
            calc_limit_compression_factor(option, results)
            calc_additional_defence_limit_factor(option, results)
            calc_vcfdc_factor(option, state_info, results)
            
            calc_expense_factor(results, new_idx, state_info)
            fetch_surplus_factor(hxd, results, new_idx)
            calc_gross_modelled_annual_premium(hxd, option, state_info, results, new_idx)

            # NOTE: was noted in the excel that "alpha" pointed to EEC limit, but then both the 
            # EEC limit and aggregate limit pointed to the aggregate input in the spreadsheet
            # As a result, this calculation is identical for alpha or beta
            agg_lim_calc(option, results, "alpha", hx.params.table_fid_limit_lookup, "Lower", "Upper")
            agg_lim_calc(option, results, "beta", hx.params.table_fid_limit_lookup, "Lower", "Upper")
            agg_lim_calc(option, results, "eec_info", hx.params.table_fid_ilfs_ee, "EELimitFrom", "EELimitTo")

            calc_limit_factor_ib(option, hxd, results, new_idx)
            calc_retention_factor_ib(option, results)
            calc_total_modifier_ib(results, new_idx)
            calc_subjective_modifier_ib(results, new_idx)

            calc_adjusted_model_premium_ib(option, hxd, results, new_idx)
            calc_bpi_percent(option, results, new_idx)

        # Validate selected options
        validate_selected_coverage_options(hxd, options, "fiduciary")


    layer.coverages.fid.internal_guideline_retention = (
        None
        if results.get("guidleine_retention") is None
        else results.get("guidleine_retention")[0]
    )












