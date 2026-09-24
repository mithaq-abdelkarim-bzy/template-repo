# v0.5.0
import hx
import pandas as pd
import numpy as np
import algorithms.rate_constants as const
from algorithms import parameter_tables_schema as params
from algorithms.rate_utilities import ratio, look_up, pd_df_from_hx_list, policy_term
from algorithms.rate_constants import benchmark_lr
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import coverages_dict


def rate_rating_summary(hxd):

    rf = hxd.cds.rating_factors  
    # Set rating methodology
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == 'Case Priced'
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == 'Rater'

    # Pull in technical premium parameters and fx rates from user library 
    tp_params_df = params.tp_parameters.df()
    fx_rates_df = params.fx_rates.df() # Using fx from library
    # fx_rates_df = hx.params.table_currency # Using fx from params
    yoa = hxd.hx_core.inception_date.year
    # To stop the model erroring if the inception year defaults to an old year not in the TP data
    if yoa in list(tp_params_df['year']):
        tp_year = yoa
    else:
        tp_year = tp_params_df['year'].max()
    
    # Placeholder variables: update with correct benchmark class and modelled expected loss, this might need to 
    # be linked if a rater can write to more than one class. May link to benchmark class in risk information.
    # bp_class = hxd.cds.standard_fields.benchmark_class
    bp_class = 'Fidelity and Crime' #PLACEHOLDER

    tp_lookup_bool = (tp_params_df['business_plan_class'] == bp_class) & (tp_params_df['year'] == tp_year)
    tp_params = tp_params_df[tp_lookup_bool]

    # Set up tp params
    che = tp_params['che'].iloc[0]
    var_exp = tp_params['var_exp'].iloc[0]
    inv_inc = tp_params['inv_inc'].iloc[0]
    cost_of_ri = tp_params['cost_of_ri'].iloc[0]
    ri_rec = tp_params['ri_rec'].iloc[0]
    roc = tp_params['roc'].iloc[0]
    fixed_exp_usd = tp_params['fixed_exp'].iloc[0]
    capital_req = tp_params['capital_req'].iloc[0]
    nmp_load = tp_params['nmp_load'].iloc[0]

    # Convert fixed expenses to model currency (default to USD if error)
    ccy = hxd.cds.currencies.source_currency
    fixed_exp = fixed_exp_usd * look_up(ccy, 'ccy', 'fx_rate', fx_rates_df, if_not_found=1)

    # Calculate technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc*capital_req

    '''
    If there is only ever one layer, use the following code to work with the first element of the layer list without having to loop
    '''
    # layer = hxd.cds.layers[0]
    # layer.expected_loss_cost = 10000 # EXAMPLE


    for layer in hxd.cds.layers:
        if not RARC_COVERAGE_USE and not RARC_INSURED_ASSET_USE:
            # PLACEHOLDER FORMULA
            calculate_premiums(layer, hxd, nmp_load, che, fixed_exp, technical_lr, benchmark_lr, var_exp, inv_inc, cost_of_ri, ri_rec, capital_req, rf) # Edit v0.3.0
        
        elif RARC_COVERAGE_USE and not RARC_INSURED_ASSET_USE:
            # Assume the layer currency is an input in this example
            # layer.currency = hxd.cds.currencies.source_currency # commented
            for idx, cvg in layer.coverages:
                
                # assume the policy term at a policy level applies to the coverage in this example
                calculate_premiums(cvg, hxd, nmp_load, che, fixed_exp, technical_lr, benchmark_lr, var_exp, inv_inc, cost_of_ri, ri_rec, capital_req, rf=rf)        
        
        elif not RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE:
            # NOTE: RARC requirement - set layer currency equal to the source currency
            layer.currency = hxd.cds.currencies.source_currency

            # calculate premium per insured asset
            for insured_asset in hxd.cds.exposure.granular.layers:
                # policy term assumed to be at a insured asset level
                insured_asset.policy_term = policy_term(insured_asset.start_date, insured_asset.end_date)
                insured_asset.brokerage = layer.brokerage
                calculate_premiums(insured_asset, hxd, nmp_load, che, fixed_exp, technical_lr, benchmark_lr, var_exp, inv_inc, cost_of_ri, ri_rec, capital_req, insured_asset)
            convert_aggregate_insured_asset_amount(hxd=hxd, fx_rates_df=fx_rates_df, aggregated_level = layer, exposure_list=getattr(hxd.cds.exposure.granular, "layers"))

        elif RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE:
            # NOTE: RARC requirement - set layer currency equal to policy currency
            layer.currency = hxd.cds.currencies.source_currency
            
            for idx, cvg in enumerate(coverages_dict.keys()):
                
                # NOTE: RARC requirement - set coverage currency equal to policy currency
                setattr(getattr(layer.coverages,cvg),"currency",hxd.cds.currencies.source_currency)
            
                # NOTE: RARC requirement - calculate premium per insured asset
                for insured_asset in getattr(hxd.cds.exposure.granular,cvg):
                    # policy term assumed to be at a insured asset level
                    insured_asset.policy_term = policy_term(insured_asset.start_date, insured_asset.end_date)
                    insured_asset.brokerage = getattr(layer.coverages,cvg).brokerage
                    calculate_premiums(insured_asset, hxd, nmp_load, che, fixed_exp, technical_lr, benchmark_lr, var_exp, inv_inc, cost_of_ri, ri_rec, capital_req, insured_asset)
                convert_aggregate_insured_asset_amount(hxd=hxd, fx_rates_df=fx_rates_df, aggregated_level = getattr(layer.coverages,cvg), exposure_list=getattr(hxd.cds.exposure.granular, cvg))
                
                

