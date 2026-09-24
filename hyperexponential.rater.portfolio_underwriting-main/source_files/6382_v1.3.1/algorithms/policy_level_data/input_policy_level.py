import hx
import os
import pandas as pd
import algorithms.rate_utilities as utils
import algorithms.rate_constants as constants
from io import StringIO
from fuzzywuzzy import fuzz, process
from algorithms                                               import parameter_tables_schema as params
from algorithms.policy_level_data.data_cleansing_policy_level import  apply_data_type_fixes
from algorithms.policy_level_data.policy_level_helpers        import import_policy_level_data
from algorithms.claim_level_data.claim_level_helpers          import import_claim_level_data
from algorithms.rate_utilities                                import pd_df_from_hx_list_v2


def check_duplicates_for_renew_columns(hxd):
    col_mapping_df = utils.pd_df_from_hx_list(hxd.cds.policy_level_data_table.unformatted_file_column_mapping)

    # Drop NaNs and reset index to avoid alignment issues
    renew_col_non_na = col_mapping_df["renew_column"].dropna().reset_index(drop=True)

    # Find duplicates in the non-NaN series
    duplicate_mask = renew_col_non_na.duplicated(keep=False)

    # If any duplicates are found, print a warning
    if duplicate_mask.any():
        duplicates = renew_col_non_na[duplicate_mask].unique().tolist()
        hx.errors.validation(f"WARNING: Duplicate values found in 'renew_column' (Policy Level Data): {duplicates}")
        hxd.non_cds.policy_level_data.duplicate_found = True

    else:
        hxd.non_cds.policy_level_data.duplicate_found = False 


def renew_sov_column_mapping_dropdown(hxd): 
    '''
    Populates the Renew column dropdown in the column mapping table for cases when files are not formatted in the correct way for the SOV.
    Removes specific unwanted columns before populating the dropdown.
    '''

    # List of columns to exclude
    cols_to_remove = [
        "Gross Premium Cnv",
        "Net Premium Cnv",
        "Paid Attritional Cnv",
        "Paid Large Cnv",
        "Paid Cat Cnv",
        "Paid Total Cnv",
        "Incurred Attritional Cnv",
        "Incurred Large Cnv",
        "Incurred Cat Cnv",
        "Incurred Total Cnv",
        "Modelled",
        "Selected Lob"
    ]

    # Get all column names
    if hxd.cds.risk_information.is_large_model_mode:
        sov_df = utils.pd_df_from_hx_list(hxd.cds.policy_level_data_table.policy_level_data_grouped)
    else:
        sov_df = utils.pd_df_from_hx_list(hxd.cds.policy_level_data_table.policy_level_data)

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
    hxd.cds.policy_level_data_table.renew_sov_column_dropdown = filtered_columns


def get_column_headers_from_policy_data_csv(hxd):
    '''
    Finds all column names in the unformatted SOV uploaded by the user.
    '''

    renew_sov_column_mapping_dropdown(hxd)

    unformatted_file = hxd.cds.policy_level_data_table.unformatted_sov_file   

    if hxd.cds.policy_level_data_table.use_policy_level_data_grouped:
        sov = hxd.cds.policy_level_data_table.policy_level_data_grouped
    else:
        sov = hxd.cds.policy_level_data_table.policy_level_data
        
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

    hxd.cds.policy_level_data_table.unformatted_file_column_mapping = [{"unformatted_column": file_column} for file_column in df.columns]

    unformatted_column_fuzzy_match(hxd)


def unformatted_column_fuzzy_match(hxd):

    valid_columns = [row.renew_column for row in hxd.cds.policy_level_data_table.renew_sov_column_dropdown if row.renew_column]
    if valid_columns != []:
        for row in hxd.cds.policy_level_data_table.unformatted_file_column_mapping:
            unformatted_column = row.unformatted_column

            if unformatted_column:
                closest_renew_column = process.extractOne(unformatted_column, valid_columns, score_cutoff=50)
                row.renew_column = closest_renew_column[0] if closest_renew_column else None
                

def sov_column_mapping_similarity_score_policy_level(hxd):

    for row in hxd.cds.policy_level_data_table.unformatted_file_column_mapping:
        if row.renew_column and row.unformatted_column:
            row.similarity_score = fuzz.WRatio(row.unformatted_column.lower(), row.renew_column.lower())


