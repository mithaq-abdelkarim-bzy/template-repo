import hx_data_schema as hx
import data_schema.sch_utilities as utils
from hx import params as hx_params
from algorithms.rate_constants import max_curves, peril_reference, max_layers

def sch_overrides(cds):

    cds.override_node_properties("hx_core/inception_date", {"async_output": ["populate_model_task"]})
    cds.override_node_properties("hx_core/expiry_date", {"async_output": ["populate_model_task"]})

    # cds /root

    #NOTE: majority of simulation task async inputs done in sch_simulation
    cds.override_node_properties("cds/programme", {"async_input": ["rate_change_task", "synergy_send_rate_change_task", "send_eso_task", "generate_tags_task"], "async_output": ["populate_model_task"], "view": {"options": {"read_only_option": {"read_only": True}}}})
    cds.override_node_properties("cds/show_other_programme_rate_change", {"async_input": ["rate_change_task"]})
    cds.override_node_properties("cds/show_cat_work_comp_input", {"async_input": ["rate_change_task"]})
    cds.override_node_properties("cds/show_agg_qs_input", {"async_input": ["run_simulation_task"]})
    cds.override_node_properties("cds/show_us_fields", {"async_input": ["rms_el_allocation_task"]})
    cds.override_node_properties("cds/territorial_focus_group", {"async_input": ["generate_tags_task", "synergy_send_rate_change_task", "send_eso_task"], "async_output": ["populate_model_task"], "view": {"options": {"read_only_option": {"read_only": True}}}})
    cds.override_node_properties("cds/territory", {"async_input": ["generate_tags_task"], "async_output": ["populate_model_task"]})
    cds.override_node_properties("cds/currency", {"default": "USD", "view": {"options": {"read_only_option": {"read_only": True}}}, "async_input": ["rms_el_allocation_task", "pull_pml_curves_task", "nmp_calc_task", "synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task"], "async_output": ["populate_model_task"]})
    cds.override_node_properties("cds/calc_type", {"async_input": ["generate_tags_task", "synergy_send_rate_change_task", "send_eso_task"], "async_output": ["populate_model_task"], "view": {"options": {"read_only_option": {"read_only": True}}}})
    cds.override_node_properties("cds/brokerage", {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task"], "async_output": ["populate_model_task"], "view": {"options": {"read_only_option": {"read_only": True}}}})
    cds.override_node_properties("cds/adj_base", {"view": {"options": {"read_only_option": {"read_only": True}}}, "async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["populate_model_task"]})
    cds.override_node_properties("cds/broker_contact", {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task"], "async_output": ["populate_model_task"], "view": {"options": {"read_only_option": {"read_only": True}}}})
    cds.override_node_properties("cds/hours_clause", {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task"], "async_output": ["populate_model_task"], "view": {"options": {"read_only_option": {"read_only": True}}}})
    cds.override_node_properties("cds/sanctions_clause", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["populate_model_task"], "view": {"options": {"read_only_option": {"read_only": True}}}})
    cds.override_node_properties("cds/terrorism_code", {"view": {"options": {"read_only_option": {"read_only": True}}}, "async_output": ["populate_model_task"], "async_input": ["synergy_send_rate_change_task", "send_eso_task"]})
    cds.override_node_properties("cds/cyber_code", {"view": {"options": {"read_only_option": {"read_only": True}}}, "async_output": ["populate_model_task"], "async_input": ["synergy_send_rate_change_task", "send_eso_task"]})
    cds.override_node_properties("cds/com_disease", {"view": {"options": {"read_only_option": {"read_only": True}}}, "async_output": ["populate_model_task"], "async_input": ["synergy_send_rate_change_task", "send_eso_task"]})
    cds.override_node_properties('cds/core_account', {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task"], "async_output": ["populate_model_task"], "view": {"options": {"read_only_option": {"read_only": True}}}})  
    cds.override_node_properties('cds/short_description', {"async_input": ["generate_tags_task", "send_eso_task"], "async_output": ["populate_model_task"]})
    cds.override_node_properties('cds/risk_carrier', {"async_input": ["generate_tags_task", "send_eso_task"], "async_output": ["populate_model_task"], "view": {"options": {"read_only_option": {"read_only": True}}}})
    cds.override_node_properties('cds/deal_status', {"async_input": ["generate_tags_task"], "async_output": ["start_renewal_task", "populate_model_task"]})  # blank on renewal
    cds.override_node_properties('cds/quotation', {"async_output": ["start_renewal_task", "populate_model_task"]})  # blank on renewal
    cds.override_node_properties('cds/discussed_london', {"async_input": ["send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"]})  # blank on renewal
    cds.override_node_properties('cds/technical_underwriter', {"async_input": ["send_eso_task"], "async_output": ["populate_model_task"]})
    cds.override_node_properties('cds/multi_year', {"async_input": ["start_renewal_task", "synergy_send_rate_change_task", "send_eso_task"], "async_output": ["populate_model_task"]})
    cds.override_node_properties('cds/quoted', {"async_output": ["start_renewal_task", "populate_model_task"]})  # blank on renewal

    cds.override_node_properties('cds/currency_policy_financials', {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["populate_model_task"]})
    cds.override_node_properties('cds/summary_fx_conversion', {"async_input": ["synergy_send_rate_change_task", "send_eso_task"]})
    cds.override_node_properties('cds/fx_conversion_label', {"async_input": ["synergy_send_rate_change_task", "send_eso_task"]})
    cds.override_node_properties('cds/summary_uwa_exposure', {"async_input": ["synergy_send_rate_change_task", "send_eso_task"]})
    cds.override_node_properties('cds/uwa_limit_label', {"async_input": ["synergy_send_rate_change_task", "send_eso_task"]})
    cds.override_node_properties('cds/summary_uwa_premium', {"async_input": ["synergy_send_rate_change_task", "send_eso_task"]})
    cds.override_node_properties('cds/uwa_premium_label', {"async_input": ["synergy_send_rate_change_task", "send_eso_task"]})  
    cds.override_node_properties('cds/summary_comments', {"async_input": ["synergy_send_rate_change_task", "send_eso_task"]}) 

    cds.override_node_properties('cds/tp_comments', {"async_output": ["populate_model_task"]})
    cds.override_node_properties('cds/tax', {"async_output": ["populate_model_task"]})
    cds.override_node_properties('cds/treaty_basis', {"async_output": ["populate_model_task"]})  

    cds.override_node_properties('cds/limit_application_ccy_label', {"async_input": ["send_eso_task"]})  
    cds.override_node_properties('cds/excess_application_ccy_label', {"async_input": ["send_eso_task"]})
    cds.override_node_properties('cds/prem_100_label', {"async_input": ["send_eso_task"]})
    cds.override_node_properties('cds/written_line_label', {"async_input": ["send_eso_task"]})
    cds.override_node_properties('cds/estimated_line_label', {"async_input": ["send_eso_task"]})
    cds.override_node_properties('cds/signed_line_label', {"async_input": ["send_eso_task"]})
    cds.override_node_properties('cds/written_epi_label', {"async_input": ["send_eso_task"]})
    cds.override_node_properties('cds/estimated_epi_label', {"async_input": ["send_eso_task"]})
    cds.override_node_properties('cds/signed_epi_label', {"async_input": ["send_eso_task"]})

    cds.override_node_properties('cds/generate_tags_run', {"async_output": ["generate_tags_task"]})

    for i in [
        "case_pricing_analysis_location",
        "deadline_date",
        "underwriter_location",
        "declinature_reason",
        "declinature_comments",
        "ceding_commission",
        "other_acq_costs",
        "includes_us_exposure",
        "market_share",
        "personal_commercial",
        "met_client_last_12_months",
        "carrier_type",
        "named_perils",
        "non_pd_bi",
        "am_best_rating",
        "application_comments"
    ]:
        cds.override_node_properties(f"cds/{i}", {"async_output": ["populate_model_task"]})    
    cds.override_node_properties("cds/show_risk_xl", {"async_input": ["rate_change_task"]})
    

    ## /bi_data
    cds.override_node_properties(f"cds/bi_data/profit", {"async_output": ["bi_data_fetch_task"]})
    cds.override_node_properties(f"cds/bi_data/ilr", {"async_output": ["bi_data_fetch_task"]})
    cds.override_node_properties(f"cds/bi_data/graph_list", {"async_output": ["bi_data_fetch_task"]})

    for i in ["yoa", "exposure", "wep", "incurred", "elr", "cumulative_rate_change"]:
        cds.override_node_properties(f"cds/bi_data/graph_list/{i}", {"async_output": ["bi_data_fetch_task"]})

    ## /standard_fields
    cds.override_node_properties("cds/standard_fields/is_renewal", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": [{"task":"start_renewal_task", "reset": False}, "populate_model_task"], "view": {"options": {"read_only_option": {"read_only": True}}}})
    cds.override_node_properties('cds/standard_fields/underwriter', {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task", "generate_tags_task"], "async_output": ["populate_model_task"], 'options_table': "table_input_underwriters", 'options_column': "underwriter", "async_output": ["populate_model_task"], "view": {"options": {"read_only_option": {"read_only": True}}}})
    cds.override_node_properties('cds/standard_fields/broker', {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task", "generate_tags_task"], "async_output": ["populate_model_task"], 'options_table': "table_input_broker", 'options_column': "broker", "view": {"options": {"read_only_option": {"read_only": True}}}})
    cds.override_node_properties('cds/standard_fields/insured_name', {'options_table': "table_insured", 'options_column': "insured_name", "allow_custom_value": True, "async_input": ["start_renewal_task", "synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task"], "async_output": ["populate_model_task"], "view": {"options": {"read_only_option": {"read_only": True}}}})
    cds.override_node_properties('cds/currencies/source_currency', {'default': "USD"})
    cds.override_node_properties('cds/standard_fields/inception_date', {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task"]})  
    cds.override_node_properties('cds/standard_fields/expiry_date', {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task"]})
    cds.override_node_properties('cds/standard_fields/rating_methodology', {"async_output": ["populate_model_task"]})

    ## /modelling_account_level
    for i in ["rms_ws_curve_selection", "rms_eq_curve_selection", "rms_scs_curve_selection", "rms_eu_ws_curve_selection", "rms_jp_eq_curve_selection", "rms_jp_ws_curve_selection", "rms_can_eq_curve_selection", "rms_caribbean_ws_curve_selection"]:
        cds.override_node_properties(f"cds/modelling_account_level/{i}", {"async_input": ["rms_el_allocation_task"], "async_output": ["start_renewal_task", "populate_model_task"]}) # blank on renewal

    cds.override_node_properties(f"cds/modelling_account_level/comments", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["populate_model_task"]})
    cds.override_node_properties(f"cds/modelling_account_level/ivor_nmp_selection", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["populate_model_task"]})

    ## /peril_allocation_account_level
    for i in ["include_ivor", "allocation_methodology"]:
        cds.override_node_properties(f"cds/peril_allocation_account_level/{i}", {"async_input": ["peril_allocation_task"], "async_output": ["start_renewal_task", "populate_model_task"]}) # blank on renewal

    ## /pml_curves 
    cds.override_node_properties(f"cds/pml_curves/comments", {"async_output": ["populate_model_task"]})

    for i in [
        "rms_curves",
        "air_curves",
        "other_curves"
    ]:
        cds.override_node_properties(f"cds/pml_curves/{i}", {"async_output": ["populate_model_task"]})

    cds.override_node_properties(f"cds/pml_curves/nmp_curves", {"async_output": [{"task": "nmp_calc_task", "reset": False}, "populate_model_task"]})

    for i in ["rms_curves", "air_curves",  "other_curves"]:
        for j in ["rp_loss"]:
            for k in hx_params.table_return_periods["return_period"]:
                cds.override_node_properties(f"cds/pml_curves/{i}/{j}/rp_{k}", {"async_input": ["rms_el_allocation_task", "pull_pml_curves_task"], "async_output": ["start_renewal_task", "populate_model_task"]}) # blank on renewal

    for i in ["rms_curves", "air_curves",  "other_curves"]:
        for j in ["rp_loss_change"]:
            for k in hx_params.table_return_periods["return_period"]:
                cds.override_node_properties(f"cds/pml_curves/{i}/{j}/rp_{k}", {"async_input": ["rms_el_allocation_task", "pull_pml_curves_task"]})

    for i in ["nmp_curves"]:
        for j in ["rp_loss"]:
            for k in hx_params.table_return_periods["return_period"]:
                cds.override_node_properties(f"cds/pml_curves/{i}/{j}/rp_{k}", {"async_input": ["rms_el_allocation_task", "pull_pml_curves_task"], "async_output": ["nmp_calc_task", "start_renewal_task", "populate_model_task"]})  # blank on renewal

    for i in ["nmp_curves"]:
        for j in ["rp_loss_change"]:
            for k in hx_params.table_return_periods["return_period"]:
                cds.override_node_properties(f"cds/pml_curves/{i}/{j}/rp_{k}", {"async_input": ["rms_el_allocation_task", "pull_pml_curves_task", "nmp_calc_task"]})

    for i in ["rms_curves", "air_curves", "other_curves"]:
        for j in ["include_in_peril_alloc", "peril", "curve_description", "currency"]:
            cds.override_node_properties(f"cds/pml_curves/{i}/{j}", {"async_input": ["rms_el_allocation_task", "pull_pml_curves_task"], "async_output": ["populate_model_task"]})

    for i in ["nmp_curves"]:
        for j in ["include_in_peril_alloc", "peril", "curve_description", "currency"]:
            cds.override_node_properties(f"cds/pml_curves/{i}/{j}", {"async_input": ["rms_el_allocation_task", "pull_pml_curves_task"],  "async_output": ["nmp_calc_task", "populate_model_task"]})


    for i in ["curve_aggregator"]:
        for j in ["rp_loss"]:
            for k in hx_params.table_return_periods["return_period"]:
                cds.override_node_properties(f"cds/pml_curves/{i}/{j}/rp_{k}", {"async_output": ["aggregate_curves_task", "start_renewal_task", "populate_model_task"]})  # blank on renewal

    ##  /curve_aggregator 
    cds.override_node_properties(f"cds/curve_aggregator/pml_selections", {"async_input": ["aggregate_curves_task", "peril_allocation_task"], "async_output": ["pull_pml_curves_task", "start_renewal_task", "populate_model_task"]}) # blank on renewal
    cds.override_node_properties(f"cds/curve_aggregator/pml_selections/include_in_aggregator", {"async_input": ["aggregate_curves_task", "peril_allocation_task"], "async_output": ["pull_pml_curves_task", "start_renewal_task", "populate_model_task"]}) # blank on renewal
    cds.override_node_properties(f"cds/curve_aggregator/pml_selections/weight", {"async_input": ["aggregate_curves_task", "peril_allocation_task"], "async_output": ["pull_pml_curves_task", "start_renewal_task", "populate_model_task"]}) # blank on renewal
    cds.override_node_properties(f"cds/curve_aggregator/pml_selections/name", {"async_input": ["aggregate_curves_task", "peril_allocation_task"], "async_output": ["pull_pml_curves_task", "start_renewal_task", "populate_model_task"]}) # blank on renewal

    for i in hx_params.table_return_periods["return_period"]:
        cds.override_node_properties(f"cds/curve_aggregator/pml_selections/rp_loss/rp_{i}", {"async_input": ["aggregate_curves_task", "peril_allocation_task"], "async_output": ["pull_pml_curves_task", "start_renewal_task", "populate_model_task"]}) # blank on renewal

    for i in hx_params.table_return_periods["return_period"]:
        cds.override_node_properties(f"cds/curve_aggregator/aggregator_output/rp_loss/rp_{i}", {"async_input": ["rate_change_task"], "async_output": ["aggregate_curves_task", "start_renewal_task", "populate_model_task"]}) # blank on renewal

    ##  /non_modelled_perils 
    cds.override_node_properties(f"cds/non_modelled_perils_visual/curve_number", {"async_input": ["nmp_calc_task"],  "async_output": ["populate_model_task"]})

    for i in ["broker_pml", "rp", "loss", "peril", "currency", "include_in_summary", "description", "curve"]:
        cds.override_node_properties(f"cds/non_modelled_perils/curve_selections/{i}", {"async_input": ["nmp_calc_task"],  "async_output": ["populate_model_task"]})

    for i in hx_params.table_return_periods["return_period"]:
        cds.override_node_properties(f"cds/non_modelled_perils/pml_broker/rp_{i}", {"async_input": ["nmp_calc_task"],  "async_output": ["populate_model_task"]})
        cds.override_node_properties(f"cds/non_modelled_perils/pml_market/rp_{i}", {"async_input": ["nmp_calc_task"]})

    for i in hx_params.table_return_periods["return_period"]:
        cds.override_node_properties(f"cds/non_modelled_perils/pml_final/rp_{i}", {"async_output": ["nmp_calc_task", "populate_model_task"]})

    ## /exposure
    for i in ["exposure_total", "bespoke_total", "key_zone_total"]:
        cds.override_node_properties(f"cds/exposure/aggregate/perc_change/{i}", {"async_input": ["rate_change_task"]})

    for child in ["exposure_measure", "exposure_comments"]:
        cds.override_node_properties(f"cds/exposure/aggregate/{child}", {"async_output": ["populate_model_task"]})

    ## /experience_rating
    for i in ["year", "gnepi_actual", "gnepi_projected"]:
        cds.override_node_properties(f"cds/experience_rating/exposure/last_eight/{i}", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"]})

    ## quote/
    for field in [
        "roc"
    ]:
        cds.override_node_properties(f"cds/quote/rol_ty/{field}", {"async_input": ["send_eso_task"]})

    ## /summary
    for field in [
        "rol_quote",
        "rol_fot",
        "bpi",
        "fot_adequacy",
        "rms_adequacy",
        "ulr",
        "risk_adjusted_rate_change",
        "epi_adj_rate",
        "prem_full_line",
        "line_written_summary_fx",
        "line_estimated_summary_fx",
        "line_signed_summary_fx",
        "epi_written_summary_fx",
        "epi_estimated_summary_fx",
        "epi_signed_summary_fx",
        "mi_250",
        "mi_250_prem_ratio",
        "mi_10",
        "mi_10_prem_ratio",
    ]:
        cds.override_node_properties(f"cds/summary/ty/{field}", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"]})


    ### /multi_year_summary
    for year in ["ty"]:
        for field in [
            "line_written_summary_fx",
            "line_estimated_summary_fx",
            "line_signed_summary_fx",
            "epi_written_summary_fx",
            "epi_estimated_summary_fx",
            "epi_signed_summary_fx",
            "mi_250",
            "mi_250_estimate_prem_ratio",
            "mi_250_prem_ratio"
        ]:
            cds.override_node_properties(f"cds/summary/multi_year_summary_{year}/{field}", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"]})


    ## /rate_change
    cds.override_node_properties(f"cds/rate_change/comments", {"async_output": ["start_renewal_task", "populate_model_task"]})


    ### /rationale
    for child in [
        "knowledge_comments",
        "portfolio_comments",
        "basis_comments",
        "unusual_comments",
        "facts_comments"
    ]:
        cds.override_node_properties(f"cds/rationale/{child}", {"async_output": ["populate_model_task"]})


    ### /pre_bind
    for i in range(1, 8):
        cds.override_node_properties(f"cds/pre_bind/answer/q_{i}", {"async_output": ["populate_model_task"]})


    ### /post_bind
    for i in range(1, 35):
        cds.override_node_properties(f"cds/post_bind/answer/q_{i}", {"async_output": ["populate_model_task"]})
        cds.override_node_properties(f"cds/post_bind/comments/q_{i}", {"async_output": ["populate_model_task"]})



    # /layers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Cap the total number of layers for rater performance, set default layers to 6
    cds.override_node_properties("cds/layers", {"max_element_count": max_layers, "default_element_count": 6, "async_input": ["start_renewal_task", "synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task"], "async_output": [{"task": "populate_model_task", "reset": False}]})

    cds.override_node_properties(f"cds/layers/limit", {"async_input": ["rms_el_allocation_task", "nmp_calc_task", "run_simulation_task", "synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"], "validation" : {"min_value": 0}, "view": {"options": {"read_only_option": {"read_only": True}}}}) # blank on renewal
    cds.override_node_properties(f"cds/layers/excess", {"async_input": ["rms_el_allocation_task", "nmp_calc_task", "run_simulation_task", "synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"], "validation" : {"min_value": 0}, "view": {"options": {"read_only_option": {"read_only": True}}}}) # blank on renewal
    cds.override_node_properties(f"cds/layers/inner_type", {"async_input": ["run_simulation_task"], "async_output": ["start_renewal_task", "populate_model_task"]}) # blank on renewal
    cds.override_node_properties("cds/layers/aggregate_deductible", {"async_input": ["run_simulation_task", "synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"], "validation" : {"min_value": 0}, "view": {"label": "AAD", "options": {"read_only_option": {"read_only": True}}}}) # blank on renewal
    cds.override_node_properties("cds/layers/number_reins", {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task", "run_simulation_task", "rate_change_task", "run_exposure_simulation_task"], "async_output": ["start_renewal_task", "populate_model_task"], "validation" : {"min_value": 0}, "view": {"options": {"read_only_option": {"read_only": True}}}}) # blank on renewal
    cds.override_node_properties("cds/layers/perc_reins_1", {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task", "run_simulation_task", "rate_change_task", "run_exposure_simulation_task"], "async_output": ["start_renewal_task", "populate_model_task"], "validation" : {"min_value": 0}, "view": {"options": {"read_only_option": {"read_only": True}}}}) # blank on renewal
    cds.override_node_properties("cds/layers/perc_reins_2", {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task", "run_simulation_task", "rate_change_task", "run_exposure_simulation_task"], "async_output": ["start_renewal_task", "populate_model_task"], "validation" : {"min_value": 0}, "view": {"options": {"read_only_option": {"read_only": True}}}}) # blank on renewal
    cds.override_node_properties("cds/layers/perc_reins_3", {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task", "run_simulation_task", "rate_change_task", "run_exposure_simulation_task"], "async_output": ["start_renewal_task", "populate_model_task"], "validation" : {"min_value": 0}, "view": {"options": {"read_only_option": {"read_only": True}}}}) # blank on renewal
    cds.override_node_properties(f"cds/layers/limit_cnv", {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task", "aggregate_curves_task", "rate_change_task", "peril_allocation_task", "run_exposure_simulation_task"]})
    cds.override_node_properties(f"cds/layers/excess_cnv", {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task", "aggregate_curves_task", "rate_change_task", "peril_allocation_task", "run_exposure_simulation_task"]})
    cds.override_node_properties(f"cds/layers/aggregate_deductible_cnv", {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task", "aggregate_curves_task", "rate_change_task", "run_exposure_simulation_task"]})
    cds.override_node_properties("cds/layers/loss_affected", {"async_output": ["start_renewal_task", "populate_model_task"]}) # blank on 
    cds.override_node_properties("cds/layers/renewal_layer", {"async_input": ["rate_change_task"], "async_output": ["start_renewal_task", "populate_model_task"]}) # blank on renewal
    cds.override_node_properties('cds/layers/layer_structure', {"async_input": ["send_eso_task"]})
    cds.override_node_properties('cds/layers/is_facility', {"async_output": ["populate_model_task"]})

    cds.override_node_properties('cds/layers/risk_xl_occurrence_limit_cnv', {"async_input": ["run_exposure_simulation_task"]})
    cds.override_node_properties('cds/layers/risk_xl_occurrence_limit', {"async_output": ["start_renewal_task"]})

    ## mandatory fields  
    cds.override_node_properties("cds/layers/brokerage", {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task"], "mode": "output", "optionality": "optional" ,"view": {"label": "Brokerage (excl. PC's)"}})
    cds.override_node_properties("cds/layers/quoted_premium", {"mode": "output", "optionality": "optional"})
    cds.override_node_properties("cds/layers/written_line", {"mode": "output", "optionality": "optional"})

    cds.override_node_properties("cds/layers/currency", {"view": {"label": "Layer Currency"}, "async_input": ["nmp_calc_task"], "async_output": ["start_renewal_task", "populate_model_task"]}) # blank on renewal
    cds.override_node_properties("cds/layers/section_reference", {"async_input": ["bi_data_fetch_task", "synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task", "start_renewal_task"], "async_output": ["start_renewal_task", "populate_model_task"],  "view": {"options": {"read_only_option": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/leader", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"], "view": {"options": {"read_only_option": {"read_only": True}}}}) # blank on renewal
    cds.override_node_properties("cds/layers/layer_description", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"], "view": {"options": {"read_only_option": {"read_only": True}}}}) # blank on renewal
    cds.override_node_properties("cds/layers/status", {"view": {"options": {"read_only_option": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/bpi_case_priced", {"default": 0, "optionality": "required"})

    ## /rate_change
    cds.override_node_properties("cds/layers/rate_change/risk_adjusted_rate_change", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "view": {"format": utils.percent_format(1)}})

    cds.override_node_properties(f"cds/layers/rate_change/expiring_layer_to_use", {"async_output": ["start_renewal_task", "populate_model_task"]})
    cds.override_node_properties(f"cds/layers/rate_change/exposure_selection", {"async_output": ["start_renewal_task", "populate_model_task"]})

    cds.override_node_properties("cds/layers/rate_change/other_change", {"view": {"label": "Other Change (incl. Brokerage)"}})
    cds.override_node_properties("cds/layers/rate_change/comments", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"]})

    cds.override_node_properties("cds/layers/rate_change/exposure_change_fixed/model_calculated",  {"async_output": ["rate_change_task", "populate_model_task"] })
    cds.override_node_properties(f"cds/layers/rate_change/exposure_change_fixed/uw_selected", {"async_output": ["start_renewal_task", "populate_model_task"]})
    cds.override_node_properties("cds/layers/rate_change/exposure_change_fixed/final",  {"async_input": ["synergy_send_rate_change_task", "send_eso_task"] })
    cds.override_node_properties("cds/layers/rate_change/exposure_change_fixed/comment",  {"async_input": ["synergy_send_rate_change_task", "send_eso_task"] })

    cds.override_node_properties("cds/layers/rate_change/limit_change_fixed/model_calculated",  {"async_output": ["rate_change_task", "populate_model_task"] })
    cds.override_node_properties(f"cds/layers/rate_change/limit_change_fixed/uw_selected", {"async_output": ["start_renewal_task", "populate_model_task"]})
    cds.override_node_properties("cds/layers/rate_change/limit_change_fixed/final",  {"async_input": ["synergy_send_rate_change_task", "send_eso_task"] })
    cds.override_node_properties("cds/layers/rate_change/limit_change_fixed/comment",  {"async_input": ["synergy_send_rate_change_task", "send_eso_task"] })

    cds.override_node_properties("cds/layers/rate_change/risk_characteristics_change_fixed/final",  {"async_input": ["synergy_send_rate_change_task", "send_eso_task"] })
    cds.override_node_properties("cds/layers/rate_change/deductible_change_fixed/final",  {"async_input": ["synergy_send_rate_change_task", "send_eso_task"] })
    cds.override_node_properties("cds/layers/rate_change/terms_conditions_change_fixed/final",  {"async_input": ["synergy_send_rate_change_task", "send_eso_task"] })
    cds.override_node_properties("cds/layers/rate_change/other_change_fixed/final",  {"async_input": ["synergy_send_rate_change_task", "send_eso_task"] })

    cds.override_node_properties(f"cds/layers/rate_change/other_change_fixed/uw_selected", {"async_output": ["start_renewal_task", "populate_model_task"]})
    cds.override_node_properties(f"cds/layers/rate_change/terms_conditions_change_fixed/uw_selected", {"async_output": ["start_renewal_task", "populate_model_task"]})

    cds.override_node_properties("cds/layers/rate_change/rol_ly_to_use",  {"async_input": ["synergy_send_rate_change_task", "send_eso_task"] })
    cds.override_node_properties("cds/layers/rate_change/rol_rebased",  {"async_input": ["synergy_send_rate_change_task", "send_eso_task"] })
    cds.override_node_properties("cds/layers/rate_change/rationale_outside_plan",  {"async_input": ["synergy_send_rate_change_task", "send_eso_task"] })

    ## /nmp
    for i in range(1,max_curves+1):
        for j in ["gross_el", "loss_on_line", "gross_sd"]:
            cds.override_node_properties(f"cds/layers/nmp/non_modelled_perils_{i}/{j}", {"async_output": ["nmp_calc_task", "populate_model_task"]})
            cds.override_node_properties(f"cds/layers/nmp/non_modelled_perils_{i}/include_curve", {"async_output": ["populate_model_task"]})

    for i in [x for x in peril_reference if x != "ap"]:
            cds.override_node_properties(f"cds/layers/nmp/non_modelled_perils_total/peril_el/el_{i}", {"async_input": ["peril_allocation_task"]})

    cds.override_node_properties(f"cds/layers/nmp/non_modelled_perils_total/gross_el_uw", {"async_output": ["populate_model_task"]})
    cds.override_node_properties(f"cds/layers/nmp/non_modelled_perils_total/gross_sd_uw", {"async_output": ["populate_model_task"]})

    ## /quote
    cds.override_node_properties(f"cds/layers/quote/rol_ty/curve_agg_rp_attach", {"async_output": ["aggregate_curves_task", "populate_model_task"]})
    cds.override_node_properties(f"cds/layers/quote/rol_ty/curve_agg_rp_exit", {"async_output": ["aggregate_curves_task", "populate_model_task"]})

    cds.override_node_properties("cds/layers/quote/rol_ty/written_line", {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"], "view": {"options": {"read_only_option": {"read_only": True}}}}) # blank on renewal
    cds.override_node_properties("cds/layers/quote/rol_ty/estimated_signing", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"], "view": {"options": {"read_only_option": {"read_only": True}}}}) # blank on renewal
    cds.override_node_properties("cds/layers/quote/rol_ty/signed_line", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"], "view": {"options": {"read_only_option": {"read_only": True}}}}) # blank on renewal
    
    cds.override_node_properties("cds/layers/quote/rol_ty/gross_lol_weighted", {"async_input": ["rate_change_task"] })

    for i in ["rms_ap", "rms_eq", "rms_ws", "rms_scs", "air_ap", "air_eq", "air_ws", "air_scs", "air_winter", "air_wf"]:
        for j in ["attach", "exit"]:
            cds.override_node_properties(f"cds/layers/quote/rol_ty/{i}_{j}", {"async_output": ["peril_allocation_task", "populate_model_task"]})

    for i in ["weighting_rms", "weighting_ivor", "weighting_air", "weighting_burn"]:
        cds.override_node_properties(f"cds/layers/quote/rol_ty/{i}", {"async_input": ["pull_pml_curves_task", "peril_allocation_task"], "async_output": ["start_renewal_task", "populate_model_task"]}) # blank on renewal

    for i in ["rol_ty"]:
        for j in ["rol_quote", "rol_fot"]:
            cds.override_node_properties(f"cds/layers/quote/{i}/{j}", {"view": {"options": {"read_only_option": {"read_only": True}}}, "async_input": ["rate_change_task", "synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"]}) # blank on renewal

    for i in ["prem_full_line", "ulr", "tpi", "bpi", "est_sign_written_ratio", "rol_afb_tech", "roc"]:
        cds.override_node_properties(f"cds/layers/quote/rol_ty/{i}", {"async_input": ["rate_change_task", "synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task"]})

    cds.override_node_properties(f"cds/layers/quote/rms_tp_calc/override_limit_factor", {"async_output": ["populate_model_task"]})

    ## /risk_xl
    cds.override_node_properties("cds/layers/quote/rol_ty/roev", {"async_input": ["rate_change_task"]})
    cds.override_node_properties("cds/layers/quote/rol_ty/layer_exposure", {"async_input": ["rate_change_task"]})

    for i in ["rol_burn_override", "rp_pml_selection", "rp_pml_selection_peak"]:
        cds.override_node_properties(f"cds/layers/quote/rol_ty/{i}", {"async_output": ["populate_model_task"]})



    ## /model
    cds.override_node_properties(f"cds/layers/model/rms/gross_el", {"async_input": ["rms_el_allocation_task", "synergy_send_rate_change_task", "send_eso_task", "run_exposure_simulation_task"], "async_output": ["start_renewal_task", "populate_model_task"]}) # blank on renewal

    cds.override_node_properties(f"cds/layers/model/rms/perc_us_el", {"async_output": ["populate_model_task"]}) # blank on renewal

    for i in ["ws_el", "eq_el", "scs_el", "eu_ws_el", "jp_ws_el", "jp_eq_el", "can_eq_el", "caribbean_ws_el"]:
        cds.override_node_properties(f"cds/layers/model/rms/{i}", {"async_input": ["peril_allocation_task"], "async_output": ["rms_el_allocation_task", "start_renewal_task", "populate_model_task"]}) # blank on renewal

    for i in ["gross_el_incl_rol", "gross_sd_incl_rol", "additional_rol", "description"]:
        cds.override_node_properties(f"cds/layers/model/nmp/{i}", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"]})

    for model_type in ["total_rms_nmp", "total_ivor_nmp", "total_air_nmp"]:
        for i in ["gross_el", "gross_sd"]:
            cds.override_node_properties(f"cds/layers/model/{model_type}/{i}", { "async_input": ["synergy_send_rate_change_task", "send_eso_task"]})

    ## /peril_allocation
    for i in ["rms_el_approx", "air_el_approx", "final_proportions"]:
        for j in [x for x in peril_reference if x != "ap"]:
            cds.override_node_properties(f"cds/layers/peril_allocation/{i}/el_{j}", {"async_output": ["peril_allocation_task", "start_renewal_task", "populate_model_task"]}) # blank on renewal

    for i in ["rms_aal", "air_aal", "ivor_aal"]:
        for j in [x for x in peril_reference if x != "ap"]:
            cds.override_node_properties(f"cds/layers/peril_allocation/{i}/el_{j}", {"async_input": ["peril_allocation_task"], "async_output": ["start_renewal_task", "populate_model_task"]}) # blank on renewal

    ## /marginal_impacts    
    for item in ["treaty_us","treaty_group","treaty_us_quake","treaty_intl"]:
        for i in ["mi_250", "mi_10"]:
            cds.override_node_properties(f"cds/layers/marginal_impacts/{item}/{i}", {"view": {"options": {"read_only_option": {"read_only": True}}}, "async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"]})  # blank on renewal

    ## /summary
    for i in [
        "rol_quote",
        "rol_fot",
        "reinstatement_description",
        "risk_adjusted_rate_change",
        "bpi",
        "fot_adequacy",
        "rms_adequacy",
        "ulr",
        "epi_adj_rate",
        "prem_full_line",
        "line_written_summary_fx",
        "line_estimated_summary_fx",
        "line_signed_summary_fx",
        "epi_written_summary_fx",
        "epi_estimated_summary_fx",
        "epi_signed_summary_fx",
        "mi_250",
        "mi_250_prem_ratio",
        "mi_10",
        "mi_10_prem_ratio"
    ]:
        cds.override_node_properties(f"cds/layers/summary/ty/{i}", {"async_input": ["synergy_send_front_sheet_task", "synergy_send_rate_change_task", "send_eso_task"]})

    for i in [
        "year_after_next",
        "next_year"        
    ]:
        cds.override_node_properties(f"cds/layers/summary/{i}/section_reference", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"]})

    ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## Other fields to be bank on renewal Or Populate Model Task~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # /additional pages
    cds.override_node_properties(f"cds/send_rate_change/peril_allocation_run", {"async_output": ["start_renewal_task", "peril_allocation_task", "populate_model_task"]})
    cds.override_node_properties(f"cds/send_rate_change/confirm_area_codes", {"async_output": ["start_renewal_task", "populate_model_task"]})
    cds.override_node_properties(f"cds/send_rate_change/confirm_rms_el_allocation", {"async_output": ["start_renewal_task", "populate_model_task"]})
    cds.override_node_properties(f"cds/send_rate_change/confirm_rate_change", {"async_output": ["start_renewal_task", "populate_model_task"]})

    # /exposure
    cds.override_node_properties(f"cds/exposure/granular/exposures", {"async_output": ["populate_model_task"]})
    
    cds.override_node_properties(f"cds/exposure/granular/exposures/ty_aggregate", {"async_output": ["start_renewal_task", "populate_model_task"]})
    cds.override_node_properties(f"cds/exposure/aggregate/ty_aggregates/bespoke_total", {"async_output": ["start_renewal_task", "populate_model_task"]})

    for i in [
        "peril",
        "address_dropdown/country",
        "address_dropdown/state",
        "address_dropdown/county",
        "description",
        "key_zone_selector"
    ]:
        cds.override_node_properties(f"cds/exposure/granular/exposures/{i}", {"async_output": ["populate_model_task"]})



    # /burn input
    cds.override_node_properties(f"cds/experience_rating/claims", {"async_output": ["populate_model_task"]})

    for field in ["coverage_1", "coverage_2", "coverage_3", "coverage_4", "coverage_5", "coverage_6", "coverage_7", "coverage_8"]:
        cds.override_node_properties(f"cds/experience_rating/coverage/{field}", {"async_output": ["populate_model_task"]})

    for field in ["gnepi_exposure_segment", "exposure_segment_1", "exposure_segment_2", "exposure_segment_3"]:
        for index, sub_field in enumerate(["segment_type", "segment_name", "allow_for_rc", "allow_for_other_changes", "inflation_option"]):
            if not((field == "gnepi_exposure_segment") & (index < 2)):
                cds.override_node_properties(f"cds/experience_rating/exposure/{field}/{sub_field}", {"async_output": ["populate_model_task"]})

    cds.override_node_properties(f"cds/experience_rating/exposure/rate_change_gross_net/rate_change", {"async_output": ["populate_model_task"]})
    cds.override_node_properties(f"cds/experience_rating/exposure/comments", {"async_output": ["populate_model_task"]})
    cds.override_node_properties(f"cds/experience_rating/exposure/exposure_start_year", {"async_output": ["populate_model_task"]})
    cds.override_node_properties(f"cds/experience_rating/exposure/burn_start_year", {"async_output": ["populate_model_task"]})

    cds.override_node_properties(f"cds/experience_rating/claims_other/comments", {"async_output": ["populate_model_task"]})
    cds.override_node_properties(f"cds/experience_rating/claims_other/net_or_gross_reins_calc", {"async_output": ["populate_model_task"]})
    cds.override_node_properties(f"cds/experience_rating/claims_other/burn_output_comments", {"async_output": ["populate_model_task"]})


    for field in ["gnepi_loss", "loss_segment_1", "loss_segment_2", "loss_segment_3"]:
        cds.override_node_properties(f"cds/experience_rating/claims/{field}", {"async_output": ["start_renewal_task", "populate_model_task"]})

    for field in ["year", "currency", "description", "large_loss", "coverage", "loss_type", "as_if_loss", "return_period", "comment"]:
        cds.override_node_properties(f"cds/experience_rating/claims/{field}", {"async_output": ["populate_model_task"]}) # dont want to blank on renewal

    # /layers
    ## /model
    for i in ["gross_sd"]: # gross_el done above
        cds.override_node_properties(f"cds/layers/model/rms/{i}", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"]})

    for model_type in ["ivor", "air"]:
        for i in ["gross_el", "gross_sd"]:
            cds.override_node_properties(f"cds/layers/model/{model_type}/{i}", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"]})

    for i in ["additional_rol", "description"]: # gross_el done above
        cds.override_node_properties(f"cds/layers/model/nmp/{i}", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"]})

    for region in ["north_east", "mid_atlantic", "carolinas", "fl_se", "fl_non_se", "al_miss", "louisiana", "tx_east", "tx_west", "cal_south", "cal_north", "pnw", "new_madrid", "hawaii", "mid_west_1", "mid_west_2", "second_event", "ca_wildfire"]:
        cds.override_node_properties(f"cds/layers/rms_regional/{region}", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"]})

    # /burn
    for field in ["coverage_1", "coverage_2", "coverage_3", "coverage_4", "coverage_5", "coverage_6", "coverage_7", "coverage_8"]:
        cds.override_node_properties(f"cds/layers/burn/burn_coverage/{field}", {"async_output": ["populate_model_task"]})

    cds.override_node_properties(f"cds/layers/burn/burn_result/selection", {"async_output": ["populate_model_task"]})


    # /modelling_account_level
    for rds in ["carolinas_ws", "miami_dade_ws", "gulf_ws", "ne_ws", "fl_pinnelas_ws", "la_eq", "nm_eq", "nm_stress_eq", "sf_eq"]:
        cds.override_node_properties(f"cds/modelling_account_level/rds_gross_loss/this_year/{rds}", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"]})

    for rds in ["carolinas_ws", "miami_dade_ws", "gulf_ws", "ne_ws", "fl_pinnelas_ws", "la_eq", "nm_eq", "nm_stress_eq", "sf_eq"]:
        cds.override_node_properties(f"cds/modelling_account_level/rds_gross_loss/yoy_growth/{rds}", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"]})

    # /summary
    cds.override_node_properties(f"cds/layers/summary/year_after_next/share", {"async_output": ["start_renewal_task", "populate_model_task"]})
    cds.override_node_properties(f"cds/layers/summary/next_year/share", {"async_output": ["start_renewal_task", "populate_model_task"]})

    cds.override_node_properties(f"cds/layers/summary/ty/multi_year_period", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", "populate_model_task"]})
    cds.override_node_properties(f"cds/layers/summary/ty/share", {"async_output": ["start_renewal_task", "populate_model_task"]})

    cds.override_node_properties(f"cds/summary_eso_obtained", {"async_output": ["start_renewal_task", "populate_model_task"]})

    # /pre_bind
    cds.override_node_properties(f"cds/pre_bind/uw_signature", {"async_output": ["start_renewal_task", "populate_model_task"]})
    cds.override_node_properties(f"cds/pre_bind/date", {"async_output": ["start_renewal_task", "populate_model_task"]})

    for i in range(1, 8):
        cds.override_node_properties(f"cds/pre_bind/answer/q_{i}", {"async_output": ["start_renewal_task", "populate_model_task"]})


    ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Renewal Task ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # /risk_xl exposure rating
    for index in range(1, 13):
        cds.override_node_properties(f"cds/risk_xl_exposure_rating/exposure_segment_{index}/exposed_limit_ly", {"async_output": ["start_renewal_task"]})

    cds.override_node_properties(f"cds/risk_xl_exposure_rating/exposure_segment_total/exposed_limit_ly", {"async_output": ["start_renewal_task"]})


    # /pml_curves
    for curve_type in ["curve_aggregator", "burn_curve", "rms_curves", "air_curves", "other_curves"]:
        for i in ["rp_2", "rp_5", "rp_10", "rp_25", "rp_50", "rp_100", "rp_200", "rp_250", "rp_500", "rp_1000", "rp_5000", "rp_10000"]:
            cds.override_node_properties(f"cds/pml_curves/{curve_type}/rp_loss_prev/{i}", {"async_input": ["rms_el_allocation_task", "pull_pml_curves_task"], "async_output": ["start_renewal_task", "populate_model_task"]})

    # /pml_curves
    for curve_type in ["nmp_curves"]:
        for i in ["rp_2", "rp_5", "rp_10", "rp_25", "rp_50", "rp_100", "rp_200", "rp_250", "rp_500", "rp_1000", "rp_5000", "rp_10000"]:
            cds.override_node_properties(f"cds/pml_curves/{curve_type}/rp_loss_prev/{i}", {"async_input": ["rms_el_allocation_task", "pull_pml_curves_task", "nmp_calc_task"], "async_output": ["start_renewal_task", {"task": "nmp_calc_task", "reset": False}, "populate_model_task"]})

    # /modelling_account_level
    for rds in ["carolinas_ws", "miami_dade_ws", "gulf_ws", "ne_ws", "fl_pinnelas_ws", "la_eq", "nm_eq", "nm_stress_eq", "sf_eq"]:
        cds.override_node_properties(f"cds/modelling_account_level/rds_gross_loss/previous_year/{rds}", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})

    # /exposure
    for i in ["bespoke_total"]:
        cds.override_node_properties(f"cds/exposure/aggregate/ly_aggregates/{i}", {"async_output": ["start_renewal_task", "populate_model_task"]})

    cds.override_node_properties(f"cds/exposure/granular/exposures/ly_aggregate", {"async_output": ["start_renewal_task", "populate_model_task"]})

    # /experience_rating
    cds.override_node_properties(f"cds/experience_rating/claims/previous_year_total", {"async_output": ["start_renewal_task", "populate_model_task"]})
    cds.override_node_properties(f"cds/experience_rating/exposure/exposure_listing", {"async_output": ["start_renewal_task", "populate_model_task"]})

    for i in ["gnepi_projected", "gnepi_actual", "exposure_value_1", "exposure_value_2", "exposure_value_3", "rate_change", "inflation_option_1", "inflation_option_2", "other_changes"]:
        cds.override_node_properties(f"cds/experience_rating/exposure/exposure_listing/{i}", {"async_output": ["start_renewal_task", "populate_model_task"]})

    # /quote 
    for i in [
        "ulr",
        "tpi",
        "bpi",
        "roc",
        "quote_adequacy",
        "fot_adequacy"
    ]:
        cds.override_node_properties(f"cds/quote/rol_ly/{i}", {"async_input": ["rate_change_task"], "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})

    # /summary
    for i in [
        "line_written_summary_fx",
        "line_estimated_summary_fx",
        "line_signed_summary_fx",

        "epi_written_summary_fx",
        "epi_estimated_summary_fx",
        "epi_signed_summary_fx",

        "mi_250",
        "mi_250_prem_ratio",
        "mi_250_estimate_prem_ratio",
    ]:
        cds.override_node_properties(f"cds/summary/multi_year_summary_ly/{i}", {"async_input": ["synergy_send_rate_change_task", "send_eso_task"], "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})

    for i in [
        "risk_adjusted_rate_change",
        "bpi",
        "fot_adequacy",
        "rms_adequacy",
        "ulr",
        "epi_adj_rate",
        "prem_full_line",
        "mi_250_prem_ratio",
        "mi_10_prem_ratio"            
    ]:
        cds.override_node_properties(f"cds/summary/ly/{i}", {"async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})

    for i in [
        "rol_quote",
        "rol_fot",
        "roc", 
        "risk_adjusted_rate_change",
        "bpi",
        "fot_adequacy",
        "rms_adequacy",
        "ulr",
        "epi_adj_rate",
        "prem_full_line",
        "mi_250_prem_ratio",
        "mi_10_prem_ratio"            
    ]:
        cds.override_node_properties(f"cds/summary/year_before_last/{i}", {"async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})

    for i in [
        "rol_quote",
        "rol_fot",
        "roc",
        "risk_adjusted_rate_change",
        "bpi",
        "fot_adequacy",
        "rms_adequacy",
        "ulr",
        "epi_adj_rate",
        "prem_full_line",
        "mi_250_prem_ratio",
        "mi_10_prem_ratio"            
    ]:
        cds.override_node_properties(f"cds/summary/expiring_year/{i}", {"async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})


    # /layers
    cds.override_node_properties("cds/layers/section_reference_ly", { "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})
    cds.override_node_properties("cds/layers/loss_affected_ly", { "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})
    cds.override_node_properties("cds/layers/renewal_layer_ly", { "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})
    cds.override_node_properties("cds/layers/currency_ly", { "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})
    cds.override_node_properties("cds/layers/leader_ly", { "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})
    cds.override_node_properties("cds/layers/layer_description_ly", { "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})
    cds.override_node_properties("cds/layers/limit_ly", { "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})
    cds.override_node_properties("cds/layers/excess_ly", { "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})
    cds.override_node_properties(f"cds/layers/limit_cnv_ly", {"async_input": ["rate_change_task"], "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})
    cds.override_node_properties(f"cds/layers/excess_cnv_ly", {"async_input": ["rate_change_task"], "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})
    cds.override_node_properties("cds/layers/inner_type_ly", {"async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})
    cds.override_node_properties(f"cds/layers/aggregate_deductible_ly", {"async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})
    cds.override_node_properties(f"cds/layers/aggregate_deductible_cnv_ly", {"async_input": ["rate_change_task"], "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})
    cds.override_node_properties("cds/layers/number_reins_ly", {"async_input": ["rate_change_task"], "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})
    cds.override_node_properties("cds/layers/perc_reins_1_ly", {"async_input": ["rate_change_task"], "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})
    cds.override_node_properties("cds/layers/perc_reins_2_ly", {"async_input": ["rate_change_task"], "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})
    cds.override_node_properties("cds/layers/perc_reins_3_ly", {"async_input": ["rate_change_task"], "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})

    cds.override_node_properties(f"cds/layers/layer_structure_ly", {"async_input": ["rate_change_task"], "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})

    cds.override_node_properties(f"cds/layers/rate_change/expiring_layer_to_use_ly", {"async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})

    cds.override_node_properties("cds/layers/is_facility_ly", {"async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})
    cds.override_node_properties("cds/layers/effective_brokerage_ly", {"async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})

    cds.override_node_properties('cds/layers/risk_xl_occurrence_limit_ly', {"async_output": ["start_renewal_task"]})
    cds.override_node_properties('cds/layers/risk_xl_occurrence_limit_cnv_ly', {"async_output": ["start_renewal_task"]})

    cds.override_node_properties('cds/layers/risk_xl_us_pml_code_ly', {"async_output": ["start_renewal_task"]})
    cds.override_node_properties('cds/layers/risk_xl_intl_pml_code_ly', {"async_output": ["start_renewal_task"]})
    ## /modelling
    for model_type in ["total_rms_nmp", "total_ivor_nmp", "total_air_nmp", "rms", "ivor", "air", "nmp"]:
        for i in ["gross_el", "gross_sd"]:
            cds.override_node_properties(f"cds/layers/model_prev/{model_type}/{i}", { "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})

    for i in ["ws_el", "eq_el", "scs_el", "perc_us_el", "eu_ws_el", "jp_ws_el", "jp_eq_el", "can_eq_el", "caribbean_ws_el"]:
        cds.override_node_properties(f"cds/layers/model_prev/rms/{i}", {"async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})

    for i in ["gross_el_incl_rol", "gross_sd_incl_rol", "additional_rol", "description"]:
        cds.override_node_properties(f"cds/layers/model_prev/nmp/{i}", {"async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})

    for region in ["north_east", "mid_atlantic", "carolinas", "fl_se", "fl_non_se", "al_miss", "louisiana", "tx_east", "tx_west", "cal_south", "cal_north", "pnw", "new_madrid", "hawaii", "mid_west_1", "mid_west_2", "second_event", "ca_wildfire"]:
        cds.override_node_properties(f"cds/layers/rms_regional_prev/{region}", {"async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})

    for item in ["treaty_us","treaty_group","treaty_us_quake","treaty_intl"]:
        for i in ["mi_250", "mi_10"]:
            cds.override_node_properties(f"cds/layers/marginal_impacts_prev/{item}/{i}", {"async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})

    ## /quote
    for i in [
        "rol_rms",
        "rol_ivor", 
        "rol_air", 
        "rol_burn",
        "rol_burn_override",
        "weighting_rms", 
        "weighting_ivor", 
        "weighting_air",
        "weighting_burn",
        "lol_rms", 
        "lol_ivor", 
        "lol_air",
        "lol_burn",
        "lol_weighted", 
        "rol_afb_tech",
        "tpi",
        "roc", 
        "ulr", 
        "bpi",
        "rol_quote",
        "rol_fot",
        "quote_fot_ratio", 
        "prem_full_line", 
        "quote_adequacy",
        "fot_adequacy",
        "rms_adequacy", 
        "written_line",
        "estimated_signing",
        "signed_line",
        "epi_written",
        "epi_estimated", 
        "epi_signed", 
        "rp_quote_break_even",
        "rp_fot_break_even",
        "rp_attach", 
        "rp_exit", 
        "rp_pml_selection",
        "rp_attach_peak",
        "rp_exit_peak", 
        "rp_pml_selection_peak"
        ]:
        cds.override_node_properties(f"cds/layers/quote/rol_ly/{i}", {"async_input": ["rate_change_task"], "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})

        cds.override_node_properties("cds/layers/quote/rol_ly/gross_lol_weighted", {"async_input": ["rate_change_task"], "async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})

    ## risk xl
    cds.override_node_properties("cds/layers/quote/rol_ly/roev", {"async_input": ["rate_change_task"], "async_output": ["start_renewal_task"]})

    cds.override_node_properties("cds/layers/quote/rol_ly/risk_xl_rol_exposure", {"async_output": ["start_renewal_task"]})
    cds.override_node_properties("cds/layers/quote/rol_ly/risk_xl_weighting_exposure", {"async_output": ["start_renewal_task"]})
    cds.override_node_properties("cds/layers/quote/rol_ly/risk_xl_lol_exposure", {"async_output": ["start_renewal_task"]})

    cds.override_node_properties("cds/layers/quote/rol_ly/layer_exposure", {"async_input": ["rate_change_task"], "async_output": ["start_renewal_task"]})
    ## /summary
    for i in [
        "next_year_section_reference",
        "next_year_share",
        "current_year_section_reference",
        "current_year_share",
        "multi_year_period",
        "reinstatement_description",
        "risk_adjusted_rate_change",
        "bpi",
        "fot_adequacy",
        "rms_adequacy",
        "ulr",
        "epi_adj_rate",
        "prem_full_line",
        "mi_250",
        "mi_250_prem_ratio",
        "mi_10",
        "mi_10_prem_ratio"
    ]:
        cds.override_node_properties(f"cds/layers/summary/ly/{i}", {"async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})


    for i in [
        "epi_written",
        "epi_estimated",
        "epi_signed",
        "layer_structure_year_before_last",
        "current_year_section_reference",
        "current_year_share",
        "section_reference",
        "leader",
        "layer_description",
        "limit_cnv",
        "excess_cnv",
        "rol_quote",
        "rol_fot",
        "rol_afb_tech",
        "reinstatement_description",
        "roc",
        "risk_adjusted_rate_change",
        "bpi",
        "fot_adequacy",
        "rms_adequacy",
        "ulr",
        "epi_adj_rate",
        "prem_full_line",
        "written_line",
        "estimated_signing",
        "signed_line",
        "mi_250",
        "mi_250_prem_ratio",
        "mi_10",
        "mi_10_prem_ratio"
    ]:
        cds.override_node_properties(f"cds/layers/summary/year_before_last/{i}", {"async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})

    for i in [
        "epi_written",
        "epi_estimated",
        "epi_signed",
        "layer_structure_expiring_year",
        "section_reference",
        "leader",
        "layer_description",
        "limit_cnv",
        "excess_cnv",
        "rol_quote",
        "rol_fot",
        "rol_afb_tech",
        "reinstatement_description",
        "roc",
        "risk_adjusted_rate_change",
        "bpi",
        "fot_adequacy",
        "rms_adequacy",
        "ulr",
        "epi_adj_rate",
        "prem_full_line",
        "written_line",
        "estimated_signing",
        "signed_line",
        "mi_250",
        "mi_250_prem_ratio",
        "mi_10",
        "mi_10_prem_ratio"
    ]:
        cds.override_node_properties(f"cds/layers/summary/expiring_year/{i}", {"async_output": ["start_renewal_task", {"task": "populate_model_task", "reset": False}]})


    ### /area_codes
    northern_europe_values = ['eat', 'ebe', 'ech', 'edk', 'emz', 'efi', 'efr', 'ege', 'eic', 'eie', 'enl', 'eno', 'egf', 'ese', 'euk', 'euf']
    southern_europe_values = ['ees', 'egr', 'eit', 'ept', 'etu']
    cee_values = ['ebg', 'cef', 'ecx', 'ecz', 'ehu', 'epl', 'ero', 'eru', 'esb', 'esc', 'esr']
    us_values = ['usa01', 'usa02', 'usa03', 'usa04', 'usa05', 'usa06', 'usa07', 'usa08', 'usa09', 'usa10', 'usa11', 'usa12', 'usa13', 'usa14', 'usa15', 'usa16', 'usa20', 'usa21', 'usa22']
    lat_am_values = ['sar', 'sbz', 'sbv', 'sbr', 'scl', 'sco', 'scr', 'sec', 'sel', 'sgt', 'sgy', 'shn', 'smx', 'snq', 'spa', 'spy', 'spe', 'suy', 'sve', 'ofg']
    aus_values = ['oa1', 'oa2', 'oa3', 'oa4', 'oa5', 'oa6', 'ota', 'onz', 'ofj']
    caribbean_values = ['bag', 'bah', 'ban', 'bbb', 'bbh', 'bbm', 'bcb', 'bcm', 'bcu', 'bdo', 'bdr', 'bgn', 'bgs', 'bgu', 'bht', 'bjm', 'bkn', 'bmq', 'bms', 'bon', 'bpr', 'bsl', 'bsv', 'bv1', 'bvs', 'bx7']
    canada_values = ['cbc', 'cqu', 'con', 'cpr', 'cat', 'bpm']
    far_east_values = ['fct', 'fcq', 'fkr', 'fhk', 'fia', 'oph', 'fsp', 'fsk', 'fta', 'fjq', 'fjw', 'mbd', 'fcy', 'ogm', 'fmy', 'mma', 'fby', 'fnp', 'mpk', 'opg', 'fth', 'fvn']
    amei_values = ['mis', 'min', 'asa', 'mae', 'mba', 'aal', 'amo', 'aeg', 'ali', 'amu', 'mjo', 'mom', 'mqa', 'ayt', 'agi']

    non_us_fields = northern_europe_values + southern_europe_values + cee_values + lat_am_values + aus_values + caribbean_values + canada_values + far_east_values + amei_values

    for field in non_us_fields:
        cds.override_node_properties(f"cds/layers/area_codes_select/{field}", {"async_output": ["populate_model_task"]})
        cds.override_node_properties(f"cds/layers/area_codes_perc/{field}", {"async_output": ["populate_model_task"]})

    for field in us_values:
        cds.override_node_properties(f"cds/layers/area_codes_perc/{field}", {"async_output": ["populate_model_task"]})

    cds.override_node_properties(f"cds/layers/area_code_x_eu_ws", {"async_output": ["populate_model_task"]})


