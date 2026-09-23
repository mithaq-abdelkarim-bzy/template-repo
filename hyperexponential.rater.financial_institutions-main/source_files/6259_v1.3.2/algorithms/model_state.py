import hx

from algorithms.rate_constants import max_layers


def model_state(hxd):
    ms = hxd.model_state
    expiring_policy_option_id = hx.meta.expiring_policy_option_id
    # expiring_policy_option_id = 56654 # For debugging in dev mode
    
    # Controls which page to show and hide when the start renewal button is pressed
    # Only displays the landing page for policies which are a renewal
    if (expiring_policy_option_id is None) or ms.pressed_start_renewal_task or (ms.expiring_policy_option_id == expiring_policy_option_id):
        ms.show_landing_page = False
        ms.show_after_landing_page = True
        ms.show_rate_change = hxd.cds.standard_fields.is_renewal
    else:
        ms.show_landing_page = True
        ms.show_after_landing_page = False
        ms.show_rate_change = False

    # For layers not used in the pricing summary, the rate change and KPI Summary is hidden
    layers = hxd.cds.layers
    num_layers = len(layers)
    for index in range(1, max_layers + 1):
        setattr(hxd.cds.rate_change, f"show_layer_{index}", index <= num_layers)

    # Set bug report message (update rater name below, use dash for space)
    hxd.bug_report_email = """Please use the following email to report a bug or issue with the model and the support team will get back to you shortly.
    Please include the model name, a brief description of the issue, and the website link to the policy the issue relates to. 
    
    [RatingTeamDev@beazley](mailto:RatingTeamDev@beazley.com?subject=Financial-Institutions-Rater)"""
