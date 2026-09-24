import * as HX from "hx-model-components";

function vw_rating_summary() {
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

      <HX.Section title="Beazley Rater Pricing" shownBy="cds/standard_fields/is_rater_priced">
        <HX.Section title="Primary Layer">
          <HX.Pane flow="right">
            <HX.Notes field="cds/currency_label" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table kb-interactive
            rowHeaderSettings={{ width: 500 }}
            title="Primary Layer Priced Quotes (Beazley Share)"
            fields={["ilf_type",
              "limit",
              "aggregate_limit",
              "number_of_reinstatements",
              "deductible",
              "guideline_deductible",
              "minimum_deductible_flag",
              null,
              "ilf_factor",
              "reinstatements_factor",
              "deductible_factor",
              null,
              "beazley_primary",
              { field: "carrier", shownBy: "cds/carrier_primary" },
              { field: "carrier_premium", shownBy: "cds/carrier_primary" },
              null,
              "quoted_premium",
              "brokerage_primary",
              //"model_premium",
              "technical_premium",
              "benchmark_premium",
              "minimum_premium_flag",
              null,
              "tpi",
              "bpi",
              "pflr",
              "roc"
            ]}
            data={[
              { datum: "cds/options", width: 250 }
            ]}
            transpose
          />
          <HX.Pane flow="right">
            <HX.Collection fields={["cds/add_excess_1"]} horizontal />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>

        <HX.Section title={"Excess Layers"} shownBy={"cds/add_excess_1"}>
          {[1, 2, 3, 4, 5].map(layer => (
            <HX.Pane key={layer}>
              <HX.Table title={`Excess Layer ${layer}`} shownBy={`cds/add_excess_${layer}`}
                kb-interactive
                rowHeaderSettings={{ width: 500 }}
                fields={[
                  `excess_${layer}_beazley_participation`,
                  `excess_${layer}_cum_attachment`,
                  `excess_${layer}_limit`,
                  null,
                  { field: `excess_${layer}_quoted_premium`, shownBy: `cds/excess_${layer}_beazley_participation` },
                  { field: `excess_${layer}_brokerage`, shownBy: `cds/excess_${layer}_beazley_participation` },
                  { field: `excess_${layer}_technical_premium`, shownBy: `cds/excess_${layer}_beazley_participation` },
                  { field: `excess_${layer}_benchmark_premium`, shownBy: `cds/excess_${layer}_beazley_participation` },
                  { field: `excess_${layer}_ilf_curve`, shownBy: `cds/excess_${layer}_beazley_participation` },
                  { field: `excess_${layer}_tpi`, shownBy: `cds/excess_${layer}_beazley_participation` },
                  { field: `excess_${layer}_bpi`, shownBy: `cds/excess_${layer}_beazley_participation` },
                  { field: `excess_${layer}_pflr`, shownBy: `cds/excess_${layer}_beazley_participation` },
                  { field: `excess_${layer}_roc`, shownBy: `cds/excess_${layer}_beazley_participation` },
                  null,
                  { field: `excess_${layer}_carrier_premium` },
                  { field: `excess_${layer}_carrier_tpi` },
                  { field: `excess_${layer}_carrier_bpi` },
                ]}
                data={[{ datum: "cds/options", width: 250 }]}
                transpose
              />
              <HX.Pane flow="right" shownBy={`cds/add_excess_${layer}`}>
                {layer < 5 && (
                  <HX.Collection fields={[`cds/add_excess_${layer + 1}`]} horizontal />
                )}
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
                <HX.Pane />
              </HX.Pane>
            </HX.Pane>
          ))}
        </HX.Section>
      </HX.Section>

      <HX.Section title="Selected Option" shownBy="cds/standard_fields/is_rater_priced">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/option_selected"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Table kb-interactive
          fields={["cum_attachment", "limit", "status_view", "section_reference_view", "quoted_premium", "brokerage", "technical_premium", "benchmark_premium", "tpi", "bpi", "pflr", "roc"]}
          data={[
            { datum: "cds/primary" },
            { datum: "cds/layers", elementLabelBy: "layer_label" }
          ]}
          filter={"excess_flag"}
        />
      </HX.Section>
      {/* FOR CASE PRICINGS */}
      {/*  */}
      <HX.Section title="Priced Quotes (Beazley Share)" shownBy="cds/standard_fields/is_case_priced">
        <HX.Pane flow="right">
          <HX.Notes field="cds/currency_label" />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane>
          <HX.Table kb-interactive
            data={[{ datum: "cds/options", width: 250 }]}
            fields={[
              "status_view",
              "section_reference_view",
              "brokerage",
              "written_line_view",
              null,
              "quoted_premium",
              "technical_premium_case_priced",
              "benchmark_premium_case_priced",
              null,
              "tpi_case_priced",
              "bpi_case_priced",
              null,
              "pflr_case_priced",
              "roc_case_priced"
            ]}
            transpose
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page >

  )
}


export { vw_rating_summary };