# v0.3.0
import hx, os, json, requests, openpyxl
import pandas as pd
from algorithms.rate_rate_change import RATE_CHANGE_BUCKETS, EXP_INPUTS_IN_CCY # Edit v0.3.0
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from libraries.rate_change.algorithms.rate_change import RateChange as RateChangeLib
import datetime
from algorithms.year_frac import basis1 # Edit v0.3.0 Import from year_frac to replicate yearfrac function, basis 1
from algorithms.rate_utilities import policy_term
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import COVERAGES_LIST
from algorithms import parameter_tables_schema as params
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import policy
from email.generator import BytesGenerator
from email import encoders
from email.mime.base import MIMEBase
import unicodedata
import io



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

        # Clear Section References and Status to avoid duplication and user error
        hxd.cds.primary.section_reference = None
        hxd.cds.primary.status = None
        for layer in hxd.cds.layers:
            layer.section_reference_view = None
            layer.status_view = None

        # Clear quoted and bound premium
        for option in hxd.cds.options:
            option.quoted_premium = None
        hxd.cds.primary.bound_premium_input = None
        for layer in hxd.cds.layers:
            layer.quoted_premium_view = None
            layer.bound_premium = None

        # Add tasks which must be done before starting a policy here >>
    rc = hxd.cds.rate_change
    rc.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id # Assigning this node in this tasks allows to clear the override at the creation of a renewal
        


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

    # NOTE: Align legacy Data Schema to current Data Schema to proceed to the import without issues.
    # - Add new node and assign their value
    # - Reassign existing node if there was a change in definition
    # - Delete Node that are not present in the current data schema
     
    # Get fields from json response and push to hxd
    expiring_layers_len = len(expiring_data["cds"]["layers"])
    layer_mapping = {}
    
    # Edit v0.3.0 Calculating annualising expiring factor
    hxd.cds.rate_change.expiring_inception_date  =  expiring_data["hx_core"]["inception_date"]
    hxd.cds.rate_change.expiring_expiry_date  = expiring_data["hx_core"]["expiry_date"]
    expiring_incept = hxd.cds.rate_change.expiring_inception_date # Date
    expiring_expiry = hxd.cds.rate_change.expiring_expiry_date # Date

    # NOTE: if 01/01/N - 31/12/N+1 is considered as one full year, use the below
    expiring_annualise = 1/ basis1(expiring_incept , expiring_expiry + datetime.timedelta(days=1)) or 0 
    # NOTE: if 01/01/N - 01/01/N+1 is considered as one full year, use the below
    # expiring_annualise = 1/ basis1(expiring_incept , expiring_expiry) or 0 

    for idx, layer in enumerate(hxd.cds.layers):
        # Throw error if expiring layer doesn't exist
        if isinstance(layer.rate_change.expiring_layer,int):
            if layer.rate_change.expiring_layer > expiring_layers_len:
                hx.errors.fatal(f"Expiring Layer {layer.rate_change.expiring_layer}, mapped to Renewal Layer {idx+1}, does not exist. Number of expiring layers is {expiring_layers_len}.")

        if layer.rate_change.expiring_layer is not None:
            # populate the expiry layer only if the layer is a renewing layer
            mapped_expiring_layer_idx = layer.rate_change.expiring_layer - 1
            assign_expiry_nodes_rate_change(
                rc_source_data = expiring_data["cds"]["layers"][mapped_expiring_layer_idx], 
                rc_data=layer.rate_change, 
                annualise_factor= expiring_annualise)
                
        # Save layer mapping
        layer_mapping[str(idx+1)] = layer.rate_change.expiring_layer

    # save mapping before assigment
    hxd.cds.rate_change.layer_mapping = json.dumps(layer_mapping)
    
    # Confirm task has been run
    hxd.cds.rate_change.has_fetch_run = True
    hxd.cds.rate_change.has_fetch_not_run = False

    return (expiring_data)


