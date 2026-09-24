# v0.5.0
import hx_data_schema as hx

from libraries.email_notification.data_schema.bug_report_schema         import bug_report
from libraries.schema_viewer.data_schema.schema_view                    import schema_view
from libraries.model_profiler.data_schema.profiling_schema              import model_profiling_schema as model_profiler
from libraries.common_data_schema.data_schema.sch_common_data_schema    import CommonDataSchema

from data_schema.sch_risk_information           import sch_risk_information
from data_schema.sch_exposure_details           import sch_exposure_details
from data_schema.sch_ihs                        import sch_ihs
from data_schema.sch_experience_rating          import sch_experience_rating
from data_schema.sch_pricing                    import sch_pricing
from data_schema.sch_rate_change                import sch_rate_change
from data_schema.sch_rating_summary             import sch_rating_summary
from data_schema.sch_example_code               import sch_example_code
from data_schema.sch_model_state                import sch_model_state
from data_schema.sch_overrides                  import sch_overrides
from data_schema.sch_rationale                  import sch_rationale
from algorithms.data_schema.sch_rater_defined   import sch_add_coverages_to_layers, RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE

def sch_common_data_schema():
    cds = CommonDataSchema()
    
    sch_overrides(          cds) 
    sch_example_code(       cds)    # TODO try and remove prior to go-live as defunct but cant remove currently as prevent models upgrading
    sch_risk_information(   cds)
    sch_exposure_details(   cds)
    sch_ihs(                cds)
    sch_experience_rating(  cds)
    sch_pricing(            cds)
    sch_rating_summary(     cds)    # create layer nodes
    sch_rate_change(        cds)    # define the rate change data schema (layer and coverage when applicable).
    sch_rationale(          cds)
    return cds.get_data_schema()

@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **sch_model_state(),
        **bug_report(), # include log new bug section
        **schema_view(),
        **model_profiler()
    })