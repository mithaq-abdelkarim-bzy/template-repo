import hx_data_schema as hx
import data_schema.sch_utilities as utils

def sch_summary_exhibits(cds):
    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        "show_coverage_chart": hx.Bool(mode = "input", default = False, view={"label": "Show Coverage chart?"}),
        "tiv_summary": hx.List(mode="output", async_output=["run_bordereau_rater_task"], children={
            "coverage": hx.Str(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Coverage", "style_cell": "hx-input"}),
            "value": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Value", "format": utils.thousands_format(0)}),
            "percentage": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "%", "format": utils.percent_format(2)}),
            "show_row": hx.Bool(mode="output", async_output=["run_bordereau_rater_task"])
        }),
        # Total structure
        "tiv_summary_total": hx.Structure(children={
            "coverage": hx.Str(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Coverage", "style_cell": "hx-input"}),
            "value": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Value", "format": utils.thousands_format(0)}),
            "percentage": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "%", "format": utils.percent_format(2)}),
        }),
        **{
            f"{stat}_summary": hx.List(mode="output", async_output=["run_bordereau_rater_task"], children={
                f"{col_name}": hx.Str(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": f"{stat}", "style_cell": "hx-input", "multiline": True}),
                "tiv": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "TIV", "format": utils.thousands_format(0)}),
                "share_lim": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Share Limit", "format": utils.thousands_format(0)}),
                "perc_share_limit": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Share Limit %", "format": utils.percent_format(2)}),
                "gn_prem": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Beazley Share\nGN Prem", "format": utils.thousands_format(0)}),
                "ws_aal": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "WS AAL", "format": utils.thousands_format(0)}),
                "eq_aal": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "EQ AAL", "format": utils.thousands_format(0)}),
                "aop_el": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "AOP EL", "format": utils.thousands_format(0)}),
                "rate_received": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "GN Rate", "format": utils.integer_format(2)}),
                "ws_aal_rate": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "WS AAL Rate", "format": utils.integer_format(2)}),
                "eq_aal_rate": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "EQ AAL Rate", "format": utils.integer_format(2)}),
                "aop_el_rate": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "AOP EL Rate", "format": utils.integer_format(2)}),
                "prem_as_perc_of_aal": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Premium as a %\n of AAL", "format": utils.percent_format(2)}),
                "show_row": hx.Bool(mode="output", async_output=["run_bordereau_rater_task"])
            })
            for stat, col_name in zip (("construction", "year_built", "occupancy", "num_floors", "state"), ("iso_constr", "year_built", "occupancy", "num_floors", "state"))
        },
        # Total structure
        **{
            f"{stat}_summary_total": hx.Structure(children={
                f"{col_name}": hx.Str(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": f"{stat}", "style_cell": "hx-input", "multiline": True}),
                "tiv": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "TIV", "format": utils.thousands_format(0)}),
                "share_lim": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Share Limit", "format": utils.thousands_format(0)}),
                "perc_share_limit": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Share Limit %", "format": utils.percent_format(2)}),
                "gn_prem": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Beazley Share\nGN Prem", "format": utils.thousands_format(0)}),
                "ws_aal": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "WS AAL", "format": utils.thousands_format(0)}),
                "eq_aal": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "EQ AAL", "format": utils.thousands_format(0)}),
                "aop_el": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "AOP EL", "format": utils.thousands_format(0)}),
                "rate_received": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Rate Received", "format": utils.integer_format(2)}),
                "ws_aal_rate": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "WS AAL Rate", "format": utils.integer_format(2)}),
                "eq_aal_rate": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "EQ AAL Rate", "format": utils.integer_format(2)}),
                "aop_el_rate": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "AOP EL Rate", "format": utils.integer_format(2)}),
                "prem_as_perc_of_aal": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Premium as a %\n of AAL", "format": utils.percent_format(2)}),
            })
            for stat, col_name in zip (("construction", "year_built", "occupancy", "num_floors", "state"), ("iso_constr", "year_built", "occupancy", "num_floors", "state"))
        },

        **{f"show_{stat}_chart": hx.Bool(mode = "input", default = False, view={"label": f"Show {stat.title().replace('_', ' ')} chart?"})
         for stat in ["construction", "year_built", "occupancy", "num_floors", "state"]
        },
        "region_summary": hx.List(mode="output", async_output=["run_bordereau_rater_task"], children={
            "state": hx.Str(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "State", "style_cell": "hx-input"}),
            "county": hx.Str(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "County", "style_cell": "hx-input"}),
            "fips": hx.Str(mode="output", async_output=["run_bordereau_rater_task"], view={"label": "FIPS"}),
            "tiv": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "TIV", "format": utils.thousands_format(0)}),
            "share_lim": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Share\nLimit", "format": utils.thousands_format(0)}),
            "perc_share_limit": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Share\nLimit %", "format": utils.percent_format(2)}),
            "beazley_share_lim": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "AFB\n Share Limit", "format": utils.thousands_format(0)}),
            "beazley_share_gn_prem": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Beazley Share\nGN Prem", "format": utils.thousands_format(0)}),
            "one_in_250_oep": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "1 in 250 OEP", "format": utils.thousands_format(0)}),
            "one_in_10_aep": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "1 in 10 AEP", "format": utils.thousands_format(0)}),

            # for row filtering
            "show_row": hx.Bool(mode="output", async_output=["run_bordereau_rater_task"])
        }),
        # For choropleth - state level
        "region_summary_state": hx.List(mode="output", async_output=["run_bordereau_rater_task"], children={
            "label": hx.Str(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Label"}),
            "state": hx.Str(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "State"}),
            "county": hx.Str(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "County"}),
            "tiv": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "TIV", "format": utils.thousands_format(0)}),
            "share_lim": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Share\nLimit", "format": utils.thousands_format(0)}),
            "perc_share_limit": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Share\nLimit %", "format": utils.percent_format(2)}),
            "beazley_share_lim": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "AFB\n Share Limit", "format": utils.thousands_format(0)}),
            "beazley_share_gn_prem": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Beazley Share\nGN Prem", "format": utils.thousands_format(0)}),
            "one_in_250_oep": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "A1 in 250 OEP", "format": utils.thousands_format(0)}), # cant start with a number so I had to write this as one_in_250
            "one_in_10_aep": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "A1 in 10 AEP", "format": utils.thousands_format(0)}),
        }),
        # Show / Hide charts
        "show_counties": hx.Bool(mode = "input", default = True),
        "show_chart": hx.Bool(mode = "input", default = False, view={"label": "Show Chart?"}),

        # Total structure
        "region_summary_total": hx.Structure(children={
            "state": hx.Str(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "State", "style_cell": "hx-input"}),
            "county": hx.Str(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "County", "style_cell": "hx-input"}),
            "fips": hx.Str(mode="output", async_output=["run_bordereau_rater_task"], view={"label": "FIPS", "style_cell": "hx-output"}),
            "tiv": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "TIV", "format": utils.thousands_format(0), "style_cell": "hx-output"}),
            "share_lim": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Share\nLimit", "format": utils.thousands_format(0), "style_cell": "hx-output"}),
            "perc_share_limit": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Share\nLimit %", "format": utils.percent_format(2), "style_cell": "hx-output"}),
            "beazley_share_lim": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "AFB\n Share Limit", "format": utils.thousands_format(0), "style_cell": "hx-output"}),
            "beazley_share_gn_prem": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "Beazley Share\nGN Prem", "format": utils.thousands_format(0), "style_cell": "hx-output"}),
            "one_in_250_oep": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "1 in 250 OEP", "format": utils.thousands_format(0), "style_cell": "hx-output"}),
            "one_in_10_aep": hx.Float(mode="output", async_output=["run_bordereau_rater_task"],  view={"label": "1 in 10 AEP", "format": utils.thousands_format(0), "style_cell": "hx-output"}),
        }),
    })


