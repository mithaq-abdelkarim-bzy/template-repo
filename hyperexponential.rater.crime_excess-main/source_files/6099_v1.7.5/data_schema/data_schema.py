import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema
import data_schema.utilities as utils
from data_schema.sch_core_data import sch_core_data
from data_schema.sch_rate_change import sch_rate_change, sch_rate_change_non_cds
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_exposure_details import sch_exposure_details, sch_exposure_details_non_cds
from data_schema.sch_modifiers import sch_modifiers
from data_schema.sch_other_calcs import sch_other_calcs, sch_other_calcs_non_cds
from data_schema.sch_model_state import sch_model_state_non_cds
from data_schema.sch_rating_summary import sch_rating_summary
from data_schema.sch_standard_kpi import sch_standard_kpi
from libraries.email_notification.data_schema.bug_report_schema import bug_report
from libraries.admitted_excess_premium.data_schema.sch_admitted_excess import sch_admitted_excess
from data_schema.sch_skeleton_overrides import sch_skeleton_overrides
from data_schema.sch_exposure_change import sch_exposure_change

def sch_common_data_schema():
    cds = CommonDataSchema()

    sch_core_data(cds)
    sch_risk_information(cds)  
    sch_exposure_details(cds)
    sch_modifiers(cds)
    sch_rate_change(cds)
    sch_other_calcs(cds)
    sch_rating_summary(cds)
    sch_standard_kpi(cds)
    sch_admitted_excess(cds)
    sch_exposure_change(cds)
    sch_skeleton_overrides(cds)
    return cds.get_data_schema()

def data_schema_non_cds():
    return {
        **sch_exposure_details_non_cds(),
        **sch_rate_change_non_cds(),
        **sch_other_calcs_non_cds(),
        **sch_model_state_non_cds(),
        "debug_str": hx.Str(mode="output"),  
    }

@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **data_schema_non_cds(),
        **bug_report()
    })


