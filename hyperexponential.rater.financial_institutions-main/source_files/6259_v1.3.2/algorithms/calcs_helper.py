import math
import operator

import hx
import numpy as np
import pandas as pd
from datetime import datetime

from algorithms import parameter_tables_schema as params
from algorithms.rate_constants import do_sides, max_layers, max_towers
from algorithms.rate_risk_information import (
    get_coverage_matrix,
    get_industry_matrix,
    get_sub_industry_matrix,
)
from algorithms.rate_utilities import (
    get_field_options,
    look_up,
    ratio,
    rgetattr,
    rsetattr,
)


def global_parameters(hxd):
    table_ccy_authorities = hx.params.table_ccy_authorities

    cover_currency = hxd.cds.risk_info.currency
    exposure_currency = hxd.cds.rating_factors.exposure_details.currency

    coverage_matrix = get_coverage_matrix(hxd)
    industry_matrix = get_industry_matrix(hxd)
    subindustry_matrix = get_sub_industry_matrix(hxd)
    fx_live_cover = look_up(cover_currency, "ccy", "fx_rate", params.fx_rates.df())
    fx_live_expo = look_up(exposure_currency, "ccy", "fx_rate", params.fx_rates.df())
    fx_authorities = look_up(cover_currency, "ccy", "fx_rate", table_ccy_authorities)

    return {
        "coverage_matrix": coverage_matrix,
        "industry_matrix": industry_matrix,
        "subindustry_matrix": subindustry_matrix,
        "fx_live_cover": fx_live_cover,
        "fx_live_expo": fx_live_expo,
        "fx_authorities": fx_authorities,
    }


def get_selected_towers_per_coverage(hxd):
    selected_towers = {
        "crime": [None for _ in range(max_layers)],
        "pi": [None for _ in range(max_layers)],
        "A": [None for _ in range(max_layers)],
        "B": [None for _ in range(max_layers)],
        "C": [None for _ in range(max_layers)],
        "Dic": [None for _ in range(max_layers)],
    }

    # Coverages label map
    coverages_map = {
        "Crime": "crime",
        "PI": "pi",
        "D&O A": "A",
        "D&O AB": "B",
        "D&O ABC": "C",
        "D&O A Dic": "Dic",
    }

    # Loop over all towers and get coverages
    for i, layer in enumerate(hxd.cds.layers):
        for tower_idx in range(1, max_towers + 1):
            if getattr(hxd.non_cds.cover_details, f"tower_{tower_idx}_show"):
                tower = getattr(layer, f"tower_{tower_idx}")
                selected_coverage = (
                    tower.coverage.selected or tower.coverage.calculated
                ) or ""
                if selected_coverage == "":
                    continue
                selected_coverages = selected_coverage.split(" / ")
                for c in selected_coverages:
                    if c in coverages_map:
                        c_key = coverages_map.get(c)
                        if c_key:
                            selected_towers[c_key][i] = f"tower_{tower_idx}"

    return pd.DataFrame(selected_towers)


def get_towers_limits(layer, hxd):
    limits = []
    for i in range(1, max_towers + 1):
        if getattr(hxd.non_cds.cover_details, f"tower_{i}_show"):
            tower = getattr(layer, f"tower_{i}")
            if tower.limit is not None:
                limits.append(tower.limit)

    return limits


def get_policy_days_duration(hxd):
    start_date = hxd.hx_core.inception_date
    end_date = hxd.hx_core.expiry_date

    if start_date and end_date:
        delta = end_date - start_date
        return delta.days

    return None


def is_round_to_annual(hxd):
    round_to_annual = True

    policy_days = get_policy_days_duration(hxd)
    if policy_days:
        round_to_annual = 362 <= policy_days <= 368

    return round_to_annual


def calculate_excess(idx, layer, hxd):
    # Note: Primary layer is only for display, no calculations
    if idx > 0:
        for i in range(1, max_towers + 1):
            if getattr(hxd.non_cds.cover_details, f"tower_{i}_show"):
                tower_curr_layer = getattr(layer, f"tower_{i}")
                tower_prev_layer = getattr(hxd.cds.layers[idx - 1], f"tower_{i}")

                # 1st Excess layer
                if idx == 1:
                    tower_curr_layer.excess.calculated = (
                        tower_prev_layer.limit or 0 
                        if tower_curr_layer.limit
                        else 0
                    )
                # 2 - 16 Excess layer
                else:
                    tower_curr_layer.excess.calculated = (
                        (tower_prev_layer.limit or 0) + (tower_prev_layer.excess.selected or 0)
                        if tower_curr_layer.limit
                        else 0
                    )


