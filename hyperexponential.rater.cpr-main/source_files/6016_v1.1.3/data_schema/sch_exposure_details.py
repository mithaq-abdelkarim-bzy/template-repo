#########################################################################################################
########################################### Outstanding Items ###########################################
#########################################################################################################
### 1) 
### 2) 
### 2) 
### 4)
### 5) 
### 6) 
### 7) 
### 8) 
### 9) 
#########################################################################################################



import hx_data_schema as hx
import data_schema.sch_utilities as utils
import data_schema.sch_tooltips as tips

# Replace / remove examples with your models exposures

def sch_exposure_details(cds):
    
    # # For aggregate exposure e.g. total revenue, sum insured etc. please add to the aggregate exposures node
    # cds.extend_node_rater_defined("cds/exposure/aggregate", {
    #     # PLACEHOLDER value used in experience rating, the experience rating should connect to the total exposure value of the model
        
    # })

    cds.extend_node_rater_defined("cds/exposure/granular", {
        "crcf"  : hx.Structure(children={

            "sum_insured":                  hx.Float(mode="output",                                       view={"label": "Gross Sum Insured",       "format": utils.thousands_format(0),        "info" : tips.tip_ed01}),
            "indemnity":                    hx.Float(mode="input",  default=None, optionality="optional", view={"label": "Indemnity (%)",           "format": utils.percent_format(0),          "info" : tips.tip_ed02}),
            "waiting_period":               hx.Float(mode="input",  default=None, optionality="optional", view={"label": "Waiting Period (d)",      "format": utils.thousands_format(0)}),
            "pre_shipment_risk":            hx.Str(  mode="input",  default="No",                         view={"label": "Pre-Shipment Risk"},          options_column="YesNo", options_table="lst_yn"),
            "pre_shipment_risk_show_hide":  hx.Bool( mode="output"),
            "pre_shipment_amt":             hx.Float(mode="input",  default=None, optionality="optional", view={"label": "Pre-Shipment Percent",    "format": utils.percent_format(0)}),
            "pst_shipment_amt":             hx.Float(mode="output",                                       view={"label": "Post-Shipment Percent",   "format": utils.percent_format(0)}),

            # used in setting up the exposure profile automatically
            "load_amt_basis":               hx.Str(  mode="input", default="Step",optionality="optional", view={"label": "Amount at Risk - basis"},  options_table="lst_amount_at_risk",  options_column="Amount at Risk"),

            "load_amt_flat":                hx.Float(mode="input",  default=None, optionality="optional", view={"label": "Flat Sum Insured",                    "format": utils.thousands_format(0)}),

            "load_amt_step_opening_si":     hx.Float(mode="input",  default=None, optionality="optional", view={"label": "Opening Sum Insured",                 "format": utils.thousands_format(0)}),
            "load_amt_step_grace_period":   hx.Int(  mode="input",  default=None, optionality="optional", view={"label": "Grace Period - months",               "format": utils.thousands_format(0)}),
            "load_amt_step_instal_amt":     hx.Float(mode="input",  default=None, optionality="optional", view={"label": "Instalment Amount (optional)",        "format": utils.thousands_format(0)}),
            "load_amt_step_instal_freq":    hx.Int(  mode="input",  default=None, optionality="optional", view={"label": "Period between instalments - months", "format": utils.thousands_format(0)}),
            "load_amt_step_term":           hx.Int(  mode="input",  default=None, optionality="optional", view={"label": "Term - months (optional)",            "format": utils.thousands_format(0)}),

            # single value fields used in the exposure profile analysis below
            "pre_shipment_adj_pct":         hx.Float(mode="output",                                       view={"label": "Pre-Shipment loading",     "format": utils.percent_format(0)}),
            "shipment_risk_adj_pct":        hx.Float(mode="output",                                       view={"label": "Shipment risk loading",    "format": utils.percent_format(0)}),
            "economic_outlook_adj_pct_pre_adj":hx.Float(mode="output",                                    view={"label": "Economic Outlook Load",    "format": utils.percent_format(0)}),
            "economic_outlook_adj_pct_pst_adj":hx.Float(mode="output",                                    view={"label": "Economic Outlook Load",    "format": utils.percent_format(0)}),
            "recovery_adj_pct":             hx.Float(mode="output",                                       view={"label": "Expected Recovery Percent","format": utils.percent_format(0)}),

            "last_run_status":              hx.Str(  mode="output",                                       view={"label": "Status - Last load of CRCF Exposure"}),
            "last_run_date":                hx.Str(  mode="output",                                       view={"label": "Date - Last load of CRCF Exposure"}),
            "last_run_value":               hx.Str(  mode="output",                                       view={"label": "Check Value - Last load of CRCF Exposure"}),
            "calc_run_value":               hx.Str(  mode="output",                                       view={"label": "Check Value - CRCF Exposure to be loaded"}),
            "check_run_consistent":         hx.Str(  mode="output",                                       view={"label": "Does data need to be reloaded:"}),

            # fixing the number of rows as i dont want them to have to add extra rows manually (or through an async task) - this was they just autohide if not needed.
            "exposure_profile": hx.List(mode="input",  default_element_count=15, min_element_count=15, max_element_count=15, children={
                "year":             hx.Int( mode="output",                                       view={"label": "Year"}),
                "year_label":       hx.Str( mode="output",                                       view={"label": "Year"}),
                "year_show_hide":   hx.Bool(mode="output",                                       view={"label": "Year show hide"}),

                "month_1":          hx.Float(mode="input", default=None, optionality="optional", view={"label": "Month 1",  "format": utils.thousands_format(0)}),
                "month_2":          hx.Float(mode="input", default=None, optionality="optional", view={"label": "Month 2",  "format": utils.thousands_format(0)}),
                "month_3":          hx.Float(mode="input", default=None, optionality="optional", view={"label": "Month 3",  "format": utils.thousands_format(0)}),
                "month_4":          hx.Float(mode="input", default=None, optionality="optional", view={"label": "Month 4",  "format": utils.thousands_format(0)}),
                "month_5":          hx.Float(mode="input", default=None, optionality="optional", view={"label": "Month 5",  "format": utils.thousands_format(0)}),
                "month_6":          hx.Float(mode="input", default=None, optionality="optional", view={"label": "Month 6",  "format": utils.thousands_format(0)}),
                "month_7":          hx.Float(mode="input", default=None, optionality="optional", view={"label": "Month 7",  "format": utils.thousands_format(0)}),
                "month_8":          hx.Float(mode="input", default=None, optionality="optional", view={"label": "Month 8",  "format": utils.thousands_format(0)}),
                "month_9":          hx.Float(mode="input", default=None, optionality="optional", view={"label": "Month 9",  "format": utils.thousands_format(0)}),
                "month_10":         hx.Float(mode="input", default=None, optionality="optional", view={"label": "Month 10", "format": utils.thousands_format(0)}),
                "month_11":         hx.Float(mode="input", default=None, optionality="optional", view={"label": "Month 11", "format": utils.thousands_format(0)}),
                "month_12":         hx.Float(mode="input", default=None, optionality="optional", view={"label": "Month 12", "format": utils.thousands_format(0)}),

                "average_default_month":                hx.Float(mode="output", view={"label": "Average Default Month",                 "format": utils.thousands_format(2)}),
                "average_default_year_month":           hx.Float(mode="output", view={"label": "Average Time to Default (n)",           "format": utils.thousands_format(2)}),
                "average_exposure":                     hx.Float(mode="output", view={"label": "Average Exposure (at n)",               "format": utils.thousands_format(0)}),
                "average_recovery_time":                hx.Float(mode="output", view={"label": "Average Time to Recoveries (from n=0)", "format": utils.thousands_format(2)}),
                "expected_recovery_pct":                hx.Float(mode="output", view={"label": "Expected Recoveries (at n=0)",          "format": utils.percent_format(3)}),
                "term_adj":                             hx.Float(mode="output", view={"label": "Term Adjustment - Final Year",          "format": utils.percent_format(3)}),

                "pre_uw_adj_tenor_load":                hx.Float(mode="output", view={"label": "Pre UW Adj:\nTenor Load",                            "format": utils.percent_format(3)}),
                "pre_uw_adj_pod_adj_inc":               hx.Float(mode="output", view={"label": "Pre UW Adj:\nAdjusted Probability of Default (at n)","format": utils.percent_format(3)}),
                "pre_uw_adj_pod_adj_inc_allow_prior":   hx.Float(mode="output", view={"label": "Pre UW Adj:\nAdjusted Probability of Default (at n), allowing for prior defaults",     "format": utils.percent_format(3)}),
                #"pre_uw_adj_lgd":                       hx.Float(mode="output", view={"label": "Loss Given Default (at n)",             "format": utils.percent_format(0)}),
                "pre_uw_adj_average_severity":          hx.Float(mode="output", view={"label": "Pre UW Adj:\nAverage Severity (at n)",               "format": utils.thousands_format(0)}),
                "pre_uw_adj_average_loss":              hx.Float(mode="output", view={"label": "Pre UW Adj:\nAverage Loss Cost (at n=0)",            "format": utils.thousands_format(0)}),
                "pre_uw_adj_average_loss_adj_lim_xs":   hx.Float(mode="output", view={"label": "Pre UW Adj:\nAverage Loss Cost (after adjustment for limit and excess)", "format": utils.thousands_format(0)}),
                "pre_uw_adj_premium_benchmark":         hx.Float(mode="output", view={"label": "Pre UW Adj:\nBenchmark Premium",                     "format": utils.thousands_format(0)}),
                "pre_uw_adj_premium_achieved":          hx.Float(mode="output", view={"label": "Pre UW Adj:\nAchieved Premium",                      "format": utils.thousands_format(0)}),
                "pre_uw_adj_premium_achieved_adj_pod":  hx.Float(mode="output", view={"label": "Pre UW Adj:\nExpected Achieved Premium",             "format": utils.thousands_format(0)}),

                "pst_uw_adj_tenor_load":                hx.Float(mode="output", view={"label": "Post UW Adj:\nTenor Load",                            "format": utils.percent_format(3)}),
                "pst_uw_adj_pod_adj_inc":               hx.Float(mode="output", view={"label": "Post UW Adj:\nAdjusted Probability of Default (at n)","format": utils.percent_format(3)}),
                "pst_uw_adj_pod_adj_inc_allow_prior":   hx.Float(mode="output", view={"label": "Post UW Adj:\nAdjusted Probability of Default (at n), allowing for prior defaults",     "format": utils.percent_format(3)}),
                #"pst_uw_adj_lgd":                       hx.Float(mode="output", view={"label": "Loss Given Default (at n)",             "format": utils.percent_format(0)}),
                "pst_uw_adj_average_severity":          hx.Float(mode="output", view={"label": "Post UW Adj:\nAverage Severity (at n)",               "format": utils.thousands_format(0)}),
                "pst_uw_adj_average_loss":              hx.Float(mode="output", view={"label": "Post UW Adj:\nAverage Loss Cost (at n=0)",            "format": utils.thousands_format(0)}),
                "pst_uw_adj_average_loss_adj_lim_xs":   hx.Float(mode="output", view={"label": "Post UW Adj:\nAverage Loss Cost (after adjustment for limit and excess)", "format": utils.thousands_format(0)}),
                "pst_uw_adj_premium_benchmark":         hx.Float(mode="output", view={"label": "Post UW Adj:\nBenchmark Premium",                     "format": utils.thousands_format(0)}),
                "pst_uw_adj_premium_achieved":          hx.Float(mode="output", view={"label": "Post UW Adj:\nAchieved Premium",                      "format": utils.thousands_format(0)}),
                "pst_uw_adj_premium_achieved_adj_pod":  hx.Float(mode="output", view={"label": "Post UW Adj:\nExpected Achieved Premium",             "format": utils.thousands_format(0)}),

                "implied_lgd_average_loss_adj_lim_xs":  hx.Float(mode="output", view={"label": "Implied LGD:\nAverage Loss Cost (after adjustment for limit and excess)", "format": utils.thousands_format(0)}),
                "implied_lgd_average_loss":             hx.Float(mode="output", view={"label": "Implied LGD:\nAverage Loss Cost (at n=0)",            "format": utils.thousands_format(0)}),
                "implied_lgd_average_severity":         hx.Float(mode="output", view={"label": "Implied LGD:\nAverage Severity (at n)",               "format": utils.thousands_format(0)}),
                "implied_lgd":                          hx.Float(mode="output", view={"label": "Implied LGD:\nLoss Given Default (at n)",             "format": utils.percent_format(3)}),

                "implied_grade_average_loss_adj_lim_xs":hx.Float(mode="output", view={"label": "Implied Grade:\nAverage Loss Cost (after adjustment for limit and excess)", "format": utils.thousands_format(0)}),
                "implied_grade_average_loss":           hx.Float(mode="output", view={"label": "Implied Grade:\nAverage Loss Cost (at n=0)",            "format": utils.thousands_format(0)}),
                "implied_grade_pod_adj_inc_allow_prior":hx.Float(mode="output", view={"label": "Implied Grade:\nCumulative Adjusted Probability of Default (from n=0)",     "format": utils.percent_format(3)}),
                "implied_grade_pod_adj_inc":            hx.Float(mode="output", view={"label": "Implied Grade:\nAdjusted Probability of Default (at n)","format": utils.percent_format(3)}),
                "implied_grade_pod_inc":                hx.Float(mode="output", view={"label": "Implied Grade:\nProbability of Default (at n)",         "format": utils.percent_format(3)}),

            }),

            "exposure_profile_label_months": hx.Structure(children={
                "month_1":          hx.Str(mode="output", view={"label": "Month 1"}),
                "month_2":          hx.Str(mode="output", view={"label": "Month 2"}),
                "month_3":          hx.Str(mode="output", view={"label": "Month 3"}),
                "month_4":          hx.Str(mode="output", view={"label": "Month 4"}),
                "month_5":          hx.Str(mode="output", view={"label": "Month 5"}),
                "month_6":          hx.Str(mode="output", view={"label": "Month 6"}),
                "month_7":          hx.Str(mode="output", view={"label": "Month 7"}),
                "month_8":          hx.Str(mode="output", view={"label": "Month 8"}),
                "month_9":          hx.Str(mode="output", view={"label": "Month 9"}),
                "month_10":         hx.Str(mode="output", view={"label": "Month 10"}),
                "month_11":         hx.Str(mode="output", view={"label": "Month 11"}),
                "month_12":         hx.Str(mode="output", view={"label": "Month 12"}),
            }),

        }),





        "political"  : hx.Structure(children={
            "tenor":                        hx.Float(mode="output",                                       view={"label": "Tenor (mths)",             "format": utils.thousands_format(0)}),
            "exposure_curve":               hx.Str(  mode="input",  default="Standard",                   view={"label": "Exposure Curve"}                       , options_table="tbl_exposure_curves", options_column="Curve" ),    
            "ec_param_b":                   hx.Float(mode="output",                                       view={"label": "Exposure Curve - param b", "format": utils.thousands_format(0)}),
            "ec_param_g":                   hx.Float(mode="output",                                       view={"label": "Exposure Curve - param g", "format": utils.thousands_format(0)}),

            
            # relating to the simulation task
            "simulation"  : hx.Structure(children={
                "last_run_status"           : hx.Str( mode="output", view={"label": "Status - Last run of Simulation"}),
                "last_run_date"             : hx.Str( mode="output", view={"label": "Date - Last run of Simulation"}),
                "last_run_value"            : hx.Str( mode="output", view={"label": "Check Value - Last run of Simulation"}),
                "calc_run_value"            : hx.Str( mode="output", view={"label": "Check Value - Prospective Simulation"}),
                "check_run_consistent"      : hx.Str( mode="output", view={"label": "Does simulation need to be rerun:"}),
                "num_sims"                  : hx.Int( mode="output", view={"label": "Number of Sims",                                                         "format": utils.thousands_format(0)}),
                "total_sim_loss_uncapped"   : hx.Float(mode="input", default=0,                     view={"label": "Simulated Loss Amount - uncapped",        "format": utils.thousands_format(0)}),
                "total_sim_loss_capped"     : hx.Float(mode="input", default=0,                     view={"label": "Simulated Loss Amount - capped",          "format": utils.thousands_format(0)}),
                "total_det_loss_uncapped"   : hx.Float(mode="output",                               view={"label": "Deterministic Loss Amount - uncapped",    "format": utils.thousands_format(0)}),
                "total_det_loss_capped"     : hx.Float(mode="output",                               view={"label": "Deterministic Loss Amount - capped",      "format": utils.thousands_format(0)}),
                "total_det_loss_scaled"     : hx.Float(mode="output",                               view={"label": "Deterministic Loss Amount - capped & scaled","format": utils.thousands_format(0)}),
            }),

            "key_summary_outputs":      hx.Structure(view={"label": "Calculation Outputs"},children={
                "tenor_score":              hx.Float(mode="output", view={"label": "Tenor Score",                                           "format": utils.thousands_format(2)}),   
                "tenor_rate":               hx.Float(mode="output", view={"label": "Tenor Rate",                                            "format": utils.thousands_format(2)}),   

                "on_cover":             hx.Structure(view={"label": "On Cover"}, children={
                    "gov_action":           hx.Bool(  mode="output", view={"label": "Government Action & Intervention"}            ),
                    "pol_violence":         hx.Bool(  mode="output", view={"label": "Political Violence"}                          ),
                    "cur_inconvertibility": hx.Bool(  mode="output", view={"label": "Currency Inconvertibility"}                   ),
                    "cont_relation_govt":   hx.Bool(  mode="output", view={"label": "Contractual Relationship with Government"}    ),
                    }),

                "exposure_rol":         hx.Structure(view={"label": "Model Premium - Exposure rate-on-line"}, children={
                    "gov_action":           hx.Float(mode="output", view={"label": "Government Action & Intervention",          "format": utils.thousands_format(2)}),
                    "pol_violence":         hx.Float(mode="output", view={"label": "Political Violence",                        "format": utils.thousands_format(2)}),
                    "cur_inconvertibility": hx.Float(mode="output", view={"label": "Currency Inconvertibility",                 "format": utils.thousands_format(2)}),
                    "cont_relation_govt":   hx.Float(mode="output", view={"label": "Contractual Relationship with Government",  "format": utils.thousands_format(2)}),
                    "total":                hx.Float(mode="output", view={"label": "Total",                                     "format": utils.thousands_format(2)}),
                    }),

                "simulated_prem":        hx.Structure(view={"label": "Model Premium - Simulated rate-on-line"}, children={
                    "gov_action":           hx.Float(mode="output", view={"label": "Government Action & Intervention",          "format": utils.thousands_format(2)}),
                    "pol_violence":         hx.Float(mode="output", view={"label": "Political Violence",                        "format": utils.thousands_format(2)}),
                    "cur_inconvertibility": hx.Float(mode="output", view={"label": "Currency Inconvertibility",                 "format": utils.thousands_format(2)}),
                    "cont_relation_govt":   hx.Float(mode="output", view={"label": "Contractual Relationship with Government",  "format": utils.thousands_format(2)}),
                    "total":                hx.Float(mode="output", view={"label": "Total",                                     "format": utils.thousands_format(2)}),
                    }),

                "simulated_loss":        hx.Structure(view={"label": "Model Loss - Simulated loss-on-line"}, children={
                    "gov_action":           hx.Float(mode="output", view={"label": "Government Action & Intervention",          "format": utils.thousands_format(2)}),
                    "pol_violence":         hx.Float(mode="output", view={"label": "Political Violence",                        "format": utils.thousands_format(2)}),
                    "cur_inconvertibility": hx.Float(mode="output", view={"label": "Currency Inconvertibility",                 "format": utils.thousands_format(2)}),
                    "cont_relation_govt":   hx.Float(mode="output", view={"label": "Contractual Relationship with Government",  "format": utils.thousands_format(2)}),
                    "total":                hx.Float(mode="output", view={"label": "Total",                                     "format": utils.thousands_format(2)}),
                    }),

                }),  



            "coverage_matrix":      hx.Structure(view={"label": "Coverage Matrix"},children={
                "mobile_assets": hx.Structure(view={"label": "Mobile Assets"}, children={
                    "gov_action":           hx.Bool( mode="input", default=False,                         view={"label": "Government Action & Intervention"},            ),
                    "pol_violence":         hx.Bool( mode="input", default=False,                         view={"label": "Political Violence"},                          ),
                    "cur_inconvertibility": hx.Bool( mode="input", default=False,                         view={"label": "Currency Inconvertibility"},                   ),
                    "cont_relation_govt":   hx.Bool( mode="input", default=False,                         view={"label": "Contractual Relationship with Government"},    ),
                }),  

                "fixed_assets":     hx.Structure(view={"label": "Fixed Assets"}, children={
                    "gov_action":           hx.Bool( mode="input", default=False,                         view={"label": "Government Action & Intervention"},            ),
                    "pol_violence":         hx.Bool( mode="input", default=False,                         view={"label": "Political Violence"},                          ),
                    "cur_inconvertibility": hx.Bool( mode="input", default=False,                         view={"label": "Currency Inconvertibility"},                   ),
                    "cont_relation_govt":   hx.Bool( mode="input", default=False,                         view={"label": "Contractual Relationship with Government"},    ),
                }),  

                "lenders_interest": hx.Structure(view={"label": "Lenders Interest"}, children={
                    "gov_action":           hx.Bool( mode="input", default=False,                         view={"label": "Government Action & Intervention"},            ),
                    "pol_violence":         hx.Bool( mode="input", default=False,                         view={"label": "Political Violence"},                          ),
                    "cur_inconvertibility": hx.Bool( mode="input", default=False,                         view={"label": "Currency Inconvertibility"},                   ),
                    "cont_relation_govt":   hx.Bool( mode="input", default=False,                         view={"label": "Contractual Relationship with Government"},    ),
                }),  

                "sublimit":         hx.Structure(view={"label": "Sublimit"}, children={
                   #"gov_action":           hx.Float(mode="input", default=None, optionality="optional", view={"label": "Government Action & Intervention",             "format": utils.thousands_format(0)} ),
                    "pol_violence":         hx.Float(mode="input", default=None, optionality="optional", view={"label": "Political Violence",                           "format": utils.thousands_format(0)} ),
                    "cur_inconvertibility": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Currency Inconvertibility",                    "format": utils.thousands_format(0)} ),
                   #"cont_relation_govt":   hx.Float(mode="input", default=None, optionality="optional", view={"label": "Contractual Relationship with Government",     "format": utils.thousands_format(0)} ),
                }),  

                "deductible":       hx.Structure(view={"label": "Deductible"}, children={
                   #"gov_action":           hx.Float(mode="input", default=None, optionality="optional", view={"label": "Government Action & Intervention",             "format": utils.thousands_format(0)} ),
                    "pol_violence":         hx.Float(mode="input", default=None, optionality="optional", view={"label": "Political Violence",                           "format": utils.thousands_format(0)} ),
                   #"cur_inconvertibility": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Currency Inconvertibility",                    "format": utils.thousands_format(0)} ),
                   #"cont_relation_govt":   hx.Float(mode="input", default=None, optionality="optional", view={"label": "Contractual Relationship with Government",     "format": utils.thousands_format(0)} ),
                }),  
            }),



            "country_exposure": hx.List(mode="input",  default_element_count=20, min_element_count=1, async_input=["rarc_task"], children={
                "id":                   hx.Float(mode="output",                                       view={"label": "ID",                  "format": utils.thousands_format(0)}),
                "country":              hx.Str(  mode="input",  default=None, optionality="optional", view={"label": "Country"},                options_table="tbl_ihs_country",     options_column="IHS Country"),
                "sum_insured":          hx.Float(mode="input",  default=None, optionality="optional", view={"label": "Total Sum Insured",   "format": utils.thousands_format(0)}),
                "excess":               hx.Float(mode="input",  default=None, optionality="optional", view={"label": "Excess",              "format": utils.thousands_format(0)}),
                "limit":                hx.Float(mode="input",  default=None, optionality="optional", view={"label": "Limit",               "format": utils.thousands_format(0)}),
                "check":                hx.Str(  mode="output",                                       view={"label": "Complete Check"}),
                "country_2dig":         hx.Str(  mode="output",                                       view={"label": "Country 2 digit"}),

                "sublimit_pv":          hx.Float(mode="output", view={"label": "Sub-limit: Political Violence",                                         "format": utils.thousands_format(0)}),
                "deductible_pv":        hx.Float(mode="output", view={"label": "Deductible: Political Violence",                                        "format": utils.thousands_format(0)}),
                "sublimit_ci":          hx.Float(mode="output", view={"label": "Sub-limit: Currency Inconvertibility",                                  "format": utils.thousands_format(0)}),
                
                "ihs_political":        hx.Float(mode="output", view={"label": "IHS Score: Political",                                                  "format": utils.thousands_format(3)}),
                "ihs_violence":         hx.Float(mode="output", view={"label": "IHS Score: Violence",                                                   "format": utils.thousands_format(3)}),
                "ihs_ci":               hx.Float(mode="output", view={"label": "IHS Score: Currency Inconvertibility",                                  "format": utils.thousands_format(3)}),
                
                "prem_roe_gai":         hx.Float(mode="output", view={"label": "Premium Rate on Exposure: Government Action & Intervention",            "format": utils.percent_format(4)}),
                "prem_roe_pv":          hx.Float(mode="output", view={"label": "Premium Rate on Exposure: Political Violence",                          "format": utils.percent_format(4)}),
                "prem_roe_ci":          hx.Float(mode="output", view={"label": "Premium Rate on Exposure: Currency Inconvertibility",                   "format": utils.percent_format(4)}),
                "prem_roe_crg":         hx.Float(mode="output", view={"label": "Premium Rate on Exposure: Contractual Relationship with Government",    "format": utils.percent_format(4)}),
                "prem_roe_tot":         hx.Float(mode="output", view={"label": "Premium Rate on Exposure: Total",                                       "format": utils.percent_format(4)}),
                
                "loss_roe_gai":         hx.Float(mode="output", view={"label": "Loss Rate on Exposure: Government Action & Intervention",               "format": utils.percent_format(4)}),
                "loss_roe_pv":          hx.Float(mode="output", view={"label": "Loss Rate on Exposure: Political Violence",                             "format": utils.percent_format(4)}),
                "loss_roe_ci":          hx.Float(mode="output", view={"label": "Loss Rate on Exposure: Currency Inconvertibility",                      "format": utils.percent_format(4)}),
                "loss_roe_crg":         hx.Float(mode="output", view={"label": "Loss Rate on Exposure: Contractual Relationship with Government",       "format": utils.percent_format(4)}),
                "loss_roe_tot":         hx.Float(mode="output", view={"label": "Loss Rate on Exposure: Total",                                          "format": utils.percent_format(4)}),
                
                "struc_adj_gai":        hx.Float(mode="output", view={"label": "Allowing for Attach/Limit: Government Action & Intervention",           "format": utils.percent_format(4)}),
                "struc_adj_pv":         hx.Float(mode="output", view={"label": "Allowing for Attach/Limit: Political Violence",                         "format": utils.percent_format(4)}),
                "struc_adj_ci":         hx.Float(mode="output", view={"label": "Allowing for Attach/Limit: Currency Inconvertibility",                  "format": utils.percent_format(4)}),
                "struc_adj_crg":        hx.Float(mode="output", view={"label": "Allowing for Attach/Limit: Contractual Relationship with Government",   "format": utils.percent_format(4)}),
                
                "net_rol_gai":          hx.Float(mode="output", view={"label": "Net Rate on Line: Government Action & Intervention",                    "format": utils.percent_format(4)}),
                "net_rol_pv":           hx.Float(mode="output", view={"label": "Net Rate on Line: Political Violence",                                  "format": utils.percent_format(4)}),
                "net_rol_ci":           hx.Float(mode="output", view={"label": "Net Rate on Line: Currency Inconvertibility",                           "format": utils.percent_format(4)}),
                "net_rol_crg":          hx.Float(mode="output", view={"label": "Net Rate on Line: Contractual Relationship with Government",            "format": utils.percent_format(4)}),
                "net_rol_tot":          hx.Float(mode="output", view={"label": "Net Rate on Line: Total",                                               "format": utils.percent_format(4)}),
                
                "gross_rol_tot":        hx.Float(mode="output", view={"label": "Gross Rate on Line: Total",                                             "format": utils.percent_format(4)}),




            }),

        }),

    })




    cds.extend_node_rater_defined("cds", {
        "modifiers"  : hx.Structure(children={
            
            
            "crcf"      : hx.Structure(children={

                "default":      hx.Structure(view={"label": "Default"}, children={
                    "grade":        hx.Str(  mode="output",                                      view={"label": "Grade"}),
                    "pod":          hx.Float(mode="output",                                      view={"label": "Probability of Default",  "format": utils.percent_format(3)}),
                    "lgd":          hx.Float(mode="output",                                      view={"label": "Loss Given Default",      "format": utils.percent_format(3)}),
                    "uw_adj":       hx.Float(mode="output",                                      view={"label": "Underwriter Adjustment",  "format": utils.percent_format(3)}),
                }),  

                "override_min": hx.Structure(view={"label": "Min"}, children={
                    "grade":        hx.Str(  mode="output",                                      view={"label": "Grade"}),
                    "pod":          hx.Float(mode="output",                                      view={"label": "Probability of Default",  "format": utils.percent_format(3)}),
                    "lgd":          hx.Float(mode="output",                                      view={"label": "Loss Given Default",      "format": utils.percent_format(3)}),
                    "uw_adj":       hx.Float(mode="output",                                      view={"label": "Underwriter Adjustment",  "format": utils.percent_format(3)}),
                }),  

                "override_max": hx.Structure(view={"label": "Max"}, children={
                    "grade":        hx.Str(  mode="output",                                      view={"label": "Grade"}),
                    "pod":          hx.Float(mode="output",                                      view={"label": "Probability of Default",  "format": utils.percent_format(3)}),
                    "lgd":          hx.Float(mode="output",                                      view={"label": "Loss Given Default",      "format": utils.percent_format(3)}),
                    "uw_adj":       hx.Float(mode="output",                                      view={"label": "Underwriter Adjustment",  "format": utils.percent_format(3)}),
                }),  
                                    
                "override":     hx.Structure(view={"label": "Override"}, children={
                    "grade":        hx.Str(  mode="input", default=None, optionality="optional", view={"label": "Grade"},           options_table="lst_credit_rating",          options_column="Rating"),
                    "pod":          hx.Float(mode="output",                                      view={"label": "Probability of Default",  "format": utils.percent_format(3)}),
                    "lgd":          hx.Float(mode="input", default=None, optionality="optional", view={"label": "Loss Given Default",      "format": utils.percent_format(3)}),
                    "uw_adj":       hx.Float(mode="input", default=None, optionality="optional", view={"label": "Underwriter Adjustment",  "format": utils.percent_format(3)}),
                }),

                "selected":     hx.Structure(view={"label": "Selected"}, children={
                    "grade":        hx.Str(  mode="output",                                      view={"label": "Grade"}),
                    "pod":          hx.Float(mode="output",                                      view={"label": "Probability of Default",  "format": utils.percent_format(3)}),
                    "lgd":          hx.Float(mode="output",                                      view={"label": "Loss Given Default",      "format": utils.percent_format(3)}),
                    "uw_adj":       hx.Float(mode="output",                                      view={"label": "Underwriter Adjustment",  "format": utils.percent_format(3)}),
                }),

                "rating_country":   hx.Str(  mode="output",                                      view={"label": "Country Credit Rating"}),
                "rating_corporate": hx.Str(  mode="input",  default="BBB+",                      view={"label": "Corporate Credit Rating"},     options_table="lst_credit_rating",          options_column="Rating"),
                "rating_source":    hx.Str(  mode="input",  default="Beazley credit tool",       view={"label": "Source of Rating"},            options_table="lst_credit_rating_source",   options_column="Source Of Rating"),
                "rating_commentary":hx.Str(  mode="input",  default=None, optionality="optional",view={"label": "Please provide commentary on the source of the credit rating."}), 
                "economic_outlook": hx.Str(  mode="output",                                      view={"label": "Economic Outlook"}),

                "obligor_commentary":hx.Str( mode="input",  default=None, optionality="optional",view={"label": "Please provide commentary on the Obligor Risk Drivers"}),
                "lgd_commentary"    :hx.Str( mode="input",  default=None, optionality="optional",view={"label": "Please provide commentary on the Security - Impact on Average LGD"}),
                "uw_adj_commentary" :hx.Str( mode="input",  default=None, optionality="optional",view={"label": "Please provide commentary on the Underwriter Adjustments"}),
            }),


            "political"  : hx.Structure(children={

                "override_min":     hx.Structure(view={"label": "Min"}, children={
                    "industry":             hx.Float(mode="output",                                      view={"label": "UW Adjustment 1 - Industry",               "format": utils.percent_format(0),    "info" : tips.tip_ed03}),
                    "insured_quality":      hx.Float(mode="output",                                      view={"label": "UW Adjustment 2 - Quality of Insured",     "format": utils.percent_format(0),    "info" : tips.tip_ed04}),
                    "asset_composition":    hx.Float(mode="output",                                      view={"label": "UW Adjustment 3 - Asset Composition",      "format": utils.percent_format(0),    "info" : tips.tip_ed05}),
                    "total":                hx.Float(mode="output",                                      view={"label": "Total",                                    "format": utils.percent_format(0)}),
                }),  

                "override":         hx.Structure(view={"label": "Override"}, children={
                    "industry":             hx.Float(mode="input",  default=0,                           view={"label": "UW Adjustment 1 - Industry",               "format": utils.percent_format(0),    "info" : tips.tip_ed03}),
                    "insured_quality":      hx.Float(mode="input",  default=0,                           view={"label": "UW Adjustment 2 - Quality of Insured",     "format": utils.percent_format(0),    "info" : tips.tip_ed04}),
                    "asset_composition":    hx.Float(mode="input",  default=0,                           view={"label": "UW Adjustment 3 - Asset Composition",      "format": utils.percent_format(0),    "info" : tips.tip_ed05}),
                    "total":                hx.Float(mode="output",                                      view={"label": "Total",                                    "format": utils.percent_format(0)}),
                }),

                "override_max":     hx.Structure(view={"label": "Max"}, children={
                    "industry":             hx.Float(mode="output",                                      view={"label": "UW Adjustment 1 - Industry",               "format": utils.percent_format(0),    "info" : tips.tip_ed03}),
                    "insured_quality":      hx.Float(mode="output",                                      view={"label": "UW Adjustment 2 - Quality of Insured",     "format": utils.percent_format(0),    "info" : tips.tip_ed04}),
                    "asset_composition":    hx.Float(mode="output",                                      view={"label": "UW Adjustment 3 - Asset Composition",      "format": utils.percent_format(0),    "info" : tips.tip_ed05}),
                    "total":                hx.Float(mode="output",                                      view={"label": "Total",                                    "format": utils.percent_format(0)}),
                }),  
                                    
                "selected":         hx.Structure(view={"label": "Selected"}, children={
                    "industry":             hx.Float(mode="output",                                      view={"label": "UW Adjustment 1 - Industry",               "format": utils.percent_format(0),    "info" : tips.tip_ed03}),
                    "insured_quality":      hx.Float(mode="output",                                      view={"label": "UW Adjustment 2 - Quality of Insured",     "format": utils.percent_format(0),    "info" : tips.tip_ed04}),
                    "asset_composition":    hx.Float(mode="output",                                      view={"label": "UW Adjustment 3 - Asset Composition",      "format": utils.percent_format(0),    "info" : tips.tip_ed05}),
                    "total":                hx.Float(mode="output",                                      view={"label": "Total",                                    "format": utils.percent_format(0)}),
                }),

                "uw_adj_commentary": hx.Str(  mode="input", default=None, optionality="optional",view={"label": "Please provide commentary on the Underwriter Adjustments"}),
            }),
        }),
        
    })
