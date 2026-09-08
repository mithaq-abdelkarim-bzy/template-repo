import hx
import pandas as pd
import numpy as np
import math as math
import json
import algorithms.rate_utilities as utils
from operator import itemgetter
from datetime import date
from algorithms.rate_constants import max_layers
from algorithms.rate_utilities import ratio, one_layer, date_to_string
from algorithms.data_schema.sch_rater_defined import coverages_dict

def save_lists_for_rate_change(hxd):
    expo = hxd.cds.exposure.granular

    airlines_list = [{
        "achieved_hull_rate": {
            "calculated": a.achieved_hull_rate.calculated,
            "override": a.achieved_hull_rate.override,
            "is_overridden": a.achieved_hull_rate.is_overridden,
            "selected": a.achieved_hull_rate.selected
        },
        "aircraft_master_series": a.aircraft_master_series,
        "aircraft_status": a.aircraft_status,
        "attachment_date": date_to_string(a.attachment_date),
        "attachment_date_check": a.attachment_date_check,
        "build_year": a.build_year, 
        "build_year_check": a.build_year_check,
        "coverage": a.coverage,
        "expiry_date": date_to_string(a.expiry_date),
        "expiry_date_check": a.expiry_date_check,
        "has_error": a.has_error,
        "hull_ccy": a.hull_ccy,
        "hull_excess": a.hull_excess,
        "hull_excess_check": a.hull_excess_check,
        "hull_limit": a.hull_limit,
        "hull_limit_check": a.hull_limit_check,
        "include": a.include,
        "liability_ccy": a.liability_ccy,
        "liability_excess": a.liability_excess,
        "liability_excess_check": a.liability_excess_check,
        "liability_limit": a.liability_limit,
        "liability_limit_check": a.liability_limit_check,
        "market_class": a.market_class,
        "no_of_aircraft": a.no_of_aircraft,
        "no_of_aircraft_check": a.no_of_aircraft_check,
        "operating_mtow_lb": a.operating_mtow_lb,
        "operating_mtow_lb_check": a.operating_mtow_lb_check,
        "operator": a.operator,
        "operator_country": a.operator_country,
        "operator_region": a.operator_region,
        "pll_award": {
            "calculated": a.pll_award.calculated,
            "override": a.pll_award.override,
            "is_overridden": a.pll_award.is_overridden,
            "selected": a.pll_award.selected
        },
        "pll_award_check": a.pll_award_check,
        "previous12_months_hours": a.previous12_months_hours,
        "previous12_months_hours_check": a.previous12_months_hours_check,
        "primary_usage": a.primary_usage,
        "registration": a.registration,
        "russian_built": a.russian_built,
        "time_in_service": a.time_in_service,
        "time_in_service_check": a.time_in_service_check,
        "total_seats": a.total_seats,
        "total_seats_check": a.total_seats_check,
        "tpl_limit_exposed": {
            "calculated": a.tpl_limit_exposed.calculated,
            "override": a.tpl_limit_exposed.override,
            "is_overridden": a.tpl_limit_exposed.is_overridden,
            "selected": a.tpl_limit_exposed.selected
        },
        "usage": a.usage,
        "value": a.value,
        "value_check": a.value_check
    } for a in expo.airlines]

    aircrafts_list = [{
        "achieved_hull_rate": {
            "calculated": a.achieved_hull_rate.calculated,
            "override": a.achieved_hull_rate.override,
            "is_overridden": a.achieved_hull_rate.is_overridden,
            "selected": a.achieved_hull_rate.selected
        },
        "aircraft_class": a.aircraft_class,
        "aircraft_master_series": a.aircraft_master_series,
        "attachment_date": date_to_string(a.attachment_date),
        "attachment_date_check": a.attachment_date_check,
        "bm_allocated_hull_premium": a.bm_allocated_hull_premium,
        "bm_allocated_liab_premium": a.bm_allocated_liab_premium,
        "build_location": a.build_location,
        "build_year": a.build_year, # FS 27/08/2025: added build year to rate change algorithm
        "combined_single_limit": a.combined_single_limit,
        "combined_single_limit_check": a.combined_single_limit_check,
        "crew_seats": a.crew_seats,
        "crew_seats_check": a.crew_seats_check,
        "expiry_date": date_to_string(a.expiry_date),
        "expiry_date_check": a.expiry_date_check,
        "fatality": a.fatality,
        "has_error": a.has_error,
        "hull_benchmark_rate": a.hull_benchmark_rate,
        "hull_ccy": a.hull_ccy,
        "include": a.include,
        "liability_ccy": a.liability_ccy,
        "no_of_aircraft": a.no_of_aircraft,
        "no_of_aircraft_check": a.no_of_aircraft_check,
        "operator": a.operator,
        "operator_country": a.operator_country,
        "operator_region": a.operator_region,
        "pax_liab_benchmark_per_seat": a.pax_liab_benchmark_per_seat,
        "pax_net_worth": a.pax_net_worth,
        "per_occ_deductible": {
            "calculated": a.per_occ_deductible.calculated,
            "override": a.per_occ_deductible.override,
            "is_overridden": a.per_occ_deductible.is_overridden,
            "selected": a.per_occ_deductible.selected
        },
        "per_occ_deductible_check": a.per_occ_deductible_check,
        "per_occ_deductible_pct": a.per_occ_deductible_pct,
        "per_occ_deductible_pct_check": a.per_occ_deductible_pct_check,
        "per_pax_liab_limit": a.per_pax_liab_limit,
        "per_pax_liab_limit_check": a.per_pax_liab_limit_check,
        "registration": a.registration,
        "renewing_aircraft": a.renewing_aircraft,
        "seat_occupancy": a.seat_occupancy,
        "time_in_service": a.time_in_service,
        "time_in_service_check": a.time_in_service_check,
        "total_hull_benchmark": a.total_hull_benchmark,
        "total_liab_benchmark": a.total_liab_benchmark,
        "total_seats": a.total_seats,
        "total_seats_check": a.total_seats_check,
        "tpl_benchmark": a.tpl_benchmark,
        "tpl_limit_exposed": a.tpl_limit_exposed,
        "tpl_limit_exposed_check": a.tpl_limit_exposed_check,
        "use": a.use,
        "value": a.value,
        "value_check": a.value_check
    } for a in expo.aircrafts]
    
    hxd.rate_change.airlines = json.dumps(airlines_list)
    hxd.rate_change.aircrafts = json.dumps(aircrafts_list)


