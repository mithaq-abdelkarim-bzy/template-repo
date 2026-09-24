import hx_data_schema as hx
import data_schema.sch_utilities as utils
import algorithms.rate_constants as const

def sch_rationale(cds):
    cds.extend_node_rater_defined("cds", {
        "comment_tool": hx.Structure(children={
            # Selecting the input comment
            "input_comment":  hx.Str(mode="input", default=None, async_input=["process_comment_task"], optionality="optional", options=const.comment_dropdown, view={"label": "Selected Comment"}),
            # Document for saving comments to
            "document": hx.File(mode="output", async_output=["process_comment_task"], file_name="comment_doc.docx", view={"label": "Document"}),
        }),

        "file_upload_1": hx.File(mode="input", view={"label": "Upload Supporting Files e.g. JPEG Images"}),
        "file_upload_2": hx.File(mode="input", view={"label": "Upload Supporting Files e.g. JPEG Images"}),
        "file_upload_3": hx.File(mode="input", view={"label": "Upload Supporting Files e.g. JPEG Images"}),
        "file_upload_4": hx.File(mode="input", view={"label": "Upload Supporting Files e.g. JPEG Images"}),
        "file_upload_5": hx.File(mode="input", view={"label": "Upload Supporting Files e.g. JPEG Images"}),
        "file_upload_6": hx.File(mode="input", view={"label": "Upload Supporting Files e.g. JPEG Images"}),
        "file_upload_7": hx.File(mode="input", view={"label": "Upload Supporting Files e.g. JPEG Images"}),
        "file_upload_8": hx.File(mode="input", view={"label": "Upload Supporting Files e.g. JPEG Images"}),
    })
    ## Comments tasks ##
    cds.override_node_properties('cds/comment_tool/input_comment',{'async_input':['process_comment_task']})
    # cds.override_node_properties('cds/standard_fields/uw_rationale',{'async_input':['process_comment_task'], 'async_output':['process_comment_task']})
    # cds.override_node_properties('cds/comment',{'async_input':['process_comment_task']})
    # cds.override_node_properties('cds/claims_history',{'async_input':['process_comment_task'], 'async_output':['process_comment_task']})
    # cds.override_node_properties('cds/t_and_c_comment',{'async_input':['process_comment_task'], 'async_output':['process_comment_task']})

    cds.override_node_properties('cds/standard_fields/uw_rationale',{'async_input':['process_comment_task'], 'async_output':[{'task':'process_comment_task', 'reset': False}]})
    cds.override_node_properties('cds/comment',{'async_input':['process_comment_task'], 'async_output':[{'task':'process_comment_task', 'reset': False}]})
    cds.override_node_properties('cds/claims_history',{'async_input':['process_comment_task'], 'async_output':[{'task':'process_comment_task', 'reset': False}]})
    cds.override_node_properties('cds/t_and_c_comment',{'async_input':['process_comment_task'], 'async_output':[{'task':'process_comment_task', 'reset': False}]})
    cds.override_node_properties('cds/modifiers/management_corp_gov/comment',{'async_input':['process_comment_task'], 'async_output':[{'task':'process_comment_task', 'reset': False}]})
    cds.override_node_properties('cds/modifiers/business_financial_model_factors/comment',{'async_input':['process_comment_task'], 'async_output':[{'task':'process_comment_task', 'reset': False}]})
    cds.override_node_properties('cds/modifiers/significant_event_factors/comment',{'async_input':['process_comment_task'], 'async_output':[{'task':'process_comment_task', 'reset': False}]})
    cds.override_node_properties('cds/modifiers/stock_market_factors/comment',{'async_input':['process_comment_task'], 'async_output':[{'task':'process_comment_task', 'reset': False}]})
    cds.override_node_properties('cds/modifiers/derivative/comment',{'async_input':['process_comment_task'], 'async_output':[{'task':'process_comment_task', 'reset': False}]})
    cds.override_node_properties('cds/modifiers/regulatory/comment',{'async_input':['process_comment_task'], 'async_output':[{'task':'process_comment_task', 'reset': False}]})
    cds.override_node_properties('cds/modifiers/ma/comment',{'async_input':['process_comment_task'], 'async_output':[{'task':'process_comment_task', 'reset': False}]})
    cds.override_node_properties('cds/key_industry/sector_uw_override_comment',{'async_input':['process_comment_task'], 'async_output':[{'task':'process_comment_task', 'reset': False}], "view": {"multiline": True}})
    cds.override_node_properties('cds/key_industry/sector_uw_override_comment_2',{'async_input':['process_comment_task'], 'async_output':[{'task':'process_comment_task', 'reset': False}], "view": {"multiline": True}})
    cds.override_node_properties('cds/key_industry/sector_uw_override_comment_3',{'async_input':['process_comment_task'], 'async_output':[{'task':'process_comment_task', 'reset': False}], "view": {"multiline": True}})
    cds.override_node_properties('cds/exposure/aggregate/revised_market_cap_comment',{'async_input':['process_comment_task'], 'async_output':[{'task':'process_comment_task', 'reset': False}], "view": {"multiline": True}})
    cds.override_node_properties('cds/exposure/aggregate/ipo_date_comment',{'async_input':['process_comment_task'], 'async_output':[{'task':'process_comment_task', 'reset': False}], "view": {"multiline": True}})