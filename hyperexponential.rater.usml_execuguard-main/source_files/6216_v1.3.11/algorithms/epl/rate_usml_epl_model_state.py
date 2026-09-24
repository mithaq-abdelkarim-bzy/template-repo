import hx

def set_dropdowns(hxd, state_info):
    endorsements = hxd.cds.modifiers.epl.endorsements
    allows_ranges = state_info.get("allows_ranges")

    # set the outputs for the tables
    #third party liability
    if allows_ranges:
        table_to_use = hx.params.table_epl_cwthird_party
        column_to_use = "ThirdParty"
    else:
        table_to_use = hx.params.table_epl_nr_third_party
        column_to_use = "Response"

    reactive_third_party_liab_dropdown = table_to_use[column_to_use].values

    endorsements.selection.reactive_third_party_liab.reactive_third_party_liab_dropdown = [
        {"dropdown_item": item} for item in reactive_third_party_liab_dropdown
    ]

    #wage and hour
    if state_info["state_code"] == "CA":
        table_to_use = hx.params.table_epl_wage_hour_ca
        column_to_use = "Response"        
    elif state_info["state_code"] == "FL":
        table_to_use = hx.params.table_epl_wage_hour_fl
        column_to_use = "Response"        
    else:
        table_to_use = hx.params.table_epl_wage_hour_selection
        column_to_use = "WageAndHour"
        

    reactive_wage_and_hour_dropdown = table_to_use[column_to_use].values

    endorsements.selection.reactive_wage_and_hour.reactive_wage_and_hour_dropdown = [
        {"dropdown_item": item} for item in reactive_wage_and_hour_dropdown
    ]

   


def shownby_conditions_epl(hxd, state_info):
    hxd.non_cds.is_split_retention = hxd.cds.modifiers.epl.bnch_split_retention_offered
    hxd.non_cds.is_state_ca = state_info["state_code"] == "CA"
    hxd.non_cds.is_state_in = state_info["state_code"] == "IN"
    hxd.non_cds.is_state_in_hide = not(hxd.non_cds.is_state_in)
    hxd.non_cds.is_state_ca_or_in = hxd.non_cds.is_state_ca or hxd.non_cds.is_state_in
    hxd.non_cds.is_state_ca_or_in_hide = not(hxd.non_cds.is_state_ca or hxd.non_cds.is_state_in)
    hxd.non_cds.is_state_ne_hide = not(state_info["state_code"] == "NE")
    hxd.non_cds.is_surplus = True if state_info["state_code"] == "Surplus" else False
    hxd.non_cds.is_state_ne = True if state_info["state_code"] == "NE" else False
    hxd.non_cds.is_epl_finished_rating = not(hxd.cds.package_information.finished_rating)
    
    #set the premium label
    if hxd.cds.standard_fields.is_admitted_or_surplus == "Surplus":
        hxd.non_cds.epl_premium_label = "Surplus Premium"
    else:
        hxd.non_cds.epl_premium_label = "Admitted Premium"
    

    hxd.non_cds.is_leader_preferred = False 