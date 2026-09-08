import hx
import numpy as np
import pandas as pd
from algorithms.rate_utilities import one_layer, ratio , look_up, look_up_with_bounds, iterate_lookups, usd, calculate_xs_factor, calculate_pct_of_technical, validate_empty_fields
from algorithms.rate_constants import param_brokerage


def rate_specie(hxd):
    layer, cvg = one_layer(hxd)
    st = cvg.specie_transit
    ss = cvg.specie_storage
    p = hx.params
    ccy = hxd.cds.currencies.source_currency
    term = hxd.cds.term.selected
    deductions = layer.brokerage
    total_deductions = ratio((1-param_brokerage), (1-deductions))

    # Initialise variables to avoid errors
    st.technical_premium = st.technical_premium_pre_uw_adj = st.technical_premium_att = st.technical_premium_cat = 0
    ss.technical_premium = ss.technical_premium_pre_uw_adj = ss.technical_premium_att = ss.technical_premium_cat = 0
    are_transit_fields_full = False
    are_storage_fields_full = False

    ### --- TRANSIT --- ###

    # Get base rate
    st.base_rate = look_up("Transit", "coverage", "factor", p.sp_base_rate) if st.transit_flag else 0

    # Get rates for Transit
    transit_factors = ["commodity", "deductible_level", "type_of_cover"]
    iterate_lookups(p, "sp_", st, transit_factors)

    st.trans_vals_factor = look_up_with_bounds(st.trans_vals, "lower_bound", "upper_bound", "factor", p.ca_turnover) # Params same as Cargo
    st.excess_factor.calculated = calculate_xs_factor(st.excess, ccy, p.ca_excess) # Params same as Cargo

    # Add validation to key fields
    if st.transit_flag:
        st_validation_nodes = ["commodity", "trans_vals", "deductible_level", "type_of_cover"]
        
        are_transit_fields_full = validate_empty_fields(
            validation_nodes=st_validation_nodes,
            structure_path="specie_transit",
            hxd_structure=st,
            cover_name="Specie Transit"
        )

    # Calculate premium if required fields have been filled in            
    if are_transit_fields_full:
        transit_factors = [
            st.base_rate,
            st.commodity_factor,
            st.trans_vals_factor,
            st.deductible_level_factor,
            st.excess_factor.selected,
            st.type_of_cover_factor,
            st.uw_discretion_factor
        ]

        st.technical_deductions = np.prod(transit_factors)
        st.technical_rate = st.technical_deductions * total_deductions
        st.technical_premium = st.technical_rate * st.trans_vals * term / 100
        st.technical_premium_pre_uw_adj = ratio(st.technical_premium, st.uw_discretion_factor)

        st.technical_premium_att = st.technical_premium
        st.technical_premium_cat = 0

        calculate_pct_of_technical(st)

    ### --- STORAGE --- ###

    # Get rates for Storage
    ss.base_rate = look_up("Storage", "coverage", "factor", p.sp_base_rate) if ss.storage_flag else 0

    storage_factors = ["commodity", "deductible_level", "survey", "type_of_cover"]
    iterate_lookups(p, "sp_", ss, storage_factors)

    ss.stock_vals_factor = look_up_with_bounds(ss.stock_vals, "lower_bound", "upper_bound", "factor", p.ca_turnover) # Params same as Cargo
    ss.excess_factor.calculated = calculate_xs_factor(ss.excess, ccy, p.ca_excess) # Params same as Cargo

    storage_factors = [
        ss.base_rate,
        ss.commodity_factor,
        ss.stock_vals_factor,
        ss.deductible_level_factor,
        ss.excess_factor.selected,
        ss.survey_factor,
        ss.risk_mgmt_factor,
        ss.type_of_cover_factor,
        ss.uw_discretion_factor
    ]

    ss.rate = np.prod(storage_factors)

    for country in ss.countries:
        country.cat_load = look_up(country.country, "country", "total_load", p.ca_cat_load) # Loads same as Cargo
        country.pct_of_cat = ratio(country.cat_expo, ss.cat_expo)

    ss.cat_pct_of_total = ratio(ss.cat_expo, ss.avg_val_pcm)
    ss.combined_cat_load = sum([country.cat_load * country.pct_of_cat for country in ss.countries])
    ss.cat_expo_tp.calculated = ss.rate * ss.cat_expo * ss.combined_cat_load / 100
    
    ss.non_cat_pct_of_total = ratio(ss.non_cat_expo, ss.avg_val_pcm)
    ss.non_cat_expo_tp = ss.rate * ss.non_cat_expo * ss.non_cat_load / 100

    tp_att_total = ss.non_cat_expo_tp
    tp_cat_total = ss.cat_expo_tp.selected
    tp_total = sum([ss.cat_expo_tp.selected, ss.non_cat_expo_tp])

    # Add validation to key fields
    if ss.storage_flag:
        ss_validation_nodes = [
            "commodity", 
            "stock_vals", 
            "deductible_level", 
            "type_of_cover", 
            "avg_val_pcm"
        ]
        
        are_storage_fields_full = validate_empty_fields(
            validation_nodes=ss_validation_nodes,
            structure_path="specie_storage",
            hxd_structure=ss,
            cover_name="Specie Storage"
        )

        if ss.non_cat_expo <=0: # Dealing with this field separately because of the label
            hx.errors.validation("Non-CAT Exposure in Specie Storage must be greater than zero.")
            are_storage_fields_full = False

    # Calculate premium if required fields have been filled in            
    if are_storage_fields_full:
        ss.technical_premium = tp_total * term * total_deductions
        ss.technical_premium_pre_uw_adj = ratio(ss.technical_premium, ss.uw_discretion_factor)
        ss.technical_deductions = ratio(tp_total, ss.stock_vals/100)
        ss.technical_rate = ss.technical_deductions * total_deductions

        ss.technical_premium_att = tp_att_total * term * total_deductions
        ss.technical_premium_cat = tp_cat_total * term * total_deductions

        calculate_pct_of_technical(ss)