@hx.task
def rarc_task(hxd, progress):
    """
    Calculate the rebased premium at a LAYER level, for each bucket using the expiring policy and the temporary data schema (transient HXD).
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

    # Get buckets 
    buckets = RATE_CHANGE_BUCKETS
    data_schema_static_filename = "data_schema/data_schema_static_copy.py"
    data_schema_static_path = os.path.join(os.path.dirname(__file__), data_schema_static_filename)

    # Get the expiring_inputs_in_ccy information to revalue in case of change in currency at renewal
    # NOTE: Provide the path of the input value node and the corresponding currency
    expiring_inputs_in_ccy = EXP_INPUTS_IN_CCY["layers"]
    fx_rates_df = params.fx_rates.df() # Using fx from library
    # fx_rates_df = hx.params.table_currency # Using fx from params

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

    rc.calculate_repriced_values(
        # expiring_policy_option_id=1161580 #129400 # NOTE: for debugging if needed
        expiring_data = expiring_data, # NOTE: this allows to use the expiry data with aligned Data Schema
        **kw_args
    )

    # Use the repriced values to calculate the changes for each bucket
    rarc_df, rarc_list = rc.calculate_rarc_by_layer()
    
    # # NOTE: for debugging if needed
    # pd.set_option('display.max_columns', None)
    # print(rarc_df)
    # print(rarc_list)

    # Calculate brokerage change for storage but not display
    for layer in hxd.cds.layers:
        if layer.rate_change.expiring_layer is not None:
            expiring_brokerage = layer.rate_change.expiring_policy_info.expiring_brokerage or 0
            renewal_brokerage = layer.brokerage or 0
            layer.rate_change.brokerage_change.model_calculated = (1 - expiring_brokerage) / (1 - renewal_brokerage)

    # Push to hxd
    for rarc_layer, hxd_layer in zip(rarc_list, hxd.cds.layers):
        hxd_layer.rate_change.temp_storage = rarc_layer["temp_storage"]
        rarc_layer.pop("temp_storage")

        # Only populate bucket change for Renewing Layer. No calculation for New Layer.
        if hxd_layer.rate_change.expiring_layer is not None: # EDIT v0.3.0
            for key, value in rarc_layer.items():
                setattr(hxd_layer.rate_change, key, value)

            # NOTE: ONLY for legacy model. NOt necessary for a first build. 
            # Assignment in tasks instead of rating (rate_rate_change(hxd)) to clear out the overrides at the creation of the renewal
            for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
                rc_vbl = getattr(hxd_layer.rate_change, item)
                rc_vbl.uw_selected.calculated = rc_vbl.model_calculated
            
    # Confirm task has been run
    hxd.cds.rate_change.has_rarc_run = True
    hxd.cds.rate_change.has_rarc_not_run = False

def assign_expiry_nodes_rate_change(rc_source_data, rc_data, annualise_factor): # Edit v0.3.0
    """
    This function assigns values to expiring rate change nodes, including the renewal premium at 100 percent for Beazley, policy term, and annualised. 
    It also populates table nodes with details such as limit, deductible, excess, and brokerage and the expiring policy information

    """
    # Expiring info
    # rc_data.expiring_policy_info.expiring_exposure =    
    rc_data.expiring_policy_info.expiring_policy_length = 12/annualise_factor or 12
    rc_data.expiring_policy_info.expiring_quoted_premium_100 = rc_source_data["quoted_premium_100"]    
    rc_data.expiring_policy_info.expiring_quoted_premium_annual_100 = rc_source_data["quoted_premium_annual_100"]
    rc_data.expiring_policy_info.expiring_aggregate_limit = rc_source_data["aggregate_limit"]
    # rc_data.expiring_policy_info.expiring_excess = rc_source_data["excess"]    
    rc_data.expiring_policy_info.expiring_attachment = rc_source_data["attachment"] # deductible
    rc_data.expiring_policy_info.expiring_brokerage = rc_source_data["brokerage"] or 0
    rc_data.expiring_policy_info.expiring_written_line = expiring_written_line  = rc_source_data["written_line"] or 0  
    rc_data.expiring_policy_info.expiring_expected_loss_100 = rc_source_data["expected_loss_cost_100"]
    rc_data.expiring_policy_info.expiring_section_reference = rc_source_data["section_reference"]
    rc_data.expiring_policy_info.expiring_benchmark_premium_100 = rc_source_data["benchmark_premium_100"]
    # rc_data.expiring_policy_info.expiring_benchmark_premium_post_uw_adj_100 = rc_source_data["benchmark_premium_post_uw_adj_100"] 
    rc_data.expiring_policy_info.expiring_bpi = rc_source_data["bpi"]
    rc_data.expiring_policy_info.expiring_currency = rc_source_data["currency"]
    
    return

# Importing expiring policy info for rate change
@hx.task
def expiring_policy_fetch_coverages_task(hxd, progress):
    '''
    Async task to import Expiring data, from an expiring policy option for rate change calculation and analysis of movement.
    Rate change Expiry data are populated at a Layer level.
    Developers will need to:
    - ensure the previous data schema is aligned to the current and 
    - verify the assignment of the Expiry node by changing the fuction assign_expiry_nodes_rate_change
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

    # NOTE: Align legacy Data Schema to current Data Schema to proceed to the import without issues.
    # Add new node and assign their value
    # Reassign exisiting node if there was a change in definition
    # Delete Node that are not present in the current data schema
   
    # Get fields from json response and push to hxd
    expiring_layers_len = len(expiring_data["cds"]["layers"])
    layer_mapping = {}
    
    # Edit v0.3.0 Calculating annualising expiring factor
    hxd.cds.rate_change.expiring_inception_date  =  expiring_data["hx_core"]["inception_date"]
    hxd.cds.rate_change.expiring_expiry_date  = expiring_data["hx_core"]["expiry_date"]
    expiring_incept = hxd.cds.rate_change.expiring_inception_date # Date
    expiring_expiry = hxd.cds.rate_change.expiring_expiry_date # Date


    # NOTE: if 01/01/N - 31/12/N+1 is considered as one full year, use the below
    expiring_annualise = 1/ basis1(expiring_incept , expiring_expiry + datetime.timedelta(days=1)) or 0 
    # NOTE: if 01/01/N - 01/01/N+1 is considered as one full year, use the below
    # expiring_annualise = 1/ basis1(expiring_incept , expiring_expiry) or 0 

    for idx, layer in enumerate(hxd.cds.layers):
        # Error message if expiring layer doesn't exist
        if isinstance(layer.rate_change.expiring_layer,int):
            if layer.rate_change.expiring_layer > expiring_layers_len:
                hx.errors.fatal(f"Expiring Layer {layer.rate_change.expiring_layer}, mapped to Renewal Layer {idx+1}, does not exist. Number of expiring layers is {expiring_layers_len}.")

        if layer.rate_change.expiring_layer is not None:
            mapped_expiring_layer_idx = layer.rate_change.expiring_layer - 1

            for coverage in COVERAGES_LIST:
                assign_expiry_nodes_rate_change(\
                    rc_source_data = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["coverages"][coverage], \
                    rc_data = getattr(layer.rate_change,coverage),\
                    annualise_factor= expiring_annualise)
        # Save layer mapping
        layer_mapping[str(idx+1)] = layer.rate_change.expiring_layer

    hxd.cds.rate_change.layer_mapping = json.dumps(layer_mapping)

    # Confirm task has been run
    hxd.cds.rate_change.has_fetch_run = True
    hxd.cds.rate_change.has_fetch_not_run = False
    return (expiring_data)

@hx.task
def rarc_task_coverages(hxd, progress):
    """
    Calculate the rebased premium at COVERAGE level, for each bucket using the expiring policy and the temporary data schema (transient HXD).
    Store the results in the current data schema for each bucket.
    Additionally, store temporary results for data validation purposes. 
    This process utilises the rate change library for calculations and stores the results in the rate change library. 
    For fleet use, use library version 2.x instead of v1.X
    """
    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Make sure expiring data is up to date
    expiring_data = expiring_policy_fetch_coverages_task(hxd, progress)

    # NOTE: Align legacy Data Schema to current Data Schema to proceed to the import without issues.
    # Add new node and assign their value
    # Reassign exisiting node if there was a change in definition
    # Delete Node that are not present in the current data schema

    # Get correct buckets based on coverage
    data_schema_static_filename = "data_schema/data_schema_static_copy.py"
    data_schema_static_path = os.path.join(os.path.dirname(__file__), data_schema_static_filename)

    # NOTE: Provide the path of the input value node and the corresponding currency
    fx_rates_df = params.fx_rates.df() # NOTE: if using fx from library
    # fx_rates_df = hx.params.table_currency # NOTE: if using fx from params

    rc_result={}

    for coverage in COVERAGES_LIST:
        # Get the rate change buckets based on the coverage name
        buckets = RATE_CHANGE_BUCKETS[coverage]
        # Get the expiring_inputs_in_ccy information to revalue in case of change in currency at renewal
        expiring_inputs_in_ccy_cvg = EXP_INPUTS_IN_CCY[coverage]
        # Prepare arguments for calculate_repriced_values() function
        kw_args = {
            "expiring_inputs_in_ccy": expiring_inputs_in_ccy_cvg, # list of tuples
            "fx_table": fx_rates_df 
        }

        # Rate Change with transient_hxd
        rc = RateChangeLib(
            hxd=hxd,
            progress=progress,
            buckets=buckets,
            layers_path=f"cds/layers",
            expiring_actual_prem=f"coverages/{coverage}/quoted_premium_annual_100",
            expiring_technical_prem=f"coverages/{coverage}/benchmark_premium_annual_100",
            expiring_currency=f"coverages/{coverage}/currency",
            async_tasks=[],
            data_schema_static_path=data_schema_static_path
        )

        rc.calculate_repriced_values(#expiring_data=[expiring_data] # when using 2.3 library
            expiring_data = expiring_data, # NOTE: this allows to use the expiry data with aligned Data Schema
            **kw_args
        )
        # Use the repriced values to calculate the changes for each bucket
        rc_result[f'{coverage}_rarc_df'], rc_result[f'{coverage}_rarc_list'] = rc.calculate_rarc_by_layer()
        
        # # NOTE: for debugging if needed
        # pd.set_option('display.max_columns', None)
        # print(rc_result[f'{coverage}_rarc_df'])
        # print(rc_result[f'{coverage}_rarc_list'])

    # Push to hxd
    for coverage in COVERAGES_LIST:
        for rarc_layer, hxd_layer in zip(rc_result[f'{coverage}_rarc_list'] , hxd.cds.layers):
            getattr(hxd_layer.rate_change, coverage).temp_storage = rarc_layer["temp_storage"]
            rarc_layer.pop("temp_storage")

            if hxd_layer.rate_change.expiring_layer is not None==True:
                # populate bucket change for Renewing Layer. No calculation for New Layer.
                for key, value in rarc_layer.items():
                    setattr(getattr(hxd_layer.rate_change, coverage), key, value)
                # Calculate brokerage change for storage but not display
                expiring_brokerage = getattr(hxd_layer.rate_change, coverage).expiring_policy_info.expiring_brokerage or 0
                renewal_brokerage = getattr(getattr(hxd_layer, "coverages"), coverage).brokerage or 0
                brokerage_change = (1 - expiring_brokerage) / (1 - renewal_brokerage)
                getattr(hxd_layer.rate_change, coverage).brokerage_change.model_calculated = brokerage_change

            # NOTE: ONLY for legacy model. Not necessary for a first build. 
            # Assignment in tasks instead of rating (rate_rate_change(hxd)) to clear out the overrides at the creation of the renewal
            for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
                rc_vbl = getattr(getattr(hxd_layer.rate_change, coverage), item)
                rc_vbl.uw_selected.calculated = rc_vbl.model_calculated

    # Confirm task has been run
    hxd.cds.rate_change.has_rarc_run = True
    hxd.cds.rate_change.has_rarc_not_run = False

# Generate policy document in Excel
@hx.task
def policy_to_excel_task(hxd, progress):    
    from openpyxl.utils.cell import coordinate_to_tuple
    
    # Load string containing data
    data = json.loads(hxd.policy_doc.data_dict)

    # Format UW comments
    if data["uw_comments"] is not None:
        uw_notes = data["uw_comments"]
        formatted_notes = uw_notes.replace('<div>','\n').replace('</div>','')
        data["uw_comments"] = formatted_notes

    # Write the dictionary values to the Excel template
    template_path = f"./model/algorithms/policy_document_template.xlsx"

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




# Generate policy document in Email
@hx.task
def generate_email_task(hxd, progress):    
    insured_name = hxd.cds.standard_fields.insured_name or "TEST TEST TEST" # NOTE: can remove the "or" condition, it's just to always have it populated
    underwriter = hxd.cds.standard_fields.underwriter
    formatted_underwriter = underwriter.replace(" ", ".").lower() if underwriter is not None else "TEST"
    underwriter_email = formatted_underwriter + "@beazley.com"
    hxd.cds.email.sender = underwriter_email
    hxd.cds.email.recipient = underwriter_email

    def normalize_name(name):
        return unicodedata.normalize('NFKD', name) \
            .encode('ascii', 'ignore') \
            .decode('ascii')

    # Create the email message
    msg = MIMEMultipart("mixed")
    msg["Subject"] = f"Rationale email - {insured_name}"
    msg["From"] = normalize_name(hxd.cds.email.sender) 
    msg["To"] = normalize_name(hxd.cds.email.recipient)

    html_content = hxd.cds.email.data_dict

    # Attach the HTML content to the email
    msg.attach(MIMEText(html_content, "html"))

    # Write the dictionary values to the Excel template
    from openpyxl.utils.cell import coordinate_to_tuple
    
    # Load string containing data
    data = json.loads(hxd.policy_doc.data_dict)

    # Format UW comments
    if data["uw_comments"] is not None:
        uw_notes = data["uw_comments"]
        formatted_notes = uw_notes.replace('<div>','\n').replace('</div>','')
        data["uw_comments"] = formatted_notes

    # Write the dictionary values to the Excel template   
    template_path = f"./model/algorithms/policy_document_template.xlsx"

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

    file_name ="Policy_Summary.xlsx"
    with hxd.policy_doc.output_file.open("b") as f:
        excel_buffer = io.BytesIO()
        workbook.save(excel_buffer)
        excel_buffer.seek(0)  # Reset buffer pointer to the beginning

        # 2. Setup the MIME attachment
        file_name = "Policy_Summary.xlsx"
        part = MIMEBase("application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        part.set_payload(excel_buffer.read())

        # 3. Encode and add headers
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{file_name}"',
        )
        msg.attach(part)

    # Save the email as an .eml file
    with hxd.cds.email.rationale_file.open("b") as file:
        gen = BytesGenerator(file, policy=policy.default)
        gen.flatten(msg)
        hxd.cds.email.show_download = True

    pass
