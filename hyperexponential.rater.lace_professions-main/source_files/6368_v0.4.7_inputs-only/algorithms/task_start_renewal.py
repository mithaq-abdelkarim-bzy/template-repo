# v0.5.0
import hx

def task_start_renewal(hxd, progress):
    # The following statement checks that the expiring information has been imported for renewals. Some teams might want to start
    # from a blank rater each time, in which case update the below
    ms = hxd.model_state
    sf = hxd.cds.standard_fields
    if not hxd.cds.standard_fields.insured_name:
        ms.landing_page_info = "❗**FAILED**: Click 'Undo' then 'Import Expiring Policy Data' in the top right corner.❗"
    else:
        ms.pressed_start_renewal_task = True
        ms.expiring_policy_option_id = hx.meta.expiring_policy_option_id
        sf.is_renewal = True
        # Add tasks which must be done before starting a policy here >>
    rc = hxd.cds.rate_change
    rc.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id # Assigning this node in this tasks allows to clear the override at the creation of a renewal
        