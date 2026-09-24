import hx_data_schema as hx
import data_schema.sch_utilities as utils
from hx import params as hx_params

def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {                                
        # Do not remove
        "policy_option_id": hx.Int(mode="output", view={"label": "Policy Option ID", "format": utils.integer_format(0)}),
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),
        "case_pricing_analysis_location": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Case Pricing Analysis Filepath"}),
        # ~~~~~

        # Account Details
        "application_date" : hx.Date(mode="input", optionality="optional", default=None, view={"label": "Application Date"}),
        "retroactive_date" : hx.Date(mode="input", optionality="optional", default=None, view={"label": "Retroactive Date"}),
        # "binder_reference" : hx.Str(mode="input", optionality="optional", default=None, view={"label": "Binder Reference"}),
        # "deal_status" : hx.Str(mode="input", optionality="optional", default=None, options=["Submission", "Quoted", "Bound", "Declined"], view={"label": "Deal Status"}), # Shown at bottom of Pricing tab.

        # Risk Details
        "coverage_name" : hx.Str(mode="input", optionality="optional", default=None, options=hx_params.lst_coverages["coverage_name"].tolist(), view={"label": "Coverage Name"}),
        "is_binder" : hx.Str(mode="input", default="No", options=["Yes", "No"], view={"label": "Is Binder?"}),
        "cyber_code" : hx.Str(mode="input", optionality="optional", options=hx_params.lst_cyber_code["cyber_code"].tolist(), default=None, view={"label": "Cyber Code"}),
        "clearance_status" : hx.Str(mode="input", optionality="optional", default=None, options=["Quotable", "Blocked"], view={"label": "Clearance Status"}),
        "clearance_date" : hx.Date(mode="input", optionality="optional", default=None, view={"label": "Clearance Date"}),

        # Comments
        "riskinfo_comments" : hx.Str(mode="input", optionality="optional", default=None, view={"label": ""}),
        # Email nodes
        "email": hx.Structure(children={
            "data_dict": hx.Str(mode="output", async_input=["generate_email_task"]),
            "rationale_file": hx.File(mode="output", async_output=["generate_email_task"], file_name="Rationale_Summary.eml", view={"label": "Click to download summary email"}),
            "referral_file": hx.File(mode="output", async_output=["generate_email_task"], file_name="Referral_Summary.eml", view={"label": "Click to download summary email"}),
            "sender": hx.Str(mode="input", default="your_uw@beazley.com", async_input=["generate_email_task"], async_output=[{"task": "generate_email_task", "reset": True}, {"task": "generate_referral_email_task", "reset": True}], view={"label": "Sender"}),
            "recipient": hx.Str(mode="input", default="uw_assistant@beazley.com", async_input=["generate_email_task"], async_output=[{"task": "generate_email_task", "reset": True}, {"task": "generate_referral_email_task", "reset": True}], view={"label": "Recipient"}),
            "show_download": hx.Bool(mode="output",  async_input=["generate_email_task"], async_output=[{"task": "generate_email_task", "reset": True}]),
        }),
    })


    # Override default properties for standard fields ---------------------

    # is_renewal - set to async output
    cds.override_node_properties('cds/standard_fields/is_renewal', {"async_output": ["start_renewal_task"]})    
