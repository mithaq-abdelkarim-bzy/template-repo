import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
import algorithms.rate_constants as const
from algorithms import parameter_tables_schema as params
from operator import itemgetter
from algorithms.rate_helpers import set_exp_factor_nodes, validate_min_max, validate_comments, schedule_mod_calculations, set_optional_coverages_nodes, set_optional_coverages_outputs

def rate_adjustments(hxd):
    cds = hxd.cds

    if cds.standard_rater_masking:

        # Longevity Factor Calculations ------------------------------
        years_in_business = cds.rating_factors.years_in_business
        longevity_params = hx.params.tbl_longevity_factor
        # Look up years_in_business in table
        row = longevity_params[longevity_params["years_in_business"] == years_in_business] 
        # Output corresponding factor from relevant row
        cds.modifiers.longevity_factor = row.iloc[0]["factor"] if not row.empty else 1


        # Experience Factor Calculations --------------------------------------------
        # Pull out row of parameter table which corresponds to Response selected in UI
        experience_params = hx.params.tbl_experience_factor
        experience_factor_row = experience_params[experience_params["experience"] == getattr(getattr(cds.modifiers, "experience_factor"),"response")].iloc[0]
        # Set min and max, and get selected value from UI
        experience_factor_row = set_exp_factor_nodes(hxd, experience_factor_row)

        # Validation: check selections are within bounds
        experience_factor_df = experience_factor_row.to_frame().T # convert to pandas df for validation function
        if (validate_min_max(experience_factor_df) == False):
            hx.errors.validation("Experience Factor value outside allowable range. [Adjustments]")

        # Set output experience factor to use in pricing
        experience_factor_output = experience_factor_row["selected"] if experience_factor_row["selected"] is not None else experience_factor_row["default"]
        cds.modifiers.experience_factor.output = experience_factor_output
        
        # Schedule Mod Calculations -------------------------------------------------
        # Set min and max, and validate selected is within bounds. Return the total schedule rating modification.
        if cds.media_masking == True:    
            cds.modifiers.total_schedule_mod = schedule_mod_calculations(hxd, "media")
        elif cds.music_masking == True:
            cds.modifiers.total_schedule_mod = schedule_mod_calculations(hxd, "music")
        elif cds.tvfilm_masking == True:
            cds.modifiers.total_schedule_mod = schedule_mod_calculations(hxd, "tvfilm")


        # Optional Coverages Calculations -------------------------------------------
        # Info Sec Liability, Tech E&O and False Advertising
        # Set min and max, and get selected values from UI
        optional_coverages = hx.params.table_optional_coverages
        optional_coverages = optional_coverages.apply(lambda row: set_optional_coverages_nodes(cds.modifiers.optional_coverages, row), axis=1)

        # Set output to use in pricing, picking up default where necessary.
        optional_coverages["default"] = np.where(optional_coverages["included"]=="Yes", const.optional_default_yes, const.optional_default_no) # optional_default_yes never actually picked up because blank selected % not possible. 
        optional_coverages["output"] = np.where((optional_coverages["included"]=="No") | (optional_coverages["selected"].isnull()), optional_coverages["default"], optional_coverages["selected"])
        optional_coverages.apply(lambda row: set_optional_coverages_outputs(cds.modifiers.optional_coverages, row), axis=1)

        # Validation: check selections are within bounds
        optional_coverages["min"] = pd.to_numeric(optional_coverages["min"]) / 100  #convert to decimal
        optional_coverages["max"] = pd.to_numeric(optional_coverages["max"]) / 100  #convert to decimal
        if (validate_min_max(optional_coverages) == False):
            hx.errors.validation("Optional Coverage value outside allowable range. [Adjustments]")

        # Validation: ensure comments have been added where selections have been made
        if (validate_comments(optional_coverages) == False):
            hx.errors.validation("Please add comments for Optional Coverage selection made. [Adjustments]")

        # Extended Reporting Period ------------------------------------------------
        cds.modifiers.extended_reporting_period.factor = 1
    

    pass