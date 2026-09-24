# v0.5.0
import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
from algorithms.rate_constants import max_layers

def sch_experience_rating(cds):

    cds.extend_node_rater_defined("cds/experience_rating", {
        # experience instructions
        "experience_instructions": hx.Str(mode="output", view={"label": "Notes for Experience Rating"}),
        # claims instructions
        "claims_instructions": hx.Str(mode="output", view={"label": "Note for Claims Data"}),
        "claims_asatdate": hx.Date(mode="input", default=None, optionality="optional", view={"label": "As At Date"}),
        "claims_policy_year": hx.Int(mode="input", default=None, optionality="optional", view={"label": "Claims Data Provided From (Policy Year)", "format": {"thousandSeparated": False, "mantissa": 0}}),
        # show/hide flags used to control the view
        "use_experience_rating_basic": hx.Bool(mode="output"),
        "use_experience_rating_agg": hx.Bool(mode="output"),
        "use_experience_rating_full": hx.Bool(mode="output"),
        "show_claims_input_table": hx.Bool(mode="output"),
        **{f"claims_show_layer_{index}": hx.Bool(mode="output") for index in range(1,max_layers+1)},
        **{f"calculation_show_layer_{index}": hx.Bool(mode="output") for index in range(1,max_layers+1)},
        # show/hide field for additional detail on the weighting calculation
        "show_weights": hx.Bool(mode="input", default=False, view={"label": "Show Weight Breakdown Details"}),
        # show/hide field for additional calculated fields in the full experience rating
        "show_to_layer_fields": hx.Bool(mode="input", default=False, view={"label": "Show To Layer Claims"}),

        # simplest experience rating (basic lookup from clean years)
        "experience_rating_basic": hx.Structure(children={
            "clean_years": hx.Str(mode="input", default="0", options_table="table_basic_experience_rating", options_column="Clean Years",  view={"label": "No. Of Years Since Last Claim"}),
            "experience_adjustment": hx.Float(mode="output", view={"label": "Experience Rating Adjustment", "format": percent_format(0)}),
        })
    })

    cds.override_node_properties("cds/experience_rating/claims", {"default_element_count":50})
    cds.extend_node_rater_defined("cds/experience_rating", {
        "claims_summary": hx.Structure(children={
            **{f"year_{key}": hx.Structure(children={
                "policy_year": hx.Str(mode="output", view={"label": "Policy Year"}),
                "revalued_notional_revenue": hx.Float(mode="output", view={"label":"Revalued Notional\nRevenue",  "format": {"thousandSeparated": True, "mantissa": 0}}),
                "revalued_notional_revenue_weighted": hx.Float(mode="output", view={"label":"Weighted Revalued\nNotional Revenue",  "format": {"thousandSeparated": True, "mantissa": 0}}),
                "pcnt_developed": hx.Float(mode="output", view={"label":"% Developed", "format": {"output": "percent", "mantissa": 1}}),
                "gu_incurred": hx.Float(mode="output", view={"label":"Incurred GU\n(USD)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "gu_inflated": hx.Float(mode="output", view={"label": "Inflated GU\n(USD)",  "format": {"thousandSeparated": True, "mantissa": 0}}),
                "ql_inflated_incurred": hx.Float(mode="output", view={"label":"Inflated Incurred\n(USD)",  "format": {"thousandSeparated": True, "mantissa": 0}}),
                "revalued_notional_revenue_oc": hx.Float(mode="output", view={"label":"Revalued Notional\nRevenue",  "format": {"thousandSeparated": True, "mantissa": 0}}),
                "revalued_notional_revenue_weighted_oc": hx.Float(mode="output", view={"label":"Weighted Revalued\nNotional Revenue",  "format": {"thousandSeparated": True, "mantissa": 0}}),
                "gu_incurred_oc": hx.Float(mode="output", view={"label":"Incurred GU", "format": {"thousandSeparated": True, "mantissa": 0}, "group": "From Ground Up"}),
                "gu_inflated_oc": hx.Float(mode="output", view={"label": "Inflated GU",  "format": {"thousandSeparated": True, "mantissa": 0}, "group": "From Ground Up"}),
                "ql_inflated_incurred_oc": hx.Float(mode="output", view={"label":"Inflated Incurred",  "format": {"thousandSeparated": True, "mantissa": 0}, "group": "Quoted Layer"}),
                "weighting_applied_year": hx.Float(mode="output", view={"label":"Weighting Applied To Each Year", "format": {"output": "percent", "mantissa": 2}}),
            })
            for key in range(20, -1, -1)},
        }
        )
    })

    cds.extend_node_rater_defined("cds/experience_rating", 
        {
            "last_x_year_labels": hx.Structure(children={
                    "last_10_years": hx.Str(mode="output"),
                    "last_15_years": hx.Str(mode="output"),
                    "last_20_years": hx.Str(mode="output")
                }
            ),
            "weighted_revalued_notional_revenue": hx.Structure(children={
                "last_10_years": hx.Float(mode="output", view={"label": "Last 10 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_15_years": hx.Float(mode="output", view={"label": "Last 15 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),    
                "last_20_years": hx.Float(mode="output", view={"label": "Last 20 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_10_years_oc": hx.Float(mode="output", view={"label": "Last 10 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_15_years_oc": hx.Float(mode="output", view={"label": "Last 15 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),    
                "last_20_years_oc": hx.Float(mode="output", view={"label": "Last 20 yrs", "format": {"thousandSeparated": True, "mantissa": 0}})
                },
                view={"label": "Weighted Revalued Notional Revenue"}
            ),
            "developed_weighted_revalued_notional_revenue": hx.Structure(children={
                "last_10_years": hx.Float(mode="output", view={"label": "Last 10 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_15_years": hx.Float(mode="output", view={"label": "Last 15 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_20_years": hx.Float(mode="output", view={"label": "Last 20 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),       
                "last_10_years_oc": hx.Float(mode="output", view={"label": "Last 10 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_15_years_oc": hx.Float(mode="output", view={"label": "Last 15 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_20_years_oc": hx.Float(mode="output", view={"label": "Last 20 yrs", "format": {"thousandSeparated": True, "mantissa": 0}})     
                },
                view={"label": "Developed Weighted Revalued Notional Revenue"}
            ),
            "value_of_claims_data": hx.Structure(children={
                "last_10_years": hx.Float(mode="output", view={"label": "Last 10 yrs", "format": {"thousandSeparated": True, "mantissa": 2}}),
                "last_15_years": hx.Float(mode="output", view={"label": "Last 15 yrs", "format": {"thousandSeparated": True, "mantissa": 2}}),
                "last_20_years": hx.Float(mode="output", view={"label": "Last 20 yrs", "format": {"thousandSeparated": True, "mantissa": 2}}),           
                "last_10_years_oc": hx.Float(mode="output", view={"label": "Last 10 yrs", "format": {"thousandSeparated": True, "mantissa": 2}}),
                "last_15_years_oc": hx.Float(mode="output", view={"label": "Last 15 yrs", "format": {"thousandSeparated": True, "mantissa": 2}}),
                "last_20_years_oc": hx.Float(mode="output", view={"label": "Last 20 yrs", "format": {"thousandSeparated": True, "mantissa": 2}}),   
                },
                view={"label": "Value of Claims Data (in Yrs)"}
            ),
            "inflated_incurred_to_quoted_layer": hx.Structure(children={
                "last_10_years": hx.Float(mode="output", view={"label": "Last 10 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_15_years": hx.Float(mode="output", view={"label": "Last 15 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_20_years": hx.Float(mode="output", view={"label": "Last 20 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),   
                "last_10_years_oc": hx.Float(mode="output", view={"label": "Last 10 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_15_years_oc": hx.Float(mode="output", view={"label": "Last 15 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_20_years_oc": hx.Float(mode="output", view={"label": "Last 20 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),          
                },
                view={"label": "Inflated Incurred To Quoted Layer"}
            ),     
            "per_yr_of_claims_data_value": hx.Structure(children={
                "last_10_years": hx.Float(mode="output", view={"label": "Last 10 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_15_years": hx.Float(mode="output", view={"label": "Last 15 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_20_years": hx.Float(mode="output", view={"label": "Last 20 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),      
                "last_10_years_oc": hx.Float(mode="output", view={"label": "Last 10 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_15_years_oc": hx.Float(mode="output", view={"label": "Last 15 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_20_years_oc": hx.Float(mode="output", view={"label": "Last 20 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),         
                },
                view={"label": "Per Year of Claims Data Value" }
            ),  
            "gross_benchmark_experience_rated_premium": hx.Structure(children={
                "last_10_years": hx.Float(mode="output", view={"label": "Last 10 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_15_years": hx.Float(mode="output", view={"label": "Last 15 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_20_years": hx.Float(mode="output", view={"label": "Last 20 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),            
                "last_10_years_oc": hx.Float(mode="output", view={"label": "Last 10 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_15_years_oc": hx.Float(mode="output", view={"label": "Last 15 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "last_20_years_oc": hx.Float(mode="output", view={"label": "Last 20 yrs", "format": {"thousandSeparated": True, "mantissa": 0}}),  
                },
                view={"label": "Gross Benchmark Experience Rate Premium"}
            ),   
            "units_to_view": hx.Str(mode="input", optionality="required", options=["Per Billion", "Per Million", "Per Thousand"], default="Per Billion", view={"label": "Units To View"}),
            "layer_to_view": hx.Str(mode="input", optionality="required", options=["Primary", "1XS", "2XS", "3XS", "4XS", "5XS", "Addl 1", "Addl 2", "Addl 3", "Addl 4", "Addl 5"], default="Primary", view={"label": "Quoted Layer To View"}),
            "experience_ccy": hx.Str(mode="output", view={"label": "CCY"}),
            "layer_to_view_summary": hx.Structure(children={
                "aoc_limit_usd": hx.Float(mode="output", view={"label":"AOC", "group": "Limit (USD)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "agg_limit_usd": hx.Float(mode="output", view={"label": "Agg", "group":"Limit (USD)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "aoc_attachment": hx.Float(mode="output", view={"label": "AOC", "group":"Attachment Excluding Retentions (USD)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "agg_attachment": hx.Float(mode="output", view={"label": "Agg", "group":"Attachment Excluding Retentions (USD)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "aoc_limit_oc": hx.Float(mode="output", view={"label":"AOC", "group": "Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "agg_limit_oc": hx.Float(mode="output", view={"label": "Agg", "group":"Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "aoc_attachment_oc": hx.Float(mode="output", view={"label": "AOC", "group":"Attachment Excluding Retentions", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "agg_attachment_oc": hx.Float(mode="output", view={"label": "Agg", "group":"Attachment Excluding Retentions", "format": {"thousandSeparated": True, "mantissa": 0}}),
                }
            )
        }
    )

    cds.extend_node_rater_defined("cds/experience_rating/claims", {
        # claims inputs
        "claim_id": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Claim ID"}),
        "claim_name": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Claimant Name"}),
        "loss_date": hx.Date(mode="input", default=None, optionality="optional", view={"label": "Loss Date"}),
        "claim_made_date": hx.Date(mode="input", default=None, optionality="optional", view={"label": "Claim Made Date"}),
        "claim_status": hx.Str(mode="input", default=None, optionality="optional", options=["Open","Closed", "Reopened"], view={"label": "Claim Status"}),
        "claim_close_date": hx.Date(mode="input", default=None, optionality="optional", view={"label": "Claim Close Date"}),
        "deductible": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Deductible", "format": thousands_format(0)}),
        "paid_claims": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Paid Claims", "format": thousands_format(0)}),
        "incurred_claims": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Incurred Claims", "format": thousands_format(0)}),
        "transaction_date": hx.Date(mode="input", default=None, optionality="optional", view={"label": "Transaction Date"}),
        "currency": hx.Str(mode="input", options_table="table_input_currency", default_index=0, options_column="ccy", view={"label": "Currency"}),
        "to_use": hx.Bool(mode="output", view={"label": "To Use?", "format": thousands_format(0)}),
        "defense_fgu_paid": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Paid Defense", "format": thousands_format(0), "group":"FGU"}),
        "defense_fgu_os": hx.Float(mode="input", default=None, optionality="optional", view={"label": "OS Defense", "format": thousands_format(0), "group":"FGU"}),
        "indemnity_fgu_paid": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Paid Indemnity", "format": thousands_format(0),"group":"FGU"}),
        "indemnity_fgu_os": hx.Float(mode="input", default=None, optionality="optional", view={"label": "OS Indemnity", "format": thousands_format(0),"group":"FGU"}),
       
        #Claims outputs
        "claim_made_year": hx.Int(mode="output", view={"label": "Claim Made Year", "format": integer_format(0)}),
        "defense_incurred": hx.Float(mode="output", view={"label": "Inc. Defense", "format": thousands_format(0), "group":"Incurred FGU (Local Currency)"}),
        "indemnity_incurred": hx.Float(mode="output", view={"label": "Inc. Indemnity", "format": thousands_format(0), "group":"Incurred FGU (Local Currency)"}),
        "claims_fx_rate": hx.Float(mode="output", view={"label": "FX Rate", "format": {"mantissa": 2}}),
        "policy_year_estimated": hx.Float(mode="output", view={"label": "Est. Policy Year", "format": integer_format(0)}),
        "defense_incurred_usd": hx.Float(mode="output", view={"label": "Inc. Defense", "format": thousands_format(0), "group": "Incurred FGU (USD)"}),
        "indemnity_incurred_usd": hx.Float(mode="output", view={"label": "Inc. Indemnity", "format": thousands_format(0), "group": "Incurred FGU (USD)"}),
        "incurred_total_usd": hx.Float(mode="output", view={"label": "Inc. Total", "format": thousands_format(0), "group": "Incurred FGU (USD)"}),
        "incurred_total_usd_inflated": hx.Float(mode="output", view={"label": "Inc. Total", "format": thousands_format(0),"group":"Inflated FGU (USD)"}),
        "paid_total_usd_inflated":  hx.Float(mode="output", view={"label": "Paid Total", "format": thousands_format(0), "group": "Inflated FGU (USD)"}),
        "total_usd_inflated": hx.Float(mode="output", view={"label": "Total Inflated", "format": thousands_format(0), "group":"Policy Retention #1 Applied FGU (USD)"}),
        "RDC_True": hx.Structure(children={
            "non_ranking_or_maintenance_ded": hx.Float(mode="output"),
            "post_ded_claims": hx.Float(mode="output"),
            "eec": hx.Float(mode="output"),
            "eec_cumulative": hx.Float(mode="output"),
            "agg_retention": hx.Float(mode="output"),
            "final_retention": hx.Float(mode="output"),
            "final_total_incurred": hx.Float(mode="output")
        }),
        "RDC_False": hx.Structure(children={
            "incurred_indemnity_inflated": hx.Float(mode="output"),
            "incurred_defense_inflated": hx.Float(mode="output"),
            "non_ranking_or_maintenance_ded": hx.Float(mode="output"),
            "post_ded_claims": hx.Float(mode="output"),
            "eec": hx.Float(mode="output"),
            "eec_cumulative": hx.Float(mode="output"),
            "agg_retention": hx.Float(mode="output"),
            "final_retention": hx.Float(mode="output"),       
            "final_total_incurred": hx.Float(mode="output")            
        }),
        "att_layer_incurred": hx.Float(mode="output", view={"label":"Incurred Attritional Layer", "format": thousands_format(0)}),
        "att_layer_inflated": hx.Float(mode="output", view={"label":"Inflated Attritional Layer", "format": thousands_format(0)}),
        "att_layer_developed": hx.Float(mode="output", view={"label":"Developed Attritional Layer", "format": thousands_format(0)}),
        "primary": hx.Float(mode="output", view={"label":"Primary", "format": thousands_format(0)}),
        "xs_1": hx.Float(mode="output", view={"label":"1XS", "format": thousands_format(0)}),
        "xs_2": hx.Float(mode="output", view={"label":"2XS", "format": thousands_format(0)}),
        "xs_3": hx.Float(mode="output", view={"label":"3XS", "format": thousands_format(0)}),
        "xs_4": hx.Float(mode="output", view={"label":"4XS", "format": thousands_format(0)}),
        "xs_5": hx.Float(mode="output", view={"label":"5XS", "format": thousands_format(0)}),
        "xs_6": hx.Float(mode="output", view={"label":"6XS", "format": thousands_format(0)}),
        "xs_7": hx.Float(mode="output", view={"label":"7XS", "format": thousands_format(0)}),
        "xs_8": hx.Float(mode="output", view={"label":"8XS", "format": thousands_format(0)}),
        "xs_9": hx.Float(mode="output", view={"label":"9XS", "format": thousands_format(0)}),
        "xs_10": hx.Float(mode="output", view={"label":"10XS", "format": thousands_format(0)}),
        "addl_1": hx.Float(mode="output", view={"label":"Additional 1", "format": thousands_format(0)}),
        "addl_2": hx.Float(mode="output", view={"label":"Additional 2", "format": thousands_format(0)}),
        "addl_3": hx.Float(mode="output", view={"label":"Additional 3", "format": thousands_format(0)}),
        "addl_4": hx.Float(mode="output", view={"label":"Additional 4", "format": thousands_format(0)}),
        "addl_5": hx.Float(mode="output", view={"label":"Additional 5", "format": thousands_format(0)}),
        "to_use_experience": hx.Bool(mode="output"),


        # claims outputs
        "use_claim": hx.Bool(mode="output", view={"label": "Use Claim?"}),
        "estimated_yoa": hx.Int(mode="override", view={"label": "Estimated YOA", "format": integer_format(0)}),
        # columns to currency convert claims values
        "total_incurred_clm_curr": hx.Float(mode="output", view={"label": "Total Incurred (Claim Currency)", "format": thousands_format(0)}),
        "clm_to_slip_fx_rate": hx.Float(mode="output", view={"label": "FX Rate to Slip Currency", "format": thousands_format(2)}),
        "total_incurred": hx.Float(mode="output", view={"label": "Total Incurred (Slip Currency)", "format": thousands_format(0)}),
        # columns to inflate/develop claims
        "inflated_total_incurred": hx.Float(mode="output", view={"label": "Inflated Total Incurred (Slip Currency)", "format": thousands_format(0)}),
        "claims_development": hx.Float(mode="output", view={"label": "Claims Development", "format": percent_format(2)}),
        "development_method": hx.Str(mode="output", view={"label": "Development Method"}),
        "developed_inflated_total_incurred": hx.Float(mode="output", view={"label": "Developed Inflated Total Incurred (Slip Currency)", "format": thousands_format(0)}),
        
        # add repeating columns for the various layers
        **{f"deductible_to_use_layer_{index}": hx.Float(mode="override", view={"label": f"Layer {index}: Deductible to use", "format": thousands_format(0)}) for index in range(1,max_layers+1)},
        **{f"limit_layer_{index}": hx.Float(mode="output", view={"label": f"Layer {index}: Limit", "format": thousands_format(0)}) for index in range(1,max_layers+1)},
        **{f"excess_layer_{index}": hx.Float(mode="output", view={"label": f"Layer {index}: Excess", "format": thousands_format(0)}) for index in range(1,max_layers+1)},
        **{f"cl_developed_total_incurred_layer_{index}": hx.Float(mode="output", view={"label": f"Layer {index}: CL Developed Total Incurred (Slip Currency)", "format": thousands_format(0)}) for index in range(1,max_layers+1)},
    })

    cds.extend_node_rater_defined("cds/experience_rating", {
        # experience rating table, includes columns for both FGU and non FGU claims
        "experience_table": hx.List(mode="input", max_element_count=20, children={

            "yoa": hx.Int(mode="output", view={"label": "YOA", "format": integer_format(0)}),
            "exposure": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Exposure", "format": thousands_format(0)}),
            "exposure_onlevelled": hx.Float(mode="output", view={"label": "On-levelled Exposure", "format": thousands_format(0)}),
            "premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Premium", "format": thousands_format(0)}),
            "premium_rate_adjusted": hx.Float(mode="output", view={"label": "Rate Adjusted Premium", "format": thousands_format(0)}),
            
            # columns to summarise information from claims table
            "agg_num_claims": hx.Int(mode="output", view={"label": "Number of Claims"}),
            "agg_sum_claims": hx.Float(mode="output", view={"label": "Sum of Inflated Claims", "format": thousands_format(0)}),
            # checkbox if year is to be used
            "include_year": hx.Bool(mode="override", view={"label": "Include Year?"}),
            
            # non FGU experience rating field to calculate loss ratio based on entered premium and claims
            "loss_ratio": hx.Float(mode="output", view={"label": "Loss Ratio", "format": percent_format(2)}),
            
            # Benchmark ULR for class for FGU experience rating
            "ulr": hx.Float(mode="output", view={"label": "AFB ULR", "format": percent_format(0)}),
            # needed for year weighting
            "claims_development": hx.Float(mode="output", view={"label": "AFB Claims Development", "format": percent_format(0)}), 
            # placeholder to use triangles to create insured specific development pattern
            "alternate_claims_development": hx.Float(mode="output", view={"label": "Insured Claims Development", "format": percent_format(0)}),
            # type of development to use (IELR, BF, Chain Ladder)
            "development_method": hx.Str(mode="output", view={"label": "Development Method"}),

            # Chain ladder developed claims for each priced layer
            **{f"cl_developed_layer_{index}": hx.Float(mode="output", view={"label": f"Layer {index}: CL Developed Incurred Claims", "format": thousands_format(0)}) for index in range(1,max_layers+1)},
            # ultimated claims for each priced layer based on development method
            **{f"ult_layer_{index}": hx.Float(mode="output", view={"label": f"Layer {index}: Ultimate Incurred Claims", "format": thousands_format(0)}) for index in range(1,max_layers+1)},
            # ultimate claims transformed into a claims per unit on-levelled exposure
            **{f"ult_rate_layer_{index}": hx.Float(mode="output", view={"label": f"Layer {index}: Ultimate Losses per m Exposure", "format": thousands_format(0)}) for index in range(1,max_layers+1)},
            
            # calculation of weights to years
            "exposure_weight": hx.Float(mode="output", view={"label": "Exposure Weight", "format": percent_format(0)}),
            "decay_weight": hx.Float(mode="output", view={"label": "Decay Weight", "format": percent_format(0)}),
            "development_weight": hx.Float(mode="output", view={"label": "Development Weight", "format": percent_format(0)}),
            "overall_score": hx.Float(mode="output", view={"label": "Overall Score", "format": percent_format(0)}),
            # normalise weights to sum to 100%
            "weight_to_year": hx.Float(mode="output", view={"label": "Weight to Year", "format": percent_format(0)}),
        })
    })

    cds.extend_node_rater_defined("cds/experience_rating", {
       #output structure for experience rating
        **{
            f"summary_layer_{index}": hx.Structure(view={"label": f"Layer {index}"}, children={
                "expected_loss_ratio": hx.Float(mode="output", view={"label": "Expected Loss Ratio", "format": percent_format(2)}),
                "loss_rate": hx.Float(mode="output", view={"label": "Loss Rate", "format": thousands_format(0)}),
                "expected_losses": hx.Float(mode="output", view={"label": "Expected Losses", "format": thousands_format(0)}),
                "filter": hx.Bool(mode="output")
                })
                for index in range(1,max_layers+1)
            },
        
        #trial setup for triangles using both an input and output example
        "use_triangle": hx.Bool(mode="input", default=False, view={"label": "Enable claims triangle?"}),
        "use_output_triangle": hx.Bool(mode="input", default=False, view={"label": "Enable output driven triangle?"}),
        #input triangle
        "triangle": hx.Triangle(mode="input", 
                                default_average="n_wtd_avg", 
                                averages={"simple": {"label": "Simple Average","average_type": "simple","latest_diagonal": "include","last_n_origin_periods": None},
                                            "wtd_avg": {"label": "Weighted Average","average_type": "column_sum","latest_diagonal": "include","last_n_origin_periods": None},
                                            "n_wtd_avg": {"label": "N Weighted Average","average_type": "column_sum","latest_diagonal": "include","last_n_origin_periods": 5,"last_n_origin_periods_editable": True,},}),
        #output triangle
        "output_triangle": hx.Triangle(mode="output", 
                                default_average="n_wtd_avg", 
                                averages={"simple": {"label": "Simple Average","average_type": "simple","latest_diagonal": "include","last_n_origin_periods": None},
                                            "wtd_avg": {"label": "Weighted Average","average_type": "column_sum","latest_diagonal": "include","last_n_origin_periods": None},
                                            "n_wtd_avg": {"label": "N Weighted Average","average_type": "column_sum","latest_diagonal": "include","last_n_origin_periods": 5,"last_n_origin_periods_editable": True,},})
    })