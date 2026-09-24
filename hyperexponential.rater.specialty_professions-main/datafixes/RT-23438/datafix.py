#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#
#' 
#' JIRA: RT-23438
#' Author: Mark Fleet
#' Date: 16/12/2025
#' Description: Upgrade Model Version
#' 
#'
#' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '#

# Import Libraries ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import requests
import warnings
import pandas
import time
import concurrent.futures
from queue import Queue
from threading import Thread
from threading import current_thread
import os
import datetime

warnings.filterwarnings("ignore")

# Import local modules
from config import Config
config = Config()

# Queues
queue_msg = Queue()
queue_progress = Queue()

# Helper Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def logger_msg(queue_msg, log_file):
    while True:
        message=queue_msg.get()
        print(message)
        pandas.DataFrame([{"Message": message, "Time": datetime.datetime.now()}]).to_csv(log_file, mode='a', header=not os.path.exists(log_file))
        queue_msg.task_done()

def logger_progress(queue_progress, progress_file):
    while True:
        progress=pandas.DataFrame(queue_progress.get())
        progress.to_csv(progress_file, mode='a', header=not os.path.exists(progress_file), index=False)
        queue_progress.task_done()

def log_msg(message):
    queue_msg.put(message)

def log_progress(progress):
    queue_progress.put(progress)

def api_request_retry(method, url, headers, json=None, stream=None):
    for i in range(config.retries):
        try:
            if method == "get":
                result = requests.get(url, headers=headers, verify=False, stream=stream)
            elif method == "patch":
                result = requests.patch(url, headers=headers, json=json, verify=False)
            else:
                result = requests.post(url, headers=headers, json=json, verify=False)
            if result.status_code==200:
                if "error" not in result.json():
                    return(result)
                if result.json()["error"]==None:
                    return(result)
            log_msg(f'{current_thread().name} - API call failed ({url}) - Attempt {i+1}: {result.json()["error"]["title"]}')
            time.sleep(5)
        except Exception as e:
            log_msg(f'{current_thread().name} - API call failed ({url}) - Attempt {i+1}: {str(e)}')
            time.sleep(5)
    return result

def detect_api_failure(result_json, step_desc):
    try: 
        if 'error' in result_json.json() and result_json.json()["error"] != None:
            log_msg(f'{current_thread().name} - Datafix failed: {result_json.json()["error"]["title"]}')
            return {'status' : "failed", "error_step": step_desc, "error_message": result_json.json()["error"]["title"], "error_detail": result_json.json()["error"]["detail"], "policy_id_new" : ""}
        if result_json.status_code != 200:
            if 'title' in result_json.json():
                log_msg(f'{current_thread().name} - Datafix failed: {result_json.json()["title"]}')
                return {'status' : "failed", "error_step": step_desc, "error_message": result_json.status_code, "error_detail": result_json.json()["title"], "policy_id_new" : ""}
            else:
                log_msg(f'{current_thread().name} - Datafix failed: {result_json.status_code}')
                return {'status' : "failed", "error_step": step_desc, "error_message": result_json.status_code, "error_detail": "", "policy_id_new" : ""}
    except KeyError:
            log_msg(f'{current_thread().name} - Datafix failed: {result_json.json()["title"]}')
            return {'status' : "failed", "error_step": step_desc, "error_message": result_json.json()["title"], "error_detail": "", "policy_id_new" : ""}
    return None

def azure_authentication():

    url = f"https://login.microsoftonline.com/{config.tenant_id}/oauth2/v2.0/token"

    if config.secret_value is not None:
        client_secret = config.secret_value
    else:
        client_secret = os.environ.get(config.secret_env_var)

    payload = {
        "Client_id": config.client_id,
        "Scope": config.scope,
        "Client_secret": client_secret,
        "Grant_type": "client_credentials"
    }
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'fpc=AsoJa2IkxjVDg4osC0s944in7HQ7AgAAAJwtR9wOAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()["access_token"]

def pad_list(source_list, target_len, default_element):
    target_list = source_list[:target_len] + [default_element]*(target_len - len(source_list))
    return target_list


