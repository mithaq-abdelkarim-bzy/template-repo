# v0.5.0
import hx, os, json, requests, openpyxl, copy

from algorithms.task_start_renewal import task_start_renewal
from algorithms.rate_change.task_rarc_expiry_policy_fetch import task_expiring_policy_fetch, task_expiring_policy_fetch_coverage
from algorithms.rate_change.task_rarc import task_rarc_layer #, task_rarc_coverage
# from algorithms.rate_change.task_rarc_insured_asset import task_rarc_layer_insured_asset, task_rarc_coverage_insured_asset
from algorithms.task_policy_document import task_policy_to_excel
from libraries.email_notification.algorithms.bug_report import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report

from algorithms.steer.tasks_steer import steer_clear_raw_data,steer_validate_raw_data, steer_format_raw_data

from algorithms.steer.async_steer_triangles_exclusion_override import steer_tri_exclusions_setup, steer_tri_override_setup, steer_tri_count_exclusions_setup, steer_tri_count_override_setup

from algorithms.task_advanced_features import advanced_features

from algorithms.steer.async_steer_populate_bc_patterns import steer_populate_bc_patterns

@hx.task
def sync_expiring_ids(hxd, progress):
    # Note this task is to be run following each migrated policy to sync the expiring ids
    hxd.model_state.expiring_policy_option_id = hx.meta.expiring_policy_option_id

@hx.task
def start_renewal_task(hxd, progress):
    task_start_renewal(hxd, progress)

@hx.task
def expiring_policy_fetch_task(hxd, progress):
    task_expiring_policy_fetch(hxd, progress)
    
# Importing expiring policy info for rate change
@hx.task
def expiring_policy_fetch_coverages_task(hxd, progress):
    task_expiring_policy_fetch_coverage(hxd, progress)

@hx.task
def rarc_task(hxd, progress):
    task_rarc_layer(hxd, progress)

# Generate policy document in Excel
@hx.task
def policy_to_excel_task(hxd, progress):
    task_policy_to_excel(hxd, progress)

# Log new bug - add the following 5 methods for bug report section
@hx.task
def new_bug_report_task(hxd, progress):
    # Update rater name in HX
    model_name = "STEER"
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
def steer_clear_raw_data_task(hxd, progress):
    steer_clear_raw_data(hxd, progress) 

@hx.task
def steer_validate_raw_data_task(hxd, progress):
    steer_validate_raw_data(hxd, progress) 

@hx.task
def steer_format_raw_data_task(hxd, progress):
    steer_format_raw_data(hxd, progress) 

@hx.task
def steer_tri_exclusions_setup_task(hxd, progress):
    steer_tri_exclusions_setup(hxd, progress)
    pass

@hx.task
def steer_tri_override_setup_task(hxd, progress):
    steer_tri_override_setup(hxd, progress)
    pass

@hx.task
def steer_tri_count_exclusions_setup_task(hxd, progress):
    steer_tri_count_exclusions_setup(hxd, progress)
    pass

@hx.task
def steer_tri_count_override_setup_task(hxd, progress):
    steer_tri_count_override_setup(hxd, progress)
    pass

@hx.task
def steer_populate_bc_patterns_task(hxd, progress):
    steer_populate_bc_patterns(hxd, progress)
    pass

@hx.task
def advanced_features_task(hxd, progress):
    advanced_features(hxd, progress)
    pass

