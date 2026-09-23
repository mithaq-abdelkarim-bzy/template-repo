import hx_data_schema as hx
import data_schema.sch_utilities as utils
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers
import copy

def sch_rate_change(cds):
    
    cds.extend_node_rater_defined("cds", {
        "rate_change": hx.Structure(children={
            **{f"show_layer_{index}": hx.Bool(mode="output") for index in range(1,max_layers+1)},
            "expiring_policy_option_id": hx.Int(mode="override", async_input=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Expiring Policy Option", "format": {"thousandSeparated": False}}),
            "rarc_calc_update": hx.Str(mode="output", async_output=["rarc_task"]),
            "rarc_run_again_message": hx.Str(mode="output"),
            "rarc_message_show": hx.Bool(mode="output"),
            "rarc_calcs_show": hx.Bool(mode="output"),
            "has_fetch_not_run": hx.Bool(mode="input", default=True, async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "has_fetch_run": hx.Bool(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "has_rarc_not_run": hx.Bool(mode="input", default=True, async_output=["rarc_task"]),
            "has_rarc_run": hx.Bool(mode="output", async_output=["rarc_task"]),
            "has_expiring_data": hx.Bool(mode="output"),  
            "layer_mapping": hx.Str(mode="output", async_output=[ "expiring_policy_fetch_task","rarc_task"]),
            "fetch_rarc_show_hide": hx.Bool(mode="output"),
            "fetch_rarc_show_hide_renewal": hx.Bool(mode="output", async_output=["start_renewal_task"]),
            "remove_tasks_errors":hx.Str(mode="input", default = "No",  options = ["Yes", "No"], async_input=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Get Back to Non-Renewal Status - Need to Re-run the two buttons"}, async_output=["clear_rate_change"]),
            
        })
    })

    cds.extend_node_rater_defined("cds/layers", {
        "deal_status_record": hx.Str(mode="output", view = {"label": "Deal Status by Renewal Options"})
    })

    cds.override_node_properties(
       "cds/layers/rate_change/expiring_layer",
        {  
            "async_input": ["expiring_policy_fetch_task", "rarc_task"],
            "async_output": ["expiring_policy_fetch_task"],
            "options": [*range(1,max_layers+1)],
            "view":{"label":"Expiring Option"}
        }
    )

    cds.extend_node_rater_defined("cds/layers/rate_change", {
        # "deal_status_record": hx.Str(mode = "output", view={"label": "Deal Status by Renewal Layers"}),
        "rebased_expiring_premium": hx.Float(mode="output", async_output=["rarc_task"], view={"label": "Rebased Expiring Premium", "format": thousands_format()}),
        # "expiring_layer": hx.Int(default=1, mode="input", options=[*range(1,max_layers+1)], async_input=["expiring_policy_fetch_task", "rarc_task"],view={"label": "Expiring Option"}),
        **{
            item: hx.Structure(view={"label": label}, children={
            "renewal": hx.Float(mode="output", view={"label": "Renewal", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "expiring": hx.Float(mode="output", view={"label": "Expiring", "format": {"thousandSeparated": True, "mantissa": 0}}),
            })
            for item, label, format_ in zip(
                [
                    "premium_policy_term_beazley_share",  
                    "premium_policy_term_100pct", 
                    "premium_annualized_beazley_share", 
                    "premium_annualized_100pct"
                    "benchmark_premium",
                    "technical_premium",
                    "written_line",
                    "bpi",
                    "tpi"
                ], 
                [
                    "Premium - Policy Term (Beazley Share)",
                    "Premium - Policy Term (100% Share)",
                    "Premium - Annualized (Beazley Share)", 
                    "Premium - Annualized (100% Share)",
                    "benchmark_premium",
                    "technical_premium",
                    "written_line",
                    "bpi",
                    "tpi"
                ],
                [copy.deepcopy(thousands_format()) for _ in range(6)] + [copy.deepcopy(percent_format()) for _ in range(3)]
            )
        },
        "expiring_policy_info": hx.Structure(children={
            "expiring_exposure": hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_policy_length": hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_premium": hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_limit": hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_deductible": hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_brokerage": hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_written_line": hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_expected_loss": hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_technical_premium": hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_tpi": hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_benchmark_premium": hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_bpi": hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
        }),


        "total_change": hx.Structure(view={"label":"Total Change"}, children={
            "model_calculated": hx.Float(mode="output", view={"label":"Model %", "format": percent_format(1)}),
            "uw_selected": hx.Float(mode="output", view={"label": "UW Selected %", "format": percent_format(1)}),
            "comments": hx.Str(mode="input", default="", view={"label": "Comment"}),
        }),              
        "simple_rate_change": hx.Float(mode="output", view={"label": "Pure Premium Change / Simple Rate Change", "format": percent_format()}),
        "risk_adjusted_rate_change": hx.Structure(view={"label": "Underwriter Selected"}, children={
            "expiry_onlevel_premium_technical": hx.Float(mode = "output", view={"label": "Rebased Expiring Premium - Technical", "format": thousands_format()}),
            "expiry_onlevel_premium_technical_net": hx.Float(mode = "output", view={"label": "Rebased Expiring Net Premium - Technical", "format": thousands_format()}),
            "technical": hx.Float(mode="output", view={"label": "Model Risk Adjusted Rate Change", "format": percent_format()}),
            "technical_net_brokerage": hx.Float(mode="output", view={"format": percent_format()}),
            "expiry_onlevel_premium_uw_selected": hx.Float(mode = "output", view={"label": "Rebased Expiring Premium - UW Selected", "format": thousands_format()}),
            "expiry_onlevel_premium_uw_selected_net": hx.Float(mode = "output", view={"label": "Rebased Expiring Net Premium - UW Selected", "format": thousands_format()}),
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
            "benchmark_premium": hx.Float(mode="output", async_output=["rarc_task"])
        })
    }),
    
    rarc_changes = [
        "exposure_change",
        "risk_characteristics_change",
        "limit_change",
        "deductible_change",
        "terms_conditions_change",
        "other_change",
        "brokerage_change",
        "rate_change"
    ]

    for change in rarc_changes:
        cds.override_node_properties(
            f"cds/layers/rate_change/{change}/model_calculated",
            {"view": {"label": "Model", "format": percent_format(1)}, "async_output": ["rarc_task"]} 
        )
        cds.override_node_properties(
            f"cds/layers/rate_change/{change}/uw_selected",
            {"view": {"label": "UW Selected", "format": percent_format(1)}}
        )
    
    
    cds.override_node_properties(
        "cds/rate_change/expiring_policy_option_id", {"view":{"label": "Expiring Policy Reference ID"}}
    )
    
    
    
    
    