def calculate_premiums(calculated_level, hxd, nmp_load, che, fixed_exp, technical_lr, benchmark_lr, var_exp, inv_inc, cost_of_ri, ri_rec, capital_req, rf): # Edit v0.3.0
    """
    Calculate the premium for the given level
    Args:
        calculated_level: this could be Layer, Coverage or Insured Asset
        pricing assumptions:
        rf = rating factor level that contains the policy_term
    """
    # PLACEHOLDER GENERCIC FORMULA - allow calculation at a layer, coverage or insured interest level
    calculated_level.expected_loss_cost_100 = max(10000 + 0.01 * (calculated_level.limit or 0) - 0.005 * (calculated_level.excess or 0) - 0.05 * (calculated_level.deductible or 0), 10000)
    calculated_level.expected_loss_cost_pre_uw_adj_100 = calculated_level.expected_loss_cost_100 * 0.95

    # Calculate the impact of UW adjustment
    calculated_level.uw_adj_impact = ratio(calculated_level.expected_loss_cost_100, calculated_level.expected_loss_cost_pre_uw_adj_100) - 1

    # If rater priced
    if hxd.cds.standard_fields.is_rater_priced and calculated_level.quoted_premium_100:
        expected_loss_100 = calculated_level.expected_loss_cost_100 * (1 + nmp_load)
        exp_loss_pre_adj_100 = calculated_level.expected_loss_cost_pre_uw_adj_100 * (1 + nmp_load)

        calculated_level.technical_premium_net_100 = ratio((expected_loss_100 * (1 + che) + fixed_exp), technical_lr)
        calculated_level.technical_premium_100 = ratio(calculated_level.technical_premium_net_100, (1 - (calculated_level.brokerage or 0)))
        calculated_level.technical_premium_pre_uw_adj_100 = ratio(ratio((exp_loss_pre_adj_100 * (1 + che) + fixed_exp), technical_lr), (1 - (calculated_level.brokerage or 0)))

        calculated_level.benchmark_premium_100 = ratio(ratio(expected_loss_100, benchmark_lr), (1 - (calculated_level.brokerage or 0)))
        calculated_level.bpi = ratio(calculated_level.quoted_premium_100, calculated_level.benchmark_premium_100)
        calculated_level.tpi = ratio(calculated_level.quoted_premium_100, calculated_level.technical_premium_100)
        calculated_level.tpi_pre_uw_adj = ratio(calculated_level.quoted_premium_100, calculated_level.technical_premium_pre_uw_adj_100)
        calculated_level.bpi_pre_uw_adj = calculated_level.bpi * (calculated_level.uw_adj_impact + 1)

        quoted_premium_net_100 = calculated_level.quoted_premium_100 * (1 - (calculated_level.brokerage or 0))
        calculated_level.pflr = ratio(expected_loss_100, (quoted_premium_net_100 or 1))
        calculated_level.pflr_pre_uw_adj = ratio(exp_loss_pre_adj_100, (quoted_premium_net_100 or 1))
        calculated_level.roc = ratio(1 - calculated_level.pflr - var_exp + inv_inc - (cost_of_ri - ri_rec) - ratio(fixed_exp + expected_loss_100 * che, quoted_premium_net_100), capital_req)

    # For case pricing only
    if hxd.cds.standard_fields.is_case_priced and calculated_level.quoted_premium_100 and calculated_level.bpi_case_priced:
        calculated_level.bpi = calculated_level.bpi_case_priced
        calculated_level.benchmark_premium_100 = ratio(calculated_level.quoted_premium_100, calculated_level.bpi)
        calculated_level.expected_loss_cost_100 = calculated_level.benchmark_premium_100 * benchmark_lr * (1 - (calculated_level.brokerage or 0))

        calculated_level.technical_premium_net_100 = ratio((calculated_level.expected_loss_cost_100 * (1 + che) + fixed_exp), technical_lr)
        calculated_level.technical_premium_100 = ratio(calculated_level.technical_premium_net_100, (1 - (calculated_level.brokerage or 0)))

        calculated_level.tpi = ratio(calculated_level.quoted_premium_100, calculated_level.technical_premium_100)
        calculated_level.pflr = ratio(benchmark_lr, calculated_level.bpi)
        calculated_level.tpi_pre_uw_adj = calculated_level.tpi
        calculated_level.technical_premium_pre_uw_adj_100 = calculated_level.technical_premium_100

        quoted_premium_net_100 = calculated_level.quoted_premium_100 * (1 - (calculated_level.brokerage or 0))
        calculated_level.roc = ratio(1 - calculated_level.pflr - var_exp + inv_inc - (cost_of_ri - ri_rec) - ratio(fixed_exp + calculated_level.expected_loss_cost_100 * che, quoted_premium_net_100), capital_req)

    # NOTE - RARC requirement - Calculate annualised premium, insurer's share and net premium. These will be used for rate change and reporting
    calculated_level.quoted_premium_annual_100 = (calculated_level.quoted_premium_100 or 0) / (rf.policy_term or 1)
    calculated_level.quoted_premium_annual = (calculated_level.quoted_premium_annual_100 or 0) * (calculated_level.written_line or 0)
    calculated_level.quoted_premium_net_100 = (calculated_level.quoted_premium_100 or 0) * (1-(calculated_level.brokerage or 0))
    calculated_level.quoted_premium = (calculated_level.quoted_premium_100 or 0) * (calculated_level.written_line or 0)
    calculated_level.quoted_premium_net = (calculated_level.quoted_premium or 0) * (1-(calculated_level.brokerage or 0))

    calculated_level.benchmark_premium_annual_100 = (calculated_level.benchmark_premium_100 or 0) / (rf.policy_term or 1)
    calculated_level.benchmark_premium_annual = (calculated_level.benchmark_premium_annual_100 or 0) * (calculated_level.written_line or 0)
    calculated_level.benchmark_premium_net_100 = (calculated_level.benchmark_premium_100 or 0) * (1-(calculated_level.brokerage or 0))
    calculated_level.benchmark_premium = (calculated_level.benchmark_premium_100 or 0) * (calculated_level.written_line or 0)
    calculated_level.benchmark_premium_net = (calculated_level.benchmark_premium or 0) * (1-(calculated_level.brokerage or 0))
        
    calculated_level.technical_premium_annual_100 = (calculated_level.technical_premium_100 or 0) / (rf.policy_term or 1)
    calculated_level.technical_premium_annual = (calculated_level.technical_premium_annual_100 or 0) * (calculated_level.written_line or 0)
    calculated_level.technical_premium_net_100 = (calculated_level.technical_premium_100 or 0) * (1-(calculated_level.brokerage or 0))
    calculated_level.technical_premium = (calculated_level.technical_premium_100 or 0) * (calculated_level.written_line or 0)
    calculated_level.technical_premium_net = (calculated_level.technical_premium or 0) * (1-(calculated_level.brokerage or 0))


