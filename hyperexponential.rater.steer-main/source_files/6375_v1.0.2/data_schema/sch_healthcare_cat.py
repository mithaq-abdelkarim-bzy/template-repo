import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers, hc_max_trial_history_years, hc_max_overall_exposure_years, hc_location_number, hc_percentile_display_number
import data_schema.sch_utilities as utils
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import coverages_dict
from data_schema.sch_rate_change import rarc_task_name

from data_schema.sch_utilities import create_node_from_list

def sch_healthcare_cat(cds):
    return {
        cds.extend_node_rater_defined("cds", { 
            "healthcare_cat": hx.Structure(children={
                "trial_history": hx.Structure(view={"label": "Trial History"}, children={
                    "trial":hx.List(mode="input", async_input=[rarc_task_name,"start_renewal_task"], async_output=[{"task": "start_renewal_task", "reset": False}],default_element_count=hc_max_trial_history_years, max_element_count=hc_max_trial_history_years, min_element_count=hc_max_trial_history_years, view={"label": "Trial"}, children={
                        **_healthcare_cat_trial_history_children(),
                    }),
                    "total":hx.Structure( view={"label": "Total"}, children={
                        **_healthcare_cat_trial_history_total_children(),
                    }),
                    "uw_view":hx.Structure( view={"label": "Select Years"}, children={
                        **_healthcare_cat_trial_history_uw_view_children(),
                    }),
                                        
                }),
                "exposure_territory": hx.Structure(view={"label": "Exposure"}, children={
                     **_healthcare_cat_exposure_territory_single_nodes(),
                    "overall_exposure_per_year":hx.List(mode="input",async_input=[rarc_task_name,"start_renewal_task"], async_output=[{"task": "start_renewal_task", "reset": False}], default_element_count=hc_max_overall_exposure_years, max_element_count=hc_max_overall_exposure_years, min_element_count=hc_max_overall_exposure_years, view={"label": "Overall Exposure Per Year"}, children={
                        **_healthcare_cat_exposure_per_year_nodes(),
                    }),
                    "exposure_spit_by_state":hx.List(mode="input", async_input=["start_renewal_task"], async_output=[{"task": "start_renewal_task", "reset": False}], default_element_count=hc_location_number, max_element_count=hc_location_number, min_element_count=hc_location_number,view={"label": "Exposure Split by State"}, children={
                        **_healthcare_cat_exposure_split_by_state_nodes(),
                    }),
                }),
                "pricing": hx.Structure(view={"label": "Pricing"}, children={
                    "territory_adjustment": hx.Structure(view={"label": "Territory Adjustment"}, children={
                        "value": hx.Float(mode="output", view={"label": "Value", "format": {"thousandSeparated": False, "mantissa": 2}}),
                    }),
                    "trial_history_adjustment": hx.Structure(view={"label": "Trial\nHistory\nAdjustment"}, children={
                        "value": hx.Float(mode="output", view={"label": "Value", "format": {"thousandSeparated": False, "mantissa": 2}}),
                    }),
                    "type_of_business_adjustment": hx.Structure(view={"label": "Type\nOf\nBusiness\nAdjustment"}, children={
                        "value": hx.Float(mode="output", view={"label": "Value", "format": {"thousandSeparated": False, "mantissa": 2}}),
                    }),
                    "specialty_adjustment": hx.Structure(view={"label": "Specialty\nAdjustment"}, children={
                        "value": hx.Float(mode="output", view={"label": "Value", "format": {"thousandSeparated": False, "mantissa": 2}}),
                    }),
                    "high_low_adjustment": hx.Structure(view={"label": "High\nLow\nAgreement"}, children={
                        "value": hx.Float(mode="output", view={"label": "Value", "format": {"thousandSeparated": False, "mantissa": 2}}),
                        "select": hx.Str(mode="input",async_input=[rarc_task_name,"start_renewal_task"], async_output=[{"task": "start_renewal_task", "reset": False}],default="Yes",optionality="required",options=["Yes","No"], view={"label": "Select"}),
                    }),
                    "social_inflation_impact": hx.Structure(view={"label": "Social\nInflation\nImpact"}, children={
                        "value": hx.Float(mode="output", view={"label": "Value", "format": {"thousandSeparated": False, "mantissa": 2}}),
                        "select": hx.Str(mode="input",async_input=[rarc_task_name,"start_renewal_task"], async_output=[{"task": "start_renewal_task", "reset": False}],default="L",optionality="required",options=["L","M","H"], view={"label": "Select"}),
                    }),
                    "total_risk_adjustment": hx.Structure(view={"label": "Total\nRisk\nAdjustment"}, children={
                        "value": hx.Float(mode="output", view={"label": "Value", "format": {"thousandSeparated": False, "mantissa": 2}}),
                    }),
                    **_healthcare_cat_pricing_loss_distribution_children(),
                    "loss_distribution_summary":hx.List(mode="input", default_element_count=hc_percentile_display_number, max_element_count=hc_percentile_display_number, min_element_count=hc_percentile_display_number, view={"label": "Exposure Split by State"}, children={
                        **_healthcare_cat_pricing_loss_distribution_list_children(),
                    }), 
                }),
                
                
            }),   
        })
    }

