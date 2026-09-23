import hx
import pandas as pd
import numpy as np
import algorithms.utils_global_lists as lst
from algorithms.rating_functions import fn_exposure_units_calc
from algorithms.rating_functions import fn_safe_deposit_policy_calc

# This is rating file sets the premium values for each of the 33 covers using the two imported rating functions. 
# the reason it's not doen as a loop is because each cover has slightly different inputs e.g. some don't rate by location so have zero as one fo the inputs
# the functions in file 'rating functions' also contains  conditions for certion cases


def set_coverage_premium(hxd):
    layer = hxd.cds.layers[0]
    exp_agg = hxd.cds.exposure.aggregate
    cov = layer.coverages

    param_exposure_part_d = hx.params.ExposureUnitsPartD
    
    # ~~~~~~~~~~~~~~ BASIC BOND PARAMS ~~~~~~~~~~~~~~~~~~~
    
    # Calc. adjusted locations and summing 
    adj_num_locations = 0
    for locs_vbl, locs_str in zip([exp_agg.branch_offices, exp_agg.facilities, exp_agg.mobile_branch_units], ['Branch Offices', 'Facilities', 'Mobile Branch Units']):
        adj_num_locations += locs_vbl.us*param_exposure_part_d[param_exposure_part_d["Additional Location"] == locs_str]["US"].iloc[0]
        adj_num_locations += locs_vbl.other*param_exposure_part_d[param_exposure_part_d["Additional Location"] == locs_str]["Other"].iloc[0]
        

    # Set ratable employees
    if hxd.cds.policy_form_used == 'Form 23':
        ratable_employees_tbl = hx.params.RatableEmployees[hx.params.RatableEmployees["Assets"] <= exp_agg.average_assets]["Ratable Employees"].iloc[-1]
        amt_over_5m = min(5,np.floor(max(0, (exp_agg.average_assets - 5e6) / 1e6))) * 5
        amt_over_10 = np.floor(max(0, (exp_agg.average_assets - 10e6) / 1e6)) * 3
        employees = ratable_employees_tbl + amt_over_5m + amt_over_10
    else:
        employees = exp_agg.number_of_employees

    # Set manual premium max coverage and deductible
    # SA: this 500e3 - is this the same value as the other 500e3s elsewhere in the code and will they all be equal?
    # If so, these should all point to the same variable (stored in a parameter table or a dedicated file for these kind of variables)
    layer.manual_premium_max_coverage = 500e3
    # SA: same considerations for 50e3 and 25e3 - all hardcoded values like this are usually better suited to a parameter table or dedicated static file
    layer.manual_premium_max_deductible = 50e3 if employees > 250 else 25e3


    # ~~~~~~~~~~~~~~~~~~~~~~~ OTHER PARAMETERS ~~~~~~~~~~~~~~~~~~~~~~~~~

    # Insuring Agreement D -- specific input    
    if layer.include_checking_accounts_coverage:
        checking_accounts_coverage_scale = 2
    else:
        checking_accounts_coverage_scale = 1

    
    # Extortion - Threats to Persons -- another sum product table
    excluded_locations_persons = 0
    for locs_vbl, locs_str in zip([exp_agg.branch_offices_ex_per, exp_agg.facilities_ex_per, exp_agg.mobile_branch_units_ex_per], ['Branch Offices', 'Facilities', 'Mobile Branch Units']):
        excluded_locations_persons += locs_vbl.us*param_exposure_part_d[param_exposure_part_d["Additional Location"] == locs_str]["US"].iloc[0]
        excluded_locations_persons += locs_vbl.other*param_exposure_part_d[param_exposure_part_d["Additional Location"] == locs_str]["Other"].iloc[0]
    
    # Extortion - Threats to Property
    excluded_locations_property = 0
    for locs_vbl, locs_str in zip([exp_agg.branch_offices_ex_prop, exp_agg.facilities_ex_prop, exp_agg.mobile_branch_units_ex_prop], ['Branch Offices', 'Facilities', 'Mobile Branch Units']):
        excluded_locations_property += locs_vbl.us*param_exposure_part_d[param_exposure_part_d["Additional Location"] == locs_str]["US"].iloc[0]
        excluded_locations_property += locs_vbl.other*param_exposure_part_d[param_exposure_part_d["Additional Location"] == locs_str]["Other"].iloc[0]
        


    # ~~~~~~~~~~~~~~~~~~~~~~~ SET PREMIUM VALUES ~~~~~~~~~~~~~~~~~~~~~~~~

    cov.cover_1_basic_bond.coverage_premium = fn_exposure_units_calc(hxd, "Basic Bond", cov.cover_1_basic_bond.coverage, cov.cover_1_basic_bond.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_2_insuring_agreement_d.coverage_premium = fn_exposure_units_calc(hxd, 'Insuring Agreement D (Forgery & Alteration)', cov.cover_2_insuring_agreement_d.coverage, cov.cover_2_insuring_agreement_d.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)*checking_accounts_coverage_scale
    cov.cover_3_agents.coverage_premium = fn_exposure_units_calc(hxd, 'Agents', cov.cover_3_agents.coverage, cov.cover_3_agents.deductible, exp_agg.number_of_agents, 0,  exp_agg.average_assets, None, None)
    cov.cover_4_audit_expense.coverage_premium = fn_exposure_units_calc(hxd, 'Audit Expense', cov.cover_4_audit_expense.coverage, cov.cover_4_audit_expense.deductible, employees, 0,  exp_agg.average_assets, None, None)
    cov.cover_5_electronic_data_processors.coverage_premium = fn_exposure_units_calc(hxd, 'Electronic Data Processors', cov.cover_5_electronic_data_processors.coverage, cov.cover_5_electronic_data_processors.deductible, employees, 0,  exp_agg.average_assets, None, None)*layer.num_data_processing_orgs
    cov.cover_6_extortion_persons.coverage_premium = fn_exposure_units_calc(hxd, 'Extortion — Threats to Persons', cov.cover_6_extortion_persons.coverage, cov.cover_6_extortion_persons.deductible, employees - exp_agg.excluded_employees_persons, adj_num_locations - excluded_locations_persons,  exp_agg.average_assets, None, None)
    cov.cover_7_extortion_property.coverage_premium = fn_exposure_units_calc(hxd, 'Extortion — Threats to Property', cov.cover_7_extortion_property.coverage, cov.cover_7_extortion_property.deductible, employees - exp_agg.excluded_employees_property, adj_num_locations - excluded_locations_property,  exp_agg.average_assets, None, None)
    cov.cover_8_faithful_duty.coverage_premium = fn_exposure_units_calc(hxd, 'Faithful Performance of Duty', cov.cover_8_faithful_duty.coverage, cov.cover_8_faithful_duty.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_9_fraudulent_mortgages.coverage_premium = fn_exposure_units_calc(hxd, 'Fraudulent Real Property Mortgages', cov.cover_9_fraudulent_mortgages.coverage, cov.cover_9_fraudulent_mortgages.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_10_fraudulent_instructions.coverage_premium = fn_exposure_units_calc(hxd, 'Fraudulent Transfer Instructions', cov.cover_10_fraudulent_instructions.coverage, cov.cover_10_fraudulent_instructions.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_11_issuers_orders.coverage_premium = fn_exposure_units_calc(hxd, 'Issuers of Register Checks or Personal Money Orders', cov.cover_11_issuers_orders.coverage, cov.cover_11_issuers_orders.deductible, 0, 0,  exp_agg.average_assets, None, None)
    cov.cover_12_misplacement.coverage_premium = fn_exposure_units_calc(hxd, 'Misplacement', cov.cover_12_misplacement.coverage, cov.cover_12_misplacement.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_13_partners_members.coverage_premium = fn_exposure_units_calc(hxd, 'Partners/Members', cov.cover_13_partners_members.coverage, cov.cover_13_partners_members.deductible, exp_agg.number_of_partners_or_members, 0,  exp_agg.average_assets, None, None)
    cov.cover_14_registered_reps.coverage_premium = fn_exposure_units_calc(hxd, 'Registered Reps. (NASD)', cov.cover_14_registered_reps.coverage, cov.cover_14_registered_reps.deductible, exp_agg.number_of_registered_reps, 0,  exp_agg.average_assets, None, None)
    cov.cover_15_servicing_contractors.coverage_premium = fn_exposure_units_calc(hxd, 'Servicing Contractors', cov.cover_15_servicing_contractors.coverage, cov.cover_15_servicing_contractors.deductible, exp_agg.number_of_servicing_contractors, 0,  exp_agg.average_assets, None, None)
    cov.cover_16_trading_loss.coverage_premium = fn_exposure_units_calc(hxd, 'Trading Loss', cov.cover_16_trading_loss.coverage, cov.cover_16_trading_loss.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_17_transit_cash_letter.coverage_premium = fn_exposure_units_calc(hxd, 'Transit Cash Letter', cov.cover_17_transit_cash_letter.coverage, cov.cover_17_transit_cash_letter.deductible, 0, 0,  exp_agg.average_assets, None, None)
    cov.cover_18_unattended_atms.coverage_premium = fn_exposure_units_calc(hxd, 'Unattended ATMs', cov.cover_18_unattended_atms.coverage, cov.cover_18_unattended_atms.deductible, 0, 0.5,  exp_agg.average_assets, None, None)*exp_agg.number_of_atms
    cov.cover_19_insuring_agreement_e.coverage_premium = fn_exposure_units_calc(hxd, 'Insuring Agreement E (Securities)', cov.cover_19_insuring_agreement_e.coverage, cov.cover_19_insuring_agreement_e.deductible, employees, adj_num_locations,  exp_agg.average_assets, layer.include_loan_participation_coverage, exp_agg.loan_to_deposit_ratio)

    cov.cover_20_computer_fraud_fi.coverage_premium = fn_exposure_units_calc(hxd, 'Computer Systems Fraud (FI)', cov.cover_20_computer_fraud_fi.coverage, cov.cover_20_computer_fraud_fi.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_21_data_processing_fi.coverage_premium = fn_exposure_units_calc(hxd, 'Data Processing Service Operations (FI)', cov.cover_21_data_processing_fi.coverage, cov.cover_21_data_processing_fi.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_22_voice_transfer_fraud_fi.coverage_premium = fn_exposure_units_calc(hxd, 'Voice Initiated Transfer Fraud (FI)', cov.cover_22_voice_transfer_fraud_fi.coverage, cov.cover_22_voice_transfer_fraud_fi.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_23_telefacsimile_transfer_fraud_fi.coverage_premium = fn_exposure_units_calc(hxd, 'Telefacsimile Transfer Fraud (FI)', cov.cover_23_telefacsimile_transfer_fraud_fi.coverage, cov.cover_23_telefacsimile_transfer_fraud_fi.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)

    cov.cover_24_liability_depository.coverage_premium = fn_safe_deposit_policy_calc(hxd, 'Liability of Depository (SD)', cov.cover_24_liability_depository.coverage, exp_agg.safe_deposit_box_coverage.num_of_rented_boxes, exp_agg.safe_deposit_box_coverage.num_of_locations, exp_agg.safe_deposit_box_coverage.combined_limit, exp_agg.safe_deposit_box_coverage.include_money_coverage)
    cov.cover_25_loss_property_damage.coverage_premium = fn_safe_deposit_policy_calc(hxd, 'Loss of Property and Damage (SD)', cov.cover_25_loss_property_damage.coverage, exp_agg.safe_deposit_box_coverage.num_of_rented_boxes, exp_agg.safe_deposit_box_coverage.num_of_locations, exp_agg.safe_deposit_box_coverage.combined_limit, exp_agg.safe_deposit_box_coverage.include_money_coverage)

    cov.cover_26_computer_fraud.coverage_premium = fn_exposure_units_calc(hxd, 'Computer Systems Fraud', cov.cover_26_computer_fraud.coverage, cov.cover_26_computer_fraud.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_27_data_processing.coverage_premium = fn_exposure_units_calc(hxd, 'Data Processing Service Operations', cov.cover_27_data_processing.coverage, cov.cover_27_data_processing.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_28_voice_transfer_fraud.coverage_premium = fn_exposure_units_calc(hxd, 'Voice Initiated Transfer Fraud', cov.cover_28_voice_transfer_fraud.coverage, cov.cover_28_voice_transfer_fraud.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_29_telefacsimile_transfer_fraud.coverage_premium = fn_exposure_units_calc(hxd, 'Telefacsimile Transfer Fraud', cov.cover_29_telefacsimile_transfer_fraud.coverage, cov.cover_29_telefacsimile_transfer_fraud.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_30_hacker.coverage_premium = fn_exposure_units_calc(hxd, 'Destruction of Data or Programs by Hacker', cov.cover_30_hacker.coverage, cov.cover_30_hacker.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_31_virus.coverage_premium = fn_exposure_units_calc(hxd, 'Destruction of Data or Programs by Virus', cov.cover_31_virus.coverage, cov.cover_31_virus.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_32_voice_computer_fraud.coverage_premium = fn_exposure_units_calc(hxd, 'Voice Computer Systems Fraud', cov.cover_32_voice_computer_fraud.coverage, cov.cover_32_voice_computer_fraud.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_33_account_takeover.coverage_premium = fn_exposure_units_calc(hxd, 'Account Takeover', cov.cover_33_account_takeover.coverage, cov.cover_33_account_takeover.deductible, employees, adj_num_locations,  exp_agg.average_assets, None, None)


    # ~~~~~~~~~~~~~~~~~~~~~~~ SET VALUES FOR MANUAL PREMIUM ~~~~~~~~~~~~~~~~~~~~~~~~

    
    # Caps deductible and coverage at the maximum for calculation of manual premium
    for cover in lst.cover_hxd_vbl(hxd):
        cover.coverage_manual = min(cover.coverage, layer.manual_premium_max_coverage)
        cover.deductible_manual = min(cover.deductible, layer.manual_premium_max_deductible)


    cov.cover_1_basic_bond.manual_premium = fn_exposure_units_calc(hxd, "Basic Bond", cov.cover_1_basic_bond.coverage_manual, cov.cover_1_basic_bond.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_2_insuring_agreement_d.manual_premium = fn_exposure_units_calc(hxd, 'Insuring Agreement D (Forgery & Alteration)', cov.cover_2_insuring_agreement_d.coverage_manual, cov.cover_2_insuring_agreement_d.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)*checking_accounts_coverage_scale
    cov.cover_3_agents.manual_premium = fn_exposure_units_calc(hxd, 'Agents', cov.cover_3_agents.coverage_manual, cov.cover_3_agents.deductible_manual, exp_agg.number_of_agents, 0,  exp_agg.average_assets, None, None)
    cov.cover_4_audit_expense.manual_premium = fn_exposure_units_calc(hxd, 'Audit Expense', cov.cover_4_audit_expense.coverage_manual, cov.cover_4_audit_expense.deductible_manual, employees, 0,  exp_agg.average_assets, None, None)
    cov.cover_5_electronic_data_processors.manual_premium = fn_exposure_units_calc(hxd, 'Electronic Data Processors', cov.cover_5_electronic_data_processors.coverage_manual, cov.cover_5_electronic_data_processors.deductible_manual, employees, 0,  exp_agg.average_assets, None, None)*layer.num_data_processing_orgs
    cov.cover_6_extortion_persons.manual_premium = fn_exposure_units_calc(hxd, 'Extortion — Threats to Persons', cov.cover_6_extortion_persons.coverage_manual, cov.cover_6_extortion_persons.deductible_manual, employees - exp_agg.excluded_employees_persons, adj_num_locations - excluded_locations_persons,  exp_agg.average_assets, None, None)
    cov.cover_7_extortion_property.manual_premium = fn_exposure_units_calc(hxd, 'Extortion — Threats to Property', cov.cover_7_extortion_property.coverage_manual, cov.cover_7_extortion_property.deductible_manual, employees - exp_agg.excluded_employees_property, adj_num_locations - excluded_locations_property,  exp_agg.average_assets, None, None)
    cov.cover_8_faithful_duty.manual_premium = fn_exposure_units_calc(hxd, 'Faithful Performance of Duty', cov.cover_8_faithful_duty.coverage_manual, cov.cover_8_faithful_duty.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_9_fraudulent_mortgages.manual_premium = fn_exposure_units_calc(hxd, 'Fraudulent Real Property Mortgages', cov.cover_9_fraudulent_mortgages.coverage_manual, cov.cover_9_fraudulent_mortgages.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_10_fraudulent_instructions.manual_premium = fn_exposure_units_calc(hxd, 'Fraudulent Transfer Instructions', cov.cover_10_fraudulent_instructions.coverage_manual, cov.cover_10_fraudulent_instructions.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_11_issuers_orders.manual_premium = fn_exposure_units_calc(hxd, 'Issuers of Register Checks or Personal Money Orders', cov.cover_11_issuers_orders.coverage_manual, cov.cover_11_issuers_orders.deductible_manual, 0, 0,  exp_agg.average_assets, None, None)
    cov.cover_12_misplacement.manual_premium = fn_exposure_units_calc(hxd, 'Misplacement', cov.cover_12_misplacement.coverage_manual, cov.cover_12_misplacement.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_13_partners_members.manual_premium = fn_exposure_units_calc(hxd, 'Partners/Members', cov.cover_13_partners_members.coverage_manual, cov.cover_13_partners_members.deductible_manual, exp_agg.number_of_partners_or_members, 0,  exp_agg.average_assets, None, None)
    cov.cover_14_registered_reps.manual_premium = fn_exposure_units_calc(hxd, 'Registered Reps. (NASD)', cov.cover_14_registered_reps.coverage_manual, cov.cover_14_registered_reps.deductible_manual, exp_agg.number_of_registered_reps, 0,  exp_agg.average_assets, None, None)
    cov.cover_15_servicing_contractors.manual_premium = fn_exposure_units_calc(hxd, 'Servicing Contractors', cov.cover_15_servicing_contractors.coverage_manual, cov.cover_15_servicing_contractors.deductible_manual, exp_agg.number_of_servicing_contractors, 0,  exp_agg.average_assets, None, None)
    cov.cover_16_trading_loss.manual_premium = fn_exposure_units_calc(hxd, 'Trading Loss', cov.cover_16_trading_loss.coverage_manual, cov.cover_16_trading_loss.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_17_transit_cash_letter.manual_premium = fn_exposure_units_calc(hxd, 'Transit Cash Letter', cov.cover_17_transit_cash_letter.coverage_manual, cov.cover_17_transit_cash_letter.deductible_manual, 0, 0,  exp_agg.average_assets, None, None)
    cov.cover_18_unattended_atms.manual_premium = fn_exposure_units_calc(hxd, 'Unattended ATMs', cov.cover_18_unattended_atms.coverage_manual, cov.cover_18_unattended_atms.deductible_manual, 0, 0.5,  exp_agg.average_assets, None, None)*exp_agg.number_of_atms
    cov.cover_19_insuring_agreement_e.manual_premium = fn_exposure_units_calc(hxd, 'Insuring Agreement E (Securities)', cov.cover_19_insuring_agreement_e.coverage_manual, cov.cover_19_insuring_agreement_e.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, layer.include_loan_participation_coverage, exp_agg.loan_to_deposit_ratio)

    cov.cover_20_computer_fraud_fi.manual_premium = fn_exposure_units_calc(hxd, 'Computer Systems Fraud (FI)', cov.cover_20_computer_fraud_fi.coverage_manual, cov.cover_20_computer_fraud_fi.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_21_data_processing_fi.manual_premium = fn_exposure_units_calc(hxd, 'Data Processing Service Operations (FI)', cov.cover_21_data_processing_fi.coverage_manual, cov.cover_21_data_processing_fi.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_22_voice_transfer_fraud_fi.manual_premium = fn_exposure_units_calc(hxd, 'Voice Initiated Transfer Fraud (FI)', cov.cover_22_voice_transfer_fraud_fi.coverage_manual, cov.cover_22_voice_transfer_fraud_fi.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_23_telefacsimile_transfer_fraud_fi.manual_premium = fn_exposure_units_calc(hxd, 'Telefacsimile Transfer Fraud (FI)', cov.cover_23_telefacsimile_transfer_fraud_fi.coverage_manual, cov.cover_23_telefacsimile_transfer_fraud_fi.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)

    cov.cover_24_liability_depository.manual_premium = fn_safe_deposit_policy_calc(hxd, 'Liability of Depository (SD)', cov.cover_24_liability_depository.coverage_manual, exp_agg.safe_deposit_box_coverage.num_of_rented_boxes, exp_agg.safe_deposit_box_coverage.num_of_locations, exp_agg.safe_deposit_box_coverage.combined_limit, exp_agg.safe_deposit_box_coverage.include_money_coverage)
    cov.cover_25_loss_property_damage.manual_premium = fn_safe_deposit_policy_calc(hxd, 'Loss of Property and Damage (SD)', cov.cover_25_loss_property_damage.coverage_manual, exp_agg.safe_deposit_box_coverage.num_of_rented_boxes, exp_agg.safe_deposit_box_coverage.num_of_locations, exp_agg.safe_deposit_box_coverage.combined_limit, exp_agg.safe_deposit_box_coverage.include_money_coverage)

    cov.cover_26_computer_fraud.manual_premium = fn_exposure_units_calc(hxd, 'Computer Systems Fraud', cov.cover_26_computer_fraud.coverage_manual, cov.cover_26_computer_fraud.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_27_data_processing.manual_premium = fn_exposure_units_calc(hxd, 'Data Processing Service Operations', cov.cover_27_data_processing.coverage_manual, cov.cover_27_data_processing.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_28_voice_transfer_fraud.manual_premium = fn_exposure_units_calc(hxd, 'Voice Initiated Transfer Fraud', cov.cover_28_voice_transfer_fraud.coverage_manual, cov.cover_28_voice_transfer_fraud.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_29_telefacsimile_transfer_fraud.manual_premium = fn_exposure_units_calc(hxd, 'Telefacsimile Transfer Fraud', cov.cover_29_telefacsimile_transfer_fraud.coverage_manual, cov.cover_29_telefacsimile_transfer_fraud.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_30_hacker.manual_premium = fn_exposure_units_calc(hxd, 'Destruction of Data or Programs by Hacker', cov.cover_30_hacker.coverage_manual, cov.cover_30_hacker.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_31_virus.manual_premium = fn_exposure_units_calc(hxd, 'Destruction of Data or Programs by Virus', cov.cover_31_virus.coverage_manual, cov.cover_31_virus.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_32_voice_computer_fraud.manual_premium = fn_exposure_units_calc(hxd, 'Voice Computer Systems Fraud', cov.cover_32_voice_computer_fraud.coverage_manual, cov.cover_32_voice_computer_fraud.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)
    cov.cover_33_account_takeover.manual_premium = fn_exposure_units_calc(hxd, 'Account Takeover', cov.cover_33_account_takeover.coverage_manual, cov.cover_33_account_takeover.deductible_manual, employees, adj_num_locations,  exp_agg.average_assets, None, None)

    

    # Round both coverage and manual premium to the nearest integer

    for cover in lst.cover_hxd_vbl(hxd):
        cover.manual_premium = round(cover.manual_premium)



    # Totals manual premium and unity premium for use in experience rating
    
    # Manual premium is added even if it isn't included in the coverage
    layer.manual_premium = 0
    for cover in lst.cover_hxd_vbl(hxd):
        if cover.available is True and cover.include is True:
            layer.manual_premium += cover.manual_premium
    
    layer.company_premium = 0
    for cover in lst.cover_hxd_vbl(hxd):
        if cover.available is True and cover.include is True:
            layer.company_premium += cover.coverage_premium





