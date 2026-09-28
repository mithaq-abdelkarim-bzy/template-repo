import hx
import numpy as np
from algorithms.rate_utilities import ratio, look_up
from algorithms import parameter_tables_schema as params

benchmark_lr = 0.7
coverage_media_advertising_factor = 0.2
cont_bi_pd_factor = 0.1
first_party_privacy_factor = 0.2
cyber_extortion_only_factor = 0.15
general_liability_tech_factor = 0.1
general_liability_staffing_factor = 1.2

brokerage_base_price = {
    "Staffing": 0.275,
    "Products": 0.25,
    "Tech": 0.25,
    "MPL": 0.25,
    "Manutech": 0.25,
    "Med Mal": 0.25,
}


def product_types_with_aggregate_limits():
    return ["Manutech", "MPL", "Tech", "Med Mal"]


def product_types_with_defence_outside_limits():
    return ["Manutech", "Products", "Tech"]


def product_types_with_advertising_liability():
    return ["Products"]


def product_types_with_product_liability():
    return ["Products"]


def product_types_with_general_liability():
    return ["Staffing", "Tech"]


def bound_statuses():
    return ["Bound", "Post Bind Complete"]


def init_product_liability(hxd):
    product_type = hxd.cds.rating_factors.product_type
    if product_type in product_types_with_product_liability():
        hxd.cds.rating_factors.show_product_liability_limits_AGG = True
    else:
        hxd.cds.rating_factors.show_product_liability_limits_AGG = False


def init_defence_outside_limits(product_type, layer):
    if product_type in product_types_with_defence_outside_limits():
        defence_outside_limits_table = (
            hx.params.table_input_coverage_defence_outside_limits
        )

        filtered_limits = defence_outside_limits_table[
            defence_outside_limits_table["product_type"] == product_type
        ]["limit"].values

        layer.defence_outside_limits.list = [
            {"limit": item} for item in filtered_limits
        ]

        layer.defence_outside_limits.show = True
    else:
        layer.defence_outside_limits.show = False


def init_personal_advertising_liability_EEC(product_type, layer):
    if product_type in product_types_with_advertising_liability():
        personal_advertising_liability_EEC_table = (
            hx.params.table_input_coverage_EEC_liability_limits
        )

        filtered_limits = personal_advertising_liability_EEC_table[
            personal_advertising_liability_EEC_table["product_type"] == product_type
        ]["limit"].values

        layer.personal_advertising_liability_EEC.list = [
            {"limit": item} for item in filtered_limits
        ]

        layer.personal_advertising_liability_EEC.show = True
    else:
        layer.personal_advertising_liability_EEC.show = False


def init_primary_deductible(product_type, layer):
    deductible_table = hx.params.table_input_coverage_deductible

    filtered_limits = deductible_table[
        deductible_table["product_type"] == product_type
    ]["deductible"].values

    layer.primary_deductible.list = [{"deductible": item} for item in filtered_limits]


def init_aggregate_limits(product_type, layer):
    if product_type in product_types_with_aggregate_limits():
        layer.liability_limits_AGG.show = True
    else:
        layer.liability_limits_AGG.show = False

    agg_liability_limits_table = hx.params.table_input_coverage_AGG_liability_limits

    # Get the current professional experience row based on professional experience name
    filtered_limits = agg_liability_limits_table[
        agg_liability_limits_table["product_type"] == product_type
    ]["limit"].values

    layer.liability_limits_AGG.list = [{"limit": item} for item in filtered_limits]


def init_general_liability(hxd, layer):
    rating_general_liability = hxd.cds.rating_factors.general_liability
    product_type = hxd.cds.rating_factors.product_type
    if product_type in product_types_with_general_liability():
        rating_general_liability.show = True
        if product_type == "Staffing":
            hxd.cds.rating_factors.show_staffing_liability_limits_AGG = True
            layer.general_liability.limit_staffing = layer.limit
            rating_general_liability.show_staffing = rating_general_liability.value
        else:
            hxd.cds.rating_factors.show_staffing_liability_limits_AGG = False
            rating_general_liability.show_staffing = False
    else:
        rating_general_liability.show = False
        hxd.cds.rating_factors.show_staffing_liability_limits_AGG = False
        rating_general_liability.show_staffing = False


def init_tech_options(hxd):
    product_type = hxd.cds.rating_factors.product_type
    if product_type == "Tech":
        hxd.cds.rating_factors.tech.show = True
    else:
        hxd.cds.rating_factors.tech.show = False


def init_blueprint_premium_table(hxd, layer):
    product_type = hxd.cds.rating_factors.product_type
    if product_type == "Manutech":
        premium_table = hx.params.table_minimum_premium
        premium_table_filtered_rows = premium_table[
            premium_table["product_type"] == product_type
        ]

        layer.premium_blueprint.list = [
            {"limit": row[1]["limit"], "premium": row[1]["premium"]}
            for row in premium_table_filtered_rows.iloc[1:].iterrows()
        ]
        layer.premium_blueprint.show = True


def init_eec_limits(layer, product_type):
    ecc_liability_limts_table = hx.params.table_input_coverage_EEC_liability_limits
    filtered_limits = ecc_liability_limts_table[
        ecc_liability_limts_table["product_type"] == product_type
    ]["limit"].values

    layer.liability_limits_EEC.list = [{"limit": item} for item in filtered_limits]


def calculate_premiums(
    layer,
    ccy,
    inception_year,
    is_rater_priced,
    calculated_price,
    underwriter_judgement_factor,
    min_premium,
):

    fx_rates_df = params.fx_rates.df()
    bp_class = "US Specialty Programmes"
    tp_params_df = params.tp_parameters.df()
    fx_rates_df = params.fx_rates.df()
    # To stop the model erroring if the inception year defaults to an old year not in the TP data
    if inception_year in list(tp_params_df["year"]):
        tp_year = inception_year
    else:
        tp_year = tp_params_df["year"].max()

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
    fixed_exp = fixed_exp_usd * look_up(
        ccy, "ccy", "fx_rate", fx_rates_df, if_not_found=1
    )

    # Calculate technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc * capital_req
    layer_quoted_premium = layer.quoted_premium or 0
    layer_brokerage = layer.brokerage or 0
    expected_losses = calculated_price * benchmark_lr
    expected_losses_pre_uw_adj = expected_losses / underwriter_judgement_factor

    if is_rater_priced:

        layer.uw_adj_impact = ratio(expected_losses, expected_losses_pre_uw_adj) - 1

        layer.technical_premium_net = ratio(
            (expected_losses * (1 + che) + fixed_exp), technical_lr
        )
        layer_technical_premium_net = layer.technical_premium_net or 0
        layer.technical_premium = ratio(
            layer_technical_premium_net, (1 - layer_brokerage)
        )

        layer.technical_premium_pre_uw_adj = ratio(
            ratio((expected_losses_pre_uw_adj * (1 + che) + fixed_exp), technical_lr),
            (1 - layer_brokerage),
        )
        layer.benchmark_premium = ratio(
            ratio(expected_losses, benchmark_lr), (1 - layer_brokerage)
        )

        layer.bpi = ratio(layer_quoted_premium, layer.benchmark_premium)
        layer.tpi = ratio(layer_quoted_premium, layer.technical_premium)
        layer.tpi_pre_uw_adj = ratio(
            layer_quoted_premium, layer.technical_premium_pre_uw_adj
        )

        quoted_premium_net = layer_quoted_premium * (1 - layer_brokerage)
        layer.pflr = ratio(expected_losses, (quoted_premium_net or 1))
        layer.roc = ratio(
            1
            - layer.pflr
            - var_exp
            + inv_inc
            - (cost_of_ri - ri_rec)
            - ratio(fixed_exp + expected_losses * che, quoted_premium_net),
            capital_req,
        )
    else:
        layer.bpi = layer.bpi_case_priced or 1
        layer.benchmark_premium = ratio(layer_quoted_premium, layer.bpi)
        expected_losses = layer.benchmark_premium * benchmark_lr * (1 - layer_brokerage)

        layer.technical_premium_net = ratio(
            (expected_losses * (1 + che) + fixed_exp), technical_lr
        )
        layer.technical_premium = ratio(
            layer.technical_premium_net, (1 - layer_brokerage)
        )

        layer.tpi = ratio(layer_quoted_premium, layer.technical_premium)
        layer.pflr = ratio(benchmark_lr, layer.bpi)
        layer.tpi_pre_uw_adj = layer.tpi
        layer.technical_premium_pre_uw_adj = layer.technical_premium

        quoted_premium_net = layer_quoted_premium * (1 - layer_brokerage)
        layer.roc = ratio(
            1
            - layer.pflr
            - var_exp
            + inv_inc
            - (cost_of_ri - ri_rec)
            - ratio(fixed_exp + expected_losses * che, quoted_premium_net),
            capital_req,
        )
    layer.model_premium = max(layer.benchmark_premium, min_premium)


