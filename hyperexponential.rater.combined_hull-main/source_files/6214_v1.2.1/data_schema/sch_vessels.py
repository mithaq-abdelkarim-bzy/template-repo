import hx_data_schema as hx
import data_schema.sch_utilities as utils
import data_schema.helpers.sch_common as common
import data_schema.helpers.modelling_helper as modelling_helper


def common_fleet_average_relativity_fields():
    return {
        "base": hx.Float(
            mode="output",
            view={
                "label": "Base",
            },
        ),
        "fleet_size": hx.Float(
            mode="output",
            view={
                "label": "Fleet Size",
            },
        ),
        "year_built": hx.Float(
            mode="output",
            view={
                "label": "Year Built",
            },
        ),
        "frequency_vessel_type": hx.Float(
            mode="output",
            view={
                "label": "Claims Frequency Vessel Type",
            },
        ),
        "flag": hx.Float(
            mode="output",
            view={
                "label": "Flag",
            },
        ),
        "frequency_dwt": hx.Float(
            mode="output",
            view={
                "label": "Claims Frequency DWT",
            },
        ),
        "base_x_year_x_value": hx.Float(
            mode="output",
            view={
                "label": "Base x Year x Value",
            },
        ),
        "severity_vessel_type": hx.Float(
            mode="output",
            view={
                "label": "Claims Severity Vessel Type",
            },
        ),
        "severity_dwt": hx.Float(
            mode="output",
            view={
                "label": "Claims Severity DWT",
            },
        ),
    }


