# v0.5.0
import hx
import pandas as pd
import numpy as np
import math as math
import json
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
RATE_CHANGE_BUCKETS = {
    "model": [], # NOTE: leave this empty - starts from expiry data priced with current model
    "exposure": [
          "cds/exposure/granular/event_cancel/events/event_name"
        , "cds/exposure/granular/event_cancel/events/country"
        , "cds/exposure/granular/event_cancel/events/state"
        , "cds/exposure/granular/event_cancel/events/date_start"
        , "cds/exposure/granular/event_cancel/events/date_end"
        , "cds/exposure/granular/event_cancel/events/tiv"
        , "cds/exposure/granular/event_cancel/events/venue"
        , "cds/exposure/granular/event_cancel/events/ihs_terrorism"
        , "cds/exposure/granular/event_cancel/events/ihs_riots_and_civil_commotion"
        , "cds/exposure/granular/event_cancel/events/ihs_strike"
        , "cds/exposure/granular/event_cancel/events/ihs_war"
        , "cds/standard_fields/rating_methodology"
        , "cds/layers/bpi_case_priced"
        , "cds/currencies/source_currency"
        , "hx_core/inception_date"
        , "hx_core/expiry_date"

    ],

    "risk_characteristics": [ 
          "cds/exposure/granular/event_cancel/event_type"
        , "cds/exposure/granular/event_cancel/exposure_curve"
        , "cds/exposure/granular/event_cancel/experience"
        , "cds/exposure/granular/event_cancel/experience_ratio"
        , "cds/exposure/granular/event_cancel/ncb"
        , "cds/exposure/granular/event_cancel/ncb_offered"
        , "cds/exposure/granular/event_cancel/base_coverages/all_risks/uw_adj_sel"
        , "cds/exposure/granular/event_cancel/base_coverages/adverse_weather/uw_adj_sel"
        , "cds/exposure/granular/event_cancel/base_coverages/earthquake/uw_adj_sel"
        , "cds/exposure/granular/event_cancel/base_coverages/windstorm/uw_adj_sel"
        , "cds/exposure/granular/event_cancel/base_coverages/wildfire/uw_adj_sel"
        , "cds/exposure/granular/event_cancel/base_coverages/terrorism/uw_adj_sel"
        , "cds/exposure/granular/event_cancel/base_coverages/cyber/uw_adj_sel"
        , "cds/exposure/granular/event_cancel/base_coverages/national_mourning/uw_adj_sel"
        , "cds/exposure/granular/event_cancel/base_coverages/riots_and_civil_commotion/uw_adj_sel"
        , "cds/exposure/granular/event_cancel/base_coverages/strike/uw_adj_sel"
        , "cds/exposure/granular/event_cancel/base_coverages/war/uw_adj_sel"
        , "cds/exposure/granular/event_cancel/base_coverages/catastrophic_non_app/delegates"
        , "cds/exposure/granular/event_cancel/base_coverages/catastrophic_non_app/uw_adj_sel"
        , "cds/exposure/granular/event_cancel/terrorism_terms/city_load"
        , "cds/exposure/granular/event_cancel/terrorism_terms/event_profile"
        , "cds/exposure/granular/event_cancel/terrorism_terms/time_distance"
        , "cds/exposure/granular/event_cancel/national_mourning/over_75/include"
        , "cds/exposure/granular/event_cancel/national_mourning/over_75/name"
        , "cds/exposure/granular/event_cancel/national_mourning/over_75/country"
        , "cds/exposure/granular/event_cancel/national_mourning/over_75/gender"
        , "cds/exposure/granular/event_cancel/national_mourning/over_75/date_of_birth"
        , "cds/exposure/granular/event_cancel/national_mourning/over_75/mod_affluence"
        , "cds/exposure/granular/event_cancel/national_mourning/over_75/mod_health"
        , "cds/exposure/granular/event_cancel/national_mourning/under_75/include"
        , "cds/exposure/granular/event_cancel/national_mourning/under_75/mod_affluence"
        , "cds/exposure/granular/event_cancel/national_mourning/under_75/mod_health"
        , "cds/exposure/granular/event_cancel/national_mourning/bespoke_1/include"
        , "cds/exposure/granular/event_cancel/national_mourning/bespoke_1/name"
        , "cds/exposure/granular/event_cancel/national_mourning/bespoke_1/country"
        , "cds/exposure/granular/event_cancel/national_mourning/bespoke_1/gender"
        , "cds/exposure/granular/event_cancel/national_mourning/bespoke_1/date_of_birth"
        , "cds/exposure/granular/event_cancel/national_mourning/bespoke_1/mod_affluence"
        , "cds/exposure/granular/event_cancel/national_mourning/bespoke_1/mod_health"
        , "cds/exposure/granular/event_cancel/national_mourning/bespoke_2/include"
        , "cds/exposure/granular/event_cancel/national_mourning/bespoke_2/name"
        , "cds/exposure/granular/event_cancel/national_mourning/bespoke_2/country"
        , "cds/exposure/granular/event_cancel/national_mourning/bespoke_2/gender"
        , "cds/exposure/granular/event_cancel/national_mourning/bespoke_2/date_of_birth"
        , "cds/exposure/granular/event_cancel/national_mourning/bespoke_2/mod_affluence"
        , "cds/exposure/granular/event_cancel/national_mourning/bespoke_2/mod_health"
        , "cds/exposure/granular/event_cancel/national_mourning/cover_level"
        , "cds/exposure/granular/event_cancel/national_mourning/mourning_period"        
        , "model_state/use_nm_app_old_model"
        , "model_state/use_determ_agg_calc"
    ],

    "deductible": [
        #   "cds/layers/aggregate_excess"
          "cds/layers/coverages/ec_total/excess"
        , "cds/layers/coverages/ec_total/deductible"
        , "cds/layers/coverages/ec_total/aggregate_excess"
        , "cds/layers/coverages/ec_total/aggregate_deductible"
        , "cds/layers/coverages/ec_total/excess_use"
        # , "cds/layers/coverages/na_total/deductible"
        # , "cds/layers/coverages/na_total/aggregate_deductible"
    ],

    "limit": [
          "cds/exposure/granular/event_cancel/base_coverages/adverse_weather/sublimit"
        , "cds/exposure/granular/event_cancel/base_coverages/earthquake/sublimit"
        , "cds/exposure/granular/event_cancel/base_coverages/windstorm/sublimit"
        , "cds/exposure/granular/event_cancel/base_coverages/wildfire/sublimit"
        , "cds/exposure/granular/event_cancel/base_coverages/terrorism/sublimit"
        , "cds/exposure/granular/event_cancel/base_coverages/cyber/sublimit"
        , "cds/exposure/granular/event_cancel/base_coverages/national_mourning/sublimit"
        , "cds/exposure/granular/event_cancel/base_coverages/riots_and_civil_commotion/sublimit"
        , "cds/exposure/granular/event_cancel/base_coverages/strike/sublimit"
        , "cds/exposure/granular/event_cancel/base_coverages/war/sublimit"
        , "cds/exposure/granular/event_cancel/base_coverages/catastrophic_non_app/sublimit"
        , "cds/layers/coverages/ec_total/limit"
        , "cds/layers/coverages/ec_total/aggregate_limit"
        # , "cds/layers/coverages/na_total/limit"
        # , "cds/layers/coverages/na_total/aggregate_limit"
    ],

    "terms_conditions": [
          "cds/exposure/granular/event_cancel/base_coverages/adverse_weather/covered"
        , "cds/exposure/granular/event_cancel/base_coverages/earthquake/covered"
        , "cds/exposure/granular/event_cancel/base_coverages/windstorm/covered"
        , "cds/exposure/granular/event_cancel/base_coverages/wildfire/covered"
        , "cds/exposure/granular/event_cancel/base_coverages/terrorism/covered"
        , "cds/exposure/granular/event_cancel/base_coverages/cyber/covered"
        , "cds/exposure/granular/event_cancel/base_coverages/cyber/trigger"
        , "cds/exposure/granular/event_cancel/base_coverages/national_mourning/covered"
        , "cds/exposure/granular/event_cancel/base_coverages/national_mourning/trigger"
        , "cds/exposure/granular/event_cancel/base_coverages/riots_and_civil_commotion/covered"
        , "cds/exposure/granular/event_cancel/base_coverages/strike/covered"
        , "cds/exposure/granular/event_cancel/base_coverages/war/covered"
        , "cds/exposure/granular/event_cancel/base_coverages/catastrophic_non_app/covered"
        , "cds/exposure/granular/event_cancel/base_coverages/catastrophic_non_app/trigger"
        , "cds/risk_info/product_bool"
    ],

    "other": [
        "cds/layers/brokerage"
    ]
} 


