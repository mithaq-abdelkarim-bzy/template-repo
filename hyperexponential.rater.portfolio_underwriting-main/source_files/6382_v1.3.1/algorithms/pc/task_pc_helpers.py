import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
import algorithms.rate_constants as constants
from algorithms.pc.task_pc_simulation import process_simulated_losses
from scipy.stats import linregress

def build_oe_detail(hxd, detail_df):
    
    cols     = [  'latest_gpi',            'ultimate_premium_selected_gnpi_selected'
                , 'additional_ibnr_total', 'latest_incurred_total_claims_total',    'ultimate_incurred_selected_total' ]

    # error trap empty df
    if detail_df[detail_df['selected_lob'].notna()].empty:
        return pd.DataFrame(columns = ['selected_lob'] + cols)          # return empty df

    # manipulating own experience detail_df to yield the totals for the required years
    inception_date  = hxd.cds.standard_fields.inception_date
    year_recent_exc = hxd.cds.pc.pc_control.dcf_exper_exc_yrs           # number of recent years we want to include
    year_recent_exc = 1 if year_recent_exc == None else year_recent_exc # error trap none without preventing zero
    year_include    = hxd.cds.pc.pc_control.dcf_exper_num_yrs or 1      # number of years we want included after allowing for the years to exclude

    inception_year  = inception_date.year
    year_max        = inception_year - 1 - year_recent_exc              # so if 2026 incept    we want 2025 less number of recent years to exclude
    year_min        = year_max       + 1 - year_include                 # so if 3 year include year_max (2024 say) - 3 + 1
    year_range      = range(year_min, year_max + 1)

    mask_years      = detail_df["yoa"].astype(int).isin(year_range)
    stg_detail_df   = detail_df[mask_years].groupby("selected_lob", dropna=False)[cols].sum(min_count=1).reset_index()
    return stg_detail_df


def build_prem_limit(hxd, prem_limit_df):
    prem_limit_df['ggpi_bzly'] = prem_limit_df["bst_share_line_size"] * prem_limit_df['future_ultimate_gross_prem']
    cols                       = ['ggpi_bzly', 'future_ultimate_gross_prem']
    stg_prem_limit_df          = prem_limit_df.groupby("selected_lob", dropna=False)[cols].sum(min_count=1).reset_index()
    return stg_prem_limit_df


