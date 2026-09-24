import hx
from algorithms import rate_constants as constants
from algorithms.rate_utilities import look_up, look_up_with_bounds, agg_lim_calc, factor_validation

def calc_admitted_total_risk_characteristics_factor(hxd, results):
    admitted_total_risk_characteristics_factor_pcl = (
        results.get("financial_condition_to_use")
        * results.get("profitability_to_use")
        * results.get("merger_acquisition_to_use")
        * results.get("layoffs_to_use")
        * results.get("litigation_to_use")
        * results.get("ownership_to_use")
        * results.get("time_in_business_to_use")
        * results.get("management_quality_to_use")
    )

    results["admitted_total_risk_characteristics_factor_pcl"] = admitted_total_risk_characteristics_factor_pcl


def calc_admitted_schedule_rating_factor(hxd, results, state_info):
    # because we need 4 different tables all of which need to be input tables and output tables  rather than just output tables
    # we cannot dynamically create them based on conditions and then set the values
    # the way round this is to create 4 tables and then hide them based on a condition

    table_name = state_info.get("schedule_rating_table")
    table = getattr(hx.params, f"table_pcl_schedule_rating_{table_name[-2:].lower()}")
    table["Reason"] = table["Reason"].str.lower().str.replace(" - ", "_of_").str.replace(" / ", "_").str.replace("/", "_").str.replace(" ", "_").str.replace("-", "")
    table["max"] = table["+/-"]
    table["min"] = table["max"] * -1
    col_dict = table[["Reason", "min", "max"]].set_index("Reason").to_dict(orient="index")

    # Sets all output nodes at this location at once using the dict. Input nodes aren't changed. Output nodes at this location
    # that aren't included in the dictionary would get overridden normally, but there aren't any present in this case. Have to
    # use setattr to avoid just redefining hxd_loc 
    setattr(hxd.cds.modifiers.pcl.schedule_rating, f"table_{table_name[-2:].lower()}", col_dict)

    hxd_loc = getattr(hxd.cds.modifiers.pcl.schedule_rating, f"table_{table_name[-2:].lower()}")    
    
    #There is an implicit 0 here in this generator expression if either of the conditions fail 
    # total_factors = sum(child[1].factor_selection.selected 
    # for child in hxd_loc 
    #                if child[1].factor_selection is not None 
    #                and child[1].factor_selection.selected is not None)
    total_factors = sum(child[1].factor_selection
    for child in hxd_loc 
                   if child[1].factor_selection is not None 
                   )

    skip_further_rationale_warnings = False
    for key, value in col_dict.items():
        # factor_selection = getattr(hxd_loc, key).factor_selection.selected
        factor_selection = getattr(hxd_loc, key).factor_selection
        factor_validation(value["min"], value["max"], factor_selection, "In PCL Inputs Sheet: " + key.title().replace("_", " "))

        if factor_selection and getattr(hxd_loc, key).rationale is None and not skip_further_rationale_warnings:
            hx.errors.validation("Please provide the rationale for each corresponding factor selection made within the Schedule Rating Table on the PCL sheet.")
            skip_further_rationale_warnings = True

    admitted_schedule_rating_min = state_info.get("schedule_rating_min")
    admitted_schedule_rating_max = state_info.get("schedule_rating_max")

    admitted_schedule_rating_factor = min(
        max(1 + total_factors, admitted_schedule_rating_min+1),
        admitted_schedule_rating_max+1,
    ) 

    # set the value in the front end
    hxd_loc.total_schedule_rating_modifier.min = admitted_schedule_rating_min
    hxd_loc.total_schedule_rating_modifier.max = admitted_schedule_rating_max
    hxd_loc.total_schedule_rating_modifier.factor_selection = admitted_schedule_rating_factor - 1

    results["admitted_schedule_rating_factor"] = admitted_schedule_rating_factor


def calc_modifiers_ib(hxd, results):
    
    #the standard function for look ups was defaulting this to zero.  Not sure why
    retroactive_data_table = hx.params.table_pcl_retro_period
    prior_acts_lookup = (
        0
        if hxd.cds.state_requirements.retroactive_date is None
        else (
            retroactive_data_table.loc[
                retroactive_data_table["RetroPeriod"]
                == hxd.cds.state_requirements.retroactive_date,
                "Credit",
            ].iloc[0]
        )
    )
    prior_acts = 1 - prior_acts_lookup
    #include a state factor
    state_factor = look_up(
        hxd.cds.state,
        "State",
        "Factor", 
        hx.params.table_pcl_state)
    #include a class of business factor
    class_of_business_factor = look_up(
        hxd.cds.industry.class_of_business,
        "BealeyOcc",
        "Factor",
        hx.params.table_pcl_occ)

    ib_objective_modifiers = (
        results.get("mergers_and_acquisition_activity_factor")
        * results.get("ownership_factor")
        * results.get("length_of_time_in_business_factor")
        * results.get("admitted_punitive_damages_factor")
        * prior_acts
        * state_factor
        * class_of_business_factor
    )

    results["ib_objective_modifiers"] = ib_objective_modifiers

    ib_subjective_modifiers = (
        results.get("financial_conditions_factor")
        * results.get("prior_claims_factor")
    )

    results["ib_subjective_modifiers"] = ib_subjective_modifiers   
