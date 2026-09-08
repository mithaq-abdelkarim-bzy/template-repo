import hx
import pandas as pd
import numpy as np
import math
from datetime import timedelta, date
import calendar
from operator import itemgetter, attrgetter
from datetime import datetime

DAYS_IN_LEAP_YEAR = 366
DAYS_IN_NON_LEAP_YEAR = 365
SECONDS_IN_A_DAY = 86400.0


def title_rc(string):
    string = string.replace("_and_", " & ")
    string = string.replace("_", " ")
    string = string.title()

    return string


def calculate_policy_term(inception_date, expiry_date):
    prorata = 1
    if inception_date and expiry_date:
        policy_days = (expiry_date - inception_date).days

        start_date = datetime.combine(inception_date, datetime.min.time())
        next_date = (
            pd.to_datetime(start_date) + pd.DateOffset(years=1) - pd.DateOffset(days=1)
        )
        delta_days = (next_date - start_date).days

        prorata = policy_days / delta_days

    return prorata


# Fastest way to convert a hx_list into a pandas dataframe
def pd_df_from_hx_list(hx_list):
    """
    Turns a hx.List() into a pandas DataFrame in a vectorised way,
    without having to specify or loop through the keys/column names in the hx.List().
    Also unpacks nested structures and extracts selected values from override fields.
    """
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
    nested_items = {
        k: dir(v) for k, v in top_row.items() if "hx_internal" in str(type(v))
    }

    # Loops through all of the found items and unpacks them
    while nested_items:
        for col in nested_items:
            # As the mode is not inferrable from the object type, use the list of available
            # attributes determined above to determine if the object is an override or not
            if nested_items[col] == [
                "calculated",
                "is_overridden",
                "override",
                "selected",
            ]:
                # This is set up to simply import the selected property of override nodes
                # but can be easily modified here to bring in any other property, or multiple
                # properties
                df[col + "_selected"] = df[col].apply(attrgetter("selected"))
                df[col + "_calculated"] = df[col].apply(attrgetter("calculated"))
                df[col] = df[col].apply(attrgetter("selected"))
            else:
                # If the item is not an override, unpack all of it's children to the DataFrame
                for child in nested_items[col]:
                    df[f"{col}/{child}"] = df[col].apply(attrgetter(child))
                df = df.drop(col, axis=1)

        # Finally, check to see if there are still items that need to be unpacked
        # (i.e. if there were multiple layers of nested structures)
        top_row = df.iloc[0]
        nested_items = {
            k: dir(v) for k, v in top_row.items() if "hx_internal" in str(type(v))
        }

    return df


