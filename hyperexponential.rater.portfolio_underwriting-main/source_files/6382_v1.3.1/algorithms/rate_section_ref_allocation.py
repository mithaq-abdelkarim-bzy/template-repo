import pandas                       as pd
import numpy                        as np
import algorithms.rate_constants    as constants
from algorithms.rate_utilities      import pd_df_from_hx_list_v2, ratio, drop_and_merge, write_pd_to_hxd


def allocate_metrics(table_pcts_df, metrics_lob_df, lob_col, ref_cols, metric_cols):
    # setup weights and metrix aligning indices
    wgts    = table_pcts_df.set_index( lob_col)[ref_cols   ].astype(float).fillna(0.0)      # weights : LOB × ref
    metrics = metrics_lob_df.set_index(lob_col)[metric_cols].astype(float).fillna(0.0)      # metrics : LOB × metric
    metrics = metrics.reindex(wgts.index).fillna(0.0)                                       # align indices

    # # normalise columns so each ref column sums to 1
    # wgts.iloc[0, :] = wgts.iloc[0, :].mask(wgts.sum(axis=0).eq(0), 1.0)                     # if a section_ref has no weights, default to first LOB
    # col_sums        = wgts.sum(axis=0).replace(0, np.nan)                                   #
    # wgts            = wgts.div(col_sums, axis=1).fillna(0.0)

    # normalise so wgts sum to 1
    # total = wgts.to_numpy().sum()
    # wgts  = wgts / total

    # normalise rows so each row sums to 1
    row_sums = wgts.sum(axis=1).replace(0, np.nan)
    wgts = wgts.div(row_sums, axis=0).fillna(0.0)


    # matrix multiply: (ref × lob) @ (lob × metric) → (ref × metric)
    out_df = pd.DataFrame(wgts.T.to_numpy() @ metrics.to_numpy(), index=ref_cols, columns=metric_cols) # using numpy for speed could have done wgts.T.dot(metrics)
    out_df.index.name = "section_ref"
    return out_df.reset_index()



def drop_blank_selected_lob(df):
    if df.empty or "selected_lob" not in df.columns:
        return df
    return df[df["selected_lob"].astype(str).str.strip().ne("") & df["selected_lob"].notna()]


