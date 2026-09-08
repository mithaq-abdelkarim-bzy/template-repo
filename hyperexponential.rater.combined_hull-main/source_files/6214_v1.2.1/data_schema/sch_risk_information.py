import hx_data_schema as hx
import data_schema.sch_utilities as utils
import hx as HX
import sys
import os


def get_currencies():
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from algorithms import parameter_tables_schema as params

    return params.fx_rates.df().ccy.unique().tolist()


def sch_risk_information(cds):
    cds.extend_node_rater_defined(
        "cds",
        {
            # Account Details
            "database_id": hx.Int(
                mode="output",
                view={"label": "Database ID", "format": utils.integer_format(0)},
            ),
            # Broker Details
            "broker_contact": hx.Str(
                mode="input",
                default="",
                view={"label": "Broker Contact"},
                async_input=["generate_rating_summary_xlsx_task"],
            ),
            "coverage_type": hx.Str(
                mode="input",
                default="Hull, IV, War",
                options=["Hull, IV, War", "Loss of Hire (LOH)", "Shipbuilders"],
                async_input=["rarc_task"],
                view={"label": "Coverage Type"},
            ),
            "name_on_yard": hx.Str(
                mode="input", default="", view={"label": "Name on Yard"}
            ),
            # Output booleans to control visibility of IV and War coverage in case of Hull coverage not selected
            "is_iv_coverage": hx.Bool(
                mode="input", default=False, view={"label": "IV Coverage"}
            ),
            "is_war_coverage": hx.Bool(
                mode="input", default=False, view={"label": "War Coverage"}
            ),
            "currency_agreed_value_label": hx.Str(mode="output"),
            "currency_loh_agreed_value_label": hx.Str(mode="output"),
            "currency_loh_total_sum_insured_label": hx.Str(mode="output"),
            "uw_dropdown_population": hx.List(
                mode="output",
                children={
                    "underwriter": hx.Str(
                        mode="output",
                    ),
                },
            ),
        },
    )

    # Override properties
    cds.override_node_properties(
        "cds/standard_fields/underwriter",
        {
            "options_data": "../../uw_dropdown_population",
            "options_field": "underwriter",
            "async_input": ["generate_rating_summary_xlsx_task"],
        },
    )

    cds.override_node_properties(
        "cds/standard_fields/is_renewal",
        {
            "async_input": [
                "push_vessels_to_datamart_task",
                "generate_rating_summary_xlsx_task",
            ],
        },
    )

    cds.override_node_properties(
        "cds/standard_fields/insured_name",
        {
            "options_table": "insured_names",
            "options_column": "insured_name",
            "allow_custom_value": True,
            "async_input": ["start_renewal_task", "generate_rating_summary_xlsx_task"],
        },
    )
    cds.override_node_properties(
        "cds/currencies/source_currency",
        {
            "default": "USD",
            "view": {"label": "Currency"},
            "async_input": [
                "generate_vessels_xlsx_task",
                "push_vessels_to_datamart_task",
                "generate_rating_summary_xlsx_task",
            ],
            "options": get_currencies(),
            "optionality": "required",
        },
    )
    cds.override_node_properties(
        "cds/standard_fields/broker",
        {
            "async_input": ["generate_rating_summary_xlsx_task"],
        },
    ),

    cds.override_node_properties(
        "cds/standard_fields/insured_name",
        {
            "async_input": ["generate_rating_summary_xlsx_task"],
        },
    )
