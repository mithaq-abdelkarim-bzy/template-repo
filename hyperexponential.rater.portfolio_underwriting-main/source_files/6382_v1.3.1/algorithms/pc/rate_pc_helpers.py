import hx
import pandas as pd
import numpy as np
import math as math
from scipy.stats import linregress

import algorithms.rate_utilities as utils
import algorithms.rate_constants as constants
from algorithms.cat.cat_helpers                 import get_cat_param_by_lob


# Decide whether to show the PC tab in UI depending on flags
def show_pc_tab(hxd, is_bbt):
    pc_path = hxd.non_cds.pc
    risk_inf_path = hxd.cds.risk_information
    is_profit_comission = risk_inf_path.is_profit_comission

    # If PC not enabled, hide everything
    if not is_profit_comission:
        setattr(pc_path, "show_pc_bbt", False)
        setattr(pc_path, "show_pc", False)
    else:
        # Show either BBT or standard PC depending on flag
        if is_bbt:
            setattr(pc_path, "show_pc_bbt", True)
            setattr(pc_path, "show_pc", False)
        else:
            setattr(pc_path, "show_pc_bbt", False)
            setattr(pc_path, "show_pc", True)


# Set required flags/fields for deficit carry forward and binder options
def show_required_fields(hxd, is_bbt):
    if is_bbt:
        # In BBT mode, deficit carry forward comes from special BBT control
        is_on_underlying_binders = False
        dcf_opt = hxd.cds.pc.pc_control.dcf_opt_bbt
    else:
        # Otherwise use normal control values
        is_on_underlying_binders = hxd.cds.pc.pc_control.ul_binders_pc
        dcf_opt = hxd.cds.pc.pc_control.dcf_opt

    # Map option string → tuple of flags
    _flag_map = {
        "$ Amount":   (True,  False, False),  # Is amount
        "Experience": (False, True,  False),  # Is experience
        "None":       (False, False, True),   # Is none
    }

    # Lookup the tuple, default to all False if unknown
    is_amount, is_experience, is_none = _flag_map.get(
        dcf_opt, (False, False, False))

    # Apply flags to the non_cds PC control object
    pc_ctrl = hxd.non_cds.pc.pc_control
    setattr(pc_ctrl, "is_amount",        is_amount)
    setattr(pc_ctrl, "is_none",          is_none)
    setattr(pc_ctrl, "is_experience",    is_experience)
    setattr(pc_ctrl, "is_pc_on_binders", is_on_underlying_binders)



def build_pc_structure(hxd, is_bbt, rater):

    # Get PC structure from rater
    pc_structure_df = rater.get('pc_structure', pd.DataFrame())

    if is_bbt:
        # Override selected_lob with dummy value
        pc_structure_df['selected_lob'] = "lob"
        
        # Mark rows visible if LOB is not null
        pc_structure_df['is_row_visible']    = pc_structure_df['selected_lob'].notna()
        pc_structure_df["total_fees"]        = None
        pc_structure_df["market_deductions"] = None
    
        # Restrict to first row for BBT setup
        pc_structure_df = pc_structure_df[:1]
    else:
        # Extract required data from rater dict
        deductions_df       = rater.get('deductions_df',   pd.DataFrame())
        prm_lim_df          = rater.get('prem_limit_data', pd.DataFrame())

        # Map unique LOBs from limit profile to PC structure
        selected_lobs                     = prm_lim_df["selected_lob"].dropna().unique()
        n                                 = min(len(selected_lobs), len(pc_structure_df))
        pc_structure_df                   = pc_structure_df[:n]
        pc_structure_df['selected_lob']   = list(selected_lobs)[:n]
        pc_structure_df['is_row_visible'] = pc_structure_df['selected_lob'].notna()

        # Map fees from deductions_df by selected_lob
        dict_lob_fees = dict(zip(deductions_df["selected_lob"], deductions_df["total_fees"]))
        pc_structure_df["total_fees"] = pc_structure_df['selected_lob'].map(dict_lob_fees).fillna(0)

        # Map market_deductions from deductions_df by selected_lob
        dict_lob_mktded = dict(zip(deductions_df["selected_lob"], deductions_df["market_deductions"]))
        pc_structure_df["market_deductions"] = pc_structure_df['selected_lob'].map(dict_lob_mktded).fillna(0)

    # JB: TODO THESE NEED TO BE WRITTEN TO 2 NEW NODES and view adjusted accordingly
    is_sliding_scale_shown = (pc_structure_df['pc_type'] == "Sliding Scale" ).any()
    is_standard_shown      = (pc_structure_df['pc_type'] == "Standard"      ).any()

    # Write PC structure back to rater
    rater['pc_structure']  =  pc_structure_df

    # write selected lob to sliding scale
    selected_lobs = pc_structure_df["selected_lob"].dropna().unique()
    path          = hxd.cds.pc.pc_structure.table_sliding_scale
    for obj, lob in zip(path, selected_lobs):                           # pairs elements from both iterables up to the shortest length
        setattr(obj, "selected_lob", lob)



