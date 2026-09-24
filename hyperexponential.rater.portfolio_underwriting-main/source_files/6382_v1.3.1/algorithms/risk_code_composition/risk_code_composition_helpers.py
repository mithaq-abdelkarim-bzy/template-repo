import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import rate_constants as constants
import algorithms.validations.risk_code_composition_validations as validations


def set_rater_type(hxd):
    non_cds_rcc = hxd.non_cds.risk_code_composition
    rcc = hxd.cds.risk_code_composition

    # get from risk information
    prem_data_available = hxd.cds.risk_information.prem_data_available

    calculated_model_type = 'Data' if prem_data_available else 'Manual'
    rcc.model_type.calculated = calculated_model_type

    # set non_cds vars to control view shownby
    selected_type = hxd.cds.risk_code_composition.model_type.selected

    non_cds_rcc.is_manual_and_prem_data_available_true = (prem_data_available and selected_type == 'Manual')

    non_cds_rcc.is_manual = selected_type == 'Manual'
    non_cds_rcc.is_data = selected_type == 'Data'

    return selected_type


def set_dropdown_values(rcc, years_dict):
    rcc.data_driven_composition.year_dropdown = sorted(years_dict.keys())


def set_years_headers(hxd, years_dict):
    for year_attr, year_value in years_dict.items():
        setattr(hxd.non_cds.risk_code_composition, year_value, year_attr)


def get_year_start(rcc, years_dict):
    """ return year end if it has an input value or first year if None"""
    selected_year_start = rcc.data_driven_composition.year_start.selected
    default_year = list(years_dict.keys())[2]
    year_start = (
        selected_year_start
        if selected_year_start is not None 
        else default_year
    )
    # if not rcc.data_driven_composition.year_start.is_overridden:
    rcc.data_driven_composition.year_start.calculated = default_year

    return year_start

def get_year_end(rcc, years_dict):
    """ return year end if it has an input value or first year if None"""
    selected_year_end = rcc.data_driven_composition.year_end.selected
    default_year = list(years_dict.keys())[1]
    year_end = (
        selected_year_end
        if selected_year_end is not None 
        else default_year
    )
    # if not rcc.data_driven_composition.year_end.is_overridden:
    rcc.data_driven_composition.year_end.calculated = default_year

    return year_end


def get_selected_years_array(year_start, year_end, years_dict):
    # Extract keys (years) and values into lists
    keys = list(years_dict.keys())       # e.g. ["2023", "2022", "2021"]
    values = list(years_dict.values())   # corresponding values for each year

    # Define the first and last years based on dict key ordering
    # NOTE: This assumes keys are sorted in descending order (latest → earliest)
    first_year = int(keys[-1])  # the earliest year
    last_year = int(keys[0])    # the latest year

    # If both start and end years are completely outside the known range, return empty
    # Return empty if year range is completely outside [first_year, last_year]
    if max(int(year_start), int(year_end)) < first_year or min(int(year_start), int(year_end)) > last_year:
        return []

    # --- Handle start year ---
    if int(year_start) < first_year:
        # Clamp start to earliest year (index after last element, corrected later by slicing)
        start_year_index = len(values)
    elif int(year_start) >= first_year and int(year_start) <= last_year:
        # Valid year inside range → find its index
        start_year_index = keys.index(str(year_start))
    else:
        return []  # fallback if somehow invalid

    # --- Handle end year ---
    if int(year_end) > last_year:
        # Clamp end to latest year (first index)
        end_year_index = 0
    elif int(year_end) >= first_year and int(year_end) <= last_year:
        # Valid year inside range → find its index
        end_year_index = keys.index(str(year_end))
    else:
        return []  # fallback if somehow invalid

    # Ensure indices are in ascending order so slicing works
    lo, hi = sorted([start_year_index, end_year_index])

    # Slice values inclusively between the start and end year
    years_array = values[lo: hi + 1]

    return years_array


def set_emojis_for_selected_years(hxd, selected_years_array):
    for year_attr in selected_years_array:
        setattr(hxd.non_cds.risk_code_composition, year_attr,
                f"{getattr(hxd.non_cds.risk_code_composition, year_attr, None)} ✅")


