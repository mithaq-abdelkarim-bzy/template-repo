import hx
import functools
import pandas as pd
import numpy as np
from operator import itemgetter
import traceback
from datetime import datetime, timedelta
from calendar import isleap
from typing import List
from algorithms.data_schema.sch_rater_defined import all_coverages_dict
from algorithms import parameter_tables_schema as params

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
def write_pd_to_hxd(df, list_node, output_cols_to_write, override_cols_to_write=[]):
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
    a = np.asarray(a)
    b = np.asarray(b)
    c = np.where(b == 0, if_undefined, a / b)
    return c

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
def usd(value, ccy, ccy_table=params.fx_rates.df()):
    fx_rate = look_up(ccy, "ccy", "fx_rate", ccy_table, if_not_found=1, lookup_type="single")
    value_in_usd = ratio(value, fx_rate)
    return value_in_usd

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

### --- RECURSIVE FUNCTIONS FOR ATTRIBUTES --- ###
def rsetattr(obj, attr, val, splitter="/", list_item=0):
    pre, _, post = attr.rpartition(splitter)
    try:
        hxd_obj = rgetattr(obj, pre, splitter=splitter, list_item=list_item) if pre else obj

        if dir(hxd_obj) == ['__contains__', '__delitem__', '__getitem__', '__iadd__', '__iter__', '__len__', '__reversed__', 'append', 'count', 'extend', 'index', 'insert', 'remove']:
        # if isinstance(hxd_obj, list):
            return setattr(hxd_obj[list_item], post, val)
        else:
            return setattr(hxd_obj, post, val)
    except AttributeError as a:
        print(f"can't set attribute - {attr} to {str(val)}")

def _rgetattr(obj, attr, list_item=0):
    # Check for list in offline/real hxd agnostic way
    if dir(obj) == ['__contains__', '__delitem__', '__getitem__', '__iadd__', '__iter__', '__len__', '__reversed__', 'append', 'count', 'extend', 'index', 'insert', 'remove']:
    # if isinstance(obj, list):
        return getattr(obj[list_item], attr)
    else:
        return getattr(obj, attr)

def rgetattr(obj, attr, splitter="/", list_item=0):
    func = functools.partial(_rgetattr, list_item=list_item)
    return functools.reduce(func, [obj] + attr.split(splitter))

def _rgetkey(obj, key, list_item=0):
    # Check for list in offline/real hxd agnostic way
    # if dir(obj) == ['__contains__', '__delitem__', '__getitem__', '__iadd__', '__iter__', '__len__', '__reversed__', 'append', 'count', 'extend', 'index', 'insert', 'remove']:
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
        caller_info = tb_stack[-3] # Typically, the index of the caller in the stack
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
def look_up(lookup_value, lookup_col, return_col, df, if_not_found=0, lookup_type="array"):
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
def look_up_closest(lookup_value, lookup_col, return_col, df, direction="lower", if_not_found=0, lookup_type="array", distance=1):
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


### --- COMMONLY USED VALUES --- ###

def tp_components(hxd):

    # Pull in technical premium parameters from user library 
    tp_params_df = params.tp_parameters.df()
    fx_rates_df = params.fx_rates.df()

    # Get latest available YOA
    yoa = hxd.hx_core.inception_date.year
    tp_year = yoa if yoa in list(tp_params_df["year"]) else tp_params_df["year"].max()

    # Get correct params based on BP class and year
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
      
    
### --- FORMULAS --- ###

def calculate_logit(alfa, beta, logit_lx, gamma, low_logit, theta, high_logit, tblRefPoints):
    logit1S = look_up("20-24", "Age band", "logit(l(x))", tblRefPoints, lookup_type="single")
    logit2S = look_up("65-69", "Age band", "logit(l(x))", tblRefPoints, lookup_type="single")

    logit = alfa + (beta * logit_lx) - gamma * (1 - ratio(low_logit, logit1S)) - theta * (1 - ratio(high_logit, logit2S))

    return logit

def calculate_approx_lx(logit):
    approx_lx = 100000 * ratio(np.exp(logit), (1 + np.exp(logit)))
    return approx_lx

