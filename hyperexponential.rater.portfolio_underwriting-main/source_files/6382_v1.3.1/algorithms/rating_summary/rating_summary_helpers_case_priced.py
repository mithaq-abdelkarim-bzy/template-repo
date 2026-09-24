import hx
import pandas as pd
import numpy as np
import algorithms.rate_utilities                         as utils
import algorithms.rate_constants                         as constants
import algorithms.validations.rating_summary_validations as validations
import algorithms.parameter_tables_schema                as params

def rate_rating_summary_case_priced(hxd, rater):
    
    # get paths
    summary_path         = hxd.cds.rating_summary            # Get the rating summary path
    pricing_outputs_path = summary_path.case_pricing         # Get the case pricing path
    
    # validate case pricing
    validations.check_case_pricing(hxd)

    # validate tpi year
    incept_yr            = hxd.hx_core.inception_date.year
    tpi_year             = hxd.cds.rating_summary.technical_premium_build_up.tpi_year.selected
    validations.check_tpi_year_value(tpi_year)
    tpi_year             = tpi_year or incept_yr

    # Initialize summary with override and output fields
    summary = init_summary_fields(pricing_outputs_path)

    # Calculate loss ratios, technical, tpi, roc
    calculate_pricing_outputs(summary           )
    calculate_tech_prem(      summary, tpi_year )
    calculate_roc(            summary, tpi_year )

     # Save calculated tech premium fields to HX summary nodes
    pricing_outputs_path.tpi_override.calculated= summary["gg_tpi_calc"]
    pricing_outputs_path.tpi                    = pricing_outputs_path.tpi_override.selected
    pricing_outputs_path.roc_override.calculated= summary["roc"]
    pricing_outputs_path.roc                    = pricing_outputs_path.roc_override.selected
    pricing_outputs_path.gn_ulr                 = summary["gn_ulr"]
    pricing_outputs_path.gg_ulr                 = summary["gg_ulr"]
    return summary


def init_summary_fields(pricing_outputs_path):
    # Create empty summary dict
    summary                       = {}
    # assign case pricing values
    summary['brokerage']          = pricing_outputs_path.brokerage              or 0
    summary['written_line']       = pricing_outputs_path.written_line           or 0
    summary['bpi']                = pricing_outputs_path.bpi                    or 0
    summary['quoted_premium_100'] = pricing_outputs_path.quoted_premium_100     or 0
    summary['tracker_class']      = pricing_outputs_path.tracker_class          or ''
    summary['tpi_override']       = pricing_outputs_path.tpi_override.override  or 0
    return summary


def calculate_pricing_outputs(summary):
    bench_lr                  = constants.benchmark_lr
    summary['gn_ulr']         = utils.ratio(bench_lr, summary['bpi']) 
    summary['gg_ulr']         = summary['gn_ulr'] * (1 - summary['brokerage']) 
    summary['quoted_premium'] = summary['quoted_premium_100'] * summary['written_line'] 


def get_value_from_tpi_params(df, mask, column, default=0):
    # Get values from DataFrame using mask and column
    values = df.loc[mask, column].values
    # Return first value if exists, else default
    return values[0] if len(values) > 0 else default


def calculate_tech_prem(summary, tpi_year):
    # Calculate expected losses
    summary['el_final'] = summary['gg_ulr'] * summary['quoted_premium']  

    # Load TPI parameters
    tpi_params_df= params.tp_parameters.df()
    tpi_mask     = (tpi_params_df["business_plan_class"] == summary['tracker_class']) & (tpi_params_df["year"] == tpi_year)


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
    
    # so the tpi and technicals goto zero if no factors exist
    if tpi_mask.any() == False:
        summary["factor"] = 0 

    # Calculate technical premiums & tpi including accommodating the override
    summary['gn_tp_calc']  = utils.ratio(summary['el_final'],        summary['factor'])
    summary["gg_tp_calc"]  = utils.ratio(summary['gn_tp_calc'],  1 - summary['brokerage'] )
    summary["gg_tpi_calc"] = utils.ratio(summary["quoted_premium"],  summary["gg_tp_calc"])


def calculate_roc(summary, tpi_year):
    # Calculate rate of capital (ROC)
    if tpi_year < 2026:
        summary['roc'] = utils.ratio(  ( 1   -  summary['gn_ulr']
                                             - (summary['ri_premium']  - summary['ri_recoveries']   )
                                             + (summary['inv_income']  * (1 - summary['ri_premium']))
                                             - (summary['net_expense']                              ))
                                             ,(summary['capital_required']   * (1 - summary['ri_premium']  )))
    else:
        summary['roc'] = utils.ratio(  ( 1  -  summary['gn_ulr']
                                                   - (summary['ri_premium']  - summary['ri_recoveries']    )
                                                   + (summary['inv_income']                                )
                                                   - (summary['net_expense']                               ))
                                             ,(summary['capital_required']                                  ))