"""
This module processes and rates PAF exposures, including assigning collection 
classes, calculating rates and premiums, applying sliding scale adjustments, 
and computing final model premiums.

It includes:
- **Applying PAF sliding scale discounts** (`apply_paf_sliding_scale`):  
  Adjusts base rates using predefined PAF discount structures.
- **Processing table values** (`calculate_table_values`):  
  Assigns collection classes, retrieves base rates, applies sliding scale 
  adjustments, and calculates totals for each coverage type, including  
  scheduled/blanket and specific schedules coverages.
- **Computing PAF premiums and rates** (`calculate_paf_premiums_and_rates`):  
  Determines base premiums, scheduled/blanket premiums, and applies  
  loss surcharge and Mys Dis coverage impacts.
- **Calculating PAF deductibles and final premiums** (`calculate_paf_deductibles_and_final_premiums`):  
  Adjusts premiums using deductible multipliers, coverage modifiers, paid 
  claims loads, and single-item limit impacts.
- **Main exposure processing function** (`rate_exposure_details`):  
  Runs all calculations in sequence to rate exposures and compute final premiums.
"""

import hx
from algorithms.rate_utilities import get_lookup_value
import algorithms.rate_constants as constants
import numpy as np
from collections import defaultdict

def apply_paf_sliding_scale(exposure, rate, sliding_scale):
    """Applies a discount based on the PAF sliding scale."""
    valid_keys = sliding_scale[sliding_scale["Lookup code"] <= exposure.tiv]
    if valid_keys.empty:
        return 0  # Handle case where value is below the lowest key
    highest_valid_row = valid_keys.iloc[-1]
    return rate - rate * highest_valid_row["PAF"]


def calculate_table_values(hxd):
    """
    Assigns collection classes and coverage types to exposures in specific schedules.
    """
    table_base_rate = hx.params.table_base_rate
    table_nyc_base_rates = hx.params.table_paf_nyc_metro_area_base_rates

    for category, schedule_type, variable_name in constants.specific_schedules_tuples:

        # Get the structure for this exposure
        exposure = getattr(hxd.cds.exposure.granular.paf.specific_schedules_structure, variable_name)

        # Assign category and schedule type
        exposure.coverage_type = schedule_type

        # Get the base rate from lookup
        lookup_key = f"Base Rate{category}{schedule_type}"
        nyc_lookups = table_nyc_base_rates['Lookup Code'].values
        value_match = "Yes" if hxd.cds.exposure.granular.paf.based_in_nyc_metro_area else "No"

        if lookup_key in nyc_lookups:
            multiplier = table_nyc_base_rates[
                (table_nyc_base_rates['Lookup Code'] == lookup_key) &
                (table_nyc_base_rates['Values'] == value_match)
            ]['PAF'].iloc[0]
            initial_rate = get_lookup_value(
                table_base_rate,
                'PAF',
                lookup_key,
                error_behavior='default_value',
                default_value=None
            )
            rate = initial_rate * multiplier

        else:  
            rate = get_lookup_value(
                table_base_rate,
                'PAF',
                lookup_key,
                error_behavior='default_value',
                default_value=None
            )

        # Apply PAF sliding scale for Fine Art and Jewellery & Watches
        if category in ['Fine Art', 'Jewellery & Watches']:
            sliding_scale = (
                hx.params.table_paf_fine_art_sliding_scale
                if category == 'Fine Art'
                else hx.params.table_paf_jewellery_sliding_scale
            )
            exposure.rate = apply_paf_sliding_scale(exposure, rate, sliding_scale)
        else:
            exposure.rate = rate
        
    # Calculate totals
    total_structure = hxd.cds.exposure.granular.paf.specific_schedules_totals_structure
    specific_schedules = hxd.cds.exposure.granular.paf.specific_schedules_structure

    # Calculate total TIV
    total_tiv = sum(schedule.tiv for _, schedule in specific_schedules if hasattr(schedule, "tiv") and schedule.tiv is not None)
    total_structure.tiv = total_tiv

    # Calculate weighted rate
    total_structure.rate = (
        sum(schedule.rate * schedule.tiv for _, schedule in specific_schedules
            if hasattr(schedule, "rate") and hasattr(schedule, "tiv") and schedule.rate is not None and schedule.tiv is not None) / total_tiv
        if total_tiv > 0 else 0
    )

    # Scheduled and blanket coverages    
    for label, variable_name in constants.scheduled_and_blanket_coverages_tuples:

        # Get the structure for this exposure
        exposure = getattr(hxd.cds.exposure.granular.paf.scheduled_and_blanket_coverages_structure,variable_name)

        # Calculate rates for Scheduled Coverage
        lookup_key = f"Base Rate{label}Scheduled"
        exposure.scheduled_rate = get_lookup_value(
            table_base_rate,
            'PAF',
            lookup_key,
            error_behavior='default_value',
            default_value=None
        )

        # Calculate rates for Blanket Coverage (if not excluded)
        if variable_name not in constants.excluded_blanket_variables:
            lookup_key = f"Base Rate{label}Blanket"
            exposure.blanket_rate = get_lookup_value(
                table_base_rate,
                'PAF',
                lookup_key,
                error_behavior='default_value',
                default_value=None
            )

    # Calculate totals
    scheduled_and_blanket_coverages_totals_structure = hxd.cds.exposure.granular.paf.scheduled_and_blanket_coverages_totals_structure
    scheduled_and_blanket_coverages = hxd.cds.exposure.granular.paf.scheduled_and_blanket_coverages_structure

    # Calculate total scheduled TIV
    total_scheduled_tiv = sum(layer.scheduled_tiv for _, layer in scheduled_and_blanket_coverages if layer.scheduled_tiv is not None)
    scheduled_and_blanket_coverages_totals_structure.scheduled_tiv = total_scheduled_tiv

    # Calculate scheduled weighted rate
    scheduled_and_blanket_coverages_totals_structure.scheduled_rate = (
        sum(layer.scheduled_rate * layer.scheduled_tiv for _, layer in scheduled_and_blanket_coverages 
            if layer.scheduled_rate is not None and layer.scheduled_tiv is not None) / total_scheduled_tiv
        if total_scheduled_tiv > 0 else 0
    )

    # Calculate total blanket TIV
    total_blanket_tiv = sum(
        getattr(layer, "blanket_tiv", 0) for _, layer in scheduled_and_blanket_coverages
        if hasattr(layer, "blanket_tiv")
    )
    scheduled_and_blanket_coverages_totals_structure.blanket_tiv = total_blanket_tiv

    # Calculate blanket weighted rate
    scheduled_and_blanket_coverages_totals_structure.blanket_rate = (
        sum(
            getattr(layer, "blanket_rate", 0) * getattr(layer, "blanket_tiv", 0)
            for variable_name, layer in scheduled_and_blanket_coverages
            if variable_name not in constants.excluded_blanket_variables 
            and hasattr(layer, "blanket_rate") and hasattr(layer, "blanket_tiv")
        ) / total_blanket_tiv if total_blanket_tiv > 0 else 0
    )


