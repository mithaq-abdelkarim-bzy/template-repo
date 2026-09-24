# v0.5.0
import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_exposure_details import sch_exposure_details
from data_schema.sch_experience_rating import sch_experience_rating
from data_schema.sch_pricing import sch_pricing
from data_schema.sch_rate_change import sch_rate_change
from data_schema.sch_rating_summary import sch_rating_summary
# from data_schema.sch_example_code import sch_example_code
from data_schema.sch_model_state import sch_model_state
from data_schema.sch_overrides import sch_overrides
from algorithms.data_schema.sch_rater_defined import sch_coverages_defined, RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE

from libraries.email_notification.data_schema.bug_report_schema import bug_report

from libraries.model_profiler.data_schema.profiling_schema import model_profiling_schema
from data_schema.schema_view import schema_view

from data_schema.sch_steer import sch_steer, sch_non_cds_steer
from data_schema.sch_clash import sch_clash
from data_schema.sch_healthcare_cat import sch_healthcare_cat, sch_non_cds_healthcare_cat

from data_schema.sch_pricing_selection import sch_pricing_selection_bdx_summary, sch_pricing_selection_cob_params



def sch_common_data_schema():
    cds = CommonDataSchema()
    sch_risk_information(cds)
    sch_pricing(cds)
    sch_rating_summary(cds) # create children of cds and cds.layer 
    sch_steer(cds)
    sch_healthcare_cat(cds)
    # sch_clash(cds)
    sch_pricing_selection_bdx_summary(cds)
    sch_pricing_selection_cob_params(cds)
    sch_overrides(cds)     
    sch_rate_change(cds) # define the rate change data schema (layer and coverage when applicable).
    return cds.get_data_schema()

@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **sch_model_state(),
        **sch_non_cds_steer(),
        **sch_non_cds_healthcare_cat(),
        **bug_report(), # include log new bug section
        # import profiler schema elements 
        **schema_view(),
        **model_profiling_schema()
        
    })