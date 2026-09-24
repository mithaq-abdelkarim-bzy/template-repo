# v0.5.0
import hx, os, json, requests, openpyxl, copy

from algorithms.task_start_renewal import task_start_renewal
from algorithms.rate_change.task_rarc_expiry_policy_fetch import task_expiring_policy_fetch, task_expiring_policy_fetch_coverage
from algorithms.rate_change.task_rarc import task_rarc_layer, task_rarc_coverage

@hx.task
def sync_expiring_ids(hxd, progress):
    # Note this task is to be run following each migrated policy to sync the expiring ids
    hxd.model_state.expiring_policy_option_id = hx.meta.expiring_policy_option_id

@hx.task
def start_renewal_task(hxd, progress):
    task_start_renewal(hxd, progress)

# Importing expiring policy for rate change
@hx.task
def expiring_policy_fetch_task(hxd, progress):
    task_expiring_policy_fetch(hxd, progress)

@hx.task
def rarc_task(hxd, progress):
    task_rarc_layer(hxd, progress)
