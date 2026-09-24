import * as HX from "hx-model-components";


function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information" shownBy="model_state/show_after_landing_page">
      <HX.Section title="Account Details">
        <HX.Pane>
          {/* NOTE  uncomment if rater requires databse_id to be displayed */}
          {/* <HX.Collection fields={["database_id"]} with="cds" horizontal /> */}
          <HX.Collection fields={["inception_date", "expiry_date"]} with="hx_core" horizontal />
          <HX.Collection fields={["underwriter"]} with="cds/standard_fields" horizontal />
          <HX.Collection fields={["cds/standard_fields/insured_name"]} horizontal />
          <HX.Collection fields={["cds/standard_fields/policy_reference", "cds/currencies/source_currency", "cds/standard_fields/is_renewal"]} horizontal />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/is_admitted_or_surplus"]} />
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection fields={["is_primary_excess"]} />
          </HX.With>

        </HX.Pane>
      </HX.Section>
      {/* NOTE use the below code if the model does not price multiple layers and it is required to store line size
        brokerage & status on the risk Information sheet */}
      <HX.Section title="Broker Details">
        <HX.Collection fields={["cds/standard_fields/broker", "cds/broker_contact"]} horizontal />
      </HX.Section>
    </HX.Page >
  )
}

export { vw_risk_information };


