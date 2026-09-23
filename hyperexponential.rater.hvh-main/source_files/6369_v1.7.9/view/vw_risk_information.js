import * as HX from "hx-model-components";


function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information">
      <HX.Section title="Account Details">
        <HX.Pane >
          <HX.Pane flow="right">
            <HX.Collection fields={["inception_date", "expiry_date"]} with="hx_core" horizontal />
            <HX.Button title="Auto-Set Expiry Date (1 Year)" task="set_expiry_date_to_one_year" />
          </HX.Pane>
          <HX.Collection fields={["underwriter", "benchmark_class"]} with="cds/standard_fields" horizontal />
          <HX.Collection fields={["cds/standard_fields/insured_name"]} horizontal />
          {/* <HX.Collection fields={["cds/standard_fields/policy_reference", "cds/expiring_policy_reference", "cds/currencies/source_currency", "cds/standard_fields/is_renewal"]} horizontal / >*/}
          <HX.Pane flow="right">
            <HX.Collection fields={["cds/standard_fields/policy_reference"]} />
            {/* <HX.Button title="Update Policy Reference" task="set_policy_reference" /> */}
            {/* <HX.Collection fields={["cds/expiring_policy_reference"]} shownBy="cds/standard_fields/is_renewal" /> */}
            <HX.Collection fields={["cds/standard_fields/is_renewal"]} />
          </HX.Pane>
          <HX.Collection fields={["cds/rating_factors/product_line"]} />
        </HX.Pane>
      </HX.Section>
      {/* NOTE use the below code if the model does not price multiple layers and it is required to store line size
        brokerage & status on teh risk Information sheet */}
      {/* <HX.Section title="Policy Information" >
        <HX.Pane>
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection fields={["written_line", "brokerage", "status"]} horizontal />
          </HX.With>
        </HX.Pane>
      </HX.Section> */}
      <HX.Section title="Broker Details">
        <HX.Collection fields={[
          { field: "cds/standard_fields/broker", shownBy: "cds/validation/broker/valid" },
          { field: "cds/standard_fields/broker.notSupported", shownBy: "cds/validation/broker/invalid", infoBy: "cds/validation/broker/info_text" },
          "cds/broker_contact",
          "cds/brokerage"
        ]} horizontal />
      </HX.Section>
      <HX.Section title="Geography">
        <HX.Collection fields={[
          "street_number",
          "street_name",
          "zip",
          "city",
          // { field: "city", shownBy: "/cds/validation/city/valid" },
          // { field: "city.notSupported", shownBy: "/cds/validation/city/invalid", infoBy: "/cds/validation/city/info_text" },
        ]} with="cds/rating_factors" horizontal />
        <HX.Collection fields={["state", "county", "distance_to_coast_options"]} with="cds/rating_factors" horizontal />
      </HX.Section>

    </HX.Page >
  )
}

export { vw_risk_information };


