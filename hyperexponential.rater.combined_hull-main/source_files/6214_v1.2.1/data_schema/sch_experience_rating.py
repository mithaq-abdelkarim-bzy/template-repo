import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
import algorithms.rate_constants as constants


def sch_experience_rating(cds):
    cds.extend_node_rater_defined(
        "cds/experience_rating",
        {
            "ship_building": hx.Structure(
                children={
                    "extracted_policies": hx.List(
                        mode="output",
                        async_output=[
                            {"task": "populate_bi_data", "reset": False},
                            {"task": "start_renewal_task", "reset": False},
                        ],
                        children={
                            "policy_reference": hx.Str(
                                mode="output",
                                async_output=[
                                    {"task": "populate_bi_data", "reset": False},
                                    {"task": "start_renewal_task", "reset": False},
                                ],
                            ),
                            "written_or_estimated_premium": hx.Float(
                                mode="output",
                                async_output=[
                                    {"task": "populate_bi_data", "reset": False},
                                    {"task": "start_renewal_task", "reset": False},
                                ],
                            ),
                            "total_incurred_shared_line": hx.Float(
                                mode="output",
                                async_output=[
                                    {"task": "populate_bi_data", "reset": False},
                                    {"task": "start_renewal_task", "reset": False},
                                ],
                            ),
                            "rate_change": hx.Float(
                                mode="output",
                                async_output=[
                                    {"task": "populate_bi_data", "reset": False},
                                    {"task": "start_renewal_task", "reset": False},
                                ],
                            ),
                            "acquisition_cost": hx.Float(
                                mode="output",
                                async_output=[
                                    {"task": "populate_bi_data", "reset": False},
                                    {"task": "start_renewal_task", "reset": False},
                                ],
                            ),
                            "signed_line": hx.Float(
                                mode="output",
                                async_output=[
                                    {"task": "populate_bi_data", "reset": False},
                                    {"task": "start_renewal_task", "reset": False},
                                ],
                            ),
                            "yoa": hx.Int(
                                mode="output",
                                async_output=[
                                    {"task": "populate_bi_data", "reset": False},
                                    {"task": "start_renewal_task", "reset": False},
                                ],
                            ),
                            "is_include_year": hx.Bool(
                                mode="output",
                                async_output=[
                                    {"task": "populate_bi_data", "reset": False},
                                    {"task": "start_renewal_task", "reset": False},
                                ],
                            ),
                            "previous_insurer": hx.Str(
                                mode="output",
                                async_output=[
                                    {"task": "populate_bi_data", "reset": False},
                                    {"task": "start_renewal_task", "reset": False},
                                ],
                            ),
                        },
                    ),
                    "claims_date": hx.Date(
                        mode="input",
                        default=None,
                        optionality="optional",
                        view={"label": "Claims Date As"},
                        async_input=["populate_bi_data"],
                        async_output=[{"task": "populate_bi_data", "reset": False}],
                    ),
                    "claims_currency": hx.Str(
                        mode="input",
                        default="USD",
                        options_table="table_input_currency",
                        options_column="ccy",
                        view={"label": "Currency for Premium and Incurred Input"},
                    ),
                    "claims_fx_rate": hx.Float(
                        mode="override",
                        view={"label": "Exchange Rate", "format": {"mantissa": 2}},
                    ),
                    "current_year_rate_change": hx.Float(
                        mode="input",
                        default=1,
                        optionality="optional",
                        view={"format": percent_format(0)},
                    ),
                    "large_load_selection": hx.Structure(
                        children={
                            "average_on_levelled_net_large_lr": hx.Float(
                                mode="output",
                                view={
                                    "label": "Average On-Levelled Net Large LR (%)",
                                    "format": percent_format(0),
                                },
                            ),
                            "user_selected": hx.Structure(
                                children={
                                    "user_number_of_years_expected_large_loss": hx.Int(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["rarc_task"],
                                        view={
                                            "label": "Expect large loss once every this number of years",
                                            "format": integer_format(0),
                                        },
                                    ),
                                    "user_average_net_lr_of_large_loss": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["rarc_task"],
                                        view={
                                            "label": "Average Net LR of a large loss (%)",
                                            "format": percent_format(0),
                                        },
                                    ),
                                    "selected_large_load": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Selected Large Load",
                                            "format": percent_format(1),
                                        },
                                    ),
                                },
                            ),
                            "portfolio_load_guidance": hx.Structure(
                                children={
                                    "guidance_number_of_years_expected_large_loss": hx.Int(
                                        mode="output",
                                        view={
                                            "label": "Expect large loss once every this number of years",
                                            "format": integer_format(0),
                                        },
                                    ),
                                    "guidance_average_net_lr_of_large_loss": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Average Net LR of a large loss (%)",
                                            "format": percent_format(0),
                                        },
                                    ),
                                    "portfolio_large_load": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Portfolio Large Load",
                                            "format": percent_format(1),
                                        },
                                    ),
                                }
                            ),
                        }
                    ),
                    "experience_pricing_results": hx.Structure(
                        children={
                            "average_attritional_ulr": hx.Float(
                                mode="output",
                                view={
                                    "label": "Average Attritional Net LR",
                                    "format": percent_format(1),
                                },
                            ),
                            "large_load": hx.Float(
                                mode="output",
                                view={
                                    "label": "Large Load",
                                    "format": percent_format(1),
                                },
                            ),
                            "total_ulr": hx.Float(
                                mode="output",
                                view={
                                    "label": "Total Net LR",
                                    "format": percent_format(1),
                                },
                            ),
                            "experience_claims_cost": hx.Float(
                                mode="output",
                                view={
                                    "format": thousands_format(0),
                                },
                            ),
                            "net_benchmark_premium_pure_experience": hx.Float(
                                mode="output",
                                view={
                                    "format": thousands_format(0),
                                },
                            ),
                        }
                    ),
                    "experience_weighting_calculation": hx.Structure(
                        children={
                            "total_number_of_vessels": hx.Int(
                                mode="output",
                                view={
                                    "label": "Total Number of Vessels",
                                    "format": integer_format(0),
                                },
                            ),
                            "experience_weighting": hx.Float(
                                mode="output",
                                view={
                                    "label": "Experience Weighting",
                                    "format": percent_format(0),
                                },
                            ),
                        }
                    ),
                    "data_input_experience_table": hx.List(
                        mode="input",
                        fixed_element_count=constants.ship_building_experience_rating_years,
                        default_element_count=constants.ship_building_experience_rating_years,
                        async_input=["start_renewal_task"],
                        children={
                            "yoa": hx.Int(
                                mode="output",
                                async_input=["start_renewal_task"],
                                view={"label": "YOA", "format": integer_format(0)},
                            ),
                            "previous_insurer": hx.Str(
                                mode="override",
                                options=["Beazley", "Non-Beazley"],
                                async_input=["rarc_task"],
                                view={"label": "Previous Insurer"},
                            ),
                            "number_of_vessels": hx.Int(
                                mode="input",
                                default=None,
                                optionality="optional",
                                async_input=["rarc_task"],
                                view={
                                    "label": "Number of Vessels",
                                    "format": integer_format(0),
                                },
                            ),
                            "premium": hx.Float(
                                mode="override",
                                async_input=["rarc_task"],
                                view={"format": thousands_format(0)},
                            ),
                            "acquisition_cost": hx.Float(
                                mode="override",
                                async_input=["rarc_task"],
                                view={
                                    "label": "Acquisition Cost %",
                                    "format": percent_format(0),
                                },
                            ),
                            "net_premium_shared_line": hx.Float(
                                mode="output",
                                view={
                                    "format": thousands_format(0),
                                },
                            ),
                            "total_incurred_shared_line": hx.Float(
                                mode="override",
                                async_input=["rarc_task"],
                                view={
                                    "format": thousands_format(0),
                                },
                            ),
                            "att_incurred_shared_line": hx.Float(
                                mode="output",
                                view={
                                    "format": thousands_format(0),
                                },
                            ),
                            "large_incurred_shared_line": hx.Float(
                                mode="input",
                                default=None,
                                optionality="optional",
                                async_input=["rarc_task"],
                                view={
                                    "format": thousands_format(0),
                                },
                            ),
                            "signed_line": hx.Float(
                                mode="override",
                                async_input=["rarc_task"],
                                view={
                                    "label": "Signed Line %",
                                    "format": percent_format(0),
                                },
                            ),
                            "rate_change": hx.Float(
                                mode="override",
                                async_input=["rarc_task"],
                                view={
                                    "label": "Rate Change %",
                                    "format": percent_format(0),
                                },
                            ),
                            "is_include_year": hx.Bool(
                                mode="override",
                                async_input=["rarc_task"],
                                view={"label": "Year to Include?"},
                            ),
                        },
                    ),
                    "ulr_projection_experience_table": hx.List(
                        mode="input",
                        fixed_element_count=constants.ship_building_experience_rating_years
                        + 1,
                        default_element_count=constants.ship_building_experience_rating_years
                        + 1,
                        children={
                            "yoa": hx.Int(
                                mode="output",
                                view={"label": "YOA", "format": integer_format(0)},
                            ),
                            "net_premium": hx.Float(
                                mode="output",
                                view={
                                    "format": thousands_format(0),
                                    "group": "100% Share",
                                },
                            ),
                            "premium": hx.Float(
                                mode="output",
                                view={
                                    "format": thousands_format(0),
                                    "group": "100% Share",
                                },
                            ),
                            "att_incurred_shared_line": hx.Float(
                                mode="output",
                                view={
                                    "format": thousands_format(0),
                                    "group": "100% Share",
                                },
                            ),
                            "large_incurred_shared_line": hx.Float(
                                mode="output",
                                view={
                                    "format": thousands_format(0),
                                    "group": "100% Share",
                                },
                            ),
                            "rate_change": hx.Float(
                                mode="output",
                                view={
                                    "label": "Rate Change % - YOY",
                                    "format": percent_format(0),
                                    "group": "On-Levelled Position - As of Current Year",
                                },
                            ),
                            "rate_change_cumulative": hx.Float(
                                mode="output",
                                view={
                                    "label": "Rate Change % - Cumulative",
                                    "format": percent_format(0),
                                    "group": "On-Levelled Position - As of Current Year",
                                },
                            ),
                            "on_levelled_net_premium": hx.Float(
                                mode="output",
                                view={
                                    "format": thousands_format(0),
                                    "group": "On-Levelled Position - As of Current Year",
                                },
                            ),
                            "on_levelled_premium": hx.Float(
                                mode="output",
                                view={
                                    "format": thousands_format(0),
                                    "group": "On-Levelled Position - As of Current Year",
                                },
                            ),
                            "claims_inflation_yoy": hx.Float(
                                mode="output",
                                view={
                                    "label": "Claims Inflation - YOY",
                                    "format": percent_format(0),
                                    "group": "On-Levelled Position - As of Current Year",
                                },
                            ),
                            "claims_inflation_cumulative": hx.Float(
                                mode="output",
                                view={
                                    "label": "Claims Inflation - Cumulative",
                                    "format": percent_format(0),
                                    "group": "On-Levelled Position - As of Current Year",
                                },
                            ),
                            "on_levelled_att_incurred_shared_line": hx.Float(
                                mode="output",
                                view={
                                    "format": thousands_format(0),
                                    "group": "On-Levelled Position - As of Current Year",
                                },
                            ),
                            "on_levelled_att_incurred_lr": hx.Float(
                                mode="output",
                                view={
                                    "label": "On-Levelled Attritional Incurred LR",
                                    "format": percent_format(1),
                                    "group": "On-Levelled Position - As of Current Year",
                                },
                            ),
                            "on_levelled_large_incurred_shared_line": hx.Float(
                                mode="output",
                                view={
                                    "format": thousands_format(0),
                                    "group": "On-Levelled Position - As of Current Year",
                                },
                            ),
                            "on_levelled_large_incurred_lr": hx.Float(
                                mode="output",
                                view={
                                    "label": "On-Levelled Large Incurred LR",
                                    "format": percent_format(1),
                                    "group": "On-Levelled Position - As of Current Year",
                                },
                            ),
                            "development_month": hx.Int(
                                mode="output",
                                view={
                                    "label": "Development Month",
                                    "format": integer_format(0),
                                    "group": "Ultimate Position - Attritional",
                                },
                            ),
                            "development_percent": hx.Float(
                                mode="output",
                                view={
                                    "label": "Development %",
                                    "format": percent_format(0),
                                    "group": "Ultimate Position - Attritional",
                                },
                            ),
                            "attritional_ulr": hx.Float(
                                mode="output",
                                view={
                                    "label": "Attritional Net LR",
                                    "format": percent_format(1),
                                    "group": "Ultimate Position - Attritional",
                                },
                            ),
                            "is_include_year": hx.Int(
                                mode="output",
                                view={"label": "Years to Include?"},
                            ),
                        },
                    ),
                }
            )
        },
    )