def fill_excess_str(idx, layer, hxd):
    global_params = global_parameters(hxd)

    # Primary layer
    if idx == 0:
        for c in ("crime", "pi", "do"):
            if global_params["coverage_matrix"][f"is_{c}"]:
                towers = {
                    'all_manager': getattr(hxd.cds.rating_factors.cover_details.primary_layer.towers_all_manager, c),
                    'fund': getattr(hxd.cds.rating_factors.cover_details.primary_layer.towers_fund, c)
                }

                for k, v in towers.items():
                    if v != "NA":
                        tower_num = int(v[-1])  # i.e Tower 1
                        sir_value = rgetattr(hxd.cds.rating_factors.cover_details.primary_layer, f'sir_{k}.{c}')
                        if sir_value:
                            sir_value = f"{round(sir_value):,}"
                            tower = getattr(layer, f"tower_{tower_num}")
                            tower.excess_str = (
                                f"{tower.excess_str} / {sir_value}"
                                if tower.excess_str
                                else sir_value
                            )

    # Excess layer
    else:
        for i in range(1, max_towers + 1):
            if getattr(hxd.non_cds.cover_details, f"tower_{i}_show"):
                tower = getattr(layer, f"tower_{i}")
                if tower.excess.selected is not None:
                    tower.excess_str = f"{round(tower.excess.selected):,}"


def fill_excess_str_fx(idx, layer, hxd):
    global_params = global_parameters(hxd)

    # Primary layer
    if idx == 0:
        fx_rate = hxd.cds.rating_summary.authorities_fx.selected
        for c in ("crime", "pi", "do"):
            if global_params["coverage_matrix"][f"is_{c}"]:
                towers = {
                    'all_manager': getattr(hxd.cds.rating_factors.cover_details.primary_layer.towers_all_manager, c),
                    'fund': getattr(hxd.cds.rating_factors.cover_details.primary_layer.towers_fund, c)
                }

                for k, v in towers.items():
                    if v != "NA":
                        tower_num = int(v[-1])
                        sir_value = rgetattr(hxd.cds.rating_factors.cover_details.primary_layer, f'sir_{k}.{c}')
                        if sir_value:
                            sir_value = f"{np.round(ratio(sir_value, fx_rate)):,}"
                            tower = getattr(layer, f"tower_{tower_num}")
                            tower.excess_str_fx = (
                                f"{tower.excess_str_fx} / {sir_value}"
                                if tower.excess_str_fx
                                else sir_value
                            )

    # Excess layer
    else:
        for i in range(1, max_towers + 1):
            if getattr(hxd.non_cds.cover_details, f"tower_{i}_show"):
                tower = getattr(layer, f"tower_{i}")
                if tower.excess_fx:
                    tower.excess_str_fx = f"{round(tower.excess_fx):,}"


def calculate_net_premium(idx, layer, hxd):
    gross = layer.quoted_premium_pro_rata_100
    if gross:
        if hxd.non_cds.cover_details.is_brokerage_all_layers:
            factor = (
                1
                - (hxd.cds.rating_factors.cover_details.brokerage_all_layers.brk or 0)
                - (hxd.cds.rating_factors.cover_details.brokerage_all_layers.lta or 0)
            )
        else:
            factor = 1 - (layer.brokerage or 0) - (layer.lta or 0)

        layer.net_premium = gross * factor


def calculate_exposure(idx, layer, hxd):
    max_exposure = 0

    for i in range(1, max_towers + 1):
        if getattr(hxd.non_cds.cover_details, f"tower_{i}_show"):
            tower = getattr(layer, f"tower_{i}")
            exposure = (tower.limit or 0) * (tower.beazley_line or 0)
            max_exposure = max(max_exposure, exposure)

    if max_exposure:
        layer.exposure = max_exposure


def calculate_afb_net_premium(idx, layer, hxd, afb_net_premium):
    global_params = global_parameters(hxd)
    layer.afb_net_premium = (afb_net_premium or 0) * global_params["fx_live_cover"]


def calculate_net_rol(idx, layer, hxd):
    net_rol = 0
    if layer.net_premium:
        max_limit = max(get_towers_limits(layer, hxd), default=None)
        if max_limit:
            net_rol = layer.net_premium / max_limit

    if net_rol:
        layer.net_rol = net_rol


def calculate_actual_ilf(idx, layer, hxd):
    curr_net_rol = layer.net_rol
    prev_net_rol = hxd.cds.layers[idx - 1].net_rol if idx > 0 else layer.net_rol

    if curr_net_rol and prev_net_rol:
        layer.actual_ilf = curr_net_rol / prev_net_rol


def calculate_annualised_benchmark_premium(idx, layer, hxd, gross_premium):
    global_params = global_parameters(hxd)

    if sum(get_towers_limits(layer, hxd)):
        layer.benchmark_premium_annualised_100 = gross_premium * global_params["fx_live_cover"]


