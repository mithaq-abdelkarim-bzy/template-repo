import hx
import pandas as pd 

def push_file_to_temp(hxd):
    '''
    Push output file to temp file
    '''
    with hxd.schedule.large_schedule_workflow.large_schedule_em_file.open("b") as f:
        df = pd.read_csv(f)

    with hxd.temp.schedule_file.open("b") as f:
        df.to_csv(f, index=False)


def push_df_to_temp(hxd):
    '''
    Push output file to temp file
    '''
    with hxd.schedule.large_schedule_workflow.schedule_output_file.open("b") as f:
        df = pd.read_feather(f)

    with hxd.temp.schedule_file.open("b") as f:
        df.to_csv(f, index=False)


def load_from_schedule(hxd):
    '''
    Load the schedule and temp file and merge it into the latest output file
    '''
    old_df = pd.DataFrame()

    if hxd.temp.schedule_file.exists:
        with hxd.temp.schedule_file.open("b") as f:
            old_df = pd.read_csv(f)

    columns = ["loc_id", "broker_loc_id", "broker_subloc_id", "fire_deductible", "currency", "fire_covered", "eq_covered", "ws_covered",
                "fl_covered", "scs_covered", "wf_covered", "street_name", "zip", "property_description", "latitude", "longitude",
                "tiv_buildings", "tiv_contents", "tiv_other", "tiv_bi", "constr_code", "raw_constr_code", "constr_description",
                "num_buildings", "num_stories", "year_built", "year_updated", "broker_occu_desc", "rms_occupancy", "pc_code", "sprinkler",
                "year_cov_last_replaced", "roof_age", "floor_area", "distance_from_coast", "roof_covering", "roof_geometry", "soil_type", 
                "liquefaction", "landslide", "floodzone", "other_floodzone", "basement", "building_elevation", "katrisk_fl_1_in_10", 
                "eq_construction_quality", "plan_irregularity", "soft_story", "vertical_irregularity", "ornamentation", "equipment_eq_bracing",
                "equipment_support_maintenance", "pounding", "ws_construction_quality", "roof_anchor", "roof_equipment_hurricane_bracing",
                "cladding_type", "frame_foundation_connection", "catnet_score_tn", "catnet_score_ha", "katrisk_score_fl", "catnet_score_fl",
                "catnet_score_wf", "catnet_score_eq", "catnet_score_ws", "riskmeter_score_wf"]

    df = pd.DataFrame([{column: getattr(row, column) for column in columns} for row in hxd.schedule.schedule_table])

    df["industry_occupancy_dropdown/industry"] = [row.industry_occupancy_dropdown.industry for row in hxd.schedule.schedule_table]
    df["industry_occupancy_dropdown/occupancy"] = [row.industry_occupancy_dropdown.occupancy for row in hxd.schedule.schedule_table]
    df["address_dropdown/country"] = [row.address_dropdown.country for row in hxd.schedule.schedule_table]
    df["address_dropdown/state"] = [row.address_dropdown.state for row in hxd.schedule.schedule_table]
    df["address_dropdown/county"] = [row.address_dropdown.county for row in hxd.schedule.schedule_table]
    df["address_dropdown/city"] = [row.address_dropdown.city for row in hxd.schedule.schedule_table]

    if not old_df.empty:
        df = old_df.append(df)

    with hxd.schedule.large_schedule_workflow.large_schedule_em_file.open("b") as f:
        df.to_csv(f, index=False)

    hxd.schedule.large_schedule_workflow.load_from_em_database = True

def load_into_debug(hxd, batch_size=5000):
    with hxd.temp.schedule_file.open("b") as f:
        df = pd.read_csv(f)

    if "level_0" in df.columns:
        df = df.drop("level_0", axis=1)

    if df.shape[0] > batch_size:
        df_batch = df[:batch_size]
        df_rest = df[batch_size:]
    else:
        df_batch = df
        df_rest = pd.DataFrame(columns=df.columns)

    hxd.schedule.debug = df_batch.to_csv()

    with hxd.schedule.large_schedule_workflow.schedule_output_file.open("b") as f:
        df_rest.reset_index().to_feather(f)