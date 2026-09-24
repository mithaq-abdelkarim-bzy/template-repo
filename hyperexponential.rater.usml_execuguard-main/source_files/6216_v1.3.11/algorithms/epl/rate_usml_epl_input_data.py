import hx
import datetime
from math import prod
import numpy as np
import re
from operator import itemgetter
from algorithms import rate_constants as constants 
from algorithms.rate_utilities import look_up, look_up_with_bounds, factor_validation, pd_df_from_hx_structure, set_labels, rgetattr, value_greater_than_max_validation

COLUMN_LABEL_FIELD = constants.coverage_validation_mapping["epl"]["column_label_field"]


def fetch_state_info(hxd):
    # set the state code. 
    if hxd.cds.standard_fields.is_admitted_or_surplus == "Surplus":
        state_code = "Surplus"
    else: 
        state_code = look_up(hxd.cds.state, "State Name", "Abbreviation", hx.params.table_reference_state)

    # read all basic inputs once from the state table
    state_code_row = hx.params.table_epl_admitted_applicabilities.loc[
        hx.params.table_epl_admitted_applicabilities["State"] == state_code
    ].iloc[0]

    state_info = {
        "state_code": state_code,
        "allows_ranges": state_code_row["Allows Ranges?"] == "TRUE",
        "allows_punitive_damages": state_code_row["Allows Punitive Damages Factor?"],
        "approved": state_code_row["Approved?"],
        "minimum_limit":state_code_row["Minimum Limit"],
    }

    return state_info

def calc_sug_class_of_business(hxd):
    
    naics_code = hxd.cds.industry.naics_code
    cob_map = hx.params.table_naics_master
    
    cob_rows = cob_map.loc[cob_map["NAICS Code"] == naics_code, "tblEPL_COBMap"].iloc[0]
    
    #will change this line to hxd.cds.modifiers adding the "s"
    hxd.cds.modifiers.epl.admitted_modifiers.sug_class_business.description = cob_rows
    

def validate_inputs_risk_characteristic(hxd, state_info, results):
    reactive_admitted_modifiers = hxd.cds.modifiers.epl.admitted_modifiers.reactive_admitted_modifiers
    risk_char = reactive_admitted_modifiers.risk_characteristics

    # risk_char_selection = risk_char.factor_selection

    if state_info["state_code"] == "FL":
        table_to_use = hx.params.table_epl_admmod_risk_characteristics_fl
    else:
        table_to_use = hx.params.table_epl_admmod_risk_characteristics
    risk_chars = look_up(risk_char.description.selected, "Description", ["Min", "Max", "Default Value"], table_to_use)
    risk_char.factor_selection.calculated = round(risk_chars["Default Value"] - 1, 6)
    if risk_char.factor_selection.selected is not None:
        factor_validation(
            round(risk_chars["Min"] - 1, 6),
            round(risk_chars["Max"] - 1, 6),
            round(risk_char.factor_selection.selected, 6),
            "In EPL Inputs Sheet: Risk Characteristic",
        )

    risk_char.min = round(risk_chars["Min"] - 1, 6)
    risk_char.max = round(risk_chars["Max"] - 1, 6)
    results["risk_characteristic_factor_epl"] = (risk_char.factor_selection.selected or 0) + 1
    
    #set the drop downs
    reactive_admitted_modifiers.reactive_admitted_modifiers_dropdown = table_to_use['Description'].values
    #choose the initial values as the default
    risk_char.description.calculated = table_to_use['Description'].iloc[0]


def validate_inputs_admitted_mod(hxd, node, name, table, error_name, results, node_string, allows_ranges=True, minus_one=False):
    
    input_val = node.description
    if allows_ranges:
        df_res = look_up(input_val, "Response", ["Factor Low", "Factor High", "Default Value"], table)
        val_min = round(df_res["Factor Low"] - minus_one,6)
        val_max = round(df_res["Factor High"] - minus_one,6)
        node.factor_selection.calculated = round(df_res["Default Value"] - minus_one, 6)
    else:
        no_range_val = look_up(input_val, "Response", ["No Range Value", "Default Value"], table)
        val_min = round(no_range_val["No Range Value"] - minus_one,6)
        val_max = round(no_range_val["No Range Value"] - minus_one,6)
        node.factor_selection.calculated = round(no_range_val["Default Value"] - minus_one, 6)
       
    
    if node.factor_selection.selected is not None:
        factor_validation(val_min, val_max, node.factor_selection.selected,"In EPL Inputs Sheet: "+ error_name)
    #these two functions are used to set labels
    #This one is used for conditional formatting
    set_labels(node.factor_selection.selected, val_min, val_max, rgetattr(hxd.non_cds, COLUMN_LABEL_FIELD), node_string, error_name)
    #This one is used for csetting the label on HR Policies 
    if hxd.non_cds.is_state_ca_or_in:
        hxd.non_cds.hr_policies_label = "Human Resources Department Practices"
    else:
        hxd.non_cds.hr_policies_label = "HR Policies"        
        
    node.min = val_min
    node.max = val_max
    results[name] = (node.factor_selection.selected or 0) + 1
    
    

