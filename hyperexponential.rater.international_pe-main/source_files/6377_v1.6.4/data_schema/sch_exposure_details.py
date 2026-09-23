import hx_data_schema as hx
import data_schema.sch_utilities as utils
from hx import params as hx_params
from libraries.common_data_schema.algorithms import parameter_tables_schema as hx_cds_params

# Replace / remove examples with your models exposures

def sch_exposure_details(cds):
    
    # For aggregate exposure e.g. total revenue, sum insured etc. please add to the aggregate exposures node
    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        
        # PLACEHOLDER value used in experience rating, the experience rating should connect to the total exposure value of the model
        # "exposure": hx.Float(mode="input", default=0, view={"label": "Exposure", "format": utils.thousands_format(0)}),

        #E&O fees
        "eo_total_fees": hx.Float(mode="input", default=0, async_input=["rarc_task"],view={"label": "Total Fees", "format": utils.thousands_format(0)}),
        #Media Tech revenue
        "mediatech_revenue": hx.Float(mode="input", default=0, async_input=["rarc_task"], view={"label": "Total Revenue", "format": utils.thousands_format(0)}),
        #GL revenue
        "gl_revenue": hx.Float(mode="output", view={"label": "Total Revenue in Source Currency", "format": utils.thousands_format(0)}),
        
    })

    
    cds.extend_node_rater_defined("cds/exposure/granular", {   
        ############################################################################################
        # Define E&O covers variables
        ############################################################################################           

        "eo_profession": hx.Str(mode = "input", default = None, optionality = "optional", options_table = "table_eo_profession", options_column = "profession", view = {"label": "Profession"} ),
        "eo_ae_operaion_shownby": hx.Bool(mode = "output",view = {"label": "A&E operation table shown by flag"} ),
        "eo_exposure_shownby": hx.Bool(mode = "output",view = {"label": "E&O exposure table shown by flag"} ),

        "eo_total_fees_pct": hx.Float(mode = "output", view = {"label": "Total Fees %", "format": utils.percent_format(0)}),
        "eo_ae_operation_pct": hx.Float(mode = "output", view = {"label": "Total A&E Operation %", "format": utils.percent_format(0)}),
        "eo_total_base_rate_relativity": hx.Float(mode = "output",view={"label": "Total Base Rate for Premium Calculation", "format": utils.thousands_format(0)}),

        # The following is to get the E&O cover discipline variable
        **{
            item: hx.Structure(view ={"label": label}, children = {
            "input_pct": hx.Float(mode = "input", default = 0, async_input=["rarc_task", "clear_eo_input_task"], async_output=["clear_eo_input_task"],view = {"label": "Percentage of Fees (%)", "format": utils.percent_format(1)}),
            "relativity":hx.Float(mode="output", view = {"label": "Relativity"}),
            "show_row": hx.Bool(mode = "output",view = {"label": label} ),
            }) 
            for item, label in zip(hx_params.table_eo_discipline["discipline_name"], hx_params.table_eo_discipline["discipline_label"])
        },

        # Define the A&E operation variable
        **{item: hx.Structure(view ={"label": label}, children = {
            "input_pct": hx.Float(mode = "input", default = 0, async_input=["rarc_task","clear_eo_input_task"],async_output=["clear_eo_input_task"],view = {"label": "Percentage of Fees (%)", "format": utils.percent_format(1)}),
            "relativity":hx.Float(mode="output", view = {"label": "Relativity"}),
            "show_row": hx.Bool(mode = "output",view = {"label": label} ),
        }) for item, label in zip(hx_params.table_eo_ae_operation["ae_operations_name"], hx_params.table_eo_ae_operation["ae_operations"])},


        ############################################################################################
        # Define Media Tech covers variables
        ############################################################################################


        "mediatech_total_revenue_pct": hx.Float(mode = "output", view = {"label": "Total Revenue %", "format": utils.percent_format(0)}),
        "mediatech_max_class": hx.Float(mode = "output"),
        "mediatech_total_base_rate_relativity": hx.Float(mode = "output",view={"label": "Total Base Rate for Premium Calculation", "format": utils.thousands_format(0)}),
                
        # Get the industry name
        **{item: hx.Structure(view ={"label": label}, children = {
            "input_pct": hx.Float(mode = "input", default = 0, async_input=["rarc_task","clear_mediatech_input_task"] , async_output=["clear_mediatech_input_task"], view = {"label": "Percentage of Revenue (%)", "format": utils.percent_format(1)}),
            "revenue_amount":hx.Float(mode="output", view = {"label": "Revenue","format": utils.thousands_format(0)}),
            "class_name": hx.Float(mode = "output",view = {"label": "Industry Class", "format": utils.thousands_format(0)} ),
        }) for item, label in zip(hx_params.table_mediatech_industry["industry_name"], hx_params.table_mediatech_industry["industry_description"])},



        ############################################################################################
        # Define GL coverage
        ############################################################################################

        "gl_product": hx.Str(mode = "output", view = {"label": "Product Type"}),
        "gl_exposure_info": hx.Structure(children={
            "product_type": hx.Str(mode = "output", view = {"label": "Product Type"}),
            "occupation": hx.Str(mode = "input", optionality="optional",async_input=["rarc_task"] , options_table = "table_gl_product_occupation", options_column="occupation_description", default = None, view = {"label": "Occupation"} ),
        }),

        "gl_revenue": hx.List(mode="input", default_element_count=3, view={"label": "Revenue Tiers"}, children={
            "tier_input": hx.Str(mode = "input",optionality= "optional",async_input=["rarc_task"] , options_table="table_gl_product_tier", options_column= "tier_description", default = None, view = {"label": "Tier"} ),
            "revenue_input": hx.Float(mode = "input", default = 0, async_input=["rarc_task"] ,view = {"label": "Revenue in Source Currency", "format": utils.thousands_format(0)}),
            "revenue_input_usd": hx.Float(mode = "output", view = {"label": "Revenue Converted to $ USD", "format": utils.thousands_format(0)}),
            "revenue_base_rate": hx.Float(mode = "output"),
            "exposure_type": hx.Str(mode = "input",optionality= "optional", options_table="table_gl_product_exposure_type", options_column= "exposure_type_description", default = None, async_input=["rarc_task"] ,view = {"label": "Type"} ),
            "tier_relativity": hx.Float(mode = "output"),
            "type_relativity": hx.Float(mode = "output"),
            "total_relativity": hx.Float(mode = "output"),
        }),
    })