def calculate_pro_rated_benchmark_premium(idx, layer, hxd):
    if layer.benchmark_premium_annualised_100:
        benchmark_premium_pro_rata_100 = layer.benchmark_premium_annualised_100

        start_date = hxd.hx_core.inception_date
        policy_days = get_policy_days_duration(hxd)
        round_to_annual = is_round_to_annual(hxd)
        if policy_days and not round_to_annual:
            benchmark_premium_pro_rata_100 *= policy_days
            start_date = datetime.combine(start_date, datetime.min.time())
            next_date = (
                pd.to_datetime(start_date)
                + pd.DateOffset(years=1)
                - pd.DateOffset(days=1)
            )
            delta = next_date - start_date
            benchmark_premium_pro_rata_100 /= delta.days

        layer.benchmark_premium_pro_rata_100 = benchmark_premium_pro_rata_100


def calculate_bpi(idx, layer, hxd):
    gross_premium = layer.quoted_premium_pro_rata_100
    benchmark_premium_pro_rata_100 = layer.benchmark_premium_pro_rata_100

    if gross_premium and benchmark_premium_pro_rata_100:
        layer.bpi = ratio(gross_premium, benchmark_premium_pro_rata_100)
        layer.bpi_pre_uw_adj = layer.bpi * (1 + (hxd.cds.modifiers.risk_category.uw_adj or 0))
        layer.pflr = benchmark_premium_pro_rata_100 * 0.7 / gross_premium
        layer.pflr_pre_uw_adj = benchmark_premium_pro_rata_100 / (1 + (hxd.cds.modifiers.risk_category.uw_adj or 0)) * 0.7 / gross_premium


def calculate_losses_split(idx, layer, hxd, expected_loss_by_layer_by_coverage):
    global_params = global_parameters(hxd)
    expected_loss_total = (
        expected_loss_by_layer_by_coverage["crime"]["manager"]
        + expected_loss_by_layer_by_coverage["crime"]["fund"]
        + expected_loss_by_layer_by_coverage["pi"]["manager"]
        + expected_loss_by_layer_by_coverage["pi"]["fund"]
        + expected_loss_by_layer_by_coverage["do"]["manager"]
        + expected_loss_by_layer_by_coverage["do"]["fund"]
    )

    if expected_loss_total == 0:
        return

    if sum(get_towers_limits(layer, hxd)):
        for c in ("crime", "pi", "do"):
            if global_params["coverage_matrix"][f"is_{c}"]:
                coverage_total_loss = (
                    expected_loss_by_layer_by_coverage[c]["manager"]
                    + expected_loss_by_layer_by_coverage[c]["fund"]
                )
                losses_split = coverage_total_loss / expected_loss_total
                if losses_split and not math.isnan(losses_split):
                    rsetattr(layer.coverages, f"{c}.losses_split", losses_split)


def calculate_net_lol(idx, layer, hxd, brokerage, ncb, lta, zero_claims_ncb_calcs):
    net_lol = 0
    if layer.benchmark_premium_pro_rata_100:
        max_limit = max(get_towers_limits(layer, hxd))
        if max_limit:
            df = {
                "brk": brokerage,
                "ncb_claims": zero_claims_ncb_calcs,
                "ncb": ncb,
                "lta": lta,
            }

            multiplier = (
                layer.benchmark_premium_pro_rata_100
                * 0.7
                * (1 - df["brk"] - (df["ncb"] * df["ncb_claims"]) - df["lta"])
            )
            net_lol = ratio(multiplier, max_limit)

    if net_lol:
        layer.net_lol = net_lol


def calculate_model_ilf(idx, layer, hxd):
    curr_model_ilf = layer.net_lol
    prev_model_ilf = hxd.cds.layers[idx - 1].net_lol if idx > 0 else layer.net_lol

    if curr_model_ilf and prev_model_ilf:
        layer.model_ilf = curr_model_ilf / prev_model_ilf


def calculate_expected_loss_cost_att(idx, layer, hxd, att_percentage):
    if sum(get_towers_limits(layer, hxd)):
        if att_percentage:
            layer.expected_loss_cost_att = att_percentage


def calculate_expected_loss_cost_cat(idx, layer, hxd, cat_percentage):
    if sum(get_towers_limits(layer, hxd)):

        if cat_percentage:
            layer.expected_loss_cost_cat = cat_percentage


def calculate_pro_rated_expected_loss(idx, layer, hxd):
    
    expected_loss_cost = layer.expected_loss_cost_annualised
    if not expected_loss_cost:
        return

    start_date = hxd.hx_core.inception_date
    policy_days = get_policy_days_duration(hxd)
    round_to_annual = is_round_to_annual(hxd)
    if policy_days and not round_to_annual:
        expected_loss_cost *= policy_days
        start_date = datetime.combine(start_date, datetime.min.time())
        next_date = (
            pd.to_datetime(start_date)
            + pd.DateOffset(years=1)
            - pd.DateOffset(days=1)
        )
        delta = next_date - start_date
        expected_loss_cost /= delta.days

    layer.expected_loss_cost = expected_loss_cost


