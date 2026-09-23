import hx

def model_state(hxd):
    '''
    Controls which page to show and hide when the start renewal button is pressed
    '''
    expiring_policy_option_id = hx.meta.expiring_policy_option_id

    if (expiring_policy_option_id is None) or (hxd.model_state.pressed_start_renewal_task):
        hxd.model_state.show_landing_page = False
        hxd.model_state.show_after_landing_page = True
    else:
        hxd.model_state.show_landing_page = True
        hxd.model_state.show_after_landing_page = False