def build_pc_calculations_df(hxd, is_bbt, rater):

    # initialise df depending on if bbt or not
    if is_bbt:  pc_calc_df, exp_param_df = initialise_bbt_pc_calculations(  hxd, rater)
    else:       pc_calc_df, exp_param_df = initialise_x_bbt_pc_calculations(hxd, rater)

    # Build BBT parameter DataFrame and extend pc_calc_df calibration + GN ULR allocation
    bbt_param_df = build_bbt_param_df(hxd, pc_calc_df[['bm_class_applied', 'selected_lob']])
    pc_calc_df   = select_cov_ulr(    hxd, pc_calc_df,  is_bbt,  bbt_param_df,  exp_param_df  )

    # Compute gross ULR net of deductions
    pc_calc_df['total_gg_ulr'] = (pc_calc_df['best_estimate_pre_pc_adj'] * (1 - pc_calc_df['deductions'])).fillna(0)

    # Loop through attr/large/cat fields & compute gross ULR by peril
    for field in ['attr', 'cat', 'large']:
        pc_calc_df[f'{field}_gg_ulr'] = pc_calc_df['total_gg_ulr'] * pc_calc_df[f'{field}_per']

    # Compute expected loss amounts
    pc_calc_df['attr_el']  = pc_calc_df['attr_gg_ulr']  * pc_calc_df['gwp_5623']
    pc_calc_df['large_el'] = pc_calc_df['large_gg_ulr'] * pc_calc_df['gwp_5623']
    pc_calc_df['cat_el']   = pc_calc_df['cat_gg_ulr']   * pc_calc_df['gwp_5623']
    
    mask_rms                         = pc_calc_df["cov_basis_cat"] == "RMS"
    pc_calc_df['cat_weather_el']     = np.where(mask_rms, pc_calc_df['cat_el'], 0)
    pc_calc_df['cat_non_weather_el'] = pc_calc_df['cat_el'] - pc_calc_df['cat_weather_el']

    # Compute stdev amounts = EL * CoV
    pc_calc_df['attr_sd']           = pc_calc_df['attr_el']             * pc_calc_df['attr_cov']
    pc_calc_df['large_sd']          = pc_calc_df['large_el']            * pc_calc_df['large_cov']
    pc_calc_df['cat_non_weather_sd']= pc_calc_df['cat_non_weather_el']  * pc_calc_df['cat_cov']
    pc_calc_df['cat_weather_sd']    = pc_calc_df['cat_weather_el']      * pc_calc_df['cat_cov']

    # fillna on nuumeric columsn with nil
    pc_calc_df[pc_calc_df.select_dtypes('number').columns] = pc_calc_df.select_dtypes('number').fillna(0)

    # Write final DataFrame back to Rater
    rater['pc_calc'] = pc_calc_df

    # Return enriched PC calculation DataFrame
    return pc_calc_df



def initialise_bbt_pc_calculations(hxd, rater):

    # Load PC calculation table into DataFrame from rater
    pc_calc_df                  = rater.get('pc_calc',                pd.DataFrame())
    pc_structure_df             = rater.get('pc_structure',           pd.DataFrame())

    # Restrict to first row for BBT setup
    pc_calc_df = pc_calc_df[:1]

    # Extract rating summary values
    deductions      = hxd.cds.rating_summary.pricing_outputs.deductions_5623
    nwp             = hxd.cds.rating_summary.pricing_outputs.afb_api     
    benchmark       = hxd.cds.rating_summary.pricing_outputs.bbt_class.selected
    best_estimate   = hxd.cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_actuarial_basis.summary.best_estimate_pre_pc_adj

    # Carry across structure metadata
    pc_calc_df['selected_lob']   = pc_structure_df['selected_lob']
    pc_calc_df['is_row_visible'] = pc_structure_df['is_row_visible']

    # Compute GWP and NWP values
    gwp_value               = utils.ratio(nwp, (1 - deductions))
    pc_calc_df['gwp_5623']  = gwp_value # Assigns the single calculated value to the entire column
    pc_calc_df['deductions']= deductions
    pc_calc_df['nwp_5623']  = nwp

    # Assign auto & applied benchmark class
    pc_calc_df['bm_class_auto']    = benchmark
    pc_calc_df['bm_class_applied'] = pc_calc_df['bm_class_override'].fillna(pc_calc_df['bm_class_auto'])

    # Set cov basis fields to BBT for each peril
    for field in ['attr', 'large', 'cat']:
        pc_calc_df[f'cov_basis_{field}'] = "BBT"

    # Exp params not used for BBT
    exp_param_df = None

    # Assign best estimate field
    pc_calc_df['best_estimate_pre_pc_adj'] = best_estimate

    return pc_calc_df, exp_param_df



