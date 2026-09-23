import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_exposure_details import sch_exposure_details
from data_schema.sch_experience_rating import sch_experience_rating
from data_schema.sch_rate_change import sch_rate_change
from data_schema.sch_rating_summary import sch_rating_summary
from data_schema.sch_quote_summary import sch_quote_summary
from data_schema.sch_rater_defined import sch_rater_defined
from data_schema.sch_model_state import sch_model_state
from data_schema.sch_standard_kpi import sch_standard_kpi
from libraries.email_notification.data_schema.bug_report_schema import bug_report



def sch_common_data_schema():
    cds = CommonDataSchema()

    sch_risk_information(cds)
    sch_rating_summary(cds)
    sch_quote_summary(cds)
    sch_rater_defined(cds)
    sch_exposure_details(cds)
    sch_experience_rating(cds)
    sch_rate_change(cds)
    sch_standard_kpi(cds)

    return cds.get_data_schema()


@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **sch_model_state(),
        **bug_report(),
        "policy_doc": hx.Structure(children={
            "output_file": hx.File(mode="output", async_output=["quote_to_excel_task"], file_name="Quote_Summary.xlsx"),
            "data_dict": hx.Str(mode="output", async_input=["quote_to_excel_task"]),
            "task_data_dict": hx.Str(mode="output", async_output=["quote_to_excel_task"]),
            "show_generate_button": hx.Bool(mode="output"),
            "show_download": hx.Bool(mode="output"),
            "premium_check": hx.Str(mode="output"),
            "show_premium_check": hx.Bool(mode="output"),
        }),
        "debug_str": hx.Str(mode="output", async_output=[]),
        "debug_bool": hx.Bool(mode="input", default=False, async_output=[])
    })

