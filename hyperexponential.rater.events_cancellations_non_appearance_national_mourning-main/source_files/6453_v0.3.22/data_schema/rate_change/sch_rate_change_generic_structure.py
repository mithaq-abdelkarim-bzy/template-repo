# v0.5.0
import hx_data_schema as hx
import data_schema.sch_utilities as utils
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers 
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import coverages_dict , max_coverages, COVERAGES_LIST


### --- DEFINE GENERIC TASKS NAME --- ###
# NOTE: The unused cases can be removed
if not RARC_COVERAGE_USE and not RARC_INSURED_ASSET_USE:
    rarc_tasks_names = ["expiring_policy_fetch_task", "rarc_task"]
    rarc_task_name = "rarc_task"
elif not RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE:
    rarc_tasks_names = ["expiring_policy_fetch_task", "rarc_task_insured_asset"]
    rarc_task_name = "rarc_task_insured_asset"
elif RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE == False:
    rarc_tasks_names=["expiring_policy_fetch_coverages_task", "rarc_task_coverages"]
    rarc_task_name = "rarc_task_coverages"
elif RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE == True:
    rarc_tasks_names=["expiring_policy_fetch_coverages_task", "rarc_task_coverages_insured_asset"]
    rarc_task_name = "rarc_task_coverages_insured_asset"

### --- DEFINE GENERIC STRUCTURE FOR LAYERS AND COVERAGES --- ###
def rc_renewal_expiring(): 
    """
    Define common rate change fields used for generic rarc table
    """
    return {
    
    "expiring": hx.Float(mode="output", view={"label": "Expiring", "format": thousands_format()}),
    "rebased_expiring": hx.Float(mode="output", view={"label": "Rebased\nExpiring", "format": thousands_format()}), 
    "renewal": hx.Float(mode="output", view={"label": "Renewal", "format": thousands_format()}),
    "expiring_revalued": hx.Float(mode="output", view={"label": "Expiring Revalued", "format": thousands_format()}), # Edit Addition v0.3.0 - Amount converted in renewing currency use to handle change in currency at renewal.
}

def rc_quoted_premium(): 
    """
    Define common rate change fields for premiums used for generic rarc table
    """

    return {
        "premium": hx.Structure(children={
        "line_100pct": hx.Structure(children={
            "policy_term": hx.Structure(view={"label": 'Premium - Policy Term (100% Line)'}, children={**rc_renewal_expiring()}), # EDIT Addition v0.3.0
            "annualised": hx.Structure(view={"label": 'Premium - Annualised (100% Line)'}, children={**rc_renewal_expiring()})
        }),
        "beazley_line": hx.Structure(children={
            "policy_term": hx.Structure(view={"label": 'Premium - Policy Term (Beazley Line)'}, children={**rc_renewal_expiring()}),
            "annualised": hx.Structure(view={"label": 'Premium - Annualised (Beazley Line)'}, children={**rc_renewal_expiring()}),
        }),
    }),
}

def expiring_info_no_insured_asset():
    """
    Define common Expiry rate change fields when insured asset are NOT used.
    These are intermediate nodes for expiry data displayed in the rate change table.
    """
    return {
    "expiring_quoted_premium_100": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_quoted_premium_annual_100": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_quoted_premium": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_quoted_premium_annual": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_limit": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_excess": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_deductible": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_brokerage": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_currency": hx.Str(mode="output", async_output=rarc_tasks_names),

}

def expiring_info_insured_asset():
    """
    Define common Expiry rate change fields when insured asset are used
    These are intermediate nodes for expiry data displayed in the rate change table.
    """
    return {
    "expiring_quoted_premium_100": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_quoted_premium_annual_100": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_quoted_premium": hx.Float(mode="output", async_output=rarc_tasks_names), # Edit v0.5.0
    "expiring_quoted_premium_annual": hx.Float(mode="output", async_output=rarc_tasks_names), # Edit v0.5.0
    # "expiring_limit": hx.Float(mode="output", async_output=rarc_tasks_names), # Edit v0.5.0 - no need when using insured asset
    # "expiring_excess": hx.Float(mode="output", async_output=rarc_tasks_names), # Edit v0.5.0  - no need when using insured asset
    # "expiring_deductible": hx.Float(mode="output", async_output=rarc_tasks_names), # Edit v0.5.0 - no need when using insured asset
    "expiring_brokerage": hx.Float(mode="output", async_output=rarc_tasks_names),
    "expiring_currency": hx.Str(mode="output", async_output=rarc_tasks_names),
}