def build_dcf_df(hxd, selected_lobs, is_bbt, oe_summary_df, oe_detail_df, prem_limit_df, pc_calculation_df, pc_structure_df):
    
    # PC control path
    pc = hxd.cds.pc.pc_control

    # Extract parameters from hxd
    basis_dcf       = pc.dcf_opt                                            # "Deficit Carry forward Option",   options=["None", "Experience", "$ Amount"]
    basis_dcf_bbt   = pc.dcf_opt_bbt
    basis_exper     = pc.dcf_exper_basis                                    # "Basis",                          options=["Incurred", "Ultimate"],    
    basis_amount    = pc.dcf_amount_basis                                   # "Basis",                          options=["Total Contract", "BST Share"],
    sum_gwp         = hxd.cds.pc.pc_calculations.summary.gwp_5623

    # Special handling if BBT mode is enabled
    if is_bbt:
        amount      = 0 if basis_dcf_bbt != "$ Amount"  else pc.dcf_amount  
        dcf         = 0 if amount is None               else -amount                  # If $ amount basis → take negative amount
        dcf_df      = pd.DataFrame({  'dcf': [dcf],  'selected_lob': ['lob'] })       # Return one-row DataFrame for BBT
        return dcf_df

    # setting columns needed
    cols_pc_calculation = ['selected_lob', 'deductions', 'gwp_5623']
    cols_pc_structure   = ['selected_lob', 'uw_expense', 'expense_basis', 'market_deductions', 'total_fees']

    # build dfs to append
    stg_detail_df           = build_oe_detail(hxd, oe_detail_df)
    stg_prem_limit_df       = build_prem_limit(hxd, prem_limit_df)
    stg_pc_calculation_df   = pc_calculation_df[cols_pc_calculation]
    stg_pc_structure_df     = pc_structure_df[  cols_pc_structure]

    # building combined df from all relevant sources
    df = pd.DataFrame({'selected_lob': selected_lobs})
    df = utils.drop_and_merge(df, stg_detail_df,         'selected_lob').fillna(0)
    df = utils.drop_and_merge(df, stg_pc_calculation_df, 'selected_lob').fillna(0)
    df = utils.drop_and_merge(df, stg_pc_structure_df,   'selected_lob').fillna(0)
    df = utils.drop_and_merge(df, stg_prem_limit_df,     'selected_lob').fillna(0)

    # calculating helper values
    df['gwp']               = df['gwp_5623'].fillna(0)
    df['ult_ggpi']          = utils.ratio(df['ultimate_premium_selected_gnpi_selected'], 1 - df['deductions'])
    df['inc_helper']        = df['additional_ibnr_total'] + df[ 'latest_incurred_total_claims_total']
    df['share_helper']      = utils.ratio(df['ggpi_bzly'], df['future_ultimate_gross_prem'])

    # calculating p&l
    df['gg_prem']           = df['latest_gpi']                                    if basis_exper == "Incurred" else df['ult_ggpi']
    df['market_brokerage']  = df['gg_prem'] * df['market_deductions']             if basis_exper == "Incurred" else 0
    df['fees']              = df['gg_prem'] * df['total_fees']                    if basis_exper == "Incurred" else 0
    df['gn_prem']           = df['gg_prem'] - df['market_brokerage'] - df['fees'] if basis_exper == "Incurred" else df['ultimate_premium_selected_gnpi_selected'] 
    df['el']                = df['inc_helper']                                    if basis_exper == "Incurred" else df['ultimate_incurred_selected_total']
    df['expenses']          = df['uw_expense'] * np.where(df['expense_basis']=="Gross Premium", df['gg_prem'], df['gn_prem'])
    df['p_l']               = df['gn_prem'] - df['el'] - df['expenses']
 
    # calculating share
    df['beazley_share']     = 1 if (basis_dcf=="$ Amount" and basis_amount=="Total Contract")  else  df['share_helper'] 

    # Calculate deficit carry forward based on type
    if   basis_dcf == "None":       df['val_1'] = 0
    elif basis_dcf == "$ Amount":   df['val_1'] = -1 * df['p_l']
    else:                           df['val_1'] = np.minimum(df["p_l"], 0)

    df['val_2'] = (df['gwp'] / sum_gwp if sum_gwp != 0 else 0) if basis_dcf == "$ Amount" else 1 
    df['dcf']   = df['beazley_share'] * df['val_1']  *  df['val_2']

    return df

 


# Main driver: calculate simulated losses based on all inputs
def calculate_simulated_losses_df(
    hxd, 
    no_lob, 
    dcf_df, 
    own_experience_summary_df, 
    selected_lobs, 
    pc_structure_df, 
    pc_calculation_df, 
    sliding_scale_df, 
    correlation_matrix_df, 
    is_bbt):

    # Build distribution parameters (attr, large, cat, etc.)
    distribution_parameter_fitting_df = build_distribution_parameter_fitting_df(hxd, pc_calculation_df)

    # Build supporting PC dataframes
    pc_options              = build_pc_options_df(hxd, selected_lobs, pc_structure_df, is_bbt)
    pc_dcf                  = build_pc_dcf_df(                  dcf_df)
    pc_structure_standard   = build_pc_structure_standard_df(   pc_structure_df)
    pc_structure_sliding_1  = build_pc_structure_sliding_1_df(  pc_structure_df)
    pc_structure_sliding_2  = sliding_scale_df # build_pc_structure_sliding_2_df(  sliding_scale_df, pc_options)
    pc_dist_params          = build_dist_params_df(             pc_calculation_df, distribution_parameter_fitting_df)
    pc_correl               = correlation_matrix_df
    pc_prem                 = build_pc_prem_df(                 pc_calculation_df)
    pc_el_scale             = build_pc_el_scale_df(             pc_calculation_df)

    # For BBT case, trim all inputs down to number of LOBs
    if is_bbt:    
        pc_options              = pc_options[            :no_lob]
        pc_dcf                  = pc_dcf[                :no_lob]
        pc_structure_standard   = pc_structure_standard[ :no_lob]
        pc_structure_sliding_1  = pc_structure_sliding_1[:no_lob]
        # pc_structure_sliding_2  = pc_structure_sliding_2[:no_lob] # JB: if BBT PC is re-enabled this would need to be considered
        pc_dist_params          = pc_dist_params[        :no_lob]
        pc_correl               = pc_correl[             :no_lob]
        pc_prem                 = pc_prem[               :no_lob]
        pc_el_scale             = pc_el_scale[           :no_lob]

    # Feed everything into the processing function
    return process_simulated_losses(
        hxd,
        no_lob,
        pc_options,
        pc_dcf,
        pc_structure_standard,
        pc_structure_sliding_1,
        pc_structure_sliding_2,
        pc_dist_params,
        pc_correl,
        pc_prem,
        pc_el_scale
    )

