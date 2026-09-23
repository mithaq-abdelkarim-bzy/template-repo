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
        "core_account": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Core Account"}),
        "platform": hx.Str(mode="input", default="Lloyd's", view={"label": "Platform"}),
        "afb_primary_wording_manuscript": hx.Bool(mode="input", default=None, optionality="optional", view={"label": "AFB Primary and Wording Manuscript"}),
        "long_term_agreement": hx.Bool(mode="input", default=None, optionality="optional", view={"label": "Long Term Agreement"}),
        "esg_syndicate": hx.Str(mode="input", default=None, optionality="optional", view={"label": "ESG Syndicate Status"}),
        "direct_ri": hx.Str(mode="input", default="Direct", view={"label": "Direct/RI"}),
        "esg_net_premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ESG Net Written Premium (USD)"}),
        "cedant_name": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Cedant Name"}),
        "any_one_claim": hx.Bool(mode="input", default=None, optionality="optional", view={"label": "Any One Claim (AOC)"}),
    })
