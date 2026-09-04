import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers
from algorithms.rate_constants import max_layers
import data_schema.sch_utilities as utils

def sch_options():
    return{
        "option_name": hx.Str(mode="input", default=None, optionality="optional", options_data="../../option_names_list", options_field="option_name", view={"label": "Option Name"}),
        "weight": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Weight %", "format": percent_format(2)}),
        "weight_excess": hx.Float(mode="output", view={"label": "Weight Excess", "format": thousands_format(0)}),
        "model_rol": hx.Float(mode="output", view={"label": "ROL", "format": percent_format(2)}),
    }

def sch_rating_summary(cds):

    cds.extend_node_rater_defined("cds/layers", {
        # Added variable to record a bpi where the risk is case priced. Do not remove as used in tpi summary. 
        "is_fun_top_up_coverage": hx.Bool(mode="input", default=False, view={"label": "Fundamental Top Up Coverage"}, async_input = ["generate_uw_doc"]),
        "bpi_case_priced": hx.Float(mode="input", default=None, optionality="optional", view={"label": "BPI (Case Priced)", "format": percent_format(1)}),
        "option_name": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Option name"}, async_input = ["generate_uw_doc"]),
        "limit_pct": hx.Float(mode="output", view={"label": "Limit %", "format": percent_format(2)}, async_input= ["generate_uw_doc"]),
        "excess_pct": hx.Float(mode="override", view={"label": "Excess %", "format": percent_format(2)}, async_input = ["generate_uw_doc"]),
        "indicated": hx.Bool(mode="input", default=True, view={"label": "Indicated"}, async_input= ["generate_uw_doc"]),
        "is_bound": hx.Bool(mode="input", default=False, view={"label": "Bound?"}),
        "model_rol": hx.Float(mode="output", view={"label": "Model ROL", "format": percent_format(2)}, async_input= ["generate_uw_doc"]),
        "warnings": hx.Str(mode="output", view={"label": "Warnings"}),
        "pflr_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "Priced-for Loss Ratio (Pre-UW Adj.)", "format": percent_format(1)}),
    })


    # Override values
    cds.override_node_properties("cds/layers",{
        "max_element_count": max_layers
        })
    
    cds.override_node_properties("cds/layers/status", {
       "options_table": "table_status", 
       "options_column": "Status",
        "view": {
            "options": {
                "input": {"label": "Status"},
        }},
        "async_input": ["generate_uw_doc"],
        })
    
    cds.override_node_properties("cds/layers/bpi_case_priced", {
        "default": 0, 
        "optionality": "required"
        })
    
    cds.override_node_properties("cds/layers/brokerage", {
        "mode": "output",
        "async_input": ["generate_uw_doc"]
        })   

    cds.override_node_properties("cds/layers/written_line", {
        "default": 1, 
        "optionality": "required", 
        "view": {
            "label": "Q/S",
            "options": {"read_only": {"read_only": True}}
            },
        "async_input": ["generate_uw_doc"]
        })

    cds.override_node_properties("cds/layers/section_reference", {
        "view": {
            "label": "Policy Reference",
            "options": {"read_only": {"read_only": True}}
            },
        "async_input": ["generate_uw_doc"]
        })

    cds.override_node_properties("cds/layers/quoted_premium", {
        "default": 0, 
        "optionality": "required",
        "view": {"options": {"read_only": {"read_only": True}}},
        "async_input": ["generate_uw_doc"]
        })
    
    cds.override_node_properties("cds/layers/is_primary_excess", {
        "async_input": ["generate_uw_doc"]
        })

    cds.override_node_properties("cds/layers/limit", {
        "async_input": ["generate_uw_doc"]
        })
    
    cds.override_node_properties("cds/layers/expected_loss_cost", {
        "async_input": ["generate_uw_doc"]
        })

    cds.override_node_properties("cds/layers/excess", {
        "mode": "override",
        "async_input": ["generate_uw_doc"]
        })

    cds.override_node_properties("cds/layers/premium", {
        "view": {"label": "Bound premium"},
        "async_input": ["generate_uw_doc"]
        })

    cds.override_node_properties("cds/layers/model_premium", {
        "view": {"label": "Model premium"},
        "async_input": ["generate_uw_doc"]
    })
    cds.override_node_properties("cds/layers/technical_premium", {
        "view": {"label": "Technical Premium"},
        "async_input": ["generate_uw_doc"]
    })
    cds.override_node_properties("cds/layers/benchmark_premium", {
        "view": {"label": "Benchmark premium"},
        "async_input": ["generate_uw_doc"]
    })
    cds.override_node_properties("cds/layers/tpi", {
        "view": {"label": "TPI%"},
        "async_input": ["generate_uw_doc"]
    })
    cds.override_node_properties("cds/layers/bpi", {
        "view": {"label": "BPI%"},
        "async_input": ["generate_uw_doc"]
    })
    
    cds.override_node_properties("cds/layers/pflr", {
    "async_input": ["generate_uw_doc"]
    })
    
    cds.override_node_properties("cds/layers/roc", {
    "async_input": ["generate_uw_doc"]
    })

    cds.override_node_properties("cds/layers/uw_adj_impact", {
    "async_input": ["generate_uw_doc"]
    })

    # Variables for blended quote calculations
    cds.extend_node_rater_defined("cds", {
            "blend_option": hx.Structure(children={
                "option_names_list": hx.List(view={"label": "List of Options Entered"},
                    mode="output", 
                    children={
                        "option_name": hx.Str(mode="output", view={"label": "Option Name"})
                        }),
                "instruction": hx.Str(mode="output", view={"label": "", "multiline": True}),
                "option_1": hx.Structure(view={"label": "Option 1"}, children={**sch_options()}),
                "option_2": hx.Structure(view={"label": "Option 2"}, children={**sch_options()}),
                "option_3": hx.Structure(view={"label": "Option 3"}, children={**sch_options()}),
                "option_name": hx.Str(mode="output", view={"label": "Option name"}),
                "limit": hx.Float(mode="output", view={"label": "Limit", "format": thousands_format(2)}),
                "limit_pct": hx.Float(mode="output", view={"label": "Limit %", "format": percent_format(2)}),
                "excess": hx.Float(mode="output", view={"label": "Dropdown Excess", "format": thousands_format(2)}),
                "excess_pct": hx.Float(mode="output", view={"label": "Initial Excess %", "format": percent_format(2)}),
                "indicated": hx.Bool(mode="output", view={"label": "Indicated"}),
                "date": hx.Date(mode="output", view={"label": "Date"}),
                "quota_share": hx.Bool(mode="output"),
                "is_bound": hx.Bool(mode="output", view={"label": "Bound?"}),
                "quoted_premium": hx.Float(mode="output", view={"label": "Bound Premium", "format": thousands_format(2)}),
        }),
    })
