# v0.5.0
import hx_data_schema as hx
import data_schema.sch_utilities as utils
from algorithms.rate_constants import max_layers, experience_rating_max_years
from data_schema.sch_rate_change import rarc_task_name


"""
NOTE: The 'override_node_properties' method is not cumulative. If two overrides are added in seperate places 
to the same node in the script, the one added last will override all the others. 
"""

def sch_overrides(cds):
    # Override properties
    cds.override_node_properties('cds/standard_fields/underwriter', {'options_table': "table_input_underwriters", 'options_column': "underwriter","allow_custom_value": True})
    cds.override_node_properties('cds/standard_fields/benchmark_class', {'mode':'output', 'optionality':'optional'})
    
    cds.override_node_properties('cds/standard_fields/insured_name', {'options_table': "insured_names", 'options_column': "insured_name", "allow_custom_value": True, "async_input": ["start_renewal_task"]})
    # see rate change
    # cds.override_node_properties('cds/currencies/source_currency', {'default': "USD","async_input": [rarc_task_name,"steer_format_raw_data_task"]})

    # Override values in cds/layers
    cds.override_node_properties("cds/layers", {"default_element_count":5,"max_element_count": max_layers,"min_element_count": max_layers,"async_input": ["steer_format_raw_data_task","steer_tri_exclusions_setup_task","advanced_features_task","steer_populate_bc_patterns_task"]})
    cds.override_node_properties("cds/layers/status", {"view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/bpi_case_priced", {"default": 0, "optionality": "required","view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/layers/bpi", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/layers/bpi_pre_uw_adj", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/layers/tpi", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/layers/tpi_pre_uw_adj", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/layers/pflr_att", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/layers/pflr_cat", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/layers/pflr", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/layers/roc", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/layers/uw_adj_impact", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    # cds.override_node_properties("cds/layers/currency", {"mode":"output", "optionality": "optional"})
    
    cds.override_node_properties("cds/layers/currency", {"mode":"output", "async_input": [rarc_task_name],"optionality": "optional"})
    
    cds.override_node_properties("cds/layers/limit", {"default":1,"optionality":"required","async_input": [rarc_task_name,"steer_format_raw_data_task","advanced_features_task"], "validation":{"min_value": 1}})
    cds.override_node_properties("cds/layers/excess", {"default":0,"optionality":"required","async_input": [rarc_task_name,"steer_format_raw_data_task","advanced_features_task"]})
    
    cds.override_node_properties("cds/layers/deductible", {"async_input": [rarc_task_name]})    
    cds.override_node_properties("cds/layers/brokerage", {"default": 0, "optionality": "required", "async_input": [rarc_task_name,"advanced_features_task"],"view": {"format": {"output": "percent", "mantissa": 2},"options": {"read_only": {"read_only": True, "label": "Brokerage (excl. PC's)"}}}, "validation":{"min_value": 0, "max_value": 1}})
    cds.override_node_properties("cds/layers/quoted_premium_net_100", {"view":{"label":"Net Quoted\nPremium\n(100%)"}} )    
    
    # cds.override_node_properties("cds/layers/quoted_premium", {"default": 0, "optionality": "required", "async_input": [rarc_task_name], "view": {"options": {"read_only": {"read_only": True}}}})
    # cds.override_node_properties("cds/layers/quoted_premium", {"mode":"output", "optionality": "optional", "async_input": [rarc_task_name], "view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/section_reference", {"async_output": ["start_renewal_task"],"view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/written_line", {"default":0,"optionality":"required","async_input": [rarc_task_name],"view": {"format": {"output": "percent", "mantissa": 2},"options": {"read_only": {"read_only": True}}}, "validation":{"min_value": 0, "max_value": 1}})
    cds.override_node_properties("cds/layers/benchmark_premium", {"async_input": [rarc_task_name]})

    cds.override_node_properties("cds/layers/quoted_premium_100", {"mode":"output", "optionality": "optional", "async_input": [rarc_task_name,"advanced_features_task"],"view":{"label":"Gross\nQuoted\nPremium\n(100%)"}})
    cds.override_node_properties("cds/layers/bkg_gross_or_net", {"async_input": [rarc_task_name], "options":["Gross","Net"]})
    cds.override_node_properties("cds/layers/aggregate_deductible", { "async_input":["advanced_features_task"]})
    
    # Override values in cds/layers/rate_change
    cds.override_node_properties("cds/layers/rate_change/other_change", {"view": {"label": "Other Change (incl. Brokerage)"}})

    # Override values in cds/layers/rate_change
    cds.override_node_properties("cds/layers/upfront_premium_gross_100", {"view": {"label": "Gross\nUpfront\nPremiums\n(100%)"}})
    cds.override_node_properties("cds/layers/upfront_premium_net_100", {"view": {"label": "Net\nUpfront\nPremiums\n(100%)"}})

    cds.override_node_properties("cds/layers/expected_premium_paid_gross_100", {"view": {"label": "Gross\nExpected\nPremium\nPaid\n(100%)"}})
    cds.override_node_properties("cds/layers/expected_premium_paid_net_100", {"view": {"label": "Net\nExpected\nPremium\nPaid\n(100%)"}})


    # Override values in cds/standard_fields
    cds.override_node_properties("cds/standard_fields/is_renewal", {"async_output": [{"task":"start_renewal_task", "reset":False}]})

    cds.override_node_properties(f"cds/pricing_selection/pareto_parameters", {"view": {"label":"Pareto"}})
    cds.override_node_properties(f"cds/pricing_selection/odf_parameters", {"view": {"label":"ODF"}})

    # override UI grouping per layer 
    for i in range(1, max_layers+1):
        group_name = f"Layer {i:02d}"

        # Risk Profile bdx
        for node_name in ["expo_pct","expo_premium","excess","sum_insured","ilf_xs_and_xm","ilf_xs_and_xl","ilf_xs_and_lmt","ilf_xs","pr_pct","pr_net_premium"]:
            cds.override_node_properties(f"cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/layer_{i:02d}/{node_name}", {"view": {"group":group_name}})
        
        # # LAS Current Year
        # for node_name in ["lower", "upper", "ilf_user_input", "ilf_selected", "pct_of_claims_to_layer", "premium", "loss_to_layer"]:
        #     cds.override_node_properties(f"cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/layer_{i:02d}/las/current_year/{node_name}", {"view": {"group":"Current Year"}})
        # # LAS Previous Year and Movement
        # for node_name in ["pct_of_claims_to_layer", "premium", "loss_to_layer"]:
        #     cds.override_node_properties(f"cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/layer_{i:02d}/las/previous_year/{node_name}", {"view": {"group":"Previous Year"}})
        #     cds.override_node_properties(f"cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/layer_{i:02d}/las/movement/{node_name}", {"view": {"group":"Movement"}})
        # # LAS Chart
        # for node_name in ["limit", "this_year", "last_year", "ilf_selected"]:
        #     cds.override_node_properties(f"cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/layer_{i:02d}/las/chart/{node_name}", {"view": {"group":"Chart"}})
    



        cds.override_node_properties(f'cds/layers/no_reinstatement', {"async_input": [rarc_task_name,"advanced_features_task"],'options': ["0","1","2","3","4","5","6","7","8","9","10","Unlimited"]})
        
        cds.override_node_properties(f'cds/layers/risk_profile_bdx/glr_pick', {"async_input": [rarc_task_name],"default":"Cedant LR","optionality":"optional",'options': ["Cedant LR","Burning Cost"]})
        
        ri_prefix_list =[""
            "RI claim", "RI Claim Count", "RI claim On Levelled", "RI claim Count On Levelled"
        ]
        for ri_prefix in ri_prefix_list:
            ri_prefix_clean = ri_prefix.lower().replace(" ","_")
            node_name = f"{ri_prefix_clean}_layer_{i:02d}"
            
            cds.override_node_properties(f"cds/steer/experience_rating/processed_claims/{node_name}", {"async_input": ["steer_tri_exclusions_setup_task", "steer_tri_count_exclusions_setup_task","steer_populate_bc_patterns_task"],"view": {"group":f"{ri_prefix}"}})

    # make Advanced Features result (mode=input, async_output) read.only
    cds.override_node_properties(f"cds/layers/expected_aad", {"async_input": [rarc_task_name],"view":{"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties(f"cds/layers/loss_corridor_loss_cost", {"async_input": [rarc_task_name],"view":{"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties(f"cds/layers/expected_reinstatement_factor", {"async_input": [rarc_task_name],"view":{"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties(f"cds/layers/expected_ncb_pct", {"async_input": [rarc_task_name],"view":{"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties(f"cds/layers/profit_commission", {"async_input": [rarc_task_name],"view":{"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties(f"cds/layers/swing_premium", {"async_input": [rarc_task_name],"view":{"options": {"read_only": {"read_only": True}}}})

    # Triangle async task
    layer_list = ["fgu"] 
    for i in range(1, max_layers+1):
        layer_name = f"layer_{i:02d}"
        layer_list.append(layer_name)
    for layer_name in layer_list:
        cds.override_node_properties(f"cds/steer/experience_rating/layers/{layer_name}/pattern_type",{"async_input": ["steer_populate_bc_patterns_task",rarc_task_name]})
        
        cds.override_node_properties(f"cds/steer/experience_rating/layers/{layer_name}/triangle_projection/incremental_dev_factor/experience_default",{"async_input": ["steer_populate_bc_patterns_task"]})
        cds.override_node_properties(f"cds/steer/experience_rating/layers/{layer_name}/triangle_projection/tail_factor/experience_default",{"async_input": ["steer_populate_bc_patterns_task"]})
        cds.override_node_properties(f"cds/steer/experience_rating/layers/{layer_name}/claim_count/incremental_dev_factor/experience_default",{"async_input": ["steer_populate_bc_patterns_task"]})
        cds.override_node_properties(f"cds/steer/experience_rating/layers/{layer_name}/claim_count/tail_factor/experience_default",{"async_input": ["steer_populate_bc_patterns_task"]})
        
        
        cds.override_node_properties(f"cds/steer/experience_rating/layers/{layer_name}/triangle_projection/incremental_dev_factor/experience_override",{"async_input": ["steer_populate_bc_patterns_task",rarc_task_name]})
        cds.override_node_properties(f"cds/steer/experience_rating/layers/{layer_name}/triangle_projection/tail_factor/experience_override",{"async_input": ["steer_populate_bc_patterns_task",rarc_task_name]})
        cds.override_node_properties(f"cds/steer/experience_rating/layers/{layer_name}/claim_count/incremental_dev_factor/experience_override",{"async_input": ["steer_populate_bc_patterns_task",rarc_task_name]})
        cds.override_node_properties(f"cds/steer/experience_rating/layers/{layer_name}/claim_count/tail_factor/experience_override",{"async_input": ["steer_populate_bc_patterns_task",rarc_task_name]})
        
        cds.override_node_properties(f"cds/steer/experience_rating/layers/{layer_name}/triangle_projection/incremental_dev_factor/experience_selected",{"async_input": [rarc_task_name]})
        cds.override_node_properties(f"cds/steer/experience_rating/layers/{layer_name}/triangle_projection/tail_factor/experience_selected",{"async_input": [rarc_task_name]})
        cds.override_node_properties(f"cds/steer/experience_rating/layers/{layer_name}/claim_count/incremental_dev_factor/experience_selected",{"async_input": [rarc_task_name]})
        cds.override_node_properties(f"cds/steer/experience_rating/layers/{layer_name}/claim_count/tail_factor/experience_selected",{"async_input": [rarc_task_name]})          
        

    # populate steer bc pattern 
    cds.override_node_properties(f"cds/steer/experience_rating/processed_claims",{"async_input": ["steer_populate_bc_patterns_task"]})
    
    async_input_steer_populate_bc = [
            "incurred_claims",
            "inflated_claims",
            "incurred_no_of_claims",
            "inflated_no_of_claims",        
    ]
    for node in async_input_steer_populate_bc:
        cds.override_node_properties(f"cds/steer/experience_rating/processed_claims/{node_name}", {"view": {"group":f"{ri_prefix}"}})


    # override grouping for triangles
    for node_name in ["parametric","curve_type","first_loss","first_loss_factor","param_1","param_2","param_3","param_4"]:
        cds.override_node_properties(f"cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/{node_name}", {"view": {"group":"Parametric Information"}})
    

    for index in range(1,experience_rating_max_years + 1):
        triangle_prefix_list = [
            "Paid",
            "Incurred",
            "Paid Expenses",
            "Incurred Expenses",
            "Paid Claim Indemnity",
            "Incurred Claim Indemnity",
            "Paid Claim Count",
            "Incurred Claim Count",
        ]
        for tri_prefix in triangle_prefix_list:
            tri_prefix_clean = tri_prefix.lower().replace(" ", "_")
            node_name = f"{tri_prefix_clean}_dy_{index:02d}"
            cds.override_node_properties(f"cds/steer/experience_rating/processed_claims/{node_name}", {"view": {"group":f"{tri_prefix} Triangle"}})
    

    # Override values in cds/steer/risk_information
    cds.override_node_properties('cds/technical_price_assumptions/select_class', {"async_input": [rarc_task_name],"default":None,"optionality":"optional",'options_table': "table_cob_code_assumptions", 'options_column': "Class of Business"})
    
    cds.override_node_properties('hx_core/inception_date', {"async_input": [rarc_task_name,"steer_format_raw_data_task","steer_tri_override_setup_task","steer_tri_count_override_setup_task","steer_populate_bc_patterns_task","start_renewal_task"]})
    cds.override_node_properties('hx_core/expiry_date', {"async_input": [rarc_task_name]})
    
    # Override risk bdx
    cds.override_node_properties('cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/cob', {"async_input": [rarc_task_name],"default":None,"optionality":"optional",'options_table': "table_cob_code_assumptions", 'options_column': "Class of Business"})
    cds.override_node_properties('cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/curve', {"async_input": [rarc_task_name],"default":None,"optionality":"optional",'options_table': "table_ilf_curve_list", 'options_column': "Description"})
    cds.override_node_properties('cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/currency', {"optionality":"optional",'options_table': "table_currency", 'options_column': "ccy"})
    

    cds.override_node_properties('cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/excess', {"async_input": [rarc_task_name],"validation":{"min_value":0}})
    cds.override_node_properties('cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/limit', {"async_input": [rarc_task_name],"validation":{"min_value":0}})
    cds.override_node_properties('cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/net_premium', {"async_input": [rarc_task_name],"validation":{"min_value":0}})
    cds.override_node_properties('cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/share', {"async_input": [rarc_task_name],"validation":{"min_value":0}})
    cds.override_node_properties('cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/insured', {"default":"", "async_input":[rarc_task_name],"optionality":"required"})
    cds.override_node_properties('cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/linkage', {"default":"", "async_input":[rarc_task_name],"optionality":"required"})
    
    # Heatlhcare_cat
    cds.override_node_properties('cds/healthcare_cat/trial_history/trial/taken_to_trial', {"validation":{"min_value": 0}})
    cds.override_node_properties('cds/healthcare_cat/trial_history/trial/wins', {"validation":{"min_value": 0}})
    cds.override_node_properties('cds/healthcare_cat/trial_history/trial/losses', {"validation":{"min_value": 0}})
    cds.override_node_properties('cds/healthcare_cat/trial_history/trial/mistrials', {"validation":{"min_value": 0}})

    cds.override_node_properties('cds/healthcare_cat/trial_history/uw_view/from_year', {"validation":{"min_value": 0}})
    cds.override_node_properties('cds/healthcare_cat/trial_history/uw_view/to_year', {"validation":{"min_value": 0}})

    cds.override_node_properties('cds/healthcare_cat/exposure_territory/type_of_business', {"default_index":0,"optionality":"required","options_column":"Exposure Base", "options_table":"table_hc_exp_base"})
    cds.override_node_properties('cds/healthcare_cat/exposure_territory/specialty', {"default_index":0,"optionality":"required","options_column":"Specialty", "options_table":"table_hc_surgical_type"})
    cds.override_node_properties('cds/healthcare_cat/exposure_territory/choose_split_by', {"default":"Premium","optionality":"required","options":["Premium","PIF"]})

    cds.override_node_properties('cds/healthcare_cat/exposure_territory/overall_exposure_per_year/physicians', {"validation":{"min_value": 0}})
    cds.override_node_properties('cds/healthcare_cat/exposure_territory/overall_exposure_per_year/professional_associations', {"validation":{"min_value": 0}})
    cds.override_node_properties('cds/healthcare_cat/exposure_territory/overall_exposure_per_year/ambulatory_surgery_centres', {"validation":{"min_value": 0}})
    cds.override_node_properties('cds/healthcare_cat/exposure_territory/overall_exposure_per_year/hospitals', {"validation":{"min_value": 0}})
    cds.override_node_properties('cds/healthcare_cat/exposure_territory/overall_exposure_per_year/ltc_facilities', {"validation":{"min_value": 0}})
    cds.override_node_properties('cds/healthcare_cat/exposure_territory/overall_exposure_per_year/other_facilities', {"validation":{"min_value": 0}})
    cds.override_node_properties('cds/healthcare_cat/exposure_territory/overall_exposure_per_year/dentists', {"validation":{"min_value": 0}})
    cds.override_node_properties('cds/healthcare_cat/exposure_territory/overall_exposure_per_year/others', {"validation":{"min_value": 0}})

    cds.override_node_properties('cds/healthcare_cat/exposure_territory/exposure_spit_by_state/premium_written', {"validation":{"min_value": 0}})
    

    
    
    only_rarc_as_async_input_nodes = [
        "cds/metadata/rater",
        "cds/layers/include_layer",
        "cds/layers/pricing_selection/risk_profile_bdx/weighting",
        "cds/layers/pricing_selection/limit_average_severity/weighting",
        "cds/layers/pricing_selection/burning_cost/weighting",
        "cds/layers/pricing_selection/clash/weighting",
        "cds/layers/pricing_selection/healthcare_cat/weighting",
        "cds/layers/pricing_selection/other_method/pure_rate",
        "cds/layers/pricing_selection/other_method/weighting",
        "cds/steer/experience_rating/on_levelling/measure",
        "cds/steer/experience_rating/on_levelling/future_inflation",
        "cds/steer/experience_rating/layers/layer_01/burning_cost/weighting",
        "cds/steer/experience_rating/layers/layer_01/burning_cost/premium",
        # "cds/steer/experience_rating/layers/layer_01/pattern_type",
        # "cds/steer/experience_rating/layers/layer_01/triangle_projection/incremental_dev_factor/experience_override",
        # "cds/steer/experience_rating/layers/layer_01/triangle_projection/tail_factor/experience_override",
        # "cds/steer/experience_rating/layers/layer_01/claim_count/incremental_dev_factor/experience_override",
        "cds/steer/experience_rating/layers/layer_02/burning_cost/weighting",
        "cds/steer/experience_rating/layers/layer_02/burning_cost/premium",
        # "cds/steer/experience_rating/layers/layer_02/pattern_type",
        # "cds/steer/experience_rating/layers/layer_02/triangle_projection/incremental_dev_factor/experience_override",
        # "cds/steer/experience_rating/layers/layer_02/triangle_projection/tail_factor/experience_override",
        # "cds/steer/experience_rating/layers/layer_02/claim_count/incremental_dev_factor/experience_override",
        "cds/steer/experience_rating/layers/layer_03/burning_cost/weighting",
        "cds/steer/experience_rating/layers/layer_03/burning_cost/premium",
        # "cds/steer/experience_rating/layers/layer_03/pattern_type",
        # "cds/steer/experience_rating/layers/layer_03/triangle_projection/incremental_dev_factor/experience_override",
        # "cds/steer/experience_rating/layers/layer_03/triangle_projection/tail_factor/experience_override",
        # "cds/steer/experience_rating/layers/layer_03/claim_count/incremental_dev_factor/experience_override",
        "cds/steer/experience_rating/layers/layer_04/burning_cost/weighting",
        "cds/steer/experience_rating/layers/layer_04/burning_cost/premium",
        # "cds/steer/experience_rating/layers/layer_04/pattern_type",
        # "cds/steer/experience_rating/layers/layer_04/triangle_projection/incremental_dev_factor/experience_override",
        # "cds/steer/experience_rating/layers/layer_04/triangle_projection/tail_factor/experience_override",
        # "cds/steer/experience_rating/layers/layer_04/claim_count/incremental_dev_factor/experience_override",
        "cds/steer/experience_rating/layers/layer_05/burning_cost/weighting",
        "cds/steer/experience_rating/layers/layer_05/burning_cost/premium",
        # "cds/steer/experience_rating/layers/layer_05/pattern_type",
        # "cds/steer/experience_rating/layers/layer_05/triangle_projection/incremental_dev_factor/experience_override",
        # "cds/steer/experience_rating/layers/layer_05/triangle_projection/tail_factor/experience_override",
        # "cds/steer/experience_rating/layers/layer_05/claim_count/incremental_dev_factor/experience_override",
        "cds/steer/experience_rating/layers/fgu/burning_cost/weighting",
        "cds/steer/experience_rating/layers/fgu/burning_cost/premium",
        # "cds/steer/experience_rating/layers/fgu/pattern_type",
        # "cds/steer/experience_rating/layers/fgu/triangle_projection/incremental_dev_factor/experience_override",
        # "cds/steer/experience_rating/layers/fgu/triangle_projection/tail_factor/experience_override",
        # "cds/steer/experience_rating/layers/fgu/claim_count/incremental_dev_factor/experience_override",
        "cds/steer/exposure_rating/risk_profile_bdx/exposure_lr",
        # "cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/insured",
        # "cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/linkage",
        "cds/steer/exposure_rating/limit_average_severity/layers/layer_01/risk_profiles/current_year/ilf_user_input",
        "cds/steer/exposure_rating/limit_average_severity/layers/layer_02/risk_profiles/current_year/ilf_user_input",
        "cds/steer/exposure_rating/limit_average_severity/layers/layer_03/risk_profiles/current_year/ilf_user_input",
        "cds/steer/exposure_rating/limit_average_severity/layers/layer_04/risk_profiles/current_year/ilf_user_input",
        "cds/steer/exposure_rating/limit_average_severity/layers/layer_05/risk_profiles/current_year/ilf_user_input",

        "cds/pricing_selection/pareto_parameters/overwrite",
        "cds/pricing_selection/odf_parameters/overwrite",
    ]

    for node in only_rarc_as_async_input_nodes:
        cds.override_node_properties(node, {"async_input": [rarc_task_name]})
    # multiple async_input including rarc
    cds.override_node_properties('cds/layers/advanced_features_input/aad', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0, "max_value": 999999999999} })
    cds.override_node_properties('cds/layers/loss_corridor/min_rate', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0, "max_value": 1}, "validation":{"min_value": 0, "max_value": 1}})
    cds.override_node_properties('cds/layers/loss_corridor/max_rate', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0, "max_value": 1}})
    cds.override_node_properties('cds/layers/loss_corridor/insured_participation', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0, "max_value": 1}})
    cds.override_node_properties('cds/layers/swing_rates/swing_brokerage', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0, "max_value": 1}})
    cds.override_node_properties('cds/layers/swing_rates/use_swing_brokerage', {'async_input': ['advanced_features_task','rarc_task']})
    cds.override_node_properties('cds/layers/swing_rates/deposit_rate', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0, "max_value": 1}})
    cds.override_node_properties('cds/layers/swing_rates/min_rate', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0, "max_value": 1}})
    cds.override_node_properties('cds/layers/swing_rates/max_rate', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0, "max_value": 1}})
    cds.override_node_properties('cds/layers/swing_rates/margin', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0}})
    cds.override_node_properties('cds/layers/swing_rates/loading_factor', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0}})
    cds.override_node_properties('cds/layers/swing_rates/claims_cap_pct', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0}})

    cds.override_node_properties('cds/layers/epi_100', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0}})
    cds.override_node_properties('cds/layers/rate', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0}})

    cds.override_node_properties('cds/layers/ceding_commission', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0, "max_value": 1}})
    cds.override_node_properties('cds/layers/ncb', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0, "max_value": 1}})
    cds.override_node_properties('cds/layers/profit_commission_rate', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0, "max_value": 1}})
    cds.override_node_properties('cds/layers/expense_allowance', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0, "max_value": 1}})
    cds.override_node_properties('cds/layers/cap_gross_pct', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0}})
    cds.override_node_properties('cds/layers/reinstatement_pct_1', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0}})
    cds.override_node_properties('cds/layers/reinstatement_pct_2', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0}})
    cds.override_node_properties('cds/layers/reinstatement_pct_3', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0}})
    cds.override_node_properties('cds/layers/reinstatement_pct_4', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0}})
    cds.override_node_properties('cds/layers/reinstatement_pct_5', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0}})
    cds.override_node_properties('cds/layers/reinstatement_pct_6', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0}})
    cds.override_node_properties('cds/layers/reinstatement_pct_7', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0}})
    cds.override_node_properties('cds/layers/reinstatement_pct_8', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0}})
    cds.override_node_properties('cds/layers/reinstatement_pct_9', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0}})
    cds.override_node_properties('cds/layers/reinstatement_pct_10', {'async_input': ['advanced_features_task','rarc_task'], "validation":{"min_value": 0}})
    
    cds.override_node_properties('cds/risk_information/include_aad', {'async_input': ['advanced_features_task','rarc_task']})
    cds.override_node_properties('cds/risk_information/include_loss_corridor', {'async_input': ['advanced_features_task','rarc_task']})
    cds.override_node_properties('cds/risk_information/include_swing_rates', {'async_input': ['advanced_features_task','rarc_task']})
    # cds.override_node_properties('cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure', {'async_input': ['steer_format_raw_data_task','rarc_task']})
    # cds.override_node_properties('cds/steer/experience_rating/on_levelling/exposure_assumptions/annual_rate_change', {'async_input': ['steer_format_raw_data_task','rarc_task']})
    # cds.override_node_properties('cds/steer/experience_rating/on_levelling/exposure_assumptions/claims_inflation', {'async_input': ['steer_format_raw_data_task','rarc_task']})
    # cds.override_node_properties('cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure_adjusted_layer_01', {'async_input': ['steer_format_raw_data_task','rarc_task']})
    # cds.override_node_properties('cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure_adjusted_layer_02', {'async_input': ['steer_format_raw_data_task','rarc_task']})
    # cds.override_node_properties('cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure_adjusted_layer_03', {'async_input': ['steer_format_raw_data_task','rarc_task']})
    # cds.override_node_properties('cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure_adjusted_layer_04', {'async_input': ['steer_format_raw_data_task','rarc_task']})
    # cds.override_node_properties('cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure_adjusted_layer_05', {'async_input': ['steer_format_raw_data_task','rarc_task']})

    