import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

def sch_experience_rating(cds):

    cds.extend_node_rater_defined("cds/experience_rating", {
        "er_calcs": hx.List(mode="input", default_element_count=8, min_element_count=8, max_element_count=8, children={
            "include": hx.Bool(mode="input", default=True,view={"label": "Include?"}),
            "yoa": hx.Int(mode="output", view={"label": "YOA", "format": integer_format(0)}),
            "yoa_label": hx.Str(mode="output", view={"label": "YOA"}),
            "exp_non_ed": hx.Int(mode="input", async_output=["backfill_exposure"], default=None, optionality="optional", view={"label": "Non-Education\nNumber of\nEstablishments", "group": "Exposure", "format": integer_format(0)}, validation={"min_value": 0}),
            "exp_ed": hx.Int(mode="input", async_output=["backfill_exposure"], default=None, optionality="optional", view={"label": "Education\nNumber of\nSchools", "group": "Exposure", "format": integer_format(0)}, validation={"min_value": 0}),
            "sel_exp_base": hx.Int(mode="output", view={"label": "Selected\nExposure\nBase", "group": "Exposure", "format": integer_format(0)}),
            "gnwp": hx.Float(mode="output", view={"label": "GNWP", "group": "Gross Net Premium (USD 000s)", "format": thousands_format(0)}),
            "rate_change": hx.Float(mode="output", view={"label": "Rate Change",  "group": "Gross Net Premium (USD 000s)", "format": percent_format(0)}),
            "rate_change_index": hx.Float(mode="output", view={"label": "Rate Change\nIndex", "group": "Gross Net Premium (USD 000s)", "format": percent_format(0)}),
            "on_level_premium": hx.Float(mode="output", view={"label": "On-Levelled\nPremium", "group": "Gross Net Premium (USD 000s)", "format": thousands_format(0)}),

            "attrition_incurred": hx.Float(mode="output", view={"label": "Incurred", "group": "Attritional Projection (USD 000s)", "format": thousands_format(0)}),
            "attrition_dev_factor": hx.Float(mode="output", view={"label": "Dev\nFactor", "group": "Attritional Projection (USD 000s)", "format": percent_format(0)}),
            "attrition_ielr": hx.Float(mode="output", view={"label": "IELR", "group": "Attritional Projection (USD 000s)", "format": percent_format(0)}),
            "attrition_ult_claims": hx.Float(mode="output", view={"label": "Ult Claims", "group": "Attritional Projection (USD 000s)", "format": thousands_format(0)}),
            "attrition_on_level_ulr": hx.Float(mode="output", view={"label": "On-Levelled\nULR", "group": "Attritional Projection (USD 000s)", "format": percent_format(0)}),

            "large_incurred": hx.Float(mode="output", view={"label": "Incurred", "group": "Large Loss Projection (USD 000s)", "format": thousands_format(0)}),
            "large_avg_lr": hx.Float(mode="output", view={"label": "Average\nLL LR", "group": "Large Loss Projection (USD 000s)", "format": percent_format(1)}),
            "large_ll_assumption": hx.Float(mode="output", view={"label": "LL\nAssumption", "group": "Large Loss Projection (USD 000s)", "format": percent_format(1)}),
            "large_weighted_ll": hx.Float(mode="output", view={"label": "Weighted\nLL", "group": "Large Loss Projection (USD 000s)", "format": percent_format(1)}),
            "large_ult_claims": hx.Float(mode="output", view={"label": "Ult Claims", "group": "Large Loss Projection (USD 000s)", "format": thousands_format(0)}),
            "large_ulr": hx.Float(mode="output", view={"label": "ULR", "group": "Large Loss Projection (USD 000s)", "format": percent_format(0)}),

            "cat_incurred": hx.Float(mode="output", view={"label": "Incurred", "group": "Cat Claims Projection (USD 000s)", "format": thousands_format(0)}),
            "cat_avg": hx.Float(mode="output", view={"label": "Average", "group": "Cat Claims Projection (USD 000s)", "format": thousands_format(0)}),
            "cat_rms_or_bp": hx.Float(mode="output", view={"label": "BP Implied", "group": "Cat Claims Projection (USD 000s)", "format": thousands_format(0)}),
            "cat_bp": hx.Float(mode="output", view={"label": "BP Implied", "group": "Total Projection (USD 000s)", "format": thousands_format(0)}),
            "cat_ult_claims": hx.Float(mode="output", view={"label": "Ult Claims", "group": "Cat Claims Projection (USD 000s)", "format": thousands_format(0)}),
            "cat_ulr": hx.Float(mode="output", view={"label": "ULR", "group": "Cat Claims Projection (USD 000s)", "format": percent_format(1)}),
            #Added 15/04/25 SB
            "total_att_ll_incurred": hx.Float(mode="output", view={"label": "Attr + LL\nIncurred", "group": "Total Projection (USD 000s)", "format": thousands_format(0)}),
            "total_att_ll_dev_factor": hx.Float(mode="output", view={"label": "Dev\nFactor", "group": "Total Projection (USD 000s)", "format": percent_format(0)}),
            "total_att_ll_ielr": hx.Float(mode="output", view={"label": "IELR", "group": "Total Projection (USD 000s)", "format": percent_format(0)}),
            "total_ult_claims": hx.Float(mode="output", view={"label": "Ult Claims", "group": "Total Projection (USD 000s)", "format": thousands_format(0)}),
            "total_on_level_ulr": hx.Float(mode="output", view={"label": "On-Levelled\nULR", "group": "Total Projection (USD 000s)", "format": percent_format(0)}),
            "attrition_ll_ult_claims": hx.Float(mode="output", view={"label": "Attr + LL\nIncurred", "group": "Total Projection (USD 000s)", "format": thousands_format(0)}),

            "ultimate_claims": hx.Float(mode="output", view={"label": "Ultimate\nClaims", "group": "Ultimate Claims (USD 000s)", "format": thousands_format(0)}),
            "infl_index": hx.Float(mode="output", view={"label": "Infl Index", "group": "Ultimate Claims (USD 000s)", "format": percent_format(0)}),
            "inf_ultimate": hx.Float(mode="output", view={"label": "Inf Ultimate", "group": "Ultimate Claims (USD 000s)", "format": thousands_format(0)}),

            "user_input_att": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Attritional", "group": "Incurred Claims (USD 000s)", "format": thousands_format(0)}, validation={"min_value": 0}),
            "user_input_large": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Large", "group": "Incurred Claims (USD 000s)", "format": thousands_format(0)}, validation={"min_value": 0}),
            "user_input_cat": hx.Float(mode="input", default=None, optionality="optional", view={"label": "CAT", "group": "Incurred Claims (USD 000s)", "format": thousands_format(0)}, validation={"min_value": 0}),
            #Added 15/04/25 SB
            "user_input_att_ll_total": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Total", "group": "Incurred Claims (USD 000s)", "format": thousands_format(0)}, validation={"min_value": 0}),
            "user_input_gnwp": hx.Float(mode="input", default=None, optionality="optional", view={"label": "GNWP", "group": "Gross Net Premium (USD 000s)", "format": thousands_format(0)}, validation={"min_value": 0}),
            "user_input_rate_change": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Rate Change", "group": "Gross Net Premium (USD 000s)", "format": percent_format(0)}, validation={"min_value": 0}),
            "user_input_num_claims": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Number Of\nClaims", "format": integer_format(0)}, validation={"min_value": 0}),
            "user_input_total_paid": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Total\nPaid", "format": {"thousandSeparated": True, "mantissa": 0}}),

            "user_input_num_incidents": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Number of\nIncidents","group": "Frequency", "format": integer_format(0)}, validation={"min_value": 0}),
            "user_input_num_deaths": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Number of\nDeaths","group": "Frequency","format": integer_format(0)}, validation={"min_value": 0}),
            "user_input_num_injuries": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Number of\nInjuries","group": "Frequency", "format": integer_format(0)}, validation={"min_value": 0}),
            "num_incidents": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Number of\nIncidents","group": "Frequency", "format": integer_format(0)}, validation={"min_value": 0}),
            "num_deaths": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Number of\nDeaths","group": "Frequency","format": integer_format(0)}, validation={"min_value": 0}),
            "num_injuries": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Number of\nInjuries","group": "Frequency", "format": integer_format(0)}, validation={"min_value": 0}),
            "user_input_incurred_total": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Incurred\nClaims", "group": "Incurred Claims (USD 000s)", "format": thousands_format(0)}, validation={"min_value": 0}),
            "frequency_ult_claims": hx.Float(mode="output", view={"label": "Ultimate\nClaims", "group": "Ultimate Claims (USD 000s)", "format": thousands_format(0)}),
            "frequency_infl_index": hx.Float(mode="output", view={"label": "Infl Index", "group": "Ultimate Claims (USD 000s)", "format": percent_format(0)}),
            "frequency_inf_ultimate": hx.Float(mode="output", view={"label": "Inf Ultimate\n Claims", "group": "Ultimate Claims (USD 000s)", "format": thousands_format(0)}),
            "sel_infl_index": hx.Float(mode="output", view={"label": "Infl Index", "group": "Ultimate Claims (USD 000s)", "format": percent_format(0)}),
        }),

        "curr_yr": hx.Structure(children={
            "yoa": hx.Int(mode="output", view={"label": "YOA", "format": integer_format(0)}),
            "yoa_label": hx.Str(mode="output", view={"label": "YOA"}),
            "exp_non_ed": hx.Int(mode="input", async_input=["backfill_exposure"], default=None, optionality="optional", view={"label": "Non-Education\nNumber of\nEstablishments", "group": "Exposure", "format": integer_format(0)}, validation={"min_value": 0}),
            "exp_ed": hx.Int(mode="input", async_input=["backfill_exposure"], default=None, optionality="optional", view={"label": "Education\nNumber of\nSchools", "group": "Exposure", "format": integer_format(0)}, validation={"min_value": 0}),
            "sel_exp_base": hx.Int(mode="output", view={"label": "Selected\nExposure\nBase", "group": "Exposure", "format": integer_format(0)}),
            "rate_change": hx.Float(mode="output", view={"label": "Rate Change",  "group": "Gross Net Premium (USD 000s)", "format": percent_format(0)}),
            "user_input_rate_change": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Rate Change", "group": "Gross Net Premium (USD 000s)", "format": percent_format(0)}, validation={"min_value": 0}),
        }),

        "er_totals": hx.Structure(children={
            "yoa": hx.Str(mode="output"),
            "gnwp": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "exp_non_ed": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "exp_ed": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "sel_exp_base": hx.Float(mode="output", view={"format": thousands_format(0)}),           
            "on_level_premium": hx.Float(mode="output", view={"format": thousands_format(0)}),

            "attrition_incurred": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "attrition_ult_claims": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "attrition_on_level_ulr": hx.Float(mode="output", view={"format": percent_format(0)}),
            "large_incurred": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "large_ult_claims": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "large_ulr": hx.Float(mode="output", view={"format": percent_format(0)}),
            "cat_incurred": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "cat_ult_claims": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "cat_ulr": hx.Float(mode="output", view={"format": percent_format(0)}),
            "ultimate_claims": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "inf_ultimate": hx.Float(mode="output", view={"format": thousands_format(0)}),
            #Added 15/04/25 SB
            "total_att_ll_incurred": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "frequency_ult_claims": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "frequency_inf_ultimate": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "num_incidents":hx.Float(mode="output", view={"format": thousands_format(0)}),
            "num_deaths": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "num_injuries": hx.Float(mode="output", view={"format": thousands_format(0)}),

            "user_input_att": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "user_input_large": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "user_input_cat": hx.Float(mode="output", view={"format": thousands_format(0)}),
            #Added 15/04/25 SB
            "user_input_att_ll_total": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "user_input_gnwp": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "user_input_num_incidents":hx.Float(mode="output", view={"format": thousands_format(0)}),
            "user_input_num_deaths": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "user_input_num_injuries": hx.Float(mode="output", view={"format": thousands_format(0)}),
            "user_input_incurred_total": hx.Float(mode="output", view={"format": thousands_format(0)}),
        }),

        "er_chart_data": hx.List(mode="output", children={
            "yoa": hx.Float(mode="output"),
            "exp_non_ed_perc": hx.Float(mode="output"),
            "exp_ed_perc": hx.Float(mode="output"),
            "gnwp_perc": hx.Float(mode="output"),
         }),

        "bi_policy_data": hx.List(mode="input", async_output=["sql_bi_fetch_task", "sql_bi_clear"], children={
            "PolicyReference": hx.Str(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Policy\nReference"}),
            "SectionReference": hx.Str(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Section\nReference"}),
            "TriFocusName": hx.Str(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "TriFocus\nName"}),
            "ClassOfBusinessCode": hx.Str(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "COB\nCode"}),
            "StatsCode": hx.Str(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Stats\nCode"}),
            "YOA": hx.Int(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "YOA", "format": integer_format(0)}),
            "SettlementCurrency": hx.Str(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Settlement\nCurrency"}),
            "ExternalAcquisitionCostMultiplier": hx.Float(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Acquisition\nCost"}),
            "WrittenOrEstimatedPremium": hx.Float(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Written\nPremium", "format": thousands_format(0)}),
            "RateChangeDivisor": hx.Float(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Rate Change\nDivisor", "format": percent_format(0)}),
            "BenchmarkPremium": hx.Float(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Benchmark\nPremium", "format": thousands_format(0)}),
            "TotalWrittenIfNotSignedMultiplier": hx.Float(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Signed\nLine", "format": percent_format(0)})
         }),

        "bi_claim_data": hx.List(mode="input", async_output=["sql_bi_fetch_task", "sql_bi_clear"], children={
            "PolicyReference": hx.Str(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Policy\nReference"}),
            "SectionReference": hx.Str(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Section\nReference"}),
            "TriFocusName": hx.Str(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "TriFocus\nName"}),
            "YOA": hx.Int(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "YOA", "format": integer_format(0)}),
            "ClaimReference": hx.Str(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Claim\nReference"}),
            "MarketCatCode": hx.Str(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Market Cat\nCode"}),
            "BeazleyShareTotalPaidInUSD": hx.Float(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Paid\nUSD", "format": thousands_format(0)}),
            "BeazleyShareTotalOutstandingInUSD": hx.Float(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Outstanding\nUSD", "format": thousands_format(0)}),
            "BeazleyShareTotalIncurredInUSD": hx.Float(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Incurred\nUSD", "format": thousands_format(0)}),
            "SettlementCurrency": hx.Str(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Settlement\nCurrency"}),
            "SlipOrderTotalIncurred": hx.Float(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Slip Order\nTotal Incurred", "format": thousands_format(0)}),
            "SignedLineMultiplier": hx.Float(mode="input", default=None, optionality="optional", async_output=["sql_bi_fetch_task"], view={"label": "Signed\nLine", "format": percent_format(0)})
         }),


        "cat_rms_or_bp": hx.Float(mode="override", view={"label": "RMS / Business Plan Cat LR", "format": percent_format(2)}),
        "data_source": hx.Str(mode="input", default_index=0, options=["Import from BI", "User to input data"], view={"label": "Data Source"}),
        "final_burning_cost": hx.Float(mode="output", view={"label": "FINAL SELECTION - BURNING COST", "format": thousands_format(0)}),
        "credibility_weight": hx.Float(mode="output", view={"label": "Credibility Weight", "format": percent_format(0)}),
        #SB added 07/05/25
        "cat_event": hx.Str(mode="input", default_index=0, options=["Yes", "No"], view={"label": "CAT Experience in Data"}),
        "experience_data": hx.Str(mode="input", default_index=0, options=["Yes", "No"], view={"label": "Experience Data Available"}),
        "actual_incurred": hx.Str(mode="input", default_index=0, options=["No", "Yes"], view={"label": "Actual Incurred Available"}),
        "exposure_trend": hx.Float(mode="input", async_input=["backfill_exposure"], default=None, optionality="optional", view={"label": "Exposure Trend", "format": percent_format(0)}, validation={"min_value": 0,"max_value": 1}),
    })

