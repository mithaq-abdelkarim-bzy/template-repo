/* eslint-disable */
import * as HX from "hx-model-components";

function vw_risk_information() {
  return (
    <HX.Page title="Risk Information" shownBy="model_state/show_after_landing_page">
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
        <HX.Section title="Account Details">
          <HX.Pane>
            <HX.Pane ratio={1}>
              <HX.Collection fields={["/hx_core/inception_date", "/hx_core/expiry_date"]} horizontal />
            </HX.Pane>
            <HX.Pane>
              <HX.Collection fields={["/cds/standard_fields/underwriter", "status"]} horizontal />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Collection fields={["/cds/standard_fields/insured_name", "/cds/standard_fields/policy_reference"]} horizontal />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane>
            <HX.Collection fields={["/cds/standard_fields/is_admitted_or_surplus", "is_primary_excess", "brokerage"]} horizontal />
            <HX.Collection fields={["/hx_core/premium_currency", "/cds/standard_fields/is_renewal", null]} horizontal />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Broker Details">
          <HX.Collection fields={["/cds/standard_fields/broker", "/cds/broker_contact"]} horizontal />
        </HX.Section>
      </HX.With>
    </HX.Page >
  )
}

export { vw_risk_information };
