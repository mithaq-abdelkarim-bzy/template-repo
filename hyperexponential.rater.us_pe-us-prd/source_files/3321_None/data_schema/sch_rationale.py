import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import coverage_options_names

import data_schema.sch_utilities as utils


def sch_rationale(cds):

    cds.extend_node_rater_defined(
        "cds",
        {
            "rationale": hx.Structure(
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
