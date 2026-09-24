import hx
import pandas as pd
import numpy as np
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, remove_before_separator, append_error_message, write_pd_to_hxd_from_task, pd_df_from_hx_list_columns_task, get_nested_attr
import algorithms.rate_constants as const
from dateutil import parser
import re
import datetime
from dateutil.relativedelta import relativedelta
from typing import Union, List, Dict, Tuple
from algorithms.steer.async_steer_populate_bc_patterns import steer_populate_bc_patterns
from algorithms.rate_validation import input_paths_steer_format_raw_data_task, get_inputs_steer_format_data_task

def steer_clear_raw_data(hxd, progress):
    """
    Clear raw_data input
    """
    raw_data = hxd.cds.steer.experience_rating.raw_data
    raw_data_df = pd_df_from_hx_list(raw_data)
    
    raw_data_df = raw_data_df.drop(index=raw_data_df.index, errors='ignore')

    write_pd_to_hxd(raw_data_df,raw_data,[f"column_{index}" for index in range(1,110)])
    return


def steer_validate_raw_data(hxd, progress):
    """
    Validates the data in the 'raw_data' based on rules in the 'Data Mapping & Other Fields' section.
    Writes errors to the 'RawDataError' and return error raw data error section.
    """

    tbl_data_mapping = hx.params.table_steer_expe_data_mapping

    # async_input nodes
    raw_data = hxd.cds.steer.experience_rating.raw_data
    data_mapping = hxd.cds.steer.experience_rating.data_mapping
    fvy = hxd.cds.steer.experience_rating.other_fields.fvy.value
    lvy = hxd.cds.steer.experience_rating.other_fields.lvy.value
    closed_indicator = hxd.cds.steer.experience_rating.misc_parameters.closed_indicator
    target_year = hxd.cds.steer.experience_rating.misc_parameters.target_year
    ms = hxd.model_state

    # async_output nodes
    pre_val_err_messages = hxd.cds.steer.experience_rating.raw_data_error.pre_val_err_messages
    show_pre_val_err_messages = hxd.cds.steer.experience_rating.raw_data_error.show_pre_val_err_messages
    accepted_missing_value_list = hxd.cds.steer.experience_rating.raw_data_error.accepted_missing_value
    field_type_list = hxd.cds.steer.experience_rating.raw_data_error.field_type
    value_within_range_list = hxd.cds.steer.experience_rating.raw_data_error.value_within_range
    
    raw_data_df = pd_df_from_hx_list(raw_data)
    # Re-order columns based on the numeric part of the column name
    raw_data_df = raw_data_df[
        sorted(
            raw_data_df.columns,
            key=lambda x: int(x.split("_")[1])
        )
    ]

    pre_val_err_mess_list = []
    show_pre_val_err_messages = False

    # first_row = raw_data_df.iloc[0]  # Get the first row of raw_data as a Series
    first_row = raw_data_df.head(1).iloc[0]
    
    is_raw_data_missing = first_row.isna().all() or (first_row == "").all()
    # check if raw_data is empty
    if is_raw_data_missing:
        append_error_message(pre_val_err_mess_list,"Page: Raw Data, Section: Raw data Input - No data found. Please paste your data.")
    # Check if fvy is empty
    if not fvy:
        append_error_message(pre_val_err_mess_list,"Page: Data Format, Section: Misc Parameters - First Year Of Data Valuation cannot be empty.")
    # Check if fvy is a four-digit number
    elif not (len(str(fvy)) ==4):
        append_error_message(pre_val_err_mess_list,"Page: Data Format, Section: Misc Parameters - First Year Of Data Valuation must be a four-digit number.")
    # Check if lvy is empty
    if not lvy:
        append_error_message(pre_val_err_mess_list,"Page: Data Format, Section: Misc Parameters - Last Year Of Data Valuation cannot be empty.")
    # Check if lvy is a four-digit number
    elif not (len(str(lvy)) ==4):
        append_error_message(pre_val_err_mess_list,"Page: Data Format, Section: Misc Parameters - Last Year Of Data Valuation must be a four-digit number.")
    # check Closed Indicator is provided
    if closed_indicator =="":
        append_error_message(pre_val_err_mess_list,"Page: Data Format, Section: Misc Parameters - Closed Indicator cannot be empty.")
    # Validation of Last year vs First year
    num_of_years = (lvy - fvy) + 1 if lvy is not None and fvy is not None else 0
    if num_of_years <= 0:
        append_error_message(pre_val_err_mess_list,"Page: Data Format, Section: Misc Parameters - Last Year Of Data Valuation must be > First Year Of Data Valuation.")
    if lvy is not None and target_year is not None and lvy > target_year:
        append_error_message(pre_val_err_mess_list,"Page: Data Format, Section: Misc Parameters - Last Year Of Data Valuation must be < Target Year.")
    
    # get Max column count
    raw_data_max_column = max_non_empty_column_count(raw_data_df)
    
    for index, field in enumerate(data_mapping):
        # Check if specify_column inputs have been provided for mandatory fields
        if field[1].mandatory_column=="Yes" and field[1].specify_column is None:
            append_error_message(pre_val_err_mess_list,f"Page: Data Format, Section: Raw Data Mapping - Provide 'Specify Column' for {field[1].field_name}.")
        # Check if specify_column inputs relate to raw_data column
        if field[1].specify_column is not None and field[1].specify_column > raw_data_max_column and raw_data_max_column !=0:
            append_error_message(pre_val_err_mess_list,f"Page: Data Format, Section: Raw Data Mapping - Provide 'Specify Column' for {field[1].field_name} within 1 and {raw_data_max_column}.")
        # Check if specify_column inputs are within range for the last developmnent
        if field[1].description =="Specify first column" and field[1].specify_column is not None and field[1].specify_column > (raw_data_max_column - (lvy - fvy)):
            append_error_message(pre_val_err_mess_list,f"Page: Data Format, Section: Raw Data Mapping - The 'Specify Column' for {field[1].field_name} assumes that more columns should be provided in the raw data. Revise the 'Specify Column' or add missing columns.")
        

    # Check empty column name in the first row of raw data
    _steer_check_raw_data_empty_column(raw_data_df,pre_val_err_mess_list)
    # Check that there are no duplicates in data_mapping specify column
    _steer_check_specify_column_duplicates(data_mapping,pre_val_err_mess_list)

    # status for first column data point provided 
    is_first_column_of_data_point_provided = any(
        field[1].description == "Specify first column" and field[1].specify_column is not None
        for field in data_mapping
    )

    if is_first_column_of_data_point_provided:
        # expand data mapping with multiple data point
        tbl_data_mapping = _expand_data_point_data_mapping(tbl_data_mapping,data_mapping,num_of_years)
        # check duplicated in triangles columns in tbl_data_mapping
        _check_specify_columns_duplicates(tbl_data_mapping, pre_val_err_mess_list)
    

    # Compile all error messages into a single string
    if pre_val_err_mess_list:
        hxd.cds.steer.experience_rating.raw_data_error.pre_val_err_messages = "\n".join(pre_val_err_mess_list)
        hxd.cds.steer.experience_rating.raw_data_error.show_pre_val_err_messages = True
        return # exit the function if mandatory data above not provided

    # uncomment to show all columns of a dataframe in the console
    pd.set_option('display.max_columns', None) 

    if not(is_raw_data_missing): # if raw_data provided
        # # Extract headers and data
        headers = raw_data_df.head(1)
        data = raw_data_df.tail(-1)

        # Find columns where the first row is not an empty string
        # non_empty_columns = first_row[first_row.astype(str).str.strip() != ""].index.tolist()
        
        # Filter columns to include only non-empty ones, preserving the original order
        non_empty_columns = [
            col for col in raw_data_df.columns.tolist()
            if first_row.astype(str).str.strip().loc[col] != ""
        ]
        
        # reduced_headers = headers[non_empty_columns]
        reduced_headers = headers[non_empty_columns]
        reduced_data = data[non_empty_columns]

        new_column_names = reduced_headers.iloc[0].tolist()
        result_df = reduced_data.copy() 

        result_df.columns = new_column_names                

        # check if there are empty rows
        empty_row_indices = find_empty_rows(result_df)
        if empty_row_indices:
            append_error_message(pre_val_err_mess_list,f"Page: On levelling, Section: Raw Data - Remove empty rows {', '.join(map(str,empty_row_indices))}.")
        
        # check uniqueness of the raw_data columns names
        duplicated_columns = find_duplicate_columns(result_df)
        if duplicated_columns:
            append_error_message(pre_val_err_mess_list,f"Page: On levelling, Section: Raw Data - Rename columns with same name: {', '.join(map(str,duplicated_columns))}.")

        if pre_val_err_mess_list:
            hxd.cds.steer.experience_rating.raw_data_error.pre_val_err_messages = "\n".join(pre_val_err_mess_list)
            hxd.cds.steer.experience_rating.raw_data_error.show_pre_val_err_messages = True
        
            ms.is_steer_raw_data_validated = False
            return # Exit function



        # Initialise dataframe
        field_type_df = pd.DataFrame(columns=["requirement", "column_name", "cell_address", "value_found"])
        accept_missing_value_df = pd.DataFrame(columns=["requirement", "column_name", "cell_address", "value_found"])
        value_within_range_df = pd.DataFrame(columns=["requirement", "column_name", "cell_address", "value_found"])

        # clean and convert raw_data data to format provided in data mapping, add mapping to raw_data column name - result_df - in tbl_data mapping
        converted_result_df, augmented_tbl_data_mapping, field_type_df = _convert_format(result_df, tbl_data_mapping)
        
        # Replace missing by default values even on multiple data point
        result_df_with_default  = _replace_with_default(converted_result_df,augmented_tbl_data_mapping)

        # Get closed indicator list used in raw_data. Not used
        # _check_closed_indicator_used(converted_result_df,augmented_tbl_data_mapping,pre_val_err_mess_list,closed_indicator)

        accept_missing_value_df = _check_missing_value_errors(converted_result_df, augmented_tbl_data_mapping)

        value_within_range_df, errors = _check_value_within_range_errors(converted_result_df, augmented_tbl_data_mapping,target_year)
        
        value_within_range_df = _check_claims_relation(converted_result_df, augmented_tbl_data_mapping,value_within_range_df,num_of_years,result_df)

        # write error in UI
        output_columns_str = ["requirement", "column_name", "cell_address", "value_found"]

        field_type_df[output_columns_str ] = field_type_df[output_columns_str ].fillna('')
        accept_missing_value_df[output_columns_str ] = accept_missing_value_df[output_columns_str ].fillna('')
        value_within_range_df[output_columns_str ] = value_within_range_df[output_columns_str ].fillna('')

        field_type = field_type_df.to_dict('records')
        accept_missing_value = accept_missing_value_df.to_dict('records')
        value_within_range = value_within_range_df.to_dict('records')

        hxd.cds.steer.experience_rating.raw_data_error.field_type = field_type
        hxd.cds.steer.experience_rating.raw_data_error.accepted_missing_value = accept_missing_value
        hxd.cds.steer.experience_rating.raw_data_error.value_within_range = value_within_range

        if not (field_type ==[] and accept_missing_value ==[] and value_within_range==[]):
            append_error_message(pre_val_err_mess_list,f"Page: Raw Data Error, Section: Raw Data Error - correct data issue and press 'Format Data' again.")
        
        if pre_val_err_mess_list:
            hxd.cds.steer.experience_rating.raw_data_error.pre_val_err_messages = "\n".join(pre_val_err_mess_list)
            hxd.cds.steer.experience_rating.raw_data_error.show_pre_val_err_messages = True
        
            ms.is_steer_raw_data_validated = False
        else:
            ms.is_steer_raw_data_validated = True
            return converted_result_df, augmented_tbl_data_mapping, num_of_years

    return

