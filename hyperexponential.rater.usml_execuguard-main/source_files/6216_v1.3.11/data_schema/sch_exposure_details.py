import hx_data_schema as hx

from algorithms.json_parameter_files.parameters import get_parameters
from data_schema.sch_utilities import percent_format, thousands_format

included = get_parameters("included.json")


def sch_exposure_details_non_cds():
    return {
        "coverage_elections": hx.Structure(
            view={"label": "Coverage Elections"},
            children={             
                 "epl_pcl": hx.Bool(
                    mode="output",                    
                    view={"label": "epl_pcl"},
                ),
             
                "excess": hx.Bool(
                    mode="output",                   
                    view={"label": "Excess"},
                ),
            },
        ),
        "is_employee_count": hx.Bool(
            mode="output", view={"label": "Is Employee Count"}
        ),
        "is_epl_inputs": hx.Bool(mode="output", view={"label": "Is EPL Inputs"}),
        "is_pcl_inputs": hx.Bool(mode="output", view={"label": "Is PCL Inputs"}),
        "is_fid_inputs": hx.Bool(mode="output", view={"label": "Is FID Inputs"}),
        "premium_label": hx.Str(mode="output")   


    }


def quote_grid_summary():
    return {
        "limit": hx.Float(
            mode="output", async_input=["word_documents_task", "rarc_task"], view={"label": "Limit", "format": thousands_format(0)}
        ),
        "adl": hx.Float(
            mode="output", view={"label": "ADL", "format": thousands_format(0)}
        ),
        "retention": hx.Float(
            mode="output", async_input=["word_documents_task", "rarc_task"],  view={"label": "Retention", "format": thousands_format(0)}
        ),      
        "benchmark_premium": hx.Float(
            mode="output", async_input=["rarc_task"], view={"label": "Benchmark Premium", "format": thousands_format(0)}
        ),
        "pre_rounding_admitted_premium": hx.Float(
            mode="output", async_input=["rarc_task"], view={"label": "Pre-Rounding Premium", "format": thousands_format(0)}
        ),
        "selected_premium": hx.Float(
            mode="input", default=0, view={"label": "Selected Premium", "format": thousands_format(0)}
        ),
        "post_rounding_admitted_premium": hx.Float(
            mode="output", async_input = ["rarc_task"], view={"label": "Post Rounding Premium",  "format": thousands_format(0)}
        ),
        "final_term_premium": hx.Float(
            mode="output", view={"label": "Final Term Premium", "format": thousands_format(0)}, async_input=["rarc_task"]
        ),
        "bpi": hx.Float(mode="output", view={"label": "BPI%", "format": {"output": "percent", "mantissa": 2}}),
    }