def calculate_largest_paf_collection_type(hxd):
    """
    Determines the category with the highest total insured value (TIV) 
    from specific schedules and blanket coverages in PAF exposure data. 
    The result is stored in `hxd.cds.exposure.aggregate.paf.largest_collection_type`.
    """
    category_totals = defaultdict(float)

    # Helper function to safely retrieve TIV values
    def get_tiv(structure, key, tiv_attr):
        return getattr(getattr(structure, key, 0), tiv_attr, 0)

    # Process specific schedules
    schedules_structure = hxd.cds.exposure.granular.paf.specific_schedules_structure
    for category, _, key in constants.specific_schedules_tuples:
        category_totals[category] += get_tiv(schedules_structure, key, "tiv")

    # Process scheduled and blanket coverages
    coverages_structure = hxd.cds.exposure.granular.paf.scheduled_and_blanket_coverages_structure
    for category, key in constants.scheduled_and_blanket_coverages_tuples:
        category_totals[category] += get_tiv(coverages_structure, key, "scheduled_tiv")
        category_totals[category] += get_tiv(coverages_structure, key, "blanket_tiv")

    max_category = max(category_totals, key=category_totals.get, default=None)
    hxd.cds.exposure.aggregate.paf.largest_collection_type = max_category



def calculate_paf_premium(collectibles,tiv_attr='tiv',rate_attr='rate'):
    """ A helper function to calculate the PAF premiums from the TIV and Rates """
    tiv = [getattr(collectible,tiv_attr) for _, collectible in collectibles if hasattr(collectible, tiv_attr) and getattr(collectible,tiv_attr) is not None]
    rates = [getattr(collectible,rate_attr) if hasattr(collectible, rate_attr) and getattr(collectible,rate_attr) is not None else 0 for _, collectible in collectibles]
    return np.dot(tiv, rates), tiv, rates


