
import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_exposure_details import sch_exposure_details
# from data_schema.sch_experience_rating import sch_experience_rating
from data_schema.sch_pricing import sch_pricing
from data_schema.sch_rate_change import sch_rate_change
from data_schema.sch_rating_summary import sch_rating_summary
from data_schema.sch_model_state import sch_model_state
from data_schema.sch_overrides import sch_overrides
from algorithms.data_schema.sch_rater_defined import sch_coverages_defined, RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
from data_schema.sch_validations import sch_validations


def sch_common_data_schema():
    cds = CommonDataSchema()
    if RARC_COVERAGE_USE: # False for Specialty Professions
        pass

    sch_overrides(cds)


    sch_risk_information(cds)
    sch_exposure_details(cds)
    # sch_experience_rating(cds)
    sch_pricing(cds)
    sch_rating_summary(cds) # create layer nodes
    if RARC_COVERAGE_USE: # False for Specialty Professions
        pass
    sch_rate_change(cds)
    return cds.get_data_schema()

@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **sch_model_state(),
        "noncds":hx.Structure(children={
            **sch_validations()
        })
        
    })
