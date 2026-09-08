import hx_data_schema as hx
import data_schema.sch_utilities as utils


def get_modelling_fields():
    modelling_prefix = "modelling_"
    return {
        modelling_prefix
        + "unique_imo": hx.Str(
            mode="output",
        ),
        modelling_prefix
        + "imo": hx.Str(
            mode="output",
            view={"label": "IMO"},
        ),
        modelling_prefix
        + "name": hx.Str(
            mode="output",
            view={
                "label": "Name",
            },
        ),
        modelling_prefix
        + "vessel_type": hx.Str(
            mode="output",
            view={
                "label": "Type",
            },
        ),
        modelling_prefix
        + "gross_tonnage": hx.Int(
            mode="output",
            view={
                "label": "Gross Tonnage",
            },
        ),
        modelling_prefix
        + "dwt": hx.Int(
            mode="output",
            view={
                "label": "DWT",
            },
        ),
        modelling_prefix
        + "year_built": hx.Int(
            mode="output",
            view={
                "label": "Build Year",
                "format": utils.integer_format(0),
            },
        ),
        modelling_prefix
        + "flag": hx.Str(
            mode="output",
            view={
                "label": "Flag",
            },
        ),
        modelling_prefix
        + "vessel_class": hx.Str(
            mode="output",
            view={
                "label": "Class",
            },
        ),
        modelling_prefix
        + "agreed_value": hx.Float(
            mode="output",
            view={
                "format": utils.thousands_format(0),
            },
        ),
        modelling_prefix
        + "converted_agreed_value": hx.Float(
            mode="output",
            view={
                "label": "Converted Agreed Value",
                "format": utils.thousands_format(0),
            },
        ),
        modelling_prefix
        + "freight_conditions": hx.Float(
            mode="output",
            view={
                "label": "Freight Conditions",
                "group": "Vessel Specific Adjustments",
                "format": utils.percent_format(0),
            },
        ),
        modelling_prefix
        + "vessel_quality": hx.Float(
            mode="output",
            view={
                "label": "Vessel/Mach. Quality",
                "group": "Vessel Specific Adjustments",
                "format": utils.percent_format(0),
            },
        ),
        modelling_prefix
        + "area_of_operation": hx.Float(
            mode="output",
            view={
                "label": "Area of Operation",
                "group": "Vessel Specific Adjustments",
                "format": utils.percent_format(0),
            },
        ),
        modelling_prefix
        + "fleet_casualty_history": hx.Float(
            mode="output",
            view={
                "label": "Fleet Casualty History",
                "group": "Soft Fleet Factors",
                "format": utils.percent_format(0),
            },
        ),
        modelling_prefix
        + "owner_quality": hx.Float(
            mode="output",
            view={
                "label": "Owner/Manager Quality",
                "group": "Soft Fleet Factors",
                "format": utils.percent_format(0),
            },
        ),
        modelling_prefix
        + "uw_adjustment": hx.Float(
            mode="output",
            view={
                "label": "UW Adjustment",
                "format": utils.percent_format(0),
            },
        ),
        modelling_prefix
        + "agg_uw_adjustment": hx.Float(
            mode="output",
            view={
                "label": "Aggregate UW Adjustment",
                "format": utils.percent_format(0),
            },
        ),
        **get_severity_fields(model_type="static"),
        **get_factor_relatives_fields(model_type="static"),
        **get_factor_build_up_calculation_fields(model_type="static"),
        **get_model_calculation_fields(model_type="static"),
        **get_severity_fields(model_type="behavioural"),
        **get_factor_relatives_fields(model_type="behavioural"),
        **get_factor_build_up_calculation_fields(model_type="behavioural"),
        **get_model_calculation_fields(model_type="behavioural"),
        **get_severity_build_up_fields(model_type="static"),
        **get_severity_build_up_fields(model_type="behavioural"),
        "modelling_behavioural_max_distance_ratio": hx.Float(
            mode="output",
            view={
                "label": "Max Distance Ratio",
                "group": "Behavioural Rating Levels",
            },
        ),
        "modelling_behavioural_perc_time_eez": hx.Float(
            mode="output",
            view={
                "label": "Perc Time EEZ",
                "group": "Behavioural Rating Levels",
                "format": utils.percent_format(0),
            },
        ),
        "modelling_behavioural_ratio_moving": hx.Float(
            mode="output",
            view={
                "label": "Ratio Moving",
                "group": "Behavioural Rating Levels",
                "format": utils.percent_format(0),
            },
        ),
        "modelling_behavioural_number_of_unique_port_visits": hx.Float(
            mode="output",
            view={
                "label": "Number Of Unique\nPort Visits",
                "group": "Behavioural Rating Levels",
                "format": utils.percent_format(0),
            },
        ),
        "modelling_behavioural_ratio_moored": hx.Float(
            mode="output",
            view={
                "label": "Ratio Moored",
                "group": "Behavioural Rating Levels",
                "format": utils.percent_format(0),
            },
        ),
        "pro_rata_adjustment": hx.Float(
            mode="output",
            view={
                "label": "Pro Rata Adjustment",
            },
        ),
    }


