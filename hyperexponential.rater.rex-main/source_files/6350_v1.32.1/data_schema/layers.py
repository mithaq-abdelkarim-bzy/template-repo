import hx_data_schema as hx
from data_schema.utilities import thousands_format, percent_format, merge_dicts, run_schedule_rater_async_tasks
from data_schema.dropdown_list import new_renewal_list, status_list, elt_for_sim_list, \
    ded_region_list, ded_type_list, ws_tier_list, scs_tier_list, eq_tier_list, \
    fl_region_list, fl_fema_zone_list
from algorithms.constant import MAX_OPTIONS, MAX_LAYERS

def layers_and_perils():
    '''
    Data schema for layer related input and layer related perils
    '''
    return {
        "layers": hx.List(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task", "start_renewal_task", "upsert_hx_meta_pas_references_task"], async_output=[{"task": "copy_primary_deductibles_task", "reset": False}], max_element_count=MAX_LAYERS, children={
            "layer_label": hx.Str(mode="output", view={"label": " " * 25 + "Layer Selector" + " " * 25}),
            # Layer Details Section
            "reference": hx.Str(mode="input", default="", async_output=["start_renewal_task", {"task": "copy_primary_deductibles_task", "reset": False}], async_input=["upsert_hx_meta_pas_references_task"], view={"label": "Reference", "options": {"read_only": {"read_only":True, "label": "Main Reference"}}}),
            "limit": hx.Float(mode="input", default=0, async_input=run_schedule_rater_async_tasks(async_input = True) + ["expiring_policy_fetch_task", "generate_quote_doc_task", "run_simulation_task"], async_output=[{"task": "copy_primary_deductibles_task", "reset": False}], view={"format": thousands_format(), "label": "Limit"}),
            "excess": hx.Float(mode="input", default=0, async_input=run_schedule_rater_async_tasks(async_input = True) + ["generate_quote_doc_task", "run_simulation_task"], async_output=[{"task": "copy_primary_deductibles_task", "reset": False}], view={"format": thousands_format(), "label": "Excess"}),
            "achieved_premium_100_gg": hx.Float(mode="input", default=None, async_input=run_schedule_rater_async_tasks(async_input = True) + ["expiring_policy_fetch_task", "case_pricing_calc_tech_premium_task"], async_output=[{"task": "copy_primary_deductibles_task", "reset": False}], optionality="optional", view={"format": thousands_format(), "label": "Achieved Premium 100% GG Slip Ccy"}),
            "brokerage": hx.Float(mode="input", default=0, async_input=run_schedule_rater_async_tasks(async_input = True) + ["expiring_policy_fetch_task", "generate_quote_doc_task", "case_pricing_calc_tech_premium_task"], async_output=[{"task": "copy_primary_deductibles_task", "reset": False}], view={"format": percent_format(mantissa=2), "label": "Brokerage"}),
            "written_line_perc": hx.Float(mode="input", default=0, async_input=run_schedule_rater_async_tasks(async_input = True) + ["expiring_policy_fetch_task", "generate_quote_doc_task", "run_simulation_task"], async_output=["start_renewal_task",{"task": "copy_primary_deductibles_task", "reset": False}], view={"format": percent_format(mantissa=2), "label": "Signed Line %", "options": {"validation":{"style_cell": "hx-neutral"}}}),
            "quoted_line_perc":  hx.Float(mode="input", default=0, async_input=run_schedule_rater_async_tasks(async_input = True) + ["expiring_policy_fetch_task", "generate_quote_doc_task", "run_simulation_task"], async_output=["start_renewal_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"format": percent_format(mantissa=2), "label": "Quoted Line %"}),

            "new_renewal": hx.Str(mode="input", options=new_renewal_list, default="New", async_output=[{"task": "copy_primary_deductibles_task", "reset": False}, "start_renewal_task"], view={"label": "New/Renewal"}),
            "status": hx.Str(mode="input", options=status_list, default="Quote", async_input=run_schedule_rater_async_tasks(async_input = True)+ ["expiring_policy_fetch_task", "generate_quote_doc_task", "run_simulation_task","upsert_hx_meta_pas_references_task"], async_output=["start_renewal_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "Status"}),
            "additional_reference_1": hx.Str(mode="input", default=None, optionality="optional", async_output=["start_renewal_task"], async_input=["upsert_hx_meta_pas_references_task"], view={"label": "Additional Reference 1"}),
            "additional_reference_2": hx.Str(mode="input", default=None, optionality="optional", async_output=["start_renewal_task"], async_input=["upsert_hx_meta_pas_references_task"], view={"label": "Additional Reference 2"}),
            "additional_reference_3": hx.Str(mode="input", default=None, optionality="optional", async_output=["start_renewal_task"], async_input=["upsert_hx_meta_pas_references_task"], view={"label": "Additional Reference 3"}),
            "additional_reference_4": hx.Str(mode="input", default=None, optionality="optional", async_output=["start_renewal_task"], async_input=["upsert_hx_meta_pas_references_task"], view={"label": "Additional Reference 4"}),
            "additional_reference_5": hx.Str(mode="input", default=None, optionality="optional", async_output=["start_renewal_task"], async_input=["upsert_hx_meta_pas_references_task"], view={"label": "Additional Reference 5"}),
            "additional_reference_6": hx.Str(mode="input", default=None, optionality="optional", async_output=["start_renewal_task"], async_input=["upsert_hx_meta_pas_references_task"], view={"label": "Additional Reference 6"}),
            # US manual RMS inputs
            "quake_aal": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), view={"format": thousands_format(), "label": "US + Canada Quake AAL"}),
            "wind_aal": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), view={"format": thousands_format(), "label": "US + Caribbean Wind AAL"}),
            "quake_sd": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), view={"format": thousands_format(), "label": "US + Canada Quake SD"}),
            "wind_sd": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), view={"format": thousands_format(), "label": "US + Caribbean Wind SD"}),
            "all_perils_sd": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), view={"format": thousands_format(), "label": "US All Perils SD"}),
            "mi_1_in_10_aep_pt": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), view={"format": thousands_format(), "label": "1 in 10 AEP Marginal Impact", "info": "(Property Group + Treaty)"}),
            "mi_1_in_250_oep_pt": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), view={"format": thousands_format(), "label": "1 in 250 OEP Marginal Impact", "info": "(Property Group + Treaty)"}),
            # Intl manual RMS inputs
            "intl_quake_aal": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), view={"format": thousands_format(), "label": "Intl Quake AAL"}),
            "intl_wind_aal": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), view={"format": thousands_format(), "label": "Intl Wind AAL"}),
            "intl_quake_sd": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), view={"format": thousands_format(), "label": "Intl Quake SD"}),
            "intl_wind_sd": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), view={"format": thousands_format(), "label": "Intl Wind SD"}),
            "intl_all_perils_sd": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), view={"format": thousands_format(), "label": "Intl All Perils SD"}),
            "sim_used": hx.Bool(mode="input", default=True, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=[{"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "Use Simulated Results over RMS?"}),
            "elt_for_sim": hx.Str(mode="input", options=elt_for_sim_list, default="GU", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=[{"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "ELT for Simulation"}),

            # Case Pricing Section
            "case_pricing": hx.Structure(children=case_pricing_inputs()),

            # Perils Section
            "perils": hx.Structure(children={
                "fire": hx.Structure(children={
                    "include": hx.Bool(mode="input", default=True, view={"label": "Fire"}, async_input=run_schedule_rater_async_tasks(async_input = True) + ["generate_quote_doc_task"], async_output=[{"task": "copy_primary_deductibles_task", "reset": False}]),
                    "deductible": hx.Float(mode="input", default=None, async_input=run_schedule_rater_async_tasks(async_input = True) + ["copy_fire_ded_task", "expiring_policy_fetch_task", "generate_quote_doc_task"], async_output=[{"task": "copy_primary_deductibles_task", "reset": False}], optionality="optional", view={"label": "Fire Deductible", "format": thousands_format()}),
                    "modifier_summary": hx.Structure(children={
                        "peril_name": hx.Str(mode="output", view={"label": "Peril"}),
                        "no_of_locs": hx.Int(mode="output", view={"label": "No of Locs"}),
                        "sum_tiv_total_usd": hx.Float(mode="output", view={"label": "TIV", "format": thousands_format(mantissa=0)}),
                        **fire_risk_factors(group=False),
                        **rating_metrics(group=False),
                    }),
                    "occupancy_summary": adjustment_factor_summary("Top 10\nOccupancy", total_col=True),
                    "construction_summary": adjustment_factor_summary("Constr.", total_col=True),
                    "sprinkler_summary": adjustment_factor_summary("Sprinkler", total_col=True),
                    "top_20_locations_summary": top_20_locations_summary(fire_risk_factors, rating_metrics),
                    "experience_rating_adj": hx.Float(mode="input", optionality="optional", default=None, async_input=["run_schedule_rater_task", "save_case_pricing_results_task"], async_output=["apply_experience_adjustment_task", "remove_experience_adjustment_task"], view={"label": "Fire", "read_only": True, "format": percent_format(1)}),
                    "machinery_breakdown_summary": hx.List(mode="output", async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], children={
                        "name": hx.Str(mode="input", default=None, optionality="optional", async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "Industry", "read_only": True}),
                        "num_locations": hx.Int(mode="input", default=None, optionality="optional", async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "No of\nLocs", "read_only": True}),
                        "tiv": hx.Int(mode="input", default=None, optionality="optional", async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "Contents + BI\nTIV", "read_only": True}),
                        "fire_mb_proportion": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "Machinery\nBreakdown %", "read_only": True, "format": {"output": "percent", "mantissa": 0}}),
                        "gu_tech_rate": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "GU\nTech Rate", "read_only": True, "format": {"output": "percent", "mantissa": 3}, "info":"Note this is a premium rate"}),
                        "worth": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "Worth", "read_only": True, "format": {"output": "percent", "mantissa": 3}}),
                        "tech_rate": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "Tech Rate", "read_only": True, "format": {"output": "percent", "mantissa": 3}}),
                        "tech_prem": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "Tech Premium", "read_only": True, "format": {"thousandSeparated": True, "mantissa": 0}}),
                        "uw_adj_tech_rate": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "UW Adj\nTech Rate", "read_only": True, "format": {"output": "percent", "mantissa": 3}}),
                        "uw_adj_tech_prem": hx.Float(mode="input", default=None, optionality="optional", async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "UW Adj\nTech Premium", "read_only": True, "format": {"thousandSeparated": True, "mantissa": 0}}),
                    }),
                }),
                "named_windstorm": hx.Structure(children={
                    "include": hx.Bool(mode="input", default=True, view={"label": "Named Windstorm"}, async_input=run_schedule_rater_async_tasks(async_input = True) + ["generate_quote_doc_task", "run_simulation_task"], async_output=[{"task": "copy_primary_deductibles_task", "reset": False}]),
                    "per_occurrence_ded": hx.Float(mode="input", default=None, async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task", "generate_quote_doc_task"], async_output=["copy_fire_ded_task", {"task": "copy_primary_deductibles_task", "reset": False}], optionality="optional", view={"label": "Minimum Per Occurrence Deductible", "format": thousands_format()}),
                    **location_ded_struct([
                        {"node_name": "named_storm_ded", "node_struct": 'hx.Bool(mode="input", default=False, async_output=[{"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "Named Storm Deductible"})'},
                        {"node_name": "region_dropdown", "node_struct": 'hx.Structure(view={"linked_options_selector": "hierarchical"}, linked_options_table="ws_deductible_dropdown", linked_options_columns=["Region", "State", "Tier"], linked_default_index=0, children={ \
                                "region": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=["named_storm_ws_task", "all_tier_fl_ws_task", "fl_ws_task", "tx_ws_task", "tier_fl_ws_task", "all_wind_ws_scs_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "Region"}), \
                                "state": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=["named_storm_ws_task", "all_tier_fl_ws_task", "fl_ws_task", "tx_ws_task", "tier_fl_ws_task", "all_wind_ws_scs_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "State"}), \
                                "tier": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=["named_storm_ws_task", "all_tier_fl_ws_task", "fl_ws_task", "tx_ws_task", "tier_fl_ws_task", "all_wind_ws_scs_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "Tier"}) \
                        })'},
                        {"node_name": "type", "node_struct": 'hx.Str(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=["named_storm_ws_task", "all_tier_fl_ws_task", "fl_ws_task", "tx_ws_task", "tier_fl_ws_task", "all_wind_ws_scs_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], options=ded_type_list, view={"label": "Type"})'},
                        {"node_name": "cell_to_fill", "node_struct": 'hx.Str(mode="output", view={"label": "Cell to fill"})'},
                        {"node_name": "percent", "node_struct": 'hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=["named_storm_ws_task", "all_tier_fl_ws_task", "fl_ws_task", "tx_ws_task", "tier_fl_ws_task", "all_wind_ws_scs_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"format": percent_format(mantissa=2), "label": "%"})'},
                        {"node_name": "location_min_max", "node_struct": 'hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=["named_storm_ws_task", "all_tier_fl_ws_task", "fl_ws_task", "tx_ws_task", "tier_fl_ws_task", "all_wind_ws_scs_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"format": thousands_format(), "label": "Location Min/Max"})'},
                        {"node_name": "sublimit", "node_struct": 'hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=["named_storm_ws_task", "all_tier_fl_ws_task", "fl_ws_task", "tx_ws_task", "tier_fl_ws_task", "all_wind_ws_scs_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"format": thousands_format(), "label": "Sublimit"})'},
                    ]),
                    "crit_cat_zone_total_summary": crit_cat_zone_summary_headline("Wind Crit CAT Zone"),
                    "crit_cat_zone_summary": crit_cat_zone_summary("Wind Crit CAT Zone"),
                    "gate_appetite_summary": gate_appetite_summary("Wind Gate"),
                    "modifier_summary": hx.Structure(children={
                        "peril_name": hx.Str(mode="output", view={"label": "Peril"}),
                        "no_of_locs": hx.Int(mode="output", view={"label": "No of Locs"}),
                        "sum_tiv_total_usd": hx.Float(mode="output", view={"label": "TIV", "format": thousands_format(mantissa=0)}),
                        **windstorm_risk_factors(group=False),
                        **rating_metrics(group=False),
                    }),
                    "gate_summary": adjustment_factor_summary("Top 10\nHurricane Gates"),
                    "ws_zone_summary": adjustment_factor_summary("Hurricane Zones", total_col=True),
                    "distance_from_coast_summary": adjustment_factor_summary("DTC", total_col=True),
                    "year_built_summary": adjustment_factor_summary("Year Built", total_col=True),
                    "risk_category_summary": adjustment_factor_summary("Hurricane\nRisk\nCategory"),
                    "occupancy_summary": adjustment_factor_summary("Top 10\nOccupancy"),
                    "construction_summary": adjustment_factor_summary("Constr."),
                    "top_20_locations_summary": top_20_locations_summary(windstorm_risk_factors, rating_metrics)
                }),
                "scs": hx.Structure(children={
                    "include": hx.Bool(mode="input", default=True, view={"label": "SCS"}, async_input=run_schedule_rater_async_tasks(async_input = True) + ["generate_quote_doc_task"], async_output=[{"task": "copy_primary_deductibles_task", "reset": False}]),
                    "per_occurrence_ded": hx.Float(mode="input", default=None, async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task", "generate_quote_doc_task"], async_output=["copy_fire_ded_task", {"task": "copy_primary_deductibles_task", "reset": False}], optionality="optional", view={"label": "Minimum Per Occurrence Deductible", "format": thousands_format()}),
                    "modifier_summary": hx.Structure(children={
                        "peril_name": hx.Str(mode="output", view={"label": "Peril"}),
                        "num_locs": hx.Int(mode="output", view={"label": "No. Locs"}),
                        "sum_tiv_total_usd": hx.Float(mode="output", view={"label": "TIV", "format": thousands_format(mantissa=0)}),
                        **scs_risk_factors(group=False),
                        **rating_metrics(group=False)
                    }),
                    **location_ded_struct([
                        {"node_name": "region_dropdown", "node_struct": 'hx.Structure(view={"linked_options_selector": "hierarchical"}, linked_options_table="scs_deductible_dropdown", linked_options_columns=["Region", "State", "Tier"], linked_default_index=0, children={ \
                                "region": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["all_wind_ws_scs_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "Region"}), \
                                "state": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["all_wind_ws_scs_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "State"}), \
                                "tier": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["all_wind_ws_scs_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "Tier"}) \
                        })'},
                        {"node_name": "type", "node_struct": 'hx.Str(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["all_wind_ws_scs_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], options=ded_type_list, view={"label": "Type"})'},
                        {"node_name": "cell_to_fill", "node_struct": 'hx.Str(mode="output", view={"label": "Cell to fill"})'},
                        {"node_name": "percent", "node_struct": 'hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["all_wind_ws_scs_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"format": percent_format(mantissa=2), "label": "%"})'},
                        {"node_name": "location_min_max", "node_struct": 'hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["all_wind_ws_scs_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"format": thousands_format(), "label": "Location Min/Max"})'},
                        {"node_name": "sublimit", "node_struct": 'hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["all_wind_ws_scs_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"format": thousands_format(), "label": "Sublimit"})'},                        
                    ]),
                    "risk_category_summary": adjustment_factor_summary("Risk Category"),
                    "construction_summary": adjustment_factor_summary("Construction"),
                    "occupancy_summary": adjustment_factor_summary("Occupancy"),
                    "top_20_locations_summary": top_20_locations_summary(scs_risk_factors, rating_metrics),
                    "experience_rating_adj": hx.Float(mode="input", optionality="optional", default=None, async_input=["run_schedule_rater_task", "save_case_pricing_results_task"], async_output=["apply_experience_adjustment_task", "remove_experience_adjustment_task"], view={"label": "SCS", "read_only": True, "format": percent_format(1)}),
                }),
                "flood": hx.Structure(children={
                    "include": hx.Bool(mode="input", default=True, view={"label": "Flood"}, async_input=run_schedule_rater_async_tasks(async_input = True) + ["generate_quote_doc_task"], async_output=[{"task": "copy_primary_deductibles_task", "reset": False}]),
                    "per_occurrence_ded": hx.Float(mode="input", default=None, async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task", "generate_quote_doc_task"], async_output=["copy_fire_ded_task", {"task": "copy_primary_deductibles_task", "reset": False}], optionality="optional", view={"label": "Minimum Per Occurrence Deductible", "format": thousands_format()}),
                    **location_ded_struct([
                        {"node_name": "region_dropdown", "node_struct": 'hx.Structure(view={"linked_options_selector": "hierarchical"}, linked_options_table="fl_deductible_dropdown", linked_options_columns=["Region", "State", "FEMA Zone"], linked_default_index=0, children={ \
                                "region": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "Region"}), \
                                "state": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "State"}), \
                                "fema_zone": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "FEMA Zone"}) \
                        })'},
                        {"node_name": "type", "node_struct": 'hx.Str(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], options=ded_type_list, view={"label": "Type"})'},
                        {"node_name": "cell_to_fill", "node_struct": 'hx.Str(mode="output", view={"label": "Cell to fill"})'},
                        {"node_name": "percent", "node_struct": 'hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"format": percent_format(mantissa=2), "label": "%"})'},
                        {"node_name": "location_min_max", "node_struct": 'hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"format": thousands_format(), "label": "Location Min/Max"})'},
                        {"node_name": "sublimit", "node_struct": 'hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"format": thousands_format(), "label": "Sublimit"})'},                        
                    ]),
                    "modifier_summary": hx.Structure(children={
                        "peril_name": hx.Str(mode="output", view={"label": "Peril"}),
                        "no_of_locs": hx.Int(mode="output", view={"label": "No of Locs"}),
                        "sum_tiv_total_usd": hx.Float(mode="output", view={"label": "TIV", "format": thousands_format(mantissa=0)}),
                        **flood_risk_factors(group=False),
                        **rating_metrics(group=False),
                    }),
                    "risk_category_summary": adjustment_factor_summary("Flood Risk\nCategory"),
                    "construction_summary": adjustment_factor_summary("Constr."),
                    "num_of_floors_summary": adjustment_factor_summary("Number of\nFloors"),
                    "top_20_locations_summary": top_20_locations_summary(flood_risk_factors, rating_metrics),
                    "experience_rating_adj": hx.Float(mode="input", optionality="optional", default=None, async_input=["run_schedule_rater_task", "save_case_pricing_results_task"], async_output=["apply_experience_adjustment_task", "remove_experience_adjustment_task"], view={"label": "Flood", "read_only": True, "format": percent_format(1)}),
                }),
                "quake": hx.Structure(children={
                    "include": hx.Bool(mode="input", default=True, view={"label": "Quake"}, async_input=run_schedule_rater_async_tasks(async_input = True) + ["generate_quote_doc_task", "run_simulation_task"], async_output=[{"task": "copy_primary_deductibles_task", "reset": False}]),
                    "per_occurrence_ded": hx.Float(mode="input", default=None, async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task", "generate_quote_doc_task", "run_simulation_task"], async_output=["copy_fire_ded_task", {"task": "copy_primary_deductibles_task", "reset": False}], optionality="optional", view={"label": "Minimum Per Occurrence Deductible", "format": thousands_format()}),
                    "ca_quake_include": hx.Bool(mode="input", default=True, async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=[{"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "California Quake Included?"}),
                    **location_ded_struct([
                        {"node_name": "region_dropdown", "node_struct": 'hx.Structure(view={"linked_options_selector": "hierarchical"}, linked_options_table="eq_deductible_dropdown", linked_options_columns=["Region", "State", "Tier"], linked_default_index=0, children={ \
                                "region": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=["ca_eq_task", "all_ca_eq_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "Region"}), \
                                "state": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=["ca_eq_task", "all_ca_eq_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "State"}), \
                                "tier": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=["ca_eq_task", "all_ca_eq_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "Tier"}) \
                        })'},
                        {"node_name": "type", "node_struct": 'hx.Str(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=["ca_eq_task", "all_ca_eq_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], options=ded_type_list, view={"label": "Type"})'},
                        {"node_name": "cell_to_fill", "node_struct": 'hx.Str(mode="output", view={"label": "Cell to fill"})'},
                        {"node_name": "percent", "node_struct": 'hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=["ca_eq_task", "all_ca_eq_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"format": percent_format(mantissa=2), "label": "%"})'},
                        {"node_name": "location_min_max", "node_struct": 'hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=["ca_eq_task", "all_ca_eq_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"format": thousands_format(), "label": "Location Min/Max"})'},
                        {"node_name": "sublimit", "node_struct": 'hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task"], async_output=["ca_eq_task", "all_ca_eq_task", "clear_deductibles_task", {"task": "copy_primary_deductibles_task", "reset": False}], view={"format": thousands_format(), "label": "Sublimit"})'},                        
                    ]),
                    "crit_cat_zone_total_summary": crit_cat_zone_summary_headline("Quake Crit CAT Zone"),
                    "crit_cat_zone_summary": crit_cat_zone_summary("Quake Crit CAT Zone"),
                    "gate_appetite_summary": gate_appetite_summary("Quake Gate"),
                    "modifier_summary": hx.Structure(children={
                        "peril_name": hx.Str(mode="output", view={"label": "Peril"}),
                        "no_of_locs": hx.Int(mode="output", view={"label": "No of Locs"}),
                        "sum_tiv_total_usd": hx.Float(mode="output", view={"label": "TIV", "format": thousands_format(mantissa=0)}),
                        **earthquake_risk_factors(group=False),
                        **rating_metrics(group=False),
                    }),
                    "cresta_summary": adjustment_factor_summary("Top 10 CRESTA\nZones"),
                    "risk_category_summary": adjustment_factor_summary("Earthquake\nRisk\nCategory"),
                    "occupancy_summary": adjustment_factor_summary("Top 10\nOccupancy"),
                    "construction_summary": adjustment_factor_summary("Constr."),
                    "eq_zone_summary": adjustment_factor_summary("EQ Zones", total_col=True),
                    "top_20_locations_summary": top_20_locations_summary(earthquake_risk_factors, rating_metrics)
                }),
                "wildfire": hx.Structure(children={
                    "include": hx.Bool(mode="input", default=True, view={"label": "Wildfire"}, async_input=run_schedule_rater_async_tasks(async_input = True) + ["generate_quote_doc_task"], async_output=[{"task": "copy_primary_deductibles_task", "reset": False}]),
                    "deductible": hx.Float(mode="input", default=None, async_output=["copy_fire_ded_task", {"task": "copy_primary_deductibles_task", "reset": False}], async_input=run_schedule_rater_async_tasks(async_input = True) + ["generate_quote_doc_task"], optionality="optional", view={"label": "Wildfire Deductible", "format": thousands_format()}),
                    "modifier_summary": hx.Structure(children={
                        "peril_name": hx.Str(mode="output", view={"label": "Peril"}),
                        "num_locs": hx.Int(mode="output", view={"label": "No. Locs"}),
                        "sum_tiv_total_usd": hx.Float(mode="output", view={"label": "TIV", "format": thousands_format(mantissa=0)}),
                        **wildfire_risk_factors(group=False),
                        **rating_metrics(group=False)
                    }),
                    "risk_category_summary": adjustment_factor_summary("Risk Category"),
                    "construction_summary": adjustment_factor_summary("Construction"),
                    "occupancy_summary": adjustment_factor_summary("Occupancy"),
                    "top_20_locations_summary": top_20_locations_summary(wildfire_risk_factors, rating_metrics),
                    "experience_rating_adj": hx.Float(mode="input", optionality="optional", default=None, async_input=["run_schedule_rater_task", "save_case_pricing_results_task"], async_output=["apply_experience_adjustment_task", "remove_experience_adjustment_task"], view={"label": "Wildfire", "read_only": True, "format": percent_format(1)}),
                    }),
                "equipment_breakdown": hx.Structure(children={
                    "include": hx.Bool(mode="input", default=True, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=[{"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "Equipment Breakdown"}),
                    "eb_premium": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": "EB premium - 100% Slip Ccy", "read_only": True, "format": thousands_format()}),
                    "actual_eb_premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Actual EB Premium Override", "format": thousands_format(),"info":"If overriding the premium, enter as 100% GG slip currency"}, async_input=["generate_quote_doc_task"]),             
                }),
                "tria": hx.Structure(children={
                    "include": hx.Bool(mode="input", default=True, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=[{"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "TRIA"}),
                    "tria_premium": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": "TRIA Premium - 100% Slip Ccy", "read_only": True, "format": thousands_format()}),
                    "actual_tria_premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Actual TRIA Premium Override", "format": thousands_format(),"info":"If overriding the premium, enter as 100% GG slip currency"}, async_input=["generate_quote_doc_task"]),
                }),
                "cyber": hx.Structure(children={
                    "include": hx.Bool(mode="input", default=False, async_input=run_schedule_rater_async_tasks(), async_output=[{"task": "copy_primary_deductibles_task","reset": False}], view={"label": "Cyber"}),
                    "include_malicious": hx.Bool(mode="input", default=False, async_input=run_schedule_rater_async_tasks(), async_output=[{"task": "copy_primary_deductibles_task","reset": False}], view={"label": "Ensuing Loss (Malicious)", "info": "Physical damage that results from an unathorized, malicious or criminal cyber act or series of unathorized, malicious or criminal acts.\n\nNOTE: This will not impact technical adequacy metrics."}),
                    "include_affirmative": hx.Bool(mode="input", default=False, async_input=run_schedule_rater_async_tasks(), async_output=[{"task": "copy_primary_deductibles_task","reset": False}], view={"label": "Affirmative", "info": "Cyber losses (typically resulting from computer system-related events) and/or Data Restoration costs (costs to restore or recreate data/programs from backups or previous generations).\n\nNOTE: This will impact technical adequacy metrics."}),
                    "sublimit": hx.Float(mode="input", default=None,async_input=run_schedule_rater_async_tasks(),  optionality="optional", async_output=[{"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "Affirmative Sublimit", "info": "The policy limit will be used if nothing is entered here", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "deductible": hx.Float(mode="input", default=None,async_input=run_schedule_rater_async_tasks(),  optionality="optional", async_output=[{"task": "copy_primary_deductibles_task", "reset": False}],view={"label": "Affirmative Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "ensuing_sublimit": hx.Float(mode="input", default=None,async_input=run_schedule_rater_async_tasks(),  optionality="optional", async_output=[{"task": "copy_primary_deductibles_task", "reset": False}], view={"label": "Ensuing Loss Sublimit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "ensuing_deductible": hx.Float(mode="input", default=None,async_input=run_schedule_rater_async_tasks(),  optionality="optional", async_output=[{"task": "copy_primary_deductibles_task", "reset": False}],view={"label": "Ensuing Loss Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "calculated_premium": hx.Float(mode="output", view={"label": "Tech Cyber Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "actual_premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Charged GG Cyber Premium", "info": "Enter as 100% GG slip currency", "format": {"thousandSeparated": True, "mantissa": 0}}),
                })
            }),
            "other_segmentations": hx.Structure(children={
                "state_summary": adjustment_factor_summary("State Summary", total_col=True),
                }),
            "segmentation_tables": hx.Structure(children={
                "table_selector": hx.Str(mode="input", default="State/Country", view={"label": "Select Risk Factor"}, options=[
                    "State/Country",
                    "Occupancy", 
                    "Construction",
                    "WS Zone",
                    "DTC",
                    "Quake Zone"
                    ]),
                "show_segmentation_tables": hx.Structure(children={
                    "state": hx.Bool(mode="output"),
                    "fire_occupancy": hx.Bool(mode="output"),
                    "fire_construction": hx.Bool(mode="output"),
                    "ws_zone": hx.Bool(mode="output"),
                    "dtc": hx.Bool(mode="output"),
                    "eq_zone": hx.Bool(mode="output"),
                }),
            }),
            # Perils Summary section
            "pre_uw_adjustment": hx.Structure(children=perils_summary_struct()),
            "post_uw_adjustment": hx.Structure(children=perils_summary_struct()),
            "trapped_exposure_rate": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Trapped Exposure Rate", "format": percent_format(mantissa=3)}),
            "trapped_exposure": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Trapped Exposure", "format": thousands_format()}),
            "cat_aop_split": hx.Structure(children={
                "perc_us_wind": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "% US Wind", "format": percent_format(mantissa=0)}),
                "perc_us_quake": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "% US Quake", "format": percent_format(mantissa=0)}),
                "perc_us_aop": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "% US AOP", "format": percent_format(mantissa=0)}),
                "perc_intl_cat": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "% Intl Cat", "format": percent_format(mantissa=0)}),
                "perc_intl_aop": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "% Intl AOP", "format": percent_format(mantissa=0)})
            }),  
            "risk_appetite_summary": hx.Structure(children={
                "us_wind_aal": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "US + Caribbean Wind AAL", "read_only": True, "format": thousands_format()}),
                "us_quake_aal": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "US + Canada Quake AAL", "read_only": True, "format": thousands_format()}),
                "us_all_perils_aal": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "US All Perils AAL", "read_only": True, "format": thousands_format()}),
                "us_wind_sd": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "US + Caribbean SD", "read_only": True, "format": thousands_format()}),
                "us_quake_sd": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "US + Canada Earthquake SD", "read_only": True, "format": thousands_format()}),
                "us_all_perils_sd": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "US All Perils SD", "read_only": True, "format": thousands_format()}),
                "aep_impact_1_in_10": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "1 in 10 AEP Marginal Impact (100%)", "read_only": True, "format": thousands_format()}),
                "oep_impact_1_in_250": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "1 in 250 OEP Marginal Impact (100%)", "read_only": True, "format": thousands_format()}),
                "aep_impact_1_in_10_wrt_line": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "1 in 10 AEP Marginal Impact (Line)", "read_only": True, "format": thousands_format()}),
                "oep_impact_1_in_250_wrt_line": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "1 in 250 OEP Marginal Impact (Line)", "read_only": True, "format": thousands_format()}),
                "oep_impact_1_in_250_cat_premium_ratio": hx.Float(mode="output", view={"label": "1 in 250 OEP Marginal Impact / CAT Premium", "format": thousands_format(mantissa=1)}),
                "intl_wind_aal": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "Intl Wind AAL", "read_only": True, "format": thousands_format()}),
                "intl_quake_aal": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "Intl Quake AAL", "read_only": True, "format": thousands_format()}),
                "intl_all_perils_aal": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "Intl All Perils AAL", "read_only": True, "format": thousands_format()}),
                "intl_wind_sd": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "Intl Wind SD", "read_only": True, "format": thousands_format()}),
                "intl_quake_sd": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "Intl Earthquake SD", "read_only": True, "format": thousands_format()}),
                "intl_all_perils_sd": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "Intl All Perils SD", "read_only": True, "format": thousands_format()}),
            }),
            "simulated_result": hx.Structure(children={
                "us_wind_aal": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"label": "US + Caribbean Wind AAL", "read_only": True, "format": thousands_format()}),
                "us_quake_aal": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"label": "US + Canada quake AAL", "read_only": True, "format": thousands_format()}),
                "us_all_perils_aal": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"label": "US All Perils AAL", "read_only": True, "format": thousands_format()}),
                "us_wind_sd": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"label": "US + Caribbean Wind SD", "read_only": True, "format": thousands_format()}),
                "us_quake_sd": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"label": "US + Canada Earthquake SD", "read_only": True, "format": thousands_format()}),
                "us_all_perils_sd": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"label": "US All Perils SD", "read_only": True, "format": thousands_format()}),
                "aep_impact_1_in_10": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"label": "1 in 10 AEP Marginal Impact (100%)", "read_only": True, "format": thousands_format()}),
                "oep_impact_1_in_250": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"label": "1 in 250 OEP Marginal Impact (100%)", "read_only": True, "format": thousands_format()}),
                "aep_impact_1_in_10_wrt_line": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"label": "1 in 10 AEP Marginal Impact (Line)", "read_only": True, "format": thousands_format()}),
                "oep_impact_1_in_250_wrt_line": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"label": "1 in 250 OEP Marginal Impact (Line)", "read_only": True, "format": thousands_format()}),
                "intl_wind_aal": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"label": "Intl Wind AAL", "read_only": True, "format": thousands_format()}),
                "intl_quake_aal": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"label": "Intl quake AAL", "read_only": True, "format": thousands_format()}),
                "intl_all_perils_aal": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"label": "Intl All Perils AAL", "read_only": True, "format": thousands_format()}),
                "intl_wind_sd": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"label": "Intl Wind SD", "read_only": True, "format": thousands_format()}),
                "intl_quake_sd": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"label": "Intl Earthquake SD", "read_only": True, "format": thousands_format()}),
                "intl_all_perils_sd": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"label": "Intl All Perils SD", "read_only": True, "format": thousands_format()}),
            }),
            "simulated_result_intl_country": hx.List(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], children={
                "country": hx.Str(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"read_only": True,}),
                "aal_ws": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"read_only": True,}),
                "aal_eq": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"], view={"read_only": True,}), 
            }),
            "risk_appetite_summary_intl_country": hx.List(mode="output", async_output=run_schedule_rater_async_tasks(async_input = False), children={
                "country": hx.Str(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": "Country", "read_only": True}),
                "aal_ws": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": "Wind AAL", "format": thousands_format(), "read_only": True}),
                "aal_eq": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": "Quake AAL", "format": thousands_format(), "read_only": True}), 
                "show_ws": hx.Bool(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}), 
                "show_eq": hx.Bool(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}), 
            }),
            "ri_cost": hx.Structure(children={
                "quake_us_ri_cost": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"]),
                "wind_us_ri_cost": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_simulation_task"]),
            }),
            "simulation_output": hx.Structure(children={
                "rds_events": hx.Structure(children={
                    "ca_quake_la": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "CA Quake - Los Angeles", "read_only": True}),
                    "ca_quake_sf": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "CA Quake - San Francisco", "read_only": True}),
                    "nm_quake": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "New Madrid Quake", "read_only": True}),
                    "nm_extreme_stress": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "New Madrid Extreme Stress Event", "read_only": True}),
                    "nw_quake": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "Pacific North West / British Columbia Quake", "read_only": True}),
                    "fl_wind_miami": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "Florida Wind - Miami-Dade", "read_only": True}),
                    "fl_wind_pinellas": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "Florida Wind - Pinellas", "read_only": True}),
                    "us_wind_gulf_of_mexico": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "US Wind Gulf of Mexico", "read_only": True}),
                    "carolinas_wind": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "Carolinas Wind following NE", "read_only": True}),
                    "north_east_wind": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "North East Wind", "read_only": True}),
                }),
                "acc_oep_gu_loss": hx.Structure(children=one_in_x_struct()),
                "pt_oep_loss": hx.Structure(children=one_in_x_struct()),
                "pt_aep_loss": hx.Structure(children=one_in_x_struct())
            })
        })
    }

