import hx
import os
import pandas as pd
import numpy as np
import requests
import json
from copy import deepcopy
from mailmerge import MailMerge
from algorithms import parameter_tables_schema as params
from datetime import timedelta, datetime
from algorithms.year_frac import basis1
from algorithms.rate_rate_change import rate_change_buckets
from algorithms.rate_constants import climate_country_dict, climate_endpoint, climate_industry_dict
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from libraries.rate_change.algorithms.rate_change import RateChange as RateChangeLib
import algorithms.rate_utilities as utils
from algorithms.async_capiq import capiq_fetch, populate_capiq_data
from algorithms.climate_documents.generate_climate_doc import generate_climate_doc
from algorithms.uw_rationale_document.generate_uw_rationale_doc import generate_uw_rationale_doc
from libraries.email_notification.algorithms.bug_report import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report
from algorithms.climate_documents.import_climate_docs import FeatherLoader
from datetime import date
from tempfile import NamedTemporaryFile

# Update example task below 
@hx.task
def example_empty_task(hxd, progress):
    pass

# Importing expiring policy for rate change
'''
Async task to import data from an expiring policy option for rate change calculation and analysis of movement.
Developers will need to update the task in two places, first for which variables from the expiring policy to import,
second to assign these to the current model variables.
'''

@hx.task
def expiring_policy_fetch_task(hxd, progress):
    '''
    Async task to import expiring data, from an expiring policy option for rate change calculation and analysis of movement.
    Rate change Expiry data are populated at a Layer level.
    NOTE: Developers will need to:
    - ensure the previous data schema is aligned to the current and 
    - verify the assignment of the Expiry node by changing the function assign_expiry_nodes_rate_change
    '''
    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id =  hxd.cds.rate_change.expiring_policy_option_id.selected # 395204 # NOTE: use hardcoded ID for debugging if needed
    expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False)

    if expiring_response.status_code != 200:
        raise Exception(expiring_response.json())

    expiring_data = expiring_response.json()["data"]

    expiring_data = align_data_schema_legacy_model_versions(hxd,expiring_data)
     
    # Get fields from json response and push to hxd
    expiring_layers_len = len(expiring_data["cds"]["layers"])
    layer_mapping = {}
    
    # Edit v0.3.0 Calculating annualising expiring factor
    hxd.cds.rate_change.expiring_inception_date  =  expiring_data["hx_core"]["inception_date"]
    hxd.cds.rate_change.expiring_expiry_date  = expiring_data["hx_core"]["expiry_date"]
    expiring_incept = hxd.cds.rate_change.expiring_inception_date # Date
    expiring_expiry = hxd.cds.rate_change.expiring_expiry_date # Date

    # NOTE: if 01/01/N - 31/12/N+1 is considered as one full year, use the below
    expiring_annualise = 1/ basis1(expiring_incept , expiring_expiry + timedelta(days=1)) or 0 
    # NOTE: if 01/01/N - 01/01/N+1 is considered as one full year, use the below
    # expiring_annualise = 1/ basis1(expiring_incept , expiring_expiry) or 0 

    for idx, layer in enumerate(hxd.cds.layers):
        # Throw error if expiring layer doesn't exist
        if isinstance(layer.rate_change.expiring_layer,int):
            if layer.rate_change.expiring_layer > expiring_layers_len:
                hx.errors.fatal(f"Expiring Layer {layer.rate_change.expiring_layer}, mapped to Renewal Layer {idx+1}, does not exist. Number of expiring layers is {expiring_layers_len}.")

        if hxd.cds.risk_information.mmp_flag is False:
            if layer.rate_change.expiring_layer is not None:
                # populate the expiry layer only if the layer is a renewing layer
                mapped_expiring_layer_idx = layer.rate_change.expiring_layer - 1
                assign_expiry_nodes_rate_change(
                    rc_source_data = expiring_data["cds"]["layers"][mapped_expiring_layer_idx], 
                    rc_data=layer.rate_change, 
                    annualise_factor= expiring_annualise)
                    
            # Save layer mapping
            layer_mapping[str(idx+1)] = layer.rate_change.expiring_layer
        else:
            mapped_expiring_layer_idx = 0
            assign_expiry_nodes_rate_change(
                rc_source_data = expiring_data["cds"]["layers"][mapped_expiring_layer_idx], 
                rc_data=layer.rate_change, 
                annualise_factor= expiring_annualise)
                    
            # Save layer mapping
            layer_mapping[str(idx+1)] = 1

    # save mapping before assigment
    hxd.cds.rate_change.layer_mapping = json.dumps(layer_mapping)
    
    # Confirm task has been run
    hxd.cds.rate_change.has_fetch_run = True
    hxd.cds.rate_change.has_fetch_not_run = False

    return (expiring_data)

