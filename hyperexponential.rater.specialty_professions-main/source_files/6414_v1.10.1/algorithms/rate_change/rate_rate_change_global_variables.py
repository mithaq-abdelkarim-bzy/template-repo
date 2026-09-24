# v0.5.0
import hx
import pandas as pd
import numpy as np
import math as math
import json
from algorithms.rate_utilities import title_rc, ratio, usd, to_ccy, look_up
from operator import itemgetter

from algorithms.rate_constants import max_layers, model_change_list, exposure_change_list, risk_characteristics_change_list, deductible_change_list, limit_change_list, terms_and_conditions_change_list, brokerage_change_list
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
    RATE_CHANGE_BUCKETS = {
        "model": model_change_list() + [], # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": exposure_change_list() + [],
        "risk_characteristics": risk_characteristics_change_list() + [],
        "deductible": deductible_change_list() + [],
        "limit": limit_change_list() + [],
        "terms_conditions": terms_and_conditions_change_list() + [],
        "other": brokerage_change_list() + []
    } 
elif not RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE:
    RATE_CHANGE_BUCKETS = {
        "layers" : {
            "model": [], # NOTE: leave this empty - starts from expiry data priced with current model
            "exposure": [
                
            ],
            "risk_characteristics": [],
            "deductible": [
                "cds/exposure/granular/layers/excess",
                "cds/exposure/granular/layers/deductible"
            ],
            "limit": [
                "cds/exposure/granular/layers/limit"
            ],
            "terms_conditions": [],
            "other": [
                "cds/layers/brokerage" # The brokerage is entered at a layer-level and applicable for the whole insured asset list
            ]
        }
    }
elif RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE == False:
    RATE_CHANGE_BUCKETS = {
        f"{COVERAGES_LIST[0]}" : {
            "model": [], # NOTE: leave this empty - starts from expiry data priced with current model
            "exposure": [],
            "risk_characteristics": [],
            "deductible": [
                "cds/layers/coverages/example_coverage_1/excess",
                "cds/layers/coverages/example_coverage_1/deductible"
            ],
            "limit": [
                "cds/layers/coverages/example_coverage_1/limit"
            ],
            "terms_conditions": [],
            "other": [
                "cds/layers/coverages/example_coverage_1/brokerage"
            ]
        },
        f"{COVERAGES_LIST[1]}" : {
            "model": [], # NOTE: leave this empty - starts from expiry data priced with current model
            "exposure": [],
            "risk_characteristics": [],
            "deductible": [
                "cds/layers/coverages/example_coverage_2/excess",
                "cds/layers/coverages/example_coverage_2/deductible"
            ],
            "limit": [
                "cds/layers/coverages/example_coverage_2/limit"
            ],
            "terms_conditions": [],
            "other": [
                "cds/layers/coverages/example_coverage_2/brokerage"
            ]
        }
    }
elif RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE == True:
    RATE_CHANGE_BUCKETS = {
        f"{COVERAGES_LIST[0]}" : {
            "model": [], # NOTE: leave this empty - starts from expiry data priced with current model
            "exposure": [
                
            ],
            "risk_characteristics": [],
            "deductible": [
                "cds/exposure/granular/example_coverage_1/excess",
                "cds/exposure/granular/example_coverage_1/deductible"
            ],
            "limit": [
                "cds/exposure/granular/example_coverage_1/limit"
            ],
            "terms_conditions": [],
            "other": [
                "cds/layers/coverages/example_coverage_1/brokerage" # The brokerage is entered at a coverage-level and applicable for the whole insured asset list
            ]
        },
        f"{COVERAGES_LIST[1]}" : {
            "model": [], # NOTE: leave this empty - starts from expiry data priced with current model
            "exposure": [],
            "risk_characteristics": [],
            "deductible": [
                "cds/exposure/granular/example_coverage_2/excess",
                "cds/exposure/granular/example_coverage_2/deductible"
            ],
            "limit": [
                "cds/exposure/granular/example_coverage_2/limit"
            ],
            "terms_conditions": [],
            "other": [
                "cds/layers/coverages/example_coverage_2/brokerage" # The brokerage is entered at a coverage-level and applicable for the whole insured asset list
            ]
        }
    }      

# NOTE: Specify the input paths and the associated currencies that influence the premium. DO NOT include any output paths in this list.
# These inputs are usually at the lowest level of premium calculation.
if not RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE == False:
    EXP_INPUTS_IN_CCY = {
        "layers":[
            # (input_node_path,input_currency_node_path)
            ("cds/options/limit","cds/ccy"),
            # ("cds/layers/excess","cds/ccy"),
            ("cds/options/deductible","cds/ccy"),
            ("cds/layers/quoted_premium_100","cds/ccy"),
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

