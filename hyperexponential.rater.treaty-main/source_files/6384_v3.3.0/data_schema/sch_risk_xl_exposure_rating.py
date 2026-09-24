import hx_data_schema as hx
from hx import params as hx_params
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
import data_schema.sch_utilities as utils
from algorithms.rate_constants import max_layers, max_exposure_years

def sch_risk_xl_exposure_rating(cds):
    cds.extend_node_rater_defined("cds", {
        "risk_xl_exposure_rating": hx.Structure(children={
            "segment_options": hx.List(mode = "output", children= {
                "option": hx.Str(mode = "output")
             }),
            **{f"show_loss_layer_{index}": hx.Bool(mode="output", optionality="optional")
                    for index in range(1, max_layers + 1)
            },
            "exposure_listing": hx.List(mode="input",default_element_count = 6, children={
                "lel_from": hx.Float(mode = "input", default = None, optionality = "optional", view={"label": "LEL From", "format": utils.thousands_format(0)}),
                "lel_to": hx.Float(mode = "input", default = None, optionality = "optional", view={"label": "LEL To", "format": utils.thousands_format(0)}),
                "attachment_band": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Attachment Band"}),
                "segment": hx.Str(mode="input", default=None, optionality="optional", options_data = "../../../segment_options", options_field = "option", allow_custom_value = False, view={"label": "Segment"}),

                "location_count": hx.Float(mode = "input", default = None, optionality = "optional", async_input=["run_exposure_simulation_task"], view={"label": "Location Count", "format": utils.thousands_format(0)}),
                "gnepi": hx.Float(mode = "input", default = None, optionality = "optional", view={"label": "GNEPI", "format": utils.thousands_format(0)}),
                "tiv": hx.Float(mode = "input", default = None, optionality = "optional", view={"label": "TIV", "format": utils.thousands_format(0)}),
                "net_exposed_limit": hx.Float(mode = "input", default = None, optionality = "optional", view={"label": "Net Exposed Limit", "format": utils.thousands_format(0)}),

                "location_count_adj": hx.Float(mode = "output", optionality = "optional", async_input=["run_exposure_simulation_task"], view={"label": "Location Count Adj.", "format": utils.thousands_format(0)}),
                "gnepi_adj": hx.Float(mode = "output", optionality = "optional", view={"label": "GNEPI Adj.", "format": utils.thousands_format(0)}),
                "tiv_adj": hx.Float(mode = "output", optionality = "optional", view={"label": "TIV Adj.", "format": utils.thousands_format(0)}),
                "net_exposed_limit_adj": hx.Float(mode = "output", optionality = "optional", view={"label": "Net Exposed Limit Adj.", "format": utils.thousands_format(0)}),

                "avg_cedant_participation": hx.Float(mode = "input", default = None, optionality = "optional", async_input=["run_exposure_simulation_task"], view={"label": "Avg Cedant Participation", "format": utils.percent_format(2)}),
                "avg_attachment": hx.Float(mode = "input", default = None, optionality = "optional", async_input=["run_exposure_simulation_task"], view={"label": "Avg Attachment", "format": utils.thousands_format(0)}),
                "avg_tiv": hx.Float(mode = "output", optionality = "optional", async_input=["run_exposure_simulation_task"], view={"label": "Avg TIV", "format": utils.thousands_format(0)}),
                "avg_lel": hx.Float(mode = "output", optionality = "optional", view={"label": "Avg LEL", "format": utils.thousands_format(0)}),
                "avg_100_pol_limit": hx.Float(mode = "output", optionality = "optional", view={"label": "Avg 100% Policy Limit", "format": utils.thousands_format(0)}),
                "gross_el": hx.Float(mode = "output", optionality = "optional", view={"label": "Gross EL", "format": utils.thousands_format(0)}),
                "avg_policy_worth": hx.Float(mode = "output", optionality = "optional", async_input=["run_exposure_simulation_task"], view={"label": "Avg Policy Worth", "format": utils.percent_format(1)}),
                "gu_el": hx.Float(mode = "output", optionality = "optional", view={"label": "GU EL", "format": utils.thousands_format(0)}),
                "expected_severity_perc": hx.Float(mode = "output", optionality = "optional", view={"label": "E[X] %", "format": utils.percent_format(2)}),
                "expected_severity": hx.Float(mode = "output", optionality = "optional", view={"label": "E[X]", "format": utils.thousands_format(0)}),
                "expected_frequency": hx.Float(mode = "output", optionality = "optional", async_input=["run_exposure_simulation_task"], view={"label": "E[N]", "format": utils.thousands_format(2)}),
                "swiss_re_c": hx.Float(mode = "output", optionality = "optional", async_input=["run_exposure_simulation_task"], view={"label": "Swiss Re C"}),
                "swiss_re_c_override": hx.Str(mode="input", default=None, optionality="optional", options_table = "table_risk_xl_curves", options_column="curve_name", async_input=["run_exposure_simulation_task"], view={"label": "Curve Override"}),
                "ex_cat_ulr_readonly": hx.Float(mode = "output", optionality = "optional", view={"label": "Ex. CAT ULR", "format": utils.percent_format(1)}),
                "ex_cat_ulr_override": hx.Float(mode = "input", default=None, optionality = "optional", view={"label": "Ex. CAT ULR Override", "format": utils.percent_format(1)}),                

                # show layer losses for each loss
                **{f"loss_layer_{index}": hx.Float(mode="output", optionality="optional", view={"label": f"Layer {index}", "format": utils.thousands_format(0)})
                    for index in range(1, max_layers + 1)
                },
            }), 
            **{f"exposure_segment_{index}" : hx.Structure(view={"label": f"Exposure Segment {index}"}, children={
                "segment_name": hx.Str(mode="input", default="",optionality="optional", view={"label": "Segment Name"}),
                "ex_cat_ulr": hx.Float(mode = "input", default = None, optionality = "optional", view={"label": "Ex. CAT ULR", "format": utils.percent_format(1)}),
                "curve_selection": hx.Str(mode="input", default=None, optionality="optional", options_table = "table_risk_xl_curves", options_column="curve_name", view={"label": "Curve Selection", "format": utils.thousands_format(2)}),
                "commentary": hx.Str(mode="input", default="",optionality="optional", view={"label": "Commentary"}),
                "exposed_limit_ty": hx.Float(mode = "output", optionality = "optional", view={"label": "Exposed Limit TY", "format": utils.thousands_format(0)}),
                "exposed_limit_ly": hx.Float(mode = "input", default = None, optionality = "optional", view={"label": "Exposed Limit LY", "format": utils.thousands_format(0), "read_only": True}),
                "exposed_limit_change": hx.Float(mode = "output", optionality = "optional", view={"label": "Exposed Limit Change", "format": utils.percent_format(1)}),
                }) for index in range(1, 21)
            },
            "exposure_segment_total" : hx.Structure(view={"label": f"Total"}, children={
                "commentary": hx.Str(mode="input", default="",optionality="optional", view={"label": "Commentary"}),
                "exposed_limit_ty": hx.Float(mode = "output", optionality = "optional", view={"label": "Exposed Limit TY", "format": utils.thousands_format(0)}),
                "exposed_limit_ly": hx.Float(mode = "input", default = None, optionality = "optional", view={"label": "Exposed Limit LY", "format": utils.thousands_format(0), "read_only": True}),
                "exposed_limit_change": hx.Float(mode = "output", optionality = "optional", view={"label": "Exposed Limit Change", "format": utils.percent_format(1)}),
                }),
            "gnepi_exposure_adjustment": hx.Bool(mode = "input", default = False, view={"label": "GNEPI Exposure Adjustment?"}),
            "gnepi_adj_factor": hx.Float(mode = "output", optionality = "optional", view={"label": "GNEPI Adjustment Factor"}),
            "gnepi_by_band": hx.Str(mode = "input", default = "Provided", options=["Provided", "Use Exposure"], view={"label": "GNEPI by band"})
            
        })
    })

    cds.extend_node_rater_defined("cds/layers",
        {
            "risk_xl_exposure_rating": hx.Structure(children={
                "gross_non_cat_el_deterministic": hx.Float(mode = "output", optionality = "optional", view = {"label": "Gross (Reins.) Non-Cat EL", "format": utils.thousands_format(0)}),
                "gross_total_el_deterministic": hx.Float(mode = "output", optionality = "optional", view = {"label": "Gross Total EL", "format": utils.thousands_format(0)}),
                "gross_total_el_sim": hx.Float(mode = "input", default = None, optionality = "optional", async_output = ["run_exposure_simulation_task", "start_renewal_task"], view = {"label": "Gross Total EL Simulation", "format": utils.thousands_format(0), "read_only": True}),

                "net_el_excl_reins_prem": hx.Float(mode = "output", optionality = "optional", view = {"label": "Net EL (Free Reinstatements)", "format": utils.thousands_format(0)}),
                "net_el": hx.Float(mode = "output", optionality = "optional", view = {"label": "Net EL", "format": utils.thousands_format(0)}),

                "model_limit_factor": hx.Float(mode = "input", default = None, optionality = "optional", async_output = ["run_exposure_simulation_task", "start_renewal_task"], view = {"label": "Model Adj. Factor", "format": {"output": "percent", "mantissa": 1}, "read_only": True}),
                "no_expected_reins": hx.Float(mode = "input", default = None, optionality = "optional", async_output = ["run_exposure_simulation_task", "start_renewal_task"], view = {"label": "Expected Reinstatement Cost", "format": {"thousandSeparated": True, "mantissa": 3}, "read_only": True}),
        }),
    })


