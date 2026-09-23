import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format

def sch_rater_defined(cds):
    cds.extend_node_items("cds/layers/coverages", {
        "cargo_transit": {"label": "Cargo"},
        "cargo_storage": {"label": "Cargo"},
        "specie_transit": {"label": "Specie"},
        "specie_storage": {"label": "Specie"},
        "conloss_transit": {"label": "Con Loss"},
        "conloss": {"label": "Con Loss"},
    })
    cds.extend_node_rater_defined("cds", {
        "policy_info": hx.Structure(children={
            "deductions": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Deductions"}),
            "term": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Term (Years)"}),
            "beazley_share": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Beazley Share (%)"}),

        }),
        "rater_selection": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Rater Selection"}),
    })
    cds.extend_node_rater_defined("cds/exposure/granular", {
        "revenue": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Revenue"}),
        "financials_quality": hx.Structure(children={
            "value": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Score"}),
            "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comments"}),

        }),
        "claims_handling": hx.Structure(children={
            "value": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Score"}),
            "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comments"}),

        }),
        "claims_experience": hx.Structure(children={
            "value": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Score"}),
            "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comments"}),

        }),
        "jurisdiction_venue": hx.Structure(children={
            "value": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Score"}),
            "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comments"}),

        }),
        "wordings": hx.Structure(children={
            "value": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Score"}),
            "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comments"}),

        }),
        "level_of_service": hx.Structure(children={
            "value": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Score"}),
            "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comments"}),

        }),
        "knowledge_of_account": hx.Structure(children={
            "value": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Score"}),
            "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comments"}),

        }),
        "nfp_gov_fp": hx.Structure(children={
            "value": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Score"}),
            "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comments"}),

        }),
        "broker": hx.Structure(children={
            "value": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Score"}),
            "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comments"}),

        }),
        "corporate_identity": hx.Structure(children={
            "value": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Score"}),
            "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comments"}),

        }),
        "total_net_score": hx.Structure(children={
            "value": hx.Float(mode="output", view={"label": "Score"}),
            "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comments"}),

        }),
        "US_International": hx.Str(mode="input", default=None, optionality="optional", view={"label": "US/International"}),
        "choice_of_law": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Choice of Law"}),
    })
