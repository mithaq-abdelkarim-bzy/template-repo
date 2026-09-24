// # v0.5.1
import * as HX from "hx-model-components";


function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information" viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Rating Model">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology", "cds/metadata/rater"]} horizontal />

        </HX.Pane>
      </HX.Section>
      {vw_risk_information_steer(scale)}
      <HX.Section title="Broker Details">
        <HX.Collection fields={["cds/standard_fields/broker", "cds/risk_information/broker_contact"]} horizontal />
      </HX.Section>
      <HX.Section title="Comments">
        <HX.Notes field="cds/risk_information/comments" />
      </HX.Section>
    </HX.Page >
  )
}


function vw_risk_information_steer() {
  return (
    <HX.With context={{ type: "struct", path: "cds" }}>
      <HX.Section title="Account Details">
        <HX.Pane >
          <HX.Collection fields={["inception_date", "expiry_date"]} with="/hx_core" horizontal />
          <HX.Collection fields={["underwriter", "benchmark_class"]} with="standard_fields" horizontal />
          <HX.Collection fields={["standard_fields/insured_name"]} horizontal />
          <HX.Collection fields={["standard_fields/policy_reference", "currencies/source_currency", "standard_fields/is_renewal"]} horizontal />
          <HX.Collection fields={["select_class", "cob_reference", null]} with="technical_price_assumptions" horizontal />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Other Account Details" shownBy="/model_state/is_steer">
        <HX.Pane >

          <HX.Collection fields={["basis"]} with="steer/risk_information" horizontal />

        </HX.Pane>
      </HX.Section>
      <HX.Section title="Advanced Features" shownBy="/model_state/show_rater_priced">
        <HX.Pane>
          <HX.Collection fields={[
            "include_aad",
            "include_loss_corridor",
            "include_ncb",
            // "include_swing_rates", 
            // "include_profit_commission"
            { field: "include_swing_rates", infoBy: "/model_state/info_by_include_swing_rates" },
            { field: "include_profit_commission", infoBy: "/model_state/info_by_include_pc" }
          ]} with="/cds/risk_information" horizontal />
        </HX.Pane>
      </HX.Section>
    </HX.With>

  )
}

export { vw_risk_information };