@hx.task
def rarc_task(hxd, progress):
    """
    Calculate the rebased premium at LAYER level, for each bucket using the expiring policy and the temporary data schema (transient HXD).
    Store the results in the current data schema for each bucket.
    Additionally, store temporary results for data validation purposes. 
    This process utilises the rate change library for calculations and stores the results in the rate change library. 
    For fleet use, use library version 2.x instead of v1.X
    """
    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Make sure expiring data is up to date
    expiring_data = expiring_policy_fetch_task(hxd, progress)

    # NOTE: Align legacy Data Schema to current Data Schema to proceed to the import without issues.
    # Add new node and assign their value
    # Reassign exisiting node if there was a change in definition
    # Delete Node that are not present in the current data schema

    # Revalue expiring in renewing currency
    # Align the layers in number of layer in cds/large_cap/layers to the number in cds/layers before (10) sending it to the rate change library
    used_expiring_large_cap_layer = len(expiring_data["cds"]["large_cap"]["layers"])
    number_item_to_add = 10 - used_expiring_large_cap_layer
    expiring_data["cds"]["large_cap"]["layers"].extend([expiring_data["cds"]["large_cap"]["layers"][0]] * number_item_to_add)    

    
    # NOTE: Re-ordering the layers in the expiring schema such that they are mapped to the renewing layers based on the expiring layer input on the Rate Change page
    # This would normally be handled by the rate change library, but because the International D&O model does not use the standard inputs (cds/layers - limit; excess; deductible; etc.), 
    # the rate change library is unable to handle this case. 
    # Once the expiring_data dictionary is prepared to be passed to the rate change calculations, we explicitly rearrange the elements of the layers list in the order specified in the Rate Change page. 
    # This step is taken for both large cap and middle market renewing policies, in case the expiring policy is large cap. 
     
    layer_mapping = json.loads(hxd.cds.rate_change.layer_mapping)

    expiring_layers = expiring_data["cds"]["large_cap"]["layers"]
    n = len(expiring_layers)

    reordered_layers = [None] * n

    for i in range(n):
        idx = layer_mapping.get(str(i + 1))

        if idx is None:
            reordered_layers[i] = deepcopy(expiring_layers[i])
        else:
            reordered_layers[i] = deepcopy(expiring_layers[idx - 1])
    
    expiring_data["cds"]["large_cap"]["layers"] = reordered_layers

    # Get buckets 
    buckets = rate_change_buckets(hxd)

    data_schema_static_filename = "data_schema/data_schema_static_copy.py"
    data_schema_static_path = os.path.join(os.path.dirname(__file__), data_schema_static_filename)

    # fx rates
    fx_rates_df = params.fx_rates.df() # Using fx from library
    # fx_rates_df = hx.params.table_currency # Using fx from params

    # Capture the expiring_inputs_in_ccy information to revalue in case of change in currency at renewal
    # NOTE: Provide the path of the input value node and the corresponding currency
    expiring_inputs_in_ccy = [
        # (input_node_path,input_currency_node_path)
        # NOTE:, the inputs supplied in this list will be supplied to the rate change library, where the currency for the items will be iteratively updated for each layer. 
        # Therefore, only layer-specific inputs should be supplied (e.g. limits, excesses, etc.)
        ("cds/large_cap/layers/limit","cds/currencies/source_currency"),
        ("cds/large_cap/layers/excess","cds/currencies/source_currency"),
        ("cds/large_cap/layers/deductible","cds/currencies/source_currency"),
        ("cds/large_cap/layers/quoted_premium_100","cds/currencies/source_currency")
    ]

    expiring_inputs_in_ccy_non_layer = [
        # NOTE:, the inputs supplied in this list will have the currencies converted OUTSIDE of the rate change library. 
        # The items in this list should be non-layer specific inputs, e.g. total assets or other value fields which are do not vary by layer. 
        "cds/exposure/aggregate/market_cap_2_year_high",
        "cds/exposure/aggregate/current_market_cap",
        "cds/exposure/aggregate/total_assets",
        "cds/exposure/aggregate/ebit",
        "cds/exposure/aggregate/net_sales",
        "cds/exposure/aggregate/total_liabilities",
        "cds/exposure/aggregate/current_assets",
        "cds/exposure/aggregate/current_liabilities",
        "cds/exposure/aggregate/retained_earnings",
        "cds/mmp/dno/excess",
        "cds/mmp/dno/deductible",
        "cds/mmp/epl/excess",
        "cds/mmp/epl/deductible",
        "cds/mmp/cll/excess",
        "cds/mmp/cll/deductible",
        "cds/mmp/dno/limit",
        "cds/mmp/epl/limit",
        "cds/mmp/cll/limit",
    ]

    # Convert expiring values from expiring ccy to renewing ccy. Only for non-layer inputs. 
    # Layer values are converted in the rate change library. 
    # expiring_data is a python dictionary, not a HX object
    expiring_fx_usd_to_ccy = fx_rates_df[fx_rates_df["ccy"] == expiring_data["cds"]["currencies"]["source_currency"]]["fx_rate"].iloc[0]
    renewing_fx_usd_to_ccy = fx_rates_df[fx_rates_df["ccy"] == hxd.cds.currencies.source_currency]["fx_rate"].iloc[0]
    fx_exp_to_ren = renewing_fx_usd_to_ccy / expiring_fx_usd_to_ccy

    for path in expiring_inputs_in_ccy_non_layer:
        keys = path.split("/")
        d = expiring_data
        for key in keys[:-1]:
            d = d[key]

        last_key = keys[-1]
        if d[last_key]:
           d[last_key] = d[last_key] * fx_exp_to_ren 

    # Prepare arguments for calculate_repriced_values() function
    kw_args = {
        "expiring_inputs_in_ccy": expiring_inputs_in_ccy, # list of tuples
        "fx_table": fx_rates_df 

    }
    # Rate Change with transient_hxd
    rc = RateChangeLib(
        hxd=hxd,
        progress=progress,
        buckets=buckets,
        layers_path="cds/layers",
        expiring_actual_prem="quoted_premium_annual_100",
        expiring_technical_prem="benchmark_premium_annual_100", 
        expiring_currency="currency",
        async_tasks=[],  # Pass the actual tasks name as a variable, not a string
        data_schema_static_path=data_schema_static_path
    )

    # for input_path, _ in expiring_inputs_in_ccy:
    #     set_none_to_zero_at_path(expiring_data, input_path)


    rc.calculate_repriced_values(
        # expiring_policy_option_id=1161580 # NOTE: for debugging if needed
        expiring_data = expiring_data, # NOTE: this allows to use the expiry data with aligned Data Schema
        **kw_args
    )


    # Use the repriced values to calculate the changes for each bucket
    rarc_df, rarc_list = rc.calculate_rarc_by_layer()

    if hxd.cds.risk_information.mmp_flag is False:
        num_layers = len(hxd.cds.large_cap.layers)
    else:
        num_layers = 1

    rarc_df = rarc_df[:num_layers]
    rarc_list = rarc_list[:num_layers]

  
    # # # NOTE: for debugging if needed
    # pd.set_option('display.max_columns', None)
    # print(rarc_df)
    # print(rarc_list)

    # Calculate brokerage change for storage but not display
    for layer in hxd.cds.layers:
        if layer.rate_change.expiring_layer is not None or hxd.cds.risk_information.mmp_flag is True:
            expiring_brokerage = layer.rate_change.expiring_policy_info.expiring_brokerage or 0
            renewal_brokerage = layer.brokerage or 0
            layer.rate_change.brokerage_change.model_calculated = (1 - expiring_brokerage) / (1 - renewal_brokerage)

    # Push to hxd
    for rarc_layer, hxd_layer in zip(rarc_list, hxd.cds.layers):
        hxd_layer.rate_change.temp_storage = rarc_layer["temp_storage"]
        rarc_layer.pop("temp_storage")

        # Only populate bucket change for Renewing Layer. No calculation for New Layer.
        if hxd_layer.rate_change.expiring_layer is not None or hxd.cds.risk_information.mmp_flag is True: # EDIT v0.2.4.2-Dev
            for key, value in rarc_layer.items():
                setattr(hxd_layer.rate_change, key, value)

            # NOTE: ONLY for legacy model. NOt necessary for a first build. Assignment in tasks instead of rating (rate_rate_change(hxd)) to clear out the overrides at the creation of the renewal
            for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
                rc_vbl = getattr(hxd_layer.rate_change, item)
                rc_vbl.uw_selected.calculated = rc_vbl.model_calculated
            
    # Confirm task has been run
    hxd.cds.rate_change.has_rarc_run = True
    hxd.cds.rate_change.has_rarc_not_run = False