def fetch_admitted_mod(node, name, table, lookup_column, results):
    if dir(node.description) == ['calculated', 'is_overridden', 'override', 'selected']:
        input_val = node.description.selected
    else:
        input_val = node.description

    # output = look_up(input_val, "Response", "Modifier", hx.params.table_unionized_employee)
    output = look_up(input_val, lookup_column, "Modifier", table)

    node.min = output - 1
    node.max = output - 1
    results[name] = output
    

def validate_inputs_punitive_damage_factor(hxd, state_info, results):
    #set the shortcut and values
    #punitive damages hidden for FL, GA and SC
    endorsements = hxd.cds.modifiers.epl.endorsements
    input_val = endorsements.selection.punitive_damages
    selection = endorsements.factor_selection.punitive_damages
    punitive_damages_table = hx.params.table_epl_punitive_damages
    
    hxd.non_cds.punitive_damages_acceptable = True

    if input_val != "Included":
        df_res = look_up(state_info["state_code"], "State", ["Punitive Damages Min Not Purchased", "Punitive Damages Max Not Purchased"], hx.params.table_epl_admitted_applicabilities)
        min_val = round(df_res["Punitive Damages Min Not Purchased"] - 1, 6)
        max_val = round(df_res["Punitive Damages Max Not Purchased"] - 1, 6)
        df_punitive = look_up(input_val, "Response", ["Default Value"], punitive_damages_table)
        selection.calculated = round(df_punitive["Default Value"] - 1, 6)
    else:
        min_val = 0
        max_val = 0
        selection.calculated = 0

    if selection.selected is not None:
        if state_info["state_code"] in ["FL", 'GA', 'SC']:
            hxd.non_cds.punitive_damages_acceptable = False
            hxd.non_cds.punitive_damages_not_acceptable = False
        else:    
            factor_validation(min_val, max_val, selection.selected, "In EPL Inputs Sheet: Punitive Damages")
            #add some conditional formating
            if selection.selected > max_val or selection.selected < min_val:
                hxd.non_cds.punitive_damages_not_acceptable = True
                hxd.non_cds.punitive_damages_acceptable = False
            else:
                hxd.non_cds.punitive_damages_not_acceptable = False
                hxd.non_cds.punitive_damages_acceptable = True     

        
    #set the row labels depending on the selection the min and the max

    set_labels(selection.selected, min_val, max_val, rgetattr(hxd.non_cds, COLUMN_LABEL_FIELD), 'punitive_damages', "Punitive Damages" )
        
    endorsements.min.punitive_damages = min_val
    endorsements.max.punitive_damages = max_val
    results["punitive_damage_factor_epl"] = (selection.selected or 0) + 1   
    
        

def validate_inputs_third_party_liability(hxd, state_info, results):
    endorsements = hxd.cds.modifiers.epl.endorsements

    third_party_liability_selection = endorsements.selection.reactive_third_party_liab.third_party_liability
    third_party_liability_factor_selection = endorsements.factor_selection.reactive_third_party_liab.third_party_liability

    if state_info.get("allows_ranges"):
        table_to_use = hx.params.table_epl_cwthird_party
        column_to_use = "ThirdParty"
    else:
        table_to_use = hx.params.table_epl_nr_third_party
        column_to_use = "Response"

    df_res = look_up(third_party_liability_selection, column_to_use, ["Min", "Max", "Default Value"], table_to_use, if_not_found=None)
    third_party_liability_factor_selection.calculated = round((df_res["Default Value"] or 1) - 1, 6)
    if df_res["Min"] is None or df_res["Max"] is None:
        hx.errors.validation('Please reselect the Third Party Liability Endorsement')

    min_val = round((df_res["Min"] or 1) - 1, 6)
    max_val = round((df_res["Max"] or 1) - 1, 6)
    factor_validation(
        min_val,
        max_val,
        third_party_liability_factor_selection.selected,
        "In EPL Inputs Sheet: Third Party Liability",
    )  

    endorsements.min.reactive_third_party_liab.third_party_liability = min_val
    endorsements.max.reactive_third_party_liab.third_party_liability = max_val
    results["third_party_liability_factor_epl"] = (third_party_liability_factor_selection.selected or 0) + 1


