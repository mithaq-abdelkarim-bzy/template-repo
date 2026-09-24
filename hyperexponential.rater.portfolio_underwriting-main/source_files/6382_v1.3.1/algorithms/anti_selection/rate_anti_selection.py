from algorithms.anti_selection.anti_selection_helpers import (
    build_anti_selection_matrix,
    add_charge_details
)


# Entry point for calculating anti-selection charges
# Builds the matrix and attaches explanatory notes for UI/reporting
def rate_anti_selection(hxd):
    # Compute guideline, suggested, and final charges for all sections
    build_anti_selection_matrix(hxd)
    
    # Populate notes/details for each section in the UI/report
    add_charge_details(hxd)

    # THIS HELPER IS RUN BUT AFTER THE LOSS RATIOS HAVE BEEN COMBINED ON THE RATING SUMMARY - SEE rate_rating_summary_non_bbt
    # build_anti_selection_applied_charge(hxd)