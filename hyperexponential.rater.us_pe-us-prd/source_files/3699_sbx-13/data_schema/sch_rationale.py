import hx_data_schema as hx


def sch_rationale(cds):

    cds.extend_node_rater_defined(
        "cds",
        {
            "uw_rationale": hx.Structure(
                children={
                    "knowledge_of_insured": hx.Str(
                        mode="input",
                        default=None,
                        optionality="optional",
                    ),
                    "portfolio_fit": hx.Str(
                        mode="input",
                        default=None,
                        optionality="optional",
                    ),
                    "basis_of_risk_selection": hx.Str(
                        mode="input",
                        default=None,
                        optionality="optional",
                    ),
                    "unusual_or_complex_operations": hx.Str(
                        mode="input",
                        default=None,
                        optionality="optional",
                    ),
                    "facts_affecting_decision": hx.Str(
                        mode="input",
                        default=None,
                        optionality="optional",
                    ),
                }
            ),
        },
    )
