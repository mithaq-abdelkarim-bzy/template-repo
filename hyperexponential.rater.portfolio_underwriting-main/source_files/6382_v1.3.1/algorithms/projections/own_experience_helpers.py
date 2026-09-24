import hx
from datetime import date
import pandas as pd
import numpy as np
import algorithms.rate_utilities as utils
from algorithms import rate_constants as constants
from algorithms.risk_information.risk_information_helpers import import_inception_date
from dateutil.relativedelta import relativedelta


def cols_exclude_fillna():
    return[ 'development_pattern_premium_override'
            ,'development_pattern_incurred_override'
            , 'ultimate_premium_selected_gnpi_override'
            
            ]


def build_policy_summary_df (policy_level_df):
    """
    Build a summary DataFrame of policy-level data grouped by YOA and LOB.

    Parameters:
    ----------
    policy_level_df : pd.DataFrame   The raw policy dataset containing premium and incurred claim values.

    Returns:
    -------
    pd.DataFrame                    A summary DataFrame with total values grouped by 'yoa' and 'selected_lob'.
    """
    #########################################################################################################
    cols_pol_grp = [ "yoa", "selected_lob"]
    cols_pol_sum = ["gross_premium_cnv",    "incurred_attritional_cnv",   "incurred_large_cnv",   "incurred_cat_cnv",    "incurred_total_cnv" ]
    cols_pol     = cols_pol_grp + cols_pol_sum
    pol_sum_df   = policy_level_df[ cols_pol ].groupby(cols_pol_grp).sum().reset_index()
    return pol_sum_df



def build_claim_summary_df (claim_level_df):
    """
    Build a summary DataFrame of incurred claims by LOB, YOA, claim status, and claim type.
    This function normalizes claim status to 'open' or 'closed', and claim type to 'cat', 'large', or 'attritional'.
    It then aggregates incurred amounts using a crosstab grouped by 'selected_lob' and 'yoa', split by status and type.
    The resulting DataFrame includes total incurred values for open, closed, and overall claims.

    Parameters:
    ----------
    claim_level_df : pd.DataFrame    The raw claims dataset containing 'claim_status', 'claim_type', 'incurred_cnv', 'selected_lob', and 'yoa'.

    Returns:
    -------
    pd.DataFrame                    A summary DataFrame with incurred values split by claim status and type, including total columns.
    """
    #########################################################################################################
    # Normalise claim_status to "closed" or "open"
    claim_level_df["status_normalised"]  = ( claim_level_df["claim_status"]
                                                .fillna("UNKNOWN") 
                                                .str
                                                .upper()
                                                .eq("CLOSED")
                                                .map({True: "closed", False: "open"}))

    # Normalise claim_type to "cat", "attritional", or "large"
    claim_type_dict                     = {"CAT": "cat",    "LARGE": "large",   "ATTRITIONAL": "attritional"}
    claim_level_df["type_normalised"]    = ( claim_level_df["claim_type"]
                                                .fillna("UNKNOWN") 
                                                .str
                                                .upper()
                                                .map(claim_type_dict)
                                                .fillna("attritional")      )
    # cross tab
    claim_sum_df                        = pd.crosstab(  index   = [claim_level_df["selected_lob"], claim_level_df["yoa"]],
                                                        columns = [claim_level_df["status_normalised"], claim_level_df["type_normalised"]],
                                                        values  = claim_level_df["incurred_cnv"],
                                                        aggfunc = "sum"
                                                      ).fillna(0).reset_index()
    
    # drop multi-index on columns
    claim_sum_df.columns                = ['_'.join(col).strip('_') if isinstance(col, tuple) else col for col in claim_sum_df.columns]
    
    # ensure columns exist
    required_cols = ["open_attritional", "open_large", "open_cat","closed_attritional", "closed_large", "closed_cat"]
    for col in required_cols:
        if col not in claim_sum_df.columns:
            claim_sum_df[col] = 0

    # add totals
    claim_sum_df["open_total"]          = utils.safe_sum_cols(claim_sum_df, ["open_attritional",   "open_large",   "open_cat"])
    claim_sum_df["closed_total"]        = utils.safe_sum_cols(claim_sum_df, ["closed_attritional", "closed_large", "closed_cat"])
    
    claim_sum_df["total_attritional"]   = utils.safe_sum_cols(claim_sum_df, ["open_attritional", "closed_attritional"])
    claim_sum_df["total_large"]         = utils.safe_sum_cols(claim_sum_df, ["open_large",       "closed_large"])
    claim_sum_df["total_cat"]           = utils.safe_sum_cols(claim_sum_df, ["open_cat",         "closed_cat"])
    claim_sum_df["total"]               = utils.safe_sum_cols(claim_sum_df, ["open_total",       "closed_total"])
    return claim_sum_df



def set_sum_lob_number(prem_limit_df, summary_df, selected_lob_1, selected_lob_2, selected_lob_3, selected_lob_4, selected_lob_5):
    """
    Assign unique Lines of Business (LOBs) to the summary DataFrame and flag visibility and selection status.

    This function:
    - Extracts unique, non-null LOBs from `prem_limit_df['selected_lob']`
    - Assigns them to the first available rows in `summary_df`
    - Generates sequential LOB numbers starting from 1
    - Flags rows as visible if a LOB is assigned
    - Marks selection status for up to three specified LOBs using boolean flags

    Parameters:
    ----------
    prem_limit_df : pd.DataFrame    Source DataFrame containing premium limit information, including a 'selected_lob' column.
    summary_df : pd.DataFrame       Target DataFrame to be updated with LOB assignments and flags. Must have sufficient rows to accommodate LOBs.
    selected_lob_1 : str            First LOB to flag as selected in the 'selected_lob_1' column.
    selected_lob_2 : str            Second LOB to flag as selected in the 'selected_lob_2' column.
    selected_lob_3 : str            Third LOB to flag as selected in the 'selected_lob_3' column.
    selected_lob_4 : str            fourth LOB to flag as selected in the 'selected_lob_4' column.
    selected_lob_5 : str            fifth LOB to flag as selected in the 'selected_lob_5' column.    

    Returns:
    -------
    pd.DataFrame
        Updated summary DataFrame with:
        - 'selected_lob': assigned LOBs
        - 'lob_number': sequential numbering
        - 'is_row_visible': True for rows with assigned LOBs
        - 'lob_visible_1', 'lob_visible_2', 'lob_visible_3', 'lob_visible_4', 'lob_visible_5': selection flags
        Only rows with non-null 'selected_lob' are retained.
    """
    unique_selected_lobs                    = prem_limit_df['selected_lob'].dropna().unique()
    num_rows                                = summary_df.shape[0]
    num_lobs                                = min(num_rows, unique_selected_lobs.shape[0])
    row_mask                                = summary_df.index[:num_lobs]
    summary_df.loc[row_mask,"selected_lob"] = unique_selected_lobs        
    summary_df.loc[row_mask,"lob_number"]   = range(1, num_lobs + 1)     
    summary_df['yoa']                       = "Total"   
    summary_df["is_row_visible"]            = summary_df["selected_lob"].notna()
    summary_df["lob_visible_1"]             = np.where(summary_df["selected_lob"] == selected_lob_1, True, False)
    summary_df["lob_visible_2"]             = np.where(summary_df["selected_lob"] == selected_lob_2, True, False)
    summary_df["lob_visible_3"]             = np.where(summary_df["selected_lob"] == selected_lob_3, True, False)
    summary_df["lob_visible_4"]             = np.where(summary_df["selected_lob"] == selected_lob_4, True, False)
    summary_df["lob_visible_5"]             = np.where(summary_df["selected_lob"] == selected_lob_5, True, False)
    summary_df                              = summary_df[summary_df["selected_lob"].notna()]
    return summary_df



def calculate_portfolio_profile_summary_by_lob(own_exp_summary, lloyds_summary, beazley_summary,  portfolio_profile_df):
    """
    Calculates weighted average metrics by Line of Business (LOB) and merges them into the own experience summary.

    This function performs the following steps:
    - Subsets relevant columns from Beazley and Lloyds summary datasets.
    - Merges these summaries into the portfolio profile using common keys.
    - Renames columns to standardized output names.
    - Computes weighted averages of selected metrics by LOB.
    - Merges the aggregated results back into the own experience summary.

    Parameters:
    ----------
    own_exp_summary : pd.DataFrame       Own experience summary to be enriched with weighted average metrics.
    lloyds_summary : pd.DataFrame        Summary data from Lloyds containing selected and model IELR and ULR metrics.
    beazley_summary : pd.DataFrame       Summary data from Beazley containing selected ULR metrics.
    portfolio_profile_df : pd.DataFrame  Portfolio profile data containing weights and merge keys.

    Returns:
    -------
    pd.DataFrame        Updated own_exp_summary with weighted average metrics merged by LOB.
    """

    # Map of raw column names → renamed output columns
    cols_map = {'selected_gn_ulr':      'lloyds_final_gn_ulr',
                'selected_ielr':        'lloyds_selected_ielr',
                'model_ielr':           'lloyds_model_ielr',
                'beazley_final_gn_ulr': 'beazley_final_gn_ulr'  }

    # Keys used to merge datasets
    merge_keys = ["selected_lob", "risk_code", "bp_class"]

    # Subset required columns from each dataset
    beazley_summary         = beazley_summary[     merge_keys + ["selected_gn_ulr"]].rename(columns= {'selected_gn_ulr':    'beazley_final_gn_ulr'})
    lloyds_summary          = lloyds_summary[      merge_keys + ["selected_gn_ulr", "selected_ielr", "model_ielr"]]
    portfolio_profile_df    = portfolio_profile_df[merge_keys + ["weighting"]]

    # Merge portfolio profile with Beazley + Lloyds summaries and rename columns
    portfolio_profile_df = (
        portfolio_profile_df
        .merge(beazley_summary, on=merge_keys, how='left')
        .merge(lloyds_summary,  on=merge_keys, how='left')
        .rename(columns=cols_map)
    )


    ## For each metric, calculate a weighted average by LOB and map it back
    # determine columns
    cols        = list(cols_map.values())
    cols_new    = [v + '_weighted' for v in cols]
    cols_merge  = cols + ["selected_lob"] 

    # weight columns
    for field in cols:
        portfolio_profile_df[f"{field}_weighted"] = portfolio_profile_df[field].fillna(0) * portfolio_profile_df["weighting"]

    # group by selected lob summing over columns, resetting index to selected lob is a column not index
    pp_grp_df = portfolio_profile_df.groupby("selected_lob")[   cols_new + ["weighting"]     ].sum().reset_index()
    
    # calc weighting
    for field in cols:
        pp_grp_df[field] = utils.ratio(pp_grp_df[f"{field}_weighted"],   pp_grp_df["weighting"]).fillna(0)
    
    # merge back into own_exp_summary
    own_exp_summary = utils.drop_and_merge(own_exp_summary, pp_grp_df[  cols_merge  ], on="selected_lob")

    return own_exp_summary



