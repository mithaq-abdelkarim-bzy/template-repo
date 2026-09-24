import hx
import os
from fuzzywuzzy import fuzz, process
import pandas as pd
import numpy as np
from io import StringIO
from algorithms.claim_level_data.data_cleansing_claim_level import  apply_data_type_fixes
from algorithms                                             import parameter_tables_schema as params
import algorithms.rate_utilities as utils
import algorithms.rate_constants as constants


def check_duplicates_for_renew_columns(hxd):
    col_mapping_df = utils.pd_df_from_hx_list(hxd.cds.claim_level_data_table.unformatted_file_column_mapping)

    # Identify duplicates in the 'renew_column' (ignoring NaNs)
    duplicate_values = (
        col_mapping_df["renew_column"]
        .dropna()
        .duplicated(keep=False)
    )

    # If any duplicates are found, print a warning
    if duplicate_values.any():
        dupes = (
            col_mapping_df.loc[duplicate_values, "renew_column"]
            .dropna()
            .unique()
            .tolist()
        )
        hx.errors.validation(f"WARNING: Duplicate values found in 'renew_column' (Claim Level Data): {dupes}")
        hxd.non_cds.claim_level_data.duplicate_found = True
    else:
        hxd.non_cds.claim_level_data.duplicate_found = False




def renew_sov_column_mapping_dropdown(hxd):
    '''
    Populates the Renew column dropdown in the column mapping table for cases when files are not formatted in the correct way for the SOV.
    '''
    cols_to_remove = [
        "Paid Cnv",
        "Outstanding Cnv",
        "Incurred Cnv",
        "Modelled",
        "Selected Lob"
    ]

    # Get all column names
    if hxd.cds.risk_information.is_large_model_mode:
        sov_df = utils.pd_df_from_hx_list(hxd.cds.claim_level_data_table.claim_level_data_grouped)
    else:
        sov_df = utils.pd_df_from_hx_list(hxd.cds.claim_level_data_table.claim_level_data)

    all_columns = list(sov_df.columns)

    # Format for dropdown
    drop_down_values = [
        col.replace('_', ' ').title()
           .replace(' Tiv', ' TIV')
           .replace('Bi ', 'BI ')
           .replace('Pd ', 'PD ')
           .replace('Gu ', 'GU ')
           .replace('Yoa', 'YOA')
        for col in all_columns
    ]

    # Filter out the columns to remove
    filtered_columns = [col for col in drop_down_values if col not in cols_to_remove]

    # Assign to dropdown field
    hxd.cds.claim_level_data_table.renew_sov_column_dropdown = filtered_columns
    

def get_column_headers_from_claim_data_csv(hxd):
    '''
    Finds all column names in the unformatted SOV uploaded by the user.
    '''

    renew_sov_column_mapping_dropdown(hxd)

    unformatted_file = hxd.cds.claim_level_data_table.unformatted_sov_file   
    sov = hxd.cds.claim_level_data_table.claim_level_data

    df= unformatted_file
    if not unformatted_file.exists:
        hx.errors.fatal("File is not uploaded")

    # Read file into dataframe
    with unformatted_file.open(mode="b") as f:
        if unformatted_file.file_extension == "csv":
            df = pd.read_csv(f)     
        elif unformatted_file.file_extension == "xlsx":
            df = pd.read_excel(f)
        else:
            hx.errors.fatal(f"Unsupported file extension '{unformatted_file.file_extension}'")

    hxd.cds.claim_level_data_table.unformatted_file_column_mapping = [{"unformatted_column": file_column} for file_column in df.columns]

    unformatted_column_fuzzy_match(hxd)


def unformatted_column_fuzzy_match(hxd):

    valid_columns = [row.renew_column for row in hxd.cds.claim_level_data_table.renew_sov_column_dropdown if row.renew_column]
    if valid_columns != []:
        for row in hxd.cds.claim_level_data_table.unformatted_file_column_mapping:
            unformatted_column = row.unformatted_column

            if unformatted_column:
                closest_renew_column = process.extractOne(unformatted_column, valid_columns, score_cutoff=50)
                row.renew_column = closest_renew_column[0] if closest_renew_column else None
                

def sov_column_mapping_similarity_score_claim_level(hxd):

    for row in hxd.cds.claim_level_data_table.unformatted_file_column_mapping:
        if row.renew_column and row.unformatted_column:
            row.similarity_score = fuzz.WRatio(row.unformatted_column.lower(), row.renew_column.lower())


