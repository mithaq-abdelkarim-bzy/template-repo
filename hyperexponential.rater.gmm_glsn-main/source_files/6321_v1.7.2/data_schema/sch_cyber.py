import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from libraries.common_data_schema.algorithms import parameter_tables_schema as params
from algorithms.rate_constants import max_layers, max_options
from hx import params as hx_params
import data_schema.sch_utilities as utils

def sch_cyber(cds):

    cds.extend_node_rater_defined("cds", {
        "bbr_masking": hx.Bool(mode="output", async_input=["cyber_copy_option"]),
        "infosec_masking":hx.Bool(mode="output", async_input=["cyber_copy_option"]),
        "cyber_copy_option_from": hx.Str(mode="input", async_input=["cyber_copy_option"], optionality="required",default="Option 1", options=["Option 1", "Option 2", "Option 3", "Option 4","Option 5","Option 6"], view={"label": "Option to copy from"}),
        "cyber_copy_option_to": hx.Str(mode="input", async_input=["cyber_copy_option"], optionality="required",default="Option 2", options=["Option 1", "Option 2", "Option 3", "Option 4","Option 5","Option 6"], view={"label": "Option to paste to"}),
    })

    #----------------------------------------------------------------------------------------------#
    # Cyber options defined in a new node, given the need for multiple options here
    #----------------------------------------------------------------------------------------------#  
    cds.extend_node_rater_defined("cds", {
        "cyber_options": hx.List(mode="input", default_element_count= max_options, fixed_element_count= max_options, view= {"label":"Options"}, children={
            "option_label": hx.Str(mode="output", view={"label": "Option"}),
            "notified_individuals_limit": hx.Float(mode = "input",allow_custom_value=True, async_input= ["rarc_task","cyber_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "cyber_copy_option", "reset": False}], optionality="optional",default = None,options_table = "table_cyber_notified_individual", options_column = "notified_individuals_limit", view = {"label": "Notified Individuals:","format":utils.thousands_format(0)}),
            "legal_forensic_limit": hx.Float(mode = "input",allow_custom_value=True, async_input= ["rarc_task","cyber_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "cyber_copy_option", "reset": False}], optionality="optional",default = None,options_table = "table_cyber_legal", options_column = "legal_forensic_limit", view = {"label": "Legal, Forensic & PR:","format":utils.thousands_format(0)}),
            "additional_breach_costs_limit": hx.Float(mode = "input",allow_custom_value=True, async_input= ["rarc_task","cyber_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "cyber_copy_option", "reset": False}], optionality="optional",default = None,options_table = "table_cyber_add_breach", options_column = "additional_breach_costs_limit", view = {"label": "Additional Breach Resp. Costs:","format":utils.thousands_format(0)}),
            "policy_agg_limit": hx.Float(mode = "input",allow_custom_value=True, async_input= ["rarc_task","cyber_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "cyber_copy_option", "reset": False}], optionality="optional",default = None,options_table = "table_cyber_policy_agg_limit", options_column = "policy_agg_limit_of_liability", view = {"label": "Policy Agg. Limit of Lia.:","format":utils.thousands_format(0)}),
            "infosec_breach_response_limit": hx.Float(mode = "input",allow_custom_value=True, async_input= ["rarc_task","cyber_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "cyber_copy_option", "reset": False}], optionality="optional",default = None,options_table = "table_cyber_policy_agg_limit", options_column = "policy_agg_limit_of_liability", view = {"label": "Breach Response Limit:","format":utils.thousands_format(0)}),
            "data_network_limit": hx.Float(mode = "input",allow_custom_value=True, async_input= ["rarc_task","cyber_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "cyber_copy_option", "reset": False}], optionality="optional",default = None,options_table = "table_cyber_data_network", options_column = "data_network_limit", view = {"label": "Data & Network Liability:","format":utils.thousands_format(0)}),
            "defense_penalties_limit": hx.Float(mode = "input",allow_custom_value=True, async_input= ["rarc_task","cyber_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "cyber_copy_option", "reset": False}], optionality="optional",default = None,options_table = "table_cyber_defense_penalties", options_column = "defense_penalties_limit", view = {"label": "Reg. Defense & Penalties:","format":utils.thousands_format(0)}),
            "payment_card_limit": hx.Float(mode = "input",allow_custom_value=True, async_input= ["rarc_task","cyber_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "cyber_copy_option", "reset": False}], optionality="optional",default = None,options_table = "table_cyber_card_liability", options_column = "card_liability_limit", view = {"label": "Payment Card Lia. & Costs:","format":utils.thousands_format(0)}),
            
            "legal_forensic_retention": hx.Float(mode = "input",allow_custom_value=True, async_input= ["rarc_task","cyber_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "cyber_copy_option", "reset": False}], optionality="optional",default = None,options_table = "table_cyber_legal_retention", options_column = "legal_forensic_retention", view = {"label": "Legal, Forensic & PR:","format":utils.thousands_format(0)}),
            "legal_forensic_subretention": hx.Float(mode = "input",allow_custom_value=True, async_input= ["rarc_task","cyber_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "cyber_copy_option", "reset": False}], optionality="optional",default = None,options_table = "table_cyber_subretention", options_column = "legal_subretention", view = {"label": "Legal Subretention:","format":utils.thousands_format(0)}),
            "policy_agg_retention": hx.Float(mode = "input",allow_custom_value=True, async_input= ["rarc_task","cyber_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "cyber_copy_option", "reset": False}], optionality="optional",default = None ,options_table = "table_cyber_agg_retention", options_column = "policy_agg_retention", view = {"label": "Agg. Per Incident, Claim, or Loss:","format":utils.thousands_format(0)}),
            "data_network_retention": hx.Float(mode = "override",async_input= ["rarc_task","generate_email_task","generate_referral_email_task"], view = {"label": "Data & Network Liability:","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000}),
            "defense_penalties_retention": hx.Float(mode = "override",async_input= ["rarc_task","generate_email_task","generate_referral_email_task"], view = {"label": "Reg. Defense & Penalties:","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000}),
            "payment_card_retention": hx.Float(mode = "override",async_input= ["rarc_task","generate_email_task","generate_referral_email_task"], view = {"label": "Payment Card Lia. & Costs:","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000}),
            "breach_response_retention": hx.Float(mode = "input", async_input= ["rarc_task","cyber_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "cyber_copy_option", "reset": False}], optionality="optional",default = None, view = {"label": "Breach Response Retention:","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000}),

            "brokerage":hx.Float(mode = "input", optionality="optional", async_input= ["rarc_task","cyber_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "cyber_copy_option", "reset": False}],default = None, view = {"label": "Brokerage","format":utils.percent_format(1)}, validation={"min_value": 0, "max_value": 1}),
            "model_premium_third_party_usd":hx.Float(mode = "output", view = {"label": "Model Premium: Third Party","format":utils.thousands_format(0)}),
            "model_premium_third_party":hx.Float(mode = "output", async_input= ["generate_email_task","generate_referral_email_task"], view = {"label": "Model Premium: Third Party Only","format":utils.thousands_format(0)}),
            "model_premium_first_party":hx.Float(mode = "output", async_input= ["generate_email_task","generate_referral_email_task"], view = {"label": "Model Premium: First Party","format":utils.thousands_format(0)}),
            "model_premium_bbr_rater":hx.Float(mode = "input", async_input= ["rarc_task","cyber_copy_option","generate_email_task","generate_referral_email_task"], async_output= [{"task": "cyber_copy_option", "reset": False}], optionality="optional",default = None, view = {"label": "Total Premium from BBR Rater","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000}),
            "model_premium_final":hx.Float(mode = "output", view = {"label": "Final Model Premium","format":utils.thousands_format(0)}, async_input= ["generate_email_task","generate_referral_email_task"]),
            **{f"model_premium_third_party_{label}_usd": hx.Float(mode="output",  view={"label": "Cyber Net Premium USD - Excess"}) for label in (["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])},
            **{f"model_premium_third_party_{label}": hx.Float(mode="output",  view={"label": "Cyber Net Premium USD - Excess"}, async_input= ["generate_email_task","generate_referral_email_task"]) for label in (["1_excess",  "2_excess", "3_excess", "4_excess","5_excess","6_excess","7_excess","8_excess","9_excess","10_excess"])},

            })
        })  





          
        