def init_layers(hxd, layer, product_type, is_rater_priced):

    init_eec_limits(layer, product_type)
    init_aggregate_limits(product_type, layer)
    init_defence_outside_limits(product_type, layer)
    init_primary_deductible(product_type, layer)
    init_personal_advertising_liability_EEC(product_type, layer)
    init_product_liability(hxd)
    init_general_liability(hxd, layer)
    init_blueprint_premium_table(hxd, layer)

    calculated_price = 0
    underwriter_judgement_factor = 1
    min_premium = 0

    if product_type == "Manutech":
        calculated_price, underwriter_judgement_factor, min_premium = (
            calculate_manutech(hxd, layer)
        )
    elif product_type == "Products":
        calculated_price, underwriter_judgement_factor, min_premium = (
            calculate_products(hxd, layer)
        )
    elif product_type == "Tech":
        calculated_price, underwriter_judgement_factor, min_premium = calculate_tech(
            hxd, layer
        )
    elif product_type == "Med Mal":
        calculated_price, underwriter_judgement_factor, min_premium = calculate_med_mal(
            hxd, layer
        )
    elif product_type == "Staffing":
        calculated_price, underwriter_judgement_factor, min_premium = (
            calculate_staffing(hxd, layer)
        )
    elif product_type == "MPL":
        calculated_price, underwriter_judgement_factor, min_premium = calculate_mpl(
            hxd, layer
        )

    ccy = hxd.cds.currencies.source_currency
    inception_year = hxd.hx_core.inception_date.year

    calculate_premiums(
        layer,
        ccy,
        inception_year,
        is_rater_priced,
        calculated_price,
        underwriter_judgement_factor,
        min_premium,
    )


def calculate_staffing_premiums(product_type, total_revenue, staffing):
    total_revenue = 0 if total_revenue is None else total_revenue
    if product_type == "Staffing":
        permanent_staffing_modifier = 0.00275
        temporary_staffing_modifier = 0.003
        peo_staffing_modifier = 0.0001475

        permanent_staffing_factor = (
            0 if staffing.permanent is None else staffing.permanent
        )
        temporary_staffing_factor = (
            0 if staffing.temporary is None else staffing.temporary
        )
        peo_staffing_factor = 0 if staffing.peo is None else staffing.peo

        permanent_staffing_premium = (
            total_revenue * permanent_staffing_modifier * permanent_staffing_factor
        )
        temporary_staffing_premium = (
            total_revenue * temporary_staffing_modifier * temporary_staffing_factor
        )
        peo_staffing_premium = (
            total_revenue * peo_staffing_modifier * peo_staffing_factor
        )

    return (
        permanent_staffing_premium,
        temporary_staffing_premium,
        peo_staffing_premium,
    )


def calculate_staffing_tier_discount(
    product_type, hazard_tier_factors_table, revenues, total_revenue
):
    tier_discount = 0
    total_revenue = 0 if total_revenue is None else total_revenue
    if total_revenue > 0:
        for revenue in revenues:
            if revenue.hazard_tier.tier is not None and revenue.value is not None:
                hazard_tier_factor_row = hazard_tier_factors_table[
                    (hazard_tier_factors_table["product_type"] == product_type)
                    & (hazard_tier_factors_table["tier"] == revenue.hazard_tier.tier)
                ]["factor"].values
                if (
                    hazard_tier_factor_row is not None
                    and len(hazard_tier_factor_row) > 0
                ):
                    tier_discount += (
                        revenue.value / total_revenue
                    ) * hazard_tier_factor_row[0]
    return tier_discount


def calculate_eec_limit_modifier(product_type, eec_limit_table, layer_limit, is_excess):
    eec_modifier = 1
    if not is_excess:
        eec_limit_row = eec_limit_table[
            (eec_limit_table["product_type"] == product_type)
            & (eec_limit_table["limit"] == layer_limit)
        ]

        if eec_limit_row is not None and len(eec_limit_row) > 0:
            eec_modifier = eec_limit_row["limit_factor"].values[0]

    return eec_modifier


def calculate_staffing_agg_limit_modifier(
    product_type, liability_agg_eec_ratio_table, layer_agg_limit, layer_eec_limit
):
    agg_limit_factor = 1
    if (
        product_type == "Staffing"
        and (layer_agg_limit is not None)
        and (layer_eec_limit is not None)
        and (layer_eec_limit > 0)
    ):
        if layer_agg_limit == 2000000 and layer_eec_limit == 1000000:
            return agg_limit_factor
        elif layer_agg_limit == 1000000 and layer_eec_limit == 1000000:
            agg_limit_factor = 1.15
        else:
            liability_agg_eec_ratio_rows = liability_agg_eec_ratio_table[
                liability_agg_eec_ratio_table["product_type"] == product_type
            ]
            limit_agg_linear_interpolation = np.interp(
                layer_agg_limit / layer_eec_limit,
                liability_agg_eec_ratio_rows["agg_eec_ratio"].values,
                liability_agg_eec_ratio_rows["factor"].values,
            )
            agg_limit_factor = limit_agg_linear_interpolation
    return agg_limit_factor


def calculate_mpl_agg_limit_modifier(
    product_type, liability_agg_eec_ratio_table, layer_agg_limit, layer_eec_limit
):

    agg_limit_factor = 1
    if (
        product_type == "MPL"
        and (layer_agg_limit is not None)
        and (layer_eec_limit is not None)
        and (layer_eec_limit > 0)
    ):
        liability_agg_eec_ratio_rows = liability_agg_eec_ratio_table[
            liability_agg_eec_ratio_table["product_type"] == product_type
        ]
        limit_agg_linear_interpolation = np.interp(
            layer_agg_limit / layer_eec_limit,
            liability_agg_eec_ratio_rows["agg_eec_ratio"].values,
            liability_agg_eec_ratio_rows["factor"].values,
        )
        agg_limit_factor = limit_agg_linear_interpolation
    return agg_limit_factor


def calculate_staffing_state_modifier(state_factors_table, state):
    state_factor = 1
    state_factor_row = state_factors_table[state_factors_table["state_code"] == state][
        "factor"
    ].values

    if state_factor_row is not None and len(state_factor_row) > 0:
        state_factor = state_factor_row[0]

    return state_factor


