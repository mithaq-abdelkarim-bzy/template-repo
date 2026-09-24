import math as math
import algorithms.rate_constants as constants
import algorithms.validations.rating_summary_validations as validations


def build_projected_gn_ulr_summary(proj_df, hxd):
    # Get the path in the HXD object to store projected GN/ULR summary
    summary_path = hxd.cds.rating_summary.model_gn_ulr.projected_gn_ulr.summary

    # Define columns to be weighted by portfolio percent
    weighted_cols = ['own_exp_gn_ulr',
                     'lloyds_gn_ulr',
                     'beazley_gn_ulr',
                     'bp_gn_ulr',
                     'case_pricing']

    # All summary columns including totals
    summary_cols = ['gn_premium', 'portfolio_percent'] + weighted_cols

    # Initialize summary dictionary
    summary = {}
    summary['gn_premium'] = proj_df['gn_premium'].sum()  # Sum GN premium
    summary['portfolio_percent'] = proj_df['portfolio_percent'].sum()  # Sum portfolio percent

    # Calculate weighted averages for specified columns
    for col in weighted_cols:
        summary[col] = proj_df['portfolio_percent'].dot(
            proj_df[col].fillna(0))  # Weighted sum
        summary[col] = summary[col] if isinstance(summary[col], float) else 0  # Ensure float

    # Set each summary attribute in HXD
    for col in summary_cols:
        setattr(summary_path, col, summary.get(col, 0))

    # Set total deductions
    setattr(
        summary_path,
        'total_deductions',        
        hxd.cds.prem_limit_profile.summary.bst_deductions
    )







def build_model_weights_summary(model_weights_df, proj_df, rating_summary_path):
    # Get path for storing model weights summary
    summary_path = rating_summary_path.model_gn_ulr.model_weights.summary

    # Filter out rows with missing selected_lob
    proj_df = proj_df[proj_df["selected_lob"].notna()]
    model_weights_df = model_weights_df[model_weights_df["selected_lob"].notna()]

    # Columns to calculate weighted values for
    weighted_cols = ['own_experience',
                     'lloyds_proj',
                     'beazley_proj',
                     'bp_proj',
                     'case_pricing']

    # Columns to sum and save
    cols_to_sum = weighted_cols + [
        'weighting_check',
        'model_estimate'
    ]

    summary = {}
    sum_projections = 0

    # Compute weighted sums for each column
    for col in weighted_cols:
        summary[col] = proj_df['portfolio_percent'].dot(model_weights_df[col].fillna(0))
        sum_projections += summary[col]

    # Check if the sum of weights is close to 1
    summary['weighting_check'] = "TRUE" if math.isclose(sum_projections, 1.0) else "FALSE"
    validations.check_model_weightings_sum_value(sum_projections)  # Validate weight sum

    # Compute weighted model estimate
    summary['model_estimate'] = proj_df['portfolio_percent'].dot(model_weights_df['model_estimate'].fillna(0))
    summary['model_estimate'] = summary['model_estimate'] if isinstance(summary['model_estimate'], float) else 0

    # Set each summary attribute in HXD
    for col in cols_to_sum:
        setattr(summary_path, col, summary.get(col, 0))

    return summary


def build_cat_loadings_summary(cat_loading_df, rating_summary_path, proj_df):
    # Get path for cat loadings summary
    summary_path = rating_summary_path.cat_loadings.summary

    # Columns to calculate weighted sums for
    cols = [
        'attr_and_lrg_exp',
        'cat_exp',
        'attr_and_lrg_bp',
        'cat_bp',
        'attr_and_lrg',
        'cat',
        'climate_change_load',
        'nmp_load_general',
        'nmp_load_weather'
    ]

    summary = {}

    # Compute weighted sums and set as attributes
    for col in cols:
        summary[col] = proj_df['portfolio_percent'].dot(
            cat_loading_df[col].fillna(0))
        summary[col] = summary[col] if isinstance(summary[col], float) else 0
        
        setattr(summary_path, col, summary.get(col, 0))


