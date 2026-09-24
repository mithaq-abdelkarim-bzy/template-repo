import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function vw_loop_rate_change_layer(num_layers) {
  const objects = [];

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.Section title={"Summary Layer " + (n + 1)} shownBy={"cds/rate_change/show_layer_" + (n + 1)} defaultCollapsed >
        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Collection
            title="Risk Details"
            numCols={4}
            fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line",
            ]}
          />
          <HX.Collection
            title="Pricing"
            numCols={2}
            fields={[
              { field: "quoted_premium", labelBy: "premium_label" },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]}
          />
          <HX.Collection
            title="Expected Loss Ratio"
            numCols={3}
            fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]}
          />
          <HX.Collection
            title="Rate Change"
            shownBy="/cds/standard_fields/is_renewal"
            numCols={3}
            fields={[
              { field: "rate_change/risk_adjusted_rate_change", shownBy: "/cds/standard_fields/is_rater_priced" },
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
    <HX.Page title="Standard KPIs" shownBy="model_state/show_after_landing_page">
      {vw_loop_rate_change_layer(max_layers())}
    </HX.Page >

  )
}


export { vw_standard_kpi };