def calculate_staffing_min_premium_modifier(
    min_premium_factors_table,
    layer_eec_limit,
    layer_agg_limit,
    permanent_staffing_premium,
    temporary_staffing_premium,
    peo_staffing_premium,
):
    min_premium_modifier = 1
    min_premium_factor_row = min_premium_factors_table[
        (min_premium_factors_table["eec_limit"] == layer_eec_limit)
        & (min_premium_factors_table["agg_limit"] == layer_agg_limit)
    ]

    if min_premium_factor_row is not None and len(min_premium_factor_row) > 0:

        if (
            (permanent_staffing_premium > 0 and temporary_staffing_premium > 0)
            or (permanent_staffing_premium > 0 and peo_staffing_premium > 0)
            or (temporary_staffing_premium > 0 and peo_staffing_premium > 0)
        ):
            min_premium_modifier = min_premium_factor_row["mixed"].values

        else:
            if permanent_staffing_premium > 0:
                min_premium_modifier = min_premium_factor_row["permanent"].values
            elif temporary_staffing_premium > 0:
                min_premium_modifier = min_premium_factor_row["temp"].values
            elif peo_staffing_premium > 0:
                min_premium_modifier = min_premium_factor_row["peo"].values

    return min_premium_modifier


def calculate_tier_type_revenues(
    product_type,
    hazard_tier_factors_table,
    revenue_types_factors_table,
    revenues,
    total_revenue,
):
    total_revenue_divided_by_1000 = (
        0 if total_revenue is None else (total_revenue / 1000)
    )
    tier_type_revenue = 0
    total_factor_percentage = 0
    revenues_dict = {}
    for i, revenue in enumerate(revenues):
        if revenue.hazard_tier.tier is not None:
            hazard_tier_factor_row = hazard_tier_factors_table[
                (hazard_tier_factors_table["product_type"] == product_type)
                & (hazard_tier_factors_table["tier"] == revenue.hazard_tier.tier)
            ]["factor"].values
            if hazard_tier_factor_row is not None and len(hazard_tier_factor_row) > 0:

                if product_type in ["Manutech", "Products"]:
                    revenue_type_factor_row = revenue_types_factors_table[
                        (revenue_types_factors_table["product_type"] == product_type)
                        & (revenue_types_factors_table["revenue_type"] == revenue.type)
                    ]["factor"].values
                    if (
                        revenue_type_factor_row is not None
                        and len(revenue_type_factor_row) > 0
                    ):
                        factor = hazard_tier_factor_row[0] * revenue_type_factor_row[0]
                        percentage = (
                            (revenue.value / total_revenue)
                            if revenue.value is not None
                            and total_revenue_divided_by_1000 is not None
                            and total_revenue_divided_by_1000 != 0
                            else 0
                        )
                        revenues_dict[i] = {
                            "factor": factor,
                            "percentage_of_total_revenue": percentage,
                        }
                        total_factor_percentage += factor * percentage
                elif revenue.value is not None:
                    tier_type_revenue += revenue.value * hazard_tier_factor_row[0]
    if tier_type_revenue == 0:
        tier_type_revenue = (
            total_factor_percentage * total_revenue_divided_by_1000
            if total_factor_percentage is not None
            and total_revenue_divided_by_1000 is not None
            else 0
        )
    return tier_type_revenue


def calculate_revenue_band(
    product_type, revenue_bands_table, tier_type_revenue, total_revenue
):
    revenue_band = tier_type_revenue
    revenue_band_rows = revenue_bands_table[
        (revenue_bands_table["product"] == product_type)
    ]

    if revenue_band_rows is not None and len(revenue_band_rows) > 0:
        linear_interpolation = np.interp(
            total_revenue,
            revenue_band_rows["band"].values,
            revenue_band_rows["factor"].values,
        )
        revenue_band = linear_interpolation * tier_type_revenue

    return revenue_band


def calculate_deductible_modifier(product_type, deductible_table, layer_deductible):
    deductible_modifier = 1
    deductible_factor = deductible_table[
        (deductible_table["product_type"] == product_type)
        & (deductible_table["deductible"] == layer_deductible)
    ]["factor"].values

    if deductible_factor is not None and len(deductible_factor) > 0:
        deductible_modifier = deductible_factor[0]

    return deductible_modifier


def calculate_staffing_deductible_modifier(
    product_type, deductible_table, layer_deductible
):
    layer_deductible = 0 if layer_deductible is None else layer_deductible
    deductible_modifier = 0
    deductible_row = deductible_table[
        (deductible_table["product_type"] == product_type)
    ]

    if deductible_row is not None and len(deductible_row) > 0:
        deductible_modifier = np.interp(
            layer_deductible / 5000,
            deductible_table["ratio"].values,
            deductible_table["factor"].values,
        )

    return deductible_modifier


def calculate_mpl_deductible_modifier(
    product_type, deductible_table, layer_deductible, guideline_deductible
):
    layer_deductible = 0 if layer_deductible is None else layer_deductible
    deductible_modifier = 0
    deductible_row = deductible_table[
        (deductible_table["product_type"] == product_type)
    ]

    if deductible_row is not None and len(deductible_row) > 0:
        deductible_modifier = np.interp(
            (layer_deductible / guideline_deductible),
            deductible_table["ratio"].values,
            deductible_table["factor"].values,
        )

    return deductible_modifier


def calculate_prior_acts_modifier(
    product_type, retroactive_years_table, retroactive_years
):
    prior_acts_modifier = 1
    retroactive_years = retroactive_years_table[
        (retroactive_years_table["product"] == product_type)
        & (retroactive_years_table["years"] == retroactive_years)
    ]["factor"].values

    if retroactive_years is not None and len(retroactive_years) > 0:
        prior_acts_modifier = retroactive_years[0]

    return prior_acts_modifier


def calculate_loss_experience_modifier(
    product_type, loss_experience_table, exposure_loss_experience
):
    loss_experience_modifier = 1
    loss_experience_row = loss_experience_table[
        (loss_experience_table["product"] == product_type)
        & (
            loss_experience_table["number_of_claims_in_years"]
            == exposure_loss_experience
        )
    ]["factor"].values

    if loss_experience_row is not None and len(loss_experience_row) > 0:
        loss_experience_modifier = loss_experience_row[0]

    return loss_experience_modifier


def calculate_minimum_premium_factor(product_type, eec_limit_table, layer_limit):
    min_premium_factor = 0
    eec_limit_row = eec_limit_table[
        (eec_limit_table["product_type"] == product_type)
        & (eec_limit_table["limit"] == layer_limit)
    ]

    if eec_limit_row is not None and len(eec_limit_row) > 0:
        min_premium_factor = eec_limit_row["min_premium_factor"].values[0]

    return min_premium_factor


def calculate_aggregate_limit(
    product_type,
    liability_agg_eec_ratio_table,
    layer_agg_limit,
    layer_eec_limit,
    eec_limit,
):
    agg_limit_factor = 1
    if (
        (layer_agg_limit is not None)
        and (layer_eec_limit is not None)
        and (layer_eec_limit > 0)
    ):
        agg_eec_ratio = layer_agg_limit / layer_eec_limit

        liability_agg_eec_ratio_rows = liability_agg_eec_ratio_table[
            liability_agg_eec_ratio_table["product_type"] == product_type
        ]

        limit_agg_linear_interpolation = np.interp(
            agg_eec_ratio,
            liability_agg_eec_ratio_rows["agg_eec_ratio"].values,
            liability_agg_eec_ratio_rows["factor"].values,
        )

        agg_limit_factor = limit_agg_linear_interpolation

    agg_limit = eec_limit * agg_limit_factor
    return agg_limit


def calculate_excess_modifier(excess_factors_table, layer_excess, is_excess):
    excess_factor = 1
    if is_excess:
        excess_factors_interpolation = np.interp(
            layer_excess,
            excess_factors_table["excess"].values,
            excess_factors_table["factor"].values,
        )
        excess_factor = 1 - excess_factors_interpolation
    return excess_factor


