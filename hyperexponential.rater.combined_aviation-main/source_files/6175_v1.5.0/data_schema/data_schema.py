import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_exposure_details import sch_exposure_details
from data_schema.sch_experience_rating import sch_experience_rating
from data_schema.sch_rate_change import sch_rate_change
from data_schema.sch_rating_summary import sch_rating_summary
from data_schema.sch_quote_summary import sch_quote_summary
from data_schema.sch_rater_defined import sch_rater_defined
from data_schema.sch_model_state import sch_model_state
from libraries.email_notification.data_schema.bug_report_schema import bug_report


def sch_common_data_schema():
    cds = CommonDataSchema()

    sch_rater_defined(cds)
    sch_risk_information(cds)
    sch_rating_summary(cds)
    sch_quote_summary(cds)
    sch_exposure_details(cds)
    sch_experience_rating(cds)
    sch_rate_change(cds)

    return cds.get_data_schema()


@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **sch_model_state(),
        **bug_report(),
        # hx core - modifying to allow for async_inputs
        "hx_core": hx.Structure(children={
            "inception_date": hx.Date(default="2018-01-01", mode="input", async_input=["rarc_task", "start_renewal_task", "show_airlines_task", "show_ga_task"], view={"label": "Inception Date"}),
            "expiry_date": hx.Date(default="2018-12-31", mode="input", async_input=["rarc_task", "start_renewal_task", "show_airlines_task", "show_ga_task"], view={"label": "Expiry Date"}),
        }, view={"label": "Hx Core"}),
        # SQL data
        "sql_db": hx.Structure(children={
            "operators": hx.List(mode="input", async_output=[{"task": "search_for_operator_task", "reset": False}, "get_sql_inputs_task", "show_airlines_task", "show_ga_task"], children={
                "operator": hx.Str(mode="input", async_output=[{"task": "search_for_operator_task", "reset": False}, "get_sql_inputs_task", "show_airlines_task", "show_ga_task"], default=None, optionality="optional")
            }),
            "registrations": hx.List(mode="input", async_output=["get_sql_inputs_task", "show_airlines_task", "show_ga_task"], children={
                "registration": hx.Str(mode="input", async_input=["get_selected_regs_task"], async_output=["get_sql_inputs_task", "show_airlines_task", "show_ga_task"], default=None, optionality="optional")
            }),
            "master_series": hx.List(mode="input", async_output=["get_sql_inputs_task", "show_airlines_task", "show_ga_task"], children={
                "aircraft_master_series": hx.Str(mode="input", async_output=["get_sql_inputs_task", "show_airlines_task", "show_ga_task"], default=None, optionality="optional")
            }),
            "has_duplicate_regs": hx.Bool(mode="output", async_output=["fetch_by_registration_task", "get_selected_regs_task"]),
            "duplicate_regs_msg": hx.Str(mode="input", default="❗❗ Duplicate registrations found. Please select which ones to keep. ❗❗", view={"read_only": True}),
            "is_at_least_one_reg_selected": hx.Bool(mode="output"),
            "duplicate_regs_selected_msg": hx.Str(mode="output"),
            "are_duplicate_regs_selected": hx.Bool(mode="output"),
            "are_regs_selected": hx.Bool(mode="input", default=True, async_output=["fetch_by_registration_task", "get_selected_regs_task"]),
            "duplicate_regs": hx.List(mode="input", async_input=["get_selected_regs_task"], async_output=["fetch_by_registration_task"], children={
                "is_selected": hx.Bool(mode="input", async_input=["get_selected_regs_task"], default=False, view={"label": "Keep?"}),
                "registration": hx.Str(mode="output", async_input=["get_selected_regs_task"], async_output=["fetch_by_registration_task"], view={"label": "Registration"}),
                "aircraft_family": hx.Str(mode="output", async_input=["get_selected_regs_task"], async_output=["fetch_by_registration_task"], view={"label": "Aircraft Family"}),
                "operator": hx.Str(mode="output", async_input=["get_selected_regs_task"], async_output=["fetch_by_registration_task"], view={"label": "Operator"}),
                "serial_number": hx.Str(mode="output", async_input=["get_selected_regs_task"], async_output=["fetch_by_registration_task"], view={"label": "Serial Number"}),
            }),
        }),
        # Expiring claims data
        "expiring_claims": hx.Str(mode="output", async_input=["show_airlines_task", "show_ga_task"], async_output=["start_renewal_task"]),
        # Rate change data
        "rate_change": hx.Structure(children={
            "airlines": hx.Str(mode="output", async_input=["rarc_task"]),
            "aircrafts": hx.Str(mode="output", async_input=["rarc_task"]),
            "expiring_aircrafts": hx.Str(mode="output", async_output=["start_renewal_task"])
        }),
        # Policy document download
        "policy_doc": hx.Structure(children={
            "output_file": hx.File(mode="output", async_output=["quote_to_excel_task"], file_name="Results_Summary.xlsx"),
            "data_dict": hx.Str(mode="output", async_input=["quote_to_excel_task"]),
            "task_data_dict": hx.Str(mode="output", async_output=["quote_to_excel_task"]),
            "show_generate_button": hx.Bool(mode="output"),
            "show_download": hx.Bool(mode="output"),
            "premium_check": hx.Str(mode="output"),
            "show_premium_check": hx.Bool(mode="output"),
        }),
        # Debugging
        "debug_str": hx.Str(mode="output"),
        "debug_str2": hx.Str(mode="output", async_output=["test_task"]),
        "debug_bool": hx.Bool(mode="input", default=False, async_output=[]),
        # **file_dict
    })

