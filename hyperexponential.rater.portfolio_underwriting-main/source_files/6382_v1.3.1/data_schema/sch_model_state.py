import hx_data_schema as hx

def sch_model_state():
    '''
    Internal Model State that controls the workflow
    '''
    return {
        "model_state": hx.Structure(children={
            "pressed_start_renewal_task": hx.Bool(mode="output", async_output=["start_renewal_task"]),

            "show_landing_page":        hx.Bool(mode="output"), # careful with this it already existed
            "show_risk_information":    hx.Bool(mode="output"),
            "show_risk_code_library":   hx.Bool(mode="output"),
            "show_policy_data":         hx.Bool(mode="output"),
            "show_claim_data":          hx.Bool(mode="output"),
            "show_risk_code_comp":      hx.Bool(mode="output"),
            "show_deductions":          hx.Bool(mode="output"),
            "show_rate_change":         hx.Bool(mode="output"), # careful with this it already existed
            "show_inflation":           hx.Bool(mode="output"),
            "show_premium_limit_prof":  hx.Bool(mode="output"),
            "show_cat":                 hx.Bool(mode="output"),
            "show_portfolio_profile":   hx.Bool(mode="output"),
            "show_own_experience":      hx.Bool(mode="output"),
            "show_lloyds_proj":         hx.Bool(mode="output"),
            "show_beazley_proj":        hx.Bool(mode="output"),
            "show_bp_proj":             hx.Bool(mode="output"),
            "show_anti_select":         hx.Bool(mode="output"),
            "show_uncertainty":         hx.Bool(mode="output"),
            "show_pc":                  hx.Bool(mode="output"),
            "show_rat_sum_std":         hx.Bool(mode="output"),
            "show_rat_sum_bbt":         hx.Bool(mode="output"),
            "show_rat_sum_case":        hx.Bool(mode="output"),
            "show_kpi":                 hx.Bool(mode="output"),
            "show_rationale":           hx.Bool(mode="output"),
            "show_something_broke":     hx.Bool(mode="output"),
            "show_json_view":           hx.Bool(mode="output"),
            "show_timer":               hx.Bool(mode="output"),

            "show_after_landing_page": hx.Bool(mode="output"),
            "landing_page_info": hx.Str(
                mode="input", 
                default="Enter an Hx policy option ID below if diffferent from expiring and click 'Start Policy'",
                async_output=["start_renewal_task"],
                view={"read_only":True}
            ),
            "expiring_policy_option_id": hx.Int(mode="input", default=None, optionality="optional", async_output=["start_renewal_task", "sync_expiring_ids"]),
        }),
        "bug_report_email": hx.Str(mode="output")
    }