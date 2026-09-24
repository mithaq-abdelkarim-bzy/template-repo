import hx
import pandas as pd
import numpy as np
import algorithms.rate_utilities as utils
import algorithms.rate_constants as constants
import algorithms.validations.rating_summary_validations as validations
from algorithms                                          import parameter_tables_schema as params

def rate_rating_summary_bbt(hxd, rater):
    
    # get paths
    summary_path = hxd.cds.rating_summary                       # Get the rating summary path
    pricing_outputs_path = summary_path.pricing_outputs         # Get the pricing outputs path
    
    # validate tpi year
    incept_yr            = hxd.hx_core.inception_date.year
    tpi_year             = hxd.cds.rating_summary.technical_premium_build_up.tpi_year.selected
    validations.check_tpi_year_value(tpi_year)
    tpi_year             = tpi_year or incept_yr

    # Initialize summary with override and output fields
    summary = init_summary_fields(pricing_outputs_path)

    # Calculate GN, CAT, and attr/large values
    calculate_pricing_outputs(summary, pricing_outputs_path)

    # Add anti-selection, uncertainty, and additional charges
    calculate_additional_loadings(summary, hxd)

    # Compute pre-technical-premium pricing adequacy metrics
    calculate_pricing_adequacy_metrics_pre_tech_prem(summary, hxd, rater)

    # Apply technical premium adjustments
    calculate_tech_prem_bbt(
        hxd,
        summary,
        summary['pre_adj'],
        summary['act_basis'],
        summary['final']
    )

    # Compute post-technical-premium metrics
    calculate_pricing_adequacy_metrics_post_tech_prem(summary, tpi_year)

    # Save metrics back to summary path
    save_pricing_adequacy_metrics_fields(summary, summary_path)

    # Calculate CAT ULR metrics
    calculate_cat_ulr(summary, summary_path)

    # Return the summary dictionary
    return summary


def init_summary_fields(pricing_outputs_path):
    # Create empty summary dict
    summary = {}
    # List of override fields
    override_fields = ['bbt_gn_ulr', 'bbt_gn_cat_ulr', 'deductions_623_2623']
    # List of output fields
    output_fields = ['deductions_5623', 'afb_api', 'tracker_class']

    for field in override_fields + output_fields:
        # Get the value from pricing outputs
        value = getattr(pricing_outputs_path, field)
        if field in override_fields:
            # Use selected value for overrides
            value = value.selected
        # Default to 0 if value is None
        summary[field] = value if value is not None else 0

    return summary


def calculate_pricing_outputs(summary, pricing_outputs_path):
    # Compute adjusted GN value
    # Calculate the numerator
    numerator = summary['bbt_gn_ulr'] * (1 - summary['deductions_623_2623'])

    # Calculate the denominator
    denominator = (1 - summary['deductions_5623'])

    # Use np.where to conditionally perform the division
    summary['gn_ulr_5623'] = np.where(
        denominator == 0,
        0,  # If denominator is 0, set result to 0
        numerator / denominator # Otherwise, perform the division
    )   

    # Calculate CAT ratio
    summary['cat_calculated'] = (
        summary['bbt_gn_cat_ulr'] / summary['bbt_gn_ulr']
        if summary['bbt_gn_ulr'] != 0
        else 0
    )

    # Use overridden CAT if available
    summary['cat'] = (
        pricing_outputs_path.cat.selected
        if pricing_outputs_path.cat.is_overridden
        else summary['cat_calculated']
    )

    # Compute complementary attr_and_large
    summary['attr_and_large'] = 1 - summary['cat']

    # Store calculated values back in pricing outputs
    pricing_outputs_path.gn_ulr_5623 = summary['gn_ulr_5623']
    pricing_outputs_path.cat.calculated = summary['cat_calculated']
    pricing_outputs_path.attr_and_large.calculated = summary['attr_and_large']


