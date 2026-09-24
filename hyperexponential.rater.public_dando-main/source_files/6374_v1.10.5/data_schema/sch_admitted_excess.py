import hx_data_schema as hx
from data_schema.sch_utilities import percent_format, thousands_format
import algorithms.rate_constants as const

def sch_admitted_excess(cds):
    cds.extend_node_rater_defined("cds",
    {
        "admitted_excess": hx.Structure(
            view={"label": "Excess Rating"},
            children = {
            # Show by conditions
            "conditions_met": hx.Bool(mode="output", view={"label": "None"}),
            "is_primary_excess": hx.Str(mode="input", default="Primary", optionality="optional", options=["Primary", "Excess"], view={"label": "Primary or Excess Rating"}),

            #Excess Inputs and Outputs Table
            "exc_prim_limit": hx.Structure( view={"label": "Primary Limit"}, children = {
                "value": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Value", "format": thousands_format(0)}),
            }),
            "exc_prim_retention": hx.Structure( view={"label": "Primary Retention"}, children = {
                "value": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Value", "format": thousands_format(0)}),
            }),
            "exc_prim_premium": hx.Structure( view={"label": "Primary Premium"}, children = {
                "value": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Value", "format": thousands_format(0)}),
            }),
            "exc_excess_limit": hx.Structure( view={"label": "Excess Limit"}, children = {
                "value": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Value", "format": thousands_format(0)}),
            }),
            "exc_excess_attach": hx.Structure( view={"label": "Excess Attachment Point"}, children = {
                "value": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Value", "format": thousands_format(0)}),
            }),
            "exc_no_policies": hx.Structure( view={"label": "No of policies sharing single limit"}, children = {
                "value": hx.Float(mode="input", default=1, optionality="optional", options=[1,2,3,4,5,6], view={"label": "Value", "format": thousands_format(0)}),
            }),

            # Admitted Excess Inputs and Outputs
            "exc_prim_rate_ade": hx.Structure( view={"label": "Primary Rate Adequacy Correction"}, children = {
                "value": hx.Float(mode="input", default=1, optionality="optional", view={"label": "Value", "format": {"mantissa": 4}}),
                "min": hx.Float(mode="output",view={"label": "Min"}),
                "max": hx.Float(mode="output",view={"label": "Max"}),
            }),
            "exc_large_loss": hx.Structure( view={"label": "Large Loss Potential"}, children = {
                "value": hx.Str(mode="input", default="Average", optionality="optional", options=["Above Average","Average", "Below Average"], view={"label": "Value"}),
            }),
            "exc_ind_risk_level": hx.Structure( view={"label": "Industry/Sector Risk Level"}, children = {
                "value": hx.Str(mode="input", default="Normal Risk", optionality="optional", options=["Low Risk","Normal Risk", "High Risk"], view={"label": "Value"}),
            }),
            "exc_ind_sec_factor": hx.Structure( view={"label": "Industry/Sector Factor"}, children = {
                "value": hx.Float(mode="input", default=1, optionality="optional", view={"label": "Value", "format": {"mantissa": 4}}),
                "min": hx.Float(mode="output",view={"label": "Min"}),
                "max": hx.Float(mode="output",view={"label": "Max"}),
            }),
            "exc_comp_spe_risk_level": hx.Structure( view={"label": "Company Specific Risk Level"}, children = {
                "value": hx.Str(mode="input", default="Normal Risk", optionality="optional", options=["Low Risk","Normal Risk", "High Risk"], view={"label": "Value"}),
            }),
            "exc_comp_spe_factor": hx.Structure( view={"label": "Company Specific Factor"}, children = {
                "value": hx.Float(mode="input", default=1, optionality="optional", view={"label": "Value", "format": {"mantissa": 4}}),
                "min": hx.Float(mode="output",view={"label": "Min"}),
                "max": hx.Float(mode="output",view={"label": "Max"}),
            }),
            "exc_liti_potential_risk_level": hx.Structure( view={"label": "Litigation Potential Risk Level"}, children = {
                "value": hx.Str(mode="input", default="Normal Risk", optionality="optional", options=["Low Risk","Normal Risk", "High Risk"], view={"label": "Value"}),
            }),
            "exc_liti_potential_factor": hx.Structure( view={"label": "Litigation Potential Factor"}, children = {
                "value": hx.Float(mode="input", default=1, optionality="optional", view={"label": "Value", "format": {"mantissa": 4}}),
                "min": hx.Float(mode="output",view={"label": "Min"}),
                "max": hx.Float(mode="output",view={"label": "Max"}),
            }),
            "exc_fl_schedule_rating_factor": hx.Structure( view={"label": "FL Schedule Rating Factor"}, children = {
                "value": hx.Float(mode="input", default=1, optionality="optional", view={"label": "Value", "format": {"mantissa": 4}}),
                "min": hx.Float(mode="output",view={"label": "Min"}),
                "max": hx.Float(mode="output",view={"label": "Max"}),
            }),
            "adm_exc_model_prem": hx.Structure( view={"label": "Model Premium"}, children = {
                "value": hx.Float(mode="output", view={"label": "Model Premium", "format": thousands_format(0)}),
            }),
            "adm_exc_max_round_down": hx.Structure( view={"label": "Max Round Down"}, children = {
                "value": hx.Float(mode="output", view={"label": "Max Round Down", "format": thousands_format(0)}),
            }),
            "adm_exc_max_round_up": hx.Structure( view={"label": "Max Round Up"}, children = {
                "value": hx.Float(mode="output", view={"label": "Max Round Up", "format": thousands_format(0)}),
            }),
            "adm_exc_round_prem": hx.Structure( view={"label": "Rounded Premium"}, children = {
                "value": hx.Float(mode="override", view={"label": "Value", "format": thousands_format(0)}),
            }),
        })
        }
    )