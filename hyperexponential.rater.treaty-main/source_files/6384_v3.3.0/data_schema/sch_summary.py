import hx_data_schema as hx
import data_schema.sch_utilities as utils
from algorithms.rate_constants import max_layers

def sch_summary(cds):

    cds.extend_node_rater_defined("cds", {
        "currency_policy_financials": hx.Str(mode="input", default="USD", options=["USD", "EUR", "JPY", "GBP"], view={"label": "Policy Financials Currency", "options": {"read_only_option": {"read_only": True}}}),
        "summary_comments": hx.Str(mode="output", optionality="optional", view={"label": "Comments"}),
        "summary_fx_conversion": hx.Float(mode="output", optionality="optional", view={"label": "FX Conversion Rate", "format": utils.thousands_format(3)}),
        "summary_uwa_exposure": hx.Float(mode="output", optionality="optional", view={"label": "UWA Exposure Limit", "format": utils.thousands_format(0)}),
        "summary_uwa_premium": hx.Float(mode="output", optionality="optional", view={"label": "UWA Premium Limit", "format": utils.thousands_format(0)}),
        "summary_uwa_warning": hx.Str(mode="output", optionality="optional", view={"label": "UWA Warning"}),
        "summary_eso_obtained": hx.Bool(mode="input", default= False, view={"label": "ESO Obtained?"}),
        "summary_show_eso_obtained": hx.Bool(mode="output"),
        "epi_yoa": hx.Float(mode="output", optionality="optional", view={"label": "EPI YOA", "format": utils.thousands_format(0)}),

        "fx_conversion_label": hx.Str(mode="output"),

        "uwa_limit_label": hx.Str(mode="output"),
        "uwa_premium_label": hx.Str(mode="output"),

        "prem_100_label": hx.Str(mode="output"),

        "written_line_label": hx.Str(mode="output"),
        "estimated_line_label": hx.Str(mode="output"),
        "signed_line_label": hx.Str(mode="output"),

        "written_epi_label": hx.Str(mode="output"),
        "estimated_epi_label": hx.Str(mode="output"),
        "signed_epi_label": hx.Str(mode="output"),
    })

    cds.extend_node_rater_defined("cds", {
        "summary": hx.Structure(children= {
            "multi_year_summary_ty": hx.Structure(view={"label": "This Year"}, children={
                "line_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"label": "Written Line Exposure", "format": utils.thousands_format(0)}),
                "line_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"label": "Estimated Signed Line Exposure", "format": utils.thousands_format(0)}),
                "line_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"label": "Signed Line Exposure", "format": utils.thousands_format(0)}),

                "epi_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"label": "Written Line EPI", "format": utils.thousands_format(0)}),
                "epi_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"label": "Estimated Line EPI", "format": utils.thousands_format(0)}),
                "epi_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"label": "Signed Line EPI", "format": utils.thousands_format(0)}),

                "mi_250": hx.Float(mode="output", optionality="optional", view={"label": "1 in 250", "format": utils.thousands_format(0)}),
                "mi_250_prem_ratio": hx.Float(mode="output", optionality="optional", view={"label": "1 in 250 / Signed EPI", "format": utils.thousands_format(2)}),
                "mi_250_estimate_prem_ratio": hx.Float(mode="output", optionality="optional", view={"label": "1 in 250 / Estimated EPI", "format": utils.thousands_format(2)}),
            }),
            "multi_year_summary_ly": hx.Structure(view={"label": "Previous Year"}, children={
                "line_written_summary_fx": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(0), "read_only": True}),
                "line_estimated_summary_fx": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(0), "read_only": True}),
                "line_signed_summary_fx": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(0), "read_only": True}),

                "epi_written_summary_fx": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(0), "read_only": True}),
                "epi_estimated_summary_fx": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(0), "read_only": True}),
                "epi_signed_summary_fx": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(0), "read_only": True}),

                "mi_250": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(0), "read_only": True}),
                "mi_250_prem_ratio": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(2), "read_only": True}),
                "mi_250_estimate_prem_ratio": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(2), "read_only": True}),
            }),
            "ty": hx.Structure(children= { 
                "risk_adjusted_rate_change": hx.Float(mode="output", optionality="optional", view={"format": utils.percent_format(2)}),
                "rol_quote": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "rol_fot": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "bpi": hx.Float(mode="output", optionality="optional", view={"format": utils.percent_format(2)}),
                "fot_adequacy": hx.Float(mode="output", optionality="optional", view={"format": utils.percent_format(2)}),
                "rms_adequacy": hx.Float(mode="output", optionality="optional", view={"format": utils.percent_format(2)}),
                "ulr": hx.Float(mode="output", optionality="optional", view={"format": utils.percent_format(2)}),
                "epi_adj_rate": hx.Float(mode="output", optionality="optional", view={"format": utils.percent_format(2)}),
                "prem_full_line": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "line_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "line_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "line_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "mi_250": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "mi_250_prem_ratio": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(2)}),
                "mi_10": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "mi_10_prem_ratio": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(2)}),
            }),
            "ly": hx.Structure(children= { 
                "risk_adjusted_rate_change": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "bpi": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "fot_adequacy": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "rms_adequacy": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "ulr": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "epi_adj_rate": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "prem_full_line": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(0), "read_only": True}),
                "line_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "line_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "line_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "mi_250": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "mi_250_prem_ratio": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(2), "read_only": True}),
                "mi_10": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "mi_10_prem_ratio": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(2), "read_only": True}),
            }),
            "year_before_last": hx.Structure(children= {
                "rol_quote": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(0), "read_only": True}),
                "rol_fot": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(0), "read_only": True}),
                "roc": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(1), "read_only": True}), 
                "risk_adjusted_rate_change": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "bpi": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "fot_adequacy": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "rms_adequacy": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "ulr": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "epi_adj_rate": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "prem_full_line": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(0), "read_only": True}),
                "line_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "line_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "line_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "mi_250": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "mi_250_prem_ratio": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(2), "read_only": True}),
                "mi_10": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "mi_10_prem_ratio": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(2), "read_only": True}),
            }),
            "expiring_year": hx.Structure(children= {
                "rol_quote": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(0), "read_only": True}),
                "rol_fot": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(0), "read_only": True}),
                "roc": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(1), "read_only": True}),  
                "risk_adjusted_rate_change": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "bpi": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "fot_adequacy": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "rms_adequacy": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "ulr": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "epi_adj_rate": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.percent_format(2), "read_only": True}),
                "prem_full_line": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(0), "read_only": True}),
                "line_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "line_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "line_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "mi_250": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "mi_250_prem_ratio": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(2), "read_only": True}),
                "mi_10": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "mi_10_prem_ratio": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(2), "read_only": True}),
            })
        })
    })

    cds.extend_node_rater_defined("cds/layers", {
        "summary": hx.Structure(children={
            "year_after_next": hx.Structure(children={
                "share": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Share", "format": utils.percent_format(0)}),
                "section_reference": hx.Str(mode="output", optionality="optional", view={"label": "Section Reference"}),
                "risk_adjusted_rate_change": hx.Float(mode="output", optionality="optional", view={"label": "Rate Change", "format": utils.percent_format(2)}),
                "roc": hx.Float(mode="output", optionality="optional", view={"label": "ROC"}),
                "rms_adequacy": hx.Float(mode="output", optionality="optional", view={"label": "RMS Adequacy"}),
                "show_row": hx.Bool(mode="output", optionality = "optional"),
            }),
            "next_year": hx.Structure(children={
                "share": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Share", "format": utils.percent_format(0)}),
                "section_reference": hx.Str(mode="output", optionality="optional", view={"label": "Section Reference"}),
                "risk_adjusted_rate_change": hx.Float(mode="output", optionality="optional", view={"label": "Rate Change", "format": utils.percent_format(2)}),
                "roc": hx.Float(mode="output", optionality="optional", view={"label": "ROC"}),
                "rms_adequacy": hx.Float(mode="output", optionality="optional", view={"label": "RMS Adequacy"}),
                "show_row": hx.Bool(mode="output", optionality = "optional"),
            }),
            "ty": hx.Structure(children={
                "share": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Share", "format": utils.percent_format(0)}),
                "multi_year_period": hx.Int(mode="input", default=1, options=[1, 2, 3], view={"label": "Multi-Year Period", "options": {"read_only_option": {"read_only": True}}}),
                ## section_reference from layers
                ## leader from layers
                ## layer_description from layers
                ## limit_cnv from layers
                ## excess from layers
                "rol_quote": hx.Float(mode="output", optionality="optional", view={"label": "Quoted ROL", "format": utils.percent_format(2)}),
                "rol_fot": hx.Float(mode="output", optionality="optional", view={"label": "FOT ROL", "format": utils.percent_format(2)}),
                ## rol_afb_tech from quote
                "reinstatement_description": hx.Str(mode="output", optionality="optional", view={"label": "Reinstatements"}),
                ## roc from quote
                "risk_adjusted_rate_change": hx.Float(mode="output", optionality="optional", view={"label": "Rate Change", "format": utils.percent_format(2)}),
                "bpi": hx.Float(mode="output", optionality="optional", view={"label": "BPI", "format": utils.percent_format(2)}),
                "fot_adequacy": hx.Float(mode="output", optionality="optional", view={"label": "FOT Adequacy", "format": utils.percent_format(2)}),
                "rms_adequacy": hx.Float(mode="output", optionality="optional", view={"label": "RMS Adequacy", "format": utils.percent_format(2)}),
                "ulr": hx.Float(mode="output", optionality="optional", view={"label": "ULR (GN)", "format": utils.percent_format(2)}),
                "epi_adj_rate": hx.Float(mode="output", optionality="optional", view={"label": "EPI ADJ. RATE", "format": utils.percent_format(2)}),
                "prem_full_line": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "line_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "line_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "line_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "mi_250": hx.Float(mode="output", optionality="optional", view={"label": "1 in 250", "format": utils.percent_format(2)}),
                "mi_250_prem_ratio": hx.Float(mode="output", optionality="optional", view={"label": "1 in 250 / Premium", "format": utils.thousands_format(2)}),
                "mi_10": hx.Float(mode="output", optionality="optional", view={"label": "1 in 10", "format": utils.percent_format(2)}),
                "mi_10_prem_ratio": hx.Float(mode="output", optionality="optional", view={"label": "1 in 10 / Premium", "format": utils.thousands_format(2)}),
            }),
            "ly": hx.Structure(children={
                "next_year_section_reference": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Next Year Reference", "read_only": True}),
                "next_year_share": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Next Year Share", "format": utils.percent_format(0), "read_only": True}),
                "current_year_section_reference": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Current Year Reference", "read_only": True}),
                "current_year_share": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Current Year Share", "format": utils.percent_format(0), "read_only": True}),
                "multi_year_period": hx.Int(mode="input", default=None, optionality="optional", view={"label": "Multi-Year Period", "read_only": True}),
                ## section_reference from layers
                ## leader from layers
                ## layer_description from layers
                ## limit_cnv from layers
                ## excess from layers
                ## rol_quote from quote
                ## rol_fot from quote
                ## rol_afb_tech from quote
                "reinstatement_description": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Reinstatements", "read_only": True}),
                ## roc from quote
                "risk_adjusted_rate_change": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Rate Change", "format": utils.percent_format(2), "read_only": True}),
                "bpi": hx.Float(mode="input", default=None, optionality="optional", view={"label": "BPI", "format": utils.percent_format(2), "read_only": True}),
                "fot_adequacy": hx.Float(mode="input", default=None, optionality="optional", view={"label": "FOT Adequacy", "format": utils.percent_format(2), "read_only": True}),
                "rms_adequacy": hx.Float(mode="input", default=None, optionality="optional", view={"label": "RMS Adequacy", "format": utils.percent_format(2), "read_only": True}),
                "ulr": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ULR (GN)", "format": utils.percent_format(2), "read_only": True}),
                "epi_adj_rate": hx.Float(mode="input", default=None, optionality="optional", view={"label": "EPI ADJ. RATE", "format": utils.percent_format(2), "read_only": True}),
                "prem_full_line": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(0), "read_only": True}),
                "line_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "line_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "line_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "mi_250": hx.Float(mode="input", default=None, optionality="optional", view={"label": "1 in 250", "format": utils.percent_format(2), "read_only": True}),
                "mi_250_prem_ratio": hx.Float(mode="input", default=None, optionality="optional", view={"label": "1 in 250 / Premium", "format": utils.thousands_format(2), "read_only": True}),
                "mi_10": hx.Float(mode="input", default=None, optionality="optional", view={"label": "1 in 10", "format": utils.percent_format(2), "read_only": True}),
                "mi_10_prem_ratio": hx.Float(mode="input", default=None, optionality="optional", view={"label": "1 in 10 / Premium", "format": utils.thousands_format(2), "read_only": True}),
            }),
            "year_before_last": hx.Structure(children={
                ## need to store epi in application currency so we can dynamically convert it in the summary tab
                "epi_written": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Written EPI", "format": utils.thousands_format(0), "read_only": True}),
                "epi_estimated": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Estimated EPI", "format": utils.thousands_format(0), "read_only": True}),
                "epi_signed": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Signed EPI", "format": utils.thousands_format(0), "read_only": True}),

                "layer_structure_year_before_last": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Layer Structure", "read_only": True}),
                "current_year_section_reference": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Current Year Reference", "read_only": True}),
                "current_year_share": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Current Year Share", "format": utils.percent_format(0), "read_only": True}),
                "section_reference": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Section Reference", "read_only": True}),
                "leader": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Leader", "read_only": True}),
                "layer_description": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Description", "read_only": True}),
                "limit_cnv": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Limit", "format": utils.thousands_format(0), "read_only": True}),
                "excess_cnv": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Excess", "format": utils.thousands_format(0), "read_only": True}),
                "rol_quote": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Quoted ROL", "format": utils.percent_format(2), "read_only": True}),
                "rol_fot": hx.Float(mode="input", default=None, optionality="optional", view={"label": "FOT ROL", "format": utils.percent_format(2), "read_only": True}),
                "rol_afb_tech": hx.Float(mode="input", default=None, optionality="optional", view={"label": "AFB Tech ROL", "format": utils.percent_format(2), "read_only": True}),
                "reinstatement_description": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Reinstatements", "read_only": True}),
                "roc": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ROC", "format": utils.percent_format(2), "read_only": True}),
                "risk_adjusted_rate_change": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Rate Change", "format": utils.percent_format(2), "read_only": True}),
                "bpi": hx.Float(mode="input", default=None, optionality="optional", view={"label": "BPI", "format": utils.percent_format(2), "read_only": True}),
                "fot_adequacy": hx.Float(mode="input", default=None, optionality="optional", view={"label": "FOT Adequacy", "format": utils.percent_format(2), "read_only": True}),
                "rms_adequacy": hx.Float(mode="input", default=None, optionality="optional", view={"label": "RMS Adequacy", "format": utils.percent_format(2), "read_only": True}),
                "ulr": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ULR", "format": utils.percent_format(2), "read_only": True}),
                "epi_adj_rate": hx.Float(mode="input", default=None, optionality="optional", view={"label": "EPI ADJ. RATE", "format": utils.percent_format(2), "read_only": True}),
                "prem_full_line": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(0), "read_only": True}),
                "written_line": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Written Line", "format": utils.percent_format(2), "read_only": True}),
                "line_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "estimated_signing": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Estimated Signing", "format": utils.percent_format(2), "read_only": True}),
                "line_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "signed_line": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Signed Line", "format": utils.percent_format(2), "read_only": True}),
                "line_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "mi_250": hx.Float(mode="input", default=None, optionality="optional", view={"label": "1 in 250", "format": utils.percent_format(2), "read_only": True}),
                "mi_250_prem_ratio": hx.Float(mode="input", default=None, optionality="optional", view={"label": "1 in 250 / Premium", "format": utils.thousands_format(2), "read_only": True}),
                "mi_10": hx.Float(mode="input", default=None, optionality="optional", view={"label": "1 in 10", "format": utils.percent_format(2), "read_only": True}),
                "mi_10_prem_ratio": hx.Float(mode="input", default=None, optionality="optional", view={"label": "1 in 10 / Premium", "format": utils.thousands_format(2), "read_only": True}),
            }),
            "expiring_year": hx.Structure(children={
                ## need to store epi in application currency so we can dynamically convert it in the summary tab
                "epi_written": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Written EPI", "format": utils.thousands_format(0), "read_only": True}),
                "epi_estimated": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Estimated EPI", "format": utils.thousands_format(0), "read_only": True}),
                "epi_signed": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Signed EPI", "format": utils.thousands_format(0), "read_only": True}),

                "layer_structure_expiring_year": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Layer Structure", "read_only": True}),
                "current_year_section_reference": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Current Year Reference", "read_only": True}),
                "section_reference": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Section Reference", "read_only": True}),
                "leader": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Leader", "read_only": True}),
                "layer_description": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Description", "read_only": True}),
                "limit_cnv": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Limit", "format": utils.thousands_format(0), "read_only": True}),
                "excess_cnv": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Excess", "format": utils.thousands_format(0), "read_only": True}),
                "rol_quote": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Quoted ROL", "format": utils.percent_format(2), "read_only": True}),
                "rol_fot": hx.Float(mode="input", default=None, optionality="optional", view={"label": "FOT ROL", "format": utils.percent_format(2), "read_only": True}),
                "rol_afb_tech": hx.Float(mode="input", default=None, optionality="optional", view={"label": "AFB Tech ROL", "format": utils.percent_format(2), "read_only": True}),
                "reinstatement_description": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Reinstatements", "read_only": True}),
                "roc": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ROC", "format": utils.percent_format(2), "read_only": True}),
                "risk_adjusted_rate_change": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Rate Change", "format": utils.percent_format(2), "read_only": True}),
                "bpi": hx.Float(mode="input", default=None, optionality="optional", view={"label": "BPI", "format": utils.percent_format(2), "read_only": True}),
                "fot_adequacy": hx.Float(mode="input", default=None, optionality="optional", view={"label": "FOT Adequacy", "format": utils.percent_format(2), "read_only": True}),
                "rms_adequacy": hx.Float(mode="input", default=None, optionality="optional", view={"label": "RMS Adequacy", "format": utils.percent_format(2), "read_only": True}),
                "ulr": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ULR", "format": utils.percent_format(2), "read_only": True}),
                "epi_adj_rate": hx.Float(mode="input", default=None, optionality="optional", view={"label": "EPI ADJ. RATE", "format": utils.percent_format(2), "read_only": True}),
                "prem_full_line": hx.Float(mode="input", default=None, optionality="optional", view={"format": utils.thousands_format(0), "read_only": True}),
                "written_line": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Written Line", "format": utils.percent_format(2), "read_only": True}),
                "line_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "estimated_signing": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Estimated Signing", "format": utils.percent_format(2), "read_only": True}),
                "line_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "signed_line": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Signed Line", "format": utils.percent_format(2), "read_only": True}),
                "line_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_written_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_estimated_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "epi_signed_summary_fx": hx.Float(mode="output", optionality="optional", view={"format": utils.thousands_format(0)}),
                "mi_250": hx.Float(mode="input", default=None, optionality="optional", view={"label": "1 in 250", "format": utils.percent_format(2), "read_only": True}),
                "mi_250_prem_ratio": hx.Float(mode="input", default=None, optionality="optional", view={"label": "1 in 250 / Premium", "format": utils.thousands_format(2), "read_only": True}),
                "mi_10": hx.Float(mode="input", default=None, optionality="optional", view={"label": "1 in 10", "format": utils.percent_format(2), "read_only": True}),
                "mi_10_prem_ratio": hx.Float(mode="input", default=None, optionality="optional", view={"label": "1 in 10 / Premium", "format": utils.thousands_format(2), "read_only": True}),
            })
        })
    })




                       