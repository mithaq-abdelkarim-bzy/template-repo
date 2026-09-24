import hx_data_schema as hx
import data_schema.sch_utilities as utils
from hx import params as hx_params

def sch_pml_curves(cds):
    cds.extend_node_rater_defined("cds",
     {
        "pml_curves": hx.Structure(children={
            "comments": hx.Str(mode="input",default="", optionality="optional", view={"label": "PML Comments"}),
            "information": hx.Str(mode="input", default = """NB: Selecting curves here will allow the underwriter to allocate RMS EL by peril in the Modelling tab (after pressing 'Run RMS EL Allocation Task'). \n \n By allocating RMS EL to each selected peril, we can accurately calculate the RI cost component of technical premium.""", view={"read_only": True}),
            **{f"{curve_type}": hx.List(mode = "input",default_element_count=6, max_element_count = 50, children={
                    "include_in_peril_alloc": hx.Str(mode="input",default = "Yes", options = ["Yes","No"], view={"label": "Include in Peril Alloc.?"}),
                    "peril": hx.Str(mode="input", default="AP",  options_column="peril_label", options_table="table_peril_name", view={"label": "Peril"}),
                    "curve_description": hx.Str(mode="input", default="", optionality="optional", view={"label": "Curve Description"}),
                    "currency": hx.Str(mode="input", default=None, optionality="optional", options_table="table_currency", options_column="currency", view={"label": "Currency"}),
                    "rp_loss": hx.Structure( view={"label": "Return Period"}, children={
                        **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": f"{label}","format":utils.thousands_format(0)}) 
                            for item,label in zip(hx_params.table_return_periods["return_period"],hx_params.table_return_periods["return_period_label"])
                        },
                    }),
                    **{f"{rp_item}": hx.Structure(view={"label": "Return Period"}, children={
                        **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", view={"label": f"{label}", "format":utils.thousands_format(0), "read_only": True}) 
                            for item,label in zip(hx_params.table_return_periods["return_period"],hx_params.table_return_periods["return_period_label"])
                        },
                        }) for rp_item in ["rp_loss_prev"]
                    },
                    **{f"{rp_item}": hx.Structure( view={"label": "Return Period"}, children={
                        **{f"rp_{item}": hx.Float(mode="output", optionality="optional", view={"label": f"{label}", "format": utils.percent_format(1)}) 
                            for item,label in zip(hx_params.table_return_periods["return_period"],hx_params.table_return_periods["return_period_label"])
                        },
                        }) for rp_item in ["rp_loss_change"]
                    },
                }) for curve_type, curve_label in zip(["rms_curves", "air_curves", "other_curves"], ["RMS Curves", "AIR Curves", "Other Curves"])
            },  
            **{f"{curve_type}": hx.List(mode = "input",default_element_count=1, max_element_count = 50, children={
                    "include_in_peril_alloc": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Include in Peril Allocation?", "read_only": True}),
                    "peril": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Peril", "read_only": True}),
                    "curve_description": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Curve Description", "read_only": True}),
                    "currency": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Currency", "read_only": True}),
                    "rp_loss": hx.Structure( view={"label": "Return Period"}, children={
                        **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", view={"label": f"{label}","format":utils.thousands_format(0), "read_only": True}) 
                            for item,label in zip(hx_params.table_return_periods["return_period"],hx_params.table_return_periods["return_period_label"])
                        },
                    }),
                    **{f"{rp_item}": hx.Structure(view={"label": "Return Period"}, children={
                        **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", view={"label": f"{label}", "format":utils.thousands_format(0), "read_only": True}) 
                            for item,label in zip(hx_params.table_return_periods["return_period"],hx_params.table_return_periods["return_period_label"])
                        },
                        }) for rp_item in ["rp_loss_prev"]
                    },
                    **{f"{rp_item}": hx.Structure( view={"label": "Return Period"}, children={
                        **{f"rp_{item}": hx.Float(mode="output", optionality="optional", view={"label": f"{label}", "format":utils.percent_format(1)}) 
                            for item,label in zip(hx_params.table_return_periods["return_period"],hx_params.table_return_periods["return_period_label"])
                        },
                        }) for rp_item in ["rp_loss_change"]
                    },
                }) for curve_type, curve_label in zip(["nmp_curves"], ["NMP Curves"])
            },
            "curve_aggregator": hx.Structure(view={"label": "Aggregated Curve"},children= { 
                "include_in_peril_alloc": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Include in Peril Alloc.?", "read_only": True}),
                "peril": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Peril", "read_only": True}),
                "curve_description": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Curve Description", "read_only": True}),
                "currency": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Currency", "read_only": True}),
                "rp_loss": hx.Structure( view={"label": "Return Period"}, children={
                    **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", view={"label": f"{label}","format":utils.thousands_format(0), "read_only": True}) 
                        for item, label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])
                    },
                }),
                **{f"{rp_item}": hx.Structure(view={"label": "Return Period"}, children={
                    **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", view={"label": f"{label}", "format":utils.thousands_format(0), "read_only": True}) 
                        for item, label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])
                    },
                    }) for rp_item in ["rp_loss_prev"]
                },
                **{f"{rp_item}": hx.Structure( view={"label": "Return Period"}, children={
                    **{f"rp_{item}": hx.Float(mode="output", optionality="optional", view={"label": f"{label}", "format":utils.percent_format(1)}) 
                        for item, label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])
                    },
                    }) for rp_item in ["rp_loss_change"]
                },
            }),
            "burn_curve": hx.Structure(view={"label": "Burn Curve"},children= { 
                "include_in_peril_alloc": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Include in Peril Alloc.?", "read_only": True}),
                "peril": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Peril", "read_only": True}),
                "curve_description": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Curve Description", "read_only": True}),
                "currency": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Currency", "read_only": True}),
                "rp_loss": hx.Structure( view={"label": "Return Period"}, children={
                    **{f"rp_{item}": hx.Float(mode="output", optionality="optional", view={"label": f"{label}","format":utils.thousands_format(0)}) 
                        for item, label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])
                    },
                }),
                **{f"{rp_item}": hx.Structure(view={"label": "Return Period"}, children={
                    **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", view={"label": f"{label}", "format":utils.thousands_format(0), "read_only": True}) 
                        for item, label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])
                    },
                    }) for rp_item in ["rp_loss_prev"]
                },
                **{f"{rp_item}": hx.Structure( view={"label": "Return Period"}, children={
                    **{f"rp_{item}": hx.Float(mode="output", optionality="optional", view={"label": f"{label}", "format":utils.percent_format(1)}) 
                        for item, label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])
                    },
                    }) for rp_item in ["rp_loss_change"]
                },
            }),
        }),
    })