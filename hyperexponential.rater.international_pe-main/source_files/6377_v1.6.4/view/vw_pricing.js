import * as HX from "hx-model-components";

function generatePricedQuotesTableFields(coverage) {
  return [
    `coverages/${coverage}/status`,
    { field: `coverages/${coverage}/section_reference.case_priced_label`, shownBy: "cds/standard_fields/is_case_priced" },
    { field: `coverages/${coverage}/section_reference.rater_priced_label`, shownBy: "cds/standard_fields/is_rater_priced" },
    `coverages/${coverage}/brokerage`,
    { field: "written_line_case_priced", shownBy: "cds/standard_fields/is_case_priced" },
    { field: `coverages/${coverage}/option_selected`, shownBy: "cds/standard_fields/is_rater_priced" },
    null,

    `coverages/${coverage}/quoted_premium`,

    { field: null, shownBy: "cds/standard_fields/is_rater_priced" },
    { field: "technical_premium", shownBy: "cds/standard_fields/is_case_priced" },
    { field: "benchmark_premium", shownBy: "cds/standard_fields/is_case_priced" },
    { field: `coverages/${coverage}/technical_premium_before_minimum_prem`, shownBy: "cds/standard_fields/is_rater_priced" },
    { field: `coverages/${coverage}/technical_premium`, shownBy: "cds/standard_fields/is_rater_priced" },
    { field: `coverages/${coverage}/benchmark_premium`, shownBy: "cds/standard_fields/is_rater_priced" },

    null,

    { field: `coverages/${coverage}/tpi`, shownBy: "cds/standard_fields/is_rater_priced" },
    { field: "tpi", shownBy: "cds/standard_fields/is_case_priced" },
    { field: `coverages/${coverage}/bpi_case_priced`, shownBy: "cds/standard_fields/is_case_priced" },
    { field: `coverages/${coverage}/bpi`, shownBy: "cds/standard_fields/is_rater_priced" },

    null,

    { field: `coverages/${coverage}/pflr`, shownBy: "cds/standard_fields/is_rater_priced" },
    { field: "pflr", shownBy: "cds/standard_fields/is_case_priced" },
    { field: `coverages/${coverage}/roc`, shownBy: "cds/standard_fields/is_rater_priced" },
    { field: "roc", shownBy: "cds/standard_fields/is_case_priced" },
    { field: `coverages/${coverage}/uw_adj_impact`, shownBy: "cds/standard_fields/is_rater_priced" },
  ]
};

function vw_pricing(scale) {
  return (
    <HX.Page title="Pricing and Rating Summary" fullWidth={true} viewScale={scale}>
      {/* shownBy="cds/gl_coverage_selection_opposite" */}
      <HX.Section title="Rating Methodology" >
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          {/* <HX.Collection fields={[{ field: "cds/local_currency_output", shownBy: "cds/gl_coverage_selection_opposite" }]} /> */}
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Coverage: E&O" shownBy="cds/eo_coverage_selection">
        <HX.Table
          data={[{ datum: "layers", width: 250 }]}
          fields={["coverages/eo/limit", "coverages/eo/aggregate_limit", "coverages/eo/deductible", "coverages/eo/guideline_deductible"]}
          title="Policy Limits and Retentions"
          syncColumnWidthsKey="mySyncedTables1"
          with="cds"
          freezeLeft={0}
          kb-interactive
          //dynamic // filter and sort
          transpose
        />
        <HX.Table
          title={"Priced Quotes"}
          data={[{ datum: "cds/layers", width: 250 }]}
          syncColumnWidthsKey="mySyncedTables1"
          fields={generatePricedQuotesTableFields("eo")}
          freezeLeft={0}
          // kb-interactive // can interact with tables like excel e.g. c&p
          transpose // note un-transpose if require layers to be listed vertically
        />
      </HX.Section>
      <HX.Section title="Coverage: Media Tech" shownBy="cds/mediatech_coverage_selection">
        <HX.Table
          data={[{ datum: "layers", width: 250 }]}
          fields={["coverages/mediatech/limit", "coverages/mediatech/aggregate_limit", "coverages/mediatech/additional_defense_limit", "coverages/mediatech/deductible", "coverages/mediatech/guideline_deductible"]}
          title="Policy Limits and Retentions"
          syncColumnWidthsKey="mySyncedTables1"
          with="cds"
          freezeLeft={0}
          kb-interactive
          //dynamic // filter and sort
          transpose
        />
        <HX.Table
          title={"Priced Quotes"}
          data={[{ datum: "cds/layers", width: 250 }]}
          syncColumnWidthsKey="mySyncedTables1"
          fields={generatePricedQuotesTableFields("mediatech")}
          freezeLeft={0}
          // kb-interactive // can interact with tables like excel e.g. c&p
          transpose // note un-transpose if require layers to be listed vertically
        />
      </HX.Section>
      <HX.Section title="Coverage: GL" shownBy="cds/gl_coverage_selection">
        <HX.Table
          data={[{ datum: "layers", width: 250 }]}
          fields={["coverages/gl/limit", "coverages/gl/aggregate_limit", "coverages/gl/gl_limit_agg", "coverages/gl/personal_advertise_limit_agg",
            "coverages/gl/defence_outside_limit", "coverages/gl/deductible", { field: "coverages/gl/excess_of", shownBy: "/cds/rating_factors/gl_excess_show" }]}
          title="Policy Limits in $ USD and Retentions in $ USD "
          syncColumnWidthsKey="mySyncedTables1"
          with="cds"
          kb-interactive
          freezeLeft={0}
          //dynamic // filter and sort
          transpose
        />
        <HX.Pane flow="right">
          <HX.Collection fields={[{ field: "cds/local_currency_output", shownBy: "cds/gl_coverage_selection" }]} />
          <HX.Collection fields={[{ field: "cds/gl_local_currency", labelBy: "cds/gl_local_currency_label" }]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane shownBy="cds/gl_local_currency">
          <HX.Table
            data={[{ datum: "layers", width: 250 }]}
            fields={["coverages/gl/limit_local_currency", "coverages/gl/aggregate_limit_local_currency", "coverages/gl/gl_limit_agg_local_currency",
              "coverages/gl/personal_advertise_limit_agg_local_currency", "coverages/gl/defence_outside_limit_local_currency", "coverages/gl/deductible_local_currency",
              { field: "coverages/gl/excess_of_local_currency", shownBy: "/cds/rating_factors/gl_excess_show" }]}
            title="Policy Limits and Retentions Converted to Source Currency "
            syncColumnWidthsKey="mySyncedTables1"
            with="cds"
            kb-interactive
            freezeLeft={0}
            //dynamic // filter and sort
            transpose
          />
        </HX.Pane>
        <HX.Table
          title={"Priced Quotes in Source Currency"}
          data={[{ datum: "cds/layers", width: 250 }]}
          fields={generatePricedQuotesTableFields("gl")}
          syncColumnWidthsKey="mySyncedTables1"
          freezeLeft={0}
          // kb-interactive // can interact with tables like excel e.g. c&p
          transpose // note un-transpose if require layers to be listed vertically
        />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_pricing };