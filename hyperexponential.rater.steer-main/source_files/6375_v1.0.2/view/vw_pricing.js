// # v0.5.1
import * as HX from "hx-model-components";

function vw_pricing(scale) {
  return (
    <HX.Page title="Pricing Assumptions" viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Layer (Up to 5 layers)">
        <HX.Pane shownBy="model_state/is_steer">
          <HX.Collection fields={[
            "model_state/is_steer_experience_rating", null, null
          ]} horizontal
          />
        </HX.Pane>
        <HX.Pane>
          <HX.Table
            title="Quoted Layers"
            with="cds"
            data={[{ datum: "layers", width: 250 }]}
            fields={[
              "status",
              null,
              "currency",
              "epi_100",
              null,
              "limit",
              "excess",
              // "deductible",
              null,
              "rate",
              "upfront_premium_gross_100",
              // "quoted_premium_100",
              null,
              "brokerage",
              "ceding_commission",
              // "ncb",
              // "profit_commission_rate",
              // "expense_allowance",
              { field: "ncb", shownBy: "/cds/risk_information/include_ncb" },
              { field: "profit_commission_rate", shownBy: "/cds/risk_information/include_profit_commission" },
              { field: "expense_allowance", shownBy: "/cds/risk_information/include_profit_commission" },
              "bkg_gross_or_net",
              null,
              "written_line",
              "line_size",
              null,
              "cap_gross_pct",
              "loss_cap_used",
              null,
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
            ]}

            kb-interactive
            //dynamic // filter and sort
            transpose
          />
          <HX.Pane shownBy="/cds/risk_information/include_aad">
            <HX.Table
              title="AAD"
              with="cds"
              data={[{ datum: "layers", width: 250 }]}
              fields={[
                "advanced_features_input/aad",
              ]}

              kb-interactive
              //dynamic // filter and sort
              transpose
              rowHeaderSettings={{ width: 260 }}
              syncColumnWidthsKey="field"
            />
          </HX.Pane>
          <HX.Pane shownBy="/cds/risk_information/include_loss_corridor">
            <HX.Table
              title="Loss Corridor"
              with="cds"
              data={[{ datum: "layers", width: 250 }]}
              fields={[
                "loss_corridor/min_rate",
                "loss_corridor/max_rate",
                "loss_corridor/insured_participation",
              ]}

              kb-interactive
              //dynamic // filter and sort
              transpose
              rowHeaderSettings={{ width: 260 }}
              syncColumnWidthsKey="field"
            />
          </HX.Pane>
          <HX.Pane shownBy="/cds/risk_information/include_swing_rates">
            <HX.Table
              title="Swing Rates"
              with="cds"
              data={[{ datum: "layers", width: 250 }]}
              fields={[
                "swing_rates/swing_brokerage",
                "swing_rates/use_swing_brokerage",
                "swing_rates/deposit_rate",
                "swing_rates/min_rate",
                "swing_rates/max_rate",
                "swing_rates/margin",
                "swing_rates/loading_factor",
                "swing_rates/claims_cap_pct",
              ]}
              kb-interactive
              //dynamic // filter and sort
              transpose
              rowHeaderSettings={{ width: 260 }}
              syncColumnWidthsKey="field"
            />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_pricing };