###########################################################################################################################################################
###                                                                         OUTSTANDING                                                                 ###
###########################################################################################################################################################
# 1)
# 2) 
# 3)
# 4)
# 5)
###########################################################################################################################################################

 


import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers
from algorithms.rate_constants import max_layers
import data_schema.sch_utilities as utils
import data_schema.sch_tooltips as tips

def premium_composition(coverage):

    group = "Total" if coverage == "total" else "Coverage"
    
    return{
            "premium_technical":    hx.Float(mode="output",             view={"label": "Technical Premium",     "info" : tips.tip_rs17,  "format": utils.thousands_format(0), "group": group}),
            "expected_loss":        hx.Float(mode="output",             view={"label": "Expected Losses",       "info" : tips.tip_rs07,  "format": utils.thousands_format(0), "group": group}),
            "che":                  hx.Float(mode="output",             view={"label": "Claims Handling Expense","info" : tips.tip_rs09, "format": utils.thousands_format(0), "group": group}),
            "fixed_expenses":       hx.Float(mode="output",             view={"label": "Fixed Expenses",        "info" : tips.tip_rs10,  "format": utils.thousands_format(0), "group": group}),
            "variable_expenses":    hx.Float(mode="output",             view={"label": "Variable Expenses",     "info" : tips.tip_rs11,  "format": utils.thousands_format(0), "group": group}),
            "investment_income":    hx.Float(mode="output",             view={"label": "Investment Income",     "info" : tips.tip_rs12,  "format": utils.thousands_format(0), "group": group}),
            "cost_of_reinsurance":  hx.Float(mode="output",             view={"label": "Cost of Reinsurance",   "info" : tips.tip_rs13,  "format": utils.thousands_format(0), "group": group}),
            "capital":              hx.Float(mode="output",             view={"label": "Capital",               "info" : tips.tip_rs14,  "format": utils.thousands_format(0), "group": group}),
            "brokerage":            hx.Float(mode="output",             view={"label": "Brokerage",             "info" : tips.tip_rs15,  "format": utils.thousands_format(0), "group": group}),

            "premium_benchmark":    hx.Float(mode="output",             view={"label": "Benchmark Premium",     "info" : tips.tip_rs21,  "format": utils.thousands_format(0), "group": group}),
            "loadings_benchmark":   hx.Float(mode="output",             view={"label": "Implied Loadings",                               "format": utils.thousands_format(0), "group": group}),

            "premium_model":        hx.Float(mode="output",             view={"label": "Model Premium",         "info" : tips.tip_rs22,  "format": utils.thousands_format(0), "group": group}),
            "loadings_model":       hx.Float(mode="output",             view={"label": "Implied Loadings",                               "format": utils.thousands_format(0), "group": group}),

            "premium_plan":         hx.Float(mode="output",             view={"label": "Plan Premium",          "info" : tips.tip_rs23,  "format": utils.thousands_format(0), "group": group}),
            "loadings_plan":        hx.Float(mode="output",             view={"label": "Implied Loadings",                               "format": utils.thousands_format(0), "group": group}),

            "premium_bound":        hx.Float(mode="output",             view={"label": "Bound Premium",         "info" : tips.tip_rs24,  "format": utils.thousands_format(0), "group": group}),
            "loadings_bound":       hx.Float(mode="output",             view={"label": "Implied Loadings",                               "format": utils.thousands_format(0), "group": group}),
    }
 

def standard_metrics():
    return{
            "bpi":                  hx.Float(mode="output",             view={"label": "BPI",                                  "format": utils.percent_format(2)}),
            "tpi":                  hx.Float(mode="output",             view={"label": "TPI",                                  "format": utils.percent_format(2)}),
            "priced_to_plan":       hx.Float(mode="output",             view={"label": "Priced to Plan",                       "format": utils.percent_format(2)}),
            "priced_gglr":          hx.Float(mode="output",             view={"label": "Priced Loss Ratio - Gross Gross",      "format": utils.percent_format(2)}),
            "priced_gnlr":          hx.Float(mode="output",             view={"label": "Priced Loss Ratio - Gross Net",        "format": utils.percent_format(2)}),
    }


