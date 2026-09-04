import hx_data_schema as hx

def exposure_management_api():
    return {
        "exposure_management_api": hx.Structure(children={
            "limit_results": hx.Int(mode="input", default=10, optionality="optional", view={"label": "Rows to Return"}, async_input=["search_exposure_management_data_task"]),
            "inputs": hx.Structure(children={
                "team": hx.Str(mode="input", default="", options_table="exposure_management_api_teams", options_column="team", async_input=["search_exposure_management_data_task"], view={"label": "Team"}),
                "accgrpid": hx.Str(mode="input", optionality="optional", default="", async_input=["search_exposure_management_data_task", "import_accgrpid_only_task"], view={"label": "Account Group Id"}),
                "reference": hx.Str(mode="input", optionality="optional", default="", async_input=["search_exposure_management_data_task"], view={"label": "Reference"}),
                "perspcode": hx.Str(mode="input", optionality="optional", default="", async_input=["search_exposure_management_data_task"], view={"label": "Persp Code"}),
                "account_name": hx.Str(mode="input", optionality="optional", default="", async_input=["search_exposure_management_data_task"], view={"label": "Account Name"})
            }),
            "search_fetch_status": hx.Str(mode="input", optionality="optional", default=None, async_output=["search_exposure_management_data_task"], view={"label": "Exposure Management API Status", "read_only": True}),
            "search_results": hx.List(mode="input", async_input=["pull_in_exposure_management_data_task"], async_output=["search_exposure_management_data_task"], children={
                "accgrpid": hx.Str(mode="input", optionality="optional", default=None, async_input=["pull_in_exposure_management_data_task"], async_output=["search_exposure_management_data_task"], view={"label": "accgrpid", "read_only": True}),
                "reference": hx.Str(mode="input", optionality="optional", default=None, async_input=["pull_in_exposure_management_data_task"], async_output=["search_exposure_management_data_task"], view={"label": "Reference", "read_only": True}),
                "account_number": hx.Str(mode="input", optionality="optional", default=None, async_input=["pull_in_exposure_management_data_task"], async_output=["search_exposure_management_data_task"], view={"label": "Account Number", "read_only": True}),
                "account_name": hx.Str(mode="input", optionality="optional", default=None, async_input=["pull_in_exposure_management_data_task"], async_output=["search_exposure_management_data_task"], view={"label": "Account Name", "read_only": True}),
                "num_locs": hx.Str(mode="input", optionality="optional", default=None, async_input=["pull_in_exposure_management_data_task"], async_output=["search_exposure_management_data_task"], view={"label": "Loc Count", "read_only": True}),
                "last_edit": hx.Date(mode="input", optionality="optional", default=None, async_input=["pull_in_exposure_management_data_task"], async_output=["search_exposure_management_data_task"], view={"label": "Last Edit", "read_only": True}),
                "selected": hx.Bool(mode="input", async_input=["pull_in_exposure_management_data_task"], default=False, view={"label": "Import"})
            }),
            "location_fetch_status": hx.Str(mode="input", optionality="optional", default=None, async_output=["pull_in_exposure_management_data_task"], view={"label": "Exposure Management API Status", "read_only": True}),
            # For simulation ELT search
            "simulation_fetch_status": hx.Str(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "Simulation Status", "read_only": True}),
    })
    }