def calculate_defence_outside_limits_modifier(
    product_type, defence_outside_limits_table, layer_defence_outside_limits
):
    defence_outside_limit_factor = 0
    if layer_defence_outside_limits is not None:
        defence_outside_limit_row = defence_outside_limits_table[
            (defence_outside_limits_table["product_type"] == product_type)
            & (defence_outside_limits_table["limit"] == layer_defence_outside_limits)
        ]["factor"].values
        if (
            defence_outside_limit_row is not None
            and len(defence_outside_limit_row) == 1
        ):
            defence_outside_limit_factor = defence_outside_limit_row[0]

    return defence_outside_limit_factor


def calculate_brokerage(product_type, layer_brokerage, underwriter_judgement):

    product_brokerage_base_price = brokerage_base_price[product_type]
    brokerage = 0
    if layer_brokerage < 1:
        brokerage = (underwriter_judgement * (1 - product_brokerage_base_price)) / (
            1 - layer_brokerage
        )
    return brokerage


def calculate_longevity_modifier(current_product, longevity_table, layer_longevity):
    longevity_table = hx.params.table_input_longevity
    longevity_modifier = 1

    factor_rows = longevity_table[
        (longevity_table["years"] == layer_longevity)
        & (longevity_table["product_type"] == current_product)
    ]["factor"].values

    if factor_rows is not None and len(factor_rows) == 1:
        longevity_modifier = factor_rows[0]
    return longevity_modifier


def calculate_revenue_totals_by_tier(revenues):
    revenue_totals_by_tier = {}

    for revenue in revenues:
        tier = revenue.hazard_tier.tier
        if tier in revenue_totals_by_tier:
            revenue_totals_by_tier[tier] += (
                0 if revenue.value is None else revenue.value
            )
        else:
            revenue_totals_by_tier[tier] = 0 if revenue.value is None else revenue.value

    return revenue_totals_by_tier


def calculate_mpl_total_revenue_after_premium(
    product_type, hazard_tier_factors_table, revenue_totals_by_tier
):
    total_revenue_after_premium = 0
    revenue_premium_dict = {}
    if product_type != "MPL":
        return total_revenue_after_premium
    filtered_hazard_tiers_rows = hazard_tier_factors_table[
        hazard_tier_factors_table["product_type"] == product_type
    ]
    for key, value in revenue_totals_by_tier.items():
        previous_value = 0
        for row in filtered_hazard_tiers_rows.iloc[:].iterrows():
            revenue_band = row[1]["revenue_band"]
            tier = row[1]["tier"]
            factor = row[1]["factor"]

            if tier != key:
                continue

            if key not in revenue_premium_dict:
                revenue_premium_dict[key] = {}
            premium = (min(value, revenue_band) - previous_value) * factor / 1000
            revenue_premium_dict[key][f"{revenue_band}"] = premium
            total_revenue_after_premium += premium
            if revenue_band > value:
                break

            previous_value = revenue_band

    return total_revenue_after_premium


def calculate_mpl_eec_limit_factors(
    product_type, eec_liability_limits_table, revenue_totals_by_tier
):
    merged_tiers = {}
    total_revenue = sum(revenue_totals_by_tier.values())
    if product_type != "MPL" or total_revenue == 0:
        return merged_tiers

    eec_liability_limits = np.unique(
        eec_liability_limits_table[
            eec_liability_limits_table["product_type"] == product_type
        ]["limit"].values
    )

    for limit in eec_liability_limits:
        filtered_eec_liability_limits_rows = eec_liability_limits_table[
            (eec_liability_limits_table["product_type"] == product_type)
            & (eec_liability_limits_table["limit"] == limit)
        ]

        if len(filtered_eec_liability_limits_rows) == 0:
            continue
        else:
            for row in filtered_eec_liability_limits_rows.iterrows():
                tier = row[1]["tier"]
                factor = row[1]["limit_factor"]
                tier_revenue = (
                    0
                    if tier not in revenue_totals_by_tier
                    else revenue_totals_by_tier[tier]
                )
                if limit in merged_tiers:
                    merged_tiers[limit] += (tier_revenue / total_revenue) * factor
                else:
                    merged_tiers[limit] = (tier_revenue / total_revenue) * factor

    return merged_tiers


def calculate_written_contract_modifiers(
    written_contract_factors_table, written_contract, revenue_totals_by_tier
):
    written_contract_modifiers_by_tier = {}
    for key, *_ in revenue_totals_by_tier.items():
        written_contract_factors_rows = written_contract_factors_table[
            written_contract_factors_table["tier"] == key
        ]
        percentages_list = written_contract_factors_rows["percentage"].values
        factors_list = written_contract_factors_rows["factor"].values
        if (
            percentages_list is None
            or len(percentages_list) == 0
            or factors_list is None
            or len(factors_list) == 0
        ):
            continue
        written_contract_modifiers_by_tier[key] = np.interp(
            written_contract,
            percentages_list,
            factors_list,
        )

    return written_contract_modifiers_by_tier


def calculate_prof_exp_modifier(product_type, prof_exp_table, prof_exp):
    prof_exp_modifier = 1
    prof_exp_row = prof_exp_table[
        (prof_exp_table["product_type"] == product_type)
        & (prof_exp_table["years_of_experience"] == prof_exp)
    ]
    if prof_exp_row is not None and len(prof_exp_row) == 1:
        prof_exp_modifier = prof_exp_row["factor"].values[0]
    return prof_exp_modifier


def calculate_mpl_eec_limit_modifier(layer_limit, is_excess, eec_limit_factors):
    eec_limit_modifier = 1
    if not is_excess and layer_limit is not None and layer_limit in eec_limit_factors:
        eec_limit_modifier = eec_limit_factors[layer_limit]
    return eec_limit_modifier


def calculate_manutech(hxd, layer):
    product_type = hxd.cds.rating_factors.product_type
    if product_type == "Manutech":
        revenues = hxd.cds.rating_factors.revenues
        total_revenue = hxd.cds.exposure.aggregate.total_revenue
        input_underwriter_judgement = hxd.cds.modifiers.underwriter_judgement or 0
        hazard_tier_factors_table = hx.params.table_hazard_tiers_factors
        revenue_types_factors_table = hx.params.table_revenue_types_factors
        revenue_bands_table = hx.params.table_input_revenue_bands
        deductible_table = hx.params.table_input_coverage_deductible
        retroactive_years_table = hx.params.table_input_retroactive_years
        loss_experience_table = hx.params.table_input_loss_experience
        eec_liability_limits_table = hx.params.table_liability_EEC_factors
        liability_agg_eec_ratio_table = hx.params.table_liability_agg_eec_ratio
        excess_factors_table = hx.params.table_excess_factors
        defence_outside_limits_table = (
            hx.params.table_input_coverage_defence_outside_limits
        )

        is_excess = hxd.non_cds.rating_summary.is_excess

        tier_type_revenue = calculate_tier_type_revenues(
            product_type,
            hazard_tier_factors_table,
            revenue_types_factors_table,
            revenues,
            total_revenue,
        )

        revenue_band = calculate_revenue_band(
            product_type, revenue_bands_table, tier_type_revenue, total_revenue
        )

        layer_deductible = layer.deductible or 0
        deductible_modifier = calculate_deductible_modifier(
            product_type, deductible_table, layer_deductible
        )

        deductible = deductible_modifier * revenue_band

        input_retroactive_years = hxd.cds.rating_factors.retroactive_years or ""

        prior_acts_modifier = calculate_prior_acts_modifier(
            product_type, retroactive_years_table, input_retroactive_years
        )

        prior_acts = deductible * prior_acts_modifier

        exposure_loss_experience = hxd.cds.rating_factors.loss_experience or ""
        loss_experience_modifier = calculate_loss_experience_modifier(
            product_type, loss_experience_table, exposure_loss_experience
        )

        loss_experience = prior_acts * loss_experience_modifier

        layer_limit = layer.limit or 0
        layer_agg_limit = layer.aggregate_limit or 0
        min_premium_factor = calculate_minimum_premium_factor(
            product_type, eec_liability_limits_table, layer_limit
        )
        eec_limit_modifier = calculate_eec_limit_modifier(
            product_type, eec_liability_limits_table, layer_limit, is_excess
        )
        eec_limit = loss_experience * eec_limit_modifier

        agg_limit = calculate_aggregate_limit(
            product_type,
            liability_agg_eec_ratio_table,
            layer_agg_limit,
            layer_limit,
            eec_limit,
        )

        layer_excess = layer.excess or 0
        excess_modifier = calculate_excess_modifier(
            excess_factors_table, layer_excess, is_excess
        )

        excess = agg_limit * excess_modifier

        layer_defence_outside_limits = layer.defence_outside_limits.limit or 0
        defence_outside_limits_modifier = calculate_defence_outside_limits_modifier(
            product_type, defence_outside_limits_table, layer_defence_outside_limits
        )
        defence_outside_limits = excess + (
            defence_outside_limits_modifier * loss_experience * 0.92
        )

        cat_load = defence_outside_limits

        underwriter_judgement_factor = 1 + input_underwriter_judgement

        underwriter_judgement = cat_load * underwriter_judgement_factor

        layer_brokerage = layer.brokerage or 0
        brokerage = calculate_brokerage(
            product_type, layer_brokerage, underwriter_judgement
        )

        min_premium = 0 if min_premium_factor is None else (min_premium_factor * 5000)

        product_brokerage_base_price = brokerage_base_price[product_type]

        calculated_price = brokerage * (1 - product_brokerage_base_price)
        return (calculated_price, underwriter_judgement_factor, min_premium)


