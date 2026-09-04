import hx

def model_state(hxd):
    '''
    Controls which page to show and hide when the start renewal button is pressed
    '''
    expiring_policy_option_id = hx.meta.expiring_policy_option_id

    if (expiring_policy_option_id is None) or (hxd.model_state.pressed_start_renewal_task) or (hxd.model_state.expiring_policy_option_id == expiring_policy_option_id):
        hxd.model_state.show_landing_page = False
        hxd.model_state.show_after_landing_page = True
    else:
        hxd.model_state.show_landing_page = True
        hxd.model_state.show_after_landing_page = False

    #Show/hide Policy Document page. Only visible for NACP/European Commercial Property
    hxd.quote_documents.show_page = hxd.model_state.show_after_landing_page and (hxd.policy_information.is_nacp or hxd.policy_information.team == "European Commercial Property")

    # ---------------------- Show/hide Additional Coverage page ----------------------
    
    # NACP have EB and TRIA; Open Market have neither; ECP just have EB; (all have cyber / data rest)
    team = hxd.policy_information.team

    tria = any([layer.perils.tria.include for layer in hxd.layers]) if team in ["NACP"] else False
    eb = any([layer.perils.equipment_breakdown.include for layer in hxd.layers]) if team in ["NACP", "European Commercial Property"] else False
    cyber = any([layer.perils.cyber.include for layer in hxd.layers])

    show_add_coverage_page = any([tria, eb, cyber])
    hxd.control.show_additional_coverages_page = hxd.model_state.show_after_landing_page and show_add_coverage_page

    # Show and hide features for cyber coverages
    affirmative_cyber = any([layer.perils.cyber.include_affirmative for layer in hxd.layers])
    malicious_cyber = any([layer.perils.cyber.include_malicious for layer in hxd.layers])

    hxd.control.show_cyber_premium = cyber and affirmative_cyber

    hxd.control.show_affirmative_cyber = hxd.model_state.show_after_landing_page and affirmative_cyber
    hxd.control.show_ensuing_loss_cyber = hxd.model_state.show_after_landing_page and malicious_cyber
    