import hx_data_schema as hx
from data_schema.sch_z_utilities import thousands_format
from data_schema.sch_z_utilities import percent_format
from data_schema.sch_z_utilities import integer_format

def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {
        # Section Risk Information
        "risk_info": hx.Structure(children={
            "database_id": hx.Str(mode="output", view={"label": "Policy Option ID"}),
            "submission_date": hx.Date(mode="override", view={"label": "Submission Date"}),
            "policy_duration": hx.Float(mode = "override", view={"label" : "Policy Duration (In Years)", "format" : {"thousandSeparated": False, "mantissa": 4}}),
            "policy_reference_exp": hx.Str(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Policy Ref"}),
            "new_replacement": hx.Str(mode="input",async_output = ["start_renewal_task"], default = None, optionality="optional", view={"options": { "invalid": {"style_cell": "hx-neutral"}}, "label": "Insured Name Manual"}),
            "insured_name_final": hx.Str(mode = "output", view = {"label" : "Selected Insured Name"}),
            "risk_class_generated": hx.Str(mode="output", view={"label": "Class Flag Generated"}),
            "srcc_coverage_given_indicator": hx.Str(mode="input", default="Yes", options_table = "table_lookup_global_yes_no_response", options_column="response", view={"label": "Is Strikes, Riots and Civil Commotion Coverage Given?"}),
            "srcc_fully_excluded_indicator": hx.Str(mode="input", default="No", options_table = "table_lookup_global_yes_no_response", options_column="response", view={"label": "Is it fully excluded?"}),
            "srcc_sublimit_indicator": hx.Str(mode="input", default="No", options_table = "table_lookup_global_yes_no_response", options_column="response", view={"label": "Is there a sub-limit?"}),
            "srcc_sublimit": hx.Float(mode="override", view={"label": "Please override sub-limit if different to total line size", "format" : thousands_format()}),
            "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),
            "expiring_policy_option_id": hx.Int(mode="override", async_input=["expiring_policy_fetch_task","start_renewal_task"], view={"label": "Expiring Policy Option ID", "format": thousands_format()}),

            # SA: The way these are structured in the mapping sheet doesn't work so I've adjusted them
            "type_dropdown": hx.List(mode="output", children={
                "type": hx.Str(mode="output", view={"label": "Type"})
            }),
            "risk_class_dropdown": hx.List(mode="output", children={
                "risk_class": hx.Str(mode="output", view={"label": "Class"})
            }),
        }),
        
        "fa_masking": hx.Bool(mode="output"),
        "jb_masking": hx.Bool(mode="output"),
        "gs_masking": hx.Bool(mode="output"),
        "cit_masking": hx.Bool(mode="output"),
        "insured_name_selected": hx.Bool(mode="output"),
        "insured_name_not_selected": hx.Bool(mode="output"),
        "risk_class_selected": hx.Bool(mode="output"),
        "risk_class_not_selected": hx.Bool(mode="output"),
        "underwriter_selected": hx.Bool(mode="output"),
        "underwriter_not_selected": hx.Bool(mode="output"),
        "policy_reference_filled": hx.Bool(mode="output"),
        "policy_reference_not_filled": hx.Bool(mode="output"),
    })

    cds.extend_node_rater_defined("cds/layers", {
        "pflr_pre_uw_adj": hx.Float(mode='output', optionality='optional', view={'label': 'Priced-for Loss Ratio (Pre-UW Adj.)', 'format': {'output': 'percent', 'mantissa': 1}}),
    })

    cds.override_node_properties("cds/standard_fields/policy_reference", {
        "default": "", 
        "optionality": "required",
        "async_input": ["fetch_bi_data_task", "bi_intelligence_fetch_task"],
        "async_output": ["start_renewal_task"],
        "view": {
            "options": {
                "invalid": {"style_cell": "hx-neutral"},
                "read_only": {"label": "Section Reference", "read_only": True},
                "kpi_summary_option": {
                    "label": "Section Reference",
                }
            }
        },
    })

    cds.override_node_properties("cds/standard_fields/is_renewal", {
        "default": False, 
        "optionality": "required",
        "async_output": ["start_renewal_task"]
    })

    cds.override_node_properties("cds/standard_fields/benchmark_class", {
        "default": None, 
        "options_data": "../../risk_info/risk_class_dropdown", 
        "options_field": "risk_class", 
        "optionality":"optional", 
        "view": {
            "options": { "invalid": {"style_cell": "hx-neutral"}},
            "label": "Class"},
    })

    # SA: Shouldn't the insured names field in standard fields be the one that Selected Insured Name, rather 
    # than the dropdown? This would mean the selected value is the one that's passed to this field for reporting
    # purposes, otherwise it'll sometimes be blank
    cds.override_node_properties("cds/standard_fields/insured_name", {
        "options_table": "table_lookup_global_firm_name", 
        "options_column": "firm_name", 
        "default": None, 
        "optionality": "optional", 
        "view": {"options": { "invalid": {"style_cell": "hx-neutral"}},
                "label": "Insured Name Search"}
    })

    cds.override_node_properties("cds/standard_fields/underwriter", {
        "async_input": ["start_renewal_task"], 
        "options_table": "table_lookup_global_underwriters", 
        "options_column": "underwriters", 
        "default": None, 
        "optionality": "optional", 
        "view": {
            "options": { "invalid": {"style_cell": "hx-neutral"}},
            "label": "Underwriter"}
    })

    cds.override_node_properties("cds/layers/status", {
        "default": "Submission",  # SA: Better to set default_index when referring to a table
        "async_output": ["start_renewal_task"], 
        "optionality": "optional",  # SA: Why make this optional when the default is not None?
        "options_table": "table_lookup_global_deal_status", 
        "options_column": "deal_status", 
        "view": {
            "options": {
                "invalid": {"style_cell": "hx-neutral"}, 
                "read_only": {"label": "Status", "read_only": True},
                "kpi_summary_option": {
                    "label": "Status",
                }
            }, 
            "label": "Deal Status"
            }
        }
    )
    
    cds.override_node_properties(
        "cds/layers/brokerage", {
            "mode": "output",
            "view": {
                "options": {
                    # "read_only": {"label": "Brokerage (excl. PC's)", "read_only": True}, 
                    "kpi_summary_option": {
                        "label": "Brokerage (excl. PC's)",
                    }
                }
            }
        }
    )
