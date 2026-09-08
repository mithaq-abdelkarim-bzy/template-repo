import hx

def model_state(hxd, expiring_policy_option_id):
    '''
    Controls which page to show and hide when the start renewal button is pressed
    '''
    cds = hxd.cds
    ms = hxd.model_state

    # Determine whether it's Airlines or GA
    cds.is_airlines = cds.rater == "Airlines"
    cds.is_ga = cds.rater == "General Aviation"


    # Show landing page when renewal
    if expiring_policy_option_id is None:
        ms.show_landing_page = False 
        ms.show_after_landing_page = True
        ms.show_rate_change = hxd.cds.standard_fields.is_renewal
    elif ms.pressed_start_renewal_task:
        ms.show_landing_page = (False or ms.has_import_failed)
        ms.show_after_landing_page = True
        ms.show_rate_change = hxd.cds.standard_fields.is_renewal       
    # This is for all the migrated cases - no landing pages are required. 
    # ms.expiring_policy_option_id = hx.meta.expiring_policy_option_id or #for testing: ms.expiring_policy_option_id == 598824 
    elif ms.expiring_policy_option_id == hx.meta.expiring_policy_option_id:
        ms.show_landing_page = False
        ms.show_after_landing_page = True
        ms.show_rate_change = hxd.cds.standard_fields.is_renewal
    else:
        ms.show_landing_page = True
        ms.show_after_landing_page = False
        ms.show_rate_change = False

    # Confirm model has started
    ms.pressed_either_task = ms.pressed_airlines_task or ms.pressed_ga_task
    
    # Show at renewal
    ms.show_airlines = ms.pressed_airlines_task and ms.show_after_landing_page
    ms.show_ga = ms.pressed_ga_task and ms.show_after_landing_page