def location_ded_struct(option_rows):
    '''
    Structure for location deductibles
    Parameters:
        option_rows (list of dict): List of dictionary that specify the argument of each expand_field_with_layer_function
    '''
    return {
        "location_ded": hx.Structure(children={
            **merge_dicts([option_struct(index, option_rows) for index in range(1, MAX_OPTIONS + 1)]),
        })
    }

def option_struct(index, option_rows):
    '''
    Structure of each option for peril decution
    '''
    return {
        f"option_{index}": hx.Structure(children={
            **{row["node_name"]: eval(row["node_struct"]) for row in option_rows}
        })
    }


def perils_summary_struct():
    return {
        "achieved_premium": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Achieved Premium", "format": thousands_format()}),
        "achieved_rate": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Achieved Rate", "format": percent_format(mantissa=3)}),
        "expected_loss": hx.Structure(children={
            "expected_loss": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Expected Loss", "format": thousands_format()}),
            "elr": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "ELR", "format": percent_format(mantissa=1)}),
            "fire": hx.Float(mode="output", view={"label": "Fire Expected Loss", "format": thousands_format()}),
            "cyber": hx.Float(mode="output", view={"label": "Cyber Expected Loss", "format": thousands_format()}),
            "nmp": hx.Float(mode="output", view={"label": "NMP Expected Loss", "format": thousands_format()}),
            "us_cat": hx.Structure(children={
                "us_cat_total": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US Cat Expected Loss Total", "format": thousands_format()}),
                "windstorm_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US + Caribbean WS Expected Loss", "format": thousands_format()}),
                "tornado_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US TN Expected Loss", "format": thousands_format()}),
                "hail_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US HA Expected Loss", "format": thousands_format()}),
                "flood_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US FL Expected Loss", "format": thousands_format()}),
                "earthquake_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US + Canada EQ Expected Loss", "format": thousands_format()}),
                "wildfire_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US WF Expected Loss", "format": thousands_format()}),
            }),
            "intl_cat": hx.Structure(children={
                "intl_cat_total": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl Cat Expected Loss Total", "format": thousands_format()}),
                "windstorm_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl WS Expected Loss", "format": thousands_format()}),
                "tornado_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl TN Expected Loss", "format": thousands_format()}),
                "hail_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl HA Expected Loss", "format": thousands_format()}),
                "flood_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl FL Expected Loss", "format": thousands_format()}),
                "earthquake_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl EQ Expected Loss", "format": thousands_format()}),
                "wildfire_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl WF Expected Loss", "format": thousands_format()}),
            })
        }),
        "benchmark_premium": hx.Structure(children={
            "benchmark_premium": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Benchmark Premium", "format": thousands_format()}),
            "bpi": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "BPI", "format": percent_format(mantissa=1)}),
        }),  
        "net_tech_prem": hx.Structure(children={
            "net_tech_prem_total": hx.Float(mode="output", view={"label": "Net Tech Prem Total", "format": thousands_format()}),
        }),
        "gross_tech_prem": hx.Structure(children={
            "gross_tech_prem_total": hx.Float(mode="output", view={"label": "Gross Tech Prem Total", "format": thousands_format()}),
            "tpi": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "TPI", "format": percent_format(mantissa=1)}),
            "fire": hx.Float(mode="output", view={"label": "Fire Premium", "format": thousands_format()}),
            "cyber": hx.Float(mode="output", view={"label": "Cyber Premium", "format": thousands_format()}),
            "nmp": hx.Float(mode="output", view={"label": "NMP Premium", "format": thousands_format()}),
            "us_cat": hx.Structure(children={
                "us_cat_total": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US Cat Premium Total", "format": thousands_format()}),
                "windstorm_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US + Caribbean WS Premium", "format": thousands_format()}),
                "tornado_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US TN Premium", "format": thousands_format()}),
                "hail_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US HA Premium", "format": thousands_format()}),
                "flood_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US FL Premium", "format": thousands_format()}),
                "earthquake_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US + Canada EQ Premium", "format": thousands_format()}),
                "wildfire_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US WF Premium", "format": thousands_format()}),
            }),
            "intl_cat": hx.Structure(children={
                "intl_cat_total": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl Cat Premium Total", "format": thousands_format()}),
                "windstorm_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl WS Premium", "format": thousands_format()}),
                "tornado_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl TN Premium", "format": thousands_format()}),
                "hail_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl HA Premium", "format": thousands_format()}),
                "flood_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl FL Premium", "format": thousands_format()}),
                "earthquake_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl EQ Premium", "format": thousands_format()}),
                "wildfire_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl WF Premium", "format": thousands_format()}),
            })
        }),
        "gross_tech_prem_rate": hx.Structure(children={
            "gross_tech_prem_rate_total": hx.Float(mode="output", view={"label": "Gross Tech Prem Rate Total", "format": percent_format(mantissa=3)}),
            "fire": hx.Float(mode="output", view={"label": "Fire Rate", "format": percent_format(mantissa=3)}),
            "cyber": hx.Float(mode="output", view={"label": "Cyber Rate", "format": percent_format(mantissa=3)}),
            "nmp": hx.Float(mode="output", view={"label": "NMP Rate", "format": percent_format(mantissa=3)}),
            "us_cat": hx.Structure(children={
                "us_cat_total": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US Cat Prem Rate Total", "format": percent_format(mantissa=3)}),
                "windstorm_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US + Caribbean WS Prem Rate", "format": percent_format(mantissa=3)}),
                "tornado_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US TN Prem Rate", "format": percent_format(mantissa=3)}),
                "hail_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US HA Prem Rate", "format": percent_format(mantissa=3)}),
                "flood_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US FL Prem Rate", "format": percent_format(mantissa=3)}),
                "earthquake_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US + Canada EQ Prem Rate", "format": percent_format(mantissa=3)}),
                "wildfire_us": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "US WF Prem Rate", "format": percent_format(mantissa=3)}),
            }),
            "intl_cat": hx.Structure(children={
                "intl_cat_total": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl Cat Prem Rate Total", "format": percent_format(mantissa=3)}),
                "windstorm_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl WS Prem Rate", "format": percent_format(mantissa=3)}),
                "tornado_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl TN Prem Rate", "format": percent_format(mantissa=3)}),
                "hail_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl HA Prem Rate", "format": percent_format(mantissa=3)}),
                "flood_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl FL Prem Rate", "format": percent_format(mantissa=3)}),
                "earthquake_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl EQ Prem Rate", "format": percent_format(mantissa=3)}),
                "wildfire_intl": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Intl WF Prem Rate", "format": percent_format(mantissa=3)}),
            })
        }),
        "tech_prem_components": hx.Structure(children={
            "coc": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Cost of Capital", "format": thousands_format()}),
            "direct_expenses": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Direct Expenses", "format": thousands_format()}),
            "indirect_expenses": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Indirect Expenses", "format": thousands_format()}),
            "lae": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Loss Adjustment Expenses", "format": thousands_format()}),
            "ri": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "RI Costs", "format": thousands_format()}),
            "sd": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "SD Loading", "format": thousands_format()}),
            "investment_income": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True), view={"label": "Investment Income", "format": thousands_format()})
        }) 
    }