def calculate_products(hxd, layer):
    product_type = hxd.cds.rating_factors.product_type
    if product_type == "Products":
        revenues = hxd.cds.rating_factors.revenues
        total_revenue = hxd.cds.exposure.aggregate.total_revenue
        input_underwriter_judgement = (
            0
            if hxd.cds.modifiers.underwriter_judgement is None
            else hxd.cds.modifiers.underwriter_judgement
        )
        hazard_tier_factors_table = hx.params.table_hazard_tiers_factors
        revenue_types_factors_table = hx.params.table_revenue_types_factors
        revenue_bands_table = hx.params.table_input_revenue_bands
        deductible_table = hx.params.table_input_coverage_deductible
        retroactive_years_table = hx.params.table_input_retroactive_years
        loss_experience_table = hx.params.table_input_loss_experience
        eec_liability_limits_table = hx.params.table_liability_EEC_factors
        tier_9_min_premium_factors_table = (
            hx.params.table_products_tier_9_min_premium_factors
        )
        min_premium_factors_table = hx.params.table_products_min_premium_factor
        excess_factors_table = hx.params.table_excess_factors
        defence_outside_limits_table = (
            hx.params.table_input_coverage_defence_outside_limits
        )

        is_excess = hxd.non_cds.rating_summary.is_excess

        tier_type_revenue = calculate_tier_type_revenues(
            product_type,
            hazard_tier_factors_table,
            revenue_types_factors_table,
            revenues,
            total_revenue,
        )

        revenue_band = calculate_revenue_band(
            product_type, revenue_bands_table, tier_type_revenue, total_revenue
        )

        layer_deductible = layer.deductible or 0
        deductible_modifier = calculate_deductible_modifier(
            product_type, deductible_table, layer_deductible
        )

        deductible = deductible_modifier * revenue_band

        input_retroactive_years = hxd.cds.rating_factors.retroactive_years or ""

        prior_acts_modifier = calculate_prior_acts_modifier(
            product_type, retroactive_years_table, input_retroactive_years
        )

        prior_acts = deductible * prior_acts_modifier

        exposure_loss_experience = hxd.cds.rating_factors.loss_experience or ""
        loss_experience_modifier = calculate_loss_experience_modifier(
            product_type, loss_experience_table, exposure_loss_experience
        )

        loss_experience = prior_acts * loss_experience_modifier

        layer_eec_limit = layer.limit or 0
        eec_liability_limits_table
        eec_liability_limits_rows = eec_liability_limits_table[
            (eec_liability_limits_table["product_type"] == product_type)
        ]
        eec_ilf = np.interp(
            layer_eec_limit,
            eec_liability_limits_rows["limit"].values,
            eec_liability_limits_rows["limit_factor"].values,
        )

        layer_agg_limit = layer.aggregate_limit or 0
        liability_ilf = np.interp(
            layer_agg_limit,
            eec_liability_limits_rows["limit"].values,
            eec_liability_limits_rows["limit_factor"].values,
        )

        layer_product_limit = layer.product_liability_limits_AGG or 0
        agg_ilf = np.interp(
            layer_product_limit,
            eec_liability_limits_rows["limit"].values,
            eec_liability_limits_rows["limit_factor"].values,
        )

        agg_reinstatement_ilf = 0.7 * (agg_ilf - eec_ilf) + eec_ilf
        products_ilf = 0.9 * (liability_ilf - eec_ilf) + eec_ilf
        total_ilf = (agg_reinstatement_ilf + products_ilf) / 2
        limit = total_ilf * loss_experience

        layer_excess = layer.excess or 0
        excess_modifier = calculate_excess_modifier(
            excess_factors_table, layer_excess, is_excess
        )

        excess = limit * excess_modifier

        layer_defence_outside_limits = layer.defence_outside_limits.limit or 0
        defence_outside_limits_modifier = calculate_defence_outside_limits_modifier(
            product_type, defence_outside_limits_table, layer_defence_outside_limits
        )
        defence_outside_limits = excess + (
            defence_outside_limits_modifier * loss_experience * 0.92
        )

        cat_load = defence_outside_limits

        underwriter_judgement_factor = 1 + input_underwriter_judgement

        underwriter_judgement = cat_load * underwriter_judgement_factor

        layer_brokerage = layer.brokerage or 0
        brokerage = calculate_brokerage(
            product_type, layer_brokerage, underwriter_judgement
        )

        is_tier_9 = False
        tier_9_factor = 0
        retroactive_years_factor = 0
        minimum_premiums_factor = 0

        layer_personal_advertising = (
            0
            if layer.personal_advertising_liability_EEC.limit is None
            else layer.personal_advertising_liability_EEC.limit
        )
        max_tier = 0
        for revenue in revenues:
            tier = 0 if revenue.hazard_tier.tier is None else revenue.hazard_tier.tier
            if tier == 9:
                is_tier_9 = True
            max_tier = max(max_tier, tier)
        if is_tier_9:
            tier_9_factor = tier_9_min_premium_factors_table[
                (tier_9_min_premium_factors_table["limit_eec"] == layer_eec_limit)
                & (tier_9_min_premium_factors_table["limit_agg"] == layer_agg_limit)
                & (
                    tier_9_min_premium_factors_table["limit_general_liability"]
                    == layer_product_limit
                )
                & (
                    tier_9_min_premium_factors_table["limit_personal_advertising"]
                    == layer_personal_advertising
                )
            ]["min_premium_factor"].values[0]

        if input_retroactive_years != "RDI":
            retroactive_years_factor = 4000

        minimum_premiums_factor_rows = min_premium_factors_table[
            (min_premium_factors_table["limit"] == layer_eec_limit)
            & (min_premium_factors_table["tier"] == max_tier)
        ]

        minimum_premiums_factor = (
            1
            if minimum_premiums_factor_rows is None
            or len(minimum_premiums_factor_rows) == 0
            else minimum_premiums_factor_rows["factor"].values[0]
        )

        min_premium = max(
            tier_9_factor, retroactive_years_factor, minimum_premiums_factor
        )

        product_brokerage_base_price = brokerage_base_price[product_type]

        calculated_price = brokerage * (1 - product_brokerage_base_price)
        return (calculated_price, underwriter_judgement_factor, min_premium)