def set_premiums_from_policy_level_data(policy_level_df, data_driven_composition_df, premium_base, years_dict):
    # Set the premium column based on the premium_base
    premium_column              = 'net_premium_cnv' if premium_base == "Net" else 'gross_premium_cnv'
    policy_level_df['risk_code']= policy_level_df['risk_code'].fillna('[blank]')
    risk_code_order             = policy_level_df['risk_code'].drop_duplicates().tolist()

    # Group by 'risk_code' and 'year_of_account' and sum the premiums
    grouped_df              = policy_level_df.groupby( ['risk_code', 'facility_lob', 'yoa'], as_index=False)[premium_column].sum()
    grouped_df['risk_code'] = pd.Categorical(  grouped_df['risk_code'], categories=risk_code_order, ordered=True   )

    # Pivot the DataFrame
    pivot_df            = grouped_df.pivot(   index=['risk_code', 'facility_lob'], columns='yoa', values=premium_column).fillna(0)
    pivot_df.columns    = pivot_df.columns.astype(int).astype(str)

    # Rename only the existing columns based on years_dict
    pivot_df = pivot_df.rename(columns=years_dict)

    # Reindex to ensure all desired columns are present, missing ones will be filled with 0
    pivot_df = pivot_df.reindex( columns=years_dict.values(), fill_value=0)

    # Reset index to flatten the DataFrame after pivoting
    pivot_df = pivot_df.reset_index()

    # Remove the name of the columns index (optional cleanup)
    pivot_df.columns.name = None

    # Store the result for further use or merging
    unique_fob_x_risk_code_df = pivot_df

    # Group by risk_code and compute the sum for each numeric year column
    premiums_df       = pivot_df.groupby('risk_code', as_index=False).sum(numeric_only=True)

    # return result_df
    return unique_fob_x_risk_code_df, premiums_df


def merge_with_lloyds_data_and_calculate_composition(premiums_df, unique_fob_x_risk_code_df, risk_code_library, selected_years_array):
    # Calculate total premiums across the selected years for both DataFrames
    premiums_df[              'selected_premium'] = premiums_df[selected_years_array].sum(axis=1)
    unique_fob_x_risk_code_df['selected_premium'] = unique_fob_x_risk_code_df[selected_years_array].sum(axis=1)
    selected_prem_sum                             = premiums_df['selected_premium'].sum()

    # Merge with risk_code_library to check if risk codes exist in Lloyd’s
    rcl_df = risk_code_library[['risk_code', 'do_we_model']]
    premiums_df               = premiums_df.merge(                rcl_df, on='risk_code', how='left'    )
    unique_fob_x_risk_code_df = unique_fob_x_risk_code_df.merge(  rcl_df, on='risk_code', how='left'    )
    
    # Flag whether each row exists in Lloyd’s data
    premiums_df[              'exist_in_lloyds_data_bool'] = premiums_df[              'do_we_model'].fillna('No')
    unique_fob_x_risk_code_df['exist_in_lloyds_data_bool'] = unique_fob_x_risk_code_df['do_we_model'].fillna('No')

    # Calculate composition as a proportion of total selected premium
    nil_prem = selected_prem_sum == 0
    premiums_df['composition']               = 0 if nil_prem else               premiums_df['selected_premium'] / selected_prem_sum
    unique_fob_x_risk_code_df['composition'] = 0 if nil_prem else unique_fob_x_risk_code_df['selected_premium'] / selected_prem_sum

    return unique_fob_x_risk_code_df, premiums_df


def calculate_and_set_total_summations(data_driven_composition_df, years, hxd):
    # Define which columns to aggregate (all years + selected premium)
    cols_to_sum = years + ['selected_premium']

    # Write column totals into the summary object inside HxD
    for col in cols_to_sum:
        setattr(
            hxd.cds.risk_code_composition.data_driven_composition.summary,
            col,
            data_driven_composition_df[col].sum()
        )

    # Build a DataFrame containing the sums for all columns
    sums = data_driven_composition_df[cols_to_sum].sum()
    sums_df = pd.DataFrame(sums).transpose()
    return sums_df


