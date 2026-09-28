import hx_data_schema as hx  # Importing the hx_data_schema module and aliasing it as hx
import hx as HX  # Importing the hx module and aliasing it as HX
import data_schema.sch_utilities as utils  # Importing the utilities module from data_schema.sch_utilities and aliasing it as utils
from datetime import (
    datetime,
    timedelta,
)  # Importing datetime and timedelta from the datetime module


# Function to extend the node rater defined with risk information
def sch_risk_information(cds):
    # Get today's date
    today = datetime.today()

    # Format today's date as a string
    today_str = today.strftime("%Y-%m-%d")

    # Extend the node rater defined with various fields
    cds.extend_node_rater_defined(
        "cds",
        {
            # Account Details
            "database_id": hx.Int(
                mode="output",
                view={
                    "label": "Database ID",
                    "format": utils.integer_format(0),
                },  # Database ID field with integer format
            ),
            "broker_contact": hx.Str(
                mode="input", default="", view={"label": "Broker Contact"}
            ),
            # Firms list
            "firms_list": hx.Structure(
                children={
                    "firms": hx.List(
                        mode="output",
                        children={"firm_name": hx.Str(mode="output")},  # Firms list
                    )
                }
            ),
        },
    )

    # Override dropdown links for the underwriter field
    cds.override_node_properties(
        "cds/standard_fields/underwriter",
        {
            "options_table": "table_input_underwriters",
            "options_column": "name",
        },  # Underwriter field options from table_input_underwriters
    )

    cds.override_node_properties(
        "cds/standard_fields/broker",
        {
            "options_table": "table_input_underwriters",
            "options_column": "name",
        },  # Broker field options from table_input_underwriters
    )

    cds.override_node_properties(
        "cds/standard_fields/insured_name",
        {
            "options_table": "table_input_reference_firms",
            "options_column": "firm_name",
            "allow_custom_value": True,
        },
    )
    # Firm names field options from table_input_reference_firms

    # Override default values for source currency field
    cds.override_node_properties(
        "cds/currencies/source_currency", {"default": "USD"}
    )  # Setting default source currency to USD
