import hx_data_schema as hx
import data_schema.sch_utilities as utils # include thousands_format, percent_format, integer_format)
from algorithms.rate_constants import max_layers, experience_rating_max_years, max_data_layout, reinstatement_max_number, las_limit_number
from data_schema.sch_utilities import create_node_from_list
from data_schema.sch_rate_change import rarc_task_name


def _steer_exposure():
    return {
        # "risk_profile_banded": hx.Structure(view={"label": "Risk Profile Banded"}, children={
        #     ** _steer_risk_profile_banded(),
        # }),
        "risk_profile_bdx": hx.Structure(view={"label": "Risk Profile Bdx"}, children={
            ** _steer_risk_profile_bdx(),
        }),
        "limit_average_severity": hx.Structure(view={"label": "Limit Average Severity"}, children={
            ** _steer_limit_average_severity(),
        }),

    }

def _steer_risk_profile_bdx():
    risk_profile_bdx = {}
    # add bdx single nodes
    risk_profile_bdx.update(_steer_risk_profile_bdx_single_node())
    # create list for risk_profiles
    risk_profiles_node = hx.List(mode="input",view={"label":"Risk Profiles"}, children={
        # add generic risk profile non layer specific nodes
        **_steer_risk_profile_bdx_list_children(),
    })
    # create structure for layers within the risk_profiles_node list and add their children nodes
    for i in range(1, max_layers+1):
        # field_name = f"layer_{i}"
        field_name = f"layer_{i:02d}"
        risk_profiles_node.children[field_name] = hx.Structure(view={"label": f"Layer {i}"}, children={
            # add risk profile bdx list layer specific nodes
            **_steer_risk_profile_bdx_List_layer_children(),

            
        })

    # add list to the result dictionaru
    risk_profile_bdx["risk_profiles"] = risk_profiles_node

    # create layers structures for summary
    layers = {}
    # adding layer node to the dict
    for i in range(1, max_layers+1):
        # field_name = f"layer_{i}"
        field_name = f"layer_{i:02d}"
        layers[field_name] = hx.Structure(view={"label": f"Layer {i}"}, children={
            # TODO IH add structure to differentiate bdx and las?
            **_steer_risk_profile_bdx_layer_generic_children(),
            "bdx":hx.Structure(view={"label": "BDX"}, children={
                # adding bdx Summary field per layer
                **_steer_risk_profile_bdx_layer_children(),
            }),
        })    
    
    return risk_profile_bdx

