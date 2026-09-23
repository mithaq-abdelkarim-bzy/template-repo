import hx
from algorithms.rate_constants import max_layers

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

    # For layers not used in the pricing summary, the rate change and KPI Summary is hidden
    layers = hxd.cds.large_cap.layers
    num_layers = len(layers)
    for index in range(1,max_layers+1):
        setattr(hxd.cds.rate_change, f"show_layer_{index}", True) if index <= num_layers else False

    if hxd.cds.risk_information.mmp_flag:
        for index in range(1,max_layers+1):
            setattr(hxd.cds.rate_change, f"show_layer_{index}", False) 





