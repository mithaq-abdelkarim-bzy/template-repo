// # v0.5.1
import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function vw_loop_layer(num_layers) {
  const objects = [];

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      // <HX.Section title={"Summary Layer " + (n + 1)} defaultCollapsed shownBy={"/cds/rate_change/show_layer_0" + (n + 1)}>
      // <HX.Section title={"Summary Layer " + (n + 1)} defaultCollapsed shownBy={"/model_state/show_layer_0" + (n + 1)}>
      <HX.Section title={"Summary Layer " + (n + 1)}>
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
            title="Pricing"
            numCols={2}
            fields={[
              "quoted_premium_100",
              null,
              "technical_premium_100",
              "benchmark_premium_100",
              "tpi",
              "bpi",
              { field: "tpi_pre_uw_adj", shownBy: "/cds/standard_fields/is_rater_priced" },
              { field: "bpi_pre_uw_adj", shownBy: "/cds/standard_fields/is_rater_priced" }
            ]}
          />
          <HX.Collection
            title="Expected Loss Ratio"
            shownBy="/cds/standard_fields/is_rater_priced"
            numCols={3}
            fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]}
          />
          <HX.Collection
            title="Expected Loss Ratio"
            shownBy="/cds/standard_fields/is_case_priced"
            numCols={3}
            fields={[
              "pflr",
              null,
              null
            ]}
          />
          <HX.Collection
            title="Rate Change"
            shownBy="/cds/standard_fields/is_renewal"
            numCols={3}
            fields={[
              { field: "rate_change/rate_change/final", shownBy: "/cds/standard_fields/is_rater_priced" },
              { field: "rate_change/risk_adjusted_rate_change_case_priced.read_only", shownBy: "/cds/standard_fields/is_case_priced" },
              null, null
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
    <HX.Page title="Standard KPIs" viewScale={scale} shownBy="model_state/show_after_landing_page">
      {vw_loop_layer(max_layers())}
    </HX.Page >

  )
}


export { vw_standard_kpi };