"""
This module provides functions for calculating the pricing variables, 
modifiers, and final key performance indicators (KPIs).

It includes:
- **Setting rate constants** (`rate_set_rate_constants`): Initializes base rate constants, 
  dropdowns, and validates user selections.
- **Calculating pricing variables** (`rate_calculate_pricing_variables`): Computes 
  peril-specific base rates, adjusted rates, minimum deductibles, and model premiums.
- **Handling peril-specific calculations**: Uses a loop to process various 
  insurance perils (AOP, Wildfire, WS, EQ, Liability, Equipment Breakdown, Excess Flood).
- **Factor variance calculations** (`calculate_factor_variances`): Determines the difference 
  between selected and bound rating factors.
- **Final KPI calculations** (`calculate_final_kpis`): Computes exposure splits, 
  peril loss ratios, and technical premiums.
- **Main pricing function** (`rate_pricing`): Runs all necessary calculations in sequence.
"""

import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
import algorithms.rate_constants as const
from operator import itemgetter
from algorithms.rate_utilities import get_lookup_value, get_deductible_impact, get_minimum_deductible
from algorithms.rate_constants import max_layers, deductible_type_mapping

def rate_set_rate_constants(hxd):
    """
    Sets rate constants before calculating modifiers.
    """
    hazard_mappings = hx.params.table_hazard_mappings
    state = hxd.cds.rating_factors.state
    county = hxd.cds.rating_factors.county
    number_of_options = hxd.cds.number_of_options
    zip_code = hxd.cds.rating_factors.zip
    zip_city_state_mappings = hx.params.table_zip_code_city_state_mappings

    # Set option to bind
    bound_layers = [
        k for k, layer in enumerate(hxd.cds.layers, start=1)
        if k <= number_of_options and layer.status == "Bound"
    ]

    hxd.cds.option_to_bind = bound_layers[0] if len(bound_layers) == 1 else None
    option_to_bind = hxd.cds.option_to_bind

    # Show/ hide modifiers table
    hxd.cds.show_option_to_bind_factor = (
        None not in (hxd.cds.option_to_bind, hxd.cds.option_to_show)
        and hxd.cds.option_to_bind != hxd.cds.option_to_show
    )

    # Set dynamic dropdowns
    zip_match = zip_city_state_mappings[zip_city_state_mappings['Risk Zip'] == zip_code]
    hxd.cds.rating_factors.city_dropdown = zip_match['Risk City']
    zip_states = zip_match['Risk State'].unique()
    state_list = sorted(set(hazard_mappings["State Code"])) if len(zip_states) == 0 else zip_states
    hxd.cds.rating_factors.state_dropdown = state_list
    zip_counties = zip_match['County'].unique()
    all_counties = hazard_mappings[hazard_mappings["State Code"] == state]["County"].unique()

    # Ensure all values are strings for consistent comparison
    zip_counties = [str(c) for c in zip_counties]
    all_counties = [str(c) for c in all_counties]

    # Move zip_counties to the front, preserving their order, and append the rest
    filtered_counties = list(dict.fromkeys(list(zip_counties) + list(all_counties)))

    hxd.cds.rating_factors.county_dropdown = filtered_counties
    
    if state not in state_list:
        if state is not None:
            hx.errors.validation(f'Risk Characteristics: Selected state {state} does not match the selected zip code')
        else:
            hx.errors.validation(f'Risk Characteristics: State field must be completed.')
    if county not in set(filtered_counties):
        hx.errors.validation(f"Risk Characteristics: Selected county '{county}' is not valid for state '{state}'")

    hxd.cds.options_to_show_dropdown = list(range(1, number_of_options + 1))
    
    # Set zero-indexed option to bind
    hxd.cds.option_to_bind_zero_indexed = option_to_bind - 1 if option_to_bind else None
    
    # Lock/Unlock layer logic for pricing tables
    for i, layer in enumerate(hxd.cds.layers):
        if i < max_layers:
            if layer.status == "Quoted":
                layer.lock_layers = True
                layer.unlock_layers = False
            else:
                layer.lock_layers = False
                layer.unlock_layers = True
        else:
            layer.lock_layers = False
            layer.unlock_layers = False

    hxd.cds.lock_layer = False
    for layer in hxd.cds.layers:
        if layer.status == "Quoted":
            hxd.cds.lock_layer = True
            break
    hxd.cds.unlock_layer = not hxd.cds.lock_layer

    # Set options/layer labels
    for option_number, layer in enumerate(hxd.cds.layers, start=1):
        is_bound_option = (layer.status=='Bound')
        emoji = "\U00002705" if is_bound_option else ""
        layer.layer_label = f"Option {option_number} {emoji}"
        layer.option_to_bind = is_bound_option
        layer.show_layer = option_number <= number_of_options
        layer.unlock_layers = (option_number <= number_of_options) and layer.unlock_layers

    # Show sections dependent on 'include_peril'
    for coverage in const.all_perils:
        setattr(hxd.cds, f"show_{coverage}_options", False)
        for k, layer in enumerate(hxd.cds.layers):
            if k < number_of_options and hasattr(layer.coverages, coverage):
                coverage_obj = getattr(layer.coverages, coverage).include_peril
                if hasattr(coverage_obj, "value") and coverage_obj.value:
                    setattr(hxd.cds, f"show_{coverage}_options", True)
                    break
                
    # Show all perils options by default
    pl = hxd.cds.rating_factors.product_line  
    if pl == 'Excess Flood':            
        for coverage_item in const.all_perils:
            if(coverage_item != 'fl'):
                setattr(hxd.cds, f"show_{coverage_item}_option", False)
                setattr(hxd.cds, f"show_{coverage_item}_options", False)
            else:    
                setattr(hxd.cds, f"show_fl_option", True)
                coverage_obj = getattr(layer.coverages, coverage_item).include_peril
                if hasattr(coverage_obj, "value") and coverage_obj.value:
                    setattr(hxd.cds, f"show_{coverage_item}_options", True)
    elif pl == 'Excess Wind & Hail':
        for coverage_item in const.all_perils:
            if(coverage_item != 'ws'):
                setattr(hxd.cds, f"show_{coverage_item}_option", False)
                setattr(hxd.cds, f"show_{coverage_item}_options", False)
            else:    
                setattr(hxd.cds, f"show_ws_option", True)
                coverage_obj = getattr(layer.coverages, coverage_item).include_peril
                if hasattr(coverage_obj, "value") and coverage_obj.value:
                    setattr(hxd.cds, f"show_{coverage_item}_options", True)
    elif pl == 'Monoline Earthquake':
        for coverage_item in const.all_perils:
            if(coverage_item != 'eq'):
                setattr(hxd.cds, f"show_{coverage_item}_option", False)
                setattr(hxd.cds, f"show_{coverage_item}_options", False)
            else:    
                setattr(hxd.cds, f"show_eq_option", True)
                coverage_obj = getattr(layer.coverages, coverage_item).include_peril
                if hasattr(coverage_obj, "value") and coverage_obj.value:
                    setattr(hxd.cds, f"show_{coverage_item}_options", True)

    elif pl != 'Excess Flood' and pl!= 'Excess Wind & Hail' and pl != 'Monoline Earthquake':
        for coverage_item in const.all_perils:
            setattr(hxd.cds, f"show_{coverage_item}_option", True)
 
    # Dynamically create limits table based on Product Line selection
    limits_visibility_rules = const.pricing_limits_table_rules
    for key, check_visibility in limits_visibility_rules.items():
        should_show_limit = check_visibility(hxd.cds.rating_factors.product_line)
        setattr(hxd.cds.pricing_limits_table, key, should_show_limit)

    # Set liability toggle
    hxd.cds.show_liability_collection_and_table = not hxd.cds.rating_factors.high_profile_client

    # Show and set WS deductibles
    hxd.cds.ws_deductible_is_not_all_perils = False
    hxd.cds.ws_deductible_is_all_perils = False
    for k, layer in enumerate(hxd.cds.layers):
        if k >= number_of_options:
            break
        if layer.coverages.ws.deductible_type.value == "All Perils":
            hxd.cds.ws_deductible_is_all_perils = True
            layer.coverages.ws.deductible_all_perils = layer.coverages.aop.deductible
        if layer.coverages.ws.deductible_type.value in ["Wind & Hail", "Named Storm"]:
            hxd.cds.ws_deductible_is_not_all_perils = True

    # Set limit override values
    for layer in hxd.cds.layers:
        layer.coverage_b_other_structures_limit.calculated = layer.coverage_a_building_limit *  0.1
        layer.coverage_c_personal_property_limit.calculated = layer.coverage_a_building_limit *  0.5
        layer.coverage_d_loss_of_use_limit.calculated = layer.coverage_a_building_limit *  0.3
        if hxd.cds.experience_rating.coverages.liability.number_of_losses > 0 or hxd.cds.rating_factors.high_profile_client == True:
            layer.coverage_l_liability_limit.calculated = 0
        else:
            layer.coverage_l_liability_limit.calculated = 0 # set a default value here
        
        layer.coverage_e_additional_living_expense_limit.calculated = 0 # default to 0

        pl = hxd.cds.rating_factors.product_line
        occ = hxd.cds.rating_factors.building_occupancy
        # Underwriter specific overrides
        if pl == 'Homeowners (HO5)' and occ in ["Primary", "Secondary"]:
            layer.coverage_l_liability_limit.calculated = 500_000
                
        elif pl == 'Homeowners (HO3)' and occ in ["Primary", "Secondary", "Secondary / Seasonal Rental", "Renovation (builders risk)"]:
            layer.coverage_l_liability_limit.calculated = 300_000

        elif pl == 'Condominium (HO6)':
            layer.coverage_l_liability_limit.calculated = 300_000 if occ != "Vacant" else 0
            
        elif pl == 'Dwelling' and occ in ["Vacant", "Rental"]:
            layer.coverage_l_liability_limit.calculated = 300_000 if occ == "Rental" else 0

    # Set In-scope TIV
    for layer in hxd.cds.layers:
        sum_of_coverages  = sum([
            layer.coverage_a_building_limit,
            layer.coverage_b_other_structures_limit.selected,
            layer.coverage_c_personal_property_limit.selected,
            layer.coverage_d_loss_of_use_limit.selected    
        ])

        for peril in const.all_perils_dict.keys():
            if peril not in ['paf','liability','eb']:
                getattr(layer.coverages,peril).tiv.value = sum_of_coverages
        layer.coverages.liability.tiv.value = layer.coverage_l_liability_limit.selected 


