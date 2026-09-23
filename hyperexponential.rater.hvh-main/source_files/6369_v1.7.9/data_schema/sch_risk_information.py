import hx_data_schema as hx
import data_schema.sch_utilities as utils
import data_schema.sch_params as sch_params

# Import parameter lists
product_lines = list(sch_params.product_lines['Values'])
construction_type = list(sch_params.construction_type['Values'])
roof_type = list(sch_params.roof_type['Values'])
building_occupancy = list(sch_params.building_occupancy['Values'])
ppc = list(sch_params.ppc['Values'])
number_of_units_list = sch_params.number_of_units_list
roof_shape_list = sch_params.roof_shape_list
occupation_list = sch_params.occupation_list

# Generate loss history data schema structure
def generate_loss_history_structure(causes):
    """
    Generate a dictionary of loss history structures for given causes.

    Args:
        causes (list of str): List of cause names.

    Returns:
        dict: A dictionary with each cause as a key and an `hx.Structure`
              representing loss history fields as the value.
    """

    def get_label(cause):
        return sch_params.all_perils_dict[cause]

    return {
        cause: hx.Structure(
            view={"label": get_label(cause)},
            children={
                "any_losses_last_five_years": hx.Bool(
                    mode="input",
                    default=False,
                    view={"label": "Any Losses in the Last 5 Years"}
                ),
                "number_of_losses": hx.Int(
                    mode="input",
                    async_input=["rarc_task"],
                    default=0,
                    view={"label": "Number of losses in the last 5 years"}
                ),
                "amount_of_losses": hx.Float(
                    mode="input",
                    async_input=["rarc_task"],
                    default=0,
                    view={
                        "label": "Amount of losses in the last 5 years",
                        "format":utils.thousands_format(0)
                        }
                ),
            },
        )
        for cause in causes
    }

loss_history = generate_loss_history_structure([cov for cov in sch_params.all_perils if cov != 'paf'])

def create_rating_factors_structure(factor_names):
    """
    Creates an HX structure for rating factors based on a given list of factor names.

    Args:
        factor_names (list): List of factor names to include in the structure.

    Returns:
        hx.Structure: HX structure with dynamically generated rating factors.
    """

    def get_factor_label(factor):

        specific_labels = {
            'include_ws':'Include WS',
            'include_eq':'Include EQ',
            'include_fl':'Include Excess FL',
            'tiv_scale':'TIV Scale',
            'ppc':'PPC',
            'distance_to_coast_options':"Distance To Coast",
            "policy_term": "Term Adjustment (in years)"
        }
        if factor in specific_labels.keys():
            return specific_labels[factor]

        return utils.title_rc(factor)

    return hx.Structure(children={
        factor : hx.Structure(view={"label":f"{get_factor_label(factor)}"},children={
            "value":hx.Str(mode="output",view={"label":"Value"}),
            "factor":hx.Float(mode="output", view={"label": "Factor"}),
            "option_to_bind_factor":hx.Float(mode="output", view={"label": "Bound Option Factor"}),
            "variance":hx.Float(mode="output", view={"label": "Variance","format":utils.percent_format(2)}),
            "base_factor":hx.Float(mode="output", view={"label": "Base Factor"}),
        })
        for factor in factor_names
    })
rating_factors_structure = create_rating_factors_structure(sch_params.factor_list)


