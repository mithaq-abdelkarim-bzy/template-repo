import hx
import algorithms.utils_global_lists as lst
import requests
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from libraries.email_notification.algorithms.bug_report import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report

# Async task to import data from an expiring policy option into the current policy for rate change and analysis of movement
@hx.task
def expiring_policy_fetch_task(hxd, progress):
    layer = hxd.cds.layers[0] 
    cds_rc = layer.rate_change

    hx_renew = init_hx_renew_api()

    # hxd.expiring_policy_option_id to allow users to manually fetch the data vs hx.meta.expiring_option_id to automatically fetch renewals 
    expiring_policy_option_id = cds_rc.expiring_policy_option_id.selected
    # expiring_policy_option_id = 43688

    # URL for the API
    response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False)

    if response.status_code != 200:
        raise Exception(response.json())

    # results stored in dict : {data:{variable_name: value}}
    data = response.json()['data']

    # hxd.cds.standard_fields.is_renewal = True    

    cds_rc.expiring_insured_name = str(data["cds"]["standard_fields"]["insured_name"]) + " - " + str(data["cds"]["yoa"])
    if data["cds"]["standard_fields"]["policy_reference"]:
        cds_rc.expiring_policy_reference = data["cds"]["standard_fields"]["policy_reference"]
    
    # # To add when switching to new benchmark calcs
    # cds_rc.expiring_revenue = data["cds"]["exposure"]["aggregate"]["revenue"]
    # cds_rc.expiring_assets = data["cds"]["exposure"]["aggregate"]["assets"]
    # cds_rc.expiring_employees = data["cds"]["exposure"]["aggregate"]["employees"]
    # cds_rc.expiring_locations = data["cds"]["exposure"]["aggregate"]["locations"]


    cds_rc.expiring_beazley_share = data["cds"]["beazley_share"]
    cds_rc.expiring_beazley_layer = data["cds"]["beazley_layer"]
    expiring_beazley_index = int(cds_rc.expiring_beazley_layer.replace("Excess ",""))
    expiring_layer = data["cds"]["layers"][0]
    expiring_layer_attachment = data["cds"]["layers"][expiring_beazley_index]


    cds_rc.expiring_premium = expiring_layer["final_premium"]
    cds_rc.expiring_premium_annual = expiring_layer["final_premium_annual"]
    cds_rc.expiring_brokerage = expiring_layer["brokerage"]


    cds_rc.expiring_limit = expiring_layer["limit"]
    # # To add when switching to new benchmark calcs
    # cds_rc.expiring_limit_social_engineering = expiring_layer["limit_social_engineering"]
    cds_rc.expiring_excess = expiring_layer_attachment["excess"]
    # # To add when switching to new benchmark calcs
    # cds_rc.expiring_excess_social_engineering = expiring_layer["excess_social_engineering"]

    cds_rc.expiring_policy_term = data["cds"]["term_adjustment"] * 12
    
    pass

@hx.task
def start_renewal_task(hxd, progress):
    layer = hxd.cds.layers[0] 
    cds_rc = layer.rate_change

    hx_renew = init_hx_renew_api()

    expiring_policy_option_id = hx.meta.expiring_policy_option_id

    # URL for the API
    response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False)

    if response.status_code != 200:
        raise Exception(response.json())

    # results stored in dict : {data:{variable_name: value}}
    data = response.json()['data']
    expiring_layer = data["cds"]["layers"][0]
    if not hxd.cds.standard_fields.insured_name:
        hx.errors.fatal("Please press 'Undo' and 'Import Expiring Policy Data' at the top right corner")

    hxd.model_state.pressed_start_renewal_task = True
    hxd.cds.standard_fields.is_renewal = True    
    layer.status = "Submission"
    cds_rc.expiring_brokerage = expiring_layer["brokerage"]
    cds_rc.expiring_insured_name = str(data["cds"]["standard_fields"]["insured_name"]) + " - " + str(data["cds"]["yoa"])
    if data["cds"]["standard_fields"]["policy_reference"]:
        cds_rc.expiring_policy_reference = data["cds"]["standard_fields"]["policy_reference"]

    # # To add when switching to new benchmark calcs
    # cds_rc.expiring_revenue = data["cds"]["exposure"]["aggregate"]["revenue"]
    # cds_rc.expiring_assets = data["cds"]["exposure"]["aggregate"]["assets"]
    # cds_rc.expiring_employees = data["cds"]["exposure"]["aggregate"]["employees"]
    # cds_rc.expiring_locations = data["cds"]["exposure"]["aggregate"]["locations"]

    cds_rc.expiring_premium = expiring_layer["final_premium"]
    cds_rc.expiring_premium_annual = expiring_layer["final_premium_annual"]

    cds_rc.expiring_beazley_share = data["cds"]["beazley_share"]

    cds_rc.expiring_limit = expiring_layer["limit"]
    # # To add when switching to new benchmark calcs
    # cds_rc.expiring_limit_social_engineering = expiring_layer["limit_social_engineering"]
    # cds_rc.expiring_excess = expiring_layer["excess"]
    # cds_rc.expiring_excess_social_engineering = expiring_layer["excess_social_engineering"]

    cds_rc.expiring_policy_term = data["cds"]["term_adjustment"] * 12

    pass


@hx.task
def new_bug_report_task(hxd, progress):
    model_name = "Excess Fidelity and Crime"
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