import hx_data_schema as hx
from data_schema.utilities import thousands_format, percent_format
from data_schema.dropdown_list import insurance_type_list

def rationale():
    rationale_schema = hx.Structure(children={
        "fill_rationale": hx.Bool(mode="input", async_input=["generate_uw_rationale_doc_task"], default = 0, view={"label": "Should a rationale be documented due to the specific nature or complexity of the risk, and/or terms?"}),
        "comments": hx.Str(mode="input", async_input=["start_renewal_task"], default="", view={"label": "Comments"}),
        "first_saved": hx.Date(mode="input", default = None, optionality = "optional", async_input=["generate_uw_rationale_doc_task"], async_output=["update_first_saved_task","start_renewal_task"], view={"options": {"read_only": {"read_only": True}}, "label":"Date Saved"}),
        "button_text": hx.Str(mode="input", default = "Saved", optionality = "optional", async_output=["update_first_saved_task"], view={"options": {"read_only": {"read_only": True}}}),
        "show_save_button": hx.Bool(mode="output", async_input=["update_first_saved_task"]),
        "show_button_text": hx.Bool(mode="output", async_input=["update_first_saved_task"]),
        "layers": hx.Int(default=1, mode="input", options=[1, 2, 3, 4, 5, 6], async_input=["generate_uw_rationale_doc_task","rationale_rater_task"], view={"label": "Layer"}),
        "layer_label":  hx.Str(mode="output",async_input=["generate_uw_rationale_doc_task"], view={"label": "Layer Label"}),
        "show_dropdown": hx.Bool(mode="output"),
        "bound_layer": hx.Str(mode="output", view={"label": "Layer"}),
        "show_bound": hx.Bool(mode ="output", async_input=["generate_uw_rationale_doc_task"]),
        "document": hx.File(mode="output", file_name="uw_rationale_doc.docx", async_output=["generate_uw_rationale_doc_task"], view={"label": "Document"}),     
    
        "risk_information": hx.Structure(children={
            "risk_name": hx.Str(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Risk Name"}),
            "policy_ref": hx.Str(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Policy Ref"}),
            "policy_period_start": hx.Date(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Policy Period Start"}),
            "policy_period_end": hx.Date(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Policy Period End"}),
            "underwriter": hx.Str(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Underwriter"}),
            "broker": hx.Str(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Broker"}),
            "occupancy": hx.Str(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Occupancy"}),
            "tiv": hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "TIV", "format": thousands_format(mantissa=0)}),
            "new_renewal": hx.Str(mode = "output", async_input=["generate_uw_rationale_doc_task"], view={"label": "New/Renewal"}),
        }),

        "rating_terms": hx.Structure(children={
            "insurance_type": hx.Str(mode="input", options=insurance_type_list, async_input=["generate_uw_rationale_doc_task"], default="", view={"label": "Insurance Type"}),
            "limit": hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Limit", "format": thousands_format(mantissa=0)}),
            "excess": hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Excess", "format": thousands_format(mantissa=0)}),
            "written_line": hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Written Line", "format": percent_format(mantissa=0)}),
            "afb_exposure": hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "AFB Exposure", "format": thousands_format(mantissa=0)}),     
        }),

        "rating_terms_2": hx.Structure(children={
            "achieved_premium_100_gg": hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Achieved Premium 100% GG Slip Ccy", "format": thousands_format(mantissa=0)}),
            "commission": hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Brokerage", "format": percent_format(mantissa=2)}),
            "rate_change": hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Rate Change (based on selections made on Rate Change tab)", "format": percent_format(mantissa=0)}),
        }),

        "natural_perils": hx.Structure(children={
            **{
                f"{peril}": hx.Structure(view={"label": f"{peril_name}"}, children={
                    "limit": hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Limit", "info": "Sublimits are equal to the ground up losses minus the excess capped at the overall limit", "format": thousands_format(mantissa=0)}),
                    "deductible": hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Deductible", "format": thousands_format(mantissa=0)}),
                    "premium": hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Premium", "format": thousands_format(mantissa=0)}),
                    "complex_ded_structure": hx.Str(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "Complex Deductible Structure?"})
                })
                for peril, peril_name in zip(("fire", "windstorm", "eq", "wildfire", "scs", "flood"), ("Fire", "Windstorm", "EQ", "Wildfire", "SCS", "Flood"))
            },
            "tpi_post_uw_adj": hx.Float(mode="output", async_input=["generate_uw_rationale_doc_task"], view={"label": "TPI % (Post UW Adjustment)", "format": percent_format(mantissa=0)}),
            "adj_factor_reason": hx.Str(mode="input", async_input=["generate_uw_rationale_doc_task"], default="", view={"label": "Adj factors (reason)"})
        }),

        "reinsurance": hx.Structure(children={
            "consortium": hx.Bool(mode="input", async_input=["generate_uw_rationale_doc_task"], default = False, view={"label": f"Consortium?"}),
            "fac_purchased": hx.Bool(mode="input", async_input=["generate_uw_rationale_doc_task"], default = False, view={"label": "FAC Purchased?"}),
            "fac_structure": hx.Str(mode="input", async_input=["generate_uw_rationale_doc_task"], default= "", view={"label": "FAC Structure"})
        }),

        "note_section": hx.Structure(children={
            "description": hx.Str(mode="input", async_input=["generate_uw_rationale_doc_task"], default="Please provide details on the following:\n- High level view of risk\n- Territory profile\n- History of account/insured\n- Cat exposure\n- Tech Risk exposure\n- Loss experience", view={"label": "Description"}),
            "special_processing": hx.Str(mode="input", async_input=["generate_uw_rationale_doc_task"], default="- Forms/Wordings (manuscript, policy change, etc)\n- Internantional exposure\n- Authority approval (LOA)", view={"label": "Special Processing"}),
            "underwriter_thoughts": hx.Str(mode="input", async_input=["generate_uw_rationale_doc_task"], async_output=["start_renewal_task"], default="- Thought process of the trade\n- Future concerns, intentions, or items to monitor", view={"label": "Underwriter Thoughts"})
        })

    })

    return {"rationale": rationale_schema}
