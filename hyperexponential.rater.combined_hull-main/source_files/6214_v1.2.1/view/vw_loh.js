import * as HX from "hx-model-components";
import { get_inputs_section, get_default_section } from "view/common";

function get_loh_vessel_details() {
  const coverage_prefix = "loh_";
  const vessel_details_prefix = "loh_vessel_details/loh_";
  const vessel_details_fields = [
    vessel_details_prefix + "name",
    vessel_details_prefix + "imo",
    vessel_details_prefix + "vessel_type",
    vessel_details_prefix + "year_built",
    vessel_details_prefix + "gross_tonnage",
    vessel_details_prefix + "dwt",
  ];
  const coverage_fields = [
    {
      field: coverage_prefix + "daily_rate",
      labelBy: "/non_cds/labels/currency_loh_daily_rate_label",
    },
    coverage_prefix + "xs_days",
    coverage_prefix + "cover",
    coverage_prefix + "conditions",
    coverage_prefix + "uw_adjustment",
    {
      field: coverage_prefix + "sum_insured",
      labelBy: "/cds/currency_loh_total_sum_insured_label",
    },
    coverage_prefix + "vessel_base_rate",
    coverage_prefix + "vessel_daily_rate",
    {
      field: coverage_prefix + "benchmark_premium",
      labelBy: "/non_cds/labels/currency_loh_benchmark_premium_label",
    },
    coverage_prefix + "vessel_achieved_rate",
  ];
  return [
    {
      field: coverage_prefix + "number_of_vessels",
      infoBy: "/non_cds/tooltips/loh/number_of_vessels",
    },
    ...vessel_details_fields,
    ...coverage_fields,
  ];
}

function vw_loh(scale) {
  coverage = "loh";
  return (
    <HX.Page
      title="Loss of Hire (LOH)"
      shownBy="/non_cds/show_hide_toggles/loh/show_loh_coverage"
      fullWidth
    >
      <HX.With
        context={{
          type: "struct",
          path: "cds/exposure/granular/vessels",
        }}
      >
        {get_inputs_section(coverage)}
        {get_default_section(coverage)}
        <HX.Section title="LOH Vessels">
          <HX.With context={{ type: "list", index: 0, path: "/cds/layers" }}>
            <HX.Pane flow="down">
              <HX.Pane flow="right">
                <HX.Button
                  task={"clear_loh_vessels_task"}
                  title="Clear Vessels Table"
                />
                <HX.Button task={"lookup_loh_imos_task"} title="Lookup IMOs" />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection
                  fields={[
                    {
                      field: "coverages/loh/loh_total_sum_insured",
                      labelBy: "/cds/currency_loh_total_sum_insured_label",
                    },
                    "coverages/loh/loh_fleet_level",
                    {
                      field: "coverages/loh/loh_total_premium",
                      labelBy:
                        "/non_cds/labels/loh/total_benchmark_premium_label",
                    },
                  ]}
                  horizontal
                  syncColumnWidthsKey="key_1"
                />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Collection
                  fields={[
                    {
                      field:
                        "/non_cds/labels/loh/loh_vessels_number_greater_than_one_warning",
                      shownBy:
                        "/non_cds/show_hide_toggles/loh/show_number_of_vessels_warning",
                    },
                    {
                      field:
                        "/non_cds/labels/loh/data_mart_warning_message.read_only_option",
                      shownBy:
                        "/non_cds/show_hide_toggles/loh/show_data_mart_warning",
                    },
                  ]}
                  horizontal
                />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
              <HX.Table
                data={[
                  "/cds/exposure/granular/vessels/loh_rating/loh_vessels_list",
                ]}
                fields={get_loh_vessel_details()}
                title=""
                kb-interactive
                dynamic
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
          </HX.With>
        </HX.Section>
      </HX.With>
    </HX.Page>
  );
}

export { vw_loh };
