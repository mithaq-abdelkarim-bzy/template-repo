import hx
import pandas as pd
import numpy as np
from operator import itemgetter



def title_rc(string):
    string = string.replace("_and_"," & ")
    string = string.replace("_"," ")
    string = string.title()

    return (string)

# new version - Seb A (24-07-2024 code review) requested update to version described here https://www.beazley.hxrenew.com/customer-service/labs/python-tips/pandas/reading-writing-pandas#reading-an-entire-lists-contents-at-once
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
        #print(str(i) + ' of ' + str(df.shape[0]))
        for col in output_cols_to_write:
            setattr(list_node[i], col, dictionary[col][i])
        for col in override_cols_to_write:
            #only need to bring back calculated column as overrides will work as normal
           setattr(getattr(list_node[i], col),"calculated",dictionary[col + "_calculated"][i])



# Fastest way to write pandas back to hxd
# Caveat is it requires manual specification of columns to write
def write_pd_to_hxd_no_overrides(df, list_node, output_cols_to_write): 
    dictionary = df.to_dict()
    
    for i in range(df.shape[0]):
        for col in output_cols_to_write:
            setattr(list_node[i], col, dictionary[col][i])



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


# Handle division by 0
def ratio(a, b, if_undefined=0):
    """
    Handles division by 0 by returning 0 instead of an error.
    Can change 'if_undefined' parameter to return a different number.
    """
    a = np.asarray(a)
    b = np.asarray(b)
    c = np.where(b == 0, if_undefined, a / b)
    return c
    

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