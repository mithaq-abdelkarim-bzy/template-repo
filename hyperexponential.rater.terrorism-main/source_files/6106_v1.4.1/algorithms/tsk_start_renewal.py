##############################################################################################################################
################                             NOTES                                                            ################ 
##############################################################################################################################

### 

##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################

### 1) Comment out policy # on row 44
### 2) 
### 3) 
### 4) 
### 5) 

##############################################################################################################################
import hx, os, openpyxl, json, requests
import pandas as pd
pd.set_option('display.max_rows', None)

from algorithms.rate_utilities                           import look_up, rgetattr, pd_df_from_hx_list, write_pd_to_hxd, date_to_string
from algorithms.rate_utilities                           import sanitize_and_sort_expiring_list_by_renewal, split_renewal_list_by_expiring
from algorithms.rate_utilities                           import get_countries_retrieved, one_layer, rgetkey, rsetattr, rgetattr

from datetime                                            import datetime, date

from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from algorithms.tsk_rarc                                 import get_expiring_data

# Renewal
def tsk_start_renewal(hxd, progress):    
    # The following statement checks that the expiring information has been imported for renewals. Some teams might want to start
    # from a blank rater each time, in which case update the below
    ms      = hxd.model_state
    sf      = hxd.cds.standard_fields
    layer   = hxd.cds.layers[0]

    if not sf.insured_name:
        ms.landing_page_info = "❗**FAILED**: Click 'Undo' then 'Import Expiring Policy Data' in the top right corner.❗"
    else:
        # standard model code
        ms.pressed_start_renewal_task = True
        ms.expiring_policy_option_id  = hx.meta.expiring_policy_option_id #or 1024296 # NOTE: id used for testing
        sf.is_renewal                 = True
        ms.is_migrated                = False

        ### custom code
    
        ##########################################
        ### Sourcing data from expiring policy
        ##########################################

        # Initialise the hx_renew_api library
        hx_renew = init_hx_renew_api()

        # Get expiring policy data
        expiring_policy_option_id   = ms.expiring_policy_option_id
        expiring_response           = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False).json()
        expiring_data               = expiring_response["data"]

        # Get Specifc Node Values
        expiring_ihs_default        = expiring_data["cds"]["layers"][0]["risk_adjustments"]["ihs_score"]["calculated"]
        expiring_ihs_selected       = expiring_data["cds"]["layers"][0]["risk_adjustments"]["ihs_score"]["selected"]


        ##########################################
        ### Updating Values
        ##########################################

        # update policy section reference - notice we read it in and then write to it using non-resetting async output behaviours
        # https://www.beazley.hxrenew.com/customer-service/platform/developer/building-your-model/algorithms/asynchronous-tasks#writing-to-async-inputs-from-your-rating-algorithm
        ref     = layer.section_reference
        if ref is not None and len(ref) == 12:
            inc_date                            = hxd.hx_core.inception_date
            new_yr                              = str(inc_date.year)[2:]
            hxd.cds.layers[0].section_reference = ref[:6] + new_yr + ref[8:]

        # setting default status on renewal
        layer.status = "Assessment Pending"

        # setting expiring ihs values
        layer.risk_adjustments.ihs_score_expiring.calculated = expiring_ihs_default
        layer.risk_adjustments.ihs_score_expiring.selected   = expiring_ihs_selected

        # reset perils confirmation
        # done by simply setting temp_perils as an output in the data schema
        # "temp_perils":                      hx.Str( mode="input", default="{}", async_output=["task_confirm_limits","start_renewal_task"]),

        # reset ihs loaded info
        # done by simply setting any field that was an:
        #   async_output of "task_fetch_ihs_data" to
        #   async_output of "task_fetch_ihs_data","start_renewal_task"

