import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers

def sch_quote_summary(cds):
    default_exclusions = [
        "Nuclear, Chemical & Biological Terrorism",
        "War & Terrorism (but see Condition: Passive War / Terrorism Extension)",
        "War & Terrorism",
        "Suicide",
        "Epidemic",
        "the Insured Person being under the influence of alcohol or drugs",
        "the Insured Person's own Criminal Act",
        "As expiry"
    ]
    default_conditions = [
        "Event Limit USD N/A",
        "Active at Work Warranty",
        "Full loss history last 5 years",
        "Firm order to be placed via PPL or Whitespace",
        "Sanctions Limitations Clause LMA 3100a",
        "Claims Control Clause",
        "Nil claims under expiring Policy",
        "Full details of any Long Term Absentees"
    ]

    cds.extend_node_rater_defined("cds", {
        "quote": hx.Structure(children={
            "reinsured_name": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Reinsured", "multiline": True}),
            "insured_name": hx.Str(mode="output", view={"label": "Original Insured", "multiline": True}),
            "cover": hx.Str(mode="output", view={"label": "Cover"}),
            "term": hx.Float(mode="output", view={"label": "Term (months)", "format": thousands_format()}),
            "max_age_attained": hx.Float(mode="override", view={"label": "Maximum Age Attained - Overridable", "format": integer_format()}),
            "no_lives": hx.Float(mode="output", view={"label": "Number of Lives", "format": integer_format()}),
            "sum_insured_basis": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Basis of Sum Insured"}),
            "max_aol_sum_insured": hx.Float(mode="override", view={"label": "Max Any One Life Sum Insured - Overridable", "format": thousands_format()}),
            "free_cover_limit": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Free Cover Limit" , "format": thousands_format()}),
            "total_sum_insured": hx.Float(mode="output", view={"label": "Total Sum Insured", "format": thousands_format()}),
            "event_limit": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Event Limit", "format": thousands_format()}),
            "deposit_premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Deposit Premium", "format": thousands_format()}),
            "adjustable_rate": hx.Float(mode="output", view={"label": "Adjustable Rate (per mille)", "format": thousands_format(2)}),
            "commission": hx.Float(mode="output", view={"label": "Commission", "format": {**percent_format(1), **{"trimMantissa": True}}}),
            "exclusions": hx.List(mode="input", async_output=["start_renewal_task"], default_element_count=len(default_exclusions), fixed_element_count=len(default_exclusions), children={
                "exclusion": hx.Str(mode="input", async_output=["start_renewal_task"], default="", fixed_values=default_exclusions, view={"label": "Exclusion", "multiline": True}),
                "is_excluded": hx.Bool(mode="input", async_output=["start_renewal_task"], default=False, view={"label": "Yes/No"})
            }),
            "conditions": hx.List(mode="input", async_output=["start_renewal_task"], default_element_count=len(default_conditions), fixed_element_count=len(default_conditions), children={
                "condition": hx.Str(mode="input", async_output=["start_renewal_task"], default="", fixed_values=default_conditions, view={"label": "Condition", "multiline": True}),
                "is_included": hx.Bool(mode="input", async_output=["start_renewal_task"], default=False, view={"label": "Yes/No"})
            }),
            "valid_until_date": hx.Date(mode="output", view={"label": "Indication Valid Until"}),
            "uw_notes": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Notes"}),
        })
    })
    