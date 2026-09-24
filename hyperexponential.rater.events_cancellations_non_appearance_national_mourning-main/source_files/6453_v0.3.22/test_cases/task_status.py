import requests
import time

base_url       = f"https://api.beazley-dev.hxrenew.com/api/v2-beta"
client_id      = ""
scope          = "api://api.beazley-dev.hxrenew.com/.default"
secret_env_var = "hx_client_secret_dev"

def get_values(base_url, policy_option_id, token, session_id):
    response = requests.post(   f"{base_url}/api/policy-option-instances/"
                                f"{policy_option_id}/get-values"
                              , headers  = {"Connection" : "close", "Authorization" : token, 'content-type': 'application/json', 'X-Hx-Session-Id' : session_id}
                              , json     = {"state": {"nodes": [""], "lists": {}}}    )
    response.raise_for_status()
    return response.json()

def start_task(base_url,policy_option_id, token, session_id,    task_name):
    response = requests.post(   f"{base_url}/api/policy-option-instances/"
                                f"{policy_option_id}/async-tasks/{task_name}/start"
                              , headers = {"Connection" : "close", "Authorization" : token, 'content-type': 'application/json', 'X-Hx-Session-Id' : session_id}
                              , json    = {"state": {"nodes": [""], "lists": {}}}    )
    response.raise_for_status()
    return response.json()

def wait_for_task(base_url, policy_option_id, token, session_id, task_name):
    start = time.time()

    while True:
        response = get_values(base_url, policy_option_id, token, session_id) 
        task = response["result"]["async_tasks"][task_name]
        if task["status"] == "FINISHED":
            return
        if task["status"] in {"ERROR", "CANCELLED"}:
            raise RuntimeError(task["status"])
        if time.time() - start > 600:
            raise TimeoutError(f"{task_name} did not finish in 10 minutes")
        print(  f"{task['status']} "
                f"({task['progress']:.0%})" )
        time.sleep(2)


# usage simple
response = get_values(base_url, policy_option_id, token, session_id) 
print(response["result"]["async_tasks"])
task = response["result"]["async_tasks"]["task_simulation"]
print(task["status"])
print(task["progress"])

# usage realistic
start_task(    base_url,    policy_option_id,    token,    session_id,    "sync_expiring_ids")
wait_for_task( base_url,    policy_option_id,    token,    session_id,    "sync_expiring_ids")

start_task(    base_url,    policy_option_id,    token,    session_id,    "task_fetch_ihs_data")
wait_for_task( base_url,    policy_option_id,    token,    session_id,    "task_fetch_ihs_data")

start_task(    base_url,    policy_option_id,    token,    session_id,    "task_simulation")
wait_for_task( base_url,    policy_option_id,    token,    session_id,    "task_simulation")

start_task(    base_url,    policy_option_id,    token,    session_id,    "policy_to_excel_task")
wait_for_task( base_url,    policy_option_id,    token,    session_id,    "policy_to_excel_task")
