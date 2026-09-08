import hx
import gc
from algorithms.aysnc_tasks.em_bi_sql.async_em_sql import search_exposure_management_data, pull_in_exposure_management_data, select_binders_for_em_pull, clear_binder_list
from algorithms.aysnc_tasks.aysnc_start_renewal import start_renewal, set_migration_flag
from algorithms.aysnc_tasks.em_bi_sql.async_bi_sql import bi_facility_fetch, bi_facility_include_all, bi_facility_exclude_all, bi_clm_and_mvmt_fetch
from algorithms.rating import run_bordereau_rater
from algorithms.aysnc_tasks.triangles.aysnc_tri_setup import tri_exclusions_setup, tri_override_setup
from algorithms.aysnc_tasks.profit_commission.async_simulate_profit_commission import simulate_pc
from algorithms.aysnc_tasks.em_bi_sql.async_sql_edm import edm_fetch
from algorithms.rate_rationale import generate_uw_rationale_doc

@hx.task
def set_migration_flag_task(hxd, progress):
    set_migration_flag(hxd, progress)
    pass

@hx.task
def search_exposure_management_data_task(hxd, progress):
    search_exposure_management_data(hxd, progress)

@hx.task
def pull_in_exposure_management_data_task(hxd, progress):
    pull_in_exposure_management_data(hxd, progress)

@hx.task
def bi_facility_fetch_task(hxd, progress):
    bi_facility_fetch(hxd, progress)
    pass

@hx.task
def rating_summary_reset_task(hxd, progress):
    rating_summary_reset(hxd, progress)

@hx.task
def bi_clm_and_mvmt_inc_triangles_fetch_task(hxd, progress):
    bi_clm_and_mvmt_fetch(hxd, progress, True)
    pass

@hx.task
def bi_clm_and_mvmt_exc_triangles_fetch_task(hxd, progress):
    bi_clm_and_mvmt_fetch(hxd, progress, False)
    pass

@hx.task
def bi_facility_include_all_task(hxd, progress):
    bi_facility_include_all(hxd, progress)
    pass

@hx.task
def bi_facility_exclude_all_task(hxd, progress):
    bi_facility_exclude_all(hxd, progress)
    pass

@hx.task
def fetch_bi_data_task(hxd, progress):
    fetch_bi_data(hxd, progress)
    pass

@hx.task
def tri_exclusions_setup_task(hxd, progress):
    tri_exclusions_setup(hxd, progress)
    pass

@hx.task
def tri_override_setup_task(hxd, progress):
    tri_override_setup(hxd, progress)
    pass

@hx.task
def bi_intelligence_fetch_task(hxd, progress):
    bi_intelligence_fetch(hxd, progress)



@hx.task
def bi_intelligence_fetch_binders_task(hxd, progress):
    bi_intelligence_fetch_binders(hxd, progress)

@hx.task
def select_binders_for_em_pull_task(hxd, progress):
    select_binders_for_em_pull(hxd, progress)

@hx.task
def clear_binder_list_task(hxd, progress):
    clear_binder_list(hxd, progress)

@hx.task
def run_bordereau_rater_task(hxd, progress):
    df = run_bordereau_rater(hxd, progress)
    gc.collect()

@hx.task
def simulate_pc_task(hxd, progress):
    simulate_pc(hxd, progress)
    pass

@hx.task
def edm_fetch_task(hxd, progress):
    edm_fetch(hxd, progress)
    pass

@hx.task
def start_renewal_task(hxd, progress):
    start_renewal(hxd, progress)
    pass

@hx.task    
def generate_uw_rationale_doc_task(hxd, progress):
    generate_uw_rationale_doc(hxd, progress)





# # Importing expiring policy for rate change
# '''
# Async task to import data from an expiring policy option for rate change calculation and analysis of movement.
# Developers will need to update the task in two places, first for which variables from the expiring policy to import,
# second to assign these to the current model variables.
# '''

# @hx.task
# def expiring_policy_fetch_task(hxd, progress):
#     user = hx.secrets.rest_api_user
#     password = hx.secrets.rest_api_password

#     expiring_policy_option_id = hxd.expiring_policy_option_id.selected
#     # expiring_policy_option_id = 75787     # Uncomment for build / debugging

#     # URL for the API
#     # SA: you should be using the v2 API. v1 will be depreciated at some point. HCM: Updated
#     url = f"https://api.beazley.hxrenew.com/api/v2-beta/policy-options/{expiring_policy_option_id}/snapshot"


#     # Update the below params variable to include all the variables which will be needed for the rate change calculation

#     params = {
#         "path": [
#             # UPDATE FROM HERE >>
#             "/brokerage",
#             "/insured", 
#             "/facility_reference", 
#             "/final_premium", 
#             "/hx_core/inception_date", 
#             "/yoa"
#             # ~~~~~~~
#         ]
#     }

#     # Call to API (do not update)  
#     try:
#         response = requests.get(url, params=params, auth=(user, password))
#     except requests.RequestException:
#         hx.errors.fatal("Unable to connect to Renew REST API")

#     # Function assigns the data from the expiring policy option to variables in the current policy. 
#     # It can handle loops and functions. 

#     # Error handling based on status code returned by API (do not update)
#     if response.ok:
#         # results stored in dict : {data:{variable_name: value}}
#         result = response.json()
#         data = result["data"]
        
#         # UPDATE FROM HERE >>

#         hxd.expiring_brokerage = data["brokerage"]
#         hxd.expiring_insured_name = data["insured"] + " - " + str(data["yoa"])
#         hxd.expiring_facility_reference = data["facility_reference"]
#         hxd.expiring_premium = data["final_premium"]

#         # ~~~~~~~~~~~~~~

        
#     # Raises error if status code is not 200 (do not update)
#     else:
#         try:
#             response_json = response.json()
#             error = f"Error: {response_json.get('title')}"
#             error += f"\nDetail: {response_json.get('detail')}" if response_json.get("detail") else ""
#             hx.errors.fatal(error)
#         except:
#             hx.errors.fatal(f"Error: {response.text}")


#     pass

