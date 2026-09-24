import hx_data_schema as hx

from algorithms.json_parameter_files.parameters import get_parameters
from data_schema.sch_utilities import percent_format, thousands_format

employer = get_parameters("employer.json")


def sch_fiduciary_non_cds():
    return {
        "is_state_ga": hx.Bool(mode="output", view={"label": "Is State GA"}),
        "is_state_ne": hx.Bool(mode="output", view={"label": "Is State NE"}),
        "is_state_oh": hx.Bool(mode="output", view={"label": "Is State OH"}),
        "is_per_occurrence_limit": hx.Bool(
            mode="output", view={"label": "Is per occurrence limit"}
        ),
        "is_surplus": hx.Bool(mode="output", view={"label": "Is Surplus"}),
        "is_fid_finished_rating": hx.Bool(mode="output", view={"label": "Is FID Finished Rating"}),
        "fid_premium_label": hx.Str(mode="output"),
        'is_multiple_fiduciary_covers': hx.Bool(mode="output", view={"label": "Is Multiple Fiduciary Covers Selected"}),
        'multiple_fiduciary_covers_message': hx.Str(mode="output", view={"label": "Multiple Fiduciary Covers Selected Message"}),
        "required_fiduciary_row_labels": hx.Structure(
            children={
                "option_selected" : hx.Str(mode="output"),
            }),
    }


def factor_selection():
    return {
        "rationale": hx.Str(mode="output", view={"label": "Rationale"}),
        "factor_selection": hx.Float(
            mode="input",
            default=0,
            view={"label": "Factor Selection", "format": percent_format(0)},
        ),
        "min": hx.Float(
            mode="output", view={"label": "Min", "format": percent_format(0)}
        ),
        "max": hx.Float(
            mode="output", view={"label": "Max", "format": percent_format(0)}
        ),
    }


def simple_factor_selection():
    return {
        "factor_selection": hx.Float(
            mode="input",
            default= None,
            optionality= "optional",
            view={
                "label": "Factor Selection",
                "group": "Non-Admitted",
                "format": percent_format(0),
            },
        ),
        "min": hx.Float(
            mode="output",
            view={"label": "Min", "group": "Non-Admitted", "format": percent_format(0)},
        ),
        "max": hx.Float(
            mode="output",
            view={"label": "Max", "group": "Non-Admitted", "format": percent_format(0)},
        ),
    }


def benchmark_factor_selection():
    return {
        "factor_selection": hx.Float(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Factor Selection", "format": percent_format(0)}            
        ),
        "min": hx.Float(
            mode="output", view={"label": "Min", "format": percent_format(0)}
        ),
        "max": hx.Float(
            mode="output", view={"label": "Max", "format": percent_format(0)}
        ),
    }


def admitted_schedule_function_rationale():
    return {
        "sponsor": hx.Str(mode="input", default=None, optionality='optional', view={"label": "Sponsor"}),
        "benefit_plan": hx.Str(mode="input", default=None, optionality='optional', view={"label": "Benefit Plan"}),
        "litigation": hx.Str(mode="input", default=None, optionality='optional', view={"label": "Litigation"}),
        "other": hx.Str(mode="input", default=None, optionality='optional', view={"label": "Other"}),
        "expense_factor": hx.Str(mode="input", default=None, optionality='optional', view={"label": "Expense Factor"}),
    }


def admitted_schedule_function_factor_selection():
    return {
        "sponsor": hx.Float(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Sponsor", "format": percent_format(0)},
        ),
        "benefit_plan": hx.Float(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Benefit Plan", "format": percent_format(0)},
        ),
        "litigation": hx.Float(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Litigation", "format": percent_format(0)},
        ),
        "other": hx.Float(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Other", "format": percent_format(0)},
        ),
        "expense_factor": hx.Float(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Expense Factor", "format": percent_format(0)},
        ),
        "total_schedule_rating_modifier": hx.Float(
            mode="output",
            view={
                "label": "Total Schedule Rating Modifier",
                "format": percent_format(0),
            },
        ),
    }


def admitted_schedule_function_min():
    return {
        "sponsor": hx.Float(
            mode="output", view={"label": "Sponsor", "format": percent_format(0)}
        ),
        "benefit_plan": hx.Float(
            mode="output", view={"label": "Benefit Plan", "format": percent_format(0)}
        ),
        "litigation": hx.Float(
            mode="output", view={"label": "Litigation", "format": percent_format(0)}
        ),
        "other": hx.Float(
            mode="output", view={"label": "Other", "format": percent_format(0)}
        ),
        "expense_factor": hx.Float(
            mode="output", view={"label": "Expense Factor", "format": percent_format(0)}
        ),
        "total_schedule_rating_modifier": hx.Float(
            mode="output",
            view={
                "label": "Total Schedule Rating Modifier",
                "format": percent_format(0),
            },
        ),
    }


