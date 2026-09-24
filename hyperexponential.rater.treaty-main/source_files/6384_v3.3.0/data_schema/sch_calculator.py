import hx_data_schema as hx
import data_schema.sch_utilities as utils
from hx import params as hx_params

def sch_calculator(cds):
    cds.extend_node_rater_defined("cds",
     {
        "calculator": hx.Structure(children={
            "input_list": hx.List(mode = "input", children={
                "el": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, view={"label": "EL", "format": utils.thousands_format(0)}),
                "sd": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, view={"label": "SD", "format": utils.thousands_format(0)})
            }),
            "results": hx.Structure( view={"label": "Aggregated"}, children={
                "el": hx.Float(mode="output", optionality="optional", view={"label": "Aggregated EL", "format": utils.thousands_format(0)}),
                "sd": hx.Float(mode="output", optionality="optional", view={"label": "Aggregated SD", "format": utils.thousands_format(0)})
            }),
            "transposer": hx.List(mode = "input", children={
                "el": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, view={"label": "EL", "format": utils.thousands_format(0), "options": {"read_only_option": {"read_only": True}}}),
                "sd": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, view={"label": "SD", "format": utils.thousands_format(0), "options": {"read_only_option": {"read_only": True}}})
            }),
        }),
    })