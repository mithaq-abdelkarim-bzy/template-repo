import * as HX from "hx-model-components";
import { get_vessel_details, get_inputs_section } from "view/common";

function vw_war(scale) {
  const read_only_suffix = ".read_only_option";
  const war_prefix = "war/war_";
  const war_validation_prefix =
    "war/war_error_validation_columns/validation_war_";
  const vessel_details_prefix = "vessel_details/";
  const war_vessels_fields = [
    vessel_details_prefix + "imo" + read_only_suffix,
    vessel_details_prefix + "name" + read_only_suffix,
    {
      field: "inception_date" + read_only_suffix,
      shownBy: "/non_cds/show_hide_toggles/war/war_show_vessel_details",
    },
    {
      field: "expiry_date" + read_only_suffix,
      shownBy: "/non_cds/show_hide_toggles/war/war_show_vessel_details",
    },
    war_prefix + "coverage",
    {
      field: war_validation_prefix + "coverage",
      shownBy: "/non_cds/show_hide_toggles/war/war_filter_by_errors",
      labelBy: "/non_cds/labels/war/validation_war_coverage",
    },
    "vessel_type" + read_only_suffix,
    {
      field: war_prefix + "agreed_value",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/agreed_value",
    },
    {
      field: war_validation_prefix + "agreed_value",
      shownBy: "/non_cds/show_hide_toggles/war/war_filter_by_errors",
      labelBy: "/non_cds/labels/war/validation_war_agreed_value",
    },
    vessel_details_prefix + "gross_tonnage" + read_only_suffix,
    "dwt" + read_only_suffix,
    "year_built" + read_only_suffix,
    {
      field: "flag" + read_only_suffix,
      shownBy: "/non_cds/show_hide_toggles/war/war_show_vessel_details",
    },
    {
      field: vessel_details_prefix + "vessel_class" + read_only_suffix,
      shownBy: "/non_cds/show_hide_toggles/war/war_show_vessel_details",
    },
    {
      field: vessel_details_prefix + "order_percent" + read_only_suffix,
      shownBy: "/non_cds/show_hide_toggles/war/war_show_vessel_details",
    },
    {
      field: vessel_details_prefix + "freight_conditions" + read_only_suffix,
      shownBy: "/non_cds/show_hide_toggles/war/war_show_vessel_details",
    },
    {
      field: vessel_details_prefix + "vessel_quality" + read_only_suffix,
      shownBy: "/non_cds/show_hide_toggles/war/war_show_vessel_details",
    },
    {
      field: vessel_details_prefix + "area_of_operation" + read_only_suffix,
      shownBy: "/non_cds/show_hide_toggles/war/war_show_vessel_details",
    },
    {
      field: war_prefix + "behavioural_model_rate",
      shownBy: "/non_cds/show_hide_toggles/war/war_show_vessel_details",
    },
    {
      field: war_prefix + "behavioural_benchmark_premium",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/behavioural_benchmark_premium",
      shownBy: "/non_cds/show_hide_toggles/iv/iv_show_vessel_details",
    },
    {
      field: war_prefix + "static_model_rate",
      shownBy: "/non_cds/show_hide_toggles/war/war_show_vessel_details",
    },
    {
      field: war_prefix + "static_benchmark_premium",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/static_benchmark_premium",
      shownBy: "/non_cds/show_hide_toggles/iv/iv_show_vessel_details",
    },
    war_prefix + "achieved_rate",
    {
      field: war_validation_prefix + "achieved_rate",
      shownBy: "/non_cds/show_hide_toggles/war/war_filter_by_errors",
      labelBy: "/non_cds/labels/war/validation_war_achieved_rate",
    },
    {
      field: war_prefix + "achieved_premium",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/achieved_premium",
    },
    war_prefix + "uw_adjustment",
    {
      field: war_prefix + "benchmark_premium",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/war_benchmark_premium",
    },
    war_prefix + "is_include_vessel",
  ];
  return (
    <HX.Page
      title="War"
      fullWidth
      shownBy="/non_cds/show_hide_toggles/war/show_war_coverage"
    >
      <HX.With
        context={{
          type: "struct",
          path: "cds/exposure/granular/vessels/hull_rating",
        }}
      >
        <HX.Section title="War Coverage">
          {get_inputs_section("war")}
          <HX.Section title="War Vessels List">
            <HX.Pane flow="down">
              <HX.Pane flow="right">
                <HX.With
                  context={{
                    type: "list",
                    index: 0,
                    path: "/cds/layers",
                  }}
                >
                  <HX.Collection
                    fields={[
                      "/non_cds/show_hide_toggles/war/war_show_vessel_details",
                      "coverages/war/total_quoted_premium",
                    ]}
                    horizontal
                  />
                </HX.With>
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection
                  fields={[
                    "/non_cds/show_hide_toggles/war/war_filter_by_errors",
                    "/non_cds/labels/war/validation_war_error_message",
                    {
                      field:
                        "/non_cds/labels/hull/data_mart_warning_message.read_only_option",
                      shownBy:
                        "/non_cds/show_hide_toggles/hull/show_data_mart_warning",
                    },
                  ]}
                  horizontal
                />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Table
                data={["vessels_list"]}
                fields={war_vessels_fields}
                title="Vessels"
                kb-interactive
                freezeRight={1}
                dynamic
                shownBy="/non_cds/show_hide_toggles/war/war_not_filter_by_errors"
              />
              <HX.Table
                data={["vessels_list"]}
                fields={war_vessels_fields}
                title="Vessels"
                kb-interactive
                freezeRight={1}
                dynamic
                shownBy="/non_cds/show_hide_toggles/war/war_filter_by_errors"
                filter={"war/war_has_error"}
              />
              <HX.Pane>
                <HX.Collection
                  fields={[{
                    field: "/non_cds/labels/mismatched_inception_year_warning.warning_option",
                    shownBy: "/non_cds/show_hide_toggles/show_mismatched_inception_year_warning"
                  }]}
                />
              </HX.Pane>
              <HX.Pane flow="right" shownBy="/non_cds/show_hide_toggles/show_powersearch">
                <HX.Button
                  task={"push_vessels_to_datamart_task"}
                  title="Push to Powersearch"
                />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.Section>
      </HX.With>
    </HX.Page>
  );
}

export { vw_war };