def initialise_x_bbt_pc_calculations(hxd, rater):

    # Load PC calculation table into DataFrame from rater
    pc_calc_df                  = rater.get('pc_calc',                pd.DataFrame())
    pc_structure_df             = rater.get('pc_structure',           pd.DataFrame())
    limit_profile_df            = rater.get('prem_limit_data',        pd.DataFrame())
    deductions_df               = rater.get('deductions_df',          pd.DataFrame())
    own_experience_summary_df   = rater.get('proj_own_exper_summary', pd.DataFrame())
    final_composition_df        = rater.get('risk_composition_final', pd.DataFrame())
    rat_sum_adeq_act_df         = rater.get('rat_sum_adeq_act', pd.DataFrame())

    # If composition missing, abort
    if final_composition_df.shape[0] == 0:
        return 

    # Assign selected LOBs & assign visibility
    n                            = len(pc_structure_df)
    pc_calc_df                   = pc_calc_df[:n]
    pc_calc_df['selected_lob']   = pc_structure_df['selected_lob']
    pc_calc_df['is_row_visible'] = pc_calc_df['selected_lob'].notna()

    # Aggregate GWP by selected LOB & map
    ss_lob_sum_gwp_5623    = limit_profile_df.groupby('selected_lob')['bst_share_ultimate_gross_premium'].sum()
    pc_calc_df['gwp_5623'] = pc_calc_df['selected_lob'].map(  ss_lob_sum_gwp_5623  ).fillna(0)

    # Map deductions by LOB
    dict_lob_sel_eff_ded     = dict(zip(deductions_df["selected_lob"], deductions_df["selected_effective_deductions"]))
    pc_calc_df['deductions'] = pc_calc_df['selected_lob'].map(  dict_lob_sel_eff_ded  ).fillna(0)

    # Compute NWP = GWP * (1 - deductions)
    pc_calc_df['nwp_5623'] = pc_calc_df['gwp_5623'] * (1 - pc_calc_df['deductions'])

    # Deduplicate composition by LOB
    unique_lobs_comp_df = final_composition_df.drop_duplicates(subset='selected_lob', keep='first')

    # Map benchmark class from composition and apply override if present
    dict_lob_bp_class              = dict(zip(unique_lobs_comp_df['selected_lob'], unique_lobs_comp_df['selected_bp_class']))
    pc_calc_df['bm_class_auto']    = pc_calc_df['selected_lob'].map(   dict_lob_bp_class     )
    pc_calc_df['bm_class_applied'] = pc_calc_df['bm_class_override'].fillna(pc_calc_df['bm_class_auto'])
    
    # Map best estimate values
    dict_lob_best_est = dict(zip(rat_sum_adeq_act_df['selected_lob'], rat_sum_adeq_act_df['best_estimate_pre_pc_adj']))
    pc_calc_df['best_estimate_pre_pc_adj'] = pc_calc_df['selected_lob'].map(   dict_lob_best_est   ).fillna(0)

    # Build experience parameter DataFrame - note these are loss ratios 'selected_attr', 'selected_large', 'selected_cat'
    if (hxd.cds.risk_information.prem_data_available == False) or (rater["policy_data"].shape[0] == 0):
        exp_param_df = None
    else:
        cols_orig = ['selected_lob', 'cov_attr',  'cov_large',  'cov_cat', 'selected_attr', 'selected_large', 'selected_cat']
        cols_new  = ['selected_lob', 'attr_cov',  'large_cov',  'cat_cov', 'attr',          'large',          'cat'         ]       
        exp_param_df = own_experience_summary_df[cols_orig].rename( columns = dict(zip(cols_orig, cols_new))  )

    return pc_calc_df, exp_param_df



