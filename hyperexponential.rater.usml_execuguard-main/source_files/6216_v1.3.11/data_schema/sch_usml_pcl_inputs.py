import hx_data_schema as hx

from data_schema.sch_utilities import percent_format


def sch_pcl_non_cds():
    return {
        "is_table_cw": hx.Bool(mode="output", view={"label": "Table CW"}),
        "is_table_ca": hx.Bool(mode="output", view={"label": "Table CA"}),
        "is_table_la": hx.Bool(mode="output", view={"label": "Table LA"}),
        "is_table_mo": hx.Bool(mode="output", view={"label": "Table MO"}),
        "is_punitive_damages": hx.Bool(mode="output", view={"label": "Is Removal of Punitive Damages Allowed"}),
        "is_pcl_finished_rating": hx.Bool(mode="output", view={"label": "Is PCL Finished Rating"}),
        "pcl_premium_label": hx.Str(mode="output"),
        'is_multiple_pcl_covers': hx.Bool(mode="output", view={"label": "Is Multiple PCL Covers Selected"}),
        'multiple_pcl_covers_message': hx.Str(mode="output", view={"label": "Multiple PCL Covers Selected Message"}),
        "required_pcl_row_labels": hx.Structure(
            children={
                "option_selected" : hx.Str(mode="output"),
            }),
    }

def quotegrid():
    return {
        "option_1": hx.Str(mode="input", default="", view={"label": "Option 1"}),
        "option_2": hx.Str(mode="input", default="", view={"label": "Option 2"}),
        "option_3": hx.Str(mode="input", default="", view={"label": "Option 3"}),
    }


def admitted_schedule_function_rationale():
    return {
        "prior_claim_activity": hx.Str(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Prior Claim Activity", "format": percent_format(0)},
        ),
        "financial_strength": hx.Str(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Financial Strength", "format": percent_format(0)},
        ),
        "mergers_and_acquisitions": hx.Str(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Mergers and Acquisitions", "format": percent_format(0)},
        ),
        "quality_of_board": hx.Str(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Quality of Board", "format": percent_format(0)},
        ),
        "length_of_time_in_business": hx.Str(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Length of Time in Business", "format": percent_format(0)},
        ),
        "size_of_revenues_assets_employees": hx.Str(
            mode="input",
            default=None,
            optionality="optional",
            view={
                "label": "Size - Revenues/Assets/Employees",
                "format": percent_format(0),
            },
        ),
        "layoffs_downsizing_spinoffs": hx.Str(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Layoffs/Downsizing/Spin-offs", "format": percent_format(0)},
        ),
        "ownership_control": hx.Str(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Ownership/Control", "format": percent_format(0)},
        ),
    }


def admitted_schedule_function_factor_selection():
    return {
        "prior_claim_activity": hx.Float(
            mode="input",
            default=0,
            view={"label": "Prior Claim Activity", "format": percent_format(0)},
        ),
        "financial_strength": hx.Float(
            mode="input",
            default=0,
            view={"label": "Financial Strength", "format": percent_format(0)},
        ),
        "mergers_and_acquisitions": hx.Float(
            mode="input",
            default=0,
            view={"label": "Mergers and Acquisitions", "format": percent_format(0)},
        ),
        "quality_of_board": hx.Float(
            mode="input",
            default=0,
            view={"label": "Quality of Board", "format": percent_format(0)},
        ),
        "length_of_time_in_business": hx.Float(
            mode="input",
            default=0,
            view={"label": "Length of Time in Business", "format": percent_format(0)},
        ),
        "size_of_revenues_assets_employees": hx.Float(
            mode="input",
            default=0,
            view={
                "label": "Size - Revenues/Assets/Employees",
                "format": percent_format(0),
            },
        ),
        "layoffs_downsizing_spinoffs": hx.Float(
            mode="input",
            default=0,
            view={"label": "Layoffs/Downsizing/Spin-offs", "format": percent_format(0)},
        ),
        "ownership_control": hx.Float(
            mode="input",
            default=0,
            view={"label": "Ownership/Control", "format": percent_format(0)},
        ),
    }