def check_policy_data_x_open_claim(summary_df, hxd):
    """
    Checks for invalid 'Open' claim development settings when claim source is 'Policy Level Data',
    adjusts them to 'Open + Closed', and displays an error message via HXD.

    Parameters:
    - summary_df: pd.DataFrame containing claim data.
    - hxd: Object used to display error messages in the UI.

    Returns:
    - pd.DataFrame: Updated summary_df with corrected claim development settings.
    """
    # Build mask for Policy Level Data + "Open" condition
    policy_data_x_open_mask = (
        (summary_df["claim_source"] == "Policy Level Data") & 
        (summary_df["claim_to_develop_to_ultimate"] == "Open")
    )

    if policy_data_x_open_mask.any():  # If invalid condition exists
        # Get affected LOBs
        selected_lobs = summary_df.loc[policy_data_x_open_mask, "selected_lob"].values
        selected_lobs_str = ", ".join(selected_lobs)

        # Build error message
        error_msg = (
            "'Claims to Develop to Ultimate' can only be set to 'Open + Closed' when "
            "'Claim Source' is 'Claim Level Data'. Since that condition isn't met, "
            f"the value has been automatically adjusted for the following LOB(s): {selected_lobs_str}"
        )

        # Display error in HXD
        hxd.non_cds.own_experience.is_error_msg_shown = True
        hxd.cds.projections_own_experience.error_msg = error_msg

        # Force adjustment in summary_df
        summary_df.loc[policy_data_x_open_mask, "claim_to_develop_to_ultimate"] = "Open + Closed"

    return summary_df



def add_yoa_lob_number(detail_df, inception_year, num_yrs):
    """
    Assign 'lob_number' and 'yoa' values to the detailed dataset based on the number of years and inception year.
    This function assumes that the dataset is ordered such that each group of `num_yrs` rows corresponds to a unique
    line of business (LOB). It assigns a sequential 'lob_number' to each group and a repeated 'yoa' (Year of Account)
    ranging from `inception_year - (num_yrs - 1)` to `inception_year`.

    Parameters:
    ----------
    detail_df       : pd.DataFrame      The detailed dataset to be updated.
    inception_year  : int               The most recent year of account.
    num_yrs         : int               The number of years of account to assign per LOB.

    Returns:
    -------
    pd.DataFrame                        The updated DataFrame with 'lob_number' and 'yoa' columns added.
    """
    #########################################################################################################
    num_rows    = detail_df.shape[0]
    num_lobs    = num_rows // num_yrs
    start_year  = inception_year - (num_yrs - 1)
    
    detail_df["lob_number"] = np.repeat(    np.arange(1,          num_lobs  +1),        num_yrs)    # implicitly will ignore any partial groups as intended, not that this should occur
    detail_df["yoa"]        = np.tile(      np.arange(start_year, inception_year + 1),  num_lobs)    # Build yoa column from inception_year backwards

    if num_rows % num_yrs != 0:
        print("Warning: Some rows may not be assigned a lob_number due to incomplete group.")

    return utils.safe_fillna_except(detail_df,cols_exclude_fillna())



def add_summary_info_and_filter(detail_df, summary_df):
    """
    Enrich the detailed dataset with summary-level attributes and filter for valid matches.

    This function merges selected columns from `summary_df` into `detail_df` using 'lob_number' as the key.
    After merging, it filters the resulting DataFrame to retain only rows where 'selected_lob' is not null,
    indicating a successful match and valid summary information. It then applies safe fill logic to handle
    missing values, excluding specific columns from being filled.

    Parameters:
    ----------
    detail_df : pd.DataFrame
        The detailed dataset containing granular policy or claim-level data.

    summary_df : pd.DataFrame
        The summary dataset containing higher-level attributes such as:
        - 'selected_lob'
        - 'claim_source'
        - 'claim_to_develop_to_ultimate'
        - 'claim_basis'
        - 'cat_basis'
        - 'lloyds_selected_ielr'
        - 'lob_visible_1', 'lob_visible_2', 'lob_visible_3', "lob_visible_4",   "lob_visible_5", 'is_row_visible'
        - 'lob_number' (used as the join key)

    Returns:
    -------
    pd.DataFrame
        A filtered and enriched DataFrame containing only rows from `detail_df` that successfully matched
        with `summary_df`, with missing values safely filled (excluding specified columns).
    """
    #########################################################################################################
    cols_sum        = [   "selected_lob",    "claim_source",    "claim_to_develop_to_ultimate", "ielr_approach"
                        , "claim_basis",     "cat_basis",       "lloyds_selected_ielr"
                        , "lob_visible_1",   "lob_visible_2",   "lob_visible_3" , "lob_visible_4",   "lob_visible_5"           , "is_row_visible"   ]
    detail_df       = utils.drop_and_merge(     detail_df,   summary_df[cols_sum+["lob_number"]],    on="lob_number")
    not_na_mask     = detail_df['selected_lob'].notna()
    detail_df       = detail_df[ not_na_mask ]
    return  utils.safe_fillna_except(detail_df,cols_exclude_fillna())



def add_policy_data(detail_df, pol_sum_df):
    """
    Merge policy-level gross premium and incurred claims data into the detailed dataset.
    This function renames specific columns in the `pol_sum_df` to pol_xxx for downstream clarity,
    then merges the resulting DataFrame into `detail_df` based on 'selected_lob' and 'yoa'.
    Missing values in the merged columns are filled with 0.

    Parameters:
    ----------
    detail_df :     pd.DataFrame    The detailed dataset containing policy-level or claim-level information.
    pol_sum_df :    pd.DataFrame   The summary dataset containing gross premium and incurred claims data by line of business and year of account.

    Returns:
    -------
    pd.DataFrame  The updated `detail_df` with merged premium and incurred claims columns.
    """
    #########################################################################################################
    cols_on         = ["selected_lob","yoa"]
    cols_orig       = ["gross_premium_cnv", "incurred_attritional_cnv",       "incurred_large_cnv",       "incurred_cat_cnv",        "incurred_total_cnv" ]
    cols_new        = ["latest_gpi",        "pol_incurred_attritional_cnv",   "pol_incurred_large_cnv",   "pol_incurred_cat_cnv",    "pol_incurred_total_cnv" ]
    cols_dict       = dict(zip(cols_orig,cols_new))
    pol_sum_df     = pol_sum_df.rename( columns = cols_dict )
    detail_df       = utils.drop_and_merge(     detail_df,   pol_sum_df[  cols_new + cols_on  ],    on=cols_on)
    return  utils.safe_fillna_except(detail_df,cols_exclude_fillna())



def add_acquisition_cost(detail_df, deductions_df):
    """
    Merge acquisition cost information into the detailed dataset.
    This function merges selected deduction columns from `deductions_df` into `detail_df`
    using 'selected_lob' as join key. Missing values in the merged columns are filled with 0.

    Parameters:
    ----------
    detail_df :     pd.DataFrame    The detailed dataset containing policy-level data.
    deductions_df : pd.DataFrame    The dataset containing acquisition cost deductions by line of business and year of account.

    Returns:
    -------
    pd.DataFrame                    The updated `detail_df` with acquisition cost information merged in.
    """
    #########################################################################################################
    deductions_df["acquisition_costs"] = deductions_df["selected_effective_deductions"]
    cols_on         = ["selected_lob"]
    cols_sum        = ["acquisition_costs"]
    detail_df       = utils.drop_and_merge(     detail_df,   deductions_df[  cols_sum + cols_on  ],    on=cols_on)
    return  utils.safe_fillna_except(detail_df,cols_exclude_fillna())



def calc_gnpi(detail_df):
    """
    Calculate Gross Net Premium Income (GNPI) for each record in the detailed dataset.
    GNPI is computed as:        GNPI = GPI × (1 - acquisition_costs)
    This function adds a new column 'latest_gnpi' to the DataFrame, filling any missing values with 0.

    Parameters:
    ----------
    detail_df : pd.DataFrame    The detailed dataset containing 'latest_gpi' and 'acquisition_costs' columns.

    Returns:
    -------
    pd.DataFrame                The updated DataFrame with a new 'latest_gnpi' column.
    """
    #########################################################################################################
    # GNPI = GPI × (1 - acquisition cost)
    detail_df["latest_gnpi"] = (detail_df["latest_gpi"] * (1 - detail_df["acquisition_costs"]))
    return detail_df



def add_claims_data(detail_df, clm_sum_df):
    """
    Merge claim summary data into the detailed dataset.
    This function renames claim summary columns to avoid collisions, then merges them into the detailed dataset
    based on 'selected_lob' and 'yoa'. Missing values are filled with 0.

    Parameters:
    ----------
    detail_df : pd.DataFrame        The detailed dataset to be enriched with claim summary data.

    clm_sum_df : pd.DataFrame       The claim summary dataset containing incurred values by LOB and YOA.

    Returns:
    -------
    pd.DataFrame                    The updated detailed dataset with claim summary columns added.
    """
    #########################################################################################################
    cols_on         = ["selected_lob","yoa"]

    cols_orig       = [ "open_attritional",          "open_large",           "open_cat",         "open_total"
                       ,"closed_attritional",        "closed_large",         "closed_cat",       "closed_total"      
                       ,"total_attritional",         "total_large",          "total_cat",        "total"            ]

    cols_new        = [ "clm_open_attritional",      "clm_open_large",       "clm_open_cat",     "clm_open_total"
                       ,"clm_closed_attritional",    "clm_closed_large",     "clm_closed_cat",   "clm_closed_total"
                       ,"clm_total_attritional",     "clm_total_large",      "clm_total_cat",    "clm_total"        ]
                       
    cols_dict       = dict(zip(cols_orig,cols_new))
    clm_sum_df      = clm_sum_df.rename( columns = cols_dict )
    detail_df       = utils.drop_and_merge(     detail_df,   clm_sum_df[  cols_new + cols_on  ],    on=cols_on)
    return  utils.safe_fillna_except(detail_df,cols_exclude_fillna())



def assign_claims(detail_df):
    """
    Assign latest incurred claims values based on claim source and basis.
    This function uses masks to determine whether to use claim-level or policy-level incurred values,
    and assigns them to new columns accordingly. If the claim source is not 'Claim Level Data' and
    the basis is not 'Attr / Lrg / Cat', values for the more detailed split open/closed are set to zero.

    Parameters:
    ----------
    detail_df : pd.DataFrame        The detailed dataset containing claim and policy incurred values.

    Returns:
    -------
    pd.DataFrame                    The updated DataFrame with assigned incurred claims columns.
    """
    #########################################################################################################

    # set masks
    mask_clm        = (detail_df['claim_source'].fillna("") == "Claim Level Data")
    mask_alc        = (detail_df['claim_basis'].fillna("")  == "Attr / Lrg / Cat")
    mask_not_clm_alc= ~( mask_alc & mask_clm)

    # Open claims
    detail_df['latest_incurred_open_claims_attr']    = np.where( mask_not_clm_alc, 0, detail_df["clm_open_attritional"])
    detail_df['latest_incurred_open_claims_large']   = np.where( mask_not_clm_alc, 0, detail_df["clm_open_large"])
    detail_df['latest_incurred_open_claims_cat']     = np.where( mask_not_clm_alc, 0, detail_df["clm_open_cat"])
    detail_df['latest_incurred_open_claims_total']   = np.where( mask_not_clm_alc, 0, detail_df["clm_open_total"])
    
    # Closed claims    
    detail_df['latest_incurred_closed_claims_attr']  = np.where( mask_not_clm_alc, 0, detail_df["clm_closed_attritional"])
    detail_df['latest_incurred_closed_claims_large'] = np.where( mask_not_clm_alc, 0, detail_df["clm_closed_large"])
    detail_df['latest_incurred_closed_claims_cat']   = np.where( mask_not_clm_alc, 0, detail_df["clm_closed_cat"])
    detail_df['latest_incurred_closed_claims_total'] = np.where( mask_not_clm_alc, 0, detail_df["clm_closed_total"])

    # Total claims (claim-level vs policy-level) 
    detail_df['latest_incurred_total_claims_attr']  = np.where( mask_clm, detail_df["clm_total_attritional"], detail_df["pol_incurred_attritional_cnv"])
    detail_df['latest_incurred_total_claims_large'] = np.where( mask_clm, detail_df["clm_total_large"],       detail_df["pol_incurred_large_cnv"])
    detail_df['latest_incurred_total_claims_cat']   = np.where( mask_clm, detail_df["clm_total_cat"],         detail_df["pol_incurred_cat_cnv"])
    detail_df['latest_incurred_total_claims_total'] = np.where( mask_clm, detail_df["clm_total"],             detail_df["pol_incurred_total_cnv"])
    return detail_df



