import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import coverage_options_names

import data_schema.sch_utilities as utils


def numbers_names_dict(number):
    numbers_names_dict = {
        1: "First",
        2: "Second",
        3: "Third",
        4: "Fourth",
        5: "Fifth",
        6: "Sixth",
        7: "Seventh",
        8: "Eighth",
        9: "Ninth",
        10: "Tenth",
    }
    return numbers_names_dict[number]


def sch_quote_design(cds):

    cds.extend_node_rater_defined(
        "cds",
        {
            "quote_design": hx.Structure(
                children={
                    "retro_date": hx.Date(
                        mode="input",
                        default=None,
                        optionality="optional",
                        view={"label": "Displayed Retro Date"},
                    ),
                    "coverage_options_list": hx.List(
                        mode="output",
                        children={
                            "option": hx.Str(
                                mode="output",
                            ),
                        },
                    ),
                    "coverage_options_label": hx.Str(
                        mode="input",
                        default="Coverage Options",
                    ),
                    "comments_label": hx.Str(
                        mode="input",
                        default="Comments/Conditions",
                    ),
                    "quotes": hx.Structure(
                        children={
                            **{
                                f"quote_{index}": hx.Structure(
                                    children={
                                        "coverage_option": hx.Str(
                                            mode="input",
                                            default=None,
                                            optionality="optional",
                                            options_data="../../../coverage_options_list",
                                            options_field="option",
                                        ),
                                        "comment": hx.Str(
                                            mode="input",
                                            default=None,
                                            optionality="optional",
                                        ),
                                    },
                                    view={
                                        "label": f"{numbers_names_dict(index)} Quote"
                                    },
                                )
                                for index in range(1, len(coverage_options_names) + 1)
                            }
                        }
                    ),
                    "overall_comments": hx.Str(
                        mode="input",
                        default=None,
                        optionality="optional",
                        view={"label": "Overall Comments"},
                    ),
                    "is_e_cigarettes_check": hx.Structure(
                        children={
                            "show": hx.Bool(
                                mode="output",
                            ),
                            "value": hx.Bool(
                                mode="input",
                                default=False,
                                view={"label": 'Type is "E-Cigarettes Products"'},
                            ),
                        }
                    ),
                }
            ),
        },
    )
