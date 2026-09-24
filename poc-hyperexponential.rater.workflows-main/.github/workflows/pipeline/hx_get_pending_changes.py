#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#
#' 
#' Progam Name: Hx Get Pending Releases
#' Author: Mark Fleet
#' Date: 16/08/2024
#' Description: Checks a model for pending releases and checks for breaking changes
#' 
#'
#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#

# Import Libraries ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from hx_auth import AzureADCredentials, HxRenewAuth
from hx_misc import parse_model_version_label, read_model_versions_json, get_model_version_from_label
from github_misc import set_output
from api_requests import api_request_retry
import hx_data_schema as hx
import os
import sys
import importlib
import json
from json import JSONEncoder
import shutil
from deepdiff import DeepDiff
import datetime
import zipfile
import shutil
from io import BytesIO

# Parameters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
model_id = os.environ.get("HX_MODEL_ID")
output_folder = os.environ.get("OUTPUT_FOLDER")
source_files_prod = "source_files_prod"
source_files_preprod = "source_files_preprod"
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

    # Read model version lists. Note: must be sorted descending already.
    model_versions_preprod = read_model_versions_json(folder = source_files_preprod)

    # Set URLs
    published_model_versions_url = f"{hx_base_url}model-versions?model_id={model_id}&sort=-id&limit=1000&published=true"
    pending_model_versions_url = f"{hx_base_url}model-versions?model_id={model_id}&sort=-id&limit=1000&release_requested=true"

    # Get published model versions
    model_versions_resp = api_request_retry("get", published_model_versions_url, headers=hx_headers)
    if model_versions_resp.status_code != 200:
        raise Exception(f"Failed to get published model versions")
    published_model_versions = model_versions_resp.json()

    # Get pending model versions
    model_versions_resp = api_request_retry("get", pending_model_versions_url, headers=hx_headers)
    if model_versions_resp.status_code != 200:
        raise Exception(f"Failed to get pending model versions")
    pending_model_versions = model_versions_resp.json()

    # Create output folder
    os.makedirs(output_folder)

    # Sync published model versions
    # Non main version (where the label contains suffix) - all other verions will be unpublished
    # Unless no pending model versions
    required_published_model_versions = []
    for v in published_model_versions:
        p = parse_model_version_label(v["label"])
        if p['version_valid'] == True and p['version_suffix'] != None:
            persist_model_version(v, required_published_model_versions)
        elif len(pending_model_versions) == 0:
            persist_model_version(v, required_published_model_versions)

    # Loop through pending model versions
    pending_changes = False
    breaking_changes = False
    breaking_changes_desc = ""
    preprod_in_sync = False
    pending_model_name = ""
    pending_model_version_id = ""
    pending_model_version_label = ""
    pending_model_version_description = ""
    pending_model_version_developer = ""
    for v in pending_model_versions:
        pending_changes = True
        pending_model_name = v["model"]["name"]
        pending_model_version_id = v["id"]
        pending_model_version_label = v["label"]
        pending_model_version_description = v["description"]
        pending_model_version_developer = v["release_requested_by_user"]["name"]

        # Parse label
        parsed_ver = parse_model_version_label(pending_model_version_label)

        # Check for valid version
        if parsed_ver['version_valid'] == False:
            print(f"-- Invalid model version label - model version {pending_model_version_id}_{str(pending_model_version_label)} --")
            breaking_changes = True
            breaking_changes_desc = f"-- Invalid model version label - model version {pending_model_version_id}_{str(pending_model_version_label)} --"
            persist_model_version(v, required_published_model_versions)
            continue

        # Skip checks for non main version (where the label contains suffix)
        if parsed_ver['version_suffix'] != None:
            print(f"-- Non main version found and skipping breaking changes checks - model version {pending_model_version_id}_{str(pending_model_version_label)} --")
            persist_model_version(v, required_published_model_versions)
            continue
        
        # Get latest published version
        previous_model_version = get_previous_model_version(published_model_versions)

        # Check for breaking changes in pending model versions
        breaking_changes, breaking_changes_desc, preprod_in_sync = check_schema_differences(pending_model_version_id, pending_model_version_label, previous_model_version['version_id'], previous_model_version['version_label'], model_versions_preprod)

        # Persist model version to output folder
        persist_model_version(v, required_published_model_versions)

        # Exit loop
        break

    # Create metadata
    create_metadata(required_published_model_versions)

    set_output('pending_changes', pending_changes)
    set_output('breaking_changes', breaking_changes)
    set_output('breaking_changes_desc', breaking_changes_desc)
    set_output('preprod_in_sync', preprod_in_sync)
    set_output('pending_model_name', pending_model_name)
    set_output('pending_model_version_id', pending_model_version_id)
    set_output('pending_model_version_label', pending_model_version_label)
    set_output('pending_model_version_description', pending_model_version_description)
    set_output('pending_model_version_developer', pending_model_version_developer)

