# v0.5.0
import hx_data_schema as hx
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import coverages_dict , max_coverages

def sch_model_state():
    '''
    Internal Model State that controls the workflow
    '''
    return {
        "model_state": hx.Structure(children={
            "pressed_start_renewal_task": hx.Bool(mode="output", async_output=["start_renewal_task"]),
            "show_landing_page": hx.Bool(mode="output"),
            "show_after_landing_page": hx.Bool(mode="output"),
            "show_rate_change": hx.Bool(mode="output"),
            "landing_page_info": hx.Str(
                mode="input",
                default="Click the 'import expiring policy data' arrow in the top right corner then click **Start Policy**. ",
                async_output=["start_renewal_task"],
                view={"read_only":True}
            ),
            "expiring_policy_option_id": hx.Int(mode="input", default=None, optionality="optional", async_output=["start_renewal_task", "sync_expiring_ids"]),
            
            "coverage_use": hx.Bool(mode="output"), # NOTE: related to the premium calculation. Required for governance # Edit v0.3.0
            "insured_asset_use": hx.Bool(mode="output"), # NOTE: related to the premium calculation. Required for governance # Edit v0.3.0
            "show_rate_change_layer_no_ia_use": hx.Bool(mode="output"),
            "layer_no_ia_use": hx.Bool(mode="output"),
            
        }),
        "bug_report_email": hx.Str(mode="output"),

        "policy_doc": hx.Structure(children={
            "data_dict": hx.Str(mode="output", async_input=["policy_to_excel_task"]),
            "output_file": hx.File(mode="output", async_output=["policy_to_excel_task"], file_name="Policy_Summary.xlsx"),
            "task_data_dict": hx.Str(mode="output", async_output=["policy_to_excel_task"]),
            "show_generate_button": hx.Bool(mode="output"),
            "show_download": hx.Bool(mode="output"),
            "premium_check": hx.Str(mode="output"),
            "show_premium_check": hx.Bool(mode="output"),

        }),

        "page_info": hx.Structure(children={
            "rate_change": hx.Structure(children={
                "notification_flag": hx.Bool(mode="output"),
                "notification_text": hx.Str(mode="output"),

            }),
        })

    }