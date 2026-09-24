import * as HX from "hx-model-components";


function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information" shownBy="model_state/show_after_landing_page">
      <HX.Section title="Account Details">
        <HX.Pane >
          {/* NOTE  uncomment if rater requires databse_id to be displayed */}
          <HX.Collection fields={["database_id"]} with="cds" horizontal />
          <HX.Collection fields={["inception_date", "expiry_date"]} with="hx_core" horizontal />
          <HX.Collection fields={["underwriter", "benchmark_class"]} with="cds/standard_fields" horizontal />
          <HX.Collection fields={["cds/standard_fields/insured_name", "cds/ccy", "cds/standard_fields/is_renewal"]} horizontal />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Location">
        <HX.Table title="Location Input"
          data={["cds/rating_factors/location/states", null, "cds/rating_factors/location"]}
          fields={["state", { field: "percentage", shownBy: "/noncds/validation/location_percentage/valid" }, { field: "percentage.notSupported", shownBy: "/noncds/validation/location_percentage/invalid", infoBy: "/noncds/validation/location_percentage/info_text" }, "risk_group", "state_factor_selected"]}
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Broker Details">
        <HX.Collection fields={["cds/standard_fields/broker", "cds/broker_contact", "cds/brokerage"]} horizontal />
      </HX.Section>
    </HX.Page >
  )
}

export { vw_risk_information };