# Fastest way to write pandas back to hxd
# Caveat is it requires manual specification of columns to write
def write_pd_to_hxd(df, list_node, output_cols_to_write, override_cols_to_write=[]):
    dictionary = df.to_dict()
    for i in range(df.shape[0]):
        for col in output_cols_to_write:
            setattr(list_node[i], col, dictionary[col][i])
        if override_cols_to_write:
            for col in override_cols_to_write:
                # only need to bring back calculated column as overrides will work as normal
                setattr(
                    getattr(list_node[i], col),
                    "calculated",
                    dictionary[col + "_calculated"][i],
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
    # Validate input types
    if not isinstance(start_date, date) or not isinstance(end_date, date):
        hx.errors.validation(
            "start date and end date must be instances of datetime.date"
        )
        return 0

    # Validate date range
    if start_date > end_date:
        hx.errors.validation("start date must be before or equal to end date")
        return 0

    if for_term:
        end_date += timedelta(days=1)

    total_days = (end_date - start_date).days
    leap_years = sum(
        1 for year in range(start_date.year, end_date.year + 1) if calendar.isleap(year)
    )
    non_leap_years = (end_date.year - start_date.year + 1) - leap_years

    total_days_in_years = (leap_years * DAYS_IN_LEAP_YEAR) + (
        non_leap_years * DAYS_IN_NON_LEAP_YEAR
    )
    years_count = end_date.year - start_date.year + 1

    if years_count == 0:
        hx.errors.validation(
            "The range of years is zero, cannot calculate average days per year"
        )
        return 0

    average_days_per_year = total_days_in_years / years_count

    if average_days_per_year == 0:
        hx.errors.validation(
            "Average days per year calculated as 0, cannot divide by zero"
        )
        return 0

    difference_in_years = total_days / average_days_per_year

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
            caller_info = tb_stack[
                -3
            ]  # Typically, the index of the caller in the stack
            file_name = caller_info.filename
            line_number = caller_info.lineno
            print(
                f"Error during lookup: {e} in file {file_name}, line {line_number}. Defaulting value to {if_not_found}."
            )
        except:
            print(f"Error during lookup: {e}. Defaulting value to {if_not_found}.")

    return value


# Function for exact match lookup, handles errors by returning 1
def look_up(lookup_value, lookup_col, return_col, df, if_not_found=1):
    if not isinstance(df, pd.DataFrame):
        print(
            f"Warning: Expected 'df' to be a pandas DataFrame, but got {type(df).__name__}."
        )
        return if_not_found
    filter_condition = df[lookup_col] == lookup_value
    return _perform_lookup(df, filter_condition, return_col, if_not_found)


# Function for range-based lookup, handles errors by returning 1
def look_up_with_bounds(
    lookup_value, lower_bound_col, upper_bound_col, return_col, df, if_not_found=1
):
    """
    Performs ranged based lookup. Note lower bound is inclusive, upper bound is exclusive. Bounds must not overlap.
    """
    if not isinstance(df, pd.DataFrame):
        print(
            f"Warning: Expected 'df' to be a pandas DataFrame, but got {type(df).__name__}."
        )
        return if_not_found
    filter_condition = (df[lower_bound_col] <= lookup_value) & (
        df[upper_bound_col] > lookup_value
    )
    return _perform_lookup(df, filter_condition, return_col, if_not_found)


def safe_get_and_fillna(df, column, default):
    if not default:
        default = 0
    value = df.get(column, default)
    return value.fillna(default) if isinstance(value, pd.Series) else value


def transform_key(key):
    # Split the key by underscores, capitalize each word, and join with spaces
    return " ".join(word.capitalize() for word in key.split("_"))


def hxd_node_setter(parent, node, value):
    """
    Set the value of a hx node, throwing a validation error with the key and value if the value is invalid.
    """
    try:
        setattr(parent, node, value)
    except Exception as e:
        # transformed_key = transform_key(node)
        # hx.errors.validation(f'Can\'t assign "{value}" to "{transformed_key}" {e}')
        return


def retrieve_range_values(
    table, lower_bound, upper_bound, lower_search_key, upper_search_key
):
    """
    Retrieve range values from a table based on specified bounds and search keys.

    Args:
        table (pandas.DataFrame): The table to retrieve values from.
        lower_bound (str): The lower bound column name.
        upper_bound (str): The upper bound column name.
        lower_search_key (float): The lower search key.
        upper_search_key (float): The upper search key.

    Returns:
        list: A list of tuples containing the lower bound, upper bound, and the corresponding row values.

    """
    filter_query = (
        f"{upper_bound} > {lower_search_key} & {lower_bound} <= {upper_search_key}"
    )
    return table.query(filter_query)


def is_hx_class(node_name):
    return "hx_internal" in str(type(node_name))


def forecast(known_x_list, known_y_list, x_to_predict):
    """
    Predicts the y value for a given x using linear regression.

    Parameters:
    known_x_list (list): List of known x values.
    known_y_list (list): List of known y values.
    x_to_predict (float): The x value for which to predict the y value.

    Returns:
    float: The predicted y value.
    """

    coefficients = np.polyfit(known_x_list, known_y_list, 1)
    slope, intercept = coefficients

    # Predict the y value for the given x
    predicted_y = slope * x_to_predict + intercept

    return predicted_y


# Create variables to avoid looping when accessing layers and coverages
def one_layer(hxd):
    """
    Returns: layer, cvg
    Use these variables to directly access the hxd without looping
    """

    layer = hxd.cds.layers[0]
    cvg = layer.coverages

    return layer, cvg


def date_to_string(date_obj: date) -> str:
    if date_obj is None:
        return date_obj
    return date_obj.strftime("%Y-%m-%d")
