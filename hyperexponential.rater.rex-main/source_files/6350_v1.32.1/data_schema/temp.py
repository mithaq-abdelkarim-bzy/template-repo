import hx_data_schema as hx
from data_schema.utilities import run_schedule_rater_async_tasks

def temp_storage():
    return {
        "temp": hx.Structure(children={
            "comments": hx.Structure(children={
                "comments_table": hx.List(mode="output", async_input=["add_new_comment_task"], async_output=["start_add_comments_task"], children={
                    "comment": hx.Str(mode="input", optionality="optional", default=None, async_input=["add_new_comment_task"], async_output=["start_add_comments_task"], view={"label": "Comments", "read_only": True}),
                    "created_date": hx.Date(mode="input", optionality="optional", default=None, async_input=["add_new_comment_task"], async_output=["start_add_comments_task"], view={"label": "Created Date", "read_only": True}),
                    "created_by": hx.Str(mode="input", optionality="optional", default=None, async_input=["add_new_comment_task"], async_output=["start_add_comments_task"], view={"label": "Created By", "read_only": True})
                }),
            }),
            "output_json": hx.Str(mode="input", default="", async_output=run_schedule_rater_async_tasks(async_input = False)),
            "simulation_validation_json": hx.Str(mode="input", default="", async_output= ["run_simulation_task"]),
            "schedule_file": hx.File(mode="output", file_name="schedule.csv", async_input=["load_from_schedule_task", "load_into_debug_task"], async_output=["push_file_to_temp_task", "push_df_to_temp_task"], view={"label": "Large Schedule EM"}),
        })
    }