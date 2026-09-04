import hx
import pandas as pd
import numpy as np
from operator import itemgetter, attrgetter
from datetime import timedelta, datetime
from calendar import isleap
from scipy.interpolate import interp2d
from collections import defaultdict


def rates_display(hxd):
   
    # Rate display - sector / sub sector
    subsector_df = hx.params.sector_subsector_rates
    sector_df = hx.params.sector_rates
    subsector_df = subsector_df.merge(sector_df, how="left", on="Sector")
    subsector_df["BaseRate"] = subsector_df["Relativity"] * subsector_df["Rate"]
    subsector_display_df = subsector_df[["Sector", "SubSector", "BaseRate", "Relativity"]].sort_values(["Sector", "SubSector"])

    hxd.subsector_rates_display = subsector_display_df.to_dict(orient="records")

    # Rate display - city risk
    city_rates_df = hx.params.city_rates_display.sort_values(["State", "City"])
    hxd.city_rates_display = city_rates_df.to_dict(orient="records")



def title_rc(string):
    string = string.replace("_and_"," & ")
    string = string.replace("_"," ")
    string = string.title()

    return (string)



# Fastest way to convert a hx_list into a pandas dataframe
def pd_df_from_hx_list(hx_list):
    '''
    Turns a hx.List() into a pandas DataFrame in a vectorised way,
    without having to specify or loop through the keys/column names in the hx.List().
    Also unpacks nested structures and extracts selected values from override fields.

    Updated to handle the offline hxd structure.

    '''
    df = pd.DataFrame(hx_list)

    # 'df' is a pandas DataFrame where each value is a tuple of (hxd_item_name, hxd_item_value).
    # First we pick out the first row and use .str to pick out a list of hxd_item_name to assign
    # as our DataFrame column names. Then loop through each column (i.e. each hx_item_name) and
    # use the itemgetter() function to pick out the hxd_item_value only.
    desired_columns = df.iloc[0].str[0]
    for col in df.columns:
        df[col] = df[col].apply(itemgetter(1))
    df.columns = desired_columns

    # Looking only at the top row to keep processing time minimal, this finds all
    # columns that have not returned values (i.e. still hold an object with a hx node type).
    # When these are found, all available attributes are stored against the column
    # name to enable mode identification below
    top_row = df.iloc[0]
    nested_items = {k: dir(v) for k, v in top_row.items() if "hx_internal" in str(type(v)) or "transient_hxd" in str(type(v))}

    # Loops through all of the found items and unpacks them
    while nested_items:
        for col in nested_items:
            # As the mode is not inferrable from the object type, use the list of available
            # attributes determined above to determine if the object is an override or not
            if nested_items[col] == ['calculated', 'is_overridden', 'override', 'selected']:
                # This is set up to simply import the selected property of override nodes
                # but can be easily modified here to bring in any other property, or multiple
                # properties
                df[col] = df[col].apply(attrgetter("selected"))
            else:
                # If the item is not an override, unpack all of it's children to the DataFrame
                for child in nested_items[col]:
                    df[f"{col}/{child}"] = df[col].apply(attrgetter(child))
                df = df.drop(col, axis=1)

        # Finally, check to see if there are still items that need to be unpacked
        # (i.e. if there were multiple layers of nested structures)
        top_row = df.iloc[0]
        nested_items = {k: dir(v) for k, v in top_row.items() if "hx_internal" in str(type(v)) or "transient_hxd" in str(type(v))}

    return df



# Fastest way to write pandas back to hxd
# Caveat is it requires manual specification of columns to write
def write_pd_to_hxd(df, list_node, output_cols_to_write, override_cols_to_write = None):
    dictionary = df.to_dict()
    for i in range(df.shape[0]):
        for col in output_cols_to_write:
            setattr(list_node[i], col, dictionary[col][i])
        if override_cols_to_write:
            for col in override_cols_to_write:
                #only need to bring back calculated column as overrides will work as normal
                setattr(getattr(list_node[i], col),"calculated",dictionary[col + "_calculated"][i])



