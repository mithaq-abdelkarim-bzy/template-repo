// # v0.5.1
import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";
import { convertToFieldObjects, createLayersList_las, renderAllLayers } from "view/vw_utilities";
import Line from "components/line";
import TwoAxisLineChart from "components/two_axis_line_chart";
import TableNoEmptyRow from "components/table_no_empty_row";

// Define the list of layers to loop through ["layer_1",..."layer_n"]
const layers = [...createLayersList_las(max_layers())];

// const layer_fields = [
//   "las/current_year/lower",
//   "las/current_year/upper",
//   "las/current_year/ilf_user_input",
//   "las/current_year/ilf_selected",
//   "las/current_year/pct_of_claims_to_layer",
//   "las/current_year/premium",
//   "las/current_year/loss_to_layer",
//   // null,
//   // "las/previous_year/pct_of_claims_to_layer",
//   // "las/previous_year/premium",
//   // "las/previous_year/loss_to_layer",
//   // null,
//   // "las/movement/pct_of_claims_to_layer",
//   // "las/movement/premium",
//   // "las/movement/loss_to_layer",
//   null,
//   "las/chart/limit",
//   "las/chart/this_year",
//   // "las/chart/last_year",
//   "las/chart/ilf_selected",
// ]

const layer_fields = [
  "current_year/lower",
  "current_year/upper",
  "current_year/ilf_user_input",
  "current_year/ilf_selected",
  "current_year/pct_of_claims_to_layer",
  "current_year/premium",
  "current_year/loss_to_layer",
  // null,
  // "previous_year/pct_of_claims_to_layer",
  // "previous_year/premium",
  // "previous_year/loss_to_layer",
  // null,
  // "movement/pct_of_claims_to_layer",
  // "movement/premium",
  // "movement/loss_to_layer",
  null,
  "chart/limit",
  "chart/this_year",
  // "chart/last_year",
  "chart/ilf_selected",

]

// const fgu_fields = [
//   "fgu/las/lower",
//   "fgu/las/upper",
//   "fgu/las/losses",
//   "fgu/las/occurrences",
//   "fgu/las/average",
//   "fgu/las/las",
//   "fgu/las/ilf_empirical",
// ]

const fgu_fields = [
  "lower",
  "upper",
  "losses",
  "occurrences",
  "average",
  "las",
  "ilf_empirical",
]

// const seriesData = Object.entries(ihsRiskNames).map(([key, label]) => ({
//   seriesLabel: label,
//   points: [{ list: `/ihs_${key}`, x: "updated_on", y: "value" }],
// }));

// function getChartData(layerName) {
//   const seriesData = [{
//     seriesLabel: `${layerName}`,
//     // seriesLabel: "layer_01",
//     points: [{
//       list: `/cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/${layerName}/las/chart/ilf_selected`,
//       x: `/cds/steer/exposure_rating/risk_profile_bdx/risk_profiles/${layerName}/las/chart/limit`,
//       y: `/cds/steer/exposure_rating/risk_profile_bdx/risk_profile/${layerName}/las/chart/this_year`
//     }],
//   }];
// }

const summaryFields = [
  "excess",
  "limit",
  "pricing_selection/limit_average_severity/pure_rate",
  // "pricing_selection/limit_average_severity/ulr",
]