def fetch_wage_and_hour_selection(hxd, state_info, results):
    endorsements = hxd.cds.modifiers.epl.endorsements

    wage_hour_input = endorsements.selection.reactive_wage_and_hour.wage_and_hour
    if state_info["state_code"] == "CA":
        table_to_use = hx.params.table_epl_wage_hour_ca
        column_to_use = "Response"
        #wage_hour_minimum_premium = 0
        results["wage_hour_factor_epl"] = 1
        results["wage_hour_minimum_premium"] = 0
    elif state_info["state_code"] == "FL":
        table_to_use = hx.params.table_epl_wage_hour_fl
        column_to_use = "Response"
        #wage_hour_minimum_premium = 0
        results["wage_hour_factor_epl"] = 1
        results["wage_hour_minimum_premium"] = 0
    else:
        table_to_use = hx.params.table_epl_wage_hour_selection
        column_to_use = "WageAndHour"
        #we need a catch for the scenario where a wage and hour selection is made and then the state is changed    
    if wage_hour_input in table_to_use[column_to_use].values:
            wage_hour_minimum_premium = table_to_use.loc[
                table_to_use[column_to_use] == wage_hour_input, "Minimum Premium"
            ].iloc[0]

            table_row = table_to_use.loc[table_to_use[column_to_use] == wage_hour_input].iloc[0]
            wage_hour_output = table_row["Modifier"]

            endorsements.min.reactive_wage_and_hour.wage_and_hour = table_row["Modifier"]-1
            endorsements.max.reactive_wage_and_hour.wage_and_hour= table_row["Modifier"]-1

            results["wage_hour_factor_epl"] = wage_hour_output
            results["wage_hour_minimum_premium"] = wage_hour_minimum_premium
    else:
        #setting the default values equal to "not purchased"
        results["wage_hour_factor_epl"] = 1
        results["wage_hour_minimum_premium"] = 0
        hx.errors.validation(f"the wage and hour selection is not available for that state")    

def fetch_client_coverage_selection(hxd, state_info, results):
    client_cov_input = hxd.cds.modifiers.epl.endorsements.selection.client_coverage
    table_to_use = hx.params.table_client_coverage

    table_modifier = look_up(client_cov_input, "Response", "Modifier", table_to_use)

    client_cov_output = 1 if state_info["state_code"] == "WA" else table_modifier

    results["client_coverage_factor_epl"] = client_cov_output

    hxd.cds.modifiers.epl.endorsements.min.client_coverage = table_modifier - 1
    hxd.cds.modifiers.epl.endorsements.max.client_coverage = table_modifier - 1


def fetch_ahern_factors(hxd, results):
    ca_charge_lookup = hxd.cds.modifiers.epl.endorsements.selection.ahern

    charge = look_up(ca_charge_lookup, "Response", "Charge", hx.params.table_epl_ahern_ca)

    if ca_charge_lookup == "With Partnership Agreement Defense Cost Coverage with full aggregate Limit of Liability (10% surcharge plus 50)":
        surcharge = 1.1
    else:
        surcharge = 1

    results["ahern_charge_factor_epl"] = charge
    results["ahern_surcharge_factor_epl"] = surcharge


def fetch_partnership_factors(hxd, state_info, results):
    partnership_input = hxd.cds.modifiers.epl.endorsements.selection.partnership_defense

    if state_info["state_code"] == "CA":
        charge = 1
    else: 
        charge = look_up(partnership_input, "Response", "Modifier", hx.params.table_partnership_def_cost)

    results["partnership_agreement_defense_costs_factor_epl"] = charge


