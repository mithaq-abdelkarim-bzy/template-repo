import hx_data_schema as hx

def elt_api():
    return {
        "elt_api": hx.Structure(children={
            "inputs": hx.Structure(children={
                "accgrpid": hx.Str(mode="input", optionality="optional", default="261324", async_input=["pull_elt_data_task"], view={"label": "Account Group Id"}),
                "perspcode": hx.Str(mode="input", optionality="optional", default="GU", async_input=["pull_elt_data_task"], view={"label": "Persp Code"}),
            }),
            "elt_fetch_status": hx.Str(mode="output", async_output=["pull_elt_data_task"], view={"label": "Exposure Management API Status"}),
            "elt_results": hx.List(mode="input", async_output=["pull_elt_data_task"], children={
                "anlsid": hx.Str(mode="output", async_output=["pull_elt_data_task"], view={"label": "Analysis ID"}),
                "name": hx.Str(mode="output", async_output=["pull_elt_data_task"], view={"label": "Name"}),
                "event_id": hx.Str(mode="output", async_output=["pull_elt_data_task"], view={"label": "Event ID"}),
                "rate": hx.Str(mode="output", async_output=["pull_elt_data_task"], view={"label": "Rate"}),
                "perspvalue": hx.Str(mode="output", async_output=["pull_elt_data_task"], view={"label": "Persp Value"}),
                "stddevi": hx.Str(mode="output", async_output=["pull_elt_data_task"], view={"label": "Std Dev I"}),
                "stddevc": hx.Str(mode="output", async_output=["pull_elt_data_task"], view={"label": "Std Dev C"}),
                "expvalue": hx.Bool(mode="input", async_output=["pull_elt_data_task"], default=False, view={"label": "Exp Value"}),
                "peril": hx.Str(mode="output", async_output=["pull_elt_data_task"], view={"label": "Peril"}),
            }),
    })
    }

