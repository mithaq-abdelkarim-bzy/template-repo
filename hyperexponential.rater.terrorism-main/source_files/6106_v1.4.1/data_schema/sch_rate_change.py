import hx_data_schema as hx
import data_schema.sch_utilities as utils
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers
from algorithms.data_schema.sch_rater_defined import coverages_dict
import copy


def renewal_expiring(): return {
    "expiring":             hx.Float(mode="output", async_output=["expiring_policy_fetch_task"],    view={"label": "Expiring",          "format": thousands_format()}),
    "rebased_expiring":     hx.Float(mode="output",                                                 view={"label": "Rebased\nExpiring", "format": thousands_format()}),
    "renewal":              hx.Float(mode="output",                                                 view={"label": "Renewal",           "format": thousands_format()}),
}

def expiring_overrride(): return {
    "expiring_override":   hx.Float(mode="input", default = None, optionality="optional",            view={"label": "Expiring Override", "format": thousands_format()}),
}


def sch_rate_change(cds):
    rarc_changes = {
        "exposure_change": {"label": "Exposure Change"},
        "risk_characteristics_change": {"label": "Risk Characteristics Change"},
        "limit_change": {"label": "Limit Change"},
        "deductible_change": {"label": "Deductible Change"},
        "terms_conditions_change": {"label": "Terms & Conditions Change"},
        "other_change": {"label": "Other Change"},
        "brokerage_change": {"label": "Brokerage Change"},
        "rate_change": {"label": "Risk Adjusted Rate Change"}
    }

    for change in rarc_changes.keys():
        cds.override_node_properties(
            f"cds/layers/rate_change/{change}/model_calculated",
            {   "view"         : {"label": "Model", "format": percent_format(1)}
              , "async_output" : [] if change == "rate_change"  else ["rarc_task"]}
        )
        cds.override_node_properties(
            f"cds/layers/rate_change/{change}/uw_selected",
            {   "view"         : {"label": "UW Selected", "format": percent_format(1)}
              , "async_output" : [] if change=="rate_change" else ["rarc_task","start_renewal_task"]}                            # added this to clear out the inputs on start of renewal.
        )
        cds.override_node_properties( f"cds/layers/rate_change/{change}/comments",  {"async_output" : ["start_renewal_task"]})  # added this to clear out the inputs on start of renewal.    
        cds.override_node_properties( f"cds/layers/rate_change/other_change",       {"view": {"label": "Other Change",  "info" : "Includes Brokerage Change"}})     # YZ request July 25
        

    cds.extend_node_rater_defined("cds", {
        "rate_change": hx.Structure(children={
            **{f"show_layer_{index}": hx.Bool(mode="output") for index in range(1,max_layers+1)},
            "expiring_policy_option_id": hx.Int(mode="override", async_input=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Expiring Policy Option", "format": {"thousandSeparated": False}}),
            "has_fetch_not_run": hx.Bool(mode="input", default=True, async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "has_fetch_run": hx.Bool(mode="output", async_output=["expiring_policy_fetch_task"]),
            "has_rarc_not_run": hx.Bool(mode="input", default=True, async_output=["rarc_task"]),
            "has_rarc_run": hx.Bool(mode="output", async_output=["rarc_task"]),
            "rarc_run_again_message": hx.Str(mode="output"),
            "rarc_message_show": hx.Bool(mode="output"),
            "layer_mapping": hx.Str(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "rarc_calc_update": hx.Str(mode="output", async_output=["rarc_task"]),
            "rarc_calcs_show": hx.Bool(mode="output")
        })
    })    
    cds.override_node_properties("cds/layers/rate_change/expiring_layer",     {  "async_input": ["expiring_policy_fetch_task", "rarc_task"],    "options": [*range(1,max_layers+1)]  }     )

    # Define common RC fields
    def expiring_and_renewal():
        return {
            item: hx.Structure(view={"label": label}, children={
            "renewal": hx.Float(mode="output", view={"label": "Renewal", "format": format_}),
            "expiring": hx.Float(mode="output", view={"label": "Expiring", "format": format_}),
            })
            for item, label, format_ in zip(
                [
                    "premium_policy_term_beazley_share",  
                    "premium_policy_term_100pct", 
                    "premium_annualized_beazley_share", 
                    "premium_annualized_100pct",
                    "benchmark_premium",
                    "bpi",
                    "written_line"
                ], 
                [
                    "Premium - Policy Term (Beazley Share)", 
                    "Premium - Policy Term (100% Share)",
                    "Premium - Annualized (Beazley Share)",
                    "Premium - Annualized (100% Share)",
                    "Gross Benchmark Premium",
                    "BPI",
                    "Beazley Share"
                ],
                [copy.deepcopy(thousands_format()) for _ in range(5)] + [copy.deepcopy(percent_format(1)) for _ in range(2)]
            )
        }

    rc_fields_rater = {
        "technical": hx.Float(mode="output", view={"label": "Model Risk Adjusted Rate Change", "format": percent_format()}),
        "technical_net_brokerage": hx.Float(mode="output", view={"format": percent_format()}),
        "uw_selected": hx.Float(mode="output", view={"label": "UW Selected Risk Adjusted Rate Change", "format": percent_format(1)}),
        "uw_selected_net_brokerage": hx.Float(mode="output", view={"label": "UW Selected Risk Adjusted Rate Change","format": percent_format()})
    }
    rc_fields_case_priced = {
        "uw_selected": hx.Float(mode="override", view={"label": "UW Selected Risk Adjusted Rate Change", "format": percent_format(1)}),
        "uw_selected_net_brokerage": hx.Float(mode="output", view={"label": "UW Selected Risk Adjusted Rate Change Net Brokerage","format": percent_format()}),
        "comments": hx.Str(mode="input", default="", view={"label": "Comment"})
    }
    rc_temp_storage = {
        "quoted_premium": hx.Float(mode="output", async_output=["rarc_task"]),
        "benchmark_premium": hx.Float(mode="output", async_output=["rarc_task"])
    }

    cds.extend_node_rater_defined("cds/layers/rate_change", {
        "premium": hx.Structure(children={
            "line_100pct": hx.Structure(children={
                "policy_term": hx.Structure(view={"label": 'Premium - Policy Term (100% Line)'}, children={**renewal_expiring()}),
                "annualised":  hx.Structure(view={"label": 'Premium - Annualised (100% Line)'}, children={**renewal_expiring(),**expiring_overrride()})
            }),
            "beazley_line": hx.Structure(children={
                "policy_term": hx.Structure(view={"label": 'Premium - Policy Term (Beazley Line)'}, children={**renewal_expiring()}),
                "annualised": hx.Structure(view={"label": 'Premium - Annualised (Beazley Line)'}, children={**renewal_expiring()}),
            }),
        }),
        "expiring_policy_info": hx.Structure(children={
            "expiring_exposure":            hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_policy_length":       hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_premium":             hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_limit":               hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_deductible":          hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_brokerage":           hx.Float(mode="output", async_output=["expiring_policy_fetch_task"], async_input=["rarc_task"]), 
            "expiring_written_line":        hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_expected_loss":       hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_section_reference":   hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_premium_annualised":  hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_benchmark_premium":   hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
            "expiring_bpi":                 hx.Float(mode="output", async_output=["expiring_policy_fetch_task"]),
        }),
        "risk_adjusted_rate_change_model_net":   hx.Float(mode="output", view={"label": "Risk Adjusted Rate Change - model - net",          "format": percent_format()}),
        "risk_adjusted_rate_change_model_gross": hx.Float(mode="output", view={"label": "Final Risk Adjusted Rate Change - model - gross",  "format": percent_format()}),
        "risk_adjusted_rate_change_uw_net":      hx.Float(mode="output", view={"label": "Final Risk Adjusted Rate Change - uw - net",       "format": percent_format()}),
        "risk_adjusted_rate_change_uw_gross":    hx.Float(mode="output", view={"label": "Final Risk Adjusted Rate Change - uw gross",       "format": percent_format()}),
        # "risk_adjusted_rate_change":             hx.Float(mode="output", view={"label": "Final Risk Adjusted Rate Change",                  "format": percent_format()}),  # removed as forms part of cds now
        # "risk_adjusted_rate_change_gross_for_reporting": hx.Float(mode="output"),                                                                                          # removed as forms part of cds now  
        "risk_adjusted_rate_change_case_priced": hx.Float(mode="input", optionality='optional', default=None, view={"label": "Final Risk Adjusted Rate Change", "format": percent_format(), "options": {"read_only": {"read_only": True}}}),
        "error_message": hx.Str(mode="output"),
        "temp_storage": hx.Structure(children={ # To store premiums when running the RARC calculation
            "quoted_premium": hx.Float(mode="output", async_output=["rarc_task"]),
            "benchmark_premium": hx.Float(mode="output", async_output=["rarc_task"]),
        }), 
        "simple_rate_change": hx.Float(mode="output", view={"label": "Pure Premium Change / Simple Rate Change", "format": percent_format()}),
        "total_change": hx.Structure(view={"label":"Total Change dictates change of"}, children={
            "calculated": hx.Float(mode="output", view={"label":"Model %", "format": percent_format()}),
            "selected": hx.Float(mode="output", view={"label": "UW Selected %", "format": percent_format()}),
            "comments": hx.Str(mode="input", default="", view={"label": "Comment"}),
        }),  
        "rebased_expiring_premium": hx.Float(mode="output", async_output=["rarc_task"], view={"label": "Rebased Expiring Premium", "format": thousands_format()}),
        **expiring_and_renewal(),

    })
