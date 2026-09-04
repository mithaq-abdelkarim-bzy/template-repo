import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_exposure_details import sch_exposure_details
from data_schema.sch_rate_change import sch_rate_change
from data_schema.sch_rating_summary import sch_rating_summary
from data_schema.sch_rationale import sch_rationale
from data_schema.sch_eso import sch_eso
from data_schema.sch_model_state import sch_model_state
from libraries.email_notification.data_schema.bug_report_schema import bug_report

def sch_common_data_schema():
    cds = CommonDataSchema()

    sch_risk_information(cds)
    sch_rate_change(cds)
    sch_exposure_details(cds)
    sch_rating_summary(cds)
    sch_rationale(cds)     
    sch_eso(cds) 

    return cds.get_data_schema()


@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **sch_model_state(),
        **bug_report(),
        "policy_doc": hx.Structure(children={
            "data_dict": hx.Str(mode="output", async_input=["generate_uw_doc"]),
            "output_file_doc": hx.File(mode="output", async_output=["generate_uw_doc"], file_name="Policy_Summary.docx"),
            "task_data_dict": hx.Str(mode="output", async_output=["generate_uw_doc"]),
            "show_generate_button": hx.Bool(mode="output"),
            "show_download": hx.Bool(mode="output"),
            "premium_check": hx.Str(mode="output"),
            "show_premium_check": hx.Bool(mode="output"),
        }),
    })