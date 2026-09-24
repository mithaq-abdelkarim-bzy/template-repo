// # v0.5.1
import * as HX from "hx-model-components";
import { convertToFieldObjects } from "view/vw_utilities";

const layer_view_fields = [
  "status",
  "currency",
  "limit",
  "excess",
  // "brokerage",
  "brokerage_inc_swing",
  "ceding_commission",
  "bkg_gross_or_net",
  "expected_aad.read_only",
  "ncb",
  "profit_commission_rate",
  "expense_allowance",
  "claim_frequency",
  "average_cost_per_claim",
  // "no_reinstatement",
  "expected_reinstatement_factor.read_only",
]


const reinstatements_fields = [
  "no_reinstatement",
  "reinstatement_pct_1",
  "reinstatement_pct_2",
  "reinstatement_pct_3",
  "reinstatement_pct_4",
  "reinstatement_pct_5",
  "reinstatement_pct_6",
  "reinstatement_pct_7",
  "reinstatement_pct_8",
  "reinstatement_pct_9",
  "reinstatement_pct_10",
]

const tp_fields = [
  "benchmark_loss_ratio",
  "claims_handling_expenses",
  "fixed_expenses",
  "variable_expenses",
  "investment_income",
  "cost_of_ri",
  "return_on_capital",
  "capital_cost",
  "non_modelled_perils_nmp"
]

function vw_rating_summary(scale) {
  return (
    // NOTE: Use the line below for review only
    // <HX.Page title="Rating Summary" fullWidth={true} shownBy="model_state/show_rate_change_layer_no_ia_use">
    <HX.Page title="Rating Summary" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page" >
      <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Summary">
        <HX.Table
          title="Priced Quotes"
          data={[
            { datum: "cds/layers", width: 150 },
            null,
            { datum: "cds/programme_all", width: 150 },
            null,
            { datum: "cds/programme_selected", width: 150 }
          ]}
          fields={[
            "status",
            "include_layer",
            "section_reference",
            "currency",
            "limit",
            "excess",
            "epi_100",
            "rate",
            { field: "bpi_case_priced", shownBy: "cds/standard_fields/is_case_priced" },
            null,
            { field: "pure_rate", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "expected_loss", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "expected_losses_after_loss_sensitive_features", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "expected_loss_inc_nmp", shownBy: "cds/standard_fields/is_rater_priced" },
            null,
            { field: "upfront_premium_gross_100", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "expected_premium_paid_gross_100", shownBy: "cds/standard_fields/is_rater_priced" },
            "quoted_premium_100",
            "benchmark_premium_100",
            "technical_premium_100",
            null,
            { field: "upfront_premium_net_100", shownBy: "cds/standard_fields/is_rater_priced" },
            { field: "expected_premium_paid_net_100", shownBy: "cds/standard_fields/is_rater_priced" },
            "quoted_premium_net_100",
            "benchmark_premium_net_100",
            "technical_premium_net_100",
            null,
            "written_line",
            "quoted_premium",
            null,
            "line_size",
            "bpi",
            "tpi",
            null,
            "pflr",
            "glr",
            "roc"


          ]}
          freezeLeft={0}
          transpose
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Layer View" shownBy="cds/standard_fields/is_rater_priced">
        <HX.Table
          // title="Priced Quotes"
          data={[
            "cds/layers"
          ]}
          fields={[
            ...convertToFieldObjects(layer_view_fields, 150),
            // "expected_aad",
            // "ncb",
            // "profit_commission_rate",
            // "expense_allowance",
            // "claim_frequency",
            // "average_cost_per_claim",
            // // "no_reinstatement",
            // "expected_reinstatement_factor",
          ]}
          freezeLeft={4}
          // transpose
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Reinstatements">
        <HX.Table
          // title="Priced Quotes"
          data={[
            "cds/layers"
          ]}
          fields={[
            ...convertToFieldObjects(reinstatements_fields, 150)
          ]}
          freezeLeft={0}
          // transpose
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Technical Price Assumptions">
        <HX.Table
          // title="Priced Quotes"
          data={[
            // "cds/layers"
            "cds/technical_price_assumptions"
          ]}
          fields={[
            ...convertToFieldObjects(tp_fields)
          ]}
          freezeLeft={0}
          // transpose
          kb-interactive
        />
      </HX.Section>
      {/* <HX.Section title="Case Pricing Analysis Filepath" shownBy="cds/standard_fields/is_case_priced"> */}
      <HX.Section title="Case Pricing Analysis Filepath" >
        <HX.Notes field="cds/risk_information/case_pricing_analysis_location" />
      </HX.Section>
    </HX.Page >

  )
}


export { vw_rating_summary };