def _steer_risk_profile_bdx_before_change():
    risk_profile_bdx = {}
    # add bdx single nodes
    risk_profile_bdx.update(_steer_risk_profile_bdx_single_node())
    # create list for risk_profiles
    risk_profiles_node = hx.List(mode="input",view={"label":"Risk Profiles"}, children={
        # add generic risk profile non layer specific nodes
        **_steer_risk_profile_bdx_list_children(),
    })
    # create structure for layers within the risk_profiles_node list and add their children nodes
    for i in range(1, max_layers+1):
        # field_name = f"layer_{i}"
        field_name = f"layer_{i:02d}"
        risk_profiles_node.children[field_name] = hx.Structure(view={"label": f"Layer {i}"}, children={
            # add risk profile bdx list layer specific nodes
            **_steer_risk_profile_bdx_List_layer_children(),
            # risk profile LAS list layer specific nodes
            "las": hx.Structure(view={"label": "LAS"},children={
                "current_year": hx.Structure(view={"label":"Current Year"}, children={                                    
                    **_steer_las_sub_layer_section_a_children(),
                    **_steer_las_sub_layer_section_b_children(),
                    **_steer_las_sub_layer_section_c_children(),
                }),
                "previous_year": hx.Structure(view={"label":"Previous Year"}, children={                                    
                    **_steer_las_sub_layer_section_b_children(),
                    **_steer_las_sub_layer_section_c_children(),
                }),
                "movement": hx.Structure(view={"label":"Movement"}, children={                                    
                    **_steer_las_sub_layer_section_b_children(),
                    **_steer_las_sub_layer_section_c_children(),
                }),
                "chart": hx.Structure(view={"label":"Chart"}, children={                                    
                    **_steer_las_sub_layer_section_d_children(),
                }),
            })  
            
        })
    # fgu layer with Risk profile LAS list nodes
    risk_profiles_node.children["fgu"] = hx.Structure(view={"label": "FGU"}, children={
        "las": hx.Structure(view={"label": "LAS"},children={
            **_steer_las_fgu_list_children()
        })  
    })

    # add list to the result dictionaru
    risk_profile_bdx["risk_profiles"] = risk_profiles_node

    # create layers structures for summary
    layers = {}
    # adding layer node to the dict
    for i in range(1, max_layers+1):
        # field_name = f"layer_{i}"
        field_name = f"layer_{i:02d}"
        layers[field_name] = hx.Structure(view={"label": f"Layer {i}"}, children={
            # TODO IH add structure to differentiate bdx and las?
            **_steer_risk_profile_bdx_layer_generic_children(),
            "bdx":hx.Structure(view={"label": "BDX"}, children={
                # adding bdx Summary field per layer
                **_steer_risk_profile_bdx_layer_children(),
            }),
        })

    las_total_layers={}
    # adding layer node to the dict for las
    for i in range(1, max_layers+1):
        field_name = f"layer_{i:02d}"
        las_total_layers[field_name] = hx.Structure(view={"label": f"Layer {i:02d}"}, children={

            "las":hx.Structure(view={"label": "LAS"}, children={                             
                **_steer_las_layer_cy_total_children(),
                "current_year":hx.Structure(view={"label": "Current Year"}, children={
                    **_steer_las_sub_layer_section_c_children()
                }),
                "previous_year":hx.Structure(view={"label": "Previous Year"}, children={
                    **_steer_las_sub_layer_section_c_children()
                }),
                "movement":hx.Structure(view={"label": "Movement"}, children={
                    **_steer_las_sub_layer_section_c_children()
                }),
            }),
        })
    ## add FGU
    las_total_layers["fgu"] = hx.Structure(view={"label": "FGU"}, children={
        "las":hx.Structure(view={"label": "LAS"}, children={
            **_steer_las_fgu_total_children()
        }),

    })
    
    risk_profile_bdx["total_las"] = hx.Structure(view={"label": "Total"}, children={
        # TODO add individual layers
        **las_total_layers
        
    })
    
    
    return risk_profile_bdx

