import hx_data_schema as hx
import data_schema.sch_utilities as utils

def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {
        # Account Details 
        "database_id": hx.Int(mode="output", view={"label": "Database ID", "format": utils.integer_format(0)}),
                                
        # Broker Details
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),
    })

    # Override properties
    cds.override_node_properties('cds/standard_fields/underwriter', {
        'options_table': "lst_underwriters", 
        'options_column': "underwriter",  
        "async_input": ["generate_uw_doc"],
        "view": {"options": {"read_only": {"read_only": True}}}
    })
    cds.override_node_properties('cds/standard_fields/insured_name', {'options_table': "lst_insureds", 'options_column': "insured", "allow_custom_value": True, "async_input": ["start_renewal_task"]})
    cds.override_node_properties('cds/standard_fields/benchmark_class', {'mode': "output"})
    cds.override_node_properties('cds/currencies/source_currency', {'default': "USD", "async_input": ["generate_uw_doc"], "view": {"options": {"read_only": {"read_only": True}}}})

    