def get_previous_model_version(published_model_versions):
    for v in published_model_versions:
        version_id = v["id"]
        version_label = v["label"]
        parsed_ver = parse_model_version_label(version_label)
        if parsed_ver['version_valid'] == True and parsed_ver['version_suffix'] == None:
            return {
                'version_id': version_id,
                'version_label': version_label
            }
    return {
        'version_id': None,
        'version_label': None
    }

def check_schema_differences(pending_model_version_id, pending_model_version_label, previous_model_version_id, previous_model_version_label, model_versions_preprod):
    schema_difference_previous = False
    schema_difference_preprod = False
    breaking_changes = False
    breaking_changes_desc = None
    preprod_in_sync  = False

    print(f"-- Checking for breaking changes - model version {pending_model_version_id}_{str(pending_model_version_label)} --")

    # Keys to keep and compare
    keys_to_keep = ['type', 'children']

    # Get pending Prod
    schema_pending = get_data_schema(source_files_prod, pending_model_version_id, pending_model_version_label, keys_to_keep)

    # Get previous schema Prod
    if previous_model_version_id is not None:
        print(f"Previous Prod model version - {previous_model_version_id}_{str(previous_model_version_label)}")
        schema_previous = get_data_schema(source_files_prod, previous_model_version_id, previous_model_version_label, keys_to_keep)
    else:
        print(f"Previous model version does not exist in Prod")
        schema_difference_previous = True

    # Get PreProd schema
    preprod_model_version_id = 0
    preprod_model_version_label = pending_model_version_label
    preprod_model_version = get_model_version_from_label(model_versions_preprod, preprod_model_version_label)
    if preprod_model_version is not None:
        preprod_model_version_id = preprod_model_version["id"]
    if does_data_schema_exist(source_files_preprod, preprod_model_version_id, preprod_model_version_label):
        #print(f"Pre-prod model version - {preprod_model_version_id}_{str(preprod_model_version_label)}")
        print(f"Tst model version - {preprod_model_version_id}_{str(preprod_model_version_label)}")
        schema_preprod = get_data_schema(source_files_preprod, preprod_model_version_id, preprod_model_version_label, keys_to_keep)
    else:
        #print(f"Model version does not exist in Pre-Prod - {str(pending_model_version_label)}")
        print(f"Model version does not exist in Tst - {str(pending_model_version_label)}")
        schema_difference_preprod = True

    # Compare to previous schema
    if not schema_difference_previous:
        if schema_pending != schema_previous:
            schema_difference_previous = True
    
    # Compare to PreProd schema
    if not schema_difference_preprod:
        if schema_pending != schema_preprod:
            schema_difference_preprod = True

    # Errors
    if schema_difference_previous and schema_difference_preprod:
        print(f"-- Breaking changes found - model version {pending_model_version_id}_{str(pending_model_version_label)} --")
        breaking_changes = True
        if previous_model_version_id is not None:
            breaking_changes_desc = DeepDiff(schema_previous, schema_pending).to_json()
        else:
            #breaking_changes_desc = f"-- Previous model version does not exist in Prod and model version does not exist in Pre-Prod - model version {pending_model_version_id}_{str(pending_model_version_label)} --"
            breaking_changes_desc = f"-- Previous model version does not exist in Prod and model version does not exist in Tst - model version {pending_model_version_id}_{str(pending_model_version_label)} --"

    elif schema_difference_previous:
        #print(f"-- Breaking changes found but PreProd in sync - model version {pending_model_version_id}_{str(pending_model_version_label)} --")
        print(f"-- Breaking changes found but Tst in sync - model version {pending_model_version_id}_{str(pending_model_version_label)} --")
        breaking_changes = True
        preprod_in_sync = True
        if previous_model_version_id is not None:
            breaking_changes_desc = DeepDiff(schema_previous, schema_pending).to_json()
    else:
        print(f"-- No breaking changes found - model version {pending_model_version_id}_{str(pending_model_version_label)} --")

    return breaking_changes, breaking_changes_desc, preprod_in_sync

