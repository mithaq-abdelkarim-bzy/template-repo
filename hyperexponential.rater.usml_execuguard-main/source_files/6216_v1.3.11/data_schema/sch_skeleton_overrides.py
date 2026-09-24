import hx
from libraries.common_data_schema.data_schema.utilities import percent_format

def sch_skeleton_overrides(cds):
    fields = {        
        "cds/standard_fields/insured_country": {
            'mode':'output'            
        },
        "cds/standard_fields/insured_state_or_province": {
            'mode':'output'            
        },
        "cds/standard_fields/insured_name": {            
            "async_input": ["start_renewal_task", "word_documents_task", "rationale_word_documents_task"],
            "options_table": "insured_names",
            "options_column": "insured_name",
            "allow_custom_value": True,            
        },
        "cds/standard_fields/is_renewal": {
            "async_output": [{"task":"start_renewal_task", "reset": False}]            
        },
        "cds/layers/brokerage": {
            "default": 0,
            "optionality": "required",
            "validation": {"min_value": 0, "max_value": 1},
            "async_input": ["rarc_task", "word_documents_task"],
            "view": {"label": "External Brokerage", "format": percent_format(2), 
            "options" : {"read_only": {"read_only": True}}}
        },    
        "cds/standard_fields/underwriter": {            
            "async_input": ["word_documents_task", "rationale_word_documents_task"],
            "options_table": "table_input_underwriters", 
            "options_column": "Underwriters",
            "allow_custom_value": True                      
        },
        "hx_core/inception_date": {            
            "async_input": [ "word_documents_task", "rationale_word_documents_task"]                      
        },
        "hx_core/expiry_date": {            
            "async_input": [ "word_documents_task", "rationale_word_documents_task"]                      
        },
        "cds/layers/status": {            
            "async_input": [ "word_documents_task"],
            "view": {
                "options": {
                    "input": {"label": "Status"},
                    "read_only": {
                        "label": "Deal Status by Renewal Layers",
                        "read_only": True,
                    },
                }
            }                      
        },
        "cds/layers/section_reference": {            
            "async_input": [ "word_documents_task"]  ,
            "view": {
                "options": {
                    "read_only": {
                        "read_only": True,
                    },
                }
            }                     
        },
        "cds/layers/written_line": {
            "mode": "input",           
            "async_input": [ "word_documents_task"] ,
            "view": {
                "options": {
                    "read_only": {
                        "read_only": True,
                    },
                }
            }                        
        },
        "cds/layers/quoted_premium": {            
            "async_input": ["rarc_task", "word_documents_task"],
            "default": 0, "mode": "output",                      
        },
        "cds/layers/technical_premium": {            
            "async_input": [ "word_documents_task"]                      
        },
        "cds/layers/technical_premium_pre_uw_adj": {            
            "async_input": [ "word_documents_task"]                      
        },
        "cds/layers/benchmark_premium": {            
            "async_input": ["rarc_task", "word_documents_task"],
            "default": 0, "mode": "output"                     
        },
        "cds/layers/tpi": {            
            "async_input": [ "word_documents_task"],
            "view": {"format": percent_format(2)}
        },
        "cds/layers/tpi_pre_uw_adj": {            
            "async_input": [ "word_documents_task"]                      
        },
        "cds/layers/bpi": {            
            "async_input": [ "word_documents_task"],
            "view": {"format": percent_format(2)}
        },
        "cds/layers/pflr": {            
            "async_input": [ "word_documents_task"]                      
        },
        "cds/layers/roc": {            
            "async_input": [ "word_documents_task"]                      
        },
        "cds/layers/uw_adj_impact": {            
            "async_input": [ "word_documents_task"]                      
        },
        "cds/standard_fields/uw_rationale": {            
            "async_input": [ "rationale_word_documents_task", "word_documents_task"]                      
        },
        "cds/standard_fields/is_rater_priced": {            
            "async_input": [ "word_documents_task"]                      
        },

    }
    for field, props in fields.items():
        cds.override_node_properties(field, props)