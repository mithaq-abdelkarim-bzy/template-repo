import hx
import pandas as pd
import numpy as np
import algorithms.utils_global_lists as lst
from algorithms.rating_functions import fn_exposure_units_calc
from algorithms.rating_functions import fn_safe_deposit_policy_calc

# This rate change file inputs the parameters of the expiring policy into the functions from 'rating_functions' to rate up the expiring policy.
# The deductible, limits and exposures are then changed in term to split out the impact of updating each of these individually
# which means the rating is done three times


def rate_change(hxd):
    layer = hxd.cds.layers[0]
    exp_agg = hxd.cds.exposure.aggregate
    cov = layer.coverages
    cds_rc = layer.rate_change
    hxd_rc = hxd.rate_change

    param_exposure_part_d = hx.params.ExposureUnitsPartD

    cds_rc.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id

    # ~~~~~~~~~~~~~~~~~~~~~~~ SET INCLUDE / EXCLUDE IN RATE CHANGE SHEET  ~~~~~~~~~~~~~~~~~~~~~~~~
    
    lst_cover_vbl = lst.cover_hxd_vbl(hxd)
    lst_cover_vbl_rc = lst.cover_hxd_vbl_rc(hxd)
    
    # Initially we only want to show the covers in the rate change table which have been selected in the proposed policy (i.e. final_include)
    # however, sometimes coverages are added or removed so I have added a flag to reveal all available covers if necessary (i.e. available)
    for vbl, vbl_rc in zip(lst_cover_vbl, lst_cover_vbl_rc):
        if layer.show_all_covers_for_rate_change is True:
            vbl_rc.available = vbl.available    
        else:
            vbl_rc.available = vbl.final_include
        
        # set final_include
        if vbl_rc.available is True and vbl_rc.include is True:
            vbl_rc.final_include = True
        
        # Transfer final premium from current table to rate change table
        if vbl.final_include is True:
            vbl_rc.coverage_premium_current = vbl.coverage_premium
  
    
    hxd_rc.show_safe_deposit_policy_table = any(obj.final_include for obj in lst_cover_vbl_rc[23:25])
    show_computer_systems_fraud_fi_rc = any(obj.final_include for obj in lst_cover_vbl_rc[19:23])
    show_computer_systems_fraud_rc = any(obj.final_include for obj in lst_cover_vbl_rc[25:])
    hxd_rc.show_computer_crime_policy_table = show_computer_systems_fraud_fi_rc or show_computer_systems_fraud_rc
    
   
    # ~~~~~~~~~~~~~~ BASIC BOND PARAMS (expiring policy) ~~~~~~~~~~~~~~~~~~~
    
    # Assets
    if (hxd_rc.financial_assets_june_rc == 0 or hxd_rc.financial_assets_dec_rc == 0):
        hxd_rc.average_assets_rc = max(exp_agg.assets_june, exp_agg.assets_december)
    else:
        hxd_rc.average_assets_rc = (exp_agg.assets_june + exp_agg.assets_december)/2

    # Set adjusted locations
    adj_num_locations_rc = 0
    for locs_vbl, locs_str in zip([hxd_rc.branch_offices_rc, hxd_rc.facilities, hxd_rc.mobile_branch_units], ['Branch Offices', 'Facilities', 'Mobile Branch Units']):
        adj_num_locations_rc += locs_vbl.us*param_exposure_part_d[param_exposure_part_d["Additional Location"] == locs_str]["US"].iloc[0]
        adj_num_locations_rc += locs_vbl.other*param_exposure_part_d[param_exposure_part_d["Additional Location"] == locs_str]["Other"].iloc[0]
        

    # Set ratable employees
    if hxd.cds.policy_form_used == 'Form 23':
        ratable_employees_tbl = hx.params.RatableEmployees[hx.params.RatableEmployees["Assets"] <= hxd_rc.average_assets_rc]["Ratable Employees"].iloc[-1]
        amt_over_5m = min(
            5, 
            np.floor(max(0, (hxd_rc.average_assets_rc - 5e6) / 1e6))) * 5  
        amt_over_10 = np.floor(max(0, (hxd_rc.average_assets_rc - 10e6) / 1e6)) * 3
        employees_rc = ratable_employees_tbl + amt_over_5m + amt_over_10
    else:
        employees_rc = hxd_rc.number_of_employees_rc
    
   
    # ~~~~~~~~~~~~~~~~~~~~~~~ OTHER PARAMETERS ~~~~~~~~~~~~~~~~~~~~~~~~~

    # Insuring Agreement D -- specifc input 
    if hxd_rc.include_checking_accounts_coverage is True:
        checking_accounts_coverage_scale_rc = 2
    else:
        checking_accounts_coverage_scale_rc = 1

    # Extortion - Threats to Persons
    excluded_locations_persons_rc = 0
    for locs_vbl, locs_str in zip([hxd_rc.branch_offices_ex_per, hxd_rc.facilities_ex_per, hxd_rc.mobile_branch_units_ex_per], ['Branch Offices', 'Facilities', 'Mobile Branch Units']):
        excluded_locations_persons_rc += locs_vbl.us*param_exposure_part_d[param_exposure_part_d["Additional Location"] == locs_str]["US"].iloc[0]
        excluded_locations_persons_rc += locs_vbl.other*param_exposure_part_d[param_exposure_part_d["Additional Location"] == locs_str]["Other"].iloc[0]
    
    # Extortion - Threats to Property
    excluded_locations_property_rc = 0
    for locs_vbl, locs_str in zip([hxd_rc.branch_offices_ex_prop, hxd_rc.facilities_ex_prop, hxd_rc.mobile_branch_units_ex_prop], ['Branch Offices', 'Facilities', 'Mobile Branch Units']):
        excluded_locations_property_rc += locs_vbl.us*param_exposure_part_d[param_exposure_part_d["Additional Location"] == locs_str]["US"].iloc[0]
        excluded_locations_property_rc += locs_vbl.other*param_exposure_part_d[param_exposure_part_d["Additional Location"] == locs_str]["Other"].iloc[0]
        

    # Calculate loss cost for computer systems fraud
    
    loss_cost_total = 0.06  # SA: Lots of hardcoded values again in this section - should be moved somewhere central like a parameter table
    if hxd_rc.independent_software_contractors.include:
        if hxd_rc.independent_software_contractors.how_many > 0:
            hxd_rc.independent_software_contractors.loss_cost = min(0.08 + (hxd_rc.independent_software_contractors.how_many - 1) * 0.03, 0.2)
        else:
            hxd_rc.independent_software_contractors.loss_cost = 0
        loss_cost_total += hxd_rc.independent_software_contractors.loss_cost

    if hxd_rc.access_to_computer.include:
        hxd_rc.access_to_computer.loss_cost = 0.06
        loss_cost_total += hxd_rc.access_to_computer.loss_cost  # SA: Seems a little neater to do this sum at the end rather than as you go along but that's just my preference. Either is fine!
    
    if hxd_rc.atms_accessed_to_system.include:
        hxd_rc.atms_accessed_to_system.loss_cost = min(hxd_rc.atms_accessed_to_system.how_many, 15) * 0.005
        loss_cost_total += hxd_rc.atms_accessed_to_system.loss_cost

    if hxd_rc.does_include_clearing_houses.include:
        hxd_rc.does_include_clearing_houses.loss_cost = 0.03
        loss_cost_total += hxd_rc.does_include_clearing_houses.loss_cost
    
    if hxd_rc.does_include_clearing_houses.include:
        hxd_rc.does_use_fed_wire.loss_cost = 0.08
        loss_cost_total += hxd_rc.does_use_fed_wire.loss_cost
    
    if hxd_rc.additional_computer_system.include:
        hxd_rc.additional_computer_system.loss_cost = 0.06 * hxd_rc.additional_computer_system.how_many
        loss_cost_total += hxd_rc.additional_computer_system.loss_cost

    if hxd_rc.other_atm_systems.include:
        hxd_rc.other_atm_systems.loss_cost = 0.005 * hxd_rc.other_atm_systems.how_many
        loss_cost_total += hxd_rc.other_atm_systems.loss_cost

    if hxd_rc.use_telex.include:
        hxd_rc.use_telex.loss_cost = 0.06
        loss_cost_total += hxd_rc.use_telex.loss_cost
        
    hxd_rc.computer_crime_total.loss_cost = loss_cost_total





    # ~~~~~~~~~~~~~~~~~~~~~~~ SET PREMIUM VALUES - EXPIRING POLICY TERMS ~~~~~~~~~~~~~~~~~~~~~~~~

    hxd_rc.cover_1_basic_bond.expiring_premium = fn_exposure_units_calc(hxd, "Basic Bond", hxd_rc.cover_1_basic_bond.coverage, hxd_rc.cover_1_basic_bond.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_2_insuring_agreement_d.expiring_premium = fn_exposure_units_calc(hxd, 'Insuring Agreement D (Forgery & Alteration)', hxd_rc.cover_2_insuring_agreement_d.coverage, hxd_rc.cover_2_insuring_agreement_d.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)*checking_accounts_coverage_scale_rc
    hxd_rc.cover_3_agents.expiring_premium = fn_exposure_units_calc(hxd, 'Agents', hxd_rc.cover_3_agents.coverage, hxd_rc.cover_3_agents.deductible, exp_agg.number_of_agents, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_4_audit_expense.expiring_premium = fn_exposure_units_calc(hxd, 'Audit Expense', hxd_rc.cover_4_audit_expense.coverage, hxd_rc.cover_4_audit_expense.deductible, employees_rc, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_5_electronic_data_processors.expiring_premium = fn_exposure_units_calc(hxd, 'Electronic Data Processors', hxd_rc.cover_5_electronic_data_processors.coverage, hxd_rc.cover_5_electronic_data_processors.deductible, employees_rc, 0, hxd_rc.average_assets_rc, None, None)*hxd_rc.num_data_processing_orgs
    hxd_rc.cover_6_extortion_persons.expiring_premium = fn_exposure_units_calc(hxd, 'Extortion — Threats to Persons', hxd_rc.cover_6_extortion_persons.coverage, hxd_rc.cover_6_extortion_persons.deductible, employees_rc - hxd_rc.excluded_employees_persons, adj_num_locations_rc - excluded_locations_persons_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_7_extortion_property.expiring_premium = fn_exposure_units_calc(hxd, 'Extortion — Threats to Property', hxd_rc.cover_7_extortion_property.coverage, hxd_rc.cover_7_extortion_property.deductible, employees_rc - hxd_rc.excluded_employees_property, adj_num_locations_rc - excluded_locations_property_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_8_faithful_duty.expiring_premium = fn_exposure_units_calc(hxd, 'Faithful Performance of Duty', hxd_rc.cover_8_faithful_duty.coverage, hxd_rc.cover_8_faithful_duty.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_9_fraudulent_mortgages.expiring_premium = fn_exposure_units_calc(hxd, 'Fraudulent Real Property Mortgages', hxd_rc.cover_9_fraudulent_mortgages.coverage, hxd_rc.cover_9_fraudulent_mortgages.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_10_fraudulent_instructions.expiring_premium = fn_exposure_units_calc(hxd, 'Fraudulent Transfer Instructions', hxd_rc.cover_10_fraudulent_instructions.coverage, hxd_rc.cover_10_fraudulent_instructions.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_11_issuers_orders.expiring_premium = fn_exposure_units_calc(hxd, 'Issuers of Register Checks or Personal Money Orders', hxd_rc.cover_11_issuers_orders.coverage, hxd_rc.cover_11_issuers_orders.deductible, 0, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_12_misplacement.expiring_premium = fn_exposure_units_calc(hxd, 'Misplacement', cov.cover_12_misplacement.coverage, hxd_rc.cover_12_misplacement.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_13_partners_members.expiring_premium = fn_exposure_units_calc(hxd, 'Partners/Members', hxd_rc.cover_13_partners_members.coverage, hxd_rc.cover_13_partners_members.deductible, hxd_rc.number_of_partners_or_members, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_14_registered_reps.expiring_premium = fn_exposure_units_calc(hxd, 'Registered Reps. (NASD)', hxd_rc.cover_14_registered_reps.coverage, hxd_rc.cover_14_registered_reps.deductible, hxd_rc.number_of_registered_reps, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_15_servicing_contractors.expiring_premium = fn_exposure_units_calc(hxd, 'Servicing Contractors', hxd_rc.cover_15_servicing_contractors.coverage, hxd_rc.cover_15_servicing_contractors.deductible, hxd_rc.number_of_servicing_contractors, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_16_trading_loss.expiring_premium = fn_exposure_units_calc(hxd, 'Trading Loss', hxd_rc.cover_16_trading_loss.coverage, hxd_rc.cover_16_trading_loss.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_17_transit_cash_letter.expiring_premium = fn_exposure_units_calc(hxd, 'Transit Cash Letter', hxd_rc.cover_17_transit_cash_letter.coverage, hxd_rc.cover_17_transit_cash_letter.deductible, 0, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_18_unattended_atms.expiring_premium = fn_exposure_units_calc(hxd, 'Unattended ATMs', hxd_rc.cover_18_unattended_atms.coverage, hxd_rc.cover_18_unattended_atms.deductible, 0, 0.5, hxd_rc.average_assets_rc, None, None)*hxd_rc.number_of_atms
    hxd_rc.cover_19_insuring_agreement_e.expiring_premium = fn_exposure_units_calc(hxd, 'Insuring Agreement E (Securities)', hxd_rc.cover_19_insuring_agreement_e.coverage, hxd_rc.cover_19_insuring_agreement_e.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, hxd_rc.include_loan_participation_coverage, hxd_rc.loan_to_deposit_ratio)

    hxd_rc.cover_20_computer_fraud_fi.expiring_premium = fn_exposure_units_calc(hxd, 'Computer Systems Fraud (FI)', hxd_rc.cover_20_computer_fraud_fi.coverage, hxd_rc.cover_20_computer_fraud_fi.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_21_data_processing_fi.expiring_premium = fn_exposure_units_calc(hxd, 'Data Processing Service Operations (FI)', hxd_rc.cover_21_data_processing_fi.coverage, hxd_rc.cover_21_data_processing_fi.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_22_voice_transfer_fraud_fi.expiring_premium = fn_exposure_units_calc(hxd, 'Voice Initiated Transfer Fraud (FI)', hxd_rc.cover_22_voice_transfer_fraud_fi.coverage, hxd_rc.cover_22_voice_transfer_fraud_fi.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_23_telefacsimile_transfer_fraud_fi.expiring_premium = fn_exposure_units_calc(hxd, 'Telefacsimile Transfer Fraud (FI)', hxd_rc.cover_23_telefacsimile_transfer_fraud_fi.coverage, hxd_rc.cover_23_telefacsimile_transfer_fraud_fi.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)

    hxd_rc.cover_24_liability_depository.expiring_premium = fn_safe_deposit_policy_calc(hxd, 'Liability of Depository (SD)', hxd_rc.cover_24_liability_depository.coverage, hxd_rc.safe_deposit_box_coverage.num_of_rented_boxes, hxd_rc.safe_deposit_box_coverage.num_of_locations, hxd_rc.safe_deposit_box_coverage.combined_limit, hxd_rc.safe_deposit_box_coverage.include_money_coverage)
    hxd_rc.cover_25_loss_property_damage.expiring_premium = fn_safe_deposit_policy_calc(hxd, 'Loss of Property and Damage (SD)', hxd_rc.cover_25_loss_property_damage.coverage, hxd_rc.safe_deposit_box_coverage.num_of_rented_boxes, hxd_rc.safe_deposit_box_coverage.num_of_locations, hxd_rc.safe_deposit_box_coverage.combined_limit, hxd_rc.safe_deposit_box_coverage.include_money_coverage)

    hxd_rc.cover_26_computer_fraud.expiring_premium = fn_exposure_units_calc(hxd, 'Computer Systems Fraud', hxd_rc.cover_26_computer_fraud.coverage, hxd_rc.cover_26_computer_fraud.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_27_data_processing.expiring_premium = fn_exposure_units_calc(hxd, 'Data Processing Service Operations', hxd_rc.cover_27_data_processing.coverage, hxd_rc.cover_27_data_processing.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_28_voice_transfer_fraud.expiring_premium = fn_exposure_units_calc(hxd, 'Voice Initiated Transfer Fraud', hxd_rc.cover_28_voice_transfer_fraud.coverage, hxd_rc.cover_28_voice_transfer_fraud.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_29_telefacsimile_transfer_fraud.expiring_premium = fn_exposure_units_calc(hxd, 'Telefacsimile Transfer Fraud', hxd_rc.cover_29_telefacsimile_transfer_fraud.coverage, hxd_rc.cover_29_telefacsimile_transfer_fraud.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_30_hacker.expiring_premium = fn_exposure_units_calc(hxd, 'Destruction of Data or Programs by Hacker', hxd_rc.cover_30_hacker.coverage, hxd_rc.cover_30_hacker.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_31_virus.expiring_premium = fn_exposure_units_calc(hxd, 'Destruction of Data or Programs by Virus', hxd_rc.cover_31_virus.coverage, hxd_rc.cover_31_virus.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_32_voice_computer_fraud.expiring_premium = fn_exposure_units_calc(hxd, 'Voice Computer Systems Fraud', hxd_rc.cover_32_voice_computer_fraud.coverage, hxd_rc.cover_32_voice_computer_fraud.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_33_account_takeover.expiring_premium = fn_exposure_units_calc(hxd, 'Account Takeover', hxd_rc.cover_33_account_takeover.coverage, hxd_rc.cover_33_account_takeover.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)



    # ~~~~~~~~~~~~~~~~~~~~~~~ SET PREMIUM VALUES - UPDATE DEDUCTIBLE TO CURRENT TERMS ~~~~~~~~~~~~~~~~~~~~~~~~

    hxd_rc.cover_1_basic_bond.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, "Basic Bond", hxd_rc.cover_1_basic_bond.coverage, cov.cover_1_basic_bond.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_2_insuring_agreement_d.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Insuring Agreement D (Forgery & Alteration)', hxd_rc.cover_2_insuring_agreement_d.coverage, cov.cover_2_insuring_agreement_d.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)*checking_accounts_coverage_scale_rc
    hxd_rc.cover_3_agents.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Agents', hxd_rc.cover_3_agents.coverage, cov.cover_3_agents.deductible, exp_agg.number_of_agents, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_4_audit_expense.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Audit Expense', hxd_rc.cover_4_audit_expense.coverage, cov.cover_4_audit_expense.deductible, employees_rc, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_5_electronic_data_processors.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Electronic Data Processors', hxd_rc.cover_5_electronic_data_processors.coverage, cov.cover_5_electronic_data_processors.deductible, employees_rc, 0, hxd_rc.average_assets_rc, None, None)*hxd_rc.num_data_processing_orgs
    hxd_rc.cover_6_extortion_persons.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Extortion — Threats to Persons', hxd_rc.cover_6_extortion_persons.coverage, cov.cover_6_extortion_persons.deductible, employees_rc - hxd_rc.excluded_employees_persons, adj_num_locations_rc - excluded_locations_persons_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_7_extortion_property.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Extortion — Threats to Property', hxd_rc.cover_7_extortion_property.coverage, cov.cover_7_extortion_property.deductible, employees_rc - hxd_rc.excluded_employees_property, adj_num_locations_rc - excluded_locations_property_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_8_faithful_duty.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Faithful Performance of Duty', hxd_rc.cover_8_faithful_duty.coverage, cov.cover_8_faithful_duty.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_9_fraudulent_mortgages.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Fraudulent Real Property Mortgages', hxd_rc.cover_9_fraudulent_mortgages.coverage, cov.cover_9_fraudulent_mortgages.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_10_fraudulent_instructions.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Fraudulent Transfer Instructions', hxd_rc.cover_10_fraudulent_instructions.coverage, cov.cover_10_fraudulent_instructions.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_11_issuers_orders.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Issuers of Register Checks or Personal Money Orders', hxd_rc.cover_11_issuers_orders.coverage, cov.cover_11_issuers_orders.deductible, 0, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_12_misplacement.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Misplacement', hxd_rc.cover_12_misplacement.coverage, cov.cover_12_misplacement.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_13_partners_members.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Partners/Members', hxd_rc.cover_13_partners_members.coverage, cov.cover_13_partners_members.deductible, hxd_rc.number_of_partners_or_members, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_14_registered_reps.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Registered Reps. (NASD)', hxd_rc.cover_14_registered_reps.coverage, cov.cover_14_registered_reps.deductible, hxd_rc.number_of_registered_reps, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_15_servicing_contractors.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Servicing Contractors', hxd_rc.cover_15_servicing_contractors.coverage, cov.cover_15_servicing_contractors.deductible, hxd_rc.number_of_servicing_contractors, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_16_trading_loss.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Trading Loss', hxd_rc.cover_16_trading_loss.coverage, cov.cover_16_trading_loss.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_17_transit_cash_letter.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Transit Cash Letter', hxd_rc.cover_17_transit_cash_letter.coverage, cov.cover_17_transit_cash_letter.deductible, 0, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_18_unattended_atms.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Unattended ATMs', hxd_rc.cover_18_unattended_atms.coverage, cov.cover_18_unattended_atms.deductible, 0, 0.5, hxd_rc.average_assets_rc, None, None)*hxd_rc.number_of_atms
    hxd_rc.cover_19_insuring_agreement_e.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Insuring Agreement E (Securities)', hxd_rc.cover_19_insuring_agreement_e.coverage, cov.cover_19_insuring_agreement_e.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, hxd_rc.include_loan_participation_coverage, hxd_rc.loan_to_deposit_ratio)

    hxd_rc.cover_20_computer_fraud_fi.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Computer Systems Fraud (FI)', hxd_rc.cover_20_computer_fraud_fi.coverage, cov.cover_20_computer_fraud_fi.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_21_data_processing_fi.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Data Processing Service Operations (FI)', hxd_rc.cover_21_data_processing_fi.coverage, cov.cover_21_data_processing_fi.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_22_voice_transfer_fraud_fi.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Voice Initiated Transfer Fraud (FI)', hxd_rc.cover_22_voice_transfer_fraud_fi.coverage, cov.cover_22_voice_transfer_fraud_fi.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_23_telefacsimile_transfer_fraud_fi.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Telefacsimile Transfer Fraud (FI)', hxd_rc.cover_23_telefacsimile_transfer_fraud_fi.coverage, cov.cover_23_telefacsimile_transfer_fraud_fi.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)

    hxd_rc.cover_24_liability_depository.expiring_premium_update_deductible = fn_safe_deposit_policy_calc(hxd, 'Liability of Depository (SD)', hxd_rc.cover_24_liability_depository.coverage, hxd_rc.safe_deposit_box_coverage.num_of_rented_boxes, hxd_rc.safe_deposit_box_coverage.num_of_locations, hxd_rc.safe_deposit_box_coverage.combined_limit, hxd_rc.safe_deposit_box_coverage.include_money_coverage)
    hxd_rc.cover_25_loss_property_damage.expiring_premium_update_deductible = fn_safe_deposit_policy_calc(hxd, 'Loss of Property and Damage (SD)', hxd_rc.cover_25_loss_property_damage.coverage, hxd_rc.safe_deposit_box_coverage.num_of_rented_boxes, hxd_rc.safe_deposit_box_coverage.num_of_locations, hxd_rc.safe_deposit_box_coverage.combined_limit, hxd_rc.safe_deposit_box_coverage.include_money_coverage)

    hxd_rc.cover_26_computer_fraud.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Computer Systems Fraud', hxd_rc.cover_26_computer_fraud.coverage, cov.cover_26_computer_fraud.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_27_data_processing.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Data Processing Service Operations', hxd_rc.cover_27_data_processing.coverage, cov.cover_27_data_processing.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_28_voice_transfer_fraud.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Voice Initiated Transfer Fraud', hxd_rc.cover_28_voice_transfer_fraud.coverage, cov.cover_28_voice_transfer_fraud.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_29_telefacsimile_transfer_fraud.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Telefacsimile Transfer Fraud', hxd_rc.cover_29_telefacsimile_transfer_fraud.coverage, cov.cover_29_telefacsimile_transfer_fraud.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_30_hacker.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Destruction of Data or Programs by Hacker', hxd_rc.cover_30_hacker.coverage, cov.cover_30_hacker.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_31_virus.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Destruction of Data or Programs by Virus', hxd_rc.cover_31_virus.coverage, cov.cover_31_virus.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_32_voice_computer_fraud.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Voice Computer Systems Fraud', hxd_rc.cover_32_voice_computer_fraud.coverage, cov.cover_32_voice_computer_fraud.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_33_account_takeover.expiring_premium_update_deductible = fn_exposure_units_calc(hxd, 'Account Takeover', hxd_rc.cover_33_account_takeover.coverage, cov.cover_33_account_takeover.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)


    # ~~~~~~~~~~~~~~~~~~~~~~~ SET PREMIUM VALUES - UPDATE LIMIT TO CURRENT TERMS ~~~~~~~~~~~~~~~~~~~~~~~~

    hxd_rc.cover_1_basic_bond.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, "Basic Bond", cov.cover_1_basic_bond.coverage, cov.cover_1_basic_bond.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_2_insuring_agreement_d.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Insuring Agreement D (Forgery & Alteration)', cov.cover_2_insuring_agreement_d.coverage, cov.cover_2_insuring_agreement_d.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)*checking_accounts_coverage_scale_rc
    hxd_rc.cover_3_agents.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Agents', cov.cover_3_agents.coverage, cov.cover_3_agents.deductible, exp_agg.number_of_agents, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_4_audit_expense.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Audit Expense', cov.cover_4_audit_expense.coverage, cov.cover_4_audit_expense.deductible, employees_rc, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_5_electronic_data_processors.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Electronic Data Processors', cov.cover_5_electronic_data_processors.coverage, cov.cover_5_electronic_data_processors.deductible, employees_rc, 0, hxd_rc.average_assets_rc, None, None)*hxd_rc.num_data_processing_orgs
    hxd_rc.cover_6_extortion_persons.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Extortion — Threats to Persons', cov.cover_6_extortion_persons.coverage, cov.cover_6_extortion_persons.deductible, employees_rc - hxd_rc.excluded_employees_persons, adj_num_locations_rc - excluded_locations_persons_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_7_extortion_property.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Extortion — Threats to Property', cov.cover_7_extortion_property.coverage, cov.cover_7_extortion_property.deductible, employees_rc - hxd_rc.excluded_employees_property, adj_num_locations_rc - excluded_locations_property_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_8_faithful_duty.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Faithful Performance of Duty', cov.cover_8_faithful_duty.coverage, cov.cover_8_faithful_duty.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_9_fraudulent_mortgages.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Fraudulent Real Property Mortgages', cov.cover_9_fraudulent_mortgages.coverage, cov.cover_9_fraudulent_mortgages.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_10_fraudulent_instructions.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Fraudulent Transfer Instructions', cov.cover_10_fraudulent_instructions.coverage, cov.cover_10_fraudulent_instructions.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_11_issuers_orders.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Issuers of Register Checks or Personal Money Orders', cov.cover_11_issuers_orders.coverage, cov.cover_11_issuers_orders.deductible, 0, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_12_misplacement.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Misplacement', cov.cover_12_misplacement.coverage, cov.cover_12_misplacement.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_13_partners_members.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Partners/Members', cov.cover_13_partners_members.coverage, cov.cover_13_partners_members.deductible, hxd_rc.number_of_partners_or_members, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_14_registered_reps.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Registered Reps. (NASD)', cov.cover_14_registered_reps.coverage, cov.cover_14_registered_reps.deductible, hxd_rc.number_of_registered_reps, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_15_servicing_contractors.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Servicing Contractors', cov.cover_15_servicing_contractors.coverage, cov.cover_15_servicing_contractors.deductible, hxd_rc.number_of_servicing_contractors, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_16_trading_loss.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Trading Loss', cov.cover_16_trading_loss.coverage, cov.cover_16_trading_loss.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_17_transit_cash_letter.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Transit Cash Letter', cov.cover_17_transit_cash_letter.coverage, cov.cover_17_transit_cash_letter.deductible, 0, 0, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_18_unattended_atms.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Unattended ATMs', cov.cover_18_unattended_atms.coverage, cov.cover_18_unattended_atms.deductible, 0, 0.5, hxd_rc.average_assets_rc, None, None)*hxd_rc.number_of_atms
    hxd_rc.cover_19_insuring_agreement_e.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Insuring Agreement E (Securities)', cov.cover_19_insuring_agreement_e.coverage, cov.cover_19_insuring_agreement_e.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, hxd_rc.include_loan_participation_coverage, hxd_rc.loan_to_deposit_ratio)

    hxd_rc.cover_20_computer_fraud_fi.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Computer Systems Fraud (FI)', cov.cover_20_computer_fraud_fi.coverage, cov.cover_20_computer_fraud_fi.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_21_data_processing_fi.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Data Processing Service Operations (FI)', cov.cover_21_data_processing_fi.coverage, cov.cover_21_data_processing_fi.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_22_voice_transfer_fraud_fi.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Voice Initiated Transfer Fraud (FI)', cov.cover_22_voice_transfer_fraud_fi.coverage, cov.cover_22_voice_transfer_fraud_fi.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_23_telefacsimile_transfer_fraud_fi.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Telefacsimile Transfer Fraud (FI)', cov.cover_23_telefacsimile_transfer_fraud_fi.coverage, cov.cover_23_telefacsimile_transfer_fraud_fi.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)

    hxd_rc.cover_24_liability_depository.expiring_premium_update_deductible_limit = fn_safe_deposit_policy_calc(hxd, 'Liability of Depository (SD)', cov.cover_24_liability_depository.coverage, hxd_rc.safe_deposit_box_coverage.num_of_rented_boxes, hxd_rc.safe_deposit_box_coverage.num_of_locations, hxd_rc.safe_deposit_box_coverage.combined_limit, hxd_rc.safe_deposit_box_coverage.include_money_coverage)
    hxd_rc.cover_25_loss_property_damage.expiring_premium_update_deductible_limit = fn_safe_deposit_policy_calc(hxd, 'Loss of Property and Damage (SD)', cov.cover_25_loss_property_damage.coverage, hxd_rc.safe_deposit_box_coverage.num_of_rented_boxes, hxd_rc.safe_deposit_box_coverage.num_of_locations, hxd_rc.safe_deposit_box_coverage.combined_limit, hxd_rc.safe_deposit_box_coverage.include_money_coverage)

    hxd_rc.cover_26_computer_fraud.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Computer Systems Fraud', cov.cover_26_computer_fraud.coverage, cov.cover_26_computer_fraud.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_27_data_processing.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Data Processing Service Operations', cov.cover_27_data_processing.coverage, cov.cover_27_data_processing.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_28_voice_transfer_fraud.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Voice Initiated Transfer Fraud', cov.cover_28_voice_transfer_fraud.coverage, cov.cover_28_voice_transfer_fraud.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_29_telefacsimile_transfer_fraud.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Telefacsimile Transfer Fraud', cov.cover_29_telefacsimile_transfer_fraud.coverage, cov.cover_29_telefacsimile_transfer_fraud.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_30_hacker.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Destruction of Data or Programs by Hacker', cov.cover_30_hacker.coverage, cov.cover_30_hacker.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_31_virus.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Destruction of Data or Programs by Virus', cov.cover_31_virus.coverage, cov.cover_31_virus.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_32_voice_computer_fraud.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Voice Computer Systems Fraud', cov.cover_32_voice_computer_fraud.coverage, cov.cover_32_voice_computer_fraud.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
    hxd_rc.cover_33_account_takeover.expiring_premium_update_deductible_limit = fn_exposure_units_calc(hxd, 'Account Takeover', cov.cover_33_account_takeover.coverage, cov.cover_33_account_takeover.deductible, employees_rc, adj_num_locations_rc, hxd_rc.average_assets_rc, None, None)
       

    # ~~~~~~~~~~~~~~ SET INDIVIDUAL RATE CHANGE ELEMENTS ~~~~~~~~~~~~~~~~~~~

    # Set all default rate change values as 1, this is only applicible for other and T&Cs
    for item in lst.rate_change_list_static:
        rc_vbl = getattr(cds_rc, item)
        setattr(rc_vbl.uw_selected, "calculated", 1)  


    # Calculate Totals for overlapping coverages i.e coverages in both expiring and current terms
    # For the expiring policy we calculate total for all coverages as well for the rc of removing coverages

    # Expiring policy 
    total_expiring_premium = 0
    total_expiring_premium_all = 0
    for item, item_rc in zip(lst_cover_vbl, lst_cover_vbl_rc):
        if item_rc.final_include is True and item.final_include is True:
            total_expiring_premium += item_rc.expiring_premium
        if item_rc.final_include is True:
            total_expiring_premium_all += item_rc.expiring_premium
            
    # Update deductible to current terms
    total_expiring_premium_update_deductible = 0
    for item, item_rc in zip(lst_cover_vbl, lst_cover_vbl_rc):
        if item_rc.final_include is True and item.final_include is True:
            total_expiring_premium_update_deductible += item_rc.expiring_premium_update_deductible

    # Update limit to current terms
    total_expiring_premium_update_deductible_limit = 0
    total_curr_exposure = 0
    for item, item_rc in zip(lst_cover_vbl, lst_cover_vbl_rc):
        if item_rc.final_include is True and item.final_include is True:
            total_expiring_premium_update_deductible_limit += item_rc.expiring_premium_update_deductible_limit
            total_curr_exposure += item.coverage_premium
    


    # Calculate rate change

    # Deductible change
    cds_rc.deductible_change.uw_selected.calculated = total_expiring_premium_update_deductible/total_expiring_premium if total_expiring_premium else 1
 
    # Limit change
    cds_rc.limit_change.uw_selected.calculated = total_expiring_premium_update_deductible_limit/total_expiring_premium_update_deductible if total_expiring_premium_update_deductible else 1

    
    # Exposure (parameter change)
    exposure_change_parameter = total_curr_exposure/total_expiring_premium_update_deductible_limit if total_expiring_premium_update_deductible_limit else 1
    

    # Exposure (add or remove coverages)
    # Most of the time the coverages offered will be the same as expiry, although sometimes coverages will be added or removed
    # and we want to reflect that in the rate change. 

    coverage_removed = 0
    coverage_added = 0
    for item, item_rc in zip(lst_cover_vbl, lst_cover_vbl_rc):
        
        # Option for removing coverages
        if item_rc.final_include is True and item.final_include is not True:
            coverage_removed += item_rc.expiring_premium
        
        # Option for adding coverages
        if item_rc.final_include is not True and item.final_include is True:
            coverage_added += item.coverage_premium


    coverage_removed_factor = (total_expiring_premium_all - coverage_removed)/total_expiring_premium_all if total_expiring_premium_all != 0 else 1
    coverage_added_factor = layer.final_premium/(layer.final_premium - coverage_added) if (layer.final_premium - coverage_added) != 0 else 1

    exposure_change_coverage_impact = coverage_added_factor*coverage_removed_factor

    # Combine for TOTAL exposure change
    cds_rc.exposure_change.uw_selected.calculated = exposure_change_parameter*exposure_change_coverage_impact


    # Brokerage 

    cds_rc.brokerage_change.uw_selected.calculated = (1-hxd_rc.expiring_brokerage)/(1-layer.brokerage)


    # Calculate final rate change by taking the product of all selected rate changes in the static list 
    final_rc = 1
    for item in lst.rate_change_list_static:
        rc_vbl = getattr(cds_rc,item)
        final_rc *= rc_vbl.uw_selected.selected
    
    # Calculate annualised renewing and expiring premiums at 100% line size
    renewal_premium = layer.final_premium_annual / layer.beazley_share
    if cds_rc.expiring_beazley_share and cds_rc.expiring_policy_term:
        expiring_premium = (cds_rc.expiring_premium / (cds_rc.expiring_policy_term / 12)) / cds_rc.expiring_beazley_share
    else:
        expiring_premium = 0

    # Divide actual premium change by calculated rate change to get 'true' rate change
    premium_percentage_change = renewal_premium / expiring_premium if expiring_premium else 0
    cds_rc.bound_final = premium_percentage_change/final_rc if premium_percentage_change !=0 else 0

    # ~~~~~~~~~~~~~~ YOY EXPOSURE CHANGES ~~~~~~~~~~~~~~~~~~~
    
    # Show YOY exposure changes for UWs
    hxd_rc.financial_assets_june_yoy = exp_agg.assets_june / hxd_rc.financial_assets_june_rc if hxd_rc.financial_assets_june_rc else 0
    hxd_rc.financial_assets_dec_yoy = exp_agg.assets_december / hxd_rc.financial_assets_dec_rc if hxd_rc.financial_assets_dec_rc else 0
    hxd_rc.number_of_employees_yoy = exp_agg.number_of_employees / hxd_rc.number_of_employees_rc if hxd_rc.number_of_employees_rc else 0

    for loop_ren, loop_exp, loop_yoy in zip(
        [exp_agg.branch_offices, exp_agg.facilities, exp_agg.mobile_branch_units],
        [hxd_rc.branch_offices_rc, hxd_rc.facilities, hxd_rc.mobile_branch_units],
        [hxd_rc.branch_offices_yoy, hxd_rc.facilities_yoy, hxd_rc.mobile_branch_units_yoy]
        ):
        loop_yoy.us = loop_ren.us / loop_exp.us if loop_exp.us else 0
        loop_yoy.other = loop_ren.other / loop_exp.other if loop_exp.other else 0


    pass