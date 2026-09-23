import * as HX from "hx-model-components";

function vw_rating_summary(scale) {
  return (
    <HX.Page title="Rating Summary" fullWidth={true}>
      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Collection fields={["cds/local_currency_output"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Coverage: E&O" shownBy="cds/eo_coverage_selection">
        {/* <HX.Pane flow="right">
          <HX.Collection fields={["cds/local_currency_output"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane> */}
        <HX.Pane></HX.Pane>
        <HX.Table
          title={"Priced Quotes in Original/Source Currency"}
          data={[{ datum: "cds/layers", width: 250 }]}
          fields={[
            "coverages/eo/status",
            "coverages/eo/section_reference",
            "coverages/eo/brokerage",
            // "written_line",
            null,
            "coverages/eo/quoted_premium",
            // { field: "coverages/eo/model_premium", shownBy: "cds/standard_fields/is_rater_priced" },
            "coverages/eo/technical_premium",
            { field: "coverages/eo/benchmark_premium" },
            // { field: "coverages/eo/technical_premium_pre_uw_adj", shownBy: "cds/standard_fields/is_rater_priced" },
            // { field: "coverages/eo/benchmark_premium_pre_uw_adj", shownBy: "cds/standard_fields/is_rater_priced" },
            null,
            "coverages/eo/tpi",
            { field: "coverages/eo/bpi", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "bpi_case_priced", shownBy: "cds/standard_fields/is_case_priced" },
            // { field: "coverages/eo/tpi_pre_uw_adj", shownBy: "cds/standard_fields/is_rater_priced" },
            // { field: "coverages/eo/bpi_pre_uw_adj", shownBy: "cds/standard_fields/is_rater_priced" },
            null,
            // { field: "coverages/eo/pflr_att", shownBy: "cds/standard_fields/is_rater_priced" },
            // { field: "coverages/eo/pflr_cat", shownBy: "cds/standard_fields/is_rater_priced" },
            "coverages/eo/pflr",
            "coverages/eo/roc",
            { field: "coverages/eo/uw_adj_impact", shownBy: "cds/standard_fields/is_rater_priced" },
          ]}
          freezeLeft={0}
          // kb-interactive // can interact with tables like excel e.g. c&p
          transpose // note un-transpose if require layers to be listed vertically
        />
      </HX.Section>

      <HX.Section title="Coverage: Media Tech" shownBy="cds/mediatech_coverage_selection">
        {/* <HX.Pane flow="right">
          <HX.Collection fields={["cds/local_currency_output"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane> */}
        <HX.Pane></HX.Pane>
        <HX.Table
          title={"Priced Quotes in Original/Source Currency"}
          data={[{ datum: "cds/layers", width: 250 }]}
          fields={[
            "coverages/mediatech/status",
            "coverages/mediatech/section_reference",
            "coverages/mediatech/brokerage",
            // "written_line",
            null,
            "coverages/mediatech/quoted_premium",
            // { field: "coverages/mediatech/model_premium", shownBy: "cds/standard_fields/is_rater_priced" },
            "coverages/mediatech/technical_premium",
            // { field: "coverages/mediatech/technical_premium_pre_uw_adj", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "coverages/mediatech/benchmark_premium" },
            null,
            "coverages/mediatech/tpi",
            // { field: "coverages/mediatech/tpi_pre_uw_adj", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "coverages/mediatech/bpi", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "bpi_case_priced", shownBy: "cds/standard_fields/is_case_priced" },
            null,
            // { field: "coverages/mediatech/pflr_att", shownBy: "cds/standard_fields/is_rater_priced" },
            // { field: "coverages/mediatech/pflr_cat", shownBy: "cds/standard_fields/is_rater_priced" },
            "coverages/mediatech/pflr",
            "coverages/mediatech/roc",
            { field: "coverages/mediatech/uw_adj_impact", shownBy: "cds/standard_fields/is_rater_priced" },
          ]}
          freezeLeft={0}
          // kb-interactive // can interact with tables like excel e.g. c&p
          transpose // note un-transpose if require layers to be listed vertically
        />
      </HX.Section>

      <HX.Section title="Coverage: GL" shownBy="cds/gl_coverage_selection">
        {/* <HX.Pane flow="right">
          <HX.Collection fields={["cds/local_currency_output"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane> */}
        <HX.Pane></HX.Pane>
        <HX.Table
          title={"Priced Quotes in $ USD"}
          data={[{ datum: "cds/layers", width: 250 }]}
          fields={[
            "coverages/gl/status",
            "coverages/gl/section_reference",
            "coverages/gl/brokerage",
            // "written_line",
            null,
            "coverages/gl/quoted_premium",
            // { field: "coverages/gl/model_premium", shownBy: "cds/standard_fields/is_rater_priced" },
            "coverages/gl/technical_premium",
            // { field: "coverages/gl/technical_premium_pre_uw_adj", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "coverages/gl/benchmark_premium" },
            null,
            "coverages/gl/tpi",
            // { field: "coverages/gl/tpi_pre_uw_adj", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "coverages/gl/bpi", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "bpi_case_priced", shownBy: "cds/standard_fields/is_case_priced" },
            null,
            // { field: "coverages/gl/pflr_att", shownBy: "cds/standard_fields/is_rater_priced" },
            // { field: "coverages/glpflr_cat", shownBy: "cds/standard_fields/is_rater_priced" },
            "coverages/gl/pflr",
            "coverages/gl/roc",
            { field: "coverages/gl/uw_adj_impact", shownBy: "cds/standard_fields/is_rater_priced" },
          ]}
          freezeLeft={0}
          // kb-interactive // can interact with tables like excel e.g. c&p
          transpose // note un-transpose if require layers to be listed vertically
        />
      </HX.Section>
    </HX.Page >

  )
}


export { vw_rating_summary };