def max_non_empty_column_count(raw_data_df):
    """
    Calculate the maximum number of non-empty values in any row of the DataFrame.

    Args:
        raw_data_df (pd.DataFrame): Input DataFrame.

    Returns:
        int: Maximum number of non-empty values in any row.
    """
    # Check for non-empty values (non-NaN and non-empty strings)
    non_empty_df = raw_data_df.notna() & (raw_data_df != '')

    # Calculate the number of non-empty values for each row
    non_empty_counts = non_empty_df.sum(axis=1)

    # Get the maximum count
    max_count = non_empty_counts.max()

    return max_count

def _steer_check_raw_data_empty_column(raw_data_df,pre_val_err_mess_list):
    """
    Check that all columns with data in raw_data_df have a column name
    """
    # Check non-empty values in the first row
    first_row_non_empty = raw_data_df.iloc[0].notna() & (raw_data_df.iloc[0].astype(str).str.strip() != "")

    # Check non-empty values in the rest of the DataFrame
    rest_non_empty = raw_data_df.iloc[1:].notna() & (raw_data_df.iloc[1:].astype(str) != "")

    # Count non-empty values in the first row
    first_row_count = first_row_non_empty.sum()

    # Count the maximum number of non-empty values in any row of the rest of the DataFrame
    rest_max_count = rest_non_empty.sum(axis=1).max()
    
    # Define Max column count
    max_non_empty_count = max(first_row_count, rest_max_count)

    # Check if the first row has less column than the rest of the data
    if first_row_count <= rest_max_count:
        # Identify columns where the first row has empty values but the rest of the DataFrame has non-empty values
        empty_in_first = ~first_row_non_empty
        non_empty_in_rest = rest_non_empty.any(axis=0)

        missing_columns = empty_in_first & non_empty_in_rest

        if missing_columns.any():
            # The first row is missing non-empty values in the following columns:")
            for col in raw_data_df.columns[missing_columns]:
                print(f"- {col}")
                append_error_message(pre_val_err_mess_list,f"Page: On Levelling, Section: Raw data Input - Provide Column name in row 1 {col}.")
    return max_non_empty_count

def _steer_check_specify_column_duplicates(data_mapping,pre_val_err_mess_list):
    # Extract specify_column values
    specify_columns = [field[1].specify_column for index, field in enumerate(data_mapping) if field[1].specify_column is not None]

    # Check for duplicated entry in specify_column
    specify_col_duplicates = set([col for col in specify_columns if specify_columns.count(col) > 1])

    if specify_col_duplicates:
        for col in specify_col_duplicates:
            # Find field names with the duplicate column number
            duplicate_fields = [field[1].field_name for index, field in enumerate(data_mapping) if field[1].specify_column == col]
            append_error_message(pre_val_err_mess_list,f"Page: Data Format, Section: Raw Data Mapping - Column number {col} is assigned to multiple fields: {', '.join(duplicate_fields)}. Duplicate assignments are not allowed" )

def _expand_data_point_data_mapping(tbl_data_mapping,data_mapping,num_of_years):
    """
    Expands the tbl_data_mapping DataFrame by adding a 'specify_column' column and new rows
    for items where "Description" is "Specify first column".

    Args:
        tbl_data_mapping (pd.DataFrame): DataFrame containing the mapping data.
        data_mapping (hx structure): Structure containing node_name and specify_column information.

    Returns:
        pd.DataFrame: Expanded DataFrame with new rows and 'specify_column' column.
    """
    # Add the 'specify_column' column to tbl_data_mapping
    tbl_data_mapping['specify_column'] = None

    # Create a list to store new rows
    new_rows = []
    # Iterate over each row in tbl_data_mapping
    for index, row in tbl_data_mapping.iterrows():
        node_name = row['node_name']
        # Get the specify_column value from data_mapping
        specify_column_value = getattr(data_mapping,f"{node_name}").specify_column

        # Assign specify_column value to the current row
        tbl_data_mapping.at[index, 'specify_column'] = specify_column_value
        max_field = 18 
        if row['Description'] == "Specify first column":
            # Add new rows for additional columns
            for i in range(1, num_of_years):
                if specify_column_value is not None:
                    new_row = row.copy()
                    max_field = max_field + 1
                    new_row['Field'] = max_field
                    new_row['Field Name'] = f"{row['Field Name']}_{i:02d}"
                    new_row['Description'] = ""  # Clear description for new rows
                    new_row['specify_column'] = i + (specify_column_value or 0)
                    new_rows.append(new_row)
            # rename field name by adding a suffix _00
            row['Field Name'] = f"{row['Field Name']}_{0:02d}"

    # Append new rows to tbl_data_mapping
    if new_rows:
        tbl_data_mapping = pd.concat([tbl_data_mapping, pd.DataFrame(new_rows)], ignore_index=True)

    return tbl_data_mapping

def _check_specify_columns_duplicates(tbl_data_mapping, pre_val_err_mess_list ):
    """
    Check for duplicate values in the 'specify_column' of tbl_data_mapping.
    If duplicates are found, print a message for each duplicate 'Field Name'.

    Args:
        tbl_data_mapping (pd.DataFrame): DataFrame containing the mapping data.
    """
    # Filter out rows where 'specify_column' is None
    non_none_rows = tbl_data_mapping[tbl_data_mapping['specify_column'].notna()]
    # Check for duplicates in 'specify_column'
    duplicates = non_none_rows[non_none_rows.duplicated(subset='specify_column', keep=False)]

    if not duplicates.empty:
        # Group duplicates by 'specify_column' and get the corresponding 'Field Name' values
        for column_value, group in duplicates.groupby('specify_column'):
            field_names = group['Field Name'].tolist()
            append_error_message(pre_val_err_mess_list,f"Page: Data Format, Section: Raw Data Mapping - Please review the first year column for {', '.join(field_names)} and ensure all historical years are provided.")


def _convert_format(result_df, tbl_data_mapping):
    """
    Join column name from raw_data - result_df_name - to tbl_data_mapping
    Remove special character from result_df Data
    Convert result_df column to intended format from tbl_data_mapping
    """
    # Define a mapping from "Field Type" to pandas data types
    field_type_to_pandas = {
        "String": "str",
        "Date": "datetime64[ns]",
        "Integer": "Int64",
        "Decimal": "float64"
        
    }
    # add column 'result_df_name' to tbl_data_mapping
    tbl_data_mapping['result_df_name'] = None

    for index, row in tbl_data_mapping.iterrows():
        specify_column_value = row['specify_column']

        # Get the column name from result_df (1-based index), at the position provided in specify_column
        if specify_column_value is not None:
            result_df_col_name = result_df.columns[specify_column_value - 1]
            tbl_data_mapping.at[index, 'result_df_name'] = result_df_col_name

    # Create a mapping from "result_df_name" to "Field Type"
    # field_mapping = dict(zip(tbl_data_mapping["result_df_name"], tbl_data_mapping["Field Type"]))
    # Create a mapping from "result_df_name" to "Field Type" for each row
    field_mapping = {
        row["result_df_name"]: row["Field Type"]
        for _, row in tbl_data_mapping.iterrows()
    }
   
    # clean data by removing special character based on data type
    cleaned_result_df = clean_special_chars(result_df, field_mapping)


    converted_df = result_df.copy()
    field_type_df = pd.DataFrame(columns=["requirement", "column_name", "cell_address", "value_found"])

    # Iterate over each column in result_df
    for col in cleaned_result_df.columns:
        # Find the corresponding "Field Name" in tbl_data_mapping
        if col in field_mapping:
            field_type = field_mapping[col]
            pandas_type = field_type_to_pandas.get(field_type, "str")

            # Convert the column to the appropriate pandas type
            if pandas_type == "datetime64[ns]":
                # Use the separate date formatting function
                converted_dates, failed_indices = format_uk_date(cleaned_result_df[col])

                if failed_indices:
                    for index in failed_indices:
                        new_row = {
                            "requirement": f"Incorrect date format. Expected UK date format (e.g., 01/12/2023, 01-Dec-2023).",
                            "column_name": col,
                            "cell_address": index+1,
                            "value_found": converted_df.iloc[index-1][col]
                        }
                        field_type_df = pd.concat([field_type_df, pd.DataFrame([new_row])], ignore_index=True)

                converted_df[col] = converted_dates

            elif pandas_type in ["Int64", "float64"]:
                # Check for non-numeric values (letters or other non-numeric characters)
                non_numeric_mask = cleaned_result_df[col].apply(lambda x: bool(re.search(r'[a-zA-Z]', str(x))) if pd.notna(x) else False)

                # Add rows to field_type_df for non-numeric values
                non_numeric_indices = non_numeric_mask[non_numeric_mask].index.tolist()
                if non_numeric_indices:
                    for index in non_numeric_indices:
                        new_row = {
                            "requirement": f"Non-numeric value found. Expected numeric value for column '{col}'.",
                            "column_name": col,
                            "cell_address": index+1,
                            "value_found": cleaned_result_df.iloc[index-1][col]
                        }
                        field_type_df = pd.concat([field_type_df, pd.DataFrame([new_row])], ignore_index=True)

                if pandas_type == "Int64":
                    # converted_df[col] = pd.to_numeric(converted_df[col], errors='coerce').astype("Int64")
                    converted_df[col] = pd.to_numeric(
                        converted_df[col].str.replace(",", ""),
                        errors="coerce"
                    ).astype("Int64")
                elif pandas_type == "float64":
                    # converted_df[col] = pd.to_numeric(converted_df[col], errors='coerce')
                    converted_df[col] = pd.to_numeric(
                        converted_df[col].str.replace(",", ""),
                        errors="coerce"
                    ).astype("float64")
            else:
                converted_df[col] = converted_df[col].astype(str)


    return converted_df, tbl_data_mapping, field_type_df


