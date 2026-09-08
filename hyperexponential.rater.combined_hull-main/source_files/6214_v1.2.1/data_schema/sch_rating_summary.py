import hx_data_schema as hx
from data_schema.sch_utilities import percent_format
from algorithms.rate_constants import max_layers
import data_schema.sch_utilities as utils


def get_rating_summary_fields(coverage_type):
    prefix = coverage_type + "_"

    rating_summary_fields = {
        prefix
        + "policy_reference": hx.Str(
            mode="input",
            optionality="optional",
            default=None,
            view={"label": "Policy Reference"},
            async_input=["populate_bi_data, generate_rating_summary_xlsx_task"],
        ),
        prefix
        + "expected_lr": hx.Float(
            mode="output",
            view={"label": "Expected LR", "format": utils.percent_format(2)},
        ),
        "benchmark_premium_pro_rated_100pct": hx.Float(
            mode="output",
            view={
                "label": "Gross Benchmark Premium (100%)",
                "format": utils.thousands_format(0),
            },
            async_input=[
                "rarc_task",
                "generate_rating_summary_xlsx_task",
            ],
        ),
        "benchmark_premium_annualised_100pct": hx.Float(
            mode="output",
            view={
                "label": "Gross Benchmark Premium (100%)",
                "format": utils.thousands_format(0),
            },
            async_input=[
                "rarc_task",
                "generate_rating_summary_xlsx_task",
            ],
        ),
        "benchmark_premium_policy_term_100pct": hx.Float(
            mode="output",
            async_input=[
                "rarc_task",
            ],
        ),
        "quoted_premium_policy_term_100pct": hx.Float(
            mode="output",
            async_input=[
                "rarc_task",
            ],
        ),
        "quoted_premium_pro_rated_100pct": hx.Float(
            mode="output",
            view={
                "label": "Gross Quoted/Achieved Premium (100%)",
                "format": utils.thousands_format(0),
            },
            async_input=[
                "rarc_task",
                "generate_rating_summary_xlsx_task",
            ],
        ),
        "quoted_premium_annualised_100pct": hx.Float(
            mode="output",
            view={
                "label": "Gross Quoted/Achieved Premium (100%)",
                "format": utils.thousands_format(0),
            },
            async_input=[
                "rarc_task",
                "generate_rating_summary_xlsx_task",
            ],
        ),
        "technical_premium_pro_rated_100pct": hx.Float(
            mode="output",
            view={
                "label": "Gross Technical Premium (100%)",
                "format": utils.thousands_format(0),
            },
            async_input=[
                "generate_rating_summary_xlsx_task",
            ],
        ),
        "technical_premium_pre_uw_adj_pro_rated_100pct": hx.Float(
            mode="output",
            view={
                "label": "Gross Technical Premium (Pre-UW Adjustment, 100%)",
                "format": utils.thousands_format(0),
            },
            async_input=[
                "generate_rating_summary_xlsx_task",
            ],
        ),
        "expected_loss_cost_pro_rated_100pct": hx.Float(
            mode="output",
            view={
                "label": "Expected Loss Cost (100%)",
                "format": utils.thousands_format(0),
            },
        ),
    }

    coverages_with_total_quoted_premiums = ["hull", "iv", "war"]

    if coverage_type in coverages_with_total_quoted_premiums:
        rating_summary_fields = {
            **rating_summary_fields,
            "total_quoted_premium": hx.Float(
                mode="output",
                view={
                    "label": "Achieved Premium",
                    "format": utils.thousands_format(0),
                },
                async_input=[
                    "generate_rating_summary_xlsx_task",
                ],
            ),
        }

    if coverage_type in ["loh", "ship_building", "hull"]:
        rating_summary_fields = {
            **rating_summary_fields,
            prefix
            + "lead_follow": hx.Str(
                mode="input",
                optionality="optional",
                default=None,
                options=["Lead", "Follow"],
                view={
                    "label": "Lead/Follow",
                },
                async_input=[
                    "generate_vessels_xlsx_task",
                    "generate_rating_summary_xlsx_task",
                ],
            ),
        }
        if coverage_type == "hull":
            rating_summary_fields = {
                **rating_summary_fields,
                "achieved_premium": hx.Float(
                    mode="output",
                    view={
                        "label": "Achieved Premium",
                        "format": utils.thousands_format(0),
                    },
                ),
            }
        else:
            rating_summary_fields = {
                **rating_summary_fields,
                prefix
                + "achieved_premium": hx.Float(
                    mode="input",
                    default=None,
                    optionality="optional",
                    async_input=[
                        "generate_rating_summary_xlsx_task",
                    ],
                    view={
                        "label": "Achieved Premium",
                        "format": utils.thousands_format(0),
                    },
                ),
            }

            if coverage_type == "loh":
                rating_summary_fields = {
                    **rating_summary_fields,
                    prefix
                    + "total_sum_insured": hx.Float(
                        mode="output",
                        view={
                            "label": "Total Sum Insured",
                            "format": utils.thousands_format(0),
                        },
                    ),
                    prefix
                    + "total_premium": hx.Float(
                        mode="output",
                        view={
                            "label": "Total Gross Benchmark Premium",
                            "format": utils.thousands_format(0),
                        },
                    ),
                    prefix
                    + "fleet_level": hx.Float(
                        mode="output",
                        view={
                            "label": "Fleet Level % Rate",
                            "format": utils.percent_format(3),
                        },
                    ),
                }
            elif coverage_type == "ship_building":
                rating_summary_fields = {
                    **rating_summary_fields,
                    "other_deductions": hx.Float(
                        mode="input",
                        optionality="optional",
                        default=None,
                        async_input=[
                            "rarc_task",
                            "generate_rating_summary_xlsx_task",
                        ],
                        view={
                            "label": "Other Deductions",
                            "format": utils.percent_format(2),
                            "options": {
                                "read_only_option": {"read_only": True},
                            },
                        },
                    ),
                }
    else:
        rating_summary_fields = {
            **rating_summary_fields,
            prefix
            + "lead_follow": hx.Str(
                mode="override",
                options=["Lead", "Follow"],
                view={
                    "label": "Lead/Follow",
                },
            ),
            prefix
            + "achieved_premium": hx.Float(
                mode="output",
                view={"label": "Achieved Premium", "format": utils.thousands_format(0)},
            ),
        }

    return rating_summary_fields


