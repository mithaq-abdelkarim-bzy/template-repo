import hx
import numpy as np
import pandas as pd
from algorithms.rate_utilities import one_layer, ratio, look_up, look_up_with_bounds, iterate_lookups, usd, calculate_xs_factor, calculate_pct_of_technical, validate_empty_fields
from algorithms.rate_constants import param_brokerage


def rate_cargo(hxd):
    layer, cvg = one_layer(hxd)
    ct = cvg.cargo_transit
    cs = cvg.cargo_storage
    p = hx.params
    ccy = hxd.cds.currencies.source_currency
    term = hxd.cds.term.selected
    deductions = layer.brokerage
    total_deductions = ratio((1-param_brokerage), (1-deductions))

    # Initialise variables to avoid errors
    ct.technical_premium = ct.technical_premium_pre_uw_adj = ct.technical_premium_att = ct.technical_premium_cat = 0
    cs.technical_premium = cs.technical_premium_pre_uw_adj = cs.technical_premium_att = cs.technical_premium_cat = 0
    are_transit_fields_full = False
    are_storage_fields_full = False

    ### --- TRANSIT --- ###

    # Get base rates and convert to array - NOTE: order in param table must match order of nodes in data schema
    transit_rates = p.ca_base_rate[p.ca_base_rate["coverage"] != "Storage"]["factor"]
    transit_rates = np.array(transit_rates)

    # Get cover selected and convert to array
    cover_selected = [
        ct.wh_to_port_flag,
        ct.loading_flag,
        ct.voyage_flag,
        ct.unloading_flag,
        ct.port_to_wh_flag
    ]
    cover_selected = np.array(cover_selected)

    # Calculate base rate
    base_rate = sum(transit_rates * cover_selected)
    ct.base_rate = base_rate if ct.transit_flag else 0

    # Get rates for Transit
    transit_factors = ["commodity", "deductible_level", "packaging", "voyage", "surveyor", "vessel", "type_of_cover"]
    iterate_lookups(p, "ca_", ct, transit_factors)

    ct.trans_vals_factor = look_up_with_bounds(ct.trans_vals, "lower_bound", "upper_bound", "factor", p.ca_turnover)
    ct.excess_factor.calculated = calculate_xs_factor(ct.excess, ccy, p.ca_excess)

    conv_factors = np.array(p.ca_conveyance["factor"]) # NOTE: order in param table must match order of nodes in data schema
    conv_splits = np.array([ct.conv_air_factor, ct.conv_land_factor, ct.conv_sea_factor])
    ct.conv_factor = sum(conv_factors * conv_splits)

    # Add validation to key fields
    if ct.transit_flag:
        # Validation for transit-specific coverages
        transit_covers = [
            ct.wh_to_port_flag,
            ct.loading_flag,
            ct.voyage_flag,
            ct.unloading_flag,
            ct.port_to_wh_flag
        ]
        are_ct_covers_selected = any(transit_covers)

        if not are_ct_covers_selected:
            hx.errors.validation("None of the coverages in Cargo Transit has been selected. Please select at least one among: \
                'Initial Warehouse to Port', 'Loading', 'Voyage', 'Unloading', 'Port to Final Warehouse'.")

        # Standard validation
        ct_validation_nodes = [
            "trans_vals",
            "commodity",
            "deductible_level",
            "packaging",
            "voyage",
            "surveyor",
            "vessel",
            "type_of_cover"
        ]
        
        are_transit_fields_full = validate_empty_fields(
            validation_nodes=ct_validation_nodes,
            structure_path="cargo_transit",
            hxd_structure=ct,
            cover_name="Cargo Transit"
        )

        ct.are_fields_full = are_transit_fields_full

    # Calculate premium if required fields have been filled in            
    if are_transit_fields_full:
        transit_factors = [
            ct.base_rate,
            ct.commodity_factor,
            ct.trans_vals_factor,
            ct.deductible_level_factor.selected,
            ct.excess_factor.selected,
            ct.packaging_factor,
            ct.conv_factor,
            ct.voyage_factor,
            ct.surveyor_factor,
            ct.vessel_factor,
            ct.uw_discretion_factor,
            ct.type_of_cover_factor
        ]

        ct.technical_deductions = np.prod(transit_factors)
        ct.technical_rate = ct.technical_deductions * total_deductions
        ct.technical_premium = ct.technical_rate * ct.trans_vals * term / 100
        ct.technical_premium_pre_uw_adj = ratio(ct.technical_premium, ct.uw_discretion_factor)
        
        ct.technical_premium_att = ct.technical_premium
        ct.technical_premium_cat = 0

        calculate_pct_of_technical(ct)

    ### --- STORAGE --- ###

    # Get rates for Storage
    cs.base_rate = look_up("Storage", "coverage", "factor", p.ca_base_rate) if cs.storage_flag else 0

    storage_factors = ["deductible_level", "survey", "type_of_cover"]
    iterate_lookups(p, "ca_", cs, storage_factors)

    cs.excess_factor.calculated = calculate_xs_factor(cs.excess, ccy, p.ca_excess)

    storage_factors = [
        cs.base_rate,
        cs.deductible_level_factor.selected,
        cs.excess_factor.selected,
        cs.survey_factor,
        cs.risk_mgmt_factor,
        cs.type_of_cover_factor,
        cs.uw_discretion_factor
    ]
    cs.rate = np.prod(storage_factors)

    for country in cs.countries:
        country.cat_load = look_up(country.country, "country", "total_load", p.ca_cat_load)
        country.pct_of_cat = ratio(country.cat_expo, cs.cat_expo)

    cs.cat_pct_of_total = ratio(cs.cat_expo, cs.avg_val_pcm)
    cs.combined_cat_load = sum([country.cat_load * country.pct_of_cat for country in cs.countries])
    cs.cat_expo_tp.calculated = cs.rate * cs.cat_expo * cs.combined_cat_load / 100
    
    cs.retail_pct_of_total = ratio(cs.retail_expo, cs.avg_val_pcm)
    cs.retail_expo_tp = cs.rate * cs.retail_expo * cs.retail_load / 100

    cs.all_else_expo.calculated = cs.avg_val_pcm - cs.cat_expo - cs.retail_expo
    cs.all_else_pct_of_total = ratio(cs.all_else_expo.selected, cs.avg_val_pcm)
    cs.all_else_expo_tp = cs.rate * cs.all_else_expo.selected * cs.all_else_load / 100

    tp_att_total = sum([cs.retail_expo_tp, cs.all_else_expo_tp])
    tp_cat_total = cs.cat_expo_tp.selected
    tp_total = tp_cat_total + tp_att_total

    # Add validation to key fields
    if cs.storage_flag:
        cs_validation_nodes = ["stock_vals", "deductible_level", "type_of_cover", "avg_val_pcm"]
        
        are_storage_fields_full = validate_empty_fields(
            validation_nodes=cs_validation_nodes,
            structure_path="cargo_storage",
            hxd_structure=cs,
            cover_name="Cargo Storage"
        )

    if are_storage_fields_full:
        cs.technical_premium = tp_total * term * total_deductions
        cs.technical_premium_pre_uw_adj = ratio(cs.technical_premium, cs.uw_discretion_factor)
        cs.technical_deductions = ratio(tp_total, cs.stock_vals/100)
        cs.technical_rate = cs.technical_deductions * total_deductions

        cs.technical_premium_att = tp_att_total * term * total_deductions
        cs.technical_premium_cat = tp_cat_total * term * total_deductions

        calculate_pct_of_technical(cs)
