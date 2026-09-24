import hx
import pandas as pd
import polars as pl
import pyarrow as pa
import numpy as np
from operator import itemgetter, attrgetter
from calendar import isleap
from datetime import timedelta
from typing   import List, Optional, Iterable
from libraries.model_profiler.algorithms.profiling_hxd_functions         import time_me

def title_rc(string):
    string = string.replace("_and_"," & ")
    string = string.replace("_"," ")
    string = string.title()

    return (string)


# Fastest way to convert a hx_list into a pandas dataframe
@time_me
def pd_df_from_hx_list(hx_list):
    '''
    Turns a hx.List() into a pandas DataFrame in a vectorised way,
    without having to specify or loop through the keys/column names in the hx.List().
    Also unpacks nested structures and extracts selected values from override fields.
    '''        
    if len(hx_list) == 0:
        return pd.DataFrame(hx_list)

    hx_name = str(hx_list)
    # Check if it already exists in the global DFs cache    
    # if hx_name and (hx_name in global_dfs.keys()):
    #     return global_dfs[hx_name]
        
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

    # if hx_name:
    #     global_dfs[hx_name] = df    
    return df




def _data_attrs(obj) -> Iterable[str]:
    """
    Return data-like attributes for obj, preferring __dict__ keys.
    Falls back to filtering dir() to exclude dunder and callables.
    """
    if hasattr(obj, "__dict__") and isinstance(obj.__dict__, dict):
        return obj.__dict__.keys()
    # Fallback: filter dir() to avoid methods/dunders
    attrs = []
    for a in dir(obj):
        if a.startswith("__") and a.endswith("__"):
            continue
        try:
            val = getattr(obj, a)
        except Exception:
            continue
        # keep non-callable, non-descriptor values
        if not callable(val):
            attrs.append(a)
    return attrs


@time_me
def pd_df_from_hx_list_v3(    hx_list,    columns: Optional[List[str]] = None,
                            non_override_children: Optional[List[str]] = None,) -> pd.DataFrame:
    if columns:
        data = [[rgetattr(x, col) for col in columns] for x in hx_list]
        return pd.DataFrame(data, columns=columns)

    # Flatten top-level (vectorized-ish)
    records = [{name: value for name, value in row} for row in hx_list]
    df = pd.DataFrame.from_records(records)

    # # Default: only pull `value` from non-override nodes (fast and typically sufficient)
    # if non_override_children is None:
    #     non_override_children = ['value']

    # Identify nested columns from top row
    top = df.iloc[0]

    # Helper to detect override shape quickly without computing full dir()
    def is_override(obj, attrs=None):
        # A robust check using attributes that should exist
        at = set(attrs or _data_attrs(obj))
        needed = {'calculated', 'is_overridden', 'override', 'selected'}
        return needed.issubset(at)

    # Build a mapping of nested columns and their attribute plans once
    nested_cols = {}
    for col, val in top.items():
        t = str(type(val))
        if val is not None and "hx_internal" in t:
            attrs = list(_data_attrs(val))  # data-like attrs only
            if is_override(val, attrs):
                nested_cols[col] = ('override', ['is_overridden', 'selected'])
            else:
                # Limit extraction to user-specified minimal children
                # Only include those present in attrs
                children = [a for a in non_override_children if a in attrs]
                nested_cols[col] = ('generic', children)

    # If nothing nested, we’re done
    if not nested_cols:
        return df

    # Extract attributes in bulk, assign directly, then drop old nested columns
    for col, (mode, children) in nested_cols.items():
        col_vals = df[col].values  # ndarray of objects for faster iteration
        if mode == 'override':
            # selected + is_overridden only
            df[f"{col}/is_overridden"] = [getattr(x, "is_overridden") for x in col_vals]
            df[col] = [getattr(x, "selected") for x in col_vals]  # overwrite with selected
        else:
            # generic: only requested minimal children
            for child in children:
                df[f"{col}/{child}"] = [getattr(x, child) for x in col_vals]
            # If you don’t need the original object column anymore, drop it:
            df.drop(columns=[col], inplace=True)
    return df


