import hx
import pandas as pd
import numpy as np
import math as math
import json
from algorithms.rate_utilities import title_rc, ratio
from operator import itemgetter
from algorithms.rate_constants import max_layers

def rate_change_buckets(hxd):

    buckets = {
        "model": [], # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": [
            "cds/layers/coverages/eb/tiv/value",
            "cds/exposure/granular/paf/specific_schedules_structure/cameras_scheduled_professional_use/tiv",
            "cds/exposure/granular/paf/specific_schedules_structure/cameras_scheduled_personal_use/tiv",
            "cds/exposure/granular/paf/specific_schedules_structure/cameras_blanket/tiv",
            "cds/exposure/granular/paf/specific_schedules_structure/fine_art_scheduled_non_fragile/tiv",
            "cds/exposure/granular/paf/specific_schedules_structure/fine_art_scheduled_fragile/tiv",
            "cds/exposure/granular/paf/specific_schedules_structure/fine_art_blanket/tiv",
            "cds/exposure/granular/paf/specific_schedules_structure/gold_silver_bullion_bank_vault/tiv",
            "cds/exposure/granular/paf/specific_schedules_structure/gold_silver_bullion_home_safe/tiv",
            "cds/exposure/granular/paf/specific_schedules_structure/golf_clubs_scheduled/tiv",
            "cds/exposure/granular/paf/specific_schedules_structure/golf_clubs_scheduled_golf_carts_excluding_collision/tiv",
            "cds/exposure/granular/paf/specific_schedules_structure/jewellery_watches_scheduled_jewellery/tiv",
            "cds/exposure/granular/paf/specific_schedules_structure/jewellery_watches_scheduled_watches/tiv",
            "cds/exposure/granular/paf/specific_schedules_structure/jewellery_watches_scheduled_jewellery_watches_bank_vault_only/tiv",
            "cds/exposure/granular/paf/specific_schedules_structure/jewellery_watches_blanket/tiv",
            "cds/exposure/granular/paf/specific_schedules_structure/musical_instruments_scheduled_professional_use/tiv",
            "cds/exposure/granular/paf/specific_schedules_structure/musical_instruments_scheduled_personal_use/tiv",
            "cds/exposure/granular/paf/specific_schedules_structure/musical_instruments_blanket/tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/antique_furniture/scheduled_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/baseball_sports_cards_and_comic_books/scheduled_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/books/scheduled_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/coins/scheduled_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/furs/scheduled_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/guns/scheduled_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/handbags/scheduled_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/memorabilia/scheduled_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/rugs/scheduled_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/silverware/scheduled_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/stamps/scheduled_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/wine_and_cigars/scheduled_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/audio_visual_equipment/scheduled_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/bicycles/scheduled_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/computers/scheduled_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/misc/scheduled_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/antique_furniture/blanket_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/baseball_sports_cards_and_comic_books/blanket_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/books/blanket_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/coins/blanket_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/furs/blanket_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/guns/blanket_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/handbags/blanket_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/memorabilia/blanket_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/rugs/blanket_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/silverware/blanket_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/stamps/blanket_tiv",
            "cds/exposure/granular/paf/scheduled_and_blanket_coverages_structure/wine_and_cigars/blanket_tiv",
            "cds/exposure/granular/paf/my_dis_coverage/tiv",
            "cds/exposure/granular/paf/wearing_limit",
        ],
        "risk_characteristics": [
            "cds/rating_factors/street_number",
            "cds/rating_factors/street_name",
            "cds/rating_factors/zip",
            "cds/rating_factors/city",
            "cds/rating_factors/state",
            "cds/rating_factors/county",
            "cds/rating_factors/distance_to_coast_options",
            "cds/rating_factors/building_occupancy",
            'cds/rating_factors/construction_type',
            'cds/rating_factors/year_built',
            'cds/rating_factors/ppc',
            'cds/rating_factors/roof_type',
            'cds/rating_factors/roof_year',
            "cds/rating_factors/square_foot",
            "cds/rating_factors/number_of_units",
            "cds/rating_factors/basement",
            "cds/rating_factors/roof_shape",
            "cds/rating_factors/number_of_storeys",
            "cds/rating_factors/fire_alarm",
            "cds/rating_factors/burglar_alarm",
            "cds/rating_factors/sprinkler",
            'cds/rating_factors/updated_roof_year',
            "cds/rating_factors/updated_wiring_year",
            "cds/rating_factors/updated_plumbing_year",
            "cds/rating_factors/updated_heating_year",
            "cds/experience_rating/coverages/aop/number_of_losses",
            "cds/experience_rating/coverages/wildfire/number_of_losses",
            "cds/experience_rating/coverages/liability/number_of_losses",
            "cds/experience_rating/coverages/eb/number_of_losses",
            "cds/experience_rating/coverages/fl/number_of_losses",
            "cds/experience_rating/coverages/ws/number_of_losses",
            "cds/experience_rating/coverages/eq/number_of_losses",
            "cds/rating_factors/insured_occupation",
            "cds/rating_factors/high_profile_client",
            "cds/rating_factors/safe",
            "cds/rating_factors/credit_score",
            "cds/exposure/granular/paf/paid_claims_amount_last_five_years",
            "cds/exposure/granular/paf/single_item_limit",
            "cds/exposure/granular/paf/based_in_nyc_metro_area"
        ],
        "deductible": [
            "cds/layers/excess",
            "cds/layers/deductible",
            "cds/layers/coverages/aop/deductible",
            "cds/layers/coverages/aop/water_damage_deductible",
            'cds/layers/coverages/wildfire/deductible',
            'cds/layers/coverages/eb/deductible',
            'cds/layers/coverages/ws/deductible',
            'cds/layers/coverages/ws/deductible_type/value',
            'cds/layers/coverages/ws/deductible_all_perils',
            'cds/layers/coverages/eq/deductible',
            'cds/layers/coverages/paf/deductible'
        ],
        "limit": [
            "cds/layers/limit",
            "cds/layers/coverage_a_building_limit",
            "cds/layers/coverage_b_other_structures_limit",
            "cds/layers/coverage_c_personal_property_limit",
            "cds/layers/coverage_d_loss_of_use_limit",
            "cds/layers/coverage_l_liability_limit",
            "cds/layers/coverage_m_med_pay_limit",
            "cds/layers/sublimits/animal",
            "cds/layers/sublimits/diving_board_and_pool",
            "cds/layers/sublimits/trampoline",
            "cds/layers/sublimits/swimming_pool",
            "cds/layers/sublimits/premises_only",
            "cds/layers/coverages/aop/water_damage_sublimit",
        ],
        "terms_conditions": [
            "hx_core/inception_date",
            "hx_core/expiry_date",
            "cds/rating_factors/product_line",
            "cds/layers/coverages/aop/include_peril/value",
            'cds/layers/coverages/wildfire/include_peril/value',
            'cds/layers/coverages/eb/include_peril/value',
            'cds/layers/coverages/fl/include_peril/value',
            'cds/layers/coverages/ws/include_peril/value',
            'cds/layers/coverages/eq/include_peril/value',
            'cds/layers/coverages/paf/include_peril/value',
            "cds/exposure/granular/paf/my_dis_coverage/include",
            "cds/exposure/granular/paf/my_dis_coverage/engagement_ring",
        ],
        "other": [
            "cds/standard_fields/broker",
            "cds/layers/brokerage",
            "cds/number_of_options",
            "cds/option_to_show",
            "cds/option_to_bind",
            "cds/standard_fields/rating_methodology",
            #"cds/layers/kpis/total/commercial_premium/premium",
            #"cds/layers/kpis/total/commercial_premium/rate",
            "cds/layers/kpis/hvh/commercial_premium/premium",
            "cds/layers/kpis/hvh/commercial_premium/rate",
            "cds/layers/kpis/paf/commercial_premium/premium",
            "cds/layers/kpis/paf/commercial_premium/rate",
        ]
    }

    return buckets

