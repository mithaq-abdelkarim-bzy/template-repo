import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
import algorithms.rate_constants as constants
from scipy.stats import linregress, norm, multivariate_normal, lognorm
from scipy.linalg import eigh
from openpyxl import workbook
from openpyxl.utils.dataframe import dataframe_to_rows


def pareto_custom(p, a, b):
    # Convert p to numpy array for safe vectorized operations
    p = np.asarray(p)

    # Clip p values to avoid divide-by-zero when p = 1 (but allow p = 0)
    epsilon = np.finfo(float).eps
    p = np.clip(p, 0.0, 1.0 - epsilon)

    # Apply the Pareto formula safely
    result = b / ((1 - p) ** (1 / a))

    return result


def exponential_custom(cat_w_b, seed, cat_w_a):
    # Compute exponential custom distribution, ensuring non-negative result
    return np.maximum((1 / cat_w_b) * np.log((1 - seed) / cat_w_a), 0) ** 2


def is_positive_definite(matrix):
    # Check if matrix is positive definite by confirming all eigenvalues are > 0
    return np.all(eigh(matrix, eigvals_only=True) > 0)


def make_positive_definite(matrix, tol=1e-6):
    # Compute eigenvalues and eigenvectors
    eigvals, eigvecs = eigh(matrix)

    # Replace small or negative eigenvalues with tolerance threshold
    eigvals[eigvals < tol] = tol

    # Reconstruct adjusted positive definite matrix
    return eigvecs @ np.diag(eigvals) @ eigvecs.T


def generate_seed_df(seed, mean_vector, cov_matrix, n_samples):
    # Set random seed for reproducibility
    np.random.seed(seed)

    # Generate multivariate normal random samples
    data = multivariate_normal.rvs(mean=mean_vector, cov=cov_matrix, size=n_samples)

    # Ensure data has correct shape (2D)
    if data.ndim == 1:
        data = data.reshape(-1, 1)

    # Convert to DataFrame with CDF-transformed values
    return pd.DataFrame(norm.cdf(data))


