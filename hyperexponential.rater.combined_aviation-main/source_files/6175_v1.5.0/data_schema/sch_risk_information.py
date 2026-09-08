import hx_data_schema as hx
from data_schema.sch_utilities import *
from algorithms.data_schema.sch_rater_defined import coverages_dict
import algorithms.rate_constants as c

def sch_risk_information(cds):
    common_tasks = ["fetch_by_operator_task", "fetch_by_registration_task", "get_selected_regs_task", "fill_with_defaults_task"]

    cds.extend_node_rater_defined("cds", { 
        # If needed
        "database_id": hx.Int(mode="output", view={"label": "Database ID", "format": integer_format(0)}),
        "rater": hx.Str(mode="input", default=None, optionality="optional", async_input=common_tasks, async_output=[{"task": "start_renewal_task", "reset": False}], options=["Airlines", "General Aviation"], view={"label": "Airlines or General Aviation?"}),
        "is_airlines": hx.Bool(mode="output", async_input=common_tasks),
        "is_ga": hx.Bool(mode="output", async_input=[*common_tasks, "rarc_task", "start_renewal_task"]),
        "is_neither": hx.Bool(mode="output", async_input=common_tasks),
        
        # Additional policy info
        "policy_info": hx.Structure(children={
            "term_calculated": hx.Float(mode="output", view={"label": "Term", "format": {**thousands_format(5), "trimMantissa": True}}),
            "term": hx.Float(mode="input", default=1, async_input=["rarc_task"], async_output=["show_airlines_task", "show_ga_task",{"task": "start_renewal_task", "reset": False}], view={"label": "Term", "format": {**thousands_format(5), "trimMantissa": True}, "options": {"read_only": {"read_only": True}}}),
            "is_term_valid": hx.Bool(mode="output"),
            "is_term_invalid": hx.Bool(mode="output"),
            "inception_date_temp": hx.Date(mode="output", async_output=["show_airlines_task", "show_ga_task", "start_renewal_task"]),
            "application_date": hx.Date(mode="input", default=None, optionality="optional", async_output=["start_renewal_task", {"task": "show_airlines_task", "reset": False}, {"task": "show_ga_task", "reset": False}], view={"label": "Application Date"}),
            "broker_contact": hx.Str(mode="input", default="", async_output=[{"task": "start_renewal_task", "reset": False}], view={"label": "Broker Contact"}),
            "direct_ri": hx.Str(mode="input", default="Direct", async_output=[{"task": "start_renewal_task", "reset": False}], options=["Direct", "Reinsurance"], view={"label": "Direct or RI?"}),
            "has_profit_commission": hx.Bool(mode="input", default=False, async_output=[{"task": "start_renewal_task", "reset": False}], view={"label": "PC?"}),
            "pc_to_gross": hx.Str(mode="input", default="Gross", async_output=[{"task": "start_renewal_task", "reset": False}], options=["Gross", "Net"] , view={"label": "Applies to G/N premium", "info": "Net = Net of commission\nGross = Gross premium"}),
            "profit_commission": hx.Float(mode="input", default=0, async_output=[{"task": "start_renewal_task", "reset": False}], validation={"min_value": 0, "max_value": 1}, view={"label": "% PC", "format": percent_format(1)}),
            "pc_expenses": hx.Float(mode="input", default=0, async_output=[{"task": "start_renewal_task", "reset": False}], validation={"min_value": 0, "max_value": 1}, view={"label": "PC Expenses", "format": percent_format(1)}),
            "pc_deficit": hx.Float(mode="input", default=0, async_output=[{"task": "start_renewal_task", "reset": False}], validation={"min_value": 0}, view={"label": "PC Deficit", "format": thousands_format()}),
            "has_no_claims_bonus": hx.Bool(mode="input", async_output=[{"task": "start_renewal_task", "reset": False}], default=False,  view={"label": "NCB?"}),
            "ncb_pct": hx.Float(mode="input", default=0, async_output=[{"task": "start_renewal_task", "reset": False}], validation={"min_value": 0, "max_value": 1}, view={"label": "% Bonus", "format": percent_format(1)}),
            "ncb_to_gross": hx.Str(mode="input", default="Gross", async_output=[{"task": "start_renewal_task", "reset": False}], options=["Gross", "Net"], view={"label": "Applies to G/N premium", "info": "Net = Net of commission\nGross = Gross premium"}),
        })

    })

    # Update underwriters variable to link to dropdown
    cds.override_node_properties("cds/standard_fields/underwriter", {"async_output": [{"task": "start_renewal_task", "reset": False}], "options_table": "table_input_underwriters", "options_column": "underwriter"})

    # Override properties
    cds.override_node_properties("cds/standard_fields/inception_date", {"async_input": ["fetch_by_operator_task", "fetch_by_registration_task", "get_selected_regs_task"]})
    cds.override_node_properties("cds/standard_fields/expiry_date", {"async_input": ["fetch_by_operator_task", "fetch_by_registration_task", "get_selected_regs_task"]})
    cds.override_node_properties("cds/standard_fields/insured_name", {"async_output": [{"task": "start_renewal_task", "reset": False}]})
    cds.override_node_properties("cds/standard_fields/broker", {"async_output": [{"task": "start_renewal_task", "reset": False}]})
    cds.override_node_properties("cds/standard_fields/is_renewal", {"async_output": [{"task": "start_renewal_task", "reset": False}]})
    cds.override_node_properties("cds/standard_fields/rating_methodology", {"async_output": [{"task": "start_renewal_task", "reset": False}]})
    cds.override_node_properties("cds/standard_fields/policy_reference", {"mode": "output"})

    cds.override_node_properties("cds/currencies/source_currency", {"default": "USD", "options": c.ccy_options, "async_output": [{"task": "start_renewal_task", "reset": False},{"task": "show_airlines_task", "reset": False},{"task": "show_ga_task", "reset": False}]})
    cds.override_node_properties("cds/currencies/multi_currency_support", {"async_output": [{"task": "start_renewal_task", "reset": False}]})
    cds.override_node_properties("cds/layers/brokerage", {
        "optionality": "required", "default": 0, "view": {"format": percent_format(1)}, "validation": {"min_value": 0, "max_value": 1}, "async_input": ["rarc_task"], "async_output": [{"task": "start_renewal_task", "reset": False}]
    })
    cds.override_node_properties("cds/layers/status", { "async_output": [{"task": "start_renewal_task", "reset": False}]})
    
    for cvg in coverages_dict.keys():
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/section_reference", {
           "async_output": [{"task": "start_renewal_task", "reset": False}],"async_input": ["rarc_task", "show_airlines_task", "show_ga_task","start_renewal_task"]
        })
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/brokerage", {
            "optionality": "required", "default": 0, "view": {"format": percent_format(1)}, "validation": {"min_value": 0, "max_value": 1}, "async_input": ["rarc_task"], "async_output": [{"task": "start_renewal_task", "reset": False}]
        })
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/written_line", {
            "optionality": "required", "default": 0, "view": {"format": percent_format(1)}, "validation": {"min_value": 0, "max_value": 1}, "async_input": ["rarc_task"], "async_output": [{"task": "start_renewal_task", "reset": False}]
        })
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/quoted_premium", {
            "optionality": "required", "default": 0, "validation": {"min_value": 0}, "async_input": ["rarc_task", "fill_historic_premium_task"], "async_output": [{"task": "start_renewal_task", "reset": False}]
        })
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/limit", {
            "default": 0, "optionality": "required", "validation": {"min_value": 0}, "async_input": ["rarc_task", "fetch_by_operator_task", "fetch_by_registration_task", "get_selected_regs_task","show_airlines_task", "show_ga_task"], "async_output": [{"task": "start_renewal_task", "reset": False}]
        })
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/excess", {
            "default": 0, "optionality": "required", "validation": {"min_value": 0}, "async_input": ["rarc_task", "fetch_by_operator_task", "fetch_by_registration_task", "get_selected_regs_task","show_airlines_task", "show_ga_task"], "async_output": [{"task": "start_renewal_task", "reset": False}]
        })
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/currency", {
            "mode": "override", "options": c.ccy_options, "async_input": ["fetch_by_operator_task", "fetch_by_registration_task", "get_selected_regs_task","show_airlines_task", "show_ga_task","start_renewal_task"]
        })
    
    # Make BM class output
    cds.override_node_properties(
        "cds/standard_fields/benchmark_class", {"mode": "output"}
    )



    