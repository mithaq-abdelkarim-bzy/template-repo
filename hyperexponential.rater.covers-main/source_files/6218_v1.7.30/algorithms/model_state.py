import hx
import requests
import algorithms.rate_utilities as utils
from operator import itemgetter
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api

def model_state(hxd):
    '''
    Controls which page to show and hide when the start renewal button is pressed
    '''
    ms = hxd.model_state

    expiring_policy_option_id = hx.meta.expiring_policy_option_id
    #expiring_policy_option_id = 1553646 # For debugging in dev mode

    # NOTE: This only displays the landing page for policies which are a renewal, 
    # to display the landing page always, then remove the first boolean
    if (expiring_policy_option_id is None) or (ms.pressed_start_renewal_task) or (ms.expiring_policy_option_id == expiring_policy_option_id):
        ms.show_landing_page = False
        ms.show_after_landing_page = True
        ms.show_rate_change = True #hxd.cds.standard_fields.is_renewal
    else:
        ms.show_landing_page = True
        ms.show_after_landing_page = True #False
        ms.show_rate_change = True #False