def clean_special_chars(result_df, column_data_types):
    """
    Removes special characters from each column in result_df based on the intended data type.
    Returns the cleaned DataFrame and a dictionary of characters removed for each column.

    Args:
        result_df (pd.DataFrame): DataFrame with string columns.
        column_data_types (dict): Dictionary mapping column names to intended data types.

    Returns:
        tuple: (cleaned DataFrame, dictionary of characters removed)
    """
    # Define common special characters to remove for each data type
    special_chars_by_type = {
        "String": [
            # Remove whitespace characters
            "\n", "\t", "\r",
        ],
        "Integer": [
            # Remove characters that are not digits or negative signs
            ",", "$","£","€", "%", " ", "\n", "\t", "\r", "+",
        ],
        "Decimal": [
            # Remove characters that are not digits, decimal points, or negative signs
            ",", "$","£","€", "%", " ", "\n", "\t", "\r", "+",
        ],
        "Date": [
            # Remove characters that are not part of standard date formats
            "[", "]", "{", "}", " ", "\n", "\t", "\r",
            # "st", "nd", "rd", "th", # These character will be removed later with regex conditions
        ]
    }

    # Initialize the result dictionary to store removed characters
    chars_removed = {}

    # Create a copy of the DataFrame to avoid modifying the original
    cleaned_df = result_df.copy()

    for col in cleaned_df.columns:
        if col in column_data_types:
            data_type = column_data_types[col]
            chars_to_remove = special_chars_by_type.get(data_type, [])

            # Remove each character from the column
            for char in chars_to_remove:

                cleaned_df[col] = cleaned_df[col].str.replace(char, "", regex=False)

            # Handle ordinal indicators for dates (e.g., "2nd" -> "2")
            if data_type == "Date":
                cleaned_df[col] = cleaned_df[col].str.replace(r'(\d+)\s*(st|nd|rd|th)\s*', r'\1 ', regex=True, flags=re.IGNORECASE)

    return cleaned_df

def format_uk_date(date_series):
    """
    Convert a pandas Series of date strings or Excel integers to datetime objects, handling UK date formats.
    Returns the converted Series and a list of indices where conversion failed.

    Args:
        date_series (pd.Series): Series containing date strings or Excel integers.

    Returns:
        tuple: (converted Series, list of failed indices)
    """
    # Common UK date formats
    uk_date_formats = [
        "%d/%m/%Y",      # 01/12/2023 (day/month/year)
        "%d-%m-%Y",      # 01-12-2023
        "%d %b %Y",      # 01 Dec 2023
        "%d %B %Y",      # 01 December 2023
        "%d/%m/%y",      # 01/12/23
        "%d-%m-%y",      # 01-12-23
        "%d %b %y",      # 01 Dec 23
        "%d %B %y",      # 01 December 23
    ]

    # Initialize the result series and list of failed indices
    converted_dates = pd.Series([pd.NaT] * len(date_series), index=date_series.index)
    failed_indices = []

    # Try to convert each date
    for idx, date_str in date_series.items():
        if pd.isna(date_str):
            continue

        # Remove ordinal indicators (e.g., "5th" -> "5", "1st" -> "1")
        date_str_clean = re.sub(r'(\d+)(st|nd|rd|th)\s*', r'\1 ', str(date_str), flags=re.IGNORECASE)

        # Check if date_str can be converted to an integer (Excel date format)
        try:
            int(float(date_str_clean))
            date_str_clean=int(float(date_str_clean))
            if date_str_clean == 0:
                date_str_clean = "" # Considered as missing value
            converted_date = pd.to_datetime(date_str_clean, origin='1899-12-30', unit='D', errors='raise')
            converted_dates[idx] = converted_date
            continue  # Skip further checks if conversion succeeds
        except (ValueError, TypeError):
            pass  # Not an integer, proceed with string parsing

        # Try to parse as a string date
        try:
            # First try with dateutil.parser (flexible)
            converted_date = parser.parse(str(date_str_clean), dayfirst=True)
            converted_dates[idx] = converted_date
        except (ValueError, TypeError):
            # If parsing fails, try with explicit UK formats
            for date_format in uk_date_formats:
                try:
                    converted_date = pd.to_datetime(date_str_clean, format=date_format, errors='raise')
                    converted_dates[idx] = converted_date
                    break
                except (ValueError, TypeError):
                    continue
            else:
                # If all formats fail, mark as failed
                failed_indices.append(idx)

    return converted_dates, failed_indices

def find_empty_rows(df):
    """
    Check for empty rows in a DataFrame and return their indices.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        list: Indices of empty rows.
    """
    # Check for rows where all values are either NaN or empty strings
    empty_rows_mask = df.isna().all(axis=1) | (df == '').all(axis=1)
    empty_row_indices = df.index[empty_rows_mask].tolist()
    return empty_row_indices

def find_duplicate_columns(df):
    """
    Returns a list of duplicate column names in the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame to check for duplicate column names.

    Returns:
        list: List of duplicate column names.
    """
    duplicate_columns = df.columns[df.columns.duplicated(keep=False)].unique().tolist()
    return duplicate_columns

def _check_missing_value_errors(result_df, tbl_data_mapping):
    """
    Check for missing values in result_df based on tbl_data_mapping.

    Args:
        result_df (pd.DataFrame): DataFrame to check for missing values.
        tbl_data_mapping (pd.DataFrame): DataFrame containing mapping information.

    Returns:
        dict: A dictionary with column names as keys and lists of indices with missing values as values.
    """
    # Get the column names where "Accept Missing Values" is "No"
    columns_to_check = tbl_data_mapping.loc[
        tbl_data_mapping["Accept Missing Values"] != "Yes", "result_df_name"
    ].tolist()

    # Initialize a list to store (row_index, column_name) tuples for missing values
    missing_values = []

    # Check for missing values in each column
    for col in columns_to_check:
        if col in result_df.columns:
            # Get indices and column name where the value is either empty string or NaN
            missing_rows = result_df[
                (result_df[col] == "") | result_df[col].isna() | (result_df[col] == None) | (result_df[col] == 'None') 
            ]

            # Iterate over the rows with missing values
            for index, row in missing_rows.iterrows():
                missing_values.append((index, col))
    
    accept_missing_value_df=pd.DataFrame(columns=["requirement", "column_name", "cell_address", "value_found"])
    
    for index, col in missing_values:
        new_row = {
            "requirement": f"Missing value not accepted '{col}'.",
            "column_name": col,
            "cell_address": index+1,
            "value_found": result_df.iloc[index-1][col]
        }
        accept_missing_value_df = pd.concat([accept_missing_value_df, pd.DataFrame([new_row])], ignore_index=True)
    
    return accept_missing_value_df


def _replace_with_default(result_df, tbl_data_mapping):
    """
    Replace missing values in result_df with default values specified in tbl_data_mapping.

    Args:
        result_df (pd.DataFrame): DataFrame containing the data to be processed.
        tbl_data_mapping (pd.DataFrame): DataFrame containing mapping information, including
            "result_df_name" (column names in result_df) and "Replace Missing With Default" (default values).

    Returns:
        pd.DataFrame: The modified DataFrame with missing values replaced by default values.
    """
    # Filter tbl_data_mapping to get columns and default values where "Replace Missing With Default" is not empty
    default_mapping = tbl_data_mapping[(tbl_data_mapping["Replace Missing with Default Value"] != "") & (tbl_data_mapping["specify_column"].notna())][["result_df_name", "Replace Missing with Default Value"]]

    if not default_mapping.empty:
        # Iterate over each column and default value pair
        for _, row in default_mapping.iterrows():
            col = row["result_df_name"]
            default_value = row["Replace Missing with Default Value"]

            # Check if the column exists in result_df
            if col in result_df.columns:
                # Replace missing values (NaN or empty string) with the default value
                result_df[col] = result_df[col].replace("", np.nan)  # Convert empty strings to NaN
                # result_df[col] = result_df[col].fillna(float(default_value))  # Replace NaN with default value
                # Convert default_value to float, or use 0.0 if conversion fails
                try:
                    default_value_float = float(default_value)
                except (ValueError, TypeError):
                    default_value_float = 0.0

                # Replace NaN with the float default value
                result_df[col] = result_df[col].fillna(default_value_float)
    return result_df

