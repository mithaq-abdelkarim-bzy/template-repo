import hx
import os
import pandas as pd
import requests
import json
from libraries.hx_renew_api.algorithms.init_hx_renew_api    import init_hx_renew_api
from mailmerge                                              import MailMerge
from algorithms.generate_doc                                import generate_doc
from libraries.email_notification.algorithms.bug_report     import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report




# Importing expiring policy for rate change
'''
Async task to import data from an expiring policy option for rate change calculation and analysis of movement.
Developers will need to update the task in two places, first for which variables from the expiring policy to import,
second to assign these to the current model variables.
'''

@hx.task
def start_renewal_task(hxd, progress):
   
    # The following statement checks that the expiring information has been imported for renewals. Some teams might want to start
    # from a blank rater each time, in which case update the below
    if not hxd.cds.standard_fields.insured_name:
        hxd.model_state.landing_page_info = "❗❗ FAILED: Click 'Undo' then 'Import Expiring Policy Data' in the top right corner ❗❗"
    else:
        hxd.model_state.pressed_start_renewal_task = True

        # Add tasks which must be done before starting a policy here >>

        # expiring_policy_fetch_task(hxd, progress)


@hx.task
def generate_uw_doc(hxd, progress):
    generate_doc(hxd, progress)
    pass

@hx.task
def new_bug_report_task(hxd, progress):
    model_name = "M&A"
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