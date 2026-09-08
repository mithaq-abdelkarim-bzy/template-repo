import hx
import pandas as pd
import numpy as np
from operator import itemgetter
import traceback
from datetime import datetime, timedelta
from calendar import isleap
from typing import List
from algorithms.data_schema.sch_rater_defined import all_coverages_dict
from algorithms import parameter_tables_schema as params

# Pull in technical premium parameters from user library 
tp_params_df = params.tp_parameters.df()

# Define function to look up bp class
def tp_lookup(vbl, bp_class, tp_year):
    out = tp_params_df[
        (tp_params_df["business_plan_class"] == bp_class)
        & (tp_params_df["year"] == tp_year)
    ][vbl].iloc[0]
    return out

def title_rc(string):
    string = string.replace("_and_"," & ")
    string = string.replace("_"," ")
    string = string.title()

    return (string)

# Fastest way to convert a hx_list into a pandas dataframe
def pd_df_from_hx_list(hx_list):
    '''
    Turns a hx.List() into a pandas DataFrame in a vectorised way, without having to specify or loop through the keys/column names in the hx.List().
    '''

    col_designation = {x[0]: getattr(x[1], "is_overridden", None) is not None for x in hx_list[0]}
    override_cols = [k for k, v in col_designation.items() if v]
    normal_cols = [x for x in col_designation if x not in override_cols]

    list_representation = [
        {column: getattr(row, column) for column in normal_cols}
        | 
        {f"{column}_calculated": getattr(row, column).calculated for column in override_cols} 
        | 
        {f"{column}_override": getattr(row, column).override for column in override_cols} 
        for row in hx_list
    ]

    df = pd.DataFrame(list_representation)

    return df

# Fastest way to write pandas back to hxd
# Caveat is it requires manual specification of columns to write
def write_pd_to_hxd(df, list_node, output_cols_to_write, override_cols_to_write = None):
    dictionary = df.to_dict()
    
    for i in range(df.shape[0]):
        for col in output_cols_to_write:
            setattr(list_node[i], col, dictionary[col][i])
        for col in override_cols_to_write:
            #only need to bring back calculated column as overrides will work as normal
            setattr(getattr(list_node[i], col),"calculated",dictionary[col + "_calculated"][i])

# Calculate difference between dates
def year_diff(start_date, end_date, for_term):
    """
    Calculate the difference in years between two dates, optionally adjusting for an inclusive term (e.g. a policy term)

    Parameters:
        start_date (datetime.date): The start date.
        end_date (datetime.date): The end date, adjusted by one day if for_term is True.
        for_term (bool): Adjust end date by one day if True.

    Returns:
        float: The year difference, considering leap years.
    """
    if for_term:
        end_date += timedelta(days=1)

    diffyears = end_date.year - start_date.year
    difference  = end_date - start_date.replace(end_date.year)
    days_in_year = isleap(end_date.year) and 366 or 365
    difference_in_years = diffyears + (difference.days + difference.seconds/86400.0)/days_in_year

    return difference_in_years

# Create variables to avoid looping when accessing layers and coverages
def one_layer(hxd):
    """
    Returns: layer, cvg
    Use these variables to directly access the hxd without looping
    """

    layer = hxd.cds.layers[0]
    cvg = layer.coverages

    return layer, cvg

# Handle division by 0
def ratio(a, b, if_undefined=0):
    """
    Handles division by 0 by returning 0 instead of an error.
    Can change 'if_undefined' parameter to return a different number.
    """
    # Check if the inputs are scalar values
    if np.isscalar(a) and np.isscalar(b):
        return if_undefined if b == 0 else a / b

    # Convert inputs to pandas Series if they aren't already
    a = pd.Series(a)
    b = pd.Series(b)
    
    # Calculate the ratio, applying if_undefined where b is zero
    result = a.where(b != 0, if_undefined) / b.where(b != 0, 1)
    
    return result
    

# Helper function to perform the lookup
def _perform_lookup(df, filter_condition, return_col, if_not_found):
    value = if_not_found  # Set the default return value
    try:
        value = df.loc[filter_condition, return_col].iloc[0]
    # Try to return helpful message for debugging
    except Exception as e:
        try:
            # Extract the entire traceback stack with the file name and line number where error occured
            tb_stack = traceback.extract_stack()
            caller_info = tb_stack[-3] # Typically, the index of the caller in the stack
            file_name = caller_info.filename
            line_number = caller_info.lineno
            print(f"Error during lookup: {e} in file {file_name}, line {line_number}. Defaulting value to {if_not_found}.")
        except:
            print(f"Error during lookup: {e}. Defaulting value to {if_not_found}.")

    return value

