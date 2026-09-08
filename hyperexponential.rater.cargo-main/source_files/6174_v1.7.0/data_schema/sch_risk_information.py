import hx_data_schema as hx
import data_schema.sch_utilities as utils

def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {
        # Account Details 
        "database_id": hx.Int(mode="output", view={"label": "Database ID", "format": utils.integer_format(0)}),
        "application_date": hx.Date(mode="input", default="2000-01-01", view={"label": "Application Date"}),
                        
        # Broker Details
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),

    })

    # Update underwriters variable to link to dropdown
    cds.override_node_properties("cds/standard_fields/underwriter", {"options_table": "table_input_underwriters", "options_column": "underwriter"})

    # Override default values
    cds.override_node_properties("cds/currencies/source_currency", {"default": "USD"})

    # Renewal-related fields
    cds.override_node_properties("cds/standard_fields/is_renewal", {"mode": "override"})
    cds.override_node_properties("cds/standard_fields/insured_name", {"async_output": ["expiring_policy_fetch_task"]})
    cds.override_node_properties("cds/currencies/source_currency", {"async_output": ["expiring_policy_fetch_task"]})

    # Allow for two section references and make policy reference a subset of it
    cds.override_node_properties("cds/standard_fields/policy_reference", {"mode": "output"})
    cds.override_node_properties("cds/layers/section_reference", {"mode": "output"})
    cds.extend_node_rater_defined("cds/layers", {
        "single_section_reference": hx.Structure(children={
            "ref": hx.Str(mode="input", default="", view={"label": "Section Reference"}, async_input=["pass_pas_reference"]),
            "type": hx.Str(mode="input", default="All", view={"label": "Region", "read_only": True}),
            "is_shown": hx.Bool(mode = "output")
        }),
        "eea_section_reference": hx.Structure(children={
            "ref": hx.Str(mode="input", default="", view={"label": "Section Reference"}, async_input=["pass_pas_reference"]),
            "type": hx.Str(mode="input", default="EEA", view={"label": "Region", "read_only": True}),
            "is_shown": hx.Bool(mode = "output")
        }),
        "non_eea_section_reference": hx.Structure(children={
            "ref": hx.Str(mode="input", default="", view={"label": "Section Reference"}, async_input=["pass_pas_reference"]),
            "type": hx.Str(mode="input", default="Non-EEA", view={"label": "Region", "read_only": True}),
            "is_shown": hx.Bool(mode = "output")
        }),
        # "single_section_reference_cargo_cyber": hx.Structure(children={
        #     "ref": hx.Str(mode="input", default="", view={"label": "Cargo Cyber Section Reference"}, async_input=["pass_pas_reference"]),
        #     "type": hx.Str(mode="input", default="Cargo Cyber: All", view={"label": "Region", "read_only": True}),
        #     "is_shown": hx.Bool(mode = "output")
        # }),
        # "eea_section_reference_cargo_cyber": hx.Structure(children={
        #     "ref": hx.Str(mode="input", default="", view={"label": "Cargo Cyber Section Reference"}, async_input=["pass_pas_reference"]),
        #     "type": hx.Str(mode="input", default="Cargo Cyber: EEA", view={"label": "Region", "read_only": True}),
        #     "is_shown": hx.Bool(mode = "output")
        # }),
        # "non_eea_section_reference_cargo_cyber": hx.Structure(children={
        #     "ref": hx.Str(mode="input", default="", view={"label": "Cargo Cyber Section Reference"}, async_input=["pass_pas_reference"]),
        #     "type": hx.Str(mode="input", default="Cargo Cyber: Non-EEA", view={"label": "Region", "read_only": True}),
        #     "is_shown": hx.Bool(mode = "output")
        # }),
        "has_double_section_ref": hx.Bool(mode="input", default=False, view={"label": "Split section reference?"}, async_input=["pass_pas_reference"]),
        "has_single_section_ref": hx.Bool(mode="output")
    })

    #to show Cargo Cyber Policy Section Reference or not
    cds.extend_node_rater_defined("cds",{
        "main_polref_is_shown": hx.Bool(mode= "output"),
        "cargo_cyber_is_shown": hx.Bool(mode= "output"),
    })

    