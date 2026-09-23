import hx_data_schema as hx
import data_schema.sch_utilities as utils

def sch_risk_assessment(cds):
    cds.extend_node_rater_defined("cds", {
        "modifiers": hx.Structure(view ={"label": "Rating Factors"}, children = {
            "message": hx.Str(mode="output", optionality="optional", view={"label": "Message"}),
            "sca_freq_adj_factor": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "SCA Frequency Adjustment Factor", "format":utils.percent_format(1)}), 
            "sca_freq_adj_factor_info": hx.Str(mode="output", optionality="optional", view={"label": "SCA Frequency Adjustment Factor Info"}),
            "sca_freq_adj_factor_comment": hx.Str(mode="input", default=None,optionality="optional", view={"label": "Comment for SCA Frequency Adjustment Factor"}),             
            "management_corp_gov_factors": hx.Structure(view={"label": "Management and Corporate Governance"}, children={
                "value": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %", "format":utils.percent_format(0)}),
                "max": hx.Float(mode="output", view={"label": "Max %", "format":utils.percent_format(0)}),
            }),
            "business_financial_model_factors": hx.Structure(view={"label": "Business / Financial Model Factors"}, children={
                "value": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %", "format":utils.percent_format(0)}),
                "max": hx.Float(mode="output", view={"label": "Max %", "format":utils.percent_format(0)}),
            }),
            "significant_event_factors": hx.Structure(view={"label": "Significant Event Factors"}, children={
                "value": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %", "format":utils.percent_format(0)}),
                "max": hx.Float(mode="output", view={"label": "Max %", "format":utils.percent_format(0)}),
            }),
            "stock_market_factors": hx.Structure(view={"label": "Stock Market Factors"}, children={
                "value": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %", "format":utils.percent_format(0)}),
                "max": hx.Float(mode="output", view={"label": "Max %", "format":utils.percent_format(0)}),
            }),
            "sca_adj_factors": hx.Structure(view={"label": "Overall SCA Adjustment Factor"}, children={
                "value": hx.Float(mode="output", optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="output", optionality="optional", view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %"}),
                "max": hx.Float(mode="output", view={"label": "Max %"}),
            }),                                             
            "regulatory_factors": hx.Structure(view={"label": "Regulatory"}, children={
                "value": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %", "format":utils.percent_format(0)}),
                "max": hx.Float(mode="output", view={"label": "Max %", "format":utils.percent_format(0)}),
            }),
            "mergers_and_acquisitions_factors": hx.Structure(view={"label": "Mergers and Acquisitions"}, children={
                "value": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %", "format":utils.percent_format(0)}),
                "max": hx.Float(mode="output", view={"label": "Max %", "format":utils.percent_format(0)}),
            }),
            "territory_of_operation_factors": hx.Structure(view={"label": "Territory of Operation"}, children={
                "value": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %", "format":utils.percent_format(0)}),
                "max": hx.Float(mode="output", view={"label": "Max %", "format":utils.percent_format(0)}),
            }),
            "esg_factors": hx.Structure(view={"label": "ESG Factor"}, children={
                "value": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %", "format":utils.percent_format(0)}),
                "max": hx.Float(mode="output", view={"label": "Max %", "format":utils.percent_format(0)}),
            }),
            "total_factors": hx.Structure(view={"label": "Total Factor"}, children={
                "value": hx.Float(mode="output", optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="output", optionality="optional",view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %"}),
                "max": hx.Float(mode="output", view={"label": "Max %"}),
            }),
            
            "management_corp_gov_factors_side_a": hx.Structure(view={"label": "Management and Corporate Governance"}, children={
                "value": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %", "format":utils.percent_format(0)}),
                "max": hx.Float(mode="output", view={"label": "Max %", "format":utils.percent_format(0)}),
            }),
            "business_financial_model_factors_side_a": hx.Structure(view={"label": "Business / Financial Model Factors"}, children={
                "value": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %", "format":utils.percent_format(0)}),
                "max": hx.Float(mode="output", view={"label": "Max %", "format":utils.percent_format(0)}),
            }),
            "significant_event_factors_side_a": hx.Structure(view={"label": "Significant Event Factors"}, children={
                "value": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %", "format":utils.percent_format(0)}),
                "max": hx.Float(mode="output", view={"label": "Max %", "format":utils.percent_format(0)}),
            }),
            "stock_market_factors_side_a": hx.Structure(view={"label": "Stock Market Factors"}, children={
                "value": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %", "format":utils.percent_format(0)}),
                "max": hx.Float(mode="output", view={"label": "Max %", "format":utils.percent_format(0)}),
            }),
            "sca_adj_factors_side_a": hx.Structure(view={"label": "Overall SCA Adjustment Factor"}, children={
                "value": hx.Float(mode="output", optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="output", optionality="optional",view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %"}),
                "max": hx.Float(mode="output", view={"label": "Max %"}),
            }),          
            
            "financial_stability_side_a_factors": hx.Structure(view={"label": "Financial Stability"}, children={
                "value": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %", "format":utils.percent_format(0)}),
                "max": hx.Float(mode="output", view={"label": "Max %", "format":utils.percent_format(0)}),
            }),
            "indemnification_side_a_factors": hx.Structure(view={"label": "Indemnification"}, children={
                "value": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %", "format":utils.percent_format(0)}),
                "max": hx.Float(mode="output", view={"label": "Max %", "format":utils.percent_format(0)}),
            }),
            "esg_factors_side_a": hx.Structure(view={"label": "ESG Factor"}, children={
                "value": hx.Float(mode="input", default=None, async_input=["rarc_task"], optionality="optional", view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %", "format":utils.percent_format(0)}),
                "max": hx.Float(mode="output", view={"label": "Max %", "format":utils.percent_format(0)}),
            }),
             "total_factors_side_a": hx.Structure(view={"label": "Total Factor"}, children={
                "value": hx.Float(mode="output", optionality="optional", validation={"min_value": -0.5}, view={"label": "Value", "format":utils.percent_format(0)}),
                "comment": hx.Str(mode="output", optionality="optional",view={"label": "Comment"}),
                "min": hx.Float(mode="output", view={"label": "Min %"}),
                "max": hx.Float(mode="output", view={"label": "Max %"}),
            }),

            "suggested_factor": hx.Float(mode="output", optionality="optional", view={"label": "Suggested Factor", "format":utils.percent_format(0)}),
            "suggested_factor_message": hx.Str(mode="output", optionality="optional", view={"label": "Message"}),
            "suggested_factor_message_for_adj": hx.Str(mode="output", optionality="optional", view={"label": "Message for Adjustments"}),

            "total_factor_info": hx.Str(mode="output", view={"label": "Total Factor Info"}),
            "total_factor_side_a_info": hx.Str(mode="output", view={"label": "Total Factor Side A Info"}),
        })
    }
)