def df_to_dict(df, from_col, to_col=None, keep_duplicates=None):
    """
    Parameter tables are accessed as Pandas dataframes.
    When we need to look up values in a parameter table from inside a loop, it is more efficient for us to convert the parameter table
    from a Pandas dataframe into a native Python dict, so we can look up directly from a key to a value or values.
    This helper function takes a Pandas dataframe, and returns a dict containing the table data

    Args:
    from_col: single string containing column name to use as a key
    to_col: a single string, or a list of strings, containing columns to return as values
    keep_duplicates: "first" or "last", specifies which row to keep if from_col column contains duplicate values
    """

    # Check if we have duplicates, and don't allow unless we've said what to do with them
    df_indexed = df.set_index(from_col)
    idx = df_indexed.index
    if any(idx.duplicated()):
        if keep_duplicates == "first" or keep_duplicates == "last":
            df_indexed = df_indexed[idx.duplicated(keep_duplicates) == False]
        else:
            dupe_values = idx[idx.duplicated()].values
            raise ValueError("DataFrame contains duplicate values in column '" + str(from_col) + "': " + str(dupe_values))

    if to_col is None:
        # No to_col specified
        # Return a dict containing:
        #   key: value from column from_col
        #   value: dict containing the other column names/values from the key row
        return df_indexed.to_dict("index")

    if isinstance(to_col, str):
        # to_col is a single column
        # Return a dict containing:
        #   key: value from column from_col
        #   value: value from column to_col
        return df_indexed[to_col].to_dict()

    if isinstance(to_col, list):
        # to_col is a list of column names
        # Return a dict containing
        #   key: value from column from_col
        #   value: dict containing column names/values for the specified columns in to_col
        return df_indexed[to_col].to_dict("index")

    return None



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

    # Handle leap start date
    if start_date.month == 2 and start_date.day == 29:
        start_date += timedelta(days=+1)

    difference  = end_date - start_date.replace(end_date.year)
    days_in_year = 366 if isleap(end_date.year) else 365
    difference_in_years = diffyears + (difference.days + difference.seconds / 86400.0) / days_in_year

    return difference_in_years


def policy_term(inception_date: datetime, expiry_date: datetime):
    d1 = inception_date
    d2 = expiry_date
    
    if d1 >= d2:
        return 0
    
    if d1.month == d2.month and d1.day == d2.day:
        return d2.year - d1.year
    
    d1_alt = d1 - timedelta(days=1)
    if d1_alt.month == d2.month and d1_alt.day == d2.day:
        return d2.year - d1_alt.year
        
    # Calculate the fractional difference in years
    days_diff = (d2 - d1).days + 1
    year_diff = days_diff / 365.25
    return year_diff



# Handle division by 0
def ratio(a, b, if_undefined=0):
    """
    Handles division by 0 or None by returning 'if_undefined' instead of an error.
    Can change 'if_undefined' parameter to return a different number.
    """
    # Convert inputs to numpy arrays with dtype=float to handle None as nan
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    
    # Replace nan (resulting from None) with 0
    a = np.nan_to_num(a, nan=0.0)
    b = np.nan_to_num(b, nan=0.0)
    
    # Perform the division with protection against division by zero
    c = np.where(b == 0, if_undefined, a / b)
    return c

def safe_sumproduct(array1, array2, if_undefined=0):
    """
    Computes the dot product of two arrays, handling None and np.nan values.
    Replaces None or np.nan with zeros before computation.
    """
    # Check for None inputs
    if array1 is None or array2 is None:
        return if_undefined
    
    # Convert to numpy arrays with dtype=float
    array1 = np.array(array1, dtype=float)
    array2 = np.array(array2, dtype=float)
    
    # Replace np.nan with zeros
    array1 = np.nan_to_num(array1, nan=0.0)
    array2 = np.nan_to_num(array2, nan=0.0)
    
    # Perform the dot product
    result = np.dot(array1, array2)
    return result

def weighted_average(array, weights, if_undefined=0):
    """
    Computes the average of array1 weighted by weights, handling None and np.nan values.
    """
    # Convert to numpy arrays with dtype=float
    array = np.array(array, dtype=float)
    weights = np.array(weights, dtype=float)
    
    # Replace np.nan with zeros
    array = np.nan_to_num(array, nan=0.0)
    weights = np.nan_to_num(weights, nan=0.0)

    sumprod = safe_sumproduct(array1=array, array2=weights, if_undefined=if_undefined)
    result = sumprod / weights.sum()
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
    '''
    Performs ranged based lookup. Note lower bound is inclusive, upper bound is exclusive. Bounds must not overlap.
    '''
    if not isinstance(df, pd.DataFrame):
        print(f"Warning: Expected 'df' to be a pandas DataFrame, but got {type(df).__name__}.")
        return if_not_found
    filter_condition = (df[lower_bound_col] <= lookup_value) & (df[upper_bound_col] > lookup_value)
    return _perform_lookup(df, filter_condition, return_col, if_not_found)



def interp2d_agg_factors(agg_factors_fn, x_loc, y_lim, agg_ratio_fn):

    '''
    Extracts the aggregate limit factor from a two-dimensional array of limit vs # of locations. 
    The agg factors table is first filtered by the ratio of the agg limit to limit.
    '''

    filtered_tbl = agg_factors_fn[agg_factors_fn["AggLimitRatio"] == agg_ratio_fn]
    filtered_tbl = filtered_tbl.drop("AggLimitRatio", axis="columns")

    x_coords = filtered_tbl.columns[1:]  # Assumes the x_coords are in the column names starting from the third column
    y_coords = filtered_tbl.iloc[:, 0]  # Second column, excluding the first element

    x_coords = x_coords.astype(float).values
    y_coords = y_coords.astype(float).values

    z_values = filtered_tbl.iloc[:, 1:].values  # Rest of table
    
    # Create the interpolation function
    interp_func = interp2d(x_coords, y_coords, z_values, kind='linear')
    
    # Interpolate at the given (x, y)
    return interp_func(x_loc, y_lim)[0]