def does_data_schema_exist(path, model_version_id, model_version_label):
    module_path = f"{path}/{model_version_id}_{str(model_version_label)}/data_schema/data_schema_static.py"
    if os.path.exists(module_path):
        return True
    else:
        return False
    
def get_data_schema(path, model_version_id, model_version_label, keys_to_keep):
    module_name = "data_schema_static"
    module_path = f"{path}/{model_version_id}_{str(model_version_label)}/data_schema/data_schema_static.py"
    remove_string = """raise Exception(\"""This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your Data Schema that will allow easier debugging.
\""")"""

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        raise ImportError(f"Could not load spec for module '{module_name}' at: {module_path}")
    source = spec.loader.get_source(module_name)
    new_source = source.replace(remove_string, "")
    module = importlib.util.module_from_spec(spec)
    codeobj = compile(new_source, module.__spec__.origin, 'exec')
    exec(codeobj, module.__dict__)
    sys.modules[module_name] = module
    sch = None
    if hasattr(module, 'hx_calculation_legacy_initial_premium'):
        sch = module.hx_calculation_legacy_initial_premium()
    else:
        sch = module.data_schema()
    d = json.loads(json.dumps(sch, indent=4, cls=HxSchemaEncoder))
    select_keys_from_dict(d, keys_to_keep)
    return d

class HxSchemaEncoder(JSONEncoder):
        def default(self, o):
            return dict((name, getattr(o, name)) for name in dir(o) if not getattr(o, name) == hx.UNDEFINED)

def select_keys_from_dict(dictionary, lst_keys):
    for k, v in list(dictionary.items()):
        is_dict = isinstance(v, dict)
        is_node = False
        if is_dict:
            is_node = v.get('type') in ['structure', 'list', 'file', 'triangle', 'int', 'float', 'str', 'bool', 'date']
        if k not in lst_keys and not is_node:
            try:
                del dictionary[k]
            except KeyError:
                pass
        if is_dict:
            select_keys_from_dict(v, lst_keys)

# # We must re-download the source files due to sparse checkout 
# def persist_model_version_old(model_version, required_published_model_versions):
#     model_version_id = model_version["id"]
#     model_version_label = model_version["label"]
#     source_dir =  f"{source_files_prod}/{model_version_id}_{str(model_version_label)}"
#     destination_dir =  f"{output_folder}/{model_version_id}_{str(model_version_label)}"
#     shutil.copytree(source_dir, destination_dir)
#     required_published_model_versions.append({ "id": model_version_id, "label": model_version_label })

def persist_model_version(model_version, required_published_model_versions):
    model_version_id = model_version["id"]
    model_version_label = model_version["label"]
    print(f"Getting model version {model_version_id}")
    source_files_url = f"{hx_base_url}/model-versions/{model_version_id}/source-files"
    source_files_stream = api_request_retry("get", source_files_url, headers=hx_headers, stream=True)
    if source_files_stream.status_code != 200:
        raise Exception(f"Failed to get source files")
    source_files_zip = zipfile.ZipFile(BytesIO(source_files_stream.content))
    destination_dir =  f"{output_folder}/{model_version_id}_{str(model_version_label)}"
    source_files_zip.extractall(destination_dir)
    shutil.rmtree(f"{destination_dir}/libraries", ignore_errors=True)
    required_published_model_versions.append({ "id": model_version_id, "label": model_version_label })

def create_metadata(required_published_model_versions):
    json_dat = {
        "last_updated": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        "published_model_versions": required_published_model_versions
    }
    filepath = os.path.join(output_folder, 'metadata.json')
    with open(filepath, 'w') as file:
        json.dump(json_dat, file)
    
if __name__ == "__main__":
    main()