import hx_data_schema as hx

def sch_model_state():
    '''
    Internal Model State that controls the workflow
    '''
    return {
        "model_state": hx.Structure(children={
            "pressed_start_renewal_task": hx.Bool(mode="output", async_output=["initialise_model","start_renewal_task"]),
            "show_landing_page": hx.Bool(mode="output"),
            "show_after_landing_page": hx.Bool(mode="output"),
            "show_rate_change": hx.Bool(mode="output"),
            "landing_page_info": hx.Str(
                mode="input", 
                # default="Click 'Import Expiring Policy Data' in the top right corner then click 'Start Model'",
                default="For Renewal, click 'Import Expiring Policy Data' in the top right corner then click 'Initialise Model'",
                async_output=["start_renewal_task","initialise_model"],
                view={"read_only":True}
            ),
            "pressed_initialise_model": hx.Bool(mode="output", async_output=[{"task": "initialise_model", "reset": False}]),
            "show_initialisation_page": hx.Bool(mode="output"),
            "show_initialise_model_button": hx.Bool(mode="output"),

        "expiring_policy_option_id": hx.Int(mode="input", default=None, optionality="optional", async_output=["start_renewal_task", "sync_expiring_ids","initialise_model"]),
        "policy_option_updated_from_id": hx.Int(mode="input", default=None, optionality="optional",async_output=["start_renewal_task","initialise_model"]),
        
        })
    }