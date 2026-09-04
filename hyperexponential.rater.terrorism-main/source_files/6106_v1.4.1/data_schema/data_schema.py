import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_exposure_details import sch_exposure_details
from data_schema.sch_rating_summary import sch_rating_summary
from data_schema.sch_rate_change import sch_rate_change
from data_schema.sch_rater_defined import sch_rater_defined, ihs_risk_names
from data_schema.sch_rationale import sch_rationale
from data_schema.sch_show_hide import sch_show_hide

from data_schema.sch_model_state import sch_model_state
import algorithms.rate_constants as c
from libraries.email_notification.data_schema.bug_report_schema import bug_report


def sch_common_data_schema():
    cds = CommonDataSchema()

    sch_rater_defined(cds)
    sch_risk_information(cds)
    sch_exposure_details(cds)
    # sch_experience_rating(cds)
    sch_rating_summary(cds)
    sch_rate_change(cds)
    sch_rationale(cds)
    sch_show_hide(cds)
    # sch_quote_summary(cds)

    return cds.get_data_schema()


@hx.data_schema
def data_schema():
    ihs_nodes = {
        "country_code": hx.Str(  mode="output", view={"label": "Country Code"}),
        "risk_name":    hx.Str(  mode="output", view={"label": "Name"}),
        "value":        hx.Float(mode="output", view={"label": "Value"}),
        "updated_on":   hx.Date( mode="output", view={"label": "Updated On"}),
        "description":  hx.Str(  mode="output", view={"label": "Description"}),
    }

    return hx.Structure(children={
        **sch_common_data_schema(),
        **sch_model_state(),
        **bug_report(),
        # hx core - modifying to allow for async_inputs
        "hx_core": hx.Structure(view={"label": "Hx Core"}, children={
            "inception_date":   hx.Date(default="2018-01-01", mode="input", async_input=["task_fetch_ihs_data","rarc_task","start_renewal_task"], view={"label": "Inception Date"}),
            "expiry_date":      hx.Date(default="2018-12-31", mode="input", async_input=["rarc_task"], view={"label": "Expiry Date"}),
        }),
        
        # IHS data
        "ihs": hx.List(mode="input", async_input=["rarc_task"], async_output=["task_fetch_ihs_data","start_renewal_task"], children={
            "country_code": hx.Str(  mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=["task_fetch_ihs_data","start_renewal_task"], view={"label": "Country Code"}),
            "risk_name":    hx.Str(  mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=["task_fetch_ihs_data","start_renewal_task"], view={"label": "Name"}),
            "value":        hx.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=["task_fetch_ihs_data","start_renewal_task"], view={"label": "Value"}),
            "updated_on":   hx.Date( mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=["task_fetch_ihs_data","start_renewal_task"], view={"label": "Updated On"}),
            "description":  hx.Str(  mode="input", default=None, optionality="optional", async_input=["rarc_task"], async_output=["task_fetch_ihs_data","start_renewal_task"], view={"label": "Description"}),
        }),
        **{f"ihs_{k}": hx.List(mode="output", children=ihs_nodes) for k in ihs_risk_names.keys()},
        "ihs_descriptions": hx.List(mode="output", children={
            "risk_name":        hx.Str(mode="output", view={"label": "Risk Name"}),
            "description":      hx.Str(mode="output", view={"label": "Latest Description"})
        }),
        "ihs_countries_retrieved": hx.Str(mode="input", default="", async_input=["rarc_task"], async_output=["task_fetch_ihs_data","start_renewal_task"]),
        
        "rate_change": hx.Structure(children={
            "countries": hx.Str(mode="output", async_input=["rarc_task"])
        }),

        # Policy document download
        "policy_doc": hx.Structure(children={
            "output_file":          hx.File(mode="output", async_output=["task_policy_to_excel"], file_name="Policy_Summary.xlsx"),
            "data_dict":            hx.Str( mode="output", async_input =["task_policy_to_excel"] ),
            "task_data_dict":       hx.Str( mode="output", async_output=["task_policy_to_excel"]),
            "show_generate_button": hx.Bool(mode="output"),
            "show_download":        hx.Bool(mode="output"),
            "premium_check":        hx.Str( mode="output"),
            "show_premium_check":   hx.Bool(mode="output"),
        }),
        
        # Debugging
        "debug_str": hx.Str(mode="output"),

        "live_hxd":  hx.Bool(mode="output", view={"label": "hxd live = True; hxd transient= False"}   ),

    })