def adjustment_factor_summary(label, total_col=False):
    return hx.List(mode="output", children={
                        "name": hx.Str(mode="output", view={"label": label}),
                        "num_locations": hx.Int(mode="output", view={"label": "No of\nLocs", "chart": {"series_type": "line", "series_axis": "secondary"}}),
                        "tiv": hx.Int(mode="output", view={"label": "TIV"}),
                        **rating_metrics(group=False, total_col=total_col)
                    })


def top_20_locations_summary(risk_factor_func, rating_metric_func):
    return hx.List(mode="output", children={
        "country": hx.Str(mode="output", view={"label": "Country", "group": "Location Factors"}),
        "state": hx.Str(mode="output", view={"label": "State", "group": "Location Factors"}),
        "county": hx.Str(mode="output", view={"label": "County", "group": "Location Factors"}),
        "zip": hx.Str(mode="output", view={"label": "Zip", "group": "Location Factors"}),
        "tiv_buildings": hx.Float(mode="output", view={"label": "Buildings", "format": thousands_format(), "group": "Exposure Factors"}),
        "tiv_contents_total": hx.Float(mode="output", view={"label": "Contents", "format": thousands_format(), "group": "Exposure Factors"}),
        "tiv_bi": hx.Float(mode="output", view={"label": "BI", "format": thousands_format(), "group": "Exposure Factors"}),
        "tiv_total": hx.Float(mode="output", view={"label": "Total", "format": thousands_format(), "group": "Exposure Factors"}),
        "itv": hx.Float(mode="output", view={"label": "ITV", "format": thousands_format(mantissa=2), "group": "Exposure Factors"}),
        "base_rate": hx.Float(mode="output", view={"label": "Base Rate", "format": percent_format(mantissa=3), "info":"Note this is a loss rate"}),
        **risk_factor_func(),
        **rating_metric_func()
    })

