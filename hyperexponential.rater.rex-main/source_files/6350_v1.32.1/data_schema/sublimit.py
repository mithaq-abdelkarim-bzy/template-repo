import hx_data_schema as hx
from data_schema.utilities import thousands_format, run_schedule_rater_async_tasks

def sublimit():
    '''
    Data schema for sublimits related input
    '''
    return {
        "sublimit": hx.Structure(children={
            "scs_sublimit": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["generate_quote_doc_task"], view={"label": "SCS Sublimit", "format": thousands_format()}),
            "ws_sublimit": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["generate_quote_doc_task", "run_simulation_task"], view={"label": "Windstorm Sublimit", "format": thousands_format()}),
            "eq_sublimit": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["generate_quote_doc_task", "run_simulation_task"], view={"label": "Earthquake Sublimit", "format": thousands_format()}),
            "fl_sublimit": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["generate_quote_doc_task"], view={"label": "Flood Sublimit", "format": thousands_format()}),
            "sublimit_warning": hx.Str(mode="output"),
        }),
    }