def calculate_annualised_technical_premium(idx, layer, hxd, afb_gross_tp):
    global_params = global_parameters(hxd)

    if sum(get_towers_limits(layer, hxd)):

        if afb_gross_tp:
            layer.technical_premium_net = afb_gross_tp * global_params["fx_live_cover"]


def calculate_pro_rated_technical_premium(idx, layer, hxd, afb_gross_tp_pre_uw_adj, tot_gross_tp_100):
    if layer.technical_premium_net:
        technical_premium = layer.technical_premium_net

        start_date = hxd.hx_core.inception_date
        policy_days = get_policy_days_duration(hxd)
        round_to_annual = is_round_to_annual(hxd)
        if policy_days and not round_to_annual:
            technical_premium *= policy_days
            start_date = datetime.combine(start_date, datetime.min.time())
            next_date = (
                pd.to_datetime(start_date)
                + pd.DateOffset(years=1)
                - pd.DateOffset(days=1)
            )
            delta = next_date - start_date
            technical_premium /= delta.days

        layer.technical_premium = technical_premium
    
    global_params = global_parameters(hxd)
    if layer.technical_premium_net:
        technical_premium_pre_uw_adj = afb_gross_tp_pre_uw_adj * global_params["fx_live_cover"]

        start_date = hxd.hx_core.inception_date
        policy_days = get_policy_days_duration(hxd)
        round_to_annual = is_round_to_annual(hxd)
        if policy_days and not round_to_annual:
            technical_premium_pre_uw_adj *= policy_days
            start_date = datetime.combine(start_date, datetime.min.time())
            next_date = (
                pd.to_datetime(start_date)
                + pd.DateOffset(years=1)
                - pd.DateOffset(days=1)
            )
            delta = next_date - start_date
            technical_premium_pre_uw_adj /= delta.days

        layer.technical_premium_pre_uw_adj = technical_premium_pre_uw_adj


    if layer.technical_premium_net:
        technical_premium_100 = tot_gross_tp_100 * global_params["fx_live_cover"]

        start_date = hxd.hx_core.inception_date
        policy_days = get_policy_days_duration(hxd)
        round_to_annual = is_round_to_annual(hxd)
        if policy_days and not round_to_annual:
            technical_premium_100 *= policy_days
            start_date = datetime.combine(start_date, datetime.min.time())
            next_date = (
                pd.to_datetime(start_date)
                + pd.DateOffset(years=1)
                - pd.DateOffset(days=1)
            )
            delta = next_date - start_date
            technical_premium_100 /= delta.days

        layer.technical_premium_100 = technical_premium_100


def calculate_tpi(idx, layer, hxd, afb_gross_premium):
    global_params = global_parameters(hxd)

    technical_premium = layer.technical_premium

    if technical_premium and afb_gross_premium:
        layer.tpi = ratio(
            afb_gross_premium * global_params["fx_live_cover"], technical_premium
        )

    technical_premium_pre_uw_adj = layer.technical_premium_pre_uw_adj

    if technical_premium_pre_uw_adj and afb_gross_premium:
        layer.tpi_pre_uw_adj = ratio(
            afb_gross_premium * global_params["fx_live_cover"], technical_premium_pre_uw_adj
        )

