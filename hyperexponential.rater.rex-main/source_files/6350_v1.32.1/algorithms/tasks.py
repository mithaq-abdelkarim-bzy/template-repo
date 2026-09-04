import hx
import polars as pl
import pandas as pd
import numpy as np
import gc
from algorithms.comments import add_new_comment, start_add_comments
from algorithms.task_deductible import copy_fire_ded, named_storm_ws, all_tier_fl_ws, fl_ws, tx_ws, \
    tier_fl_ws, all_wind_ws_scs, ca_eq, all_ca_eq, copy_primary_deductibles
from algorithms.exposure_management_task import search_exposure_management_data, pull_in_exposure_management_data, pull_general_exchange_rate_data
from algorithms.spatialkey.batch_enhancement import run_batch_enhancement, open_spatialkey_dashboard
from algorithms.rate_change import expiring_policy_fetch
from algorithms.firm_task import search_firm, import_firm
from algorithms.quote_documents.quote_document_generation import generate_quote_doc
from algorithms.rating import run_schedule_rater
from algorithms.simulation.simulation import run_simulation
from algorithms.data_assignment import generate_output_file
from time import perf_counter
from algorithms.account_segmentation import produce_heatmap
from algorithms.rationale import update_first_saved
from algorithms.automated_testing_task import push_file_to_temp, push_df_to_temp, load_from_schedule, load_into_debug
from algorithms.renewal_pull import start_renewal
from algorithms.summary import produce_climate_map
from algorithms.climate_documents.generate_climate_doc import generate_climate_doc
from algorithms.climate_documents.generate_flood_climate_metrics import generate_flood_climate_metrics
from algorithms.rationale import rationale_rater, generate_uw_rationale_doc
from algorithms.utilities import convert_hx_list_to_df, pd_df_from_hx_list, write_pd_to_hxd
from algorithms.experience_rating import apply_experience_adjustment, remove_experience_adjustment
from algorithms.populate_fields import show_hide_notifications
from algorithms.schedule import read_schedule_table, check_remodel
from algorithms.case_pricing.save_case_pricing_results import save_case_pricing_results
from algorithms.case_pricing.case_pricing_calcs import case_pricing_calc_tech_premium
from algorithms.policy_information import upsert_hx_meta_pas_references
from libraries.email_notification.algorithms.bug_report import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report


@hx.task
def run_spatialkey_task(hxd, progress):
    # t1_start = perf_counter()
    run_batch_enhancement(hxd, progress)
    # t1_stop = perf_counter()

    # hx.errors.fatal(f"Elapsed time: {t1_stop - t1_start}")

@hx.task
def open_spatialkey_dashboard_task(hxd, progress):
    open_spatialkey_dashboard(hxd, progress)

@hx.task
def named_storm_ws_task(hxd, progress):
    named_storm_ws(hxd)

@hx.task
def all_tier_fl_ws_task(hxd, progress):
    all_tier_fl_ws(hxd)

@hx.task
def fl_ws_task(hxd, progress):
    fl_ws(hxd)

@hx.task
def tx_ws_task(hxd, progress):
    tx_ws(hxd)

@hx.task
def tier_fl_ws_task(hxd, progress):
    tier_fl_ws(hxd)

@hx.task
def all_wind_ws_scs_task(hxd, progress):
    all_wind_ws_scs(hxd)

@hx.task
def ca_eq_task(hxd, progress):
    ca_eq(hxd)

@hx.task
def all_ca_eq_task(hxd, progress):
    all_ca_eq(hxd)

@hx.task
def clear_deductibles_task(hxd, progress):
    pass

@hx.task
def copy_fire_ded_task(hxd, progress):
    copy_fire_ded(hxd)

@hx.task
def add_new_comment_task(hxd, progress):
    add_new_comment(hxd)

@hx.task
def start_add_comments_task(hxd, progress):
    start_add_comments(hxd)