def calculate_movement(detail_df):
    """
    Calculate movement in incurred claims by claim type.
    Movement is defined as the difference between the current position and last year's position
    for each claim type: attritional, large, cat, and total.

    Parameters:
    ----------
    detail_df : pd.DataFrame     The detailed dataset containing current and prior year incurred values.

    Returns:
    -------
    pd.DataFrame                 The updated DataFrame with movement columns added.
    """
    #########################################################################################################

    # movement = current position – last year’s position
    for claim_type in ["attr", "large", "cat", "total"]:
        detail_df[f"movement_{claim_type}"] = (   detail_df[f"latest_incurred_total_claims_{claim_type}"] 
                                                - detail_df[f"last_year_position_{claim_type}"]             ).fillna(0)
    return detail_df



def calculate_gn_ilr(detail_df):
    """
    Calculate GN ILR (Gross Net Incurred Loss Ratio) for each claim type.
    GN ILR is calculated as incurred claims divided by GNPI, with safeguards against division by zero.

    Parameters:
    ----------
    detail_df : pd.DataFrame        The detailed dataset containing incurred claims and GNPI.

    Returns:
    -------
    pd.DataFrame                    The updated DataFrame with GN ILR columns added.
    """
    #########################################################################################################
    # GN ILR = current position / GNPI (avoid divide by zero)

    for claim_type in ["attr", "large", "cat", "total"]:
        detail_df[f"gn_ilr_{claim_type}"] = utils.ratio(detail_df[f"latest_incurred_total_claims_{claim_type}"], detail_df["latest_gnpi"]).fillna(0)

    return detail_df



def calculate_ldf_and_rate_change(detail_df, portfolio_profile_summary_df, hxd):
    """
    Calculates development pattern adjustments for premium, incurred, and paid losses based on Lloyd's development factors 
    and override logic, interpolated by elapsed time since reference date.

    Parameters
    ----------
    detail_df : pd.DataFrame
        Detailed data containing year of account (YOA), selected line of business, and other relevant fields.
    
    portfolio_profile_summary_df : pd.DataFrame
        Summary data containing Lloyd's development factors and rate change information by line of business.
    
    hxd : object
        Hierarchical data object containing metadata such as inception date, insured data date, and YOA basis.

    Returns
    -------
    pd.DataFrame
        Updated detail_df with calculated development patterns, applied rate changes, and cleaned columns.
    
    Notes
    -----
    - Handles missing insured data date by defaulting to inception date.
    - Computes elapsed time since reference date based on YOA and basis (Calendar vs Inception).
    - Interpolates Lloyd's development factors between lower and upper bounds.
    - Applies override logic where applicable for premium and incurred development patterns.
    - Applies rate change override logic.
    - Cleans up intermediate columns after computation.
    """

    # extract dates and YOA basis (Calendar vs Inception) from hxd
    inception_date      = hxd.cds.standard_fields.inception_date
    data_yoa_basis      = hxd.cds.risk_information.data_yoa_basis
    insured_data_date   = hxd.cds.risk_information.insured_data_date
    num_years           = constants.YEARS_TO_CONSIDER_IN_PORTFOLIO_PROFILE
    inception_year      = inception_date.year

    # handle missing as at date and flick to pd datetime
    if insured_data_date is None:
        insured_data_date = inception_date - relativedelta(months=9)
    insured_data_date = pd.to_datetime(insured_data_date)   

    # compute reference date per YOA (year of account)
    if data_yoa_basis == "Calendar Year":  
        detail_df['reference_date'] = pd.to_datetime(   detail_df['yoa'].astype(str) + '-01-01' )
    else:
        detail_df['reference_date'] = pd.to_datetime(   detail_df['yoa'].astype(str) 
                                                        + '-' 
                                                        + str(inception_date.month) 
                                                        + '-' 
                                                        + str(inception_date.day)               )

    # time elapsed (in years) since reference date
    detail_df["adjustments_actual"] = ( (insured_data_date - detail_df['reference_date']).dt.days / 365.25 )

    # lower bound = floor of elapsed years, upper = +1
    detail_df["adjustments_lower"]  = np.maximum(0,             np.floor(detail_df["adjustments_actual"]))
    detail_df["adjustments_upper"]  = np.minimum(num_years - 1, detail_df["adjustments_lower"] + 1       )

    # string labels for mapping to profile data
    detail_df["adjustments_lower_str"] = "year_" + detail_df["adjustments_lower"].astype(int).astype(str)
    detail_df["adjustments_upper_str"] = "year_" + detail_df["adjustments_upper"].astype(int).astype(str)

    # get intended column labels
    cols_yrs    = ["year_" + str(y) for y in range(0,num_years)]
    
    # determine the column names that will need to be dropped following the merge, this will still need to be tested as some get dropped/renamed
    cols_detail = detail_df.columns
    cols_pp     = portfolio_profile_summary_df.columns
    cols_extra  = [col for col in cols_pp if col not in cols_detail]


    # merge portfolio profile on selected lob
    detail_df       = utils.drop_and_merge(detail_df, portfolio_profile_summary_df, on = ["selected_lob"])

    # rename the lloyds XXX development columns to the desc. in adjustments_lower_str & adjustments_upper_str
    # then access the values dynamically putting them into adjustments_prem_lloyds_lower & adjustments_prem_lloyds_upper etc
    # interpolate actual factor between lower and upper
    # map to development patterns from the adjustments "staging area where these are calculated
    detail_label= ["prem",   "incurred","paid"]
    dp_label    = ["premium","incurred","paid"]

    for det, dp in   zip(detail_label,  dp_label):
        detail_df.columns                           = detail_df.columns.str.replace(f"lloyds_{dp}_development/", "", regex=False)
        detail_df[f"adjustments_{det}_lloyds_lower"]= utils.indirect_column_lookup(detail_df,"adjustments_lower_str")
        detail_df[f"adjustments_{det}_lloyds_upper"]= utils.indirect_column_lookup(detail_df,"adjustments_upper_str")
        denominator                                 = (detail_df["adjustments_upper"]                    - detail_df["adjustments_lower"]).replace(0,np.nan)
        
        detail_df[f"adjustments_{det}_lloyds_actual"] = (   detail_df[f"adjustments_{det}_lloyds_lower"] 
                                                        +  (detail_df["adjustments_actual"]              - detail_df["adjustments_lower"]) 
                                                        *  (detail_df[f"adjustments_{det}_lloyds_upper"] - detail_df[f"adjustments_{det}_lloyds_lower"]) 
                                                        /  denominator
                                                        ).fillna(0)
        
        detail_df[f"adjustments_{det}_lloyds_actual"] = np.where(detail_df[f"adjustments_{det}_lloyds_actual"] <0, 0, detail_df[f"adjustments_{det}_lloyds_actual"] )

        detail_df[f"development_pattern_{dp}_lloyds_unadjusted"]  = detail_df[f"adjustments_{det}_lloyds_lower" ] 
        detail_df[f"development_pattern_{dp}_lloyds"]             = detail_df[f"adjustments_{det}_lloyds_actual"]
        
        cols_drop   = detail_df.columns.intersection(cols_yrs)
        detail_df   = detail_df.drop(columns = cols_drop)

    # if override is missing → use Lloyd’s, else use override
    for field in ["premium", "incurred"]:
        detail_df[f"development_pattern_{field}_selected"] = (          detail_df[f"development_pattern_{field}_override"]
                                                                .fillna(detail_df[f"development_pattern_{field}_lloyds"]))

    # load rate change - notice it is an override field hence bespoke logic
    col_dest                            = "applied_rate_change"
    detail_df.columns                   = detail_df.columns.str.replace(f"rate_change_with_selection_override/", "", regex=False)
    detail_df['year_str']               = "year_" + (inception_year - detail_df["yoa"]).astype(int).astype(str) 
    detail_df[f"{col_dest}/calculated"] = utils.indirect_column_lookup(detail_df,"year_str")
    detail_df[ col_dest ]               = np.where(   detail_df[f'{col_dest}/is_overridden']
                                                    , detail_df[   col_dest   ]
                                                    , detail_df[f'{col_dest}/calculated'])      
    cols_drop                           = detail_df.columns.intersection(cols_yrs)
    detail_df                           = detail_df.drop(columns = cols_drop)

    # determine the extra columns that were added from portfolio profile that need to now be dropped
    cols_drop  = detail_df.columns.intersection(cols_extra)
    detail_df  = detail_df.drop(columns = cols_drop)

    return detail_df



def calculate_ultimate_premium_selected(detail_df):
    """
    Calculates the selected ultimate premium based on GNPI and development pattern, applying an override if present.

    Parameters
    ----------
    detail_df : pd.DataFrame
        DataFrame containing:
            - latest_gnpi: Latest gross net premium income
            - development_pattern_premium_selected: Selected premium development pattern
            - ultimate_premium_selected_gnpi_override (optional): Override value for ultimate premium

    Returns
    -------
    pd.DataFrame
        Updated DataFrame with:
            - ultimate_premium_selected_gnpi_cl: Calculated ultimate premium using GNPI and development pattern
            - ultimate_premium_selected_gnpi_selected: Final value using override if present, otherwise calculated
            - ultimate_premium_selected_gnpi_selected_ol as above after onlevelling
    """
    # Ultimate premium (calculated)
    detail_df['ultimate_premium_selected_gnpi_cl']   = utils.ratio(   detail_df['latest_gnpi']
                                                                    , detail_df['development_pattern_premium_selected']).fillna(0)

    # Use override if present
    detail_df["ultimate_premium_selected_gnpi_selected"] = np.where(  detail_df["ultimate_premium_selected_gnpi_override"].isna()
                                                                    , detail_df["ultimate_premium_selected_gnpi_cl"]
                                                                    , detail_df["ultimate_premium_selected_gnpi_override"]    )
    # onlevel
    detail_df["ultimate_premium_selected_gnpi_selected_ol"] = (   detail_df["ultimate_premium_selected_gnpi_selected"]
                                                                * detail_df["applied_rate_change_cumulative"]).fillna(0)

    return detail_df



def calculate_exposure_weighting_1(detail_df):
    """
    Adds exposure weighting based on ultimate premium ratios to max values per LOB.

    Parameters
    ----------
    detail_df : pd.DataFrame    Includes selected_lob, ultimate_premium_selected_gnpi_selected, and its on-level version.

    Returns
    -------
    pd.DataFrame    Original DataFrame with max GNPI values and exposure weighting columns.
    """

    # columns
    cols_orig = ["selected_lob", "ultimate_premium_selected_gnpi_selected", "ultimate_premium_selected_gnpi_selected_ol"]
    cols_new  = ["selected_lob", "max_gnpi",                                "max_gnpi_ol"]
    dict_cols = dict(zip(cols_orig, cols_new))

    # Max GNPI by selected LOB
    lob_max_gnpi_df = (detail_df[cols_orig]
                            .groupby("selected_lob")
                            .max()   
                            .reset_index()              
                            .rename(columns = dict_cols ) )

    # Add Max back to detail_df
    detail_df       = utils.drop_and_merge(detail_df, lob_max_gnpi_df, on = ["selected_lob"])

    # test if max_gnpi = 0 then 0 else min (1, gnpi/max_gnpi)
    detail_df['exposure_weighting_onlevel_1']  = np.minimum(1, utils.ratio(  detail_df['ultimate_premium_selected_gnpi_selected_ol']
                                                                            ,detail_df['max_gnpi_ol'])).fillna(0)
    detail_df['exposure_weighting_nominal_1']  = np.minimum(1, utils.ratio(  detail_df['ultimate_premium_selected_gnpi_selected']
                                                                            ,detail_df['max_gnpi'])).fillna(0)
    return detail_df