def calculate_effective_rate(coverage):
    """Calculate the effective rate."""
    return max(coverage.base_rate * coverage.modifiers_impact.factor, coverage.minimum_rate)


def calculate_model_premium(coverage, deductible_impact):
    """Calculate the model premium."""
    return deductible_impact * calculate_effective_rate(coverage) * coverage.tiv.value


def rate_calculate_pricing_variables(hxd):
    """
    Main pricing variable calculations to be run after extracting modifiers
    """
    # Top level constants that do not change by option or peril
    zip_code = hxd.cds.rating_factors.zip
    state = hxd.cds.rating_factors.state
    county = hxd.cds.rating_factors.county
    distance_to_coast = hxd.cds.rating_factors.distance_to_coast 

    for layer in hxd.cds.layers:
        #Set minimum rates
        for peril_variable, peril_column in const.all_perils_dict.items():
            if peril_variable == 'paf':
                continue
            elif peril_variable == 'fl':
                specific_coverage = getattr(layer.coverages,peril_variable)
                lookup_code = str(state) + str(county)
                flood_zone_code = get_lookup_value(
                    hx.params.table_hazard_mappings,
                    'NFIP Flood Zone',
                    lookup_code,reference_column='Lookup',
                    error_behavior='default_value',
                    default_value=''
                )
                specific_coverage.flood_zone = flood_zone_code
                lookup_code = 'Minimum RateFloodZone' + flood_zone_code
                specific_coverage.minimum_rate = get_lookup_value(
                    hx.params.table_minimum_rate,
                    peril_column,
                    lookup_code,
                    error_behavior='default_value',
                    default_value=0
                )
            else:
                specific_coverage = getattr(layer.coverages,peril_variable)
                specific_coverage.minimum_rate = get_lookup_value(hx.params.table_minimum_rate,peril_column,'Minimum Rate')

        # Set base rates
        for peril_variable, peril_column in const.all_perils_dict.items():
            if peril_variable == 'paf':
                continue
            elif peril_variable == 'ws':
                specific_coverage = getattr(layer.coverages, peril_variable)
                ws_zip_table = hx.params.table_ws_rates_zip
                ws_county_table = hx.params.table_ws_rates_county
                ws_state_table = hx.params.table_ws_rates_state
                specific_coverage.base_rate = (
                    ws_zip_table[ws_zip_table['Zip'] == zip_code]['WS Rates'].iloc[0]
                    if ws_zip_table[ws_zip_table['Zip'] == zip_code].shape[0] > 0 else
                    ws_county_table[(ws_county_table['County'] == county)&(ws_county_table['State'] == state)]['WS Rates'].iloc[0]
                    if ws_county_table[(ws_county_table['County'] == county)&(ws_county_table['State'] == state)].shape[0] > 0 else
                    ws_state_table[ws_state_table['State'] == state]['WS Rates'].iloc[0]
                    if ws_state_table[ws_state_table['State'] == state].shape[0] > 0 else 0
                )
            elif peril_variable == 'eb':
                # Retrieve coverage structure and base rate table
                specific_coverage = getattr(layer.coverages, peril_variable)
                eb_base_rate_table = hx.params.table_base_rate
                eb_base_rate_table = eb_base_rate_table[
                    eb_base_rate_table['Lookup code'].str.contains("Base Premium Coverage A Limit", na=False)
                ]

                # Create key mapping for lookup
                key_mapping = dict(zip(eb_base_rate_table["Values"].astype(int), eb_base_rate_table["Lookup code"]))
                lookup_keys = sorted(key_mapping.keys())

                # Determine the correct lookup code based on limit
                limit = layer.coverage_a_building_limit
                lookup_code = next(
                    (key_mapping[key] for key in reversed(lookup_keys) if key <= limit),
                    key_mapping[min(lookup_keys)]
                )

                # Calculate effective rate
                base_premium = get_lookup_value(eb_base_rate_table, peril_column, lookup_code)
                eb_base_rate = base_premium / specific_coverage.tiv.value if specific_coverage.tiv.value != 0 else 0
                eb_base_rate = eb_base_rate * const.target_loss_ratios_dict['Equipment breakdown']
                effective_rate = max(
                    eb_base_rate * specific_coverage.modifiers_impact.factor,
                    specific_coverage.minimum_rate
                )
                if specific_coverage.include_peril.value is False:
                    effective_rate = 0

                specific_coverage.base_rate = effective_rate

            elif peril_variable == 'aop':
                specific_coverage = getattr(layer.coverages, peril_variable)
                specific_coverage.base_rate = hx.params.table_base_rate[hx.params.table_base_rate['Lookup code']=='Base Rate'][const.aop_sub_perils].values.sum()

            elif peril_variable == 'eq':
                # Set base rate for other perils
                specific_coverage = getattr(layer.coverages, peril_variable)
                base_rate = get_lookup_value(
                    hx.params.table_base_rate, peril_column, 'Base Rate'
                )          
                specific_coverage.base_rate = base_rate * const.target_loss_ratios_dict['EQ']  
                
            else:
                # Set base rate for other perils
                specific_coverage = getattr(layer.coverages, peril_variable)
                base_rate = get_lookup_value(
                    hx.params.table_base_rate, peril_column, 'Base Rate'
                )
                if peril_variable == 'fl':
                    if specific_coverage.include_peril.value is False:
                        base_rate = 0
                specific_coverage.base_rate = base_rate

        # Set adjusted and final rates
        for peril_variable, peril_column in const.all_perils_dict.items():
            if peril_variable in ['aop', 'wildfire', 'ws', 'eq', 'fl']:
                specific_coverage = getattr(layer.coverages, peril_variable)

                # Calculate adjusted base rate
                specific_coverage.adjusted_base_rate = (
                    specific_coverage.base_rate * specific_coverage.modifiers_impact.factor
                    if specific_coverage.modifiers_impact.factor is not None else None
                )

                # Calculate final modified rate
                if specific_coverage.adjusted_base_rate is not None and specific_coverage.minimum_rate is not None:
                    specific_coverage.final_modified_rate = max(
                        specific_coverage.adjusted_base_rate, specific_coverage.minimum_rate
                    )

        
        # Assign Wildfire Deductible Type/Deductible dropdown values
        dropdown_items = list(deductible_type_mapping.keys())
        wf_included = getattr(layer.coverages, "wildfire").include_peril.value

        if wf_included:
            dropdown_items.remove("Excluded")

            layer.coverages.wildfire.deductible_type_dropdown = dropdown_items
            layer.coverages.wildfire.deductible_dropdown = deductible_type_mapping.get(layer.coverages.wildfire.deductible_type, [])
            if layer.coverages.wildfire.deductible_type == "AOP":
                layer.coverages.wildfire.deductible_dropdown = [getattr(layer.coverages, "aop").deductible]
        else:
            layer.coverages.wildfire.deductible_type_dropdown = ["Excluded"]

        for peril, config in const.peril_pricing_calc_settings.items():
            peril_coverage = getattr(layer.coverages, peril)

            # Set minimum deductible if applicable
            
            if 'default_deductible' in config:
                peril_coverage.minimum_deductible = get_minimum_deductible(hxd, peril, state, distance_to_coast, default_value=config['default_deductible'])

                if peril == 'wildfire' and wf_included == True and layer.coverages.wildfire.deductible_type == "Percentage (%)":
                    total_cov = layer.coverage_a_building_limit + layer.coverage_b_other_structures_limit.selected + layer.coverage_c_personal_property_limit.selected + layer.coverage_d_loss_of_use_limit.selected
                    peril_coverage.final_deductible = max(peril_coverage.minimum_deductible, ((getattr(peril_coverage, 'deductible', 0) or 0) / 100) *  total_cov)
                else:
                    peril_coverage.final_deductible = max(peril_coverage.minimum_deductible, getattr(peril_coverage, 'deductible', 0) or 0)

                deductible_percent = peril_coverage.final_deductible / peril_coverage.tiv.value if peril_coverage.tiv.value != 0 else 0
                peril_coverage.deductible_impact = get_deductible_impact(peril, deductible_percent)

                if peril == 'aop':
                    peril_coverage.final_modified_rate = peril_coverage.final_modified_rate * peril_coverage.deductible_impact


            # Special handling for WS deductible
            if 'ws_deductible' in config:
                peril_coverage.minimum_deductible = get_minimum_deductible(hxd, peril, state, distance_to_coast, default_value=0)
                if peril_coverage.deductible_type.value in ["Wind & Hail", "Named Storm"]:
                    peril_coverage_deductible = peril_coverage.deductible or 0
                else:
                    peril_coverage_deductible = peril_coverage.deductible_all_perils or 0
                    peril_coverage_deductible = peril_coverage_deductible / peril_coverage.tiv.value * 100 if peril_coverage.tiv.value != 0 else 0
                peril_coverage.final_deductible = max(peril_coverage.minimum_deductible,peril_coverage_deductible)
                
                deductible_percent = peril_coverage.final_deductible
                peril_coverage.deductible_impact = get_deductible_impact(peril, deductible_percent)

                #effective_premium = peril_coverage.base_rate * peril_coverage.tiv.value #slightly different model premium calc
                effective_premium = peril_coverage.final_modified_rate * peril_coverage.tiv.value
                peril_coverage.model_premium = effective_premium * peril_coverage.deductible_impact

            # Special handling for EQ deductible
            if 'eq_deductible' in config:
                deductible_percent = peril_coverage.deductible
                peril_coverage.deductible_impact = get_deductible_impact(peril,deductible_percent)

            # Special handling for Equipment Breakdown (EB) deductible impact
            if 'deductible_table' in config:
                deductible_table = getattr(hx.params, config['deductible_table'])
                peril_coverage.deductible_impact = get_lookup_value(
                    deductible_table,
                    config['column'],
                    peril_coverage.deductible,
                    reference_column='Values',
                    error_behavior='default_value',
                    default_value=0
                    )

            # Calculate model premium
            if peril == 'ws':
                pass
            elif peril =='aop':
                aop_weights = hx.params.table_aop_weights[const.aop_sub_perils].iloc[0].values
                prospective_tivs = hx.params.table_aop_prospective_tiv[const.aop_sub_perils].iloc[0].values
                sum_product = np.dot(aop_weights, prospective_tivs)
                peril_coverage.model_premium = peril_coverage.final_modified_rate * sum_product   
            elif peril == 'eb':
                peril_coverage.model_premium = peril_coverage.deductible_impact * peril_coverage.tiv.value * peril_coverage.base_rate
            # Liability case uses AOP deductible
            elif config.get('uses_aop_deductible'):
                #peril_coverage.model_premium = calculate_model_premium(peril_coverage, layer.coverages.aop.deductible_impact)
                prospective_tiv = hx.params.table_aop_prospective_tiv['Liability'].iloc[0]
                effective_rate = max(peril_coverage.base_rate * peril_coverage.modifiers_impact.factor,peril_coverage.minimum_rate)
                #peril_coverage.model_premium = layer.coverages.aop.deductible_impact * prospective_tiv * effective_rate # Liability doesnt have deductibles, so remove this
                peril_coverage.model_premium = prospective_tiv * effective_rate
            else:
                peril_coverage.model_premium = calculate_model_premium(peril_coverage, peril_coverage.deductible_impact)

            # Calculate model rate
            peril_coverage.model_rate = (
                peril_coverage.model_premium / peril_coverage.tiv.value if peril_coverage.tiv.value != 0 else 0
            )

        #### Excess FL ####
        peril_column = 'Excess FL' 
        peril_variable = 'fl' 
        peril_coverage = getattr(layer.coverages,peril_variable)  

        # xs building coverage
        total_b = layer.coverage_a_building_limit + layer.coverage_b_other_structures_limit.selected
        building_coverage = max(total_b - const.flood_excess_limit_dict['building'],0)
        peril_coverage.xs_building_coverage.calculated = min(building_coverage,const.xs_flood_limit_available)

        # xs contents coverage
        total_c = layer.coverage_c_personal_property_limit.selected
        remaining_limit_after_building = const.xs_flood_limit_available - peril_coverage.xs_building_coverage.selected
        contents_coverage = max(total_c - const.flood_excess_limit_dict['contents'],0)
        peril_coverage.xs_contents_coverage.calculated = min(contents_coverage,remaining_limit_after_building)

        # Get XS flood deductible    
        if total_b == 0:
            building_prop = 0            
            xsfl_building_ded_perc = 1
        else:
            building_prop = (total_b) / (total_b + total_c)
            xsfl_building_ded_perc = min(const.flood_excess_limit_dict['building'] / total_b ,1)
        
        if total_c == 0:
            contents_prop = 0
            xsfl_contents_ded_perc = 1
        else:
            contents_prop = (total_c) / (total_b + total_c)
            xsfl_contents_ded_perc = min(const.flood_excess_limit_dict['contents'] / total_c ,1)


        xsfl_b_ded_impact = get_deductible_impact(peril_variable, xsfl_building_ded_perc)
        xsfl_c_ded_impact = get_deductible_impact(peril_variable, xsfl_contents_ded_perc)

        xsfl_ded_impact = building_prop * xsfl_b_ded_impact + contents_prop * xsfl_c_ded_impact        

        # gross model premium
        effective_rate = calculate_effective_rate(peril_coverage) * xsfl_ded_impact
        contents_and_building = sum([peril_coverage.xs_building_coverage.selected, peril_coverage.xs_contents_coverage.selected])
        peril_coverage.model_premium = effective_rate * contents_and_building

        # model rate
        peril_coverage.model_rate = effective_rate

        #### Excess Wind & Hail Deductible ####
        if hxd.cds.rating_factors.product_line == "Excess Wind & Hail":

            peril_column = 'WS' 
            peril_variable = 'ws'
            peril_coverage = getattr(layer.coverages, peril_variable)

            # W&H XS amounts
            peril_coverage.xs_building_coverage.calculated = max(total_b - const.xs_wind_hail_limit_dict['building'],0)
            peril_coverage.xs_contents_coverage.calculated = max(total_c - const.xs_wind_hail_limit_dict['contents'],0)                      

            # proportions
            if total_b == 0:
                building_prop = 0
                ws_building_ded_perc = 1
            else:
                building_prop = total_b / (total_b + total_c)
                ws_building_ded_perc = min(const.xs_wind_hail_limit_dict['building'] / total_b, 1)

            if total_c == 0:
                contents_prop = 0
                ws_contents_ded_perc = 1
            else:
                contents_prop = total_c / (total_b + total_c)
                ws_contents_ded_perc = min(const.xs_wind_hail_limit_dict['contents'] / total_c, 1)

            # deductible impact
            xswh_b_ded_impact = get_deductible_impact(peril_variable, ws_building_ded_perc)
            xswh_c_ded_impact = get_deductible_impact(peril_variable, ws_contents_ded_perc)

            xswh_ded_impact = (
                building_prop * xswh_b_ded_impact +
                contents_prop * xswh_c_ded_impact
            )

            # premium calculation 
            effective_rate = calculate_effective_rate(peril_coverage) * xswh_ded_impact
            xswh_contents_and_building = sum([peril_coverage.xs_building_coverage.selected, peril_coverage.xs_contents_coverage.selected])
            

            peril_coverage.model_premium = effective_rate * xswh_contents_and_building
            peril_coverage.model_rate = effective_rate

    
        # Calculate AOP Breakdown
        peril_variable = "aop"
        peril_coverage = getattr(layer.coverages, peril_variable)

        aop_mp = peril_coverage.model_premium or 0
        aop_mr = peril_coverage.model_rate or 0  # Assuming model_rate needs similar splitting

        # Define peril categories and their corresponding lookup keys
        peril_categories = {
            "model_premium_water_damage": "Water Damage",
            "model_premium_hail": "Hail/Wind",
            "model_premium_fire": "Fire",
            "model_premium_other": "Other",
        }

        # Assign model premium and model rate values dynamically
        for attr_suffix, peril in peril_categories.items():
            proportion = get_lookup_value(
                hx.params.table_aop_split, "Base Rate Proportions", peril, reference_column="Peril"
            )
            setattr(peril_coverage, attr_suffix, aop_mp * proportion)
            setattr(peril_coverage, attr_suffix.replace("premium", "rate"), aop_mr * proportion)
        
        sublimits_mapping = {
            "animal_included": "animal_dropdown_options",
            "diving_board_and_pool_included": "diving_board_dropdown_options",
            "trampoline_included": "trampoline_dropdown_options",
            "swimming_pool_included": "swimming_pool_dropdown_options"
        }
        
        for sublimit, dropdown in sublimits_mapping.items():
            coverage_l_value = layer.coverage_l_liability_limit.selected

            if getattr(layer.sublimits, sublimit) and (coverage_l_value and coverage_l_value > 0):
                dropdown_list = [25000, coverage_l_value]
            else:
                dropdown_list = []

            setattr(layer.sublimits, dropdown, dropdown_list)

    # Handling wildfire score
    if hxd.cds.option_to_show:
        option_to_show = hxd.cds.option_to_show - 1
    else:
        option_to_show = 0 #just default to show option 1
    layer_coverage = hxd.cds.layers[option_to_show].coverages
    hxd.cds.rating_factors.wildfire.wildfire_score.factor = layer_coverage.wildfire.wildfire_score

