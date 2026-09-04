import * as HX from "hx-model-components";

function vw_rating_summary2(scale) {
  return (
    <HX.Page title="Rating Summary" fullWidth={false} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />

        </HX.Pane>
      </HX.Section>
      <HX.Section title="Underwriter adjustment to benchmark" shownBy="cds/standard_fields/is_rater_priced">
        <HX.Collection fields={["uw_adjustment", null, null, null]}
          with="cds/exposure/granular"
          horizontal />
        <HX.Collection fields={["uw_adjustment_rationale", null]}
          with="cds/exposure/granular"
          horizontal />
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

        <HX.Button task="insert_hx_meta_policy_references_task" title="Pass Policy Reference to PAS References" />

        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} shownBy="cds/standard_fields/is_rater_priced">
          <HX.Pane>
            <HX.Table
              title="Output (all in 100% share terms)"
              data={[null
                , { datum: "net_kpi", maxWidth: 140 }
                , null
                , { datum: "gross_kpi", maxWidth: 140 }
                ,]}
              fields={['benchmark_premium'
                , 'benchmark_rate'
                , null
                , "achieved_premium"
                , "achieved_rate"
                , null
                , "bpi_pre_uw_adj"
                , "bpi_post_uw_adj"
                , "pflr"
                , null
                , "technical_premium"
                , "tpi_pre_uw_adj"
                , "tpi_post_uw_adj"
                ,]}
              dynamic
              kb-interactive
              transpose
            />
          </HX.Pane>
        </HX.With>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} shownBy="cds/standard_fields/is_case_priced">
          <HX.Collection
            title="Priced Quotes"
            numCols={2}
            fields={[
              "quoted_premium_net_case_priced",
              "bpi_case_priced",
              "technical_premium_net",
              "benchmark_premium_net",
            ]}
          />
          <HX.Collection
            title="Pricing Metrics"
            numCols={2}
            fields={[
              "tpi",
              "pflr"
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