// Function to render one layer
function renderLimitAverageSeverityLayer(layerName) {
  const displayName = layerName === 'fgu' ? 'FGU' : `Layer ${layerName.split('_')[1]}`;
  const num_layer = +layerName.split('_')[1] - 1;
  const fieldObjects = convertToFieldObjects(layer_fields);
  const prefixedFields = fieldObjects.map(item => {
    if (item === null) {
      return null;
    }
    return {
      // field: `${layerName}/${item.field}`,
      field: `${item.field}`,
      maxWidth: item.maxWidth,
      shownBy: item.shownBy
      // shownBy: `/model_state/show_layer_${layerName.split('_')[1].toString().padStart(2, '0')}`
    };

  });

  // Create Series data for chart
  const curveNames = {
    this_year: "Current Year",
    // last_year: "Previous Year",

  };

  const seriesData = Object.entries(curveNames).map(([key, label]) => ({
    seriesLabel: label,
    // seriesLabel: `${layerName}`,
    // points: [{ list: `/ihs_${key}`, x: "updated_on", y: "value" }],
    points: [{
      list: `/cds/steer/exposure_rating/limit_average_severity/layers/${layerName}/risk_profiles`,
      x: `chart/limit`,
      y: `chart/${key}`
    }],
  }));

  return (
    // <HX.With context={{ type: "struct", path: "/cds/steer/exposure_rating/risk_profile_bdx" }}>

    // <HX.Section title={displayName} shownBy="/model_state/show_"{layerName}> 
    < HX.Section title={displayName} shownBy={`/model_state/show_${layerName}`}>
      <HX.Pane>
        <HX.Pane>
          {/* <HX.Collection fields={[`layers/${layerName}/excess`, null, null, null, null, null]} horizontal />
              <HX.Collection fields={[`layers/${layerName}/limit`, null, null, null, null, null]} horizontal /> */}

          {/* <HX.Collection fields={[`layers/${layerName}/excess`, `layers/${layerName}/limit`, null, null, null, null]} horizontal /> */}
          <HX.With context={{ type: "list", path: "/cds/layers", index: num_layer }}>
            <HX.Collection fields={[`excess`, null, null, null, null, null]} horizontal />
            <HX.Collection fields={[`limit`, null, null, null, null, null]} horizontal />
          </HX.With>

        </HX.Pane>
        <HX.Pane>
          <HX.Table
            data={[
              `/cds/steer/exposure_rating/limit_average_severity/layers/${layerName}/risk_profiles`,
              // null,
              `/cds/steer/exposure_rating/limit_average_severity/layers/${layerName}/total`,
            ]}
            fields={[
              // ...convertToFieldObjects(layer_fields)
              ...prefixedFields
            ]}
            title={displayName}
            kb-interactive
            // with={layerName}
            syncColumnWidthsKey="field"
          // rowHeaderSettings={{ width: 140 }}
          />

          {/* <TableNoEmptyRow
            data={[
              `/cds/steer/exposure_rating/limit_average_severity/layers/${layerName}/risk_profiles`,
              // null,
              `/cds/steer/exposure_rating/limit_average_severity/layers/${layerName}/total`,
            ]}
            fields={[
              // ...convertToFieldObjects(layer_fields)
              // ...prefixedFields
              "current_year/lower"
            ]}
            title={displayName}
            kb-interactive
            
            // syncColumnWidthsKey="field"
          
          /> */}

        </HX.Pane>
        <HX.Pane>
          <HX.With context={{ type: "struct", path: "/cds/steer/exposure_rating/limit_average_severity/layers" }}>
            {/* <HX.With context={{ type: "list", path: "/cds/steer/exposure_rating/limit_average_severity/layers", index: num_layer }}> */}
            <HX.Collection fields={[`${layerName}/glr`, null, null, null, null, null]} horizontal />
            <HX.Collection fields={[`${layerName}/expected_loss`, null, null, null, null, null]} horizontal />
            <HX.Collection fields={[`${layerName}/pure_rate`, null, null, null, null, null]} horizontal />
            <HX.Collection fields={[`${layerName}/rol`, null, null, null, null, null]} horizontal />
            {/* <HX.Collection fields={[`total_las/${layerName}/las/glr`, `total_las/${layerName}/las/expected_loss`, `total_las/${layerName}/las/pure_rate`, `total_las/${layerName}/las/rol`, null, null]} horizontal /> */}

            <HX.Collection fields={[`/model_state/show_las_chart_${layerName}`, null, null, null, null, null]} horizontal />

            <HX.Pane flow="right" shownBy={`/model_state/show_las_chart_${layerName}`}>
              <HX.Pane ratio={1}>
                <Line
                  title="% of Claims to Layer"
                  xAxisLabel="Limit"
                  yAxisLabel="% of Claims to Layer"
                  series={seriesData}
                />
              </HX.Pane>
              <HX.Pane ratio={1}>
                <Line
                  title="ILF"
                  xAxisLabel="Limit"
                  yAxisLabel="ILF"
                  series={[
                    {
                      seriesLabel: "ILF Empirical",
                      points: [
                        {
                          list: `/cds/steer/exposure_rating/limit_average_severity/layers/${layerName}/risk_profiles`,
                          x: `chart/limit`,
                          y: "chart/ilf_selected",
                        },
                      ],
                    },
                    {
                      seriesLabel: "ILF Selected",
                      points: [
                        {
                          list: `/cds/steer/exposure_rating/limit_average_severity/layers/fgu/risk_profiles`,
                          x: `upper`,
                          y: `ilf_empirical`,
                        },
                      ],
                    },
                  ]}
                />
                {/* <TwoAxisLineChart
                  title="ILF"
                  xAxisLabel="Limit"
                  yAxisLabel="ILF Factor"
                  yAxis2Label=""
                  series={[
                    {
                      yaxis: "y",
                      label: "ILF Empirical",
                      colour: "#000000",
                      line_type: 'lines+marker',
                      points: [
                        {
                          list: `/cds/steer/exposure_rating/risk_profile_bdx/risk_profiles`,
                          x: `${layerName}/las/chart/limit`,
                          y: "fgu/las/ilf_empirical",
                        },
                      ],
                    },
                    {
                      yaxis: "y",
                      label: "Average Expected Loss",
                      colour: "#CA3397",
                      line_type: 'lines',
                      points: [
                        {
                          list: `/cds/steer/exposure_rating/risk_profile_bdx/risk_profiles`,
                          x: `${layerName}/las/chart/limit`,
                          y: `${layerName}/las/chart/ilf_selected`,
                        },
                      ],
                    },
                  ]}
                /> */}
              </HX.Pane>
            </HX.Pane>


          </HX.With>
        </HX.Pane>
      </HX.Pane>
    </HX.Section >
    // </HX.With >
  )
}

