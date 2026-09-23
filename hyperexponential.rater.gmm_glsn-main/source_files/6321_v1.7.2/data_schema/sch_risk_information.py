import hx_data_schema as hx
import data_schema.sch_utilities as utils

def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {
        # Account Details 
        "database_id": hx.Int(mode="output", view={"label": "Database ID", "format": utils.integer_format(0)}),
                                
        # Broker Details
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),

        # Cyber Selection:
        "cyber_selection": hx.Bool(mode = "output"),

        # Tech EO Selection:
        "tech_eo_selection": hx.Bool(mode = "output"),

        # Case Pricing Analysis Location Box
        "case_pricing_analysis_location": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Case Pricing Analysis Filepath"}),

    })

    cds.extend_node_rater_defined('cds',{
        # is_real_renewal for carrying exposure from NTU policy
        "is_real_renewal": hx.Bool(mode = "output"),
        "expiry_inception_date": hx.Date(default="2018-01-01", mode="input", view={"label": "Expiry Inception Date"}, async_output=["roll_exposure_fields_task", "start_renewal_task","initialise_model"]),

    })

    # Override dropwown links
    cds.override_node_properties('cds/standard_fields/underwriter', {"options_table": "table_input_underwriters", "options_column": "underwriter", "allow_custom_value": True, "async_input" : ["generate_email_task","generate_referral_email_task","save_uw_to_pas_reference", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"]})
    
    # Override default values
    cds.override_node_properties('cds/currencies/source_currency', {"mode":"output", "async_input" : ["rarc_task","generate_email_task","generate_referral_email_task"]})
   
   # Override default values
    cds.override_node_properties('hx_core/inception_date', {"async_input" : ["rarc_task","generate_email_task","generate_referral_email_task","roll_exposure_fields_task","start_renewal_task","initialise_model", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"]})
    cds.override_node_properties('hx_core/expiry_date', {"async_input" : ["rarc_task","generate_email_task","generate_referral_email_task", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"]})
    
    # insured name - set to async task
    cds.override_node_properties('cds/standard_fields/insured_name', {
        "options_table": "table_insured_name",
        "options_column": "firm_name",
        "allow_custom_value": True,
        "async_input": ["start_renewal_task","initialise_model", "generate_email_task","generate_referral_email_task", "generate_primary_proposal_template_task", "generate_excess_proposal_template_task"]
    })

    # is_renewal - set to async output
    cds.override_node_properties('cds/standard_fields/is_renewal', {"async_output": ["start_renewal_task","initialise_model"],"async_input": ["generate_email_task","generate_referral_email_task"]})    


