import hx_data_schema as hx
import algorithms.rate_constants as c
from algorithms.data_schema.sch_utilities import thousands_format, percent_format, integer_format, hx_node, get_existing_attributes

### --- DEFINING THE NODES HERE SO THAT THEIR PROPERTIES ARE DYNAMICALLY ACCESSIBLE BY THE RATING ALGORITHM --- ###

### --- AIRLINES FIELDS --- ###
common_tasks = [
    "fetch_by_operator_task", 
    {"task": "fetch_by_registration_task", "reset": False}, 
    {"task": "get_selected_regs_task", "reset": False}, 
    "clear_table_task", 
    {"task": "fill_with_defaults_task", "reset": False},
    {"task": "start_renewal_task", "reset": False},
    ]

airlines_validation_cols = [
    "no_of_aircraft",
    "attachment_date",
    "expiry_date",
    "time_in_service",
    "build_year",
    "total_seats",
    "previous12_months_hours",
    "operating_mtow_lb",
    "value",
    "hull_limit",
    "hull_excess",
    "liability_limit",
    "liability_excess",
    "pll_award"
]

airlines_inputs = {
    "include": hx.Bool(mode="input", default=True, async_input=["rarc_task"], async_output=[{"task": "fill_with_defaults_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], view={"label": "Include\nExposure?"}),
    "no_of_aircraft": hx.Int(mode="input", default=1, optionality="optional", validation={"min_value": 0}, async_input=["rarc_task"], async_output=common_tasks, view={"label": "Number of\nAircraft"}),
    "operator": hx.Str(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Operator Name"}),
    "aircraft_master_series": hx.Str(mode="input", default=None, optionality="optional", options_data="../../../../../../sql_db/master_series", options_field="aircraft_master_series", allow_custom_value=True, async_input=["rarc_task"], async_output=common_tasks, view={"label": "Master Series"}),
    "registration": hx.Str(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Registration"}),
    "aircraft_status": hx.Str(mode="input", default=None, optionality="optional", options_table="al_StatusMapping", options_column="Airlines Rater Mapped Name", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Status"}),
    "coverage": hx.Str(mode="input", default=None, optionality="optional", options=["Full Cover", "TLO"], async_input=["rarc_task"], async_output=common_tasks, view={"label": "Coverage"}),
    "attachment_date": hx.Date(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Risk\nAttachment\nDate"}),
    "expiry_date": hx.Date(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Risk\nExpiry\nDate"}),
    "time_in_service": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "% Time in\nService", "format": percent_format()}),
    "build_year": hx.Int(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Build Year", "format": integer_format()}),
    "usage": hx.Str(mode="input", default=None, optionality="optional", options=c.usage_options, async_input=["rarc_task"], async_output=common_tasks, view={"label": "Usage"}),
    "primary_usage": hx.Str(mode="input", default=None, optionality="optional", options=c.primary_usage_options, async_input=["rarc_task"], async_output=common_tasks, view={"label": "Primary Usage"}),
    "market_class": hx.Str(mode="input", default=None, optionality="optional", options_table="al_HullFreqClass", options_column="Class", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Market Class"}),
    "russian_built": hx.Bool(mode="input", default=False, async_input=["rarc_task"], async_output=common_tasks, view={"label": "Russian\nBuilt?"}),
    "operator_country": hx.Str(mode="input", default=None, optionality="optional", options_table="OperatorCountryList", options_column="Country", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Operator Country"}),
    "total_seats": hx.Int(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Seats", "format": integer_format()}),
    "previous12_months_hours": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Utilisation\n(Annual hrs)", "format": thousands_format()}),
    "operating_mtow_lb": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "MTOW", "format": thousands_format()}),
    "value": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Value", "format": thousands_format()}),
    "hull_limit": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Hull Limit", "format": thousands_format()}),
    "hull_excess": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Hull Excess", "format": thousands_format()}),
    "hull_ccy": hx.Str(mode="input", default=None, optionality="optional", options=c.ccy_options, async_input=["rarc_task"], async_output=common_tasks, view={"label": "Hull\nCurrency"}),
    "liability_limit": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Liability\nLimit", "format": thousands_format()}),
    "liability_excess": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Liability\nExcess", "format": thousands_format()}),
    "liability_ccy": hx.Str(mode="input", default=None, optionality="optional", options=c.ccy_options, async_input=["rarc_task"], async_output=common_tasks, view={"label": "Liability\nCurrency"}),
    "pll_award": hx.Float(mode="override", async_input=["fetch_by_registration_task", "rarc_task"], view={"label": "PLL\nAward", "format": thousands_format()}),
    "tpl_limit_exposed": hx.Float(mode="override", async_input=["fetch_by_registration_task", "rarc_task"], view={"label": "TPL Limit\nExposed", "format": percent_format(2)}),
    "achieved_hull_rate": hx.Float(mode="override", async_input=["fetch_by_registration_task", "rarc_task"], view={"label": "Gross\nAchieved\nHull Rate", "format": percent_format(2)}),
}

airlines_outputs = {
    "operator_region": hx.Str(mode="output", view={"label": "Operator Region"}),
}

airlines_validation_nodes = {
    (col + "_check"): hx.Str(mode="output", view={"label": "Error"}) for col in airlines_validation_cols
}

airlines_dict = {
    **airlines_inputs,
    **airlines_outputs,
    **airlines_validation_nodes,
    "has_error": hx.Bool(mode="output"), # For table validation
}

airlines_rating = {
    # Fleet Details
    "no_of_aircraft": hx.Int(mode="output", view={"label": "Number of\nAircraft", "group": "Fleet Details"}),
    "registration": hx.Str(mode="output", view={"label": "Registration", "group": "Fleet Details"}),
    "value_usd": hx.Float(mode="output", view={"label": "Value\n(USD)", "format": thousands_format(0), "group": "Fleet Details"}),
    "coverage": hx.Str(mode="output", view={"label": "Coverage", "group": "Fleet Details"}),
    "attachment_date": hx.Date(mode="output", view={"label": "Risk\nAttachment\nDate", "group": "Fleet Details"}),
    "expiry_date": hx.Date(mode="output", view={"label": "Risk\nExpiry\nDate", "group": "Fleet Details"}),
    "usage": hx.Str(mode="output", view={"label": "Usage", "group": "Fleet Details"}),
    "market_class": hx.Str(mode="output", view={"label": "Market\nClass", "group": "Fleet Details"}),
    "build_year": hx.Int(mode="output", view={"label": "Build\nYear", "group": "Fleet Details"}),
    "aircraft_status": hx.Str(mode="output", view={"label": "Status", "group": "Fleet Details"}),
    "previous12_months_hours": hx.Float(mode="output", view={"label": "Utilisation\n(Annual hrs)", "format": thousands_format(0), "group": "Fleet Details"}),
    "operator_region": hx.Str(mode="output", view={"label": "Operator\nRegion", "group": "Fleet Details"}),
    "russian_built": hx.Bool(mode="output", view={"label": "Russian\nBuilt?", "group": "Fleet Details"}),
    "total_seats": hx.Int(mode="output", view={"label": "Seats", "group": "Fleet Details"}),
    "operating_mtow_lb": hx.Float(mode="output", view={"label": "Operating\nMTOW", "format": thousands_format(0), "group": "Fleet Details"}),
    "include": hx.Bool(mode="output", view={"label": "Include?"}),

    # Hull Pricing
    "hull_f_base": hx.Float(mode="output", view={"label": "Base\nFrequency", "format": percent_format(3), "group": "Hull Pricing"}),
    "hull_f_status": hx.Float(mode="output", view={"label": "Status", "format": thousands_format(4), "group": "Hull Pricing"}),
    "hull_f_operator_region": hx.Float(mode="output", view={"label": "Operator\nRegion", "format": thousands_format(4), "group": "Hull Pricing"}),
    "hull_f_previous12_months_hours": hx.Float(mode="output", view={"label": "Utilisation\n(Annual hrs)", "format": thousands_format(4), "group": "Hull Pricing"}),
    "hull_f_market_class": hx.Float(mode="output", view={"label": "Market\nClass", "format": thousands_format(4), "group": "Hull Pricing"}),
    "hull_f_build_year_group": hx.Str(mode="output", view={"label": "Build Year\nGroup", "group": "Hull Pricing"}),
    "hull_f_build_year": hx.Float(mode="output", view={"label": "Build\nYear", "format": thousands_format(4), "group": "Hull Pricing"}),
    "hull_f_usage": hx.Float(mode="output", view={"label": "Usage", "format": thousands_format(4), "group": "Hull Pricing"}),
    "hull_frequency": hx.Float(mode="output", view={"label": "Frequency", "format": percent_format(3), "group": "Hull Pricing"}),
    "hull_s_base": hx.Float(mode="output", view={"label": "Base\nSeverity", "format": percent_format(1), "group": "Hull Pricing"}),
    "hull_s_previous12_months_hours": hx.Float(mode="output", view={"label": "Utilisation\n(Annual hrs)", "format": thousands_format(4), "group": "Hull Pricing"}),
    "hull_s_market_class": hx.Float(mode="output", view={"label": "Market\nClass", "format": thousands_format(4), "group": "Hull Pricing"}),
    "hull_s_russian_built": hx.Float(mode="output", view={"label": "Russian\nBuild", "format": thousands_format(4), "group": "Hull Pricing"}),
    "hull_s_mtow": hx.Float(mode="output", view={"label": "MTOW", "format": thousands_format(4), "group": "Hull Pricing"}),
    "hull_s_build_year_group": hx.Str(mode="output", view={"label": "Build Year\nGroup", "group": "Hull Pricing"}),
    "hull_s_build_year": hx.Float(mode="output", view={"label": "Build\nYear", "format": thousands_format(4), "group": "Hull Pricing"}),
    "hull_severity": hx.Float(mode="output", view={"label": "Severity", "format": percent_format(1), "group": "Hull Pricing"}),
    "hull_low_value_load": hx.Float(mode="output", view={"label": "Low Value\nCraft Load", "format": thousands_format(4), "group": "Hull Pricing"}),
    "hull_fleet_adj": hx.Float(mode="output", view={"label": "Fleet\nAdjustment", "format": thousands_format(4), "group": "Hull Pricing"}),
    "hull_attr_uplift": hx.Float(mode="output", view={"label": "Attritional\nUplift", "format": thousands_format(4), "group": "Hull Pricing"}),
    "hull_loss_cost_gu_usd": hx.Float(mode="output", view={"label": "Loss Cost\nGU(USD)", "format": thousands_format(), "group": "Hull Pricing"}),
    "hull_limit_point": hx.Float(mode="output", view={"label": "Limit\nPoint", "format": thousands_format(4), "group": "Hull Pricing"}),
    "hull_excess_point": hx.Float(mode="output", view={"label": "Excess\nPoint", "format": thousands_format(4), "group": "Hull Pricing"}),
    "hull_loss_cost_usd": hx.Float(mode="output", view={"label": "Hull Loss\nCost (USD)", "format": thousands_format(), "group": "Hull Pricing"}),
    "hull_limit_usd": hx.Float(mode="output", view={"label": "Hull Limit\n(USD)", "format": thousands_format(), "group": "Hull Pricing"}),
    "hull_excess_usd": hx.Float(mode="output", view={"label": "Hull Excess\n(USD)", "format": thousands_format(), "group": "Hull Pricing"}),

    # PAX Liability
    "pax_seats_in_service": hx.Int(mode="output", view={"label": "Seats In\nService", "group": "PAX Liability"}),
    "pax_base_freq_year_built": hx.Float(mode="output", view={"label": "Base Freq x\nYear Built", "format": percent_format(4), "group": "PAX Liability"}),
    "pax_status": hx.Float(mode="output", view={"label": "Status", "format": percent_format(1), "group": "PAX Liability"}),
    "pax_operator_region": hx.Float(mode="output", view={"label": "Operator\nRegion", "format": thousands_format(4), "group": "PAX Liability"}),
    "pax_12_months_hours": hx.Float(mode="output", view={"label": "12 months\nhours", "format": thousands_format(4), "group": "PAX Liability"}),
    "pax_market_class": hx.Float(mode="output", view={"label": "Market\nClass", "format": thousands_format(4), "group": "PAX Liability"}),
    "pax_severity_per_seat_usd": hx.Float(mode="output", view={"label": "Severity Per\nSeat (USD)", "format": thousands_format(), "group": "PAX Liability"}),
    "pax_attr_uplift": hx.Float(mode="output", view={"label": "Attritional\nUplift", "format": thousands_format(4), "group": "PAX Liability"}),
    "pax_liability_per_seat": hx.Float(mode="output", view={"label": "PAX Liability\nPer Seat", "format": thousands_format(), "group": "PAX Liability"}),
    "pax_fleet_adj": hx.Float(mode="output", view={"label": "Fleet\nAdjustment", "format": thousands_format(4), "group": "PAX Liability"}),
    "pax_loss_cost_gu_usd": hx.Float(mode="output", view={"label": "PAX GU\nLoss Cost (USD)", "format": thousands_format(), "group": "PAX Liability"}),
    "pax_limit_point": hx.Float(mode="output", view={"label": "Limit\nPoint", "format": thousands_format(4), "group": "PAX Liability"}),
    "pax_attachment_point": hx.Float(mode="output", view={"label": "Attachment\nPoint", "format": thousands_format(4), "group": "PAX Liability"}),
    "liability_limit_usd": hx.Float(mode="output", view={"label": "Liability\nLimit (USD)", "format": thousands_format(), "group": "PAX Liability"}),
    "liability_excess_usd": hx.Float(mode="output", view={"label": "Liability\nExcess (USD)", "format": thousands_format(), "group": "PAX Liability"}),
    "pax_loss_cost_usd": hx.Float(mode="output", view={"label": "PAX Loss\nCost(USD)", "format": thousands_format(), "group": "PAX Liability"}),

    # TPL Liability
    "tpl_liab_limit_exposed": hx.Float(mode="output", view={"label": "Liability Limit\n% Exposed", "format": percent_format(1), "group": "TPL Liability"}),
    "tpl_usage": hx.Float(mode="output", view={"label": "Usage", "format": thousands_format(4), "group": "TPL Liability"}),
    "tpl_rate_on_limit": hx.Float(mode="output", view={"label": "Rate on\nLimit", "format": percent_format(3), "group": "TPL Liability"}),
    "tpl_base_loss_cost_usd": hx.Float(mode="output", view={"label": "Base Loss\nCost (USD)", "format": thousands_format(), "group": "TPL Liability"}),
    "tpl_fleet_adj": hx.Float(mode="output", view={"label": "Fleet\nAdjustment", "format": thousands_format(4), "group": "TPL Liability"}),
    "tpl_loss_cost_usd": hx.Float(mode="output", view={"label": "TPL Loss Cost\n(USD)", "format": thousands_format(), "group": "TPL Liability"}),

    # Benchmarking
    "bm_term_adj": hx.Float(mode="output", view={"label": "Term\nAdjustment", "format": thousands_format(4), "group": "Benchmarking"}),
    "bm_hull_large_loss_cost": hx.Float(mode="output", view={"label": "Hull Large\nLoss Cost", "format": thousands_format(), "group": "Benchmarking"}),
    "bm_hull_large_severity": hx.Float(mode="output", view={"label": "Hull Large\nSeverity", "format": thousands_format(), "group": "Benchmarking"}),
    "bm_liab_large_frequency": hx.Float(mode="output", view={"label": "Liab Large\nFrequency", "format": percent_format(3), "group": "Benchmarking"}),
    "bm_liab_large_loss_cost": hx.Float(mode="output", view={"label": "Liab Large\nLoss Cost", "format": thousands_format(), "group": "Benchmarking"}),
    "bm_liab_large_severity": hx.Float(mode="output", view={"label": "Liability Large\nSeverity", "format": thousands_format(), "group": "Benchmarking"}),
    "bm_hull_benchmark": hx.Float(mode="output", view={"label": "Hull\nBenchmark", "format": thousands_format(), "group": "Benchmarking"}),
    "bm_hull_benchmark_rate": hx.Float(mode="output", view={"label": "Hull Benchmark\nRate", "format": percent_format(3), "group": "Benchmarking"}),
    "bm_pax_liab_benchmark_cost": hx.Float(mode="output", view={"label": "PAX Liability\nBenchmark Cost", "format": thousands_format(), "group": "Benchmarking"}),
    "bm_pax_liability_per_seat": hx.Float(mode="output", view={"label": "PAX Liability\nPer Seat", "format": thousands_format(), "group": "Benchmarking"}),
    "bm_tpl_benchmark": hx.Float(mode="output", view={"label": "TPL\nBenchmark", "format": thousands_format(), "group": "Benchmarking"}),
    "bm_allocated_hull_premium": hx.Float(mode="output", view={"label": "Allocated Hull\nPremium", "format": thousands_format(), "group": "Benchmarking"}),
    "bm_aircraft_in_expiry_fleet": hx.Bool(mode="output", view={"label": "Aircraft in\nExpiry Fleet", "group": "Benchmarking"}),
    "bm_total_liab_premium": hx.Float(mode="output", view={"label": "Total Liab\nPremium", "format": thousands_format(), "group": "Benchmarking"}),
    "bm_allocated_liab_premium": hx.Float(mode="output", view={"label": "Allocated Liab\nPremium", "format": thousands_format(), "group": "Benchmarking"}),
}

airlines_rating_summary = {
    "fleet_size": hx.Int(mode="output", view={"label": "Fleet Size", "group": "Fleet Details"}),
    "hull_loss_cost": hx.Float(mode="output", view={"label": "Expected Fleet Hull Loss Cost", "format": thousands_format(), "group": "Hull Pricing"}),
    "total_seats": hx.Int(mode="output", view={"label": "Total number of seats in service", "format": thousands_format(), "group": "PAX Liability"}),
    "pax_loss_cost": hx.Float(mode="output", view={"label": "Expected Fleet PAX Liability Loss Cost", "format": thousands_format(), "group": "PAX Liability"}),
    "tpl_loss_cost": hx.Float(mode="output", view={"label": "Expected Fleet TPL Liability Loss Cost", "format": thousands_format(), "group": "TPL Liability"}),
    "hull_large_severity": hx.Float(mode="output", view={"label": "Avg Hull Large Severity", "format": thousands_format(), "group": "Benchmarking"}),
    "liab_large_severity": hx.Float(mode="output", view={"label": "Avg Liability Large Severity", "format": thousands_format(), "group": "Benchmarking"}),
}

summary_totals_dict = {
    "hull_value": hx.Float(mode="output", view={"label": "Hull\nValue", "format": thousands_format()}),
    "hull_benchmark": hx.Float(mode="output", view={"label": "Hull\nBenchmark", "format": thousands_format()}),
    "hull_benchmark_rate": hx.Float(mode="output", view={"label": "Hull\nBenchmark\nRate", "format": percent_format(2)}),
    "pax_limit": hx.Float(mode="output", view={"label": "PAX Limit", "format": thousands_format()}),
    "pax_liab_benchmark": hx.Float(mode="output", view={"label": "PAX\nLiability\nBenchmark", "format": thousands_format()}),
    "pax_liab_benchmark_per_seat": hx.Float(mode="output", view={"label": "PAX\nLiability\nBenchmark\nPer Seat", "format": thousands_format()}),
    "tpl_benchmark": hx.Float(mode="output", view={"label": "TPL\nBenchmark", "format": thousands_format()}),
    "total_hull_benchmark": hx.Float(mode="output", view={"label": "Total\nHull\nBenchmark", "format": thousands_format()}),
    "total_liab_benchmark": hx.Float(mode="output", view={"label": "Total\nLiability\nBenchmark", "format": thousands_format()}),
    "total_benchmark": hx.Float(mode="output", view={"label": "Total\nBenchmark", "format": thousands_format()})
}

summary_dict = {
    "include": hx.Bool(mode="output", view={"label": "Include?"}),
    "market_class": hx.Str(mode="output", view={"label": "Market Class"}),
    "aircraft_class": hx.Str(mode="output", view={"label": "Class"}),
    "no_of_aircraft": hx.Int(mode="output", view={"label": "Number of\nAircraft"}),
    "registration": hx.Str(mode="output", view={"label": "Registration"}),
    **summary_totals_dict
}

### --- GENERAL AVIATION FIELDS --- ###
ga_validation_cols = [
    "no_of_aircraft",
    "value",
    "attachment_date",
    "expiry_date",
    "time_in_service",
    "per_occ_deductible_pct",
    "per_occ_deductible",
    "total_seats",
    "crew_seats",
    "per_pax_liab_limit",
    "combined_single_limit",
    "tpl_limit_exposed",
    "build_year",
    "use",
    "operator_country",
    "aircraft_class"
]

ga_inputs = {
    "include": hx.Bool(mode="input", default=True, async_input=["rarc_task"], async_output=[{"task": "fill_with_defaults_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], view={"label": "Include\nExposure?"}),
    "aircraft_class": hx.Str(mode="input", default=None, optionality="optional", async_input=["rarc_task"], options=c.aircraft_class_options, async_output=common_tasks, view={"label": "Class"}),
    "operator": hx.Str(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Operator Name"}),
    "aircraft_master_series": hx.Str(mode="input", default=None, optionality="optional", async_input=["rarc_task"], options_data="../../../../../../sql_db/master_series", options_field="aircraft_master_series", allow_custom_value=True, async_output=common_tasks, view={"label": "Master Series"}),
    "no_of_aircraft": hx.Int(mode="input", default=1, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Number of\nAircraft"}),
    "registration": hx.Str(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Registration"}),
    "value": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Hull\nValue", "format": thousands_format()}),
    "hull_ccy": hx.Str(mode="input", default=None, optionality="optional", async_input=["rarc_task"], options=c.ccy_options, async_output=common_tasks, view={"label": "Hull\nCurrency"}),
    "attachment_date": hx.Date(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Risk\nAttachment\nDate"}),
    "expiry_date": hx.Date(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Risk\nExpiry\nDate"}),
    "time_in_service": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task", "fill_pax_limit_implied"], async_output=common_tasks, view={"label": "% Time in\nService", "format": percent_format()}), # FS 25/09/2025: "fill_pax_limit_implied" async task added
    "build_location": hx.Str(mode="input", default=None, optionality="optional", async_input=["rarc_task"], options=["Non-Russian Built", "Russian Built"], async_output=common_tasks, view={"label": "Build\nLocation"}),
    "build_year": hx.Int(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Build\nYear", "format": integer_format()}),
    "operator_country": hx.Str(mode="input", default=None, optionality="optional", options_table="OperatorCountryList", options_column="Country", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Operator Country"}),
    "use": hx.Str(mode="input", default=None, optionality="optional", options=c.ga_use_options, async_input=["rarc_task"], async_output=common_tasks, view={"label": "Use"}),
    "per_occ_deductible_pct": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Per Occ\nDeductible %", "format": percent_format(1)}),
    "per_occ_deductible": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "Per Occ\nDeductible", "format": thousands_format()}),
    "pax_net_worth": hx.Str(mode="input", default=None, optionality="optional", async_input=["rarc_task"], options=["Low", "High", "Unknown"], async_output=common_tasks, view={"label": "PAX\nNet Worth"}),
    "total_seats": hx.Int(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Total Seats\n(Crew + PAX)", "format": integer_format()}),
    "crew_seats": hx.Int(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "Total\nCrew\nSeats", "format": integer_format()}),
    "per_pax_liab_limit": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task", "fill_pax_limit_implied"], async_output=[*common_tasks, {"task": "fill_pax_limit_implied", "reset": False}], view={"label": "Per PAX\nLiability\nLimit", "format": thousands_format()}), # FS 25/09/2025: "fill_pax_limit_implied" async task added
    "combined_single_limit": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=common_tasks, view={"label": "CSL", "format": thousands_format()}),
    "liability_ccy": hx.Str(mode="input", default=None, optionality="optional", options=c.ccy_options, async_input=["rarc_task"], async_output=common_tasks, view={"label": "Liability\nCurrency"}),
    "tpl_limit_exposed": hx.Float(mode="input", default=None, optionality="optional", async_input=["fetch_by_registration_task", "rarc_task"], async_output=common_tasks, view={"label": "TPL Limit\nExposed", "format": percent_format(2)}),
    "achieved_hull_rate": hx.Float(mode="override", async_input=["fetch_by_registration_task", "rarc_task"], view={"label": "Gross\nAchieved\nHull Rate", "format": percent_format(2)}),   
}

ga_outputs = {
    "number_of_engines": hx.Str(mode="output", view={"label": "Number of\nEngines"}),
    "operator_region": hx.Str(mode="output", view={"label": "Operator Region"}),
    "seat_occupancy": hx.Float(mode="output", view={"label": "Expected\nSeat\nOccupancy", "format": percent_format(1)}),
    "fatality": hx.Float(mode="output", view={"label": "Fatality", "format": percent_format(1)}),
    "hull_benchmark_rate": hx.Float(mode="output", view={"label": "Hull\nBenchmark\nRate", "format": percent_format(2)}),
    "pax_liab_benchmark_per_seat": hx.Float(mode="output", view={"label": "PAX\nLiability\nBenchmark\nPer Seat", "format": thousands_format()}),
    "tpl_benchmark": hx.Float(mode="output", view={"label": "TPL\nBenchmark", "format": thousands_format()}),
    "total_hull_benchmark": hx.Float(mode="output", view={"label": "Total\nHull\nBenchmark", "format": thousands_format()}),
    "total_liab_benchmark": hx.Float(mode="output", view={"label": "Total\nLiability\nBenchmark", "format": thousands_format()}),
    "renewing_aircraft": hx.Str(mode="output", view={"label": "Renewing\nAircraft"}),
    "bm_allocated_hull_premium": hx.Float(mode="output", view={"label": "Allocated Hull\nPremium", "format": thousands_format()}),
    "bm_allocated_liab_premium": hx.Float(mode="output", view={"label": "Allocated Liab\nPremium", "format": thousands_format()}),
}

ga_validation_nodes = {
    (col + "_check"): hx.Str(mode="output", view={"label": "Error"}) for col in ga_validation_cols
}

ga_dict = {
    **ga_inputs,
    **ga_outputs,
    **ga_validation_nodes,
    "has_error": hx.Bool(mode="output"), # For table validation
}

ga_rating = {
    "include": hx.Bool(mode="output", view={"label": "Include?"}),
    "bm_term_adj": hx.Float(mode="output", view={"label": "Term\nAdjustment", "format": thousands_format(2)}), # Including "bm_" for consistency with Airlines
    
    # Total Loss Freq
    "aircraft_class": hx.Str(mode="output", view={"label": "Aircraft Class"}),
    "base_rate": hx.Float(mode="output", view={"label": "Base Rate", "format": percent_format(2)}),
    "no_of_aircraft": hx.Int(mode="output", view={"label": "Number of\nAircraft", "format": thousands_format(0)}),
    "base_freq_all_aircraft": hx.Float(mode="output", view={"label": "Base Freq\n(All Aircraft)", "format": percent_format(2)}),
    "hull_value_usd": hx.Float(mode="output", view={"label": "Hull Value\n(USD)", "format": thousands_format(0)}),
    "hull_value_adjuster": hx.Float(mode="output", view={"label": "Hull Value\nAdjuster", "format": thousands_format(2)}),
    "time_in_service": hx.Float(mode="output", view={"label": "% Time in\nService", "format": percent_format(0)}),
    "status_adjuster": hx.Float(mode="output", view={"label": "Status\nAdjuster", "format": thousands_format(2)}),
    "build_location": hx.Str(mode="output", view={"label": "Build Location"}),
    "build_location_adjuster": hx.Float(mode="output", view={"label": "Build Location\nAdjuster", "format": thousands_format(2)}),
    "freq_region": hx.Str(mode="output", view={"label": "Region"}),
    "use": hx.Str(mode="output", view={"label": "Use"}),
    "region_x_use_adjuster": hx.Float(mode="output", view={"label": "Region x\nUse Adjuster", "format": thousands_format(2)}),
    "region_adjuster": hx.Float(mode="output", view={"label": "Region\nAdjuster", "format": thousands_format(2)}),
    "use_adjuster": hx.Float(mode="output", view={"label": "Use\nAdjuster", "format": thousands_format(2)}),
    "fleet_size": hx.Int(mode="output", view={"label": "Fleet Size", "format": thousands_format(0)}),
    "fleet_size_adjuster": hx.Float(mode="output", view={"label": "Fleet\nSize\nAdjuster", "format": thousands_format(2)}),
    "exp_total_losses": hx.Float(mode="output", view={"label": "Expected\nNumber of\nTotal Losses", "format": thousands_format(4)}),
    "exp_partial_losses": hx.Float(mode="output", view={"label": "Expected\nNumber of\nPartial Losses", "format": thousands_format(4)}),

    # Hull Rating
    "hull_per_occ_deductible_usd": hx.Float(mode="output", view={"label": "Per Occ\nDeductible\n(USD)", "format": thousands_format(0)}),
    "hull_severity": hx.Float(mode="output", view={"label": "Loss Severity", "format": thousands_format(0)}),
    "hull_partial_base_severity": hx.Float(mode="output", view={"label": "Partial\nBase Severity", "format": percent_format(0)}),
    "hull_partial_engine_adjuster": hx.Float(mode="output", view={"label": "Partial\nEngine Factor", "format": thousands_format(2)}),
    "hull_partial_build_year_adjuster": hx.Float(mode="output", view={"label": "Partial Build\nYear Factor", "format": thousands_format(2)}),
    "hull_total_loss_unadjusted": hx.Float(mode="output", view={"label": "Expected\nTotal Losses", "format": thousands_format(0)}),
    "hull_partial_loss_unadjusted": hx.Float(mode="output", view={"label": "Expected\nPartial Losses", "format": thousands_format(0)}),
    "hull_expected_loss_unadjusted": hx.Float(mode="output", view={"label": "Expected Loss\n(Total & Partial Losses)", "format": thousands_format(0)}),
    "hull_attritional_adjuster": hx.Float(mode="output", view={"label": "Attritional\nAdjuster", "format": thousands_format(2)}),
    "hull_expected_loss": hx.Float(mode="output", view={"label": "Expected\nLoss", "format": thousands_format(0)}),
    "hull_benchmark_cost": hx.Float(mode="output", view={"label": "Benchmark", "format": thousands_format(0)}),
    "hull_net_rate": hx.Float(mode="output", view={"label": "Net\nRate", "format": percent_format(2)}),
    "hull_benchmark_rate": hx.Float(mode="output", view={"label": "Benchmark\nRate", "format": percent_format(4)}),

    # PAX Rating
    "pax_exp_total_losses": hx.Float(mode="output", view={"label": "Expected\nNumber of\nTotal Losses", "format": thousands_format(4)}),
    "total_seats_all_aircraft": hx.Int(mode="output", view={"label": "Total Number\nof Seats\nfrom All Aircraft", "format": thousands_format(0)}),
    "total_seats": hx.Int(mode="output", view={"label": "Number\nof Seats", "format": thousands_format(0)}),
    "seat_occupancy": hx.Float(mode="output", view={"label": "Expected Seat\nOccupany %", "format": percent_format(0)}),
    "fatality": hx.Float(mode="output", view={"label": "Fatality %", "format": percent_format(0)}),
    "exp_no_of_deaths": hx.Float(mode="output", view={"label": "Expected No.\nof Deaths", "info": "When a Total Loss Occurs", "format": thousands_format(2)}),
    "operator_region": hx.Str(mode="output", view={"label": "Region"}),
    "pax_award_usd": hx.Float(mode="output", view={"label": "PAX Award\n(USD)", "format": thousands_format(0)}),
    "pax_limit_usd": hx.Float(mode="output", view={"label": "PAX Limit\n(USD)", "format": thousands_format(0)}),
    "apply_pax_limit": hx.Float(mode="output", view={"label": "Apply PAX\nLimit", "format": thousands_format(0)}),
    "gu_pax_losses": hx.Float(mode="output", view={"label": "GU PAX\nLosses", "format": thousands_format(0)}),
    "max_pax_losses": hx.Float(mode="output", view={"label": "Max PAX\nLosses\n(Full Occy)", "format": thousands_format(0)}),
    "pax_per_occ_limit_usd": hx.Float(mode="output", view={"label": "Per Occ\nLimit\n(USD)", "format": thousands_format(0)}),
    "pax_apply_occ_limit_ded": hx.Float(mode="output", view={"label": "Apply\nOccurrence\nLimit/Deductible", "format": thousands_format(0)}),
    "pax_apply_occ_limit_ded_to_max_loss": hx.Float(mode="output", view={"label": "Apply\nOccurrence\nLimit/Deductible\nto Max Loss", "format": thousands_format(0)}),
    "pax_exp_loss_from_total_losses": hx.Float(mode="output", view={"label": "Expected\nLoss from\nTotal Losses", "format": thousands_format(0)}),
    "pax_attritional_adjuster": hx.Float(mode="output", view={"label": "Attritional\nAdjuster", "format": thousands_format(2)}),
    "pax_expected_loss": hx.Float(mode="output", view={"label": "Expected\nLoss", "format": thousands_format(0)}),
    "pax_benchmark_cost": hx.Float(mode="output", view={"label": "Benchmark", "format": thousands_format(0)}),
    "pax_benchmark_per_seat": hx.Int(mode="output", view={"label": "Benchmark\nper Seat", "format": thousands_format(0)}),

    # TPL Rating
    "tpl_limit_usd": hx.Float(mode="output", view={"label": "TPL Limit\n(USD)", "format": thousands_format(0)}),
    "tpl_limit_exposed": hx.Float(mode="output", view={"label": "Limit\nExposed\n(USD)", "format": percent_format(0)}),
    "tpl_net_rol_exposed": hx.Float(mode="output", view={"label": "Net Rate\non Line\n(Exposed)", "format": percent_format(4)}),
    "tpl_net_rol_unexposed": hx.Float(mode="output", view={"label": "Net Rate\non Line\n(Unexposed)", "format": percent_format(5)}),
    "tpl_expected_loss_unadjusted": hx.Float(mode="output", view={"label": "Expected\nLoss\n(Unadjusted)", "format": thousands_format(0)}),
    "tpl_expected_loss": hx.Float(mode="output", view={"label": "Expected\nLoss", "format": thousands_format(0)}),
    "tpl_benchmark_cost": hx.Float(mode="output", view={"label": "Benchmark", "format": thousands_format(0)}),
    "tpl_net_rate": hx.Float(mode="output", view={"label": "Net\nRate", "format": percent_format(3)}),
    "tpl_gross_rate": hx.Float(mode="output", view={"label": "Gross\nRate", "format": percent_format(3)}),
}

### --- EXPOSURE DICTIONARY COMBINING AIRLINES AND GA --- ###

exposure_dict = {
    ### --- Common fields --- ###
    "operators": hx.List(mode="input", async_output=[{"task": "start_renewal_task", "reset": False}], children={
        "operator": hx.Str(mode="input", async_input=["fetch_by_operator_task"], async_output=[{"task": "start_renewal_task", "reset": False}], default=None, optionality="optional", options_data="../../../../../../sql_db/operators", options_field="operator", view={"label": "Selected Operator"}),
        "operator_class": hx.Str(mode="output", view={"label": "TLO Operator Class"})
    }),
    "operator_search": hx.Str(mode="input", async_input=["search_for_operator_task"], async_output=[{"task": "start_renewal_task", "reset": False}],default=None, optionality="optional", view={"label": "Operator Search"}),
    "are_operators_fetched": hx.Bool(mode="output", async_output=["search_for_operator_task"]),
    "operators_msg": hx.Str(mode="output", async_output=["search_for_operator_task"]),
    "registrations": hx.List(mode="input", async_output=[{"task": "start_renewal_task", "reset": False}], children={
        "registration": hx.Str(mode="input", async_input=["fetch_by_registration_task", "get_selected_regs_task"], async_output=[{"task": "start_renewal_task", "reset": False}], default=None, optionality="optional", options_data="../../../../../../sql_db/registrations", options_field="registration", view={"label": "Registration", "options": {"read_only": {"read_only": True}}}),
    }),
    "has_missing_regs": hx.Bool(mode="output", async_output=["fetch_by_registration_task", "get_selected_regs_task", "fetch_by_operator_task", "clear_table_task"]),
    "has_missing_regs_msg": hx.Str(mode="output", async_output=["fetch_by_registration_task", "get_selected_regs_task", "fetch_by_operator_task", "clear_table_task"]),
    "has_duplicate_regs": hx.Bool(mode="output"),
    "has_duplicate_regs_msg": hx.Str(mode="output", view={"style_cell": "hx-bad"}),
    "fleet_size": hx.Int(mode="override", async_input=["rarc_task"], view={"label": "Fleet Size"}),
    "hull_premium": hx.Structure(view={"label": "Hull Premium"}, children={
        "from_slip": hx.Float(mode="output", view={"label": "From Slip", "format": thousands_format(0)}),
        "from_rate": hx.Float(mode="output", view={"label": "From Hull Rates", "format": thousands_format(0), "options": {"red": {"style_cell": "hx-bad"}}}),
        "are_premiums_equal": hx.Bool(mode="output"),
        "are_premiums_different": hx.Bool(mode="output"),
        "difference_msg": hx.Str(mode="output")
    }),
    "data_check": hx.Str(mode="output"),
    "show_check_cols": hx.Bool(mode="input", async_output=[{"task": "start_renewal_task", "reset": False}], default=False, view={"label": "Validate Data"}),
    "show_full_table": hx.Bool(mode="output"),
    "show_validation_table": hx.Bool(mode="output"),
    "all_fields_valid": hx.Bool(mode="output"),
    "show_rc_page": hx.Bool(mode="output"),

    ### --- Airlines page --- ####
    "selected_operator_class": hx.Str(mode="input", default="G", options=["A", "B", "C", "D", "E", "F", "G"], async_input=["rarc_task"], async_output=common_tasks, view={"label": "Selected Operator Class"}),
    "status_split": hx.Structure(view={"label": "Status Split"}, children={
        "in_service": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=[{"task": "start_renewal_task", "reset": False}], view={"label": "In Service", "format": percent_format()}),
        "storage": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"],async_output=[{"task": "start_renewal_task", "reset": False}], view={"label": "Storage", "format": percent_format()}),
        "other": hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=[{"task": "start_renewal_task", "reset": False}], view={"label": "Other", "format": percent_format()})
    }),
    "status_split_msg": hx.Str(mode="output"),
    "show_status_split_msg": hx.Bool(mode="output"),
    "show_al_pricing": hx.Bool(mode="input", async_output=[{"task": "start_renewal_task", "reset": False}], default=False, view={"label": "Show Actuarial Pricing"}),
    # "airlines": hx.List(mode="input", async_input=["rarc_task"], async_output=["fetch_by_operator_task", {"task": "fetch_by_registration_task", "reset": False}, {"task": "get_selected_regs_task", "reset": False}, "clear_table_task", {"task": "rarc_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], children=airlines_dict),
    "airlines": hx.List(mode="input", async_input=["rarc_task"], async_output=[{"task": "start_renewal_task", "reset": False}, "fetch_by_operator_task", {"task": "fetch_by_registration_task", "reset": False}, {"task": "get_selected_regs_task", "reset": False}, "clear_table_task", {"task": "rarc_task", "reset": False}], children=airlines_dict),
    "airlines_default": hx.List(mode="input", async_output=[{"task": "start_renewal_task", "reset": False}, {"task": "show_airlines_task", "reset": False}], async_input=["fill_with_defaults_task"], max_element_count=1, children={
        **{
            node: hx_node(obj)(
                mode="input", 
                async_input=["fill_with_defaults_task"],
                async_output=[{"task": "start_renewal_task", "reset": False},{"task": "show_airlines_task", "reset": False}],
                **({"default": None, "optionality": "optional"} if obj.default==hx.nodes.UNDEFINED else {"default": obj.default, "optionality": obj.optionality}), 
                view=obj.view,
                **get_existing_attributes(obj, ["options", "options_table", "options_column", "options_data", "options_field", "allow_custom_value"])
            ) for node, obj in airlines_inputs.items() if node != "countries" # Exclude list created for dyanmic dropdowns
        },
        **airlines_outputs,
    }),
    "airlines_check_col_labels": hx.Structure(children={
        (col + "_check_label"): hx.Str(mode="output") for col in airlines_validation_cols
    }),
    "airlines_rating": hx.List(mode="output", children=airlines_rating),
    "airlines_rating_summary": hx.Structure(children=airlines_rating_summary),

    ### --- GA page --- ###
    "show_ga_pricing": hx.Bool(mode="input", default=False, async_output=[{"task": "start_renewal_task", "reset": False}], view={"label": "Show Actuarial Pricing"}),
    # "aircrafts": hx.List(mode="input", async_input=["rarc_task"], async_output=["fetch_by_operator_task", {"task": "fetch_by_registration_task", "reset": False}, {"task": "get_selected_regs_task", "reset": False}, "clear_table_task", {"task": "rarc_task", "reset": False}, {"task": "start_renewal_task", "reset": False}], children=ga_dict),
    "aircrafts": hx.List(mode="input", async_input=["rarc_task"], async_output=[{"task": "start_renewal_task", "reset": False},"fetch_by_operator_task", {"task": "fetch_by_registration_task", "reset": False}, {"task": "get_selected_regs_task", "reset": False}, "clear_table_task", {"task": "rarc_task", "reset": False}], children=ga_dict),
    "aircrafts_default": hx.List(mode="input", async_output=[{"task": "start_renewal_task", "reset": False}, {"task": "show_ga_task", "reset": False}], async_input=["fill_with_defaults_task"], max_element_count=1, children={
        **{
            node: hx_node(obj)(
                mode="input", 
                async_input=["fill_with_defaults_task"],
                async_output=[{"task": "start_renewal_task", "reset": False}, {"task": "show_ga_task", "reset": False}],
                **({"default": None, "optionality": "optional"} if obj.default==hx.nodes.UNDEFINED else {"default": obj.default, "optionality": obj.optionality}), 
                view=obj.view,
                **get_existing_attributes(obj, ["options", "options_table", "options_column", "options_data", "options_field", "allow_custom_value"])
            ) for node, obj in ga_inputs.items() if node != "countries" # Exclude list created for dyanmic dropdowns
        },
        **ga_outputs
    }),
    "ga_check_col_labels": hx.Structure(children={
        (col + "_check_label"): hx.Str(mode="output") for col in ga_validation_cols
    }),
    "ga_rating": hx.List(mode="output", children=ga_rating),

    ### --- Common Rating Summary --- ###
    "aircraft_summary": hx.List(mode="output", children=summary_dict),
    "aircraft_summary_total": hx.Structure(view={"label": "Totals"}, children=summary_totals_dict),
    "show_aircraft_summary": hx.Bool(mode="output"),
    "hide_aircraft_summary": hx.Bool(mode="output")
}

### --- COVERAGES --- ###
cover_selection_dict = {
    "cover_selection": hx.Structure(children={
        "are_fields_full": hx.Bool(mode="output"),
    }),
}

coverages_dict = {
    "hull": {"label": "Hull"},
    "liability": {"label": "Liability"}
}

cvg_common_fields = {
    "quoted_premium_net": hx.Float(mode="output", view={"label": "Net Quoted Premium", "format": thousands_format()}),
    "profit_commission": hx.Float(mode="input", default=0, async_output=[{"task": "start_renewal_task", "reset": False}], validation={"min_value": 0, "max_value": 1}, view={"label": "PC %", "format": percent_format(1)}),
    "ncb_pct": hx.Float(mode="input", default=0, async_output=[{"task": "start_renewal_task", "reset": False}], validation={"min_value": 0, "max_value": 1}, view={"label": "NCB %", "format": percent_format(1)}),
    "rate_change": hx.Float(mode="input", default=None, optionality="optional", async_output=[{"task": "start_renewal_task", "reset": False}], validation={"min_value": 0}, view={"label": "Rate Change", "format": percent_format(1)}),
    "rate_change_label": hx.Str(mode="output"),
    "benchmark_premium_exp": hx.Float(mode="output", view={"label": "Gross Benchmark Premium (Experience)", "format": thousands_format()}),
    "exp_credibility": hx.Float(mode="output", view={"label": "Experience Credibility Rate", "format": percent_format()}),
    "benchmark_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Gross Benchmark Premium (Blended)", "format": thousands_format()}),
    "benchmark_premium_post_uw_adj": hx.Float(mode="output", view={"label": "Gross Benchmark Premium (UW Adjusted)", "format": thousands_format()}),
    "pflr_net": hx.Float(mode="output", view={"label": "Implied Net LR", "format": percent_format(1)}),
    "business_plan_bpi": hx.Float(mode="output", view={"label": "Business Plan BPI", "format": percent_format(1)}),
    "roc_bpi": hx.Float(mode="output", view={"label": "BPI to meet 15% ROC", "format": percent_format(1)}),
}
    
hull_dict = {
    **cvg_common_fields,
    "coverage": hx.Str(mode="input", default=None, optionality="optional", options=["Full Cover", "Total Loss"], async_input=["show_airlines_task"], async_output=[{"task": "start_renewal_task", "reset": False}], view={"label": "Coverage"}),
    "benchmark_premium_pre_exp": hx.Float(mode="output", view={"label": "Gross Benchmark Premium", "info": "Pre-experience adjustment", "format": thousands_format()}),
    "benchmark_rate_pre_exp": hx.Float(mode="output", view={"label": "Gross Rate", "format": percent_format(2)}),
    "uw_adj": hx.Float(mode="input", default=1, async_input=["rarc_task"], async_output=[{"task": "start_renewal_task", "reset": False}], validation={"min_value": 0.5, "max_value": 1.5}, view={"label": "Hull UW Adjustment", "format": percent_format()}),
}

liability_dict = {
    **cvg_common_fields,
    "coverage": hx.Str(mode="input", default=None, optionality="optional", options=["Combined", "Passenger", "Third Party"], async_output=[{"task": "start_renewal_task", "reset": False}], view={"label": "Coverage"}),
    "pax": hx.Structure(view={"label": "PAX Liability"}, children={
        "benchmark_premium_pre_exp": hx.Float(mode="output", view={"label": "Gross Benchmark Premium", "info": "Pre-experience adjustment", "format": thousands_format()}),
        "benchmark_rate_pre_exp": hx.Str(mode="output", view={"label": "Gross Rate"}),
    }),
    "tpl": hx.Structure(view={"label": "TPL"}, children={
        "benchmark_premium_pre_exp": hx.Float(mode="output", view={"label": "Gross Benchmark Premium", "info": "Pre-experience adjustment",  "format": thousands_format()}),
        "benchmark_rate_pre_exp": hx.Float(mode="output", view={"label": "Gross Rate", "format": thousands_format()}),
    }),
    "uw_adj": hx.Float(mode="input", default=1, async_input=["rarc_task"], async_output=[{"task": "start_renewal_task", "reset": False}], validation={"min_value": 0.5, "max_value": 1.5}, view={"label": "Liability UW Adjustment", "format": percent_format()}),
    "min_rate_info": hx.Str(mode="output")
}

# Using the following dictionary as a subset of the data schema that is accessible in rating
all_coverages_dict = {
    "hull": hull_dict,
    "liability": liability_dict
}

### --- LAYERS --- ###
layers_dict = {
    "pilot_uw_adj": hx.Float(mode="input", default=1, async_input=["rarc_task"], async_output=[{"task": "start_renewal_task", "reset": False}], validation={"min_value": 0.5, "max_value": 1.5}, view={"label": "Pilot Experience", "format": percent_format()}),
    "quoted_premium_case_priced": hx.Float(mode="output", view={"label": "Gross Quoted Premium", "format": thousands_format()}),
    "totals": hx.Structure(view={"label": "Overall"}, children={
        "benchmark_premium": hx.Float(mode="output", view={"label": "Gross Benchmark Premium for Pol Term", "format": thousands_format()}),
        "quoted_premium": hx.Float(mode="output", view={"label": "Gross Quoted Premium", "format": thousands_format()}),
        "pflr": hx.Float(mode="output", view={"label": "Implied Gross LR", "format": percent_format(1)}),
        "pflr_net": hx.Float(mode="output", view={"label": "Implied Net LR", "format": percent_format(1)}),
        "bpi": hx.Float(mode="output", view={"label": "BPI", "format": percent_format(1)}),
        "technical_premium": hx.Float(mode="output", view={"label": "Gross Technical Premium for Pol Term", "format": thousands_format()}),
        "technical_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Gross Technical Premium for Pol Term (Pre-UW Adjustment)", "format": thousands_format()}),
        "tpi": hx.Float(mode="output", view={"label": "TPI", "format": percent_format(1)}),
        "tpi_pre_uw_adj": hx.Float(mode="output", view={"label": "TPI (Pre-UW Adjustment)", "format": percent_format(1)}),
    })
}

### --- EXPERIENCE RATING --- ###
input_dict = {
    "historic_premium_known": hx.Bool(mode="input", default=False, async_input=["rarc_task"], async_output=common_tasks, view={"label": "Historic premium known?", "info": "If not known, enter the new/renewing EPI for all claims history years."}),
    "no_of_years_history": hx.Int(mode="input", default=10, validation={"min_value": 0}, async_input=["fill_historic_premium_task"], async_output=common_tasks, view={"label": "Number of years of history"}),
    "show_rc_calcs": hx.Bool(mode="input", async_output=[{"task": "start_renewal_task", "reset": False}], default=False, view={"label": "Show Rate Change Calcs"}),
    "as_at_date": hx.Date(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=[{"task": task, "reset": False} for task in ["show_airlines_task", "show_ga_task", "start_renewal_task"]], view={"label": "As At Date", "info": "The cut-off date for the claims."}),
    "as_at_date_message": hx.Str(mode="output"),
    "show_date_message": hx.Bool(mode="output"),
    "expiring_claims_msg": hx.Str(mode="output", async_output=["show_airlines_task", "show_ga_task", "start_renewal_task"]),
    "show_expiring_claims_msg": hx.Bool(mode="output", async_output=["show_airlines_task", "show_ga_task", "start_renewal_task"]),
}

# claims_dict = {"yoa": hx.Int(mode="output", async_input=["show_airlines_task", "show_ga_task"], view={"label": "YOA", "format": integer_format()})}
claims_dict = {"yoa": hx.Int(
        mode="input", default=None, optionality="optional",
        async_input=["rarc_task"],
        async_output=[{"task": task, "reset": False} for task in ["show_airlines_task", "show_ga_task", "start_renewal_task"]], 
        view={"label": "YOA", "format": integer_format()}
    ),
    "years_to_inception": hx.Int(
        mode="input", default=None, optionality="optional",
        async_input=["rarc_task"],
        async_output=[{"task": task, "reset": False} for task in ["show_airlines_task", "show_ga_task", "start_renewal_task"]], 
        view={"label": "Years to\nInception", "format": integer_format(), "group": "Inflation"}
    )
}

expe_tasks = [{"task": task, "reset": False} for task in ["show_airlines_task", "show_ga_task", "fill_historic_premium_task", "start_renewal_task"]]

for k, v in coverages_dict.items():
    k = k[:4]
    claims_dict[f"{k}_attr_claims"] = hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=expe_tasks, view={"label": "Incurred\nAttritional\nClaims\n(100% Share)", "format": thousands_format(), "group": v["label"]})
    claims_dict[f"{k}_large_losses"] = hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=expe_tasks, view={"label": "Incurred\nLarge\nLosses\n(100% Share)", "format": thousands_format(), "group": v["label"]})
    claims_dict[f"{k}_gross_premium"] = hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=expe_tasks, view={"label": "Gross\nPremium", "format": thousands_format(), "group": v["label"]})
    claims_dict[f"{k}_exposure_adj"] = hx.Float(mode="input", default=1, optionality="optional", async_input=["rarc_task"], async_output=[{"task": task, "reset": False} for task in ["show_airlines_task", "show_ga_task", "start_renewal_task"]], view={"label": "Exposure\nAdjustment", "format": {**percent_format(1), "trimMantissa": True}, "group": v["label"]})
    claims_dict[f"{k}_rate_change"] = hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=[{"task": task, "reset": False} for task in ["show_airlines_task", "show_ga_task", "start_renewal_task"]], view={"label": "Rate\nChange", "format": {**percent_format(1), "trimMantissa": True}, "group": v["label"]})
    claims_dict[f"{k}_as_if_premium"] = hx.Float(mode="output", view={"label": "As-if\nPremium", "format": thousands_format(), "group": v["label"]})
    claims_dict[f"{k}_pct_developed"] = hx.Float(mode="output", view={"label": "% Developed", "format": percent_format(1), "group": v["label"]})
    claims_dict[f"{k}_ult_attr_claims"] = hx.Float(mode="output", view={"label": "Ultimate\nAttritional\nClaims", "format": thousands_format(), "group": v["label"]})
    claims_dict[f"{k}_ulr"] = hx.Float(mode="output", view={"label": "ULR", "format": percent_format(1), "group": v["label"]})
    claims_dict[f"{k}_portfolio_rc"] = hx.Float(mode="output", view={"label": v["label"][:4], "format": percent_format(1), "group": "Portfolio Rate Change"})
    claims_dict[f"{k}_rc_to_use"] = hx.Float(mode="output", view={"label": v["label"][:4], "format": percent_format(1), "group": "Rate Change to use", "info": "Defaulting to 100% where rate change not present or given."})
    claims_dict[f"{k}_cumul_rc"] = hx.Float(mode="output", view={"label": v["label"][:4], "format": percent_format(1), "group": "Cumulative Rate Change"})
    claims_dict[f"{k}_inflation"] = hx.Float(mode="output", view={"label": v["label"][:4], "format": percent_format(1), "group": "Inflation"})

expe_rating_summary_dict = {
    "max_insured_loss": hx.Float(mode="output", view={"label": "Max Insured Loss Possible", "format": thousands_format()}),
    "implied_lllr": hx.Float(mode="output", view={"label": "Implied LL Loss Ratio", "format": percent_format(1)}),
    "implied_rp": hx.Float(mode="output", view={"label": "Implied RP of such a loss", "format": {**thousands_format(2), "trimMantissa": True}}),
    "large_loss_loading": hx.Float(mode="output", view={"label": "Average LL Loading to apply", "format": percent_format(1)}),
    "ll_loading_label": hx.Str(mode="input", async_output=[{"task": "start_renewal_task", "reset": False}], default="Large Loss Loading"),
    "actual_no_of_years": hx.Float(mode="output", view={"label": "Number of years claims experience", "format": integer_format()}),
    "quoted_premium": hx.Float(mode="output", view={"label": "Gross Quoted Premium", "format": thousands_format()}),
    "implied_attr_lr": hx.Float(mode="output", view={"label": "Implied Expected Attritional LR", "format": percent_format(1)}),
    "expected_lr": hx.Float(mode="output", view={"label": "Expected Loss Ratio", "format": percent_format(1)}),
    "expected_claims": hx.Float(mode="output", view={"label": "Expected Claims", "format": thousands_format()}),
    "expected_claims_label": hx.Str(mode="output"),
    "credibility": hx.Float(mode="output", view={"label": "Credibility", "format": percent_format(1)}),
}


