import hx_data_schema as hx
from data_schema.utilities import thousands_format, percent_format

def model_state():
    '''
    Internal Model State that controls the workflow
    '''
    return {
        "model_state": hx.Structure(children={
            "pressed_start_renewal_task": hx.Bool(mode="input", optionality="optional", default=None, async_output=["start_renewal_task"], view={"read_only": True}),
            "show_landing_page": hx.Bool(mode="output"),
            "show_after_landing_page": hx.Bool(mode="output"),
            "expiring_policy_option_id": hx.Int(mode="input", default=None, async_output=["start_renewal_task", "sync_expiring_ids"], optionality="optional"),
            "intl_ded_message": hx.Str(mode="input", default="These deductibles apply to all layers. \nBlank international deductibles below will default to the per occurance deductibles above by peril.\nSublimits are ground up.", view={"label": "Team", "options": {"read_only": {"read_only": True}}}),
            "min_ded_label": hx.Str(mode="output"),
            "max_ded_label": hx.Str(mode="output"),
            "sublimit_label": hx.Str(mode="output")
        }),
        "control": hx.Structure(children={
            "show_additional_coverages_page": hx.Bool(mode="output"),
            "show_wrt_line": hx.Bool(mode="output"),
            "show_wrt_line_validation": hx.Bool(mode="output"),
            "show_affirmative_cyber": hx.Bool(mode="output"),
            "show_ensuing_loss_cyber": hx.Bool(mode = "output"),
            "show_cyber_premium": hx.Bool(mode = "output"),
            "show_run_rater_warning": hx.Bool(mode = "input", optionality="optional", default=False, async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"read_only": True})
        }),
        "info": hx.Structure(children={
            "machinery_breakdown_msg": hx.Str(mode="output"),
            "equipment_breakdown_msg": hx.Str(mode="output"),
            "remodelling_info_msg": hx.Str(mode="output"),
            "remodel_msg": hx.Str(mode="input", optionality="optional", default=None, async_output=['check_remodel_task'], view={"read_only": True}),
            "remodelling_needed": hx.Bool(mode="input", default=False, async_output=["check_remodel_task"]),
            "remodelling_not_needed": hx.Bool(mode="input", default=True, async_output=["check_remodel_task"]),
            "run_rater_warning": hx.Str(mode="input", optionality="optional", default=None, async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"read_only": True}),
            "cat_limit_framwork_msg": hx.Str(mode="output", async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}]),
            "deductible_info": hx.Str(mode="output")
        }),
        "email": hx.Structure(children={
            "remodelling_check_file": hx.File(mode="output", async_output=["check_remodel_task"], file_name="Remodelling_Check.eml", view={"label": "Click to download the remodelling check results"}),
            "sender": hx.Str(mode="input", default="your_uw@beazley.com", async_input=["check_remodel_task"], async_output=[{"task": "check_remodel_task", "reset": True}], view={"label": "Sender"}),
            "recipient": hx.Str(mode="input", default="uw_assistant@beazley.com", async_input=["check_remodel_task"], async_output=[{"task": "check_remodel_task", "reset": True}], view={"label": "Recipient"})
        }),
        "df_output": hx.File(mode="output", file_name="df.csv", async_output=["run_schedule_rater_task", "save_case_pricing_results_task","remove_experience_adjustment_task"]),
    }