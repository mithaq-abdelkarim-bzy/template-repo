import hx_data_schema as hxd

def sch_model_state():
    """
    Internal Model State that controls the workflow
    """
    return {
        "model_state": hxd.Structure(children={
            "pressed_start_renewal_task": hxd.Bool(mode="output", async_output=["start_renewal_task"]),
            "show_landing_page": hxd.Bool(mode="output"),
            "show_after_landing_page": hxd.Bool(mode="output"),
            "show_rate_change": hxd.Bool(mode="output"),
            "landing_page_info": hxd.Str(
                mode="input",
                default="Click the 'import expiring policy data' arrow in the top right corner then click **Start Policy**. ",
                async_output=["start_renewal_task"],
                view={"read_only":True}
            ),
            "expiring_policy_option_id": hxd.Int(mode="input", default=None, optionality="optional", async_output=["start_renewal_task", "sync_expiring_ids"]),
        }),
        "bug_report_email": hxd.Str(mode="output"),
    }
