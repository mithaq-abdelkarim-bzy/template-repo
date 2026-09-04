import hx_data_schema as hx
from data_schema.utilities import thousands_format, percent_format

def rate_change():
    # Section Policy Information
    return  {
        "rate_change": hx.Structure(children={
            "expiring_policy_info": hx.Structure(children={
                "expiring_num_locs": hx.Float(mode="input", optionality="optional", default=None, async_output=["expiring_policy_fetch_task"], view={"read_only": True}),
                "expiring_tiv_total": hx.Float(mode="input", optionality="optional", default=None, async_output=["expiring_policy_fetch_task"], view={"read_only": True}),
                "expiring_policy_length": hx.Float(mode="input", optionality="optional", default=None, async_output=["expiring_policy_fetch_task"], view={"read_only": True}),
                "expiring_achieved_premium": hx.Float(mode="input", optionality="optional", default=None, async_output=["expiring_policy_fetch_task"], view={"read_only": True}),
                "expiring_limit": hx.Float(mode="input", optionality="optional", default=None, async_output=["expiring_policy_fetch_task"], view={"read_only": True}),
                "expiring_excess": hx.Float(mode="input", optionality="optional", default=None, async_output=["expiring_policy_fetch_task"], view={"read_only": True}),
                "expiring_deductible": hx.Float(mode="input", optionality="optional", default=None, async_output=["expiring_policy_fetch_task"], view={"read_only": True}),
                "expiring_brokerage": hx.Float(mode="input", optionality="optional", default=None, async_output=["expiring_policy_fetch_task"], view={"read_only": True}),
                "expiring_writ_line": hx.Float(mode="input", optionality="optional", default=None, async_output=["expiring_policy_fetch_task"], view={"read_only": True}),
                "expiring_expected_loss": hx.Float(mode="input", optionality="optional", default=None, async_output=["expiring_policy_fetch_task"], view={"read_only": True}),
            }),
            "expiring_policy_option_id": hx.Int(mode="override", async_input=["expiring_policy_fetch_task"], view={"label": "Expiring Policy Option", "format": {"thousandSeparated": False}}),
            "expiring_bpro_premium": hx.Float(mode="input", default=0, async_output=["expiring_policy_fetch_task"], view={"label": "Expiring", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "layer": hx.Structure(children={
                "renewal": hx.Int(default=1, mode="input", options=[1, 2, 3, 4, 5, 6], async_input=["expiring_policy_fetch_task"], view={"label": "Renewal Layer"}),
                "expiring": hx.Int(default=1, mode="input", options=[1, 2, 3, 4, 5, 6], async_input=["expiring_policy_fetch_task"], view={"label": "Expiring Layer"}),
            }),
            "premium_policy_term": hx.Structure(children={
                "renewal": hx.Float(mode="output", view={"label": "Renewal", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "expiring": hx.Float(mode="output", view={"label": "Expiring", "format": {"thousandSeparated": True, "mantissa": 0}}),
            }),
            "premium_policy_term_100pct": hx.Structure(children={
                "renewal": hx.Float(mode="output", view={"label": "Renewal", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "expiring": hx.Float(mode="output", view={"label": "Expiring", "format": {"thousandSeparated": True, "mantissa": 0}}),
            }),
            "premium_annualized": hx.Structure(children={
                "renewal": hx.Float(mode="output", view={"label": "Renewal", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "expiring": hx.Float(mode="output", view={"label": "Expiring", "format": {"thousandSeparated": True, "mantissa": 0}}),
            }),
            "premium_annualized_100pct": hx.Structure(children={
                "renewal": hx.Float(mode="output", view={"label": "Renewal", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "expiring": hx.Float(mode="output", view={"label": "Expiring", "format": {"thousandSeparated": True, "mantissa": 0}}),
            }),
            "exposure_change": hx.Structure(children={
                "renewal": hx.Float(mode="output", view={"label": " ", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "expiring": hx.Float(mode="output", view={"label": " ", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "ratio": hx.Float(mode="output", view={"label": "Exposure change dictates change of", "format": percent_format()}),
                "ratio_uw": hx.Float(mode="override", view={"label": " ", "format": percent_format()}),
                "comments": hx.Str(mode="input", default="", view={"label": " "}),
            }),
            "risk_characteristics_change": hx.Structure(children={
                "renewal": hx.Float(mode="output", view={"label": " ", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "expiring": hx.Float(mode="output", view={"label": " ", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "ratio": hx.Float(mode="output", view={"label": "Risk Characteristic change dictates change of", "format": percent_format()}),
                "ratio_uw": hx.Float(mode="override", view={"label": " ", "format": percent_format()}),
                "comments": hx.Str(mode="input", default="", view={"label": " "}),
            }),
            "deductible_change": hx.Structure(children={
                "renewal": hx.Float(mode="output", view={"label": " ", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "expiring": hx.Float(mode="output", view={"label": " ", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "ratio": hx.Float(mode="output", view={"label": "Deductible change dictates change of", "format": percent_format()}),
                "ratio_uw": hx.Float(mode="override", view={"label": " ", "format": percent_format()}),
                "comments": hx.Str(mode="input", default="", view={"label": " "}),
            }),
            "limit_change": hx.Structure(children={
                "renewal": hx.Float(mode="output", view={"label": " ", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "expiring": hx.Float(mode="output", view={"label": " ", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "ratio": hx.Float(mode="output", view={"label": "Limit change dictates change of", "format": percent_format()}),
                "ratio_uw": hx.Float(mode="override", view={"label": " ", "format": percent_format()}),
                "comments": hx.Str(mode="input", default="", view={"label": " "}),
            }),
            "terms_and_conditions_change": hx.Structure(children={
                "renewal": hx.Float(mode="output", view={"label": " ", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "expiring": hx.Float(mode="output", view={"label": " ", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "ratio": hx.Float(mode="output", view={"label": "Terms and conditions change dictates change of", "format": percent_format()}),
                "ratio_uw": hx.Float(mode="override", view={"label": " ", "format": percent_format()}),
                "comments": hx.Str(mode="input", default="", view={"label": " "}),
            }),
            "other_change": hx.Structure(children={
                "renewal_brokerage": hx.Float(mode="output", view={"label": "Brokerage", "format": percent_format(mantissa=2)}),
                "renewal_signed_line": hx.Float(mode="output", view={"label": "Signed Line", "format": percent_format(mantissa=2)}),
                "expiring_brokerage": hx.Float(mode="output", view={"label": "Brokerage", "format": percent_format(mantissa=2)}),
                "expiring_signed_line": hx.Float(mode="output", view={"label": "Signed Line", "format": percent_format(mantissa=2)}),
                "ratio": hx.Float(mode="output", view={"label": "Other factors change dictates change of", "format": percent_format()}),
                "ratio_uw": hx.Float(mode="override", view={"label": " ", "format": percent_format()}),
                "comments": hx.Str(mode="input", default="", view={"label": " "}),
            }),
            "total_factor": hx.Structure(children={
                "technical": hx.Float(mode="output", view={"label": "Total Factor", "format": percent_format()}),
                "underwriter": hx.Float(mode="output", view={"label": "Total Factor", "format": percent_format()}),
            }),
            "simple_rate_change": hx.Float(mode="output", view={"label": "Simple Rate Change", "format": percent_format()}),
            "risk_adjusted_rate_change": hx.Structure(children={
                "technical": hx.Float(mode="output", view={"label": "Risk Adjusted Rate Change", "format": percent_format()}),
                "underwriter": hx.Float(mode="output", view={"label": "Risk Adjusted Rate Change", "format": percent_format()}),
            }),
            "error_message": hx.Str(mode="output"),
            })
        }
    