def calculate_additional_loadings(summary, hxd):
    # Get the summary path
    summary_path = hxd.cds.rating_summary

    # Get anti-selection charge
    summary['anti_selection'] = hxd.cds.anti_selection.matrix.overall_selected.final_selected.selected
    # Get uncertainty charge
    summary['uncertainty'] = hxd.cds.uncertainty.matrix.overall_selected.final_selected.selected
    # Get additional BBT charge
    summary['additional_charge'] = summary_path.additional_loadings.summary.additional_charge_bbt

    # Save charges to summary path
    summary_path.additional_loadings.summary.anti_selection_charge = summary['anti_selection']
   
    summary_path.additional_loadings.summary.uncertainty_charge = summary['uncertainty']


def get_pc_impact(hxd, best_estimate_pre_pc_adj_ref_bbt, rater):
    # Get paths
    pc_path = hxd.cds.pc.profit_commission
    po_path = hxd.cds.rating_summary.pricing_outputs
    
    # Check if profit commission exists
    pc_selected = hxd.cds.risk_information.is_profit_comission
    pc_available= len(pc_path.details) and pc_selected

    if pc_available:
        pc_df   = rater.get("pc_details", pd.DataFrame())
        po_path.bbt_pc.calculated = pc_df['pc_impact'].iloc[0]
    else:
        # No profit commission
        po_path.bbt_pc.calculated = 0

    # set pc equal to selected value to accommodate overrides
    pc = po_path.bbt_pc.selected

    return pc


def init_actuarial_basis(hxd, summary, rater):
    # Initialize actuarial basis dict
    summary['act_basis'] = {}

    # Best estimate before profit commission
    summary['act_basis']['best_estimate_pre_pc_adj'] = (
        summary['gn_ulr_5623']
        + summary['uncertainty']
        + summary['anti_selection']
        + summary['additional_charge']
    )

    # Get profit commission impact
    pc_impact = get_pc_impact(hxd, summary['act_basis']['best_estimate_pre_pc_adj'], rater)
    summary['act_basis']['pc_impact'] = pc_impact

    # Total best estimate including profit commission
    summary['act_basis']['best_estimate'] = (
        summary['act_basis']['pc_impact']
        + summary['act_basis']['best_estimate_pre_pc_adj']
    )

    # Compute baseline premium index
    bench_lr = constants.benchmark_lr
    summary['act_basis']['bpi'] = (
        bench_lr / summary['act_basis']['best_estimate']
        if summary['act_basis']['best_estimate'] != 0
        else 0
    )


def init_pre_adjustment(summary):
    # Initialize pre-adjustment dict
    summary['pre_adj'] = {}

    # Best estimate pre-PC adjustment
    summary['pre_adj']['best_estimate_pre_pc_adj'] = summary['gn_ulr_5623']

    # Scale profit commission proportionally
    summary['pre_adj']['pc_impact'] = (
        summary['act_basis']['pc_impact']
        * summary['act_basis']['best_estimate_pre_pc_adj']
        / summary['pre_adj']['best_estimate_pre_pc_adj']
        if summary['pre_adj']['best_estimate_pre_pc_adj'] != 0
        else 0
    )

    # Total pre-adjustment best estimate
    summary['pre_adj']['best_estimate'] = (
        summary['pre_adj']['pc_impact']
        + summary['pre_adj']['best_estimate_pre_pc_adj']
    )

    # Baseline premium index   
    bench_lr = constants.benchmark_lr
    summary['pre_adj']['bpi'] = (
        bench_lr / summary['pre_adj']['best_estimate']
        if summary['pre_adj']['best_estimate'] != 0
        else 0
    )


