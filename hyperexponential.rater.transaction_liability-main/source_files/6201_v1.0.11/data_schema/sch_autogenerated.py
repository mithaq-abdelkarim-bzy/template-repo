import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format

def sch_rater_defined(cds):
    cds.extend_node_rater_defined("cds", {
        "policy_info": hx.Structure(children={
            "project_name": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Project Name"}),
            "target_name": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Target Company (Name)"}),
            "transaction_value": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Transaction Value  "}),
            "total_limit": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Total limit purchased  "}),
            "policyholder": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Policy Purchased by  "}),
            "buyer_name": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Buyer (name)  "}),
            "buyer_lawyer": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Lawyer (buyer) "}),
            "seller_name": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Seller (name)  "}),
            "seller_lawyer": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Lawyer (seller)  "}),
            "uw_expenses_flag": hx.Bool(mode="input", default=True, view={"label": "Include UW Expenses"}),
            "uw_expenses": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Underwriting Expenses  "}),
            "distressed_business_flag": hx.Bool(mode="input", default=True, view={"label": "Distressed Business  "}),
            "rationale": hx.Structure(children={
                "knowledge_of_insured": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Knowledge of the Insured"}),
                "portfolio_fit": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Portfolio Fit & Basis of Risk Selection"}),
                "complex_considerations": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Unusual Or Complex Considerations"}),
                "facts_affecting_decision": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Facts Affecting Decision"}),

            }),

        }),
        "rating_factors": hx.Structure(children={
            "freq": hx.Structure(children={
                "target": hx.Structure(children={
                    "jurisdiction": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Jurisdiction  "}),
                    "industry": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Industry"}),
                    "business_nature": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Nature of Business  "}),
                    "ihs_enforcement": hx.Str(mode="output", view={"label": "IHS Contract Enforcement"}),
                    "default_score": hx.Float(mode="output", view={"label": "Default Score  "}),
                    "freq_adjustment": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Adjustment  "}),
                    "freq_adjusted": hx.Float(mode="output", view={"label": "Adjusted frequency  "}),

                }),

            }),
            "sev": hx.Structure(children={
                "due_diligence": hx.Structure(children={
                    "coverage_flag": hx.Bool(mode="input", default=True, view={"label": "Covered?"}),
                    "severity_assessment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Severity assessment"}),
                    "adjustment": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Adjustment"}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "disclosure": hx.Structure(children={
                    "coverage_flag": hx.Bool(mode="input", default=True, view={"label": "Covered?"}),
                    "severity_assessment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Severity assessment"}),
                    "adjustment": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Adjustment"}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "general_warranties": hx.Structure(children={
                    "coverage_flag": hx.Bool(mode="input", default=True, view={"label": "Covered?"}),
                    "severity_assessment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Severity assessment"}),
                    "adjustment": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Adjustment"}),
                    "term": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Term (years)"}),
                    "term_modifier": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Term modifier"}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "tax_warranties": hx.Structure(children={
                    "coverage_flag": hx.Bool(mode="input", default=True, view={"label": "Covered?"}),
                    "severity_assessment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Severity assessment"}),
                    "adjustment": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Adjustment"}),
                    "term": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Term (years)"}),
                    "term_modifier": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Term modifier"}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "modified_score": hx.Float(mode="output", view={"label": "Modified Score"}),
                "div_flag": hx.Bool(mode="input", default=True, view={"label": "Include DIV"}),
                "volatility": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Volatility"}),
                "multiple": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Multiple"}),

            }),

        }),
        "eso": hx.Structure(children={
            "premium_term": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Term Premium Figure Gross"}),
            "exposure_limits": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Exposure Limits"}),
            "term": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Term"}),
            "overlining": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Over Lining (Total Exposure)"}),
            "cob": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Unauthorised COB or MOP"}),
            "authorising_comments": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Amount Authorising/Further Comments"}),
            "authorising_comments_info": hx.Str(mode="output", view={"label": "None"}),
            "section_references": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Policy Reference (if multiple)"}),
            "policy_reference_3": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Policy Reference (if multiple)"}),
            "bind_date": hx.Date(mode="input", default=None, optionality="optional", view={"label": "Bind Date"}),
            "authoriser": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Authoriser Name"}),
            "authoriser_authority": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Authoriser's Authority Limit"}),
            "authorisation_date": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Date of Authorisation"}),
            "info": hx.Str(mode="output", view={"label": "None"}),

        }),
    })
    cds.extend_node_rater_defined("cds/layers", {
        "policy_type": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Policy Type"}),
        "option_name": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Option name"}),
        "limit_pct": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Limit %"}),
        "excess_pct": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Excess %"}),
        "indicated": hx.Bool(mode="input", default=True, view={"label": "Indicated"}),
        "date": hx.Date(mode="input", default=None, optionality="optional", view={"label": "Date"}),
        "is_bound": hx.Bool(mode="input", default=True, view={"label": "Bound?"}),
        "bp_premium": hx.Float(mode="output", view={"label": "Biz plan premium (targets BP%)"}),
        "model_rol": hx.Float(mode="output", view={"label": "Model ROL"}),
        "midpt": hx.Float(mode="output", view={"label": "MIDPT"}),
        "warnings": hx.Str(mode="output", view={"label": "Warnings"}),
    })
    cds.override_node_properties("cds/layers/written_line", {
        "view": {"label": "Q/S"},
    })
    cds.override_node_properties("cds/layers/premium", {
        "view": {"label": "Bound premium"},
    })
    cds.override_node_properties("cds/layers/model_premium", {
        "view": {"label": "Model premium"},
    })
    cds.override_node_properties("cds/layers/technical_premium", {
        "view": {"label": "Technical Premium"},
    })
    cds.override_node_properties("cds/layers/benchmark_premium", {
        "view": {"label": "Benchmark premium"},
    })
    cds.override_node_properties("cds/layers/tpi", {
        "view": {"label": "TPI%"},
    })
    cds.override_node_properties("cds/layers/bpi", {
        "view": {"label": "BPI%"},
    })
