import hx
import pandas as pd
import numpy as np
from operator import itemgetter
from algorithms import rate_constants as constants
import calendar as ca

LIST_NODE_DIR = ['__contains__', '__delitem__', '__getitem__', '__iadd__', '__iter__', '__len__', '__reversed__', 'append', 'count', 'extend', 'index', 'insert', 'remove']


def calc_pro_rata(inception, expiry, method):
    # Method 1:
    if method == 1:
        pro_rata = year_diff(inception, expiry, False)
    # Method 2:
    elif method == 2:
        # Using the max to avoid a 0 when inception = expiry
        pro_rata = max((360 * (expiry.year - inception.year) + (30 * (expiry.month - inception.month) + (expiry.day - inception.day))), 1)
        pro_rata = pro_rata / 360

    return pro_rata


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


# SA: Could do with some refining to be generic. Works for the current purpose only
def pd_df_from_hx_structure(hx_structure):
    '''
    Turns a hx.List() into a pandas DataFrame in a vectorised way, without having to specify or loop through the keys/column names in the hx.List().
    '''
    row_designation = dir(hx_structure)

    col_designation = {x[0]: getattr(x[1], "is_overridden", None) is not None for x in getattr(hx_structure, row_designation[0])}
    override_cols = [k for k, v in col_designation.items() if v]
    normal_cols = [x for x in col_designation if x not in override_cols]

    list_representation = [
        {column: getattr(row[1], column) for column in normal_cols}
        | 
        {f"{column}_calculated": getattr(row[1], column).calculated for column in override_cols} 
        | 
        {f"{column}_override": getattr(row[1], column).override for column in override_cols} 
        for row in hx_structure
    ]

    df = pd.DataFrame(list_representation, index=row_designation)

    return df


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
        end_date += timedelta(days=1)

    diffyears = end_date.year - start_date.year
    difference  = end_date - start_date.replace(end_date.year)
    days_in_year = ca.isleap(end_date.year) and 366 or 365
    difference_in_years = diffyears + (difference.days + difference.seconds/86400.0)/days_in_year

    return difference_in_years

def year_diff_expiring(start_date, end_date, for_term):
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
def _perform_lookup(df, filter_condition, return_cols, if_not_found):
    value = if_not_found  # Set the default return value

    try:
        value = df.loc[filter_condition, return_cols].iloc[0]
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

    if isinstance(value, pd.Series):
        return value.to_dict()
    elif isinstance(return_cols, list) and value == if_not_found:
        return {col: value for col in return_cols}
    else:
        return value


# Function for exact match lookup, handles errors by returning 1
def look_up(lookup_value, lookup_col, return_cols, df, if_not_found=1):
    if not isinstance(df, pd.DataFrame):
        print(f"Warning: Expected 'df' to be a pandas DataFrame, but got {type(df).__name__}.")
        return if_not_found
    filter_condition = df[lookup_col] == lookup_value
    return _perform_lookup(df, filter_condition, return_cols, if_not_found)
    

# Function for range-based lookup, handles errors by returning 1
def look_up_with_bounds(lookup_value, lower_bound_col, upper_bound_col, return_cols, df, if_not_found=1):
    '''
    Performs ranged based lookup. Note lower bound is inclusive, upper bound is exclusive. Bounds must not overlap.
    '''
    if not isinstance(df, pd.DataFrame):
        print(f"Warning: Expected 'df' to be a pandas DataFrame, but got {type(df).__name__}.")
        return if_not_found
    filter_condition = (df[lower_bound_col] <= lookup_value) & (df[upper_bound_col] > lookup_value)
    return _perform_lookup(df, filter_condition, return_cols, if_not_found)
    

# a function that checks the input is within a range and sends a message
#check to make sure not none first as factors may not be needed for model
def factor_validation(min, max, factor, string):
    if factor is not None:
        if factor > max or factor < min:
            hx.errors.validation(f"{string} factor is outside min and max")