def build_additional_loadings_summary(rating_summary_path, proj_df, additional_loadings_df):
    # Get path for additional loadings summary
    summary_path = rating_summary_path.additional_loadings.summary

    # Columns to calculate weighted sums for
    cols = [
        'anti_selection_charge',
        'uncertainty_charge',
        'additional_charge'
    ]

    summary = {}

    # Compute weighted sums and set as attributes
    for col in cols:
        summary[col] = proj_df['portfolio_percent'].dot(
            additional_loadings_df[col].fillna(0))
        summary[col] = summary[col] if isinstance(summary[col], float) else 0
        
        setattr(summary_path, col, summary.get(col, 0))

    return summary


def build_cat_ulr_summary_totals(rating_summary_path, proj_df, cat_ulr_summary_df):
    # Get path for cat ULR summary
    summary_path = rating_summary_path.cat_ulr_summary.summary

    # Columns to calculate weighted sums for
    cols = [
        'gn_cat_ulr_excl_loads',
        'gn_cat_ulr_inc_loads'
    ]

    summary = {}

    # Compute weighted sums and set as attributes
    for col in cols:
        summary[col] = proj_df['portfolio_percent'].dot(
            cat_ulr_summary_df[col].fillna(0))
        summary[col] = summary[col] if isinstance(summary[col], float) else 0
        
        setattr(summary_path, col, summary.get(col, 0))

    return summary


def build_pricing_adequacy_metrics_summary(hxd, pre_adj, act_basis_df, final_df, proj_df):
    # Get paths for pre-adjusted, actuarial basis, and final pricing summaries
    adeq_path = hxd.cds.rating_summary.pricing_adequacy_metrics
    pre_adj_path = adeq_path.pricing_adequacy_pre_adj.summary
    act_basis_path = adeq_path.pricing_adequacy_actuarial_basis.summary
    final_path = adeq_path.pricing_adequacy_final_pricing.summary

    # Columns to calculate weighted sums for
    weighted_cols = [
        'best_estimate_pre_pc_adj',
        'best_estimate',
        'roc'
    ]

    summary_pre_adj = {}
    summary_act_basis = {}
    summary_final_df = {}

    # Compute weighted sums for pre-adjusted and actuarial basis
    for col in weighted_cols:
        summary_pre_adj[col] = proj_df['portfolio_percent'].dot(
            pre_adj[col].fillna(0))
        summary_act_basis[col] = proj_df['portfolio_percent'].dot(
            act_basis_df[col].fillna(0))

    # Add PC impact if it exists
    pc_impact_summary = hxd.cds.pc.profit_commission.summary.pc_impact
    is_there_profit_commission = hxd.cds.risk_information.is_profit_comission
    summary_act_basis["pc_impact"] = (
        pc_impact_summary 
        if pc_impact_summary is not None 
        and is_there_profit_commission 
        else 0
    )


    bench_lr = constants.benchmark_lr 

    # Compute TPI and BPI metrics
    gn_premium_summary = hxd.cds.rating_summary.model_gn_ulr.projected_gn_ulr.summary.gn_premium
    tp_actuarial_summary = hxd.cds.rating_summary.technical_premium_build_up.summary.tp_actuarial
    summary_act_basis["tpi"] = gn_premium_summary / \
        tp_actuarial_summary if tp_actuarial_summary != 0 else 0
    summary_act_basis["bpi"] = bench_lr / \
        summary_act_basis['best_estimate'] if summary_act_basis['best_estimate'] != 0 else 0

    tp_pre_adj_summary = hxd.cds.rating_summary.technical_premium_build_up.summary.tp_pre_adj
    summary_pre_adj["bpi"] = (bench_lr / summary_pre_adj['best_estimate']
                              ) if summary_pre_adj['best_estimate'] != 0 else 0
    summary_pre_adj["pc_impact"] = (
        summary_act_basis["pc_impact"]
        * summary_act_basis['best_estimate_pre_pc_adj']
        / summary_pre_adj['best_estimate_pre_pc_adj']
    ) if summary_pre_adj['best_estimate_pre_pc_adj'] != 0 else 0
    summary_pre_adj["tpi"] = gn_premium_summary / \
        tp_pre_adj_summary if tp_pre_adj_summary != 0 else 0

    # Compute final weighted columns
    tp_final_summary = hxd.cds.rating_summary.technical_premium_build_up.summary.tp_final
    final_weighted_cols = [
        'uw_adj', 'best_estimate_gn', 'best_estimate_gg', 'roc']
    for col in final_weighted_cols:
        summary_final_df[col] = proj_df['portfolio_percent'].dot(
            final_df[col].fillna(0))
    summary_final_df["bpi"] = bench_lr / \
        summary_final_df['best_estimate_gn'] if summary_final_df['best_estimate_gn'] != 0 else 0
    summary_final_df["tpi"] = gn_premium_summary / \
        tp_final_summary if tp_final_summary != 0 else 0

    # Set attributes for each path
    for col in weighted_cols + ['pc_impact', 'bpi', 'tpi']:
        setattr(pre_adj_path, col, summary_pre_adj.get(col, 0))
        setattr(act_basis_path, col, summary_act_basis.get(col, 0))

    for col in final_weighted_cols + ['bpi', 'tpi']:
        setattr(final_path, col, summary_final_df.get(col, 0))


