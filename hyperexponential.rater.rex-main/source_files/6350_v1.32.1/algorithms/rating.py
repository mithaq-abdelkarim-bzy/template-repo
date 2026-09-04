import hx
import json
import gc
import polars as pl
from algorithms.layers import layers_calc, map_layers_usd
from algorithms.populate_fields import populate_text, populate_dropdown, validation_error, populate_notifications, populate_info_boxes_text, validate_hurricane, initial_quoted_inputs, validation_run_schedule_rater_error
from algorithms.experience_rating import experience_rating
from algorithms.schedule import schedule_table_calc, read_schedule_table, map_tiv_usd, schedule_table_hxd_assignment, schedule_tiv_rater_calc, update_schedule_field_labels, get_currency_exchange, ind_occ_map
from algorithms.schedule_clean_state_county import schedule_table_hxd_assignment_state_county
from algorithms.state_county_rating_col_save import state_county_rating_col_save
from algorithms.policy_information import policy_information_mapping, generate_tags
from algorithms.fire.fire_rating import fire_rating_calc, fire_hxd_assignment, fire_occupancy_guide
from algorithms.fire.fire_summary import fire_analysis_summary
from algorithms.wildfire.wildfire_rating import wildfire_rating_calc, wildfire_hxd_assignment
from algorithms.wildfire.wildfire_summary import wildfire_analysis_summary
from algorithms.peril_agnostic.peril_rating_summaries import peril_rating_summary, peril_rating_assignment
from algorithms.windstorm.windstorm_rating import windstorm_us_rating_calc, windstorm_intl_rating_calc, windstorm_expected_loss_calc, windstorm_hxd_assignment
from algorithms.scs.hail_rating import hail_rating_calc, hail_hxd_assignment
from algorithms.scs.tornado_rating import tornado_rating_calc, tornado_hxd_assignment
from algorithms.scs.scs_summary import scs_analysis_summary
from algorithms.scs.scs_rating import scs_hxd_assignment
from algorithms.windstorm.windstorm_summary import windstorm_analysis_summary
from algorithms.earthquake.earthquake_rating import earthquake_us_rating_calc, earthquake_intl_rating_calc, earthquake_expected_loss_calc, earthquake_hxd_assignment
from algorithms.earthquake.earthquake_summary import earthquake_analysis_summary
from algorithms.flood.flood_rating import flood_us_rating_calc, flood_intl_rating_calc, flood_hxd_assignment
from algorithms.flood.flood_summary import flood_analysis_summary
from algorithms.bi_rating import bi_rating_calc
from algorithms.summary import total_expected_loss_summary, premium_summary, underwriter_adjustments, climate_metrics_calc, premium_summary_assignment, overall_analysis_summary, final_technical_premium_columns
from algorithms.data_assignment import data_assignment, create_country_state_summary
from algorithms.inflation import inflation
from algorithms.rating_common_functions import peril_covered_layer
from algorithms.cat_modelling import cat_method_calc, cat_method_expected_loss, cat_method_us_mi_tp_components, cat_method_hxd_assignment, drop_cat_method_columns
from algorithms.rate_change import rate_change_rater
from algorithms.quote_documents.quote_document_generation import quote_doc_rating_actions, quote_doc_rater_calc
from algorithms.tria import tria_calc
from algorithms.equipment_breakdown import equipment_breakdown_calc
from algorithms.account_segmentation import create_required_summary_tables, account_segmentation_rater
from algorithms.rationale import rationale_rater
from algorithms.exposure_management_task import pull_exchange_rate_data
from algorithms.spatialkey.spatialkey_rating_col_save import spatialkey_rating_col_save
from algorithms.model_state import model_state
from algorithms.nmp.nmp_rating import nmp_rating_calc
from algorithms.case_pricing.case_pricing_totals import case_pricing_totals
from algorithms.utilities import RunAsyncRaterProgress, TimerTracker
from libraries.email_notification.algorithms.bug_report import provision_bug_report_inputs_outputs
from algorithms.cyber_rating import cyber_rating, cyber_hxd_assignment
from algorithms.climate_documents.climate_peril_selection import climate_peril_selection
from algorithms.cat_zone_summary import cat_zone_summary


