# v0.5.0
### --- DEFINING THE NODES HERE SO THAT THEIR PROPERTIES ARE DYNAMICALLY ACCESSIBLE BY THE RATING ALGORITHM --- ###
import hx_data_schema as hx
from algorithms.data_schema.sch_utilities import thousands_format, percent_format, integer_format

### --- TRACK RATER USE OF COVERAGES AND FLEET --- ###
# NOTE: Set RARC_COVERAGE_USE to True if using coverages for Rate Adjusted Rate Change (RARC).
# This setting is stored in cds/rate_change/rarc_coverage_use and can be independent of model_state/coverage_use.
RARC_COVERAGE_USE = False 

# NOTE: Set RARC_INSURED_ASSET_USE to True if the Rate Change is calculated at an insured interest level (e.g., for aircraft, vessels, spacecrafts, etc.).
# This setting is stored in cds/rate_change/rarc_insured_asset_use and can be independent of model_state/insured_asset_use.
RARC_INSURED_ASSET_USE = False 


### --- DEFINE COVERAGES HERE --- ###
# NOTE: provide coverage name and the label for the view
coverages_dict= {"all_risks"                : {"label": "All Risks"},
                    "adverse_weather"          : {"label": "Adverse Weather"},
                    "earthquake"               : {"label": "Earthquake"},
                    "windstorm"                : {"label": "Windstorm"},
                    "wildfire"                 : {"label": "Wildfire"},
                    "terrorism"                : {"label": "Terrorism"},
                    "cyber"                    : {"label": "Cyber"},
                    "national_mourning"        : {"label": "National Mourning"},
                    "riots_and_civil_commotion": {"label": "Riots and Civil Commotion"},
                    "strike"                   : {"label": "Strike"},
                    "war"                      : {"label": "War"},
                    "catastrophic_non_app"     : {"label": "Catastrophic Non-App"},
                    "ec_total"                 : {"label": "Event Cancellation Total"},
                    "na_total"                 : {"label": "Non-Appearance Total"}} 


example_coverage_generic_dict={ 
    "plan_premium_100": hx.Float(mode="output", view={"label": "Gross Plan Premium 100%"}),  
    # "quoted_premium_100": hx.Float(mode="output", view={"label": "Gross Quoted Premium (100%)"}),
    # "technical_premium_100": hx.Float(mode="output", view={"label": "Gross Technical Premium (100%)"}),
    # "benchmark_premium_100": hx.Float(mode="output", view={"label": "Gross Benchmark Premium (100%)"}),
    "plan_rol":         hx.Float(mode="output", view={"label": "Gross Plan Rate-on-Line"}), 
    "quoted_rol":       hx.Float(mode="output", view={"label": "Offered Rate-on-Line"}),
    "quoted_roe":       hx.Float(mode="output", view={"label": "Offered Rate-on-Exposure"}),    


    "plan_premium_pre_uw_adj_100":      hx.Float(mode="output", view={"label": "Gross Plan Premium (Pre-UW Adjustment) 100%"}), 
    "quoted_premium_pre_uw_adj_100":    hx.Float(mode="output", view={"label": "Gross Quoted Premium (Pre-UW Adjustment) 100%"}),
    "technical_premium_pre_uw_adj_100": hx.Float(mode="output", view={"label": "Gross Technical Premium (Pre-UW Adjustment) 100%"}), 
    "benchmark_premium_pre_uw_adj_100": hx.Float(mode="output", view={"label": "Gross Benchmark Premium (Pre-UW Adjustment) 100%"}),
    "plan_rol_pre_uw_adj":              hx.Float(mode="output", view={"label": "Gross Plan (Pre-UW Adjustment) Rate-on-Line"}), 
    "quoted_rol_pre_uw_adj":            hx.Float(mode="output", view={"label": "Offered (Pre-UW Adjustment) Rate-on-Line"}),
    # "quoted_roe": hx.Float(mode="output", view={"label": "Offered Rate-on-Exposure"}),    # not needed pre-uw-adj

    }


COVERAGES_LIST  = list(coverages_dict.keys())
max_coverages   = len(coverages_dict)





def sch_add_coverages_to_layers(cds):
    cds.extend_node_items(        "cds/layers/coverages", {**coverages_dict})                ### --- Adding coverages to the list of layers --- NOTE this code duplicates all the common fields from layer to each coverage.
    cds.extend_node_rater_defined("cds/layers/coverages", {**example_coverage_generic_dict}) ### --- Adding rated-defined field to ALL coverages --- ####

    # ### --- Adding a rated-defined field to a specifc coverage --- #### 
    # for cvg in coverages_dict.keys():
    #     cvg_dict = qp_total_dict if cvg in ['ec_total','na_total'] else qp_coverage_dict
    #     cds.extend_node_rater_defined(f"cds/layers/coverages/{cvg}", {**cvg_dict})
    # cds.extend_node_rater_defined("cds/layers/coverages/example_coverage_2", {**example_coverage_2_specific_dict})
