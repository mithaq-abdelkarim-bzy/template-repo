import hx_data_schema as hx
from data_schema.utilities import thousands_format, set_node_properties, run_schedule_rater_async_tasks
from data_schema.dropdown_list import schedule_peril_covered_list, schedule_soil_type_list, schedule_liquefaction_list, \
        schedule_landslide_list, schedule_eq_const_qual_list, schedule_plan_irregularity_list, schedule_soft_story_list, \
        schedule_vertical_irregularity_list, schedule_ornamentation_list, schedule_equipment_eq_bracing_list, \
        schedule_equipment_support_maintenance_list, schedule_pounding_list, schedule_ws_const_qual_list, schedule_roof_anchor_list,    \
        schedule_roof_equip_hurricane_bracing_list, schedule_cladding_type_list, schedule_frame_foundation_connection_list, \
        schedule_river_flood_zone_code, schedule_river_flood_zone_schema, \
        schedule_surge_flood_label, schedule_flood_rank_text, \
        schedule_flood_label

CONSTR_CODE_MAX = 6
PC_CODE_MAX = 10

def schedule():
    '''
    Data schema for schedule page
    '''
    schedule_schema = hx.Structure(children={
            "debug": hx.Str(mode="input", optionality="optional", default=None, async_output=["run_simulation_task", "load_into_debug_task"], view={"read_only": True}),
            "schedule_warnings": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Warnings/Messages", "read_only": True}, async_output=["run_schedule_rater_task", "save_case_pricing_results_task"]),
            "tiv_buildings_label": hx.Str(mode="input", default="Buildings", async_output=['run_schedule_rater_task', 'save_case_pricing_results_task', {"task": "remove_experience_adjustment_task", "reset": False}]),
            "tiv_contents_label": hx.Str(mode="input", default="Contents", async_output=['run_schedule_rater_task', 'save_case_pricing_results_task', {"task": "remove_experience_adjustment_task", "reset": False}]),
            "tiv_other_label": hx.Str(mode="input", default="Other", async_output=['run_schedule_rater_task', 'save_case_pricing_results_task', {"task": "remove_experience_adjustment_task", "reset": False}]),
            "tiv_bi_label": hx.Str(mode="input", default="BI", async_output=['run_schedule_rater_task', 'save_case_pricing_results_task', {"task": "remove_experience_adjustment_task", "reset": False}]),
            "tiv_total_label": hx.Str(mode="input", default="Total", async_output=['run_schedule_rater_task', 'save_case_pricing_results_task', {"task": "remove_experience_adjustment_task", "reset": False}]),
            "tiv_total_outside_table_label": hx.Str(mode="input", default="Total TIV in Schedule", async_output=['run_schedule_rater_task', 'save_case_pricing_results_task', {"task": "remove_experience_adjustment_task", "reset": False}]),
            "spatial_key_file": hx.File(mode="output", file_name="spatial_key.csv", async_input=run_schedule_rater_async_tasks(async_input = True), async_output=["run_spatialkey_task"], view={"label": "Spatial Key Result"}),
            "run_rater_progress_information": hx.Str(mode="output", async_output=["run_schedule_rater_task", 'save_case_pricing_results_task', {"task": "remove_experience_adjustment_task", "reset": False}]),
            "large_schedule_workflow": hx.Structure(children={
                "large_schedule_em_file": hx.File(mode="output", file_name="em_schedule.csv", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task", "run_spatialkey_task", "push_file_to_temp_task"], async_output=["pull_in_exposure_management_data_task", "load_from_schedule_task"], view={"label": "Large Schedule EM"}),
                "schedule_file": hx.File(mode="input", file_extension=["csv"], async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_spatialkey_task", "confirm_override_task", "run_simulation_task"], view={"label": "Upload schedule files"}),
                "schedule_output_file": hx.File(mode="output", file_name="output.feather", async_input=["push_df_to_temp_task"], async_output=run_schedule_rater_async_tasks(async_input = True) + ["load_into_debug_task"], view={"label": "Output schedule calculation file"}),
                "spatial_key_updated": hx.Bool(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True),async_output=["pull_in_exposure_management_data_task", "confirm_override_task", "run_spatialkey_task"], view={"read_only": True}),
                "simulation_updated": hx.Bool(mode="input", optionality="optional", default=None, async_output=["pull_in_exposure_management_data_task", "run_simulation_task"], view={"read_only": True}),
                "run_rater_information": hx.Str(mode="output"),
                "load_from_schedule_file": hx.Bool(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_spatialkey_task", "run_simulation_task"], async_output=["pull_in_exposure_management_data_task", "confirm_override_task"], view={"read_only": True}),
                "load_from_em_database": hx.Bool(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_spatialkey_task", "run_simulation_task"], async_output=["pull_in_exposure_management_data_task", "confirm_override_task", "load_from_schedule_task"], view={"read_only": True}),
                "num_of_locations": hx.Int(mode="input", optionality="optional", default=None, async_output=["pull_in_exposure_management_data_task", "confirm_override_task"], view={"read_only": True})
            }),
            "small_schedule_workflow": hx.Structure(children={
                "spatial_key_hash": hx.Str(mode="input", optionality="optional", default=None, async_output=["run_spatialkey_task"], view={"read_only": True}),
                "spatial_key_updated": hx.Bool(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True)),
                "simulation_updated": hx.Bool(mode="input", optionality="optional", default=None, async_output=["pull_in_exposure_management_data_task", "run_simulation_task"], view={"read_only": True}),
                "run_rater_information": hx.Str(mode="output"),                
            }),
            "schedule_table": hx.List(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True) + ["generate_quote_doc_task", "run_spatialkey_task", "run_simulation_task", "produce_heatmap_task", "produce_climate_map_task"], async_output=["pull_in_exposure_management_data_task"], children={
                # General field
                "loc_id": hx.Str(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["produce_heatmap_task", "produce_climate_map_task", "load_from_schedule_task", "generate_climate_doc_task"], view={"label": "LocID", "group": "Identifiers"}, async_output=["pull_in_exposure_management_data_task"]),
                "broker_loc_id": hx.Str(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "BrokerLocID", "group": "Identifiers"}, async_output=["pull_in_exposure_management_data_task"]),
                "broker_subloc_id": hx.Str(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "BrokerSubLocID", "group": "Identifiers"}, async_output=["pull_in_exposure_management_data_task"]),
                "fire_deductible": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Fire\nDeductible", "group": "General", "format": thousands_format()}, async_output=["pull_in_exposure_management_data_task"]),
                
                "fire_covered": hx.Str(mode="input", options=schedule_peril_covered_list, default_index=0, async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Fire Covered", "group": "General"}, async_output=["pull_in_exposure_management_data_task"]),
                "eq_covered": hx.Str(mode="input", options=schedule_peril_covered_list, default_index=0, async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "EQ Covered", "group": "General"}, async_output=["pull_in_exposure_management_data_task"]),
                "ws_covered": hx.Str(mode="input", options=schedule_peril_covered_list, default_index=0, async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "WS Covered", "group": "General"}, async_output=["pull_in_exposure_management_data_task"]),
                "fl_covered": hx.Str(mode="input", options=schedule_peril_covered_list, default_index=0, async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "FL Covered", "group": "General"}, async_output=["pull_in_exposure_management_data_task"]),
                "scs_covered": hx.Str(mode="input", options=schedule_peril_covered_list, default_index=0, async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "SCS Covered", "group": "General"}, async_output=["pull_in_exposure_management_data_task"]),
                "wf_covered": hx.Str(mode="input", options=schedule_peril_covered_list, default_index=0, async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "WF Covered", "group": "General"}, async_output=["pull_in_exposure_management_data_task"]),
                # Address field
                "address_dropdown": hx.Structure(view={"linked_options_selector": "hierarchical"}, linked_options_table="address_table", linked_options_columns=["Country", "State", "County", "City"], linked_default_index=0, children={
                    "country": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task", "produce_heatmap_task", "produce_climate_map_task","generate_climate_doc_task","load_from_schedule_task"], view={"label": "Country", "group": "Address"}, async_output=["pull_in_exposure_management_data_task"]),
                    "state": hx.Str(mode="input", async_input=["produce_heatmap_task", "produce_climate_map_task", "generate_climate_doc_task","run_spatialkey_task", "load_from_schedule_task"], view={"label": "State", "group": "Address"}, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task", "pull_in_exposure_management_data_task"]),
                    "county": hx.Str(mode="input", async_input=["produce_heatmap_task", "produce_climate_map_task", "generate_climate_doc_task", "run_spatialkey_task", "load_from_schedule_task"], view={"label": "County", "group": "Address"}, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task", "pull_in_exposure_management_data_task"]),
                    "city": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True) + ["produce_heatmap_task", "produce_climate_map_task", "generate_climate_doc_task", "load_from_schedule_task"], view={"label": "City", "group": "Address"}, async_output=["pull_in_exposure_management_data_task"])
                }),
                "property_description": hx.Str(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Property Description", "group": "Address"}, async_output=["pull_in_exposure_management_data_task"]),
                "street_name": hx.Str(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["produce_heatmap_task", "produce_climate_map_task", "generate_climate_doc_task", "load_from_schedule_task"], view={"label": "Street Name", "group": "Address"}, async_output=["pull_in_exposure_management_data_task"]),
                "zip": hx.Str(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task", "load_from_schedule_task", "produce_climate_map_task", "generate_climate_doc_task"], view={"label": "Zip", "group": "Address"}, async_output=["pull_in_exposure_management_data_task", {"task": "run_spatialkey_task", "reset": False}]),
                "latitude": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["produce_heatmap_task", "produce_climate_map_task", "generate_climate_doc_task", "load_from_schedule_task"], async_output=["pull_in_exposure_management_data_task", {"task": "run_spatialkey_task", "reset": False}], view={"label": "Latitude", "format": thousands_format(mantissa=6), "group": "Address"}, validation={"min_value": -90, "max_value": 90}),
                "longitude": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["produce_heatmap_task", "produce_climate_map_task", "generate_climate_doc_task", "load_from_schedule_task"], async_output=["pull_in_exposure_management_data_task", {"task": "run_spatialkey_task", "reset": False}], view={"label": "Longitude", "format": thousands_format(mantissa=6), "group": "Address"}, validation={"min_value": -180, "max_value": 180}),
                
                # TIV - Risk Currency field
                "currency": hx.Str(mode="input", optionality="optional", options_table="currency", options_column="currency", async_input=run_schedule_rater_async_tasks(async_input = True) + ["run_simulation_task", "load_from_schedule_task"], default="USD", view={"label": "Currency", "group": "Insured Values"}, async_output=["pull_in_exposure_management_data_task"]),
                "tiv_buildings": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task", "run_simulation_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Buildings", "group": "Insured Values", "format": thousands_format()}),
                "tiv_contents": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task", "run_simulation_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Contents", "group": "Insured Values", "format": thousands_format()}),
                "tiv_other": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task", "run_simulation_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Other", "group": "Insured Values", "format": thousands_format()}),
                "tiv_bi": hx.Float(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task", "run_simulation_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "BI", "group": "Insured Values", "format": thousands_format()}),
                "tiv_total": hx.Float(mode="output", async_input=run_schedule_rater_async_tasks(async_input = True) + ["generate_quote_doc_task", "produce_heatmap_task", "produce_climate_map_task", "generate_climate_doc_task", "load_from_schedule_task"], view={"label": "Total", "group": "Insured Values", "format": thousands_format()}),

                # Construction field
                "constr_code": hx.Int(mode="input", default=None, optionality="optional", options=[i for i in range(0, CONSTR_CODE_MAX + 1)], async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Modelled\nConstruction\nCode", "group": "Construction"}, async_output=["pull_in_exposure_management_data_task"]),
                "raw_constr_code": hx.Str(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Raw Construction\nCode\n(Info Only)", "group": "Construction"}, async_output=["pull_in_exposure_management_data_task"]),
                "constr_description": hx.Str(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Constr\nDescription\n(Info Only)", "group": "Construction"}, async_output=["pull_in_exposure_management_data_task"]),
                "num_buildings": hx.Int(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Num\nBuildings", "group": "Construction"}, async_output=["pull_in_exposure_management_data_task"]),
                "num_stories": hx.Int(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Num\nStories", "group": "Construction"}, async_output=["pull_in_exposure_management_data_task"]),
                "year_built": hx.Int(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Year\nBuilt", "group": "Construction", "format": {"thousandSeparated": False}}, async_output=["pull_in_exposure_management_data_task"]),
                "year_updated": hx.Int(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Year\nUpdated", "group": "Construction", "format": {"thousandSeparated": False}}, async_output=["pull_in_exposure_management_data_task"]),
                "industry_occupancy_dropdown": hx.Structure(view={"linked_options_selector": "flat"}, linked_options_table="non_cat_base_rates_live_dropdown", linked_options_columns=["Industry", "Occupancy"], linked_default_index=0, children={
                    "industry": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Industry", "group": "Occupancy"}, async_output=["pull_in_exposure_management_data_task", {"task":"run_schedule_rater_task", "reset": False}, {"task":"save_case_pricing_results_task", "reset": False}]),
                    "occupancy": hx.Str(mode="input", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Occupancy", "group": "Occupancy"}, async_output=["pull_in_exposure_management_data_task", {"task":"run_schedule_rater_task", "reset": False}, {"task":"save_case_pricing_results_task", "reset": False}]),
                }),
                "broker_occu_desc": hx.Str(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Broker\nOccupancy Desc\n(Info Only)", "group": "Occupancy"}, async_output=["pull_in_exposure_management_data_task"]),
                "rms_occupancy": hx.Str(mode="input", default=None, optionality="optional", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "RMS Occupancy\n(Info Only)", "group": "Occupancy"}, async_output=["pull_in_exposure_management_data_task"]),
                # Peril Specific field
                "pc_code": hx.Int(mode="input", default=None, optionality="optional", options=[i for i in range(0, PC_CODE_MAX + 1)], async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "PC Code", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "sprinkler": hx.Str(mode="input", default=None, optionality="optional", options_table="sprinklers", options_column="Sprinklers", async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Sprinkler", "group": "Construction"}, async_output=["pull_in_exposure_management_data_task"]),
                "year_cov_last_replaced": hx.Int(mode="input", default=None, optionality="optional",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Year Roof\nCovering Last\nReplaced", "group": "Peril Specific", "format": {"thousandSeparated": False}}, async_output=["pull_in_exposure_management_data_task"]),
                "roof_age": hx.Str(mode="input", default=None, optionality="optional", options_table="roof_age", options_column="Age",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Roof Age", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "floor_area": hx.Float(mode="input", default=None, optionality="optional",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Floor Area", "group": "Peril Specific", "format": thousands_format()}, async_output=["pull_in_exposure_management_data_task"]),
                "distance_from_coast": hx.Float(mode="input", default=None, optionality="optional",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Distance From\nCoast - miles", "group": "Peril Specific", "format": thousands_format(mantissa=2)}, async_output=["pull_in_exposure_management_data_task"]),
                "roof_covering": hx.Str(mode="input", default=None, optionality="optional", options_table="roof_covering", options_column="Covering",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Roof Covering", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "roof_geometry": hx.Str(mode="input", default=None, optionality="optional", options_table="roof_geometry", options_column="Geometry",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Roof Geometry", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "ws_tier": hx.Int(mode="output",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "WS Tier", "group": "Risk Grouping - For Info Only"}),
                "wf_tier": hx.Int(mode="output",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "WF Tier", "group": "Risk Grouping - For Info Only"}),
                "ws_gate": hx.Str(mode="output",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "WS Gate", "group": "Risk Grouping - For Info Only"}),
                "eq_gate": hx.Str(mode="output",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "EQ Gate", "group": "Risk Grouping - For Info Only"}),
                "eq_crit_cat_zone": hx.Str(mode="input", default=None, optionality="optional",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], async_output=["run_spatialkey_task"], view={"label": "EQ CAT Zone", "group": "Risk Grouping - For Info Only","read_only": True}),
                "ws_crit_cat_zone": hx.Str(mode="input", default=None, optionality="optional",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], async_output=["run_spatialkey_task"], view={"label": "WS CAT Zone", "group": "Risk Grouping - For Info Only","read_only": True}),
                "cresta_zone": hx.Str(mode="output",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Cresta Zone", "group": "Risk Grouping - For Info Only"}),
                "soil_type": hx.Str(mode="input", default=None, optionality="optional", options=schedule_soil_type_list,  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Soil Type", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "liquefaction": hx.Str(mode="input", default=None, optionality="optional", options=schedule_liquefaction_list,  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Liquefaction", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "landslide": hx.Str(mode="input", default=None, optionality="optional", options=schedule_landslide_list,  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Landslide", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "floodzone": hx.Str(mode="input", default=None, optionality="optional", options_table="fl_tiers", options_column="Zone",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "FloodZone", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "other_floodzone": hx.Str(mode="input", default=None, optionality="optional",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Other FloodZone", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "basement": hx.Str(mode="input", default=None, optionality="optional", options_table="basement", options_column="Basement",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Basement", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "building_elevation": hx.Float(mode="input", default=None, optionality="optional",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Building\nElevation", "format": thousands_format(mantissa=8), "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "katrisk_fl_1_in_10": hx.Float(mode="input", default=None, optionality="optional",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "KatRisk Flood\nDepth 1 in 10", "format": thousands_format(mantissa=2), "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "eq_construction_quality": hx.Str(mode="input", default=None, optionality="optional", options=schedule_eq_const_qual_list,  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "EQ Construction\nQuality", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "plan_irregularity": hx.Str(mode="input", default=None, optionality="optional", options=schedule_plan_irregularity_list,  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Plan Irregularity", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "soft_story": hx.Str(mode="input", default=None, optionality="optional", options=schedule_soft_story_list,  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Soft Story", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "vertical_irregularity": hx.Str(mode="input", default=None, optionality="optional", options=schedule_vertical_irregularity_list,  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Vertical\nIrregularity", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "ornamentation": hx.Str(mode="input", default=None, optionality="optional", options=schedule_ornamentation_list,  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Ornamentation", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "equipment_eq_bracing": hx.Str(mode="input", default=None, optionality="optional", options=schedule_equipment_eq_bracing_list,  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Equipment EQ\nBracing", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "equipment_support_maintenance": hx.Str(mode="input", default=None, optionality="optional", options=schedule_equipment_support_maintenance_list,  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Equipment\nSupport\nMaintenance", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "pounding": hx.Str(mode="input", default=None, optionality="optional", options=schedule_pounding_list,  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Pounding", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "ws_construction_quality": hx.Str(mode="input", default=None, optionality="optional", options=schedule_ws_const_qual_list,  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "WS Construction\nQuality", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "roof_anchor": hx.Str(mode="input", default=None, optionality="optional", options=schedule_roof_anchor_list,  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Roof Anchor", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "roof_equipment_hurricane_bracing": hx.Str(mode="input", default=None, optionality="optional", options=schedule_roof_equip_hurricane_bracing_list,  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Roof Equipment\nHurricane\nBracing", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "cladding_type": hx.Str(mode="input", default=None, optionality="optional", options=schedule_cladding_type_list,  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Cladding Type", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),
                "frame_foundation_connection": hx.Str(mode="input", default=None, optionality="optional", options=schedule_frame_foundation_connection_list,  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "Frame\nFoundation\nConnection", "group": "Peril Specific"}, async_output=["pull_in_exposure_management_data_task"]),

                "katrisk_score_fl": hx.Str(mode="input", default=None, optionality="optional", options_table="fl_katrisk_score", options_column="KatRisk Score", allow_custom_value=True,  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "KatRisk Score -\nFL", "group": "CatNet Score"}, async_output=["run_spatialkey_task", "pull_in_exposure_management_data_task"]),
                "catnet_score_wf": hx.Float(mode="input", default=None, optionality="optional",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "CatNet Score -\nWF", "group": "CatNet Score"}, validation={"min_value": 0, "max_value": 10}, async_output=["run_spatialkey_task", "pull_in_exposure_management_data_task"]),
                "riskmeter_score_wf": hx.Int(mode="input", default=None, optionality="optional",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "RiskMeter Score -\nWF", "group": "CatNet Score"}, validation={"min_value": 0, "max_value": 100}, async_output=["pull_in_exposure_management_data_task"]),
                
                # CatNet Scores
                "catnet_score_ha": hx.Str(mode="input", default=None, optionality="optional", options_table="ha_catnet_dropdown", options_column="Score Band", allow_custom_value=True, async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "CatNet Score -\nHA", "group": "CatNet Score"}, async_output=["run_spatialkey_task", "pull_in_exposure_management_data_task"]),
                "catnet_score_tn": hx.Str(mode="input", default=None, optionality="optional", options_table="tn_catnet_mapping_table", options_column="sk_tn_catnet_level", allow_custom_value=True, async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": "CatNet Score -\nTN", "group": "CatNet Score"}, async_output=["run_spatialkey_task", "pull_in_exposure_management_data_task"]),
                **{
                    f"catnet_score_{peril}": hx.Str(mode="input", default=None, optionality="optional", options_table=f"{peril}_catnet_score", options_column="Score Band",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": f"CatNet Score -\n{peril.upper()}", "group": "CatNet Score"}, async_output=["run_spatialkey_task", "pull_in_exposure_management_data_task"])
                    for peril in ["fl", "eq", "ws"]
                },
                **{
                    f"risk_level_{peril}": hx.Str(mode="output",  async_input=run_schedule_rater_async_tasks(async_input = True) + ["load_from_schedule_task"], view={"label": f"Risk Level -\n{peril.upper()}", "group": "Risk Grouping - For Info Only"})
                    for peril in ["eq", "ws", "fl", "scs", "wf"]
                },

                "fema_flood": hx.Int(mode="input", default=None, optionality="optional", view={"label": "Fema\nFlood", "group": "Peril Specific"}, async_output=["run_spatialkey_task", "pull_in_exposure_management_data_task"]),
                "fema_flood_risk": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Fema\nFlood\nRisk", "group": "Peril Specific"}, async_output=["run_spatialkey_task", "pull_in_exposure_management_data_task"]),
                "fema_flood_zone": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Fema\nFlood\nZone", "group": "Peril Specific"}, async_output=["run_spatialkey_task", "pull_in_exposure_management_data_task"]),
                "fema_flood_subzone": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Fema\nFlood\nSubzone", "group": "Peril Specific"}, async_output=["run_spatialkey_task", "pull_in_exposure_management_data_task"]),
                "fema_flood_combined_zone": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Fema\nFlood\nCombined Zone", "group": "Peril Specific"}, async_output=["run_spatialkey_task", "pull_in_exposure_management_data_task"]),

                # Matching Schedule Output Data
                "tiv_building_usd": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "tiv_contents_usd": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "tiv_contents_only_usd": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "tiv_contents1_usd": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "tiv_other_usd": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "tiv_bi_usd": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "tiv_total_usd": hx.Float(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                **{
                    f"score_category_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_input=run_schedule_rater_async_tasks(async_input = True), async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"Score Category -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                    for peril in ["eq", "ws", "fl", "scs", "wf"]
                },
                "output_by_layer": hx.List(mode="output", async_input=["generate_climate_doc_task"], async_output=run_schedule_rater_async_tasks(async_input = False), children={
                    "layer_index": hx.Int(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    **{
                        f"deductible_usd_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"Deductible (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                        for peril in ["fire", "eq", "ws", "fl", "scs", "cyber"] 
                    },
                    **{
                        f"sublimit_usd_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"Sublimit (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                        for peril in ["eq", "ws", "fl", "scs", "cyber"]
                    },
                    "aal_post_uw_eq_us_usd_100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "aal_post_uw_ws_us_usd_100": hx.Float(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "aal_pre_uw_eq_us_usd_100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "aal_pre_uw_ws_us_usd_100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "aal_post_uw_eq_intl_usd_100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "aal_post_uw_ws_intl_usd_100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "aal_pre_uw_eq_intl_usd_100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "aal_pre_uw_ws_intl_usd_100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    **{
                        f"coc_post_uw_usd_100_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"coc_post_uw_usd_100 (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                        for peril in ["eq", "fl", "ha", "tn", "wf", "ws"]
                    },
                    **{
                        f"coc_pre_uw_usd_100_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"coc_pre_uw_usd_100 (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                        for peril in ["eq", "fl", "ha", "tn", "wf", "ws"]
                    },
                    **{
                        f"el_post_uw_usd_100_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"el_post_uw_usd_100_ (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                        for peril in ["eq", "fire_total", "fl", "ha", "tn", "total", "wf", "ws", "cyber_total"]
                    },
                    **{
                        f"el_pre_uw_usd_100_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"el_pre_uw_usd_100_ (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                        for peril in ["eq", "fire_total", "fl", "ha", "tn", "total", "wf", "ws", "cyber_total"]    
                    },
                    **{
                        f"flc_entry_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"flc_entry_ (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                        for peril in ["eq", "fire", "fl", "ha", "tn", "wf", "ws"]    
                    },
                    **{
                        f"flc_exit_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"flc_exit_ (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                        for peril in ["eq", "fire", "fl", "ha", "tn", "wf", "ws"]    
                    },
                    **{
                        f"flc_worth_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"flc_worth_ (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                        for peril in ["eq", "fire", "fl", "ha", "tn", "wf", "ws"]    
                    },
                    "lae_post_uw_eq_usd100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "lae_post_uw_ws_usd100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "lae_pre_uw_eq_usd100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "lae_pre_uw_ws_usd100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    **{
                        f"premtp_gn_max_post_uw_usd_100_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"premtp_gn_max_post_uw_usd_100_ (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                        for peril in ["eq", "fire", "fl", "ha", "tn", "wf", "ws", "cyber", "total"]    
                    },
                    **{
                        f"premtp_gn_max_pre_uw_usd_100_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"premtp_gn_max_post_uw_usd_100_ (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                        for peril in ["eq", "fire", "fl", "ha", "tn", "wf", "ws", "cyber", "total"]    
                    },
                    **{
                        f"rate_base_total_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"rate_base_total_ (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                        for peril in ["eq", "fire", "fl", "scs", "wf", "ws"]    
                    },
                    **{
                        f"rate_gu_total_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"rate_gu_total_ (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                        for peril in ["eq", "fire", "fl", "scs", "wf", "ws"]    
                    },
                    "ri_cost_post_uw_eq_usd100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "ri_cost_post_uw_ws_usd100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "ri_cost_pre_uw_eq_usd100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "ri_cost_pre_uw_ws_usd100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "sd_post_uw_eq_usd100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "sd_post_uw_ws_usd100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "sd_pre_uw_eq_usd100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "sd_pre_uw_ws_usd100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    **{
                        f"tivexposed_total_usd_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"tivexposed_total_usd_ (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                        for peril in ["eq", "fire", "fl", "scs", "wf", "ws"]
                    }
                }),
                "cgear_score_total": hx.Float(mode="input", optionality="optional", default=None, async_input=["generate_climate_doc_task"], async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_basement_fl": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_bi_cbi": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_bi_indemnityperiod": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_bi_waitingperiod": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                **{
                    f"rfr_construction_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"rfr_construction_ (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                    for peril in ["eq", "fire", "fl", "ha", "tn", "wf", "ws"]
                },
                "rfr_elevation_fl": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_floorarea_ha": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_floorarea_ws": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                **{
                    f"rfr_hazardscore_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"rfr_hazardscore_ (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                    for peril in ["eq", "fl", "ha", "tn", "wf", "ws"]
                },
                "rfr_hazardscoreriskmeter_wf": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_katriskscore_fl": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_mexicanfonden_fire": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_nofloors_eq": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_nofloors_fl": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_nofloors_ws": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                **{
                    f"rfr_occ_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"rfr_occ_ (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                    for peril in ["eq", "ha", "tn", "wf", "ws"]
                },
                **{
                    f"rfr_sizedisc_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"rfr_sizedisc_ (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                    for peril in ["ha", "tn", "wf", "fl", "fire"]
                },
                "rfr_ppc_fire": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_ppc_wf": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_riskquality_fire": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_roofage_ha": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_roofage_ws": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_roofcovering_ha": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_roofcovering_ws": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_roofgeometry_ha": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_roofgeometry_ws": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_sprinkler_fire": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "rfr_ss_ws": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                **{
                    f"rfr_yearbuilt_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"rfr_yearbuilt_ (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                    for peril in ["eq", "ha", "tn", "ws"]
                },
            }),
            "large_schedule_output": hx.List(mode="output", async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], children={
                "zip": hx.Str(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": "Zip", "read_only": True}),
                "country": hx.Str(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": "Country", "read_only": True}),
                "state": hx.Str(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "State", "read_only": True}),
                "county": hx.Str(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False) + ["run_simulation_task"], view={"label": "County", "read_only": True}),
                "gate_no_eq": hx.Str(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": "Gate Number Earthquake", "read_only": True}),
                "gate_no_ws": hx.Str(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": "Gate Number Windstorm", "read_only": True}),
                "occupancy": hx.Str(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": "Occupancy", "read_only": True}),
                "tiv_buildings": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "tiv_contents": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "tiv_other": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "tiv_bi": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "ex_rate": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                "output_by_layer": hx.List(mode="output", async_output=run_schedule_rater_async_tasks(async_input = False), children={
                    "layer_index": hx.Int(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    **{
                        f"el_pre_uw_usd_100_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"el_pre_uw_usd_100_ (USD) -\n{peril.upper()}", "read_only": True})
                        for peril in ["eq", "fire_total", "fl", "ha", "tn", "total", "wf", "ws", "cyber_total"]
                    },
                    "aal_pre_uw_eq_us_usd_100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),                    
                    "aal_pre_uw_ws_us_usd_100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "aal_pre_uw_eq_intl_usd_100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "aal_pre_uw_ws_intl_usd_100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    **{
                        f"coc_pre_uw_usd_100_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"coc_pre_uw_usd_100_ (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                        for peril in ["eq", "fl", "ha", "tn", "wf", "ws", "cyber"]
                    },
                    **{
                        f"deductible_usd_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"Deductible (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                        for peril in ["fire", "eq", "ws", "fl", "scs", "cyber"]
                    },
                    "ri_cost_pre_uw_eq_usd100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "ri_cost_pre_uw_ws_usd100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "lae_pre_uw_eq_usd100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    "lae_pre_uw_ws_usd100": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
                    **{
                        f"tivexposed_total_usd_{peril}": hx.Float(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"tivexposed_total_usd_ (USD) -\n{peril.upper()}", "read_only": True, "group": "Peril Specific"})
                        for peril in ["eq", "fire", "fl", "scs", "wf", "ws"]
                    }
                }),
                **{
                    f"catnet_score_{peril}": hx.Str(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": f"CatNet Score -\n{peril.upper()}", "read_only": True})
                    for peril in ["tn", "ha", "fl", "eq", "ws", "wf"]
                },
                "cresta_zone": hx.Str(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": "Cresta Zone", "group": "Peril Specific", "read_only": True}),
                "ws_tier": hx.Int(mode="input", optionality="optional", default=None, async_output=run_schedule_rater_async_tasks(async_input = False), view={"label": "WS Tier", "group": "Peril Specific", "read_only": True}),
            }),
            "schedule_total": hx.Structure(view={"label": "Total"}, children={
                "tiv_buildings": hx.Float(mode="output", view={"label": "Buildings", "group": "Insured Values", "format": thousands_format()}),
                "tiv_contents": hx.Float(mode="output", view={"label": "Contents", "group": "Insured Values", "format": thousands_format()}),
                "tiv_other": hx.Float(mode="output", view={"label": "Other", "group": "Insured Values", "format": thousands_format()}),
                "tiv_bi": hx.Float(mode="output", view={"label": "BI", "group": "Insured Values", "format": thousands_format()}),
                "tiv_total": hx.Float(mode="output", view={"label": "Total", "group": "Insured Values", "format": thousands_format()}, async_input=["expiring_policy_fetch_task", "generate_quote_doc_task"]),
                "floor_area": hx.Float(mode="output", view={"label": "Floor Area", "group": "Peril Specific", "format": thousands_format()}, async_input=["expiring_policy_fetch_task", "generate_quote_doc_task"]),
                "num_locs": hx.Int(mode="output", view={"label": "Number of Locations in Schedule", "format": thousands_format()}, async_input=["expiring_policy_fetch_task"]),
            }),
        })
    
    spatialkey_input_paths = ["schedule_table", "schedule_table/tiv_bi", "schedule_table/tiv_buildings", "schedule_table/tiv_other", "schedule_table/tiv_contents", "schedule_table/address_dropdown/city", "schedule_table/address_dropdown/country", \
        "schedule_table/address_dropdown/county", "schedule_table/address_dropdown/state", "schedule_table/industry_occupancy_dropdown/occupancy", "schedule_table/constr_code", "schedule_table/latitude", "schedule_table/longitude", "schedule_table/loc_id", "schedule_table/sprinkler", "schedule_table/street_name", "schedule_table/zip"]
    set_node_properties(schedule_schema, spatialkey_input_paths, async_input=["run_spatialkey_task"])

    spatialkey_output_paths = ["schedule_table/catnet_score_tn", "schedule_table/katrisk_score_fl", "schedule_table/catnet_score_ha", "schedule_table/catnet_score_ws", \
        "schedule_table/catnet_score_fl", "schedule_table/catnet_score_eq", "schedule_table/catnet_score_wf", "schedule_table/fema_flood", "schedule_table/fema_flood_risk", \
            "schedule_table/fema_flood_zone", "schedule_table/fema_flood_subzone", "schedule_table/fema_flood_combined_zone", "schedule_table/floodzone"]
    set_node_properties(schedule_schema, spatialkey_output_paths, async_output=["run_spatialkey_task"])



    return {
        "schedule" : schedule_schema,
    }