def _check_value_within_range_errors(result_df, tbl_data_mapping,target_year):
    """
    Check if values in result_df are within specified ranges based on tbl_data_mapping.

    Args:
        result_df (pd.DataFrame): DataFrame containing the data to be checked.
        tbl_data_mapping (pd.DataFrame): DataFrame containing mapping information.
        target_year (int): The target year for range checks.

    Returns:
        list: A list of tuples (row_index, column_name, error_message) for values outside the specified range.
    """
    # Initialize a list to store errors
    errors = []

    # Filter tbl_data_mapping for relevant rows    
    relevant_mapping = tbl_data_mapping[
        tbl_data_mapping["specify_column"].notna() &
        (tbl_data_mapping["Value Within Range"] != "")
    ]
    
    policy_year_name = tbl_data_mapping.loc[tbl_data_mapping['Field Name'] == 'Policy year', 'result_df_name'].values[0]


    value_within_range_df = pd.DataFrame(columns=["requirement", "column_name", "cell_address", "value_found"])

    # Iterate over each relevant row in tbl_data_mapping
    for _, row in relevant_mapping.iterrows():
        col = row["result_df_name"]
        value_range = row["Value Within Range"]
        field_type = row["Field Type"]
        
        # Check if the column exists in result_df
        if col in result_df.columns:
            # Handle Date type
            if field_type == "Date" and value_range == "Policy Year  - Inception Year":
                # Convert the column to datetime
                result_df[col] = pd.to_datetime(result_df[col], errors='coerce')

                # Iterate over each value in the column
                for index, value in result_df[col].items():
                    policy_year = result_df.at[index,policy_year_name]
                    if pd.notna(value) and pd.notna(policy_year):
                        year = value.year
                        
                        # Check if the year is within the range
                        if not (policy_year <= year <= target_year):
                            errors.append((index,col))
                        
                            new_row = {
                                "requirement": f"Date year {year} is not between Policy Year {policy_year} and Target Year {target_year}.",
                                "column_name": col,
                                "cell_address": index+1,
                                # "value_found": result_df.iloc[index-1][col]
                                "value_found": result_df.iloc[index-1][col]
                            }
                            value_within_range_df = pd.concat([value_within_range_df, pd.DataFrame([new_row])], ignore_index=True)
                    
            # Handle Integer type
            elif field_type == "Integer" and value_range == "Policy Year  - Inception Year":
                # Iterate over each value in the column
                for index, value in result_df[col].items():
                    policy_year = result_df.at[index,policy_year_name]
                    if pd.notna(value) and pd.notna(policy_year):
                        
                        # Check if the value is within the range
                        if not (policy_year <= value <= target_year):
                            errors.append((index,col))

                            new_row = {
                                "requirement": f"Integer value {value} is not between Policy Year {policy_year} and Target Year {target_year}.",
                                "column_name": col,
                                "cell_address": index+1,
                                # "value_found": result_df.iloc[index-1][col]
                                "value_found": result_df.iloc[index-1][col]
                            }
                            value_within_range_df = pd.concat([value_within_range_df, pd.DataFrame([new_row])], ignore_index=True)

            # Handle Decimal type
            elif field_type == "Decimal" and value_range == ">=0":
                # Iterate over each value in the column
                for index, value in result_df[col].items():
                    if pd.notna(value):
                        # Check if the value is >= 0
                        if int(value) < 0:
                            errors.append((index,col))
                            new_row = {
                                "requirement": f"Decimal value {value} is less than 0",
                                "column_name": col,
                                "cell_address": index+1,
                                # "value_found": result_df.iloc[index-1][col]
                                "value_found": result_df.iloc[index-1][col]
                                

                            }
                            value_within_range_df = pd.concat([value_within_range_df, pd.DataFrame([new_row])], ignore_index=True)
    return value_within_range_df, errors
    
def _check_claims_relation(df, tbl_data_mapping, value_within_range_df,num_of_years,result_df):
    """
    When indeminity and expenses are provided, check the claim relation is true: claim = indemnity + expenses
    This is done for each data point, incurred/paid.

    Args:
        df (pd.DataFrame): DataFrame containing the data to be checked.
        tbl_data_mapping (pd.DataFrame): DataFrame containing mapping information.
        value_within_range_df (pd.DataFrame): DataFrame for error output
        num_of_years: number of data point in the triangles
    """

    claim_types = ["inc","paid"] # as per data format UI
    for claim_type in claim_types:
        if tbl_data_mapping.loc[tbl_data_mapping['Field Name'] == f'Claim {claim_type}_{0:02d}', "specify_column"].values[0] is not None:
            for index in range(num_of_years):
                # Check if indemnity and cost mapping has been provided
                # if not ((tbl_data_mapping.loc[tbl_data_mapping['Field Name'] == f'Indemnity {claim_type}_{index:02d}', "specify_column"] is not None ) and (tbl_data_mapping.loc[tbl_data_mapping['Field Name'] == f'Defense cost {claim_type}_{index:02d}', "specify_column"] is not None)):
                #     return value_within_range_df
                
                if not ((tbl_data_mapping.loc[tbl_data_mapping['Field Name'] == f'Indemnity {claim_type}_{index:02d}', "specify_column"].iloc[0] is not None ) and (tbl_data_mapping.loc[tbl_data_mapping['Field Name'] == f'Defense cost {claim_type}_{index:02d}', "specify_column"].iloc[0] is not None)):
                    return value_within_range_df

                # Check if claim mapping has been provided
                # if tbl_data_mapping.loc[tbl_data_mapping['Field Name'] == f'Claim {claim_type}_{index:02d}', "specify_column"].items() is not None:
                if tbl_data_mapping.loc[tbl_data_mapping['Field Name'] == f'Claim {claim_type}_{index:02d}', "specify_column"].values[0] is not None:
                    # Get the column names
                    indemnity_col = tbl_data_mapping.loc[tbl_data_mapping['Field Name'] == f'Indemnity {claim_type}_{index:02d}', "result_df_name"].values[0]
                    costs_col = tbl_data_mapping.loc[tbl_data_mapping['Field Name'] == f'Defense cost {claim_type}_{index:02d}', "result_df_name"].values[0]
                    claim_col = tbl_data_mapping.loc[tbl_data_mapping['Field Name'] == f'Claim {claim_type}_{index:02d}', "result_df_name"].values[0]

                    if indemnity_col in df.columns and costs_col in df.columns and claim_col in df.columns:
                        # Check claim relation
                        # mask = (df[indemnity_col] + df[costs_col]) != df[claim_col]
                        # Check claim relation, rounded to 4 decimal places
                        # mask = (
                        #     round(df[indemnity_col] + df[costs_col], 2) !=
                        #     round(df[claim_col], 2)
                        # )
                        mask = (
                            (df[indemnity_col] + df[costs_col]).round(2)
                            .sub(df[claim_col].round(2))
                            .abs()
                            > 0.05
                        )
                        if mask.any():
                            # Get the rows where the relation fails
                            failed_rows = df[mask].index.tolist()
                            for row in failed_rows:
                                new_row = {
                                    "requirement": f"The relation {indemnity_col} + {costs_col} is not equal to {claim_col}.",
                                    # "column_name": f"{indemnity_col}, {costs_col} and {claim_col}",
                                    "column_name": f"{claim_col}",
                                    "cell_address": row+1,
                                    "value_found": f" Found: {result_df.loc[row, claim_col]}, expected: {float(df.loc[row, indemnity_col])+float(df.loc[row, costs_col])}."
                                }
                                value_within_range_df = pd.concat([value_within_range_df, pd.DataFrame([new_row])], ignore_index=True)
    return value_within_range_df

def _check_closed_indicator_used(result_df,tbl_data_mapping,pre_val_err_mess_list, closed_indicator):
    """
    Check that the Closed indicator in the data is unique and consistent with the one entered
    """
    closed_year = tbl_data_mapping[tbl_data_mapping["Field Name"]=="Closed year"]["result_df_name"].values[0]
    claim_status = tbl_data_mapping[tbl_data_mapping["Field Name"]=="Status"]["result_df_name"].values[0]
    if tbl_data_mapping[tbl_data_mapping["Field Name"]=="Closed date"]["result_df_name"].values[0]:
        closed_date = tbl_data_mapping[tbl_data_mapping["Field Name"]=="Closed date"]["result_df_name"].values[0]
    
        # Filter rows where "Closed date" or "Closed year" and not NA or empty strings
        filtered_status = result_df.loc[
            ((result_df[closed_date] != "") &
            (result_df[closed_date].notna())) |
            ((result_df[closed_year] != "") &
            (result_df[closed_year].notna())),
            claim_status
        ]
    else:
        # Filter rows where "Closed date" or "Closed year" and not NA or empty strings
        filtered_status = result_df.loc[
            ((result_df[closed_year] != "") &
            (result_df[closed_year].notna())),
            claim_status
        ]

    # Get the list of status values
    status_list = filtered_status.tolist()

    # # Check if the list is unique
    # unique_status = list(set(status_list))

    # # Check Closed indicator is unique and the same as the one entered
    # if len(unique_status) == 1:
    #     # Check if the unique value is equal to closed_indicator
    #     if unique_status[0] != closed_indicator:
    #         append_error_message(pre_val_err_mess_list,f"Page: Data Format, Section: Misc Parameters - Align the Closed Indicator '{closed_indicator}' to the raw_data status '{unique_status[0]}'.")
    # else:  
    #     append_error_message(pre_val_err_mess_list,f"Page: On Levelling, Section: Raw data Input - Multiple Closed Indicators found in raw data:  '{', '.join(unique_status)}'. Use unique Closed Indicator '{closed_indicator}' to correct the raw data.")
    # return 

    # get the list of status used
    unique_status_list = list(set(status_list))

    closed_indicator_normalized = closed_indicator.strip().lower()
    unique_status_list_normalized = [status.strip().lower() for status in unique_status_list]

    closed_indicator_normalized in unique_status_list_normalized

    # Check Closed indicator is unique and the same as the one entered
    # if not (closed_indicator in unique_status_list):
    
    if not (closed_indicator_normalized in unique_status_list_normalized):
        append_error_message(pre_val_err_mess_list,f"Page: On Levelling, Section: Raw data Input - Ensure Claim status uses the Closed Indicator '{closed_indicator}' in the raw data.")
    return 

