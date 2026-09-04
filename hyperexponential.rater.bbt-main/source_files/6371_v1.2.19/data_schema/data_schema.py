import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema
from data_schema.sch_rationale                  import sch_rationale
from data_schema.sch_risk_information           import sch_risk_information
from data_schema.sch_rms                        import sch_rms
from data_schema.sch_bi_data                    import sch_bi_data
from data_schema.sch_triangle_projection        import sch_triangle_projection
from data_schema.sch_rating_summary             import sch_rating_summary
from data_schema.sch_claim_summary              import sch_claim_summary
from data_schema.sch_profit_commission          import sch_profit_commission
from data_schema.sch_show_hide                  import sch_show_hide
from data_schema.sch_async_overrides            import sch_async_tasks
from data_schema.sch_utilities                  import set_node_properties
from data_schema.sch_model_state                import sch_model_state
from libraries.email_notification.data_schema.bug_report_schema import bug_report


def sch_common_data_schema():
    cds = CommonDataSchema()
    sch_risk_information(cds)
    sch_rms(cds)
    sch_bi_data(cds)
    sch_triangle_projection(cds)
    sch_rating_summary(cds)
    sch_claim_summary(cds)
    sch_profit_commission(cds)
    sch_rationale(cds)
    sch_model_state(cds) 
    sch_show_hide(cds)
    sch_async_tasks(cds)                    ### sch_async_tasks needs to go last 


    return cds.get_data_schema()


@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        "uw_doc_template" : hx.File(mode="output", file_name = "uw_doc_template.docx", view={"label": "UW Document Template"}, async_output=["generate_uw_doc_task"]),
        **bug_report()
    })


