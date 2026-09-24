import hx_data_schema as hx

def sch_model_state():
    '''
    Internal Model State that controls the workflow
    '''
    return {
        "model_state": hx.Structure(children={
            "pressed_start_renewal_task": hx.Bool(mode="input", default=None, optionality="optional", async_output=["start_renewal_task"], async_input=["rarc_task"]),
            "show_landing_page": hx.Bool(mode="output"),
            "show_after_landing_page": hx.Bool(mode="output"),
            "show_rate_change": hx.Bool(mode="output"),
            "landing_page_info": hx.Str(
                mode="input", 
                default="Click 'Import Expiring Policy Data' in the top right corner then click 'Start Policy'",
                async_input=["rarc_task"],
                async_output=["start_renewal_task"],
                view={"read_only":True}
            ),
            "pressed_populate_capiq_task": hx.Bool(mode="input", default=None, optionality="optional", async_output=["populate_capiq_data_task","populate_capiq_data_from_wb_task"], async_input=["rarc_task"]),
            # "pressed_populate_capiq_task": hx.Bool(mode="output", async_output=["populate_capiq_data_task","populate_capiq_data_from_wb_task","skip_capiq_task"]), TODO: uncomment if ading the skip button
        })
    }