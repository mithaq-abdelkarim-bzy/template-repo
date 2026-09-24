import hx_data_schema as hx
from hx import params as hx_params
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
import data_schema.sch_utilities as utils
from algorithms.rate_constants import peril_label, peril_reference

def sch_peril_allocation(cds):
    cds.extend_node_rater_defined("cds", {
        "peril_allocation_account_level": hx.Structure(children={
            "include_ivor": hx.Str(mode="input", default="No", options=["Yes", "No"], view={"label": "Include IVOR in allocation?"}),
            "allocation_methodology": hx.Str(mode="input", default="PML", options=["PML", "AAL"], view={"label": "RMS / AIR Allocation Methodology"}),
            "skip_peril_allocation": hx.Bool(mode="input", default=False, view={"label": "Skip Peril Allocation"})
        })
    })

    cds.extend_node_rater_defined("cds/layers", {
        "peril_allocation": hx.Structure(children={
            "final_proportions": hx.Structure(children={
                **{f"el_{item}": hx.Float(mode="input", default = None, optionality="optional", view={"label": f"{label}","format": {"output": "percent", "mantissa": 1}, "read_only": True}) 
                    for item, label in zip([x for x in peril_reference if x != "ap"], [x for x in peril_label if x != "AP"])}
            }),
            "rms_el_approx": hx.Structure(children={
                **{f"el_{item}": hx.Float(mode="input", default = None, optionality="optional", view={"label": f"{label}","format":utils.thousands_format(0), "read_only": True}) 
                    for item, label in zip([x for x in peril_reference if x != "ap"], ["RMS " + x + " PML Approx." for x in peril_label if x != "AP"])}
            }),
            "air_el_approx": hx.Structure(children={
                **{f"el_{item}": hx.Float(mode="input", default = None, optionality="optional", view={"label": f"{label}","format":utils.thousands_format(0), "read_only": True}) 
                    for item, label in zip([x for x in peril_reference if x != "ap"], ["AIR " + x + " PML Approx." for x in peril_label if x != "AP"])}
            }),
            "rms_aal": hx.Structure(children={
                **{f"el_{item}": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, view={"label": f"{label}","format":utils.thousands_format(0)}) 
                    for item, label in zip([x for x in peril_reference if x != "ap"], ["RMS " + x + " AAL" for x in peril_label if x != "AP"])}
            }),
            "air_aal": hx.Structure(children={
                **{f"el_{item}": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, view={"label": f"{label}","format":utils.thousands_format(0)}) 
                    for item, label in zip([x for x in peril_reference if x != "ap"], ["AIR " + x + " AAL" for x in peril_label if x != "AP"])}
            }),
            "ivor_aal": hx.Structure(children={
                **{f"el_{item}": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, view={"label": f"{label}","format":utils.thousands_format(0)}) 
                    for item, label in zip([x for x in peril_reference if x != "ap"], ["IVOR " + x + " AAL" for x in peril_label if x != "AP"])}
            }),
            ### simulation table
            "simulation_perc": hx.Structure(children={
                **{f"gross_table_{i}": hx.Float(mode="input", default = None, optionality="optional", async_output=["run_simulation_task"], view = {"label": f"Table {i + 1}", "format": utils.percent_format(1), "read_only": True})
                for i in range(8)}
            }),
            "simulation_dollar": hx.Structure(children={
                **{f"gross_table_{i}": hx.Float(mode="input", default = None, optionality="optional", async_output=["run_simulation_task"], view = {"label": f"Table {i + 1}", "format": utils.thousands_format(0), "read_only": True})
                for i in range(8)}
            }),
            "simulation_std_dollar": hx.Structure(children={
                **{f"gross_table_{i}": hx.Float(mode="input", default = None, optionality="optional", async_output=["run_simulation_task"], view = {"label": f"Table {i + 1}", "format": utils.thousands_format(0), "read_only": True})
                for i in range(8)}
            })    
        }),
    })


