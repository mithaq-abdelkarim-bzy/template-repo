import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter


def is_match_inception_year_and_policy_year(inception_year, policy_reference):
    if (not (inception_year and policy_reference)) or (len(policy_reference) < 8):
        return True
    else:
        try:
            return str(inception_year)[-2:] == policy_reference[6:8]
        except (ValueError, TypeError):
            return False


def rate_risk_information(hxd):
    # Extracts database id for the risk information tab
    underwriters_table = hx.params.table_input_underwriters
    hxd.cds.database_id = hx.meta.policy_option_id
    coverage_type = hxd.cds.coverage_type
    currency = hxd.cds.currencies.source_currency
    inception_year = (
        hxd.cds.standard_fields.inception_date.year
        if hxd.cds.standard_fields.inception_date
        else None
    )
    hxd.cds.currency_agreed_value_label = (
        f"Agreed Value ({currency})" if currency else "Agreed Value"
    )
    hxd.cds.currency_loh_agreed_value_label = (
        f"Hull Value - ({currency})" if currency else "Hull Value"
    )

    hxd.cds.currency_loh_total_sum_insured_label = (
        f"Total Sum Insured - ({currency})" if currency else "Total Sum Insured"
    )

    hxd.non_cds.labels.currency_loh_benchmark_premium_label = (
        f"Gross Benchmark Premium - ({currency})"
        if currency
        else "Gross Benchmark Premium"
    )

    hxd.non_cds.labels.currency_loh_daily_rate_label = (
        f"LOH Daily Rate - ({currency})" if currency else "LOH Daily Rate"
    )
    show_hide_toggles = hxd.non_cds.show_hide_toggles
    show_hide_toggles.hull.show_hull_coverage = False
    show_hide_toggles.loh.show_loh_coverage = False
    show_hide_toggles.ship_building.show_ship_building_coverage = False
    show_hide_toggles.iv.show_iv_coverage = False
    show_hide_toggles.war.show_war_coverage = False
    show_hide_toggles.show_powersearch = True
    # underwriters_list = []
    underwriters_list = underwriters_table["underwriter"].tolist()
    mismatched_inception_message = (
        "Warning, Inception Year does not match the Policy Reference's year"
    )
    if not hxd.model_state.show_after_landing_page:
        return
    if coverage_type == "Hull, IV, War":
        show_hide_toggles.hull.show_hull_coverage = True
        show_hide_toggles.iv.show_iv_coverage = hxd.cds.is_iv_coverage
        show_hide_toggles.war.show_war_coverage = hxd.cds.is_war_coverage

        for coverage in ["hull", "iv", "war"]:
            if (coverage == "iv" and not hxd.cds.is_iv_coverage) or (
                coverage == "war" and not hxd.cds.is_war_coverage
            ):
                continue
            if not is_match_inception_year_and_policy_year(
                inception_year,
                getattr(hxd.cds.layers[0].coverages, coverage).section_reference,
            ):
                show_hide_toggles.show_mismatched_inception_year_warning = True
                show_hide_toggles.show_powersearch = False
                hxd.non_cds.labels.mismatched_inception_year_warning = (
                    f"{coverage.capitalize()}: {mismatched_inception_message}"
                )
                break
        # underwriters_list.extend(underwriters_table["underwriter"].tolist())
    elif coverage_type == "Loss of Hire (LOH)":
        # underwriters_list = underwriters_table.loc[
        #     underwriters_table["team"] == "team 2"
        # ]["underwriter"].tolist()
        show_hide_toggles.loh.show_loh_coverage = True
        if not is_match_inception_year_and_policy_year(
            inception_year,
            hxd.cds.layers[0].coverages.loh.section_reference,
        ):
            show_hide_toggles.show_mismatched_inception_year_warning = True
            show_hide_toggles.show_powersearch = False
            hxd.non_cds.labels.mismatched_inception_year_warning = (
                f"{coverage_type}: {mismatched_inception_message}"
            )

    elif coverage_type == "Shipbuilders":
        # underwriters_list.extend(
        #     underwriters_table.loc[underwriters_table["team"] == "team 3"][
        #         "underwriter"
        #     ].tolist()
        # )
        ship_building_labels = hxd.non_cds.labels.ship_building
        ship_building_labels.achieved_premium = (
            (f"Achieved Net Premium (100%, {currency})")
            if currency
            else "Achieved Net Premium (100%)"
        )
        ship_building_labels.exposure_benchmark_premium = (
            f"Benchmark Net Premium (Exposure Rated, 100%, {currency})"
            if currency
            else "Benchmark Net Premium (Exposure Rated, 100%)"
        )
        ship_building_labels.experience_benchmark_premium = (
            f"Benchmark Net Premium (Experience Rated, 100%, {currency})"
            if currency
            else "Benchmark Net Premium (Experience Rated, 100%)"
        )
        ship_building_labels.blended_premium_pre_adj = (
            f"Blended Benchmark Net Premium (100%, {currency}) Before UW Adj."
            if currency
            else "Blended Benchmark Net Premium (100%) Before UW Adj."
        )
        ship_building_labels.blended_premium_post_adj = (
            f"Blended Benchmark Net Premium (100%, {currency}) After UW Adj."
            if currency
            else "Blended Benchmark Net Premium (100%) After UW Adj."
        )
        show_hide_toggles.ship_building.show_ship_building_coverage = True
        if not is_match_inception_year_and_policy_year(
            inception_year,
            hxd.cds.layers[0].coverages.ship_building.section_reference,
        ):
            show_hide_toggles.show_mismatched_inception_year_warning = True
            hxd.non_cds.labels.mismatched_inception_year_warning = (
                hxd.non_cds.labels.mismatched_inception_year_warning
            )
            hxd.non_cds.labels.mismatched_inception_year_warning = (
                f"{coverage_type}: {mismatched_inception_message}"
            )

    underwriters_list.append("Other")
    hxd.cds.uw_dropdown_population = [
        {"underwriter": item} for item in underwriters_list
    ]