@hx.task
def fetch_em_location_data_task(hxd, progress):
    fetch_em_location_data(hxd, progress)

@hx.task
def search_exposure_management_data_task(hxd, progress):
    # t1_start = perf_counter()
    search_exposure_management_data(hxd, progress)
    # t1_stop = perf_counter()

    # hx.errors.fatal(f"Elapsed time: {t1_stop - t1_start}")

@hx.task
def pull_in_exposure_management_data_task(hxd, progress):
    # t1_start = perf_counter()
    pull_in_exposure_management_data(hxd, progress)
    # t1_stop = perf_counter()

    # hx.errors.fatal(f"Elapsed time: {t1_stop - t1_start}")

@hx.task
def expiring_policy_fetch_task(hxd, progress):
    expiring_policy_fetch(hxd, progress)

@hx.task
def run_schedule_rater_task(hxd, progress):
    # t1_start = perf_counter()
    if hxd.policy_information.policy_level_validation:
        hx.errors.fatal("Please clear all validation errors (X on the button right corner) before running the rater")

    other_data, df = run_schedule_rater(hxd, progress)
    gc.collect()
    if hxd.policy_information.large_schedule_model:
            generate_output_file(hxd, df, other_data)

    # flags for validation
    hxd.experience_rating.experience_rating_run = False
    hxd.experience_rating.run_rater_run = True
    # t1_stop = perf_counter()

    # hx.errors.fatal(f"Elapsed time: {t1_stop - t1_start}")

@hx.task
def search_firm_task(hxd, progress):
    search_firm(hxd)

@hx.task
def import_firm_task(hxd, progress):
    import_firm(hxd)

@hx.task    
def generate_quote_doc_task(hxd, progress):
    generate_quote_doc(hxd, progress)

@hx.task
def run_simulation_task(hxd, progress):
    # t1_start = perf_counter()
    run_simulation(hxd, progress)
    # t1_stop = perf_counter()

    # hx.errors.fatal(f"Elapsed time: {t1_stop - t1_start}")    

@hx.task
def confirm_override_task(hxd, progress):
    large_workflow_structure = hxd.schedule.large_schedule_workflow
    if large_workflow_structure.schedule_file.exists:
        large_workflow_structure.load_from_schedule_file = True
        with large_workflow_structure.schedule_file.open("b") as f:
            large_workflow_structure.num_of_locations = len(pl.read_csv(f))

@hx.task
def update_first_saved_task(hxd, progress):
    update_first_saved(hxd, progress)

@hx.task
def rationale_rater_task(hxd, progress):
    rationale_rater(hxd, progress)

@hx.task    
def generate_uw_rationale_doc_task(hxd, progress):
    generate_uw_rationale_doc(hxd, progress)

@hx.task
def produce_heatmap_task(hxd, progress):
    produce_heatmap(hxd, progress)

### Automated testing / migration related
@hx.task
def push_file_to_temp_task(hxd, progress):
    push_file_to_temp(hxd)

@hx.task
def push_df_to_temp_task(hxd, progress):
    push_df_to_temp(hxd)

@hx.task
def load_from_schedule_task(hxd, progress):
    load_from_schedule(hxd)

@hx.task
def load_into_debug_task(hxd, progress):
    load_into_debug(hxd)

### Renewal Workflow
@hx.task
def import_accgrpid_only_task(hxd, progress):
    hxd.policy_information.accgrpid = hxd.exposure_management_api.inputs.accgrpid

@hx.task
def start_renewal_task(hxd, progress):
    start_renewal(hxd)

### Climate   
@hx.task
def generate_flood_climate_metrics_task(hxd, progress):
    generate_flood_climate_metrics(hxd, progress)

@hx.task
def generate_climate_doc_task(hxd, progress):
    generate_climate_doc(hxd, progress)

@hx.task
def produce_climate_map_task(hxd, progress):
    produce_climate_map(hxd, progress)
    
