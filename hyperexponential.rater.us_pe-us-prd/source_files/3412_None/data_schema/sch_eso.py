import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import coverage_options_names

import data_schema.sch_utilities as utils


def sch_eso(cds):

    cds.extend_node_rater_defined(
        "cds",
        {
            "eso": hx.Structure(
                children={
                    "requesting_underwriter": hx.Str(
                        mode="output",
                        view={"label": "Requesting Underwriter"},
                    ),
                    "term_premium_figure_gross": hx.Structure(
                        children={
                            "exception": hx.Bool(
                                mode="input",
                                default=False,
                                view={"label": "Term Premium Figure Gross"},
                            ),
                            "amount": hx.Float(mode="output"),
                        },
                    ),
                    "exposure_limits": hx.Structure(
                        children={
                            "exception": hx.Bool(
                                mode="input",
                                default=False,
                                view={"label": "Exposure Limits"},
                            ),
                            "amount": hx.Float(mode="output"),
                        },
                    ),
                    "term": hx.Structure(
                        children={
                            "exception": hx.Bool(
                                mode="input",
                                default=False,
                                view={"label": "Term"},
                            ),
                            "amount": hx.Float(mode="output"),
                        },
                    ),
                    "over_lining": hx.Structure(
                        children={
                            "exception": hx.Bool(
                                mode="input",
                                default=False,
                                view={"label": "Over-Lining (Total Exposure)"},
                            ),
                            "amount": hx.Float(
                                mode="input",
                                default=None,
                                optionality="optional",
                            ),
                        },
                    ),
                    "unauthorised_cob_or_mop": hx.Structure(
                        children={
                            "exception": hx.Bool(
                                mode="input",
                                default=False,
                                view={"label": "Unauthorised COB or MOP"},
                            ),
                            "amount": hx.Float(
                                mode="input",
                                default=None,
                                optionality="optional",
                            ),
                        },
                    ),
                    "amount_authorising": hx.Structure(
                        children={
                            "input": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Amount Authorising/Further Comments"},
                            ),
                            "warning": hx.Str(
                                mode="output",
                            ),
                        }
                    ),
                    "sign_off": hx.Structure(
                        children={
                            "policy_reference": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Policy Reference"},
                            ),
                            "bind_date": hx.Date(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Bind Date"},
                            ),
                            "authoriser_name": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Authoriser Name"},
                            ),
                            "authorisers_authority_limit": hx.Float(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Authoriser's Authority Limit"},
                            ),
                            "date_of_authorisation": hx.Date(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Date Of Authorisation"},
                            ),
                        }
                    ),
                    "warning": hx.Str(
                        mode="output",
                    ),
                }
            ),
        },
    )