def get_severity_build_up_fields(model_type):
    group_prefix = model_type.capitalize() + " "
    prefix = model_type + "_build_up_severity_"
    common_fields = {
        prefix
        + "base_x_build_year_x_agreed_value": hx.Float(
            mode="output",
            view={
                "label": "Base",
                "group": group_prefix + " - Severity Build Up",
            },
        ),
        prefix
        + "vessel_type": hx.Float(
            mode="output",
            view={
                "label": "Type",
                "group": group_prefix + " - Severity Build Up",
            },
        ),
        prefix
        + "dwt_lower_bound": hx.Float(
            mode="output",
            view={
                "label": "DWT Lower Band",
                "group": group_prefix + " - Severity Build Up",
                "format": utils.integer_format(0),
            },
        ),
        prefix
        + "dwt_upper_bound": hx.Float(
            mode="output",
            view={
                "label": "DWT Upper Bound",
                "group": group_prefix + " - Severity Build Up",
                "format": utils.integer_format(0),
            },
        ),
        prefix
        + "dwt_lower_bound_factor": hx.Float(
            mode="output",
            view={
                "label": "DWT Lower Relativity",
                "group": group_prefix + " - Severity Build Up",
            },
        ),
        prefix
        + "dwt_upper_bound_factor": hx.Float(
            mode="output",
            view={
                "label": "DWT Upper Relativity",
                "group": group_prefix + " - Severity Build Up",
            },
        ),
        prefix
        + "dwt": hx.Float(
            mode="output",
            view={
                "label": "DWT",
                "group": group_prefix + " - Severity Build Up",
            },
        ),
        prefix
        + "predicted": hx.Float(
            mode="output",
            view={
                "label": "Predicted Severity (%)",
                "group": group_prefix + " - Severity Build Up",
            },
        ),
        prefix
        + "model": hx.Float(
            mode="output",
            view={
                "label": "Model Severity",
                "group": group_prefix + " - Severity Build Up",
                "format": utils.thousands_format(0),
            },
        ),
    }

    result = {**common_fields} if model_type == "static" else {**common_fields}

    return result


def get_factor_build_up_calculation_fields(model_type):
    group_prefix = model_type.capitalize() + " "
    prefix = model_type + "_build_up_"
    common_fields = {
        prefix
        + "base": hx.Float(
            mode="output",
            view={
                "label": "Base",
                "group": group_prefix + " - Frequency Build Up",
            },
        ),
        prefix
        + "fleet_size": hx.Float(
            mode="output",
            view={
                "label": "Fleet Size",
                "group": group_prefix + " - Frequency Build Up",
            },
        ),
        prefix
        + "year_built": hx.Float(
            mode="output",
            view={
                "label": "Year of Build",
                "group": group_prefix + " - Frequency Build Up",
            },
        ),
        prefix
        + "frequency_vessel_type": hx.Float(
            mode="output",
            view={
                "label": "Type",
                "group": group_prefix + " - Frequency Build Up",
            },
        ),
        prefix
        + "flag": hx.Float(
            mode="output",
            view={
                "label": "Flag",
                "group": group_prefix + " - Frequency Build Up",
            },
        ),
        prefix
        + "frequency_dwt_lower_bound": hx.Float(
            mode="output",
            view={
                "label": "DWT Lower Band",
                "group": group_prefix + " - Frequency Build Up",
                "format": utils.integer_format(0),
            },
        ),
        prefix
        + "frequency_dwt_upper_bound": hx.Float(
            mode="output",
            view={
                "label": "DWT Upper Bound",
                "group": group_prefix + " - Frequency Build Up",
                "format": utils.integer_format(0),
            },
        ),
        prefix
        + "frequency_dwt_lower_bound_factor": hx.Float(
            mode="output",
            view={
                "label": "DWT Lower Relativity",
                "group": group_prefix + " - Frequency Build Up",
            },
        ),
        prefix
        + "frequency_dwt_upper_bound_factor": hx.Float(
            mode="output",
            view={
                "label": "DWT Upper Relativity",
                "group": group_prefix + " - Frequency Build Up",
            },
        ),
        prefix
        + "frequency_dwt": hx.Float(
            mode="output",
            view={
                "label": "DWT",
                "group": group_prefix + " - Frequency Build Up",
            },
        ),
        prefix
        + "frequency_predicted": hx.Float(
            mode="output",
            view={
                "label": f"Predicted Frequency - {group_prefix}",
                "group": group_prefix + " - Frequency Build Up",
            },
        ),
        prefix
        + "expected_loss": hx.Float(
            mode="output",
            view={
                "label": f"Expected Loss - {group_prefix}",
                "group": group_prefix + " - Frequency Build Up",
                "format": utils.thousands_format(0),
            },
        ),
    }

    result = (
        {**common_fields}
        if model_type == "static"
        else {
            **common_fields,
            prefix
            + "max_distance_ratio": hx.Float(
                mode="output",
                view={
                    "label": "Max Distance Ratio",
                    "group": group_prefix + " - Frequency Build Up",
                },
            ),
            prefix
            + "perc_time_eez": hx.Float(
                mode="output",
                view={
                    "label": "Perc Time EEZ",
                    "group": group_prefix + " - Frequency Build Up",
                },
            ),
            prefix
            + "ratio_moving": hx.Float(
                mode="output",
                view={
                    "label": "Ratio Moving",
                    "group": group_prefix + " - Frequency Build Up",
                },
            ),
            prefix
            + "number_of_unique_port_visits": hx.Float(
                mode="output",
                view={
                    "label": "Number Of Unique\nPort Visits",
                    "group": group_prefix + " - Frequency Build Up",
                },
            ),
            prefix
            + "ratio_moored": hx.Float(
                mode="output",
                view={
                    "label": "Ratio Moored",
                    "group": group_prefix + " - Frequency Build Up",
                },
            ),
        }
    )

    return result


