import hx_data_schema as hx
import data_schema.sch_utilities as utils
from hx import params as hx_params

def sch_curve_aggregator(cds):
    cds.extend_node_rater_defined("cds",
     {
        "curve_aggregator": hx.Structure(children={
            "aggregator_output": hx.Structure(children={
                "rp_labels": hx.Structure( view={"label": "Return Period"}, children={
                    **{f"rp_{item}": hx.Int(mode="input", default=label, optionality="optional", view={"format":utils.thousands_format(0),"read_only":True}) 
                        for item,label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period"])},
                    }),
                "rp_loss": hx.Structure( view={"label": "Loss"}, children={
                    **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": f"{label}","format":utils.thousands_format(0)}) 
                        for item,label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])
                    },
                }),
            }),
            "pml_selections": hx.List(mode = "input",default_element_count=6, children={
                "include_in_aggregator": hx.Bool(mode="input",default=True, view={"label": "Include in Curve Aggregator?"}),
                "weight": hx.Float(mode="input", default=1, optionality="optional", validation={"min_value": 0, "max_value": 1}, view={"label": "Weight", "format": {"output": "percent", "mantissa": 0}}),
                "name": hx.Str(mode="input", default="", optionality="optional", view={"label": "Curve Name"}),
                "rp_loss": hx.Structure( view={"label": "Return Period"}, children={
                    **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": f"{label}","format":utils.thousands_format(0)}) 
                        for item,label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])
                    },
                }),
            }) 
        }),            
    })