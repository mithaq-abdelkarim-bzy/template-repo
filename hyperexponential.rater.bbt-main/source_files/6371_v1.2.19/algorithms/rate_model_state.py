import hx
import requests
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api


def rate_model_state(hxd):
    cds = hxd.cds
    '''
    Controls which page to show and hide when the start renewal button is pressed
    '''
    expiring_policy_option_id = hx.meta.expiring_policy_option_id

    # latest iteration of skeleton model has an async task used to sync cds.model_state.expiring_policy for all migrated data at the time of migration
    # bbt was created prior to this with an extra field coded to tag migrated records hence we condition additionally on cds.model_state.migrated_record
    # to achieve the same outcome

    if expiring_policy_option_id is None or cds.model_state.pressed_start_renewal_task or (cds.model_state.expiring_policy == expiring_policy_option_id) or cds.model_state.migrated_record:
        cds.model_state.show_landing_page = False
        cds.model_state.show_after_landing_page = True
    else:
        cds.model_state.show_landing_page = True
        cds.model_state.show_after_landing_page = False