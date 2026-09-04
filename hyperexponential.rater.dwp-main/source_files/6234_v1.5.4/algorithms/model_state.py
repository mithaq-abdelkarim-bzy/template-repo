import hx

def model_state(hxd):
    '''
    Controls which page to show and hide when the start renewal button is pressed
    '''
    ms = hxd.model_state

    expiring_policy_option_id = hx.meta.expiring_policy_option_id
    # expiring_policy_option_id = 56654 # For debugging in dev mode

    # NOTE: This only displays the landing page for policies which are a renewal, 
    # to display the landing page always, then remove the first boolean
    if (expiring_policy_option_id is None) or (ms.pressed_start_renewal_task) or (ms.expiring_policy_option_id == expiring_policy_option_id):
        ms.show_landing_page = False
        ms.show_after_landing_page = True
        ms.show_rate_change = hxd.cds.standard_fields.is_renewal
    else:
        ms.show_landing_page = True
        ms.show_after_landing_page = False
        ms.show_rate_change = False

     
    # Set bug report message
    hxd.bug_report_email = """Please use the following email to report a bug or issue with the model and the support team will get back to you shortly.
    Please include the model name, a brief description of the issue, and the website link to the policy the issue relates to. 
    
    [RatingTeamDev@beazley](mailto:RatingTeamDev@beazley.com?subject=DWP-Rater)"""

    # Keep track of count of validations through model
    hxd.flags.validation_count = 0


def allow_policy_doc_download(hxd):
    layer = hxd.cds.layers[0]
    doc = hxd.policy_doc
        
    tp = layer.technical_premium or 0
    bp = layer.benchmark_premium or 0
    qp = layer.quoted_premium or 0
    vc = hxd.flags.validation_count
    
    if bp <= 0:
        doc.premium_check = f"Benchmark Premium has not been calculated. Please fill in the relevant fields in to calculate premium."
        doc.show_premium_check = True
    elif tp <= 0:
        doc.premium_check = "Benchmark Premium has not been fully calculated. Please check the validation errors at the bottom right corner."
        doc.show_premium_check = True
    elif qp <= 0:
        doc.premium_check = "Quoted Premium should be greater than 0. Please input a valid number in Rating Summary."
        doc.show_premium_check = True
    elif vc > 0:
        doc.premium_check = "Please complete the underwriter rationale."
        doc.show_premium_check = True
    else:
        doc.show_generate_button = True
            