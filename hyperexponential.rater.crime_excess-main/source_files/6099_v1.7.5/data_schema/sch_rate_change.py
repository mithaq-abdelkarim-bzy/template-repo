import hx_data_schema as hx
import libraries.common_data_schema.data_schema.utilities as utils
import algorithms.utils_global_lists as lst
from algorithms.utils_functions import create_title

def sch_rate_change(cds):
    cds.extend_node_rater_defined("cds/layers/rate_change", {
        # Section Rate Change
        "expiring_policy_option_id": hx.Int(mode="override", async_input=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Policy Option", "format": {"thousandSeparated": False}}),
        "expiring_insured_name": hx.Str(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Insured Name"}),
        "expiring_premium": hx.Float(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Premium (Beazley's Share)", "format": utils.thousands_format(0)}),
        "expiring_brokerage": hx.Float(mode="input", default=0.15, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Brokerage/Commission", "format": utils.percent_format(1)}),
        "expiring_premium_comment": hx.Str(mode="input", default="", view={"label": "Comment"}),
        "expiring_beazley_share": hx.Float(mode="input", default=1, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Beazley Share", "format": utils.percent_format(0)}),
        "expiring_excess": hx.Float(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Attachment Point", "format": utils.thousands_format(0)}),
        "expiring_excess_social_engineering": hx.Float(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring SE Attachment Point", "format": utils.thousands_format(0)}),
        "expiring_excess_other_cov": hx.Float(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Other Cov Attachment Point", "format": utils.thousands_format(0)}),
        "expiring_limit": hx.Float(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Full Layer Limit", "format": utils.thousands_format(0)}),
        "expiring_limit_social_engineering": hx.Float(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Social Engineering Limit", "format": utils.thousands_format(0)}),
        "expiring_limit_other_cov": hx.Float(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Other Coverage Limit", "format": utils.thousands_format(0)}),
        "expiring_policy_term": hx.Float(mode="input", default=12, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Policy Term (months)"}),
        "expiring_premium_annual": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Annualized Premium"}),
        "expiring_revenue": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Annual Revenue", "format": utils.thousands_format(0)}),
        "expiring_assets": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Assets", "format": utils.thousands_format(0)}),
        "expiring_employees": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Number of Officers and Employees", "format": utils.thousands_format(0)}),
        "expiring_locations": hx.Int(mode="input", default=0, async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Number of Locations", "format": utils.thousands_format(0)}),
        "expiring_beazley_layer": hx.Str(mode="input", default="", async_output=["expiring_policy_fetch_task", "start_renewal_task"], view={"label": "Expiring Beazley Layer"}),


    })

    for rc_item in [item + "_change" for item in lst.rate_change_list_static] + ["rate_change"]:
        cds.override_node_properties(f"cds/layers/rate_change/{rc_item}/uw_selected", {
            "view": {"label": "Rate Change", "format": utils.percent_format(2)}
        })

def sch_rate_change_non_cds():
    return {
        "show_rate_change": hx.Bool(mode="output"),
        "expiring_policy_option_id": hx.Int(mode="output", async_input=["expiring_policy_fetch_task", "start_renewal_task"]),
    }