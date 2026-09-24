import hx_data_schema as hx
import libraries.common_data_schema.data_schema.utilities as utils
from algorithms.rate_constants import max_layers
from libraries.common_data_schema.data_schema.utilities import percent_format, thousands_format
import copy



def sch_rate_change(cds):

    
    cds.extend_node_rater_defined("cds", {
        "rate_change": hx.Structure(children={
            "show_hide_rc": hx.Bool(mode="output"),
           
           "expiring_policy_option_id": hx.Int(mode="override", async_input=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Expiring Policy Option", "format": {"thousandSeparated": False}}),
            "rarc_run_again_message": hx.Str(mode="output"),
            "rarc_message_show": hx.Bool(mode="output"),
            "uw_selected_rarc": hx.Float(mode="output", async_output=["rarc_task"], view={"label": "UW Selected Risk Adjusted Rate Change", "format":percent_format()}),
            "premium_annualized_beazley_share": hx.Structure(view={"label": "Premium"}, children={**coverage_prem()}),
            "check_if_prem_changed": hx.Float(mode="output", async_output=["rarc_task"]),

            # RC fields 
            "exposure_change": hx.Structure(view={"label": "Exposure Change"}, children={**coverage_rc_fields()}),
            "risk_characteristics_change": hx.Structure(view={"label": "Risk Characteristics Change"}, children={**coverage_rc_fields()}),
            "limit_change": hx.Structure(view={"label": "Limit change"}, children={**coverage_rc_fields()}),
            "deductible_change": hx.Structure(view={"label": "Deductible Change"}, children={**coverage_rc_fields()}),
            "terms_conditions_change": hx.Structure(view={"label": "Terms and Conditions Change"}, children={**coverage_rc_fields()}),
            "brokerage_change": hx.Structure(view={"label": "Brokerage Change"}, children={**coverage_rc_fields()}),
            "rate_change": hx.Structure(view={"label": "Rate Change"}, children={**coverage_rc_fields()}),

            "coverage_indicator": hx.Structure(children={
                "epl": hx.Bool(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], async_input=["expiring_policy_fetch_task", "rarc_task"]),
                "fid": hx.Bool(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], async_input=["expiring_policy_fetch_task", "rarc_task"]),
                "pcl": hx.Bool(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], async_input=["expiring_policy_fetch_task", "rarc_task"]),
            }),
            # nodes for individual coverage s
            "fte": hx.Structure(view={"label": "FTE's"}, children={**coverage_details()}), 
            "assets": hx.Structure(view={"label": "Assets"}, children={**coverage_details()}), 
            "limit": hx.Structure(view={"label": "Limit"}, children={**coverage_details()}), 
            "ded": hx.Structure(view={"label": "Deductible"}, children={**coverage_details()}), 
            "participants": hx.Structure(view={"label": "Participants"}, children={**coverage_details()}), 

            # show hide ftes for PCL if coverage is execuguard package 
            "execugard_package": hx.Bool(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]),
            "not_execugard_package": hx.Bool(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"]) 
        })
    })

def coverage_prem():
    return{
        "epl": hx.Structure(view={"label": "EPL"}, children={
            "renewal": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"],  view={"label": "Renewal", "format": {"thousandSeparated": True, "mantissa": 0}, "group": "EPL"}),
            "expiring": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Expiring", "format": {"thousandSeparated": True, "mantissa": 0}, "group": "EPL"}),  
            }),
        "fid": hx.Structure(view={"label": "FID"}, children={
            "renewal": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Renewal", "format": {"thousandSeparated": True, "mantissa": 0}, "group": "FID"}),
            "expiring": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Expiring", "format": {"thousandSeparated": True, "mantissa": 0}, "group": "FID"}),  
            }),
        "pcl": hx.Structure(view={"label": "PCL"}, children={
            "renewal": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Renewal", "format": {"thousandSeparated": True, "mantissa": 0}, "group": "PCL"}),
            "expiring": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Expiring", "format": {"thousandSeparated": True, "mantissa": 0}, "group": "PCL"}),  
            }),
        "execuguard": hx.Structure(view={"label": "Execuguard"}, children={
            "renewal": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Renewal", "format": {"thousandSeparated": True, "mantissa": 0}, "group": "Execuguard"}),
            "expiring": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Expiring", "format": {"thousandSeparated": True, "mantissa": 0}, "group": "Execuguard"}),  
            })
    }