def merge_risk_code_Library(df, lloyds_risk_codes_df, hxd):
    # Keep track of number of original rows so merge doesn’t expand results
    no_of_rows = df.shape[0]

    # Drop existing description column (will be replaced from library)
    df = df.drop(columns=['risk_code_description'])

    # Filter Lloyd’s risk codes down to only those used in df
    filtered_lloyds_risk_codes_df = lloyds_risk_codes_df[
        lloyds_risk_codes_df['risk_code'].isin(df['cs_risk_code'])
    ]

    # Select fields to merge in from risk code library
    fields_to_merge = [
        'risk_code', 'do_we_model', 'assigned_bp_class',
        'assigned_tracker', 'risk_code_description'
    ]

    # Merge df with risk code library using cs_risk_code ↔ risk_code
    df = df.merge(
        filtered_lloyds_risk_codes_df[fields_to_merge],
        left_on='cs_risk_code',
        right_on='risk_code',
        how='left'
    )

    # Flag existence of risk code in data
    df['exists_in_data_bool'] = df['do_we_model'].fillna('No')

    # Calculate default selected business plan class
    df['selected_bp_class/calculated'] = np.where(
        df['assigned_bp_class'].isna(),
        "Not Found",
        df['assigned_bp_class']
    )
    # Respect overrides where present, otherwise use calculated value
    df['selected_bp_class'] = np.where(
        df['selected_bp_class/is_overridden'],
        df['selected_bp_class'],
        df['selected_bp_class/calculated']
    )

    # Adjust tracker assignment based on insured name
    insured_name = hxd.cds.standard_fields.insured_name
    nan_mask = df['assigned_tracker'].notna()

    if insured_name == "AON CLIENT TREATY":
        df.loc[nan_mask, 'assigned_tracker'] = df.loc[nan_mask, 'assigned_tracker'] + " ACT"
    elif insured_name == "MARSH FAST TRACK":
        df.loc[nan_mask, 'assigned_tracker'] = df.loc[nan_mask, 'assigned_tracker'] + " Marsh"

    # Calculate default tracker class
    df['tracker_class/calculated'] = np.where(
        df['assigned_tracker'].isna(),
        "Not Found",
        df['assigned_tracker']
    )
    # Respect overrides where present, otherwise use calculated tracker class
    df['tracker_class'] = np.where(
        df['tracker_class/is_overridden'],
        df['tracker_class'],
        df['tracker_class/calculated']
    )
  
    # Return same number of rows as original df
    return df[:no_of_rows]


def init_composition_selection_from_dcd(unique_fob_x_risk_code_df, rcc, rater):
    # Load the composition selection table from the data model into a DataFrame
    data_composition_selection_df = rater.get("risk_comp_data", pd.DataFrame())

    # Populate with derived data from the unique risk code composition
    data_composition_selection_df['cs_risk_code'] = unique_fob_x_risk_code_df["risk_code"]
    data_composition_selection_df['cs_composition'] = unique_fob_x_risk_code_df["composition"]
    data_composition_selection_df['cs_facility_line_of_business'] = unique_fob_x_risk_code_df["facility_lob"]

    # Columns that should not be disturbed by sorting operations
    non_sorted_fields = [
        'model', 
        'selected_lob',
        'selected_bp_class',
        'tracker_class',
        'selected_bp_class/is_overridden',
        'tracker_class/is_overridden'
    ]

    # Extract a copy of the non-sorted fields
    filtered_model_non_sorted = data_composition_selection_df[non_sorted_fields]

    # Compute the maximum composition value per risk code for sorting
    data_composition_selection_df['max_composition'] = (
        data_composition_selection_df
        .groupby('cs_risk_code')['cs_composition']
        .transform('max')
    )
    
    # Sort by max composition (first) and then composition values, descending
    data_composition_selection_df = data_composition_selection_df.sort_values(
        by=['max_composition', 'cs_composition'],
        ascending=[False, False]
    )
    
    # Drop the temporary max column and reset index
    data_composition_selection_df = data_composition_selection_df.drop(columns='max_composition')
    data_composition_selection_df = data_composition_selection_df.reset_index(drop=True)

    # Restore non-sorted fields into the DataFrame
    data_composition_selection_df[non_sorted_fields] = filtered_model_non_sorted

    # Mark rows as visible only if they have a valid risk code
    data_composition_selection_df['is_row_visible'] = np.where(
        data_composition_selection_df['cs_risk_code'].notna(), True, False)

    return data_composition_selection_df