def calculate_factor_variances(hxd):
    """ Calculate variances between option to bind and shown option """
    rating_factors = hxd.cds.rating_factors
    for peril_name, (peril_variable, factor_list) in const.peril_configs.items():
        factor_list_with_modifier_impact = factor_list + ['total_modifier_impact']
        peril_structure = getattr(rating_factors,peril_variable)
        for factor in factor_list_with_modifier_impact:
            factor_structure = getattr(peril_structure,factor)
            if factor_structure.factor is None:
                continue
            if factor_structure.option_to_bind_factor is None:
                factor_structure.option_to_bind_factor = factor_structure.factor
            factor_structure.variance = utils.signed_percentage_difference(
                float(factor_structure.factor),
                float(factor_structure.option_to_bind_factor)
                )


def calculate_final_kpis(hxd):
    """Calculate final KPIs section"""

    for layer_number,layer in enumerate(hxd.cds.layers,start=1):
        # Coverage Split
        tiv_value = layer.coverages.aop.tiv.value or 1
        tiv_split = layer.kpis.tiv_split

        # Calculate percentages for coverage
        tiv_split.cov_a_perc = layer.coverage_a_building_limit / tiv_value
        tiv_split.cov_b_perc = layer.coverage_b_other_structures_limit.selected / tiv_value
        tiv_split.cov_c_perc = layer.coverage_c_personal_property_limit.selected / tiv_value
        tiv_split.others_perc = 1 - sum([tiv_split.cov_a_perc, tiv_split.cov_b_perc, tiv_split.cov_c_perc])

        # Peril Split
        total_expected_loss_cost = 0
        total_technical_premium = 0

        for peril, (variable_name, _) in const.peril_configs.items():
            layer_coverage = layer.coverages
            coverage_attr = getattr(layer_coverage, variable_name)         
                                
            # Go through all the include peril flags
            if coverage_attr.include_peril.value:
                if hxd.cds.rating_factors.product_line in 'Excess Flood' and peril not in ('Excess FL', 'Liability'):
                    coverage_attr.expected_loss_cost = 0
                    coverage_attr.technical_premium = 0
                elif hxd.cds.rating_factors.product_line in 'Excess Wind & Hail' and peril not in ('WS', 'Liability'):
                    coverage_attr.expected_loss_cost = 0
                    coverage_attr.technical_premium = 0
                elif hxd.cds.rating_factors.product_line in 'Monoline Earthquake' and peril not in ('EQ', 'Liability'):
                    coverage_attr.expected_loss_cost = 0
                    coverage_attr.technical_premium = 0
                else:
                    # Calculate expected loss cost and technical premium for each peril
                    expected_loss_cost = coverage_attr.model_premium #* const.target_loss_ratios_dict[peril]
                    coverage_attr.expected_loss_cost = expected_loss_cost
                    total_expected_loss_cost += expected_loss_cost

                    # Calculate technical premium
                    tp_uplift = getattr(hxd.cds.tp_uplift, variable_name)
                    technical_premium = expected_loss_cost * tp_uplift.tp_uplift_factor.factor
                
                    if peril != 'PAF':
                        technical_premium = technical_premium / (1-hxd.cds.brokerage.selected) #if hxd.cds.brokerage.selected else 0
                    else:
                        technical_premium = technical_premium * const.target_loss_ratios_dict['PAF'] / (1-0.275) # TODO: Check magic number
                    coverage_attr.technical_premium = technical_premium 
                    total_technical_premium += technical_premium
            else:
                coverage_attr.expected_loss_cost = 0
                coverage_attr.technical_premium = 0

        layer.expected_loss_cost = total_expected_loss_cost

        # Calculate peril split percentages
        pflr_split = layer.kpis.pflr_split
        for peril, (variable_name, _) in const.peril_configs.items():
            coverage_attr = getattr(layer.coverages, variable_name)
            setattr(pflr_split, f"{variable_name}_perc", coverage_attr.expected_loss_cost / total_expected_loss_cost if total_expected_loss_cost else 0)

        # Calculate AOP peril split percentages
        table_aop_split = hx.params.table_aop_split
        pflr_split.water_damage_perc = pflr_split.aop_perc * table_aop_split[table_aop_split['Peril']=='Water Damage']['Base Rate Proportions'].iloc[0]
        pflr_split.hail_perc = pflr_split.aop_perc * table_aop_split[table_aop_split['Peril']=='Hail/Wind']['Base Rate Proportions'].iloc[0]
        pflr_split.fire_perc = pflr_split.aop_perc * table_aop_split[table_aop_split['Peril']=='Fire']['Base Rate Proportions'].iloc[0]
        pflr_split.other_perc = pflr_split.aop_perc * table_aop_split[table_aop_split['Peril']=='Other']['Base Rate Proportions'].iloc[0]
        

        # Rates and premiums
        hxd.cds.kpis_show_rates = hxd.cds.kpis_rate_premium_toggle == 'Rate per 100 TIV'
        hxd.cds.kpis_show_premiums = not hxd.cds.kpis_show_rates

        # Sum of limits for rate calculations
        sum_of_limits = sum([
            layer.coverage_a_building_limit,
            layer.coverage_b_other_structures_limit.selected,
            layer.coverage_c_personal_property_limit.selected,
            layer.coverage_d_loss_of_use_limit.selected
        ])

        # Calculate technical premiums and rates        
        layer.kpis.hvh.technical_premium.rate = (total_technical_premium - layer.coverages.paf.technical_premium) / sum_of_limits * 100 if sum_of_limits else 0
        layer.kpis.paf.technical_premium.rate = layer.coverages.paf.technical_premium / hxd.cds.exposure.aggregate.paf.tiv * 100 if hxd.cds.exposure.aggregate.paf.tiv else 0
        limits_plus_paf = sum([sum_of_limits, hxd.cds.exposure.aggregate.paf.tiv])
        layer.kpis.total.technical_premium.rate = total_technical_premium / limits_plus_paf * 100 if limits_plus_paf else 0

        layer.kpis.hvh.technical_premium.premium = round(total_technical_premium - layer.coverages.paf.technical_premium)
        layer.kpis.paf.technical_premium.premium = round(layer.coverages.paf.technical_premium)
        layer.kpis.total.technical_premium.premium = layer.kpis.paf.technical_premium.premium + layer.kpis.hvh.technical_premium.premium

        # Calculate HVH pre adj commercial premiums and rates
        calculate_hvh_commerical_rate(hxd,layer)
        if layer.kpis.hvh.commercial_premium_pre_uw_adj.rate is not None:
            if hxd.cds.rating_factors.product_line == "Excess Flood":
                # xs building coverage
                total_b = layer.coverage_a_building_limit + layer.coverage_b_other_structures_limit.selected
                building_coverage = max(total_b - const.flood_excess_limit_dict['building'],0)
                xs_building_coverage = min(building_coverage,const.xs_flood_limit_available)

                # xs contents coverage
                total_c = layer.coverage_c_personal_property_limit.selected
                remaining_limit_after_building = const.xs_flood_limit_available - xs_building_coverage
                contents_coverage = max(total_c - const.flood_excess_limit_dict['contents'],0)
                xs_contents_coverage = min(contents_coverage,remaining_limit_after_building)

                # xsfl commercial premium
                layer.kpis.hvh.commercial_premium_pre_uw_adj.premium = round(layer.kpis.hvh.commercial_premium_pre_uw_adj.rate * (xs_building_coverage + xs_contents_coverage) / 100)

            else:
                layer.kpis.hvh.commercial_premium_pre_uw_adj.premium = round(layer.kpis.hvh.commercial_premium_pre_uw_adj.rate * sum_of_limits / 100)
        # Calculate PAF pre adj commercial premiums
        if  hxd.cds.rating_factors.product_line in ("Excess Flood", "Excess Wind & Hail", "Monoline Earthquake"):
            layer.kpis.paf.commercial_premium_pre_uw_adj.premium = 0
            layer.kpis.paf.commercial_premium_pre_uw_adj.rate = 0
        else:
            layer.kpis.paf.commercial_premium_pre_uw_adj.premium = round(layer.coverages.paf.model_premium)
            layer.kpis.paf.commercial_premium_pre_uw_adj.rate = layer.kpis.paf.commercial_premium_pre_uw_adj.premium / hxd.cds.exposure.aggregate.paf.tiv * 100 if hxd.cds.exposure.aggregate.paf.tiv else 0

        # Set post adj commercial values to pre values
        if layer.kpis.hvh.commercial_premium_pre_uw_adj.rate:
            layer.kpis.hvh.commercial_premium.rate.calculated = layer.kpis.hvh.commercial_premium_pre_uw_adj.rate
            layer.kpis.hvh.commercial_premium.premium.calculated = layer.kpis.hvh.commercial_premium_pre_uw_adj.premium

        layer.kpis.paf.commercial_premium.premium.calculated = layer.kpis.paf.commercial_premium_pre_uw_adj.premium
        layer.kpis.paf.commercial_premium.rate.calculated = layer.kpis.paf.commercial_premium_pre_uw_adj.rate

        # Calculate HVH pre and post adj splits
        if hxd.cds.kpis_show_rates:
            total_pre_adj_value = layer.kpis.hvh.commercial_premium_pre_uw_adj.rate
            total_post_adj_node = layer.kpis.hvh.commercial_premium.rate
            pre_uw_obj = layer.kpis.hvh.commercial_premium_pre_uw_adj.rate_splits
            post_uw_obj = layer.kpis.hvh.commercial_premium.rate_splits

            if hxd.cds.show_commercial_premium_breakdown:
                hxd.cds.show_rate_splits = True
                hxd.cds.show_premium_splits = False

        elif hxd.cds.kpis_show_premiums:
            total_pre_adj_value = layer.kpis.hvh.commercial_premium_pre_uw_adj.premium
            total_post_adj_node = layer.kpis.hvh.commercial_premium.premium
            pre_uw_obj = layer.kpis.hvh.commercial_premium_pre_uw_adj.premium_splits
            post_uw_obj = layer.kpis.hvh.commercial_premium.premium_splits

            if hxd.cds.show_commercial_premium_breakdown:
                hxd.cds.show_premium_splits = True
                hxd.cds.show_rate_splits = False

        else:
            total_pre_adj_value = None
            total_post_adj_node = None
            pre_uw_obj = None
            post_uw_obj = None

        def effective_override_value(node):
            if node is None:
                return None
            if getattr(node, "is_overridden", False) and node.selected is not None:
                return node.selected
            return node.calculated

        def effective_split_value(node):
            if getattr(node, "is_overridden", False) and node.selected is not None:
                return node.selected
            return node.calculated or 0


        # For EB, set the commercial premium to the flat rates
        # W:\Finance\Actuarial\Pricing\01 - Property\02 - BUSA Homeowners\2026\6. EB Rates
        # Special handling for eb base rate
        eb_base_rate_table = hx.params.table_base_rate
        eb_base_rate_table = eb_base_rate_table[
            eb_base_rate_table['Lookup code'].str.contains("Base Premium Coverage A Limit", na=False)
        ]

        # Create key mapping for lookup
        key_mapping = dict(zip(eb_base_rate_table["Values"].astype(int), eb_base_rate_table["Lookup code"]))
        lookup_keys = sorted(key_mapping.keys())

        # Determine the correct lookup code based on limit
        limit = layer.coverage_a_building_limit
        lookup_code = next(
            (key_mapping[key] for key in reversed(lookup_keys) if key <= limit),
            key_mapping[min(lookup_keys)]
        )
        # Calculate effective rate
        eb_base_premium = get_lookup_value(eb_base_rate_table, 'Equipment breakdown', lookup_code)

        if layer.coverages.eb.include_peril.value == False:
            layer.kpis.pflr_split.eb_perc = 0
        elif hxd.cds.rating_factors.product_line in ['Monoline Earthquake', 'Excess Flood', 'Excess Wind & Hail']:
            layer.kpis.pflr_split.eb_perc = 0
        else:            
            layer.kpis.pflr_split.eb_perc = eb_base_premium /  layer.kpis.hvh.commercial_premium_pre_uw_adj.premium if layer.kpis.hvh.commercial_premium_pre_uw_adj.premium else 0           
        
        layer.kpis.pflr_split.eq_perc = layer.kpis.hvh.commercial_premium_pre_uw_adj.rate_splits.eq / layer.kpis.hvh.commercial_premium_pre_uw_adj.rate if layer.kpis.hvh.commercial_premium_pre_uw_adj.rate_splits.eq else 0
        layer.kpis.pflr_split.fl_perc = layer.kpis.hvh.commercial_premium_pre_uw_adj.rate_splits.excess_flood / layer.kpis.hvh.commercial_premium_pre_uw_adj.rate if layer.kpis.hvh.commercial_premium_pre_uw_adj.rate_splits.excess_flood else 0        

        ho_perc = 1 - (layer.kpis.pflr_split.eq_perc + layer.kpis.pflr_split.fl_perc + layer.kpis.pflr_split.eb_perc)

        # Pre Adj splits
        if total_pre_adj_value is not None and pre_uw_obj:
            
            pre_uw_obj.eq = total_pre_adj_value * layer.kpis.pflr_split.eq_perc if layer.kpis.pflr_split.eq_perc else 0
            pre_uw_obj.excess_flood = total_pre_adj_value * layer.kpis.pflr_split.fl_perc if layer.kpis.pflr_split.fl_perc else 0            
            pre_uw_obj.equipment_breakdown = total_pre_adj_value * layer.kpis.pflr_split.eb_perc if layer.kpis.pflr_split.eb_perc else 0            
            pre_uw_obj.ho = total_pre_adj_value - pre_uw_obj.eq - pre_uw_obj.excess_flood - pre_uw_obj.equipment_breakdown

            if hxd.cds.kpis_show_premiums:
                # calculate rate splits also
                layer.kpis.hvh.commercial_premium_pre_uw_adj.rate_splits.ho = layer.kpis.hvh.commercial_premium_pre_uw_adj.rate * ho_perc if ho_perc else 0
                layer.kpis.hvh.commercial_premium_pre_uw_adj.rate_splits.eq = layer.kpis.hvh.commercial_premium_pre_uw_adj.rate * layer.kpis.pflr_split.eq_perc if layer.kpis.pflr_split.eq_perc else 0
                layer.kpis.hvh.commercial_premium_pre_uw_adj.rate_splits.excess_flood = layer.kpis.hvh.commercial_premium_pre_uw_adj.rate * layer.kpis.pflr_split.fl_perc if layer.kpis.pflr_split.fl_perc else 0
                layer.kpis.hvh.commercial_premium_pre_uw_adj.rate_splits.equipment_breakdown = layer.kpis.hvh.commercial_premium_pre_uw_adj.rate * layer.kpis.pflr_split.eb_perc if layer.kpis.pflr_split.eb_perc else 0

                # round values
                total_pre_adj_value = round(total_pre_adj_value)
                pre_uw_obj.eq = round(total_pre_adj_value * layer.kpis.pflr_split.eq_perc) if layer.kpis.pflr_split.eq_perc else 0
                pre_uw_obj.excess_flood = round(total_pre_adj_value * layer.kpis.pflr_split.fl_perc) if layer.kpis.pflr_split.fl_perc else 0            
                pre_uw_obj.equipment_breakdown = round(total_pre_adj_value * layer.kpis.pflr_split.eb_perc) if layer.kpis.pflr_split.eb_perc else 0            
                pre_uw_obj.ho = total_pre_adj_value - pre_uw_obj.eq - pre_uw_obj.excess_flood - pre_uw_obj.equipment_breakdown

            elif hxd.cds.kpis_show_rates:                
                # calculate premium splits also
                layer.kpis.hvh.commercial_premium.premium.calculated = round(layer.kpis.hvh.commercial_premium.premium.selected)
                layer.kpis.hvh.commercial_premium.premium_splits.eq.calculated = round(layer.kpis.hvh.commercial_premium.premium.selected * layer.kpis.pflr_split.eq_perc)if layer.kpis.pflr_split.eq_perc else 0
                layer.kpis.hvh.commercial_premium.premium_splits.excess_flood.calculated = round(layer.kpis.hvh.commercial_premium.premium.selected * layer.kpis.pflr_split.fl_perc) if layer.kpis.pflr_split.fl_perc else 0
                layer.kpis.hvh.commercial_premium.premium_splits.equipment_breakdown.calculated = round(layer.kpis.hvh.commercial_premium.premium.selected * layer.kpis.pflr_split.eb_perc) if layer.kpis.pflr_split.eb_perc else 0

                # balancing item
                layer.kpis.hvh.commercial_premium.premium_splits.ho.calculated = layer.kpis.hvh.commercial_premium.premium.selected - layer.kpis.hvh.commercial_premium.premium_splits.eq.calculated - layer.kpis.hvh.commercial_premium.premium_splits.excess_flood.calculated - layer.kpis.hvh.commercial_premium.premium_splits.equipment_breakdown.calculated

        # Post Adj splits: restore old behaviour, but populate .calculated on override nodes
        total_post_adj_value = effective_override_value(total_post_adj_node)
        if total_post_adj_value is not None and post_uw_obj:
            
            post_uw_obj.eq.calculated = total_post_adj_value * layer.kpis.pflr_split.eq_perc if layer.kpis.pflr_split.eq_perc else 0
            post_uw_obj.excess_flood.calculated = total_post_adj_value * layer.kpis.pflr_split.fl_perc if layer.kpis.pflr_split.fl_perc else 0
            post_uw_obj.equipment_breakdown.calculated = total_post_adj_value * layer.kpis.pflr_split.eb_perc if layer.kpis.pflr_split.eb_perc else 0
            post_uw_obj.ho.calculated = total_post_adj_value - post_uw_obj.eq.calculated - post_uw_obj.excess_flood.calculated - post_uw_obj.equipment_breakdown.calculated

            if hxd.cds.kpis_show_premiums:
                # calculate rate splits also
                layer.kpis.hvh.commercial_premium.rate_splits.ho.calculated = layer.kpis.hvh.commercial_premium.rate.selected * ho_perc if ho_perc else 0
                layer.kpis.hvh.commercial_premium.rate_splits.eq.calculated = layer.kpis.hvh.commercial_premium.rate.selected * layer.kpis.pflr_split.eq_perc if layer.kpis.pflr_split.eq_perc else 0
                layer.kpis.hvh.commercial_premium.rate_splits.excess_flood.calculated = layer.kpis.hvh.commercial_premium.rate.selected * layer.kpis.pflr_split.fl_perc if layer.kpis.pflr_split.fl_perc else 0
                layer.kpis.hvh.commercial_premium.rate_splits.equipment_breakdown.calculated = layer.kpis.hvh.commercial_premium.rate.selected * layer.kpis.pflr_split.eb_perc if layer.kpis.pflr_split.eb_perc else 0

                # round values
                total_post_adj_value = round(total_post_adj_value)
                post_uw_obj.eq.calculated = round(total_post_adj_value * layer.kpis.pflr_split.eq_perc) if layer.kpis.pflr_split.eq_perc else 0
                post_uw_obj.excess_flood.calculated = round(total_post_adj_value * layer.kpis.pflr_split.fl_perc) if layer.kpis.pflr_split.fl_perc else 0
                post_uw_obj.equipment_breakdown.calculated = round(total_post_adj_value * layer.kpis.pflr_split.eb_perc) if layer.kpis.pflr_split.eb_perc else 0
                post_uw_obj.ho.calculated = total_post_adj_value - post_uw_obj.eq.calculated - post_uw_obj.excess_flood.calculated - post_uw_obj.equipment_breakdown.calculated

            elif hxd.cds.kpis_show_rates:
                # calculate premium splits also
                layer.kpis.hvh.commercial_premium.premium.calculated = round(layer.kpis.hvh.commercial_premium.premium.selected)
                layer.kpis.hvh.commercial_premium.premium_splits.eq.calculated = round(layer.kpis.hvh.commercial_premium.premium.selected * layer.kpis.pflr_split.eq_perc) if layer.kpis.pflr_split.eq_perc else 0
                layer.kpis.hvh.commercial_premium.premium_splits.excess_flood.calculated = round(layer.kpis.hvh.commercial_premium.premium.selected * layer.kpis.pflr_split.fl_perc) if layer.kpis.pflr_split.fl_perc else 0
                layer.kpis.hvh.commercial_premium.premium_splits.equipment_breakdown.calculated = round(layer.kpis.hvh.commercial_premium.premium.selected * layer.kpis.pflr_split.eb_perc) if layer.kpis.pflr_split.eb_perc else 0

                # balancing item for rounded numbers.
                layer.kpis.hvh.commercial_premium.premium_splits.ho.calculated = layer.kpis.hvh.commercial_premium.premium.selected - layer.kpis.hvh.commercial_premium.premium_splits.eq.calculated - layer.kpis.hvh.commercial_premium.premium_splits.excess_flood.calculated - layer.kpis.hvh.commercial_premium.premium_splits.equipment_breakdown.calculated


        # Total post adj output = sum of effective split values
        splits = ["ho", "eq", "excess_flood", "equipment_breakdown"]
        post_adj_value = sum(effective_split_value(getattr(post_uw_obj, split)) for split in splits) if post_uw_obj else 0

        if hxd.cds.kpis_show_rates:
            layer.kpis.hvh.commercial_premium.rate.calculated = post_adj_value
            layer.kpis.hvh.commercial_premium.premium.calculated = post_adj_value * sum_of_limits / 100 if sum_of_limits else 0
        elif hxd.cds.kpis_show_premiums:
            layer.kpis.hvh.commercial_premium.premium.calculated = post_adj_value
            layer.kpis.hvh.commercial_premium.rate.calculated = post_adj_value / sum_of_limits * 100 if sum_of_limits else 0
        
        # Apply overrides (split level)
        # if rate overridden, premium should change accordingly
        if layer.kpis.hvh.commercial_premium.rate_splits.ho.is_overridden is True:
            layer.kpis.hvh.commercial_premium.premium_splits.ho.calculated = round(layer.kpis.hvh.commercial_premium.rate_splits.ho.selected * sum_of_limits / 100)

        if layer.kpis.hvh.commercial_premium.rate_splits.eq.is_overridden is True:
            layer.kpis.hvh.commercial_premium.premium_splits.eq.calculated = round(layer.kpis.hvh.commercial_premium.rate_splits.eq.selected * sum_of_limits / 100)

        if layer.kpis.hvh.commercial_premium.rate_splits.excess_flood.is_overridden is True:
            layer.kpis.hvh.commercial_premium.premium_splits.excess_flood.calculated = round(layer.kpis.hvh.commercial_premium.rate_splits.excess_flood.selected * sum_of_limits / 100)

        if layer.kpis.hvh.commercial_premium.rate_splits.equipment_breakdown.is_overridden is True:
            layer.kpis.hvh.commercial_premium.premium_splits.equipment_breakdown.calculated = round(layer.kpis.hvh.commercial_premium.rate_splits.equipment_breakdown.selected * sum_of_limits / 100)

        # if premium overridden, rate should change accordingly
        if layer.kpis.hvh.commercial_premium.premium_splits.ho.is_overridden is True:
            layer.kpis.hvh.commercial_premium.rate_splits.ho.calculated = layer.kpis.hvh.commercial_premium.premium_splits.ho.selected / sum_of_limits * 100 if sum_of_limits else 0

        if layer.kpis.hvh.commercial_premium.premium_splits.eq.is_overridden is True:
            layer.kpis.hvh.commercial_premium.rate_splits.eq.calculated = layer.kpis.hvh.commercial_premium.premium_splits.eq.selected / sum_of_limits * 100 if sum_of_limits else 0

        if layer.kpis.hvh.commercial_premium.premium_splits.excess_flood.is_overridden is True:
            layer.kpis.hvh.commercial_premium.rate_splits.excess_flood.calculated = layer.kpis.hvh.commercial_premium.premium_splits.excess_flood.selected / sum_of_limits * 100 if sum_of_limits else 0

        if layer.kpis.hvh.commercial_premium.premium_splits.equipment_breakdown.is_overridden is True:
            layer.kpis.hvh.commercial_premium.rate_splits.equipment_breakdown.calculated = layer.kpis.hvh.commercial_premium.premium_splits.equipment_breakdown.selected / sum_of_limits * 100 if sum_of_limits else 0

        # Apply overrides (total level)
        # if total rate overridden, total premium should change accordingly
        if layer.kpis.hvh.commercial_premium.rate.is_overridden is True:
            layer.kpis.hvh.commercial_premium.premium.calculated = round(layer.kpis.hvh.commercial_premium.rate.selected * sum_of_limits / 100)

        if (layer.kpis.hvh.commercial_premium.rate_splits.ho.is_overridden is True
            or layer.kpis.hvh.commercial_premium.rate_splits.eq.is_overridden is True
            or layer.kpis.hvh.commercial_premium.rate_splits.excess_flood.is_overridden is True
            or layer.kpis.hvh.commercial_premium.rate_splits.equipment_breakdown.is_overridden is True):
            layer.kpis.hvh.commercial_premium.premium.calculated = sum([round((layer.kpis.hvh.commercial_premium.rate_splits.ho.selected or 0) * sum_of_limits / 100),
            round((layer.kpis.hvh.commercial_premium.rate_splits.eq.selected or 0) * sum_of_limits / 100),
            round((layer.kpis.hvh.commercial_premium.rate_splits.excess_flood.selected or 0) * sum_of_limits / 100),            
            round((layer.kpis.hvh.commercial_premium.rate_splits.equipment_breakdown.selected or 0) * sum_of_limits / 100)])

            layer.kpis.hvh.commercial_premium.rate.calculated = sum([(layer.kpis.hvh.commercial_premium.rate_splits.ho.selected or 0),
            (layer.kpis.hvh.commercial_premium.rate_splits.eq.selected or 0),
            (layer.kpis.hvh.commercial_premium.rate_splits.excess_flood.selected or 0),
            (layer.kpis.hvh.commercial_premium.rate_splits.equipment_breakdown.selected or 0)
            ])

        if layer.kpis.paf.commercial_premium.rate.is_overridden is True:
            layer.kpis.paf.commercial_premium.premium.calculated = round(layer.kpis.paf.commercial_premium.rate.selected *  hxd.cds.exposure.aggregate.paf.tiv / 100)

        # if premium overridden, rate should change accordingly
        if layer.kpis.hvh.commercial_premium.premium.is_overridden is True:
            layer.kpis.hvh.commercial_premium.rate.calculated = layer.kpis.hvh.commercial_premium.premium.selected / sum_of_limits * 100 if sum_of_limits else 0

        if (layer.kpis.hvh.commercial_premium.premium_splits.ho.is_overridden is True
            or layer.kpis.hvh.commercial_premium.premium_splits.eq.is_overridden is True
            or layer.kpis.hvh.commercial_premium.premium_splits.excess_flood.is_overridden is True
            or layer.kpis.hvh.commercial_premium.premium_splits.equipment_breakdown.is_overridden is True):
            layer.kpis.hvh.commercial_premium.rate.calculated = sum([(layer.kpis.hvh.commercial_premium.premium_splits.ho.selected or 0),
            (layer.kpis.hvh.commercial_premium.premium_splits.eq.selected or 0),
            (layer.kpis.hvh.commercial_premium.premium_splits.excess_flood.selected or 0),
            (layer.kpis.hvh.commercial_premium.premium_splits.equipment_breakdown.selected or 0)]) / sum_of_limits * 100

        if layer.kpis.paf.commercial_premium.premium.is_overridden is True:
            layer.kpis.paf.commercial_premium.rate.calculated = layer.kpis.paf.commercial_premium.premium.selected / hxd.cds.exposure.aggregate.paf.tiv * 100 if hxd.cds.exposure.aggregate.paf.tiv else 0

        # Validate overrides
        if layer.kpis.hvh.commercial_premium.premium.selected is not None and layer.kpis.hvh.commercial_premium.rate.selected is not None:
            premium_override_value = layer.kpis.hvh.commercial_premium.premium.selected
            rate_equivalent_premium_value = layer.kpis.hvh.commercial_premium.rate.selected * sum_of_limits / 100

            if not math.isclose(premium_override_value, rate_equivalent_premium_value, rel_tol=1e-3, abs_tol=1):             
                hx.errors.validation(f'HVH commercial rate and premium are not aligned please check the override values in option {layer_number}.')


            if hxd.cds.kpis_rate_premium_toggle == 'Rate per 100 TIV':
                rate_split_total_value = sum([(layer.kpis.hvh.commercial_premium.rate_splits.ho.selected or 0),
                (layer.kpis.hvh.commercial_premium.rate_splits.eq.selected or 0),
                (layer.kpis.hvh.commercial_premium.rate_splits.excess_flood.selected or 0),
                (layer.kpis.hvh.commercial_premium.rate_splits.equipment_breakdown.selected or 0)])  * sum_of_limits / 100                                       
            elif hxd.cds.kpis_rate_premium_toggle == 'Premium': 
                premium_split_total_value = sum([(layer.kpis.hvh.commercial_premium.premium_splits.ho.selected or  0),
                (layer.kpis.hvh.commercial_premium.premium_splits.eq.selected or 0),
                (layer.kpis.hvh.commercial_premium.premium_splits.excess_flood.selected or  0),
                (layer.kpis.hvh.commercial_premium.premium_splits.equipment_breakdown.selected or 0)])

            
            if hxd.cds.kpis_rate_premium_toggle == 'Premium': 
                if not math.isclose(premium_override_value, premium_split_total_value, rel_tol=1e-3, abs_tol=1):             
                    hx.errors.validation(f'HVH commercial premium splits do not sum to total in option {layer_number}.')

            if hxd.cds.kpis_rate_premium_toggle == 'Rate per 100 TIV': 
                if not math.isclose(rate_equivalent_premium_value, rate_split_total_value, rel_tol=1e-3, abs_tol=1):             
                    hx.errors.validation(f'HVH commercial rate splits do not sum to total in option {layer_number}.')
                        

        if layer.kpis.paf.commercial_premium.premium.selected is not None and layer.kpis.paf.commercial_premium.rate.selected is not None:
            premium_override_value = layer.kpis.paf.commercial_premium.premium.selected
            rate_equivalent_premium_value = layer.kpis.paf.commercial_premium.rate.selected * hxd.cds.exposure.aggregate.paf.tiv / 100
            if not math.isclose(premium_override_value, rate_equivalent_premium_value, rel_tol=1e-3, abs_tol=1):
                hx.errors.validation(f'PAF commercial rate and premium are not aligned please check the override values in option {layer_number}.')           
                       
        # Total commercial premiums
        if layer.kpis.hvh.commercial_premium_pre_uw_adj.premium is not None and layer.kpis.paf.commercial_premium_pre_uw_adj.premium is not None:
            layer.kpis.total.commercial_premium_pre_uw_adj.premium = layer.kpis.hvh.commercial_premium_pre_uw_adj.premium + layer.kpis.paf.commercial_premium_pre_uw_adj.premium
        if layer.kpis.hvh.commercial_premium.premium.selected is not None and layer.kpis.paf.commercial_premium.premium.selected is not None:
            layer.kpis.total.commercial_premium.premium = layer.kpis.hvh.commercial_premium.premium.selected + layer.kpis.paf.commercial_premium.premium.selected

        # Underwriting adjustments
        if layer.kpis.hvh.commercial_premium_pre_uw_adj.premium:
            layer.kpis.hvh.modifiers.uw_adjustment = layer.kpis.hvh.commercial_premium.premium.selected / layer.kpis.hvh.commercial_premium_pre_uw_adj.premium - 1

        if layer.kpis.paf.commercial_premium_pre_uw_adj.premium:
            layer.kpis.paf.modifiers.uw_adjustment = layer.kpis.paf.commercial_premium.premium.selected / layer.kpis.paf.commercial_premium_pre_uw_adj.premium - 1

        # Total TPI adjustments
        if layer.kpis.total.commercial_premium_pre_uw_adj.premium:
            layer.kpis.total.tpi_pre_uw_adj = (
                (layer.kpis.total.commercial_premium_pre_uw_adj.premium /  layer.kpis.total.technical_premium.premium)
                if layer.kpis.total.technical_premium.premium else 0
            )

        if layer.kpis.total.commercial_premium.premium:
            layer.kpis.total.tpi = (
                layer.kpis.total.commercial_premium.premium  / layer.kpis.total.technical_premium.premium
                if layer.kpis.total.technical_premium.premium else 0
            )

        # UW adjustment impact
        if layer.kpis.total.commercial_premium_pre_uw_adj.premium and layer.kpis.total.commercial_premium.premium:
            layer.uw_adj_impact = layer.kpis.total.commercial_premium.premium / layer.kpis.total.commercial_premium_pre_uw_adj.premium - 1


        # Rates for total commercial premiums
        layer.kpis.total.commercial_premium_pre_uw_adj.rate = (
            layer.kpis.total.commercial_premium_pre_uw_adj.premium / limits_plus_paf * 100
            if limits_plus_paf and layer.kpis.total.commercial_premium_pre_uw_adj.premium else 0
        )
        layer.kpis.total.commercial_premium.rate = (
            layer.kpis.total.commercial_premium.premium / limits_plus_paf * 100
            if limits_plus_paf and layer.kpis.total.commercial_premium.premium else 0
        )


