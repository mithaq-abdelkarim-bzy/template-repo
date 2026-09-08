import hx_data_schema as hx
import data_schema.utilities as utils

def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {
        # Risk information 
        "database_id": hx.Int(mode="output", view={"label": "Database ID", "format": utils.integer_format(0)}),
        "application_date": hx.Date(mode="input", default="2000-01-01", view={"label": "Application Date"}),
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),
        "is_surplus": hx.Bool(mode="output"),
    
        # Rationale
        "general_comments": hx.Str(mode="input", default="", view={"label": "Knowledge Of Insured"}),

        # Premium metrics
        "term_adjustment_underlying": hx.Float(mode="output", view={"label":"Term Adjustment for the Underlying Layer"}),
        "term_adjustment": hx.Float(mode="output", view={"label":"Term Adjustment"}),

        "modifiers_dollar_value": hx.Float(mode="output", view={"label": "Schedule Rating Impact", "format":utils.thousands_format(0)}),
    })

    cds.extend_node_rater_defined("cds/layers", {
        # Risk information 
        "is_bound": hx.Bool(mode="output"),
        
        # Premium metrics
        "deviation_from_unity": hx.Float(mode="output", view={"label": "Deviation from Unity", "format": utils.integer_format(3)}),
        "net_benchmark_premium": hx.Float(mode="output", view={"label": "Net Benchmark Premium", "format":utils.thousands_format(0)}),
        "net_technical_premium": hx.Float(mode="output", view={"label": "Net Technical Premium", "format":utils.thousands_format(0)}),
    })
    
    cds.override_node_properties("cds/layers/quoted_premium", {
        "mode": "output"
    })
    
    cds.extend_node_rater_defined("cds/layers/rate_change", {
        "expiring_policy_reference": hx.Str(mode="input", default="", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Policy Reference Number"}),
    })

    cds.override_node_properties("cds/standard_fields/policy_reference", {
        "view": {"label": "Policy Reference Number (to be filled when bound)"}
        }
    )
    
    cds.override_node_properties("cds/layers/is_primary_excess", {
        "mode": "output", 
        "view": {"label": "Primary / Excess"}
    })

    cds.override_node_properties("cds/layers/brokerage", {
        "default": 0.15,
        "view": {"label": "Brokerage / Commission", "format": utils.percent_format(1)}
    })

    cds.override_node_properties("cds/standard_fields/underwriter", {
        "default": None,
        "options_table": "underwriter_list",
        "options_column": "UnderwriterName",
        "allow_custom_value": True
    })

    cds.override_node_properties("cds/layers/status", {
        "default": "Submission",
        "options": ["Submission", "Quote", "Bound", "Not Taken Up"],
        "view": {"label": "Deal Status"},
        "async_output": ["expiring_policy_fetch_task", "start_renewal_task"],
        # "optionality": "required"  # Commented to make optional. Reason of this is described in the comments for: https://beazley.atlassian.net/browse/RRG-12669
    })

    cds.override_node_properties("cds/standard_fields/is_admitted_or_surplus", {
        "default": "Admitted",
        "options": ["Admitted", "Admitted - LRE", "Surplus"],
        "view": {"label": "Admitted / Surplus"},
        "optionality": "required"
    })

    cds.override_node_properties("cds/standard_fields/is_renewal", {
        "view": {"label": "Renewal?"},
        "async_output": ["start_renewal_task"]
    })