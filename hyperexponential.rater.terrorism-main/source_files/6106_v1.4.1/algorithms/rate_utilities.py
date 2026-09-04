import hx
import functools
import pandas as pd
import numpy as np
import uuid
from operator import itemgetter, attrgetter
from collections import Counter
import traceback
from datetime import date, datetime, timedelta
from calendar import isleap
from typing import List
from algorithms.data_schema.sch_rater_defined import all_coverages_dict
from algorithms import parameter_tables_schema as params


def title_rc(string):
    string = string.replace("_and_"," & ")
    string = string.replace("_"," ")
    string = string.title()

    return (string)

def date_to_string(date_obj: date) -> str:
    if date_obj is None:
        return date_obj
    return date_obj.strftime("%Y-%m-%d")

# Linear interpolation
def linear_interp(x_series: pd.Series, y_series: pd.Series, x_value):
    """
    Perform linear interpolation to estimate y_values for given x_values
    using x_series and y_series.

    Parameters:
    - x_series: pd.Series of x values (must be sorted in ascending order)
    - y_series: pd.Series of corresponding y values
    - x_value: Either a float or a pd.Series of x values to interpolate

    Returns:
    - A single interpolated float if x_value is a float
    - A pd.Series of interpolated values if x_value is a pd.Series
    """
    x_series = x_series.values  # Convert to numpy array for efficiency
    y_series = y_series.values  # Convert to numpy array for efficiency

    # Convert single float x_value to array if necessary
    is_scalar = np.isscalar(x_value)
    x_value = np.array([x_value]) if is_scalar else x_value.values

    # Handle out-of-range values (extrapolate as nearest boundary values)
    x_value = np.clip(x_value, x_series[0], x_series[-1])

    # Get indices where x_value falls between x_series values
    indices = np.searchsorted(x_series, x_value, side="right") - 1

    # Get corresponding x1, x2, y1, y2 values
    x1, x2 = x_series[indices], x_series[indices + 1]
    y1, y2 = y_series[indices], y_series[indices + 1]

    # Compute interpolated y values using vectorized operations
    y_value = y1 + (y2 - y1) * (x_value - x1) / (x2 - x1)

    return y_value[0] if is_scalar else pd.Series(y_value, index=pd.Index(x_value))

# Functions for MBBEFD curves
def mbbefd(b, g, x):
    # Ensure b and g are floats
    b = float(b)
    g = float(g)
    
    # Convert x to a numeric pandas Series if it is not already
    scalar_input = False
    if not isinstance(x, pd.Series):
        x = pd.Series([x])
        scalar_input = True
    # Ensure x is of float type
    x = pd.to_numeric(x, errors='coerce')

    # Initialize result Series
    result = pd.Series(index=x.index, dtype=float)

    # Apply conditions
    if g == 1:
        result[:] = x
    elif b == 1 and g > 1:
        result[:] = np.log(1 + (g - 1) * x) / np.log(g)
    elif b * g == 1 and g > 1:
        result[:] = (1 - b ** x) / (1 - b)
    elif b > 0 and b != 1 and b * g != 1 and g > 1:
        # Using elementwise operations on Series x with scalars b and g
        # With b and g explicitly cast to float and x as numeric, np.log should work properly
        result[:] = np.log(((g - 1) * b + (1 - g * b) * (b ** x)) / (1 - b)) / np.log(g * b)
    else:
        result[:] = -1

    # Return scalar if input was scalar
    if scalar_input:
        return result.iloc[0]
    return result