def build_bbt_param_df(hxd, pc_calc_df):
    # initialize param df with LOB + bm_class mapping
    bbt_df = pd.DataFrame({  'bm_class': pc_calc_df['bm_class_applied'].values
                            ,'selected_lob': pc_calc_df['selected_lob'].values })

    # load bbt parameters and select year
    bbt_params_df   = hx.params.table_bbt_parameters  # lookup table
    min_year        = bbt_params_df["year"].min()
    max_year        = bbt_params_df["year"].max()
    inception_year  = hxd.cds.standard_fields.inception_date.year
    selected_year   = sorted([min_year, max_year, inception_year])[1]
    bbt_params_df   = bbt_params_df[bbt_params_df['year'] == int(selected_year)]

    # merge bbt parameters into bbt_df conforming column names
    cols_bbt_orig = ['Business Plan Class', 'Att LR', 'Large LR', 'Cat LR' , 'Att COV',  'Large COV', 'Cat COV']
    cols_bbt_new  = ['bm_class',            'attr',   'large',    'cat',     'attr_cov', 'large_cov', 'cat_cov']
    cols_map      = dict(zip(cols_bbt_orig,  cols_bbt_new))
    bbt_params_df = bbt_params_df.rename(  columns=cols_map  )
    bbt_df        = utils.drop_and_merge(bbt_df, bbt_params_df, 'bm_class' ).fillna(0)

    # force loss ratio percents to add to 100%
    bbt_df['total'] = 1
    ss_uplift       = utils.ratio(    bbt_df['total'],    bbt_df[['attr', 'large', 'cat']].sum(axis=1)  )
    bbt_df[['attr', 'large', 'cat']] = bbt_df[['attr', 'large', 'cat']].mul(ss_uplift, axis=0)              

    return bbt_df.fillna(0)



def select_cov_ulr(hxd, pc_calc_df, is_bbt, bbt_param_df, exp_param_df=None):
    # take pc_calc_df and add bbt_param_df after adding '_bbt' to column names to distinguish
    cols            = bbt_param_df.columns.difference( ['bm_class', 'selected_lob'] )
    dict_map_cols   = {col: f"{col}_bbt" for col in cols}
    bbt_param_df    = bbt_param_df.rename (columns = dict_map_cols )
    pc_calc_df      = utils.drop_and_merge( pc_calc_df,  bbt_param_df,  "selected_lob" )

    # default to bbt
    fields = ['attr', 'large', 'cat', 'attr_cov', 'large_cov', 'cat_cov']
    for field in fields :
        pc_calc_df[field] = pc_calc_df[f'{field}_bbt']

    # following only needed where have not imported bbt risk 
    if not is_bbt:
        # take pc_calc_df and add bbt_param_df after adding '_exp' to column names to distinguish
        exp_available = True if exp_param_df is not None else False
        if exp_available:
            cols            = exp_param_df.columns.difference(  ['selected_lob'] )
            dict_map_cols   = {col: f"{col}_exp" for col in cols}
            exp_param_df    = exp_param_df.rename (columns = dict_map_cols )
            pc_calc_df      = utils.drop_and_merge( pc_calc_df,  exp_param_df,  "selected_lob" )

            # setup experience masks
            mask_attr   = pc_calc_df["cov_basis_attr"]  == "Experience"
            mask_large  = pc_calc_df["cov_basis_large"] == "Experience"
            mask_cat    = pc_calc_df["cov_basis_cat"]   == "Experience"
            masks = [mask_attr, mask_large, mask_cat, mask_attr, mask_large, mask_cat]

            # iterate over fields and masks passing experience values where selectrewd
            for field, mask in zip (fields, masks):
                pc_calc_df.loc[mask,field] = pc_calc_df.loc[mask,f'{field}_exp']

        # allow for rms on cat - no easy way to avoid an apply/loop give underlying cat structure
        mask_cat = pc_calc_df["cov_basis_cat"]   == "RMS"
        pc_calc_df.loc[mask_cat, 'cat_cov'] = ( pc_calc_df.loc[mask_cat, 'selected_lob'].apply(lambda lob: get_cat_param_by_lob(hxd, lob, "cov")))
        pc_calc_df.loc[mask_cat, 'cat']     = ( pc_calc_df.loc[mask_cat, 'selected_lob'].apply(lambda lob: get_cat_param_by_lob(hxd, lob, "selected_gn_cat_ulr")))

    # calc total ratio and percent contributions
    pc_calc_df['total']     = pc_calc_df[  ['attr', 'cat', 'large']  ].sum(  axis=1  )  # total ratio
    
    pc_calc_df['large_per'] = utils.ratio(    pc_calc_df['large'],    pc_calc_df['total'] )  # large share
    pc_calc_df['cat_per']   = utils.ratio(    pc_calc_df['cat']  ,    pc_calc_df['total'] )  # cat share
    pc_calc_df['attr_per']  = 1 - pc_calc_df['large_per'] - pc_calc_df['cat_per']
    
    return pc_calc_df