# Build Deficit Carry Forward (DCF) DataFrame
def build_pc_dcf_df(dcf_df):
    df = pd.DataFrame()
    df["selected_lob"] = dcf_df['selected_lob']
    df["dcf"] = dcf_df['dcf']
    return df


# Build DataFrame with fitted distribution parameters
def build_distribution_parameter_fitting_df(hxd, pc_calculations_df):
    df = pd.DataFrame()

    # Copy selected LOBs
    df['selected_lob']  = pc_calculations_df['selected_lob']

    # Calculate attritional mu and sigma
    df['attr_mu']       = calculate_attr_mu(pc_calculations_df[['attr_el', 'attr_sd']])
    df['attr_sigma']    = calculate_attr_sigma(pc_calculations_df[['attr_el', 'attr_sd']])

    # Large loss distribution parameters
    df['lrg_bool']  = pc_calculations_df['large_sd'] == 0
    df['lrg_alpha'] = np.where(df['lrg_bool'], 0, 1 + (pc_calculations_df['large_el'] / pc_calculations_df['large_sd']))
    df['lrg_beta']  = np.where(df['lrg_bool'], 0, (pc_calculations_df['large_el'] * (df['lrg_alpha'] - 1)) / df['lrg_alpha'])

    # CAT non-weather distribution parameters
    df['cat_helper']= 1 + np.sqrt(1 + (pc_calculations_df['cat_non_weather_el'] / pc_calculations_df['cat_non_weather_sd'])**2)
    df['cat_bool']  = pc_calculations_df['cat_non_weather_sd'] == 0
    df['cat_alpha'] = np.where(df['cat_bool'], 0, df['cat_helper'])
    df['cat_beta']  = np.where(df['cat_bool'], 0, ((df['cat_alpha'] - 1) * pc_calculations_df['cat_non_weather_el']) / df['cat_alpha'])

    # CAT weather parameters (regression-based)
    p1_list = []
    p2_list = []
    for lob in df['selected_lob']:
        if pd.notna(lob):
            p1, p2 = get_cat_w_p1_and_p2(hxd, lob)
        else:
            p1, p2 = 0, 0
        p1_list.append(p1)
        p2_list.append(p2)

    # Assign calculated values
    df = df.assign(cat_w_p1=p1_list, cat_w_p2=p2_list)

    return df



# Calculate "mu" parameter for attritional losses
def calculate_attr_mu(df):
    numerator = df['attr_el'] ** 2
    denominator = np.sqrt(df['attr_sd'] ** 2 + df['attr_el'] ** 2)

    # Ratio formula
    ratio = numerator / denominator

    # Mask invalid values
    ratio = ratio.where(denominator > 0, np.nan)
    ratio = ratio.where(ratio > 0, np.nan)

    # Log transform and replace NaN with 0
    return np.log(ratio).fillna(0)


