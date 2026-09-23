import hx_data_schema as hx
import data_schema.sch_utilities as utils
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers

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

    for change in rarc_changes:
        cds.override_node_properties(
            f"cds/layers/rate_change/{change}/model_calculated", {"async_output": ["rarc_task"],"view":{"format": utils.percent_format(1)}} 
        )
        cds.override_node_properties(
            f"cds/layers/rate_change/{change}/uw_selected", {"async_input": ["generate_email_task","generate_referral_email_task"],"view":{"format": utils.percent_format(1)}, "async_output" : [{"task": "rarc_task", "reset": False}, "initialise_model", "clear_overrides_task","start_renewal_task"]} 
        )
        cds.override_node_properties(
            f"cds/layers/rate_change/{change}/comments", {"async_input": ["generate_email_task","generate_referral_email_task"], "async_output": [{"task": "rarc_task", "reset": False}, {"task": "initialise_model", "reset": False}, "start_renewal_task"]} 
        )

  
    
    cds.extend_node_rater_defined("cds", {
        "rate_change": hx.Structure(children={
            **{f"show_layer_{index}": hx.Bool(mode="output") for index in range(1,max_layers+1)},
            "expiring_policy_option_id": hx.Int(mode="override", async_input=["expiring_policy_fetch_task", "rarc_task","start_renewal_task","initialise_model"],async_output=["start_renewal_task","initialise_model"], view={"label": "Expiring Policy Option", "format": {"thousandSeparated": False}}),
            "has_fetch_not_run": hx.Bool(mode="input", default=True, async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "has_fetch_run": hx.Bool(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "has_rarc_not_run": hx.Bool(mode="input", default=True, async_output=["rarc_task"]),
            "has_rarc_run": hx.Bool(mode="output", async_output=["rarc_task"]),
            "rarc_run_again_message": hx.Str(mode="output"),
            "rarc_message_show": hx.Bool(mode="output"),
            "layer_mapping": hx.Str(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "instructions": hx.Str(mode="input",view={"label": "Instructions", "read_only":True,"multiline":True},
                default="""The rate change tab calculates the change in premium associated with each component (detailed descriptions in the table below). The most appropriate method to obtain a rate change is to calculate the change on premium rather than the change in underlying factors as there are numerous interactions and products to consider.

                    To calculate the rate change, please follow the steps below:
                    1) The user should fist click 'Fetch Expiring Data' to initialise the rate change calculation.
                    2) If there have been any changes to the previous tabs (including the first instance of reaching this tab in any record/YOA), please press 'Calculate Rate Change'.
                    3) The rater will derive the rate changes to each component from the user input.
                    4) The user will be able to override the rate change values as appropriate in the 'UW Selected %' column.
                    5) To recalculate rate change following further changes, please press 'Calculate Rate Change' again.
                    6) Following the task running, the user will be able to override 'Expiring' and 'Renewal' fields with rate change automatically calculating WITHOUT havinng to run the task again. 

                    _Rate Change Components Include:_
                    _**Exposure Change**_: Driven by changes to base premium (due to revenue, product, class, base rate, venue and exposure measure)
                    _**Risk Characteristics Change**_: Driven by changes to schedule modifiers, cyber modifiers, currency)
                    _**Deductible Change**_: Driven by changes to retentions (main, cyber)
                    _**Limit Change**_: Driven by changes to EEL, agg limits (main, cyber, umbrella)
                    _**Terms and Conditions Change**_: Driven by changes to coverages included, retro date, claims basis, policy term, Tech E&O, Umbrella
                    _**Brokerage Change**_: Driven by Brokerage changes
                    _**Other Change**_: Driven by any other factor
                    """),
        })
    })

    cds.override_node_properties("cds/layers/rate_change/expiring_layer", {
        "mode": "output",
        "async_input": ["expiring_policy_fetch_task", "rarc_task"],
        "options": [*range(1,max_layers+1)],        
    })


    cds.extend_node_rater_defined("cds/layers/rate_change", {
        "expiring_layer_dropdown": hx.Str(mode="input", default="Primary", options=["Primary", "Excess 1", "Excess 2", "Excess 3", "Excess 4", "Excess 5", "Excess 6", "Excess 7", "Excess 8", "Excess 9", "Excess 10"], async_input=["expiring_policy_fetch_task", "rarc_task","generate_email_task","generate_referral_email_task"],view={"label": "Expiring Layer"}),
        "rebased_expiring_premium": hx.Float(mode="output", async_output=["rarc_task"], view={"label": "Rebased Expiring Premium", "format": thousands_format()}),
        "renewal_premium_warning": hx.Str(mode="output"),
        "renewal_premium_warning_show": hx.Bool(mode="output"),
        **{
            item: hx.Structure(view={"label": label}, children={
            "renewal": hx.Float(mode="input", default = None,  optionality = "optional",view={"label": "Actual Renewal Premium", "format": {"thousandSeparated": True, "mantissa": 0}},async_output=[{"task":"expiring_policy_fetch_task", "reset": False}, {"task":"rarc_task", "reset": False},"stat_renewal_task"],async_input=["generate_email_task","generate_referral_email_task"]),
            "expiring": hx.Float(mode="input", default = None, optionality = "optional",async_output=["expiring_policy_fetch_task", {"task":"rarc_task", "reset": False},"stat_renewal_task"], view={"label": "Expiring Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "implied": hx.Float(mode="output", view={"label": "Implied Renewal Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
            })
            for item, label in zip(["premium_policy_term_beazley_share",  "premium_policy_term_100pct", "premium_annualized_beazley_share", "premium_annualized_100pct"], ["Premium - Policy Term (Beazley Share)", "Premium - Policy Term (100% Share)","Premium - Annualized (Beazley Share)", "Premium - Annualized (100% Share)"])
        },
        "expiring_policy_info": hx.Structure(children={
            "expiring_exposure": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_policy_length": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_premium": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_limit": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_deductible": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_brokerage": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_write_line": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_expected_loss": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_section_reference": hx.Str(mode="input", default = None, optionality = "optional",view={"label": "Layer Label"}, async_output=["start_renewal_task","initialise_model"]),
        }),
        "total_change": hx.Structure(view={"label":"Total Change dictates change of"}, children={
            "calculated": hx.Float(mode="output", view={"label":"Model %", "format": utils.percent_format(1)}),
            "selected": hx.Float(mode="output", view={"label": "UW Selected %", "format": utils.percent_format(1)}),
            "comments": hx.Str(mode="input", default="", view={"label": "Comment"}),
        }),              
        "simple_rate_change": hx.Float(mode="output", view={"label": "Pure Premium Change / Simple Rate Change", "format": utils.percent_format(1)}),
        "risk_adjusted_rate_change": hx.Structure(view={"label": "Underwriter Selected"}, children={
            "technical": hx.Float(mode="output", view={"label": "Model Risk Adjusted Rate Change", "format": utils.percent_format(1)}),
            "technical_net_brokerage": hx.Float(mode="output", view={"format": utils.percent_format(1)}),
            "uw_selected": hx.Float(mode="output",async_input=["generate_email_task","generate_referral_email_task"], view={"label": "UW Selected Risk Adjusted Rate Change", "format": utils.percent_format(1)}),
            "uw_selected_net_brokerage": hx.Float(mode="output", view={"label": "UW Selected Risk Adjusted Rate Change","format": utils.percent_format(1)}),
        }),
        "risk_adjusted_rate_change_case_priced": hx.Structure(view={"label": "Underwriter Selected"}, children={
            "uw_selected": hx.Float(mode="override", view={"label": "UW Selected Risk Adjusted Rate Change", "format": utils.percent_format(1)}),
            "uw_selected_net_brokerage": hx.Float(mode="output", view={"label": "UW Selected Risk Adjusted Rate Change Net Brokerage","format": utils.percent_format(1)}),
            "comments": hx.Str(mode="input", default="", view={"label": "Comment"}),
        }),
        "error_message": hx.Str(mode="output"),
        "temp_storage": hx.Structure(children={ # To store premiums when running the RARC calculation
            "quoted_premium": hx.Float(mode="output", async_output=["rarc_task"]),
            "benchmark_premium": hx.Float(mode="output", async_output=["rarc_task"]),
        })
    })