import hx_data_schema as hx

def sch_model_state():
    '''
    Internal Model State that controls the workflow
    '''
    return {
        "model_state": hx.Structure(children={
            "pressed_start_renewal_task": hx.Bool(mode="input", optionality="optional", default=False),
            "show_landing_page": hx.Bool(mode="output"),
            "show_after_landing_page": hx.Bool(mode="output"),
            "show_rate_change": hx.Bool(mode="output"),
            "landing_page_info": hx.Str(
                mode="input", 
                default="Click **Start Policy** to load the model.",
                view={"read_only":True}
            ),
            "expiring_policy_option_id": hx.Int(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=["sync_expiring_ids"]),
            "is_expiring_policy": hx.Bool(mode="input", default=False, async_output=["rarc_task"])
        })
    }