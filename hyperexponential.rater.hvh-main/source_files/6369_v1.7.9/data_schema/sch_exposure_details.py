import hx_data_schema as hx
import data_schema.sch_utilities as utils
import data_schema.sch_params as sch_params
import re

# Replace / remove examples with your models exposures
def sch_exposure_details(cds):
    
    # For aggregate exposure e.g. total revenue, sum insured etc. please add to the aggregate exposures node
    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        # PLACEHOLDER value used in experience rating, the experience rating should connect to the total exposure value of the model
        "example_aggregate_exposure": hx.Float(mode="input", default=0, view={"label": "Agg Exposure", "format": utils.thousands_format(0)}),
        "paf":hx.Structure(children={
            "tiv": hx.Float(mode="output", view={"label": "Total TIV", "format": utils.thousands_format(0)}),
            "base_premium": hx.Float(mode="output", view={"label": "Base Premium", "format": utils.thousands_format(0)}),
            "base_rate": hx.Float(mode="output", view={"label": "Base Rate", "format": utils.percent_format(2)}),
            "largest_collection_type": hx.Str(mode="output", view={"label":"Largest Collection Type"}),
        })
         
    })

    # For granular exposure lists e.g. aircrafts, hospitals etc, please add to the granular node
    cds.extend_node_rater_defined("cds/exposure/granular", {        
        # Replace the below with your models exposures
        "example_exposure": hx.List(mode="input",  async_input=["rarc_task"], children={
            "country": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Country"}),
            "city": hx.Str(mode="input", default=None, optionality="optional", view={"label": "City"}),
            "type": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Type"}),
            "tiv": hx.Float(mode="input", default=None, optionality="optional", view={"label": "TIV", "format": utils.thousands_format(0)}),
        }),
        "paf": hx.Structure(children={
            "tiv": hx.Float(mode="output", view={"label": "TIV"}),
            "specific_schedules_structure": hx.Structure(children={
                variable_name: hx.Structure(
                    view={"label": f"{category}"},
                    children={
                        "tiv": hx.Float(mode="input", default=0,  async_input=["rarc_task"], view={"label": "TIV", "format": utils.thousands_format(0)}),
                        "coverage_type": hx.Str(mode="output", view={"label": "Coverage Type"}),
                        "rate": hx.Float(mode="output", view={"label": "Rate", "format": utils.percent_format(2)}),
                    }
                ) 
                for category, schedule, variable_name in sch_params.specific_schedules
            }),
           "specific_schedules_totals_structure":hx.Structure(view={"label":"Total"},children={
                "tiv": hx.Float(mode="output", view={"label": "TIV", "format": utils.thousands_format(0)}),
                "rate": hx.Float(mode="output", view={"label": "Rate","format":utils.percent_format(2)}),
            }),
            "scheduled_and_blanket_coverages_structure": hx.Structure(children={
                variable_name: hx.Structure(
                    view={"label": label}, 
                    children={
                        "scheduled_tiv": hx.Float(mode="input", default=0,  async_input=["rarc_task"], 
                                                view={"label": "Scheduled Coverage TIV", "format": utils.thousands_format(0)}),
                        "scheduled_rate": hx.Float(mode="output", 
                                                view={"label": "Scheduled Rate", "format": utils.percent_format(2)}),
                        **(
                            {} if variable_name in sch_params.excluded_blanket_variables else {
                                "blanket_tiv": hx.Float(mode="input", default=0,  async_input=["rarc_task"], 
                                                        view={"label": "Blanket Coverage TIV", "format": utils.thousands_format(0)}),
                                "blanket_rate": hx.Float(mode="output", 
                                                        view={"label": "Blanket Rate", "format": utils.percent_format(2)}),
                            }
                        )
                    }
                ) 
                for label, variable_name in sch_params.scheduled_and_blanket_coverages
            }),
            "scheduled_and_blanket_coverages_totals_structure":hx.Structure(view={"label":"Total"},children={
                "scheduled_tiv": hx.Float(mode="output", view={"label": "Scheduled Coverage TIV", "format": utils.thousands_format(0)}),
                "scheduled_rate": hx.Float(mode="output", view={"label": "Scheduled Rate","format":utils.percent_format(2)}),
                "blanket_tiv": hx.Float(mode="output", view={"label": "Blanket Coverage TIV", "format": utils.thousands_format(0)}),
                "blanket_rate": hx.Float(mode="output", view={"label": "Blanket Rate","format":utils.percent_format(2)}),
            }),
            "my_dis_coverage":hx.Structure(children={
                "include":hx.Bool(mode="input",default=False,  async_input=["rarc_task"],view={"label":"Coverage Included"}),
                "engagement_ring":hx.Bool(mode="input",default=True,  async_input=["rarc_task"],view={"label":"Engagement Ring Included"}),
                "tiv":hx.Float(mode="input",default=0,  async_input=["rarc_task"],view={"label":"TIV"}),
                "base_premium":hx.Float(mode="output",view={"label":"Mysterious Disappearance Premium"})
            }),
            "wearing_limit":hx.Float(mode="input",  async_input=["rarc_task"],optionality="optional",default=None,view={"label":"Wearing Limit Value"}),
            "paid_claims_amount_last_five_years":hx.Float(mode="input",default=0,  async_input=["rarc_task"],view={"label":"Paid Claims Amount in the Last Five Years", "format": utils.thousands_format(0)}),
            "paid_claims_impact":hx.Float(mode="output",view={"label":"Paid Claims Impact"}),
            "single_item_limit":hx.Str(mode="input",default_index=0,  async_input=["rarc_task"],options=[f"{i}%" for i in range(0, 110, 10)],view={"label":"Single Item %"}),
            "single_item_limit_impact":hx.Float(mode="output",view={"label":"Single Item % Impact"}),
            "based_in_nyc_metro_area":hx.Bool(mode="input",async_input=["rarc_task"],default=False,view={"label":"Based in NYC Metro Area","info":"Bronx\nKings (Brooklyn)\nNew York (Manhattan)\nQueens (Queens)\nRichmond (Staten Island)\nHudson (NJ)"})
        }),
        **{cat: hx.Structure(children={"tiv": hx.Float(mode="output", view={"label": "TIV"})})
            for cat in sch_params.all_perils if cat != "paf"}
    })

