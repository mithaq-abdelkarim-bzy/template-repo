########################################################################################################################
####################                        OUTSTANDING                                             ####################
########################################################################################################################

###                                                                                                                  ###
########################################################################################################################


import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

def sch_profit_commission(cds):
        
    cds.extend_node_rater_defined("cds", {

        "profit_commission": hx.Structure(children={
            "simulate_pc_task_status"               : hx.Str(mode="output", view={"label": "Simulate PC Status"} ),
            "consistent_pc_latest_param"            : hx.Str(mode="output", view={"label": "Simulated PC upto-date"} ),


            "param_attritional": hx.Structure(view={"label": "Attritional"},children={
                "expected_loss"                     : hx.Float(mode="output", view={"label": "Expected Loss",               "format":thousands_format(0)}),
                "cov_benchmark"                     : hx.Float(mode="output", view={"label": "Benchmark CoV",               "format":percent_format(2)}),
                "cov_actual"                        : hx.Float(mode="output", view={"label": "Actual CoV",                  "format":percent_format(2)}),
                "cov_selected"                      : hx.Float(mode="output", view={"label": "Selected CoV",                "format":percent_format(2)}),
                "stdev_benchmark"                   : hx.Float(mode="output", view={"label": "Benchmark Standard Deviation","format":thousands_format(0)}),
                "stdev_actual"                      : hx.Float(mode="output", view={"label": "Actual Standard Deviation",   "format":thousands_format(0)}),
                "stdev_selected"                    : hx.Float(mode="output", view={"label": "Selected Standard Deviation", "format":thousands_format(0)}),
                "distribution"                      : hx.Str(  mode="output", view={"label": "Distribution"}),
                "param_1"                           : hx.Float(mode="output", view={"label": "Parameter 1",                 "format":thousands_format(4)}),
                "param_2"                           : hx.Float(mode="output", view={"label": "Parameter 2",                 "format":thousands_format(4)}),
                "client_weight"                     : hx.Float(mode="output", view={"label": "Weighting to Client Data",    "format":percent_format(2)}),
            }),

            "param_large": hx.Structure(view={"label": "Large"},children={
                "expected_loss"                     : hx.Float(mode="output", view={"label": "Expected Loss",               "format":thousands_format(0)}),
                "cov_benchmark"                     : hx.Float(mode="output", view={"label": "Benchmark CoV",               "format":percent_format(2)}),
                "cov_actual"                        : hx.Float(mode="output", view={"label": "Actual CoV",                  "format":percent_format(2)}),
                "cov_selected"                      : hx.Float(mode="output", view={"label": "Selected CoV",                "format":percent_format(2)}),
                "stdev_benchmark"                   : hx.Float(mode="output", view={"label": "Benchmark Standard Deviation","format":thousands_format(0)}),
                "stdev_actual"                      : hx.Float(mode="output", view={"label": "Actual Standard Deviation",   "format":thousands_format(0)}),
                "stdev_selected"                    : hx.Float(mode="output", view={"label": "Selected Standard Deviation", "format":thousands_format(0)}),
                "distribution"                      : hx.Str(  mode="output", view={"label": "Distribution"}),
                "param_1"                           : hx.Float(mode="output", view={"label": "Parameter 1",                 "format":thousands_format(4)}),
                "param_2"                           : hx.Float(mode="output", view={"label": "Parameter 2",                 "format":thousands_format(4)}),
                "client_weight"                     : hx.Float(mode="output", view={"label": "Weighting to Client Data",    "format":percent_format(2)}),
            }),

            "param_cat_natural": hx.Structure(view={"label": "Natural Catastrophe"},children={
                "expected_loss"                     : hx.Float(mode="output", view={"label": "Expected Loss",               "format":thousands_format(0)}),
                "cov_benchmark"                     : hx.Float(mode="output", view={"label": "Benchmark CoV",               "format":percent_format(2)}),
                "cov_actual"                        : hx.Float(mode="output", view={"label": "Actual CoV",                  "format":percent_format(2)}),
                "cov_selected"                      : hx.Float(mode="output", view={"label": "Selected CoV",                "format":percent_format(2)}),
                "stdev_benchmark"                   : hx.Float(mode="output", view={"label": "Benchmark Standard Deviation","format":thousands_format(0)}),
                "stdev_actual"                      : hx.Float(mode="output", view={"label": "Actual Standard Deviation",   "format":thousands_format(0)}),
                "stdev_selected"                    : hx.Float(mode="output", view={"label": "Selected Standard Deviation", "format":thousands_format(0)}),
                "distribution"                      : hx.Str(  mode="output", view={"label": "Distribution"}),
                "param_1"                           : hx.Float(mode="output", view={"label": "Parameter 1",                 "format":thousands_format(4)}),
                "param_2"                           : hx.Float(mode="output", view={"label": "Parameter 2",                 "format":thousands_format(4)}),
                "client_weight"                     : hx.Float(mode="output", view={"label": "Weighting to Client Data",    "format":percent_format(2)}),
            }),

            "param_cat_other": hx.Structure(view={"label": "Non-Natural Catastrophe (or NatCat if no RMS)"},children={
                "expected_loss"                     : hx.Float(mode="output", view={"label": "Expected Loss",               "format":thousands_format(0)}),
                "cov_benchmark"                     : hx.Float(mode="output", view={"label": "Benchmark CoV",               "format":percent_format(2)}),
                "cov_actual"                        : hx.Float(mode="output", view={"label": "Actual CoV",                  "format":percent_format(2)}),
                "cov_selected"                      : hx.Float(mode="output", view={"label": "Selected CoV",                "format":percent_format(2)}),
                "stdev_benchmark"                   : hx.Float(mode="output", view={"label": "Benchmark Standard Deviation","format":thousands_format(0)}),
                "stdev_actual"                      : hx.Float(mode="output", view={"label": "Actual Standard Deviation",   "format":thousands_format(0)}),
                "stdev_selected"                    : hx.Float(mode="output", view={"label": "Selected Standard Deviation", "format":thousands_format(0)}),
                "distribution"                      : hx.Str(  mode="output", view={"label": "Distribution"}),
                "param_1"                           : hx.Float(mode="output", view={"label": "Parameter 1",                 "format":thousands_format(4)}),
                "param_2"                           : hx.Float(mode="output", view={"label": "Parameter 2",                 "format":thousands_format(4)}),
                "client_weight"                     : hx.Float(mode="output", view={"label": "Weighting to Client Data",    "format":percent_format(2)}),
            }),

            
            # this is a list of 10 scenarios including base in first position (0) and then a combination of inputs, output calcs and output async details
            "scenarios": hx.List(mode="input", default_element_count=10, min_element_count=10, max_element_count=10, children={
                "scenario"                          : hx.Str(  mode="output", view={"label": "Scenario"}),
                "label"                             : hx.Str(  mode="output", view={"label": "Label:"}),
                "include"                           : hx.Bool( mode="input",  view={"label": "Include:"},                                                           default=True),
                "complete"                          : hx.Bool( mode="output", view={"label": "Complete:"}),
                "share"                             : hx.Float(mode="input",  view={"label": "PC (%):",                             "format":percent_format(2)},    default=None,   optionality="optional"),
                "expenses"                          : hx.Float(mode="input",  view={"label": "UW Expense (%):",                     "format":percent_format(2)},    default=None,   optionality="optional"),  
                "basis"                             : hx.Str(  mode="input",  view={"label": "UW Expense % of Premium Basis:",      "format":percent_format(2)},    default="Gross",options_table="lst_gn", options_column="GrossNet"),
                "deficit"                           : hx.Float(mode="input",  view={"label": "Deficit:", "format":thousands_format(0)},                             default=0),
                "additionalfeaturesindicator"       : hx.Str(  mode="input",  view={"label": "Additional Structure type:"},                                         default="No",   options_table="lst_pc_structure_type", options_column="StructureType"),
                "threshold_bonus_share"             : hx.Float(mode="input",  view={"label": "PC Payable Below Threshold (%):",     "format":percent_format(2)},    default=None,   optionality="optional"),
                "threshold_lr_cutoff"               : hx.Float(mode="input",  view={"label": "Net LR Threshold (%):",               "format":percent_format(2)},    default=None,   optionality="optional"),
                "slidingscale_bonus_lr"             : hx.Float(mode="input",  view={"label": "For each % below Net LR Threshold (%):","format":percent_format(2)},  default=None,   optionality="optional"),
                "slidingscale_bonus_scale"          : hx.Float(mode="input",  view={"label": "Profit Comm. Increases by (%):",      "format":percent_format(2)},    default=None,   optionality="optional"),
                "slidingscale_bonus_maxtotalpc"     : hx.Float(mode="input",  view={"label": "to Max Profit Comm (%):",             "format":percent_format(2)},    default=None,   optionality="optional"),
                "slidingscale_clawback_lr"          : hx.Float(mode="input",  view={"label": "For each % above Net LR Threshold (%):","format":percent_format(2)},  default=None,   optionality="optional"),
                "slidingscale_clawback_scale"       : hx.Float(mode="input",  view={"label": "Profit Comm. Decreases by (%):",      "format":percent_format(2)},    default=None,   optionality="optional"),
                "slidingscale_clawback_mintotalpc"  : hx.Float(mode="input",  view={"label": "to Min Profit Comm (%):",             "format":percent_format(2)},    default=None,   optionality="optional"),


                "result_param_1_att"               : hx.Float(mode="output", view={"label": "Simulated Param1 Attrition",                                       "format":thousands_format(4)}),
                "result_param_1_large"             : hx.Float(mode="output", view={"label": "Simulated Param1 Large",                                           "format":thousands_format(4)}),
                "result_param_1_cat_other"         : hx.Float(mode="output", view={"label": "Simulated Param1 Non-Natural Catastrophe (or NatCat if no RMS)",   "format":thousands_format(4)}),
                "result_param_1_cat_natural"       : hx.Float(mode="output", view={"label": "Simulated Param1 Natural Catastrophe",                             "format":thousands_format(4)}),

                "result_param_2_att"               : hx.Float(mode="output", view={"label": "Simulated Param2 Attrition",                                       "format":thousands_format(4)}),
                "result_param_2_large"             : hx.Float(mode="output", view={"label": "Simulated Param2 Large",                                           "format":thousands_format(4)}),
                "result_param_2_cat_other"         : hx.Float(mode="output", view={"label": "Simulated Param2 Non-Natural Catastrophe (or NatCat if no RMS)",   "format":thousands_format(4)}),
                "result_param_2_cat_natural"       : hx.Float(mode="output", view={"label": "Simulated Param2 Natural Catastrophe",                             "format":thousands_format(4)}),


                "result_exp_loss_att"               : hx.Float(mode="output", view={"label": "Simulated Attrition",                                             "format":thousands_format(0)}),
                "result_exp_loss_large"             : hx.Float(mode="output", view={"label": "Simulated Large",                                                 "format":thousands_format(0)}),
                "result_exp_loss_cat_other"         : hx.Float(mode="output", view={"label": "Simulated Non-Natural Catastrophe (or NatCat if no RMS)",         "format":thousands_format(0)}),
                "result_exp_loss_cat_natural"       : hx.Float(mode="output", view={"label": "Simulated Natural Catastrophe",                                   "format":thousands_format(0)}),
                "result_exp_loss_total"             : hx.Float(mode="output", view={"label": "Simulated Total",                                                 "format":thousands_format(0)}),
                "result_exp_pc_payable"             : hx.Float(mode="output", view={"label": "PC Payable",                                                      "format":thousands_format(0)}),
                "result_exp_pc_payable_override"    : hx.Float(mode="input",  view={"label": "PC Payable Override",                                             "format":thousands_format(0)}, default=None,   optionality="optional"),
                "result_exp_pc_payable_selected"    : hx.Float(mode="output", view={"label": "PC Payable Selected",                                             "format":thousands_format(0)}),
                "result_exp_frequency_loss"         : hx.Float(mode="output", view={"label": "Frequency of Losses (years)",                                     "format":thousands_format(2)}),


                "result_exp_pc_payable_to_GGEPI"         : hx.Float(mode="output", view={"label": "Frequency of Losses (years)"}),
                ### possibly 2-3 more rows to add from ax30:ax33 but need to understand purpose - think Net is being misused in these lines

             }),

            # this is a list of upto 10 scenarios including base always in first position (0) then there would be circa 41 ulrs identified therein
            "distributions": hx.List(mode="output", children={
                "scenario"              : hx.Str(  mode="output", view={"label": "Scenario"}),
                "bucket"                : hx.Str(  mode="output", view={"label": "GN ULR Range"}),
                "ulr"                   : hx.Float(mode="output", view={"label": "Net Loss Ratio",                  "format":percent_format(2)}),
                "uw_profit"             : hx.Float(mode="output", view={"label": "Underwriter Profit (USD)",        "format":thousands_format(0)}),
                "pc_payable"            : hx.Float(mode="output", view={"label": "PC Payable (USD)",                "format":thousands_format(0)}),
#                "cdf_att"               : hx.Float(mode="output", view={"label": "CDF (Att)"}),
                "pdf_att"               : hx.Float(mode="output", view={"label": "Att",                             "format":percent_format(2)}),
#                "cdf_large"             : hx.Float(mode="output", view={"label": "CDF (Large)"}),
                "pdf_large"             : hx.Float(mode="output", view={"label": "Large",                           "format":percent_format(2)}),
#                "cdf_cat_other"         : hx.Float(mode="output", view={"label": "CDF (Non Nat Cat)"}),
                "pdf_cat_other"         : hx.Float(mode="output", view={"label": "Non Nat Cat",                     "format":percent_format(2)}),
#                "cdf_cat_natural"       : hx.Float(mode="output", view={"label": "CDF (Cat)"}),
                "pdf_cat_natural"       : hx.Float(mode="output", view={"label": "Cat",                             "format":percent_format(2)}),
#                "cdf_total"             : hx.Float(mode="output", view={"label": "CDF (Total)"}),
                "pdf_total"             : hx.Float(mode="output", view={"label": "Total",                           "format":percent_format(2)}),
            }),
        })
    })