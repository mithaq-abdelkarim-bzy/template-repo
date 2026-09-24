#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#
#' 
#' Progam Name: Hx Reject Releases
#' Author: Mark Fleet
#' Date: 18/12/2024
#' Description: Approves model version releases
#' 
#'
#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#

# Import Libraries ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from hx_auth import AzureADCredentials, HxRenewAuth
from github_misc import set_output
from api_requests import api_request_retry
import os
import json  

# Parameters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
model_id = os.environ.get("HX_MODEL_ID")
base_url = os.environ.get("HX_API_BASE_URL")
output_folder = os.environ.get("OUTPUT_FOLDER")

def main():
    # Auth
    auth = HxRenewAuth(
        AzureADCredentials(
            azure_ad_tenant=os.environ.get("HX_AZURE_AD_TENANTID"),
            client_id=os.environ.get("HX_AZURE_AD_CLIENTID"),
            client_secret=os.environ.get("HX_AZURE_AD_CLIENTSECRET"),
            grant_type="client_credentials",
            scope=os.environ.get("HX_AZURE_AD_SCOPE"),
        )
    )

    # Set URLs
    base_url = os.environ.get("HX_API_BASE_URL")
    published_model_versions_url = f"{base_url}model-versions?model_id={model_id}&sort=-id&limit=1000&published=true"

    # Set headers
    headers = {"Authorization": f"Bearer {auth.bearer_token}"}

    # Open metadata for list of expected published model versions
    with open(os.path.join(output_folder, 'metadata.json')) as f:
        d = json.load(f)
    required_published_model_versions = d["published_model_versions"]

    # Get published model versions
    model_versions_resp = api_request_retry("get", published_model_versions_url, headers=headers)
    if model_versions_resp.status_code != 200:
        raise Exception(f"Failed to get published model versions")
    published_model_versions = model_versions_resp.json()

    # Reject new model version(s)
    rejected_model_versions = []
    for r in required_published_model_versions:
        if not any(p['id'] == r["id"] for p in published_model_versions):

            # Set URLs
            model_version_id = r['id']
            reject_release_url = f"{base_url}model-versions/{model_version_id}/releases/reject"

            # Set payload
            json_dat = {
            "comments" : "Rejected via GitHub Pipeline"
            }

            # Reject
            reject_release_resp = api_request_retry("post", reject_release_url, headers=headers, json=json_dat)
            if reject_release_resp.status_code == 200:
                print(f"Successfully rejected release for model version {model_version_id}")
                rejected_model_versions.append(f"{model_version_id}")
            else:
                print(reject_release_resp.json())
                raise Exception(f"Failed to reject model version {model_version_id}")
  
    # Set outputs
    set_output('rejected_model_versions', ",".join(rejected_model_versions))

def load_metadata(file):
    with open(file) as f:
        d = json.load(f)
        return d

if __name__ == "__main__":
    main()