import hx
import json
from datetime import datetime
from algorithms.rate_utilities import pd_df_from_hx_list

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
    uw = hxd.cds.uw_rationale
    mod = hxd.cds.modifiers
    exp = hxd.cds.exposure.granular
    el = layer.expected_loss
    
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
        
        "limit": layer.limit,
        "agg_limit": layer.aggregate_limit,
        "type": layer.type,

        "risk_preparedness": rf.risk_preparedness,
        "security": rf.security,
        "crisis_management": rf.crisis_management,
        "social_media": rf.social_media,
        "high_profile_event": rf.high_profile_event,

        "bi_and_ee_cover": rf.bi_and_ee_cover,
        "seperate_bi_ee_agg_limits": rf.seperate_bi_ee_agg_limits,
        "bi_tiv": rf.bi_tiv,
        "extensions_covered": rf.extensions_covered,
        "liability_covered": rf.liability_covered,
        "extensions_comment": cds.uw_rationale.extensions_comment,

        "knowledge_of_insured": uw.knowledge_of_insured,
        "portfolio_fit": uw.portfolio_fit,
        "basis_of_risk_selection": uw.basis_of_risk_selection,
        "complex_considerations": uw.complex_considerations,
        "facts_affecting_decision": uw.facts_affecting_decision,

        "quoted_premium": layer.quoted_premium,
        "benchmark_premium": layer.benchmark_premium,
        "technical_premium": layer.technical_premium,
        "model_premium": layer.model_premium,
        "bpi": layer.bpi,
        "tpi": layer.tpi,
        # "tpi_pre_uw_adj": layer.tpi_pre_uw_adj,
        "underwriter_adjustment": mod.underwriter_adjustment,
        "uw_comments": uw.comments,

        "exposure_rated": el.exposure_rated,
        "experience_rated": el.experience_rated,
        "experience_weight": el.experience_weight,
        "blended_el": el.blended,

        "rate_change": layer.rate_change.risk_adjusted_rate_change.uw_selected

    }

    # Deductible vs Excess
    if layer.type == "Deductible":
        data["deductible"] = layer.deductible
    else:
        data["deductible"] = layer.excess


    # Add edcucation and non education exposure
    education_cols = ["institution_name","num_schools","country","state_code","state_name","city_risk","location","school_grade","school_type","boarding_day","num_students","num_employees","sex_of_school","num_req_counselling","factor_city_risk"]
    education_lst = list_converter(exp.education, col_order=education_cols)
    data["education_df"] = education_lst

    non_education_cols = ["establishment_name","sector/sector","sector/sub_sector","num_of_est","country","state_code","state_name","city_risk","location","footfall_measure","num_of_staff_per_est","footfall_measure_per_est","east_of_access","enclosed_space","num_of_days","num_req_counselling","footfall_band","factor_city_risk"]
    non_education_lst = list_converter(exp.non_education, col_order=non_education_cols)
    data["non_education_df"] = non_education_lst

    
    # Add URL of hx policy
    p_id = hx.meta.policy_id
    po_id = hx.meta.policy_option_id
    policy_url = f"https://www.beazley.hxrenew.com/policies/{p_id}/options/{po_id}"
    data["policy_url"] = policy_url

    # Format data
    formatted_data = clean_data_for_policy_doc(data)
    json_data = json.dumps(formatted_data)

    return json_data

# Push dictionary to hxd for storage
def store_policy_data(hxd):
    layer = hxd.cds.layers[0]

    # Don't run if premium has not been input
    if not layer.quoted_premium:
        return

    data = create_dict_for_excel(hxd)
    hxd.policy_doc.data_dict = data

    # Compare task data with live data to unhide download button
    task_data = hxd.policy_doc.task_data_dict
    hxd.policy_doc.show_download = True if data == task_data else False
    