@hx.task
def start_renewal_task(hxd, progress):
   
    # The following statement checks that the expiring information has been imported for renewals. Some teams might want to start
    # from a blank rater each time, in which case update the below
    if not hxd.cds.standard_fields.insured_name:
        hxd.model_state.landing_page_info = "❗❗ FAILED: Click 'Undo' then 'Import Expiring Policy Data' in the top right corner ❗❗"
    else:
        hxd.model_state.pressed_start_renewal_task = True

        # Initialise the hx_renew_api library
        hx_renew = init_hx_renew_api()

        # Get expiring policy data
        expiring_policy_option_id = hx.meta.expiring_policy_option_id  
        expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False)

        if expiring_response.status_code != 200:
            raise Exception(expiring_response.json())

        expiring_data = expiring_response.json()["data"]

        # Setting Renewal Indicator to True
        hxd.cds.standard_fields.is_renewal = True
        hxd.cds.capiq_search_complete = False

        # Clearing Section References and Status to avoid duplication and user error
        for i, layer in enumerate(hxd.cds.large_cap.layers):
            layer.section_reference = None

            if expiring_data["cds"]["large_cap"]["layers"][i]["status"] == "Bound":
                layer.status = "Submission"
            else:
                layer.status = None
                
        hxd.cds.mmp.total.section_reference = None

        if expiring_data["cds"]["mmp"]["total"]["status"] == "Bound":
            hxd.cds.mmp.total.status = "Submission"
        else:
            hxd.cds.mmp.total.status = None       

        # Applying Expiring Comments for Rating Summary MMP
        hxd.cds.mmp.dno.expiring_appetite_comment = expiring_data["cds"]["mmp"]["dno"]["appetite_comment"]
        hxd.cds.mmp.epl.expiring_appetite_comment = expiring_data["cds"]["mmp"]["epl"]["appetite_comment"]
        hxd.cds.mmp.cll.expiring_appetite_comment = expiring_data["cds"]["mmp"]["cll"]["appetite_comment"]


