import hx_data_schema as hx
import data_schema.sch_utilities as utils
from hx import params as hx_params



def sch_tech_eo(cds):
    #----------------------------------------------------------------------------------------------#
    # Total Tech_EO exposure set out in exposure aggregate node
    #----------------------------------------------------------------------------------------------#
    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        "tech_eo_rateble_revenue": hx.Float(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], default=1, optionality="required", view={"label": "Rateable Revenue %","format":utils.percent_format(0)}, validation={"min_value": 0, "max_value": 1}),
        "tech_eo_total_revenue": hx.Float(mode="output", view={"label": "Total Revenue Allocation","format":utils.percent_format(0)}),
    })
    
    
    #----------------------------------------------------------------------------------------------#
    # Individual Tech_EO exposures set out in exposure granular node
    #----------------------------------------------------------------------------------------------
    cds.extend_node_rater_defined("cds/exposure/granular", {
        **{item: hx.Structure(view ={"label": label}, children = {
            "tech_eo_percent_rateble_revenue": hx.Float(mode="input", async_input=["rarc_task","generate_email_task","generate_referral_email_task"], default=0, optionality="required", view={"label": "% of Rateable Revenue","format":utils.percent_format(0)}, validation={"min_value": 0, "max_value": 1}),
            "tech_eo_class": hx.Float(mode="output", view={"label": "Class","format":utils.integer_format(0)}, async_input=["generate_email_task","generate_referral_email_task"]),
            "tech_eo_revenue": hx.Float(mode="output", view={"label": "Revenue","format":utils.thousands_format(0)}, async_input=["generate_email_task","generate_referral_email_task"]),
        }) for item, label in zip(hx_params.table_tech_eo["industry_class_name"], hx_params.table_tech_eo["industry_class_label"])},

        
    })