def reweight_composition(rcc_cs_df, rcc):
    # Ensure cs_composition column is numeric
    rcc_cs_df['cs_composition'] = pd.to_numeric(
        rcc_cs_df['cs_composition'], errors='coerce')

    # Replace NaN with 0 for safety
    rcc_cs_df['cs_composition'].fillna(0, inplace=True)

    # Calculate the total composition for rows flagged as "model=True"
    sum_composition_yes = rcc_cs_df[rcc_cs_df['model'] == True]['cs_composition'].sum()

    # Calculate reweighted composition only for valid, modelled rows
    rcc_cs_df['composition_reweighted'] = rcc_cs_df.apply(
        lambda row: row['cs_composition'] / sum_composition_yes
        if (row['model'] == True
            and row['cs_composition'] > 0
            and sum_composition_yes != 0
            and row['cs_risk_code'] != '')
        else 0, axis=1
    )

    # this is an errortrap for entering risk codes before composition percentages ... without premium data...
    if sum_composition_yes == 0:
        mask_active_risk_code   = rcc_cs_df['risk_code'].notna()
        mask_model              = rcc_cs_df['model'] == True
        mask_model_arc          = mask_active_risk_code & mask_model
        if mask_model_arc.any():
            number = mask_model_arc.sum()
            filler = utils.ratio(1, number)
            rcc_cs_df.loc[mask_model_arc, 'composition_reweighted'] = filler

    return rcc_cs_df


def save_premiums_table(data_driven_composition_df, rcc, years_columns):
    # Define which columns to output to the premiums table
    output_cols_to_write = [
        "risk_code",
        "selected_premium",
        "exist_in_lloyds_data_bool",
        "composition"
    ] + years_columns

    # Subset and persist to the data model
    data_driven_composition_df = data_driven_composition_df[output_cols_to_write]
    rcc.data_driven_composition.premiums_table = data_driven_composition_df.to_dict(orient="records")






def build_data_cs_table(rcc, unique_fob_x_risk_code_df, risk_code_library, hxd, rater):
    # Build the initial composition selection DataFrame
    df = init_composition_selection_from_dcd(
        unique_fob_x_risk_code_df, 
        rcc, 
        rater
    )

    # Merge in fields from the risk code library
    df = merge_risk_code_Library(df, risk_code_library, hxd)

    # Recalculate composition weights
    df = reweight_composition(df, rcc)

    # Calculate total and modelled composition sums
    sum_composition = df['cs_composition'].sum()
    sum_modelled_composition = df[df['model'] == True]['cs_composition'].sum()

    # Calculate modelled percentage of composition
    modelled_percentage = sum_modelled_composition / sum_composition if sum_composition != 0 else 0

    # Save back into rcc
    rcc.data_driven_composition.composition_selection.modelled = modelled_percentage
    
    # Save the selection table to rater
    rater['risk_comp_data']  = df

    return df


def build_manual_cs_table(rcc, lloyds_risk_codes_df, hxd, rater):
    # Load the manual composition table into a DataFrame
    df = rater.get("risk_comp_manual", pd.DataFrame())
    
    # Validate manual risk code and composition values
    validations.check_manual_risk_code_values(df["cs_risk_code"])
    validations.check_manual_composition_values(df[df["cs_risk_code"].notna()]["cs_composition"] )

    # If table is empty or has no valid codes, return as-is
    if df.empty or df["cs_risk_code"].isna().all():
        return df

    # Merge in risk code library details
    df = merge_risk_code_Library(df, lloyds_risk_codes_df, hxd)

    # Recalculate composition weights
    df = reweight_composition(df, rcc)

    # Compute composition totals
    sum_composition = df['cs_composition'].sum()
    sum_modelled_composition = df[df['model'] == True]['cs_composition'].sum()

    # Calculate modelled percentage of composition
    modelled_percentage = sum_modelled_composition / sum_composition if sum_composition != 0 else 0
    rcc.composition_manual.modelled = modelled_percentage

    # Add missing helper columns
    df['cs_facility_line_of_business'] = df['selected_lob']
    df['is_row_visible'] = np.where(df['cs_risk_code'].notna(), True, False)

    # Keep only rows with valid codes - modified 6-feb as code was dropping rows at start if empty in first row and coming misaligned
    # df = df[df["cs_risk_code"].notna()]
    # drop blank rows at end
    mask = df["cs_risk_code"].notna()                       # True where there is data
    if mask.any():
        last_pos = np.where(mask.to_numpy())[0].max()       # integer position
        df = df.iloc[: last_pos + 1]                        # keep up to and including last data row
    else:
        df = df.iloc[0:0]                                   # no data at all -> empty df

    num_cols = df.select_dtypes(include="number").columns
    str_cols = df.select_dtypes(include=["object", "string"]).columns
    df[num_cols] = df[num_cols].fillna(0)
    df[str_cols] = df[str_cols].fillna("")

    # Save manual composition table to rater
    rater['risk_comp_manual'] = df
    
    return df


