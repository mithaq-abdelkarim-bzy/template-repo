import hx, json, openpyxl
import pandas as pd

from algorithms.rate_utilities                           import look_up, rgetattr, pd_df_from_hx_list, write_pd_to_hxd, date_to_string
from algorithms.rate_utilities                           import sanitize_and_sort_expiring_list_by_renewal, split_renewal_list_by_expiring
from algorithms.rate_utilities                           import get_countries_retrieved, one_layer, rgetkey, rsetattr, rgetattr

from copy                                                import deepcopy
from algorithms.data_schema.sch_rater_defined            import perils, ihs_risk_names

pd.set_option('display.max_rows', None)


# Confirm Policy Limits entered on perils tab and dump values to a json
def tsk_confirm_limits(hxd, progress):    
    
    expo = hxd.cds.exposure.aggregate

    temp_perils = {}
    for peril in perils.keys():
        temp_perils[peril] = {}
        temp_perils[peril]["limit_selected"]        = rgetattr(expo, f"perils/{peril}/limit_selected")
        temp_perils[peril]["excess_selected"]       = rgetattr(expo, f"perils/{peril}/excess_selected")
        temp_perils[peril]["deductible_selected"]   = rgetattr(expo, f"perils/{peril}/deductible_selected")

    expo.temp_perils = json.dumps(temp_perils)