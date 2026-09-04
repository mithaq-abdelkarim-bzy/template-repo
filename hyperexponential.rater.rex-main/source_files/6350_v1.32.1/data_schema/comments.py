import hx_data_schema as hx
from data_schema.utilities import set_node_properties

def comments():
    '''
    Data schema for comments section in page policy info
    '''
    return {
        "comments": hx.Structure(children={
            "comments_table": hx.List(mode="output", async_input=["start_add_comments_task"], async_output=["add_new_comment_task"], children={
                "comment": hx.Str(mode="input", optionality="optional", default=None, async_input=["start_add_comments_task"], async_output=["add_new_comment_task"], view={"label": "Comments", "read_only": True}),
                "created_date": hx.Date(mode="input", optionality="optional", default=None, async_input=["start_add_comments_task"], async_output=["add_new_comment_task"], view={"label": "Created Date", "read_only": True}),
                "created_by": hx.Str(mode="input", optionality="optional", default=None, async_input=["start_add_comments_task"], async_output=["add_new_comment_task"], view={"label": "Created By", "read_only": True})
            }),
            "comment_input_box": hx.Str(mode="input", default="", async_input=["add_new_comment_task"], async_output=["start_add_comments_task"]),
            "show_comment_input_box": hx.Bool(mode="input", default=False, async_output=["add_new_comment_task", "start_add_comments_task"]),
            "hide_comment_input_box": hx.Bool(mode="input", default=True, async_output=["add_new_comment_task", "start_add_comments_task"]),
        })
    }