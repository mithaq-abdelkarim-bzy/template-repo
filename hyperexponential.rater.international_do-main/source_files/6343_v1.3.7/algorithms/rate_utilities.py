import hx
import pandas as pd
import numpy as np
from operator import itemgetter
from operator import attrgetter
import re as re
from datetime import timedelta, datetime
import calendar as ca
from scipy.stats import gamma, poisson, lognorm, norm
from algorithms import parameter_tables_schema as params
import algorithms.rate_constants as const





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
        difference = end_date - datetime.date(end_date.year, 2, 28)

    days_in_year = ca.isleap(end_date.year) and 366 or 365
    difference_in_years = diffyears + (difference.days)/days_in_year

    return difference_in_years

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


def day_diff(start_date, end_date, for_term):
    """
    Calculate the number of days between two dates, optionally adjusting the end date for an inclusive term.

    Parameters:
        start_date (datetime.date): The start date.
        end_date (datetime.date): The end date, adjusted by one day if for_term is True.
        for_term (bool): Adjust end date by one day if True.

    Returns:
        int: The total number of days between start and end dates.
    """
    if for_term:
        end_date += timedelta(days=1)

    return (end_date - start_date).days


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

# Convert to USD
def usd(value, ccy, ccy_table=params.fx_rates.df(), lookup_type="single"):
    fx_rate = look_up(ccy, "ccy", "fx_rate", ccy_table, if_not_found=1, lookup_type=lookup_type)
    value_in_usd = ratio(value, fx_rate)
    return value_in_usd

# Convert to currency from USD
def to_ccy(value_in_usd, ccy, ccy_table=params.fx_rates.df(), lookup_type="single"):
    """Converts from USD value to current currency"""
    fx_rate = look_up(ccy, "ccy", "fx_rate", ccy_table, if_not_found=1, lookup_type=lookup_type)
    value = value_in_usd * fx_rate
    return value



# Function that extracts the SIC code from anywhere in a string 

def extract_sic(input):
    match = re.search(r'\d+', input) 
    if match: 
        return match.group()
        
        return None

    pass


# Interpolates a value from a given table
# Looks up the x value above and below and looks up f(x) from the table
# Returns input "if_out_of_range" if no above and below value in the table can be found
def interp_table_row(df, value, x_lower, x_upper, f_lower, f_upper, if_out_of_range):
    if (
        (value >= min(df[x_lower]))  & 
        (value < max(df[x_upper]))
    ):
        df_row = df[(df[x_lower] <= value) & (df[x_upper] > value)].iloc[0]
        xp = [df_row[x_lower], df_row[x_upper]]
        fp = [df_row[f_lower], df_row[f_upper]]
        result = np.interp(value, xp, fp)
    else:
        result = if_out_of_range
    return result


# Applies the truncated lognormal distribution to a layer
def truncated_lognormal(limit, excess, mu, sigma, order=1):
    # Convert inputs to NumPy arrays once
    limit = np.asarray(limit, dtype=np.float64)
    excess = np.asarray(excess, dtype=np.float64)

    # Cap values to avoid divide-by-zero and overflow
    upper = np.minimum(limit + excess, 1e9)
    lower = np.minimum(excess, 1e9)

    # Replace zeros with a small positive value for log stability
    upper = np.where(upper == 0, np.finfo(float).eps, upper)
    lower = np.where(lower == 0, np.finfo(float).eps, lower)

    # Precompute logs
    log_upper = np.log(upper)
    log_lower = np.log(lower)

    # Precompute constant multiplier
    base_exp = np.exp(order * mu + 0.5 * order**2 * sigma**2)

    # levupper_lnorm
    z_upper_k = (log_upper - mu) / sigma - order * sigma
    z_upper = (log_upper - mu) / sigma
    levupper_lnorm = base_exp * norm.cdf(z_upper_k) + upper**order * (1 - norm.cdf(z_upper))

    # levlower_lnorm
    z_lower_k = (log_lower - mu) / sigma - order * sigma
    z_lower = (log_lower - mu) / sigma
    levlower_lnorm = base_exp * norm.cdf(z_lower_k) + lower**order * (1 - norm.cdf(z_lower))

    # Denominator with clipping for stability
    denominator = np.clip(1 - norm.cdf(z_lower), np.finfo(float).eps, None)

    return (levupper_lnorm - levlower_lnorm) / denominator

# Function that calculates the fixed claim amount within specified limits
def fixed_clt(x, xmin, xmax, franchise):

    # Ensure x, xmin, and xmax are numpy arrays with right type
    x = np.array(x, dtype=np.float64)
    xmin = np.array(xmin, dtype=np.float64)
    xmax = np.array(xmax, dtype=np.float64)

    result = np.maximum(np.minimum(x, xmax), xmin) - xmin * (not franchise)

    return result

# Function that Calculates Net Technical Premium for an Array of Expected Losses
def calc_net_tech_premium(expected_losses, hxd):

    import algorithms.rate_utilities as utils
    
    fx_rates = params.fx_rates.df()
    tp_params_df = params.tp_parameters.df()

    # FX Rates
    ccy = hxd.cds.currencies.source_currency
    fx_rate = fx_rates[fx_rates["ccy"]==ccy]["fx_rate"].iloc[0]

    bp_class = "International ML"

    year = calc_tp_year(hxd)

    tp_IML = tp_params_df[(tp_params_df['business_plan_class'] == bp_class) &
        ((tp_params_df['year'] == year))]

    che = np.float64(tp_IML["che"].iloc[0])
    var_exp = np.float64(tp_IML["var_exp"].iloc[0])
    inv_inc = np.float64(tp_IML["inv_inc"].iloc[0])
    cost_of_ri = np.float64(tp_IML["cost_of_ri"].iloc[0])
    ri_rec = np.float64(tp_IML["ri_rec"].iloc[0])
    roc = np.float64(tp_params_df[(tp_params_df['business_plan_class'] == bp_class)]["roc"].iloc[0])
    fixed_exp_usd = np.float64(tp_IML["fixed_exp"].iloc[0])
    fixed_exp = np.float64(fixed_exp_usd*fx_rate)
    capital_req = np.float64(tp_IML["capital_req"].iloc[0])
    nmp_load = np.float64(tp_IML["nmp_load"].iloc[0])

    profit_load = capital_req * roc

    tech_prem = ((np.array(expected_losses, dtype = np.float64) * (1 + che) + fixed_exp)/(1 - (cost_of_ri - ri_rec) - var_exp - profit_load + inv_inc))


    return tech_prem


def calc_tp_year(hxd):

    tp_params_df = params.tp_parameters.df()
    
    yoa = hxd.hx_core.inception_date.year
    bp_year = yoa if yoa in tp_params_df["year"].values else tp_params_df["year"].max()

    return bp_year
