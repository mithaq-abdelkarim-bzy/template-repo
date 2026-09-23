import hx, os, json, requests, openpyxl, json
import pandas as pd
from algorithms.rate_rate_change import rate_change_buckets
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from libraries.rate_change.algorithms.rate_change import RateChange as RateChangeLib
import itertools
from openpyxl.utils.cell import coordinate_to_tuple
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from libraries.email_notification.algorithms.bug_report import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report
import algorithms.rate_constants as const


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

        # Set the inception date back one day
        hxd.hx_core.inception_date = hxd.hx_core.inception_date - timedelta(days=1)
        


@hx.task
def set_expiry_date_to_one_year(hxd,progress):
    hxd.hx_core.expiry_date = hxd.hx_core.inception_date + relativedelta(years=1)
        



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
        layer.rate_change.premium.line_100pct.annualised.expiring = expiring_premium = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["quoted_premium"]
        expiring_written_line = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["written_line"] or 0
        layer.rate_change.premium.beazley_line.annualised.expiring = expiring_premium * expiring_written_line
        # NOTE: ... Add expiring fields as required here

        # Save layer mapping
        layer_mapping[str(idx+1)] = layer.rate_change.expiring_layer

    hxd.cds.rate_change.layer_mapping = json.dumps(layer_mapping)

    # Confirm task has been run
    hxd.cds.rate_change.has_fetch_run = True
    hxd.cds.rate_change.has_fetch_not_run = False
    return expiring_data


