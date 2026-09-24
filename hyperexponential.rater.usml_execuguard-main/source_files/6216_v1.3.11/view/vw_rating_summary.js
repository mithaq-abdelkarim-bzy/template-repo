import * as HX from "hx-model-components";

function vw_rating_summary(scale) {
  return (
    <HX.Page title="Rating Summary" fullWidth={true} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology.read_only", null]} horizontal />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Rater Status">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/package_information/finished_rating"]} />
          <HX.Pane flow="right">
            <HX.Button task="word_documents_task" title="Generate Coverage Options" />
            <HX.File field="/cds/coverage_options" />
          </HX.Pane>
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Coverage Options">
        <HX.Table
          title="Priced Quotes (Beazley Share)"
          data={[{ datum: "cds/layers", width: 250 }]}
          fields={[
            "status.input",
            "section_reference",
            "brokerage",
            "written_line",
            null,
            "quoted_premium",
            "technical_premium",
            { field: "technical_premium_pre_uw_adj", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "benchmark_premium" },
            null,
            "tpi",
            { field: "tpi_pre_uw_adj", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "bpi", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "bpi_case_priced", shownBy: "cds/standard_fields/is_case_priced" },
            null,
            "pflr",
            "roc",
            { field: "uw_adj_impact", shownBy: "cds/standard_fields/is_rater_priced" },
          ]}
          freezeLeft={0}
          kb-interactive // can interact with tables like excel e.g. c&p
          transpose // note un-transpose if require layers to be listed vertically
        />

      </HX.Section>
      <HX.Section title="Quote Grid Summary" shownBy="cds/admitted_excess_local/is_policy_primary">
        <HX.Table
          data={[
            "cds/quote_grid_summary/epl",
            "cds/quote_grid_summary/fid",
            "cds/quote_grid_summary/pcl",
          ]}
          fields={["limit", "adl", "retention", "benchmark_premium", "pre_rounding_admitted_premium", "selected_premium", "post_rounding_admitted_premium", "final_term_premium", "bpi"]}
          title="Quote Grid Summary"
          syncColumnWidthsKey="mySyncedTables1"
        />
      </HX.Section>

      <HX.Section title="Final Premium Summary" shownBy="cds/admitted_excess_local/is_policy_primary">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/final_premium_summary/benchmark_premium", "cds/final_premium_summary/pre_rounding_admitted_premium", "cds/final_premium_summary/post_rounding_admitted_premium"]} />
          <HX.Collection fields={["cds/final_premium_summary/benchmark_term_premium", "cds/final_premium_summary/technical_term_premium", "cds/final_premium_summary/final_admitted_term_premium"]} />
          <HX.Collection fields={["cds/final_premium_summary/bpi", "cds/final_premium_summary/tpi"]} />
          <HX.Collection fields={["cds/final_premium_summary/rounding_min", "cds/final_premium_summary/rounding_max"]} />


        </HX.Pane>
      </HX.Section>
    </HX.Page >

  )
}


export { vw_rating_summary };