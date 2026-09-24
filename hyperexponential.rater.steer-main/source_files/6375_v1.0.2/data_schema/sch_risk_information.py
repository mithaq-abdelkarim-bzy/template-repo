# v0.5.0
import hx_data_schema as hx
import data_schema.sch_utilities as utils

def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {                                
        "risk_information": hx.Structure(view={"label":"Risk Information"}, children={
            ** _sch_risk_information(),
        }),
        "metadata": hx.Structure(view={"label":"Meta data"}, children={
            ** _sch_metadata(),
        })
    })

def _sch_risk_information():
    return {
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),
        "case_pricing_analysis_location": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Case Pricing Analysis Filepath"}),
        "inception_year": hx.Float(mode="output", view={"label": "Inception Year", "format": utils.integer_format()}),
        "include_aad": hx.Bool(mode="input", default=False, async_input=["advanced_features_task"],view={"label": "Include AAD"}),
        "include_loss_corridor": hx.Bool(mode="input", default=False, async_input=["advanced_features_task"], view={"label": "Include Loss Corridor"}),
        "include_ncb": hx.Bool(mode="input", default=False, async_input=["advanced_features_task"], view={"label": "Include NCB"}),
        "include_swing_rates": hx.Bool(mode="input", default=False, async_input=["advanced_features_task"], view={"label": "Include Swing Rates"}),  
        "include_profit_commission": hx.Bool(mode="input", default=False, async_input=["advanced_features_task"], view={"label": "Include Profit Commission"}),  
        
        "comments": hx.Str(mode="input", default="", view={"label": "Comments"}),            
    } 

def _sch_metadata():
    return {
        "policy_option_id": hx.Int(mode="output", view={"label": "Policy Option ID", "format": utils.integer_format(0)}),
        # "rater": hx.Str(mode="input", default="STEER", optionality="optional", options=["STEER","Healthcare CAT","Clash"], view={"label": "Rater"}),
        "rater": hx.Str(mode="input", default="STEER", optionality="optional", options=["STEER","Healthcare CAT","Clash"], view={"label": "Rater"}),        
        "model_version_id": hx.Int(mode="output", view={"label": "Policy Option ID", "format": utils.integer_format(0)}), 
        "skeleton_version": hx.Str(mode="input", default="0.5.1", optionality="optional", view={"label": "Skeleton Version"}),        
    } 


 