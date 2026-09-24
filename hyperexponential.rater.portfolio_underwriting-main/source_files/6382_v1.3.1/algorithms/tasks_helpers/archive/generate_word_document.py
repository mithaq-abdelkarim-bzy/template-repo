import hx
import json
import os
from mailmerge import MailMerge
import pandas as pd
import algorithms.rate_utilities as utils
from io import StringIO


def generate_word_document(hxd):
    # Bail out early if global message indicates model isn't finalized
    if hxd.non_cds.global_fields.is_there_global_message:
        hx.errors.fatal("Model is not finalized yet.")

    is_bbt = hxd.cds.risk_information.follow_main_syndicate

    if is_bbt:
        document = merge_word_doc_fields_bbt(hxd)

    else:
        document = merge_word_doc_fields(hxd)
        
    # Finally, write the merged document to storage (via FileField .open)
    with hxd.cds.rationale.word_rationale_template.open("b") as f:
        document.write(f)


def format_composition_string(df):
    # Sort by composition, keep top 5, and format into a readable string
    df_sorted = df.sort_values('composition', ascending=False).head(5)
    return ' '.join(
        f"{row['risk_code']} ({float(row['composition']) * 100:.1f}%)"
        for _, row in df_sorted.iterrows()
    ).strip()


def word_document_helper(hxd):
    results = {}

    # ---------------- Premium & Limit Profile ----------------
    prem_limit_df = utils.pd_df_from_hx_list(hxd.cds.prem_limit_profile.table)
    prem_limit_df = prem_limit_df.dropna(subset=['selected_lob'])
    results['lob'] = ', '.join(prem_limit_df['selected_lob'].astype(str).tolist())
    results['tracker_classes'] = ', '.join(
        prem_limit_df['assigned_trifocus'].unique().astype(str).tolist())

    # ---------------- Deductions ----------------
    deductions_df_str = hxd.non_cds.assumed_deductions.final_deductions_str
    deductions_df = pd.read_csv(
        StringIO(deductions_df_str)).dropna(subset=['selected_lob'])
    combined_df = pd.merge(prem_limit_df, deductions_df,
                           on="selected_lob", how="left")

    deductions = [
        "market_deductions", "mga_fee", "facility_brokerage", "leaders_fee",
        "service_fee", "other", "selected_effective_deductions"
    ]
    total_premium = combined_df["bst_net_premium"].sum()

    # Weighted average of each deduction type across LOBs
    for deduction in deductions:
        results[deduction] = (
            combined_df["bst_net_premium"].fillna(0).dot(
                combined_df[deduction]) / total_premium
            if total_premium else 0
        )

    # ---------------- Risk Code Composition ----------------
    risk_code_df_str = hxd.non_cds.risk_code_composition.final_composition_str
    risk_code_df = pd.read_csv(StringIO(risk_code_df_str))
    grouped_risk_code_df = risk_code_df.groupby(
        'risk_code', as_index=False)['composition'].sum()
    results['big_str'] = format_composition_string(grouped_risk_code_df)

    # ---------------- CDS Summary ----------------
    cds_summary = hxd.cds.prem_limit_profile.summary
    results['max_limit'] = cds_summary.max_limit_at_100_per
    results['average_limit'] = cds_summary.avg_limit_at_100_per
    results['currency'] = hxd.cds.currencies.source_currency
    results['gross'] = cds_summary.bst_share_ultimate_gross_premium
    results['net'] = cds_summary.bst_net_premium

    # ---------------- Cat Loadings ----------------
    cat_loadings = hxd.cds.rating_summary.cat_loadings.summary
    results['total_nmp'] = cat_loadings.nmp_load_general + \
        cat_loadings.nmp_load_weather

    # ---------------- Pricing Adequacy (Pre-Adjustment) ----------------
    pa_pre_adj = hxd.cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_pre_adj

    # Handle summary and table safely in case of missing data
    pricing_adequacy_pre_adj_summary_dict = pa_pre_adj.summary
    if hxd.non_cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_pre_adj.table_str is None:
        pricing_adequacy_pre_adj_table_df = pd.DataFrame({
            'selected_lob': [""],
            'pc_impact': [0],
            'best_estimate': [0],
            'bpi': [0],
            'tpi': [0],
            'roc': [0],
            'pricing_adequacy_pre_adj_df': [0],
        })
    else:
        table_str = hxd.non_cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_pre_adj.table_str
        pricing_adequacy_pre_adj_table_df = pd.read_csv(StringIO(table_str))

    # Extract summary values (fall back to 0 if None)
    results.update({
        'pre_adj_pc_impact_summary': pricing_adequacy_pre_adj_summary_dict.pc_impact or 0,
        'pre_adj_best_estimate_summary': pricing_adequacy_pre_adj_summary_dict.best_estimate or 0,
        'pre_adj_bpi_summary': pricing_adequacy_pre_adj_summary_dict.bpi or 0,
        'pre_adj_tpi_summary': pricing_adequacy_pre_adj_summary_dict.tpi or 0,
        'pre_adj_roc_summary': pricing_adequacy_pre_adj_summary_dict.roc or 0,
        'pricing_adequacy_pre_adj_table_df': pricing_adequacy_pre_adj_table_df,
    })

    # ---------------- Anti-selection & Uncertainty ----------------
    add_loadings = hxd.cds.rating_summary.additional_loadings.summary
    results['anti_uncert_string'] = f"{add_loadings.anti_selection_charge*100:.1f}% / {add_loadings.uncertainty_charge*100:.1f}%"

    # ---------------- Methodology ----------------
    # Merge GN/ULR projections with weights and calculate outputs
    projected_gn_ulr_df = utils.pd_df_from_hx_list(
        hxd.cds.rating_summary.model_gn_ulr.projected_gn_ulr.table)
    model_weights_df = utils.pd_df_from_hx_list(
        hxd.cds.rating_summary.model_gn_ulr.model_weights.table)
    combined_df_2 = pd.merge(
        projected_gn_ulr_df, model_weights_df, on="selected_lob", how="left")

    case_own_experience_total = hxd.cds.rating_summary.model_gn_ulr.model_weights.summary.own_experience
    case_priced_weights_total = hxd.cds.rating_summary.model_gn_ulr.model_weights.summary.case_pricing

    if case_priced_weights_total == 0 and case_own_experience_total == 0:
        combined_df_2["own_experience_outputs"] = combined_df_2["own_exp_gn_ulr"]
    elif case_priced_weights_total > 0:
        combined_df_2["own_experience_outputs"] = combined_df_2["own_exp_gn_ulr"]
    else:
        combined_df_2["own_experience_outputs"] = combined_df_2["case_pricing_x"].fillna(
            0)

    # Choose business plan vs Beazley projections
    business_plan_weights_total = hxd.cds.rating_summary.model_gn_ulr.model_weights.summary.bp_proj
    beazley_projections_weights_total = hxd.cds.rating_summary.model_gn_ulr.model_weights.summary.beazley_proj

    if business_plan_weights_total > 0 or beazley_projections_weights_total > 0:
        combined_df_2["business_plan_outputs"] = combined_df_2["bp_gn_ulr"]
    else:
        combined_df_2["business_plan_outputs"] = combined_df_2["beazley_gn_ulr"]

    # Final merged methodology table
    methods_df = pd.merge(combined_df, combined_df_2,
                          on="selected_lob", how="left")
    methods_output_df = methods_df[[
        'selected_lob', 'bst_net_premium', 'portfolio_composition',
        'own_experience_outputs', 'lloyds_gn_ulr', 'business_plan_outputs',
        'own_experience', 'lloyds_proj', 'bp_proj', 'model_estimate'
    ]]
    results['methods_output_df'] = methods_output_df

    # Weighted totals for methods
    results["own_experience_total"] = combined_df_2["gn_premium"].fillna(
        0).dot(combined_df_2["own_exp_gn_ulr"].fillna(0)) / results['net']
    results["lloyds_total"] = combined_df_2["gn_premium"].fillna(0).dot(
        combined_df_2["lloyds_gn_ulr"].fillna(0)) / results['net']
    results["business_plan_total"] = combined_df_2["gn_premium"].fillna(
        0).dot(combined_df_2["bp_gn_ulr"].fillna(0)) / results['net']

    # ---------------- Pricing ----------------
    cat_df = utils.pd_df_from_hx_list(
        hxd.cds.rating_summary.cat_loadings.cat_allocation)
    additional_loading_df = utils.pd_df_from_hx_list(
        hxd.cds.rating_summary.additional_loadings.additional_pricing_loads)
    final_pricing_df = utils.pd_df_from_hx_list(
        hxd.cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_final_pricing.table)
    pc_structure_df = utils.pd_df_from_hx_list_v2(
        hxd.cds.pc.pc_structure.table)

    if hxd.non_cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_actuarial_basis.table_str is None:
        actuarial_basis_df = pd.DataFrame(
            {'selected_lob': [""], 'pc_impact': [0]})
    else:
        actuarial_basis_df_str = hxd.non_cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_actuarial_basis.table_str
        actuarial_basis_df = pd.read_csv(StringIO(actuarial_basis_df_str))

    # Merge pricing data sources
    pricing_df = methods_df.merge(cat_df, on="selected_lob", how="left") \
        .merge(actuarial_basis_df, on="selected_lob", how="left") \
        .merge(additional_loading_df, on="selected_lob", how="left") \
        .merge(final_pricing_df, on="selected_lob", how="left") \
        .merge(results['pricing_adequacy_pre_adj_table_df'], on="selected_lob", how="left")

    pricing_df["cc_outputs"] = (
        pricing_df["cat"] 
        * pricing_df["climate_change_load"] 
        * pricing_df["model_estimate"]
    ).fillna(0)
    

    pricing_df["nmp_loading"] = (
        pricing_df["nmp_load_general"] 
        + pricing_df["nmp_load_weather"]
    )

    results['pricing_output_df'] = pricing_df[[
        'selected_lob', 'model_estimate', 'nmp_loading', 'cc_outputs',
        'best_estimate_x', 'anti_selection_charge', 'uncertainty_charge',
        'pc_impact_x', 'uw_adj', 'best_estimate_gn'
    ]]

    # Climate change total (weighted)
    combined_df_3 = pd.merge(cat_df, model_weights_df,
                             on="selected_lob", how="left")
    combined_df_3["cc_outputs"] = (
        combined_df_3["cat"] * combined_df_3["climate_change_load"] * combined_df_3["model_estimate"]).fillna(0)
    combined_df_4 = pd.merge(combined_df_3, prem_limit_df,
                             on="selected_lob", how="left")
    results["cc_total"] = combined_df_4["cc_outputs"].fillna(0).dot(
        combined_df_4["bst_net_premium"].fillna(0)) / results['net']

    # ---------------- TAM ----------------
    results['tam_output_df'] = pricing_df[[
        'selected_lob', 'bst_net_premium', 'best_estimate_gn',
        'bpi_x', 'tpi_x', 'roc_x', 'best_estimate_y', 'bpi_y', 'tpi_y', 'roc_y'
    ]]

    # ---------------- Profit Commission ----------------
    results["profit_commision_description"] = generate_profit_commission_description(hxd)

    return results


