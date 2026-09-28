import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import (
    CommonDataSchema,
)
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_exposure_details import sch_exposure_details
from data_schema.sch_rating_summary import sch_rating_summary
from data_schema.sch_rationale import sch_rationale


def sch_common_data_schema():
    cds = CommonDataSchema()

    sch_risk_information(cds)
    sch_exposure_details(cds)
    sch_rating_summary(cds)
    sch_rationale(cds)

    return cds.get_data_schema()


@hx.data_schema
def data_schema():
    return hx.Structure(children={**sch_common_data_schema()})
