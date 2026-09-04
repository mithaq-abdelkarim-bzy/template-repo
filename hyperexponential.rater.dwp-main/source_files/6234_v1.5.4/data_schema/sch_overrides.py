import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
import data_schema.sch_utilities as utils

def sch_overrides(cds):
    
    # Override Risk information tab 
    cds.override_node_properties("cds/standard_fields/underwriter", {
        "options_table": "lst_underwriters", 
        "options_column": "Underwriters",
        "allow_custom_value": True
    })
    cds.override_node_properties("cds/standard_fields/insured_name", {
        "options_table": "lst_insured_names", 
        "options_column": "insured_name", 
        "allow_custom_value": True, 
        "async_input": ["start_renewal_task"]
    })
    cds.override_node_properties("cds/currencies/source_currency", {"default": "USD", "optionality": "required"})
    cds.override_node_properties("cds/standard_fields/benchmark_class", {"mode": "output"})
    cds.override_node_properties("cds/standard_fields/uw_rationale", {"mode": "output"})
    cds.override_node_properties("cds/standard_fields/is_renewal", {"async_output": [{"task":"start_renewal_task", "reset":False}]})
    
    # Override layers
    cds.override_node_properties("cds/layers", {
        "min_element_count": 6,
        "max_element_count": 6, 
        "default_element_count": 6,
        "async_input": ["rarc_task"],
    })
    cds.override_node_properties("cds/layers/aggregate_limit", {
        "async_input": ["rarc_task"],
        "options_data": "../agg_limits_list", 
        "options_field": "values",
        "view": {"label": "Agg Limit"},
        "default": 1e6
    })
    cds.override_node_properties("cds/layers/status", {
        "default": "Rating",
        "view": {
            "options": {
                "input": {"label": "Status"},
                "read_only": {"label": "Deal Status by Renewal Layers", "read_only": True}
            }
        }
    })


    # Add validations
    cds.override_node_properties("cds/layers/limit", {"async_input": ["rarc_task"], "validation": {"min_value": 0}, "default": 1e6})
    cds.override_node_properties("cds/layers/deductible", {"default": 10e3, "async_input": ["rarc_task"], "validation": {"min_value": 0}})
    cds.override_node_properties("cds/layers/excess", {"async_input": ["rarc_task"], "validation": {"min_value": 0}})  
    cds.override_node_properties("cds/layers/written_line", {"default": 1, "validation": {"min_value": 0, "max_value": 1}})
        
    
    # Update labels for Rating Summary
    cds.override_node_properties("cds/layers/benchmark_premium", {"async_input": ["rarc_task"], "view": {"label": "Benchmark Premium After UW Adj"}})
    cds.override_node_properties("cds/layers/benchmark_premium_pre_uw_adj", {"view": {"label": "Benchmark Premium Before UW Adj"}})    
    cds.override_node_properties("cds/layers/technical_premium", {"view": {"label": "Technical Premium After UW Adj"}})    
    cds.override_node_properties("cds/layers/technical_premium_pre_uw_adj", {"view": {"label": "Technical Premium Before UW Adj"}})    
    cds.override_node_properties("cds/layers/expected_loss_cost", {"view": {"label": "Final Expected Loss"}})
    cds.override_node_properties("cds/layers/quoted_premium", {"async_input": ["rarc_task"] ,"view": {"options":{
        "input": {"label": "EPI 100% Line Size"},
        "read_only": {"label": "EPI", "read_only": True}
    }}})
    cds.override_node_properties("cds/layers/brokerage", {"default": 0.2, "optionality": "required", "validation": {"min_value": 0, "max_value": 1}, "async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/bpi_case_priced", {"default": 0, "optionality": "required"})

   
    # Override async tasks
    cds.override_node_properties("cds/standard_fields/policy_reference", {"async_input": ["sql_bi_fetch_task"]})
   

