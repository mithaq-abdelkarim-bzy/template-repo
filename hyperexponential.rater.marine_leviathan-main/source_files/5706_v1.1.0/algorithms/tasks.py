import hx, os, json, requests, openpyxl
import pandas as pd
from algorithms.rate_rate_change import rate_change_buckets
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from libraries.rate_change.algorithms.rate_change import RateChange as RateChangeLib



import numpy as np
import math
import copy
from algorithms.rate_rate_change import rate_change_buckets
from datetime import datetime
### --- EMAIL EXAMPLE --- ###
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import policy
from email.generator import BytesGenerator
import time
#from libraries.email_notification.algorithms.bug_report import send_bug_report, new_bug_report, cancel_bug_report, generate_bug_report, add_additional_file
import re
from html.parser import HTMLParser


import pandas as pd
import numpy as np

import datetime
import sys
import importlib
import algorithms.rate_constants as c
from algorithms.rate_utilities import ratio, title_rc,  look_up,  policy_term
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd


@hx.task
def sync_expiring_ids(hxd, progress):
    # Note this task is to be run following each migrated policy to sync the expiring ids
    hxd.model_state.expiring_policy_option_id = hx.meta.expiring_policy_option_id


@hx.task
def start_renewal_task(hxd, progress):
    # The following statement checks that the expiring information has been imported for renewals. Some teams might want to start
    # from a blank rater each time, in which case update the below
    ms = hxd.model_state
    sf = hxd.cds.standard_fields
    if not hxd.cds.standard_fields.insured_name:
        ms.landing_page_info = "❗**FAILED**: Click 'Undo' then 'Import Expiring Policy Data' in the top right corner.❗"
    else:
        ms.pressed_start_renewal_task = True
        ms.expiring_policy_option_id = hx.meta.expiring_policy_option_id
        sf.is_renewal = True
        # Add tasks which must be done before starting a policy here >>




# Importing expiring policy for rate change
@hx.task
def expiring_policy_fetch_task(hxd, progress):
    '''
    Async task to import data from an expiring policy option for rate change calculation and analysis of movement.
    Developers will need to update the task in two places, first for which variables from the expiring policy to import,
    second to assign these to the current model variables.
    '''
    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id = hxd.cds.rate_change.expiring_policy_option_id.selected #or 85244 # NOTE: use hardcoded ID for debugging if needed
    expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False)

    if expiring_response.status_code != 200:
        raise Exception(expiring_response.json())

    expiring_data = expiring_response.json()["data"]

    # Get fields from json response and push to hxd
    expiring_layers_len = len(expiring_data["cds"]["layers"])
    layer_mapping = {}

    for idx, layer in enumerate(hxd.cds.layers):
        # Throw error if expiring layer doesn't exist
        if layer.rate_change.expiring_layer > expiring_layers_len:
            hx.errors.fatal(f"Expiring Layer {layer.rate_change.expiring_layer}, mapped to Renewal Layer {idx+1}, does not exist. Number of expiring layers is {expiring_layers_len}.")

        mapped_expiring_layer_idx = layer.rate_change.expiring_layer - 1
        layer.rate_change.premium.line_100pct.annualised.expiring = expiring_premium = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["quoted_premium_annualised"]
        expiring_written_line = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["written_line"] or 0
        layer.rate_change.premium.beazley_line.annualised.expiring = expiring_premium * expiring_written_line
        layer.rate_change.expiring_policy_info.expiring_brokerage = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["brokerage"] or 0
        # NOTE add other expiring fields as required here

        # Save layer mapping
        layer_mapping[str(idx+1)] = layer.rate_change.expiring_layer

    hxd.cds.rate_change.layer_mapping = json.dumps(layer_mapping)

    # Confirm task has been run
    hxd.cds.rate_change.has_fetch_run = True
    hxd.cds.rate_change.has_fetch_not_run = False


