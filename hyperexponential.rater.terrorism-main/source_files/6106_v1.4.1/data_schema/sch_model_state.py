import hx_data_schema as hx

def sch_model_state():
    '''
    Internal Model State that controls the workflow
    '''
    return {
        "model_state": hx.Structure(children={
            "pressed_start_renewal_task"        : hx.Bool(mode="output", view={"label": "pressed_start_renewal_task"},            async_output=["start_renewal_task"]),
            "show_landing_page"                 : hx.Bool(mode="output", view={"label": "show_landing_page"}),
            "show_after_landing_page"           : hx.Bool(mode="output", view={"label": "show_after_landing_page"}),
            "show_rate_change"                  : hx.Bool(mode="output", view={"label": "show_rate_change"}),
            "has_import_failed"                 : hx.Bool(mode="output", view={"label": "has_import_failed"},                     async_output=["start_renewal_task"]),

            "landing_page_info": hx.Str(
                mode="input",
                default="Click the 'import expiring policy data' arrow in the top right corner then click **Start Policy**. ",
                async_output=["start_renewal_task"],
                view={"read_only":True}
            ),
            "expiring_policy_option_id": hx.Int(mode="input", default=None, optionality="optional",                                             async_output=["start_renewal_task", "sync_expiring_ids"]),

            "is_migrated"                       : hx.Bool(mode="input",  view={"label": "is_migrated"},                         default=False,  async_output=["start_renewal_task", "sync_expiring_ids"] , async_input=["rarc_task"]),
            "not_migrated"                      : hx.Bool(mode="output", view={"label": "not_migrated"}),
            "is_new"                            : hx.Bool(mode="input",  view={"label": "is_new"},                              default=True),
            
            "show_rs_cvg"                       : hx.Bool(mode="input",  view={"label": "Show coverage detail"},                default=False),
            "show_rs_before_uw_adj"             : hx.Bool(mode="input",  view={"label": "Show Values Before UW Adjustment"},    default=False),
            "show_rs_plan"                      : hx.Bool(mode="input",  view={"label": "Show plan rates"},    default=False),
            
            # Plan rates shown
            "show_rs_not_cvg_not_before_uw_adj" : hx.Bool(mode="output", view={"label": "show_rs_not_cvg_not_before_uw_adj"}),
            "show_rs_yes_cvg_not_before_uw_adj" : hx.Bool(mode="output", view={"label": "show_rs_yes_cvg_not_before_uw_adj"}),
            "show_rs_not_cvg_yes_before_uw_adj" : hx.Bool(mode="output", view={"label": "show_rs_not_cvg_yes_before_uw_adj"}),
            "show_rs_yes_cvg_yes_before_uw_adj" : hx.Bool(mode="output", view={"label": "show_rs_yes_cvg_yes_before_uw_adj"}),
            # Plan rates hidden
            "show_rs_not_cvg_not_before_uw_adj_not_plan" : hx.Bool(mode="output", view={"label": "show_rs_not_cvg_not_before_uw_adj_not_plan"}),
            "show_rs_yes_cvg_not_before_uw_adj_not_plan" : hx.Bool(mode="output", view={"label": "show_rs_yes_cvg_not_before_uw_adj_not_plan"}),
            "show_rs_not_cvg_yes_before_uw_adj_not_plan" : hx.Bool(mode="output", view={"label": "show_rs_not_cvg_yes_before_uw_adj_not_plan"}),
            "show_rs_yes_cvg_yes_before_uw_adj_not_plan" : hx.Bool(mode="output", view={"label": "show_rs_yes_cvg_yes_before_uw_adj_not_plan"}),
        }),
        "bug_report_email": hx.Str(mode="output"),
    }