# a function that checks the input is within a range and exits the function
def input_validation(min, max, value, string):
    if value is not None:
        if value > max or value < min:
            hx.errors.validation(f"{string} is less than {min} or greater than {max}")
            return False  # Indicate validation failure
        return True  # Indicate validation success
    return

#a validation that just returns the error message
def value_less_than_min_validation(min_val, value, value_string, min_string):
    if value is not None:
        if value < min_val:
            hx.errors.validation(f"{value_string} is  less than {min_string}")
            return False  # Indicate validation failure
        return True  # Indicate validation success
    return

def greater_than_validation(max, value, value_string, max_string):
    if max > value:
        hx.errors.validation(f"{max_string} is  greater than {value_string}")
        return False  # Indicate validation failure
    return True  # Indicate validation success

#a validation that just returns the error message
def value_greater_than_max_validation(max, value, value_string, max_string):
    if value > max:
        hx.errors.validation(f"{value_string} is  greater than {max_string}")

def ratio_validation(max, numerator, denominator, numerator_string, denominator_string):
    if denominator == 0:
        return
    else:    
        if numerator / denominator > max:
            hx.errors.validation(
                f"{numerator_string} divided by {denominator_string} is  greater than {max}"
            )
            return False  # Indicate validation failure
        return True  # Indicate validation success


def interpolation_factor(retention, table, lower_column, upper_column, large_loss_potential_column, factor_table, factor_table_column):
    row_to_use = table[
        (table[lower_column] <= retention)
        & (table[upper_column] > retention)
    ].iloc[0]

    lower_bound = row_to_use[lower_column]
    upper_bound = row_to_use[upper_column]

    lower_factor = factor_table.loc[factor_table[factor_table_column] == lower_bound, large_loss_potential_column].iloc[0]
    upper_factor = factor_table.loc[factor_table[factor_table_column] == upper_bound, large_loss_potential_column].iloc[0]

    interpolation_factor = ((retention - lower_bound)/(upper_bound - lower_bound)) * (upper_factor - lower_factor) + lower_factor

    return interpolation_factor


def agg_lim_calc(option, results, name, table, lower_col, upper_col):
    input_to_use = option.aggregate_limit  

    df_res = look_up_with_bounds(input_to_use, lower_col, upper_col, [lower_col, upper_col], table)

    x0 = df_res[lower_col]
    x1 = df_res[upper_col]

    if name == "eec_info":
        results.setdefault("limit_from", []).append(x0)
        results.setdefault("limit_to", []).append(x1)
    else:
        output = (input_to_use - x0) / (x1 - x0)
        results.setdefault(name, []).append(output)


# a function that allows you to set the labels of table rows depending on the min, max and factor
# this is best called from within the validation function.
#this also considers the None condition first
def set_labels(selection, min, max, column_labels, row_node, label):
    if selection is None:
        setattr(column_labels, row_node, label)
    else:
        setattr(
            column_labels,
            row_node,
            (
                f"{label} {constants.incomplete_column}"
                if selection > max or selection < min
                else label
            )
        )

def set_labels_multiple_selections(options, column_labels, row_node, label):
    if [option.option_selected for option in options] is None:
        setattr(column_labels, row_node, label)
    else:
        setattr(
            column_labels,
            row_node,
            (
                f"{label} {constants.incomplete_column}"
                if sum([option.option_selected for option in options]) > 1
                else label
            )
        )

def rsetattr(obj, attr, val, splitter=".", list_items=[0]):
    pre, _, post = attr.rpartition(splitter)
    try:
        hxd_obj = rgetattr(obj, pre, splitter=splitter, list_items=list_items) if pre else obj

        if dir(hxd_obj) == LIST_NODE_DIR:
            return setattr(hxd_obj[list_items[-1]], post, val)
        else:
            return setattr(hxd_obj, post, val)
    except AttributeError as a:
        print(f"can't set attribute - {attr} to {str(val)}")
        setattr(hxd_obj, post, val)


