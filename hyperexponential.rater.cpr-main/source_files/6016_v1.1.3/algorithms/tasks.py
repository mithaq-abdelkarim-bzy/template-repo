#########################################################################################################
########################################### Outstanding Items ###########################################
#########################################################################################################
### 1) CHECK comment out line 152:         expiring_policy_option_id=473090 # NOTE: for debugging if needed
### 2) 
### 3) 
### 4) 
### 5) 
#########################################################################################################

import hx, os, json, requests, openpyxl
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime

from algorithms.rate_rate_change                            import rate_change_buckets
from libraries.hx_renew_api.algorithms.init_hx_renew_api    import init_hx_renew_api
from libraries.rate_change.algorithms.rate_change           import RateChange as RateChangeLib
from algorithms.tsk_api_ihs_data                            import api_ihs_data
from algorithms.tsk_sql_bi_data                             import sql_bi_data
from algorithms.tsk_sim_political                           import sim_political
from algorithms.tsk_fill_exposure_profile                   import fill_exposure_profile



@hx.task
def task_sim_political(hxd, progress):
    sim_political(hxd, progress)
    pass


@hx.task
def task_api_ihs_data(hxd, progress):
    api_ihs_data(hxd, progress)
    pass


@hx.task
def task_sql_bi_data(hxd, progress):
    sql_bi_data(hxd, progress)
    pass


@hx.task
def task_fill_exposure_profile(hxd, progress):
    fill_exposure_profile(hxd, progress)
    pass



@hx.task
def sync_expiring_ids(hxd, progress):
    # Note this task is to be run following each migrated policy to sync the expiring ids
    hxd.model_state.expiring_policy_option_id   = hx.meta.expiring_policy_option_id
    hxd.model_state.is_migrated                 = True



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
        hxd.cds.layers[0].status = "Assessment Pending"
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
    expiring_policy_option_id = hxd.cds.rate_change.expiring_policy_option_id.selected# or 328232 # NOTE: use hardcoded ID for debugging if needed
    expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False)

    if expiring_response.status_code != 200:
        raise Exception(expiring_response.json())

    expiring_data = expiring_response.json()["data"]

    # Get fields from json response and push to hxd
    expiring_layers_len = len(expiring_data["cds"]["layers"])
    layer_mapping = {}


    # CUSTOM >>> calculating expiring term - not part of skeleton model
    expiring_incept     = expiring_data["hx_core"]["inception_date"]    # string
    expiring_expiry     = expiring_data["hx_core"]["expiry_date"]       # string
    expiring_term       = ( 12  if   (expiring_incept == "" or expiring_expiry == "")
                                else (pd.to_datetime(expiring_expiry)  +  relativedelta(days=1)  -  pd.to_datetime(expiring_incept)).days / 365.25 * 12)          # need to do empty test on string not datetime
    expiring_annualise  = 12 / expiring_term


    for idx, layer in enumerate(hxd.cds.layers):
        # Throw error if expiring layer doesn't exist
        if layer.rate_change.expiring_layer > expiring_layers_len:
            hx.errors.fatal(f"Expiring Layer {layer.rate_change.expiring_layer}, mapped to Renewal Layer {idx+1}, does not exist. Number of expiring layers is {expiring_layers_len}.")

        mapped_expiring_layer_idx                                   = layer.rate_change.expiring_layer - 1
        expiring_written_line                                       = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["written_line"]


        # CUSTOM >>> annualising expiring factor was not part of skeleton model
        # political and credit handled separately below due to political defect advised 11-aug-25 (uw have been entering annual rol when actuarial understood to be term)
        if expiring_data["cds"]['product'] == 'Political Risk':   
            exp_100_annual_bound   = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]['political']['premium_composition_pst_uwadj']['total']["premium_bound"]  # this is always annual 100pct
        else:
            exp_100_annual_bound   = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["quoted_premium"]   * (expiring_annualise)           / (expiring_written_line or 1)

        layer.rate_change.premium.line_100pct.annualised.expiring   = exp_100_annual_bound
        layer.rate_change.premium.beazley_line.annualised.expiring  = layer.rate_change.premium.line_100pct.annualised.expiring                     * (expiring_written_line or 0)
        layer.rate_change.expiring_policy_info.expiring_brokerage   = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["brokerage"] or 0


        # NOTE: ... Add expiring fields as required here

        # CUSTOM >>> capture term in months - field already existed in skeleton model - but was not used
        layer.rate_change.expiring_policy_info.expiring_policy_length=expiring_term

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
        async_tasks=[task_sim_political],  # Pass the actual tasks, not strings
        # async_tasks=[],  # Pass the actual tasks, not strings
        data_schema_static_path=data_schema_static_path
    )

    rc.calculate_repriced_values(
        #   expiring_policy_option_id=533267 # NOTE: for debugging if needed
    )

    # Use the repriced values to calculate the changes for each bucket
    rarc_df, rarc_list = rc.calculate_rarc_by_layer()
    
    # NOTE: for debugging if needed
    pd.set_option('display.max_columns', None)
    print(rarc_df)
    print(rarc_list)

    # Calculate brokerage change for storage but not display
    for layer in hxd.cds.layers:
        expiring_brokerage = layer.rate_change.expiring_policy_info.expiring_brokerage or 0
        renewal_brokerage = layer.brokerage or 0
        layer.rate_change.brokerage_change.model_calculated = (1 - expiring_brokerage) / (1 - renewal_brokerage)


    # Push to hxd
    for rarc_layer, hxd_layer in zip(rarc_list, hxd.cds.layers):
        hxd_layer.rate_change.temp_storage = rarc_layer["temp_storage"]
        rarc_layer.pop("temp_storage")

        # THE SECTION COMMENTED OUT BELOW WAS NEEDED WHEN THE UNDERSTANDING WAS THE UW ENTERED A TERM ROL, NOW WE KNOW IT TO BE ANNUAL
        #
        # # CUSTOM >>> adjust for using inception/expiry dates as inputs to RARC algorithm
        # # Typically RARC algorithm works as follows:
        # #       i)   calculate relative changes from bucket-bucket on a constant policy length (current? inception/expiry dates are always used),
        # #       ii)  determines the change in bound & benchmark from expiring to renewing on an annualised basis 
        # #       iii) imply the rate change by comparing the total bound premium change in (ii) to the total explained change in (i), with it never mattering that the first is at term and second annualised
        # # However under risk characteristics bucket we have to push the inception & expiry dates to get the impact of change in ihs factors.
        # #       consequently this means we have a term change flowing into the calculation for "" the impact of which is (renewing_term / expiring_term)
        # #       the factor below is intended to reverse this logic stripping out this impact by deriving a multiplier    (expiring_term / renewing_term)
        # #       we then adjust the risk characteristics change factor prior to it being pushed to the hxd
        # # Additionally for crcf we have the ADDITIONAL issue that pushing an exposure profile of different terms can  

        # expiring_term       = hxd_layer.rate_change.expiring_policy_info.expiring_policy_length or 12
        # renewing_term       = hxd.cds.rating_factors.policy_term  or 12
        # term_expiry_renew   = expiring_term / renewing_term    

        # original_value      = rarc_layer['risk_characteristics_change']['model_calculated']
        # rarc_layer['risk_characteristics_change']['model_calculated'] = original_value / term_expiry_renew

        # if hxd.cds.product != 'Political Risk':
        #     original_value      = rarc_layer['exposure_change']['model_calculated']
        #     rarc_layer['exposure_change']['model_calculated'] = original_value * term_expiry_renew



        for key, value in rarc_layer.items():
            setattr(hxd_layer.rate_change, key, value)


        # so we can clear out the overrides on renewal we need the uw_selected values to be set within the async task - instead of row 97 of rate change algo - it could be implemented more elegantly but it works!
        for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
            rc_vbl                          = getattr(hxd_layer.rate_change, item)
            rc_vbl.uw_selected.calculated   = rc_vbl.model_calculated
        


    # Confirm task has been run
    hxd.cds.rate_change.has_rarc_run        = True
    hxd.cds.rate_change.has_rarc_not_run    = False






