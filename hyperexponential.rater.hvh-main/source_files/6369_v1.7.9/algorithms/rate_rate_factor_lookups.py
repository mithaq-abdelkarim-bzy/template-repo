"""
This module provides functions for performing rating factor lookups for 
the modifiers breakdown section. It retrieves lookup values, maps state-county 
hazard zones, applies range-based lookups, and dynamically assigns rating 
factors across multiple perils.

It includes:
- **Lookup Value Retrieval** (`get_lookup_value`): 
  Fetches values from parameter tables based on lookup conditions.
- **Hazard Zone Mapping** (`get_hazard_mapping`): 
  Maps state-county combinations to hazard zones.
- **Range-Based Lookups** (`generate_lookup_ranges`, `get_lookup_range_key`): 
  Determines correct lookup keys for numeric factors like age or number of storeys.
- **Dynamic Factor Application** (`apply_factor`): 
  Applies rating factors dynamically across multiple perils.
- **TIV Scale Factor Calculation**: 
  Computes total insured value (TIV) scale factors for applicable perils.
- **Modifier Impact Calculation**: 
  Computes total impact of applicable rating factors per peril.
- **Main Rating Lookup Processing** (`rate_rate_factor_lookups`): 
  Applies rating factor lookups, calculates hazard mappings, and 
  computes total modifier impact for each peril.
"""

import hx
import math
import algorithms.rate_constants as const
from algorithms.rate_utilities import get_lookup_value, get_deductible_impact, get_minimum_deductible

aop_sub_peril_factors = {}
aop_layer_specific_tiv_factors = {}

def generate_lookup_ranges(table):
    """
    Reads an `hx` parameter table and generates a dictionary mapping numeric ranges to lookup codes.

    Args:
        table : A `hx` parameter table with 'Lookup code' and 'Values' columns.

    Returns:
        dict: A dictionary with numeric range tuples as keys (inclusive lower, inclusive upper)
              and lookup codes as values.
    """
    lookup_ranges = {}
    rows = table.sort_values('Values').iterrows()
    
    for _, row in rows:
        lookup_label = row["Lookup code"]
        lower_bound = row["Values"]
        
        # Get the next row's value to determine upper bound
        next_row = table[table['Values'] > lower_bound]
        upper_bound = next_row['Values'].min() - 1 if not next_row.empty else float('inf')
        
        # Store the range in the dictionary
        lookup_ranges[(lower_bound, upper_bound)] = lookup_label

    return lookup_ranges


def get_lookup_range_key(value, lookup_ranges):
    """
    Determines the appropriate lookup key based on a numeric value.

    Args:
        value (numeric): The numeric value to categorize.
        lookup_ranges (dict): Dictionary mapping numeric range tuples to lookup codes.

    Returns:
        any: The corresponding lookup code if found, otherwise `None`.
    """
    for (lower, upper), lookup_code in lookup_ranges.items():
        if lower <= value <= upper:
            return lookup_code
    return None


def get_perils_with_factor(factor):
    """
    Returns a list of perils where the given factor is present in the peril configuration.

    Args:
        factor (str): The factor to search for.

    Returns:
        list: List of perils where the factor is present.
    """
    return [peril for peril, (_, factors) in const.peril_configs.items() if factor in factors]


def apply_factor(
    rating_factors,
    factor_name,
    lookup_table,
    bool_type=False,
    reference_column="Lookup code",
    lookup_value=None
):
    """
    Applies a specified rating factor across all relevant perils, with special logic for AOP.

    Args:
        rating_factors (object): The rating factors object.
        factor_name (str): The factor to apply (e.g., 'product_line', 'fire_alarm').
        lookup_table (str): The lookup table name in `hx.params`.
        bool_type (bool, optional): If True, converts boolean values to 'Yes'/'No'. Defaults to False.
        reference_column (str, optional): The column to use for lookups. Defaults to 'Lookup code'.
        lookup_value (any, optional): Overrides the derived lookup value.

    Returns:
        None
    """
    relevant_perils = get_perils_with_factor(factor_name)

    # Retrieve the input value for the factor
    factor_value = getattr(rating_factors, factor_name)
    derived_lookup_value = "Yes" if bool_type and factor_value else "No" if bool_type else factor_value
    final_lookup_value = lookup_value if lookup_value is not None else derived_lookup_value

    factor_lookup_table = getattr(hx.params, lookup_table)

    for peril_column in relevant_perils:
        peril_attribute = const.peril_configs[peril_column][0]
        peril_factors = getattr(rating_factors, peril_attribute)
        peril_factor = getattr(peril_factors, factor_name)

        if peril_column == 'AOP':
            # Special logic for AOP using sub-perils
            weighted_factors = [
                float(get_lookup_value(
                    factor_lookup_table,
                    sub_peril,
                    final_lookup_value,
                    reference_column,
                    error_behavior='default_value',
                    default_value=1.0
                ))
                for sub_peril in const.aop_sub_perils
            ]

            # Use get_lookup_value for AOP weights as well
            aop_weights_table = hx.params.table_aop_weights
            weights = [
                float(get_lookup_value(
                    aop_weights_table,
                    sub_peril,
                    'AOP Weights',  # or another lookup key if dynamic
                    reference_column,
                    error_behavior='default_value',
                    default_value=1.0
                ))
                for sub_peril in const.aop_sub_perils
            ]

            # Compute sumproduct
            aop_sub_peril_factors[factor_name] = weighted_factors
            sumproduct_result = sum(f * w for f, w in zip(weighted_factors, weights))

            peril_factor.value = final_lookup_value
            peril_factor.factor = sumproduct_result

        else:
            # Standard lookup
            peril_factor.value = factor_value
            peril_factor.factor = get_lookup_value(
                factor_lookup_table,
                peril_column,
                final_lookup_value,
                reference_column,
                error_behavior='default_value',
                default_value=None
            )