def admitted_schedule_function_min():
    return {
        "prior_claim_activity": hx.Float(
            mode="output",
            view={"label": "Prior Claim Activity", "format": percent_format(0)},
        ),
        "financial_strength": hx.Float(
            mode="output",
            view={"label": "Financial Strength", "format": percent_format(0)},
        ),
        "mergers_and_acquisitions": hx.Float(
            mode="output",
            view={"label": "Mergers and Acquisitions", "format": percent_format(0)},
        ),
        "quality_of_board": hx.Float(
            mode="output",
            view={"label": "Quality of Board", "format": percent_format(0)},
        ),
        "length_of_time_in_business": hx.Float(
            mode="output",
            view={"label": "Length of Time in Business", "format": percent_format(0)},
        ),
        "size_of_revenues_assets_employees": hx.Float(
            mode="output",
            view={
                "label": "Size - Revenues/Assets/Employees",
                "format": percent_format(0),
            },
        ),
        "layoffs_downsizing_spinoffs": hx.Float(
            mode="output",
            view={"label": "Layoffs/Downsizing/Spin-offs", "format": percent_format(0)},
        ),
        "ownership_control": hx.Float(
            mode="output",
            view={"label": "Ownership/Control", "format": percent_format(0)},
        ),
    }


def admitted_schedule_function_max():
    return {
        "prior_claim_activity": hx.Float(
            mode="output",
            view={"label": "Prior Claim Activity", "format": percent_format(0)},
        ),
        "financial_strength": hx.Float(
            mode="output",
            view={"label": "Financial Strength", "format": percent_format(0)},
        ),
        "mergers_and_acquisitions": hx.Float(
            mode="output",
            view={"label": "Mergers and Acquisitions", "format": percent_format(0)},
        ),
        "quality_of_board": hx.Float(
            mode="output",
            view={"label": "Quality of Board", "format": percent_format(0)},
        ),
        "length_of_time_in_business": hx.Float(
            mode="output",
            view={"label": "Length of Time in Business", "format": percent_format(0)},
        ),
        "size_of_revenues_assets_employees": hx.Float(
            mode="output",
            view={
                "label": "Size - Revenues/Assets/Employees",
                "format": percent_format(0),
            },
        ),
        "layoffs_downsizing_spinoffs": hx.Float(
            mode="output",
            view={"label": "Layoffs/Downsizing/Spin-offs", "format": percent_format(0)},
        ),
        "ownership_control": hx.Float(
            mode="output",
            view={"label": "Ownership/Control", "format": percent_format(0)},
        ),
    }


