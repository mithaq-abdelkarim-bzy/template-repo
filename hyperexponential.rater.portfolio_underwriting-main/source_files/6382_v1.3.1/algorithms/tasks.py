import hx
from algorithms.claim_level_data.input_claim_level                  import get_column_headers_from_claim_data_csv, import_claim_data_from_csv, clear_claim_table, pre_group_claim_data, un_group_claim_data
from algorithms.policy_level_data.input_policy_level                import get_column_headers_from_policy_data_csv, import_policy_data_from_csv, clear_policy_table, write_policy_claim_data_to_hxd, pre_group_policy_data, un_group_policy_data
from algorithms.risk_code_composition.tasks_risk_code_composition   import copy_composition_selection_table_to_manual, clear_manual_composition_table
from algorithms.pc.task_pc                                          import calculate_profit_commission
# from algorithms.tasks_helpers.generate_word_document                import generate_word_document
from algorithms.tasks_helpers.task_policy_to_excel                  import task_policy_to_excel
from algorithms.tasks_helpers.task_renewal_start                    import task_renewal_start
from algorithms.tasks_helpers.fetch_bbt                             import fetch_bbt
from algorithms.tasks_helpers.sync_lob_lists                        import sync_lob_lists
from algorithms.tasks_helpers.map_expiring                          import task_map_expiring_rate_change
from libraries.model_profiler.algorithms.profiling_hxd_functions    import time_me
from libraries.hx_renew_api.algorithms.init_hx_renew_api            import init_hx_renew_api
from libraries.email_notification.algorithms.bug_report import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report


@hx.task
def sync_expiring_ids(hxd, progress):
    # Note this task is to be run following each migrated policy to sync the expiring ids
    hxd.model_state.expiring_policy_option_id = hx.meta.expiring_policy_option_id

@hx.task
def sync_lob_lists_task(hxd, progress):
    sync_lob_lists(hxd)

@hx.task
def map_expiring_rate_change_task(hxd, progress):
    task_map_expiring_rate_change(hxd)

@hx.task
def fetch_bbt_task(hxd, progress):
    fetch_bbt(hxd)

@hx.task
def start_renewal_task(hxd, progress):
    if hxd.cds.standard_fields.insured_name is not None:
        hxd.model_state.landing_page_info = "❗**FAILED**: Click 'Undo' TWICE and DO NOT click 'Import Expiring Policy Data' again.❗"
    else:
        hxd.model_state.pressed_start_renewal_task = True
        task_renewal_start(hxd)

@hx.task
def get_column_headers_from_claim_data_csv_task(hxd, progress):
    get_column_headers_from_claim_data_csv(hxd)

@hx.task
def import_claim_data_from_csv_task(hxd, progress):
    import_claim_data_from_csv(hxd)

@hx.task
def clear_claim_level_table_task(hxd, progress):
    clear_claim_table(hxd)

@hx.task
def write_policy_claim_data_to_hxd_task(hxd, progress):
    write_policy_claim_data_to_hxd(hxd)

@hx.task
def get_column_headers_from_policy_data_csv_task(hxd, progress):
    get_column_headers_from_policy_data_csv(hxd)

@hx.task
def import_policy_data_from_csv_task(hxd, progress):
    import_policy_data_from_csv(hxd)

@hx.task
def clear_policy_level_table_task(hxd, progress):
    clear_policy_table(hxd)
    
@hx.task
def calculate_profit_commission_task(hxd, progress):
    calculate_profit_commission(hxd)

@hx.task
def copy_composition_selection_table(hxd, progress):
    copy_composition_selection_table_to_manual(hxd)

@hx.task
def clear_manual_risk_code_composition_table(hxd, progress):
    clear_manual_composition_table(hxd)
    
# @hx.task
# def generate_word_document_task(hxd, progress):
#     generate_word_document(hxd)    

@hx.task
def generate_excel_document_task(hxd, progress):
    task_policy_to_excel(hxd)   

@time_me
@hx.task
def pre_group_policy_data_task(hxd, progress):
    pre_group_policy_data(hxd)

@hx.task
def un_group_policy_data_task(hxd, progress):
    un_group_policy_data(hxd)


@hx.task
def pre_group_claim_data_task(hxd, progress):
    pre_group_claim_data(hxd)

@hx.task
def un_group_claim_data_task(hxd, progress):
    un_group_claim_data(hxd)

@hx.task
def new_bug_report_task(hxd, progress):
    model_name = "Portfolio Underwriting"
    new_bug_report(hxd, progress, model_name)

@hx.task
def send_bug_report_task(hxd, progress):
    send_bug_report(hxd, progress)

@hx.task
def cancel_bug_report_task(hxd, progress):
    cancel_bug_report(hxd, progress)

@hx.task
def generate_bug_report_task(hxd, progress):
    generate_bug_report(hxd, progress)

@hx.task
def add_additional_file_task(hxd, progress):
    add_additional_file(hxd, progress)