def apply_range_lookup(rating_factors, factor_name, lookup_table, inception_date=None):
    """
    Applies a range-based lookup for factors like 'number_of_storeys', 'lowest_floor_elevation', 'distance_to_coast',
    'year_built', and 'roof_year'. Special handling is included for AOP.

    Args:
        rating_factors (object): The rating factors object.
        factor_name (str): The factor to apply.
        lookup_table (str): The name of the lookup table in `hx.params`.
        inception_date (datetime, optional): Used to calculate age (e.g., year_built or roof_year).
    """
    perils_with_factor = get_perils_with_factor(factor_name)

    # Handle roof_year fallback to updated_roof_year if available
    if factor_name == 'roof_year':
        factor_value = getattr(rating_factors, 'updated_roof_year', None) or getattr(rating_factors, 'roof_year', None)
    else:
        factor_value = getattr(rating_factors, factor_name, None)

    if factor_value is None:
        return

    # If using age (e.g., year built), derive it
    if inception_date and isinstance(factor_value, (int, float)):
        lookup_value = inception_date.year - factor_value
    else:
        lookup_value = factor_value

    # Determine lookup key from lookup range logic
    lookup_ranges = generate_lookup_ranges(getattr(hx.params, lookup_table))
    lookup_key = get_lookup_range_key(lookup_value, lookup_ranges)
    if lookup_key is None:
        return

    for peril_column in perils_with_factor:
        peril_attribute = const.peril_configs[peril_column][0]
        peril_factors = getattr(rating_factors, peril_attribute)
        peril_factor = getattr(peril_factors, factor_name)

        if peril_column == 'AOP':
            # Special logic for AOP using sub-perils
            aop_weights_table = hx.params.table_aop_weights

            # Range-based factors for each sub-peril
            sub_peril_factors = [
                float(get_lookup_value(
                    getattr(hx.params, lookup_table),
                    sub_peril,
                    lookup_key,
                    error_behavior='default_value',
                    default_value=1.0
                ))
                for sub_peril in const.aop_sub_perils
            ]

            # Corresponding weights
            sub_peril_weights = [
                float(get_lookup_value(
                    aop_weights_table,
                    sub_peril,
                    'AOP Weights',
                    error_behavior='default_value',
                    default_value=1.0
                ))
                for sub_peril in const.aop_sub_perils
            ]

            aop_sub_peril_factors[factor_name] = sub_peril_factors
            # Calculate sumproduct
            sumproduct_result = sum(f * w for f, w in zip(sub_peril_factors, sub_peril_weights))

            peril_factor.value = factor_value
            peril_factor.factor = sumproduct_result

        else:
            # Standard single lookup for non-AOP perils
            peril_factor.value = factor_value
            peril_factor.factor = get_lookup_value(
                getattr(hx.params, lookup_table),
                peril_column,
                lookup_key,
                error_behavior='default_value',
                default_value=1.0
            )