def fetch_coinsurance_credit(hxd, results):
    coinsure_per = hxd.cds.modifiers.epl.per_self_ins.selection
    hxd.cds.modifiers.epl.per_self_ins.max_credit = constants.coinsure_max_credit
    
    if coinsure_per is not None:
        if coinsure_per > constants.coinsure_max_credit:
            coinsurance_output = 1 - constants.coinsure_max_credit
        else:
            coinsurance_output = 1 - coinsure_per

        value_greater_than_max_validation(
        constants.coinsure_max_credit, 
        coinsure_per, 
        'Coinsurance-Percent Self Insured Selection', 
        'Max Credit')    
    else:
        coinsurance_output = 1

    hxd.cds.modifiers.epl.per_self_ins.max_credit = constants.coinsure_max_credit
    
    
        
    results["coinsurance_factor_epl"] = coinsurance_output

def get_ca_rating_factors(modifier, ca_factors_df):
    ca_factors_row = ca_factors_df[ca_factors_df["Modifier"]==modifier]
    if ca_factors_row.empty:
        ca_min = 0
        ca_max = 0
    else:
        ca_min = ca_factors_row["Min"].iloc[0]
        ca_max = ca_factors_row["Max"].iloc[0]   
    return ca_min, ca_max

def validate_inputs_schedule_rating_factors(hxd, state_info, results):
    adm = hxd.cds.modifiers.epl.admitted_schedule_rating
    ca_factors = hx.params.table_epl_schedule_rating_factors_ca
    other_dict, both_dict = constants.get_epl_admitted_factor_dict(state_info["state_code"])

    # Set constant min and max values
    other_list = ["prior_claim_activity", "turnover_rate", "financial_strength", "hr_policies", "demographic_metro"]
    for fid in other_list:
        if state_info["state_code"] in ["HI", "NE"]:
            setattr(adm.min, fid, constants.adm_sch_rating_min_hi_ne)
            setattr(adm.max, fid, constants.adm_sch_rating_max_hi_ne)
        elif state_info["state_code"] in ["NY", "LA"]:
            setattr(adm.min, fid, constants.adm_sch_rating_min_ny_la)
            setattr(adm.max, fid, constants.adm_sch_rating_max_ny_la)
        
        #New code for admitted updates Indiana and CA
        elif state_info["state_code"] in ["IN"]:
            setattr(adm.min, fid, constants.adm_sch_rating_min_in)
            setattr(adm.max, fid, constants.adm_sch_rating_max_in)
        elif state_info["state_code"] in ["CA"]:
            ca_min, ca_max = get_ca_rating_factors(fid, ca_factors)
            setattr(adm.min, fid, ca_min)
            setattr(adm.max, fid, ca_max)
        else:
            setattr(adm.min, fid, constants.adm_sch_rating_min)
            setattr(adm.max, fid, constants.adm_sch_rating_max)

    for key, value in other_dict.items():
        factor_validation(getattr(adm.min, key), getattr(adm.max, key), getattr(adm.factor_selection, key), "In EPL Inputs Sheet: " + value)

    both_list = ["management", "internal_controls", "cooperation", "experience", "staffing_turnover", "salary_structure"]
    for fid in both_list:
        if state_info["state_code"] in ["CA"]:
            ca_min, ca_max = get_ca_rating_factors(fid, ca_factors)
            setattr(adm.min, fid, ca_min)
            setattr(adm.max, fid, ca_max)
        elif state_info["state_code"] in ["IN"]:
            setattr(adm.min, fid, constants.adm_sch_rating_min_in)
            setattr(adm.max, fid, constants.adm_sch_rating_max_in)            
        else:
            setattr(adm.min, fid, constants.adm_sch_rating_min_both)
            setattr(adm.max, fid, constants.adm_sch_rating_max_both)

    for key, value in both_dict.items():
        factor_validation(getattr(adm.min, key), getattr(adm.max, key), getattr(adm.factor_selection, key), "In EPL Inputs Sheet: "+ value)


    # special case for stability
    adm.min.stability = constants.adm_sch_rating_min_stability if state_info["state_code"] == "CA" else 0
    adm.max.stability = constants.adm_sch_rating_max_stability if state_info["state_code"] == "CA" else 0
    if state_info["state_code"] == "CA":
        factor_validation(adm.min.stability, adm.max.stability, adm.factor_selection.stability, "In EPL Inputs Sheet: Stability Admitted Schedule Rating")

    if any((
        (adm.factor_selection.prior_claim_activity and adm.rationale.prior_claim_activity is None),
        (adm.factor_selection.turnover_rate and adm.rationale.turnover_rate is None),
        (adm.factor_selection.financial_strength and adm.rationale.financial_strength is None),
        (adm.factor_selection.hr_policies and adm.rationale.hr_policies is None),
        (adm.factor_selection.demographic_metro and adm.rationale.demographic_metro is None),
        (adm.factor_selection.management and adm.rationale.management is None),
        (adm.factor_selection.internal_controls and adm.rationale.internal_controls is None),
        (adm.factor_selection.cooperation and adm.rationale.cooperation is None),
        (adm.factor_selection.experience and adm.rationale.experience is None),
        (adm.factor_selection.staffing_turnover and adm.rationale.staffing_turnover is None),
        (adm.factor_selection.salary_structure and adm.rationale.salary_structure is None),
        (adm.factor_selection.stability and adm.rationale.stability is None),
    )):
        hx.errors.validation("Please provide the rationale for each corresponding factor selection made within the Admitted Schedule Rating Table on the EPL sheet.")


