import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

def sch_rate_change(cds):

    rarc_changes = [
        "exposure_change",
        "risk_characteristics_change",
        "limit_change",
        "deductible_change",
        "terms_conditions_change",
        "other_change",
        "brokerage_change"
    ]

    # Add rate change task as an async output of cds nodes
    for change in rarc_changes:
        cds.override_node_properties(f"cds/layers/rate_change/{change}/model_calculated",   {"async_output": ["rarc_task"]} )
        cds.override_node_properties(f"cds/layers/rate_change/{change}/uw_selected",        {"async_output": ["rarc_task","start_renewal_task"]} )  # added this to clear out the inputs on start of renewal.
        cds.override_node_properties(f"cds/layers/rate_change/{change}/comments",           {"async_output": ["start_renewal_task"]} )              # added this to clear out the inputs on start of renewal.    

    
    cds.extend_node_rater_defined("cds", {
        "rate_change": hx.Structure(children={
            "expiring_policy_option_id": hx.Int(mode="override", async_input=["expiring_policy_fetch_task", "rarc_task", "case_priced_expiry_import"], view={"label": "Expiring Policy Option", "format": {"thousandSeparated": False}}),
            "has_fetch_not_run": hx.Bool(mode="input", default=True, async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "has_fetch_run": hx.Bool(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "has_rarc_not_run": hx.Bool(mode="input", default=True, async_output=["rarc_task"]),
            "has_rarc_run": hx.Bool(mode="output", async_output=["rarc_task"]),
            "rarc_run_again_message": hx.Str(mode="output"),
            "rarc_message_show": hx.Bool(mode="output"),
            "layer_mapping": hx.Str(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"])
        })
    })

    cds.extend_node_rater_defined("cds/layers/rate_change", {
        "rebased_expiring_premium": hx.Float(mode="output", async_output=["rarc_task"], view={"label": "Rebased Expiring Premium", "format": thousands_format()}),
        **{
            item: hx.Structure(view={"label": label}, children={
            "renewal": hx.Float(mode="output", view={"label": "Renewal", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "expiring": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task", "case_priced_expiry_import"], view={"label": "Expiring", "format": {"thousandSeparated": True, "mantissa": 0}}),
            })
            for item, label in zip(
                ["premium_policy_term_beazley_share",  "premium_policy_term_100pct", "premium_annualized_beazley_share", "premium_annualized_100pct"], 
                ["Premium - Policy Term (Beazley Share)", "Premium - Policy Term (100% Share)","Annualised Premium (Beazley Share)", " Annualised Premium (100% Share)"]
            )
        },
        "expiring_policy_info": hx.Structure(children={
            "expiring_exposure": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_policy_length": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_premium": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_limit": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_deductible": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_brokerage": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_written_line": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_expected_loss": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_bpi": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task", "case_priced_expiry_import"]),
        }),         
        "simple_rate_change": hx.Float(mode="output", view={"label": "Pure Premium Change / Simple Rate Change", "format": percent_format()}),
        "risk_adjusted_rate_change": hx.Structure(view={"label": "Underwriter Selected"}, children={
            "technical": hx.Float(mode="output", view={"label": "Model Risk Adjusted Rate Change", "format": percent_format()}),
            "technical_net_brokerage": hx.Float(mode="output", view={"format": percent_format()}),
            "uw_selected": hx.Float(mode="output", view={"label": "UW Selected Risk Adjusted Rate Change", "format": percent_format()}),
            "uw_selected_net_brokerage": hx.Float(mode="output", view={"label": "UW Selected Risk Adjusted Rate Change","format": percent_format()}),
        }),
        "risk_adjusted_rate_change_case_priced": hx.Structure(view={"label": "Underwriter Selected"}, children={
            "uw_selected": hx.Float(mode="override", view={"label": "UW Selected Risk Adjusted Rate Change", "format": percent_format()}),
            "uw_selected_net_brokerage": hx.Float(mode="output", view={"label": "UW Selected Risk Adjusted Rate Change Net Brokerage","format": percent_format()}),
            "comments": hx.Str(mode="input", default="", view={"label": "Comment"}),
        }),
        "error_message": hx.Str(mode="output"),
        "temp_storage": hx.Structure(children={ # To store premiums when running the RARC calculation
            "quoted_premium": hx.Float(mode="output", async_output=["rarc_task"]),
            "benchmark_premium": hx.Float(mode="output", async_output=["rarc_task"]),
        })
    })