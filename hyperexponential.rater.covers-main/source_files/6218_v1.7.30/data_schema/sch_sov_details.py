import hx_data_schema as hx
import data_schema.sch_utilities as utils
from data_schema.sch_show_hide_and_dropdown import schedule_policy_type, sprinkler_list, covered_list


CONSTR_CODE_MAX = 6
ATC_CODE_MAX = 54
PC_CODE_MAX = 10

#cds.extend_node_rater_defined("cds/exposure/aggregate", {
#    "policy_type_summary": hx.Structure(children={
#        "new_renewal_summary": hx.Str(
#            mode="input",
#            default="Unknown",
#            options=schedule_policy_type,
#            view={"label": "Policy Type (New/Renewal)", "group": "Policy Summary"}
#        )
#    })
#})


def sch_sov_details(cds):
    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        "spatialkey": hx.Structure(children={
            "fetch_status": hx.Str(mode="output", async_output=["run_spatialkey_task"], view={"label": "Fetch Status", "multiline": True}),
            "csv_status": hx.Str(mode="output", view={"label": "Spatialkey Task Status"}),
            "job_id": hx.Str(mode="output", async_input=["open_spatialkey_dashboard_task"], async_output=["run_spatialkey_task"], view={"label": "Spatial Key Job ID"}),
            "dataset_id": hx.Str(mode="output", async_input=["open_spatialkey_dashboard_task"],  async_output=["run_spatialkey_task"], view={"label": "Spatial Key Dataset ID"}),
            "dashboard_note": hx.Str(mode="output", async_output=["open_spatialkey_dashboard_task"], view={"label": "Spatial Key Dashboard", "multiline": True}),
        }),
        "debug": hx.Str(mode="output", async_output=["run_simulation_task", "load_into_debug_task"]),
        "schedule_warnings": hx.Str(mode="output", view={"label": "Warnings/Messages"}),
        "run_rater_information": hx.Str(mode="output"),
        # For simulation ELT search
        "simulation_fetch_status": hx.Str(mode="output", async_output=["run_simulation_task"], view={"label": "Simulation Status"}),      
    })


    cds.extend_node_rater_defined("cds/exposure/granular", {
      "schedule_table": hx.List(mode="input", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], children={
            # General fields
            "last_updated"                 : hx.Date(mode="input",     default=None,      optionality="optional",       async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Update\nDate",              "group": "General"}),
            "loc_id"                       : hx.Str(mode="input",      default=None,      optionality="optional",       async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "LocID",                     "group": "General"}),
            "acc_name"                     : hx.Str(mode="input",      default=None,      optionality="optional",       async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Account\nName",             "group": "General"}),
            "acc_number"                   : hx.Str(mode="input",      default=None,      optionality="optional",       async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Account\nNumber",           "group": "General"}),
            "inception_date"               : hx.Date(mode="input",     default=None,      optionality="optional",       async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Inception Date",            "group": "General"}),
            "expiry_date"                  : hx.Date(mode="input",     default=None,      optionality="optional",       async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Expiry Date",               "group": "General"}),
            "ceded_share"                  : hx.Float(mode = "input",  default=None,      optionality="optional",       async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], #validation={"min_value": 0, "max_value": 1}, 
                view={"label": "Ceded Share",               "group": "General", "format": utils.percent_format(2)}),
            "acc_beazley_received_gg_prem" : hx.Float(mode="input",    default=None,      optionality="optional",       async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Account AFB Recieved GGP",  "group": "General", "format": utils.thousands_format(0)}),
            "acc_all_perils_gg_sd"         : hx.Float(mode="input",    default=None,      optionality="optional",       async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Account all\nPerils SD",    "group": "General", "format": utils.thousands_format(0)}),
            "loc_1_in_250_oep"             : hx.Float(mode="input",    default=None,      optionality="optional",       async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "1 in 250\nOEP",             "group": "General", "format": utils.thousands_format(0)}),
            "loc_1_in_10_aep"              : hx.Float(mode="input",    default=None,      optionality="optional",       async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "1 in 10\nAEP",              "group": "General", "format": utils.thousands_format(0)}),
            "new_renewal"                  : hx.Str(mode="input",      default="Unknown", options=schedule_policy_type, async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "New/Renewal",               "group": "General"}),
            "loc_ws_beazley_share_gg_aal": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "AFB WS AAL", "format": utils.thousands_format(0), "group": "WS"}),
            "loc_eq_beazley_share_gg_aal": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "AFB AAL (WS and EQ only)", "format": utils.thousands_format(0), "group": "EQ"}),
        
            # Address field
            "address_dropdown": hx.Structure(view={"linked_options_selector": "hierarchical"}, linked_options_table="table_address", linked_options_columns=["Country", "State", "County", "City"], linked_default_index=0, children={
                "country": hx.Str(mode="input", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Country", "group": "Address"}),
                "state": hx.Str(mode="input", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "State", "group": "Address"}),
                "county": hx.Str(mode="input", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "County", "group": "Address"}),
                "city": hx.Str(mode="input", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "City", "group": "Address"})
            }),

            "street_address": hx.Str(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Street Name", "group": "Address"}),
            "zip": hx.Str(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"],  view={"label": "Zip", "group": "Address"}),
            "latitude": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Latitude", "format": utils.thousands_format(6), "group": "Address"}, validation={"min_value": -90, "max_value": 90}),
            "longitude": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Longitude", "format": utils.thousands_format(6), "group": "Address"}, validation={"min_value": -180, "max_value": 180}),


            # # TIV - Risk Currency field
            "loc_tiv_buildings": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Buildings", "format": utils.thousands_format(0), "group": "TIV - Risk Currency"}),
            "loc_tiv_contents": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Contents", "format": utils.thousands_format(0), "group": "TIV - Risk Currency"}),
            "loc_tiv_bi": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "BI", "format": utils.thousands_format(0), "group": "TIV - Risk Currency"}),
            "loc_tiv_total": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Total", "format": utils.thousands_format(0), "group": "TIV - Risk Currency"}),

            # Construction field
            "iso_constr": hx.Str(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Construction\nISO", "group": "Construction"}),
            "ppc_code": hx.Int(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "PPC", "group": "Construction"}),
            "sprinkler": hx.Str(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Sprinkler?", "group": "Construction"}),
            "occupancy_description": hx.Str(mode="input", default=None, async_input=["run_bordereau_rater_task" , "simulate_pc_task"], optionality="optional", async_output=["pull_in_exposure_management_data_task"], view={"label": "Occupancy\nDescription", "group": "Construction"}),
            "num_stories": hx.Int(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Num\nStories", "group": "Construction"}),
            "year_built": hx.Int(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Year\nBuilt", "format": {"thousandSeparated": False}, "group": "Construction"}),
            "floor_area": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"],  view={"label": "Floor\nArea", "format":  utils.thousands_format(0), "group": "Construction"}),
            "distance_to_coast": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"],  view={"label": "Distance\nto Coast", "format":  utils.thousands_format(0), "group": "Construction"}),
            "beazley_gate": hx.Str(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Beazley Gate?", "group": "Construction"}), # if we needs to save nodes we can calculate this based on zip rather than pulling from EM

            "industry_occupancy_dropdown": hx.Structure(view={"linked_options_selector": "hierarchical"}, linked_options_table="table_atc_mapping", linked_options_columns=["BI Group", "Mapped ATC"], linked_default_index=0, children={
                "industry": hx.Str(mode="input", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Industry", "group": "Construction"}),
                "occupancy": hx.Str(mode="input", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Occupancy", "group": "Construction"}),
            }),

            # nodes for reporting these will not be displayed 
            "rms_event_15022534": hx.Float(mode="output", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "California eq - Los Angeles\n(15022534)"}),
            "rms_event_15006191": hx.Float(mode="output", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "California eq - San Francisco\n(15006191)"}),
            "rms_event_15355285": hx.Float(mode="output", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "New Madrid eq\n(15355285)"}),
            "rms_event_15387653": hx.Float(mode="output", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "New Madrid Extreme Stress Event\n(15387653)"}),
            "rms_event_15100131": hx.Float(mode="output", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "PNW eq\n(15100131)"}),
            "rms_event_2865409": hx.Float(mode="output", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Florida ws #1 - Miami-Dade\n(2865409)"}),
            "rms_event_2869298": hx.Float(mode="output", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Florida ws #2 - Pinellas Hurricane\n(2869298)"}),
            "rms_event_2848918": hx.Float(mode="output", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "USA ws Gulf of Mexico\n(2848918)"}),
            "rms_event_2867710": hx.Float(mode="output", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Carolinas ws immediately following NE ws\n(2867710)"}),
            "rms_event_2874165": hx.Float(mode="output", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "North East ws\n(2874165)"}),

          
            **{
                f"{peril}_loc_beazley_share_aal": hx.Float(mode= "input", default=None, optionality="optional", view={"label": f"Loc\n{peril_name}\n AAL AFB", "group": f"{peril_name}"})
                for peril, peril_name in zip (("ws", "eq"), ("WS", "EQ"))
            },

            # AOP 
            **partial_common_peril_nodes("aop"),


            #Fire
            "fire_occupancy_modifier": hx.Float(mode="output", view={"label": "Occupancy", "format": utils.percent_format(0), "group": "Modifiers"}),
            "fire_size_discount_modifier": hx.Float(mode="output", view={"label": "Size Discount\n", "format": utils.thousands_format(2), "group": "Modifiers"}),
            "fire_proportion_covered": hx.Float(mode="output", view={"label": "\nProportion Covered", "format": utils.thousands_format(2), "group": "Modifiers"}),
            "fire_iso_ppc_modifier": hx.Float(mode="output", view={"label": "PPC", "format": utils.thousands_format(2), "group": "Modifiers"}),
            **common_peril_nodes("fire"),

            #WS
            "loc_ws_beazley_share_gg_aal": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Location Wind\nAAL AFB", "group": "WS", "format": utils.thousands_format(0)}),

            "ws_ded_modifier": hx.Float(mode="output", view={"label": "Deductible", "format": utils.percent_format(0), "group": "Modifiers"}),
            "ws_construction_modifier": hx.Float(mode="output", view={"label": "Construction", "format": utils.percent_format(0), "group": "Modifiers"}),
            "ws_occupancy_modifier": hx.Float(mode="output", view={"label": "Occupancy", "format": utils.percent_format(0), "group": "Modifiers"}),
            "ws_num_floors_modifier": hx.Float(mode="output", view={"label": "Number of Floors", "format": utils.percent_format(0), "group": "Modifiers"}),
            "ws_yb_modifier": hx.Float(mode="output", view={"label": "YB", "format": utils.percent_format(0), "group": "Modifiers"}),
            **common_peril_nodes("ws"),
            **partial_common_peril_nodes("ws"),

            #EQ
            "loc_eq_beazley_share_gg_aal": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Location EQ\nAAL AFB", "group":"EQ", "format": utils.thousands_format(0)}),

            "eq_ded_modifier": hx.Float(mode="output", view={"label": "Deductible", "format": utils.percent_format(0), "group": "Modifiers"}),
            "eq_construction_modifier": hx.Float(mode="output", view={"label": "Construction", "format": utils.percent_format(0), "group": "Modifiers"}),
            "eq_occupancy_modifier": hx.Float(mode="output", view={"label": "Occupancy", "format": utils.percent_format(0), "group": "Modifiers"}),
            "eq_num_floors_modifier": hx.Float(mode="output", view={"label": "Number of Floors", "format": utils.percent_format(0), "group": "Modifiers"}),
            "eq_yb_modifier": hx.Float(mode="output", view={"label": "YB", "format": utils.percent_format(0), "group": "Modifiers"}),
            **common_peril_nodes("eq"),
            **partial_common_peril_nodes("eq"),

            #SCS
            "scs_construction_modifier": hx.Float(mode="output", view={"label": "Construction", "format": utils.percent_format(0), "group": "Modifiers"}),
            "scs_occupancy_modifier": hx.Float(mode="output", view={"label": "Occupancy", "format": utils.percent_format(0), "group": "Modifiers"}),
            "scs_year_built_modifier": hx.Float(mode="output", view={"label": "Year\nBuilt", "format": utils.percent_format(0), "group": "Modifiers"}),
            "scs_bhi_modifier": hx.Float(mode="output", view={"label": "BHI", "format": utils.percent_format(0), "group": "Modifiers"}),
            "scs_fl_area_modifier": hx.Float(mode="output", view={"label": "Floor\nArea", "format": utils.percent_format(0), "group": "Modifiers"}),
            "scs_size_discount_modifier": hx.Float(mode="output", view={"label": "Size Discount", "format": utils.thousands_format(0), "group": "Modifiers"}),
            **common_peril_nodes("scs"),
            **partial_common_peril_nodes("scs"),
                   
            #fl
            "fl_spatial_key_modifier": hx.Float(mode="output", view={"label": "Spatial\nKey", "format": utils.percent_format(0), "group": "Modifiers"}),
            "fl_construction_modifier": hx.Float(mode="output", view={"label": "Construction", "format": utils.percent_format(0), "group": "Modifiers"}),
            "fl_num_floors_modifier": hx.Float(mode="output", view={"label": "Number of Floors", "format": utils.percent_format(0), "group": "Modifiers"}),
            **common_peril_nodes("fl"),
            
            #WF
            "wf_spatial_key_modifier": hx.Float(mode="output", view={"label": "WF Spatial\nKey", "format": utils.percent_format(0), "group": "Modifiers"}),
            "wf_construction_modifier": hx.Float(mode="output", view={"label": "WF Construction", "format": utils.percent_format(0), "group": "Modifiers"}),
            "wf_occupancy_modifier": hx.Float(mode="output", view={"label": "WF Occupancy", "format": utils.percent_format(0), "group": "Modifiers"}),
            "wf_ppc_modifier": hx.Float(mode="output", view={"label": "WF PPC", "format": utils.percent_format(0), "group": "Modifiers"}),
            **common_peril_nodes("wf"),

            #WTS
            **common_peril_nodes("wts"),
        }),


        "sov_total": hx.Structure(view={"label": "Total"}, children={
            "num_locs": hx.Int(mode="output", view={"label": "Number of Locations in Schedule", "format": utils.thousands_format(0)}, async_output=["pull_in_exposure_management_data_task"]),
            "loc_tiv_buildings": hx.Float(mode="output", view={"label": "Buildings", "format": utils.thousands_format(0)}, async_output=["pull_in_exposure_management_data_task"]),
            "loc_tiv_contents": hx.Float(mode="output", view={"label": "Contents", "format": utils.thousands_format(0)}, async_output=["pull_in_exposure_management_data_task"]),
            "loc_tiv_bi": hx.Float(mode="output", view={"label": "BI", "format": utils.thousands_format(0)}, async_output=["pull_in_exposure_management_data_task"]),
            "loc_tiv_total": hx.Float(mode="output", view={"label": "Total", "format": utils.thousands_format(0)}, async_input=["simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"]),
            "loc_ws_beazley_share_gg_aal": hx.Float(mode="output", view={"label": "Location Wind\nAAL AFB", "group": "WS", "format": utils.thousands_format(0)}, async_output=["pull_in_exposure_management_data_task"]),
            "loc_eq_beazley_share_gg_aal": hx.Float(mode="output", view={"label": "Location EQ\nAAL AFB", "group": "EQ", "format": utils.thousands_format(0)}, async_output=["pull_in_exposure_management_data_task"]),
            "floor_area": hx.Float(mode="output", view={"label": "Floor Area", "format": utils.thousands_format(0), "group": "Construction"}, async_output=["pull_in_exposure_management_data_task"]),
        }), 

    }),

    # add muliple names to ws. eq, and scs for display purposes
    for peril, full_name in zip (("ws", "eq","scs"), ("WS", "EQ", "SCS")):

        cds.override_node_properties(f"cds/exposure/granular/schedule_table/loc_{peril}_covered", {"view": {"options": {
            "exposure_details": {"group": f"{full_name}"},
            "pricing": {"group": "General"}
        }}})

        cds.override_node_properties(f"cds/exposure/granular/schedule_table/loc_{peril}_excess", {"view": {"options": {
            "exposure_details": {"group": f"{full_name}"},
            "pricing": {"group": "Rating Metrics"}
        }}})

        cds.override_node_properties(f"cds/exposure/granular/schedule_table/loc_{peril}_limit", {"view": {"options": {
            "exposure_details": {"group": f"{full_name}"},
            "pricing": {"group": "Rating Metrics"}
        }}})

        cds.override_node_properties(f"cds/exposure/granular/schedule_table/loc_{peril}_ded", {"view": {"options": {
            "exposure_details": {"group": f"{full_name}"},
            "pricing": {"group": "Rating Metrics"}
        }}})

    #add multiple names to AOP for display purposes
    cds.override_node_properties(f"cds/exposure/granular/schedule_table/loc_aop_covered", {"view": {"options": {
        "fire_exposure_details": {"group": "Fire"},
        "fl_exposure_details": {"group": "FL"},
        "wf_exposure_details": {"group": "WF"},
        "pricing": {"group": "Rating Metrics"},
    }}})
    cds.override_node_properties(f"cds/exposure/granular/schedule_table/loc_aop_excess", {"view": {"options": {
        "fire_exposure_details": {"group": "Fire"},
        "fl_exposure_details": {"group": "FL"},
        "wf_exposure_details": {"group": "WF"},
        "pricing": {"group": "Rating Metrics"},
    }}})
    cds.override_node_properties(f"cds/exposure/granular/schedule_table/loc_aop_limit", {"view": {"options": {
        "fire_exposure_details": {"group": "Fire"},
        "fl_exposure_details": {"group": "FL"},
        "wf_exposure_details": {"group": "WF"},
        "pricing": {"group": "Rating Metrics"},
    }}})
    cds.override_node_properties(f"cds/exposure/granular/schedule_table/loc_aop_ded", {"view": {"options": {
        "fire_exposure_details": {"group": "Fire"},
        "fl_exposure_details": {"group": "FL"},
        "wf_exposure_details": {"group": "WF"},
        "pricing": {"group": "Rating Metrics"},
    }}})








