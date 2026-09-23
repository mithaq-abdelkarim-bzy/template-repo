import hx
import os
import json
from algorithms.rate_rate_change import rate_change_buckets
from algorithms import parameter_tables_schema as params
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from libraries.rate_change.algorithms.rate_change import RateChange as RateChangeLib
from libraries.email_notification.algorithms.bug_report import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report


# Update example task below 
@hx.task
def rarc_task(hxd, progress):

    if hxd.cds.rate_change.remove_tasks_errors == "Yes":
        pass
    else:
        buckets = rate_change_buckets(hxd)

        data_schema_static_filename = "data_schema_static_copy.py"
        data_schema_static_path = os.path.join(os.path.dirname(__file__), data_schema_static_filename)

        # Rate Change with offline_hxd
        rc = RateChangeLib(
            hxd=hxd,
            progress=progress,
            buckets=buckets,
            layers_path="cds/layers",  # SA: Is this necessary?
            expiring_actual_prem="quoted_premium",  # SA: Is this necessary?
            expiring_technical_prem="benchmark_premium",  # SA: Is this necessary?
            async_tasks=[],  # Pass the actual tasks, not strings
            data_schema_static_path=data_schema_static_path
        )

        rc.calculate_repriced_values(
            expiring_policy_option_id=hxd.cds.rate_change.expiring_policy_option_id.selected
        )

        # Use the repriced values to calculate the changes for each bucket
        rarc_df, rarc_list = rc.calculate_rarc_by_layer()

        # Push to hxd
        # for rarc_layer, hxd_layer in zip(rarc_list, hxd.cds.layers):
        #     hxd_layer.rate_change = rarc_layer
        for rarc_layer, hxd_layer in zip(rarc_list, hxd.cds.layers):
            hxd_layer.rate_change = rarc_layer
            hxd_layer.rate_change.temp_storage = rarc_layer["temp_storage"]
            rarc_layer.pop("temp_storage")
            


        layer_mapping = {}
        for idx, layer in enumerate(hxd.cds.layers):
            layer_mapping[str(idx+1)] = layer.rate_change.expiring_layer
        hxd.cds.rate_change.layer_mapping = json.dumps(layer_mapping)


        # Confirm task has been run
        hxd.cds.rate_change.has_rarc_run = True
        hxd.cds.rate_change.has_rarc_not_run = False

        pass










# Importing expiring policy for rate change
'''
Async task to import data from an expiring policy option for rate change calculation and analysis of movement.
Developers will need to update the task in two places, first for which variables from the expiring policy to import,
second to assign these to the current model variables.
'''

@hx.task
def expiring_policy_fetch_task(hxd, progress):
    
    # if not hxd.cds.rate_change.expiring_policy_option_id.selected:
    #     hx.errors.fatal("Expiring policy option ID cannot be empty.")
        
    if hxd.cds.rate_change.remove_tasks_errors == "Yes":
        pass
    else:       
        # Initialise the hx_renew_api library
        hx_renew = init_hx_renew_api()

        # Get expiring policy data
        expiring_policy_option_id = hxd.cds.rate_change.expiring_policy_option_id.selected 

        expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False)

        if expiring_response.status_code != 200:
            raise Exception(expiring_response.json())

        expiring_data = expiring_response.json()["data"]
        layer_mapping = {}
        # Get fields from json response and push to hxd
        for idx, layer in enumerate(hxd.cds.layers):
            layer.rate_change.expiring_policy_info.expiring_premium = expiring_data["cds"]["layers"][idx]["quoted_premium"]
            #layer.rate_change.expiring_policy_info.expiring_written_line = expiring_data["cds"]["layers"][idx]["written_line"]
            #layer.rate_change.expiring_policy_info.expiring_technical_premium = expiring_data["cds"]["layers"][idx]["technical_premium"]
            layer.rate_change.expiring_policy_info.expiring_benchmark_premium = expiring_data["cds"]["layers"][idx]["benchmark_premium"]
            #layer.rate_change.expiring_policy_info.expiring_tpi = expiring_data["cds"]["layers"][idx]["tpi"]
            # layer.rate_change.expiring_policy_info.expiring_bpi = expiring_data["cds"]["layers"][idx]["bpi"]
            # Save layer mapping
            layer.rate_change.expiring_layer = idx + 1
            layer_mapping[str(idx+1)] = layer.rate_change.expiring_layer

        hxd.cds.rate_change.layer_mapping = json.dumps(layer_mapping)

        # Confirm task has been run
        hxd.cds.rate_change.has_fetch_run = True
        hxd.cds.rate_change.has_fetch_not_run = False

# # Populate other useful fields
# hxd.cds.standard_fields.insured_name = expiring_data["cds"]["standard_fields"]["insured_name"]
# hxd.cds.currencies.source_currency = expiring_data["cds"]["currencies"]["source_currency"]






@hx.task
def start_renewal_task(hxd, progress):
   
    # The following statement checks that the expiring information has been imported for renewals. Some teams might want to start
    # from a blank rater each time, in which case update the below
    if not hxd.cds.standard_fields.insured_name:
        hxd.model_state.landing_page_info = "❗❗ FAILED: Click 'Undo' then 'Import Expiring Policy Data' in the top right corner ❗❗"
    else:
        hxd.model_state.pressed_start_renewal_task = True
        # Default renewal flag to true upon renewal    
        hxd.cds.standard_fields.is_renewal = True
        hxd.cds.rate_change.fetch_rarc_show_hide_renewal = True
        

        # Add tasks which must be done before starting a policy here >>

        # expiring_policy_fetch_task(hxd, progress)

@hx.task
def clear_eo_input_task(hxd,progress):
    discipline_list = hx.params.table_eo_discipline["discipline_name"]
    [setattr(getattr(hxd.cds.exposure.granular, item), "input_pct", 0.0) for item in discipline_list]
    ae_operation_list = hx.params.table_eo_ae_operation["ae_operations_name"]
    [setattr(getattr(hxd.cds.exposure.granular , item ), "input_pct", 0.0) for item in ae_operation_list]

    pass

@hx.task
def clear_mediatech_input_task(hxd, progress):
    industry_list = hx.params.table_mediatech_industry["industry_name"] 
    [setattr(getattr(hxd.cds.exposure.granular, item), "input_pct",0.0) for item in industry_list]
    pass


@hx.task
def new_bug_report_task(hxd, progress):
    model_name = "International PE"
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