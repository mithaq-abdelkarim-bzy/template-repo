import hx
import pandas as pd
import numpy as np
from algorithms.rate_constants import all_perils_dict
import algorithms.rate_utilities as ut

# A list of years in the rating factors that must be before or equal to inception year
year_factors_before_inception = [
        'year_built',
        'roof_year',
        'updated_roof_year',
        "updated_wiring_year",
        "updated_plumbing_year",
        "updated_heating_year"
    ]

mandatory_risk_fields = [
        'building_occupancy','construction_type','year_built',
        'ppc','roof_type','roof_year','distance_to_coast_options'
    ]

def validate_year_before_inception(hxd, factor):
    """ 
    Validate that a given year factor (e.g., year_built, roof_year) is before the inception date.
    
    Args:
        hxd: The main data object containing rating factors and inception date.
        factor (str): Name of year variable to be pulled from hxd.cds.rating_factors.
    """
    factor_name = ut.title_rc(factor)
    factor = getattr(hxd.cds.rating_factors,factor)
    inception_year = hxd.hx_core.inception_date.year  # Extract year as an integer

    if factor is None:
        return  # Skip validation if the factor is None
    
    # if factor > inception_year:
    #     hx.errors.validation(f"Risk Characteristics: {factor_name} ({factor}) must not be after Inception Year ({inception_year}).")


