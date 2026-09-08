import * as HX from "hx-model-components";
import Bar from "components/bar";

function vw_vessel_analysis(scale) {
  prefix = "vessel_analysis_";
  return (
    <HX.Page
      title="Vessel Analysis"
      shownBy="/non_cds/show_hide_toggles/hull/show_modelling_page"
    >
      <HX.With
        context={{
          type: "struct",
          path: "cds/vessel_analysis/hull_rating",
        }}
      >
        <HX.Section title="Options">
          <HX.Pane flow="right">
            <HX.Collection
              fields={[
                "imo_and_name/" + prefix + "imo",
                "imo_and_name/" + prefix + "name",
                prefix + "achieved_rate",
              ]}
              horizontal
            />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Similar Vessel Rate Comparison - Achieved vs. Achieved Rate Distribution">
          <HX.Pane flow="down">
            <HX.Pane flow="right">
              <HX.Table
                title="Vessel Type Age DWT"
                data={[prefix + "vessel_type_age_dwt_table"]}
                fields={[prefix + "vessel_type", prefix + "age_range", prefix + "dwt_range"]}
              />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <Bar
                title="Achieved Rate Distribution - Type, Age & DWT"
                data={[
                  {
                    list: "vessel_analysis_vessel_pre_type_age_dwt_list",
                    labelBy: "constant_pre_y",
                  },
                  {
                    list: "vessel_analysis_vessel_post_type_age_dwt_list",
                    labelBy: "constant_post_y",
                  },
                ]}
                traces={[
                  {
                    field: "vessel_analysis_pre_type_age_dwt",
                    label: "Vessels with lower rate",
                  },
                  {
                    field: "vessel_analysis_post_type_age_dwt",
                    label: "Vessels with higher rate",
                  },
                ]}
                xAxisTickAngle={-45}
                gapBetweenBarsSize={0.05}
                xAxisLabel="Achieved Rate"
                yAxisLabel=""
                barMode="stack"
              />
              <HX.Collection
                fields={[
                  prefix + "vessels_type_age_dwt_lower_rate",
                  prefix + "vessels_type_age_dwt_higher_rate",
                  prefix + "vessels_type_age_dwt_count",
                ]}
              />
            </HX.Pane>
            <HX.Pane />
            <HX.Pane />
            <HX.Pane flow="right">
              <Bar
                title="Achieved Rate Distribution - Type & Age"
                data={[
                  {
                    list: "vessel_analysis_vessel_pre_type_age_list",
                    labelBy: "constant_pre_y",
                  },
                  {
                    list: "vessel_analysis_vessel_post_type_age_list",
                    labelBy: "constant_post_y",
                  },
                ]}
                traces={[
                  {
                    field: "vessel_analysis_pre_type_age",
                    label: "Vessels with lower rate",
                  },
                  {
                    field: "vessel_analysis_post_type_age",
                    label: "Vessels with higher rate",
                  },
                ]}
                xAxisTickAngle={-45}
                gapBetweenBarsSize={0.05}
                xAxisLabel="Achieved Rate"
                yAxisLabel=""
                barMode="stack"
              />
              <HX.Collection
                fields={[
                  prefix + "vessels_type_age_lower_rate",
                  prefix + "vessels_type_age_higher_rate",
                  prefix + "vessels_type_age_count",
                ]}
              />
            </HX.Pane>
            <HX.Pane />
            <HX.Pane />
            <HX.Pane flow="right">
              <Bar
                title="Achieved Rate Distribution - Type"
                data={[
                  {
                    list: "vessel_analysis_vessel_pre_type_list",
                    labelBy: "constant_pre_y",
                  },
                  {
                    list: "vessel_analysis_vessel_post_type_list",
                    labelBy: "constant_post_y",
                  },
                ]}
                traces={[
                  {
                    field: "vessel_analysis_pre_type",
                    label: "Vessels with lower rate",
                  },
                  {
                    field: "vessel_analysis_post_type",
                    label: "Vessels with higher rate",
                  },
                ]}
                xAxisTickAngle={-45}
                gapBetweenBarsSize={0.05}
                xAxisLabel="Achieved Rate"
                yAxisLabel=""
                barMode="stack"
              />
              <HX.Collection
                fields={[
                  prefix + "vessels_type_lower_rate",
                  prefix + "vessels_type_higher_rate",
                  prefix + "vessels_type_count",
                ]}
              />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page>
  );
}

export { vw_vessel_analysis };