def init_final(hxd, summary):
    # Get summary path
    summary_path = hxd.cds.rating_summary

    # Initialize final dict
    summary['final'] = {}

    # Underwriting-adjusted BBT
    summary['final']['uw_adj_bbt'] = summary_path.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary.uw_adj_bbt or 0

    # Best estimate gross net
    summary['final']['best_estimate_gn'] = ( summary['final']['uw_adj_bbt'] + summary['act_basis']['best_estimate'] )

    # Best estimate gross general
    summary['final']['best_estimate_gg'] = ( summary['final']['best_estimate_gn']  * (1 - summary['deductions_5623'])   )

    # Baseline premium index
    bench_lr = constants.benchmark_lr    
    summary['final']['bpi'] = ( bench_lr / summary['final']['best_estimate_gn'] if summary['final']['best_estimate_gn'] != 0  else 0    )


def calculate_pricing_adequacy_metrics_pre_tech_prem(summary, hxd, rater):
    # Compute actuarial basis
    init_actuarial_basis(hxd, summary, rater)
    # Compute pre-adjustment metrics
    init_pre_adjustment(summary)
    # Compute final metrics
    init_final(hxd, summary)


def get_value_from_tpi_params(df, mask, column, default=0):
    # Get values from DataFrame using mask and column
    values = df.loc[mask, column].values
    # Return first value if exists, else default
    return values[0] if len(values) > 0 else default


def calculate_tech_prem_bbt(hxd, summary, pre_adj_summary, act_basis_summary, final_summary):
    # Get the rating summary path
    summary_path = hxd.cds.rating_summary
    # Load TPI parameters DataFrame
    tpi_params_df   = params.tp_parameters.df()
    # Get TPI year from summary path
    incept_yr = hxd.hx_core.inception_date.year
    tpi_year  = summary_path.technical_premium_build_up.tpi_year.selected or incept_yr

    # Calculate expected losses for pre-adjustment, actuarial, and final
    summary['el_pre_adj'] = pre_adj_summary['best_estimate'] * summary['afb_api']
    summary['el_actuarial'] = act_basis_summary['best_estimate'] * summary['afb_api']
    summary['el_final'] = final_summary['best_estimate_gn'] * summary['afb_api']

    # Create mask to select correct TPI row
    tpi_mask = (tpi_params_df["business_plan_class"] == summary['tracker_class']) & (tpi_params_df["year"] == tpi_year)

    # Retrieve TPI parameters
    summary['net_expense']      = get_value_from_tpi_params(tpi_params_df, tpi_mask, "var_exp")
    summary['inv_income']       = get_value_from_tpi_params(tpi_params_df, tpi_mask, "inv_inc")
    summary['ri_premium']       = get_value_from_tpi_params(tpi_params_df, tpi_mask, "cost_of_ri")
    summary['ri_recoveries']    = get_value_from_tpi_params(tpi_params_df, tpi_mask, "ri_rec")
    summary['capital_required'] = get_value_from_tpi_params(tpi_params_df, tpi_mask, "capital_req")
    summary['target_roc']       = get_value_from_tpi_params(tpi_params_df, tpi_mask, "roc")

    # Calculate factor for tech premium adjustment
    if tpi_year < 2026:
        summary["factor"] = ( 1 -  summary['net_expense']
                                    - (summary['ri_premium'] - summary['ri_recoveries'])
                                    +  summary['inv_income'] * (1 - summary['ri_premium'])
                                    - (summary['target_roc'] * summary['capital_required'] * (1 - summary['ri_premium']))    )
    else:
        summary["factor"] = ( 1 -  summary['net_expense']
                                    - (summary['ri_premium'] - summary['ri_recoveries'])
                                    +  summary['inv_income'] 
                                    - (summary['target_roc'] * summary['capital_required'])    )



    # Calculate technical premiums for pre-adjustment, actuarial, and final
    summary['tp_pre_adj'] = summary['el_pre_adj'] / summary['factor'] if summary['factor'] != 0 else 0
    summary['tp_actuarial'] = summary['el_actuarial'] / summary['factor'] if summary['factor'] != 0 else 0
    summary['tp_final'] = summary['el_final'] / summary['factor'] if summary['factor'] != 0 else 0

    # Calculate gross general final values
    # Calculate the denominator    
    denominator = (1 - summary["deductions_5623"])

    # Use np.where to conditionally perform the division
    summary["gg_tp_final"] = np.where(
        denominator == 0,
        0,  # If denominator is 0, set result to NaN
        summary['tp_final'] / denominator # Otherwise, perform the division
    )
    bench_lr = constants.benchmark_lr 
    summary["gg_bm_final"] = summary["el_final"] / bench_lr

    # List of fields to push to HX nodes
    tech_prem_fields = [
        'el_pre_adj', 'el_actuarial', 'el_final', 'net_expense', 'inv_income',
        'ri_premium', 'ri_recoveries', 'capital_required', 'target_roc',
        'tp_pre_adj', 'tp_actuarial', 'tp_final', 'gg_tp_final', 'gg_bm_final'
    ]

    # Save calculated tech premium fields to HX summary nodes
    for field in tech_prem_fields:
        node = summary_path.technical_premium_build_up.summary
        setattr(node, field, summary[field])