def rc_expiring_info(): 
    """
    Define common Expiry rate change fields
    """
    if not RARC_INSURED_ASSET_USE:
        return {**expiring_info_no_insured_asset()}
    else:
        return {**expiring_info_insured_asset()}

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

def rc_show_coverages(): 
    """
    Define show_coverage_ids node for UI
    """
    return {f"show_coverage_{index}": hx.Bool(mode="output") for index in range(1,max_coverages+1)} if RARC_COVERAGE_USE else {}

def insured_asset_list_name(): # Edit v0.5.0
    """
    Define staging nodes for insured asset list depending of the use of coverages
    """
    if not RARC_COVERAGE_USE:
        return {
            "layers": hx.Str(mode="output", async_input=[rarc_task_name]),
        }
    else:
        return {
            f"{COVERAGES_LIST[0]}": hx.Str(mode="output", async_input=[rarc_task_name]),
            f"{COVERAGES_LIST[1]}": hx.Str(mode="output", async_input=[rarc_task_name]),
        }

def rc_insured_asset_list(): # Edit v0.5.0
    """
    Define the structure to store insured asset list using conditional statement
    """
    return {"insured_asset_list": hx.Structure(
        children={
            **insured_asset_list_name()
        }
    )} if RARC_INSURED_ASSET_USE else {}


# EDIT addition v0.5.0
def expiring_and_renewal_no_insured_asset():
    """
    Define common rate change fields used for generic rarc table
    NOTE: add more fields if necessary
    """

    renewal_vs_expiry = [
        "limit",
        "deductible",
        "excess",
        "brokerage",
        "currency",
    ]

    renewal_vs_expiry_label = [
        "Limit",
        "Deductible",
        "Excess",
        "Brokerage",
        "Currency",
    ]

    renewal_vs_expiry_format = [
        {"thousandSeparated": True, "mantissa": 0},
        {"thousandSeparated": True, "mantissa": 0},
        {"thousandSeparated": True, "mantissa": 0},
        {"output": "percent", "mantissa": 1},
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
                "expiring_revalued": hx.Str(mode="output", view={"label": "Expiring \n Revalued", "format": format_}), # Edit Addition v0.3.0 - Amount converted in renewing currency use to handle change in currency at renewal.
                }) 
        else:
            result[item] = hx.Structure(view={"label": label}, children={
                "renewal": hx.Float(mode="output", view={"label": "Renewal", "format": format_}),
                "expiring": hx.Float(mode="output", view={"label": "Expiring", "format": format_}),
                "expiring_revalued": hx.Float(mode="output", view={"label": "Expiring \n Revalued", "format": format_}), # Edit Addition v0.3.0 - Amount converted in renewing currency use to handle change in currency at renewal.
                }) 

    return result

# EDIT addition v0.5.0
def expiring_and_renewal_insured_asset():
    """
    Define common rate change fields used for generic rarc table
    NOTE: add more fields if necessary
    """

    renewal_vs_expiry = [
        # "limit",
        # "deductible",
        # "excess",
        "brokerage",
        "currency",
    ]

    renewal_vs_expiry_label = [
        # "Limit",
        # "Deductible",
        # "Excess",
        "Brokerage",
        "Currency",
    ]

    renewal_vs_expiry_format = [
        # {"thousandSeparated": True, "mantissa": 0},
        # {"thousandSeparated": True, "mantissa": 0},
        # {"thousandSeparated": True, "mantissa": 0},
        {"output": "percent", "mantissa": 1},
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
                "expiring_revalued": hx.Str(mode="output", view={"label": "Expiring \n Revalued", "format": format_}), # Edit Addition v0.3.0 - Amount converted in renewing currency use to handle change in currency at renewal.
                }) 
        else:
            result[item] = hx.Structure(view={"label": label}, children={
                "renewal": hx.Float(mode="output", view={"label": "Renewal", "format": format_}),
                "expiring": hx.Float(mode="output", view={"label": "Expiring", "format": format_}),
                "expiring_revalued": hx.Float(mode="output", view={"label": "Expiring \n Revalued", "format": format_}), # Edit Addition v0.3.0 - Amount converted in renewing currency use to handle change in currency at renewal.
                }) 

    return result

def rc_expiring_and_renewal():
    """
    Define common rate change fields used for generic rarc table
    """
    if not RARC_INSURED_ASSET_USE:
        return {**expiring_and_renewal_no_insured_asset()}
    else:
        return {**expiring_and_renewal_insured_asset()}
