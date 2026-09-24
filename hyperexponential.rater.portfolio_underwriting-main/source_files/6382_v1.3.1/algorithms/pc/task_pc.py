import hx
import pandas                       as pd
import numpy                        as np
import math                         as math
import algorithms.rate_utilities    as utils
import algorithms.rate_constants    as constants
# from scipy.stats                             import linregress, norm, multivariate_normal, lognorm
# from scipy.linalg                            import eigh
# from openpyxl                                import workbook
# from openpyxl.utils.dataframe                import dataframe_to_rows
from algorithms.pc.profit_commission_helpers import (build_profit_commission_df, build_profit_commission_summary)
from algorithms.pc.task_pc_helpers           import (    build_dcf_df,    calculate_simulated_losses_df)


def process_sliding_scale_df(path_sliding_scale):
    frames = []
    for lob in path_sliding_scale:
        lob_df                  = utils.pd_df_from_hx_list_v2(lob.scale).dropna()
        lob_df.loc[-1]          = [0] * len(lob_df.columns)                         # add blank row for the realignment (shift) a few rows below
        lob_df                  = lob_df.sort_index().reset_index(drop=True)        
        lob_df['selected_lob']  = lob.selected_lob                                  # add lob
        lob_df['gn_ulr']        = lob_df['gn_ulr_less_than']
        lob_df['pc_perc']       = lob_df['pc'].shift(-1).fillna(0)                  # we do this to align the percentages correctly for when they are applied
        lob_df['scale_row']     = lob_df.index                                      # so we have the order
        lob_df                  = lob_df.drop(columns=['gn_ulr_less_than','pc'])    # drop extra columns
        frames.append(lob_df)

    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def calculate_profit_commission(hxd):
    # Navigate into PC path within HXD structure
    pc_path = hxd.cds.pc

    # Check if risk follows the main syndicate (BBT case)
    is_bbt = hxd.cds.risk_information.follow_main_syndicate

    # set paths
    path_pc_structure   = pc_path.pc_structure.table
    path_pc_calc        = pc_path.pc_calculations.details
    path_sliding_scale  = pc_path.pc_structure.table_sliding_scale
    path_prem_limit     = hxd.cds.prem_limit_profile.table

    # load dfs
    pc_structure_df     = utils.pd_df_from_hx_list_v2(path_pc_structure )
    pc_calcs_df         = utils.pd_df_from_hx_list_v2(path_pc_calc      )
    prem_limit_df       = utils.pd_df_from_hx_list_v2(path_prem_limit   )
    sliding_scale_df    = process_sliding_scale_df(   path_sliding_scale)


    if is_bbt:
        # BBT case → single pseudo-LOB setup
        no_lob = 1
        correl_df = pd.DataFrame({"selected_lob" : [1]})
        oe_summary_df = pd.DataFrame({"selected_lob" : ["lob"]})
        oe_detail_df  = pd.DataFrame({"selected_lob" : ["lob"]})
        selected_lobs = ["lob"]

    else:
        # Non-BBT case → derive LOBs from input tables

        # set paths
        path_oe_summary = hxd.cds.projections_own_experience.summary_table
        path_oe_detail  = hxd.cds.projections_own_experience.detail_table
    
        # load dfs
        oe_summary_df   = utils.pd_df_from_hx_list_v2(path_oe_summary)
        oe_detail_df    = utils.pd_df_from_hx_list_v2(path_oe_detail)

        # Identify unique selected LOBs (ignoring blanks / duplicates)
        selected_lobs   = prem_limit_df["selected_lob"].dropna().unique()
        no_lob          = len(selected_lobs)

        # Build correlation matrix for LOBs
        correl_path     = pc_path.cm_sel
        list_list       = [ [node.coeff for node in row.cm_col]    for row in correl_path]
        correl_df       = pd.DataFrame(list_list)   

    # cropping df to just number lobs
    oe_summary_df       = oe_summary_df[     :no_lob]
    oe_detail_df        = oe_detail_df[      :no_lob * constants.YEARS_TO_CONSIDER_IN_OWN_EXPERIENCE]
    pc_calcs_df         = pc_calcs_df[       :no_lob]
    pc_structure_df     = pc_structure_df[   :no_lob]

    # Build deficit carry-forward table across LOBs
    dcf_df      = build_dcf_df(hxd, selected_lobs, is_bbt, oe_summary_df, oe_detail_df, prem_limit_df,  pc_calcs_df, pc_structure_df)

    # Calculate simulated loss results (stochastic engine output)
    sim_loss_df = calculate_simulated_losses_df(
        hxd, 
        no_lob,
        dcf_df, 
        oe_summary_df, 
        selected_lobs,
        pc_structure_df, 
        pc_calcs_df, 
        sliding_scale_df, 
        correl_df, 
        is_bbt)

    # Build profit commission results table
    profit_commission_df = build_profit_commission_df(hxd, pc_calcs_df, pc_structure_df, sim_loss_df, dcf_df)

    if not is_bbt:
        # Only build summary for non-BBT cases
        build_profit_commission_summary(hxd, profit_commission_df, sim_loss_df)