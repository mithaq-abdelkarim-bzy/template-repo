import hx_data_schema as hx

from data_schema.sch_utilities import percent_format
from data_schema.sch_helper_functions import modifiers_selection, modifiers_factor_selection, factor_selection, coinsurance, modifiers_selection_inputs

def admitted_schedule():
    builder = {"rationale": {}, "factor_selection": {}, "min": {}, "max": {}, "out_of_range": {}}

    fields = {
        ("prior_claim_activity", "Prior Claim Activity"),
        ("turnover_rate", "Turnover Rate"),
        ("financial_strength", "Financial Strength"),
        ("hr_policies", "HR Policies"),
        ("demographic_metro", "Demographics/Metro"),
        ("management", "Management"),
        ("internal_controls", "Internal Controls"),
        ("cooperation", "Cooperation"),
        ("experience", "Experience"),
        ("staffing_turnover", "Staffing Turnover"),
        ("salary_structure", "Salary Structure"),
        ("stability", "Stability")
    }

    # Populate all fields
    for fid, label in fields:
        builder["rationale"][fid] = hx.Str(mode="input", default=None, optionality="optional", view={"label": label})
        builder["factor_selection"][fid] = hx.Float(mode="input", default=None, optionality="optional", view={"label": label, "format": {"output": "percent", "mantissa": 1}})
        builder["min"][fid] = hx.Float(mode="output", view={"label": label, "format": {"output": "percent", "mantissa": 0}})
        builder["max"][fid] = hx.Float(mode="output", view={"label": label, "format": {"output": "percent", "mantissa": 0}})
        builder["out_of_range"][fid] = hx.Str(mode="output", view={"label": label})

    # Add Total Schedule Rating Modifier Field
    builder["factor_selection"]["tot_sch_rat"] = hx.Float(mode="output", view={"label": "Total Schedule Rating Modifier", "format": {"output": "percent", "mantissa": 0}})
    builder["min"]["tot_sch_rat"] = hx.Float(mode="output", view={"label": "Total Schedule Rating Modifier", "format": {"output": "percent", "mantissa": 0}})
    builder["max"]["tot_sch_rat"] = hx.Float(mode="output", view={"label": "Total Schedule Rating Modifier", "format": {"output": "percent", "mantissa": 0}})
    builder["out_of_range"]["tot_sch_rat"] = hx.Str(mode="input", default="", view={"label": "Total Schedule Rating Modifier"})

    # Transform into HX structure
    return {
        'rationale': hx.Structure(view={'label': 'Rationale'}, children=builder['rationale']),
        'factor_selection': hx.Structure(view={'label': 'Factor Selection'}, children=builder['factor_selection']),
        'min': hx.Structure(view={'label': 'Min'}, children=builder['min']),
        'max': hx.Structure(view={'label': 'Max'}, children=builder['max']),
        'out_of_range': hx.Structure(view={'label': 'Out of range'}, children=builder['out_of_range'])
    }