def pd_df_from_hx_list_seb(hx_list, columns: Optional[List[str]] =None):
    '''
    Turns a hx.List() into a pandas DataFrame in a vectorised way,
    without having to specify or loop through the keys/column names in the hx.List().
    Also unpacks nested structures and extracts selected values from override fields.


    Args:
        hx_list: The hxd list node object
        columns: A list of columns to import. Manually specifying this is more efficient in most cases,
            especially when the number of children required is much smaller than the number of children in 
            the list. If this is not specified, all children are imported. 
    '''

    if not hx_list:  # JB added to handle empty list
        return pd.DataFrame(columns=columns if columns else [])

    if columns:
        # Can speed the function up a lot by manually specifying columns. This also can reduce the
        # amount of data imported if you only need to import the input columns. Nested columns must 
        # be referenced down to the deepest child node using dot (".") notation 
        df = pd.DataFrame(
            [[
                rgetattr(x, col) for col in columns
            ] for x in hx_list], 
            columns=columns
            )
        df.columns = [c.replace('.',            '/') for c in df.columns] # JB added to format consistently correctly
        df.columns = df.columns.str.replace(r'/selected$', '', regex=True) # JB added to format consistently correctly # SA fix to only change when ends in selected as breaking selected_ielr
    else:
        df = pd.DataFrame(hx_list)

        # If not specifying columns manually, importing all of the hx_list element gives a pandas 
        # DataFrame where each value is a tuple of (hxd_item_name, hxd_item_value).
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
                    df[f"{col}/is_overridden"] = df[col].apply(attrgetter("is_overridden"))
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






@time_me
def pd_df_from_hx_list_v2(hx_list, columns: Optional[List[str]] =None):
    '''
    Turns a hx.List() into a pandas DataFrame in a vectorised way,
    without having to specify or loop through the keys/column names in the hx.List().
    Also unpacks nested structures and extracts selected values from override fields.


    Args:
        hx_list: The hxd list node object
        columns: A list of columns to import. Manually specifying this is more efficient in most cases,
            especially when the number of children required is much smaller than the number of children in 
            the list. If this is not specified, all children are imported. 
    '''

    if not hx_list:  # JB added to handle empty list
        return pd.DataFrame(columns=columns if columns else [])

    if columns:
        # Can speed the function up a lot by manually specifying columns. This also can reduce the
        # amount of data imported if you only need to import the input columns. Nested columns must 
        # be referenced down to the deepest child node using dot (".") notation 
        df = pd.DataFrame(
            [[
                rgetattr(x, col) for col in columns
            ] for x in hx_list], 
            columns=columns
            )
        df.columns = [c.replace('.',            '/') for c in df.columns] # JB added to format consistently correctly
        df.columns = [c.replace('/selected',    '' ) for c in df.columns] # JB added to format consistently correctly
    else:
        df = pd.DataFrame(hx_list)

        # If not specifying columns manually, importing all of the hx_list element gives a pandas 
        # DataFrame where each value is a tuple of (hxd_item_name, hxd_item_value).
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
                    df[f"{col}/is_overridden"] = df[col].apply(attrgetter("is_overridden"))
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


























def rgetattr(obj, path):
    '''
    Recursively access a nested hxd object though a attribute path that includes "."
    '''
    for attr in path.split('.'):
        obj = getattr(obj, attr)
    return obj

@time_me
def pl_df_from_hx_list(hx_list):
    pd_df = pd_df_from_hx_list(hx_list)
    arrow_table = pa.Table.from_pandas(pd_df, preserve_index=False)
    pl_df = pl.from_arrow(arrow_table)
    return pl_df

@time_me
def pd_to_pl_df(pd_df):
    arrow_table = pa.Table.from_pandas(pd_df, preserve_index=False)
    pl_df = pl.from_arrow(arrow_table)
    return pl_df


# Fastest way to write pandas back to hxd
# Caveat is it requires manual specification of columns to write
# Fastest way to write pandas back to hxd
# Caveat is it requires manual specification of columns to write
@time_me
def write_pd_to_hxd(df, list_node, output_cols_to_write, override_cols_to_write=[]):    

    hx_name = str(list_node)
    
    dictionary = df.to_dict()
    for i in range(df.shape[0]):
        for col in output_cols_to_write:
            # set nested columns (Structure Node in list Node)
            if '/' in col:
                parent_col, child_col = col.split('/')
                setattr(
                    getattr(list_node[i], parent_col), child_col, dictionary[col][i])
            else:
                setattr(list_node[i], col, dictionary[col][i])
        if override_cols_to_write:
            for col in override_cols_to_write:
                # only need to bring back calculated column as overrides will work as normal
                if '/' in col:
                    parent_col, child_col = col.split('/')
                    setattr(
                        getattr(getattr(list_node[i], parent_col), child_col),
                        "calculated",
                        dictionary[col][i])
                else:
                    setattr(
                        getattr(list_node[i], col), "calculated", dictionary[col][i])

