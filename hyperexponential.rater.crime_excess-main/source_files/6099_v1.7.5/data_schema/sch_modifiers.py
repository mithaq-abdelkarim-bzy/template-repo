import hx_data_schema as hx
import data_schema.utilities as utils
import algorithms.utils_global_lists as lst
from algorithms.utils_functions import create_title

def sch_modifiers(cds):
    cds.extend_node_rater_defined("cds", {
        # Modifiers
        **{
            loop_vbl: hx.Structure(view={"label": create_title(loop_vbl)}, children={
                "available": hx.Bool(mode="output"),
                "minimum_state": hx.Float(mode="output", view={"label": "Max Credit", "format":utils.percent_format(0)}),
                "maximum_state": hx.Float(mode="output", view={"label": "Max Debit", "format":utils.percent_format(0)}),
                "selected": hx.Float(mode="input", default=0, view={"label": "Selected", "format":{"output":"percent", "mantissa":1}}),
                "comment": hx.Str(mode="input", default="", view={"label": "Comment"}),
                "minimum_plan": hx.Float(mode="output", view={"label": "Max Credit Rate Plan", "format":utils.percent_format(0)}),
                "maximum_plan": hx.Float(mode="output", view={"label": "Max Debit Rate Plan", "format":utils.percent_format(0)}),
            })
            for loop_vbl in ["classification_peculiarities", "management", "personnel", "location", "response_to_losses", "endorsements","expense_modification"]
        },
       "total_modifiers": hx.Structure(view={"label": "Total Modifiers"}, children={
            "minimum_state": hx.Float(mode="output", view={"label": "Max Credit", "format":utils.percent_format(0)}),
            "maximum_state": hx.Float(mode="output", view={"label": "Max Debit", "format":utils.percent_format(0)}),
            "selected": hx.Float(mode="output", view={"label": "Selected", "format":{"output":"percent", "mantissa":1}})
        }),
        "total_unbounded": hx.Float(mode="output", view={"label": "Total Unbounded", "format":utils.percent_format(0)}),
        "mod_factor": hx.Float(mode="output", view={"label": "Factor"}),
        "eligibility_min_before": hx.Float(mode="output", view={"label": "Eligibility Requirement (Before)", "format":utils.thousands_format(0)}),
        "eligibility_min_after": hx.Float(mode="output", view={"label": "Eligibility Requirement (After)", "format":utils.thousands_format(0)}),
        "expense_mod_factor": hx.Float(mode="output", view={"label": "Expense Modification Factor"}),
        "expense_mod_flag": hx.Bool(mode="output"),
        # For surplus or LRE only
        "surplus_deviation_factor": hx.Float(mode="input", default=1, view={"label": "Surplus Deviation", "format":utils.integer_format(3)})
    })

