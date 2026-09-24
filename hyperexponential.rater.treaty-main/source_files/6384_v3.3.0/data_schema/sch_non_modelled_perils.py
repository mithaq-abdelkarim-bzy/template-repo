import hx_data_schema as hx
import data_schema.sch_utilities as utils
from hx import params as hx_params
from algorithms.rate_constants import max_curves, peril_label, peril_reference


def sch_non_modelled_perils(cds):

    # Setup each NMP curve section: dropdowns for peril, include in summary etc, and structures for the chosen PMLs
    cds.extend_node_rater_defined("cds",
     {
        "non_modelled_perils": hx.List(mode="input", default_element_count=max_curves, view={"label": "Layers"}, children={
            "curve_selections": hx.Structure(children={
                "include_in_summary": hx.Bool(mode="input",default = True, view={"label": "Include in Summary?"}),
                "broker_pml": hx.Bool(mode="input", default = True, view={"label": "Use Broker PML?"}),
                "peril": hx.Str(mode="input", default="AP", options_column="peril_label", options_table="table_peril_name", view={"label": "Peril"}),
                "description": hx.Str(mode="input", default="", optionality = "optional", view={"label": "Methodology description"}),
                "currency": hx.Str(mode="input", default=None, optionality="optional", options_table="table_currency", options_column="currency", view={"label": "Currency"}),
                "curve": hx.Str(mode="input", default=None, optionality = "optional", options_table="table_nmp_curve_names", options_column="curve", view={"label": "Curve"}),
                "rp": hx.Int(mode="input",default=None, optionality="optional", validation={"min_value": 2}, view={"label": "RP", "format": utils.thousands_format(0)}),
                "loss": hx.Float(mode="input",default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Loss", "format": utils.thousands_format(0)}),
                "show_market_pml": hx.Bool(mode="output"),
                "pml_broker_label": hx.Str(mode="output", optionality="optional"),
                "pml_market_label": hx.Str(mode="output", optionality="optional")               
            }),
            "rp_labels": hx.Structure( view={"label": "Return Period"}, children={
                **{f"rp_{item}": hx.Int(mode="input", default=label, optionality="optional", view={"format":utils.thousands_format(0), "read_only":True}) 
                    for item,label in zip(hx_params.table_return_periods["return_period"],hx_params.table_return_periods["return_period"])},
                    }),
            "pml_broker": hx.Structure(view={"label": "PML - Broker"}, children={
                **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"format":utils.thousands_format(0)}) 
                    for item,label in zip(hx_params.table_return_periods["return_period"],hx_params.table_return_periods["return_period"])},
                    }),
            "pml_market": hx.Structure(view={"label": "PML Market"}, children={
                **{f"rp_{item}": hx.Float(mode="output", optionality="optional", view={"format":utils.thousands_format(0)}) 
                    for item,label in zip(hx_params.table_return_periods["return_period"],hx_params.table_return_periods["return_period"])},
                    }),  
            "pml_final": hx.Structure(view={"label": "PML Final"}, children={
                **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", view={"format":utils.thousands_format(0), "read_only":True}) 
                    for item,label in zip(hx_params.table_return_periods["return_period"],hx_params.table_return_periods["return_period"])},
                    }),                 
        }),
    })

    # This section enables the underwriter to select how many curves they want to view in the NMP tab
    cds.extend_node_rater_defined("cds",
     {
             "non_modelled_perils_visual": hx.Structure( view={"label": "NMP Visual"}, children={
                "us_wf_information": hx.Str(mode="input", default = """NB: For US Accounts, WF EL calculated below will be used to calculate WF RI Cost.""", view={"read_only": True}),
                "information": hx.Str(mode="input", default = """NB: NMP methodology uses the PML curve therefore assuming a maximum of one event per year. \n \nThis approximation works well for higher layers but please note potential under-estimation of EL on lower layers with higher frequency expected.""", view={"read_only": True}),
                "curve_number": hx.Int(mode="input",default = 1, options_table = "table_nmp_curve_count",options_column = "count", view={"label": "Number of Curves", "format": utils.thousands_format(0)}),
                **{f"show_curve_{index}": hx.Bool(mode="output", view={"format":utils.thousands_format(0)}) 
                    for index in range(1,max_curves+1)},
                    }),
    })

    ## Add in layer results for each NMP curve
    cds.extend_node_rater_defined("cds/layers",
     { 
        "nmp": hx.Structure( children={
            **{f"non_modelled_perils_{index}": hx.Structure(view={"label": "NMP"}, children={
                "gross_el": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Gross EL", "format": utils.thousands_format(0), "read_only":True}),
                "loss_on_line": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Gross LoL",  "format": utils.percent_format(1), "read_only":True}),
                "gross_sd": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Gross SD", "format": utils.thousands_format(0), "read_only":True}),           
                "include_curve": hx.Bool(mode="input", default=True, view={"label":f"Include Curve"})       
                }) for index in range (1,max_curves+1) },
            "non_modelled_perils_total": hx.Structure(view={"label": "NMP Total"}, children={
                "gross_el": hx.Float(mode="output", optionality="optional", view={"label": "Gross EL", "format": utils.thousands_format(0)}),
                "loss_on_line": hx.Float(mode="output", optionality="optional", view={"label": "Gross LoL",  "format": utils.percent_format(1)}),
                "gross_sd": hx.Float(mode="output", optionality="optional", view={"label": "Gross SD", "format": utils.thousands_format(0)}),
                "gross_el_uw": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Gross EL UW Override", "format": utils.thousands_format(0)}),
                "gross_sd_uw": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Gross SD UW Override", "format": utils.thousands_format(0)}),
                "peril_el": hx.Structure(children={
                    **{f"el_{item}": hx.Float(mode="output", optionality = "optional") 
                        for item in [x for x in peril_reference if x != "ap"]}
                })  
            })
        })
    })