def rate_section_ref_allocation(hxd, rater):

    # path
    path            = hxd.cds.rating_summary.section_ref_allocation
    
    # number of references
    max_num_refs    = constants.NUMBER_SECTION_REFERENCES
    sel_num_refs    = path.num_ref

    # df cols
    deductions_cols = ['selected_lob', 'market_deductions', 'mga_fee', 'facility_brokerage', 'leaders_fee', 'service_fee', 'other', 'selected_effective_deductions']
    adeq_pre_uw_cols= ['selected_lob', 'bpi', 'tpi', 'best_estimate',    'roc', 'pc_impact']
    adeq_pst_uw_cols= ['selected_lob', 'bpi', 'tpi', 'best_estimate_gn', 'roc']
    prem_limit_cols = ['selected_lob', 'bst_share_ultimate_gross_premium', 'future_ultimate_gross_prem']
    rarc_cols = ['selected_lob', 'year_0/selected']

    #### TODO ****** MOVE READ/WRITE on HXD lists to rate_RATER page and then just save to rater
    # load dfs
    alloc_df        = pd_df_from_hx_list_v2(path.table_pcts)
    deductions_df   = rater.get("deductions_df",     pd.DataFrame())
    adeq_pre_uw_df  = rater.get("rat_sum_adeq_act",  pd.DataFrame())
    adeq_pst_uw_df  = rater.get("rat_sum_adeq_final",pd.DataFrame())
    prem_limit_df   = rater.get("prem_limit_data",   pd.DataFrame())
    rarc_df         = rater.get("rate_change_data",  pd.DataFrame())

    # filter dfs to non blank lobs
    # alloc_df        = drop_blank_selected_lob(alloc_df)           # not allocation df as it is blank until assigned!
    deductions_df   = drop_blank_selected_lob(deductions_df)
    adeq_pre_uw_df  = drop_blank_selected_lob(adeq_pre_uw_df)
    adeq_pst_uw_df  = drop_blank_selected_lob(adeq_pst_uw_df)
    prem_limit_df   = drop_blank_selected_lob(prem_limit_df)
    rarc_df         = drop_blank_selected_lob(rarc_df)

    # exit if we have no data
    if len(deductions_df)==0:
        return

    # rename cols
    adeq_pre_uw_new_cols= ['selected_lob', 'bpi_pre', 'tpi_pre', 'pflr_pre', 'roc_pre', 'pc_impact']
    adeq_pst_uw_new_cols= ['selected_lob', 'bpi_pst', 'tpi_pst', 'pflr_pst', 'roc_pst']
    prem_limit_new_cols = ['selected_lob', 'qp_gg_bst', 'qp_gg_100']
    rarc_new_cols = ['selected_lob', 'rarc']
    adeq_pre_uw_df      = (adeq_pre_uw_df.rename( columns=dict(zip(adeq_pre_uw_cols, adeq_pre_uw_new_cols)))
                                         .reindex(columns=adeq_pre_uw_new_cols).fillna(0.0)                 )    # reindex selects the columns forcing them to np.nan if they dont exist
    adeq_pst_uw_df      = (adeq_pst_uw_df.rename( columns=dict(zip(adeq_pst_uw_cols, adeq_pst_uw_new_cols)))
                                         .reindex(columns=adeq_pst_uw_new_cols).fillna(0.0)                 )
    prem_limit_df       = (prem_limit_df.rename(  columns=dict(zip(prem_limit_cols,  prem_limit_new_cols )))
                                        .reindex(columns=prem_limit_new_cols  ).fillna(0.0)                 
                                        .groupby('selected_lob', as_index=False).sum(numeric_only=True)     )    # agg by selected_lob (prem_limit rows are per facility_lob)
    deductions_df       = (deductions_df.reindex(columns=deductions_cols      ).fillna(0.0)                 )
    rarc_df            = (rarc_df.rename( columns=dict(zip(rarc_cols, rarc_new_cols)))
                                         .reindex(columns=rarc_new_cols).fillna(0.0)                 )

    # drop and merge
    df  = drop_and_merge(deductions_df, adeq_pre_uw_df, ['selected_lob'] )
    df  = drop_and_merge(df,            adeq_pst_uw_df, ['selected_lob'] )
    df  = drop_and_merge(df,            prem_limit_df,  ['selected_lob'] )
    df  = drop_and_merge(df,            rarc_df,  ['selected_lob'] )

    # calculating/converting to additive values ready for allocation
    df['qp_gn_bst']     = df['qp_gg_bst']  *  ( 1 - df['selected_effective_deductions'] )

    df['el_pre']        = df['qp_gn_bst']  *  ( df['pflr_pre']  +  df['pc_impact']      )  
    df['el_pst']        = df['qp_gn_bst']  *  ( df['pflr_pst']  +  df['pc_impact']      )

    df['bp_gg_bst_pre'] = ratio(df['qp_gg_bst'], df['bpi_pre'])
    df['bp_gg_bst_pst'] = ratio(df['qp_gg_bst'], df['bpi_pst'])
    df['tp_gg_bst_pre'] = ratio(df['qp_gg_bst'], df['tpi_pre'])
    df['tp_gg_bst_pst'] = ratio(df['qp_gg_bst'], df['tpi_pst'])

    df['bp_gn_bst_pre'] = ratio(df['qp_gn_bst'], df['bpi_pre'])
    df['bp_gn_bst_pst'] = ratio(df['qp_gn_bst'], df['bpi_pst'])
    df['tp_gn_bst_pre'] = ratio(df['qp_gn_bst'], df['tpi_pre'])
    df['tp_gn_bst_pst'] = ratio(df['qp_gn_bst'], df['tpi_pst'])

    df['amt_pc_impact']                     = df['qp_gg_bst']  *  df['pc_impact']
    df['amt_roc_bst_pre']                   = df['qp_gn_bst']  *  df['roc_pre']                 # this is not exactly right but should facilitate an approximate allocation check happy - spoke to YZ - all good # new formula requested by jd 21-april-2026 focus on net
    df['amt_roc_bst_pst']                   = df['qp_gn_bst']  *  df['roc_pst']                 # this is not exactly right but should facilitate an approximate allocation check happy - spoke to YZ - all good

    df['amt_market_deductions']             = df['qp_gg_bst']  *  df['market_deductions']
    df['amt_mga_fee']                       = df['qp_gg_bst']  *  df['mga_fee']
    df['amt_facility_brokerage']            = df['qp_gg_bst']  *  df['facility_brokerage']
    df['amt_leaders_fee']                   = df['qp_gg_bst']  *  df['leaders_fee']
    df['amt_service_fee']                   = df['qp_gg_bst']  *  df['service_fee']
    df['amt_other']                         = df['qp_gg_bst']  *  df['other']
    df['amt_selected_effective_deductions'] = df['qp_gg_bst']  *  df['selected_effective_deductions']

    df['implied_expiry']                    = df['qp_gn_bst'] / df['rarc']

    # listing out the columns in df we want to use
    main_cols   = [   'qp_gg_bst',     'qp_gg_100',       'qp_gn_bst'
                    , 'el_pre',        'el_pst'
                    , 'bp_gg_bst_pre', 'bp_gg_bst_pst',   'tp_gg_bst_pre',    'tp_gg_bst_pst'
                    , 'bp_gn_bst_pre', 'bp_gn_bst_pst',   'tp_gn_bst_pre',    'tp_gn_bst_pst'
                    , 'amt_pc_impact', 'amt_roc_bst_pre', 'amt_roc_bst_pst'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                    , 'amt_market_deductions',            'amt_mga_fee',      'amt_facility_brokerage'
                    , 'amt_leaders_fee',                  'amt_service_fee',  'amt_other'
                    , 'amt_selected_effective_deductions'
                    , 'implied_expiry']

    # adding selected_lob to alloc_df and assigning cols
    alloc_df['selected_lob']    = adeq_pre_uw_df['selected_lob'].reset_index(drop=True).reindex(range(len(alloc_df))).fillna('')
    alloc_cols                  = [f'ref_{i:02d}' for i in range(1,max_num_refs + 1)]                 # gives format as follows ['ref_01', 'ref_02', 'ref_03', 'ref_04', 'ref_05'] 
    alloc_df['label']           = alloc_df['selected_lob']                                            # this is the name of the outputted column
    alloc_df['is_row_visible']  = alloc_df['selected_lob'].ne('') 

    # calculating the output df
    out_df = allocate_metrics(alloc_df, df, 'selected_lob', alloc_cols, main_cols)

    # recalculating the metrics in the output for the specified columns
    out_df['section_ref']                   = [getattr(path.section_ref,f'ref_{i:02}') for i in range(1,max_num_refs + 1)]
    out_df['trifocus']                      = [getattr(path.trifocus   ,f'ref_{i:02}') for i in range(1,max_num_refs + 1)]
    out_df['status']                        = hxd.cds.risk_information.deal_status
    
    out_df['market_deductions']             = ratio(out_df['amt_market_deductions'],             out_df['qp_gg_bst'])
    out_df['mga_fee']                       = ratio(out_df['amt_mga_fee'],                       out_df['qp_gg_bst'])
    out_df['facility_brokerage']            = ratio(out_df['amt_facility_brokerage'],            out_df['qp_gg_bst'])
    out_df['leaders_fee']                   = ratio(out_df['amt_leaders_fee'],                   out_df['qp_gg_bst'])
    out_df['service_fee']                   = ratio(out_df['amt_service_fee'],                   out_df['qp_gg_bst'])
    out_df['other']                         = ratio(out_df['amt_other'],                         out_df['qp_gg_bst'])
    out_df['selected_effective_deductions'] = ratio(out_df['amt_selected_effective_deductions'], out_df['qp_gg_bst'])
    
    out_df['pc_impact']                     = ratio(out_df['amt_pc_impact'],                     out_df['qp_gn_bst']) # notice using gn consistent with the standard pflr  
    out_df['written_line']                  = ratio(out_df['qp_gg_bst'],                         out_df['qp_gg_100'])

    out_df['rarc']                          = ratio(out_df['qp_gn_bst'],                         out_df['implied_expiry'])

    # out_df['quoted_premium_gg_bst']         = out_df['qp_gg_bst']                                           
    # out_df['technical_premium_gg_bst']      = out_df['tp_gg_bst_pst']
    # out_df['benchmark_premium_gg_bst']      = out_df['bp_gg_bst_pst']

    out_df['quoted_premium_gn_bst']         = out_df['qp_gn_bst']
    out_df['technical_premium_gn_bst']      = out_df['tp_gn_bst_pst']
    out_df['benchmark_premium_gn_bst']      = out_df['bp_gn_bst_pst']
    out_df['technical_premium_gn_bst_pre']  = out_df['tp_gn_bst_pre']
    out_df['benchmark_premium_gn_bst_pre']  = out_df['bp_gn_bst_pre']

    out_df['quoted_premium_gg_bst']         = ratio(out_df['qp_gn_bst'],     1 - out_df['selected_effective_deductions'])   # new formula requested by jd 21-april-2026 focus on net and infer gross
    out_df['technical_premium_gg_bst']      = ratio(out_df['tp_gn_bst_pst'], 1 - out_df['selected_effective_deductions'])   # new formula requested by jd 21-april-2026 focus on net and infer gross                       
    out_df['benchmark_premium_gg_bst']      = ratio(out_df['bp_gn_bst_pst'], 1 - out_df['selected_effective_deductions'])   # new formula requested by jd 21-april-2026 focus on net and infer gross
    out_df['technical_premium_gg_bst_pre']  = ratio(out_df['tp_gn_bst_pre'], 1 - out_df['selected_effective_deductions'])   # new formula requested by jd 21-april-2026 focus on net and infer gross                       
    out_df['benchmark_premium_gg_bst_pre']  = ratio(out_df['bp_gn_bst_pre'], 1 - out_df['selected_effective_deductions'])   # new formula requested by jd 21-april-2026 focus on net and infer gross

    out_df['tpi']                           = ratio(out_df['qp_gn_bst'],                     out_df['tp_gn_bst_pst'])       # new formula requested by jd 21-april-2026 focus on net
    out_df['bpi']                           = ratio(out_df['qp_gn_bst'],                     out_df['bp_gn_bst_pst'])       # new formula requested by jd 21-april-2026 focus on net
    out_df['pflr']                          = ratio(out_df['el_pst'],                            out_df['qp_gn_bst'])       # notice using gn consistent with the standard pflr  
    out_df['roc']                           = ratio(out_df['amt_roc_bst_pst'],                   out_df['qp_gn_bst'])       # new formula requested by jd 21-april-2026 focus on net

    out_df['tpi_pre_uw_adj']                = ratio(out_df['qp_gn_bst'],                     out_df['tp_gn_bst_pre'])       # new formula requested by jd 21-april-2026 focus on net
    out_df['bpi_pre_uw_adj']                = ratio(out_df['qp_gn_bst'],                     out_df['bp_gn_bst_pre'])       # new formula requested by jd 21-april-2026 focus on net
    out_df['pflr_pre_uw_adj']               = ratio(out_df['el_pre'],                            out_df['qp_gn_bst'])       # notice using gn consistent with the standard pflr  
    out_df['roc_pre_uw_adj']                = ratio(out_df['amt_roc_bst_pre'],                   out_df['qp_gn_bst'])       # new formula requested by jd 21-april-2026 focus on net

    out_df['uw_adj_impact']                 = ratio(out_df['el_pst'],                            out_df['el_pre'   ])

    #### TODO ****** MOVE READ/WRITE on HXD lists to rate_RATER page and then just save to rater
    # write output df back to hxd
    out_df              = out_df.head(sel_num_refs)
    out_cols            = [ 'section_ref',          'status',         'trifocus',          'market_deductions',   'mga_fee'   
                           ,'facility_brokerage',   'leaders_fee',    'service_fee',       'selected_effective_deductions'
                           ,'other',                'pc_impact',      'written_line',      'uw_adj_impact'
                           ,'tpi',                  'bpi',            'pflr',              'roc'
                           ,'tpi_pre_uw_adj',       'bpi_pre_uw_adj', 'pflr_pre_uw_adj',   'roc_pre_uw_adj'     
                           ,'quoted_premium_gg_bst',       'quoted_premium_gn_bst'     
                           ,'technical_premium_gg_bst',    'technical_premium_gn_bst',     'technical_premium_gg_bst_pre',    'technical_premium_gn_bst_pre'
                           ,'benchmark_premium_gg_bst',    'benchmark_premium_gn_bst',     'benchmark_premium_gg_bst_pre',    'benchmark_premium_gn_bst_pre'
                           ,'rarc'              
                           ]
    path.metrics_by_ref = out_df[out_cols].fillna(0).to_dict(orient="records")        # passing as dictionary as all outputs 

    summary_df = calcualte_section_ref_allocation_summary(df)
    summary_cols        = ['market_deductions',   'mga_fee'   
                           ,'facility_brokerage',   'leaders_fee',    'service_fee',       'selected_effective_deductions'
                           ,'other',                'pc_impact',      'written_line',      'uw_adj_impact'
                           ,'tpi',                  'bpi',            'pflr',              'roc'
                           ,'tpi_pre_uw_adj',       'bpi_pre_uw_adj', 'pflr_pre_uw_adj',   'roc_pre_uw_adj'     
                           ,'quoted_premium_gg_bst',       'quoted_premium_gn_bst'     
                           ,'technical_premium_gg_bst',    'technical_premium_gn_bst',     'technical_premium_gg_bst_pre',    'technical_premium_gn_bst_pre'
                           ,'benchmark_premium_gg_bst',    'benchmark_premium_gn_bst',     'benchmark_premium_gg_bst_pre',    'benchmark_premium_gn_bst_pre'
                           ,'rarc'              
                           ]
    #path.metrics_summary = summary_df[summary_cols].fillna(0).to_dict(orient="records")        # passing as dictionary as all outputs 

    for col in summary_cols:
        setattr(
            path.metrics_summary,
            col,
            summary_df[col].iloc[0]
        )

    ## write allocation df back to hxd
    # helper calcs
    total_pcts_by_ref = alloc_df[alloc_cols].sum(axis=0)
    
    # totals list
    total_df          = alloc_df[['label','is_row_visible']]
    total_df['total'] = alloc_df[alloc_cols].sum(axis=1)
    total_df['check'] = total_df['total'].between(0.99,1.01).map({True: 'ok', False: 'check'})
    
    # write to hxd
    path.total_pcts_by_ref = total_pcts_by_ref.to_dict()    # assigning direct to the structure node
    write_pd_to_hxd(alloc_df, path.table_pcts, ['label','is_row_visible'])

    path_non_cds            = hxd.non_cds.rating_summary.section_ref_allocation
    path_non_cds.show_refs  ={f'ref_{i:02d}': (False if i>sel_num_refs else True) for i in range(1,max_num_refs + 1)}
    
    path.total_pcts_by_lob      = total_df.to_dict(orient="records")   # assigning direct to the structure node

    # Showing premium by LOB before selecting the %s
    lob_premium_df = df[['selected_lob', 'qp_gn_bst']].copy()

    lob_premium_df = (
        lob_premium_df
        .rename(columns={
            'selected_lob': 'label',
            'qp_gn_bst': 'total'
        })
    )

    lob_premium_df['is_row_visible'] = lob_premium_df['label'].ne('')
    path.premium_by_lob      = lob_premium_df.to_dict(orient="records") 



