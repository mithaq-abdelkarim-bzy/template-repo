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
    cds.override_node_properties('cds/standard_fields/insured_name', {'options_table': "insured_names", 'options_column': "insured_name", "allow_custom_value": True, "async_input": ["start_renewal_task"]})
    cds.override_node_properties('cds/currencies/source_currency', {'default': "USD", "async_input":["run_simulation_task"],"view":{"label": "Exposure Structure & Premium Currency"}})
    cds.override_node_properties("cds/standard_fields/inception_date", {"async_input": ["run_simulation_task"]})
    cds.override_node_properties("cds/standard_fields/expiry_date", {"async_input": ["run_simulation_task"]})



    # Override values
    cds.override_node_properties("cds/layers", {"max_element_count": max_layers, "async_input":["run_simulation_task"], "default_element_count": 5})
    cds.override_node_properties("cds/layers/status", {"view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/bpi_case_priced", {"default": 0, "optionality": "required"})
    cds.override_node_properties("cds/standard_fields/is_renewal", {"async_output": [{"task":"start_renewal_task", "reset":False}]})
    
    

    cds.override_node_properties("cds/layers/limit", {"async_input": [rarc_task_name,"run_simulation_task"]})
    cds.override_node_properties("cds/layers/excess", {"async_input": [rarc_task_name,"run_simulation_task"]})
    cds.override_node_properties("cds/layers/deductible", {"async_input": [rarc_task_name,"run_simulation_task"]})    
    cds.override_node_properties("cds/layers/brokerage", {"default": 0, "optionality": "required","validation":{"min_value":0.0, "max_value":0.9999}, "async_input": [rarc_task_name,"run_simulation_task"],"view": {"options": {"read_only": {"read_only": True, "label": "Brokerage (excl. PC's)"}}}})
    # cds.override_node_properties("cds/layers/quoted_premium", {"default": 0, "optionality": "required", "async_input": [rarc_task_name], "view": {"options": {"read_only": {"read_only": True}}}})
    # cds.override_node_properties("cds/layers/quoted_premium", {"mode":"output", "optionality": "optionality", "async_input": [rarc_task_name], "view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/section_reference", {"view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/written_line", {"view": {"options": {"read_only": {"read_only": True}},"group":"Beazley Share"}})
    cds.override_node_properties("cds/layers/benchmark_premium", {"async_input": [rarc_task_name]})
    cds.override_node_properties("cds/layers/technical_premium_100", {"view":{"label": "Technical\nPremium", "format": {"thousandSeparated": True, "mantissa": 0}, "group":"100% Gross Share"}})
    cds.override_node_properties("cds/layers/benchmark_premium_100", {"view":{"label": "Benchmark\nPremium", "format": {"thousandSeparated": True, "mantissa": 0}, "group":"100% Gross Share"}})
    cds.override_node_properties("cds/layers/quoted_premium_100", {"view":{"label": "Quoted\nPremium", "format": {"thousandSeparated": True, "mantissa": 0}, "group":"100% Gross Share"}})

    cds.override_node_properties("cds/layers/rate_change/other_change", {"view": {"label": "Other Change (incl. Brokerage)"}})




    