# NOTE: Specify the input paths and the associated currencies that influence the premium. DO NOT include any output paths in this list.
# These inputs are usually at the lowest level of premium calculation.
EXP_INPUTS_IN_CCY = {
    "layers":[
        # (input_node_path,input_currency_node_path)
        ("cds/exposure/granular/event_cancel/base_coverages/adverse_weather/sublimit",      "cds/layers/currency"),
        ("cds/exposure/granular/event_cancel/base_coverages/earthquake/sublimit",           "cds/layers/currency"),
        ("cds/exposure/granular/event_cancel/base_coverages/windstorm/sublimit",            "cds/layers/currency"),
        ("cds/exposure/granular/event_cancel/base_coverages/wildfire/sublimit",             "cds/layers/currency"),
        ("cds/exposure/granular/event_cancel/base_coverages/terrorism/sublimit",            "cds/layers/currency"),
        ("cds/exposure/granular/event_cancel/base_coverages/cyber/sublimit",                "cds/layers/currency"),
        ("cds/exposure/granular/event_cancel/base_coverages/national_mourning/sublimit",    "cds/layers/currency"),
        ("cds/exposure/granular/event_cancel/base_coverages/riots_and_civil_commotion/sublimit", "cds/layers/currency"),
        ("cds/exposure/granular/event_cancel/base_coverages/strike/sublimit",               "cds/layers/currency"),
        ("cds/exposure/granular/event_cancel/base_coverages/war/sublimit",                  "cds/layers/currency"),
        ("cds/exposure/granular/event_cancel/base_coverages/catastrophic_non_app/sublimit", "cds/layers/currency"),
        ("cds/exposure/granular/event_cancel/events/tiv",                                   "cds/layers/currency"),
        ("cds/layers/coverages/ec_total/limit",                                             "cds/layers/currency"),
        ("cds/layers/coverages/ec_total/excess",                                            "cds/layers/currency"),
        ("cds/layers/coverages/ec_total/deductible",                                        "cds/layers/currency"),
        ("cds/layers/coverages/ec_total/aggregate_limit",                                   "cds/layers/currency"),
        ("cds/layers/coverages/ec_total/aggregate_excess",                                  "cds/layers/currency"),
        ("cds/layers/coverages/ec_total/aggregate_deductible",                              "cds/layers/currency"),
        ("cds/layers/coverages/na_total/limit",                                             "cds/layers/currency"),
        ("cds/layers/coverages/na_total/aggregate_limit",                                   "cds/layers/currency"),
    ]
}