@hx.rating
def rating_algorithm(hxd):
    hxd.policy_information.small_schedule_model = not hxd.policy_information.large_schedule_model


    # Policy information
    policy_information_mapping(hxd)
    layers_calc(hxd)
    schedule_tiv_rater_calc(hxd)
    hxd.schedule.schedule_total.num_locs = len(list(hxd.schedule.schedule_table))

    if hxd.temp.output_json:
        data_assignment(hxd, json.loads(hxd.temp.output_json))

    rate_change_rater(hxd)
    quote_doc_rating_actions(hxd)
    account_segmentation_rater(hxd)
    rationale_rater(hxd)
    spatialkey_rating_col_save(hxd)
    state_county_rating_col_save(hxd)
    experience_rating(hxd)
    fire_occupancy_guide(hxd)

    # Populates default text box and dynamic dropdowns in the model
    populate_text(hxd)
    populate_dropdown(hxd)
    model_state(hxd)
    initial_quoted_inputs(hxd)
    
    validation_error(hxd)
    if hxd.temp.output_json and hxd.temp.simulation_validation_json:
        validation_run_schedule_rater_error(hxd, json.loads(hxd.temp.output_json), json.loads(hxd.temp.simulation_validation_json))
    elif hxd.temp.output_json:
        validation_run_schedule_rater_error(hxd, json.loads(hxd.temp.output_json))

    populate_notifications(hxd)
    populate_info_boxes_text(hxd)

    #Climate
    climate_peril_selection(hxd)
    validate_hurricane(hxd)

    # Nested country/state summary table
    create_country_state_summary(hxd, hxd.pricing_layer_segmentation.state_country)

    # If the policy is cased priced 
    if hxd.policy_information.is_case_priced:
        case_pricing_totals(hxd)

    provision_bug_report_inputs_outputs(hxd)
    


