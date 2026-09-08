import hx_data_schema as hx
import data_schema.sch_utilities as utils


def portfolio_metrics_async_tasks():
    return [
        {
            "task": "portfolio_analysis_search_task",
            "reset": True,
        },
        {
            "task": "clear_portfolio_analysis_search_task",
            "reset": True,
        },
    ]


def sch_portfolio_analysis(cds):
    cds.extend_node_rater_defined(
        "cds",
        {
            "portfolio_analysis": hx.Structure(
                children={
                    "hull_rating": hx.Structure(
                        children={
                            "exported_data": hx.File(
                                mode="output",
                                async_output=["generate_portfolio_analysis_excel"],
                                file_name="Portfolio_Analysis.xlsx",
                            ),
                            "filter_options": hx.Structure(
                                children={
                                    "effective_date": hx.Structure(
                                        children={
                                            "effective_date_from": hx.Date(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={"label": "Effective Date From"},
                                                async_input=[
                                                    "portfolio_analysis_search_task"
                                                ],
                                                async_output=[
                                                    "clear_portfolio_analysis_search_task"
                                                ],
                                            ),
                                            "effective_date_to": hx.Date(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={"label": "Effective Date To"},
                                                async_input=[
                                                    "portfolio_analysis_search_task"
                                                ],
                                                async_output=[
                                                    "clear_portfolio_analysis_search_task"
                                                ],
                                            ),
                                        }
                                    ),
                                    "insured": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={"label": "Insured"},
                                        async_input=["portfolio_analysis_search_task"],
                                        async_output=[
                                            "clear_portfolio_analysis_search_task"
                                        ],
                                    ),
                                    "policy_reference": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={"label": "Policy Section Reference"},
                                        async_input=["portfolio_analysis_search_task"],
                                        async_output=[
                                            "clear_portfolio_analysis_search_task"
                                        ],
                                    ),
                                    "status": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        options=[
                                            "Assessment Pending",
                                            "Rating",
                                            "Quoted",
                                            "Bound",
                                            "Post Bind Complete",
                                            "Declined",
                                            "Not Taken Up",
                                        ],
                                        view={"label": "Status"},
                                        async_input=["portfolio_analysis_search_task"],
                                        async_output=[
                                            "clear_portfolio_analysis_search_task"
                                        ],
                                    ),
                                    "agreed_value": hx.Structure(
                                        children={
                                            "agreed_value_from": hx.Float(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={
                                                    "label": "Agreed Value From",
                                                    "format": utils.thousands_format(0),
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task"
                                                ],
                                                async_output=[
                                                    "clear_portfolio_analysis_search_task"
                                                ],
                                            ),
                                            "agreed_value_to": hx.Float(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={
                                                    "label": "Agreed Value To",
                                                    "format": utils.thousands_format(0),
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task"
                                                ],
                                                async_output=[
                                                    "clear_portfolio_analysis_search_task"
                                                ],
                                            ),
                                        }
                                    ),
                                    "currency": hx.Str(
                                        mode="input",
                                        default=None,
                                        options_table="table_input_currency",
                                        options_column="ccy",
                                        optionality="optional",
                                        view={"label": "Currency"},
                                        async_input=["portfolio_analysis_search_task"],
                                        async_output=[
                                            "clear_portfolio_analysis_search_task"
                                        ],
                                    ),
                                    "has_policy_reference": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Has Policy Section Reference ?"
                                        },
                                        async_input=["portfolio_analysis_search_task"],
                                        async_output=[
                                            "clear_portfolio_analysis_search_task"
                                        ],
                                    ),
                                    "live_risk_entry": hx.Date(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={"label": "Live Risk entry"},
                                        async_input=["portfolio_analysis_search_task"],
                                        async_output=[
                                            "clear_portfolio_analysis_search_task"
                                        ],
                                    ),
                                    "imo": hx.Int(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "IMO",
                                            "format": utils.integer_format(0),
                                        },
                                        async_input=["portfolio_analysis_search_task"],
                                        async_output=[
                                            "clear_portfolio_analysis_search_task"
                                        ],
                                    ),
                                    "gross_tonnage": hx.Structure(
                                        children={
                                            "gross_tonnage_from": hx.Float(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={
                                                    "label": "Gross Tonnage From",
                                                    "format": utils.integer_format(0),
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task"
                                                ],
                                                async_output=[
                                                    "clear_portfolio_analysis_search_task"
                                                ],
                                            ),
                                            "gross_tonnage_to": hx.Float(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={
                                                    "label": "Gross Tonnage To",
                                                    "format": utils.integer_format(0),
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task"
                                                ],
                                                async_output=[
                                                    "clear_portfolio_analysis_search_task"
                                                ],
                                            ),
                                        }
                                    ),
                                    "flag": hx.Str(
                                        mode="input",
                                        default=None,
                                        options_table="table_flags",
                                        options_column="vessel_flag",
                                        optionality="optional",
                                        view={"label": "Flag"},
                                        async_input=["portfolio_analysis_search_task"],
                                        async_output=[
                                            "clear_portfolio_analysis_search_task"
                                        ],
                                    ),
                                    "broker": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={"label": "Broker"},
                                        async_input=["portfolio_analysis_search_task"],
                                        async_output=[
                                            "clear_portfolio_analysis_search_task"
                                        ],
                                    ),
                                    "operator_domicile": hx.Str(
                                        mode="input",
                                        default=None,
                                        options_table="table_flags",
                                        options_column="vessel_flag",
                                        optionality="optional",
                                        view={"label": "Operator Domicile"},
                                        async_input=["portfolio_analysis_search_task"],
                                        async_output=[
                                            "clear_portfolio_analysis_search_task"
                                        ],
                                    ),
                                    "year_built": hx.Structure(
                                        children={
                                            "year_built_from": hx.Int(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={
                                                    "label": "Year of Build From",
                                                    "format": utils.integer_format(0),
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task"
                                                ],
                                                async_output=[
                                                    "clear_portfolio_analysis_search_task"
                                                ],
                                            ),
                                            "year_built_to": hx.Int(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={
                                                    "label": "Year of Build To",
                                                    "format": utils.integer_format(0),
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task"
                                                ],
                                                async_output=[
                                                    "clear_portfolio_analysis_search_task"
                                                ],
                                            ),
                                        }
                                    ),
                                    "vessel_class": hx.Str(
                                        mode="input",
                                        default=None,
                                        options_table="table_vessel_classifications",
                                        options_column="classification_society",
                                        optionality="optional",
                                        view={"label": "Class"},
                                        async_input=["portfolio_analysis_search_task"],
                                        async_output=[
                                            "clear_portfolio_analysis_search_task"
                                        ],
                                    ),
                                    "coverage": hx.Str(
                                        mode="input",
                                        default=None,
                                        options_table="table_coverage_factor",
                                        options_column="coverage",
                                        optionality="optional",
                                        view={"label": "Coverage"},
                                        async_input=["portfolio_analysis_search_task"],
                                        async_output=[
                                            "clear_portfolio_analysis_search_task"
                                        ],
                                    ),
                                    "dwt": hx.Structure(
                                        children={
                                            "dwt_from": hx.Float(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={
                                                    "label": "DWT From",
                                                    "format": utils.integer_format(0),
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task"
                                                ],
                                                async_output=[
                                                    "clear_portfolio_analysis_search_task"
                                                ],
                                            ),
                                            "dwt_to": hx.Float(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={
                                                    "label": "DWT To",
                                                    "format": utils.integer_format(0),
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task"
                                                ],
                                                async_output=[
                                                    "clear_portfolio_analysis_search_task"
                                                ],
                                            ),
                                        }
                                    ),
                                    "vessel_type": hx.Str(
                                        mode="input",
                                        default=None,
                                        options_table="table_vessel_types",
                                        options_column="vessel_type",
                                        optionality="optional",
                                        view={"label": "Vessel Type"},
                                        async_input=["portfolio_analysis_search_task"],
                                        async_output=[
                                            "clear_portfolio_analysis_search_task"
                                        ],
                                    ),
                                    "follow_lead": hx.Str(
                                        mode="input",
                                        default=None,
                                        options=["Follow", "Lead"],
                                        optionality="optional",
                                        view={"label": "Follow/Lead"},
                                        async_input=["portfolio_analysis_search_task"],
                                        async_output=[
                                            "clear_portfolio_analysis_search_task"
                                        ],
                                    ),
                                }
                            ),
                            "portfolio_metrics": hx.Structure(
                                children={
                                    "vessels_count": hx.Int(
                                        mode="output",
                                        view={
                                            "label": "Vessels Count",
                                            "format": utils.integer_format(0),
                                        },
                                        async_input=[
                                            "portfolio_analysis_search_task",
                                            "generate_portfolio_analysis_excel",
                                        ],
                                        async_output=portfolio_metrics_async_tasks(),
                                    ),
                                    "average_agreed_value": hx.Float(
                                        mode="output",
                                        view={
                                            "format": utils.thousands_format(0),
                                        },
                                        async_input=[
                                            "portfolio_analysis_search_task",
                                            "generate_portfolio_analysis_excel",
                                        ],
                                        async_output=portfolio_metrics_async_tasks(),
                                    ),
                                    "average_achieved_rate": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Average Achieved Rate",
                                            "format": utils.percent_format(2),
                                        },
                                        async_input=[
                                            "portfolio_analysis_search_task",
                                            "generate_portfolio_analysis_excel",
                                        ],
                                        async_output=portfolio_metrics_async_tasks(),
                                    ),
                                    "vessels": hx.List(
                                        mode="output",
                                        async_output=portfolio_metrics_async_tasks(),
                                        async_input=[
                                            "portfolio_analysis_search_task",
                                            "generate_portfolio_analysis_excel",
                                        ],
                                        children={
                                            "id": hx.Int(
                                                mode="output",
                                                view={
                                                    "label": "Id",
                                                    "format": utils.integer_format(0),
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "imo": hx.Int(
                                                mode="output",
                                                view={
                                                    "label": "IMO",
                                                    "format": utils.integer_format(0),
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "insured": hx.Str(
                                                mode="output",
                                                view={"label": "Insured"},
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "policy_reference": hx.Str(
                                                mode="output",
                                                view={
                                                    "label": "Policy Section Reference"
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "effective_date": hx.Date(
                                                mode="output",
                                                view={"label": "Effective Date"},
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "expiry_date": hx.Date(
                                                mode="output",
                                                view={"label": "Expiry Date"},
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "coverage": hx.Str(
                                                mode="output",
                                                view={"label": "Coverage"},
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "original_agreed_value": hx.Float(
                                                mode="output",
                                                view={
                                                    "label": "Original Agreed Value",
                                                    "format": utils.thousands_format(0),
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "original_currency": hx.Str(
                                                mode="output",
                                                view={"label": "Original Currency"},
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "agreed_value_converted": hx.Float(
                                                mode="output",
                                                view={
                                                    "format": utils.thousands_format(0)
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "vessel_type": hx.Str(
                                                mode="output",
                                                view={"label": "Vessel Type"},
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "gross_tonnage": hx.Int(
                                                mode="output",
                                                view={
                                                    "label": "Gross Tonnage",
                                                    "format": utils.integer_format(0),
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "dwt": hx.Int(
                                                mode="output",
                                                view={
                                                    "label": "DWT",
                                                    "format": utils.integer_format(0),
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "year_built": hx.Int(
                                                mode="output",
                                                view={
                                                    "label": "Year Built",
                                                    "format": utils.integer_format(0),
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "flag": hx.Str(
                                                mode="output",
                                                view={"label": "Flag"},
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "classification": hx.Str(
                                                mode="output",
                                                view={"label": "Classification"},
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "achieved_rate": hx.Float(
                                                mode="output",
                                                view={
                                                    "label": "Achieved Rate",
                                                    "format": utils.percent_format(2),
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "order_percent": hx.Float(
                                                mode="output",
                                                view={
                                                    "label": "Order %",
                                                    "format": utils.percent_format(0),
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "written_line_percent": hx.Float(
                                                mode="output",
                                                view={
                                                    "label": "Written Line %",
                                                    "format": utils.percent_format(2),
                                                },
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "operator_domicile": hx.Str(
                                                mode="output",
                                                view={"label": "Operator Domicile"},
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "broker": hx.Str(
                                                mode="output",
                                                view={"label": "Broker"},
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "follow_lead": hx.Str(
                                                mode="output",
                                                view={"label": "Follow Lead"},
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "vessel_name": hx.Str(
                                                mode="output",
                                                view={"label": "Vessel Name"},
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                            "type_abrv": hx.Str(
                                                mode="output",
                                                view={"label": "Type Abrv"},
                                                async_input=[
                                                    "portfolio_analysis_search_task",
                                                    "generate_portfolio_analysis_excel",
                                                ],
                                                async_output=portfolio_metrics_async_tasks(),
                                            ),
                                        },
                                    ),
                                }
                            ),
                        }
                    )
                }
            )
        },
    )