def calcualte_section_ref_allocation_summary(df):

    total_cols = [
        'qp_gg_bst',
        'qp_gg_100',
        'qp_gn_bst',
        'el_pre',
        'el_pst',
        'bp_gn_bst_pre',
        'bp_gn_bst_pst',
        'tp_gn_bst_pre',
        'tp_gn_bst_pst',
        'amt_pc_impact',
        'amt_roc_bst_pre',
        'amt_roc_bst_pst',
        'amt_market_deductions',
        'amt_mga_fee',
        'amt_facility_brokerage',
        'amt_leaders_fee',
        'amt_service_fee',
        'amt_other',
        'amt_selected_effective_deductions',
        'implied_expiry'
    ]

    out = pd.DataFrame([{
        c: df[c].sum()
        for c in total_cols
    }])

    # deductions
    out['market_deductions'] = ratio(out['amt_market_deductions'], out['qp_gg_bst'])
    out['mga_fee']           = ratio(out['amt_mga_fee'], out['qp_gg_bst'])
    out['facility_brokerage']= ratio(out['amt_facility_brokerage'], out['qp_gg_bst'])
    out['leaders_fee']       = ratio(out['amt_leaders_fee'], out['qp_gg_bst'])
    out['service_fee']       = ratio(out['amt_service_fee'], out['qp_gg_bst'])
    out['other']             = ratio(out['amt_other'], out['qp_gg_bst'])

    out['selected_effective_deductions'] = ratio(
        out['amt_selected_effective_deductions'],
        out['qp_gg_bst']
    )

    out['pc_impact'] = ratio(
        out['amt_pc_impact'],
        out['qp_gn_bst']
    )

    out['written_line'] = ratio(
        out['qp_gg_bst'],
        out['qp_gg_100']
    )

    out['rarc'] = ratio(out['qp_gn_bst'], out['implied_expiry'])

    # premiums
    out['quoted_premium_gn_bst'] = out['qp_gn_bst']

    out['technical_premium_gn_bst']     = out['tp_gn_bst_pst']
    out['benchmark_premium_gn_bst']     = out['bp_gn_bst_pst']
    out['technical_premium_gn_bst_pre'] = out['tp_gn_bst_pre']
    out['benchmark_premium_gn_bst_pre'] = out['bp_gn_bst_pre']

    out['quoted_premium_gg_bst'] = ratio(
        out['qp_gn_bst'],
        1 - out['selected_effective_deductions']
    )

    out['technical_premium_gg_bst'] = ratio(
        out['tp_gn_bst_pst'],
        1 - out['selected_effective_deductions']
    )

    out['benchmark_premium_gg_bst'] = ratio(
        out['bp_gn_bst_pst'],
        1 - out['selected_effective_deductions']
    )

    out['technical_premium_gg_bst_pre'] = ratio(
        out['tp_gn_bst_pre'],
        1 - out['selected_effective_deductions']
    )

    out['benchmark_premium_gg_bst_pre'] = ratio(
        out['bp_gn_bst_pre'],
        1 - out['selected_effective_deductions']
    )

    # indices
    out['tpi'] = ratio(
        out['qp_gn_bst'],
        out['tp_gn_bst_pst']
    )

    out['bpi'] = ratio(
        out['qp_gn_bst'],
        out['bp_gn_bst_pst']
    )

    out['pflr'] = ratio(
        out['el_pst'],
        out['qp_gn_bst']
    )

    out['roc'] = ratio(
        out['amt_roc_bst_pst'],
        out['qp_gn_bst']
    )

    out['tpi_pre_uw_adj'] = ratio(
        out['qp_gn_bst'],
        out['tp_gn_bst_pre']
    )

    out['bpi_pre_uw_adj'] = ratio(
        out['qp_gn_bst'],
        out['bp_gn_bst_pre']
    )

    out['pflr_pre_uw_adj'] = ratio(
        out['el_pre'],
        out['qp_gn_bst']
    )

    out['roc_pre_uw_adj'] = ratio(
        out['amt_roc_bst_pre'],
        out['qp_gn_bst']
    )

    out['uw_adj_impact'] = ratio(
        out['el_pst'],
        out['el_pre']
    )

    return out
