import hx
import json
import os
import copy
import time
import pandas as pd
import numpy as np
import requests
import openpyxl
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from algorithms.rate_utilities import ratio, title_rc
from algorithms.rate_constants import excel_password
from algorithms.rate_rate_change import rate_change_buckets
from libraries.rate_change.algorithms.rate_change import RateChange as RateChangeLib
from algorithms.policy_document import create_dict_for_excel
from libraries.email_notification.algorithms.bug_report import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report

# Import expiring policy for rate change
@hx.task
def expiring_policy_fetch_task(hxd, progress):

    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id = hxd.cds.rate_change.expiring_policy_option_id.selected #or 85244 # NOTE: id used for testing
    expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False)

    if expiring_response.status_code != 200:
        raise Exception(expiring_response.json())

    expiring_data = expiring_response.json()["data"]

    # Get fields from json response and push to hxd
    for idx, layer in enumerate(hxd.cds.layers):
        layer.rate_change.expiring_policy_info.expiring_premium = expiring_data["cds"]["layers"][idx]["quoted_premium"]
        layer.rate_change.expiring_policy_info.expiring_written_line = expiring_data["cds"]["layers"][idx]["written_line"]
        layer.rate_change.expiring_policy_info.expiring_technical_premium = expiring_data["cds"]["layers"][idx]["technical_premium"]
        layer.rate_change.expiring_policy_info.expiring_benchmark_premium = expiring_data["cds"]["layers"][idx]["benchmark_premium"]
        layer.rate_change.expiring_policy_info.expiring_tpi = expiring_data["cds"]["layers"][idx]["tpi"]
        layer.rate_change.expiring_policy_info.expiring_bpi = expiring_data["cds"]["layers"][idx]["bpi"]

    # Populate other useful fields
    hxd.cds.standard_fields.insured_name = expiring_data["cds"]["standard_fields"]["insured_name"]
    hxd.cds.currencies.source_currency = expiring_data["cds"]["currencies"]["source_currency"]

# Rate Change
@hx.task
def rarc_task(hxd, progress):

    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Make sure expiring data is up to date TODO delete
    # expiring_policy_fetch_task(hxd, progress)

    # Get correct buckets based on coverage
    buckets = rate_change_buckets(hxd)

    data_schema_static_filename = "data_schema/data_schema_static_copy.py"
    data_schema_static_path = os.path.join(os.path.dirname(__file__), data_schema_static_filename)

    # Rate Change with offline_hxd
    rc = RateChangeLib(
        hxd=hxd,
        progress=progress,
        buckets=buckets,
        layers_path="cds/layers",
        expiring_actual_prem="quoted_premium",
        expiring_technical_prem="benchmark_premium",
        async_tasks=[],  # Pass the actual tasks, not strings
        data_schema_static_path=data_schema_static_path
    )

    rc.calculate_repriced_values(
        # expiring_policy_option_id=144560 # NOTE: for debugging if needed
    )

    # Use the repriced values to calculate the changes for each bucket
    rarc_df, rarc_list = rc.calculate_rarc_by_layer()
    
    # NOTE: for debugging if needed
    # pd.set_option('display.max_columns', None)
    # print(rarc_df)
    # print(rarc_list)

    # Push to hxd
    for rarc_layer, hxd_layer in zip(rarc_list, hxd.cds.layers):
        hxd_layer.rate_change.temp_storage = rarc_layer["temp_storage"]
        rarc_layer.pop("temp_storage")

        for key, value in rarc_layer.items():
            setattr(hxd_layer.rate_change, key, value)


# Generate policy document in Excel
@hx.task
def policy_to_excel_task(hxd, progress):
    cover = hxd.cds.cover_selection
    
    # Load string containing data
    data = json.loads(hxd.policy_doc.data_dict)

    # Get template based on cover
    template = None
    if cover.is_cargo:
        template = "cargo_template"
        if cover.is_cargo_cyber:
                template = "cargo_and_cargo_cyber_template"
    elif cover.is_cargo_cyber_dropdown:
        template = "cargo_cyber_template"
    elif cover.is_specie:
        template = "specie_template"
    elif cover.is_conloss:
        template = "conloss_template"

    if not template:
        hx.errors.fatal("No cover has been selected in Risk Information.")



    # Write the dictionary values to the Excel template
    template_path = f"./model/algorithms/policy_doc_templates/{template}.xlsx"
    # template_path = f"/workspace/editing/algorithms/policy_doc_templates/{template}.xlsx"
    # Load the workbook and select the active worksheet
    workbook = openpyxl.load_workbook(template_path)
    #sheet = workbook.active

    if (cover.is_cargo and cover.is_cargo_cyber):
        sheet_1 = workbook["Summary - Cargo"]
        sheet_2 = workbook["Summary - Cargo Cyber"]
        sheet_idx = workbook.sheetnames.index(sheet_2.title)   
        cargo_dict = {k: v for k, v in data.items() if not k.endswith("cyber")}
        cargo_cyber_dict = {k: v for k, v in data.items() if k.endswith("cyber")}
    else:
        sheet = workbook["Summary"]

    if template != "cargo_and_cargo_cyber_template":
    # Fill the named ranges with data
        for key, value in data.items():
            if key in workbook.defined_names:
                # Get the cell corresponding to the named range
                cells = workbook.defined_names[key].destinations
                for title, coord in cells:
                    if title == sheet.title:  # Ensure the named range is in the correct sheet
                        sheet[coord] = value
        # Protect the sheet to prevent changes
        sheet.protection.enable()
        sheet.protection.set_password(excel_password)
    else:
    # Fill the named ranges with data
        for key, value in cargo_dict.items():
            if key in workbook.defined_names:
                # Get the cell corresponding to the named range
                cells = workbook.defined_names[key].destinations
                for title, coord in cells:
                    if title == sheet_1.title:  # Ensure the named range is in the correct sheet
                        sheet_1[coord] = value        
        for key, value in cargo_cyber_dict.items():
            print(f"key value is {key}")
            if key in workbook.defined_names:
                # Get the cell corresponding to the named range
                cells = workbook.defined_names[key].destinations
                for title, coord in cells:
                    if title == sheet_2.title:  # Ensure the named range is in the correct sheet
                        sheet_2[coord] = value   
        # Protect the sheet to prevent changes
        sheet_1.protection.enable()
        sheet_1.protection.set_password(excel_password)    
        sheet_2.protection.enable()
        sheet_2.protection.set_password(excel_password)    

    # Save the filled template to a new file
    with hxd.policy_doc.output_file.open("b") as f:
        workbook.save(f)

    # Store task data to allow comparison if anything changes in rating
    hxd.policy_doc.task_data_dict = hxd.policy_doc.data_dict

