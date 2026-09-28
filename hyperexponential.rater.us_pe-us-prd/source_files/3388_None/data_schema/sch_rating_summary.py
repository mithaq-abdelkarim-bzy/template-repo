import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import coverage_options
from algorithms.rate_constants import cob_code_options_number
from algorithms.rate_constants import coverage_policy_status
from algorithms.rate_constants import coverage_policy_status
from algorithms.rate_constants import brokerage

import data_schema.sch_utilities as utils


def sch_rating_summary(cds):
    # Adding coverages to the layers list. NOTE this code duplicates all the common fields from layer to each coverage.

    cds.extend_node_items("cds/layers/coverages", {"option": {"label": "label"}})
    cds.override_node_properties("cds/layers", {"default_element_count": 3})

    cds.extend_node_rater_defined(
        "cds/layers",
        {
            "show_excess": hx.Bool(
                mode="output"
            ),  # This is a flag to show the excess options
            "liability_limits_EEC": hx.Structure(
                children={
                    "show": hx.Bool(mode="output"),
                    "list": hx.List(
                        mode="output", children={"limit": hx.Int(mode="output")}
                    ),
                }
            ),
            "liability_limits_AGG": hx.Structure(
                children={
                    "show": hx.Bool(mode="output"),
                    "list": hx.List(
                        mode="output", children={"limit": hx.Int(mode="output")}
                    ),
                }
            ),
            "product_liability_limits_AGG": hx.Int(
                mode="input",
                default=None,
                optionality="optional",
                options_table="table_input_products_product_liability_limits",
                options_column="limit",
                view={
                    "label": "Product Liability Limits AGG",
                    "format": thousands_format(),
                },
            ),
            "personal_advertising_liability_EEC": hx.Structure(
                children={
                    "show": hx.Bool(mode="output"),
                    "list": hx.List(
                        mode="output", children={"limit": hx.Int(mode="output")}
                    ),
                    "limit": hx.Int(
                        mode="input",
                        default=None,
                        optionality="optional",
                        options_data="../list",
                        options_field="limit",
                        view={
                            "label": "Personal Advertising Liability EEC",
                            "format": thousands_format(),
                        },
                    ),
                }
            ),
            "defence_outside_limits": hx.Structure(
                children={
                    "show": hx.Bool(mode="output"),
                    "list": hx.List(
                        mode="output", children={"limit": hx.Int(mode="output")}
                    ),
                    "limit": hx.Int(
                        mode="input",
                        default=None,
                        optionality="optional",
                        options_data="../list",
                        options_field="limit",
                        view={
                            "label": "Defence Outside Limits",
                            "format": thousands_format(),
                        },
                    ),
                }
            ),
            "general_liability": hx.Structure(
                children={
                    "limit_staffing": hx.Int(
                        mode="output",
                        view={
                            "label": "General Liability Limits",
                            "format": thousands_format(),
                        },
                    )
                }
            ),
            "effective_rate": hx.Float(
                mode="output",
                view={"label": "Effective Rate", "format": percent_format()},
            ),
            "primary_deductible": hx.Structure(
                children={
                    "show": hx.Bool(mode="output"),
                    "list": hx.List(
                        mode="output", children={"deductible": hx.Int(mode="output")}
                    ),
                }
            ),
            "cob": hx.Structure(
                children={
                    **{
                        f"code_{index}": hx.Str(
                            mode="input",
                            default=None,
                            optionality="optional",
                            options_table="table_input_cob_codes",
                            options_column="code",
                            view={"label": f"COB Code {index}"},
                        )
                        for index in range(1, cob_code_options_number + 1)
                    },
                    **{
                        f"premium_{index}": hx.Int(
                            mode="input",
                            default=None,
                            optionality="optional",
                            view={
                                "label": f"Percentage Premium {index}",
                                "format": percent_format(),
                            },
                        )
                        for index in range(1, cob_code_options_number + 1)
                    },
                },
            ),
            "premium_blueprint": hx.Structure(
                children={
                    "show": hx.Bool(mode="output"),
                    "list": hx.List(
                        mode="output",
                        children={
                            "limit": hx.Str(
                                mode="output",
                                view={"label": "Limit", "format": thousands_format()},
                            ),
                            "premium": hx.Int(
                                mode="output",
                                view={"label": "Premium", "format": thousands_format()},
                            ),
                        },
                    ),
                }
            ),
        },
    )

    cds.override_node_properties(
        "cds/layers/limit",
        {
            "options_data": "../liability_limits_EEC/list",
            "options_field": "limit",
            "default": None,
            "optionality": "optional",
            "view": {"label": "Liability Limits EEC", "format": thousands_format()},
        },
    )

    cds.override_node_properties(
        "cds/layers/aggregate_limit",
        {
            "options_data": "../liability_limits_AGG/list",
            "options_field": "limit",
            "default": None,
            "optionality": "optional",
            "view": {"label": "Liability Limits AGG", "format": thousands_format()},
        },
    )
    cds.override_node_properties(
        "cds/layers/deductible",
        {
            "options_data": "../primary_deductible/list",
            "options_field": "deductible",
            "default": None,
            "optionality": "optional",
            "view": {"label": "Primary Deductible", "format": thousands_format()},
        },
    )


def add_options(cds):

    cds.extend_node_items(
        "cds/layers/coverages", [{"name": "option", "label": "label"}]
    )

    # cds.override_node_properties(
    #     "cds/layers/coverages/" + option["name"] + "/excess",
    #     {
    #         "default": None,
    #         "view": {"label": "Excess of"},
    #     },
    # )
    # cds.override_node_properties(
    #     "cds/layers/coverages/" + option["name"] + "/status",
    #     {
    #         "view": {"label": "Policy Status"},
    #         "default": coverage_policy_status[0],
    #         "optionality": "required",
    #         "options": coverage_policy_status,
    #     },
    # )
    # cds.override_node_properties(
    #     "cds/layers/coverages/" + option["name"] + "/premium",
    #     {"view": {"label": "Gross Annual Premium"}},
    # )
    # cds.override_node_properties(
    #     "cds/layers/coverages/" + option["name"] + "/brokerage",
    #     {"default": 0.275, "view": {"label": "Brokerage Percentage"}},
    # )

    # cds.override_node_properties(
    #     "cds/layers/coverages/" + option["name"] + "/pflr",
    #     {"view": {"label": "Gross Loss Ratio"}},
    # )

    # cds.override_node_properties(
    #     "cds/layers/coverages/" + option["name"] + "/tpi",
    #     {"view": {"label": "TPI"}},
    # )
    # cds.override_node_properties(
    #     "cds/layers/coverages/" + option["name"] + "/technical_premium",
    #     {"view": {"label": "Annual Technical Premium"}},
    # )
    # cds.override_node_properties(
    #     "cds/layers/coverages/" + option["name"] + "/bpi",
    #     {"view": {"label": "BPI"}},
    # )
    # cds.override_node_properties(
    #     "cds/layers/coverages/" + option["name"] + "/benchmark_premium",
    #     {"view": {"label": "Annual Benchmark Premium"}},
    # )
    # cds.override_node_properties(
    #     "cds/layers/coverages/" + option["name"] + "/model_premium",
    #     {"view": {"label": "Annual Model Premium"}},
    # )