def calculate_tech(hxd, layer):
    product_type = hxd.cds.rating_factors.product_type
    if product_type == "Tech":
        revenues = hxd.cds.rating_factors.revenues
        total_revenue = hxd.cds.exposure.aggregate.total_revenue or 0
        input_underwriter_judgement = hxd.cds.modifiers.underwriter_judgement or 0
        hazard_tier_factors_table = hx.params.table_hazard_tiers_factors
        revenue_types_factors_table = hx.params.table_revenue_types_factors
        revenue_bands_table = hx.params.table_input_revenue_bands
        deductible_table = hx.params.table_input_coverage_deductible
        retroactive_years_table = hx.params.table_input_retroactive_years
        longevity_table = hx.params.table_input_longevity
        loss_experience_table = hx.params.table_input_loss_experience
        eec_liability_limits_table = hx.params.table_liability_EEC_factors
        liability_agg_eec_ratio_table = hx.params.table_liability_agg_eec_ratio
        excess_factors_table = hx.params.table_excess_factors
        defence_outside_limits_table = (
            hx.params.table_input_coverage_defence_outside_limits
        )

        is_excess = hxd.non_cds.rating_summary.is_excess

        tier_type_revenue = calculate_tier_type_revenues(
            product_type,
            hazard_tier_factors_table,
            revenue_types_factors_table,
            revenues,
            total_revenue,
        )

        revenue_band = calculate_revenue_band(
            product_type, revenue_bands_table, tier_type_revenue, total_revenue
        )

        layer_deductible = layer.deductible or 0
        deductible_modifier = calculate_deductible_modifier(
            product_type, deductible_table, layer_deductible
        )

        deductible = deductible_modifier * revenue_band

        layer_eec_limit = layer.limit or 0
        layer_agg_limit = layer.aggregate_limit or 0
        min_premium_factor = calculate_minimum_premium_factor(
            product_type, eec_liability_limits_table, layer_eec_limit
        )
        eec_limit_modifier = calculate_eec_limit_modifier(
            product_type, eec_liability_limits_table, layer_eec_limit, is_excess
        )
        eec_limit = deductible * eec_limit_modifier

        agg_limit = calculate_aggregate_limit(
            product_type,
            liability_agg_eec_ratio_table,
            layer_agg_limit,
            layer_eec_limit,
            eec_limit,
        )

        layer_excess = layer.excess or 0
        excess_modifier = calculate_excess_modifier(
            excess_factors_table, layer_excess, is_excess
        )

        excess = agg_limit * excess_modifier

        input_retroactive_years = hxd.cds.rating_factors.retroactive_years or ""

        prior_acts_modifier = calculate_prior_acts_modifier(
            product_type, retroactive_years_table, input_retroactive_years
        )

        prior_acts = excess * prior_acts_modifier

        layer_longevity = hxd.cds.rating_factors.longevity.years or ""
        longevity_modifier = calculate_longevity_modifier(
            product_type, longevity_table, layer_longevity
        )

        longevity = prior_acts * longevity_modifier

        exposure_loss_experience = hxd.cds.rating_factors.loss_experience or ""
        loss_experience_modifier = calculate_loss_experience_modifier(
            product_type, loss_experience_table, exposure_loss_experience
        )

        loss_experience = longevity * loss_experience_modifier

        layer_defence_outside_limits = layer.defence_outside_limits.limit or 0
        defence_outside_limits_modifier = calculate_defence_outside_limits_modifier(
            product_type, defence_outside_limits_table, layer_defence_outside_limits
        )

        defence_outside_limits = defence_outside_limits_modifier * loss_experience

        coverage_media_advertising = (
            (defence_outside_limits * coverage_media_advertising_factor)
            + defence_outside_limits
            if hxd.cds.rating_factors.tech.media_and_advertising
            else defence_outside_limits
        )

        cont_bi_pd = (
            (defence_outside_limits * cont_bi_pd_factor) + coverage_media_advertising
            if hxd.cds.rating_factors.tech.cont_bi_pd
            else coverage_media_advertising
        )

        first_party_privacy = (
            (defence_outside_limits * first_party_privacy_factor) + cont_bi_pd
            if hxd.cds.rating_factors.tech.first_party_privacy
            else cont_bi_pd
        )

        cyber_extortion_only = (
            (defence_outside_limits * cyber_extortion_only_factor) + first_party_privacy
            if hxd.cds.rating_factors.tech.cyber_extortion_only
            else first_party_privacy
        )

        general_liabilty = (
            (defence_outside_limits * general_liability_tech_factor)
            + cyber_extortion_only
            if hxd.cds.rating_factors.general_liability.value
            else cyber_extortion_only
        )

        cat_load = general_liabilty

        underwriter_judgement_factor = 1 + input_underwriter_judgement

        underwriter_judgement = cat_load * underwriter_judgement_factor

        layer_brokerage = layer.brokerage or 0
        brokerage = calculate_brokerage(
            product_type, layer_brokerage, underwriter_judgement
        )
        min_premium = min_premium_factor or 0

        product_brokerage_base_price = brokerage_base_price[product_type]

        calculated_price = brokerage * (1 - product_brokerage_base_price)
        return (calculated_price, underwriter_judgement_factor, min_premium)


