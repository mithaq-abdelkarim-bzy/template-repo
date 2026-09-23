import hx
import pandas as pd
import numpy as np
import algorithms.utils_global_lists as lst


def experience_rating(hxd):
    layer = hxd.cds.layers[0]
    exp_agg = hxd.cds.exposure.aggregate
    cov = layer.coverages
    param_loss_cost = hx.params.SubjectLossCost
    std_fields = hxd.cds.standard_fields
    
    # SA: you're saving this to a variable here but not using it in the lines below? 
    # Also again 500e3 coming up several times throughout the script - if they all pointed to one location they could easily be all changed at once later 
    manual_max_coverage = 500e3
    
    
    for clm in hxd.cds.experience_rating.claims:
        if clm.coverage != "Premium Bearing Endorsements":
            vbl = hx.params.Coverages[hx.params.Coverages["Coverage Type"] == clm.coverage]["Coverage Variable"].iloc[0]
            cover_vbl = getattr(cov, vbl)

            clm.limited_deductible = max(cover_vbl.deductible, cover_vbl.min_deductible) if cover_vbl.min_deductible else 0
            clm.limited_coverage = min(cover_vbl.coverage, manual_max_coverage)

        else:
            clm.limited_deductible = max(layer.coverages.cover_1_basic_bond.deductible, layer.coverages.cover_1_basic_bond.min_deductible)
            clm.limited_coverage = min(layer.coverages.cover_1_basic_bond.coverage, manual_max_coverage)

        clm.net_direct_loss_incurred = max(0, clm.loss - clm.limited_deductible)
        clm.exceeds_500k = "Yes" if clm.net_direct_loss_incurred > manual_max_coverage else "No"
        clm.exceeds_500k_num = 1 if clm.net_direct_loss_incurred > manual_max_coverage else 0
   
    hxd.cds.experience_rating.total.exceeds_500k = sum(item.exceeds_500k_num for item in hxd.cds.experience_rating.claims)

    company_expected_loss_ratio = 0.7574 if std_fields.insured_state_or_province == "Washington" else 0.725
    lae_discount_factor = 1.1413

    three_year_manual_premium = layer.manual_premium * 3
    company_subject_loss_cost = three_year_manual_premium * company_expected_loss_ratio / lae_discount_factor
    cslc_first_band_upper = param_loss_cost["Subject Loss Cost"].iloc[1]
    cslc_last_band_lower = param_loss_cost["Subject Loss Cost"].iloc[-1]
    premium_modifier = param_loss_cost[param_loss_cost['Subject Loss Cost'] <= company_subject_loss_cost]['Premium Modifier'].iloc[-1]
    adjusted_loss_multiplier = param_loss_cost[param_loss_cost['Subject Loss Cost'] <= company_subject_loss_cost]['Adjusted Loss Multiplier'].iloc[-1]

    if company_subject_loss_cost < cslc_first_band_upper:
        maximum_single_loss = 3.18 * three_year_manual_premium
    elif company_subject_loss_cost > cslc_last_band_lower:
        maximum_single_loss = 0.318 * three_year_manual_premium
    else:
        maximum_single_loss = param_loss_cost[param_loss_cost['Subject Loss Cost'] <= company_subject_loss_cost]['Maximum Single Loss'].iloc[-1]
        
    if std_fields.insured_state_or_province != "Texas":
        maximum_single_loss = maximum_single_loss * (1 + hxd.cds.experience_rating.total.exceeds_500k)


    for clm in hxd.cds.experience_rating.claims:
        clm.adjusted_loss = min(
            max(0, clm.loss - clm.limited_deductible),
            clm.limited_coverage, 
            maximum_single_loss
            )

    hxd.cds.experience_rating.total.adjusted_loss = sum(item.adjusted_loss for item in hxd.cds.experience_rating.claims)

    adjusted_loss_ratio = hxd.cds.experience_rating.total.adjusted_loss / three_year_manual_premium if three_year_manual_premium != 0 else 0

    # Check LCRP-1 Applies with catch for when the state is null
    if std_fields.insured_state_or_province:
        if layer.company_premium > hx.params.StateLookup[hx.params.StateLookup["State"] == std_fields.insured_state_or_province]["Premium Threshold for LCRP-1"].iloc[0]:
            # Experience Mod (II.C.5.)
            experience_mod_5 = premium_modifier + adjusted_loss_ratio*adjusted_loss_multiplier
        else:
            experience_mod_5 = 1
    else:
        experience_mod_5 = 1

    # Experience Mod (II.C.7.)
    experience_mod_7 = 1
    
    # Eligible for Excess Experience Mod?
    hxd.cds.experience_rating.eligible_for_excess_experience_mod = cov.cover_1_basic_bond.coverage > exp_agg.basic_unit_of_coverage

    # Use Excess Experience Mod?    
    if hxd.cds.experience_rating.eligible_for_excess_experience_mod is True and (hxd.cds.experience_rating.use_excess_experience_mod is True or std_fields.insured_state_or_province == "Texas"):
        if std_fields.insured_state_or_province == "Texas":
            hxd.cds.experience_rating.experience_modification = min(experience_mod_5,experience_mod_7)
        else:
            hxd.cds.experience_rating.experience_modification = experience_mod_7
    else:
        hxd.cds.experience_rating.experience_modification = experience_mod_5

         







    
