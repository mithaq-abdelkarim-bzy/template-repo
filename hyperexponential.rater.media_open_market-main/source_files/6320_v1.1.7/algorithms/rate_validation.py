import hx
import pandas as pd
import numpy as np
from algorithms import parameter_tables_schema as params
from algorithms.rate_utilities import look_up
from datetime import datetime

def rate_validations(hxd):
    cds = hxd.cds 

    # FX rate for currency conversion
    fx_rates_df = params.fx_rates.df()
    ccy = cds.currencies.source_currency
    fx_rate = look_up(ccy, 'ccy', 'fx_rate', fx_rates_df, if_not_found=1) # default to USD if error

    # Validations for all coverages --------------------------------------------------------------------------------------------------------------
    # Insured name must be completed, this is needed to ensure landing page works correctly
    if not hxd.cds.standard_fields.insured_name:
        hx.errors.validation("Insured name field must be completed. [Risk Information]")

    # Currency has been selected
    if not cds.currencies.source_currency:
        hx.errors.validation("Currency field must be completed. [Risk Information]")

    # Coverage type has been selected
    if not cds.coverage_name:
        hx.errors.validation("Coverage Name field must be completed. [Risk Information]")

    # Coverage type has been selected
    if not cds.standard_fields.underwriter:
        hx.errors.validation("Underwriter field must be completed. [Risk Information]")
    
    # Validation to check how many layers are set as bound, also updates premium label for bound policies
    bound_count = 0
    for layer in hxd.cds.layers:
        if layer.status in ["Bound", "Post Bind Complete"]:
            bound_count += 1
            layer.premium_label = "Gross Bound Premium"
        else:
            layer.premium_label = "Gross Quoted Premium"
    
    # Ensure one layer is bound.
    if bound_count == 0:
        hx.errors.validation("Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final. [Rating Summary]")
    elif bound_count > 1:
        hx.errors.validation("There must be only one bound policy. [Rating Summary]")

    # Require section reference to be entered for bound layer
    for layer in hxd.cds.layers:
        if (layer.status in ["Bound", "Post Bind Complete"]) & (layer.section_reference is None):
            hx.errors.validation("Section reference must be entered for bound policy. [Rating Summary]")

    # Require bound premium to be entered for bound layer
    for index, layer in enumerate(cds.layers):
        if layer.status not in ["Bound", "Post Bind Complete"]:
            continue #  Skip layers that aren't bound

        if cds.standard_fields.is_rater_priced:
            if (index==0):
                if cds.primary.bound_premium is None:
                    hx.errors.validation("Bound premium must be entered for bound policy. [Rating Summary]")
            elif layer.bound_premium is None:
                hx.errors.validation("Bound premium must be entered for bound policy. [Rating Summary]")
        elif cds.standard_fields.is_case_priced:
            if layer.quoted_premium_view is None:
                hx.errors.validation("Quoted premium must be entered for bound policy. [Rating Summary]")
        

    # Country must be entered
    if not cds.rating_factors.location:
        hx.errors.validation("Country field must be completed. [Exposure Details]")


    # Validations for standard coverages only [Media Liability, Music Liability, Annual TV & Film LARGE] -------------------------------------------
    if cds.standard_rater_masking:
        
        # Years in business must be entered
        if not cds.rating_factors.years_in_business:
            hx.errors.validation("Years in Business field must be completed. [Exposure Details]")
 
        # Total revenue and/or rateable revenue must be entered (and greater than zero)
        if not (cds.exposure.aggregate.total_revenue or cds.exposure.aggregate.rateable.revenue):
            hx.errors.validation("Revenue greater than zero must be entered. [Exposure Details]")
            # Validations already exist in schema to ensure values are > 0

        # When total revenue is entered, rateable revenue <= total revenue
        if cds.exposure.aggregate.total_revenue and (cds.exposure.aggregate.rateable.revenue > cds.exposure.aggregate.total_revenue):
            hx.errors.validation("Rateable Revenue is greater than the Total Revenue. Please try again. [Exposure Details]")

        # # Total revenue must be < 1 billion USD
        # total_revenue_usd = cds.exposure.aggregate.total_revenue / fx_rate
        # rateable_revenue_usd = cds.exposure.aggregate.rateable.revenue / fx_rate
        # if (total_revenue_usd > 1e9) or (rateable_revenue_usd > 1e9):
        #     hx.errors.validation("Revenue exceeds the maximum limit of 1 billion USD. Please try again. [Exposure Details]")


    # Validations for nonstandard coverages only [Individual TV, Individual Film, Annual TV & Film SMALL] -------------------------------------------

    # if cds.annualtv_masking: # -> validations now been added to schema instead.
    #     # Turnover must be entered, and greater than 0
    #     if (cds.annual_tv.turnover is None) or (cds.annual_tv.turnover <= 0): 
    #         hx.errors.validation("Turnover greater than zero must be entered. [Exposure Details]") 
    #     # Number of productions must be entered, and greater than 0
    #     if (cds.exposure.aggregate.annual_tv.number_of_productions is None) or (cds.exposure.aggregate.annual_tv.number_of_productions <= 0):
    #         hx.errors.validation("Number of Productions greater than zero must be entered. [Exposure Details]")

    if cds.individualtv_masking:
        if cds.exposure.aggregate.individual_tv.length is None:
            hx.errors.validation("Length Type must be selected. [Exposure Details]")
        if cds.individual_tv.selections.genre is None:
            hx.errors.validation("Genre Type must be selected. [Exposure Details]")

    if cds.individualfilm_masking:
        if cds.exposure.aggregate.individual_film.exhibition is None:
            hx.errors.validation("Scope of Release must be selected. [Exposure Details]")




     

    
