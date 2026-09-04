########################################################################################################################
####################                        xyz                                                     ####################
########################################################################################################################
###                                                                                                                  ###
########################################################################################################################

import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format, set_node_properties

def sch_async_tasks(cds):


    ### overrides for edm_fetch_task ###
    cds.override_node_properties("cds/rms/edm_reference_lookup",                        {"async_output"   : ["edm_fetch_task"],})
    cds.override_node_properties("cds/rms/edm_reference_lookup/portnum",                {"async_output"   : ["edm_fetch_task"],})

    cds.override_node_properties("cds/rms/fetch_edm_data_reference_lookup_task_status", {"async_output"   : ["edm_fetch_task"],})
    cds.override_node_properties("cds/rms/fetch_edm_data_task_status",                  {"async_output"   : ["edm_fetch_task"],})
    cds.override_node_properties("cds/rms/edm_reference_selected",                      {"async_output"   : ["edm_fetch_task"],})

    cds.override_node_properties("cds/rms/edm",                                         {"async_output"   : ["edm_fetch_task"],})
    cds.override_node_properties("cds/rms/edm/return_period",                           {"async_output"   : ["edm_fetch_task"],})
    cds.override_node_properties("cds/rms/edm/probability",                             {"async_output"   : ["edm_fetch_task"],})
    cds.override_node_properties("cds/rms/edm/portnum",                                 {"async_output"   : ["edm_fetch_task"],})
    cds.override_node_properties("cds/rms/edm/ws_loss_amount",                          {"async_output"   : ["edm_fetch_task"],})
    cds.override_node_properties("cds/rms/edm/ws_premium",                              {"async_output"   : ["edm_fetch_task"],})
    cds.override_node_properties("cds/rms/edm/ws_currency",                             {"async_output"   : ["edm_fetch_task"],})
    cds.override_node_properties("cds/rms/edm/ws_fxrate",                               {"async_output"   : ["edm_fetch_task"],})
    cds.override_node_properties("cds/rms/edm/eq_loss_amount",                          {"async_output"   : ["edm_fetch_task"],})
    cds.override_node_properties("cds/rms/edm/eq_premium",                              {"async_output"   : ["edm_fetch_task"],})
    cds.override_node_properties("cds/rms/edm/eq_currency",                             {"async_output"   : ["edm_fetch_task"],})
    cds.override_node_properties("cds/rms/edm/eq_fxrate",                               {"async_output"   : ["edm_fetch_task"],})



    ### overrides for bi_ ... _fetch_task  - input ###
    cds.override_node_properties("cds/bi_data/include_all_facility_references",                   {"async_input"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/risk_info/facility_reference2",                             {"async_input"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/risk_info/facility_reference3",                             {"async_input"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/risk_info/facility_reference4",                             {"async_input"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/risk_info/facility_reference5",                             {"async_input"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/risk_info/facility_reference6",                             {"async_input"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/risk_info/facility_reference7",                             {"async_input"   : ["bi_facility_fetch_task"],})


    ### overrides for tri_exclusions_setup_task  & tri_override_setup_task
    cds.override_node_properties("cds/triangle_projection/tri_2_manual_input",                   {"async_input"    : ["tri_exclusions_setup_task"]
                                                                                                  ,"async_output"  : ["tri_override_setup_task"],})
    
    cds.override_node_properties("cds/triangle_projection/override_triangle_date",               {"async_input"    : ["tri_override_setup_task"],})
    cds.override_node_properties("cds/triangle_projection/override_triangle_years",              {"async_input"    : ["tri_override_setup_task"],})
    cds.override_node_properties("cds/triangle_projection/async_override_triangle_status",       {"async_output"   : ["tri_override_setup_task"],})
    cds.override_node_properties("cds/triangle_projection/override_triangle_date_used",          {"async_output"   : ["tri_override_setup_task"],})

    cds.override_node_properties("cds/triangle_projection/override_triangle",                    {"async_input"    : ["tri_exclusions_setup_task"],})
    cds.override_node_properties("cds/triangle_projection/tri_3a_exclusions",                    {"async_output"   : ["tri_exclusions_setup_task"],})
    cds.override_node_properties("cds/triangle_projection/tri_exclusions_setup_task_status",     {"async_output"   : ["tri_exclusions_setup_task"],})





    cds.override_node_properties("cds/layers/commission",                                       {"async_output"   : [{"task": "bi_facility_fetch_task", "reset": False}],})
    cds.override_node_properties("cds/layers/quoted_premium_100pct",                            {"async_input"    : ["simulate_pc_task"],
                                                                                                 "async_output"   : [{"task": "bi_facility_fetch_task", "reset": False}
                                                                                                                      ,{"task": "bi_clm_and_mvmt_inc_triangles_fetch_task", "reset": False}
                                                                                                                      ,{"task": "bi_clm_and_mvmt_exc_triangles_fetch_task", "reset": False} ],}) ### done as part of this task due to necessary fx conversion

    cds.override_node_properties("cds/bi_data/fetch_facility_detail_task_status",               {"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/fetch_clm_and_mvmt_detail_task_status",           {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"],})
    cds.override_node_properties("cds/risk_info/bic_data_asat",                                 {"async_input"    : ["tri_exclusions_setup_task"],
                                                                                                 "async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"],})


    cds.override_node_properties("cds/bi_data/triangles_loaded",                                {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"],})


    #facility detail - list node
    cds.override_node_properties("cds/bi_data/facility_detail",                                   {"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/date_extracted",                    {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/section_reference",                 {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/insured_party",                     {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/inception_date",                    {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/expiry_date",                       {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/underwriter_name",                  {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/settlement_currency",               {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/section_is_renewal",                {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/division",                          {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/written_or_estimated_signed_line",  {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/trifocus_name",                     {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/external_acquisition_cost_multiplier", {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                    ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/profit_commission_multiplier",      {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/placing_brokername",                {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/risk_class_code",                   {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/yoa",                               {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/rate_change_divisor",               {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/written_or_estimated_premium",      {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/spot_rate_usd_to_sett",             {"async_output"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/net_beazley_premium_sett_fx",       {"async_output"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/net_100pct_premium_sett_fx",        {"async_output"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/gross_100pct_premium_sett_fx",      {"async_output"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/net_100pct_premium_adjexp_sett_fx", {"async_output"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
    cds.override_node_properties("cds/bi_data/facility_detail/include",                           {"async_input"    : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"]
                                                                                                 ,"async_output"   : ["bi_facility_fetch_task"
                                                                                                                        ,"bi_facility_include_all_task"
                                                                                                                        ,"bi_facility_exclude_all_task"],})

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
    cds.override_node_properties("cds/bi_data/claims_listing/trifocus_name",                     {"async_output"   : ["bi_clm_and_mvmt_inc_triangles_fetch_task"
                                                                                                                        , "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                                                                                                        ,"bi_facility_fetch_task"],})
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


    # profit_commission scenario list node inputs
    cds.override_node_properties("cds/profit_commission/scenarios",                             {"async_input"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/label",                       {"async_input"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/include",                     {"async_input"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/complete",                    {"async_input"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/share",                       {"async_input"   : ["simulate_pc_task"]
                                                                                                ,"async_output"  : [{"task": "bi_facility_fetch_task", "reset": False}], })
    cds.override_node_properties("cds/profit_commission/scenarios/expenses",                    {"async_input"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/basis",                       {"async_input"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/deficit",                     {"async_input"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/additionalfeaturesindicator", {"async_input"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/threshold_bonus_share",       {"async_input"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/threshold_lr_cutoff",         {"async_input"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/slidingscale_bonus_lr",       {"async_input"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/slidingscale_bonus_scale",    {"async_input"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/slidingscale_bonus_maxtotalpc",{"async_input"  : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/slidingscale_clawback_lr",    {"async_input"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/slidingscale_clawback_scale", {"async_input"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/slidingscale_clawback_mintotalpc",{"async_input":["simulate_pc_task"],})
    cds.override_node_properties("cds/layers/total_deductions",                                 {"async_input"   : ["simulate_pc_task"
                                                                                                                        ,"generate_uw_doc_task"]})



    # profit_commission individual node outputs
    cds.override_node_properties("cds/profit_commission/param_attritional/distribution",        {"async_input":["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/param_attritional/param_1",             {"async_input":["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/param_attritional/param_2",             {"async_input":["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/param_attritional/expected_loss",       {"async_input":["simulate_pc_task"],})

    cds.override_node_properties("cds/profit_commission/param_large/distribution",              {"async_input":["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/param_large/param_1",                   {"async_input":["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/param_large/param_2",                   {"async_input":["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/param_large/expected_loss",             {"async_input":["simulate_pc_task"],})

    cds.override_node_properties("cds/profit_commission/param_cat_natural/distribution",        {"async_input":["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/param_cat_natural/param_1",             {"async_input":["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/param_cat_natural/param_2",             {"async_input":["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/param_cat_natural/expected_loss",       {"async_input":["simulate_pc_task"],})

    cds.override_node_properties("cds/profit_commission/param_cat_other/distribution",          {"async_input":["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/param_cat_other/param_1",               {"async_input":["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/param_cat_other/param_2",               {"async_input":["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/param_cat_other/expected_loss",         {"async_input":["simulate_pc_task"],})



    # profit_commission scenario list node outputs
    cds.override_node_properties("cds/profit_commission/scenarios/result_exp_loss_att",         {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/result_exp_loss_large",       {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/result_exp_loss_cat_other",   {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/result_exp_loss_cat_natural", {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/result_exp_loss_total",       {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/result_exp_pc_payable",       {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/result_exp_frequency_loss",   {"async_output"   : ["simulate_pc_task"],})

    cds.override_node_properties("cds/profit_commission/scenarios/result_param_1_att",          {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/result_param_1_large",        {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/result_param_1_cat_other",    {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/result_param_1_cat_natural",  {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/result_param_2_att",          {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/result_param_2_large",        {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/result_param_2_cat_other",    {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/scenarios/result_param_2_cat_natural",  {"async_output"   : ["simulate_pc_task"],})



    # profit_commission dsitribution list node outputs
    cds.override_node_properties("cds/profit_commission/distributions",                         {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/distributions/scenario",                {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/distributions/bucket",                  {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/distributions/ulr",                     {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/distributions/uw_profit",               {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/distributions/pc_payable",              {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/distributions/pdf_att",                 {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/distributions/pdf_large",               {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/distributions/pdf_cat_other",           {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/distributions/pdf_cat_natural",         {"async_output"   : ["simulate_pc_task"],})
    cds.override_node_properties("cds/profit_commission/distributions/pdf_total",               {"async_output"   : ["simulate_pc_task"],})

    # profit_commission individual node outputs
    cds.override_node_properties("cds/profit_commission/simulate_pc_task_status",               {"async_output"   : ["simulate_pc_task"],})



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

    cds.override_node_properties("cds/model_state/pressed_start_renewal_task",                                          {"async_output"   : ["start_renewal_task"],})
    cds.override_node_properties("cds/model_state/expiring_policy",                                                     {"async_output"   : ["start_renewal_task"],})

    cds.override_node_properties("cds/model_state/migrated_record",                                                     {"async_output"   : ["set_migration_flag_task"],})


    # nodes specific to generate_uw_doc_task
    cds.override_node_properties("cds/rating_summary/technical/gg_premium_quoted_100_pct",                          {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/technical/gn_premium_quoted_exc_pc_100_pct",                   {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/technical/gg_premium_quoted_afb",                              {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/technical/gn_premium_quoted_exc_pc_afb",                       {"async_input"   : ["generate_uw_doc_task"],})

    cds.override_node_properties("cds/rating_summary/technical/amts_pst_uw_adj/gg_premium_tech_100_pct",            {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/technical/amts_pst_uw_adj/gn_premium_tech_exc_pc_100_pct",     {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/technical/amts_pst_uw_adj/gg_premium_tech_afb",                {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/technical/amts_pst_uw_adj/gn_premium_tech_exc_pc_afb",         {"async_input"   : ["generate_uw_doc_task"],})

    cds.override_node_properties("cds/rating_summary/technical/amts_pst_uw_adj/gg_premium_bench_100_pct",           {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/technical/amts_pst_uw_adj/gn_premium_bench_exc_pc_100_pct",    {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/technical/amts_pst_uw_adj/gg_premium_bench_afb",               {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/technical/amts_pst_uw_adj/gn_premium_bench_exc_pc_afb",        {"async_input"   : ["generate_uw_doc_task"],})

    cds.override_node_properties("cds/rating_summary/summary_ratios/attritional/gg_pre_uw_adj/ulr_final",           {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/attritional/gn_pre_uw_adj/ulr_final",           {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/attritional/gg_pst_uw_adj/ulr_final",           {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/attritional/gn_pst_uw_adj/ulr_final",           {"async_input"   : ["generate_uw_doc_task"],})

    cds.override_node_properties("cds/rating_summary/summary_ratios/large/gg_pre_uw_adj/ulr_final",                 {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/large/gn_pre_uw_adj/ulr_final",                 {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/large/gg_pst_uw_adj/ulr_final",                 {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/large/gn_pst_uw_adj/ulr_final",                 {"async_input"   : ["generate_uw_doc_task"],})

    cds.override_node_properties("cds/rating_summary/summary_ratios/catastrophe/gg_pre_uw_adj/ulr_final",           {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/catastrophe/gn_pre_uw_adj/ulr_final",           {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/catastrophe/gg_pst_uw_adj/ulr_final",           {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/catastrophe/gn_pst_uw_adj/ulr_final",           {"async_input"   : ["generate_uw_doc_task"],})

    cds.override_node_properties("cds/rating_summary/summary_ratios/total/gg_pre_uw_adj/ulr_priced_final",          {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/total/gn_pre_uw_adj/ulr_priced_final_exc_pc",   {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/total/gg_pst_uw_adj/ulr_priced_final",          {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/total/gn_pst_uw_adj/ulr_priced_final_exc_pc",   {"async_input"   : ["generate_uw_doc_task"],})

    cds.override_node_properties("cds/rating_summary/summary_ratios/attritional/uw_adjustment",                     {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/large/uw_adjustment",                           {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/summary_ratios/catastrophe/uw_adjustment",                     {"async_input"   : ["generate_uw_doc_task"],})

    cds.override_node_properties("cds/rating_summary/kpi/pre_uw_adj/expected_profit",                               {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/kpi/pre_uw_adj/allocated_capital",                             {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/kpi/pre_uw_adj/roc",                                           {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/kpi/pre_uw_adj/bpi",                                           {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/kpi/pre_uw_adj/tpi",                                           {"async_input"   : ["generate_uw_doc_task"],})


    cds.override_node_properties("cds/rating_summary/kpi/pst_uw_adj/expected_profit",                               {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/kpi/pst_uw_adj/allocated_capital",                             {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/kpi/pst_uw_adj/roc",                                           {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/kpi/pst_uw_adj/bpi",                                           {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/kpi/pst_uw_adj/tpi",                                           {"async_input"   : ["generate_uw_doc_task"],})

    cds.override_node_properties("cds/rating_summary/technical/percent_pc",                                         {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/technical/amount_pc_100",                                      {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rating_summary/technical/amount_pc_afb",                                      {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/standard_fields/uw_rationale",                                                {"async_input"   : ["generate_uw_doc_task"],})
    cds.override_node_properties("cds/rationale/actuarial_review",                                                  {"async_input"   : ["generate_uw_doc_task"],})

    cds.override_node_properties("cds/layers/rate_change/rate_change/uw_selected",                                  {"async_input"   : ["generate_uw_doc_task"],"view":{"label": "UW Selected %", "format": {"output": "percent", "mantissa": 2}}})





