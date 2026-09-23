import hx_data_schema as hxd
from libraries.common_data_schema.data_schema.utilities import percent_format, thousands_format

from algorithms.rate_constants import max_layers
from algorithms.rate_utilities import get_layer_labels


def renewal_expiring():
    return {
        "expiring": hxd.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Expiring", "format": thousands_format()}),
        "rebased_expiring": hxd.Float(mode="output", view={"label": "Rebased\nExpiring", "format": thousands_format()}),
        "renewal": hxd.Float(mode="output", view={"label": "Renewal", "format": thousands_format()})
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
        "rate_change": hxd.Structure(children={
            **{f"show_layer_{index}": hxd.Bool(mode="output") for index in range(1,max_layers+1)},
            "expiring_policy_option_id": hxd.Int(mode="override", async_input=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Expiring Policy Option", "format": {"thousandSeparated": False}}),
            "has_fetch_not_run": hxd.Bool(mode="input", default=True, async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "has_fetch_run": hxd.Bool(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "has_rarc_not_run": hxd.Bool(mode="input", default=True, async_output=["rarc_task"]),
            "has_rarc_run": hxd.Bool(mode="output", async_output=["rarc_task"]),
            "rarc_run_again_message": hxd.Str(mode="output"),
            "rarc_message_show": hxd.Bool(mode="output"),
            "layer_mapping": hxd.Str(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"])
        })
    })

    cds.override_node_properties("cds/layers/rate_change/expiring_layer", {
        "mode": "output",
        "async_output": [{"task": "rarc_task", "reset": False}, {"task": "expiring_policy_fetch_task", "reset": False}],
        "async_input": ["expiring_policy_fetch_task", "rarc_task"],
        "options": [*range(1, max_layers + 1)]
    })

    cds.override_node_properties("cds/layers/rate_change/other_change", {"view": {"label": "Other Change (incl. Brokerage)"}})

    cds.extend_node_rater_defined("cds/layers/rate_change", {
        "expiring_layer_label": hxd.Str(mode="input", optionality="optional", async_input=["expiring_policy_fetch_task", "rarc_task"], options=get_layer_labels(), default="Primary", view={"label": "Expiring Layer"}),
        "premium": hxd.Structure(children={
            "line_100pct": hxd.Structure(children={
                "annualised": hxd.Structure(view={"label": 'Premium - Annualised (100% Line)'}, children={**renewal_expiring()})
            }),
            "beazley_line": hxd.Structure(children={
                "policy_term": hxd.Structure(view={"label": 'Premium - Policy Term (Beazley Line)'}, children={**renewal_expiring()}),
                "annualised": hxd.Structure(view={"label": 'Premium - Annualised (Beazley Line)'}, children={**renewal_expiring()}),
            }),
        }),
        "expiring_policy_info": hxd.Structure(children={
            "expiring_exposure": hxd.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_policy_length": hxd.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_premium": hxd.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_limit": hxd.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_deductible": hxd.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_brokerage": hxd.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_write_line": hxd.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_expected_loss": hxd.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_section_reference": hxd.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
        }),
        "risk_adjusted_rate_change": hxd.Float(mode="output", view={"label": "Final Risk Adjusted Rate Change", "format": percent_format()}),
        "risk_adjusted_rate_change_case_priced": hxd.Float(mode="input", optionality='optional', default=None, view={"label": "Final Risk Adjusted Rate Change", "format": percent_format(), "options": {"read_only": {"read_only": True}}}),
        "risk_adjusted_rate_change_gross_for_reporting": hxd.Float(mode="output"),
        "error_message": hxd.Str(mode="output"),
        "temp_storage": hxd.Structure(children={ # To store premiums when running the RARC calculation
            "quoted_premium": hxd.Float(mode="output", async_output=["rarc_task"]),
            "benchmark_premium": hxd.Float(mode="output", async_output=["rarc_task"]),
            "currency": hxd.Str(mode="input", default=None, async_input=["rarc_task"],async_output=["rarc_task"], optionality="optional",  view={"label": "Currency"}),

        }),
        "new_layer": hxd.Bool(mode="output", view={"label": "New Layer"}), # Edit Addition v0.3.0 
        "renewing_layer": hxd.Bool(mode="output",async_input= ["rarc_task"]), # Edit Addition v0.3.0 
        "show_expiring_revalued": hxd.Bool(mode="output",async_input= ["rarc_task"]), # Edit Addition v0.3.0 - Amount converted in renewing currency use to handle change in currency at renewal.

    })
