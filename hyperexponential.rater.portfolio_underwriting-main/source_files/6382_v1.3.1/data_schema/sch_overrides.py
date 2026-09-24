import hx
from libraries.common_data_schema.data_schema.utilities import percent_format
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
          

def sch_overrides(cds):
    fields = {
        "cds/currencies/source_currency": {
            "view": {"label":"Currency"},
            "default": "USD",
            "async_input": [ "generate_word_document_task", "generate_excel_document_task"],
            "async_output":["fetch_bbt_task","start_renewal_task"] 
        },
        "cds/standard_fields/insured_name": {
            "mode": "input",
            "default": None,
            "allow_custom_value": True,
            "async_input": [ "generate_word_document_task", "generate_excel_document_task", "start_renewal_task"],
            "async_output":["fetch_bbt_task",{"task":"start_renewal_task", "reset":False}],
            "optionality": "optional",
            "options_column": "firm_name", 
            "options_table": "table_firm_name",            
            "view": {"label":"Insured Name"}           
        },
        "cds/standard_fields/broker": {
            "mode": "override",
            "view": {"label":"Broker Name"}           
        },
        "cds/standard_fields/inception_date": {         
            "async_input": [ "generate_word_document_task", "generate_excel_document_task", "calculate_profit_commission_task"]                      
        },
        "cds/standard_fields/expiry_date": {         
            "async_input": ["generate_word_document_task", "generate_excel_document_task"]                      
        },
        "hx_core/inception_date": {         
            "default": "2026-01-01",
            "async_output":["fetch_bbt_task","start_renewal_task"],
        },
        "hx_core/expiry_date": {         
            "default": "2026-12-31",
            "async_output":["fetch_bbt_task","start_renewal_task"],
        },
        "cds/standard_fields/policy_reference": {            
            "async_input": ["generate_word_document_task", "generate_excel_document_task"],
            "async_output":["start_renewal_task"],                      
        },
        "cds/standard_fields/benchmark_class": {            
            "mode": "output"                     
        },
        "cds/standard_fields/trifocus": {            
            "mode": "output"                      
        },
        "cds/standard_fields/underwriter": {
            "options_column": "underwriter", 
            "options_table": "table_input_underwriters",                
            "async_input": ["generate_word_document_task", "generate_excel_document_task"],
            "async_output":["start_renewal_task"],                      
        },       
        "cds/standard_fields/is_renewal": {           
            "view": {"label": "Renewal?"},
            "async_input": ["generate_word_document_task",  "generate_excel_document_task"],
            "async_output":["fetch_bbt_task",{"task":"start_renewal_task", "reset":False}]                       
        },
        "cds/layers/status": {           
            "mode": "output",
            "options_column": "deal_status", 
            "options_table": "table_input_deal_status"                  
        },
        "cds/layers/trifocus": {           
            "mode": "output"
        },
        "cds/standard_fields/facility_reference": { 
            "mode": "output"
        },
        "cds/layers/section_reference": { 
            "mode": "output"
        },
        "cds/layers/limit": { 
            "mode": "output"
        },
        "cds/layers/excess": { 
            "mode": "output"
        },
        "cds/layers/currency": { 
            "mode": "output"
        },
        "cds/standard_fields/uw_rationale": { 
            "mode": "output"
        },
        "cds/layers/brokerage": {           
            "mode": "output",
            "view": {"label": "Brokerage (excl. PC's)", "format": percent_format(2)}                   
        },
        "cds/layers/written_line": {           
            "mode": "output",
            "view": {"label": "Written Line", "format": percent_format(2)}                   
        },
        "cds/layers/quoted_premium": {       
            "view": {"label": "BST Share Gross EPI"},                 
            "mode": "output"                
        },
        "cds/layers/tpi": {       
            "view": {"label": "TPI", "format": percent_format(2)}             
        },
        "cds/layers/bpi": {       
            "view": {"label": "BPI", "format": percent_format(2)}             
        },
        "cds/layers/bpi_pre_uw_adj": {       
            "view": {"label": "BPI (Pre-UW Adjustment)", "format": percent_format(2)}             
        },
        "cds/layers/tpi_pre_uw_adj": {       
            "view": {"label": "TPI (Pre-UW Adjustment)", "format": percent_format(2)}             
        },
        "cds/layers/uw_adj_impact": {       
            "view": {"label": "Impact of Underwriting Adjustments", "format": percent_format(2)}             
        },
        "cds/layers/pflr": {       
            "view": {"label": "Priced-for Loss Ratio", "format": percent_format(2)}             
        }
    }
    for field, props in fields.items():
        cds.override_node_properties(field, props)