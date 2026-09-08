import * as HX from "hx-model-components";
import { max_layers, max_options } from "view/vw_constants";

function vw_loop_rate_change_layer(num_layers) {
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
              "status_view",
              "/cds/standard_fields/policy_reference.read_only",
              "brokerage.read_only",
              "written_line_view",
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

  return objects
}


function vw_loop_rate_change_option(num_options) {
  const objects = [];

  // standard kpi for case priced
  for (let n = 0; n < num_options; n++) {
    objects.push(
      <HX.Section title={"Summary Layer " + (n + 1)} defaultCollapsed shownBy={"cds/rate_change/show_option_" + (n + 1)}>
        <HX.With context={{ type: "list", path: "cds/options", index: n }}>
          <HX.Collection
            title="Risk Details"
            numCols={4}
            fields={[
              "status_view",
              "section_reference.read_only",
              "brokerage.read_only",
              "written_line.read_only",
            ]}
          />
          <HX.Collection
            title="Pricing"
            numCols={2}
            fields={[
              "quoted_premium.read_only",
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi.read_only",
            ]}
          />
          <HX.Collection
            title="Expected Loss Ratio"
            numCols={3}
            fields={[
              "pflr",
              null,
              null
            ]}
          />
        </HX.With>
      </HX.Section>);
  }

  return objects
}

function vw_standard_kpi(scale) {
  return (
    <HX.Page title="Standard KPIs" shownBy="cds/standard_fields/is_case_priced">
      {vw_loop_rate_change_option(max_options())}
    </HX.Page >
  )
}

function vw_standard_kpi_rater(scale) {
  return (
    <HX.Page title="Standard KPIs" shownBy="cds/standard_fields/is_rater_priced">
      {vw_loop_rate_change_layer(max_layers())}
    </HX.Page >
  )
}


export { vw_standard_kpi, vw_standard_kpi_rater };