def rate_rate_factor_lookups(hxd):
    rating_factors = hxd.cds.rating_factors
    state_code = rating_factors.state
    county = rating_factors.county

    hazard_mapping = hx.params.table_hazard_mappings[
        (hx.params.table_hazard_mappings['State Code'] == state_code) & 
        (hx.params.table_hazard_mappings['County'] == county)
    ]

    # Set option to show
    if hxd.cds.option_to_show:
        option_to_show = hxd.cds.option_to_show - 1
        hxd.cds.show_modifiers_breakdown = True
    else:
        option_to_show = 0 #just default to show option 1
        hxd.cds.show_modifiers_breakdown = False

    layer_coverage = hxd.cds.layers[option_to_show].coverages

    # Policy Term
    for peril in const.all_perils:
        getattr(rating_factors,peril).policy_term.value = hxd.cds.rating_factors.policy_term
        getattr(rating_factors,peril).policy_term.factor = hxd.cds.rating_factors.policy_term
    aop_sub_peril_factors['policy_term'] = [hxd.cds.rating_factors.policy_term] * len(const.aop_sub_perils)

    # Standard factors
    for factor in ['product_line','construction_type','roof_type','building_occupancy']:
        apply_factor(rating_factors,factor,f'table_{factor}')

    # Bool Factors
    for factor in ['fire_alarm','burglar_alarm','basement','retrofit','soft_storey']:
        apply_factor(rating_factors,factor,f'table_{factor}',bool_type=True,reference_column='Values')

    # Custom References
    apply_factor(rating_factors,'safe','table_safe_installed',bool_type=True,reference_column='Values')
    apply_factor(rating_factors,'ppc','table_ppc',reference_column='Values')
    apply_factor(rating_factors,'sprinkler','table_sprinkler',reference_column='Values')
    apply_factor(rating_factors,'distance_to_coast_options','table_distance_to_coast_options',reference_column='Values')

    # Set year built
    if rating_factors.year_built is not None:
        if rating_factors.year_built < const.min_year_built:
            lookup_value = const.min_year_built
        elif rating_factors.year_built > const.max_year_built:
            lookup_value = const.max_year_built
        else:
            lookup_value = None  # Use the actual year
        apply_factor(
            rating_factors,
            'year_built',
            'table_year_built',
            reference_column="Values",
            lookup_value=lookup_value
        )

    # Numerical based lookups
    apply_range_lookup(rating_factors,'lowest_floor_elevation','table_base_flood_elevation')
    apply_range_lookup(rating_factors,'number_of_storeys','table_number_of_storeys')
    apply_range_lookup(rating_factors,'square_foot','table_input_sqft')

    # Age based lookups
    inception_date = hxd.hx_core.inception_date
    apply_range_lookup(rating_factors, "roof_year", "table_roof_age", inception_date)

    # State county zone
    perils_with_product_line = get_perils_with_factor('product_line')
    for peril_column in perils_with_product_line:
        rating_factors_peril = getattr(rating_factors, const.peril_configs[peril_column][0])


        if not hazard_mapping.empty:
            hazard_zone = hazard_mapping['AOP'].iloc[0]
            zone = state_code + county + hazard_zone
            rating_factors.state_county_zone = zone
            rating_factors_peril.hazard_zone.value = hazard_zone

            if peril_column == 'AOP':
                # Special handling for AOP: weighted sum across sub-perils
                aop_weights_table = hx.params.table_aop_weights

                sub_peril_factors = [
                    float(get_lookup_value(
                        hx.params.table_state_rels,
                        sub_peril,
                        state_code + hazard_zone,
                        error_behavior='default_value',
                        default_value=1.0
                    ))
                    for sub_peril in const.aop_sub_perils
                ]

                sub_peril_weights = [
                    float(get_lookup_value(
                        aop_weights_table,
                        sub_peril,
                        'AOP Weights',
                        error_behavior='default_value',
                        default_value=1.0
                    ))
                    for sub_peril in const.aop_sub_perils
                ]

                aop_sub_peril_factors['state_county_zone'] = sub_peril_factors
                sumproduct_result = sum(f * w for f, w in zip(sub_peril_factors, sub_peril_weights))

                rating_factors_peril.state_county_zone.factor = sumproduct_result
                rating_factors_peril.state_county_zone.value = zone

            else:
                # Standard logic
                rating_factors_peril.state_county_zone.factor = get_lookup_value(
                    hx.params.table_state_rels, 
                    peril_column, 
                    state_code + hazard_zone,
                    error_behavior='default_value',
                    default_value=0
                )
                rating_factors_peril.state_county_zone.value = zone
        else:
            rating_factors_peril.state_county_zone.value = 'Not a valid state county combo'


    # Number of losses
    perils_with_loss = get_perils_with_factor('loss')
    experience_rating_coverages = hxd.cds.experience_rating.coverages
    for peril_column in perils_with_loss:
        rating_factors_peril = getattr(rating_factors, const.peril_configs[peril_column][0])
        number_of_losses = getattr(experience_rating_coverages, const.peril_configs[peril_column][0]).number_of_losses
        rating_factors_peril.loss.value = number_of_losses

        loss_lookup_value = number_of_losses if number_of_losses <= 2 else 3

        if peril_column == 'AOP':
            # Use common number_of_losses but apply sumproduct for factor
            aop_weights_table = hx.params.table_aop_weights

            sub_peril_factors = [
                float(get_lookup_value(
                    hx.params.table_number_of_losses,
                    sub_peril,
                    loss_lookup_value,
                    reference_column="Values",
                    error_behavior='default_value',
                    default_value=1.0
                ))
                for sub_peril in const.aop_sub_perils
            ]

            sub_peril_weights = [
                float(get_lookup_value(
                    aop_weights_table,
                    sub_peril,
                    'AOP Weights',
                    error_behavior='default_value',
                    default_value=1.0
                ))
                for sub_peril in const.aop_sub_perils
            ]
            
            aop_sub_peril_factors['loss'] = sub_peril_factors
            rating_factors_peril.loss.factor = sum(f * w for f, w in zip(sub_peril_factors, sub_peril_weights))

        else:
            # Standard lookup for other perils
            rating_factors_peril.loss.factor = get_lookup_value(
                hx.params.table_number_of_losses,
                peril_column,
                loss_lookup_value,
                reference_column="Values",
                error_behavior='default_value',
                default_value=1.0
            )

    # Calculate WS values
    peril_column = 'WS'
    rating_factors_peril = rating_factors.ws

    # WS Peril (Can vary by layer)
    for layer_index, layer in enumerate(hxd.cds.layers, start=1):
        ws_ded = layer.coverages.ws.deductible_type

        ws_ded.factor = get_lookup_value(
            hx.params.table_ws_peril,
            peril_column,
            ws_ded.value,
            error_behavior='default_value',
            default_value=None
            )
    
        if layer_index == hxd.cds.option_to_show:
            rating_factors_peril.peril.value = ws_ded.value
            rating_factors_peril.peril.factor = ws_ded.factor
        if layer_index == hxd.cds.option_to_bind:
            rating_factors_peril.peril.option_to_bind_factor = ws_ded.factor
    
    # Calculate PAF Values
    peril_column = 'PAF'
    rating_factors_peril = rating_factors.paf

    # Credit Score
    rating_factors_peril.credit_score.value = rating_factors.credit_score
    credit_score_factor = get_lookup_value(
        hx.params.table_credit_score,
        peril_column,
        str(rating_factors_peril.credit_score.value),
        error_behavior='default_value',
        default_value=1,
        reference_column='Values'
        )
    if credit_score_factor == 'Decline':
        rating_factors_peril.credit_score.value =  f'{rating_factors.credit_score} too low: DECLINE'
        rating_factors_peril.credit_score.factor = 0
        hx.errors.validation(f"Credit Score: {rating_factors.credit_score} too low.")
    else:
        rating_factors_peril.credit_score.factor = credit_score_factor

    # Include WS/EQ/FL/Wildfire
    # TODO: Add wildfire score once defined
    # Define the perils and their corresponding attributes
    included_perils = {'WS': 'ws', 'EQ': 'eq', 'Excess FL': 'fl'}

    for layer_index, layer in enumerate(hxd.cds.layers, start=1):
        layer_coverage_structure = layer.coverages
        # Assign values dynamically
        for peril_code, peril_attr in included_perils.items():
            getattr(rating_factors_peril, f"include_{peril_attr}").value = getattr(layer_coverage_structure, peril_attr).include_peril.value

        if not hazard_mapping.empty:
            for peril_code, peril_attr in included_perils.items():
                include_peril = getattr(layer_coverage_structure, peril_attr).include_peril.value
                factor_attr = getattr(rating_factors_peril, f"include_{peril_attr}")

                if include_peril:
                    hazard_zone = str(hazard_mapping[peril_code].iloc[0]).strip().upper()
                    if hazard_zone == '#N/A':
                        include_peril_factor = 1
                    else:
                        include_peril_factor = (
                            get_lookup_value(hx.params.table_paf_hazard_load, 'PAF', f"{peril_code}{hazard_zone}", reference_column='Values') *
                            get_lookup_value(hx.params.table_paf_hazard_surcharge, 'PAF', peril_code, reference_column='Values')
                        )
                else:
                    include_peril_factor = 1

                getattr(layer_coverage_structure, peril_attr).include_peril.factor = include_peril_factor
                if layer_index == hxd.cds.option_to_show:
                    factor_attr.factor = include_peril_factor
                if layer_index == hxd.cds.option_to_bind:
                    factor_attr.option_to_bind_factor = include_peril_factor
        else:
            for peril_attr in included_perils.values():
                getattr(rating_factors_peril, f"include_{peril_attr}").value = 'Not a valid state county combo'

    # TIV Scale Factors
    limit_scale_table = hx.params.table_limit_scale
    aop_weights_table = hx.params.table_aop_weights
    perils_with_tiv_scale = get_perils_with_factor("tiv_scale")

    for peril_column in perils_with_tiv_scale:
        peril_key = const.peril_configs[peril_column][0]

        for layer_index, layer in enumerate(hxd.cds.layers, start=1):
            layer_coverage_structure = layer.coverages
            specific_layer_coverage = getattr(layer_coverage_structure, peril_key)
            rating_factor = getattr(rating_factors, peril_key)
            if peril_column == "Wildfire":
                specific_layer_coverage.tiv.factor = 1
            elif peril_column == "AOP":
                # Use the same TIV across all AOP sub-perils
                tiv = specific_layer_coverage.tiv.value or 0

                # Compute factor for each sub-peril using TIV and sub-peril-specific a & b
                factors = []
                weights = []

                for sub_peril in const.aop_sub_perils:
                    if sub_peril == "WaterDamage":
                        # Lookup baseline TIV from table_aop_prospective_tiv
                        baseline_tiv = float(get_lookup_value(
                            hx.params.table_aop_prospective_tiv,
                            sub_peril,
                            'Prospective TIV',
                            error_behavior='default_value',
                            default_value=1.0
                        ))

                        # Lookup exponent from table_water_damage_limit_scale
                        exponent_factor = hx.params.table_water_damage_limit_scale['Values'].iloc[0]

                        if tiv > 0 and baseline_tiv > 0:
                            factor = min((tiv / baseline_tiv) ** exponent_factor, 1.8) # added a TIV scale cap of 1.8
                        else:
                            factor = 0.0
                    
                    # Different uppdated caluclation for WinterStorm tiv scale
                    elif sub_peril == "WinterStorm":
                    # Lookup baseline TIV from table_aop_prospective_tiv
                        baseline_tiv = float(get_lookup_value(
                            hx.params.table_aop_prospective_tiv,
                            sub_peril,
                            'Prospective TIV',
                            error_behavior='default_value',
                            default_value=1.0
                        ))

                        if tiv > 0 and baseline_tiv > 0:
                            factor = tiv / baseline_tiv
                        else:
                            factor = 0.0
                    
                    else:
                        a = get_lookup_value(limit_scale_table, sub_peril, "a", reference_column="Values")
                        b = get_lookup_value(limit_scale_table, sub_peril, "b", reference_column="Values")
                        factor = (a / 100) * (tiv ** b)

                    weight = float(get_lookup_value(
                        aop_weights_table,
                        sub_peril,
                        "AOP Weights",
                        error_behavior='default_value',
                        default_value=1.0
                    ))

                    factors.append(factor)
                    weights.append(weight)

                # Compute weighted sumproduct
                aop_layer_specific_tiv_factors[layer_index] = factors 
                final_factor = sum(f * w for f, w in zip(factors, weights))
                specific_layer_coverage.tiv.factor = final_factor

            else:
                # Standard non-AOP logic
                a = get_lookup_value(limit_scale_table, peril_column, "a", reference_column="Values")
                b = get_lookup_value(limit_scale_table, peril_column, "b", reference_column="Values")

                tiv = specific_layer_coverage.tiv.value or 0
                if peril_column == 'Liability':
                    specific_layer_coverage.tiv.factor = (a / 100) * (tiv ** b)
                else:
                    specific_layer_coverage.tiv.factor = 1 / ((a / 1000) * (tiv ** b)) if tiv != 0 else 0
            # Set values for rating_factor based on selected layers
            if layer_index == hxd.cds.option_to_show:
                rating_factor.tiv_scale.value = int(specific_layer_coverage.tiv.value or 0)
                rating_factor.tiv_scale.factor = specific_layer_coverage.tiv.factor
            if layer_index == hxd.cds.option_to_bind:
                rating_factor.tiv_scale.option_to_bind_factor = specific_layer_coverage.tiv.factor


    # Calculate total modifier impact for each peril
    for peril_column, (peril, factor_names) in const.peril_configs.items():
        if peril == 'paf':
            rating_factors_peril = getattr(rating_factors, peril)
            for layer_index, layer in enumerate(hxd.cds.layers, start=1):
                layer_coverage_structure = layer.coverages
                specific_layer_coverage = getattr(layer_coverage_structure, peril)

                # Calculate total factor from rating factors
                paf_factor_discounts = [
                    ((getattr(layer.coverages.ws.include_peril, "factor", 0) or 0) - 1) if factor == "include_ws"
                    else ((getattr(layer.coverages.eq.include_peril, "factor", 0) or 0) - 1) if factor == "include_eq"
                    else ((getattr(layer.coverages.fl.include_peril, "factor", 0) or 0) - 1) if factor == "include_fl"
                    else ((getattr(layer.coverages.wildfire.include_peril, "factor", 0) or 0) - 1) if factor == "include_wildfire"
                    else ((float(getattr(getattr(rating_factors_peril, factor, None), "factor", 0) or 0)) - 1)
                    if getattr(rating_factors_peril, factor, None) and getattr(rating_factors_peril, factor).factor is not None
                    else 0
                    for factor in factor_names
                ]

                total_factor = 1 + sum(paf_factor_discounts)

                # Assign total factor to the relevant attributes
                specific_layer_coverage.modifiers_impact.factor = total_factor

                if layer_index == hxd.cds.option_to_show:
                    rating_factors_peril.total_modifier_impact.factor = total_factor
                if layer_index == hxd.cds.option_to_bind:
                    rating_factors_peril.total_modifier_impact.option_to_bind_factor = total_factor

        elif peril == 'aop':
            # Validate global (shared) sub-peril factor lengths
            list_lengths = [len(v) for k, v in aop_sub_peril_factors.items()]
            if len(set(list_lengths)) != 1:
                raise ValueError("All shared AOP sub-peril factor lists must be the same length")

            n = list_lengths[0]
            if len(weights) != n:
                raise ValueError(f"AOP weights length ({len(weights)}) must match factor list length ({n})")

            rating_factors_peril = getattr(rating_factors, peril)

            for layer_index, layer in enumerate(hxd.cds.layers, start=1):
                specific_layer_coverage = getattr(layer.coverages, peril)

                # Build full dict of shared + layer-specific factors
                full_factors = {
                    **aop_sub_peril_factors,  # shared across layers
                    "tiv": aop_layer_specific_tiv_factors[layer_index],  # layer-specific TIV
                }

                # Validate all factor lengths for this layer
                if any(len(lst) != n for lst in full_factors.values()):
                    raise ValueError(f"Layer {layer_index}: Mismatch in AOP sub-peril factor list lengths")

                # Compute index-wise products
                products = [
                    math.prod([full_factors[key][i] for key in full_factors])
                    for i in range(n)
                ]

                if layer.coverages.ws.include_peril.value is False:
                    for i, sub_peril in enumerate(const.aop_sub_perils):
                        if sub_peril in ["Hail", "Wind"]:
                            products[i] = 0
                    

                result = sum(p * w for p, w in zip(products, weights))

                # Assign result
                specific_layer_coverage.modifiers_impact.factor = result

                if layer_index == hxd.cds.option_to_show:
                    rating_factors_peril.total_modifier_impact.factor = result
                if layer_index == hxd.cds.option_to_bind:
                    rating_factors_peril.total_modifier_impact.option_to_bind_factor = result

        else:
            rating_factors_peril = getattr(rating_factors, peril)

            for layer_index, layer in enumerate(hxd.cds.layers, start=1):
                layer_coverage_structure = layer.coverages
                specific_layer_coverage = getattr(layer_coverage_structure, peril)

                factors = [
                    specific_layer_coverage.tiv.factor if name == "tiv_scale"
                    else specific_layer_coverage.deductible_type.factor if name == "peril"
                    else getattr(rating_factors_peril, name).factor
                    for name in factor_names
                ]

                factor = math.prod([x for x in factors if x is not None])

                specific_layer_coverage.modifiers_impact.factor = factor

                if layer_index == hxd.cds.option_to_show:
                    rating_factors_peril.total_modifier_impact.factor = factor
                if layer_index == hxd.cds.option_to_bind:
                    rating_factors_peril.total_modifier_impact.option_to_bind_factor = factor

    # Calculate TP uplift
    tp_uplifts_table = hx.params.table_tp_uplift_factors
    tp_uplift_structure = hxd.cds.tp_uplift
    for peril_column, (peril, _) in const.peril_configs.items():
        peril_tp_uplift = getattr(tp_uplift_structure,peril)
        peril_tp_uplift.tp_uplift_factor.factor = get_lookup_value(
            tp_uplifts_table,
            peril_column,
            str(state_code)+str(county),
            reference_column='Lookup',
            error_behavior='default_value',
            default_value=0)
        peril_tp_uplift.tp_uplift_factor.option_to_bind_factor = peril_tp_uplift.tp_uplift_factor.factor