def calculate_decay_ratio_weighting_2(detail_df, inception_year):
    """
    Applies exponential decay weighting to each record in the DataFrame based on its Year of Account (YOA)
    relative to the inception year.

    Parameters
    ----------
    detail_df : pd.DataFrame
        DataFrame containing a 'yoa' column representing the Year of Account.

    inception_year : int
        The reference year from which decay is calculated (typically the portfolio's inception year).

    Returns
    -------
    pd.DataFrame
        Updated DataFrame with a new column:
            - decay_ratio_weighting_2: exponential decay factor calculated as DECAY_RATIO^(inception_year - yoa)

    Notes
    -----
    - The decay factor decreases for older YOAs, giving more weight to recent years.
    - Assumes 'yoa' is an integer.
    - Uses constants.DECAY_RATIO as the base for exponential decay.
    """
    decay       = constants.DECAY_RATIO
    detail_df["decay_ratio_weighting_2"] = decay **   ( inception_year - detail_df["yoa"] )
    return detail_df



def calculate_developed_weighting_3(detail_df):
    """
    Assigns developed weighting to each record based on the selected incurred development pattern.

    Parameters
    ----------
    detail_df : pd.DataFrame
        DataFrame containing the column 'development_pattern_incurred_selected'.

    Returns
    -------
    pd.DataFrame
        Updated DataFrame with a new column:
            - developed_weighting_3: equal to 'development_pattern_incurred_selected', with NaNs replaced by 0.
    """
    # Developed weighting = incurred pattern
    detail_df["developed_weighting_3"] = detail_df["development_pattern_incurred_selected"].fillna(0)
    return detail_df



def calculate_modelled_weighting(detail_df):
    """
    Calculates modelled weighting for each record based on exposure, decay, and development factors.
    Normalizes the weight within each selected line of business (LOB).

    Parameters
    ----------
    detail_df : pd.DataFrame
        DataFrame containing:
            - exposure_weighting_onlevel_1
            - decay_ratio_weighting_2
            - developed_weighting_3
            - selected_lob

    Returns
    -------
    pd.DataFrame
        Updated DataFrame with:
            - overall_weighting_onlevel: raw product of the three weight components
            - sum_cl_wgt: total weight per LOB
            - modelled_weighting: normalized weight per record
    """
    # Modelled weighting
    detail_df['overall_weighting_onlevel'] = (     detail_df['exposure_weighting_onlevel_1'] 
                                                     *  detail_df['decay_ratio_weighting_2'] 
                                                     *  detail_df['developed_weighting_3']    ).fillna(0)

    detail_df['overall_weighting_nominal'] = (     detail_df['exposure_weighting_nominal_1'] 
                                                     *  detail_df['decay_ratio_weighting_2'] 
                                                     *  detail_df['developed_weighting_3']    ).fillna(0)
    
    # columns
    cols_orig = ["selected_lob", "overall_weighting_onlevel", "overall_weighting_nominal"]
    cols_new  = ["selected_lob", "sum_cl_ol_wgt",             "sum_cl_wgt"]
    dict_cols = dict(zip(cols_orig, cols_new))

    # Sum ChainLadder weight by selected LOB
    lob_sum_wgt_df  = (detail_df[cols_orig].groupby("selected_lob")
                                           .sum()   
                                           .reset_index()              
                                           .rename(columns= dict_cols) )

    # Add sum_cl_wgt back to detail_df
    detail_df       = utils.drop_and_merge(detail_df, lob_sum_wgt_df, on = ["selected_lob"])

    # Normalize
    detail_df['modelled_weighting'] = np.where( detail_df['ielr_approach'] == "Nominal"
                                                , utils.ratio(detail_df['overall_weighting_nominal'], detail_df["sum_cl_wgt"   ]).fillna(0)
                                                , utils.ratio(detail_df['overall_weighting_onlevel'], detail_df["sum_cl_ol_wgt"]).fillna(0))
    return detail_df





def calculate_ielr_weighting(detail_df):
    """
    Calculates and assigns IELR weightings for both 'selected' and 'claim-level' categories
    across each claim type.

    For each of the claim types ['attr', 'cat', 'large', 'total'], and for each weighting mode ['cl', 'sel'],
    the function:
    - Sets the default weighting from the 'modelled_weighting' column into 'ielr_weighting_{mode}_{type}/calculated'.
    - Checks if an override flag ('ielr_weighting_{mode}_{type}/is_overridden') is True.
    - If overridden, retains the manually input value in 'ielr_weighting_{mode}_{type}'.
    - Otherwise, assigns the calculated value from 'modelled_weighting' to 'ielr_weighting_{mode}_{type}'.

    Parameters:
        detail_df (pd.DataFrame): A DataFrame containing modelled weightings, override flags,
                                  and optionally manually input weightings for both selected and claim-level modes.

    Returns:
        pd.DataFrame: The updated DataFrame with calculated and final IELR weightings per claim type and mode.
    """
    # Assign modelled → selected (per claim type)
    for m in ['cl','sel']:
        for claim_type in ['attr', 'cat', 'large', 'total']:
            detail_df[f'ielr_weighting_{m}_{claim_type}/calculated'] = detail_df['modelled_weighting']
            # override with manual input if flagged, else keep calculated
            detail_df[f'ielr_weighting_{m}_{claim_type}'] = np.where(   detail_df[f'ielr_weighting_{m}_{claim_type}/is_overridden']
                                                                    , detail_df[f'ielr_weighting_{m}_{claim_type}']
                                                                    , detail_df[f'ielr_weighting_{m}_{claim_type}/calculated']    )
    return detail_df



def calculate_method_incurred(detail_df):
    """
    Determines the appropriate reserving method ('IELR', 'BF', or 'CL') based on the incurred development pattern,
    with optional manual override.

    Logic:
    - If incurred development < BF threshold → method = 'IELR'
    - If incurred development < CL threshold → method = 'BF'
    - Otherwise → method = 'CL'
    - If an override flag is set, use the manually specified method instead of the calculated one.

    Parameters:
        detail_df (pd.DataFrame): A DataFrame containing incurred development patterns, override flags,
                                  and optionally manually input reserving methods.

    Returns:
        pd.DataFrame: The updated DataFrame with calculated and final reserving methods.
    """
    ############################################################################################################################################
    # load constant thresholds
    bf_threshold = constants.THRESHOLD_FOR_BF
    cl_threshold = constants.THRESHOLD_FOR_CL

    # choose method based on development pattern: < 0.4 → IELR, 0.4–0.75 → BF, ≥ 0.75 → CL
    detail_df['method_incurred/calculated'] = np.where(       detail_df['development_pattern_incurred_selected'] < bf_threshold,  "IELR",
                                                  np.where(   detail_df['development_pattern_incurred_selected'] < cl_threshold,  "BF"  ,
                                                                                                                                  "CL"    ))
    # use override if present, else keep calculated
    detail_df['method_incurred'] = np.where(      detail_df['method_incurred/is_overridden']
                                                , detail_df['method_incurred']
                                                , detail_df['method_incurred/calculated']    )
    return detail_df



def calculate_ultimate_incurred_cl(detail_df):
    """
    Calculates ultimate incurred claims for each claim type ('attr', 'large', 'cat', 'total') 
    based on whether to develop open claims only or total claims (open + closed), 
    using a selected development pattern.

    For each claim type:
    - Projects open claims using the development pattern.
    - Adds closed claims to form the open+closed total.
    - Projects total incurred claims using the same development pattern.
    - Chooses between open-only or total development based on the 'claim_to_develop_to_ultimate' flag.

    After processing all claim types:
    - Drops intermediate helper columns used in calculations.
    - Calculates the implied IELR for the total using ultimate incurred and selected premium.

    Parameters:
        detail_df (pd.DataFrame): A DataFrame containing incurred claims, development patterns,
                                  and a flag indicating whether to develop open or total claims.

    Returns:
        pd.DataFrame: The updated DataFrame with ultimate incurred claims and implied IELR.
    """
    for claim_type in ["attr", "large", "cat", "total"]:
        # project open claims using development pattern
        detail_df['open_div_result'] = utils.ratio(   detail_df[f'latest_incurred_open_claims_{claim_type}']
                                                    , detail_df[f'development_pattern_incurred_selected']    ).fillna(0)

        # add closed claims contribution
        detail_df['open_total']      = ( detail_df['open_div_result'] +   detail_df[f'latest_incurred_closed_claims_{claim_type}'] )

        # project combined (open + closed) position using development pattern
        detail_df['combined_result'] = utils.ratio(   detail_df[f'latest_incurred_total_claims_{claim_type}']
                                                    , detail_df[f'development_pattern_incurred_selected']     ).fillna(0)

        # choose whether to develop only open or total claims
        detail_df[f'ultimate_incurred_cl_{claim_type}'] = np.where(   detail_df["claim_to_develop_to_ultimate"] == "Open"
                                                                    , detail_df['open_total']
                                                                    , detail_df['combined_result']            )

    # drop intermediate helper columns
    detail_df = detail_df.drop(columns={'open_div_result','open_total','combined_result'})

    # calculate implied IELR for total
    detail_df['ultimate_incurred_cl_ielr'] = utils.ratio(   detail_df['ultimate_incurred_cl_total']
                                                             , detail_df['ultimate_premium_selected_gnpi_selected']).fillna(0)
    return detail_df



