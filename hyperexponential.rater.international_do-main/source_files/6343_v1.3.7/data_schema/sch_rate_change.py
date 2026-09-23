import hx_data_schema as hx
import data_schema.sch_utilities as utils
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers

### --- DEFINE GENERIC TASKS NAME --- ###
rarc_tasks_names = ["expiring_policy_fetch_task", "rarc_task"]

rarc_task_name = "rarc_task"

### --- DEFINE GENERIC STRUCTURE FOR LAYERS AND COVERAGES --- ###
def renewal_expiring(): 
    """
    Define common rate change fields used for generic rarc table
    """
    return {
    # "expiring": hx.Float(mode="output", async_output=rarc_tasks_names, view={"label": "Expiring", "format": thousands_format()}),
    "expiring": hx.Float(mode="output", view={"label": "Expiring", "format": thousands_format()}),
    "rebased_expiring": hx.Float(mode="output", view={"label": "Rebased\nExpiring", "format": thousands_format()}), 
    "renewal": hx.Float(mode="output", view={"label": "Renewal", "format": thousands_format()}),
    "expiring_revalued": hx.Float(mode="output", view={"label": "Expiring Revalued", "format": thousands_format()}), # Edit Addition v0.2.4.1-Dev - Amount converted in renewing currency use to handle change in currency at renewal.
}

def rc_quoted_premium(): 
    """
    Define common rate change fields for premiums used for generic rarc table
    """

    return {
        "premium": hx.Structure(children={
        "line_100pct": hx.Structure(children={
            "policy_term": hx.Structure(view={"label": 'Premium - Policy Term (100% Line)'}, children={**renewal_expiring()}), # EDIT Addition v0.2.4.1-Dev
            "annualised": hx.Structure(view={"label": 'Premium - Annualised (100% Line)'}, children={**renewal_expiring()})
        }),
        "beazley_line": hx.Structure(children={
            "policy_term": hx.Structure(view={"label": 'Premium - Policy Term (Beazley Line)'}, children={**renewal_expiring()}),
            "annualised": hx.Structure(view={"label": 'Premium - Annualised (Beazley Line)'}, children={**renewal_expiring()}),
        }),
    }),
}

def rc_expiring_info(): 
    """
    Define common Expiry rate change fields
    """
    return {
    "expiring_exposure": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_policy_length": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_quoted_premium_100": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_quoted_premium_annual_100": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_limit": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_excess": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_deductible": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_brokerage": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_written_line": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_expected_loss_100": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_section_reference": hx.Str(mode="output", async_output=rarc_tasks_names),
    "expiring_benchmark_premium_100": hx.Float(mode="output", async_output=rarc_tasks_names),
    # "expiring_benchmark_premium_post_uw_adj_100": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_bpi": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_currency": hx.Str(mode="output", async_output=rarc_tasks_names),
    "expiring_market_cap": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_total_assets": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_insider_share": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_mmp_flag": hx.Bool(mode="output", async_output=rarc_tasks_names),
    "expiring_employees": hx.Float(mode="output", async_output=rarc_tasks_names),

}

def rc_temp_storage(): 
    """
    Define common rate change fields to store premiums when running the RARC calculation.
    NOTE: The naming convention for these nodes does not align with the rest of the Data Schema. 
    Instead, they follow the naming conventions of the rate change library and are consistent with the values of "expiring_actual_prem" and "expiring_technical_prem".
    """
    return  {
    "quoted_premium": hx.Float(mode="output", async_output=[rarc_task_name]), # Same node name as rate change library. This node will be in line with the value of expiring_actual_prem
    "benchmark_premium": hx.Float(mode="output", async_output=[rarc_task_name]), # Same node name as rate change library. This node will be in line with the value of expiring_technical_prem
    "currency": hx.Str(mode="output", async_output=[rarc_task_name]),
}

