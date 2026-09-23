import hx
import pandas as pd
import numpy as np
from operator import itemgetter, attrgetter
from datetime import timedelta
import datetime as date
import calendar as ca
import math
from scipy.stats import gamma, poisson, lognorm, norm


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
                    df[f"{col}.{child}"] = df[col].apply(attrgetter(child))
                df = df.drop(col, axis=1)

        # Finally, check to see if there are still items that need to be unpacked
        # (i.e. if there were multiple layers of nested structures)
        top_row = df.iloc[0]
        nested_items = {k: dir(v) for k, v in top_row.items() if "hx_internal" in str(type(v))}

    return df

# Fastest way to write pandas back to hxd
# Caveat is it requires manual specification of columns to write
# def write_pd_to_hxd(df, list_node, output_cols_to_write, override_cols_to_write = None):
#     dictionary = df.to_dict()
    
#     for i in range(df.shape[0]):
#         for col in output_cols_to_write:
#             setattr(list_node[i], col, dictionary[col][i])
#         for col in override_cols_to_write:
#             #only need to bring back calculated column as overrides will work as normal
#             setattr(getattr(list_node[i], col),"calculated",dictionary[col + "_calculated"][i])
# def write_pd_to_hxd(df, list_node, output_cols_to_write):
#     dictionary = df.to_dict()
   
#     for i in range(df.shape[0]):
#         for col in output_cols_to_write:
#             setattr(list_node[i], col, dictionary[col][i])
# Fastest way to write pandas back to hxd
# Caveat is it requires manual specification of columns to write

def write_pd_to_hxd(df, list_node, output_cols_to_write, override_cols_to_write = []):
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
        end_date += date.timedelta(days=1)

    diffyears = end_date.year - start_date.year

    try: # IR edit
        difference = end_date - start_date.replace(end_date.year)
    except ValueError: # If end_date is Feb 29th (i.e. in leap year) but Feb 29th doesn't exist in start_date year (i.e. not a leap year), use Feb 28th.
        difference = end_date - date.date(end_date.year, 2, 28)

    days_in_year = ca.isleap(end_date.year) and 366 or 365
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


# LEV function
def lev(x, mu, sigma, distribution = "lognormal"):
    if distribution == "gamma":
        if x == 0:
            lev_result = 0
        else:
            lev_result  = mu * sigma * gamma.cdf(x, mu+1, sigma, scale =1) + x*(1-gamma.cdf(x, mu, sigma, scale =1))
    else:
        if x == 0:
            lev_result = 0
        else: 
            lev_result = math.exp(0.5 * sigma**2 + mu) * norm.cdf((math.log(x) - mu)/sigma - sigma, loc = 0, scale = 1) + x * (1 -norm.cdf((math.log(x) - mu)/sigma, loc = 0, scale = 1))
    return lev_result

# calucate ILF
def layer_lev(underlying, new_lim, mu, sigma):
    if underlying < 0:
        layer_lev_result = 0
    else:
        layer_lev_result = lev(underlying+new_lim, mu,sigma) - lev(underlying, mu, sigma)
    return layer_lev_result


#lev column 
def lev_col(x, mu, sigma, distribution="lognormal"):
    if distribution == "gamma":
        lev_result = np.where(x == 0, 0, mu * sigma * gamma.cdf(x, mu+1, sigma, scale =1) + x*(1-gamma.cdf(x, mu, sigma, scale=1)))
    else:
        lev_result = np.where(x == 0, 0, np.exp(0.5 * sigma**2 + mu) * norm.cdf((np.log(x) - mu)/sigma - sigma, loc=0, scale=1) + x * (1 -norm.cdf((np.log(x) - mu)/sigma, loc=0, scale=1)))
    return lev_result

#lev column 
def lev_col_lognormal(x, mu, sigma):
    # SA: where is redundant here when called from layer_lev_col as it already checks for x = 0
    return np.exp(0.5 * sigma**2 + mu) * norm.cdf((np.log(x) - mu)/sigma - sigma, loc=0, scale=1) + x * (1 -norm.cdf((np.log(x) - mu)/sigma, loc=0, scale=1))

# calculate ILF
def layer_lev_col(underlying, new_lim, mu, sigma):
    layer_lev_result = np.where(underlying == 0, 0, lev_col_lognormal(underlying + new_lim, mu, sigma) - lev_col_lognormal(underlying, mu, sigma))
    return layer_lev_result

# Calculates the policy term rating factor
def policy_term(inception_date: date, expiry_date: date):
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