def import_policy_data_from_csv(hxd):
    '''
    Replaces column names in the SOV with the Renew column names selected by the user in the column mapping table.
    '''

    found_duplicates = hxd.non_cds.policy_level_data.duplicate_found

    if found_duplicates:
        hx.errors.fatal("Duplicate values found in 'renew_column' (Policy Level Data)")

    unformatted_file = hxd.cds.policy_level_data_table.unformatted_sov_file
    
    column_mapping_df = utils.pd_df_from_hx_list(hxd.cds.policy_level_data_table.unformatted_file_column_mapping)

    df = unformatted_file

    if not unformatted_file.exists:
        hx.errors.fatal("File is not uploaded")

   # Read file into dataframe
    with unformatted_file.open(mode="b") as f:
        if unformatted_file.file_extension == "csv":
            df = pd.read_csv(f, keep_default_na=False)
        elif unformatted_file.file_extension == "xlsx":
            df = pd.read_excel(f)
            
        else:
            hx.errors.fatal(f"Unsupported file extension '{unformatted_file.file_extension}'")


    # Build the rename map
    rename_map = {
        row["unformatted_column"]: row["renew_column"].replace(" ", "_").lower()
        for _, row in column_mapping_df.iterrows()
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

    df = apply_data_type_fixes(df, hxd) 

    is_large_model_mode = hxd.cds.risk_information.is_large_model_mode

    if is_large_model_mode:
        pre_group_policy_data(hxd, df=df)  # When using large model, automatically pre-group claim data
    else:
        hxd.cds.policy_level_data_table.policy_level_data = df.to_dict(orient="records")


def clear_policy_table(hxd):
    """Clears all data from the SOV table."""   
    hxd.cds.policy_level_data_table.use_policy_level_data_grouped = False
    return

def write_policy_claim_data_to_hxd(hxd):
    policy_level_df = import_policy_level_data(hxd)
    claim_level_df = import_claim_level_data(hxd)

    hxd.non_cds.policy_level_data.policy_level_data_df_str = policy_level_df.to_csv(index=False)
    hxd.non_cds.claim_level_data.claim_level_data_df_str = claim_level_df.to_csv(index=False)



def pre_group_policy_data(hxd, df=None):
    # error trap none
    if df is None:
        path_data   = hxd.cds.policy_level_data_table.policy_level_data
        cols        = constants.policy_data_used_inputs
        df          = pd_df_from_hx_list_v2( path_data, cols )

    # specify columns & safety value
    value_cols = [  "gross_premium",        "net_premium",  
                    "paid_attritional",     "paid_large",     "paid_cat",     "paid_total",   
                    "incurred_attritional", "incurred_large", "incurred_cat", "incurred_total" ]
    group_cols = ["account_name", "facility_lob", "yoa", "risk_code", "currency"]
    group_safe = ["[unknown]",    "[unknown]",      0,   "[blank]",   "USD"] 

    # --- ensure all needed GROUP BY columns exist and create missing columns with safety value
    for c,s in zip(group_cols,group_safe):
        if c not in df.columns:   df[c] = s
        else:                     df[c] = df[c].fillna(s)

    # --- ensure all needed VALUE columns exist and create missing columns with zeros
    missing_cols = [c for c in value_cols if c not in df.columns]
    if missing_cols:
        df = df.assign(**{c: 0 for c in missing_cols})

    # force value columns to be numeric, coercing errors, and filling with 0 where na
    df[value_cols]  = df[value_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

    # error trapping bad currency
    fx_rates_df    = params.fx_rates.df() # Currency conversion table  
    allowed_ccy    = fx_rates_df["ccy"].astype(str).str.strip().str.upper().tolist()
    df["currency"] = df["currency"].astype(    str).str.strip().str.upper().where(lambda s: s.isin(set(allowed_ccy)), "USD")

    # group
    df_grouped      = df.groupby(group_cols, dropna=False, as_index=False)[value_cols].sum()

    # assign to hxd
    hxd.cds.policy_level_data_table.policy_level_data_grouped     = df_grouped.to_dict(orient="records")
    hxd.cds.policy_level_data_table.use_policy_level_data_grouped = True


def un_group_policy_data(hxd):
    hxd.cds.policy_level_data_table.use_policy_level_data_grouped = False