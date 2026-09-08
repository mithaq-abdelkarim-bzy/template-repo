import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function vw_loop_rate_change_layer(num_layers) {
  const objects = [];

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.Section title={"Summary Layer " + (n + 1)} defaultCollapsed shownBy="cds/cover_selection/is_selected">
        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Collection
            title="Risk Details"
            numCols={4}
            fields={[
              "status_view",
              "section_reference_view",
              "brokerage_view",
              "written_line_view",
            ]}
          />
          <HX.Collection
            title="Pricing"
            numCols={2}
            fields={[
              "quoted_premium_view",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj",
            ]} shownBy="/cds/standard_fields/is_rater_priced"
          />

          <HX.Collection
            title="Expected Loss Ratio"
            numCols={3}
            fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]}
            shownBy="/cds/standard_fields/is_rater_priced"
          />

          <HX.Collection
            title="Pricing"
            numCols={2}
            fields={[
              "quoted_premium_view",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
            ]} shownBy="/cds/standard_fields/is_case_priced"
          />
          <HX.Collection
            title="Expected Loss Ratio"
            numCols={3}
            fields={[
              "pflr", null, null
            ]}
            shownBy="/cds/standard_fields/is_case_priced"
          />
        </HX.With>
      </HX.Section>
    );
  }
  return objects
}


function vw_standard_kpi(scale) {
  return (
    <HX.Page title="Standard KPIs">
      {vw_loop_rate_change_layer(max_layers())}
    </HX.Page >

  )
}


export { vw_standard_kpi };