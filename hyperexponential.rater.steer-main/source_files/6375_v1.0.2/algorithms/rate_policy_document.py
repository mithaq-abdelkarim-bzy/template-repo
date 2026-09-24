# v0.5.1
import hx
import json
from datetime import datetime
from algorithms.rate_utilities import pd_df_from_hx_list
from algorithms.model_profiler.profiling_hxd_functions import time_me
# Format data in dictionary for Excel
def clean_data_for_policy_doc(data):
    for key, value in data.items():
        if value is None:
            data[key] = ""
        elif value is True:
            data[key] = "Yes"
        elif value is False:
            data[key] = "No"
        elif key in ["inception_date", "expiry_date"]:
            date_str = str(value)
            data[key] = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")

    return data


def list_converter(hx_list, col_order = []):
    df = pd_df_from_hx_list(hx_list)
    if col_order:
        df = df[col_order]

    dict_of_lists = df.to_dict(orient='records')

    return dict_of_lists


# Create data dictionary to write to Excel file
def create_dict_for_excel(hxd):
    cds = hxd.cds
    sf = hxd.cds.standard_fields
    rf = hxd.cds.rating_factors
    layer = hxd.cds.layers[0]
    # exp = hxd.cds.exposure.granular
    
    # Add scalr fields below
    # Data tables are added after
    data = {
        
        "brokerage": layer.brokerage,
        "expiry_date": sf.expiry_date,
        "inception_date": sf.inception_date,
        "insured_name": sf.insured_name,
        "underwriter": sf.underwriter,
        "section_reference": sf.policy_reference,
        "source_currency": cds.currencies.source_currency,
        "term": rf.policy_term,
        "written_line": layer.written_line,
        "status": layer.status,
                
        "quoted_premium_100": layer.quoted_premium_100,
        "benchmark_premium_100": layer.benchmark_premium_100,
        "technical_premium_100": layer.technical_premium_100,
        "bpi": layer.bpi,
        "tpi": layer.tpi,
        "underwriter_adjustment": layer.uw_adj_impact,
        "uw_comments": sf.uw_rationale,
        
        # "rate_change": layer.rate_change.risk_adjusted_rate_change
        "rate_change": layer.rate_change.rate_change.final

    }


    # Add data tables here, need to convert to a dictionary for storate in the data dictionary using 'list_converter'
    # You do not have to output all cols 
    # exposure_cols = ["country","city","type","tiv"]
    # exposure_lst = list_converter(exp.example_exposure, col_order=exposure_cols)
    # data["exposure_df"] = exposure_lst

    
    # Add URL of hx policy
    p_id = hx.meta.policy_id
    po_id = hx.meta.policy_option_id
    policy_url = f"https://www.beazley.hxrenew.com/policies/{p_id}/options/{po_id}"
    data["policy_url"] = policy_url

    # Format data
    formatted_data = clean_data_for_policy_doc(data)
    json_data = json.dumps(formatted_data)

    return json_data
@time_me
# Push dictionary to hxd for storage
def store_policy_data(hxd):
    # If there are multiple layers you'll need to update
    layer = hxd.cds.layers[0]

    # Don't run if premium has not been input
    if not layer.quoted_premium_100:
        return

    data = create_dict_for_excel(hxd)
    hxd.policy_doc.data_dict = data

    # Compare task data with live data to unhide download button
    task_data = hxd.policy_doc.task_data_dict
    hxd.policy_doc.show_download = True if data == task_data else False
    