# Function for exact match lookup, handles errors by returning 1
def look_up(lookup_value, lookup_col, return_col, df, if_not_found=1):
    if not isinstance(df, pd.DataFrame):
        print(f"Warning: Expected 'df' to be a pandas DataFrame, but got {type(df).__name__}.")
        return if_not_found
    filter_condition = df[lookup_col] == lookup_value
    return _perform_lookup(df, filter_condition, return_col, if_not_found)

# Function for range-based lookup, handles errors by returning 1
def look_up_with_bounds(lookup_value, lower_bound_col, upper_bound_col, return_col, df, if_not_found=1):
    if not isinstance(df, pd.DataFrame):
        print(f"Warning: Expected 'df' to be a pandas DataFrame, but got {type(df).__name__}.")
        return if_not_found
    filter_condition = (df[lower_bound_col] <= lookup_value) & (df[upper_bound_col] >= lookup_value)
    return _perform_lookup(df, filter_condition, return_col, if_not_found)


# Apply look-up function iteratively when having consistent names in data schema and params
def iterate_lookups(params: object, tbl_prefix: str, parent: object,  children: list) -> None:

    for node in children:
        lookup_value = getattr(parent, node)
        lookup_col = node
        return_col = "factor"

        try: 
            df = getattr(params, tbl_prefix + node)
        except:
            df = getattr(params, "ca_" + node) # Default to Cargo param table if cover-specific table not found
            print (f"Param table {tbl_prefix}{node} does not exist. Using ca_{node}.")

        value = look_up(lookup_value, lookup_col, return_col, df)

        try:
            setattr(parent, node + "_factor", value)
        except:
            override_node = getattr(parent, node + "_factor")
            setattr(override_node, "calculated", value)

# Convert to USD - 2023 param table
def usd_2023(value, ccy, ccy_table=hx.params.ca_currency):
    fx_rate = look_up(ccy, "currency", "rate", ccy_table)
    value_in_usd = ratio(value, fx_rate)
    return value_in_usd

def usd(value, ccy, ccy_table=params.fx_rates.df()):
    fx_rate = look_up(ccy, "ccy", "fx_rate", ccy_table)
    value_in_usd = ratio(value, fx_rate)
    return value_in_usd

# Apply formula to excess amount and calculate factor
def calculate_xs_factor(xs, ccy, xs_table):
    if not xs or xs < 0:
        bounded_factor = 1
        return bounded_factor

    xs_in_usd = usd(xs, ccy)
    
    b = look_up("b", "parameter", "value", xs_table)
    c = look_up("c", "parameter", "value", xs_table)

    factor = b * np.log(xs_in_usd) + c
    bounded_factor = min(factor, 1)

    return bounded_factor

# Calculate actual premium as % of technical premium, based on actual input
def calculate_pct_of_technical(parent: object) -> None:
    actual_rate = getattr(parent, "actual_rate")
    quoted_premium = getattr(parent, "quoted_premium")
    technical_rate = getattr(parent, "technical_rate")
    technical_premium = getattr(parent, "technical_premium")

    if actual_rate and quoted_premium is None:
        setattr(parent, "pct_of_technical", ratio(actual_rate, technical_rate))
    if actual_rate is None and quoted_premium:
        setattr(parent, "pct_of_technical", ratio(quoted_premium, technical_premium))

# Obtain node from data_schema() dictionary through pathing
def get_node(dictionary, node_path):
    """
    Retrieve value from nested dictionary using a path string separated by slashes.
    Can be used to retrieve specific properties of data schema nodes when passing the data schema as a dictionary.

    :param dictionary: The dictionary to search into.
    :param node_path: A string representing the path to the target value, with each key separated by slashes.
    :return: The value found at the nested path, or raises AttributeError if any key is missing.
    """

    keys = node_path.split("/")  # Split the single string by slashes to get the list of keys
    current_level = dictionary

    for key in keys:
        try:
            current_level = current_level[key]
        except KeyError:
            raise AttributeError(f"Node '{key}' does not exist in data schema.")
    return current_level

# Iterate through list of fields to validate
def validate_empty_fields(
        validation_nodes: List[str],
        structure_path: str,
        hxd_structure: object,
        cover_name: str,
        include_zero_fields: bool = True,
    ) -> bool:

    are_all_valid = True

    for node in validation_nodes:
        hxd_node = getattr(hxd_structure, node)
        node_path = structure_path + f"/{node}"
        label = get_node(all_coverages_dict, node_path).view.get("label")
        
        # Check if the node is empty
        if hxd_node is None:
            message = f"{label} in {cover_name} cannot be empty."
            hx.errors.validation(message)
            are_all_valid = False

        # Check if the node is a number and <= 0
        elif include_zero_fields and isinstance(hxd_node, (int, float)) and hxd_node <= 0:
            message = f"{label} in {cover_name} must be greater than zero."
            hx.errors.validation(message)
            are_all_valid = False

    return are_all_valid