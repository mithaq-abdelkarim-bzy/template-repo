import hx_data_schema as hx
import data_schema.sch_utilities as utils
from algorithms.rate_constants import max_layers

def sch_bi_data(cds):

    cds.extend_node_rater_defined("cds", {
        "bi_data": hx.Structure(children={
            "profit": hx.Float(mode="output", optionality="optional", view={"label": "Profit", "format": utils.thousands_format(0)}),
            "ilr": hx.Float(mode="output", optionality="optional", view={"label": "Incurred LR", "format": {"output": "percent", "mantissa": 1}}),
            "break_even": hx.Str(mode="output", optionality="optional", view={"label": "Break Even"}),
            "graph_list": hx.List(mode = "output", children= {
                "yoa": hx.Float(mode="output", optionality="optional", view={"label": "Year", "format": utils.thousands_format(0)}),
                "exposure": hx.Float(mode="output", optionality="optional", view={"label": "Exposure", "format": utils.thousands_format(0)}),
                "wep": hx.Float(mode="output", optionality="optional", view={"label": "WEP", "format": {"output": "percent", "mantissa": 1}}),
                "incurred": hx.Float(mode="output", optionality="optional", view={"label": "Incurred", "format": {"output": "percent", "mantissa": 1}}),
                "elr": hx.Float(mode="output", optionality="optional", view={"label": "ELR", "format": {"output": "percent", "mantissa": 1}}),
                "cumulative_rate_change": hx.Float(mode="output", optionality="optional", view={"label": "Rate Change", "format": {"output": "percent", "mantissa": 1}}), 
            })         
        }),
    })
