
##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################

###  1) technical_premium_net_bzly_share
###  2) 
###  3) 
###  4) 
###  5)
###  6) 
###  7) 
###  8) 
###  9) 
### 10)
##############################################################################################################################

import hx
import pandas as pd
import numpy as np
import math as math
import json
from dateutil.relativedelta import relativedelta
from algorithms.rate_utilities import one_layer, ratio, pd_df_from_hx_list, look_up, tp_components, year_diff, policy_term
from algorithms.rate_utilities import to_ccy, mbbefd, rsetattr, rgetattr
from algorithms.rate_constants import benchmark_lr
from algorithms import parameter_tables_schema as params
from algorithms.data_schema.sch_rater_defined import authorities, perils


def calculate_technical_premium(hxd,  expected_loss_cost,  total_expected_loss_cost=None,  written_line=None,  brokerage=None,  bp_class=None):
    layer, cvg  = one_layer(hxd)
    tp          = tp_components(hxd, bp_class)

    # Set key TP params
    che             = tp["che"]
    fixed_exp       = tp["fixed_exp"]
    technical_lr    = tp["technical_lr"]

    # Check for None's and allow for allocation of fixed expenses to different coverages based on EL
    fixed_exp       = 0                         if total_expected_loss_cost is None else fixed_exp * ratio(expected_loss_cost, total_expected_loss_cost) 
    written_line    = (layer.written_line or 0) if written_line             is None else written_line
    brokerage       = (layer.brokerage    or 0) if brokerage                is None else brokerage
    
    # Calculate premium
    expected_loss_bzly_share         = expected_loss_cost * written_line
    technical_premium_net_bzly_share = ratio(expected_loss_bzly_share * (1 + che) + fixed_exp,   technical_lr   )
    technical_premium_net_100pct     = ratio(technical_premium_net_bzly_share,                   written_line   )
    technical_premium                = ratio(technical_premium_net_100pct,                       (1 - brokerage))

    return technical_premium