def loss_composition():
    return{
            "exposure":             hx.Float(mode="output",             view={"label": "a) Maximum Exposure",                                             "format": utils.thousands_format(0)}),
            "credit_rating":        hx.Str(  mode="output",             view={"label": "b) Selected Grade",           "info" : tips.tip_rs01,                                              }),
            "pod":                  hx.Float(mode="output",             view={"label": "c) Probability of Default",   "info" : tips.tip_rs02,             "format": utils.percent_format(2)}),
            "tenor_load":           hx.Float(mode="output",             view={"label": "d) Total Tenor Loading",      "info" : tips.tip_rs03,             "format": utils.percent_format(2)}),
            "lgd":                  hx.Float(mode="output",             view={"label": "e) Loss Given Default",       "info" : tips.tip_rs04,             "format": utils.percent_format(2)}),
            "recovery_discounted":  hx.Float(mode="output",             view={"label": "f) Discount Recoveries",      "info" : tips.tip_rs05,             "format": utils.percent_format(2)}),
            "limit_discount":       hx.Float(mode="output",             view={"label": "g) Limit Discount",           "info" : tips.tip_rs06,             "format": utils.percent_format(2)}),
            "term":                 hx.Float(mode="output",             view={"label": "h) Term",                     "info" : tips.tip_rs19,             "format": utils.percent_format(2)}),
            "other":                hx.Float(mode="output",             view={"label": "i) Other",                    "info" : tips.tip_rs20,             "format": utils.percent_format(2)}),
            "expected_loss":        hx.Float(mode="output",             view={"label": "Expected Loss",               "info" : tips.tip_rs18,             "format": utils.thousands_format(0)}),
    }



