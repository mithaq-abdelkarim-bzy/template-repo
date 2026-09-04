import * as HX from "hx-model-components";


function vw_risk_information(scale) {
  return (
    <HX.Page title="Risk Information" shownBy="model_state/show_after_landing_page">
      <HX.Section title="Account Details">
        <HX.Pane >
          <HX.Collection fields={["inception_date", "expiry_date"]} with="hx_core" horizontal />
          <HX.Collection fields={["underwriter", "benchmark_class"]} with="cds/standard_fields" horizontal />
          <HX.Notes field="underwriter_warning" shownBy="show_underwriter_warning" with="uw_validation" />
          <HX.Collection fields={["cds/standard_fields/insured_name"]} horizontal />
          <HX.Collection fields={[
            "cds/standard_fields/policy_reference",
            "cds/currencies/source_currency",
            "cds/standard_fields/is_renewal"
          ]} horizontal />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Policy Information" >
        <HX.Pane>
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection fields={["written_line", "brokerage", "status"]} horizontal />
          </HX.With>
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Broker Details">
        <HX.Collection fields={["cds/standard_fields/broker", "cds/broker_contact"]} horizontal />
      </HX.Section>
      <HX.Section title="Policy Document" >
        <HX.Button task="policy_to_excel_task" title="Generate Policy Document" shownBy="policy_doc/show_generate_button" />
        <HX.Notes field="policy_doc/premium_check" shownBy="policy_doc/show_premium_check" />
        <HX.File
          with="policy_doc"
          field="output_file"
          title="Click on the icon below to download the policy document"
          shownBy="show_download" />
      </HX.Section>
    </HX.Page >
  )
}

export { vw_risk_information };


