import hx, os, openpyxl, json, requests
import pandas as pd
pd.set_option('display.max_rows', None)

from algorithms.tsk_policy_to_excel                     import tsk_policy_to_excel
from algorithms.tsk_fetch_ihs_data                      import tsk_fetch_ihs_data
from algorithms.tsk_confirm_limits                      import tsk_confirm_limits
from algorithms.tsk_policy_to_excel                     import tsk_policy_to_excel
from algorithms.tsk_start_renewal                       import tsk_start_renewal
from algorithms.tsk_rarc                                import tsk_expiring_policy_fetch,   tsk_rarc
from algorithms.rate_constants                          import max_layers
from libraries.email_notification.algorithms.bug_report import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report


# sets hx pas reference to the entered section reference(s)
# needs to be added to each task run, and section_reference made an async input of each of the tasks it is added to
def set_pas_references(hxd, progress):    
    pas_to_assign = [hxd.cds.layers[x].section_reference for x in range(max_layers) if x is not None]
    if pas_to_assign[0] is not None:
        hx.meta.pas_references = pas_to_assign
    else:
        hx.meta.pas_references.clear()


@hx.task
def sync_expiring_ids(hxd, progress):
    # Note this task is to be run following each migrated policy to sync the expiring ids
    hxd.model_state.expiring_policy_option_id   = hx.meta.expiring_policy_option_id
    hxd.model_state.is_migrated                 = True
    set_pas_references(hxd, progress)


@hx.task
def start_renewal_task(hxd, progress):
    tsk_start_renewal(hxd, progress)
    set_pas_references(hxd, progress)

@hx.task
def task_fetch_ihs_data(hxd, progress):
    tsk_fetch_ihs_data(hxd, progress)
    set_pas_references(hxd, progress)

@hx.task
def task_confirm_limits(hxd, progress):
    tsk_confirm_limits(hxd, progress)
    set_pas_references(hxd, progress)

@hx.task
def task_policy_to_excel(hxd, progress):    
    tsk_policy_to_excel(hxd, progress)
    set_pas_references(hxd, progress)

@hx.task
def expiring_policy_fetch_task(hxd, progress):
    tsk_expiring_policy_fetch(hxd, progress)
    set_pas_references(hxd, progress)

@hx.task
def rarc_task(hxd, progress):
    tsk_rarc(hxd, progress)
    set_pas_references(hxd, progress)

@hx.task
def clean_country_task(hxd,progress):
    expo = hxd.cds.exposure.granular
    for country in expo.countries:
        country_clean_val = getattr(country, 'country_clean')
        if (country_clean_val is not None) and (country_clean_val != " ") :
            setattr(country, 'country', country_clean_val )
@hx.task
def new_bug_report_task(hxd, progress):
    model_name = "Terrorism"
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

@hx.task
def copy_country_covers_task(hxd, progress):
    
    import algorithms.rate_utilities as utils
    cds = hxd.cds

    # Extract current values for all countries
    countries_dict = [{
        "coverage": item.coverage,
        "limit": item.limit,
        "excess": item.excess,
        "subcoverage": item.subcoverage,
        "sublimit": item.sublimit,
        "deductible": item.deductible,
        # "total_sum_insured": item.total_sum_insured,
        # "bi_sum_insured": item.bi_sum_insured,
        # "pd_sum_insured": item.pd_sum_insured,
    } for item in cds.exposure.granular.countries]
    countries_df = pd.DataFrame(countries_dict)
    
    # Copy entries for first country down to all other countries
    countries_df.iloc[1:] = countries_df.iloc[0]

    # Assign back to nodes
    utils.write_pd_to_hxd(countries_df, cds.exposure.granular.countries, list(countries_df.columns))
