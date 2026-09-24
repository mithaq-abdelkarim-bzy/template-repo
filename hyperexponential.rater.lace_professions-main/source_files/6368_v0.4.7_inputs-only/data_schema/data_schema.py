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


def input_overrides(cds):
    # territory
    cds.override_node_properties('cds/exposure/granular/territory/summary/total/year_0_pcnt', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/territory/summary/total/year_0_value', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/territory/summary/total/year_1_pcnt', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/territory/summary/total/year_1_value', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/territory/summary/total/year_2_pcnt', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/territory/summary/total/year_2_value', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/territory/summary/total/year_3_pcnt', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/territory/summary/total/year_3_value', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/territory/summary/total/year_4_pcnt', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/territory/summary/total/year_4_value', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/territory/summary/total/year_5_pcnt', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/territory/summary/total/year_5_value', {"mode":"input","default":0, "optionality":"optional"})

    # client details lawyers
    cds.override_node_properties("cds/exposure/granular/client_details_lawyers/areas_of_practice_total/year_0_value", {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties("cds/exposure/granular/client_details_lawyers/areas_of_practice_total/year_1_value", {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties("cds/exposure/granular/client_details_lawyers/areas_of_practice_total/year_2_value", {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties("cds/exposure/granular/client_details_lawyers/areas_of_practice_total/year_3_value", {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties("cds/exposure/granular/client_details_lawyers/areas_of_practice_total/year_4_value", {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties("cds/exposure/granular/client_details_lawyers/areas_of_practice_total/year_5_value", {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties("cds/exposure/granular/client_details_lawyers/areas_of_practice_total/year_0_pcnt", {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties("cds/exposure/granular/client_details_lawyers/areas_of_practice_total/year_1_pcnt", {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties("cds/exposure/granular/client_details_lawyers/areas_of_practice_total/year_2_pcnt", {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties("cds/exposure/granular/client_details_lawyers/areas_of_practice_total/year_3_pcnt", {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties("cds/exposure/granular/client_details_lawyers/areas_of_practice_total/year_4_pcnt", {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties("cds/exposure/granular/client_details_lawyers/areas_of_practice_total/year_5_pcnt", {"mode":"input","default":0, "optionality":"optional"})

    # client details AEC
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_0_value', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_1_value', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_2_value', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_3_value', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_4_value', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_5_value', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_0_pcnt', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_1_pcnt', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_2_pcnt', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_3_pcnt', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_4_pcnt', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/areas_of_practice_total/year_5_pcnt', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/individual_project_types/total/year_0_value', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/individual_project_types/total/year_1_value', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/individual_project_types/total/year_2_value', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/individual_project_types/total/year_3_value', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/individual_project_types/total/year_4_value', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/individual_project_types/total/year_5_value', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/individual_project_types/total/year_0_pcnt', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/individual_project_types/total/year_1_pcnt', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/individual_project_types/total/year_2_pcnt', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/individual_project_types/total/year_3_pcnt', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/individual_project_types/total/year_4_pcnt', {"mode":"input","default":0, "optionality":"optional"})
    cds.override_node_properties('cds/exposure/granular/client_details_AEC/individual_project_types/total/year_5_pcnt', {"mode":"input","default":0, "optionality":"optional"})

    # Exposure Details - rest of changes implemented in sch_exposure_details
    cds.override_node_properties('cds/exposure/granular/exposure_expected_current_year', {"mode":"input","default":0, "optionality":"optional"})

    # Structure & Pricing
    for layer_path in ['cds/layers', 'cds/layers_addl']:
        for field in [
            'benchmark_premium_100', 'benchmark_premium_uw_view', 'blended_model_net_rate',
            'blended_uw_net_rate', 'bound_premium_share', 'bpi_bound_100', 'bpi_quoted_100',
            'expected_loss_cost_net', 'experience_rate', 'experience_weighting', 'exposure_rate',
            'exposure_rate_incl_adj', 'gross_rate_per_mill', 'technical_premium_100',
            'tpi_bound_100', 'tpi_quoted_100', 'uw_experience_weighting',
            'experience_rate_incl_adj', 'experience_weighting_2', 'blended_model_net_rate_pre',
            'expected_loss_cost_net_pre', 'technical_premium_100_incl_adj',
            'benchmark_premium_100_incl_adj', 'bpi_quoted_100_incl_adj', 'bpi_bound_100_incl_adj',
            'tpi_quoted_100_incl_adj', 'tpi_bound_100_incl_adj',
        ]:
            cds.override_node_properties(f'{layer_path}/{field}', {"mode":"input","default":0, "optionality":"optional"})

        for field in [
            'aoc_limit', 'agg_limit', 'aoc_attachment', 'agg_attachment',
            'gross_benchmark_premium', 'ilf_gross_benchmark_premium',
            'aoc_limit_oc', 'agg_limit_oc', 'aoc_attachment_oc', 'agg_attachment_oc',
            'gross_benchmark_premium_oc', 'ilf_gross_benchmark_premium_oc',
        ]:
            cds.override_node_properties(f'{layer_path}/experience_rating_summary/{field}', {"mode":"input", "default":0, "optionality":"optional"})

    for field in ['excess_agg', 'excess_eec', 'unadjusted_blended_model_net_rate', 'unadjusted_bound_tpi', 'unadjusted_exposure_rate', 'unadjusted_technical_premium']:
        cds.override_node_properties(f'cds/layers/{field}', {"mode":"input","default":0, "optionality":"optional"})

    # Experience Rating - keep live model fields editable for migration.
    cds.override_node_properties('cds/experience_rating/experience_ccy', {"mode":"input", "default":"", "optionality":"optional"})
    cds.override_node_properties('cds/experience_rating/gross_benchmark_experience_rated_premium/last_15_years', {"mode":"input","default":0, "optionality":"optional"})

    for year in range(20, -1, -1):
        for field in [
            'revalued_notional_revenue_oc',
            'revalued_notional_revenue_weighted_oc',
            'gu_incurred_oc',
            'gu_inflated_oc',
            'ql_inflated_incurred_oc',
            'weighting_applied_year',
        ]:
            cds.override_node_properties(f'cds/experience_rating/claims_summary/year_{year}/{field}', {"mode":"input", "default":0, "optionality":"optional"})

    for structure in [
        'weighted_revalued_notional_revenue',
        'developed_weighted_revalued_notional_revenue',
        'value_of_claims_data',
        'inflated_incurred_to_quoted_layer',
        'per_yr_of_claims_data_value',
        'gross_benchmark_experience_rated_premium',
    ]:
        for field in ['last_10_years_oc', 'last_15_years_oc', 'last_20_years_oc']:
            cds.override_node_properties(f'cds/experience_rating/{structure}/{field}', {"mode":"input", "default":0, "optionality":"optional"})

    for field in ['aoc_limit_oc', 'agg_limit_oc', 'aoc_attachment_oc', 'agg_attachment_oc']:
        cds.override_node_properties(f'cds/experience_rating/layer_to_view_summary/{field}', {"mode":"input", "default":0, "optionality":"optional"})

    
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
    input_overrides(cds)
    return cds.get_data_schema()

@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **sch_model_state(),
        **bug_report() # include log new bug section
    })
