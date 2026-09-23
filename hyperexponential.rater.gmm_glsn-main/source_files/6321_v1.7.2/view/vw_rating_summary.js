import * as HX from "hx-model-components";
import { gmm_schedule_mods, glsn_schedule_mods } from "view/vw_constants";

function vw_rating_summary(scale) {
  return (
    <HX.Page title="Rating Summary" fullWidth={true} viewScale={scale}>
      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Collection fields={[{ field: "cds/override_terms_to_display", shownBy: "cds/glsn_masking" }]} />
          <HX.Collection fields={[{ field: "cds/cips", shownBy: "cds/international_masking" }]} />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Layer Details">

        <HX.Table
          shownBy="cds/standard_fields/is_rater_priced"
          title="Priced Quotes (Beazley Share)"
          data={[{ datum: "cds/rating_factors/retention", labelAlign: "left" }, { datum: "cds/layers", elementLabelBy: "layer_label", labelAlign: "left" }]}
          fields={[
            "limit",
            "aggregate_limit",
            "brokerage",
            "model_premium",
            "quoted_premium",
            { field: "quoted_rate", shownBy: "cds/glsn_masking" },

            null,
            "bound_premium",
            { field: "bound_rate", shownBy: "cds/glsn_masking" },
            "section_reference",
            "status.input",
            // "written_line",

            null,
            "bpi",
            "tpi",
            "net_written_premium",
            // { field: "technical_premium_pre_uw_adj", shownBy: "cds/standard_fields/is_rater_priced" },
            "benchmark_premium",
            "technical_premium",

            // { field: "tpi_pre_uw_adj", shownBy: "cds/standard_fields/is_rater_priced" },
            // null,
            // { field: "pflr_att", shownBy: "cds/standard_fields/is_rater_priced" },
            // { field: "pflr_cat", shownBy: "cds/standard_fields/is_rater_priced" },
            // "pflr",
            // "roc",
            // { field: "uw_adj_impact", shownBy: "cds/standard_fields/is_rater_priced" },
          ]}
          filter={"show_row"}
          freezeLeft={0}
          kb-interactive
        // transpose
        />

        <HX.Table
          shownBy="cds/standard_fields/is_case_priced"
          title="Priced Quotes (Beazley Share)"
          data={[{ datum: "cds/rating_factors/retention", labelAlign: "left" }, { datum: "cds/layers", elementLabelBy: "layer_label", labelAlign: "left" }]}
          fields={[
            "limit_case_priced",
            "excess_case_priced",
            "brokerage_case_priced",

            null,
            "bound_premium",
            // { field: "bound_rate", shownBy: "cds/glsn_masking" },
            "section_reference",
            "status.input",
            // "written_line",

            null,
            "bpi_case_priced",
            "tpi",
            "net_written_premium",
            "benchmark_premium",
            "technical_premium",
          ]}
          filter={"show_row"}
          freezeLeft={0}
          kb-interactive
        // transpose
        />

      </HX.Section>

      <HX.Section title="Case Pricing Analysis Filepath" shownBy="cds/standard_fields/is_case_priced">
        <HX.Notes field="cds/case_pricing_analysis_location" />
      </HX.Section>


      <HX.Section title="Schedule Modifiers" shownBy="cds/standard_fields/is_rater_priced">
        <HX.Table shownBy="/cds/gmm_masking"
          data={gmm_schedule_mods()}
          fields={["min", "max", "value", "comment"]}
          with="cds/modifiers/gmm"
          kb-interactive
        />

        <HX.Table shownBy="/cds/glsn_masking"
          data={glsn_schedule_mods()}
          fields={["min", "max", "value", "comment"]}
          with="cds/modifiers/glsn"
          kb-interactive
        />

      </HX.Section>
    </HX.Page >

  )
}


export { vw_rating_summary };