def generate_profit_commission_description(hxd):
    pc_structure_df = utils.pd_df_from_hx_list_v2(
        hxd.cds.pc.pc_structure.table)

    profit_commission_description = ""

    if hxd.cds.risk_information.is_profit_comission:
        pc_structure_df = pc_structure_df[pc_structure_df["selected_lob"].notna(
        )]
        standard_bool = (pc_structure_df["pc_type"] == "Standard").any()
        sliding_scale_bool = (
            pc_structure_df["pc_type"] == "Sliding Scale").any()
        if standard_bool and sliding_scale_bool:
            profit_commission_description = "PC varies by class of business, refer to profit commission section below"
        else:
            uw_expense = pc_structure_df["uw_expense"].values[0]
            expense_basis = pc_structure_df["expense_basis"].values[0]
            if standard_bool:
                standard_df = utils.pd_df_from_hx_list_v2(
                    hxd.cds.pc.pc_structure.for_standard)
                pc_percent = standard_df["pc_percent"].values[0]
                profit_commission_description = f"{pc_percent * 100:.5f}% after {uw_expense * 100}% Underwriting expenses on {expense_basis}"
            else:
                profit_commission_description = f"Sliding Scale PC after {uw_expense * 100}% Underwriting expenses on {expense_basis}"
    else:
        profit_commission_description = "Not Applicable"

    return profit_commission_description