@hx.task
def rarc_task(hxd, progress):

    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Make sure expiring data is up to date
    expiring_policy_fetch_task(hxd, progress)

    # Get correct buckets based on coverage
    buckets = rate_change_buckets(hxd)

    data_schema_static_filename = "data_schema_static_copy.py"
    data_schema_static_path = os.path.join(os.path.dirname(__file__), data_schema_static_filename)

    # Rate Change with offline_hxd
    rc = RateChangeLib(
        hxd=hxd,
        progress=progress,
        buckets=buckets,
        layers_path="cds/layers",
        expiring_actual_prem="quoted_premium_annualised",
        expiring_technical_prem="benchmark_premium_annualised",
        async_tasks=[],  # Pass the actual tasks, not strings
        data_schema_static_path=data_schema_static_path
    )

    rc.calculate_repriced_values(
        # expiring_policy_option_id=129400 # NOTE: for debugging if needed
    )

    # Use the repriced values to calculate the changes for each bucket
    rarc_df, rarc_list = rc.calculate_rarc_by_layer()
    
    # NOTE: for debugging if needed
    # pd.set_option('display.max_columns', None)
    # print(rarc_df)
    # print(rarc_list)

    # Calculate brokerage change for storage but not display
    for layer in hxd.cds.layers:
        expiring_brokerage = layer.rate_change.expiring_policy_info.expiring_brokerage or 0
        renewal_brokerage = layer.brokerage or 0
        layer.rate_change.brokerage_change.model_calculated = (1 - expiring_brokerage) / (1 - renewal_brokerage)

    # Push to hxd
    for rarc_layer, hxd_layer in zip(rarc_list, hxd.cds.layers):
        hxd_layer.rate_change.temp_storage = rarc_layer["temp_storage"]
        rarc_layer.pop("temp_storage")

        if hxd_layer.rate_change.expiring_layer:
            for key, value in rarc_layer.items():
                setattr(hxd_layer.rate_change, key, value)

    # Confirm task has been run
    hxd.cds.rate_change.has_rarc_run = True
    hxd.cds.rate_change.has_rarc_not_run = False






# Generate policy document in Excel
@hx.task
def policy_to_excel_task(hxd, progress):    
    from openpyxl.utils.cell import coordinate_to_tuple
    
    sf = hxd.cds.standard_fields

    # Load string containing data
    data = json.loads(hxd.policy_doc.data_dict)

    # Write the dictionary values to the Excel template
    if sf.is_rater_priced:
        template_path = f"./model/algorithms/Policy_Summary.xlsx"
    else:
        template_path = f"./model/algorithms/Policy_Summary - Case Priced.xlsx"

    # Load the workbook 
    workbook = openpyxl.load_workbook(template_path)

    # Fill the named ranges with data
    for key, value in data.items():
        if key in workbook.defined_names:
            # Get the cell corresponding to the named range
            cells = workbook.defined_names[key].destinations
            for sheet_name, coord in cells:
                # Get the relevant worksheet
                sheet = workbook[sheet_name]
                # If value is a list, write values dynamically
                if isinstance(value, list):
                    coord = coord.replace("$", "")
                    row, col = coordinate_to_tuple(coord)
                    for df_row_index, df_row in enumerate(value, start=row):
                        for df_col_index, (cell_key, cell_value) in enumerate(df_row.items(), start=col):
                            # Write each value into the corresponding cell
                            sheet.cell(row=df_row_index, column=df_col_index, value=cell_value)
                else:
                    # Assign single value to the cell
                    sheet[coord] = value


    # Protect the sheet to prevent changes
    # sheet.protection.enable()
    # sheet.protection.set_password(excel_password)

    # rationale_sheet = workbook['Rationale']
    # rationale_sheet.sheet_state = 'hidden'

    
    # Save the filled template to a new file
    with hxd.policy_doc.output_file.open("b") as f:
        workbook.save(f)
    # Store task data to allow comparison if anything changes in rating
    hxd.policy_doc.task_data_dict = hxd.policy_doc.data_dict

@hx.task
def insert_hx_meta_policy_references_task(hxd, progress):
    # add the Policy Reference to PAS
    hx.meta.pas_references.clear()
    section_reference = hxd.cds.standard_fields.policy_reference

    hx.meta.pas_references.append(section_reference)
    
    #hx.meta.pas_references.extend(list(pas_references_set))