def _steer_limit_average_severity():
    """
    Create limit average severity structure
    """
    # limit average severity structure
    las_dict = {}
    # create layers structures
    layers = {}

    # adding FGU node to the dict
    layers["fgu"] = hx.Structure(view={"label": "fgu"}, children={
        "risk_profiles": hx.List(mode="output", view={"label": "Risk Profiles"}, children={
            **_steer_las_fgu_list_children()
        }),
        "total": hx.Structure(view={"label": "Total"},children={
            **_steer_las_fgu_total_children()
        }),        
    })

    # adding layer node to the dict
    for i in range(1, max_layers+1):
        # field_name = f"layer_{i}"
        field_name = f"layer_{i:02d}"
        layers[field_name] = hx.Structure(view={"label": f"Layer {i:02d}"}, children={
            "risk_profiles": hx.List(mode="input",async_input=[rarc_task_name],default_element_count=las_limit_number, max_element_count=las_limit_number, min_element_count=las_limit_number,view={"label": "Risk Profiles"},children={
                # **_steer_las_sub_layer_children(),
                "current_year": hx.Structure(view={"label":"Current Year"}, children={                                    
                    **_steer_las_sub_layer_section_a_children(),
                    **_steer_las_sub_layer_section_b_children(),
                    **_steer_las_sub_layer_section_c_children(),
                }),
                "previous_year": hx.Structure(view={"label":"Previous Year"}, children={                                    
                    **_steer_las_sub_layer_section_b_children(),
                    **_steer_las_sub_layer_section_c_children(),
                }),
                "movement": hx.Structure(view={"label":"Movement"}, children={                                    
                    **_steer_las_sub_layer_section_b_children(),
                    **_steer_las_sub_layer_section_c_children(),
                }),
                "chart": hx.Structure(view={"label":"Chart"}, children={                                    
                    **_steer_las_sub_layer_section_d_children(),
                }),
            }),
            "total": hx.Structure(view={"label": "Total"},children={
                "current_year": hx.Structure(view={"label":"Current Year"}, children={                                    
                    **_steer_las_sub_layer_section_c_children()
                }),
                
            }),  
            "limit": hx.Float(mode="output", view={"label": "Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "excess": hx.Float(mode="output", view={"label": "Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
            **_steer_las_layer_cy_total_children(),                                  
        })



    las_dict["layers"] = hx.Structure(view={"label": f"Layers"}, children={
        **layers
        })


    return las_dict

def _steer_risk_profile_bdx_layer_generic_children():
    node_info_list = [
        ("Limit",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Excess",hx.Float,"output",None,utils.thousands_format(0),None,None),
    ]
    return create_node_from_list(node_info_list) 

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

def _steer_risk_profile_bdx_single_node():

    node_info_list = [
        ("Exposure LR",hx.Float,"input",0,utils.percent_format(2),None,None),
        ("Exposure Profile gross Premium",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("No. of risk",hx.Int,"output",None,utils.integer_format(0),None,None),
        ("Curve",hx.Str,"output",None,None,None,None),
        ("Message",hx.Str,"output",None,None,None,None),

    ]
    return create_node_from_list(node_info_list)
    
def _steer_risk_profile_bdx_list_children():
    node_info_list = [
        ("COB",hx.Str,"input","",None,None,None),
        ("Curve",hx.Str,"input","",None,None,None),
        ("Insured",hx.Str,"input","",None,None,None),
        ("Currency",hx.Str,"output",None,None,None,None),
        ("Limit",hx.Float,"input",0,utils.thousands_format(0),None,None),
        ("Excess",hx.Float,"input",0,utils.thousands_format(0),None,None),
        ("Net Premium",hx.Float,"input",0,utils.thousands_format(0),None,None),
        ("Share",hx.Float,"input",0,utils.percent_format(2),None,None),
        ("Linkage",hx.Str,"input","",None,None,None),
        ("Parametric",hx.Str,"output",None,None,None,None),
        ("Parametric",hx.Str,"output",None,None,None,None),
        ("Curve Type",hx.Str,"output",None,None,None,None),
        ("Fx Rate to USD",hx.Float,"output",None,utils.thousands_format(2),None,None),
        ("First Loss",hx.Bool,"output",None,None,None,None),
        ("First Loss Factor",hx.Float,"output",None,utils.thousands_format(7),None,None),
        ("Param_1",hx.Float,"output",None,utils.thousands_format(2),None,None),
        ("Param_2",hx.Float,"output",None,utils.thousands_format(2),None,None),
        ("Param_3",hx.Float,"output",None,utils.thousands_format(2),None,None),
        ("Param_4",hx.Float,"output",None,utils.thousands_format(2),None,None),
        ("Exposure",hx.Float,"output",None,None,None,None),
    ]
    return create_node_from_list(node_info_list)

def _steer_risk_profile_bdx_List_layer_children():
    node_info_list = [
        ("Expo Pct",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("Expo premium",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Excess",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Sum Insured",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("ILF_xs_and_xm",hx.Float,"output",None,utils.thousands_format(2),None,None),
        ("ILF_xs_and_xl",hx.Float,"output",None,utils.thousands_format(2),None,None),
        ("ILF_xs_and_lmt",hx.Float,"output",None,utils.thousands_format(2),None,None),
        ("ILF_xs",hx.Float,"output",None,utils.thousands_format(2),None,None),
        ("PR Pct",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("PR Net Premium",hx.Float,"output",None,utils.thousands_format(0),None,None),
    ]
    return create_node_from_list(node_info_list)



def _steer_las_layer_cy_total_children():
    layer_total_node_info_list = [
        ("GLR",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("Expected Loss",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Pure Rate",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("ROL",hx.Float,"output",None,utils.percent_format(2),None,None),
    ]
    return create_node_from_list(layer_total_node_info_list)

def _steer_las_fgu_total_children():
    fgu_total_node_info_list = [
        ("Losses",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Occurrences",hx.Int,"output",None,utils.integer_format(0),None,None),
        ("Average",hx.Float,"output",None,utils.thousands_format(0),None,None),
    ]
    return create_node_from_list(fgu_total_node_info_list)

def _steer_las_fgu_list_children():
    node_info_list = [
        ("Lower",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Upper",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Losses",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Occurrences",hx.Int,"output",None,utils.integer_format(0),None,None),
        ("Average",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("LAS",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("ILF Empirical",hx.Float,"output",None,utils.thousands_format(2),None,None),
    ]
    return create_node_from_list(node_info_list)

def _steer_las_sub_layer_section_a_children():
    node_info_list = [
        ("Lower",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Upper",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("ILF User Input",hx.Float,"input",0,utils.thousands_format(2),None,None),
        ("ILF Selected",hx.Float,"output",None,utils.thousands_format(2),None,None),
    ]
    return create_node_from_list(node_info_list)

def _steer_las_sub_layer_section_b_children():
    node_info_list = [
        ("Pct of Claims to Layer",hx.Float,"output",None,utils.percent_format(2),None,None),
    ]
    return create_node_from_list(node_info_list)

def _steer_las_sub_layer_section_c_children():
    node_info_list = [
        ("Premium",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Loss to Layer",hx.Float,"output",None,utils.thousands_format(0),None,None),
    ]
    return create_node_from_list(node_info_list)

def _steer_las_sub_layer_section_d_children():
    node_info_list = [
        ("Limit",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("This year",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Last Year",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("ILF Selected",hx.Float,"output",None,utils.percent_format(2),None,None),
    ]
    return create_node_from_list(node_info_list)

def _steer_cd_all_curves():
    node_info_list = [
        ("Description",hx.Str,"output",None,None,None,None),
        ("Parametric",hx.Str,"output",None,None,None,None),
        ("Curve Description",hx.Str,"output",None,None,None,None),
        ("Source",hx.Str,"output",None,None,None,None),
    ]
    return create_node_from_list(node_info_list) 


def _steer_cd_commercial_auto_state():
    node_info_list = [
        ("Group 1",hx.Str,"output",None,None,None,None),
        ("Group 2",hx.Str,"output",None,None,None,None),
        ("Group 3",hx.Str,"output",None,None,None,None),
        ("Group 4",hx.Str,"output",None,None,None,None),
        ("Group 5",hx.Str,"output",None,None,None,None),
        ("Group 6",hx.Str,"output",None,None,None,None),
        ("Group 7",hx.Str,"output",None,None,None,None),
        ("Group 8",hx.Str,"output",None,None,None,None),
    ]
    return create_node_from_list(node_info_list) 

def _steer_cd_cyber():
    node_info_list = [
        ("Low",hx.Str,"output",None,None,None,None),
        ("High",hx.Str,"output",None,None,None,None),

    ]
    return create_node_from_list(node_info_list) 

def _steer_cd_healthcare():
    node_info_list = [
        ("Low",hx.Str,"output",None,None,None,None),
        ("Medium",hx.Str,"output",None,None,None,None),
        ("Medium High",hx.Str,"output",None,None,None,None),
        ("High",hx.Str,"output",None,None,None,None),
        ("Very High",hx.Str,"output",None,None,None,None),

    ]
    return create_node_from_list(node_info_list) 

def _steer_cd_private_d_and_o():
    node_info_list = [
        ("Low",hx.Str,"output",None,None,None,None),
        ("Medium",hx.Str,"output",None,None,None,None),
        ("High",hx.Str,"output",None,None,None,None),
        ("Very High",hx.Str,"output",None,None,None,None),
    ]
    return create_node_from_list(node_info_list) 