def build_non_cds_final_selected_composition(hxd, rater, manual_df=None, data_df=None):
    model_type = hxd.cds.risk_code_composition.model_type.selected

    # Final set of columns to keep for export and reporting
    filtered_cols = [
        'risk_code',
        'composition',
        'facility_lob',
        'selected_lob',
        'modelled',
        'selected_bp_class',
        'selected_trifocus',
        'risk_code_description'
    ]

    # Only proceed if manual_df or data_df is provided
    if data_df is None and manual_df is None:
        # raise Exception("returning empty dfs")
        # If no data provided, return empty dataframes
        policy_level_df = pd.DataFrame({})
        claim_level_df = pd.DataFrame({})
        final_df = pd.DataFrame(columns=filtered_cols)
    else:
        # Choose input source depending on model type
        selected_df = manual_df if model_type == 'Manual' else data_df

        # Remove rows with no risk code and reset index
        selected_df = selected_df.dropna(subset=['cs_risk_code'])
        selected_df = selected_df.reset_index(drop=True)

        # Build final dataframe
        final_df                            = pd.DataFrame()
        final_df['risk_code']               = selected_df['cs_risk_code']
        final_df['composition']             = selected_df['composition_reweighted'].fillna(0)
        final_df['facility_lob']            = selected_df['cs_facility_line_of_business']
        final_df['selected_lob']            = selected_df['selected_lob']
        final_df['selected_bp_class']       = selected_df['selected_bp_class']
        final_df['selected_trifocus']       = selected_df['tracker_class']
        final_df['risk_code_description']   = selected_df['risk_code_description']
        final_df['modelled']                = selected_df['model']
        final_df["modelled_string"]         = np.where( final_df['modelled'] == True,  "Yes", "No" )

        # Ensure selected LOB is always a string (no NaN)
        final_df['selected_lob'] = final_df['selected_lob'].fillna(0).astype('string')

        # Update policy-level and claim-level data
        policy_level_df = update_policy_level_lob(final_df, hxd, rater["policy_data"])
        claim_level_df  = update_claim_level_data_lob(final_df, hxd, rater["claim_data"])

        # Replace exact zero compositions with very small positive number
        final_df.loc[final_df['composition'] == 0, 'composition'] = 0.000000000001

        # added 30-jan-26 to filter out blank rows
        mask        = final_df['modelled'] == True
        final_df    = final_df[mask]
        
        # added 6-feb-26 to aggregate where duplicates exist
        num_col     = "composition"
        group_cols  = [c for c in final_df.columns if c != num_col]
        final_df    = final_df.groupby(group_cols, dropna=False, as_index=False).agg({num_col: "sum"})

        # Sort compositions in descending order and reset index
        final_df = final_df.sort_values(by='composition', ascending=False)
        final_df = final_df.reset_index(drop=True)

        # Save output in non-CDS structures
        hxd.non_cds.risk_code_composition.final_composition = final_df[filtered_cols].to_dict(orient="records")

    # Store updated dataframes in rater dict
    rater["policy_data"]            = policy_level_df
    rater["claim_data"]             = claim_level_df
    rater["risk_composition_final"] = final_df

    # Validate that selected LOB values are present
    validations.check_selected_lob_values(final_df[final_df["risk_code"].notna()]["selected_lob"], hxd)