@hx.task
def new_bug_report_task(hxd, progress):
    model_name = "Cargo"
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
def pass_pas_reference(hxd, progress):
    hx.meta.pas_references.clear()
    layer = hxd.cds.layers[0]
    eea_section_reference = layer.eea_section_reference.ref
    non_eea_section_reference = layer.non_eea_section_reference.ref
    single_section_reference = layer.single_section_reference.ref

    
    has_double_section_ref = layer.has_double_section_ref
    #append policy reference to PAS
    def is_valid(reference):
        return reference is not None and reference != ""
    if has_double_section_ref:
        if is_valid(eea_section_reference) :
            hx.meta.pas_references.append(eea_section_reference)
        if is_valid(non_eea_section_reference ):
            if non_eea_section_reference != eea_section_reference:
                hx.meta.pas_references.append(non_eea_section_reference)
    else:
        if is_valid(single_section_reference) :
            hx.meta.pas_references.append(single_section_reference)
    
    if hxd.cds.cover_selection.is_cargo_cyber:
        # Cyber Add on
        layer_cyber = layer.coverages.cargo_cyber_addon
        eea_section_reference_cyber_addon = layer_cyber.eea_section_reference.ref
        non_eea_section_reference_cyber_addon = layer_cyber.non_eea_section_reference.ref
        single_section_reference_cyber_addon = layer_cyber.single_section_reference.ref

        existing_refs = [eea_section_reference,non_eea_section_reference,single_section_reference ]
        #append the cyber addon policy reference
        if has_double_section_ref:
            if is_valid(eea_section_reference_cyber_addon) and (eea_section_reference_cyber_addon not in existing_refs) :
                hx.meta.pas_references.append(eea_section_reference_cyber_addon)
            if is_valid(non_eea_section_reference_cyber_addon ) and (non_eea_section_reference_cyber_addon not in existing_refs):
                if non_eea_section_reference_cyber_addon != eea_section_reference_cyber_addon:
                    hx.meta.pas_references.append(non_eea_section_reference_cyber_addon)
        else:
            if is_valid(single_section_reference_cyber_addon) and (single_section_reference_cyber_addon not in existing_refs):
                hx.meta.pas_references.append(single_section_reference_cyber_addon)   

@hx.task
def load_cargo_input(hxd,progress):
    cargo_transit_input_dict = ["transit_flag",	"wh_to_port_flag","excess","loading_flag","voyage_flag", "unloading_flag","port_to_wh_flag","commodity","trans_vals", "deductible_level","packaging","conv_air","conv_land", "conv_sea", "conv_air_factor", "conv_land_factor", "conv_sea_factor", "voyage","surveyor","vessel", "uw_discretion", "uw_discretion_factor", "type_of_cover","actual_rate"]
    cargo_storage_input_dict = ["storage_flag",	"stock_vals","excess","deductible_level",	"survey",	"risk_mgmt",	"risk_mgmt_factor",	"type_of_cover",	"uw_discretion",	"uw_discretion_factor",	"avg_val_pcm",	"cat_expo",	"cat_expo",	"retail_expo",	"retail_load",	"all_else_load",	"actual_rate"]
    ct = hxd.cds.layers[0].coverages.cargo_transit
    ct_cyber = hxd.cds.layers[0].coverages.cargo_cyber_transit
    cs = hxd.cds.layers[0].coverages.cargo_storage
    cs_cyber = hxd.cds.layers[0].coverages.cargo_cyber_storage

    #load the carge transit value to cargo cyber
    for name in cargo_transit_input_dict:
        input_value = getattr(ct,name)
        setattr(ct_cyber, name, input_value)
    #load the carge storage value to cargo cyber
    for name in cargo_storage_input_dict:
        input_value = getattr(cs,name)
        setattr(cs_cyber, name, input_value)
    #load the cargo storage value from the country list
    cs_country = cs.countries
    cs_cyber_country = cs_cyber.countries
    for item_cargo, item_cargo_cyber in zip(cs_country, cs_cyber_country):
        value_temp = getattr(item_cargo, "country")
        setattr(item_cargo_cyber, "country", value_temp)
        value_temp = getattr(item_cargo, "cat_expo")
        setattr(item_cargo_cyber, "cat_expo", value_temp)
    
    #load the brokerage and written line to Cargo Cyber Add On
    layer = hxd.cds.layers[0]
    layer_cyber = hxd.cds.layers[0].coverages.cargo_cyber_addon
    layer_cyber.brokerage = layer.brokerage
    layer_cyber.written_line = layer.written_line
   
    pass  