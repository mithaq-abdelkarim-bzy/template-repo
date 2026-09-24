// v0.3.0
import * as HX from "hx-model-components";
import { exposure_detail_years } from "view/vw_constants";
import TwoAxisLineChart from "components/line";

function vw_exposure_details(scale) {
  return (
    <HX.Page title="Exposure Details" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Instructions" defaultCollapsed={true}>
        <HX.Notes field="cds/exposure/granular/exposure_details_notes" />
      </HX.Section>
      <HX.Section title="Exposure Details">
        <HX.Pane shownBy="cds/profession_lawyers_bool">
          <HX.Collection fields={[{
            field: "cds/exposure/granular/exposure_expected_current_year",
            labelBy: "cds/exposure/granular/exposure_expected_current_year_label"
          },
            null, null, null]} horizontal />
          <HX.Table
            title="Exposure Details"
            data={exposure_detail_years()}
            fields={[
              { field: "gross_fee", width: 180 },
              { field: "revalued_fee", width: 180 },
              { field: "weighting", width: 180 }
            ]}
            rowHeaderSettings={{ width: 80 }}
            with="cds/exposure/granular"
            dynamic
            kb-interactive
          />
        </HX.Pane>
        <HX.Pane shownBy="cds/profession_lawyers_bool_not">
          <HX.Collection fields={[{
            field: "cds/exposure/granular/exposure_expected_current_year",
            labelBy: "cds/exposure/granular/exposure_expected_current_year_label"
          },
            null, null, null]} horizontal />
          <HX.Table
            title="Exposure Details"
            data={exposure_detail_years()}
            fields={[
              { field: "professional_services_fee", width: 180 },
              { field: "epc_design_construct_values", width: 180 },
              { field: "hard_fm_revenue", width: 180 },
              { field: "construct_pass_soft_fm_revenue", width: 180 },
              { field: "revenue_100_pcnt", width: 180 },
              { field: "notional_revenue", width: 180 },
              { field: "revalued_notional_revenue", width: 180 },
              { field: "weighting", width: 180 }
            ]}
            rowHeaderSettings={{ width: 80 }}
            with="cds/exposure/granular"
            dynamic
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Chart - Model Loss Cost by Revenue" defaultCollapsed={false}>
        {/* <TwoAxisLineChart
          title="Model Loss Cost by Revenue"
          xAxisLabel="Revenue"
          yAxisLabel="Loss Cost"
          yAxis2Label=""
          series={[
            {
              yaxis: "y",
              label: "AEC",
              colour: "#000000",
              line_type: 'lines+marker',
              points: [
                {
                  list: "cds/exposure/granular/chart_loss_cost_by_revenue/data/points",
                  x: "revenue",
                  y: "loss_cost_aec",
                },
              ],
            },
            {
              yaxis: "y",
              label: "Lawyers",
              colour: "#CA3397",
              line_type: 'lines',
              points: [
                {
                  list: "cds/exposure/granular/chart_loss_cost_by_revenue/data/points",
                  x: "revenue",
                  y: "loss_cost_lpl",
                },
              ],
            },
          ]}
        /> */}
        <HX.Pane>
          <HX.XYChart
            data={["data", "data"]}
            points={["points_uk", "points_eu"]}
            xField="revenue"
            yField="loss_cost"
            formatFrom="y"
            labelField={["label_uk", "label_eu"]}
            xAxis={{
              label: "Revenue/Fees (Millions)",
            }}
            yAxis={{
              label: "Loss Cost (Millions)",
            }}
            with="cds/exposure/granular/chart_loss_cost_by_revenue"
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_exposure_details };
