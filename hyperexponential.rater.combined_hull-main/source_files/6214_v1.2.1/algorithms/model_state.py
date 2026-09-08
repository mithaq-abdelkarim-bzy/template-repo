import hx


def model_state(hxd):
    """
    Controls which page to show and hide when the start renewal button is pressed
    """
    expiring_policy_option_id = hx.meta.expiring_policy_option_id
    # expiring_policy_option_id = 56654 # For debugging in dev mode

    # NOTE: This only displays the landing page for policies which are a renewal,
    # to display the landing page always, then remove the first boolean
    # is_expiring_policy is only set in the Snapshot of an expiring Policy during renewal to make sure the expiring Algorithm flows properly during Rate Change
    if (expiring_policy_option_id is None) or (hxd.model_state.pressed_start_renewal_task) or (hxd.model_state.is_expiring_policy):
        hxd.model_state.show_landing_page = False
        hxd.model_state.show_after_landing_page = True
        hxd.model_state.show_rate_change = hxd.cds.standard_fields.is_renewal
    else:
        hxd.model_state.show_landing_page = True
        hxd.model_state.show_after_landing_page = False
        hxd.model_state.show_rate_change = False
