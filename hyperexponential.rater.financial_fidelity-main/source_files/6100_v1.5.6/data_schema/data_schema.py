import hx_data_schema as hx
import libraries.common_data_schema.data_schema.utilities as utils
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema
from data_schema.sch_core_data import sch_core_data
from data_schema.sch_rate_change import sch_rate_change, sch_rate_change_non_cds
from data_schema.sch_exposure_details import sch_exposure_details, sch_exposure_details_non_cds
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_modifiers import sch_modifiers
from data_schema.sch_other_calcs import sch_other_calcs, sch_other_calcs_non_cds
from data_schema.sch_experience_rating import sch_experience_rating
from data_schema.sch_model_state import sch_model_state
from libraries.email_notification.data_schema.bug_report_schema import bug_report

def sch_common_data_schema():
    cds = CommonDataSchema()

    sch_core_data(cds)
    sch_risk_information(cds)  
    sch_exposure_details(cds)
    sch_modifiers(cds)
    sch_experience_rating(cds)
    sch_rate_change(cds)
    sch_other_calcs(cds)

    return cds.get_data_schema()

def data_schema_non_cds():
    return {
        **sch_other_calcs_non_cds(),
        **sch_rate_change_non_cds(),
        **sch_exposure_details_non_cds(),
    }

@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **sch_model_state(),
        **data_schema_non_cds(),
        **bug_report()
    })
