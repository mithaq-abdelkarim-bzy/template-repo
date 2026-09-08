########################################################################################################################
####################                        OUTSTANDING                                             ####################
########################################################################################################################

########################################################################################################################

import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
from data_schema.sch_show_hide_and_dropdown import yes_no_list, basis_list

def sch_rating_summary(cds):
        
    # Extending cds nodes for RMS
    cds.extend_node_rater_defined("cds", {

        "rating_summary": hx.Structure(children={
            "message_excluded_years"                    : hx.Str(mode="output", view={"label": "Status - Load Historic Claims"}),
            "chart_basis"                               : hx.Str(mode="input", default="Gross Gross",  options=basis_list, view={"label": "Metric Basis"}),
            "chart_show_basis_gn"                       : hx.Bool(mode="output", view={"label": "Show basis"}),
            "chart_show_basis_gg"                       : hx.Bool(mode="output", view={"label": "Show basis"}),

            # listing of individual facilities (technically section references)
            "detail_by_year": hx.List(mode="input", default_element_count=16, min_element_count=16, max_element_count=16, children={
                "yoa"                                   : hx.Float(mode="output", view={"label": "Year of\nAccount",                                "format":integer_format(0)},    async_input=["generate_uw_rationale_doc_task"]),
                "incept_date"                           : hx.Date(mode="output",  view={"label": "Inception\nDate"}),
                "expiry_date"                           : hx.Date(mode="output",  view={"label": "Expiry Date"}),
                "expiry_date_annual_est"                : hx.Date(mode="output",  view={"label": "Expiry Date\nannualised"}),

                "include_suggested"                     : hx.Str(  mode="output", view={"label": "Include -\ncalculated"}),
                "include_override"                      : hx.Str(  mode="input",  view={"label": "Include -\noverride"},                                            default=None,   optionality="optional", options=yes_no_list),
                "include_selected"                      : hx.Str(  mode="output", view={"label": "Include -\nselected"}),
                "include_selected_weight"               : hx.Float(mode="output", view={"label": "Include -\nselected weight",                      "format":thousands_format(2)}),


                "policy_length_calc"                    : hx.Float(mode="output", view={"label": "Policy Length -\ncalculated",                     "format":thousands_format(2)}),
                "policy_length_override"                : hx.Float(mode="input",  view={"label": "Policy Length -\noverride",                       "format":thousands_format(2)},  default=None,   optionality="optional"),
                "policy_length_selected"                : hx.Float(mode="output", view={"label": "Policy Length -\nselected",                       "format":thousands_format(2)}),
                "policy_length_scalant"                 : hx.Float(mode="output", view={"label": "Policy Length -\nscalant",                        "format":thousands_format(2)}),
                "maturity"                              : hx.Float(mode="output", view={"label": "Number of years\ndeveloped",                      "format":thousands_format(5)}),


                "port_chg_prior"                        : hx.Float(mode="output", view={"label": "Portfolio Change -\nprevious",                    "format":percent_format(2)}),
                "port_chg_suggested"                    : hx.Float(mode="output", view={"label": "Portfolio Change -\nsuggested",                   "format":percent_format(2)}),
                "port_chg_override"                     : hx.Float(mode="input",  view={"label": "Portfolio Change -\noverride",                    "format":percent_format(2)},    default=None,   optionality="optional" ),
                "port_chg_selected"                     : hx.Float(mode="output", view={"label": "Portfolio Change -\nselected",                    "format":percent_format(2)}),
                "port_chg_cumul_prior"                  : hx.Float(mode="output", view={"label": "Portfolio Change -\nCumulative Index previous",   "format":percent_format(2)}),
                "port_chg_cumul_suggested"              : hx.Float(mode="output", view={"label": "Portfolio Change -\nCumulative Index suggested",  "format":percent_format(2)}),
                "port_chg_cumul_selected"               : hx.Float(mode="output", view={"label": "Portfolio Change -\nCumulative Index selected",   "format":percent_format(2)}),

                "rate_chg_prior"                        : hx.Float(mode="output", view={"label": "Rate Change -\nprevious",                         "format":percent_format(2)}),
                "rate_chg_account"                      : hx.Float(mode="output", view={"label": "Rate Change -\naccount",                          "format":percent_format(2)}),
                "rate_chg_portfolio"                    : hx.Float(mode="output", view={"label": "Rate Change -\nbenchmark",                        "format":percent_format(2)}),
                "rate_chg_suggested"                    : hx.Float(mode="output", view={"label": "Rate Change -\nsuggested",                        "format":percent_format(2)}),
                "rate_chg_override"                     : hx.Float(mode="input",  view={"label": "Rate Change -\noverride",                         "format":percent_format(2)},    default=None,   optionality="optional" ),
                "rate_chg_selected"                     : hx.Float(mode="output", view={"label": "Rate Change -\nselected",                         "format":percent_format(2)}),
                "rate_chg_cumul_prior"                  : hx.Float(mode="output", view={"label": "Rate Change -\nCumulative Index previous",        "format":percent_format(2)}),
                "rate_chg_cumul_suggested"              : hx.Float(mode="output", view={"label": "Rate Change -\nCumulative Index suggested",       "format":percent_format(2)}),
                "rate_chg_cumul_selected"               : hx.Float(mode="output", view={"label": "Rate Change -\nCumulative Index selected",        "format":percent_format(2)}),

                "infl_chg_prior"                        : hx.Float(mode="output", view={"label": "Inflation Change -\nprevious",                    "format":percent_format(2)}),
                "infl_chg_suggested"                    : hx.Float(mode="output", view={"label": "Inflation Change -\nsuggested",                   "format":percent_format(2)}),
                "infl_chg_override"                     : hx.Float(mode="input",  view={"label": "Inflation Change -\noverride",                    "format":percent_format(2)},    default=None,   optionality="optional" ),
                "infl_chg_selected"                     : hx.Float(mode="output", view={"label": "Inflation Change -\nselected",                    "format":percent_format(2)}),
                "infl_chg_cumul_prior"                  : hx.Float(mode="output", view={"label": "Inflation Change -\nCumulative Index previous",   "format":percent_format(2)}),
                "infl_chg_cumul_suggested"              : hx.Float(mode="output", view={"label": "Inflation Change -\nCumulative Index suggested",  "format":percent_format(2)}),
                "infl_chg_cumul_selected"               : hx.Float(mode="output", view={"label": "Inflation Change -\nCumulative Index selected",   "format":percent_format(2)}),

                "experience_default_perc_ult"           : hx.Float(mode="output", view={"label": "Development -\n% Ultimate -\nExperience Default", "format":percent_format(2)}),
                "experience_selected_perc_ult"          : hx.Float(mode="output", view={"label": "Development -\n% Ultimate -\nExperience Selected","format":percent_format(2)}),
                "benchmark_default_perc_ult"            : hx.Float(mode="output", view={"label": "Development -\n% Ultimate -\nBenchamrk Default",  "format":percent_format(2)}),
                "benchmark_selected_perc_ult"           : hx.Float(mode="output", view={"label": "Development -\n% Ultimate -\nBenchamrk Selected", "format":percent_format(2)}),
                "blended_default_perc_ult"              : hx.Float(mode="output", view={"label": "Development -\n% Ultimate -\nBlended Default",    "format":percent_format(2)}),
                "blended_selected_perc_ult"             : hx.Float(mode="output", view={"label": "Development -\n% Ultimate -\nBlended Selected",   "format":percent_format(2)}),
                "prior_selected_perc_ult"               : hx.Float(mode="output", view={"label": "Development -\n% Ultimate -\nBlended Prior",   "format":percent_format(2)}),
                "interp_blended_selected_perc_ult"      : hx.Float(mode="output", view={"label": "Development -\n% Ultimate -\nBlended Sel & Interp", "format": {"output": "percent", "mantissa": 2}}),

                "premium_prior"                         : hx.Float(mode="output", view={"label": "GG Written\nPremium -\nprior",                    "format":thousands_format(0)}),
                "premium_suggested"                     : hx.Float(mode="output", view={"label": "GG Written\nPremium -\nsuggested",                "format":thousands_format(0)}),
                "premium_override"                      : hx.Float(mode="input",  view={"label": "GG Written\nPremium -\noverride",                 "format":thousands_format(0)},    default=None,   optionality="optional" ),
                "premium_selected"                      : hx.Float(mode="output", view={"label": "GG Written\nPremium -\nselected",                 "format":thousands_format(0)},    async_input=["generate_uw_rationale_doc_task"]),
                "premium_selected_gn"                   : hx.Float(mode="output", view={"label": "GN Written\nPremium -\nselected",                 "format":thousands_format(0)},    async_input=["generate_uw_rationale_doc_task"]),
                "premium_selected_ol"                   : hx.Float(mode="output", view={"label": "GG Written\nPremium -\nselected,\non-level",      "format":thousands_format(0)}),
                "premium_selected_ol_scaled"            : hx.Float(mode="output", view={"label": "GG Written\nPremium -\nselected,\non-level,\nscaled","format":thousands_format(0)}),

                "incurred_prior"                        : hx.Float(mode="output", view={"label": "Incurred -\nprevious",                            "format":thousands_format(0)}),
                "paid_listing"                          : hx.Float(mode="output", view={"label": "Paid -\nbi paid",                                 "format":thousands_format(0)}),
                "incurred_listing"                      : hx.Float(mode="output", view={"label": "Incurred -\nbi",                                  "format":thousands_format(0)}),
                "incurred_pp_blend"                     : hx.Float(mode="output", view={"label": "Incurred -\npp blend",                            "format":thousands_format(0)}),
                "incurred_pp_most_likely"               : hx.Float(mode="output", view={"label": "Incurred -\npp most likely",                      "format":thousands_format(0)}),
                "incurred_triangle"                     : hx.Float(mode="output", view={"label": "Incurred -\nbi triangle",                         "format":thousands_format(0)}),
                "incurred_suggested"                    : hx.Float(mode="output", view={"label": "Incurred -\nsuggested",                           "format":thousands_format(0)}),
                "incurred_override"                     : hx.Float(mode="input",  view={"label": "Incurred -\noverride",                            "format":thousands_format(0)},    default=None,   optionality="optional" ),
                "incurred_selected"                     : hx.Float(mode="output", view={"label": "Incurred -\nselected",                            "format":thousands_format(0)},    async_input=["generate_uw_rationale_doc_task"]),
                "incurred_selected_lr"                  : hx.Float(mode="output", view={"label": "GG Incurred LR -\nselected",                      "format":percent_format(2)},      async_input=["generate_uw_rationale_doc_task"]),
                "incurred_selected_lr_gn"               : hx.Float(mode="output", view={"label": "GN Incurred LR -\nselected",                      "format":percent_format(2)},      async_input=["generate_uw_rationale_doc_task"]),

                "large_threshold_usd"                   : hx.Float(mode="output", view={"label": "Large Threshold\nUSD",                            "format":thousands_format(0)}),
                "large_threshold_sett_fx"               : hx.Float(mode="output", view={"label": "Large Threshold\nSettlement Fx",                  "format":thousands_format(0)}),
                "incurred_large_prior"                  : hx.Float(mode="output", view={"label": "Incurred Large -\nprevious",                      "format":thousands_format(0)}),
                "paid_large_listing"                    : hx.Float(mode="output", view={"label": "Incurred Large -\nbi paid",                       "format":thousands_format(0)}),
                "incurred_large_listing"                : hx.Float(mode="output", view={"label": "Incurred Large -\nbi incurred",                   "format":thousands_format(0)}),
                "incurred_large_pp_blend"               : hx.Float(mode="output", view={"label": "Incurred Large -\npp blend",                      "format":thousands_format(0)}),
                "incurred_large_pp_most_likely"         : hx.Float(mode="output", view={"label": "Incurred Large -\npp most likely",                "format":thousands_format(0)}),
                "incurred_large_triangle"               : hx.Float(mode="output", view={"label": "Incurred Large -\nbi triangle",                   "format":thousands_format(0)}),
                "incurred_large_suggested"              : hx.Float(mode="output", view={"label": "Incurred Large -\nsuggested",                     "format":thousands_format(0)}),
                "incurred_large_override"               : hx.Float(mode="input",  view={"label": "Incurred Large -\noverride",                      "format":thousands_format(0)},    default=None,   optionality="optional" ),
                "incurred_large_selected"               : hx.Float(mode="output", view={"label": "Incurred Large -\nselected",                      "format":thousands_format(0)}),
                "incurred_large_selected_lr"            : hx.Float(mode="output", view={"label": "Incurred Large -\nselected loss ratio",           "format":percent_format(2)}), 
                "incurred_large_selected_inflated"      : hx.Float(mode="output", view={"label": "Incurred Large -\nselected inflated",             "format":thousands_format(0)}),

                "incurred_cat_prior"                    : hx.Float(mode="output", view={"label": "Incurred Cat -\nprevious",                        "format":thousands_format(0)}),
                "paid_cat_listing"                      : hx.Float(mode="output", view={"label": "Incurred Cat -\nbi paid",                         "format":thousands_format(0)}),
                "incurred_cat_listing"                  : hx.Float(mode="output", view={"label": "Incurred Cat -\nbi incurred",                     "format":thousands_format(0)}),
                "incurred_cat_pp_blend"                 : hx.Float(mode="output", view={"label": "Incurred Cat -\npp blend",                        "format":thousands_format(0)}),
                "incurred_cat_pp_most_likely"           : hx.Float(mode="output", view={"label": "Incurred Cat -\npp most likely",                  "format":thousands_format(0)}),
                "incurred_cat_triangle"                 : hx.Float(mode="output", view={"label": "Incurred Cat -\nbi triangle",                     "format":thousands_format(0)}),
                "incurred_cat_suggested"                : hx.Float(mode="output", view={"label": "Incurred Cat -\nsuggested",                       "format":thousands_format(0)}),
                "incurred_cat_override"                 : hx.Float(mode="input",  view={"label": "Incurred Cat -\noverride",                        "format":thousands_format(0)},    default=None,   optionality="optional" ),
                "incurred_cat_selected"                 : hx.Float(mode="output", view={"label": "Incurred Cat -\nselected",                        "format":thousands_format(0)}),
                "incurred_cat_selected_lr"              : hx.Float(mode="output", view={"label": "Incurred Cat -\nselected loss ratio",             "format":thousands_format(0)}),
                "incurred_cat_selected_inflated"        : hx.Float(mode="output", view={"label": "Incurred Cat -\nselected inflated",               "format":thousands_format(0)}),

                "incurred_att_prior"                    : hx.Float(mode="output", view={"label": "Incurred\nAttritional -\nprevious",               "format":thousands_format(0)}),
                "paid_att_listing"                      : hx.Float(mode="output", view={"label": "Incurred\nAttritional -\nbi paid",                "format":thousands_format(0)}),
                "incurred_att_listing"                  : hx.Float(mode="output", view={"label": "Incurred\nAttritional -\nbi incurred",            "format":thousands_format(0)}),
                "incurred_att_pp_blend"                 : hx.Float(mode="output", view={"label": "Incurred\nAttritional -\npp blend",               "format":thousands_format(0)}),
                "incurred_att_pp_most_likely"           : hx.Float(mode="output", view={"label": "Incurred\nAttritional -\npp most likely",         "format":thousands_format(0)}),
                "incurred_att_triangle"                 : hx.Float(mode="output", view={"label": "Incurred\nAttritional -\nbi triangle",            "format":thousands_format(0)}),
                "incurred_att_suggested"                : hx.Float(mode="output", view={"label": "Incurred\nAttritional -\nsuggested",              "format":thousands_format(0)}),
                "incurred_att_override"                 : hx.Float(mode="output", view={"label": "Incurred\nAttritional -\noverride",               "format":thousands_format(0)}),
                "incurred_att_selected"                 : hx.Float(mode="output", view={"label": "Incurred\nAttritional -\nselected",               "format":thousands_format(0)}),
                "incurred_att_selected_lr"              : hx.Float(mode="output", view={"label": "Incurred\nAttritional -\nselected loss ratio",    "format":percent_format(2)}), 
                "incurred_att_selected_inflated"        : hx.Float(mode="output", view={"label": "Incurred\nAttritional -\nselected inflated",      "format":thousands_format(0)}),

                "incurred_non_cat_selected_lr"          : hx.Float(mode="output", view={"label": "GG Non-Cat Incurred\nLR - selected",              "format":percent_format(2)},      async_input=["generate_uw_rationale_doc_task"]),
                "incurred_non_cat_selected_lr_gn"       : hx.Float(mode="output", view={"label": "GN Non-Cat Incurred\nLR - selected",              "format":percent_format(2)},      async_input=["generate_uw_rationale_doc_task"]),

                "ultimate_att_cl_selected"                   : hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nCL selected",                                   "format":thousands_format(0)}),
                "ultimate_att_cl_selected_py_factors"        : hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nCL selected prior:\ndevelopment",               "format":thousands_format(0)}),
                "ultimate_att_cl_selected_py_factors_data"   : hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nCL selected prior:\ndevelopment; data",         "format":thousands_format(0)}),
                "ultimate_att_cl_selected_ol"                : hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nCL selected inflated",                          "format":thousands_format(0)}),
                "ultimate_att_cl_selected_ol_exc_scalant"    : hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nCL selected before\nscalant",                   "format":thousands_format(0)}),
                "ultimate_att_cl_selected_ol_py_ol_assump"   : hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nCL selected prior:\ninflation",                 "format":thousands_format(0)}),
                "ultimate_att_cl_selected_ol_py_factors"     : hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nCL selected prior:\ninflation;\ndevelopment",   "format":thousands_format(0)}),
                "ultimate_att_cl_selected_ol_py_factors_data": hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nCL selected prior:\ninflation;\ndevelopment; data","format":thousands_format(0)}),

                "reserving_method_attritional"                 : hx.Str(  mode="output", view={"label": "Ultimate\nAttritional -\nReserving method\nselected"}),
                "ultimate_att_meth_selected_ol"                : hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nMethod selected\ninflated",                   "format":thousands_format(0)}),
                "ultimate_att_meth_selected_ol_exc_scalant"    : hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nMethod selected\nbefore scalant",             "format":thousands_format(0)}),
                "ultimate_att_meth_selected_ol_py_ol_assump"   : hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nMethod selected\nprior: inflation",           "format":thousands_format(0)}),
                "ultimate_att_meth_selected_ol_py_factors"     : hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nMethod selected\nprior: inflation;\ndevelopment", "format":thousands_format(0)}),
                "ultimate_att_meth_selected_ol_py_factors_data": hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nMethod selected\nprior: inflation;\ndevelopment; data", "format":thousands_format(0)}),

                "weighting_exposure"                    : hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nmethod weighting -\nexposure",   "format":percent_format(2)}), 
                "weighting_decay"                       : hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nmethod weighting -\ndecay",      "format":percent_format(2)}),
                "weighting_development"                 : hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nmethod weighting -\ndevelopment","format":percent_format(2)}),
                "weighting_combined"                    : hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nmethod weighting -\ncombined",   "format":percent_format(2)}),
                "weighting_final"                       : hx.Float(mode="output", view={"label": "Ultimate\nAttritional -\nmethod weighting -\nfinal",      "format":percent_format(2)}),

                "display_yoa"                           : hx.Str(  mode="output", view={"label": "Year"}),
                "display_premium_ol"                    : hx.Float(mode="output", view={"label": "Premium",             "format":thousands_format(0)}),
                "display_attritional_weight"            : hx.Float(mode="output", view={"label": "Weight",              "format":percent_format(1)}),

                "display_attritional_incurred_lr"       : hx.Float(mode="output", view={"label": "Incurred\nLR",        "format":percent_format(2)}),
                "display_attritional_chainladder_lr"    : hx.Float(mode="output", view={"label": "Chainladder\nLR",     "format":percent_format(2)}),
                "display_attritional_approach"          : hx.Str(  mode="output", view={"label": "Approach"}),
                "display_attritional_selected_lr"       : hx.Float(mode="output", view={"label": "Selected\nLR",        "format":percent_format(2)}),
                
                "display_large_incurred_lr"             : hx.Float(mode="output", view={"label": "Incurred\nLR",        "format":percent_format(2)}),
                "display_large_chainladder_lr"          : hx.Float(mode="output", view={"label": "Chainladder\nLR",     "format":percent_format(2)}),
                "display_large_approach"                : hx.Str(  mode="output", view={"label": "Approach"}),
                "display_large_selected_lr"             : hx.Float(mode="output", view={"label": "Selected\nLR",        "format":percent_format(2)}),

                "display_cat_incurred_lr"               : hx.Float(mode="output", view={"label": "Incurred\nLR",        "format":percent_format(2)}),
                "display_cat_chainladder_lr"            : hx.Float(mode="output", view={"label": "Chainladder\nLR",     "format":percent_format(2)}),
                "display_cat_approach"                  : hx.Str(  mode="output", view={"label": "Approach"}),
                "display_cat_selected_lr"               : hx.Float(mode="output", view={"label": "Selected\nLR",        "format":percent_format(2)}),

                "display_show_row_inputs"               : hx.Bool( mode="output", view={"label": "Show Row -\ninputs"}),
                "display_show_row_rating"               : hx.Bool( mode="output", view={"label": "Show Row -\nrating"}),


                "chart_att_ilr_gg"                      : hx.Float(mode="output", view={"label": "Att. ILR",       "format":percent_format(1)}),
                "chart_large_ilr_gg"                    : hx.Float(mode="output", view={"label": "Large ILR",       "format":percent_format(1)}),
                "chart_cat_ilr_gg"                      : hx.Float(mode="output", view={"label": "Cat ILR",       "format":percent_format(1)}),

                "chart_att_ilr_gn"                      : hx.Float(mode="output", view={"label": "Att. ILR",       "format":percent_format(1)}),
                "chart_large_ilr_gn"                    : hx.Float(mode="output", view={"label": "Large ILR",       "format":percent_format(1)}),
                "chart_cat_ilr_gn"                      : hx.Float(mode="output", view={"label": "Cat ILR",       "format":percent_format(1)}),

                "chart_att_ilr_ol_gg"                   : hx.Float(mode="output", view={"label": "Att. ILR on-level",       "format":percent_format(1)}),
                "chart_large_ilr_ol_gg"                 : hx.Float(mode="output", view={"label": "Large ILR on-level",       "format":percent_format(1)}),
                "chart_cat_ilr_ol_gg"                   : hx.Float(mode="output", view={"label": "Cat ILR on-level",       "format":percent_format(1)}),

                "chart_att_ilr_ol_gn"                   : hx.Float(mode="output", view={"label": "Att. ILR on-level",       "format":percent_format(1)}),
                "chart_large_ilr_ol_gn"                 : hx.Float(mode="output", view={"label": "Large ILR on-level",       "format":percent_format(1)}),
                "chart_cat_ilr_ol_gn"                   : hx.Float(mode="output", view={"label": "Cat ILR on-level",       "format":percent_format(1)}),

                "chart_att_ilr_proposed_gg"             : hx.Float(mode="output", view={"label": "Att. Proposed",       "format":percent_format(1)}),
                "chart_large_ilr_proposed_gg"           : hx.Float(mode="output", view={"label": "Large Proposed",       "format":percent_format(1)}),
                "chart_cat_ilr_proposed_gg"             : hx.Float(mode="output", view={"label": "Cat Proposed",       "format":percent_format(1)}),                

                "chart_att_ilr_proposed_gn"             : hx.Float(mode="output", view={"label": "Att. Proposed",       "format":percent_format(1)}),
                "chart_large_ilr_proposed_gn"           : hx.Float(mode="output", view={"label": "Large Proposed",       "format":percent_format(1)}),
                "chart_cat_ilr_proposed_gn"             : hx.Float(mode="output", view={"label": "Cat Proposed",       "format":percent_format(1)}),

                "chart_att_ilr"                         : hx.Float(mode="output", view={"label": "Att. ULR",       "format":percent_format(1)}),
                "chart_large_ilr"                       : hx.Float(mode="output", view={"label": "Large ULR",       "format":percent_format(1)}),
                "chart_cat_ilr"                         : hx.Float(mode="output", view={"label": "Cat ULR",       "format":percent_format(1)}),

                "chart_premium"                         : hx.Float(mode="output", view={"label": "Premium",       "format":percent_format(1)}),
                "chart_pricing_lr"                      : hx.Float(mode="output", view={"label": "Pricing LR",       "format":percent_format(1)}),
                "chart_experience_lr"                   : hx.Float(mode="output", view={"label": "Experience LR",       "format":percent_format(1)}),

            }),

            "detail_by_year_total": hx.Structure(view={"label": "Total"}, children={
                "premium_selected"                      : hx.Float(mode="output", view={"label": "GG Written\nPremium -\nselected",                 "format":thousands_format(0)},    async_input=["generate_uw_rationale_doc_task"]),
                "premium_selected_gn"                   : hx.Float(mode="output", view={"label": "GN Written\nPremium -\nselected",                 "format":thousands_format(0)},    async_input=["generate_uw_rationale_doc_task"]),

                "incurred_selected"                     : hx.Float(mode="output", view={"label": "Incurred -\nselected",                            "format":thousands_format(0)},    async_input=["generate_uw_rationale_doc_task"]),
                "incurred_selected_lr"                  : hx.Float(mode="output", view={"label": "GG Incurred LR -\nselected",                      "format":percent_format(2)},      async_input=["generate_uw_rationale_doc_task"]),
                "incurred_selected_lr_gn"               : hx.Float(mode="output", view={"label": "GN Incurred LR -\nselected",                      "format":percent_format(2)},      async_input=["generate_uw_rationale_doc_task"]),

                "incurred_large_selected"               : hx.Float(mode="output", view={"label": "Incurred Large -\nselected",                      "format":thousands_format(0)}),

                "incurred_att_selected"                 : hx.Float(mode="output", view={"label": "Incurred\nAttritional -\nselected",               "format":thousands_format(0)}),
                
                "incurred_non_cat_selected_lr"          : hx.Float(mode="output", view={"label": "GG Non-Cat Incurred\nLR - selected",              "format":percent_format(2)},      async_input=["generate_uw_rationale_doc_task"]),
                "incurred_non_cat_selected_lr_gn"       : hx.Float(mode="output", view={"label": "GN Non-Cat Incurred\nLR - selected",              "format":percent_format(2)},      async_input=["generate_uw_rationale_doc_task"]),

            }),


            "summary_ratios": hx.Structure(children={

                "attritional"   : hx.Structure(children={
                    "gg_pre_uw_adj"     : hx.Structure(view={"label": "GG Loss Ratio"}, children={
                       "ulr_initial_benchmark"          : hx.Float(mode="output", view={"label": "ULR: Inital Benchmark",               "format":percent_format(1)}),
                       "ulr_initial_experience"         : hx.Float(mode="output", view={"label": "ULR: Experience A priori",             "format":percent_format(1)}),
                       "ulr_initial_experience_weighting":hx.Float(mode="output", view={"label": "ULR: Initial Experience Weighting",   "format":percent_format(1)}),
                       "ulr_initial_selected"           : hx.Float(mode="output", view={"label": "ULR: Initial Selected",               "format":percent_format(1)}),
                       "ulr_previous_selected_inferred" : hx.Float(mode="output", view={"label": "ULR: Inferred Selected Previous",     "format":percent_format(1)}),
                       "ulr_previous_override"          : hx.Float(mode="output", view={"label": "ULR: Override Previous",              "format":percent_format(1)}),
                       "ulr_previous"                   : hx.Float(mode="output", view={"label": "ULR: Previous",                       "format":percent_format(1)}),
                       "ulr_previous_suggested"         : hx.Float(mode="output", view={"label": "ULR: Suggested Previous",             "format":percent_format(1)}),
                       "ulr_selected_ol_py_factors_data": hx.Float(mode="output", view={"label": "ULR: Previous, TY Method",            "format":percent_format(1)}),
                       "ulr_selected_ol_py_factors"     : hx.Float(mode="output", view={"label": "ULR: TY Data, TY Method",             "format":percent_format(1)}),
                       "ulr_selected_ol_py_ol_assump"   : hx.Float(mode="output", view={"label": "ULR: TY Data, TY Method, TY % Dev",   "format":percent_format(1)}),
                       "ulr_selected_ol_exc_scalant"    : hx.Float(mode="output", view={"label": "ULR: Suggested",                      "format":percent_format(1)}),
                       "ulr_selected_ol"                : hx.Float(mode="output", view={"label": "ULR: Selected",                       "format":percent_format(1)}),
                       "ulr_uw_override"                : hx.Float(mode="input",  view={"label": "ULR: UW Override",                    "format":percent_format(1)}, default=None,   optionality="optional" ),
                       "ulr_final_uw"                   : hx.Float(mode="output", view={"label": "ULR: Final UW Selected",              "format":percent_format(1)}),
                       "ulr_actuarial_override"         : hx.Float(mode="input",  view={"label": "ULR: Actuarial Override",             "format":percent_format(1)}, default=None,   optionality="optional" ),
                       "ulr_actuarial_override_output"  : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",             "format":percent_format(1)}),
                       "ulr_final"                      : hx.Float(mode="output",    view={"label": "ULR: Final Projected", "format":percent_format(1)}),
                       "blended_LR"               : hx.Float(mode="output", view={"label": "ULR: Final Selected",                 "format":percent_format(1) }),
                       
                    }),

                    "gn_pre_uw_adj"     : hx.Structure(view={"label": "GN Loss Ratio"}, children={
                       "ulr_initial_benchmark"          : hx.Float(mode="output", view={"label": "ULR: Inital Benchmark",               "format":percent_format(1)}),
                       "ulr_initial_experience"         : hx.Float(mode="output", view={"label": "ULR: Experience A prior",             "format":percent_format(1)}),
                       "ulr_initial_experience_weighting":hx.Float(mode="output", view={"label": "ULR: Initial Experience Weighting",   "format":percent_format(1)}),
                       "ulr_initial_selected"           : hx.Float(mode="output", view={"label": "ULR: Initial Selected",               "format":percent_format(1)}),
                       "ulr_previous_selected_inferred" : hx.Float(mode="output", view={"label": "ULR: Inferred Selected Previous",     "format":percent_format(1)}),
                       "ulr_previous_override"          : hx.Float(mode="output", view={"label": "ULR: Override Previous",              "format":percent_format(1)}),
                       "ulr_previous"                   : hx.Float(mode="output", view={"label": "ULR: Previous",                       "format":percent_format(1)}),
                       "ulr_previous_suggested"         : hx.Float(mode="output", view={"label": "ULR: Suggested Previous",             "format":percent_format(1)}),
                       "ulr_selected_ol_py_factors_data": hx.Float(mode="output", view={"label": "ULR: Previous, TY Method",            "format":percent_format(1)}),
                       "ulr_selected_ol_py_factors"     : hx.Float(mode="output", view={"label": "ULR: TY Data, TY Method",             "format":percent_format(1)}),
                       "ulr_selected_ol_py_ol_assump"   : hx.Float(mode="output", view={"label": "ULR: TY Data, TY Method, TY % Dev",   "format":percent_format(1)}),
                       "ulr_selected_ol_exc_scalant"    : hx.Float(mode="output", view={"label": "ULR: Suggested",                      "format":percent_format(1)}),
                       "ulr_selected_ol"                : hx.Float(mode="output", view={"label": "ULR: Selected",                       "format":percent_format(1)}),
                       "ulr_uw_override"                : hx.Float(mode="output", view={"label": "ULR: Override",                       "format":percent_format(1)}),
                       "ulr_final_uw"                   : hx.Float(mode="output", view={"label": "ULR: Final UW Selected",              "format":percent_format(1)}),
                       "ulr_actuarial_override"         : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",             "format":percent_format(1)}),
                       "ulr_actuarial_override_output"  : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",             "format":percent_format(1)}),
                       "ulr_final"                      : hx.Float(mode="output",  view={"label": "ULR: Final Projected",       "format":percent_format(1)}),
                       "blended_LR"               : hx.Float(mode="output", view={"label": "ULR: Final Selected",                 "format":percent_format(1)}),
                    }),

                    "gg_pst_uw_adj"     : hx.Structure(view={"label": "GG Loss Ratio"}, children={
                    #    "ulr_initial_benchmark"          : hx.Float(mode="output", view={"label": "ULR: Inital Benchmark"}),                #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_initial_experience"         : hx.Float(mode="output", view={"label": "ULR: Initial Experience"}),              #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_initial_experience_weighting":hx.Float(mode="output", view={"label": "ULR: Initial Experience Weighting"}),    #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_initial_selected"           : hx.Float(mode="output", view={"label": "ULR: Initial Selected"}),                #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_previous_selected_inferred" : hx.Float(mode="output", view={"label": "ULR: Inferred Selected Previous"}),      #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_previous_override"          : hx.Float(mode="output", view={"label": "ULR: Override Previous"}),               #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_previous"                   : hx.Float(mode="output", view={"label": "ULR: Previous"}),                        #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_previous_suggested"         : hx.Float(mode="output", view={"label": "ULR: Suggested Previous"}),              #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_selected_ol_py_factors_data": hx.Float(mode="output", view={"label": "ULR: Previous, TY Method"}),             #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_selected_ol_py_factors"     : hx.Float(mode="output", view={"label": "ULR: TY Data, TY Method"}),              #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_selected_ol_py_ol_assump"   : hx.Float(mode="output", view={"label": "ULR: TY Data, TY Method, TY % Dev"}),    #shown for completeness/uniformity here - but not able to be calc or displayed
                       "ulr_selected_ol_exc_scalant"    : hx.Float(mode="output", view={"label": "ULR: Suggested",                      "format":percent_format(1)}),
                       "ulr_selected_ol"                : hx.Float(mode="output", view={"label": "ULR: Selected",                       "format":percent_format(1)}),
                       
                       "ulr_uw_override"                : hx.Float(mode="input", view={"label": "ULR: Override",                       "format":percent_format(1)}, default=None,   optionality="optional"),
                       "ulr_final_uw"                   : hx.Float(mode="output", view={"label": "ULR: Final UW Selected",              "format":percent_format(1)}),
                       "ulr_actuarial_override"         : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",             "format":percent_format(1)}),
                       "ulr_actuarial_override_output"  : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",             "format":percent_format(1)}),
                       "ulr_final"                      : hx.Float(mode="output", view={"label": "ULR: Projected Pst Adj",       "format":percent_format(1)}),
                       "blended_LR"               : hx.Float(mode="output", view={"label": "ULR: Projected Pre Adj",                 "format":percent_format(1)})
                      
                    }),

                    "gn_pst_uw_adj"     : hx.Structure(view={"label": "GN Loss Ratio"}, children={
                    #    "ulr_initial_benchmark"          : hx.Float(mode="output", view={"label": "ULR: Inital Benchmark"}),               #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_initial_experience"         : hx.Float(mode="output", view={"label": "ULR: Initial Experience"}),             #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_initial_experience_weighting":hx.Float(mode="output", view={"label": "ULR: Initial Experience Weighting"}),   #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_initial_selected"           : hx.Float(mode="output", view={"label": "ULR: Initial Selected"}),               #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_previous_selected_inferred" : hx.Float(mode="output", view={"label": "ULR: Inferred Selected Previous"}),     #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_previous_override"          : hx.Float(mode="output", view={"label": "ULR: Override Previous"}),              #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_previous"                   : hx.Float(mode="output", view={"label": "ULR: Previous"}),                       #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_previous_suggested"         : hx.Float(mode="output", view={"label": "ULR: Suggested Previous"}),             #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_selected_ol_py_factors_data": hx.Float(mode="output", view={"label": "ULR: Previous, TY Method"}),            #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_selected_ol_py_factors"     : hx.Float(mode="output", view={"label": "ULR: TY Data, TY Method"}),             #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_selected_ol_py_ol_assump"   : hx.Float(mode="output", view={"label": "ULR: TY Data, TY Method, TY % Dev"}),   #shown for completeness/uniformity here - but not able to be calc or displayed
                       "ulr_selected_ol_exc_scalant"    : hx.Float(mode="output", view={"label": "ULR: Suggested",                      "format":percent_format(1)}),
                       "ulr_selected_ol"                : hx.Float(mode="output", view={"label": "ULR: Selected",                       "format":percent_format(1)}),
                       "ulr_uw_override"                : hx.Float(mode="output", view={"label": "ULR: Override",                       "format":percent_format(1)}),
                       "ulr_final_uw"                   : hx.Float(mode="output", view={"label": "ULR: Final UW Selected",              "format":percent_format(1)}),
                       "ulr_actuarial_override"         : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",             "format":percent_format(1)}),
                       "ulr_actuarial_override_output"  : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",             "format":percent_format(1)}),
                       "ulr_final"                      : hx.Float(mode="output", view={"label": "ULR: Projected Pst Adj",                 "format":percent_format(1)}),
                       "blended_LR"               : hx.Float(mode="output", view={"label": "ULR: Projected Pre Adj",                 "format":percent_format(1)}),
                    }),

                    "uw_override"       : hx.Bool(mode="input",  view={"label": "Turn off Loading"},                                                                    default=False),
                    "uw_adjustment"     : hx.Float(mode="input", view={"label": "UW Adj  (% load/discount) (-50% to +200%)",            "format":percent_format(1)},    default=None,   optionality="optional" ),
                    "uw_rationale"      : hx.Str(mode="input", view={"label": "Rationale Required:"},                                                                   default=None,    optionality="optional", async_input=["generate_uw_rationale_doc_task"] ),
                }),



                "large"         : hx.Structure(children={
                    "gg_pre_uw_adj"     : hx.Structure(view={"label": "GG Loss Ratio"}, children={
                       "ulr_previous"                   : hx.Float(mode="output", view={"label": "ULR: Previous",                               "format":percent_format(1)}),
                       "ulr_benchmark"                  : hx.Float(mode="output", view={"label": "ULR: Benchmark",                              "format":percent_format(1)}),
                       "ulr_experience"                 : hx.Float(mode="output", view={"label": "ULR: Experience",                             "format":percent_format(1)}),
                       "ulr_experience_weighting"       : hx.Float(mode="output", view={"label": "ULR: Experience Weighting",                   "format":percent_format(1)}),
                       "ulr_selected_ol"                : hx.Float(mode="output", view={"label": "ULR: Selected",                               "format":percent_format(1)}),
                       "ulr_uw_override"                : hx.Float(mode="output",  view={"label": "ULR: Override",                              "format":percent_format(1)}),
                       "ulr_final_uw"                   : hx.Float(mode="output", view={"label": "ULR: Final UW Selected",                      "format":percent_format(1)}),
                       "ulr_actuarial_override"         : hx.Float(mode="input",  view={"label": "ULR: Actuarial Override",                     "format":percent_format(1)},    default=None,   optionality="optional" ),
                       "ulr_actuarial_override_output"  : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",                     "format":percent_format(1)}),
                       "ulr_final"                      : hx.Float(mode="output", view={"label": "ULR: Final Projected",               "format":percent_format(1)}),
                       "blended_LR"               : hx.Float(mode="output", view={"label": "ULR: Final Selected",                 "format":percent_format(1)}),
                    }),


                    "gn_pre_uw_adj"     : hx.Structure(view={"label": "GN Loss Ratio"}, children={
                       "ulr_previous"                   : hx.Float(mode="output", view={"label": "ULR: Previous",                               "format":percent_format(1)}),
                       "ulr_benchmark"                  : hx.Float(mode="output", view={"label": "ULR: Benchmark",                              "format":percent_format(1)}),
                       "ulr_experience"                 : hx.Float(mode="output", view={"label": "ULR: Experience",                             "format":percent_format(1)}),
                       "ulr_experience_weighting"       : hx.Float(mode="output", view={"label": "ULR: Experience Weighting",                   "format":percent_format(1)}),
                       "ulr_selected_ol"                : hx.Float(mode="output", view={"label": "ULR: Selected",                               "format":percent_format(1)}),
                       "ulr_uw_override"                : hx.Float(mode="output", view={"label": "ULR: Override",                               "format":percent_format(1)}),
                       "ulr_final_uw"                   : hx.Float(mode="output", view={"label": "ULR: Final UW Selected",                      "format":percent_format(1)}),
                       "ulr_actuarial_override"         : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",                     "format":percent_format(1)}),
                       "ulr_actuarial_override_output"  : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",                     "format":percent_format(1)}),
                       "ulr_final"                      : hx.Float(mode="output", view={"label": "ULR: Final Projected",               "format":percent_format(1)}),
                       "blended_LR"               : hx.Float(mode="output", view={"label": "ULR: Final Selected",                 "format":percent_format(1)}),
                    }),

                    "gg_pst_uw_adj"     : hx.Structure(view={"label": "GG Loss Ratio"}, children={
                    #    "ulr_previous"           : hx.Float(mode="output", view={"label": "ULR: Previous"}),                   #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_benchmark"          : hx.Float(mode="output", view={"label": "ULR: Benchmark"}),                  #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_experience"         : hx.Float(mode="output", view={"label": "ULR: Experience"}),                 #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_experience_weighting":hx.Float(mode="output", view={"label": "ULR: Experience Weighting"}),       #shown for completeness/uniformity here - but not able to be calc or displayed
                       "ulr_selected_ol"                : hx.Float(mode="output", view={"label": "ULR: Selected",                               "format":percent_format(1)}),
                       "ulr_uw_override"                : hx.Float(mode="input", view={"label": "ULR: Override",                               "format":percent_format(1)},    default=None,   optionality="optional"),
                       "ulr_final_uw"                   : hx.Float(mode="output", view={"label": "ULR: Final UW Selected",                      "format":percent_format(1)}),
                       "ulr_actuarial_override"         : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",                     "format":percent_format(1)}),
                       "ulr_actuarial_override_output"  : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",                     "format":percent_format(1)}),
                       "ulr_final"                      : hx.Float(mode="output", view={"label": "ULR: Projected Pst Adj",               "format":percent_format(1)}),
                       "blended_LR"               : hx.Float(mode="output", view={"label": "ULR: Projected Pre Adj",                 "format":percent_format(1)}),
                    }),

                    "gn_pst_uw_adj"     : hx.Structure(view={"label": "GN Loss Ratio"}, children={
                    #    "ulr_previous"           : hx.Float(mode="output", view={"label": "ULR: Previous"}),                   #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_benchmark"          : hx.Float(mode="output", view={"label": "ULR: Benchmark"}),                  #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_experience"         : hx.Float(mode="output", view={"label": "ULR: Experience"}),                 #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_experience_weighting":hx.Float(mode="output", view={"label": "ULR: Experience Weighting"}),       #shown for completeness/uniformity here - but not able to be calc or displayed
                       "ulr_selected_ol"                : hx.Float(mode="output", view={"label": "ULR: Selected",                               "format":percent_format(1)}),
                       "ulr_uw_override"                : hx.Float(mode="output", view={"label": "ULR: Override",                               "format":percent_format(1)}),
                       "ulr_final_uw"                   : hx.Float(mode="output", view={"label": "ULR: Final UW Selected",                      "format":percent_format(1)}),
                       "ulr_actuarial_override"         : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",                     "format":percent_format(1)}),
                       "ulr_actuarial_override_output"  : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",                     "format":percent_format(1)}),
                       "ulr_final"                      : hx.Float(mode="output", view={"label": "ULR: Projected Pst Adj",               "format":percent_format(1)}),
                       "blended_LR"               : hx.Float(mode="output", view={"label": "ULR: Projected Pre Adj",                 "format":percent_format(1)}),
                    }),

                    "uw_adjustment"     : hx.Float(mode="input", view={"label": "UW Adj  (% load/discount) (-50% to +200%)",            "format":percent_format(1)},    default=None,   optionality="optional" ),
                    "uw_override"       : hx.Bool(mode="input",  view={"label": "Turn off Loading"},                                                                    default=False),
                    "uw_rationale"      : hx.Str(mode="input", view={"label": "Rationale Required:"},                                                                   default=None,   optionality="optional", async_input=["generate_uw_rationale_doc_task"] ),

                }),



                "catastrophe"   : hx.Structure(children={
                    "gg_pre_uw_adj"                     : hx.Structure(view={"label": "GG Loss Ratio"}, children={
                       "ulr_previous_exc_nml"           : hx.Float(mode="output", view={"label": "ULR: Previous exc NML",                       "format":percent_format(1)}),
                       "ulr_previous"                   : hx.Float(mode="output", view={"label": "ULR: Previous",                               "format":percent_format(1)}),
                       "ulr_rms"                        : hx.Float(mode="output", view={"label": "ULR: RMS",                                    "format":percent_format(1)}),
                       "ulr_benchmark"                  : hx.Float(mode="output", view={"label": "ULR: Benchmark",                              "format":percent_format(1)}),
                       "ulr_experience"                 : hx.Float(mode="output", view={"label": "ULR: Experience",                             "format":percent_format(1)}),
                       "ulr_experience_weighting"       : hx.Float(mode="output", view={"label": "ULR: Experience Weighting",                   "format":percent_format(1)}),
                       "ulr_selected_ol_exc_nml"        : hx.Float(mode="output", view={"label": "ULR: Projected exc NML & Climate",             "format":percent_format(1)}),
                       "ulr_selected_ol_nml"            : hx.Float(mode="output", view={"label": "ULR: Selected NML & Climate Load",            "format":percent_format(1)}),
                       "ulr_selected_ol"                : hx.Float(mode="output", view={"label": "ULR: Selected inc NML & Climate",             "format":percent_format(1)}),
                       "ulr_uw_override"                : hx.Float(mode="output", view={"label": "ULR: Override",                               "format":percent_format(1)}),
                       "ulr_final_uw"                   : hx.Float(mode="output", view={"label": "ULR: Final UW Selected",                      "format":percent_format(1)}),
                       "ulr_actuarial_override"         : hx.Float(mode="input",  view={"label": "ULR: Actuarial Override",                     "format":percent_format(1)},    default=None,   optionality="optional" ), 
                       "ulr_actuarial_override_output"  : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",                     "format":percent_format(1)}),
                       "ulr_final"                      : hx.Float(mode="output", view={"label": "ULR: Final Projected",                         "format":percent_format(1)}),
                       "blended_LR"               : hx.Float(mode="output", view={"label": "ULR: Final Selected",                 "format":percent_format(1)}),
                    }),


                    "gn_pre_uw_adj"                     : hx.Structure(view={"label": "GN Loss Ratio"}, children={
                       "ulr_previous_exc_nml"           : hx.Float(mode="output", view={"label": "ULR: Previous exc NML",                       "format":percent_format(1)}),
                       "ulr_previous"                   : hx.Float(mode="output", view={"label": "ULR: Previous",                               "format":percent_format(1)}),
                       "ulr_rms"                        : hx.Float(mode="output", view={"label": "ULR: RMS",                                    "format":percent_format(1)}),
                       "ulr_benchmark"                  : hx.Float(mode="output", view={"label": "ULR: Benchmark",                              "format":percent_format(1)}),
                       "ulr_experience"                 : hx.Float(mode="output", view={"label": "ULR: Experience",                             "format":percent_format(1)}),
                       "ulr_experience_weighting"       : hx.Float(mode="output", view={"label": "ULR: Experience Weighting",                   "format":percent_format(1)}),
                       "ulr_selected_ol_exc_nml"        : hx.Float(mode="output", view={"label": "ULR: Projected exc NML & Climate",             "format":percent_format(1)}),
                       "ulr_selected_ol_nml"            : hx.Float(mode="output", view={"label": "ULR: Selected NML & Climate Load",            "format":percent_format(1)}),
                       "ulr_selected_ol"                : hx.Float(mode="output", view={"label": "ULR: Selected inc NML & Climate",             "format":percent_format(1)}),
                       "ulr_uw_override"                : hx.Float(mode="output", view={"label": "ULR: Override",                               "format":percent_format(1)}),
                       "ulr_final_uw"                   : hx.Float(mode="output", view={"label": "ULR: Final UW Selected",                      "format":percent_format(1)}),
                       "ulr_actuarial_override"         : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",                     "format":percent_format(1)}),
                       "ulr_actuarial_override_output"  : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",                     "format":percent_format(1)}),
                       "ulr_final"                      : hx.Float(mode="output", view={"label": "ULR: Final Projected",                         "format":percent_format(1)}),
                       "blended_LR"               : hx.Float(mode="output", view={"label": "ULR: Final Selected",                 "format":percent_format(1)}),
                    }),

                    "gg_pst_uw_adj"     : hx.Structure(view={"label": "GG Loss Ratio"}, children={
                    #    "ulr_previous_exc_nml"   : hx.Float(mode="output", view={"label": "ULR: Previous exc NML"}),           #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_previous"           : hx.Float(mode="output", view={"label": "ULR: Previous"}),                   #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_rms"                : hx.Float(mode="output", view={"label": "ULR: RMS"}),                        #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_benchmark"          : hx.Float(mode="output", view={"label": "ULR: Benchmark"}),                  #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_experience"         : hx.Float(mode="output", view={"label": "ULR: Experience"}),                 #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_experience_weighting":hx.Float(mode="output", view={"label": "ULR: Experience Weighting"}),       #shown for completeness/uniformity here - but not able to be calc or displayed
                       "ulr_selected_ol_exc_nml"        : hx.Float(mode="output", view={"label": "ULR: Projected exc NML & Climate",             "format":percent_format(1)}),
                       "ulr_selected_ol_nml"            : hx.Float(mode="output", view={"label": "ULR: Selected NML & Climate Load",            "format":percent_format(1)}),
                       "ulr_selected_ol"                : hx.Float(mode="output", view={"label": "ULR: Selected inc NML & Climate",             "format":percent_format(1)}),
                       "ulr_uw_override"                : hx.Float(mode="input", view={"label": "ULR: Override",                               "format":percent_format(1)},    default=None,   optionality="optional"),
                       "ulr_final_uw"                   : hx.Float(mode="output", view={"label": "ULR: Final UW Selected",                      "format":percent_format(1)}),
                       "ulr_actuarial_override"         : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",                     "format":percent_format(1)}),
                       "ulr_actuarial_override_output"  : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",                     "format":percent_format(1)}),
                       "ulr_final"                      : hx.Float(mode="output", view={"label": "ULR: Projected Pst Adj",                         "format":percent_format(1)}),
                       "blended_LR"               : hx.Float(mode="output", view={"label": "ULR: Projected Pre Adj",                 "format":percent_format(1)}),
                    }),

                    "gn_pst_uw_adj"     : hx.Structure(view={"label": "GN Loss Ratio"}, children={
                    #    "ulr_previous_exc_nml"   : hx.Float(mode="output", view={"label": "ULR: Previous exc NML"}),           #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_previous"           : hx.Float(mode="output", view={"label": "ULR: Previous"}),                   #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_rms"                : hx.Float(mode="output", view={"label": "ULR: RMS"}),                        #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_benchmark"          : hx.Float(mode="output", view={"label": "ULR: Benchmark"}),                  #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_experience"         : hx.Float(mode="output", view={"label": "ULR: Experience"}),                 #shown for completeness/uniformity here - but not able to be calc or displayed
                    #    "ulr_experience_weighting":hx.Float(mode="output", view={"label": "ULR: Experience Weighting"}),       #shown for completeness/uniformity here - but not able to be calc or displayed
                       "ulr_selected_ol_exc_nml"        : hx.Float(mode="output", view={"label": "ULR: Projected exc NML & Climate",             "format":percent_format(1)}),
                       "ulr_selected_ol_nml"            : hx.Float(mode="output", view={"label": "ULR: Selected NML & Climate Load",            "format":percent_format(1)}),
                       "ulr_selected_ol"                : hx.Float(mode="output", view={"label": "ULR: Selected inc NML & Climate",             "format":percent_format(1)}),
                       "ulr_uw_override"                : hx.Float(mode="output", view={"label": "ULR: Override",                               "format":percent_format(1)}),
                       "ulr_final_uw"                   : hx.Float(mode="output", view={"label": "ULR: Final UW Selected",                      "format":percent_format(1)}),
                       "ulr_actuarial_override"         : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",                     "format":percent_format(1)}),
                       "ulr_actuarial_override_output"  : hx.Float(mode="output", view={"label": "ULR: Actuarial Override",                     "format":percent_format(1)}),
                       "ulr_final"                      : hx.Float(mode="output", view={"label": "ULR: Projected Pst Adj",                         "format":percent_format(1),     "options": {"rationale": {"label": "Cat Load Pick"}}},     async_input=["generate_uw_rationale_doc_task"]),
                       "blended_LR"               : hx.Float(mode="output", view={"label": "ULR: Projected Pre Adj",                 "format":percent_format(1)}),
                    }),

                    "uw_adjustment"         : hx.Float(mode="input", view={"label": "UW Adj  (% load/discount) (-50% to +200%)",        "format":percent_format(1)},    default=None,   optionality="optional" ),
                    "uw_override"           : hx.Bool(mode="input",  view={"label": "Turn off Loading"},                                                                default=False),
                    "uw_rationale"          : hx.Str(mode="input", view={"label": "Rationale Required:"},                                                               default=None,   optionality="optional", async_input=["generate_uw_rationale_doc_task"] ),
                }),


                "total"   : hx.Structure(children={
                    "gg_pre_uw_adj"             : hx.Structure(view={"label": "GG Pre\nUW adj"}, children={
                       "ulr_priced_final"           : hx.Float(mode="output", view={"label": "ULR: Final Selected",                          "format":percent_format(1)}),
                       

                    }),

                    "pre_uw_adj"     : hx.Structure(view={"label": "Pre\nUW adj"}, children={
                        "comb_ratio_exc_pc"      : hx.Float(mode="output", view={"label": "Combined Ratio (exc PC)",          "format":percent_format(1)}, async_input=["generate_uw_rationale_doc_task"]),
                        "comb_ratio_inc_pc"      : hx.Float(mode="output", view={"label": "Combined Ratio (inc PC)",          "format":percent_format(1)}, async_input=["generate_uw_rationale_doc_task"]),

}),
                    "pst_uw_adj"     : hx.Structure(view={"label": "Pst\nUW adj"}, children={
                        "comb_ratio_exc_pc"      : hx.Float(mode="output", view={"label": "Combined Ratio (exc PC)",          "format":percent_format(1)}, async_input=["generate_uw_rationale_doc_task"]),
                        "comb_ratio_inc_pc"      : hx.Float(mode="output", view={"label": "Combined Ratio (inc PC)",          "format":percent_format(1)} ,async_input=["generate_uw_rationale_doc_task"]),

}),


                    "gn_pre_uw_adj"     : hx.Structure(view={"label": "GN Pre\nUW adj"}, children={
                       "ulr_priced_final_exc_pc" : hx.Float(mode="output", view={"label": "ULR: Final Selected (not Net of PC)",        "format":percent_format(1)}),
                       "ulr_priced_final_inc_pc" : hx.Float(mode="output", view={"label": "ULR: Final Selected (Net of PC)",            "format":percent_format(1)}),
                       "ulr_bench"               : hx.Float(mode="output", view={"label": "ULR: Benchmark",                             "format":percent_format(1)}),
                       "ulr_plan"                : hx.Float(mode="output", view={"label": "ULR: Business Plan",                         "format":percent_format(1)}),
                       "ulr_prior"               : hx.Float(mode="output", view={"label": "ULR: Prior",                                 "format":percent_format(1)}),
                       
}),

                    "gg_pst_uw_adj"     : hx.Structure(view={"label": "GG Post\nUW adj"}, children={
                       "ulr_priced_final"        : hx.Float(mode="output", view={"label": "ULR: Final Selected",                        "format":percent_format(1)}),
                    }),

                    "gn_pst_uw_adj"     : hx.Structure(view={"label": "GN Post\nUW adj"}, children={
                       "ulr_priced_final_exc_pc" : hx.Float(mode="output", view={"label": "ULR: Final Selected (not Net of PC)",        "format":percent_format(1)}),
                       "ulr_priced_final_inc_pc" : hx.Float(mode="output", view={"label": "ULR: Final Selected (Net of PC)",            "format":percent_format(1)}),
                       "ulr_bench"               : hx.Float(mode="output", view={"label": "ULR: Benchmark",                             "format":percent_format(1)}),
                       "ulr_plan"                : hx.Float(mode="output", view={"label": "ULR: Business Plan",                         "format":percent_format(1)}),
                       "ulr_prior"               : hx.Float(mode="output", view={"label": "ULR: Prior",                                 "format":percent_format(1)}),
                       
}),

                    "uw_adjustment"         : hx.Float(mode="output", view={"label": "Overall Implied UW Adj",                          "format":percent_format(1)}),

                }),

            }),


            "technical"   : hx.Structure(children={

                "amts_pre_uw_adj"     : hx.Structure(view={"label": "Pre\nUW adj"}, children={
                    "losses_att_afb"             : hx.Float(mode="output", view={"label": "Losses - Attritional",                           "format":thousands_format(0)}),
                    "losses_lrg_afb"             : hx.Float(mode="output", view={"label": "Losses - Shock",                                 "format":thousands_format(0)}),
                    "losses_cat_afb"             : hx.Float(mode="output", view={"label": "Losses - Cat",                                   "format":thousands_format(0)}),
                    "losses_tot_afb"             : hx.Float(mode="output", view={"label": "Losses - Total",                                 "format":thousands_format(0)}),
                    "lae_afb"                    : hx.Float(mode="output", view={"label": "Costs - LAE",                                    "format":thousands_format(0)}),
                    "expense_afb"                : hx.Float(mode="output", view={"label": "Costs - Expenses",                               "format":thousands_format(0)}),
                    "reinsurance_afb"            : hx.Float(mode="output", view={"label": "Costs - Reinsurance",                            "format":thousands_format(0)}),
                    "investment_afb"             : hx.Float(mode="output", view={"label": "Investment Income",                              "format":thousands_format(0)}),
                    "profit_req_afb"             : hx.Float(mode="output", view={"label": "Profit Required",                                "format":thousands_format(0)}),
                    "aqn_comm_afb"               : hx.Float(mode="output", view={"label": "Acqn - Commission",                              "format":thousands_format(0)}),
                    "aqn_brok_afb"               : hx.Float(mode="output", view={"label": "Acqn - Brokerage",                               "format":thousands_format(0)}),
                    "aqn_iptax_afb"              : hx.Float(mode="output", view={"label": "Acqn - IPT",                                     "format":thousands_format(0)}),
                    "aqn_total"       : hx.Float(mode="output", view={"label": "Acqn - Total",                            "format":thousands_format(0)}),
                    "aqn_pc_afb"                 : hx.Float(mode="output", view={"label": "Acqn - PC",                                      "format":thousands_format(0)}),
                    "aqn_total_inc_pc_afb"       : hx.Float(mode="output", view={"label": "Acqn - Total inc PC",                            "format":thousands_format(0)}),

                    "gn_premium_tech_inc_pc_afb"     : hx.Float(mode="output", view={"label": "Technical Premium - AFB - GN - net of PC",   "format":thousands_format(0)}),
                    "gn_premium_tech_exc_pc_afb"     : hx.Float(mode="output", view={"label": "Technical Premium - AFB - GN - gross of PC", "format":thousands_format(0)}),
                    "gg_premium_tech_afb"            : hx.Float(mode="output", view={"label": "Technical Premium - AFB - GG",               "format":thousands_format(0)}),
                    "gn_premium_tech_inc_pc_100_pct" : hx.Float(mode="output", view={"label": "Technical Premium - 100% - GN - net of PC",  "format":thousands_format(0)}),
                    "gn_premium_tech_exc_pc_100_pct" : hx.Float(mode="output", view={"label": "Technical Premium - 100% - GN - gross of PC","format":thousands_format(0)}),
                    "gg_premium_tech_100_pct"        : hx.Float(mode="output", view={"label": "Technical Premium - 100% - GG",              "format":thousands_format(0)}),

                    "gn_premium_bench_inc_pc_afb"    : hx.Float(mode="output", view={"label": "Benchmark Premium - AFB - GN - net of PC",   "format":thousands_format(0)}),
                    "gn_premium_bench_exc_pc_afb"    : hx.Float(mode="output", view={"label": "Benchmark Premium - AFB - GN - gross of PC", "format":thousands_format(0)}),
                    "gg_premium_bench_afb"           : hx.Float(mode="output", view={"label": "Benchmark Premium - AFB - GG",               "format":thousands_format(0)}),
                    "gn_premium_bench_inc_pc_100_pct": hx.Float(mode="output", view={"label": "Benchmark Premium - 100% - GN - net of PC",  "format":thousands_format(0)}),
                    "gn_premium_bench_exc_pc_100_pct": hx.Float(mode="output", view={"label": "Benchmark Premium - 100% - GN - gross of PC","format":thousands_format(0)}),
                    "gg_premium_bench_100_pct"       : hx.Float(mode="output", view={"label": "Benchmark Premium - 100% - GG",              "format":thousands_format(0)}),

                }),


                "amts_pst_uw_adj"     : hx.Structure(view={"label": "Pst\nUW adj"}, children={
                    "losses_att_afb"             : hx.Float(mode="output", view={"label": "Losses - Attritional",                           "format":thousands_format(0)}),
                    "losses_lrg_afb"             : hx.Float(mode="output", view={"label": "Losses - Shock",                                 "format":thousands_format(0)}),
                    "losses_cat_afb"             : hx.Float(mode="output", view={"label": "Losses - Cat",                                   "format":thousands_format(0)}),
                    "losses_tot_afb"             : hx.Float(mode="output", view={"label": "Losses - Total",                                 "format":thousands_format(0)}),
                    "lae_afb"                    : hx.Float(mode="output", view={"label": "Costs - LAE",                                    "format":thousands_format(0)}),
                    "expense_afb"                : hx.Float(mode="output", view={"label": "Costs - Expenses",                               "format":thousands_format(0)}),
                    "reinsurance_afb"            : hx.Float(mode="output", view={"label": "Costs - Reinsurance",                            "format":thousands_format(0)}),
                    "investment_afb"             : hx.Float(mode="output", view={"label": "Investment Income",                              "format":thousands_format(0)}),
                    "profit_req_afb"             : hx.Float(mode="output", view={"label": "Profit Required (CoC)",                          "format":thousands_format(0)}),
                    "aqn_comm_afb"               : hx.Float(mode="output", view={"label": "Acqn - Commission",                              "format":thousands_format(0)}),
                    "aqn_brok_afb"               : hx.Float(mode="output", view={"label": "Acqn - Brokerage",                               "format":thousands_format(0)}),
                    "aqn_iptax_afb"              : hx.Float(mode="output", view={"label": "Acqn - IPT",                                     "format":thousands_format(0)}),
                    "aqn_total"       : hx.Float(mode="output", view={"label": "Acqn - Total",                            "format":thousands_format(0)}),
                    "aqn_pc_afb"                 : hx.Float(mode="output", view={"label": "Acqn - PC",                                      "format":thousands_format(0)}),
                    "aqn_total_inc_pc_afb"       : hx.Float(mode="output", view={"label": "Acqn - Total inc PC",                            "format":thousands_format(0)}),

                    "gn_premium_tech_inc_pc_afb"     : hx.Float(mode="output", view={"label": "Technical Premium - AFB - GN - net of PC",   "format":thousands_format(0)}),
                    "gn_premium_tech_exc_pc_afb"     : hx.Float(mode="output", view={"label": "Technical Premium - AFB - GN - gross of PC", "format":thousands_format(0)}),
                    "gg_premium_tech_afb"            : hx.Float(mode="output", view={"label": "Technical Premium - AFB - GG",               "format":thousands_format(0)}),
                    "gn_premium_tech_inc_pc_100_pct" : hx.Float(mode="output", view={"label": "Technical Premium - 100% - GN - net of PC",  "format":thousands_format(0)}),
                    "gn_premium_tech_exc_pc_100_pct" : hx.Float(mode="output", view={"label": "Technical Premium - 100% - GN - gross of PC","format":thousands_format(0)}),
                    "gg_premium_tech_100_pct"        : hx.Float(mode="output", view={"label": "Technical Premium - 100% - GG",              "format":thousands_format(0)}),

                    "gn_premium_bench_inc_pc_afb"    : hx.Float(mode="output", view={"label": "Benchmark Premium - AFB - GN - net of PC",   "format":thousands_format(0)}),
                    "gn_premium_bench_exc_pc_afb"    : hx.Float(mode="output", view={"label": "Benchmark Premium - AFB - GN - gross of PC", "format":thousands_format(0)}),
                    "gg_premium_bench_afb"           : hx.Float(mode="output", view={"label": "Benchmark Premium - AFB - GG",               "format":thousands_format(0)}),
                    "gn_premium_bench_inc_pc_100_pct": hx.Float(mode="output", view={"label": "Benchmark Premium - 100% - GN - net of PC",  "format":thousands_format(0)}),
                    "gn_premium_bench_exc_pc_100_pct": hx.Float(mode="output", view={"label": "Benchmark Premium - 100% - GN - gross of PC","format":thousands_format(0)}),
                    "gg_premium_bench_100_pct"       : hx.Float(mode="output", view={"label": "Benchmark Premium - 100% - GG",              "format":thousands_format(0)}),
                }),

                "gn_premium_quoted_inc_pc_afb"      : hx.Float(mode="output", view={"label": "Quoted Premium - AFB - GN - net of PC",       "format":thousands_format(0)}),
                "gn_premium_quoted_exc_pc_afb"      : hx.Float(mode="output", view={"label": "Quoted Premium - AFB - GN - gross of PC",     "format":thousands_format(0)}),
                "gg_premium_quoted_afb"             : hx.Float(mode="output", view={"label": "Quoted Premium - AFB - GG",                   "format":thousands_format(0)}),
                "gn_premium_quoted_inc_pc_100_pct"  : hx.Float(mode="output", view={"label": "Quoted Premium - 100% - GN - net of PC",      "format":thousands_format(0)}),
                "gn_premium_quoted_exc_pc_100_pct"  : hx.Float(mode="output", view={"label": "Quoted Premium - 100% - GN - gross of PC",    "format":thousands_format(0)}),
                "gg_premium_quoted_100_pct"         : hx.Float(mode="output", view={"label": "Quoted Premium - 100% - GG",                  "format":thousands_format(0)}),

                "percent_pc"            : hx.Float(mode="output", view={"label": "Calculated Avg PC Payable as a % of GG EPI",              "format":percent_format(2)},        async_input=["generate_uw_rationale_doc_task"]),
                "percent_pc_prior"      : hx.Float(mode="output", view={"label": "Calculated Avg PC Payable as a % of GG EPI - Previous",   "format":percent_format(2)}),
                "amount_pc_100"         : hx.Float(mode="output", view={"label": "Modelled PC - 100%",                                      "format":thousands_format(0)},      async_input=["generate_uw_rationale_doc_task"]),
                "amount_pc_afb"         : hx.Float(mode="output", view={"label": "Modelled PC - AFB ",                                      "format":thousands_format(0)}),

            }),

            "loss_ratio_summary_blended"   : hx.Structure(children={
            **{
                f"{adj}"                            : hx.Structure(view={"label": f"{label}"},children={
                    "gg_priced_final_ulr"               : hx.Float(mode="output", view={"label": "GG ULR: Final Selected",               "format":percent_format(1)}),
                    "gn_ulr_bench"                  : hx.Float(mode="output", view={"label": "GN ULR Benchmark",                     "format":percent_format(1)}),
                    "gn_ulr_plan"                   : hx.Float(mode="output", view={"label": "GN ULR Business Plan",                 "format":percent_format(1)}),
                    "gn_ulr_priced_final_exc_pc"    : hx.Float(mode="output", view={"label": "ULR: Final Selected (not Net of PC)",  "format":percent_format(1)}),
                    "gn_ulr_priced_final_inc_pc"    : hx.Float(mode="output", view={"label": "ULR: Final Selected (Net of PC)",      "format":percent_format(1)}),
                    "ULR_prior"                     : hx.Float(mode="output", view={"label": "ULR: Prior",                           "format":percent_format(1)}),
                    "comb_ratio_exc_pc"            : hx.Float(mode="output", view={"label": "Combined Ratio (excl pc)",  "format":percent_format(1)}),
                    "comb_ratio_inc_pc"   : hx.Float(mode="output", view={"label": "Combined Ratio (incl pc)",  "format":percent_format(1)}),
})
            for adj, label in zip (["pre_uw_adj", "post_uw_adj"] ,["Pre\nUW adj", "Post\nUW adj"])
            }
            }),

            "kpi"   : hx.Structure(children={
                "pre_uw_adj"                        : hx.Structure(view={"label": "Pre\nUW adj"}, children={
                    "expected_profit"               : hx.Float(mode="output", view={"label": "Expected Profit",                             "format":thousands_format(0)}),
                    "allocated_capital"             : hx.Float(mode="output", view={"label": "Allocated Capital",                           "format":thousands_format(0)}),
                    "roc"                           : hx.Float(mode="output", view={"label": "RoC (Profit/Allocated Capital)",              "format":percent_format(1)}),
                    "bpi"                           : hx.Float(mode="output", view={"label": "BPI",                                         "format":percent_format(1)}),
                    "tpi"                           : hx.Float(mode="output", view={"label": "TPI",                                         "format":percent_format(1)}),
                    "bpi_prior"                     : hx.Float(mode="output", view={"label": "BPI Prior",                                   "format":percent_format(1)}),
                    "tpi_prior"                     : hx.Float(mode="output", view={"label": "TPI Prior",                                   "format":percent_format(1)}),
                }),

                "pst_uw_adj"     : hx.Structure(view={"label": "Post\nUW adj"}, children={
                    "expected_profit"               : hx.Float(mode="output", view={"label": "Expected Profit",                             "format":thousands_format(0)}),
                    "allocated_capital"             : hx.Float(mode="output", view={"label": "Allocated Capital",                           "format":thousands_format(0)}),
                    "roc"                           : hx.Float(mode="output", view={"label": "RoC (Profit/Allocated Capital)",              "format":percent_format(1)},    async_input=["generate_uw_rationale_doc_task"]),
                    "bpi"                           : hx.Float(mode="output", view={"label": "BPI",                                         "format":percent_format(1)},    async_input=["generate_uw_rationale_doc_task"]),
                    "tpi"                           : hx.Float(mode="output", view={"label": "TPI",                                         "format":percent_format(1)},    async_input=["generate_uw_rationale_doc_task"]),
                    "bpi_prior"                     : hx.Float(mode="output", view={"label": "BPI Prior",                                   "format":percent_format(1)}),
                    "tpi_prior"                     : hx.Float(mode="output", view={"label": "TPI Prior",                                   "format":percent_format(1)}),
                }),

                "case_priced"      : hx.Structure(view={"label": "Case Priced"}, children={
                    "gg_att_ulr"                            : hx.Float(mode="input", view={"label": "Case Priced GG Att ULR",                      "format":percent_format(1)}, default=None, optionality="optional"),
                    "gg_lrg_ulr"                            : hx.Float(mode="input", view={"label": "Case Priced GG Large Loss ULR",               "format":percent_format(1)}, default=None, optionality="optional"),
                    "gg_cat_ulr"                            : hx.Float(mode="input", view={"label": "Case Priced GG Cat ULR",                      "format":percent_format(1)}, default=None, optionality="optional"),
                    "bpi"                                   : hx.Float(mode="input", view={"label": "Case Priced BPI",                             "format":percent_format(1)}, default=None, optionality="optional"),
                    "tpi"                                   : hx.Float(mode="input", view={"label": "Case Priced TPI",                             "format":percent_format(1)}, default=None, optionality="optional"),
                    "show_case_pricing_input_section"       : hx.Bool(mode="output", view={"label": "Show basis"}),
                }),

            }),

            "kpi_experience_exposure_blend"   : hx.Structure(children={
                "pre_uw_adj"                        : hx.Structure(view={"label": "Pre\nUW adj"}, children={
                    "expected_profit"               : hx.Float(mode="output", view={"label": "Expected Profit",                             "format":thousands_format(0)}),
                    "allocated_capital"             : hx.Float(mode="output", view={"label": "Allocated Capital",                           "format":thousands_format(0)}),
                    "roc"                           : hx.Float(mode="output", view={"label": "RoC (Profit/Allocated Capital)",              "format":percent_format(1)}),
                    "bpi"                           : hx.Float(mode="output", view={"label": "BPI",                                         "format":percent_format(1)}),
                    "tpi"                           : hx.Float(mode="output", view={"label": "TPI",                                         "format":percent_format(1)}),
                    "bpi_prior"                     : hx.Float(mode="output", view={"label": "BPI Prior",                                   "format":percent_format(1)}),
                    "tpi_prior"                     : hx.Float(mode="output", view={"label": "TPI Prior",                                   "format":percent_format(1)}),
                }),

                "post_uw_adj"     : hx.Structure(view={"label": "Post\nUW adj"}, children={
                    "expected_profit"               : hx.Float(mode="output", view={"label": "Expected Profit",                             "format":thousands_format(0)}),
                    "allocated_capital"             : hx.Float(mode="output", view={"label": "Allocated Capital",                           "format":thousands_format(0)}),
                    "roc"                           : hx.Float(mode="output", view={"label": "RoC (Profit/Allocated Capital)",              "format":percent_format(1)}),
                    "bpi"                           : hx.Float(mode="output", view={"label": "BPI",                                         "format":percent_format(1)}),
                    "tpi"                           : hx.Float(mode="output", view={"label": "TPI",                                         "format":percent_format(1)}),
                    "bpi_prior"                     : hx.Float(mode="output", view={"label": "BPI Prior",                                   "format":percent_format(1)}),
                    "tpi_prior"                     : hx.Float(mode="output", view={"label": "TPI Prior",                                   "format":percent_format(1)}),
                }),

            }),


            "chart_premium_breakdown" : hx.Structure(children={
                #add options column for 2 rows below , options_table="yes_no_list", options_column="YesNo"
                "uw_adj_basis"  : hx.Str(mode="input", options=["Post","Pre"], view={"label": "Select UW Adjustment Basis"}, default="Post"),
                "premium_basis" : hx.Str(mode="input",default="Gross Gross", options=basis_list, view={"label": "Select Premium Basis"}),
                "title_string"  : hx.Str(mode="output", view={"label": ""}),
                
                "technical"                         : hx.Structure(view={"label": "Technical"}, children={
                    "client_premium"                : hx.Float(mode="output", view={"label": "Client Premium"}),
                    "losses"                        : hx.Float(mode="output", view={"label": "EL"}),
                    "reinsurance"                   : hx.Float(mode="output", view={"label": "RI"}),
                    "cost_of_capital"               : hx.Float(mode="output", view={"label": "CoC"}),
                    "expense"                       : hx.Float(mode="output", view={"label": "Expense (Incl. Inv.)"}),
                    "bp_loading"                    : hx.Float(mode="output", view={"label": "BP Loading"}),
                    "brokerage"                     : hx.Float(mode="output", view={"label": "Brokerage"}),
                    "metric"                        : hx.Str(mode="output", view={"label": "TPI"}),
                    "metric_string"                 : hx.Str(mode="output", view={"label": ""}),
                }),
                  
                "tp_exposure_weights_pre_uw"                         : hx.Structure(children={
                    "exposure_prem_upscale"                          : hx.Float(mode="output", async_output=["run_bordereau_rater_task"]),
                    "brokerage"                                      : hx.Float(mode="output", async_output=["run_bordereau_rater_task"]),
                    "coc"                                            : hx.Float(mode="output", async_output=["run_bordereau_rater_task"]),
                    "direct_expense"                                 : hx.Float(mode="output", async_output=["run_bordereau_rater_task"]),
                    "indirect_expense"                               : hx.Float(mode="output", async_output=["run_bordereau_rater_task"]),
                    "lae"                                            : hx.Float(mode="output", async_output=["run_bordereau_rater_task"]),
                    "ri_cost"                                        : hx.Float(mode="output", async_output=["run_bordereau_rater_task"]),
                    "sd_load"                                        : hx.Float(mode="output", async_output=["run_bordereau_rater_task"]),
                    "nmp_load"                                       : hx.Float(mode="output", async_output=["run_bordereau_rater_task"]),
                    "investment_income"                              : hx.Float(mode="output", async_output=["run_bordereau_rater_task"]),
                }),      

                "tp_exposure_experience_blend"                       : hx.Structure(children={
                        "client_premium"                             : hx.Float(mode="output", view={"label": "Client Premium"}),
                        "expected_loss"                              : hx.Float(mode="output", view={"label": "Expected Loss"}),
                        "coc"                                        : hx.Float(mode="output", view={"label": "Cost of Capital"}),
                        "direct_expense"                             : hx.Float(mode="output", view={"label": "Direct Expenses"}),
                        "indirect_expense"                           : hx.Float(mode="output", view={"label": "Indirect Expenses"}),
                        "lae"                                        : hx.Float(mode="output", view={"label": "Loss Adjustment Expenses"}),
                        "ri_cost"                                    : hx.Float(mode="output", view={"label": "RI Cost"}),
                        "sd_load"                                    : hx.Float(mode="output", view={"label": "SD Loadings"}),
                        "nmp_load"                                   : hx.Float(mode="output", view={"label": "SD Loadings"}),
                        "bp_loading"                                 : hx.Float(mode="output", view={"label": "BP Loading"}),
                        "brokerage"                                  : hx.Float(mode="output", view={"label": "Brokerage"}),
                        "investment_income"                          : hx.Float(mode="output", view={"label": "Investment Income"}),
                }),  

                "bp_exposure_experience_blend" : hx.Structure(children={
                        "client_premium"       : hx.Float(mode="output", view={"label": "Client Premium"}),
                        "expected_loss"        : hx.Float(mode="output", view={"label": "Expected Loss"}),
                        "brokerage"            : hx.Float(mode="output", view={"label": "Brokerage"}),
                        "bp_loading"           : hx.Float(mode="output", view={"label": "BP Loading"}),
                }),
                "client_exposure_experience_blend"  : hx.Structure(view={"label": "Client"}, children={
                    "client_premium"                : hx.Float(mode="output", view={"label": "Client Premium"}),
                    "losses"                        : hx.Float(mode="output", view={"label": "EL"}),
                    "reinsurance"                   : hx.Float(mode="output", view={"label": "RI"}),
                    "cost_of_capital"               : hx.Float(mode="output", view={"label": "CoC"}),
                    "expense"                       : hx.Float(mode="output", view={"label": "Expense"}),
                    "bp_loading"                    : hx.Float(mode="output", view={"label": "BP Loading"}),
                    "brokerage"                     : hx.Float(mode="output", view={"label": "Brokerage"}),
                    "metric"                        : hx.Str(mode="output", view={"label": ""}),
                }),   

                "benchmark"                         : hx.Structure(view={"label": "Benchmark"}, children={
                    "client_premium"                : hx.Float(mode="output", view={"label": "Client Premium"}),
                    "losses"                        : hx.Float(mode="output", view={"label": "EL"}),
                    "reinsurance"                   : hx.Float(mode="output", view={"label": "RI"}),
                    "cost_of_capital"               : hx.Float(mode="output", view={"label": "CoC"}),
                    "expense"                       : hx.Float(mode="output", view={"label": "Expense"}),
                    "bp_loading"                    : hx.Float(mode="output", view={"label": "BP Loading"}),
                    "brokerage"                     : hx.Float(mode="output", view={"label": "Brokerage"}),
                    "metric"                        : hx.Str(mode="output", view={"label": "BPI"}),
                    "metric_string"                 : hx.Str(mode="output", view={"label": ""}),
                }),               

                "client"                            : hx.Structure(view={"label": "Client"}, children={
                    "client_premium"                : hx.Float(mode="output", view={"label": "Client Premium"}),
                    "losses"                        : hx.Float(mode="output", view={"label": "EL"}),
                    "reinsurance"                   : hx.Float(mode="output", view={"label": "RI"}),
                    "cost_of_capital"               : hx.Float(mode="output", view={"label": "CoC"}),
                    "expense"                       : hx.Float(mode="output", view={"label": "Expense"}),
                    "bp_loading"                    : hx.Float(mode="output", view={"label": "BP Loading"}),
                    "brokerage"                     : hx.Float(mode="output", view={"label": "Brokerage"}),
                    "metric"                        : hx.Str(mode="output", view={"label": ""}),
                }),     

                "exposure_experience_prem_blend"        : hx.Structure(children = {
                **{
                f"{adj}"                                : hx.Structure(           view={"label": f"{label}"}, children={
                    "gn_premium_tech_inc_pc_afb"                     : hx.Float(mode="output", view={"label": "Technical Premium - AFB - GN - net of PC",             "format": thousands_format()}),
                    "gg_premium_tech_afb"                            : hx.Float(mode="output", view={"label": "Technical Premium - AFB - GG",                         "format": thousands_format(0)}),
                    "gn_premium_bench_inc_pc_afb"                    : hx.Float(mode="output", view={"label": "Benchmark Premium - AFB - GN - net of PC",             "format": thousands_format(0)}),
                    "gg_premium_bench_afb"                           : hx.Float(mode="output", view={"label": "Benchmark Premium - AFB - GG",                         "format": thousands_format(0)}),
                    "combined_operating_ratio"                       : hx.Float(mode="output", view={"label": "Combined Operating Ratio",                             "format": percent_format(2)}),
                    "combined_operating_ratio_inc_pc" : hx.Float(mode="output", view={"label": "Combined Operating Ratio Inc PC", "format": percent_format(2)}),
                    "losses_tot_afb"                                 : hx.Float(mode="output", view={"label": "Losses - Total",                                       "format": thousands_format(0)}),
                    "expense_afb"                                    : hx.Float(mode="output", view={"label": "Costs - Expenses",                                      "format": thousands_format(0)}),
                    "investment_afb"                                 : hx.Float(mode="output", view={"label": "Investment Income",                                     "format": thousands_format(0)}),
                    "profit_req_afb"                                 : hx.Float(mode="output", view={"label": "Profit Required",                                       "format": thousands_format(0)}),
                    "aqn_comm_afb"                                   : hx.Float(mode="output", view={"label": "Acqn - Commission",                                     "format":thousands_format(0)}),
                    "aqn_brok_afb"                                   : hx.Float(mode="output", view={"label": "Acqn - Brokerage",                                      "format":thousands_format(0)}),
                    "aqn_iptax_afb"                                  : hx.Float(mode="output", view={"label": "Acqn - IPT",                                            "format":thousands_format(0)}),
                    "aqn_total_exc_pc_afb"                           : hx.Float(mode="output", view={"label": "Acqn - Total exc PC",                                   "format":thousands_format(0)}),
                    "aqn_pc_afb"                                     : hx.Float(mode="output", view={"label": "Acqn - PC",                                             "format":thousands_format(0)}),
                })
                for adj, label in zip(["pre_uw_adj", "post_uw_adj"], ["Pre\nUW adj", "Post\nUW adj"])
                }
                })          

            }),
 
            "standard_deviation"             : hx.Structure(children={
                "attritional"                : hx.Float(mode="output", view={"label": "Standard Dev - Attritional"}),
                "large"                      : hx.Float(mode="output", view={"label": "Standard Dev - Large"}),
                "catastrophe"                : hx.Float(mode="output", view={"label": "Standard Dev - Catastrophe"}),
            }),



        })
    })

    ############################ UW Adjustments #############################
    cds.extend_node_rater_defined(f"cds", {
        "exposure_adj"                : hx.Structure(children={
        **{
            f"{peril.lower()}"        : hx.Structure(view={"label": f"{peril}"}, children={
                
                 "exp_loss"            : hx.Float(mode="output",                                     view={"label": "Expected Loss",   "format": thousands_format()},     async_output=["run_bordereau_rater_task"]),
                "pre_uw_adj_gg_ulr"   : hx.Float(mode="input",  default=None  ,   optionality="optional",                    view={"label": "GG ULR",   "format": percent_format(2),"read_only": True},      async_output=["run_bordereau_rater_task"]),
                "pre_uw_adj_gn_ulr"   : hx.Float(mode="input",  default=None   ,   optionality="optional",                     view={"label": "GN ULR",     "format": percent_format(2),"read_only": True},     async_output=["run_bordereau_rater_task"]),
                "ulr_adjustment"      : hx.Float(mode="input", default=0, optionality="optional",   view={"label": "ULR Adjustment",  "info": "Adjustments should be between -50% and +200%", "format": percent_format(2)}),
                "post_uw_adj_gn_ulr"  : hx.Float(mode="output",                                     view={"label": "GN Adjusted ULR",                                                         "format": percent_format(2)}),
            })
        for peril in ("Att_and_Large", "Cat")
        }
        })
    })

    cds.extend_node_rater_defined("cds", {
        "exposure_experience_weights"  : hx.Structure(children={
            "exposure_rating"        : hx.Structure(view={"label": "Exposure\nRating"}, children={
                "pre_uw_adj_gg_ulr"   : hx.Float(mode="output",                                       view={"label": "GG ULR",             "format": percent_format(2)}),
                "pre_uw_adj_gn_ulr"   : hx.Float(mode="output",                                       view={"label": "GN ULR",             "format": percent_format(2)}),
                "ulr_adjustment"      : hx.Float(mode="output",                                       view={"label": "ULR Adjustment",     "format": percent_format(2)}),
                "post_uw_adj_gg_ulr"  : hx.Float(mode="output",                                       view={"label": "GG Adjusted ULR",    "format": percent_format(2)}),
                "post_uw_adj_gn_ulr"  : hx.Float(mode="output",                                       view={"label": "GN Adjusted ULR",    "format": percent_format(2)}),
                "sugg_weight"         : hx.Float(mode="output",                                       view={"label": "Suggested\nWeights", "format": percent_format(2)}),
                "sel_weight"          : hx.Float(mode="input", default=None, optionality="optional",  view={"label": "Selected\nWeights",  "format": percent_format(2)}),
                "final_weight"        : hx.Float(mode="output",                                       view={"label": "Final\nWeights",     "format": percent_format(2)}),
            }),
            "experience_rating"       : hx.Structure(view={"label": "Experience\nRating"}, children={
                "pre_uw_adj_gg_ulr"   : hx.Float(mode="output",                                       view={"label": "GG ULR",             "format": percent_format(2)}),
                "pre_uw_adj_gn_ulr"   : hx.Float(mode="output",                                       view={"label": "GN ULR",             "format": percent_format(2)}),
                "ulr_adjustment"      : hx.Float(mode="output",                                       view={"label": "ULR Adjustment",     "format": percent_format(2)}),
                "post_uw_adj_gg_ulr"  : hx.Float(mode="output",                                       view={"label": "GG Adjusted ULR",    "format": percent_format(2)}),
                "post_uw_adj_gn_ulr"  : hx.Float(mode="output",                                       view={"label": "GN Adjusted ULR",    "format": percent_format(2)}),
                "sugg_weight"         : hx.Float(mode="output",                                       view={"label": "Suggested\nWeights", "format": percent_format(2)}),
                "sel_weight"          : hx.Float(mode="output",                                       view={"label": "Selected\nWeights",  "format": percent_format(2)}),
                "final_weight"        : hx.Float(mode="output",                                       view={"label": "Final\nWeights",     "format": percent_format(2)}),
            }),

            "gn_final_ulr"             : hx.Float(mode="output",       view={"label": "GN Final\nULR",      "format": percent_format(2)} ),
        })
    })

    cds.extend_node_rater_defined("cds", {
        "exposure_rating": hx.Structure(children = {
        **{
            f"{adj}"                         : hx.Structure(children={
                "beazley_share_gn_tp"        : hx.Float(mode="output", view={"label": "Gross Tech Prem Total",       "format": thousands_format()},   async_output=["run_bordereau_rater_task"]),
                "bp"                         : hx.Float(mode="output", view={"label": "Gross Benchmark Prem",        "format": thousands_format(0)}),
                "expected_loss"              : hx.Float(mode="output", view={"label": "Expected Loss",               "format": thousands_format(0)}),
                "elr"                        : hx.Float(mode="output", view={"label": "ELR",                         "format": percent_format(1)}),
                "net_tech_prem_total"        : hx.Float(mode="output", view={"label": "Net Tech Prem Total",         "format": thousands_format(0)}),
                "tpi"                        : hx.Float(mode="output", view={"label": "TPI",                         "format": percent_format(1)}),
                "bpi"                        : hx.Float(mode="output", view={"label": "BPI",                         "format": percent_format(1)}),
            })
        for adj in ("pre_uw_adj", "post_uw_adj")
        }
        })
    })

    cds.extend_node_rater_defined("cds", {
        "gg_received_beazley_share_exposure_prem"        : hx.Float(mode="output", view={"label": "Gross Received (Exposure) Premium"},              async_output=["run_bordereau_rater_task"])
    }) 


   ########################### end of uw Adjustments #############################