### claims FX rates
@hx.task
def pull_exchange_rate_claim_data_task(hxd, progress):

    res_slip = pull_general_exchange_rate_data(hxd, progress,hxd.policy_information.slip_currency)

    # predefine this to neaten up the code
    er = hxd.experience_rating

    claims_df = pd_df_from_hx_list(er.claims)

    #need to calculate a selected currency column to use
    claims_df['currency_selected'] = claims_df['currency_calculated']
    claims_df.loc[claims_df['currency_override'].notnull(), 'currency_selected'] = claims_df['currency_override']

    #get a list of unique currencies
    currencies = claims_df["currency_selected"].unique()

    # initialise adf with unique currencies
    d = {'currency': currencies}
    df = pd.DataFrame(data=d)

    
    def pull_exchange_rate(row):
        res_claim = pull_general_exchange_rate_data(hxd, progress, row['currency'])
        return res_claim[0]
    
    df['exchange_rate'] = df.apply(pull_exchange_rate, axis = 1)

    claims_df = claims_df.merge(df, how="left", left_on="currency_selected", right_on="currency")

    claims_df["clm_to_slip_fx_rate"] = res_slip[0] / claims_df['exchange_rate']
    claims_df["exchange_rate_date"] = res_slip[1]

    output_columns = ["clm_to_slip_fx_rate",
                    "exchange_rate_date"]

    write_pd_to_hxd(claims_df, er.claims, output_columns)

### apply calculated experience adjustment
@hx.task
def apply_experience_adjustment_task(hxd, progress):
    #can't run the rater in this task right now, Seb looking into the error
    apply_experience_adjustment(hxd, progress)
    
### remove calculated experience adjustment
@hx.task
def remove_experience_adjustment_task(hxd, progress):
    remove_experience_adjustment(hxd, progress)
    run_schedule_rater_task(hxd, progress)
   
@hx.task
def show_hide_notifications_task(hxd, progress):
    show_hide_notifications(hxd, progress)

@hx.task
def sync_expiring_ids(hxd, progress):
    # Note this task is to be run following each migrated policy to sync the expiring ids
    hxd.model_state.expiring_policy_option_id = hx.meta.expiring_policy_option_id

@hx.task
def fill_intl_ded_countries_task(hxd, progress):
    # Loads schedule and calculates schedule outputs
    df = read_schedule_table(hxd)
    df = df.filter(pl.col("country") != "United States")
    intl_countries = df.groupby("country").sum()[["country", "tiv_total"]].to_pandas()

    for peril in ["fire", "named_windstorm", "scs", "flood", "quake", "wildfire"]:
        ded_df = pd_df_from_hx_list(getattr(hxd.non_layer_perils, peril).intl_ded)
        ded_df = ded_df[ded_df["country"].isin(intl_countries["country"].values)]
        ded_df = ded_df.merge(intl_countries, on="country", how="outer")
        ded_df = ded_df.sort_values("country")
        ded_df["tiv"] = ded_df["tiv_total"]
        ded_df = ded_df.drop("tiv_total", axis=1)
        ded_df = ded_df.replace({np.nan: None})
        if ded_df.empty:
            getattr(hxd.non_layer_perils, peril).intl_ded = [{}]
        else:
            getattr(hxd.non_layer_perils, peril).intl_ded = ded_df.to_dict(orient="records")


@hx.task
def copy_intl_ded_perils_task(hxd, progress):
    for peril in ["named_windstorm", "scs", "flood", "quake", "wildfire"]:
        ded_df = pd_df_from_hx_list(hxd.non_layer_perils.fire.intl_ded)
        ded_df = ded_df.replace({np.nan: None})
        getattr(hxd.non_layer_perils, peril).intl_ded = ded_df.to_dict(orient="records")


@hx.task
def copy_primary_deductibles_task(hxd, progress):
    copy_primary_deductibles(hxd)



