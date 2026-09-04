import hx_data_schema as hx
from data_schema.utilities import thousands_format, percent_format, integer_format, set_node_properties, run_schedule_rater_async_tasks
from algorithms.constant import MAX_LAYERS


def claims_layer_cols():
    d={}
    for index in range(1,MAX_LAYERS+1):
        # note the use of '=' here instead of ':'
        d[f"deductible_to_use_layer_{index}"] = hx.Float(mode="override", async_input=["pull_exchange_rate_claim_data_task"], view={"label": f"Layer {index}: Deductible to use", "format": thousands_format(0)})
        d[f"limit_layer_{index}"] = hx.Float(mode="output", async_input=["pull_exchange_rate_claim_data_task"], view={"label": f"Layer {index}: Limit", "format": thousands_format(0)})
        d[f"excess_layer_{index}"] = hx.Float(mode="output", async_input=["pull_exchange_rate_claim_data_task"], view={"label": f"Layer {index}: Excess", "format": thousands_format(0)})
        d[f"cl_developed_total_incurred_layer_{index}"] = hx.Float(mode="output", async_input=["pull_exchange_rate_claim_data_task"], view={"label": f"Layer {index}: CL Developed Total Incurred (Slip Currency)", "format": thousands_format(0)})
    return d


def claim_peril_agg_cols():
    d={}
    for peril in ["Fire","Named Windstorm","SCS","Flood","Quake","Wildfire"]:
        # note the use of '=' here instead of ':'
        d[f"num_claims_{peril.replace(' ', '_').lower()}"] = hx.Int(mode="output", view={"label": f"Number of {peril} claims"})
        d[f"unadj_sum_claims_{peril.replace(' ', '_').lower()}"] = hx.Float(mode="output", view={"label": f"Sum of Unadjusted {peril} claims", "format": thousands_format(0)})
        d[f"sum_claims_{peril.replace(' ', '_').lower()}"] = hx.Float(mode="output", view={"label": f"Sum of Inflated {peril} claims", "format": thousands_format(0)})
    return d

def cat_noncat_layer_res_cols():
    d={}
    # commented out as removing Cat component from experience rating for now
    # for IsCat in ["Non Cat", "Cat"]:
    for IsCat in ["Non Cat"]:
        for index in range(1,MAX_LAYERS+1):
            # note the use of '=' here instead of ':'
            # Chain ladder developed claims for each priced layer split by cat/non-cat
            d[f"{IsCat.replace(' ', '_').lower()}_cl_developed_layer_{index}"] = hx.Float(mode="output", view={"label": f"Layer {index}: {IsCat} CL Developed Incurred Claims", "format": thousands_format(0)})
            # ultimated claims for each priced layer based on development method split by cat/non-cat
            d[f"{IsCat.replace(' ', '_').lower()}_ult_layer_{index}"] = hx.Float(mode="output", view={"label": f"Layer {index}: {IsCat} Ultimate Incurred Claims", "format": thousands_format(0)})
            # ultimate claims transformed into a claims per unit on-levelled exposure split by cat/non-cat
            d[f"{IsCat.replace(' ', '_').lower()}_ult_rate_layer_{index}"] = hx.Float(mode="output", view={"label": f"Layer {index}: {IsCat} Ultimate Loss Rate", "format": percent_format(3)})
            # ultimate claims transformed into a loss ratio
            d[f"{IsCat.replace(' ', '_').lower()}_ult_loss_ratio_layer_{index}"] = hx.Float(mode="output", view={"label": f"Layer {index}: {IsCat} Ultimate Loss Ratio", "format": percent_format(1)})
    return d

