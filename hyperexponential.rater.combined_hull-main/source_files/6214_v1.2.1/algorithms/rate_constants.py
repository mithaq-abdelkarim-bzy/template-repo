# If changing the max_layers below, you must also update in vw_constants to the same number
max_layers = 1

benchmark_lr = 0.7

modelling_prefix = "modelling_"
model_types = ["behavioural", "static"]
claim_types = ["frequency", "severity"]
calculation_or_factor_relatives = ["calculation", "factor_relatives"]
claim_type_fields = ["vessel_type", "dwt"]
factor_relatives_fields = claim_type_fields + ["year_built", "flag"]
calculation_fields = [
    "coverage",
    "coverage_factor",
    "deductible",
    "order",
]

# MARINE HULL CONSTS
coverage_cl_290_factor = 4
coverage_cl_290 = "CL 290"
large_base_rate = 402.168945323276
iv_base_rate = 0.00125
iv_plan_ulr = 0.5
iv_plan_commission = 0.2


# LOH CONSTS
loh_base_rate_brokerage = 0.2

# Shipbuilders CONSTS
ship_building_war_factor = 0.00005

ship_building_experience_rating_years = 10

incomplete_column = "\U0000274c"  # Red X
complete_column = "\U00002705"  # Green Check

bp_class = "Hull"
excel_password = "giraffe"