def calculate_ielr_fields(detail_df, summary_df):
    """
    Calculates Incurred Estimated Loss Ratios (IELRs) by claim type and applies override logic
    to produce final IELR values for each line of business.

    This function performs the following steps:
    1. Filters the detail data to include only rows where the 'CL' method is used.
    2. Computes weighted IELR numerators and denominators for each claim type.
    3. Aggregates these values by 'selected_lob' and calculates IELRs.
    4. Merges the calculated IELRs into the summary DataFrame.
    5. Applies override logic to determine final IELRs based on override flags.
    6. Computes a derived IELR field excluding catastrophe losses.

    Parameters
    ----------
    detail_df : pd.DataFrame
        Detailed data containing incurred losses, premiums, IELR weightings, and override flags.
        Expected columns include:
        - 'method_incurred'
        - 'selected_lob'
        - 'ultimate_incurred_cl_<claim_type>'
        - 'ielr_weighting_<claim_type>'
        - 'ultimate_premium_selected/gnpi_cl'

    summary_df : pd.DataFrame
        Summary data to be updated with calculated and selected IELR values.
        Expected columns include:
        - 'selected_lob'
        - 'ielr_<claim_type>/is_overridden'

    Returns
    -------
    pd.DataFrame
        Updated summary_df with:
        - 'ielr_<claim_type>/calculated' (calculated IELR values)
        - 'ielr_<claim_type>' (final selected IELR values after applying override logic)
        - 'ielr_total_excl_cat' (sum of 'ielr_attr' and 'ielr_large')
    """
    claim_types = ["attr", "large", "cat", "total"]

    # helper factors which are independent of the loop
    nom_wgt = detail_df["overall_weighting_nominal"] 
    ol_wgt  = detail_df["overall_weighting_onlevel"] 
    nom_prem= detail_df["ultimate_premium_selected_gnpi_selected"]
    ol_prem = detail_df["ultimate_premium_selected_gnpi_selected_ol"]
    inf_idx = detail_df["applied_inflation_cumulative"] 
    mask_nom= detail_df["ielr_approach"] == "Nominal"
    
    cl_only        = np.where( detail_df["method_incurred"] == "CL", 1, 0)
    ielr_adj_numer = np.where(mask_nom,        1, inf_idx / ol_prem)
    ielr_adj_denom = np.where(mask_nom, nom_prem,                 1)

    # calculate numerator and denominator for each ielr calculation in detail df
    col_filt   = ["selected_lob"]
    for claim_type in claim_types:
        
        ## 1) SELECTED IELR
        col                  = 'ielr'
        col_numer            = f'{col}_numerator_{claim_type}'
        col_denom            = f'{col}_denominator_{claim_type}'
        cl_ult               = detail_df[f"ultimate_incurred_cl_{claim_type}"] 
        sel_wgt              = detail_df[f"ielr_weighting_cl_{claim_type}"]
        detail_df[col_numer] = ( cl_ult * sel_wgt * cl_only * ielr_adj_numer ).fillna(0)
        detail_df[col_denom] = (          sel_wgt * cl_only * ielr_adj_denom ).fillna(0)
        col_filt            += [col_numer,  col_denom]

        ## 2) NOMINAL IELR
        col                  = 'ielr_nominal'
        col_numer            = f'{col}_numerator_{claim_type}'
        col_denom            = f'{col}_denominator_{claim_type}'
        detail_df[col_numer] = (cl_ult   * nom_wgt * cl_only ).fillna(0)
        detail_df[col_denom] = (nom_prem * nom_wgt * cl_only ).fillna(0)
        col_filt            += [col_numer,   col_denom]

        ## 3) OL All yr IELR
        col                  = 'ielr_ol_all_yr'
        col_numer            = f'{col}_numerator_{claim_type}'
        col_denom            = f'{col}_denominator_{claim_type}'
        detail_df[col_numer] = (cl_ult * inf_idx / ol_prem * ol_wgt ).fillna(0)
        detail_df[col_denom] = (                             ol_wgt ).fillna(0)
        col_filt            += [col_numer,   col_denom]

        ## 4) OL CL yr IELR
        col                  = 'ielr_ol_cl_yr'
        col_numer            = f'{col}_numerator_{claim_type}'
        col_denom            = f'{col}_denominator_{claim_type}'
        detail_df[col_numer] = (cl_ult * inf_idx / ol_prem * ol_wgt * cl_only ).fillna(0)
        detail_df[col_denom] = (                             ol_wgt * cl_only ).fillna(0)
        col_filt            += [col_numer,   col_denom]


    # group by selected_lob and sum the calculated numerators and denominators
    summary_filt_df = detail_df[col_filt].groupby("selected_lob").sum().reset_index().fillna(0)

    # determine the ielr to assign to the "calculated" part of hx override fields
    col_summ   = ["selected_lob"]
    for claim_type in claim_types:
        col_name                    = f'ielr_{claim_type}/calculated'
        col_summ                   += [col_name]
        summary_filt_df[col_name]   = utils.ratio(  summary_filt_df[f'ielr_numerator_{claim_type}']
                                                  , summary_filt_df[f'ielr_denominator_{claim_type}'] )

    # determine the default approach ielrs
    for apch in ['ielr_nominal','ielr_ol_all_yr','ielr_ol_cl_yr']:
        for claim_type in claim_types:
            col_name                 = f'{apch}_{claim_type}'
            col_summ                += [col_name]
            summary_filt_df[col_name]= utils.ratio(  summary_filt_df[f'{apch}_numerator_{claim_type}']
                                                   , summary_filt_df[f'{apch}_denominator_{claim_type}'] )

    summary_df = utils.drop_and_merge(summary_df, summary_filt_df[col_summ],  on = ["selected_lob"])

    # determine the ielr to assign to the "selected" part of hx override fields
    for claim_type in claim_types:
        col_name                    = f'ielr_{claim_type}'
        summary_df[col_name]        = np.where(     summary_df[f'{col_name}/is_overridden']
                                                  , summary_df[f'{col_name}']
                                                  , summary_df[f'{col_name}/calculated']    )

    # determine total excl cat = attr + large
    for apch in ['ielr','ielr_nominal','ielr_ol_all_yr','ielr_ol_cl_yr']:
        summary_df[f'{apch}_total_excl_cat'] = summary_df[f'{apch}_attr'] + summary_df[f'{apch}_large']

    # # drop intermediate columns
    # col_drop   = list(set(col_filt) - {"selected_lob"})
    # summary_df = summary_df.drop(columns=col_drop)

    return summary_df



def append_ielr(detail_df, summary_df):
    """
    Appends IELR values from the summary DataFrame to the detail DataFrame based on 'selected_lob'.
    This function merges the following IELR fields from `summary_df` into `detail_df`: 'ielr_attr', 'ielr_large', 'ielr_cat', 'ielr_total'
    It uses a utility function `drop_and_merge` to:
    1. Drop any existing IELR columns in `detail_df` that would be overwritten.
    2. Merge the selected IELR columns from `summary_df` using 'selected_lob' as the join key.

    Parameters
    ----------
    detail_df : pd.DataFrame        The detailed DataFrame to be updated with IELR values.
    summary_df : pd.DataFrame       The summary DataFrame containing IELR values by 'selected_lob'.

    Returns
    -------
    pd.DataFrame                    Updated `detail_df` with appended IELR columns.
    """
    # append ielr to detail_df
    col_summ   = ["selected_lob", "ielr_attr", "ielr_large", "ielr_cat", "ielr_total"]
    detail_df  = utils.drop_and_merge(detail_df, summary_df[col_summ],  on = ["selected_lob"])
    return detail_df



def calculate_ultimate_incurred_ielr(detail_df):
    """
    Calculates ultimate incurred losses using the IELR approach for each claim type.

    This function estimates ultimate incurred losses by multiplying the selected premium
    ('ultimate_premium_selected_gnpi_selected') by the IELR for each claim type
    ('attr', 'large', 'cat', 'total'). If the IELR approach is not 'Nominal', the result
    is adjusted by dividing by the cumulative on-level factor.

    Formula:
        ultimate_incurred_ielr_<claim_type> =
            (ultimate_premium_selected_gnpi_selected * ielr_<claim_type>) /
            (1 if ielr_approach == 'Nominal' else onlevel_factor_cumulative)

    Parameters
    ----------
    detail_df : pd.DataFrame
        DataFrame containing:
        - 'ultimate_premium_selected_gnpi_selected' : float
        - 'ielr_attr', 'ielr_large', 'ielr_cat', 'ielr_total' : float
        - 'ielr_approach' : str (e.g., 'Nominal' or other)
        - 'onlevel_factor_cumulative' : float

    Returns
    -------
    pd.DataFrame
        Updated DataFrame with new columns:
        - 'ultimate_incurred_ielr_attr'
        - 'ultimate_incurred_ielr_large'
        - 'ultimate_incurred_ielr_cat'
        - 'ultimate_incurred_ielr_total'
    """

    # determine if lr detrending is required and the factor
    detrend = np.where(detail_df["ielr_approach"] == "Nominal",  1,  1 / detail_df["onlevel_factor_cumulative"].fillna(1) )

    # calculate ultimates on ielr approach - notice it doesnt matter if claim basis is attr/large/cat or total
    
    for claim_type in ["attr", "large", "cat", "total"]:
        detail_df[f"ultimate_incurred_ielr_{claim_type}"] = (   detail_df["ultimate_premium_selected_gnpi_selected"]
                                                              * detail_df[f"ielr_{claim_type}"]                      
                                                              * detrend                                         )
    return detail_df



def calculate_ultimate_incurred_bf(detail_df):
    """
    Calculate Bornhuetter-Ferguson (BF) ultimate incurred values for different claim types.
    This function applies the standard BF method to estimate ultimate incurred claims by blending
    the chain-ladder (CL) projection with the Initial Expected Loss Ratio (IELR) projection,
    weighted by the selected development pattern.
    Formula used:    BF Ultimate = CL Ultimate * Dev% + IELR Ultimate * (1 - Dev%)

    Parameters:
    -----------
    detail_df : pd.DataFrame
        A DataFrame containing the following columns for each claim type:
        - 'ultimate_incurred_cl_{claim_type}'
        - 'ultimate_incurred_ielr_{claim_type}'
        - 'development_pattern_incurred_selected'

    Returns:
    --------
    pd.DataFrame
        The input DataFrame with additional columns:
        - 'ultimate_incurred_bf_attr'
        - 'ultimate_incurred_bf_large'
        - 'ultimate_incurred_bf_cat'
        - 'ultimate_incurred_bf_total'
    """
    # BF = incurred + IELR portion * (1 – dev%): agreed Nov 2025 by PB previously weighted CL which could be distorted by claim to develop = open only
    for claim_type in ["attr", "large", "cat", "total"]:
        detail_df[f'ultimate_incurred_bf_{claim_type}'] = (   detail_df[f'latest_incurred_total_claims_{claim_type}'] 
                                                            + detail_df[f'ultimate_incurred_ielr_{claim_type}']
                                                            * (1 - detail_df['development_pattern_incurred_selected'])  ).fillna(0)

    return detail_df



def calculate_additional_ibnr(detail_df):
    """
    Calculate the total additional IBNR (Incurred But Not Reported) across claim types.
    This function computes the total additional IBNR by summing the values for 'attr', 'large',
    and 'cat' claim types. It handles missing values by treating them as zero.

    Parameters:
    -----------
    detail_df : pd.DataFrame  A DataFrame containing the following columns:  'additional_ibnr_attr', 'additional_ibnr_large', 'additional_ibnr_cat'

    Returns:
    --------
    pd.DataFrame
        The input DataFrame with an additional column:        - 'additional_ibnr_total'
    """
   # total additional IBNR = sum of attr, large, cat
    detail_df["additional_ibnr_total"] = (   detail_df["additional_ibnr_attr"] 
                                           + detail_df["additional_ibnr_large"] 
                                           + detail_df["additional_ibnr_cat"]    ).fillna(0)

    return detail_df



