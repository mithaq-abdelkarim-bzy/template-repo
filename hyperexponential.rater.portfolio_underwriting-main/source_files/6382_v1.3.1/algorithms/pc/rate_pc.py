import pandas as pd
from algorithms.pc.rate_pc_helpers    import (show_pc_tab,              show_required_fields,  build_pc_structure,
                                              build_pc_calculations_df, build_pc_cals_summary, build_pc_corr_matrix)

def rate_pc(hxd, is_bbt, rater):
    # Display profit commission tab
    show_pc_tab(hxd, is_bbt)

    # Display required fields for input
    show_required_fields(hxd, is_bbt)

    # For non-BBT mode, check selected LOBs from premium/limit profile
    if not is_bbt:
        prm_lim_df    = rater.get("prem_limit_data", pd.DataFrame())
        selected_lobs = prm_lim_df.query('selected_lob != "0"')["selected_lob"].dropna().unique()

        # If no LOBs are selected, exit early
        if len(selected_lobs) == 0:
            return

    # Build profit commission structure from inputs
    build_pc_structure(hxd, is_bbt, rater)
    
    # Build profit commission calculations DataFrame
    pc_calculation_df = build_pc_calculations_df(hxd, is_bbt, rater)

    # For non-BBT mode, build correlation matrix and calculation summary
    bool_interlock  = hxd.cds.pc.pc_control.is_pc_interlocking
    bool_corr_allow = hxd.cds.pc.pc_control.allow_for_correlation
    bool_not_bbt    = not is_bbt
    bool_experience = 'selected_lob' in rater.get('proj_own_exper_detail', pd.DataFrame()).columns
    bool_corr       = bool_not_bbt & bool_corr_allow & bool_interlock & bool_experience

    if bool_corr:
        build_pc_corr_matrix(   hxd, rater)
    else:
        n = 1 if is_bbt else len(selected_lobs)
        hxd.cds.pc.cm_sel  = [ {"cm_col": [{"coeff": 1 if col==row else 0} for col in range(n)]}  for row in  range(n)  ] # list of dictionaries

    if bool_not_bbt:
        build_pc_cals_summary(  hxd, pc_calculation_df)

