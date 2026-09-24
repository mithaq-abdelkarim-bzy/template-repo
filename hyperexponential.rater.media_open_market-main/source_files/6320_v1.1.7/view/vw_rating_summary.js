import * as HX from "hx-model-components";

function vw_rating_summary(scale) {
  return (
    <HX.Page title="Rating Summary" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">

      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Coverage Options" shownBy="cds/standard_fields/is_case_priced">
        <HX.Table
          title="Priced Quotes"
          data={[{ datum: "cds/layers", elementLabelBy: "layer_label", labelAlign: "left" }]}
          fields={[
            { field: "status_view", width: 200 },
            { field: "section_reference_view", width: 200 },
            { field: "brokerage_input", width: 200 },
            { field: "written_line_input", width: 200 },
            null,
            { field: "quoted_premium_view", width: 200 },
            { field: "technical_premium", width: 200 },
            { field: "benchmark_premium", width: 200 },
            null,
            { field: "tpi", width: 200 },
            { field: "bpi_case_priced", shownBy: "cds/standard_fields/is_case_priced", width: 200 },
            null,
            { field: "pflr", width: 200 },
            { field: "roc", width: 200 },
          ]}
          freezeLeft={0}
          // transpose
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Case Pricing Analysis Filepath" shownBy="cds/standard_fields/is_case_priced">
        <HX.Notes field="cds/case_pricing_analysis_location" />
      </HX.Section>

      <HX.Section title="Primary Layer Options" shownBy="cds/standard_fields/is_rater_priced">
        <HX.Table
          title="Coverages"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[
            { field: "eec_limit", labelAlign: "left" },
            { field: "aggregate_limit", labelAlign: "left" },
            { field: "retention", labelAlign: "left" }
          ]}
          kb-interactive
          transpose
          shownBy="cds/rater_priced_standard"
        />
        <HX.Table
          title="Coverages"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[
            { field: "eec_limit", labelAlign: "left" },
            { field: "aggregate_limit", labelAlign: "left" },
            { field: "eec_excess", labelAlign: "left" },
            // { field: "aggregate_excess", labelAlign: "left" },
          ]}
          kb-interactive
          transpose
          shownBy="cds/rater_priced_nonstandard"
        />
        <HX.Collection
          fields={["cds/rating_factors/guideline_deductible", null, null, null, null]}
          horizontal
          syncColumnWidthsKey="mySyncedTables1"
          shownBy="cds/rater_priced_standard"
        />
        <HX.Collection
          fields={["cds/rating_factors/ilf_curve", null, null, null, null]}
          horizontal
          syncColumnWidthsKey="mySyncedTables1"
          shownBy="cds/rater_priced_standard"
        />
        <HX.Table
          title="Primary Layer Details"
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/options", elementLabelBy: "option_label" }]}
          fields={[
            { field: "technical_premium", labelAlign: "left" },
            { field: "benchmark_premium", labelAlign: "left" },
            { field: "quoted_premium", labelAlign: "left" },
            { field: "quoted_bpi", labelAlign: "left" }
          ]}
          kb-interactive
          transpose
        />
        <HX.Collection syncColumnWidthsKey="mySyncedTables1"
          fields={["cds/option_selected"]}
        />
      </HX.Section>

      <HX.Section title="Primary Layer" shownBy="cds/standard_fields/is_rater_priced">
        <HX.Pane>
          <HX.Table syncColumnWidthsKey="mySyncedTables1"
            data={[{ datum: "primary", labelAlign: "left", elementLabelBy: "layer_label" }]}
            with="cds"
            fields={[
              "brokerage",
              "quoted_premium_view",
              "bound_premium_input",
              "status",
              "section_reference",
              "benchmark_premium",
              "technical_premium",
              "bpi",
              "tpi"
            ]}
          />
        </HX.Pane>
        <HX.Pane shownBy="cds/coverage_selected_flag">
          <HX.Collection horizontal syncColumnWidthsKey="mySyncedTables1"
            fields={["cds/price_excess_flag"]}
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Excess Pricing" shownBy="cds/rater_priced_excess">
        <HX.Table
          title=""
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/primary", labelAlign: "left", elementLabelBy: "layer_label" }, { datum: "cds/layers", elementLabelBy: "layer_label", labelAlign: "left" }]}
          fields={[
            "aggregate_limit_view",
            "attachment",
            "quoted_premium_view",
            "bound_premium",
            "status_view",
            "section_reference_view"
          ]}
          kb-interactive
          freezeLeft={0}
          filter={"excess_flag"}
        />
        <HX.Table
          title=""
          syncColumnWidthsKey="mySyncedTables1"
          data={[{ datum: "cds/layers", elementLabelBy: "layer_label", labelAlign: "left" }]}
          fields={[ // Might want to reorder these
            "benchmark_premium",
            "technical_premium",
            "implied_price_per_m",
            "implied_ilf",
            "brokerage_input",
            "carrier",
            "quoted_price_per_m",
            "quoted_ilf",
            "bpi",
            "tpi"
          ]}
          kb-interactive
          freezeLeft={0}
        />
        <HX.Notes
          field="cds/excess_pricing_note"
          title="Excess Pricing Notes"
        />
      </HX.Section>

    </HX.Page>
  )
}

export { vw_rating_summary };