def common_peril_nodes(peril):

    return{
        f"{peril}_total_modifier_impact": hx.Float(mode="output", async_output=["pull_in_exposure_management_data_task"], view={"label": "Total Impact", "format": utils.percent_format(2), "group": "Modifiers"}),
        f"{peril}_base_rate": hx.Float(mode="output", async_output=["pull_in_exposure_management_data_task"], view={"label": "Base Rate", "format": utils.thousands_format(2), "group": "Rating Metrics"}),
        f"{peril}_worth": hx.Float(mode="output", async_output=["pull_in_exposure_management_data_task"], view={"label": "Worth", "format": utils.thousands_format(2), "group": "Rating Metrics"}),
        f"{peril}_el": hx.Float(mode="output", async_output=["pull_in_exposure_management_data_task"], view={"label": "EL", "format": utils.thousands_format(2), "group": "Rating Metrics"}),
        f"{peril}_rate": hx.Float(mode="output", async_output=["pull_in_exposure_management_data_task"], view={"label": "Rate", "format": utils.thousands_format(2), "group": "Rating Metrics"}),
        f"{peril}_gn_tp": hx.Float(mode="output", async_output=["pull_in_exposure_management_data_task"], view={"label": "GN TP", "format": utils.thousands_format(0), "group": "Rating Metrics"}),
        f"{peril}_loc_profit": hx.Float(mode="output", async_output=["pull_in_exposure_management_data_task"], view={"label": "Profit", "format": utils.thousands_format(0), "group": "Rating Metrics"}),
        
    }

def partial_common_peril_nodes(peril):
    return{
        f"loc_{peril}_covered": hx.Str(mode = "input", default="Yes", optionality="optional", options=covered_list, async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Covered?"}),
        f"loc_{peril}_excess": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Excess", "format": utils.thousands_format(0)}),
        f"loc_{peril}_limit": hx.Float(mode="input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Limit", "format": utils.thousands_format(0)}),
        f"loc_{peril}_ded": hx.Float(mode= "input", default=None, optionality="optional", async_input=["run_bordereau_rater_task" , "simulate_pc_task"], async_output=["pull_in_exposure_management_data_task"], view={"label": "Deductible", "format": utils.thousands_format(0)}),
    }