def crit_cat_zone_summary(label):
    return hx.List(mode="output", async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], children={
        "cat_zone": hx.Str(mode="input", optionality="optional", default=None, async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": label, "read_only": True}),
        "tiv": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "Ground Up TIV\n(USD)", "format": thousands_format(), "read_only": True}),
        "exposed_limit": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "Exposed Limit\n(USD)", "format": thousands_format(), "read_only": True}),
        "exposed_limit_threshold": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "Exposed Limit\nThreshold (USD)", "format": thousands_format(), "read_only": True}),
        "within_threshold": hx.Str(mode="input", optionality="optional", default=None, async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "Within Threshold?", "read_only": True}),
        "flood_zone_av_exposed_limit": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "Flood Zone A & V\nExposed Limit (USD)", "format": thousands_format(), "read_only": True}),
    })

def crit_cat_zone_summary_headline(label):
    return hx.List(mode="output", async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], children={
        "cat_zone": hx.Str(mode="input", optionality="optional", default=None, async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": label, "read_only": True}),
        "exposed_limit_threshold": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "Exposed Limit\nThreshold (USD)", "format": thousands_format(), "read_only": True}),
        "within_threshold": hx.Str(mode="input", optionality="optional", default=None, async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "Within Threshold?", "read_only": True}),
    })

