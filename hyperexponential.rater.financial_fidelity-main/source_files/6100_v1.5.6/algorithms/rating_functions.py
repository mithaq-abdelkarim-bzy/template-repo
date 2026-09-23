import hx
import pandas as pd
import numpy as np



def fn_exposure_units_calc(hxd, fn_coverage_type, fn_limit, fn_deductible, fn_employees, fn_locations, fn_assets, fn_include_loan_participation_coverage, fn_loan_to_deposit_ratio):
    layer = hxd.cds.layers[0]
    exp_agg = hxd.cds.exposure.aggregate
    cov = layer.coverages

    # Parameter tables
    df_part_a = pd.DataFrame(hx.params.ExposureUnitsPartA)
    df_part_b = pd.DataFrame(hx.params.ExposureUnitsPartB)
    df_part_c = pd.DataFrame(hx.params.ExposureUnitsPartC)

    # Exceptions for different coverages types    
    if fn_coverage_type == 'Insuring Agreement E (Securities)':
        if fn_include_loan_participation_coverage is True:
            loss_cost_e = pd.DataFrame(hx.params.LossCostsEIncluding)
        else:
            loss_cost_e = pd.DataFrame(hx.params.LossCostsEExcluding)
        loss_cost = np.interp(fn_loan_to_deposit_ratio, loss_cost_e['Loan to Deposit Ratio'], loss_cost_e[hxd.cds.policy_form_used])
    elif fn_coverage_type == 'Electronic Data Processors':
        loss_cost = (hx.params.LossCosts[hx.params.LossCosts["Coverage Type"] == 'Electronic Data Processors'][hxd.cds.policy_form_used].iloc[0])
    elif fn_coverage_type == "Computer Systems Fraud (FI)" or fn_coverage_type == "Computer Systems Fraud":
        loss_cost = layer.computer_crime_total.loss_cost
    else:
        loss_cost = hx.params.LossCosts[hx.params.LossCosts["Coverage Type"] == fn_coverage_type][hxd.cds.policy_form_used].iloc[0]

    # Small loan company exception
    if hxd.cds.type_of_insured == 'Small Loan Company':
        adjustment_factor = 0.2
    else:
        adjustment_factor = 1
    
    exposure_b = np.interp(fn_employees, df_part_b['number_of_employees'], df_part_b['exposure_units'])
    
    # Coverage + Deductible
    exposure_a_det = np.interp(fn_limit + fn_deductible, df_part_a['coverage'], df_part_a['exposure_units'])
    exposure_c_det = np.interp(fn_limit + fn_deductible, df_part_c['coverage'], df_part_c['multiplier'])

    # Limited Coverage + Deductible
    exposure_a_limited_det = np.interp(min(fn_limit + fn_deductible, exp_agg.basic_unit_of_coverage, layer.basic_unit_upper_limit), df_part_a['coverage'], df_part_a['exposure_units'])
    
    # Deductible
    exposure_a_att = np.interp(fn_deductible, df_part_a['coverage'], df_part_a['exposure_units'])
    exposure_c_att = np.interp(fn_deductible, df_part_c['coverage'], df_part_c['multiplier'])

    # Limited Deductible
    exposure_a_limited_att = np.interp(min(fn_deductible, exp_agg.basic_unit_of_coverage, layer.basic_unit_upper_limit), df_part_a['coverage'], df_part_a['exposure_units'])
    
    # Total
    exposure_units_total_people_det = exposure_a_det + exposure_b*exposure_c_det
    exposure_units_total_locations_det = fn_locations*exposure_a_limited_det*adjustment_factor

    exposure_units_total_people_att = (exposure_a_att + exposure_b*exposure_c_att)*0.85
    exposure_units_total_locations_att = fn_locations*exposure_a_limited_att*0.85*adjustment_factor
    
    if fn_coverage_type == "Unattended ATMs":    
        exposure_units_total = exposure_units_total_locations_det - exposure_units_total_locations_att
    else:
        exposure_units_total = exposure_units_total_people_det + exposure_units_total_locations_det - exposure_units_total_people_att - exposure_units_total_locations_att

    company_premium = exposure_units_total*loss_cost*layer.insured_state_loss_cost_multiplier
    adj_company_premium = company_premium
    
    return adj_company_premium




def fn_safe_deposit_policy_calc(hxd, fn_coverage_type, fn_limit, fn_boxes, fn_locations, fn_single_limit, fn_include_money):
    layer = hxd.cds.layers[0]
    exp_agg = hxd.cds.exposure.aggregate
    cov = layer.coverages

    df_liab = pd.DataFrame(hx.params.LiabilityDepositoryLossCost)
    df_prop = pd.DataFrame(hx.params.LossPropertyDamagesAdditionalLocations)

    # Liability of Depository (SD)
    if fn_single_limit is True:
        single_limit = 0.9
    else:
        single_limit = 1

    liab_factor = np.interp(fn_limit, df_liab['Limit'], df_liab['Loss Cost'])
    

    # Loss of Property and Damage (SD)
    if fn_include_money is True:
        money_coverage = 2
    else:
        money_coverage = 1.6

    add_locs = fn_locations - 1
    charge_per_layer = df_prop[df_prop['Additional Locations'] <= add_locs]['Charge Each in Layer'].iloc[-1]
    charge_start_of_layer = df_prop[df_prop['Additional Locations'] <= add_locs]['Total Charge Start of Layer'].iloc[-1]
    lower_bound = df_prop[df_prop['Additional Locations'] <= add_locs]['Additional Locations'].iloc[-1]
    
    location_factor = max(0, add_locs - lower_bound)*charge_per_layer + charge_start_of_layer + 1
    
    # Calc 
    if fn_coverage_type == 'Liability of Depository (SD)':
        company_premium = fn_boxes*liab_factor*layer.insured_state_loss_cost_multiplier*single_limit
    elif fn_coverage_type == 'Loss of Property and Damage (SD)':
        company_premium = fn_boxes*money_coverage*location_factor*liab_factor*single_limit*layer.insured_state_loss_cost_multiplier
    else:
        company_premium = 0

    adj_company_premium = company_premium

    return adj_company_premium

