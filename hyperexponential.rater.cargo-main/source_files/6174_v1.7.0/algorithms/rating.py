import hx
import algorithms.rate_utilities as utils

from algorithms.rate_risk_information import rate_risk_information
from algorithms.rate_cargo import rate_cargo
from algorithms.rate_cargo_cyber import rate_cargo_cyber
from algorithms.rate_specie import rate_specie
from algorithms.rate_conloss import rate_conloss
from algorithms.rate_rating_summary import rate_rating_summary
from algorithms.rate_rate_change import rate_rate_change
from algorithms.tpi_summary import tpi_summary
from algorithms.rate_ux import show_and_hide_pages, show_and_hide_fields, validate_status, allow_policy_doc_download, validate_written_line, validate_currency
from algorithms.policy_document import create_dict_for_excel, store_policy_data
from libraries.common_data_schema.algorithms.sync_hx_core import sync_hx_core
from libraries.email_notification.algorithms.bug_report import provision_bug_report_inputs_outputs


@hx.rating
def rating_algorithm(hxd):

    ### --- User experience --- ###
    show_and_hide_pages(hxd)
    show_and_hide_fields(hxd)

    ### --- Rating --- ###
    rate_risk_information(hxd)

    if hxd.cds.cover_selection.is_cargo:
        rate_cargo(hxd)
        #cargo cyber add on will only be running when selection is Cargo
        if hxd.cds.cover_selection.is_cargo_cyber:
            rate_cargo_cyber(hxd)
    elif hxd.cds.cover_selection.is_cargo_cyber_dropdown and (not hxd.cds.cover_selection.is_cargo_cyber):
        rate_cargo_cyber(hxd)
    elif hxd.cds.cover_selection.is_specie:
        rate_specie(hxd)
    elif hxd.cds.cover_selection.is_conloss:
        rate_conloss(hxd)

    rate_rating_summary(hxd)
    tpi_summary(hxd)

    if hxd.cds.standard_fields.is_renewal:
        rate_rate_change(hxd)

    ### --- Utilities and additional validation --- ###
    sync_hx_core(hxd)
    validate_status(hxd)
    validate_written_line(hxd)
    validate_currency(hxd)

    ### --- Policy document generation --- ###
    store_policy_data(hxd)
    allow_policy_doc_download(hxd)
    provision_bug_report_inputs_outputs(hxd)




    

