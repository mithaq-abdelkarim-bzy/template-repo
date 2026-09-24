#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#
#' 
#' Progam Name: Api Requests
#' Author: Mark Fleet
#' Date: 16/08/2024
#' Description: Handles all Api requests with retry functionality
#' 
#'
#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#

# Import Libraries ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import requests
import warnings
import time

# Parameters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
retries = 3 # How many times to retry the APIs after failure

warnings.filterwarnings("ignore")

def api_request_retry(method, url, headers, json=None, stream=None):
    for i in range(retries):
        try:
            if method == "get":
                result = requests.get(url, headers=headers, verify=False, stream=stream)
            else:
                result = requests.post(url, headers=headers, json=json, verify=False)
            if result.status_code>=200 and result.status_code<=299:
                return(result)
            print(f'API call failed ({url}) - Attempt {i+1}: {result.json()}')
            time.sleep(5)
        except Exception as e:
            print(f'API call failed ({url}) - Attempt {i+1}: {str(e)}')
            time.sleep(5)
    return result