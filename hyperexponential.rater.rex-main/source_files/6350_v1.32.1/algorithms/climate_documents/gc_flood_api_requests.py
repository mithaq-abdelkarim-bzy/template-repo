
####
# This script sets out the functions required to connect to the Guy Carpenter AdvantagePoint HazardAPI for use in the Flood Climate Risk Scoring metric. 
# This includes (Re)authenication, API calls and data processing. 

# Import Libraries ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import requests
import warnings
import pandas
import time
import concurrent.futures
import pandas as pd
import numpy as np
from threading import Thread
from threading import current_thread
from threading import Lock
import os
import datetime
import hx

warnings.filterwarnings("ignore")

# Parameters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
retries = 3
overall_retries = 1
workers = 16
stop_threads = False
gc_token_expiry = datetime.datetime.now()
gc_headers = ""

base_url = f"https://analyticsservices.guycarp.com/rest/uw/v3/"
scope = "UWHazardAPI"

# Helper Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def api_request_retry(method, url, headers, json=None, stream=None):
    for i in range(retries):
        try:
            if method == "get":
                result = requests.get(url, headers=headers, verify=False, stream=stream)
            else:
                result = requests.post(url, headers=headers, json=json, verify=False)
            if result.status_code==200:
                if "error" not in result.json():
                    return(result)
                if result.json()["error"]==None:
                    return(result)
            print(f'{current_thread().name} - API call failed ({url}) - Attempt {i+1}: {result.json()["error"]["title"]}')
            time.sleep(5)
        except Exception as e:
            print(f'{current_thread().name} - API call failed ({url}) - Attempt {i+1}: {str(e)}')
            time.sleep(5)
    print(result.json())
    return result

def detect_api_failure(result_json, step_desc):
    try: 
        if result_json.status_code != 200:
            if 'message' in result_json.json():
                print(f'{current_thread().name} - API failed: {result_json.json()["message"]}')
                return {'status' : "failed", "error_step": step_desc, "error_message": result_json.status_code, "error_detail": result_json.json()["message"]}
            else:
                print(f'{current_thread().name} - API failed: {result_json.status_code}')
                return {'status' : "failed", "error_step": step_desc, "error_message": result_json.status_code, "error_detail": ""}
    except KeyError:
            print(f'{current_thread().name} - API failed: {result_json.status_code}')
            return {'status' : "failed", "error_step": step_desc, "error_message": result_json.status_code, "error_detail": ""}
    return None

def gc_authentication():

    global gc_headers
    global gc_token_expiry

    client_id = hx.secrets.guycarp_client_id
    client_secret = hx.secrets.guycarp_client_secret
    username = hx.secrets.guycarp_user_name
    password = hx.secrets.guycarp_user_password



    now = datetime.datetime.now()

    url = "https://analyticsservices.guycarp.com/oauth/token"

    payload = {
        "client_id": client_id,
        "scope": scope,
        "client_secret": client_secret,
        "grant_type": "password",
        "username": username,
        "password": password
    }
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'fpc=AsoJa2IkxjVDg4osC0s944in7HQ7AgAAAJwtR9wOAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
    }
    for i in range(3): 
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            break
        except Exception as e:
            time.sleep(1)
    
    gc_token_expiry = now + datetime.timedelta(0, response.json()["expires_in"] - 60)
    auth_token_formatted = f"Bearer {response.json()['access_token']}"
    gc_headers = {"Connection": "close", "Authorization": auth_token_formatted, 'content-type': 'application/json'}

def refresh_access_token():
    global gc_token_expiry
    while True:
        if stop_threads:
            break
        now = datetime.datetime.now()
        if now > gc_token_expiry:
            print(f'{current_thread().name} - Refreshing access token')
            lock = Lock()
            with lock:
                gc_authentication()
        time.sleep(10)

def gc_api_calls(output, loc_id):

    global gc_headers

    # Set URLs
    location_hazard_info_url = f"{base_url}/hazard/api/LocationHazardInfo"

    # Define JSON structure 
    input_json = {
        "Latitude": output["latitude"].iloc[0],
        "Longitude": output["longitude"].iloc[0],
        "CountryCode": output["country"].iloc[0],
        "HazardLayers": [
            {"LayerId": "1074"},
            {"LayerId": "1076"},
            {"LayerId": "1079"},
            {"LayerId": "1327"},
            {"LayerId": "1330"},
            {"LayerId": "1332"}
        ],
        "Distances": [
            {
                "Value": 1,
                "Unit": "miles"
            }
        ]
    }

    # Post
    location_hazard_info = api_request_retry("post", location_hazard_info_url, headers = gc_headers, json = input_json)
    failure = detect_api_failure(location_hazard_info, "location_hazard_info")
    if failure != None:
            print(f"{current_thread().name} - gc_api_calls {loc_id} failed: {failure['error_message']}")
            return failure

    # Navigate to the list of HazardLayers
    hazard_layers = location_hazard_info.json()["ReturnValues"]["HazardInfos"][0]["HazardLayers"]

    # Add each value to a column for the single row of data
    for i, layer in enumerate(hazard_layers):
        # convert str data to int or return 0s for missing data. 
        if layer['Label']:
            try:
                result = int(float(layer['Label']))
            except Exception as er:
                result = 0
        else:
            result = 0
        output[f"label_{i+1}"] = result

    # Return successful response
    return {'status' : "succeeded", "error_step" : "", "error_message" : "", "error_detail" : ""}

def process_location(input, delay):
    row = input.iloc[0]
    output = input.copy()
   
    if delay > 0:
        print(f"{current_thread().name} - Sleeping for {delay} seconds")
        time.sleep(delay)
    
    policy_start = time.time()

    print(f'{current_thread().name} - loc_id {row["loc_id"]}')

    try:
        result = gc_api_calls(output, loc_id = row["loc_id"])

        policy_end = time.time()

        # Write result back to the output scheme
        # output["status"] = result["status"]
        output["status"] = result["error_message"]
        output["error_step"] = result["error_step"]
        output["error_message"] = result["error_message"]
        output["error_detail"] = result["error_detail"]
        output["time_taken"] = policy_end - policy_start
        output["time"] = datetime.datetime.now()
        return output
        
    except Exception as e:
        output["status"] = str(e)
        output["error_step"] = ""
        output["error_message"] = str(e)
        output["error_detail"] = ""
        output["time"] = datetime.datetime.now()
        print(f"{current_thread().name} - gc_api_calls {row['loc_id']} failed: {str(e)}")
        return output

def main(data, workers):

    global stop_threads

    # Create initial access token and start thread to refresh token as needed
    gc_authentication()
    refresh_token_thread = Thread(target = refresh_access_token)
    refresh_token_thread.start()

    # Start thread pool
    for i in range(overall_retries):
        data = [data.iloc[[i]] for i in range(data.shape[0])]
        delay = [x * 0.5 if x < workers else 0 for x in range(len(data))]
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            data = pandas.concat(executor.map(process_location, data, delay))

    stop_threads = True

    return data