def generate_bbt_hyperlink(hxd):
    bbt_option_id = hxd.cds.risk_information.bbt_option_id
    
    if not bbt_option_id:
        return ""

    if hx.secrets.environment_name == 'beazley-dev':      
        po_env = 'beazley-dev'
    elif hx.secrets.environment_name == 'beazley-tst':      
        po_env = 'beazley-tst'
    else:                                                   
        po_env = 'beazley'

    link = f"https://{po_env}.hxrenew.com/policy-options/{bbt_option_id}"

    return link


def merge_word_doc_fields_bbt(hxd):

    template = os.path.join(
        os.path.dirname(__file__),
        "..",
        "templates",
        "rationale_template_bbt.docx"
    )

    # Load the MailMerge document with the template
    document = MailMerge(template)

    ri = hxd.cds.risk_information
    sf = hxd.cds.standard_fields
    rs = hxd.cds.rating_summary
    pam = rs.pricing_adequacy_metrics
    add_loadings = hxd.cds.rating_summary.additional_loadings.summary
    cat_loadings = hxd.cds.rating_summary.cat_loadings.summary

    profit_commission_description = generate_profit_commission_description(hxd)
    bbt_hyperlink = generate_bbt_hyperlink(hxd)

    document.merge(
        insured_name=f"{sf.insured_name}",
        policy_reference=f"{sf.policy_reference}",
        underwriter_name=f"{sf.underwriter}",
        facility_type=f"{ri.facility_type}",
        selected_lob=f"{rs.pricing_outputs.bbt_class.selected}",
        tracker_class=f"{rs.pricing_outputs.tracker_class}",
        new_business_or_renewal= "Renewal" if sf.is_renewal else "New Business",
        deal_status=f"{ri.deal_status}",
        inception_date=f"{sf.inception_date}",
        expiry_date=f"{sf.expiry_date}",
        total_deductions=f"{rs.pricing_outputs.deductions_623_2623.selected or 0}%",
        profit_commision_description=f"{profit_commission_description}",
        bbt_hyperlink=f"{bbt_hyperlink}",

        anti_selection_to_uncertainty_ratio=f"{add_loadings.anti_selection_charge*100:.1f}% / {add_loadings.uncertainty_charge*100:.1f}%",
        percent_impact_on_ulr=f"{(pam.pricing_adequacy_actuarial_basis.summary.pc_impact or 0)*100:.1f}%",
        gn_ulr_net_of_pc=f"{(pam.pricing_adequacy_actuarial_basis.summary.best_estimate or 0)*100:.1f}%",
        bpi=f"{(pam.pricing_adequacy_final_pricing.summary.bpi or 0) * 100:.1f}%",
        tpi=f"{(pam.pricing_adequacy_final_pricing.summary.tpi or 0) * 100:.1f}%",
        roc=f"{(pam.pricing_adequacy_final_pricing.summary.roc or 0) * 100:.1f}%",
        percent_impact_on_ulr_excl=f"{(pam.pricing_adequacy_pre_adj.summary.pc_impact or 0)*100:.1f}%",
        gn_ulr_net_of_pc_excl=f"{(pam.pricing_adequacy_pre_adj.summary.best_estimate or 0)*100:.1f}%",
        bpi_excl=f"{(pam.pricing_adequacy_pre_adj.summary.bpi or 0) * 100:.1f}%",
        tpi_excl=f"{(pam.pricing_adequacy_pre_adj.summary.tpi or 0) * 100:.1f}%",
        roc_excl=f"{(pam.pricing_adequacy_pre_adj.summary.roc or 0) * 100:.1f}%",
        
        pricing_year=f"{sf.inception_date.year}",
        rationale_1=f"{hxd.cds.rationale.key_information}",
        rationale_2=f"{hxd.cds.rationale.rationale_assumptions}",
        rationale_3=f"{hxd.cds.rationale.rationale_methodology}",
        rationale_4=f"{hxd.cds.rationale.key_uncertainties}",
        
        pricing_selected_gnulr_total=f"{pam.pricing_adequacy_pre_adj.summary.best_estimate * 100:.1f} %",
        pricing_antiselection_total=f"{rs.additional_loadings.summary.anti_selection_charge * 100:.1f} %",
        pricing_uncertainty_total=f"{rs.additional_loadings.summary.uncertainty_charge * 100:.1f} %",
        pricing_pc_impact_on_gnulr_total=f"{pam.pricing_adequacy_actuarial_basis.summary.pc_impact * 100:.1f} %",
        pricing_uw_adj_total=f"{(pam.pricing_adequacy_final_pricing.summary.uw_adj or 0) * 100:.1f} %",
        pricing_selected_gnulr_final_total=f"{(pam.pricing_adequacy_final_pricing.summary.best_estimate_gn or 0) * 100:.1f} %",
        
        # tam_gn_premium_total=f"{hxd.cds.prem_limit_profile.summary.bst_net_premium:.1f}",
        tam_selected_gnulr_total=f"{(pam.pricing_adequacy_final_pricing.summary.best_estimate_gn or 0) * 100:.1f} %",
        tam_bpi_total=f"{(pam.pricing_adequacy_final_pricing.summary.bpi or 0) * 100:.1f} %",
        tam_tpi_total=f"{(pam.pricing_adequacy_final_pricing.summary.tpi or 0) * 100:.1f} %",
        tam_roc_total=f"{(pam.pricing_adequacy_final_pricing.summary.roc or 0) * 100:.1f} %",
        tam_gnulr_excl_total=f"{(pam.pricing_adequacy_pre_adj.summary.best_estimate or 0) * 100:.1f} %",
        tam_bpi_excl_total=f"{(pam.pricing_adequacy_pre_adj.summary.bpi or 0) * 100:.1f} %",
        tam_tpi_excl_total=f"{(pam.pricing_adequacy_pre_adj.summary.tpi or 0) * 100:.1f} %",
        tam_roc_excl_total=f"{(pam.pricing_adequacy_pre_adj.summary.roc or 0) * 100:.1f} %",
        
        tpi_rating_summary_year=f"{rs.technical_premium_build_up.tpi_year.selected}",
    )

    return document