@hx.task
def capiq_fetch_task(hxd, progress):
    capiq_fetch(hxd, progress)
    pass

@hx.task
def populate_capiq_data_task(hxd, progress):
    populate_capiq_data(hxd, progress)
    pass

@hx.task
def save_uw_to_pas_reference(hxd, progress):
    pas_reference = hxd.cds.standard_fields.insured_name
    hx.meta.pas_references.clear()
    hx.meta.pas_references.append(pas_reference)


@hx.task
def generate_climate_doc_task(hxd, progress):
    country = hxd.cds.risk_information.climate_document_country
    industry = hxd.cds.risk_information.climate_document_industry
    loader = FeatherLoader(endpoint=climate_endpoint)

    try:
        relative_path = climate_country_dict[country] + climate_industry_dict[industry]
    except KeyError as exc:
        hx.errors.fatal(f"No template configured for country '{country}'")
        raise exc

    doc = loader.load_word_document(relative_path)

    with NamedTemporaryFile(suffix=".docx") as tmp:
        doc.save(tmp.name)
        document = MailMerge(tmp.name)

        document.merge(
            insured_name=str(hxd.cds.standard_fields.insured_name or ""),
            date=date.today().strftime("%d %B %Y")
        )

        with hxd.cds.risk_information.climate_document.open("b") as f:
            document.write(f)

    progress.update(1.0)


