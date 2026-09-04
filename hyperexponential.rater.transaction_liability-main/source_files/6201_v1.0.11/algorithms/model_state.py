import hx

def model_state(hxd):
    '''
    Controls which page to show and hide when the start renewal button is pressed
    '''
    expiring_policy_option_id = hx.meta.expiring_policy_option_id
    # expiring_policy_option_id = 56654 # For debugging in dev mode
    
    # NOTE: This only displays the landing page for policies which are a renewal, 
    # to display the landing page always, then remove the first boolean
    if (expiring_policy_option_id is None) or (hxd.model_state.pressed_start_renewal_task):
        hxd.model_state.show_landing_page = False
        hxd.model_state.show_after_landing_page = True
        hxd.model_state.show_rate_change = hxd.cds.standard_fields.is_renewal
    else:
        hxd.model_state.show_landing_page = True
        hxd.model_state.show_after_landing_page = False
        hxd.model_state.show_rate_change = False

    # Set bug report message (update rater name below, use dash for space)
    hxd.bug_report_email = """Please use the following email to report a bug or issue with the model and the support team will get back to you shortly.
    Please include the model name, a brief description of the issue, and the website link to the policy the issue relates to. 
    
    [RatingTeamDev@beazley](mailto:RatingTeamDev@beazley.com?subject=RATERNAME-Rater)"""
