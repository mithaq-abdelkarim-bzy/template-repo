import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function generate_content(n, selected_coverage) {
  return (
    <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
      <HX.Collection
        title="Risk Details"
        numCols={4}
        fields={[
          `coverages/${selected_coverage}/status.read_only`,
          `coverages/${selected_coverage}/section_reference.read_only`,
          `coverages/${selected_coverage}/brokerage.read_only`,
          { field: `written_line_case_priced.read_only`, shownBy: "/cds/standard_fields/is_case_priced" },
          { field: `coverages/${selected_coverage}/written_line.read_only`, shownBy: "/cds/standard_fields/is_rater_priced" },
        ]}
      />
      <HX.Collection
        title="Pricing"
        numCols={2}
        fields={[
          { field: `coverages/${selected_coverage}/quoted_premium.read_only` },
          null,
          { field: "technical_premium", shownBy: "/cds/standard_fields/is_case_priced" },
          { field: `coverages/${selected_coverage}/technical_premium.short_label`, shownBy: "/cds/standard_fields/is_rater_priced" },
          { field: "benchmark_premium", shownBy: "/cds/standard_fields/is_case_priced" },
          { field: `coverages/${selected_coverage}/benchmark_premium.short_label`, shownBy: "/cds/standard_fields/is_rater_priced" },
          { field: `tpi`, shownBy: "/cds/standard_fields/is_case_priced" },
          { field: `coverages/${selected_coverage}/tpi`, shownBy: "/cds/standard_fields/is_rater_priced" },
          { field: `bpi`, shownBy: "/cds/standard_fields/is_case_priced" },
          { field: `coverages/${selected_coverage}/bpi`, shownBy: "/cds/standard_fields/is_rater_priced" },
          { field: `coverages/${selected_coverage}/tpi_pre_uw_adj`, shownBy: "/cds/standard_fields/is_rater_priced" },
          { field: `coverages/${selected_coverage}/bpi_pre_uw_adj`, shownBy: "/cds/standard_fields/is_rater_priced" }
        ]}
      />
      <HX.Collection
        title="Expected Loss Ratio"
        numCols={3}
        fields={[
          { field: "pflr", shownBy: "/cds/standard_fields/is_case_priced" },
          { field: null, shownBy: "/cds/standard_fields/is_case_priced" },
          { field: null, shownBy: "/cds/standard_fields/is_case_priced" },
          { field: `coverages/${selected_coverage}/pflr`, shownBy: "/cds/standard_fields/is_rater_priced" },
          { field: `coverages/${selected_coverage}/pflr_pre_uw_adj`, shownBy: "/cds/standard_fields/is_rater_priced" },
          { field: `coverages/${selected_coverage}/uw_adj_impact`, shownBy: "/cds/standard_fields/is_rater_priced" },
        ]}
      />
    </HX.With>
  );
};


function vw_loop_rate_change_layer(num_layers) {
  const objects = [];

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.Section title={"Summary Layer " + (n + 1)} defaultCollapsed shownBy="cds/eo_coverage_selection">
        {generate_content(n, "eo")}
      </HX.Section>
    );
    objects.push(
      <HX.Section title={"Summary Layer " + (n + 1)} defaultCollapsed shownBy="cds/mediatech_coverage_selection">
        {generate_content(n, "mediatech")}
      </HX.Section>
    );
    objects.push(
      <HX.Section title={"Summary Layer " + (n + 1)} defaultCollapsed shownBy="cds/gl_coverage_selection">
        {generate_content(n, "gl")}
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