def build_tech_prem_build_up_summary(hxd, tech_prem_df):
    # Get path for technical premium build-up summary
    tech_prem_summary_path = hxd.cds.rating_summary.technical_premium_build_up.summary
    cols_to_sum = [
        'el_pre_adj',
        'el_actuarial',
        'el_final',
        'tp_pre_adj',
        'tp_actuarial',
        'tp_final',
        'gg_tp_final',
        'gg_bm_final'
    ]

    summary = {}

    # Sum columns and set attributes
    for col in cols_to_sum:
        summary[col] = tech_prem_df[col].sum()
        summary[col] = summary[col] if isinstance(summary[col], float) else 0

        setattr(tech_prem_summary_path, col, summary.get(col, 0))


def build_trifocus_summary_totals(hxd):
    # Get path for trifocus summary
    trifocus_path = hxd.cds.rating_summary.trifocus_summary
    summary_path = hxd.cds.rating_summary

    # Initialize summary dictionary with zero defaults
    summary = {
        'model_estimate': 0,
        'be_before_loads': 0,
        'anti_selection': 0,
        'uncertainty': 0,
        'additional_charge': 0,
        'pc_impact': 0,
        'be_after_pc': 0,
        'uw_adj': 0,
        'be_post_uw': 0,
        'bpi': 0,
        'tpi': 0,
        'roc': 0
    }

    # Populate summary from existing HXD summaries
    summary['model_estimate'] = summary_path.model_gn_ulr.model_weights.summary.model_estimate
    summary['anti_selection'] = summary_path.additional_loadings.summary.anti_selection_charge
    summary['uncertainty'] = summary_path.additional_loadings.summary.uncertainty_charge
    summary['additional_charge'] = summary_path.additional_loadings.summary.additional_charge
    summary['pc_impact'] = summary_path.pricing_adequacy_metrics.pricing_adequacy_actuarial_basis.summary.pc_impact
    summary['be_after_pc'] = summary_path.pricing_adequacy_metrics.pricing_adequacy_actuarial_basis.summary.best_estimate
    summary['be_before_loads'] = (
        summary['be_after_pc'] - summary['anti_selection']
        - summary['uncertainty'] - summary['additional_charge']
    )
    summary['uw_adj'] = summary_path.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary.uw_adj
    summary['be_post_uw'] = summary_path.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary.best_estimate_gn
    summary['bpi'] = summary_path.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary.bpi
    summary['tpi'] = summary_path.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary.tpi
    summary['roc'] = summary_path.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary.roc

    # Set each summary value in trifocus path
    for key, value in summary.items():
        node = getattr(trifocus_path, key)
        setattr(node, "summary", value)
