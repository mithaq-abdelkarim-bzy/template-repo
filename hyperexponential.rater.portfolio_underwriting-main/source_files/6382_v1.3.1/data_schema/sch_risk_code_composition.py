import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format, create_node
from algorithms import rate_constants as constants


def generate_years_headers_list(start: int, end: int):
    return [f"year_{year}" for year in range(start, end + 1)]


def get_string_values_outputs_for_composition_selction():
    return [
        ("cs_risk_code", "Risk code"),
        ("exists_in_data_bool", "Available for \nModelling?"),
        ("cs_facility_line_of_business", "Facility Line\nof Business"),
        ("risk_code_description", "Risk Code Description"),
    ]


def sch_risk_code_composition(cds):
    cds.extend_node_rater_defined(
        "cds",
        {
            "risk_code_composition": hx.Structure(
                view={"label": "Risk Code Composition"},
                children={
                    "model_type": hx.Str(mode="override", options=['Data', 'Manual'], view={"label": "Risk Code Composition Source", "options": {"read_only_option": {"read_only": True}}}),
                    "data_driven_composition": hx.Structure(
                        children={
                            "year_end": hx.Str(mode="override", options_data="../year_dropdown", options_field="year_0", optionality="optional", view={"label": "Year End"}),
                            "year_start": hx.Str(mode="override", options_data="../year_dropdown", options_field="year_0", optionality="optional", view={"label": "Year Start"}),
                            "year_dropdown": hx.List(mode="output", children={"year_0": hx.Str(mode="output")}),
                            "premium_basis": create_node("Premium Basis", type="str", options=["Gross", "Net"], default="Net"),
                            "premiums_table": hx.List(
                                mode="output",
                                children={
                                    **{f"year_{i}": create_node(f"year_{i}", "output") for i in range(0, constants.YEARS_TO_CONSIDER_IN_RISK_CODE_COMPOSITION + 1)},
                                    "selected_premium": create_node("Selected \nPremium", "output"),
                                    "composition": create_node("Composition", "output", format=percent_format(2)),
                                    "risk_code": create_node("Risk Code", "output", type='str'),
                                    "exist_in_lloyds_data_bool": create_node("Available for \nModelling?", "output", type='str'),
                                }
                            ),
                            "summary": hx.Structure(
                                view={"label": "Total"},
                                children={
                                    **{f"year_{i}": create_node(f"year_{i}", "output") for i in range(0, constants.YEARS_TO_CONSIDER_IN_RISK_CODE_COMPOSITION + 1)},
                                    "selected_premium": create_node("Selected Premium", "output")
                                }
                            ),
                            "composition_selection": hx.Structure(
                                view={"label": "Composition Selection"},
                                children={
                                    "table": hx.List(
                                        mode="input",
                                        default_element_count=192,
                                        async_input=[
                                            "copy_composition_selection_table"],
                                        children={
                                            **{field: hx.Str(mode="output", async_input=["copy_composition_selection_table"], view={"label": label}) for field, label in get_string_values_outputs_for_composition_selction()},
                                            "cs_composition": hx.Float(mode="output", async_input=["copy_composition_selection_table"], view={"label": "Composition", "format": percent_format(2)}),
                                            "composition_reweighted": hx.Float(mode="output", async_input=["copy_composition_selection_table"], view={"label": "Composition\nRe-weighted", "format": percent_format(2)}),
                                            "model": hx.Bool(mode="input", default=True, optionality='required', async_input=["copy_composition_selection_table"], view={"label": "Model"}),
                                            "selected_lob": hx.Str(mode="input", default=None, optionality='optional', async_input=["copy_composition_selection_table"], view={"label": "Selected Line\nof Business"}),
                                            "selected_bp_class":hx.Str(mode="override", optionality="optional", options_data="../../../../../bp_class_desc", options_field="desc", view={"label": "Selected Business\nPlan Class"}, async_input=["copy_composition_selection_table"]),
                                            "tracker_class":  create_node("Tracker Class", mode="override", type='str', options="table_trifocus_list/Trifocus List", async_input=["copy_composition_selection_table"]),
                                            "is_row_visible": hx.Bool(mode="output", async_input=["copy_composition_selection_table"],)
                                        }
                                    ),                                                  
                                    "modelled": hx.Float(mode="output", view={"label": "% Modelled", "format": {"output": "percent", "mantissa": 2}})
                                }
                            ),
                        }
                    ),
                    "composition_manual": hx.Structure(
                        view={"label": "Composition Selection"},
                        children={
                            "table": hx.List(
                                mode="input",
                                default_element_count=192,
                                async_output=[
                                    "copy_composition_selection_table", "clear_manual_risk_code_composition_table"],
                                children={
                                    "cs_risk_code": hx.Str(mode="input", default=None, optionality="optional", options_column="RiskCode", options_table="table_lloyds_risk_code_desc", async_output=["copy_composition_selection_table", "clear_manual_risk_code_composition_table"], view={"label": "Risk Code"}),
                                    "cs_composition": hx.Float(mode="input", default=0, optionality='optional', async_output=["copy_composition_selection_table", "clear_manual_risk_code_composition_table"], view={"label": "Composition", "format": percent_format(2)}),
                                    "exists_in_data_bool": hx.Str(mode="output", view={"label": "Available for \nModelling?"}),
                                    "model": hx.Bool(mode="input", async_output=["copy_composition_selection_table", "clear_manual_risk_code_composition_table"], default=True, optionality='required', view={"label": "Model"}),
                                    "composition_reweighted": hx.Float(mode="output", view={"label": "Composition\nRe-weighted", "format": percent_format(2)}),
                                    "cs_facility_line_of_business": hx.Str(mode="output", view={"label": "Facility Line\nof Business"}),
                                    "selected_lob": hx.Str(mode="input", default=None, optionality='optional', async_output=["copy_composition_selection_table", "clear_manual_risk_code_composition_table"], view={"label": "Selected Line\nof Business"}),
                                    "selected_bp_class":hx.Str(mode="override", optionality="optional", options_data="../../../../bp_class_desc", options_field="desc", view={"label": "Selected Business\nPlan Class"}),
                                    "tracker_class": create_node("Tracker Class", mode="override", type='str', options="table_trifocus_list/Trifocus List"),
                                    "risk_code_description": hx.Str(mode="output", view={"label": "Risk Code Description"}), "is_row_visible": hx.Bool(mode="output")
                                }
                            ),
                            "modelled": hx.Float(mode="output", view={"label": "% Modelled", "format": {"output": "percent", "mantissa": 2}})
                        }
                    ),
                    "bp_class_desc": hx.List(mode="output", children={"desc": hx.Str(mode="output")})

                    
                }
            ),
        }
    )
