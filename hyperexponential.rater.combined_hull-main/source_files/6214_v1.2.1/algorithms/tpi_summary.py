import hx
import pandas as pd
import numpy as np
from algorithms import parameter_tables_schema as params
from algorithms.rate_utilities import ratio, look_up, calculate_policy_term
from algorithms import rate_constants as constants


def tpi_summary(hxd):

    # Set rating methodology
    hxd.cds.standard_fields.is_case_priced = (
        hxd.cds.standard_fields.rating_methodology == "Case Priced"
    )
    hxd.cds.standard_fields.is_rater_priced = (
        hxd.cds.standard_fields.rating_methodology == "Rater"
    )

    is_dev = False

    bp_class = hxd.cds.coverage_type if is_dev else "Hull"
    if not bp_class:
        return
    # Pull in technical premium parameters and fx rates from user library
    tp_params_df = (
        hx.params.table_original_rater_params if is_dev else params.tp_parameters.df()
    )
    fx_rates_df = params.fx_rates.df()
    tp_year = hxd.hx_core.inception_date.year
    # To stop the model erroring if the inception year defaults to an old year not in the TP data
    if tp_year not in list(
        tp_params_df[tp_params_df["business_plan_class"] == bp_class]["year"]
    ):
        tp_year = tp_params_df[tp_params_df["business_plan_class"] == bp_class][
            "year"
        ].max()

    # Placeholder variables: update with correct benchmark class and modelled expected loss, this might need to
    # be linked if a rater can write to more than one class. May link to benchmark class in risk information.
    # bp_class = hxd.cds.standard_fields.benchmark_class

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

    # Convert fixed expenses to model currency (default to USD if error)
    ccy = hxd.cds.currencies.source_currency
    fixed_exp = fixed_exp_usd * look_up(
        ccy, "ccy", "fx_rate", fx_rates_df, if_not_found=1
    )

    # Calculate technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc * capital_req
    policy_term = calculate_policy_term(
        hxd.cds.standard_fields.inception_date, hxd.cds.standard_fields.expiry_date
    )

    if hxd.cds.standard_fields.is_rater_priced:
        for layer in hxd.cds.layers:
            for coverage in layer.coverages:
                coverage_data = coverage[1]
                coverage_name = coverage[0]
                coverage_brokerage = (
                    coverage_data.brokerage.selected or 0
                    if (coverage_name == "iv") or (coverage_name == "war")
                    else coverage_data.brokerage or 0
                )
                coverage_written_line = (
                    coverage_data.written_line.selected or 0
                    if (coverage_name == "iv") or (coverage_name == "war")
                    else coverage_data.written_line or 0
                )
                coverage_data.rating_summary_brokerage = coverage_brokerage
                coverage_data.rating_summary_written_line = coverage_written_line
                # NOTE if currency varies by layer you must convert fixed expenses fx within
                # the loop here

                # Note this is Beazley share for the calculation of TPI.
                # To update to 100%, scale by line size at the end
                # Expected loss increased by the NMP load
                #

                if not coverage_data.expected_loss_cost_pro_rated_100pct:
                    continue
                expected_loss = (
                    coverage_data.expected_loss_cost_pro_rated_100pct or 0
                ) * coverage_written_line
                expected_loss_cost_pre_uw_adj = (
                    coverage_data.expected_loss_cost_pre_uw_adj or 0
                ) * coverage_written_line
                if coverage_written_line > 0:
                    coverage_data.technical_premium_net = (
                        ratio(
                            (expected_loss * (1 + che) + fixed_exp),
                            technical_lr,
                        )
                        / coverage_written_line
                    )

                    coverage_data.technical_premium_pro_rated_100pct = ratio(
                        coverage_data.technical_premium_net,
                        (1 - coverage_brokerage),
                    )
                    coverage_data.technical_premium = (
                        coverage_data.technical_premium_pro_rated_100pct
                        * coverage_written_line
                    )

                    coverage_data.technical_premium_pre_uw_adj_pro_rated_100pct = ratio(
                        ratio(
                            (expected_loss_cost_pre_uw_adj * (1 + che) + fixed_exp),
                            technical_lr,
                        ),
                        ((1 - coverage_brokerage) * coverage_written_line),
                    )
                    coverage_data.technical_premium_pre_uw_adj = (
                        coverage_data.technical_premium_pre_uw_adj_pro_rated_100pct
                        * coverage_written_line
                    )

                if not coverage_data.quoted_premium_pro_rated_100pct:
                    continue
                coverage_data.quoted_premium = (
                    coverage_data.quoted_premium_pro_rated_100pct
                    * coverage_written_line
                )
                coverage_data.quoted_premium_annualised_100pct = (
                    coverage_data.quoted_premium_pro_rated_100pct / (policy_term or 1)
                )

                coverage_data.quoted_premium_policy_term_100pct = (
                    coverage_data.quoted_premium_pro_rated_100pct * (policy_term or 1)
                )

                if coverage_data.benchmark_premium_pro_rated_100pct is not None:
                    coverage_data.benchmark_premium = (
                        coverage_data.benchmark_premium_pro_rated_100pct
                        * coverage_written_line
                    )

                    coverage_data.benchmark_premium_annualised_100pct = (
                        coverage_data.benchmark_premium_pro_rated_100pct
                        / (policy_term or 1)
                    )

                    coverage_data.benchmark_premium_policy_term_100pct = (
                        coverage_data.benchmark_premium_pro_rated_100pct
                    ) * (policy_term or 1)

                    coverage_data.bpi = ratio(
                        coverage_data.quoted_premium_pro_rated_100pct,
                        coverage_data.benchmark_premium_pro_rated_100pct,
                    )

                    benchmark_premium_pre_uw_adj_pro_rated_100pct = ratio(
                        coverage_data.benchmark_premium_pro_rated_100pct,
                        (1+coverage_data.uw_adj_impact)
                    )

                    coverage_data.benchmark_premium_pre_uw_adj = (
                        benchmark_premium_pre_uw_adj_pro_rated_100pct
                        * coverage_written_line
                    )

                    coverage_data.bpi_pre_uw_adj = ratio(
                        coverage_data.quoted_premium_pro_rated_100pct,
                        benchmark_premium_pre_uw_adj_pro_rated_100pct
                    )
                    
                    quoted_premium_net = (
                        coverage_data.quoted_premium_pro_rated_100pct * (1 - coverage_brokerage - (coverage_data.other_deductions or 0))
                        if coverage_name == "ship_building"
                        else coverage_data.quoted_premium_pro_rated_100pct
                        * (1 - coverage_brokerage)
                    )

                if coverage_data.technical_premium_pro_rated_100pct is not None:
                    coverage_data.tpi = ratio(
                        coverage_data.quoted_premium_pro_rated_100pct,
                        coverage_data.technical_premium_pro_rated_100pct,
                    )
                if (
                    coverage_data.technical_premium_pre_uw_adj_pro_rated_100pct
                    is not None
                ):
                    coverage_data.tpi_pre_uw_adj = ratio(
                        coverage_data.quoted_premium_pro_rated_100pct,
                        coverage_data.technical_premium_pre_uw_adj_pro_rated_100pct,
                    )

                coverage_data.pflr = ratio(coverage_data.expected_loss_cost_pro_rated_100pct, (quoted_premium_net or 1))
                expected_loss_cost_pre_uw_adj_pro_rated_100pct = ratio(
                    coverage_data.expected_loss_cost_pro_rated_100pct,
                    (1+coverage_data.uw_adj_impact)
                )
                coverage_data.pflr_pre_uw_adj = ratio(expected_loss_cost_pre_uw_adj_pro_rated_100pct,(quoted_premium_net or 1))
                # TODO: add Att and Cat expected loss to common data schema?
                # layer.pflr_att = ratio(layer.expected_loss_cost_att, (quoted_premium_net or 1))
                # layer.pflr_cat = ratio(layer.expected_loss_cost_cat, (quoted_premium_net or 1))
                coverage_data.roc = ratio(1- coverage_data.pflr - var_exp + inv_inc - (cost_of_ri - ri_rec)- ratio(fixed_exp + expected_loss * che, quoted_premium_net),capital_req)

    elif hxd.cds.standard_fields.is_case_priced:
        for layer in hxd.cds.layers:
            for coverage in layer.coverages:
                coverage_data = coverage[1]
                coverage_name = coverage[0]
                quoted_premium = coverage_data.quoted_premium_case_priced
                coverage_brokerage = (
                    coverage_data.brokerage.selected or 0
                    if (coverage_name == "iv") or (coverage_name == "war")
                    else coverage_data.brokerage or 0
                )
                coverage_written_line = (
                    coverage_data.written_line.selected or 0
                    if (coverage_name == "iv") or (coverage_name == "war")
                    else coverage_data.written_line or 0
                )
                coverage_data.rating_summary_brokerage = coverage_brokerage
                coverage_data.rating_summary_written_line = coverage_written_line
                bpi_case_priced = coverage_data.bpi_case_priced
                if not (
                    bpi_case_priced
                    and quoted_premium
                    and (bpi_case_priced != 0)
                    and (quoted_premium != 0)
                ):
                    continue

                coverage_data.bpi = coverage_data.bpi_case_priced
                coverage_data.quoted_premium_pro_rated_100pct = (
                    coverage_data.quoted_premium_case_priced
                )
                coverage_data.quoted_premium = (
                    coverage_data.quoted_premium_pro_rated_100pct
                    * coverage_written_line
                )
                coverage_data.quoted_premium_annualised_100pct = (
                    coverage_data.quoted_premium_pro_rated_100pct / (policy_term or 1)
                )

                coverage_data.benchmark_premium_policy_term_100pct = (
                    coverage_data.benchmark_premium_pro_rated_100pct
                ) * (policy_term or 1)

                coverage_data.quoted_premium_policy_term_100pct = (
                    coverage_data.quoted_premium_pro_rated_100pct * (policy_term or 1)
                )

                coverage_data.benchmark_premium_pro_rated_100pct = ratio(
                    coverage_data.quoted_premium_pro_rated_100pct, coverage_data.bpi
                )
                coverage_data.benchmark_premium = (
                    coverage_data.benchmark_premium_pro_rated_100pct
                    * coverage_written_line
                )
                coverage_data.benchmark_premium_annualised_100pct = (
                    coverage_data.benchmark_premium_pro_rated_100pct
                    / (policy_term or 1)
                )

                coverage_data.expected_loss_cost_pro_rated_100pct = (
                    coverage_data.benchmark_premium_pro_rated_100pct
                    * constants.benchmark_lr
                    * (1 - coverage_brokerage)
                )
                coverage_data.expected_loss_cost = (
                    coverage_data.expected_loss_cost_pro_rated_100pct
                    * coverage_written_line
                )

                coverage_data.technical_premium_net = ratio(
                    (
                        coverage_data.expected_loss_cost_pro_rated_100pct * (1 + che)
                        + fixed_exp
                    ),
                    technical_lr,
                )
                coverage_data.technical_premium_pro_rated_100pct = ratio(
                    coverage_data.technical_premium_net, (1 - coverage_brokerage)
                )
                coverage_data.technical_premium = (
                    coverage_data.technical_premium_pro_rated_100pct
                    * coverage_written_line
                )

                coverage_data.tpi = ratio(
                    coverage_data.quoted_premium_pro_rated_100pct,
                    coverage_data.technical_premium_pro_rated_100pct,
                )

                coverage_data.pflr = ratio(constants.benchmark_lr, coverage_data.bpi)
                coverage_data.tpi_pre_uw_adj = coverage_data.tpi
                coverage_data.technical_premium_pre_uw_adj_pro_rated_100pct = (
                    coverage_data.technical_premium_pro_rated_100pct
                )
                coverage_data.technical_premium_pre_uw_adj = (
                    coverage_data.technical_premium * coverage_written_line
                )

                quoted_premium_net = coverage_data.quoted_premium_pro_rated_100pct * (
                    1 - coverage_brokerage
                )

                coverage_data.roc = ratio(
                        1
                        - coverage_data.pflr
                        - var_exp
                        + inv_inc
                        - (cost_of_ri - ri_rec)
                        - ratio(
                            fixed_exp
                            + coverage_data.expected_loss_cost_pro_rated_100pct * che,
                            quoted_premium_net,
                        ),
                        capital_req
                )