def apply_base_factor(hxd,rating_factors, factor_name, lookup_table, bool_type=False, reference_column="Lookup code"):
    """
    Applies a base rating factor dynamically across all relevant perils.

    Args:
        rating_factors (object): The rating factors object.
        factor_name (str): The factor to apply (e.g., 'product_line', 'fire_alarm').
        lookup_table (str): The lookup table name to use in `hx.params`.
        bool_type (bool, optional): If True, converts boolean values to 'Yes'/'No' for lookup. Defaults to False.
        reference_column (str, optional): The column to use for lookups. Defaults to 'Lookup code'.

    Returns:
        None (modifies `rating_factors` in place).
    """
    relevant_perils = get_perils_with_factor(factor_name)

    # Retrive the input value for the factor and convert the booleans
    factor_value = const.base_commercial_rates_factors[factor_name]
    lookup_value = "Yes" if bool_type and factor_value else "No" if bool_type else factor_value

    for peril_column in relevant_perils:
        peril_attribute = const.peril_configs[peril_column][0]
        peril_factors = getattr(rating_factors, peril_attribute)
        peril_factor = getattr(peril_factors, factor_name)
        factor_lookup_table = getattr(hx.params, lookup_table)
        if peril_column == 'AOP':
            # Weighted logic for AOP base factor using sub-perils
            weighted_factors = [
                float(get_lookup_value(
                    factor_lookup_table,
                    sub_peril,
                    lookup_value,
                    reference_column,
                    error_behavior='default_value',
                    default_value=1.0
                ))
                for sub_peril in const.aop_sub_perils
            ]

            aop_weights_table = hx.params.table_aop_weights
            weights = [
                float(get_lookup_value(
                    aop_weights_table,
                    sub_peril,
                    'AOP Weights',
                    reference_column,
                    error_behavior='default_value',
                    default_value=1.0
                ))
                for sub_peril in const.aop_sub_perils
            ]

            sumproduct_result = sum(f * w for f, w in zip(weighted_factors, weights))

            peril_factor.base_factor = sumproduct_result
            setattr(
                hxd.cds.commercial_rates_base_rels,
                peril_attribute,
                getattr(hxd.cds.commercial_rates_base_rels, peril_attribute) * sumproduct_result
            )
        else:
            # Standard lookup
            factor = get_lookup_value(
                factor_lookup_table,
                peril_column,
                lookup_value,
                reference_column,
                error_behavior='default_value',
                default_value=None
            )
            if factor is not None:
                peril_factor.base_factor = factor
                setattr(
                    hxd.cds.commercial_rates_base_rels,
                    peril_attribute,
                    getattr(hxd.cds.commercial_rates_base_rels, peril_attribute) * factor
                )