def sch_exposure_details(cds):
    cds.extend_node_rater_defined(
        "cds",
        {
            "coverage_elections": hx.Structure(
                view={"label": "Coverage Elections"},
                children={
                    "epl": hx.Bool(
                        mode="input",
                        default=False,
                        optionality="required",
                        view={"label": "EPL"},
                        async_input=["rarc_task", "expiring_policy_fetch_task"]
                    ),
                    "fid": hx.Bool(
                        mode="input",
                        default=False,
                        optionality="required",
                        view={"label": "Fiduciary"},
                        async_input=["rarc_task", "expiring_policy_fetch_task"]
                    ),
                    "pcl": hx.Bool(
                        mode="input",
                        default=False,
                        optionality="required",
                        view={"label": "PCL"},
                        async_input=["rarc_task", "expiring_policy_fetch_task"]
                    )
            }),
            "state": hx.Str(
                mode="input",
                optionality="optional",
                options_column="State Name",
                options_table="table_state",
                default=None,
                view={"label": "State"},
                async_input=["rarc_task"]
            ),
            "reactive_zipcode": hx.Structure(
                children={
                    "reactive_zipcode_list": hx.List(
                        mode="output",
                        children={
                            "zipcode": hx.Str(mode="output")
                        },  # reactive zipcode list
                    ),
                    "zipcode": hx.Str(
                        mode="input",
                        optionality="optional",
                        options_field="zipcode",
                        options_data="../reactive_zipcode_list",
                        # options_table="table_zipcode",
                        default=None,
                        view={"label": "ZIP Code"},
                    ),
                },
            ),
            "is_cov_elections": hx.Bool(
                mode="input",
                default=True,
                optionality="required",
                view={"label": "Select Coverage Elections"},
            ),
            "county": hx.Str(mode="output", view={"label": "County"}),
            "brokerage": hx.Float(
                mode="input", optionality="optional", default=None, view={"label": " ","format":percent_format(0)}
            ),
            "industry": hx.Structure(
                view={"label": "Industry"},
                children={
                    "naics_search": hx.Str(
                        mode="input",
                        optionality="optional",
                        options_column="NAICS_Key",
                        options_table="table_naics_master",
                        default=None,
                        view={"label": "NAICS Industry Search"},
                    ),

                    "naics_code": hx.Str(
                        mode="output",
                        view={"label": "NAICS Code"},
                        async_input=["word_documents_task"]
                    ),

                    "mapped_sic_code": hx.Str(
                        mode="output",
                        view={"label": "Approximate SIC Code"},
                        async_input=["word_documents_task"]
                    ),
                
                    "class_of_business": hx.Str(
                        mode="output", 
                        view={"label": "Class of Business"},
                        async_input=["word_documents_task"]
                    ),
                    "sic_code": hx.Str(
                        mode="input",
                        optionality="optional",
                        options_column="SIC",
                        options_table="table_sic_code",
                        default=None,
                        view={"label": "SIC Code"},
                    ),
                    "alert": hx.Str(mode="output", view={"label": "Alert"}),
                    "wh_status": hx.Str(mode="output", view={"label": "WH Status"}),
                    "wh_information": hx.Str(
                        mode="output", view={"label": "WH Information"}
                    ),
                },
            ),
            "company_ownership": hx.Str(
                mode="input",
                optionality="optional",
                options_column="Options",
                options_table="table_company_ownership",
                default=None,
                view={"label": " "},
            ),
            "state_requirements": hx.Structure(
                view={"label": "State Requirements"},
                children={
                    "retroactive_date": hx.Str(
                        mode="input",
                        optionality="optional",
                        options_column="NonDates",
                        options_table="table_non_dates",
                        default=None,#'Policy Inception'
                        view={"label": "Retroactive Date"},
                    ),
                    "prior_knowledge_date": hx.Str(
                        mode="input",
                        optionality="optional",
                        options_column="Response",
                        options_table="table_prior_knowledge",
                        default=None,#'1st policy year'
                        view={"label": "Prior Knowledge Date"},
                    ),
                },
            ),
            "package_information": hx.Structure(
                view={"label": "Package Information"},
                children={
                    "combined_single_aggregate_limit": hx.Bool(
                        mode="input",
                        default=False,
                        optionality="required",
                        view={"label": "Combined Single Aggregate Limit"},
                    ),
                    "package_discount": hx.Float(
                        mode="output", view={"label": "Package Discount","format":percent_format(0)}
                    ),
                    "finished_rating": hx.Bool(
                        mode="input",
                        default=False,
                        optionality="required",
                        view={"label": "Finished Rating"},
                    ),
                },
            ),
            "quote_grid_summary": hx.Structure(
                view={"label": "Quote Grid Summary"},
                children={
                    "epl": hx.Structure(
                        view={"label": "EPL"}, children={**quote_grid_summary()}
                    ),
                    "fid": hx.Structure(
                        view={"label": "Fiduciary"}, children={**quote_grid_summary()}
                    ),
                    "pcl": hx.Structure(
                        view={"label": "PCL"}, children={**quote_grid_summary()}
                    ),
                    "cc": hx.Structure(
                        view={"label": "CC"}, children={**quote_grid_summary()}
                    ),
                },
            ),
            "final_premium_summary": hx.Structure(
                view={"label": "Final Premium Summary"},
                children={
                    "rounding_min": hx.Float(
                        mode="output", view={"label": "Rounding Min", "format": thousands_format(0)}
                    ),
                    "rounding_max": hx.Float(
                        mode="output", view={"label": "Rounding Max", "format": thousands_format(0)}
                    ),
                    "benchmark_premium": hx.Float(
                        mode="output", view={"label": "Benchmark Premium", "format": thousands_format(0)}, async_input=["rarc_task"]
                    ),
                    "benchmark_premium_pre_uw_adj": hx.Float(
                        mode="output", view={"label": "Benchmark Premium (pre UW Adjustments)", "format": thousands_format(0)}, async_input=["rarc_task"]
                    ),                 
                    "pre_rounding_admitted_premium": hx.Float(
                        mode="output", view={"label": "Pre-Rounding Admitted Premium", "format": thousands_format(0)}, async_input=["rarc_task"]
                    ),
                    "post_rounding_admitted_premium": hx.Float(
                        mode="output", async_input = ["rarc_task"], view={"label": "Post-Rounding Admitted Premium", "format": thousands_format(0)}
                    ),
                    "benchmark_term_premium": hx.Float(
                        mode="output", view={"label": "Benchmark Term Premium", "format": thousands_format(0)}
                    ),
                    "benchmark_term_premium_pre_uw_adj": hx.Float(
                        mode="output", view={"label": "Benchmark Term Premium (pre UW Adjustments)", "format": thousands_format(0)}
                    ),
                    "technical_term_premium": hx.Float(
                        mode="output", view={"label": "Technical Term Premium", "format": thousands_format(0)}
                    ),
                    "final_admitted_term_premium": hx.Float(
                        mode="output", async_input=["rarc_task", "expiring_policy_fetch_task"], view={"label": "Final Admitted Term Premium", "format": thousands_format(0)}
                    ),
                    "bpi": hx.Float(mode="output", view={"label": "BPI", "format":percent_format(2)}),
                    "tpi": hx.Float(mode="output", view={"label": "TPI", "format":percent_format(2)}),
                },
            ),
        },
    )
