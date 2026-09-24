#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#
#' 
#' Progam Name: Hx Get Model Source Files
#' Author: Mark Fleet
#' Date: 16/08/2024
#' Description: Gets a model version's source files
#' 
#'
#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#

# Import Libraries ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from hx_auth import AzureADCredentials, HxRenewAuth
from hx_misc import read_model_versions_json, parse_model_version_label, get_model_version_folder
from github_misc import set_output
from api_requests import api_request_retry
import os
import zipfile
import shutil
from io import BytesIO
import json

# Parameters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
model_id = os.environ.get("HX_MODEL_ID")
ignore_model_version_ids = os.environ.get("HX_IGNORE_MODEL_VERSION_IDS")
output_folder = os.environ.get("OUTPUT_FOLDER")
hx_base_url = os.environ.get("HX_API_BASE_URL")
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
hx_headers = {"Authorization": f"Bearer {hx_auth.bearer_token}"}

def main():

    # Set URLs
    published_model_versions_url = f"{hx_base_url}model-versions?model_id={model_id}&sort=-id&limit=1000&published=true"
    non_published_model_versions_url = f"{hx_base_url}model-versions?model_id={model_id}&sort=-id&limit=50&published=false"

    # Create output folder if not exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read existing model versions list
    model_versions_existing = read_model_versions_json(folder = output_folder)

    print(f"Getting source files for Model {model_id}")

    # Get published model versions
    model_versions_resp = api_request_retry("get", published_model_versions_url, headers=hx_headers)
    if model_versions_resp.status_code != 200:
        raise Exception(f"Failed to get published model versions")
    published_model_versions = model_versions_resp.json()

    # Get non published model versions
    model_versions_resp = api_request_retry("get", non_published_model_versions_url, headers=hx_headers)
    if model_versions_resp.status_code != 200:
        raise Exception(f"Failed to get non published model versions")
    non_published_model_versions = model_versions_resp.json()

    # Merge and sort arrays
    model_versions = published_model_versions
    model_versions.extend(non_published_model_versions)
    model_versions = sorted(model_versions, key=lambda x: x['id'], reverse=True)

    # Parse labelS
    for v in list(model_versions):
        v["parsed_label"] = parse_model_version_label(v["label"])

    # Iterate over model versions
    source_files_changed = False
    redundant_model_version_folders = []
    ignore_model_version_ids_list = [int(x.strip()) for x in ignore_model_version_ids.split(',')]
    for model_version in model_versions:
        model_version_id = model_version["id"]
        model_version_label = model_version["label"]

        # Check if we already have the source files
        model_version_folder = None
        existing_model_version_folder = get_model_version_folder(output_folder, model_version_id)
        if existing_model_version_folder is not None:
            print(f"Model version {model_version_id} already present")
            # Check if label has changed - we must re-download the source files due to sparse checkout 
            model_version_folder = f"{output_folder}/{model_version_id}_{str(model_version_label)}"
            new_model_version_folder_exists = os.path.isdir(model_version_folder)
            if existing_model_version_folder != model_version_folder and not new_model_version_folder_exists:
                print(f"Label has changed - Re-download source files to new folder and flag old folder for removal")
                model_version_folder = None
                redundant_model_version_folders.append(f"{'"' + existing_model_version_folder + '"'}") # Must have double quotes so array can be split from GA

        # Download source files
        if model_version_folder is None and model_version_id not in ignore_model_version_ids_list:
            source_files_changed = True
            print(f"Getting model version {model_version_id}")
            source_files_url = f"{hx_base_url}/model-versions/{model_version_id}/source-files"
            source_files_stream = api_request_retry("get", source_files_url, headers=hx_headers, stream=True)
            if source_files_stream.status_code != 200:
                raise Exception(f"Failed to get source files")
            source_files_zip = zipfile.ZipFile(BytesIO(source_files_stream.content))
            model_version_folder = f"{output_folder}/{model_version_id}_{str(model_version_label)}"
            source_files_zip.extractall(model_version_folder)
            shutil.rmtree(f"{model_version_folder}/libraries", ignore_errors=True)
            enrich_metadata(model_version_folder)


    # Create model versions json
    if model_versions != model_versions_existing:
        source_files_changed = True
        create_model_versions_json(model_versions)

    # Check for pending changes
    pending_changes = False
    for v in model_versions:
        if v["release_requested"] == True:
            pending_changes = True

    # Check for model versions newly marked for testing
    newly_marked_for_testing = False
    if model_versions_existing is not None:
        testable_versions = [v for v in model_versions if v['testable'] == True and v['parsed_label']['version_valid'] == True and v['parsed_label']['version_suffix'] is None]
        if testable_versions:
            testable_versions_existing = [v for v in model_versions_existing if v['testable'] == True and v['parsed_label']['version_valid'] == True and v['parsed_label']['version_suffix'] is None]
            testable_versions_ids_existing = [v['id'] for v in testable_versions_existing]
            new_testable_versions = [v for v in testable_versions if v['id'] not in testable_versions_ids_existing]
            if new_testable_versions:
                newly_marked_for_testing = True

    set_output('source_files_changed', source_files_changed)
    set_output('pending_changes', pending_changes)
    set_output('newly_marked_for_testing', newly_marked_for_testing)
    set_output('redundant_model_version_folders', " ".join(redundant_model_version_folders))

    print(f"Complete")

def create_model_versions_json(model_versions):
    model_versions_json = "model_versions.json"
    filepath = os.path.join(output_folder, model_versions_json)
    with open(filepath, 'w') as file:
        json.dump(model_versions, file)

def enrich_metadata(model_version_folder):
    metadata_path = os.path.join(model_version_folder, "metadata.json")
    with open(metadata_path, 'r') as file:
            data = file.read()
    metadata = json.loads(data)
    for user_library_dependency in metadata['user_library_dependencies']:
        user_library_dependency['label'] = model_version_id_to_label(user_library_dependency['model_version_id'])
    with open(metadata_path, 'w') as file:
        json.dump(metadata, file)

def model_version_id_to_label(model_version_id):
    base_url = os.environ.get("HX_API_BASE_URL")
    model_version_url = f"{base_url}/model-versions/{model_version_id}"
    model_version_resp = api_request_retry("get", model_version_url, headers=hx_headers)
    if model_version_resp.status_code != 200:
        raise Exception(f"Failed to get model version")
    model_version = model_version_resp.json()
    model_version_label = model_version['label']
    return model_version_label

if __name__ == "__main__":
    main()