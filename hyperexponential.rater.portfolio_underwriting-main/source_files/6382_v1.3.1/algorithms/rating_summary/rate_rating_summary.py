from libraries.model_profiler.algorithms.profiling_hxd_functions    import time_me
from algorithms.rating_summary.rating_summary_helpers_bbt           import rate_rating_summary_bbt
from algorithms.rating_summary.rating_summary_helpers_case_priced   import rate_rating_summary_case_priced
from algorithms.rating_summary.rating_summary_helpers_non_bbt       import (set_tech_prem_dropdown_list, rate_rating_summary_non_bbt)

@time_me
def rate_rating_summary(hxd, is_bbt, rater):
    # Set up the dropdown options for technical premium in the UI or internal structure
    set_tech_prem_dropdown_list(hxd)
    is_case_priced = hxd.cds.standard_fields.rating_methodology != "Rater"

    if is_case_priced:
        rate_rating_summary_case_priced(hxd,rater)      # If Case Priced, call the specific rating summary function
    elif is_bbt:  
        rate_rating_summary_bbt(        hxd, rater)     # If BBT, call the specific rating summary function
    else:
        rate_rating_summary_non_bbt(    hxd, rater)     # If not BBT, call the regular rating summary function with the provided rater