# Generate policy document in Excel
@hx.task
def policy_to_excel_task(hxd, progress):    
    from openpyxl.utils.cell import coordinate_to_tuple
    
    # Load string containing data
    data = json.loads(hxd.policy_doc.data_dict)

    # setting the right policy url string
    if   hx.secrets.environment_name == 'beazley-dev':      data["policy_url"] = data["dev_policy_url"]
    elif hx.secrets.environment_name == 'beazley-tst':      data["policy_url"] = data["tst_policy_url"]
    else:                                                   data["policy_url"] = data["prd_policy_url"]


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


    # declare sheets for manipulation
    risk_info_sheet  = workbook['RiskInformation']
    exposure_sheet   = workbook['Exposure']
    rating_sum_sheet = workbook['RatingSummary']


    # hide using data grouping the relevant cells
    if data['product'] == 'Political Risk':                             # data['product'] ... 'product' here is the name in our custom dictionary not the hxd
        risk_info_sheet.row_dimensions.group(start=36, end=50, hidden=True)
        exposure_sheet.column_dimensions.group(start='A', end='Q', hidden=True)
        rating_sum_sheet.row_dimensions.group(start=36, end=53, hidden=True)
    else:
        risk_info_sheet.row_dimensions.group(start=36, end=50, hidden=False)
        exposure_sheet.column_dimensions.group(start='R', end='AC', hidden=True)
        rating_sum_sheet.row_dimensions.group(start=54, end=69, hidden=True)


    # Save the filled template to a new file
    with hxd.policy_doc.output_file.open("b") as f:
        workbook.save(f)

    # Store task data to allow comparison if anything changes in rating
    hxd.policy_doc.task_data_dict = hxd.policy_doc.data_dict


