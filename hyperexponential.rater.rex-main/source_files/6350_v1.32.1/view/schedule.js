import * as HX from "hx-model-components";
import { render_notifications } from "view/results_tables";
import InfoBox from "components/infobox";

function schedule() {
  return (
    <HX.Page title="Schedule" fullWidth={true} shownBy="model_state/show_after_landing_page">
      {render_notifications()}
      <HX.Section title="Exposure Management Database Import">
        {/* <HX.Button task="import_accgrpid_only_task" title="Run" /> */}
        <HX.Section title="Search Filters">
          <HX.Pane>
            <HX.Collection fields={[
              "exposure_management_api/inputs/accgrpid",
              "exposure_management_api/inputs/account_name",
            ]} horizontal />
            <HX.Collection fields={[
              "exposure_management_api/inputs/reference",
              "exposure_management_api/inputs/team"
            ]} horizontal />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={["exposure_management_api/limit_results"]} />
            <HX.Button task="search_exposure_management_data_task" title="Search Exposure Management Database" />
            <HX.Notes field="exposure_management_api/search_fetch_status" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Search Results">
          <HX.Table
            data={["exposure_management_api/search_results"]}
            fields={[
              "accgrpid",
              "reference",
              "account_number",
              "account_name",
              "last_edit",
              "num_locs",
              "selected"
            ]}
          />
          <HX.Pane flow="right">
            <HX.Button task="pull_in_exposure_management_data_task" title="Pull in Selected" />
            <HX.Notes field="exposure_management_api/location_fetch_status" />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
      </HX.Section>

      <HX.Section title="Schedule Upload" shownBy="policy_information/large_schedule_model" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.File field="schedule/large_schedule_workflow/schedule_file" title="Schedule Upload" />
            <HX.Button task="confirm_override_task" title="Confirm Upload" />
          </HX.Pane>
          <HX.File field="schedule/large_schedule_workflow/large_schedule_em_file" title="Schedule Download" />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="SpatialKey Integration">
        <HX.Pane flow="right">
          <HX.Button title="Upload" task="run_spatialkey_task" />
          <HX.Notes field="spatialkey/fetch_status" />
          <HX.Button title="Refresh Dashboard Link" task="open_spatialkey_dashboard_task" />
          <HX.Notes field="dashboard_note" with="spatialkey" />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Schedule" shownBy="policy_information/small_schedule_model">
        <HX.Pane flow="right">
          <HX.Collection horizontal fields={[
            "schedule/schedule_total/num_locs",
            { field: "schedule/schedule_total/tiv_total", labelBy: "schedule/tiv_total_outside_table_label" }
          ]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Pane flow="right" shownBy="info/remodelling_not_needed">
            <HX.Button task="check_remodel_task" title="Remodelling Check" />
            <HX.Notes field={'info/remodel_msg'} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right" shownBy="info/remodelling_needed">
            <HX.Button task="check_remodel_task" title="Remodelling Check" />
            <HX.Notes field={'info/remodel_msg'} />
            <HX.File field="email/remodelling_check_file" />
            <InfoBox textNode="info/remodelling_info_msg" />
            <HX.Pane />
          </HX.Pane>
        </HX.Pane>
        <HX.Table
          data={["schedule_total", null, "schedule_table"]}
          fields={[
            "address_dropdown/country", "address_dropdown/state", "address_dropdown/county", "address_dropdown/city",
            "street_name", "zip", "property_description", "latitude", "longitude",
            "currency",
            { field: "tiv_buildings", labelBy: "tiv_buildings_label" },
            { field: "tiv_contents", labelBy: "tiv_contents_label" },
            { field: "tiv_other", labelBy: "tiv_other_label" },
            { field: "tiv_bi", labelBy: "tiv_bi_label" },
            { field: "tiv_total", labelBy: "tiv_total_label" },
            "fire_deductible", "fire_covered", "eq_covered", "ws_covered", "fl_covered", "scs_covered", "wf_covered",
            "industry_occupancy_dropdown/industry", "industry_occupancy_dropdown/occupancy", "broker_occu_desc", "rms_occupancy",
            "constr_code", "raw_constr_code", "constr_description", "num_buildings", "num_stories", "year_built", "year_updated", "sprinkler",
            "catnet_score_tn", "catnet_score_ha", "katrisk_score_fl", "catnet_score_fl",
            "catnet_score_wf", "catnet_score_eq", "catnet_score_ws", "riskmeter_score_wf",

            "pc_code", "year_cov_last_replaced", "roof_age",
            "floor_area", "distance_from_coast", "roof_covering", "roof_geometry", "floodzone",
            "basement", "eq_construction_quality", "plan_irregularity",
            "soft_story", "vertical_irregularity", "ornamentation", "equipment_eq_bracing", "liquefaction", "equipment_support_maintenance",
            "pounding", "ws_construction_quality", "roof_anchor", "roof_equipment_hurricane_bracing", "cladding_type", "frame_foundation_connection",
            "ws_tier", "wf_tier", "ws_gate", "eq_gate", "eq_crit_cat_zone", "ws_crit_cat_zone", "cresta_zone",
            "risk_level_eq", "risk_level_ws", "risk_level_fl", "risk_level_scs", "risk_level_wf",
            "loc_id", "broker_loc_id", "broker_subloc_id"
          ]}
          with="schedule"
          dynamic={true}
          freezeLeft={0}
          kb-interactive
          maxListVisibleRows={10}
        />
      </HX.Section>

      {/* Occupancy Guide */}
      <HX.Section title="Occupancy Detail" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Collection fields={["non_layer_perils/fire/occupancy_guide/industry_occupancy_dropdown/industry"]} />
          <HX.Collection fields={["non_layer_perils/fire/occupancy_guide/industry_occupancy_dropdown/occupancy"]} />
          <HX.Pane ratio={6} />
        </HX.Pane>
        <HX.Pane>
          <HX.Notes field={"non_layer_perils/fire/occupancy_guide/occupancy_description"} />
        </HX.Pane>
      </HX.Section>

      {/* Machinery Breakdown Section */}
      <HX.Section title="Machinery Breakdown">
        <InfoBox textNode="info/machinery_breakdown_msg" />
        <HX.Pane flow="right">
          <HX.Button task="machinery_breakdown_industry_task" title="Load Industries" />
          <HX.Pane ratio={3} />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Notes field={"non_layer_perils/fire/machinery_breakdown_message"} />
          <HX.Pane ratio={3} />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Table
            data={["machinery_breakdown"]}
            fields={[
              { field: "industry", width: 300 },
              { field: "tiv_contents", width: 150 },
              { field: "fire_mb_proportion", width: 150 }
            ]}
            kb-interactive
            with="non_layer_perils/fire"
          />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane flow="right">
          <HX.Collection fields={["non_layer_perils/fire/machinery_breakdown_sublimit"]} />
          <HX.Pane ratio={3} />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Run Simulation">
        <HX.Pane flow="right">
          <HX.Notes field="exposure_management_api/simulation_fetch_status" />
          <HX.Button title="Run Simulation" task="run_simulation_task" />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Run Rater">
        <HX.Pane flow="right">
          <HX.Notes field="schedule/large_schedule_workflow/run_rater_information" shownBy="policy_information/large_schedule_model" />
          <HX.Notes field="schedule/small_schedule_workflow/run_rater_information" shownBy="policy_information/small_schedule_model" />
          <HX.Pane>
            <HX.Button title="Run Rater" task="run_schedule_rater_task" />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Warnings/Messages" >
        {/* <HX.Notes field="schedule/debug" /> */}
        <HX.Notes field="schedule/schedule_warnings" />
      </HX.Section>

    </HX.Page>
  )
}

export { schedule };