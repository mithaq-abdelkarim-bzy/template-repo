import hx_data_schema as hx
import data_schema.sch_utilities as utils


def get_factor_relatives_fields(model_type):
    group_prefix = model_type.capitalize() + " "
    prefix = model_type + "_"
    return {
        prefix
        + "base": hx.Float(
            mode="output",
            view={
                "label": "Base",
                "group": group_prefix + "Claims Frequency",
                "format": utils.percent_format(2),
            },
        ),
        prefix
        + "fleet_size": hx.Float(
            mode="output",
            view={
                "label": "Fleet Size",
                "group": group_prefix + "Claims Frequency",
                "format": utils.thousands_format(0),
            },
        ),
        prefix
        + "date_built": hx.Float(
            mode="output",
            view={
                "label": "Date Built",
                "group": group_prefix + "Claims Frequency",
                "format": utils.percent_format(2),
            },
        ),
        prefix
        + "frequency_vessel_type": hx.Float(
            mode="output",
            view={
                "label": "Vessel Type",
                "group": group_prefix + "Claims Frequency",
                "format": utils.percent_format(2),
            },
        ),
        prefix
        + "flag": hx.Float(
            mode="output",
            view={
                "label": "Flag",
                "group": group_prefix + "Claims Frequency",
                "format": utils.percent_format(2),
            },
        ),
        prefix
        + "frequency_dwt": hx.Float(
            mode="output",
            view={
                "label": "DWT",
                "group": group_prefix + "Claims Frequency",
                "format": utils.percent_format(2),
            },
        ),
    }


def get_severity_fields():
    prefix = "severity_"
    return {
        "base_x_build_year_x_agreed_value": hx.Float(
            mode="output",
            view={
                "label": "Base x Date Built\nx Agreed Value",
                "group": "Claims Severity",
                "format": utils.percent_format(2),
            },
        ),
        prefix
        + "vessel_type": hx.Float(
            mode="output",
            view={
                "label": "Vessel Type",
                "group": "Claims Severity",
                "format": utils.percent_format(2),
            },
        ),
        prefix
        + "dwt": hx.Float(
            mode="output",
            view={
                "label": "DWT",
                "group": "Claims Severity",
                "format": utils.percent_format(2),
            },
        ),
    }


def get_model_calculation_fields(model_type):
    group = model_type.capitalize() + " Calculation"
    prefix = model_type + "_"
    return {
        prefix
        + "model_frequency": hx.Float(
            mode="output",
            view={
                "label": "Model Frequency",
                "format": utils.percent_format(2),
                "group": group,
            },
        ),
        prefix
        + "model_severity": hx.Float(
            mode="output",
            view={
                "label": "Model Severity (USD)",
                "group": group,
            },
        ),
        prefix
        + "large_loss_overlay": hx.Float(
            mode="output",
            view={
                "label": "Large Loss Overlay (USD)",
                "group": group,
            },
        ),
        prefix
        + "coverage": hx.Str(
            mode="output",
            view={
                "label": "Coverage",
                "group": group,
            },
        ),
        prefix
        + "coverage_factor": hx.Float(
            mode="output",
            view={
                "label": "Coverage Factor",
                "group": group,
            },
        ),
        prefix
        + "expected_loss": hx.Float(
            mode="output",
            view={
                "label": "Expected Loss (USD)",
                "group": group,
            },
        ),
        prefix
        + "deductible": hx.Float(
            mode="output",
            view={
                "label": "Deductible",
                "group": group,
            },
        ),
        prefix
        + "mbbefdg": hx.Float(
            mode="output",
            view={
                "label": "MBBEFDG",
                "format": utils.percent_format(2),
                "group": group,
            },
        ),
        prefix
        + "order_percent": hx.Float(
            mode="output",
            view={
                "label": "Order",
                "format": utils.percent_format(2),
                "group": group,
            },
        ),
        prefix
        + "el_pre_uw_adj": hx.Float(
            mode="output",
            view={
                "label": "EL Pre UW Adj. (USD)",
                "group": group,
            },
        ),
        prefix
        + "all_uw_adj": hx.Float(
            mode="output",
            view={
                "label": "All UW Adj",
                "format": utils.percent_format(2),
                "group": group,
            },
        ),
        prefix
        + "el_post_uw_adj": hx.Float(
            mode="output",
            view={
                "label": "EL Post UW Adj. (USD)",
                "group": group,
            },
        ),
    }


def sch_modelling(cds):
    modelling_prefix = "modelling"
    cds.extend_node_rater_defined(
        "cds/exposure/granular",
        {
            "modelling": hx.Structure(
                children={
                    "modelling_vessels_list": hx.List(
                        mode="output",
                        children={
                            "vessel_details": hx.Structure(
                                children={
                                    modelling_prefix
                                    + "_freight_conditions": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Freight Conditions",
                                            "group": "Vessel Specific Adjustments",
                                            "format": utils.percent_format(2),
                                        },
                                    ),
                                    modelling_prefix
                                    + "_vessel_quality": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Vessel/Mach. Quality",
                                            "group": "Vessel Specific Adjustments",
                                            "format": utils.percent_format(2),
                                        },
                                    ),
                                    modelling_prefix
                                    + "_area_of_operation": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Area of Operation",
                                            "group": "Vessel Specific Adjustments",
                                            "format": utils.percent_format(2),
                                        },
                                    ),
                                    modelling_prefix
                                    + "_fleet_casualty_history": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Fleet Casualty History",
                                            "group": "Soft Fleet Factors",
                                            "format": utils.percent_format(2)
                                        },
                                    ),
                                    modelling_prefix
                                    + "_owner_quality": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Owner/Manager Quality",
                                            "group": "Soft Fleet Factors",
                                            "format": utils.percent_format(2),
                                        },
                                    ),
                                    modelling_prefix
                                    + "_agg_uw_adjustment": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Aggregate UW Adjustment",
                                            "format": utils.percent_format(2),
                                        },
                                    ),
                                }
                            ),
                            "severity": hx.Structure(
                                children={**get_severity_fields()},
                            ),
                            "static_model_factor_relatives": hx.Structure(
                                children={
                                    **get_factor_relatives_fields(model_type="static"),
                                }
                            ),
                            "static_model_calculation": hx.Structure(
                                children={
                                    **get_model_calculation_fields(model_type="static"),
                                }
                            ),
                            "behavioural_model_factor_relatives": hx.Structure(
                                children={
                                    **get_factor_relatives_fields(
                                        model_type="behavioural"
                                    ),
                                }
                            ),
                            "behavioural_model_calculation": hx.Structure(
                                children={
                                    **get_model_calculation_fields(
                                        model_type="behavioural"
                                    ),
                                }
                            ),
                        },
                    ),
                },
            ),
        },
    )
