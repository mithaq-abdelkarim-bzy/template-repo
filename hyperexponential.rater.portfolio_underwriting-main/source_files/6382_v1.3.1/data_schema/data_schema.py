import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema
from libraries.model_profiler.data_schema.profiling_schema           import model_profiling_schema

from data_schema.sch_risk_information           import sch_risk_information
from data_schema.sch_risk_code_library          import sch_risk_code_library
from data_schema.sch_assumed_deductions         import sch_assumed_deductions
from data_schema.sch_policy_level_data          import sch_policy_level_data
from data_schema.sch_claim_level_data           import sch_claim_level_data
from data_schema.sch_bp_projections             import sch_bp_projections
from data_schema.sch_rate_change                import sch_rate_change
from data_schema.sch_rating_summary             import sch_rating_summary
from data_schema.sch_model_state                import sch_model_state
from data_schema.sch_overrides                  import sch_overrides
from data_schema.sch_risk_code_composition      import sch_risk_code_composition
from data_schema.sch_non_cds                    import sch_non_cds_controllers
from data_schema.sch_portfolio_profile          import sch_portfolio_profile
from data_schema.sch_inflation                  import sch_inflation
from data_schema.sch_base_inf                   import sch_base_inf
from data_schema.sch_excess_inf                 import sch_excess_inf
from data_schema.sch_lloyds_risk_code_data      import sch_lloyds_risk_code_data
from data_schema.sch_cat                        import sch_cat
from data_schema.sch_premium_and_limit_profile  import sch_premium_and_limit_profile

from data_schema.sch_projections_own_experience import sch_projections_own_experience
from data_schema.sch_projections_lloyds_beazley import sch_projections_lloyds, sch_projections_beazley

from data_schema.sch_anti_selection             import sch_anti_selection
from data_schema.sch_uncertainty                import sch_uncertainty
from data_schema.sch_pc                         import sch_pc
from data_schema.sch_overrides                  import sch_overrides
from data_schema.sch_standard_kpis              import sch_standard_kpis
from data_schema.sch_rationale                  import sch_rationale
from data_schema.sch_expiring                   import sch_expiring
from data_schema.schema_view                    import schema_view
from libraries.email_notification.data_schema.bug_report_schema import bug_report

def sch_common_data_schema():
    cds = CommonDataSchema()


    sch_risk_information(       cds)
    sch_standard_kpis(          cds)
    sch_risk_code_library(      cds)
    sch_policy_level_data(      cds)
    sch_claim_level_data(       cds)
    sch_risk_code_composition(  cds)
    sch_assumed_deductions(     cds)
    sch_portfolio_profile(      cds)
    sch_rate_change(            cds)
    sch_inflation(              cds)
    sch_cat(                    cds)
    sch_premium_and_limit_profile(cds)
    sch_lloyds_risk_code_data(  cds)

    sch_projections_own_experience(cds)
    sch_projections_lloyds(     cds)
    sch_projections_beazley(    cds)

    sch_bp_projections(         cds)
    sch_anti_selection(         cds)
    sch_uncertainty(            cds)
    sch_pc(                     cds)
    sch_rating_summary(         cds)
    sch_rationale(              cds)
    sch_expiring(               cds)
    sch_overrides(              cds)    

    return cds.get_data_schema()

# These are the data schema items used for formatting and don't go into the cds
def sch_non_cds_items():
    return {
        "non_cds": hx.Structure( children={ **sch_non_cds_controllers(),        }  ),
                   **model_profiling_schema() }

@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **sch_model_state(),
        **sch_non_cds_items(),
        **bug_report(),
         **schema_view(),
    })