def calculate_ultimate_incurred_selected(detail_df):
    """
    Calculate the selected ultimate incurred values for each claim type based on the selected method.
    This function determines the selected ultimate incurred value for each claim type ('attr', 'large',
    'cat', 'total') using the method specified in the 'method_incurred' column. It supports Chain Ladder (CL),
    Bornhuetter-Ferguson (BF), and IELR methods. It also adds any additional IBNR and applies overrides
    where flagged.
    Additionally, it handles aggregation logic for total claims when the claim basis is split
    ('Attr / Lrg / Cat') or not.

    Parameters:
    -----------
    detail_df : pd.DataFrame
        A DataFrame containing:
        - 'method_incurred'
        - 'ultimate_incurred_cl_{claim_type}'
        - 'ultimate_incurred_bf_{claim_type}'
        - 'ultimate_incurred_ielr_{claim_type}'
        - 'additional_ibnr_{claim_type}'
        - 'ultimate_incurred_selected_{claim_type}/is_overridden'
        - 'ultimate_incurred_selected_{claim_type}'
        - 'claim_basis'

    Returns:
    --------
    pd.DataFrame
        The input DataFrame with updated columns:
        - 'ultimate_incurred_selected_{claim_type}/calculated'
        - 'ultimate_incurred_selected_{claim_type}'
        - 'ultimate_incurred_selected_total'
        - 'ultimate_incurred_selected_total/calculated'
    """
    for claim_type in ["attr", "large", "cat", "total"]:
        # pick method-specific ultimate (CL, BF, IELR)
        col = f'ultimate_incurred_selected_{claim_type}/calculated'
        detail_df[ col ] =  np.where(     detail_df[f'method_incurred'] == "CL",   detail_df[f'ultimate_incurred_cl_{claim_type}'],
                                np.where( detail_df[f'method_incurred'] == "BF",   detail_df[f'ultimate_incurred_bf_{claim_type}'],
                                                                                   detail_df[f'ultimate_incurred_ielr_{claim_type}']))
        # add additional ibnr
        detail_df[ col ]+=  detail_df[f'additional_ibnr_{claim_type}'].fillna(0)
        
        # override if flagged
        col = f'ultimate_incurred_selected_{claim_type}' 
        detail_df[ col ] = np.where( detail_df[f'{col}/is_overridden'],    detail_df[ col ],    detail_df[f'{col}/calculated'])

    
    # handling situation where 'claim_basis' is "Attr / Lrg / Cat" and thereby should have some summed
    # in some situations we will calculated total twice but far more elegant for code
    col = 'ultimate_incurred_selected'
    detail_df[ f'{col}_total' ]           =  np.where(     detail_df['claim_basis'] != "Attr / Lrg / Cat" 
                                                       ,   detail_df[f'{col}_total']
                                                       ,   detail_df[f'{col}_attr']  
                                                         + detail_df[f'{col}_large']  
                                                         + detail_df[f'{col}_cat'])

    detail_df[f'{col}_total/calculated']  =  np.where(     detail_df['claim_basis'] != "Attr / Lrg / Cat" 
                                                       ,   detail_df[f'{col}_total/calculated']
                                                       ,   detail_df[f'{col}_attr/calculated']  
                                                         + detail_df[f'{col}_large/calculated']  
                                                         + detail_df[f'{col}_cat/calculated'])

    # total excluding cat = attr + large (or just total if not split)
    detail_df[ f'{col}_total_x_cat' ]     =  np.where(     detail_df['claim_basis'] != "Attr / Lrg / Cat" 
                                                       ,   detail_df[f'{col}_total']
                                                       ,   detail_df[f'{col}_attr']  
                                                         + detail_df[f'{col}_large'] )
    return detail_df



def calculate_ultimate_ulr_selected(detail_df):
    """
    Calculate the selected Ultimate Loss Ratio (ULR) for each claim type.

    This function computes the ULR by dividing the selected ultimate incurred amount by the
    selected gross net written premium (GNPI CL basis) for each claim type. It avoids division
    by zero using a utility ratio function and fills missing values with zero.

    Parameters:
    -----------
    detail_df : pd.DataFrame
        A DataFrame containing:
        - 'ultimate_incurred_selected_{claim_type}' for each of:
            ['attr', 'large', 'cat', 'total', 'total_x_cat']
        - 'ultimate_premium_selected_gnpi_cl'

    Returns:
    --------
    pd.DataFrame
        The input DataFrame with additional columns:
        - 'ultimate_ulr_selected_{claim_type}' for each of:
            ['attr', 'large', 'cat', 'total', 'total_x_cat']
    """
    col_source  = "ultimate_incurred_selected"
    col_dest    = "ultimate_ulr_selected"

    for claim_type in ["attr", "large", "cat", "total", "total_x_cat"]:
        # ULR = ultimate incurred / premium (avoid divide by zero)
        detail_df[f'{col_dest}_{claim_type}'] = utils.ratio(   detail_df[   f'{col_source}_{claim_type}' ]
                                                             , detail_df[f'ultimate_premium_selected_gnpi_selected']).fillna(0)
    return detail_df



def calculate_applied_inflation(detail_df, inflation_summary_df):
    """
    Calculates and applies inflation values to a detailed portfolio DataFrame based on a summary inflation table.

    This function merges inflation data into the detailed portfolio data using 'selected_lob' as the key.
    It dynamically selects the inflation value corresponding to each row's 'yoa' (year of account) and applies
    override logic: if an override flag is set, the overridden value is used; otherwise, the calculated value is used.

    Parameters:
    ----------
    detail_df : pd.DataFrame
        The detailed portfolio data, including 'yoa', 'selected_lob', and override flags/values.
    
    inflation_summary_df : pd.DataFrame
        A summary table containing inflation values by 'selected_lob' and year of account (as columns).

    Returns:
    -------
    pd.DataFrame
        The updated detail_df with a new 'applied_inflation' column and temporary columns removed.
    """


    # determine the column names that will need to be dropped following the merge, this will still need to be tested as some get dropped/renamed
    cols_detail = detail_df.columns
    cols_inf     = inflation_summary_df.columns
    cols_extra  = [col for col in cols_inf if col not in cols_detail]

    # merge portfolio profile on selected lob
    detail_df       = utils.drop_and_merge(detail_df, inflation_summary_df, on = ["selected_lob"])

    # load inflation - notice it is an override field hence bespoke logic - and we are accessing the column headings dynamically
    col_dest                            = "applied_inflation"


    detail_df[f"{col_dest}/calculated"] = utils.indirect_column_lookup(detail_df,"year_str")

    detail_df[ col_dest ]               = np.where(   detail_df[f'{col_dest}/is_overridden']
                                                    , detail_df[   col_dest   ]
                                                    , detail_df[f'{col_dest}/calculated'])
    # drop extraneous columns
    detail_df                           = detail_df.drop(columns = cols_extra)

    return detail_df



def calculate_on_level_indices(detail_df):
    # get cumulative amount by year ascending, get overall product, product/cumul gives the index needed.
    detail_df['applied_inflation_plus_1'] = 1 + detail_df['applied_inflation'] 
    for col in ['applied_rate_change', 'applied_inflation_plus_1']:
        detail_df[col           ] = pd.to_numeric(detail_df[col], errors='coerce')
        ss_col                    = detail_df.groupby("lob_number")[col]
        detail_df[f'{col}_cumul'] = ss_col.cumprod()
        detail_df[f'{col}_prod' ] = ss_col.transform('prod')
        detail_df[f'{col}_index'] = utils.ratio(    detail_df[f'{col}_prod' ],     detail_df[f'{col}_cumul']   )

    detail_df['applied_rate_change_cumulative'] = detail_df['applied_rate_change_index']
    detail_df['applied_inflation_cumulative']   = detail_df['applied_inflation_plus_1_index']
    detail_df['onlevel_factor_cumulative']      = utils.ratio(   detail_df[ 'applied_inflation_cumulative'   ] 
                                                               , detail_df[ 'applied_rate_change_cumulative' ])

    return detail_df



def calculate_on_levelled(detail_df):

    # Apply to ultimate cols
    col_names = ["attr", "large",  "cat",  "total", "total_x_cat"]
    for col_name in col_names:
        detail_df[f'ultimate_ulr_on_levelled_{col_name}'] = (   detail_df[f'ultimate_ulr_selected_{col_name}'] 
                                                              * detail_df['onlevel_factor_cumulative']          )
    
    return detail_df






def calculate_visible_detail_rows(detail_df, show_all_yrs):
    """
    Adjust LOB visibility flags in the detailed dataset based on premium and claims presence.
    If `show_all_yrs` is False, this function identifies rows where both:
    - `latest_incurred_total_claims_total` is zero, and
    - `ultimate_premium_selected_gnpi_selected` is zero
    These rows are considered empty for the year and have their LOB visibility flags
    (`lob_visible_1`, `lob_visible_2`, `lob_visible_3`, "lob_visible_4",   "lob_visible_5") set to False.

    Parameters:
    ----------
    detail_df : pd.DataFrame    The detailed dataset containing claim and premium information, along with LOB visibility flags.
    show_all_yrs : bool         A flag indicating whether all years should be shown regardless of data presence.

    Returns:
    -------
    pd.DataFrame                The updated DataFrame with visibility flags adjusted for rows lacking both claims and premium.
    """
    if not show_all_yrs:
        mask_empty_claims_yr        = (detail_df['latest_incurred_total_claims_total']      ==0 )
        mask_empty_premium_yr       = (detail_df['ultimate_premium_selected_gnpi_selected'] ==0 )
        mask_not_latest_year        = (detail_df['yoa'] != max(detail_df['yoa']))
        mask_empty_yr               =( mask_empty_claims_yr & mask_empty_premium_yr & mask_not_latest_year)
        detail_df.loc[mask_empty_yr, ['lob_visible_1', 'lob_visible_2', 'lob_visible_3', "lob_visible_4",   "lob_visible_5"]] = False
    return detail_df


def calculate_where_detail_overrides(detail_df):
    # determine overrides on development
    mask_prem_dev        = detail_df['development_pattern_premium_override'].notna()
    mask_loss_dev        = detail_df['development_pattern_incurred_override'].notna()
    detail_df['ovd_dev'] = mask_prem_dev | mask_loss_dev

    # determine overrides on indices
    mask_rate              = detail_df['applied_rate_change/is_overridden']
    mask_inflation         = detail_df['applied_inflation/is_overridden']
    detail_df['ovd_index'] = mask_rate | mask_inflation

    # determine overrides on ielr weights
    mask_ielr_wgt_attr            = detail_df['ielr_weighting_cl_attr/is_overridden'] 
    mask_ielr_wgt_large           = detail_df['ielr_weighting_cl_large/is_overridden']
    mask_ielr_wgt_cat             = detail_df['ielr_weighting_cl_cat/is_overridden']
    mask_ielr_wgt_total           = detail_df['ielr_weighting_cl_total/is_overridden']
    detail_df['ovd_ielr_weights'] = mask_ielr_wgt_attr | mask_ielr_wgt_large | mask_ielr_wgt_cat | mask_ielr_wgt_total 

    # determine overrides on premium
    detail_df['ovd_premium'] = detail_df['ultimate_premium_selected_gnpi_override'].notna()

    # determine overrides on ibnr
    mask_ibnr_attr            = detail_df['additional_ibnr_attr' ].fillna(0) != 0
    mask_ibnr_large           = detail_df['additional_ibnr_large'].fillna(0) != 0
    mask_ibnr_cat             = detail_df['additional_ibnr_cat'  ].fillna(0) != 0
    detail_df['ovd_ibnr']     = mask_ibnr_attr | mask_ibnr_large | mask_ibnr_cat
                          
    # determine overrides on ultimate method
    detail_df['ovd_ultimate_method'] = detail_df['method_incurred/is_overridden']
    
    # determine overrides on ultimates
    mask_ultimate_attr        = detail_df['ultimate_incurred_selected_attr/is_overridden']
    mask_ultimate_large       = detail_df['ultimate_incurred_selected_large/is_overridden']
    mask_ultimate_cat         = detail_df['ultimate_incurred_selected_cat/is_overridden']
    mask_ultimate_total       = detail_df['ultimate_incurred_selected_total/is_overridden']
    detail_df['ovd_ultimate'] = mask_ultimate_attr | mask_ultimate_large | mask_ultimate_cat | mask_ultimate_total     

    # determine overrides on ulr weights
    mask_ulr_wgt_attr            = detail_df['ielr_weighting_sel_attr/is_overridden']
    mask_ulr_wgt_large           = detail_df['ielr_weighting_sel_large/is_overridden']
    mask_ulr_wgt_cat             = detail_df['ielr_weighting_sel_cat/is_overridden']
    mask_ulr_wgt_total           = detail_df['ielr_weighting_sel_total/is_overridden']
    detail_df['ovd_ulr_weights'] = mask_ulr_wgt_attr | mask_ulr_wgt_large | mask_ulr_wgt_cat | mask_ulr_wgt_total     

    return detail_df



