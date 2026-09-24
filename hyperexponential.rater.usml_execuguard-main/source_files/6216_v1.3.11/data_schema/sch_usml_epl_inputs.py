import hx_data_schema as hx


def sch_epl_non_cds():
    return {
        "is_split_retention": hx.Bool(mode="output", view={"label": "Is Split Retention"}),
        "is_state_ca": hx.Bool(mode="output", view={"label": "Is State CA"}),
        "is_state_in": hx.Bool(mode="output", view={"label": "Is State IN"}),
        "is_state_in_hide": hx.Bool(mode="output", view={"label": "Is Not State IN"}),
        "is_state_ne_hide": hx.Bool(mode="output", view={"label": "Is State NE Hide"}),
        "is_state_ca_or_in": hx.Bool(mode="output", view={"label": "Is State CA or IN"}),
        "is_state_ca_or_in_hide": hx.Bool(mode="output", view={"label": "Is State CA or IN Hide"}),
        'is_leader_preferred': hx.Bool(mode="output", view={"label": "Is Leader Preferred"}),
        'is_multiple_epl_covers': hx.Bool(mode="output", view={"label": "Is Multiple EPL Covers Selected"}),
        'multiple_epl_covers_message': hx.Str(mode="output", view={"label": "Multiple EPL Covers Selected Message"}),
        "punitive_damages_acceptable":hx.Bool(mode="output"),
        "punitive_damages_not_acceptable":hx.Bool(mode="output"),
        'required_epl_row_labels': hx.Structure(
                    children={
                        "punitive_damages": hx.Str(mode="output"),
                        "option_selected" : hx.Str(mode="output"),
                        "financial_stability" : hx.Str(mode="output"),
                        "loss_prevention_and_mitigation" : hx.Str(mode="output"),
                        "employment_policies" : hx.Str(mode="output"),

                    }),
        "hr_policies_label": hx.Str(mode = "output"),
        "is_epl_finished_rating": hx.Bool(mode="output", view={"label": "Is EPL Finished Rating"}),
        "epl_premium_label": hx.Str(mode="output")          

    }
    

def quotegrid():
    return {
        "option_1": hx.Str(mode="input", default="", view={"label": "Option 1"}),
        "option_2": hx.Str(mode="input", default="", view={"label": "Option 2"}),
        "option_3": hx.Str(mode="input", default="", view={"label": "Option 3"}),
    }


def state_split_children():
    return {
        "state": hx.Str(
            mode="input",
            optionality="optional",
            options_column="State Name",
            options_table="table_state",
            default=None,
            view={"label": "State"},
        ),
        # Retention
        "retention": hx.Float(
            mode="input",
            default=None,
            optionality="optional",
            view={
                "label": "Retention",
                "format": {"thousandSeparated": True, "mantissa": 0},
            },
        ),
        # Proportion
        "proportion": hx.Float(
            mode="output",
            view={
                "label": "Proportion",
                "format": {"thousandSeparated": True, "mantissa": 2},
            },
        ),
        # Retention Factor
        "retention_factor": hx.Float(
            mode="output",
            view={
                "label": "Retention Factor",
                "format": {"thousandSeparated": True, "mantissa": 2},
            },
        ),
        # Weighted Factor
        "weighted_factor": hx.Float(
            mode="output",
            view={
                "label": "Weighted Factor",
                "format": {"thousandSeparated": True, "mantissa": 2},
            },
        ),
    }


def option_split_children():
    return {
        "basis_for_split": hx.Str(
            mode="input",
            default=None,
            optionality="optional",
            options=["Location", "Salary", "Multi Plaintiff", "Employee"],
            view={"label": "Basis for Split"},
        ),
        # Detail
        "detail": hx.Str(mode="output", view={"label": "Detail"}),
        # Retention
        "retention": hx.Float(
            mode="input",
            default=None,
            optionality="optional",
            view={
                "label": "Retention",
                "format": {"thousandSeparated": True, "mantissa": 0},
            },
        ),
        # Retention Modifier
        "retention_modifier": hx.Float(
            mode="input",
            default=None,
            optionality="optional",
            view={
                "label": "Retention Modifier (%)",
                "format": {"output": "percent", "mantissa": 1},
            },
        ),
    }


