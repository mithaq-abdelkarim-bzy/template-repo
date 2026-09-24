// # v0.5.1
import * as HX from "hx-model-components";
import { max_layers, max_raw_data_columns } from "view/vw_constants";
import TwoAxisLineChart from "components/two_axis_line_chart";
import { convertToFieldObjects, node_name_list_with_suffix } from "view/vw_utilities";


function vw_healthcare_cat_pricing(scale) {
  return (
    <HX.Page title="Pricing Specifics" viewScale={scale} shownBy="model_state/show_healthcare_cat">
      <HX.With context={{ type: "struct", path: "cds/healthcare_cat" }}>
        <HX.Section title="Pricing Specifics">
          <HX.Pane>
            <HX.Table
              // title="Policy Specifics"
              with="pricing"
              data={[
                "territory_adjustment",
                "trial_history_adjustment",
                "type_of_business_adjustment",
                "specialty_adjustment",
                "high_low_adjustment",
                "social_inflation_impact",
                "total_risk_adjustment",
              ]}
              fields={[

                { field: "value", width: 150 },
                { field: "select", width: 150 },
              ]}
              kb-interactive
              // syncColumnWidthsKey="healthcare_cat/expected_cost_in_layer_beazley_share"
              rowHeaderSettings={{ width: 350 }}
            />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Pricing Information">
          <HX.Pane>
            <HX.Table
              // title="Policy Information"

              data={[
                { datum: "/cds/layers", width: 150 }
              ]}
              fields={[
                "healthcare_cat/gross_portfolio_size",
                "epi_100",
                null,
                "excess",
                "limit",
                "healthcare_cat/detachment",
                null,
                "healthcare_cat/expected_cost_in_layer_total",
                "healthcare_cat/expected_cost_in_layer_beazley_share",

              ]}
              kb-interactive
              transpose
              // syncColumnWidthsKey="total_risk_adjustment"
              rowHeaderSettings={{ width: 350 }}
            />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Loss Distribution">
          <HX.Pane flow="right">
            <HX.Pane ratio={1}>
              <HX.Collection
                with="pricing"
                fields={[
                  // { field: "mean_cat_ulr", width: 150 },
                  "mean_cat_ulr",
                  "decay_factor",
                  "loss_ratio_1_in_50"
                ]}
              // syncColumnWidthsKey="cds/layers/excess"
              />
            </HX.Pane>

            <HX.Pane ratio={1}></HX.Pane>
            <HX.Pane ratio={1}></HX.Pane>
            <HX.Pane ratio={1}></HX.Pane>
            <HX.Pane ratio={1}></HX.Pane>
          </HX.Pane>
          <HX.Pane flow="right">


            <HX.Pane>
              <HX.Table
                title="Loss distribution"

                // data={[
                // { datum: "pricing/loss_distribution_list", width: 150 }
                // "pricing/loss_distribution_summary"

                data={[
                  { datum: "pricing/loss_distribution_summary", elementLabelBy: "loss_percentile_display" }
                ]}
                fields={
                  [
                    // { field: "loss_percentile", width: 150 },
                    { field: "ulr", width: 150 }

                  ]}
                kb-interactive
                // transpose
                // syncColumnWidthsKey="total_risk_adjustment"
                rowHeaderSettings={{ width: 350 }}
              />

            </HX.Pane>
            <HX.Pane>
              <TwoAxisLineChart
                title="ULR Cumulative Loss Distribution"
                xAxisLabel="Probability of Loss"
                yAxisLabel="Loss Ratio"
                yAxis2Label=""
                xAxisMin={0.9}
                xAxisStep={0.1}



                height={700}
                width={600}
                line_thickness={1}
                legend_position="center"

                series={[
                  {
                    yaxis: "y",
                    label: "Loss Ratio",
                    colour: "#CA3397",
                    line_type: 'lines+marker',
                    points: [
                      {
                        list: "/healthcare_cat/pricing_calc/loss_distribution_calculation",
                        x: "loss_percentile",
                        y: "ulr",
                      },
                    ],

                  },

                  // {
                  //   yaxis: "y2", // "y"
                  //   label: "Win %",
                  //   colour: "#CA3397",
                  //   line_type: 'lines',
                  //   points: [
                  //     {
                  //       list: "/cds/healthcare_cat/trial_history/trial",
                  //       x: "uw_year",
                  //       y: "win_pct",
                  //     },
                  //   ],
                  // },

                ]}
              />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>

      </HX.With>
    </HX.Page >
  )
}

export { vw_healthcare_cat_pricing };