def calculate_summary_totals(detail_df, summary_df):
    """
    Aggregates financial and claims data from the detail DataFrame and merges it into the summary DataFrame.
    Also calculates modelled and selected loss ratios using weighted IELR logic.

    This function performs the following steps:
    1. Defines a dictionary of columns to aggregate using `.agg()`, primarily with 'sum' operations.
    2. Computes helper columns for weighted IELR-based loss ratios (default and selected) for each claim type.
    3. Aggregates the detail DataFrame by 'selected_lob' using the defined aggregation dictionary.
    4. Merges the aggregated results into the summary DataFrame using a utility function `drop_and_merge`.
    5. Calculates modelled and selected loss ratios for each claim type, applying override logic for attritional and large claims.
    6. Computes standard incurred loss ratios and ultimate loss ratios.
    7. Calculates additional derived metrics such as acquisition costs and total loss ratios excluding catastrophe losses.

    Parameters
    ----------
    detail_df : pd.DataFrame      Detailed data by year containing premiums, incurred losses, IELR weightings, and claim-level metrics.

    summary_df : pd.DataFrame     Summary data to be updated with aggregated and calculated metrics.

    Returns
    -------
    pd.DataFrame
        Updated summary_df with:
        - Aggregated financial and claims metrics
        - Modelled and selected loss ratios (with override logic)
        - Standard incurred and ultimate loss ratios
        - Acquisition cost ratio and total loss ratio excluding catastrophe
    """

    # Although all aggregations are currently sums, .agg() with a dictionary is used to allow future flexibility (e.g., max, mean).

    # initialising the dictionary of values to aggregate with operation to apply
    agg_dict = {    'latest_gpi':                               'sum'
                  , 'latest_gnpi':                              'sum'
                  , 'ultimate_premium_selected_gnpi_cl':        'sum'
                  , 'ultimate_premium_selected_gnpi_override':  'sum'
                  , 'ultimate_premium_selected_gnpi_selected':  'sum'
                  , 'ultimate_premium_selected_gnpi_selected_ol':'sum'
                  , 'ultimate_incurred_selected_total_x_cat':   'sum'}

    clm_types = ["attr",  "large",   "cat",  "total"]

    # defining the columns to aggregate by claim type
    sum_cols   = [    'latest_incurred_open_claims', 'latest_incurred_closed_claims',    'latest_incurred_total_claims'
                    ,'last_year_position',          'movement',                         'ultimate_incurred_selected'   
                    ,'ultimate_incurred_ielr',      'ultimate_incurred_bf',             'ultimate_incurred_cl'          
                    ,'additional_ibnr'                                                                                 ]
    
    for clm in clm_types:
        for col in sum_cols:
            agg_dict[f'{col}_{clm}'] =  'sum'

    # defining the columns to aggregate boolean overrides
    any_cols = ["ovd_dev",      "ovd_index",            "ovd_premium",   "ovd_ielr_weights", 
                "ovd_ibnr",     "ovd_ultimate_method",  "ovd_ultimate",  "ovd_ulr_weights"   ]

    for col in any_cols:
        agg_dict[col] =  'any'

    # calculating helper column for premium weight when using nominal approach - this premium weight was a defect in old algo but kept here for compatability
    nom_prem = np.where(detail_df["ielr_approach"] != "Nominal",  1, detail_df["ultimate_premium_selected_gnpi_selected"].fillna(1) )

    # calculating helper columns for ielrs & covs
    for clm in clm_types:
        col_ulr     = f'ultimate_ulr_on_levelled_{clm}'
        col_wgt_cl  = f'ielr_weighting_cl_{clm}'
        col_wgt_sel = f'ielr_weighting_sel_{clm}'
        # ielr helpers
        detail_df[f'helper_def_{clm}_gnlr_numerator']    = (nom_prem   *   detail_df[col_wgt_cl]   *   detail_df[col_ulr])   # weighted aggregation
        detail_df[f'helper_def_{clm}_gnlr_denominator']  = (nom_prem   *   detail_df[col_wgt_cl]                         )   # weighted aggregation
        detail_df[f'helper_sel_{clm}_gnlr_numerator']    = (nom_prem   *   detail_df[col_wgt_sel]  *   detail_df[col_ulr])
        detail_df[f'helper_sel_{clm}_gnlr_denominator']  = (nom_prem   *   detail_df[col_wgt_sel]                        )
        detail_df[f'helper_ollr_{clm}_gnlr_numerator']   = (nom_prem                               *   detail_df[col_ulr])   # simple aggregation
        detail_df[f'helper_ollr_{clm}_gnlr_denominator'] = (nom_prem                                                     )   # simple aggregation
        
        # cov helpers - ex1: E[X]; ex2: E[X squared]
        detail_df[f'helper_ex1_{clm}_cov_numerator']    = (nom_prem   *   detail_df[col_wgt_sel]   * (detail_df[col_ulr]   ))  
        detail_df[f'helper_ex1_{clm}_cov_denominator']  = (nom_prem   *   detail_df[col_wgt_sel]                            )   
        detail_df[f'helper_ex2_{clm}_cov_numerator']    = (nom_prem   *   detail_df[col_wgt_sel]   * (detail_df[col_ulr]**2)) # notice squared
        detail_df[f'helper_ex2_{clm}_cov_denominator']  = (nom_prem   *   detail_df[col_wgt_sel]                            )


        agg_dict[f'helper_def_{clm}_gnlr_numerator']     =  'sum'
        agg_dict[f'helper_def_{clm}_gnlr_denominator']   =  'sum'
        agg_dict[f'helper_sel_{clm}_gnlr_numerator']     =  'sum'
        agg_dict[f'helper_sel_{clm}_gnlr_denominator']   =  'sum'
        agg_dict[f'helper_ollr_{clm}_gnlr_numerator']    =  'sum'
        agg_dict[f'helper_ollr_{clm}_gnlr_denominator']  =  'sum'

        agg_dict[f'helper_ex1_{clm}_cov_numerator']      =  'sum'
        agg_dict[f'helper_ex1_{clm}_cov_denominator']    =  'sum'
        agg_dict[f'helper_ex2_{clm}_cov_numerator']      =  'sum'
        agg_dict[f'helper_ex2_{clm}_cov_denominator']    =  'sum'


    # group detail_df by selected lob summing columns specified in agg_dict and joining back onto summary_df 
    # dropping any duplicate columns in join from summary_df
    detail_grouped_df = detail_df.groupby("selected_lob").agg(   agg_dict  )
    summary_df        = utils.drop_and_merge(summary_df, detail_grouped_df, on="selected_lob").fillna(0)

    # assigning default & selected loss ratios in summary_df for each claim type based on helpers
    # incorporates allowance for attritional and large being overrides
    for clm in clm_types:
        
        clm_al = clm in ["attr",  "large"]
        if clm_al:          qual = '/calculated'
        elif clm=='cat':    qual = '_exp'
        else:               qual = ''
        
        # qual = '/calculated' if clm_al else ''
        summary_df[f'model_default_{clm}{qual}']     =  utils.ratio(   summary_df[f'helper_def_{clm}_gnlr_numerator'],   summary_df[f'helper_def_{clm}_gnlr_denominator'] )
        summary_df[f'selected_{clm}{qual}']          =  utils.ratio(   summary_df[f'helper_sel_{clm}_gnlr_numerator'],   summary_df[f'helper_sel_{clm}_gnlr_denominator'] )
        summary_df[f'ultimate_ulr_on_levelled_{clm}']=  utils.ratio(   summary_df[f'helper_ollr_{clm}_gnlr_numerator'],  summary_df[f'helper_ollr_{clm}_gnlr_denominator'])
        summary_df[f'ex1_{clm}']                     =  utils.ratio(   summary_df[f'helper_ex1_{clm}_cov_numerator'],    summary_df[f'helper_ex1_{clm}_cov_denominator'])
        summary_df[f'ex2_{clm}']                     =  utils.ratio(   summary_df[f'helper_ex2_{clm}_cov_numerator'],    summary_df[f'helper_ex2_{clm}_cov_denominator'])
        summary_df[f'cov_{clm}']                     =( (summary_df[f'ex2_{clm}']   -   (summary_df[f'ex1_{clm}'] **2 )  ) **0.5
                                                       /(summary_df[f'ex1_{clm}']                                                )).replace([np.inf, -np.inf], np.nan).fillna(0)

        if clm_al:
            summary_df[f'model_default_{clm}']   =  np.where(  summary_df[f'model_default_{clm}/is_overridden']
                                                             , summary_df[f'model_default_{clm}'              ]
                                                             , summary_df[f'model_default_{clm}/calculated'   ])
            summary_df[f'selected_{clm}']        =  np.where(  summary_df[f'selected_{clm}/is_overridden'     ]
                                                             , summary_df[f'selected_{clm}'                   ]
                                                             , summary_df[f'selected_{clm}/calculated'        ])
    # calculate standard loss ratios
    for clm in clm_types:
        summary_df[f'gn_ilr_{clm}']                = utils.ratio(   summary_df[f'latest_incurred_total_claims_{clm}']  
                                                                  , summary_df['latest_gnpi'] )
        summary_df[f'ultimate_ulr_selected_{clm}'] = utils.ratio(   summary_df[f'ultimate_incurred_selected_{clm}']     
                                                                  , summary_df['ultimate_premium_selected_gnpi_selected'] )

    # to allow adjustments to the total ULR it was agreed to bring forward the override part of the attritional lr - agreed YZ 15-jan-2026
    summary_df['selected_total'] += np.where(summary_df['selected_attr/is_overridden'], summary_df['selected_attr'],0)

    # calculate additional columns for which totals are required that do not follow a format
    summary_df['acquisition_costs']                    = 1 - utils.ratio(  summary_df['latest_gnpi'],  summary_df['latest_gpi']) 
    summary_df['ultimate_ulr_selected_total_x_cat']    = summary_df['ultimate_ulr_selected_attr']     + summary_df['ultimate_ulr_selected_large']
    summary_df['ultimate_ulr_on_levelled_total_x_cat'] = summary_df['ultimate_ulr_on_levelled_attr']  + summary_df['ultimate_ulr_on_levelled_large']
    summary_df["ultimate_incurred_cl_ielr"]            = utils.ratio(summary_df["ultimate_incurred_cl_total"], summary_df["ultimate_premium_selected_gnpi_selected"])

    # determine overrides on ielr
    mask_ielr_attr            = summary_df['ielr_attr/is_overridden']
    mask_ielr_large           = summary_df['ielr_large/is_overridden']
    mask_ielr_cat             = summary_df['ielr_cat/is_overridden']
    mask_ielr_total           = summary_df['ielr_total/is_overridden']
    summary_df['ovd_ielr'] = mask_ielr_attr | mask_ielr_large | mask_ielr_cat | mask_ielr_total     

    # determine overrides on ulr
    mask_ulr_sel_attr  = summary_df['selected_attr/is_overridden']
    mask_ulr_sel_large = summary_df['selected_large/is_overridden']
    mask_ulr_sel_cat   = summary_df['selected_cat/is_overridden']
    mask_ulr_md_attr   = summary_df['model_default_attr/is_overridden']
    mask_ulr_md_large  = summary_df['model_default_large/is_overridden']
    mask_ulr_md_cat    = summary_df['model_default_cat/is_overridden']
    summary_df['ovd_ulr'] = (   mask_ulr_sel_attr  | mask_ulr_sel_large | mask_ulr_sel_cat 
                              | mask_ulr_md_attr   | mask_ulr_md_large  | mask_ulr_md_cat     )

    # flicking boolean overrides to strings
    summary_df['ovd_dev']               = np.where(summary_df['ovd_dev'],            "✅", "") # AE request March 26 dont use "❌"
    summary_df['ovd_index']             = np.where(summary_df['ovd_index'],          "✅", "")
    summary_df['ovd_ielr_weights']      = np.where(summary_df['ovd_ielr_weights'],   "✅", "")
    summary_df['ovd_premium']           = np.where(summary_df['ovd_premium'],        "✅", "")
    summary_df['ovd_ibnr']              = np.where(summary_df['ovd_ibnr'],           "✅", "")
    summary_df['ovd_ultimate_method']   = np.where(summary_df['ovd_ultimate_method'],"✅", "")
    summary_df['ovd_ultimate']          = np.where(summary_df['ovd_ultimate'],       "✅", "")
    summary_df['ovd_ulr_weights']       = np.where(summary_df['ovd_ulr_weights'],    "✅", "")
    summary_df['ovd_ulr']               = np.where(summary_df['ovd_ulr'],            "✅", "")  
    summary_df['ovd_ielr']              = np.where(summary_df['ovd_ielr'],           "✅", "")


    # store the row as an index to use in the hx.With statement
    summary_df['row']                              = summary_df.index
    return summary_df