def experience_rating():
    experience_rating_schema = hx.Structure(children={
        # show/hide flags used to control the view and experience rating calcs
        "claims_available": hx.Bool(mode="input", default=False, view={"label": "Loss Data Available?"}),
        "claims_fgu": hx.Bool(mode="input", default = False, view={"label": "Are claims values from the ground up?", "info": "If the claims values represent the loss to the historic year's layer, with no information about excess/deductible, untick this box?"}),
        "claims_net_of_deductible": hx.Bool(mode="input", default = False, view={"label": "Are Claims net of Deductible?"}),
        
        # show/hide flags used to control the view
        "use_experience_rating_basic": hx.Bool(mode="output", async_input=["apply_experience_adjustment_task"]),
        "use_experience_rating_agg": hx.Bool(mode="output", async_input=["apply_experience_adjustment_task"]),
        "use_experience_rating_full": hx.Bool(mode="output", async_input=["apply_experience_adjustment_task"]),
        "show_claims_input_table": hx.Bool(mode="output"),

        # input instructions node
        "input_instructions": hx.Str(mode = "output", view = {"label": "Instructions"}),

        # double loop like this only works if keys are idnetical, but cannot have more than one key in a loop 
        # unless you use a helper function see top of this file
        **{
            f"{name}_{index}": hx.Bool(mode="output") 
            for index in range(1, MAX_LAYERS+1) 
            for name in ["claims_show_layer", "calculation_show_layer"]
        },
        #show/hide field for additional detail on the weighting calculation
        "show_weights": hx.Bool(mode="input", default=False, view={"label": "Show Weight Breakdown Details"}),
        #show/hide field for additional calculated fields in the full experience rating
        "show_to_layer_fields": hx.Bool(mode="input", default=False, view={"label": "Show To Layer Claims"}),

        #fields to use for validation to ensure run_schedule_rater_task is run after applying experience adjustments
        "experience_rating_run": hx.Bool(mode="input", optionality="optional", default=None, async_output=["run_schedule_rater_task", "apply_experience_adjustment_task", "remove_experience_adjustment_task"], view={"read_only": True}),
        "run_rater_run": hx.Bool(mode="input", optionality="optional", default=None, async_output=["run_schedule_rater_task", "apply_experience_adjustment_task", "remove_experience_adjustment_task"], view={"read_only": True}),

        #simplest experience rating (basic lookup from clean years)
        "experience_rating_basic": hx.Structure(children={
            "clean_years": hx.Str(mode="input", default="0", options_table="basic_experience_rating", options_column="Clean Years",  view={"label": "No. Of Years Since Last Claim"}),
            "experience_adjustment": hx.Float(mode="output", async_input=["apply_experience_adjustment_task"], view={"label": "Suggested Experience Adjustment", "format": percent_format(1)}),
        }),

        # claims capture table
        "claims": hx.List(mode="input", children={
            #claims inputs
            "claim_id": hx.Str(mode="input", default=None, optionality="optional", async_input=["pull_exchange_rate_claim_data_task"], view={"label": "Claim ID"}),
            "claim_made_date": hx.Date(mode="input", default=None, optionality="optional", async_input=["pull_exchange_rate_claim_data_task"], view={"label": "Claim Made Date"}),
            "claim_status": hx.Str(mode="input", default="Closed", options=["Open","Closed"], async_input=["pull_exchange_rate_claim_data_task"], view={"label": "Claim Status"}),
            "cause_of_loss": hx.Str(mode="input", default="Fire", options=["Fire","Named Windstorm","SCS","Flood","Quake","Wildfire"], async_input=["pull_exchange_rate_claim_data_task"], view={"label": "Cause of Loss"}),
            "deductible": hx.Float(mode="input", default=0, optionality="optional", async_input=["pull_exchange_rate_claim_data_task"], view={"label": "Deductible", "format": thousands_format(0)}),
            "incurred_claims": hx.Float(mode="input", default=0, optionality="optional", async_input=["pull_exchange_rate_claim_data_task"], view={"label": "Incurred Claims", "format": thousands_format(0)}),
            "currency": hx.Str(mode="override", options_column="currency", options_table="currency", async_input=["pull_exchange_rate_claim_data_task"], view={"label": "Claim Currency"}),
            
            #claims outputs
            "use_claim": hx.Bool(mode="output", async_input=["pull_exchange_rate_claim_data_task"], view={"label": "Use Claim?"}),
            "is_cat": hx.Bool(mode="output", async_input=["pull_exchange_rate_claim_data_task"], view={"label": "Is Cat?"}),
            "estimated_yoa": hx.Int(mode="override", async_input=["pull_exchange_rate_claim_data_task"], view={"label": "Estimated YOA", "format": integer_format(0)}),
            # columns to currency convert claims values
            "total_incurred_clm_curr": hx.Float(mode="output", async_input=["pull_exchange_rate_claim_data_task"], view={"label": "Total Incurred (Claim Currency)", "format": thousands_format(0)}),
            "clm_to_slip_fx_rate": hx.Float(mode="input", optionality="optional", default=None, async_output=["pull_exchange_rate_claim_data_task"], view={"label": "FX Rate to Slip Currency", "read_only": True, "format": thousands_format(2)}),
            "exchange_rate_date": hx.Str(mode="input", optionality="optional", default=None, async_output=["pull_exchange_rate_claim_data_task"], view={"label": "Exchange Rate Date", "read_only": True}),
            "total_incurred": hx.Float(mode="output", async_input=["pull_exchange_rate_claim_data_task"], view={"label": "Total Incurred (Slip Currency)", "format": thousands_format(0)}),
            #columns to inflate/develop claims
            "inflated_total_incurred": hx.Float(mode="output", async_input=["pull_exchange_rate_claim_data_task"], view={"label": "Inflated Total Incurred (Slip Currency)", "format": thousands_format(0)}),
            "claims_development": hx.Float(mode="output", async_input=["pull_exchange_rate_claim_data_task"], view={"label": "Claims Development", "format": percent_format(1)}),
            "development_method": hx.Str(mode="output", async_input=["pull_exchange_rate_claim_data_task"], view={"label": "Development Method"}),
            "developed_inflated_total_incurred": hx.Float(mode="output", async_input=["pull_exchange_rate_claim_data_task"], view={"label": "Developed Inflated Total Incurred (Slip Currency)", "format": thousands_format(0)}),
            "sublimit": hx.Float(mode="output", async_input=["pull_exchange_rate_claim_data_task"], view={"label": "Sublimit", "format": thousands_format(0)}),
            
            #add repeating columns for the various layers
            # NOTE: a helper function appears to be th only way to loop through mutliple different keys in the same loop
            **claims_layer_cols(),
        }),


        #experience rating table, includes columns for both FGU and non FGU claims
        "experience_table": hx.List(mode="input", default_element_count=10, max_element_count=10, children={
            "yoa": hx.Int(mode="output", view={"label": "YOA", "format": integer_format(0)}),
            "str_yoa": hx.Str(mode="output", view={"label": "YOA"}),
            "exposure": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Exposure", "format": thousands_format(0)}),
            "exposure_inflation": hx.Float(mode="override", view={"label": "Exposure Inflation", "format": percent_format(1)}),
            "exposure_onlevelled": hx.Float(mode="output", view={"label": "On-levelled Exposure", "format": thousands_format(0)}),
            "premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "100% GG Premium", "format": thousands_format(0)}),
            "premium_rate_change": hx.Float(mode="override", view={"label": "Premium Rate Change", "format": percent_format(1)}),
            "premium_rate_adjusted": hx.Float(mode="output", view={"label": "Rate Adjusted Premium", "format": thousands_format(0)}),
            
            #columns to summarise information from claims table by peril
            **claim_peril_agg_cols(),
            #checkbox if year is to be used
            "include_year": hx.Bool(mode="override", view={"label": "Include Year?"}),
            
            #non FGU experience rating field to calculate loss ratio based on entered premium and claims
            "loss_ratio": hx.Float(mode="output", view={"label": "Non-Cat Loss Ratio", "format": percent_format(1)}), #agg

            # Benchmark ULR for class for FGU experience rating split by cat/non-cat
            "non_cat_ulr": hx.Float(mode="output", view={"label": "AFB Non Cat ULR", "format": percent_format(0)}), #full
            # commented out as removing Cat component from experience rating for now
            # "cat_ulr": hx.Float(mode="output", view={"label": "AFB Cat ULR", "format": percent_format(0)}), #full
            # placeholder to use triangles to create insured specific development pattern
            "claims_development": hx.Float(mode="output", view={"label": "AFB Claims Development", "format": percent_format(0)}),
            # type of development to use (IELR, BF, Chain Ladder)
            "development_method": hx.Str(mode="output", view={"label": "Development Method"}),

            # per layer fields for CL developed, ultimate and utlimate rate claims
            **cat_noncat_layer_res_cols(),
            
            # calculation of weights to years
            "exposure_weight": hx.Float(mode="output", view={"label": "Exposure Weight", "info": "Weight to on-levelled TIV compared to current year. Capped at 100%.", "format": percent_format(0)}),
            "decay_weight": hx.Float(mode="output", view={"label": "Decay Weight", "info": "Weighting to give more credit to recent years' experience.", "format": percent_format(0)}),
            "development_weight": hx.Float(mode="output", view={"label": "Development Weight", "info": "Weighting to give more credit to years with more developed claims.", "format": percent_format(0)}),
            "overall_score": hx.Float(mode="output", view={"label": "Overall Score", "format": percent_format(0)}),
            # normalise weights to sum to 100%
            "weight_to_year": hx.Float(mode="output", view={"label": "Weight to Year", "format": percent_format(0)}),
        }),
        **{
            f"summary_layer_{index}": hx.Structure(view={"label": f"Layer {index}"}, children={
                "non_cat_elr_non_cat_prem": hx.Float(mode="output", view={"label": "Experience Non-Cat ELR to Non-Cat Premium", "format": percent_format(1)}),
                "non_cat_expected_loss_ratio": hx.Float(mode="output", view={"label": "Experience Non-Cat ELR", "format": percent_format(1)}),
                "model_non_cat_loss_ratio": hx.Float(mode="output", view={"label": "Model Non-Cat ELR", "format": percent_format(1)}),
                "non_cat_loss_rate": hx.Float(mode="output", view={"label": "Non-Cat Loss Rate", "format": percent_format(3)}),
                # commented out as removing Cat component from experience rating for now
                # "cat_loss_rate": hx.Float(mode="output", view={"label": "Cat Loss Rate", "format": thousands_format(0)}),
                # "rms_loss_rate": hx.Float(mode="output", view={"label": "RMS Loss Rate", "format": thousands_format(0)}),
                # "combined_loss_rate": hx.Float(mode="output", view={"label": "Combined Loss Rate", "format": thousands_format(0)}),
                "non_cat_expected_losses": hx.Float(mode="output", view={"label": "Experience Non-Cat Expected Losses", "format": thousands_format(0)}),
                "model_non_cat_expected_losses": hx.Float(mode="output", view={"label": "Model Non-Cat Expected Losses", "format": thousands_format(0)}),
                "cred_weight": hx.Float(mode="output", view={"label": "Credibility Weighting to Experience", "format": percent_format(1)}),
                "experience_adjustment": hx.Float(mode="output", async_input=["apply_experience_adjustment_task"], view={"label": "Suggested Non-Cat Experience Adjustment", "format": percent_format(1)}),
                "filter": hx.Bool(mode="output")
                })
                for index in range(1,MAX_LAYERS+1)
            },
    })
    return {"experience_rating": experience_rating_schema}