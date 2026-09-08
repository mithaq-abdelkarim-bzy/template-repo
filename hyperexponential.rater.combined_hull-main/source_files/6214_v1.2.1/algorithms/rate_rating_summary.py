import hx
import math as math
import algorithms.rate_constants as constants
from algorithms.rate_utilities import pd_df_from_hx_list, ratio


def rate_rating_summary(hxd):

    show_hide_toggles = hxd.non_cds.show_hide_toggles
    vessels = hxd.cds.exposure.granular.vessels
    is_hull = show_hide_toggles.hull.show_hull_coverage
    is_iv = show_hide_toggles.iv.show_iv_coverage
    is_war = show_hide_toggles.war.show_war_coverage
    is_loh = show_hide_toggles.loh.show_loh_coverage
    is_ship_building = show_hide_toggles.ship_building.show_ship_building_coverage

    show_rating_summary_table = hxd.non_cds.show_rating_summary_table
    show_rating_summary_table.show_loh_table = False
    show_rating_summary_table.show_hull_table = False
    show_rating_summary_table.show_hull_iv_table = False
    show_rating_summary_table.show_hull_war_table = False
    show_rating_summary_table.show_hull_iv_war_table = False
    show_rating_summary_table.show_ship_building_table = False

    validation_message = "Add a note in Rating Summary's UW comment to explain the Shipbuilders UW adjustment"
    is_uw_note_needed = False

    if is_loh:
        loh_rating_summary = hxd.cds.layers[0].coverages.loh

        if loh_rating_summary.status not in ["Bound", "Post Bind Complete"]:
            hx.errors.validation(
                "LOH Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final"
            )

        vessels_df = pd_df_from_hx_list(
            hxd.cds.exposure.granular.vessels.loh_rating.loh_vessels_list
        )
        loh_rating_summary.benchmark_premium_pro_rated_100pct = (
            loh_rating_summary.loh_total_premium
        )

        brokerage = loh_rating_summary.brokerage or 0
        benchmark_premium_mask = vessels_df["loh_benchmark_premium"].notna()

        vessels_df.loc[benchmark_premium_mask, "expected_loss"] = (
            vessels_df.loc[benchmark_premium_mask, "loh_benchmark_premium"]
            .mul(1 - brokerage)
            .mul(constants.benchmark_lr)
        )

        vessels_df.loc[benchmark_premium_mask, "expected_loss_pre_uw_adj"] = (
            vessels_df.loc[benchmark_premium_mask, "expected_loss"].div(
                1
                + vessels_df.loc[benchmark_premium_mask, "loh_uw_adjustment"].fillna(0)
            )
        )

        loh_rating_summary.expected_loss_cost_pro_rated_100pct = (
            vessels_df["expected_loss"].fillna(0).sum()
        )

        loh_rating_summary.expected_loss_cost_pre_uw_adj = (
            vessels_df["expected_loss_pre_uw_adj"].fillna(0).sum()
        )

        loh_rating_summary.uw_adj_impact = (
            None
            if loh_rating_summary.expected_loss_cost_pro_rated_100pct == 0
            else ratio(
                loh_rating_summary.expected_loss_cost_pro_rated_100pct,
                loh_rating_summary.expected_loss_cost_pre_uw_adj,
            )
            - 1
        )

        loh_rating_summary.quoted_premium_pro_rated_100pct = (
            loh_rating_summary.loh_achieved_premium
        )
        show_rating_summary_table.show_loh_table = True
    elif is_ship_building:
        ship_building_rating_summary = hxd.cds.layers[0].coverages.ship_building
        if ship_building_rating_summary.status not in ["Bound", "Post Bind Complete"]:
            hx.errors.validation(
                "Shipbuilders Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final"
            )
        brokerage = ship_building_rating_summary.brokerage or 0
        other_deductions = ship_building_rating_summary.other_deductions or 0
        experience_rating = hxd.cds.experience_rating.ship_building
        uw_adj = ship_building_rating_summary.ship_building_uw_adjustment or 0
        exposure_net_benchmark_premium_pre_uw_adj = (
            ship_building_rating_summary.ship_building_net_benchmark_premium_pre_uw_adj
            or 0
        )

        exposure_loss_cost_pre_uw_adj = (
            ship_building_rating_summary.expected_loss_cost_pre_uw_adj or 0
        )
        experience_loss_cost_pre_uw_adj = (
            experience_rating.experience_pricing_results.experience_claims_cost or 0
        )
        experience_credibility = (
            experience_rating.experience_weighting_calculation.experience_weighting or 0
        )

        ship_building_rating_summary.expected_loss_cost_pre_uw_adj = (
            exposure_loss_cost_pre_uw_adj * (1 - experience_credibility)
        ) + (experience_loss_cost_pre_uw_adj * experience_credibility)

        ship_building_rating_summary.expected_loss_cost_pro_rated_100pct = (
            ship_building_rating_summary.expected_loss_cost_pre_uw_adj * (1 + uw_adj)
        )

        experience_premium = (
            ship_building_rating_summary.ship_building_experience_premium or 0
        )

        ship_building_rating_summary.ship_building_blended_benchmark_premium_pre_uw_adj = (
            exposure_net_benchmark_premium_pre_uw_adj * (1 - experience_credibility)
        ) + (
            experience_premium * experience_credibility
        )

        ship_building_rating_summary.ship_building_blended_benchmark_premium_post_uw_adj = (
            ship_building_rating_summary.ship_building_blended_benchmark_premium_pre_uw_adj
            * (1 + uw_adj)
        )

        ship_building_rating_summary.benchmark_premium_pro_rated_100pct = (
            ship_building_rating_summary.ship_building_blended_benchmark_premium_post_uw_adj
            / (1 - brokerage - other_deductions)
        )

        ship_building_rating_summary.uw_adj_impact = (
            None
            if ship_building_rating_summary.expected_loss_cost_pro_rated_100pct == 0
            else ratio(
                ship_building_rating_summary.expected_loss_cost_pro_rated_100pct,
                ship_building_rating_summary.expected_loss_cost_pre_uw_adj,
            )
            - 1
        )

        show_rating_summary_table.show_ship_building_table = True
        if (
            (not ship_building_rating_summary.ship_building_uw_adjustment is None)
            and (ship_building_rating_summary.ship_building_uw_adjustment > 0)
            and ((not hxd.cds.uw_comment) or (len(hxd.cds.uw_comment) == 0))
        ):
            is_uw_note_needed = True
    elif is_hull:
        any_coverage_bound = False
        hull_rating_summary = hxd.cds.layers[0].coverages.hull

        if hull_rating_summary.section_reference:
            if hull_rating_summary.status in ["Bound", "Post Bind Complete"]:
                any_coverage_bound = True
            else:
                hx.errors.validation(
                    "Hull Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final"
                )

        vessels_df = pd_df_from_hx_list(vessels.hull_rating.vessels_list)
        hull_rating_summary.total_quoted_premium = (
            hull_rating_summary.quoted_premium_pro_rated_100pct
        ) = hull_rating_summary.achieved_premium = (
            vessels_df["achieved_premium"].fillna(0).sum()
        )
        vessels_df["premium_to_use"] = vessels_df[
            "behavioural_benchmark_premium"
        ].fillna(vessels_df["static_benchmark_premium"])

        brokerage = hull_rating_summary.brokerage or 0
        hull_rating_summary.benchmark_premium_pro_rated_100pct = (
            vessels_df["premium_to_use"].fillna(0).sum()
        )
        modelling_list = hxd.cds.exposure.granular.vessels.hull_rating.modelling_list
        if len(modelling_list) == 0:
            return
        modelling_df = pd_df_from_hx_list(modelling_list)
        modelling_columns = modelling_df.columns
        static_prefix = "static_"
        behavioural_prefix = "behavioural_"
        if f"{behavioural_prefix}el_pre_uw_adj" in modelling_columns:
            modelling_df["el_pre_uw_adj"] = modelling_df[
                f"{behavioural_prefix}el_pre_uw_adj"
            ].fillna(modelling_df[f"{static_prefix}el_pre_uw_adj"])
        elif f"{static_prefix}el_pre_uw_adj" in modelling_columns:
            modelling_df["el_pre_uw_adj"] = modelling_df[
                f"{static_prefix}el_pre_uw_adj"
            ]

        if f"{behavioural_prefix}el_post_uw_adj" in modelling_columns:
            modelling_df["el_post_uw_adj"] = modelling_df[
                f"{behavioural_prefix}el_post_uw_adj"
            ].fillna(modelling_df[f"{static_prefix}el_post_uw_adj"])
        elif f"{static_prefix}el_post_uw_adj" in modelling_columns:
            modelling_df["el_post_uw_adj"] = modelling_df[
                f"{static_prefix}el_post_uw_adj"
            ]

        if (f"el_pre_uw_adj" in modelling_df.columns) and (
            f"el_post_uw_adj" in modelling_df.columns
        ):
            # Benchmark LR is already factored in the vessels premium calculation
            hull_rating_summary.expected_loss_cost_pro_rated_100pct = (
                modelling_df["el_post_uw_adj"].fillna(0).sum()
            )
            hull_rating_summary.expected_loss_cost_pre_uw_adj = (
                modelling_df["el_pre_uw_adj"].fillna(0).sum()
            )

            hull_rating_summary.uw_adj_impact = (
                None
                if hull_rating_summary.expected_loss_cost_pro_rated_100pct == 0
                else ratio(
                    hull_rating_summary.expected_loss_cost_pro_rated_100pct,
                    hull_rating_summary.expected_loss_cost_pre_uw_adj,
                )
                - 1
            )

        iv_prefix = "iv/iv_"
        iv_rating_summary = hxd.cds.layers[0].coverages.iv
        iv_brokerage = iv_rating_summary.brokerage.selected or 0
        war_prefix = "war/war_"
        war_rating_summary = hxd.cds.layers[0].coverages.war
        war_brokerage = war_rating_summary.brokerage.selected or 0
        mask_is_include_iv_vessel = vessels_df[f"{iv_prefix}is_include_vessel"]
        mask_is_include_war_vessel = vessels_df[f"{war_prefix}is_include_vessel"]

        if is_iv and is_war:

            if iv_rating_summary.section_reference:
                if iv_rating_summary.status in [
                    "Bound",
                    "Post Bind Complete",
                ]:
                    any_coverage_bound = True
                else:
                    hx.errors.validation(
                        "IV Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final"
                    )

            if war_rating_summary.section_reference:
                if war_rating_summary.status in [
                    "Bound",
                    "Post Bind Complete",
                ]:
                    any_coverage_bound = True
                else:
                    hx.errors.validation(
                        "War Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final"
                    )

            iv_rating_summary.benchmark_premium_pro_rated_100pct = (
                vessels_df.loc[
                    mask_is_include_iv_vessel, f"{iv_prefix}benchmark_premium"
                ]
                .fillna(0)
                .sum()
            )

            iv_benchmark_premium_mask = (
                mask_is_include_iv_vessel
                & vessels_df[f"{iv_prefix}benchmark_premium"].notna()
            )
            vessels_df.loc[
                iv_benchmark_premium_mask, f"{iv_prefix}expected_loss_cost"
            ] = (
                vessels_df.loc[
                    iv_benchmark_premium_mask, f"{iv_prefix}benchmark_premium"
                ]
                .mul(constants.benchmark_lr)
                .mul(1 - iv_brokerage)
            )

            vessels_df.loc[
                iv_benchmark_premium_mask, f"{iv_prefix}expected_loss_cost_pre_uw_adj"
            ] = vessels_df.loc[
                iv_benchmark_premium_mask, f"{iv_prefix}expected_loss_cost"
            ].div(
                (
                    1
                    + vessels_df.loc[
                        iv_benchmark_premium_mask, f"{iv_prefix}uw_adjustment"
                    ].fillna(0)
                )
            )

            iv_rating_summary.expected_loss_cost_pro_rated_100pct = (
                vessels_df.loc[
                    mask_is_include_iv_vessel, f"{iv_prefix}expected_loss_cost"
                ]
                .fillna(0)
                .sum()
            )

            iv_rating_summary.expected_loss_cost_pre_uw_adj = (
                vessels_df.loc[
                    mask_is_include_iv_vessel,
                    f"{iv_prefix}expected_loss_cost_pre_uw_adj",
                ]
                .fillna(0)
                .sum()
            )

            iv_rating_summary.uw_adj_impact = (
                None
                if iv_rating_summary.expected_loss_cost_pro_rated_100pct == 0
                else ratio(
                    iv_rating_summary.expected_loss_cost_pro_rated_100pct,
                    iv_rating_summary.expected_loss_cost_pre_uw_adj,
                )
                - 1
            )

            iv_rating_summary.total_quoted_premium = (
                iv_rating_summary.quoted_premium_pro_rated_100pct
            ) = iv_rating_summary.iv_achieved_premium = (
                vessels_df.loc[
                    mask_is_include_iv_vessel, f"{iv_prefix}achieved_premium"
                ]
                .fillna(0)
                .sum()
            )

            war_rating_summary.benchmark_premium_pro_rated_100pct = (
                vessels_df.loc[
                    mask_is_include_war_vessel, f"{war_prefix}benchmark_premium"
                ]
                .fillna(0)
                .sum()
            )

            war_rating_summary.total_quoted_premium = (
                war_rating_summary.quoted_premium_pro_rated_100pct
            ) = war_rating_summary.war_achieved_premium = (
                vessels_df.loc[
                    mask_is_include_war_vessel, f"{war_prefix}achieved_premium"
                ]
                .fillna(0)
                .sum()
            )

            war_benchmark_premium_mask = (
                mask_is_include_war_vessel
                & vessels_df[f"{war_prefix}benchmark_premium"].notna()
            )
            vessels_df.loc[
                war_benchmark_premium_mask, f"{war_prefix}expected_loss_cost"
            ] = (
                vessels_df.loc[
                    war_benchmark_premium_mask, f"{war_prefix}benchmark_premium"
                ]
                .mul(constants.benchmark_lr)
                .mul(1 - war_brokerage)
            )

            vessels_df.loc[
                war_benchmark_premium_mask, f"{war_prefix}expected_loss_cost_pre_uw_adj"
            ] = vessels_df.loc[
                war_benchmark_premium_mask, f"{war_prefix}expected_loss_cost"
            ].div(
                (
                    1
                    + vessels_df.loc[
                        war_benchmark_premium_mask, f"{war_prefix}uw_adjustment"
                    ].fillna(0)
                )
            )

            war_rating_summary.expected_loss_cost_pro_rated_100pct = (
                vessels_df.loc[
                    mask_is_include_war_vessel, f"{war_prefix}expected_loss_cost"
                ]
                .fillna(0)
                .sum()
            )

            war_rating_summary.expected_loss_cost_pre_uw_adj = (
                vessels_df.loc[
                    mask_is_include_war_vessel,
                    f"{war_prefix}expected_loss_cost_pre_uw_adj",
                ]
                .fillna(0)
                .sum()
            )

            war_rating_summary.uw_adj_impact = (
                None
                if war_rating_summary.expected_loss_cost_pro_rated_100pct == 0
                else ratio(
                    war_rating_summary.expected_loss_cost_pro_rated_100pct,
                    war_rating_summary.expected_loss_cost_pre_uw_adj,
                )
                - 1
            )

            show_rating_summary_table.show_hull_iv_war_table = True
        elif is_iv:

            if iv_rating_summary.section_reference:
                if iv_rating_summary.status in [
                    "Bound",
                    "Post Bind Complete",
                ]:
                    any_coverage_bound = True
                else:
                    hx.errors.validation(
                        "IV Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final"
                    )

            iv_rating_summary.benchmark_premium_pro_rated_100pct = (
                vessels_df.loc[
                    mask_is_include_iv_vessel, f"{iv_prefix}benchmark_premium"
                ]
                .fillna(0)
                .sum()
            )

            iv_benchmark_premium_mask = (
                mask_is_include_iv_vessel
                & vessels_df[f"{iv_prefix}benchmark_premium"].notna()
            )
            vessels_df.loc[
                iv_benchmark_premium_mask, f"{iv_prefix}expected_loss_cost"
            ] = (
                vessels_df.loc[
                    iv_benchmark_premium_mask, f"{iv_prefix}benchmark_premium"
                ]
                .mul(constants.benchmark_lr)
                .mul(1 - iv_brokerage)
            )

            vessels_df.loc[
                iv_benchmark_premium_mask, f"{iv_prefix}expected_loss_cost_pre_uw_adj"
            ] = vessels_df.loc[
                iv_benchmark_premium_mask, f"{iv_prefix}expected_loss_cost"
            ].div(
                (
                    1
                    + vessels_df.loc[
                        iv_benchmark_premium_mask, f"{iv_prefix}uw_adjustment"
                    ].fillna(0)
                )
            )

            iv_rating_summary.expected_loss_cost_pro_rated_100pct = (
                vessels_df.loc[
                    mask_is_include_iv_vessel, f"{iv_prefix}expected_loss_cost"
                ]
                .fillna(0)
                .sum()
            )

            iv_rating_summary.expected_loss_cost_pre_uw_adj = (
                vessels_df.loc[
                    mask_is_include_iv_vessel,
                    f"{iv_prefix}expected_loss_cost_pre_uw_adj",
                ]
                .fillna(0)
                .sum()
            )

            iv_rating_summary.uw_adj_impact = (
                None
                if iv_rating_summary.expected_loss_cost_pro_rated_100pct == 0
                else ratio(
                    iv_rating_summary.expected_loss_cost_pro_rated_100pct,
                    iv_rating_summary.expected_loss_cost_pre_uw_adj,
                )
                - 1
            )

            iv_rating_summary.total_quoted_premium = (
                iv_rating_summary.quoted_premium_pro_rated_100pct
            ) = iv_rating_summary.iv_achieved_premium = (
                vessels_df.loc[
                    mask_is_include_iv_vessel, f"{iv_prefix}achieved_premium"
                ]
                .fillna(0)
                .sum()
            )
            show_rating_summary_table.show_hull_iv_table = True
        elif is_war:

            if war_rating_summary.section_reference:
                if war_rating_summary.status in [
                    "Bound",
                    "Post Bind Complete",
                ]:
                    any_coverage_bound = True
                else:
                    hx.errors.validation(
                        "War Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final"
                    )

            war_rating_summary.benchmark_premium_pro_rated_100pct = (
                vessels_df.loc[
                    mask_is_include_war_vessel, f"{war_prefix}benchmark_premium"
                ]
                .fillna(0)
                .sum()
            )

            war_rating_summary.total_quoted_premium = (
                war_rating_summary.quoted_premium_pro_rated_100pct
            ) = war_rating_summary.war_achieved_premium = (
                vessels_df.loc[
                    mask_is_include_war_vessel, f"{war_prefix}achieved_premium"
                ]
                .fillna(0)
                .sum()
            )

            war_benchmark_premium_mask = (
                mask_is_include_war_vessel
                & vessels_df[f"{war_prefix}benchmark_premium"].notna()
            )
            vessels_df.loc[
                war_benchmark_premium_mask, f"{war_prefix}expected_loss_cost"
            ] = (
                vessels_df.loc[
                    war_benchmark_premium_mask, f"{war_prefix}benchmark_premium"
                ]
                .mul(constants.benchmark_lr)
                .mul(1 - war_brokerage)
            )

            vessels_df.loc[
                war_benchmark_premium_mask, f"{war_prefix}expected_loss_cost_pre_uw_adj"
            ] = vessels_df.loc[
                war_benchmark_premium_mask, f"{war_prefix}expected_loss_cost"
            ].div(
                (
                    1
                    + vessels_df.loc[
                        war_benchmark_premium_mask, f"{war_prefix}uw_adjustment"
                    ].fillna(0)
                )
            )

            war_rating_summary.expected_loss_cost_pro_rated_100pct = (
                vessels_df.loc[
                    mask_is_include_war_vessel, f"{war_prefix}expected_loss_cost"
                ]
                .fillna(0)
                .sum()
            )

            war_rating_summary.expected_loss_cost_pre_uw_adj = (
                vessels_df.loc[
                    mask_is_include_war_vessel,
                    f"{war_prefix}expected_loss_cost_pre_uw_adj",
                ]
                .fillna(0)
                .sum()
            )

            war_rating_summary.uw_adj_impact = (
                None
                if war_rating_summary.expected_loss_cost_pro_rated_100pct == 0
                else ratio(
                    war_rating_summary.expected_loss_cost_pro_rated_100pct,
                    war_rating_summary.expected_loss_cost_pre_uw_adj,
                )
                - 1
            )
            show_rating_summary_table.show_hull_war_table = True
        else:
            show_rating_summary_table.show_hull_table = True

        if not any_coverage_bound:
            hx.errors.validation(
                "At least one Hull, IV or War section must be bound to mark a policy as final"
            )

    if is_uw_note_needed:
        hx.errors.validation(validation_message)

    hxd.non_cds.show_hide_toggles.ship_building.show_uw_adj_warning = is_uw_note_needed
    hxd.non_cds.show_hide_toggles.ship_building.hide_uw_adj_warning = (
        not is_uw_note_needed
    )
