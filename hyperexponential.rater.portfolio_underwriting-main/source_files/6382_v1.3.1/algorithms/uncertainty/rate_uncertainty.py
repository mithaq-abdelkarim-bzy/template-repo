from algorithms.uncertainty.uncertainty_helpers import (
    build_uncertainty_matrix,
    add_load_details
)


# Entry point for rating uncertainty: builds matrix and adds notes
def rate_uncertainty(hxd):
    # Compute all matrix values and update overall totals
    build_uncertainty_matrix(hxd)
    
    # Populate HX with notes/descriptions for each uncertainty factor
    add_load_details(hxd)