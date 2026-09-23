import hx
import algorithms.utils_global_lists as lst
import requests
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from libraries.email_notification.algorithms.bug_report import new_bug_report, send_bug_report, generate_bug_report, cancel_bug_report, add_additional_file


@hx.task
def copy_basic_bond_terms(hxd, progress):
    layer = hxd.cds.layers[0] 
    exp_agg = hxd.cds.exposure.aggregate
    cov = layer.coverages
    rc = layer.rate_change
    
    # Much of the time the other coverages limits / deductibles will just match the basic bond cover, although not always.
    # This task copies the limit / deductible from basic bond to the other selected coverages 
    
    cover_hxd_vbl = lst.cover_hxd_vbl(hxd)
    
    basic_bond_limit = cov.cover_1_basic_bond.coverage
    basic_bond_deduct = cov.cover_1_basic_bond.deductible

    for cover in cover_hxd_vbl[1:]:
        if cover.final_include is True:
            cover.coverage = basic_bond_limit
            cover.deductible = basic_bond_deduct
        
    pass

@hx.task
def copy_expiring_basic_bond_terms(hxd, progress):
    hxd_rc = hxd.rate_change
    
    # Much of the time the other coverages limits / deductibles will just match the basic bond cover, although not always.
    # This task copies the limit / deductible from basic bond to the other selected coverages 
    
    cover_hxd_vbl = lst.cover_hxd_vbl_rc(hxd)
    
    basic_bond_limit = hxd_rc.cover_1_basic_bond.coverage
    basic_bond_deduct = hxd_rc.cover_1_basic_bond.deductible

    for cover in cover_hxd_vbl[1:]:
        if cover.final_include is True:
            cover.coverage = basic_bond_limit
            cover.deductible = basic_bond_deduct
        
    pass


