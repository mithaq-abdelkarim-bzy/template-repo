import * as HX from "hx-model-components";
import { render_notifications } from "view/results_tables";

function rate_change() {
  return (
    <HX.Page title="Rate Change" fullWidth={true} shownBy="model_state/show_after_landing_page">
      {render_notifications()}
      <HX.Section>
        <HX.Pane flow="right">
          <HX.Collection fields={[
            "rate_change/expiring_policy_option_id",
          ]} />
          <HX.Button task="expiring_policy_fetch_task" title="Fetch Expiring Data" />
        </HX.Pane>
        <HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              // "policy_information/insured_output",
              "rate_change/layer/renewal",
              "rate_change/layer/expiring",
            ]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection title="Premium - Policy Term (100% Share)" fields={[
              "renewal",
              "expiring",
            ]} with="rate_change/premium_policy_term_100pct" />
            <HX.Collection title="Premium - Policy Term (Beazley Share)" fields={[
              "renewal",
              "expiring",
            ]} with="rate_change/premium_policy_term" />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection title="Premium - Annualized (100% Share)" fields={[
              "renewal",
              "expiring",
            ]} with="rate_change/premium_annualized_100pct" />
            <HX.Collection title="Premium - Annualized (Beazley Share)" fields={[
              "renewal",
              "expiring",
            ]} with="rate_change/premium_annualized" />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection title="BPro Premium"
              fields={[
                "rate_change/expiring_bpro_premium",
              ]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
      <HX.Section title="UW Rate Change">
        <HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection title="Model %"
              fields={[
                "exposure_change/ratio",
                "risk_characteristics_change/ratio",
                "deductible_change/ratio",
                "limit_change/ratio",
                "terms_and_conditions_change/ratio",
                "other_change/ratio",
              ]} with="rate_change" />
            <HX.Collection title="UW Selected %"
              fields={[
                "exposure_change/ratio_uw",
                "risk_characteristics_change/ratio_uw",
                "deductible_change/ratio_uw",
                "limit_change/ratio_uw",
                "terms_and_conditions_change/ratio_uw",
                "other_change/ratio_uw",
              ]} with="rate_change" />
            <HX.Collection title="Comments"
              fields={[
                "exposure_change/comments",
                "risk_characteristics_change/comments",
                "deductible_change/comments",
                "limit_change/comments",
                "terms_and_conditions_change/comments",
                "other_change/comments",
              ]} with="rate_change" />
            <HX.Collection title="Renewal"
              fields={[
                "exposure_change/renewal",
                "risk_characteristics_change/renewal",
                "deductible_change/renewal",
                "limit_change/renewal",
                "terms_and_conditions_change/renewal",
                "other_change/renewal_brokerage",
                "other_change/renewal_signed_line",
              ]} with="rate_change" />
            <HX.Collection title="Expiring"
              fields={[
                "exposure_change/expiring",
                "risk_characteristics_change/expiring",
                "deductible_change/expiring",
                "limit_change/expiring",
                "terms_and_conditions_change/expiring",
                "other_change/expiring_brokerage",
                "other_change/expiring_signed_line",
              ]} with="rate_change" />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection title="Rate Changes"
              fields={[
                "total_factor/technical",
                "risk_adjusted_rate_change/technical",
                "simple_rate_change"
              ]} with="rate_change" />
            <HX.Collection title="Underwriter Selected"
              fields={[
                "total_factor/underwriter",
                "risk_adjusted_rate_change/underwriter"
              ]} with="rate_change" />
            <HX.Pane />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>

    </HX.Page >
  )
}

export { rate_change };