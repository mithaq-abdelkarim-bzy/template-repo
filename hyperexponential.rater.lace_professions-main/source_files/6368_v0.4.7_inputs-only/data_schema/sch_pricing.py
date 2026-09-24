# v0.5.0
import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
from algorithms.rate_constants import get_territory_groups, territory_labels, get_all_layer_names

new_column = "🆕"


def get_territory_dropdown_values():
    return [None] + ["Not Specified"] + list(territory_labels.values())


def er_summary_fields():
    return {
        "aoc_limit": hx.Float(mode="output", view={"label": "AOC Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "agg_limit": hx.Float(mode="output", view={"label": "Agg Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "aoc_attachment": hx.Float(mode="output", view={"label": "AOC Attachment\nExcluding Retentions", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "agg_attachment": hx.Float(mode="output", view={"label": "Agg Attachment\nExcluding Retentions", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "gross_benchmark_premium": hx.Float(mode="output", view={"label": "Gross Benchmark\nExperience Rated Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "ilf_gross_benchmark_premium": hx.Float(mode="output", view={"label": "ILF Implied\nGross Benchmark Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "aoc_limit_oc": hx.Float(mode="output", view={"label": "AOC Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "agg_limit_oc": hx.Float(mode="output", view={"label": "Agg Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "aoc_attachment_oc": hx.Float(mode="output", view={"label": "AOC Attachment\nExcluding Retentions", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "agg_attachment_oc": hx.Float(mode="output", view={"label": "Agg Attachment\nExcluding Retentions", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "gross_benchmark_premium_oc": hx.Float(mode="output", view={"label": "Gross Benchmark\nExperience Rated Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "ilf_gross_benchmark_premium_oc": hx.Float(mode="output", view={"label": "ILF Implied\nGross Benchmark Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
    }


def pricing_layer_fields(include_addl_only_fields=False):
    fields = {
        "limit_eec": hx.Float(mode="input", default=None, async_input=["rarc_task", "run_simulation_task"], optionality="optional", view={"label": "AOC", "format": {"thousandSeparated": True, "mantissa": 0}, "group": "Limit"}),
        "limit_agg": hx.Float(mode="input", default=None, async_input=["rarc_task", "run_simulation_task"], optionality="optional", view={"label": "Aggregate", "format": {"thousandSeparated": True, "mantissa": 0}, "group":"Limit"}),
        "excess_eec": hx.Float(mode="input" if include_addl_only_fields else "output", default=None if include_addl_only_fields else hx.UNDEFINED, async_input=["rarc_task", "run_simulation_task"], optionality="optional" if include_addl_only_fields else hx.UNDEFINED, view={"label": "AOC", "format": {"thousandSeparated": True, "mantissa": 0}, "group":"Excess"}),
        "excess_agg": hx.Float(mode="input" if include_addl_only_fields else "output", default=None if include_addl_only_fields else hx.UNDEFINED, async_input=["rarc_task", "run_simulation_task"], optionality="optional" if include_addl_only_fields else hx.UNDEFINED, view={"label": "Aggregate", "format": {"thousandSeparated": True, "mantissa": 0},"group":"Excess"}),
        "rtc": hx.Float(mode="input", default=None, async_input=["rarc_task", "run_simulation_task"], optionality="optional", view={"label": "RTC Tower", "format": {"thousandSeparated": True, "mantissa": 0},"group":"Round The Clock"}),
        "rtc_agg": hx.Float(mode="input", default=None, async_input=["rarc_task", "run_simulation_task"], optionality="optional", view={"label": "RTC Tower Agg", "format": {"thousandSeparated": True, "mantissa": 0}, "group": "Round The Clock"}),
        "defense_cost": hx.Str(mode="input", default="No", async_input=["rarc_task", "run_simulation_task"], optionality="required", options=["Yes", "No"], view={"label": "Defense Costs\nin Addition"}),
        "wordings_adj": hx.Float(mode="input", default=None, async_input=["rarc_task", "run_simulation_task"], optionality="optional", view={"label": "Wordings","format": {"output": "percent", "mantissa": 1}, "group":"Adjustments"}),
        "uw_adj": hx.Float(mode="input", default=0, async_input=["rarc_task", "run_simulation_task"], optionality="optional", view={"label": "UW", "format": {"output": "percent", "mantissa": 1}, "group":"Adjustments"}),
        "name": hx.Str(mode="output",  async_input=["rarc_task", "run_simulation_task"], view={"label": "UW Adjustment", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "include": hx.Bool(mode="input", async_input=["rarc_task", "run_simulation_task"], optionality="required", default=True, view={"label": "Include?"}),
        "sim_output_uw_adj": hx.Structure(children={
            "exposure_premium": hx.Float(mode="output", async_output=["run_simulation_task"], view={"label": "Exposure Premium\nper $m revenue/fees", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "average_freq": hx.Float(mode="output", async_output=["run_simulation_task"], view={"label": "Av.Frequency\nper $m revenues/fees",  "format": {"output": "percent", "mantissa": 1}}),
            "average_defense_cost_freq": hx.Float(mode="output", async_output=["run_simulation_task"], view={"label": "Av Defense Cost Freq\nper $m revenue/fees",  "format": {"output": "percent", "mantissa": 1}}),
            "layer_exhaust_prob": hx.Float(mode="output", async_output=["run_simulation_task"], view={"label": "Exhaustion\nProbability",  "format": {"output": "percent", "mantissa": 1}}),
        }),
        "sim_output_no_uw_adj": hx.Structure(children={
            "exposure_premium": hx.Float(mode="output", async_output=["run_simulation_task"], view={"label": "Exposure Premium\nper $m revenue/fees", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "average_freq": hx.Float(mode="output", async_output=["run_simulation_task"], view={"label": "Av.Frequency\nper $m revenues/fees",  "format": {"output": "percent", "mantissa": 1}}),
            "average_defense_cost_freq": hx.Float(mode="output", async_output=["run_simulation_task"], view={"label": "Av Defense Cost Freq\nper $m revenue/fees",  "format": {"output": "percent", "mantissa": 1}}),
            "layer_exhaust_prob": hx.Float(mode="output", async_output=["run_simulation_task"], view={"label": "Exhaustion\nProbability",  "format": {"output": "percent", "mantissa": 1}}),
        }),
        "exposure_rate": hx.Float(mode="output", async_output=["run_simulation_task"], view={"label": "Exposure\nRate",  "format": {"thousandSeparated": True, "mantissa": 0},"group":"Model Net Rate per mil Fees"}),
        "exposure_rate_incl_adj": hx.Float(mode="output", view={"label": "Exposure Rate\n(Incl Adj)",  "format": {"thousandSeparated": True, "mantissa": 0},"group":"Model Net Rate per mil Fees"}),
        "experience_rate": hx.Float(mode="output", view={"label": "Experience\nRate",  "format": {"thousandSeparated": True, "mantissa": 0},"group":"Model Net Rate per mil Fees"}),
        "experience_rate_incl_adj": hx.Float(mode="output", view={"label": new_column+"Experience Rate\n(Incl Adj)", "format": {"thousandSeparated": True, "mantissa": 0}, "group":"Model Net Rate per mil Fees"}),
        "experience_rate_20yr_avg": hx.Float(mode="output", view={"label": "Experience Rate 20yr AVg",  "format": {"output": "percent", "mantissa": 1}}),
        "experience_rate_15yr_avg": hx.Float(mode="output", view={"label": "Experience Rate 15yr AVg",  "format": {"output": "percent", "mantissa": 1}}),
        "experience_rate_10yr_avg": hx.Float(mode="output", view={"label": "Experience Rate 10yr AVg",  "format": {"output": "percent", "mantissa": 1}}),
        "experience_weighting": hx.Float(mode="output", view={"label": "Experience\nWeighting",  "format": {"output": "percent", "mantissa": 1}}),
        "experience_weighting_2": hx.Float(mode="override", view={"label": new_column+"Experience\nWeighting", "format": {"output": "percent", "mantissa": 1}}),
        "blended_model_net_rate_pre": hx.Float(mode="output", view={"label": "Blended Model\nNet Rate",  "format": {"thousandSeparated": True, "mantissa": 0}, "group": new_column+"Pre Adjustments"}),
        "expected_loss_cost_net_pre": hx.Float(mode="output", view={"label": "Expected\nNet Loss Cost",  "format": {"thousandSeparated": True, "mantissa": 0}, "group": new_column+"Pre Adjustments"}),
        "blended_model_net_rate": hx.Float(mode="output", view={"label": "Blended Model\nNet Rate",  "format": {"thousandSeparated": True, "mantissa": 0}, "group": new_column+"Post Adjustments"}),
        "expected_loss_cost_net": hx.Float(mode="output", view={"label": "Expected\nNet Loss Cost",  "format": {"thousandSeparated": True, "mantissa": 0}, "group": new_column+"Post Adjustments"}),
        "uw_experience_weighting": hx.Float(mode="output", view={"label": "Experience\nWeighting",  "format": {"output": "percent", "mantissa": 1}, "group":"UW View"}),
        "blended_uw_net_rate": hx.Float(mode="output", view={"label": "Blended Net Rate\nper mil Revenue",  "format": {"thousandSeparated": True, "mantissa": 0}, "group":"UW View"}),
        "benchmark_premium_uw_view": hx.Float(mode="output", view={"label": "Benchmark\nPremium",  "format": {"thousandSeparated": True, "mantissa": 0}, "group":"UW View"}),
        "technical_premium_100_incl_adj": hx.Float(mode="output", async_input=["rarc_task"], optionality="optional", view={"label": "Technical Premium\nIncl UW Adj", "format": {"thousandSeparated": True, "mantissa": 0},"group":"100% Gross Share"}),
        "benchmark_premium_100_incl_adj": hx.Float(mode="output", async_input=["rarc_task"], optionality="optional", view={"label": "Benchmark Premium\nIncl UW Adj", "format": {"thousandSeparated": True, "mantissa": 0},"group":"100% Gross Share"}),
        "benchmark_premium_experience_100": hx.Float(mode="output", async_input=["rarc_task"], optionality="optional", view={"label": "Benchmark\nPremium (Experience)", "format": {"thousandSeparated": True, "mantissa": 0},"group":"100% Gross Share"}),
        "benchmark_premium_exposure_100": hx.Float(mode="output", async_input=["rarc_task"], optionality="optional", view={"label": "Benchmark\nPremium (Exposure)", "format": {"thousandSeparated": True, "mantissa": 0},"group":"100% Gross Share"}),
        "bound_premium_100": hx.Float(mode="input", async_input=["rarc_task"], optionality="optional", default=None, view={"label": "Bound\nPremium", "format": {"thousandSeparated": True, "mantissa": 0},"group":"100% Gross Share"}),
        "gross_rate_per_mill": hx.Float(mode="output", view={"label": "Gross Rate\nper mil Revenue",  "format": {"output": "percent", "mantissa": 1},"group":"100% Gross Share"}),
        "bpi_quoted_100": hx.Float(mode="output", optionality="optional",  view={"label": "Quoted BPI", "format": {"output": "percent", "mantissa": 1},"group":new_column+"100% Gross Share - Excluding UW Adjustments"}),
        "bpi_bound_100": hx.Float(mode="output", optionality="optional",  view={"label": "Bound BPI", "format": {"output": "percent", "mantissa": 1},"group":new_column+"100% Gross Share - Excluding UW Adjustments"}),
        "tpi_quoted_100": hx.Float(mode="output", optionality="optional",  view={"label": "Quoted TPI", "format": {"output": "percent", "mantissa": 1},"group":new_column+"100% Gross Share - Excluding UW Adjustments"}),
        "tpi_bound_100": hx.Float(mode="output", optionality="optional",  view={"label": "Bound TPI", "format": {"output": "percent", "mantissa": 1},"group":new_column+"100% Gross Share - Excluding UW Adjustments"}),
        "bpi_quoted_100_incl_adj": hx.Float(mode="output", optionality="optional",  view={"label": "Quoted BPI", "format": {"output": "percent", "mantissa": 1},"group":new_column+"100% Gross Share - Including UW Adjustments"}),
        "bpi_bound_100_incl_adj": hx.Float(mode="output", optionality="optional",  view={"label": "Bound BPI", "format": {"output": "percent", "mantissa": 1},"group":new_column+"100% Gross Share - Including UW Adjustments"}),
        "tpi_quoted_100_incl_adj": hx.Float(mode="output", optionality="optional",  view={"label": "Quoted TPI", "format": {"output": "percent", "mantissa": 1},"group":new_column+"100% Gross Share - Including UW Adjustments"}),
        "tpi_bound_100_incl_adj": hx.Float(mode="output", optionality="optional",  view={"label": "Bound TPI", "format": {"output": "percent", "mantissa": 1},"group":new_column+"100% Gross Share - Including UW Adjustments"}),
        "bound_premium_share": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Bound Premium", "format": {"thousandSeparated": True, "mantissa": 0}, "group":"Beazley Share"}),
        "gross_premium_uw_view": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "UW View\nGross Premium", "format": {"thousandSeparated": True, "mantissa": 0}, "group":"Elevated Risk Year View (For Reference Only)"}),
        "technical_premium_ryv": hx.Float(mode="output", async_input=["rarc_task"], optionality="optional", view={"label": "Technical Premium\n(incl. UW Adj)", "format": {"thousandSeparated": True, "mantissa": 0},"group":"Elevated Risk Year View (For Reference Only)"}),
        "benchmark_premium_ryv": hx.Float(mode="output", async_input=["rarc_task"], optionality="optional", view={"label": "Benchmark Premium\n(incl. UW Adj)", "format": {"thousandSeparated": True, "mantissa": 0},"group":"Elevated Risk Year View (For Reference Only)"}),
        "bpi_quoted_ryv": hx.Float(mode="output", optionality="optional", view={"label": "Quoted BPI", "format": {"output": "percent", "mantissa": 1}, "group": "Elevated Risk Year View (For Reference Only)"}),
        "bpi_bound_ryv": hx.Float(mode="output", optionality="optional", view={"label": "Bound BPI", "format": {"output": "percent", "mantissa": 1}, "group": "Elevated Risk Year View (For Reference Only)"}),
        "tpi_quoted_ryv": hx.Float(mode="output", optionality="optional", view={"label": "Quoted TPI", "format": {"output": "percent", "mantissa": 1}, "group": "Elevated Risk Year View (For Reference Only)"}),
        "tpi_bound_ryv": hx.Float(mode="output", optionality="optional", view={"label": "Bound TPI", "format": {"output": "percent", "mantissa": 1}, "group": "Elevated Risk Year View (For Reference Only)"}),
        "experience_rating_summary": hx.Structure(children=er_summary_fields()),
        "unadjusted_exposure_rate": hx.Float(mode="output", view={"label": "Unadjusted Exposure Rate", "format": {"thousandSeparated": True, "mantissa": 2}, "group":"No UW Adjustment"}),
        "unadjusted_blended_model_net_rate": hx.Float(mode="output", view={"label": "Unadjusted Blended Model Net Rate", "format": {"output": "percent", "mantissa": 1}, "group":"No UW Adjustment"}),
        "unadjusted_technical_premium": hx.Float(mode="output", view={"label": "Unadjusted Technical Premium", "format": {"thousandSeparated": True, "mantissa": 2}, "group":"No UW Adjustment"}),
        "unadjusted_bound_tpi": hx.Float(mode="output", view={"label": "Unadjusted Bound TPI", "format": {"output": "percent", "mantissa": 1}, "group":"No UW Adjustment"}),
    }
    if include_addl_only_fields:
        fields.update({
            "technical_premium_100": hx.Float(mode="output", async_input=["rarc_task"], optionality="optional", view={"label": new_column+"Technical Premium\nExcl UW Adj", "format": {"thousandSeparated": True, "mantissa": 0},"group":"100% Gross Share"}),
            "benchmark_premium_100": hx.Float(mode="output", async_input=["rarc_task"], optionality="optional", view={"label": new_column+"Benchmark Premium\nExcl UW Adj", "format": {"thousandSeparated": True, "mantissa": 0},"group":"100% Gross Share"}),
            "quoted_premium_100": hx.Float(mode="input", default=0, async_input=["rarc_task"], optionality="required", view={"label": "Quoted\nPremium", "format": {"thousandSeparated": True, "mantissa": 0}, "options": {"read_only": {"read_only": True}},"group":"100% Gross Share"}),
            "brokerage": hx.Float(mode="input", async_input=["rarc_task", "run_simulation_task"], validation={"min_value":0.0, "max_value":0.9999}, optionality="optional", default=0, view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}, "options": {"read_only": {"read_only": True}}}),
            "status": hx.Str(mode="input", default=None, async_input=["rarc_task"], optionality="optional", options=["Assessment Pending", "Rating", "Quoted", "Bound", "Post Bind Complete", "Declined", "Not Taken Up"], view={"label": "Status", "options": {"read_only": {"read_only": True}}}),
            "section_reference": hx.Str(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Section Reference", "options": {"read_only": {"read_only": True}}}),
            "written_line": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Written Line", "format": {"output": "percent", "mantissa": 1}, "options": {"read_only": {"read_only": True}},"group":"Beazley Share"}),
            "premium_label": hx.Str(mode="output"),
            "tpi": hx.Float(mode="output", optionality="optional", view={"label": "TPI", "format": {"output": "percent", "mantissa": 1}}),
            "bpi": hx.Float(mode="output", optionality="optional", view={"label": "BPI", "format": {"output": "percent", "mantissa": 1}}),
            "tpi_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "TPI (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
            "bpi_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "BPI (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
            "pflr": hx.Float(mode="output", optionality="optional", view={"label": "Priced-for Loss Ratio", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "pflr_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "Priced-for Loss Ratio (Pre-UW Adj.)", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "uw_adj_impact": hx.Float(mode="output", optionality="optional", view={"label": "Impact of Underwriting Adjustments", "format": {"output": "percent", "mantissa": 1}}),
            "rate_change": hx.Structure(children={
                "risk_adjusted_rate_change": hx.Float(mode="output", optionality="optional", view={"label": "Risk Adjusted Rate Change", "format": {"output": "percent", "mantissa": 1}}),
                "risk_adjusted_rate_change_case_priced": hx.Float(mode="output", optionality="optional", view={"label": "Risk Adjusted Rate Change", "format": {"output": "percent", "mantissa": 1}}),
            }),
        })
    return fields


def sch_pricing(cds):
    cds.extend_node_rater_defined("cds", {
        "rating_factors": hx.Structure(children={
            "policy_term": hx.Float(mode="output"),
            "elevated_risk_year_load": hx.Float(mode="input", optionality="required", default=0.0, view={"label":"Elevated Risk Year Load", "format": {"output": "percent", "mantissa": 1}}),
            "cat_load": hx.Float(mode="output", view={"label": "Cat Load", "format": {"output": "percent", "mantissa": 1}}),
        }),
        "retention_split": hx.List(mode="input", default_element_count=5, children={
            "region": hx.Str(mode="input", async_input=["run_simulation_task","rarc_task"], optionality="optional", options=get_territory_dropdown_values(), default_index=0, view={"label":"Region"}),
            "ccy": hx.Str(mode="input", async_input=["run_simulation_task","rarc_task"], optionality="optional", options_table="table_input_currency", default_index=0, options_column="ccy", view={"label":"Currency"}),
            "eec": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], optionality="optional", default=None, view={"label":"EEC", "format": {"thousandSeparated": True, "mantissa": 0},"group":"Retention"}),
            "aggregate": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], optionality="optional", default=None, view={"label":"Aggregate","format": {"thousandSeparated": True, "mantissa": 0},"group":"Retention"}),
            "retention_underlying": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], optionality="optional", default=None, view={"label":"Underlying","format": {"thousandSeparated": True, "mantissa": 0}, "group": "Additional Retention"}),
            "retention_residual": hx.Float(mode="input", async_input=["run_simulation_task","rarc_task"], optionality="optional", default=None, view={"label":"Residual", "format": {"thousandSeparated": True, "mantissa": 0},"group": "Additional Retention"}),
            "defence_cost_bool": hx.Str(mode="input", default="No", async_input=["rarc_task", "run_simulation_task"], optionality="required", options=["Yes", "No"], view={"label": "Also applies to \ndefence costs?"}),
        }),
        "retention_split_notes": hx.Str(mode="output"),
        "sp_underwriter_comments": hx.Str(mode="output"),
        "hover_info": hx.Structure(children={
            "num_att_full": hx.Str(mode="output"),
            "num_att_fte": hx.Str(mode="output"),
            "retention_underlying": hx.Str(mode="output"),
            "retention_residual": hx.Str(mode="output"),
            "rtc": hx.Str(mode="output"),
            "wordings_adj": hx.Str(mode="output"),
            "uw_adj": hx.Str(mode="output"),
            "blended_model_net_rate": hx.Str(mode="output"),
            "expected_loss_cost_net": hx.Str(mode="output"),
            "uw_experience_weighting": hx.Str(mode="output"),
            "blended_uw_net_rate": hx.Str(mode="output"),
            "benchmark_premium_uw_view": hx.Str(mode="output"),
            "gross_rate_per_mill": hx.Str(mode="output"),
            "elevated_risk_year_load": hx.Str(mode="output"),
            "gross_benchmark_premium": hx.Str(mode="output"),
            "ilf_gross_benchmark_premium": hx.Str(mode="output"),
            "value_of_claims_data": hx.Str(mode="output"),
            "per_year_claims_data": hx.Str(mode="output"),
            "total_usd_inflated": hx.Str(mode="output"),
            "territory_policy_year": hx.Str(mode="output"),
            "inception_date": hx.Str(mode="output"),
            "latest_policy_year": hx.Str(mode="output"),
            "calculated_policy_year": hx.Str(mode="output"),
            "cat_load": hx.Str(mode="output"),
        }),
        "retention_split_uw_comments": hx.Str(mode="input", optionality="optional", default=None),
        "retention_split_uw_comments_plaintext": hx.Str(mode="output"),
        "technical_premium_buildup_layer": hx.Str(mode="input", optionality="optional", options=get_all_layer_names(), default_index=0, view={"label": "Select Layer to Display"}),
        "run_simulation_notes": hx.Str(mode="output", view={"label":"Message"}),
        "run_simulation_notes_bool": hx.Bool(mode="output"),
        "policy_notes": hx.Str(mode="output"),
        "ave_chart": hx.Structure(children={"data": hx.Structure(children={
            "label_exposure": hx.Str(mode="output", view={"label": "Simulated Loss"}),
            "label_experience": hx.Str(mode="output", view={"label": "Actual Loss"}),
            "points_exposure": hx.List(mode="input", default_element_count=35, children={
                "percentile": hx.Float(mode="output", view={"label": "Percentile", "format": {"output": "percent", "mantissa": 1}}),
                "loss": hx.Float(mode="output", view={"format": thousands_format(1), "chart": {"series_type": "pointline"}}),
            }),
            "points_experience": hx.List(mode="input", default_element_count=35, children={
                "percentile": hx.Float(mode="output", view={"label": "Percentile", "format": {"output": "percent", "mantissa": 1}}),
                "loss": hx.Float(mode="output", view={"format": thousands_format(1), "chart": {"series_type": "pointline"}}),
            }),
        })}),
        "pbu_chart": hx.Structure(children={"data": hx.Structure(children={
            "technical_premium": hx.Structure(children={"brokerage": hx.Float(mode="output"), "profit_load": hx.Float(mode="output"), "expenses": hx.Float(mode="output"), "ri_cost": hx.Float(mode="output"), "elc": hx.Float(mode="output")}),
            "benchmark_premium": hx.Structure(children={"brokerage": hx.Float(mode="output"), "profit_load": hx.Float(mode="output"), "expenses": hx.Float(mode="output"), "ri_cost": hx.Float(mode="output"), "elc": hx.Float(mode="output")}),
            "bound_premium": hx.Structure(children={"brokerage": hx.Float(mode="output"), "profit_load": hx.Float(mode="output"), "expenses": hx.Float(mode="output"), "ri_cost": hx.Float(mode="output"), "elc": hx.Float(mode="output")}),
        })}),
    })

    cds.extend_node_rater_defined("cds/layers", pricing_layer_fields())
    cds.extend_node_rater_defined("cds", {
        "layers_addl": hx.List(mode="input", async_input=["rarc_task"], default_element_count=3, max_element_count=5, children=pricing_layer_fields(include_addl_only_fields=True))
    })

    cds.override_node_properties("cds/layers/technical_premium_100", {"view":{"label": new_column+"Technical Premium\nExcl UW Adj", "group":"100% Gross Share"}})
    cds.override_node_properties("cds/layers/benchmark_premium_100", {"view":{"label": new_column+"Benchmark Premium\nExcl UW Adj", "group":"100% Gross Share"}})