function vw_steer_exposure_rating_limit_average_severity(scale) {
  return (
    // <HX.Page title="Limit Average Severity" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
    <HX.Page title="Limit Average Severity" viewScale={scale} shownBy="model_state/show_steer_las_bdx">
      <HX.With context={{ type: "struct", path: "cds/steer/exposure_rating/limit_average_severity/layers" }} >
        {/* <HX.With context={{ type: "list", path: "cds/steer/exposure_rating/limit_average_severity/layers", index: num_layer }} > */}
        <HX.Section title="Limit Average Severity">
          <HX.Pane flow="down">

            <HX.Pane>
              <HX.Pane flow="right">
                <HX.Table
                  title="FGU"
                  // with="layers"
                  // with="fgu"
                  data={[
                    // "risk_profiles", "total"
                    "fgu/risk_profiles", "fgu/total"
                  ]}
                  fields={[
                    ...convertToFieldObjects(fgu_fields)
                  ]}
                // rowHeaderSettings={{ width: 140 }}
                />
                <HX.Notes field="/cds/steer/exposure_rating/risk_profile_bdx/message" shownBy="/model_state/is_bdx_input_issue" />
              </HX.Pane>
              <HX.Pane>
                <HX.Pane >
                  {renderAllLayers(layers, renderLimitAverageSeverityLayer)}
                </HX.Pane>
              </HX.Pane>
              <HX.Pane>
                <HX.Table
                  title="Summary"
                  with="/cds"
                  data={["layers"]}
                  fields={[
                    ...convertToFieldObjects(summaryFields, 120)

                  ]}
                  kb-interactive
                  // with={layerName}
                  syncColumnWidthsKey="field"
                  rowHeaderSettings={{ width: 150 }}
                />

              </HX.Pane>
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page >
  )
}

export { vw_steer_exposure_rating_limit_average_severity };