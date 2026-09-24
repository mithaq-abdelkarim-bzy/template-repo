#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#
#' 
#' Progam Name: Model movement checks
#' Author: Mark Fleet
#' Date: 12/02/2025
#' Description: Compares source files between environments and determines if any model movement is required
#' 
#'
#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#

# Import Libraries ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from api_requests import api_request_retry
from hx_misc import read_model_versions_json, get_model_version_from_label, get_model_version_folder, get_latest_model_version
from github_misc import set_output
import hx_data_schema as hx
import os
from packaging.version import Version
import json

# Parameters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
environment = os.environ.get("ENVIRONMENT")
model_id = os.environ.get("HX_MODEL_ID")
output_folder = os.environ.get("OUTPUT_FOLDER")
source_files_dev = "source_files_dev"
source_files_tst = "source_files_tst"
source_files_preprod = "source_files_preprod"
source_files_prod = "source_files_prod"
model_versions_json = "model_versions.json"

def main():

    checks_complete = False

    # Dev checks
    if environment == "DEV":

        model_versions_dev = read_model_versions_json(folder = source_files_dev, testable = True, valid_labels_only = True, sort_descending = True)
        model_versions_tst = read_model_versions_json(folder = source_files_tst, valid_labels_only = True, sort_descending = True)
        #model_versions_preprod = read_model_versions_json(source_files_preprod, True)
        model_movement_dev_req = False
        model_movement_dev_model_is_live = False
        model_movement_dev_model_version_id = 0
        model_movement_dev_model_version_label = ""
        model_movement_dev_model_version_developer = ""
        model_movement_dev_model_version_description = ""
        model_movement_dev_dest_branch = ""
        model_movement_dev_python_package_changes = ""
        model_movement_dev_user_library_changes = ""

        # Check the latest model version
        v = model_versions_dev[0]
        model_movement_dev_model_name = model_versions_dev[0]["model"]["name"]
        model_version_id = v["id"]
        model_version_label = v["label"]
        model_version_testable = v["testable"]
        model_version_developer = v["created_by_user"]["email"]
        model_version_description = v["description"]
        model_version_parsed_label_dev = v["parsed_label"]

        # Determine if model is live based on major version
        model_is_live = int(model_version_parsed_label_dev['version_major']) > 0

        # # Check if label also in TST and PREPROD
        # tst_model_version = get_model_version_from_label(model_versions_tst, model_version_label)
        # preprod_model_version = get_model_version_from_label(model_versions_preprod, model_version_label)

        # if tst_model_version is None or preprod_model_version is None:
        #     print(f"Version {model_version_label} needs to be deployed to TST/PREPROD")
        #     model_movement_dev_req = True
        #     model_movement_dev_model_is_live = model_is_live
        #     model_movement_dev_model_version_id = model_version_id
        #     model_movement_dev_model_version_label = model_version_label
        #     model_movement_dev_model_version_developer = model_version_developer
        #     model_movement_dev_model_version_description = model_version_description
        #     model_movement_dev_dest_branch = "MAIN"
        #     break

        # Check if label also in TST
        tst_model_version = get_model_version_from_label(model_versions_tst, model_version_label)

        if tst_model_version is None:
            print(f"Version {model_version_label} needs to be deployed to TST")
            model_movement_dev_req = True
            model_movement_dev_model_is_live = model_is_live
            model_movement_dev_model_version_id = model_version_id
            model_movement_dev_model_version_label = model_version_label
            model_movement_dev_model_version_developer = model_version_developer
            model_movement_dev_model_version_description = model_version_description
            model_movement_dev_dest_branch = "MAIN"

            # Package checks
            model_version_folder_dev = get_model_version_folder(source_files_dev, model_version_id)
            model_version_id_tst, model_version_label_tst = get_latest_model_version(model_versions=model_versions_tst, valid_labels_only=True)
            model_version_folder_tst = get_model_version_folder(source_files_tst, model_version_id_tst)
            model_movement_dev_python_package_changes, model_movement_dev_user_library_changes = compare_package_and_library_dependencies(model_version_folder_tst, model_version_folder_dev, "tst", "dev")

            checks_complete = True

        set_output('model_movement_dev_req', model_movement_dev_req)
        set_output('model_movement_dev_model_name', model_movement_dev_model_name)
        set_output('model_movement_dev_model_is_live', model_movement_dev_model_is_live)
        set_output('model_movement_dev_model_version_id', model_movement_dev_model_version_id)
        set_output('model_movement_dev_model_version_label', model_movement_dev_model_version_label)
        set_output('model_movement_dev_model_version_developer', model_movement_dev_model_version_developer)
        set_output('model_movement_dev_model_version_description', model_movement_dev_model_version_description)
        set_output('model_movement_dev_dest_branch', model_movement_dev_dest_branch)
        set_output('model_movement_dev_python_package_changes', model_movement_dev_python_package_changes)
        set_output('model_movement_dev_user_library_changes', model_movement_dev_user_library_changes)

    # Prod checks
    if environment == "PROD":
        model_versions_dev = read_model_versions_json(folder = source_files_dev, valid_labels_only = True, sort_descending = True)
        model_versions_prod = read_model_versions_json(folder = source_files_prod, valid_labels_only = True, published = True, sort_descending = True)
        model_movement_prod_req = False
        model_movement_prod_model_is_live = False
        model_movement_prod_model_version_id = 0
        model_movement_prod_model_version_label = ""
        model_movement_prod_model_version_developer = ""   
        model_movement_prod_model_version_description = ""     
        model_movement_prod_dest_branch = "" 
        model_movement_prod_python_package_changes = ""
        model_movement_prod_user_library_changes = ""

        # Check the latest model version
        v = model_versions_prod[0]
        model_movement_prod_model_name = model_versions_prod[0]["model"]["name"]
        model_version_id = v["id"]
        model_version_label = v["label"]
        model_version_developer = v["created_by_user"]["email"]
        model_version_description = v["description"]
        model_version_parsed_label_prod = v["parsed_label"]

        # Determine if model is live based on major version
        model_is_live = int(model_version_parsed_label_prod['version_major']) > 0

        # Check if PROD label also in DEV - If the model version labelled is the same as the model version in the MAIN branch on DEV then it would mean that the model has just been moved up from DEV → TST → PREPROD → PROD and will therefore not trigger any model movement down.
        dev_model_version = get_model_version_from_label(model_versions_dev, model_version_label)
        if dev_model_version:
            checks_complete = True 

        # Check if no versions already in DEV
        if not checks_complete:
            if not model_versions_dev:
                #print(f"Version {model_version_label} needs to be deployed to DEV/TST/PREPROD - MAIN branch")
                print(f"Version {model_version_label} needs to be deployed to DEV/TST - MAIN branch")
                model_movement_prod_req = True
                model_movement_prod_model_is_live = model_is_live
                model_movement_prod_model_version_id = model_version_id
                model_movement_prod_model_version_label = model_version_label
                model_movement_prod_model_version_developer = model_version_developer
                model_movement_prod_model_version_description = model_version_description
                model_movement_prod_dest_branch = "MAIN"
                checks_complete = True 

        # Compare to latest version in DEV
        if not checks_complete:
            dev_model_version = model_versions_dev[0]
            model_version_parsed_label_dev = dev_model_version["parsed_label"]

            # Check if the PROD label version is higher than the current label version in DEV - the model version is moved directly into the MAIN branch on DEV and the model version will automatically contain the same release note and be labelled and marked for testing. 
            if Version(model_version_parsed_label_prod['version_number_as_string']) > Version(model_version_parsed_label_dev['version_number_as_string']):
                #print(f"Version {model_version_label} needs to be deployed to DEV/TST/PREPROD - MAIN branch")
                print(f"Version {model_version_label} needs to be deployed to DEV/TST - MAIN branch")
                model_movement_prod_req = True
                model_movement_prod_model_is_live = model_is_live
                model_movement_prod_model_version_id = model_version_id
                model_movement_prod_model_version_label = model_version_label
                model_movement_prod_model_version_developer = model_version_developer
                model_movement_prod_model_version_description = model_version_description
                model_movement_prod_dest_branch = "MAIN"

                # Package checks
                model_version_folder_prod = get_model_version_folder(source_files_prod, model_version_id)
                model_version_id_dev, model_version_label_dev = get_latest_model_version(model_versions=model_versions_dev, valid_labels_only=True)
                model_version_folder_dev = get_model_version_folder(source_files_dev, model_version_id_dev)
                model_movement_prod_python_package_changes, model_movement_prod_user_library_changes = compare_package_and_library_dependencies(model_version_folder_dev, model_version_folder_prod, "dev", "prod")

                checks_complete = True

            else: # the model version is moved into the MAIN (PROD) branch on DEV. The model will contain the same release note and label and be marked for testing.
                print(f"Version {model_version_label} needs to be deployed to DEV - MAIN (PROD) branch")
                model_movement_prod_req = True
                model_movement_prod_model_is_live = model_is_live
                model_movement_prod_model_version_id = model_version_id
                model_movement_prod_model_version_label = model_version_label
                model_movement_prod_model_version_developer = model_version_developer
                model_movement_prod_model_version_description = model_version_description
                model_movement_prod_dest_branch = "MAIN (PROD)"

                # Package checks
                model_version_folder_prod = get_model_version_folder(source_files_prod, model_version_id)
                model_version_id_dev, model_version_label_dev = get_latest_model_version(model_versions=model_versions_dev, valid_labels_only=True)
                model_version_folder_dev = get_model_version_folder(source_files_dev, model_version_id_dev)
                model_movement_prod_python_package_changes, model_movement_prod_user_library_changes = compare_package_and_library_dependencies(model_version_folder_dev, model_version_folder_prod, "dev", "prod")

                checks_complete = True

        set_output('model_movement_prod_req', model_movement_prod_req)
        set_output('model_movement_prod_model_name', model_movement_prod_model_name)
        set_output('model_movement_prod_model_is_live', model_movement_prod_model_is_live)
        set_output('model_movement_prod_model_version_id', model_movement_prod_model_version_id)
        set_output('model_movement_prod_model_version_label', model_movement_prod_model_version_label)
        set_output('model_movement_prod_model_version_developer', model_movement_prod_model_version_developer)
        set_output('model_movement_prod_model_version_description', model_movement_prod_model_version_description)
        set_output('model_movement_prod_dest_branch', model_movement_prod_dest_branch)
        set_output('model_movement_prod_python_package_changes', model_movement_prod_python_package_changes)
        set_output('model_movement_prod_user_library_changes', model_movement_prod_user_library_changes)