def convert_aggregate_insured_asset_amount(hxd, fx_rates_df, aggregated_level, exposure_list):
    """
    Convert and aggregate insured asset amounts at a given aggregated level.
    This is a compulsory step for rate change with insured assets.

    Args:
        hxd: The HXD object containing the data.
        fx_rates_df: DataFrame containing currency and FX rate information.
        aggregated_level: insured asset value are converted and aggregated to that level (layer, coverage)
        exposure_list: name of the insured asset list to convert and aggregate
    
    Requirements: 
        The insured asset values are assumed to be in currency.

    """
    # RARC requirement - Get the insured interest list as DataFrame
    insured_asset_df = pd_df_from_hx_list(exposure_list)

    # RARC requirement - Merge the DataFrames on the currency column to add the FX value to the DataFrame
    insured_asset_with_fx_df = insured_asset_df.merge(
        fx_rates_df,
        left_on="currency",
        right_on="ccy",
        how="left"
    )

    # RARC requirement - Add the fx_rate column to the DataFrame
    insured_asset_df["fx_rate"] = insured_asset_with_fx_df["fx_rate"]

    # RARC requirement - get FX from USD to reporting currency
    fx_from_usd_to_reporting_ccy = look_up(hxd.cds.currencies.source_currency, "ccy", "fx_rate", fx_rates_df, if_not_found=1)

    # RARC requirement - list the aggregated value nodes for conversion
    premium_to_convert = [
        "quoted_premium_100",
        "quoted_premium_annual_100",
        "quoted_premium_annual",
        "quoted_premium_net_100",
        "quoted_premium_net",
        "quoted_premium",

        "technical_premium_100",
        "technical_premium_pre_uw_adj_100",
        "technical_premium_net_100",
        "technical_premium_net",
        "technical_premium",

        "benchmark_premium_100",
        "benchmark_premium_annual_100",
        "benchmark_premium_annual",
        "benchmark_premium_net_100",
        "benchmark_premium_net",
        "benchmark_premium",

        "expected_loss_cost_100",
        "expected_loss_cost_pre_uw_adj_100",
    ]

    # RARC requirement - Calculate the converted premium for aggregation
    for prem in premium_to_convert:
        insured_asset_df[prem + "_conv"] = (
            insured_asset_with_fx_df[prem] * ratio(fx_from_usd_to_reporting_ccy, insured_asset_with_fx_df["fx_rate"])
        )
        # Sum premiums and assign value to the coverage premiums
        setattr(aggregated_level, prem, insured_asset_df[prem + "_conv"].fillna(0).sum())

    # RARC requirement - set TPI, BPI, and other ratios
    setattr(aggregated_level, "tpi", ratio(getattr(aggregated_level, "quoted_premium_100"), getattr(aggregated_level, "technical_premium_100")))
    setattr(aggregated_level, "tpi_pre_uw_adj", ratio(getattr(aggregated_level, "quoted_premium_100"), getattr(aggregated_level, "technical_premium_pre_uw_adj_100")))

    quoted_premium_100 = getattr(aggregated_level, "quoted_premium_100")
    if quoted_premium_100:
        setattr(aggregated_level, "pflr", ratio(getattr(aggregated_level, "expected_loss_cost_100"), quoted_premium_100))
        setattr(aggregated_level, "pflr_pre_uw_adj", ratio(getattr(aggregated_level, "expected_loss_cost_pre_uw_adj_100"), quoted_premium_100, if_undefined=0))

    setattr(aggregated_level, "bpi", ratio(getattr(aggregated_level, "quoted_premium_100"), getattr(aggregated_level, "benchmark_premium_100")))