import * as HX from "hx-model-components";
import { render_notifications } from "view/results_tables";

function rationale() {
  return (
    <HX.Page title="Rationale" fullWidth={true} shownBy="model_state/show_after_landing_page">
      {render_notifications()}
      <HX.Section title="Risk Information">
        <HX.Collection fields={["rationale/fill_rationale"]} />
        <HX.Pane flow="right">
          <HX.Collection fields={["rationale/layers"]} shownBy="rationale/show_dropdown" />
          <HX.Collection fields={["rationale/bound_layer"]} shownBy="rationale/show_bound" />
          <HX.Collection fields={["rationale/layer_label"]} />

          <HX.Collection fields={["rationale/first_saved.read_only"]} />
          <HX.Button task="update_first_saved_task" title="Save" shownBy="rationale/show_save_button" />
          <HX.Collection fields={["rationale/button_text.read_only"]} shownBy="rationale/show_button_text" />
        </HX.Pane>

        <HX.Collection fields={["risk_name", "policy_period_start", "policy_period_end"]} with="rationale/risk_information" horizontal />
        <HX.Collection fields={["policy_ref", "underwriter", "broker"]} with="rationale/risk_information" horizontal />
        <HX.Collection fields={["occupancy", "tiv", "new_renewal"]} with="rationale/risk_information" horizontal />
      </HX.Section>

      <HX.Section title="Rating & Terms">
        <HX.Pane>
          <HX.Table
            data={["rationale/rating_terms"]}
            fields={[
              "insurance_type",
              "limit",
              "excess",
              "written_line",
              "afb_exposure"
            ]}
          />
          <HX.Collection fields={["achieved_premium_100_gg", "commission", "rate_change"]} with="rationale/rating_terms_2" horizontal />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Natural Perils">
        <HX.Pane flow="right" reflow={true}>
          <HX.Table
            data={["fire", "windstorm", "eq", "wildfire", "scs", "flood"]}
            fields={["limit", "deductible", "complex_ded_structure", "premium"]}
            with="rationale/natural_perils"
            kb-interactive />
          <HX.Pane>
            <HX.Collection fields={["rationale/natural_perils/tpi_post_uw_adj"]} horizontal />
            <HX.Notes title="Adj factor (reason)" field="rationale/natural_perils/adj_factor_reason" stretch />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Reinsurance">
        <HX.Pane>
          <HX.Collection fields={["consortium", "fac_purchased"]} with="rationale/reinsurance" horizontal />
          <HX.Notes title="FAC Structure" field="rationale/reinsurance/fac_structure" shownBy="rationale/reinsurance/fac_purchased" />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Notes">
        <HX.Notes title="Description" field="rationale/note_section/description" />
        <HX.Notes title="Special Processing" field="rationale/note_section/special_processing" />
        <HX.Notes title="Underwriter Thoughts" field="rationale/note_section/underwriter_thoughts" />

        <HX.Button task="generate_uw_rationale_doc_task" title="Generate UW Rationale Document" />
        <HX.File field="rationale/document" />
      </HX.Section>

    </HX.Page >
  )
}

export { rationale };
