import hx_data_schema as hx



def spatialkey():
    return {
        "spatialkey": hx.Structure(children={
            "fetch_status": hx.Str(mode="input", optionality="optional", default=None, async_output=["run_spatialkey_task"], view={"label": "Fetch Status", "read_only": True, "multiline": True}),
            "csv_status": hx.Str(mode="output", view={"label": "Spatialkey Task Status"}),
            "job_id": hx.Str(mode="input", optionality="optional", default=None, async_input=["open_spatialkey_dashboard_task"], async_output=["run_spatialkey_task"], view={"label": "Spatial Key Job ID", "read_only": True}),
            "dataset_id": hx.Str(mode="input", optionality="optional", default=None, async_input=["open_spatialkey_dashboard_task"],  async_output=["run_spatialkey_task"], view={"label": "Spatial Key Dataset ID", "read_only": True}),
            "dashboard_note": hx.Str(mode="input", optionality="optional", default=None, async_output=["open_spatialkey_dashboard_task"], view={"label": "Spatial Key Dashboard", "read_only": True, "multiline": True}),
        })
    }