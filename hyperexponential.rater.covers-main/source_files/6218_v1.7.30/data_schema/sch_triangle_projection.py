########################################################################################################################
####################                        OUTSTANDING                                             ####################
########################################################################################################################
###                                                                                                                  ###
########################################################################################################################


import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

def sch_triangle_projection(cds):
        
    # Extending cds nodes for RMS
    cds.extend_node_rater_defined("cds", {

        "triangle_projection": hx.Structure(children={
            "override_triangle":                hx.Bool( mode="input",   view={"label": "Use Override Triangle?"},                   default=False,                           async_input=["tri_exclusions_setup_task"]),
            "override_triangle_date":           hx.Date( mode="input",   view={"label": "Enter Date of Override Triangle:"},         default=None, optionality="optional",    async_input=["tri_override_setup_task"]),
            "override_triangle_date_used":      hx.Date( mode="input",   view={"label": "Date of Override Triangle used: "},         default=None, optionality="optional",    async_output=["tri_override_setup_task"]),
            "override_triangle_years":          hx.Float(mode="input",   view={"label": "Enter Number of Years:"},                   default=5,                               async_input=["tri_override_setup_task"]),
            "assign_override_triangle_status":  hx.Str(  mode="output",  view={"label": "Override Triangle Status"}),
            "async_override_triangle_status":   hx.Str(  mode="output",  view={"label": "Override Triangle Last Setup Status"},                                               async_output=["tri_override_setup_task"]),


            "tri_exclusions_setup_task_status": hx.Str(mode="output",   view={"label": "Exclusions Triangle Task Status"},                                                    async_output=["tri_exclusions_setup_task"]),
            "tri_exclusions_dimensions_status": hx.Str(mode="output",   view={"label": "Exclusions Triangle Active?"} ),

            "benchmark_name": hx.Structure(view={"label": "Benchmark Name"}, children={
                "default"           : hx.Str(mode="output",             view={"label": "Algorithmic"} ),
                "override"          : hx.Str(mode="input",              view={"label": "Override"},                                 default=None, optionality="optional",   options_table="lst_benchmarknames", options_column="Benchmark Class"),
                "selected"          : hx.Str(mode="output",             view={"label": "Selected"}),
            }),
            "experience_weight": hx.Structure(view={"label": "Experience Weight"}, children={
                "default"           : hx.Float(mode="output",           view={"label": "Algorithmic", "format":percent_format(1)}),
                "override"          : hx.Float(mode="input",            view={"label": "Override",    "format":percent_format(1)},  default=None, optionality="optional"),
                "selected"          : hx.Float(mode="output",           view={"label": "Selected",    "format":percent_format(1)}),
            }),
            "benchmark_use_occurrence": hx.Bool(mode="input",  default=False, view={"label": "Use Claims Occurrence pattern, not Claims Made "}),


            "tri_1_loaded_from_bi": hx.Triangle(mode="output"),
            "tri_2_manual_input":   hx.Triangle(mode="input",                                                                                  async_input=["tri_exclusions_setup_task"], async_output=["tri_override_setup_task"]),
            "tri_3_selected":       hx.Triangle(mode="output",  default_average="vw_all", averages={
                "vw_3":   {"label":   "3-year",  "average_type": "column_sum",  "latest_diagonal": "include",  "last_n_origin_periods": 3},
                "vw_5":   {"label":   "5-year",  "average_type": "column_sum",  "latest_diagonal": "include",  "last_n_origin_periods": 5},
                "vw_7":   {"label":   "7-year",  "average_type": "column_sum",  "latest_diagonal": "include",  "last_n_origin_periods": 7},
                "vw_10":  {"label":  "10-year",  "average_type": "column_sum",  "latest_diagonal": "include",  "last_n_origin_periods": 10},
                "vw_all": {"label": "all-year",  "average_type": "column_sum",  "latest_diagonal": "include",  "last_n_origin_periods": None},
            }),

            "tri_4_result":       hx.Triangle(mode="output",  default_average="vw_all", averages={
                "vw_7":   {"label":   "7-year",  "average_type": "column_sum",  "latest_diagonal": "include",  "last_n_origin_periods": 7},
                "vw_all": {"label": "all-year",  "average_type": "column_sum",  "latest_diagonal": "include",  "last_n_origin_periods": None},
            }),
            "tri_3a_exclusions":   hx.Triangle(mode="input",                                                                                     async_output=["tri_exclusions_setup_task"]),



            "incremental_dev_factor": hx.List(mode="input", default_element_count=15, view={"label": "Incremental DF"}, children={
                "show_idf_row"          : hx.Bool( mode="output", view={"label": "Show Row"}),
                "development_qtr"       : hx.Float(mode="output", view={"label": "Development Qtr",             "format":integer_format(0)}),
                "development_mth"       : hx.Float(mode="output", view={"label": "Development Mth",             "format":integer_format(0)}),
                "development_label"     : hx.Str(  mode="output", view={"label": "Label"}),

                "experience_default"    : hx.Float(mode="output", view={"label": "Experience - Algorithmic",    "format":thousands_format(3)}),
                "experience_override"   : hx.Float(mode="input",  view={"label": "Experience - Override",       "format":thousands_format(3)}, default=None, optionality="optional" ),
                "experience_selected"   : hx.Float(mode="output", view={"label": "Experience - Selected",       "format":thousands_format(3)}),

                "benchmark_default"     : hx.Float(mode="output", view={"label": "Benchmark - Algorithmic",     "format":thousands_format(3)}),
                "benchmark_override"    : hx.Float(mode="output", view={"label": "Benchmark - Override",        "format":thousands_format(3)}),
                "benchmark_selected"    : hx.Float(mode="output", view={"label": "Benchmark - Selected",        "format":thousands_format(3)}),

                "blended_default"       : hx.Float(mode="output", view={"label": "Blended - Algorithmic",       "format":thousands_format(3)}),
                "blended_override"      : hx.Float(mode="output", view={"label": "Blended - Override",          "format":thousands_format(3)}),
                "blended_selected"      : hx.Float(mode="output", view={"label": "Blended - Selected",          "format":thousands_format(3)})
            }),


            "tail_factor": hx.Structure(view={"label": "Tail DF"}, children={
                "show_idf_row"          : hx.Bool( mode="output", view={"label": "Show Row"}),

                "experience_default"    : hx.Float(mode="output", view={"label": "Experience - Algorithmic",    "format":thousands_format(3)}),
                "experience_override"   : hx.Float(mode="input",  view={"label": "Experience - Override",       "format":thousands_format(3)}, default=None, optionality="optional" ),
                "experience_selected"   : hx.Float(mode="output", view={"label": "Experience - Selected",       "format":thousands_format(3)}),

                "benchmark_default"     : hx.Float(mode="output", view={"label": "Benchmark - Algorithmic",     "format":thousands_format(3)}),
                "benchmark_override"    : hx.Float(mode="output", view={"label": "Benchmark - Override",        "format":thousands_format(3)}),
                "benchmark_selected"    : hx.Float(mode="output", view={"label": "Benchmark - Selected",        "format":thousands_format(3)}),

                "blended_default"       : hx.Float(mode="output", view={"label": "Blended - Algorithmic",       "format":thousands_format(3)}),
                "blended_override"      : hx.Float(mode="output", view={"label": "Blended - Override",          "format":thousands_format(3)}),
                "blended_selected"      : hx.Float(mode="output", view={"label": "Blended - Selected",          "format":thousands_format(3)})

            }),


            "percents_ultimate": hx.List(mode="input", default_element_count=15, view={"label": "Incremental DF"}, children={
                "show_ult_row"          : hx.Bool( mode="output", view={"label": "Show Row"}),
                "development_qtr"       : hx.Float(mode="output", view={"label": "Development Qtr",                     "format":integer_format(0)}),
                "development_mth"       : hx.Float(mode="output", view={"label": "Development Mth",                     "format":integer_format(0)}),
                "percents_label"        : hx.Str(  mode="output", view={"label": "Label"}),

                "experience_default_perc_ult"    : hx.Float(mode="output", view={"label": "Experience - Algorithmic",   "format":percent_format(2)}),
                "experience_override_perc_ult"   : hx.Float(mode="output", view={"label": "Experience - Override",      "format":percent_format(2)}),
                "experience_selected_perc_ult"   : hx.Float(mode="output", view={"label": "Experience - Selected",      "format":percent_format(2)}),

                "benchmark_default_perc_ult"     : hx.Float(mode="output", view={"label": "Benchmark - Algorithmic",    "format":percent_format(2)}),
                "benchmark_override_perc_ult"    : hx.Float(mode="output", view={"label": "Benchmark - Override",       "format":percent_format(2)}),
                "benchmark_selected_perc_ult"    : hx.Float(mode="output", view={"label": "Benchmark - Selected",       "format":percent_format(2)}),

                "blended_default_perc_ult"       : hx.Float(mode="output", view={"label": "Blended - Algorithmic",      "format":percent_format(2)}),
                "blended_override_perc_ult"      : hx.Float(mode="output", view={"label": "Blended - Override",         "format":percent_format(2)}),
                "blended_selected_perc_ult"      : hx.Float(mode="output", view={"label": "Blended - Selected",         "format":percent_format(2)})
            }),
        })
    })
