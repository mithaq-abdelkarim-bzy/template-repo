import hx_data_schema as hx
import data_schema.sch_utilities as utils
from algorithms.rate_constants import max_layers

"""
NOTE: The 'override_node_properties' method is not cumulative. If two overrides are added in seperate places 
to the same node in the script, the one added last will override all the others. 
"""

def sch_overrides(cds):

    
    # Override properties
    cds.override_node_properties('cds/standard_fields/underwriter', {'options_table': "table_input_underwriters", 'options_column': "underwriter", "async_input": ["generate_email_task"] })
    cds.override_node_properties('cds/standard_fields/insured_name', {'options_table': "insured_names", 'options_column': "insured_name", "allow_custom_value": True, "async_input": ["start_renewal_task","generate_email_task"]})
    cds.override_node_properties('cds/currencies/source_currency', {'default': "USD" ,"async_input": ["rarc_task"]})



    # Override values
    cds.override_node_properties("cds/layers", {"max_element_count": max_layers, "default_element_count": 1})
    # cds.override_node_properties("cds/layers/status", {"view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/bpi_case_priced", {"default": 0, "optionality": "required"})
    cds.override_node_properties("cds/standard_fields/is_renewal", {"async_output": [{"task":"start_renewal_task", "reset":False}]})
    

    cds.override_node_properties("cds/layers/limit", {"async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/excess", {"async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/deductible", {"async_input": ["rarc_task"]})    
    # cds.override_node_properties("cds/layers/brokerage", {"default": 0, "optionality": "required", "async_input": ["rarc_task"],"view": {"options": {"read_only": {"read_only": True, "label": "Brokerage (excl. PC's)"}}}})
    # cds.override_node_properties("cds/layers/quoted_premium", {"default": 0, "optionality": "required", "async_input": ["rarc_task"], "view": {"options": {"read_only": {"read_only": True}}}})
    # cds.override_node_properties("cds/layers/section_reference", {"view": {"options": {"read_only": {"read_only": True}}}})
    # cds.override_node_properties("cds/layers/written_line", {"view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/written_line", { "mode": "output", "async_input" : ["rarc_task","generate_email_task","generate_referral_email_task"]})
    cds.override_node_properties("cds/layers/benchmark_premium", {"async_input": ["rarc_task"]})
    
    cds.override_node_properties("cds/layers/rate_change/other_change", {"view": {"label": "Other Change (incl. Brokerage)"}})



    

