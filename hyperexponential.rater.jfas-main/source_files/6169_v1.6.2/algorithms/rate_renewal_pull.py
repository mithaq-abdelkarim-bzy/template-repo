import hx
import requests
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_z_utilities as utils
from operator import itemgetter
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api

def start_renewal(hxd,df):
    cds = hxd.cds

    if not cds.standard_fields.underwriter:
        hx.errors.fatal("Please press 'Undo' and 'Import Expiring Policy Data' at the top right corner")
        
    cds.model_state.pressed_start_renewal_task = True

    user = hx.secrets.rest_api_user
    password = hx.secrets.rest_api_password
    expiring_policy_option_id = cds.risk_info.expiring_policy_option_id.selected
    #expiring_policy_option_id = 86468

    # Call to API
    v2_api = init_hx_renew_api()
    response = v2_api.snapshots.get_snapshot(expiring_policy_option_id)

    # Error handling based on status code returned by API
    if response.ok:
        # results stored in dict : {data:{variable_name: value}}
        result = response.json()
        data = result["data"]

        cds.risk_info.new_replacement = data["cds"]["risk_info"]["insured_name_final"]
        cds.standard_fields.policy_reference = ""
        cds.layers[0].status = "Quoted"
        cds.standard_fields.is_renewal = True
    else:
        try:
            response_json = response.json()
            error = f"Error: {response_json.get('title')}"
            error += f"\nDetail: {response_json.get('detail')}" if response_json.get("detail") else ""
            hx.errors.fatal(error)
        except:
            hx.errors.fatal(f"Error: {response.text}")

        




