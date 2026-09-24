import hx
from libraries.common_data_schema.algorithms.sync_hx_core                import sync_hx_core
from algorithms.model_state                                              import model_state
from algorithms.references_ratings.rate_inf                              import rate_base_inf, rate_excess_inf
from algorithms.risk_information.rate_risk_information                   import rate_risk_information
from algorithms.risk_code_library.rate_risk_code_library                 import rate_risk_code_library
from algorithms.policy_level_data.rate_policy_level                      import rate_policy_level
from algorithms.claim_level_data.rate_claim_level                        import rate_claims_level
from algorithms.risk_code_composition.rate_risk_code_composition         import rate_risk_code_composition
from algorithms.assumed_deductions.rate_assumed_deductions               import rate_assumed_deductions
from algorithms.bp_projections.rate_bp_projections_pre_rate_change       import rate_bp_projections_pre_rate_change
from algorithms.portfolio_profile.rate_portfolio_profile                 import rate_portfolio_profile
from algorithms.rate_change.rate_rate_change                             import rate_rate_change
from algorithms.bp_projections.rate_bp_projections_post_rate_change      import rate_bp_projections_post_rate_change
from algorithms.inflation.rate_inflation                                 import rate_inflation
from algorithms.cat.rate_cat                                             import rate_cat
from algorithms.premium_and_limit_profile.rate_premium_and_limit_profile import rate_premium_and_limit_profile
from algorithms.anti_selection.rate_anti_selection                       import rate_anti_selection
from algorithms.uncertainty.rate_uncertainty                             import rate_uncertainty
from algorithms.pc.rate_pc                                               import rate_pc
from algorithms.rating_summary.rate_rating_summary                       import rate_rating_summary
from algorithms.rate_map_to_cds                                          import rate_map_to_cds
from algorithms.rate_rater                                               import rater_load, rater_save
from algorithms.rate_section_ref_allocation                              import rate_section_ref_allocation
from algorithms.projections.rate_all_projections                         import rate_all_projections
from algorithms.export.policy_document                                   import store_policy_data


from libraries.model_profiler.algorithms.profiling_hxd_functions         import time_me
from algorithms.schema_view.rating                                       import schema_view_rating

import algorithms.validations.risk_code_composition_validations as rc_validations
import algorithms.validations.rating_summary_validations as rs_validations
from libraries.email_notification.algorithms.bug_report import provision_bug_report_inputs_outputs


@hx.rating
@time_me
def rating_algorithm(hxd):

    is_bbt              = hxd.cds.risk_information.follow_main_syndicate
    is_rater_priced     = hxd.cds.standard_fields.rating_methodology == "Rater"

    model_state(            hxd)
    sync_hx_core(           hxd)
    rater = {}
    rater_load(             hxd, rater)
    rate_base_inf(          hxd, rater)
    rate_excess_inf(        hxd, rater)
    rate_risk_information(  hxd)
    rate_risk_code_library( hxd, rater)

    if is_rater_priced and (not is_bbt):
        rate_policy_level(                      hxd, rater)
        rate_claims_level(                      hxd, rater)
        rate_risk_code_composition(             hxd, rater)

        # Validate that selected_lob lists have the right length before continuing
        if not rc_validations.validate_list_lengths(hxd, rater):
            rater_save(             hxd, rater)
            schema_view_rating(hxd=hxd)
            return

        rate_assumed_deductions(                hxd, rater)
        rate_inflation(                         hxd, rater)
        rate_bp_projections_pre_rate_change(    hxd, rater)                             
        rate_portfolio_profile(                 hxd, rater, run_lloyds_data_only=True)  
        rate_premium_and_limit_profile(         hxd, rater) 
        rate_rate_change(                       hxd, rater)
        rate_bp_projections_post_rate_change(   hxd, rater)
        rate_portfolio_profile(                 hxd, rater, run_lloyds_data_only=False)
        rate_cat(                               hxd, rater)
        rate_all_projections(                   hxd, rater)

    rate_anti_selection(                hxd)
    rate_uncertainty(                   hxd)
    rate_rating_summary(                hxd, is_bbt, rater)
    rate_pc(                            hxd, is_bbt, rater)
    rate_section_ref_allocation(        hxd, rater)
    rater_save(                         hxd, rater)
    rate_map_to_cds(                    hxd, is_bbt)
    store_policy_data(                  hxd, rater)     # needs to be after map to cds above - it uses its values
    rs_validations.check_excel_produced(hxd)            # needs to be after store policy data - it relies on a test therein on whether the excel template is valid/current

    schema_view_rating(             hxd=hxd)

    bug_report_node = getattr(hxd, "bug_report", None)
    if bug_report_node is not None:
        provision_bug_report_inputs_outputs(hxd)
    return

    

################################