# NOTE: Specify the input paths and the associated currencies that influence the premium. DO NOT include any output paths in this list.
# These inputs are usually at the lowest level of premium calculation.
if not RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE == False:
    EXP_INPUTS_IN_CCY = {
        "layers":[
            # (input_node_path,input_currency_node_path)
            ("cds/layers/limit","cds/layers/currency"),
            ("cds/layers/excess","cds/layers/currency"),
            ("cds/layers/deductible","cds/layers/currency"),
            ("cds/layers/quoted_premium_100","cds/layers/currency"),
        ]
    }
elif not RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE == True:
    EXP_INPUTS_IN_CCY = {
        "layers" : [
            # (input_node_path,input_currency_node_path)
            ("cds/exposure/granular/layers/limit","cds/layers/coverages/layers/currency"),
            ("cds/exposure/granular/layers/excess","cds/exposure/granular/layers/currency"),
            ("cds/exposure/granular/layers/deductible","cds/exposure/granular/layers/currency"),
            ("cds/exposure/granular/layers/quoted_premium_100","cds/exposure/granular/layers/currency"),
        ],
    }
elif RARC_COVERAGE_USE == True and RARC_INSURED_ASSET_USE == False:
    EXP_INPUTS_IN_CCY = {
        f"{COVERAGES_LIST[0]}" : [
            # (input_node_path,input_currency_node_path)
            ("cds/layers/coverages/example_coverage_1/limit","cds/layers/coverages/example_coverage_1/currency"),
            ("cds/layers/coverages/example_coverage_1/excess","cds/layers/coverages/example_coverage_1/currency"),
            ("cds/layers/coverages/example_coverage_1/deductible","cds/layers/coverages/example_coverage_1/currency"),
            ("cds/layers/coverages/example_coverage_1/quoted_premium_100","cds/layers/coverages/example_coverage_1/currency"),
        ],
        f"{COVERAGES_LIST[1]}" : [
            # (input_node_path,input_currency_node_path)
            ("cds/layers/coverages/example_coverage_2/limit","cds/layers/coverages/example_coverage_2/currency"),
            ("cds/layers/coverages/example_coverage_2/excess","cds/layers/coverages/example_coverage_2/currency"),
            ("cds/layers/coverages/example_coverage_2/deductible","cds/layers/coverages/example_coverage_2/currency"),
            ("cds/layers/coverages/example_coverage_2/quoted_premium_100","cds/layers/coverages/example_coverage_2/currency"),
        ]       
    }
elif RARC_COVERAGE_USE == True and RARC_INSURED_ASSET_USE == True:
    EXP_INPUTS_IN_CCY = {
        f"{COVERAGES_LIST[0]}" : [
            # (input_node_path,input_currency_node_path)
            ("cds/exposure/granular/example_coverage_1/limit","cds/layers/coverages/example_coverage_1/currency"),
            ("cds/exposure/granular/example_coverage_1/excess","cds/exposure/granular/example_coverage_1/currency"),
            ("cds/exposure/granular/example_coverage_1/deductible","cds/exposure/granular/example_coverage_1/currency"),
            ("cds/exposure/granular/example_coverage_1/quoted_premium_100","cds/exposure/granular/example_coverage_1/currency"),
        ],
        f"{COVERAGES_LIST[1]}" : [
            # (input_node_path,input_currency_node_path)
            ("cds/exposure/granular/example_coverage_2/limit","cds/exposure/granular/example_coverage_2/currency"),
            ("cds/exposure/granular/example_coverage_2/excess","cds/exposure/granular/example_coverage_2/currency"),
            ("cds/exposure/granular/example_coverage_2/deductible","cds/exposure/granular/example_coverage_2/currency"),
            ("cds/exposure/granular/example_coverage_2/quoted_premium_100","cds/exposure/granular/example_coverage_2/currency"),
        ]       
    }

