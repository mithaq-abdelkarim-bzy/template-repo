import * as HX from "hx-model-components";
import { number_curves } from "view/vw_constants";


function vw_curve_aggregator(scale) {
  return (
    <HX.Page title="Curve Aggregator" fullWidth={true} viewScale={scale} shownBy="cds/show_non_risk_xl">
      <HX.Section title="Input">
        <HX.Pane>
          <HX.Table
            data={[{ datum: "cds/curve_aggregator/pml_selections" },
            ]}
            fields={[
              "include_in_aggregator"
              , "weight"
              , "name"]}
            transpose
            rowHeaderSettings={{ width: 250 }}
            kb-interactive
            syncColumnWidthsKey="curve_agg_input"
          />
          <HX.Table
            data={[{ datum: "cds/curve_aggregator/pml_selections" },
            ]}
            fields={[
              "rp_loss/rp_10000",
              "rp_loss/rp_5000",
              "rp_loss/rp_1000",
              "rp_loss/rp_500",
              "rp_loss/rp_250",
              "rp_loss/rp_200",
              "rp_loss/rp_100",
              "rp_loss/rp_50",
              "rp_loss/rp_25",
              "rp_loss/rp_10",
              "rp_loss/rp_5",
              "rp_loss/rp_2"]}
            transpose
            rowHeaderSettings={{ width: 250 }}
            kb-interactive
            syncColumnWidthsKey="curve_agg_input"
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Output">
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane >
            <HX.Table
              data={[
                { datum: "cds/curve_aggregator/aggregator_output/rp_labels", width: 250 },
                { datum: "cds/curve_aggregator/aggregator_output/rp_loss", maxWidth: 400 },
              ]}
              fields={[
                "rp_10000",
                "rp_5000",
                "rp_1000",
                "rp_500",
                "rp_250",
                "rp_200",
                "rp_100",
                "rp_50",
                "rp_25",
                "rp_10",
                "rp_5",
                "rp_2"]}
              transpose
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane>
            <HX.Button task="pull_pml_curves_task" title="Pull Curves" />
            <HX.Button task="aggregate_curves_task" title="Run Aggregate Curves Task" />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_curve_aggregator }