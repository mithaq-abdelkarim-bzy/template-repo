import hx_data_schema as hx
from data_schema.sch_utilities import create_node


def sch_rationale(cds):
    cds.extend_node_rater_defined("cds", {
        "rationale": hx.Structure(
            children={
                "word_rationale_template": hx.File(mode="output", async_output=["generate_word_document_task"], file_name="portfolio_uw_rationale_template.docx"),
                "excel_rationale_template": hx.File(mode="output", async_output=["generate_excel_document_task"], file_name="portfolio_uw_rationale_template.xlsx"),
                "key_information": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Key Information about Account"}, async_input=["generate_word_document_task"]),
                "rationale_assumptions": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Rationale behind Assumption Selection"}, async_input=["generate_word_document_task"]),
                "rationale_methodology": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Rationale behind Methodology Selection and Overrides"}, async_input=["generate_word_document_task"]),
                "key_uncertainties": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Key Uncertainties"}, async_input=["generate_word_document_task"]),
                "polcy_claim_data_msg": hx.Str(mode="output"),
                "rate_change_notes": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Rationale behind Selection and Overrides"}, async_input=["generate_word_document_task"]),
                "prem_limit_notes": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Rationale behind Selection and Overrides"}, async_input=["generate_word_document_task"]),
                "cat_notes": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Rationale behind Selection and Overrides"}, async_input=["generate_word_document_task"])
            }
        )
    })