def sch_rating_summary(cds):
    cds.extend_node_rater_defined(
        "cds",
        {
            "uw_comment": hx.Str(
                mode="input",
                optionality="optional",
                default=None,
                view={"options": {"warning": {"style_cell": "hx-bad"}}},
                async_input=[
                    "generate_rating_summary_xlsx_task",
                ],
            )
        },
    )

    cds.extend_node_items(
        "cds/layers/coverages",
        {
            "iv": {"label": "IV"},
            "war": {"label": "War"},
            "loh": {"label": "Loss of Hire"},
            "ship_building": {"label": "Shipbuilders"},
            "hull": {"label": "Hull"},
        },
    )

    cds.extend_node_rater_defined(
        "cds/layers/coverages/hull",
        {
            **get_rating_summary_fields(coverage_type="hull"),
        },
    )

    cds.extend_node_rater_defined(
        "cds/layers/coverages/iv",
        {
            **get_rating_summary_fields(coverage_type="iv"),
            "iv_perc_of_h_and_m_value": hx.Float(
                mode="input",
                optionality="optional",
                default=None,
                validation={"min_value": 0, "max_value": 1},
                view={
                    "label": "IV Value as % of combined value of H&M and IV",
                    "format": utils.percent_format(2),
                    "info": "IV% represents the proportion of the total value made up of IV relative to H&M and IV combined. \nFor example, if IV% is 10% and the H&M value is $9m, the IV value would be $1m (i.e. 10% of the total $10m)."
                },
            ),
        },
    )

    cds.extend_node_rater_defined(
        "cds/layers/coverages/war",
        {**get_rating_summary_fields(coverage_type="war")},
    )
    cds.extend_node_rater_defined(
        "cds/layers/coverages/loh",
        {**get_rating_summary_fields(coverage_type="loh")},
    )

    cds.extend_node_rater_defined(
        "cds/layers/coverages/ship_building",
        {
            **get_rating_summary_fields(coverage_type="ship_building"),
            "ship_building_number_of_vessels": hx.Int(
                mode="input",
                default=None,
                optionality="optional",
                async_input=["ship_building_number_of_vessels_task"],
                view={
                    "label": "Number of Vessels",
                },
            ),
            "ship_building_policy_details": hx.Str(
                mode="input",
                optionality="required",
                default="Enter an overall time spent in production",
                async_input=[
                    "rarc_task",
                    "generate_rating_summary_xlsx_task",
                ],
                options=[
                    "Enter an overall time spent in production",
                    "Enter the time spent at each production stage",
                ],
                view={"label": "Policy Details"},
            ),
            "ship_building_show_production_stages_time": hx.Bool(
                mode="output",
                async_input=[
                    "generate_rating_summary_xlsx_task",
                ],
            ),
            "ship_building_show_overall_time": hx.Bool(mode="output"),
            "ship_building_is_war_cover": hx.Bool(
                mode="input",
                default=False,
                async_input=[
                    "rarc_task",
                    "generate_rating_summary_xlsx_task",
                ],
                view={"label": "Capture War Cover"},
            ),
            "ship_building_uw_adjustment": hx.Float(
                mode="input",
                optionality="optional",
                default=None,
                async_input=[
                    "generate_rating_summary_xlsx_task",
                ],
                view={
                    "label": "Underwriter Adjustment",
                    "format": utils.percent_format(0),
                },
                validation={"min_value": -0.5, "max_value": 0.5},
            ),
            "ship_building_experience_weighting": hx.Float(
                mode="output",
                async_input=[
                    "generate_rating_summary_xlsx_task",
                ],
                view={
                    "label": "Weight to Experience Based Premium (%)",
                    "format": utils.percent_format(0),
                },
            ),
            "ship_building_experience_premium": hx.Float(
                mode="output",
                async_input=[
                    "generate_rating_summary_xlsx_task",
                ],
                view={
                    "label": "Benchmark net premium (Experience Rated, 100%)",
                    "format": utils.thousands_format(0),
                },
            ),
            "ship_building_blended_benchmark_premium_pre_uw_adj": hx.Float(
                mode="output",
                async_input=[
                    "generate_rating_summary_xlsx_task",
                ],
                view={
                    "format": utils.thousands_format(0),
                },
            ),
            "ship_building_blended_benchmark_premium_post_uw_adj": hx.Float(
                mode="output",
                async_input=[
                    "generate_rating_summary_xlsx_task",
                ],
                view={
                    "format": utils.thousands_format(0),
                },
            ),
            "ship_building_net_benchmark_premium_pre_uw_adj": hx.Float(
                mode="output",
                async_input=[
                    "generate_rating_summary_xlsx_task",
                ],
                view={
                    "format": utils.thousands_format(0),
                },
            ),
        },
    )

    # Override values
    cds.override_node_properties(
        "cds/layers",
        {
            "max_element_count": max_layers,
            "async_input": [
                "ship_building_number_of_vessels_task",
                "generate_vessels_xlsx_task",
                "generate_rating_summary_xlsx_task",
                "push_vessels_to_datamart_task",
            ],
        },
    )

    cds.extend_node_rater_defined(
        "cds/layers/coverages",
        {
            "bpi_case_priced": hx.Float(
                mode="input",
                default=None,
                optionality="optional",
                view={"label": "BPI (Case Priced)", "format": percent_format(1)},
            ),
            "quoted_premium_case_priced": hx.Float(
                mode="input",
                default=None,
                optionality="optional",
                view={
                    "label": "Quoted Premium (Case Priced)",
                    "format": utils.thousands_format(0),
                },
            ),
            "rating_summary_brokerage": hx.Float(
                mode="output",
                view={
                    "label": "Brokerage",
                    "format": percent_format(2),
                },
                async_input=[
                    "generate_rating_summary_xlsx_task",
                ],
            ),
            "rating_summary_written_line": hx.Float(
                mode="output",
                view={
                    "label": "Written Line",
                    "format": percent_format(2),
                },
                async_input=[
                    "generate_rating_summary_xlsx_task",
                ],
            ),
        },
    )

    coverages = ["iv", "war", "loh", "ship_building", "hull"]

    mode_override_object = {
        "mode": "override",
        "async_input": [
            "generate_vessels_xlsx_task",
            "generate_rating_summary_xlsx_task",
            "rarc_task",
            "push_vessels_to_datamart_task",
        ],
        "view": {
            "options": {
                "read_only_option": {"read_only": True},
                "warning": {"style_cell": "hx-bad"},
            }
        },
    }
    override_coverages = ["iv", "war"]
    for coverage in coverages:
        cds.override_node_properties(
            f"cds/layers/coverages/{coverage}/written_line",
            (
                mode_override_object
                if coverage in override_coverages
                else {
                    "view": {
                        "options": {
                            "read_only_option": {"read_only": True},
                            "warning": {"style_cell": "hx-bad"},
                        },
                        "format": utils.percent_format(2),
                    },
                    "async_input": [
                        "generate_vessels_xlsx_task",
                        "generate_rating_summary_xlsx_task",
                        "push_vessels_to_datamart_task",
                    ],
                }
            ),
        )

        cds.override_node_properties(
            f"cds/layers/coverages/{coverage}/brokerage",
            (
                mode_override_object
                if coverage in override_coverages
                else {
                    "view": {
                        "options": {
                            "read_only_option": {"read_only": True},
                            "warning": {"style_cell": "hx-bad"},
                        },
                        "format": utils.percent_format(2),
                    },
                    "async_input": [
                        "generate_vessels_xlsx_task",
                        "generate_rating_summary_xlsx_task",
                        "rarc_task",
                    ],
                }
            ),
        )

        cds.override_node_properties(
            f"cds/layers/coverages/{coverage}/quoted_premium",
            {
                "view": {"label": "Gross Quoted/Achieved Premium (100%)"},
                "mode": "output",
                "async_input": [
                    "rarc_task",
                    "generate_rating_summary_xlsx_task",
                ],
            },
        )

        if coverage == "ship_building":
            cds.override_node_properties(
                f"cds/layers/coverages/{coverage}/section_reference",
                {
                    "view": {"label": "Policy Section Reference"},
                    "async_input": [
                        "populate_bi_data",
                        "generate_rating_summary_xlsx_task",
                        "upsert_hx_meta_policy_references_task",
                    ],
                    "async_output": [
                        {"task": "start_renewal_task", "reset": False},
                    ],
                },
            )
        else:
            cds.override_node_properties(
                f"cds/layers/coverages/{coverage}/section_reference",
                {
                    "view": {"label": "Policy Section Reference"},
                    "async_input": [
                        "generate_vessels_xlsx_task",
                        "generate_rating_summary_xlsx_task",
                        "push_vessels_to_datamart_task",
                        "upsert_hx_meta_policy_references_task",
                    ],
                    "async_output": [
                        {"task": "start_renewal_task", "reset": False},
                    ],
                },
            )

        cds.override_node_properties(
            f"cds/layers/coverages/{coverage}/status",
            {
                "view": {
                    "options": {
                        "input": {"label": "Status"},
                        "read_only": {
                            "label": "Deal Status by Renewal Layers",
                            "read_only": True,
                        },
                    }
                },
                "async_input": [
                    "generate_rating_summary_xlsx_task",
                ],
            },
        )

        cds.override_node_properties(
            f"cds/layers/coverages/{coverage}/tpi",
            {
                "async_input": [
                    "generate_rating_summary_xlsx_task",
                ],
                "view": {
                    "format": utils.percent_format(2),
                },
            },
        )

        cds.override_node_properties(
            f"cds/layers/coverages/{coverage}/bpi",
            {
                "async_input": [
                    "generate_rating_summary_xlsx_task",
                ],
                "view": {
                    "format": utils.percent_format(2),
                },
            },
        )

        cds.override_node_properties(
            f"cds/layers/coverages/{coverage}/tpi_pre_uw_adj",
            {
                "async_input": [
                    "generate_rating_summary_xlsx_task",
                ],
                "view": {
                    "format": utils.percent_format(2),
                },
            },
        )

        cds.override_node_properties(
            f"cds/layers/coverages/{coverage}/pflr",
            {
                "async_input": [
                    "generate_rating_summary_xlsx_task",
                ],
            },
        )

        cds.override_node_properties(
            f"cds/layers/coverages/{coverage}/pflr_pre_uw_adj",
            {
                "view": {
                    "format": utils.percent_format(1),
                },
            },
        )
        
        

        cds.override_node_properties(
            f"cds/layers/coverages/{coverage}/roc",
            {
                "async_input": [
                    "generate_rating_summary_xlsx_task",
                ],
            },
        )

        cds.override_node_properties(
            f"cds/layers/coverages/{coverage}/uw_adj_impact",
            {
                "async_input": [
                    "generate_rating_summary_xlsx_task",
                ],
            },
        )