def calculate_med_mal(hxd, layer):
    product_type = hxd.cds.rating_factors.product_type
    if product_type == "Med Mal":
        revenue_bands_table = hx.params.table_input_revenue_bands
        opv_band_table = hx.params.table_med_mal_opv_band
        allied_medical_table = hx.params.table_allied_medical
        social_services_table = hx.params.table_input_social_services
        deductible_table = hx.params.table_input_coverage_deductible
        retroactive_years_table = hx.params.table_input_retroactive_years
        loss_experience_table = hx.params.table_input_loss_experience
        eec_liability_limits_table = hx.params.table_liability_EEC_factors
        liability_agg_eec_ratio_table = hx.params.table_liability_agg_eec_ratio
        excess_factors_table = hx.params.table_excess_factors
        premium_table = hx.params.table_minimum_premium

        is_excess = hxd.non_cds.rating_summary.is_excess
        input_underwriter_judgement = hxd.cds.modifiers.underwriter_judgement or 0
        allied_medical = hxd.cds.rating_factors.med_mal.allied_medical
        social_services = hxd.cds.rating_factors.med_mal.social_services
        allied_medical_exposure = allied_medical.exposure_measure or 0
        social_services_exposure = social_services.exposure_measure or 0

        allied_medical_type = allied_medical.exposure_type

        allied_medical_exposure_factor = 1

        if allied_medical_type == "OPV's":
            allied_medical_exposure_factor = opv_band_table[
                opv_band_table["lower_band"] <= allied_medical_exposure
            ]["factor"].values.max()
        elif allied_medical_type == "Receipts":
            allied_medical_exposure_factor = revenue_bands_table[
                revenue_bands_table["band"]
                <= allied_medical_exposure & revenue_bands_table["product"]
                == product_type
            ]["factor"].values.max()

        allied_medical_rows = (
            []
            if allied_medical.allied_medical_type is None
            else allied_medical_table[
                allied_medical_table["allied_medical"].values
                == allied_medical.allied_medical_type
            ]
        )

        allied_medical_factor = (
            0
            if len(allied_medical_rows) == 0
            else allied_medical_rows["exposure_factor"].values[0]
        )

        social_services_rows = (
            []
            if social_services.social_services_type is None
            else social_services_table[
                social_services_table["social_services"]
                == social_services.social_services_type
            ]
        )
        social_services_factor = (
            0
            if len(social_services_rows) == 0
            else social_services_rows["exposure_factor"].values[0]
        )

        allied_medical_premium = (
            allied_medical_exposure
            * allied_medical_exposure_factor
            * allied_medical_factor
        )

        social_services_premium = social_services_exposure * social_services_factor

        base_premium = max(social_services_premium, allied_medical_premium)

        layer_eec_limit = layer.limit or 0
        layer_agg_limit = layer.aggregate_limit or 0
        min_premium_factor = calculate_minimum_premium_factor(
            product_type, eec_liability_limits_table, layer_eec_limit
        )
        eec_limit_modifier = calculate_eec_limit_modifier(
            product_type, eec_liability_limits_table, layer_eec_limit, is_excess
        )
        eec_limit = base_premium * eec_limit_modifier

        agg_limit = calculate_aggregate_limit(
            product_type,
            liability_agg_eec_ratio_table,
            layer_agg_limit,
            layer_eec_limit,
            eec_limit,
        )

        layer_excess = layer.excess or 0
        excess_modifier = calculate_excess_modifier(
            excess_factors_table, layer_excess, is_excess
        )

        excess = agg_limit * excess_modifier

        input_retroactive_years = hxd.cds.rating_factors.retroactive_years or ""
        prior_acts_modifier = calculate_prior_acts_modifier(
            product_type, retroactive_years_table, input_retroactive_years
        )
        prior_acts = excess * prior_acts_modifier

        layer_deductible = layer.deductible or 0
        deductible_modifier = calculate_deductible_modifier(
            product_type, deductible_table, layer_deductible
        )

        deductible = deductible_modifier * prior_acts

        cat_load = deductible

        total_credit_debit = hxd.cds.rating_factors.med_mal.total_credit_or_debit
        total_credit_debit_specials = 0

        input_loss_experience = hxd.cds.rating_factors.loss_experience or ""
        if total_credit_debit < -0.25:
            total_credit_debit_specials = 0.75 * cat_load
        else:
            loss_experience_rows = loss_experience_table[
                (loss_experience_table["product"] == product_type)
                & (
                    loss_experience_table["number_of_claims_in_years"]
                    == input_loss_experience
                )
            ]
            loss_experience_factor = (
                0
                if len(loss_experience_rows) == 0
                else loss_experience_rows["factor"].values[0]
            )
            total_credit_debit_specials = (
                1 + loss_experience_factor + total_credit_debit
            ) * cat_load

        layer_brokerage = layer.brokerage or 0
        brokerage = calculate_brokerage(
            product_type, layer_brokerage, total_credit_debit_specials
        )

        total_endorsements = hxd.cds.rating_factors.med_mal.total_endorsement
        endorsements = (1 + total_endorsements) * brokerage

        min_premium_rows = premium_table[
            (premium_table["product_type"] == product_type)
            & (premium_table["limit"] == layer_eec_limit)
        ]
        min_premium_factor = (
            0
            if ((min_premium_rows is None) or (len(min_premium_rows) == 0))
            else min_premium_rows["premium"].values[0]
        )

        min_premium = (1 + total_endorsements) * min_premium_factor

        underwriter_judgement_factor = 1 + input_underwriter_judgement

        product_brokerage_base_price = brokerage_base_price[product_type]

        calculated_price = endorsements * (1 - product_brokerage_base_price)
        return (calculated_price, underwriter_judgement_factor, min_premium)


def calculate_staffing(hxd, layer):
    product_type = hxd.cds.rating_factors.product_type
    if product_type == "Staffing":
        revenues = hxd.cds.rating_factors.revenues
        total_revenue = hxd.cds.exposure.aggregate.total_revenue or 0
        input_underwriter_judgement = hxd.cds.modifiers.underwriter_judgement or 0
        hazard_tier_factors_table = hx.params.table_hazard_tiers_factors
        deductible_ratio_table = hx.params.table_deductible_ratio
        retroactive_years_table = hx.params.table_input_retroactive_years
        loss_experience_table = hx.params.table_input_loss_experience
        eec_liability_limits_table = hx.params.table_liability_EEC_factors
        liability_agg_eec_ratio_table = hx.params.table_liability_agg_eec_ratio
        excess_factors_table = hx.params.table_excess_factors
        states_factors_table = hx.params.table_input_states
        min_premium_factors_table = hx.params.table_staffing_min_premium_factors

        tiers = list(set(hazard_tier_factors_table["tier"]))

        is_excess = hxd.non_cds.rating_summary.is_excess

        staffing = hxd.cds.rating_factors.staffing
        permanent_staffing_premium, temporary_staffing_premium, peo_staffing_premium = (
            calculate_staffing_premiums(product_type, total_revenue, staffing)
        )

        base_premium = (
            permanent_staffing_premium
            + temporary_staffing_premium
            + peo_staffing_premium
        )

        tier_discount = calculate_staffing_tier_discount(
            product_type, hazard_tier_factors_table, revenues, total_revenue
        )

        premium_after_discount = base_premium * (1 + tier_discount)

        tiers_calculations = {}
        for tier in tiers:
            tiers_calculations[tier] = {"revenue": 0, "eec": 0, "agg": 0}

        for revenue in revenues:
            if revenue.hazard_tier is not None and revenue.hazard_tier.tier is not None:
                tier = revenue.hazard_tier.tier
                if tier in tiers_calculations:
                    tiers_calculations[tier]["revenue"] += (
                        0 if revenue.value is None else revenue.value
                    )

        if total_revenue != 0:
            for tier in tiers_calculations:
                tiers_calculations[tier]["revenue"] = (
                    premium_after_discount
                    * tiers_calculations[tier]["revenue"]
                    / total_revenue
                )

        layer_limit = layer.limit or 0
        layer_agg_limit = layer.aggregate_limit or 0
        eec_limit_modifier = calculate_eec_limit_modifier(
            product_type, eec_liability_limits_table, layer_limit, is_excess
        )

        agg_limit_modifier = calculate_staffing_agg_limit_modifier(
            product_type,
            liability_agg_eec_ratio_table,
            layer_agg_limit,
            layer_limit,
        )
        total_agg_limit = 0
        for key, *_ in tiers_calculations.items():
            tiers_calculations[key]["eec"] = (
                eec_limit_modifier * tiers_calculations[key]["revenue"]
            )
            tiers_calculations[key]["agg"] = (
                agg_limit_modifier * tiers_calculations[key]["eec"]
            )
            total_agg_limit += tiers_calculations[key]["agg"]

        layer_excess = 0 if layer.excess is None else layer.excess
        excess_modifier = calculate_excess_modifier(
            excess_factors_table, layer_excess, is_excess
        )

        excess = total_agg_limit * excess_modifier

        layer_deductible = 0 if layer.deductible is None else layer.deductible
        deductible_modifier = calculate_staffing_deductible_modifier(
            product_type, deductible_ratio_table, layer_deductible
        )

        deductible = excess * deductible_modifier

        state = hxd.cds.standard_fields.insured_state_or_province
        state_modifier = calculate_staffing_state_modifier(states_factors_table, state)

        state_factor = state_modifier * deductible

        exposure_loss_experience = hxd.cds.rating_factors.loss_experience or ""
        loss_experience_modifier = calculate_loss_experience_modifier(
            product_type, loss_experience_table, exposure_loss_experience
        )

        loss_experience = state_factor * loss_experience_modifier

        input_retroactive_years = hxd.cds.rating_factors.retroactive_years or ""
        prior_acts_modifier = calculate_prior_acts_modifier(
            product_type, retroactive_years_table, input_retroactive_years
        )
        prior_acts = loss_experience * prior_acts_modifier

        is_general_liability = hxd.cds.rating_factors.general_liability.value
        general_liability = (
            prior_acts * general_liability_staffing_factor
            if is_general_liability
            else prior_acts
        )

        cat_load = general_liability

        underwriter_judgement_factor = 1 + input_underwriter_judgement

        underwriter_judgement = cat_load * underwriter_judgement_factor

        layer_brokerage = layer.brokerage or 0
        brokerage = calculate_brokerage(
            product_type, layer_brokerage, underwriter_judgement
        )

        min_premium_factors_table
        min_premium_modifier = calculate_staffing_min_premium_modifier(
            min_premium_factors_table,
            layer.limit,
            layer.aggregate_limit,
            permanent_staffing_premium,
            temporary_staffing_premium,
            peo_staffing_premium,
        )
        min_premium = (
            0
            if (layer_brokerage * min_premium_modifier / 0.275) == 1000000
            else min_premium_modifier
        )

        underwriter_judgement_factor = 1 + input_underwriter_judgement

        product_brokerage_base_price = brokerage_base_price[product_type]

        calculated_price = brokerage * (1 - product_brokerage_base_price)
        return (calculated_price, underwriter_judgement_factor, min_premium)