def calculate_paf_premiums_and_rates(hxd):
    """ Calculate the total PAF premiums and rates from the table values """
    paf_aggregate = hxd.cds.exposure.aggregate.paf
    paf_granular = hxd.cds.exposure.granular.paf

    # Calculate total TIV
    paf_aggregate.tiv = (
        paf_granular.scheduled_and_blanket_coverages_totals_structure.scheduled_tiv +
        paf_granular.scheduled_and_blanket_coverages_totals_structure.blanket_tiv +
        paf_granular.specific_schedules_totals_structure.tiv
    )

    # Retrieve the specific schedules structure
    specific_schedules = hxd.cds.exposure.granular.paf.specific_schedules_structure

    # Calculate Specific Schedules Premium
    specific_schedules_premium, specific_schedules_tiv, _ = calculate_paf_premium(specific_schedules)

    # Retrieve the scheduled and blanket coverages structure
    scheduled_coverages = hxd.cds.exposure.granular.paf.scheduled_and_blanket_coverages_structure

    # Calculate Scheduled and Blanket Premium
    scheduled_premium, scheduled_tiv, _ = calculate_paf_premium(scheduled_coverages,'scheduled_tiv','scheduled_rate')
    blanket_coverages = [c for c in scheduled_coverages if hasattr(c[1], "blanket_tiv")]
    blanket_premium, blanket_tiv, _ = calculate_paf_premium(blanket_coverages,'blanket_tiv','blanket_rate')

    # Calculate total base premium
    paf_aggregate.base_premium = specific_schedules_premium + scheduled_premium + blanket_premium

    # Calculate total base rate
    paf_aggregate.base_rate = paf_aggregate.base_premium / paf_aggregate.tiv if paf_aggregate.tiv != 0 else 0

    # Calculate Mys Dis Premium
    mys_dis_coverage_factor = get_lookup_value(
        hx.params.table_paf_mys_dis,
        'PAF',
        'PAFMys DisYes' if paf_granular.my_dis_coverage.include else 'PAFMys DisNo',
    )
    engagement_ring_factor = get_lookup_value(
        hx.params.table_paf_mys_dis,
        'PAF',
        'PAFMys DisEngagement Ring'
    ) if paf_granular.my_dis_coverage.engagement_ring else 0

    max_item_tiv = max(*(specific_schedules_tiv + scheduled_tiv + blanket_tiv))
    mys_dis_tiv_percent_of_max = paf_granular.my_dis_coverage.tiv / max_item_tiv if max_item_tiv != 0 else 0
    paf_granular.my_dis_coverage.base_premium = (
        (mys_dis_coverage_factor + engagement_ring_factor) * mys_dis_tiv_percent_of_max * paf_aggregate.base_premium
    )

    paf_paid_claims_load_dollars = constants.paf_loss_surcharge * paf_granular.paid_claims_amount_last_five_years / 5
    paf_granular.paid_claims_impact = (
        (paf_paid_claims_load_dollars + paf_aggregate.base_premium) / paf_aggregate.base_premium 
        if paf_aggregate.base_premium != 0 else 1
    )

    # Single Item Limit Impact
    paf_granular.single_item_limit_impact = constants.paf_single_item_impact_dict.get(paf_granular.single_item_limit, 1)


def calculate_paf_deductibles_and_final_premiums(hxd):

    paf_granular = hxd.cds.exposure.granular.paf
    paf_aggregate = hxd.cds.exposure.aggregate.paf
    effective_premium =  hxd.cds.exposure.aggregate.paf.base_premium

    for layer in hxd.cds.layers:
        paf_structure = layer.coverages.paf

        # Calculate PAF deductible multiplier
        paf_deductible_multiplier = get_lookup_value(
            hx.params.table_paf_deductible_load,
            'PAF',
            paf_structure.deductible,
            reference_column='Values'
            )
        paf_ded_load = - effective_premium * paf_deductible_multiplier
        max_paf_ded_load = - constants.paf_max_ded_credit * paf_structure.deductible
        capped_ded_load = max(max_paf_ded_load,paf_ded_load)
        paf_structure.deductible_impact = (effective_premium + capped_ded_load)/effective_premium if effective_premium != 0 else 1

        # Calculate modifiers load
        modifiers_load = effective_premium * paf_structure.modifiers_impact.factor - effective_premium

        # Calculate claims load
        paf_paid_claims_load_dollars = constants.paf_loss_surcharge * paf_granular.paid_claims_amount_last_five_years/5

        # Single item load
        single_item_load = paf_granular.single_item_limit_impact * effective_premium - effective_premium
        total_load = sum([
            effective_premium,
            modifiers_load,
            paf_granular.my_dis_coverage.base_premium,
            capped_ded_load,
            paf_paid_claims_load_dollars,
            single_item_load
            ]) / effective_premium if effective_premium != 0 else 0

        paf_structure.model_premium = effective_premium * total_load
        paf_structure.model_rate = paf_structure.model_premium / paf_aggregate.tiv if paf_aggregate.tiv != 0 else 0


def rate_exposure_details(hxd):
    """
    Main exposure details function.
    """
    calculate_table_values(hxd)
    calculate_largest_paf_collection_type(hxd)
    calculate_paf_premiums_and_rates(hxd)
    calculate_paf_deductibles_and_final_premiums(hxd)
