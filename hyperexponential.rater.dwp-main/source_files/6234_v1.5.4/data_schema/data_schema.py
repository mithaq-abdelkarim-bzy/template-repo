import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_exposure_details import sch_exposure_details
from data_schema.sch_experience_rating import sch_experience_rating
from data_schema.sch_rate_change import sch_rate_change
from data_schema.sch_overrides import sch_overrides
from data_schema.sch_model_state import sch_model_state
from data_schema.sch_standard_kpi import sch_standard_kpi
from data_schema.sch_non_cds import sch_non_cds
from libraries.email_notification.data_schema.bug_report_schema import bug_report


def sch_common_data_schema():
    cds = CommonDataSchema()

    sch_risk_information(cds)
    sch_exposure_details(cds)
    sch_experience_rating(cds) 
    sch_rate_change(cds)
    sch_overrides(cds)
    sch_standard_kpi(cds)

    return cds.get_data_schema()


@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **sch_non_cds(),
        **sch_model_state(),
         **bug_report()
    })