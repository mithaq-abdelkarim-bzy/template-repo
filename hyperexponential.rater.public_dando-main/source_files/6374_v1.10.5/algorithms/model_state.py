import hx

def model_state(hxd):
    '''
    Controls which page to show and hide when the start renewal button is pressed
    '''
    ms = hxd.model_state
    expiring_policy_option_id = hx.meta.expiring_policy_option_id
    # expiring_policy_option_id = 56654 # For debugging in dev mode
    ms.show_rate_change = hxd.cds.standard_fields.is_renewal

    # NOTE: This only displays the landing page for policies which are a renewal, 
    # to display the landing page always, then remove the first boolean
    # if (expiring_policy_option_id is None) or (hxd.model_state.pressed_start_renewal_task):
    #     hxd.model_state.show_landing_page = False
    #     hxd.model_state.show_after_landing_page = True
    #     hxd.model_state.show_rate_change = hxd.cds.standard_fields.is_renewal
    # else:
    #     hxd.model_state.show_landing_page = True
    #     hxd.model_state.show_after_landing_page = False
    #     hxd.model_state.show_rate_change = False

    new_workbench_rater(ms, hxd.cds.capiq_wb_id)


def new_workbench_rater(ms, capiq_wb_id):
    if (capiq_wb_id is None) or (ms.pressed_populate_capiq_task):
        ms.show_landing_page = False
        ms.show_after_landing_page = True
    else:
        ms.show_landing_page = True
        ms.show_after_landing_page = False
        ms.show_rate_change = False    

    


