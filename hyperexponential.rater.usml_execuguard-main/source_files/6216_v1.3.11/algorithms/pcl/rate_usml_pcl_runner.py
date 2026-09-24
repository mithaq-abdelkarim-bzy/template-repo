import hx
from algorithms.pcl.rate_usml_pcl_input_data import (
    validate_inputs_risk_characteristics,
    validate_inputs_generic_ib,
    validate_inputs_subjective_modifiers_ib,
    fetch_state_info,
    fetch_asset_and_retention_categories,
    fetch_admitted_cob_factor,
    fetch_admitted_punitive_damages_factor,
    fetch_admitted_ne_deviation_factor,
    fetch_surplus_deviation_factor,
    fetch_base_premium_ib,
    set_retention_value
)
from algorithms.pcl.rate_usml_pcl_options_funcs import (
    validate_option_pcl,
    validation_functions_pcl,    
    calc_admitted_retention_factor,
    calc_admitted_limit_factor,
    calc_combined_retention_and_limit_factor,
    calc_admitted_unrounded_premium,
    fetch_eec_info,
    calc_ilf_ib,
    calc_retention_factor_ib,
    calc_limit_retention_factor_ib,
    calc_model_premium_ib,
    calc_bpi_percent,
    calc_guideline_minimium_premium
)
from algorithms.pcl.rate_usml_pcl_model_state import (
    shownby_conditions_pcl
)
from algorithms.pcl.rate_usml_pcl_factor_calcs import (
    calc_admitted_total_risk_characteristics_factor,
    calc_modifiers_ib,
    calc_admitted_schedule_rating_factor
)
from algorithms.rate_utilities import validate_aggregate_retention, validate_selected_coverage_options, set_labels_multiple_selections, rgetattr
from algorithms import rate_constants as constants



def rate_usml_pcl_runner(hxd):
    results = {}

    # hardcoding a default label, in case the validation fails. Without this hardcoded, if it fails we would get an empty label
    hxd.non_cds.required_pcl_row_labels.option_selected = "Option Selected?"
    
    if validation_functions_pcl(hxd):
        return

    state_info = fetch_state_info(hxd)

    shownby_conditions_pcl(hxd, state_info)

    validate_inputs_risk_characteristics(hxd, results, state_info)

    layer = hxd.cds.layers[0]
    # call the functions that perform the non_loop_functions
    options = layer.coverages.pcl.quote_grid.qg_options
 
    ar_validation_passed, valid_option_indices = validate_aggregate_retention(
        options, 
        constants.aggregate_limit_pcl_max,
        state_info.get("minimum_limit"),
        constants.retention_pcl_max,
        constants.retention_pcl_min,
        "PCL" )

    #need to run this now just to extract the retention
    for new_idx, idx in enumerate(valid_option_indices):
        option = options[idx]
        validation_passed = validate_option_pcl(option, results, state_info)
        if not validation_passed or not ar_validation_passed:
            continue
        set_retention_value(option, results)   
        fetch_asset_and_retention_categories(hxd, state_info, results, new_idx)
    
    fetch_admitted_cob_factor(hxd, results)
    fetch_admitted_punitive_damages_factor(hxd, results, state_info)
    fetch_admitted_ne_deviation_factor(hxd, state_info, results)
    fetch_surplus_deviation_factor(hxd, state_info, results)

    calc_admitted_total_risk_characteristics_factor(hxd, results)
    calc_admitted_schedule_rating_factor(hxd, results, state_info)

    # calculate the IB premium
    validate_inputs_generic_ib(hxd, hx.params.table_pcl_ma_activity_non_admitted, "Non-Admitted Mergers and Acquisitions", "mergers_and_acquisition_activity", results)
    validate_inputs_generic_ib(hxd, hx.params.table_pcl_ownership_non_admitted, "Non-Admitted Ownership", "ownership", results)
    validate_inputs_generic_ib(hxd, hx.params.table_pcl_length_of_time_non_admitted, "Non-Admitted Length of Time", "length_of_time_in_business", results)
    validate_inputs_subjective_modifiers_ib(hxd, results)

    # Validate selected options
    validate_selected_coverage_options(hxd, options, "pcl")
    
    fetch_base_premium_ib(hxd, results)

    calc_modifiers_ib(hxd, results)

    hxd.cds.rating_factors.pcl.base_rate.admitted_minimum_premium = state_info.get("minimum_premium")
    hxd.cds.rating_factors.pcl.base_rate.admitted_minimum_limit = state_info.get("minimum_limit")

    

        
   #need to run this a second time for the main calculations
    for new_idx, idx in enumerate(valid_option_indices):
        option = options[idx]
        validation_passed = validate_option_pcl(option, results,state_info)
        if not validation_passed or not ar_validation_passed:
            continue

        # create the admitted premium
        calc_admitted_retention_factor(option, state_info, results,idx)
        calc_admitted_limit_factor(option, results)
        
        calc_combined_retention_and_limit_factor(option, state_info, results, new_idx)
        
        calc_admitted_unrounded_premium(hxd, option, state_info, results, new_idx)
          

        # create the Internal Benchmark (IB) premium
        #fetch_eec_info(option, results)
        #calc_ilf_ib(option, hxd, results, new_idx)
        #calc_retention_factor_ib(option, hxd, results, new_idx)
        
        calc_limit_retention_factor_ib(option, hxd, results, new_idx)
        calc_model_premium_ib(option, hxd,results, new_idx)
        calc_bpi_percent(option, results, new_idx)
        calc_guideline_minimium_premium(option, hxd, state_info)