def sch_non_cds_healthcare_cat():
    '''
    Non CDS nodes for intermediate calculation only
    '''
    return {
        "healthcare_cat": hx.Structure(children={
            "pricing_calc": hx.Structure(view={"label": "Pricing Calculation"}, children={
                "loss_distribution_calculation":hx.List(mode="output", view={"label": "Exposure Split by State"}, children={
                    **_healthcare_cat_pricing_calculation_loss_distribution_list_children(),
                }),
                
            }),
        }),
    }

def _healthcare_cat_trial_history_children():
    node_info_list = [
        ("Display YOA",hx.Str,"output",None,None,[rarc_task_name,"start_renewal_task"],None),
        ("UW Year",hx.Int,"output",None,None,[rarc_task_name,"start_renewal_task"],None),
        ("Taken to Trial",hx.Int,"input",0,utils.integer_format(0),[rarc_task_name,"start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),
        ("Wins",hx.Int,"input",0,utils.integer_format(0),[rarc_task_name,"start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),
        ("Losses",hx.Int,"input",0,utils.integer_format(0),[rarc_task_name,"start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),
        ("Mistrials",hx.Int,"input",0,utils.integer_format(0),[rarc_task_name,"start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),
        ("Win Pct",hx.Float,"output",None,utils.percent_format(2),[rarc_task_name,"start_renewal_task"],None),

        ]
    return create_node_from_list(node_info_list) 

def _healthcare_cat_trial_history_total_children():
    node_info_list = [
        ("Display YOA",hx.Str,"output",None,None,None,None),
        ("UW Year",hx.Int,"output",None,None,None,None),
        ("Taken to Trial",hx.Int,"output",None,utils.integer_format(0),None,None),
        ("Wins",hx.Int,"output",None,utils.integer_format(0),None,None),
        ("Losses",hx.Int,"output",None,utils.integer_format(0),None,None),
        ("Mistrials",hx.Int,"output",None,utils.integer_format(0),None,None),
        ("Win Pct",hx.Float,"output",None,utils.percent_format(2),None,None),
        ]
    return create_node_from_list(node_info_list) 
def _healthcare_cat_trial_history_uw_view_children():
    node_info_list = [
        ("From Year",hx.Int,"input",0,utils.integer_format(0),[rarc_task_name,"start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),
        ("To Year",hx.Int,"input",0,utils.integer_format(0),[rarc_task_name,"start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),

        ("Display YOA",hx.Str,"output",None,None,None,None),
        ("UW Year",hx.Int,"output",None,None,None,None),
        ("Taken to Trial",hx.Int,"output",None,utils.integer_format(0),None,None),
        ("Wins",hx.Int,"output",None,utils.integer_format(0),None,None),
        ("Losses",hx.Int,"output",None,utils.integer_format(0),None,None),
        ("Mistrials",hx.Int,"output",None,utils.integer_format(0),None,None),
        ("Win Pct",hx.Float,"output",None,utils.percent_format(2),None,None),
        ]
    return create_node_from_list(node_info_list) 

def _healthcare_cat_exposure_territory_single_nodes():
    node_info_list = [
        ("Type of business",hx.Str,"input","",None,[rarc_task_name,"start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),
        ("Specialty",hx.Str,"input","",None,[rarc_task_name,"start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),
        ("Choose split by",hx.Str,"input","",None,[rarc_task_name,"start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),


        ]
    return create_node_from_list(node_info_list)

def _healthcare_cat_exposure_per_year_nodes():
    node_info_list = [
        ("Display YOA",hx.Str,"output",None,None,[rarc_task_name, "start_renewal_task"],None),
        ("UW Year",hx.Int,"output",None,None,[rarc_task_name, "start_renewal_task"],None),
        ("Physicians",hx.Int,"input",0,utils.integer_format(0),[rarc_task_name, "start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),
        ("Professional Associations",hx.Int,"input",0,utils.integer_format(0),[rarc_task_name, "start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),
        ("Ambulatory Surgery Centres",hx.Int,"input",0,utils.integer_format(0),[rarc_task_name, "start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),
        ("Hospitals",hx.Int,"input",0,utils.integer_format(0),[rarc_task_name, "start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),
        ("LTC Facilities",hx.Int,"input",0,utils.integer_format(0),[rarc_task_name, "start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),
        ("Other Facilities",hx.Int,"input",0,utils.integer_format(0),[rarc_task_name, "start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),
        ("Dentists",hx.Int,"input",0,utils.integer_format(0),[rarc_task_name, "start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),
        ("Others",hx.Int,"input",0,utils.integer_format(0),[rarc_task_name, "start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),
        ("Total Physicians In Force",hx.Int,"output",None,utils.integer_format(0),[rarc_task_name, "start_renewal_task"],None),



        ]
    return create_node_from_list(node_info_list) 

def _healthcare_cat_exposure_split_by_state_nodes():
    node_info_list = [
        ("Venue",hx.Str,"output",None,None,None,None),
        ("Premium Written",hx.Float,"input",0,utils.thousands_format(0),[rarc_task_name, "start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),
        ("Total PIF Current Year",hx.Float,"input",0,utils.thousands_format(0),[rarc_task_name, "start_renewal_task"],[{"task": "start_renewal_task", "reset": False}]),
        ("Split",hx.Float,"output",None,utils.percent_format(0),None,None),
        ]
    return create_node_from_list(node_info_list) 

def _healthcare_cat_pricing_loss_distribution_children():
    node_info_list = [
        ("Mean CAT ULR",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("Decay Factor",hx.Float,"output",None,utils.thousands_format(4),None,None),
        ("Loss Ratio 1 in 50",hx.Float,"output",None,utils.percent_format(2),None,None),

        ]
    return create_node_from_list(node_info_list)

def _healthcare_cat_pricing_loss_distribution_list_children():
    node_info_list = [
        ("Loss Percentile Display",hx.Str,"output",None,None,None,None),
        ("Loss Percentile",hx.Float,"output",None,utils.percent_format(0),None,None),
        ("ULR",hx.Float,"output",None,utils.percent_format(2),None,None),

        ]
    return create_node_from_list(node_info_list)

def _healthcare_cat_pricing_calculation_loss_distribution_list_children():
    node_info_list = [
        ("Band Size",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("Loss Percentile",hx.Float,"output",None,utils.percent_format(2),None,None),
        ("ULR",hx.Float,"output",None,utils.percent_format(2),None,None),
        ]
    no_suffix_list =[
        ("FGU Expected Cat Loss",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Expected Loss in Layer",hx.Float,"output",None,utils.thousands_format(0),None,None),
        ("Expected Loss x Prob of loss",hx.Float,"output",None,utils.thousands_format(0),None,None),
    ]
    layer_nodes = []
    for index in range (max_layers):
        suffix = f'_{index+1:02d}'
        for item in no_suffix_list:
            updated_item = (item[0] + suffix,) + item[1:]
            layer_nodes.append(updated_item)

    node_info_list.extend(layer_nodes)


    return create_node_from_list(node_info_list) 
