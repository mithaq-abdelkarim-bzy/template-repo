import hx
import json
from datetime import datetime
from algorithms.rate_utilities import one_layer

# Format data in dictionary for Excel
def clean_data_for_policy_doc(data):
    for key, value in data.items():
        if value is None:
            data[key] = ""
        elif value is True:
            data[key] = "YES"
        elif value is False:
            data[key] = "NO"
        elif key in ["inception_date", "expiry_date"]:
            date_str = str(value)
            data[key] = datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")

    return data

# Unpack countries from list
def get_countries(cover, suffix_v = ""):
    countries = {}

    for idx, country in enumerate(cover.countries):
        countries[f"country_{idx+1}{suffix_v}"] = country.country
        countries[f"cat_expo_{idx+1}{suffix_v}"] = country.cat_expo
        countries[f"cat_load_{idx+1}{suffix_v}"] = country.cat_load

    return countries

# Unpack standard fields
def get_standard_fields(cds, sf, layer):
    standard_fields = {
        "brokerage": layer.brokerage,
        "expiry_date": sf.expiry_date,
        "inception_date": sf.inception_date,
        "insured_name": sf.insured_name,
        "section_reference": layer.section_reference,
        "source_currency": cds.currencies.source_currency,
        "term": cds.term.selected,
        "written_line": layer.written_line,
        "uw_rationale": sf.uw_rationale
    }

    return standard_fields

# Unpack rating summary
def get_rating_summary(layer):
    rating_summary = {
        "gross_premium_label": layer.gross_premium_label,
        "quoted_premium": layer.quoted_premium,
        "benchmark_premium": layer.benchmark_premium,
        "technical_premium": layer.technical_premium,
        "technical_premium_pre_uw_adj": layer.technical_premium_pre_uw_adj,
        "bpi": layer.bpi,
        "tpi": layer.tpi,
        "tpi_pre_uw_adj": layer.tpi_pre_uw_adj,
        # Expiring
        "expiring_premium": layer.rate_change.expiring_policy_info.expiring_premium,
        "expiring_benchmark_premium": layer.rate_change.expiring_policy_info.expiring_benchmark_premium,
        "expiring_technical_premium": layer.rate_change.expiring_policy_info.expiring_technical_premium,
        "expiring_bpi": layer.rate_change.expiring_policy_info.expiring_bpi,
        "expiring_tpi": layer.rate_change.expiring_policy_info.expiring_tpi
    }

    return rating_summary

