import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function vw_loop_rate_change_layer(num_layers) {
  const objects = [];

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.Section title={"Summary Layer " + (n + 1)} defaultCollapsed shownBy={"cds/rate_change/show_layer_" + (n + 1)}>
        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Collection
            title="Risk Details"
            numCols={4}
            fields={[
              "status.read_only",
              "section_reference.read_only",
              "brokerage.read_only",
              "written_line.read_only",
            ]}
          />
          <HX.Collection
            title="Priced Quotes (Beazley Share)"
            numCols={2}
            fields={[
              "quoted_premium.read_only",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
            ]}
          />
          <HX.Collection
            title="Expected Loss Ratio"
            numCols={3}
            fields={[
              "pflr",
              "pflr_att",
              "pflr_cat",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]}
          />
          <HX.Collection
            title="Other Metrics"
            numCols={3}
            fields={[
              "roc",
              { field: "rate_change/risk_adjusted_rate_change/uw_selected", shownBy: "/cds/standard_fields/is_renewal" },
              null,
              null
            ]}
          />
        </HX.With>
      </HX.Section>
    );
  }
  return objects
}


function vw_standard_kpi(scale) {
  return (
    <HX.Page title="Standard KPIs" fullWidth={false} shownBy="model_state/show_after_landing_page">
      {vw_loop_rate_change_layer(max_layers())}
    </HX.Page >

  )
}


export { vw_standard_kpi };