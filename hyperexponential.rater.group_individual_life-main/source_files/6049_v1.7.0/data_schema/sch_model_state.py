import hx_data_schema as hx

def sch_model_state():
    '''
    Internal Model State that controls the workflow
    '''
    return {
        "model_state": hx.Structure(children={
            "pressed_start_renewal_task": hx.Bool(mode="output", async_output=["start_renewal_task"]),
            "show_landing_page": hx.Bool(mode="output"),
            "show_after_landing_page": hx.Bool(mode="output"),
            "show_group": hx.Bool(mode="output"),
            "show_premium_group": hx.Bool(mode="output"),
            "show_rate_change": hx.Bool(mode="output"),
            "has_import_failed": hx.Bool(mode="output", async_output=["start_renewal_task"]),
            "landing_page_info": hx.Str(
                mode="input", 
                default="Click 'Start Policy' to import the expiring information.",
                async_output=["start_renewal_task"],
                view={"read_only": True}
            )
        })
    }