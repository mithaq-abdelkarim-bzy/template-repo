import hx
from algorithms import parameter_tables_schema as params
from algorithms.rate_constants import benchmark_lr
from algorithms.rate_utilities import ratio, look_up
from algorithms.rate_constants import *
from algorithms.excess.rate_usml_excess_helpers import pro_rata_factor_calculation


def tpi_summary(hxd):

    # Set rating methodology
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == "Case Priced"
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == "Rater"

    # Pull in technical premium parameters and fx rates from user library
    tp_params_df = params.tp_parameters.df()
    fx_rates_df = params.fx_rates.df()
    yoa = hxd.hx_core.inception_date.year
    # To stop the model erroring if the inception year defaults to an old year not in the TP data
    if yoa in list(tp_params_df["year"]):
        tp_year = yoa
    else:
        tp_year = tp_params_df["year"].max()

    # Placeholder variables: update with correct benchmark class and modelled expected loss, this might need to
    # be linked if a rater can write to more than one class. May link to benchmark class in risk information.
    # bp_class = hxd.cds.standard_fields.benchmark_class
    bp_class = "US EPL"

    # Define function to look up bp class
    def tp_lookup(vbl, bp_class):
        out = tp_params_df[
            (tp_params_df["business_plan_class"] == bp_class)
            & (tp_params_df["year"] == tp_year)
        ][vbl].iloc[0]
        return out

    # Set up tp params
    che = tp_lookup("che", bp_class)
    var_exp = tp_lookup("var_exp", bp_class)
    inv_inc = tp_lookup("inv_inc", bp_class)
    cost_of_ri = tp_lookup("cost_of_ri", bp_class)
    ri_rec = tp_lookup("ri_rec", bp_class)
    roc = tp_lookup("roc", bp_class)
    fixed_exp_usd = tp_lookup("fixed_exp", bp_class)
    capital_req = tp_lookup("capital_req", bp_class)
    nmp_load = tp_lookup("nmp_load", bp_class)

    # Convert fixed expenses to model currency (default to USD if error)
    ccy = hxd.cds.currencies.source_currency
    fixed_exp = fixed_exp_usd * look_up(
        ccy, "ccy", "fx_rate", fx_rates_df, if_not_found=1
    )
    table_capital_load_primary_excess = hx.params.table_capital_load_primary_excess
    primary_excess = hxd.cds.layers[0].is_primary_excess or "Primary"
    capital_load = table_capital_load_primary_excess.loc[
        table_capital_load_primary_excess["primary_excess"] == primary_excess,
        "factor",
    ].iloc[0]

    # Calculate technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc * capital_load

    final_premium_summary = hxd.cds.final_premium_summary
    is_admitted = hxd.cds.standard_fields.is_admitted_or_surplus == "Admitted"
    pro_rata_factor = pro_rata_factor_calculation(hxd)
    excess_term_premium = 0 if hxd.cds.admitted_excess.rounded_premium.value.selected is None else hxd.cds.admitted_excess.rounded_premium.value.selected*pro_rata_factor

    # if primary_excess == "Primary" and is_admitted:
    if primary_excess == "Primary":
        risk_bpi = final_premium_summary.bpi
        final_admitted_term_premium = final_premium_summary.final_admitted_term_premium
        benchmark_premium = final_premium_summary.benchmark_term_premium
        benchmark_premium_pre_uw_adj = final_premium_summary.benchmark_term_premium_pre_uw_adj
    else:
        risk_bpi = hxd.cds.admitted_excess_local.bpi.value
        #overwrite final_premium summary to reflect Excess BPI in top bar
        final_premium_summary.bpi = risk_bpi
        #also setting the final admitted term premium to the excess premium to bring it out in the front end
        final_premium_summary.final_admitted_term_premium = excess_term_premium
        final_admitted_term_premium = excess_term_premium
        benchmark_premium = hxd.cds.admitted_excess_local.benchmark_term_premium.value
        benchmark_premium_pre_uw_adj = hxd.cds.admitted_excess_local.benchmark_term_premium_pre_uw_adj.value

    final_premium_summary.benchmark_term_premium = benchmark_premium

    brokerage = hxd.cds.layers[0].brokerage or 0

    technical_term_premium = 0 if ((not final_admitted_term_premium) or (not risk_bpi) or (risk_bpi == 0)) else(
        final_admitted_term_premium
        / risk_bpi
        * 0.7
        * (1 + che)
        + fixed_exp_usd
    ) / (1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc * capital_load)
    final_premium_summary.technical_term_premium = technical_term_premium

    technical_term_premium_pre_uw_adj = 0 if ((not risk_bpi) or (risk_bpi == 0)) else(
        benchmark_premium_pre_uw_adj
        * 0.7
        * (1 + che)
        + fixed_exp_usd
    ) / (1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc * capital_load)

    final_premium_summary.tpi = 0 if ((not final_admitted_term_premium) or (not final_premium_summary.technical_term_premium) or (final_premium_summary.technical_term_premium == 0)) else ratio(
        final_admitted_term_premium, final_premium_summary.technical_term_premium
    )  

    layer = hxd.cds.layers[0]
    layer.quoted_premium = final_admitted_term_premium

    #an additional validation around the status and section reference        
    if  layer.status in ["Bound","Post Bind Complete"] and layer.section_reference is None:
        hx.errors.validation(
            f"A Section Reference must be entered if Status is set to Bound or Post Bind Complete"
        )

    if hxd.cds.standard_fields.is_rater_priced and final_admitted_term_premium:
        # NOTE if currency varies by layer you must convert fixed expenses fx within
        # the loop here
        # Note this is Beazley share for the calculation of TPI.
        # To update to 100%, scale by line size at the end
        # Expected loss increased by the NMP load
        # expected_loss = layer.expected_loss_cost * (1 + nmp_load)
        #As we don't know the expected loss we are using the benchmark premium and backing out the usual calc
        #the expected loss is calculated on gross term premium basis as per the excel rater
        if risk_bpi * expected_loss_ratio == 0:
            expected_loss = 0
            expected_loss_pre_uw_adj = 0
        else:    
            expected_loss = final_admitted_term_premium / risk_bpi * expected_loss_ratio
            expected_loss_pre_uw_adj = benchmark_premium_pre_uw_adj * expected_loss_ratio

        layer.expected_loss_cost = expected_loss  
        layer.expected_loss_cost_pre_uw_adj = expected_loss_pre_uw_adj

        layer.uw_adj_impact = ratio(layer.expected_loss_cost, layer.expected_loss_cost_pre_uw_adj) - 1
        
        layer.technical_premium = final_premium_summary.technical_term_premium
        layer.technical_premium_net = layer.technical_premium * (1 - brokerage)
        layer.technical_premium_pre_uw_adj = technical_term_premium_pre_uw_adj
      
        layer.benchmark_premium = final_premium_summary.benchmark_term_premium

        layer.bpi = ratio(final_admitted_term_premium, layer.benchmark_premium)
        
        layer.tpi = ratio(final_admitted_term_premium, final_premium_summary.technical_term_premium)
       
        layer.tpi_pre_uw_adj = ratio(
            final_admitted_term_premium, layer.technical_premium_pre_uw_adj
        )
        quoted_premium_net = final_admitted_term_premium * (1 - brokerage)
        layer.pflr = ratio(expected_loss, (quoted_premium_net or 1))
        # TODO: add Att and Cat expected loss to common data schema?
        # layer.pflr_att = ratio(layer.expected_loss_cost_att, (quoted_premium_net or 1))
        # layer.pflr_cat = ratio(layer.expected_loss_cost_cat, (quoted_premium_net or 1))
        layer.roc = ratio(
            1
            - layer.pflr
            - var_exp
            + inv_inc
            - (cost_of_ri - ri_rec)
            - ratio(fixed_exp + expected_loss * che, quoted_premium_net),
            capital_req,
        )
        layer.pflr_pre_uw_adj = layer.pflr
        layer.bpi_pre_uw_adj = ratio(layer.quoted_premium, benchmark_premium_pre_uw_adj)
    # For case pricing only
    if (
        hxd.cds.standard_fields.is_case_priced
        and final_admitted_term_premium
        and layer.bpi_case_priced
    ):
        layer.bpi = layer.bpi_case_priced
        final_premium_summary.bpi = layer.bpi_case_priced
        layer.benchmark_premium = ratio(final_admitted_term_premium, layer.bpi)
        layer.expected_loss_cost = (
            layer.benchmark_premium * benchmark_lr
        )
        layer.technical_premium = ratio(
            (layer.expected_loss_cost * (1 + che) + fixed_exp), technical_lr
        )
        layer.technical_premium_net = layer.technical_premium * (1 - brokerage)
        layer.tpi = ratio(final_admitted_term_premium, layer.technical_premium)
        final_premium_summary.tpi = layer.tpi
        layer.pflr = ratio(benchmark_lr, layer.bpi)
        layer.tpi_pre_uw_adj = layer.tpi
        layer.technical_premium_pre_uw_adj = technical_term_premium_pre_uw_adj
        quoted_premium_net = final_admitted_term_premium * (1 - brokerage)
        layer.roc = ratio(
            1
            - layer.pflr
            - var_exp
            + inv_inc
            - (cost_of_ri - ri_rec)
            - ratio(fixed_exp + layer.expected_loss_cost * che, quoted_premium_net),
            capital_req,
        )
        layer.uw_adj_impact = 0