def compare_package_and_library_dependencies(model_version_folder_1, model_version_folder_2, env_1, env_2):

    # Set version env keys
    version_key_1 = f"version_{env_1}"
    version_key_2 = f"version_{env_2}"

    # Read metadata
    if model_version_folder_1 != None:
        metadata_path_1 = os.path.join(model_version_folder_1, "metadata.json")
        with open(metadata_path_1, 'r') as file:
                data = file.read()
        metadata_1 = json.loads(data)
    else:
         metadata_1 = {
              "user_library_dependencies": [],
              "direct_python_package_dependencies": [],
              "resolved_python_package_versions": [],
         }
    metadata_path_2 = os.path.join(model_version_folder_2, "metadata.json")
    with open(metadata_path_2, 'r') as file:
            data = file.read()
    metadata_2 = json.loads(data)

    # User library checks
    user_library_changes = []
    for user_library_dependency in metadata_2['user_library_dependencies']:
         match = [d for d in metadata_1['user_library_dependencies'] if d['package_name'] == user_library_dependency['package_name']]
         if len(match) == 0:
            user_library_change = {}
            user_library_change['package_name'] = user_library_dependency['package_name']
            user_library_change[version_key_1] = "N/A"
            user_library_change[version_key_2] = user_library_dependency.get('label', f"Unknown {env_2}")
            user_library_changes.append(user_library_change)
         elif user_library_dependency.get('label', f"Unknown {env_2}") != match[0].get('label', f"Unknown {env_1}"):
            user_library_change = {}
            user_library_change['package_name'] = user_library_dependency['package_name']
            user_library_change[version_key_1] = match[0].get('label', f"Unknown {env_1}")
            user_library_change[version_key_2] = user_library_dependency.get('label', f"Unknown {env_2}")
            user_library_changes.append(user_library_change)

    # Python package checks
    python_package_changes = []
    for python_package_dependency in metadata_2['direct_python_package_dependencies']:
         match = [d for d in metadata_1['direct_python_package_dependencies'] if d['package_name'] == python_package_dependency['package_name']]
         if len(match) == 0:
            python_package_change = {}
            python_package_change['package_name'] = python_package_dependency['package_name']
            python_package_change[version_key_1] = "N/A"
            python_package_change[version_key_2] = python_package_dependency['package_specifier']
            python_package_changes.append(python_package_change)
         elif python_package_dependency['package_specifier'] != match[0]['package_specifier']:
            python_package_change = {}
            python_package_change['package_name'] = python_package_dependency['package_name']
            python_package_change[version_key_1] = match[0]['package_specifier']
            python_package_change[version_key_2] = python_package_dependency['package_specifier']
            python_package_changes.append(python_package_change)

    python_package_changes = json.dumps(python_package_changes, indent=4)
    user_library_changes = json.dumps(user_library_changes, indent=4)

    return python_package_changes, user_library_changes

if __name__ == "__main__":
    main()