# Async task to import data from an expiring policy option into the current policy for rate change and analysis of movement
@hx.task
def expiring_policy_fetch_task(hxd, progress):
    layer = hxd.cds.layers[0] 
    exp_agg = hxd.cds.exposure.aggregate
    cov = layer.coverages
    cds_rc = layer.rate_change
    hxd_rc = hxd.rate_change

    user = hx.secrets.rest_api_user
    password = hx.secrets.rest_api_password

    expiring_policy_option_id = cds_rc.expiring_policy_option_id.selected
    if not expiring_policy_option_id:
        hx.errors.fatal("Expiring Policy Option ID is missing. Enter Policy ID manually")

    # Call to API
    v2_api = init_hx_renew_api()
    response = v2_api.snapshots.get_snapshot(expiring_policy_option_id)

    if response.status_code != 200:
        raise Exception(response.json())

    # results stored in dict : {data:{variable_name: value}}
    data = response.json()['data']
    expiring_layer = data["cds"]["layers"][0]
    expiring_exp_agg = data["cds"]["exposure"]["aggregate"]
    expiring_cov = expiring_layer["coverages"]
    
    # hxd.cds.standard_fields.is_renewal = True  # Commented as reason explained in RRG-12623
    layer.status = "Submission"
    hxd_rc.expiring_brokerage = expiring_layer["brokerage"]
    cds_rc.expiring_insured_name = str(data["cds"]["standard_fields"]["insured_name"]) + " - " + str(data["cds"]["yoa"])
    if data["cds"]["standard_fields"]["policy_reference"]:
        cds_rc.expiring_policy_reference = data["cds"]["standard_fields"]["policy_reference"]
    cds_rc.expiring_premium = expiring_layer["final_premium"]
    cds_rc.expiring_policy_term = expiring_layer["term_adjustment"] * 12
    cds_rc.expiring_beazley_share = expiring_layer["beazley_share"]

    hxd_rc.financial_assets_june_rc = expiring_exp_agg["assets_june"]
    hxd_rc.financial_assets_dec_rc = expiring_exp_agg["assets_december"]
    hxd_rc.number_of_employees_rc = expiring_exp_agg["number_of_employees"]
    
    hxd_rc.branch_offices_rc.us = expiring_exp_agg["branch_offices"]["us"]
    hxd_rc.facilities.us = expiring_exp_agg["facilities"]["us"]
    hxd_rc.mobile_branch_units.us = expiring_exp_agg["mobile_branch_units"]["us"]
    hxd_rc.branch_offices_rc.other = expiring_exp_agg["branch_offices"]["other"]
    hxd_rc.facilities.other = expiring_exp_agg["facilities"]["other"]
    hxd_rc.mobile_branch_units.other = expiring_exp_agg["mobile_branch_units"]["other"]


    for vbl, name in zip(lst.cover_hxd_vbl_rc(hxd), lst.cover_str_static):
        vbl.include = expiring_cov[name]["final_include"]
        vbl.coverage = expiring_cov[name]["coverage"]
        vbl.deductible = expiring_cov[name]["deductible"]

    # Additional coverage

    hxd_rc.include_checking_accounts_coverage = expiring_layer["include_checking_accounts_coverage"]
    hxd_rc.number_of_agents = expiring_exp_agg["number_of_agents"]
    hxd_rc.loan_to_deposit_ratio = expiring_exp_agg["loan_to_deposit_ratio"]
    hxd_rc.include_loan_participation_coverage = expiring_layer["include_loan_participation_coverage"]
    hxd_rc.num_data_processing_orgs = expiring_layer["num_data_processing_orgs"]
    
    hxd_rc.branch_offices_ex_per = expiring_exp_agg['branch_offices_ex_per']
    hxd_rc.facilities_ex_per = expiring_exp_agg['facilities_ex_per']
    hxd_rc.mobile_branch_units_ex_per = expiring_exp_agg['mobile_branch_units_ex_per']
    hxd_rc.branch_offices_ex_prop = expiring_exp_agg['branch_offices_ex_prop']
    hxd_rc.facilities_ex_prop = expiring_exp_agg['facilities_ex_prop']
    hxd_rc.mobile_branch_units_ex_prop = expiring_exp_agg['mobile_branch_units_ex_prop']

    hxd_rc.excluded_employees_persons = expiring_exp_agg['excluded_employees_persons']
    hxd_rc.excluded_employees_property = expiring_exp_agg['excluded_employees_property']
    hxd_rc.number_of_issuers_of_register_checks = expiring_exp_agg['number_of_issuers_of_register_checks']
    hxd_rc.number_of_partners_or_members = expiring_exp_agg['number_of_partners_or_members']
    hxd_rc.number_of_registered_reps = expiring_exp_agg['number_of_registered_reps']
    hxd_rc.number_of_servicing_contractors = expiring_exp_agg['number_of_servicing_contractors']
    hxd_rc.number_of_atms = expiring_exp_agg['number_of_atms']

    hxd_rc.safe_deposit_box_coverage.num_of_rented_boxes = expiring_exp_agg['safe_deposit_box_coverage']['num_of_rented_boxes']
    hxd_rc.safe_deposit_box_coverage.num_of_locations = expiring_exp_agg['safe_deposit_box_coverage']['num_of_locations']
    hxd_rc.safe_deposit_box_coverage.combined_limit = expiring_exp_agg['safe_deposit_box_coverage']['combined_limit']
    hxd_rc.safe_deposit_box_coverage.include_money_coverage = expiring_exp_agg['safe_deposit_box_coverage']['include_money_coverage']

    hxd_rc.access_to_computer.include = expiring_exp_agg['access_to_computer']['include']
    hxd_rc.does_include_clearing_houses.include = expiring_exp_agg['does_include_clearing_houses']['include']
    hxd_rc.does_use_fed_wire.include = expiring_exp_agg['does_use_fed_wire']['include']
    hxd_rc.use_telex.include = expiring_exp_agg['use_telex']['include']

    hxd_rc.independent_software_contractors.include = expiring_exp_agg['independent_software_contractors']['include']
    hxd_rc.atms_accessed_to_system.include = expiring_exp_agg['atms_accessed_to_system']['include']
    hxd_rc.additional_computer_system.include = expiring_exp_agg['additional_computer_system']['include']
    hxd_rc.other_atm_systems.include = expiring_exp_agg['other_atm_systems']['include']

    hxd_rc.independent_software_contractors.how_many = expiring_exp_agg['independent_software_contractors']['how_many']
    hxd_rc.atms_accessed_to_system.how_many = expiring_exp_agg['atms_accessed_to_system']['how_many']
    hxd_rc.additional_computer_system.how_many = expiring_exp_agg['additional_computer_system']['how_many']
    hxd_rc.other_atm_systems.how_many = expiring_exp_agg['other_atm_systems']['how_many']

    pass