def calculate_hvh_commerical_rate(hxd,layer):
    """
    Calculate the HVH commercial rates
    """
    county_rates = hx.params.table_county_commercial_rates
    state_rates = hx.params.table_state_commercial_rates
    state = hxd.cds.rating_factors.state
    county = hxd.cds.rating_factors.county
    nb_discount = hx.params.table_nb_discount

    # Attempt to fetch nb discount
    nb_discount_row = nb_discount[nb_discount['State Code'] == state] 

    # Attempt to fetch county-level rates
    county_row = county_rates[
        (county_rates['State Code'] == state) & 
        (county_rates['County'] == county)
    ]

    if not county_row.empty:
        row = county_row.iloc[0]
    else:
        # Fallback to state-level rates
        state_row = state_rates[state_rates['State Code'] == state]
        if state_row.empty:
            return  # No rates available, skip calculation
        row = state_row.iloc[0]

    if hxd.cds.standard_fields.is_renewal == True:
        base_attr_rate = row.get('Selected Attr (per 100 TIV)')
        base_cat_rate = row.get('Selected Cat (per 100 TIV)')
    else:
        base_attr_rate = row.get('Selected Attr (per 100 TIV)') * (1+ nb_discount_row.get('NB Discount').iloc[0])
        base_cat_rate = row.get('Selected Cat (per 100 TIV)') * (1+ nb_discount_row.get('NB Discount').iloc[0])

    if base_attr_rate is None or base_cat_rate is None:
        return  # Incomplete rate info, skip calculation

    # Calculate total base rates
    zip_code = hxd.cds.rating_factors.zip
    state = hxd.cds.rating_factors.state
    county = hxd.cds.rating_factors.county
    table_base_rate = hx.params.table_base_rate
    ws_zip_table = hx.params.table_ws_rates_zip
    ws_county_table = hx.params.table_ws_rates_county
    ws_state_table = hx.params.table_ws_rates_state
    raw_base_rates = {}
    raw_base_rates['aop'] = layer.coverages.aop.base_rate
    raw_base_rates['wildfire'] = layer.coverages.wildfire.base_rate
    raw_base_rates['liability'] = layer.coverages.liability.base_rate
    raw_base_rates['eq'] = layer.coverages.eq.base_rate

    # Special handling for eb base rate
    eb_base_rate_table = hx.params.table_base_rate
    eb_base_rate_table = eb_base_rate_table[
        eb_base_rate_table['Lookup code'].str.contains("Base Premium Coverage A Limit", na=False)
    ]

    # Create key mapping for lookup
    key_mapping = dict(zip(eb_base_rate_table["Values"].astype(int), eb_base_rate_table["Lookup code"]))
    lookup_keys = sorted(key_mapping.keys())

    # Determine the correct lookup code based on limit
    limit = layer.coverage_a_building_limit
    limit_total = (layer.coverage_a_building_limit +
     layer.coverage_b_other_structures_limit.selected +
     layer.coverage_c_personal_property_limit.selected +
      layer.coverage_d_loss_of_use_limit.selected)

    # Lookup based on coverage a
    lookup_code = next(
        (key_mapping[key] for key in reversed(lookup_keys) if key <= limit),
        key_mapping[min(lookup_keys)]
    )

    # Calculate effective rate
    base_premium = get_lookup_value(eb_base_rate_table, 'Equipment breakdown', lookup_code)   
    
    eb_base_premium = base_premium if base_premium else 0
    eb_base_rate = base_premium / (limit_total / 100) if limit_total != 0 else 0        
    # raw_base_rates['eb'] = eb_base_rate * const.target_loss_ratios_dict['Equipment breakdown']
    
    # Remove EB flat rates from attritional prem. will be added back on later.
    base_attr_rate = max(base_attr_rate - eb_base_rate,0)

    # Special handling for FL
    raw_base_rates['fl'] = table_base_rate[table_base_rate['Values']=='Base Rate']['Excess FL'].iloc[0]

    # Special handling for ws
    raw_base_rates['ws'] = (
        ws_zip_table[ws_zip_table['Zip'] == zip_code]['WS Rates'].iloc[0]
        if ws_zip_table[ws_zip_table['Zip'] == zip_code].shape[0] > 0 else
        ws_county_table[(ws_county_table['County'] == county)&(ws_county_table['State'] == state)]['WS Rates'].iloc[0]
        if ws_county_table[(ws_county_table['County'] == county)&(ws_county_table['State'] == state)].shape[0] > 0 else
        ws_state_table[ws_state_table['State'] == state]['WS Rates'].iloc[0]
        if ws_state_table[ws_state_table['State'] == state].shape[0] > 0 else 0
    )

    # DK EDIT - removed eb as using flat rates for eb comm premium
    attr_base_total = sum([
        raw_base_rates['aop'],
        raw_base_rates['wildfire'],
        raw_base_rates['fl'],
        raw_base_rates['liability']
        # raw_base_rates['eb']
    ])

    cat_base_total = sum([
        raw_base_rates['ws'],
        raw_base_rates['eq'],
    ])

    total_commercial_rate = 0

    for peril in const.all_perils:
        if peril == 'paf':
            continue

        coverage = getattr(layer.coverages, peril)
        rf_peril = getattr(hxd.cds.rating_factors, peril)

        # Build rate multiplier
        multiplier = 1
        for factor_key in const.base_commercial_rates_factors:            
            if factor_key in ['include_peril', 'assumed_tiv', 'deductible']:
                continue
            factor = getattr(rf_peril, factor_key).factor
            if factor:
                multiplier *= factor

        tiv_factor = getattr(coverage.tiv, 'factor', None)
        if tiv_factor:
            if peril in ['aop','liability','wildfire']:
                tiv = getattr(layer.coverages,peril).tiv.value
                tiv_factor = tiv_factor / (tiv/1_000_000) if tiv != 0 else 0
            multiplier *= tiv_factor

        # multiplier *= coverage.include_peril.value

        deductible_impact = getattr(coverage, 'deductible_impact', None)
        if deductible_impact:
            multiplier *= deductible_impact

        # Calculate final adjustment
        base_rel = getattr(hxd.cds.commercial_rates_base_rels, peril)
        adjustment = multiplier / base_rel

        # Apply to base rate                
        if peril in ['aop', 'wildfire', 'liability', 'fl'] and attr_base_total > 0:
            attr_split = raw_base_rates[peril] / attr_base_total            
            coverage.commercial_rates_rater_rels = adjustment * base_attr_rate * attr_split                   
        
        elif peril in ['ws', 'eq'] and cat_base_total > 0:
            cat_split = raw_base_rates[peril] / cat_base_total
            coverage.commercial_rates_rater_rels = adjustment * base_cat_rate * cat_split
        else:
            coverage.commercial_rates_rater_rels = 0  # Fallback for unsupported or missing base

        # Take into account peril include flag       
        
        if hxd.cds.rating_factors.product_line == "Excess Flood":
            # Liability coverage has no include/exclude flag and is dependent on coverage_l
            if peril == 'liability' and layer.coverage_l_liability_limit.selected == 0:
                coverage.commercial_rates_rater_rels = 0                
            elif peril in ['aop', 'wildfire', 'ws', 'eq', 'eb']:
                coverage.commercial_rates_rater_rels = 0

        elif hxd.cds.rating_factors.product_line == "Excess Wind & Hail":
            
            if peril == 'liability' and layer.coverage_l_liability_limit.selected == 0:
                coverage.commercial_rates_rater_rels = 0
            elif peril in ['aop', 'wildfire', 'fl', 'eq', 'eb']:
                coverage.commercial_rates_rater_rels = 0

        elif hxd.cds.rating_factors.product_line == "Monoline Earthquake":
            # Liability coverage has no include/exclude flag and is dependent on coverage_l
            if peril == 'liability' and layer.coverage_l_liability_limit.selected == 0:
                coverage.commercial_rates_rater_rels = 0
            elif peril in ['aop', 'wildfire', 'fl', 'ws']:
                coverage.commercial_rates_rater_rels = 0

        else:
            if coverage.include_peril.value is False:
                coverage.commercial_rates_rater_rels = 0        

            total_commercial_rate += coverage.commercial_rates_rater_rels        

        if peril in ['fl']:
            layer.kpis.hvh.commercial_premium_pre_uw_adj.rate_splits.excess_flood = coverage.commercial_rates_rater_rels

        if peril in ['eq']:
            layer.kpis.hvh.commercial_premium_pre_uw_adj.rate_splits.eq = coverage.commercial_rates_rater_rels
       
    if hxd.cds.rating_factors.product_line == "Excess Flood":
        layer.kpis.hvh.commercial_premium_pre_uw_adj.rate_splits.excess_flood = max(coverage.commercial_rates_rater_rels, 0.15)

    if hxd.cds.rating_factors.product_line == "Monoline Earthquake":
        layer.kpis.hvh.commercial_premium_pre_uw_adj.rate_splits.eq = max(coverage.commercial_rates_rater_rels, 0.15)    
    
    if layer.coverages.eb.include_peril.value is True:
        layer.kpis.hvh.commercial_premium_pre_uw_adj.rate = max(total_commercial_rate + eb_base_rate, 0.15)
    else:
        layer.kpis.hvh.commercial_premium_pre_uw_adj.rate = max(total_commercial_rate, 0.15)
        
def rate_pricing(hxd):
    """ The main pricing calculations function """
    fx_rates = params.fx_rates.df()

    rate_calculate_pricing_variables(hxd)
    calculate_factor_variances(hxd)
    calculate_final_kpis(hxd)

