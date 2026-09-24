# If changing the max_layers below, you must also update in vw_constants to the same number
max_layers = 6

benchmark_lr = 0.7

YEARS_TO_CONSIDER_IN_RISK_CODE_COMPOSITION = 9
YEARS_TO_CONSIDER_IN_ASSUMED_DEDUCTIONS = YEARS_TO_CONSIDER_IN_RISK_CODE_COMPOSITION
YEARS_TO_CONSIDER_IN_PORTFOLIO_PROFILE = 26
YEARS_TO_CONSIDER_IN_Inflation = 26
YEARS_TO_CONSIDER_IN_RATE_CHANGE = 16
NUM_CURVES_IN_CAT = 10
YEARS_TO_CONSIDER_IN_OWN_EXPERIENCE = 16
DEFAULT_NUM_LOB = 5
MAX_NUM_LOB = 50
DEFAULT_NUM_RISK_CODES = 10
MAX_NUM_RISK_CODES = 50
YEARS_TO_CONSIDER_IN_LLOYDS_PROJECTIONS = 23
NUMBER_OF_INFLATION_YEARS = 6

NUMBER_SECTION_REFERENCES = 20

DECAY_RATIO = 0.9
THRESHOLD_FOR_BF = 0.4 
THRESHOLD_FOR_CL = 0.75
BENCHMARK_LR = 0.7



LLOYDS_YEAR_ASSUME_FULLY_DEV = 2004

LLOYDS_DATA_CUTOFF_DATE     = '2026-01-01'
BEAZLEY_DATA_CUTOFF_DATE    = '2026-06-30'

cols_to_value_dict = {
        'own_performance': 1,
        'lloyds_performance': 0.5,
        'beazley_performance': 1,
        'business_plan': 1,
        'case_pricing': 1,
        'pricing_2623_623': 1
    }

common_fields = ['mga_fee', 'facility_brokerage',
                     'leaders_fee', 'service_fee', 'other'] 


policy_data_fields = [
        "umr",
        "policy_reference",
        "account_name",
        "facility_lob",
        "inception_date",
        "expiry_date",
        "yoa",
        "month_processed",
        "risk_code",
        "currency",
        "gross_premium",
        "net_premium",
        "paid_attritional",
        "paid_large",
        "paid_cat",
        "paid_total",
        "incurred_attritional",
        "incurred_large",
        "incurred_cat",
        "incurred_total",
        "sum_insured_tiv",
        "limit_attachment_currency",
        "limit",
        "attachment",
        "primary",
        "order_per",
        "risk_location",
        "industry_type",
        "region",
        "occupancy_property",
        "habitational",
        "slip_leader",
        "naic_sic",
    ]

policy_data_used_inputs = [
        "account_name",
        "facility_lob",
        "yoa",
        "risk_code",
        "currency",
        "gross_premium",
        "net_premium",
        "paid_attritional",
        "paid_large",
        "paid_cat",
        "paid_total",
        "incurred_attritional",
        "incurred_large",
        "incurred_cat",
        "incurred_total"    ]

claim_data_fields = [
    "umr",
    "policy_reference",
    "claim_reference",
    "account_name",
    "facility_lob",
    "loss_date",
    "claim_made_date",
    "closed_date",
    "month_processed",
    "yoa",
    "claim_status",
    "risk_code",
    "currency",
    "claim_type",
    "cat_code",
    "paid",
    "outstanding",
    "incurred",
    "selected_lob"
]


claim_data_used_inputs = [
    "facility_lob",
    "yoa",
    "claim_status",
    "risk_code",
    "currency",
    "claim_type",
    "paid",
    "outstanding",
    "incurred",
    "selected_lob"
]



policy_fields_to_convert = [
        "gross_premium", "net_premium", "paid_attritional", "paid_large",
        "paid_cat", "paid_total", "incurred_attritional", "incurred_large",
        "incurred_cat", "incurred_total"
    ]    
lloyds_tables = [
        'lloyds_incurred_development',
        'lloyds_paid_development',
        'lloyds_premium_development',
        'rate_change_no_override'
    ]  
risk_code_library_multiplying_factor = 1000      


NODES_DRIVEN_BY_SELECTED_LOB = [
    "anti_selection.applied_charge.table",
    "assumed_deductions.data_driven_deductions.deductions.table",
    "assumed_deductions.deductions_manually_entered.table",
    "bp_projections.bp_summary_by_lob",
    "pc.pc_structure.table",
    "pc.pc_structure.table_sliding_scale",
    "pc.pc_calculations.details",
    "pc.cm_ovd",
    # "pc.cm_ovd[0].cm_col",
    # "prem_limit_profile.table",
    "projections_own_experience.summary_table",
    # "projections_own_experience.detail_table",    # * constants.YEARS_TO_CONSIDER_IN_OWN_EXPERIENCE
    "rate_change",
    "rating_summary.model_gn_ulr.projected_gn_ulr.table",
    "rating_summary.model_gn_ulr.model_weights.table",
    "rating_summary.cat_loadings.cat_allocation",
    "rating_summary.additional_loadings.additional_pricing_loads",
    "rating_summary.pricing_adequacy_metrics.pricing_adequacy_final_pricing.table",
    "uncertainty.applied_charge.table",
    "rating_summary.section_ref_allocation.table_pcts"
    # "rating_summary.section_ref_allocation.total_pcts_by_lob" 
]

NODES_DRIVEN_BY_FACILITY_LOB = [
    "prem_limit_profile.table",
]

NODES_DRIVEN_BY_FACILITY_LOB = [
    "prem_limit_profile.table",
]

NODES_DRIVEN_BY_RISK_CODES = [
    "bp_projections.bp_details",                  # by DEFAULT_NUM_RISK_CODES
    "inflation.details",                          # by DEFAULT_NUM_RISK_CODES
    "projections_lloyds.summary_table",
    "projections_beazley.summary_table",
]