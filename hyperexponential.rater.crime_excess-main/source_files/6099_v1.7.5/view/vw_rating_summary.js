/* eslint-disable */
import * as HX from "hx-model-components";
// import * as lst from "algorithms/utils_global_lists";

function vw_rating_summary() {
  return (
    <HX.Page title="Rating Summary" fullWidth shownBy="model_state/show_after_landing_page">
      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section shownBy="/cds/standard_fields/is_rater_priced">
        <HX.Section title="Individual Risk Rating">
          <HX.Table kb-interactive
            data={["classification_peculiarities", "management", "personnel", "location", "response_to_losses", "endorsements", "expense_modification", null, { datum: "total_modifiers" }]}
            fields={[{ field: "minimum_state", width: 200 },
            { field: "maximum_state", width: 200 },
            { field: "selected", width: 200 },
            { field: "comment" }]}
            filter="available"
            with="cds"
          />
          <HX.Pane flow="right">
            <HX.Collection fields={["mod_factor", "eligibility_min_before", "eligibility_min_after"]} with="cds" horizontal />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Expense Modification" shownBy="cds/expense_mod_flag">
          <HX.Table kb-interactive
            data={["expense_modification"]}
            fields={[{ field: "minimum_state", width: 200 },
            { field: "maximum_state", width: 200 },
            { field: "selected", width: 200 },
            { field: "comment" }]}
            with="cds"
          />
        </HX.Section>

        <HX.Section title="Rating Summary">
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Pane>
              <HX.Collection fields={["/cds/standard_fields/is_admitted_or_surplus", { field: "/cds/surplus_deviation_factor", shownBy: "/cds/is_surplus" }, "brokerage"]} horizontal syncColumnWidthsKey="Summary" />
              <HX.Pane flow="right">
                <HX.Collection title="Premium" fields={["final_premium", "final_premium_annual", "status"]} horizontal syncColumnWidthsKey="Summary" />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection title="Benchmark Pricing" fields={["benchmark_premium", "bpi"]} />
              <HX.Collection title="Technical Pricing" fields={["technical_premium", "tpi"]} />
              <HX.Collection title="Other Metrics" fields={["/hx_core/ulr", "/cds/term_adjustment", { field: "rate_change/rate_change/uw_selected", shownBy: "/cds/standard_fields/is_renewal" }]} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Section>

      <HX.Section title="Technical Summary" shownBy="/cds/standard_fields/is_case_priced">
        <HX.Table
          title="Priced Quote"
          data={[{ datum: "cds/options", width: 250 }]}
          fields={[
            "status",
            "section_reference",
            "brokerage",
            "written_line",
            null,
            "quoted_premium",
            "technical_premium",
            "benchmark_premium",
            null,
            "tpi",
            "bpi",
            null,
            "pflr",
            "roc"
          ]}
          freezeLeft={0}
          kb-interactive
          transpose
        />
      </HX.Section>

    </HX.Page>
  )
}

export { vw_rating_summary };
