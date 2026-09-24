import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
import algorithms.rate_constants as const
from algorithms import parameter_tables_schema as params
from operator import itemgetter
# Import helper functions:
from algorithms.rate_helpers import exposure_measure_calcs, class_base_rate_calculations, assign_modifier_annualtv, assign_modifier_individualtv, assign_modifier_individualfilm

def rate_exposure_details(hxd):
    cds = hxd.cds

    # FX rate for currency conversion -----------------------------
    ccy = hxd.cds.currencies.source_currency
    fx_rates_df = params.fx_rates.df()
    fx_rate = utils.look_up(ccy, 'ccy', 'fx_rate', fx_rates_df, if_not_found=1) # default to USD if error

    # Set show/hide masking ---------------------------------------
    cds.media_masking = cds.coverage_name == "Media Liability"
    cds.music_masking = cds.coverage_name == "Music Liability"
    cds.tvfilm_masking = cds.coverage_name == "Annual TV & Film LARGE" # Previously "TV & Film E&O"
    cds.individualtv_masking = cds.coverage_name == "Individual TV"
    cds.annualtv_masking = cds.coverage_name == "Annual TV & Film SMALL" # Previously "Annual TV"
    cds.individualfilm_masking = cds.coverage_name == "Individual Film"
    cds.standard_rater_masking = (cds.coverage_name == "Media Liability") | (cds.coverage_name == "Music Liability") | (cds.coverage_name == "Annual TV & Film LARGE")
    cds.nonstandard_rater_masking = (cds.coverage_name == "Individual TV") | (cds.coverage_name == "Annual TV & Film SMALL") | (cds.coverage_name == "Individual Film")

    # Territory Factor calculation --------------------------------
    location = cds.rating_factors.location
    territory_params = hx.params.tbl_territory_factor
    # Look up location in table and output corresponding factor
    row = territory_params[territory_params["country"] == location]
    cds.rating_factors.territory_factor = row.iloc[0]["rate"] if not row.empty else 1

    # Standard rater calculations (Media Liability, Music Liability, TV & Film E&O) ------------------------------------------------------------------------------------
    if cds.standard_rater_masking:

        # Granular Exposure calculations ------------------------------
        # exposure_params = pd.DataFrame(columns=["exposure_measure", "exposure_name", "class", "base_rate"])

        # Get the base rates for each exposure measure:
        # Media Liability
        if cds.media_masking:
            exposure_params = exposure_measure_calcs(hxd, "media")

        # Music Liability
        elif cds.music_masking:
            exposure_params = exposure_measure_calcs(hxd, "music")

        # TV & Film E&O
        elif cds.tvfilm_masking:
            exposure_params = exposure_measure_calcs(hxd, "tvfilm")


        # Base Rate calculations (done in USD) ---------------------------------------
        total_revenue_usd = cds.exposure.aggregate.total_revenue / fx_rate
        rateable_revenue_usd = cds.exposure.aggregate.rateable.revenue / fx_rate if cds.exposure.aggregate.rateable.revenue != 0 else total_revenue_usd

        total_revenue_usd = max(total_revenue_usd, 0)
        rateable_revenue_usd = max(rateable_revenue_usd, 0)
        nonrateable_revenue_usd = max(total_revenue_usd - rateable_revenue_usd, 0)

        # Revenue split for granular exposures
        exposure_params["rateable_revenue_usd"] = exposure_params["base_rate"] * rateable_revenue_usd
        # Revenue split by class
        exposure_by_class = exposure_params.groupby("class")["base_rate"].sum().reset_index().rename(columns={"base_rate": "weight"})  # Sum base rates to get weight for each class.
        exposure_by_class["alloc_revenue_rateable_usd"] = exposure_by_class["weight"] * rateable_revenue_usd
        exposure_by_class["alloc_revenue_nonrateable_usd"] = exposure_by_class["weight"] * nonrateable_revenue_usd

        # Base rate bands (in USD) -----------
        base_rate_bands = hx.params.tbl_base_rates
        # Rateable revenue
        bands_rateable = base_rate_bands[base_rate_bands["revenue"] < rateable_revenue_usd].iloc[-1] if rateable_revenue_usd > 0 else base_rate_bands.iloc[0] # Find relevant row for total rateable revenue.
        exposure_by_class = class_base_rate_calculations(exposure_by_class, bands_rateable, "rateable") # Calculate interpolated rates for each class
        # Non-rateable revenue
        bands_nonrateable = base_rate_bands[base_rate_bands["revenue"] < nonrateable_revenue_usd].iloc[-1] if nonrateable_revenue_usd > 0 else base_rate_bands.iloc[0] # Find relevant row for total non-rateable revenue.
        exposure_by_class = class_base_rate_calculations(exposure_by_class, bands_nonrateable, "nonrateable") # Calculate interpolated rates for each class
        # Base rates
        rateable_base_rate_usd = (exposure_by_class["weight"] * exposure_by_class["interpolated_rate_rateable"]).sum() if rateable_revenue_usd != 0 else 0
        nonrateable_base_rate_usd = (exposure_by_class["weight"] * exposure_by_class["interpolated_rate_nonrateable"]).sum() if nonrateable_revenue_usd != 0 else 0

        # Assign to nodes (in source currency) -------
        cds.exposure.aggregate.nonrateable.revenue = nonrateable_revenue_usd * fx_rate
        cds.exposure.aggregate.rateable.base_rate = rateable_base_rate_usd * fx_rate
        cds.exposure.aggregate.nonrateable.base_rate = nonrateable_base_rate_usd * fx_rate

        # Base Premium calculations (in USD) ---------
        if (rateable_revenue_usd > 0 and nonrateable_revenue_usd > 0):
            base_premium_usd = rateable_base_rate_usd + nonrateable_base_rate_usd
        else:
            base_premium_usd = rateable_base_rate_usd
        # Assign to node (in source currency)
        cds.exposure.aggregate.total_base_premium = base_premium_usd * fx_rate


        # Hazard Class calculations -----------------------------------
        if not exposure_by_class.empty:
            exposure_by_class["mask"] = exposure_by_class["class"].where(exposure_by_class["weight"] > 0, -1)
            dominant_class = exposure_by_class["mask"].max()
        else:
            dominant_class = -1
        hazard_class = "Hazard Class " + str(int(abs(dominant_class)))

        # Assign to node
        cds.exposure.aggregate.hazard_group = hazard_class


        # Minimum Premium calculations --------------------------------
        min_prem_params = hx.params.tbl_minimum_premiums
        min_premium_usd = min_prem_params[min_prem_params["class"] == dominant_class]["minimum"].iloc[0] if dominant_class >= 1 else 0
        # Assign to node (in source currency)
        cds.exposure.aggregate.minimum_premium = min_premium_usd * fx_rate

        # ILF Curve Default calculations ------------------------------
        mapping = const.ilf_mapping
        exposure_params["level"] = exposure_params["class"].replace(mapping)
        exposure_by_level = exposure_params.groupby("level")["rateable_revenue_usd"].sum().reset_index()
        # Default curve is the level which has the most revenue allocated to it.
        default_curve = exposure_by_level[exposure_by_level["rateable_revenue_usd"] == max(exposure_by_level["rateable_revenue_usd"])]["level"].iloc[0]
        cds.rating_factors.default_curve = default_curve


        # Guideline Deductible calculations (in USD) -----------------------
        # Total revenue for classes 1,2,3
        revenue_low = exposure_params[exposure_params["class"].isin([1,2,3])]["rateable_revenue_usd"].sum()
        # Total revenue for classes 4,5,6
        revenue_high = exposure_params[exposure_params["class"].isin([4,5,6])]["rateable_revenue_usd"].sum()

        # Parameters depend on whether Canada or not
        location = cds.rating_factors.location
        if location is not None and location.upper() == "CANADA":
            deduct_params = hx.params.tbl_guideline_deduct_calc_CAD
        else:
            deduct_params = hx.params.tbl_guideline_deduct_calc
        
        # Guideline deductible slope and intercept
        low_row = utils.find_last_row(deduct_params, "revenue_low", revenue_low)
        slope_low = low_row["slope"] if not low_row.empty else 0
        intercept_low = low_row["intercept"] if not low_row.empty else 0

        high_row = utils.find_last_row(deduct_params, "revenue_low", revenue_high)
        slope_high = high_row["slope_high"] if not high_row.empty else 0
        intercept_high = high_row["intercept_high"] if not high_row.empty else 0

        # Minimum retention
        row = utils.find_last_row(deduct_params, "revenue_low", rateable_revenue_usd)
        min_retention_usd = row["min_deductible"] if not row.empty else 0

        # Guideline deductible
        if revenue_high == 0:
            guideline_deductible_usd = intercept_low + slope_low * revenue_low
        else:
            if revenue_low == 0:
                guideline_deductible_usd = intercept_high + slope_high * revenue_high
            else:
                guideline_deductible_usd = max(revenue_low * slope_low + revenue_high * slope_high, 25000)
        guideline_deductible_usd = np.round(guideline_deductible_usd, -3) # Round to the nearest 1000
        guideline_deductible_usd = max(guideline_deductible_usd, min_retention_usd) # Ensure is at least size of minimum retention
        # Assign to node (in source currency)
        cds.rating_factors.guideline_deductible = guideline_deductible_usd * fx_rate



    # Annual TV calculations ----------------------------------------------------------------------------------------------------------------------
    elif cds.annualtv_masking:
        turnover = cds.annual_tv.turnover
        # Capped Productions for Rating ------------
        est_productions = cds.exposure.aggregate.annual_tv.number_of_productions or 0
        capped_productions = min(est_productions, 7) if turnover <= 2e6 else est_productions
        # Assign to node
        cds.exposure.aggregate.annual_tv.capped_productions = capped_productions

        # Genre ------------
        genre_params = hx.params.tbl_annualtv_genre

        # list of genres
        genre_list = genre_params["type_name"]
        
        # calcs for each genre
        genre_premiums = []
        for item in genre_list:
            # get percentage of total turnover from UI
            perc = getattr(getattr(cds.exposure.granular.annual_tv.genre, item),"perc_of_total_turnover")
            perc = float(perc)/100 if perc is not None else 0 # convert to decimal

            # Validation: cannot have a negative percentage
            if perc < 0:
                hx.errors.validation("Percentage of Total Turnover cannot be negative for any genres. [Exposure Details]")

            turnover_amount = turnover * perc if turnover is not None else None
            setattr(getattr(cds.exposure.granular.annual_tv.genre, item), "turnover_amount", turnover_amount)

            alloc_production_number = capped_productions * perc if turnover is not None else None
            setattr(getattr(cds.exposure.granular.annual_tv.genre, item), "alloc_production_number", alloc_production_number)

            # pull out relevant average premuim from parameter table
            average_premium_usd = genre_params[genre_params["type_name"]==item]["average_premium"].iloc[0]
            average_premium = average_premium_usd * fx_rate # Convert to source currency
            setattr(getattr(cds.exposure.granular.annual_tv.genre, item), "average_premium", average_premium)

            base_premium = alloc_production_number * average_premium if turnover is not None else 0
            setattr(getattr(cds.exposure.granular.annual_tv.genre, item), "base_premium", base_premium)
            # also append to list for calculating total
            genre_premiums.append(base_premium)

        # Total Base Premium -------------
        total_base_premium = sum(genre_premiums)
        cds.exposure.aggregate.total_base_premium = total_base_premium

        # Selections and Modifiers ------------
        # Selections are fixed to 'Yes' for annual policy selection and aggregate limit selection.

        # Calculate modifiers for remaining selections which lookup parameter tables
        # IMPORTANT: check structure of parameter table: first column must be the selection dropdown. The function refers to index, rather than column name.
        assign_modifier_annualtv(hxd, "jurisdiction")
        assign_modifier_annualtv(hxd, "australian")
        assign_modifier_annualtv(hxd, "lawyers")


    # Individual TV calculations ----------------------------------------------------------------------------------------------------------------------
    elif cds.individualtv_masking:

        # Selections and Modifiers ------------

        # Length type reference
        tv_length_params = hx.params.tbl_indtv_length
        tv_length_selected = cds.exposure.aggregate.individual_tv.length
        # Pick out reference corresponding to selection
        tv_length_ref = utils.parameter_lookup(tv_length_params, "length", tv_length_selected, "column_reference", None)

        # Number of Episodes 
        tv_episodes_selected = cds.exposure.aggregate.individual_tv.number_of_episodes
        tv_episodes_selected = tv_episodes_selected or 0
        if tv_episodes_selected <= 10:
            tv_episodes_mod = tv_episodes_selected # increase by 1, between 0 and 10
        elif tv_episodes_selected <= 20:
            tv_episodes_mod = 10 + 0.5*(tv_episodes_selected - 10) # increase by 0.5, between 10 and 15
        elif tv_episodes_selected <= 30:
            tv_episodes_mod = 15 + 0.25*(tv_episodes_selected - 20) # increase by 0.25, between 15 and 17.5
        else:
            tv_episodes_mod = 17.5 # capped at 17.5
        setattr(cds.individual_tv.modifiers, "number_of_episodes", tv_episodes_mod) #IR: has been removed from UI
        
        # Genre
        tv_genre_params = hx.params.tbl_indtv_genre
        tv_genre_selected = cds.individual_tv.selections.genre
        # Look up modifier: row corresponds to selected genre type, column corresponds to tv_length_ref
        tv_genre_mod = tv_genre_params[tv_genre_params["exhibition_type"] == tv_genre_selected].iloc[0,tv_length_ref] if (tv_genre_selected is not None and tv_length_ref is not None) else 0
        # Convert this base premium to source currency
        base_premium = tv_genre_mod * fx_rate
        setattr(cds.individual_tv.modifiers, "genre", base_premium)
        setattr(cds.exposure.aggregate, "total_base_premium", base_premium)

        # Jurisdiction
        tv_juris_params = hx.params.tbl_indtv_jurisdiction
        tv_juris_selected = cds.individual_tv.selections.jurisdiction
        # Pick out modifier and reference corresponding to selection
        tv_juris_mod = utils.parameter_lookup(tv_juris_params, "type", tv_juris_selected, "modifier", None)
        # tv_juris_ref = utils.parameter_lookup(tv_juris_params, "type", tv_juris_selected, "min_column_reference") # IR: not used
        # Assign back to UI
        setattr(cds.individual_tv.modifiers, "jurisdiction", tv_juris_mod)


        # Calculate modifiers for remaining selections which lookup parameter tables
        # IMPORTANT: check structure of parameter table: first column must be the selection dropdown. The function refers to index, rather than column name.
        assign_modifier_individualtv(hxd, "policy_period")
        assign_modifier_individualtv(hxd, "soundtrack")
        assign_modifier_individualtv(hxd, "merchandising")
        assign_modifier_individualtv(hxd, "australian")
        assign_modifier_individualtv(hxd, "coverage_basis")
        assign_modifier_individualtv(hxd, "established_format")
        assign_modifier_individualtv(hxd, "primary_broadcast")
        assign_modifier_individualtv(hxd, "lawyers")
        assign_modifier_individualtv(hxd, "webisodes")

        # Coverage Basis modifier and reference
        if cds.individual_tv.selections.coverage_basis == "Claims Made":
            coverage_basis_modifier = const.claimsmade_modifier    
        elif cds.rating_factors.location == "CANADA" and  cds.individual_tv.selections.coverage_basis == "Occurrence":
            coverage_basis_modifier = const.occurence_modifier_canada
        else: 
            coverage_basis_modifier = const.occurence_modifier
        # Assign back to UI
        setattr(cds.individual_tv.modifiers, "coverage_basis", coverage_basis_modifier)
        

    # Individual Film calculations ---------------------------------------------------------------------------------------------------------------------
    elif cds.individualfilm_masking:

        # Selections and Modifiers ------------

        # Scope of Release modifier
        film_scope_params = hx.params.tbl_film_exhibition
        film_scope_selected = cds.exposure.aggregate.individual_film.exhibition
        # Pick out modifier corresponding to selection. Note, this particular "modifier" is actually base premium
        film_scope_modifier = utils.parameter_lookup(film_scope_params, "scope_of_release", film_scope_selected, "base_premium", 0)
        # Convert this base premium to source currency
        base_premium = film_scope_modifier * fx_rate
        setattr(cds.individual_film.modifiers, "exhibition", base_premium)
        setattr(cds.exposure.aggregate, "total_base_premium", base_premium)

        # Jurisdiction modifier and reference
        film_juris_params = hx.params.tbl_film_jurisdiction
        film_juris_selected = cds.individual_film.selections.jurisdiction
        # Pick out modifier and reference corresponding to selection 
        film_juris_modifier = utils.parameter_lookup(film_juris_params, "type", film_juris_selected, "modifier", None)
        # film_juris_ref = utils.parameter_lookup(film_juris_params, "type", film_juris_selected, "minimum_column_reference", None) # IR: not used
        # Assign back to UI
        setattr(cds.individual_film.modifiers, "jurisdiction", film_juris_modifier)

        # Coverage Basis modifier and reference
        if cds.individual_film.selections.coverage_basis == "Claims Made":
            coverage_basis_modifier = const.claimsmade_modifier    
        elif cds.rating_factors.location == "CANADA" and  cds.individual_film.selections.coverage_basis == "Occurrence":
            coverage_basis_modifier = const.occurence_modifier_canada
        else: 
            coverage_basis_modifier = const.occurence_modifier
        # Assign back to UI
        setattr(cds.individual_film.modifiers, "coverage_basis", coverage_basis_modifier)



        # Calculate modifiers for remaining selections which lookup parameter tables
        # IMPORTANT: check structure of parameter table: first column must be the selection dropdown. The function refers to index, rather than column name.
        assign_modifier_individualfilm(hxd, "budget")
        assign_modifier_individualfilm(hxd, "cast")
        assign_modifier_individualfilm(hxd, "appeal")
        assign_modifier_individualfilm(hxd, "subject_matter")
        # assign_modifier_individualfilm(hxd, "jurisdiction")
        assign_modifier_individualfilm(hxd, "foreign_language")
        assign_modifier_individualfilm(hxd, "soundtrack")
        assign_modifier_individualfilm(hxd, "merchandising")
        assign_modifier_individualfilm(hxd, "policy_period")
        assign_modifier_individualfilm(hxd, "australian")
       # assign_modifier_individualfilm(hxd, "coverage_basis")
        assign_modifier_individualfilm(hxd, "established_format")
        assign_modifier_individualfilm(hxd, "lawyers")


    pass