# Check if data exists
def data_exists(df):
    '''
    Takes an hxd list and checks if it contains any data. Outputs true or false.
    '''   
    pd_df = pd_df_from_hx_list(df).dropna(how="all")
    has_data = pd_df.shape[0] > 0
    return has_data



def extract_subkey_values(data_dict, subkey):
    """
    Extract values for a specific subkey from a nested dictionary.
   
    Parameters:
    data_dict (dict): The original dictionary with multiple subkeys per key.
    subkey (str): The subkey whose values you want to extract.

    Returns:
    dict: A dictionary with the keys from the original dictionary and values from the specified subkey.
    """
    return {k: v[subkey] for k, v in data_dict.items() if subkey in v}




# Calculate reverse cumulative product for rate change an inflation
def calc_reverse_product(lst_input):
    indx = []
    cum = 1
    for i in reversed(lst_input):
        cum *= i
        indx.append(cum)
    indx.pop()
    indx.reverse()
    return indx



# Convert df to a nested list for use in the rate change calcs
def df_to_nested_list(df):
    nested_list = []
    # Iterate over each row in the df
    for row in df.itertuples(index=False):
        nested_dict = defaultdict(dict) 
        # Iterate over each column 
        for col, value in zip(df.columns, row):
            # Split the col name by '/' for nested keys
            keys = col.split('/')
            temp = nested_dict
            # Iterate over all keys except the last one to build the nested structure
            for key in keys[:-1]:
                temp = temp[key]  # Move deeper into the defaultdict
            # Set the value for the final key
            temp[keys[-1]] = value
        # Append the fully constructed dictionary to the list
        nested_list.append(dict(nested_dict))  # Convert defaultdict back to a regular dict
    return nested_list



def transient_list_from_hx_list(hx_list):
    '''
    Turns a hx.List() into a nested list for use with the transient hxd. Also unpacks nested structures and extracts selected values from override fields.
    '''
    def is_basic_type(value):
        return isinstance(value, (str, int, float, bool, type(None)))

    def is_override(value):
        attrs = dir(value)
        override_attrs = ['calculated', 'is_overridden', 'override', 'selected']
        return set(attrs) == set(override_attrs)

    def is_nested_item(value):
        value_type = str(type(value))
        return ("hx_internal" in value_type) or ("_hxd" in value_type) or ("transient_hxd" in value_type)

    def hx_item_to_dict(item):
        if is_basic_type(item):
            return item
        elif is_override(item):
            return getattr(item, 'selected', None)
        elif is_nested_item(item):
            result = {}
            for attr in dir(item):
                if not attr.startswith('_') and not attr.endswith('_'):
                    value = getattr(item, attr)
                    result[attr] = hx_item_to_dict(value)
            return result
        elif isinstance(item, (list, tuple)):
            return [hx_item_to_dict(sub_item) for sub_item in item]
        else:
            return str(item)  # Fallback for unexpected types

    nested_list = [hx_item_to_dict(hx_item) for hx_item in hx_list]
    return nested_list




def calculate_percentage_change(input_list):
    percentage_changes = []
    for i in range(1, len(input_list)):
        prev = input_list[i - 1]
        curr = input_list[i]
        change = curr / prev - 1 if prev !=0 else -1
        percentage_changes.append(change)
    return percentage_changes



def format_millions(value, ccy):
    # Ensure the value is in millions
    ccy_f = '$' if ccy == 'USD' else ccy+' '
    
    if not value:
        return None

    if value < 500000:
        formatted_value = f"{ccy_f}{value / 1000:.1f}k"
        # Remove unnecessary decimal if it's .0
        if formatted_value.endswith(".0k"):
            formatted_value = formatted_value.replace(".0k", "k")
    else:           
        formatted_value = f"{ccy_f}{value / 1000000:.1f}m"
        # Remove unnecessary decimal if it's .0
        if formatted_value.endswith(".0m"):
            formatted_value = formatted_value.replace(".0m", "m")
    
    return formatted_value



def tp_lookup(vbl, bp_class, tp_params_df, tp_year):
    parameter = tp_params_df[
        (tp_params_df['business_plan_class'] == bp_class)
        & (tp_params_df['year'] == tp_year)
    ][vbl].iloc[0]
    return parameter