def process_simulated_losses(
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
    pc_el_scale):

    # Get references to PC control flags
    pc_interlock            = hxd.cds.pc.pc_control.is_pc_interlocking
    underlying_pc           = hxd.cds.pc.pc_control.ul_binders_pc
    treated_as_expense      = hxd.cds.pc.pc_control.ul_pc_as_expense
    proportion_of_binders   = hxd.cds.pc.pc_control.ul_pc_as_expense_pct
    underlying_pc_exp       = False if not underlying_pc else treated_as_expense

    # Calculate proportion of binders if applicable
    prop_underlying = proportion_of_binders if underlying_pc else 0
    prop_underlying = prop_underlying or 0

    # Number of simulations to run
    n = hxd.cds.pc.pc_control.no_of_simulations

    # Initialize mean vector for LOBs
    mean_vector = np.zeros(no_lob)

    # Symmetrize correlation matrix
    matrix_input = pc_correl.values
    matrix_input = (matrix_input + matrix_input.T) / 2

    # Ensure matrix is positive definite
    if not is_positive_definite(matrix_input):
        matrix_input = make_positive_definite(matrix_input, tol=1e-3)

    # Generate random seeds for attr, lrg, and cat distributions
    seed_attr = generate_seed_df(seed=1, mean_vector=mean_vector, cov_matrix=matrix_input, n_samples=n)
    seed_lrg  = generate_seed_df(seed=2, mean_vector=mean_vector, cov_matrix=matrix_input, n_samples=n)
    seed_cat  = generate_seed_df(seed=3, mean_vector=mean_vector, cov_matrix=matrix_input, n_samples=n)

    # Create global table per LOB with seeds
    pc_global_table_list = []
    for i in range(no_lob):
        df = pd.DataFrame({
            'seed_attr': seed_attr.iloc[:, i],
            'seed_lrg': seed_lrg.iloc[:, i],
            'seed_cat': seed_cat.iloc[:, i]
        })
        pc_global_table_list.append(df)

    # Initialize list for results across LOBs
    pc_result_all_lob = []

    # Process each selected LOB
    for idx, row in pc_options.dropna(subset=['selected_lob']).iterrows():
        selected_lob = row['selected_lob']

        # Copy seeds into LOB-specific dataframe
        df = pc_global_table_list[idx].copy()

        # setup masks        
        mask_dist   = pc_dist_params['selected_lob']== selected_lob
        mask_opt    = pc_options['selected_lob']== selected_lob
        mask_el     = pc_el_scale['selected_lob']== selected_lob

        # Extract LOB-specific parameters
        rms_flag            = pc_dist_params.loc[mask_dist, 'rms'       ].values[0]
        pc_structure_type   = pc_options.loc[    mask_opt,  'pc_type'   ].values[0]
        attr_scale          = pc_el_scale.loc[   mask_el,   'attr_scale'].values[0]
        lrg_scale           = pc_el_scale.loc[   mask_el,   'lrg_scale' ].values[0]
        cat_scale           = pc_el_scale.loc[   mask_el,   'cat_scale' ].values[0]
        attr_mu             = pc_dist_params.loc[mask_dist, 'attr_mu'   ].values[0]
        attr_sigma          = pc_dist_params.loc[mask_dist, 'attr_sigma'].values[0]
        lrg_a               = pc_dist_params.loc[mask_dist, 'lrg_alpha' ].values[0]
        lrg_b               = pc_dist_params.loc[mask_dist, 'lrg_beta'  ].values[0]
        cat_non_w_a         = pc_dist_params.loc[mask_dist, 'cat_alpha' ].values[0]
        cat_non_w_b         = pc_dist_params.loc[mask_dist, 'cat_beta'  ].values[0]
        cat_w_a             = pc_dist_params.loc[mask_dist, 'cat_w_p1'  ].values[0]
        cat_w_b             = pc_dist_params.loc[mask_dist, 'cat_w_p2'  ].values[0]
        deficit             = pc_dcf.loc[pc_dcf["selected_lob"]== selected_lob, "dcf"].values[0]

        # Add premiums
        df['gwp'] = pc_prem.loc[pc_prem['selected_lob']== selected_lob, 'gwp'].values[0]
        df['gnp'] = pc_prem.loc[pc_prem['selected_lob']== selected_lob, 'nwp'].values[0]

        # Calculate attritional expected loss
        df['attr_el'] = lognorm.ppf(df['seed_attr'], s=attr_sigma, scale=np.exp(attr_mu))
        df['attr_el'] = df['attr_el'].fillna(0)

        # Calculate large expected loss
        df['lrg_el'] = pareto_custom(df['seed_lrg'], lrg_a, lrg_b)
        df['lrg_el'] = df['lrg_el'].fillna(0)

        # Scale attritional losses
        sim_attr_scale_factor   = attr_scale / df["attr_el"].mean()
        df['attr_el']          *= sim_attr_scale_factor
        df['attr_el']           = df['attr_el'].fillna(0)

        # Scale large losses
        mean_lrg_el      = df['lrg_el'].mean()
        lrg_scale_factor = lrg_scale / mean_lrg_el if mean_lrg_el != 0 else 0
        df['lrg_el']     = df['lrg_el'] * lrg_scale_factor
        df['lrg_el']     = df['lrg_el'].fillna(0)

        # Calculate catastrophe losses
        if rms_flag == 'Yes':   df['cat_el'] = exponential_custom(cat_w_b, df['seed_cat'], cat_w_a)
        else:                   df['cat_el'] = pareto_custom(df['seed_cat'], cat_non_w_a, cat_non_w_b)

        df['cat_el'] = df['cat_el'].fillna(0)

        # Scale catastrophe losses
        mean_cat_el      = df['cat_el'].mean()
        cat_scale_factor = cat_scale / mean_cat_el if mean_cat_el != 0 else 0
        df['cat_el']    *= cat_scale_factor
        df['cat_el']     = df['cat_el'].fillna(0)

        # Calculate total expected losses
        df['total_el'] = df[['attr_el', 'lrg_el', 'cat_el']].fillna(0).sum(axis=1)

        # Apply PC structure type
        if pc_structure_type == 'Standard':
            mask         = pc_structure_standard["selected_lob"] == selected_lob
            uw_exp_perc  = pc_structure_standard.loc[mask, "uw_exp"].values[0]
            uw_exp_perc  = 0 if uw_exp_perc is None else uw_exp_perc
            uw_exp_basis = pc_structure_standard.loc[mask, "uw_exp_basis"].values[0]
            pc_perc      = pc_structure_standard.loc[mask, "pc_perc"].values[0]

            df["uw_exp_perc"]  = uw_exp_perc
            df["uw_exp_basis"] = uw_exp_basis
            df["pc_perc"]      = pc_perc
            df["deficit"]      = deficit

        else:
            # Calculate gross net ULR
            df['gn_ulr'] = utils.ratio(df['total_el'], df['gnp'])

            mask         = pc_structure_sliding_1["selected_lob"] == selected_lob
            uw_exp_perc  = pc_structure_sliding_1.loc[mask, "uw_exp"].values[0]
            uw_exp_perc  = 0 if uw_exp_perc is None else uw_exp_perc
            uw_exp_basis = pc_structure_sliding_1.loc[mask, "uw_exp_basis"].values[0]

            # Prepare sliding PC structure
            mask_2       = pc_structure_sliding_2['selected_lob'] == selected_lob
            filtered_pc_structure_sliding_2 = pc_structure_sliding_2[mask_2]
            
            # Sort dataframes for asof merge
            df = df.sort_values('gn_ulr').reset_index(drop=True)
            filtered_pc_structure_sliding_2           = filtered_pc_structure_sliding_2.sort_values('gn_ulr').reset_index(drop=True)
            filtered_pc_structure_sliding_2['gn_ulr'] = filtered_pc_structure_sliding_2['gn_ulr'].fillna(0.0).astype('float64')

            # Merge sliding structure percentages
            df                  = pd.merge_asof(df, filtered_pc_structure_sliding_2, on="gn_ulr", direction="backward")
            df["uw_exp_perc"]   = uw_exp_perc
            df["uw_exp_basis"]  = uw_exp_basis
            df["deficit"]       = deficit
            
        # If no underlying PC is applied
        if not underlying_pc:
            binder_pc_multiplier = 1

            # Zero-out binder-related fields
            df['binder_gwp']        = 0
            df['binder_gnp']        = 0
            df['binder_deficit']    = 0
            df['binder_total_el']   = 0
            df['binder_uw_exp']     = 0
            df['binder_expected_p_l']=0
            df['binder_pc_payable'] = 0

        # If underlying PC applies
        else:
            # If no underlying PC experience
            if not underlying_pc_exp:
                binder_pc_multiplier = 1 + prop_underlying

                # Zero-out binder-related fields
                df['binder_gwp']         = 0
                df['binder_gnp']         = 0
                df['binder_deficit']     = 0
                df['binder_total_el']    = 0
                df['binder_uw_exp']      = 0
                df['binder_expected_p_l']= 0
                df['binder_pc_payable']  = 0

            # If underlying PC experience exists
            else:
                binder_proportion = prop_underlying
                binder_pc_multiplier = 1

                # Scale binder premiums and losses
                df['binder_gwp']        = df['gwp']     * binder_proportion
                df['binder_gnp']        = df['gnp']     * binder_proportion
                df['binder_deficit']    = df['deficit'] * binder_proportion
                df['binder_total_el']   = df['total_el']* binder_proportion

                # Compute binder UW expenses based on basis
                df['binder_uw_exp']     = np.where(
                    df['uw_exp_basis'] == 'Gross Premium',
                    df['uw_exp_perc'] * df['binder_gwp'],
                    df['uw_exp_perc'] * df['binder_gnp']
                )

                # Compute binder expected profit/loss
                df['binder_expected_p_l'] = (
                    df['binder_gnp']
                    - df['binder_total_el']
                    - df['binder_uw_exp']
                    + df['binder_deficit']
                )

                # Compute binder PC payable if profitable
                df['binder_pc_payable'] = np.where(
                    df['binder_expected_p_l'] > 0,
                    df['binder_expected_p_l'] * df['pc_perc'],
                    0
                )

        # Compute UW expenses
        df['uw_exp'] = np.where(
            df['uw_exp_basis'] == 'Gross Premium',
            df['uw_exp_perc'] * df['gwp'],
            df['uw_exp_perc'] * df['gnp']
        )

        # Compute contract expected profit/loss
        df['expected_p_l'] = (
            df['gnp']
            - df['total_el']
            - df['uw_exp']
            + df['deficit']
            - df['binder_pc_payable']
        )

        # Compute PC payable if profitable
        df['pc_payable'] = np.where(
            df['expected_p_l'] > 0,
            df['expected_p_l'] * df['pc_perc'],
            0
        )

        # Total PC payable (contract + binder), adjusted by multiplier
        df['pc_payable_total'] = df['pc_payable'] + df['binder_pc_payable']
        df['pc_payable_total'] = df['pc_payable_total'] * binder_pc_multiplier

        # Recompute binder PC payable when multiplier > 1
        if binder_pc_multiplier != 1:
            df["binder_pc_payable"] = (
                (
                    df["pc_payable_total"]
                    / binder_pc_multiplier
                ) * (binder_pc_multiplier - 1)
            )

        # Compute net of PC premium
        df['gnp_less_pc'] = df['gnp'] - df['pc_payable_total']

        # Compute GN ULR before and after PC
        sum_gnp = df['gnp'].sum()
        gnulr_1 = df['total_el'].sum() / sum_gnp if sum_gnp != 0 else 0

        sum_gnp_less_pc = df['gnp_less_pc'].sum()
        gnulr_2 = df['total_el'].sum() / sum_gnp_less_pc if sum_gnp_less_pc != 0 else 0

        # PC impact is difference in ULR
        pc_impact = gnulr_2 - gnulr_1

        # Handle NaN
        if np.isnan(pc_impact):
            pc_impact = 0

        # Build result dictionary
        result = {
            'selected_lob':     selected_lob,
            'avg_contract_attr':df['attr_el'            ].mean(),
            'avg_contract_lrg': df['lrg_el'             ].mean(),
            'avg_contract_cat': df['cat_el'             ].mean(),
            'avg_contract_total':df['total_el'          ].mean(),
            'avg_contract_p_l': df['expected_p_l'       ].mean(),
            'avg_binder_total': df['binder_total_el'    ].mean(),
            'avg_binder_p_l':   df['binder_expected_p_l'].mean(),
            'avg_binder_pc':    df['binder_pc_payable'  ].mean(),
            'avg_contract_pc':  df['pc_payable'         ].mean(),
            'avg_total_pc':     df['pc_payable_total'   ].mean(),
            'avg_gnp_less_pc':  df['gnp_less_pc'        ].mean(),
            'pc_impact':        pc_impact
        }

        # Store tables and results
        pc_global_table_list[idx] = df.copy()
        pc_result_all_lob.append(result)

    # Build results DataFrame
    pc_result_df = pd.DataFrame(pc_result_all_lob)

    # Build interlocking table from all LOBs
    pc_interlocking_table = pd.DataFrame({
        'gwp':                  sum(df['gwp'] for df in pc_global_table_list),
        'gnp':                  sum(df['gnp'] for df in pc_global_table_list),
        'total_el':             sum(df['total_el'] for df in pc_global_table_list),
        'uw_exp_perc':          pc_global_table_list[0]['uw_exp_perc'],
        'uw_exp_basis':         pc_global_table_list[0]['uw_exp_basis'],
        'pc_perc':              pc_global_table_list[0]['pc_perc'],
        'deficit':              sum(df['deficit'] for df in pc_global_table_list),
        'binder_gwp':           sum(df['binder_gwp'] for df in pc_global_table_list),
        'binder_gnp':           sum(df['binder_gnp'] for df in pc_global_table_list),
        'binder_deficit':       sum(df['binder_deficit'] for df in pc_global_table_list),
        'binder_total_el':      sum(df['binder_total_el'] for df in pc_global_table_list),
        'binder_uw_exp':        sum(df['binder_uw_exp'] for df in pc_global_table_list),
        'binder_expected_p_l':  sum(df['binder_expected_p_l'] for df in pc_global_table_list),
        'binder_pc_payable':    sum(df['binder_pc_payable'] for df in pc_global_table_list),
        'uw_exp':               sum(df['uw_exp'] for df in pc_global_table_list),
        'expected_p_l':         sum(df['expected_p_l'] for df in pc_global_table_list),
        'pc_payable_total':     sum(df['pc_payable_total'] for df in pc_global_table_list),
    })

    # If no interlocking
    if pc_interlock == False:
        pc_interlocking_table['gnp_less_pc'] = (pc_interlocking_table['gnp'] - pc_interlocking_table['pc_payable_total'])
        gnulr_1                 = pc_interlocking_table['total_el'].sum() / pc_interlocking_table['gnp'].sum()
        gnulr_2                 = pc_interlocking_table['total_el'].sum() / pc_interlocking_table['gnp_less_pc'].sum()
        pc_impact_tot_ind       = gnulr_2 - gnulr_1
        pc_impact_tot_interlock = pc_impact_tot_ind

    # If interlocking applies
    else:
        pc_type_1 = pc_options['pc_type'].iloc[0]

        # Apply standard PC structure
        if pc_type_1 == "Standard":
            pc_perc                         = pc_structure_standard["pc_perc"].iloc[0]
            pc_interlocking_table["pc_perc"]= pc_perc

        # Apply sliding scale PC structure
        else:
            pc_interlocking_table["gn_ulr"]           = (pc_interlocking_table["total_el"] / pc_interlocking_table["gnp"]).fillna(0)
            selected_lob                              = pc_structure_sliding_2['selected_lob'].iat[0]                              
            mask_2                                    = pc_structure_sliding_2['selected_lob'] == selected_lob
            filtered_pc_structure_sliding_2           = pc_structure_sliding_2[mask_2]
            filtered_pc_structure_sliding_2           = filtered_pc_structure_sliding_2.sort_values('gn_ulr').reset_index(drop=True)
            filtered_pc_structure_sliding_2['gn_ulr'] = filtered_pc_structure_sliding_2['gn_ulr'].fillna(0.0).astype('float64')

            pc_interlocking_table = pc_interlocking_table.sort_values('gn_ulr').reset_index(drop=True).drop(columns=['pc_perc'])
            pc_interlocking_table = pd.merge_asof(pc_interlocking_table, filtered_pc_structure_sliding_2, on='gn_ulr', direction='backward')


        # Handle binder logic in interlocking
        if not underlying_pc:
            binder_pc_multiplier = 1
            pc_interlocking_table["binder_pc_payable_interlock"] = 0
        else:
            if not underlying_pc_exp:
                binder_pc_multiplier = 1 + prop_underlying
                pc_interlocking_table["binder_pc_payable_interlock"] = 0
            else:
                binder_proportion = prop_underlying
                binder_pc_multiplier = 1
                pc_interlocking_table['binder_pc_payable_interlock'] = np.where(
                    pc_interlocking_table['binder_expected_p_l'] > 0,
                    pc_interlocking_table['binder_expected_p_l'] * pc_interlocking_table['pc_perc'],
                    0
                )

        # Compute UW expenses under interlock
        pc_interlocking_table["uw_exp"] = np.where(
            pc_interlocking_table["uw_exp_basis"] == "Gross Premium",
            pc_interlocking_table["uw_exp_perc"] * pc_interlocking_table["gwp"],
            pc_interlocking_table["uw_exp_perc"] * pc_interlocking_table["gnp"]
        )

        # Compute expected P/L under interlock
        pc_interlocking_table["expected_p_l_interlock"] = (
            pc_interlocking_table["gnp"]
            - pc_interlocking_table["total_el"]
            - pc_interlocking_table["uw_exp"]
            + pc_interlocking_table["deficit"]
            - pc_interlocking_table["binder_pc_payable_interlock"]
        )

        # Compute PC payable under interlock
        pc_interlocking_table["pc_payable_interlock"] = np.where(
            pc_interlocking_table["expected_p_l_interlock"] > 0,
            pc_interlocking_table["expected_p_l_interlock"] * pc_interlocking_table["pc_perc"], 
            0
        )

        # Total PC payable under interlock
        pc_interlocking_table["pc_payable_total_interlock"] = (
            pc_interlocking_table["pc_payable_interlock"] +
            pc_interlocking_table["binder_pc_payable_interlock"]
        )

        pc_interlocking_table["pc_payable_total_interlock"] *= binder_pc_multiplier

        # Recompute binder PC under interlock when multiplier > 1
        if binder_pc_multiplier != 1:
            pc_interlocking_table["binder_pc_payable_interlock"] = (
                (
                    pc_interlocking_table["pc_payable_total_interlock"]
                    / binder_pc_multiplier
                ) * (binder_pc_multiplier - 1)
            )

        # Compute net of PC premiums under both structures
        pc_interlocking_table["gnp_less_pc"] = (
            pc_interlocking_table["gnp"] - pc_interlocking_table["pc_payable_total"]
        )

        pc_interlocking_table["gnp_less_pc_interlock"] = (
            pc_interlocking_table["gnp"] - pc_interlocking_table["pc_payable_total_interlock"]
        )

        # Compute ULRs for interlock impact
        sum_interlock_gnp = pc_interlocking_table["gnp"].sum()
        gnulr_1 = pc_interlocking_table["total_el"].sum() / sum_interlock_gnp if sum_interlock_gnp != 0 else 0

        sum_gnp_less_pc = pc_interlocking_table["gnp_less_pc"].sum()
        gnulr_2 = pc_interlocking_table["total_el"].sum() / sum_gnp_less_pc if sum_gnp_less_pc != 0 else 0

        sum_gnp_less_pc_interlock = pc_interlocking_table["gnp_less_pc_interlock"].sum()
        gnulr_3 = pc_interlocking_table["total_el"].sum() / sum_gnp_less_pc_interlock if sum_gnp_less_pc_interlock != 0 else 0

        # Compute PC impact for independent and interlock structures
        pc_impact_tot_ind = gnulr_2 - gnulr_1
        pc_impact_tot_interlock = gnulr_3 - gnulr_1

    # Add PC impact results
    pc_result_df['pc_impact_tot_ind'] = pc_impact_tot_ind
    pc_result_df['pc_impact_tot_interlock'] = pc_impact_tot_interlock

    # Compute scaling factor for PC impact
    scaling_factor = pc_impact_tot_interlock / pc_impact_tot_ind if pc_impact_tot_ind != 0 else 0

    # Apply scaling to results
    pc_result_df["pc_impact_scaled"] = pc_result_df["pc_impact"] * scaling_factor
    pc_result_df["avg_total_pc_scaled"] = pc_result_df["avg_total_pc"] * scaling_factor

    # Adjust GNP less PC for scaling
    pc_result_df["avg_gnp_less_pc_scaled"] = (
        pc_result_df["avg_gnp_less_pc"] 
        + pc_result_df["avg_total_pc"]
        - pc_result_df["avg_total_pc_scaled"]
    )

    return pc_result_df
