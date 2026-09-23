import hx
import pandas as pd
import numpy as np
from operator import itemgetter


# This function creates the name to be presented in the view from the input variable
def create_title(string):
    string = string.replace("_ex_per","")
    string = string.replace("_ex_prop","")
    string = string.replace("_yoy","")
    string = string.replace("_and_"," & ")
    string = string.replace("_rc","")
    string = string.replace("_"," ")
    string = string.title()

    return (string)



# helper function for viewing pandas dataframes
def glimpse_pd(df, max_width=76):

    # find the max string lengths of the column names and dtypes for formatting
    _max_len = max([len(col) for col in df])
    _max_dtype_label_len = max([len(str(df[col].dtype)) for col in df])

    # print the dimensions of the dataframe
    print(f"{type(df)}:  {df.shape[0]} rows of {df.shape[1]} columns")

    # print the name, dtype and first few values of each column
    for _column in df:

        _col_vals = df[_column].head(max_width).to_list()
        _col_type = str(df[_column].dtype)

        output_col = f"{_column}:".ljust(_max_len+1, ' ')
        output_dtype = f" {_col_type}".ljust(_max_dtype_label_len+3, ' ')

        output_combined = f"{output_col} {output_dtype} {_col_vals}"

        # trim the output if too long
        if len(output_combined) > max_width:
            output_combined = output_combined[0:(max_width-4)] + " ..."

        print(output_combined)

# Helper function for python format
def format_f_string(num):
    if num is None:
        # SA: Is it correct that None will always translate to infinity? 
        # None can be from any data error, while infinity can be accurately represented by np.inf
        return "infinity"  
    elif num >= 10**6:
        return f"${num/10**6}m"
    elif num >= 10**3:
        return f"${num/10**3}k"
    else:
        return f"${num}"
        

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
    