# Calculate "sigma" parameter for attritional losses
def calculate_attr_sigma(df):
    denominator = 1 + df['attr_el'] ** 2

    # Ratio formula
    ratio = df['attr_sd'] ** 2 / denominator

    # Mask invalid values
    ratio = ratio.where(denominator > 0, np.nan)
    ratio = ratio.where(ratio >= 0, np.nan)

    # Apply log and sqrt to derive sigma
    inside_log = 1 + ratio
    inside_log = inside_log.where(inside_log > 0, np.nan)
    attr_sigma = np.sqrt(np.log(inside_log)).fillna(0)

    return attr_sigma



# Extract CAT curve parameters (p1, p2) for a given LOB
def get_cat_w_p1_and_p2(hxd, lob):
    cat_path = hxd.cds.cat

    # List of CAT return periods
    probabilities = [10000, 5000, 1000, 500, 250, 200, 100, 50, 30, 10, 5, 2] 

    # Extract critical probabilities for all return periods
    critical_probs = [
        getattr(getattr(cat_path, f'one_in_{p}'), 'critical_prob')
        for p in probabilities
    ]

    curve_vals = []
    found = False

    # Loop through curves in CAT and find the one matching the LOB
    for i in range(1, constants.NUM_CURVES_IN_CAT + 1):
        curve_lob = getattr(cat_path.selected_class, f'curve_{i}', None)
        if curve_lob == lob:
            for p in probabilities:
                field = getattr(cat_path, f'one_in_{p}')
                curve_val = getattr(field, f'curve_{i}', None)
                curve_vals.append(curve_val)
                found = True
            break

    # If no matching curve, return zeros
    if not found:
        return (0, 0)

    # Convert to NumPy arrays
    arr_1 = np.array(critical_probs, dtype=np.float64)
    arr_2 = np.array(curve_vals, dtype=np.float64)

    # Apply validity mask
    mask = (arr_1 > 0) & (arr_2 >= 0)

    if not np.any(mask):
        return (0, 0)

    # Transform data for linear regression
    ln_arr_1 = np.log(arr_1[mask])
    sqrt_arr_2 = np.sqrt(arr_2[mask])

    # Fit regression line (slope and intercept)
    slope, intercept, *_ = linregress(sqrt_arr_2, ln_arr_1)

    # Convert intercept back from log scale
    exp_intercept = np.exp(intercept)

    return exp_intercept, slope


def build_pc_options_df(hxd, selected_lobs, pc_structure_df, is_bbt):
    if is_bbt:
        # Return placeholder PC options DF for BBT
        df = pd.DataFrame({
            'selected_lob': ['lob'],
            'pc_interlock':[False],
            'underlying_pc': [False],
            'prop_underlying':[0],
            'underlying_pc_exp': [False]
        }) 
        # Default PC type set to "Standard"
        df['pc_type'] = pc_structure_df['pc_type'].iat[0] or 'Standard'

        return df

    # Get PC control settings from HX
    pc_control_path     = hxd.cds.pc.pc_control
    pc_interlock        = pc_control_path.is_pc_interlocking
    underlying_pc       = pc_control_path.ul_binders_pc
    underlying_pc_exp   = pc_control_path.ul_pc_as_expense
    prop_underlying     = pc_control_path.ul_pc_as_expense_pct

    # Build PC options DF
    pc_options_df = pd.DataFrame()
    pc_options_df['selected_lob']   = selected_lobs
    pc_options_df['pc_type']        = pc_structure_df['pc_type']
    pc_options_df['pc_interlock']   = pc_interlock
    pc_options_df['underlying_pc']  = underlying_pc

    # Handle case when underlying PC is enabled
    if underlying_pc:
        pc_options_df['prop_underlying'] = prop_underlying if prop_underlying is not None else 0
        pc_options_df['underlying_pc_exp'] = underlying_pc_exp
    else:
        pc_options_df['prop_underlying'] = 0
        pc_options_df['underlying_pc_exp'] = False

    return pc_options_df





