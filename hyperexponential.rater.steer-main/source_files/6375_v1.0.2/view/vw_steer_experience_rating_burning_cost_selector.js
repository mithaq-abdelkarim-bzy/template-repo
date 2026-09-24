// # v0.5.1
import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";
import { createLayersList, convertToFieldObjects, renderAllLayers } from "view/vw_utilities";
import EditableText from "components/text_box_editable";
import TwoAxisLineChart from "components/two_axis_line_chart";
import Line from "components/line";


// Define the layers to loop through
const layers = [...createLayersList(max_layers())];

const burningCostFields = [
  // "policy_year",
  "weighting",
  "onlevelled_exposure",
  "incurred_claims",
  "incurred_no_of_claims",
  "inflated_claims",
  "inflated_no_of_claims",
  "ultimate_claims_developed",
  "ultimate_claims_developed_and_inflated",
  "ibnr",
  "ultimate_no_of_claims_developed",

  "frequency_per_m_exposure",
  "average_cost_per_claim",
  "loss_cost_per_m_exposure",
  "rate_pct",
  "expected_loss_cost",
  null,
  "premium",
  "ulr",
  null,
  "claim_dev_pct",
  "claim_count_dev_pct",
  "claim_dev_method",
  "claim_count_dev_method",
  null,
  "cl_incurred_claims_developed",
  "cl_inflated_claims_developed",
  "cl_claim_count_developed",
  "cl_freq",
  "cl_acpc",
  "cl_acpc_inflated",
  null,
  "bf_claim_amount",
  "bf_claim_amount_inflated",
  "bf_claim_count"

]

const summaryFields = [
  "excess",
  "limit",
  "pricing_selection/burning_cost/pure_rate",
  "pricing_selection/burning_cost/ulr",
]

const bfFields = [
  "frequency_per_m_exposure",
  "acpc",
  "loss_cost_per_m_revenue",
  "offset_rows"
]


function display_selected_claim_pattern() {
  return <HX.Collection fields={["pattern_type"]} />;
}