def rate_change_buckets(hxd):

    ### --- GENERAL AVIATION --- ###
    if hxd.cds.is_ga:
        hull_buckets = {
            "model": [
                # Add policy dates for correct parameter to be looked up
                "hx_core/inception_date",
                "hx_core/expiry_date",
            ], # Start from expiry data priced with current model
            "exposure": [
                "cds/policy_info/term",
                "cds/layers/coverages/hull/quoted_premium", # Should be consistent with term

                "cds/exposure/granular/fleet_size", # YZ: Used to be in Risk Characteristic but is moved to Exposure Bucket. Override: This is a discount factor of exposure size.
                "cds/exposure/granular/aircrafts/include",
                "cds/exposure/granular/aircrafts/registration", # Including registration so fleet size is calculated correctly
                "cds/exposure/granular/aircrafts/no_of_aircraft",
                "cds/exposure/granular/aircrafts/value",
                "cds/exposure/granular/aircrafts/hull_ccy",
                "cds/exposure/granular/aircrafts/attachment_date",
                "cds/exposure/granular/aircrafts/expiry_date",
                "cds/exposure/granular/aircrafts/achieved_hull_rate", # Doesn't affect rating, here to avoid deletion of overrides when running rarc_task
            ],
            "risk_characteristics": [
                "cds/exposure/granular/aircrafts/aircraft_class", # YZ: Used to be in exposure for additional aircraft and now is moved to risk characteristic      
                "cds/exposure/granular/aircrafts/build_location",
                "cds/exposure/granular/aircrafts/build_year", # FS 27/08/2025: added build year to rate change algorithm
                "cds/exposure/granular/aircrafts/operator_country",
                "cds/exposure/granular/aircrafts/use",
                "cds/exposure/granular/aircrafts/time_in_service"
            ],
            "deductible": [
                "cds/exposure/granular/aircrafts/per_occ_deductible_pct",
                "cds/exposure/granular/aircrafts/per_occ_deductible",
            ],
            "limit": [],
            "terms_conditions": [],
            "brokerage": [
                "cds/layers/coverages/hull/brokerage"
            ],
            "other": [
                # UW Adjustments
                "cds/layers/pilot_uw_adj",
                "cds/layers/coverages/hull/uw_adj",
                # Experience Rating
                "cds/experience_rating/claims_available",
                "cds/experience_rating/as_at_date",
                "cds/experience_rating/historic_premium_known",
                "cds/experience_rating/claims/yoa",
                "cds/experience_rating/claims/years_to_inception",
                "cds/experience_rating/claims/hull_attr_claims",
                "cds/experience_rating/claims/hull_large_losses",
                "cds/experience_rating/claims/hull_gross_premium",
                "cds/experience_rating/claims/hull_exposure_adj",
                "cds/experience_rating/claims/hull_rate_change"
            ]
        }

        liab_buckets = {
            "model": [
                # Add policy dates for correct parameter to be looked up
                "hx_core/inception_date",
                "hx_core/expiry_date",
            ], # Start from expiry data priced with current model
            "exposure": [
                "cds/policy_info/term",
                "cds/layers/coverages/liability/quoted_premium", # Should be consistent with term
                
                "cds/exposure/granular/fleet_size", # YZ: Moved from the Risk Characteristic to Exposure. Override
                "cds/exposure/granular/aircrafts/include",
                "cds/exposure/granular/aircrafts/registration", # Including registration so fleet size is calculated correctly
                "cds/exposure/granular/aircrafts/no_of_aircraft",
                "cds/exposure/granular/aircrafts/liability_ccy",
                "cds/exposure/granular/aircrafts/attachment_date",
                "cds/exposure/granular/aircrafts/expiry_date",
                # PAX
                "cds/exposure/granular/aircrafts/total_seats",
                "cds/exposure/granular/aircrafts/crew_seats",
                "cds/exposure/granular/aircrafts/pax_net_worth",
                # TPL
                "cds/exposure/granular/aircrafts/combined_single_limit", # Despite being a limit, it effectively determines the TPL exposure
                "cds/exposure/granular/aircrafts/tpl_limit_exposed"
            ],
            "risk_characteristics": [
                "cds/exposure/granular/aircrafts/aircraft_class", # YZ: Moved away from Exposure Bucket to Risk Characteristic. Putting class here so that frequency is calculated
                "cds/exposure/granular/aircrafts/time_in_service", # YZ: Moved away from Exposure Bucket to Risk Characteristic. 
                "cds/exposure/granular/aircrafts/operator_country", # YZ: add this in Liability.
                # "cds/exposure/granular/aircrafts/operator_region", # YZ:  Moved away from Exposure Bucket to Risk Characteristics. Calculates fatality rate and seat occupancy
                "cds/exposure/granular/aircrafts/use", # YZ:  Moved away from Exposure Bucket to Risk Characteristic. Calculates fatality rate and seat occupancy
            ],
            "deductible": [],
            "limit":[
                "cds/exposure/granular/aircrafts/per_pax_liab_limit"  # YZ: Moved away from Exposure Bucket to Limit. 
	        ],
            "terms_conditions": [],
            "brokerage": [
                "cds/layers/coverages/liability/brokerage"
            ],
            "other": [
                # UW Adjustments
                "cds/layers/pilot_uw_adj",
                "cds/layers/coverages/liability/uw_adj",
                # Experience Rating
                "cds/experience_rating/claims_available",
                "cds/experience_rating/as_at_date",
                "cds/experience_rating/historic_premium_known",
                "cds/experience_rating/claims/yoa",
                "cds/experience_rating/claims/years_to_inception",
                "cds/experience_rating/claims/liab_attr_claims",
                "cds/experience_rating/claims/liab_large_losses",
                "cds/experience_rating/claims/liab_gross_premium",
                "cds/experience_rating/claims/liab_exposure_adj",
                "cds/experience_rating/claims/liab_rate_change"
            ]
        }

    ### --- AIRLINES --- ###
    else:
        hull_buckets = {
            "model": [
                # Add policy dates for correct parameter to be looked up
                "hx_core/inception_date",
                "hx_core/expiry_date",
            ], # Start from expiry data priced with current model
            "exposure": [
                "cds/policy_info/term",
                "cds/layers/coverages/hull/quoted_premium", # Should be consistent with term

                "cds/exposure/granular/fleet_size", # YZ: Moved from Risk Characteristic to Exposure. Override
                "cds/exposure/granular/airlines/include",
                "cds/exposure/granular/airlines/registration", # Including registration so fleet size is calculated correctly
                "cds/exposure/granular/airlines/no_of_aircraft",
                "cds/exposure/granular/airlines/value",
                "cds/exposure/granular/airlines/hull_ccy",
                "cds/exposure/granular/airlines/attachment_date",
                "cds/exposure/granular/airlines/expiry_date",
                "cds/exposure/granular/airlines/achieved_hull_rate", # Doesn't affect rating, here to avoid deletion of overrides when running rarc_task
            ],
            "risk_characteristics": [
                "cds/exposure/granular/selected_operator_class",
                "cds/exposure/granular/status_split/in_service",
                "cds/exposure/granular/status_split/storage",
                "cds/exposure/granular/status_split/other",
                "cds/exposure/granular/airlines/aircraft_status",
                "cds/exposure/granular/airlines/coverage",
                "cds/exposure/granular/airlines/time_in_service",
                "cds/exposure/granular/airlines/operator_country",
                "cds/exposure/granular/airlines/previous12_months_hours",
                "cds/exposure/granular/airlines/market_class",
                "cds/exposure/granular/airlines/build_year",
                "cds/exposure/granular/airlines/usage",
                "cds/exposure/granular/airlines/russian_built",
		        "cds/exposure/granular/airlines/operating_mtow_lb" #YZ: Add MTOW in the Risk Characteristic bucket.
            ],
            "deductible": [
                "cds/exposure/granular/airlines/hull_excess"
            ],
            "limit":[
	         "cds/exposure/granular/airlines/hull_limit", # YZ: Moved from Exposure Bucket to Limit.
	        ],
            "terms_conditions": [],
            "brokerage": [
                "cds/layers/coverages/hull/brokerage"
            ],
            "other": [
                # UW Adjustments
                "cds/layers/pilot_uw_adj",
                "cds/layers/coverages/hull/uw_adj",
                # Experience Rating
                "cds/experience_rating/claims_available",
                "cds/experience_rating/as_at_date",
                "cds/experience_rating/historic_premium_known",
                "cds/experience_rating/claims/yoa",
                "cds/experience_rating/claims/years_to_inception",
                "cds/experience_rating/claims/hull_attr_claims",
                "cds/experience_rating/claims/hull_large_losses",
                "cds/experience_rating/claims/hull_gross_premium",
                "cds/experience_rating/claims/hull_exposure_adj",
                "cds/experience_rating/claims/hull_rate_change",
            ]
        }
        liab_buckets = {
            "model": [
                # Add policy dates for correct parameter to be looked up
                "hx_core/inception_date",
                "hx_core/expiry_date",
            ], # Start from expiry data priced with current model
            "exposure": [
                "cds/policy_info/term",
                "cds/layers/coverages/liability/quoted_premium", # Should be consistent with term

		        "cds/exposure/granular/fleet_size", # YZ Change from Risk Characteristic to Exposure. Override
                "cds/exposure/granular/airlines/include",
                "cds/exposure/granular/airlines/registration", # Including registration so fleet size is calculated correctly
                "cds/exposure/granular/airlines/no_of_aircraft",
                "cds/exposure/granular/airlines/liability_ccy",
                "cds/exposure/granular/airlines/attachment_date",
                "cds/exposure/granular/airlines/expiry_date",
                # PAX
                "cds/exposure/granular/airlines/total_seats",
                "cds/exposure/granular/airlines/liability_limit", # Despite being a limit, it effectively determines the PAX exposure
                # TPL
                "cds/exposure/granular/airlines/pll_award", # Override
                "cds/exposure/granular/airlines/tpl_limit_exposed" # Override
            ],
            "risk_characteristics": [
                "cds/exposure/granular/status_split/in_service",
                "cds/exposure/granular/status_split/storage",
                "cds/exposure/granular/status_split/other",
                "cds/exposure/granular/airlines/aircraft_status", # YZ: Change from Exposure Bucket to Risk Characteristic.
                # PAX
                "cds/exposure/granular/airlines/usage", # YZ: Move from Exposure to Risk Characteristic. Including usage because it's necessary to calculate TPL loss cost
                "cds/exposure/granular/airlines/build_year",
                "cds/exposure/granular/airlines/operator_country",
                "cds/exposure/granular/airlines/previous12_months_hours",
                "cds/exposure/granular/airlines/market_class",
                "cds/exposure/granular/airlines/time_in_service",
		        "cds/exposure/granular/airlines/operating_mtow_lb" #YZ: Add MTOW in the Risk Characteristic bucket.
                # TPL has no specific risk characteristics factor                
            ],
            "deductible": [
                "cds/exposure/granular/airlines/liability_excess"
            ],
            "limit": [],
            "terms_conditions": [],
            "brokerage": [
                "cds/layers/coverages/liability/brokerage"
            ],
            "other": [
                # UW Adjustments
                "cds/layers/pilot_uw_adj",
                "cds/layers/coverages/liability/uw_adj",
                # Experience Rating
                "cds/experience_rating/claims_available",
                "cds/experience_rating/as_at_date",
                "cds/experience_rating/historic_premium_known",
                "cds/experience_rating/claims/yoa",
                "cds/experience_rating/claims/years_to_inception",
                "cds/experience_rating/claims/liab_attr_claims",
                "cds/experience_rating/claims/liab_large_losses",
                "cds/experience_rating/claims/liab_gross_premium",
                "cds/experience_rating/claims/liab_exposure_adj",
                "cds/experience_rating/claims/liab_rate_change"
            ]
        }

    return hull_buckets, liab_buckets

