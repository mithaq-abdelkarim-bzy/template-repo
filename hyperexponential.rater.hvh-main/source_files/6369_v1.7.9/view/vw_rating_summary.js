import * as HX from "hx-model-components";

function vw_rating_summary(scale) {
  return (
    <HX.Page title="Rating Summary" fullWidth={true}>
      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Coverage Options">
        <HX.Table
          title="Priced Quotes"
          data={[{ datum: "cds/layers", width: 250, elementLabelBy: 'layer_label' }]}
          fields={[
            "status.read_only",
            "section_reference",
            "brokerage",
            "written_line",
            null,
            { field: "quoted_premium", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "quoted_premium_case_priced", shownBy: "cds/standard_fields/is_case_priced" },
            //{ field: "model_premium", shownBy: "cds/standard_fields/is_rater_priced" },
            "technical_premium",
            //{ field: "technical_premium_pre_uw_adj", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "benchmark_premium" },
            null,
            "tpi",
            { field: "tpi_pre_uw_adj", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "bpi", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "bpi_case_priced", shownBy: "cds/standard_fields/is_case_priced" },
            null,
            { field: "pflr_att", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "pflr_cat", shownBy: "cds/standard_fields/is_rater_priced" },
            "pflr",
            //"roc",
            { field: "uw_adj_impact", shownBy: "cds/standard_fields/is_rater_priced" },
          ]}
          freezeLeft={0}
          transpose
          filter="show_layer"
        />
      </HX.Section>
      <HX.Section title="Case Pricing Analysis Filepath" shownBy="cds/standard_fields/is_case_priced">
        <HX.Notes field="cds/case_pricing_analysis_location" />
      </HX.Section>
    </HX.Page >

  )
}


export { vw_rating_summary };