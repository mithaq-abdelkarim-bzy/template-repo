import hx
import numpy as np
import pandas as pd
from algorithms.rate_utilities import one_layer, ratio , look_up, look_up_with_bounds, iterate_lookups, usd, calculate_xs_factor, calculate_pct_of_technical, validate_empty_fields
from algorithms.rate_constants import param_brokerage


def rate_conloss(hxd):
    layer, cvg = one_layer(hxd)
    clt = cvg.conloss_transit
    clc = cvg.conloss
    p = hx.params
    ccy = hxd.cds.currencies.source_currency
    term = hxd.cds.term.selected
    deductions = layer.brokerage
    total_deductions = ratio((1-param_brokerage), (1-deductions))

    # Initialise variables to avoid errors
    clt.technical_premium = clt.technical_premium_pre_uw_adj = clt.technical_premium_att = clt.technical_premium_cat = 0
    clc.technical_premium = clc.technical_premium_pre_uw_adj = clc.technical_premium_att = clc.technical_premium_cat = 0
    are_transit_fields_full = False
    are_conloss_fields_full = False

    ### --- TRANSIT --- ###

    # Get base rate
    clt.base_rate = look_up("Transit", "coverage", "factor", p.cl_base_rate) if clt.transit_flag else 0

    # Get rates for Transit
    transit_factors = ["deductible_level", "voyage", "surveyor", "vessel", "type_of_cover"]
    iterate_lookups(p, "cl_", clt, transit_factors)

    clt.trans_vals_factor = look_up_with_bounds(clt.trans_vals, "lower_bound", "upper_bound", "factor", p.cl_turnover) # Params same as Cargo

    packaging_factors = np.array([
        look_up(clt.packaging_1, "packaging", "factor", p.cl_packaging),
        look_up(clt.packaging_2, "packaging", "factor", p.cl_packaging),
        ])
    packaging_splits = np.array([clt.packaging_1_factor, clt.packaging_2_factor])
    clt.packaging_factor = sum(packaging_factors * packaging_splits)

    conv_factors = np.array(p.ca_conveyance["factor"]) # NOTE: order in param table must match order of nodes in data schema
    conv_splits = np.array([clt.conv_air_factor, clt.conv_land_factor, clt.conv_sea_factor])
    clt.conv_factor = sum(conv_factors * conv_splits)

    # Add validation to key fields
    if clt.transit_flag:
        clt_validation_nodes = [
            "trans_vals",
            "deductible_level",
            "voyage",
            "surveyor",
            "vessel",
            "type_of_cover"
        ]
        
        are_transit_fields_full = validate_empty_fields(
            validation_nodes=clt_validation_nodes,
            structure_path="conloss_transit",
            hxd_structure=clt,
            cover_name="Transit"
        )

        if not clt.packaging_1 and not clt.packaging_2: # Dealing with this field separately because of its structure
            hx.errors.validation("Packaging fields in Transit cannot both be empty.")
            are_transit_fields_full = False

    # Calculate premium if required fields have been filled in            
    if are_transit_fields_full:
        transit_factors = [
            clt.base_rate,
            clt.trans_vals_factor,
            clt.deductible_level_factor,
            clt.packaging_factor,
            clt.conv_factor,
            clt.voyage_factor,
            clt.surveyor_factor,
            clt.vessel_factor,
            clt.uw_discretion_factor,
            clt.type_of_cover_factor
        ]

        clt.technical_deductions = np.prod(transit_factors)
        clt.technical_rate = clt.technical_deductions * total_deductions
        clt.technical_premium = clt.technical_rate * clt.trans_vals / 100
        clt.technical_premium_pre_uw_adj = ratio(clt.technical_premium, clt.uw_discretion_factor)

        clt.technical_premium_att = clt.technical_premium
        clt.technical_premium_cat = 0

        calculate_pct_of_technical(clt)

     ### --- CON LOSS --- ###

    # Get rates for Con Loss
    clc.base_rate = look_up("Con Loss", "coverage", "factor", p.cl_base_rate) if clc.conloss_flag else 0
    clc.limit_factor = look_up_with_bounds(clc.limit, "lower_bound", "upper_bound", "factor", p.cl_indemnity_limit) # Params same as Cargo
    clc.exposure_factor = look_up(clc.exposure, "exposure", "factor", p.cl_exposure)
    clc.deductible_level_factor = look_up(clc.indemnity_period, "period", clc.deductible_level, p.cl_indemnity_period)

    # Add validation to key fields
    if clc.conloss_flag:
        clc_validation_nodes = ["exposure", "indemnity_period", "deductible_level"]
        
        are_conloss_fields_full = validate_empty_fields(
            validation_nodes=clc_validation_nodes,
            structure_path="conloss",
            hxd_structure=clc,
            cover_name="Con Loss"
        )

        if clc.limit <= 0: # Dealing with this field separately because it's part of the CDS
            hx.errors.validation("Indemnity Limit in Con Loss must be greater than zero.")
            are_storage_fields_full = False

    # Calculate premium if required fields have been filled in 
    if are_conloss_fields_full:
        conloss_factors = [
            clc.base_rate,
            clc.limit_factor,
            clc.exposure_factor,
            clc.deductible_level_factor,
            clc.uw_discretion_factor
        ]
        clc.technical_deductions = np.prod(conloss_factors)
        clc.technical_rate = clc.technical_deductions * total_deductions
        clc.technical_premium = clc.technical_rate * clc.limit / 100
        clc.technical_premium_pre_uw_adj = ratio(clc.technical_premium, clc.uw_discretion_factor)

        clc.technical_premium_att = clc.technical_premium
        clc.technical_premium_cat = 0

        calculate_pct_of_technical(clc)