def rate_rating_summary(hxd, curves_df):

    # links to hx structures
    cds             = hxd.cds
    layer, cvg      = one_layer(hxd)
    tp              = tp_components(hxd)
    sf              = cds.standard_fields
    expo_a          = cds.exposure.aggregate
    expo_g          = cds.exposure.granular
    brokerage       = layer.brokerage
    ra              = layer.risk_adjustments
    
    # links to hx nodes
    uw_multiplier       = ra.uw_multiplier
    uw_ihs_multiplier   = ra.uw_ihs_adjustment
    limit               = expo_a.policy_limit
    ccy                 = hxd.cds.currencies.source_currency
    inception_date      = hxd.hx_core.inception_date
    expiry_date         = hxd.hx_core.expiry_date
    is_migrated         = hxd.model_state.is_migrated

    # Annual
    p           = cvg.property
    pd_         = p.pd
    bi          = p.bi
    l           = cvg.liability
    c           = cvg.construction
    t           = cvg.total
    hxd_cvg     = [p, l, c]
    hxd_cvg_all = [p, pd_, bi, l, c, t]

    # Policy period
    p_p             = cvg.property.policy_period
    pd_p            = p_p.pd
    bi_p            = p_p.bi
    l_p             = cvg.liability.policy_period
    c_p             = cvg.construction.policy_period 
    t_p             = cvg.total.policy_period
    hxd_cvg_p       = [p_p, l_p, c_p]
    hxd_cvg_all_p   = [p_p, pd_p, bi_p, l_p, c_p, t_p]

    # UW Authorities USD 
    uw_a = layer.uw_authorities.authority
    uw_p = layer.uw_authorities.policy
    uw_w = layer.uw_authorities.warning

    # UW Authorities on current currency
    uw_a_current_currency = layer.uw_authorities_current_currency.authority
    uw_p_current_currency = layer.uw_authorities_current_currency.policy
    uw_w_current_currency = layer.uw_authorities_current_currency.warning

    cds.authority_ccy_label =  f"Authority - {ccy}"
    cds.policy_ccy_label =  f"Policy - {ccy}"

    # Param tables
    AggUsage            = hx.params.AggUsage
    BusPlanLossRatios   = hx.params.BusPlanLossRatios
    SalzmannB           = hx.params.SalzmannB
    Underwriters        = hx.params.Underwriters
    InflationRates      = hx.params.InflationRates

    # plan loss ratio
    business_plan_lr    = look_up(inception_date.year, "YoA", "LR", BusPlanLossRatios, if_not_found=BusPlanLossRatios["LR"].iloc[-1], lookup_type="single")

    # Early exit without curves_df
    if curves_df.empty:
        return

    ### --- ANNUAL --- ###
    # Get latest available YOA
    yoa             = inception_date.year
    inflation_year  = yoa if yoa in list(InflationRates["YOA"]) else InflationRates["YOA"].max()
    inflation       = look_up(inflation_year, "YOA", "Inflation", InflationRates, if_not_found=1, lookup_type="single")

    ## Model price calculation
    adjustments_mp      = (1 - expo_a.agg_discount) * benchmark_lr * (1 + inflation)
    
    # factors to apply to pre uw adj - migrated approach used all figures before ihs, new approach main df is calculated after uw adjusting ihs
    pre_uw_adj_factor   = 1 if is_migrated else (uw_ihs_multiplier or 1) 

    # bi model price
    bi_total_prem_base_net       = curves_df[["cvg_bi_base_premium", "subcvg_bi_base_premium"]].sum().sum()
    bi_total_prem_plan_net       = ratio(bi_total_prem_base_net * adjustments_mp,    business_plan_lr)
    bi_total_prem_plan_gross     = ratio(bi_total_prem_plan_net,                     (1 - brokerage) )
    bi.model_premium_pre_uw_adj  = 0 if c.is_covered else bi_total_prem_plan_gross

    # pd model price
    pd_total_prem_base_net       = curves_df[["cvg_pd_base_premium", "subcvg_pd_base_premium"]].sum().sum()
    pd_total_prem_plan_net       = ratio(pd_total_prem_base_net * adjustments_mp,    business_plan_lr)
    pd_total_prem_plan_gross     = ratio(pd_total_prem_plan_net,                     (1 - brokerage) )
    pd_.model_premium_pre_uw_adj = 0 if c.is_covered else pd_total_prem_plan_gross

    # liability (li) model price
    li_total_prem_base_net       = curves_df[["cvg_liab_base_premium", "subcvg_liab_base_premium"]].sum().sum()
    li_total_prem_plan_net       = ratio(li_total_prem_base_net * adjustments_mp,    business_plan_lr)
    li_total_prem_plan_gross     = ratio(li_total_prem_plan_net,                     (1 - brokerage) )
    li_model_premium_pre_uw_adj  = 0 if c.is_covered else li_total_prem_plan_gross
    l.model_premium_pre_uw_adj   = to_ccy(li_model_premium_pre_uw_adj, ccy) # Liab prem calculated in USD because of ILFs

    p.model_premium_pre_uw_adj   = bi.model_premium_pre_uw_adj + pd_.model_premium_pre_uw_adj
    c.model_premium_pre_uw_adj   = c.years_annual.model_premium_pre_uw_adj or 0
    t.model_premium_pre_uw_adj   = sum([getattr(cov, "model_premium_pre_uw_adj") for cov in hxd_cvg])

    for cov in hxd_cvg_all:
        cov.model_rol_pre_uw_adj = ratio(cov.model_premium_pre_uw_adj, limit)                       # Model ROL     before UW adj
        cov.model_premium        = cov.model_premium_pre_uw_adj * uw_multiplier                     # Model Premium  after Uw adj 
        cov.model_rol            = ratio(cov.model_premium, limit)                                  # Model ROL      after Uw adj 
        cov.benchmark_premium    = ratio(cov.model_premium * business_plan_lr, benchmark_lr)        # Bench Premium  after Uw adj 


    # Minimum rates and premiums
    agg_multiplier      = look_up(expo_a.details.aggregate_usage, "Agg Usage", "UW Multiplier", AggUsage, lookup_type="single")
    
    p.minimum_premium   = max( p.model_premium * agg_multiplier,    expo_g.wa_nl_min_rol * limit)   if not c.is_covered else 0
    p.minimum_rol       = ratio(p.minimum_premium, limit)
    
    bi.minimum_premium  = p.minimum_rol * ratio(bi.model_premium, p.model_rol)
    bi.minimum_rol      = ratio(bi.minimum_premium, limit)

    pd_.minimum_premium = p.minimum_rol * ratio(pd_.model_premium, p.model_rol)
    pd_.minimum_rol     = ratio(pd_.minimum_premium, limit)

    l.minimum_premium   = max( l.model_premium * agg_multiplier,    expo_g.wa_liab_min_rol * limit) if not c.is_covered else 0
    l.minimum_rol       = ratio(l.minimum_premium, limit)

    c.minimum_premium   = c.years_annual.model_premium_post_agg_adj or 0
    c.minimum_rol       = ratio(c.minimum_premium, limit)

    t.minimum_premium   = sum([getattr(cov, "minimum_premium") for cov in hxd_cvg])
    t.minimum_rol       = ratio(t.minimum_premium, limit)


    quoted_premium      = layer.quoted_premium_100_pct or 0
    quoted_rol          = layer.quoted_rol or 0

    t_p.quoted_premium  = quoted_premium if layer.quoted_premium_100_pct is not None else quoted_rol * limit # notice quoted premium here is 100%
    t_p.quoted_rol      = quoted_rol     if layer.quoted_rol is not None else ratio(quoted_premium, limit)

    written_line        = layer.written_line or 1
    layer.quoted_premium= (t_p.quoted_premium or 0) * written_line                                           # notice quoted premium here is at share
    layer.quoted_premium_case_priced = layer.quoted_premium                                        

    # Quoted premium - annual
    incept_date_plus1yr = (inception_date + relativedelta(years=1))
    annualisation_factor= ratio(   (incept_date_plus1yr - inception_date).days,    c.days_difference)
    #YZ Change 23/10/2025: The expiry date adjustment. if term:  01/07/2024 - 30/06/2025, it is still one year.
    if ((incept_date_plus1yr - inception_date).days - c.days_difference <= 1)  and ((incept_date_plus1yr - inception_date).days - c.days_difference >= 0):
        annualisation_factor = 1
    t.quoted_premium    = t_p.quoted_premium * annualisation_factor
    t.quoted_rol        = ratio(t.quoted_premium, limit)


    # MBBEFD
    b = SalzmannB["b"].iloc[0]
    g = SalzmannB["g"].iloc[0]

    # ROE
    sum_insured = expo_a.total_sum_insured
    excess      = expo_a.policy_excess
    t.quoted_roe = ratio(
        ratio(t.quoted_premium, sum_insured),
        mbbefd(b, g, ratio(limit + excess, sum_insured)) -  mbbefd(b, g, ratio(excess, sum_insured))
    ) 

    #  Rater priced
    if hxd.cds.standard_fields.is_rater_priced: 
        # Technical
        expected_loss_cost_annualised_100_pct=t.benchmark_premium * benchmark_lr  * (1 - layer.brokerage) 
        layer.expected_loss_cost_annualised = expected_loss_cost_annualised_100_pct * written_line
        t.technical_premium                 = calculate_technical_premium(hxd, expected_loss_cost_annualised_100_pct, expected_loss_cost_annualised_100_pct)
        t.tpi                               = ratio(t.quoted_premium, t.technical_premium)

        # Benchmark
        t.bpi                               = ratio(t.quoted_premium, t.benchmark_premium)
        t.expected_loss_ratio               = ratio(benchmark_lr, t.bpi)
        t.benchmark_premium_pre_uw_adj      = ratio(t.model_premium_pre_uw_adj * business_plan_lr, benchmark_lr)
        t.bpi_pre_uw_adj                    = ratio(t.quoted_premium, t.benchmark_premium_pre_uw_adj)
        t.expected_loss_ratio_pre_uw_adj    = ratio(benchmark_lr, t.bpi_pre_uw_adj)

        # Technical pre-UW adjustments
        expected_loss_cost_pre_uw_adj_annualised_100_pct= t.benchmark_premium_pre_uw_adj * benchmark_lr  * (1 - layer.brokerage)
        layer.expected_loss_cost_pre_uw_adj_annualised  = expected_loss_cost_pre_uw_adj_annualised_100_pct * written_line 
        t.technical_premium_pre_uw_adj                  = calculate_technical_premium(hxd, expected_loss_cost_pre_uw_adj_annualised_100_pct, expected_loss_cost_pre_uw_adj_annualised_100_pct)
        t.tpi_pre_uw_adj                                = ratio(t.quoted_premium, t.technical_premium_pre_uw_adj)
    
    if hxd.cds.standard_fields.is_case_priced and layer.quoted_premium_case_priced > 0 and layer.bpi_case_priced > 0: 
        t.bpi = layer.bpi_case_priced
        t.benchmark_premium = ratio(layer.quoted_premium_case_priced, t.bpi) * annualisation_factor
        t.expected_loss_cost = t.benchmark_premium * benchmark_lr * (1 - brokerage)
        
        t.technical_premium = calculate_technical_premium(hxd, t.expected_loss_cost,t.expected_loss_cost)
        t.technical_premium_net = t.technical_premium * (1 - brokerage)  
        t.tpi = ratio(t.quoted_premium, t.technical_premium)
        t.tpi_pre_uw_adj = t.tpi
        t.technical_premium_pre_uw_adj = t.technical_premium
        
        # Additional metrics for CDS
        t.pflr = ratio(benchmark_lr, t.bpi)
        quoted_premium_net = t.quoted_premium * (1 - brokerage)
        t.roc = ratio(
            1 - t.pflr - tp["var_exp"] + tp["inv_inc"] - (tp["cost_of_ri"] - tp["ri_rec"]) - ratio(tp["fixed_exp"] + t.expected_loss_cost * tp["che"], quoted_premium_net),
            tp["capital_req"]
        )

    
    ### --- POLICY PERIOD --- ###
    term_factor = ratio(1, annualisation_factor)

    for cov, cov_p in zip(hxd_cvg_all, hxd_cvg_all_p):
        if (cov_p == c_p) or (cov_p == t_p):
            continue

        cov_p.benchmark_premium         = cov.benchmark_premium * term_factor                           # Benchmark Price
        cov_p.model_premium_pre_uw_adj  = cov.model_premium_pre_uw_adj * term_factor                    # Model Price
        cov_p.model_rol_pre_uw_adj      = ratio(cov_p.model_premium_pre_uw_adj, limit)                  # Model ROL
        cov_p.model_premium             = cov.model_premium * term_factor                               # UW Adjusted Price
        cov_p.model_rol                 = ratio(cov_p.model_premium, limit)                             # UW Adjusted ROL
        cov_p.minimum_premium           = cov.minimum_premium * term_factor                             # Minimum Price
        cov_p.minimum_rol               = ratio(cov_p.minimum_premium, limit)                           # Minimum ROL

    
    # Treat Construction separately
    c_p.benchmark_premium               = c.years_total.benchmark_premium
    c_p.model_premium_pre_uw_adj        = c.years_total.model_premium_pre_uw_adj
    c_p.model_rol_pre_uw_adj            = ratio(c_p.model_premium_pre_uw_adj or 0, limit)
    c_p.model_premium                   = c.years_total.model_premium
    c_p.model_rol                       = ratio(c_p.model_premium or 0, limit)
    c_p.minimum_premium                 = c.years_total.model_premium_post_agg_adj
    c_p.minimum_rol                     = ratio(c_p.minimum_premium or 0, limit)

    
    def safe_sum(iterable):
        return sum(x or 0 for x in iterable)

    # Calculate totals
    t_p.benchmark_premium               = safe_sum([getattr(cov, "benchmark_premium")           for cov in hxd_cvg_p])
    t_p.model_premium_pre_uw_adj        = safe_sum([getattr(cov, "model_premium_pre_uw_adj")    for cov in hxd_cvg_p])
    t_p.model_premium                   = safe_sum([getattr(cov, "model_premium")               for cov in hxd_cvg_p])
    t_p.minimum_premium                 = safe_sum([getattr(cov, "minimum_premium")             for cov in hxd_cvg_p])
    t_p.model_rol_pre_uw_adj            = ratio(t_p.model_premium_pre_uw_adj, limit)
    t_p.model_rol                       = ratio(t_p.model_premium, limit)
    t_p.minimum_rol                     = ratio(t_p.minimum_premium, limit)
    
    t_p.quoted_roe                      = t.quoted_roe * term_factor # TODO: check this is correct

    if hxd.cds.standard_fields.is_rater_priced: 
        # Technical
        expected_loss_cost_100_pct          = t_p.benchmark_premium * benchmark_lr  * (1 - layer.brokerage)
        layer.expected_loss_cost            = expected_loss_cost_100_pct * written_line
        t_p.technical_premium               = calculate_technical_premium(hxd, expected_loss_cost_100_pct, expected_loss_cost_100_pct)
        t_p.tpi                             = ratio(t_p.quoted_premium, t_p.technical_premium)

        # Benchmark
        t_p.bpi                             = ratio(t_p.quoted_premium, t_p.benchmark_premium)
        t_p.expected_loss_ratio             = ratio(benchmark_lr, t_p.bpi)
        t_p.benchmark_premium_pre_uw_adj    = ratio(t_p.model_premium_pre_uw_adj * business_plan_lr, benchmark_lr)
        t_p.bpi_pre_uw_adj                  = ratio(t_p.quoted_premium, t_p.benchmark_premium_pre_uw_adj)
        t_p.expected_loss_ratio_pre_uw_adj  = ratio(benchmark_lr, t_p.bpi_pre_uw_adj)
        
        # Technical pre-UW adjustments
        expected_loss_cost_pre_uw_adj_100_pct=t_p.benchmark_premium_pre_uw_adj * benchmark_lr  * (1 - layer.brokerage)
        layer.expected_loss_cost_pre_uw_adj = expected_loss_cost_pre_uw_adj_100_pct * written_line
        t_p.technical_premium_pre_uw_adj    = calculate_technical_premium(hxd, expected_loss_cost_pre_uw_adj_100_pct, expected_loss_cost_pre_uw_adj_100_pct)
        t_p.tpi_pre_uw_adj                  = ratio(t_p.quoted_premium, t_p.technical_premium_pre_uw_adj)
        # Push results to standard nodes
        layer.benchmark_premium             = t_p.benchmark_premium * written_line
        layer.technical_premium             = t_p.technical_premium * written_line
        layer.technical_premium_pre_uw_adj  = t_p.technical_premium_pre_uw_adj * written_line
        layer.tpi                           = t_p.tpi
        layer.tpi_pre_uw_adj                = t_p.tpi_pre_uw_adj
        layer.bpi                           = t_p.bpi
        layer.bpi_pre_uw_adj                = t_p.bpi_pre_uw_adj

        # Additional metrics for CDS
        layer.pflr              = ratio(benchmark_lr, layer.bpi)
        layer.pflr_pre_uw_adj   = ratio(benchmark_lr, layer.bpi_pre_uw_adj)
        quoted_premium_net      = layer.quoted_premium_case_priced * (1 - layer.brokerage)
        expense_ratio           = tp["var_exp"]    +    ratio(tp["fixed_exp"] + layer.expected_loss_cost * tp["che"],    quoted_premium_net)
        layer.roc               = ratio(1   -   layer.pflr   -   (tp["cost_of_ri"] - tp["ri_rec"])   -   expense_ratio   +   tp["inv_inc"],    tp["capital_req"])
        layer.uw_adj_impact     = ratio(layer.expected_loss_cost, layer.expected_loss_cost_pre_uw_adj)
    
        # Store annualised premiums for use in rate change calcs
        layer.quoted_premium_annualised     = t.quoted_premium    * written_line
        layer.benchmark_premium_annualised  = t.benchmark_premium * written_line

    if hxd.cds.standard_fields.is_case_priced and layer.quoted_premium_case_priced > 0 :
        benchmark_premium = 0
        if layer.bpi_case_priced > 0: 
            benchmark_premium = ratio(layer.quoted_premium_case_priced, layer.bpi_case_priced)
            
            layer.expected_loss_cost = benchmark_premium * benchmark_lr * (1 - brokerage)
            technical_premium_net_100 = ratio((layer.expected_loss_cost * (1 + tp["che"]) + tp["fixed_exp"]), tp["technical_lr"])

            layer.technical_premium =  ratio(technical_premium_net_100, (1 - (layer.brokerage or 0)))
            layer.technical_premium_net = layer.technical_premium * (1 - brokerage)  
            layer.tpi = ratio(layer.quoted_premium_case_priced, layer.technical_premium)
            layer.tpi_pre_uw_adj = layer.tpi
            layer.technical_premium_pre_uw_adj = layer.technical_premium
            
            # Additional metrics for CDS
            layer.pflr = ratio(benchmark_lr, layer.bpi_case_priced)
            quoted_premium_net = layer.quoted_premium_case_priced * (1 - brokerage)
            layer.roc = ratio(
                1 - layer.pflr - tp["var_exp"] + tp["inv_inc"] - (tp["cost_of_ri"] - tp["ri_rec"]) - ratio(tp["fixed_exp"] + layer.expected_loss_cost * tp["che"], quoted_premium_net),
                tp["capital_req"]
            )
            layer.benchmark_premium = benchmark_premium
        layer.benchmark_premium_annualised  = t.benchmark_premium * written_line
        layer.quoted_premium_annualised     = t.benchmark_premium * written_line

    # UW Authorities
    
    label_value = ["New Business - Gross Line Cost", "New Business - Beazley Net Premium", "Renewal - Gross Line Cost", "Renewal - Beazley Net Premium"]
    filtered_UWs = Underwriters[Underwriters["name"] == sf.underwriter]

    for auth in authorities:
        value = None if filtered_UWs.empty else filtered_UWs[auth].iloc[0]
        setattr(uw_a, auth, value)
        
    for auth in authorities:
        value = None if filtered_UWs.empty else filtered_UWs[auth].iloc[0]
        # convert all values beside terms
        if (auth != 'term'):
            value = to_ccy(value, ccy) if value else value
        setattr(uw_a_current_currency, auth, value)

    def calculate_gross_line(line, written_line, order, basis, limit, fx_rate):
        if line is not None:            return ratio(order * line if basis == "Of Order" else line, fx_rate)
        elif written_line is not None:  return limit * ratio(order * written_line if basis == "Of Order" else written_line, fx_rate)
        elif line is not None:          return limit * ratio(ratio(line, limit), fx_rate)      # Redundant check, but keeping for clarity
        return None

    def calculate_net_premium(quoted_premium, brokerage, line, written_line, order, basis, limit, fx_rate):
        return ratio( (quoted_premium or 0)   
                            * (1 - brokerage) 
                            * (order * written_line if basis == "Of Order" else written_line) 
                            if written_line is not None else ratio(line, limit)
                        , fx_rate)

    gross_line  = calculate_gross_line( layer.line,                     layer.written_line,
                                        layer.order,                    layer.written_line_basis,
                                        limit,                          expo_g.fx_to_usd)

    net_premium = calculate_net_premium(layer.quoted_premium_100_pct,   brokerage,
                                        layer.line,                     layer.written_line,
                                        layer.order,                    layer.written_line_basis,
                                        limit,                          expo_g.fx_to_usd)

    gross_line_current_currency =calculate_gross_line( layer.line,                     layer.written_line,
                                        layer.order,                    layer.written_line_basis,
                                        limit,                          1)
    net_premium_current_currency = calculate_net_premium(layer.quoted_premium_100_pct,   brokerage,
                                        layer.line,                     layer.written_line,
                                        layer.order,                    layer.written_line_basis,
                                        limit,                          1)
    if sf.is_renewal:
        uw_p.ren_gross_line     = gross_line
        uw_p.ren_net_premium    = net_premium
        uw_p_current_currency.ren_gross_line     = gross_line_current_currency
        uw_p_current_currency.ren_net_premium    = net_premium_current_currency
    else:
        uw_p.nb_gross_line      = gross_line
        uw_p.nb_net_premium     = net_premium
        uw_p_current_currency.nb_gross_line     = gross_line_current_currency
        uw_p_current_currency.nb_net_premium    = net_premium_current_currency

    term_diff = relativedelta(expiry_date, inception_date)
    
    #YZ: 23/10/2025 update the term difference: The expiry date adjustment. if term:  01/07/2024 - 30/06/2025, it is still one year.
    expiry_date_1_year = inception_date + relativedelta(years = 1)
    if (expiry_date_1_year - expiry_date).days == 1:
        month_diff = 12
        uw_p.term = term_diff.years * 12 + month_diff
    else : 
        uw_p.term = term_diff.years * 12 + term_diff.months

    uw_p_current_currency.term = uw_p.term
    for auth in authorities:
        pol_value   = getattr(uw_p, auth)
        auth_value  = getattr(uw_a, auth)
        if (pol_value is None) or (auth_value is None):     continue
        elif pol_value > auth_value:                        setattr(uw_w, auth, "❗❗ Above limit ❗❗")

    for auth in authorities:
        pol_value   = getattr(uw_p_current_currency, auth)
        auth_value  = getattr(uw_a_current_currency, auth)
        if (pol_value is None) or (auth_value is None):     continue
        elif pol_value > auth_value:                        setattr(uw_w_current_currency, auth, "❗❗ Above limit ❗❗")

    ### --- PERIL SHEET --- ###
    cvg_perils_tbl      = hx.params.coverage_perils
    coverages           = [c.coverage for c in expo_g.countries]
    subcoverages        = [c.subcoverage for c in expo_g.countries]

    # Get limits per coverage
    countries_df        = pd_df_from_hx_list(expo_g.countries)
    old_col_name_list   = ["coverage", "subcoverage", "limit",      "sublimit",     "excess",       "deductible"]
    new_col_name_list   = ["coverage", "subcoverage", "cvg_limit",  "subcvg_limit", "cvg_excess",   "cvg_deductible"]
    rename_dict         = dict(zip(old_col_name_list,new_col_name_list))
    countries_df        = countries_df[  old_col_name_list  ].rename(  columns=rename_dict )  # notice we are selecting columns here too

    countries_df["subcvg_excess"]       = countries_df["cvg_excess"]
    countries_df["subcvg_deductible"]   = countries_df["cvg_deductible"]


    cvg_col_list    = ["coverage",    "cvg_limit",    "cvg_excess",    "cvg_deductible"]
    subcvg_col_list = ["subcoverage", "subcvg_limit", "subcvg_excess", "subcvg_deductible"]
    merged_tbl      = (cvg_perils_tbl
                        .merge( countries_df[cvg_col_list],     on="coverage",                                  how="left" )
                        .merge( countries_df[subcvg_col_list],  left_on="coverage", right_on="subcoverage",     how="left" )
                        .fillna(0)    )

    for peril in perils.keys():
        filtered_df         = merged_tbl[merged_tbl["peril"] == peril]
        is_peril_present    = any(filtered_df["coverage"].isin(coverages)) or any(filtered_df["coverage"].isin(subcoverages))

        fields              = ["is_covered","limit","excess","deductible"]
        for field in fields:
            if field == "is_covered":   calculated  = "Yes" if is_peril_present else "No"
            else:                       calculated  = 0 if pd.isna(x := filtered_df[[f"cvg_{field}", f"subcvg_{field}"]].max().max()) else x                       
            override    = rgetattr(expo_a, f"perils/{peril}/{field}_override")
            selected    = override or calculated
            
            # forcing selected to nil where is_covered is no
            if field != "is_covered":
                is_covered = rgetattr(expo_a, f"perils/{peril}/is_covered_selected")
                if is_covered == "No":
                    selected = 0 

            rsetattr(expo_a.perils, f"{peril}/{field}_calculated",   calculated)
            rsetattr(expo_a.perils, f"{peril}/{field}_selected",     selected)


    # Compare limits to latest saved
    current_perils = {}
    for peril in perils.keys():
        current_perils[peril]                        = {}
        current_perils[peril]["limit_selected"]      = rgetattr(expo_a, f"perils/{peril}/limit_selected")
        current_perils[peril]["excess_selected"]     = rgetattr(expo_a, f"perils/{peril}/excess_selected")
        current_perils[peril]["deductible_selected"] = rgetattr(expo_a, f"perils/{peril}/deductible_selected")

    temp_perils             = json.loads(expo_a.temp_perils)
    expo_a.confirm_message  = "❗❗ Please confirm the limits are correct ❗❗"

    if current_perils == temp_perils:
        expo_a.confirm_message = "✅ Correct limits confirmed."
        expo_a.are_limits_correct = True
    else:
        hx.errors.validation("Please confirm that the limits in Peril Sheet are correct by clicking on 'Confirm limits'.")
    
    expo_a.cbi_peril_territory_covered_show = False
    if expo_a.cbi_perils.unnamed.is_covered_selected == "Yes": expo_a.cbi_peril_territory_covered_show = True
    if expo_a.cbi_perils.named.is_covered_selected   == "Yes": expo_a.cbi_peril_territory_covered_show = True


    # assign cds values
    layer.limit         = countries_df["cvg_limit"].fillna(0).max()
    layer.excess        = countries_df["cvg_excess"].fillna(0).min()
    layer.deductible    = countries_df["cvg_deductible"].fillna(0).min()

    layer.trifocus      = sf.trifocus



    return term_factor
    