def steer_format_raw_data(hxd, progress):
    """
    Format data and populate page Experience which includes:
    raw data information and calculated fields (claims to layer for each layer).
    """
    # Get data from Validation data
    if not steer_validate_raw_data(hxd, progress):
        return

    converted_result_df, augmented_tbl_data_mapping, num_of_years = steer_validate_raw_data(hxd, progress)

    # Initialise variables
    layers = hxd.cds.layers
    coverage_basis = hxd.cds.steer.experience_rating.other_fields.coverage_basis.value
    exposure_assumptions = hxd.cds.steer.experience_rating.on_levelling.exposure_assumptions
    exposure_assumptions_df = pd_df_from_hx_list(exposure_assumptions)

    # Column names
    incurred_capped_col = "incurred_capped"
    incurred_indemnity_capped_col = "incurred_indemnity_capped"
    expenses_capped_col = "expenses_capped"
    trended_claim_col = "trended_claim"
    trended_claim_indemnity_col = "trended_claim_indemnity"
    trended_expenses_col = "trended_expenses"

    closed_year = "closed_year"

    incurred_claim_col = f"incurred_dy_{const.experience_rating_max_years}"
    paid_claim_col = f"paid_dy_{const.experience_rating_max_years}"
    incurred_claim_prev_col = f"incurred_dy_{const.experience_rating_max_years-1}"
    paid_claim_prev_col = f"paid_dy_{const.experience_rating_max_years-1}"
    incurred_expenses_col = f"incurred_expenses_dy_{const.experience_rating_max_years}"
    paid_expenses_col = f"paid_expenses_dy_{const.experience_rating_max_years}"
    incurred_indemnity_col = f"incurred_claim_indemnity_dy_{const.experience_rating_max_years}"
    paid_indemnity_col = f"paid_claim_indemnity_dy_{const.experience_rating_max_years}"
    incurred_indemnity_prev_col = f"incurred_claim_indemnity_dy_{const.experience_rating_max_years-1}"
    paid_indemnity_prev_col = f"paid_claim_indemnity_dy_{const.experience_rating_max_years-1}"


    # initial settings
    lvy = hxd.cds.steer.experience_rating.other_fields.lvy.value
    fvy = hxd.cds.steer.experience_rating.other_fields.fvy.value

    mapping_data_point = {}
    mapping_data_point_prefix = {
        "claim_paid_": "paid_dy_",
        "claim_inc_": "incurred_dy_",
        "defense_cost_paid_": "paid_expenses_dy_",
        "defense_cost_inc_": "incurred_expenses_dy_",
        "indemnity_paid_": "paid_claim_indemnity_dy_",
        "indemnity_inc_": "incurred_claim_indemnity_dy_",
    }

    mvts_cols = [
        "claim_ranking",
        "claim_reference",
        "yoa",
        "status",
        "last_year",
        "this_year",
        "incurred_movement",
        "last_year_on_levelled",
        "this_year_on_levelled",
        "incurred_movement_on_levelled",
    ]

    # Process table mapping
    filtered_tbl_mapping_df = augmented_tbl_data_mapping[augmented_tbl_data_mapping["specify_column"].notna()].copy()
    filtered_tbl_mapping_df.loc[:, "schema_name"] = (
        filtered_tbl_mapping_df["Field Name"]
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    mapping_dict = (
        filtered_tbl_mapping_df
        .dropna(subset=["result_df_name"])
        .set_index("schema_name")["result_df_name"]
        .to_dict()
    )

    schema_raw_data_mapping_dict = {k: v for k, v in mapping_dict.items() if v is not None}
    reverse_schema_raw_data_mapping_dict = {v: k for k, v in mapping_dict.items() if v is not None}

    # Initialise DataFrames
    processed_claims_df = pd.DataFrame(columns=schema_raw_data_mapping_dict.keys())
    claims_mvts_df = pd.DataFrame(columns=mvts_cols)

    # Populate processed_claims_df
    selected_columns = list(schema_raw_data_mapping_dict.values())
    processed_claims_df = converted_result_df[selected_columns].rename(columns=reverse_schema_raw_data_mapping_dict)

    # Initialise output_columns with existing non triangles columns
    output_columns = [
        col for col in processed_claims_df.columns
        if not any(col.startswith(prefix) for prefix in mapping_data_point_prefix.keys())
    ]

    ##### start of Helper functions #####
    def _create_claim_count_columns(df, output_columns, claim_type, num_of_years):
        """Helper function to create claim count columns for a given claim type (incurred or paid). This will become the source of the claim count triangle"""
        for i in range(num_of_years):
            year_index = const.experience_rating_max_years - i
            claim_col = f"{claim_type}_dy_{year_index:02d}"
            count_col = f"{claim_type}_claim_count_dy_{year_index:02d}"
            print(claim_col)
            df[count_col] = df[claim_col].apply(lambda x: 1 if isinstance(x, (int, float)) and x > 0 else 0)
            output_columns.append(count_col)

    def _apply_policy_limit(df, result_col, claim_col, policy_limit_col):
        if policy_limit_col in df.columns:
            df[result_col] = df.apply(lambda row: min(row[claim_col], row[policy_limit_col]), axis=1)
        else:
            df[result_col] = df[claim_col]
        return df

    def _get_inflation_index(df, exposure_df):
        min_uw_year = exposure_df["uw_year"].min()
        df = df.merge(
            exposure_df[["uw_year", "inflation_index"]],
            how="left",
            left_on="policy_year",
            right_on="uw_year"
        )
        missing_years = df["inflation_index"].isnull()
        df.loc[missing_years, "inflation_index"] = exposure_df.loc[
            exposure_df["uw_year"] == min_uw_year, "inflation_index"
        ].values[0]
        df.drop(columns=["uw_year"], inplace=True)
        return df

    def _add_pro_rated_expenses(df, expenses_col, indemnity_col, subject_claim_col, pro_rated_expenses):
        df["pro_rata_ratio"] = np.where(
            df[indemnity_col] == 0,
            0,
            df[expenses_col] / df[indemnity_col]
        )
        df[pro_rated_expenses] = df[subject_claim_col] * df["pro_rata_ratio"]
        return df
    ##### end helper functions #####

    # Rename triangle columns
    for key, value in mapping_data_point_prefix.items():
        if any(col.startswith(key) for col in processed_claims_df.columns):
            for i in range(num_of_years):
                hx_col_name = f"{value}{const.experience_rating_max_years - i}"
                df_col_name = f"{key}{(num_of_years - i - 1):02d}"
                mapping_data_point[df_col_name] = hx_col_name
                output_columns.append(hx_col_name)
                processed_claims_df.rename(columns={df_col_name: hx_col_name}, inplace=True)
            # Create claims count columns
            if key.startswith("claim_inc"):
                _create_claim_count_columns(processed_claims_df, output_columns, "incurred", num_of_years)
            
            if key.startswith("claim_paid"):
                if augmented_tbl_data_mapping.loc[augmented_tbl_data_mapping["Field Name"]=="Claim paid_00","specify_column"].values[0] is not None:
                    _create_claim_count_columns(processed_claims_df, output_columns, "paid", num_of_years) 
    
    # add additional field for completeness in processed_claims_df
    if coverage_basis == "Costs Pro-Rata":
        claim_types = ["inc","paid"]
        for claim_type in claim_types:
            prefix = "incurred" if claim_type == "inc" else "paid"
            last_column_name = f"{prefix}_dy_{const.experience_rating_max_years}"
            if last_column_name not in processed_claims_df.columns:
                for index in range(num_of_years):
                    dev_index = const.experience_rating_max_years - index
                    claim_col = f"{prefix}_dy_{dev_index}"
                    indemnity_col = f"{prefix}_claim_indemnity_dy_{dev_index}"
                    expenses_col = f"{prefix}_expenses_dy_{dev_index}"
                    claim_count_col = f"{prefix}_claim_count_dy_{dev_index}"

                    # Check if columns exist in the DataFrame
                    indemnity_exists = indemnity_col in processed_claims_df.columns
                    expenses_exists = expenses_col in processed_claims_df.columns

                    # Assign 0 if either column does not exist, otherwise sum the columns
                    if indemnity_exists and expenses_exists:
                        processed_claims_df[claim_col] = processed_claims_df[indemnity_col] + processed_claims_df[expenses_col]
                    elif indemnity_exists:
                        processed_claims_df[claim_col] = processed_claims_df[indemnity_col]
                    elif expenses_exists:
                        processed_claims_df[claim_col] = processed_claims_df[expenses_col]
                    else:
                        processed_claims_df[claim_col] = 0

                    # processed_claims_df[claim_col] = processed_claims_df[indemnity_col] + processed_claims_df[expenses_col] 
                    processed_claims_df.loc[processed_claims_df[claim_col] != 0,claim_count_col] = 1
                    
                    output_columns.extend([claim_col, claim_count_col])

    # Apply inflation index
    processed_claims_df = _get_inflation_index(processed_claims_df, exposure_assumptions_df)

    # Add FGU incurred claims and inflated claims
    if coverage_basis == "Costs Exclusive":
        processed_claims_df["incurred_claims"] = processed_claims_df[incurred_indemnity_col]
    # else:
    #     processed_claims_df["incurred_claims"] = processed_claims_df[incurred_claim_col]
    elif coverage_basis == "Costs Inclusive":
        processed_claims_df["incurred_claims"] = processed_claims_df[incurred_claim_col]
    else:
        processed_claims_df["incurred_claims"] = processed_claims_df[incurred_indemnity_col] + processed_claims_df[incurred_expenses_col]

    processed_claims_df["inflated_claims"] = processed_claims_df["incurred_claims"] * processed_claims_df["inflation_index"]

    output_columns.extend(["incurred_claims", "inflated_claims"])

    # Set fields subject to limit
    mapping_coverage_claim_subject_to_limit = {
        "Costs Inclusive": incurred_claim_col,
        "Costs Exclusive": incurred_indemnity_col,
        "Costs Pro-Rata": incurred_indemnity_col,
    }

    claim_subject_to_limit = mapping_coverage_claim_subject_to_limit[coverage_basis]

    # Apply policy limit
    processed_claims_df = _apply_policy_limit(processed_claims_df, incurred_capped_col, claim_subject_to_limit, "policy_limit")

    # Calculate inflated claims
    processed_claims_df[f"{claim_subject_to_limit}_inflated"] = (processed_claims_df[claim_subject_to_limit] * processed_claims_df["inflation_index"])

    processed_claims_df = _apply_policy_limit(processed_claims_df, trended_claim_col, f"{claim_subject_to_limit}_inflated", "policy_limit")

    # add capped indemnity in the dataframe
    if {incurred_indemnity_col}.issubset(processed_claims_df.columns):
        processed_claims_df[incurred_indemnity_capped_col] = processed_claims_df[incurred_capped_col]
        
    # Calculate Trended Expenses
    if {incurred_expenses_col}.issubset(processed_claims_df.columns):
        if coverage_basis == "Costs Pro-Rata":
            processed_claims_df = _add_pro_rated_expenses(processed_claims_df, incurred_expenses_col, incurred_indemnity_col, incurred_capped_col, expenses_capped_col)
            # processed_claims_df[incurred_indemnity_capped_col] = processed_claims_df[incurred_capped_col]
            processed_claims_df[incurred_capped_col] = processed_claims_df[incurred_capped_col] + processed_claims_df[expenses_capped_col]
            
            processed_claims_df = _add_pro_rated_expenses(processed_claims_df, incurred_expenses_col, incurred_indemnity_col, trended_claim_col, trended_expenses_col)
            processed_claims_df[trended_claim_indemnity_col] = processed_claims_df[trended_claim_col] 
            processed_claims_df[trended_claim_col] = processed_claims_df[trended_claim_col] + processed_claims_df[trended_expenses_col]
            # output_columns.extend([incurred_indemnity_capped_col,trended_claim_indemnity_col])
        elif coverage_basis == "Costs Exclusive":
            processed_claims_df[expenses_capped_col] = 0
            # processed_claims_df[incurred_indemnity_capped_col] = processed_claims_df[incurred_capped_col]
            processed_claims_df[incurred_capped_col] = processed_claims_df[incurred_capped_col] + processed_claims_df[expenses_capped_col]
            
            processed_claims_df[trended_expenses_col] = 0
            processed_claims_df[trended_claim_indemnity_col] = processed_claims_df[trended_claim_col] 
            processed_claims_df[trended_claim_col] = processed_claims_df[trended_claim_col] + processed_claims_df[trended_expenses_col]
        else:
            processed_claims_df = _add_pro_rated_expenses(processed_claims_df, incurred_expenses_col, incurred_claim_col, trended_claim_col, trended_expenses_col)
        
        output_columns.append(trended_expenses_col)

    output_columns.extend([incurred_capped_col, trended_claim_col])

    # Set fields subject to RI limit
    mapping_coverage_claim_subject_to_ri_limit = {
        "Costs Inclusive": incurred_capped_col, # incurred capped
        "Costs Exclusive": incurred_indemnity_capped_col, # indemnity capped
        "Costs Pro-Rata": incurred_indemnity_capped_col, # indemnity capped
    }

    # Calculate RI claims
    for idx, layer in enumerate(layers, start=1):
        ri_claim_col = f"ri_claim_layer_{idx:02d}"
        trended_ri_claim_col = f"ri_claim_on_levelled_layer_{idx:02d}"
        ri_expenses_col = f"{expenses_capped_col}_ri_{idx:02d}"
        ri_trended_expenses_col = f"{trended_expenses_col}_ri_{idx:02d}"
        claim_subject_to_ri_limit = f"{mapping_coverage_claim_subject_to_ri_limit[coverage_basis]}"
        ri_claim_count_layer = f"ri_claim_count_layer_{idx:02d}"
        ri_claim_count_on_levelled_layer = f"ri_claim_count_on_levelled_layer_{idx:02d}"
        
        def _calculate_ri_claim(claim_col):
            """
            Apply layer excess and limit to the claim col
            """
            excess_amount = processed_claims_df[claim_col] - layer.excess if layer.excess else processed_claims_df[claim_col]
            return excess_amount.clip(lower=0).clip(upper=layer.limit)

        processed_claims_df[ri_claim_col] = _calculate_ri_claim(claim_subject_to_ri_limit)
        #Calculate inflated claims
        processed_claims_df[f"{claim_subject_to_ri_limit}_inflated"] = processed_claims_df[claim_subject_to_ri_limit] * processed_claims_df["inflation_index"]
        processed_claims_df[trended_ri_claim_col] = _calculate_ri_claim(f"{claim_subject_to_ri_limit}_inflated")
        
        # processed_claims_df[trended_ri_claim_col] = _calculate_ri_claim("trended_claim")

        if coverage_basis == "Costs Pro-Rata":
            processed_claims_df = _add_pro_rated_expenses(processed_claims_df, incurred_expenses_col, incurred_indemnity_col, ri_claim_col, ri_expenses_col)
            processed_claims_df[ri_claim_col] = processed_claims_df[ri_claim_col] + processed_claims_df[ri_expenses_col]
            
            processed_claims_df = _add_pro_rated_expenses(processed_claims_df, incurred_expenses_col, incurred_indemnity_col, trended_ri_claim_col,ri_trended_expenses_col)
            processed_claims_df[trended_ri_claim_col] = processed_claims_df[trended_ri_claim_col] + processed_claims_df[ri_trended_expenses_col]

        # Set to False if ri_claim_col is <= 0 or NA
        processed_claims_df[ri_claim_count_layer] = (processed_claims_df[ri_claim_col].notna() & (processed_claims_df[ri_claim_col] > 0))
        # Set to True if closed_year > 0 and not NA, otherwise False
        processed_claims_df[ri_claim_count_on_levelled_layer] = (processed_claims_df[ri_claim_col].notna() & (processed_claims_df[trended_ri_claim_col] > 0))

        output_columns.extend([ri_claim_col, trended_ri_claim_col,ri_claim_count_layer,ri_claim_count_on_levelled_layer])

    if num_of_years > 1:
        # set claim movement subject premiums
        if coverage_basis == "Costs Exclusive":
            claim_mvts_prev_col = incurred_indemnity_prev_col
            claim_mvts_col = incurred_indemnity_col
        else:
            claim_mvts_prev_col = incurred_claim_prev_col
            claim_mvts_col = incurred_claim_col

        mapping_processed_claim_to_claim_mvts = {
            "reference": "claim_reference",
            "policy_year": "yoa",
            "status": "status",
            f"{claim_mvts_prev_col}": "last_year",
            f"{claim_mvts_col}": "this_year",
            "inflation_index": "inflation_index"
        }

        claims_mvts_df = processed_claims_df[list(mapping_processed_claim_to_claim_mvts.keys())].rename(columns=mapping_processed_claim_to_claim_mvts)

        claims_mvts_df["incurred_movement"] = (claims_mvts_df["this_year"] - claims_mvts_df["last_year"]).astype(float)
        claims_mvts_df["last_year_on_levelled"] = claims_mvts_df["last_year"] * claims_mvts_df["inflation_index"]
        claims_mvts_df["this_year_on_levelled"] = claims_mvts_df["this_year"] * claims_mvts_df["inflation_index"]
        claims_mvts_df["incurred_movement_on_levelled"] = claims_mvts_df["this_year_on_levelled"] - claims_mvts_df["last_year_on_levelled"]

        # Ranking and sorting
        claims_mvts_df["claim_ranking"] = claims_mvts_df["incurred_movement"].rank(ascending=False, method='first')
        processed_claims_df["claim_ranking"] = claims_mvts_df["claim_ranking"]
        claims_mvts_df = claims_mvts_df.sort_values(by="claim_ranking", ascending=True)
        output_columns.append("claim_ranking")

        # Prepare output columns
        mvts_output_columns_str = ["claim_reference", "yoa", "status", "last_year", "this_year"]
        mvts_output_columns_flt = [
            "claim_ranking", "last_year", "this_year", "incurred_movement",
            "last_year_on_levelled", "this_year_on_levelled", "incurred_movement_on_levelled",
        ]

        # Fill NA values
        claims_mvts_df[mvts_output_columns_str] = claims_mvts_df[mvts_output_columns_str].fillna('')
        claims_mvts_df[mvts_output_columns_flt] = claims_mvts_df[mvts_output_columns_flt].fillna(0)
        claims_mvts_df = claims_mvts_df[mvts_output_columns_str + mvts_output_columns_flt]

        # Convert to list of dictionaries and write to hxd
        claim_movements = claims_mvts_df.to_dict('records')
        hxd.cds.steer.experience_rating.claim_movements = claim_movements
    elif num_of_years == 1:
        # set claim movement subject premiums
        if coverage_basis == "Costs Exclusive":
            # claim_mvts_prev_col = incurred_indemnity_prev_col
            claim_mvts_col = incurred_indemnity_col
        else:
            # claim_mvts_prev_col = incurred_claim_prev_col
            claim_mvts_col = incurred_claim_col

        mapping_processed_claim_to_claim_mvts = {
            "reference": "claim_reference",
            "policy_year": "yoa",
            "status": "status",
            # f"{claim_mvts_prev_col}": "last_year",
            f"{claim_mvts_col}": "this_year",
            "inflation_index": "inflation_index"
        }

        claims_mvts_df = processed_claims_df[list(mapping_processed_claim_to_claim_mvts.keys())].rename(columns=mapping_processed_claim_to_claim_mvts)
        claims_mvts_df["last_year"] = 0
        claims_mvts_df["incurred_movement"] = (claims_mvts_df["this_year"] - claims_mvts_df["last_year"]).astype(float)
        
        claims_mvts_df["last_year_on_levelled"] = claims_mvts_df["last_year"] * claims_mvts_df["inflation_index"]
        claims_mvts_df["this_year_on_levelled"] = claims_mvts_df["this_year"] * claims_mvts_df["inflation_index"]
        claims_mvts_df["incurred_movement_on_levelled"] = claims_mvts_df["this_year_on_levelled"] - claims_mvts_df["last_year_on_levelled"]

        # Ranking and sorting
        claims_mvts_df["claim_ranking"] = claims_mvts_df["incurred_movement"].rank(ascending=False, method='first')
        processed_claims_df["claim_ranking"] = claims_mvts_df["claim_ranking"]
        claims_mvts_df = claims_mvts_df.sort_values(by="claim_ranking", ascending=True)
        output_columns.append("claim_ranking")

        # Prepare output columns
        mvts_output_columns_str = ["claim_reference", "yoa", "status", "last_year", "this_year"]
        mvts_output_columns_flt = [
            "claim_ranking", "last_year", "this_year", "incurred_movement",
            "last_year_on_levelled", "this_year_on_levelled", "incurred_movement_on_levelled",
        ]

        # Fill NA values
        claims_mvts_df[mvts_output_columns_str] = claims_mvts_df[mvts_output_columns_str].fillna('')
        claims_mvts_df[mvts_output_columns_flt] = claims_mvts_df[mvts_output_columns_flt].fillna(0)
        claims_mvts_df = claims_mvts_df[mvts_output_columns_str + mvts_output_columns_flt]

        # Convert to list of dictionaries and write to hxd
        claim_movements = claims_mvts_df.to_dict('records')
        hxd.cds.steer.experience_rating.claim_movements = claim_movements

    # Categorize output columns
    string_columns = ["reference", "claimant", "insured", "status"]
    output_columns_str = [col for col in output_columns if any(sc in col.lower() for sc in string_columns)]
    output_columns = [col for col in output_columns if not any(sc in col.lower() for sc in string_columns)]

    output_columns_date = [col for col in output_columns if "date" in col.lower()]
    output_columns = [col for col in output_columns if "date" not in col.lower()]

    output_columns_flt = output_columns

    # Fill NA values in processed_claims_df
    dummy_date = pd.to_datetime(const.dum_old_date, format='%Y%m%d')
    processed_claims_df[output_columns_str] = processed_claims_df[output_columns_str].fillna('')
    processed_claims_df[output_columns_date] = processed_claims_df[output_columns_date].fillna(dummy_date)
    
    processed_claims_df[output_columns_flt] = processed_claims_df[output_columns_flt].fillna(0)

    # Combine and filter columns
    output_columns_combined = output_columns_str + output_columns_date + output_columns_flt
    processed_claims_df = processed_claims_df[output_columns_combined]

    # # Assign value to processed claims
    hxd.cds.steer.experience_rating.processed_claims = processed_claims_df.to_dict('records')

    live_hxd = False if "transient_hxd" in str(type(hxd)) else True
    if live_hxd:    

        # build df with YOA, only triangle column inc/paid and corresponding count, closed status
        steer_triangle_data(hxd,processed_claims_df, fvy, lvy, "incurred", "fgu",coverage_basis)
        steer_triangle_data(hxd,processed_claims_df, fvy, lvy, "paid", "fgu",coverage_basis)

        layers_claims_dfs = steer_calculate_layer_triangles(hxd,processed_claims_df, len(hxd.cds.layers))

        for layer_index in range(len(hxd.cds.layers)):
            layer_name = f"layer_{layer_index+1:02d}"

            steer_triangle_data(hxd,layers_claims_dfs[layer_name], fvy, lvy, "incurred", layer_name,coverage_basis)
            steer_triangle_data(hxd,layers_claims_dfs[layer_name], fvy, lvy, "paid", layer_name,coverage_basis)
        # steer_tri_set_up_triangles_task(hxd, progress)
    # steer_populate_bc_patterns(hxd, progress)

    # ##############################
    # ## Create Data Validation List
    # ##############################    

    # get the task inputs list
    task_data_dict, task_layer_data_list, task_raw_data_list, task_expo_assumptions_list = get_inputs_steer_format_data_task(hxd)
    
    ms = hxd.model_state
    # Save a list in string node in model_state
    ms.data_used_in_steer_format_data_task = str(task_data_dict)
    ms.layer_data_used_in_steer_format_data_task = task_layer_data_list
    ms.raw_data_used_in_steer_format_data_task = task_raw_data_list
    ms.expo_assumptions_data_used_in_steer_format_data_task = task_expo_assumptions_list
    # Save Status for task
    ms.has_run_steer_format_data = True

def steer_tri_set_up_triangles_task(hxd, progress):
    fvy = hxd.cds.steer.experience_rating.other_fields.fvy.value
    lvy = hxd.cds.steer.experience_rating.other_fields.lvy.value
    coverage_basis = hxd.cds.steer.experience_rating.other_fields.coverage_basis.value
    # Assign value to processed claims
    processed_claims_df = pd_df_from_hx_list(hxd.cds.steer.experience_rating.processed_claims)

    # build df with YOA, only triangle column inc/paid and corresponding count, closed status
    steer_triangle_data(hxd,processed_claims_df, fvy, lvy, "incurred", "fgu",coverage_basis)
    steer_triangle_data(hxd,processed_claims_df, fvy, lvy, "paid", "fgu",coverage_basis)

    layers_claims_dfs = steer_calculate_layer_triangles(hxd,processed_claims_df, len(hxd.cds.layers))

    for layer_index in range(len(hxd.cds.layers)):
        layer_name = f"layer_{layer_index+1:02d}"

        steer_triangle_data(hxd,layers_claims_dfs[layer_name], fvy, lvy, "incurred", layer_name, coverage_basis)
        steer_triangle_data(hxd,layers_claims_dfs[layer_name], fvy, lvy, "paid", layer_name, coverage_basis)

    
    
def steer_triangle_data(hxd, df, fvy, lvy, claim_basis, layer_name ,coverage_basis):
    """
    Prepare layer name triangle data for a claim basis. Count will be populated only if layer_name is "fgu"

    """
    def filter_columns(df, exact_names, contained_substrings):
        """
        Returns a DataFrame with columns that either:
        - Exactly match names in `exact_names`, or
        - Contain any substring in `contained_substrings`.

        Parameters:
        - df: pandas DataFrame
        - exact_names: list of str, exact column names to include
        - contained_substrings: list of str, substrings to search for in column names

        Returns:
        - pandas DataFrame with filtered columns
        """
        # Columns that exactly match
        exact_matches = [col for col in df.columns if col in exact_names]

        # Columns that contain any of the substrings
        substring_matches = [
            col for col in df.columns
            if any(substring.lower() in col.lower() for substring in contained_substrings)
        ]

        # Combine both types of matches, removing duplicates
        all_matches = list(set(exact_matches + substring_matches))

        return df[all_matches]

    layer_pre_fix = "ri_layer_" if layer_name != "fgu" else ""

    num_of_dev = lvy - fvy + 1
    # For "Costs Exclusive" coverage, set incurred equal to indeminity
    if (coverage_basis == "Costs Exclusive") and f"{claim_basis}_claim_indemnity_dy_{const.experience_rating_max_years}" in df.columns:
        for year_index in range(num_of_dev):
            year_suffix = f"{const.experience_rating_max_years - year_index}"
            indemnity_col = f"{claim_basis}_claim_indemnity_dy_{year_suffix}"
            claim_col = f"{claim_basis}_dy_{year_suffix}"
            claim_count_col = f"{claim_basis}_claim_count_dy_{year_suffix}"

            df[claim_col] = df[indemnity_col]
            df[claim_count_col] = 0
            df.loc[ df[claim_col] > 0, claim_count_col] = 1
            df[claim_count_col] = df.loc[ df[claim_col] > 0, claim_count_col]
    # elif coverage_basis == "Costs Pro-Rata" and f"{claim_basis}_claim_indemnity_dy_{const.experience_rating_max_years}" in df.columns:
    #     for year_index in range(num_of_dev):
    #             year_suffix = f"{const.experience_rating_max_years - year_index}"
    #             indemnity_col = f"{claim_basis}_claim_indemnity_dy_{year_suffix}"
    #             expenses_col = f"{claim_basis}_expenses_dy_{year_suffix}"
    #             claim_col = f"{claim_basis}_dy_{year_suffix}"
    #             claim_count_col = f"{claim_basis}_claim_count_dy_{year_suffix}"

    #             # Calculate pro-rata expenses
    #             df["pro_rata_pct"] = (
    #                 df[expenses_col]
    #                 .div(df[indemnity_col].where(df[indemnity_col].notna() & df[indemnity_col].ne(0)))
    #                 .fillna(0)
    #             )

    #             # Calculate pro-rated expenses
    #             df["pro_rated_expenses"] = df["pro_rata_pct"] * df[indemnity_col]

    #             df[claim_col] = df[indemnity_col] + df["pro_rated_expenses"]
    #             df[claim_count_col] = 0
    #             df.loc[ df[claim_col] > 0, claim_count_col] = 1
    #             df[claim_count_col] = df.loc[ df[claim_col] > 0, claim_count_col]
    #             # Remove temporary columns
    #             df.pop("pro_rata_pct")
    #             df.pop("pro_rated_expenses")



    exact_names = ["policy_year","status"]

    contained_claim_substrings = [f"{layer_pre_fix}{claim_basis}_dy_"]
    contained_count_substrings = [f"{layer_pre_fix}{claim_basis}_claim_count_dy_"]

    # construct "{claim_basis}_dy_", "YOA", "status"
    claims_tri = filter_columns(df, exact_names, contained_claim_substrings)
    # construct "{claim_basis}_claim_count_dy_", "YOA", "status"
    count_tri = filter_columns(df, exact_names, contained_count_substrings)

    # get claims columns
    claims_columns = [col for col in claims_tri.columns if col.startswith(f'{layer_pre_fix}{claim_basis}_dy_')]
    # Aggregate by 'policy_year' and sum the claims columns
    aggregated_claims_tri = claims_tri.groupby('policy_year')[claims_columns].sum().reset_index().sort_values('policy_year').sort_index(axis=1)

    # get count columns
    count_columns = [col for col in count_tri.columns if col.startswith(f"{layer_pre_fix}{claim_basis}_claim_count_dy_")]
    # Aggregate by 'policy_year' and sum the claims columns
    aggregated_count_tri = count_tri.groupby('policy_year')[count_columns].sum().reset_index().sort_values('policy_year').sort_index(axis=1)

    last_origin_year            = int(aggregated_claims_tri["policy_year"].max())
    # first_origin_year           = int(aggregated_claims_tri["policy_year"].min())
    first_origin_year           = int(lvy - const.experience_rating_max_years+1)

    # num_origin_periods = (last_origin_year - first_origin_year) + 1
    # num_origin_periods = num_dev_periods = max(lvy,last_origin_year)-min(fvy,first_origin_year) + 1
    # num_origin_periods = num_dev_periods = max(const.experience_rating_max_years, max(lvy,last_origin_year)-min(fvy,first_origin_year) + 1)
    num_origin_periods = num_dev_periods = min(const.experience_rating_max_years, lvy-min(fvy,first_origin_year) + 1)
    # num_origin_periods = num_dev_periods = const.experience_rating_max_years

    leap_day                = True if (hxd.hx_core.inception_date.month == 2 and hxd.hx_core.inception_date.day == 29) else False
    first_origin_month          = (hxd.cds.steer.experience_rating.other_fields.data_as_at_date.value.month or hxd.hx_core.inception_date.month)
    first_origin_day            = (hxd.cds.steer.experience_rating.other_fields.data_as_at_date.value.day or hxd.hx_core.inception_date.day) - (1 if leap_day else 0)
    first_origin_date           = datetime.date(first_origin_year,first_origin_month,first_origin_day)


    # tri = hxd.cds.steer.experience_rating.layers.fgu.triangle_projection
    tri_claim = getattr(hxd.cds.steer.experience_rating.layers, layer_name).triangle_projection
    tri_1_ab = tri_claim.tri_1a_raw_data_incurred  if claim_basis == "incurred" else tri_claim.tri_1b_raw_data_paid
    tri_1_ab.origin_period_count = num_origin_periods
    tri_1_ab.dev_period_increment    = 12
    tri_1_ab.dev_period_count = num_dev_periods
    tri_1_ab.first_dev_period = 12

    # triangle > list array for origin periods > Used below as couldnt pass a list:  tri_1_ab.origin_periods = [first_origin_date + relativedelta(years=k) for k in range(last_origin_year-first_origin_year+1)]
    for k in range(tri_1_ab.origin_period_count):
        tri_1_ab.origin_periods[k] = first_origin_date + relativedelta(years=k) 

    if claim_basis == "incurred":
        tri_count = getattr(hxd.cds.steer.experience_rating.layers,layer_name).claim_count
        tri_count_1 = tri_count.tri_1a_raw_data_incurred
        tri_count_1.origin_period_count = num_origin_periods
        tri_count_1.dev_period_increment    = 12
        tri_count_1.dev_period_count = num_dev_periods
        tri_count_1.first_dev_period = 12

        # triangle > list array for origin periods > Used below as couldnt pass a list:  tri_1_target.origin_periods = [first_origin_date + relativedelta(years=k) for k in range(last_origin_year-first_origin_year+1)]
        for k in range(tri_count_1.origin_period_count):
            tri_count_1.origin_periods[k] = first_origin_date + relativedelta(years=k) 


    def populate_triangles(
        num_origin_periods: int,
        aggregated_tri_df: pd.DataFrame,
        fvy:int,
        lvy:int,
        experience_rating_max_years: int,
        col_pre_fix: str,
        hxd_tri
        ) -> dict:
        """
        Retrieve incurred values from a claims triangle DataFrame for each (origin_index, dev_index) pair.

        Args:
            num_origin_periods: Number of origin periods.
            num_dev_periods: Number of development periods.
            aggregated_tri_df: DataFrame containing claims triangle data.
            
            experience_rating_max_years: Maximum years for experience rating (used to construct column names).

        Returns:
            Dictionary with keys as (origin_index, dev_index) tuples and values as incurred amounts.
        """
        # min_origin_period = int(aggregated_tri_df["policy_year"].min())
        # min_origin_period = (int(aggregated_tri_df["policy_year"].min()),lvy-const.experience_rating_max_years+1)
        min_origin_period = lvy-const.experience_rating_max_years+1

        for origin_index in range(num_origin_periods):
            origin_year = int(min_origin_period + origin_index)
            origin_period = datetime.date(origin_year,  first_origin_month,  first_origin_day)
            
            for dev_index in range(num_dev_periods + 1):
                # Define the column name to search
                data_dev = const.experience_rating_max_years - num_dev_periods + origin_index + dev_index+1
              
                claim_col = f'{col_pre_fix}_{(data_dev):02d}'
                
                # Define the dev_period of the triangle
                dev_period = (dev_index + 1) * 12
            
                if dev_period <= num_dev_periods * 12:
                    if claim_col in aggregated_tri_df.columns:
                        mask = aggregated_tri_df['policy_year'] == origin_year
                        if mask.any():
                            # Get the incurred value
                            value = aggregated_tri_df.loc[mask, claim_col].values[0]
                            hxd_tri.cumulative_data[ hxd_tri.origin_periods.index(origin_period), hxd_tri.dev_periods.index(dev_period)] =  value                         
                        else:
                            hxd_tri.cumulative_data[ hxd_tri.origin_periods.index(origin_period), hxd_tri.dev_periods.index(dev_period)] =  0                       

        return

    # populate FGU claims triangles
    populate_triangles(
        num_origin_periods,
        aggregated_claims_tri,
        fvy,
        lvy,
        const.experience_rating_max_years,
        f"{layer_pre_fix}{claim_basis}_dy",
        tri_1_ab 
    )
    
    if claim_basis == "incurred" and layer_name == "fgu":
    # populate FGU claims count triangles
        populate_triangles(
            num_origin_periods,
            aggregated_count_tri,
            fvy,
            lvy,
            const.experience_rating_max_years,
            f"{layer_pre_fix}{claim_basis}_claim_count_dy",
            tri_count_1
        )
    return aggregated_claims_tri, aggregated_count_tri
  
def steer_calculate_layer_triangles(hxd,df,layer_num):
    """
    Calculate layer triangles for each layer based on coverage basis and limits.

    Args:
        hxd: Object containing configuration and layer details.
        df: Input DataFrame with claims data.
        layer_num: Number of layers to process.

    Returns:
        dict: Dictionary of DataFrames, one per layer, with calculated triangles.
    """
    def _get_pre_cap_col(col):
        return (
            col.replace("paid_dy_", "pre_cap_paid_dy_")
            if col.startswith("paid_dy_")
            else col.replace("incurred_dy_", "pre_cap_incurred_dy_")
        )

    def _get_indemnity_col(col):
        return (
            col.replace("paid_dy_", "paid_claim_indemnity_dy_")
            if col.startswith("paid_dy_")
            else col.replace("incurred_dy_", "incurred_claim_indemnity_dy_")
        )
    def _get_expenses_col(col):
        return (
            col.replace("paid_dy_", "paid_expenses_dy_")
            if col.startswith("paid_dy_")
            else col.replace("incurred_dy_", "incurred_expenses_dy_")
        )

    def _get_post_cap_col(col):
        return col.replace("paid_dy_", "post_cap_paid_dy_").replace("incurred_dy_", "post_cap_incurred_dy_")

    def _get_ri_layer_col(col):
        return col.replace("paid_dy_", "ri_layer_paid_dy_").replace("incurred_dy_", "ri_layer_incurred_dy_")

    # Create a copy of the input DataFrame to avoid modifying the original
    df_copy = df.copy()
    coverage_basis = hxd.cds.steer.experience_rating.other_fields.coverage_basis.value
    layers_claims_dfs = {}

    for i in range(layer_num):
        layer_key = f"layer_{i+1:02d}"
        layer_df = df_copy.copy()
        excess = hxd.cds.layers[i].excess
        limit = hxd.cds.layers[i].limit

        for col in layer_df.columns:
            if not col.startswith(("incurred_dy_", "paid_dy_")):
                continue

            pre_cap_col = _get_pre_cap_col(col)
            indemnity_col = _get_indemnity_col(col)
            expenses_col = _get_expenses_col(col)
            post_cap_col = _get_post_cap_col(col)
            ri_layer_col = _get_ri_layer_col(col)

            # Calculate percentage expenses if coverage_basis is "Costs Pro-Rata"
            if coverage_basis == "Costs Pro-Rata" and indemnity_col in layer_df.columns:
                layer_df[f"pct_expenses_{col}"] = (layer_df[expenses_col] / layer_df[indemnity_col]).fillna(0)

            # Assign pre-cap column based on coverage basis
            if coverage_basis == "Costs Inclusive":
                layer_df[pre_cap_col] = layer_df[col]
            elif (coverage_basis == "Costs Exclusive" or coverage_basis == "Costs Pro-Rata") and (indemnity_col in layer_df.columns):
                layer_df[pre_cap_col] = layer_df[indemnity_col]
            else:
                layer_df[pre_cap_col] = layer_df[col]

            # Cap values if policy_limit exists
            if "policy_limit" in layer_df.columns:
                layer_df[post_cap_col] = layer_df[pre_cap_col].clip(upper=layer_df["policy_limit"])
            else:
                layer_df[post_cap_col] = layer_df[pre_cap_col]

            # Calculate RI layer column
            
            layer_df[ri_layer_col] = (layer_df[post_cap_col] - excess).clip(upper=limit, lower=0) if (excess is not None) and (limit is not None) else 0

            # Add expenses if necessary
            if coverage_basis == "Costs Pro-Rata" and f"pct_expenses_{col}" in layer_df.columns:
                layer_df[ri_layer_col] *= (1 + layer_df[f"pct_expenses_{col}"])

        layers_claims_dfs[layer_key] = layer_df

    return layers_claims_dfs
 