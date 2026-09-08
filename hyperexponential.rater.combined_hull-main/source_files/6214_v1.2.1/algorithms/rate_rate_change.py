import json

import hx

from algorithms.rate_constants import max_layers
from algorithms.rate_utilities import date_to_string, is_hx_class, one_layer, ratio, title_rc


def save_lists_for_rate_change(hxd):
    if hxd.non_cds.show_hide_toggles.hull.show_hull_coverage:
        hull_vessels_list = hxd.cds.exposure.granular.vessels.hull_rating.vessels_list

        # Export the hull vessels list
        exported_hull_vessels_list = [
            {
                "vessel_details": {"imo": v.vessel_details.imo},
                "unique_imo": v.unique_imo,
                "inception_date": date_to_string(v.inception_date),
                "expiry_date": date_to_string(v.expiry_date),
                "coverage": v.coverage,
                "agreed_value": v.agreed_value,
                "year_built": v.year_built,
                "flag": v.flag,
                "model_flag": v.model_flag,
                "vessel_type": v.vessel_type,
                "dwt": v.dwt,
                "deductible": v.deductible,
                # "number_of_unique_port_visits": v.number_of_unique_port_visits,
                # "perc_time_eez": v.perc_time_eez,
                # "ratio_moving": v.ratio_moving,
                # "max_distance_ratio": v.max_distance_ratio,
                "ratio_moored": v.ratio_moored,
                "ship_type": v.ship_type,
                "raw_ship_type": v.raw_ship_type,
                "age": v.age,
                "uw_adjustment": v.uw_adjustment,
                "iv": {
                    "iv_agreed_value": {
                        "calculated": v.iv.iv_agreed_value.calculated,
                        "is_overridden": True,
                        "selected": v.iv.iv_agreed_value.selected,
                    },
                    "iv_deductible": {
                        "calculated": v.iv.iv_deductible.calculated,
                        "is_overridden": True,
                        "selected": v.iv.iv_deductible.selected,
                    },
                    "iv_is_include_vessel": v.iv.iv_is_include_vessel,
                    "iv_achieved_premium": v.iv.iv_achieved_premium,
                    "iv_coverage": v.iv.iv_coverage,
                    "iv_uw_adjustment": v.iv.iv_uw_adjustment,
                },
                "war": {
                    "war_agreed_value": {
                        "calculated": v.war.war_agreed_value.calculated,
                        "is_overridden": True,
                        "selected": v.war.war_agreed_value.selected,
                    },
                    "war_is_include_vessel": v.war.war_is_include_vessel,
                    "war_achieved_premium": v.war.war_achieved_premium,
                    "war_uw_adjustment": v.war.war_uw_adjustment,
                },
            }
            for v in hull_vessels_list
        ]
        hxd.rate_change.hull_vessels = json.dumps(exported_hull_vessels_list)

    elif hxd.non_cds.show_hide_toggles.loh.show_loh_coverage:
        loh_vessels_list = hxd.cds.exposure.granular.vessels.loh_rating.loh_vessels_list
        exported_loh_vessels_list = [
            {
                "loh_unique_identifier": v.loh_unique_identifier,
                "loh_cover": v.loh_cover,
                "loh_daily_rate": v.loh_daily_rate,
                "loh_xs_days": v.loh_xs_days,
                "loh_uw_adjustment": v.loh_uw_adjustment,
            }
            for v in loh_vessels_list
        ]
        hxd.rate_change.loh_vessels = json.dumps(exported_loh_vessels_list)

    elif hxd.non_cds.show_hide_toggles.ship_building.show_ship_building_coverage:
        ship_building_vessels_list = (
            hxd.cds.exposure.granular.vessels.ship_building_rating.ship_building_vessels_list
        )
        exported_ship_building_vessels_list = [
            {
                "ship_building_index": v.ship_building_index,
                "ship_building_number_of_vessels": v.ship_building_number_of_vessels,
                "ship_building_total_months_steel_cutting_keel_laying": v.ship_building_total_months_steel_cutting_keel_laying,
                "ship_building_total_months_keel_laying_launch": v.ship_building_total_months_keel_laying_launch,
                "ship_building_total_months_launch_delivery": v.ship_building_total_months_launch_delivery,
                "ship_building_total_months_all_stages": v.ship_building_total_months_all_stages,
                "ship_building_vessel_type": v.ship_building_vessel_type,
                "ship_building_country": v.ship_building_country,
                "ship_building_survey_grade": v.ship_building_survey_grade,
                "ship_building_deductible": v.ship_building_deductible,
                "ship_building_sum_insured": v.ship_building_sum_insured,
            }
            for v in ship_building_vessels_list
        ]
        hxd.rate_change.shipbuilders_vessels = json.dumps(
            exported_ship_building_vessels_list
        )


