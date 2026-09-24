import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
import algorithms.rate_constants as constants

def get_field_label_group_mode_float_tuple(is_bp_details=False):
    mode = "override" if is_bp_details else "output"
    return [
        ("composition", "Composition", "output", None),
        ("acc_aquisition_costs", "Accout\nAcquisition\nCosts", "output", None),
        ("attr_base_gn_ulr", "Attritional\nBase GN ULR", "output", "Attritional GN ULR"),
        ("attr_inflation_1_year", "Inflation\n1 Year", "output", "Attritional GN ULR"),
        ("attr_rate_change", "Rate Change", "output", "Attritional GN ULR"),
        ("attr_rarc_margin", "RARC Margin", "output", "Attritional GN ULR"),
        ("attr_portfolio_change", "Portfolio\nChange", "output", "Attritional GN ULR"),
        ("cat_base_gn_ulr", "Cat Base\nGN ULR", "output", "CAT GN ULR"),
        ("cat_inflation_1_year", "Inflation 1 Year", "output", "CAT GN ULR"),
        ("cat_rate_change", "Rate Change", "output", "CAT GN ULR"),
        ("cat_rarc_margin", "RARC Margin", "output", "CAT GN ULR"),
        ("cat_climate_change", "Climate Change", "output", "CAT GN ULR"),
        ("cat_nmp_general", "NMP General", "output", "CAT GN ULR"),
        ("cat_nmp_all_other", "NMP All Other", "output", "CAT GN ULR"),
        ("selected_attr_gn_ulr", "Selected\nAttritional\nGN ULR", "output", "Final Selected GN ULR"),
        ("selected_cat_gn_ulr", "Selected Cat\nGN ULR", "output", "Final Selected GN ULR"),
        ("total_gn_ulr", "Total\nGN ULR", "output", "Final Selected GN ULR"),
        ("bp_acquisition_costs", "BP Acquisition\nCosts", "output", "Final Selected GN ULR"),
        ("adj_attr_gn_ulr", "Adj Attritional\nGN ULR", mode, "Final Selected GN ULR"),
        ("adj_cat_gn_ulr", "Adj Cat\nGN ULR", mode, "Final Selected GN ULR"),
        ("adj_total_gn_ulr", "Adj Total\nGN ULR", "output", "Final Selected GN ULR")
    ]


def sch_bp_projections(cds):
    cds.extend_node_rater_defined(
        "cds",
        {
            "bp_projections": hx.Structure(
                view={"label": "Business Plan Pricing"},
                children={
                    "bp_summary_by_lob": hx.List(
                        mode="input",
                        default_element_count=constants.DEFAULT_NUM_LOB,
                        async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                        async_input=[],
                        children={
                            "tracker_class": hx.Str(mode="output", view={"label": "Tracker Class"}, async_input=[]),
                            "selected_lob": hx.Str(mode="output", view={"label": "Selected Line of Business"}, async_input=[]),
                            "bp_class": hx.Str(mode="output", view={"label": "Beazley Business Plan Class"}, async_input=[]),
                            "risk_code": hx.Str(mode="output", view={"label": "Risk Code"}, async_input=[]),
                            "is_row_visible": hx.Bool(mode="output", async_input=[]),
                            "rate_change_override": hx.Float(mode="output", async_input=[], view={"label": "Rate Change\nOverride", "format": percent_format(1)}),
                            **{
                                field: hx.Float(
                                    mode=mode,
                                    async_input=["sync_lob_lists_task"], 
                                    view={"label": label,
                                          "format": percent_format(1),
                                          "group": group}
                                ) for field, label, mode, group in get_field_label_group_mode_float_tuple()
                            }
                        }
                    ),
                    "bp_details": hx.List(
                        mode="input",
                        default_element_count=constants.DEFAULT_NUM_RISK_CODES,
                        async_input=[],
                        async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                        children={
                            "tracker_class": hx.Str(mode="output", view={"label": "Tracker Class"}, async_input=[]),
                            "selected_lob": hx.Str(mode="output", view={"label": "Selected Line of Business"}, async_input=[]),
                            "bp_class": hx.Str(mode="override", view={"label": "Beazley Business Plan Class"}, async_input=["sync_lob_lists_task"]),
                            "risk_code": hx.Str(mode="output", view={"label": "Risk Code"}, async_input=[]),
                            "is_row_visible": hx.Bool(mode="output", async_input=[]),
                            "rate_change_override": hx.Float(mode="override", async_input=["sync_lob_lists_task"],  view={"label": "Rate Change\nOverride", "format": percent_format(1)}),
                            **{
                                field: hx.Float(
                                    mode=mode,
                                    async_input=["sync_lob_lists_task"],
                                    view={"label": label,
                                          "format": percent_format(1),
                                          "group": group}
                                ) for field, label, mode, group in get_field_label_group_mode_float_tuple(is_bp_details=True)
                            }
                        }
                    )
                },
            ),
        }),