def calculate_initial_base_rate(hxd):
    initial_base_rate_values = {"crime": 0, "pi": 0, "do": 0}

    global_params = global_parameters(hxd)
    industry = hxd.cds.key_industry.code_name.lower() if hxd.cds.key_industry.code_name else hxd.cds.key_industry.code_name
    sub_industry = hxd.cds.rating_factors.risk_info.sub_industry.lower() if hxd.cds.rating_factors.risk_info.sub_industry else hxd.cds.rating_factors.risk_info.sub_industry
    is_public = hxd.cds.rating_factors.risk_info.ownership_type == "Public"    
    table_base_rates = hx.params.table_base_rates.query(
        f'industry.str.lower() == "{industry}" and sub_industry.str.lower() == "{sub_industry}"'
    )
    regions_list = (
        ("africa", "Africa"),
        ("arab_states", "Arab States"),
        ("asia", "Asia"),
        ("oceania", "Oceania"),
        ("europe", "Europe"),
        ("former_soviet_republics", "Former Soviet Republics"),
        ("usa", "USA"),
        ("canada", "Canada"),
        ("south_latin_america", "South/Latin America"),
        ("caribbean", "Caribbean"),
        ("row", "RoW"),
    )

    # Aggregate region base rates
    if not table_base_rates.empty:
        for entity, c in zip(
            ("employees", "revenues", "assets"), ("crime", "pi", "do")
        ):
            if global_params["coverage_matrix"][f"is_{c}"]:
                is_percent = (
                    getattr(hxd.cds.exposure.granular.regions.splits_entered_as, entity)
                    == "Percentage"
                )
                switch = "percent" if is_percent else "value"
                total_amount = (
                    1
                    if is_percent
                    else rgetattr(hxd.cds.exposure.aggregate.total_amounts, entity)
                )

                #Handle cases when the summation of table values is greater than insterted total amount
                if is_percent:
                    missing_percent = rgetattr(hxd.non_cds.exposure_details.regions.missing_amounts.percent, entity)
                    if missing_percent and (missing_percent != 0):
                        total_amount -= missing_percent                
                else:
                    missing_value = rgetattr(hxd.non_cds.exposure_details.regions.missing_amounts.value, entity)
                    if missing_value and (missing_value != 0):
                        total_amount -= missing_value        
                                                

                base_rates = table_base_rates.query(f'coverage == "{c}"')

                if not base_rates.empty:
                    for region_id, region_label in regions_list:
                        base_rate = base_rates.query(
                            f'region == "{region_label}"'
                        ).rate.item()
                        region_split = rgetattr(
                            hxd.cds.exposure.granular.regions.regions_list,
                            f"{region_id}.{switch}.{entity}",
                        )
                        region_split_ratio = ratio(region_split, total_amount)

                        initial_base_rate_values[c] += base_rate * region_split_ratio

        # Special handling for Public D&O
        if global_params["coverage_matrix"]["is_do"] and is_public:
            market_cap_us = 0
            if hxd.non_cds.exposure_details.market_cap_us_show:
                market_cap_us = hxd.cds.exposure.aggregate.market_cap_us or 0
            base_rate_us = table_base_rates.query('coverage == "do" and region == "USA"').rate.item() * market_cap_us

            region = hxd.cds.rating_factors.risk_info.region.lower() if hxd.cds.rating_factors.risk_info.region else hxd.cds.rating_factors.risk_info.region
            region_base_rate = 0
            region_query = table_base_rates.query(f'coverage == "do" and region.str.lower() == "{region}"')
            if not region_query.empty:
                region_expo = 1 - market_cap_us
                region_base_rate = region_query.rate.item() * region_expo

            public_ownership_base_rate = hx.params.table_ownership_do.query('ownership == "Public"').base_rate.item()

            initial_base_rate_values["do"] = (base_rate_us + region_base_rate) * public_ownership_base_rate

    return initial_base_rate_values


def calculate_size_factor(hxd):
    exposure_values = {"crime": None, "pi": None, "do": None}
    size_factor_values = {"crime": None, "pi": None, "do": None}

    global_params = global_parameters(hxd)
    is_public = hxd.cds.rating_factors.risk_info.ownership_type == "Public"
    table_aum = hx.params.table_aum_parameters
    table_mkfactor = hx.params.table_mk_factor_do
    table_size_factor = hx.params.table_size_factor
    industry = hxd.cds.key_industry.code_name.lower() if hxd.cds.key_industry.code_name else hxd.cds.key_industry.code_name

    ## Get exposure to use

    if global_params["coverage_matrix"]["is_crime"]:
        # value 1
        exposure_values["crime"] = hxd.cds.exposure.aggregate.total_amounts.employees

    if global_params["coverage_matrix"]["is_pi"]:
        # value 1
        exposure_values["pi"] = (
            hxd.cds.exposure.aggregate.total_amounts.revenues
            / global_params["fx_live_expo"]
        )
        # value 2
        if hxd.non_cds.exposure_details.total_aum_show:
            aum = (hxd.cds.exposure.aggregate.total_amounts.aum or 0) / global_params[
                "fx_live_expo"
            ]
            if aum and industry and (industry == "investment managers"):
                conversion_factor = table_aum.query(
                    'coverage == "pi" and category == "conversion factor"'
                ).parameter.item()
                weight_aum = table_aum.query(
                    'coverage == "pi" and category == "weight to aum"'
                ).parameter.item()
                exposure_values["pi"] = (
                    conversion_factor * aum * weight_aum
                    + (1 - weight_aum) * exposure_values["pi"]
                )
        exposure_values["pi"] /= 1000000

    if global_params["coverage_matrix"]["is_do"]:
        # value 1
        exposure_values["do"] = (
            hxd.cds.exposure.aggregate.total_amounts.assets
            / global_params["fx_live_expo"]
        )
        # value 2
        market_cap = (hxd.cds.exposure.aggregate.market_cap or 0) / global_params[
            "fx_live_expo"
        ]
        if market_cap and is_public:
            exposure_values["do"] = market_cap
        else:
            mk_factor = table_mkfactor.query(
                'category == "Factor MK-Assets"'
            ).value.item()
            exposure_values["do"] *= mk_factor
        exposure_values["do"] /= 1000000

    ## Get size factor
    for c in exposure_values:
        table_slice = table_size_factor.query(f'coverage == "{c}"')

        a_val = table_slice.query('parameter == "a"').value.item()
        b_val = table_slice.query('parameter == "b"').value.item()
        median_values = [
            table_slice.query('parameter == "min"').value.item(),
            table_slice.query('parameter == "max"').value.item(),
            a_val * exposure_values[c] ** b_val if exposure_values[c] else 0,
        ]

        size_factor_values[c] = np.median(median_values)

    return size_factor_values