def sch_rating_summary(cds):
    cds.extend_node_rater_defined('cds/layers', {
        # Added variable to record a bpi where the risk is case priced. Do not remove as used in tpi summary. 
        'bpi_case_priced': hx.Float(mode='input', default=None, optionality='optional', view={'label': 'BPI (Case Priced)', 'format': percent_format(1)}),
        'pflr_pre_uw_adj': hx.Float(mode='output', optionality='optional', view={'label': 'Priced-for Loss Ratio (Pre-UW Adj.)', 'format': {'output': 'percent', 'mantissa': 1}}),
        'premium_label': hx.Str(mode='output'),

        # Used for rate change calcs
        'quoted_premium_annualised': hx.Float(mode='output', async_input=["rarc_task"]),
        'benchmark_premium_annualised': hx.Float(mode='output', async_input=["rarc_task"]),

        "political"  : hx.Structure(children={
     
            "metrics_summary_pre_uwadj":     hx.Structure(view={"label": "Metrics\nPre-UWadj"}, children={
                "rol_offered":              hx.Float(mode="output",                                      view={"label": "Rate-on-Line - Offered",               "format": utils.percent_format(2)}),
                "rol_model":                hx.Float(mode="output",                                      view={"label": "Rate-on-Line - Model",                 "format": utils.percent_format(2)}),
                "rol_plan":                 hx.Float(mode="output",                                      view={"label": "Rate-on-Line - Plan",                  "format": utils.percent_format(2)}),
                "rol_technical":            hx.Float(mode="output",                                      view={"label": "Rate-on-Line - Technical",             "format": utils.percent_format(2)}),
                "rol_benchmark":            hx.Float(mode="output",                                      view={"label": "Rate-on-Line - Benchmark",             "format": utils.percent_format(2)}),
                **standard_metrics() 
            }),

            "metrics_summary_pst_uwadj":     hx.Structure(view={"label": "Metrics\nPst-UWadj"}, children={
                "rol_offered":              hx.Float(mode="input", default=None, optionality='optional', view={"label": "Rate-on-Line - Offered",               "format": utils.percent_format(2)}),
                "rol_model":                hx.Float(mode="output",                                      view={"label": "Rate-on-Line - Model",                 "format": utils.percent_format(2)}),
                "rol_plan":                 hx.Float(mode="output",                                      view={"label": "Rate-on-Line - Plan",                  "format": utils.percent_format(2)}),
                "rol_technical":            hx.Float(mode="output",                                      view={"label": "Rate-on-Line - Technical",             "format": utils.percent_format(2)}),
                "rol_benchmark":            hx.Float(mode="output",                                      view={"label": "Rate-on-Line - Benchmark",             "format": utils.percent_format(2)}),
                **standard_metrics() 
            }),

            # uses list comprehension to loop over the given structure, before unpacking
            "premium_composition_pre_uwadj":     hx.Structure(view={"label": "Metrics\nPre-UWadj"}, children={
                **{item: hx.Structure(view={"label": label}, children={                    **premium_composition(coverage=item)                })
                    for item, label in zip( ["gov_action",  "pol_violence", "cur_inconvertibility", "cont_relation_govt", "total"], 
                                            ["Government\nAction &\nIntervention", "Political\nViolence", "Currency\nInconvertibility", "Contractual\nRelationship\nwith\nGovernment", "Total"])},
            }),

            "premium_composition_pst_uwadj":     hx.Structure(view={"label": "Metrics\nPst-UWadj"}, children={
                **{item: hx.Structure(view={"label": label}, children={                    **premium_composition(coverage=item)              })
                    for item, label in zip( ["gov_action",  "pol_violence", "cur_inconvertibility", "cont_relation_govt", "total"], 
                                            ["Government\nAction &\nIntervention", "Political\nViolence", "Currency\nInconvertibility", "Contractual\nRelationship\nwith\nGovernment", "Total"])},
            }),

        }),  



        "crcf"  : hx.Structure(children={

            "loss_composition_pre_uwadj_term":     hx.Structure(view={"label": "Loss Calc\nPre-UWadj\nTerm"}, children={       **loss_composition()  }),
            "loss_composition_pst_uwadj_term":     hx.Structure(view={"label": "Loss Calc\nPst-UWadj\nTerm"}, children={       **loss_composition()  }),


            "metrics_summary_pre_uwadj_annual":     hx.Structure(view={"label": "Metrics\nPre-UWadj\nAnnual"}, children={
                "roe_offered":              hx.Float(mode="output",                                      view={"label": "Rate-on-Exposure - Offered",               "format": utils.percent_format(2)}),
                "roe_plan":                 hx.Float(mode="output",                                      view={"label": "Rate-on-Exposure - Plan",                  "format": utils.percent_format(2)}),
                "roe_technical":            hx.Float(mode="output",                                      view={"label": "Rate-on-Exposure - Technical",             "format": utils.percent_format(2)}),
                "roe_benchmark":            hx.Float(mode="output",                                      view={"label": "Rate-on-Exposure - Benchmark",             "format": utils.percent_format(2)}),
                #**standard_metrics() 
            }),


            "metrics_summary_pre_uwadj_term":     hx.Structure(view={"label": "Metrics\nPre-UWadj\nTerm"}, children={
                "roe_offered":              hx.Float(mode="output",                                      view={"label": "Rate-on-Exposure - Offered",               "format": utils.percent_format(2)}),
                "roe_plan":                 hx.Float(mode="output",                                      view={"label": "Rate-on-Exposure - Plan",                  "format": utils.percent_format(2)}),
                "roe_technical":            hx.Float(mode="output",                                      view={"label": "Rate-on-Exposure - Technical",             "format": utils.percent_format(2)}),
                "roe_benchmark":            hx.Float(mode="output",                                      view={"label": "Rate-on-Exposure - Benchmark",             "format": utils.percent_format(2)}),
                **standard_metrics() 
            }),

            # notice below roe_offered is an input
            "metrics_summary_pst_uwadj_annual":     hx.Structure(view={"label": "Metrics\nPst-UWadj\nAnnual"}, children={
                "roe_offered":              hx.Float(mode="input", default=None, optionality='optional', view={"label": "Rate-on-Exposure - Offered",               "format": utils.percent_format(2)}),
                "roe_plan":                 hx.Float(mode="output",                                      view={"label": "Rate-on-Exposure - Plan",                  "format": utils.percent_format(2)}),
                "roe_technical":            hx.Float(mode="output",                                      view={"label": "Rate-on-Exposure - Technical",             "format": utils.percent_format(2)}),
                "roe_benchmark":            hx.Float(mode="output",                                      view={"label": "Rate-on-Exposure - Benchmark",             "format": utils.percent_format(2)}),
                #**standard_metrics() 
            }),


            "metrics_summary_pst_uwadj_term":     hx.Structure(view={"label": "Metrics\nPst-UWadj\nTerm"}, children={
                "roe_offered":              hx.Float(mode="output",                                      view={"label": "Rate-on-Exposure - Offered",               "format": utils.percent_format(2)}),
                "roe_plan":                 hx.Float(mode="output",                                      view={"label": "Rate-on-Exposure - Plan",                  "format": utils.percent_format(2)}),
                "roe_technical":            hx.Float(mode="output",                                      view={"label": "Rate-on-Exposure - Technical",             "format": utils.percent_format(2)}),
                "roe_benchmark":            hx.Float(mode="output",                                      view={"label": "Rate-on-Exposure - Benchmark",             "format": utils.percent_format(2)}),
                "credit_rating_bound":      hx.Str(  mode="output",                                      view={"label": "Bound Grade (implied)",                                                      }),
                "lgd_bound":                hx.Float(mode="output",                                      view={"label": "Bound LGD (implied)",                      "format": utils.percent_format(2)}),
                **standard_metrics() 
            }),


            "premium_composition_pre_uwadj_annual":     hx.Structure(view={"label": "Metrics\nPre-UWadj\nAnnual"}, children={   **premium_composition(coverage="total")                }),
            "premium_composition_pre_uwadj_term":       hx.Structure(view={"label": "Metrics\nPre-UWadj\nTerm"},   children={   **premium_composition(coverage="total")                }),
            "premium_composition_pst_uwadj_annual":     hx.Structure(view={"label": "Metrics\nPst-UWadj\nAnnual"}, children={   **premium_composition(coverage="total")                }),
            "premium_composition_pst_uwadj_term":       hx.Structure(view={"label": "Metrics\nPst-UWadj\nTerm"},   children={   **premium_composition(coverage="total")                }),





        }),  


    })


    