# NOTE: ANY CHANGES MADE TO update_claim_level_data_lob SHOULD ALSO BE MADE TO update_policy_level_lob
def update_policy_level_lob(final_composition_df, hxd, policy_level_df):
    # Drop old 'selected_lob' if present
    policy_level_df = policy_level_df.drop(columns=["selected_lob"], errors="ignore")

    # Risk_code + facility_lob → selected_lob (highest priority)
    policy_risk_code_x_lob_map_df = policy_level_df.merge(
        final_composition_df[["selected_lob", "modelled_string", "facility_lob", "risk_code"]]
        .drop_duplicates(subset=[                                "facility_lob", "risk_code"], keep="first"),
        on=["risk_code", "facility_lob"],
        how="left"
    )

    # Facility_lob → selected_lob (fallback)
    policy_lob_map_df = policy_level_df.merge(
        final_composition_df[["selected_lob", "modelled_string", "facility_lob"]]
        .drop_duplicates(subset=[                                "facility_lob"], keep="first"),
        on=["facility_lob"],
        how="left"
    )

    # Determine masks for what data is actually available
    mask_rc_lob_1 = policy_risk_code_x_lob_map_df["selected_lob"].notna()
    mask_rc_lob_2 = policy_risk_code_x_lob_map_df["selected_lob"] != "0"
    mask_rc_lob   = mask_rc_lob_1 & mask_rc_lob_2

    mask_lob_1    = policy_lob_map_df["selected_lob"].notna()
    mask_lob_2    = policy_lob_map_df["selected_lob"] != "0"
    mask_lob      = mask_lob_1 & mask_lob_2

    # Selected_lob hierarchy: risk_code+lob → lob → "Not Assigned"
    policy_level_df["selected_lob"] = np.where(      mask_rc_lob,    policy_risk_code_x_lob_map_df["selected_lob"]
                                         , np.where( mask_lob,       policy_lob_map_df["selected_lob"]
                                         ,                           "Not Assigned"                               ))

    # Modelled flag hierarchy: risk_code+lob → lob → "No"
    policy_level_df["modelled"] = np.where(      mask_rc_lob,    policy_risk_code_x_lob_map_df["modelled_string"]
                                    , np.where(  mask_lob,       policy_lob_map_df["modelled_string"]
                                        ,                        "No"                                            ))
    policy_level_df["modelled"] = policy_level_df["modelled"].fillna("No")

    return policy_level_df


# NOTE: ANY CHANGES MADE TO update_claim_level_data_lob SHOULD ALSO BE MADE TO update_policy_level_lob
def update_claim_level_data_lob(final_composition_df, hxd, claim_level_df):
    # Drop old 'selected_lob' if present
    claim_level_df = claim_level_df.drop(columns=["selected_lob"], errors="ignore")

    # Risk_code + facility_lob → selected_lob (highest priority)
    claim_risk_code_x_lob_map_df = claim_level_df.merge(
        final_composition_df[["selected_lob", "modelled_string", "facility_lob", "risk_code"]]
        .drop_duplicates(subset=[                                "facility_lob", "risk_code"], keep="first"),
        on=["risk_code", "facility_lob"],
        how="left"
    )

    # Facility_lob → selected_lob (fallback)
    claim_lob_map_df = claim_level_df.merge(
        final_composition_df[["selected_lob", "modelled_string", "facility_lob"]]
        .drop_duplicates(subset=[                                "facility_lob"], keep="first"),
        on=["facility_lob"],
        how="left"
    )

    # Determine masks for what data is actually available
    mask_rc_lob_1 = claim_risk_code_x_lob_map_df["selected_lob"].notna()
    mask_rc_lob_2 = claim_risk_code_x_lob_map_df["selected_lob"] != "0"
    mask_rc_lob   = mask_rc_lob_1 & mask_rc_lob_2

    mask_lob_1    = claim_lob_map_df["selected_lob"].notna()
    mask_lob_2    = claim_lob_map_df["selected_lob"] != "0"
    mask_lob      = mask_lob_1 & mask_lob_2

    # Selected_lob hierarchy: risk_code+lob → lob → "Not Assigned"
    claim_level_df["selected_lob"]  = np.where(      mask_rc_lob,    claim_risk_code_x_lob_map_df["selected_lob"]
                                         , np.where( mask_lob,       claim_lob_map_df["selected_lob"]
                                         ,                           "Not Assigned"                               ))

    # Modelled flag hierarchy: risk_code+lob → lob → "No"
    claim_level_df["modelled"]  = np.where(      mask_rc_lob,    claim_risk_code_x_lob_map_df["modelled_string"]
                                    , np.where(  mask_lob,       claim_lob_map_df["modelled_string"]
                                        ,                        "No"                                            ))
    claim_level_df["modelled"] = claim_level_df["modelled"].fillna("No")
    return claim_level_df