def admitted_schedule_function_max():
    return {
        "sponsor": hx.Float(
            mode="output", view={"label": "Sponsor", "format": percent_format(0)}
        ),
        "benefit_plan": hx.Float(
            mode="output", view={"label": "Benefit Plan", "format": percent_format(0)}
        ),
        "litigation": hx.Float(
            mode="output", view={"label": "Litigation", "format": percent_format(0)}
        ),
        "other": hx.Float(
            mode="output", view={"label": "Other", "format": percent_format(0)}
        ),
        "expense_factor": hx.Float(
            mode="output", view={"label": "Expense Factor", "format": percent_format(0)}
        ),
        "total_schedule_rating_modifier": hx.Float(
            mode="output",
            view={
                "label": "Total Schedule Rating Modifier",
                "format": percent_format(0),
            },
        ),
    }


def sch_usml_fiduciary_inputs(cds):
    # Employer Type table
    cds.extend_node_rater_defined(
        "cds",
        {
            "fid": hx.Structure(
                view={"label": "Fiduciary"},
                children={
                    # Total Admitted Modifier
                    "employer_type": hx.Str(
                        mode="input",
                        optionality="optional",
                        options=list(employer.keys()),
                        default_index=0,
                        view={"label": "Employer Type"},
                        async_input=["rarc_task"],
                    ),
                    "base_premium": hx.Structure(
                        view={"label": "Base Premium"},
                        children={
                            "bp_plans": hx.List(
                                mode="input",
                                default_element_count=1,                                
                                children={
                                    "plan_title": hx.Str(mode="output"
                                    ),
                                    "assets_contributions": hx.Float(
                                        mode="input",
                                        optionality="optional",
                                        default=None,
                                        view={"label": "Assets/Contributions",
                                        "info": "Additional Plans can be added by right clicking in the adjacent cell and inserting a new column.",
                                        "format": thousands_format(0)},
                                        async_input=["rarc_task"],
                                        
                                    ),
                                    "total_employees_or_members": hx.Float(
                                        mode="input",
                                        optionality="optional",
                                        default=None,
                                        view={"label": "Total Employees or Members",
                                        "format": thousands_format(0)},
                                        async_input=["rarc_task"],
                                    ),
                                    "additional_designated_fiduciaries": hx.Float(
                                        mode="input",
                                        optionality="optional",
                                        default=None,
                                        view={
                                            "label": "Additional Designated Fiduciaries",
                                            "format": thousands_format(0)
                                        },
                                        async_input=["rarc_task"],
                                    ),
                                    "plan_type": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_column="Response",
                                        options_table="table_plan_type",
                                        default_index=0,
                                        view={"label": "Plan Type"},
                                        async_input=["rarc_task"],
                                    ),
                                    "reactive_employee_exposure": hx.Structure(
                                        children={
                                            "reactive_employee_exposure_dropdown": hx.List(
                                                mode="output",
                                                children={
                                                    "dropdown_item": hx.Str(
                                                        mode="output"
                                                    )
                                                },
                                            ),
                                            "employee_exposure": hx.Str(
                                                mode="input",
                                                optionality="optional",
                                                options_field="dropdown_item",
                                                options_data="../reactive_employee_exposure_dropdown",
                                                default=None,
                                                view={"label": "Employee Exposure"},
                                                async_input=["rarc_task"],
                                            ),
                                        }
                                    ),
                                    "percent_of_active_participants": hx.Float(
                                        mode="input",
                                        optionality="optional",
                                        default=None,
                                        view={
                                            "label": "Percent of Active Participants",
                                            "format": percent_format(0)
                                        },
                                        async_input=["rarc_task"],
                                    ),
                                },
                            )
                        },
                    ),
                    # Plan Sponsor table
                    "plan_sponsor": hx.Structure(
                        view={"label": "Plan Sponsor"},
                        children={
                            "reactive_financial_condition": hx.Structure(
                                children={
                                    "reactive_financial_condition_dropdown": hx.List(
                                        mode="output",
                                        children={
                                            "dropdown_item": hx.Str(mode="output")
                                        },
                                    ),
                                    "financial_condition": hx.Structure(
                                        view={"label": "Financial Condition"},
                                        children={
                                            "selection": hx.Str(
                                                mode="input",
                                                optionality="optional",
                                                options_field="dropdown_item",
                                                options_data="../../reactive_financial_condition_dropdown",
                                                default="Average",
                                                view={"label": "Selection"},
                                            ),
                                            **simple_factor_selection(),
                                        },
                                    ),
                                }
                            ),
                            "merger_acquisition_activity": hx.Structure(
                                view={"label": "Merger Acquisition Activity"},
                                children={
                                    "selection": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_column="Response",
                                        options_table="table_merger_acquisition",
                                        default_index=1,
                                        view={"label": "Selection"},
                                    ),
                                    **simple_factor_selection(),
                                },
                            ),
                            "industry_quality": hx.Structure(
                                view={"label": "Industry Quality"},
                                children={
                                    "selection": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_column="Response",
                                        options_table="table_industry",
                                        default_index=1,
                                        view={"label": "Selection"},
                                    )
                                },
                            ),
                            "reactive_layoffs_downsizing_spinoffs": hx.Structure(
                                children={
                                    "reactive_layoffs_downsizing_spinoffs_dropdown": hx.List(
                                        mode="output",
                                        children={
                                            "dropdown_item": hx.Str(mode="output")
                                        },
                                    ),
                                    "layoffs_downsizing_spinoffs": hx.Structure(
                                        view={
                                            "label": "Layoffs, Downsizing, or Spin-Offs"
                                        },
                                        children={
                                            "selection": hx.Str(
                                                mode="input",
                                                optionality="optional",
                                                options_field="dropdown_item",
                                                options_data="../../reactive_layoffs_downsizing_spinoffs_dropdown",
                                                default="None in prior two years and none anticipated during the next year.",
                                                view={"label": "Selection"},
                                            )
                                        },
                                    ),
                                }
                            ),
                            "type_of_union": hx.Structure(
                                view={"label": "Type of Union"},
                                children={
                                    "selection": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_column="Response",
                                        options_table="table_type_of_union",
                                        default_index=0,
                                        view={"label": "Selection"},
                                    )
                                },
                            ),
                        },
                    ),
                    # Benefit Plans table
                    "benefit_plans": hx.Structure(
                        view={"label": "Benefit Plans"},
                        children={
                            "reactive_financial_condition_bp": hx.Structure(
                                children={
                                    "reactive_financial_condition_bp_dropdown": hx.List(
                                        mode="output",
                                        children={
                                            "dropdown_item": hx.Str(mode="output")
                                        },
                                    ),
                                    "financial_condition_bp": hx.Structure(
                                        view={"label": "Financial Condition"},
                                        children={
                                            "selection": hx.Str(
                                                mode="input",
                                                optionality="optional",
                                                options_field="dropdown_item",
                                                options_data="../../reactive_financial_condition_bp_dropdown",
                                                default="Average",
                                                view={"label": "Selection"},
                                            ),
                                            **simple_factor_selection(),
                                        },
                                    ),
                                }
                            ),
                            "outside_professionals": hx.Structure(
                                view={"label": "Outside Professionals"},
                                children={
                                    "selection": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_column="Response",
                                        options_table="table_outside_professionals",
                                        default_index=1,
                                        view={"label": "Selection"},
                                    ),
                                    **simple_factor_selection(),
                                },
                            ),
                            "funding_level": hx.Structure(
                                view={"label": "Funding Level"},
                                children={
                                    "selection": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_column="Response",
                                        options_table="table_funding_level",
                                        default_index=1,
                                        view={"label": "Selection"},
                                    )
                                },
                            ),
                            "investments_expenses": hx.Structure(
                                view={"label": "Investments/Expenses"},
                                children={
                                    "selection": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_column="Response",
                                        options_table="table_investment_expenses",
                                        default_index=0,
                                        view={"label": "Selection"},
                                    )
                                },
                            ),
                            "asset_performance": hx.Structure(
                                view={"label": "Asset Performance"},
                                children={
                                    "selection": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_column="Response",
                                        options_table="table_asset_performance",
                                        default_index=0,
                                        view={"label": "Selection"},
                                    )
                                },
                            ),
                            "benefits": hx.Structure(
                                view={"label": "Benefits"},
                                children={
                                    "selection": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_column="Response",
                                        options_table="table_benefits",
                                        default_index=0,
                                        view={"label": "Selection"},
                                    )
                                },
                            ),
                        },
                    ),
                    # Litigation table
                    "reactive_litigation": hx.Structure(
                        children={
                            "reactive_litigation_dropdown": hx.List(
                                mode="output",
                                children={"dropdown_item": hx.Str(mode="output")},
                            ),
                            "litigation": hx.Structure(
                                view={"label": "Litigation"},
                                children={
                                    "selection": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_field="dropdown_item",
                                        options_data="../../reactive_litigation_dropdown",
                                        default="None",
                                        view={"label": "Selection"},
                                    )
                                },
                            ),
                        }
                    ),
                    # Foreign Charge table
                    "number_of_plans_outside_us": hx.Structure(
                        view={"label": "Number of Plans outside the US"},
                        children={
                            "number_of_plans_outside_us": hx.Int(
                                mode="input",
                                default=0,
                                view={"label": "# of Plans Outside the U.S."},
                            ),
                            "factor_selection": hx.Float(
                                mode="input",
                                default=None,
                                optionality= "optional",
                                view={
                                    "label": "Factor Selection",
                                    "format": percent_format(0),
                                },
                            ),
                            "min": hx.Float(
                                mode="output",
                                view={"label": "Min", "format": percent_format(0)},
                            ),
                            "max": hx.Float(
                                mode="output",
                                view={"label": "Max", "format": percent_format(0)},
                            ),
                        },
                    ),
                },
            )
        },
    ),

    cds.extend_node_rater_defined(
        "cds/layers",
        {
            "fid": hx.Structure(
                view={"label": "Fiduciary"},
                children={
                    "admitted_schedule_rating": hx.Structure(
                        view={"label": "Admitted Schedule Rating"},
                        children={
                            "rationale": hx.Structure(
                                view={"label": "Rationale"},
                                children={**admitted_schedule_function_rationale()},
                            ),
                            "factor_selection": hx.Structure(
                                view={"label": "Factor Selection"},
                                children={
                                    **admitted_schedule_function_factor_selection()
                                },
                            ),
                            "min": hx.Structure(
                                view={"label": "Min"},
                                children={**admitted_schedule_function_min()},
                            ),
                            "max": hx.Structure(
                                view={"label": "Max"},
                                children={**admitted_schedule_function_max()},
                            ),
                        },
                    ),
                    # Expense Rating table
                    "expense_rating": hx.Structure(
                        view={"label": "Expense Rating"},
                        children={
                            "factor_selection": hx.Float(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={
                                    "label": "Factor Selection",
                                    "format": percent_format(0),
                                },
                            ),
                            "min": hx.Float(
                                mode="output",
                                view={"label": "Min", "format": percent_format(0)},
                            ),
                            "max": hx.Float(
                                mode="output",
                                view={"label": "Max", "format": percent_format(0)},
                            ),
                        },
                    ),
                    # NE Deviation Factor
                    "ne_deviation_factor": hx.Structure(
                        view={"label": "NE Deviation Factor"},
                        children={
                             "rationale": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Rationale"},
                            ),
                            "credit_debit": hx.Float(
                                mode="input",
                                optionality = "optional",
                                default=None,
                                view={
                                    "label": "Rate Credit/Debit",
                                    "format": percent_format(0),
                                },
                            ),
                            "min": hx.Float(
                                mode="output",
                                view={"label": "Min", "format": percent_format(0)},
                            ),
                            "max": hx.Float(
                                mode="output",
                                view={"label": "Max", "format": percent_format(0)},
                            ),
                        },
                    ),
                    # Surplus Deviation
                    "surplus_deviation": hx.Float(
                        mode="input", default=None, optionality='optional', 
                        view={"label": "Surplus Deviation",
                        "format": {"output": "percent", "mantissa": 0}}
                    ),
                    # Benchmark UW Modifiers table
                    "benchmark_uw_modifiers": hx.Structure(
                        view={"label": "Benchmark UW Modifiers"},
                        children={
                            "prior_claim_activity": hx.Structure(
                                view={"label": "Prior Claim Activity"},
                                children={**benchmark_factor_selection()},
                            ),
                            "additional_risk_characteristics": hx.Structure(
                                view={"label": "Additional Risk Characteristics"},
                                children={**benchmark_factor_selection()},
                            ),
                        },
                    ),
                },
            )
        },
    )

    cds.extend_node_rater_defined(
        "cds/layers/coverages/fid",
        {
            # Quote Grid
            "quote_grid": hx.Structure(
                view={"label": "Quote Grid"},
                children={
                    "qg_options": hx.List(
                        mode="input",
                        default_element_count=1,
                        children={
                            "aggregate_limit": hx.Float(
                                mode="input",
                                optionality="optional",
                                default=None,
                                view={
                                    "label": "Aggregate Limit",
                                    "format": thousands_format(0),
                                },
                                async_input=["rarc_task"]
                            ),
                            "per_occurrence_limit": hx.Str(
                                mode="input",
                                optionality="optional",
                                default=None,
                                view={"label": "Per Occurrence Limit"},
                            ),
                            "adl_limit": hx.Float(
                                mode="input",
                                optionality="optional",
                                default=None,
                                view={
                                    "label": "Additional Defense Limit",
                                    "format": thousands_format(0),
                                },
                                async_input=["rarc_task"]
                            ),
                            "retention": hx.Float(
                                mode="input",
                                optionality="optional",
                                default=None,
                                view={
                                    "label": "Retention",
                                    "format": thousands_format(0),
                                },
                                async_input=["rarc_task"]
                            ),
                            "voluntary_compliance_fees_and_defense": hx.Float(
                                mode="input",
                                optionality="optional",
                                default=None,
                                view={"label": "Voluntary Compliance Fees and Defense"},
                            ),
                            "admitted_premium": hx.Float(
                                mode="output",
                                view={
                                    "label": "Admitted Premium",
                                    "format": thousands_format(0),
                                },
                            ),
                            "internal_benchmark": hx.Float(
                                mode="output",
                                view={
                                    "label": "Internal Benchmark",
                                    "format": thousands_format(0),
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
                            "internal_benchmark_pre_uw_adj": hx.Float(
                                mode="output",
                                view={
                                    "label": "Internal Benchmark (pre UW Adjustment)",
                                    "format": thousands_format(0),
                                },
                            ),
                            "bpi": hx.Float(
                                mode="output",
                                view={
                                    "label": "Coverage BPI%", "format": percent_format(0),
                                },
                            ),
                            "option_selected": hx.Bool(
                                mode="input",
                                default=True,
                                view={"label": "Select Option?"},
                            ),
                        },
                    )
                },
            ),
            "minimum_admitted_agg_limit": hx.Int(
                mode="output", view={"label": "Minimum Admitted Agg Limit"}
            ),
            "internal_guideline_retention": hx.Int(
                mode="output", view={"label": "Internal Guideline Retention"}
            ),
        },
    )
def running_prem_summary_childern():
    return{
        "modifier": hx.Float(mode="output", view={"label": "Modifier", "format": {"thousandSeparated": True, "mantissa": 2}}),
        "prem": hx.Float(mode="output", view={"label": "Running Premium", "format": {"thousandSeparated": True, "mantissa": 2}}),
    }

def sch_running_prem_summary_fid(cds):
    cds.extend_node_rater_defined("cds/layers/coverages/fid", {
        "running_prem_sum": hx.Structure(children={
            "base_rate": hx.Structure(view={"label": "Base Premium"}, children={**running_prem_summary_childern()}),
            "lim_adj": hx.Structure(view={"label": "Limit Adjustment"}, children={**running_prem_summary_childern()}),
            "retention_adj": hx.Structure(view={"label": "Retention Adjustment"}, children={**running_prem_summary_childern()}),
            "fl_adj": hx.Structure(view={"label": "FL Adjustment"}, children={**running_prem_summary_childern()}),
            "risk_char_adj": hx.Structure(view={"label": "Risk Characteristics Adjustment"}, children={**running_prem_summary_childern()}),
            "lim_compression_adj": hx.Structure(view={"label": "Limit Compression Adjustment"}, children={**running_prem_summary_childern()}),
            "adl_adj": hx.Structure(view={"label": "ADL Adjustment"}, children={**running_prem_summary_childern()}),
            "fcf_adj": hx.Structure(view={"label": "Foreign Charge Adjustment"}, children={**running_prem_summary_childern()}),
            "vcfdc_adj": hx.Structure(view={"label": "Voluntary Compliance Fees and Defense Adjustment"}, children={**running_prem_summary_childern()}),
            "exp_fac_adj": hx.Structure(view={"label": "Expense Factor Adjustment"}, children={**running_prem_summary_childern()}),
            "prior_acts_adj": hx.Structure(view={"label": "Prior Acts Adjustment"}, children={**running_prem_summary_childern()}),            
            "sch_rating_adj": hx.Structure(view={"label": "Schedule Rating Adjustment"}, children={**running_prem_summary_childern()}),
        })  
    })