def sch_vessels(cds):
    loh_prefix = "loh_"
    ship_building_prefix = "ship_building_"
    ship_building_pricing_prefix = "ship_building_pricing_"
    vessels_validation_prefix = "validation_"
    iv_validation_prefix = "validation_iv_"
    war_validation_prefix = "validation_war_"
    cds.override_node_properties(
        "cds/standard_fields/inception_date",
        {
            "async_input": [
                "set_vessels_defaults_task",
                "populate_bi_data",
                "push_vessels_to_datamart_task",
            ]
        },
    )
    cds.override_node_properties(
        "cds/standard_fields/expiry_date",
        {"async_input": ["set_vessels_defaults_task", "push_vessels_to_datamart_task"]},
    )
    cds.extend_node_rater_defined(
        "cds/exposure/aggregate",
        {
            "average_build_year": hx.Float(
                mode="output",
                view={
                    "label": "Average Build Year",
                    "format": utils.integer_format(0),
                },
            )
        },
    )
    cds.extend_node_rater_defined(
        "cds/exposure/granular",
        {
            "vessels": hx.Structure(
                children={
                    "vessels_defaults": hx.Structure(
                        children={
                            "hull": hx.Structure(
                                children={
                                    "inception_date": hx.Date(
                                        mode="override",
                                        async_input=["set_vessels_defaults_task"],
                                        view={
                                            "label": "Inception Date",
                                        },
                                    ),
                                    "expiry_date": hx.Date(
                                        mode="override",
                                        async_input=["set_vessels_defaults_task"],
                                        view={
                                            "label": "Expiry Date",
                                        },
                                    ),
                                    "freight_conditions": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_table="table_freight_conditions",
                                        options_column="freight_conditions",
                                        default="Average",
                                        view={"label": "Freight Conditions"},
                                        async_input=["set_vessels_defaults_task"],
                                    ),
                                    "vessel_quality": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_table="table_vessel_quality",
                                        options_column="vessel_quality",
                                        default="Average",
                                        view={"label": "Vessel/Mach. Quality"},
                                        async_input=["set_vessels_defaults_task"],
                                    ),
                                    "area_of_operation": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_table="table_area_of_operation",
                                        options_column="area_of_operation",
                                        default="Average",
                                        view={"label": "Area of Operation"},
                                        async_input=["set_vessels_defaults_task"],
                                    ),
                                    "coverage": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        default=None,
                                        options_table="table_coverage_factor",
                                        options_column="coverage",
                                        view={"label": "Coverage"},
                                        async_input=["set_vessels_defaults_task"],
                                    ),
                                    "deductible": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Deductible",
                                            "format": utils.thousands_format(0),
                                        },
                                        validation={"min_value": 0},
                                        async_input=["set_vessels_defaults_task"],
                                    ),
                                    "order_percent": hx.Float(
                                        mode="input",
                                        default=1,
                                        optionality="optional",
                                        view={
                                            "label": "Order",
                                            "format": utils.percent_format(2),
                                        },
                                        async_input=["set_vessels_defaults_task"],
                                        validation={"min_value": 0, "max_value": 1},
                                    ),
                                }
                            ),
                            "loh": hx.Structure(
                                children={
                                    loh_prefix
                                    + "vessel_type": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        options_table="table_vessel_types",
                                        options_column="vessel_type",
                                        view={
                                            "label": "Type",
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                        },
                                        async_input=["set_loh_vessels_defaults_task"],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    loh_prefix
                                    + "year_built": hx.Int(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Year built",
                                            "format": {"thousandSeparated": False},
                                        },
                                        async_input=["set_loh_vessels_defaults_task"],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            }
                                        ],
                                        validation={"min_value": 0},
                                    ),
                                    loh_prefix
                                    + "gross_tonnage": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Gross Tonnage",
                                            "format": utils.thousands_format(0),
                                        },
                                        async_input=["set_loh_vessels_defaults_task"],
                                        validation={"min_value": 0},
                                    ),
                                    loh_prefix
                                    + "agreed_value": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Hull Value (USD)",
                                            "format": utils.thousands_format(0),
                                        },
                                        async_input=["set_loh_vessels_defaults_task"],
                                        validation={"min_value": 0},
                                    ),
                                    loh_prefix
                                    + "daily_rate": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "format": utils.thousands_format(0),
                                        },
                                        async_input=["set_loh_vessels_defaults_task"],
                                        validation={"min_value": 0},
                                    ),
                                    loh_prefix
                                    + "xs_days": hx.Int(
                                        mode="input",
                                        default=None,
                                        options=utils.get_unique_keys_list(
                                            "table_loh_base_rate", "xs_days"
                                        ),
                                        optionality="optional",
                                        view={
                                            "label": "XS (Days)",
                                            "format": utils.integer_format(0),
                                        },
                                        async_input=["set_loh_vessels_defaults_task"],
                                    ),
                                    loh_prefix
                                    + "cover": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        default=None,
                                        options=utils.get_unique_keys_list(
                                            "table_loh_base_rate", "cover"
                                        ),
                                        view={
                                            "label": "Cover",
                                        },
                                        async_input=["set_loh_vessels_defaults_task"],
                                    ),
                                    loh_prefix
                                    + "uw_adjustment": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "UW Adjustment",
                                            "format": utils.percent_format(2),
                                        },
                                        async_input=["set_loh_vessels_defaults_task"],
                                    ),
                                }
                            ),
                        }
                    ),
                    "loh_rating": hx.Structure(
                        children={
                            "data_mart_temp_vessels_list": hx.List(
                                mode="input",
                                async_input=["push_vessels_to_datamart_task"],
                                async_output=[
                                    {
                                        "task": "push_vessels_to_datamart_task",
                                        "reset": False,
                                    }
                                ],
                                children={
                                    loh_prefix
                                    + "unique_identifier": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    loh_prefix
                                    + "imo": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    loh_prefix
                                    + "name": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    loh_prefix
                                    + "vessel_type": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    loh_prefix
                                    + "year_built": hx.Int(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    loh_prefix
                                    + "dwt": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),

                                    loh_prefix
                                    + "inception_date": hx.Date(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    loh_prefix
                                    + "expiry_date": hx.Date(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    loh_prefix
                                    + "xs_days": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    loh_prefix
                                    + "sum_insured": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    loh_prefix
                                    + "vessel_achieved_rate": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    loh_prefix
                                    + "policy_reference": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    loh_prefix
                                    + "written_line": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    loh_prefix
                                    + "currency": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    # loh_prefix
                                    # + "is_renewal": hx.Int(
                                    #     mode="input",
                                    #     default=None,
                                    #     optionality="optional",
                                    #     async_input=["push_vessels_to_datamart_task"],
                                    #     async_output=[
                                    #         {
                                    #             "task": "push_vessels_to_datamart_task",
                                    #             "reset": False,
                                    #         }
                                    #     ],
                                    # ),
                                },
                            ),
                            loh_prefix
                            + "vessels_list": hx.List(
                                mode="input",
                                async_output=[
                                    "clear_loh_vessels_task",
                                    {"task": "rarc_task", "reset": False},
                                ],
                                async_input=[
                                    "lookup_loh_imos_task",
                                    "start_renewal_task",
                                    "generate_rating_summary_xlsx_task",
                                ],
                                children={
                                    loh_prefix
                                    + "unique_identifier": hx.Str(
                                        mode="output",
                                        async_input=[
                                            "rarc_task",
                                            "push_vessels_to_datamart_task",
                                        ],
                                    ),
                                    loh_prefix
                                    + "vessel_achieved_rate": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Achieved Rate %",
                                            "format": utils.percent_format(6)
                                        },
                                        async_input=[
                                            "push_vessels_to_datamart_task",
                                            "generate_rating_summary_xlsx_task",
                                            "rarc_task",
                                        ],
                                        validation={"min_value": 0},
                                    ),   
                                    loh_prefix
                                    + "vessel_details": hx.Structure(
                                        children={
                                            loh_prefix
                                            + "imo": hx.Str(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={
                                                    "label": "IMO",
                                                    "options": {
                                                        "read_only_option": {
                                                            "read_only": True
                                                        }
                                                    },
                                                },
                                                async_input=[
                                                    "lookup_loh_imos_task",
                                                    "rarc_task",
                                                    "generate_rating_summary_xlsx_task",
                                                    "push_vessels_to_datamart_task",
                                                ],
                                            ),
                                            loh_prefix
                                            + "name": hx.Str(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={
                                                    "label": "Vessel Name",
                                                    "options": {
                                                        "read_only_option": {
                                                            "read_only": True
                                                        }
                                                    },
                                                },
                                                async_output=[
                                                    {
                                                        "task": "lookup_loh_imos_task",
                                                        "reset": False,
                                                    },
                                                ],
                                                async_input=[
                                                    "rarc_task",
                                                    "generate_rating_summary_xlsx_task",
                                                    "push_vessels_to_datamart_task",
                                                ],
                                            ),
                                            loh_prefix
                                            + "vessel_type": hx.Str(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                options_table="table_vessel_types",
                                                options_column="vessel_type",
                                                view={"label": "Type"},
                                                async_input=[
                                                    "generate_rating_summary_xlsx_task",
                                                    "rarc_task",
                                                    "push_vessels_to_datamart_task",
                                                ],
                                                async_output=[
                                                    {
                                                        "task": "lookup_loh_imos_task",
                                                        "reset": False,
                                                    },
                                                    {
                                                        "task": "set_loh_vessels_defaults_task",
                                                        "reset": False,
                                                    },
                                                ],
                                            ),
                                            loh_prefix
                                            + "year_built": hx.Int(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={
                                                    "label": "Build Year",
                                                    "format": utils.integer_format(0),
                                                },
                                                async_input=[
                                                    "generate_rating_summary_xlsx_task",
                                                    "rarc_task",
                                                    "push_vessels_to_datamart_task",
                                                ],
                                                async_output=[
                                                    {
                                                        "task": "set_loh_vessels_defaults_task",
                                                        "reset": False,
                                                    },
                                                    {
                                                        "task": "lookup_loh_imos_task",
                                                        "reset": False,
                                                    },
                                                ],
                                                validation={"min_value": 0},
                                            ),
                                            loh_prefix
                                            + "gross_tonnage": hx.Float(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={
                                                    "label": "Gross Tonnage",
                                                    "format": utils.thousands_format(0),
                                                },
                                                async_input=[
                                                    "generate_rating_summary_xlsx_task",
                                                    "rarc_task",
                                                    "push_vessels_to_datamart_task",
                                                ],
                                                async_output=[
                                                    {
                                                        "task": "lookup_loh_imos_task",
                                                        "reset": False,
                                                    },
                                                    {
                                                        "task": "set_loh_vessels_defaults_task",
                                                        "reset": False,
                                                    },
                                                ],
                                                validation={"min_value": 0},
                                            ),
                                            loh_prefix
                                            + "dwt": hx.Float(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={
                                                    "label": "DWT",
                                                    "format": utils.thousands_format(0),
                                                },
                                                async_input=[
                                                    "push_vessels_to_datamart_task",
                                                    "generate_rating_summary_xlsx_task",
                                                    "rarc_task",
                                                ],
                                                async_output=[
                                                    {
                                                        "task": "lookup_loh_imos_task",
                                                        "reset": False,
                                                    },
                                                ],
                                                validation={"min_value": 0},
                                            )                                     
                                            
                                        },
                                    ),
                                    **common.output_vessel_details("loh"),
                                },
                            ),
                        }
                    ),
                    "ship_building_rating": hx.Structure(
                        children={
                            ship_building_prefix
                            + "vessels_list": hx.List(
                                mode="input",
                                async_output=[
                                    {
                                        "task": "ship_building_number_of_vessels_task",
                                        "reset": False,
                                    },
                                    {"task": "rarc_task", "reset": False},
                                ],
                                async_input=["ship_building_number_of_vessels_task"],
                                children={
                                    "ship_building_index": hx.Int(
                                        mode="output",
                                        async_input=["rarc_task"],
                                    ),
                                    **common.output_vessel_details("ship_building"),
                                },
                            ),
                            ship_building_pricing_prefix
                            + "vessels_list": hx.List(
                                mode="output",
                                children={
                                    ship_building_pricing_prefix
                                    + "overall_process_base_rate": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Overall Process Base Rate",
                                            "format": utils.percent_format(2),
                                        },
                                    ),
                                    ship_building_pricing_prefix
                                    + "base_rate_steel_cutting_keel_laying": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Steel Cutting and Keel Lay - Base Rate",
                                            "format": utils.percent_format(2),
                                        },
                                    ),
                                    ship_building_pricing_prefix
                                    + "base_rate_keel_laying_launch": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Launch -Base Rate",
                                            "format": utils.percent_format(2),
                                        },
                                    ),
                                    ship_building_pricing_prefix
                                    + "base_rate_launch_delivery": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Delivery- Base Rate",
                                            "format": utils.percent_format(2),
                                        },
                                    ),
                                    ship_building_pricing_prefix
                                    + "base_rate_non_war": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Base rate (non-war)",
                                            "format": utils.percent_format(2),
                                        },
                                    ),
                                    ship_building_pricing_prefix
                                    + "vessel_type": hx.Str(
                                        mode="output",
                                        view={
                                            "label": "Type of Vessel",
                                            "format": utils.percent_format(0),
                                        },
                                    ),
                                    ship_building_pricing_prefix
                                    + "country": hx.Str(
                                        mode="output",
                                        view={
                                            "label": "Country",
                                            "format": utils.percent_format(0),
                                        },
                                    ),
                                    ship_building_pricing_prefix
                                    + "survey_grade": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Survey Grade",
                                            "format": utils.percent_format(0),
                                        },
                                    ),
                                    ship_building_pricing_prefix
                                    + "deductible": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Deductible",
                                            "format": utils.percent_format(0),
                                        },
                                    ),
                                    ship_building_pricing_prefix
                                    + "non_war_premium_net_rate": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Non-war premium net rate",
                                            "format": utils.percent_format(3),
                                        },
                                    ),
                                    ship_building_pricing_prefix
                                    + "war_premium_net_rate": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "War premium net rate",
                                            "format": utils.percent_format(3),
                                        },
                                    ),
                                    ship_building_pricing_prefix
                                    + "total_exposure_net_rate_pre_fleet": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Total exposure net rate (pre fleet discount)",
                                            "format": utils.percent_format(3),
                                        },
                                    ),
                                    ship_building_pricing_prefix
                                    + "fleet_discount": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Fleet discount",
                                            "format": utils.percent_format(0),
                                        },
                                    ),
                                    ship_building_pricing_prefix
                                    + "total_exposure_net_rate": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Total exposure net rate",
                                            "format": utils.percent_format(3),
                                        },
                                    ),
                                    ship_building_pricing_prefix
                                    + "exposure_net_premium": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Exposure net premium",
                                            "format": utils.thousands_format(0),
                                        },
                                    ),
                                },
                            ),
                        }
                    ),
                    "hull_rating": hx.Structure(
                        children={
                            "output_summary_xlsx": hx.File(
                                mode="output",
                                async_output=[
                                    "generate_rating_summary_xlsx_task",
                                ],
                                file_name="output_summary.xlsx",
                            ),
                            "vessels_xlsx": hx.File(
                                mode="output",
                                async_output=["generate_vessels_xlsx_task"],
                                file_name="vessels.xlsx",
                            ),
                            "is_modelling": hx.Bool(
                                mode="input",
                                default=False,
                                view={"label": "Show Actuarial Pricing"},
                            ),
                            "fleet_size": hx.Int(mode = "output", 
                                view = {"label": "Fleet Size", 
                                "format": utils.thousands_format(0)}),
                            "fleet_soft_factors": hx.Structure(
                                children={
                                    "fleet_casualty_history": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_table="table_fleet_casualty_history",
                                        options_column="fleet_casualty_history",
                                        default="Average",
                                        async_input=[
                                            "generate_vessels_xlsx_task",
                                            "generate_rating_summary_xlsx_task",
                                            "rarc_task",
                                        ],
                                        view={"label": "Fleet Casualty History"},
                                    ),
                                    "owner_quality": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_table="table_owner_quality",
                                        options_column="owner_quality",
                                        default="Average",
                                        async_input=[
                                            "generate_vessels_xlsx_task",
                                            "generate_rating_summary_xlsx_task",
                                            "rarc_task",
                                        ],
                                        view={"label": "Owner/Manager Quality"},
                                    ),
                                }
                            ),
                            "operator_domicile": hx.Str(
                                mode="input",
                                optionality="optional",
                                options_table="table_flags",
                                options_column="vessel_flag",
                                default=None,
                                async_input=[
                                    "generate_vessels_xlsx_task",
                                    "generate_rating_summary_xlsx_task",
                                ],
                                view={"label": "Operator Domicile"},
                            ),
                            "fleet_average_relativity": hx.Structure(
                                children={
                                    "static": hx.Structure(
                                        children={
                                            **common_fleet_average_relativity_fields(),
                                        }
                                    ),
                                    "behavioural": hx.Structure(
                                        children={
                                            **common_fleet_average_relativity_fields(),
                                            "max_distance_ratio": hx.Float(
                                                mode="output",
                                                view={
                                                    "label": "Max Distance Ratio",
                                                },
                                            ),
                                            "perc_time_eez": hx.Float(
                                                mode="output",
                                                view={
                                                    "label": "Time EEZ",
                                                },
                                            ),
                                            "ratio_moving": hx.Float(
                                                mode="output",
                                                view={
                                                    "label": "Ratio Moving",
                                                },
                                            ),
                                            "ratio_moored": hx.Float(
                                                mode="output",
                                                view={
                                                    "label": "Ratio Moored",
                                                },
                                            ),
                                            "number_of_unique_port_visits": hx.Float(
                                                mode="output",
                                                view={
                                                    "label": "Number of Unique Port Visits",
                                                },
                                            ),
                                        }
                                    ),
                                },
                            ),
                            "data_mart_temp_vessels_list": hx.List(
                                mode="input",
                                async_input=["push_vessels_to_datamart_task"],
                                async_output=[
                                    {
                                        "task": "push_vessels_to_datamart_task",
                                        "reset": False,
                                    }
                                ],
                                children={
                                    "imo": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "name": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "vessel_type": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "year_built": hx.Int(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "dwt": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "order_percent": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "inception_date": hx.Date(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "expiry_date": hx.Date(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "deductible": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "agreed_value": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "achieved_rate": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "hull_written_line": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "hull_policy_reference": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "iv_written_line": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "iv_agreed_value": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "iv_achieved_rate": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "iv_deductible": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "iv_policy_reference": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "war_written_line": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "war_agreed_value": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "war_achieved_rate": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "war_policy_reference": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "currency": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=["push_vessels_to_datamart_task"],
                                        async_output=[
                                            {
                                                "task": "push_vessels_to_datamart_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    # "is_renewal": hx.Int(
                                    #     mode="input",
                                    #     default=None,
                                    #     optionality="optional",
                                    #     async_input=["push_vessels_to_datamart_task"],
                                    #     async_output=[
                                    #         {
                                    #             "task": "push_vessels_to_datamart_task",
                                    #             "reset": False,
                                    #         }
                                    #     ],
                                    # )
                                },
                            ),
                            "vessels_list": hx.List(
                                mode="input",
                                async_input=[
                                    "lookup_imos_task",
                                    "generate_rating_summary_xlsx_task",
                                    "generate_vessels_xlsx_task",
                                    "rarc_task",
                                    "push_vessels_to_datamart_task",
                                ],
                                async_output=[
                                    "clear_vessels_task",
                                    {"task": "rarc_task", "reset": False},
                                ],
                                children={
                                    "has_error": hx.Bool(mode="output"),
                                    "error_validation_columns": hx.Structure(
                                        children={
                                            vessels_validation_prefix
                                            + "name": hx.Str(mode="output"),
                                            vessels_validation_prefix
                                            + "inception_date": hx.Str(mode="output"),
                                            vessels_validation_prefix
                                            + "expiry_date": hx.Str(mode="output"),
                                            vessels_validation_prefix
                                            + "vessel_type": hx.Str(mode="output"),
                                            vessels_validation_prefix
                                            + "gross_tonnage": hx.Str(mode="output"),
                                            vessels_validation_prefix
                                            + "dwt": hx.Str(mode="output"),
                                            vessels_validation_prefix
                                            + "year_built": hx.Str(mode="output"),
                                            vessels_validation_prefix
                                            + "flag": hx.Str(mode="output"),
                                            vessels_validation_prefix
                                            + "vessel_class": hx.Str(mode="output"),
                                            vessels_validation_prefix
                                            + "order_percent": hx.Str(mode="output"),
                                            vessels_validation_prefix
                                            + "freight_conditions": hx.Str(
                                                mode="output"
                                            ),
                                            vessels_validation_prefix
                                            + "vessel_quality": hx.Str(mode="output"),
                                            vessels_validation_prefix
                                            + "area_of_operation": hx.Str(
                                                mode="output"
                                            ),
                                            vessels_validation_prefix
                                            + "coverage": hx.Str(mode="output"),
                                            vessels_validation_prefix
                                            + "agreed_value": hx.Str(mode="output"),
                                            vessels_validation_prefix
                                            + "deductible": hx.Str(mode="output"),
                                            vessels_validation_prefix
                                            + "achieved_rate": hx.Str(mode="output"),
                                        }
                                    ),
                                    "vessel_details": hx.Structure(
                                        children={
                                            "imo": hx.Str(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={
                                                    "label": "IMO",
                                                    "options": {
                                                        "read_only_option": {
                                                            "read_only": True
                                                        }
                                                    },
                                                },
                                                async_input=[
                                                    "lookup_imos_task",
                                                    "generate_rating_summary_xlsx_task",
                                                    "generate_vessels_xlsx_task",
                                                    "rarc_task",
                                                    "push_vessels_to_datamart_task",
                                                ],
                                            ),
                                            "name": hx.Str(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={
                                                    "label": "Name",
                                                    "options": {
                                                        "read_only_option": {
                                                            "read_only": True
                                                        }
                                                    },
                                                },
                                                async_input=[
                                                    "rarc_task",
                                                    "generate_rating_summary_xlsx_task",
                                                    "generate_vessels_xlsx_task",
                                                    "push_vessels_to_datamart_task",
                                                ],
                                                async_output=[
                                                    {
                                                        "task": "lookup_imos_task",
                                                        "reset": False,
                                                    }
                                                ],
                                            ),
                                            "gross_tonnage": hx.Float(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                view={
                                                    "label": "Gross Tonnage",
                                                    "format": utils.thousands_format(0),
                                                    "options": {
                                                        "read_only_option": {
                                                            "read_only": True
                                                        }
                                                    },
                                                },
                                                async_input=[
                                                    "generate_vessels_xlsx_task",
                                                    "generate_rating_summary_xlsx_task",
                                                    "rarc_task",
                                                ],
                                                async_output=[
                                                    {
                                                        "task": "set_vessels_defaults_task",
                                                        "reset": False,
                                                    },
                                                    {
                                                        "task": "lookup_imos_task",
                                                        "reset": False,
                                                    },
                                                ],
                                                validation={"min_value": 0},
                                            ),
                                            "vessel_class": hx.Str(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                options_table="table_vessel_classifications",
                                                options_column="classification_society",
                                                async_input=[
                                                    "rarc_task",
                                                    "generate_vessels_xlsx_task",
                                                    "generate_rating_summary_xlsx_task",
                                                ],
                                                view={
                                                    "label": "Class",
                                                    "options": {
                                                        "read_only_option": {
                                                            "read_only": True
                                                        }
                                                    },
                                                },
                                            ),
                                            "order_percent": hx.Float(
                                                mode="input",
                                                default=None,
                                                optionality="optional",
                                                validation={
                                                    "min_value": 0,
                                                    "max_value": 1,
                                                },
                                                view={
                                                    "label": "Order (%)",
                                                    "format": utils.percent_format(0),
                                                    "options": {
                                                        "read_only_option": {
                                                            "read_only": True
                                                        }
                                                    },
                                                },
                                                async_input=[
                                                    "rarc_task",
                                                    "set_vessels_defaults_task",
                                                    "generate_vessels_xlsx_task",
                                                    "generate_rating_summary_xlsx_task",
                                                    "push_vessels_to_datamart_task",
                                                ],
                                                async_output=[
                                                    {
                                                        "task": "set_vessels_defaults_task",
                                                        "reset": False,
                                                    },
                                                ],
                                            ),
                                            "freight_conditions": hx.Str(
                                                mode="input",
                                                optionality="optional",
                                                options_table="table_freight_conditions",
                                                options_column="freight_conditions",
                                                default=None,
                                                view={
                                                    "label": "Freight Conditions",
                                                    "options": {
                                                        "read_only_option": {
                                                            "read_only": True
                                                        }
                                                    },
                                                },
                                                async_input=[
                                                    "rarc_task",
                                                    "set_vessels_defaults_task",
                                                    "generate_vessels_xlsx_task",
                                                    "generate_rating_summary_xlsx_task",
                                                ],
                                                async_output=[
                                                    {
                                                        "task": "set_vessels_defaults_task",
                                                        "reset": False,
                                                    },
                                                    "clear_vessels_task",
                                                ],
                                            ),
                                            "vessel_quality": hx.Str(
                                                mode="input",
                                                optionality="optional",
                                                options_table="table_vessel_quality",
                                                options_column="vessel_quality",
                                                default=None,
                                                view={
                                                    "label": "Vessel/Mach. Quality",
                                                    "options": {
                                                        "read_only_option": {
                                                            "read_only": True
                                                        }
                                                    },
                                                },
                                                async_input=[
                                                    "rarc_task",
                                                    "set_vessels_defaults_task",
                                                    "generate_vessels_xlsx_task",
                                                    "generate_rating_summary_xlsx_task",
                                                ],
                                                async_output=[
                                                    {
                                                        "task": "set_vessels_defaults_task",
                                                        "reset": False,
                                                    },
                                                    "clear_vessels_task",
                                                ],
                                            ),
                                            "area_of_operation": hx.Str(
                                                mode="input",
                                                optionality="optional",
                                                options_table="table_area_of_operation",
                                                options_column="area_of_operation",
                                                default=None,
                                                view={
                                                    "label": "Area of Operation",
                                                    "options": {
                                                        "read_only_option": {
                                                            "read_only": True
                                                        }
                                                    },
                                                },
                                                async_input=[
                                                    "rarc_task",
                                                    "set_vessels_defaults_task",
                                                    "generate_vessels_xlsx_task",
                                                    "generate_rating_summary_xlsx_task",
                                                ],
                                                async_output=[
                                                    {
                                                        "task": "set_vessels_defaults_task",
                                                        "reset": False,
                                                    },
                                                    "clear_vessels_task",
                                                ],
                                            ),
                                            "fleet_casualty_history": hx.Str(
                                                mode="output",
                                                options_table="table_fleet_casualty_history",
                                                options_column="fleet_casualty_history",
                                            ),
                                            "owner_quality": hx.Str(
                                                mode="output",
                                                options_table="table_owner_quality",
                                                options_column="owner_quality",
                                            ),
                                        }
                                    ),
                                    "unique_imo": hx.Str(
                                        mode="output", async_input=["rarc_task"]
                                    ),
                                    "inception_date": hx.Date(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Inception",
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                        },
                                        async_input=[
                                            "set_vessels_defaults_task",
                                            "generate_vessels_xlsx_task",
                                            "generate_rating_summary_xlsx_task",
                                            "rarc_task",
                                            "push_vessels_to_datamart_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "set_vessels_defaults_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "expiry_date": hx.Date(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Expiry",
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                        },
                                        async_input=[
                                            "set_vessels_defaults_task",
                                            "generate_vessels_xlsx_task",
                                            "generate_rating_summary_xlsx_task",
                                            "rarc_task",
                                            "push_vessels_to_datamart_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "set_vessels_defaults_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "vessel_type": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        options_table="table_vessel_types",
                                        options_column="vessel_type",
                                        view={
                                            "label": "Type",
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                        },
                                        async_input=[
                                            "generate_vessels_xlsx_task",
                                            "generate_rating_summary_xlsx_task",
                                            "rarc_task",
                                            "push_vessels_to_datamart_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "set_vessels_defaults_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "dwt": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "DWT",
                                            "format": utils.thousands_format(0),
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                        },
                                        async_input=[
                                            "generate_vessels_xlsx_task",
                                            "rarc_task",
                                            "generate_rating_summary_xlsx_task",
                                            "push_vessels_to_datamart_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            }
                                        ],
                                        validation={"min_value": 0},
                                    ),
                                    "year_built": hx.Int(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Year built",
                                            "format": utils.integer_format(0),
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                        },
                                        async_input=[
                                            "generate_vessels_xlsx_task",
                                            "rarc_task",
                                            "push_vessels_to_datamart_task",
                                            "generate_rating_summary_xlsx_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "set_vessels_defaults_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                        ],
                                        validation={"min_value": 0},
                                    ),
                                    "flag": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        options_table="table_flags",
                                        options_column="vessel_flag",
                                        allow_custom_value=True,
                                        view={
                                            "label": "Flag",
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                        },
                                        async_input=[
                                            "generate_vessels_xlsx_task",
                                            "rarc_task",
                                            "generate_rating_summary_xlsx_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            }
                                        ],
                                    ),
                                    "coverage": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        default=None,
                                        options_table="table_coverage_factor",
                                        options_column="coverage",
                                        view={
                                            "label": "Coverage",
                                            "options": {
                                                "read_only_option": {"read_only": True},
                                                "output_summary": {
                                                    "read_only": True,
                                                    "group": "Hull",
                                                },
                                            },
                                        },
                                        async_input=[
                                            "set_vessels_defaults_task",
                                            "generate_rating_summary_xlsx_task",
                                            "generate_vessels_xlsx_task",
                                            "rarc_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "set_vessels_defaults_task",
                                                "reset": False,
                                            },
                                            "clear_vessels_task",
                                        ],
                                    ),
                                    "agreed_value": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Agreed Value",
                                            "options": {
                                                "read_only_option": {"read_only": True},
                                                "output_summary": {
                                                    "read_only": True,
                                                    "group": "Hull",
                                                },
                                            },
                                            "format": utils.thousands_format(0),
                                        },
                                        async_input=[
                                            "generate_rating_summary_xlsx_task",
                                            "generate_vessels_xlsx_task",
                                            "rarc_task",
                                            "push_vessels_to_datamart_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "set_vessels_defaults_task",
                                                "reset": False,
                                            },
                                        ],
                                        validation={"min_value": 0},
                                    ),
                                    "deductible": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Deductible",
                                            "format": utils.thousands_format(0),
                                            "options": {
                                                "read_only_option": {"read_only": True},
                                                "output_summary": {
                                                    "read_only": True,
                                                    "group": "Hull",
                                                },
                                            },
                                        },
                                        validation={"min_value": 0},
                                        async_input=[
                                            "generate_rating_summary_xlsx_task",
                                            "set_vessels_defaults_task",
                                            "generate_vessels_xlsx_task",
                                            "rarc_task",
                                            "push_vessels_to_datamart_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "set_vessels_defaults_task",
                                                "reset": False,
                                            },
                                            "clear_vessels_task",
                                        ],
                                    ),
                                    "behavioural_model_rate": hx.Float(
                                        mode="output",
                                        async_input=[
                                            "generate_vessels_xlsx_task",
                                            "generate_rating_summary_xlsx_task",
                                        ],
                                        view={
                                            "label": "Static + Behavioural \n Model Rate (%)",
                                            "format": utils.percent_format(3),
                                        },
                                    ),
                                    "behavioural_benchmark_premium": hx.Float(
                                        mode="output",
                                        async_input=[
                                            "generate_vessels_xlsx_task",
                                            "generate_rating_summary_xlsx_task",
                                        ],
                                        view={
                                            "label": "Static + Behavioural \n Benchmark Premium (USD)",
                                            "format": utils.thousands_format(0),
                                        },
                                    ),
                                    "static_model_rate": hx.Float(
                                        mode="output",
                                        async_input=[
                                            "generate_vessels_xlsx_task",
                                            "generate_rating_summary_xlsx_task",
                                        ],
                                        view={
                                            "label": "Static Model Rate (%)",
                                            "format": utils.percent_format(3),
                                        },
                                    ),
                                    "static_benchmark_premium": hx.Float(
                                        mode="output",
                                        async_input=[
                                            "generate_vessels_xlsx_task",
                                            "generate_rating_summary_xlsx_task",
                                        ],
                                        view={
                                            "label": "Static Benchmark \n Premium (USD)",
                                            "format": utils.thousands_format(0),
                                        },
                                    ),
                                    "achieved_rate": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        async_input=[
                                            "rarc_task",
                                            "generate_rating_summary_xlsx_task",
                                            "generate_vessels_xlsx_task",
                                            "push_vessels_to_datamart_task",
                                        ],
                                        view={
                                            "label": "Achieved Rate (%)",
                                            "format": utils.percent_format(6),
                                            "options": {
                                                "read_only_option": {"read_only": True},
                                                "output_summary": {
                                                    "read_only": True,
                                                    "group": "Hull",
                                                },
                                            },
                                        },
                                        validation={"min_value": 0},
                                    ),
                                    "achieved_premium": hx.Float(
                                        mode="output",
                                        async_input=[
                                            "generate_vessels_xlsx_task",
                                            "generate_rating_summary_xlsx_task",
                                        ],
                                        view={
                                            "label": "Achieved Premium",
                                            "format": utils.thousands_format(0),
                                        },
                                    ),
                                    "average_achieved_rate": hx.Float(
                                        mode="output",
                                        async_input=[
                                            "generate_vessels_xlsx_task",
                                            "generate_rating_summary_xlsx_task",
                                        ],
                                        view={
                                            "label": "Average Achieved Rate \n(2018-20)",
                                            "format": utils.percent_format(3),
                                        },
                                    ),
                                    "uw_adjustment": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "UW Adjustment",
                                            "format": utils.percent_format(2),
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                        },
                                        async_input=[
                                            "set_vessels_defaults_task",
                                            "generate_vessels_xlsx_task",
                                            "generate_rating_summary_xlsx_task",
                                            "rarc_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "set_vessels_defaults_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "percent_of_similar_vessel_that_achieved_lower_rate": hx.Float(
                                        mode="output",
                                        async_input=[
                                            "generate_rating_summary_xlsx_task",
                                            "generate_vessels_xlsx_task",
                                        ],
                                        view={
                                            "label": "% of Similar Vessel \nthat Achieved a Lower Rate",
                                            "format": utils.percent_format(2),
                                        },
                                    ),
                                    "first_rate_model_rate": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "First Rate Model Rate (%)",
                                            "format": utils.percent_format(2),
                                        },
                                    ),
                                    "unity_premium": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Unity Premium",
                                            "format": utils.thousands_format(0),
                                        },
                                    ),
                                    "number_of_port_visits": hx.Int(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Number Of port Visits",
                                            "group": "Port Visits",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "number_of_unique_port_visits": hx.Int(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Number Of Unique\nPort Visits",
                                            "group": "Port Visits",
                                        },
                                        async_input=[
                                            "lookup_imos_task",
                                            "start_renewal_task",
                                            "rarc_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "age": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Age",
                                        },
                                        async_input=["rarc_task"],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_antarctica": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Antarctica",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_australia_and_new_zealand": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Australia\nandNew Zealand",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_eastern_asia": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Eastern Asia",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_eastern_europe": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Eastern Europe",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_high_seas": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "High Seas",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_latin_america_and_caribbean": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Latin America and\nthe Caribbean",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_melanesia": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Melanesia",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_micronesia": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Micronesia",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_northern_africa": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Northern Africa",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_northern_america": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Northern America",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_northern_europe": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Northern Europe",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_polynesia": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Polynesia",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_south_eastern_asia": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "South-Eastern Asia",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_southern_asia": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Southern Asia",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_southern_europe": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Southern Europe",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_sub_saharan_africa": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Sub-Saharan Africa",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_western_asia": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Western Asia",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_aths_western_europe": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Western Europe",
                                            "group": "ATHS Regions",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "change_in_fleet": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Change in Fleet",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_class_changes_5yr": hx.Bool(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Class Changes 5yr",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "model_dwt": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Model DWT",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "model_flag": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Flag for Model",
                                        },
                                        async_input=[
                                            "lookup_imos_task",
                                            "start_renewal_task",
                                            "rarc_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "model_gross_tonnage": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Model Gross Tonnage",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "max_distance_ratio": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Max Distance Ratio",
                                        },
                                        async_input=[
                                            "lookup_imos_task",
                                            "start_renewal_task",
                                            "rarc_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "net_sum_insured": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Net Sum Insured",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "num_journeys_cut": hx.Int(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Number of Journeys Cut",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "num_port_visits_cut": hx.Int(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Number of Port\nVisits Cut",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "perc_time_eez": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Time EEZ",
                                            "format": {"mantissa": 2},
                                            "group": "Vessel Time Zone Allocation",
                                        },
                                        async_input=[
                                            "lookup_imos_task",
                                            "start_renewal_task",
                                            "rarc_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "perc_time_hrz": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Time HRZ",
                                            "format": {"mantissa": 2},
                                            "group": "Vessel Time Zone Allocation",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "perc_time_seca": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Time SECA",
                                            "format": {"mantissa": 2},
                                            "group": "Vessel Time Zone Allocation",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "powerkwmax": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Power KW Max",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "ratio_anchored": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Anchored",
                                            "format": utils.percent_format(2),
                                            "group": "Vessel Activity Allocation",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "ratio_moored": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Moored",
                                            "format": utils.percent_format(2),
                                            "group": "Vessel Activity Allocation",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "ratio_moving": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Moving",
                                            "format": utils.percent_format(2),
                                            "group": "Vessel Activity Allocation",
                                        },
                                        async_input=[
                                            "lookup_imos_task",
                                            "start_renewal_task",
                                            "rarc_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "total_unique_imos_owner": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Total Unique IMOs\nOwner Bins",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "unique_journey_ratio": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Unique Journey",
                                            "format": utils.percent_format(2),
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "unique_port_ratio": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Unique Port",
                                            "format": utils.percent_format(2),
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "ship_type": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "options": {
                                                "read_only_option": {"read_only": True}
                                            },
                                            "label": "Ship Type",
                                        },
                                        async_input=[
                                            "lookup_imos_task",
                                            "start_renewal_task",
                                            "rarc_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "current_flag": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Current Flag",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "model_ship_name": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Model Ship Name",
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "mapped_vessel_type": hx.Str(
                                        mode="output",
                                        view={
                                            "label": "Mapped Vessel Type",
                                        }
                                    ),
                                    "raw_deadweight": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Raw Deadweight",
                                            "format": {"mantissa": 5},
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "year_of_build": hx.Int(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Year of Build",
                                            "format": utils.integer_format(0),
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                        validation={"min_value": 0},
                                    ),
                                    "raw_grosstonnage": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Raw Gross Tonnage",
                                            "format": {"mantissa": 5},
                                        },
                                        async_input=[
                                            "rarc_task",
                                            "start_renewal_task",
                                            "lookup_imos_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "raw_ship_type": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Raw Ship Type",
                                        },
                                        async_input=[
                                            "lookup_imos_task",
                                            "start_renewal_task",
                                            "rarc_task",
                                        ],
                                        async_output=[
                                            {
                                                "task": "lookup_imos_task",
                                                "reset": False,
                                            },
                                            {
                                                "task": "start_renewal_task",
                                                "reset": False,
                                            },
                                        ],
                                    ),
                                    "is_behavioural_data": hx.Bool(
                                        mode="output",
                                        view={"label": "Behavioural Data Exists"},
                                        async_input=["lookup_imos_task", "rarc_task"],
                                    ),
                                    "iv": hx.Structure(
                                        children={
                                            **common.output_vessel_details("iv"),
                                            "iv_has_error": hx.Bool(mode="output"),
                                            "iv_error_validation_columns": hx.Structure(
                                                children={
                                                    iv_validation_prefix
                                                    + "coverage": hx.Str(mode="output"),
                                                    iv_validation_prefix
                                                    + "agreed_value": hx.Str(
                                                        mode="output"
                                                    ),
                                                    iv_validation_prefix
                                                    + "achieved_rate": hx.Str(
                                                        mode="output"
                                                    ),
                                                }
                                            ),
                                            "iv_output_summary_coverage": hx.Str(
                                                mode="output",
                                                async_input=[
                                                    "generate_rating_summary_xlsx_task",
                                                ],
                                                view={
                                                    "label": "Coverage",
                                                    "group": "IV",
                                                },
                                            ),
                                            "iv_output_summary_agreed_value": hx.Int(
                                                mode="output",
                                                async_input=[
                                                    "generate_rating_summary_xlsx_task",
                                                ],
                                                view={
                                                    "label": "Agreed Value",
                                                    "group": "IV",
                                                    "format": utils.thousands_format(0),
                                                },
                                            ),
                                            "iv_output_summary_deductible": hx.Int(
                                                mode="output",
                                                async_input=[
                                                    "generate_rating_summary_xlsx_task",
                                                ],
                                                view={
                                                    "label": "Deductible",
                                                    "group": "IV",
                                                    "format": utils.thousands_format(0),
                                                },
                                            ),
                                            "iv_output_summary_achieved_rate": hx.Float(
                                                mode="output",
                                                async_input=[
                                                    "generate_rating_summary_xlsx_task",
                                                ],
                                                view={
                                                    "label": "Achieved Rate",
                                                    "format": utils.percent_format(6),
                                                    "group": "IV",
                                                },
                                            ),
                                            "iv_average_achieved_rate": hx.Float(
                                                mode="output",
                                                view={
                                                    "label": "Average Achieved Rate (2018-20)",
                                                    "format": utils.percent_format(2),
                                                },
                                            ),
                                            "iv_percent_of_similar_vessel_that_achieved_lower_rate": hx.Float(
                                                mode="output",
                                                view={
                                                    "label": "% of Similar Vessel that Achieved a Lower Rate",
                                                    "format": utils.percent_format(2),
                                                },
                                            ),
                                            "iv_first_rate_model_rate": hx.Float(
                                                mode="output",
                                                view={
                                                    "label": "First Rate Model Rate (%)",
                                                    "format": utils.percent_format(2),
                                                },
                                            ),
                                        },
                                    ),
                                    "war": hx.Structure(
                                        children={
                                            **common.output_vessel_details("war"),
                                            "war_has_error": hx.Bool(mode="output"),
                                            "war_error_validation_columns": hx.Structure(
                                                children={
                                                    war_validation_prefix
                                                    + "coverage": hx.Str(mode="output"),
                                                    war_validation_prefix
                                                    + "agreed_value": hx.Str(
                                                        mode="output"
                                                    ),
                                                    war_validation_prefix
                                                    + "achieved_rate": hx.Str(
                                                        mode="output"
                                                    ),
                                                }
                                            ),
                                            "war_output_summary_coverage": hx.Str(
                                                mode="output",
                                                async_input=[
                                                    "generate_rating_summary_xlsx_task",
                                                ],
                                                view={
                                                    "label": "Coverage",
                                                    "group": "War",
                                                },
                                            ),
                                            "war_output_summary_agreed_value": hx.Int(
                                                mode="output",
                                                async_input=[
                                                    "generate_rating_summary_xlsx_task",
                                                ],
                                                view={
                                                    "label": "Agreed Value",
                                                    "group": "War",
                                                    "format": utils.thousands_format(0),
                                                },
                                            ),
                                            "war_output_summary_achieved_rate": hx.Float(
                                                mode="output",
                                                async_input=[
                                                    "generate_rating_summary_xlsx_task",
                                                ],
                                                view={
                                                    "label": "Achieved Rate",
                                                    "format": utils.percent_format(6),
                                                    "group": "War",
                                                },
                                            ),
                                        },
                                    ),
                                },
                            ),
                            "modelling_list": hx.List(
                                mode="output",
                                children={**modelling_helper.get_modelling_fields()},
                            ),
                        }
                    ),
                }
            )
        },
    )