def calculate_risk_assessment_factor(hxd):
    risk_assessment_factors = {"crime": 1, "pi": 1, "do": 1}

    global_params = global_parameters(hxd)
    table_risk_assessment = hx.params.table_risk_assessment
    bool_fids = (
        "agents_as_employees",
        "market_regulator",
        "valuation_for_pevc",
        "loan_covenant",
        "dando_portfolio_companies",
        "data_centre",
        "tech_outsourcing",
    )
    fids_coverage_map = {
        "policy_wording": ("any_any", {"crime", "pi", "do"}),
        "claims_history_cpi": ("any_crime_pi", {"crime", "pi"}),
        "claims_history_do": ("any_do", {"do"}),
        "risk_management": ("any_any", {"crime", "pi", "do"}),
        "strength_of_financial": ("any_any", {"crime", "pi", "do"}),
        "technological_infrastructure": ("any_any", {"crime", "pi", "do"}),
        "quality_of_control": ("any_crime", {"crime"}),
        "agents_as_employees": ("notins_crime_pi", {"crime", "pi"}),
        "regulatory_risk": ("any_pi_do", {"pi", "do"}),
        "quality_of_claims_handling": ("ins_pi", {"pi"}),
        "product_complexity": ("any_pi", {"pi"}),
        "quality_of_bcp": ("fin_pi", {"pi"}),
        "market_regulator": ("ban_fin_pi", {"pi"}),
        "extent_of_leveraged_gearing": ("inv_pi", {"pi"}),
        "quality_of_performance_non_pevc": ("inv_pi", {"pi"}),
        "redemption_gates": ("inv_pi", {"pi"}),
        "valuation_for_pevc": ("inv_PE_VC_RE_pi", {"pi"}),
        "loan_covenant": ("inv_PE_VC_RE_pi", {"pi"}),
        "dando_portfolio_companies": ("inv_PE_VC_do", {"do"}),
        "data_centre": ("fin_any", {"crime", "pi", "do"}),
        "tech_outsourcing": ("fin_any", {"crime", "pi", "do"}),
    }

    # loop over fids with question number to determine level factor from table
    for i, (fid, (switch, covers)) in enumerate(fids_coverage_map.items()):
        is_shown = getattr(hxd.non_cds.risk_assesment, switch)  # Is question showing?
        if is_shown:
            # loop over coverages and check if it is required to continue with calculation, otherwise the factor is kept 1 as it is
            for c in risk_assessment_factors:
                if risk_assessment_factors[c] == 0:
                    continue  # if the factor value for this coverage is already 0 then ignore this coverage in future iterations
                if c in covers:
                    if not global_params["coverage_matrix"][f"is_{c}"]:
                        risk_assessment_factors[c] = (
                            0  # if the coverage is required for this question and the coverage is off then set the factor to 0
                        )
                    else:  # calculate the factor
                        field_value = getattr(hxd.cds.modifiers.risk_category, fid)
                        if field_value is not None:
                            risk_level = (
                                get_field_options("risk_assessment", fid).index(
                                    field_value
                                )
                                if fid not in bool_fids
                                else 0 if field_value else 1
                            )
                            level_factor = table_risk_assessment.loc[i].at[
                                f"level_{risk_level + 1}"
                            ]
                            risk_assessment_factors[c] *= 1 + level_factor

    return risk_assessment_factors


