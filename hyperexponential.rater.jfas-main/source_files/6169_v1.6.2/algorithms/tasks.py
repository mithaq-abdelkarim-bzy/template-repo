import hx
import requests
from algorithms.rate_risk_information import expiring_policy_fetch
from algorithms.rate_experience_rating import fetch_bi_data
from algorithms.rate_renewal_pull import start_renewal
from algorithms.bi_intelligence import bi_intelligence_fetch,query_beazley_intelligence_database
from algorithms.rate_rationale import generate_rationale_doc
from libraries.email_notification.algorithms.bug_report import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report


@hx.task
def task(hxd, progress):
    pass

@hx.task
def experience_fields(hxd, progress):
    pass


@hx.task
def clear_exposure_input_task(hxd, progress):
    pass

@hx.task
def expiring_policy_fetch_task(hxd, progress):
    expiring_policy_fetch(hxd, progress)
    pass

@hx.task
def start_renewal_task(hxd, progress):
    start_renewal(hxd, progress)
    pass

@hx.task
def bi_intelligence_fetch_task(hxd, progress):
    bi_intelligence_fetch(hxd)
    
@hx.task
def generate_rationale_doc_task(hxd, progress):
    generate_rationale_doc(hxd, progress)

@hx.task
def new_bug_report_task(hxd, progress):
    model_name = "Property Risks - JFAS"
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
