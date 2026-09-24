import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
import algorithms.rate_constants as constants

def generate_years_headers_list(start: int, end: int):
    return [f"year_{year}" for year in range(start, end + 1)]


def sch_inflation(cds):
    cds.extend_node_rater_defined(
        "cds",
        {
            "inflation": hx.Structure(
                view={"label": "Business Plan Pricing"},
                children={
                    "summary_by_lob": hx.List(
                        mode="output",
                        children={
                            "selected_lob": hx.Str(mode="output", view={"label": "Selected LoB"}),
                            "risk_code": hx.Str(mode="output", view={"label": "Risk Code"}),
                            "composition": hx.Float(mode="output", view={"label": "Composition","format" :percent_format(0)}),
                            "bp_class": hx.Str(mode="output", view={"label": "BP Class"}),
                            **{
                                field: hx.Float(mode="output", view={
                                                "label": label, "format": percent_format(1)})
                                for field, label in [(year, year) for year in generate_years_headers_list(0, 25)]
                            }
                        }
                    ),
                    "details": hx.List(
                        mode="input",
                        default_element_count=constants.DEFAULT_NUM_RISK_CODES,
                        async_input=[],
                        async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                        children={
                            "selected_lob": hx.Str(mode="output", view={"label": "Selected LoB"}, async_input=[]),
                            "risk_code": hx.Str(mode="output", view={"label": "Risk Code"}, async_input=[]),
                            "composition": hx.Float(mode="output", view={"label": "Composition",'format':percent_format(0)}, async_input=[]),
                            "bp_class": hx.Str(mode="override", view={"label": "BP Class"}, async_input=["sync_lob_lists_task"]),
                            "is_row_visible": hx.Bool(mode="output", async_input=[]),
                            **{
                                field: hx.Float(mode="output", view={"label": label, "format": percent_format(1)}, async_input=[])
                                for field, label in  [(year, year) for year in generate_years_headers_list(6, 25)]
                            },
                            **{
                                field: hx.Float(mode="override", view={"label": label, "format": percent_format(1)}, async_input=["sync_lob_lists_task"])
                                for field, label in [(year, year) for year in generate_years_headers_list(0, 5)]
                            }
                        }
                    )
                },
            ),
        }
    )