def calculate_pi_product_mix_factor(hxd):
    industry_factors = {
        "banking": 1,
        "insurance": 1,
        "financial": 1,
        "stock_broker": 1,
        "trust_admin": 1,
    }
    solvency_ratio = 1
    segment_factor = 1

    global_params = global_parameters(hxd)
    table_revenue_split = hx.params.table_revenue_split
    table_solvency_ratio = hx.params.table_solvency_ratio

    # factor_key -> visibility_field_switch, industry_label, subindustry_label, ((field_id, field_label), ...)
    industry_map = {
        "banking": (
            "revenue_split_banks",
            "Banks",
            "Any",
            (
                ("interest", "Interest income"),
                ("fee", "Fee income"),
                ("trading", "Trading income"),
                ("other", "Other income"),
            ),
        ),
        "insurance": (
            "premium_split",
            "Insurance companies",
            "Any",
            (
                ("life", "Life insurance"),
                ("pc", "P&C insurance"),
                ("personal", "Personal lines"),
                ("commercial", "Commercial lines"),
                ("healthcare", "Medical/Healthcare"),
                ("ripc", "Reinsurance"),
                ("other", "Other"),
            ),
        ),
        "financial": (
            "revenue_split_exchanges",
            "Financial infrastructure & exchanges",
            "Any",
            (
                ("exchange", "Exchange"),
                ("listing", "Listing"),
                ("clear_settlement", "Clearing & Settlement"),
                ("depositary", "Depositary"),
                ("other", "Other"),
            ),
        ),
        "stock_broker": (
            "revenue_split_brokers",
            "Other",
            "Stock brokers/dealers",
            (
                ("institutional_advisory", "Institutional advisory"),
                ("institutional_execution", "Institutional execution only"),
                ("retail_advisory", "Retail advisory"),
                ("retail_execution", "Retail execution only"),
                ("retail_discretionary", "Retail Discretionary"),
                ("other", "Other"),
            ),
        ),
        "trust_admin": (
            "revenue_split_admin",
            "Other",
            "Trust Administrator",
            (
                ("est_companies", "Establishment/admin of companies"),
                ("est_trusts", "Establishment/admin of trusts"),
                ("outside_board", "Outside board positions"),
                ("legal_advice", "Legal advice"),
                ("accountancy", "Accountancy"),
                ("tax", "Tax"),
                ("other", "Other"),
            ),
        ),
    }

    # Industries
    for key, (switch, industry, subindustry, fields) in industry_map.items():
        is_shown = rgetattr(hxd.non_cds.exposure_details, f"{switch}.show")
        if is_shown:
            table_slice = table_revenue_split.query(
                f'industry.str.lower() == "{str(industry).lower()}" and subindustry.str.lower() == "{str(subindustry).lower()}"'
            )

            amounts = []
            factors = []
            for field_id, field_label in fields:
                field_value = rgetattr(
                    hxd.cds.exposure.granular, f"{switch}.{field_id}.amount"
                )
                if field_value is not None:
                    amounts.append(field_value)
                    factors.append(
                        table_slice.query(f'split == "{field_label}"').factor.item()
                    )

            multiplier = ratio(
                sum(map(operator.mul, factors, amounts)), sum(amounts)
            )  # SUMPRODUCT(factors_column, revenue_amounts_column) / SUM(revenue_amounts_column)
            industry_factors[key] *= multiplier

    # Solvency Ratio
    if hxd.non_cds.exposure_details.premium_split.show:
        field_value = hxd.cds.rating_factors.exposure_details.solvency_ratio
        if field_value is not None and field_value < table_solvency_ratio.iat[0, 1]:
            solvency_ratio = table_solvency_ratio.iat[1, 1]

    # Segment Factor
    if global_params["industry_matrix"]["is_inv"]:
        subindustry = hxd.cds.rating_factors.risk_info.sub_industry.lower() if hxd.cds.rating_factors.risk_info.sub_industry else hxd.cds.rating_factors.risk_info.sub_industry
        segment_factor_query = table_revenue_split.query(                      
            f'industry.str.lower() == "investment managers" and split.str.lower() == "{subindustry}"'
        ).factor
        if not segment_factor_query.empty:
            segment_factor = segment_factor_query.item()

    return np.prod(list(industry_factors.values())) * solvency_ratio * segment_factor


