import hx_data_schema as hx
from data_schema.utilities import set_node_properties, run_schedule_rater_async_tasks

def core():
    '''
    Overriding the exisiting hx core
    '''
    core_schema = hx.Structure(children={
        "inception_date": hx.Date(default="2018-01-01", mode="input", view={"label": "Inception Date"}),
        "expiry_date": hx.Date(default="2018-12-31", mode="input", view={"label": "Expiry Date"}),
        "model_premium": hx.Float(mode="output", view={"label": "Model Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "charged_premium": hx.Float(mode="output", view={"label": "Charged Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "premium_currency": hx.Str(mode="output", view={"label": "Premium Currency"}),
        "ulr": hx.Float(mode="output", view={"label": "ULR", "format": {"output": "percent", "mantissa": 1}}),
        "class_code": hx.Str(mode="output", view={"label": "Class Code"}),
    })

    set_node_properties(core_schema, ["inception_date"], async_input=run_schedule_rater_async_tasks(async_input = True) + ["generate_quote_doc_task", "generate_flood_climate_metrics_task"])
    set_node_properties(core_schema, ["expiry_date"], async_input=["generate_quote_doc_task"])
    set_node_properties(core_schema, ["charged_premium"], async_input=["generate_quote_doc_task"])
    return {"hx_core": core_schema}