# @time_me
def build_pc_corr_matrix(hxd, rater):
    def bounded(ov, cv):
        val = ov if ov is not None else cv
        if val is None:
            return None
        else:
            return -1.0 if val < -1.0 else (1.0 if val > 1.0 else val)


    # linking to pc & loading the client data df
    pc        = hxd.cds.pc
    long_df   = rater.get('proj_own_exper_detail', pd.DataFrame())
    test      = 'selected_lob' not in long_df.columns

    if test:
        return
    
    # calculate the client correlation matrix
    wide_df   = long_df.pivot(index="yoa", columns="lob_number", values="ultimate_ulr_on_levelled_total")
    wide_df   = wide_df.reindex(sorted(wide_df.columns, key=int), axis=1)
    calc_df   = wide_df.corr().fillna(0)

    # import the override correlation matrix and determine selected
    ovd_l_l   = [ [node.coeff for node in row.cm_col]    for row in pc.cm_ovd ] # Nones remain as Nones ... # accessing an individual value: pc.cm_calc[0].cm_col[0].coeff 
    calc_l_l  = calc_df.values.tolist()
    sel_l_l   = [ [bounded(ov,cv) for ov,     cv     in zip(ov_row,  cv_row)]
                                  for ov_row, cv_row in zip(ovd_l_l, calc_l_l)]
    sel_df    = pd.DataFrame(sel_l_l, index=calc_df.index, columns=calc_df.columns, dtype=object)  # Nones remain as Nones

    # Force the triangle to be complete - using the values in top right and enforcing 1 on the diagonals
    n                         = len(sel_df)
    rng                       = range(n)
    mask_lower                = np.tril(np.ones((n, n), dtype=bool), k=-1)
    sel_df.values[rng, rng]   = 1.0
    sel_df.values[mask_lower] = sel_df.T.values[mask_lower]

    rater['correl_mtx_sel']   = sel_df

    # write back to hxd 
    pc.cm_calc = [ {"cm_col": [{"coeff": float(val)} for val in row]}    for row in calc_df.values  ] # list of dictionaries
    pc.cm_sel  = [ {"cm_col": [{"coeff": float(val)} for val in row]}    for row in  sel_df.values  ] # list of dictionaries


    # write selected lob to override object
    selected_lobs = long_df["selected_lob"].dropna().unique()
    path_calc     = hxd.cds.pc.cm_calc
    path_ovd      = hxd.cds.pc.cm_ovd
    path_sel      = hxd.cds.pc.cm_sel

    for obj_calc, obj_ovd, obj_sel, lob in zip(path_calc, path_ovd, path_sel, selected_lobs):                           # pairs elements from both iterables up to the shortest length
        setattr(obj_calc, "selected_lob", lob)
        setattr(obj_ovd,  "selected_lob", lob)
        setattr(obj_sel,  "selected_lob", lob)                

    return



def build_pc_cals_summary(hxd, pc_calc_df):
    summary_path = hxd.cds.pc.pc_calculations.summary  # target summary path in hxd

    # fields that need GWP-weighted averages
    weighted_fields = [ 'attr_gg_ulr', 'large_gg_ulr', 'cat_gg_ulr', 'total_gg_ulr',
                        'attr_cov', 'large_cov', 'cat_cov'    ]

    # fields that should be summed directly
    fields_to_sum = [   'gwp_5623', 'nwp_5623',
                        'attr_el', 'large_el', 'cat_non_weather_el', 'cat_weather_el',
                        'attr_sd', 'large_sd', 'cat_non_weather_sd', 'cat_weather_sd'    ]

    summary      = {}  # dictionary to hold final results
    df           = pc_calc_df.fillna(0)  # ensure no NaNs in calculations
    gwp_5623_sum = df['gwp_5623'].sum()  # total gross premium
    no_prem      = gwp_5623_sum == 0

    for field in weighted_fields:
        summary[field] = 0 if no_prem else (df['gwp_5623'] * df[field]).sum() / gwp_5623_sum

    for field in fields_to_sum:  # direct sums
        summary[field] = df[field].sum()

    summary["deductions"] = 0 if no_prem else 1 - (summary["nwp_5623"] / gwp_5623_sum)

    # write values into hxd summary object
    for col in fields_to_sum + weighted_fields + ["deductions"]:
        setattr(summary_path, col, summary[col])


