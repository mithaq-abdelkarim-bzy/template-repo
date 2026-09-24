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
            f"cds/layers/rate_change/{change}/model_calculated", {
                "mode": "input", 
                "default": None, 
                "optionality": "optional", 
                "async_output": ["rarc_task", "rc_private_task"],
                "view":{"format": {"output": "percent", "mantissa": 2}, "read_only": True}
            } 
        )
    
    cds.extend_node_rater_defined("cds", {
        "rate_change": hx.Structure(children={
            **{f"show_layer_{index}": hx.Bool(mode="output") for index in range(1,max_layers+1)},
            "expiring_policy_option_id": hx.Int(mode="override", async_input=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Expiring Policy Option", "format": {"thousandSeparated": False}}),
            "has_fetch_not_run": hx.Bool(mode="input", default=True, async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "has_fetch_run": hx.Bool(mode="input", default=None, optionality="optional", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "has_rarc_not_run": hx.Bool(mode="input", default=True, async_output=["rarc_task"]),
            "has_rarc_run": hx.Bool(mode="input", default=None, optionality="optional", async_output=["rarc_task"]),
            "rarc_run_again_message": hx.Str(mode="output"),
            "rarc_message_show": hx.Bool(mode="output"),
            "layer_mapping": hx.Str(mode="input", default=None, optionality="optional", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "instructions": hx.Str(mode="input",view={"label": "Instructions", "read_only":True,"multiline":True},
                default="""The rate change tab calculates the change in premium associated with each component (detailed descriptions in the table below). The most appropriate method to obtain a rate change is to calculate the change on premium rather than the change in underlying factors as there are numerous interactions and products to consider.

                    To calculate the rate change, please follow the steps below:
                    1) The user should fist click 'Fetch Expiring Data' to initialise the rate change calculation.
                    2) Select mapping between renewing layers and expiry, this needs to be a 1-1 mapping so for layers that are not needed for rate change calculations, select the empty option.
                    3) If there have been any changes to the previous tabs (including the first instance of reaching this tab in any record/YOA), please press 'Calculate Rate Change'.
                    4) The rater will derive the rate changes to each component from the user input.
                    5) The user will be able to override the rate change values as appropriate in the 'UW Selected %' column.
                    6) To recalculate rate change following further changes, please press 'Calculate Rate Change' again.
                    7) Following the task running, the user will be able to override 'Expiring' and 'Renewal' fields with rate change automatically calculating WITHOUT having to run the task again. 

                    _Rate Change Components Include:_
                    _**Exposure Change**_: Driven by changes to base premium due to market cap, assets, country, and industry
                    _**Risk Characteristics Change**_: Driven by changes to schedule modifiers
                    _**Deductible Change**_: Driven by changes to excesses, and deductibles
                    _**Limit Change**_: Driven by changes to limits 
                    _**Terms and Conditions Change**_: Driven by changes to coverages selected
                    _**Other Change**_: Driven by any other factors such as brokerage
                    """),
            "show_rarc_table": hx.Bool(mode="output", async_input=["rarc_task"], view={"label": "Show Rate Change Table"}),
        })
    })

    #cds.override_node_properties(
    #    "cds/layers/rate_change/model_calculated", 
    #    {  
    #        "view":{"format": {"output": "percent", "mantissa": 2}}
    #    } 
    #)

    cds.override_node_properties(
        "cds/layers/rate_change/expiring_layer", 
        {  
            "async_input": ["expiring_policy_fetch_task", "rarc_task"],
            "options": [*range(1,max_layers+1)]
        } 
    )

    cds.override_node_properties(
        "cds/layers/rate_change/other_change", {"view":{"label":"Other Change (incl. Brokerage)"}}
    )
    
    renewal_vs_expiry = [
        "premium_policy_term_beazley_share",  
        "premium_policy_term_100pct", 
        "premium_annualized_beazley_share", 
        "premium_annualized_100pct",
        "limit",
        "deductible",
        "excess",
        "side_a_excess",
        "abc_tower",
        "total_excess",
        "market_cap",
        "asset_size",
        "insider_share",
        "revised_market_cap",
        "exp_sector_freq",
        "exp_freq",
        "brokerage"
    ]

    renewal_vs_expiry_label = [
        "Premium - Policy Term (Beazley Share)", 
        "Premium - Policy Term (100% Share)",
        "Premium - Annualized (Beazley Share)", 
        "Premium - Annualized (100% Share)",
        "Limit",
        "Deductible",
        "Excess",
        "Side A Excess",
        "ABC Tower",
        "Total Excess",
        "Market Cap",
        "Asset Size",
        "Insider Shareholder Share",
        "Revsised Market Cap",
        "Expected Sector Frequency",
        "Expected Frequency",
        "Brokerage",
    ]

    cds.extend_node_rater_defined("cds/layers/rate_change", {
        # Creating copies of the fields from the common data schema that are uneditable
        "exposure_change_fixed": hx.Structure(view={"label": "Exposure Change"}, children={
            "model_calculated": hx.Float(mode="output", view={"label": "Model %", "format": {"output": "percent", "mantissa": 2}}),
            "uw_selected": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "UW Selected %", "format": {"output": "percent", "mantissa": 2}}),
            "comments": hx.Str(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Comment"}),
        }),
        "limit_change_fixed": hx.Structure(view={"label": "Limit Change"}, children={
            "model_calculated": hx.Float(mode="output", view={"label": "Model %", "format": {"output": "percent", "mantissa": 2}}),
            "uw_selected": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "UW Selected %", "format": {"output": "percent", "mantissa": 2}}),
            "comments": hx.Str(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Comment"}),
        }),
        "deductible_change_fixed": hx.Structure(view={"label": "Deductible Change"}, children={
            "model_calculated": hx.Float(mode="output", view={"label": "Model %", "format": {"output": "percent", "mantissa": 2}}),
            "uw_selected": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "UW Selected %", "format": {"output": "percent", "mantissa": 2}}),
            "comments": hx.Str(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Comment"}),
        }),
        "excess_change_fixed": hx.Structure(view={"label": "Excess Change"}, children={
            "model_calculated": hx.Float(mode="output", view={"label": "Model %", "format": {"output": "percent", "mantissa": 2}}),
            "uw_selected": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "UW Selected %", "format": {"output": "percent", "mantissa": 2}}),
            "comments": hx.Str(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Comment"}),
        }),
        "other_change_fixed": hx.Structure(view={"label": "Other Change (incl. Brokerage)"}, children={
            "model_calculated": hx.Float(mode="output", view={"label": "Model %", "format": {"output": "percent", "mantissa": 2}}),
            "uw_selected": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "UW Selected %", "format": {"output": "percent", "mantissa": 2}}),
            "comments": hx.Str(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Comment"}),
        }),
        "brokerage_change_fixed": hx.Structure(view={"label": "Brokerage Change"}, children={
            "model_calculated": hx.Float(mode="output", view={"label": "Model %", "format": {"output": "percent", "mantissa": 2}}),
            "uw_selected": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "UW Selected %", "format": {"output": "percent", "mantissa": 2}}),
            "comments": hx.Str(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Comment"}),
        }),
        "asset_size_change_fixed": hx.Structure(view={"label": "Asset Size  Change"}, children={
            "model_calculated": hx.Float(mode="output", view={"label": "Model %", "format": {"output": "percent", "mantissa": 2}}),
            "uw_selected": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "UW Selected %", "format": {"output": "percent", "mantissa": 2}}),
            "comments": hx.Str(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Comment"}),
        }),
        # other changes are in the library. Adding this here bec I don't think other models will need it in the library
        "asset_size_change": hx.Structure(view={"label": "Asset Size Change"}, children={
            "model_calculated": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Model %", "format": {"output": "percent", "mantissa": 2}}),
            "uw_selected": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "UW Selected %", "format": {"output": "percent", "mantissa": 2}}),
            "comments": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
        }),
        "excess_change": hx.Structure(view={"label": "Excess Change"}, children={
            "model_calculated": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Model %", "format": {"output": "percent", "mantissa": 2}}),
            "uw_selected": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "UW Selected %", "format": {"output": "percent", "mantissa": 2}}),
            "comments": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
        }),
        "rebased_expiring_premium": hx.Float(mode="input", default=None, optionality="optional", async_output=["rarc_task"], view={"label": "Rebased Expiring Premium", "format": thousands_format()}),
        **{
            item: hx.Structure(view={"label": label}, children={
            "renewal": hx.Float(mode="output", view={"label": "Renewal", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "expiring": hx.Float(mode="override",  optionality="optional", async_input=["expiring_policy_fetch_task", "rarc_task", "rc_private_task"], async_output=[{"task": "expiring_policy_fetch_task", "reset": False},  {"task": "rarc_task", "reset": False}], view={"label": "Expiring", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "private_priced": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task", "rc_private_task"], view={"label": "Expiring","format": {"thousandSeparated": True, "mantissa": 0}}), # once we have a year of data we can remove this and repoint the private D&O expiring to the overally expiring
            })
            for item, label in zip(renewal_vs_expiry, renewal_vs_expiry_label)
        },
        "ei_offered": hx.Structure(view={"label": "EI offered (ABC only)"}, children={
            "renewal": hx.Bool(mode="input", default=False, view={"label": "Renewal"}),
            "expiring": hx.Bool(mode="input", default=False, async_output=["expiring_policy_fetch_task", "rarc_task"]),
        }),
        "expiring_policy_info": hx.Structure(children={
            "expiring_exposure": hx.Float(mode="input", default=None, optionality="optional", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_policy_length": hx.Float(mode="input", default=None, optionality="optional", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_premium": hx.Float(mode="input", default=None, optionality="optional", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_limit": hx.Float(mode="input", default=None, optionality="optional", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_deductible": hx.Float(mode="input", default=None, optionality="optional", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_brokerage": hx.Float(mode="input", default=None, optionality="optional", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_write_line": hx.Float(mode="input", default=None, optionality="optional", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_expected_loss": hx.Float(mode="input", default=None, optionality="optional", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "expiring_excess": hx.Float(mode="input", default=None, optionality="optional", async_output=["expiring_policy_fetch_task", "rarc_task"]),
        }),
        "total_change": hx.Structure(view={"label":"Total Change dictates change of"}, children={
            "calculated": hx.Float(mode="output", view={"label":"Model %", "format": percent_format()}),
            "selected": hx.Float(mode="output", view={"label": "UW Selected %", "format": percent_format()}),
            "comments": hx.Str(mode="input", default="", view={"label": "Comment"}),
        }),              
        "simple_rate_change": hx.Float(mode="output", view={"label": "Pure Premium Change / Simple Rate Change", "format": percent_format()}),
        "risk_adjusted_rate_change": hx.Structure(view={"label": "Underwriter Selected"}, children={
            "technical": hx.Float(mode="output", view={"label": "Model Risk Adjusted Rate Change", "format": {"output": "percent", "mantissa": 2}}),
            "technical_net_brokerage": hx.Float(mode="output", view={"format": percent_format()}),
            "uw_selected": hx.Float(mode="output", view={"label": "UW Selected Risk Adjusted Rate Change", "format": {"output": "percent", "mantissa": 2}}),
            "uw_selected_net_brokerage": hx.Float(mode="output", view={"label": "UW Selected Risk Adjusted Rate Change","format": {"output": "percent", "mantissa": 2}}),
        }),
        "new_calculated_premium": hx.Structure(view={"label": "Underwriter Selected"}, children={
            "technical": hx.Float(mode="output", view={"label": "Model New Calculated Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_net_brokerage": hx.Float(mode="output", view={"label": "Model New Calculated Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "uw_selected": hx.Float(mode="output", view={"label": "UW Selected New Calculated Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "uw_selected_net_brokerage": hx.Float(mode="output", view={"label": "UW Selected New Calculated Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
        }),
        "new_premium": hx.Structure(view={"label": "Underwriter Selected"}, children={
            "gross": hx.Float(mode="output", view={"label": "New Premium (as per slip)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "net_brokerage": hx.Float(mode="output", view={"label": "New Premium (as per slip)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        }),
        "risk_adjusted_rate_change_case_priced": hx.Structure(view={"label": "Underwriter Selected"}, children={
            "uw_selected": hx.Float(mode="override", view={"label": "UW Selected Risk Adjusted Rate Change", "format": percent_format()}),
            "uw_selected_net_brokerage": hx.Float(mode="output", view={"label": "UW Selected Risk Adjusted Rate Change Net Brokerage","format": percent_format()}),
            "comments": hx.Str(mode="input", default="", view={"label": "Comment"}),
        }),
        "error_message": hx.Str(mode="output"),
        "temp_storage": hx.Structure(children={ # To store premiums when running the RARC calculation
            "quoted_premium": hx.Float(mode="input", default=None, optionality="optional", async_output=["rarc_task"]),
            "benchmark_premium": hx.Float(mode="input", default=None, optionality="optional", async_output=["rarc_task"]),
        }),
        # New field for comments on why expiry information is overriden. TODO: make the expiry information overrides
        "overriden_expiring": hx.Structure(children={
            "is_overriden": hx.Bool(mode="output"),
            "comments": hx.Str(mode="input", default="", view={"label": "Comment"}),
        })
    })
    
    cds.extend_node_rater_defined("cds/layers/rate_change", {
        "private_rc_result": hx.Structure(
            view={"label": "Private RC Result"},
            children={"layer_index": hx.Int(mode="output", async_output=["rc_private_task"], view={"label": "Layer Index"}),
                "asset_rc": hx.Float(mode="output", async_output=["rc_private_task"], view={"label": "Asset RC", "format": {"output": "percent", "mantissa": 2}}),
                "limit_rc": hx.Float(mode="output", async_output=["rc_private_task"], view={"label": "Limit RC", "format": {"output": "percent", "mantissa": 2}}),
                "excess_rc": hx.Float(mode="output", async_output=["rc_private_task"], view={"label": "Excess RC", "format": {"output": "percent", "mantissa": 2}}),
                "deductible_rc": hx.Float(mode="output", async_output=["rc_private_task"], view={"label": "Deductible RC", "format": {"output": "percent", "mantissa": 2}}),
                "risk_characteristics_rc": hx.Float(mode="output", async_output=["rc_private_task"], view={"label": "Risk Characteristics RC", "format": {"output": "percent", "mantissa": 2}}),
                "terms_conditions_rc": hx.Float(mode="output", async_output=["rc_private_task"], view={"label": "T&C RC", "format": {"output": "percent", "mantissa": 2}}),
                "brokerage_rc": hx.Float(mode="output", async_output=["rc_private_task"], view={"label": "Brokerage RC", "format": {"output": "percent", "mantissa": 2}}),
                "other_rc": hx.Float(mode="output", async_output=["rc_private_task"], view={"label": "Other RC", "format": {"output": "percent", "mantissa": 2}}),
                "total_rc": hx.Float(mode="output", async_output=["rc_private_task"], view={"label": "Total RC", "format": {"output": "percent", "mantissa": 2}}),
            })
        })
#### Formatting ####
    cds.override_node_properties("cds/layers/rate_change/insider_share/renewal", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/layers/rate_change/insider_share/expiring", {"mode": "override","view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/layers/rate_change/brokerage/renewal", {"async_input": ["rarc_task", "rc_private_task"], "view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/layers/rate_change/brokerage/expiring", {"mode": "override", "view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/layers/rate_change/brokerage/private_priced", {"async_input": ["rarc_task", "rc_private_task"], "view": {"format": {"output": "percent", "mantissa": 2}}})

    cds.override_node_properties("cds/layers/rate_change/risk_characteristics_change/uw_selected", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/layers/rate_change/rate_change/uw_selected", {"view": {"format": {"output": "percent", "mantissa": 2}}})
    cds.override_node_properties("cds/layers/rate_change/rate_change/model_calculated", {"view": {"format": {"output": "percent", "mantissa": 2}}})

#### Updating async tasks ####

# This is only necessary because of set_child_nodes_to_rarc_task_inputs(cds.get_data_schema(), cds)
# All these updates are in the extend_node_rater_defined function above
# However, these get overrided with async_input=["rarc_task"] unless they are set again here

    cds.override_node_properties('cds/rate_change/expiring_policy_option_id',{'async_input':["expiring_policy_fetch_task"]})
    cds.override_node_properties("cds/exposure/aggregate/total_assets",{"async_input": ["rarc_task", "rc_private_task"], "async_output": ["populate_capiq_data_task", "populate_capiq_data_from_wb_task"]})
    cds.override_node_properties("cds/layers/rate_change/asset_size/renewal",{"async_input": ["rarc_task", "rc_private_task"]})
    cds.override_node_properties("cds/layers/rate_change/asset_size/private_priced", {"async_input": ["rarc_task", "rc_private_task"]})
    cds.override_node_properties("cds/layers/rate_change/limit/private_priced", {"async_input": ["rarc_task", "rc_private_task"]})
    cds.override_node_properties("cds/layers/rate_change/limit/renewal",{"async_input": ["rarc_task", "rc_private_task"]})
    cds.override_node_properties("cds/layers/rate_change/deductible/private_priced",{"async_input": ["rarc_task", "rc_private_task"]})
    cds.override_node_properties("cds/layers/rate_change/deductible/renewal",{"async_input": ["rarc_task", "rc_private_task"]})
    cds.override_node_properties("cds/layers/rate_change/excess/private_priced",{"async_input": ["rarc_task", "rc_private_task"]})
    cds.override_node_properties("cds/layers/rate_change/excess/renewal", {"async_input": ["rarc_task", "rc_private_task"]})
    cds.override_node_properties("cds/layers/rate_change/total_excess/private_priced",{"async_input": ["rarc_task", "rc_private_task"]})
    cds.override_node_properties("cds/layers/rate_change/total_excess/renewal",{"async_input": ["rarc_task", "rc_private_task"]})
    cds.override_node_properties('cds/coverage', {'options': ["ABC", "Side A", "Armour"], 'async_input':['rarc_task', 'rc_private_task', 'generate_tags_cuap', 'generate_tags_twice']})
    # cds.override_node_properties("cds/coverage", {"async_input": ["rarc_task", "rc_private_task"]})
    # cds.override_node_properties("cds/layers/rate_change/brokerage/private_priced", {"async_input": ["rarc_task", "rc_private_task"]})

    # cds.override_node_properties("cds/layers/rate_change/exposure_change/uw_selected", {"async_output": ["rarc_task", "rc_private_task"]})
    # cds.override_node_properties("cds/layers/rate_change/excess_change/uw_selected", {"async_output": ["rarc_task", "rc_private_task"]})
    cds.override_node_properties("cds/layers/rate_change/premium_annualized_100pct/private_priced", {"async_input": ["rarc_task", "rc_private_task"]})
    cds.override_node_properties("cds/layers/rate_change/premium_annualized_100pct/renewal", {"async_input": ["rarc_task", "rc_private_task"]})
    # cds.override_node_properties("cds/layers/rate_change/exposure_change_fixed/model_calculated", {"async_input": ["rarc_task", "rc_private_task"]})

    
    cds.override_node_properties("cds/layers/coverages/abc/brokerage", {"async_input": ["rarc_task", "rc_private_task"]})
    cds.override_node_properties("cds/layers/coverages/side_a/brokerage",{"async_input": ["rarc_task", "rc_private_task"]})

