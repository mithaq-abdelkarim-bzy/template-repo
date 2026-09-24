import requests
import json
import warnings
import logging as log
log.basicConfig(format='%(asctime)s %(message)s')
warnings.filterwarnings("ignore")
import os
# Import helper function
from algorithms.generate_example_data import create_example_data

def azure_authentication():

    url = "https://login.microsoftonline.com/9a50eba8-7568-447a-bcb9-27a0d464aa80/oauth2/v2.0/token"
    
    payload = 'Client_id=0e70ff59-43b4-471b-a140-a55a8473178d&Scope=api%3A%2F%2Fapi.beazley.hxrenew.com%2F.default&Client_secret=+hx.secrets.v2_rest_api_client_secret+&Grant_type=client_credentials'    

    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'fpc=AsoJa2IkxjVDg4osC0s944in7HQ7AgAAAJwtR9wOAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()["access_token"]

def get_snapshot(policy_option_id):

    auth_token_formatted = f"Bearer {azure_authentication()}"

    headers = {"Connection": "close", "Authorization": auth_token_formatted, 'content-type': 'application/json'}

    resp = requests.get(f"https://api.beazley.hxrenew.com/api/v2-beta/policy-options/{policy_option_id}/snapshot", headers=headers, verify=False)

    if resp.status_code == 200:
        log.warning(f"Snapshot extract successful for Policy Option ID {policy_option_id}")
        return resp.json()
    else:
        log.warning(f"Snapshot extract failed for Policy Option ID {policy_option_id}")
        #log.warning(get_str(resp.content))
        return resp.json()

def pull_snapshot(policy_option_id, output_path):

    snapshot_json = get_snapshot(policy_option_id)

    snapshot_json = snapshot_json['data']

    snapshot_json = [snapshot_json]
    #     # Provide a folder location that the file will be exported to
    # output_folder = "editing/test_cases/"
    # output_file = os.path.join(output_folder, f"snapshot_{policy_option_id}.json")

    # with open(output_path, "w") as f:
    #     json.dump(snapshot_json, f)
    output_file = os.path.join(output_path, "full_snapshot.json")
    with open(output_file, "w") as file:
        json.dump(snapshot_json, file, indent=4)

def get_inputs_from_snapshots():
    
    # Get input file path
    file = "editing/test_cases/full_snapshot.json"
        
    with open(file, "r") as input_file:
        # Process input snapshot through helper function
        policy_json = json.load(input_file)[0]
        snapshot_inputs = create_example_data(policy_json)

        # Export to output file
        with open ("editing/test_cases/output_snapshot.json", "w+") as output_file:
            json.dump(snapshot_inputs, output_file, indent=2)




# Call function
pull_snapshot(109687, "editing/test_cases/")
get_inputs_from_snapshots()




# def get_inputs_from_snapshots():
    
#     # Get input file path
#     file = "editing/test_cases/full_snapshot.json"
        
#     with open(file, "r") as input_file:
#         # Process input snapshot through helper function
#         policy_json = json.load(input_file)
#         snapshot_inputs = create_example_data(policy_json)

#         # Export to output file
#         with open ("editing/test_cases/output_snapshot.json", "w+") as output_file:
#             json.dump(snapshot_inputs, output_file, indent=2)

# get_inputs_from_snapshots()

