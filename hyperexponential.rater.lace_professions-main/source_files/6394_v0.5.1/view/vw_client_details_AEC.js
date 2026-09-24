// v0.3.0
import * as HX from "hx-model-components";
import EditableText from "components/text_box_editable";
import { exposure_detail_years } from "view/vw_constants";

function vw_client_details_AEC(scale) {
  return (
    <HX.Page title="Client Details - AEC " shownBy="cds/profession_lawyers_bool_not" fullWidth={true} viewScale={scale}>
      <HX.Section title="Instructions" defaultCollapsed={false}>
        <HX.Notes field="cds/exposure/granular/client_details_AEC/notes" />
      </HX.Section>
      <HX.Section title="Individual Project Type" defaultCollapsed={false}>
        <HX.Collection fields={["client_details_AEC/bool_ipt_is_pcnt",
          "client_details_AEC/bool_ipt_enter_at_level",
          "client_details_AEC/weighted_pcnt_filter_value",
          "bool_show_inception_year_client_details_input",]} horizontal
          with="cds/exposure/granular" />

        <HX.Table
          data={[
            { datum: "client_details_AEC/individual_project_types/total" }
          ]}
          fields={[
            { field: "year_0_pcnt", width: 130, labelBy: "client_details_AEC/summary_year_total_ipt_labels/year_0", shownBy: "bool_show_inception_year_client_details_output_pcnt", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_pcnt", width: 130, labelBy: "client_details_AEC/summary_year_total_ipt_labels/year_1", shownBy: "client_details_AEC/bool_ipt_is_pcnt" },
            { field: "year_2_pcnt", width: 130, labelBy: "client_details_AEC/summary_year_total_ipt_labels/year_2", shownBy: "client_details_AEC/bool_ipt_is_pcnt" },
            { field: "year_3_pcnt", width: 130, labelBy: "client_details_AEC/summary_year_total_ipt_labels/year_3", shownBy: "client_details_AEC/bool_ipt_is_pcnt" },
            { field: "year_4_pcnt", width: 130, labelBy: "client_details_AEC/summary_year_total_ipt_labels/year_4", shownBy: "client_details_AEC/bool_ipt_is_pcnt" },
            { field: "year_5_pcnt", width: 130, labelBy: "client_details_AEC/summary_year_total_ipt_labels/year_5", shownBy: "client_details_AEC/bool_ipt_is_pcnt" },
            { field: "year_0_value", width: 130, labelBy: "client_details_AEC/summary_year_total_ipt_labels/year_0", shownBy: "bool_show_inception_year_client_details_output_value", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_value", width: 130, labelBy: "client_details_AEC/summary_year_total_ipt_labels/year_1", shownBy: "client_details_AEC/bool_ipt_is_pcnt_not" },
            { field: "year_2_value", width: 130, labelBy: "client_details_AEC/summary_year_total_ipt_labels/year_2", shownBy: "client_details_AEC/bool_ipt_is_pcnt_not" },
            { field: "year_3_value", width: 130, labelBy: "client_details_AEC/summary_year_total_ipt_labels/year_3", shownBy: "client_details_AEC/bool_ipt_is_pcnt_not" },
            { field: "year_4_value", width: 130, labelBy: "client_details_AEC/summary_year_total_ipt_labels/year_4", shownBy: "client_details_AEC/bool_ipt_is_pcnt_not" },
            { field: "year_5_value", width: 130, labelBy: "client_details_AEC/summary_year_total_ipt_labels/year_5", shownBy: "client_details_AEC/bool_ipt_is_pcnt_not" },
            null,
            { field: "weighted", width: 200 },
            null,
            { field: "expected_loss_cost", width: 200 }
            // { field: "frequency", width: 200 },
            // { field: "severity", width: 200 },

          ]}
          rowHeaderSettings={{ width: 380 }}
          with="cds/exposure/granular"
          dynamic={true}
          kb-interactive
        />
        <HX.Table
          shownBy="client_details_AEC/bool_ipt_enter_at_level"
          title="Please enter by project location:"
          data={[
            { datum: "client_details_AEC/individual_project_types/airport_runways" },
            { datum: "client_details_AEC/individual_project_types/arenas_stadiums_convention_centers" },
            { datum: "client_details_AEC/individual_project_types/bridges_tunnels" },
            { datum: "client_details_AEC/individual_project_types/chemical_pharmaceutical_plants" },
            { datum: "client_details_AEC/individual_project_types/dams_harbours_jetties_wetland_mitigation" },
            { datum: "client_details_AEC/individual_project_types/hospitals" },
            { datum: "client_details_AEC/individual_project_types/mining" },
            { datum: "client_details_AEC/individual_project_types/modular_buildings" },
            { datum: "client_details_AEC/individual_project_types/oil_refineries_pipelines_powerplants" },
            { datum: "client_details_AEC/individual_project_types/parking_garages" },
            { datum: "client_details_AEC/individual_project_types/processing_treatment" },
            { datum: "client_details_AEC/individual_project_types/residential_buildings_high_rise" },
            { datum: "client_details_AEC/individual_project_types/warehouses_data_centres" },
            { datum: "client_details_AEC/individual_project_types/residential_buildings_low_rise" },

            { datum: "client_details_AEC/individual_project_types/institutional_lower_risk_output" },
            { datum: "client_details_AEC/individual_project_types/churches" },
            { datum: "client_details_AEC/individual_project_types/colleges_universities_schools" },
            { datum: "client_details_AEC/individual_project_types/convalescent_retirement_facilities" },
            { datum: "client_details_AEC/individual_project_types/correctional_facilities_jails" },
            { datum: "client_details_AEC/individual_project_types/courthouses" },
            { datum: "client_details_AEC/individual_project_types/institutional_other" },
            { datum: "client_details_AEC/individual_project_types/military" },

            { datum: "client_details_AEC/individual_project_types/recreational_lower_risk_output" },
            { datum: "client_details_AEC/individual_project_types/amusement_park" },
            { datum: "client_details_AEC/individual_project_types/casinos" },
            { datum: "client_details_AEC/individual_project_types/parks_playgrounds_pools" },
            { datum: "client_details_AEC/individual_project_types/recreational_other" },
            { datum: "client_details_AEC/individual_project_types/sports_facilities" },

            { datum: "client_details_AEC/individual_project_types/general_building_lower_risk_output" },
            { datum: "client_details_AEC/individual_project_types/airport_terminals" },
            { datum: "client_details_AEC/individual_project_types/general_building_other" },
            { datum: "client_details_AEC/individual_project_types/hotels_motels" },
            { datum: "client_details_AEC/individual_project_types/libraries_museums" },
            { datum: "client_details_AEC/individual_project_types/offices" },
            { datum: "client_details_AEC/individual_project_types/retail_malls_shopping_centers_restaurants" },

            { datum: "client_details_AEC/individual_project_types/infrastructure_lower_risk_output" },
            { datum: "client_details_AEC/individual_project_types/infrastructure_other" },
            { datum: "client_details_AEC/individual_project_types/rail" },
            { datum: "client_details_AEC/individual_project_types/roads" },
            { datum: "client_details_AEC/individual_project_types/utilities" },

            { datum: "client_details_AEC/individual_project_types/industrial_lower_risk_output" },
            { datum: "client_details_AEC/individual_project_types/industrial_other" },
            { datum: "client_details_AEC/individual_project_types/manufacturing_facilities" },
            { datum: "client_details_AEC/individual_project_types/nuclear_facilities" },

            { datum: "client_details_AEC/individual_project_types/environmental_lower_risk_output" },
            { datum: "client_details_AEC/individual_project_types/asbestos_abatement" },
            { datum: "client_details_AEC/individual_project_types/environmental_other" },
            { datum: "client_details_AEC/individual_project_types/waste_brokering" }
          ]}
          fields={[
            { field: "year_0_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_0", shownBy: "bool_show_inception_year_client_details_output_pcnt", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_1", shownBy: "client_details_AEC/bool_ipt_is_pcnt" },
            { field: "year_2_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_2", shownBy: "client_details_AEC/bool_ipt_is_pcnt" },
            { field: "year_3_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_3", shownBy: "client_details_AEC/bool_ipt_is_pcnt" },
            { field: "year_4_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_4", shownBy: "client_details_AEC/bool_ipt_is_pcnt" },
            { field: "year_5_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_5", shownBy: "client_details_AEC/bool_ipt_is_pcnt" },
            { field: "year_0_value", width: 130, labelBy: "territory/summary_year_labels/year_0", shownBy: "bool_show_inception_year_client_details_output_value", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_value", width: 130, labelBy: "territory/summary_year_labels/year_1", shownBy: "client_details_AEC/bool_ipt_is_pcnt_not" },
            { field: "year_2_value", width: 130, labelBy: "territory/summary_year_labels/year_2", shownBy: "client_details_AEC/bool_ipt_is_pcnt_not" },
            { field: "year_3_value", width: 130, labelBy: "territory/summary_year_labels/year_3", shownBy: "client_details_AEC/bool_ipt_is_pcnt_not" },
            { field: "year_4_value", width: 130, labelBy: "territory/summary_year_labels/year_4", shownBy: "client_details_AEC/bool_ipt_is_pcnt_not" },
            { field: "year_5_value", width: 130, labelBy: "territory/summary_year_labels/year_5", shownBy: "client_details_AEC/bool_ipt_is_pcnt_not" },
            null,
            { field: "weighted", width: 200 },
            null,
            { field: "frequency", width: 200 },
            { field: "severity", width: 200 },
          ]}
          rowHeaderSettings={{ width: 380 }}
          with="cds/exposure/granular"
          dynamic
          filter={"filter"}
          kb-interactive
        />
        <HX.Table
          shownBy="client_details_AEC/bool_ipt_enter_at_level_not"
          title="Please enter by project location:"
          data={[
            { datum: "client_details_AEC/individual_project_types/airport_runways" },
            { datum: "client_details_AEC/individual_project_types/arenas_stadiums_convention_centers" },
            { datum: "client_details_AEC/individual_project_types/bridges_tunnels" },
            { datum: "client_details_AEC/individual_project_types/chemical_pharmaceutical_plants" },
            { datum: "client_details_AEC/individual_project_types/dams_harbours_jetties_wetland_mitigation" },
            { datum: "client_details_AEC/individual_project_types/hospitals" },
            { datum: "client_details_AEC/individual_project_types/mining" },
            { datum: "client_details_AEC/individual_project_types/modular_buildings" },
            { datum: "client_details_AEC/individual_project_types/oil_refineries_pipelines_powerplants" },
            { datum: "client_details_AEC/individual_project_types/parking_garages" },
            { datum: "client_details_AEC/individual_project_types/processing_treatment" },
            { datum: "client_details_AEC/individual_project_types/residential_buildings_high_rise" },
            { datum: "client_details_AEC/individual_project_types/warehouses_data_centres" },
            { datum: "client_details_AEC/individual_project_types/residential_buildings_low_rise" },
            { datum: "client_details_AEC/individual_project_types/institutional_lower_risk_input" },
            { datum: "client_details_AEC/individual_project_types/recreational_lower_risk_input" },
            { datum: "client_details_AEC/individual_project_types/general_building_lower_risk_input" },
            { datum: "client_details_AEC/individual_project_types/infrastructure_lower_risk_input" },
            { datum: "client_details_AEC/individual_project_types/industrial_lower_risk_input" },
            { datum: "client_details_AEC/individual_project_types/environmental_lower_risk_input" },
          ]}
          fields={[
            { field: "year_0_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_0", shownBy: "bool_show_inception_year_client_details_output_pcnt", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_1", shownBy: "client_details_AEC/bool_ipt_is_pcnt" },
            { field: "year_2_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_2", shownBy: "client_details_AEC/bool_ipt_is_pcnt" },
            { field: "year_3_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_3", shownBy: "client_details_AEC/bool_ipt_is_pcnt" },
            { field: "year_4_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_4", shownBy: "client_details_AEC/bool_ipt_is_pcnt" },
            { field: "year_5_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_5", shownBy: "client_details_AEC/bool_ipt_is_pcnt" },
            { field: "year_0_value", width: 130, labelBy: "territory/summary_year_labels/year_0", shownBy: "bool_show_inception_year_client_details_output_value", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_value", width: 130, labelBy: "territory/summary_year_labels/year_1", shownBy: "client_details_AEC/bool_ipt_is_pcnt_not" },
            { field: "year_2_value", width: 130, labelBy: "territory/summary_year_labels/year_2", shownBy: "client_details_AEC/bool_ipt_is_pcnt_not" },
            { field: "year_3_value", width: 130, labelBy: "territory/summary_year_labels/year_3", shownBy: "client_details_AEC/bool_ipt_is_pcnt_not" },
            { field: "year_4_value", width: 130, labelBy: "territory/summary_year_labels/year_4", shownBy: "client_details_AEC/bool_ipt_is_pcnt_not" },
            { field: "year_5_value", width: 130, labelBy: "territory/summary_year_labels/year_5", shownBy: "client_details_AEC/bool_ipt_is_pcnt_not" },
            null,
            { field: "weighted", width: 200 },
            null,
            { field: "frequency", width: 200 },
            { field: "severity", width: 200 },
          ]}
          rowHeaderSettings={{ width: 380 }}
          with="cds/exposure/granular"
          dynamic
          kb-interactive
        />
      </HX.Section>
      {/* <HX.Section title="Chart - Loss Cost by Project Type" defaultCollapsed={false}>
        <HX.CategoryChart
          data={[
            "residential_lower_risk",
            "residential_higher_risk",
            "institutional_lower_risk_output",
            "recreational_lower_risk_output",
            "general_building_lower_risk_output",
            "infrastructure_lower_risk_output",
            "industrial_lower_risk_output",
            "environmental_lower_risk_output"]}
          fields={["expected_loss_cost"]}
          columnType="cluster"
          with="cds/exposure/granular/client_details_AEC/individual_project_types_chart"
        />
      </HX.Section> */}
      <HX.Section title="Areas of Practice" defaultCollapsed={false}>
        <HX.Collection fields={[
          "cds/exposure/granular/client_details_AEC/bool_aop_is_pcnt",
          "cds/exposure/granular/bool_show_inception_year_client_details_input",
          null,
          null]} horizontal />
        <HX.Table
          data={[
            { datum: "client_details_AEC/areas_of_practice_total", }
          ]}
          fields={[
            { field: "year_0_pcnt", width: 130, labelBy: "client_details_AEC/summary_year_total_aop_labels/year_0", shownBy: "bool_show_inception_year_client_details_output_pcnt", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_pcnt", width: 130, labelBy: "client_details_AEC/summary_year_total_aop_labels/year_1", shownBy: "client_details_AEC/bool_aop_is_pcnt" },
            { field: "year_2_pcnt", width: 130, labelBy: "client_details_AEC/summary_year_total_aop_labels/year_2", shownBy: "client_details_AEC/bool_aop_is_pcnt" },
            { field: "year_3_pcnt", width: 130, labelBy: "client_details_AEC/summary_year_total_aop_labels/year_3", shownBy: "client_details_AEC/bool_aop_is_pcnt" },
            { field: "year_4_pcnt", width: 130, labelBy: "client_details_AEC/summary_year_total_aop_labels/year_4", shownBy: "client_details_AEC/bool_aop_is_pcnt" },
            { field: "year_5_pcnt", width: 130, labelBy: "client_details_AEC/summary_year_total_aop_labels/year_5", shownBy: "client_details_AEC/bool_aop_is_pcnt" },
            { field: "year_0_value", width: 130, labelBy: "client_details_AEC/summary_year_total_aop_labels/year_0", shownBy: "bool_show_inception_year_client_details_output_value", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_value", width: 130, labelBy: "client_details_AEC/summary_year_total_aop_labels/year_1", shownBy: "client_details_AEC/bool_aop_is_pcnt_not" },
            { field: "year_2_value", width: 130, labelBy: "client_details_AEC/summary_year_total_aop_labels/year_2", shownBy: "client_details_AEC/bool_aop_is_pcnt_not" },
            { field: "year_3_value", width: 130, labelBy: "client_details_AEC/summary_year_total_aop_labels/year_3", shownBy: "client_details_AEC/bool_aop_is_pcnt_not" },
            { field: "year_4_value", width: 130, labelBy: "client_details_AEC/summary_year_total_aop_labels/year_4", shownBy: "client_details_AEC/bool_aop_is_pcnt_not" },
            { field: "year_5_value", width: 130, labelBy: "client_details_AEC/summary_year_total_aop_labels/year_5", shownBy: "client_details_AEC/bool_aop_is_pcnt_not" },
            null,
            { field: "weighted", width: 130 },
            null,
            { field: "elc", width: 200 }
            // { field: "frequency", width: 200 },
            // { field: "severity", width: 200 },
          ]}
          rowHeaderSettings={{ width: 380 }}
          with="cds/exposure/granular"
          dynamic={true}
          kb-interactive
        />
        <HX.Table
          data={[
            {
              datum: "client_details_AEC/areas_of_practice",
              elementLabelBy: "areas_of_practice",
            }
          ]}
          fields={[
            { field: "year_0_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_0", shownBy: "bool_show_inception_year_client_details_output_pcnt", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_1", shownBy: "client_details_AEC/bool_aop_is_pcnt" },
            { field: "year_2_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_2", shownBy: "client_details_AEC/bool_aop_is_pcnt" },
            { field: "year_3_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_3", shownBy: "client_details_AEC/bool_aop_is_pcnt" },
            { field: "year_4_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_4", shownBy: "client_details_AEC/bool_aop_is_pcnt" },
            { field: "year_5_pcnt", width: 130, labelBy: "territory/summary_year_labels/year_5", shownBy: "client_details_AEC/bool_aop_is_pcnt" },
            { field: "year_0_value", width: 130, labelBy: "territory/summary_year_labels/year_0", shownBy: "bool_show_inception_year_client_details_output_value", infoBy: "/cds/hover_info/territory_policy_year" },
            { field: "year_1_value", width: 130, labelBy: "territory/summary_year_labels/year_1", shownBy: "client_details_AEC/bool_aop_is_pcnt_not" },
            { field: "year_2_value", width: 130, labelBy: "territory/summary_year_labels/year_2", shownBy: "client_details_AEC/bool_aop_is_pcnt_not" },
            { field: "year_3_value", width: 130, labelBy: "territory/summary_year_labels/year_3", shownBy: "client_details_AEC/bool_aop_is_pcnt_not" },
            { field: "year_4_value", width: 130, labelBy: "territory/summary_year_labels/year_4", shownBy: "client_details_AEC/bool_aop_is_pcnt_not" },
            { field: "year_5_value", width: 130, labelBy: "territory/summary_year_labels/year_5", shownBy: "client_details_AEC/bool_aop_is_pcnt_not" },
            null,
            { field: "weighted", width: 130 },
            null,
            { field: "frequency", width: 200 },
            { field: "severity", width: 200 },
          ]}
          rowHeaderSettings={{ width: 380 }}
          with="cds/exposure/granular"
          dynamic
          kb-interactive
        />
      </HX.Section>
      {/* <HX.Section title="Chart - Loss Cost by Area Of Practice" defaultCollapsed={false}>
        <HX.CategoryChart
          data={[
            "architecture",
            "architecture_interior_design",
            "civil",
            "construction_management",
            "environmental",
            "geotech",
            "mep",
            "other_low_risk",
            "process_engineering",
            "structural",
            "surveyor"
          ]}
          fields={["expected_loss_cost"]}
          columnType="cluster"
          with="cds/exposure/granular/client_details_AEC/areas_of_practice_chart"
        />
      </HX.Section> */}
      <HX.Section title="Client Specifics" defaultCollapsed={false}>
        <HX.Collection fields={["cds/exposure/granular/client_details_AEC/size_of_matters", null]} horizontal />
        <EditableText textNode="cds/exposure/granular/client_details_AEC/uw_comments" placeholderText="Underwriter Comments" />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_client_details_AEC };