def calculate_adjustment_factors(hxd):
    global_params = global_parameters(hxd)
    table_retro_cover = hx.params.table_retro_cover.set_index("retro_dates")
    table_do_cover_types = hx.params.table_do_cover_types.set_index("cover_type")
    table_side_a_dic = hx.params.table_side_a_dic.set_index("category")

    final_uw_adj = 1 + (hxd.cds.modifiers.risk_category.uw_adj or 0)
    selected_towers = get_selected_towers_per_coverage(hxd)

    adjustment_factors = {
        "crime": {"retro": 0, "specific": 1, "final_uw_adj": final_uw_adj},
        "pi": {
            "retro": 0,
            "specific": (
                1
                if calculate_pi_product_mix_factor(hxd) == 0
                else calculate_pi_product_mix_factor(hxd)
            ),
            "final_uw_adj": final_uw_adj,
        },
        "A": {"retro": 0, "specific": 0, "final_uw_adj": final_uw_adj},
        "B": {"retro": 0, "specific": 0, "final_uw_adj": final_uw_adj},
        "C": {"retro": 0, "specific": 0, "final_uw_adj": final_uw_adj},
        "Dic": {"retro": 0, "specific": 0, "final_uw_adj": final_uw_adj},
    }

    # Retros
    for key in adjustment_factors:
        c = "do" if key in do_sides else key

        if global_params["coverage_matrix"][f"is_{c}"]:
            retro_date_value = getattr(
                hxd.cds.rating_factors.cover_details, f"{c}_retroactive_date"
            )
            factor = table_retro_cover.at[retro_date_value, c]
            adjustment_factors[key]["retro"] = factor

    # Specifics for D&O A B C
    for side in ("A", "B", "C"):
        if global_params["coverage_matrix"]["is_do"]:            
            adjustment_factors[side]["specific"] = table_do_cover_types.at[
                    side.upper(), "factor"
                ]

    # Specific for D&O Dic    
    if global_params["coverage_matrix"]["is_do"]:
        sides_sum = (
            adjustment_factors["A"]["specific"]
            + adjustment_factors["B"]["specific"]
            + adjustment_factors["C"]["specific"]
        )
        do_filtered_towers = (
            selected_towers[["C", "B", "A"]]
            .dropna(axis=0, how="all")
            .dropna(axis=1, how="all")
        )
        do_types_map = {"A": "A", "B": "AB", "C": "ABC"}

        category = "NA"
        for layer_num, covers in do_filtered_towers.iterrows():
            if category != "NA":
                break

            for do_type, tower in covers.iteritems():
                if not tower:
                    continue

                # DN Updated to account for 0 excess and Side C excess
                if layer_num == 0 and getattr(hxd.cds.layers[layer_num], tower).excess.selected is None:
                    if hxd.cds.rating_factors.cover_details.primary_layer.sir_all_manager.do is not None:
                        excess_value = hxd.cds.rating_factors.cover_details.primary_layer.sir_all_manager.do
                    else:
                        if hxd.cds.rating_factors.cover_details.primary_layer.sir_fund.do is not None:
                            excess_value = hxd.cds.rating_factors.cover_details.primary_layer.sir_fund.do
                        else:
                            if hxd.cds.rating_factors.cover_details.primary_layer.sir_all_manager.do_side_c is not None:
                                excess_value = hxd.cds.rating_factors.cover_details.primary_layer.sir_all_manager.do_side_c
                            else:
                                excess_value = hxd.cds.rating_factors.cover_details.primary_layer.sir_fund.do_side_c
 
                else:
                    excess_value = getattr(hxd.cds.layers[layer_num], tower).excess.selected
                # DN Updated to account for 0 excess
                if excess_value is not None:
                    category = do_types_map[do_type]
                    break

        factor = table_side_a_dic.at[category, "factor"]
        adjustment_factors["Dic"]["specific"] = sides_sum * factor

    return adjustment_factors


def calculate_frequency_split(hxd):
    freq_split = {
        "crime": {"manager": 1, "fund": 0},
        "pi": {"manager": 1, "fund": 0},
        "do": {"manager": 1, "fund": 0},
    }

    global_params = global_parameters(hxd)
    table_fund_manager_freq_split_imi = (
        hx.params.table_fund_manager_freq_split_imi.set_index("cover")
    )

    fund_factor_column = "other"
    if global_params["industry_matrix"]["is_inv"] and not (
        global_params["subindustry_matrix"]["is_mf"]
        or global_params["subindustry_matrix"]["is_sf"]
    ):
        fund_factor_column = "imi"

    for c in freq_split:
        freq_split[c]["fund"] = table_fund_manager_freq_split_imi.at[
            c, fund_factor_column
        ]
        freq_split[c]["manager"] = 1 - freq_split[c]["fund"]

    return freq_split


def calculate_cover_factor(hxd):
    cover_factors = {
        "crime": {"manager": 0, "fund": 0, "base_rate": 0},
        "pi": {"manager": 0, "fund": 0, "base_rate": 0},
        "A": {"manager": 0, "fund": 0, "base_rate": 0},
        "B": {"manager": 0, "fund": 0, "base_rate": 0},
        "C": {"manager": 0, "fund": 0, "base_rate": 0},
        "Dic": {"manager": 0, "fund": 0, "base_rate": 0},
    }

    size_factors = calculate_size_factor(hxd)
    initial_base_rates = calculate_initial_base_rate(hxd)
    risk_assessment_factors = calculate_risk_assessment_factor(hxd)
    adjustment_factors = calculate_adjustment_factors(hxd)
    freq_split = calculate_frequency_split(hxd)
    industry = hxd.cds.key_industry.code_name.lower() if hxd.cds.key_industry.code_name else hxd.cds.key_industry.code_name

    for key in cover_factors:
        c = "do" if key in do_sides else key

        if size_factors[c]:
            multiplier = np.prod(
                [
                    initial_base_rates[c],
                    size_factors[c],
                    risk_assessment_factors[c],
                    adjustment_factors[key]["retro"],
                    adjustment_factors[key]["specific"],
                    adjustment_factors[key]["final_uw_adj"],
                ]
            )

            cover_factors[key]["manager"] = multiplier * freq_split[c]["manager"]
            cover_factors[key]["fund"] = (
                0
                if industry != "investment managers"
                else multiplier * freq_split[c]["fund"]
            )
            cover_factors[key]["base_rate"] = (
                cover_factors[key]["manager"] + cover_factors[key]["fund"]
            )

    return cover_factors
