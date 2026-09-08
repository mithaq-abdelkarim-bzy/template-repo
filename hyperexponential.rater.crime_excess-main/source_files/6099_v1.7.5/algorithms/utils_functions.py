import hx
import pandas as pd
import numpy as np
from operator import itemgetter


# This function creates the name to be presented in the view from the input variable
def create_title(string):
    string = string.replace("_ex_per","")
    string = string.replace("_ex_prop","")
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