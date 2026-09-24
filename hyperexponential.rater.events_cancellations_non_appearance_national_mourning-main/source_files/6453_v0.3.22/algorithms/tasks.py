# v0.5.0
import hx, os, json, requests, openpyxl, copy

from algorithms.rate_change.task_rarc_expiry_policy_fetch   import task_expiring_policy_fetch, task_expiring_policy_fetch_coverage
from algorithms.rate_change.task_rarc                       import task_rarc_layer, task_rarc_coverage
from algorithms.rate_change.task_rarc_insured_asset         import task_rarc_layer_insured_asset, task_rarc_coverage_insured_asset
from algorithms.tsk_policy_to_excel                         import tsk_policy_to_excel
from algorithms.tsk_start_renewal                           import tsk_start_renewal
from algorithms.tsk_sql_bi_data                             import tsk_sql_bi_data
from algorithms.tsk_simulation                              import tsk_simulation
from algorithms.tsk_fetch_ihs_data                          import tsk_fetch_ihs_data
from algorithms.rate_constants                              import max_layers
from libraries.email_notification.algorithms.bug_report     import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report

# sets hx pas reference to the entered section reference(s)
# needs to be added to each task run, and section_reference made an async input of each of the tasks it is added to
def set_pas_references(hxd, progress):    
    pas_to_assign = [hxd.cds.layers[x].coverages.ec_total.section_reference for x in range(max_layers) if x is not None]
    if pas_to_assign[0] is not None:
        hx.meta.pas_references = pas_to_assign
    else:
        hx.meta.pas_references.clear()

@hx.task
def task_sql_bi_data(hxd, progress):
    tsk_sql_bi_data(hxd, progress)
    set_pas_references(hxd, progress)
    pass


@hx.task
def task_simulation(hxd, progress):
    tsk_simulation(hxd, progress)
    set_pas_references(hxd, progress)
    pass


@hx.task
def task_fetch_ihs_data(hxd, progress):
    tsk_fetch_ihs_data(hxd, progress)
    set_pas_references(hxd, progress)
    pass


@hx.task
def task_start_renewal(hxd, progress):
    tsk_start_renewal(hxd, progress)
    set_pas_references(hxd, progress)
    pass


@hx.task
def sync_expiring_ids(hxd, progress):
    # Note this task is to be run following each migrated policy to sync the expiring ids
    hxd.model_state.expiring_policy_option_id                = hx.meta.expiring_policy_option_id
    hxd.cds.rate_change.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id # Assigning this node in this tasks allows to clear the override at the creation of a renewal
    set_pas_references(hxd, progress)
    pass


@hx.task
def expiring_policy_fetch_task(hxd, progress):
    task_expiring_policy_fetch(hxd, progress)
    set_pas_references(hxd, progress)
    pass
    
# Importing expiring policy info for rate change
@hx.task
def expiring_policy_fetch_coverages_task(hxd, progress):
    task_expiring_policy_fetch_coverage(hxd, progress)
    set_pas_references(hxd, progress)
    pass

@hx.task
def rarc_task(hxd, progress):
    task_rarc_layer(hxd, progress)
    set_pas_references(hxd, progress)
    pass

@hx.task
def rarc_task_coverages(hxd, progress):
    task_rarc_coverage(hxd, progress)
    set_pas_references(hxd, progress)
    pass


@hx.task
def rarc_task_insured_asset(hxd, progress):
    task_rarc_layer_insured_asset(hxd, progress)
    set_pas_references(hxd, progress)
    pass


@hx.task
def rarc_task_coverages_insured_asset(hxd, progress):
    task_rarc_coverage_insured_asset(hxd, progress)
    set_pas_references(hxd, progress)
    pass


# Generate policy document in Excel
@hx.task
def policy_to_excel_task(hxd, progress):
    tsk_policy_to_excel(hxd, progress)
    set_pas_references(hxd, progress)
    pass

# Log new bug - add the following 5 methods for bug report section
@hx.task
def new_bug_report_task(hxd, progress):
    # Update rater name
    model_name = "Skeleton"
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
