import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from libraries.common_data_schema.algorithms import parameter_tables_schema as params
from algorithms.rate_constants import max_layers, max_options
from hx import params as hx_params
import data_schema.sch_utilities as utils

def sch_rating_summary(cds):

    cds.extend_node_rater_defined("cds", {
        "override_terms_to_display": hx.Str(mode="input", default="All", options=["All","Product Liability","E&O","Healthcare Professional Liability","General Liability","Sexual Abuse","Employee Benefits Liability","Product Recall Expenses","Tech E&O/Products/Media"], view={"label": "Override terms to display:"}),
    })

    #----------------------------------------------------------------------------------------------#
    # Standard layers structuring
    #----------------------------------------------------------------------------------------------#
    #Add rater specific elements to the layers node
    cds.extend_node_rater_defined("cds/layers", {
            "layer_label": hx.Str(mode="output", view={"label": "Layer Label"}, async_input=["generate_excess_proposal_template_task"]),
            "gross_premium":hx.Float(mode="output", view={"label": "Gross Premium","format":utils.thousands_format(0)}),
            # Added variable to record a bpi where the risk is case priced. Do not remove as used in tpi summary. 
            "bpi_case_priced": hx.Float(mode="input", default=None, optionality="optional", view={"label": "BPI (Case Priced)", "format": utils.percent_format(1)}),
            "quoted_rate":hx.Float(mode="output", view={"label": "Quoted Rate","format":utils.percent_format(0)}),
            "bound_premium": hx.Float(mode="input", optionality="optional", default=None, view={"label": "Bound Premium", "format":utils.thousands_format(0)}, async_input=["expiring_policy_fetch_task","rarc_task","generate_email_task","generate_referral_email_task", "generate_excess_proposal_template_task"], async_output=[{"task": "initialise_model", "reset": False}], validation={"min_value": 0, "max_value": 1000000000}),
            "bound_rate":hx.Float(mode="output", view={"label": "Bound Rate","format":utils.percent_format(0)}),
            "net_written_premium":hx.Float(mode="output", view={"label": "Net Written Premium","format":utils.thousands_format(0)}, async_input=["generate_email_task","generate_referral_email_task"]),
            "show_row": hx.Bool(mode="output", view={"label": "Show Row"}),
            "limit_case_priced": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Limit","format":utils.thousands_format(0)}, async_input = ["generate_email_task","generate_referral_email_task"]),
            "excess_case_priced": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Excess","format":utils.thousands_format(0)}, async_input = ["generate_email_task","generate_referral_email_task"]),
            "brokerage_case_priced": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Brokerage","format":utils.percent_format(2)}, async_input = ["rarc_task","generate_email_task","generate_referral_email_task"])
        })
    #Changing the name of some nodes to align with rater descriptions
    cds.override_node_properties("cds/layers/limit", { "mode": "output","view":{"label":"Each Loss Limit"}, "async_input" : ["generate_email_task","generate_referral_email_task", "generate_excess_proposal_template_task"] })
    cds.override_node_properties("cds/layers/aggregate_limit", { "mode": "output", "async_input" : ["generate_email_task","generate_referral_email_task", "generate_excess_proposal_template_task"]})
    cds.override_node_properties("cds/layers/brokerage", { "mode": "output", "async_input" : ["rarc_task","generate_email_task","generate_referral_email_task", "generate_primary_proposal_template_task"],"view":{"format": utils.percent_format(2)} })
    cds.override_node_properties("cds/layers/model_premium", { "mode": "output","view":{"label":"Model Premium"}, "async_input" : ["generate_email_task","generate_referral_email_task"] })
    cds.override_node_properties("cds/layers/quoted_premium", { "mode": "output", "async_input" : ["rarc_task","generate_email_task","generate_referral_email_task", "generate_excess_proposal_template_task"] ,"view":{"label":"Quoted Premium"}})
    cds.override_node_properties("cds/layers/benchmark_premium", { "mode": "output" , "async_input" : ["rarc_task","generate_email_task","generate_referral_email_task"],"view":{"label":"Benchmark Premium"}})
    cds.override_node_properties("cds/layers/technical_premium", { "mode": "output" , "async_input" : ["rarc_task","generate_email_task","generate_referral_email_task"],"view":{"label":"Technical Premium"}})
    cds.override_node_properties("cds/layers/bpi", { "async_input" : ["generate_email_task","generate_referral_email_task"],"view":{"format": utils.percent_format(0)}})
    cds.override_node_properties("cds/layers/tpi", { "async_input" : ["generate_email_task","generate_referral_email_task"],"view":{"format": utils.percent_format(0)}})
    cds.override_node_properties("cds/layers/section_reference", { "async_input" : ["generate_email_task","generate_referral_email_task"],"async_output" : [{"task": "initialise_model", "reset": False}],"view":{"label":"Policy Reference"}})
    
        
    
    # Override values
    cds.override_node_properties("cds/layers", {"default_element_count": max_layers + 2})
    cds.override_node_properties("cds/layers/status", {"async_input" : ["generate_email_task","generate_referral_email_task", "generate_excess_proposal_template_task"], "async_output" : [{"task": "initialise_model", "reset": False}],
        "view": {"options": {
        "input": {"label": "Status"},
        "read_only": {"label": "Deal Status by Renewal Layers", "read_only": True}
    }}})

    cds.override_node_properties("cds/layers/bpi_case_priced", {"default": 0, "optionality": "required"})

    #----------------------------------------------------------------------------------------------#
    # Structure housing schedule modifiers
    #----------------------------------------------------------------------------------------------#
    cds.extend_node_rater_defined("cds", {
        "modifiers": hx.Structure(view ={"label": "Schedule Modifiers"}, children = {
            "cyber": hx.Structure(view ={"label": "Schedule Modifiers"}, children = {
                **{item: hx.Structure(view={"label": label}, children={
                    "min":hx.Float(mode = "output", view = {"label": "Min","format":utils.percent_format(0)}),
                    "max":hx.Float(mode = "output", view = {"label": "Max","format":utils.percent_format(0)}),
                    "value":hx.Float(mode = "input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], optionality="optional",default = None, view = {"label": "Value","format":utils.percent_format(0)}),
                    "comment": hx.Str(mode = "input", optionality="optional",default = None,view={"label": "Comments"}, async_input=["generate_email_task","generate_referral_email_task"]),
                    })for item, label in zip(hx_params.table_cyber_schedule_rating["description_name"], hx_params.table_cyber_schedule_rating["description_label"])},

                "cyber_loss_rating": hx.List(mode="input",max_element_count=1, children={
                    "cyber_loss_ratio": hx.Str(mode = "input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], optionality="required",default = "No Losses",options_table = "table_cyber_loss_rating", options_column = "loss_ratio", view = {"label": "Loss Ratio"}),
                    "cyber_loss_ratio_min": hx.Float(mode = "output", view = {"label": "Min","format":utils.integer_format(2)}),
                    "cyber_loss_ratio_max": hx.Float(mode = "output", view = {"label": "Max","format":utils.integer_format(2)}),
                    "cyber_loss_ratio_selected": hx.Float(mode = "override", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], view = {"label": "Selection","format":utils.integer_format(2)}),
                    }),    
            }),

            "gmm": hx.Structure(view ={"label": "Schedule Modifiers"}, children = {
                **{item: hx.Structure(view ={"label": label}, children = {
                "min":hx.Str(mode = "output", view = {"label": "Min","format":utils.percent_format(0)}, async_input=["generate_email_task","generate_referral_email_task"]),
                "max":hx.Str(mode = "output", view = {"label": "Max","format":utils.percent_format(0)}, async_input=["generate_email_task","generate_referral_email_task"]),
                "value":hx.Float(mode = "output", view = {"label": "Value","format":utils.percent_format(0)}, async_input=["rarc_task","generate_email_task","generate_referral_email_task"]),
                "comment": hx.Str(mode = "output", view={"label": "Comments"}, async_input=["generate_email_task","generate_referral_email_task"]),
                }) if item == "total_schedule_rating" else
                hx.Structure(view ={"label": label}, children = {
                "min":hx.Str(mode = "output", view = {"label": "Min","format":utils.percent_format(0)}, async_input=["generate_email_task","generate_referral_email_task"]),
                "max":hx.Str(mode = "output", view = {"label": "Max","format":utils.percent_format(0)}, async_input=["generate_email_task","generate_referral_email_task"]),
                "value":hx.Float(mode = "input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], optionality="optional",default = None, view = {"label": "Value","format":utils.percent_format(0)}),
                "comment": hx.Str(mode = "input", optionality="optional",default = None,view={"label": "Comments"}, async_input=["generate_email_task","generate_referral_email_task"]),
                })
                for item, label in zip(hx_params.table_gmm_schedule_mods["description_name"], hx_params.table_gmm_schedule_mods["description_label"])},
            }),

            "glsn": hx.Structure(view ={"label": "Schedule Modifiers"}, children = {
                **{item: hx.Structure(view ={"label": label}, children = {
                "min":hx.Str(mode = "output", view = {"label": "Min","format":utils.percent_format(0)}, async_input=["generate_email_task","generate_referral_email_task"]),
                "max":hx.Str(mode = "output", view = {"label": "Max","format":utils.percent_format(0)}, async_input=["generate_email_task","generate_referral_email_task"]),
                "value":hx.Float(mode = "output", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], view = {"label": "Value","format":utils.percent_format(0)}),
                "comment": hx.Str(mode = "output", view={"label": "Comments"}, async_input=["generate_email_task","generate_referral_email_task"]),
                }) if item == "total_schedule_rating" else
                hx.Structure(view ={"label": label}, children = {
                "min":hx.Str(mode = "output", view = {"label": "Min","format":utils.percent_format(0)}, async_input=["generate_email_task","generate_referral_email_task"]),
                "max":hx.Str(mode = "output", view = {"label": "Max","format":utils.percent_format(0)}, async_input=["generate_email_task","generate_referral_email_task"]),
                "value":hx.Float(mode = "input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], optionality="optional",default = None, view = {"label": "Value","format":utils.percent_format(0)}),
                "comment": hx.Str(mode = "input", optionality="optional",default = None,view={"label": "Comments"}, async_input=["generate_email_task","generate_referral_email_task"]),
                }) 
                for item, label in zip(hx_params.table_glsn_schedule_mods["description_name"], hx_params.table_glsn_schedule_mods["description_label"])},
            }),
        })
    })
    

