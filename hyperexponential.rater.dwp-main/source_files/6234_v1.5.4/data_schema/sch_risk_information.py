import hx_data_schema as hx
# import data_schema.sch_utilities as utils
from data_schema.sch_utilities import thousands_format, percent_format, integer_format


def sch_risk_information(cds):
        
    # Extend root node
    cds.extend_node_rater_defined("cds", {
        
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),

        # Add rating factors bucket
        "rating_factors": hx.Structure(children={
            "bi_and_ee_cover": hx.Bool(mode="input", default=False, view={"label": "BI & EE Cover?"}, async_input=["rarc_task"]),
            "seperate_bi_ee_agg_limits": hx.Bool(mode="input", default=False, view={"label": "Seperate BI and EE Agg Limits?"}, async_input=["rarc_task"]),
            "bi_tiv": hx.Float(mode="input", default=None, optionality="optional", view={"label": "BI Total Insured Value", "format": thousands_format(0)}, async_input=["rarc_task"]),
            "extensions_covered": hx.Float(mode="input", default=0, options=[0, 0.05, 0.1, 0.15, 0.2, 0.25], view={"label": "Extensions Covered?", "format": percent_format(0)}, async_input=["rarc_task"]),
            "liability_covered": hx.Bool(mode="input", default=True, view={"label": "Liability Covered? "}, async_input=["rarc_task"]),
            
            "risk_preparedness": hx.Str(mode="input", default="Average", options_table="preparedness_factor", options_column="Level", view={"label": "Risk Preparedness"}, async_input=["rarc_task"]),
            "security": hx.Str(mode="input", default="Average", options_table="preparedness_factor", options_column="Level", view={"label": "Security"}, async_input=["rarc_task"]),
            "crisis_management": hx.Str(mode="input", default="Average", options_table="preparedness_factor", options_column="Level", view={"label": "Crisis Management"}, async_input=["rarc_task"]),
            "social_media": hx.Bool(mode="input", default=False, view={"label": "Social Media"}, async_input=["rarc_task"]),
            "high_profile_event": hx.Str(mode="input", default_index=0, options_table="preparedness_factor_high_profile_event", options_column="High Profile Event", view={"label": "High Profile Event?"}, async_input=["rarc_task"]),

            "base_inflation": hx.Float(mode="output"),
            "social_inflation": hx.Float(mode="output"),
            
            "policy_term": hx.Float(mode="output"),

            "preparedness_factor_ed": hx.Float(mode="output", async_input=["rarc_task"]),
            "preparedness_factor_non_ed": hx.Float(mode="output", async_input=["rarc_task"]),

        }),

        # Total Expected Loss
        "ground_up_expected_loss": hx.Structure(children={
            "education": hx.Float(mode="output"),
            "non_education": hx.Float(mode="output"),
            "education_annualised": hx.Float(mode="output", async_input=["rarc_task"]),
            "non_education_annualised": hx.Float(mode="output", async_input=["rarc_task"]),
        }),

        # underwriter modifiers
        "modifiers": hx.Structure(children={
            "underwriter_adjustment": hx.Float(
                mode="input", 
                default=None,
                optionality="optional",
                validation={"min_value": -0.5, "max_value": 0.5},
                async_input=["rarc_task"],
                view={"label": "Underwriter Adjustment", "format": percent_format(0)}
            )
        }),
    
        # Minimum premiums (the base min premium is based on $1m limit and no deductible)
        "min_premium_base": hx.Structure(children={
            "education": hx.Float(mode="output"),
            "non_education": hx.Float(mode="output"),
        }),

        # Add underwriter comments and rationale
        "uw_rationale": hx.Structure(children={
            "knowledge_of_insured": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Knowledge of the Insured)"}),
            "portfolio_fit": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Portfolio Fit"}),
            "basis_of_risk_selection": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Basis of Risk Selection"}),
            "complex_considerations": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Any Unusual or Complex Considerations"}),
            "facts_affecting_decision": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Any facts which affect Underwriter's decision?"}),
            "comments": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Underwriter Comments"}),
            "extensions_comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Extensions Comment"}),
            "is_rationale_required": hx.Bool(mode="output"),
        }),

    })
       
        
    # Extend layers rater defined
    cds.extend_node_rater_defined("cds/layers", {
        
        # Policy Level Info 
        "type": hx.Str(mode="input", default="Deductible", options=["Deductible", "Excess"], view={"label": "Type"}, async_input=["rarc_task"]),
        "agg_limits_list": hx.List(mode="output", children={
            "values": hx.Float(mode="output"),
        }),

        # Min premiums vary by layer 
        "min_premium": hx.Structure(children={
            "education": hx.Float(mode="output"),
            "non_education": hx.Float(mode="output"),
            "flag": hx.Bool(mode="output"),
        }),

        # Total expected loss costs
        "expected_loss": hx.Structure(children={
            "education": hx.Float(mode="output", view={"label": "Education Loss Cost", "format": thousands_format(0)}),
            "non_education": hx.Float(mode="output", view={"label": "Non-Education Loss Cost", "format": thousands_format(0)}),
            "exposure_rated": hx.Float(mode="output", view={"label": "Exposure Rated", "format": thousands_format(0)}),
            "experience_rated": hx.Float(mode="output", view={"label": "Experience Rated", "format": thousands_format(0)}),
            "experience_weight": hx.Float(mode="output", view={"label": "Experience Weight", "format": percent_format(0)}),
            "blended": hx.Float(mode="output", view={"label": "Blended Expected Loss", "format": thousands_format(0)}),
        }),
        
        # Rating Summary
        "filter": hx.Bool(mode="output"), # To filter first col in alt scenarios
        "label": hx.Str(mode="output"),
        "bpi_case_priced": hx.Float(mode="input", default=None, optionality="optional", view={"label": "BPI (Case Priced)", "format": percent_format(1)}),       
        
        "suggested_epi": hx.Float(mode="output", view={"label": "Suggested EPI", "format": thousands_format(0)}),
        "alt_limit": hx.Float(mode="override", view={"label": "Alt Limit", "format": thousands_format(0)}),
        "alt_agg_limit": hx.Float(mode="override", view={"label": "Alt Agg Limit", "format": thousands_format(0)}),

        
        # Add premium metrics 
        "benchmark_premium_annualised": hx.Float(mode="output", view={"label": "Annualised Benchmark Premium (100%)", "format": thousands_format(0)}, async_input=["rarc_task"]),
        "quoted_premium_annualised": hx.Float(mode="output", view={"label": "Annualised Quoted Premium (100%)", "format": thousands_format(0)}, async_input=["rarc_task"]),
        "benchmark_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Benchmark Premium Before UW Adj", "format": thousands_format(0)}),
    })


    


    
    
   
   
    

