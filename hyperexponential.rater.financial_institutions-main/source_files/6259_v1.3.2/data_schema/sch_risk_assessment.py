import hx_data_schema as hxd

from algorithms.rate_utilities import get_field_options
from libraries.common_data_schema.data_schema.utilities import percent_format


def sch_risk_assessment(cds):
    cds.extend_node_rater_defined("cds", {
        "modifiers": hxd.Structure(children={
            "risk_category": hxd.Structure(view={"label": "Risk category"}, children={
                "policy_wording": hxd.Str(mode="input", default=None, optionality="optional", options=get_field_options("risk_assessment", "policy_wording"), async_input=["rarc_task"], view={"label": "Policy wording"}),
                "claims_history_cpi": hxd.Str(mode="input", default=None, optionality="optional", options=get_field_options("risk_assessment", "claims_history_cpi"), async_input=["rarc_task"], view={"label": "Claims History - Crime & PI"}),
                "claims_history_do": hxd.Str(mode="input", default=None, optionality="optional", options=get_field_options("risk_assessment", "claims_history_do"), async_input=["rarc_task"], view={"label": "Claims History - D&O"}),
                "risk_management": hxd.Str(mode="input", default=None, optionality="optional", options=get_field_options("risk_assessment", "risk_management"), async_input=["rarc_task"], view={"label": "Quality of risk management"}),
                "strength_of_financial": hxd.Str(mode="input", default=None, optionality="optional", options=get_field_options("risk_assessment", "strength_of_financial"), async_input=["rarc_task"], view={"label": "Strength of financials"}),
                "technological_infrastructure": hxd.Str(mode="input", default=None, optionality="optional", options=get_field_options("risk_assessment", "technological_infrastructure"), async_input=["rarc_task"], view={"label": "Quality of technological infrastructure"}),
                "quality_of_control": hxd.Str(mode="input", default=None, optionality="optional", options=get_field_options("risk_assessment", "quality_of_control"), async_input=["rarc_task"], view={"label": "Quality of physical controls"}),
                "agents_as_employees": hxd.Bool(mode="input", default=False, async_input=["rarc_task"], view={"label": "Are agents included as employees?"}),
                "regulatory_risk": hxd.Str(mode="input", default=None, optionality="optional", options=get_field_options("risk_assessment", "regulatory_risk"), async_input=["rarc_task"], view={"label": "Regulatory risk"}),
                "quality_of_claims_handling": hxd.Str(mode="input", default=None, optionality="optional", options=get_field_options("risk_assessment", "quality_of_claims_handling"), async_input=["rarc_task"], view={"label": "Quality of claims handling"}),
                "product_complexity": hxd.Str(mode="input", default=None, optionality="optional", options=get_field_options("risk_assessment", "product_complexity"), async_input=["rarc_task"], view={"label": "Complexity of insured's products/services"}),
                "quality_of_bcp": hxd.Str(mode="input",default=None, optionality="optional",  options=get_field_options("risk_assessment", "quality_of_bcp"), async_input=["rarc_task"], view={"label": "Quality of business continuity plans"}),
                "market_regulator": hxd.Bool(mode="input", default=False, async_input=["rarc_task"], view={"label": "Is the insured a regulatory body?"}),
                "extent_of_leveraged_gearing": hxd.Str(mode="input", default=None, optionality="optional", options=get_field_options("risk_assessment", "extent_of_leveraged_gearing"), async_input=["rarc_task"], view={"label": "Extent of leverage/gearing"}),
                "quality_of_performance_non_pevc": hxd.Str(mode="input", default=None, optionality="optional", options=get_field_options("risk_assessment", "quality_of_performance_non_pevc"), async_input=["rarc_task"], view={"label": "Investment performance"}),
                "redemption_gates": hxd.Str(mode="input", default=None, optionality="optional", options=get_field_options("risk_assessment", "redemption_gates"), async_input=["rarc_task"], view={"label": "Net inflow/outflows"}),
                "valuation_for_pevc": hxd.Bool(mode="input", default=True, async_input=["rarc_task"], view={"label": "Satisfactory external annual valuation/validation?"}),
                "loan_covenant": hxd.Bool(mode="input", default=False, async_input=["rarc_task"], view={"label": "Loan covenant breach?"}),
                "dando_portfolio_companies": hxd.Bool(mode="input", default=False, async_input=["rarc_task"], view={"label": "D&O cover purchased for portfolio companies?"}),
                "data_centre": hxd.Bool(mode="input", default=True, async_input=["rarc_task"], view={"label": "Data centre strategy?"}),
                "tech_outsourcing": hxd.Bool(mode="input", default=True, async_input=["rarc_task"], view={"label": "Technology Outsourcing?"}),
                "difference_in_conditions": hxd.Str(mode="input", default=None, optionality="optional", options=get_field_options("risk_assessment", "difference_in_conditions"), async_input=["rarc_task"], view={"label": "Difference in Conditions only (A-side DIC only)"}),
                "uw_adj": hxd.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"options":{"input":{"label": "Underwriting adjustment (-30% max credit)", "format": percent_format()},
                                                                                                                                    "read_only": {"label": "Impact of Underwriting Adjustments", "format": percent_format(), "read_only": True}}})}),
            "comment": hxd.Structure(view={"label": "Comment"}, children={
                "policy_wording": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Policy wording"}),
                "claims_history_cpi": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Claims History - Crime & PI"}),
                "claims_history_do": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Claims History - D&O"}),
                "risk_management": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Quality of risk management"}),
                "strength_of_financial": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Strength of financials"}),
                "technological_infrastructure": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Quality of technological infrastructure"}),
                "quality_of_control": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Quality of physical controls"}),
                "agents_as_employees": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Are agents included as employees?"}),
                "regulatory_risk": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Regulatory risk"}),
                "quality_of_claims_handling": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Quality of claims handling"}),
                "product_complexity": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Complexity of insured's products/services"}),
                "quality_of_bcp": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Quality of business continuity plans"}),
                "market_regulator": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Is the insured a regulatory body?"}),
                "extent_of_leveraged_gearing": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Extent of leverage/gearing"}),
                "quality_of_performance_non_pevc": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Investment performance"}),
                "redemption_gates": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Net inflow/outflows"}),
                "valuation_for_pevc": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Satisfactory external annual valuation/validation?"}),
                "loan_covenant": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Loan covenant breach?"}),
                "dando_portfolio_companies": hxd.Str(mode="input", default="", optionality="optional", view={"label": "D&O cover purchased for portfolio companies?"}),
                "data_centre": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Data centre strategy?"}),
                "tech_outsourcing": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Technology Outsourcing?"}),
                "difference_in_conditions": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Difference in Conditions only (A-side DIC only)"}),
                "uw_adj": hxd.Str(mode="input", default="", optionality="optional", view={"options":{"input":{"label": "Underwriting adjustment (-30% max credit)"},
                                                                                                                "read_only": {"label": "Underwriting adjustment (-30% max credit)", "read_only": True}}})
            })
        })
    })


def sch_risk_assessment_non_cds():
    return {
        "risk_assesment": hxd.Structure(children={
            "any_any": hxd.Bool(mode="output"),
            "any_crime": hxd.Bool(mode="output"),
            "any_pi": hxd.Bool(mode="output"),
            "any_do": hxd.Bool(mode="output"),
            "any_crime_pi": hxd.Bool(mode="output"),
            "any_pi_do": hxd.Bool(mode="output"),
            "fin_any": hxd.Bool(mode="output"),
            "notins_crime_pi": hxd.Bool(mode="output"),  # Industry != Insurance and Coverage == Crime or PI
            "ins_pi": hxd.Bool(mode="output"),
            "fin_pi": hxd.Bool(mode="output"),
            "ban_fin_pi": hxd.Bool(mode="output"),
            "inv_pi": hxd.Bool(mode="output"),
            "inv_PE_VC_RE_pi": hxd.Bool(mode="output"),  # Industry == Investment and Sub Industry any(Private Eq, Venture Cap, Real Est) and Coverage == PI
            "inv_PE_VC_do": hxd.Bool(mode="output"),
        })
    }
