import hx_data_schema as hx
import data_schema.sch_utilities as utils
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers


def renewal_expiring(): return {
    "expiring": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Expiring", "format": thousands_format()}),
    "rebased_expiring": hx.Float(mode="output", view={"label": "Rebased\nExpiring", "format": thousands_format()}),
    "renewal": hx.Float(mode="output", view={"label": "Renewal", "format": thousands_format()}),
}

def sch_rate_change(cds):
    rarc_changes = [
        "exposure_change",
        "risk_characteristics_change",
        "limit_change",
        "deductible_change",
        "terms_conditions_change",
        "other_change"
    ]

    for change in rarc_changes:
        cds.override_node_properties(
            f"cds/layers/rate_change/{change}/model_calculated", {"async_output": ["rarc_task"]} 
        )
    
    cds.extend_node_rater_defined("cds", {
        "rate_change": hx.Structure(children={
            **{f"show_layer_{index}": hx.Bool(mode="output") for index in range(1,max_layers+1)},
            "expiring_policy_option_id": hx.Int(mode="override", async_input=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Expiring Policy Option", "format": {"thousandSeparated": False}}),
            "has_fetch_not_run": hx.Bool(mode="input", default=True, async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "has_fetch_run": hx.Bool(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "has_rarc_not_run": hx.Bool(mode="input", default=True, async_output=["rarc_task"]),
            "has_rarc_run": hx.Bool(mode="output", async_output=["rarc_task"]),
            "rarc_run_again_message": hx.Str(mode="output"),
            "rarc_message_show": hx.Bool(mode="output"),
            "layer_mapping": hx.Str(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"])
        })
    })

    cds.override_node_properties(
        "cds/layers/rate_change/expiring_layer", 
        {  
            "async_input": ["expiring_policy_fetch_task", "rarc_task"],
            "options": [*range(1,max_layers+1)]
        } 
    )

    cds.extend_node_rater_defined("cds/layers/rate_change", {
        "premium": hx.Structure(children={
            "line_100pct": hx.Structure(children={
                "annualised": hx.Structure(view={"label": 'Premium - Annualised (100% Line)'}, children={**renewal_expiring()})
            }),
            "beazley_line": hx.Structure(children={
                "policy_term": hx.Structure(view={"label": 'Premium - Policy Term (Beazley Line)'}, children={**renewal_expiring()}),
                "annualised": hx.Structure(view={"label": 'Premium - Annualised (Beazley Line)'}, children={**renewal_expiring()}),
            }),
        }),
        "expiring_policy_info": hx.Structure(children={
            "expiring_exposure": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_policy_length": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_premium": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_limit": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_deductible": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_brokerage": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_write_line": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_expected_loss": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_section_reference": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
        }),
        "risk_adjusted_rate_change": hx.Float(mode="output", view={"label": "Final Risk Adjusted Rate Change", "format": percent_format()}),
        "risk_adjusted_rate_change_case_priced": hx.Float(mode="input", optionality='optional', default=None, view={"label": "Final Risk Adjusted Rate Change", "format": percent_format(), "options": {"read_only": {"read_only": True}}}),
        "risk_adjusted_rate_change_gross_for_reporting": hx.Float(mode="output"),
        "error_message": hx.Str(mode="output"),
        "temp_storage": hx.Structure(children={ # To store premiums when running the RARC calculation
            "quoted_premium": hx.Float(mode="output", async_output=["rarc_task"]),
            "benchmark_premium": hx.Float(mode="output", async_output=["rarc_task"]),
        })
    })