def fetch_prior_knowledge_factor(hxd, state_info, results):
    if hxd.cds.state_requirements.prior_knowledge_date is not None and state_info["state_code"] == 'OH':
        table = hx.params.table_epl_prior_knowledge_date
        inception_date = hxd.hx_core.inception_date
        expiry_date = hxd.hx_core.expiry_date

        policy_years = int(round((expiry_date - inception_date - datetime.timedelta(days=1)).days / 365))
        lookup_string = str(policy_years) + hxd.cds.state_requirements.prior_knowledge_date

        prior_knowledge_factor = look_up(lookup_string, "Response", "Factor", table)
    else:
        prior_knowledge_factor = 1

    results["prior_knowledge_factor_epl"] = prior_knowledge_factor


def fetch_admitted_ne_deviation_factor(hxd, state_info, results):
    ne_shortcut = hxd.cds.modifiers.epl.ne_deviation_factor
    ne_shortcut.min = constants.ne_deviation_min
    ne_shortcut.max = constants.ne_deviation_max
    ne_deviation_factor_credit_debit = ne_shortcut.factor_selection or 0

    # set the deviation factor to be used in the calculations
    
    if ne_shortcut.factor_selection == 0:
        ne_deviation_factor_epl = 1
    else:
        ne_deviation_factor_epl = max(
                1 + constants.ne_deviation_min,
                min(
                    1 + constants.ne_deviation_max,
                    1 + ne_deviation_factor_credit_debit,
                ),
            )

    #a validation message for the rationale    
    if (ne_deviation_factor_credit_debit is not None and ne_deviation_factor_credit_debit !=0) and ne_shortcut.rationale is None:
        hx.errors.validation("Please provide a rationale for the NE Deviation in EPL Inputs" )
    #a min and max validation
    factor_validation(
        ne_shortcut.min,
        ne_shortcut.max,
        ne_deviation_factor_credit_debit,
        "In EPL Inputs Sheet: NE Deviation",
    )    

    #a catch to return the ne_deviation_factor to 1 if the state changes from nebraska to something else
    if state_info["state_code"] != "NE":
        ne_deviation_factor_epl = 1

    results["ne_deviation_factor_epl"] = ne_deviation_factor_epl


def fetch_surplus_deviation(hxd, state_info, results):
    # extract the value of surplus deviation from the layers and add it to the results list
    surplus_deviation = hxd.cds.modifiers.epl.surplus_deviation or 0
    surplus_deviation_factor_epl = 1 + surplus_deviation if state_info["state_code"] == "Surplus" else 1

    results["surplus_deviation_factor_epl"] = surplus_deviation_factor_epl


def fetch_client_coverage_factor(hxd, results):
    client_cov = hxd.cds.modifiers.epl.endorsements.selection.client_coverage
    if client_cov == "Not Purchased":
        client_coverage_output = constants.client_coverage_not_purchased
    else:
        client_coverage_output = constants.client_coverage_other
        
    results["ib_client_coverage_factor_epl"] = client_coverage_output


def validate_inputs_subjective_motifiers(hxd, uw_category, string, results, minus_one = False):
    min_val = getattr(constants, f"{uw_category}_min")
    max_val = getattr(constants, f"{uw_category}_max")

    target_object = getattr(hxd.cds.modifiers.epl.benchmark_uw_modifiers, uw_category)

    subjective_modifier_output = 1 + (target_object.factor_selection or 0)

    # set the front end values
   
    target_object.min = min_val
    target_object.max = max_val
    factor_validation(min_val, max_val, round(subjective_modifier_output-minus_one, 6), "In EPL Inputs Sheet: "+ string)

    results[string] = subjective_modifier_output
    