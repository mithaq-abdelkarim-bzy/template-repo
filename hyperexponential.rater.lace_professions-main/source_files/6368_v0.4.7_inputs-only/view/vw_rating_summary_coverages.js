// v0.3.0
// USE FOR COVERAGES
import * as HX from "hx-model-components";
import { max_layers } from "view/vw_constants";

function vw_loop_rating_summary(num_layers) {
  const objects = [];

  for (let n = 0; n < num_layers; n++) {
    objects.push(
      <HX.Section title={"Coverage Options layer " + (n + 1)} shownBy={"cds/rate_change/show_layer_" + (n + 1)}>
        <HX.With context={{ type: "list", path: "cds/layers", index: n }}>
          <HX.Pane flow="right">
            <HX.Table
              title={"Priced Quotes Layer " + (n + 1) + " Coverage 1"}
              data={[{ datum: "coverages/example_coverage_1", width: 250 }]}
              fields={[
                "status",
                "section_reference",
                "brokerage",
                "written_line",
                null,
                "currency",
                "quoted_premium_100", // EDIT v0.3.0
                { field: "model_premium" },
                "technical_premium_100",// EDIT v0.3.0
                { field: "technical_premium_pre_uw_adj_100" },// EDIT v0.3.0
                { field: "benchmark_premium_100" },// EDIT v0.3.0
                null,
                "tpi",
                { field: "tpi_pre_uw_adj" },
                { field: "bpi" },
                { field: "bpi_case_priced", shownBy: "/cds/standard_fields/is_case_priced" },
                null,
                { field: "pflr_att" },
                { field: "pflr_cat" },
                "pflr",
                "roc",
                { field: "uw_adj_impact" },
              ]}
              freezeLeft={0}
              transpose
              kb-interactive
            />
            <HX.Table
              title={"Priced Quotes Layer " + (n + 1) + " Coverage 2"}
              data={[{ datum: "coverages/example_coverage_2", width: 250 }]}
              fields={[
                "status",
                "section_reference",
                "brokerage",
                "written_line",
                null,
                "currency",
                "quoted_premium_100", // EDIT v0.3.0
                { field: "model_premium" },
                "technical_premium_100",// EDIT v0.3.0
                { field: "technical_premium_pre_uw_adj_100" },// EDIT v0.3.0
                { field: "benchmark_premium_100" },// EDIT v0.3.0
                null,
                "tpi",
                { field: "tpi_pre_uw_adj" },
                { field: "bpi" },
                { field: "bpi_case_priced", shownBy: "/cds/standard_fields/is_case_priced" },
                null,
                { field: "pflr_att" },
                { field: "pflr_cat" },
                "pflr",
                "roc",
                { field: "uw_adj_impact" },
              ]}
              freezeLeft={0}
              transpose
              kb-interactive
            />
          </HX.Pane>
        </HX.With>
      </HX.Section>


    );
  }
  return objects
}

function vw_rating_summary_coverages(scale) {
  return (
    <HX.Page title="Rating Summary Coverages" fullWidth={true} viewScale={0.90} shownBy="model_state/coverage_no_ia_use">

      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      {vw_loop_rating_summary(max_layers())}
      <HX.Section title="Case Pricing Analysis Filepath" shownBy="cds/standard_fields/is_case_priced">
        <HX.Notes field="cds/case_pricing_analysis_location" />
      </HX.Section>
    </HX.Page >
  )
}
export { vw_rating_summary_coverages };