def _rgetattr(obj, attr, list_items=[0], get_missing_indexes_from=None):
    if not isinstance(list_items, list):
        list_items = [list_items]
    if list_items == []:
        list_items = [0]

    # Check for list in offline/real hxd agnostic way
    if dir(obj) == LIST_NODE_DIR:
        list_item = list_items[0]
        list_items = list_items[1:]
        if get_missing_indexes_from is not None and len(obj) <= list_item:
            return getattr(get_missing_indexes_from._default_child, attr), list_items
        else:
            return getattr(obj[list_item], attr), list_items
    else:
        return getattr(obj, attr), list_items


def rgetattr(obj, attr, splitter=".", list_items=[0], get_missing_indexes_from=None):
    attrs = attr.split(splitter)
    for a in attrs:
        obj, list_items_new = _rgetattr(obj, a, list_items=list_items, get_missing_indexes_from=get_missing_indexes_from)
        if get_missing_indexes_from is not None:
            get_missing_indexes_from, _ = _rgetattr(get_missing_indexes_from, a, list_items=list_items)

        list_items = list_items_new  # Need to assign here as list_items is needed unmodified for both _rgetattr statements
    return obj

def validate_aggregate_retention(
    options,
    aggregate_limit_max,
    aggregate_limit_min,
    retention_max,
    retention_min,
    coverage_string
):
    """
    Validates aggregate limit and retention values in a list of options.

    Args:
        options: A list of objects with 'aggregate_limit' and 'retention' attributes.
        aggregate_limit_max: The maximum allowed aggregate limit.
        aggregate_limit_min: The minimum allowed aggregate limit.
        retention_max: The maximum allowed retention.
        retention_min: The minimum allowed retention.
        coverage_string: A string the indicates which coverage is being selected.

     Returns a tuple containing:
        - bool: True if at least one option passes validation, False otherwise.  This is for the overall loop control.
        - list: A list of indices (0-based) of options that passed validation.  These are the options to process.
    """

   
    valid_options = []
    overall_passed = False # Flag to indicate if at least one option passed
    for i, option in enumerate(options):
        if option.aggregate_limit is None or option.retention is None:
            hx.errors.validation(f"Option {i+1} in {coverage_string} Inputs is missing aggregate limit or retention.")
            continue  # Skip to the next option if either is missing

        
        if (option.aggregate_limit > aggregate_limit_max or
                option.aggregate_limit < aggregate_limit_min):
            hx.errors.validation(f"Option {i+1} in {coverage_string} Inputs has an aggregate limit outside the allowed range ({aggregate_limit_min}-{aggregate_limit_max}).")
            continue
        if coverage_string == "EPL":     
           if (option.retention > retention_max or option.retention < retention_min):
                hx.errors.validation(f"Option {i+1} in {coverage_string} Inputs has a retention outside the allowed range ({retention_min}-{retention_max}).")
                continue      
        else:
            if (option.retention < retention_min):
                hx.errors.validation(f"Option {i+1} in {coverage_string} Inputs: Retention should be greater than {retention_min}.")
                continue 

   

        valid_options.append(i)
        overall_passed = True # Set to True if at least one option passes

    return overall_passed, valid_options


def validate_selected_coverage_options(hxd, options, coverage):
    current_coverage = constants.coverage_validation_mapping.get(coverage, {})

    if not current_coverage:
        pass
    
    # Validate selected options
    if sum([option.option_selected for option in options]) > 1:
        error_message = f"Please only select one {current_coverage['label']} option"
        hx.errors.validation(error_message)
        #set the text box as a more immediate prompt
        current_coverage["are_multiple_selected"](hxd.non_cds, True)
        current_coverage["multiple_selected_error_msg"](hxd.non_cds, error_message)

    label_object = rgetattr(hxd.non_cds,current_coverage["column_label_field"])
    set_labels_multiple_selections(options, label_object, "option_selected", "Option Selected?")