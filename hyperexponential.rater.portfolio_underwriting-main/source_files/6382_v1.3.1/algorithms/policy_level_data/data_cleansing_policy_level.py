import pandas as pd
import hx_data_schema as HX
import hx
import numpy as np
from datetime import datetime # Import the datetime class

#This dictionary is the same as the data schema and maps the types
column_type_mapping = {
    "umr": str,
    "policy_reference": str,
    "account_name": str,
    "facility_lob": str,   
    "inception_date": str, 
    "expiry_date": str,
    "yoa": int,
    "month_processed": str,  
    "risk_code": str,
    "currency": str,
    "gross_premium": float,
    "net_premium": float,  
    "paid_attritional": float,
    "paid_large": float,
    "paid_cat": float,
    "paid_total": float,
    "incurred_attritional": float,
    "incurred_large": float,
    "incurred_cat": float,
    "incurred_total": float,  
    "sum_insured_tiv": float,
    "limit_attachment_currency": str,
    "limit": float,
    "attachment": float,
    "primary": str,
    "order_per": float,
    "risk_location": str,
    "industry_type": str,
    "region": str,
    "occupancy_property": str,
    "habitational": str,
    "slip_leader": str,
    "naic_sic": str
    }   



def fix_numeric_values(df, column_name, replacement_log):
    """Fixes numeric values in a vectorized manner and logs replacements."""
    column = df[column_name].astype(str)

    # Remove commas
    comma_mask = column.str.contains(',', na=False)
    comma_count = comma_mask.sum()
    df.loc[comma_mask, column_name] = column.str.replace(',', '', regex=False)

    # Replace non-numeric values with 0
    numeric_col = pd.to_numeric(df[column_name], errors='coerce')
    non_numeric_mask = numeric_col.isna()
    non_numeric_count = non_numeric_mask.sum()
    df.loc[non_numeric_mask, column_name] = 0

    # Ensure float type for consistency
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce').fillna(0)

    # Log replacements
    if comma_count > 0:
        replacement_log.append(f"- Removed commas from {comma_count} value(s) in column '{column_name}'.")
    if non_numeric_count > 0:
        replacement_log.append(f"- Replaced {non_numeric_count} non-numeric value(s) in column '{column_name}' with 0.")

    return df


def reformat_date(date_str):
    """Reformats a date string from 'dd/mm/yyyy' to 'yyyy-mm-dd',
       but only if it's not already in 'yyyy-mm-dd' format.
    """
    try:
        # Attempt to parse the date assuming 'dd/mm/yyyy'
        parts = date_str.split('/')
        if len(parts) == 3:
            day, month, year = parts
            return f"{year}-{month}-{day}"
        else:
            # If parsing as 'dd/mm/yyyy' fails, assume it's already in the correct format
            return date_str 
    except (ValueError, IndexError):
        # Handle cases where parsing fails, assume it's already correct
        return date_str


def apply_data_type_fixes(df: pd.DataFrame, hxd):
    """Applies data type-specific fixes to the DataFrame and tracks replacements."""
    replacement_log = []  # Initialize an empty list to store replacement details

    for column in df.columns:
        if column in column_type_mapping:
            expected_type = column_type_mapping[column]
            if expected_type == str:
                if column == "currency" or column == "risk_code":
                    df.loc[df[column].isna(), column] = None
                    continue

                col_data = df[column]
                missing_count = col_data.isnull().sum()

                if missing_count > 0:
                    df[column] = df[column].fillna("").astype(str)
                    replacement_log.append(f"- Replaced {missing_count} missing value(s) in column '{column}' with an empty string.") 

            elif expected_type in (int, float):
               
                # This creates a list of booleans first, then converts to a Series
                string_mask = pd.Series([isinstance(x, str) for x in df[column]], index=df.index)                
                string_to_numeric_count = string_mask.sum()

                if string_to_numeric_count > 0:
                        # Attempt conversion (non-numeric strings become NaN)
                    df[column] = pd.to_numeric(df[column], errors='coerce')
                    replacement_log.append(
                            f"- Converted {string_to_numeric_count} string value(s) to numeric in column '{column}'. Non-numeric values set to NaN."
                    )

                # Handle missing values post-conversion
                missing_count = df[column].isnull().sum()
                
                if missing_count > 0:
                    df[column] = df[column].fillna(0).astype(expected_type)
                    replacement_log.append(
                        f"- Replaced {missing_count} missing value(s) in column '{column}' with 0."
                    )

                # Final cleanup: remove commas, enforce numeric again
                df = fix_numeric_values(df, column, replacement_log)

                # Ensure final type cast
                df[column] = df[column].astype(expected_type)

                # except Exception as e:
                #     replacement_log.append(
                #         f"- WARNING: Could not convert column '{column}' to {expected_type.__name__}: {e}"
                #     )
            # elif expected_type == "date":
            #     missing_count = df[column].isnull().sum()
            #     if missing_count > 0:
            #         df[column] = df[column].fillna("1900-01-01")                  
            #         replacement_log.append(f"- Replaced {missing_count} missing value(s) in column '{column}' with '1900-01-01'.")
            #     # df[column] = df[column].apply(reformat_date)
            #     replacement_log.append(f"- Changed the date format in {column} to the format 'YYYY-MM-DD'.")


    # Create the message string for replacements
    if replacement_log:
        replacement_message = "The following replacements were made:\n" + "\n".join(replacement_log)
    else:
        replacement_message = "No replacements were made."
    hxd.cds.policy_level_data_table.replacement_log = replacement_message
    return df

