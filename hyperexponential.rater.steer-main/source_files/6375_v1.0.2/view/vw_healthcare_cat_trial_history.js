// # v0.5.1
import * as HX from "hx-model-components";
import Bar from "components/bar";
import TwoAxisLineChart from "components/two_axis_line_chart";
import LineBar from "components/combined_bar_line";
import { max_layers, max_raw_data_columns } from "view/vw_constants";


import { convertToFieldObjects, node_name_list_with_suffix } from "view/vw_utilities";

const exposureAssumptionsFields = [
  // "display_yoa",
  // "uw_year",
  "taken_to_trial",
  "wins",
  "losses",
  "mistrials",
  "win_pct",

]


function vw_healthcare_cat_trial_history(scale) {
  return (
    <HX.Page title="Trial History" viewScale={scale} shownBy="model_state/show_healthcare_cat">
      <HX.With context={{ type: "struct", path: "cds/healthcare_cat" }}>
        <HX.Section title="Trial History">
          <HX.Pane flow="right">
            <HX.Pane flow="down">
            </HX.Pane>
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
            <HX.Pane></HX.Pane>
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Table
                title="Trial History"
                with="trial_history"
                data={
                  [{ datum: "trial", elementLabelBy: "display_yoa" },
                    "total"
                  ]}
                fields={[
                  ...convertToFieldObjects(exposureAssumptionsFields, 150),

                ]}
                kb-interactive
              />
            </HX.Pane>
            <HX.Pane>

              {/* <Bar
                title="Historic Trend On Trials in Court"
                data={[
                  { list: "/cds/healthcare_cat/trial_history/trial", labelBy: "display_yoa" },
                ]}
                traces={[
                  { field: "taken_to_trial", label: "Taken To Trial" },
                  { field: "win_pct", label: "Win %" },
                  
                ]}
                xAxisTickAngle={-45}
                gapBetweenBarsSize={0.10}
                xAxisLabel="YOA"
                yAxisLabel="Win %"
                barMode="stack"
              /> */}

              {/* <TwoAxisLineChart
                title="Historic Trend On Trials in Court"
                xAxisLabel="Year"
                yAxisLabel="Taken To Trial"
                yAxis2Label="Win %"
                series={[
                  {
                    yaxis: "y",
                    label: "Taken To Trial",
                    colour: "#000000",
                    line_type: 'lines+marker',
                    points: [
                      {
                        list: "/cds/healthcare_cat/trial_history/trial",
                        x: "uw_year",
                        y: "taken_to_trial",
                      },
                    ],
                  },

                  {
                    yaxis: "y2", // "y"
                    label: "Win %",
                    colour: "#CA3397",
                    line_type: 'lines',
                    points: [
                      {
                        list: "/cds/healthcare_cat/trial_history/trial",
                        x: "uw_year",
                        y: "win_pct",
                      },
                    ],
                  },
                ]}
              /> */}


              <LineBar
                title={"Historic Trend On Trials in Court"}

                // select data to pass in prop below
                data={[{ list: "/cds/healthcare_cat/trial_history/trial", labelBy: "uw_year", }]}
                // select data to render as bars in prop below
                traces={[
                  { field: "taken_to_trial", label: "Taken To Trial", color: "#4085fd" },

                ]}
                // select data to render as lines in prop below
                series={[{
                  seriesLabel: "Win %",
                  seriesColor: "#e24a0e",
                  seriesLineType: 'solid',//'dash'
                  seriesMode: 'lines',
                  // edit below specifically
                  points: [{ list: "/cds/healthcare_cat/trial_history/trial", x: "uw_year", y: "win_pct", },],
                },]}
                xAxisTickAngle={-45}
                xAxisLabel="Taken To Trial"
                yAxisLabel="Win %"
                barMode="group"
                gapBetweenBarsSize={0.3}
                width={700}
                height={500}
                y2SeparateAxis={true}
              />

            </HX.Pane>
          </HX.Pane>
          <HX.Pane>

            <HX.Table
              title="Underwiting View on Average History Loss Ratio"
              with="trial_history"
              data={
                [
                  "uw_view"
                ]}
              fields={[
                { field: "from_year", width: 150 },
                { field: "to_year", width: 150 },
                ...convertToFieldObjects(exposureAssumptionsFields, 150),

              ]}
              kb-interactive
            />
          </HX.Pane>

        </HX.Section>

      </HX.With>
    </HX.Page >
  )
}

export { vw_healthcare_cat_trial_history };