# Create data dictionary to write to Excel file
def create_dict_for_excel(hxd):
    cds = hxd.cds
    sf = hxd.cds.standard_fields
    layer, cvg = one_layer(hxd)
    layer_cyber = hxd.cds.layers[0].coverages.cargo_cyber_addon
    ct = cvg.cargo_transit
    cs = cvg.cargo_storage
    ct_cyber = cvg.cargo_cyber_transit
    cs_cyber = cvg.cargo_cyber_storage
    st = cvg.specie_transit
    ss = cvg.specie_storage
    clt = cvg.conloss_transit
    clc = cvg.conloss

    data = {}

    if cds.cover_selection.is_cargo:
        data = {
            # Transit
            "transit_flag": ct.transit_flag,
            "wh_to_port_flag": ct.wh_to_port_flag,
            "loading_flag": ct.loading_flag,
            "voyage_flag": ct.voyage_flag,
            "unloading_flag": ct.unloading_flag,
            "port_to_wh_flag": ct.port_to_wh_flag,
            "transit_base_rate": ct.base_rate,
            "transit_commodity": ct.commodity,
            "transit_commodity_factor": ct.commodity_factor,
            "trans_vals": ct.trans_vals,
            "trans_vals_factor": ct.trans_vals_factor,
            "transit_deductible_level": ct.deductible_level,
            "transit_deductible_level_factor": ct.deductible_level_factor.selected,
            "transit_excess": ct.excess,
            "transit_excess_factor": ct.excess_factor.selected,
            "packaging": ct.packaging,
            "packaging_factor": ct.packaging_factor,
            "conv_air": ct.conv_air,
            "conv_land": ct.conv_land,
            "conv_sea": ct.conv_sea,
            "conv_air_factor": ct.conv_air_factor,
            "conv_land_factor": ct.conv_land_factor,
            "conv_sea_factor": ct.conv_sea_factor,
            "conv_factor": ct.conv_factor,
            "voyage": ct.voyage,
            "voyage_factor": ct.voyage_factor,
            "surveyor": ct.surveyor,
            "surveyor_factor": ct.surveyor_factor,
            "vessel": ct.vessel,
            "vessel_factor": ct.vessel_factor,
            "transit_uw_discretion": ct.uw_discretion,
            "transit_uw_discretion_factor": ct.uw_discretion_factor,
            "transit_type_of_cover": ct.type_of_cover,
            "transit_type_of_cover_factor": ct.type_of_cover_factor,
            "transit_technical_deductions": ct.technical_deductions,
            "transit_technical_rate": ct.technical_rate,
            "transit_technical_premium": ct.technical_premium,
            "transit_pct_of_technical": ct.pct_of_technical,
            "transit_actual_rate": ct.actual_rate,
            "transit_quoted_premium": ct.quoted_premium,
            # Storage
            "storage_flag": cs.storage_flag,
            "storage_base_rate": cs.base_rate,
            "stock_vals": cs.stock_vals,
            "storage_deductible_level": cs.deductible_level,
            "storage_deductible_level_factor": cs.deductible_level_factor.selected,
            "storage_excess": cs.excess,
            "storage_excess_factor": cs.excess_factor.selected,
            "survey": cs.survey,
            "survey_factor": cs.survey_factor,
            "risk_mgmt": cs.risk_mgmt,
            "risk_mgmt_factor": cs.risk_mgmt_factor,
            "storage_type_of_cover": cs.type_of_cover,
            "storage_type_of_cover_factor": cs.type_of_cover_factor,
            "storage_uw_discretion": cs.uw_discretion,
            "storage_uw_discretion_factor": cs.uw_discretion_factor,
            "storage_rate": cs.rate,
            "avg_val_pcm": cs.avg_val_pcm,
            "cat_expo": cs.cat_expo,
            "combined_cat_load": cs.combined_cat_load,
            **get_countries(cs),
            "retail_expo": cs.retail_expo,
            "retail_load": cs.retail_load,
            "all_else_expo": cs.all_else_expo.selected,
            "all_else_load": cs.all_else_load,
            "storage_technical_deductions": cs.technical_deductions,
            "storage_technical_rate": cs.technical_rate,
            "storage_technical_premium": cs.technical_premium,
            "storage_pct_of_technical": cs.pct_of_technical,
            "storage_actual_rate": cs.actual_rate,
            "storage_quoted_premium": cs.quoted_premium
        }
        if cds.cover_selection.is_cargo_cyber:
            if layer.has_single_section_ref:
                section_reference_v = layer_cyber.single_section_reference.ref
            elif layer.has_double_section_ref:
                section_reference_v = layer_cyber.eea_section_reference.ref
            data = {
                # Transit
                "transit_flag": ct.transit_flag,
                "wh_to_port_flag": ct.wh_to_port_flag,
                "loading_flag": ct.loading_flag,
                "voyage_flag": ct.voyage_flag,
                "unloading_flag": ct.unloading_flag,
                "port_to_wh_flag": ct.port_to_wh_flag,
                "transit_base_rate": ct.base_rate,
                "transit_commodity": ct.commodity,
                "transit_commodity_factor": ct.commodity_factor,
                "trans_vals": ct.trans_vals,
                "trans_vals_factor": ct.trans_vals_factor,
                "transit_deductible_level": ct.deductible_level,
                "transit_deductible_level_factor": ct.deductible_level_factor.selected,
                "transit_excess": ct.excess,
                "transit_excess_factor": ct.excess_factor.selected,
                "packaging": ct.packaging,
                "packaging_factor": ct.packaging_factor,
                "conv_air": ct.conv_air,
                "conv_land": ct.conv_land,
                "conv_sea": ct.conv_sea,
                "conv_air_factor": ct.conv_air_factor,
                "conv_land_factor": ct.conv_land_factor,
                "conv_sea_factor": ct.conv_sea_factor,
                "conv_factor": ct.conv_factor,
                "voyage": ct.voyage,
                "voyage_factor": ct.voyage_factor,
                "surveyor": ct.surveyor,
                "surveyor_factor": ct.surveyor_factor,
                "vessel": ct.vessel,
                "vessel_factor": ct.vessel_factor,
                "transit_uw_discretion": ct.uw_discretion,
                "transit_uw_discretion_factor": ct.uw_discretion_factor,
                "transit_type_of_cover": ct.type_of_cover,
                "transit_type_of_cover_factor": ct.type_of_cover_factor,
                "transit_technical_deductions": ct.technical_deductions,
                "transit_technical_rate": ct.technical_rate,
                "transit_technical_premium": ct.technical_premium,
                "transit_pct_of_technical": ct.pct_of_technical,
                "transit_actual_rate": ct.actual_rate,
                "transit_quoted_premium": ct.quoted_premium,
                # Storage
                "storage_flag": cs.storage_flag,
                "storage_base_rate": cs.base_rate,
                "stock_vals": cs.stock_vals,
                "storage_deductible_level": cs.deductible_level,
                "storage_deductible_level_factor": cs.deductible_level_factor.selected,
                "storage_excess": cs.excess,
                "storage_excess_factor": cs.excess_factor.selected,
                "survey": cs.survey,
                "survey_factor": cs.survey_factor,
                "risk_mgmt": cs.risk_mgmt,
                "risk_mgmt_factor": cs.risk_mgmt_factor,
                "storage_type_of_cover": cs.type_of_cover,
                "storage_type_of_cover_factor": cs.type_of_cover_factor,
                "storage_uw_discretion": cs.uw_discretion,
                "storage_uw_discretion_factor": cs.uw_discretion_factor,
                "storage_rate": cs.rate,
                "avg_val_pcm": cs.avg_val_pcm,
                "cat_expo": cs.cat_expo,
                "combined_cat_load": cs.combined_cat_load,
                **get_countries(cs),
                "retail_expo": cs.retail_expo,
                "retail_load": cs.retail_load,
                "all_else_expo": cs.all_else_expo.selected,
                "all_else_load": cs.all_else_load,
                "storage_technical_deductions": cs.technical_deductions,
                "storage_technical_rate": cs.technical_rate,
                "storage_technical_premium": cs.technical_premium,
                "storage_pct_of_technical": cs.pct_of_technical,
                "storage_actual_rate": cs.actual_rate,
                "storage_quoted_premium": cs.quoted_premium,
                # transit cyber
                "transit_flag_cyber": ct_cyber.transit_flag,
                "wh_to_port_flag_cyber": ct_cyber.wh_to_port_flag,
                "loading_flag_cyber": ct_cyber.loading_flag,
                "voyage_flag_cyber": ct_cyber.voyage_flag,
                "unloading_flag_cyber": ct_cyber.unloading_flag,
                "port_to_wh_flag_cyber": ct_cyber.port_to_wh_flag,
                "transit_base_rate_cyber": ct_cyber.base_rate,
                "transit_commodity_cyber": ct_cyber.commodity,
                "transit_commodity_factor_cyber": ct_cyber.commodity_factor,
                "trans_vals_cyber": ct_cyber.trans_vals,
                "trans_vals_factor_cyber": ct_cyber.trans_vals_factor,
                "transit_deductible_level_cyber": ct_cyber.deductible_level,
                "transit_deductible_level_factor_cyber": ct_cyber.deductible_level_factor.selected,
                "transit_excess_cyber": ct_cyber.excess,
                "transit_excess_factor_cyber": ct_cyber.excess_factor.selected,
                "packaging_cyber": ct_cyber.packaging,
                "packaging_factor_cyber": ct_cyber.packaging_factor,
                "conv_air_cyber": ct_cyber.conv_air,
                "conv_land_cyber": ct_cyber.conv_land,
                "conv_sea_cyber": ct_cyber.conv_sea,
                "conv_air_factor_cyber": ct_cyber.conv_air_factor,
                "conv_land_factor_cyber": ct_cyber.conv_land_factor,
                "conv_sea_factor_cyber": ct_cyber.conv_sea_factor,
                "conv_factor_cyber": ct_cyber.conv_factor,
                "voyage_cyber": ct_cyber.voyage,
                "voyage_factor_cyber": ct_cyber.voyage_factor,
                "surveyor_cyber": ct_cyber.surveyor,
                "surveyor_factor_cyber": ct_cyber.surveyor_factor,
                "vessel_cyber": ct_cyber.vessel,
                "vessel_factor_cyber": ct_cyber.vessel_factor,
                "transit_uw_discretion_cyber": ct_cyber.uw_discretion,
                "transit_uw_discretion_factor_cyber": ct_cyber.uw_discretion_factor,
                "transit_type_of_cover_cyber": ct_cyber.type_of_cover,
                "transit_type_of_cover_factor_cyber": ct_cyber.type_of_cover_factor,
                "transit_technical_deductions_cyber": ct_cyber.technical_deductions,
                "transit_technical_rate_cyber": ct_cyber.technical_rate,
                "transit_technical_premium_cyber": ct_cyber.technical_premium,
                "transit_pct_of_technical_cyber": ct_cyber.pct_of_technical,
                "transit_actual_rate_cyber": ct_cyber.actual_rate,
                "transit_quoted_premium_cyber": ct_cyber.quoted_premium,
                # Cargo Cyber Storage
                "storage_flag_cyber": cs_cyber.storage_flag,
                "storage_base_rate_cyber": cs_cyber.base_rate,
                "stock_vals_cyber": cs_cyber.stock_vals,
                "storage_deductible_level_cyber": cs_cyber.deductible_level,
                "storage_deductible_level_factor_cyber": cs_cyber.deductible_level_factor.selected,
                "storage_excess_cyber": cs_cyber.excess,
                "storage_excess_factor_cyber": cs_cyber.excess_factor.selected,
                "survey_cyber": cs_cyber.survey,
                "survey_factor_cyber": cs_cyber.survey_factor,
                "risk_mgmt_cyber": cs_cyber.risk_mgmt,
                "risk_mgmt_factor_cyber": cs_cyber.risk_mgmt_factor,
                "storage_type_of_cover_cyber": cs_cyber.type_of_cover,
                "storage_type_of_cover_factor_cyber": cs_cyber.type_of_cover_factor,
                "storage_uw_discretion_cyber": cs_cyber.uw_discretion,
                "storage_uw_discretion_factor_cyber": cs_cyber.uw_discretion_factor,
                "storage_rate_cyber": cs_cyber.rate,
                "avg_val_pcm_cyber": cs_cyber.avg_val_pcm,
                "cat_expo_cyber": cs_cyber.cat_expo,
                "combined_cat_load_cyber": cs_cyber.combined_cat_load,
                **get_countries(cs_cyber, suffix_v="_cyber"),
                "retail_expo_cyber": cs_cyber.retail_expo,
                "retail_load_cyber": cs_cyber.retail_load,
                "all_else_expo_cyber": cs_cyber.all_else_expo.selected,
                "all_else_load_cyber": cs_cyber.all_else_load,
                "storage_technical_deductions_cyber": cs_cyber.technical_deductions,
                "storage_technical_rate_cyber": cs_cyber.technical_rate,
                "storage_technical_premium_cyber": cs_cyber.technical_premium,
                "storage_pct_of_technical_cyber": cs_cyber.pct_of_technical,
                "storage_actual_rate_cyber": cs_cyber.actual_rate,
                "storage_quoted_premium_cyber": cs_cyber.quoted_premium,
                # Cargo Cyber add on policy information
                # "gross_premium_label_cyber": layer_cyber.gross_premium_label,
                "quoted_premium_cyber": layer_cyber.quoted_premium,
                "benchmark_premium_cyber": layer_cyber.benchmark_premium,
                "technical_premium_cyber": layer_cyber.technical_premium,
                "technical_premium_pre_uw_adj_cyber": layer_cyber.technical_premium_pre_uw_adj,
                "bpi_cyber": layer_cyber.bpi,
                "tpi_cyber": layer_cyber.tpi,
                "tpi_pre_uw_adj_cyber": layer_cyber.tpi_pre_uw_adj,    
                "section_reference_cyber": section_reference_v,
                "written_line_cyber": layer_cyber.written_line,
                "brokerage_cyber": layer_cyber.brokerage        
            }
    elif cds.cover_selection.is_cargo_cyber_dropdown:
        data = {
            # cargo Cyber Transit
            "transit_flag": ct_cyber.transit_flag,
            "wh_to_port_flag": ct_cyber.wh_to_port_flag,
            "loading_flag": ct_cyber.loading_flag,
            "voyage_flag": ct_cyber.voyage_flag,
            "unloading_flag": ct_cyber.unloading_flag,
            "port_to_wh_flag": ct_cyber.port_to_wh_flag,
            "transit_base_rate": ct_cyber.base_rate,
            "transit_commodity": ct_cyber.commodity,
            "transit_commodity_factor": ct_cyber.commodity_factor,
            "trans_vals": ct_cyber.trans_vals,
            "trans_vals_factor": ct_cyber.trans_vals_factor,
            "transit_deductible_level": ct_cyber.deductible_level,
            "transit_deductible_level_factor": ct_cyber.deductible_level_factor.selected,
            "transit_excess": ct_cyber.excess,
            "transit_excess_factor": ct_cyber.excess_factor.selected,
            "packaging": ct_cyber.packaging,
            "packaging_factor": ct_cyber.packaging_factor,
            "conv_air": ct_cyber.conv_air,
            "conv_land": ct_cyber.conv_land,
            "conv_sea": ct_cyber.conv_sea,
            "conv_air_factor": ct_cyber.conv_air_factor,
            "conv_land_factor": ct_cyber.conv_land_factor,
            "conv_sea_factor": ct_cyber.conv_sea_factor,
            "conv_factor": ct_cyber.conv_factor,
            "voyage": ct_cyber.voyage,
            "voyage_factor": ct_cyber.voyage_factor,
            "surveyor": ct_cyber.surveyor,
            "surveyor_factor": ct_cyber.surveyor_factor,
            "vessel": ct_cyber.vessel,
            "vessel_factor": ct_cyber.vessel_factor,
            "transit_uw_discretion": ct_cyber.uw_discretion,
            "transit_uw_discretion_factor": ct_cyber.uw_discretion_factor,
            "transit_type_of_cover": ct_cyber.type_of_cover,
            "transit_type_of_cover_factor": ct_cyber.type_of_cover_factor,
            "transit_technical_deductions": ct_cyber.technical_deductions,
            "transit_technical_rate": ct_cyber.technical_rate,
            "transit_technical_premium": ct_cyber.technical_premium,
            "transit_pct_of_technical": ct_cyber.pct_of_technical,
            "transit_actual_rate": ct_cyber.actual_rate,
            "transit_quoted_premium": ct_cyber.quoted_premium,
            # Cargo Cyber Storage
            "storage_flag": cs_cyber.storage_flag,
            "storage_base_rate": cs_cyber.base_rate,
            "stock_vals": cs_cyber.stock_vals,
            "storage_deductible_level": cs_cyber.deductible_level,
            "storage_deductible_level_factor": cs_cyber.deductible_level_factor.selected,
            "storage_excess": cs_cyber.excess,
            "storage_excess_factor": cs_cyber.excess_factor.selected,
            "survey": cs_cyber.survey,
            "survey_factor": cs_cyber.survey_factor,
            "risk_mgmt": cs_cyber.risk_mgmt,
            "risk_mgmt_factor": cs_cyber.risk_mgmt_factor,
            "storage_type_of_cover": cs_cyber.type_of_cover,
            "storage_type_of_cover_factor": cs_cyber.type_of_cover_factor,
            "storage_uw_discretion": cs_cyber.uw_discretion,
            "storage_uw_discretion_factor": cs_cyber.uw_discretion_factor,
            "storage_rate": cs_cyber.rate,
            "avg_val_pcm": cs_cyber.avg_val_pcm,
            "cat_expo": cs_cyber.cat_expo,
            "combined_cat_load": cs_cyber.combined_cat_load,
            **get_countries(cs_cyber),
            "retail_expo": cs_cyber.retail_expo,
            "retail_load": cs_cyber.retail_load,
            "all_else_expo": cs_cyber.all_else_expo.selected,
            "all_else_load": cs_cyber.all_else_load,
            "storage_technical_deductions": cs_cyber.technical_deductions,
            "storage_technical_rate": cs_cyber.technical_rate,
            "storage_technical_premium": cs_cyber.technical_premium,
            "storage_pct_of_technical": cs_cyber.pct_of_technical,
            "storage_actual_rate": cs_cyber.actual_rate,
            "storage_quoted_premium": cs_cyber.quoted_premium
        }
    elif cds.cover_selection.is_specie:
        data = {
            # Transit
            "transit_flag": st.transit_flag,
            "transit_base_rate": st.base_rate,
            "transit_commodity": st.commodity,
            "transit_commodity_factor": st.commodity_factor,
            "trans_vals": st.trans_vals,
            "trans_vals_factor": st.trans_vals_factor,
            "transit_deductible_level": st.deductible_level,
            "transit_deductible_level_factor": st.deductible_level_factor,
            "transit_excess": st.excess,
            "transit_excess_factor": st.excess_factor.selected,
            "transit_uw_discretion": st.uw_discretion,
            "transit_uw_discretion_factor": st.uw_discretion_factor,
            "transit_type_of_cover": st.type_of_cover,
            "transit_type_of_cover_factor": st.type_of_cover_factor,
            "transit_technical_deductions": st.technical_deductions,
            "transit_technical_rate": st.technical_rate,
            "transit_technical_premium": st.technical_premium,
            "transit_pct_of_technical": st.pct_of_technical,
            "transit_actual_rate": st.actual_rate,
            "transit_quoted_premium": st.quoted_premium,
            # Storage
            "storage_flag": ss.storage_flag,
            "storage_base_rate": ss.base_rate,
            "storage_commodity": ss.commodity,
            "storage_commodity_factor": ss.commodity_factor,
            "stock_vals": ss.stock_vals,
            "stock_vals_factor": ss.stock_vals_factor,
            "storage_deductible_level": ss.deductible_level,
            "storage_deductible_level_factor": ss.deductible_level_factor,
            "storage_excess": ss.excess,
            "storage_excess_factor": ss.excess_factor.selected,
            "survey": ss.survey,
            "survey_factor": ss.survey_factor,
            "risk_mgmt": ss.risk_mgmt,
            "risk_mgmt_factor": ss.risk_mgmt_factor,
            "storage_type_of_cover": ss.type_of_cover,
            "storage_type_of_cover_factor": ss.type_of_cover_factor,
            "storage_uw_discretion": ss.uw_discretion,
            "storage_uw_discretion_factor": ss.uw_discretion_factor,
            "storage_rate": ss.rate,
            "avg_val_pcm": ss.avg_val_pcm,
            "cat_expo": ss.cat_expo,
            "combined_cat_load": ss.combined_cat_load,
            **get_countries(ss),
            "non_cat_expo": ss.non_cat_expo,
            "non_cat_load": ss.non_cat_load,
            "storage_technical_deductions": ss.technical_deductions,
            "storage_technical_rate": ss.technical_rate,
            "storage_technical_premium": ss.technical_premium,
            "storage_pct_of_technical": ss.pct_of_technical,
            "storage_actual_rate": ss.actual_rate,
            "storage_quoted_premium": ss.quoted_premium
        }

    elif cds.cover_selection.is_conloss:
        data = {
            # Transit
            "transit_flag": clt.transit_flag,
            "transit_base_rate": clt.base_rate,
            "trans_vals": clt.trans_vals,
            "trans_vals_factor": clt.trans_vals_factor,
            "transit_deductible_level": clt.deductible_level,
            "transit_deductible_level_factor": clt.deductible_level_factor,
            "packaging_1": clt.packaging_1,
            "packaging_1_factor": clt.packaging_1_factor,
            "packaging_2": clt.packaging_2,
            "packaging_2_factor": clt.packaging_2_factor,
            "packaging_factor": clt.packaging_factor,
            "conv_air": clt.conv_air,
            "conv_land": clt.conv_land,
            "conv_sea": clt.conv_sea,
            "conv_air_factor": clt.conv_air_factor,
            "conv_land_factor": clt.conv_land_factor,
            "conv_sea_factor": clt.conv_sea_factor,
            "conv_factor": clt.conv_factor,
            "voyage": clt.voyage,
            "voyage_factor": clt.voyage_factor,
            "surveyor": clt.surveyor,
            "surveyor_factor": clt.surveyor_factor,
            "vessel": clt.vessel,
            "vessel_factor": clt.vessel_factor,
            "transit_uw_discretion": clt.uw_discretion,
            "transit_uw_discretion_factor": clt.uw_discretion_factor,
            "transit_type_of_cover": clt.type_of_cover,
            "transit_type_of_cover_factor": clt.type_of_cover_factor,
            "transit_technical_deductions": clt.technical_deductions,
            "transit_technical_rate": clt.technical_rate,
            "transit_technical_premium": clt.technical_premium,
            "transit_pct_of_technical": clt.pct_of_technical,
            "transit_actual_rate": clt.actual_rate,
            "transit_quoted_premium": clt.quoted_premium,
            # Con Loss
            "storage_flag": clc.conloss_flag,
            "storage_base_rate": clc.base_rate,
            "limit": clc.limit,
            "limit_factor": clc.limit_factor,
            "exposure": clc.exposure,
            "exposure_factor": clc.exposure_factor,
            "indemnity_period": clc.indemnity_period,
            "storage_deductible_level": clc.deductible_level,
            "storage_deductible_level_factor": clc.deductible_level_factor,
            "storage_uw_discretion": clc.uw_discretion,
            "storage_uw_discretion_factor": clc.uw_discretion_factor, 
            "storage_technical_deductions": clc.technical_deductions,
            "storage_technical_rate": clc.technical_rate,
            "storage_technical_premium": clc.technical_premium,
            "storage_pct_of_technical": clc.pct_of_technical,
            "storage_actual_rate": clc.actual_rate,
            "storage_quoted_premium": clc.quoted_premium
        }
    
    # Add standard fields and rating summary
    standard_fields = get_standard_fields(cds, sf, layer)
    rating_summary = get_rating_summary(layer)
    data.update(standard_fields)
    data.update(rating_summary)

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
    if layer.quoted_premium == 0:
        return

    data = create_dict_for_excel(hxd)
    hxd.policy_doc.data_dict = data

    # Compare task data with live data to unhide download button
    task_data = hxd.policy_doc.task_data_dict
    hxd.policy_doc.show_download = True if data == task_data else False
    