import hx
import pandas as pd
import numpy as np
from algorithms.percentage_validations import set_invalid,set_valid

def rate_validations(hxd):

    #### Risk Information Page ####################################################################
    
    # Insured name must be populated
    if (hxd.cds.standard_fields.insured_name == None):
        hx.errors.validation("Risk Information Page: No Insured Name entered.")

    # Underwriter name must be populated
    if (hxd.cds.standard_fields.underwriter == None):
        hx.errors.validation("Risk Information Page: No Underwriter name entered.")

    # Location percentage should sum to 100%
    if hxd.cds.rating_factors.location.percentage != 1:
        set_invalid(hxd, "location_percentage", "Risk Information page: Location percentages need to sum to 100%")
    else:
        set_valid(hxd, "location_percentage")

    #### Discipline Details Page ##################################################################
    


    #### Modifiers Page ###########################################################################
    rating_factors = hxd.cds.rating_factors
    mods_srf = hxd.cds.modifiers.schedule_rating_factor

    # Retroactive date cannot be after inception date
    if (rating_factors.opt_coverages.full_prior_act_date != None):
        if (hxd.hx_core.inception_date < rating_factors.opt_coverages.full_prior_act_date):
            hx.errors.validation("Modifier Details Page: Retroactive date cannot be after inception date.")

    # Can't enter negative values - experience modification
    if (hxd.cds.modifiers.exp_mod.incurred_loss != None): 
        if (hxd.cds.modifiers.exp_mod.incurred_loss < 0):
            hx.errors.validation("Modifier Details Page: 1. Experience Modification -  Total incurred loss cannot be negative.")

    if (hxd.cds.modifiers.exp_mod.number_of_claims != None): 
        if (hxd.cds.modifiers.exp_mod.number_of_claims < 0):
            hx.errors.validation("Modifier Details Page: 1. Experience Modification - Number of claims cannot be negative.")

    if (hxd.cds.modifiers.exp_mod.number_of_incidents != None): 
        if (hxd.cds.modifiers.exp_mod.number_of_incidents < 0):
            hx.errors.validation("Modifier Details Page: 1. Experience Modification - Number of incidents cannot be negative.")

    if (hxd.cds.modifiers.exp_mod.written_premium != None): 
        if (hxd.cds.modifiers.exp_mod.written_premium < 0):
            hx.errors.validation("Modifier Details Page: 1. Experience Modification - Written premium cannot be negative.")

    if (hxd.cds.modifiers.exp_mod.incurred_lr.override != None): 
        if (hxd.cds.modifiers.exp_mod.incurred_lr.selected < 0):
            hx.errors.validation("Modifier Details Page: 1. Experience Modification - Incurred LR cannot be negative.")

    if (hxd.cds.modifiers.exp_mod.exp_mod_factor.override != None): 
        if (hxd.cds.modifiers.exp_mod.exp_mod_factor.selected < 0):
            hx.errors.validation("Modifier Details Page: 1. Experience Modification - Experience modification factor cannot be negative.")

    # Can't enter negative values - written contracts
    if (hxd.cds.rating_factors.written_contracts.percentage != None): 
        if (hxd.cds.rating_factors.written_contracts.percentage < 0):
            hx.errors.validation("Modifier Details Page: 2. Use of Written Contracts - Percentage cannot be negative.")

    if (hxd.cds.rating_factors.written_contracts.written_contracts_factor != None): 
        if (hxd.cds.rating_factors.written_contracts.written_contracts_factor < 0):
            hx.errors.validation("Modifier Details Page: 2. Use of Written Contracts - Written Contracts Factor cannot be negative.")

    # Can't enter negative values - Longevity with Carrier 
    if (hxd.cds.rating_factors.longevity_with_carrier.yrs_insured != None): 
        if (hxd.cds.rating_factors.longevity_with_carrier.yrs_insured < 0):
            hx.errors.validation("Modifier Details Page: 3. Longevity with Carrier - Number of years insured cannot be negative.")

    # Can't enter negative values - Longevity
    if (hxd.cds.rating_factors.longevity.yr_start != None): 
        if (hxd.cds.rating_factors.longevity.yr_start < 0):
            hx.errors.validation("Modifier Details Page: 4. Longevity - Insured start year cannot be negative.")

    # year start date after inception date
    if (hxd.cds.rating_factors.longevity.yr_start != None): 
        if (rating_factors.longevity.yr_start > hxd.hx_core.inception_date.year):
           hx.errors.validation("Modifier Details Page: 4. Longevity - Insured start year is after inception date.")

    # Check project type % fees in aggregate table percentages sum to 1
    fee_pct = hxd.cds.exposure.aggregate.project_type_category.cat_type_total.fee_percentage

    if fee_pct == 0 or round(fee_pct, 2) == 1:
        set_valid(hxd, "fee_percentage")
    else:
        set_invalid(hxd,"fee_percentage","Modifier Details Page: Project Types percentages do not sum to 100%.")
    # Check there are comments for schedule rating factors that have been enter

    # Create list to loop through all the schedule rating items
    lst_srf_vbl = [mods_srf.qual_of_staff,
                    mods_srf.rm_attendance,
                    mods_srf.foreign_work,
                    mods_srf.loss_prev,
                    mods_srf.client_type,
                    mods_srf.contractual_practices,
                    mods_srf.engi_procure_construct,
                    mods_srf.peer_review]

    for loop_vbl in lst_srf_vbl:
        if (loop_vbl.factor != 0 and loop_vbl.comment == None):
            hx.errors.validation("Modifier Details Page: Schedule Factor entered and no comment provided.")

        if (loop_vbl.factor > loop_vbl.max or loop_vbl.factor < loop_vbl.min):
            hx.errors.validation("Modifier Details Page: Schedule Factor entered is outside of min/max range.") 


    #### Rating Summary Page ######################################################################
    layers = hxd.cds.layers

    # Status - at least one layer must be marked as bound 
    bound_count = 0
    for layer in layers:
        if layer.status in ["Bound"]:
            bound_count += 1
    
    if bound_count == 0:
        hx.errors.validation("Rating Summary Page: At least one layer must have Status marked as 'Bound' to mark a policy as final")

    # Section Reference - if there's a bounded option, check that a section reference exists
    for index, layer in enumerate(layers):
        if (layer.status == "Bound" and layer.section_reference is None):
            if (index == 0):
                hx.errors.validation("Rating Summary Page: No section reference entered for bounded primary layer.")
            elif (index > 0 and getattr(hxd.cds, f"add_excess_{index}")):
                hx.errors.validation(f"Rating Summary Page: No section reference entered for bounded excess layer {index}.")
            else: 
                pass
    