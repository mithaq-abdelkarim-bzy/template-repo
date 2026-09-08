import hx_data_schema as hx
import data_schema.utilities as utils
import algorithms.utils_global_lists as lst

def sch_other_calcs(cds):
    cds.extend_node_rater_defined("cds/layers", {
        # Other
        "final_premium": hx.Float(mode="output", view={"label": "Final Premium", "format":utils.thousands_format(0)}),  
        "final_premium_annual": hx.Float(mode="output", view={"label": "Final Premium (Annualized)", "format":utils.thousands_format(0)}),  
        "unity_premium_annual": hx.Float(mode="output", view={"label": "Unity Premium (Annualized)", "format":utils.thousands_format(0)}),  
        "priced_to_lr": hx.Float(mode="output"),
        "benchmark_lr": hx.Float(mode="output"),
        "technical_lr": hx.Float(mode="output"),
        "assumed_brokerage": hx.Float(mode="output"),
    })

def sch_other_calcs_non_cds():
    return {
        # Debugging
        "debug_num": hx.Float(mode="output", view={"format": utils.integer_format(3)}),
        "debug_num1": hx.Float(mode="output", view={"format": utils.integer_format(3)}),
        "debug_num2": hx.Float(mode="output", view={"format": utils.integer_format(3)}),
        "debug_num3": hx.Float(mode="output", view={"format": utils.integer_format(3)}),
        "debug_num4": hx.Float(mode="output", view={"format": utils.integer_format(3)}),
        "debug_num5": hx.Float(mode="output", view={"format": utils.integer_format(3)}),
        "debug_str": hx.Str(mode="output"),

        "debug_task_input": hx.Float(mode="input", default=0, async_input=["test_async_task"], view={"format": utils.integer_format(1)}),
        "debug_task_output": hx.Float(mode="input", default=0, async_output="test_async_task", view={"format": utils.integer_format(1)}),
        }
