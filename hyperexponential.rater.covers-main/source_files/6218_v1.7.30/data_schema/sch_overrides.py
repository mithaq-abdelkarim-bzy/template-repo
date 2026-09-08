import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers
import data_schema.sch_utilities as utils

def sch_async_tasks(cds):
    cds.extend_node_rater_defined("cds/layers", {
        # Added variable to record a bpi where the risk is case priced. Do not remove as used in tpi summary. 
        "bpi_case_priced": hx.Float(mode="input", default=None, optionality="optional", view={"label": "BPI (Case Priced)", "format": percent_format(1)}),
    })

    # Override values
    cds.override_node_properties("cds/layers", {"max_element_count": max_layers})
    cds.override_node_properties("cds/layers/status", {
        "async_input":["run_bordereau_rater_task", "bi_clm_and_mvmt_exc_triangles_fetch_task", "simulate_pc_task", "pull_in_exposure_management_data_task"],
        "async_output":["start_renewal_task"],"view": {"options": {
        "input": {"label": "Status"},
        "read_only": {"label": "Deal Status by Renewal Layers", "read_only": True}
        
    }}})
    cds.override_node_properties("cds/layers/bpi_case_priced", {"default": 0, "optionality": "required"})
    
    # Add nodes to async_inputs for rarc_task
    cds.override_node_properties("cds/layers/limit", {"async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/excess", {"async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/deductible", {"async_input": ["rarc_task"]})    
    cds.override_node_properties("cds/layers/brokerage", {"default": 0, "optionality": "required", "async_input": ["rarc_task", "run_bordereau_rater_task" , "simulate_pc_task"], "view": {"format": utils.percent_format(2)}, "validation": {"min_value": 0, "max_value": 1}})
    cds.override_node_properties("cds/layers/written_line", {"default": 1, "optionality": "required", "async_input": ["bi_clm_and_mvmt_exc_triangles_fetch_task","pull_in_exposure_management_data_task", "run_bordereau_rater_task" , "simulate_pc_task", "generate_uw_rationale_doc_task"], "validation": {"min_value": 0, "max_value": 1}, "view": {"label":"Written Line","format": utils.percent_format(2), "options": {
        "rationale": {"label": "Written Line", "read_only": True}
    }}})
    cds.override_node_properties("cds/layers/signed_line", {"default": 0, "optionality": "required", "async_input": ["bi_clm_and_mvmt_exc_triangles_fetch_task","pull_in_exposure_management_data_task", "run_bordereau_rater_task" , "simulate_pc_task", "generate_uw_rationale_doc_task"], "validation": {"min_value": 0, "max_value": 1}, "view": {"label":"Signed Line","format": utils.percent_format(2), "options": {
        "rationale": {"label": "Signed Line", "read_only": True}
    }}})
    cds.override_node_properties("cds/layers/benchmark_premium", {"async_input": ["rarc_task"]})

    
    ### overrides for bi_ ... _fetch_task  - input ###
    cds.override_node_properties("cds/bi_data/include_all_facility_references",                   {"async_input"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/risk_info/facility_reference2",                             {"async_input"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/risk_info/facility_reference3",                             {"async_input"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/risk_info/facility_reference4",                             {"async_input"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/risk_info/facility_reference5",                             {"async_input"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/risk_info/facility_reference6",                             {"async_input"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/risk_info/facility_reference7",                             {"async_input"   : ["bi_facility_fetch_task","start_renewal_task"],})
    
    #facility detail - list node
    cds.override_node_properties("cds/bi_data/facility_detail",                                   {"async_output"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/date_extracted",                    {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/section_reference",                 {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/insured_party",                     {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/inception_date",                    {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/expiry_date",                       {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/underwriter_name",                  {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 })
    cds.override_node_properties("cds/bi_data/facility_detail/settlement_currency",               {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/section_is_renewal",                {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,})
    cds.override_node_properties("cds/bi_data/facility_detail/division",                          {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/written_or_estimated_signed_line",  {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                       , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                })
    cds.override_node_properties("cds/bi_data/facility_detail/trifocus_name",                     {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 })
    cds.override_node_properties("cds/bi_data/facility_detail/external_acquisition_cost_multiplier", {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                    })
    cds.override_node_properties("cds/bi_data/facility_detail/profit_commission_multiplier",      {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                })
    cds.override_node_properties("cds/bi_data/facility_detail/placing_brokername",                {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/risk_class_code",                   {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/yoa",                               {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/rate_change_divisor",               {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/written_or_estimated_premium",      {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 })
    cds.override_node_properties("cds/bi_data/facility_detail/spot_rate_usd_to_sett",             {"async_output"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/net_beazley_premium_sett_fx",       {"async_output"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/net_100pct_premium_sett_fx",        {"async_output"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/gross_100pct_premium_sett_fx",      {"async_output"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/net_100pct_premium_adjexp_sett_fx", {"async_output"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task","start_renewal_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/include",                           {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"
                                                                                                                        ,"bi_facility_include_all_task"
                                                                                                                        ,"bi_facility_exclude_all_task","start_renewal_task"],})

#claims_listing list node
    cds.override_node_properties("cds/bi_data/claims_listing",                                   {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/date_extracted",                    {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/section_reference",                 {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/claim_reference",                   {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/exposure_reference",                {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/yoa",                               {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/beazley_catcode",                   {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/market_catcode",                    {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    # cds.override_node_properties("cds/bi_data/claims_listing/trifocus_name",                     {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        # , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        # ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/settlement_currency",               {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/block_indicator",                   {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/date_of_loss",                      {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/claim_made_date",                   {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/claim_or_circumstance",             {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/beazley_share_total_incurred",      {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/slip_order_total_incurred",         {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/slip_order_total_paid",             {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/beazley_share_pre_peer_blend",      {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/beazley_share_pre_peer_most_likely",{"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/loss_category",                     {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/bi_paid",                          {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/bi_os",                            {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/bi_incurred",                      {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/pre_peer_blend_incurred",          {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/pre_peer_most_likely_incurred",    {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/show_cat",                         {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/show_large",                       {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_listing/class_rank",                       {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})

    cds.override_node_properties("cds/bi_data/claims_movements",                                {"async_input"    : ["tri_exclusions_setup_task"]
                                                                                                ,"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_movements/date_extracted",                 {"async_input"    : ["tri_exclusions_setup_task"]
                                                                                                ,"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_movements/loss_category",                  {"async_input"    : ["tri_exclusions_setup_task"]
                                                                                                ,"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_movements/yoa",                            {"async_input"    : ["tri_exclusions_setup_task"]
                                                                                                ,"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_movements/mvmt_yr",                        {"async_input"    : ["tri_exclusions_setup_task"]
                                                                                                ,"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/claims_movements/incurredmvmt_100_sett_fx",       {"async_input"    : ["tri_exclusions_setup_task"]
                                                                                                ,"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})



     # renewal task outputs
    cds.override_node_properties("cds/rating_summary/detail_by_year/port_chg_prior",                                    {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/detail_by_year/rate_chg_prior",                                    {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/detail_by_year/infl_chg_prior",                                    {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/detail_by_year/prior_selected_perc_ult",                           {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/detail_by_year/incurred_att_prior",                                {"async_output"   : ["start_renewal_task"],})
    
    cds.override_node_properties("cds/rating_summary/detail_by_year/include_override",                                  {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/detail_by_year/policy_length_override",                            {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/detail_by_year/port_chg_override",                                 {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/detail_by_year/rate_chg_override",                                 {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/detail_by_year/infl_chg_override",                                 {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/detail_by_year/premium_override",                                  {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/detail_by_year/incurred_override",                                 {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/detail_by_year/incurred_cat_override",                             {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/detail_by_year/incurred_large_override",                           {"async_output"   : ["start_renewal_task"],})

    cds.override_node_properties("cds/rating_summary/summary_ratios/attritional/gg_pre_uw_adj/ulr_previous_override",   {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/attritional/gg_pre_uw_adj/ulr_previous",            {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/attritional/gg_pre_uw_adj/ulr_previous_suggested",  {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/large/gg_pre_uw_adj/ulr_previous",                  {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/catastrophe/gg_pre_uw_adj/ulr_previous_exc_nml",    {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/catastrophe/gg_pre_uw_adj/ulr_previous",            {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/total/gn_pre_uw_adj/ulr_prior",                     {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/total/gn_pst_uw_adj/ulr_prior",                     {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/kpi/pre_uw_adj/bpi_prior",                                         {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/kpi/pre_uw_adj/tpi_prior",                                         {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/kpi/pst_uw_adj/bpi_prior",                                         {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/rating_summary/kpi/pst_uw_adj/tpi_prior",                                         {"async_output"   : ["start_renewal_task"],})

    cds.override_node_properties("cds/profit_commission/scenarios/result_exp_pc_payable_override",                      {"async_output"   : ["start_renewal_task"],}) ### we want to clear this value out on renewal

    #cds.override_node_properties("model_state/pressed_start_renewal_task",                                          {"async_output"   : ["start_renewal_task"],})
    #cds.override_node_properties("model_state/expiring_policy",                                                     {"async_output"   : ["start_renewal_task"],})
                                                                                                                        
                                                                                                                        # Override nodes
    #################JK look to see if we could replace this with quoted_premium_100pct ########################################################################################################################
    cds.override_node_properties("cds/layers/premium", {"async_input": ["run_bordereau_rater_task" , "simulate_pc_task"], "view": {"options": {
        "read_only": {"label": "Gross Bound Premium", "read_only": True}
    }}})
    
    cds.override_node_properties("cds/layers/quoted_premium", {"view": {"label": "AFB EPI (Net of Aqn, Gross of PC)"}, "mode": "output", "validation": {"min_value": 0}})
    cds.override_node_properties("cds/layers/bpi_case_priced", {"default": 0, "optionality": "required"})

    # Override dropwown links
    # cds.override_node_properties('cds/standard_fields/underwriter', {"async_output": ["bi_facility_fetch_task"]}) # 'options_table': "table_input_underwriters", 'options_column': "underwriter", 
    
    # Override default values
    cds.override_node_properties('cds/currencies/source_currency', {"default": "USD", "async_input": ["run_bordereau_rater_task", "simulate_pc_task", "bi_clm_and_mvmt_inc_triangles_fetch_task", "bi_clm_and_mvmt_exc_triangles_fetch_task", "generate_uw_rationale_doc_task"], 'view': {'label': "Currency", "options": {
        "rationale": {"label": "Risk Currency", "read_only": True}
    }}})

    # Override Policy Reference name
    cds.override_node_properties('cds/standard_fields/facility_reference', {"async_input": ["bi_facility_fetch_task", "search_exposure_management_data_task", "edm_fetch_task", "generate_uw_rationale_doc_task","start_renewal_task"], 'view': {'label': "Binder Reference", "options": {
        "rationale": {"read_only": True}
    }}})

    # Override Inception and Expiry date
    cds.override_node_properties('cds/standard_fields/inception_date', {"async_input": ["pull_in_exposure_management_data_task", "run_bordereau_rater_task" , "simulate_pc_task", "generate_uw_rationale_doc_task"]})
    cds.override_node_properties('cds/standard_fields/expiry_date', {"async_input": ["pull_in_exposure_management_data_task", "run_bordereau_rater_task" , "simulate_pc_task"]})

    # Override Insured Name label
    cds.override_node_properties('cds/standard_fields/insured_name', {"allow_custom_value": True, "options_table" : "lst_insurednames", "options_column" : "Description", 'async_input': ["run_bordereau_rater_task" , "simulate_pc_task", "generate_uw_rationale_doc_task"], 'view': {'label': "Binder Name", "options": {
        "rationale": {"label": "Coverholder", "read_only": True}
    }}})

    # overrides for BI
    cds.override_node_properties("cds/standard_fields/trifocus",{"view": {"label": "TriFocus"}, "allow_custom_value": True, "options_table": "table_tfgmappings", "options_column": "Trifocus"})
    cds.override_node_properties("cds/standard_fields/broker", {"async_input": ["generate_uw_rationale_doc_task"], 'view': {"options": {
        "rationale": {"label": "Placing Broker", "read_only": True}
    }}})
   

    cds.override_node_properties("cds/standard_fields/benchmark_class", {"mode": "output", "async_input": ["bi_clm_and_mvmt_exc_triangles_fetch_task", "bi_clm_and_mvmt_inc_triangles_fetch_task","run_bordereau_rater_task","simulate_pc_task"]})

    cds.override_node_properties("hx_core/inception_date",{"async_input": ["bi_clm_and_mvmt_inc_triangles_fetch_task", "bi_clm_and_mvmt_exc_triangles_fetch_task","tri_exclusions_setup_task", "tri_override_setup_task"], "view":{"options": {
        "rationale": {"read_only": True}
    }}})
    
    #cds.override_node_properties("cds/standard_fields/is_renewal", {"view": {"label": "Renewal"}, "async_output": ["bi_facility_fetch_task"]})
    

    ##############################
    cds.extend_node_rater_defined("cds", {
        "input_file": hx.File(mode="input", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], file_extension=["csv", "xlsx"], view={"label": "Input File"}),
        "output_file": hx.File(mode="output", async_output=["run_bordereau_rater_task" , "simulate_pc_task"], file_name="output_file.xlsx", view={"label": "Output File"}),
    })

