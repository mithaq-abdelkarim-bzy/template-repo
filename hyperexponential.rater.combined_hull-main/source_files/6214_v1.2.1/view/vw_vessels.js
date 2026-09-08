import * as HX from "hx-model-components";
import { get_inputs_section, get_default_section } from "view/common";

function vw_vessels(scale) {
  disable_behavioural_feilds = [
    {
      field: "number_of_port_visits.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "number_of_unique_port_visits.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "age.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_antarctica.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_australia_and_new_zealand.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_eastern_asia.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_eastern_europe.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_high_seas.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_latin_america_and_caribbean.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_melanesia.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_micronesia.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_northern_africa.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_northern_america.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_northern_europe.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_polynesia.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_south_eastern_asia.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_southern_asia.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_southern_europe.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_sub_saharan_africa.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_western_asia.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_western_europe.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "change_in_fleet.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_class_changes_5yr.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "model_dwt.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "model_flag.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "model_gross_tonnage.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "max_distance_ratio.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "net_sum_insured.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "num_journeys_cut.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "num_port_visits_cut.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "perc_time_eez.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "perc_time_hrz.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "perc_time_seca.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "powerkwmax.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "ratio_anchored.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "ratio_moored.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "ratio_moving.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "total_unique_imos_owner.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "unique_journey_ratio.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "unique_port_ratio.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "ship_type.read_only_option",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "current_flag",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "model_ship_name",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "raw_deadweight",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "year_of_build",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "raw_grosstonnage",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "raw_ship_type",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_behavioural_data",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "mapped_vessel_type",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
  ]
  enable_behavioural_feilds = [
    {
      field: "number_of_port_visits",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "number_of_unique_port_visits",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "age",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_antarctica",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_australia_and_new_zealand",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_eastern_asia",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_eastern_europe",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_high_seas",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_latin_america_and_caribbean",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_melanesia",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_micronesia",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_northern_africa",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_northern_america",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_northern_europe",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_polynesia",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_south_eastern_asia",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_southern_asia",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_southern_europe",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_sub_saharan_africa",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_western_asia",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_aths_western_europe",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "change_in_fleet",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_class_changes_5yr",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "model_dwt",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "model_flag",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "model_gross_tonnage",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "max_distance_ratio",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "net_sum_insured",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "num_journeys_cut",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "num_port_visits_cut",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "perc_time_eez",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "perc_time_hrz",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "perc_time_seca",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "powerkwmax",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "ratio_anchored",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "ratio_moored",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "ratio_moving",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "total_unique_imos_owner",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "unique_journey_ratio",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "unique_port_ratio",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "ship_type",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "current_flag",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "model_ship_name",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "raw_deadweight",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "year_of_build",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "raw_grosstonnage",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "raw_ship_type",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "is_behavioural_data",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
    {
      field: "mapped_vessel_type",
      shownBy: "/non_cds/show_hide_toggles/hull/show_vessels_details",
    },
  ]

  standard_vessel_fields = [
    "vessel_details/imo",
    {
      field: "vessel_details/name",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/name",
    },
    {
      field: "error_validation_columns/validation_name",
      labelBy: "/non_cds/labels/hull/validation_name",
      shownBy: "/non_cds/show_hide_toggles/hull/filter_by_errors",
    },
    {
      field: "inception_date",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/inception_date",
    },
    {
      field: "error_validation_columns/validation_inception_date",
      labelBy: "/non_cds/labels/hull/validation_inception_date",
      shownBy: "/non_cds/show_hide_toggles/hull/filter_by_errors",
    },
    {
      field: "expiry_date",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/expiry_date",
    },
    {
      field: "error_validation_columns/validation_expiry_date",
      labelBy: "/non_cds/labels/hull/validation_expiry_date",
      shownBy: "/non_cds/show_hide_toggles/hull/filter_by_errors",
    },
    {
      field: "coverage",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/coverage",
    },
    {
      field: "error_validation_columns/validation_coverage",
      labelBy: "/non_cds/labels/hull/validation_coverage",
      shownBy: "/non_cds/show_hide_toggles/hull/filter_by_errors",
    },
    {
      field: "vessel_type",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/vessel_type",
    },
    {
      field: "error_validation_columns/validation_vessel_type",
      labelBy: "/non_cds/labels/hull/validation_vessel_type",
      shownBy: "/non_cds/show_hide_toggles/hull/filter_by_errors",
    },
    {
      field: "agreed_value",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/agreed_value",
    },
    {
      field: "error_validation_columns/validation_agreed_value",
      labelBy: "/non_cds/labels/hull/validation_agreed_value",
      shownBy: "/non_cds/show_hide_toggles/hull/filter_by_errors",
    },
    {
      field: "vessel_details/gross_tonnage",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/gross_tonnage",
    },
    {
      field: "error_validation_columns/validation_gross_tonnage",
      labelBy: "/non_cds/labels/hull/validation_gross_tonnage",
      shownBy: "/non_cds/show_hide_toggles/hull/filter_by_errors",
    },
    {
      field: "dwt",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/dwt",
    },
    {
      field: "error_validation_columns/validation_dwt",
      labelBy: "/non_cds/labels/hull/validation_dwt",
      shownBy: "/non_cds/show_hide_toggles/hull/filter_by_errors",
    },
    {
      field: "year_built",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/year_built",
    },
    {
      field: "error_validation_columns/validation_year_built",
      labelBy: "/non_cds/labels/hull/validation_year_built",
      shownBy: "/non_cds/show_hide_toggles/hull/filter_by_errors",
    },
    {
      field: "flag",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/flag",
    },
    {
      field: "error_validation_columns/validation_flag",
      labelBy: "/non_cds/labels/hull/validation_flag",
      shownBy: "/non_cds/show_hide_toggles/hull/filter_by_errors",
    },
    {
      field: "vessel_details/vessel_class",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/vessel_class",
    },
    {
      field: "error_validation_columns/validation_vessel_class",
      labelBy: "/non_cds/labels/hull/validation_vessel_class",
      shownBy: "/non_cds/show_hide_toggles/hull/filter_by_errors",
    },
    {
      field: "deductible",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/deductible",
    },
    {
      field: "error_validation_columns/validation_deductible",
      labelBy: "/non_cds/labels/hull/validation_deductible",
      shownBy: "/non_cds/show_hide_toggles/hull/filter_by_errors",
    },
    {
      field: "vessel_details/order_percent",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/order_percent",
    },
    {
      field: "error_validation_columns/validation_order_percent",
      labelBy: "/non_cds/labels/hull/validation_order_percent",
      shownBy: "/non_cds/show_hide_toggles/hull/filter_by_errors",
    },
    {
      field: "vessel_details/freight_conditions",
      labelBy:
        "/non_cds/labels/required_vessels_columns_labels/freight_conditions",
    },
    {
      field: "error_validation_columns/validation_freight_conditions",
      labelBy: "/non_cds/labels/hull/validation_freight_conditions",
      shownBy: "/non_cds/show_hide_toggles/hull/filter_by_errors",
    },
    {
      field: "vessel_details/vessel_quality",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/vessel_quality",
    },
    {
      field: "error_validation_columns/validation_vessel_quality",
      labelBy: "/non_cds/labels/hull/validation_vessel_quality",
      shownBy: "/non_cds/show_hide_toggles/hull/filter_by_errors",
    },
    {
      field: "vessel_details/area_of_operation",
      labelBy:
        "/non_cds/labels/required_vessels_columns_labels/area_of_operation",
    },
    {
      field: "error_validation_columns/validation_area_of_operation",
      labelBy: "/non_cds/labels/hull/validation_area_of_operation",
      shownBy: "/non_cds/show_hide_toggles/hull/filter_by_errors",
    },
    "behavioural_model_rate",
    {
      field: "behavioural_benchmark_premium",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/behavioural_benchmark_premium",
    },
    "static_model_rate",
    {
      field: "static_benchmark_premium",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/static_benchmark_premium",
    },

    {
      field: "achieved_rate",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/achieved_rate",
    },
    {
      field: "error_validation_columns/validation_achieved_rate",
      labelBy: "/non_cds/labels/hull/validation_achieved_rate",
      shownBy: "/non_cds/show_hide_toggles/hull/filter_by_errors",
    },
    {
      field: "achieved_premium",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/achieved_premium",
    },
    {
      field: "average_achieved_rate",
      shownBy: "/cds/exposure/granular/vessels/hull_rating/is_modelling",
    },
    "uw_adjustment"
  ]

  const vessels_fields_with_behavioural = standard_vessel_fields.concat(enable_behavioural_feilds);

  const vessels_fields_without_behavioural = standard_vessel_fields.concat(disable_behavioural_feilds);


  return (
    <HX.Page
      title="Vessels"
      fullWidth
      shownBy="/non_cds/show_hide_toggles/hull/show_hull_coverage"
    >
      {get_inputs_section("hull")}
      <HX.Section title="Fleet Soft Factors">
        <HX.With
          context={{
            type: "struct",
            path: "cds/exposure/granular/vessels/hull_rating/fleet_soft_factors",
          }}
        >
          <HX.Pane flow="right">
            <HX.Collection
              fields={["fleet_casualty_history", "owner_quality"]}
              horizontal
            />
            <HX.Pane />
          </HX.Pane>
        </HX.With>
      </HX.Section>
      {get_default_section("hull")}
      <HX.Section title="Vessels">
        <HX.Pane flow="down">
          <HX.Pane flow="right" reflow={false}>
            <HX.Pane flow="down" ratio={3}>
              <HX.Button
                task={"clear_vessels_task"}
                title="Clear Vessels Table"
              />
              <HX.Collection
                fields={[
                  "/non_cds/show_hide_toggles/hull/show_vessels_details",
                  "cds/exposure/granular/vessels/hull_rating/fleet_size",
                ]}
              />
            </HX.Pane>
            <HX.Pane flow="down" ratio={3}>
              <HX.Button task={"lookup_imos_task"} title="Lookup IMOs" />
              <HX.Collection
                fields={["/non_cds/show_hide_toggles/hull/filter_by_errors"]}
              />
            </HX.Pane>
            <HX.Pane flow="down" ratio={4}>
              <HX.With
                context={{
                  type: "list",
                  index: 0,
                  path: "/cds/layers",
                }}
              >
                <HX.Collection
                  fields={["coverages/hull/total_quoted_premium"]}
                />
              </HX.With>
              <HX.Collection
                fields={[
                  "/non_cds/labels/hull/validation_error_message",
                  {
                    field:
                      "/non_cds/labels/hull/data_mart_warning_message.read_only_option",
                    shownBy:
                      "/non_cds/show_hide_toggles/hull/show_data_mart_warning",
                  },
                  {
                    field:
                      "/non_cds/labels/hull/duplicate_imo_and_name_message.read_only_option",
                    shownBy:
                      "/non_cds/show_hide_toggles/hull/show_duplicate_vessel_warning",
                  }
                ]}
              />
            </HX.Pane>
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.With
            context={{
              type: "list",
              path: "cds/exposure/granular/vessels/hull_rating/vessels_list",
              index: 0,
            }}
          >
            <HX.Table
              maxListVisibleRows={30}
              filter={"has_error"}
              data={["/cds/exposure/granular/vessels/hull_rating/vessels_list"]}
              fields={vessels_fields_with_behavioural}
              kb-interactive
              freezeLeft={2}
              shownBy="/non_cds/show_hide_toggles/hull/filter_by_errors"
            />
            <HX.Table
              maxListVisibleRows={30}
              data={["/cds/exposure/granular/vessels/hull_rating/vessels_list"]}
              fields={vessels_fields_with_behavioural}
              kb-interactive
              freezeLeft={2}
              shownBy="/non_cds/show_hide_toggles/hull/not_filter_by_errors"
            />
          </HX.With>
          <HX.Pane>
            <HX.Collection
              fields={[{ field: "/non_cds/labels/mismatched_inception_year_warning.warning_option", shownBy: "/non_cds/show_hide_toggles/show_mismatched_inception_year_warning" }]}
            />
          </HX.Pane>
          <HX.Pane flow="right" shownBy="/non_cds/show_hide_toggles/show_powersearch">
            <HX.Button
              task={"generate_vessels_xlsx_task"}
              title="Generate Vessels Excel"
            />
            <HX.File
              field="/cds/exposure/granular/vessels/hull_rating/vessels_xlsx"
              shownBy="/non_cds/show_hide_toggles/hull/show_generated_vessels_xlsx"
            />
            <HX.Button
              task={"push_vessels_to_datamart_task"}
              title="Push to Powersearch"
            />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  );
}

export { vw_vessels };
