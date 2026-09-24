import hx_data_schema as hx
import data_schema.sch_utilities as utils



def sch_risk_information(cds):
    cds.extend_node_rater_defined(
        "cds",
        {   
            #add the word document output nodes
            "coverage_options": hx.File(mode="output", async_output=["word_documents_task"], file_name="coverage_options.docx"),
            "rationale_document": hx.File(mode="output", async_output=["rationale_word_documents_task"], file_name="rationale_document.docx"),
            # Account Details
            # Database ID
            "database_id": hx.Float(mode="output", view={"label": "Database ID"}),
            # Application Date
            "application_date": hx.Date(
                default="2024-07-22", mode="input", view={"label": "Application Date"}
            ),
            # New/Replacement
            "new_replac": hx.Str(
                mode="input",
                default=None,
                optionality="optional",
                options=["New", "Replacement"],
                view={"label": "New/Replacement"},
            ),
            # Broker Contact
            "broker_contact": hx.Str(
                mode="input", default="", view={"label": "Broker Contact"}
            ),
            # Primary or Excess?
            "priexc": hx.Str(
                mode="input",
                default="Primary",
                options=["Primary", "Excess"],
                view={"label": "Primary or Excess?"},
            ),
            # Admitted or Surplus?
            "admsur": hx.Str(
                mode="input",
                default="Admitted",
                options=["Admitted", "Surplus"],
                view={"label": "Admitted or Surplus?"},
            ),
            # Application Date
            "application_date": hx.Date(
                default="2024-07-22", mode="input", view={"label": "Application Date"}
            ),
            # Clearance Status
            "clearance_status": hx.Str(
                mode="input",
                default=None,
                optionality="optional",
                options=["Quotable", "Blocked"],
                view={"label": "Clearance Status"},
            ),
            # Clearance Date
            "clearance_date": hx.Date(
                default=None,
                mode="input",
                optionality="optional",
                view={"label": "Clearance Date"},
            ),
            # Deal Status
            "deal_status": hx.Str(
                mode="input", default="Submission", view={"label": "Deal Status"}
            ),
            # New/Replacement
            "new_replac": hx.Str(
                mode="input",
                default=None,
                optionality="optional",
                options=["New", "Replacement"],
                view={"label": "New/Replacement"},
            ),
            # Clearance Status and Date
            "risk_info": hx.Structure(
                view={"label": "Risk Info"},
                children={
                    "clearance_status": hx.Str(
                        mode="input",
                        default=None,
                        optionality="optional",
                        options=["Quotable", "Blocked"],
                        view={"label": "Clearance Status"},
                    ),
                    "clearance_date": hx.Str(
                        mode="input",
                        default=None,
                        optionality="optional",
                        view={"label": "Clearance Date"},
                    ),
                },
            ),
        },
    ),

    # Override default values
    cds.override_node_properties("cds/currencies/source_currency", {"default": "USD"})
    cds.override_node_properties(
        "cds/standard_fields/inception_date", {"async_input": ["rarc_task"]}
    )
    cds.override_node_properties(
        "cds/standard_fields/expiry_date", {"async_input": ["rarc_task"]}
    )

    # Is admitted Or Surplus async input
    cds.override_node_properties(
        "cds/standard_fields/is_admitted_or_surplus", {"async_input": ["rarc_task"]}
    )
