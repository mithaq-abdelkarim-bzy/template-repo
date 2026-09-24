# v0.5.0
import hx
import pandas as pd
import numpy as np
import math as math
import json
from algorithms.rate_utilities import title_rc, ratio, usd, to_ccy, look_up
from operator import itemgetter

from algorithms.rate_constants import max_layers
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import COVERAGES_LIST

from algorithms import parameter_tables_schema as params

# -----------------------------------------------------------------------------
# NOTE
# As we need the rate change buckets to align with the PMD we have grouped
# brokerage and other into 'other incl. brokerage' and allocated other node below. 
# Brokerage will be calculated seperately in the rarc_task but not displayed standalone.
# -----------------------------------------------------------------------------

# NOTE: Provide the bucket information according to the value set to RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE in algorithms.data_schema.sch_rater_defined.py. The unused case can be removed.
if not RARC_COVERAGE_USE and not RARC_INSURED_ASSET_USE:
    RATE_CHANGE_BUCKETS_STEER = {
        "model": [], # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": [
            "hx_core/inception_date",
            "hx_core/expiry_date",
            "cds/layers/include_layer",

            # # not bearing premium
            # "cds/key_industry/code_type",
            # "cds/key_industry/code",
            # "cds/key_industry/code_name",
            # # not bearing premium
            # "cds/standard_fields/insured_name",
            # "cds/standard_fields/broker",
            # "cds/standard_fields/insured_country",
            # "cds/standard_fields/insured_postal_code",
            # "cds/standard_fields/insured_state_or_province",
            # "cds/standard_fields/is_admitted_or_surplus",
            # "cds/standard_fields/is_free_trade_zone",
            # "cds/standard_fields/is_renewal",
            # "cds/standard_fields/underwriter",
            # "cds/standard_fields/policy_reference",
            # "cds/standard_fields/facility_reference",
            # "cds/standard_fields/benchmark_class",
            # "cds/standard_fields/uw_rationale",
            # "cds/standard_fields/trifocus",
            # "cds/standard_fields/rating_methodology",


            # "cds/layers/section_reference",
            
            # "cds/layers/written_line",
            # "cds/layers/premium", # not used
            # "cds/layers/status", # not premiums bearing
            # "cds/layers/is_primary_excess", # not premiums bearing
            # "cds/layers/trifocus", # not premiums bearing



            # # removed since the result of the advanced features are input node async output read_only
            # "cds/layers/advanced_features_input/aad",
            # "cds/layers/loss_corridor/min_rate",
            # "cds/layers/loss_corridor/max_rate",
            # "cds/layers/loss_corridor/insured_participation",
            # "cds/layers/swing_rates/swing_brokerage",
            # "cds/layers/swing_rates/use_swing_brokerage",
            # "cds/layers/swing_rates/deposit_rate",
            # "cds/layers/swing_rates/min_rate",
            # "cds/layers/swing_rates/max_rate",
            # "cds/layers/swing_rates/margin",
            # "cds/layers/swing_rates/loading_factor",
            # "cds/layers/swing_rates/claims_cap_pct",

            "cds/layers/epi_100",
            "cds/layers/rate",
            "cds/layers/ceding_commission",
            # "cds/layers/ncb",
            # "cds/layers/profit_commission_rate",
            # "cds/layers/expense_allowance",
            "cds/layers/bkg_gross_or_net",
            # "cds/layers/cap_gross_pct",
            # "cds/layers/no_reinstatement",
            # "cds/layers/reinstatement_pct_1",
            # "cds/layers/reinstatement_pct_2",
            # "cds/layers/reinstatement_pct_3",
            # "cds/layers/reinstatement_pct_4",
            # "cds/layers/reinstatement_pct_5",
            # "cds/layers/reinstatement_pct_6",
            # "cds/layers/reinstatement_pct_7",
            # "cds/layers/reinstatement_pct_8",
            # "cds/layers/reinstatement_pct_9",
            # "cds/layers/reinstatement_pct_10",


            "cds/layers/pricing_selection/risk_profile_bdx/weighting",
            "cds/layers/pricing_selection/limit_average_severity/weighting",
            "cds/layers/pricing_selection/burning_cost/weighting",
            "cds/layers/pricing_selection/clash/weighting",
            "cds/layers/pricing_selection/healthcare_cat/weighting",
            "cds/layers/pricing_selection/other_method/pure_rate",
            "cds/layers/pricing_selection/other_method/weighting",
            "cds/layers/risk_profile_bdx/glr_pick",

            # "cds/currencies/target_currency", # not used
            "cds/currencies/source_currency",
            # "cds/currencies/multi_currency_support", # not used
            # "cds/currencies/rates/code", # not used
            # "cds/currencies/rates/rate", # not used

            # "cds/experience_rating/claims_available", # not used
            # "cds/experience_rating/claims_fgu", # not used
            # "cds/experience_rating/claims_net_of_deductible", # not used

            # "cds/risk_information/broker_contact", # not premium bearing
            # "cds/risk_information/case_pricing_analysis_location", # not premium bearing




            # "cds/risk_information/comments", # not premium bearing
            # "cds/metadata/rater", # not premium bearing

            "cds/technical_price_assumptions/select_class",

            # "cds/steer/risk_information/database_id", # Old process, not used
            # "cds/steer/risk_information/application_date",# Old process, not used
            # "cds/steer/risk_information/deal_status",# Old process, not used
            # "cds/steer/risk_information/clearance_status",# Old process, not used
            # "cds/steer/risk_information/basis",# Old process, not used
            # "cds/steer/risk_information/new_replacement",# Old process, not used

            "cds/steer/experience_rating/on_levelling/measure",
            "cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure",
            "cds/steer/experience_rating/on_levelling/exposure_assumptions/annual_rate_change",
            "cds/steer/experience_rating/on_levelling/exposure_assumptions/claims_inflation",
            "cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure_adjusted_layer_01",
            "cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure_adjusted_layer_02",
            "cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure_adjusted_layer_03",
            "cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure_adjusted_layer_04",
            "cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure_adjusted_layer_05",
            "cds/steer/experience_rating/on_levelling/future_inflation",
            ## removed since the pattern is an input node async output 
            # "cds/steer/experience_rating/raw_data/column_01",
            # "cds/steer/experience_rating/raw_data/column_02",
            # "cds/steer/experience_rating/raw_data/column_03",
            # "cds/steer/experience_rating/raw_data/column_04",
            # "cds/steer/experience_rating/raw_data/column_05",
            # "cds/steer/experience_rating/raw_data/column_06",
            # "cds/steer/experience_rating/raw_data/column_07",
            # "cds/steer/experience_rating/raw_data/column_08",
            # "cds/steer/experience_rating/raw_data/column_09",
            # "cds/steer/experience_rating/raw_data/column_10",
            # "cds/steer/experience_rating/raw_data/column_11",
            # "cds/steer/experience_rating/raw_data/column_12",
            # "cds/steer/experience_rating/raw_data/column_13",
            # "cds/steer/experience_rating/raw_data/column_14",
            # "cds/steer/experience_rating/raw_data/column_15",
            # "cds/steer/experience_rating/raw_data/column_16",
            # "cds/steer/experience_rating/raw_data/column_17",
            # "cds/steer/experience_rating/raw_data/column_18",
            # "cds/steer/experience_rating/raw_data/column_19",
            # "cds/steer/experience_rating/raw_data/column_20",
            # "cds/steer/experience_rating/raw_data/column_21",
            # "cds/steer/experience_rating/raw_data/column_22",
            # "cds/steer/experience_rating/raw_data/column_23",
            # "cds/steer/experience_rating/raw_data/column_24",
            # "cds/steer/experience_rating/raw_data/column_25",
            # "cds/steer/experience_rating/raw_data/column_26",
            # "cds/steer/experience_rating/raw_data/column_27",
            # "cds/steer/experience_rating/raw_data/column_28",
            # "cds/steer/experience_rating/raw_data/column_29",
            # "cds/steer/experience_rating/raw_data/column_30",
            # "cds/steer/experience_rating/raw_data/column_31",
            # "cds/steer/experience_rating/raw_data/column_32",
            # "cds/steer/experience_rating/raw_data/column_33",
            # "cds/steer/experience_rating/raw_data/column_34",
            # "cds/steer/experience_rating/raw_data/column_35",
            # "cds/steer/experience_rating/raw_data/column_36",
            # "cds/steer/experience_rating/raw_data/column_37",
            # "cds/steer/experience_rating/raw_data/column_38",
            # "cds/steer/experience_rating/raw_data/column_39",
            # "cds/steer/experience_rating/raw_data/column_40",
            # "cds/steer/experience_rating/raw_data/column_41",
            # "cds/steer/experience_rating/raw_data/column_42",
            # "cds/steer/experience_rating/raw_data/column_43",
            # "cds/steer/experience_rating/raw_data/column_44",
            # "cds/steer/experience_rating/raw_data/column_45",
            # "cds/steer/experience_rating/raw_data/column_46",
            # "cds/steer/experience_rating/raw_data/column_47",
            # "cds/steer/experience_rating/raw_data/column_48",
            # "cds/steer/experience_rating/raw_data/column_49",
            # "cds/steer/experience_rating/raw_data/column_50",
            # "cds/steer/experience_rating/raw_data/column_51",
            # "cds/steer/experience_rating/raw_data/column_52",
            # "cds/steer/experience_rating/raw_data/column_53",
            # "cds/steer/experience_rating/raw_data/column_54",
            # "cds/steer/experience_rating/raw_data/column_55",
            # "cds/steer/experience_rating/raw_data/column_56",
            # "cds/steer/experience_rating/raw_data/column_57",
            # "cds/steer/experience_rating/raw_data/column_58",
            # "cds/steer/experience_rating/raw_data/column_59",
            # "cds/steer/experience_rating/raw_data/column_60",
            # "cds/steer/experience_rating/raw_data/column_61",
            # "cds/steer/experience_rating/raw_data/column_62",
            # "cds/steer/experience_rating/raw_data/column_63",
            # "cds/steer/experience_rating/raw_data/column_64",
            # "cds/steer/experience_rating/raw_data/column_65",
            # "cds/steer/experience_rating/raw_data/column_66",
            # "cds/steer/experience_rating/raw_data/column_67",
            # "cds/steer/experience_rating/raw_data/column_68",
            # "cds/steer/experience_rating/raw_data/column_69",
            # "cds/steer/experience_rating/raw_data/column_70",
            # "cds/steer/experience_rating/raw_data/column_71",
            # "cds/steer/experience_rating/raw_data/column_72",
            # "cds/steer/experience_rating/raw_data/column_73",
            # "cds/steer/experience_rating/raw_data/column_74",
            # "cds/steer/experience_rating/raw_data/column_75",
            # "cds/steer/experience_rating/raw_data/column_76",
            # "cds/steer/experience_rating/raw_data/column_77",
            # "cds/steer/experience_rating/raw_data/column_78",
            # "cds/steer/experience_rating/raw_data/column_79",
            # "cds/steer/experience_rating/raw_data/column_80",
            # "cds/steer/experience_rating/raw_data/column_81",
            # "cds/steer/experience_rating/raw_data/column_82",
            # "cds/steer/experience_rating/raw_data/column_83",
            # "cds/steer/experience_rating/raw_data/column_84",
            # "cds/steer/experience_rating/raw_data/column_85",
            # "cds/steer/experience_rating/raw_data/column_86",
            # "cds/steer/experience_rating/raw_data/column_87",
            # "cds/steer/experience_rating/raw_data/column_88",
            # "cds/steer/experience_rating/raw_data/column_89",
            # "cds/steer/experience_rating/raw_data/column_90",
            # "cds/steer/experience_rating/raw_data/column_91",
            # "cds/steer/experience_rating/raw_data/column_92",
            # "cds/steer/experience_rating/raw_data/column_93",
            # "cds/steer/experience_rating/raw_data/column_94",
            # "cds/steer/experience_rating/raw_data/column_95",
            # "cds/steer/experience_rating/raw_data/column_96",
            # "cds/steer/experience_rating/raw_data/column_97",
            # "cds/steer/experience_rating/raw_data/column_98",
            # "cds/steer/experience_rating/raw_data/column_99",
            # "cds/steer/experience_rating/raw_data/column_100",
            # "cds/steer/experience_rating/raw_data/column_101",
            # "cds/steer/experience_rating/raw_data/column_102",
            # "cds/steer/experience_rating/raw_data/column_103",
            # "cds/steer/experience_rating/raw_data/column_104",
            # "cds/steer/experience_rating/raw_data/column_105",
            # "cds/steer/experience_rating/raw_data/column_106",
            # "cds/steer/experience_rating/raw_data/column_107",
            # "cds/steer/experience_rating/raw_data/column_108",
            # "cds/steer/experience_rating/raw_data/column_109",

            ## Mapping only
            # "cds/steer/experience_rating/misc_parameters/closed_indicator",
            # "cds/steer/experience_rating/misc_parameters/data_layout",
            # "cds/steer/experience_rating/data_mapping/field_01/specify_column",
            # "cds/steer/experience_rating/data_mapping/field_02/specify_column",
            # "cds/steer/experience_rating/data_mapping/field_03/specify_column",
            # "cds/steer/experience_rating/data_mapping/field_04/specify_column",
            # "cds/steer/experience_rating/data_mapping/field_05/specify_column",
            # "cds/steer/experience_rating/data_mapping/field_06/specify_column",
            # "cds/steer/experience_rating/data_mapping/field_07/specify_column",
            # "cds/steer/experience_rating/data_mapping/field_08/specify_column",
            # "cds/steer/experience_rating/data_mapping/field_09/specify_column",
            # "cds/steer/experience_rating/data_mapping/field_10/specify_column",
            # "cds/steer/experience_rating/data_mapping/field_11/specify_column",
            # "cds/steer/experience_rating/data_mapping/field_12/specify_column",
            # "cds/steer/experience_rating/data_mapping/field_13/specify_column",
            # "cds/steer/experience_rating/data_mapping/field_14/specify_column",
            # "cds/steer/experience_rating/data_mapping/field_15/specify_column",
            # "cds/steer/experience_rating/data_mapping/field_16/specify_column",
            # "cds/steer/experience_rating/data_mapping/field_17/specify_column",
            # "cds/steer/experience_rating/data_mapping/field_18/specify_column",

            "cds/steer/experience_rating/other_fields/fvy/value",
            
            "cds/steer/experience_rating/other_fields/data_as_at_date/value",

            # "cds/steer/experience_rating/column_display/reference/show",
            # "cds/steer/experience_rating/column_display/claimant/show",
            # "cds/steer/experience_rating/column_display/insured/show",
            # "cds/steer/experience_rating/column_display/status/show",
            # "cds/steer/experience_rating/column_display/incident_date/show",
            # "cds/steer/experience_rating/column_display/report_date/show",
            # "cds/steer/experience_rating/column_display/closed_date/show",
            # "cds/steer/experience_rating/column_display/incident_year/show",
            # "cds/steer/experience_rating/column_display/policy_year/show",
            # "cds/steer/experience_rating/column_display/closed_year/show",
            # "cds/steer/experience_rating/column_display/policy_limit/show",
            # "cds/steer/experience_rating/column_display/policy_excess/show",
            # "cds/steer/experience_rating/column_display/paid/show",
            # "cds/steer/experience_rating/column_display/incurred/show",
            # "cds/steer/experience_rating/column_display/paid_expenses/show",
            # "cds/steer/experience_rating/column_display/incurred_expenses/show",
            # "cds/steer/experience_rating/column_display/paid_claim_ind/show",
            # "cds/steer/experience_rating/column_display/inc_claim_ind/show",
            # "cds/steer/experience_rating/column_display/incurred_claims/show",
            # "cds/steer/experience_rating/column_display/inflated_claims/show",
            # "cds/steer/experience_rating/column_display/incurred_capped/show",
            # "cds/steer/experience_rating/column_display/trended_claim/show",
            # "cds/steer/experience_rating/column_display/trended_expenses/show",
            # "cds/steer/experience_rating/column_display/ri_claim/show",
            # "cds/steer/experience_rating/column_display/ri_claim_on_levelled/show",
            # "cds/steer/experience_rating/column_display/ri_claim_count/show",
            # "cds/steer/experience_rating/column_display/ri_claim_count_on_levelled/show",
            # "cds/steer/experience_rating/column_display/claim_ranking/show",
            # "cds/steer/experience_rating/column_display/row_number/show",
            # "cds/steer/experience_rating/raw_data_error/pre_val_err_messages",

            "cds/steer/experience_rating/layers/layer_01/burning_cost/weighting",
            "cds/steer/experience_rating/layers/layer_01/burning_cost/premium",
            "cds/steer/experience_rating/layers/layer_01/pattern_type",
            # "cds/steer/experience_rating/layers/layer_01/bc_comment", # no premium bearring
            # "cds/steer/experience_rating/layers/layer_01/triangle_projection/selected_average_option_input",
            # "cds/steer/experience_rating/layers/layer_01/triangle_projection/override_triangle",
            # "cds/steer/experience_rating/layers/layer_01/triangle_projection/override_triangle_date",
            # "cds/steer/experience_rating/layers/layer_01/triangle_projection/override_triangle_date_used",
            # "cds/steer/experience_rating/layers/layer_01/triangle_projection/override_triangle_years",
            # "cds/steer/experience_rating/layers/layer_01/triangle_projection/benchmark_name/override",
            # "cds/steer/experience_rating/layers/layer_01/triangle_projection/experience_weight/override",
            # "cds/steer/experience_rating/layers/layer_01/triangle_projection/benchmark_use_occurrence",
            # "cds/steer/experience_rating/layers/layer_01/triangle_projection/tri_1_basis",
            # "cds/steer/experience_rating/layers/layer_01/triangle_projection/tri_2_manual_input",
            # "cds/steer/experience_rating/layers/layer_01/triangle_projection/tri_3a_exclusions",
            "cds/steer/experience_rating/layers/layer_01/triangle_projection/incremental_dev_factor/experience_selected_set_in_task",
            "cds/steer/experience_rating/layers/layer_01/triangle_projection/tail_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/layer_01/claim_count/selected_average_option_input",
            # "cds/steer/experience_rating/layers/layer_01/claim_count/override_triaingle",
            # "cds/steer/experience_rating/layers/layer_01/claim_count/override_triangle_date",
            # "cds/steer/experience_rating/layers/layer_01/claim_count/override_triangle_date_used",
            # "cds/steer/experience_rating/layers/layer_01/claim_count/override_triangle_years",
            # "cds/steer/experience_rating/layers/layer_01/claim_count/benchmark_name/override",
            # "cds/steer/experience_rating/layers/layer_01/claim_count/experience_weight/override",
            # "cds/steer/experience_rating/layers/layer_01/claim_count/benchmark_use_occurrence",
            # "cds/steer/experience_rating/layers/layer_01/claim_count/tri_1_basis",
            # "cds/steer/experience_rating/layers/layer_01/claim_count/tri_2_manual_input",
            # "cds/steer/experience_rating/layers/layer_01/claim_count/tri_3a_exclusons",
            "cds/steer/experience_rating/layers/layer_01/claim_count/incremental_dev_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/layer_01/claim_count/tail_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/layer_01/layer_name", # non premium bearings

            "cds/steer/experience_rating/layers/layer_02/burning_cost/weighting",
            "cds/steer/experience_rating/layers/layer_02/burning_cost/premium",
            "cds/steer/experience_rating/layers/layer_02/pattern_type",
            # "cds/steer/experience_rating/layers/layer_02/bc_comment",
            # "cds/steer/experience_rating/layers/layer_02/triangle_projection/selected_average_option_input",
            # "cds/steer/experience_rating/layers/layer_02/triangle_projection/override_triangle",
            # "cds/steer/experience_rating/layers/layer_02/triangle_projection/override_triangle_date",
            # "cds/steer/experience_rating/layers/layer_02/triangle_projection/override_triangle_date_used",
            # "cds/steer/experience_rating/layers/layer_02/triangle_projection/override_triangle_years",
            # "cds/steer/experience_rating/layers/layer_02/triangle_projection/benchmark_name/override",
            # "cds/steer/experience_rating/layers/layer_02/triangle_projection/experience_weight/override",
            # "cds/steer/experience_rating/layers/layer_02/triangle_projection/benchmark_use_occurrence",
            # "cds/steer/experience_rating/layers/layer_02/triangle_projection/tri_1_basis",
            # "cds/steer/experience_rating/layers/layer_02/triangle_projection/tri_2_manual_input",
            # "cds/steer/experience_rating/layers/layer_02/triangle_projection/tri_3a_exclusions",
            "cds/steer/experience_rating/layers/layer_02/triangle_projection/incremental_dev_factor/experience_selected_set_in_task",
            "cds/steer/experience_rating/layers/layer_02/triangle_projection/tail_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/layer_02/claim_count/selected_average_option_input",
            # "cds/steer/experience_rating/layers/layer_02/claim_count/override_triangle",
            # "cds/steer/experience_rating/layers/layer_02/claim_count/override_triangle_date",
            # "cds/steer/experience_rating/layers/layer_02/claim_count/override_triangle_date_used",
            # "cds/steer/experience_rating/layers/layer_02/claim_count/override_triangle_years",
            # "cds/steer/experience_rating/layers/layer_02/claim_count/benchmark_name/override",
            # "cds/steer/experience_rating/layers/layer_02/claim_count/experience_weight/override",
            # "cds/steer/experience_rating/layers/layer_02/claim_count/benchmark_use_occurrence",
            # "cds/steer/experience_rating/layers/layer_02/claim_count/tri_1_basis",
            # "cds/steer/experience_rating/layers/layer_02/claim_count/tri_2_manual_input",
            # "cds/steer/experience_rating/layers/layer_02/claim_count/tri_3a_exclusions",
            "cds/steer/experience_rating/layers/layer_02/claim_count/incremental_dev_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/layer_02/claim_count/tail_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/layer_02/layer_name",

            "cds/steer/experience_rating/layers/layer_03/burning_cost/weighting",
            "cds/steer/experience_rating/layers/layer_03/burning_cost/premium",
            "cds/steer/experience_rating/layers/layer_03/pattern_type",
            # "cds/steer/experience_rating/layers/layer_03/bc_comment",
            # "cds/steer/experience_rating/layers/layer_03/triangle_projection/selected_average_option_input",
            # "cds/steer/experience_rating/layers/layer_03/triangle_projection/override_triangle",
            # "cds/steer/experience_rating/layers/layer_03/triangle_projection/override_triangle_date",
            # "cds/steer/experience_rating/layers/layer_03/triangle_projection/override_triangle_date_used",
            # "cds/steer/experience_rating/layers/layer_03/triangle_projection/override_triangle_years",
            # "cds/steer/experience_rating/layers/layer_03/triangle_projection/benchmark_name/override",
            # "cds/steer/experience_rating/layers/layer_03/triangle_projection/experience_weight/override",
            # "cds/steer/experience_rating/layers/layer_03/triangle_projection/benchmark_use_occurrence",
            # "cds/steer/experience_rating/layers/layer_03/triangle_projection/tri_1_basis",
            # "cds/steer/experience_rating/layers/layer_03/triangle_projection/tri_2_manual_input",
            # "cds/steer/experience_rating/layers/layer_03/triangle_projection/tri_3a_exclusions",
            "cds/steer/experience_rating/layers/layer_03/triangle_projection/incremental_dev_factor/experience_selected_set_in_task",
            "cds/steer/experience_rating/layers/layer_03/triangle_projection/tail_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/layer_03/claim_count/selected_average_option_input",
            # "cds/steer/experience_rating/layers/layer_03/claim_count/override_triangle",
            # "cds/steer/experience_rating/layers/layer_03/claim_count/override_triangle_date",
            # "cds/steer/experience_rating/layers/layer_03/claim_count/override_triangle_date_used",
            # "cds/steer/experience_rating/layers/layer_03/claim_count/override_triangle_years",
            # "cds/steer/experience_rating/layers/layer_03/claim_count/benchmark_name/override",
            # "cds/steer/experience_rating/layers/layer_03/claim_count/experience_weight/override",
            # "cds/steer/experience_rating/layers/layer_03/claim_count/benchmark_use_occurrence",
            # "cds/steer/experience_rating/layers/layer_03/claim_count/tri_1_basis",
            # "cds/steer/experience_rating/layers/layer_03/claim_count/tri_2_manual_input",
            # "cds/steer/experience_rating/layers/layer_03/claim_count/tri_3a_exclusions",
            "cds/steer/experience_rating/layers/layer_03/claim_count/incremental_dev_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/layer_03/claim_count/tail_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/layer_03/layer_name",

            "cds/steer/experience_rating/layers/layer_04/burning_cost/weighting",
            "cds/steer/experience_rating/layers/layer_04/burning_cost/premium",
            "cds/steer/experience_rating/layers/layer_04/pattern_type",
            # "cds/steer/experience_rating/layers/layer_04/bc_comment",
            # "cds/steer/experience_rating/layers/layer_04/triangle_projection/selected_average_option_input",
            # "cds/steer/experience_rating/layers/layer_04/triangle_projection/override_triangle",
            # "cds/steer/experience_rating/layers/layer_04/triangle_projection/override_triangle_date",
            # "cds/steer/experience_rating/layers/layer_04/triangle_projection/override_triangle_date_used",
            # "cds/steer/experience_rating/layers/layer_04/triangle_projection/override_triangle_years",
            # "cds/steer/experience_rating/layers/layer_04/triangle_projection/benchmark_name/override",
            # "cds/steer/experience_rating/layers/layer_04/triangle_projection/experience_weight/override",
            # "cds/steer/experience_rating/layers/layer_04/triangle_projection/benchmark_use_occurrence",
            # "cds/steer/experience_rating/layers/layer_04/triangle_projection/tri_1_basis",
            # "cds/steer/experience_rating/layers/layer_04/triangle_projection/tri_2_manual_input",
            # "cds/steer/experience_rating/layers/layer_04/triangle_projection/tri_3a_exclusions",
            "cds/steer/experience_rating/layers/layer_04/triangle_projection/incremental_dev_factor/experience_selected_set_in_task",
            "cds/steer/experience_rating/layers/layer_04/triangle_projection/tail_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/layer_04/claim_count/selected_average_option_input",
            # "cds/steer/experience_rating/layers/layer_04/claim_count/override_triangle",
            # "cds/steer/experience_rating/layers/layer_04/claim_count/override_triangle_date",
            # "cds/steer/experience_rating/layers/layer_04/claim_count/override_triangle_date_used",
            # "cds/steer/experience_rating/layers/layer_04/claim_count/override_triangle_years",
            # "cds/steer/experience_rating/layers/layer_04/claim_count/benchmark_name/override",
            # "cds/steer/experience_rating/layers/layer_04/claim_count/experience_weight/override",
            # "cds/steer/experience_rating/layers/layer_04/claim_count/benchmark_use_occurrence",
            # "cds/steer/experience_rating/layers/layer_04/claim_count/tri_1_basis",
            # "cds/steer/experience_rating/layers/layer_04/claim_count/tri_2_manual_input",
            # "cds/steer/experience_rating/layers/layer_04/claim_count/tri_3a_exclusions",
            "cds/steer/experience_rating/layers/layer_04/claim_count/incremental_dev_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/layer_04/claim_count/tail_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/layer_04/layer_name",

            "cds/steer/experience_rating/layers/layer_05/burning_cost/weighting",
            "cds/steer/experience_rating/layers/layer_05/burning_cost/premium",
            "cds/steer/experience_rating/layers/layer_05/pattern_type",
            # "cds/steer/experience_rating/layers/layer_05/bc_comment",
            # "cds/steer/experience_rating/layers/layer_05/triangle_projection/selected_average_option_input",
            # "cds/steer/experience_rating/layers/layer_05/triangle_projection/override_triangle",
            # "cds/steer/experience_rating/layers/layer_05/triangle_projection/override_triangle_date",
            # "cds/steer/experience_rating/layers/layer_05/triangle_projection/override_triangle_date_used",
            # "cds/steer/experience_rating/layers/layer_05/triangle_projection/override_triangle_years",
            # "cds/steer/experience_rating/layers/layer_05/triangle_projection/benchmark_name/override",
            # "cds/steer/experience_rating/layers/layer_05/triangle_projection/experience_weight/override",
            # "cds/steer/experience_rating/layers/layer_05/triangle_projection/benchmark_use_occurrence",
            # "cds/steer/experience_rating/layers/layer_05/triangle_projection/tri_1_basis",
            # "cds/steer/experience_rating/layers/layer_05/triangle_projection/tri_2_manual_input",
            # "cds/steer/experience_rating/layers/layer_05/triangle_projection/tri_3a_exclusions",
            "cds/steer/experience_rating/layers/layer_05/triangle_projection/incremental_dev_factor/experience_selected_set_in_task",
            "cds/steer/experience_rating/layers/layer_05/triangle_projection/tail_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/layer_05/claim_count/selected_average_option_input",
            # "cds/steer/experience_rating/layers/layer_05/claim_count/override_triangle",
            # "cds/steer/experience_rating/layers/layer_05/claim_count/override_triangle_date",
            # "cds/steer/experience_rating/layers/layer_05/claim_count/override_triangle_date_used",
            # "cds/steer/experience_rating/layers/layer_05/claim_count/override_triangle_years",
            # "cds/steer/experience_rating/layers/layer_05/claim_count/benchmark_name/override",
            # "cds/steer/experience_rating/layers/layer_05/claim_count/experience_weight/override",
            # "cds/steer/experience_rating/layers/layer_05/claim_count/benchmark_use_occurrence",
            # "cds/steer/experience_rating/layers/layer_05/claim_count/tri_1_basis",
            # "cds/steer/experience_rating/layers/layer_05/claim_count/tri_2_manual_input",
            # "cds/steer/experience_rating/layers/layer_05/claim_count/tri_3a_exclusions",
            "cds/steer/experience_rating/layers/layer_05/claim_count/incremental_dev_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/layer_05/claim_count/tail_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/layer_05/layer_name",

            "cds/steer/experience_rating/layers/fgu/burning_cost/weighting",
            "cds/steer/experience_rating/layers/fgu/burning_cost/premium",
            "cds/steer/experience_rating/layers/fgu/pattern_type",
            # "cds/steer/experience_rating/layers/fgu/bc_comment",
            # "cds/steer/experience_rating/layers/fgu/triangle_projection/selected_average_option_input",
            # "cds/steer/experience_rating/layers/fgu/triangle_projection/override_triangle",
            # "cds/steer/experience_rating/layers/fgu/triangle_projection/override_triangle_date",
            # "cds/steer/experience_rating/layers/fgu/triangle_projection/override_triangle_date_used",
            # "cds/steer/experience_rating/layers/fgu/triangle_projection/override_triangle_years",
            # "cds/steer/experience_rating/layers/fgu/triangle_projection/benchmark_name/override",
            # "cds/steer/experience_rating/layers/fgu/triangle_projection/experience_weight/override",
            # "cds/steer/experience_rating/layers/fgu/triangle_projection/benchmark_use_occurrence",
            # "cds/steer/experience_rating/layers/fgu/triangle_projection/tri_1_basis",
            # "cds/steer/experience_rating/layers/fgu/triangle_projection/tri_2_manual_input",
            # "cds/steer/experience_rating/layers/fgu/triangle_projection/tri_3a_exclusions",
            "cds/steer/experience_rating/layers/fgu/triangle_projection/incremental_dev_factor/experience_selected_set_in_task",
            "cds/steer/experience_rating/layers/fgu/triangle_projection/tail_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/fgu/claim_count/selected_average_option_input",
            # "cds/steer/experience_rating/layers/fgu/claim_count/override_triangle",
            # "cds/steer/experience_rating/layers/fgu/claim_count/override_triangle_date",
            # "cds/steer/experience_rating/layers/fgu/claim_count/override_triangle_date_used",
            # "cds/steer/experience_rating/layers/fgu/claim_count/override_triangle_years",
            # "cds/steer/experience_rating/layers/fgu/claim_count/benchmark_name/override",
            # "cds/steer/experience_rating/layers/fgu/claim_count/experience_weight/override",
            # "cds/steer/experience_rating/layers/fgu/claim_count/benchmark_use_occurrence",
            # "cds/steer/experience_rating/layers/fgu/claim_count/tri_1_basis",
            # "cds/steer/experience_rating/layers/fgu/claim_count/tri_2_manual_input",
            # "cds/steer/experience_rating/layers/fgu/claim_count/tri_3a_exclusions",
            "cds/steer/experience_rating/layers/fgu/claim_count/incremental_dev_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/fgu/claim_count/tail_factor/experience_selected_set_in_task",
            # "cds/steer/experience_rating/layers/fgu/layer_name",

            "cds/steer/exposure_rating/risk_profile_bdx/exposure_lr",
            "cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/cob",
            "cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/curve",
            "cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/insured",
            "cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/limit",
            "cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/excess",
            "cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/net_premium",
            "cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/share",
            "cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/linkage",

            "cds/steer/exposure_rating/limit_average_severity/layers/layer_01/risk_profiles/current_year/ilf_user_input",
            "cds/steer/exposure_rating/limit_average_severity/layers/layer_02/risk_profiles/current_year/ilf_user_input",
            "cds/steer/exposure_rating/limit_average_severity/layers/layer_03/risk_profiles/current_year/ilf_user_input",
            "cds/steer/exposure_rating/limit_average_severity/layers/layer_04/risk_profiles/current_year/ilf_user_input",
            "cds/steer/exposure_rating/limit_average_severity/layers/layer_05/risk_profiles/current_year/ilf_user_input",

        

            "cds/pricing_selection/pareto_parameters/overwrite",
            "cds/pricing_selection/odf_parameters/overwrite",
            # "cds/other_method_rationale", # Non premium breaing
            # "cds/rate_change/has_fetch_not_run",
            # "cds/rate_change/has_rarc_not_run",
            # "cds/rate_change/instructions",
            # "model_state/landing_page_info",
            # "model_state/expiring_policy_option_id",
            # "model_state/is_steer_experience_rating",
            # "model_state/is_steer_exposure_rating_risk_profil_banded",
            # "model_state/is_steer_exposure_rating_risk_profil_bdx",
            # "model_state/is_steer_exposure_rating_limit_average_severity",
            # "model_state/show_las_chart_layer_01",
            # "model_state/show_las_chart_layer_02",
            # "model_state/show_las_chart_layer_03",
            # "model_state/show_las_chart_layer_04",
            # "model_state/show_las_chart_layer_05",
            # "bug_report/summary", # reporting
            # "bug_report/email_body",
            # "bug_report/file_helper_text",
            # "bug_report/files_shown",
            # "bug_report/screenshot_files/f1/file",
            # "bug_report/screenshot_files/f1/show_file",
            # "bug_report/screenshot_files/f1/show_text",
            # "bug_report/screenshot_files/f2/file",
            # "bug_report/screenshot_files/f2/show_file",
            # "bug_report/screenshot_files/f2/show_text",
            # "bug_report/screenshot_files/f3/file",
            # "bug_report/screenshot_files/f3/show_file",
            # "bug_report/screenshot_files/f3/show_text",
            # "bug_report/screenshot_files/f4/file",
            # "bug_report/screenshot_files/f4/show_file",
            # "bug_report/screenshot_files/f4/show_text",
            # "bug_report/screenshot_files/f5/file",
            # "bug_report/screenshot_files/f5/show_file",
            # "bug_report/screenshot_files/f5/show_text",
            # "bug_report/show_email",
            # "model_profiling/selected_segment",
            # "model_profiling/timer_threshold",
            
        ],
        "risk_characteristics": [
            # only coverage
            "cds/steer/experience_rating/other_fields/coverage_basis/value",

        ],
        "deductible": [
            "cds/layers/excess",
            "cds/layers/deductible"
        ],
        "limit": [
            "cds/layers/limit"
        ],
        "terms_conditions": [

            "cds/risk_information/include_aad",
            "cds/risk_information/include_loss_corridor",
            "cds/risk_information/include_swing_rates",

            "cds/layers/swing_rates/use_swing_brokerage",

            "cds/layers/expected_aad",
            "cds/layers/loss_corridor_loss_cost",
            "cds/layers/expected_reinstatement_factor",
            "cds/layers/expected_ncb_pct",
            "cds/layers/profit_commission",
            "cds/layers/swing_premium",


        ],
        "other": [
            "cds/layers/brokerage"
        ]
    } 

    RATE_CHANGE_BUCKETS_HEALTHCARE_CAT = {
        "model": [], # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": [
            "hx_core/inception_date",
            "hx_core/expiry_date",
            "cds/layers/include_layer",

            "cds/layers/epi_100",
            "cds/layers/rate",
            "cds/layers/ceding_commission",

            "cds/layers/bkg_gross_or_net",

            "cds/layers/pricing_selection/risk_profile_bdx/weighting",
            "cds/layers/pricing_selection/limit_average_severity/weighting",
            "cds/layers/pricing_selection/burning_cost/weighting",
            "cds/layers/pricing_selection/clash/weighting",
            "cds/layers/pricing_selection/healthcare_cat/weighting",
            "cds/layers/pricing_selection/other_method/pure_rate",
            "cds/layers/pricing_selection/other_method/weighting",

            "cds/currencies/source_currency",

            "cds/technical_price_assumptions/select_class",

            "cds/healthcare_cat/trial_history/trial/taken_to_trial",
            "cds/healthcare_cat/trial_history/trial/wins",
            "cds/healthcare_cat/trial_history/trial/losses",
            "cds/healthcare_cat/trial_history/trial/mistrials",

            "cds/healthcare_cat/trial_history/uw_view/from_year",
            "cds/healthcare_cat/trial_history/uw_view/to_year",

            "cds/healthcare_cat/exposure_territory/type_of_business",
            "cds/healthcare_cat/exposure_territory/specialty",
            

            "cds/healthcare_cat/exposure_territory/overall_exposure_per_year/physicians",
            "cds/healthcare_cat/exposure_territory/overall_exposure_per_year/professional_associations",
            "cds/healthcare_cat/exposure_territory/overall_exposure_per_year/ambulatory_surgery_centres",
            "cds/healthcare_cat/exposure_territory/overall_exposure_per_year/hospitals",
            "cds/healthcare_cat/exposure_territory/overall_exposure_per_year/ltc_facilities",
            "cds/healthcare_cat/exposure_territory/overall_exposure_per_year/other_facilities",
            "cds/healthcare_cat/exposure_territory/overall_exposure_per_year/dentists",
            "cds/healthcare_cat/exposure_territory/overall_exposure_per_year/others",

            "cds/healthcare_cat/exposure_territory/choose_split_by", 

            "cds/healthcare_cat/exposure_territory/exposure_spit_by_state/premium_written",
            "cds/healthcare_cat/exposure_territory/exposure_spit_by_state/total_pif_current_year",

            "cds/healthcare_cat/pricing/high_low_adjustment/select",
            "cds/healthcare_cat/pricing/social_inflation_impact/select",

            "cds/pricing_selection/pareto_parameters/overwrite",
            "cds/pricing_selection/odf_parameters/overwrite",            
        ],
        "risk_characteristics": [],
        "deductible": [
            "cds/layers/excess",
            "cds/layers/deductible"
        ],
        "limit": [
            "cds/layers/limit"
        ],
        "terms_conditions": [
            "cds/risk_information/include_aad",
            "cds/risk_information/include_loss_corridor",
            "cds/risk_information/include_swing_rates",

            "cds/layers/swing_rates/use_swing_brokerage",

            "cds/layers/expected_aad",
            "cds/layers/loss_corridor_loss_cost",
            "cds/layers/expected_reinstatement_factor",
            "cds/layers/expected_ncb_pct",
            "cds/layers/profit_commission",
            "cds/layers/swing_premium",            
        ],
        "other": [
            "cds/layers/brokerage"
        ]
    }

    RATE_CHANGE_BUCKETS_CLASH = {
        "model": [], # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": [
            "hx_core/inception_date",
            "hx_core/expiry_date",
            "cds/layers/include_layer",

            "cds/layers/epi_100",
            "cds/layers/rate",
            "cds/layers/ceding_commission",

            "cds/layers/bkg_gross_or_net",

            "cds/layers/pricing_selection/risk_profile_bdx/weighting",
            "cds/layers/pricing_selection/limit_average_severity/weighting",
            "cds/layers/pricing_selection/burning_cost/weighting",
            "cds/layers/pricing_selection/clash/weighting",
            "cds/layers/pricing_selection/healthcare_cat/weighting",
            "cds/layers/pricing_selection/other_method/pure_rate",
            "cds/layers/pricing_selection/other_method/weighting",

            "cds/currencies/source_currency",

            "cds/technical_price_assumptions/select_class",

            "cds/pricing_selection/pareto_parameters/overwrite",
            "cds/pricing_selection/odf_parameters/overwrite",              
        ],
        "risk_characteristics": [],
        "deductible": [
            "cds/layers/excess",
            "cds/layers/deductible"
        ],
        "limit": [
            "cds/layers/limit"
        ],
        "terms_conditions": [
            "cds/risk_information/include_aad",
            "cds/risk_information/include_loss_corridor",
            "cds/risk_information/include_swing_rates",

            "cds/layers/swing_rates/use_swing_brokerage",

            "cds/layers/expected_aad",
            "cds/layers/loss_corridor_loss_cost",
            "cds/layers/expected_reinstatement_factor",
            "cds/layers/expected_ncb_pct",
            "cds/layers/profit_commission",
            "cds/layers/swing_premium",              
        ],
        "other": [
            "cds/layers/brokerage"
        ]
    }



