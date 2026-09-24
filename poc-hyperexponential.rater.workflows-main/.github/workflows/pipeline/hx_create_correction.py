#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#
#' 
#' Progam Name: Hx Create Correction
#' Author: Mark Fleet
#' Date: 23/02/2026
#' Description: Creates a correction using a record_id
#' 
#'
#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#

# Import Libraries ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from hx_auth import AzureADCredentials, HxRenewAuth
from github_misc import set_output
from api_requests import api_request_retry
import os

# Parameters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
hx_policy_option_id = os.environ.get("HX_POLICY_OPTION_ID")
hx_correction_name = os.environ.get("HX_CORRECTION_NAME")
hx_model_id = os.environ.get("HX_MODEL_ID")
hx_base_url = os.environ.get("HX_VERSIONED_API_BASE_URL")
hx_api_version = os.environ.get("HX_VERSIONED_API_VERSION")
hx_tenant_id = os.environ.get("HX_AZURE_AD_TENANTID")
hx_client_id = os.environ.get("HX_AZURE_AD_CLIENTID")
hx_client_secret = os.environ.get("HX_AZURE_AD_CLIENTSECRET")
hx_scope = os.environ.get("HX_AZURE_AD_SCOPE")

# Hx Auth
hx_auth = HxRenewAuth(
    AzureADCredentials(
        azure_ad_tenant = hx_tenant_id,
        client_id = hx_client_id,
        client_secret = hx_client_secret,
        grant_type="client_credentials",
        scope = hx_scope,
    )
)

# Hx headers
hx_headers = {
    "Authorization": f"Bearer {hx_auth.bearer_token}",
    "Hx-Api-Version": hx_api_version
}

def main():

    correction_status = None
    has_error = False

    # Get record_id using policy_option_id
    policy_option_url = f"{hx_base_url}options/{hx_policy_option_id}"
    policy_option_resp = api_request_retry("get", policy_option_url, headers=hx_headers)
    if policy_option_resp.status_code == 200:
        record_id = policy_option_resp.json()["record_id"]
    else:
        correction_status = f"Error: Failed to get Policy Option Id {hx_policy_option_id}. API Response: {policy_option_resp.json()}"
        has_error = True
    
    # Get model_version_id using record_id
    if has_error == False:
        record_url = f"{hx_base_url}records/{record_id}"
        record_resp = api_request_retry("get", record_url, headers=hx_headers)
        if record_resp.status_code == 200:
            model_version_id = record_resp.json()["model_version_id"]
        else:
            correction_status = f"Error: Failed to get Record Id {record_id}. API Response: {record_resp.json()}"
            has_error = True
    
    # Get model_id using model_version_id
    if has_error == False:
        model_version_url = f"{hx_base_url}model-versions/{model_version_id}"
        model_version_resp = api_request_retry("get", model_version_url, headers=hx_headers)
        if model_version_resp.status_code == 200:
            model_id = model_version_resp.json()["model"]["id"]
        else:
            correction_status = f"Error: Failed to get Model Version Id {model_version_id}. API Response: {model_version_resp.json()}"
            has_error = True
        
    # Validate that model_id matches repo
    if has_error == False:
        if int(model_id) != int(hx_model_id):
            print(f"model_id: {model_id}")
            print(f"hx_model_id: {hx_model_id}")
            correction_status = f"Error: You are trying to create a correction for a different model. Please check that the Policy Option Id is correct"
            has_error = True

    # Create correction using record_id
    if has_error == False:
        correction_url = f"{hx_base_url}records/{record_id}/corrections"
        json_dat = {
            "name" : hx_correction_name
        }
        correction_record_id = None
        correction_option_id = None
        correction_resp = api_request_retry("post", correction_url, headers=hx_headers, json=json_dat)
        if correction_resp.status_code <= 201:
            correction_record_id = correction_resp.json()["id"]
            correction_option_id = correction_resp.json()["option_id"]
            correction_status = f"Successfully created correction with Record Id {correction_record_id} from Policy Option Id {hx_policy_option_id} having Record Id {record_id}"
        else:
            correction_status = f"Error: Failed to create correction from Policy Option Id {hx_policy_option_id} having Record Id {record_id}. API Response: {correction_resp.json()}"
            has_error = True
  
    # Set outputs
    set_output('correction_status', correction_status)
    set_output('has_error', has_error)

if __name__ == "__main__":
    main()