import hx
import pandas as pd
import numpy as np
from operator import itemgetter
from datetime import timedelta, datetime


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
                    df[f"{col}/{child}"] = df[col].apply(attrgetter(child))
                df = df.drop(col, axis=1)

        # Finally, check to see if there are still items that need to be unpacked
        # (i.e. if there were multiple layers of nested structures)
        top_row = df.iloc[0]
        nested_items = {k: dir(v) for k, v in top_row.items() if "hx_internal" in str(type(v))}

    return df



# Fastest way to write pandas back to hxd
# Caveat is it requires manual specification of columns to write
def write_pd_to_hxd(df, list_node, output_cols_to_write, override_cols_to_write = []):
    dictionary = df.to_dict()
    for i in range(df.shape[0]):
        for col in output_cols_to_write:
            setattr(list_node[i], col, dictionary[col][i])
        if override_cols_to_write:
            for col in override_cols_to_write:
                #only need to bring back calculated column as overrides will work as normal
                setattr(getattr(list_node[i], col),"calculated",dictionary[col + "_calculated"][i])


# Calculates the policy term rating factor
def policy_term(inception_date: datetime, expiry_date: datetime):
    """
    Calculates the policy term rating factor. 
    This function returns 1.0 both if the expiry date is exclusive (e.g. 06/12/2024 - 06/12/2025), the US method,
    or if the expiry date is inclusive (e.g. 06/12/2024 - 05/12/2025).

    Parameters:
        inception_date: datetime
        expiry_date: datetime

    Returns:
        float: The year difference, considering leap years.
    """

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
    '''
    Performs ranged based lookup. Note lower bound is inclusive, upper bound is exclusive. Bounds must not overlap.
    '''
    if not isinstance(df, pd.DataFrame):
        print(f"Warning: Expected 'df' to be a pandas DataFrame, but got {type(df).__name__}.")
        return if_not_found
    filter_condition = (df[lower_bound_col] <= lookup_value) & (df[upper_bound_col] > lookup_value)
    return _perform_lookup(df, filter_condition, return_col, if_not_found)


    

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




def transient_list_from_hx_list(hx_list):
    '''
    Turns a hx.List() into a nested list for use with the transient hxd. 
    Also unpacks nested structures and extracts selected values from override fields.
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