def rate_change_buckets(hxd):

    hull_rating_buckets = {
        "model": [            
            "hx_core/inception_date",
            # "hx_core/expiry_date",
        ],  # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": [
            "cds/exposure/granular/vessels/hull_rating/vessels_list/vessel_details/imo",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/unique_imo",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/inception_date",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/expiry_date",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/agreed_value",
        ],
        "risk_characteristics": [
            "cds/exposure/granular/vessels/hull_rating/vessels_list/year_built",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/vessel_type",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/coverage",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/flag",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/model_flag",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/dwt",
            # "cds/exposure/granular/vessels/hull_rating/vessels_list/max_distance_ratio",
            # "cds/exposure/granular/vessels/hull_rating/vessels_list/number_of_unique_port_visits",
            # "cds/exposure/granular/vessels/hull_rating/vessels_list/perc_time_eez",
            # "cds/exposure/granular/vessels/hull_rating/vessels_list/ratio_moving",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/ratio_moored",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/ship_type",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/raw_ship_type",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/age",
        ],
        "deductible": [
            "cds/exposure/granular/vessels/hull_rating/vessels_list/deductible"
        ],
        "limit": [],
        "terms_conditions": [],
        "brokerage": ["cds/layers/coverages/hull/brokerage"],
        "other": [
            "cds/exposure/granular/vessels/hull_rating/vessels_list/uw_adjustment",
            "cds/exposure/granular/vessels/hull_rating/fleet_soft_factors/fleet_casualty_history",
            "cds/exposure/granular/vessels/hull_rating/fleet_soft_factors/owner_quality",
        ],
    }

    iv_buckets = {
        "model": [
            "hx_core/inception_date",
            # "hx_core/expiry_date",
        ],  # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": [
            "cds/exposure/granular/vessels/hull_rating/vessels_list/unique_imo",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/inception_date",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/expiry_date",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/iv/iv_agreed_value",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/agreed_value",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/iv/iv_is_include_vessel",
        ],
        "risk_characteristics": [
            "cds/exposure/granular/vessels/hull_rating/vessels_list/year_built",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/flag",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/model_flag",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/vessel_type",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/dwt",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/coverage",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/iv/iv_coverage",
            # "cds/exposure/granular/vessels/hull_rating/vessels_list/max_distance_ratio",
            # "cds/exposure/granular/vessels/hull_rating/vessels_list/number_of_unique_port_visits",
            # "cds/exposure/granular/vessels/hull_rating/vessels_list/perc_time_eez",
            # "cds/exposure/granular/vessels/hull_rating/vessels_list/ratio_moving",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/ratio_moored",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/ship_type",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/raw_ship_type",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/age",
        ],
        "deductible": [
            "cds/exposure/granular/vessels/hull_rating/vessels_list/deductible",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/iv/iv_deductible",
        ],
        "limit": [],
        "terms_conditions": [],
        "brokerage": [
            "cds/layers/coverages/hull/brokerage",
            "cds/layers/coverages/iv/brokerage",
        ],
        "other": [
            "cds/exposure/granular/vessels/hull_rating/vessels_list/iv/iv_uw_adjustment",
            "cds/exposure/granular/vessels/hull_rating/fleet_soft_factors/fleet_casualty_history",
            "cds/exposure/granular/vessels/hull_rating/fleet_soft_factors/owner_quality",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/uw_adjustment",
        ],
    }

    war_buckets = {
        "model": [
            "hx_core/inception_date",
            # "hx_core/expiry_date",
        ],  # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": [
            "cds/exposure/granular/vessels/hull_rating/vessels_list/unique_imo",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/war/war_agreed_value",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/war/war_is_include_vessel",
            "cds/exposure/granular/vessels/hull_rating/vessels_list/war/war_achieved_premium",
        ],
        "risk_characteristics": [],
        "deductible": [],
        "limit": [],
        "terms_conditions": [],
        "brokerage": [
            "cds/layers/coverages/war/brokerage",
        ],
        "other": [
            "cds/exposure/granular/vessels/hull_rating/vessels_list/war/war_uw_adjustment"
        ],
    }

    loh_buckets = {
        "model": [
            # "hx_core/inception_date",
            # # "hx_core/expiry_date",
        ],  # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": [
            # "hx_core/inception_date",
            # "hx_core/expiry_date",
            "cds/exposure/granular/vessels/loh_rating/loh_vessels_list/loh_daily_rate",
        ],
        "risk_characteristics": [
            "cds/exposure/granular/vessels/loh_rating/loh_vessels_list/loh_cover"
            
        ],
        "deductible": [
            "cds/exposure/granular/vessels/loh_rating/loh_vessels_list/loh_xs_days"
        ],
        "limit": [],
        "terms_conditions": [],
        "brokerage": [
            "cds/layers/coverages/loh/brokerage",
        ],
        "other": [
            "cds/exposure/granular/vessels/loh_rating/loh_vessels_list/loh_uw_adjustment"
        ],
    }

    ship_builders_buckets = {
        "model": [
            # "hx_core/inception_date",
            # # "hx_core/expiry_date",
        ],  # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": [
            # "hx_core/inception_date",
            # "hx_core/expiry_date",
            "cds/exposure/granular/vessels/ship_building_rating/ship_building_vessels_list/ship_building_number_of_vessels",
            "cds/exposure/granular/vessels/ship_building_rating/ship_building_vessels_list/ship_building_total_months_steel_cutting_keel_laying",
            "cds/exposure/granular/vessels/ship_building_rating/ship_building_vessels_list/ship_building_total_months_keel_laying_launch",
            "cds/exposure/granular/vessels/ship_building_rating/ship_building_vessels_list/ship_building_total_months_launch_delivery",
            "cds/exposure/granular/vessels/ship_building_rating/ship_building_vessels_list/ship_building_total_months_all_stages",
            "cds/exposure/granular/vessels/ship_building_rating/ship_building_vessels_list/ship_building_sum_insured",
            "cds/exposure/granular/vessels/ship_building_rating/ship_building_vessels_list/ship_building_vessel_type",
            "cds/exposure/granular/vessels/ship_building_rating/ship_building_vessels_list/ship_building_country",
            "cds/exposure/granular/vessels/ship_building_rating/ship_building_vessels_list/ship_building_survey_grade",
            "cds/exposure/granular/vessels/ship_building_rating/ship_building_vessels_list/ship_building_deductible",
            "cds/layers/coverages/ship_building/ship_building_is_war_cover",
            "cds/experience_rating/ship_building/data_input_experience_table/previous_insurer",
            "cds/experience_rating/ship_building/data_input_experience_table/number_of_vessels",
            "cds/experience_rating/ship_building/data_input_experience_table/premium",
            "cds/experience_rating/ship_building/data_input_experience_table/acquisition_cost",
            "cds/experience_rating/ship_building/data_input_experience_table/total_incurred_shared_line",
            "cds/experience_rating/ship_building/data_input_experience_table/large_incurred_shared_line",
            "cds/experience_rating/ship_building/data_input_experience_table/signed_line",
            "cds/experience_rating/ship_building/data_input_experience_table/rate_change",
            "cds/experience_rating/ship_building/data_input_experience_table/is_include_year",
            "cds/experience_rating/ship_building/large_load_selection/user_selected/user_number_of_years_expected_large_loss",
            "cds/experience_rating/ship_building/large_load_selection/user_selected/user_average_net_lr_of_large_loss",
        ],
        "risk_characteristics": [],
        "deductible":[],
        "limit": [],
        "terms_conditions": [],
        "brokerage": [
            "cds/layers/coverages/ship_building/brokerage",
            "cds/layers/coverages/ship_building/other_deductions",
        ],
        "other": [],
    }

    return (
        hull_rating_buckets,
        iv_buckets,
        war_buckets,
        loh_buckets,
        ship_builders_buckets,
    )