def calculate_mpl(hxd, layer):
    product_type = hxd.cds.rating_factors.product_type
    if product_type == "MPL":
        guideline_deductible_factor = 0.002
        guideline_base = 2500
        revenues = hxd.cds.rating_factors.revenues
        total_revenue = (
            0
            if hxd.cds.exposure.aggregate.total_revenue is None
            else hxd.cds.exposure.aggregate.total_revenue
        )
        input_underwriter_judgement = hxd.cds.modifiers.underwriter_judgement or 0
        hazard_tier_factors_table = hx.params.table_hazard_tiers_factors
        written_contract_factors_table = hx.params.table_mpl_written_contract_factors
        prof_exp_table = hx.params.table_input_professional_experience
        client_revenue_table = hx.params.table_input_mpl_client_revenue
        deductible_ratio_table = hx.params.table_deductible_ratio
        retroactive_years_table = hx.params.table_input_retroactive_years
        longevity_table = hx.params.table_input_longevity
        loss_experience_table = hx.params.table_input_loss_experience
        eec_liability_limits_table = hx.params.table_liability_EEC_factors
        liability_agg_eec_ratio_table = hx.params.table_liability_agg_eec_ratio
        excess_factors_table = hx.params.table_excess_factors

        is_excess = hxd.non_cds.rating_summary.is_excess

        revenues_total_by_tier = calculate_revenue_totals_by_tier(revenues)

        total_revenue_after_premium = calculate_mpl_total_revenue_after_premium(
            product_type, hazard_tier_factors_table, revenues_total_by_tier
        )

        guideline_deducitble = max(
            total_revenue * guideline_deductible_factor, guideline_base
        )

        eec_limit_factors = calculate_mpl_eec_limit_factors(
            product_type, eec_liability_limits_table, revenues_total_by_tier
        )

        input_written_contract = (
            0
            if hxd.cds.rating_factors.business_with_written_contract.percentage is None
            else hxd.cds.rating_factors.business_with_written_contract.percentage
        )
        written_contract_modifiers = calculate_written_contract_modifiers(
            written_contract_factors_table,
            input_written_contract,
            revenues_total_by_tier,
        )

        input_loss_experience = (
            0
            if hxd.cds.rating_factors.loss_experience is None
            else hxd.cds.rating_factors.loss_experience
        )
        loss_experience_modifier = calculate_loss_experience_modifier(
            product_type, loss_experience_table, input_loss_experience
        )

        loss_experience = loss_experience_modifier * total_revenue_after_premium

        input_prof_exp = (
            0
            if hxd.cds.rating_factors.professional_experience.years is None
            else hxd.cds.rating_factors.professional_experience.years
        )
        prof_exp_modifier = calculate_prof_exp_modifier(
            product_type, prof_exp_table, input_prof_exp
        )
        prof_exp = prof_exp_modifier * loss_experience

        input_longevity = hxd.cds.rating_factors.longevity.years or ""
        longevity_modifier = calculate_longevity_modifier(
            product_type, longevity_table, input_longevity
        )
        longevity = longevity_modifier * prof_exp

        written_contract_modifier = 0
        if total_revenue > 0:
            for key, value in revenues_total_by_tier.items():
                if key is None:
                    continue
                written_contract_modifier += (
                    value
                    * (
                        0
                        if (
                            key not in written_contract_modifiers
                            or written_contract_modifiers[key] is None
                        )
                        else written_contract_modifiers[key]
                    )
                ) / total_revenue

        written_contract = written_contract_modifier * longevity

        input_client_revenue = (
            0
            if hxd.cds.rating_factors.business_with_written_contract.revenue is None
            else hxd.cds.rating_factors.business_with_written_contract.revenue
        )
        client_revenue_modifier_rows = client_revenue_table[
            client_revenue_table["average_revenue"] == input_client_revenue
        ]["factor"].values

        client_revenue_modifier = 0
        if len(client_revenue_modifier_rows) == 1:
            client_revenue_modifier = client_revenue_modifier_rows[0]

        client_revenue = written_contract * client_revenue_modifier

        retroactive_years = hxd.cds.rating_factors.retroactive_years
        prior_acts_modifier = calculate_prior_acts_modifier(
            product_type, retroactive_years_table, retroactive_years
        )
        prior_acts = client_revenue * prior_acts_modifier

        layer_deductible = 0 if layer.deductible is None else layer.deductible
        deductible_modifier = calculate_mpl_deductible_modifier(
            product_type, deductible_ratio_table, layer_deductible, guideline_deducitble
        )
        deductible = prior_acts * deductible_modifier

        layer_limit = 0 if layer.limit is None else layer.limit
        eec_limit_modifier = calculate_mpl_eec_limit_modifier(
            layer_limit, is_excess, eec_limit_factors
        )
        eec_limit = deductible * eec_limit_modifier

        layer_agg_limit = 0 if layer.aggregate_limit is None else layer.aggregate_limit
        agg_limit_modifier = calculate_mpl_agg_limit_modifier(
            product_type,
            liability_agg_eec_ratio_table,
            layer_agg_limit,
            layer_limit,
        )
        total_agg_limit = agg_limit_modifier * eec_limit

        layer_excess = 0 if layer.excess is None else layer.excess
        excess_modifier = calculate_excess_modifier(
            excess_factors_table, layer_excess, is_excess
        )
        excess = total_agg_limit * excess_modifier

        cat_load = excess

        underwriter_judgement_factor = 1 + input_underwriter_judgement

        underwriter_judgement = cat_load * underwriter_judgement_factor

        layer_brokerage = layer.brokerage or 0
        brokerage = calculate_brokerage(
            product_type, layer_brokerage, underwriter_judgement
        )

        min_premium_factor = calculate_minimum_premium_factor(
            product_type, eec_liability_limits_table, layer_limit
        )

        min_premium = min_premium_factor or 0

        underwriter_judgement_factor = 1 + input_underwriter_judgement

        product_brokerage_base_price = brokerage_base_price[product_type]

        calculated_price = brokerage * (1 - product_brokerage_base_price)
        return (calculated_price, underwriter_judgement_factor, min_premium)


def rate_rating_summary(hxd):
    bound_count = 0

    product_type = hxd.cds.rating_factors.product_type
    init_tech_options(hxd)
    hxd.cds.standard_fields.is_case_priced = (
        hxd.cds.standard_fields.rating_methodology == "Case Priced"
    )
    hxd.cds.standard_fields.is_rater_priced = (
        hxd.cds.standard_fields.rating_methodology == "Rater"
    )    

    layers = hxd.cds.layers
    is_rater_priced = hxd.cds.standard_fields.is_rater_priced
    for layer in layers:
        init_layers(hxd, layer, product_type, is_rater_priced)
        if layer.status in bound_statuses():
            bound_count += 1

    hxd.non_cds.rating_factors.show = (
        hxd.cds.rating_factors.tech.show or hxd.cds.rating_factors.general_liability.show
    )
    
    if bound_count == 0:
        hx.errors.validation(
            "Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final"
        )
    elif bound_count > 1:
        hx.errors.validation("There must be only one bound policy")
