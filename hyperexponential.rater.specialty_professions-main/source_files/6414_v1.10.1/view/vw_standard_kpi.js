import * as HX from "hx-model-components";
import { max_layers, max_options } from "view/vw_constants";

function vw_loop_rate_change_layer(num_layers, num_options) {
  const objects = [];
  // standard kpi for rater priced
  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.Section title={"Summary Layer " + (n + 1)} defaultCollapsed shownBy="cds/standard_fields/is_rater_priced">
        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Collection
            title="Risk Details"
            numCols={4}
            fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line",
            ]}
          />
          <HX.Collection
            title="Pricing"
            numCols={2}
            fields={[
              "quoted_premium",
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
        </HX.With>
      </ HX.Section>
    );
  }

  // standard kpi for case priced
  for (let n = 0; n < num_options; n++) {
    objects.push(
      <HX.Section title={"Summary Option " + (n + 1)} defaultCollapsed shownBy="cds/standard_fields/is_case_priced">
        <HX.With context={{ type: "list", path: "cds/options", index: n }}>
          <HX.Collection
            title="Risk Details"
            numCols={4}
            fields={[
              "status",
              "section_reference",
              "brokerage_view",
              "written_line_case_priced",
            ]}
          />
          <HX.Collection
            title="Pricing"
            numCols={2}
            fields={[
              "quoted_premium_view",
              null,
              "technical_premium_case_priced",
              "benchmark_premium_case_priced",
              "tpi_case_priced",
              "bpi_case_priced_view",
            ]}
          />
          <HX.Collection
            title="Expected Loss Ratio"
            numCols={3}
            fields={[
              "pflr_case_priced",
              null,
              null
            ]}
          />
        </HX.With>
      </ HX.Section>
    );
  }
  return objects
}


function vw_standard_kpi(scale) {
  return (
    <HX.Page title="Standard KPIs" >
      {vw_loop_rate_change_layer(max_layers(), max_options())}
    </HX.Page >
  )
}


export { vw_standard_kpi };