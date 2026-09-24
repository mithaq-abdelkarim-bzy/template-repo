import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
from algorithms import rate_constants as constants


def generate_years_headers_list(start: int, end: int):
    return [f"year_{year}" for year in range(start, end + 1)]


def sch_assumed_deductions(cds):
    cds.extend_node_rater_defined(
        "cds",
        {
            "assumed_deductions": hx.Structure(
                children={
                    "model_type": hx.Str(mode="override", options=['Data', 'Manual'], view={"label": "Assumed Deductions Source", "options": {"read_only_option": {"read_only": True}}}),
                    "data_driven_deductions": hx.Structure(
                        view={"label": "Gross Premium"},
                        children={
                            "year_end": hx.Str(mode="override", options_data="../year_dropdown", options_field="year_0", optionality="optional", view={"label": "Year End"}),
                            "year_start": hx.Str(mode="override", options_data="../year_dropdown", options_field="year_0", optionality="optional",  view={"label": "Year Start"}),
                            "year_dropdown": hx.List(mode="output", children={"year_0": hx.Str(mode="output")}),
                            "gross_premium": hx.Structure(
                                view={"label": "Gross Premium"},
                                children={
                                    "summary": hx.Structure(
                                        view={"label": "Total"},
                                        children={
                                            **{year: hx.Float(mode="output", view={"label": f"Total {year}", "format": thousands_format(0)}) for year in generate_years_headers_list(0, constants.YEARS_TO_CONSIDER_IN_ASSUMED_DEDUCTIONS)}
                                        }),
                                    "deductions_derived_from_data": hx.List(
                                        mode="output",
                                        children={
                                            **{year: hx.Float(mode="output", view={"label": f"Total {year}", "format": thousands_format(0)}) for year in generate_years_headers_list(0, constants.YEARS_TO_CONSIDER_IN_ASSUMED_DEDUCTIONS)},
                                            "selected_lob": hx.Str(mode="output", view={"label": "Selected Line of Business"})
                                        }),
                                }
                            ),
                            "net_premium": hx.Structure(
                                view={"label": "Net Premium"},
                                children={
                                    "summary": hx.Structure(
                                        view={"label": "Total"},
                                        children={
                                            **{year: hx.Float(mode="output", view={"label": f"Total {year}", "format": thousands_format(0)}) for year in generate_years_headers_list(0, constants.YEARS_TO_CONSIDER_IN_ASSUMED_DEDUCTIONS)},
                                        }),
                                    "deductions_derived_from_data": hx.List(
                                        mode="output",
                                        children={
                                            **{year: hx.Float(mode="output", view={"label": f"Total {year}", "format": thousands_format(0)}) for year in generate_years_headers_list(0, constants.YEARS_TO_CONSIDER_IN_ASSUMED_DEDUCTIONS)},
                                            "selected_lob": hx.Str(mode="output", view={"label": "Selected Line of Business"})
                                        }),
                                }
                            ),
                            "market_deductions": hx.Structure(
                                view={"label": "Market Deductions"},
                                children={
                                    "summary": hx.Structure(
                                        view={"label": "Total"},
                                        children={
                                            **{year: hx.Float(mode="output", view={"label": f"{year}", "format": percent_format(2)}) for year in generate_years_headers_list(0, constants.YEARS_TO_CONSIDER_IN_ASSUMED_DEDUCTIONS)},
                                        }),
                                    "deductions_derived_from_data": hx.List(
                                        mode="output",
                                        children={
                                            **{year: hx.Float(mode="output", view={"label": f"{year}", "format": percent_format(2)}) for year in generate_years_headers_list(0, constants.YEARS_TO_CONSIDER_IN_ASSUMED_DEDUCTIONS)},
                                            "selected_lob": hx.Str(mode="output", view={"label": "Selected Line of Business"})
                                        })
                                }
                            ),
                            "deductions": hx.Structure(
                                view={"label": "Data Driven Deductions"},
                                children={
                                    "table": hx.List(
                                        mode="input",
                                        default_element_count=constants.DEFAULT_NUM_LOB,
                                        async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                                        children={
                                            "selected_lob":      hx.Str(mode="output", view={"label": "Selected Line of Business"}),
                                            "market_deductions": hx.Float(mode="override", async_input=["sync_lob_lists_task"], view={"label": "Market Deductions", "format": percent_format(2)}),
                                            "mga_fee":           hx.Float(mode="override", async_input=["sync_lob_lists_task"], view={"label": "Consortium Managers fee / MGA fee", "format": percent_format(2)}),
                                            "facility_brokerage":hx.Float(mode="override", async_input=["sync_lob_lists_task"], view={"label": "Facility Brokerage", "format": percent_format(2)}),
                                            "leaders_fee":       hx.Float(mode="override", async_input=["sync_lob_lists_task"], view={"label": "Leaders Fee", "format": percent_format(2)}),
                                            "service_fee":       hx.Float(mode="override", async_input=["sync_lob_lists_task"], view={"label": "Service Fee", "format": percent_format(2)}),
                                            "other":             hx.Float(mode="override", async_input=["sync_lob_lists_task"], view={"label": "Other", "format": percent_format(2)}),
                                            "selected_effective_deductions": hx.Float(mode="output", view={"label": "Selected Effective Deductions", "format": percent_format(2)}),
                                            "is_row_visible":   hx.Bool(mode="output")
                                        }
                                    ),
                                    "amount": hx.Structure(
                                        view={"label": "Amount"},
                                        children={
                                            "mga_fee": hx.Float(mode="input", default=0, optionality='optional', view={"label": "Consortium Managers fee / MGA fee", "format": percent_format(2)}),
                                            "facility_brokerage": hx.Float(mode="input", default=0, optionality='optional', view={"label": "Facility Brokerage", "format": percent_format(2)}),
                                            "leaders_fee": hx.Float(mode="input", default=0, optionality='optional', view={"label": "Leaders fee", "format": percent_format(2)}),
                                            "service_fee": hx.Float(mode="input", default=0, optionality='optional', view={"label": "Service Fee", "format": percent_format(2)}),
                                            "other": hx.Float(mode="input", default=0, optionality='optional', view={"label": "Other", "format": percent_format(2)}),
                                        }
                                    ),
                                    "basis": hx.Structure(
                                        view={"label": "Basis"},
                                        children={
                                            "mga_fee": hx.Str(mode="input", default_index=0, options=['Gross', 'Net'], view={"label": "Consortium Managers fee / MGA fee"}),
                                            "facility_brokerage": hx.Str(mode="input", default_index=0, options=['Gross', 'Net'], view={"label": "Facility Brokerage"}),
                                            "leaders_fee": hx.Str(mode="input", default_index=0, options=['Gross', 'Net'], view={"label": "Leaders fee"}),
                                            "service_fee": hx.Str(mode="input", default_index=0, options=['Gross', 'Net'], view={"label": "Service Fee"}),
                                            "other": hx.Str(mode="input", default_index=0, options=['Gross', 'Net'], optionality='optional', view={"label": "Other"}),
                                        }
                                    ),
                                }
                            ),
                        }
                    ),
                    "deductions_manually_entered": hx.Structure(
                        view={"label": "Deductions Manually entered"},
                        children={
                            "table": hx.List(
                                mode="input",
                                default_element_count=constants.DEFAULT_NUM_LOB,
                                async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                                children={
                                    "selected_lob": hx.Str(mode="output", view={"label": "Selected Line of Business"}),
                                    "market_deductions": hx.Float(mode="input", default=0, optionality='optional', view={"label": "Market Deductions", "format": percent_format(2)}),
                                    "mga_fee": hx.Float(mode="override", view={"label": "Consortium Managers fee / MGA fee", "format": percent_format(2)}),
                                    "facility_brokerage": hx.Float(mode="override", view={"label": "Facility Brokerage", "format": percent_format(2)}),
                                    "leaders_fee": hx.Float(mode="override", view={"label": "Leaders Fee", "format": percent_format(2)}), 
                                    "service_fee": hx.Float(mode="override", view={"label": "Service Fee", "format": percent_format(2)}),
                                    "other": hx.Float(mode="override", view={"label": "Other", "format": percent_format(2)}),
                                    "selected_effective_deductions":  hx.Float(mode="output", view={"label": "Selected Effective Deductions", "format": percent_format(2)}),
                                    "is_row_visible": hx.Bool(mode="output")
                                }
                            ),
                            "amount": hx.Structure(
                                view={"label": "Amount"},
                                children={
                                    "selected_lob": hx.Str(mode="output", view={"label": " "}),
                                    "market_deductions": hx.Float(mode="output", view={"label": " "}),
                                    "mga_fee": hx.Float(mode="input", default=0, optionality='optional', view={"label": "Consortium Managers fee / MGA fee", "format": percent_format(2)}),
                                    "facility_brokerage": hx.Float(mode="input", default=0, optionality='optional', view={"label": "Facility Brokerage", "format": percent_format(2)}),
                                    "leaders_fee": hx.Float(mode="input", default=0, optionality='optional', view={"label": "Leaders fee", "format": percent_format(2)}),
                                    "service_fee": hx.Float(mode="input", default=0, optionality='optional', view={"label": "Service Fee", "format": percent_format(2)}),
                                    "other": hx.Float(mode="input", default=0, optionality='optional', view={"label": "Other", "format": percent_format(2)}),
                                }
                            ),
                            "basis": hx.Structure(
                                view={"label": "Basis"},
                                children={
                                    "selected_lob": hx.Str(mode="output", view={"label": "Selected Line of Business"}),
                                    "market_deductions": hx.Float(mode="output", view={"label": "Market Deductions"}),
                                    "mga_fee": hx.Str(mode="input", default_index=0, options=['Gross', 'Net'], view={"label": "Consortium Managers fee / MGA fee"}),
                                    "facility_brokerage": hx.Str(mode="input", default_index=0, options=['Gross', 'Net'], view={"label": "Facility Brokerage"}),
                                    "leaders_fee": hx.Str(mode="input", default_index=0, options=['Gross', 'Net'], view={"label": "Leaders fee"}),
                                    "service_fee": hx.Str(mode="input", default_index=0, options=['Gross', 'Net'], view={"label": "Service Fee"}),
                                    "other": hx.Str(mode="input", default_index=0, options=['Gross', 'Net'], optionality='optional', view={"label": "Other"}),
                                }
                            ),
                        }
                    ),
                }
            )
        }
    )