def calculate_tpi_roc(summary, basis, tp_basis, tpi_year):
    # Determine estimate field depending on basis
    estimate_field = "best_estimate_gn" if basis == "final" else "best_estimate"

    # Calculate TPI ratio
    summary[basis]['tpi'] = summary['afb_api'] / summary[tp_basis] if summary[tp_basis] != 0 else 0

    # Calculate rate of capital (ROC)
    if tpi_year < 2026:
        summary[basis]['roc'] = utils.ratio(  ( 1   -  summary[basis][estimate_field]
                                                    - (summary['ri_premium']  - summary['ri_recoveries']   )
                                                    + (summary['inv_income']  * (1 - summary['ri_premium']))
                                                    - (summary['net_expense']                              ))
                                             ,(summary['capital_required']   * (1 - summary['ri_premium']  )))
    else:
        summary[basis]['roc'] = utils.ratio(  ( 1  -  summary[basis][estimate_field]
                                                   - (summary['ri_premium']  - summary['ri_recoveries']    )
                                                   + (summary['inv_income']                                )
                                                   - (summary['net_expense']                               ))
                                             ,(summary['capital_required']                                  ))


def calculate_pricing_adequacy_metrics_post_tech_prem(summary, tpi_year):
    # Calculate TPI and ROC for actuarial basis
    calculate_tpi_roc(summary, "act_basis", "tp_actuarial", tpi_year)
    # Calculate TPI and ROC for pre-adjustment basis
    calculate_tpi_roc(summary, "pre_adj", "tp_pre_adj", tpi_year)
    # Calculate TPI and ROC for final basis
    calculate_tpi_roc(summary, "final", "tp_final", tpi_year)


def save_pricing_adequacy_metrics_fields(summary, summary_path):
    # Push pre-adjustment values to HX nodes
    for k, v in summary['pre_adj'].items():
        setattr(summary_path.pricing_adequacy_metrics.pricing_adequacy_pre_adj.summary, k, v)
    # Push actuarial basis values to HX nodes
    for k, v in summary['act_basis'].items():
        setattr(summary_path.pricing_adequacy_metrics.pricing_adequacy_actuarial_basis.summary, k, v)
    # Push final values to HX nodes, excluding uw_adj_bbt
    for k, v in summary['final'].items():
        if k != "uw_adj_bbt":
            setattr(summary_path.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary, k, v)


def calculate_cat_ulr(summary, summary_path):
    # Calculate CAT ULR excluding additional loadings
    summary["gn_cat_ulr_excl_loads"] = summary["gn_ulr_5623"] * summary["cat"]
    # Calculate CAT ULR including additional loadings
    summary["gn_cat_ulr_inc_loads"] = summary["final"]["best_estimate_gn"] * summary["cat"]

    # Save CAT ULR values to HX nodes
    summary_path.cat_ulr_summary.summary.gn_cat_ulr_excl_loads = summary["gn_cat_ulr_excl_loads"]
    summary_path.cat_ulr_summary.summary.gn_cat_ulr_inc_loads = summary["gn_cat_ulr_inc_loads"]