def rate_rate_change(hxd):

    layer, cvg = one_layer(hxd)
    hull = cvg.hull
    liab = cvg.liability

    rc = layer.rate_change
    rc_hull = rc.hull
    rc_liab = rc.liability

    exp = layer.rate_change.expiring_policy_info
    exp_hull = rc_hull.expiring_policy_info
    exp_liab = rc_liab.expiring_policy_info

    hxd.cds.rate_change.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id

    # Define conditions for function to run
    has_expiring_data = exp.expiring_premium is not None and exp.expiring_written_line is not None

    # Exit if condition is not satisfied
    if not has_expiring_data:
        return

    # For layers not used in the pricing summary, the rate change is hidden
    num_layers = len(hxd.cds.layers)
    for index in range(1, max_layers+1):
        setattr(hxd.cds.rate_change, f"show_layer_{index}", True) if index <= num_layers else False
    
    # --- Continue with the rate change calculation - calculate Beazley share premium
    hxd_coverages = [hull, liab]
    rc_hxd_coverages = [rc_hull, rc_liab]
    expiring_hxd_coverages = [exp_hull, exp_liab]

    # Initialise conditions for premium change check
    are_changes_calculated = True
    is_bm_different = False
    is_quoted_different = False

    for cvg, rc_cvg, exp_cvg in zip(hxd_coverages, rc_hxd_coverages, expiring_hxd_coverages):
        rc_cvg.premium_policy_term_100pct.renewal = cvg.quoted_premium or 0
        rc_cvg.premium_policy_term_beazley_share.renewal = rc_cvg.premium_policy_term_100pct.renewal * cvg.written_line

        rc_cvg.premium_policy_term_100pct.expiring = exp_cvg.expiring_premium
        rc_cvg.premium_policy_term_beazley_share.expiring = exp_cvg.expiring_premium * exp_cvg.expiring_written_line
        
        rc_cvg.written_line.expiring = exp_cvg.expiring_written_line
        rc_cvg.written_line.renewal = cvg.written_line

        rc_cvg.benchmark_premium.expiring = exp_cvg.expiring_benchmark_premium
        rc_cvg.benchmark_premium.renewal = cvg.benchmark_premium

        rc_cvg.benchmark_premium_post_uw_adj.expiring = exp_cvg.expiring_benchmark_premium_post_uw_adj
        rc_cvg.benchmark_premium_post_uw_adj.renewal = cvg.benchmark_premium_post_uw_adj

        rc_cvg.bpi.expiring = exp_cvg.expiring_bpi
        rc_cvg.bpi.renewal = cvg.bpi

        # Calculate change for each bucket - NOTE: use annualised premium for consistency
        rebased_premium_model = rebased_premium_uw = exp_cvg.expiring_premium_annualised or 0
        quoted_premium = cvg.quoted_premium_annualised or 0
        
        # Calculate UW overrides
        for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change", "brokerage_change"]:
            rc_vbl = getattr(rc_cvg, item)
            rc_vbl.uw_selected.calculated = rc_vbl.model_calculated
            rebased_premium_model *= rc_vbl.model_calculated or 0
            rebased_premium_uw *= rc_vbl.uw_selected.selected or 0

            # Validate overrides if unexplained
            if rc_vbl.uw_selected.is_overridden is True and rc_vbl.comments is None:
                hx.errors.validation(f"Rate Change: {(utils.title_rc(item))} has been overridden and no comment provided")

            # Check all changes are calculated
            are_changes_calculated *= (rc_vbl.uw_selected.selected is not None)

        # Calculate final rate change with overrides
        renewal_premium = quoted_premium

        model_rarc = ratio(renewal_premium, rebased_premium_model, 1)
        final_rarc = ratio(renewal_premium, rebased_premium_uw, 1)

        rc_cvg.rate_change.model_calculated = model_rarc
        rc_cvg.risk_adjusted_rate_change.uw_selected = rc_cvg.rate_change.uw_selected = final_rarc

        # Determine condition to run calcs again - NOTE: premium in temp storage is annualised
        is_current_bm_different = rc_cvg.temp_storage.benchmark_premium and (cvg.benchmark_premium_annualised != rc_cvg.temp_storage.benchmark_premium)
        is_current_quoted_different = rc_cvg.temp_storage.quoted_premium and (cvg.quoted_premium_annualised != rc_cvg.temp_storage.quoted_premium)

        is_bm_different = is_bm_different or is_current_bm_different
        is_quoted_different = is_quoted_different or is_current_quoted_different

    # Raise validation error if changes are not calculated
    if not are_changes_calculated:
        hx.errors.validation("Rate change must be calculated in the Rate Change page. Click on 'Calculate Rate Change' or override values manually in the 'UW Selected' column for both Hull and Liability.")

    # Prompt user to run calcs again if premium changes
    term = hxd.cds.policy_info.term
    rarc_message = ""
    rarc_message_show = False

    # Get previus and current premiums - NOTE: premium in temp storage is annualised so need to convert it to policy term
    previous_bm_prem = "{:,.0f}".format(sum([rc_hull.temp_storage.benchmark_premium or 0, rc_liab.temp_storage.benchmark_premium or 0]) * term)
    previous_quoted_prem = "{:,.0f}".format(sum([rc_hull.temp_storage.quoted_premium or 0, rc_liab.temp_storage.quoted_premium or 0]) * term)
    current_bm_prem = "{:,.0f}".format(layer.benchmark_premium or 0)
    current_quoted_prem = "{:,.0f}".format(quoted_premium)

    if is_bm_different and is_quoted_different:
        rarc_message = "Benchmark and quoted premiums have changed. Please run the rate change calculation again."
        rarc_message_show = True
    elif is_bm_different:
        rarc_message = f"Benchmark premium has changed from {previous_bm_prem} to {current_bm_prem}.\nPlease run the rate change calculation again."
        rarc_message_show = True
    elif is_quoted_different:
        rarc_message = f"Quoted premium has changed from {previous_quoted_prem} to {current_quoted_prem}.\nPlease run the rate change calculation again."
        rarc_message_show = True
    
    hxd.cds.rate_change.rarc_run_again_message = rarc_message
    hxd.cds.rate_change.rarc_message_show = rarc_message_show
    hxd.cds.rate_change.rarc_calcs_show = not rarc_message_show

    # Add validation error to prevent policy from being set to final
    if is_bm_different or is_quoted_different:
        hx.errors.validation("'Calculate Rate Change' in the Rate Change page must be run again.")

    # Show warning message for registrations
    hxd.cds.rate_change.show_reg_warning = (hxd.cds.rate_change.reg_warning is not None) and (not rarc_message_show)
        

        



    



