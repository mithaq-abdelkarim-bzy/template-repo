import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_exposure_details import sch_exposure_details
from data_schema.sch_triage import sch_triage
#from data_schema.sch_experience_rating import sch_experience_rating
from data_schema.sch_pricing import sch_pricing
from data_schema.sch_tech_eo import sch_tech_eo
from data_schema.sch_cyber import sch_cyber
from data_schema.sch_rate_change import sch_rate_change
from data_schema.sch_rating_summary import sch_rating_summary
from data_schema.sch_example_code import sch_example_code
from data_schema.sch_model_state import sch_model_state
from libraries.email_notification.data_schema.bug_report_schema import bug_report


def sch_common_data_schema():
    cds = CommonDataSchema()

    sch_risk_information(cds)
    sch_rate_change(cds)
    sch_exposure_details(cds)
    sch_triage(cds)
    sch_pricing(cds)
    sch_tech_eo(cds)
    sch_cyber(cds)
    sch_rating_summary(cds)
    #sch_experience_rating(cds) 


    return cds.get_data_schema()


@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **sch_model_state(),
        **bug_report()
    })