import * as HX from "hx-model-components";

function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information" fullWidth={false} viewScale={scale}>
      <HX.With context={{ type: "struct", path: "cds" }}>
        <HX.Section title="Account Details">
          <HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection with="/hx_core" fields={["inception_date", "expiry_date"]} horizontal />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Collection fields={["standard_fields/underwriter"]} />
              <HX.Pane />
            </HX.Pane>
            <HX.Collection fields={["standard_fields/insured_name"]} />
            <HX.Pane flow="right">
              <HX.Collection
                with="standard_fields"
                fields={["policy_reference", "is_renewal"]}
                horizontal
              />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Broker Details">
          <HX.Pane flow="right">
            <HX.Collection fields={["standard_fields/broker", "broker_contact"]} horizontal />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Coverage Selection">
          <HX.Pane>
            <HX.Collection with="account_details"
              fields={[
                "product_type",
                "retroactive_years/years"
              ]}
              horizontal />
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page>
  );
}

export { vw_risk_information };
