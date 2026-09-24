import pandas as pd
import hx_data_schema as HX
import hx
import numpy as np
from datetime import datetime


# This dictionary maps column names to their expected data types
# (mirrors the schema for claim-level data).
column_type_mapping = {
    "umr": str,
    "policy_reference": str,
    "claim_reference": str,
    "account_name": str,
    "facility_lob": str,  
    "loss_date": str,
    "claim_made_date": str,
    "closed_date": str,
    "month_processed": str, 
    "yoa": int,    
    "claim_status": str,
    "risk_code": str,
    "currency": str,
    "claim_type": str,
    "cat_code": str,
    "paid": float,
    "outstanding": float,
    "incurred": float,  
    "modelled": str
}


def fix_numeric_values(df, column_name, replacement_log):
    """Cleans numeric values by removing commas, handling non-numeric entries,
       converting to float, and logging all replacements.
    """
    column = df[column_name]

    # Find values that contain commas (e.g. "1,000") and count them
    values_with_commas = column[column.astype(str).str.contains(',', na=False)]
    comma_count = len(values_with_commas)

    # Remove commas so numbers can be converted cleanly
    df[column_name] = df[column_name].astype("string").str.replace(',', '')

    # Identify non-numeric values (after comma removal)
    non_numeric_mask = pd.to_numeric(df[column_name], errors='coerce').isna()
    non_numeric_count = non_numeric_mask.sum()

    # Replace non-numeric values with 0
    df.loc[non_numeric_mask, column_name] = "0"

    # Try converting the cleaned column to float
    try:
        df[column_name] = df[column_name].astype(float)
    except ValueError:
        # If conversion fails, log a warning
        replacement_log.append(
            f"- Unable to convert some values in column '{column_name}' to float. Further investigation might be needed."
        )

    # Log replacements made
    if comma_count > 0:
        replacement_log.append(f"- Removed commas from {comma_count} numeric value(s) in column '{column_name}'.")
    if non_numeric_count > 0:
        replacement_log.append(f"- Replaced {non_numeric_count} non-numeric value(s) in column '{column_name}' with 0.")

    return df


def reformat_date(date_str):
    """Reformats a date string from 'dd/mm/yyyy' to 'yyyy-mm-dd'
       if applicable, otherwise returns the input unchanged.
    """
    try:
        # Attempt to split the string into day, month, year
        parts = date_str.split('/')
        if len(parts) == 3:
            day, month, year = parts
            return f"{year}-{month}-{day}"
        else:
            # If it doesn’t look like dd/mm/yyyy, assume it’s already correct
            return date_str 
    except (ValueError, IndexError):
        # If parsing fails, return the input unchanged
        return date_str


def apply_data_type_fixes(df: pd.DataFrame, hxd):
    """Applies type-based cleaning rules to a DataFrame
       and logs all replacements into hxd for transparency.
    """
    replacement_log = []  # Stores details of fixes made

    # Iterate over all columns in the DataFrame
    for column in df.columns:
        if column in column_type_mapping:
            expected_type = column_type_mapping[column]

            # ---- Handle string columns ----
            if expected_type == str:
                if column == "claim_type" or column == "currency":
                    # Leave claim_type and currency as None if missing
                    df.loc[df[column].isna(), column] = None
                    continue

                # Replace missing string values with empty strings
                missing_count = df[column].isnull().sum()
                if missing_count > 0:
                    df[column] = df[column].fillna("").astype(str)
                    replacement_log.append(
                        f"- Replaced {missing_count} missing value(s) in column '{column}' with an empty string."
                    )

            # ---- Handle numeric columns (int, float) ----
            elif expected_type in (int, float):
                try:
                    # Count how many string values exist in numeric columns
                    string_to_numeric_count = sum(isinstance(x, str) for x in df[column])
                    if string_to_numeric_count > 0:
                        # Convert string numbers to the expected type
                        df[column] = df[column].astype(expected_type)
                        replacement_log.append(
                            f"- Converted {string_to_numeric_count} string value(s) to numeric in column '{column}'."
                        )
                except Exception as e:
                    # If conversion fails, log the warning
                    replacement_log.append(
                        f"- WARNING: Could not convert some strings to numeric in column '{column}': {e}"
                    )

                # Fill missing values with 0
                missing_count = df[column].isnull().sum()
                if missing_count > 0:
                    df[column] = df[column].fillna(0).astype(expected_type)
                    replacement_log.append(
                        f"- Replaced {missing_count} missing value(s) in column '{column}' with 0."
                    )

                # Further clean numbers (remove commas, etc.)
                df = fix_numeric_values(df, column, replacement_log)

            # ---- Handle date columns ----
            elif expected_type == "date":
                missing_count = df[column].isnull().sum()
                if missing_count > 0:
                    # Replace missing dates with a default sentinel date
                    df[column] = df[column].fillna("1900-01-01")
                    replacement_log.append(
                        f"- Replaced {missing_count} missing value(s) in column '{column}' with '1900-01-01'."
                    )

                # Optionally reformat dates (commented out currently)
                # df[column] = df[column].apply(reformat_date)
                replacement_log.append(
                    f"- Changed the date format in {column} to the format 'YYYY-MM-DD'."
                )

    # Build the log message (either list of changes or "no changes")
    if replacement_log:
        replacement_message = "The following replacements were made:\n" + "\n".join(replacement_log)
    else:
        replacement_message = "No replacements were made."

    # Save the log into the HxD object for transparency
    hxd.cds.claim_level_data_table.replacement_log = replacement_message

    return df