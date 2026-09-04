import * as HX from "hx-model-components";

function vw_rating_summary(scale) {
  return (
    <HX.Page title="Rating Summary" fullWidth={true} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Summary" shownBy="cds/standard_fields/is_rater_priced">
        <HX.Pane flow="right">
          <HX.Pane>
            <HX.Notes field="messages/rating_summary_note" title=" " />
            <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
              <HX.Collection numCols={2} fields={[
                { field: "quoted_premium", labelBy: "/messages/epi_heading" },
                "/cds/modifiers/underwriter_adjustment",
                "model_premium",
                { field: "/messages/min_premium_note", shownBy: "min_premium/flag" }
              ]} />
            </HX.With >
          </HX.Pane>
          <HX.Pane>
            <HX.Notes field="cds/uw_rationale/comments" title="Comments" />
          </HX.Pane>
        </HX.Pane>
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} >
          <HX.Pane flow="right">
            <HX.Collection
              title="Pricing - Expected Loss"
              fields={[
                "expected_loss/exposure_rated",
                "expected_loss/experience_rated",
                "expected_loss/experience_weight",
                "expected_loss/blended"
              ]}
            />
            <HX.Collection
              title="Technical Pricing - Targets 15% RoC"
              fields={[
                "technical_premium",
                "tpi",
                "roc"
              ]}
            />
            <HX.Collection
              title="Benchmark Pricing - Targets 70% NLR"
              fields={[
                "benchmark_premium",
                "bpi",
                "pflr"
              ]}
            />
          </HX.Pane>
        </HX.With>
      </HX.Section>
      <HX.Section title="Alternate Scenarios" shownBy="cds/standard_fields/is_rater_priced">
        <HX.Table
          data={[{ datum: "cds/layers", elementLabelBy: "label" }]}
          syncColumnWidthsKey="mySyncedTables1"
          fields={[
            "alt_limit",
            "alt_agg_limit",
            null,
            "suggested_epi",
            null,
            "model_premium"
          ]}
          transpose
          filter={"filter"}
        />
      </HX.Section>
      <HX.Section title="Summary" shownBy="cds/standard_fields/is_case_priced">
        <HX.Notes field="messages/policy_info_note" />
        <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} >
          <HX.Collection
            title="Priced Quotes"
            numCols={2}
            fields={[
              "quoted_premium",
              "bpi_case_priced",
              "technical_premium",
              "benchmark_premium",
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
    </HX.Page >
  )
}


export { vw_rating_summary };