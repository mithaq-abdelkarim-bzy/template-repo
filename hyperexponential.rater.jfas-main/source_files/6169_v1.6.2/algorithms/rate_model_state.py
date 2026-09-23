import hx

def rate_model_state(hxd):
    cds = hxd.cds
    '''
    Controls which page to show and hide when the start renewal button is pressed
    '''
    expiring_policy_option_id = hx.meta.expiring_policy_option_id

    if expiring_policy_option_id is None or cds.model_state.pressed_start_renewal_task:
        cds.model_state.show_landing_page = False
        cds.model_state.show_after_landing_page = True
    else:
        cds.model_state.show_landing_page = True
        cds.model_state.show_after_landing_page = False