def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {                                
        # Do not remove
        "policy_option_id": hx.Int(mode="output", view={"label": "Policy Option ID", "format": utils.integer_format(0)}),
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),
        "case_pricing_analysis_location": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Case Pricing Analysis Filepath"}),
        # ~~~~~
        "expiring_policy_reference":hx.Str(mode="output",view={"label": "Expiring Policy Reference"}),
        "brokerage": hx.Float(mode="override", view={"label": "Brokerage","format":utils.percent_format(1),"options": {"read_only": {"read_only": True}}}),
        
        "rating_factors":hx.Structure(children={
            "policy_term": hx.Float(mode="output"),
            "product_line":hx.Str(mode="input",default_index=0,  async_input=["rarc_task","generate_recommended_peril_inclusions"],options=product_lines,view={"label": "Product Line","options": {"read_only": {"read_only": True}}}),
            "construction_type": hx.Str(mode="input",default=None,  async_input=["rarc_task"],optionality='optional',options=construction_type,view={"label": "Construction Type","options": {"read_only": {"read_only": True}, "notSupported":{"style_cell":"hx-neutral"}}}),
            "roof_type": hx.Str(mode="input",default=None,  async_input=["rarc_task"],optionality='optional',options=roof_type,view={"label": "Roof Type","options": {"read_only": {"read_only": True}}}),
            "year_built": hx.Int(mode="input",default=None,  async_input=["rarc_task"],optionality='optional', view={"label": "Year Built","format": utils.integer_format(0),"options": {"read_only": {"read_only": True}}}),
            "roof_year": hx.Int(mode="output", async_input=["rarc_task"], optionality='optional', view={"label": "Roof Year","format":utils.integer_format(0)}),
            "building_occupancy": hx.Str(mode="input",default=None,  async_input=["rarc_task","generate_recommended_peril_inclusions"],optionality='optional',options=building_occupancy,view={"label": "Building Occupancy","options": {"read_only": {"read_only": True}}}),
            "number_of_storeys": hx.Int(mode="input",default=None,  async_input=["rarc_task"],optionality='optional',view={"label": "Number of Storeys","options": {"read_only": {"read_only": True}}}),
            "fire_alarm": hx.Bool(mode="input",default=False,  async_input=["rarc_task"],view={"label": "Fire Alarm","options": {"read_only": {"read_only": True}}}),
            "burglar_alarm": hx.Bool(mode="input",default=False,  async_input=["rarc_task"],view={"label": "Burglar Alarm","options": {"read_only": {"read_only": True}}}),
            "sprinkler": hx.Str(mode="input",default_index=0,  async_input=["rarc_task"],options_table='table_sprinkler',options_column='Values',view={"label": "Sprinkler","options": {"read_only": {"read_only": True}}}),
            "ppc": hx.Int(mode="input",default=None,  async_input=["rarc_task"],optionality='optional',options=ppc,view={"label": "PPC","options": {"read_only": {"read_only": True}}}),
            "updated_wiring_year":hx.Int(default=None,optionality="optional", mode="input",  async_input=["rarc_task"], view={"label": "Updated Wiring Year","format":utils.integer_format(0)}),
            "updated_plumbing_year":hx.Int(default=None,optionality="optional", mode="input",  async_input=["rarc_task"], view={"label": "Updated Plumbing Year","format":utils.integer_format(0)}),
            "updated_heating_year":hx.Int(default=None,optionality="optional", mode="input",  async_input=["rarc_task"], view={"label": "Updated Heating Year","format":utils.integer_format(0)}),
            "updated_roof_year":hx.Int(default=None,optionality="optional", mode="input",  async_input=["rarc_task"], view={"label": "Updated Roof Year", "info":"If Updated Roof Year is empty, the Roof Year is assumed to be the Year Built", "format":utils.integer_format(0)}),
            "square_foot":hx.Int(default=None,optionality="optional", mode="input",allow_custom_value=True,options_table='table_input_sqft',options_column='Values',  async_input=["rarc_task"], view={"label": "Square Foot"}),
            "number_of_units":hx.Str(mode="input",default=None,  async_input=["rarc_task"],options=number_of_units_list,optionality='optional',view={"label": "Number of Units", "options": {"notSupported":{"style_cell":"hx-neutral"}}}),
            "basement":hx.Bool(mode="input",default=False,  async_input=["rarc_task"],view={"label": "Basement","options": {"read_only": {"read_only": True}}}),
            "roof_shape":hx.Str(mode="input",default=None,  async_input=["rarc_task"],optionality='optional',options=roof_shape_list,view={"label":"Roof Shape", "options": {"notSupported":{"style_cell":"hx-neutral"}}}),
            "crime_score":hx.Int(mode="output",  async_input=["rarc_task"],view={"label": "Crime Score"}),
            "wildfire_score":hx.Int(mode="output",  async_input=["rarc_task"],view={"label": "Wildfire Score"}),
            "insured_occupation":hx.Str(mode="input",default_index=0,  async_input=["rarc_task"],options=occupation_list, allow_custom_value = True, view={"label":"Insured Occupation", "options": {"notSupported":{"style_cell":"hx-neutral"}}}),
            "high_profile_client":hx.Bool(mode="input",default=False,  async_input=["rarc_task"],view={"label": "High Profile Client"}),
            "safe":hx.Bool(mode="input",default=False,  async_input=["rarc_task"],view={"label": "Safe"}),
            "credit_score":hx.Int(mode="input",default=None,  async_input=["rarc_task"],optionality='optional',view={"label":"Credit Score","options": {"read_only": {"read_only": True}}}),
            "state_dropdown" : hx.List(mode="output", children={
                "state" :hx.Str(mode="output", view={"label": "State"})
                }),
            "county_dropdown": hx.List(mode="output", children={
                "county":hx.Str(mode="output", view={"label": "County"})
                }),
            "state" : hx.Str(mode="input", options_data="../state_dropdown", options_field="state", optionality="optional", default=None, view={"label" : "State"},async_input=['generate_recommended_peril_inclusions','rarc_task']),
            "county" : hx.Str(mode="input", options_data="../county_dropdown", options_field="county", optionality="optional", default=None, view={"label" : "County"},async_input=['generate_recommended_peril_inclusions','rarc_task']),
            "distance_to_coast":hx.Float(mode="output",view={"label":"Distance to Coast (miles)"},async_input=['generate_recommended_peril_inclusions']),
            "distance_to_coast_options":hx.Str(mode="input",optionality='optional',default=None,  async_input=["rarc_task"],options_table="table_distance_to_coast_options",options_column="Values",view={"label":"Distance to Coast"}),
            "street_number":hx.Str(mode="input",default="",  async_input=["rarc_task"],view={"label":"Street Number"}),
            "street_name":hx.Str(mode="input",default="",  async_input=["rarc_task"],view={"label":"Street Name"}),
            "zip":hx.Str(mode="input",default="",  async_input=["rarc_task"],view={"label":"ZIP Code (5 digits)"}),
            "city":hx.Str(mode="input", options_data="../city_dropdown", options_field="city", optionality="optional", default=None,allow_custom_value=True ,  async_input=["rarc_task"],view={"label":"City", "options": {"notSupported":{"style_cell":"hx-neutral"}}}),
            "city_dropdown": hx.List(mode="output", children={
                "city":hx.Str(mode="output", view={"label": "City"})
                }),
            "state_county_zone":hx.Str(mode="output",view={"label": "State County Zone"}), 
            "retrofit":hx.Bool(mode="input",default=True,  async_input=["rarc_task"],view={"label":"Retrofit"}),
            "soft_storey":hx.Bool(mode="input",default=True,  async_input=["rarc_task"],view={"label":"Soft Storey"}),
            "lowest_floor_elevation":hx.Float(mode="input",default=0,  async_input=["rarc_task"],view={"label":"Lowest Floor Elevation"}),
            **{peril: rating_factors_structure for peril in sch_params.all_perils},
        }),

        "tp_uplift": hx.Structure(children={
            **{
                peril: hx.Structure(children={
                    "tp_uplift_factor" : hx.Structure(view={"label":"TP Uplift Factor"},children={
                        "factor":hx.Float(mode="output", view={"label": "Factor"}),
                        "option_to_bind_factor":hx.Float(mode="output", view={"label": "Factor"}),
        })
                }) for peril in sch_params.all_perils
            }
        }),

        "excess_wind_hail_selected": hx.Bool(mode="output"),
        "excess_wind_hail_not_selected": hx.Bool(mode="output")

    }),
    cds.extend_node_rater_defined("cds/experience_rating", {
        "coverages":hx.Structure(children={
            **loss_history,
            "total":hx.Structure(view={"label":"Total"},children={
                "number_of_losses": hx.Int(mode="output",view={"label": "Number of Losses"}),
                "amount_of_losses": hx.Float(mode="output",view={"label": "Number of Losses","format":utils.thousands_format(0)})
            })
        }),
    })
