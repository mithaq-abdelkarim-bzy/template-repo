import hx_data_schema as hx
import data_schema.sch_utilities as utils # include thousands_format, percent_format, integer_format)
from algorithms.rate_constants import max_layers, experience_rating_max_years, max_data_layout, reinstatement_max_number
from data_schema.sch_utilities import create_node_from_list

def sch_pricing_selection_bdx_summary(cds):
    return {
        cds.extend_node_rater_defined("cds/layers", { 
            "pricing_selection": hx.Structure(view={"label": "Pricing Selection"}, children={
                "final_selection": hx.Structure(view={"label": "Final Selection"}, children={
                    ** _final_selection_children(),
                }),
                "risk_profile_bdx": hx.Structure(view={"label": "Risk Profile Bdx"}, children={
                    ** _exposure_method_children(),
                }),
                "limit_average_severity": hx.Structure(view={"label": "Limit Average Severity"}, children={
                    ** _method_children(),
                }),
                "burning_cost": hx.Structure(view={"label": "Burning Cost"}, children={
                    ** _method_children(),
                    "ulr": hx.Float(mode="output", optionality="optional", view={"label": "ULR", "format": {"output": "percent", "mantissa": 2}}),
                            
                }),
                "clash": hx.Structure(view={"label": "Clash"}, children={
                    ** _method_children(),
                }),
                "healthcare_cat": hx.Structure(view={"label": "Healthcare Cat"}, children={
                    ** _method_children(),
                }),
                "other_method": hx.Structure(view={"label": "Other Method"}, children={
                    ** _other_method_children(),
                }),
                
            }),
            "risk_profile_bdx": hx.Structure(view={"label": "Risk Profile Bdx"}, children={
                **_steer_risk_profile_bdx_layer_children(),
            }),  

        })
    }

def _steer_risk_profile_bdx_layer_children():
    node_info_list = [

        ("Pro Rata Premium",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Exposure Premium",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("GLR Pick",hx.Str,"input","Cedant LR",None,None,None),
        ("Exposure LR",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("EL at loss ratio",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Rate on NPI",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("Loss Premium",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Pure Rate",hx.Float,"output",None,utils.percent_format(2),None,None),
    ]
    return create_node_from_list(node_info_list) 

def sch_pricing_selection_cob_params(cds):
    return {
        cds.extend_node_rater_defined("cds", { 
            "pricing_selection": hx.Structure(view={"label": "Pricing Selection"}, children={
                "pareto_parameters": hx.Structure(view={"label": "Pareto Parameters"}, children={
                    ** _params_children(),
                }),
                "odf_parameters": hx.Structure(view={"label": "ODF Parameters"}, children={
                    ** _params_children(),
                }),
            }),
            "other_method_rationale": hx.Str(mode="input", default="", view={"label": "Other Method Rationale"}),

        })
    }

def _pricing_assumptions_children():
    node_info_list = [
        ("Limit",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Excess",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("EPI",hx.Float,"output",None,utils.thousands_format(0),None,None),

    ]
    return create_node_from_list(node_info_list) 
    

def _final_selection_children():
    node_info_list = [
        ("Total Weighting",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("PLR Method",hx.Str,"output",None,None,None,None),
        ("Pure Rate",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("Pure Premium",hx.Float,"output",None,utils.thousands_format(0),"advanced_features_task",None),
        ("Pure ROL",hx.Float,"output",None,utils.percent_format(2),None,None),

    ]
    return create_node_from_list(node_info_list)
    
def _exposure_method_children():
    node_info_list = [
        ("Cedant Loss Ratio",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("Pure Rate",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("Pure Premium",hx.Float,"output",None,utils.thousands_format(0),"advanced_features_task",None),
        ("Pure ROL",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("Weighting",hx.Float,"input",None,utils.percent_format(2),None,None,"optional"),



    ]
    return create_node_from_list(node_info_list)

def _method_children():
    node_info_list = [
        ("Pure Rate",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("Pure Premium",hx.Float,"output",None,utils.thousands_format(0),"advanced_features_task",None),
        ("Pure ROL",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("Weighting",hx.Float,"input",None,utils.percent_format(2),None,None,"optional"),



    ]
    return create_node_from_list(node_info_list)

def _other_method_children():
    node_info_list = [
        ("Pure Rate",hx.Float,"input",0.0,utils.percent_format(2),None,None),
        ("Pure Premium",hx.Float,"output",None,utils.thousands_format(0),"advanced_features_task",None),
        ("Pure ROL",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("Weighting",hx.Float,"input",None,utils.percent_format(2),None,None,"optional"),

    ]
    return create_node_from_list(node_info_list)

def _params_children():
    node_info_list = [
        ("Default",hx.Float,"output",None,utils.thousands_format(2),None,None),
        ("Overwrite",hx.Float,"input",None,utils.thousands_format(2),None,None,"optional"),
        ("Selected",hx.Float,"output",None,utils.thousands_format(2),["advanced_features_task"],None),

    ]
    return create_node_from_list(node_info_list)




