// v0.3.0
import * as HX from "hx-model-components";

function vw_rating_summary2(scale) {
  return (
    // NOTE: Use the line below for review only
    <HX.Page title="Rating Summary" fullWidth={true} shownBy="model_state/show_rate_change_layer_no_ia_use">
      {/* // NOTE: Use the line below for LIVE MODEL 
    <HX.Page title="Rating Summary" fullWidth={false} shownBy="model_state/show_after_landing_page"> */}
      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Summary">
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
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
        </HX.With>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} shownBy="cds/standard_fields/is_rater_priced">
          <HX.Collection
            title="Priced Quotes"
            numCols={2}
            fields={[
              "quoted_premium_100", // EDIT v0.3.0
              "model_premium",
              "technical_premium_100",
              "technical_premium_pre_uw_adj_100",
              "benchmark_premium_100",
              "currency",
            ]}
          />
          <HX.Collection
            title="Pricing Metrics"
            numCols={3}
            fields={[
              "tpi",
              "tpi_pre_uw_adj",
              "bpi",
              // { field: "bpi_case_priced", shownBy: "cds/standard_fields/is_case_priced" },
              "pflr",
              "pflr_att",
              "pflr_cat",

            ]}
          />
          <HX.Collection
            title="Other Metrics"
            numCols={2}
            fields={[
              "roc",
              "uw_adj_impact",
            ]}
          />

        </HX.With>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} shownBy="cds/standard_fields/is_case_priced">
          <HX.Collection
            title="Priced Quotes"
            numCols={2}
            fields={[
              "quoted_premium_100",
              "bpi_case_priced_100",
              "technical_premium_100",
              "benchmark_premium_100",
              "currency",
            ]}
          />
          <HX.Collection
            title="Pricing Metrics"
            numCols={3}
            fields={[
              "tpi",
              "pflr",
              "roc",
            ]}
          />
        </HX.With>
      </HX.Section>
      <HX.Section title="Case Pricing Analysis Filepath" shownBy="cds/standard_fields/is_case_priced">
        <HX.Notes field="cds/case_pricing_analysis_location" />
      </HX.Section>
    </HX.Page >

  )
}


export { vw_rating_summary2 };