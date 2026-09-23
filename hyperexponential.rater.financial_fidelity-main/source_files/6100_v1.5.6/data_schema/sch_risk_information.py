import hx_data_schema as hx
import libraries.common_data_schema.data_schema.utilities as utils

def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {
        # Risk information 
        "database_id": hx.Int(mode="output", view={"label": "Database ID", "format": utils.integer_format(0)}),
        "application_date": hx.Date(mode="input", default="2000-01-01", view={"label": "Application Date"}),
        "general_comments": hx.Str(mode="input", default="", view={"label": "Knowledge Of Insured"}),
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),
    })
        
    cds.extend_node_rater_defined("cds/layers", {
        # Risk information 
        "broker": hx.Str(mode="input", default="", view={"label": "Broker Name"}),
        "is_bound": hx.Bool(mode="output"),
        "quota_share_flag": hx.Bool(mode="input", default=False, view={"label": "Quota Share?"}),
        "is_follow": hx.Bool(mode="input", default=False, view={"label": "Is Beazley following the lead insurer's premium?"}),
        "lead_insurer": hx.Str(mode="input", default="", view={"label": "Lead Insurer"}),
        "participating_insurer": hx.Str(mode="input", default="", view={"label": "Participating Insurer"}),

        # Premium metrics
        "lead_limit": hx.Float(mode="input", default=0, view={"label": "Leader's Limit", "format":utils.thousands_format(0)}),
        "lead_premium": hx.Float(mode="input", default=0, view={"label": "Leader's Premium", "format":utils.thousands_format(0)}),
        "beazley_share": hx.Float(mode="input", default=1, view={"label": "Beazley's Share", "format": utils.percent_format(0)}),
        "manual_premium": hx.Float(mode="output", view={"label": "Total Manual Premium", "format":utils.thousands_format(0)}),
        "company_premium": hx.Float(mode="output", view={"label": "Total Premium (pre experience rating)", "format":utils.thousands_format(0)}),
        "final_premium": hx.Float(mode="output", view={"label": "Final Premium (Beazley's Share)", "format":utils.thousands_format(0)}),
        "final_premium_annual": hx.Float(mode="output", view={"label": "Final Annualized Premium (Beazley's Share)", "format":utils.thousands_format(0)}),
        "net_benchmark_premium": hx.Float(mode="output", view={"label": "Net Benchmark Premium", "format":utils.thousands_format(0)}),
        "modifiers_dollar_value": hx.Float(mode="output", view={"label": "Schedule Rating Impact", "format":utils.thousands_format(0)}),
        "bound_deviation_from_unity": hx.Float(mode="output", view={"label": "Deviation from Unity", "format": utils.integer_format(3)})
    })
        
    cds.extend_node_rater_defined("cds/layers/rate_change", {
        # Risk information   
        "expiring_policy_reference": hx.Str(mode="input", default="", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Policy Reference Number"}),
    })

    cds.override_node_properties("cds/layers/status", {
        "default": "Submission",
        "options": ["Submission", "Quote", "Bound", "Not Taken Up"],
        "view": {
            "options": {
                "read_only": {"label": "Status", "read_only": True},
                "rating_summary_option": {
                    "label": "Status"
                }
            }, 
            "label": "Deal Status"
        },
        "async_output": ["expiring_policy_fetch_task", "start_renewal_task"],
        # "optionality": "required"  # Commented to make optional. Reason of this is described in the comments for: https://beazley.atlassian.net/browse/RRG-12669
    })
    
    cds.override_node_properties("cds/layers/quoted_premium", {
        "mode": "output"
    })

    cds.override_node_properties(
        "cds/standard_fields/policy_reference", {
            "view": {
                "label": "Policy Reference Number (to be filled when bound)",
                "options": {
                    "read_only": {"read_only": True, "label": "Section Reference"},
                    "rating_summary_option": {
                        "label": "Section Reference"
                    }
                }
            }
        }
    )

    cds.override_node_properties(
        "cds/layers/is_primary_excess", {
            "mode": "output", 
            "view": {"label": "Primary or Excess"}
        }
    )

    cds.override_node_properties(
        "cds/standard_fields/is_renewal", {
            "view": {"label": "Renewal?"},
            "async_output": ["start_renewal_task"]
        }
    )

    cds.override_node_properties(
        "cds/layers/brokerage", {
            "default": 0.15, 
            "view": {
                "label": "Brokerage / Commission", 
                "format": utils.percent_format(1),
                "options": {
                    "read_only": {"label": "Brokerage (excl. PC's)", "read_only": True},
                    "rating_summary_option": {
                        "label": "Brokerage"
                    }
                }
            }
        }
    )

    cds.override_node_properties('cds/layers/section_reference', {
        "view": {"options": {"read_only": {"read_only": True, }}},
    })

    cds.override_node_properties('cds/layers/written_line', {
        "default": 1, 
        "view": {"options": {"read_only": {"read_only": True}}},
    })

    cds.override_node_properties('cds/layers/bpi_case_priced', {
        "view": {"label":"BPI","options": {"read_only": {"read_only": True}}},
    })

    cds.override_node_properties('cds/layers/quoted_premium_case_priced', {
        "view": {"options": {"read_only": {"read_only": True, }}},
    })
    