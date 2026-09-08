import hx_data_schema as hx

def sch_model_state():
    '''
    Internal Model State that controls the workflow
    '''
    return {
        "model_state": hx.Structure(children={

            "pressed_start_renewal_task": hx.Bool(mode="output", async_output=["start_renewal_task"]),
            "show_landing_page": hx.Bool(mode="output"),
            "show_airlines": hx.Bool(mode="output"),
            "show_ga": hx.Bool(mode="output"),

            "pressed_airlines_task": hx.Bool(mode="input", default=False, async_output=["show_airlines_task", "show_ga_task", "start_renewal_task"]),
            "pressed_ga_task": hx.Bool(mode="input", default=False, async_output=["show_airlines_task", "show_ga_task", "start_renewal_task"]),
            "pressed_either_task": hx.Bool(mode="output"),
            "has_sql_conn_failed": hx.Bool(mode="input", default=False, async_output=["show_airlines_task", "show_ga_task", "start_renewal_task"]),
            "sql_failure_msg": hx.Str(mode="input", default="❗❗ Failed to connect to SQL database. Please proceed and enter data manually. ❗❗", view={"read_only": True}),
            
            "is_product_inconsistent": hx.Bool(mode="output"),
            "inconsistent_product_msg": hx.Str(mode="input", default="❗❗ Inconsistent product selected and model shown. Please return to 'Risk Information' and select 'Airlines' or 'General Aviation' correctly. ❗❗"),
            "show_after_landing_page": hx.Bool(mode="output"),

            "show_rate_change": hx.Bool(mode="output"),
            
            "import_expiry_prompt": hx.Str(mode="input", default="Click on 'Import Expiring Policy Data' in the top right corner to import the expiring information.", view={"read_only": True}),

            "landing_page_info": hx.Str(mode="input", default="Click on 'Start Policy' to load the model.", async_output=["start_renewal_task"], view={"read_only": True}),
            "has_import_failed": hx.Bool(mode="output", async_output=["start_renewal_task"]),

            "expiring_policy_option_id": hx.Int(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=["start_renewal_task", "sync_expiring_ids"])
        })
    }