def coverage_rc_fields():
    return{
        "epl": hx.Structure(view={"label": "EPL"}, children={
            "model": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], async_input=["expiring_policy_fetch_task", "rarc_task", "word_documents_task"], view={"label": "Model", "format":percent_format(), "group": "EPL"}),
            "selected": hx.Float(mode="override", async_output=[{"task": "rarc_task", "reset": False}], async_input=["expiring_policy_fetch_task", "rarc_task", "word_documents_task"], view={"label": "Selected", "format":percent_format(), "group": "EPL"}),  
            }),
        "fid": hx.Structure(view={"label": "FID"}, children={
            "model": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], async_input=["expiring_policy_fetch_task", "rarc_task", "word_documents_task"], view={"label": "Model", "format":percent_format(), "group": "FID"}),
            "selected": hx.Float(mode="override", async_output=[{"task": "rarc_task", "reset": False}], async_input=["expiring_policy_fetch_task", "rarc_task", "word_documents_task"], view={"label": "Selected", "format":percent_format(), "group": "FID"}),  
            }),
        "pcl": hx.Structure(view={"label": "PCL"}, children={
            "model": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], async_input=["expiring_policy_fetch_task", "rarc_task", "word_documents_task"], view={"label": "Model", "format":percent_format(), "group": "PCL"}),
            "selected": hx.Float(mode="override", async_output=[{"task": "rarc_task", "reset": False}], async_input=["expiring_policy_fetch_task", "rarc_task", "word_documents_task"], view={"label": "Selected", "format":percent_format(), "group": "PCL"}),  
            }),
        "execuguard": hx.Structure(view={"label": "Execuguard"}, children={
            "model": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], async_input=["expiring_policy_fetch_task", "rarc_task", "word_documents_task"], view={"label": "Model", "format":percent_format(), "group": "Execuguard"}),
            "selected": hx.Float(mode="override", async_output=[{"task": "rarc_task", "reset": False}], async_input=["expiring_policy_fetch_task", "rarc_task", "word_documents_task"], view={"label": "Selected", "format":percent_format(), "group": "Execuguard"}),  
            })
    }

def coverage_details ():
    return{
        "epl": hx.Structure(view={"label": "EPL"}, children={
            "expiry": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], async_input=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Expiry", "format":thousands_format(), "group": "EPL"}),
            "renewal": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], async_input=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Renewal", "format":thousands_format(), "group": "EPL"}),
            "rate_change": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], async_input=["expiring_policy_fetch_task", "rarc_task"], view={"label": "RC", "format":percent_format(), "group": "EPL"}),  
            }),
        "fid": hx.Structure(view={"label": "FID"}, children={
            "expiry": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], async_input=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Expiry", "format":thousands_format(), "group": "FID"}),
            "renewal": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], async_input=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Renewal", "format":thousands_format(), "group": "FID"}),
            "rate_change": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], async_input=["expiring_policy_fetch_task", "rarc_task"], view={"label": "RC", "format":percent_format(), "group": "FID"}),    
            }),
        "pcl": hx.Structure(view={"label": "PCL"}, children={
            "expiry": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], async_input=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Expiry", "format":thousands_format(), "group": "PCL"}),
            "renewal": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], async_input=["expiring_policy_fetch_task", "rarc_task"], view={"label": "Renewal", "format":thousands_format(), "group": "PCL"}),
            "rate_change": hx.Float(mode="output", async_output=["expiring_policy_fetch_task", "rarc_task"], async_input=["expiring_policy_fetch_task", "rarc_task"], view={"label": "RC", "format":percent_format(), "group": "PCL"}),  
            })
    }