def get_factor_relatives_fields(model_type):
    group_prefix = model_type.capitalize() + " "
    prefix = model_type + "_"
    common_fields = {
        prefix
        + "base": hx.Float(
            mode="output",
            view={
                "label": "Base",
                "group": group_prefix + "Claims Frequency",
            },
        ),
        prefix
        + "fleet_size": hx.Float(
            mode="output",
            view={
                "label": "Fleet Size",
                "group": group_prefix + "Claims Frequency",
            },
        ),
        prefix
        + "year_built": hx.Float(
            mode="output",
            view={
                "label": "Date Built",
                "group": group_prefix + "Claims Frequency",
            },
        ),
        prefix
        + "frequency_vessel_type": hx.Float(
            mode="output",
            view={
                "label": "Vessel Type",
                "group": group_prefix + "Claims Frequency",
            },
        ),
        prefix
        + "flag": hx.Float(
            mode="output",
            view={
                "label": "Flag",
                "group": group_prefix + "Claims Frequency",
            },
        ),
        prefix
        + "frequency_dwt": hx.Float(
            mode="output",
            view={
                "label": "DWT",
                "group": group_prefix + "Claims Frequency",
            },
        ),
    }

    result = (
        {**common_fields}
        if model_type == "static"
        else {
            **common_fields,
            prefix
            + "max_distance_ratio": hx.Float(
                mode="output",
                view={
                    "label": "Max Distance Ratio",
                    "group": group_prefix + "Claims Frequency",
                },
            ),
            prefix
            + "perc_time_eez": hx.Float(
                mode="output",
                view={
                    "label": "Time EEZ",
                    "group": group_prefix + "Claims Frequency",
                },
            ),
            prefix
            + "ratio_moving": hx.Float(
                mode="output",
                view={
                    "label": "Ratio Moving",
                    "group": group_prefix + "Claims Frequency",
                },
            ),
            prefix
            + "number_of_unique_port_visits": hx.Float(
                mode="output",
                view={
                    "label": "Number Of Unique\nPort Visits",
                    "group": group_prefix + "Claims Frequency",
                },
            ),
            prefix
            + "ratio_moored": hx.Float(
                mode="output",
                view={
                    "label": "Ratio Moored",
                    "group": group_prefix + "Claims Frequency",
                },
            ),
        }
    )

    return result


def get_severity_fields(model_type):
    group_prefix = model_type.capitalize() + " "
    prefix = f"{model_type}_severity_"
    return {
        prefix
        + "base_x_build_year_x_agreed_value": hx.Float(
            mode="output",
            view={
                "label": "Base x Date Built\nx Agreed Value",
                "group": group_prefix + "Claims Severity",
            },
        ),
        prefix
        + "vessel_type": hx.Float(
            mode="output",
            view={
                "label": "Vessel Type",
                "group": group_prefix + "Claims Severity",
            },
        ),
        prefix
        + "dwt": hx.Float(
            mode="output",
            view={
                "label": "DWT",
                "group": group_prefix + "Claims Severity",
            },
        ),
    }


def get_model_calculation_fields(model_type):
    group = model_type.capitalize() + " Model Calculation"
    prefix = model_type + "_"
    return {
        prefix
        + "model_frequency": hx.Float(
            mode="output",
            view={
                "label": "Model Frequency",
                "group": group,
            },
        ),
        prefix
        + "model_severity": hx.Float(
            mode="output",
            view={
                "label": "Model Severity (USD)",
                "group": group,
                "format": utils.thousands_format(0),
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
                "format": utils.thousands_format(0),
            },
        ),
        prefix
        + "deductible": hx.Float(
            mode="output",
            view={
                "label": "Deductible",
                "group": group,
                "format": utils.thousands_format(0),
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
                "format": utils.thousands_format(0),
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
                "format": utils.thousands_format(0),
            },
        ),
    }