@time_me
# 20% faster using itertuples
def write_pd_to_hxd_v2(df, list_node, output_cols_to_write, override_cols_to_write=[]):    
    
    # Map column names to positions once
    col_to_pos = {c: i for i, c in enumerate(df.columns)}

    # Iterate rows as tuples
    for i, row in enumerate(df.itertuples(index=False, name=None)):
        for col in output_cols_to_write:
            # set nested columns (Structure Node in list Node)
            if '/' in col:
                parent_col, child_col = col.split('/', 1)
                target                = getattr(list_node[i], parent_col)
                target_col            = child_col
            else:
                target                = list_node[i]    
                target_col            = col
            value = row[col_to_pos[col]]
            setattr(target, target_col, value)

        if override_cols_to_write:
            for col in override_cols_to_write:
                # only need to bring back calculated column as overrides will work as normal
                if '/' in col:
                    parent_col, child_col = col.split('/', 1)
                    target                = getattr(getattr(list_node[i], parent_col), child_col)
                else:
                    target                = getattr(list_node[i], col)
                value             = row[col_to_pos[f"{col}/calculated"]]
                target.calculated = value    




@time_me
def write_pl_to_hxd(df: pl.DataFrame, list_node, output_cols_to_write, override_cols_to_write=[]):
    """
    Writes data from a Polars DataFrame back into a list_node (e.g. hx.List()), handling
    both flat attributes and nested override structures.
    """
    n_rows = df.height

    # Convert each column into a list once (efficient access)
    data = {col: df[col].to_list() for col in output_cols_to_write + override_cols_to_write}

    for i in range(n_rows):
        for col in output_cols_to_write:
            if '/' in col:
                parent_col, child_col = col.split('/')
                setattr(
                    getattr(list_node[i], parent_col),
                    child_col,
                    data[col][i]
                )
            else:
                setattr(list_node[i], col, data[col][i])

        for col in override_cols_to_write:
            if '/' in col:
                parent_col, child_col = col.split('/')
                setattr(
                    getattr(getattr(list_node[i], parent_col), child_col),
                    "calculated",
                    data[col][i]
                )
            else:
                setattr(
                    getattr(list_node[i], col),
                    "calculated",
                    data[col][i]
                )


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

    diffyears           = end_date.year - start_date.year
    difference          = end_date - start_date.replace(end_date.year)
    days_in_year        = isleap(end_date.year) and 366 or 365
    difference_in_years = diffyears + (difference.days + difference.seconds/86400.0)/days_in_year

    return difference_in_years


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


def year_frac(start_date, end_date):
    """
    Calculates the year fraction between two dates using the US 30/360 day count convention.
    
    The 30/360 method assumes all months have 30 days and a year has 360 days. It is commonly used 
    in financial calculations such as bond interest accrual and loan schedules.
    
    Parameters:
        start_date (datetime.date): The starting date.
        end_date (datetime.date): The ending date.
    
    Returns:
        float: The fractional number of years between the two dates based on the 30/360 convention.
    """

    # Extract year, month, and day from both dates
    Y1, M1, D1 = start_date.year, start_date.month, start_date.day
    Y2, M2, D2 = end_date.year, end_date.month, end_date.day

    # Adjust start day: if it's the 31st, treat it as the 30th
    if D1 == 31:
        D1 = 30

    # Adjust end day: if it's the 31st and start day is 30 or 31, treat it as the 30th
    if D2 == 31 and D1 in [30, 31]:
        D2 = 30

    # Calculate the year fraction using the 30/360 formula
    year_frac = ((Y2 - Y1) * 360 + (M2 - M1) * 30 + (D2 - D1)) / 360

    return year_frac



# Safely sum totals, handling missing columns

def safe_sum_cols(df, cols, nan_value=0):
    """
    Safely sum specified columns in a DataFrame, handling missing columns and NaN values.

    Parameters:
    ----------
    df   : pd.DataFrame                         The DataFrame containing the columns to sum.
    cols : list of str                          List of column names to sum.
    nan_value : numeric, optional (default=0)   Value to use in place of NaN or missing columns.

    Returns:
    -------
    pd.Series        A Series representing the row-wise sum across the specified columns.
    """
    return sum(df[col].fillna(nan_value) if col in df.columns else nan_value for col in cols)



