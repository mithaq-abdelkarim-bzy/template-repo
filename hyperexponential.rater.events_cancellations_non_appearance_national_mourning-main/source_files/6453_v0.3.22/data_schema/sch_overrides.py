# v0.5.0
import hx_data_schema as hx
import data_schema.sch_utilities as utils
from algorithms.rate_constants import max_layers
from data_schema.sch_rate_change import rarc_task_name


"""
NOTE: The 'override_node_properties' method is not cumulative. If two overrides are added in seperate places 
to the same node in the script, the one added last will override all the others. 
"""

def sch_overrides(cds):

    
    # Override properties
    cds.override_node_properties('cds/standard_fields/underwriter', {'options_table': "table_input_underwriters", 'options_column': "underwriter"})
    cds.override_node_properties('cds/standard_fields/insured_name', {'options_table': "lst_insured_names", 'options_column': "insured_name", "allow_custom_value": True, "async_input": ["task_start_renewal"]})
    cds.override_node_properties('cds/standard_fields/inception_date', {"async_input": ["task_fetch_ihs_data"]})

    # cds.override_node_properties('cds/currencies/source_currency', {'default': "USD"}) # handled on rate change



    # Override values
    cds.override_node_properties("cds/layers",        {"default_element_count": max_layers, "async_input":["task_simulation"]})
    cds.override_node_properties("cds/layers/status",                           {"default":"Rating", "view": {"options": {"read_only": {"read_only": True}}}
                                                                                , "async_output": ["task_start_renewal"]})
    cds.override_node_properties("cds/layers/bpi_case_priced", {"default": 0, "optionality": "required"})
    cds.override_node_properties("cds/standard_fields/is_renewal", {"async_output": [{"task":"task_start_renewal", "reset":False}]})

    cds.override_node_properties("cds/layers/limit",                            {"mode":"output", "async_input": [rarc_task_name, "task_simulation"]})
    cds.override_node_properties("cds/layers/excess",                           {"mode":"output", "async_input": [rarc_task_name, "task_simulation"]})
    cds.override_node_properties("cds/layers/deductible",                       {"mode":"output", "async_input": [rarc_task_name, "task_simulation"]})
    cds.override_node_properties("cds/layers/aggregate_deductible",             {"mode":"output", "async_input": [rarc_task_name, "task_simulation"]})   
    cds.override_node_properties("cds/layers/aggregate_limit",                  {"mode":"output", "async_input": [rarc_task_name, "task_simulation"]})   
    cds.override_node_properties("cds/layers/expected_loss_cost_pre_uw_adj_100",{                 "async_input": [rarc_task_name, "task_simulation"]})


    cds.override_node_properties("cds/layers/brokerage",    {"default": 0, "optionality": "required", "async_input": [rarc_task_name],"view": {"options": {"read_only": {"read_only": True, "label": "Brokerage (excl. PC's)"}}}})
    # cds.override_node_properties("cds/layers/quoted_premium", {"default": 0, "optionality": "required", "async_input": [rarc_task_name], "view": {"options": {"read_only": {"read_only": True}}}})
    # cds.override_node_properties("cds/layers/quoted_premium", {"mode":"output", "optionality": "optionality", "async_input": [rarc_task_name], "view": {"options": {"read_only": {"read_only": True}}}})
    # cds.override_node_properties("cds/layers/section_reference", {"mode":"output", "view": {"options": {"read_only": {"read_only": True}}} })             # Data Schema item '/cds/layers/*/section_reference.view.options.read_only' cannot contain 'read_only' in output values
    cds.override_node_properties("cds/layers/section_reference", {"mode":"output"})
    cds.override_node_properties("cds/layers/written_line", {"view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/benchmark_premium", {"async_input": [rarc_task_name]})

    cds.override_node_properties("cds/layers/rate_change/other_change", {"view": {"label": "Other Change (incl. Brokerage)"}})

    cds.override_node_properties('cds/standard_fields/policy_reference',{ 'mode'            : 'output'})
    cds.override_node_properties('cds/standard_fields/benchmark_class' ,{ 'mode'            : 'output'})
    cds.override_node_properties('cds/standard_fields/trifocus'        ,{ 'mode'            : 'output'})
    cds.override_node_properties('cds/layers/trifocus'                 ,{ 'mode'            : 'output'})

    