@hx.task
def generate_uw_rationale_doc_task(hxd, progress):
    generate_uw_rationale_doc(hxd, progress)


def assign_expiry_nodes_rate_change(rc_source_data, rc_data, annualise_factor): # Edit v0.2.4.1-Dev
    """
    This function assigns values to expiring rate change nodes, including the renewal premium at 100 percent for Beazley, policy term, and annualised. 
    It also populates table nodes with details such as limit, deductible, excess, and brokerage and the expiring policy information

    """
    # Expiring info
    # rc_data.expiring_policy_info.expiring_exposure =    
    rc_data.expiring_policy_info.expiring_policy_length = 12/annualise_factor or 12
    rc_data.expiring_policy_info.expiring_quoted_premium_100 = rc_source_data["quoted_premium_100"]    
    rc_data.expiring_policy_info.expiring_quoted_premium_annual_100 = rc_source_data["quoted_premium_annual_100"]
    rc_data.expiring_policy_info.expiring_limit = rc_source_data["limit"]
    rc_data.expiring_policy_info.expiring_excess = rc_source_data["excess"]    
    rc_data.expiring_policy_info.expiring_deductible = rc_source_data["deductible"]
    rc_data.expiring_policy_info.expiring_brokerage = rc_source_data["brokerage"] or 0
    rc_data.expiring_policy_info.expiring_written_line = expiring_written_line  = rc_source_data["written_line"] or 0  
    rc_data.expiring_policy_info.expiring_expected_loss_100 = rc_source_data["expected_loss_cost_100"]
    rc_data.expiring_policy_info.expiring_section_reference = rc_source_data["section_reference"]
    rc_data.expiring_policy_info.expiring_benchmark_premium_100 = rc_source_data["benchmark_premium_100"]
    # rc_data.expiring_policy_info.expiring_benchmark_premium_post_uw_adj_100 = rc_source_data["benchmark_premium_post_uw_adj_100"] 
    rc_data.expiring_policy_info.expiring_bpi = rc_source_data["bpi"]
    rc_data.expiring_policy_info.expiring_currency = rc_source_data["currency"]
    rc_data.expiring_policy_info.expiring_market_cap = rc_source_data["market_cap"]
    rc_data.expiring_policy_info.expiring_total_assets = rc_source_data["total_assets"]
    rc_data.expiring_policy_info.expiring_insider_share = rc_source_data["insider_share"]
    rc_data.expiring_policy_info.expiring_mmp_flag = rc_source_data["mmp_flag"]
    rc_data.expiring_policy_info.expiring_employees = rc_source_data["number_employees"]

    return



def set_none_to_zero_at_path(data, path):
    """
    Replace None with 0 specified by a slash-separated path.
    If any list is encountered along the path, apply recursively to each element.
    """
    keys = path.split("/")

    def _set(node, idx):
        # If we ran out of keys, nothing to set
        if idx >= len(keys):
            return

        key = keys[idx]

        if isinstance(node, dict):
            next_node = node.get(key, None)

            # If this is the leaf key, set only if None
            if idx == len(keys) - 1:
                if next_node is None:
                    node[key] = 0
                # else leave existing value as-is
                return

            # If missing intermediate dict, nothing to do safely
            if next_node is None:
                return

            # Recurse into the next level
            _set(next_node, idx + 1)

        elif isinstance(node, list):
            # Recurse into each element with the same remaining keys
            for elem in node:
                _set(elem, idx)

        # If node is neither dict nor list, path is invalid at this point; do nothing

    _set(data, 0)


