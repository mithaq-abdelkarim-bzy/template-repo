# v0.5.0
import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_exposure_details import sch_exposure_details
from data_schema.sch_claims import sch_claims
from data_schema.sch_experience_rating import sch_experience_rating
from data_schema.sch_pricing import sch_pricing
from data_schema.sch_rate_change import sch_rate_change
from data_schema.sch_rating_summary import sch_rating_summary,sch_rating_summary_coverages
from data_schema.sch_territory import sch_territory
from data_schema.sch_example_code import sch_example_code
from data_schema.sch_model_state import sch_model_state
from data_schema.sch_overrides import sch_overrides
from algorithms.data_schema.sch_rater_defined import sch_coverages_defined, RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
from libraries.email_notification.data_schema.bug_report_schema import bug_report


def sch_common_data_schema():
    cds = CommonDataSchema()
    if RARC_COVERAGE_USE: # NOTE: go to algorithms.data_schema.sch_rater_defined and set RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE
        sch_coverages_defined(cds) # define coverages in line with the CDS

    sch_overrides(cds) 
    sch_example_code(cds) # remove for live model
    sch_experience_rating(cds)
    sch_risk_information(cds)
    sch_exposure_details(cds)
    sch_territory(cds)
    # sch_experience_rating(cds)
    sch_pricing(cds)
    sch_rating_summary(cds) # create layer nodes
    if RARC_COVERAGE_USE: 
        sch_rating_summary_coverages(cds) # add coverage nodes
    sch_rate_change(cds) # define the rate change data schema (layer and coverage when applicable).
    return cds.get_data_schema()

@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **sch_model_state(),
        **bug_report() # include log new bug section
    })
