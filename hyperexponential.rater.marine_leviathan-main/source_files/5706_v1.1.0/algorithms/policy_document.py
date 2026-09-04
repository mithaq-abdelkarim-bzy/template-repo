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
    exp = hxd.cds.exposure.granular
    
    # Add scalr fields below
    # Data tables are added after
    
    if sf.is_rater_priced :

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

            "benchmark_premium_net": layer.net_kpi.benchmark_premium,
            "benchmark_premium": layer.benchmark_premium,
            "benchmark_rate_net": layer.net_kpi.benchmark_rate,
            "benchmark_rate": layer.gross_kpi.benchmark_rate,
    
            "quoted_premium_net": layer.net_kpi.achieved_premium,       
            "quoted_premium": layer.quoted_premium,
            "achieved_rate_net": layer.net_kpi.achieved_rate,
            "achieved_rate": layer.gross_kpi.achieved_rate,

            "bpi": layer.bpi,
            "bpi_pre_uw_adj":  layer.net_kpi.bpi_pre_uw_adj,
            "pflr": layer.net_kpi.pflr,

            "technical_premium_net": layer.net_kpi.technical_premium,
            "tpi": layer.tpi,
            "tpi_pre_uw_adj":  layer.net_kpi.tpi_pre_uw_adj,

            "underwriter_adjustment": layer.uw_adj_impact,
            "adj_rationale": exp.uw_adjustment_rationale,
            
            "rate_change": layer.rate_change.risk_adjusted_rate_change,
            
            "u_ROV": exp.number_of_units.rov,
            "u_AUV": exp.number_of_units.auv,
            "u_Seismic_Towed": exp.number_of_units.seismic_towed,
            "u_Seismic_Ocean_Bottom": exp.number_of_units.seismic_ocean_bottom,
            "u_Diving": exp.number_of_units.diving_oceanographic,
            "u_Subs": exp.number_of_units.submersibles,
            "u_Other": exp.number_of_units.other,

            "SI_ROV": exp.total_sum_insured.rov,
            "SI_AUV": exp.total_sum_insured.auv,
            "SI_Seismic_Towed": exp.total_sum_insured.seismic_towed,
            "SI_Seismic_Ocean_Bottom": exp.total_sum_insured.seismic_ocean_bottom,
            "SI_Diving": exp.total_sum_insured.diving_oceanographic,
            "SI_Subs": exp.total_sum_insured.submersibles,
            "SI_Other": exp.total_sum_insured.other,

            "XS_ROV": exp.excess_per_loss.rov,
            "XS_Seismic_Towed": exp.excess_per_loss.seismic_towed,
            "XS_Seismic_Ocean_Bottom": exp.excess_per_loss.seismic_ocean_bottom,
            "XS_Diving": exp.excess_per_loss.diving_oceanographic,
            "XS_Subs": exp.excess_per_loss.submersibles,
            "XS_Other": exp.excess_per_loss.other,

            "XS_AUV_NormalOps": exp.excess_per_loss_auv.normal_ops,
            "XS_AUV_LaunchAndRecov": exp.excess_per_loss_auv.launch_recovery,

            "benchmark_ROV": exp.benchmark_premium.rov,
            "benchmark_AUV": exp.benchmark_premium.auv,
            "benchmark_Seismic_Towed": exp.benchmark_premium.seismic_towed,
            "benchmark_Seismic_Ocean_Bottom": exp.benchmark_premium.seismic_ocean_bottom,
            "benchmark_diving": exp.benchmark_premium.diving_oceanographic,
            "benchmark_sub": exp.benchmark_premium.submersibles,
            "benchmark_other": exp.benchmark_premium.other,

            "TypeOfWork": exp.type_of_work,
            "IceDebrisTraffic": exp.ice_debris_other_traffic,
            "ExperienceLevel": exp.experience_level,
            "UsageFactor": exp.usage_factor,

            "uw_comments": sf.uw_rationale
    }

    if sf.is_case_priced:

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

            "benchmark_premium_net": layer.net_kpi.benchmark_premium,
            "benchmark_premium": layer.benchmark_premium,
            
            "quoted_premium_net": layer.quoted_premium_net_case_priced,       
            "quoted_premium": layer.quoted_premium,
         
            "bpi": layer.bpi,
            "pflr": layer.pflr,

            "technical_premium_net": layer.net_kpi.technical_premium,
            "tpi": layer.tpi,
                      
            "rate_change": layer.rate_change.risk_adjusted_rate_change_case_priced,
            
            "uw_comments": sf.uw_rationale
    }


    # Add data tables here, need to convert to a dictionary for storate in the data dictionary using 'list_converter'
    # You do not have to output all cols 
    exposure_cols = ["country","city","type","tiv"]
    exposure_lst = list_converter(exp.example_exposure, col_order=exposure_cols)
    data["exposure_df"] = exposure_lst


    
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
    # If there are multiple layers you'll need to update
    layer = hxd.cds.layers[0]

    # Don't run if premium has not been input
    if not layer.quoted_premium:
        return

    data = create_dict_for_excel(hxd)
    hxd.policy_doc.data_dict = data

    # Compare task data with live data to unhide download button
    task_data = hxd.policy_doc.task_data_dict
    hxd.policy_doc.show_download = True if data == task_data else False
    