def sch_usml_epl_inputs(cds):   

    cds.extend_node_rater_defined(
    "cds/layers/coverages/epl",
    {
        # Quote Grid
        "quote_grid": hx.Structure(
            view={"label": "Quote Grid"},
            children={
                "qg_options": hx.List(
                    mode="input",
                    default_element_count=1,
                    children={
                        #
                        # Aggregate Limit
                        "aggregate_limit": hx.Float(
                            mode="input",
                            default=None,
                            optionality="optional",
                            view={
                                "label": "Aggregate Limit",
                                "format": {
                                    "thousandSeparated": True,
                                    "mantissa": 0,
                                },
                            },
                            async_input=["rarc_task"]
                        ),
                        # Additional Defense Limit
                        "adl_limit": hx.Float(
                            mode="input",
                            default=None,
                            optionality="optional",
                            view={
                                "label": "Additional Defense Limit",
                                "format": {
                                    "thousandSeparated": True,
                                    "mantissa": 0,
                                },
                            },
                            async_input=["rarc_task"]                            
                        ),
                        # Additional Employment Event Loss Limit
                        "event_loss_limit": hx.Float(
                            mode="input",
                            default=None,
                            optionality="optional",
                            view={
                                "label": "Additional Employment Event Loss Limit",
                                "format": {
                                    "thousandSeparated": True,
                                    "mantissa": 0,
                                },
                            },
                        ),
                        # Retention
                        "retention": hx.Float(
                            mode="input",
                            default=None,
                            optionality="optional",
                            view={
                                "label": "Retention",
                                "format": {
                                    "thousandSeparated": True,
                                    "mantissa": 0,
                                },
                            },
                            async_input=["rarc_task"]
                        ),
                        # Admitted Premium
                        "admitted_premium": hx.Float(
                            mode="output",
                            view={
                                "label": "Admitted Premium",
                                "format": {
                                    "thousandSeparated": True,
                                    "mantissa": 0,
                                },
                            },
                        ),
                           # Guideline Minimum retention
                        "miniumum_retention": hx.Float(
                            mode="output",
                            view={
                                "label": "Minimum Retention",
                                "format": {
                                    "thousandSeparated": True,
                                    "mantissa": 0,
                                },
                            },
                        ),
                        # Guideline Minimum Premium
                        "guideline_minimum_premium": hx.Float(
                            mode="output",
                            view={
                                "label": "Guideline Minimum Premium",
                                "format": {
                                    "thousandSeparated": True,
                                    "mantissa": 0,
                                },
                            },
                        ),

                        # Select Option?
                        "option_selected": hx.Bool(
                            mode="input",
                            default=True,
                            view={"label": "Select Option?"},
                        ),
                        # Guideline Retention
                        "guideline_retention": hx.Float(
                            mode="output",
                            view={
                                "label": "Guideline Retention",
                                "format": {
                                    "thousandSeparated": True,
                                    "mantissa": 0,
                                },
                            },
                        ),
                        # Internal Benchmark
                        "internal_benchmark": hx.Float(
                            mode="output",
                            view={
                                "label": "Internal Benchmark",
                                "format": {
                                    "thousandSeparated": True,
                                    "mantissa": 2,
                                },
                            },
                        ),
                        # Internal Benchmark pre UW Adj
                        "internal_benchmark_pre_uw_adj": hx.Float(
                            mode="output",
                            view={
                                "label": "Internal Benchmark (pre UW Adjustment)",
                                "format": {
                                    "thousandSeparated": True,
                                    "mantissa": 0,
                                },
                            },
                        ),
                        # Coverage BPI%
                        "bpi": hx.Float(
                            mode="output",
                            view={
                                "label": "Coverage BPI%",
                                "format": {"output": "percent", "mantissa": 1},
                            },
                        ),
                    },
                ),
            },
        ),

        #### State Split
        # Main Retention Selected
        "main_retention_selected": hx.Float(
            mode="output",
            view={
                "label": "Main Retention Selected",
                "format": {"thousandSeparated": True, "mantissa": 0},
            },
        ),
        # State
        "state_split": hx.Structure(
            view={"label": "State Split"},
            children={
                "state_split_1": hx.Structure(
                    view={"label": "State Split 1"},
                    children={**state_split_children()},
                ),
                "state_split_2": hx.Structure(
                    view={"label": "State Split 2"},
                    children={**state_split_children()},
                ),
                "state_split_3": hx.Structure(
                    view={"label": "State Split 3"},
                    children={**state_split_children()},
                ),
                "state_split_4": hx.Structure(
                    view={"label": "State Split 4"},
                    children={**state_split_children()},
                ),
                "state_split_5": hx.Structure(
                    view={"label": "State Split 5"},
                    children={**state_split_children()},
                ),
            },
        ),
        "option_split": hx.Structure(
            view={"label": "State Split"},
            children={
                "option_split_1": hx.Structure(
                    view={"label": "Option Split 1"},
                    children={**option_split_children()},
                ),
                "option_split_2": hx.Structure(
                    view={"label": "Option Split 2"},
                    children={**option_split_children()},
                ),
            },
        )},
    )


def running_prem_summary_childern():
    return{
        "modifier": hx.Float(mode="output", view={"label": "Modifier", "format": {"thousandSeparated": True, "mantissa": 2}}),
        "prem": hx.Float(mode="output", view={"label": "Running Premium", "format": {"thousandSeparated": True, "mantissa": 2}}),
    }

def sch_running_prem_summary_epl(cds):
    cds.extend_node_rater_defined("cds/layers/coverages/epl", {
        "running_prem_sum": hx.Structure(children={
            "base_rate": hx.Structure(view={"label": "Base Premium"}, children={**running_prem_summary_childern()}),
            "lim_adj": hx.Structure(view={"label": "Limit Adjustment"}, children={**running_prem_summary_childern()}),
            "modifier_adj": hx.Structure(view={"label": "Modifier Adjustment"}, children={**running_prem_summary_childern()}),
            "state_adj": hx.Structure(view={"label": "State Adjustment"}, children={**running_prem_summary_childern()}),
            "ded_adj": hx.Structure(view={"label": "Deductible Adjustment"}, children={**running_prem_summary_childern()}),
            "coinsurance_adj": hx.Structure(view={"label": "Coinsurance Adjustment"}, children={**running_prem_summary_childern()}),
            "employment_event_adj": hx.Structure(view={"label": "Employment Event Adjustment"}, children={**running_prem_summary_childern()}),
            "adl_adj": hx.Structure(view={"label": "ADL Adjustment"}, children={**running_prem_summary_childern()}),
            "sch_rating_adj": hx.Structure(view={"label": "Schedule Rating Adjustment"}, children={**running_prem_summary_childern()}),
            "prior_acts_adj": hx.Structure(view={"label": "Prior Acts Adjustment"}, children={**running_prem_summary_childern()}),
            "ne_deviation_adj": hx.Structure(view={"label": "NE Deviation Adjustment"}, children={**running_prem_summary_childern()}),
            "surp_dev_adj": hx.Structure(view={"label": "Surplus Deviation Adjustment"}, children={**running_prem_summary_childern()}),
        })  
    })
    