def save_unique_lobs_to_hxd(summary_df, own_experience_path):
    """
    Extract unique LOB values from the summary DataFrame and store them in the HXD object.
    This function retrieves the 'selected_lob' values from `summary_df` and assigns them to
    the `drop_down_lobs` attribute of the `own_experience_path` object. The values are converted
    into a list of dictionaries using `to_dict(orient="records")`.

    Parameters:
    ----------
    summary_df : pd.DataFrame           A DataFrame containing a 'selected_lob' column with LOB identifiers.
    own_experience_path : object        An object with a `drop_down_lobs` attribute where the extracted LOBs will be stored.

    Returns:    None
    -------
    """
    own_experience_path.drop_down_lobs   =  summary_df[['selected_lob']].to_dict(orient="records")
    return 




def save_selected_lob_to_hxd(detail_df, summary_df, own_experience_path):
    """
    Saves selected LOB (Line of Business) totals from a summary DataFrame into structured output paths.

    This function filters the input DataFrame for each visible LOB (lob_visible_1 to lob_visible_5),
    and if exactly one row is found for a given LOB, it extracts a predefined set of metrics and writes
    them to the corresponding attribute (`selected_lob_totals_1`, `selected_lob_totals_2`, `selected_lob_totals_3`,`selected_lob_totals_4`, `selected_lob_totals_5`)
    on the `own_experience_path` object.

    Parameters
    ----------
    summary_df : pandas.DataFrame
        A DataFrame containing summary-level actuarial metrics, including visibility flags and calculated outputs
        for attritional, large, cat, and total splits.

    own_experience_path : object
        An object with attributes `selected_lob_totals_1`, `selected_lob_totals_2`, and `selected_lob_totals_3`,`selected_lob_totals_4`, `selected_lob_totals_5`,
        each expected to be a writable container (e.g., dataclass or custom object) for storing LOB-specific values.

    Notes
    -----
    - Only LOBs with exactly one visible row are processed.
    - The function assumes all required columns exist in `summary_df`.

    Returns
    -------
    None
    """
    # alct columns that are needed
    def alct_core_lst(k):
        return [        f'latest_incurred_open_claims_{k}',
                        f'latest_incurred_closed_claims_{k}',
                        f'latest_incurred_total_claims_{k}',
                        f'last_year_position_{k}',
                        f'movement_{k}',
                        f'gn_ilr_{k}',
                        f'ultimate_incurred_ielr_{k}',
                        f'ultimate_incurred_bf_{k}',
                        f'ultimate_incurred_cl_{k}',             
                        f'ultimate_ulr_selected_{k}',
                        f'ultimate_incurred_selected_{k}',
                        f'ultimate_ulr_on_levelled_{k}',            
                        f'additional_ibnr_{k}',                 ]


    # columns needed in summary - not override (also implicitly none of these are inputs)
    core_std_lst        =  [   'row',
                                'lob_number',
                                'selected_lob',
                                'yoa',

                                'latest_gpi',
                                'latest_gnpi',
                                'acquisition_costs',

                                'ultimate_premium_selected_gnpi_cl',
                                'ultimate_premium_selected_gnpi_override',
                                'ultimate_premium_selected_gnpi_selected',  
                                'ultimate_premium_selected_gnpi_selected_ol',

                                'ultimate_incurred_cl_ielr',
                                'ultimate_incurred_selected_total_x_cat',     
                                'ultimate_ulr_selected_total_x_cat',
                                'ultimate_ulr_on_levelled_total_x_cat',

                                'lob_visible_1',
                                'lob_visible_2',
                                'lob_visible_3',
                                'lob_visible_4',
                                'lob_visible_5'           
                                
                                # 'ielr_total_excl_cat',

                            ]

    chart_detail_cols = {   'yoa',  'gn_ilr_total', 'ultimate_ulr_selected_total', 'ultimate_ulr_on_levelled_total'}
                            # }


    # build final lists of columns
    summary_totals_lst  = (   core_std_lst
                            + [item for k in ['attr', 'large', 'cat', 'total'] for item in alct_core_lst(k)] )
 
    
    # write data to hxd
    for x in range(1,6):
        sum_lob_df = summary_df.loc[    summary_df[f'lob_visible_{x}']   ]
        if sum_lob_df.shape[0] == 1:

            # write summary data to hxd
            sum_row = sum_lob_df.iloc[0] 
            lob_path = getattr(own_experience_path, f'selected_lob_totals_{x}' )
            for node in summary_totals_lst:
                setattr(   lob_path,   node,   sum_row[node]  )

            # write chart data to hxd
            det_lob_df                  = detail_df.loc[   detail_df[f'lob_visible_{x}'],    chart_detail_cols]     # isolate just the rows & columns we want 
            det_lob_df['pricing_basis'] = sum_row['selected_total']
            setattr(   lob_path,   "chart_data",   det_lob_df.to_dict(orient="records")   )

            # write show hide to hxd
            show_alc = False if sum_row['claim_basis'] =="Total" else True
            setattr(   lob_path,   "show_alc",   show_alc   )

            # write ielr approaches data to hxd
            for apch in ['nominal','ol_all_yr','ol_cl_yr']:
                ielr_path = getattr(lob_path.ielr_approaches, apch)
                for claim_type in ["attr", "large", "cat", "total", "total_excl_cat"]:
                    col_source  = f'ielr_{apch}_{claim_type}'
                    node_dest   = f'ielr_{claim_type}'
                    setattr( ielr_path,   node_dest,   sum_row[col_source])

    return




def calculate_cat_gn_ulr_bp(summary_df, bp_summary_df):
    # Load BP projections table
    bp_summary_df['gn_cat_ulr_bp'] = bp_summary_df['adj_cat_gn_ulr']   # conforming name
    cols_merge = ['selected_lob', 'gn_cat_ulr_bp']
    summary_df = utils.drop_and_merge(summary_df, bp_summary_df[  cols_merge  ], on="selected_lob")
    return summary_df



def calculate_cat_gn_ulr_rms(summary_df, hxd):
    # Access RMS cat curves
    cat_path = hxd.cds.cat

    # extract the values from the given data structure
    ss_selected_lob         = [getattr(cat_path.selected_class,      f"curve_{i}")          for i in range(1,11)]
    ss_selected_gn_cat_ulr  = [getattr(cat_path.selected_gn_cat_ulr, f"curve_{i}").selected for i in range(1,11)]
    ss_selected_gn_cat_prem = [getattr(cat_path.gn_in_force_premium, f"curve_{i}_cnv")      for i in range(1,11)]

    # convert the extracted values to a dataframe and calculate incurred
    cat_df = pd.DataFrame({ "curve":                list(range(1, 11)),
                            "selected_lob":         ss_selected_lob,
                            "gn_cat_ulr_selected":  ss_selected_gn_cat_ulr,
                            "gn_cat_premium":       ss_selected_gn_cat_prem })

    cat_df['incurred_selected'] = cat_df['gn_cat_premium']  *  cat_df['gn_cat_ulr_selected']
    cols_sum = ['incurred_selected', 'gn_cat_premium', 'gn_cat_ulr_selected']
    cat_df[cols_sum] = cat_df[cols_sum].fillna(0)

    # group by selected lob, to accomodate duplicate selected_lob and derive the gn lr
    cat_grp_df                   = cat_df.groupby("selected_lob", as_index=False)[cols_sum].sum()
    
    if cat_grp_df.empty:
        summary_df['gn_cat_ulr_rms'] = 0
    else:
        cat_grp_df['gn_cat_ulr_rms'] = utils.ratio( cat_grp_df['incurred_selected'], cat_grp_df['gn_cat_premium'] )
        cols_merge = ['selected_lob','gn_cat_ulr_rms']
        summary_df = utils.drop_and_merge(summary_df, cat_grp_df[  cols_merge  ], on="selected_lob")
    return summary_df



def set_cat_gn_ulr_and_totals(summary_df):

    mask_rms = summary_df['cat_basis'] == "RMS"
    mask_bp  = summary_df['cat_basis'] == "BP"
    mask_tot = summary_df['claim_basis'] == "Total"

    for basis in ['model_default', 'selected']:
        basis_cat = f'{basis}_cat'
        summary_df[f'{basis_cat}_bp']      = summary_df['gn_cat_ulr_bp' ]
        summary_df[f'{basis_cat}_rms']     = summary_df['gn_cat_ulr_rms']
        summary_df[f'{basis_cat}_basis']   = summary_df['cat_basis']
        
        summary_df[f'{basis_cat}/calculated'] = np.where(       mask_rms, summary_df['gn_cat_ulr_rms']
                                                    ,np.where(  mask_bp,  summary_df['gn_cat_ulr_bp' ]
                                                        ,                 summary_df[f'{basis_cat}_exp'  ]))

        summary_df[f'{basis_cat}']            = np.where(  summary_df[f'{basis_cat}/is_overridden']
                                                         , summary_df[f'{basis_cat}'             ]
                                                         , summary_df[f'{basis_cat}/calculated'  ])

        summary_df[f'{basis}_total']          = summary_df[f'{basis_cat}'] + np.where(mask_tot, summary_df[f'{basis}_total'] - summary_df[f'{basis_cat}_exp']
                                                                                              , summary_df[f'{basis}_attr']  + summary_df[f'{basis}_large'] )
        summary_df[f'{basis}_total_excl_cat'] = summary_df[f'{basis}_total'] - summary_df[f'{basis_cat}']

    return summary_df






def get_lloyds_bzy_lrs(hxd, rater, summary_df):

    # specify the columns needed
    cols_lr     = ['model_ielr', 'model_final_gn_ulr', 'selected_ielr', 'selected_final_gn_ulr']
    cols_lr_lob = ['selected_lob'] + cols_lr
    cols_all    = ['composition']  + cols_lr_lob

    # load the lloyds and beazley dataframe filtering to just columns needed
    lloyds_summary_df = rater.get("proj_lloyds_summary",  pd.DataFrame())[cols_all]
    bzly_summary_df   = rater.get("proj_beazley_summary", pd.DataFrame())[cols_all]

    # map loss ratios based on lloyds and beazley
    for sce, df in zip(['beazley','lloyds'], [bzly_summary_df, lloyds_summary_df]):
        cols_out = ['selected_lob']                                                             # initialise list of output cols
        df[cols_lr]   = df[cols_lr].mul(df['composition'].reindex(df.index), axis=0)            # apply weight lr
        grp_df        = df[cols_all].groupby("selected_lob").sum().reset_index().fillna(0)      # grp weighted cols
        for col_in in cols_lr:
            col_out         = f'{sce}_{col_in}'                                                 # specify output col name
            cols_out       += [col_out]                                                         # accumulate list of output cols
            grp_df[col_out] = utils.ratio( grp_df[col_in],  grp_df['composition'] )             # calculate weighted lr allowing for comp
        summary_df    = utils.drop_and_merge(summary_df,    grp_df[cols_out],   "selected_lob") # add columns to summary_df
    
    return summary_df.fillna(0)


