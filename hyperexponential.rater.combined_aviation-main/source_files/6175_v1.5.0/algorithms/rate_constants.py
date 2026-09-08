import hx
from algorithms import parameter_tables_schema as params

def get_unique(df, column_name):
    # Remove duplicates, sort, and return as a list
    return sorted(df[column_name].drop_duplicates().tolist())

# If changing the max_layers below, you must also update in vw_constants to the same number
max_layers = 1
benchmark_lr = 0.7
liab_min_rate = 0.0002
excel_password = "giraffe"

# Get dropdown options from param tables
usage_options = get_unique(hx.params.al_UsageMapping, "AircraftUsageMapped")
primary_usage_options = get_unique(hx.params.al_UsageMapping, "AircraftUsage")
market_class_options = get_unique(hx.params.al_HullFreqClass, "Class")
region_options = get_unique(hx.params.OperatorCountryList, "Region Airlines")

# FS 27/08/2024: Aircraft class options updated to include two options for PistonHeli and BusinessJet
aircraft_class_options = ["PistonHeli1", "PistonHeli2", "PistonFixed1", "PistonFixed2", "TurbineHeli1", "TurbineHeli2", "Turboprops1", "Turboprops2", "BusinessJet1", "BusinessJet2"]
ga_region_options = get_unique(hx.params.OperatorCountryList, "Region GA")
ga_use_options = get_unique(hx.params.ga_MappedUsageType, "GA Mapped Primary Usage")
# FS 02/09/2025: Additional Use Option Added
ga_use_options.append("Training - Experienced")

ccy_options = get_unique(params.fx_rates.df(), "ccy")
