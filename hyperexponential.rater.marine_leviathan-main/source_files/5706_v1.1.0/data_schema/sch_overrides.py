import hx_data_schema as hx
import data_schema.sch_utilities as utils
from algorithms.rate_constants import max_layers

"""
NOTE: The 'override_node_properties' method is not cumulative. If two overrides are added in seperate places 
to the same node in the script, the one added last will override all the others. 
"""

def sch_overrides(cds):

    
    # Override properties
    cds.override_node_properties('cds/standard_fields/policy_reference', {"async_input": ["insert_hx_meta_policy_references_task"]})
    cds.override_node_properties('cds/standard_fields/underwriter', {'options_table': "table_input_underwriters", 'options_column': "underwriter"})
    cds.override_node_properties('cds/standard_fields/insured_name', {'options_table': "insured_names", 'options_column': "insured_name", "allow_custom_value": True, "async_input": ["start_renewal_task"]})
    cds.override_node_properties("cds/currencies/source_currency", {"default": "USD", "optionality":"optional", "options" : ["AUD", "CAD", "DKK", "EUR", "GBP", "JPY", "NOK", "SGD", "USD"] , "async_input": ["start_renewal_task"]})




    # Override values
    cds.override_node_properties("cds/layers", {"max_element_count": max_layers})
    cds.override_node_properties("cds/layers/status", {"view": {"options": {"read_only": {"read_only": True}}},"async_input": ["start_renewal_task"]})
    cds.override_node_properties("cds/layers/bpi_case_priced", {"default": 0, "optionality": "required"})
    cds.override_node_properties("cds/standard_fields/is_renewal", {"async_output": [{"task":"start_renewal_task", "reset":False}]})
    cds.override_node_properties("cds/standard_fields/is_rater_priced", {"async_input": ["policy_to_excel_task"]})
    
   
    cds.override_node_properties('hx_core/inception_date', {"default" : "2025-01-01","async_input": ["rarc_task"]})
    cds.override_node_properties('hx_core/expiry_date', {"default" : "2026-01-01", "async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/limit", {"async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/excess", {"async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/deductible", {"async_input": ["rarc_task"]})    
    cds.override_node_properties("cds/layers/brokerage", {"default": 0, "optionality": "required", "async_input": ["rarc_task"],"view": {"options": {"read_only": {"read_only": True, "label": "Brokerage (excl. PC's)"}}}})
    cds.override_node_properties("cds/layers/quoted_premium", {"default": 0, "optionality": "required", "async_input": ["rarc_task"], "view": {"options": {"read_only": {"read_only": True}}}})
    #cds.override_node_properties("cds/layers/section_reference", {"view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/written_line", {"view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties("cds/layers/benchmark_premium", {"async_input": ["rarc_task"]})
    
    cds.override_node_properties("cds/layers/rate_change/other_change", {"view": {"label": "Other Change (incl. Brokerage)"}})
    #cds.override_node_properties("cds/layers/benchmark_premium", {"view": {"label": "Gross brokerage"}})
    #cds.override_node_properties("cds/layers/technical_premium", {"view": {"label": "Gross brokerage"}})
    #cds.override_node_properties("cds/layers/technical_premium_net", {"view": {"label": "Net brokerage"}})
    #cds.override_node_properties("cds/layers/technical_premium_pre_uw_adj", {"view": {"label": "Gross brokerage"}})
    #cds.override_node_properties("cds/layers/tpi_pre_uw_adj", {"view": {"label": "TPI"}})
    

    cds.override_node_properties("cds/layers/section_reference", {"mode" : "output"})
    cds.override_node_properties("cds/layers/brokerage", {"mode" : "output", "async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/written_line", {"mode" : "output", "async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/quoted_premium", {"mode" : "output"})
    
    
  