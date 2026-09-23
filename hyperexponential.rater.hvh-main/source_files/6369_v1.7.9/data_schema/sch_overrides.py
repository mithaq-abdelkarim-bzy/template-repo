import hx_data_schema as hx
import data_schema.sch_utilities as utils
from data_schema import sch_params
from algorithms.rate_constants import max_layers
from datetime import datetime

"""
NOTE: The 'override_node_properties' method is not cumulative. If two overrides are added in seperate places 
to the same node in the script, the one added last will override all the others. 
"""
def sch_overrides(cds):
    
    cds.override_node_properties('hx_core/inception_date', {"async_input":["rarc_task","start_renewal_task","set_expiry_date_to_one_year"],"async_output":[{"task": "start_renewal_task", "reset": False}],"view":{"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties('hx_core/expiry_date', {"async_input":["rarc_task"],"async_output":["set_expiry_date_to_one_year"],"view":{"options": {"read_only": {"read_only": True}}}})

    # Override properties
    cds.override_node_properties('cds/standard_fields/underwriter', {'options_table': "table_input_underwriters", 'options_column': "underwriter", "allow_custom_value":True, "view":{"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties('cds/standard_fields/policy_reference', {"view":{"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties('cds/standard_fields/broker', {"async_input":["rarc_task"],'options_table': "table_broker", 'options_column': "Broker","allow_custom_value":True, "view":{"options": {"read_only": {"read_only": True}, "notSupported":{"style_cell":"hx-neutral"}}}})    
    cds.override_node_properties('cds/standard_fields/insured_name', { "async_input": ["start_renewal_task"], "view":{"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties('cds/currencies/source_currency', {'mode':"output"})
    cds.override_node_properties('cds/standard_fields/benchmark_class', {'mode':"output"})
    cds.override_node_properties("cds/standard_fields/rating_methodology", {"async_input": ["rarc_task"]})

    # Override values
    #cds.override_node_properties("cds/layers", {"max_element_count": max_layers, "async_output": ["set_number_of_options"]})
    cds.override_node_properties("cds/layers", {"default_element_count": 6})
    cds.override_node_properties("cds/layers/status", {"options":["Rating Pending", "Quoted", "Bound", "Declined", "Not Taken Up", "Revoked", "Cancelled", "Bound MTA", "Lapsed", "Post Bind Complete"],"view":{"options": {"read_only": {"read_only": True}, "notSupported":{"style_cell":"hx-neutral"}}}})
    cds.override_node_properties("cds/layers/bpi_case_priced", {"default": 0, "optionality": "required"})
    cds.override_node_properties("cds/standard_fields/is_renewal", {"async_output": [{"task":"start_renewal_task", "reset":False}], "view":{"options": {"read_only": {"read_only": True}}}})
    
    cds.override_node_properties("cds/layers/limit", {"async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/excess", {"async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/deductible", {"async_input": ["rarc_task"]})    
    cds.override_node_properties("cds/layers/brokerage", {"mode": "output", "async_input": ["rarc_task"]})
    #cds.override_node_properties("cds/layers/quoted_premium", {"default": 0, "optionality": "required", "async_input": ["rarc_task"], "view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/quoted_premium", {"mode": "output", "async_input": ["rarc_task"], "view":{"label":"Commercial Premium"}})
    cds.override_node_properties("cds/layers/section_reference", {'mode':"output","view":{"label":"Policy Reference"}})
    cds.override_node_properties("cds/layers/written_line",{'mode':"output"})
    cds.override_node_properties("cds/layers/benchmark_premium", {"async_input": ["rarc_task"], "view":{"label":"Benchmark Premium"}})
    cds.override_node_properties("cds/layers/technical_premium", {"async_input": ["rarc_task"],"view":{"label":"Technical Premium"}})
    
    cds.override_node_properties("cds/layers/rate_change/other_change", {"view": {"label": "Other Change (incl. Brokerage)"}})

    cds.override_node_properties('cds/layers/coverages/aop/include_peril/value', {"async_input":["rarc_task"],"view":{"label": "AOP","options": {"read_only": {"read_only": True, "label":"Include Peril"}, "read_only_same_label": {"read_only": True}}}})
    cds.override_node_properties('cds/layers/coverages/ws/include_peril/value', {"async_input":["rarc_task"],"view":{"label": "WS","options": {"read_only": {"read_only": True, "label":"Include Peril"}, "read_only_same_label": {"read_only": True}}}})
    cds.override_node_properties('cds/layers/coverages/eq/include_peril/value', {"default":False,"async_input":["rarc_task"],"view":{"label": "EQ","options": {"read_only": {"read_only": True, "label":"Include Peril"}, "read_only_same_label": {"read_only": True}}}})
    cds.override_node_properties('cds/layers/coverages/fl/include_peril/value', {"default":False,"async_input":["rarc_task"],"view":{"label": "Excess FL","options": {"read_only": {"read_only": True, "label":"Include Peril"}, "read_only_same_label": {"read_only": True}}}})
    cds.override_node_properties('cds/layers/coverages/wildfire/include_peril/value', {"async_input":["rarc_task"],"view":{"label": "Wildfire","options": {"read_only": {"read_only": True, "label":"Include Peril"}, "read_only_same_label": {"read_only": True}}}})
    cds.override_node_properties('cds/layers/coverages/paf/include_peril/value', {"default":False,"async_input":["rarc_task"],"view":{"label": "PAF","options": {"read_only": {"read_only": True, "label":"Include Peril"}, "read_only_same_label": {"read_only": True}}}})
    cds.override_node_properties('cds/layers/coverages/eb/include_peril/value', {"async_input":["rarc_task"],"view":{"label": "Equipment Breakdown","options": {"read_only": {"read_only": True, "label":"Include Peril"}, "read_only_same_label": {"read_only": True}}}})

    cds.override_node_properties('cds/rating_factors/paf/total_modifier_impact/option_to_bind_factor', {"view":{"label": "Total Modifiers Impact"}})

    cds.override_node_properties('cds/layers/coverages/aop/deductible', {"default_index":0,"async_input":["rarc_task", "generate_recommended_peril_inclusions"],"options_table":"table_aop_deductible_options","options_column":"AOP Deductible", "optionality": "required","allow_custom_value":True, "view": {"info":"Excludes Water Damage","options": {"read_only": {"info":"","read_only": True}, "notSupported":{"style_cell":"hx-neutral"}}}})
    cds.override_node_properties('cds/layers/coverages/aop/minimum_deductible', {"view": {"info":"Excludes Water Damage"}})
    cds.override_node_properties('cds/layers/coverages/aop/final_deductible', {"view": {"info":"Excludes Water Damage"}})
    cds.override_node_properties('cds/layers/coverages/wildfire/deductible', {"async_input":["rarc_task","generate_recommended_peril_inclusions"], "async_output":["generate_recommended_peril_inclusions"], "options_data": "../deductible_dropdown", "options_field": "value", "optionality": "optional", "default": 0, "view": {"options": {"read_only": {"read_only": True}, "notSupported":{"style_cell":"hx-neutral"}}}})
    cds.override_node_properties('cds/layers/coverages/eb/deductible', {"default":None,"options":[500,1000],"async_input":["rarc_task"], "optionality": "optional", "view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties('cds/layers/coverages/eq/deductible', {"default":None,"options":[0.03,0.05,0.1],"async_input":["rarc_task"], "optionality": "optional", "view": {"format": utils.percent_format(2),"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties('cds/layers/coverages/ws/minimum_deductible', {"view": {"format": utils.percent_format(2)}})
    cds.override_node_properties('cds/layers/coverages/ws/final_deductible', {"view": {"format": utils.percent_format(2)}})
    cds.override_node_properties('cds/layers/coverages/paf/deductible', {"default_index":0,"async_input":["rarc_task"], "options":[0,100,500,1_000,2_500,5_000,10_000,25_000,50_000], "optionality": "required", "view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties('cds/layers/coverages/ws/deductible', {"mode":"input","options_table":"table_ws_deductible_options","options_column":"WS Deductible", "allow_custom_value":True, "async_input":["rarc_task"],"optionality":"optional","view": {"format": utils.percent_format(0),"options": {"read_only": {"read_only": True}, "notSupported":{"style_cell":"hx-neutral"}}}})
    cds.override_node_properties('cds/layers/coverages/fl/deductible', {"async_input":["rarc_task"],"view": {"options": {"read_only": {"read_only": True}}}})
    
    cds.override_node_properties('cds/layers/kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/ho', {"view": {"format": utils.thousands_format(2)}})
    cds.override_node_properties('cds/layers/kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/eq', {"view": {"format": utils.thousands_format(2)}})
    cds.override_node_properties('cds/layers/kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/excess_flood', {"view": {"format": utils.thousands_format(2)}})
    cds.override_node_properties('cds/layers/kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/equipment_breakdown', {"view": {"format": utils.thousands_format(2)}})


    for peril in ['aop','wildfire','ws','fl','eq']:
        cds.override_node_properties(f'cds/layers/coverages/{peril}/tiv/value', {"view":{"options":{"rationale_page":{"label":"TIV"}}}})
    cds.override_node_properties('cds/layers/coverages/eb/tiv/value', {'mode':"input","default":0,"async_input": ["rarc_task"],"view":{"options":{"rationale_page":{"read_only":True,"label":"TIV"}, "read_only": {"read_only": True}}}})

    cds.override_node_properties('cds/layers/coverages/fl',{"view":{"info":"Building Excess: $250,000\nContents Excess: $100,000"}}) 

    for peril in ['aop','wildfire','liability','eb','ws','eq','fl']:
        label_name = sch_params.all_perils_dict[peril] if peril != 'eb' else 'EB'
        cds.override_node_properties(f'cds/layers/coverages/{peril}/model_premium', {"view":{"label":f"{label_name} Final Expected Losses"}})
        cds.override_node_properties(f'cds/layers/coverages/{peril}/model_rate', {"view":{"label":f"{label_name} Final Loss Rate"}})