def calculate_qx(lives_df, which, prefix):

    if prefix not in ["N", "L"]:
        raise ValueError("Invalid prefix. Use 'N' for nationality or 'L' for location.")

    # Calculate min, median and max for the lx
    min_lx = lives_df[[f"{prefix}_lx_actual_Approx_l(x)", f"{prefix}_lx_above_Approx_l(x)", f"{prefix}_lx_plus2_Approx_l(x)"]].min(axis=1)
    median_lx = lives_df[[f"{prefix}_lx_actual_Approx_l(x)", f"{prefix}_lx_above_Approx_l(x)", f"{prefix}_lx_plus2_Approx_l(x)"]].median(axis=1)
    max_lx = lives_df[[f"{prefix}_lx_actual_Approx_l(x)", f"{prefix}_lx_above_Approx_l(x)", f"{prefix}_lx_plus2_Approx_l(x)"]].max(axis=1)

    # Calculate min, median and max for the ages
    min_ages = lives_df[["S_age_actual_Nominal_average_age", "S_age_above_Nominal_average_age", "S_age_plus2_Nominal_average_age"]].min(axis=1)
    median_ages = lives_df[["S_age_actual_Nominal_average_age", "S_age_above_Nominal_average_age", "S_age_plus2_Nominal_average_age"]].median(axis=1)
    max_ages = lives_df[["S_age_actual_Nominal_average_age", "S_age_above_Nominal_average_age", "S_age_plus2_Nominal_average_age"]].max(axis=1)

    # Calculate the age condition
    age_condition_lower = np.where(lives_df["S_age_plus2_Nominal_average_age"] < lives_df["S_age_actual_Nominal_average_age"], 
                        lives_df["S_adj_plus2_Ultimate_to_Duration"], 
                        lives_df["S_adj_actual_Ultimate_to_Duration"])
    age_condition_upper = np.where(lives_df["S_age_plus2_Nominal_average_age"] < lives_df["S_age_actual_Nominal_average_age"], 
                        lives_df["S_adj_actual_Ultimate_to_Duration"], 
                        lives_df["S_adj_above_Ultimate_to_Duration"])

    # Calculate the final result
    if which == "lower":
        qx_lower = (1 - median_lx / max_lx) / (median_ages - min_ages) * age_condition_lower * lives_df[f"{prefix}_a&b_0_factor_for_dev_country"]
        return qx_lower
    elif which == "upper":
        qx_upper = (1 - min_lx / median_lx) / (max_ages - median_ages) * age_condition_upper * lives_df[f"{prefix}_a&b_0_factor_for_dev_country"]
        return qx_upper
    else:
        raise ValueError("The 'which' argument should be either 'lower' or 'upper'.")

def calculate_exp_params(lives_df, which, prefix):

    if prefix not in ["N", "L"]:
        raise ValueError("Invalid prefix. Use 'N' for nationality or 'L' for location.")

    # Log-transform the dependent variable range
    log_y = np.log(lives_df[[f"{prefix}_qx_0_Qx_lower", f"{prefix}_qx_0_Qx_upper"]].values)
    
    # Independent variable range: Create a design matrix with an intercept term
    X = np.array([[1, 1], [1, 2]])

    # Perform linear regression using numpy.linalg.lstsq
    # We need to solve for each row in log_y separately
    coefficients = np.linalg.lstsq(X, log_y.T, rcond=None)[0]

    # Extract intercepts and slopes
    intercepts = coefficients[0]
    slopes = coefficients[1]

    # Compute the exponential of the intercepts
    exp_intercepts = np.exp(intercepts)

    # Convert the results to pandas Series
    exp_intercepts_series = pd.Series(exp_intercepts, index=lives_df.index)
    slopes_series = pd.Series(slopes, index=lives_df.index)

    if which == "c":
        return exp_intercepts_series
    elif which == "b":
        return slopes_series
    else:
        raise ValueError("which must be either 'b' or 'c'")

def calculate_x_value(lives_df, age_col="age_attained"):
    
    # Extract the relevant columns
    age_attained = lives_df[age_col]  # Assuming 'F' is the column name in the DataFrame
    age_plus_2 = lives_df["S_age_plus2_Nominal_average_age"]
    age_actual = lives_df["S_age_actual_Nominal_average_age"]
    age_above = lives_df["S_age_above_Nominal_average_age"]

    # Calculate the minimum of the specified columns
    min_val = np.min([age_plus_2, age_actual, age_above], axis=0)
    
    # Calculate the median of the specified columns
    median_val = np.median([age_plus_2, age_actual, age_above], axis=0)
    
    # Apply the formula
    x_val = 1 + ratio((age_attained - min_val), (median_val - min_val))

    return x_val

def calculate_r1(lives_df, life_CauseSplitCoeff, life_CauseSplitIntercept, age_col="age_attained"):
    
    CauseSplitCoeff = life_CauseSplitCoeff["Coefficient of (x-62)2"].iloc[0]
    CauseSplitIntercept = life_CauseSplitIntercept["Intercept term"].iloc[0]

    r1 = CauseSplitCoeff * (lives_df[age_col] - 62)**2 + lives_df["B_nat_nation_Parameter_m"] * (lives_df[age_col] - 62) + CauseSplitIntercept
    r1_true = np.maximum(r1, CauseSplitIntercept)

    return r1_true

def calculate_ci_exp_param(lives_df):
    def compute_params(row):
        # Log-transform the dependent variables
        log_y = np.log([row["ci_rate_lower_age"], row["ci_rate_upper_age"]])
        
        # Independent variable range with an intercept term
        X = np.array([[1, row["ci_age_band_min"]], [1, row["ci_age_band_max"]]])
        
        # Perform linear regression using numpy.linalg.lstsq
        coefficients, residuals, rank, s = np.linalg.lstsq(X, log_y, rcond=None)
        
        # Extract the slope and intercept
        slope = coefficients[1]
        intercept = coefficients[0]
        
        # Compute the exponential of the slope
        exp_intercept = np.exp(intercept)
        
        return pd.Series([exp_intercept, slope])

    # Apply the function to each row and convert the result to a DataFrame
    params_df = lives_df.apply(compute_params, axis=1)
    params_df.columns = ["ci_c_param", "ci_b_param"]

    # Concatenate the original DataFrame with the new parameters
    lives_df = pd.concat([lives_df, params_df], axis=1)

    return lives_df