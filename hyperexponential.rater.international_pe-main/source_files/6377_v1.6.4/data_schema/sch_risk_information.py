import hx_data_schema as hx
import data_schema.sch_utilities as utils
from hx import params as hx_params

def sch_risk_information(cds):

    cds.extend_node_rater_defined("cds", {
        # Account Details 
        "database_id": hx.Int(mode="output", view={"label": "Database ID", "format": utils.integer_format(0)}),
                                
        # Broker Details
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),

        # currency list
        "source_currency_name": hx.Str(mode = "input", options_table= "table_fx_rates", options_column = "ccy_name", default = "United States Dollar", view = {"label": "Source Currency Name"}),

    })

    # Override dropwown links
    cds.override_node_properties('cds/standard_fields/underwriter', {"allow_custom_value": True, 'options_table': "table_input_underwriters", 'options_column': "underwriter"})
    
    # Override default values
    cds.override_node_properties('cds/currencies/source_currency', {'mode': "output"})

    # is_renewal - set to async output
    cds.override_node_properties('cds/standard_fields/is_renewal', {"async_output": ["start_renewal_task"]})

    cds.override_node_properties('cds/standard_fields/insured_name', { "async_input": ["start_renewal_task"]})

    # add coverage selection 
    cds.extend_node_rater_defined("cds", {
        "eo_coverage_selection": hx.Bool(mode = "output", async_input=["rarc_task"], view={"label": "E&O "}),
        "mediatech_coverage_selection": hx.Bool(mode = "output",  async_input=["rarc_task"], view={"label": "Media Tech "}),
        "gl_coverage_selection": hx.Bool(mode = "output",async_input=["rarc_task"], view={"label": "GL "}),
        "coverage_selection": hx.Str(mode = "input", default = None, optionality="optional", options = ["E&O", "Media Tech", "GL"], view = {"label": "Coverage"}),
        "gl_coverage_selection_opposite": hx.Bool(mode = "output"),

    })

    # override the insured name property
    cds.override_node_properties("cds/standard_fields/insured_name", {
        "options_table": "table_insured_name",
        "options_column": "firm_name",
        "allow_custom_value": True,
        "async_input": ["start_renewal_task"]
    })

    