def safe_divide_into_column(df, numerator_col, denominator_col, result_col, default=0.0):
    """
    Safely divides two DataFrame columns element-wise and assigns the result to a new column using masking.

    Parameters:
    - df: pd.DataFrame
    - numerator_col: str - column name for the numerator
    - denominator_col: str - column name for the denominator
    - result_col: str - column name where the result will be stored
    - default: value to assign when denominator is 0 or NaN

    Returns:
    - pd.DataFrame with result_col added/updated
    """
    # Convert columns to numeric types
    df[numerator_col] = pd.to_numeric(df[numerator_col], errors='coerce')
    df[denominator_col] = pd.to_numeric(df[denominator_col], errors='coerce')

    # Initialize the result column with default value
    df[result_col] = default

    # Apply division only where the denominator is not zero or NaN
    valid_mask = (df[denominator_col] != 0) & (~df[denominator_col].isna())
    df.loc[valid_mask, result_col] = (
        df.loc[valid_mask, numerator_col] / df.loc[valid_mask, denominator_col]
    )

    return df

def drop_and_merge(left_df, right_df, on, how='left', drop_from='left', validate='many_to_one'):
    """
    Safely merges two DataFrames while avoiding column duplication and enforcing merge integrity.

    Parameters:
    ----------
    left_df : pd.DataFrame        The left DataFrame in the merge operation.
    right_df : pd.DataFrame       The right DataFrame in the merge operation.
    on : list or str              Column(s) to join on. Must be present in both DataFrames.
    how : str, default 'left'     Type of merge to perform. Options include 'left', 'right', 'inner', 'outer'.
    drop_from : str, default 'left'
        Specifies which DataFrame to drop overlapping columns from before merging.
        Options: 'left' or 'right'.
    validate : str, default 'many_to_one'
        Ensures the merge relationship is valid. For example, 'many_to_one' checks that
        the right DataFrame has unique keys.

    Returns:
    -------
    pd.DataFrame        A merged DataFrame with overlapping columns removed and merge integrity validated.

    Raises:
    ------
    MergeError          If the merge relationship does not match the specified `validate` condition.
    """
    # Drop any columns from left_df that also exist in right_df (excluding the join keys)
    overlap_cols = [col for col in right_df.columns if col in left_df.columns and col not in on]
    
    if drop_from == 'left':
        left_df  = left_df.drop(columns=overlap_cols)
    else:
        right_df = right_df.drop(columns=overlap_cols)

    # Perform the merge
    return left_df.merge(right_df, on=on, how=how, validate=validate)



def indirect_column_lookup(df: pd.DataFrame, column_name: str) -> np.ndarray:
    """
    For each row in the DataFrame, looks up the value from the column whose name is specified
    in the given column (e.g., 'adjustments_lower_str').

    Parameters:
    - df: pd.DataFrame — the input DataFrame
    - column_name: str — the name of the column containing the target column names

    Returns:
    - np.ndarray — array of values looked up from the specified columns
    """
    # Convert DataFrame to NumPy array
    values = df.to_numpy()

    # Get column indices for each row's target column name
    col_indices = df.columns.get_indexer(df[column_name])

    # Get row indices
    row_indices = np.arange(len(df))

    # Return the looked-up values
    return values[row_indices, col_indices]


def safe_fillna_except(df: pd.DataFrame, exclude_cols: list) -> pd.DataFrame:
    """
    Fills NaN values with 0 in all columns except those listed in exclude_cols,
    but only if those columns exist in the DataFrame.

    Parameters:
    - df: pd.DataFrame — the input DataFrame
    - exclude_cols: list — list of column names to exclude from fillna

    Returns:
    - pd.DataFrame — DataFrame with NaNs filled (except in excluded columns)
    """
    # Filter out columns that don't exist in the DataFrame
    valid_exclude = [col for col in exclude_cols if col in df.columns]

    # Identify columns to fill
    fill_cols = [col for col in df.columns if col not in valid_exclude]

    # Fill NaNs in selected columns
    df[fill_cols] = df[fill_cols].fillna(0)

    return df