def import_claim_data_from_csv(hxd):
    '''
    Replaces column names in the SOV with the Renew column names selected by the user in the column mapping table.
    '''

    found_duplicates = hxd.non_cds.claim_level_data.duplicate_found

    if found_duplicates:
        hx.errors.fatal("Duplicate values found in 'renew_column' (Claim Level Data)")

    unformatted_file = hxd.cds.claim_level_data_table.unformatted_sov_file
    
    column_mapping = utils.pd_df_from_hx_list(hxd.cds.claim_level_data_table.unformatted_file_column_mapping)
    sov = hxd.cds.claim_level_data_table.claim_level_data

    df = unformatted_file

    if not unformatted_file.exists:
        hx.errors.fatal("File is not uploaded")

   # Read file into dataframe
    with unformatted_file.open(mode="b") as f:
        if unformatted_file.file_extension == "csv":
            df = pd.read_csv(f)
        elif unformatted_file.file_extension == "xlsx":
            df = pd.read_excel(f)
            
        else:
            hx.errors.fatal(f"Unsupported file extension '{unformatted_file.file_extension}'")

    # Build the rename map
    rename_map = {
        row["unformatted_column"]: row["renew_column"].replace(" ", "_").lower()
        for _, row in column_mapping.iterrows()
        if pd.notna(row["renew_column"])
    }

    # Rename columns
    df.rename(columns=rename_map, inplace=True)

    # Build the target column list (unique, deduplicated)
    desired_columns = list(dict.fromkeys(rename_map.values()))

    # Filter only columns that actually exist in df
    existing_columns = [col for col in desired_columns if col in df.columns]

    # Apply selection safely
    df = df[existing_columns]

    # Determine and apply data type fixes, and get the summary DataFrame
    df = apply_data_type_fixes(df, hxd) 

    is_large_model_mode = hxd.cds.risk_information.is_large_model_mode

    if is_large_model_mode:
        pre_group_claim_data(hxd, df=df)  # When using large model, automatically pre-group claim data
    else:
        hxd.cds.claim_level_data_table.claim_level_data = df.to_dict(orient="records")


def clear_claim_table(hxd):
    """Clears all data from the SOV table."""
    hxd.cds.claim_level_data_table.use_claim_level_data_grouped = False  
    return   
          

def pre_group_claim_data(hxd, df=None):
    if df is None:
        path_data = hxd.cds.claim_level_data_table.claim_level_data
        cols      = constants.claim_data_used_inputs
        df        = utils.pd_df_from_hx_list_v2( path_data, cols )

    # specify columns & safety value
    value_cols = ["paid", "outstanding", "incurred"]
    group_cols = ["facility_lob", "yoa", "claim_status", "risk_code", "currency", "claim_type" ]
    group_safe = ["[unknown]",    0,     "Open",        "[blank]",    "USD",      "Attritional"] 


    # --- ensure all needed GROUP BY columns exist and create missing columns with safety value
    for c,s in zip(group_cols,group_safe):
        if c not in df.columns:   df[c] = s
        else:                     df[c] = df[c].fillna(s)

    # --- ensure all needed VALUE columns exist and create missing columns with zeros
    missing_cols = [c for c in value_cols if c not in df.columns]
    if missing_cols:
        df = df.assign(**{c: 0 for c in missing_cols})

    df[value_cols] = df[value_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

    # error trapping bad claim type labels
    type_map = {
        "CAT":              "CAT",
        "CATASTROPHE":      "CAT",
        "CAT LOSS":         "CAT",
        "LARGE":            "Large",
        "LARGE LOSS":       "Large",
        "LL":               "Large",
        "ATTR":             "Attritional",
        "ATTRITIONAL":      "Attritional",
        "ATTRITIONAL LOSS": "Attritional",
    }
    df["claim_type"] = df["claim_type"].astype(str).str.strip().str.upper().map(type_map).fillna("Attritional")

    # error trapping bad claim status
    status_map = {
        "CLOSED":       "Closed",
        "CLOSE":        "Closed",
        "SETTLED":      "Closed",
        "FINALIZED":    "Closed",
        "FINALISED":    "Closed",
        "PAID":         "Closed",
        "OPEN":         "Open",
        "REOPENED":     "Open",
        "RE-OPENED":    "Open",
        "PENDING":      "Open",
        "REPORTED":     "Open",
        "IN PROGRESS":  "Open",
    }
    df["claim_status"] = df["claim_status"].astype(str).str.strip().str.upper().map(status_map).fillna("Open")

    # error trapping bad currency
    fx_rates_df    = params.fx_rates.df() # Currency conversion table  
    allowed_ccy    = fx_rates_df["ccy"].astype(str).str.strip().str.upper().tolist()
    df["currency"] = df["currency"].astype(    str).str.strip().str.upper().where(lambda s: s.isin(set(allowed_ccy)), "USD")

    # group
    df = df.groupby(group_cols, dropna=False, as_index=False)[value_cols].sum()

    # assign to hxd
    hxd.cds.claim_level_data_table.claim_level_data_grouped     = df.to_dict(orient="records")
    hxd.cds.claim_level_data_table.use_claim_level_data_grouped = True

def un_group_claim_data(hxd):
    hxd.cds.claim_level_data_table.use_claim_level_data_grouped = False