def rate_validations(hxd):
    # Product line selection logic for Excess Wind & Hail
    if hxd.cds.rating_factors.product_line == "Excess Wind & Hail":
        hxd.cds.excess_wind_hail_selected = True
        hxd.cds.excess_wind_hail_not_selected = False
    else:
        hxd.cds.excess_wind_hail_selected = False
        hxd.cds.excess_wind_hail_not_selected = True

    rf = hxd.cds.rating_factors

    # Insured name must be completed, this is needed to ensure landing page works correctly
    if not hxd.cds.standard_fields.insured_name:
        hx.errors.validation("Risk Information: Insured name field must be completed.")

    # Policy Reference must be Completed
    if not hxd.cds.standard_fields.policy_reference:
        hx.errors.validation("Risk Information: Policy reference field must be completed.")

    # Validation to check how many layers are set as bound, also updates premium label for bound policies
    bound_count = 0
    for k,layer in enumerate(hxd.cds.layers,start=1):
        if layer.status in ["Bound", "Post Bind Complete", "Bound MTA"]:
            bound_count += 1
            layer.premium_label = "Gross Bound Premium"
            if k > hxd.cds.number_of_options:
                hx.errors.validation(
                        f"Pricing: Option {k} is still set to Bound please expand the number of options remove the Bound status."
                    )
        else:
            layer.premium_label = "Gross Quoted Premium"
    
    # if bound_count == 0:
    #     hx.errors.validation("Pricing: Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final")
    # elif bound_count > 1:
    #     hx.errors.validation("Pricing: There must be only one bound policy")

    if bound_count > 1:
        hx.errors.validation("Pricing: There must be only one bound policy")

    # Validate that the years in rating factors are before the inception date
    for factor in year_factors_before_inception:
        validate_year_before_inception(hxd,factor)

    # Validate that roof year is after year built
    if rf.roof_year and rf.year_built:
        if rf.roof_year < rf.year_built:
            hx.errors.validation(
                f"Risk Characteristics: Roof Year ({rf.roof_year}) must be after Year Built ({rf.year_built})."
            )

    # Validate that update roof year is after roof year
    if rf.updated_roof_year and rf.roof_year:
        if rf.updated_roof_year < rf.roof_year:
            hx.errors.validation(
                f"Risk Characteristics: Update Roof Year ({rf.updated_roof_year}) must be after Roof Year ({rf.roof_year})."
            )
    # Mandatory Risk Characteristic fields
    for field in mandatory_risk_fields:
        if getattr(rf,field) is None:
            title = 'PPC' if field == 'ppc' else ut.title_rc(field)
            title = 'Distance to Coast' if field == 'distance_to_coast_options' else ut.title_rc(field) 
            hx.errors.validation(
                f"Risk Characteristics: {title} field must be completed."
            )


    for k, layer in enumerate(hxd.cds.layers,start=1):
        if layer.coverages.wildfire.include_peril.value and layer.coverages.wildfire.wildfire_score is None:
            hx.errors.validation(
                f"Pricing: Wildfire score must be populated in option {k}"
            )
        if layer.coverages.eq.deductible not in [0.03,0.05,0.1] and layer.coverages.eq.include_peril.value and hxd.cds.show_eq_options:
                hx.errors.validation(
                f"Pricing: EQ deductible must be 3%, 5% or 10% in option {k}"
            )
        if layer.coverages.eb.deductible is None and layer.coverages.eb.include_peril.value and hxd.cds.show_eb_options:
                hx.errors.validation(
                f"Pricing: Equipment Breakdown deductible value must not be none in option {k}."
            )
            # Only validate if NOT Excess Wind & Hail
        if hxd.cds.rating_factors.product_line != "Excess Wind & Hail":

            if (
                layer.coverages.ws.deductible is None
                and layer.coverages.ws.include_peril.value
                and hxd.cds.show_ws_options
                and layer.coverages.ws.deductible_type.value in ['Named Storm', 'Wind & Hail']
            ):
                hx.errors.validation(
                    f"Pricing: WS deductible value must not be none in option {k}."
                )

            if (
                layer.coverages.ws.deductible_all_perils is None
                and layer.coverages.ws.include_peril.value
                and hxd.cds.show_ws_options
                and layer.coverages.ws.deductible_type.value == 'All Perils'
            ):
                hx.errors.validation(
                    f"Pricing: WS deductible value must not be none in option {k}."
                )
        if k == hxd.cds.number_of_options:
            break

    # Warning (not validation) adjustments are not too extreme   
    
    hvh_extreme_adjustment_count = 0
    paf_extreme_adjustment_count = 0
    hxd.cds.notes.hvh_cp_deviate_warning_flag = False    
    hxd.cds.notes.paf_cp_deviate_warning_flag = False
    
    # hvh
    for k,layer in enumerate(hxd.cds.layers,start=1):                
        if layer.kpis.hvh.commercial_premium_pre_uw_adj.rate and layer.kpis.hvh.commercial_premium.rate.selected:
            if layer.kpis.hvh.commercial_premium_pre_uw_adj.rate - layer.kpis.hvh.commercial_premium.rate.selected > 0.15:                
                hvh_extreme_adjustment_count += 1

    if hvh_extreme_adjustment_count > 0:        
        hxd.cds.notes.hvh_cp_deviate_warning_flag = True
        hxd.cds.notes.hvh_cp_deviate_warning = f"Warning: HVH commercial premium rate in at least one option is 0.15 lower than the pre adjusted amount."            
    

    for k,layer in enumerate(hxd.cds.layers,start=1):
        if layer.kpis.paf.commercial_premium_pre_uw_adj.rate and layer.kpis.paf.commercial_premium.rate.selected:
            if layer.kpis.paf.commercial_premium_pre_uw_adj.rate - layer.kpis.paf.commercial_premium.rate.selected > 0.15:
                paf_extreme_adjustment_count += 1
    
    if paf_extreme_adjustment_count > 0:        
        hxd.cds.notes.paf_cp_deviate_warning_flag = True
        hxd.cds.notes.paf_cp_deviate_warning = f"Warning: PAF commercial premium rate in at least one option is 0.15 lower than the pre adjusted amount."            
    

    # for k, layer in enumerate(hxd.cds.layers,start=1):
    #     if layer.kpis.hvh.commercial_premium_pre_uw_adj.rate and layer.kpis.hvh.commercial_premium.rate.selected:
    #         if layer.kpis.hvh.commercial_premium_pre_uw_adj.rate - layer.kpis.hvh.commercial_premium.rate.selected > 0.15:
    #                 hx.errors.validation(
    #                 f"HVH commercial premium rate in option {k} cannot be 0.15 lower than the pre adjusted amount."
    #             )

    #     if layer.kpis.paf.commercial_premium_pre_uw_adj.rate and layer.kpis.paf.commercial_premium.rate.selected:
    #         if layer.kpis.paf.commercial_premium_pre_uw_adj.rate - layer.kpis.paf.commercial_premium.rate.selected > 0.15:
    #                 hx.errors.validation(
    #                 f"PAF commercial premium rate in option {k} cannot be 0.15 lower than the pre adjusted amount."
    #             )

    #     if layer.kpis.total.commercial_premium_pre_uw_adj.rate and layer.kpis.total.commercial_premium.rate:
    #         if layer.kpis.total.commercial_premium_pre_uw_adj.rate - layer.kpis.total.commercial_premium.rate > 0.15:
    #                 hx.errors.validation(
    #                 f"Total commercial premium rate in option {k} cannot be 0.15 lower than the pre adjusted amount."
    #             )
    #     if k == hxd.cds.number_of_options:
    #         break