def rate_base_commercial_rates_lookup(hxd):
    """
    Calculate the base factors required for the hvh commercial rates
    """
    state = hxd.cds.rating_factors.state
    distance_to_coast = hxd.cds.rating_factors.distance_to_coast 

    for peril in const.all_perils:
        setattr(hxd.cds.commercial_rates_base_rels, peril, 1)

    # Calculate base factors
    rating_factors = hxd.cds.rating_factors

    # Standard factors
    for factor in ['product_line','construction_type','building_occupancy','number_of_storeys']:
        apply_base_factor(hxd,rating_factors,factor,f'table_{factor}')

    # Bool Factors
    for factor in ['fire_alarm','burglar_alarm','basement','retrofit','soft_storey']:
        apply_base_factor(hxd,rating_factors,factor,f'table_{factor}',bool_type=True,reference_column='Values')

    apply_base_factor(hxd,rating_factors,'safe','table_safe_installed',bool_type=True,reference_column='Values')
    apply_base_factor(hxd,rating_factors,'ppc','table_ppc',reference_column='Values')
    apply_base_factor(hxd,rating_factors,'sprinkler','table_sprinkler',reference_column='Values')


    apply_base_factor(hxd,rating_factors,'year_built','table_year_built',reference_column="Values")
    apply_base_factor(hxd,rating_factors,'roof_year','table_roof_age')
    apply_base_factor(hxd,rating_factors,'loss','table_number_of_losses')
    apply_base_factor(hxd,rating_factors,'square_foot','table_input_sqft')

    # TIV Scale Factor
    limit_scale_table = hx.params.table_limit_scale
    perils_with_tiv_scale = get_perils_with_factor("tiv_scale")
    assumed_tiv = const.base_commercial_rates_factors['assumed_tiv'] # assumed_tiv = 3,000,000
    for peril_column in perils_with_tiv_scale:
        peril_key = const.peril_configs[peril_column][0]
        rating_factor = getattr(rating_factors, peril_key)
        if peril_key == 'wildfire':
            factor = 1
            factor = factor / (assumed_tiv / 1_000_000)
            rating_factor.tiv_scale.base_factor = factor
        elif peril_key == 'aop':

            # Compute factor for each sub-peril using TIV and sub-peril-specific a & b
            factors = []
            weights = []

            for sub_peril in const.aop_sub_perils:
                if sub_peril == "WaterDamage":
                    # Lookup baseline TIV from table_aop_prospective_tiv
                    baseline_tiv = float(get_lookup_value(
                        hx.params.table_aop_prospective_tiv,
                        sub_peril,
                        'Prospective TIV',
                        error_behavior='default_value',
                        default_value=1.0
                    ))

                    # Lookup exponent from table_water_damage_limit_scale
                    exponent_factor = hx.params.table_water_damage_limit_scale['Values'].iloc[0]

                    if assumed_tiv > 0 and baseline_tiv > 0:
                        factor = min((assumed_tiv / baseline_tiv) ** exponent_factor, 1.8) # added a TIV scale cap of 1.8
                    else:
                        factor = 0.0

                # Different uppdated caluclation for WinterStorm tiv scale
                elif sub_peril == "WinterStorm":
                    # Lookup baseline TIV from table_aop_prospective_tiv
                    baseline_tiv = float(get_lookup_value(
                        hx.params.table_aop_prospective_tiv,
                        sub_peril,
                        'Prospective TIV',
                        error_behavior='default_value',
                        default_value=1.0
                    ))

                    if assumed_tiv > 0 and baseline_tiv > 0:
                        factor = assumed_tiv / baseline_tiv
                    else:
                        factor = 0.0

                else:
                    a = get_lookup_value(limit_scale_table, sub_peril, "a", reference_column="Values")
                    b = get_lookup_value(limit_scale_table, sub_peril, "b", reference_column="Values")
                    factor = (a / 100) * (assumed_tiv ** b)

                weight = float(get_lookup_value(
                    hx.params.table_aop_weights,
                    sub_peril,
                    "AOP Weights",
                    error_behavior='default_value',
                    default_value=1.0
                ))

                factors.append(factor)
                weights.append(weight)

            # Compute weighted sumproduct
            final_factor = sum(f * w for f, w in zip(factors, weights))

            factor = final_factor / (assumed_tiv / 1_000_000)
            rating_factor.tiv_scale.base_factor = factor

        elif peril_key == 'liability':
            a = get_lookup_value(limit_scale_table, peril_column, "a", reference_column="Values")
            b = get_lookup_value(limit_scale_table, peril_column, "b", reference_column="Values")
            factor = (a / 100) * (assumed_tiv ** b) #1 / ((a / 1000) * (assumed_tiv ** b)) if assumed_tiv != 0 else 0
            factor = factor / (assumed_tiv / 1_000_000) # whats this for??
            rating_factor.tiv_scale.base_factor = factor
        else:
            a = get_lookup_value(limit_scale_table, peril_column, "a", reference_column="Values")
            b = get_lookup_value(limit_scale_table, peril_column, "b", reference_column="Values")
            factor = 1 / ((a / 1000) * (assumed_tiv ** b)) if assumed_tiv != 0 else 0 # why 1/xxx
            rating_factor.tiv_scale.base_factor = factor
        setattr(hxd.cds.commercial_rates_base_rels, peril_key, getattr(hxd.cds.commercial_rates_base_rels,peril_key) * factor)

    # Deductible Load
    for peril_column in ['aop','eb','wildfire','ws','eq']:
        if peril_column == 'eb':
            hxd.cds.commercial_rates_base_rels.eb = getattr(hxd.cds.commercial_rates_base_rels,'eb') * 1 # No value for 0 in table
        elif peril_column in ['aop','wildfire']:
            deductible_value = get_minimum_deductible(hxd, peril_column, state, distance_to_coast, default_value=2500)
            deductible_percent = deductible_value / assumed_tiv if assumed_tiv != 0 else 0
            ded_factor = get_deductible_impact(peril_column, deductible_percent)
            setattr(hxd.cds.commercial_rates_base_rels, peril_column, getattr(hxd.cds.commercial_rates_base_rels,peril_column) * ded_factor)
        elif peril_column == 'ws':
            deductible_percent = get_minimum_deductible(hxd, peril_column, state, distance_to_coast, default_value=0)
            ded_factor = get_deductible_impact(peril_column, deductible_percent)
            setattr(hxd.cds.commercial_rates_base_rels, peril_column, getattr(hxd.cds.commercial_rates_base_rels,peril_column) * ded_factor)
            pass
        else:
            deductible_value = const.base_commercial_rates_factors['deductible']['all'] if peril_column != 'eq' else const.base_commercial_rates_factors['deductible']['eq']
            ded_factor = get_deductible_impact(peril_column,deductible_value)
            setattr(hxd.cds.commercial_rates_base_rels, peril_column, getattr(hxd.cds.commercial_rates_base_rels,peril_column) * ded_factor)
