import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format


def sch_vessel_analysis(cds):
    prefix = "vessel_analysis_"
    cds.extend_node_rater_defined(
        "cds",
        {
            "vessel_analysis": hx.Structure(
                children={
                    "hull_rating": hx.Structure(
                        children={
                            "drop_down_info": hx.List(
                                mode="output",
                                children={
                                    "drop_down_imo": hx.Str(mode="output"),
                                    "drop_down_name": hx.Str(mode="output"),
                                },
                            ),
                            "imo_and_name": hx.Structure(
                                linked_options_data="../drop_down_info",
                                linked_options_fields=[
                                    "drop_down_imo",
                                    "drop_down_name",
                                ],
                                children={
                                    prefix
                                    + "imo": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "IMO",
                                        },
                                    ),
                                    prefix
                                    + "name": hx.Str(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={"label": "Vessel Name"},
                                    ),
                                },
                            ),
                            prefix
                            + "vessel_type_age_dwt": hx.Str(
                                mode="output",
                            ),
                            prefix
                            + "vessel_type_age_dwt_table": hx.Structure(
                                children={
                                    prefix
                                    + "vessel_type": hx.Str(
                                        mode="output",
                                        view={
                                            "label": "Type",
                                        },
                                    ),
                                    prefix
                                    + "age_range": hx.Str(
                                        mode="output",
                                        view={
                                            "label": "Age",
                                        },
                                    ),
                                    prefix
                                    + "dwt_range": hx.Str(
                                        mode="output",
                                        view={
                                            "label": "DWT",
                                        },
                                    ),
                                }
                            ),
                            prefix
                            + "vessel_pre_type_list": hx.List(
                                mode="output",
                                children={
                                    prefix + "pre_type": hx.Float(mode="output"),
                                    "constant_pre_y": hx.Float(mode="output"),
                                },
                            ),
                            prefix
                            + "vessel_post_type_list": hx.List(
                                mode="output",
                                children={
                                    prefix + "post_type": hx.Float(mode="output"),
                                    "constant_post_y": hx.Float(mode="output"),
                                },
                            ),
                            prefix
                            + "vessels_type_higher_rate": hx.Float(
                                mode="output",
                                view={
                                    "format": percent_format(0),
                                    "label": "Similar Vessels % Achieving Higher Rate (2018-20)",
                                },
                            ),
                            prefix
                            + "vessels_type_lower_rate": hx.Float(
                                mode="output",
                                view={
                                    "format": percent_format(0),
                                    "label": "Similar Vessels % Achieving Lower Rate (2018-20)",
                                },
                            ),
                            prefix
                            + "vessels_type_count": hx.Int(
                                mode="output",
                                view={
                                    "format": integer_format(),
                                    "label": "Number of Vessels Contributing to Distribution",
                                },
                            ),
                            prefix
                            + "vessel_pre_type_age_list": hx.List(
                                mode="output",
                                children={
                                    prefix + "pre_type_age": hx.Float(mode="output"),
                                    "constant_pre_y": hx.Float(mode="output"),
                                },
                            ),
                            prefix
                            + "vessel_post_type_age_list": hx.List(
                                mode="output",
                                children={
                                    prefix + "post_type_age": hx.Float(mode="output"),
                                    "constant_post_y": hx.Float(mode="output"),
                                },
                            ),
                            prefix
                            + "vessels_type_age_higher_rate": hx.Float(
                                mode="output",
                                view={
                                    "format": percent_format(0),
                                    "label": "Similar Vessels % Achieving Higher Rate (2018-20)",
                                },
                            ),
                            prefix
                            + "vessels_type_age_lower_rate": hx.Float(
                                mode="output",
                                view={
                                    "format": percent_format(0),
                                    "label": "Similar Vessels % Achieving Lower Rate (2018-20)",
                                },
                            ),
                            prefix
                            + "vessels_type_age_count": hx.Int(
                                mode="output",
                                view={
                                    "format": integer_format(),
                                    "label": "Number of Vessels Contributing to Distribution",
                                },
                            ),
                            prefix
                            + "vessel_pre_type_age_dwt_list": hx.List(
                                mode="output",
                                children={
                                    prefix
                                    + "pre_type_age_dwt": hx.Float(mode="output"),
                                    "constant_pre_y": hx.Float(mode="output"),
                                },
                            ),
                            prefix
                            + "vessel_post_type_age_dwt_list": hx.List(
                                mode="output",
                                children={
                                    prefix
                                    + "post_type_age_dwt": hx.Float(mode="output"),
                                    "constant_post_y": hx.Float(mode="output"),
                                },
                            ),
                            prefix
                            + "vessels_type_age_dwt_higher_rate": hx.Float(
                                mode="output",
                                view={
                                    "format": percent_format(0),
                                    "label": "Similar Vessels % Achieving Higher Rate (2018-20)",
                                },
                            ),
                            prefix
                            + "vessels_type_age_dwt_lower_rate": hx.Float(
                                mode="output",
                                view={
                                    "format": percent_format(0),
                                    "label": "Similar Vessels % Achieving Lower Rate (2018-20)",
                                },
                            ),
                            prefix
                            + "vessels_type_age_dwt_count": hx.Int(
                                mode="output",
                                view={
                                    "format": integer_format(),
                                    "label": "Number of Vessels Contributing to Distribution",
                                },
                            ),
                            prefix
                            + "achieved_rate": hx.Float(
                                mode="output",
                                view={
                                    "format": percent_format(2),
                                    "label": "Achieved Rate",
                                },
                            ),
                        }
                    ),
                }
            ),
        },
    )
