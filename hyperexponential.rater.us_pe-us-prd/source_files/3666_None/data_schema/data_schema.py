import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import (
    CommonDataSchema,
)
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_exposure_details import (
    sch_exposure_details,
    sch_rating_factors_non_cds,
)
from data_schema.sch_rating_summary import (
    sch_rating_summary,
    sch_rating_summary_non_cds,
)
from data_schema.sch_rationale import sch_rationale
from data_schema.sch_model_state import sch_model_state
from data_schema.sch_rate_change import sch_rate_change


def sch_common_data_schema():
    cds = CommonDataSchema()

    sch_risk_information(cds)
    sch_rate_change(cds)
    sch_exposure_details(cds)
    sch_rating_summary(cds)
    sch_rationale(cds)

    return cds.get_data_schema()


@hx.data_schema
def data_schema():
    return hx.Structure(
        children={
            **sch_common_data_schema(),
            **sch_model_state(),
            **sch_non_cds_items(),
        }
    )


# These are the data schema items used for formatting and don't go into the cds
def sch_non_cds_items():
    return {
        "non_cds": hx.Structure(
            children={
                **sch_rating_factors_non_cds(),
                **sch_rating_summary_non_cds(),
            }
        )
    }
