import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_rate_change import sch_rate_change
from data_schema.sch_rating_summary import sch_rating_summary
from data_schema.sch_coverage import sch_coverage
from data_schema.sch_rater_defined import sch_rater_defined
from libraries.email_notification.data_schema.bug_report_schema import bug_report


def sch_common_data_schema():
    cds = CommonDataSchema()

    sch_risk_information(cds)
    sch_rate_change(cds)
    sch_rating_summary(cds)
    sch_coverage(cds)
    sch_rater_defined(cds)

    return cds.get_data_schema()


@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **bug_report(),
        "policy_doc": hx.Structure(children={
            "data_dict": hx.Str(mode="output", async_input=["policy_to_excel_task"]),
            "output_file": hx.File(mode="output", file_name="Policy_Summary.xlsx", async_output=["policy_to_excel_task"]),
            "task_data_dict": hx.Str(mode="output", async_output=["policy_to_excel_task"]), # To store the data_dict used by the task and compare it to the live one
            "show_generate_button": hx.Bool(mode="output"),
            "show_download": hx.Bool(mode="output"),
            "premium_check": hx.Str(mode="output"),
            "show_premium_check": hx.Bool(mode="output"),
        }),
        "debug_str": hx.Str(mode="output", async_output=[]),
    })

