import hx_data_schema as hx
import data_schema.sch_utilities as utils

def sch_eso(cds):
    
    cds.extend_node_rater_defined("cds", {
        "eso": hx.Structure(children={
            "premium_total":                hx.Float(mode="override", view={"label": "Premium", "info": "This is Beazley's share, calculated based on the QS from the Rating Summary tab. It applies only to the options selected from the table above.", "format": {"thousandSeparated": True, "mantissa": 0}}, async_input= ["generate_uw_doc"]),
            "limit_total":                  hx.Float(mode="override", view={"label": "Limit", "info": "This is Beazley's share, calculated based on the QS from the Rating Summary tab. It applies only to the options selected from the table above.", "format": {"thousandSeparated": True, "mantissa": 0}}, async_input= ["generate_uw_doc"]),
            "label":                        hx.Str(mode="output", view={"label": "Option"}),
            "term":                         hx.Str(mode="override", view={"label": "Term", "info": "Based on severity selections for General Warranties and Tax Warranties/Deed in the Exposure Details tab.", "format": {"thousandSeparated": True, "mantissa": 0}}, async_input= ["generate_uw_doc"]),
            "additional_term_info":         hx.Str(mode="input", default=None, optionality="optional", view={"label": "Term"}, async_input= ["generate_uw_doc"]),
            "over_lining":                  hx.Str(mode="input", default="N/A", optionality="optional", view={"label": "Over Lining (Total Exposure)"}, async_input= ["generate_uw_doc"]),
            "cob":                          hx.Str(mode="input", default="N/A", optionality="optional", view={"label": "Unauthorised COB or MOP"}, async_input= ["generate_uw_doc"]),
            "authorising_comments":         hx.Str(mode="input", default=None, optionality="optional", view={"label": "Amount Authorising/Further Comments"}, async_input= ["generate_uw_doc"]),
            "authorising_comments_info":    hx.Str(mode="output", view={"label": "None"}, async_input= ["generate_uw_doc"]),
            "section_references":           hx.Str(mode="output", view={"label": "Selected Policy References"}, async_input= ["generate_uw_doc"]),
            "bind_date":                    hx.Date(mode="input", default=None, optionality="optional", view={"label": "Bind Date"}, async_input= ["generate_uw_doc"]),
            "approving_uw":                 hx.Str(mode="input", default=None, optionality="optional", view={"label": "Approving Underwriter's Limit of Authority:"}, async_input= ["generate_uw_doc"]),
            "authorisation_date":           hx.Date(mode="input", default=None, optionality="optional", view={"label": "Date of Authorisation"}, async_input= ["generate_uw_doc"]),
            "info":                         hx.Str(mode="output", view={"label": "None"}, async_input= ["generate_uw_doc"]),
            "document":                     hx.File(mode="output", file_name="eso_doc.docx", async_output=["generate_uw_doc"], view={"label": "Document"}),


            "options": hx.Structure(children={
                "coverage": hx.Structure(children={
                    "option_0": hx.Str(mode="output"),
                    "option_1": hx.Str(mode="output"),
                    "option_2": hx.Str(mode="output"),
                    "option_3": hx.Str(mode="output"),
                    "option_4": hx.Str(mode="output"),
                    "option_5": hx.Str(mode="output"),
                    "option_6": hx.Str(mode="output"),
                    "option_7": hx.Str(mode="output"),
                    "option_8": hx.Str(mode="output"),
                    "option_9": hx.Str(mode="output"),
                    "label": hx.Str(mode="output", view={"label": "Option"})
                }),
                "include_option": hx.Structure(children={
                    "option_0": hx.Bool(mode="input", default=True),
                    "option_1": hx.Bool(mode="input", default=True),
                    "option_2": hx.Bool(mode="input", default=True),
                    "option_3": hx.Bool(mode="input", default=True),
                    "option_4": hx.Bool(mode="input", default=True),
                    "option_5": hx.Bool(mode="input", default=True),
                    "option_6": hx.Bool(mode="input", default=True),
                    "option_7": hx.Bool(mode="input", default=True),
                    "option_8": hx.Bool(mode="input", default=True),
                    "option_9": hx.Bool(mode="input", default=True),
                    "label": hx.Str(mode="output", view={"label": "Include in Totals?"})
                }),
                "show_hide": hx.Structure(children={
                    "option_0": hx.Bool(mode="output"),
                    "option_1": hx.Bool(mode="output"),
                    "option_2": hx.Bool(mode="output"),
                    "option_3": hx.Bool(mode="output"),
                    "option_4": hx.Bool(mode="output"),
                    "option_5": hx.Bool(mode="output"),
                    "option_6": hx.Bool(mode="output"),
                    "option_7": hx.Bool(mode="output"),
                    "option_8": hx.Bool(mode="output"),
                    "option_9": hx.Bool(mode="output")
                })
            }),
        }) 
    })