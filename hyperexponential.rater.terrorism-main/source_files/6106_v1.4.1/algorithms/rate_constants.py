from algorithms import parameter_tables_schema as params

def get_unique(df, column_name):
    # Remove duplicates, sort, and return as a list
    return sorted(df[column_name].drop_duplicates().tolist())

# If changing the max_layers below, you must also update in vw_constants to the same number
max_layers   = 1

# Rating constants
benchmark_lr = 0.7
bi_weighting = 0.3
cbi_load     = 0.05

# Other constants
excel_password = "Safe"

# Get dropdown options from param tables
ccy_options  = get_unique(params.fx_rates.df(), "ccy")
