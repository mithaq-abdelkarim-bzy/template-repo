import * as HX from "hx-model-components";
import { get_vessel_details, get_inputs_section } from "view/common";

function vw_iv(scale) {
  const read_only_suffix = ".read_only_option";
  const iv_prefix = "iv/iv_";
  const iv_validation_prefix = "iv/iv_error_validation_columns/validation_iv_";
  const vessel_details_prefix = "vessel_details/";
  const iv_vessels_fields = [
    vessel_details_prefix + "imo" + read_only_suffix,
    vessel_details_prefix + "name" + read_only_suffix,
    {
      field: "inception_date" + read_only_suffix,
      shownBy: "/non_cds/show_hide_toggles/iv/iv_show_vessel_details",
    },
    {
      field: "expiry_date" + read_only_suffix,
      shownBy: "/non_cds/show_hide_toggles/iv/iv_show_vessel_details",
    },
    iv_prefix + "coverage",
    {
      field: iv_validation_prefix + "coverage",
      shownBy: "/non_cds/show_hide_toggles/iv/iv_filter_by_errors",
      labelBy: "/non_cds/labels/iv/validation_iv_coverage",
    },
    "vessel_type" + read_only_suffix,
    {
      field: iv_prefix + "agreed_value",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/agreed_value",
    },
    {
      field: iv_validation_prefix + "agreed_value",
      shownBy: "/non_cds/show_hide_toggles/iv/iv_filter_by_errors",
      labelBy: "/non_cds/labels/iv/validation_iv_agreed_value",
    },
    vessel_details_prefix + "gross_tonnage" + read_only_suffix,
    "dwt" + read_only_suffix,
    "year_built" + read_only_suffix,
    {
      field: "flag" + read_only_suffix,
      shownBy: "/non_cds/show_hide_toggles/iv/iv_show_vessel_details",
    },
    {
      field: vessel_details_prefix + "vessel_class" + read_only_suffix,
      shownBy: "/non_cds/show_hide_toggles/iv/iv_show_vessel_details",
    },
    {
      field: iv_prefix + "deductible",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/deductible",
    },
    {
      field: vessel_details_prefix + "order_percent" + read_only_suffix,
      shownBy: "/non_cds/show_hide_toggles/iv/iv_show_vessel_details",
    },
    {
      field: vessel_details_prefix + "freight_conditions" + read_only_suffix,
      shownBy: "/non_cds/show_hide_toggles/iv/iv_show_vessel_details",
    },
    {
      field: vessel_details_prefix + "vessel_quality" + read_only_suffix,
      shownBy: "/non_cds/show_hide_toggles/iv/iv_show_vessel_details",
    },
    {
      field: vessel_details_prefix + "area_of_operation" + read_only_suffix,
      shownBy: "/non_cds/show_hide_toggles/iv/iv_show_vessel_details",
    },
    {
      field: iv_prefix + "behavioural_model_rate",
      shownBy: "/non_cds/show_hide_toggles/iv/iv_show_vessel_details",
    },
    {
      field: iv_prefix + "behavioural_benchmark_premium",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/behavioural_benchmark_premium",
      shownBy: "/non_cds/show_hide_toggles/iv/iv_show_vessel_details",
    },
    {
      field: iv_prefix + "static_model_rate",
      shownBy: "/non_cds/show_hide_toggles/iv/iv_show_vessel_details",
    },
    {
      field: iv_prefix + "static_benchmark_premium",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/static_benchmark_premium",
      shownBy: "/non_cds/show_hide_toggles/iv/iv_show_vessel_details",
    },
    iv_prefix + "achieved_rate",
    {
      field: iv_validation_prefix + "achieved_rate",
      shownBy: "/non_cds/show_hide_toggles/iv/iv_filter_by_errors",
      labelBy: "/non_cds/labels/iv/validation_iv_achieved_rate",
    },
    {
      field: iv_prefix + "achieved_premium",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/achieved_premium",
    },
    iv_prefix + "uw_adjustment",
    {
      field: iv_prefix + "benchmark_premium",
      labelBy: "/non_cds/labels/required_vessels_columns_labels/iv_benchmark_premium",
    },
    iv_prefix + "is_include_vessel",
  ];
  return (
    <HX.Page
      title="IV"
      fullWidth
      shownBy="/non_cds/show_hide_toggles/iv/show_iv_coverage"
    >
      <HX.With
        context={{
          type: "struct",
          path: "cds/exposure/granular/vessels/hull_rating",
        }}
      >
        <HX.Section title="IV Coverage">
          {get_inputs_section("iv")}
          <HX.Section title="IV Vessels List">
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
                      "/non_cds/show_hide_toggles/iv/iv_show_vessel_details",
                      "coverages/iv/iv_perc_of_h_and_m_value",
                      "coverages/iv/total_quoted_premium",
                    ]}
                    syncColumnWidthsKey="key_1"
                    horizontal
                  />
                </HX.With>
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection
                  fields={[
                    "/non_cds/show_hide_toggles/iv/iv_filter_by_errors",
                    "/non_cds/labels/iv/validation_iv_error_message",
                    {
                      field:
                        "/non_cds/labels/hull/data_mart_warning_message.read_only_option",
                      shownBy:
                        "/non_cds/show_hide_toggles/hull/show_data_mart_warning",
                    },
                  ]}
                  syncColumnWidthsKey="key_1"
                  horizontal
                />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Table
                data={["vessels_list"]}
                fields={iv_vessels_fields}
                kb-interactive
                freezeRight={1}
                dynamic
                shownBy="/non_cds/show_hide_toggles/iv/iv_not_filter_by_errors"
              />
              <HX.Table
                data={["vessels_list"]}
                fields={iv_vessels_fields}
                kb-interactive
                freezeRight={1}
                dynamic
                shownBy="/non_cds/show_hide_toggles/iv/iv_filter_by_errors"
                filter={"iv/iv_has_error"}
              />
              <HX.Pane>
                <HX.Collection
                  fields={[{
                    field: "/non_cds/labels/mismatched_inception_year_warning.warning_option",
                    shownBy: "/non_cds/show_hide_toggles/show_mismatched_inception_year_warning"
                  }]}
                />
              </HX.Pane>
              <HX.Pane flow="right" shownBy="/non_cds/show_hide_toggles/show_powersearch" >
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

export { vw_iv };
