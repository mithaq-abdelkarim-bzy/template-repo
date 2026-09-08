import * as HX from "hx-model-components";

function vw_output_summary(scale) {
  return (
    <HX.Page
      title="Output Summary"
      fullWidth
      shownBy="/non_cds/show_hide_toggles/hull/show_hull_coverage"
    >
      <HX.Section title="">
        <HX.Pane flow="down">
          <HX.With
            context={{
              type: "list",
              path: "cds/exposure/granular/vessels/hull_rating/vessels_list",
              index: 0,
            }}
          >
            <HX.Table
              maxListVisibleRows={15}
              data={["/cds/exposure/granular/vessels/hull_rating/vessels_list"]}
              fields={[
                "vessel_details/imo.read_only_option",
                "vessel_details/name.read_only_option",
                "coverage.output_summary",
                {
                  field: "agreed_value.output_summary",
                  labelBy:
                    "/non_cds/labels/required_vessels_columns_labels/agreed_value",
                },
                "achieved_rate.output_summary",
                {
                  field: "iv/iv_output_summary_coverage",
                  shownBy: "/non_cds/show_hide_toggles/iv/show_iv_coverage",
                },
                {
                  field: "iv/iv_output_summary_agreed_value",
                  shownBy: "/non_cds/show_hide_toggles/iv/show_iv_coverage",
                  labelBy:
                    "/non_cds/labels/required_vessels_columns_labels/agreed_value",
                },
                {
                  field: "iv/iv_output_summary_achieved_rate",
                  shownBy: "/non_cds/show_hide_toggles/iv/show_iv_coverage",
                },
                {
                  field: "war/war_output_summary_coverage",
                  shownBy: "/non_cds/show_hide_toggles/war/show_war_coverage",
                },
                {
                  field: "war/war_output_summary_agreed_value",
                  shownBy: "/non_cds/show_hide_toggles/war/show_war_coverage",
                  labelBy:
                    "/non_cds/labels/required_vessels_columns_labels/agreed_value",
                },
                {
                  field: "war/war_output_summary_achieved_rate",
                  shownBy: "/non_cds/show_hide_toggles/war/show_war_coverage",
                },
              ]}
              kb-interactive
            />
          </HX.With>
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  );
}

export { vw_output_summary };
