import hx_data_schema as hx

from algorithms.json_parameter_files.parameters import get_parameters
from libraries.common_data_schema.data_schema.utilities import percent_format, thousands_format

included = get_parameters("included.json")

def sch_admitted_excess_local(cds):
    cds.extend_node_rater_defined("cds",{
        "admitted_excess_local": hx.Structure(
            view={"label": "Excess Rating - Model Specific"},
            children = {
                "is_policy_primary": hx.Bool(mode="output", view={"label": "Is Policy Primary?"}) ,
                "benchmark_term_premium": hx.Structure(view={"label": "Gross Benchmark Term Premium"}, children={
                    "value": hx.Float(mode="output", view={"label": "Value", "format": thousands_format(0)}),
                }),
                "benchmark_term_premium_pre_uw_adj": hx.Structure(view={"label": "Gross Benchmark Term Premium (pre UW Adjustments)"}, children={
                    "value": hx.Float(mode="output", view={"label": "Value", "format": thousands_format(0)}),
                }),
                "technical_term_premium": hx.Structure(view={"label": "Gross Technical Term Premium"}, children={
                    "value": hx.Float(mode="output", view={"label": "Value", "format": thousands_format(0)}),
                }),
                "technical_term_premium_pre_uw_adj": hx.Structure(view={"label": "Gross Technical Term Premium (pre UW Adjustments)"}, children={
                    "value": hx.Float(mode="output", view={"label": "Value", "format": thousands_format(0)}),
                }),
                "bpi": hx.Structure(view={"label": "Gross BPI"}, children={
                    "value": hx.Float(mode="output", view={"label": "Value", "format": percent_format(1)}),
                }),
                "bpi_pre_uw_adj": hx.Structure(view={"label": "Gross BPI (pre UW Adjustments)"}, children={
                    "value": hx.Float(mode="output", view={"label": "Value", "format": percent_format(1)}),
                }),
                "tpi": hx.Structure(view={"label": "Gross TPI"}, children={
                    "value": hx.Float(mode="output", view={"label": "Value", "format": percent_format(1)}),
                }),
                "tpi_pre_uw_adj": hx.Structure(view={"label": "Gross TPI (pre UW Adjustments)"}, children={
                    "value": hx.Float(mode="output", view={"label": "Value", "format": percent_format(1)}),
                }),
            }
        )

        }
    )
def sch_excess_rate_change(cds):
    cds.extend_node_rater_defined("cds", {
        "excess_rate_change": hx.Structure(children={
            "show_hide_excess_rc": hx.Bool(mode="output"),
            "comments": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comments"}),

            "exposure": hx.Structure(view={"label": "Exposure"}, children={
                "fte": hx.Structure(view={"label": "FTEs"}, children ={**exposure_rc_details()}),
                "plan_assets": hx.Structure(view={"label": "Plan Assets"}, children ={**exposure_rc_details()}),
                "plan_participants": hx.Structure(view={"label": "Plan Participants"}, children ={**exposure_rc_details()}),
                "total_assets": hx.Structure(view={"label": "Total Assets"}, children ={**exposure_rc_details()}),
                "total_rate_change": hx.Structure(view={"label": "Total Exposure"}, children ={
                    "rate_change": hx.Float(mode="output", view={"label": "Rate Change", "format":percent_format(2)})
                })             
            }),
            
            "deductible": hx.Structure(view={"label": "Deductible"}, children={**excess_rc_details()}),
            "limit": hx.Structure(view={"label": "Limit"}, children={**excess_rc_details()}),
            "brokerage": hx.Structure(view={"label": "Brokerage"}, children={
                "expiry": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Expiring", "format":percent_format(2)}),
                "renewal": hx.Float(mode="output", view={"label": "Renewal", "format":percent_format(2)}),
                "rate_change": hx.Float(mode="output", view={"label": "Rate Change", "format":percent_format(2)})
                }),
            "risk_char": hx.Structure(view={"label": "Risk Characteristics"}, children={"rate_change": hx.Float(mode="input", default=1, view={"label": "Rate Change", "format":percent_format(2)})}),
            "terms_and_conditions": hx.Structure(view={"label": "Terms and Conditions"}, children={"rate_change": hx.Float(mode="input", default=1, view={"label": "Rate Change", "format":percent_format(2)})}),
            "annualized_expiring_prem": hx.Structure(view={"label": "Annualized Expiring Premium"}, children={"rate_change": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Rate Change", "format":thousands_format()})}),
            "expected_new_prem": hx.Structure(view={"label": "Expected New Premium"}, children={"rate_change": hx.Float(mode="output", view={"label": "Rate Change", "format":thousands_format()})}),
            "new_prem": hx.Structure(view={"label": "New Premium"}, children={"rate_change": hx.Float(mode="output", view={"label": "Rate Change", "format":thousands_format()})}),
            "final_rc": hx.Structure(view={"label": "Final Rate Change"}, children={"rate_change": hx.Float(mode="output", view={"label": "Rate Change", "format":percent_format(2)})}),
        })
    })

def excess_rc_details():
    return{
        "expiry": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Expiring", "format":thousands_format()}),
        "renewal": hx.Float(mode="output", view={"label": "Renewal", "format":thousands_format()}),
        "rate_change": hx.Float(mode="output", view={"label": "Rate Change", "format":percent_format(2)})
    }

def exposure_rc_details():
    return{
        "expiry": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Expiring", "format":thousands_format()}),
        "renewal": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Renewal", "format":thousands_format()}),
        "rate_change": hx.Float(mode="output", view={"label": "Rate Change", "format":percent_format(2)}),
        "weights": hx.Float(mode="input", default=(1/4), optionality="optional", view={"label": "Weight", "format":percent_format(2)}),
    }