@hx.task
def rarc_task(hxd, progress):

    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Make sure expiring data is up to date
    expiring_data = expiring_policy_fetch_task(hxd, progress)

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
        expiring_actual_prem="quoted_premium_annualised",
        expiring_technical_prem="benchmark_premium_annualised",
        async_tasks=[],  # Pass the actual tasks, not strings
        data_schema_static_path=data_schema_static_path
    )

    [layer.get("sublimits", {}).pop(key, None) for layer in expiring_data.get("cds", {}).get("layers", []) for key in ["animal_dropdown_options", "diving_board_dropdown_options", "trampoline_dropdown_options", "swimming_pool_dropdown_options"] if layer.get("sublimits", {}).get(key) == []]
    
    rc.calculate_repriced_values(
       expiring_data = expiring_data # expiring_policy_option_id=129400 # NOTE: for debugging if needed
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

    # Confirm task has been run
    hxd.cds.rate_change.has_rarc_run = True
    hxd.cds.rate_change.has_rarc_not_run = False






# Generate policy document in Excel
@hx.task
def policy_to_excel_task(hxd, progress):    
    
    # Load string containing data
    data = json.loads(hxd.policy_doc.data_dict)

    # Write the dictionary values to the Excel template
    template_path = f"./model/algorithms/example_document_template.xlsx"

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


def get_peril_value(table, state, county, column, default=True):
    """Returns True/False for a peril based on the table lookup."""
    row = table[(table['State Code'] == state) & (table['County'] == county)]
    if not row.empty and column in row:
        return row[column].map({'Include': True, 'Exclude': False}).iloc[0]
    return default  # Default to True if no match is found

import itertools
import hx

@hx.task
def generate_recommended_peril_inclusions(hxd, progress):
    """
    Generate the recommended inclusions for the perils covered table.
    """

    rf = hxd.cds.rating_factors
    state, county = rf.state, rf.county
    pl = rf.product_line
    occ = rf.building_occupancy

    # Validate required fields
    missing = []

    if not state:
        missing.append("state")
    if not county:
        missing.append("county")
    if not rf.product_line:
        missing.append("product_line")
    if not rf.building_occupancy:
        missing.append("building_occupancy")

    if missing:
        hx.errors.fatal(f"Missing required value(s): {', '.join(missing)}.")

    exclusions = hx.params.table_general_exclusions
    ws_table = hx.params.table_ws_exclusions
    flood_zone_table = hx.params.table_flood_zone_exclusions
    hazard_mappings = hx.params.table_hazard_mappings

    def get_ws_inclusion():
        try:
            limit = ws_table.loc[ws_table['State Code'] == state, 'Distance to Coast Limit (WS)'].iloc[0]
            if limit == 'None' or rf.distance_to_coast > float(limit):
                return get_peril_value(exclusions, state, county, 'WS')
        except Exception:
            pass
        return False

    def get_fl_inclusion():
        try:
            flood_zone = hazard_mappings.loc[
                (hazard_mappings['State Code'] == state) &
                (hazard_mappings['County'] == county),
                'NFIP Flood Zone'
            ].iloc[0]
            include = flood_zone_table.loc[
                flood_zone_table['Flood Zone'] == flood_zone,
                'Include/Exclude'
            ].iloc[0]
            if include != 'Exclude':
                return get_peril_value(exclusions, state, county, 'FL')
        except Exception:
            pass
        return False

    def get_wf_inclusion(state: str, county: str):
        with open("./model/algorithms/wildfire_coverage_mapping.json", "r") as f:
            rules = json.load(f)

        config = rules.get(state)

        # If state doesn't exist, we set wildfire coverage to off
        rf = hxd.cds.rating_factors
        pl = rf.product_line

        if pl in ['Excess Flood', 'Excess Wind & Hail', 'Monoline Earthquake']:
            return False
        else:
            if not config:
                return False

            # Otherwise check if we should set it to on
            mode = config.get("mode")
            if mode == "all":
                return True
            if mode == "include":
                return county in config.get("counties", [])
        
        return False

    # Set Base values
    aop = get_peril_value(exclusions, state, county, 'AOP')
    eb = get_peril_value(exclusions, state, county, 'Equipment Breakdown')
    wildfire = get_peril_value(exclusions, state, county, 'Wildfire')
    ws = get_ws_inclusion()
    fl = get_fl_inclusion()
    eq = False
    paf = False

    cov_a = cov_m = 0
    sub_animal = sub_diving = sub_trampoline = sub_swim = 0
    sub_prem = False
    # Underwriter overrides
    if pl == 'Homeowners (HO5)' and occ in ["Primary", "Secondary"]:
        aop, ws, wildfire, eb, fl = True, True, True, True, False
        cov_a, cov_m = 500_000, 10_000
        sub_animal = sub_diving = sub_trampoline = sub_swim = 500_000

    elif pl == 'Homeowners (HO3)' and occ in ["Primary", "Secondary", "Secondary / Seasonal Rental", "Renovation (builders risk)"]:
        aop, ws, wildfire, eb, fl = True, True, True, False, False
        cov_a = 300_000
        cov_m = 1_000 if occ != "Renovation (builders risk)" else 0
        sub_animal = sub_diving = sub_trampoline = sub_swim = 300_000
        sub_prem = occ in ["Secondary / Seasonal Rental", "Renovation (builders risk)"]

    elif pl == 'Condominium (HO6)':
        aop, ws, wildfire, eb, fl = True, True, True, False, False
        cov_a = 300_000
        if occ in ["Primary", "Secondary", "Secondary / Seasonal Rental"]:
            cov_m = 1_000
        sub_animal = 300_000 if occ in ["Primary", "Secondary", "Secondary / Seasonal Rental", "Renovation (builders risk)"] else 0

    elif pl == 'Dwelling' and occ in ["Vacant", "Rental"]:
        aop, ws, wildfire, eb, fl = True, True, True, False, False
        cov_a = 300_000
        if occ == "Rental":
            cov_m = 1_000 
            sub_animal = sub_diving = sub_trampoline = sub_swim = 25_000
            sub_prem = True

    elif pl =='Excess Flood':
        fl =  True
    elif  pl =='Excess Wind & Hail':
        ws = True
    elif pl == 'Monoline Earthquake':
        eq = True
    
    wildfire = get_wf_inclusion(state, county)    
    hxd.cds.wildfire_enabled = wildfire
    hxd.cds.wildfire_disabled = not hxd.cds.wildfire_enabled       
    
    # Assign peril inclusions
    for layer in itertools.islice(hxd.cds.layers, hxd.cds.number_of_options):
        layer.coverages.aop.include_peril.value = aop
        layer.coverages.eq.include_peril.value = eq
        layer.coverages.wildfire.include_peril.value = wildfire
        layer.coverages.paf.include_peril.value = paf
        layer.coverages.eb.include_peril.value = eb
        layer.coverages.ws.include_peril.value = ws
        layer.coverages.fl.include_peril.value = fl

        layer.coverage_a_building_limit = cov_a
        layer.coverage_m_med_pay_limit = cov_m

        layer.sublimits.animal = sub_animal
        layer.sublimits.diving_board_and_pool = sub_diving
        layer.sublimits.trampoline = sub_trampoline
        layer.sublimits.swimming_pool = sub_swim
        layer.sublimits.premises_only = sub_prem

        layer.coverages.wildfire.deductible = layer.coverages.aop.deductible

@hx.task
def new_bug_report_task(hxd, progress):
    model_name = "Property Risks - HVH"
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