import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema

from data_schema.cds_set_coverages import cds_set_coverages
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_exposure_input import sch_exposure_input
from data_schema.sch_fine_art import sch_fine_art
from data_schema.sch_jewellers_block import sch_jewellers_block
from data_schema.sch_general_specie import sch_general_specie
from data_schema.sch_cash_in_transit import sch_cash_in_transit
from data_schema.sch_experience_rating import sch_experience_rating
from data_schema.sch_final_selections_and_summary import sch_final_selections_and_summary
from data_schema.sch_rationale import sch_rationale
from data_schema.sch_rate_change import sch_rate_change, sch_rate_change_non_cds
from data_schema.sch_model_state import sch_model_state
from data_schema.sch_show_page import sch_show_page
from libraries.email_notification.data_schema.bug_report_schema import bug_report
from data_schema.sch_validation import sch_validation

def sch_common_data_schema():
    cds = CommonDataSchema()

    cds_set_coverages(cds)
    sch_risk_information(cds)
    sch_exposure_input(cds)
    sch_fine_art(cds)
    sch_jewellers_block(cds)
    sch_general_specie(cds)
    sch_cash_in_transit(cds)
    sch_experience_rating(cds)
    sch_final_selections_and_summary(cds)
    sch_rationale(cds)
    sch_rate_change(cds)
    sch_model_state(cds)
    sch_show_page(cds)
    sch_validation(cds)

    return cds.get_data_schema()


@hx.data_schema
def data_schema():
    return hx.Structure(
        children={
            **sch_common_data_schema(),
            **sch_rate_change_non_cds(),
            **bug_report(),
            
            # RATIONALE FILE
            "rationale_file" : hx.File(mode="output", file_name = "uwr.docx", view={"label": "UW Rationale"}, async_output=["generate_rationale_doc_task"], async_input=["new_bug_report_task"]),

            "debug": hx.Str(mode = "output", async_input=["new_bug_report_task"]),
            # "uat_prod_indicator": hx.Str(mode = "output", async_input = ["fetch_bi_data_task","bi_intelligence_fetch_task"])
            
        }
    )

