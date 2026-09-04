import hx
from algorithms.async_sql_edm                       import edm_fetch
from algorithms.async_sql_bi                        import bi_facility_include_all, bi_facility_exclude_all, bi_facility_fetch,  bi_clm_and_mvmt_fetch
from algorithms.async_tri_setup                     import tri_exclusions_setup, tri_override_setup
from algorithms.async_simulate_profit_commission    import simulate_pc
from algorithms.async_start_renewal                 import start_renewal, set_migration_flag
from algorithms.async_generate_uw_doc               import generate_uw_doc
from libraries.email_notification.algorithms.bug_report import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report


@hx.task
def set_migration_flag_task(hxd, progress):
    set_migration_flag(hxd, progress)
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
def tri_exclusions_setup_task(hxd, progress):
    tri_exclusions_setup(hxd, progress)
    pass


@hx.task
def tri_override_setup_task(hxd, progress):
    tri_override_setup(hxd, progress)
    pass


@hx.task
def edm_fetch_task(hxd, progress):
    edm_fetch(hxd, progress)
    pass


@hx.task
def bi_facility_fetch_task(hxd, progress):
    bi_facility_fetch(hxd, progress)
    pass


@hx.task
def bi_clm_and_mvmt_inc_triangles_fetch_task(hxd, progress):
    bi_clm_and_mvmt_fetch(hxd, progress, True)
    pass


@hx.task
def bi_clm_and_mvmt_exc_triangles_fetch_task(hxd, progress):
    bi_clm_and_mvmt_fetch(hxd, progress, False)
    pass


@hx.task
def simulate_pc_task(hxd, progress):
    simulate_pc(hxd, progress)
    pass


@hx.task
def start_renewal_task(hxd, progress):
    start_renewal(hxd, progress)
    pass


@hx.task
def generate_uw_doc_task(hxd, progress):
    generate_uw_doc(hxd, progress)
    pass

@hx.task
def new_bug_report_task(hxd, progress):
    model_name = "BBT"
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