# NOTE: Specify the input paths and the associated currencies that influence the premium. DO NOT include any output paths in this list.
# These inputs are usually at the lowest level of premium calculation.
if not RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE == False:
    EXP_INPUTS_IN_CCY_STEER = {
        "layers":[
            # (input_node_path,input_currency_node_path)
            ("cds/layers/limit","cds/layers/currency"),
            ("cds/layers/excess","cds/layers/currency"),
            ("cds/layers/deductible","cds/layers/currency"),
            # ("cds/layers/quoted_premium_100","cds/layers/currency"),

            # ("cds/layers/advanced_features_input/aad","cds/layers/currency"),
            # ("cds/layers/epi_100","cds/layers/currency"),
            # ("cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure","cds/layers/currency"),
            # ("cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure_adjusted_layer_01","cds/layers/currency"),
            # ("cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure_adjusted_layer_02","cds/layers/currency"),
            # ("cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure_adjusted_layer_03","cds/layers/currency"),
            # ("cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure_adjusted_layer_04","cds/layers/currency"),
            # ("cds/steer/experience_rating/on_levelling/exposure_assumptions/exposure_adjusted_layer_05","cds/layers/currency"),

            # ("cds/steer/experience_rating/layers/layer_01/burning_cost/weighting","cds/layers/currency"),
            # ("cds/steer/experience_rating/layers/layer_01/burning_cost/premium","cds/layers/currency"),
            # ("cds/steer/experience_rating/layers/layer_02/burning_cost/weighting","cds/layers/currency"),
            # ("cds/steer/experience_rating/layers/layer_02/burning_cost/premium","cds/layers/currency"),
            # ("cds/steer/experience_rating/layers/layer_03/burning_cost/weighting","cds/layers/currency"),
            # ("cds/steer/experience_rating/layers/layer_03/burning_cost/premium","cds/layers/currency"),
            # ("cds/steer/experience_rating/layers/layer_04/burning_cost/weighting","cds/layers/currency"),
            # ("cds/steer/experience_rating/layers/layer_04/burning_cost/premium","cds/layers/currency"),
            # ("cds/steer/experience_rating/layers/layer_05/burning_cost/weighting","cds/layers/currency"),
            # ("cds/steer/experience_rating/layers/layer_05/burning_cost/premium","cds/layers/currency"),

            # ("cds/steer/experience_rating/layers/fgu/burning_cost/weighting","cds/layers/currency"),
            # ("cds/steer/experience_rating/layers/fgu/burning_cost/premium","cds/layers/currency"),

            # ("cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/limit","cds/layers/currency"),
            # ("cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/excess","cds/layers/currency"),
            # ("cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/net_premium","cds/layers/currency"),

        ]
    }
    EXP_INPUTS_IN_CCY_HEALTHCARE_CAT = {
        "layers":[
            # (input_node_path,input_currency_node_path)
            ("cds/layers/limit","cds/layers/currency"),
            ("cds/layers/excess","cds/layers/currency"),
            ("cds/layers/deductible","cds/layers/currency"),
            # ("cds/layers/quoted_premium_100","cds/layers/currency"),

            # ("cds/layers/advanced_features_input/aad","cds/layers/currency"),
            # ("cds/layers/epi_100","cds/layers/currency"),


        ]
    }
    EXP_INPUTS_IN_CCY_CLASH = {
        "layers":[
            # (input_node_path,input_currency_node_path)
            ("cds/layers/limit","cds/layers/currency"),
            ("cds/layers/excess","cds/layers/currency"),
            ("cds/layers/deductible","cds/layers/currency"),
            # ("cds/layers/quoted_premium_100","cds/layers/currency"),

            # ("cds/layers/advanced_features_input/aad","cds/layers/currency"),
            # ("cds/layers/epi_100","cds/layers/currency"),

        ]
    }