# Task to save the case pricing results in the model
@hx.task
def save_case_pricing_results_task(hxd, progress):
    if hxd.policy_information.policy_level_validation:
        hx.errors.fatal("Please clear all validation errors (X on the button right corner) before running the rater")

    save_case_pricing_results(hxd, progress)


@hx.task
def case_pricing_calc_tech_premium_task(hxd, progress):
    case_pricing_calc_tech_premium(hxd, progress)

# Task to generate machinery breakdown industry input table
@hx.task
def machinery_breakdown_industry_task(hxd, progress):
    # Loads schedule and sets up the Machinery Breakdown table 

    non_cat_base_rates_pl = pl.from_pandas(hx.params.non_cat_base_rates)
    non_cat_base_rates_pl = non_cat_base_rates_pl.with_columns((pl.col("MB") - pl.col("Contents")).alias("excess_mb_rate"))
    industries_with_mb_list = non_cat_base_rates_pl.filter(pl.col("excess_mb_rate") > 0)["Industry"].unique().to_list()

    columns = ["industry", "fire_mb_proportion"]
    mb_existing_pl = pl.from_pandas(pd.DataFrame([{column: getattr(row, column) for column in columns} for row in hxd.non_layer_perils.fire.machinery_breakdown]))
    
    df = read_schedule_table(hxd)
    df = df[["industry", "tiv_contents", "tiv_bi"]].fill_null(0)
    df = df.filter(pl.col("tiv_contents") > 0)      # if there is no contents TIV, then there cannot be machinery breakdown
    df = df.with_columns((pl.col("tiv_contents") + pl.col("tiv_bi")).alias("tiv_contents_bi"))

    if df["tiv_contents"].fill_null(0).sum() == 0:      # if there is no contents TIV, then there cannot be machinery breakdown
        hxd.non_layer_perils.fire.machinery_breakdown_message = "Please enter schedule information and ensure that there is at least one location with contents TIV."
    else:
        mb_pl = df.groupby("industry").agg(pl.sum("tiv_contents_bi").alias("tiv_contents"))     # TODO - rename node to "tiv_content_bi" - DP 03/10 labelled tiv_contents to avoid changing node and causing a breaking change 
        mb_pl = mb_pl.filter(pl.col("industry").is_in(industries_with_mb_list)).sort("industry")
        mb_pl = mb_pl.join(mb_existing_pl, on = "industry", how = "left").fill_null(0)
                
        if mb_pl.select(pl.col("industry").drop_nulls()).height == 0:
            hxd.non_layer_perils.fire.machinery_breakdown = [{"industry": "", "tiv_contents": 0, "fire_mb_proportion": 0}]      # TODO - rename node to "tiv_content_bi" - DP 03/10 kept as tiv_contents to avoid changing node and causing a breaking change 
            hxd.non_layer_perils.fire.machinery_breakdown_message = "There are no industries in the schedule with Machinery Breakdown coverage."
        else:
            hxd.non_layer_perils.fire.machinery_breakdown = mb_pl.to_pandas().to_dict("records")
            hxd.non_layer_perils.fire.machinery_breakdown_message = "Enter the proportion of the TIV that is subject to Machinery Breakdown cover below."



@hx.task
def new_bug_report_task(hxd, progress):
    model_name = "REX"
    new_bug_report(hxd, progress, model_name)

@hx.task
def send_bug_report_task(hxd, progress):
    send_bug_report(hxd, progress)

@hx.task
def cancel_bug_report_task(hxd, progress):
    cancel_bug_report(hxd, progress)

@hx.task
def generate_bug_report_task(hxd, progress):
    generate_bug_report(hxd, progress)

@hx.task
def add_additional_file_task(hxd, progress):
    add_additional_file(hxd, progress)

@hx.task
def check_remodel_task(hxd, progress):
    check_remodel(hxd)

@hx.task
def upsert_hx_meta_pas_references_task(hxd, progress):
    upsert_hx_meta_pas_references(hxd)