@hx.task
def start_renewal_task(hxd, progress):

    layer = hxd.cds.layers[0] 
    exp_agg = hxd.cds.exposure.aggregate
    cov = layer.coverages
    cds_rc = layer.rate_change
    hxd_rc = hxd.rate_change

    if not hxd.cds.standard_fields.insured_name:
        hx.errors.fatal("❗❗❗ FAILED: Click 'Undo' then 'Import Expiring Policy Data' in the top right corner ❗❗❗")
        
    hxd.model_state.pressed_start_renewal_task = True

    hx_renew_api = init_hx_renew_api()

    # hxd.expiring_policy_option_id to allow users to manually fetch the data vs hx.meta.expiring_option_id to automatically fetch renewals 
    expiring_policy_option_id = hx.meta.expiring_policy_option_id

    # URL for the API
    response = hx_renew_api.snapshots.get_snapshot(expiring_policy_option_id)

    if response.status_code != 200:
        raise Exception(response.json())

    # results stored in dict : {data:{variable_name: value}}
    data = response.json()['data']
    expiring_layer = data["cds"]["layers"][0]
    expiring_exp_agg = data["cds"]["exposure"]["aggregate"]
    expiring_cov = expiring_layer["coverages"]
    
    hxd.cds.standard_fields.is_renewal = True
    layer.status = "Submission"
    hxd_rc.expiring_brokerage = expiring_layer["brokerage"]
    cds_rc.expiring_insured_name = str(data["cds"]["standard_fields"]["insured_name"]) + " - " + str(data["cds"]["yoa"])
    if data["cds"]["standard_fields"]["policy_reference"]:
        cds_rc.expiring_policy_reference = data["cds"]["standard_fields"]["policy_reference"]
    cds_rc.expiring_premium = expiring_layer["final_premium"]
    cds_rc.expiring_policy_term = expiring_layer["term_adjustment"] * 12
    cds_rc.expiring_beazley_share = expiring_layer["beazley_share"]

    hxd_rc.financial_assets_june_rc = expiring_exp_agg["assets_june"]
    hxd_rc.financial_assets_dec_rc = expiring_exp_agg["assets_december"]
    hxd_rc.number_of_employees_rc = expiring_exp_agg["number_of_employees"]
    
    hxd_rc.branch_offices_rc.us = expiring_exp_agg["branch_offices"]["us"]
    hxd_rc.facilities.us = expiring_exp_agg["facilities"]["us"]
    hxd_rc.mobile_branch_units.us = expiring_exp_agg["mobile_branch_units"]["us"]
    hxd_rc.branch_offices_rc.other = expiring_exp_agg["branch_offices"]["other"]
    hxd_rc.facilities.other = expiring_exp_agg["facilities"]["other"]
    hxd_rc.mobile_branch_units.other = expiring_exp_agg["mobile_branch_units"]["other"]


    for vbl, name in zip(lst.cover_hxd_vbl_rc(hxd), lst.cover_str_static):
        vbl.include = expiring_cov[name]["final_include"]
        vbl.coverage = expiring_cov[name]["coverage"]
        vbl.deductible = expiring_cov[name]["deductible"]

    # Additional coverage

    hxd_rc.include_checking_accounts_coverage = expiring_layer["include_checking_accounts_coverage"]
    hxd_rc.number_of_agents = expiring_exp_agg["number_of_agents"]
    hxd_rc.loan_to_deposit_ratio = expiring_exp_agg["loan_to_deposit_ratio"]
    hxd_rc.include_loan_participation_coverage = expiring_layer["include_loan_participation_coverage"]
    hxd_rc.num_data_processing_orgs = expiring_layer["num_data_processing_orgs"]
    
    hxd_rc.branch_offices_ex_per = expiring_exp_agg['branch_offices_ex_per']
    hxd_rc.facilities_ex_per = expiring_exp_agg['facilities_ex_per']
    hxd_rc.mobile_branch_units_ex_per = expiring_exp_agg['mobile_branch_units_ex_per']
    hxd_rc.branch_offices_ex_prop = expiring_exp_agg['branch_offices_ex_prop']
    hxd_rc.facilities_ex_prop = expiring_exp_agg['facilities_ex_prop']
    hxd_rc.mobile_branch_units_ex_prop = expiring_exp_agg['mobile_branch_units_ex_prop']

    hxd_rc.excluded_employees_persons = expiring_exp_agg['excluded_employees_persons']
    hxd_rc.excluded_employees_property = expiring_exp_agg['excluded_employees_property']
    hxd_rc.number_of_issuers_of_register_checks = expiring_exp_agg['number_of_issuers_of_register_checks']
    hxd_rc.number_of_partners_or_members = expiring_exp_agg['number_of_partners_or_members']
    hxd_rc.number_of_registered_reps = expiring_exp_agg['number_of_registered_reps']
    hxd_rc.number_of_servicing_contractors = expiring_exp_agg['number_of_servicing_contractors']
    hxd_rc.number_of_atms = expiring_exp_agg['number_of_atms']

    hxd_rc.safe_deposit_box_coverage.num_of_rented_boxes = expiring_exp_agg['safe_deposit_box_coverage']['num_of_rented_boxes']
    hxd_rc.safe_deposit_box_coverage.num_of_locations = expiring_exp_agg['safe_deposit_box_coverage']['num_of_locations']
    hxd_rc.safe_deposit_box_coverage.combined_limit = expiring_exp_agg['safe_deposit_box_coverage']['combined_limit']
    hxd_rc.safe_deposit_box_coverage.include_money_coverage = expiring_exp_agg['safe_deposit_box_coverage']['include_money_coverage']

    hxd_rc.access_to_computer.include = expiring_exp_agg['access_to_computer']['include']
    hxd_rc.does_include_clearing_houses.include = expiring_exp_agg['does_include_clearing_houses']['include']
    hxd_rc.does_use_fed_wire.include = expiring_exp_agg['does_use_fed_wire']['include']
    hxd_rc.use_telex.include = expiring_exp_agg['use_telex']['include']

    hxd_rc.independent_software_contractors.include = expiring_exp_agg['independent_software_contractors']['include']
    hxd_rc.atms_accessed_to_system.include = expiring_exp_agg['atms_accessed_to_system']['include']
    hxd_rc.additional_computer_system.include = expiring_exp_agg['additional_computer_system']['include']
    hxd_rc.other_atm_systems.include = expiring_exp_agg['other_atm_systems']['include']

    hxd_rc.independent_software_contractors.how_many = expiring_exp_agg['independent_software_contractors']['how_many']
    hxd_rc.atms_accessed_to_system.how_many = expiring_exp_agg['atms_accessed_to_system']['how_many']
    hxd_rc.additional_computer_system.how_many = expiring_exp_agg['additional_computer_system']['how_many']
    hxd_rc.other_atm_systems.how_many = expiring_exp_agg['other_atm_systems']['how_many']


    pass


@hx.task
def new_bug_report_task(hxd, progress):
    model_name = "Financial Fidelity"
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