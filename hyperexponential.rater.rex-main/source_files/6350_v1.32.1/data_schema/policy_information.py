import hx_data_schema as hx
from data_schema.utilities import thousands_format, set_node_properties, run_schedule_rater_async_tasks

def policy_information():
    # Section Policy Information
    policy_information_schema = hx.Structure(children={
        "insured": hx.Str(mode="input", default = None, optionality="optional", async_input=["generate_quote_doc_task", "check_remodel_task"], async_output=["import_firm_task", "start_renewal_task"], view={"options": {"read_only": {"read_only": True}},"label": "Insured"}),
        "version_comment": hx.Str(mode="input", default="", view={"label": "Version Comment"}),
        "underwriter": hx.Str(mode="input", default=None, optionality="optional", options_table="team", options_column="Initials",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["start_renewal_task", "run_simulation_task", "check_remodel_task"], view={"label": "Underwriter"}),
        "team": hx.Str(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task", "case_pricing_calc_tech_premium_task"], view={"label": "Team"}),
        "is_om": hx.Bool(mode="output"),
        "is_nacp": hx.Bool(mode="output"),
        "uw_office": hx.Str(mode="output", view={"label": "UW Office"}),
        # "policy_length": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True) + ["expiring_policy_fetch_task"], view={"label": "Policy Length (Years)", "format": thousands_format(mantissa=3)}),
        "policy_length": hx.Float(mode="override", async_input=run_schedule_rater_async_tasks(async_input = True) + ["expiring_policy_fetch_task", "case_pricing_calc_tech_premium_task"], view={"label": "Policy Length (Years)", "format": thousands_format(mantissa=3)}),
        "bi_waiting_period": hx.Int(mode="override", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "BI Waiting Period"}),
        "bi_indemnity_period": hx.Int(mode="override", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "BI Indemnity Period"}),
        "broker_branch": hx.Str(mode="input", default="", view={"label": "Broker Branch"}),
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),
        "website": hx.Str(mode="input", default="", view={"label": "Website"}),
        "cbi": hx.Str(mode="input", options_table="cbi", options_column="CBI", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "CBI"}),
        "lead_follow": hx.Str(mode="input", default=None, optionality="optional", options=["Lead", "Follow"], view={"label": "Lead/Follow"}),
        "slip_currency": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task","pull_exchange_rate_claim_data_task"], options_table="currency", options_column="currency", default="USD", view={"label": "Currency"}),
        "exchange_rate_date": hx.Str(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "Exchange Rate Date", "read_only": True}), # TODO: Should this be overwritable? 
        "exchange_rate": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task", "case_pricing_calc_tech_premium_task"], view={"label": "Exchange Rate", "read_only": True, "format": thousands_format(mantissa=3)}),
        "accgrpid": hx.Str(mode="input", default=None,  optionality="optional", async_input=["run_simulation_task", "check_remodel_task"], async_output=["pull_in_exposure_management_data_task", "import_accgrpid_only_task", "start_renewal_task"], view={"label": "Accgrpid"}),
        "account_group_name": hx.Str(mode="input", default=None,  optionality="optional", async_output=["pull_in_exposure_management_data_task", "start_renewal_task"], view={"label": "Account Group Name"}),
        "mexican_fonden": hx.Bool(mode="input", default=False, async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Mexican Fonden"}),
        "large_schedule_model": hx.Bool(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_spatialkey_task", "run_simulation_task", "pull_in_exposure_management_data_task"], default=False, view={"label": "Use Large Schedule Model?"}),
        "small_schedule_model": hx.Bool(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_spatialkey_task", "run_simulation_task", "produce_heatmap_task", "produce_climate_map_task","generate_climate_doc_task"], view={"label": "Use Small Schedule Model?"}),
        "fac_powerapp_note": hx.Str(mode="output", view={"label": "Fac PowerApp link"}),
        "user_guide_note": hx.Str(mode="output", view={"label": "User Guide Link"}),
        "insured_search": hx.Structure(children={
            "firmid_input": hx.Int(mode="input", optionality="optional", default=None, async_input=["search_firm_task"], view={"label": "Firm ID"}),
            "firmname_input": hx.Str(mode="input", optionality="optional", default=None, async_input=["search_firm_task"], view={"label": "Insured"}),
            "custom_firmname": hx.Str(mode="input", optionality="optional", default=None, async_input=["import_firm_task"], view={"label": "Custom Insured", "info": "Entering overrides search result"}),
            "search_result": hx.List(mode="output", async_output=["search_firm_task"], async_input=["import_firm_task"], children={
                "firm_id": hx.Int(mode="input", optionality="optional", default=None, async_output=["search_firm_task"], async_input=["import_firm_task"], view={"label": "Firm ID", "read_only": True, "format": {"thousandSeparated": False}}),
                "firm_name": hx.Str(mode="input", optionality="optional", default=None, async_output=["search_firm_task"], async_input=["import_firm_task"], view={"label": "Insured", "read_only": True}),
                "selected": hx.Bool(mode="input", default=False, async_output=["search_firm_task"], async_input=["import_firm_task"], view={"label": "Selected"})
            }),
        }),
        "policy_level_validation": hx.Bool(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True)),
        # TODO: move to non-layer-perils
        "top_20_sort_by": hx.Str(mode="input", options=["TIV", "Expected Loss"], default="Expected Loss", view={"label": "Top 20 Metric"}, async_input=run_schedule_rater_async_tasks(async_input = True)),
        "doesnt_require_validation": hx.Structure(children={
            **{f"{peril}": hx.Bool(mode="output") for peril in ["fire", "named_windstorm", "scs", "flood", "quake", "wildfire"]},
        }),
        "requires_validation": hx.Structure(children={
            **{f"{peril}": hx.Bool(mode="output") for peril in ["fire", "named_windstorm", "scs", "flood", "quake", "wildfire"]},
        }),
        "notifications": hx.Structure(children={
            "notification_box": hx.Str(mode="output"),
            "show_notifications": hx.Bool(mode="output"),
            "show_hide": hx.Bool(mode="input", async_output = [{"task": "show_hide_notifications_task", "reset": False}], default=True),
            "notifications_populated": hx.Bool(mode="output")
        }),
        "is_case_priced": hx.Bool(mode="input", default=False, async_input=["run_schedule_rater_task","remove_experience_adjustment_task", "save_case_pricing_results_task"], view={"label": "Risk Case Priced (Actuary Use Only)"}),
        "case_pricing_note": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Case Pricing Note"}),
        "case_pricing_info": hx.Str(mode="input", default= "**Info**\nPopulate results from case pricing below and press button _Run Rater_.\n\nPlease ensure that the TIV's entered into the schedule are of the same currency.\n\nThere are two ways to complete.\n1. Input case priced technical premium, expected losses and TP breakdown and rate change below. Press button _Save Case Pricing Results_ to commit to model.\n2. Input **expected losses**, 1 in 250 & 1 in 10 **marginal impact**, **RI costs** and rate change. Press _Calculate Technical Premium_ button to populate other fields. Then _Save Case Pricing Results_ to commit to model.", view={"label": "Case Pricing Note", "read_only": True}),
    })

    return {"policy_information": policy_information_schema}