def rate_rate_change(hxd):

    layers = hxd.cds.layers
    rc = hxd.cds.rate_change
    rc.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id
    expiring_policy_option_id = hx.meta.expiring_policy_option_id
    bound_count = 0
    for k,layer in enumerate(hxd.cds.layers,start=1):
        if layer.status in ["Bound"]:
            bound_count += 1
    if bound_count != 1:
        #hx.errors.validation("Please select 1 bound option.")
        return
    
    # For layers not used in the pricing summary, the rate change is hidden
    num_layers = len(layers)
    for index in range(1,max_layers+1):
        setattr(hxd.cds.rate_change, f"show_layer_{index}", True) if index <= num_layers else False
    
    for idx, layer in enumerate(layers):        
        
        rc_prem = layer.rate_change.premium
        # Add renewal premium to table - NOTE: this assumes 'quoted_premium' is annualised 
        layer.quoted_premium = layer.quoted_premium or 0
        rc_prem.line_100pct.annualised.renewal = layer.quoted_premium
        rc_prem.beazley_line.annualised.renewal = layer.quoted_premium * (layer.written_line or 0)
        
        # Calculate change for each bucket
        rebased_premium_model = rebased_premium_uw = rc_prem.line_100pct.annualised.expiring or 0

        # Initialise list to check all changes are filled in
        rate_changes = []

        for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
            # Calculate rebased premium based on % changes
            rc_vbl = getattr(layer.rate_change, item)
            rc_vbl.uw_selected.calculated = rc_vbl.model_calculated
            rebased_premium_model *= rc_vbl.model_calculated or 0
            rebased_premium_uw *= rc_vbl.uw_selected.selected or 0

            # Add selected change to list
            rate_changes.append(rc_vbl.uw_selected.selected)
            
            # Validate overrides if unexplained
            if rc_vbl.uw_selected.is_overridden is True and rc_vbl.comments is None:
                hx.errors.validation(f"Rate Change: {(title_rc(item))} has been overridden and no comment provided")

        # Calculate final rate change with overrides
        renewal_premium = layer.quoted_premium

        model_rarc = ratio(renewal_premium, rebased_premium_model, 1)
        final_rarc = ratio(renewal_premium, rebased_premium_uw, 1)

        layer.rate_change.rate_change.model_calculated = model_rarc
        layer.rate_change.risk_adjusted_rate_change = layer.rate_change.rate_change.uw_selected = final_rarc

        # Valildation to ensure rate change is completed for bound layers
        # Remove rate change validation error as headless integration can't trigger aysnc tasks.
        # if hxd.cds.standard_fields.is_rater_priced:
        #     if any(change is None for change in rate_changes) and layer.status in ["Bound", "Post Bind Complete", "Bound MTA"]:
        #         hx.errors.validation(f"Rate Change: Rate change must be completed for bound layer {idx+1}")
        # if hxd.cds.standard_fields.is_case_priced:
        #     if layer.rate_change.risk_adjusted_rate_change_case_priced is None and layer.status in ["Bound", "Post Bind Complete", "Bound MTA"]:
        #         hx.errors.validation(f"Rate Change: Rate change must be completed for bound layer {idx+1}")

    # Validate layer mapping
    current_mapping = {}
    for idx, layer in enumerate(layers):
        current_mapping[str(idx+1)] = layer.rate_change.expiring_layer 

    previous_mapping = json.loads(rc.layer_mapping) if rc.layer_mapping else current_mapping
    if current_mapping != previous_mapping:
        hx.errors.validation("Rate change: Mapping of Expiring Layers to Renewal Layers is inconsistent with numbers shown in Rate Change")

        task = "'Calculate Rate Change'" if rc.has_rarc_run else "'Fetch Expiring Data'"
        rc.rarc_run_again_message = f"❗ Mapping of Expiring Layers to Renewal Layers has changed. Run {task} again ❗"
        rc.rarc_message_show = True
        
        return # Do not validate any further until the task is run again

    # Validate premiums
    if not rc.has_rarc_run:
        return

    for idx, layer in enumerate(layers):
        if idx == hxd.cds.option_to_bind_zero_indexed:
            is_bm_different = (layer.benchmark_premium_annualised != layer.rate_change.temp_storage.benchmark_premium)
            is_quoted_different = (layer.quoted_premium_annualised != layer.rate_change.temp_storage.quoted_premium)

            if is_bm_different and is_quoted_different:
                rc.rarc_run_again_message = "❗ Benchmark and quoted premiums have changed. Run the rate change calculation again ❗"
                rc.rarc_message_show = True
                break
            elif is_bm_different:
                rc.rarc_run_again_message = f"❗ Benchmark premium has changed on Layer {idx+1}. Run the rate change calculation again ❗"
                rc.rarc_message_show = True
                break
            elif is_quoted_different:
                rc.rarc_run_again_message = f"❗ Quoted premium has changed on Layer {idx+1}. Run the rate change calculation again ❗"
                rc.rarc_message_show = True
                break

    if is_bm_different or is_quoted_different:
        hx.errors.validation("'Calculate Rate Change' in the Rate Change page must be run again.")
        