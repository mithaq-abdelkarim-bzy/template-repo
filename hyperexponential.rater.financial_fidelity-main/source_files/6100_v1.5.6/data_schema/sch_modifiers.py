import hx_data_schema as hx
import libraries.common_data_schema.data_schema.utilities as utils
import algorithms.utils_global_lists as lst
from algorithms.utils_functions import create_title

def sch_modifiers(cds):
    cds.extend_node_rater_defined("cds/layers", {
        # Modifiers
        **{
            loop_vbl: hx.Structure(view={"label": create_title(loop_vbl)}, children={
                "minimum": hx.Float(mode="output", view={"label": "Minimum", "format":utils.percent_format(0)}),
                "maximum": hx.Float(mode="output", view={"label": "Maximum", "format":utils.percent_format(0)}),
                "uw_selected": hx.Float(mode="input", default=0, view={"label": "Selected", "format":{"output":"percent", "mantissa":1}}),
                "prior_modifier": hx.Float(mode="input", default=0, view={"label": "Prior Selected", "format":{"output":"percent", "mantissa":1}}),
                "comment": hx.Str(mode="input", default="", view={"label": "Comment"}),
            })
            for loop_vbl in ["audit_procedures","internal_controls","management_and_personnel","classification_peculiarities"]
        },
        "total_modifiers": hx.Structure(view={"label": "Total Modifiers"}, children={
            "minimum": hx.Float(mode="output", view={"label": "Minimum", "format":utils.percent_format(0)}),
            "maximum": hx.Float(mode="output", view={"label": "Maximum", "format":utils.percent_format(0)}),
            "uw_selected": hx.Float(mode="output", view={"label": "Schedule Rating", "format":{"output":"percent", "mantissa":1}}),
            "prior_modifier": hx.Float(mode="output", view={"label": "Prior Selected", "format":{"output":"percent", "mantissa":1}}),
        }),
        "modifier_label": hx.Str(mode="output"),
        "modifier_flag": hx.Bool(mode="output"),
        "total_label": hx.Str(mode="output"),

        "a_rating_dev_factor": hx.Float(mode="input", default=1, view={"label": "(a) Rating Deviation Factor", "format":utils.integer_format(3)}),
    })