def run_schedule_rater(hxd, progress, save_case_pricing = False):
    '''
    Function that runs most of the rater function (apart from frontend mapping and text populate)
    '''
    if save_case_pricing == False:
        status = RunAsyncRaterProgress(hxd, progress)
    # Create tags
    generate_tags(hxd)

    # Update the field labels
    update_schedule_field_labels(hxd)

    # Pull exchange rate data from EM database
    if not save_case_pricing: #### FS Addition for save_case_pricing_bug
        pull_exchange_rate_data(hxd, progress) 
    
    # other_data is a dict that carries the information that are not stored in dataframe format in variable df
    other_data = {}

    # Load in inflation
    other_data = inflation(hxd, other_data)

    # Loads schedule and calculates schedule outputs
    df = read_schedule_table(hxd)
    df = ind_occ_map(hxd, df)

    # Decide if need to assign value to hxd for large models, set 400,000 for 20M node limit
    other_data['large_model_assign'] = hxd.policy_information.large_schedule_model and (
                                        (len(df) <= 100_000 and (len(df) * len(hxd.layers) <= 200_000))   
                                    )

    # Get currency exchange first as it's used in multiple places
    if not save_case_pricing: #### FS Addition for save_case_pricing_bug
        df = get_currency_exchange(hxd, df, progress)
    else:
        exchange_rate = hxd.policy_information.exchange_rate or 1
        df = df.with_columns(pl.lit(exchange_rate).alias("exchange_rate"))

    df = schedule_table_calc(hxd, df, other_data)
    schedule_table_hxd_assignment(hxd, df, other_data)

    # Map TIV to USD
    df = map_tiv_usd(hxd, df, other_data, progress)

    perils = ["fire", "wf", "ws", "eq", "scs", "fl"]
    peril_node_names = ["fire", "wildfire", "named_windstorm", "quake", "scs", "flood"]
    for peril, peril_node_name in zip(perils, peril_node_names):
        for index, layer in enumerate(hxd.layers, start=1):
            df = peril_covered_layer(hxd, df, index, layer, peril, peril_node_name)

    map_layers_usd(hxd, df, other_data, perils, peril_node_names)

    if save_case_pricing == False:
        status.update("map_layers_usd")

    # Calculate underwriter adjustments
    underwriter_adjustments(hxd, df, other_data)

    # Calculate Business Interruption output
    df = bi_rating_calc(hxd, df, other_data)

    if not (df.shape[0] == 1 and df["year_built"].null_count() == 1):  # Default setting error catching TODO improve
        # Calculate peril specific rating items
        df = fire_rating_calc(hxd, df, other_data)
        df = fire_hxd_assignment(hxd, df, other_data)

        df = cyber_rating(hxd, df)
        df = cyber_hxd_assignment(hxd, df, other_data)

        df = wildfire_rating_calc(hxd, df, other_data)
        df = wildfire_hxd_assignment(hxd, df, other_data)

        df = windstorm_us_rating_calc(hxd, df, other_data)
        df = windstorm_intl_rating_calc(hxd, df, other_data)
        df = windstorm_expected_loss_calc(hxd, df, other_data)
        df = windstorm_hxd_assignment(hxd, df, other_data)

        df = earthquake_us_rating_calc(hxd, df, other_data)
        df = earthquake_intl_rating_calc(hxd, df, other_data)
        df = earthquake_expected_loss_calc(hxd, df, other_data)
        df = earthquake_hxd_assignment(hxd, df, other_data)

        df = hail_rating_calc(hxd, df, other_data)
        df = hail_hxd_assignment(hxd, df, other_data)

        df = tornado_rating_calc(hxd, df, other_data)
        df = tornado_hxd_assignment(hxd, df, other_data)
        df = scs_hxd_assignment(hxd, df, other_data)

        df = flood_us_rating_calc(hxd, df, other_data)
        df = flood_intl_rating_calc(hxd, df, other_data)
        df = flood_hxd_assignment(hxd, df, other_data)

        ### Simulation/RMS input for earthquake/windstorm ###

        df = cat_method_calc(hxd, df, other_data)

        cat_peril = ["windstorm_us", "earthquake_us", "windstorm_intl", "earthquake_intl"]
        df = cat_method_expected_loss(hxd, df, other_data, cat_peril)

        us_cat_peril = ["windstorm_us", "earthquake_us"]
        df = cat_method_us_mi_tp_components(hxd, df, other_data, us_cat_peril)

        df = cat_method_hxd_assignment(hxd, df, other_data)
        df = drop_cat_method_columns(hxd, df, other_data) 

        if save_case_pricing == False:
            status.update("earthquake_windstorm_simulation")
        
        ### Calculates Premium and Summary for each peril
        peril_node_names = [
            "fire", 
            "wildfire_us", "wildfire_intl",
            "windstorm_us", "windstorm_intl", 
            "earthquake_us", "earthquake_intl", 
            "hail_us", "hail_intl", 
            "tornado_us", "tornado_intl",
            "flood_us", "flood_intl",
            "cyber",
            "nmp"
            ]

        ### NMP expected loss
        df = nmp_rating_calc(hxd,df,other_data,peril_node_names)

        df, other_data = total_expected_loss_summary(hxd, df, other_data, peril_node_names)

        # Calculates direct and indirect expenses, gross net premium
        for peril in peril_node_names:
            df = peril_rating_summary(hxd, df, other_data, peril)

        df = peril_rating_assignment(hxd, df, other_data)
        
        # Selects method with highest premium and populate the result to front end (Pre/Post UW Adj Summary)
        df = premium_summary(hxd, df, other_data, peril_node_names)
        df = premium_summary_assignment(hxd, df, other_data)

        if save_case_pricing == False:
            status.update("premium_summary")

        # Updates the df for the final gg technical premium
        df = final_technical_premium_columns(hxd, df, other_data)

        # Calculate and populate results to Peril Analysis Page
        fire_analysis_summary(hxd, df, other_data)
        wildfire_analysis_summary(hxd, df, other_data)
        windstorm_analysis_summary(hxd, df, other_data)
        earthquake_analysis_summary(hxd, df, other_data)
        flood_analysis_summary(hxd, df, other_data)
        scs_analysis_summary(hxd, df, other_data)

        overall_analysis_summary(hxd, df, other_data, peril_node_names)

        create_required_summary_tables(hxd, other_data)

        if hxd.policy_information.team != "Renewables":
            df = cat_zone_summary(hxd, df, other_data)

        if save_case_pricing == False:
            status.update("create_required_summary_tables")

        ### Climate Metrics
        df = climate_metrics_calc(hxd, df, other_data)

        ### Equipment Breakdown/TRIA
        if (hxd.policy_information.team == "NACP" or hxd.policy_information.team == "European Commercial Property"):
            equipment_breakdown_calc(hxd, df, other_data)
            tria_calc(hxd, df, other_data)

        quote_doc_rater_calc(hxd, df)

        # We only output values to result tab if the schedule is valid
        other_data["valid_schedule"] = True
    else:
        other_data["valid_schedule"] = False

    hxd.temp.output_json = json.dumps(other_data)

    schedule_table_hxd_assignment_state_county(hxd, df, other_data["large_model_assign"])

    if hxd.policy_information.is_case_priced:
        with hxd.df_output.open("b") as f:
            df.write_csv(f)
    
    if save_case_pricing == False: 
        status.finish()
            
    return other_data, df
