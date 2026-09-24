import * as HX from "hx-model-components";


function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information" shownBy="model_state/show_after_landing_page">

      <HX.Section title="Account Details">
        <HX.Pane >
          <HX.Collection fields={["hx_core/inception_date", "hx_core/expiry_date", "cds/retroactive_date", "cds/application_date"]} horizontal />
          <HX.Collection fields={["underwriter", "insured_name"]} with="cds/standard_fields" horizontal />
        </HX.Pane>
        {/* <HX.Pane flow="right">
          <HX.Collection fields={["application_date", null]} with="cds" />
          <HX.Collection fields={["cds/standard_fields/policy_reference", "cds/binder_reference"]} />
        </HX.Pane> */}
      </HX.Section>

      <HX.Section title="Risk Details">
        <HX.Pane>
          <HX.Collection fields={["cds/currencies/source_currency", "cds/standard_fields/is_renewal"]} horizontal />
          <HX.Collection fields={["clearance_status", "coverage_name"]} with="cds" horizontal />
          <HX.Collection fields={["clearance_date", "is_binder",]} with="cds" horizontal />
          <HX.Collection fields={[null, "cyber_code"]} with="cds" horizontal />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Broker Details">
        <HX.Collection fields={["cds/standard_fields/broker", "cds/broker_contact"]} horizontal />
      </HX.Section>

      <HX.Section title="Comments">
        <HX.Collection fields={["cds/riskinfo_comments"]} />
      </HX.Section>

    </HX.Page >
  )
}

export { vw_risk_information };


