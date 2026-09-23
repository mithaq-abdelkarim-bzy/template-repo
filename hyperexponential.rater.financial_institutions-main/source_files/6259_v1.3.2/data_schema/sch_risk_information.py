import hx_data_schema as hxd

from algorithms.rate_utilities import get_field_options


def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {
        # Policy Tags
        "is_policy_tag_error": hxd.Bool(mode="output", async_output=["generate_tags"]),
        "policy_tag_msg": hxd.Str(mode="output",  async_output=["generate_tags"], view={"label": "Policy Tags Feedback"}),
        "climate_document": hxd.File(mode="output", async_output=["generate_climate_doc_task"], file_name="climate_litigation_spotlight.docx", view={"label": "Document"}),       
        "climate_document_country": hxd.Str(mode="input", async_input=["generate_climate_doc_task"], optionality="required", options=["Australia", "France", "Germany", "The Netherlands", "United Kingdom"], default="Australia", view={"label": "Country"}),
        "risk_info": hxd.Structure(children={
            "currency": hxd.Str(mode="input", default="USD", options_column="Currency code", options_table="table_ccy_base", async_input=["rarc_task"], view={"label": "Currency of insurance program"}),
            "broker_contact": hxd.Str(mode="input", default="", view={"label": "Broker Contact"}),
            "platform": hxd.Str(mode="input", options=get_field_options("risk_information", "platform"), default="Lloyd's", allow_custom_value=True, view={"label": "Platform"}),
            "eea_non_eea_indicator": hxd.Bool(mode="input", default=False, view={"label": "EEA and Non-EEA Ref"}),
            "direct_ri": hxd.Str(mode="input", options=get_field_options("risk_information", "direct_ri"), default="Direct", view={"label": "Direct/RI"}),
            "cedant_name": hxd.Str(mode="input", default="", view={"label": "Cedant Name"}),
            "comments": hxd.Str(mode="input", default=""),
            "quote_details_search": hxd.Str(mode="input", default="", async_input=["save_quote_details_to_pas_reference"], view={"label": "Quote Details (for Policies tab)"}),
        })
    })

    # CDS Overrides
    cds.override_node_properties("hx_core/inception_date", {"default": "2024-08-01", "async_input": ["rarc_task"]})
    cds.override_node_properties("hx_core/expiry_date", {"default": "2024-08-01", "async_input": ["rarc_task"]})
    cds.override_node_properties("cds/standard_fields/broker", {"options_table": "table_brokers", "options_column": "name", "async_input": ["generate_tags"]})
    cds.override_node_properties("cds/standard_fields/underwriter", {"options_table": "table_underwriters", "options_column": "name", "async_input": ["generate_tags"]})
    cds.override_node_properties("cds/standard_fields/insured_name", {"options_table": "table_reference_firms", "options_column": "firm_name", "allow_custom_value": True, "async_input": ["start_renewal_task", "generate_tags", "generate_climate_doc_task"]})
    cds.override_node_properties("cds/standard_fields/insured_country", {"default": "United Kingdom", "options_data": "../../../non_cds/risk_info/country_dropdown", "options_field": "country", "view": {"label": "Country of Domicile"}, "async_input": ["rarc_task", "generate_tags"]})
    cds.override_node_properties("cds/standard_fields/is_renewal", {"async_output": [{"task":"start_renewal_task", "reset":False}]})
    cds.override_node_properties("cds/key_industry/code_name", {"default": "Banks", "options_data": "../../../non_cds/risk_info/industry_dropdown", "options_field": "industry", "view": {"label": "Industry"}, "async_input": ["rarc_task", "generate_tags"]})


def sch_risk_information_non_cds():
    return {
        "risk_info": hxd.Structure(children={
            "region_dropdown": hxd.List(mode="output", children={"region": hxd.Str(mode="output")}),
            "country_dropdown": hxd.List(mode="output", children={"country": hxd.Str(mode="output")}),
            "industry_dropdown": hxd.List(mode="output", children={"industry": hxd.Str(mode="output")}),
            "sub_industry_dropdown": hxd.List(mode="output", children={"sub_industry": hxd.Str(mode="output")}),
            "is_coverage_required": hxd.Bool(mode="output"),
        })
    }
