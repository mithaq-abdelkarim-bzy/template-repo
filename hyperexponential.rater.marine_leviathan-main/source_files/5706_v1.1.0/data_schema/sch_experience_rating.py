import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
from algorithms.rate_constants import max_layers

def sch_experience_rating(cds):

    cds.extend_node_rater_defined("cds/experience_rating", {
        # show/hide flags used to control the view
        "use_experience_rating_basic": hx.Bool(mode="output"),
        "use_experience_rating_agg": hx.Bool(mode="output"),
        "use_experience_rating_full": hx.Bool(mode="output"),
        "show_claims_input_table": hx.Bool(mode="output"),
        **{f"claims_show_layer_{index}": hx.Bool(mode="output") for index in range(1,max_layers+1)},
        **{f"calculation_show_layer_{index}": hx.Bool(mode="output") for index in range(1,max_layers+1)},
        #show/hide field for additional detail on the weighting calculation
        "show_weights": hx.Bool(mode="input", default=False, view={"label": "Show Weight Breakdown Details"}),
        #show/hide field for additional calculated fields in the full experience rating
        "show_to_layer_fields": hx.Bool(mode="input", default=False, view={"label": "Show To Layer Claims"}),

        #simplest experience rating (basic lookup from clean years)
        "experience_rating_basic": hx.Structure(children={
            "clean_years": hx.Str(mode="input", default="0", options_table="table_basic_experience_rating", options_column="Clean Years",  view={"label": "No. Of Years Since Last Claim"}),
            "experience_adjustment": hx.Float(mode="output", view={"label": "Experience Rating Adjustment", "format": percent_format(0)}),
        })
    })

    cds.extend_node_rater_defined("cds/experience_rating/claims", {
        #claims inputs
        "claim_id": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Claim ID"}),
        "loss_date": hx.Date(mode="input", default=None, optionality="optional", view={"label": "Loss Date"}),
        "claim_made_date": hx.Date(mode="input", default=None, optionality="optional", view={"label": "Claim Made Date"}),
        "claim_status": hx.Str(mode="input", default="Closed", options=["Open","Closed"], view={"label": "Claim Status"}),
        "claim_close_date": hx.Date(mode="input", default=None, optionality="optional", view={"label": "Claim Close Date"}),
        "deductible": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Deductible", "format": thousands_format(0)}),
        "paid_claims": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Paid Claims", "format": thousands_format(0)}),
        "incurred_claims": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Incurred Claims", "format": thousands_format(0)}),
        "transaction_date": hx.Date(mode="input", default=None, optionality="optional", view={"label": "Transaction Date"}),
        "currency": hx.Str(mode="override", options_table="table_currency", options_column="currency", view={"label": "Claim Currency"}), # will need to link this to a currency table etc.
        
        #claims outputs
        "use_claim": hx.Bool(mode="output", view={"label": "Use Claim?"}),
        "estimated_yoa": hx.Int(mode="override", view={"label": "Estimated YOA", "format": integer_format(0)}),
        # columns to currency convert claims values
        "total_incurred_clm_curr": hx.Float(mode="output", view={"label": "Total Incurred (Claim Currency)", "format": thousands_format(0)}),
        "clm_to_slip_fx_rate": hx.Float(mode="output", view={"label": "FX Rate to Slip Currency", "format": thousands_format(2)}),
        "total_incurred": hx.Float(mode="output", view={"label": "Total Incurred (Slip Currency)", "format": thousands_format(0)}),
        #columns to inflate/develop claims
        "inflated_total_incurred": hx.Float(mode="output", view={"label": "Inflated Total Incurred (Slip Currency)", "format": thousands_format(0)}),
        "claims_development": hx.Float(mode="output", view={"label": "Claims Development", "format": percent_format(2)}),
        "development_method": hx.Str(mode="output", view={"label": "Development Method"}),
        "developed_inflated_total_incurred": hx.Float(mode="output", view={"label": "Developed Inflated Total Incurred (Slip Currency)", "format": thousands_format(0)}),
        
        #add repeating columns for the various layers
        **{f"deductible_to_use_layer_{index}": hx.Float(mode="override", view={"label": f"Layer {index}: Deductible to use", "format": thousands_format(0)}) for index in range(1,max_layers+1)},
        **{f"limit_layer_{index}": hx.Float(mode="output", view={"label": f"Layer {index}: Limit", "format": thousands_format(0)}) for index in range(1,max_layers+1)},
        **{f"excess_layer_{index}": hx.Float(mode="output", view={"label": f"Layer {index}: Excess", "format": thousands_format(0)}) for index in range(1,max_layers+1)},
        **{f"cl_developed_total_incurred_layer_{index}": hx.Float(mode="output", view={"label": f"Layer {index}: CL Developed Total Incurred (Slip Currency)", "format": thousands_format(0)}) for index in range(1,max_layers+1)},
    })

    cds.extend_node_rater_defined("cds/experience_rating", {
        #experience rating table, includes columns for both FGU and non FGU claims
        "experience_table": hx.List(mode="input", max_element_count=20, children={

            "yoa": hx.Int(mode="output", view={"label": "YOA", "format": integer_format(0)}),
            "exposure": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Exposure", "format": thousands_format(0)}),
            "exposure_onlevelled": hx.Float(mode="output", view={"label": "On-levelled Exposure", "format": thousands_format(0)}),
            "premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Premium", "format": thousands_format(0)}),
            "premium_rate_adjusted": hx.Float(mode="output", view={"label": "Rate Adjusted Premium", "format": thousands_format(0)}),
            
            #columns to summarise information from claims table
            "agg_num_claims": hx.Int(mode="output", view={"label": "Number of Claims"}),
            "agg_sum_claims": hx.Float(mode="output", view={"label": "Sum of Inflated Claims", "format": thousands_format(0)}),
            #checkbox if year is to be used
            "include_year": hx.Bool(mode="override", view={"label": "Include Year?"}),
            #alternative method where a year might be given a partial weight instead of just include/exclude
            # "include_year_2": hx.Float(mode="override", validation={"min_value": 0, "max_value": 1}, view={"label": "Year Weight"}),
            
            #non FGU experience rating field to calculate loss ratio based on entered premium and claims
            "loss_ratio": hx.Float(mode="output", view={"label": "Loss Ratio", "format": percent_format(2)}), #agg
            
            # Benchmark ULR for class for FGU experience rating
            "ulr": hx.Float(mode="output", view={"label": "AFB ULR", "format": percent_format(0)}), #full
            # needed for year weighting
            "claims_development": hx.Float(mode="output", view={"label": "AFB Claims Development", "format": percent_format(0)}), 
            # placeholder to use triangles to create insured specific development pattern
            "alternate_claims_development": hx.Float(mode="output", view={"label": "Insured Claims Development", "format": percent_format(0)}), #full
            # type of development to use (IELR, BF, Chain Ladder)
            "development_method": hx.Str(mode="output", view={"label": "Development Method"}), #full

            # Chain ladder developed claims for each priced layer
            **{f"cl_developed_layer_{index}": hx.Float(mode="output", view={"label": f"Layer {index}: CL Developed Incurred Claims", "format": thousands_format(0)}) for index in range(1,max_layers+1)}, #full
            # ultimated claims for each priced layer based on development method
            **{f"ult_layer_{index}": hx.Float(mode="output", view={"label": f"Layer {index}: Ultimate Incurred Claims", "format": thousands_format(0)}) for index in range(1,max_layers+1)}, #full
            # ultimate claims transformed into a claims per unit on-levelled exposure
            **{f"ult_rate_layer_{index}": hx.Float(mode="output", view={"label": f"Layer {index}: Ultimate Losses per m Exposure", "format": thousands_format(0)}) for index in range(1,max_layers+1)}, #full
            
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
                "expected_loss_ratio": hx.Float(mode="output", view={"label": "Expected Loss Ratio", "format": percent_format(2)}), #agg
                "loss_rate": hx.Float(mode="output", view={"label": "Loss Rate", "format": thousands_format(0)}), #full
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