def simple_factor_selection():
    return {
        "factor_selection": hx.Float(
            mode="input",
            default=1,
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
    
def table_a_b():
    return {
        "table_a": hx.Str(view={"label": "Table A"}, mode="output"),
        "table_b": hx.Str(view={"label": "Table B"}, mode="output")
    }

def options():
    options_to_use = [1, 2, 3, 4, 5]
    return {
        f"option_{option}": hx.Structure(
            children={**table_a_b()}            
        )
        for option in options_to_use
    }                        

def sch_usml_pcl_inputs(cds):

    cds.extend_node_rater_defined(
        "cds/exposure/granular",
        {         

            "pcl": hx.Structure(
            view={"label": "Fiduciary"},
            children={
            # Total Admitted Modifier
            "base_rate": hx.Structure(
                view={"label": "Base Rate"},
                children={
                    # Asset Size
                    "asset_size": hx.Float(
                        mode="input",
                        default=None,
                        optionality="optional",
                        view={
                            "label": "Asset Size",
                            "format": {"thousandSeparated": True, "mantissa": 0},
                        },
                        async_input=["rarc_task"],
                    ),
                    # Revenue
                    "revenue": hx.Float(
                        mode="input",
                        default=None,
                        optionality="optional",
                        view={
                            "label": "Revenue",
                            "format": {"thousandSeparated": True, "mantissa": 0},
                        },
                        async_input=["rarc_task"],
                    ),
            }),

            # Class of Business
            "class_of_business": hx.Str(
                mode="output", view={"label": "Class of Business"}
            ),
             "class_of_business_table": hx.Structure(                
                 children={
                    **options()                 
                 }
            )
                       
            })
    }),

    cds.extend_node_rater_defined(
        "cds",
        {
            "rating_factors": hx.Structure(
            view={"label": "Fiduciary"},
            children={
            # Total Admitted Modifier
            
            "pcl": hx.Structure(
            view={"label": "Fiduciary"},
            children={
            # Total Admitted Modifier

            "base_rate": hx.Structure(
                view={"label": "Base Rate"},
                children={
                    # Admitted Minimum Premium
                    "admitted_minimum_premium": hx.Float(
                        mode="output",
                        view={
                            "label": "Admitted Minimum Premium",
                            "format": {"thousandSeparated": True, "mantissa": 0},
                        },
                    ),
                    # Admitted Minimum Limit
                    "admitted_minimum_limit": hx.Float(
                        mode="output",
                        view={
                            "label": "Admitted Minimum Limit",
                            "format": {"thousandSeparated": True, "mantissa": 0},
                            }
                            ),
                })
            })
            })
        }), 
   

    cds.extend_node_rater_defined(
    "cds/layers/coverages/pcl",
    {
        
        "quote_grid": hx.Structure(
            view={"label": "Quote Grid"},
            children={
                "qg_options": hx.List(
                    mode="input",
                    default_element_count=1,
                    children={
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
                        # Limit/Retention Factor
                        "limit_retention": hx.Float(
                            mode="output",
                            view={
                                "label": "Limit/Retention Factor",
                                "format": {
                                    "thousandSeparated": True,
                                    "mantissa": 2,
                                },
                            },
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
                        # Internal Benchmark
                        "internal_benchmark": hx.Float(
                            mode="output",
                            view={
                                "label": "Internal Benchmark",
                                "format": {
                                    "thousandSeparated": True,
                                    "mantissa": 0,
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
                        # BPI%
                        "bpi": hx.Float(
                            mode="output",
                            view={
                                "label": "BPI%",
                                "format": {"output": "percent", "mantissa": 2},
                            },
                        ),
                        # Select Option?
                        "option_selected": hx.Bool(
                            mode="input",
                            default=True,
                            view={"label": "Select Option?"},
                        ),
                    },
                )}
                )
                
    })

def running_prem_summary_childern():
    return{
        "modifier": hx.Float(mode="output", view={"label": "Modifier", "format": {"thousandSeparated": True, "mantissa": 2}}),
        "prem": hx.Float(mode="output", view={"label": "Running Premium", "format": {"thousandSeparated": True, "mantissa": 2}}),
    }

def sch_running_prem_summary_pcl(cds):
    cds.extend_node_rater_defined("cds/layers/coverages/pcl", {
        "running_prem_sum": hx.Structure(children={
            "base_rate": hx.Structure(view={"label": "Base Premium"}, children={**running_prem_summary_childern()}),
            "combined_retention_and_limit_adj": hx.Structure(view={"label": "Combined Retention and Limit Adjustment"}, children={**running_prem_summary_childern()}),
            "risk_char_adj": hx.Structure(view={"label": "Risk Characteristics Adjustment"}, children={**running_prem_summary_childern()}),
            "cob_adj": hx.Structure(view={"label": "COB Adjustment"}, children={**running_prem_summary_childern()}),            
            "punitive_damages_adj": hx.Structure(view={"label": "Punitive Damages Adjustment"}, children={**running_prem_summary_childern()}),
            "state_adj": hx.Structure(view={"label": "State Adjustment"}, children={**running_prem_summary_childern()}),
            "surp_dev_adj": hx.Structure(view={"label": "Surplus Deviation Adjustment"}, children={**running_prem_summary_childern()}),

        })  
    })