def rate_rate_change(hxd):

    layer, cvg = one_layer(hxd)
    # For layers not used in the pricing summary, the rate change is hidden
    num_layers = len(hxd.cds.layers)
    # Define conditions for function to run
    has_expiring_data = False

    hxd_coverages = []
    rc_hxd_coverages = []
    expiring_hxd_coverages = []
    coverages_list = []
    if hxd.non_cds.show_hide_toggles.hull.show_hull_coverage:
        coverages_list.append("hull")
        if hxd.non_cds.show_hide_toggles.iv.show_iv_coverage:
            coverages_list.append("iv")
        if hxd.non_cds.show_hide_toggles.war.show_war_coverage:
            coverages_list.append("war")
    elif hxd.non_cds.show_hide_toggles.loh.show_loh_coverage:
        coverages_list.append("loh")
    elif hxd.non_cds.show_hide_toggles.ship_building.show_ship_building_coverage:
        coverages_list.append("ship_building")

    for coverage_name in coverages_list:
        rc = getattr(layer.rate_change, coverage_name)

        hxd.cds.rate_change.expiring_policy_option_id.calculated = (
            hx.meta.expiring_policy_option_id
        )

        # --- Continue with the rate change calculation - calculate Beazley share premium
        hxd_coverages.append(getattr(cvg, coverage_name))
        rc_hxd_coverages.append(getattr(layer.rate_change, coverage_name))
        expiring_hxd_coverages.append(rc.expiring_policy_info)
        has_expiring_data = has_expiring_data or (
            (rc.expiring_policy_info.expiring_premium is not None)
            and (rc.expiring_policy_info.expiring_written_line is not None)
        )

    if not has_expiring_data:
        if hxd.cds.standard_fields.is_renewal:
            hx.errors.validation(
                "Rate change must be calculated in the Rate Change page. Click on 'Fetch Expiring Data' then 'Calculate Rate Change'"
            )
        return

    for index in range(1, max_layers + 1):
        (
            setattr(hxd.cds.rate_change, f"show_layer_{index}", True)
            if index <= num_layers
            else False
        )

    # Initialise conditions for premium change check
    are_changes_calculated = True
    is_bm_different = False
    is_quoted_different = False
    is_bm_zero = False
    is_quoted_zero = False

    for cvg, rc_cvg, exp_cvg in zip(
        hxd_coverages, rc_hxd_coverages, expiring_hxd_coverages
    ):
        written_line = (
            cvg.written_line.selected
            if is_hx_class(cvg.written_line)
            else cvg.written_line
        )
        rc_cvg.premium_policy_term_100pct.renewal = (
            cvg.quoted_premium_pro_rated_100pct or 0
        )
        rc_cvg.premium_policy_term_beazley_share.renewal = (
            rc_cvg.premium_policy_term_100pct.renewal or 0
        ) * (written_line or 0)

        rc_cvg.premium_policy_term_100pct.expiring = exp_cvg.expiring_premium or 0
        rc_cvg.premium_policy_term_beazley_share.expiring = (
            exp_cvg.expiring_premium or 0
        ) * (exp_cvg.expiring_written_line or 0)

        rc_cvg.written_line.expiring = exp_cvg.expiring_written_line or 0
        rc_cvg.written_line.renewal = written_line or 0

        rc_cvg.benchmark_premium.expiring = exp_cvg.expiring_benchmark_premium or 0
        rc_cvg.benchmark_premium.renewal = cvg.benchmark_premium_pro_rated_100pct or 0

        rc_cvg.bpi.expiring = exp_cvg.expiring_bpi or 0
        rc_cvg.bpi.renewal = cvg.bpi or 0

        # Calculate change for each bucket - NOTE: use annualised premium for consistency
        rebased_premium_model = rebased_premium_uw = exp_cvg.expiring_premium or 0
        quoted_premium = cvg.quoted_premium_annualised_100pct or 0

        # Calculate UW overrides
        for item in [
            "exposure_change",
            "risk_characteristics_change",
            "deductible_change",
            "limit_change",
            "terms_conditions_change",
            "other_change",
            "brokerage_change",
        ]:
            rc_vbl = getattr(rc_cvg, item)
            rc_vbl.uw_selected.calculated = rc_vbl.model_calculated
            rebased_premium_model *= rc_vbl.model_calculated or 0
            rebased_premium_uw *= rc_vbl.uw_selected.selected or 0

            # Validate overrides if unexplained
            if rc_vbl.uw_selected.is_overridden is True and rc_vbl.comments is None:
                hx.errors.validation(
                    f"Rate Change: {(title_rc(item))} has been overridden and no comment provided"
                )

            # Check all changes are calculated
            are_changes_calculated = are_changes_calculated and (
                rc_vbl.uw_selected.selected is not None
            )

        # Calculate final rate change with overrides
        renewal_premium = quoted_premium

        model_rarc = ratio(renewal_premium, rebased_premium_model, 1)
        final_rarc = ratio(renewal_premium, rebased_premium_uw, 1)

        rc_cvg.rate_change.model_calculated = model_rarc
        rc_cvg.risk_adjusted_rate_change_uw_selected.uw_selected = (
            rc_cvg.rate_change.uw_selected
        ) = final_rarc

        # For PMD reporting
        brokerage_change = rc_cvg.brokerage_change.model_calculated or 1
        rc_cvg.risk_adjusted_rate_change_gross_for_reporting = final_rarc * brokerage_change

        # Determine condition to run calcs again - NOTE: premium in temp storage is annualised
        is_current_bm_different = rc_cvg.temp_storage.benchmark_premium and (
            cvg.benchmark_premium_policy_term_100pct
            != rc_cvg.temp_storage.benchmark_premium
        )
        is_current_quoted_different = rc_cvg.temp_storage.quoted_premium and (
            cvg.quoted_premium_policy_term_100pct != rc_cvg.temp_storage.quoted_premium
        )

        is_bm_different = is_bm_different or is_current_bm_different
        is_quoted_different = is_quoted_different or is_current_quoted_different
        is_quoted_zero = (rc_cvg.premium_policy_term_100pct.renewal == 0) or (
            rc_cvg.premium_policy_term_100pct.expiring == 0
        )
        is_bm_zero = (rc_cvg.benchmark_premium.renewal == 0) or (
            rc_cvg.benchmark_premium.expiring == 0
        )
    
    # Show vessel duplication error if exists
    if hxd.non_cds.show_hide_toggles.hull.show_duplicate_vessel_warning:
        hxd.cds.rate_change.rarc_run_again_message = (
            "Duplicate Vessel's IMO and Name exists"
        )
        hxd.cds.rate_change.rarc_message_show = True

    # Prompt user to run calcs again if premium changes
    if is_quoted_zero:
        if hxd.cds.rate_change.rarc_run_again_message is None:
            hxd.cds.rate_change.rarc_run_again_message = (
                "Expiring or Renewal Quoted Premium is 0"
            )
        else:
            hxd.cds.rate_change.rarc_run_again_message += (
                "\nExpiring or Renewal Quoted Premium is 0"
            )
        hxd.cds.rate_change.rarc_message_show = True
    if is_bm_zero:
        if hxd.cds.rate_change.rarc_run_again_message is None:
            hxd.cds.rate_change.rarc_run_again_message = (
                "Expiring or Renewal Benchmark Premium is 0"
            )
        else:
            hxd.cds.rate_change.rarc_run_again_message += (
                "\nExpiring or Renewal Benchmark Premium is 0"
            )
        hxd.cds.rate_change.rarc_message_show = True
    if is_bm_different or is_quoted_different:
        if hxd.cds.rate_change.rarc_run_again_message is None:
            hxd.cds.rate_change.rarc_run_again_message = "Benchmark or quoted premiums have changed. Please run the rate change calculation again."
        else:
            hxd.cds.rate_change.rarc_run_again_message += "\nBenchmark or quoted premiums have changed. Please run the rate change calculation again."
        hxd.cds.rate_change.rarc_message_show = True
        hx.errors.validation(
            "'Calculate Rate Change' in the Rate Change page must be run again."
        )
        return
    
    hxd.cds.rate_change.rarc_note_for_uw = ("The RARC model calculation does not incorporate the impact of Other Deductions (e.g. Profit Commission).\n\n Please input this impact manually in the 'UW Selected' column within the Other bucket.")
    is_ship_building = hxd.non_cds.show_hide_toggles.ship_building.show_ship_building_coverage
    hxd.non_cds.show_hide_toggles.rate_change.show_rarc_note_for_uw = not is_ship_building

    # Map coverage labels to their corresponding coverage types
    coverage_mapping = {
        "hull": hxd.non_cds.show_hide_toggles.hull.show_hull_coverage,
        "iv": hxd.non_cds.show_hide_toggles.iv.show_iv_coverage,
        "war": hxd.non_cds.show_hide_toggles.war.show_war_coverage,
        "loh": hxd.non_cds.show_hide_toggles.loh.show_loh_coverage,
        "ship_building": hxd.non_cds.show_hide_toggles.ship_building.show_ship_building_coverage,
    }

    # Iterate through the coverage mapping
    for coverage, is_toggled in coverage_mapping.items():
        if is_toggled:
            rc = getattr(layer.rate_change, coverage, None)
            if rc is not None:
                rc.rarc_calcs_show = True
                hxd.non_cds.show_hide_toggles.rate_change.show_generate_output_summary_button = (
                    True
                )
                # Show warning message for rate change

    # Raise validation error if changes are not calculated
    if not (is_quoted_zero or is_bm_zero or are_changes_calculated):
        if hxd.cds.rate_change.rarc_run_again_message is None:
            hxd.cds.rate_change.rarc_run_again_message = "Rate change must be calculated. Click on 'Calculate Rate Change' or override values manually in the 'UW Selected'"
        else:
            hxd.cds.rate_change.rarc_run_again_message += "\nRate change must be calculated. Click on 'Calculate Rate Change' or override values manually in the 'UW Selected'"
        hxd.cds.rate_change.rarc_message_show = True
        hx.errors.validation(
            "Rate change must be calculated in the Rate Change page. Click on 'Calculate Rate Change' or override values manually in the 'UW Selected'"
        )
