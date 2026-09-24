import hx_data_schema as hx
import data_schema.sch_utilities as utils
from hx import params as hx_params
from algorithms.rate_constants import max_layers

def sch_simulation(cds):

    # Add table coverages node, by layer select which perils are included
    cds.extend_node_rater_defined("cds/layers",
     { "simulation": hx.Structure(children={
            "run_layer": hx.Bool(mode="input", default=True, async_input=["run_simulation_task"], view={"label": f"Run Layer?"}),
            "include_combined_layer_1": hx.Bool(mode="input", default=False, async_input=["run_simulation_task"], view={"label": f"Include in Combined Layer 1?"}),
            "include_combined_layer_2": hx.Bool(mode="input", default=False, async_input=["run_simulation_task"], view={"label": f"Include in Combined Layer 2?"}),
            "sim_coverage": hx.Structure(children={
                **{f"coverage_{i}": hx.Bool(mode="input", default=True, async_input=["run_simulation_task"],  view={"label": f"Table {i}"})
                for i in range(1,9)
                },
            }),
            "sim_result": hx.Structure(children={
                "aal": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task", "start_renewal_task"], view = {"label": "AAL", "format": utils.thousands_format(0), "read_only": True}),
                "subject_loss": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task", "start_renewal_task"], view = {"label": "Subject Loss", "format": utils.thousands_format(0), "read_only": True}),
                "gross_el_pre_inur": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task", "start_renewal_task"], view = {"label": "Gross EL (Pre Inuring)", "format": utils.thousands_format(0), "read_only": True}),
                "gross_sd_pre_inur": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task", "start_renewal_task"], view = {"label": "Gross SD (Pre Inuring)", "format": utils.thousands_format(0), "read_only": True}),
                "gross_el": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task", "start_renewal_task"], view = {"label": "Gross EL", "format": utils.thousands_format(0), "read_only": True, "style_cell": "hx-input"}),
                "gross_sd": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task", "start_renewal_task"], view = {"label": "Gross SD", "format": utils.thousands_format(0), "read_only": True, "style_cell": "hx-input"}),
                "net_el": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task", "start_renewal_task"], view = {"label": "Net EL", "format": utils.thousands_format(0), "read_only": True}),
                "net_sd": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task", "start_renewal_task"], view = {"label": "Net SD", "format": utils.thousands_format(0), "read_only": True}),                     
            })
        })
    })

    cds.extend_node_rater_defined("cds", {
        "simulation": hx.Structure(children={
           "format": hx.Str(mode="input", default = """ELT Columns: [EVENTID, RATE, PERSPVALUE, STDDEVC, STDDEVI, EXPVALUE] \nYLT Columns: [YEAR, EVENTID, LOSS]""", view={"read_only": True}),
           "max_sims": hx.Int(mode="input", default = 50000, optionality="optional", validation={"min_value": 0, "max_value": 500000}, async_input=["run_simulation_task"], view = {"label": "No. Sims"}),
           "sims_lcm": hx.Int(mode="input", default=None, optionality="optional", async_input=["run_simulation_task"], async_output=["file_processing_task"], view = {"label": "No. Sims", "read_only": True}),
           "sims_commentary": hx.Str(mode="input", default=None, optionality="optional", async_input=["run_simulation_task"], async_output=["file_processing_task"], view = {"label": "No. Sims Commentary", "read_only": True}),
           "exposure_increase": hx.Float(mode="input", default = None, optionality="optional", async_input=["run_simulation_task"], view = {"label": "Exposure Increase", "format": {"output": "percent", "mantissa": 1}}),
           "subject_lae": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "Subject LAE", "format": {"output": "percent", "mantissa": 1}}),
           "cut_off": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "Cut Off"}),
           "attritional_sim": hx.Structure(view = {"label": "Log Normal Parameterisation"}, children={
                "mean":  hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "Mean"}),
                "sd":  hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "SD"})
           }),
           "combined_1": hx.Structure(view = {"label": "Combined Layer 1"}, children = {
                "combined_limit": hx.Float(mode="input", default = None, optionality="optional", async_input=["run_simulation_task"], view = {"label": "Combined Limit"}),
                "combined_el": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "Combined EL", "read_only": True}),
                "combined_sd": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "Combined SD", "read_only": True}),
           }),
           "combined_2": hx.Structure(view = {"label": "Combined Layer 2"}, children = {
                "combined_limit": hx.Float(mode="input", default = None, optionality="optional", async_input=["run_simulation_task"], view = {"label": "Combined Limit"}),
                "combined_el": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "Combined EL", "read_only": True}),
                "combined_sd": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "Combined SD", "read_only": True}),
           }),
            "fhcf_1": hx.Structure(view = {"label": "FHCF 1"}, children = {
                "limit": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "Limit", "format": utils.thousands_format(0)}),
                "excess": hx.Float(mode="input", default = None,optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "Excess", "format": utils.thousands_format(0)}),
                "participation": hx.Float(mode="input", default = None,optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "Participation", "format": {"output": "percent", "mantissa": 1}}),
                "lae_cap": hx.Float(mode="input", default = None,optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "LAE Cap", "format": {"output": "percent", "mantissa": 1}}),
                "el": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_simulation_task"], async_output=["run_simulation_task"], view = {"label": "EL", "format": utils.thousands_format(0), "read_only": True}),
                "sd": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_simulation_task"], async_output=["run_simulation_task"], view = {"label": "SD", "format": utils.thousands_format(0), "read_only": True})
           }),
            "fhcf_2": hx.Structure(view = {"label": "FHCF 2"}, children = {
                "limit": hx.Float(mode="input", default = None,optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "Limit", "format": utils.thousands_format(0)}),
                "excess": hx.Float(mode="input", default = None,optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "Excess", "format": utils.thousands_format(0)}),
                "participation": hx.Float(mode="input", default = None,optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "Participation", "format": {"output": "percent", "mantissa": 1}}),
                "lae_cap": hx.Float(mode="input", default = None,optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "LAE Cap", "format": {"output": "percent", "mantissa": 1}}),
                "el": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_simulation_task"], async_output=["run_simulation_task"], view = {"label": "EL", "format": utils.thousands_format(0), "read_only": True}),
                "sd": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_simulation_task"], async_output=["run_simulation_task"], view = {"label": "SD", "format": utils.thousands_format(0), "read_only": True})
           }),
           "inuring_ri": hx.Structure(children = {
                **{f"inur_{i}": hx.Structure(view = {"label": f"Layer {i}"}, children = {
                    "limit": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "Limit", "format": utils.thousands_format(0)}),
                    "excess": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "Excess", "format": utils.thousands_format(0)}),
                    "placed": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "Placed", "format": {"output": "percent", "mantissa": 1}}),
                    "deductible_type": hx.Str(mode="input", default = None, optionality="optional", options = ["Conventional", "Franchise"], async_input=["run_simulation_task"], view = {"label": "Deductible Type"}),
                    "reinstatements": hx.Int(mode="input", default = None, optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "Reinstatements"}),
                    "inur_lae": hx.Float(mode="input", default = None, optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "LAE Cap", "format": {"output": "percent", "mantissa": 1}}),
                }) for i in range(1, 5)
                },
           }),
           "files": hx.Structure(children={
                **{f"input_file_{i}": hx.File(mode="input", file_extension=["csv", "xlsx", "zip"], async_input=["file_processing_task", "run_simulation_task"] , view={"label": "Input File"})
                    for i in range(1,9)
            }}),
            "file_list": hx.List(mode="input", default_element_count = 8, children={
                "file_name": hx.Str(mode="input", default=None, optionality = "optional", async_input=["run_simulation_task"], async_output = ["file_processing_task"], view={"label": "File Name", "read_only": True}),
                "table_type": hx.Str(mode="input", default=None, optionality = "optional", async_input=["run_simulation_task"], async_output = ["file_processing_task"], view={"label": "Table Type", "read_only": True}),
                "max_sims": hx.Int(mode="input", default=None, optionality = "optional", async_input=["run_simulation_task"], async_output = ["file_processing_task"], view={"label": "Max Sims", "read_only": True}),
                "table_el": hx.Float(mode="input", default=None, optionality = "optional", async_input=["run_simulation_task"], async_output = ["file_processing_task"], view={"label": "Table EL", "format": utils.thousands_format(0), "read_only": True}),
                "description": hx.Str(mode="input", default = None, optionality = "optional", async_input=["run_simulation_task"], async_output = ["file_processing_task"], view={"label": "Description", "options": {"read_only_option": {"read_only": True}}}),
                "qualifying_excess": hx.Float(mode="input", default= None, optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "Qualifying Excess", "format": utils.thousands_format(0)}),
                "qualifying_limit": hx.Float(mode="input", default= None, optionality="optional", validation={"min_value": 0}, async_input=["run_simulation_task"], view = {"label": "Qualifying Limit", "format": utils.thousands_format(0)}),
                "fhcf_1": hx.Bool(mode="input", default = False, async_input=["run_simulation_task"], view={"label": "FHCF 1"}),
                "fhcf_2": hx.Bool(mode="input", default = False, async_input=["run_simulation_task"], view={"label": "FHCF 2"}),
                "inur_1": hx.Bool(mode="input", default = False, async_input=["run_simulation_task"], view={"label": "Inur 1"}),
                "inur_2": hx.Bool(mode="input", default = False, async_input=["run_simulation_task"], view={"label": "Inur 2"}),
                "inur_3": hx.Bool(mode="input", default = False, async_input=["run_simulation_task"], view={"label": "Inur 3"}),
                "inur_4": hx.Bool(mode="input", default = False, async_input=["run_simulation_task"], view={"label": "Inur 4"}),
                ## table_curves
                "curve": hx.Structure( view={"label": "PML"}, children={
                    **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": f"{label}","format":utils.thousands_format(0), "read_only": True}, async_output=["run_simulation_task"]) 
                        for item,label in zip(hx_params.table_return_periods["return_period"],hx_params.table_return_periods["return_period_label"])},
                }),
                "curve_aep": hx.Structure( view={"label": "PML"}, children={
                    **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": f"{label}","format":utils.thousands_format(0), "read_only": True}, async_output=["run_simulation_task"]) 
                        for item,label in zip(hx_params.table_return_periods["return_period"],hx_params.table_return_periods["return_period_label"])},
                }),
                "aal": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "AAL", "format": utils.thousands_format(0), "read_only": True}),
            }),
            "pml_comparison": hx.Structure(children={
                "rp_labels": hx.Structure( view={"label": "Return Period"}, children={
                    **{f"rp_{item}": hx.Int(mode="input", default=label, optionality="optional", view={"format":utils.thousands_format(0),"read_only":True}) 
                        for item,label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period"])},
                        "aal": hx.Str(mode="input", default = "AAL", optionality="optional", view = {"label": " ", "read_only": True}),
                }),
                "simulation_gross": hx.Structure( view={"label": "Simulation Pre Inuring"}, children={
                    **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": f"{label}","format":utils.thousands_format(0), "read_only": True}, async_output=["run_simulation_task"]) 
                        for item,label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])},
                        "aal": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "AAL", "format": utils.thousands_format(0), "read_only": True})
                }),
                "simulation_net_inur": hx.Structure( view={"label": "Simulation Net Inuring (Subject Loss)"}, children={
                    **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": f"{label}","format":utils.thousands_format(0), "read_only": True}, async_output=["run_simulation_task"]) 
                        for item,label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])},
                        "aal": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "AAL", "format": utils.thousands_format(0), "read_only": True})
                }),
                "model_gross": hx.Structure( view={"label": "Model Gross"}, children={
                    **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": f"{label}","format":utils.thousands_format(0)}) 
                        for item,label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])},
                        "aal": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "AAL", "format": utils.thousands_format(0), "read_only": True})
                }),
                "model_net_inur": hx.Structure( view={"label": "Model Net Inuring"}, children={
                    **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": f"{label}","format":utils.thousands_format(0)}) 
                        for item,label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])},
                        "aal": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "AAL", "format": utils.thousands_format(0), "read_only": True})
                }),
                "difference_gross": hx.Structure( view={"label": "Gross Difference"}, children={
                    **{f"rp_{item}": hx.Float(mode="output", optionality="optional", view={"label": f"{label}","format":utils.percent_format(0)}) 
                        for item,label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])},
                        "aal": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "AAL", "format": utils.percent_format(0), "read_only": True})
                }),         
                "difference_net_inur": hx.Structure( view={"label": "Net Inuring Difference"}, children={
                    **{f"rp_{item}": hx.Float(mode="output", optionality="optional", view={"label": f"{label}","format":utils.percent_format(0)}) 
                        for item,label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])},
                        "aal": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "AAL", "format": utils.percent_format(0), "read_only": True})
                }),

                "simulation_gross_aep": hx.Structure( view={"label": "Simulation Pre Inuring"}, children={
                    **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": f"{label}","format":utils.thousands_format(0), "read_only": True}, async_output=["run_simulation_task"]) 
                        for item,label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])},
                        "aal": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "AAL", "format": utils.thousands_format(0), "read_only": True})
                }),
                "simulation_net_inur_aep": hx.Structure( view={"label": "Simulation Net Inuring (Subject Loss)"}, children={
                    **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": f"{label}","format":utils.thousands_format(0), "read_only": True}, async_output=["run_simulation_task"]) 
                        for item,label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])},
                        "aal": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "AAL", "format": utils.thousands_format(0), "read_only": True})
                }),
                "model_gross_aep": hx.Structure( view={"label": "Model Gross"}, children={
                    **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": f"{label}","format":utils.thousands_format(0)}) 
                        for item,label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])},
                        "aal": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "AAL", "format": utils.thousands_format(0), "read_only": True})
                }),
                "model_net_inur_aep": hx.Structure( view={"label": "Model Net Inuring"}, children={
                    **{f"rp_{item}": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": f"{label}","format":utils.thousands_format(0)}) 
                        for item,label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])},
                        "aal": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "AAL", "format": utils.thousands_format(0), "read_only": True})
                }),
                "difference_gross_aep": hx.Structure( view={"label": "Gross Difference"}, children={
                    **{f"rp_{item}": hx.Float(mode="output", optionality="optional", view={"label": f"{label}","format":utils.percent_format(0)}) 
                        for item,label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])},
                        "aal": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "AAL", "format": utils.percent_format(0), "read_only": True})
                }),         
                "difference_net_inur_aep": hx.Structure( view={"label": "Net Inuring Difference"}, children={
                    **{f"rp_{item}": hx.Float(mode="output", optionality="optional", view={"label": f"{label}","format":utils.percent_format(0)}) 
                        for item,label in zip(hx_params.table_return_periods["return_period"], hx_params.table_return_periods["return_period_label"])},
                        "aal": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "AAL", "format": utils.percent_format(0), "read_only": True})
                }),             
            }),
            "choropleth_map": hx.List(mode = "output", async_output=["run_simulation_task"], children={
                "state": hx.Str(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "State", "read_only": True}),
                "value": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "AAL", "format": utils.thousands_format(0), "read_only": True}),
            }),
            "choropleth_caribbean": hx.Structure(children={
                "state": hx.Str(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "State", "read_only": True}),
                "value": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "AAL", "format": utils.thousands_format(0), "read_only": True}),
            }),
            "choropleth_other": hx.Structure(children={
                "state": hx.Str(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "State", "read_only": True}),
                "value": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "AAL", "format": utils.thousands_format(0), "read_only": True}),
            }),
            "total": hx.Structure(view={"label": "Total"}, children={
                "value": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_simulation_task"], view = {"label": "AAL", "format": utils.thousands_format(0), "read_only": True}),
            }),
            "table_labels": hx.Structure(children={
                "gross_table_0": hx.Str(mode="output"),
                "gross_table_1": hx.Str(mode="output"),
                "gross_table_2": hx.Str(mode="output"),
                "gross_table_3": hx.Str(mode="output"),
                "gross_table_4": hx.Str(mode="output"),
                "gross_table_5": hx.Str(mode="output"),
                "gross_table_6": hx.Str(mode="output"),
                "gross_table_7": hx.Str(mode="output"),
                "gross_table_8": hx.Str(mode="output"),
            }),
            "file_formatter": hx.Structure(children={
                "input_file": hx.File(mode="input", file_extension=["csv"], async_input=["file_formatter_read_task", "file_formatter_write_task"] , view={"label": "Input File"}),
                "output_file": hx.File(mode="output", async_output=["file_formatter_write_task"], file_name="cleaned_file.csv", view={"label": "Output File"}),

                "file_column_names": hx.Structure(view = {"label": "Existing Column Names"}, children={
                    "column_1": hx.Str(mode="input", default=None, optionality = "optional", async_input=["file_formatter_write_task"], async_output = ["file_formatter_read_task"], view={"label": "Column 1", "read_only": True}),
                    "column_2": hx.Str(mode="input", default=None, optionality = "optional", async_input=["file_formatter_write_task"], async_output = ["file_formatter_read_task"], view={"label": "Column 2", "read_only": True}),
                    "column_3": hx.Str(mode="input", default=None, optionality = "optional", async_input=["file_formatter_write_task"], async_output = ["file_formatter_read_task"], view={"label": "Column 3", "read_only": True}),
                    "column_4": hx.Str(mode="input", default=None, optionality = "optional", async_input=["file_formatter_write_task"], async_output = ["file_formatter_read_task"], view={"label": "Column 4", "read_only": True}),
                    "column_5": hx.Str(mode="input", default=None, optionality = "optional", async_input=["file_formatter_write_task"], async_output = ["file_formatter_read_task"], view={"label": "Column 5", "read_only": True}),
                    "column_6": hx.Str(mode="input", default=None, optionality = "optional", async_input=["file_formatter_write_task"], async_output = ["file_formatter_read_task"], view={"label": "Column 6", "read_only": True}),
                    "column_7": hx.Str(mode="input", default=None, optionality = "optional", async_input=["file_formatter_write_task"], async_output = ["file_formatter_read_task"], view={"label": "Column 7", "read_only": True}),
                    "column_8": hx.Str(mode="input", default=None, optionality = "optional", async_input=["file_formatter_write_task"], async_output = ["file_formatter_read_task"], view={"label": "Column 8", "read_only": True}),
                    "column_9": hx.Str(mode="input", default=None, optionality = "optional", async_input=["file_formatter_write_task"], async_output = ["file_formatter_read_task"], view={"label": "Column 9", "read_only": True}),
                    "column_10": hx.Str(mode="input", default=None, optionality = "optional", async_input=["file_formatter_write_task"], async_output = ["file_formatter_read_task"], view={"label": "Column 10", "read_only": True})
                }),
                "override_column_names": hx.Structure(view = {"label": "New Column Names"}, children={
                    "column_1": hx.Str(mode="input", default=None, optionality = "optional", options=["EVENTID", "RATE", "PERSPVALUE", "STDDEVC", "STDDEVI", "EXPVALUE", "YEAR", "LOSS"], async_input=["file_formatter_write_task"], view={"label": "Column 1"}),
                    "column_2": hx.Str(mode="input", default=None, optionality = "optional", options=["EVENTID", "RATE", "PERSPVALUE", "STDDEVC", "STDDEVI", "EXPVALUE", "YEAR", "LOSS"], async_input=["file_formatter_write_task"], view={"label": "Column 2"}),
                    "column_3": hx.Str(mode="input", default=None, optionality = "optional", options=["EVENTID", "RATE", "PERSPVALUE", "STDDEVC", "STDDEVI", "EXPVALUE", "YEAR", "LOSS"], async_input=["file_formatter_write_task"], view={"label": "Column 3"}),
                    "column_4": hx.Str(mode="input", default=None, optionality = "optional", options=["EVENTID", "RATE", "PERSPVALUE", "STDDEVC", "STDDEVI", "EXPVALUE", "YEAR", "LOSS"], async_input=["file_formatter_write_task"], view={"label": "Column 4"}),
                    "column_5": hx.Str(mode="input", default=None, optionality = "optional", options=["EVENTID", "RATE", "PERSPVALUE", "STDDEVC", "STDDEVI", "EXPVALUE", "YEAR", "LOSS"], async_input=["file_formatter_write_task"], view={"label": "Column 5"}),
                    "column_6": hx.Str(mode="input", default=None, optionality = "optional", options=["EVENTID", "RATE", "PERSPVALUE", "STDDEVC", "STDDEVI", "EXPVALUE", "YEAR", "LOSS"], async_input=["file_formatter_write_task"], view={"label": "Column 6"}),
                    "column_7": hx.Str(mode="input", default=None, optionality = "optional", options=["EVENTID", "RATE", "PERSPVALUE", "STDDEVC", "STDDEVI", "EXPVALUE", "YEAR", "LOSS"], async_input=["file_formatter_write_task"], view={"label": "Column 7"}),
                    "column_8": hx.Str(mode="input", default=None, optionality = "optional", options=["EVENTID", "RATE", "PERSPVALUE", "STDDEVC", "STDDEVI", "EXPVALUE", "YEAR", "LOSS"], async_input=["file_formatter_write_task"], view={"label": "Column 8"}),
                    "column_9": hx.Str(mode="input", default=None, optionality = "optional", options=["EVENTID", "RATE", "PERSPVALUE", "STDDEVC", "STDDEVI", "EXPVALUE", "YEAR", "LOSS"], async_input=["file_formatter_write_task"], view={"label": "Column 9"}),
                    "column_10": hx.Str(mode="input", default=None, optionality = "optional", options=["EVENTID", "RATE", "PERSPVALUE", "STDDEVC", "STDDEVI", "EXPVALUE", "YEAR", "LOSS"], async_input=["file_formatter_write_task"], view={"label": "Column 10"}),
                }),
            }),
        }),
    })
