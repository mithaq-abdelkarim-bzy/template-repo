import hx_data_schema as hx
import data_schema.sch_utilities as utils


def output_vessel_details(coverage_type):
    if not coverage_type in ["iv", "war", "loh", "ship_building", "modelling"]:
        return {}

    base_common_fields = {
        coverage_type
        + "_benchmark_premium": hx.Float(
            mode="output",
            view={"label": "Benchmark Premium", "format": utils.thousands_format(0)},
        ),
    }

    result = {}

    if coverage_type in ["iv", "war", "modelling"]:
        result = {
            **base_common_fields,
            coverage_type
            + "_behavioural_model_rate": hx.Float(
                mode="output",
                view={
                    "label": "Static + Behavioural\nModel Rate (%)",
                    "format": utils.percent_format(2),
                },
            ),
            coverage_type
            + "_behavioural_benchmark_premium": hx.Float(
                mode="output",
                view={
                    "label": "Static + Behavioural\nBenchmark Premium (USD)",
                    "format": utils.thousands_format(0),
                },
            ),
            coverage_type
            + "_static_model_rate": hx.Float(
                mode="output",
                view={
                    "label": "Static Model Rate (%)",
                    "format": utils.percent_format(2),
                },
            ),
            coverage_type
            + "_static_benchmark_premium": hx.Float(
                mode="output",
                view={
                    "label": "Static Benchmark Premium (USD)",
                    "format": utils.thousands_format(0),
                },
            ),
            coverage_type
            + "_achieved_rate": hx.Float(
                mode="input",
                default=None,
                optionality="optional",
                view={
                    "label": "Achieved Rate (%)",
                    "format": utils.percent_format(6),
                    "options": {
                        "output_summary": {
                            "read_only": True,
                            "group": f"{coverage_type.capitalize()}",
                        }
                    },
                },
                validation={"min_value": 0},
                async_input=[
                    "generate_rating_summary_xlsx_task",
                    "rarc_task",
                    "push_vessels_to_datamart_task",
                ],
            ),
            coverage_type
            + "_achieved_premium": hx.Float(
                mode="output",
                async_input=["rarc_task", "generate_rating_summary_xlsx_task"],
                view={"label": "Achieved Premium", "format": utils.thousands_format(0)},
            ),
            coverage_type
            + "_uw_adjustment": hx.Float(
                mode="input",
                default=None,
                optionality="optional",
                async_input=["rarc_task"],
                view={
                    "label": "UW Adjustment",
                    "format": utils.percent_format(2),
                },
            ),
            coverage_type
            + "_is_include_vessel": hx.Bool(
                mode="input",
                default=True,
                view={"label": "Include Vessel"},
                async_input=[
                    "generate_rating_summary_xlsx_task",
                    "rarc_task",
                    "push_vessels_to_datamart_task",
                ],
            ),
        }
        if coverage_type == "iv" or coverage_type == "war":
            result = {
                **result,
                coverage_type
                + "_agreed_value": hx.Float(
                    mode="override",
                    view={
                        "label": "Agreed Value",
                        "format": utils.thousands_format(0),
                        "options": {
                            "output_summary": {
                                "read_only": True,
                                "group": f"{coverage_type.capitalize()}",
                            }
                        },
                    },
                    validation={"min_value": 0},
                    async_input=[
                        "generate_rating_summary_xlsx_task",
                        "rarc_task",
                        "push_vessels_to_datamart_task",
                    ],
                ),
            }
            if coverage_type == "iv":
                result = {
                    **result,
                    coverage_type
                    + "_coverage": hx.Str(
                        mode="input",
                        default="CL 290",
                        options_table="table_coverage_factor",
                        options_column="coverage",
                        view={
                            "label": "Coverage",
                            "options": {
                                "output_summary": {
                                    "read_only": True,
                                    "group": f"{coverage_type.capitalize()}",
                                }
                            },
                        },
                        async_input=["generate_rating_summary_xlsx_task", "rarc_task"],
                    ),
                    coverage_type
                    + "_deductible": hx.Float(
                        mode="override",
                        async_input=["rarc_task", "push_vessels_to_datamart_task"],
                        view={
                            "label": "Deductible",
                            "format": utils.thousands_format(0),
                        },
                        validation={"min_value": 0},
                    ),
                }
            else:
                result = {
                    **result,
                    coverage_type
                    + "_coverage": hx.Str(
                        mode="input",
                        default="CL 281",
                        options_table="table_coverage_factor",
                        options_column="coverage",
                        view={
                            "label": "Coverage",
                            "options": {
                                "output_summary": {
                                    "read_only": True,
                                    "group": f"{coverage_type.capitalize()}",
                                }
                            },
                        },
                        async_input=["generate_rating_summary_xlsx_task"],
                    ),
                }
        else:
            result = {
                **result,
                coverage_type
                + "_agreed_value": hx.Float(
                    mode="output",
                    view={"label": "Agreed Value", "format": utils.thousands_format(0)},
                    validation={"min_value": 0},
                ),
            }

    elif coverage_type == "loh":
        result = {
            **base_common_fields,
            coverage_type
            + "_number_of_vessels": hx.Int(
                mode="input",
                optionality="optional",
                default=None,
                async_input=["generate_rating_summary_xlsx_task", "rarc_task"],
                view={"label": "Number of Vessels", "format": utils.integer_format(0)},
                validation={"min_value": 0},
            ),
            coverage_type
            + "_agreed_value": hx.Float(
                mode="input",
                optionality="optional",
                default=None,
                view={"format": utils.thousands_format(0)},
                async_output=[
                    {
                        "task": "set_loh_vessels_defaults_task",
                        "reset": False,
                    },
                ],
                async_input=[
                    "generate_rating_summary_xlsx_task",
                    "set_loh_vessels_defaults_task",
                    "rarc_task",
                ],
                validation={"min_value": 0},
            ),
            coverage_type
            + "_achieved_premium": hx.Float(
                mode="input",
                optionality="optional",
                default=None,
                async_input=["rarc_task"],
                view={"label": "Achieved Premium", "format": utils.thousands_format(0)},
                validation={"min_value": 0},
            ),
            coverage_type
            + "_daily_rate": hx.Float(
                mode="input",
                default=None,
                optionality="optional",
                view={
                    "options": {"read_only_option": {"read_only": True}},
                    "format": utils.thousands_format(0),
                },
                async_output=[
                    {
                        "task": "set_loh_vessels_defaults_task",
                        "reset": False,
                    },
                ],
                async_input=[
                    "generate_rating_summary_xlsx_task",
                    "set_loh_vessels_defaults_task",
                    "rarc_task",
                ],
                validation={"min_value": 0},
            ),
            coverage_type
            + "_xs_days": hx.Int(
                mode="input",
                default=None,
                optionality="optional",
                options=utils.get_unique_keys_list("table_loh_base_rate", "xs_days"),
                view={
                    "options": {"read_only_option": {"read_only": True}},
                    "label": "XS (Days)",
                    "format": utils.integer_format(0),
                },
                async_output=[
                    {
                        "task": "set_loh_vessels_defaults_task",
                        "reset": False,
                    },
                ],
                async_input=[
                    "generate_rating_summary_xlsx_task",
                    "set_loh_vessels_defaults_task",
                    "rarc_task",
                    "push_vessels_to_datamart_task",
                ],
            ),
            coverage_type
            + "_cover": hx.Str(
                mode="input",
                optionality="optional",
                default=None,
                options=utils.get_unique_keys_list("table_loh_base_rate", "cover"),
                view={
                    "label": "Cover",
                    "options": {"read_only_option": {"read_only": True}},
                },
                async_output=[
                    {
                        "task": "set_loh_vessels_defaults_task",
                        "reset": False,
                    },
                ],
                async_input=[
                    "generate_rating_summary_xlsx_task",
                    "set_loh_vessels_defaults_task",
                    "rarc_task",
                ],
            ),
            coverage_type
            + "_conditions": hx.Str(
                mode="output",
                async_input=["generate_rating_summary_xlsx_task"],
                view={"label": "Conditions"},
            ),
            coverage_type
            + "_sum_insured": hx.Float(
                mode="output",
                async_input=["push_vessels_to_datamart_task"],
                view={"label": "Sum Insured", "format": utils.thousands_format(0)},
            ),
            coverage_type
            + "_vessel_base_rate": hx.Float(
                mode="output",
                async_input=["push_vessels_to_datamart_task"],
                view={
                    "label": " Gross Benchmark Rate %",
                    "format": utils.percent_format(6),
                },
            ),
            coverage_type
            + "_vessel_daily_rate": hx.Float(
                mode="output",
                view={"label": "Gross Benchmark Day Rate (per Vessel)", "format": {"mantissa": 2}},
            ),
            coverage_type
            + "_uw_adjustment": hx.Float(
                mode="input",
                default=None,
                optionality="optional",
                view={
                    "label": "UW Adjustment",
                    "format": utils.percent_format(1),
                },
                async_output=[
                    {
                        "task": "set_loh_vessels_defaults_task",
                        "reset": False,
                    },
                ],
                async_input=["set_loh_vessels_defaults_task", "rarc_task"],
                validation={"min_value": -0.5, "max_value": 2},
            ),
        }

    elif coverage_type == "ship_building":
        result = {
            **base_common_fields,
            coverage_type
            + "_vessel_type": hx.Str(
                mode="input",
                default=None,
                optionality="optional",
                options_table="ship_building_vessel_types",
                options_column="vessel_type",
                async_input=["rarc_task", "generate_rating_summary_xlsx_task"],
                view={
                    "label": "Vessel Type",
                },
            ),
            coverage_type
            + "_vessel_name": hx.Str(
                mode="input",
                default=None,
                optionality="optional",
                async_input=["rarc_task", "generate_rating_summary_xlsx_task"],
                view={
                    "label": "Vessel Name",
                },
            ),
            coverage_type
            + "_attachment_date": hx.Date(
                mode="input",
                default=None,
                optionality="optional",
                async_input=["rarc_task", "generate_rating_summary_xlsx_task"],
                view={
                    "label": "Attachment Date",
                },
            ),
            coverage_type
            + "_delivery_date": hx.Date(
                mode="input",
                default=None,
                optionality="optional",
                async_input=["rarc_task", "generate_rating_summary_xlsx_task"],
                view={
                    "label": "Delivery Date",
                },
            ),
            coverage_type
            + "_number_of_vessels": hx.Int(
                mode="input",
                default=None,
                optionality="optional",
                async_input=["rarc_task", "generate_rating_summary_xlsx_task"],
                view={
                    "label": "Number of Vessels",
                    "format": utils.integer_format(0),
                },
                validation={"min_value": 0},
            ),
            coverage_type
            + "_total_months_steel_cutting_keel_laying": hx.Float(
                mode="input",
                default=None,
                optionality="optional",
                async_input=["rarc_task", "generate_rating_summary_xlsx_task"],
                view={
                    "label": "Total Months Steel\nCutting-Keel Laying",
                    "format": {"mantissa": 3},
                },
                validation={"min_value": 0},
            ),
            coverage_type
            + "_total_months_keel_laying_launch": hx.Float(
                mode="input",
                default=None,
                optionality="optional",
                async_input=["rarc_task", "generate_rating_summary_xlsx_task"],
                view={
                    "label": "Total Months Keel\nLaying-Launch",
                    "format": {"mantissa": 3},
                },
                validation={"min_value": 0},
            ),
            coverage_type
            + "_total_months_launch_delivery": hx.Float(
                mode="input",
                default=None,
                optionality="optional",
                async_input=["rarc_task", "generate_rating_summary_xlsx_task"],
                view={
                    "label": "Total Months\nKeel Launch-Delivery",
                    "format": {"mantissa": 3},
                },
                validation={"min_value": 0},
            ),
            coverage_type
            + "_total_months_all_stages": hx.Float(
                mode="input",
                default=None,
                optionality="optional",
                async_input=["rarc_task", "generate_rating_summary_xlsx_task"],
                view={"label": "Total Months (All Stages)", "format": {"mantissa": 3}},
                validation={"min_value": 0},
            ),
            coverage_type
            + "_country": hx.Str(
                mode="input",
                default=None,
                options_table="ship_building_countries",
                options_column="country",
                optionality="optional",
                async_input=["rarc_task", "generate_rating_summary_xlsx_task"],
                view={
                    "label": "Country",
                },
            ),
            coverage_type
            + "_survey_grade": hx.Str(
                mode="input",
                default=None,
                optionality="optional",
                options_table="ship_building_survey_grade",
                options_column="grade",
                async_input=["rarc_task", "generate_rating_summary_xlsx_task"],
                view={
                    "label": "Survey Grade",
                },
            ),
            coverage_type
            + "_deductible": hx.Float(
                mode="input",
                default=None,
                optionality="optional",
                async_input=["rarc_task", "generate_rating_summary_xlsx_task"],
                view={
                    "label": "Deductible",
                    "format": utils.thousands_format(0),
                },
                validation={"min_value": 0},
            ),
            coverage_type
            + "_sum_insured": hx.Float(
                mode="input",
                default=None,
                optionality="optional",
                async_input=["rarc_task", "generate_rating_summary_xlsx_task"],
                view={"label": "Sum Insured", "format": utils.thousands_format(0)},
                validation={"min_value": 0},
            ),
            coverage_type
            + "_benchmark_rate": hx.Float(
                mode="output",
                async_input=["generate_rating_summary_xlsx_task"],
                view={
                    "label": "Benchmark rate\n(net brokerage)\nincl UW adj",
                    "format": utils.percent_format(3),
                },
            ),
        }

    return result