# Fastest way to convert a hx_list into a pandas dataframe
def pd_df_from_hx_list(hx_list, splitter="."):
    '''
    Turns a hx.List() into a pandas DataFrame in a vectorised way,
    without having to specify or loop through the keys/column names in the hx.List().
    Also unpacks nested structures and extracts selected values from override fields.
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
    nested_items = {k: dir(v) for k, v in top_row.items() if "hx_internal" in str(type(v))}

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
                    df[f"{col}{splitter}{child}"] = df[col].apply(attrgetter(child))
                df = df.drop(col, axis=1)

        # Finally, check to see if there are still items that need to be unpacked
        # (i.e. if there were multiple layers of nested structures)
        top_row = df.iloc[0]
        nested_items = {k: dir(v) for k, v in top_row.items() if "hx_internal" in str(type(v))}

    return df

# Fastest way to write pandas back to hxd
# Caveat is it requires manual specification of columns to write
def write_pd_to_hxd(df, list_node, output_cols_to_write, override_cols_to_write=[], splitter=".", replace_nan=False):
    if replace_nan:
        # Convert the DataFrame to object type and replace NaN with None
        df = df.astype(object).where(pd.notnull(df), None)

    dictionary = df.to_dict()

    def set_nested_attr(obj, attr_path, value):
        """Sets the value of a nested attribute given by attr_path on obj."""
        attrs = attr_path.split(splitter)
        for attr in attrs[:-1]:
            obj = getattr(obj, attr)
        setattr(obj, attrs[-1], value)

    def set_nested_override_calculated(obj, attr_path, value):
        """Sets the 'calculated' attribute on a nested override object."""
        attrs = attr_path.split(splitter)
        for attr in attrs:
            obj = getattr(obj, attr)
        setattr(obj, "calculated", value)

    for i in range(df.shape[0]):
        for col in output_cols_to_write:
            value = dictionary[col][i]
            set_nested_attr(list_node[i], col, value)
        if override_cols_to_write:
            for col in override_cols_to_write:
                value = dictionary[col][i]
                set_nested_override_calculated(list_node[i], col, value)

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

# Calculates the policy term rating factor
def policy_term(inception_date, expiry_date, return_days=False):
    """
    Calculates the policy term rating factor for either single datetime values or pandas Series.
    For Series inputs, operations are vectorized.

    This function returns 1.0 both if the expiry date is exclusive 
    (e.g. 06/12/2024 - 06/12/2025), the US method,
    or if the expiry date is inclusive (e.g. 06/12/2024 - 05/12/2025).

    Parameters:
        inception_date: datetime or pd.Series of datetime
        expiry_date: datetime or pd.Series of datetime

    Returns:
        float or pd.Series of float: The year difference, considering leap years.
    """
    
    # Check if either input is a pandas Series.
    is_series = isinstance(inception_date, pd.Series) or isinstance(expiry_date, pd.Series)
    
    if not is_series:
        # Scalar (single datetime) handling.
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

        if return_days:
            return year_diff, days_diff

        return year_diff
    
    else:
        # Ensure both inputs are pandas Series
        # If one input is a scalar, convert it to a Series of the same length as the other
        if not isinstance(inception_date, pd.Series):
            inception_date = pd.Series([inception_date] * len(expiry_date), index=expiry_date.index)
        if not isinstance(expiry_date, pd.Series):
            expiry_date = pd.Series([expiry_date] * len(inception_date), index=inception_date.index)

        d1 = inception_date
        d2 = expiry_date

        # Initialize the result with NaNs
        result = pd.Series(np.nan, index=d1.index)

        # Condition where inception date is not before expiry date
        condition_invalid = d1 >= d2
        result[condition_invalid] = 0

        # Check for same month and day condition
        same_md = (d1.dt.month == d2.dt.month) & (d1.dt.day == d2.dt.day)
        result[same_md & ~condition_invalid] = d2.dt.year[same_md & ~condition_invalid] - d1.dt.year[same_md & ~condition_invalid]

        # Check for the alternative condition with day adjustment
        d1_alt = d1 - pd.Timedelta(days=1)
        alt_same_md = (d1_alt.dt.month == d2.dt.month) & (d1_alt.dt.day == d2.dt.day) & result.isna()
        result[alt_same_md] = d2.dt.year[alt_same_md] - d1_alt.dt.year[alt_same_md]

        # For remaining NaNs, calculate the fractional year difference
        remaining = result.isna() & ~condition_invalid
        if remaining.any():
            days_diff = (d2 - d1).dt.days + 1
            result[remaining] = days_diff[remaining] / 365.25

        return result

# Handle division by 0
def ratio(a, b, if_undefined=0):
    # Convert inputs to pandas Series if they are not scalars
    a_series = pd.Series(a) if not np.isscalar(a) else pd.Series([a])
    b_series = pd.Series(b) if not np.isscalar(b) else pd.Series([b])
    
    # Convert to numeric; non-numeric values (including None) become NaN
    a_series = pd.to_numeric(a_series, errors='coerce')
    b_series = pd.to_numeric(b_series, errors='coerce')
    
    # Replace zeros in the denominator with NaN, perform division, then fill NaNs with if_undefined.
    result = a_series.div(b_series.replace(0, np.nan)).fillna(if_undefined)
    
    # If the original inputs were scalars, return a scalar
    if a_series.size == 1 and b_series.size == 1:
        return result.iloc[0]
    return result

# Create variables to avoid looping when accessing layers and coverages
def one_layer(hxd):
    """
    Returns: layer, cvg
    Use these variables to directly access the hxd without looping
    """

    layer = hxd.cds.layers[0]
    cvg = layer.coverages

    return layer, cvg

# Easier sum with the hxd object
def sum_(hxd_node, hxd_list):
    sum_list = [getattr(item, hxd_node) for item in hxd_list]
    result = sum(sum_list)
    return result

# Quickly get list from hxd object
def array(hxd_node, hxd_list):
    array = [getattr(item, hxd_node) for item in hxd_list]
    return np.asarray(array)
    
# Convert to USD
def usd(value, ccy, ccy_table=params.fx_rates.df(), lookup_type="single"):
    fx_rate = look_up(ccy, "ccy", "fx_rate", ccy_table, if_not_found=1, lookup_type=lookup_type)
    value_in_usd = ratio(value, fx_rate)
    return value_in_usd

# Convert to currency currency from USD
def to_ccy(value_in_usd, ccy, ccy_table=params.fx_rates.df(), lookup_type="single"):
    """Converts from USD value to current currency"""
    fx_rate = look_up(ccy, "ccy", "fx_rate", ccy_table, if_not_found=1, lookup_type=lookup_type)
    value = value_in_usd * fx_rate
    return value

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
            message = f"'{label}' in {cover_name} cannot be empty."
            hx.errors.validation(message)
            are_all_valid = False

        # Check if the node is a number and <= 0
        elif include_zero_fields and isinstance(hxd_node, (int, float)) and hxd_node <= 0:
            message = f"'{label}' in {cover_name} must be greater than zero."
            hx.errors.validation(message)
            are_all_valid = False

    return are_all_valid

### --- RATE CHANGE HELPERS --- ###

# Unique sentinel value used when fillna is enabled or duplicates are found
SENTINEL = str(uuid.uuid4())

def sanitize_and_sort_expiring_list_by_renewal(
    expiring_list, 
    renewal_list, 
    sorting_key, 
    remove_duplicates=False
):
    """
    Sort the expiring list to follow the order of the renewal list based on a given sorting key.
    
    - If there are duplicate sorting keys in the expiring list, the value is replaced with a unique sentinel.
    - If there are duplicate sorting keys in the renewal list and that key is present in the expiring list,
      the expiring list's value is replaced with a unique sentinel.
      
    The resulting effect is that any item with a modified sorting key will be included in the dropped items.

    """
    # Initialise flags for warnings
    flag_exp_duplicates = False
    flag_renewal_duplicates = False
    
    if remove_duplicates:
        # Replace duplicate sorting_keys in the expiring_list with a unique sentinel value
        exp_keys = [d[sorting_key] for d in expiring_list]
        dup_exp_keys = {k for k, count in Counter(exp_keys).items() if count > 1}
        if dup_exp_keys:
            flag_exp_duplicates = True
        for idx, d in enumerate(expiring_list):
            if d[sorting_key] in dup_exp_keys:
                d[sorting_key] = f"{SENTINEL}_{idx}"
        
        # Check for duplicate sorting_keys in the renewal_list
        renewal_keys = [d[sorting_key] for d in renewal_list]
        dup_renewal_keys = {k for k, count in Counter(renewal_keys).items() if count > 1}
        for idx, d in enumerate(expiring_list):
            if d[sorting_key] in dup_renewal_keys:
                d[sorting_key] = f"{SENTINEL}_{idx}"
                flag_renewal_duplicates = True
    
    # Create a lookup for the order of keys from the renewal list
    renewal_order = {d[sorting_key]: idx for idx, d in enumerate(renewal_list)}
    
    # Partition expiring_list into items with keys in renewal_order and those without
    common = [d for d in expiring_list if d[sorting_key] in renewal_order]
    others = [d for d in expiring_list if d[sorting_key] not in renewal_order]
    
    # Sort items present in the renewal_order
    common.sort(key=lambda d: renewal_order[d[sorting_key]])
    
    # Build warnings list based on the triggered conditions
    warnings = []
    if remove_duplicates and flag_exp_duplicates:
        warnings.append("Duplicate countries are present in the expiring data.")
    if remove_duplicates and flag_renewal_duplicates:
        warnings.append("Duplicate countries are present in the renewal data, and the same country is present in the expiry fleet.")        
    
    return common + others, warnings

# Split expiring and renewal list based on elements in renewal list
def split_renewal_list_by_expiring(expiring_sorted, renewal_list, sorting_key):
    # Build a set of keys from the expiring list and renewal list
    expiring_keys = {item[sorting_key] for item in expiring_sorted}
    renewal_keys = {item[sorting_key] for item in renewal_list}

    # Partition the renewal list based on renewal_keys and expiring_keys
    common = [item for item in expiring_sorted if item[sorting_key] in renewal_keys]
    other = [item for item in renewal_list if item[sorting_key] not in expiring_keys]
    dropped = [item for item in expiring_sorted if item[sorting_key] not in renewal_keys]

    return common, other, dropped


### --- RECURSIVE FUNCTIONS FOR ATTRIBUTES --- ###
def rsetattr(obj, attr, val, splitter="/", list_item=0):
    pre, _, post = attr.rpartition(splitter)
    try:
        hxd_obj = rgetattr(obj, pre, splitter=splitter, list_item=list_item) if pre else obj

        if dir(hxd_obj) == ['__contains__', '__delitem__', '__getitem__', '__iadd__', '__iter__', '__len__', '__reversed__', 'append', 'count', 'extend', 'index', 'insert', 'remove']:
            return setattr(hxd_obj[list_item], post, val)
        else:
            return setattr(hxd_obj, post, val)
    except AttributeError as a:
        print(f"can't set attribute - {attr} to {str(val)}")

def _rgetattr(obj, attr, list_item=0):
    # Check for list in offline/real hxd agnostic way
    if dir(obj) == ['__contains__', '__delitem__', '__getitem__', '__iadd__', '__iter__', '__len__', '__reversed__', 'append', 'count', 'extend', 'index', 'insert', 'remove']:
        return getattr(obj[list_item], attr)
    else:
        return getattr(obj, attr)

def rgetattr(obj, attr, splitter="/", list_item=0):
    func = functools.partial(_rgetattr, list_item=list_item)
    return functools.reduce(func, [obj] + attr.split(splitter))

def _rgetkey(obj, key, list_item=0):
    if isinstance(obj, list):
        return obj[list_item][key]
    else:
        return obj[key]

def rgetkey(obj, key, splitter="/", list_item=0):
    func = functools.partial(_rgetkey, list_item=list_item)
    return functools.reduce(func, [obj] + key.split(splitter))

### --- LOOK-UP FUNCTIONS --- ###

# Provide information on a failed lookup
def _handle_exception(e, if_not_found):
    try:
        # Extract the entire traceback stack with the file name and line number where error occured
        tb_stack = traceback.extract_stack()
        caller_info = tb_stack[-4] # Typically, the index of the caller in the stack
        file_name = caller_info.filename
        line_number = caller_info.lineno
        print(f"Error during lookup: {e} in file {file_name}, line {line_number}. Defaulting value to {if_not_found}.")
    except:
        print(f"Error during lookup: {e}. Defaulting value to {if_not_found}.")

# Handle single lookup
def _handle_single_lookup(lookup_value, lookup_col, return_col, df, if_not_found):
    value = if_not_found
    filter_condition = df[lookup_col] == lookup_value

    try:
        value = df.loc[filter_condition, return_col].iloc[0]
    except Exception as e:
        _handle_exception(e, if_not_found)

    return value

# Handle array lookup
def _handle_array_lookup(lookup_value, lookup_col, return_col, df, if_not_found):
    # Convert lookup_value to a DataFrame and name the column
    result_df = lookup_value.to_frame(name="lookup_col")
    
    # Ensure both columns have the same data type before merging
    if df[lookup_col].dtype != result_df["lookup_col"].dtype:
        # Convert the data type of result_df["lookup_col"] to match df[lookup_col]
        result_df["lookup_col"] = result_df["lookup_col"].astype(df[lookup_col].dtype)
    
    # Merge the DataFrames
    result_df = result_df.merge(df, left_on="lookup_col", right_on=lookup_col, how="left")
    
    # Fill NaN values with if_not_found and return the result column
    result = result_df[return_col].fillna(if_not_found)
    
    return result

# Function to find the closest value in a column to a given value
def find_closest(df, column, lookup_value, direction="lower", if_not_found=0, lookup_type="array", distance=1):
    sorted_values = df[column].sort_values().values
    
    if lookup_type == "single":
        # Check if look_value is a scalar or a pandas Series and return error
        if isinstance(lookup_value, pd.Series):
            raise ValueError("'lookup_value' is an array, but 'lookup_type' is 'single'.")
        
        idx = sorted_values.searchsorted(lookup_value)
        if direction == "lower":
            idx -= distance
            if idx >= 0:
                return sorted_values[idx]
            else:
                return sorted_values[0]
        elif direction == "upper":
            if idx < len(sorted_values):
                return sorted_values[idx]
            else:
                return sorted_values[-1]
        return if_not_found
    
    elif lookup_type == "array":
        # Check if look_value is a scalar or a pandas Series and return error
        if not isinstance(lookup_value, pd.Series):
            raise ValueError("'lookup_value' is a scalar, but 'lookup_type' is 'array'.")
        
        lookup_values = lookup_value.values if isinstance(lookup_value, pd.Series) else lookup_value
        idxs = np.searchsorted(sorted_values, lookup_values, side='right')
        
        if direction == "lower":
            idxs -= distance
            idxs[idxs < 0] = 0
            closest_values = sorted_values[idxs]
        elif direction == "higher":
            idxs[idxs >= len(sorted_values)] = len(sorted_values) - 1
            closest_values = sorted_values[idxs]
        else:
            raise ValueError("Invalid direction. Use 'lower' or 'higher'.")
        
        return pd.Series(closest_values, index=lookup_value.index if isinstance(lookup_value, pd.Series) else None)
    else:
        raise ValueError("Invalid lookup_type. Use 'single' or 'array'.")

# Function for exact match lookup, handles errors by returning 1
def look_up(lookup_value, lookup_col, return_col, df, if_not_found=np.nan, lookup_type="array"):
    if not isinstance(df, pd.DataFrame):
        print(f"Warning: Expected 'df' to be a pandas DataFrame, but got {type(df).__name__}.")
        return if_not_found
    
    # Only handle the two types of lookup
    if lookup_type == "single":
        return _handle_single_lookup(lookup_value, lookup_col, return_col, df, if_not_found)
    elif lookup_type == "array":
        return _handle_array_lookup(lookup_value, lookup_col, return_col, df, if_not_found)
    else:
        raise ValueError("Invalid lookup_type. Use 'single' or 'array'.")

# Function for closest match lookup, handles errors by returning if_not_found
def look_up_closest(lookup_value, lookup_col, return_col, df, direction="lower", if_not_found=np.nan, lookup_type="array", distance=1):
    if not isinstance(df, pd.DataFrame):
        print(f"Warning: Expected 'df' to be a pandas DataFrame, but got {type(df).__name__}.")
        return if_not_found
    
    closest_value = find_closest(df, lookup_col, lookup_value, direction, if_not_found, lookup_type, distance)

    # Only handle the two types of lookup
    if lookup_type == "single":
        return _handle_single_lookup(closest_value, lookup_col, return_col, df, if_not_found)
    elif lookup_type == "array":
        return _handle_array_lookup(closest_value, lookup_col, return_col, df, if_not_found)
    else:
        raise ValueError("Invalid lookup_type. Use 'single' or 'array'.")
    
# --- Adding look-ups with bounds
# Handle single bounds lookup
def _handle_single_lookup_with_bounds(lookup_value, lower_bound_col, upper_bound_col, return_col, df, if_not_found):
    try:
        filter_condition = (df[lower_bound_col] <= lookup_value) & (df[upper_bound_col] > lookup_value)
        value = df.loc[filter_condition, return_col].iloc[0]
    except Exception as e:
        _handle_exception(e, if_not_found)
        value = if_not_found
    return value

# Handle array bounds lookup
def _handle_array_lookup_with_bounds(lookup_value, lower_bound_col, upper_bound_col, return_col, df, if_not_found):
    try:
        # Ensure the DataFrame is sorted by lower_bound_col for efficient searching
        df_sorted = df.sort_values(lower_bound_col).reset_index(drop=True)
        lower_bounds = df_sorted[lower_bound_col].values
        upper_bounds = df_sorted[upper_bound_col].values

        # Convert lookup_value to a NumPy array for vectorized operations
        lookup_array = lookup_value.values if isinstance(lookup_value, pd.Series) else np.array(lookup_value)

        # Use searchsorted to find the insertion point for each lookup value
        indices = np.searchsorted(lower_bounds, lookup_array, side="right") - 1

        # Initialize the result array with if_not_found
        result = np.full(lookup_array.shape, if_not_found, dtype=df_sorted[return_col].dtype)

        # Create a mask for valid indices
        valid_mask = (indices >= 0) & (lookup_array < upper_bounds[indices])

        # Assign the corresponding return_col values where the mask is valid
        result[valid_mask] = df_sorted.loc[indices[valid_mask], return_col].values

        return pd.Series(result, index=lookup_value.index if isinstance(lookup_value, pd.Series) else None)
    except Exception as e:
        _handle_exception(e, if_not_found)
        if isinstance(lookup_value, pd.Series):
            return pd.Series([if_not_found] * len(lookup_value), index=lookup_value.index)
        else:
            return if_not_found

def look_up_with_bounds(lookup_value, lower_bound_col, upper_bound_col, return_col, df, if_not_found=np.nan, lookup_type="array"):
    if not isinstance(df, pd.DataFrame):
        print(f"Warning: Expected 'df' to be a pandas DataFrame, but got {type(df).__name__}.")
        return if_not_found

    # Only handle the two types of lookup
    if lookup_type == "single":
        return _handle_single_lookup_with_bounds(lookup_value, lower_bound_col, upper_bound_col, return_col, df, if_not_found)
    elif lookup_type == "array":
        return _handle_array_lookup_with_bounds(lookup_value, lower_bound_col, upper_bound_col, return_col, df, if_not_found)
    else:
        raise ValueError("Invalid lookup_type. Use 'single' or 'array'.")

### --- COMMONLY USED VALUES --- ###

def get_countries_retrieved(hxd, matching_key="country_cvg_subcvg"):
    expo = hxd.cds.exposure.granular

    return {
        "matching_keys": [getattr(c, matching_key) for c in expo.countries],
        "inception_date": date_to_string(hxd.hx_core.inception_date)
    }

def tp_components(hxd, bp_class=None):

    # Pull in technical premium parameters from user library 
    tp_params_df = params.tp_parameters.df()
    fx_rates_df = params.fx_rates.df()

    # Get latest available YOA
    yoa = hxd.hx_core.inception_date.year
    tp_year = yoa if yoa in list(tp_params_df["year"]) else tp_params_df["year"].max()

    # Get correct params based on BP class and year
    if not bp_class:
        bp_class = hxd.cds.standard_fields.benchmark_class
        
    bp_mask = (tp_params_df["business_plan_class"] == bp_class) & (tp_params_df["year"] == tp_year)

    # Set up tp params
    che = tp_params_df[bp_mask]["che"].iloc[0]
    var_exp = tp_params_df[bp_mask]["var_exp"].iloc[0]
    inv_inc = tp_params_df[bp_mask]["inv_inc"].iloc[0]
    cost_of_ri = tp_params_df[bp_mask]["cost_of_ri"].iloc[0]
    ri_rec = tp_params_df[bp_mask]["ri_rec"].iloc[0]
    roc = tp_params_df[bp_mask]["roc"].iloc[0]
    fixed_exp_usd = tp_params_df[bp_mask]["fixed_exp"].iloc[0]
    capital_req = tp_params_df[bp_mask]["capital_req"].iloc[0]
    nmp_load = tp_params_df[bp_mask]["nmp_load"].iloc[0]

    # Convert fixed expenses to model currency (default to USD if error)
    ccy = hxd.cds.currencies.source_currency
    fixed_exp = fixed_exp_usd * look_up(ccy, "ccy", "fx_rate", fx_rates_df, lookup_type="single", if_not_found=1)
    
    # Add TP params to dict
    tp_dict = {
        "che": che,
        "var_exp": var_exp,
        "inv_inc": inv_inc,
        "cost_of_ri": cost_of_ri,
        "ri_rec": ri_rec,
        "roc": roc,
        "fixed_exp": fixed_exp,
        "capital_req": capital_req,
        "nmp_load": nmp_load,
        "technical_lr": (1 - var_exp + inv_inc - (cost_of_ri-ri_rec) - roc * capital_req) # Calculate technical loss ratio (excl. fixed costs)
    }

    return tp_dict