def sch_rate_change(cds):
    """
    BUILD RATE CHANGE DATA SCHEMA FOR LAYERS
    """
    rarc_changes = {
        "exposure_change": {"label": "Exposure Change"},
        "risk_characteristics_change": {"label": "Risk Characteristics Change"},
        "limit_change": {"label": "Limit Change"},
        "deductible_change": {"label": "Deductible Change"},
        "terms_conditions_change": {"label": "Terms & Conditions Change"},
        "other_change": {"label": "Other Change"},
        "brokerage_change": {"label": "Brokerage Change"},
        "rate_change": {"label": "Risk Adjusted Rate Change"}
    }

    for change in rarc_changes.keys():
        # EDIT v0.2.4.1-Dev
        cds.override_node_properties(f"cds/layers/rate_change/{change}/model_calculated",{"view": {"label": "Model", "format": percent_format(1)},"async_output": [] if change == "rate_change" else [rarc_task_name]} )
        cds.override_node_properties(f"cds/layers/rate_change/{change}/uw_selected",{"view": {"label": "UW Selected", "format": percent_format(1)},"async_output": [] if change == "rate_change" else [{"task": rarc_task_name, "reset": False},"start_renewal_task"]} )  # added this to clear out the override on start of renewal but keep the selected value when Calculating Rate change again.
        cds.override_node_properties(f"cds/layers/rate_change/{change}/uw_override",{"view": {"label": "UW Override", "format": percent_format(1),"read_only": True} if change == "rate_change" else {"label": "UW Override", "format": percent_format(1)}})
        cds.override_node_properties(f"cds/layers/rate_change/{change}/final",{"view": {"label": "Final", "format": percent_format(1)}} )
        cds.override_node_properties(f"cds/layers/rate_change/{change}/comments",{"async_output": ["start_renewal_task"]} ) # added this to clear out the input on start of renewal.

    cds.override_node_properties(
        "cds/layers/rate_change/expiring_layer", 
        {  
            "async_input": ["expiring_policy_fetch_task", "rarc_task"],
            "async_output": [{"task": "start_renewal_task", "reset": False}],
            "options": [*range(1,max_layers+1)],
            "default": None
        } 
    )
    def expiring_and_renewal():
        """
        Define common rate change fields used for generic rarc table
        NOTE: add more fields if necessary
        """

        renewal_vs_expiry = [
            "limit",
            "deductible",
            "excess",
            "market_cap",
            "total_assets",
            "insider_share",
            "number_employees",
            "brokerage",
            "currency",
            "mmp_flag",
        ]

        renewal_vs_expiry_label = [
            "Limit",
            "Deductible",
            "Excess",
            "Market Cap",
            "Total Assets",
            "Insider Shareholder Share",
            "Number of Employees",
            "Brokerage",
            "Currency",
            "Middle Market",
        ]

        renewal_vs_expiry_format = [
            {"thousandSeparated": True, "mantissa": 0},
            {"thousandSeparated": True, "mantissa": 0},
            {"thousandSeparated": True, "mantissa": 0},
            {"thousandSeparated": True, "mantissa": 0},
            {"thousandSeparated": True, "mantissa": 0},
            {"output": "percent", "mantissa": 1},
            {"thousandSeparated": True, "mantissa": 0},
            {"output": "percent", "mantissa": 1},
            {},
            {},
        ]

        result={}

        for item, label, format_ in zip(
                renewal_vs_expiry, 
                renewal_vs_expiry_label,
                renewal_vs_expiry_format
            ):
            if item == "currency":
                result[item] = hx.Structure(view={"label": label}, children={
                    "renewal": hx.Str(mode="output", view={"label": "Renewal", "format": format_}),
                    "expiring": hx.Str(mode="output", view={"label": "Expiring", "format": format_}),
                    "expiring_revalued": hx.Str(mode="output", view={"label": "Expiring Revalued", "format": format_}), # Edit Addition v0.2.4.1-Dev - Amount converted in renewing currency use to handle change in currency at renewal.
                    })
            elif item == "mmp_flag":
                result[item] = hx.Structure(view={"label": label}, children={
                    "renewal": hx.Bool(mode="output", view={"label": "Renewal", "format": format_}),
                    "expiring": hx.Bool(mode="output", view={"label": "Expiring", "format": format_}),
                    "expiring_revalued": hx.Bool(mode="output", view={"label": "Expiring Revalued", "format": format_}), # Edit Addition v0.2.4.1-Dev - Amount converted in renewing currency use to handle change in currency at renewal.
                    }) 
            else:
                result[item] = hx.Structure(view={"label": label}, children={
                    "renewal": hx.Float(mode="output", view={"label": "Renewal", "format": format_}),
                    "expiring": hx.Float(mode="output", view={"label": "Expiring", "format": format_}),
                    "expiring_revalued": hx.Float(mode="output", view={"label": "Expiring Revalued", "format": format_}), # Edit Addition v0.2.4.1-Dev - Amount converted in renewing currency use to handle change in currency at renewal.
                    }) 

        return result    


    cds.extend_node_rater_defined("cds/layers/rate_change", {
        # "risk_adjusted_rate_change": hx.Float(mode="output", view={"label": "Final Risk Adjusted Rate Change", "format": percent_format()}), # EDIT v0.2.4.2-Dev removed since it has moved to CDS 1.3.0
        "risk_adjusted_rate_change_case_priced": hx.Float(mode="input", optionality='optional', default=None, view={"label": "Final Risk Adjusted Rate Change", "format": percent_format(), "options": {"read_only": {"read_only": True}}}),
        # "risk_adjusted_rate_change_gross_for_reporting": hx.Float(mode="output"), # EDIT v0.2.4.2-Dev removed since it has moved to CDS 1.3.0
        **rc_quoted_premium(),
        **expiring_and_renewal(),        
        "expiring_policy_info": hx.Structure(children={**rc_expiring_info()}),
        "error_message": hx.Str(mode="output"),
        "temp_storage": hx.Structure(children={**rc_temp_storage()}),
        # "new_layer": hx.Bool(mode="input", default=False, async_input= rarc_tasks_names, view={"label": "New Layer"}), # Edit Addition v0.2.4.1-Dev 
        "new_layer": hx.Bool(mode="output", view={"label": "New Layer"}), # Edit Addition v0.2.4.1-Dev 
        "renewing_layer": hx.Bool(mode="output",async_input= rarc_tasks_names), # Edit Addition v0.2.4.1-Dev 
        "show_expiring_revalued": hx.Bool(mode="output",async_input= rarc_tasks_names), # Edit Addition v0.2.4.1-Dev - Amount converted in renewing currency use to handle change in currency at renewal.
    })

    ### --- MODIFIED RATE CHANGE DATA SCHEMA FOR LAYERS --- ### 
    cds.override_node_properties("cds/layers/quoted_premium_annual_100", {"async_input": [rarc_task_name]})
    cds.override_node_properties("cds/layers/benchmark_premium_annual_100", {"async_input": [rarc_task_name]})

    cds.extend_node_rater_defined("cds", {
        "rate_change": hx.Structure(children={
            **{f"show_layer_{index}": hx.Bool(mode="output") for index in range(1,max_layers+1)},
            "expiring_policy_option_id": hx.Int(mode="override", async_input=["expiring_policy_fetch_task", "rarc_task", "start_renewal_task", "get_expiring_appetite_comment"], view={"label": "Expiring Policy Option", "format": {"thousandSeparated": False}}),
            "has_fetch_not_run": hx.Bool(mode="input", default=True, async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "has_fetch_run": hx.Bool(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "has_rarc_not_run": hx.Bool(mode="input", default=True, async_output=["rarc_task"]),
            "has_rarc_run": hx.Bool(mode="output", async_output=["rarc_task"]),
            "rarc_run_again_message": hx.Str(mode="output"),
            "rarc_message_show": hx.Bool(mode="output"),
            "layer_mapping": hx.Str(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "instructions": hx.Str(mode="input",view={"label": "Instructions", "read_only":True,"multiline":True},
                default="""The rate change tab calculates the change in premium associated with each component (detailed descriptions in the table below). The most appropriate method to obtain a rate change is to calculate the change on premium rather than the change in underlying factors as there are numerous interactions and products to consider.

                    To calculate the rate change, please follow the steps below:
                    1) The user should fist click 'Fetch Expiring Data' to initialise the rate change calculation.
                    2) Select mapping between renewing layers and expiry, this needs to be a 1-1 mapping so for layers that are not needed for rate change calculations, select the empty option.
                    3) If there have been any changes to the previous tabs (including the first instance of reaching this tab in any record/YOA), please press 'Calculate Rate Change'.
                    4) The rater will derive the rate changes to each component from the user input.
                    5) The user will be able to override the rate change values as appropriate in the 'UW Selected %' column.
                    6) To recalculate rate change following further changes, please press 'Calculate Rate Change' again.
                    7) Following the task running, the user will be able to override 'Expiring' and 'Renewal' fields with rate change automatically calculating WITHOUT having to run the task again. 

                    _Rate Change Components Include:_
                    _**Exposure Change**_: Driven by changes to base premium due to market cap, assets, country, industry, and ADR percentage
                    _**Risk Characteristics Change**_: Driven by changes to schedule modifiers
                    _**Deductible Change**_: Driven by changes to excesses, and deductibles
                    _**Limit Change**_: Driven by changes to limits 
                    _**Terms and Conditions Change**_: Driven by changes to coverages selected
                    _**Other Change**_: Driven by any other factors such as brokerage
                    """),
            "expiring_inception_date": hx.Date(mode="output", async_output=rarc_tasks_names),
            "expiring_expiry_date": hx.Date(mode="output", async_output=rarc_tasks_names),
        })
    })

    #### Formatting ####
    cds.override_node_properties("cds/layers/rate_change/insider_share/renewal", {"view": {"format": {"output": "percent", "mantissa": 1}}})
    cds.override_node_properties("cds/layers/rate_change/insider_share/expiring", {"view": {"format": {"output": "percent", "mantissa": 1}}})
    cds.override_node_properties("cds/layers/rate_change/brokerage/renewal", {"view": {"format": {"output": "percent", "mantissa": 1}}})
    cds.override_node_properties("cds/layers/rate_change/brokerage/expiring", {"view": {"format": {"output": "percent", "mantissa": 1}}})