# Build PC structure DataFrame for "Standard" profit commission
def build_pc_structure_standard_df(pc_structure_df):
    # Create an empty DataFrame
    df = pd.DataFrame()

    # Assign selected LOB, UW expense, basis, and standard PC percent
    df = df.assign(
        selected_lob=pc_structure_df['selected_lob'],
        uw_exp      =pc_structure_df['uw_expense'],
        uw_exp_basis=pc_structure_df['expense_basis'],
        pc_perc     =pc_structure_df['std_pc_percent'].fillna(0)
    )

    return df




# Build PC structure DataFrame for "Sliding Scale 1" commission
def build_pc_structure_sliding_1_df(pc_structure_df):
    # Create an empty DataFrame
    df = pd.DataFrame()

    # Assign selected LOB, UW expense, and expense basis
    df = df.assign(
        selected_lob=pc_structure_df['selected_lob'],
        uw_exp=pc_structure_df['uw_expense'], 
        uw_exp_basis=pc_structure_df['expense_basis']
    )

    return df


# # Build PC structure DataFrame for "Sliding Scale 2" commission
# def build_pc_structure_sliding_2_df(for_sliding_scale_df, pc_options):
#     # Create an empty DataFrame
#     df = pd.DataFrame()

#     # Extract only rows with valid LOBs
#     lobs = pc_options['selected_lob'].dropna()
#     pc_options = pc_options[pc_options['selected_lob'].notna()]

#     # Loop through each LOB option
#     for i, row in pc_options.iterrows():
#         index = i + 1
#         pc_type = row['pc_type']

#         # If not "Standard", use sliding scale GN ULR and PC percent
#         if pc_type != "Standard":
#             df[f'gn_ulr_{index}'] = for_sliding_scale_df[f'selected_lob_{index}/gn_ulr_less_than'].fillna(0)
#             df[f'pc_perc_{index}'] = for_sliding_scale_df[f'selected_lob_{index}/pc'].fillna(0)
#         else:
#             # For "Standard", default to zeros
#             df[f'gn_ulr_{index}'] = 0
#             df[f'pc_perc_{index}'] = 0

#     # Add a zero row at the top for shifting alignment
#     zero_row = pd.DataFrame([0] * len(df.columns)).T
#     zero_row.columns = df.columns
#     df = pd.concat([zero_row, df], ignore_index=True)

#     # Shift PC percentages one row down
#     pc_perc_cols = [col for col in df.columns if col.startswith('pc_perc_')]
#     df[pc_perc_cols] = df[pc_perc_cols].shift(-1).fillna(0)

#     # Remove rows that are entirely zero
#     df = df.loc[~(df == 0).all(axis=1)]

#     return df

# Build distribution parameter DataFrame including RMS indicator
def build_dist_params_df(pc_calculation_df, distribution_parameter_fitting_df):
    df = distribution_parameter_fitting_df

    # Mark whether RMS is applicable (if CAT weather EL > 0)
    df['rms'] = np.where(
        pc_calculation_df['cat_weather_el'] > 0,
        "Yes",
        "No"
    )
    return df


# Build dataframe for premium-related values
def build_pc_prem_df(pc_calculation_df):
    df = pd.DataFrame()

    # Map fields from pc_calculation_df into new columns
    df = df.assign(
        selected_lob=pc_calculation_df['selected_lob'],   # Line of business
        gwp=pc_calculation_df['gwp_5623'],                # Gross written premium
        deduct_perc=pc_calculation_df['deductions'],      # Deductions percentage
        nwp=pc_calculation_df['nwp_5623']                 # Net written premium
    )

    return df




# Build dataframe for expected loss scale factors
def build_pc_el_scale_df(pc_calculation_df):
    df = pd.DataFrame()

    # Extract attritional and large event ELs
    df = df.assign(
        selected_lob=pc_calculation_df['selected_lob'],
        attr_scale=pc_calculation_df['attr_el'],      # Attritional loss scale
        lrg_scale=pc_calculation_df['large_el']       # Large loss scale
    )

    # Use cat_non_weather if available, otherwise fall back to cat_weather
    df['cat_scale'] = np.where(
        pc_calculation_df["cat_non_weather_el"] == 0,
        pc_calculation_df["cat_weather_el"],
        pc_calculation_df["cat_non_weather_el"]
    )

    return df
