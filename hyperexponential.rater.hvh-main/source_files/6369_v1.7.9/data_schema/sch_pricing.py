import hx_data_schema as hx
import data_schema.sch_params as sch_params
import data_schema.sch_utilities as utils

def sch_pricing(cds):
    cds.extend_node_rater_defined("cds", {                                
        "number_of_options":hx.Int(mode="input",default=1,options=[1,2,3,4,5,6],async_input=['generate_recommended_peril_inclusions','rarc_task'],view={"label":"Number of Options"}),
        "show_option_to_bind_factor":hx.Bool(mode="output"),
        "option_to_bind":hx.Int(mode="output",async_input=['rarc_task'],view={"label":"Bound Option"}),
        "option_to_bind_zero_indexed":hx.Int(mode="output",view={"label":"Option To Bind"}),
        "option_to_show":hx.Int(mode="input",default=1,async_input=['rarc_task'],options_data="../options_to_show_dropdown", options_field="option_to_show", optionality="optional",view={"label":"Option To Show"}),
        "options_to_show_dropdown": hx.List(mode="output", children={
            "option_to_show":hx.Int(mode="output", view={"label": "Option To Show"})
            }),
        "show_liability_collection_and_table":hx.Bool(mode="output"),
        "show_full_pricing_tables":hx.Bool(mode="input",default=False,view={"label":"Show Full Pricing Tables"}),
        "kpis_show_aop_break_down":hx.Bool(mode="input",default=False,view={"label":"Show Full AOP Breakdown"}),
        "kpis_show_rates":hx.Bool(mode="output"),
        "kpis_show_premiums":hx.Bool(mode="output"),
        "show_modifiers_breakdown":hx.Bool(mode="output",view={"label":"Show Modifiers Breakdown"}),
        "ws_deductible_is_all_perils":hx.Bool(mode="output"),
        "ws_deductible_is_not_all_perils":hx.Bool(mode="output"),
        "kpis_rate_premium_toggle":hx.Str(mode="input",default_index=0,options=["Rate per 100 TIV","Premium"],view={"label":"Rate/Premium Toggle"}),
        **{f"show_{opt}_option": hx.Bool(mode="output") for opt in sch_params.all_perils},
        **{f"show_{opt}_options": hx.Bool(mode="output") for opt in sch_params.all_perils},
        **{f"show_full_pricing_tables_{opt}":hx.Bool(mode="input",default=False,view={"label":f"Show Full {label} Breakdown"}) for opt, label in sch_params.all_perils_dict.items()},
        "notes":hx.Structure(children={
            "paf_pricing_collectible_classification_note": hx.Str(mode="input", default="By continuing you confirm that no individual item is >$25k in value (wine no greater than $1k)", view={"options": {"read_only": {"read_only": True}}}),
            "equipment_breakdown_note": hx.Str(mode="input", default="By continuing you confirm that the TIV is <$20m, if not then please refer to Katie", view={"read_only":True}),
            "aop_modifiers_breakdown_note": hx.Str(mode="input", default="Factors will be the same across all options if TIV is the same across all options.", view={"options": {"read_only": {"read_only": True}}}),
            "paf_modifiers_breakdown_note": hx.Str(mode="input", default="Factors will be the same across all options if the inclusion/exclusion of WS, EQ, Excess FL Wildfire coverages are the same across all options.", view={"options": {"read_only": {"read_only": True}}}),
            "underwriter_adjustments_hvh": hx.Str(mode="input",default="Please enter reason for adjustment.",view={"label":"UW Adj factor (reason)"}),
            "underwriter_adjustments_paf": hx.Str(mode="input",default="Please enter reason for adjustment.",view={"label":"UW Adj factor (reason)"}),
            "rationale_description": hx.Str(mode="input",default="Please provide details on the following:\n- High level view of risk\n- Territory profile\n- History of account/insured\n- Cat exposure\n- Loss experience"),
            "rationale_special_processing": hx.Str(mode="input",default="- Forms/Wordings (manuscript, policy change etc)\n- Authority approval (LOA)"),
            "rationale_underwriter_thoughts": hx.Str(mode="input",default="- Future concerns, intentions, or items to monitor"),
            "hvh_cp_deviate_warning": hx.Str(mode="output"),
            "paf_cp_deviate_warning": hx.Str(mode="output"),            
            "hvh_cp_deviate_warning_flag": hx.Bool(mode="output"),
            "paf_cp_deviate_warning_flag": hx.Bool(mode="output"),
            
        }),
        "commercial_rates_base_rels":hx.Structure(children={
            **{f"{peril}": hx.Float(mode="output") for peril in sch_params.all_perils},
        }),
        "pricing_limits_table": hx.Structure(children={
            "show_coverage_a_building_limit": hx.Bool(mode="output"),
            "show_coverage_b_other_structures_limit": hx.Bool(mode="output"),
            "show_coverage_c_personal_property_limit": hx.Bool(mode="output"),
            "show_coverage_d_loss_of_use_limit": hx.Bool(mode="output"),
            "show_coverage_e_additional_living_expense_limit": hx.Bool(mode="output"),
            "show_coverage_l_liability_limit": hx.Bool(mode="output"),
            "show_coverage_m_med_pay_limit": hx.Bool(mode="output"),
        }),
        "show_commercial_premium_breakdown": hx.Bool(mode="input", default=True),
        "show_premium_splits": hx.Bool(mode="output"),
        "show_rate_splits": hx.Bool(mode="output"),
        "lock_layer": hx.Bool(mode="output"),
        "unlock_layer": hx.Bool(mode="output"),
        "wildfire_enabled": hx.Bool(mode="output", async_output=["generate_recommended_peril_inclusions"]),
        "wildfire_disabled": hx.Bool(mode="output", async_output=["generate_recommended_peril_inclusions"])
    }),

    # Adding coverages to the layers list. NOTE this code duplicates all the common fields from layer to each coverage.
    cds.extend_node_items("cds/layers/coverages", {
        "aop": {"label": "AOP"},
        "wildfire": {"label":"Wildfire"},
        "ws": {"label": "WS"},
        "liability":{"label":"Liability"},
        "eq": {"label":"EQ"},
        "fl":{"label":"Excess FL"},
        "wildfire":{"label":"Wildfire"},
        "paf":{"label":"PAF"},
        "eb":{"label":"Equipment Breakdown"}
    })

    # Adding a rated-defined field to ALL coverages
    cds.extend_node_rater_defined("cds/layers/coverages", {
        "include_peril": hx.Structure(children={
            "value":hx.Bool(mode="input", default=True, view={"label": "Include Peril"},async_output=['generate_recommended_peril_inclusions']),
            "factor":hx.Float(mode="output",view={"label":"In-Scope TIV"})
        }),
        "coverage_a_building_limit":hx.Int(mode="input",default=0,  async_input=["rarc_task"],view={"label":"Coverage A - Building"}),
        "coverage_b_other_structures_limit":hx.Int(mode="override",view={"label":"Coverage B - Other Structures"}),
        "coverage_c_personal_property_limit":hx.Int(mode="input",default=0,  async_input=["rarc_task"],view={"label":"Coverage C - Personal Property"}),
        "coverage_d_loss_of_use_limit":hx.Int(mode="input",default=0,  async_input=["rarc_task"],view={"label":"Coverage D - Loss of Use"}),
        "coverage_e_additional_living_expense_limit":hx.Int(mode="input",default=0,  async_input=["rarc_task"],view={"label":"Coverage E - Additional Living Expense"}),
        "coverage_l_liability_limit":hx.Int(mode="input",default=0,  async_input=["rarc_task"],view={"label":"Coverage L - Liability"}),
        "coverage_m_med_pay_limit":hx.Int(mode="input",default=0,  async_input=["rarc_task"],view={"label":"Coverage M - Med Pay"}),
        "sublimits":hx.Structure(children={
            "animal":hx.Int(mode="input",default=0,view={"label":"Animal Liability Limitation"}),
            "diving_board_and_pool":hx.Int(mode="input",default=0,view={"label":"Diving Board & Pool Slide Liability Limitiation"}),
            "trampoline":hx.Int(mode="input",default=0,view={"label":"Trampoline Liability Limitation"}),
            "swimming_pool":hx.Int(mode="input",default=0,view={"label":"Swimming Pool Liability Limitation"}),
            "premises_only":hx.Bool(mode="input",default=False,view={"label":"Premises Only"}),
        }),
        "tiv":hx.Structure(children={
            "value":hx.Float(mode="output",view={"label":"In-Scope TIV", "format": utils.thousands_format(0)}),
            "factor":hx.Float(mode="output",view={"label":"In-Scope TIV"})
        }),
        "base_rate":hx.Float(mode="output",view={"label":"Base Rate","format": utils.percent_format(2)}),
        "modifiers_impact":hx.Structure(children={
            "factor":hx.Float(mode="output",view={"label":"Modifiers Impact"}),
        }),
        "adjusted_base_rate":hx.Float(mode="output",view={"label":"Adjusted Base Rate","format": utils.percent_format(2)}),
        "minimum_rate":hx.Float(mode="output",view={"label":"Minimum Rate","format": utils.percent_format(2)}),
        "final_modified_rate":hx.Float(mode="output",view={"label":"Final Modified Rate","format":utils.percent_format(2)}),
        "minimum_deductible":hx.Float(mode="output",view={"label":"Minimum Deductible", "format": utils.thousands_format(0)}),
        "final_deductible":hx.Float(mode="output",view={"label":"Final Deductible", "format": utils.thousands_format(0)}),
        "deductible_impact":hx.Float(mode="output",view={"label":"Deductible Impact"}),
        "model_rate": hx.Float(mode="output",view={"label":"Model Rate","format":utils.percent_format(3)}),
        "expected_loss_cost": hx.Float(mode="output",view={"label":"Expected Loss Cost"}),
        "commercial_rates_rater_rels":hx.Float(mode="output",view={"label":"Commercial Rates - Rater Rels"})
    })

    # Adding a rated-defined fields to AOP.
    cds.extend_node_rater_defined("cds/layers/coverages/aop", {
        "model_premium_water_damage":hx.Float(mode="output",view={"label":"Final Expected Losses (Water Damage)","format": utils.thousands_format(0)}),
        "model_premium_hail":hx.Float(mode="output",view={"label":"Final Expected Losses (Hail)","format": utils.thousands_format(0)}),
        "model_premium_fire":hx.Float(mode="output",view={"label":"Final Expected Losses (Fire)","format": utils.thousands_format(0)}),
        "model_premium_other":hx.Float(mode="output",view={"label":"Final Expected Losses (Other)","format": utils.thousands_format(0)}),
        "model_rate_water_damage":hx.Float(mode="output",view={"label":"Final Loss Rate (Water Damage)","format": utils.percent_format(3)}),
        "model_rate_hail":hx.Float(mode="output",view={"label":"Final Loss Rate (Hail/Wind)","format": utils.percent_format(3)}),
        "model_rate_fire":hx.Float(mode="output",view={"label":"Final Loss Rate (Fire)","format": utils.percent_format(3)}),
        "model_rate_other":hx.Float(mode="output",view={"label":"Final Loss Rate (Other)","format": utils.percent_format(3)}),  
        "expected_loss_cost_water_damage":hx.Float(mode="output",view={"label":"Expected Loss Cost (Water Damage)"}),
        "expected_loss_cost_hail":hx.Float(mode="output",view={"label":"Expected Loss Cost (Hail/Wind)"}),
        "expected_loss_cost_fire":hx.Float(mode="output",view={"label":"Expected Loss Cost (Fire)"}),
        "expected_loss_cost_other":hx.Float(mode="output",view={"label":"Expected Loss Cost (Other)"}),
        "pflr_water_damage":hx.Float(mode="output",view={"label": "Priced-for Loss Ratio (Water Damage)", "format": utils.percent_format(1)}),
        "pflr_hail":hx.Float(mode="output",view={"label": "Priced-for Loss Ratio (Hail/Wind)", "format": utils.percent_format(1)}),
        "pflr_fire":hx.Float(mode="output",view={"label": "Priced-for Loss Ratio (Fire)", "format": utils.percent_format(1)}),
        "pflr_other":hx.Float(mode="output",view={"label": "Priced-for Loss Ratio (Other)", "format": utils.percent_format(1)}),
        "water_damage_deductible":hx.Float(mode="input",default=0,  async_input=["rarc_task"],allow_custom_value=True,options_table="table_wd_ded_dropdown",options_column="Water Damage Deductible",optionality="optional",view={"label":"Water Damage Deductible", "format": utils.thousands_format(0), "options": {"read_only": {"read_only": True}}}),
        "water_damage_sublimit":hx.Float(mode="input",default_index=0, allow_custom_value=True, async_input=["rarc_task"],options_table="table_wd_sublimit_dropdown",options_column="Water Damage Sublimit",view={"label":"Water Damage Sublimit", "format": utils.thousands_format(0), "options": {"read_only": {"read_only": True}}}),
    })

    # Adding a rated-defined fields to WS.
    cds.extend_node_rater_defined("cds/layers/coverages/ws", {
        "deductible_type":hx.Structure(children={
            "value":hx.Str(mode="input",default_index=0,  async_input=["rarc_task"],options=sch_params.ws_deductible_list,view={"label":"Deductible Type", "options": {"read_only": {"read_only": True}}}),
            "factor":hx.Float(mode="output",view={"label":"Modifiers Impact"}),
        }),
        #"deductible_percent":hx.Float(mode="output",view={"label":"Deductible (%)", "format": utils.percent_format(2)}),
        "deductible_all_perils":hx.Float(mode="output",async_input=["rarc_task"],view={"label":"Deductible (All Perils)","format":utils.thousands_format(0)}),
        #"selected_ws_deductible":hx.Float(mode="output",view={"label":"Selected WS Deductible %","format": utils.percent_format(2)})
    })

    # Adding a rated-defined fields to FL.
    cds.extend_node_rater_defined("cds/layers/coverages/fl", {
        "flood_zone":hx.Str(mode="output",view={"label":"Flood Zone"}),
        "xs_building_coverage":hx.Float(mode="override",view={"label":"XS Building Coverage", "format": utils.thousands_format(0)}),
        "xs_contents_coverage":hx.Float(mode="override",view={"label":"XS Contents Coverage", "format": utils.thousands_format(0)}),
    })

    # Adding a rated-defined fields to XS W&H.
    cds.extend_node_rater_defined("cds/layers/coverages/ws", {        
        "xs_building_coverage":hx.Float(mode="override",view={"label":"XS Building Coverage", "format": utils.thousands_format(0)}),
        "xs_contents_coverage":hx.Float(mode="override",view={"label":"XS Contents Coverage", "format": utils.thousands_format(0)}),
    })


    # Adding a rated-defined fields to WF.
    cds.extend_node_rater_defined("cds/layers/coverages/wildfire", {
        "deductible_type_dropdown": hx.List(mode="output", children={
            "type": hx.Str(mode="output", view={"label": "Value"})
        }),
        "deductible_dropdown": hx.List(mode="output", children={
            "value": hx.Float(mode="output", view={"label": "Value"})
        }),
        "deductible_type": hx.Str(mode="input", options_data="../deductible_type_dropdown", options_field="type", optionality="optional", default="AOP", view={"label" : "Deductible Type", "options": {"notSupported":{"style_cell":"hx-neutral"}}}),
        "wildfire_score":hx.Int(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 100}, async_input=["rarc_task"],view={"label": "Wildfire Score", "options": {"read_only": {"read_only": True}}})
    })
    
    cds.extend_node_rater_defined('cds/layers', {
        "name": hx.Str(mode="output", view={"label": "Layer"}),
        "layer_no": hx.Int(mode="output", view={"label": "Layer"}),
        "lock_layers": hx.Bool(mode="output", view={"label": "Locked Layer"}),
        "unlock_layers": hx.Bool(mode="output", view={"label": "Unlocked Layer"}),
        "show_layer":hx.Bool(mode="output"),
        "layer_label":hx.Str(mode="output",view={"label":"Layer Label"}),
        "option_to_bind":hx.Bool(mode="output"),
        "coverage_a_building_limit":hx.Int(mode="input",default=0, async_input=["rarc_task"],async_output=['generate_recommended_peril_inclusions'],view={"label":"Coverage A - Building", "options": {"read_only": {"read_only": True}}}),
        "coverage_b_other_structures_limit":hx.Int(mode="override", async_input=["rarc_task"],view={"label":"Coverage B - Other Structures", "options": {"read_only": {"read_only": True}}}),
        "coverage_c_personal_property_limit":hx.Int(mode="override", async_input=["rarc_task"],view={"label":"Coverage C - Personal Property", "options": {"read_only": {"read_only": True}}}),
        "coverage_d_loss_of_use_limit":hx.Int(mode="override", async_input=["rarc_task"],view={"label":"Coverage D - Loss of Use / Fair Rental Value", "info":"Loss of Use is for HO3, HO5, HO6. Fair Rental Value is for DP3", "options": {"read_only": {"read_only": True}}}),
        "coverage_e_additional_living_expense_limit":hx.Int(mode="override", async_input=["rarc_task"],view={"label":"Coverage E - Additional Living Expense", "options": {"read_only": {"read_only": True}}}),
        "coverage_l_liability_limit":hx.Int(mode="override", async_input=["rarc_task"],view={"label":"Coverage L - Liability", "options": {"read_only": {"read_only": True}}}),
        "coverage_m_med_pay_limit":hx.Int(mode="input", default=None, options=[0, 1000, 5000, 10000], optionality="optional", allow_custom_value=True,async_input=["rarc_task"],async_output=['generate_recommended_peril_inclusions'],view={"label":"Coverage M - Med Pay", "options": {"notSupported":{"style_cell":"hx-neutral"}, "read_only": {"read_only": True}}}),
        "sublimits":hx.Structure(children={
            "animal_dropdown_options" : hx.List(mode="output", children={
                "value" :hx.Int(mode="output", view={"label": "Value"})
            }),
            "diving_board_dropdown_options" : hx.List(mode="output", children={
                "value" :hx.Int(mode="output", view={"label": "Value"})
            }),
            "trampoline_dropdown_options" : hx.List(mode="output", children={
                "value" :hx.Int(mode="output", view={"label": "Value"})
            }),
            "swimming_pool_dropdown_options" : hx.List(mode="output", children={
                "value" :hx.Int(mode="output", view={"label": "Value"})
            }),
            "animal_included": hx.Bool(mode="input", default=False, view={"label":"Animal Liability Limitation Included"}),
            "diving_board_and_pool_included": hx.Bool(mode="input", default=False, view={"label":"Diving Board & Pool Slide Liability Limitiation Included"}),
            "trampoline_included": hx.Bool(mode="input", default=False, view={"label":"Trampoline Liability Limitation Included"}),
            "swimming_pool_included": hx.Bool(mode="input", default=False, view={"label":"Swimming Pool Liability Limitation Included"}),
            "animal":hx.Int(mode="input", options_data="../animal_dropdown_options", options_field="value", optionality="optional", allow_custom_value=True, default=None, async_input=["rarc_task"],async_output=['generate_recommended_peril_inclusions'],view={"label":"Animal Liability Limitation", "format": utils.thousands_format(), "options": {"read_only": {"read_only": True}, "notSupported":{"style_cell":"hx-neutral"}}}),
            "diving_board_and_pool":hx.Int(mode="input", options_data="../diving_board_dropdown_options", options_field="value", optionality="optional", allow_custom_value=True, default=None, async_input=["rarc_task"],async_output=['generate_recommended_peril_inclusions'],view={"label":"Diving Board & Pool Slide Liability Limitiation", "format": utils.thousands_format(), "options": {"read_only": {"read_only": True}, "notSupported":{"style_cell":"hx-neutral"}}}),
            "trampoline":hx.Int(mode="input", options_data="../trampoline_dropdown_options", options_field="value", optionality="optional", allow_custom_value=True, default=None, async_input=["rarc_task"],async_output=['generate_recommended_peril_inclusions'],view={"label":"Trampoline Liability Limitation", "format": utils.thousands_format(), "options": {"read_only": {"read_only": True}, "notSupported":{"style_cell":"hx-neutral"}}}),
            "swimming_pool":hx.Int(mode="input", options_data="../swimming_pool_dropdown_options", options_field="value", optionality="optional", allow_custom_value=True, default=None, async_input=["rarc_task"],async_output=['generate_recommended_peril_inclusions'],view={"label":"Swimming Pool Liability Limitation", "format": utils.thousands_format(), "options": {"read_only": {"read_only": True}, "notSupported":{"style_cell":"hx-neutral"}}}),
            "premises_only":hx.Bool(mode="input",default=False,  async_input=["rarc_task"],async_output=['generate_recommended_peril_inclusions'],view={"label":"Premises Only", "options": {"read_only": {"read_only": True}}}),
        }),
        "kpis":hx.Structure(children={
            "tiv_split":hx.Structure(children={
                "cov_a_perc":hx.Float(mode="output",view={"label":"Coverage A", "format": utils.percent_format(0)}),
                "cov_b_perc":hx.Float(mode="output",view={"label":"Coverage B", "format": utils.percent_format(0)}),
                "cov_c_perc":hx.Float(mode="output",view={"label":"Coverage C", "format": utils.percent_format(0)}),
                "others_perc":hx.Float(mode="output",view={"label":"All other coverages", "format": utils.percent_format(0)}),
            }),
            "pflr_split":hx.Structure(children={
                "aop_perc":hx.Float(mode="output",view={"label":"AOP", "format": utils.percent_format(0)}),
                "water_damage_perc":hx.Float(mode="output",view={"label":"AOP - Water Damage", "format": utils.percent_format(0)}),
                "hail_perc":hx.Float(mode="output",view={"label":"AOP - Hail", "format": utils.percent_format(0)}),
                "fire_perc":hx.Float(mode="output",view={"label":"AOP - Fire", "format": utils.percent_format(0)}),
                "other_perc":hx.Float(mode="output",view={"label":"AOP - Other", "format": utils.percent_format(0)}),
                "wildfire_perc":hx.Float(mode="output",view={"label":"Wildfire", "format": utils.percent_format(0)}),
                "liability_perc":hx.Float(mode="output",view={"label":"Liability", "format": utils.percent_format(0)}),
                "ws_perc":hx.Float(mode="output",view={"label":"WS", "format": utils.percent_format(0)}),
                "eq_perc":hx.Float(mode="output",view={"label":"EQ", "format": utils.percent_format(0)}),
                "fl_perc":hx.Float(mode="output",view={"label":"Excess FL", "format": utils.percent_format(0)}),
                "eb_perc":hx.Float(mode="output",view={"label":"Equipment Breakdown", "format": utils.percent_format(0)}), 
                "paf_perc":hx.Float(mode="output",view={"label":"PAF", "format": utils.percent_format(0)}),                  
            }),
            **{key: hx.Structure(children={
                "technical_premium": hx.Structure(children={
                    "premium":hx.Float(mode="output", view={"label": "Technical Premium", "format": utils.thousands_format(0)}),
                    "rate":hx.Float(mode="output", view={"label": "Technical Premium", "format": utils.thousands_format(2)}),
                }),
                "commercial_premium_pre_uw_adj": hx.Structure(children={
                    "premium": hx.Float(mode="output", view={"label": "Commercial Premium Pre Adj", "format": utils.thousands_format(0)}),
                    "rate": hx.Float(mode="output", view={"label": "Commercial Premium Pre Adj", "format": utils.thousands_format(2)}),
                    **({
                        "premium_splits": splits_schema("Pre"),
                        "rate_splits": splits_schema("Pre", "rate")
                    } if key == 'hvh' else {})
                }),
                **({"modifiers": hx.Structure(children={
                    "uw_adjustment": hx.Float(mode="output", view={"label": "UW Adjustment", "format": utils.percent_format(2)}),
                })} if key != "total" else {}),  # Include 'modifiers' only for 'hvh' and 'paf'
                "commercial_premium": hx.Structure(children={
                    "premium":hx.Float(mode="output" if key == 'total' else "override",
                        async_input=["rarc_task"], view={
                            "label": "Commercial Premium Post Adj",
                            "format": utils.thousands_format(0),
                            **({"options": {"read_only": {"read_only": True}}} if key != 'total' else {})}),
                    "rate":hx.Float(mode="output" if key == 'total' else "override",
                        async_input=["rarc_task"], view={
                            "label": "Commercial Premium Post Adj", 
                            "format": utils.thousands_format(2),
                            **({"options": {"read_only": {"read_only": True}}} if key != 'total' else {})}),
                    **({
                        "premium_splits": splits_schema(suffix="Post", section="hvh"),
                        "rate_splits": splits_schema(suffix="Post", section="hvh", node_type="rate"),
                    } if key == 'hvh' else {})
                }),
                "benchmark_premium": hx.Float(mode="output", view={"label": "Benchmark Premium"}),
                "technical_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Technical Premium Pre UW Adjustment"}),
                "tpi": hx.Float(mode="output", view={"label": "TPI", "format": utils.percent_format(2)}),
                "tpi_pre_uw_adj": hx.Float(mode="output", view={"label": "TPI Pre UW Adjustment", "format": utils.percent_format(2)}),
                "pflr": hx.Float(mode="output", view={"label": "PFLR", "format": utils.percent_format(2)}),
                "pflr_pre_uw_adj": hx.Float(mode="output", view={"label": "PFLR Pre UW Adjustment", "format": utils.percent_format(2)}),
                "roc": hx.Float(mode="output", view={"label": "ROC"}),
            }) for key in ["hvh", "paf", "total"]}
        })
    }),


def splits_schema(suffix, section="", node_type="premium"):
    return hx.Structure(children={
        "ho": hx.Float(mode="override" if section=="hvh" else "output", view={"label": f"HO Split {suffix} Adj", "format": utils.thousands_format(2 if node_type == "rate" else 0)}),
        "eq": hx.Float(mode="override" if section=="hvh" else "output", view={"label": f"EQ Split {suffix} Adj", "format": utils.thousands_format(2 if node_type == "rate" else 0)}),
        "excess_flood": hx.Float(mode="override" if section=="hvh" else "output", view={"label": f"FL Split {suffix} Adj", "format": utils.thousands_format(2 if node_type == "rate" else 0)}),
        "equipment_breakdown": hx.Float(mode="override" if section=="hvh" else "output", view={"label": f"EB Split {suffix} Adj", "format": utils.thousands_format(2 if node_type == "rate" else 0)})
    })