# Datafix Function ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def datafix(output):

    row = output.iloc[0]

    # Values
    policy_id = row["policy_id"]
    model_version_id = row["model_version_id"]

    log_msg(f"{current_thread().name} - Started datafixing PolicyID {policy_id}")

    # Auth
    for i in range(3): 
        try:       
            bearer_token = azure_authentication()
            break
        except Exception as e:
            time.sleep(1)
    auth_token_formatted = f"Bearer {bearer_token}"
    headers_policy = {"Connection": "close", "Authorization": auth_token_formatted, 'content-type': 'application/json'}

    # Write datafix progress out to progress tracker
    output["status"] = "started"
    output["time"] = datetime.datetime.now()
    log_progress(output)

    # Set URLs
    update_model_version_url = f"{config.base_url}policies/{policy_id}/update-model-version"

    # Set data
    json_dat = {
    "model_version_id" : int(model_version_id),
    "archive_original" : True
    }

    # Post
    update_model_version = api_request_retry("post", update_model_version_url, headers = headers_policy, json = json_dat)
    failure = detect_api_failure(update_model_version, "update model version")
    if failure != None:
            log_msg(f"{current_thread().name} - Datafix {policy_id} failed: {failure['error_message']}")
            return failure
    policy_id_new = update_model_version.json()["id"]

    # Return successful response
    log_msg(f"{current_thread().name} - Finished datafixing PolicyID {policy_id}")
    return {'status' : "succeeded", "error_step" : "", "error_message" : "", "error_detail" : "", "policy_id_new" : policy_id_new}


def process_policy(input, delay):
    row = input.iloc[0]
    output = input.copy()

    # Skip policy if not migrating it or it has already succeeded
    if row["datafix"] == "no" or row["status"] == "succeeded":
        return output
    
    if delay > 0:
        log_msg(f"{current_thread().name} - Sleeping for {delay} seconds")
        time.sleep(delay)
    
    policy_start = time.time()

    try:
        result = datafix(output)

        policy_end = time.time()

        # Write migration result back to the migration scheme
        output["status"] = result["status"]
        output["error_step"] = result["error_step"]
        output["error_message"] = result["error_message"]
        output["error_detail"] = result["error_detail"]
        output["time_taken"] = policy_end - policy_start
        output["time"] = datetime.datetime.now()
        output["policy_id_new"] = result["policy_id_new"]
        log_progress(output)
        return output
        
    except Exception as e:
        output["status"] = "failed"
        output["error_step"] = ""
        output["error_message"] = str(e)
        output["error_detail"] = ""
        output["time"] = datetime.datetime.now()
        output["policy_id_new"] = ""
        log_progress(output)
        log_msg(f"{current_thread().name} - Datafix {row["policy_id"]} failed: {str(e)}")
        return output


def main(output_path, workers, progress_file, log_file):

    input_scheme = pandas.read_csv(config.input_file)
    
    start = time.time()

    # Set up message logging
    msg_logger = Thread(target=logger_msg, args=(queue_msg, log_file), daemon=True)
    progress_logger = Thread(target=logger_progress, args=(queue_progress, progress_file), daemon=True)

    msg_logger.start()
    progress_logger.start()

    for i in range(config.overall_retries):
        input_scheme = [input_scheme.iloc[[i]] for i in range(input_scheme.shape[0])]
        delay = [x * 2 if x < workers else 0 for x in range(len(input_scheme))]
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            input_scheme = pandas.concat(executor.map(process_policy, input_scheme, delay))

    input_scheme.to_csv(output_path)
            
    end = time.time()

    queue_msg.join()
    queue_progress.join()

    return(end - start)


def run_datafix(workers):
    output_dir = config.output_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, f"Output.csv")
    progress_path = os.path.join(output_dir, f"Progress.csv")
    log_path = os.path.join(output_dir, f"Log.csv")
    perf_time = main(output_path, workers, progress_path, log_path)
    perf_time = {"workers": workers, "time": perf_time}
    print(f"Completed {workers} workers")

# Start datafix
run_datafix(config.workers)