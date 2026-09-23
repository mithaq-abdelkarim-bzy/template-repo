import hx_data_schema as hx
import data_schema.sch_utilities as utils
from hx import params as hx_params
from libraries.common_data_schema.algorithms import parameter_tables_schema as hx_cds_params

# Replace / remove examples with your models exposures

def sch_rating_factors(cds):

    cds.extend_node_rater_defined("cds", { 

        # dfine rating factors
        "rating_factors":  hx.Structure(children = {

            # define E&O Rating Factors
            "eo_territory": hx.Structure( children={
                "input_value": hx.Str(mode = "input", async_input=["rarc_task"],default = None, optionality = "optional",options_table = "table_eo_territory", options_column = "territory", view = {"label": "Territory"}),
                "relativity": hx.Float(mode = "output"),
            }),    
            
            "eo_size_relativity": hx.Float(mode = "output"), 


            "eo_prior_knowledge": hx.Structure(view = {"label": "Prior Knowledge Date"}, children={
                "input_value": hx.Str(mode = "input", default = "Two years",async_input=["rarc_task"] , options_table = "table_eo_prior_knowledge", options_column = "prior_knowledge", view = {"label": "Description"}),
                "relativity": hx.Float(mode = "output",  view = {"label": "Applied Relativity"})
            }),
            "eo_cost_included": hx.Structure(view = {"label": "Cost Included"}, children={
                "input_value": hx.Str(mode = "input", default = "Yes", async_input=["rarc_task"] , options_table = "table_eo_cost_included", options_column = "cost_included", view = {"label": "Description"}),
                "relativity": hx.Float(mode = "output",  view = {"label": "Applied Relativity"})
            }),

            # Media Tech rating factors
            "mediatech_territory": hx.Structure(children={
                "input_value": hx.Str(mode = "input", default = None,async_input=["rarc_task"] , optionality = "optional",options_table = "table_eo_territory", options_column = "territory", view = {"label": "Territory"}),
                "relativity": hx.Float(mode = "output"),
            }),
                

            "mediatech_prior_acts": hx.Structure(view = {"label": "Retroactivity"}, children={
                "coverage": hx.Str(mode = "input", default = "Unlimited",async_input=["rarc_task"] , options = ["Unlimited", "Specific Date"] , view = {"label": "Retroactive Date"}),
                "retroactive_date": hx.Date(mode = "input", default = None,async_input=["rarc_task"] , optionality = "optional", view = {"label": "Retroactive Start Date"}),
                "relativity": hx.Float(mode = "output", view = {"label": "Retroactivity Relativity"}),
                "shown_by": hx.Bool(mode = "output")

            }),

            "mediatech_longevity": hx.Structure(children= {
                "business_years": hx.Str(mode = "input", default = "3-9 Years",  async_input=["rarc_task"] , options_table = "table_mediatech_longevity", options_column = "year_in_business_name", view = {"label": "Years in Business from Inception"}),
                "relativity": hx.Float(mode = "output", view = {"label": "Business Longevity Relativity"}),
            }),



            "mediatech_cost_included":hx.Structure(view = {"label": "Claim Experience"}, children={
                "cost_included": hx.Str(mode = "input", default = "Yes",async_input=["rarc_task"] , options_table = "table_mediatech_cost_included", options_column = "response", view = {"label": "Cost Included"}),
                "relativity":hx.Float(mode = "output",  view = {"label": "Cost Included Relativity"}),
            }),

            # GL rating factors
            "gl_territory": hx.Structure(children={
                "input_value": hx.Str(mode = "input", default = None, optionality = "optional",options_table = "table_eo_territory", options_column = "territory", view = {"label": "Territory"}),
            }),
            "gl_loss":hx.Structure(children={
                "input_value": hx.Str(mode = "input", optionality= "optional", async_input=["rarc_task"] , options_table="table_gl_product_loss_experience", options_column= "loss_experience", default = None, view = {"label": "Loss Experience Description"}),
                "relativity": hx.Float(mode = "output", view = {"label": "Relativity"})
            }), 


            "gl_excess_primary": hx.Structure(children= {
                "input_value": hx.Str(mode = "input", async_input=["rarc_task"] ,options = ["Primary", "Excess"], optionality="optional", default = None, view = {"label": "Excess/Primary"}),
                "excess_relativity": hx.Float(mode = "output")
            }),
            "gl_excess_show": hx.Bool(mode = "output")    

        }),

        # Define Modifiers 

        "modifiers": hx.Structure(children = {
            # EO Modifiers
            "eo_schedule_modifier": hx.Structure(view = {"label": "Program Modifier"}, children={
                "input_value": hx.Float(mode = "input", default = 0 , async_input=["rarc_task"],view = {"label": "User Input", "format": utils.percent_format(0)}),
                "min_rel": hx.Float(mode = "output",  view = {"label": "Minimum", "format": utils.percent_format(0)}),
                "max_rel": hx.Float(mode = "output",  view = {"label": "Maximum", "format": utils.percent_format(0)}),
                "applied_rel": hx.Float(mode = "output",  view = {"label": "Applied", "format": utils.percent_format(0)}),
            }), 
            "eo_insurance_history": hx.Structure(view = {"label": "Insurance History"}, children = {
                "input_value": hx.Str(mode = "input", default = "Other",  async_input=["rarc_task"], options_table = "table_eo_insurance_history", options_column = "insurance_history_list", view = {"label": "Description"}),
                "input_rel": hx.Float(mode = "input", async_input=["rarc_task"], default = None, optionality = "optional", view = {"label": "User Input Relativity"}),
                "output_class": hx.Str(mode = "output", view = {"label": "Insurance History"}),
                "min_rel": hx.Float(mode = "output",  view = {"label": "Minimum Relativity"}),
                "max_rel": hx.Float(mode = "output",  view = {"label": "Maximum Relativity"}),
                "default_rel": hx.Float(mode = "output",  view = {"label": "Default Relativity"}),
                "applied_rel": hx.Float(mode = "output",  view = {"label": "Applied Relativity"}),
            }),
            "eo_claim_history": hx.Structure(view = {"label": "Claims History"}, children = {
                "input_value": hx.Str(mode = "input", default = "None",async_input=["rarc_task"],  options_table = "table_eo_claim_history", options_column = "claim_history", view = {"label": "Description"}),
                "input_rel": hx.Float(mode = "input",default = None, async_input=["rarc_task"] , optionality = "optional", view = {"label": "User Input Relativity"}),
                "min_rel": hx.Float(mode = "output",  view = {"label": "Minimum Relativity"}),
                "max_rel": hx.Float(mode = "output",  view = {"label": "Maximum Relativity"}),
                "default_rel": hx.Float(mode = "output",  view = {"label": "Default Relativity"}),
                "applied_rel": hx.Float(mode = "output",  view = {"label": "Applied Relativity"}),
            }),
            # Media Tech Modifiers
            **{item: hx.Structure(view ={"label": label}, children = {
                "input_value": hx.Float(mode = "input", default = 0, async_input=["rarc_task"] ,view = {"label": "User Input", "format": utils.percent_format(0)}),
                "min_val": hx.Float(mode = "output",  view = {"label": "Minimum", "format": utils.percent_format(0)}),
                "max_val": hx.Float(mode = "output",  view = {"label": "Maximum","format": utils.percent_format(0)}),
                "default_val": hx.Float(mode = "output",  view = {"label": "Default","format": utils.percent_format(0)}),
                "applied_val": hx.Float(mode = "output",  view = {"label": "Applied", "format": utils.percent_format(0)}),
            }) for item, label in zip(hx_params.table_mediatech_schedule["schedule_name"], hx_params.table_mediatech_schedule["schedule_factor"])},

            "mediatech_total_schedule": hx.Structure(view={"label": "Total Schedule Modification"}, children={
                "input_value": hx.Float(mode = "output", view = {"label": "Selected", "format": utils.percent_format(0)}),
                "min_val": hx.Float(mode = "output",  view = {"label": "Minimum", "format": utils.percent_format(0)}),
                "max_val": hx.Float(mode = "output",  view = {"label": "Maximum","format": utils.percent_format(0)}),
                "default_val": hx.Float(mode = "output",  view = {"label": "Default","format": utils.percent_format(0)}),
                "applied_val": hx.Float(mode = "output",  view = {"label": "Applied", "format": utils.percent_format(0)}),                
            }),
            "mediatech_bipd": hx.Structure(view = {"label": "Contingent Bodily Injury / Property  Damage"}, children= {
                "input_value": hx.Str(mode = "input", default = "No",async_input=["rarc_task"] , options_table = "table_mediatech_bi_pd_cover", options_column = "contingent_bi_pd", view = {"label": "Included ?"}),
                "input_relativity": hx.Float(mode = "input", default = None, async_input=["rarc_task"] , optionality = "optional",  view = {"label": "User Input Relativity","format": utils.percent_format(0)}),
                "min_rel": hx.Float(mode = "output",  view = {"label": "Minimum Relativity", "format": utils.percent_format(0)}),
                "max_rel": hx.Float(mode = "output",  view = {"label": "Maximum Relativity", "format": utils.percent_format(0)}),
                "default_rel": hx.Float(mode = "output",  view = {"label": "Default Relativity", "format": utils.percent_format(0)}),
                "applied_rel": hx.Float(mode = "output",  view = {"label": "Applied Relativity", "format": utils.percent_format(0)}),
            }),
            "mediatech_claim_experience": hx.Structure(view = {"label": "Claim Experience"}, children={
                "input_value": hx.Str(mode = "input", default = "No claim activity",async_input=["rarc_task"] , options_table = "table_mediatech_claim_experience", options_column = "experience", view = {"label": "Activity"}),
                "input_relativity": hx.Float(mode = "input", default = None, async_input=["rarc_task"] ,optionality = "optional",   view = {"label": "User Input Relativity"}),
                "min_rel": hx.Float(mode = "output",  view = {"label": "Minimum Relativity"}),
                "max_rel": hx.Float(mode = "output",  view = {"label": "Maximum Relativity"}),
                "default_rel": hx.Float(mode = "output",  view = {"label": "Default Relativity"}),
                "applied_rel": hx.Float(mode = "output",  view = {"label": "Applied Relativity"}),

            
            }),


            # GL UW adjustment
            "gl_uw_adjustment": hx.Structure( view = {"label": "UW Judgement"}, children = {
                "input_value": hx.Float(mode = "input", default = 0, async_input=["rarc_task"] ,view = {"label": "User Input","format": utils.percent_format(0)}),
                "min_value": hx.Float(mode = "output", view = {"label":"Min","format": utils.percent_format(0)}),
                "max_value": hx.Float(mode = "output", view = {"label":"Max","format": utils.percent_format(0)}),
                "applied_value": hx.Float(mode = "output", view = {"label":"Applied","format": utils.percent_format(0)}),
            
            }),   

            
        }),
    
        "gl_tier_notes": hx.Structure(children= {
            "text_box": hx.Str(mode = "output"),
            "show_box": hx.Bool(mode = "input", view = {"label": "Show the Product Tiers Description"}, default = False),
            "stretch_box": hx.Bool(mode = "output")
        })


    })