def merge_word_doc_fields(hxd):
    
    template = os.path.join(
        os.path.dirname(__file__),
        "..",
        "templates",
        "rationale_template.docx"
    )

    # Load the MailMerge document with the template
    document = MailMerge(template)

    # Get helper-calculated results
    results = word_document_helper(hxd)
    pam = hxd.cds.rating_summary.pricing_adequacy_metrics
    ri = hxd.cds.risk_information
    sf = hxd.cds.standard_fields
    rs = hxd.cds.rating_summary

    # Merge in scalar fields into the Word template
    document.merge(
        insured_name=f"{sf.insured_name}",
        policy_reference=f"{sf.policy_reference}",
        underwriter_name=f"{sf.underwriter}",
        facility_type=f"{ri.facility_type}",
        deal_status=f"{ri.deal_status}",
        priced_by=f"{ri.priced_by}",
        selected_lob_list=f"{results['lob']}",
        tracker_classes_list=f"{results['tracker_classes']}",
        top_five_risk_codes=f"{results['big_str']}",
        new_business_or_renewal= "Renewal" if sf.is_renewal else "New Business",
        inception_date=f"{sf.inception_date}",
        expiry_date=f"{sf.expiry_date}",
        rationale_1=f"{hxd.cds.rationale.key_information}",
        rationale_2=f"{hxd.cds.rationale.rationale_assumptions}",
        rationale_3=f"{hxd.cds.rationale.rationale_methodology}",
        rationale_4=f"{hxd.cds.rationale.key_uncertainties}",
        bst_share=f"{hxd.cds.prem_limit_profile.summary.bst_share_line_size * 100:.1f}%",
        max_to_average_limit_ratio=f"{results['currency']} {results['max_limit']/1000000:.1f}m / {results['currency']} {results['average_limit']/1000000:.1f}m",
        ultimate_to_net_premium_ratio=f"{results['currency']} {results['gross']/1000000:.1f}m GROSS / {results['currency']} {results['net']/1000000:.1f}m NET",
        market_deductions=f"{results['market_deductions']*100:.1f}",
        consortium_fee=f"{results['mga_fee']*100:.1f}",
        facility_brokerage=f"{results['facility_brokerage']*100:.1f}",
        leaders_fee=f"{results['leaders_fee']*100:.1f}",
        service_fee=f"{results['service_fee']*100:.1f}",
        other_fee=f"{results['other']*100:.1f}",
        total_deductions=f"{results['selected_effective_deductions']*100:.1f}",
        profit_commision_description=f"{results['profit_commision_description']}",
        anti_selection_to_uncertainty_ratio=results['anti_uncert_string'],
        percent_impact_on_ulr=f"{(pam.pricing_adequacy_actuarial_basis.summary.pc_impact or 0)*100:.1f}%",
        gn_ulr_net_of_pc=f"{(pam.pricing_adequacy_actuarial_basis.summary.best_estimate or 0)*100:.1f}%",
        bpi=f"{(pam.pricing_adequacy_final_pricing.summary.bpi or 0) * 100:.1f}%",
        tpi=f"{(pam.pricing_adequacy_final_pricing.summary.tpi or 0) * 100:.1f}%",
        roc=f"{(pam.pricing_adequacy_final_pricing.summary.roc or 0) * 100:.1f}%",
        percent_impact_on_ulr_excl=f"{results['pre_adj_pc_impact_summary'] * 100:.1f}%",
        gn_ulr_net_of_pc_excl=f"{results['pre_adj_best_estimate_summary'] * 100:.1f}%",
        bpi_excl=f"{results['pre_adj_bpi_summary'] * 100:.1f}%",
        tpi_excl=f"{results['pre_adj_tpi_summary'] * 100:.1f}%",
        roc_excl=f"{results['pre_adj_roc_summary'] * 100:.1f}%",
        tpi_rating_summary_year=f"{rs.technical_premium_build_up.tpi_year.selected}"
    )

    # -------------------------------
    # Methodology table (loop over DF)
    # -------------------------------
    layers_copy = []
    for index, row in results['methods_output_df'].iterrows():
        layers_copy.append({
            "gnulr_cob": f"{row['selected_lob']}",
            "gnulr_premium": f"{row['bst_net_premium']:.1f}",
            "gnulr_percent_of_portfolio": f"{row['portfolio_composition'] * 100:.1f}%",
            "gnulr_own_experience": f"{row['own_experience_outputs'] * 100:.1f}%",
            "gnulr_lloyds_risk_codes": f"{row['lloyds_gn_ulr'] * 100:.1f}%",
            "gnulr_business_plan": f"{row['business_plan_outputs'] * 100:.1f}%",
            "gnulr_weightings_own_experience": f"{row['own_experience'] * 100:.1f}%",
            "gnulr_weightings_lloyds_risk_codes": f"{row['lloyds_proj'] * 100:.1f}%",
            "gnulr_weightings_business_plan": f"{row['bp_proj'] * 100:.1f}%",
            "gnulr_model_percent": f"{row['model_estimate'] * 100:.1f}%"
        })
    document.merge_rows("gnulr_cob", layers_copy)

    # Merge totals for methodology table
    document.merge(
        gnulr_premium_total=f"{hxd.cds.prem_limit_profile.summary.bst_net_premium:.1f}",
        gnulr_own_experience_total=f"{results['own_experience_total'] * 100:.1f} %",
        gnulr_lloyds_risk_codes_total=f"{results['lloyds_total'] * 100:.1f} %",
        gnulr_business_plan_total=f"{results['business_plan_total'] * 100:.1f} %",
        gnulr_weightings_own_experience_total=f"{rs.model_gn_ulr.model_weights.summary.own_experience * 100:.1f} %",
        gnulr_weightings_lloyds_risk_codes_total=f"{rs.model_gn_ulr.model_weights.summary.lloyds_proj * 100:.1f} %",
        gnulr_weightings_business_plan_total=f"{rs.model_gn_ulr.model_weights.summary.bp_proj * 100:.1f} %",
        gnulr_model_percent_total=f"{rs.model_gn_ulr.model_weights.summary.model_estimate * 100:.1f} %",
    )

    # -------------------------
    # Pricing table (loop over DF)
    # -------------------------
    layers_copy = []
    for index, row in results['pricing_output_df'].iterrows():
        layers_copy.append({
            "pricing_cob": f"{row['selected_lob']}",
            "pricing_model_gnulr_percent": f"{row['model_estimate']*100:.1f}%",
            "pricing_nmp_loading": f"{row['nmp_loading'] * 100:.1f}%",
            "pricing_cc_load": f"{row['cc_outputs'] * 100:.1f}%",
            "pricing_selected_gnulr": f"{row['best_estimate_x'] * 100:.1f}%",
            "pricing_antiselection": f"{row['anti_selection_charge'] * 100:.1f}%",
            "pricing_uncertainty": f"{row['uncertainty_charge'] * 100:.1f}%",
            "pricing_pc_impact_on_gnulr": f"{row['pc_impact_x'] * 100:.1f}%",
            "pricing_uw_adj": f"{row['uw_adj'] * 100:.1f}%",
            "pricing_selected_gnulr_final": f"{row['best_estimate_gn'] * 100:.1f}%"
        })

    document.merge_rows("pricing_cob", layers_copy)
    
    # Merge totals for pricing table
    document.merge(
        pricing_model_gnulr_percent_total=f"{rs.model_gn_ulr.model_weights.summary.model_estimate * 100:.1f}%",
        pricing_nmp_loading_total=f"{results['total_nmp'] * 100:.1f} %",
        pricing_cc_load_total=f"{results['cc_total'] * 100:.1f} %",
        pricing_selected_gnulr_total=f"{results['pre_adj_best_estimate_summary'] * 100:.1f} %",
        pricing_antiselection_total=f"{rs.additional_loadings.summary.anti_selection_charge * 100:.1f} %",
        pricing_uncertainty_total=f"{rs.additional_loadings.summary.uncertainty_charge * 100:.1f} %",
        pricing_pc_impact_on_gnulr_total=f"{rs.pricing_adequacy_metrics.pricing_adequacy_actuarial_basis.summary.pc_impact * 100:.1f} %",
        pricing_uw_adj_total=f"{(rs.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary.uw_adj or 0) * 100:.1f} %",
        pricing_selected_gnulr_final_total=f"{(rs.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary.best_estimate_gn or 0) * 100:.1f} %",
    )

    # ----------------------
    # TAM table (loop over DF)
    # ----------------------
    bst_percent_total = 0
    layers_copy = []
    for index, row in results['tam_output_df'].iterrows():
        layers_copy.append({
            "tam_cob": f"{row['selected_lob']}",
            "tam_gn_premium": f"{row['bst_net_premium']:.1f}",
            "tam_selected_gnulr": f"{row['best_estimate_gn'] * 100:.1f}%",
            "tam_bpi": f"{row['bpi_y'] * 100:.1f}%",
            "tam_tpi": f"{row['tpi_y'] * 100:.1f}%",
            "tam_roc": f"{row['roc_y'] * 100:.1f}%",
            "tam_gnulr_excl": f"{row['best_estimate_y'] * 100:.1f}%",
            "tam_bpi_excl": f"{row['bpi_x'] * 100:.1f}%",
            "tam_tpi_excl": f"{row['tpi_x'] * 100:.1f}%",
            "tam_roc_excl": f"{row['roc_x'] * 100:.1f}%"
        })
        # Increment weighted portfolio percentage
        bst_percent_total += 0 if results['net'] == 0 else (
            row['bst_net_premium'] or 0)/results['net']

    document.merge_rows("tam_cob", layers_copy)

    # Merge totals for TAM table
    document.merge(
        gnulr_percent_of_portfolio_total=f"{bst_percent_total * 100:.1f} %",
        tam_gn_premium_total=f"{hxd.cds.prem_limit_profile.summary.bst_net_premium:.1f}",
        tam_selected_gnulr_total=f"{(rs.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary.best_estimate_gn or 0) * 100:.1f} %",
        tam_bpi_total=f"{(rs.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary.bpi or 0) * 100:.1f} %",
        tam_tpi_total=f"{(rs.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary.tpi or 0) * 100:.1f} %",
        tam_roc_total=f"{(rs.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary.roc or 0) * 100:.1f} %",
        tam_gnulr_excl_total=f"{(results['pre_adj_best_estimate_summary'] or 0) * 100:.1f} %",
        tam_bpi_excl_total=f"{(results['pre_adj_bpi_summary'] or 0) * 100:.1f} %",
        tam_tpi_excl_total=f"{(results['pre_adj_tpi_summary'] or 0) * 100:.1f} %",
        tam_roc_excl_total=f"{(results['pre_adj_roc_summary'] or 0) * 100:.1f} %"
    )

    return document