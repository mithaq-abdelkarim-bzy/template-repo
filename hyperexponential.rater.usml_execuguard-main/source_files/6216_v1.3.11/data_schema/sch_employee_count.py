import hx_data_schema as hx

from data_schema.sch_utilities import thousands_format


def employee_types():
    return {
        "fte": hx.Int(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Full-Time Employees"},
            async_input=["rarc_task"],
        ),
        "pte": hx.Int(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Part-Time Employees"},
            async_input=["rarc_task"],
        ),
    }


def risk_factor():
    return {
        "risk_factor": hx.Str(mode="input", default="", view={"label": "Risk Factor"}),
    }


def head_count():
    return {
        "head_count": hx.Int(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Head Count"},
            async_input=["rarc_task"],
        ),
    }


def ftes_weighted_risk():
    return{
        "ftes": hx.Float(mode='output', view={"label": "FTEs", "format": thousands_format(1)}),
        "weighted_risk": hx.Float(mode='output', view={"label": "Weighted Risk", "format": thousands_format(2)}),
    }


def sch_employee_count(cds): 
    cds.extend_node_rater_defined("cds",{
        "us_states":hx.Structure(view={"label": "States"}, children={
            "Alabama": hx.Structure(view={"label": "Alabama"}, children={
                    "fte": hx.Int(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Full-Time Employees"},
            async_input=["rarc_task"],
        ),
        "pte": hx.Int(
            mode="input",
            default=None,
            optionality="optional",
            view={"label": "Part-Time Employees"},
            async_input=["rarc_task"],
        ),        
            }),
            "Alaska": hx.Structure(view={"label": "Alaska"}, children={
                            **employee_types()          
                        }),
            "Arizona": hx.Structure(view={"label": "Arizona"}, children={
                            **employee_types()          
                        }),
            "Arkansas": hx.Structure(view={"label": "Arkansas"}, children={
                            **employee_types()          
                        }),
            "California": hx.Structure(view={"label": "California"}, children={
                            **employee_types()          
                        }),
            "Colorado": hx.Structure(view={"label": "Colorado"}, children={
                            **employee_types()          
                        }),
            "Connecticut": hx.Structure(view={"label": "Connecticut"}, children={
                            **employee_types()          
                        }),
            "Delaware": hx.Structure(view={"label": "Delaware"}, children={
                            **employee_types()          
                        }),
            "District_of_Columbia": hx.Structure(view={"label": "District of Columbia"}, children={
                            **employee_types()          
                        }),
            "Florida": hx.Structure(view={"label": "Florida"}, children={
                            **employee_types()          
                        }),
            "Georgia": hx.Structure(view={"label": "Georgia"}, children={
                            **employee_types()          
                        }),
            "Hawaii": hx.Structure(view={"label": "Hawaii"}, children={
                            **employee_types()          
                        }),
            "Idaho": hx.Structure(view={"label": "Idaho"}, children={
                            **employee_types()          
                        }),
            "Illinois": hx.Structure(view={"label": "Illinois"}, children={
                            **employee_types()          
                        }),
            "Indiana": hx.Structure(view={"label": "Indiana"}, children={
                            **employee_types()          
                        }),
            "Iowa": hx.Structure(view={"label": "Iowa"}, children={
                            **employee_types()          
                        }),
            "Kansas": hx.Structure(view={"label": "Kansas"}, children={
                            **employee_types()          
                        }),
            "Kentucky": hx.Structure(view={"label": "Kentucky"}, children={
                            **employee_types()          
                        }),
            "Louisiana": hx.Structure(view={"label": "Louisiana"}, children={
                            **employee_types()          
                        }),
            "Maine": hx.Structure(view={"label": "Maine"}, children={
                            **employee_types()
                        }),
            "Maryland": hx.Structure(view={"label": "Maryland"}, children={
                            **employee_types()          
                        }),
            "Massachusetts": hx.Structure(view={"label": "Massachusetts"}, children={
                            **employee_types()          
                        }),
            "Michigan": hx.Structure(view={"label": "Michigan"}, children={
                            **employee_types()          
                        }),
            "Minnesota": hx.Structure(view={"label": "Minnesota"}, children={
                            **employee_types()          
                        }),
            "Mississippi": hx.Structure(view={"label": "Mississippi"}, children={
                            **employee_types()          
                        }),
            "Missouri": hx.Structure(view={"label": "Missouri"}, children={
                            **employee_types()          
                        }),
            "Montana": hx.Structure(view={"label": "Montana"}, children={
                            **employee_types()          
                        }),
            "Nebraska": hx.Structure(view={"label": "Nebraska"}, children={
                            **employee_types()          
                        }),
            "Nevada": hx.Structure(view={"label": "Nevada"}, children={
                            **employee_types()          
                        }),
            "New_Hampshire": hx.Structure(view={"label": "New Hampshire"}, children={
                            **employee_types()          
                        }),
            "New_Jersey": hx.Structure(view={"label": "New Jersey"}, children={
                            **employee_types()          
                        }),
            "New_Mexico": hx.Structure(view={"label": "New Mexico"}, children={
                            **employee_types()          
                        }),                       
            "New_York_metro": hx.Structure(view={"label": "New York - metro"}, children={
                            **employee_types()          
                        }),
            "New_York_non_metro": hx.Structure(view={"label": "New York - non-metro"}, children={
                            **employee_types()          
                        }),
            "North_Carolina": hx.Structure(view={"label": "North Carolina"}, children={
                            **employee_types()          
                        }),
            "North_Dakota": hx.Structure(view={"label": "North Dakota"}, children={
                            **employee_types()          
                        }),
            "Ohio": hx.Structure(view={"label": "Ohio"}, children={
                            **employee_types()          
                        }),
            "Oklahoma": hx.Structure(view={"label": "Oklahoma"}, children={
                            **employee_types()          
                        }),
            "Oregon": hx.Structure(view={"label": "Oregon"}, children={
                            **employee_types()          
                        }),
            "Pennsylvania": hx.Structure(view={"label": "Pennsylvania"}, children={
                            **employee_types()          
                        }),
            "Rhode_Island": hx.Structure(view={"label": "Rhode Island"}, children={
                            **employee_types()          
                        }),
            "South_Carolina": hx.Structure(view={"label": "South Carolina"}, children={
                            **employee_types()          
                        }),
            "South_Dakota": hx.Structure(view={"label": "South Dakota"}, children={
                            **employee_types()          
                        }),
            "Tennessee": hx.Structure(view={"label": "Tennessee"}, children={
                            **employee_types()          
                        }),
            "Texas": hx.Structure(view={"label": "Texas"}, children={
                            **employee_types()          
                        }),
            "Utah": hx.Structure(view={"label": "Utah"}, children={
                            **employee_types()          
                        }),
            "Vermont": hx.Structure(view={"label": "Vermont"}, children={
                            **employee_types()          
                        }),
            "Virginia": hx.Structure(view={"label": "Virginia"}, children={
                            **employee_types()          
                        }),
            "Washington": hx.Structure(view={"label": "Washington"}, children={
                            **employee_types()          
                        }),
            "West_Virginia": hx.Structure(view={"label": "West Virginia"}, children={
                            **employee_types()          
                        }),
            "Wisconsin": hx.Structure(view={"label": "Wisconsin"}, children={
                            **employee_types()          
                        }),
            "Wyoming": hx.Structure(view={"label": "Wyoming"}, children={
                            **employee_types()          
                        }),           
            "Total": hx.Structure(view={"label": "Total"}, children={
                            "fte": hx.Int(
                                mode="output",                                
                                view={"label": "Full-Time Employees"},
                                async_input=["rarc_task"],
                            ),
                            "pte": hx.Int(
                                mode="output",                                
                                view={"label": "Part-Time Employees"},
                                async_input=["rarc_task"],
                            )          
                        })
        }),

        "split":hx.Structure(view={"label": "Regions"}, children={
            "seasonal": hx.Structure(view={"label": "Seasonal Employees"}, children={
                **head_count()
            }),
            "independent_contractors": hx.Structure(view={"label": "Independent Contractors"}, children={
                   **head_count()
            }),
            "temporary": hx.Structure(view={"label": "Temporary Employees"}, children={
                   **head_count()
            }),
            "foreign": hx.Structure(view={"label": "Foreign Employees"}, children={
                   **head_count()
            }),
        }),
        "weights":hx.Structure(view={"label": "Regions"}, children={
            "high": hx.Structure(view={"label": "High"}, children={
                **ftes_weighted_risk()
            }),
            "above_average": hx.Structure(view={"label": "Above Average"}, children={
                **ftes_weighted_risk()
            }),
            "moderate": hx.Structure(view={"label": "Moderate"}, children={
                **ftes_weighted_risk()
            }),
            "average": hx.Structure(view={"label": "Average"}, children={
                **ftes_weighted_risk()
            }),
            "below_average": hx.Structure(view={"label": "Below Average"}, children={
                **ftes_weighted_risk()
            }),
        
        }),
        "total_ftes": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Total FTEs", "format": thousands_format(1)}),
        "total_state_factor": hx.Float(mode="output", view={"label": "Total State Factor", "format": thousands_format(2)}),
        "comments": hx.Str(mode="input", default="", view={"label": "Comments"}),
    
     })
