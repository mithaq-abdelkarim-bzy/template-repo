import hx
# from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
def model_state(hxd):
    '''
    Controls which page to show and hide when the start renewal button is pressed
    '''

    hxd.model_state.show_initialisation_page = True
    print(f'Model state - This is the policy_option_updated_from_id:{hxd.model_state.policy_option_updated_from_id}')
    

    expiring_policy_option_id = hx.meta.expiring_policy_option_id
    # TODO - coment the below beofre go live.
    # expiring_policy_option_id = None #109687 # For debugging in dev mode

    # States in landing page
    if (expiring_policy_option_id is None):# New Policy
        # hide renewl message
        hxd.model_state.show_landing_page = False 
        # show button initialise_model
        hxd.model_state.show_initialise_model_button = True
    else: # renewals
        if not hxd.cds.standard_fields.insured_name: # Expiry data not fetched
            hxd.model_state.show_landing_page = True # this shows the  prompt to require the import of the expiry data
            # Hide button initialise_model
            hxd.model_state.show_initialise_model_button = False
        else: # expiry data has been fetched
            # show button initialise_model
            hxd.model_state.show_initialise_model_button = True
            pass

    
    # Initialisation button not pressed
    if hxd.model_state.pressed_initialise_model == None or hxd.model_state.pressed_initialise_model == False or hxd.model_state.pressed_initialise_model == False:
        hxd.model_state.show_initialisation_page = True
        
    else: # Initialisation button pressed
        # not a model version update
        if hxd.model_state.policy_option_updated_from_id == None or hxd.model_state.policy_option_updated_from_id == 0:
            
            # new policy
            if (expiring_policy_option_id is None):
                hxd.model_state.show_initialisation_page = False
                
            
            else:
            # renewal Policy 
                # start model button pressed or expiring_policy_option_id fetch in schema
                if (hxd.model_state.pressed_start_renewal_task) == True: # or (hxd.model_state.expiring_policy_option_id == expiring_policy_option_id):
                    hxd.model_state.show_initialisation_page = False
                                      
                # start model not pressed 
                else:
                    hxd.model_state.show_initialisation_page = True
                    
                    hxd.model_state.show_rate_change = False
        # model version update New and Renewal policy
        elif hxd.model_state.policy_option_updated_from_id != None and hxd.model_state.policy_option_updated_from_id != 0:
            hxd.model_state.show_initialisation_page = False
        
        # hxd.model_state.show_rate_change = hxd.cds.standard_fields.is_renewal
        hxd.model_state.show_rate_change = hxd.cds.is_real_renewal

    # # expiring_policy_option_id = hx.meta.expiring_policy_option_id
    # expiring_policy_option_id = 830774 #109687 # For debugging in dev mode
    
    # # NOTE: This only displays the landing page for policies which are a renewal, 
    # # to display the landing page always, then remove the first boolean
    # if (expiring_policy_option_id is None) or (hxd.model_state.pressed_start_renewal_task) or (hxd.model_state.expiring_policy_option_id == expiring_policy_option_id):
    #     # TODO remove before live 
        
    #     # hxd.model_state.show_landing_page = False
    #     hxd.model_state.show_rate_change = hxd.cds.standard_fields.is_renewal
    # else:
    #     # hxd.model_state.show_landing_page = True
    #     hxd.model_state.show_rate_change = False