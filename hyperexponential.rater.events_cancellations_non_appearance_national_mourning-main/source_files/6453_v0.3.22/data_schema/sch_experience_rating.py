# v0.5.0
import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
from algorithms.rate_constants import max_layers

def sch_experience_rating(cds):
    grp_gnwp     = "Gross Net Premium (source currency)"
    grp_att_loss = "Attritional (source currency)"
    grp_lrg_loss = "Large (source currency)"
    grp_cat_loss = "Cat (source currency)"
    grp_assump   = "Assumptions"
    grp_onlevel  = "On-Levelling"
    grp_att_proj = "Attritional Projection"
    grp_lrg_proj = "Large Projection"
    grp_cat_proj = "CAT Projection"
    grp_tot_proj = "Total Projection"
    grp_actuary  = "Actuarial"
    grp_weight   = "Weight"
    grp_overall  = "Overall"
    

    cds.extend_node_rater_defined("cds/experience_rating", {
        # show/hide flags used to control the view
        "use_policy_ref_filter":   hx.Bool(mode="input",default=True, optionality="required", view={"label":"Filter data to only section ref"}),
        "evaluation_date":         hx.Date(mode="output",                                       view={"label": "Evaluation Date (date of data)"}),
        "evaluation_date_calc":    hx.Date(mode="output",                                       view={"label": "Evaluation Date est. (6mth prior incept)"}),
        "evaluation_date_ovd":     hx.Date(mode="input", default=None, optionality="optional",  view={"label": "Evaluation Date (if known)"},               async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),

        "el_cy_tiv":               hx.Float(mode="output",                                     view={"label": "Current Year TIV",               "format": thousands_format(0)}),
        "el_final_rate":           hx.Float(mode="output",                                     view={"label": "Final Loss Rate (per 000 TIV)",  "format": thousands_format(4)}),
        "el_final_calc":           hx.Float(mode="output",                                     view={"label": "Final Loss Cost Calculated",     "format": thousands_format(0)}),
        "el_final_ovd":            hx.Float(mode="input", default=None, optionality="optional",view={"label": "Final Loss Cost Override",       "format": thousands_format(0)}, async_output=["task_start_renewal"]), # we dont want the value carrying over on renewal
        "el_final":                hx.Float(mode="output",                                     view={"label": "Final Loss Cost Selected",       "format": thousands_format(0)}),

        "el_weight_calc":          hx.Float(mode="output",                                     view={"label": "Weight Calculated",      "format": percent_format(1)}),
        "el_weight_ovd":           hx.Float(mode="input", default=None, optionality="optional",view={"label": "Weight Override",        "format": percent_format(1)}, async_output=["task_start_renewal"]), # we dont want the value carrying over on renewal
        "el_weight":               hx.Float(mode="output",                                     view={"label": "Weight Selected",        "format": percent_format(1)}),
        "el_years":                hx.Int(  mode="output",                                     view={"label": "Number of years",        "format": thousands_format(0)}),
        "el_avg_exposure":         hx.Float(mode="output",                                     view={"label": "Avg Exposure",           "format": thousands_format(0)}),
        "el_avg_exposure_band":    hx.Float(mode="output",                                     view={"label": "Avg Exposure Band",      "format": thousands_format(0)}),

        "exposure_trend_backfill": hx.Float(mode="input", default=0,    optionality="required",view={"label": "Exposure Trend Backfill","format": percent_format(1)}),

        "policy_table": hx.List(mode="input", async_output=[{'task': 'task_sql_bi_data', 'reset': False}], children={
            "policy_ref":     hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Policy Reference"},         async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "section_ref":    hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Section Reference"},        async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "yoa":            hx.Int(  mode="input", default=None, optionality="optional",  view={"label": "YOA"},                      async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "coverage_name":  hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Coverage Name"},            async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "trifocus_name":  hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "TriFocus Name"},            async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "division":       hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Division"},                 async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "settlement_fx":  hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Settlement Currency"},      async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "index_bzly":     hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Index"},                    async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "class_code":     hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Class of Business Code"},   async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "bool_ec":        hx.Bool( mode="input", default=False,optionality="required",  view={"label": "Flag Event Cancellation"},  async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "bool_na":        hx.Bool( mode="input", default=False,optionality="required",  view={"label": "Flag Non Appearance"},      async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),

            # The financial figures are all in USD per the labels
            "gnwp_bzly_usd":    hx.Float(mode="input", default=None, optionality="optional", view={"label": "GNWP @ Beazley Share (USD)",    "format": thousands_format(0)}, async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "incurred_bzly_usd":hx.Float(mode="input", default=None, optionality="optional", view={"label": "Incurred @ Beazley Share (USD)","format": thousands_format(0)}, async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "gnwp_100_usd":     hx.Float(mode="input", default=None, optionality="optional", view={"label": "GNWP @ 100% (USD)",             "format": thousands_format(0)}, async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "incurred_100_usd": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Incurred @ 100% (USD)",         "format": thousands_format(0)}, async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "share_bzly":       hx.Float(mode="input", default=None, optionality="optional", view={"label": "Beazley Share",                 "format": percent_format(1)},   async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "rate_chg_init":    hx.Float(mode="input", default=None, optionality="optional", view={"label": "Rate Change Initial",           "format": percent_format(1)},   async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "rate_chg":         hx.Float(mode="input", default=None, optionality="optional", view={"label": "Rate Change Reformatted",       "format": percent_format(1)},   async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),

            # The financial figures translated to settlement fx per original policy
            "fx_rate_usd_sett": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Fx Rate to Sett Fx from BI USD",    "format": thousands_format(4)}, async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "gnwp_bzly":        hx.Float(mode="input", default=None, optionality="optional", view={"label": "GNWP @ Beazley Share (Sett Fx)",    "format": thousands_format(0)}, async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "incurred_bzly":    hx.Float(mode="input", default=None, optionality="optional", view={"label": "Incurred @ Beazley Share (Sett Fx)","format": thousands_format(0)}, async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "gnwp_100":         hx.Float(mode="input", default=None, optionality="optional", view={"label": "GNWP @ 100% (Sett Fx)",             "format": thousands_format(0)}, async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "incurred_100":     hx.Float(mode="input", default=None, optionality="optional", view={"label": "Incurred @ 100% (Sett Fx)",         "format": thousands_format(0)}, async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
 
            # The financial figures translated to source currency code (scc) per RENEWING POLICY
            "gnwp_bzly_scc":    hx.Float(mode="output",                                        view={"label": "GNWP @ Beazley Share (policy fx)",    "format": thousands_format(0)}),
            "incurred_bzly_scc":hx.Float(mode="output",                                        view={"label": "Incurred @ Beazley Share (policy fx)","format": thousands_format(0)}),
            "gnwp_100_scc":     hx.Float(mode="output",                                        view={"label": "GNWP @ 100% (policy fx)",             "format": thousands_format(0)}),
            "incurred_100_scc": hx.Float(mode="output",                                        view={"label": "Incurred @ 100% (policy fx)",         "format": thousands_format(0)}),
        }),


        "claim_table": hx.List(mode="input", async_output=[{'task': 'task_sql_bi_data', 'reset': False}], children={
            "policy_ref":     hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Policy Reference"},             async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "section_ref":    hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Section Reference"},            async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "claim_ref":      hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Claim Reference"},              async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "trifocus_name":  hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "TriFocus Name"},                async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "division":       hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Division"},                     async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "yoa":            hx.Int(  mode="input", default=None, optionality="optional",  view={"label": "YOA"},                          async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "settlement_fx":  hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Settlement Currency"},          async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),

            "cat_code_bzly":  hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Cat Code - Beazley"},           async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "cat_desc_bzly":  hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Cat Description - Beazley"},    async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "cat_code_mkt":   hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Cat Code - Market"},            async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "cat_desc_mkt":   hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Cat Description = Beazley"},    async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "cat_bzly_bool":  hx.Bool( mode="input", default=None, optionality="optional",  view={"label": "Cat Flag Beazley"},             async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),

            "cause_of_loss":  hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Cause of Loss"},                async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "bool_covid":     hx.Bool( mode="input", default=False,optionality="required",  view={"label": "Flag Covid"},                   async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "index_bzly":     hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Index"},                        async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),

            "class_code":     hx.Str(  mode="input", default=None, optionality="optional",  view={"label": "Class of Business Code"},       async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "bool_ec":        hx.Bool( mode="input", default=True, optionality="required",  view={"label": "Flag Event Cancellation"},      async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "bool_na":        hx.Bool( mode="input", default=False,optionality="required",  view={"label": "Flag Non Appearance"},          async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "bool_large":     hx.Bool( mode="output",                                       view={"label": "Flag Large"}),

            # The financial figures are in settlement currency without qualifications
            "incurred_bzly":  hx.Float(mode="input", default=None, optionality="optional",  view={"label": "Incurred @ Beazley Share Sett Fx",   "format": thousands_format(0)}, async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "os_bzly":        hx.Float(mode="input", default=None, optionality="optional",  view={"label": "Outstanding @ Beazley Share Sett Fx","format": thousands_format(0)}, async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "incurred_100":   hx.Float(mode="input", default=None, optionality="optional",  view={"label": "Incurred @ 100% Sett Fx",            "format": thousands_format(0)}, async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),
            "share_bzly":     hx.Float(mode="input", default=None, optionality="optional",  view={"label": "Beazley Share",                      "format": percent_format(1)},   async_output=[{'task': 'task_sql_bi_data', 'reset': False}]),

            # The financial figures translated to source currency code (scc) per RENEWING POLICY
            "incurred_bzly_scc": hx.Float(mode="output",                                    view={"label": "Incurred @ Beazley Share",   "format": thousands_format(0)}),
            "os_bzly_scc":       hx.Float(mode="output",                                    view={"label": "Outstanding @ Beazley Share","format": thousands_format(0)}),
            "incurred_100_scc":  hx.Float(mode="output",                                    view={"label": "Incurred @ 100%",            "format": thousands_format(0)}),

            "incurred_100_scc_attr":  hx.Float(mode="output",                                  view={"label": "Attritional Incurred @ 100% (policy fx)", "format": thousands_format(0)}),
            "incurred_100_scc_large": hx.Float(mode="output",                                  view={"label": "Large Incurred @ 100% (policy fx)",       "format": thousands_format(0)}),
            "incurred_100_scc_cat":   hx.Float(mode="output",                                  view={"label": "Cat Incurred @ 100% (policy fx)",         "format": thousands_format(0)}),
        }),


        "analysis_table": hx.List(mode="input",  async_input=["rarc_task"], async_output=["task_start_renewal"], default_element_count=10, children={
            "yoa":                   hx.Int(  mode="output",                                      view={"label": "YOA","group": "year"}),
            "yoa_label":             hx.Str(  mode="output",                                      view={"label": "YOA","group": "year"}),
            "include":               hx.Bool( mode="input", default=True,optionality="required",  view={"label": "Include",                                      "group": grp_overall                               }, async_output=["task_start_renewal"]),
            "tiv_calc":              hx.Float(mode="output",                                      view={"label": "Exposure TIV\nBackfilled\n(Source Currency)",  "group": grp_overall, "format": thousands_format(0)}),
            "tiv_ovd":               hx.Float(mode="input", default=None, optionality="optional", view={"label": "Exposure TIV\nOverride\n(Source Currency)",    "group": grp_overall, "format": thousands_format(0)}, async_output=["task_start_renewal"]),
            "tiv":                   hx.Float(mode="output",                                      view={"label": "Exposure TIV\n(Source Currency)",              "group": grp_overall, "format": thousands_format(0)}),
            "gnwp_ol_dup":                   hx.Float(mode="output",                              view={"label": "GN Premium -\nOnlevelled",                     "group": grp_overall, "format": thousands_format(0)}),
            "total_ol_selected_ultimate_dup":hx.Float(mode="output",                              view={"label": "Ultimate\nIncurred -\nInflated and\nProjected","group": grp_overall, "format": thousands_format(0)}),
            "total_ol_selected_ulr_dup":     hx.Float(mode="output",                              view={"label": "Total ULR -\nOn-Levelled\nand\nProjected",     "group": grp_overall, "format": percent_format(1)  }),
            "total_ol_selected_ult_to_tiv":  hx.Float(mode="output",                              view={"label": "Incurred per\nTIV(000s)",                      "group": grp_overall, "format": thousands_format(2)}),

            "gnwp_nominal_calc":     hx.Float(mode="output",                                      view={"label": "Gross Net\nPremium -\nLoaded from BI",  "group": grp_gnwp,"format": thousands_format(0)}),
            "gnwp_nominal_ovd":      hx.Float(mode="input",  default=None, optionality="optional",view={"label": "Gross Net\nPremium -\nOverride",        "group": grp_gnwp,"format": thousands_format(0)}           , async_output=["task_start_renewal"]),
            "gnwp_nominal":          hx.Float(mode="output",                                      view={"label": "Gross Net\nWritten\nPremium",           "group": grp_gnwp,"format": thousands_format(0)}),

            "attr_incurred_calc":    hx.Float(mode="output",                                      view={"label": "Incurred -\nLoaded from BI",            "group": grp_att_loss,"format": thousands_format(0)}),
            "attr_incurred_ovd":     hx.Float(mode="input",  default=None, optionality="optional",view={"label": "Incurred -\nOverride",                  "group": grp_att_loss,"format": thousands_format(0)}       , async_output=["task_start_renewal"]),
            "attr_incurred":         hx.Float(mode="output",                                      view={"label": "Incurred",                              "group": grp_att_loss,"format": thousands_format(0)}),
            "large_incurred_calc":   hx.Float(mode="output",                                      view={"label": "Incurred -\nLoaded from BI",            "group": grp_lrg_loss,"format": thousands_format(0)}),
            "large_incurred_ovd":    hx.Float(mode="input",  default=None, optionality="optional",view={"label": "Incurred -\nOverride",                  "group": grp_lrg_loss,"format": thousands_format(0)}       , async_output=["task_start_renewal"]),
            "large_incurred":        hx.Float(mode="output",                                      view={"label": "Incurred",                              "group": grp_lrg_loss,"format": thousands_format(0)}),
            "cat_incurred_calc":     hx.Float(mode="output",                                      view={"label": "Incurred -\nLoaded from BI",            "group": grp_cat_loss,"format": thousands_format(0)}),
            "cat_incurred_ovd":      hx.Float(mode="input",  default=None, optionality="optional",view={"label": "Incurred -\nOverride",                  "group": grp_cat_loss,"format": thousands_format(0)}       , async_output=["task_start_renewal"]),
            "cat_incurred":          hx.Float(mode="output",                                      view={"label": "Incurred",                              "group": grp_cat_loss,"format": thousands_format(0)}),

            "rate_inc_calc":          hx.Float(mode="output",                                     view={"label": "Rate\nChange -\nDefault",               "group": grp_assump,  "format": thousands_format(3)}),
            "rate_inc_ovd":           hx.Float(mode="input",default=None, optionality="optional", view={"label": "Rate\nChange -\nOverride",              "group": grp_assump,  "format": thousands_format(3)}       , async_output=["task_start_renewal"]),
            "rate_inc":               hx.Float(mode="output",                                     view={"label": "Rate\nChange",                          "group": grp_assump,  "format": thousands_format(3)}),
            "rate_cum":               hx.Float(mode="output",                                     view={"label": "Rate\nChange\nIndex",                   "group": grp_assump,  "format": thousands_format(3)}),
            "inf_inc_calc":           hx.Float(mode="output",                                     view={"label": "Inflation\n-\nDefault",                 "group": grp_assump,  "format": thousands_format(3)}),
            "inf_inc_ovd":            hx.Float(mode="input",default=None, optionality="optional", view={"label": "Inflation\n-\nOverride",                "group": grp_assump,  "format": thousands_format(3)}       , async_output=["task_start_renewal"]),
            "inf_inc":                hx.Float(mode="output",                                     view={"label": "Inflation",                             "group": grp_assump,  "format": thousands_format(3)}),
            "inf_cum":                hx.Float(mode="output",                                     view={"label": "Inflation\nIndex",                      "group": grp_assump,  "format": thousands_format(3)}),

            "attr_pct_ultimate_calc": hx.Float(mode="output",                                     view={"label": "%Ultimate\nAttritional -\nCalculated",  "group": grp_actuary, "format": percent_format(1)}),
            "attr_pct_ultimate_ovd":  hx.Float(mode="input",default=None, optionality="optional", view={"label": "%Ultimate\nAttritional -\nOverride",    "group": grp_actuary, "format": percent_format(1)}         , async_output=["task_start_renewal"]),
            "large_pct_ultimate_calc":hx.Float(mode="output",                                     view={"label": "%Ultimate\nLarge -\nCalculated",        "group": grp_actuary, "format": percent_format(1)}),
            "large_pct_ultimate_ovd": hx.Float(mode="input",default=None, optionality="optional", view={"label": "%Ultimate\nLarge -\nOverride",          "group": grp_actuary, "format": percent_format(1)}         , async_output=["task_start_renewal"]),
            "cat_pct_ultimate_calc":  hx.Float(mode="output",                                     view={"label": "%Ultimate\nCat -\nCalculated",          "group": grp_actuary, "format": percent_format(1)}),
            "cat_pct_ultimate_ovd":   hx.Float(mode="input",default=None, optionality="optional", view={"label": "%Ultimate\nCat -\nOverride",            "group": grp_actuary, "format": percent_format(1)}         , async_output=["task_start_renewal"]),
            "attr_ielr_calc":         hx.Float(mode="output",                                     view={"label": "IELR\nAttritional -\nCalculated",       "group": grp_actuary, "format": percent_format(1)}),
            "attr_ielr_ovd":          hx.Float(mode="input",default=None, optionality="optional", view={"label": "IELR\nAttritional -\nOverride",         "group": grp_actuary, "format": percent_format(1)}         , async_output=["task_start_renewal"]),
            "large_ielr_calc":        hx.Float(mode="output",                                     view={"label": "IELR\nLarge -\nCalculated",             "group": grp_actuary, "format": percent_format(1)}),
            "large_ielr_ovd":         hx.Float(mode="input",default=None, optionality="optional", view={"label": "IELR\nLarge -\nOverride",               "group": grp_actuary, "format": percent_format(1)}         , async_output=["task_start_renewal"]),
            "cat_ielr_calc":          hx.Float(mode="output",                                     view={"label": "IELR\nCat -\nCalculated",               "group": grp_actuary, "format": percent_format(1)}),
            "cat_ielr_ovd":           hx.Float(mode="input",default=None, optionality="optional", view={"label": "IELR\nCat -\n Override",                "group": grp_actuary, "format": percent_format(1)}         , async_output=["task_start_renewal"]),

            "gnwp_ol":                hx.Float(mode="output",                                      view={"label": "Gross Net\nPremium -\nOn-Levelled",    "group": grp_onlevel, "format": thousands_format(0)}),
            "attr_ol_incurred":       hx.Float(mode="output",                                      view={"label": "Attritional\nIncurred -\nInflated",    "group": grp_onlevel, "format": thousands_format(0)}),
            "large_ol_incurred":      hx.Float(mode="output",                                      view={"label": "Large\nIncurred -\nInflated",          "group": grp_onlevel, "format": thousands_format(0)}),
            "cat_ol_incurred":        hx.Float(mode="output",                                      view={"label": "Cat\nIncurred -\nInflated",            "group": grp_onlevel, "format": thousands_format(0)}),
            "total_ol_incurred":      hx.Float(mode="output",                                      view={"label": "Total\nIncurred -\nInflated",          "group": grp_onlevel, "format": thousands_format(0)}),


            "attr_pct_ultimate":         hx.Float(mode="output", view={"label": "Development\nPattern",          "group": grp_att_proj, "format": percent_format(1)  }),
            "attr_method":               hx.Str(  mode="output", view={"label": "Method",                        "group": grp_att_proj                               }),
            "attr_ol_cl_ultimate":       hx.Float(mode="output", view={"label": "CL -\nUltimate\nIncurred",      "group": grp_att_proj, "format": thousands_format(0)}),
            "attr_ol_bf_ultimate":       hx.Float(mode="output", view={"label": "BF -\nUltimate\nIncurred",      "group": grp_att_proj, "format": thousands_format(0)}),
            "attr_ol_ielr_ultimate":     hx.Float(mode="output", view={"label": "IELR -\nUltimate\nIncurred",    "group": grp_att_proj, "format": thousands_format(0)}),
            "attr_ol_selected_ultimate": hx.Float(mode="output", view={"label": "Attritional\nFinal\nIncurred",  "group": grp_att_proj, "format": thousands_format(0)}),
            "attr_ol_cl_lr":             hx.Float(mode="output", view={"label": "CL ULR",                        "group": grp_att_proj, "format": percent_format(1)  }),
            "attr_ol_bf_lr":             hx.Float(mode="output", view={"label": "BF ULR",                        "group": grp_att_proj, "format": percent_format(1)  }),
            "attr_ol_ielr":              hx.Float(mode="output", view={"label": "IELR",                          "group": grp_att_proj, "format": percent_format(1)  }),
            "attr_ol_selected_ulr":      hx.Float(mode="output", view={"label": "Attritional\nFinal\nULR",       "group": grp_att_proj, "format": percent_format(1)  }),

            "large_pct_ultimate":        hx.Float(mode="output", view={"label": "Large\nDevelopment\nPattern",   "group": grp_lrg_proj, "format": percent_format(1)  }),
            "large_method":              hx.Str(  mode="output", view={"label": "Method",                        "group": grp_lrg_proj                               }),
            "large_credibility":         hx.Float(mode="output", view={"label": "Large\nCredibility",            "group": grp_lrg_proj, "format": percent_format(1)  }),
            "large_ol_cl_ultimate":      hx.Float(mode="output", view={"label": "Large\nCL -\nFinal\nIncurred",  "group": grp_lrg_proj, "format": thousands_format(0)}),
            "large_ol_bf_ultimate":      hx.Float(mode="output", view={"label": "Large\nBF -\nFinal\nIncurred",  "group": grp_lrg_proj, "format": thousands_format(0)}),
            "large_ol_ielr_ultimate":    hx.Float(mode="output", view={"label": "Large\nIELR -\nFinal\nIncurred","group": grp_lrg_proj, "format": thousands_format(0)}),
            "large_ol_selected_ultimate":hx.Float(mode="output", view={"label": "Large\nFinal\nIncurred",        "group": grp_lrg_proj, "format": thousands_format(0)}),
            "large_ol_cl_lr":            hx.Float(mode="output", view={"label": "Large\nCL ULR",                 "group": grp_lrg_proj, "format": percent_format(1)  }),
            "large_ol_bf_lr":            hx.Float(mode="output", view={"label": "Large\nBF ULR",                 "group": grp_lrg_proj, "format": percent_format(1)  }),
            "large_ol_ielr":             hx.Float(mode="output", view={"label": "Large\nIELR",                   "group": grp_lrg_proj, "format": percent_format(1)  }),
            "large_ol_selected_ulr":     hx.Float(mode="output", view={"label": "Large\nFinal\nULR",             "group": grp_lrg_proj, "format": percent_format(1)  }),

            "cat_pct_ultimate":          hx.Float(mode="output", view={"label": "Cat\nDevelopment\nPattern",     "group": grp_cat_proj, "format": percent_format(1)  }),
            "cat_method":                hx.Str(  mode="output", view={"label": "Method",                        "group": grp_cat_proj                               }),
            "cat_ol_cl_ultimate":        hx.Float(mode="output", view={"label": "Cat\nCL -\nFinal\nIncurred",    "group": grp_cat_proj, "format": thousands_format(0)}),
            "cat_ol_bf_ultimate":        hx.Float(mode="output", view={"label": "Cat\nBF -\nFinal\nIncurred",    "group": grp_cat_proj, "format": thousands_format(0)}),
            "cat_ol_ielr_ultimate":      hx.Float(mode="output", view={"label": "Cat\nIELR -\nFinal\nIncurred",  "group": grp_cat_proj, "format": thousands_format(0)}),
            "cat_ol_selected_ultimate":  hx.Float(mode="output", view={"label": "Cat\nFinal\nIncurred",          "group": grp_cat_proj, "format": thousands_format(0)}),
            "cat_ol_cl_lr":              hx.Float(mode="output", view={"label": "Cat\nCL ULR",                   "group": grp_cat_proj, "format": percent_format(1)  }),
            "cat_ol_bf_lr":              hx.Float(mode="output", view={"label": "Cat\nBF ULR",                   "group": grp_cat_proj, "format": percent_format(1)  }),
            "cat_ol_ielr":               hx.Float(mode="output", view={"label": "Cat\nIELR\n(BP)",               "group": grp_cat_proj, "format": percent_format(1)  }),
            "cat_ol_selected_ulr":       hx.Float(mode="output", view={"label": "Cat\nFinal\nULR",               "group": grp_cat_proj, "format": percent_format(1)  }),

            "total_pct_ultimate":        hx.Float(mode="output", view={"label": "Total\nDevelopment\nPattern",   "group": grp_tot_proj, "format": percent_format(1)  }),
            "total_ol_cl_ultimate":      hx.Float(mode="output", view={"label": "Total\nCL -\nFinal\nIncurred",  "group": grp_tot_proj, "format": thousands_format(0)}),
            "total_ol_bf_ultimate":      hx.Float(mode="output", view={"label": "Total\nBF -\nFinal\nIncurred",  "group": grp_tot_proj, "format": thousands_format(0)}),
            "total_ol_ielr_ultimate":    hx.Float(mode="output", view={"label": "Total\nIELR -\nFinal\nIncurred","group": grp_tot_proj, "format": thousands_format(0)}),
            "total_ol_selected_ultimate":hx.Float(mode="output", view={"label": "Total\nFinal\nIncurred",        "group": grp_tot_proj, "format": thousands_format(0)}),
            "total_ol_cl_lr":            hx.Float(mode="output", view={"label": "Total\nCL ULR",                 "group": grp_tot_proj, "format": percent_format(1)  }),
            "total_ol_bf_lr":            hx.Float(mode="output", view={"label": "Total\nBF ULR",                 "group": grp_tot_proj, "format": percent_format(1)  }),
            "total_ol_ielr":             hx.Float(mode="output", view={"label": "Total\nIELR",                   "group": grp_tot_proj, "format": percent_format(1)  }),
            "total_ol_selected_ulr":     hx.Float(mode="output", view={"label": "Total\nFinal\nULR",             "group": grp_tot_proj, "format": percent_format(1)  }),

            "wgt_include":          hx.Float(mode="output", view={"label": "Include",                            "group": grp_weight,"format": thousands_format(3)}),
            "wgt_decay":            hx.Float(mode="output", view={"label": "Decay\nFactor",                      "group": grp_weight,"format": thousands_format(3)}),
            "wgt_exposure":         hx.Float(mode="output", view={"label": "Exposure\nFactor",                   "group": grp_weight,"format": thousands_format(3)}),
            "wgt_pct_ult":          hx.Float(mode="output", view={"label": "Development\nFactor",                "group": grp_weight,"format": thousands_format(3)}),
            "wgt_overall_initial":  hx.Float(mode="output", view={"label": "Overall\n(intermediate)",            "group": grp_weight,"format": thousands_format(3)}),
            "wgt_overall_final":    hx.Float(mode="output", view={"label": "Overall\n(Final)",                   "group": grp_weight,"format": thousands_format(3)}),
        }),

        "analysis_table_total_included": hx.Structure(children={
            "yoa_label":             hx.Str(  mode="output", view={"label": "YOA",                      "group": "year"}),
            "tiv_calc":              hx.Float(mode="output", view={"label": "Exposure TIV\nBackfilled\n(Source Currency)",  "group": grp_overall, "format": thousands_format(0)}),
            "tiv_ovd":               hx.Float(mode="output", view={"label": "Exposure TIV\nOverride\n(Source Currency)",    "group": grp_overall, "format": thousands_format(0)}),
            "tiv":                   hx.Float(mode="output", view={"label": "Exposure TIV\n(Source Currency)",              "group": grp_overall, "format": thousands_format(0)}),
            "gnwp_ol_dup":                   hx.Float(mode="output",                              view={"label": "GN Premium -\nOnlevelled",                     "group": grp_overall, "format": thousands_format(0)}),
            "total_ol_selected_ultimate_dup":hx.Float(mode="output",                              view={"label": "Ultimate\nIncurred -\nInflated and\nProjected","group": grp_overall, "format": thousands_format(0)}),
            "total_ol_selected_ulr_dup":     hx.Float(mode="output",                              view={"label": "Total ULR -\nOn-Levelled\nand\nProjected",     "group": grp_overall, "format": percent_format(1)  }),
        }),


        "analysis_table_total": hx.Structure(children={
            "yoa_label":             hx.Str(  mode="output", view={"label": "YOA",                      "group": "year"}),
            "gnwp_ol":                hx.Float(mode="output",                                      view={"label": "Gross Net\nPremium -\nOn-Levelled",                     "group": grp_onlevel, "format": thousands_format(0)}),
            "attr_ol_incurred":       hx.Float(mode="output",                                      view={"label": "Attritional\nIncurred -\nInflated",                              "group": grp_onlevel, "format": thousands_format(0)}),
            "large_ol_incurred":      hx.Float(mode="output",                                      view={"label": "Large\nIncurred -\nInflated",                              "group": grp_onlevel, "format": thousands_format(0)}),
            "cat_ol_incurred":        hx.Float(mode="output",                                      view={"label": "Cat\nIncurred -\nInflated",                              "group": grp_onlevel, "format": thousands_format(0)}),
            "total_ol_incurred":      hx.Float(mode="output",                                      view={"label": "Total\nIncurred -\nInflated",                              "group": grp_onlevel, "format": thousands_format(0)}),

            "attr_ol_cl_ultimate":       hx.Float(mode="output", view={"label": "CL -\nUltimate\nIncurred",      "group": grp_att_proj, "format": thousands_format(0)}),
            "attr_ol_bf_ultimate":       hx.Float(mode="output", view={"label": "BF -\nUltimate\nIncurred",      "group": grp_att_proj, "format": thousands_format(0)}),
            "attr_ol_ielr_ultimate":     hx.Float(mode="output", view={"label": "IELR -\nUltimate\nIncurred",    "group": grp_att_proj, "format": thousands_format(0)}),
            "attr_ol_selected_ultimate": hx.Float(mode="output", view={"label": "Attritional\nFinal\nIncurred",  "group": grp_att_proj, "format": thousands_format(0)}),
            "attr_ol_cl_lr":             hx.Float(mode="output", view={"label": "CL ULR",                        "group": grp_att_proj, "format": percent_format(1)  }),
            "attr_ol_ielr":              hx.Float(mode="output", view={"label": "IELR",                          "group": grp_att_proj, "format": percent_format(1)  }),
            "attr_ol_bf_lr":             hx.Float(mode="output", view={"label": "BF ULR",                        "group": grp_att_proj, "format": percent_format(1)  }),
            "attr_ol_selected_ulr":      hx.Float(mode="output", view={"label": "Attritional\nFinal\nULR",       "group": grp_att_proj, "format": percent_format(1)  }),

            "large_ol_cl_ultimate":      hx.Float(mode="output", view={"label": "Large\nCL -\nFinal\nIncurred",  "group": grp_lrg_proj, "format": thousands_format(0)}),
            "large_ol_bf_ultimate":      hx.Float(mode="output", view={"label": "Large\nBF -\nFinal\nIncurred",  "group": grp_lrg_proj, "format": thousands_format(0)}),
            "large_ol_ielr_ultimate":    hx.Float(mode="output", view={"label": "Large\nIELR -\nFinal\nIncurred","group": grp_lrg_proj, "format": thousands_format(0)}),
            "large_ol_selected_ultimate":hx.Float(mode="output", view={"label": "Large\nFinal\nIncurred",        "group": grp_lrg_proj, "format": thousands_format(0)}),
            "large_ol_cl_lr":            hx.Float(mode="output", view={"label": "Large\nCL ULR",                 "group": grp_lrg_proj, "format": percent_format(1)  }),
            "large_ol_ielr":             hx.Float(mode="output", view={"label": "Large\nIELR",                   "group": grp_lrg_proj, "format": percent_format(1)  }),
            "large_ol_bf_lr":            hx.Float(mode="output", view={"label": "Large\nBF ULR",                 "group": grp_lrg_proj, "format": percent_format(1)  }),
            "large_ol_selected_ulr":     hx.Float(mode="output", view={"label": "Large\nFinal\nULR",             "group": grp_lrg_proj, "format": percent_format(1)  }),

            "cat_ol_cl_ultimate":        hx.Float(mode="output", view={"label": "Cat\nCL -\nFinal\nIncurred",    "group": grp_cat_proj, "format": thousands_format(0)}),
            "cat_ol_bf_ultimate":        hx.Float(mode="output", view={"label": "Cat\nBF -\nFinal\nIncurred",    "group": grp_cat_proj, "format": thousands_format(0)}),
            "cat_ol_ielr_ultimate":      hx.Float(mode="output", view={"label": "Cat\nIELR -\nFinal\nIncurred",  "group": grp_cat_proj, "format": thousands_format(0)}),
            "cat_ol_selected_ultimate":  hx.Float(mode="output", view={"label": "Cat\nFinal\nIncurred",          "group": grp_cat_proj, "format": thousands_format(0)}),
            "cat_ol_cl_lr":              hx.Float(mode="output", view={"label": "Cat\nCL ULR",                   "group": grp_cat_proj, "format": percent_format(1)  }),
            "cat_ol_ielr":               hx.Float(mode="output", view={"label": "Cat\nIELR\n(BP)",               "group": grp_cat_proj, "format": percent_format(1)  }),
            "cat_ol_bf_lr":              hx.Float(mode="output", view={"label": "Cat\nBF ULR",                   "group": grp_cat_proj, "format": percent_format(1)  }),
            "cat_ol_selected_ulr":       hx.Float(mode="output", view={"label": "Cat\nFinal\nULR",               "group": grp_cat_proj, "format": percent_format(1)  }),

            "total_ol_cl_ultimate":      hx.Float(mode="output", view={"label": "Total\nCL -\nFinal\nIncurred",  "group": grp_tot_proj, "format": thousands_format(0)}),
            "total_ol_bf_ultimate":      hx.Float(mode="output", view={"label": "Total\nBF -\nFinal\nIncurred",  "group": grp_tot_proj, "format": thousands_format(0)}),
            "total_ol_ielr_ultimate":    hx.Float(mode="output", view={"label": "Total\nIELR -\nFinal\nIncurred","group": grp_tot_proj, "format": thousands_format(0)}),
            "total_ol_selected_ultimate":hx.Float(mode="output", view={"label": "Total\nFinal\nUltimate",        "group": grp_tot_proj, "format": thousands_format(0)}),
            "total_ol_cl_lr":            hx.Float(mode="output", view={"label": "Total\nCL ULR",                 "group": grp_tot_proj, "format": percent_format(1)  }),
            "total_ol_ielr":             hx.Float(mode="output", view={"label": "Total\nIELR",                   "group": grp_tot_proj, "format": percent_format(1)  }),
            "total_ol_bf_lr":            hx.Float(mode="output", view={"label": "Total\nBF ULR",                 "group": grp_tot_proj, "format": percent_format(1)  }),
            "total_ol_selected_ulr":     hx.Float(mode="output", view={"label": "Total\nFinal\nULR",             "group": grp_tot_proj, "format": percent_format(1)  }),
        }),

        "analysis_table_cy": hx.Structure(children={
            "yoa_label":             hx.Str(  mode="output", view={"label": "YOA",                      "group": "year"}),
            "tiv_calc":              hx.Float(mode="output", view={"label": "Exposure TIV\nBackfilled\n(Source Currency)",  "group": grp_overall, "format": thousands_format(0)}),
            "tiv":                   hx.Float(mode="output", view={"label": "Exposure TIV\n(Source Currency)",              "group": grp_overall, "format": thousands_format(0)}),

            "rate_inc_calc":         hx.Float(mode="output", view={"label": "Rate\nChange -\nDefault",               "group": grp_assump,  "format": thousands_format(3)}),
            "rate_inc":              hx.Float(mode="output", view={"label": "Rate\nChange",                          "group": grp_assump,  "format": thousands_format(3)}),
            "rate_cum":              hx.Float(mode="output", view={"label": "Rate\nChange\nIndex",                   "group": grp_assump,  "format": thousands_format(3)}),
            "inf_inc_calc":          hx.Float(mode="output", view={"label": "Inflation\n-\nDefault",                 "group": grp_assump,  "format": thousands_format(3)}),
            "inf_inc":               hx.Float(mode="output", view={"label": "Inflation",                             "group": grp_assump,  "format": thousands_format(3)}),
            "inf_cum":               hx.Float(mode="output", view={"label": "Inflation\nIndex",                      "group": grp_assump,  "format": thousands_format(3)}),
        })


    })