def align_data_schema_legacy_model_versions(hxd,expiring_data):
    # NOTE: Align legacy Data Schema to current Data Schema to proceed to the import without issues.
    # - Add new node and assign their value
    # - Reassign existing node if there was a change in definition
    # - Delete Node that are not present in the current data schema

    for idx_layer, layer in enumerate(expiring_data["cds"]["layers"]):
        # check if expiring poi is from a all inputs model, if so, delete uw_selected node as it would be equal to None
        if not isinstance(expiring_data["cds"]["layers"][idx_layer]["rate_change"]["brokerage_change"]["uw_selected"], dict):

            expiring_data["cds"]["layers"][idx_layer]["rate_change"]["brokerage_change"]["uw_selected"]= {
                        "calculated": expiring_data["cds"]["layers"][idx_layer]["rate_change"]["brokerage_change"]["uw_selected"],
                    }
            expiring_data["cds"]["layers"][idx_layer]["rate_change"]["exposure_change"]["uw_selected"]={
                        "calculated": expiring_data["cds"]["layers"][idx_layer]["rate_change"]["exposure_change"]["uw_selected"],
                    }
            expiring_data["cds"]["layers"][idx_layer]["rate_change"]["risk_characteristics_change"]["uw_selected"]={
                        "calculated": expiring_data["cds"]["layers"][idx_layer]["rate_change"]["risk_characteristics_change"]["uw_selected"],
                    }
            expiring_data["cds"]["layers"][idx_layer]["rate_change"]["deductible_change"]["uw_selected"]={
                        "calculated": expiring_data["cds"]["layers"][idx_layer]["rate_change"]["deductible_change"]["uw_selected"],
                    }
            expiring_data["cds"]["layers"][idx_layer]["rate_change"]["limit_change"]["uw_selected"]={
                        "calculated": expiring_data["cds"]["layers"][idx_layer]["rate_change"]["limit_change"]["uw_selected"],
                    }
            expiring_data["cds"]["layers"][idx_layer]["rate_change"]["terms_conditions_change"]["uw_selected"]={
                        "calculated": expiring_data["cds"]["layers"][idx_layer]["rate_change"]["terms_conditions_change"]["uw_selected"],
                    }
            expiring_data["cds"]["layers"][idx_layer]["rate_change"]["other_change"]["uw_selected"]={
                        "calculated": expiring_data["cds"]["layers"][idx_layer]["rate_change"]["other_change"]["uw_selected"],
                    }
        
        # 202602 - cds/layers/market_cap was originally set up to use 2-year MC, but this has been updated to use the max or current MC or 2-year high MC
        expiring_data["cds"]["layers"][idx_layer]["market_cap"] = max(
            expiring_data["cds"]["exposure"]["aggregate"]["market_cap_2_year_high"] or 0,
            expiring_data["cds"]["exposure"]["aggregate"]["current_market_cap"] or 0
        )
    return expiring_data


@hx.task
def generate_tags(hxd, progress):
    # Tags for Underwriter, Broker, CountryOfDomicile, Industry, SubIndustry
    tag_fields = {
        'Underwriter': hxd.cds.standard_fields.underwriter,
        'Broker': hxd.cds.standard_fields.broker,
        'Insured': hxd.cds.standard_fields.insured_name
    }

    new_tags = []
    tag_fields_error = []

    # Validate and generate tags
    for label, value in tag_fields.items():
        if value:
            new_tags.append(value.replace(" ", ""))
        else:
            tag_fields_error.append(label)

    # Set policy tags or error message
    if tag_fields_error:
        msg_string = 'Error saving policy tags - Please select: ' + ', '.join(tag_fields_error)
        hx.errors.validation(msg_string)
        hxd.cds.is_policy_tag_error = True
        hxd.cds.policy_tag_msg = msg_string
    else:
        hx.meta.policy_tags = new_tags
        hxd.cds.is_policy_tag_error = False
        hxd.cds.policy_tag_msg = "Success!"

@hx.task
def new_bug_report_task(hxd, progress):
    model_name = "International D&O"
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