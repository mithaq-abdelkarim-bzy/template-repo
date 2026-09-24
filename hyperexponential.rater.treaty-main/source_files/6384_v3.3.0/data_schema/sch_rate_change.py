import hx_data_schema as hx
import data_schema.sch_utilities as utils
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers


def renewal_expiring(): return {
    "expiring": hx.Float(mode="output", async_output=["expiring_policy_fetch_task"], view={"label": "Expiring", "format": thousands_format()}),
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
    
    cds.override_node_properties(
        "cds/layers/rate_change/expiring_layer", 
        {  
            "async_input": ["expiring_policy_fetch_task", "rarc_task"],
            "options": [*range(1,max_layers+1)]
        } 
    )

    cds.extend_node_rater_defined("cds", {
        "rate_change": hx.Structure(children = {
            "rate_change_validation": hx.Bool(mode="output"),
            "risk_adjusted_rate_change": hx.Float(mode="output", view={"format": utils.percent_format(1)}),
            "risk_xl_exposure_selection": hx.Str(mode="input", default = "ROEV", options = ["ROEV", "BPI"], async_input=["rate_change_task"], view={"label": 'Exposure Selection'}),
            "comments": hx.Str(mode="input", default = None, optionality="optional", view={"label": 'Comments'}),
            **{f"show_layer_{index}": hx.Bool(mode="output", view={"format":utils.thousands_format(0)}) 
                    for index in range(1, max_layers + 1)}
        })
    })

    cds.extend_node_rater_defined("cds/layers/rate_change", {
        "exposure_change_fixed": hx.Structure(view={"label": "Exposure Change"}, children={
            "model_calculated": hx.Float(mode="input", default = None, optionality="optional", view={"label": "Exposure \n Model Factor", "format": utils.percent_format(1), "read_only": True}),
            "uw_selected": hx.Float(mode="input", default=None, optionality="optional", async_input=["rate_change_task"], validation={"min_value": 0, "max_value": 100}, view={"label": "Exposure \n UW Selected %", "format": utils.percent_format(1)}),
            "final": hx.Float(mode="output", view={"label": "Exposure Change", "format": utils.percent_format(1)}),
            "comment": hx.Str(mode="output",optionality="optional"),
        }),
        "limit_change_fixed": hx.Structure(view={"label": "Limit Change"}, children={
            "model_calculated": hx.Float(mode="input", default = None, optionality="optional", view={"label": "Limits & Retentions \n Model Factor", "format": utils.percent_format(1), "read_only": True}),
            "uw_selected": hx.Float(mode="input", default=None, optionality="optional", async_input=["rate_change_task"], validation={"min_value": 0, "max_value": 100}, view={"label": "Limits & Retentions \n UW Selected %", "format": utils.percent_format(1)}),
            "final": hx.Float(mode="output", view={"label": "Limits & Retentions Change", "format": utils.percent_format(1)}),
            "comment": hx.Str(mode="output",optionality="optional"),
        }),
        "other_change_fixed": hx.Structure(view={"label": "Other Change (incl. Brokerage)"}, children={
            "uw_selected": hx.Float(mode="input", default=None, optionality="optional", async_input=["rate_change_task"], validation={"min_value": 0, "max_value": 100}, view={"label": "Other Change \n UW Selected %", "format": utils.percent_format(1)}),
            "final": hx.Float(mode="output", view={"label": "Other Changer", "format": utils.percent_format(1)}),
        }),
        "terms_conditions_change_fixed": hx.Structure(view={"label": "Terms & Conditions Change"}, children={
            "uw_selected": hx.Float(mode="input", default=None, optionality="optional", async_input=["rate_change_task"], validation={"min_value": 0, "max_value": 100}, view={"label": "T&C \n UW Selected %", "format": utils.percent_format(1)}),
            "final": hx.Float(mode="output", view={"label": "Terms & Conditions Change", "format": utils.percent_format(1)}),
        }),
        "risk_characteristics_change_fixed": hx.Structure(view={"label": "Risk Characteristics Change"}, children={
            "final": hx.Float(mode="output", view={"label": "Risk Characteristics Change", "format": utils.percent_format(1)}),
        }),
        "deductible_change_fixed": hx.Structure(view={"label": "Deductible Change"}, children={
            "final": hx.Float(mode="output", view={"label": "Deductible Change", "format": utils.percent_format(1)}),
        }),
        "risk_adjusted_rate_change_case_priced": hx.Float(mode="input", optionality='optional', default=None, view={"label": "Final Risk Adjusted Rate Change", "format": percent_format(), "options": {"read_only": {"read_only": True}}}),
        
        ## Bespoke
        "expiring_layer_to_use": hx.Int(mode="input", default = 1, async_input=["rate_change_task"], view={"label": 'Expiring layer to use'}),
        "expiring_layer_to_use_ly": hx.Int(mode="input", default=None, optionality="optional", view={"label": 'Expiring layer to use', "read_only": True}),
        "exposure_selection": hx.Str(mode="input", default = "Total", options = ["Total", "Bespoke", "Key Zone", "Premium"] , async_input=["rate_change_task"], view={"label": 'Exposure Selection'}),
        "exposure_increase": hx.Float(mode="output", optionality="optional", async_input=["rate_change_task"], view={"label": 'GU Exposure Change', "format": utils.percent_format(1)}),
        "rebase_factor": hx.Float(mode="output", optionality="optional", async_input=["rate_change_task"], view={"label": 'Rebase Factor', "format": utils.percent_format(1)}),
        "rol_rebased": hx.Float(mode="output", optionality="optional", async_input=["rate_change_task"], view={"label": 'FOT ROL LY Rebased', "format": {"output": "percent", "mantissa": 2}}),
        "rol_ly_to_use": hx.Float(mode="output", optionality="optional", async_input=["rate_change_task"], view={"label": 'FOT ROL LY', "format": {"output": "percent", "mantissa": 2}}),
        "comments": hx.Str(mode="input", default = None, optionality="optional", view={"label": 'Comments'}),
        "rationale_outside_plan": hx.Str(mode="input", default = None, optionality="optional", view={"label": 'Rationale if outside business plan'}),
    })