import hx
import numpy as np
from algorithms import rate_constants as constants
from algorithms.rate_utilities import rgetattr
from libraries.model_profiler.algorithms.profiling_hxd_functions         import time_me


def check_selected_lob_values(selected_lob_col, hxd):
    if selected_lob_col.isna().any() or not len(selected_lob_col) or (selected_lob_col == '0').all():
        hx.errors.validation("Warning: “Selected Line of Business” (Risk Code Composition Tab) is blank. Please review before submission.")

        hxd.non_cds.global_fields.is_lobs_msg_shown = True 
        hxd.non_cds.global_fields.is_there_global_message = True


def check_manual_risk_code_values(risk_code_col):
    if not risk_code_col.notna().any():
        hx.errors.validation("Warning: “Risk Code-Manual” (Risk Code Composition Tab) is blank. Please review before submission.")


def check_manual_composition_values(composition_col):
    if composition_col.isna().any():
        hx.errors.validation("Warning: “Composition-Manual” (Risk Code Composition Tab) is blank. Please review before submission")



@time_me
def list_length_matches(hxd, lob_list_length, rc, fac):
    cds = hxd.cds
    last_list_length = None
    
    if rc:
        hxd.non_cds.global_fields.required_riskcode_table_length = lob_list_length or 1
        default_list_length                                      = constants.DEFAULT_NUM_RISK_CODES
        paths                                                    = constants.NODES_DRIVEN_BY_RISK_CODES
    elif fac:
        hxd.non_cds.global_fields.required_fac_lob_table_length  = lob_list_length or 1
        default_list_length                                      = constants.DEFAULT_NUM_RISK_CODES
        paths                                                    = constants.NODES_DRIVEN_BY_FACILITY_LOB
    else:
        hxd.non_cds.global_fields.required_sel_lob_table_length  = lob_list_length or 1
        default_list_length                                      = constants.DEFAULT_NUM_LOB
        paths                                                    = constants.NODES_DRIVEN_BY_SELECTED_LOB

    for path in paths:
        current_list_length = len(rgetattr(cds, path))
        if current_list_length < lob_list_length:
            hx.errors.validation("LOB List has changed. Please re-sync the LOB tables")
            return False

        elif (current_list_length > lob_list_length) and (lob_list_length > default_list_length):
            hx.errors.validation("LOB List has changed. Please re-sync the LOB tables")
            return False
        
        elif (last_list_length != None) and (last_list_length != current_list_length):          # new criteria added 27-3-2026 so sync_lob_lists is required if a new list is added as part of a model upgrade
            hx.errors.validation("LOB List has changed. Please re-sync the LOB tables")
            return False

        last_list_length = current_list_length

    return True

def validate_list_lengths(hxd, rater):
    # source and mask risk composition
    rc_df                = rater["risk_composition_final"]
    rc_df                = rc_df[rc_df["risk_code"].notna()]
    rc_df['selected_lob']= np.where(rc_df['selected_lob']=="0", rc_df['facility_lob'], rc_df['selected_lob'])
    mask_slob            = rc_df['selected_lob'].eq("0")
    rc_df['selected_lob'].mask(mask_slob, rc_df['facility_lob'])
    # get required number of rows
    curr_sel_lob_len     = rc_df[ ["selected_lob"]              ].drop_duplicates().shape[0] 
    curr_fac_lob_len     = rc_df[ ["facility_lob"]              ].drop_duplicates().shape[0] 
    curr_sel_rc_len      = rc_df[ ["selected_lob", "risk_code"] ].drop_duplicates().shape[0]
    # check required number of rows = available
    sel_lob_lengths_okay = list_length_matches(hxd, curr_sel_lob_len, False, False)
    fac_lob_lengths_okay = list_length_matches(hxd, curr_fac_lob_len, False, True )
    sel_rc_lengths_okay  = list_length_matches(hxd, curr_sel_rc_len,  True , False)
    # apply test and write to hxd
    lob_lengths_okay     = sel_lob_lengths_okay and sel_rc_lengths_okay and fac_lob_lengths_okay
    hxd.non_cds.global_fields.mismatched_lob_table_length = not lob_lengths_okay
    return lob_lengths_okay