def gate_appetite_summary(label):
    return hx.List(mode="output", async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], children={
        "gate": hx.Str(mode="input", optionality="optional", default=None, async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": label, "read_only": True}),
        "tiv": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "Ground Up TIV\n(USD)", "format": thousands_format(), "read_only": True}),
        "exposed_limit": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "Exposed Limit\n(USD)", "format": thousands_format(), "read_only": True}),
        "flood_zone_av_exposed_limit": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_schedule_rater_task", {"task": "remove_experience_adjustment_task", "reset": False}, {"task": "save_case_pricing_results_task", "reset": False}], view={"label": "Flood Zone A & V\nExposed Limit (USD)", "format": thousands_format(), "read_only": True}),
    })

def fire_risk_factors(group=True):
    return {
        "occupancy": hx.Float(mode="output", view={"label": "Occupancy", "format": percent_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "construction": hx.Float(mode="output", view={"label": "Construction", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "pc_code": hx.Float(mode="output", view={"label": "PC Code", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "sprinkler": hx.Float(mode="output", view={"label": "Sprinkler", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "bi_waiting_period": hx.Float(mode="output", view={"label": "BI Waiting\nPeriod", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "bi_indemnity_period": hx.Float(mode="output", view={"label": "BI Indemnity\nPeriod", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "cbi": hx.Float(mode="output", view={"label": "CBI", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "mexican_fonden": hx.Float(mode="output", view={"label": "Mexican\nFonden", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "fire_size_discount": hx.Float(mode="output", view={"label": "Size Discount", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "total_modifier_impact": hx.Float(mode="output", view={"label": "Total\nModifier\nImpact", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
    }


def windstorm_risk_factors(group=True):
    return {
        "occupancy": hx.Float(mode="output", view={"label": "Occupancy", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "construction": hx.Float(mode="output", view={"label": "Construction", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "year_built": hx.Float(mode="output", view={"label": "Year Built", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "floor_area": hx.Float(mode="output", view={"label": "Floor Area", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "num_of_floors": hx.Float(mode="output", view={"label": "Number of\nFloors", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "roof_age": hx.Float(mode="output", view={"label": "Roof Age", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "roof_covering": hx.Float(mode="output", view={"label": "Roof\nCovering", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "roof_geometry": hx.Float(mode="output", view={"label": "Roof\nGeometry", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "construction_quality": hx.Float(mode="output", view={"label": "Construction\nQuality", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "roof_anchor": hx.Float(mode="output", view={"label": "Roof Anchor", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "roof_bracing": hx.Float(mode="output", view={"label": "Roof\nEquipment\nHurricane\nBracing", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "roof_cladding": hx.Float(mode="output", view={"label": "Cladding\nType", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "frame_connection": hx.Float(mode="output", view={"label": "Frame\nFoundation\nConnection", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "storm_surge": hx.Float(mode="output", view={"label": "Storm\nSurge", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "catnet_score": hx.Float(mode="output", view={"label": "CatNet\nScore", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "total_modifier_impact": hx.Float(mode="output", view={"label": "Total\nModifier\nImpact", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
    }


def earthquake_risk_factors(group=True):
    return {
        "occupancy": hx.Float(mode="output", view={"label": "Occupancy", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "construction": hx.Float(mode="output", view={"label": "Construction", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "year_built": hx.Float(mode="output", view={"label": "Year Built", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "num_of_floors": hx.Float(mode="output", view={"label": "Number of\nFloors", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "construction_quality": hx.Float(mode="output", view={"label": "Construction\nQuality", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "plan_irregularity": hx.Float(mode="output", view={"label": "Plan\nIrregularity", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "soft_story": hx.Float(mode="output", view={"label": "Soft Story", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "vertical_irregularity": hx.Float(mode="output", view={"label": "Vertical\nIrregularity", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "ornamentation": hx.Float(mode="output", view={"label": "Ornamentation", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "equipment_bracing": hx.Float(mode="output", view={"label": "Equipment\nEQ Bracing", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "equipment_maintenance": hx.Float(mode="output", view={"label": "Equipment\nSupport\nMaintenance", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "pounding": hx.Float(mode="output", view={"label": "Pounding", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "catnet_score": hx.Float(mode="output", view={"label": "CatNet\nScore - Int\nOnly", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "total_modifier_impact": hx.Float(mode="output", view={"label": "Total\nModifier\nImpact", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
    }

def flood_risk_factors(group=True):
    return {
        "construction": hx.Float(mode="output", view={"label": "Construction", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "num_of_floors": hx.Float(mode="output", view={"label": "Number of\nFloors", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "basement": hx.Float(mode="output", view={"label": "Basement", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "elevation": hx.Float(mode="output", view={"label": "Elevation", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "katrisk_catnet_score": hx.Float(mode="output", view={"label": "KatRisk/Cat\nNet Score", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "size_discount": hx.Float(mode="output", view={"label": "Size Discount", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "total_modifier_impact": hx.Float(mode="output", view={"label": "Total\nModifier\nImpact", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
    }

def wildfire_risk_factors(group=True):
    return {
        "occupancy": hx.Float(mode="output", view={"label": "Occupancy", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "construction": hx.Float(mode="output", view={"label": "Construction", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "pc_code": hx.Float(mode="output", view={"label": "PC Code", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "catnet_score": hx.Float(mode="output", view={"label": "CatNet Score", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "size_discount": hx.Float(mode="output", view={"label": "Size Discount", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "bi_waiting_period": hx.Float(mode="output", view={"label": "BI Waiting Period", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "total_modifier_impact": hx.Float(mode="output", view={"label": "Total Modifier Impact", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
    }

def scs_risk_factors(group=True):
    return {
        "occupancy": hx.Float(mode="output", view={"label": "Occupancy", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "construction": hx.Float(mode="output", view={"label": "Construction", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "year_built": hx.Float(mode="output", view={"label": "Year Built", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "floor_area": hx.Float(mode="output", view={"label": "Floor Area", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "roof_age": hx.Float(mode="output", view={"label": "Roof Age", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "roof_covering": hx.Float(mode="output", view={"label": "Roof Covering", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "roof_geometry": hx.Float(mode="output", view={"label": "Roof Geometry", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "catnet_score": hx.Float(mode="output", view={"label": "CatNet Score - Int Only", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "size_discount": hx.Float(mode="output", view={"label": "Size Discount", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
        "total_modifier_impact": hx.Float(mode="output", view={"label": "Total Modifier Impact", "format": thousands_format(mantissa=2), "group": ("Risk Factors" if group else None)}),
    }

def rating_metrics(group=True, total_col=False):
    if total_col:
        return {
        "gu_tech_rate": hx.Float(mode="output", view={"label": "GU\nTech Rate", "format": percent_format(mantissa=3), "group": ("Rating Metrics" if group else None), "info":"Note this is a premium rate"}),
        "total_gu_tech_rate": hx.Float(mode="output", view={"label": "Total GU Tech Rate", "format": percent_format(mantissa=3), "group": ("Rating Metrics" if group else None)}),
        "worth": hx.Float(mode="output", view={"label": "Worth", "format": percent_format(mantissa=3), "group": ("Rating Metrics" if group else None)}),
        "tech_rate": hx.Float(mode="output", view={"label": "Tech Rate", "format": percent_format(mantissa=3), "group": ("Rating Metrics" if group else None)}),
        "uw_adj_tech_rate": hx.Float(mode="output", view={"label": "UW Adj\nTech Rate", "format": percent_format(mantissa=3), "group": ("Rating Metrics" if group else None)}),
        "uw_adj_tech_prem": hx.Float(mode="output", view={"label": "UW Adj\nTech Premium" ,"format": thousands_format(mantissa=0), "group": ("Rating Metrics" if group else None)}),
        "tech_prem": hx.Float(mode="output", view={"label": "Tech Premium", "format": thousands_format(mantissa=0), "group": ("Rating Metrics" if group else None)}),
        "gu_prem": hx.Float(mode="output", view={"label": "GU Tech Premium", "format": thousands_format(mantissa=0), "group": ("Rating Metrics" if group else None)}),
        "gu_loss": hx.Float(mode="output", view={"label": "GU Loss", "format": thousands_format(mantissa=0), "group": ("Rating Metrics" if group else None)}),
        "itv": hx.Float(mode="output", view={"label": "ITV", "format": thousands_format(mantissa=0), "group": ("Rating Metrics" if group else None)})
    }
    else:
        return {
        "gu_tech_rate": hx.Float(mode="output", view={"label": "GU\nTech Rate", "format": percent_format(mantissa=3), "group": ("Rating Metrics" if group else None), "info":"Note this is a premium rate"}),
        "worth": hx.Float(mode="output", view={"label": "Worth", "format": percent_format(mantissa=1), "group": ("Rating Metrics" if group else None)}),
        "tech_rate": hx.Float(mode="output", view={"label": "Tech Rate", "format": percent_format(mantissa=3), "group": ("Rating Metrics" if group else None)}),
        "uw_adj_tech_rate": hx.Float(mode="output", view={"label": "UW Adj\nTech Rate", "format": percent_format(mantissa=3), "group": ("Rating Metrics" if group else None)}),
        "uw_adj_tech_prem": hx.Float(mode="output", view={"label": "UW Adj\nTech Premium" ,"format": thousands_format(mantissa=0), "group": ("Rating Metrics" if group else None)}),
        "tech_prem": hx.Float(mode="output", view={"label": "Tech Premium" ,"format": thousands_format(mantissa=0), "group": ("Rating Metrics" if group else None)}),
        "gu_prem": hx.Float(mode="output", view={"label": "GU Tech Premium" ,"format": thousands_format(mantissa=0), "group": ("Rating Metrics" if group else None)}),
        "gu_loss": hx.Float(mode="output", view={"label": "GU Loss" ,"format": thousands_format(mantissa=0), "group": ("Rating Metrics" if group else None)}),
        "itv": hx.Float(mode="output", view={"label": "ITV" ,"format": thousands_format(mantissa=0), "group": ("Rating Metrics" if group else None)})
    }


def one_in_x_struct():
    return {
        "one_in_10000": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "10000", "read_only": True}),
        "one_in_5000": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "5000", "read_only": True}),
        "one_in_1000": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "1000", "read_only": True}),
        "one_in_500": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "500", "read_only": True}),
        "one_in_250": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "250", "read_only": True}),
        "one_in_200": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "200", "read_only": True}),
        "one_in_150": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "150", "read_only": True}),
        "one_in_100": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "100", "read_only": True}),
        "one_in_50": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "50", "read_only": True}),
        "one_in_30": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "30", "read_only": True}),
        "one_in_10": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "10", "read_only": True}),
        "one_in_2": hx.Float(mode="input", optionality="optional", default=None, async_output=["run_simulation_task"], view={"label": "2", "read_only": True}),
    }



def case_pricing_perils_dict(label):
    return {
        "fire": f"Fire {label}",
        "us_ws": f"US WS {label}",
        "us_tn": f"US TN {label}",
        "us_ha": f"US HA {label}",
        "us_scs": f"US SCS {label}",
        "us_fl": f"US FL {label}",
        "us_eq": f"US EQ {label}",
        "us_wf": f"US WF {label}",
        "intl_ws": f"Intl WS {label}",
        "intl_tn": f"Intl TN {label}",
        "intl_ha": f"Intl HA {label}",
        "intl_scs": f"Intl SCS {label}",
        "intl_fl": f"Intl FL {label}",
        "intl_eq": f"Intl EQ {label}",
        "intl_wf": f"Intl WF {label}"
    }


def case_pricing_inputs():
    case_pricing_el_dict = {}
    for key, value in case_pricing_perils_dict("Expected Loss").items():
        case_pricing_el_dict[key] = hx.Float(mode="input", async_input=["save_case_pricing_results_task", "case_pricing_calc_tech_premium_task"], default=None, optionality="optional", view={"label": value, "format":thousands_format()})
    
    case_pricing_tech_dict = {}
    for key, value in case_pricing_perils_dict("Tech Premium").items():
        case_pricing_tech_dict[key] = hx.Float(mode="input", async_input=["save_case_pricing_results_task"], async_output=["case_pricing_calc_tech_premium_task"], default=None, optionality="optional", view={"label": value, "format":thousands_format()})
    
    return {
        "technical_premium": hx.Float(mode="output", async_input=["save_case_pricing_results_task"], view={"label": "Gross Technical Premium (100%)", "format": thousands_format()}),
        "benchmark_premium": hx.Float(mode="output", async_input=["save_case_pricing_results_task"], view={"label": "Gross Benchmark Premium (100%)", "format": thousands_format()}),
        "tpi": hx.Float(mode="output", async_input=["save_case_pricing_results_task"], view={"label": "TPI", "format": percent_format()}),
        "bpi": hx.Float(mode="output", async_input=["save_case_pricing_results_task"], view={"label": "BPI", "format": percent_format()}),
        "elr": hx.Float(mode="output", async_input=["save_case_pricing_results_task"], view={"label": "ELR", "format": percent_format()}),
        
        "total_exp_loss": hx.Float(mode="output", async_input=["save_case_pricing_results_task", "case_pricing_calc_tech_premium_task"], view={"label": "Total Expected Loss", "format":thousands_format()}),
        "us_exp_loss": hx.Float(mode="output", async_input=["save_case_pricing_results_task"], view={"label": "US Expected Loss Total", "format":thousands_format()}),
        "intl_exp_loss": hx.Float(mode="output", async_input=["save_case_pricing_results_task"], view={"label": "Intl Expected Loss Total", "format":thousands_format()}),
        "us_tech_prem": hx.Float(mode="output", async_input=["save_case_pricing_results_task"], view={"label": "US Tech Premium Total", "format":thousands_format()}),
        "intl_tech_prem": hx.Float(mode="output", async_input=["save_case_pricing_results_task"], view={"label": "Intl Tech Premium Total", "format":thousands_format()}),
        
        "risk_adj_rate_change": hx.Float(mode="input",default=None, optionality="optional", async_input=["save_case_pricing_results_task"], view={"label": "Risk Adjusted Rate Change", "format": percent_format(2)}),
        "aep_impact_1_in_10": hx.Float(mode="input",default=None, optionality="optional", async_input=["save_case_pricing_results_task"], view={"label": "1 in 10 AEP Marginal Impact", "format":thousands_format()}),
        "oep_impact_1_in_250": hx.Float(mode="input",default=None, optionality="optional", async_input=["save_case_pricing_results_task", "case_pricing_calc_tech_premium_task"], view={"label": "1 in 250 OEP Marginal Impact", "format":thousands_format()}),
        "nmp_premium": hx.Float(mode="input", default=None, optionality="optional", async_input=["save_case_pricing_results_task"], async_output=["case_pricing_calc_tech_premium_task"], view={"label": "NMP Premium", "format":thousands_format()}),
        
        "tp_breakdown": hx.Structure(children={
            "coc": hx.Float(mode="input", default=None, optionality="optional", async_input=["save_case_pricing_results_task"], async_output=["case_pricing_calc_tech_premium_task"], view={"label": "TP Cost of Capital", "format":thousands_format()}),
            "dir_exp": hx.Float(mode="input", default=None, optionality="optional", async_input=["save_case_pricing_results_task"], async_output=["case_pricing_calc_tech_premium_task"], view={"label": "TP Direct Expenses", "format":thousands_format()}),
            "ind_exp": hx.Float(mode="input", default=None, optionality="optional", async_input=["save_case_pricing_results_task"], async_output=["case_pricing_calc_tech_premium_task"], view={"label": "TP Indirect Expenses", "format":thousands_format()}),
            "sd_loading": hx.Float(mode="input", default=None, optionality="optional", async_input=["save_case_pricing_results_task"], async_output=["case_pricing_calc_tech_premium_task"], view={"label": "TP SD Loading", "format":thousands_format()}),
            "inv_ret": hx.Float(mode="input", default=None, optionality="optional", async_input=["save_case_pricing_results_task"], async_output=["case_pricing_calc_tech_premium_task"], view={"label": "TP Investment Return", "format":thousands_format()}),
            "lae": hx.Float(mode="input", default=None, optionality="optional", async_input=["save_case_pricing_results_task"], async_output=["case_pricing_calc_tech_premium_task"], view={"label": "TP Loss Adjustment Expenses", "format":thousands_format()}),
            "ri_cost": hx.Float(mode="input", default=None, optionality="optional", async_input=["save_case_pricing_results_task", "case_pricing_calc_tech_premium_task"], view={"label": "RI Cost", "format":thousands_format()}),
            
        }),
        "expected_loss": hx.Structure(children=case_pricing_el_dict),
        "tech_premium": hx.Structure(children=case_pricing_tech_dict)
    }
    