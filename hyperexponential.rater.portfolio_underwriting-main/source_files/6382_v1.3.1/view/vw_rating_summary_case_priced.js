// v0.3.0
import * as HX from "hx-model-components";

function vw_rating_summary_case_priced(scale) {
  return (
    <HX.Page
      title="Rating Summary"
      fullWidth={false}
      shownBy="model_state/show_rat_sum_case">
      <HX.Section title="Summary">
        <HX.Collection
          title="Risk Details"
          numCols={4}
          fields={[
            "cds/risk_information/deal_status",
            "cds/standard_fields/policy_reference",
            "cds/rating_summary/case_pricing/brokerage",
            "cds/rating_summary/case_pricing/written_line",
          ]}
        />
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}        >
          <HX.Collection
            title="Priced Quotes"
            numCols={2}
            fields={[
              "/cds/rating_summary/case_pricing/quoted_premium_100",
              "/cds/rating_summary/case_pricing/bpi",
              "technical_premium_100",
              "benchmark_premium_100",
              "/cds/currencies/source_currency",
              "/cds/rating_summary/case_pricing/tracker_class",
            ]}
          />
          <HX.Collection
            title="Pricing Metrics"
            numCols={3}
            fields={[
              "/cds/rating_summary/case_pricing/tpi_override",
              "pflr",
              "/cds/rating_summary/case_pricing/roc_override",
            ]}
          />
        </HX.With>
      </HX.Section>
      <HX.Section title="Case Pricing Analysis Filepath" >
        <HX.Notes field="cds/rating_summary/case_pricing/case_pricing_analysis_location" />
      </HX.Section>
    </HX.Page >

  )
}


export { vw_rating_summary_case_priced };