function renderBurningCostLayer() {

  return (
    <HX.Section title="Burning Cost">
      <HX.Pane>
        <HX.Pane flow="right">
          <HX.Pane ratio={1}>
            <HX.Button task="steer_populate_bc_patterns_task" title="Update Burning Cost Pattern" />
          </HX.Pane>
          <HX.Pane ratio={1}>
            <HX.Collection fields={["triangle_projection/update_pattern_message"]} shownBy="triangle_projection/is_not_experience_selected_updated" horizontal />
          </HX.Pane>
          <HX.Pane ratio={4}>

          </HX.Pane>
        </HX.Pane>


        <HX.Pane>
          <HX.Table
            // with={layerName}
            data={[
              { datum: "burning_cost", elementLabelBy: "policy_year_label" },
              null,
              "selected_years_wa",
              "all_years_wa"
            ]}
            fields={[
              ...convertToFieldObjects(burningCostFields, 120)
            ]}
            title="Burning Cost"
            kb-interactive

            syncColumnWidthsKey="field"
            rowHeaderSettings={{ width: 160 }}
          />
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Pane ratio={1}>
            <EditableText
              textNode="bc_comment"
              placeholderText="Comment on manual adjustments, selected claims pattern..."
            />
          </HX.Pane>
          <HX.Pane ratio={1}>
            {/* <HX.Collection fields={["triangle_projection/update_pattern_message"]} shownBy="triangle_projection/is_not_experience_selected_updated" horizontal /> */}
            <HX.Collection fields={["bc_ulr_message"]} horizontal />

          </HX.Pane>
          <HX.Pane ratio={1}>
            <HX.Pane >
              <HX.Pane flow="right">

                <HX.Pane ratio={1}>
                  {/* <HX.Button task="steer_populate_bc_patterns_task" title="Update Burning Cost Pattern" /> */}
                </HX.Pane>

                <HX.Pane ratio={1}>
                  {display_selected_claim_pattern()}
                </HX.Pane>

              </HX.Pane>

              <HX.Table
                // with={layerName}
                title="Expected Pick from Experience (for years using CL)"
                data={[
                  "bf_expected/incurred_claim",
                  "bf_expected/inflated_claim",
                ]}
                fields={[
                  ...convertToFieldObjects(bfFields, 250)
                ]}
                kb-interactive
              />

            </HX.Pane>

          </HX.Pane>

        </HX.Pane>

        <HX.Pane flow="right">
          {/* <Line
            title="Expected Loss Cost"
            xAxisLabel="Year"
            yAxisLabel="Expected Loss"
            series={[
              {
                seriesLabel: "Average Expected Loss",
                points: [
                  {
                    list: "burning_cost",
                    x: "policy_year_label",
                    y: "average_expected_loss_cost",
                  },
                ],
              },
              {
                seriesLabel: "Expected Loss",
                points: [
                  {
                    list: "burning_cost",
                    x: "policy_year_label",
                    y: "expected_loss_cost",
                  },
                ],
              },
            ]}
          /> */}
          <HX.Pane ratio={1}>
            <TwoAxisLineChart
              title="Expected Loss Cost"
              xAxisLabel="Year"
              yAxisLabel="Expected Loss"
              yAxis2Label=""
              xAxisStep={1}
              xAxisTickFormat='.0f'
              yAxisTickFormat=',.0f'
              y2AxisTickFormat=',.0f'
              series={[
                {
                  yaxis: "y",
                  label: "Expected Loss",
                  colour: "#000000",
                  line_type: 'lines+marker',
                  points: [
                    {
                      list: "burning_cost",
                      x: "policy_year_label",
                      y: "average_expected_loss_cost",
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
                      list: "burning_cost",
                      x: "policy_year_label",
                      y: "expected_loss_cost",
                    },
                  ],
                },
              ]}
            />
          </HX.Pane>
          <HX.Pane ratio={1}>
            <TwoAxisLineChart
              title="Frequency per M of Exposure"
              xAxisLabel="Year"
              yAxisLabel="Frequency"
              yAxis2Label=""
              xAxisStep={1}
              xAxisTickFormat='.0f'
              yAxisTickFormat=',.2f'
              y2AxisTickFormat=',.0f'
              series={[
                {
                  yaxis: "y",
                  label: "Average Freq/m of Exposure",
                  colour: "#000000",
                  line_type: 'lines+marker',
                  points: [
                    {
                      list: "burning_cost",
                      x: "policy_year_label",
                      y: "average_freq_per_m_exposure",
                    },
                  ],
                },
                {
                  yaxis: "y",
                  label: "Frequency/m of Exposure",
                  colour: "#CA3397",
                  line_type: 'lines',
                  points: [
                    {
                      list: "burning_cost",
                      x: "policy_year_label",
                      y: "frequency_per_m_exposure",
                    },
                  ],
                },
              ]}
            />
          </HX.Pane>
          <HX.Pane ratio={1}>
            <TwoAxisLineChart
              title="Loss Cost per M of Exposure"
              xAxisLabel="Year"
              yAxisLabel="Loss Cost"
              yAxis2Label=""
              xAxisStep={1}
              xAxisTickFormat='.0f'
              yAxisTickFormat=',.0f'
              y2AxisTickFormat=',.0f'
              series={[
                {
                  yaxis: "y",
                  label: "Average Loss Cost/m of Exposure",
                  colour: "#000000",
                  line_type: 'lines+marker',
                  points: [
                    {
                      list: "burning_cost",
                      x: "policy_year_label",
                      y: "average_loss_cost_per_m_exposure",
                    },
                  ],
                },
                {
                  yaxis: "y",
                  label: "Loss Cost/m of Exposure",
                  colour: "#CA3397",
                  line_type: 'lines',
                  points: [
                    {
                      list: "burning_cost",
                      x: "policy_year_label",
                      y: "loss_cost_per_m_exposure",
                    },
                  ],
                },
              ]}
            />
          </HX.Pane>
        </HX.Pane>

      </HX.Pane>
    </HX.Section>
    // </HX.With>
  )
}

function summary() {

  return (
    <HX.Section title="Summary">
      <HX.Pane>
        <HX.Pane>
          <HX.With context={{ type: "struct", path: "/cds/steer/experience_rating/layers/fgu/selected_years_wa" }}>
            <HX.Collection title="FGU" fields={[null, null, null, "rate_pct", "ulr", null, null, null, null]} horizontal syncColumnWidthsKey="field" />
          </HX.With>
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
    </HX.Section>

  )
}

function vw_steer_experience_rating_burning_cost_selector(scale) {
  return (
    <HX.Page title="Burning Cost" fullWidth={true} viewScale={0.8} shownBy="model_state/show_steer_experience_rating">
      {/* {renderAllLayers(layers, renderBurningCostLayer)} */}
      <HX.Selector
        with="cds/steer/experience_rating/layers"
        data={[...createLayersList(max_layers())]}
        dropdown={"layer_name"} >
        {renderBurningCostLayer()}

      </HX.Selector>

      {summary()}


    </HX.Page >
  )
}

export { vw_steer_experience_rating_burning_cost_selector };