def sch_modifiers(cds):
    #a data schema which combines the modifier values for epl and pcl into one schema branch
    cds.extend_node_rater_defined(
        "cds",
        {
            "modifiers": hx.Structure(
            view={"label": "Fiduciary"},
            children={
            # Total Admitted Modifier

                "epl": hx.Structure(
                view={"label": "Fiduciary"},
                children={
                # Total Admitted Modifier


                    # Admitted Modifiers table
                    "admitted_modifiers": hx.Structure(
                        view={"label": "Admitted Modifiers"},
                        children={
                            "reactive_admitted_modifiers": hx.Structure(
                                children={
                                    "reactive_admitted_modifiers_dropdown": hx.List(
                                        mode="output",
                                        children={"dropdown_item": hx.Str(mode="output")},
                                    ),
                                    "risk_characteristics": hx.Structure(
                                        view={"label": "Risk Characteristics"},
                                        children={
                                            "description": hx.Str(
                                                mode="override",
                                                optionality="optional",
                                                options_field="dropdown_item",
                                                options_data="../../reactive_admitted_modifiers_dropdown",                                                
                                                view={"label": "Description"},
                                            ),
                                            **factor_selection(),
                                        },
                                    ),
                                }
                            ),
                            "financial_stability": hx.Structure(
                                view={"label": "Financial Stability"},
                                children={
                                    "description": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_column="Response",
                                        options_table="table_financial_stability",
                                        default="Average",
                                        view={"label": "Description"},
                                    ),
                                    **factor_selection(),
                                },
                            ),
                            "loss_prevention_and_mitigation": hx.Structure(
                                view={"label": "Loss Prevention and Mitigation"},
                                children={
                                    "description": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_column="Response",
                                        options_table="table_loss_prevention",
                                        default="Average",
                                        view={"label": "Description"},
                                    ),
                                    **factor_selection(),
                                },
                            ),
                            "employment_policies": hx.Structure(
                                view={"label": "Employment Policies"},
                                children={
                                    "description": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_column="Response",
                                        options_table="table_employment_policies",
                                        default="Average",
                                        view={"label": "Description"},
                                    ),
                                    **factor_selection(),
                                },
                            ),
                            "reactive_cob": hx.Structure(
                                children={
                                    "reactive_cob_dropdown": hx.List(
                                        mode="output",
                                        children={"dropdown": hx.Str(mode="output")},
                                    ),
                                    "class_of_business": hx.Structure(
                                        view={"label": "Class of Business"},
                                        children={
                                            "description": hx.Str(
                                                mode="override",
                                                optionality="optional",
                                                options_column="Table",
                                                options_table="table_epl_cob",
                                                view={"label": "Description"},
                                            ),
                                            "min": hx.Float(
                                                mode="output",
                                                view={
                                                    "label": "Min",
                                                    "format": {
                                                        "output": "percent",
                                                        "mantissa": 0,
                                                    },
                                                },
                                            ),
                                            "max": hx.Float(
                                                mode="output",
                                                view={
                                                    "label": "Max",
                                                    "format": {
                                                        "output": "percent",
                                                        "mantissa": 0,
                                                    },
                                                },
                                            ),
                                        },
                                    ),
                                }
                            ),
                            #####VLOOKUP FORMULAE GOES IN HERE#####
                            "sug_class_business": hx.Structure(
                                view={"label": "Suggested Class of Business"},
                                children={
                                    "description": hx.Str(
                                        mode="output", view={"label": "Description"}
                                    )
                                },
                            ),
                            "unionized_employees": hx.Structure(
                                view={"label": "*Number of Unionized Employees"},
                                children={
                                    "description": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_column="Response",
                                        options_table="table_unionized_employee",
                                        default="0-19%",
                                        view={"label": "Description"},
                                    ),
                                    "min": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Min",
                                            "format": {"output": "percent", "mantissa": 0},
                                        },
                                    ),
                                    "max": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Max",
                                            "format": {"output": "percent", "mantissa": 0},
                                        },
                                    ),
                                },
                            ),
                            "stock_option_exposure": hx.Structure(
                                view={"label": "Stock Option Exposure"},
                                children={
                                    "description": hx.Str(
                                        mode="input",
                                        optionality="optional",
                                        options_column="Response",
                                        options_table="table_stock_option_exp",
                                        default="Minimal/Non-Existent",
                                        view={"label": "Description"}),
                                    "min": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Min",
                                            "format": {"output": "percent", "mantissa": 0},
                                        },
                                    ),
                                    "max": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Max",
                                            "format": {"output": "percent", "mantissa": 0},
                                        },
                                    )})
                        }),
                    
                        # Will split retentions be offered?
                        "bnch_split_retention_offered": hx.Bool(
                            mode="input",
                            default=False,
                            view={"label": "Will split retentions be offered?"},
                        ),

                        "endorsements": hx.Structure(
                            view={"label": "Endorsements"},children={                    
                            "selection": hx.Structure(view={"label": "Selection"},  children={
                                "punitive_damages": hx.Str( mode="input", optionality="optional", options_column="Response", options_table="table_epl_punitive_damages",
                                    default_index=1, view={"label": "Punitive Damages",
                                        "options":{
                                            "mandatory":{"style_cell":"hx-bad"}}
                                    }),
                                "reactive_third_party_liab": hx.Structure( children={
                                    "reactive_third_party_liab_dropdown": hx.List(
                                        mode="output",
                                        children={"dropdown_item": hx.Str(mode="output")},
                                    ),
                                    "third_party_liability":
                                   
                                                hx.Str(
                                                mode="input",
                                                optionality="optional",
                                                options_field="dropdown_item",                                                
                                                options_data="../reactive_third_party_liab_dropdown",
                                                default="Included",
                                                view={"label": "Third Party Liability"},
                                            )
                                           
                                }),
                                 "reactive_wage_and_hour": hx.Structure( children={
                                    "reactive_wage_and_hour_dropdown": hx.List(
                                        mode="output",
                                        children={"dropdown_item": hx.Str(mode="output")},
                                    ),
                                    "wage_and_hour":                            
                                                hx.Str(
                                                mode="input",
                                                optionality="optional",
                                                options_field="dropdown_item",                                        
                                                options_data="../reactive_wage_and_hour_dropdown",
                                                default="Not Purchased",
                                                view={"label": "Wage and Hour Selection"},
                                            )
                                            
                                }),
                               
                                "client_coverage": hx.Str(mode="input",optionality="optional",options_column="Response",options_table="table_client_coverage",
                                    default="Not Purchased",view={"label": "Client Coverage Selection"}),
                                "ahern": hx.Str(mode="input",optionality="optional",options_column="Response",options_table="table_ahern_ca",
                                    default="Not Purchased",view={"label": "Ahern/Partnership Agreement Selection"}),
                                "partnership_defense": hx.Str(mode="input",optionality="optional",options_column="Response",options_table="table_partnership_def_cost",
                                    default="Not Purchased",view={"label": "Partnership Agreement Defense Costs Selection"}),
                                "leaders_preferred": hx.Str(mode="input",optionality="optional",
                                    default="Not Purchased",view={"label": "Leadership Preffered Selection"}),
                            }),
                            "factor_selection": hx.Structure(view={"label": "Factor Selection"},  children={
                                 "punitive_damages": hx.Float( mode="override", optionality="optional", 
                                    view={"label": "Punitive Damages",
                                    "options":{
                                                "mandatory":{"style_cell":"hx-bad"}},
                                    "format": {"output": "percent", "mantissa": 0}}),
                                'reactive_third_party_liab': hx.Structure(children={
                                "third_party_liability": hx.Float( mode="override", optionality="optional", view={"label": "Third Party Liability","format": {"output": "percent", "mantissa": 0}}),
                            })
                            }),
                            'min': hx.Structure(view={"label": "Min"},  children={
                                "punitive_damages": hx.Float( mode="output", 
                                    view={"label": "Punitive Damages",
                                    "options":{
                                                "mandatory":{"style_cell":"hx-bad"}},
                                "format": {"output": "percent", "mantissa": 0}}),   
                                'reactive_third_party_liab': hx.Structure(children={
                                "third_party_liability": hx.Float( mode="output", view={"label": "Third Party Liability","format": {"output": "percent", "mantissa": 0}})
                                }),
                                'reactive_wage_and_hour': hx.Structure(children={
                                "wage_and_hour": hx.Float(mode="output", view={"label": "Wage and Hour Selection","format": {"output": "percent", "mantissa": 0}}),
                                }),
                                "client_coverage": hx.Float(mode="output", view={"label": "Client Coverage Selection","format": {"output": "percent", "mantissa": 0}}),

                            }),
                            'max': hx.Structure(view={"label": "Max"},  children={
                               "punitive_damages": hx.Float(mode="output", 
                                    view={"label": "Punitive Damages",
                                    "options":{
                                                "mandatory":{"style_cell":"hx-bad"}},
                                "format": {"output": "percent", "mantissa": 0}}),    
                                'reactive_third_party_liab': hx.Structure(children={
                                "third_party_liability": hx.Float(mode="output", view={"label": "Third Party Liability","format": {"output": "percent", "mantissa": 0}})
                                }),
                                'reactive_wage_and_hour': hx.Structure(children={
                                "wage_and_hour": hx.Float(mode="output", view={"label": "Wage and Hour Selection","format": {"output": "percent", "mantissa": 0}}),
                                }),
                                "client_coverage": hx.Float(mode="output", view={"label": "Client Coverage Selection","format": {"output": "percent", "mantissa": 0}}),
                            }),
                            }),
                
                    # Coinsurance table
                    "coinsurance": hx.Structure(
                        view={"label": "Coinsurance"}, children={**coinsurance()}
                    ),
                    "per_self_ins": hx.Structure(
                        view={"label": "Percent Self Insured"}, children={**coinsurance()}
                    ),
                    # Total Admitted Modifier
                    "total_admitted_modifier": hx.Float(
                        mode="output", view={"label": "Total Admitted Modifier"}
                    ),
                    # Admitted Schedule Rating
                    "admitted_schedule_rating": hx.Structure(view={"label": "Admitted Schedule Rating"}, children=admitted_schedule()),
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
                            "factor_selection": hx.Float(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={
                                    "label": "Factor Selection",
                                    "format": {"output": "percent", "mantissa": 1},
                                },
                            ),
                            "min": hx.Float(
                                mode="output",                       
                                view={
                                    "label": "Min",
                                    "format": {"output": "percent", "mantissa": 0},
                                },
                            ),
                            "max": hx.Float(
                                mode="output",                        
                                view={
                                    "label": "Max",
                                    "format": {"output": "percent", "mantissa": 0},
                                },
                            ),
                            "out_of_range": hx.Str(
                                mode="output", view={"label": "Out of Range"}
                            ),
                        },
                    ),
                    # Surplus Deviation
                    "surplus_deviation": hx.Float(
                        mode="input",
                        default=None,
                        optionality="optional",
                        view={
                            "label": "Surplus Deviation",
                            "format": {"output": "percent", "mantissa": 0},
                        },
                    ),
                    # Benchmark UW Modifiers
                    "benchmark_uw_modifiers": hx.Structure(
                        view={"label": "Benchmark UW Modifiers"},
                        children={
                            "bnch_risk_characteristics": hx.Structure(
                                view={"label": "Risk Characteristics"},
                                children={
                                    "factor_selection": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Factor Selection",
                                            "format": {"output": "percent", "mantissa": 1},
                                        },
                                    ),
                                    "min": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Min",
                                            "format": {"output": "percent", "mantissa": 0},
                                        },
                                    ),
                                    "max": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Max",
                                            "format": {"output": "percent", "mantissa": 0},
                                        },
                                    ),
                                },
                            ),
                            "bnch_pro_claim_activity": hx.Structure(
                                view={"label": "Prior Claim Activity"},
                                children={
                                    "factor_selection": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Factor Selection",
                                            "format": {"output": "percent", "mantissa": 1},
                                        },
                                    ),
                                    "min": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Min",
                                            "format": {"output": "percent", "mantissa": 0},
                                        },
                                    ),
                                    "max": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Max",
                                            "format": {"output": "percent", "mantissa": 0},
                                        },
                                    ),
                                },
                            ),
                            "bnch_hr_policies": hx.Structure(
                                view={"label": "HR Policies"},
                                children={
                                    "factor_selection": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Factor Selection",
                                            "format": {"output": "percent", "mantissa": 1},
                                        },
                                    ),
                                    "min": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Min",
                                            "format": {"output": "percent", "mantissa": 0},
                                        },
                                    ),
                                    "max": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Max",
                                            "format": {"output": "percent", "mantissa": 0},
                                        },
                                    ),
                                },
                            ),
                            "bnch_turnover_ma_layoffs": hx.Structure(
                                view={"label": "Turnover, M&A Activity, Layoffs"},
                                children={
                                    "factor_selection": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Factor Selection",
                                            "format": {"output": "percent", "mantissa": 1},
                                        },
                                    ),
                                    "min": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Min",
                                            "format": {"output": "percent", "mantissa": 0},
                                        },
                                    ),
                                    "max": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Max",
                                            "format": {"output": "percent", "mantissa": 0},
                                        },
                                    ),
                                },
                            ),
                            "bnch_financial_strength": hx.Structure(
                                view={"label": "Financial Strength"},
                                children={
                                    "factor_selection": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Factor Selection",
                                            "format": {"output": "percent", "mantissa": 1},
                                        },
                                    ),
                                    "min": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Min",
                                            "format": {"output": "percent", "mantissa": 0},
                                        },
                                    ),
                                    "max": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Max",
                                            "format": {"output": "percent", "mantissa": 0},
                                        },
                                    ),
                                },
                            ),
                            "bnch_demographic": hx.Structure(
                                view={"label": "Demographic"},
                                children={
                                    "factor_selection": hx.Float(
                                        mode="input",
                                        default=None,
                                        optionality="optional",
                                        view={
                                            "label": "Factor Selection",
                                            "format": {"output": "percent", "mantissa": 1},
                                        },
                                    ),
                                    "min": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Min",
                                            "format": {"output": "percent", "mantissa": 0},
                                        },
                                    ),
                                    "max": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Max",
                                            "format": {"output": "percent", "mantissa": 0},
                                        },
                                    ),
                                },
                            ),
                        }),
            }),
            "pcl": hx.Structure(
            view={"label": "Fiduciary"},
            children={
            # Financial Condition
                "modifiers_table": hx.Structure(
                    view={"label": "Modifiers"},
                    children={
                        "financial_condition": hx.Structure(
                            view={"label": "Financial Condition"},
                            children={
                                "description": hx.Str(
                                    mode="input",
                                    default="Average",
                                    optionality="optional",
                                    options=["Above Average", "Average", "Below Average"],
                                    view={"label": "Description"},
                                ),
                                **modifiers_selection(),
                                **modifiers_factor_selection(),
                            },
                        ),
                        # Merger & Acquisition Activity
                        "mergers_and_acquisition_activity": hx.Structure(
                            view={"label": "Merger & Acquisition Activity"},
                            children={
                                "description": hx.Str(
                                    mode="input",
                                    default="None",
                                    optionality="optional",
                                    options=["None", "Some", "Significant"],
                                    view={"label": "Description"},
                                ),
                                **modifiers_selection(),
                                **modifiers_factor_selection(),
                            },
                        ),
                        # Ownership
                        "ownership": hx.Structure(
                            view={"label": "Ownership"},
                            children={
                                "description": hx.Str(
                                    mode="input",
                                    default=">50 shareholders",
                                    optionality="optional",
                                    options=[
                                        "<10 shareholders",
                                        "11-25 shareholders",
                                        "25-50 shareholders",
                                        ">50 shareholders",
                                        "Major shareholder/family exclusion",
                                    ],
                                    view={"label": "Description"},
                                ),
                                **modifiers_selection(),
                                **modifiers_factor_selection(),
                            },
                        ),
                        # Length of Time in Busniess
                        "length_of_time_in_business": hx.Structure(
                            view={"label": "Length of Time in Busniess"},
                            children={
                                "description": hx.Str(
                                    mode="input",
                                    default=">10 Years",
                                    optionality="optional",
                                    options=["<3 Years", "3-10 Years", ">10 Years"],
                                    view={"label": "Description"},
                                ),
                                **modifiers_selection(),
                                **modifiers_factor_selection(),
                            },
                        ),
                        # Layoffs, Downsizing or Spin-offs
                        "layoffs_downsizing_or_spinoffs": hx.Structure(
                            view={"label": "Layoffs, Downsizing or Spin-offs"},
                            children={
                                "description": hx.Str(
                                    mode="input",
                                    default="None in prior two years and none anticipated during the next year",
                                    optionality="optional",
                                    options=[
                                        "None in prior two years and none anticipated during the next year",
                                        "5% or more in prior two years or anticipated during the next year",
                                    ],
                                    view={"label": "Description"},
                                ),
                                **modifiers_selection(),
                            },
                        ),
                        # Profitability
                        "profitability": hx.Structure(
                            view={"label": "Profitability"},
                            children={
                                "description": hx.Str(
                                    mode="input",
                                    default="Average",
                                    optionality="optional",
                                    options=["Above Average", "Average", "Below Average"],
                                    view={"label": "Description"},
                                ),
                                **modifiers_selection(),
                            },
                        ),
                        # Quality of Management
                        "quality_of_management": hx.Structure(
                            view={"label": "Quality of Management"},
                            children={
                                "description": hx.Str(
                                    mode="input",
                                    default="Experienced Professional Team",
                                    optionality="optional",
                                    options=[
                                        "Experienced Professional Team",
                                        "Family Members/Limited Experience",
                                    ],
                                    view={"label": "Description"},
                                ),
                                **modifiers_selection(),
                            },
                        ),
                    # Litigation
                    "litigation": hx.Structure(
                        view={"label": "Litigation"},
                        children={
                            "description": hx.Str(
                                mode="input",
                                default="No D&O Claims",
                                optionality="optional",
                                options=[
                                    "No D&O Claims",
                                    "Insured involved in any litigation that could impact earnings or financial position",
                                ],
                                view={"label": "Description"},
                            ),
                            **modifiers_selection(),
                        },
                    ),
                    "reactive_removal_of_punitive_damages": hx.Structure( children={
                                    "reactive_removal_of_punitive_damages_dropdown": hx.List(
                                        mode="output",
                                        children={"dropdown_item": hx.Str(mode="output")},
                                    ),
                                    "removal_of_punitive_damages": hx.Structure(
                                        view={"label": "Removal of Punitive Damages"},
                                        children={
                                            "description": hx.Str(
                                                mode="input",
                                                optionality="optional",
                                                options_field="dropdown_item",                                        
                                                options_data="../../reactive_removal_of_punitive_damages_dropdown",
                                                default="No",
                                                view={"label": "Description"},
                                            ),
                                            **modifiers_selection(),
                                            
                                }),
                    }),
                },
            ), #closes modifier table
            # Class of Business
            "class_of_business": hx.Str(
                mode="output", view={"label": "Class of Business"}
            ),
            # Prior Claim Activity
            "bnch_prior_claim_activity_selection": hx.Structure(
                view={"label": "Prior Claim Activity"},
                children={
                    "factor_selection": hx.Float(
                        mode="input",
                        default=None,
                        optionality="optional",
                        view={
                            "label": "Factor Selection",
                            "group": "Non-Admitted",
                            "format": percent_format(0),
                        },
                    ),
                    "min": hx.Float(
                        mode="output",                       
                        view={
                            "label": "Min",
                            "group": "Non-Admitted",
                            "format": {"output": "percent", "mantissa": 0},
                        },
                    ),
                    "max": hx.Float(
                        mode="output",                        
                        view={
                            "label": "Max",
                            "group": "Non-Admitted",
                            "format": {"output": "percent", "mantissa": 0},
                        },
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
                mode="input",
                default=None,
                optionality="optional",
                view={
                    "label": "Surplus Deviation",
                    "format": {"output": "percent", "mantissa": 0},
                },
            ),
       
            "schedule_rating": hx.Structure(
                view={"label": "Admitted Schedule Rating"},
                children={
                    "table_cw": hx.Structure(
                        view={"label": "Table CW"},
                        children={
                            "prior_claim_activity": hx.Structure(
                                view={"label": "Prior Claim Activity"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "financial_strength": hx.Structure(
                                view={"label": "Financial Strength"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "mergers_and_acquisitions": hx.Structure(
                                view={"label": "Mergers and Acquisition"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "quality_of_board": hx.Structure(
                                view={"label": "Quality of Board"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "length_of_time_in_business": hx.Structure(
                                view={"label": "Length of Time in Business"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "size_of_revenues_assets_employees": hx.Structure(
                                view={"label": "Size - Revenues/Assets/Employees"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "layoffs_downsizing_spinoffs": hx.Structure(
                                view={"label": "Layoffs/Downsizing/Spin-offs"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "ownership_control": hx.Structure(
                                view={"label": "Ownership/Control"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "total_schedule_rating_modifier": hx.Structure(
                                view={"label": "Total Schedule Rating Modifier"},
                                children={
                                    "factor_selection": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Factor Selection",
                                            "format": percent_format(0),
                                        },
                                    ),
                                    "min": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Min",
                                            "format": {
                                                "output": "percent",
                                                "mantissa": 0,
                                            },
                                        },
                                    ),
                                    "max": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Max",
                                            "format": {
                                                "output": "percent",
                                                "mantissa": 0,
                                            },
                                        },
                                    ),
                                },
                            ),
                        },
                    ),
                    "table_ca": hx.Structure(
                        view={"label": "Table CA"},
                        children={
                            "classification_peculiarities": hx.Structure(
                                view={"label": "Classification Peculiarities"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "significant_transactional_event": hx.Structure(
                                view={"label": "Significant Transactional Event"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "regulatory_exposure": hx.Structure(
                                view={"label": "Regulatory Exposure"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "board_of_directors": hx.Structure(
                                view={"label": "Board of Directors"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "management_practices": hx.Structure(
                                view={"label": "Management Practices"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "experience": hx.Structure(
                                view={"label": "Experience"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "total_schedule_rating_modifier": hx.Structure(
                                view={"label": "Total Schedule Rating Modifier"},
                                children={
                                    "factor_selection": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Factor Selection",
                                            "format": percent_format(0),
                                        },
                                    ),
                                    "min": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Min",
                                            "format": {
                                                "output": "percent",
                                                "mantissa": 0,
                                            },
                                        },
                                    ),
                                    "max": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Max",
                                            "format": {
                                                "output": "percent",
                                                "mantissa": 0,
                                            },
                                        },
                                    ),
                                },
                            ),
                        },
                    ),
                    "table_la": hx.Structure(
                        view={"label": "Table LA"},
                        children={
                            "prior_claim_activity": hx.Structure(
                                view={"label": "Prior Claim Activity"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "financial_strength": hx.Structure(
                                view={"label": "Financial Strength"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "mergers_and_acquisitions": hx.Structure(
                                view={"label": "Mergers and Acquisitions"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "quality_of_board": hx.Structure(
                                view={"label": "Quality of Board"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "length_of_time_in_business": hx.Structure(
                                view={"label": "Length of Time in Business"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "size_of_revenues_assets_employees": hx.Structure(
                                view={"label": "Size - Revenues/Assets/Employees"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "layoffs_downsizing_spinoffs": hx.Structure(
                                view={"label": "Layoffs/Downsizing/Spin-offs"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "total_schedule_rating_modifier": hx.Structure(
                                view={"label": "Total Schedule Rating Modifier"},
                                children={
                                    "factor_selection": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Factor Selection",
                                            "format": percent_format(0),
                                        },
                                    ),
                                    "min": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Min",
                                            "format": {
                                                "output": "percent",
                                                "mantissa": 0,
                                            },
                                        },
                                    ),
                                    "max": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Max",
                                            "format": {
                                                "output": "percent",
                                                "mantissa": 0,
                                            },
                                        },
                                    ),
                                },
                            ),
                        },
                    ),
                    "table_mo": hx.Structure(
                        view={"label": "Table MO"},
                        children={
                            "prior_claim_activity": hx.Structure(
                                view={"label": "Prior Claim Activity"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "cash_position_stability": hx.Structure(
                                view={"label": "Cash Position/Stability"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "diversification_strategy": hx.Structure(
                                view={"label": "Diversification Strategy"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "board_shareholders": hx.Structure(
                                view={"label": "Board / Shareholders"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "size_of_revenues_assets_employees": hx.Structure(
                                view={"label": "Size - Revenues/Assets/Employees"},
                                children={**modifiers_selection_inputs()},
                            ),
                            "total_schedule_rating_modifier": hx.Structure(
                                view={"label": "Total Schedule Rating Modifier"},
                                children={
                                    "factor_selection": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Factor Selection",
                                            "format": percent_format(0),
                                        },
                                    ),
                                    "min": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Min",
                                            "format": {
                                                "output": "percent",
                                                "mantissa": 0,
                                            },
                                        },
                                    ),
                                    "max": hx.Float(
                                        mode="output",
                                        view={
                                            "label": "Max",
                                            "format": {
                                                "output": "percent",
                                                "mantissa": 0,
                                            },
                                        },
                                    ),
                                },
                            ),
                        },
                    ),
                },
            ),
            })

        })
    })    