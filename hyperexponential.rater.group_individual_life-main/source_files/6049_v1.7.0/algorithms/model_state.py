import hx

def model_state(hxd):
    '''
    Controls which page to show and hide when the start renewal button is pressed
    '''
    cds = hxd.cds
    ms = hxd.model_state

    # Determine whether it's Group or Individual
    cds.is_group = cds.rater == "Group"
    cds.is_individual = cds.rater == "Individual"

    expiring_policy_option_id = hx.meta.expiring_policy_option_id #or 55165 # NOTE: For debugging in dev mode

    # Show landing page when renewal
    if (expiring_policy_option_id is None) or (ms.pressed_start_renewal_task):
        ms.show_landing_page = False or ms.has_import_failed
        ms.show_after_landing_page = True
        ms.show_rate_change = hxd.cds.standard_fields.is_renewal
    else:
        ms.show_landing_page = True
        ms.show_after_landing_page = False
        ms.show_rate_change = False

    ms.show_group = ms.show_after_landing_page and cds.is_group
